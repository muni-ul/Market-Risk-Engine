from __future__ import annotations

import numpy as np
import pandas as pd

from pyrisklab.exceptions import MarketSimulationError
from pyrisklab.models import MarketConfig


def simulate_gbm_path(config: MarketConfig, seed: int) -> pd.DataFrame:
    if config.initial_price <= 0:
        raise MarketSimulationError(f"market.initial_price must be > 0. Received {config.initial_price}.")
    if config.volatility < 0:
        raise MarketSimulationError(f"market.volatility must be >= 0. Received {config.volatility}.")
    if config.trading_days <= 0:
        raise MarketSimulationError(f"market.trading_days must be > 0. Received {config.trading_days}.")
    if config.steps <= 0:
        raise MarketSimulationError(f"market.steps must be > 0. Received {config.steps}.")
    if config.paths < 1:
        raise MarketSimulationError(f"market.paths must be >= 1. Received {config.paths}.")
    dt = 1.0 / config.trading_days
    rng = np.random.default_rng(seed)
    shocks = rng.standard_normal((config.steps, config.paths))
    increments = (config.drift - 0.5 * config.volatility**2) * dt
    increments += config.volatility * np.sqrt(dt) * shocks
    prices = np.vstack([np.full(config.paths, config.initial_price), config.initial_price * np.exp(np.cumsum(increments, axis=0))])

    rows = []
    for path_id in range(config.paths):
        for step in range(config.steps + 1):
            row = {
                "step": step,
                "time_years": step / config.trading_days,
                "underlying_price": float(prices[step, path_id]),
            }
            if config.paths > 1:
                row["path_id"] = path_id
            rows.append(row)
    df = pd.DataFrame(rows)
    if not np.isfinite(df["underlying_price"]).all() or (df["underlying_price"] <= 0).any():
        raise MarketSimulationError("market simulation produced non-finite or nonpositive prices.")
    return df
