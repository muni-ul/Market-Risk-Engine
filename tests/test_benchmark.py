from __future__ import annotations

from pyrisklab.benchmark import generate_benchmark_inputs, run_pricing_benchmark
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
