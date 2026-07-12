---
name: Bug report
about: Report a reproducible PyRiskLab issue
title: "[Bug]: "
labels: bug
assignees: ""
---

## Summary

Describe the issue briefly.

## Reproduction

```bash
python -m pyrisklab run --config configs/demo.yaml --overwrite
```

If you used a different config, name it here.

## Expected Behavior

What did you expect to happen?

## Actual Behavior

What happened instead?

## Environment

- Python version:
- Operating system:
- PyRiskLab version or commit:

## Generated Artifacts To Inspect

If the run completed, mention any relevant files under `results/<run_name>/`,
especially `summary_report.md`, `run_metadata.json`, `orders.csv`,
`risk_events.csv`, or `benchmark.csv`.

## Scope Check

PyRiskLab is simulation-only. Issues should not request live market data,
brokerage integration, real trades, dashboards, SaaS features, databases, cloud
deployment, or investment advice.
