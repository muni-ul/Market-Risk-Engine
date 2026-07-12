## Summary

Describe the change briefly.

## Change Type

- [ ] Runtime behavior
- [ ] Tests or validation
- [ ] Documentation
- [ ] Packaging or repo hygiene

## Local Validation

Run the checks that match the change. Generated result folders should stay
local and out of git.

```bash
pytest
ruff check .
python -m pyrisklab run --config configs/demo.yaml --overwrite
python -m pyrisklab run --config configs/risk_stress.yaml --overwrite
```

## Reviewer Artifacts

If the pipeline output changed, inspect:

- `results/demo_run/summary_report.md`
- `results/demo_run/run_metadata.json`
- `results/demo_run/benchmark.csv`
- `results/demo_run/orders.csv`
- `results/demo_run/risk_events.csv`

Also update `docs/REVIEWER_GUIDE.md`, `docs/FINAL_REVIEW_CHECKLIST.md`, or
`docs/sample_outputs/` if reviewer workflow or output contracts changed.

## Scope Check

- [ ] Keeps PyRiskLab local and simulation-only
- [ ] Does not add live market data, broker APIs, real trades, dashboards,
      SaaS features, databases, cloud deployment, or investment advice
- [ ] Keeps generated results out of git except `results/.gitkeep`
- [ ] Updates relevant docs or sample-output contracts when behavior changes
