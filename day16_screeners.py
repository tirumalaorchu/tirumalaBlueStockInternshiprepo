from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd


class PresetScreeners:
    """Run the six Day 16 presets against a company fundamentals universe."""

    def __init__(self, data: pd.DataFrame | str | Path):
        if isinstance(data, pd.DataFrame):
            frame = data.copy()
        else:
            path = Path(data)
            if not path.is_file():
                raise FileNotFoundError(f"Input file not found: {path}")
            frame = pd.read_csv(path)

        frame.columns = [
            column.strip().lower().replace(" ", "_") for column in frame.columns
        ]
        self.data = frame
        self._require_columns({"company_id", "company_name"})
        if "year" in self.data.columns:
            self.latest = (
                self.data.sort_values(["company_id", "year"], kind="stable")
                .drop_duplicates("company_id", keep="last")
                .reset_index(drop=True)
            )
        else:
            self.latest = self.data.copy()

    def _require_columns(self, columns: Iterable[str]) -> None:
        missing = sorted(set(columns).difference(self.data.columns))
        if missing:
            raise ValueError("Missing required columns: " + ", ".join(missing))

    def _result(
        self, frame: pd.DataFrame, mask: pd.Series, preset: str
    ) -> pd.DataFrame:
        result = frame.loc[mask].copy()
        result["preset"] = preset
        return result.sort_values(
            ["company_name", "company_id"], kind="stable"
        ).reset_index(drop=True)

    def quality_compounder(self) -> pd.DataFrame:
        frame = self.latest
        self._require_columns(
            {"roe", "de_ratio", "free_cash_flow_crore", "revenue_cagr_5yr"}
        )
        mask = (
            frame["roe"].gt(15)
            & frame["de_ratio"].lt(1.0)
            & frame["free_cash_flow_crore"].gt(0)
            & frame["revenue_cagr_5yr"].gt(10)
        )
        return self._result(frame, mask, "Quality Compounder")

    def value_pick(self) -> pd.DataFrame:
        frame = self.latest
        self._require_columns({"pe", "pb", "de_ratio", "dividend_yield"})
        mask = (
            frame["pe"].gt(0)
            & frame["pe"].lt(20)
            & frame["pb"].gt(0)
            & frame["pb"].lt(3.0)
            & frame["de_ratio"].lt(2.0)
            & frame["dividend_yield"].gt(1)
        )
        return self._result(frame, mask, "Value Pick")

    def growth_accelerator(self) -> pd.DataFrame:
        frame = self.latest
        self._require_columns({"pat_cagr_5yr", "revenue_cagr_5yr", "de_ratio"})
        mask = (
            frame["pat_cagr_5yr"].gt(20)
            & frame["revenue_cagr_5yr"].gt(15)
            & frame["de_ratio"].lt(2.0)
        )
        return self._result(frame, mask, "Growth Accelerator")

    def dividend_champion(self) -> pd.DataFrame:
        frame = self.latest
        self._require_columns(
            {"dividend_yield", "dividend_payout", "free_cash_flow_crore"}
        )
        mask = (
            frame["dividend_yield"].gt(2)
            & frame["dividend_payout"].ge(0)
            & frame["dividend_payout"].lt(80)
            & frame["free_cash_flow_crore"].gt(0)
        )
        return self._result(frame, mask, "Dividend Champion")

    def debt_free_blue_chip(self) -> pd.DataFrame:
        frame = self.latest
        self._require_columns({"de_ratio", "roe", "revenue_crore"})
        mask = (
            frame["de_ratio"].eq(0)
            & frame["roe"].gt(12)
            & frame["revenue_crore"].gt(5000)
        )
        return self._result(frame, mask, "Debt-Free Blue Chip")

    def turnaround_watch(self) -> pd.DataFrame:
        self._require_columns(
            {"year", "revenue_cagr_3yr", "free_cash_flow_crore", "de_ratio"}
        )
        ordered = self.data.sort_values(["company_id", "year"], kind="stable").copy()
        ordered["latest_year"] = ordered.groupby("company_id")["year"].transform("max")
        ordered["previous_de_ratio"] = ordered.groupby("company_id")["de_ratio"].shift(1)
        mask = (
            ordered["year"].eq(ordered["latest_year"])
            & ordered["revenue_cagr_3yr"].gt(10)
            & ordered["free_cash_flow_crore"].gt(0)
            & ordered["de_ratio"].lt(ordered["previous_de_ratio"])
        )
        result = ordered.loc[mask].copy()
        result["preset"] = "Turnaround Watch"
        return result.sort_values(
            ["company_name", "company_id"], kind="stable"
        ).reset_index(drop=True)

    def run_all(self) -> dict[str, pd.DataFrame]:
        return {
            "quality_compounder": self.quality_compounder(),
            "value_pick": self.value_pick(),
            "growth_accelerator": self.growth_accelerator(),
            "dividend_champion": self.dividend_champion(),
            "debt_free_blue_chip": self.debt_free_blue_chip(),
            "turnaround_watch": self.turnaround_watch(),
        }

    def save_all(self, output_directory: str | Path) -> None:
        output_path = Path(output_directory)
        output_path.mkdir(parents=True, exist_ok=True)
        for name, result in self.run_all().items():
            result.to_csv(output_path / f"{name}.csv", index=False)