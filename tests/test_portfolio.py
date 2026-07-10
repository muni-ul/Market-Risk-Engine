from __future__ import annotations

import pandas as pd
import pytest

from pyrisklab.exceptions import PortfolioError
from pyrisklab.portfolio import Portfolio, build_portfolio_history


def trade(side="BUY", quantity=1, price=5.0, commission=0.0):
    return type(
        "TradeRow",
        (),
        {"symbol": "CALL_105", "side": side, "quantity": quantity, "fill_price": price, "commission": commission},
    )()


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
    assert portfolio.realized_pnl == 200


def test_cannot_sell_more_than_held():
    with pytest.raises(PortfolioError):
        Portfolio(10000).apply_trade(trade("SELL", 1, 7.0))


def test_invalid_contract_multiplier_fails():
    with pytest.raises(PortfolioError, match="contract_multiplier"):
        Portfolio(10000, contract_multiplier=0)


def test_fractional_contract_multiplier_fails():
    with pytest.raises(PortfolioError, match="contract_multiplier"):
        Portfolio(10000, contract_multiplier=100.5)


def test_nonfinite_starting_cash_fails():
    with pytest.raises(PortfolioError, match="starting_cash"):
        Portfolio(float("inf"))


def test_fractional_trade_quantity_fails():
    with pytest.raises(PortfolioError, match="trade quantity"):
        Portfolio(10000).apply_trade(trade("BUY", quantity=1.5))


def test_negative_commission_fails():
    with pytest.raises(PortfolioError, match="negative commission"):
        Portfolio(10000).apply_trade(trade("BUY", 1, 5.0, commission=-1.0))


def test_nonfinite_fill_price_fails():
    with pytest.raises(PortfolioError, match="fill_price"):
        Portfolio(10000).apply_trade(trade("BUY", 1, float("nan")))


def test_portfolio_total_value_updates_correctly():
    portfolio = Portfolio(10000)
    portfolio.apply_trade(trade("BUY", 1, 5.0))
    snapshot = portfolio.mark_to_market(1, "CALL_105", 6.0)
    assert snapshot.total_value == 10100


def test_nonfinite_market_price_fails():
    with pytest.raises(PortfolioError, match="market_price"):
        Portfolio(10000).mark_to_market(1, "CALL_105", float("inf"))


def test_drawdown_updates_correctly():
    pricing = pd.DataFrame({"step": [0, 1], "symbol": ["CALL_105", "CALL_105"], "option_price": [5.0, 4.0]})
    trades = pd.DataFrame({"step": [0], "symbol": ["CALL_105"], "side": ["BUY"], "quantity": [1], "fill_price": [5.0], "commission": [0.0]})
    history = build_portfolio_history(trades, pricing, 10000)
    assert history["drawdown"].iloc[-1] == 100
