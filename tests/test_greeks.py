from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from pyrisklab.exceptions import GreeksError
from pyrisklab.greeks import calculate_greeks, calculate_greeks_for_market_path
from pyrisklab.models import OptionContract


def test_greeks_return_finite_values_for_normal_inputs():
    greeks = calculate_greeks(100, 100, 1.0, 0.05, 0.2, "call")
    assert all(np.isfinite(value) for value in greeks.values())


def test_call_delta_is_reasonable():
    assert 0 < calculate_greeks(100, 100, 1.0, 0.05, 0.2, "call")["delta"] < 1


def test_put_delta_is_reasonable():
    assert -1 < calculate_greeks(100, 100, 1.0, 0.05, 0.2, "put")["delta"] < 0


def test_near_expiry_handling_does_not_crash():
    greeks = calculate_greeks(100, 100, 0.0, 0.05, 0.2, "call")
    assert all(np.isfinite(value) for value in greeks.values())


def test_nonfinite_greek_parameter_fails():
    with pytest.raises(GreeksError, match="volatility"):
        calculate_greeks(100, 100, 1.0, 0.05, np.nan, "call")


def test_scalar_spot_with_vector_time_returns_vector_greeks():
    greeks = calculate_greeks(100, 100, np.array([0.25, 0.5, 1.0]), 0.05, 0.2, "call")
    assert greeks["delta"].shape == (3,)
    assert greeks["gamma"].shape == (3,)


def test_calculate_greeks_for_market_path_rejects_invalid_trading_days():
    market_path = pd.DataFrame(
        {"step": [0], "time_years": [0.0], "underlying_price": [100.0]}
    )
    option = OptionContract("SIM_STOCK", "CALL_105", "call", 105.0, 0.04, 0.2, 90)

    with pytest.raises(GreeksError, match="trading_days"):
        calculate_greeks_for_market_path(market_path, option, 0)
