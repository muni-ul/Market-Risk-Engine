# PyRiskLab Reviewer Guide

This guide is the short path for someone evaluating PyRiskLab as a software
engineering portfolio project.

PyRiskLab uses options pricing as the simulation domain, but the project signal
is Python engineering: package structure, CLI automation, deterministic configs,
numerical computation, state management, risk validation, tests, benchmark
evidence, and reproducible local artifacts.

## Best Signal

For software-intern review, focus less on finance and more on the engineering
shape: one-command automation, clean modules, defensive validation,
debugging-friendly errors, stateful simulation, generated output contracts,
benchmark evidence, and reviewer documentation.

## Five-Minute Review Path

1. Read the top of `README.md` to confirm the project scope and simulation-only
   disclaimer.
2. Skim `docs/PROJECT_STATUS.md` for implemented scope and local verification
   commands.
3. Skim `docs/features/README.md` for the ordered feature plan mapped to
   implementation evidence.
4. Skim `docs/REQUIREMENTS_TRACEABILITY.md` for the original requirements
   mapped to current repo evidence.
5. Skim `docs/FAQ.md` for direct answers to common reviewer questions.
6. Skim `docs/DESIGN_DECISIONS.md` for the major engineering tradeoffs.
7. Skim `docs/ARCHITECTURE.md` for the module responsibilities and data flow.
8. Skim `docs/CONFIG_REFERENCE.md` for the YAML inputs that drive the run.
9. Skim `docs/VALIDATION_NOTES.md` for defensive checks and edge-case coverage.
10. Open `docs/SAMPLE_OUTPUT.md` for the expected terminal output and report
   shape.
11. Open `docs/DEMO_WALKTHROUGH.md` for the screenshot targets and short talk
   track.
12. Inspect `docs/sample_outputs/artifact_manifest.md`,
   `docs/sample_outputs/csv_contracts.md`, and
   `docs/sample_outputs/chart_artifacts.md` for the generated artifact
   contracts.
13. Read `docs/PORTFOLIO_CASE_STUDY.md` for the engineering decisions and
    interview story.
14. Use `docs/FINAL_REVIEW_CHECKLIST.md` for the final local validation pass
    before resume use.

## Main Demo Command

```bash
python -m pyrisklab run --config configs/demo.yaml --overwrite
```

The command creates `results/demo_run/` locally. Generated outputs are
intentionally not committed as a full results folder, so reviewers can
reproduce them from the config.

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

- `summary_report.md`: run summary, simulation-only language, Greeks,
  risk/execution audit counts, benchmark evidence, run metadata section,
  generated artifact list, and limitations.
- `run_metadata.json`: config path, config SHA-256 digest, benchmark settings,
  row counts, order status counts, expected artifacts, generated artifacts, and
  generated artifact byte sizes.
- `orders.csv`: proposed simulated orders with `status` and `risk_reason` audit
  columns.
- `benchmark.csv`: loop-vs-vectorized Black-Scholes assumptions, runtime,
  speedup, max absolute error, and equivalence check.
- `portfolio_value.png` and `drawdown.png`: quick visual evidence that
  portfolio state is tracked through the run.

## Optional Risk-Audit Demo

```bash
python -m pyrisklab run --config configs/risk_stress.yaml --overwrite
```

This preset writes `results/risk_stress_run/` and tightens risk limits so
proposed orders are blocked. It is useful for checking that risk validation,
blocked-order reasons, `risk_events.csv`, order status counts, and
summary-report audit sections are visible without editing the main demo config.

## Testing And Lint Commands

```bash
pytest
ruff check .
```

Tests are organized by feature area under `tests/`, including config validation,
market simulation, pricing, Greeks, strategy, execution, portfolio accounting,
risk validation, reporting, benchmark behavior, and pipeline smoke coverage.

For the full local verification sequence, reviewers can also use the helper:

```bash
python scripts/local_verify.py
python scripts/local_verify.py --list
python scripts/local_verify.py --only ruff --only demo
```

Use `docs/FINAL_REVIEW_CHECKLIST.md` for the final resume-ready gate and
`docs/DEBUGGING_GUIDE.md` for targeted triage if any local command fails.

## What The Project Is Not

PyRiskLab is not a trading bot, brokerage integration, live market-data client,
dashboard app, SaaS product, database project, ML trading predictor, or
investment-advice tool. It is a local simulation and reporting engine built to
demonstrate software engineering discipline.
