---
name: Feature request
about: Suggest a scoped PyRiskLab improvement
title: "[Feature]: "
labels: enhancement
assignees: ""
---

## Summary

Describe the improvement briefly.

## Software Engineering Signal

Which project signal would this strengthen?

- [ ] CLI automation
- [ ] Config validation or reproducibility
- [ ] Numerical correctness
- [ ] pandas output contracts
- [ ] Risk validation or fake execution auditability
- [ ] Benchmark or performance reporting
- [ ] Debugging or error handling
- [ ] Documentation or reviewer experience
- [ ] Packaging or repo hygiene

## Proposed Behavior

What should change for a local reviewer running the project?

## Validation Plan

Which local checks would prove the change works?

```bash
pytest
ruff check .
python -m pyrisklab run --config configs/demo.yaml --overwrite
python -m pyrisklab run --config configs/risk_stress.yaml --overwrite
```

You can also preview or target the same local checks with:

```bash
python scripts/local_verify.py --list
python scripts/local_verify.py --only ruff --only demo
```

## Output Contract Impact

Will this change any generated artifact names, columns, charts, metadata fields,
or summary-report sections?

Should this update `docs/REVIEWER_GUIDE.md`, `docs/FINAL_REVIEW_CHECKLIST.md`,
or `docs/sample_outputs/`?
Should this update `docs/INTERVIEW_NOTES.md`, `docs/RESUME_SNIPPETS.md`, or
`docs/GITHUB_PROFILE_SETUP.md` for resume, interview, or public GitHub
presentation wording?

## Scope Check

PyRiskLab Version 1 is local and simulation-only. Feature requests should not
add live market data, brokerage integration, real trades, dashboards, SaaS
features, databases, cloud deployment, accounts, payments, ML trading
prediction, or investment advice.
