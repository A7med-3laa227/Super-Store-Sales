# Data Quality and Validation

All checks below are implemented in [`scripts/validate_data.py`](../scripts/validate_data.py) and can be re-run at any time:

```bash
pip install pandas openpyxl
python scripts/validate_data.py
```

The script only **reads** the source workbook. The original dataset is never modified; every cleaning step happens later, inside Power Query, so the source data and the transformed data stay separate.

**Result of the last run: 29 PASS, 9 WARN, 13 INFO.**

## What was checked and what was found

### Issues that need handling (WARN)

| # | Finding | Evidence | Handling |
|---|---|---|---|
| 1 | Malformed first column header | Header text is `Row ID+O6G3A1:R6` | Renamed to `ID` in Power Query. |
| 2 | `ind1` and `ind2` are empty | 5,901 of 5,901 rows blank | Removed in Power Query. |
| 3 | `ID` is not a unique key | ID 4918 is used by two different orders (`CA-2019-160304`, `CA-2020-163125`) | Not used as a key. `Order ID` + product are used to identify lines. |
| 4 | An order with two order dates | `CA-2019-160304` has two different Order Dates (a consequence of finding 3) | Kept as is; flagged. Impact: one order (about 0.03% of orders). |
| 5 | `Returns` holds Excel errors | 5,614 cells are `#N/A`, 287 cells are `1` | Power Query replaces errors with `0` (this step exists in the PBIX). |
| 6 | Product ID maps to two names | 28 Product IDs have two different names | No effect on the current visuals, which use category and sub-category. Relevant only if product-level analysis is added. |
| 7 | Payment Mode varies inside an order | 1,063 of 3,003 orders use more than one mode | Treated as a **line-level** attribute. Do not report "orders by payment mode" as if each order had one mode. |
| 8 | Non-breaking spaces in names | 139 rows in `Product Name` contain U+00A0 | Clean with `Text.Clean` / `Text.Replace` in Power Query if product-level analysis is added. |
| 9 | **Profit greater than Sales** | 14 lines (6 Copiers; others Storage, Phones, Accessories, Binders, Chairs) | Profit cannot exceed sales if cost is non-negative. These lines carry 29,312 profit (**16.7% of total**) on only 10,920 sales. Overall margin is 11.19% with them and 9.39% without. They are **kept** (the source cannot be corrected without the original data), but every insight that depends on margin states this sensitivity. |

### Informational findings (INFO)

- 1,098 loss-making lines (18.6%), total loss 91,710; 108 of them lose more than the sale value. Negative profit is plausible business data, not an error.
- 39 lines have exactly zero profit.
- Order-to-ship time ranges from 0 to 8 days (mean 3.927 at line level, 3.936 at order level).
- 76 lines ship in the calendar year after the order; Ship Date reaches 2021-01-05 while Order Date ends 2020-12-31.
- 14 rows (7 pairs) share the same Order ID and Product ID but are not exact duplicates; treated as separate line items.
- 52 city names occur in several states (normal for US city names), so City must always be combined with State.
- 15 product names appear under more than one Product ID.
- Distinct customers are not additive across regions (1,902 summed by region vs 773 overall), which matters when building customer KPIs.
- The dataset has no discount, cost or unit price columns.

### Checks that passed (PASS)

- All 22 expected business columns exist; no nulls in any business column except `Returns`, `ind1`, `ind2`.
- No exact duplicate rows.
- Every Order Date and Ship Date is a valid date; Ship Date is never before Order Date; all 24 months have orders.
- Sales > 0 on every line; Quantity is a whole number from 1 to 14.
- One customer per order; one ship date and one ship mode per order; one name and one segment per Customer ID.
- Product ID prefix (`FUR`, `OFF`, `TEC`) agrees with Category on every row; each sub-category belongs to one category; each state to one region.
- The Returns flag is consistent within each order (no order is partly returned).
- **Reconciliation:** Sales and Profit summed by Category, Sub-Category, Region, State, Segment, Ship Mode and Payment Mode each equal the grand totals; orders by year sum to the 3,003 distinct orders.

## Transformations (Power Query)

The PBIX applies these steps to `SuperStore_Sales` (taken from the saved query):

1. Load `Sheet1` from the Excel workbook and promote headers.
2. Set data types (text, date, whole number, decimal).
3. Rename the malformed first column to `ID`.
4. Replace errors in `Returns` with `0`.
5. Sort by `Returns` descending.
6. Re-apply data types.
7. Remove `ind1` and `ind2`.

One calculated column, `Avg Delivery`, is added in the model (order-to-ship days).

## How the results were validated

- **Source checks:** the script above, run against the workbook in this repository.
- **Independent reconciliation:** breakdown totals compared with the grand totals (section 7 of the script output).
- **Reference values:** the script prints headline figures computed directly from the source data (Total Sales 1,565,804.32; Total Profit 175,262.11; 22,317 units; 3,003 distinct orders; 773 customers; average order-to-ship time 3.927 days). Every figure quoted in `business_insights.md` comes from this kind of independent calculation.

### What has **not** been validated

The values displayed on the cards and charts inside the PBIX were **not** read back. Power BI Desktop is needed to render the report, and the PBIX file does not store query results. The figures in this documentation are therefore computed from the dataset, not copied from the dashboard. When the report is opened in Power BI Desktop with no slicer selected, the card values can be compared with the reference values above.

The PBIX and the Excel workbook were not modified by this validation; the script opens the workbook read-only.
