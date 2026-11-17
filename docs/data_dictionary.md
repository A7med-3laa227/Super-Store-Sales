# Data Dictionary

Source file: `data/SuperStore Sales DataSet.xlsx` (sheet `Sheet1`).
Grain: **one row = one order line** (one product on one order). 5,901 rows, 3,003 distinct orders (about 1.97 lines per order; 1,559 orders have a single line).
Period: orders from 2019-01-01 to 2020-12-31 (24 months, no gaps).

The "Power BI type" column shows the data type the PBIX applies in Power Query. Counts were produced with `scripts/validate_data.py`.

## Columns

| Column | Power BI type | Role | Description and business meaning | Notes |
|---|---|---|---|---|
| `Row ID+O6G3A1:R6` (renamed **ID**) | Whole number | Identifier | Source row number. | Header text in the Excel file is malformed. **Not unique**: ID 4918 appears on two different orders (`CA-2019-160304`, `CA-2020-163125`). Do not use as a key. |
| **Order ID** | Text | Dimension (degenerate) | Business identifier of the order, shared by all lines of that order. Pattern: prefix (`CA` or `US`), order year, number, e.g. `CA-2019-160304`. | 3,003 distinct. The year in the ID matches the Order Date year on every row. |
| **Order Date** | Date | Dimension (time) | Date the customer placed the order. | 2019-01-01 to 2020-12-31. Primary date for all trend analysis. |
| **Ship Date** | Date | Dimension (time) | Date the order was shipped. | 2019-01-05 to 2021-01-05. 76 lines ship in the year after the order. Never earlier than Order Date. |
| **Ship Mode** | Text | Dimension | Shipping service: Standard Class, Second Class, First Class, Same Day. | 4 values. Constant within an order. |
| **Customer ID** | Text | Dimension key | Unique customer code. | 773 distinct. One name and one segment per ID. |
| **Customer Name** | Text | Dimension attribute | Customer's name. | 773 distinct, 1:1 with Customer ID. |
| **Segment** | Text | Dimension | Customer segment: Consumer, Corporate, Home Office. | 3 values. |
| **Country** | Text | Dimension | Country of the order. | Single value (United States). No analytical value; hide in the model. |
| **City** | Text | Dimension | Delivery city. | 452 distinct. 52 city names occur in more than one state, so a city must always be paired with its state. |
| **State** | Text | Dimension | Delivery state (49 values, includes District of Columbia). | Each state belongs to exactly one region. Used for the map and the state ranking. |
| **Region** | Text | Dimension | Sales region: West, East, Central, South. | 4 values (Central 13 states, East 14, South 11, West 11). Used by the slicer on every page. |
| **Product ID** | Text | Dimension key | Product code. Prefix identifies the category: `FUR`, `OFF`, `TEC`. | 1,755 distinct. 28 IDs carry two different product names. |
| **Category** | Text | Dimension | Top product level: Furniture, Office Supplies, Technology. | 3 values. Consistent with the Product ID prefix on every row. |
| **Sub-Category** | Text | Dimension | Second product level (17 values, e.g. Chairs, Phones, Binders). | Each sub-category belongs to one category. |
| **Product Name** | Text | Dimension attribute | Product description. | 1,742 distinct. 139 rows contain non-breaking spaces (U+00A0). 15 names appear under more than one Product ID. |
| **Sales** | Decimal number | Measure (additive) | Revenue of the order line. | Always > 0 (0.836 to 9,099.93). Currency is not stated in the source. Net or gross of discount is not stated. |
| **Quantity** | Whole number | Measure (additive) | Units sold on the line. | 1 to 14. Sum = 22,317 units. |
| **Profit** | Decimal number | Measure (additive) | Profit of the order line. | Negative on 1,098 lines (18.6%). 14 lines have Profit > Sales; see [`data_quality_validation.md`](data_quality_validation.md). |
| **Returns** | Whole number | Flag | 1 = the order is flagged as returned. | In the Excel file, 287 cells hold `1` and 5,614 cells hold the error value `#N/A`. Power Query replaces errors with `0`. The flag is consistent within each order (104 orders). Its exact meaning is not documented in the source. |
| **Payment Mode** | Text | Dimension | Payment method: COD, Online, Cards. | 3 values. Varies **within** an order (1,063 of 3,003 orders use more than one mode), so it is a line-level attribute. |
| `ind1`, `ind2` | (removed) | None | Unnamed helper columns. | Completely empty (5,901 of 5,901 blank). Removed in Power Query. |

## Calculated column in the existing PBIX

| Column | DAX | Meaning |
|---|---|---|
| **Avg Delivery** (table `SuperStore_Sales`) | `DATEDIFF(SuperStore_Sales[Order Date], SuperStore_Sales[Ship Date], DAY)` | Whole days between order and shipment. It measures **order-to-ship time**, not delivery to the customer (there is no delivery date in the data). The name is easy to misread; the dashboard labels the resulting card "Ship Days" (see `dashboard_overview.md`). |

## Dimensions and measures

- **Dimensions:** Order ID, Order Date, Ship Date, Ship Mode, Customer ID/Name, Segment, City, State, Region, Product ID/Name, Category, Sub-Category, Payment Mode.
- **Additive measures:** Sales, Quantity, Profit.
- **Derived metrics** (profit margin, average order value, distinct order count, growth): not stored in the data and not defined as explicit measures in the existing report. Where this documentation quotes them, they are computed from the source data and labelled as such.

## Limitations of the dataset

- No discount, unit price or cost columns, so profit and loss cannot be decomposed into price, discount or cost effects.
- No delivery date, so true delivery performance cannot be measured; only order-to-ship days.
- Only two calendar years (2019 and 2020): year-over-year comparison is limited to one pair of years, and seasonality rests on two cycles.
- Currency and the meaning of the `Returns` flag are not documented.
- The dataset source could not be verified from the repository. Its structure resembles the widely used public "Superstore" sample data with extra columns such as `Payment Mode`, but this is an observation, not a verified origin. Treat it as a practice dataset, not real company data.
