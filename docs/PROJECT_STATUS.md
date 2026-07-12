# PyRiskLab Project Status

PyRiskLab Version 1 is implemented as a local Python simulation and reporting
project. This page is a quick status summary for recruiters, reviewers, and
future maintainers.

## Implemented

- One-command CLI entry point: `python -m pyrisklab run --config configs/demo.yaml --overwrite`
- Real package layout under `src/pyrisklab/`
- Modular config, market, pricing, Greeks, strategy, execution, portfolio, risk,
  benchmark, reporting, and pipeline code
- Deterministic YAML configs for the main demo and risk-stress demo
- Synthetic market simulation, Black-Scholes pricing, Greeks, fake execution,
  portfolio tracking, risk validation, and benchmark reporting
- CSV, PNG, JSON, copied-config, and Markdown report artifact contracts
- pytest suite covering core modules, output contracts, packaging metadata, and
  repo hygiene
- Reviewer docs for architecture, config, validation, performance, debugging,
  demo walkthrough, traceability, resume wording, and final verification

## User-Run Verification

Generated run outputs are intentionally not committed. Before using the project
on a resume, run the local verification pass from the repository root:

```bash
pytest
ruff check .
python -m pyrisklab run --config configs/demo.yaml --overwrite
python -m pyrisklab run --config configs/risk_stress.yaml --overwrite
```

To preview the helper command list without running anything:

```bash
python scripts/local_verify.py --list
```

To run the helper:

```bash
python scripts/local_verify.py
```

## Not Included

PyRiskLab intentionally does not include live market data, brokerage
integrations, real order execution, dashboards, SaaS accounts, databases, cloud
deployment, ML trading prediction, or investment advice.

## Best Reviewer Starting Points

- `README.md`
- `docs/REVIEWER_GUIDE.md`
- `docs/REQUIREMENTS_TRACEABILITY.md`
- `docs/FINAL_REVIEW_CHECKLIST.md`
- `docs/RESUME_SNIPPETS.md`
