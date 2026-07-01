# BlueStock Mutual Fund Dashboard

## Data Source

Preferred source:
- `bluestock_mf.db` at `d:\BlueStock\tirumalaBlueStockInternshiprepo\bluestock_mf.db`

Alternative source:
- Import cleaned CSVs from `mutual_fund_analytics/data/processed/`

Required tables:
- `dim_date`
- `dim_fund`
- `fact_nav`
- `fact_transactions`
- `fact_performance`
- `fact_aum`
- `fact_benchmark_indices`
- `fact_monthly_sip_inflows`
- `fact_category_inflows`
- `fact_industry_folio_count`
- `fact_portfolio_holdings`

## Data Model Relationships

Create these relationships in Power BI (one-to-many, single direction):
- `dim_fund[amfi_code]` -> `fact_nav[amfi_code]`
- `dim_fund[amfi_code]` -> `fact_transactions[amfi_code]`
- `dim_fund[amfi_code]` -> `fact_performance[amfi_code]`
- `dim_date[date_key]` -> `fact_nav[date_key]`
- `dim_date[date_key]` -> `fact_transactions[date_key]`
- `dim_date[date_key]` -> `fact_performance[date_key]`
- `dim_date[date_key]` -> `fact_aum[date_key]`
- `dim_date[date_key]` -> `fact_benchmark_indices[date_key]`
- `dim_date[date_key]` -> `fact_monthly_sip_inflows[date_key]`
- `dim_date[date_key]` -> `fact_category_inflows[date_key]`
- `dim_date[date_key]` -> `fact_industry_folio_count[date_key]`
- `dim_date[date_key]` -> `fact_portfolio_holdings[date_key]`

## Recommended Measures

### Industry overview measures
- Total AUM (₹ crore):
  ```DAX
  Total AUM = SUM(fact_aum[aum_crore])
  ```
- Total SIP Inflows (₹ crore):
  ```DAX
  Total SIP Inflows = SUM(fact_monthly_sip_inflows[sip_inflow_crore])
  ```
- Total Folios (crore):
  ```DAX
  Total Folios = SUM(fact_industry_folio_count[total_folios_crore])
  ```
- Schemes Count:
  ```DAX
  Total Schemes = DISTINCTCOUNT(dim_fund[amfi_code])
  ```

### Performance and analytics measures
- Average return (3 yr):
  ```DAX
  Avg Return 3Y = AVERAGE(fact_performance[return_3yr_pct])
  ```
- Average risk (StdDev):
  ```DAX
  Avg StdDev = AVERAGE(fact_performance[std_dev_ann_pct])
  ```
- Fund AUM for bubble size:
  ```DAX
  Fund AUM = SUM(fact_performance[aum_crore])
  ```
- Net transaction amount:
  ```DAX
  Net Transaction Amount = SUM(fact_transactions[amount_inr])
  ```
- SIP vs Lumpsum vs Redemption split:
  ```DAX
  SIP Amount = CALCULATE(SUM(fact_transactions[amount_inr]), fact_transactions[transaction_type] = "SIP")
  Lumpsum Amount = CALCULATE(SUM(fact_transactions[amount_inr]), fact_transactions[transaction_type] = "Lumpsum")
  Redemption Amount = CALCULATE(SUM(fact_transactions[amount_inr]), fact_transactions[transaction_type] = "Redemption")
  ```

### Trend measures
- Monthly transaction volume:
  ```DAX
  Monthly Transaction Volume = SUM(fact_transactions[amount_inr])
  ```
- Nifty 50 close value:
  Use `fact_benchmark_indices[close_value]` with `index_name` filter for Nifty 50.
- Category net inflow:
  ```DAX
  Category Net Inflow = SUM(fact_category_inflows[net_inflow_crore])
  ```

## Page Layouts

### Page 1 — Industry Overview
Cards:
- `Total AUM`
- `Total SIP Inflows`
- `Total Folios`
- `Total Schemes`

Visuals:
- Line chart: `dim_date[year]` or `dim_date[calendar_date]` vs `SUM(fact_aum[aum_crore])`
- Bar chart: `fact_aum[fund_house]` vs `SUM(fact_aum[aum_crore])`

### Page 2 — Fund Performance
Slicers:
- `dim_fund[fund_house]`
- `dim_fund[category]`
- `dim_fund[plan]`

Visuals:
- Scatter chart:
  - X axis: `fact_performance[return_1yr_pct]` or `return_3yr_pct`
  - Y axis: `fact_performance[std_dev_ann_pct]`
  - Size: `fact_performance[aum_crore]`
  - Details: `dim_fund[scheme_name]`
- Table: `dim_fund[scheme_name]`, `dim_fund[fund_house]`, `dim_fund[category]`, `fact_performance[return_1yr_pct]`, `fact_performance[std_dev_ann_pct]`, `fact_performance[aum_crore]`
- NAV line chart vs benchmark:
  - `dim_date[calendar_date]` on axis
  - `fact_nav[nav]` for selected fund
  - add `fact_benchmark_indices[close_value]` with `index_name = "Nifty 50"`

### Page 3 — Investor Analytics
Slicers:
- `fact_transactions[state]`
- `fact_transactions[age_group]`
- `fact_transactions[city_tier]`

Visuals:
- State transaction bar: `fact_transactions[state]` vs `SUM(amount_inr)`
- Donut: `fact_transactions[transaction_type]` vs `SUM(amount_inr)`
- Age group bar: `fact_transactions[age_group]` vs `AVERAGE(fact_transactions[amount_inr])`
- Monthly transaction line: `dim_date[calendar_date]` vs `SUM(fact_transactions[amount_inr])`

### Page 4 — SIP & Market Trends
Visuals:
- Dual-axis chart:
  - Bar: `dim_date[calendar_date]` vs `SUM(fact_monthly_sip_inflows[sip_inflow_crore])`
  - Line: `fact_benchmark_indices[close_value]` filtered to `Nifty 50`
- Heatmap: `fact_category_inflows[month]` on rows, `fact_category_inflows[category]` on columns, `SUM(net_inflow_crore)` as values
- Top 5 categories by FY25 net inflow: use `TOPN(5, SUM(fact_category_inflows[net_inflow_crore]))` and show bar chart.

## Interactivity

- Enable cross-filtering between page charts.
- Use tooltips where available for:
  - AUM trend points
  - fund bubbles (show scheme, return, risk, AUM, category)
  - transaction bars
- Drill-through:
  - Create a detail page called `NAV Detail`
  - Add `dim_fund[scheme_name]` or `dim_fund[amfi_code]` as drill-through field
  - Include NAV time series and benchmark comparison on drill-through page

## Theme and Branding

- Import or manually configure Bluestock colors in Power BI theme.
- Use `Bluestock` palette for consistent card/visual styling.
- Add logo on each page as report image.

## Export checklist

1. Save the report as `bluestock_mf_dashboard.pbix`.
2. Export the report to PDF from Power BI Desktop.
3. Export each page to PNG using `File > Export > Export current page as PNG` or `Export > Export report to PDF/PNG`.
4. Name outputs:
   - `Dashboard.pdf`
   - `Page1_Industry_Overview.png`
   - `Page2_Fund_Performance.png`
   - `Page3_Investor_Analytics.png`
   - `Page4_SIP_Market_Trends.png`

## Notes

- `fact_performance` has a single performance snapshot per fund; use this table for risk/return and AUM bubble sizing.
- Use `dim_date` to normalize date relationships and build fiscal/year filters.
- For Nifty 50 benchmark, filter `fact_benchmark_indices[index_name]` explicitly.
