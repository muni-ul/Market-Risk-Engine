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


def test_fractional_num_prices_fails_with_project_error():
    with pytest.raises(BenchmarkError, match="num_prices"):
        generate_benchmark_inputs(10.5, 42)


def test_boolean_num_prices_fails_with_project_error():
    with pytest.raises(BenchmarkError, match="num_prices"):
        generate_benchmark_inputs(True, 42)


def test_mismatched_benchmark_inputs_raise_project_error():
    with pytest.raises(BenchmarkError, match="same length"):
        price_loop({"spot": np.array([100.0, 101.0]), "time_to_expiry": np.array([0.5])})


def test_non_mapping_benchmark_inputs_raise_project_error():
    with pytest.raises(BenchmarkError, match="mapping"):
        price_loop([("spot", np.array([100.0])), ("time_to_expiry", np.array([0.5]))])


def test_nonnumeric_benchmark_inputs_raise_project_error():
    with pytest.raises(BenchmarkError, match="numeric arrays"):
        price_loop({"spot": np.array(["bad"]), "time_to_expiry": np.array([0.5])})


def test_empty_benchmark_inputs_raise_project_error():
    with pytest.raises(BenchmarkError, match="at least one price"):
        price_loop({"spot": np.array([]), "time_to_expiry": np.array([])})


def test_nonfinite_benchmark_inputs_raise_project_error():
    with pytest.raises(BenchmarkError, match="finite"):
        price_loop({"spot": np.array([100.0, np.nan]), "time_to_expiry": np.array([0.5, 0.5])})
