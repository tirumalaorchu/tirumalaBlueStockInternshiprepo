import os
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
from sqlalchemy import create_engine, text

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "mutual_fund_analytics" / "data"
PROCESSED_DIR = RAW_DIR / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = ROOT / "bluestock_mf.db"
SCHEMA_FILE = ROOT / "schema.sql"


def clean_nav_history():
    df = pd.read_csv(RAW_DIR / "02_nav_history.csv", parse_dates=["date"])
    df = (
        df.drop_duplicates(["amfi_code", "date"], keep="last")
        .sort_values(["amfi_code", "date"])
        .reset_index(drop=True)
    )
    df["nav"] = pd.to_numeric(df["nav"], errors="coerce")
    df = df[df["nav"] > 0].copy()

    filled_rows = []
    for amfi_code, group in df.groupby("amfi_code", sort=False):
        group = group.set_index("date").sort_index()
        full_index = pd.date_range(group.index.min(), group.index.max(), freq="B")
        group = group.reindex(full_index)
        group["amfi_code"] = amfi_code
        group["nav"] = group["nav"].ffill()
        group = group.dropna(subset=["nav"]).reset_index().rename(columns={"index": "date"})
        filled_rows.append(group)

    df_clean = pd.concat(filled_rows, ignore_index=True)
    df_clean.to_csv(PROCESSED_DIR / "nav_history_cleaned.csv", index=False, date_format="%Y-%m-%d")
    return df_clean


def clean_investor_transactions():
    df = pd.read_csv(RAW_DIR / "08_investor_transactions.csv")
    df["transaction_date"] = pd.to_datetime(df["transaction_date"], dayfirst=True, errors="coerce")

    type_map = {
        "sip": "SIP",
        "lumpsum": "Lumpsum",
        "lump sum": "Lumpsum",
        "lump_sum": "Lumpsum",
        "redemption": "Redemption",
        "redeem": "Redemption",
        "switch": "Switch",
    }

    df["transaction_type"] = (
        df["transaction_type"].astype(str)
        .str.strip()
        .str.lower()
        .map(type_map)
        .fillna(df["transaction_type"].astype(str).str.title())
    )

    df["amount_inr"] = pd.to_numeric(df["amount_inr"], errors="coerce")
    df = df[df["amount_inr"] > 0].copy()

    allowed_kyc = {"Verified", "Pending", "Not Verified", "Unverified", "Unknown"}
    df["kyc_status"] = (
        df["kyc_status"].astype(str)
        .str.strip()
        .replace({"not verified": "Not Verified", "unverified": "Unverified"})
        .where(lambda x: x.isin(allowed_kyc), "Unknown")
    )

    df = df.dropna(subset=["transaction_date"]).copy()
    df["transaction_date"] = df["transaction_date"].dt.date.astype(str)
    df.to_csv(PROCESSED_DIR / "investor_transactions_cleaned.csv", index=False)
    return df


def clean_scheme_performance():
    df = pd.read_csv(RAW_DIR / "07_scheme_performance.csv")

    numeric_cols = [
        "return_1yr_pct",
        "return_3yr_pct",
        "return_5yr_pct",
        "benchmark_3yr_pct",
        "alpha",
        "beta",
        "sharpe_ratio",
        "sortino_ratio",
        "std_dev_ann_pct",
        "max_drawdown_pct",
        "aum_crore",
        "expense_ratio_pct",
    ]

    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

    anomaly_reasons = []
    for _, row in df.iterrows():
        reasons = []
        for col in ["return_1yr_pct", "return_3yr_pct", "return_5yr_pct", "benchmark_3yr_pct"]:
            if pd.isna(row[col]):
                reasons.append(f"{col} missing")
            elif abs(row[col]) > 300:
                reasons.append(f"{col} outlier")
        if pd.isna(row["expense_ratio_pct"]):
            reasons.append("expense_ratio_pct missing")
        elif not (0.1 <= row["expense_ratio_pct"] <= 2.5):
            reasons.append("expense_ratio_pct out of range")
        anomaly_reasons.append("; ".join(reasons) if reasons else "OK")

    df["performance_quality"] = anomaly_reasons
    df.to_csv(PROCESSED_DIR / "scheme_performance_cleaned.csv", index=False)
    return df


