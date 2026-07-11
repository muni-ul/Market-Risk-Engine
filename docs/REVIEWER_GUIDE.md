# PyRiskLab Reviewer Guide

This guide is the short path for someone evaluating PyRiskLab as a software engineering portfolio project.

PyRiskLab uses options pricing as the simulation domain, but the project signal is Python engineering: package structure, CLI automation, deterministic configs, numerical computation, state management, risk validation, tests, benchmark evidence, and reproducible local artifacts.

## Five-Minute Review Path

1. Read the top of `README.md` to confirm the project scope and simulation-only disclaimer.
2. Skim `docs/ARCHITECTURE.md` for the module responsibilities and data flow.
3. Open `docs/SAMPLE_OUTPUT.md` for the expected terminal output and report shape.
4. Inspect `docs/sample_outputs/csv_contracts.md` and `docs/sample_outputs/chart_artifacts.md` for the generated artifact contracts.
5. Read `docs/PORTFOLIO_CASE_STUDY.md` for the engineering decisions and interview story.

## Main Demo Command

```bash
python -m pyrisklab run --config configs/demo.yaml --overwrite
```

The command creates `results/demo_run/` locally. Generated outputs are intentionally not committed as a full results folder, so reviewers can reproduce them from the config.

## What To Inspect After Running

```text
results/demo_run/
  config_used.yaml
  market_path.csv
  pricing_history.csv
  greeks_history.csv
  signals.csv
  orders.csv
  trades.csv
  portfolio_history.csv
  risk_events.csv
  benchmark.csv
  run_metadata.json
  market_path.png
  option_price.png
  greeks.png
  portfolio_value.png
  drawdown.png
  summary_report.md
```

The strongest files to open first are:

- `summary_report.md`: run summary, simulation-only language, Greeks, risk/execution audit counts, benchmark evidence, run metadata section, generated artifact list, and limitations.
- `run_metadata.json`: config path, config SHA-256 digest, benchmark settings, row counts, order status counts, expected artifacts, generated artifacts, and generated artifact byte sizes.
- `orders.csv`: proposed simulated orders with `status` and `risk_reason` audit columns.
- `benchmark.csv`: loop-vs-vectorized Black-Scholes assumptions, runtime, speedup, max absolute error, and equivalence check.
- `portfolio_value.png` and `drawdown.png`: quick visual evidence that portfolio state is tracked through the run.

## Optional Risk-Audit Demo

```bash
python -m pyrisklab run --config configs/risk_stress.yaml --overwrite
```

This preset tightens risk limits so proposed orders are blocked. It is useful for checking that risk validation, blocked-order reasons, `risk_events.csv`, order status counts, and summary-report audit sections are visible without editing the main demo config.

## Testing And Lint Commands

```bash
pytest
ruff check .
```

Tests are organized by feature area under `tests/`, including config validation, market simulation, pricing, Greeks, strategy, execution, portfolio accounting, risk validation, reporting, benchmark behavior, and pipeline smoke coverage.

## What The Project Is Not

PyRiskLab is not a trading bot, brokerage integration, live market-data client, dashboard app, SaaS product, database project, ML trading predictor, or investment-advice tool. It is a local simulation and reporting engine built to demonstrate software engineering discipline.
