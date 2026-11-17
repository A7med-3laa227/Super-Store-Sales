# Super Store Sales Analysis & Business Intelligence Dashboard

![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?logo=powerbi&logoColor=black)
![DAX](https://img.shields.io/badge/DAX-Calculated%20column-0078D4)
![Data](https://img.shields.io/badge/Data-5%2C901%20order%20lines-444444)

A three-page Power BI dashboard that analyzes the sales performance of a US retail company (2019 to 2020): sales and profit over time, product, customer, regional, shipping and payment views, and a short-term sales forecast.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Business Objectives](#business-objectives)
3. [Dataset Description](#dataset-description)
4. [Tools & Technologies](#tools--technologies)
5. [Dashboard Overview](#dashboard-overview)
6. [Key KPIs](#key-kpis)
7. [Key Business Questions](#key-business-questions)
8. [Key Insights](#key-insights)
9. [Repository Structure](#repository-structure)
10. [Screenshots](#screenshots)
11. [Future Improvements](#future-improvements)
12. [Author](#author)

## Project Overview

This is a portfolio project built in Microsoft Power BI. It takes an Excel sales dataset of 5,901 order lines (3,003 orders, 773 customers, 24 months) and turns it into an interactive report that lets a viewer explore how sales are distributed across product categories, customer segments, regions, states, ship modes and payment modes, and how sales and profit develop month by month.

The report covers these business areas: sales performance, profitability over time, product mix, regional performance, customer segments, shipping and payment. A Region slicer, synchronized across all pages, lets the viewer focus on one region at a time.

The documentation in [`docs/`](docs) goes beyond the report: it documents the dataset and its quality, records exactly how the dashboard is configured, and verifies the business insights against the source data.

## Business Objectives

The existing dashboard supports these objectives:

- Show total sales and profit and how they develop over time.
- Identify which product categories and sub-categories generate the most sales.
- Compare sales across regions and states.
- Compare sales across customer segments.
- Show how sales split across ship modes and payment modes, and the average time from order to shipment.
- Show seasonal patterns in sales and a short-term sales forecast.

Questions the report cannot answer on its own, such as profit by category or region and year-over-year growth, are listed in [`docs/business_questions.md`](docs/business_questions.md).

## Dataset Description

| Item | Detail |
|---|---|
| File | [`data/SuperStore Sales DataSet.xlsx`](data/SuperStore%20Sales%20DataSet.xlsx), sheet `Sheet1` |
| Source | Not documented in the repository and not verifiable. Its structure resembles the public "Superstore" sample data, so treat it as a practice dataset |
| Records | 5,901 order lines, 3,003 distinct orders, 773 customers, 1,742 product names |
| Granularity | One row per order line (one product on one order) |
| Period | Orders from 2019-01-01 to 2020-12-31 |
| Geography | United States: 4 regions, 49 states, 452 cities |
| Dimensions | Order ID, Order Date, Ship Date, Ship Mode, Customer, Segment, City, State, Region, Product, Category, Sub-Category, Payment Mode |
| Measures | Sales, Quantity, Profit (plus a `Returns` flag) |

**Known limitations:**

- No discount, cost or unit price columns, so profit can be described but not explained.
- No delivery date; only the ship date, so delivery performance cannot be measured.
- Two calendar years only.
- Data quality findings (for example 14 lines where Profit exceeds Sales, and a non-unique `ID` column) are documented in [`docs/data_quality_validation.md`](docs/data_quality_validation.md).

Column-by-column details are in [`docs/data_dictionary.md`](docs/data_dictionary.md).

## Tools & Technologies

| Tool | Use in this project |
|---|---|
| **Microsoft Power BI** | Report, visuals, slicers, page navigation, built-in forecasting |
| **Power Query** | Loads the Excel sheet, sets data types, renames the first column, replaces `#N/A` errors in `Returns` with 0, removes two empty columns |
| **DAX** | One calculated column, `Avg Delivery` (days between order and ship date). All other figures are Power BI implicit aggregations (Sum, Average) |
| **Microsoft Excel** | Source data file |

Python (pandas) was used **only** to independently check the dataset and the figures quoted in the documentation ([`scripts/validate_data.py`](scripts/validate_data.py)). It is not part of the dashboard.

## Dashboard Overview

The report has three pages. A page navigator and a synchronized Region slicer appear on each of them. Full details are in [`docs/dashboard_overview.md`](docs/dashboard_overview.md).

| Page | Purpose | Visuals |
|---|---|---|
| **Home** | One-screen summary of sales by product, customer, region, shipping and payment | 4 KPI cards; bar charts: Sales by Category, Sub Category (top 3), Ship Mode; donut charts: Sales by Segment, Region, Payment Mode |
| **Trend** | Sales and profit over time, plus geography | Sales by Month and Profit by Month (area charts); map of sales and profit by state |
| **Forecasting** | Short-term sales forecast and state ranking | Two line charts with Power BI's built-in forecast; Sales by State bar chart (top 10) |

**Filters and interactions:** the Region slicer filters every visual and keeps its selection when you change pages; visuals cross-filter each other with Power BI's default behavior. The sub-category and state bar charts show only the top 3 and top 10 respectively.

## Key KPIs

The four KPI cards on the Home page and how they are defined in the report:

| KPI (card title) | Definition | Calculation in the report | Why it matters |
|---|---|---|---|
| **Sales** | Total revenue of all order lines | Implicit Sum of `Sales` | Measures the size of the business |
| **profits** | Total profit of all order lines | Implicit Sum of `Profit` | Shows how much of sales is kept as profit |
| **Orders** | Units sold (see note) | Implicit Sum of `Quantity` | Shows sales volume |
| **Ship Days** | Average days between order and shipment | Implicit Average of the calculated column `Avg Delivery` | Indicates how quickly orders are processed |

The calculated column behind Ship Days is:

```dax
Avg Delivery = DATEDIFF(SuperStore_Sales[Order Date], SuperStore_Sales[Ship Date], DAY)
```

**Notes.** The card titled "Orders" sums `Quantity` (22,317 units across the dataset); the number of distinct orders is 3,003. "Ship Days" measures order-to-ship time because the data has no delivery date. The report defines no explicit DAX measures, and this README does not add any.

## Key Business Questions

| Area | Questions the report helps answer |
|---|---|
| Sales performance | What are total sales? How do sales change by month? Is there a seasonal pattern? What does the near-term forecast look like? |
| Profitability | What is total profit? How does profit change over time? Which states are profitable? |
| Product analysis | Which categories sell the most? Which sub-categories sell the most (top 3)? |
| Regional analysis | Which regions and states contribute most to sales? |
| Customer analysis | Which customer segments contribute most to sales? |
| Shipping and payment | How long does it take to ship an order? How do sales split across ship modes and payment modes? |

[`docs/business_questions.md`](docs/business_questions.md) marks each question as answered, partly answered, answerable from the data only, or not answerable.

## Key Insights

All figures were computed from the dataset and can be reproduced with `scripts/validate_data.py`. The dashboard was not rendered for this documentation, so values were not copied from its visuals. Details and recommendations are in [`docs/business_insights.md`](docs/business_insights.md).

- **Sales grew faster than profit.** Sales rose 77.3% from 2019 to 2020, but profit only 14.2%; the profit margin fell from 14.49% to 9.33%. *Recommendation: track margin next to sales and collect discount and cost data to explain the drop.*
- **Technology is the profit engine; Furniture is not.** Technology earned a 19.22% margin on 30.05% of sales; Furniture earned 2.22% on 28.84% of sales.
- **Some sub-categories lose money.** Tables lose 11,092 (margin -9.30%) despite being the sixth-largest sub-category by sales. The Home page shows only the top 3 sub-categories, so these do not appear there.
- **Ten of 49 states have negative profit,** including Texas (-14,078 on 116,262 of sales), the third-largest state by sales.
- **Sales peak in September, November and December** in both years; November and December alone are 27.9% (2019) and 29.7% (2020) of annual sales.
- **Data-quality caveat.** 14 lines with Profit greater than Sales carry 16.7% of total profit; without them the overall margin is 9.39% instead of 11.19%.

## Repository Structure

```text
Super-Store-Sales/
├── README.md
├── .gitignore
├── dashboard/
│   └── Super Store Sales.pbix
├── data/
│   └── SuperStore Sales DataSet.xlsx
├── docs/
│   ├── data_dictionary.md
│   ├── data_quality_validation.md
│   ├── dashboard_overview.md
│   ├── business_questions.md
│   └── business_insights.md
└── scripts/
    └── validate_data.py
```


## Future Improvements

None of the following exists in the current report:

- Add a profit margin KPI and year-over-year and month-over-month comparisons as explicit DAX measures.
- Count distinct orders for the "Orders" KPI and add average order value.
- Show profit by category, sub-category, region and segment, and show all sub-categories instead of the top 3.
- Build a dedicated date table instead of Power BI's automatic date tables.
- Use a parameter for the Excel file path so the report can be refreshed on any computer.
- Add drill-through pages and report tooltips for product and customer detail.
- Source discount, cost and delivery-date data to explain profit and measure real delivery performance.

## Author

**Ahmed Alaa**
GitHub: [https://github.com/A7med-3laa227](https://github.com/A7med-3laa227)
