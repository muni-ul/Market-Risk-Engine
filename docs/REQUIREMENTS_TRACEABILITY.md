# PyRiskLab Requirements Traceability

This page maps the original Version 1 project requirements to the current
repository artifacts. It is meant for reviewers who want to confirm that
PyRiskLab is a finished local Python engineering project, not a loose script or
notebook.

## Requirement Map

| Requirement | Current evidence |
| --- | --- |
| One command runs the project | `python -m pyrisklab run --config configs/demo.yaml --overwrite` is documented in `README.md`, `docs/REVIEWER_GUIDE.md`, and `docs/FINAL_REVIEW_CHECKLIST.md`. |
| Real package layout | Runtime code lives under `src/pyrisklab/`; the root `pyrisklab/` package is a launcher shim that mirrors the small public API for repo-root CLI/import use. |
| Clean module split | `docs/ARCHITECTURE.md` and `docs/API_REFERENCE.md` describe the CLI, config, market, pricing, Greeks, strategy, execution, portfolio, risk, benchmark, reporting, and pipeline modules. |
| Config-driven reproducibility | `configs/demo.yaml`, `configs/risk_stress.yaml`, copied `config_used.yaml`, config SHA-256 metadata, and `docs/CONFIG_REFERENCE.md`. |
| NumPy, pandas, SciPy, matplotlib stack | Declared in `requirements.txt` and `pyproject.toml`; summarized in `README.md`. |
| SciPy Black-Scholes pricing | `src/pyrisklab/pricing.py`, `tests/test_pricing.py`, and `docs/API_REFERENCE.md`. |
| Greeks calculation | `src/pyrisklab/greeks.py`, `tests/test_greeks.py`, and generated `greeks_history.csv` / `greeks.png` contracts. |
| Fake execution and portfolio state | `src/pyrisklab/execution.py`, `src/pyrisklab/portfolio.py`, `tests/test_execution.py`, `tests/test_portfolio.py`, and generated order/trade/portfolio artifacts. |
| Risk-rule validation | `src/pyrisklab/risk.py`, `tests/test_risk.py`, `configs/risk_stress.yaml`, the local `results/risk_stress_run/` artifact folder, and `docs/sample_outputs/risk_stress_demo.md`. |
| pytest suite exists | Tests are organized under `tests/`; coverage areas are mapped in `docs/TESTING_STRATEGY.md`. |
| CSV outputs | `docs/sample_outputs/csv_contracts.md` documents stable CSV artifact names and columns. |
| PNG charts | `docs/sample_outputs/chart_artifacts.md` documents generated chart artifacts. |
| Markdown summary report | `docs/SAMPLE_OUTPUT.md` and `docs/sample_outputs/summary_report_excerpt.md`. |
| Benchmark compares loop vs vectorized NumPy | `src/pyrisklab/benchmark.py`, `tests/test_benchmark.py`, `docs/PERFORMANCE_NOTES.md`, and `benchmark.csv` contract docs. |
| Simulation-only scope | `README.md`, `SECURITY.md`, `docs/REVIEWER_GUIDE.md`, and `docs/VALIDATION_NOTES.md` all reinforce no live data, no brokerage integration, no real trades, and no investment advice. |
| Polished reviewer presentation | `README.md`, `docs/DEMO_WALKTHROUGH.md`, `docs/REVIEWER_GUIDE.md`, `docs/PORTFOLIO_CASE_STUDY.md`, and `docs/INTERVIEW_NOTES.md`. |

## Final Verification Commands

Run these locally before putting the project on a resume:

```bash
pytest
ruff check .
python -m pyrisklab run --config configs/demo.yaml --overwrite
python -m pyrisklab run --config configs/risk_stress.yaml --overwrite
```

Or use the optional helper:

```bash
python scripts/local_verify.py
```

Use `python scripts/local_verify.py --list` to preview the helper command list
without running tests or demos.

Use `python scripts/local_verify.py --only ruff --only demo` when you want a
targeted local check instead of the full validation sequence.

The generated `results/` folders are intentionally not committed, so the final
evidence comes from running the commands locally and inspecting
`results/demo_run/`, `results/risk_stress_run/`, and the artifact list in
`docs/FINAL_REVIEW_CHECKLIST.md`.
