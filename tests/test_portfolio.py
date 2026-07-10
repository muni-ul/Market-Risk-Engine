from __future__ import annotations

import pandas as pd
import pytest

from pyrisklab.exceptions import PortfolioError
from pyrisklab.portfolio import Portfolio, build_portfolio_history


def trade(side="BUY", quantity=1, price=5.0):
    return type("TradeRow", (), {"symbol": "CALL_105", "side": side, "quantity": quantity, "fill_price": price, "commission": 0.0})()


def test_buy_decreases_cash_and_increases_position():
    portfolio = Portfolio(10000)
    portfolio.apply_trade(trade())
    assert portfolio.cash == 9500
    assert portfolio.current_quantity("CALL_105") == 1


def test_sell_increases_cash_and_decreases_position():
    portfolio = Portfolio(10000)
    portfolio.apply_trade(trade("BUY", 1, 5.0))
    portfolio.apply_trade(trade("SELL", 1, 7.0))
    assert portfolio.cash == 10200
    assert portfolio.current_quantity("CALL_105") == 0


def test_cannot_sell_more_than_held():
    with pytest.raises(PortfolioError):
        Portfolio(10000).apply_trade(trade("SELL", 1, 7.0))


def test_portfolio_total_value_updates_correctly():
    portfolio = Portfolio(10000)
    portfolio.apply_trade(trade("BUY", 1, 5.0))
    snapshot = portfolio.mark_to_market(1, "CALL_105", 6.0)
    assert snapshot.total_value == 10100


def test_drawdown_updates_correctly():
    pricing = pd.DataFrame({"step": [0, 1], "symbol": ["CALL_105", "CALL_105"], "option_price": [5.0, 4.0]})
    trades = pd.DataFrame({"step": [0], "symbol": ["CALL_105"], "side": ["BUY"], "quantity": [1], "fill_price": [5.0], "commission": [0.0]})
    history = build_portfolio_history(trades, pricing, 10000)
    assert history["drawdown"].iloc[-1] == 100
