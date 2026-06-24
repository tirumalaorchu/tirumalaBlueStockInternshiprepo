# Data Dictionary

This document describes the cleaned data files and the SQLite star schema for the mutual fund analytics project.

## Processed CSV files

### nav_history_cleaned.csv
- `amfi_code` (integer): Unique AMFI identifier for each fund scheme.
- `date` (date): Business date for NAV value.
- `nav` (float): Net asset value per unit. Forward-filled for missing business days and validated to be greater than zero.

### investor_transactions_cleaned.csv
- `investor_id` (string): Unique investor identifier.
- `transaction_date` (date): Transaction date in YYYY-MM-DD format.
- `amfi_code` (integer): Fund scheme identifier.
- `transaction_type` (string): Standardized transaction type: SIP, Lumpsum, Redemption, Switch, etc.
- `amount_inr` (float): Transaction amount in Indian Rupees (validated > 0).
- `state` (string): Investor state.
- `city` (string): Investor city.
- `city_tier` (string): City tier classification.
- `age_group` (string): Age group bucket.
- `gender` (string): Investor gender.
- `annual_income_lakh` (float): Annual income in lakhs.
- `payment_mode` (string): Payment method used.
- `kyc_status` (string): KYC status normalized to Verified, Pending, Not Verified, Unverified, or Unknown.

### scheme_performance_cleaned.csv
- `amfi_code` (integer): Fund scheme identifier.
- `scheme_name` (string): Scheme name.
- `fund_house` (string): Asset management company.
- `category` (string): Fund category.
- `plan` (string): Plan type (Regular/Direct).
- `return_1yr_pct` (float): 1-year return percentage.
- `return_3yr_pct` (float): 3-year return percentage.
- `return_5yr_pct` (float): 5-year return percentage.
- `benchmark_3yr_pct` (float): 3-year benchmark return percentage.
- `alpha` (float): Alpha metric.
- `beta` (float): Beta metric.
- `sharpe_ratio` (float): Sharpe ratio.
- `sortino_ratio` (float): Sortino ratio.
- `std_dev_ann_pct` (float): Annualized standard deviation.
- `max_drawdown_pct` (float): Maximum drawdown percentage.
- `aum_crore` (float): Assets under management in crores.
- `expense_ratio_pct` (float): Expense ratio percentage.
- `morningstar_rating` (integer): Morningstar rating.
- `risk_grade` (string): Risk grade.
- `performance_quality` (string): Anomaly flag status.

### fund_master_cleaned.csv
- `amfi_code` (integer): Fund scheme identifier.
- `fund_house` (string): Asset management company.
- `scheme_name` (string): Scheme name.
- `category` (string): Fund category.
- `sub_category` (string): Fund sub-category.
- `plan` (string): Plan type.
- `launch_date` (date): Scheme launch date.
- `benchmark` (string): Benchmark index name.
- `expense_ratio_pct` (float): Expense ratio percentage.
- `exit_load_pct` (float): Exit load percentage.
- `min_sip_amount` (float): Minimum SIP amount.
- `min_lumpsum_amount` (float): Minimum lump-sum investment amount.
- `fund_manager` (string): Fund manager name.
- `risk_category` (string): Risk category.
- `sebi_category_code` (string): SEBI category code.

### aum_by_fund_house_cleaned.csv
- `date` (date): AUM snapshot date.
- `fund_house` (string): Asset management company.
- `aum_lakh_crore` (float): AUM value in lakh crores.
- `aum_crore` (float): AUM value in crores.
- `num_schemes` (integer): Number of schemes for the fund house.

### monthly_sip_inflows_cleaned.csv
- `month` (date): Month in YYYY-MM format.
- `sip_inflow_crore` (float): SIP inflow in crores.
- `active_sip_accounts_crore` (float): Active SIP accounts in crores.
- `new_sip_accounts_lakh` (float): New SIP accounts in lakhs.
- `sip_aum_lakh_crore` (float): SIP AUM in lakh crores.
- `yoy_growth_pct` (float): Year-over-year growth percentage.

### category_inflows_cleaned.csv
- `month` (date): Month in YYYY-MM format.
- Category-specific inflow columns (numeric): Inflows by category.

### industry_folio_count_cleaned.csv
- `month` (date): Month in YYYY-MM format.
- Industry folio count columns (numeric): Folio counts by industry.

