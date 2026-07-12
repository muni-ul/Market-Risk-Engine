# Implementation Audit Notes

This page records static repo checks that help reviewers distinguish the
current implementation from historical planning notes under `docs/features/`.
It does not replace the final local validation commands in
`docs/FINAL_REVIEW_CHECKLIST.md`.

## Placeholder Scan

The finished implementation should not contain placeholder runtime code. When
auditing this, focus on the current source and tests:

```bash
rg -n "TODO|TBD|FIXME|NotImplemented|placeholder|stub|raise NotImplemented|coming soon" src tests
```

Expected result for the finished MVP: no matches in `src/` or `tests/`.

Some historical planning files under `docs/features/` intentionally mention
early placeholder steps because they preserve the original ordered build plan.
Those references are not runtime implementation placeholders.

## Current Runtime Surface

The active implementation lives in:

- `src/pyrisklab/` for the installable package
- `pyrisklab/` for the lightweight repo-root launcher/API shim
- `configs/demo.yaml` for the main deterministic demo
- `configs/risk_stress.yaml` for the blocked-order risk-audit demo
- `tests/` for pytest coverage
- `scripts/local_verify.py` for optional local validation orchestration

Generated outputs stay local under `results/<run_name>/` and are intentionally
ignored by Git except for `results/.gitkeep`.

## What This Audit Does Not Prove

Static checks can show that files, docs, and implementation markers are in the
right shape, but they do not prove runtime behavior. Before using PyRiskLab on a
resume or GitHub profile, run the final local validation pass:

```bash
pytest
ruff check .
python -m pyrisklab run --config configs/demo.yaml --overwrite
python -m pyrisklab run --config configs/risk_stress.yaml --overwrite
```
