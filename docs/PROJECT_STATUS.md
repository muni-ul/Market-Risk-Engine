# PyRiskLab Project Status

PyRiskLab Version 1 is implemented as a local Python simulation and reporting
project. This page is a quick status summary for recruiters, reviewers, and
future maintainers.

## Resume Signal

The strongest software-engineering signal is not the finance domain itself. It
is that PyRiskLab behaves like a small production-style local tool: one command
loads a deterministic config, runs a modular simulation pipeline, validates
inputs and risk rules, records state transitions, benchmarks vectorized
computation, and writes reproducible artifacts for review.

For AMD-like software internship applications, the best framing is:

> Local Python simulation, automation, testing, debugging, and
> performance-tooling project using options pricing as the problem domain.

## Implemented

- One-command CLI entry point: `python -m pyrisklab run --config configs/demo.yaml --overwrite`
- Real package layout under `src/pyrisklab/`
- Modular config, market, pricing, Greeks, strategy, execution, portfolio, risk,
  benchmark, reporting, and pipeline code
- Deterministic YAML configs for the main demo and risk-stress demo
  (`results/demo_run/` and `results/risk_stress_run/` when run locally)
- Synthetic market simulation, Black-Scholes pricing, Greeks, fake execution,
  portfolio tracking, risk validation, and benchmark reporting
- CSV, PNG, JSON, copied-config, and Markdown report artifact contracts
- pytest suite covering core modules, output contracts, packaging metadata, and
  repo hygiene
- Reviewer docs for architecture, design decisions, config, assumptions,
  validation, performance, debugging, platform notes, FAQ, demo walkthrough,
  traceability, resume wording, and final verification
- Feature build index mapping the original ordered feature plan to current
  implementation evidence
- GitHub bug report, feature request, and pull request templates that keep
  issues and changes scoped to local simulation engineering

## User-Run Verification

Generated run outputs are intentionally not committed. Before using the project
on a resume, run the local verification pass from the repository root:

```bash
pytest
ruff check .
python -m pyrisklab run --config configs/demo.yaml --overwrite
python -m pyrisklab run --config configs/risk_stress.yaml --overwrite
```

Use `docs/FINAL_REVIEW_CHECKLIST.md` for the complete artifact-inspection list
and resume-ready gate after those commands finish.

To preview the helper command list without running anything:

```bash
python scripts/local_verify.py --list
```

To run only selected checks:

```bash
python scripts/local_verify.py --only ruff --only demo
```

To run the helper:

```bash
python scripts/local_verify.py
```

After running the demos, keep `results/demo_run/` and
`results/risk_stress_run/` local. They are ignored by Git so the repository
stays lightweight while reviewers can reproduce the same artifact set from the
committed configs.

## Not Included

PyRiskLab intentionally does not include live market data, brokerage
integrations, real order execution, dashboards, SaaS accounts, databases, cloud
deployment, ML trading prediction, or investment advice.

## Best Reviewer Starting Points

- `README.md`
- `docs/RECRUITER_BRIEF.md`
- `docs/REVIEWER_GUIDE.md`
- `docs/DESIGN_DECISIONS.md`
- `docs/FAQ.md`
- `docs/features/README.md`
- `docs/REQUIREMENTS_TRACEABILITY.md`
- `docs/FINAL_REVIEW_CHECKLIST.md`
- `docs/RESUME_SNIPPETS.md`
