# Dashboard Overview

This document describes the Power BI report in [`dashboard/Super Store Sales.pbix`](../dashboard/Super%20Store%20Sales.pbix) **exactly as it is saved**. Nothing in the report was modified.

## How the report was inspected

The PBIX is a zip package. It was opened **read-only** (on a copy, then confirmed byte-identical to the original by SHA-256) and the following parts were read:

| Part | What it gave |
|---|---|
| `Report/Layout` | Pages, visuals, titles, fields, aggregations, filters, slicer settings, forecast settings, navigation |
| `DataModel` (read with an open-source PBIX parser) | Tables, columns, data types, calculated columns, Power Query (M) code, auto-generated date tables |

**Could not be verified:** the report was never rendered, so displayed values, number formatting in practice, colours, text-box wording and the visual appearance were not seen. Statements below are about how the report is configured, not about how it looks.

## Report at a glance

| Item | Detail |
|---|---|
| Pages | 3: `Home`, `Trend`, `Forecasting` (canvas 1280 x 720) |
| Data | Imported from Excel into one table, `SuperStore_Sales` (5,901 rows) |
| Slicers | One **Region** slicer per page, synchronised across all three pages |
| Navigation | A page navigator on every page |
| Explicit DAX measures | None. All numbers are Power BI implicit aggregations (Sum or Average) of columns |
| Calculated columns | One: `Avg Delivery` (days between Order Date and Ship Date) |
| Relationships | None defined (single data table) |
| Not present | Drill-through pages, report tooltips, bookmarks, custom theme, custom visual-interaction settings |

## Page 1: Home

**Purpose:** a one-screen summary of sales by product, customer, region, shipping and payment dimensions.

| Element | Type | Configuration |
|---|---|---|
| Orders | Card | Sum of `Quantity` (units sold, see note 1) |
| Sales | Card | Sum of `Sales` |
| profits | Card | Sum of `Profit` |
| Ship Days | Card | Average of `Avg Delivery` (order-to-ship days) |
| Sales by Category | Clustered bar | Category, Sum of Sales |
| Sales by Sub Category | Clustered bar | Sub-Category, Sum of Sales, filtered to **Top 3** by Sales (note 2) |
| Sales by Ship Mode | Clustered bar | Ship Mode, Sum of Sales (filter in file: note 3) |
| Sales by Segment | Donut | Segment, Sum of Sales |
| Sales by Region | Donut | Region, Sum of Sales |
| Sales by Payment Mode | Donut | Payment Mode, Sum of Sales |
| Region | Slicer | Basic mode; synchronised with the other pages |

**Questions it answers:** which categories, segments, regions, ship modes and payment modes generate the most sales; how large the headline totals are.

## Page 2: Trend

**Purpose:** sales and profit over time, plus geography.

| Element | Type | Configuration |
|---|---|---|
| Sales by Month | Stacked area | Sum of Sales over the Order Date hierarchy (Year, Month, Day) |
| Profit by Month | Stacked area | Sum of Profit over the Order Date hierarchy |
| Sales and State | Map | State, Sum of Sales, Sum of Profit |
| Region | Slicer | Synchronised |

**Questions it answers:** how sales and profit move over 2019 and 2020; seasonal patterns; which states account for the most sales.

## Page 3: Forecasting

**Purpose:** short-term sales forecasts and a state ranking.

| Element | Type | Configuration |
|---|---|---|
| Sales Forecast - 15 days (top) | Line chart | Sum of Sales by Order Date with Power BI's built-in forecast (analytics pane); saved settings: forecast length 10, confidence level 90%, maximum seasonality 1 |
| Sales Forecast - 15 days (bottom) | Line chart | Same fields; saved settings: forecast length 10, confidence level 95%, maximum seasonality 10 |
| Sales by State | Clustered bar | State, Sum of Sales, filtered to **Top 10** by Sales (note 4) |
| Region | Slicer | Synchronised |

The forecasts use Power BI's built-in forecasting feature; no custom forecasting model or DAX is involved. The two charts carry the same title but different saved settings (note 5).

**Questions it answers:** what the sales trend suggests for the next period; which ten states sell the most.

## Filters and interactions

- The Region slicer filters every visual on its page and, because it is synchronised, applies the selection on the other pages too.
- No custom visual-interaction rules are stored, so Power BI's default cross-filtering and cross-highlighting between visuals applies.
- Visual-level filters: Top 3 Sub-Category (Home, two visuals), Top 10 State (Forecasting).
- Navigation: a page navigator button list on every page.
- Fonts and colours: no custom theme is applied; Arial is used in visuals.

## Navigation

Use the page navigator on the left side of each page to move between Home, Trend and Forecasting. The Region slicer keeps its selection when you change pages.

## Notes on how the report is configured

These are factual observations about the saved report, recorded so the documentation matches it. They are **not** changes; the report was left untouched.

1. **"Orders" card.** It sums `Quantity`, so it counts **units sold** (22,317 across the whole dataset). The number of distinct orders is 3,003.
2. **"Sales by Sub Category"** shows only the top 3 sub-categories by sales (Phones, Chairs, Binders in the full dataset), although the dataset has 17. The chart title does not mention the Top 3 filter, and the loss-making sub-categories (for example Tables) are therefore not visible on this chart.
3. **"Sales by Ship Mode".** The saved file contains a Top 3 filter on `Sub-Category` for this visual (the same filter as note 2). If it is applied as saved, the bars cover only sales from those three sub-categories (35.3% of total sales in the full dataset) instead of all sales. The report was not rendered, so this could not be confirmed visually.
4. **"Sales by State"** shows the top 10 of 49 states (69.2% of sales), also without the filter being named in the title.
5. **Forecast titles.** Both charts are titled "15 days" while the saved forecast length is 10 for each, with different confidence levels and seasonality settings. With only two years of data, the forecast should be read as indicative.
6. **"Ship Days" card.** It averages order-to-ship days (the data has no delivery date) and the card is configured to show 0 decimal places, while the average is 3.93 days.
7. **Profit by category, region or segment** is not shown on any page. Profit appears only over time (Trend) and by state on the map.

## Data source and refresh

The Power Query source is a file path on the original author's `Downloads` folder, so **Refresh will fail on another computer** until the data source is pointed to the workbook in `data/`. The PBIX stores an imported copy of the data, so the report opens and works without refreshing. See the README for the steps.
