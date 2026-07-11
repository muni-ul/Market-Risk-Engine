from __future__ import annotations

import math
from numbers import Real

import pandas as pd

from pyrisklab.exceptions import PortfolioError
from pyrisklab.models import PortfolioSnapshot, Position


class Portfolio:
    def __init__(self, starting_cash: float, contract_multiplier: int = 100, allow_short: bool = False) -> None:
        starting_cash = _as_finite_float(starting_cash, "starting_cash")
        contract_multiplier = _as_positive_integer(contract_multiplier, "contract_multiplier")
        if starting_cash <= 0:
            raise PortfolioError(f"starting_cash must be greater than 0. Received {starting_cash}.")
        self.starting_cash = starting_cash
        self.cash = starting_cash
        self.contract_multiplier = contract_multiplier
        self.allow_short = allow_short
        self.positions: dict[str, Position] = {}
        self.realized_pnl = 0.0
        self.peak_value = float(starting_cash)
        self.snapshots: list[PortfolioSnapshot] = []

    def current_quantity(self, symbol: str) -> int:
        return self.positions.get(symbol, Position(symbol)).quantity

    def apply_trade(self, trade_row) -> None:
        quantity = _as_positive_integer(trade_row.quantity, "trade quantity")
        fill_price = _as_finite_float(trade_row.fill_price, "fill_price")
        commission = _as_finite_float(getattr(trade_row, "commission", 0.0), "commission")
        symbol = str(trade_row.symbol)
        side = str(trade_row.side).upper()
        if fill_price < 0:
            raise PortfolioError(f"cannot apply trade with negative fill_price. Received {fill_price}.")
        if commission < 0:
            raise PortfolioError(f"cannot apply trade with negative commission. Received {commission}.")

        position = self.positions.setdefault(symbol, Position(symbol))
        notional = fill_price * quantity * self.contract_multiplier
        if side == "BUY":
            total_cost = notional + commission
            if total_cost > self.cash:
                raise PortfolioError(f"insufficient cash for BUY order. Required {total_cost:.2f}, available {self.cash:.2f}.")
            old_qty = position.quantity
            new_qty = old_qty + quantity
            position.average_cost = ((old_qty * position.average_cost) + (quantity * fill_price)) / new_qty
            position.quantity = new_qty
            self.cash -= total_cost
        elif side == "SELL":
            if not self.allow_short and quantity > position.quantity:
                raise PortfolioError(f"cannot sell {quantity} {symbol} contracts when current position is {position.quantity}.")
            self.cash += notional - commission
            self.realized_pnl += (fill_price - position.average_cost) * quantity * self.contract_multiplier - commission
            position.quantity -= quantity
            if position.quantity == 0:
                position.average_cost = 0.0
        else:
            raise PortfolioError(f"trade side must be BUY or SELL. Received {side!r}.")

    def mark_to_market(self, step: int, symbol: str, market_price: float) -> PortfolioSnapshot:
        market_price = _as_finite_float(market_price, "market_price")
        if market_price < 0:
            raise PortfolioError(f"market_price must be >= 0. Received {market_price}.")
        position = self.positions.get(symbol, Position(symbol))
        positions_value = position.quantity * market_price * self.contract_multiplier
        unrealized = (market_price - position.average_cost) * position.quantity * self.contract_multiplier
        total_value = self.cash + positions_value
        self.peak_value = max(self.peak_value, total_value)
        drawdown = self.peak_value - total_value
        drawdown_pct = drawdown / self.peak_value if self.peak_value > 0 else 0.0
        snapshot = PortfolioSnapshot(
            step=step,
            cash=self.cash,
            symbol=symbol,
            position_quantity=position.quantity,
            average_cost=position.average_cost,
            market_price=market_price,
            positions_value=positions_value,
            realized_pnl=self.realized_pnl,
            unrealized_pnl=unrealized,
            total_value=total_value,
            peak_value=self.peak_value,
            drawdown=drawdown,
            drawdown_pct=drawdown_pct,
        )
        self.snapshots.append(snapshot)
        return snapshot


def build_portfolio_history(trades: pd.DataFrame, pricing_history: pd.DataFrame, starting_cash: float, contract_multiplier: int = 100) -> pd.DataFrame:
    trades = _require_dataframe(trades, "trades")
    pricing_history = _require_dataframe(pricing_history, "pricing_history")
    required = {"step", "symbol", "option_price"}
    missing = required - set(pricing_history.columns)
    if missing:
        raise PortfolioError(f"pricing_history is missing required columns: {', '.join(sorted(missing))}.")
    portfolio = Portfolio(starting_cash, contract_multiplier)
    trades_by_step = {}
    if not trades.empty:
        for trade in trades.sort_values(["step"]).itertuples(index=False):
            trades_by_step.setdefault(int(trade.step), []).append(trade)
    for price in pricing_history.sort_values(["step"]).itertuples(index=False):
        for trade in trades_by_step.get(int(price.step), []):
            portfolio.apply_trade(trade)
        market_price = _as_finite_float(price.option_price, "pricing_history.option_price")
        portfolio.mark_to_market(int(price.step), str(price.symbol), market_price)
    return pd.DataFrame([snapshot.__dict__ for snapshot in portfolio.snapshots])


def _as_finite_float(value, field_name: str) -> float:
    if isinstance(value, bool):
        raise PortfolioError(f"{field_name} must be numeric. Received {value!r}.")
    try:
        parsed = float(value)
    except (TypeError, ValueError) as exc:
        raise PortfolioError(f"{field_name} must be numeric. Received {value!r}.") from exc
    if not math.isfinite(parsed):
        raise PortfolioError(f"{field_name} must be finite. Received {value!r}.")
    return parsed


def _require_dataframe(value, name: str) -> pd.DataFrame:
    if not isinstance(value, pd.DataFrame):
        raise PortfolioError(
            f"{name} must be a pandas DataFrame. Received {type(value).__name__}."
        )
    return value


def _as_positive_integer(value, field_name: str) -> int:
    if isinstance(value, bool):
        raise PortfolioError(f"{field_name} must be an integer. Received {value!r}.")
    if isinstance(value, Real):
        numeric = float(value)
        if not math.isfinite(numeric):
            raise PortfolioError(f"{field_name} must be a finite integer. Received {value!r}.")
        if not numeric.is_integer():
            raise PortfolioError(f"{field_name} must be an integer. Received {value!r}.")
    try:
        parsed = int(value)
    except (OverflowError, TypeError, ValueError) as exc:
        raise PortfolioError(f"{field_name} must be an integer. Received {value!r}.") from exc
    if parsed <= 0:
        raise PortfolioError(f"{field_name} must be greater than 0. Received {parsed}.")
    return parsed
