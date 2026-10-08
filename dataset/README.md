# RainCraft Umbrellas Pvt. Ltd.: course datasets

> ⚠️ **RainCraft is a fictional company.** All data here is simulated by `generate_raincraft_data.py`. Names of customers, people and suppliers are invented. Use it freely for learning and public portfolio work.

## The company

RainCraft Umbrellas Pvt. Ltd. is a **Kolkata-based manufacturer and distributor of umbrellas and raincoats**.

- **What it sells:** 3-fold, 2-fold and long umbrellas, kids' umbrellas, golf umbrellas, raincoats and UV sun umbrellas
- **Where products come from:** some are made in its own small factory (*In-house*); the rest are **imported from suppliers in China**
- **Who it sells to:**
  - **B2B:** Distributors, Wholesalers and Retailers across 4 zones: *South Bengal, North Bengal, North-East, Other East* (Bihar, Jharkhand, Odisha)
  - **B2C:** walk-in customers at its own retail counters (and, in later years, WhatsApp orders)
- **Warehouses:** Kolkata, Siliguri, Guwahati
- **Credit:** most B2B customers buy on credit (15–60 days); small retailers usually pay cash

### What the owner keeps saying

These complaints run through the whole course. Each one is backed by a pattern hidden in the data.

1. *"Our sales are growing, but there is never enough cash in the bank."*
2. *"In the monsoon some products run out, while other boxes sit in the godown for months."*
3. *"Customers in the North-East keep complaining about late deliveries."*
4. *"Our imports from China never arrive on time."*
5. *"Some customers have started complaining about quality."*
6. *"Production is slow; workers don't turn up around festivals."*

> 🔒 **Don't read the generator script's logic before Week 9.** It is effectively the answer key. Finding the patterns is your job.

## Three sizes

| Size | Period | Scale | Use it for | As-of date* |
|---|---|---|---|---|
| **small** | 1 Apr – 30 Jun 2025 (3 months) | 15 customers, 12 products, ~340 order lines, ~1,500 retail lines | Learning formulas by hand (Weeks 1–2) | 30 Jun 2025 |
| **medium** | 1 Apr 2025 – 31 Mar 2026 (1 year) | 60 customers, 40 products, ~2,600 order lines, ~13,500 retail lines | Pivots, dashboards, Power Query, SQL practice (Weeks 2–8) | 31 Mar 2026 |
| **huge** | 1 Apr 2023 – 31 Mar 2026 (3 years) | 300 customers, 80 products, ~34,500 order lines, ~267,000 retail lines | SQL at scale, Power BI, capstones (Weeks 9–16) | 31 Mar 2026 |

\* *As-of date* = the day the data was "exported". Payments after this date haven't happened yet, so anything unpaid is **outstanding**.

The three sizes are **separate simulations** of the same company, so their numbers won't match each other. `huge` represents RainCraft after expansion (more customers, more stores, a bigger factory team).

**Huge is zipped** (`raincraft_huge.zip`, ~3.6 MB) because the unzipped retail file is ~25 MB, which is GitHub's browser-upload limit. Unzip it on your laptop; keep only the zip in the repo (the `.gitignore` already does this).

## Files in each folder

| File | One row = | Key columns |
|---|---|---|
| `products.csv` | one product (SKU) | sku, product_name, category, made_in, supplier_id, unit_cost, wholesale_price, mrp |
| `customers.csv` | one B2B customer | customer_id, customer_name, customer_type, city, state, zone, sales_rep, payment_terms, credit_days, credit_limit, onboarded_on |
| `suppliers.csv` | one import supplier | supplier_id, supplier_name, country, promised_lead_days |
| `orders.csv` | one B2B sales order | order_id, order_date, customer_id, warehouse, order_status, promised_delivery_date, dispatch_date, delivery_date, invoice_date, due_date, invoice_amount |
| `order_items.csv` | one product line in an order | order_id, line_no, sku, qty, unit_price, discount_pct, line_amount |
| `payments.csv` | one payment received | payment_id, order_id, customer_id, payment_date, amount, payment_mode |
| `pos_sales.csv` | one product line in a retail bill | bill_no, bill_datetime, store, sku, qty, unit_mrp, discount_pct, net_amount, payment_mode, cashier_id |
| `purchase_orders.csv` | one import order to a supplier | po_id, supplier_id, sku, po_date, ordered_qty, unit_cost, promised_arrival_date, actual_arrival_date, received_qty, status |
| `inventory_monthly.csv` | one product in one month | month, sku, opening_qty, produced_qty, received_qty, b2b_shipped_qty, retail_sold_qty, closing_qty, lost_retail_qty |
| `production_log.csv` | one factory working day | date, workers_scheduled, workers_present, planned_units, produced_units, rejected_units, remarks |
| `complaints.csv` | one customer complaint | complaint_id, complaint_date, order_id, customer_id, sku, complaint_type, channel, resolution_days, status |

**Extra files in `small/` and `medium/`** (ready-made extracts for Excel practice):

| File | What it is |
|---|---|
| `sales_lines_flat.csv` | Order lines already joined with customer and product details: one big table, no lookups needed. **Line value is deliberately not included; you calculate it.** |
| `sales_lines_messy.csv` | The same data the way it often arrives in real life: mixed date formats, "2 dz" and "24 pcs" in the qty column, ₹ symbols in prices, spelling variants of cities, extra spaces, duplicates, blanks. **For Week 2 cleaning practice.** |
| `invoice_status.csv` | One row per invoice with amount received so far (up to the as-of date). |

## Column notes and business rules

- **Money:** Indian Rupees (₹), **excluding GST** (kept simple on purpose).
- **qty:** in pieces. B2B orders are always in multiples of 12 (umbrellas are traded by the **dozen**).
- **discount_pct:** a fraction. `0.05` means 5%. Format the column as % in Excel.
- **Line value (B2B):** `qty × unit_price × (1 − discount_pct)`. It equals `line_amount` in `order_items.csv`.
- **order_status:**
  - `Delivered`: delivered to customer
  - `In Transit`: dispatched, not yet delivered on the as-of date
  - `Pending`: waiting for stock (backorder) on the as-of date
  - `Cancelled`: customer cancelled, usually after waiting too long for stock
- **Revenue:** an order becomes revenue when it is **invoiced**, which happens at dispatch. Pending and Cancelled orders have `invoice_amount = 0`.
- **due_date:** `invoice_date + credit_days`. Cash customers (`credit_days = 0`) pay on delivery.
- **Outstanding:** `invoice_amount − amount received`. **Overdue** = outstanding *and* past its due date.
- **lost_retail_qty:** walk-in customers who wanted a product that was out of stock (lost sales).
- **Prices change each financial year (April–March)**, so the same product costs less in FY2023-24 than in FY2025-26.

## Regenerating the data (optional)

You never need to do this; the files are already here. It needs Python 3 with `pandas` and `numpy`.

```bash
python generate_raincraft_data.py --size all --out .
```

Same seed → exactly the same data every time.
