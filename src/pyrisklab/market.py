from __future__ import annotations

import math
from numbers import Real

import numpy as np
import pandas as pd

from pyrisklab.exceptions import MarketSimulationError
from pyrisklab.models import MarketConfig


def simulate_gbm_path(config: MarketConfig, seed: int) -> pd.DataFrame:
    initial_price = _as_finite_float(config.initial_price, "market.initial_price")
    drift = _as_finite_float(config.drift, "market.drift")
    volatility = _as_finite_float(config.volatility, "market.volatility")
    trading_days = _as_positive_integer(config.trading_days, "market.trading_days")
    steps = _as_positive_integer(config.steps, "market.steps")
    paths = _as_positive_integer(config.paths, "market.paths")
    if initial_price <= 0:
        raise MarketSimulationError(f"market.initial_price must be > 0. Received {initial_price}.")
    if volatility < 0:
        raise MarketSimulationError(f"market.volatility must be >= 0. Received {volatility}.")

    dt = 1.0 / trading_days
    rng = np.random.default_rng(seed)
    shocks = rng.standard_normal((steps, paths))
    increments = (drift - 0.5 * volatility**2) * dt
    increments += volatility * np.sqrt(dt) * shocks
    prices = np.vstack(
        [
            np.full(paths, initial_price),
            initial_price * np.exp(np.cumsum(increments, axis=0)),
        ]
    )

    rows = []
    for path_id in range(paths):
        for step in range(steps + 1):
            row = {
                "step": step,
                "time_years": step / trading_days,
                "underlying_price": float(prices[step, path_id]),
            }
            if paths > 1:
                row["path_id"] = path_id
            rows.append(row)
    df = pd.DataFrame(rows)
    if not np.isfinite(df["underlying_price"]).all() or (df["underlying_price"] <= 0).any():
        raise MarketSimulationError("market simulation produced non-finite or nonpositive prices.")
    return df


def _as_finite_float(value, field_name: str) -> float:
    if isinstance(value, bool):
        raise MarketSimulationError(f"{field_name} must be numeric. Received {value!r}.")
    try:
        parsed = float(value)
    except (TypeError, ValueError) as exc:
        raise MarketSimulationError(f"{field_name} must be numeric. Received {value!r}.") from exc
    if not math.isfinite(parsed):
        raise MarketSimulationError(f"{field_name} must be finite. Received {value!r}.")
    return parsed


def _as_positive_integer(value, field_name: str) -> int:
    if isinstance(value, bool):
        raise MarketSimulationError(f"{field_name} must be an integer. Received {value!r}.")
    if isinstance(value, Real):
        numeric = float(value)
        if not math.isfinite(numeric):
            raise MarketSimulationError(
                f"{field_name} must be a finite integer. Received {value!r}."
            )
        if not numeric.is_integer():
            raise MarketSimulationError(f"{field_name} must be an integer. Received {value!r}.")
    try:
        parsed = int(value)
    except (OverflowError, TypeError, ValueError) as exc:
        raise MarketSimulationError(
            f"{field_name} must be an integer. Received {value!r}."
        ) from exc
    if parsed <= 0:
        raise MarketSimulationError(f"{field_name} must be > 0. Received {parsed}.")
    return parsed
