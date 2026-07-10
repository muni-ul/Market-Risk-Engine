from __future__ import annotations

import time
from collections.abc import Callable

import numpy as np
import pandas as pd

from pyrisklab.exceptions import BenchmarkError
from pyrisklab.models import BenchmarkConfig
from pyrisklab.pricing import black_scholes_price


def generate_benchmark_inputs(num_prices: int, seed: int) -> dict[str, np.ndarray]:
    if num_prices <= 0:
        raise BenchmarkError(f"num_prices must be > 0. Received {num_prices}.")
    rng = np.random.default_rng(seed)
    return {
        "spot": rng.uniform(50.0, 150.0, num_prices),
        "time_to_expiry": rng.uniform(1 / 252, 1.0, num_prices),
    }


def price_loop(inputs: dict[str, np.ndarray]) -> np.ndarray:
    return np.array(
        [
            black_scholes_price(spot, 105.0, time_to_expiry, 0.04, 0.20, "call")
            for spot, time_to_expiry in zip(inputs["spot"], inputs["time_to_expiry"], strict=True)
        ]
    )


def price_vectorized(inputs: dict[str, np.ndarray]) -> np.ndarray:
    return np.asarray(black_scholes_price(inputs["spot"], 105.0, inputs["time_to_expiry"], 0.04, 0.20, "call"))


def run_pricing_benchmark(config: BenchmarkConfig) -> pd.DataFrame:
    if not config.enabled:
        return pd.DataFrame(columns=["method", "num_prices", "runtime_seconds", "speedup_vs_loop", "max_abs_error_vs_loop", "passed_equivalence_check"])
    inputs = generate_benchmark_inputs(config.num_prices, config.seed)
    loop_prices, loop_runtime = _time(price_loop, inputs)
    vector_prices, vector_runtime = _time(price_vectorized, inputs)
    if not np.isfinite(loop_prices).all() or not np.isfinite(vector_prices).all():
        raise BenchmarkError("benchmark pricing produced non-finite values.")
    max_abs_error = float(np.max(np.abs(loop_prices - vector_prices)))
    if max_abs_error > config.tolerance:
        raise BenchmarkError("loop and vectorized pricing results differed beyond tolerance.")
    vector_speedup = loop_runtime / vector_runtime if vector_runtime > 0 else float("inf")
    return pd.DataFrame(
        [
            {
                "method": "python_loop",
                "num_prices": config.num_prices,
                "runtime_seconds": loop_runtime,
                "speedup_vs_loop": 1.0,
                "max_abs_error_vs_loop": 0.0,
                "passed_equivalence_check": True,
            },
            {
                "method": "numpy_vectorized",
                "num_prices": config.num_prices,
                "runtime_seconds": vector_runtime,
                "speedup_vs_loop": vector_speedup,
                "max_abs_error_vs_loop": max_abs_error,
                "passed_equivalence_check": True,
            },
        ]
    )


def _time(fn: Callable[[dict[str, np.ndarray]], np.ndarray], inputs: dict[str, np.ndarray]) -> tuple[np.ndarray, float]:
    start = time.perf_counter()
    result = fn(inputs)
    return result, time.perf_counter() - start
