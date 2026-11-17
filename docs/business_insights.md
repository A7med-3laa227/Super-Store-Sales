# Business Insights

## How to read this document

- Every figure below was **computed from the source dataset** and is printed by section 9 of [`scripts/validate_data.py`](../scripts/validate_data.py), so each number can be reproduced.
- The dashboard itself was **not rendered**, so the numbers were not copied from its visuals. They match what the report's Sum and Average aggregations produce when no slicer is selected (all regions).
- Profit margin means `Profit / Sales`. The report has no margin KPI; margin is derived here from the data.
- The dataset has no discount, cost or price columns. Insights say **what** happened, not **why**; causes are listed as questions to investigate, never as findings.
- **Data-quality caveat:** 14 order lines have Profit greater than Sales (about 0.7% of sales but 16.7% of profit; see [`data_quality_validation.md`](data_quality_validation.md)). Where this materially changes an insight, both figures are given.

## Headline figures

| Metric | Value |
|---|---|
| Sales | 1,565,804 |
| Profit | 175,262 |
| Profit margin | 11.19% (9.39% without the 14 flagged lines) |
| Distinct orders / order lines | 3,003 / 5,901 |
| Units sold | 22,317 |
| Customers | 773 |
| Average order-to-ship time | 3.93 days |

---

## Insight 1: Sales grew much faster than profit in 2020

**Observation.** Sales rose from 564,680 (2019) to 1,001,125 (2020), an increase of **77.3%**. Profit rose only **14.2%**, from 81,823 to 93,439. The profit margin fell from **14.49% to 9.33%**. Without the 14 flagged lines the same pattern holds (11.92% to 7.96%).

**Significance.** Growth was not translating into proportional profit; each extra unit of sales was less profitable in 2020.

**Recommendation.** Treat margin as a primary KPI next to sales. Collect discount and cost data to find out why margin fell; the current data cannot explain it.

## Insight 2: Technology earns the most profit; Furniture earns almost none

**Observation.**

| Category | Sales | Share of sales | Profit | Margin |
|---|---|---|---|---|
| Office Supplies | 643,708 | 41.11% | 74,797 | 11.62% |
| Technology | 470,588 | 30.05% | 90,458 | 19.22% |
| Furniture | 451,509 | 28.84% | 10,007 | 2.22% |

