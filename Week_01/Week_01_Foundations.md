# Week 1 · Foundations: How Business Works, Excel Formulas & Your First AI Prompts

> **Suggested dates:** Thu 8 Oct – Wed 14 Oct 2026 · Thu 15 Oct = catch-up buffer · then Durga Puja break 🪔
> **Time:** about 2.5 hours a day
> **Data:** `datasets/small/` (RainCraft, Apr–Jun 2025)

---

## By the end of this week you can…

- Explain what Business, Data and Operations Analysts do, and how a customer order turns into cash
- Open a data file in Excel properly, turn it into a Table, sort, filter and use `$` references
- Answer business questions with `SUMIFS`, `COUNTIFS`, `AVERAGEIFS`, `MAXIFS` and `UNIQUE`
- Write a structured AI prompt, and catch AI when its numbers are wrong
- Read and build a simple Profit & Loss statement
- Write a short, clear professional email

## Week tracker

Tick as you go (edit this file on GitHub and change `[ ]` to `[x]`).

| Day | Topic | Learn | Assignment | Case of the Day | English |
|---|---|---|---|---|---|
| Day 0 | Setup (30 min) | [X] | — | — | — |
| Day 1 | How companies work & analyst roles | [ ] | [ ] | [ ] | [ ] |
| Day 2 | Excel foundations | [ ] | [ ] | [ ] | [ ] |
| Day 3 | SUMIFS & friends | [ ] | [ ] | [ ] | [ ] |
| Day 4 | AI as your assistant | [ ] | [ ] | [ ] | [ ] |
| Day 5 | Revenue, costs & profit | [ ] | [ ] | [ ] | [ ] |
| Day 6 | **Weekly case: "Where is our money?"** | — | [ ] | — | [ ] |
| Day 7 | Review, LinkedIn, check-in | [ ] quiz | [ ] GitHub | [ ] post | [ ] check-in |

---

## Day 0 · Setup (30 minutes, do this before Day 1)

- [ ] **GitHub:** create a public repository named `business-analyst-journey`. Upload this course's files: `README.md`, `00_Course_Roadmap.md`, `datasets/`, `Week_01/`.
- [ ] **Laptop:** make a folder `Documents/BA-Course/` and copy `datasets/small/` into it. Work on your laptop; upload finished work to GitHub at the end of each day.
- [ ] **Excel check:** open Excel → *File → Account*. It should say *Microsoft 365*. That means you have `XLOOKUP`, `UNIQUE`, `FILTER` and `SORT`.
- [ ] **Phone:** open the Gemini or Claude app and find **voice mode**. You'll use it for 10 minutes of English practice daily.
- [ ] **Anti-overwhelm step:** mute or unfollow 3–5 accounts that post "learn these 20 AI tools now" content. The course roadmap is your only tool list.
- [ ] **Learning log:** create `Week_01/my_work/learning_log.md`. Each day, write 3 lines: *What I learned · What confused me · One question.*

---

## Meet RainCraft: the company you work for

> **The story:** You have just joined **RainCraft Umbrellas Pvt. Ltd.** as a **Junior Business Analyst**.
> RainCraft is a Kolkata-based company that makes and imports umbrellas and raincoats, and sells them to distributors, wholesalers and retailers across East and North-East India. It also has its own retail counter in Kolkata.
> Your manager is **Mr. Prabir Sen, Managing Director**. On your first morning he tells you:
>
> *"Last quarter was our best ever for sales. But every week I'm short of cash to pay suppliers and salaries. I want to understand what is going on."*

RainCraft is fictional; its data is simulated. The business problems are real ones that small manufacturers face. Read the [dataset guide](../datasets/README.md) once (10 minutes) before Day 1.

**Files you'll use this week (all in `datasets/small/`):**

| File | Used on |
|---|---|
| `sales_lines_flat.csv`: every B2B order line, with customer and product details | Days 2, 3, 4 |
| `products.csv`: cost, wholesale price and MRP of each product | Day 5 |
| `orders.csv`: one row per order, with status and invoice amount | Day 5 (stretch) |
| `invoice_status.csv`: every invoice with amount received so far | Day 6 |
| `customers.csv`: credit days and credit limits | Day 6 |

---

# Day 1 · How companies work & what analysts actually do

### 1.1 A company is a set of flows

Every business, from a tea stall to Amazon, runs on four flows:

| Flow | At RainCraft | Where it is recorded |
|---|---|---|
| **Goods** | Fabric and frames → factory → umbrellas → warehouse → customer | Production log, stock register, delivery challans |
| **Money** | Customer pays → RainCraft pays suppliers, workers, rent | Invoices, payment receipts, bank statement |
| **Orders** | A shop in Silchar orders 10 dozen umbrellas | Sales orders, purchase orders |
| **Information** | Who ordered what, when, at what price, delivered late or on time | Billing software (Busy/Tally), Excel, WhatsApp |

**An analyst's job is to read the information flow so the company can manage the other three better.**

### 1.2 The two loops every product business runs

**Order-to-Cash (O2C):** from the customer's order to money in the bank.

```
Customer order → Credit check → Stock check → Pick & pack → Dispatch + Tax invoice
→ Delivery → Payment due date → Payment received → Matched in accounts
```

**Procure-to-Pay (P2P):** from needing materials to paying the supplier.

```
Need identified → Purchase order (PO) → Supplier ships → Goods received & checked
→ Supplier invoice → Payment to supplier
```

Problems in these loops are what analysts are hired to find. Examples: *a customer pays 60 days late* (O2C), or *an import arrives 3 weeks late and stock runs out* (P2P).

### 1.3 Who asks the analyst for what

| Department | Typical questions they bring to an analyst |
|---|---|
| **Sales** | Which customers are buying less than last year? Which zone is growing? Who are our top 20 customers? |
| **Operations / Supply chain** | Which products will run out next month? How many orders were delivered late, and why? |
| **Finance** | How much money is stuck with customers? Who is overdue? What is our margin by product? |
| **Purchase** | Which supplier is always late? How much should we order, and when? |
| **Management** | Are we growing profitably? Where should we invest next year? |

### 1.4 Four analyst roles, compared

| | **Business / Data Analyst** | **Operations Analyst** | **IT Business Analyst** | **Consulting Analyst** |
|---|---|---|---|---|
| Core question | *What is happening and why?* | *How do we run this better and cheaper?* | *What exactly should the software do?* | *What should the client decide?* |
| Day to day | Pull data, clean it, build reports & dashboards, explain trends | Track processes (orders, delivery, stock, support), find delays and cost leaks, build MIS reports | Interview users, write requirements and user stories, work with developers | Structure problems, analyse, build slide decks with recommendations |
| Main tools | Excel, SQL, Power BI | Excel, SQL, Power BI, process maps | Jira, Confluence, Word, diagrams | Excel, PowerPoint |
| Common first-job titles in India | Data Analyst, Business Analyst, MIS Executive, Reporting Analyst | Operations Analyst, Supply Chain Analyst, Business Operations Analyst | Associate BA, Junior BA | Analyst, Business Analyst (consulting) |

