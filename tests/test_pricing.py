from __future__ import annotations

import numpy as np
import pytest

from pyrisklab.exceptions import PricingError
from pyrisklab.pricing import black_scholes_price


def test_known_call_price():
    assert black_scholes_price(100, 100, 1.0, 0.05, 0.2, "call") == pytest.approx(10.4506, rel=1e-4)


def test_known_put_price():
    assert black_scholes_price(100, 100, 1.0, 0.05, 0.2, "put") == pytest.approx(5.5735, rel=1e-4)


def test_put_call_parity():
    call = black_scholes_price(100, 100, 1.0, 0.05, 0.2, "call")
    put = black_scholes_price(100, 100, 1.0, 0.05, 0.2, "put")
    assert call - put == pytest.approx(100 - 100 * np.exp(-0.05), rel=1e-6)


def test_expiry_intrinsic_value():
    assert black_scholes_price(110, 100, 0.0, 0.05, 0.2, "call") == 10.0


def test_invalid_option_type_fails():
    with pytest.raises(PricingError):
        black_scholes_price(100, 100, 1.0, 0.05, 0.2, "calls")


def test_nonfinite_pricing_parameter_fails():
    with pytest.raises(PricingError, match="risk_free_rate"):
        black_scholes_price(100, 100, 1.0, np.nan, 0.2, "call")


def test_vectorized_input_returns_expected_shape():
    prices = black_scholes_price(np.array([95, 100, 105]), 100, np.array([1, 1, 1]), 0.05, 0.2, "call")
    assert prices.shape == (3,)


def test_scalar_spot_with_vector_time_returns_vector():
    prices = black_scholes_price(100, 100, np.array([0.25, 0.5, 1.0]), 0.05, 0.2, "call")
    assert prices.shape == (3,)
