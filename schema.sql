CREATE TABLE IF NOT EXISTS dim_date (
    date_key TEXT PRIMARY KEY,
    calendar_date TEXT NOT NULL,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    day INTEGER,
    weekday TEXT,
    is_weekend BOOLEAN
);

CREATE TABLE IF NOT EXISTS dim_fund (
    amfi_code INTEGER PRIMARY KEY,
    fund_house TEXT,
    scheme_name TEXT,
    category TEXT,
    sub_category TEXT,
    plan TEXT,
    benchmark TEXT,
    launch_date TEXT,
    expense_ratio_pct REAL,
    exit_load_pct REAL,
    min_sip_amount REAL,
    min_lumpsum_amount REAL,
    fund_manager TEXT,
    risk_category TEXT,
    sebi_category_code TEXT
);

CREATE TABLE IF NOT EXISTS fact_nav (
    nav_id INTEGER PRIMARY KEY,
    date_key TEXT NOT NULL,
    amfi_code INTEGER NOT NULL,
    nav REAL,
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE IF NOT EXISTS fact_transactions (
    transaction_id INTEGER PRIMARY KEY,
    date_key TEXT NOT NULL,
    investor_id TEXT,
    amfi_code INTEGER,
    transaction_date TEXT,
    transaction_type TEXT,
    amount_inr REAL,
    state TEXT,
    city TEXT,
    city_tier TEXT,
    age_group TEXT,
    gender TEXT,
    annual_income_lakh REAL,
    payment_mode TEXT,
    kyc_status TEXT,
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE IF NOT EXISTS fact_performance (
    performance_id INTEGER PRIMARY KEY,
    amfi_code INTEGER NOT NULL,
    date_key TEXT NOT NULL,
    return_1yr_pct REAL,
    return_3yr_pct REAL,
    return_5yr_pct REAL,
    benchmark_3yr_pct REAL,
    alpha REAL,
    beta REAL,
    sharpe_ratio REAL,
    sortino_ratio REAL,
    std_dev_ann_pct REAL,
    max_drawdown_pct REAL,
    aum_crore REAL,
    expense_ratio_pct REAL,
    morningstar_rating INTEGER,
    risk_grade TEXT,
    performance_quality TEXT,
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

CREATE TABLE IF NOT EXISTS fact_aum (
    aum_id INTEGER PRIMARY KEY,
    date_key TEXT NOT NULL,
    fund_house TEXT,
    aum_lakh_crore REAL,
    aum_crore REAL,
    num_schemes INTEGER,
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
);

CREATE TABLE IF NOT EXISTS fact_benchmark_indices (
    benchmark_id INTEGER PRIMARY KEY,
    date_key TEXT NOT NULL,
    index_name TEXT,
    close_value REAL,
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
);

CREATE TABLE IF NOT EXISTS fact_monthly_sip_inflows (
    sip_inflow_id INTEGER PRIMARY KEY,
    date_key TEXT NOT NULL,
    sip_inflow_crore REAL,
    active_sip_accounts_crore REAL,
    new_sip_accounts_lakh REAL,
    sip_aum_lakh_crore REAL,
    yoy_growth_pct REAL,
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
);

CREATE TABLE IF NOT EXISTS fact_category_inflows (
    category_inflow_id INTEGER PRIMARY KEY,
    date_key TEXT NOT NULL,
    category TEXT,
    net_inflow_crore REAL,
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
);

CREATE TABLE IF NOT EXISTS fact_industry_folio_count (
    folio_count_id INTEGER PRIMARY KEY,
    date_key TEXT NOT NULL,
    total_folios_crore REAL,
    equity_folios_crore REAL,
    debt_folios_crore REAL,
    hybrid_folios_crore REAL,
    others_folios_crore REAL,
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
);

CREATE TABLE IF NOT EXISTS fact_portfolio_holdings (
    holding_id INTEGER PRIMARY KEY,
    date_key TEXT NOT NULL,
    amfi_code INTEGER,
    stock_symbol TEXT,
    stock_name TEXT,
    sector TEXT,
    weight_pct REAL,
    market_value_cr REAL,
    current_price_inr REAL,
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);