### portfolio_holdings_cleaned.csv
- `amfi_code` (integer): Fund scheme identifier.
- `stock_symbol` (string): Holding security symbol.
- `stock_name` (string): Holding security name.
- `sector` (string): Sector classification.
- `weight_pct` (float): Portfolio weight percentage.
- `market_value_cr` (float): Market value in crores.
- `current_price_inr` (float): Current price in INR.
- `portfolio_date` (date): Holdings snapshot date.

### benchmark_indices_cleaned.csv
- `date` (date): Index date.
- `index_name` (string): Benchmark index name.
- `close_value` (float): Closing index value.

## Star schema tables

### dim_date
- `date_key` (TEXT): Primary key in YYYY-MM-DD.
- `calendar_date` (TEXT): Same as date_key.
- `year` (INTEGER): Calendar year.
- `quarter` (INTEGER): Calendar quarter.
- `month` (INTEGER): Calendar month.
- `day` (INTEGER): Calendar day.
- `weekday` (TEXT): Weekday name.
- `is_weekend` (BOOLEAN): Weekend flag.

### dim_fund
- `amfi_code` (INTEGER): Primary key.
- `fund_house` (TEXT): Asset manager.
- `scheme_name` (TEXT): Scheme name.
- `category` (TEXT): Fund category.
- `sub_category` (TEXT): Fund sub-category.
- `plan` (TEXT): Plan type.
- `benchmark` (TEXT): Benchmark index.
- `launch_date` (TEXT): Launch date.
- `expense_ratio_pct` (REAL): Expense ratio.
- `exit_load_pct` (REAL): Exit load.
- `min_sip_amount` (REAL): Minimum SIP value.
- `min_lumpsum_amount` (REAL): Minimum lumpsum value.
- `fund_manager` (TEXT): Fund manager.
- `risk_category` (TEXT): Risk category.
- `sebi_category_code` (TEXT): SEBI category code.

### fact_nav
- `nav_id` (INTEGER): Surrogate key.
- `date_key` (TEXT): Foreign key to `dim_date`.
- `amfi_code` (INTEGER): Foreign key to `dim_fund`.
- `nav` (REAL): Net asset value.

### fact_transactions
- `transaction_id` (INTEGER): Surrogate key.
- `date_key` (TEXT): Foreign key to `dim_date`.
- `investor_id` (TEXT): Investor identifier.
- `amfi_code` (INTEGER): Foreign key to `dim_fund`.
- `transaction_date` (TEXT): Raw transaction date.
- `transaction_type` (TEXT): Transaction type.
- `amount_inr` (REAL): Transaction amount.
- `state` (TEXT): Investor state.
- `city` (TEXT): Investor city.
- `city_tier` (TEXT): City tier.
- `age_group` (TEXT): Age group.
- `gender` (TEXT): Gender.
- `annual_income_lakh` (REAL): Annual income.
- `payment_mode` (TEXT): Payment mode.
- `kyc_status` (TEXT): KYC status.

### fact_performance
- `performance_id` (INTEGER): Surrogate key.
- `amfi_code` (INTEGER): Foreign key to `dim_fund`.
- `date_key` (TEXT): Foreign key to `dim_date`.
- `return_1yr_pct` (REAL): 1-year return.
- `return_3yr_pct` (REAL): 3-year return.
- `return_5yr_pct` (REAL): 5-year return.
- `benchmark_3yr_pct` (REAL): Benchmark 3-year return.
- `alpha` (REAL): Alpha value.
- `beta` (REAL): Beta value.
- `sharpe_ratio` (REAL): Sharpe ratio.
- `sortino_ratio` (REAL): Sortino ratio.
- `std_dev_ann_pct` (REAL): Annual volatility.
- `max_drawdown_pct` (REAL): Maximum drawdown.
- `aum_crore` (REAL): AUM in crores.
- `expense_ratio_pct` (REAL): Expense ratio.
- `morningstar_rating` (INTEGER): Morningstar rating.
- `risk_grade` (TEXT): Risk grade.
- `performance_quality` (TEXT): Cleaning status and anomaly flag.

### fact_aum
- `aum_id` (INTEGER): Surrogate key.
- `date_key` (TEXT): Foreign key to `dim_date`.
- `fund_house` (TEXT): Fund house.
- `aum_lakh_crore` (REAL): AUM value in lakh crores.
- `aum_crore` (REAL): AUM value in crores.
- `num_schemes` (INTEGER): Number of schemes.
