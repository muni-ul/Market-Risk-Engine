from __future__ import annotations

import math
from numbers import Real

import numpy as np
import pandas as pd

from pyrisklab.exceptions import RiskError
from pyrisklab.models import RiskCheckResult, RiskConfig, RiskEvent

RISK_EVENT_COLUMNS = [
    "step",
    "event_type",
    "severity",
    "symbol",
    "proposed_side",
    "proposed_quantity",
    "proposed_notional",
    "portfolio_value",
    "limit_name",
    "limit_value",
    "observed_value",
    "reason",
]


class RiskManager:
    def __init__(self, config: RiskConfig, contract_multiplier: int = 100) -> None:
        self.config = config
        self.contract_multiplier = _as_positive_integer(
            contract_multiplier,
            "contract_multiplier",
        )
        self.trading_stopped = False
        self.events: list[RiskEvent] = []

    def validate_order(
        self,
        order_row,
        current_position_quantity: int,
        portfolio_value: float,
        drawdown_pct: float = 0.0,
        available_cash: float | None = None,
        estimated_commission: float = 0.0,
    ) -> RiskCheckResult:
        quantity = _as_contract_quantity(order_row.quantity)
        price = _as_nonnegative_price(order_row.requested_price, "order requested_price")
        current_position_quantity = _as_integer(
            current_position_quantity,
            "current_position_quantity",
        )
        portfolio_value = _as_nonnegative_price(portfolio_value, "portfolio_value")
        drawdown_pct = _as_nonnegative_price(drawdown_pct, "drawdown_pct")
        estimated_commission = _as_nonnegative_price(
            estimated_commission,
            "estimated_commission",
        )
        if available_cash is not None:
            available_cash = _as_nonnegative_price(available_cash, "available_cash")
        side = str(order_row.side).upper()
        if quantity <= 0:
            raise RiskError("risk validation received an invalid order quantity or price.")

        proposed_notional = price * quantity * self.contract_multiplier
        if self.trading_stopped:
            return self._block(
                order_row,
                proposed_notional,
                portfolio_value,
                "trading_stopped",
                1.0,
                1.0,
                "Trading has stopped after a prior risk breach.",
            )

        if side == "BUY":
            resulting_quantity = current_position_quantity + quantity
        elif side == "SELL":
            resulting_quantity = current_position_quantity - quantity
            if resulting_quantity < 0:
                return self._block(
                    order_row,
                    proposed_notional,
                    portfolio_value,
                    "short_position",
                    0.0,
                    abs(resulting_quantity),
                    f"Blocked SELL {quantity} {order_row.symbol} "
                    f"at step {order_row.step}: short selling is disabled.",
                )
        else:
            raise RiskError(f"order side must be BUY or SELL. Received {side!r}.")

        if abs(resulting_quantity) > self.config.max_position_quantity:
            return self._block(
                order_row,
                proposed_notional,
                portfolio_value,
                "max_position_quantity",
                self.config.max_position_quantity,
                abs(resulting_quantity),
                f"Blocked {side} {quantity} {order_row.symbol} "
                f"at step {order_row.step}: resulting quantity {resulting_quantity} "
                f"exceeds max_position_quantity {self.config.max_position_quantity}.",
            )
        if proposed_notional > self.config.max_trade_notional:
            return self._block(
                order_row,
                proposed_notional,
                portfolio_value,
                "max_trade_notional",
                self.config.max_trade_notional,
                proposed_notional,
                f"Blocked {side} {quantity} {order_row.symbol} "
                f"at step {order_row.step}: trade notional {proposed_notional:.2f} "
                f"exceeds max_trade_notional {self.config.max_trade_notional:.2f}.",
            )
        cash_required = proposed_notional + estimated_commission
        if side == "BUY" and available_cash is not None and cash_required > available_cash:
            return self._block(
                order_row,
                proposed_notional,
                portfolio_value,
                "available_cash",
                available_cash,
                cash_required,
                f"Blocked BUY {quantity} {order_row.symbol} "
                f"at step {order_row.step}: required cash {cash_required:.2f} "
                f"exceeds available cash {available_cash:.2f}.",
            )
        if self.config.stop_trading_on_breach and drawdown_pct >= self.config.max_drawdown_pct:
            self.trading_stopped = True
            return self._block(
                order_row,
                proposed_notional,
                portfolio_value,
                "max_drawdown_pct",
                self.config.max_drawdown_pct,
                drawdown_pct,
                f"Trading stopped because drawdown_pct {drawdown_pct:.4f} "
                f"exceeded max_drawdown_pct {self.config.max_drawdown_pct:.4f}.",
            )
        loss_pct = max(
            0.0,
            (self.config.starting_cash - portfolio_value) / self.config.starting_cash,
        )
        if self.config.stop_trading_on_breach and loss_pct >= self.config.max_loss_pct:
            self.trading_stopped = True
            return self._block(
                order_row,
                proposed_notional,
                portfolio_value,
                "max_loss_pct",
                self.config.max_loss_pct,
                loss_pct,
                f"Trading stopped because loss_pct {loss_pct:.4f} "
                f"exceeded max_loss_pct {self.config.max_loss_pct:.4f}.",
            )
        return RiskCheckResult(True, [])

    def _block(
        self,
        order_row,
        proposed_notional: float,
        portfolio_value: float,
        limit_name: str,
        limit_value: float,
        observed_value: float,
        reason: str,
    ) -> RiskCheckResult:
        quantity = _as_contract_quantity(order_row.quantity)
        event = RiskEvent(
            step=int(order_row.step),
            event_type="ORDER_BLOCKED",
            severity="WARNING",
            symbol=str(order_row.symbol),
            proposed_side=str(order_row.side).upper(),
            proposed_quantity=quantity,
            proposed_notional=proposed_notional,
            portfolio_value=portfolio_value,
            limit_name=limit_name,
            limit_value=limit_value,
            observed_value=observed_value,
            reason=reason,
        )
        self.events.append(event)
        return RiskCheckResult(False, [event])


def risk_events_frame(events: list[RiskEvent]) -> pd.DataFrame:
    return pd.DataFrame([event.__dict__ for event in events], columns=RISK_EVENT_COLUMNS)


def _as_contract_quantity(value) -> int:
    return _as_positive_integer(value, "order quantity")


def _as_positive_integer(value, field_name: str) -> int:
    parsed = _as_integer(value, field_name)
    if parsed <= 0:
        raise RiskError(f"{field_name} must be > 0. Received {parsed}.")
    return parsed


def _as_integer(value, field_name: str) -> int:
    if isinstance(value, bool):
        raise RiskError(f"{field_name} must be an integer. Received {value!r}.")
    if isinstance(value, Real):
        numeric = float(value)
        if not math.isfinite(numeric):
            raise RiskError(f"{field_name} must be a finite integer. Received {value!r}.")
        if not numeric.is_integer():
            raise RiskError(f"{field_name} must be an integer. Received {value!r}.")
    try:
        parsed = int(value)
    except (OverflowError, TypeError, ValueError) as exc:
        raise RiskError(f"{field_name} must be an integer. Received {value!r}.") from exc
    return parsed


def _as_nonnegative_price(value, field_name: str) -> float:
    if isinstance(value, bool):
        raise RiskError(f"{field_name} must be numeric. Received {value!r}.")
    try:
        price = float(value)
    except (TypeError, ValueError) as exc:
        raise RiskError(f"{field_name} must be numeric. Received {value!r}.") from exc
    if not np.isfinite(price) or price < 0:
        raise RiskError(f"{field_name} must be finite and >= 0. Received {value!r}.")
    return price
