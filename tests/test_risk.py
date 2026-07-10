from __future__ import annotations

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
