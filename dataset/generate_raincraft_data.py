#!/usr/bin/env python3
"""
RainCraft Umbrellas Pvt. Ltd. — synthetic business dataset generator
=====================================================================

RainCraft is a FICTIONAL umbrella & raincoat manufacturer-distributor based in
Kolkata, selling to shops across East and North-East India (B2B) and to walk-in
customers through its own retail counters (B2C). It makes some products in its
own small factory and imports the rest from suppliers in China.

The data is simulated, but the business problems inside it are realistic:
seasonal demand, stock-outs in the monsoon, dead stock, money stuck with
credit customers, late imports, late deliveries, quality complaints, worker
absenteeism. Your job as the analyst is to find them.

Usage
-----
    python generate_raincraft_data.py --size small   --out ./datasets
    python generate_raincraft_data.py --size all     --out ./datasets

Same seed -> same data, every time.
"""
import argparse
import os
import zipfile
from collections import defaultdict, deque
from datetime import date, timedelta

import numpy as np
import pandas as pd

# ----------------------------------------------------------------------------
# Size presets
# ----------------------------------------------------------------------------
CONFIGS = {
    "small": dict(
        start="2025-04-01", end="2025-06-30", n_skus=12, n_customers=15,
        prod_workers=6, seed=120,
        stores={"Kolkata Store": ("2020-01-01", 6)},
        defect_window=("2025-04-10", "2025-05-31"),
        late_joiners=0.0, churners=0.0,
    ),
    "medium": dict(
        start="2025-04-01", end="2026-03-31", n_skus=40, n_customers=60,
        prod_workers=6, seed=202,
        stores={"Kolkata Store": ("2020-01-01", 14), "Siliguri Store": ("2020-01-01", 10)},
        defect_window=("2025-06-01", "2025-08-15"),
        late_joiners=0.10, churners=0.05,
    ),
    "huge": dict(
        start="2023-04-01", end="2026-03-31", n_skus=80, n_customers=300,
        prod_workers=18, seed=303,
        stores={
            "Kolkata Store": ("2020-01-01", 90),
            "Siliguri Store": ("2020-01-01", 60),
            "Guwahati Store": ("2024-06-01", 70),
            "WhatsApp Orders": ("2025-01-01", 25),
        },
        defect_window=("2025-01-10", "2025-03-31"),
        late_joiners=0.30, churners=0.10,
    ),
}

# ----------------------------------------------------------------------------
# Master data building blocks
# ----------------------------------------------------------------------------
# (category, code, cost range, share of SKUs, season type, imported share, lines)
CATEGORIES = [
    ("3-Fold Umbrella", "3F", (150, 240), 0.28, "rain", 0.25, ["Classic", "Breeze", "Compact", "Storm"]),
    ("2-Fold Umbrella", "2F", (190, 300), 0.16, "rain", 0.30, ["Classic", "Breeze"]),
    ("Long Umbrella", "LG", (220, 380), 0.16, "rain", 0.50, ["Auto-Open", "Heritage", "Storm"]),
    ("Kids Umbrella", "KD", (110, 180), 0.10, "rain", 0.40, ["Kiddo"]),
    ("Golf Umbrella", "GF", (420, 650), 0.06, "rain", 1.00, ["Pro"]),
    ("Raincoat", "RC", (260, 520), 0.12, "monsoon", 0.30, ["Shield"]),
    ("UV Sun Umbrella", "UV", (230, 360), 0.12, "summer", 0.60, ["SunGuard"]),
]
COLOURS = ["Black", "Navy Blue", "Maroon", "Floral Print", "Polka Dot", "Transparent",
           "Red", "Bottle Green", "Grey", "Sky Blue", "Checks", "Beige"]
KIDS_COLOURS = ["Cartoon Print", "Red", "Polka Dot", "Sky Blue", "Pink", "Yellow"]

# Month index 1..12 -> demand multiplier (retail view)
SEASON = {
    "rain":    [0, .20, .25, .50, .80, 1.3, 1.9, 2.0, 1.6, 1.1, .50, .25, .20],
    "monsoon": [0, .10, .10, .20, .40, 1.0, 2.4, 2.6, 2.0, 1.0, .30, .10, .10],
    "summer":  [0, .20, .40, 1.2, 2.0, 2.0, 1.0, .50, .50, .50, .40, .20, .20],
}
# Owner's production plan by month (not demand-driven on purpose)
PROD_PLAN = [0, 1.1, 1.2, 1.3, 1.3, 1.3, 1.2, 1.0, .8, .7, .6, .8, 1.0]

