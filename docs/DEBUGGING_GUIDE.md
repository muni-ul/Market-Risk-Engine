# PyRiskLab Debugging Guide

PyRiskLab is designed to fail with readable project errors for normal user or
config mistakes. Use this guide when diagnosing a local run.

## Start With The Normal Demo

```bash
python -m pyrisklab run --config configs/demo.yaml --overwrite
```

Expected user-facing errors are printed without a long traceback:

```text
ConfigError: market.volatility must be >= 0. Received -0.20.
RunError: results/demo_run already exists. Use --overwrite or choose a different run_name.
```

## Use Debug Mode For Tracebacks

When developing or investigating an unexpected failure, add `--debug`:

```bash
python -m pyrisklab run --config configs/demo.yaml --debug
```

Debug mode keeps the same project error type but prints traceback details so
the failing module is easier to locate.

## Triage Generated Outputs

If a run completes, inspect these files first:

- `results/demo_run/summary_report.md`: human-readable summary, limitations,
  risk/execution counts, benchmark notes, and artifact list.
- `results/demo_run/run_metadata.json`: config SHA-256, benchmark settings,
  row counts, order status counts, expected/generated artifacts, and artifact
  byte sizes.
- `results/demo_run/orders.csv`: approved, blocked, or skipped simulated-order
  status and `risk_reason`.
- `results/demo_run/risk_events.csv`: blocked-order reason details for risk
  breaches.
- `results/demo_run/benchmark.csv`: loop-vs-vectorized timings and numerical
  equivalence status.

## Common Checks

- If the output folder already exists, rerun with `--overwrite` or change
  `run_name` in the config.
- If config validation fails, compare the field against `docs/CONFIG_REFERENCE.md`.
- If risk behavior is unclear, run `configs/risk_stress.yaml` and inspect
  `risk_events.csv`.
- If a report artifact is missing or empty, inspect `run_metadata.json` and the
  generated artifact list in `summary_report.md`.
- If benchmark timing looks surprising, remember that speedup is machine
  dependent; the equivalence flag and max absolute error are the correctness
  signals.

## Scope Boundary

Debugging should stay local. PyRiskLab does not depend on live market data,
brokerage credentials, network calls, databases, dashboards, or cloud services.
