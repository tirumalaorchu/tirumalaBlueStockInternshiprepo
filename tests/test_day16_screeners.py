import pandas as pd

from day16_screeners import PresetScreeners


def make_universe() -> pd.DataFrame:
    rows = []
    for company_id in range(1, 93):
        for year in range(2020, 2026):
            latest = year == 2025
            rows.append(
                {
                    "company_id": company_id,
                    "company_name": f"Company {company_id:02d}",
                    "year": year,
                    "roe": 20 if company_id <= 10 else 8,
                    "de_ratio": (
                        0
                        if company_id <= 10 and latest
                        else 0.5
                        if company_id <= 15 and latest
                        else 0.8
                        if company_id <= 15
                        else 1.5
                    ),
                    "pe": 15 if company_id <= 20 else 35,
                    "pb": 2 if company_id <= 20 else 5,
                    "dividend_yield": 3 if company_id <= 20 else 0.5,
                    "dividend_payout": 50 if company_id <= 20 else 90,
                    "free_cash_flow_crore": 100 if company_id <= 50 else -100,
                    "revenue_crore": 6000 if company_id <= 10 else 2000,
                    "revenue_cagr_3yr": 15 if company_id <= 15 else 5,
                    "revenue_cagr_5yr": 20 if company_id <= 20 else 5,
                    "pat_cagr_5yr": 25 if company_id <= 20 else 5,
                }
            )
    return pd.DataFrame(rows)


def test_all_presets_return_between_five_and_fifty_companies():
    universe = make_universe()
    results = PresetScreeners(universe).run_all()

    assert universe["company_id"].nunique() == 92
    for name, result in results.items():
        assert 5 <= len(result) <= 50, f"{name} returned {len(result)} rows"
        assert result["company_id"].nunique() == len(result)


def test_each_preset_enforces_its_rules():
    results = PresetScreeners(make_universe()).run_all()

    quality = results["quality_compounder"]
    assert (quality["roe"] > 15).all()
    assert (quality["de_ratio"] < 1).all()
    assert (quality["free_cash_flow_crore"] > 0).all()
    assert (quality["revenue_cagr_5yr"] > 10).all()

    value = results["value_pick"]
    assert (value["pe"] < 20).all()
    assert (value["pb"] < 3).all()
    assert (value["de_ratio"] < 2).all()
    assert (value["dividend_yield"] > 1).all()

    growth = results["growth_accelerator"]
    assert (growth["pat_cagr_5yr"] > 20).all()
    assert (growth["revenue_cagr_5yr"] > 15).all()
    assert (growth["de_ratio"] < 2).all()

    dividend = results["dividend_champion"]
    assert (dividend["dividend_yield"] > 2).all()
    assert (dividend["dividend_payout"] < 80).all()
    assert (dividend["free_cash_flow_crore"] > 0).all()

    blue_chip = results["debt_free_blue_chip"]
    assert (blue_chip["de_ratio"] == 0).all()
    assert (blue_chip["roe"] > 12).all()
    assert (blue_chip["revenue_crore"] > 5000).all()

    turnaround = results["turnaround_watch"]
    assert (turnaround["revenue_cagr_3yr"] > 10).all()
    assert (turnaround["free_cash_flow_crore"] > 0).all()
    assert (turnaround["de_ratio"] < turnaround["previous_de_ratio"]).all()