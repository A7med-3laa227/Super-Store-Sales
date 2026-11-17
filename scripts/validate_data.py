"""
Data quality validation for the Super Store Sales dataset.

Reads data/SuperStore Sales DataSet.xlsx (read-only; the source file is never
modified) and prints a PASS / WARN / INFO report covering structure, missing
values, duplicates, dates, numeric ranges, key consistency and reconciliation
of totals. It also prints reference headline figures computed directly from the source
data, which the documentation in docs/ quotes.

Usage (from the repository root):
    pip install pandas openpyxl
    python scripts/validate_data.py
"""

from pathlib import Path

import openpyxl
import pandas as pd

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "SuperStore Sales DataSet.xlsx"

EXPECTED_COLUMNS = [
    "Order ID", "Order Date", "Ship Date", "Ship Mode", "Customer ID",
    "Customer Name", "Segment", "Country", "City", "State", "Region",
    "Product ID", "Category", "Sub-Category", "Product Name", "Sales",
    "Quantity", "Profit", "Returns", "Payment Mode", "ind1", "ind2",
]

results = []


def record(status, check, detail=""):
    results.append((status, check, detail))
    print(f"[{status:<4}] {check}" + (f": {detail}" if detail else ""))


def section(title):
    print(f"\n=== {title} ===")


# keep_default_na=False so Excel '#N/A' error cells in 'Returns' stay visible
raw = pd.read_excel(DATA_FILE, keep_default_na=False, na_values=[""])
first_col = raw.columns[0]
df = raw.rename(columns={first_col: "ID"}).copy()
n = len(df)

# ---------------------------------------------------------------- structure
section("1. Structure")
record("INFO", "Rows x columns", f"{n} x {df.shape[1]}")
missing_cols = [c for c in EXPECTED_COLUMNS if c not in df.columns]
record("PASS" if not missing_cols else "WARN", "Expected columns present", str(missing_cols or "all 22 + ID"))
record("WARN" if first_col != "Row ID" else "PASS",
       "First column header", f"'{first_col}' (malformed header; treated as a row ID, renamed 'ID' in Power Query)")

# ---------------------------------------------------------------- missing values
section("2. Missing / placeholder values")
# pandas turns Excel error cells into NaN, so count them with openpyxl instead
ws = openpyxl.load_workbook(DATA_FILE, read_only=True, data_only=True).active
header = [c.value for c in next(ws.iter_rows(min_row=1, max_row=1))]
ret_idx = header.index("Returns")
error_cells = sum(1 for row in ws.iter_rows(min_row=2, values_only=True) if str(row[ret_idx]).startswith("#"))
returns_flag = int((df["Returns"] == 1).sum())
record("INFO", "Returns column",
       f"{returns_flag} cells = 1 (flagged), {error_cells} cells are Excel error values ('#N/A'); Power Query replaces errors with 0")
for col in ["ind1", "ind2"]:
    empty = int(df[col].isna().sum())
    record("WARN" if empty == n else "PASS", f"Column '{col}' empty", f"{empty}/{n} rows blank (no content; removed in Power Query)")
core = [c for c in EXPECTED_COLUMNS if c not in ("ind1", "ind2", "Returns")]
nulls = {c: int(df[c].isna().sum()) for c in core if df[c].isna().sum() > 0}
record("PASS" if not nulls else "WARN", "Nulls in business columns (excluding Returns, ind1, ind2)", str(nulls or "none"))

# ---------------------------------------------------------------- duplicates
section("3. Duplicates")
exact = int(df.drop(columns=["ID"]).duplicated().sum())
record("PASS" if exact == 0 else "WARN", "Exact duplicate rows (ignoring ID)", str(exact))
dup_ids = df.loc[df["ID"].duplicated(keep=False), ["ID", "Order ID"]]
record("WARN" if len(dup_ids) else "PASS", "Duplicate values in ID column",
       f"{dup_ids['ID'].nunique()} ID value(s) shared by {len(dup_ids)} rows; Order IDs: {sorted(dup_ids['Order ID'].unique())} -> ID is NOT a reliable primary key")
dup_lines = int(df.duplicated(["Order ID", "Product ID"], keep=False).sum())
record("INFO", "Same Order ID + Product ID on more than one line", f"{dup_lines} rows (not exact duplicates; may be separate line items)")

# ---------------------------------------------------------------- dates
section("4. Dates")
for col in ["Order Date", "Ship Date"]:
    ok = pd.api.types.is_datetime64_any_dtype(df[col]) and df[col].notna().all()
    record("PASS" if ok else "WARN", f"{col} is a valid date for every row", f"{df[col].min().date()} to {df[col].max().date()}")