ZONES = {
    # zone: (cities with state, promise_days, transit range)
    "South Bengal": ([("Kolkata", "West Bengal"), ("Howrah", "West Bengal"), ("Durgapur", "West Bengal"),
                      ("Asansol", "West Bengal"), ("Bardhaman", "West Bengal"), ("Kharagpur", "West Bengal")], 3, (1, 2)),
    "North Bengal": ([("Siliguri", "West Bengal"), ("Jalpaiguri", "West Bengal"), ("Cooch Behar", "West Bengal"),
                      ("Malda", "West Bengal"), ("Gangtok", "Sikkim")], 4, (1, 3)),
    "North-East": ([("Guwahati", "Assam"), ("Dibrugarh", "Assam"), ("Silchar", "Assam"), ("Jorhat", "Assam"),
                    ("Tezpur", "Assam"), ("Shillong", "Meghalaya"), ("Agartala", "Tripura"), ("Dimapur", "Nagaland"),
                    ("Imphal", "Manipur"), ("Aizawl", "Mizoram"), ("Itanagar", "Arunachal Pradesh")], 6, (2, 5)),
    "Other East": ([("Patna", "Bihar"), ("Bhagalpur", "Bihar"), ("Purnia", "Bihar"), ("Ranchi", "Jharkhand"),
                    ("Jamshedpur", "Jharkhand"), ("Bhubaneswar", "Odisha"), ("Cuttack", "Odisha")], 5, (2, 4)),
}
ZONE_WEIGHTS = {"South Bengal": 0.25, "North Bengal": 0.20, "North-East": 0.40, "Other East": 0.15}
SALES_REPS = {"South Bengal": ["Amit Sarkar"], "North Bengal": ["Rina Das"],
              "North-East": ["Bikash Roy", "Priyanka Baruah"], "Other East": ["Rakesh Singh"]}

NAME_A = ["Maa Tara", "Sri Durga", "New", "Shree Ganesh", "Laxmi", "Bharat", "Purbanchal", "Brahmaputra",
          "Kamakhya", "Annapurna", "Jai Hind", "Royal", "Modern", "City", "Rainbow", "Sunrise", "Himalaya",
          "Teesta", "Ganga", "Barak", "Lokenath", "Sai", "Om", "Krishna", "Mahamaya", "Biswakarma", "Sonali",
          "Rupali", "Janata", "Popular", "Diamond", "Star", "Kalyani", "Saraswati", "Jagannath", "Hanuman"]
NAME_B = ["Traders", "Enterprises", "Stores", "Distributors", "Agencies", "Umbrella House", "Bastralaya",
          "General Store", "Wholesale", "& Sons", "Trading Co.", "Emporium", "Bazaar", "Marketing"]

SUPPLIERS = [
    ("S01", "Shangyu Sunrise Umbrella Co.", "China", 45),
    ("S02", "Xiamen Bluesky Rain Gear Ltd.", "China", 50),
    ("S03", "Ningbo Brightway Umbrella Co.", "China", 40),   # the problem supplier
    ("S04", "Shaoxing Evergreen Textiles", "China", 55),
]
DEFECT_SUPPLIER = "S03"

# Factory closed (festivals / national holidays). Synthetic calendar, approximate.
CLOSED_DAYS = set()
for d1, d2 in [("2023-10-21", "2023-10-24"), ("2024-10-10", "2024-10-13"), ("2025-09-29", "2025-10-02")]:
    for x in pd.date_range(d1, d2):
        CLOSED_DAYS.add(x.date())
for s in ["2023-11-12", "2024-10-31", "2025-10-20",          # Kali Puja / Diwali
          "2024-03-25", "2025-03-14", "2026-03-03",          # Dol / Holi
          "2023-04-14", "2024-04-14", "2025-04-14",          # Poila Baisakh / Bohag Bihu
          "2023-08-15", "2024-08-15", "2025-08-15",
          "2024-01-26", "2025-01-26", "2026-01-26",
          "2023-12-25", "2024-12-25", "2025-12-25", "2024-01-01", "2025-01-01", "2026-01-01"]:
    CLOSED_DAYS.add(date.fromisoformat(s))
# High-absenteeism windows (workers travel home: Puja, Chhath, Bihu, harvest)
ABSENT_WINDOWS = [("2023-10-14", "2023-10-28"), ("2024-10-03", "2024-10-17"), ("2025-09-22", "2025-10-06"),
                  ("2023-11-17", "2023-11-21"), ("2024-11-05", "2024-11-09"), ("2025-10-25", "2025-10-29"),
                  ("2023-04-12", "2023-04-18"), ("2024-04-12", "2024-04-18"), ("2025-04-12", "2025-04-18"),
                  ("2024-01-13", "2024-01-17"), ("2025-01-13", "2025-01-17"), ("2026-01-13", "2026-01-17")]
PUJA_SHOPPING = [("2023-10-07", "2023-10-20"), ("2024-09-26", "2024-10-09"), ("2025-09-15", "2025-09-28")]


def in_windows(d, windows):
    return any(date.fromisoformat(a) <= d <= date.fromisoformat(b) for a, b in windows)


def fy_multiplier(d):
    """Prices in the product master are FY2025-26 prices; earlier years were ~6% cheaper per year."""
    fy_start_year = d.year if d.month >= 4 else d.year - 1
    return 1.06 ** (fy_start_year - 2025)


