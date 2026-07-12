# PyRiskLab Performance Notes

PyRiskLab includes a small local benchmark to demonstrate performance-aware
engineering. It is designed to show why vectorized numerical code matters, not
to promise a universal speedup.

## Reviewer Signal

The important signal is the benchmark workflow, not a specific number:
PyRiskLab generates deterministic inputs, runs scalar and vectorized pricing
paths, verifies numerical equivalence, records assumptions, and writes the
result to a reproducible CSV artifact.

## What Is Compared

The benchmark compares two Black-Scholes pricing paths over the same
deterministic generated inputs:

- `python_loop`: repeatedly calls the scalar Black-Scholes pricing path.
- `numpy_vectorized`: evaluates the same pricing formula over NumPy arrays.

Both methods use the same generated spot prices and time-to-expiry values. The
benchmark fixes the comparison assumptions in code so `benchmark.csv` remains
auditable:

- Option type: `call`
- Strike: `105.0`
- Risk-free rate: `0.04`
- Volatility: `0.20`

## Output Contract

`benchmark.csv` records:

- `method`
- `num_prices`
- `option_type`
- `strike`
- `risk_free_rate`
- `volatility`
- `runtime_seconds`
- `speedup_vs_loop`
- `max_abs_error_vs_loop`
- `passed_equivalence_check`

When `benchmark.enabled` is false, PyRiskLab still writes an empty
`benchmark.csv` with the same headers and explains the disabled benchmark in the
summary report.

## How To Read The Result

Read the benchmark in this order:

1. Confirm `passed_equivalence_check` is true.
2. Inspect `max_abs_error_vs_loop` to see the numerical difference between the
   loop and vectorized paths.
3. Compare `runtime_seconds` and `speedup_vs_loop`.

Runtime is machine-dependent. Results can vary with CPU, operating system,
Python version, NumPy/SciPy versions, background load, and
`benchmark.num_prices`.
The repository therefore documents the benchmark shape and assumptions instead
of claiming a fixed speedup.

## Scope Boundaries

This is a local Python benchmark for software-engineering evidence. It is not:

- a GPU benchmark
- a C++ benchmark
- a Numba benchmark
- a trading-performance claim
- a profitability claim

The useful interview point is that PyRiskLab verifies numerical equivalence
before reporting speedup, keeps benchmark inputs deterministic, and writes the
result as a reproducible local artifact.