ship_days = (df["Ship Date"] - df["Order Date"]).dt.days
record("PASS" if (ship_days >= 0).all() else "WARN", "Ship Date on or after Order Date", f"violations: {int((ship_days < 0).sum())}")
record("INFO", "Days between order and ship date", f"min {ship_days.min()}, max {ship_days.max()}, mean {ship_days.mean():.3f} (line level)")
cross_year = int((df["Ship Date"].dt.year > df["Order Date"].dt.year).sum())
record("INFO", "Lines shipped in the calendar year after the order", f"{cross_year} (Ship Date reaches {df['Ship Date'].max().date()}, i.e. 2021)")
months = df["Order Date"].dt.to_period("M").nunique()
record("PASS" if months == 24 else "WARN", "Months with orders", f"{months} of 24 (no gaps in the monthly series)")
per_order_dates = df.groupby("Order ID")["Order Date"].nunique()
record("WARN" if (per_order_dates > 1).any() else "PASS", "Order IDs with more than one Order Date",
       f"{int((per_order_dates > 1).sum())}: {list(per_order_dates[per_order_dates > 1].index)}")

# ---------------------------------------------------------------- numeric
section("5. Numeric fields")
record("PASS" if (df["Sales"] > 0).all() else "WARN", "Sales > 0 on every line", f"min {df['Sales'].min():.3f}")
qty_ok = (df["Quantity"] >= 1).all() and (df["Quantity"] % 1 == 0).all()
record("PASS" if qty_ok else "WARN", "Quantity is a whole number >= 1", f"range {df['Quantity'].min()} to {df['Quantity'].max()}")
neg = int((df["Profit"] < 0).sum())
record("INFO", "Loss-making lines (Profit < 0)", f"{neg} lines = {neg / n:.1%}; total loss {df.loc[df['Profit'] < 0, 'Profit'].sum():,.0f}; zero-profit lines: {int((df['Profit'] == 0).sum())}")
big_loss = int((df["Profit"] < -df["Sales"]).sum())
record("INFO", "Lines where the loss exceeds the sale value (margin below -100%)", str(big_loss))
profit_gt_sales = df[df["Profit"] > df["Sales"]]
record("WARN" if len(profit_gt_sales) else "PASS", "Lines where Profit > Sales (impossible if Profit = Sales - cost with cost >= 0)",
       f"{len(profit_gt_sales)} lines, e.g. {profit_gt_sales.sort_values('Profit', ascending=False)['Product Name'].head(2).tolist()}")
if len(profit_gt_sales):
    pg = profit_gt_sales
    kept = df.drop(profit_gt_sales.index)
    record("INFO", "Impact of the Profit > Sales lines",
           f"they carry {pg['Profit'].sum():,.0f} profit ({pg['Profit'].sum() / df['Profit'].sum():.1%} of total) on {pg['Sales'].sum():,.0f} sales; "
           f"overall margin {df['Profit'].sum() / df['Sales'].sum():.2%} -> {kept['Profit'].sum() / kept['Sales'].sum():.2%} without them")
record("INFO", "No Discount, Cost or Unit Price column", "profit drivers cannot be decomposed (limitation)")

# ---------------------------------------------------------------- consistency
section("6. Key / attribute consistency (distinct values per key should be 1)")
pairs = [
    ("Order ID", "Customer ID"), ("Order ID", "Ship Date"), ("Order ID", "Ship Mode"),
    ("Customer ID", "Customer Name"), ("Customer ID", "Segment"),
    ("Product ID", "Category"), ("Product ID", "Sub-Category"), ("Sub-Category", "Category"),
    ("State", "Region"), ("Product ID", "Product Name"), ("Order ID", "Payment Mode"), ("City", "State"),
]
for key, col in pairs:
    bad = int((df.groupby(key)[col].nunique() > 1).sum())
    status = "PASS" if bad == 0 else ("INFO" if (key, col) in [("City", "State")] else "WARN")
    note = " (expected: e.g. same city name in several states)" if (key, col) == ("City", "State") else ""
    record(status, f"{key} -> {col}", f"{bad} {key} value(s) map to more than one {col}{note}")
