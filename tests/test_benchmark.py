from __future__ import annotations

import numpy as np
import pytest

from pyrisklab.benchmark import (
    BENCHMARK_COLUMNS,
    generate_benchmark_inputs,
    price_loop,
    run_pricing_benchmark,
)
from pyrisklab.exceptions import BenchmarkError
from pyrisklab.models import BenchmarkConfig, BenchmarkResult


def test_benchmark_returns_loop_and_vectorized_rows():
    df = run_pricing_benchmark(BenchmarkConfig(True, 1000, 42))
    assert set(df["method"]) == {"python_loop", "numpy_vectorized"}
    assert list(df.columns) == BENCHMARK_COLUMNS
    assert set(df["option_type"]) == {"call"}
    assert set(df["strike"]) == {105.0}
    assert set(df["risk_free_rate"]) == {0.04}
    assert set(df["volatility"]) == {0.20}


def test_benchmark_result_model_matches_csv_contract():
    assert list(BenchmarkResult.__dataclass_fields__) == BENCHMARK_COLUMNS


def test_disabled_benchmark_keeps_output_headers():
    df = run_pricing_benchmark(BenchmarkConfig(False, 1000, 42))
    assert df.empty
    assert list(df.columns) == BENCHMARK_COLUMNS


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


def test_mismatched_benchmark_outputs_raise_project_error(monkeypatch):
    def short_vectorized(_inputs):
        return np.array([1.0])

    monkeypatch.setattr("pyrisklab.benchmark.price_vectorized", short_vectorized)

    with pytest.raises(BenchmarkError, match="matching shapes"):
        run_pricing_benchmark(BenchmarkConfig(True, 3, 42))


def test_nonfinite_benchmark_outputs_raise_project_error(monkeypatch):
    def nan_vectorized(inputs):
        return np.full_like(inputs["spot"], np.nan, dtype=float)

    monkeypatch.setattr("pyrisklab.benchmark.price_vectorized", nan_vectorized)

    with pytest.raises(BenchmarkError, match="non-finite"):
        run_pricing_benchmark(BenchmarkConfig(True, 3, 42))


def test_nonnumeric_benchmark_outputs_raise_project_error(monkeypatch):
    def bad_vectorized(inputs):
        return ["bad-price"] * len(inputs["spot"])

    monkeypatch.setattr("pyrisklab.benchmark.price_vectorized", bad_vectorized)

    with pytest.raises(BenchmarkError, match="numeric"):
        run_pricing_benchmark(BenchmarkConfig(True, 3, 42))