# ----------------------------------------------------------------------------
# Generator
# ----------------------------------------------------------------------------
class RainCraftSim:
    def __init__(self, size):
        self.size = size
        self.cfg = CONFIGS[size]
        self.rng = np.random.default_rng(self.cfg["seed"])
        self.start = date.fromisoformat(self.cfg["start"])
        self.end = date.fromisoformat(self.cfg["end"])
        self.days = [x.date() for x in pd.date_range(self.start, self.end)]

    # ---------------- master data ----------------
    def make_products(self):
        rng, n = self.rng, self.cfg["n_skus"]
        counts = [max(1, int(round(c[3] * n))) for c in CATEGORIES]
        while sum(counts) > n:
            counts[int(np.argmax(counts))] -= 1
        while sum(counts) < n:
            counts[0] += 1
        rows, used = [], set()
        for (cat, code, (lo, hi), _, season, imp_share, lines), k in zip(CATEGORIES, counts):
            for i in range(k):
                for _ in range(50):
                    line = rng.choice(lines)
                    colour = rng.choice(KIDS_COLOURS if code == "KD" else COLOURS)
                    name = f"{line} {cat.replace(' Umbrella', '')} - {colour}"
                    if name not in used:
                        used.add(name)
                        break
                imported = rng.random() < imp_share
                cost = round(float(rng.uniform(lo, hi)) * (1.12 if imported else 1.0), 0)
                wholesale = round(cost * rng.uniform(1.30, 1.55) / 5) * 5
                mrp = round(wholesale * rng.uniform(1.55, 1.85) / 10) * 10 - 1
                rows.append(dict(
                    sku=f"RC-{code}-{i + 1:02d}", product_name=name, category=cat,
                    made_in="Imported" if imported else "In-house",
                    supplier_id=(rng.choice([s[0] for s in SUPPLIERS]) if imported else "IN-HOUSE"),
                    unit_cost=cost, wholesale_price=float(wholesale), mrp=float(mrp),
                    season_type=season,
                ))
        df = pd.DataFrame(rows)
        # make sure the problem supplier actually supplies something
        imp = df.index[df.made_in == "Imported"]
        if len(imp) and (df.supplier_id == DEFECT_SUPPLIER).sum() == 0:
            df.loc[imp[0], "supplier_id"] = DEFECT_SUPPLIER
        # popularity: lognormal, ~15% slow movers (dead-stock candidates)
        pop = rng.lognormal(0, 0.7, len(df))
        slow = rng.random(len(df)) < 0.15
        if (df.made_in == "Imported").any() and not slow[(df.made_in == "Imported").values].any():
            slow[df.index[df.made_in == "Imported"][0]] = True   # guarantee one imported slow mover
        pop[slow] *= 0.05
        df["_pop"] = pop / pop.sum()
        df["_slow"] = slow
        self.products = df

    def make_customers(self):
        rng, n = self.rng, self.cfg["n_customers"]
        zones = list(ZONE_WEIGHTS)
        rows, used = [], set()
        n_dist = max(2, int(round(0.10 * n)))
        n_whole = max(3, int(round(0.30 * n)))
        types = (["Distributor"] * n_dist + ["Wholesaler"] * n_whole + ["Retailer"] * (n - n_dist - n_whole))
        rng.shuffle(types)
        span = (self.end - self.start).days
        for i, ctype in enumerate(types):
            zone = rng.choice(zones, p=[ZONE_WEIGHTS[z] for z in zones])
            cities = ZONES[zone][0]
            city, state = cities[rng.integers(len(cities))]
            for _ in range(100):
                nm = f"{rng.choice(NAME_A)} {rng.choice(NAME_B)}"
                if (nm, city) not in used:
                    used.add((nm, city))
                    break
            credit = {"Distributor": [45, 60], "Wholesaler": [30, 45], "Retailer": [0, 0, 15, 30]}[ctype]
            credit_days = int(rng.choice(credit))
            behaviour = rng.choice(["good", "average", "slow", "defaulter"], p=[0.55, 0.30, 0.12, 0.03])
            if rng.random() < self.cfg["late_joiners"]:
                onboarded = self.start + timedelta(days=int(rng.integers(30, max(31, span - 60))))
            else:
                onboarded = self.start - timedelta(days=int(rng.integers(200, 3000)))
            churn = None
            if rng.random() < self.cfg["churners"]:
                churn = max(onboarded, self.start) + timedelta(days=int(rng.integers(90, max(91, span))))
            rows.append(dict(
                customer_id=f"C{i + 1:03d}", customer_name=nm, customer_type=ctype,
                city=city, state=state, zone=zone,
                sales_rep=rng.choice(SALES_REPS[zone]) if self.size == "huge" else SALES_REPS[zone][0],
                payment_terms="Cash" if credit_days == 0 else "Credit", credit_days=credit_days,
                credit_limit=float({"Distributor": 1_000_000, "Wholesaler": 400_000, "Retailer": 100_000}[ctype]
                                   * rng.choice([0.5, 1, 1.5])),
                onboarded_on=onboarded,
                _behaviour=behaviour, _churn=churn,
                _size=float(rng.lognormal(0, 0.35)),
            ))
        self.customers = pd.DataFrame(rows)

    # ---------------- helpers ----------------
    def season(self, stype, month):
        return SEASON[stype][month]

    def b2b_season(self, month):
        # shops stock up ~1 month before the retail peak
        return SEASON["rain"][month % 12 + 1] * 0.9 + 0.1

    def expected_daily_units(self):
        """Expected units/day per SKU, averaged over a year (used to set stock levels & production)."""
        rate = {"Distributor": 0.12, "Wholesaler": 0.07, "Retailer": 0.04}
        qty = {"Distributor": 150, "Wholesaler": 60, "Retailer": 24}
        lines = {"Distributor": 4.5, "Wholesaler": 3.0, "Retailer": 2.0}
        b2b = sum(rate[t] * lines[t] * qty[t] * sz for t, sz in
                  zip(self.customers.customer_type, self.customers["_size"]))
        b2b *= np.mean([self.b2b_season(m) for m in range(1, 13)]) * 6 / 7
        retail = sum(v[1] for v in self.cfg["stores"].values()) * 1.35 * 1.1
        return self.products["_pop"].values * (b2b + retail)

    # ---------------- simulation ----------------
    def simulate(self):
        rng = self.rng
        P = self.products.set_index("sku")
        skus = list(P.index)
        sku_season = P.season_type.to_dict()
        pop = P._pop.values
        exp_units = dict(zip(skus, self.expected_daily_units()))

        # stock & policies
        stock = {}
        for s in skus:
            if P.at[s, "_slow"] and P.at[s, "made_in"] == "Imported":
                stock[s] = int(rng.integers(900, 2000))           # owner over-bought: dead stock
            elif P.at[s, "made_in"] == "Imported":
                stock[s] = int(exp_units[s] * 90)
            else:
                stock[s] = int(exp_units[s] * 80)          # stock built up before the season
        reorder = {s: max(60, exp_units[s] * 60 * rng.lognormal(0, 0.4)) for s in skus}
        lot = {s: max(120, round(exp_units[s] * 105 * rng.lognormal(0, 0.4) / 12) * 12) for s in skus}
        for s in skus:
            if P.at[s, "_slow"]:
                lot[s] = max(lot[s], 600)                       # optimistic re-orders on slow sellers
        inhouse = [s for s in skus if P.at[s, "made_in"] == "In-house"]
        plan_share = np.array([exp_units[s] for s in inhouse]) * rng.lognormal(0, 0.35, len(inhouse))
        plan_share = plan_share / plan_share.sum() if len(inhouse) else plan_share
        workers = self.cfg["prod_workers"]
        inhouse_demand = sum(exp_units[s] for s in inhouse) * 365
        working_days = sum(1 for d in pd.date_range("2025-04-01", "2026-03-31")
                           if d.weekday() != 6) * np.mean(PROD_PLAN[1:])
        units_per_worker = max(10, 1.25 * inhouse_demand / max(1, working_days) / workers)

        queue = defaultdict(deque)       # sku -> deque of [order_id, line_no, qty]
        demand_q, q_start = defaultdict(int), self.start
        open_po = {}                     # sku -> po index
        orders, items, inv_rows, pos_counter = [], [], [], defaultdict(int)
        pos_rows, prod_rows, po_rows = [], [], []
        line_fill = {}                   # (order_id, line_no) -> fill date
        inv = defaultdict(lambda: defaultdict(int))  # (month, sku) -> fields
        month_open = {}

        cust = self.customers.to_dict("records")
        order_seq = 0
        store_prefix = {"Kolkata Store": "KOL", "Siliguri Store": "SLG", "Guwahati Store": "GHY", "WhatsApp Orders": "WAP"}
        defect_a, defect_b = (date.fromisoformat(x) for x in self.cfg["defect_window"])
        po_seq = 0

        for d in self.days:
            m = d.month
            mkey = d.strftime("%Y-%m")
            if mkey not in month_open:
                month_open[mkey] = dict(stock)
            weekday = d.weekday()

            # ---- 0. quarterly re-planning (owner reacts to last quarter, with a lag) ----
            if d.day == 1 and d.month in (1, 4, 7, 10) and d != self.start and sum(demand_q.values()):
                ndays = max(1, (d - q_start).days)
                if len(inhouse):
                    recent = np.array([demand_q[s] for s in inhouse], dtype=float) + 1
                    plan_share = 0.5 * plan_share + 0.5 * recent / recent.sum()
                for s in skus:
                    if P.at[s, "made_in"] == "Imported" and not P.at[s, "_slow"]:
                        avg = demand_q[s] / ndays
                        reorder[s] = 0.5 * reorder[s] + 0.5 * avg * 75
                        lot[s] = max(120, round((0.5 * lot[s] + 0.5 * avg * 120) / 12) * 12)
                demand_q = defaultdict(int)
                q_start = d

            # ---- 1. supply: PO arrivals ----
            for po in po_rows:
                if po["_arrival"] == d and po["status"] == "Open":
                    po["status"] = "Received"
                    po["actual_arrival_date"] = d
                    stock[po["sku"]] += po["received_qty"]
                    inv[(mkey, po["sku"])]["received_qty"] += po["received_qty"]
                    open_po.pop(po["sku"], None)

            # ---- 2. supply: factory production (Mon-Sat) ----
            if weekday != 6 and len(inhouse):
                closed = d in CLOSED_DAYS
                absent_rate = 0.30 if in_windows(d, ABSENT_WINDOWS) else 0.08
                present = 0 if closed else int(rng.binomial(workers, 1 - absent_rate))
                planned = 0 if closed else int(workers * units_per_worker * PROD_PLAN[m])
                remark = "Factory closed (holiday)" if closed else ""
                eff = rng.uniform(0.85, 1.0)
                if not closed and rng.random() < 0.03:
                    eff *= 0.6
                    remark = "Power cut"
                produced = int(planned * (present / workers) * eff) if workers else 0
                rejected = int(rng.binomial(produced, 0.02)) if produced else 0
                good = produced - rejected
                if not closed and present < workers * 0.75 and not remark:
                    remark = "High absenteeism"
                prod_rows.append(dict(date=d, workers_scheduled=workers, workers_present=present,
                                      planned_units=planned, produced_units=produced,
                                      rejected_units=rejected, remarks=remark))
                if good:
                    backlog = np.array([sum(x[2] for x in queue[s]) for s in inhouse], dtype=float)
                    share = plan_share
                    if backlog.sum() > 0:           # supervisor pushes urgent backorders
                        share = 0.6 * plan_share + 0.4 * backlog / backlog.sum()
                    alloc = rng.multinomial(good, share / share.sum())
                    for s, q in zip(inhouse, alloc):
                        stock[s] += int(q)
                        inv[(mkey, s)]["produced_qty"] += int(q)

            # ---- 3. purchase orders (5th of month, imported SKUs) ----
            if d.day == 5:
                for s in skus:
                    if P.at[s, "made_in"] != "Imported" or s in open_po:
                        continue
                    if stock[s] < reorder[s]:
                        sup = P.at[s, "supplier_id"]
                        promised = [x[3] for x in SUPPLIERS if x[0] == sup][0]
                        delay = int(np.clip(rng.normal(5, 7), -3, 40))
                        if (d.month == 12 and d.day >= 5) or d.month in (1,):
                            delay += int(rng.integers(15, 31))       # Chinese New Year shutdown
                        if rng.random() < 0.08:
                            delay += int(rng.integers(10, 25))       # port congestion
                        qty = int(lot[s])
                        recv = qty if rng.random() > 0.05 else int(qty * rng.uniform(0.8, 0.95))
                        po_seq += 1
                        po_rows.append(dict(
                            po_id=f"PO{po_seq:04d}", supplier_id=sup, sku=s, po_date=d,
                            ordered_qty=qty, unit_cost=round(P.at[s, "unit_cost"] * fy_multiplier(d), 2),
                            promised_arrival_date=d + timedelta(days=promised),
                            actual_arrival_date=None, received_qty=recv, status="Open",
                            _arrival=d + timedelta(days=promised + delay),
                        ))
                        open_po[s] = po_seq

            # ---- 4. serve backorders first ----
            for s in skus:
                q = queue[s]
                if not q or stock[s] <= 0:
                    continue
                keep = deque()
                while q:                       # oldest first; skip lines that don't fit yet
                    oid, ln, qty = q.popleft()
                    if stock[s] >= qty:
                        stock[s] -= qty
                        line_fill[(oid, ln)] = d
                        inv[(mkey, s)]["b2b_shipped_qty"] += qty
                    else:
                        keep.append([oid, ln, qty])
                queue[s] = keep

            # ---- 5. new B2B orders (Mon-Sat) ----
            if weekday != 6 and d not in CLOSED_DAYS:
                for c in cust:
                    if c["onboarded_on"] > d or (c["_churn"] and d > c["_churn"]):
                        continue
                    base = {"Distributor": 0.12, "Wholesaler": 0.07, "Retailer": 0.04}[c["customer_type"]]
                    if rng.random() >= base * self.b2b_season(m) * c["_size"]:
                        continue
                    order_seq += 1
                    oid = f"SO{order_seq:06d}"
                    nl = {"Distributor": (3, 6), "Wholesaler": (2, 4), "Retailer": (1, 3)}[c["customer_type"]]
                    n_lines = int(rng.integers(nl[0], nl[1] + 1))
                    w = pop * np.array([self.season(sku_season[s], m % 12 + 1) for s in skus])
                    w = w / w.sum()
                    chosen = rng.choice(len(skus), size=min(n_lines, len(skus)), replace=False, p=w)
                    disc_rng = {"Distributor": (0.08, 0.12), "Wholesaler": (0.03, 0.07), "Retailer": (0.0, 0.03)}[c["customer_type"]]
                    dozens = {"Distributor": (5, 20), "Wholesaler": (2, 8), "Retailer": (1, 3)}[c["customer_type"]]
                    for ln, idx in enumerate(chosen, 1):
                        s = skus[idx]
                        qty = int(rng.integers(dozens[0], dozens[1] + 1) * 12 * c["_size"] / 12) * 12 or 12
                        price = round(P.at[s, "wholesale_price"] * fy_multiplier(d), 2)
                        disc = round(float(rng.uniform(*disc_rng)), 2)
                        items.append(dict(order_id=oid, line_no=ln, sku=s, qty=qty,
                                          unit_price=price, discount_pct=disc))
                        demand_q[s] += qty
                        if not queue[s] and stock[s] >= qty:
                            stock[s] -= qty
                            line_fill[(oid, ln)] = d
                            inv[(mkey, s)]["b2b_shipped_qty"] += qty
                        else:
                            queue[s].append([oid, ln, qty])
                    orders.append(dict(order_id=oid, order_date=d, customer_id=c["customer_id"],
                                       _zone=c["zone"], _nlines=len(chosen)))

            # ---- 6. retail POS ----
            for store, (open_from, lam) in self.cfg["stores"].items():
                if d < date.fromisoformat(open_from):
                    continue
                factor = np.mean([self.season(t, m) for t in ("rain", "rain", "monsoon", "summer")])
                factor *= 1.35 if weekday >= 5 else 1.0
                rain_p = {6: .6, 7: .65, 8: .6, 9: .45, 5: .35, 10: .2}.get(m, .05)
                if rng.random() < rain_p:
                    factor *= 1.7
                if in_windows(d, PUJA_SHOPPING):
                    factor *= 1.5
                n_bills = int(rng.poisson(lam * factor))
                for _ in range(n_bills):
                    pos_counter[store] += 1
                    bill = f"{store_prefix[store]}-{pos_counter[store]:06d}"
                    hour = int(rng.choice(range(10, 21), p=np.array([3, 4, 5, 6, 6, 6, 7, 9, 11, 12, 10]) / 79))
                    ts = pd.Timestamp(d) + pd.Timedelta(hours=hour, minutes=int(rng.integers(0, 60)))
                    n_items = int(rng.choice([1, 2, 3], p=[.7, .22, .08]))
                    wr = pop * np.array([self.season(sku_season[s], m) for s in skus])
                    wr = wr / wr.sum()
                    years_in = (d - date(2023, 4, 1)).days / 1095
                    cash_p = 0.55 - 0.25 * years_in
                    mode = rng.choice(["Cash", "UPI", "Card"], p=[cash_p, 0.92 - cash_p, 0.08])
                    if store == "WhatsApp Orders":
                        mode = rng.choice(["UPI", "Cash on Delivery"], p=[.8, .2])
                    sale_disc = 0.10 if (in_windows(d, PUJA_SHOPPING) or m == 7 and d.day >= 20) else \
                        float(rng.choice([0, 0, 0, 0.05]))
                    for idx in rng.choice(len(skus), size=n_items, replace=False, p=wr):
                        s = skus[idx]
                        qty = 1 if rng.random() < 0.88 else 2
                        demand_q[s] += qty
                        if stock[s] < qty:          # walk-in customer leaves: lost sale
                            inv[(mkey, s)]["lost_retail_qty"] += qty
                            continue
                        stock[s] -= qty
                        inv[(mkey, s)]["retail_sold_qty"] += qty
                        mrp = round(P.at[s, "mrp"] * fy_multiplier(d))
                        pos_rows.append(dict(bill_no=bill, bill_datetime=ts, store=store, sku=s, qty=qty,
                                             unit_mrp=float(mrp), discount_pct=sale_disc,
                                             net_amount=round(qty * mrp * (1 - sale_disc), 2),
                                             payment_mode=mode,
                                             cashier_id=f"{store_prefix[store]}-C{int(rng.integers(1, 4))}"))

        # month-end inventory rows
        months = sorted(month_open)
        for i, mk in enumerate(months):
            close = month_open[months[i + 1]] if i + 1 < len(months) else stock
            for s in skus:
                f = inv[(mk, s)]
                inv_rows.append(dict(month=mk, sku=s, opening_qty=month_open[mk][s],
                                 produced_qty=f["produced_qty"], received_qty=f["received_qty"],
                                 b2b_shipped_qty=f["b2b_shipped_qty"], retail_sold_qty=f["retail_sold_qty"],
                                 closing_qty=close[s], lost_retail_qty=f["lost_retail_qty"]))

        self._orders, self._items, self._pos = orders, items, pos_rows
        self._prod, self._po, self._inv = prod_rows, po_rows, inv_rows
        self._line_fill = line_fill
        self._defect = (defect_a, defect_b)

    # ---------------- post-processing ----------------
    def finalise(self):
        rng = self.rng
        P = self.products.set_index("sku")
        C = self.customers.set_index("customer_id")
        items = pd.DataFrame(self._items)
        items["line_amount"] = (items.qty * items.unit_price * (1 - items.discount_pct)).round(2)
        orders = []
        for o in self._orders:
            fills = [self._line_fill.get((o["order_id"], ln)) for ln in range(1, o["_nlines"] + 1)]
            zone = o["_zone"]
            promise = ZONES[zone][1]
            row = dict(order_id=o["order_id"], order_date=o["order_date"], customer_id=o["customer_id"],
                       warehouse={"South Bengal": "Kolkata WH", "Other East": "Kolkata WH",
                                  "North Bengal": "Siliguri WH", "North-East": "Guwahati WH"}[zone],
                       promised_delivery_date=o["order_date"] + timedelta(days=promise))
            waited = ((max(f for f in fills if f) if all(fills) else self.end) - o["order_date"]).days
            if not all(fills):
                # never fully filled within the data window
                cancel = waited > 30 and rng.random() < 0.5
                row.update(dispatch_date=None, delivery_date=None,
                           order_status="Cancelled" if cancel else "Pending")
            elif waited > 30 and rng.random() < 0.25:
                row.update(dispatch_date=None, delivery_date=None, order_status="Cancelled")
            else:
                disp = max(max(fills), o["order_date"]) + timedelta(days=int(rng.integers(0, 2)))
                if disp.weekday() == 6:
                    disp += timedelta(days=1)
                lo, hi = ZONES[zone][2]
                transit = int(rng.integers(lo, hi + 1))
                if zone == "North-East" and disp.month in (6, 7, 8) and rng.random() < 0.35:
                    transit += int(rng.integers(1, 7))      # monsoon landslides / road closures
                deliv = disp + timedelta(days=transit)
                if deliv > self.end:
                    row.update(dispatch_date=disp if disp <= self.end else None, delivery_date=None,
                               order_status="In Transit" if disp <= self.end else "Pending")
                else:
                    row.update(dispatch_date=disp, delivery_date=deliv, order_status="Delivered")
            orders.append(row)
        orders = pd.DataFrame(orders)
        inv_amt = items.groupby("order_id").line_amount.sum().round(2)
        orders["invoice_amount"] = orders.order_id.map(inv_amt)
        orders.loc[orders.order_status.isin(["Cancelled", "Pending"]), "invoice_amount"] = 0.0
        orders["invoice_date"] = orders.dispatch_date
        orders["due_date"] = [
            (r.invoice_date + timedelta(days=int(C.at[r.customer_id, "credit_days"]))) if pd.notna(r.invoice_date) and r.invoice_date else None
            for r in orders.itertuples()]

        # payments
        pays, seq = [], 0
        for r in orders.itertuples():
            if not r.invoice_amount or r.invoice_date is None or pd.isna(r.invoice_date):
                continue
            cd = int(C.at[r.customer_id, "credit_days"])
            beh = C.at[r.customer_id, "_behaviour"]
            if cd == 0:
                base_day = r.delivery_date if r.delivery_date is not None and not pd.isna(r.delivery_date) else r.invoice_date
                delay = int(rng.integers(0, 3))
                plan = [(base_day + timedelta(days=delay), r.invoice_amount)]
                modes = ["Cash", "UPI", "NEFT"]
                mp = [.4, .45, .15]
            else:
                if beh == "good":
                    late = int(np.clip(rng.normal(2, 4), -5, 10))
                elif beh == "average":
                    late = int(np.clip(rng.normal(15, 10), 0, 45))
                elif beh == "slow":
                    late = int(np.clip(rng.normal(55, 25), 20, 150))
                else:
                    late = 9999 if rng.random() < 0.7 else int(rng.integers(90, 200))
                first = r.due_date + timedelta(days=late) if late < 9999 else None
                if first is None:
                    plan = []
                elif beh in ("average", "slow", "defaulter") and rng.random() < 0.3:
                    part = round(r.invoice_amount * rng.uniform(0.3, 0.7), 2)
                    plan = [(first, part),
                            (first + timedelta(days=int(rng.integers(10, 60))), round(r.invoice_amount - part, 2))]
                else:
                    plan = [(first, r.invoice_amount)]
                modes = ["NEFT", "Cheque", "UPI", "Cash"]
                mp = [.5, .3, .15, .05]
            for pdate, amt in plan:
                if pdate > self.end:
                    continue
                seq += 1
                pays.append(dict(payment_id=f"PAY{seq:06d}", order_id=r.order_id, customer_id=r.customer_id,
                                 payment_date=pdate, amount=float(amt), payment_mode=rng.choice(modes, p=mp)))
        payments = pd.DataFrame(pays, columns=["payment_id", "order_id", "customer_id", "payment_date", "amount", "payment_mode"])

        # complaints
        comp, cseq = [], 0
        da, db = self._defect
        delivered = orders[orders.order_status == "Delivered"]
        it_by_order = items.groupby("order_id")
        for r in delivered.itertuples():
            late = (r.delivery_date - r.promised_delivery_date).days
            types = []
            if late > 3 and rng.random() < 0.35:
                types.append(("Late delivery", None))
            for li in it_by_order.get_group(r.order_id).itertuples():
                if P.at[li.sku, "supplier_id"] == DEFECT_SUPPLIER and da <= r.order_date <= db + timedelta(days=30):
                    if rng.random() < 0.25:
                        types.append((rng.choice(["Quality - broken spokes", "Quality - fabric leaking",
                                                  "Quality - handle/button fault"]), li.sku))
                elif rng.random() < 0.006:
                    types.append((rng.choice(["Quality - broken spokes", "Quality - fabric leaking",
                                              "Quality - handle/button fault"]), li.sku))
            if rng.random() < 0.005:
                types.append((rng.choice(["Wrong item sent", "Short quantity"]), None))
            for t, sku in types:
                cseq += 1
                cdate = r.delivery_date + timedelta(days=int(rng.integers(1, 11)))
                if cdate > self.end:
                    continue
                res = int(rng.integers(5, 31) if t.startswith("Quality") else rng.integers(1, 8))
                comp.append(dict(complaint_id=f"CMP{cseq:05d}", complaint_date=cdate, order_id=r.order_id,
                                 customer_id=r.customer_id, sku=sku, complaint_type=t,
                                 channel=rng.choice(["Phone", "WhatsApp", "Email"], p=[.45, .45, .10]),
                                 resolution_days=res if cdate + timedelta(days=res) <= self.end else None,
                                 status="Closed" if cdate + timedelta(days=res) <= self.end else "Open"))
        complaints = pd.DataFrame(comp)

        po = pd.DataFrame(self._po)
        if len(po):
            po.loc[po.status == "Open", "received_qty"] = 0
            po = po.drop(columns=["_arrival"])

        self.out = dict(
            products=self.products.drop(columns=["_pop", "_slow", "season_type"]),
            customers=self.customers.drop(columns=["_behaviour", "_churn", "_size"]),
            suppliers=pd.DataFrame(SUPPLIERS, columns=["supplier_id", "supplier_name", "country", "promised_lead_days"]),
            orders=orders[["order_id", "order_date", "customer_id", "warehouse", "order_status",
                           "promised_delivery_date", "dispatch_date", "delivery_date",
                           "invoice_date", "due_date", "invoice_amount"]],
            order_items=items[["order_id", "line_no", "sku", "qty", "unit_price", "discount_pct", "line_amount"]],
            payments=payments,
            pos_sales=pd.DataFrame(self._pos),
            purchase_orders=po,
            inventory_monthly=pd.DataFrame(self._inv),
            production_log=pd.DataFrame(self._prod),
            complaints=complaints,
        )

    # ---------------- flat / messy extracts for Excel practice ----------------
    def flat_sales(self):
        o, it, c, p = (self.out[k] for k in ("orders", "order_items", "customers", "products"))
        df = it.merge(o[["order_id", "order_date", "customer_id", "order_status"]], on="order_id") \
               .merge(c[["customer_id", "customer_name", "customer_type", "city", "state", "zone",
                         "sales_rep", "payment_terms"]], on="customer_id") \
               .merge(p[["sku", "product_name", "category"]], on="sku")
        df = df.sort_values(["order_date", "order_id", "line_no"])
        return df[["order_id", "order_date", "order_status", "customer_id", "customer_name", "customer_type",
                   "city", "state", "zone", "sales_rep", "payment_terms", "sku", "product_name", "category",
                   "qty", "unit_price", "discount_pct"]]

    def invoice_status(self):
        o, pay, c = self.out["orders"], self.out["payments"], self.out["customers"]
        inv = o[o.invoice_amount > 0].merge(
            c[["customer_id", "customer_name", "customer_type", "payment_terms", "credit_days"]], on="customer_id")
        got = pay.groupby("order_id").agg(amount_received=("amount", "sum"), last_payment_date=("payment_date", "max"))
        inv = inv.merge(got, on="order_id", how="left")
        inv["amount_received"] = inv.amount_received.fillna(0).round(2)
        return inv[["order_id", "customer_id", "customer_name", "customer_type", "payment_terms", "credit_days",
                    "invoice_date", "due_date", "invoice_amount", "amount_received", "last_payment_date"]]

    def messy(self, flat):
        rng = np.random.default_rng(self.cfg["seed"] + 7)
        df = flat.copy().astype(object)
        n = len(df)
        city_alias = {"Kolkata": ["Calcutta", "KOLKATA", "kolkata "], "Guwahati": ["Gauhati", "guwahati", " Guwahati"],
                      "Siliguri": ["Shiliguri", "SILIGURI"], "Bhubaneswar": ["Bhubaneshwar"], "Howrah": ["Haora"]}
        df = df.reset_index(drop=True)
        dates = []
        for d in df.order_date:
            f = rng.random()
            dates.append(d.strftime("%d/%m/%Y") if f < 0.4 else d.strftime("%d-%b-%Y") if f < 0.6 else d.isoformat())
        df["order_date"] = dates
        for i in range(n):
            if df.at[i, "city"] in city_alias and rng.random() < 0.25:
                df.at[i, "city"] = rng.choice(city_alias[df.at[i, "city"]])
            if rng.random() < 0.08:
                df.at[i, "customer_name"] = rng.choice([df.at[i, "customer_name"].upper(), df.at[i, "customer_name"] + "  ",
                                                         " " + df.at[i, "customer_name"].lower()])
            if rng.random() < 0.10:
                q = int(df.at[i, "qty"])
                df.at[i, "qty"] = f"{q // 12} dz" if q % 12 == 0 and rng.random() < 0.5 else f"{q} pcs"
            if rng.random() < 0.10:
                df.at[i, "unit_price"] = f"₹{float(df.at[i, 'unit_price']):,.2f}"
            if rng.random() < 0.02:
                df.at[i, rng.choice(["city", "category", "zone"])] = ""
            if rng.random() < 0.03:
                df.at[i, "discount_pct"] = f"{float(df.at[i, 'discount_pct']) * 100:.0f}%"
        dup = df.sample(frac=0.03, random_state=int(self.cfg["seed"]))
        df = pd.concat([df, dup]).sample(frac=1, random_state=int(self.cfg["seed"]) + 1).reset_index(drop=True)
        return df

    # ---------------- write ----------------
    def write(self, out_dir):
        folder = os.path.join(out_dir, self.size)
        os.makedirs(folder, exist_ok=True)
        written = []
        for name, df in self.out.items():
            path = os.path.join(folder, f"{name}.csv")
            df.to_csv(path, index=False)
            written.append(path)
        if self.size in ("small", "medium"):
            flat = self.flat_sales()
            flat.to_csv(os.path.join(folder, "sales_lines_flat.csv"), index=False)
            self.messy(flat.reset_index(drop=True)).to_csv(os.path.join(folder, "sales_lines_messy.csv"), index=False)
            self.invoice_status().to_csv(os.path.join(folder, "invoice_status.csv"), index=False)
        if self.size == "huge":
            zpath = os.path.join(out_dir, "raincraft_huge.zip")
            with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
                for p in written:
                    z.write(p, arcname=os.path.join("huge", os.path.basename(p)))
        return folder

    def run(self, out_dir):
        self.make_products()
        self.make_customers()
        self.simulate()
        self.finalise()
        return self.write(out_dir)


def main():
    ap = argparse.ArgumentParser(description="Generate RainCraft Umbrellas synthetic datasets")
    ap.add_argument("--size", choices=["small", "medium", "huge", "all"], default="all")
    ap.add_argument("--out", default="./datasets")
    a = ap.parse_args()
    for s in (["small", "medium", "huge"] if a.size == "all" else [a.size]):
        folder = RainCraftSim(s).run(a.out)
        print(f"[{s}] written to {folder}")


if __name__ == "__main__":
    main()