names_multi_id = int((df.groupby("Product Name")["Product ID"].nunique() > 1).sum())
text_cols = ["Customer Name", "City", "State", "Product Name", "Sub-Category"]
nbsp = {c: int(df[c].astype(str).str.contains("\u00a0").sum()) for c in text_cols}
nbsp = {c: v for c, v in nbsp.items() if v}
untrimmed = {c: int((df[c].astype(str) != df[c].astype(str).str.strip()).sum()) for c in text_cols}
untrimmed = {c: v for c, v in untrimmed.items() if v}
record("WARN" if nbsp else "PASS", "Non-breaking spaces (U+00A0) in text columns", str(nbsp or "none"))
record("WARN" if untrimmed else "PASS", "Leading/trailing spaces in text columns", str(untrimmed or "none"))
record("INFO", "Product Name -> Product ID", f"{names_multi_id} product names appear under more than one Product ID")
prefix = df["Product ID"].str[:3].map({"FUR": "Furniture", "OFF": "Office Supplies", "TEC": "Technology"})
record("PASS" if (prefix == df["Category"]).all() else "WARN", "Product ID prefix agrees with Category")
ret_mixed = int((df.assign(r=(df["Returns"] == 1)).groupby("Order ID")["r"].nunique() > 1).sum())
record("PASS" if ret_mixed == 0 else "WARN", "Returns flag is consistent within each order", f"orders with mixed flags: {ret_mixed}")
pm_multi = int((df.groupby("Order ID")["Payment Mode"].nunique() > 1).sum())
record("INFO", "Orders paid with more than one Payment Mode", f"{pm_multi} of {df['Order ID'].nunique()} orders -> Payment Mode is a line-level attribute")

# ---------------------------------------------------------------- reconciliation
section("7. Reconciliation (each breakdown must add up to the grand total)")
tot_sales, tot_profit, tot_qty = df["Sales"].sum(), df["Profit"].sum(), df["Quantity"].sum()
for dim in ["Category", "Sub-Category", "Region", "State", "Segment", "Ship Mode", "Payment Mode"]:
    s_ok = abs(df.groupby(dim)["Sales"].sum().sum() - tot_sales) < 1e-6
    p_ok = abs(df.groupby(dim)["Profit"].sum().sum() - tot_profit) < 1e-6
    record("PASS" if s_ok and p_ok else "WARN", f"Sales and Profit by {dim} sum to total")
yearly_orders = df.groupby(df["Order Date"].dt.year)["Order ID"].nunique().sum()
record("PASS" if yearly_orders == df["Order ID"].nunique() else "WARN", "Orders by year sum to distinct orders", f"{yearly_orders} vs {df['Order ID'].nunique()}")
cust_by_region = int(df.groupby("Region")["Customer ID"].nunique().sum())
record("INFO", "Distinct customers are not additive across regions", f"sum by region {cust_by_region} vs {df['Customer ID'].nunique()} distinct overall")

# ---------------------------------------------------------------- reference KPIs
section("8. Reference values computed from the source data")
orders = df["Order ID"].nunique()
year = df["Order Date"].dt.year
s19, s20 = df.loc[year == 2019, "Sales"].sum(), df.loc[year == 2020, "Sales"].sum()
p19, p20 = df.loc[year == 2019, "Profit"].sum(), df.loc[year == 2020, "Profit"].sum()
order_level_ship = df.drop_duplicates("Order ID").assign(d=lambda x: (x["Ship Date"] - x["Order Date"]).dt.days)["d"].mean()
ref = {
    "Total Sales": f"{tot_sales:,.2f}",
    "Total Profit": f"{tot_profit:,.2f}",
    "Profit Margin %": f"{tot_profit / tot_sales:.2%}",
    "Total Orders (distinct Order ID)": f"{orders:,}",
    "Order lines (rows)": f"{n:,}",
    "Total Quantity": f"{tot_qty:,}",
    "Average Order Value": f"{tot_sales / orders:,.2f}",
    "Total Customers (distinct)": f"{df['Customer ID'].nunique():,}",
    "Avg Days to Ship (line level)": f"{ship_days.mean():.3f}",
    "Avg Days to Ship (order level)": f"{order_level_ship:.3f}",
    "Sales 2019 / 2020": f"{s19:,.2f} / {s20:,.2f}",
    "Sales YoY % (2020 vs 2019)": f"{s20 / s19 - 1:.2%}",
    "Profit 2019 / 2020": f"{p19:,.2f} / {p20:,.2f}",
    "Profit YoY % (2020 vs 2019)": f"{p20 / p19 - 1:.2%}",
    "Margin 2019 / 2020": f"{p19 / s19:.2%} / {p20 / s20:.2%}",
    "Orders with a return flag": f"{int(df.loc[df['Returns'] == 1, 'Order ID'].nunique())} ({df.loc[df['Returns'] == 1, 'Order ID'].nunique() / orders:.2%} of orders)",
}
for k, v in ref.items():
    print(f"  {k:<38} {v}")

# ---------------------------------------------------------------- insight figures
section("9. Figures quoted in docs/business_insights.md")
df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.month
df["ShipDays"] = ship_days


def breakdown(dim, top=None):
    g = df.groupby(dim).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    g["Share%"] = 100 * g["Sales"] / tot_sales
    g["Margin%"] = 100 * g["Profit"] / g["Sales"]
    g = g.sort_values("Sales", ascending=False)
    print(f"\n  By {dim}:")
    print(g.head(top).round(2).to_string() if top else g.round(2).to_string())


