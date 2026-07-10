from __future__ import annotations

import numpy as np
import pytest

from pyrisklab.benchmark import generate_benchmark_inputs, price_loop, run_pricing_benchmark
from pyrisklab.exceptions import BenchmarkError
from pyrisklab.models import BenchmarkConfig


def test_benchmark_returns_loop_and_vectorized_rows():
    df = run_pricing_benchmark(BenchmarkConfig(True, 1000, 42))
    assert set(df["method"]) == {"python_loop", "numpy_vectorized"}


def test_benchmark_saves_a_csv(tmp_path):
    path = tmp_path / "benchmark.csv"
    run_pricing_benchmark(BenchmarkConfig(True, 100, 42)).to_csv(path, index=False)
    assert path.exists()


def test_speedup_calculation_handles_tiny_runtimes_safely():
    df = run_pricing_benchmark(BenchmarkConfig(True, 1, 42))
    assert "speedup_vs_loop" in df.columns


def test_inputs_are_deterministic():
    a = generate_benchmark_inputs(5, 42)
    b = generate_benchmark_inputs(5, 42)
    assert (a["spot"] == b["spot"]).all()


def test_mismatched_benchmark_inputs_raise_project_error():
    with pytest.raises(BenchmarkError, match="same length"):
        price_loop({"spot": np.array([100.0, 101.0]), "time_to_expiry": np.array([0.5])})


def test_nonfinite_benchmark_inputs_raise_project_error():
    with pytest.raises(BenchmarkError, match="finite"):
        price_loop({"spot": np.array([100.0, np.nan]), "time_to_expiry": np.array([0.5, 0.5])})
