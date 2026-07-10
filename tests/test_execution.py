from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from pyrisklab.exceptions import ExecutionError
from pyrisklab.execution import create_orders_from_signals, execute_orders


def pricing():
    return pd.DataFrame({"step": [1], "symbol": ["CALL_105"], "option_price": [5.0]})


def signal(action="BUY", quantity=1):
    return pd.DataFrame({"step": [1], "symbol": ["CALL_105"], "action": [action], "quantity": [quantity], "reason": ["test"]})


def test_valid_order_creates_trade():
    orders = create_orders_from_signals(signal(), pricing())
    trades = execute_orders(orders)
    assert trades["notional"].iloc[0] == 500.0


def test_zero_quantity_order_fails():
    with pytest.raises(ExecutionError):
        create_orders_from_signals(signal("BUY", 0), pricing())


def test_negative_quantity_order_fails():
    with pytest.raises(ExecutionError):
        create_orders_from_signals(signal("BUY", -1), pricing())


def test_fractional_signal_quantity_fails():
    with pytest.raises(ExecutionError, match="integer"):
        create_orders_from_signals(signal("BUY", 1.5), pricing())


def test_fractional_order_quantity_fails():
    orders = create_orders_from_signals(signal("BUY", 1), pricing())
    orders.loc[0, "quantity"] = 1.5
    with pytest.raises(ExecutionError, match="integer"):
        execute_orders(orders)


def test_order_side_is_normalized_before_execution():
    orders = create_orders_from_signals(signal("BUY", 1), pricing())
    orders.loc[0, "side"] = "buy"
    trades = execute_orders(orders)
    assert trades["side"].iloc[0] == "BUY"


def test_nonfinite_order_quantity_fails():
    orders = create_orders_from_signals(signal("BUY", 1), pricing())
    orders.loc[0, "quantity"] = float("inf")
    with pytest.raises(ExecutionError, match="integer"):
        execute_orders(orders)


def test_numpy_fractional_order_quantity_fails():
    orders = create_orders_from_signals(signal("BUY", 1), pricing())
    orders.loc[0, "quantity"] = np.float64(1.5)
    with pytest.raises(ExecutionError, match="integer"):
        execute_orders(orders)


def test_nonfinite_commission_fails():
    orders = create_orders_from_signals(signal("BUY", 1), pricing())
    with pytest.raises(ExecutionError, match="commission_per_contract"):
        execute_orders(orders, commission_per_contract=np.nan)


def test_nonnumeric_requested_price_fails_cleanly():
    orders = create_orders_from_signals(signal("BUY", 1), pricing())
    orders.loc[0, "requested_price"] = "bad-price"
    with pytest.raises(ExecutionError, match="requested_price"):
        execute_orders(orders)


def test_nonnumeric_pricing_history_price_fails_cleanly():
    bad_pricing = pricing()
    bad_pricing.loc[0, "option_price"] = "bad-price"
    with pytest.raises(ExecutionError, match="option_price"):
        create_orders_from_signals(signal("BUY", 1), bad_pricing)


def test_fractional_contract_multiplier_fails():
    orders = create_orders_from_signals(signal("BUY", 1), pricing())
    with pytest.raises(ExecutionError, match="contract_multiplier"):
        execute_orders(orders, contract_multiplier=100.5)
