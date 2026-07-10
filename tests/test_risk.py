from __future__ import annotations

import numpy as np
import pytest

from pyrisklab.exceptions import RiskError
from pyrisklab.risk import RiskManager


def order(quantity=1, price=5.0, side="BUY"):
    return type("OrderRow", (), {"step": 1, "symbol": "CALL_105", "side": side, "quantity": quantity, "requested_price": price})()


def test_position_limit_blocks_oversized_order(risk_config):
    result = RiskManager(risk_config).validate_order(order(quantity=2), 9, 10000)
    assert not result.allowed


def test_trade_notional_limit_blocks_expensive_order(risk_config):
    result = RiskManager(risk_config).validate_order(order(price=30), 0, 10000)
    assert not result.allowed


def test_max_drawdown_breach_stops_future_trades(risk_config):
    manager = RiskManager(risk_config)
    assert not manager.validate_order(order(), 0, 10000, drawdown_pct=0.15).allowed
    assert not manager.validate_order(order(), 0, 10000).allowed


def test_allowed_trade_passes(risk_config):
    assert RiskManager(risk_config).validate_order(order(), 0, 10000).allowed


def test_risk_event_includes_readable_reason(risk_config):
    result = RiskManager(risk_config).validate_order(order(price=30), 0, 10000)
    assert "trade notional" in result.events[0].reason


def test_available_cash_blocks_buy_order(risk_config):
    result = RiskManager(risk_config).validate_order(order(price=20), 0, 10000, available_cash=1000)
    assert not result.allowed
    assert "available cash" in result.events[0].reason


def test_available_cash_check_includes_estimated_commission(risk_config):
    result = RiskManager(risk_config).validate_order(
        order(price=9),
        0,
        10000,
        available_cash=905,
        estimated_commission=10,
    )
    assert not result.allowed
    assert result.events[0].observed_value == 910


def test_fractional_order_quantity_fails_defensively(risk_config):
    with pytest.raises(RiskError, match="integer"):
        RiskManager(risk_config).validate_order(order(quantity=1.5), 0, 10000)


def test_invalid_contract_multiplier_fails_defensively(risk_config):
    with pytest.raises(RiskError, match="contract_multiplier"):
        RiskManager(risk_config, contract_multiplier=0)


def test_fractional_contract_multiplier_fails_defensively(risk_config):
    with pytest.raises(RiskError, match="contract_multiplier"):
        RiskManager(risk_config, contract_multiplier=100.5)


def test_nonfinite_order_price_fails_defensively(risk_config):
    with pytest.raises(RiskError, match="invalid order"):
        RiskManager(risk_config).validate_order(order(price=np.nan), 0, 10000)
