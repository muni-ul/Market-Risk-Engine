import numpy as np

from pyrisklab.application_service import run_portfolio_scenario
from pyrisklab.scenarios import MARKET_PRESETS, ScenarioInputs


def test_default_scenario_is_deterministic_and_reconciles():
    a = run_portfolio_scenario(ScenarioInputs(paths=100))
    b = run_portfolio_scenario(ScenarioInputs(paths=100))
    assert np.array_equal(a.portfolio_paths, b.portfolio_paths)
    final = a.representative.iloc[-1]
    assert np.isclose(final.portfolio_value, final.cash + final.stock_value + final.option_value)
    assert 0 <= a.summary["probability_below_start"] <= 1


def test_presets_are_professional_and_complete():
    assert "Baseline Market" in MARKET_PRESETS
    assert all({"drift", "volatility", "seed"} == set(v) for v in MARKET_PRESETS.values())


def test_invalid_allocation_has_helpful_error():
    errors = ScenarioInputs(cash_pct=50, stock_pct=60, option_pct=10).validate()
    assert any("total 100%" in error for error in errors)