def clean_shared_data():
    cleaned_files = []

    fund_master = pd.read_csv(RAW_DIR / "01_fund_master.csv", parse_dates=["launch_date"])
    fund_master["expense_ratio_pct"] = pd.to_numeric(fund_master["expense_ratio_pct"], errors="coerce")
    fund_master["exit_load_pct"] = pd.to_numeric(fund_master["exit_load_pct"], errors="coerce")
    fund_master["min_sip_amount"] = pd.to_numeric(fund_master["min_sip_amount"], errors="coerce")
    fund_master["min_lumpsum_amount"] = pd.to_numeric(fund_master["min_lumpsum_amount"], errors="coerce")
    fund_master.to_csv(PROCESSED_DIR / "fund_master_cleaned.csv", index=False, date_format="%Y-%m-%d")
    cleaned_files.append(fund_master)

    aum = pd.read_csv(RAW_DIR / "03_aum_by_fund_house.csv", parse_dates=["date"])
    aum[["aum_lakh_crore", "aum_crore", "num_schemes"]] = aum[["aum_lakh_crore", "aum_crore", "num_schemes"]].apply(pd.to_numeric, errors="coerce")
    aum.to_csv(PROCESSED_DIR / "aum_by_fund_house_cleaned.csv", index=False, date_format="%Y-%m-%d")
    cleaned_files.append(aum)

    monthly_sip = pd.read_csv(RAW_DIR / "04_monthly_sip_inflows.csv")
    monthly_sip["month"] = pd.to_datetime(monthly_sip["month"], format="%Y-%m", errors="coerce")
    monthly_sip[["sip_inflow_crore", "active_sip_accounts_crore", "new_sip_accounts_lakh", "sip_aum_lakh_crore", "yoy_growth_pct"]] = monthly_sip[["sip_inflow_crore", "active_sip_accounts_crore", "new_sip_accounts_lakh", "sip_aum_lakh_crore", "yoy_growth_pct"]].apply(pd.to_numeric, errors="coerce")
    monthly_sip["month"] = monthly_sip["month"].dt.strftime("%Y-%m")
    monthly_sip.to_csv(PROCESSED_DIR / "monthly_sip_inflows_cleaned.csv", index=False)
    cleaned_files.append(monthly_sip)

    category_inflows = pd.read_csv(RAW_DIR / "05_category_inflows.csv")
    if "month" in category_inflows.columns:
        category_inflows["month"] = pd.to_datetime(category_inflows["month"], format="%Y-%m", errors="coerce")
        category_inflows["month"] = category_inflows["month"].dt.strftime("%Y-%m")
    for col in category_inflows.columns:
        if col != "month":
            category_inflows[col] = pd.to_numeric(category_inflows[col], errors="coerce")
    category_inflows.to_csv(PROCESSED_DIR / "category_inflows_cleaned.csv", index=False)
    cleaned_files.append(category_inflows)

    industry_folio = pd.read_csv(RAW_DIR / "06_industry_folio_count.csv")
    if "month" in industry_folio.columns:
        industry_folio["month"] = pd.to_datetime(industry_folio["month"], format="%Y-%m", errors="coerce")
        industry_folio["month"] = industry_folio["month"].dt.strftime("%Y-%m")
    for col in industry_folio.columns:
        if col != "month":
            industry_folio[col] = pd.to_numeric(industry_folio[col], errors="coerce")
    industry_folio.to_csv(PROCESSED_DIR / "industry_folio_count_cleaned.csv", index=False)
    cleaned_files.append(industry_folio)

    holdings = pd.read_csv(RAW_DIR / "09_portfolio_holdings.csv", parse_dates=["portfolio_date"])
    holdings[["weight_pct", "market_value_cr", "current_price_inr"]] = holdings[["weight_pct", "market_value_cr", "current_price_inr"]].apply(pd.to_numeric, errors="coerce")
    holdings["portfolio_date"] = holdings["portfolio_date"].dt.strftime("%Y-%m-%d")
    holdings.to_csv(PROCESSED_DIR / "portfolio_holdings_cleaned.csv", index=False)
    cleaned_files.append(holdings)

    benchmark = pd.read_csv(RAW_DIR / "10_benchmark_indices.csv", parse_dates=["date"])
    benchmark["close_value"] = pd.to_numeric(benchmark["close_value"], errors="coerce")
    benchmark["date"] = benchmark["date"].dt.strftime("%Y-%m-%d")
    benchmark.to_csv(PROCESSED_DIR / "benchmark_indices_cleaned.csv", index=False)
    cleaned_files.append(benchmark)

    return cleaned_files


def build_date_dimension(date_series_list):
    dates = pd.concat(date_series_list, ignore_index=True).dropna().drop_duplicates()
    dates = pd.to_datetime(dates, errors="coerce").dropna().drop_duplicates().sort_values()
    dim_date = pd.DataFrame({
        "date_key": dates.dt.strftime("%Y-%m-%d"),
        "calendar_date": dates.dt.strftime("%Y-%m-%d"),
        "year": dates.dt.year,
        "quarter": dates.dt.quarter,
        "month": dates.dt.month,
        "day": dates.dt.day,
        "weekday": dates.dt.day_name(),
        "is_weekend": dates.dt.weekday >= 5,
    })
    return dim_date


