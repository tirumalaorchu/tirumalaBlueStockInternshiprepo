import argparse
from pathlib import Path

import pandas as pd


def load_table(path: Path) -> pd.DataFrame:
    if not path.is_file():
        raise FileNotFoundError(f"Input file not found: {path}")
    with path.open("rb") as source:
        signature = source.read(8)
    return pd.read_excel(path, header=1) if signature.startswith(b"PK") else pd.read_csv(path, header=1)


def calculate_task15_kpis(frame: pd.DataFrame) -> pd.DataFrame:
    required = {
        "equity_capital", "reserves", "borrowings", "other_liabilities",
        "total_assets", "investments", "total_liabilities",
    }
    missing = sorted(required.difference(frame.columns))
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))

    result = frame.copy()
    result["net_worth"] = result["equity_capital"] + result["reserves"]
    result["capital_employed"] = result["total_assets"] - result["other_liabilities"]
    result["net_debt"] = result["borrowings"] - result["investments"]
    result["debt_to_equity"] = result["borrowings"].div(result["net_worth"])
    result["debt_to_equity"] = result["debt_to_equity"].where(result["net_worth"] > 0)
    result["debt_to_assets_pct"] = result["borrowings"].div(result["total_assets"]).mul(100)
    result["debt_to_assets_pct"] = result["debt_to_assets_pct"].where(result["total_assets"] != 0)
    result["balance_difference"] = result["total_assets"] - result["total_liabilities"]
    result["balance_status"] = result["balance_difference"].eq(0).map({True: "Balanced", False: "Check Required"})
    result["high_leverage_flag"] = result["debt_to_equity"].gt(5).fillna(False)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Calculate Task 15 capital-structure KPIs")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path, default=Path("results/financial_kpis_task15.csv"))
    args = parser.parse_args()
    result = calculate_task15_kpis(load_table(args.input))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output, index=False)
    print(f"Task 15 completed: {len(result)} records written")
    print(f"Saved result: {args.output}")


if __name__ == "__main__":
    main()