Technology produces the largest profit from the second-largest sales. Furniture is almost as large as Technology in sales but yields about one ninth of its profit. (Technology's margin is 14.60% without the 14 flagged lines, still the highest.)

**Significance.** Sales share is a poor guide to where profit comes from. A dashboard that shows only sales by category (as the Home page does) hides this.

**Recommendation.** Review Furniture pricing, discounts and costs first; protect the Technology offer.

## Insight 3: A few sub-categories lose money

**Observation.** Tables lose **11,092** on 119,294 of sales (margin **-9.30%**); 121 of its 190 lines are loss-making. Supplies (-1,654, -4.50%) and Bookcases (-343, -0.60%) are also negative, and Machines is break-even (profit 38 on 91,988 of sales). At the other end, Copiers shows 71.6% (see Insight 8); among the remaining sub-categories with more than 50,000 in sales, Paper (21.23%), Accessories (20.72%) and Appliances (16.40%) have the highest margins.

**Significance.** Tables is the 6th-largest sub-category by sales yet destroys profit. The Home page's sub-category chart shows only the top 3 by sales (Phones, Chairs, Binders), so these loss-makers are not visible there.

**Recommendation.** Investigate Tables first (pricing, discounting, shipping cost) and show profit by sub-category on the dashboard.

## Insight 4: West leads; Central has the weakest margin

**Observation.**

| Region | Sales | Share | Profit | Margin |
|---|---|---|---|---|
| West | 522,441 | 33.37% | 67,860 | 12.99% |
| East | 450,235 | 28.75% | 53,400 | 11.86% |
| Central | 341,008 | 21.78% | 27,450 | 8.05% |
| South | 252,121 | 16.10% | 26,552 | 10.53% |

Central's weakness comes from Furniture, which runs at a **-1.5%** margin there (3.1% to 3.5% in the other regions).

**Significance.** Central has about 35% more sales than South but roughly the same profit (27,450 versus 26,552), and Furniture is a visible part of the gap.

**Recommendation.** Look at Furniture sales in the Central region before changing anything else in that region.

## Insight 5: Sales concentrate in a few states, and ten states lose money

**Observation.** California (335,190 sales, 49,372 profit) and New York (186,748 sales, 41,012 profit) lead. The top 10 states by sales make up **69.2%** of sales. **10 of 49 states** have negative total profit; the largest losses are Texas (-14,078 on 116,262 of sales, margin -12.1%), Illinois (-9,555), Ohio (-9,339) and Pennsylvania (-9,298). Texas is the third-largest state by sales.

**Significance.** A large state can still be unprofitable; ranking states by sales alone (as the state bar chart does) hides it.

**Recommendation.** Use the map's profit field or add profit to the state ranking, and review the loss-making states with the largest sales first.

## Insight 6: Sales peak in September and in November and December

**Observation.** In both years, the three highest months are **September, November and December**. November plus December account for 27.9% (2019) and 29.7% (2020) of the year's sales; October to December account for 35.5% and 38.6%.

**Significance.** The pattern repeats across both years, which supports planning around a late-year peak. Two years is a short history, so it is a pattern, not a proven seasonal law.

**Recommendation.** Plan stock and staffing for September and the November-December peak, and revisit the pattern as more years of data become available.

## Insight 7: Customer segments, ship modes and payment modes

**Observation.**

- **Segments:** Consumer is the largest (48.09% of sales); Corporate 32.55%, Home Office 19.35%. Margins are close (10.80%, 11.34%, 11.92%), so segment is not a strong profit driver.
- **Ship modes:** Standard Class carries **58.27%** of sales. Average order-to-ship time is 5.05 days for Standard Class, 3.22 for Second Class, 2.14 for First Class and 0.05 for Same Day. Margins range from 9.18% (Same Day) to 12.25% (First Class).
- **Payment modes:** COD 42.62% of sales, Online 35.38%, Cards 21.99%. Online has the lowest margin (9.76% versus 12.30% for COD). Payment Mode varies inside orders, so these are shares of order **lines**.

**Significance.** The business depends on Consumer customers and Standard shipping. Same Day is the fastest mode and also has the lowest margin; the data cannot show whether shipping cost is the reason.

**Recommendation.** Compare shipping cost with shipping revenue for Same Day if cost data becomes available; look at why Online lines earn a lower margin.

## Insight 8: Profit is concentrated in a small number of lines

**Observation.** The top 1% of order lines (59 lines) generate **49.5%** of total profit (86,838 of 175,262). Copiers earn 42,775 on 59,736 of sales (71.6% margin; 40.5% without the 14 flagged lines). In total, 1,098 lines (18.6%) lose money, losing 91,710 against 266,972 earned on profitable lines.

**Significance.** Total profit relies on a handful of large Copier and Technology lines, so results are sensitive to a few orders and to the data-quality issue above.

**Recommendation.** Verify the large-profit lines against the original source before drawing conclusions from them; report profit with and without outliers.

## Insight 9: Revenue is spread widely across customers

**Observation.** The top 10 customers account for 6.1% of sales and the top 10% of customers (77 of 773) for 29.9%.

**Significance.** Revenue is not dependent on a few accounts, so customer concentration risk appears low in this dataset.

## Insight 10: Returns (interpret with care)

**Observation.** 104 orders (3.46% of orders, 287 lines) carry a return flag, representing 5.64% of sales. The source does not document what the flag means.

**Significance.** The flagged share is small, but without a definition (returned, refunded, cancelled) it cannot be used for decisions. No report visual uses the Returns column.

**Recommendation.** Confirm the definition of the flag before using it in any KPI.

---

## What this analysis cannot say

- **Why** margins or profits differ (no discount, cost or price data).
- Whether customers actually received their orders on time (no delivery date).
- Anything about years other than 2019 and 2020.
- How the report looks when rendered or the exact values it displays.
