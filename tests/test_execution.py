from __future__ import annotations

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
