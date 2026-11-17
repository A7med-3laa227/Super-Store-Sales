# Business Questions

This document lists the business questions the project addresses and states honestly **how well the existing dashboard answers each one**.

- **Answered**: a visual in the report shows it directly.
- **Partly**: the report shows part of the answer, or the answer needs a caveat.
- **Dataset only**: the data can answer it, but no report visual does. Verified results are in [`business_insights.md`](business_insights.md).
- **Not answerable**: the dataset does not contain what is needed.

Page names refer to the report pages `Home`, `Trend` and `Forecasting` (see [`dashboard_overview.md`](dashboard_overview.md)).

## Sales performance

| Question | Status | Where |
|---|---|---|
| What are total sales? | Answered | Home, Sales card |
| How do sales change month to month? | Answered | Trend, Sales by Month |
| Are there seasonal sales patterns? | Answered (two years only) | Trend, Sales by Month |
| What might sales look like in the near term? | Partly | Forecasting; built-in forecast with two different saved settings |
| How did 2020 compare with 2019? | Dataset only | No year-over-year visual or measure exists |

## Profitability

| Question | Status | Where |
|---|---|---|
| What is total profit? | Answered | Home, profits card |
| How does profit change over time? | Answered | Trend, Profit by Month |
| What is the overall profit margin? | Dataset only | No margin KPI in the report |
| Which categories, sub-categories or regions are most or least profitable? | Dataset only | The report shows sales by these, not profit |
| Which states make a profit or a loss? | Partly | Trend, map (sales and profit fields) |
| Why are some products loss-making? | Not answerable | No discount, cost or price columns |

## Product analysis

| Question | Status | Where |
|---|---|---|
| Which categories generate the most sales? | Answered | Home, Sales by Category |
| Which sub-categories sell the most? | Partly | Home, Sales by Sub Category shows only the top 3 of 17 |
| Which sub-categories sell least or lose money? | Dataset only | Hidden by the Top 3 filter |
| Which individual products perform best? | Dataset only | No product-level visual |

## Regional analysis

| Question | Status | Where |
|---|---|---|
| Which regions contribute most to sales? | Answered | Home, Sales by Region |
| Which states contribute most to sales? | Answered | Forecasting, Sales by State (top 10); Trend, map |
| How does a single region look in detail? | Answered | Region slicer on every page |
| Which regions are most profitable? | Dataset only | Not shown by region |

## Customer analysis

| Question | Status | Where |
|---|---|---|
| Which customer segments generate the most sales? | Answered | Home, Sales by Segment |
| Which segments are most profitable? | Dataset only | Not shown |
| How concentrated is revenue among customers? | Dataset only | No customer-level visual |

## Shipping and payment

| Question | Status | Where |
|---|---|---|
| What is the average time from order to shipment? | Answered | Home, Ship Days card (shown with 0 decimals) |
| How is sales split across ship modes? | Partly | Home, Sales by Ship Mode (see the filter note in the dashboard overview) |
| How fast is each ship mode? | Dataset only | No visual compares ship days by mode |
| How is sales split across payment modes? | Answered | Home, Sales by Payment Mode |
| How long does delivery take for customers? | Not answerable | There is no delivery date, only a ship date |

## Returns

| Question | Status | Where |
|---|---|---|
| How many orders were returned? | Dataset only | The `Returns` column is not used in any visual; its exact meaning is undocumented |
