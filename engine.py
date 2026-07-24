from pathlib import Path
from typing import Iterable

import pandas as pd


class ScreenerEngine:
    """Calculate screening KPIs and filter companies by investment criteria."""

    def __init__(self, data: pd.DataFrame | str | Path):
        frame = data.copy() if isinstance(data, pd.DataFrame) else self._load_file(Path(data))
        self.data = self._calculate_kpis(frame)

    @staticmethod
    def _load_file(path: Path) -> pd.DataFrame:
        if not path.is_file():
            raise FileNotFoundError(f"Input file not found: {path}")
        with path.open("rb") as source:
            signature = source.read(8)
        if signature.startswith(b"PK"):
            return pd.read_excel(path, header=1)
        return pd.read_csv(path, header=1)

    @staticmethod
    def _require_columns(frame: pd.DataFrame, columns: Iterable[str]) -> None:
        missing = sorted(set(columns).difference(frame.columns))
        if missing:
            raise ValueError("Missing required columns: " + ", ".join(missing))

    @classmethod
    def _calculate_kpis(cls, frame: pd.DataFrame) -> pd.DataFrame:
        cls._require_columns(
            frame,
            {"equity_capital", "reserves", "borrowings", "other_liabilities", "total_assets"},
        )
        result = frame.copy()
        result["net_worth"] = result["equity_capital"] + result["reserves"]
        result["capital_employed"] = result["total_assets"] - result["other_liabilities"]
        if "net_profit" in result.columns:
            result["computed_roe"] = (
                result["net_profit"].div(result["net_worth"]).mul(100)
            ).where(result["net_worth"] > 0)
        if "operating_profit" in result.columns:
            result["computed_roce"] = (
                result["operating_profit"].div(result["capital_employed"]).mul(100)
            ).where(result["capital_employed"] > 0)
        result["de_ratio"] = result["borrowings"].div(result["net_worth"])
        result["de_ratio"] = result["de_ratio"].where(result["net_worth"] > 0)
        result["de_warning"] = result["de_ratio"].gt(1).fillna(False)
        return result

    def screen(
        self,
        min_roe: float = 15,
        max_de_ratio: float = 1,
        min_roce: float | None = None,
        sectors: Iterable[str] | None = None,
    ) -> pd.DataFrame:
        """Return rows matching the supplied screening criteria."""
        self._require_columns(self.data, {"computed_roe", "de_ratio"})
        selected = self.data["computed_roe"].ge(min_roe) & self.data["de_ratio"].lt(max_de_ratio)
        if min_roce is not None:
            self._require_columns(self.data, {"computed_roce"})
            selected &= self.data["computed_roce"].ge(min_roce)
        if sectors is not None:
            self._require_columns(self.data, {"broad_sector"})
            selected &= self.data["broad_sector"].isin(sectors)
        return self.data.loc[selected].copy()

    def save(self, frame: pd.DataFrame, output_path: str | Path) -> Path:
        destination = Path(output_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        frame.to_csv(destination, index=False)
        return destination