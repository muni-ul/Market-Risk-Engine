from __future__ import annotations

import numpy as np
import pandas as pd

from pyrisklab.exceptions import StrategyError
from pyrisklab.models import StrategyConfig


def generate_signals(pricing_history: pd.DataFrame, greeks_history: pd.DataFrame, strategy_config: StrategyConfig) -> pd.DataFrame:
    _validate_inputs(pricing_history, greeks_history)
    merged = pricing_history.merge(
        greeks_history[["step", "symbol", "delta", "gamma", "vega"]],
        on=["step", "symbol"],
        how="inner",
        validate="one_to_one",
    )
    if len(merged) != len(pricing_history):
        raise StrategyError("pricing_history and greeks_history have mismatched step values.")

    rows = []
    last_action_step: int | None = None
    for row in merged.itertuples(index=False):
        delta = float(row.delta)
        if not np.isfinite(delta):
            action, quantity, reason = "HOLD", 0, "Delta is missing or not finite; holding."
        elif delta < strategy_config.buy_delta_below:
            action, quantity, reason = "BUY", strategy_config.trade_quantity, f"Delta {delta:.4f} is below buy threshold {strategy_config.buy_delta_below:.4f}."
        elif delta > strategy_config.sell_delta_above:
            action, quantity, reason = "SELL", strategy_config.trade_quantity, f"Delta {delta:.4f} is above sell threshold {strategy_config.sell_delta_above:.4f}."
        else:
            action, quantity, reason = "HOLD", 0, (
                f"Delta {delta:.4f} is between buy threshold {strategy_config.buy_delta_below:.4f} "
                f"and sell threshold {strategy_config.sell_delta_above:.4f}."
            )

        if action in {"BUY", "SELL"} and last_action_step is not None:
            elapsed = int(row.step) - last_action_step
            if elapsed < strategy_config.min_steps_between_trades:
                action, quantity = "HOLD", 0
                reason = (
                    f"Signal suppressed by cooldown: only {elapsed} steps since last actionable signal; "
                    f"minimum is {strategy_config.min_steps_between_trades}."
                )
        if action in {"BUY", "SELL"}:
            last_action_step = int(row.step)

        rows.append(
            {
                "step": int(row.step),
                "symbol": row.symbol,
                "action": action,
                "quantity": quantity,
                "reference_price": float(row.option_price),
                "underlying_price": float(row.underlying_price),
                "option_price": float(row.option_price),
                "delta": delta,
                "gamma": float(row.gamma),
                "vega": float(row.vega),
                "time_to_expiry": float(row.time_to_expiry),
                "strategy_name": strategy_config.name,
                "reason": reason,
            }
        )
    return pd.DataFrame(rows)


def _validate_inputs(pricing_history: pd.DataFrame, greeks_history: pd.DataFrame) -> None:
    if pricing_history.empty or greeks_history.empty:
        raise StrategyError("strategy input data cannot be empty.")
    pricing_required = {"step", "symbol", "option_price", "underlying_price", "time_to_expiry"}
    greeks_required = {"step", "symbol", "delta", "gamma", "vega"}
    missing_pricing = pricing_required - set(pricing_history.columns)
    missing_greeks = greeks_required - set(greeks_history.columns)
    if missing_pricing:
        raise StrategyError(f"pricing_history is missing required columns: {', '.join(sorted(missing_pricing))}.")
    if missing_greeks:
        raise StrategyError(f"greeks_history is missing required columns: {', '.join(sorted(missing_greeks))}.")
    _require_finite(pricing_history, ["option_price", "underlying_price", "time_to_expiry"], "pricing_history")
    _require_finite(greeks_history, ["gamma", "vega"], "greeks_history")


def _require_finite(df: pd.DataFrame, columns: list[str], name: str) -> None:
    for column in columns:
        values = pd.to_numeric(df[column], errors="coerce")
        if not np.isfinite(values).all():
            raise StrategyError(f"{name}.{column} must contain only finite numeric values.")
