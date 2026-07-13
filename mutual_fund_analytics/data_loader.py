from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, Optional, Union

import pandas as pd


DATA_DIR = Path(__file__).resolve().parent / "data" / "processed"


def load_processed_csv(file_path: Union[str, Path], parse_dates: Optional[Iterable[str]] = None) -> pd.DataFrame:
    """Load a processed CSV file from the mutual fund analytics dataset."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    parse_dates = list(parse_dates or [])
    return pd.read_csv(path, parse_dates=parse_dates)


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names to lowercase snake_case."""
    normalized = df.copy()
    normalized.columns = [
        col.strip().lower().replace(" ", "_").replace("-", "_") for col in normalized.columns
    ]
    return normalized


def clean_numeric_columns(df: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    """Replace invalid numeric values with NaN for selected columns."""
    cleaned = df.copy()
    for column in columns:
        if column in cleaned.columns:
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")
            cleaned[column] = cleaned[column].where(cleaned[column].notna() & (cleaned[column] > 0), pd.NA)
    return cleaned


def load_all_processed_files() -> Dict[str, pd.DataFrame]:
    """Load all processed CSV files in the analytics data folder."""
    files = {
        "nav_history": "nav_history_cleaned.csv",
        "scheme_performance": "scheme_performance_cleaned.csv",
        "aum_by_fund_house": "aum_by_fund_house_cleaned.csv",
        "monthly_sip_inflows": "monthly_sip_inflows_cleaned.csv",
        "category_inflows": "category_inflows_cleaned.csv",
        "investor_transactions": "investor_transactions_cleaned.csv",
        "industry_folio_count": "industry_folio_count_cleaned.csv",
        "portfolio_holdings": "portfolio_holdings_cleaned.csv",
        "fund_master": "fund_master_cleaned.csv",
    }

    return {
        name: load_processed_csv(DATA_DIR / filename)
        for name, filename in files.items()
    }
