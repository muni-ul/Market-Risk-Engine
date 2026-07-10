from __future__ import annotations

from numbers import Real

import numpy as np
import pandas as pd

from pyrisklab.exceptions import ExecutionError

ORDER_COLUMNS = ["order_id", "step", "symbol", "side", "quantity", "order_type", "requested_price", "source_signal_reason"]
TRADE_COLUMNS = ["trade_id", "order_id", "step", "symbol", "side", "quantity", "fill_price", "commission", "contract_multiplier", "notional", "fill_model"]


def create_orders_from_signals(signals: pd.DataFrame, pricing_history: pd.DataFrame, default_order_type: str = "market") -> pd.DataFrame:
    _validate_signal_inputs(signals, pricing_history)
    price_lookup = _build_price_lookup(pricing_history)
    orders = []
    for row in signals.itertuples(index=False):
        action = str(row.action).upper()
        if action == "HOLD":
            continue
        if action not in {"BUY", "SELL"}:
            raise ExecutionError(f"signal at step {row.step} has action {row.action!r}. Expected one of: BUY, SELL, HOLD.")
        quantity = _as_contract_quantity(row.quantity, "actionable signal quantity")
        if quantity <= 0:
            raise ExecutionError(f"actionable signal quantity must be greater than 0. Received {quantity}.")
        key = (int(row.step), str(row.symbol))
        if key not in price_lookup:
            raise ExecutionError(f"cannot fill order at step {row.step} for {row.symbol} because pricing_history has no option_price.")
        price = price_lookup[key]
        orders.append(
            {
                "order_id": f"ORD-{len(orders) + 1:06d}",
                "step": int(row.step),
                "symbol": str(row.symbol),
                "side": action,
                "quantity": quantity,
                "order_type": default_order_type,
                "requested_price": price,
                "source_signal_reason": str(getattr(row, "reason", "")),
            }
        )
    return pd.DataFrame(orders, columns=ORDER_COLUMNS)


def execute_orders(orders: pd.DataFrame, commission_per_contract: float = 0.0, contract_multiplier: int = 100, fill_model: str = "deterministic_mid") -> pd.DataFrame:
    if fill_model != "deterministic_mid":
        raise ExecutionError(f"fill_model must be 'deterministic_mid'. Received {fill_model!r}.")
    if not np.isfinite(commission_per_contract) or commission_per_contract < 0:
        raise ExecutionError(f"commission_per_contract must be >= 0. Received {commission_per_contract}.")
    contract_multiplier = _as_contract_quantity(contract_multiplier, "contract_multiplier")
    if contract_multiplier <= 0:
        raise ExecutionError(f"contract_multiplier must be > 0. Received {contract_multiplier}.")
    if orders.empty:
        return pd.DataFrame(columns=TRADE_COLUMNS)
    missing = set(ORDER_COLUMNS) - set(orders.columns)
    if missing:
        raise ExecutionError(f"orders is missing required columns: {', '.join(sorted(missing))}.")

    trades = []
    for row in orders.itertuples(index=False):
        quantity = _as_contract_quantity(row.quantity, "order.quantity")
        price = float(row.requested_price)
        if quantity <= 0:
            raise ExecutionError(f"order.quantity must be greater than 0. Received {quantity}.")
        if row.side not in {"BUY", "SELL"}:
            raise ExecutionError(f"order.side must be BUY or SELL. Received {row.side!r}.")
        if not np.isfinite(price) or price < 0:
            raise ExecutionError(f"requested_price must be finite and >= 0. Received {price}.")
        notional = price * quantity * contract_multiplier
        trades.append(
            {
                "trade_id": f"TRD-{len(trades) + 1:06d}",
                "order_id": row.order_id,
                "step": int(row.step),
                "symbol": row.symbol,
                "side": row.side,
                "quantity": quantity,
                "fill_price": price,
                "commission": commission_per_contract * quantity,
                "contract_multiplier": contract_multiplier,
                "notional": notional,
                "fill_model": fill_model,
            }
        )
    return pd.DataFrame(trades, columns=TRADE_COLUMNS)


def _validate_signal_inputs(signals: pd.DataFrame, pricing_history: pd.DataFrame) -> None:
    if signals.empty:
        return
    signal_required = {"step", "symbol", "action", "quantity"}
    pricing_required = {"step", "symbol", "option_price"}
    missing_signals = signal_required - set(signals.columns)
    missing_pricing = pricing_required - set(pricing_history.columns)
    if missing_signals:
        raise ExecutionError(f"signals is missing required columns: {', '.join(sorted(missing_signals))}.")
    if missing_pricing:
        raise ExecutionError(f"pricing_history is missing required columns: {', '.join(sorted(missing_pricing))}.")


def _build_price_lookup(pricing_history: pd.DataFrame) -> dict[tuple[int, str], float]:
    if pricing_history.duplicated(["step", "symbol"]).any():
        raise ExecutionError("pricing_history has duplicate rows for the same step and symbol.")
    lookup = {}
    for row in pricing_history.itertuples(index=False):
        price = float(row.option_price)
        if not np.isfinite(price) or price < 0:
            raise ExecutionError(f"option_price must be finite and >= 0. Received {price}.")
        lookup[(int(row.step), str(row.symbol))] = price
    return lookup


def _as_contract_quantity(value, field: str) -> int:
    if isinstance(value, bool):
        raise ExecutionError(f"{field} must be an integer. Received {value!r}.")
    if isinstance(value, Real) and not float(value).is_integer():
        raise ExecutionError(f"{field} must be an integer. Received {value!r}.")
    try:
        quantity = int(value)
    except (TypeError, ValueError) as exc:
        raise ExecutionError(f"{field} must be an integer. Received {value!r}.") from exc
    return quantity
