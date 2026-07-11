from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from pyrisklab.exceptions import StrategyError
from pyrisklab.models import StrategyConfig
from pyrisklab.strategy import generate_signals


def frames(delta: float):
    pricing = pd.DataFrame({"step": [1], "symbol": ["CALL_105"], "option_price": [5.0], "underlying_price": [100.0], "time_to_expiry": [0.2]})
    greeks = pd.DataFrame({"step": [1], "symbol": ["CALL_105"], "delta": [delta], "gamma": [0.1], "vega": [0.2]})
    return pricing, greeks


def test_low_delta_can_generate_buy_signal(strategy_config):
    pricing, greeks = frames(0.4)
    assert generate_signals(pricing, greeks, strategy_config)["action"].iloc[0] == "BUY"


def test_high_delta_can_generate_sell_signal(strategy_config):
    pricing, greeks = frames(0.8)
    assert generate_signals(pricing, greeks, strategy_config)["action"].iloc[0] == "SELL"


def test_otherwise_hold(strategy_config):
    pricing, greeks = frames(0.5)
    assert generate_signals(pricing, greeks, strategy_config)["action"].iloc[0] == "HOLD"


def test_nonfinite_delta_holds_with_reason(strategy_config):
    pricing, greeks = frames(np.nan)
    signals = generate_signals(pricing, greeks, strategy_config)
    assert signals["action"].iloc[0] == "HOLD"
    assert "not finite" in signals["reason"].iloc[0]


def test_nonfinite_option_price_fails(strategy_config):
    pricing, greeks = frames(0.5)
    pricing.loc[0, "option_price"] = np.nan
    with pytest.raises(StrategyError, match="option_price"):
        generate_signals(pricing, greeks, strategy_config)


def test_non_dataframe_pricing_history_fails_cleanly(strategy_config):
    _pricing, greeks = frames(0.5)
    with pytest.raises(StrategyError, match="pricing_history"):
        generate_signals([{"step": 1}], greeks, strategy_config)


def test_non_dataframe_greeks_history_fails_cleanly(strategy_config):
    pricing, _greeks = frames(0.5)
    with pytest.raises(StrategyError, match="greeks_history"):
        generate_signals(pricing, [{"delta": 0.5}], strategy_config)


def test_invalid_strategy_thresholds_fail_defensively():
    pricing, greeks = frames(0.5)
    config = StrategyConfig("simple_delta_rule", 0.8, 0.7, 1, 0)
    with pytest.raises(StrategyError, match="buy_delta_below"):
        generate_signals(pricing, greeks, config)


def test_nonnumeric_strategy_threshold_fails_defensively():
    pricing, greeks = frames(0.5)
    config = StrategyConfig("simple_delta_rule", "low", 0.7, 1, 0)
    with pytest.raises(StrategyError, match="buy_delta_below"):
        generate_signals(pricing, greeks, config)


def test_invalid_strategy_quantity_fails_defensively():
    pricing, greeks = frames(0.5)
    config = StrategyConfig("simple_delta_rule", 0.45, 0.7, 0, 0)
    with pytest.raises(StrategyError, match="trade_quantity"):
        generate_signals(pricing, greeks, config)


def test_fractional_strategy_quantity_fails_defensively():
    pricing, greeks = frames(0.5)
    config = StrategyConfig("simple_delta_rule", 0.45, 0.7, 1.5, 0)
    with pytest.raises(StrategyError, match="trade_quantity"):
        generate_signals(pricing, greeks, config)