This course prepares you mainly for the **first two columns**, with consulting-style problem solving and one week of IT-BA basics.

### 1.5 The analyst loop

Every analyst task, in every company, follows the same loop:

```
1. Question  →  2. Data  →  3. Clean  →  4. Analyse  →  5. Insight  →  6. Recommendation  →  7. Communicate
```

Beginners jump straight to step 4. Good analysts spend real time on **step 1** (what exactly are we trying to answer?) and **step 7** (will the manager understand and act on it?).

### 1.6 What you do NOT need

You do not need Python, machine learning, 20 AI tools, or a certification to get a first analyst job. Job posts for 0–2 year analyst roles in India mostly ask for **Excel + SQL + one dashboard tool + communication + business sense**. Today's assignment will show you this with real job posts.

### 📺 Watch (about 40 minutes total)

| Video | Language | Why |
|---|---|---|
| [Data Analyst Job Description Explained](https://www.youtube.com/watch?v=hgeP8ahNz2o) | Hindi | What the role involves, in simple words |
| [Day in the Life: Operations Analyst](https://www.youtube.com/watch?v=8EvCK6eYSmU) | English | A real ops analyst's day (Chennai) |
| [O2C Cycle (Order to Cash): Practical Understanding](https://www.youtube.com/watch?v=bT9ig6NKoEA) | Hindi/English | The order-to-cash loop with examples |

### ✍️ Assignment (about 60 min) → save as `my_work/W1D1_company_map.md`

1. **RainCraft's O2C, step by step.** Make a table with 8 rows (one per O2C step) and 4 columns: *Step · Which team does it · Document created · What can go wrong*. Use your own experience of how billing and dispatch work in a real business.
2. **Analyst questions.** Write 3 questions *each* that Sales, Operations and Finance at RainCraft would ask an analyst (9 questions in total).
3. **Real job market check.** On Naukri or LinkedIn, find **5 real job posts** in Bangalore (0–2 years) titled *Business Analyst*, *Operations Analyst*, *MIS Executive* or *Data Analyst*. Make this table:

   | Company | Title | Top 5 skills asked | Tools mentioned |
   |---|---|---|---|

   Then count: how many of the 5 posts mention Excel? SQL? Power BI/Tableau? Python? Write 2 lines on what you notice.

### 🔍 Case of the Day: Blinkit / Zepto and 10-minute delivery

Quick-commerce apps promise delivery in about 10 minutes from small local warehouses called *dark stores*.

**Question:** Which teams have to work together so that one order arrives in 10 minutes? List at least 5 teams. For each team, name **one number (metric)** they would check every day. Answer in 5–8 lines.

<details>
<summary>Model answer (open only after you write yours)</summary>

- **Category / Purchase:** fill rate, i.e. % of items in stock when customers search for them
- **Dark-store operations:** picking time per order (seconds from order to packed)
- **Delivery / Last mile:** average delivery time; % of orders delivered within 10 minutes
- **Demand planning:** forecast accuracy (predicted vs actual sales per item per store)
- **Customer support:** complaints per 1,000 orders; refund rate
- **Finance:** cost per delivery; contribution margin per order
- **Product / Tech:** app conversion rate (visits → orders)

The insight: a 10-minute promise is an **operations** promise more than a tech one. Analysts sit in every one of these teams.
</details>

### 🗣️ English (10 min)

Record a **60-second voice note** introducing yourself using this structure, then play it back once:

> *"Hello, my name is ___. I completed my MBA in Marketing and HR in 2022. In my previous role at a manufacturing and retail business, I handled ___, ___ and ___. I noticed problems like ___. Now I am building skills to become a business and operations analyst, starting with Excel and business fundamentals."*

**Rule:** describe only what you actually did. Things you *noticed* count. Say "I noticed…" or "I observed…" rather than claiming you fixed it.

Then type your introduction into Gemini or Claude with this prompt:

```
Correct the grammar of my self-introduction below. Keep my meaning and keep it simple.
Then list my 3 most important mistakes and explain each in one line, in simple English.
My introduction: [paste]
```

### ✅ Self-check

<details>
<summary>1. What is the difference between O2C and P2P?</summary>
O2C is the selling loop: customer order to cash received. P2P is the buying loop: purchase order to supplier paid.
</details>
<details>
<summary>2. A company has high sales but is always short of cash. Which loop would you look at first, and why?</summary>
O2C, especially the last steps (payment due → payment received). If customers pay late, sales exist on paper but the cash hasn't arrived. You will check this on Day 6.
</details>

---

# Day 2 · Excel foundations, done properly

### 2.1 Open CSV files the right way

1. Double-click `sales_lines_flat.csv`. It opens in Excel.
2. **Immediately** do *File → Save As → Excel Workbook (.xlsx)* and name it `W1_RainCraft_Q1.xlsx`. CSV files cannot save formulas, formatting or multiple sheets.
3. Check that the `order_date` column is right-aligned. Right-aligned means Excel understood it as a date. Left-aligned means it is text, which you'll learn to fix in Week 2.

### 2.2 What clean ("tidy") data looks like

- **One header row**, with one name per column
- **One row = one record** (here: one product line in one order)
- **No blank rows or columns**, no merged cells, no totals mixed into the data
- **One type per column** (numbers are numbers, dates are dates)

`sales_lines_flat.csv` is tidy. Next week you'll meet `sales_lines_messy.csv`, which is not.

### 2.3 Excel Tables (Ctrl + T): use them always

Click any cell in the data → **Ctrl + T** → tick *My table has headers* → OK. Then in *Table Design*, rename the table from `Table1` to **`Sales`**.

Why Tables:
- New rows are included automatically in formulas, pivots and charts
- Formulas copy down the whole column by themselves
- You write readable formulas: `=SUM(Sales[qty])` instead of `=SUM(O2:O338)`
- A *Total Row* (Table Design → tick Total Row) gives quick sums, averages and counts

Inside a Table, a formula that refers to "this row" uses `[@column]`, for example `=[@qty]*[@unit_price]`.

### 2.4 Sort, filter, freeze

- **Filter:** the arrow on each header. You can filter on several columns at once.
- **Sort:** largest to smallest, A to Z, or by several levels (*Data → Sort*).
- **Freeze panes:** *View → Freeze Panes → Freeze Top Row* keeps the header visible while you scroll.
- Always **clear filters** (*Data → Clear*) before you calculate totals, or you will get confused.

### 2.5 Relative vs absolute references (`$`)

When you copy a formula, Excel shifts the cell references. That is a **relative** reference (`B2`).
To stop a reference from moving, add `$`, which makes it **absolute** (`$B$2`). Press **F4** to toggle.

Example: a growth target of 10% sits in cell `B1`. Next to each zone's sales, `=C5*(1+$B$1)` copied down always uses `B1`. Without `$`, the second row would use `B2`, the third `B3`… and give wrong answers.

Mixed references (`$B2` or `B$2`) lock only the column or only the row. You'll use them in Week 2.

### 2.6 Number formats that look professional

- **Percent:** select the `discount_pct` column → *Home → %*. Now `0.05` shows as `5%`.
- **Indian rupee with lakh commas (₹12,34,567.00):** if your Windows region is *English (India)*, the ₹ currency format already uses lakh grouping. If not, use *Format Cells → Custom* and paste:
  ```
  [>=10000000]"₹"##\,##\,##\,##0.00;[>=100000]"₹"##\,##\,##0.00;"₹"##,##0.00
  ```
- **Thousands of rows look better** with: bold header, freeze top row, numbers right-aligned, no colourful fills.

### 2.7 Ten shortcuts worth learning this week

| Shortcut | Does |
|---|---|
| Ctrl + T | Make a Table |
| Ctrl + Shift + L | Turn filters on/off |
| Ctrl + Arrow key | Jump to the end of the data |
| Ctrl + Shift + Arrow | Select to the end of the data |
| Ctrl + Space / Shift + Space | Select column / row |
| F4 | Toggle `$` in a formula |
| F2 | Edit the current cell |
| Alt + = | AutoSum |
| Ctrl + ; | Today's date |
| Ctrl + 1 | Format Cells |

### 📺 Watch (about 45 minutes)

| Video | Language |
|---|---|
| [MS Excel Sort & Filter: Full Tutorial](https://www.youtube.com/watch?v=W0brExaq2sU) | Hindi |
| [How to Use Tables in Excel: Create, Format, Filter & Sort](https://www.youtube.com/watch?v=Q4dgE7SrNUo) | Hindi |
| [When to Use $ in Excel: Absolute vs Relative References](https://www.youtube.com/watch?v=mt3cjp3BClo) | English |
| Read: [Microsoft: Switch between relative and absolute references](https://support.microsoft.com/en-us/excel/switch-between-relative-and-absolute-references) | English (5 min) |

### ✍️ Assignment (about 60 min) → `my_work/W1_RainCraft_Q1.xlsx`, sheet **Sales**

1. Open `sales_lines_flat.csv`, save as `.xlsx`, make it a Table named **Sales**, freeze the top row.
2. Add a new column **`Line Value`** = `=[@qty]*[@unit_price]*(1-[@discount_pct])`. Format it as ₹.
3. Format `discount_pct` as %.
4. Turn on the **Total Row** and show the **sum** of Line Value.
5. **Sort** by Line Value, largest first. Which order line is the biggest? Write the order ID, customer, product and qty.
6. **Filter:** `zone` = North-East **and** `customer_type` = Retailer. How many lines are there? Clear filters after.
7. **`$` practice:** on a new sheet **Targets**, put `Target growth` in `A1` and `10%` in `B1`. In `A4:A7` type the 4 zones. In `B4:B7` type each zone's sales (for today, copy them from the Day 3 answer key; tomorrow you'll calculate them yourself). In `C4` write a formula for next year's target using `$B$1`, and copy it down.
8. Add a column **`Dozens`** = `=[@qty]/12`. (B2B umbrellas are traded by the dozen; every qty should give a whole number.)

<details>
<summary>Answer key (check after you finish)</summary>

- Rows: **337** order lines, **111** orders
- Sum of Line Value (all rows, Total Row): **₹56,39,571.60**
- Biggest line: **SO000049, Rupali Trading Co., Compact 3-Fold – Floral Print, 216 pcs = ₹69,552.00**
- North-East + Retailer: **53 lines**
- Targets (+10%): North-East ₹27,14,472.42 · South Bengal ₹22,49,041.08 · North Bengal ₹9,22,430.52 · Other East ₹1,99,208.46
- If your Line Value total is different: check that `discount_pct` is a fraction (0.05), not 5, and that you used `(1-…)` with brackets.
</details>

### 🔍 Case of the Day: DMart's low prices

DMart (Avenue Supermarts) is widely known for **owning most of its store buildings** instead of renting, keeping a **focused range of products**, and **paying suppliers faster than most retailers**, which helps it negotiate lower buying prices. It then passes part of the saving on as low prices.

**Questions (5–8 lines):**
1. Why does paying suppliers quickly help DMart buy cheaper?
2. Name 4 numbers a DMart analyst would look at **every day**.

<details>
<summary>Model answer</summary>

1. Suppliers value fast, reliable payment because it reduces their own cash problems. In return they give a lower price. DMart can afford to pay fast because its products sell quickly (high stock turnover).
2. Daily numbers: sales per store and per square foot; footfall and bills per store; average bill value; stock-outs on top-selling items; inventory days (how many days of sales are sitting in stock); gross margin by category.

Link to RainCraft: RainCraft sells on **credit** and imports with long lead times. That is the opposite of DMart's model. Keep this in mind on Day 6.
</details>

### 🗣️ English (10 min): anatomy of a work email

| Part | Rule | Example |
|---|---|---|
| **Subject** | Specific + action + date if any | `PO-1045 delayed: please confirm dispatch date by Fri` |
| **Greeting** | Dear Mr./Ms. Surname (formal) · Hi Firstname (colleague) | `Dear Mr. Banerjee,` |
| **Purpose** | First line says why you're writing | `I am writing about our order PO-1045, which is now 5 days late.` |
| **Details** | Facts only: numbers, dates, references | `It was due on 10 June for 600 pcs.` |
| **Ask** | One clear request with a deadline | `Could you please confirm a dispatch date by 5 pm tomorrow?` |
| **Close** | Polite + your name, role, company | `Thank you for your support. Regards, …` |

**Exercise:** rewrite these 3 weak subject lines: `Regarding order`, `Urgent!!!`, `Need info`. Invent the details.

---

# Day 3 · Answering business questions with formulas (SUMIFS & friends)

### 3.1 Why these formulas matter

Managers ask questions like *"How much did we sell in the North-East?"* or *"How many orders came from distributors?"* Each of these is **a total (or count, or average) with conditions**. That is exactly what the `…IFS` family does.

### 3.2 SUMIF vs SUMIFS

```
=SUMIF(  criteria_range, criteria, sum_range )                            ← one condition only
=SUMIFS( sum_range, criteria_range1, criteria1, criteria_range2, criteria2, … )   ← one or many conditions
```

⚠️ The order is different. In `SUMIFS` the **sum range comes first**. To avoid confusion, **always use SUMIFS**, even for one condition.

Example (total sales in the North-East):
```
=SUMIFS(Sales[Line Value], Sales[zone], "North-East")
```
Better: put the zone name in a cell (say `A4`) and refer to it, so the formula can be copied down:
```
=SUMIFS(Sales[Line Value], Sales[zone], A4)
```

### 3.3 The most common mistakes (and fixes)

| Mistake | What happens | Fix |
|---|---|---|
| Sum range and criteria range of different sizes | `#VALUE!` | Use Table columns (`Sales[...]`), so they always match |
| Typing text without quotes: `North-East` | Error or 0 | `"North-East"`, or better, a cell reference |
| Extra space in the data (`"North-East "`) | Answer is 0 | Week 2: `TRIM` |
| Wanting "everything except X" | — | `"<>Cancelled"` |
| Wanting "more than 100" | — | `">100"` or `">="&B1` |
| Forgetting to exclude cancelled orders | Sales overstated | Add `Sales[order_status], "<>Cancelled"` |

### 3.4 The family

| Formula | Answers | Example |
|---|---|---|
| `SUMIFS` | How much? | Sales value in North-East, excluding cancelled |
| `COUNTIFS` | How many rows? | Lines with qty ≥ 100 |
| `AVERAGEIFS` | Average? | Average qty per line for Retailers |
| `MAXIFS` / `MINIFS` | Biggest / smallest? | Largest single line for Distributors |

```
=COUNTIFS(Sales[qty], ">=100")
=AVERAGEIFS(Sales[qty], Sales[customer_type], "Retailer")
=MAXIFS(Sales[Line Value], Sales[customer_type], "Distributor")
```

### 3.5 UNIQUE and SORT: let Excel build the list for you (Microsoft 365)

Instead of typing zone names by hand:
```
=UNIQUE(Sales[zone])
```
The result **spills** down into as many cells as needed. If it's in cell `A4`, you can refer to the whole spilled list as `A4#`. That means one formula can fill the whole summary column:
```
=SUMIFS(Sales[Line Value], Sales[zone], A4#, Sales[order_status], "<>Cancelled")
```
And to sort a list: `=SORT(UNIQUE(Sales[zone]))`.

> If you see `#SPILL!`, something is blocking the cells below. Clear them.

### 3.6 How to lay out a summary table

On a new sheet **Summary**: question as a heading → labels in column A → formulas in B and C → a **% share** column → a one-line *insight* written under the table. The insight line is what a manager actually reads.

### 📺 Watch (about 45 minutes)

| Video | Language |
|---|---|
| [SUMIFS Formula in Excel in Hindi: SUMIF and SUMIFS](https://www.youtube.com/watch?v=rDaTTrW6N_0) | Hindi |
| [Excel COUNTIFS, SUMIFS & AVERAGEIFS (tutorial + examples)](https://www.youtube.com/watch?v=1WzT6B-1a0M) | English |
| [Two Excel Dynamic Array Functions: UNIQUE and SORT](https://www.youtube.com/watch?v=s7zRj9qi9Bc) | English |

### ✍️ Assignment (about 60–75 min) → same workbook, new sheet **Summary**

**Rule for all questions: exclude Cancelled orders** unless the question says otherwise.

1. **Sales by zone:** use `UNIQUE` for the zone list, `SUMIFS` for value, and add a **% share** column. Which zone is #1?
2. **Sales by customer type** (Distributor / Wholesaler / Retailer) with % share.
3. **Credit vs Cash:** sales by `payment_terms`, with % share. Write one line: what does this mean for cash in the bank?
4. **Units by product:** `UNIQUE` product names, `SUMIFS` on `qty`. Which product sold the most units? (Tip: wrap the two columns in `SORT`, or sort manually.)
5. **Top customer** by sales value.
6. **Average qty per line** for each customer type (`AVERAGEIFS`). Why is it so different?
7. **Monthly trend:** add a column `Month` to the Sales table: `=TEXT([@order_date],"yyyy-mm")`. Then sales by month with `UNIQUE` + `SUMIFS`.
8. **Two-condition question:** total **qty** of *Kids Umbrella* sold to *Retailers* in the *North-East*.
9. **Counting:** how many order lines have qty ≥ 100 (all statuses)?
10. **Average order value** = total sales ÷ number of orders (excluding cancelled).
    *Stretch:* count orders (not lines) with `=COUNTA(UNIQUE(FILTER(Sales[order_id], Sales[order_status]<>"Cancelled")))`
11. **Confidence check (10 min):** open a blank sheet and redo the 8-row Notebook/Pen/Bag exercise from the intake skill check: Total column, total per region with SUMIFS, product with most units, and a quick column chart (*Insert → Column Chart*). Notice how much faster it is now.

Under each table, write **one insight sentence**, for example: *"North-East is our largest zone (45% of sales), driven by one distributor."*

<details>
<summary>Answer key</summary>

Total sales excluding cancelled: **₹55,31,956.80** (one order, SO000044 from Kamakhya Enterprises, was cancelled).

| Zone | Sales | Share |
|---|---|---|
| North-East | ₹24,67,702.20 | 44.6% |
| South Bengal | ₹20,44,582.80 | 37.0% |
| North Bengal | ₹8,38,573.20 | 15.2% |
| Other East | ₹1,81,098.60 | 3.3% |

| Customer type | Sales | Share | Avg qty per line |
|---|---|---|---|
| Distributor | ₹35,89,593.00 | 64.9% | 108.9 |
| Wholesaler | ₹11,92,711.20 | 21.6% | 46.3 |
| Retailer | ₹7,49,652.60 | 13.6% | 23.1 |

- Credit ₹47,82,304.20 (**86.4%**) · Cash ₹7,49,652.60 (13.6%). → 86% of sales do not turn into cash immediately.
- Top product by units: **Compact 3-Fold – Beige, 4,272 pcs**, then Classic 2-Fold – Maroon (3,528), Breeze 3-Fold – Bottle Green (2,832)
- Top customer: **Kamakhya Enterprises, ₹21,45,100.80** (a North-East distributor, about 39% of all sales by itself → a concentration risk)
- Months: Apr ₹12,08,330.40 · May ₹21,77,221.20 · Jun ₹21,46,405.20 (sales jump as shops stock up before the monsoon)
- Kids Umbrella → Retailers → North-East: **192 pcs**
- Lines with qty ≥ 100: **64**
- Orders excluding cancelled: **110** → Average order value **₹50,290.52**
</details>

### 🔍 Case of the Day: Myntra's big sale

Myntra runs a large sale event called *End of Reason Sale (EORS)* a few times a year.

**Question:** Three weeks before the sale, the category team asks you for data. Write **5 questions** you would answer, each one as a `SUMIFS`/`COUNTIFS`-style question (for example: *"Total units of men's sneakers sold in the last sale, by city"*).

<details>
<summary>Model answer</summary>

1. Units and value sold per category in the last sale vs a normal week → how much stock to prepare
2. Sales per category **by city/region** → where to place stock in warehouses
3. Number of orders per day of the last sale → staffing for warehouses and delivery
4. Return rate per category in the last sale → which categories need better size guides
5. Average discount per brand vs units sold → which discounts actually moved volume
</details>

### 🗣️ English (15 min): rewrite a real email

Rewrite the vendor-delay email you wrote in the intake skill check, using yesterday's email structure. Then compare with the model:

<details>
<summary>Model email</summary>

**Subject:** PO-1045 delayed by 5 days: please confirm dispatch date by tomorrow

Dear Mr. Banerjee,

I hope you are well. I am writing about our order PO-1045 (dated 2 June, 600 pcs of 3-fold umbrellas), which was due on 10 June and has not reached us yet.

We are now out of stock on these items and our customers are waiting for their orders.

Could you please confirm a firm dispatch date by 5 pm tomorrow? If the full quantity is not ready, a part shipment of the available stock this week would help us a lot.

Thank you for your support. We value our partnership and would like to plan this together.

Regards,
[Your name]
Purchase & Operations, RainCraft Umbrellas Pvt. Ltd.
+91-XXXXX XXXXX

*What changed:* a specific subject, the PO number and dates, the impact stated without blaming, one clear ask with a deadline, a backup option (part shipment), and a relationship-friendly close.
</details>

---

# Day 4 · AI as your analyst assistant (and how to stop getting bad answers)

### 4.1 What AI chat tools are good and bad at

| Good at | Bad at |
|---|---|
| Explaining concepts simply, in Hindi or English | **Arithmetic on data you paste**: it can add wrong and sound confident |
| Writing and fixing Excel formulas, SQL, DAX | Knowing *your* company's facts (it guesses) |
| Drafting emails, reports, summaries | Recent events (unless it searches the web) |
| Turning messy notes into structure | Saying "I don't know" (it tends to invent an answer instead; this is called *hallucination*) |
| Quizzing you, role-playing an interviewer | Reading huge files reliably |

Bad AI results usually come from **vague prompts** and from **asking AI to do the calculation**. Both are fixable.

### 4.2 The prompt structure: R-C-T-F-R

| Part | Means | Example |
|---|---|---|
| **R**ole | Who should the AI act as? | *"You are a senior business analyst mentoring a junior analyst."* |
| **C**ontext | Your situation, data, audience | *"I work at an umbrella distributor. My manager is the MD. Data covers Apr–Jun 2025."* |
| **T**ask | Exactly what to produce | *"Draft a monthly sales summary."* |
| **F**ormat | Length, structure, style | *"Max 150 words, 3 bullet findings + 1 recommendation, Indian number format."* |
| **R**ules | Limits and checks | *"Use ONLY the numbers I give you. Don't calculate new ones. Ask me if something is missing."* |

**Weak prompt** (a typical first attempt):
```
make a short monthly sales report from this messy excel sheet
```

**Strong prompt:**
```
Role: You are a senior business analyst helping a junior analyst.
Context: I work at RainCraft, an umbrella manufacturer-distributor. I calculated these
numbers in Excel for Apr–Jun 2025 (cancelled orders excluded):
- Total sales: ₹55.32 lakh. Monthly: Apr ₹12.08 L, May ₹21.77 L, Jun ₹21.46 L
- By zone: North-East 44.6%, South Bengal 37.0%, North Bengal 15.2%, Other East 3.3%
- Top customer: Kamakhya Enterprises, ₹21.45 L (39% of sales)
- 86% of sales are on credit
Task: Write a short sales summary for my Managing Director.
Format: Max 150 words. 3 bullet findings, 1 risk, 1 recommendation. Simple English.
Rules: Use ONLY these numbers. Do not calculate anything new. If you need more
information, ask me first.
```

**Key idea:** give AI your **calculated summary**, not raw data. Excel does the maths; AI does the words.

### 4.3 The golden rules

1. **Excel computes, AI writes.** Ask AI for *formulas*, not *answers*. Test every formula in Excel.
2. **Verify every number** AI gives you against your Excel result before using it anywhere.
3. **Iterate.** The first answer is a draft. Follow up: *"Shorter"*, *"Make it more formal"*, *"You used a number I didn't give you; remove it."*
4. **Privacy.** Never paste a real employer's customer names, prices or personal data into public AI tools. RainCraft is fictional, so it's safe to practise with.
5. **Use AI as a tutor:** *"Explain SUMIFS like I'm a shopkeeper, then give me 3 practice questions and check my answers."*

### 📺 Watch (about 35 minutes)

| Video | Language |
|---|---|
| [Prompt Engineering for Beginners: How to Write Better AI Prompts](https://www.youtube.com/watch?v=T_-2M_1pgoE) | English |
| [Prompt Engineering Full Course (playlist)](https://www.youtube.com/playlist?list=PLyz4Eb45WBQ02Md7BiIO1sUsKTs8GcWKS): watch only the first 2–3 videos | Hindi |

### ✍️ Assignment (about 60 min) → `my_work/W1D4_prompts.md`

1. **Prompt makeover.** Paste the weak prompt and the strong prompt above into Gemini or Claude, one at a time (with your Day 3 numbers). Save both outputs. Write 3 lines on the difference.
2. **The verification experiment.** Copy the **first 30 rows** of the Sales table (with headers) and paste them into the AI. Ask: *"What is the total Line Value by zone?"* Then calculate the same 30 rows in Excel. Make this table:

   | Zone | AI answer | Excel answer | Match? |
   |---|---|---|---|

   Whatever the result, write one line on what this means for your work.
3. **AI as formula helper.** Ask AI: *"I have an Excel Table named Sales with columns category, customer_type, zone, qty. Write a formula for the total qty of Kids Umbrella sold to Retailers in North-East."* Test it in Excel. Does it give 192? If you get an error, paste the error back to the AI and fix it together.
4. **Start your Prompt Library:** create `my_work/prompt_library.md` with 5 reusable prompts in R-C-T-F-R format:
   - Explain a concept simply
   - Write an Excel formula for my Table
   - Check and improve my email
   - Quiz me on today's topic
   - Turn my numbers into a 5-line summary

   You'll keep adding to this file for 16 weeks.

### 🔍 Case of the Day: Flipkart's Big Billion Days

During Flipkart's *Big Billion Days* sale, customer questions jump sharply ("Where is my order?", "Refund status?", "Is this product genuine?").

**Questions:**
1. Which 3 types of questions can an AI chatbot handle well, and which 2 must go to a human?
2. Name 2 numbers to check whether the chatbot is helping or hurting.

<details>
<summary>Model answer</summary>

1. **AI handles well:** order tracking, standard refund/return status, FAQs (delivery time, offers). **Human needed:** complaints involving money lost or wrong charges, and angry or sensitive cases (damaged expensive product, repeated failures).
2. **Metrics:** % of chats resolved without a human (containment rate), *and* customer satisfaction (CSAT) for AI chats vs human chats. A high containment rate with low CSAT means the bot is just blocking customers. Also: repeat-contact rate within 48 hours.
</details>

### 🗣️ English (15 min): AI as your speaking partner

Open **voice mode** in the Gemini or Claude app and say:

> *"I'm practising English for job interviews. Ask me simple questions about my day and my studies, one at a time. After each of my answers, repeat my sentence back in correct English, then ask the next question."*

Talk for 10 minutes. Don't worry about mistakes; the goal is speaking without stopping.

---

# Day 5 · Business basics: revenue, costs and profit (the P&L)

### 5.1 The Profit & Loss statement (P&L), line by line

| Line | Meaning | RainCraft example |
|---|---|---|
| **Revenue (Sales)** | Money earned from selling, whether collected yet or not | Invoices to shops + retail counter sales |
| − **COGS** (Cost of Goods Sold) | Direct cost of the products sold | Cost to make or import each umbrella sold |
| = **Gross Profit** | What's left to run the company | |
| **Gross Margin %** | Gross Profit ÷ Revenue | |
| − **Operating Expenses (Opex)** | Running costs | Salaries, rent, electricity, freight, marketing |
| = **Operating Profit (EBIT)** | Profit from the business itself | |
| − **Interest** | Cost of loans | Working-capital loan from the bank |
| = **Profit Before Tax (PBT)** | | |
| − **Tax** | | |
| = **Net Profit (PAT)** | The "bottom line" | |
| **Net Margin %** | Net Profit ÷ Revenue | |

### 5.2 Profit is not cash

Revenue is counted when the **invoice** is raised. Cash arrives when the **customer pays**.
If 86% of RainCraft's sales are on 30–60 days credit, the P&L can show a healthy profit while the bank account is nearly empty. **This is Mr. Sen's problem**, and you'll measure it tomorrow.

### 5.3 Two channels, two kinds of economics

- **B2B (shops):** large volumes, lower price (wholesale price minus discount), credit risk, freight cost
- **Retail counter (walk-in customers):** small volumes, full MRP, cash or UPI immediately, high margin

### 5.4 Unit economics: one umbrella

| Compact 3-Fold – Beige | Sold to a wholesaler | Sold at the counter |
|---|---|---|
| Price | ₹240 wholesale − 5% discount = **₹228** | MRP **₹399** |
| Cost | ₹168 | ₹168 |
| Gross profit per piece | **₹60** | **₹231** |
| Gross margin | **26.3%** | **57.9%** |

One umbrella sold at the counter earns almost **4× the gross profit** of one sold to a wholesaler. Wholesale wins on **volume**: one distributor order can be 200 pieces.

### 📺 Watch (about 35 minutes)

| Video | Language |
|---|---|
| [Profit and Loss Account Explained](https://www.youtube.com/watch?v=YaVV_hMDDCI) | Hindi |
| [Profit & Loss Statement in Excel](https://www.youtube.com/watch?v=uZuGCjPh-Qg) | Hinglish |

### ✍️ Assignment (about 60 min) → same workbook, new sheet **P&L**

**Inputs** (RainCraft, Apr–Jun 2025). Type these into an *Inputs* block at the top of the sheet:

| Input | Amount (₹) |
|---|---|
| B2B revenue (invoiced orders: Delivered + In Transit) | 49,91,653.20 |
| B2B cost of goods sold | 37,41,456.00 |
| Retail counter revenue | 7,87,494.10 |
| Retail cost of goods sold | 3,28,736.00 |
| Salaries & wages | 6,30,000 |
| Rent (factory, store, warehouses) | 2,40,000 |
| Electricity | 75,000 |
| Outward freight (delivery to customers) | 1,85,000 |
| Marketing | 40,000 |
| Office & admin | 60,000 |
| Interest on bank loan | 55,000 |
| Tax rate | 25% |

**Tasks:**
1. Build the P&L **with formulas that refer to the input cells** (no typed totals): Revenue, COGS, Gross Profit, Gross Margin %, total Opex, EBIT, Interest, PBT, Tax, Net Profit, Net Margin %.
2. Add a small **channel table**: Revenue, COGS, Gross Profit and Gross Margin % for **B2B** vs **Retail**.
3. **What-if:** change salaries to ₹7,00,000. What happens to Net Profit? (Then change it back.) This is why you never type totals by hand.
4. Write **3 insight lines** under the P&L. One must be about the two channels.
5. **Stretch:** open `orders.csv`, make it a Table, and prove the B2B revenue number yourself:
   `=SUMIFS(orders[invoice_amount], orders[order_status], "Delivered") + SUMIFS(orders[invoice_amount], orders[order_status], "In Transit")`

<details>
<summary>Answer key</summary>

| Line | ₹ |
|---|---|
| Revenue | 57,79,147.30 |
| COGS | 40,70,192.00 |
| **Gross Profit** | **17,08,955.30** (Gross Margin **29.57%**) |
| Opex | 12,30,000.00 |
| **EBIT** | **4,78,955.30** |
| Interest | 55,000.00 |
| PBT | 4,23,955.30 |
| Tax @25% | ≈ 1,05,988.83 |
| **Net Profit** | **≈ 3,17,966.48** (Net Margin **5.50%**) |

Channel gross margin: **B2B 25.05%** vs **Retail 58.26%**.
What-if (salaries ₹7,00,000): Net Profit falls by ₹52,500 (₹70,000 × 75%) to about ₹2,65,466.

Possible insights: (1) RainCraft is profitable, but keeps only about ₹5.50 of every ₹100 of sales as net profit. (2) Retail is a small share of revenue but earns more than double the margin of B2B. (3) Freight and credit are hidden costs of the B2B channel.
</details>

### 🔍 Case of the Day: why a quick-commerce order can lose money

**Question:** A customer places a ₹500 grocery order on a 10-minute delivery app. List the **revenue items** and **cost items** for the company on this one order. Then explain in 3 lines why the company can lose money on it.

<details>
<summary>Model answer</summary>

**Revenue:** product margin (the difference between selling price and buying price), delivery/handling/platform fee, payment from brands for ads and placement.
**Costs:** rider payment, packing, dark-store rent and staff (shared across orders), discount/coupon, payment-gateway fee, wastage of perishables, customer-support cost.
**Why a loss is possible:** on a ₹500 basket the product margin may be only ₹50–₹100. A rider, a coupon and a share of rent can cost more than that. Companies improve this with bigger baskets (higher average order value), more orders per store per hour, and ad income. This is **unit economics**: profit or loss per single order.
</details>

### 🗣️ English (10 min): update email to your manager

Write a 5–6 line email to Mr. Sen summarising the P&L. Use this skeleton:

> **Subject:** Q1 (Apr–Jun) P&L summary: profitable, retail margin much higher than B2B
> Dear Mr. Sen,
> Please find the Q1 P&L summary below.
> • Revenue was ₹__ lakh and net profit ₹__ lakh (__% net margin).
> • Retail earns __% gross margin vs __% for B2B.
> • [One concern]
> I will share the receivables (customer payments) analysis tomorrow.
> Regards, …

---

# Day 6 · Weekly Case Study: "Where is our money?" (about 2 hours)

### The situation

> Mr. Sen: *"Our P&L says we made a profit in Q1. Sales were our best ever. But the bank balance is low and I'm struggling to pay our China supplier. Tell me where the money is, who owes us, and what we should do. I need it by tomorrow."*

**Data:** `invoice_status.csv` (all invoices with money received **up to 30 June 2025**) and `customers.csv` (credit days and credit limits).

### Key terms

- **Outstanding** = invoice amount − amount received (money customers still owe)
- **Not yet due** = outstanding, but the due date hasn't come yet (normal credit)
- **Overdue** = outstanding **and** past the due date (a problem)
- **Days overdue** = as-of date − due date
- **Credit limit** = the maximum a customer is allowed to owe at one time

### Tasks → `my_work/W1_Receivables.xlsx` + `my_work/W1_case_where_is_our_money.md`

**Part A: Build (Excel)**
1. Open `invoice_status.csv`, save as `.xlsx`, make a Table named **Inv**.
2. In a cell outside the table, type the as-of date `30-06-2025` and name the cell **AsOf**: click the cell → type `AsOf` in the *Name Box* (left of the formula bar) → Enter.
3. Add columns:
   - `Outstanding` = `=ROUND([@invoice_amount]-[@amount_received],2)`
   - `Status` = `=IF([@Outstanding]<=0,"Paid",IF([@due_date]<AsOf,"Overdue","Not yet due"))`
   - `Days Overdue` = `=IF([@Status]="Overdue",AsOf-[@due_date],"")`

**Part B: Analyse (new sheet "Analysis")**

4. Totals: invoiced, received, outstanding, and **% collected**.
5. Outstanding split: **Not yet due** vs **Overdue** (`SUMIFS` on Status).
6. A customer table: `UNIQUE` customer names → total invoiced, outstanding, overdue, number of overdue invoices (`COUNTIFS`). Sort by outstanding.
7. Outstanding by **customer type**.
8. The **oldest** overdue invoice (`MAXIFS` on Days Overdue, or sort).
9. **Credit-limit check:** for the top 4 customers by outstanding, look up their `credit_limit` in `customers.csv` (by eye is fine this week; next week you'll use `XLOOKUP`). Is anyone above their limit?

**Part C: Recommend (Markdown note, 1 page)**

10. **3 findings**, each with a number.
11. **3 recommendations** that a small company could start next week.
12. **Email 1:** to Mr. Sen, max 150 words, summarising findings and recommendations.
13. **Email 2:** to the overdue customer with the most overdue invoices: a polite payment reminder that protects the relationship (list the invoices, total, request a payment date).

### Evaluation checklist (tick before you submit)

- [ ] Every number in the note can be traced to a formula in Excel
- [ ] The note separates **overdue** from **not yet due** (the most common beginner mistake is mixing them)
- [ ] Recommendations are specific (who, what, by when), not just "improve collections"
- [ ] Email to the customer is polite, specific, and has one clear ask
- [ ] Indian number format (lakh) used consistently

<details>
<summary>Answer key and model insights (open only after you finish)</summary>

**Numbers (as of 30 June 2025):**

| Item | ₹ |
|---|---|
| Invoiced (103 invoices) | 49,91,653.20 |
| Received | 24,98,705.99 (**50.1% collected**) |
| **Outstanding** | **24,92,947.21** |
| of which Not yet due (28 invoices) | 22,04,667.60 |
| of which **Overdue** (9 invoices) | **2,88,279.61** |

- Overdue by customer: **City Trading Co. (Siliguri, wholesaler): 6 invoices, ₹2,04,796.42** · Rupali Bastralaya: 3 invoices, ₹83,483.19
- Oldest overdue: **SO000004, City Trading Co., due 5 May 2025, 56 days overdue, ₹46,598.40**
- Biggest outstanding: Kamakhya Enterprises ₹11,59,619.40 · Rupali Trading Co. ₹5,57,206.20 · Saraswati Agencies ₹2,89,985.40 · City Trading Co. ₹2,72,588.02
- By type: Distributor ₹17,16,825.60 · Wholesaler ₹7,62,678.01 · Retailer ₹13,443.60
- **Credit limit breach:** Kamakhya Enterprises owes ₹11,59,619.40 against a ₹10,00,000 limit (**₹1,59,619.40 over**)
- Paid in full 66 · partly paid 3 · nothing paid yet 34
- The one retailer with outstanding (Diamond Wholesale, ₹13,443.60) is a cash customer whose order was invoiced on 30 June and is still in transit. Not a problem: they pay on delivery. Spotting this kind of "false alarm" is good analysis.

**Model findings:**
1. Half of Q1 sales (₹24.9 lakh) has not been collected. Most of it (₹22.0 lakh) is simply **not due yet**: the cash gap comes mainly from **giving 30–45 days credit during peak season**, not mainly from bad customers.
2. The real overdue problem is small and concentrated: ₹2.9 lakh, **71% of it from one wholesaler** (City Trading Co.) with 6 unpaid invoices, the oldest 56 days late.
3. **Concentration risk:** one distributor (Kamakhya) owes ₹11.6 lakh, which is 47% of all outstanding money, and is **above its credit limit**. If it pays late, RainCraft's cash crisis gets much worse.

**Model recommendations:**
1. **Hold new credit orders** for any customer above its credit limit or more than 30 days overdue, until a payment is received (starting with Kamakhya's limit and City Trading's overdue invoices).
2. **Reminder routine:** WhatsApp/email reminder 5 days before due date, on the due date, and 7 days after; the sales rep calls at 15 days overdue.
3. **Early-payment discount:** offer 1–1.5% off if paid within 10 days. A small margin cost buys faster cash in peak season.
4. **Weekly receivables report** to Mr. Sen every Monday (the table you just built: outstanding, overdue, top 5 debtors).
</details>

---

# Day 7 · Review, GitHub, LinkedIn & check-in

### 7.1 Review quiz (15 min)

<details><summary>1. In SUMIFS, which argument comes first?</summary>The sum range. <code>=SUMIFS(sum_range, criteria_range1, criteria1, …)</code></details>
<details><summary>2. What does <code>$B$1</code> do when you copy a formula?</summary>It keeps the reference fixed on B1 (absolute reference). F4 toggles it.</details>
<details><summary>3. Name 3 benefits of an Excel Table.</summary>Formulas copy automatically; ranges grow with new data; readable structured references; built-in Total Row and filters.</details>
<details><summary>4. Write the criteria to exclude cancelled orders.</summary><code>Sales[order_status], "&lt;&gt;Cancelled"</code></details>
<details><summary>5. Gross profit vs net profit?</summary>Gross profit = revenue − cost of goods sold. Net profit = what remains after all costs, including operating expenses, interest and tax.</details>
<details><summary>6. RainCraft's retail margin is ~58% and B2B ~25%. Why not sell only retail?</summary>Retail volume is small; B2B moves much larger quantities through shops across many states. The question is the right mix, plus cost control in B2B (freight, credit).</details>
<details><summary>7. Outstanding vs overdue?</summary>Outstanding = still unpaid. Overdue = unpaid and past the due date. Not-yet-due money is normal credit; overdue money is a problem.</details>
<details><summary>8. Why give AI your summary numbers instead of raw data?</summary>AI can make arithmetic mistakes on pasted data. Excel calculates reliably; AI is better at writing words around correct numbers.</details>
<details><summary>9. What are the 5 parts of R-C-T-F-R?</summary>Role, Context, Task, Format, Rules.</details>
<details><summary>10. Name the steps of the analyst loop.</summary>Question → Data → Clean → Analyse → Insight → Recommendation → Communicate.</details>

### 7.2 GitHub (15 min)

Upload this week's work into `Week_01/my_work/`:
`W1D1_company_map.md` · `W1_RainCraft_Q1.xlsx` · `W1D4_prompts.md` · `prompt_library.md` · `W1_Receivables.xlsx` · `W1_case_where_is_our_money.md` · `learning_log.md`
Then tick Week 1 ✅ in the main `README.md`.

### 7.3 LinkedIn (30 min)

**Profile headline** (update once, keep it honest):
```
MBA (Marketing & HR) | Building skills in Business & Operations Analytics: Excel, SQL, Power BI | Learning in public
```

**Post #1.** Pick one template, edit it in your own words, and post it. Add the post link to `linkedin/posts_log.md`.

<details>
<summary>Template A: short and professional</summary>

```
Week 1 of my 16-week journey to become a Business / Operations Analyst ✅

This week I worked on a practice project using simulated data for a fictional
umbrella manufacturer, and learned:
• How "order-to-cash" works, from a customer's order to money in the bank
• Excel SUMIFS, COUNTIFS and UNIQUE to answer business questions in seconds
• How to read a P&L, and why profit is not the same as cash

The most interesting finding: the company was profitable, but half of the
quarter's sales hadn't been collected yet, because most customers buy on
30–45 days credit during peak season.

Next week: cleaning messy real-world data. 

What's one Excel function you use every day at work?

#BusinessAnalysis #Excel #LearningInPublic
```
</details>

<details>
<summary>Template B: storytelling</summary>

```
"Sales are at a record high. So why is there no money in the bank?"

This was the question in my first practice case this week, on simulated data for
a fictional umbrella company. I've seen this problem up close in a real business,
so it felt very familiar.

Using Excel (SUMIFS, simple status columns, a summary table), I found:
→ Half of the quarter's sales were still with customers
→ Most of it wasn't late, just on 30–45 days credit
→ The real risk: one customer owed nearly half of all outstanding money,
  and was above their credit limit

Lesson: profit is an opinion, cash is a fact. 🙂

This is Week 1 of 16 in my journey to become a Business / Operations Analyst.
I'll share what I learn every week.

#OperationsAnalyst #BusinessAnalysis #Excel #LearningInPublic
```
</details>

**Posting tips:** post between 8–10 am on a weekday; reply to every comment; connect with 10 people this week (analysts at companies you'd like to join, classmates, people who comment).

### 7.4 Weekly reflection (10 min) → add to `learning_log.md`

1. What was the hardest part of this week?
2. Which topic do I want to revisit in the catch-up buffer?
3. On a scale of 1–5, how confident am I with SUMIFS? With explaining a P&L in English?
4. One thing I'll do differently next week.

### 7.5 Check-in with your mentor (30 min)

| Minutes | Agenda |
|---|---|
| 5 | Show the GitHub repo and the Week 1 tracker |
| 10 | Walk through the Day 6 case **in English**: 3 findings, 3 recommendations (practice for interviews) |
| 5 | One win, one struggle |
| 5 | Mentor asks 3 random questions from the quiz |
| 5 | Plan: which days of Week 2 might be tight (Puja, travel), and how to adjust |

---

## Week 1 glossary

| Term | Meaning |
|---|---|
| **B2B / B2C** | Business-to-business (selling to shops) / Business-to-consumer (selling to end customers) |
| **O2C / P2P** | Order-to-Cash (selling loop) / Procure-to-Pay (buying loop) |
| **SKU** | Stock Keeping Unit: one specific product (e.g. Compact 3-Fold – Beige) |
| **MRP** | Maximum Retail Price, the price printed on the product |
| **COGS** | Cost of Goods Sold, the direct cost of products sold |
| **Gross margin** | Gross profit ÷ revenue |
| **Credit days** | Days a customer is allowed before payment is due |
| **Outstanding / Overdue** | Unpaid / unpaid and past due date |
| **Credit limit** | Maximum a customer may owe at one time |
| **AOV** | Average Order Value = sales ÷ number of orders |
| **Unit economics** | Profit or loss on one unit or one order |
| **Hallucination** | When AI states something false with confidence |

---

**Next week (Week 2):** cleaning the messy file (`sales_lines_messy.csv`), `XLOOKUP`, `IF`/`IFS`, date functions, data validation, plus strategy frameworks (SWOT, PESTLE, Porter's Five Forces). Enjoy the Puja break first! 🪔
