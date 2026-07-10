from __future__ import annotations

import numpy as np

from pyrisklab.greeks import calculate_greeks


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
