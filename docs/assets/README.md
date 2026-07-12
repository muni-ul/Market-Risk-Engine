# Screenshot Asset Guide

Use this folder for curated screenshots after you run PyRiskLab locally. Do not
copy the whole `results/` folder into the repo; keep generated run folders local
and only commit a small set of hand-picked images if you want GitHub or resume
reviewers to see visual evidence immediately.

Before committing any curated screenshots, complete the resume-ready validation
path in `docs/FINAL_REVIEW_CHECKLIST.md` so the images match the current configs,
artifact names, and documentation.

## Recommended Captures

After running:

```bash
python -m pyrisklab run --config configs/demo.yaml --overwrite
```

capture or copy:

- `results/demo_run/summary_report.md` preview as `summary-report.png`
- `results/demo_run/portfolio_value.png` as `portfolio-value.png`
- `results/demo_run/drawdown.png` as `drawdown.png`
- `results/demo_run/benchmark.csv` preview as `benchmark-csv.png`
- `results/demo_run/run_metadata.json` preview as `run-metadata.png`

For the risk-audit preset:

```bash
python -m pyrisklab run --config configs/risk_stress.yaml --overwrite
```

capture a preview of `results/risk_stress_run/risk_events.csv` as
`risk-events.png`.

## Review Notes

- Keep screenshots focused on software-engineering evidence: CLI execution,
  artifact contracts, risk validation, benchmark reporting, and reproducibility.
- Avoid screenshots that imply real trading, profitability, live market data, or
  brokerage connectivity.
- Regenerate screenshots only after your final local validation pass so images
  match the committed configs and docs.
