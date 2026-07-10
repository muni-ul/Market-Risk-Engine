from __future__ import annotations

import pandas as pd

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