for dim in ["Category", "Region", "Segment", "Ship Mode", "Payment Mode"]:
    breakdown(dim)
breakdown("Sub-Category")
breakdown("State", top=6)
state_profit = df.groupby("State")["Profit"].sum()
print(f"\n  States with negative total profit: {int((state_profit < 0).sum())} of {df['State'].nunique()}")
print("  Loss-making states:", state_profit[state_profit < 0].sort_values().round(0).to_dict())
top10_share = df.groupby("State")["Sales"].sum().nlargest(10).sum() / tot_sales
top3 = df.groupby("Sub-Category")["Sales"].sum().nlargest(3)
print(f"  Top 10 states share of sales: {top10_share:.1%}; top 3 sub-categories {list(top3.index)} share: {top3.sum() / tot_sales:.1%}")

print("\n  Monthly sales by year:")
print(df.pivot_table(index="Month", columns="Year", values="Sales", aggfunc="sum").round(0).to_string())
for yr in (2019, 2020):
    d = df[df["Year"] == yr]
    nd = d[d["Month"] >= 11]["Sales"].sum() / d["Sales"].sum()
    q4 = d[d["Month"] >= 10]["Sales"].sum() / d["Sales"].sum()
    top3m = d.groupby("Month")["Sales"].sum().nlargest(3).index.tolist()
    print(f"  {yr}: Nov+Dec share {nd:.1%}, Oct-Dec share {q4:.1%}, three highest months {sorted(top3m)}")
for yr in (2019, 2020):
    d = df[df["Year"] == yr]
    print(f"  {yr}: sales {d['Sales'].sum():,.2f}, profit {d['Profit'].sum():,.2f}, margin {d['Profit'].sum() / d['Sales'].sum():.2%}")
kept = df.drop(profit_gt_sales.index)
for yr in (2019, 2020):
    d = kept[kept["Year"] == yr]
    print(f"  {yr} margin without the Profit > Sales lines: {d['Profit'].sum() / d['Sales'].sum():.2%}")

print("\n  Average order-to-ship days by Ship Mode:")
print(df.groupby("Ship Mode")["ShipDays"].mean().round(2).sort_values().to_string())

ret = df[df["Returns"] == 1]
print(f"\n  Returns flag: {ret['Order ID'].nunique()} orders ({ret['Order ID'].nunique() / orders:.2%}), "
      f"{len(ret)} lines ({len(ret) / n:.2%}), sales on flagged lines {ret['Sales'].sum():,.2f} ({ret['Sales'].sum() / tot_sales:.2%} of sales)")

top1pct = df.nlargest(int(round(n * 0.01)), "Profit")
print(f"  Top 1% of lines by profit ({len(top1pct)} lines): {top1pct['Profit'].sum():,.0f} profit = {top1pct['Profit'].sum() / tot_profit:.1%} of total")
cop = df[df["Sub-Category"] == "Copiers"]
cop_kept = kept[kept["Sub-Category"] == "Copiers"]
print(f"  Copiers: sales {cop['Sales'].sum():,.0f}, profit {cop['Profit'].sum():,.0f}, margin {cop['Profit'].sum() / cop['Sales'].sum():.1%}; "
      f"without the Profit > Sales lines margin {cop_kept['Profit'].sum() / cop_kept['Sales'].sum():.1%}")
tech = kept[kept["Category"] == "Technology"]
print(f"  Technology margin without the Profit > Sales lines: {tech['Profit'].sum() / tech['Sales'].sum():.2%}")
tab = df[df["Sub-Category"] == "Tables"]
print(f"  Tables: {int((tab['Profit'] < 0).sum())} of {len(tab)} lines loss-making")
rc = df.pivot_table(index="Region", columns="Category", values=["Profit", "Sales"], aggfunc="sum")
print("  Region x Category margin %:")
print((100 * rc["Profit"] / rc["Sales"]).round(1).to_string())
cust = df.groupby("Customer ID")["Sales"].sum().sort_values(ascending=False)
print(f"  Customers: top 10 = {cust.head(10).sum() / tot_sales:.1%} of sales; top 10% ({int(len(cust) * 0.1)}) = {cust.head(int(len(cust) * 0.1)).sum() / tot_sales:.1%}")
print(f"  Profit from profitable lines {df.loc[df['Profit'] > 0, 'Profit'].sum():,.0f}; loss lines {df.loc[df['Profit'] < 0, 'Profit'].sum():,.0f}")

# ---------------------------------------------------------------- summary
section("Summary")
counts = {s: sum(1 for r in results if r[0] == s) for s in ("PASS", "WARN", "INFO")}
print(f"PASS: {counts['PASS']}   WARN: {counts['WARN']}   INFO: {counts['INFO']}")
