
from typing import Optional


def net_profit_margin(net_profit: float, sales: float) -> Optional[float]:
    """
    Net Profit Margin = (Net Profit / Sales) * 100
    """
    if sales == 0:
        return None
    return (net_profit / sales) * 100


def operating_profit_margin(operating_profit: float,
                             sales: float,
                             opm_percentage: float = None):
    """
    Operating Profit Margin = (Operating Profit / Sales) * 100

    Returns:
        (calculated_opm, mismatch)

    mismatch=True if difference > 1%
    """
    if sales == 0:
        return None, False

    calculated = (operating_profit / sales) * 100

    mismatch = False
    if opm_percentage is not None:
        if abs(calculated - opm_percentage) > 1:
            mismatch = True

    return calculated, mismatch


def return_on_equity(net_profit: float,
                     equity_capital: float,
                     reserves: float) -> Optional[float]:
    """
    ROE = Net Profit / (Equity + Reserves) * 100
    """

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return (net_profit / equity) * 100


def return_on_capital_employed(ebit: float,
                               equity_capital: float,
                               reserves: float,
                               borrowings: float) -> Optional[float]:
    """
    ROCE = EBIT / (Equity + Reserves + Borrowings) * 100
    """

    capital = equity_capital + reserves + borrowings

    if capital <= 0:
        return None

    return (ebit / capital) * 100


def check_roce_benchmark(roce: float,
                         broad_sector: str,
                         sector_benchmark: float = None):
    """
    Financial sector uses sector benchmark.
    Others use absolute threshold of 15%.
    """

    if roce is None:
        return False

    if broad_sector.lower() == "financials":
        if sector_benchmark is None:
            raise ValueError("Sector benchmark required.")

        return roce >= sector_benchmark

    return roce >= 15


def return_on_assets(net_profit: float,
                     total_assets: float) -> Optional[float]:
    """
    ROA = Net Profit / Total Assets * 100
    """

    if total_assets == 0:
        return None

    return (net_profit / total_assets) * 100