def create_sqlite_database(nav_df, transactions_df, performance_df, aum_df, dim_fund_df, dim_date_df):
    if DB_PATH.exists():
        DB_PATH.unlink()

    engine = create_engine(f"sqlite:///{DB_PATH}")
    with engine.begin() as conn:
        conn.exec_driver_sql("PRAGMA foreign_keys=ON;")
        schema_sql = SCHEMA_FILE.read_text()
        for statement in schema_sql.split(";"):
            stmt = statement.strip()
            if stmt:
                conn.exec_driver_sql(stmt)

    dim_date_df.to_sql("dim_date", engine, if_exists="append", index=False)
    dim_fund_df.to_sql("dim_fund", engine, if_exists="append", index=False)

    nav_fact = nav_df.copy()
    nav_fact["date_key"] = nav_fact["date"].dt.strftime("%Y-%m-%d")
    nav_fact = nav_fact[["date_key", "amfi_code", "nav"]]
    nav_fact.to_sql("fact_nav", engine, if_exists="append", index=False)

    transactions_fact = transactions_df.copy()
    transactions_fact["date_key"] = pd.to_datetime(transactions_fact["transaction_date"]).dt.strftime("%Y-%m-%d")
    columns = ["date_key", "investor_id", "amfi_code", "transaction_date", "transaction_type", "amount_inr", "state", "city", "city_tier", "age_group", "gender", "annual_income_lakh", "payment_mode", "kyc_status"]
    transactions_fact = transactions_fact[columns]
    transactions_fact.to_sql("fact_transactions", engine, if_exists="append", index=False)

    performance_fact = performance_df.copy()
    performance_fact["performance_date"] = pd.Timestamp("2024-01-01")
    performance_fact["date_key"] = performance_fact["performance_date"].dt.strftime("%Y-%m-%d")
    fact_cols = [
        "amfi_code",
        "date_key",
        "return_1yr_pct",
        "return_3yr_pct",
        "return_5yr_pct",
        "benchmark_3yr_pct",
        "alpha",
        "beta",
        "sharpe_ratio",
        "sortino_ratio",
        "std_dev_ann_pct",
        "max_drawdown_pct",
        "aum_crore",
        "expense_ratio_pct",
        "morningstar_rating",
        "risk_grade",
        "performance_quality",
    ]
    performance_fact = performance_fact[fact_cols]
    performance_fact.to_sql("fact_performance", engine, if_exists="append", index=False)

    aum_fact = aum_df.copy()
    aum_fact["date_key"] = aum_fact["date"].dt.strftime("%Y-%m-%d")
    aum_fact = aum_fact[["date_key", "fund_house", "aum_lakh_crore", "aum_crore", "num_schemes"]]
    aum_fact.to_sql("fact_aum", engine, if_exists="append", index=False)

    with engine.connect() as conn:
        results = {
            "dim_date": pd.read_sql("SELECT COUNT(*) AS cnt FROM dim_date", conn).iloc[0, 0],
            "dim_fund": pd.read_sql("SELECT COUNT(*) AS cnt FROM dim_fund", conn).iloc[0, 0],
            "fact_nav": pd.read_sql("SELECT COUNT(*) AS cnt FROM fact_nav", conn).iloc[0, 0],
            "fact_transactions": pd.read_sql("SELECT COUNT(*) AS cnt FROM fact_transactions", conn).iloc[0, 0],
            "fact_performance": pd.read_sql("SELECT COUNT(*) AS cnt FROM fact_performance", conn).iloc[0, 0],
            "fact_aum": pd.read_sql("SELECT COUNT(*) AS cnt FROM fact_aum", conn).iloc[0, 0],
        }
    return results


def main():
    print("Cleaning data and generating processed CSVs...")
    nav_df = clean_nav_history()
    transactions_df = clean_investor_transactions()
    performance_df = clean_scheme_performance()
    shared = clean_shared_data()

    fund_master_clean = pd.read_csv(PROCESSED_DIR / "fund_master_cleaned.csv", parse_dates=["launch_date"])
    aum_clean = pd.read_csv(PROCESSED_DIR / "aum_by_fund_house_cleaned.csv", parse_dates=["date"])
    benchmark_clean = pd.read_csv(PROCESSED_DIR / "benchmark_indices_cleaned.csv", parse_dates=["date"])

    date_columns = [
        nav_df["date"],
        pd.to_datetime(transactions_df["transaction_date"], errors="coerce"),
        fund_master_clean["launch_date"],
        aum_clean["date"],
        pd.to_datetime(benchmark_clean["date"], errors="coerce"),
    ]
    dim_date_df = build_date_dimension(date_columns)

    results = create_sqlite_database(
        nav_df,
        transactions_df,
        performance_df,
        aum_clean,
        fund_master_clean,
        dim_date_df,
    )

    print("SQLite database loaded at", DB_PATH)
    print("Row counts:")
    for table_name, count in results.items():
        print(f"  {table_name}: {count}")

    csv_counts = {path.name: sum(1 for _ in pd.read_csv(path).itertuples()) for path in PROCESSED_DIR.glob("*_cleaned.csv")}
    print("Processed CSV row counts:")
    for name, count in csv_counts.items():
        print(f"  {name}: {count}")

    print("Done.")


if __name__ == "__main__":
    main()
