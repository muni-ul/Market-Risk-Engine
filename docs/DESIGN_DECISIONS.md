# Design Decisions

This page summarizes the main Version 1 engineering choices behind PyRiskLab.
The goal is to make the project easy to discuss in a technical interview without
requiring a reviewer to read every planning document.

## Local CLI First

PyRiskLab uses a command-line workflow instead of a dashboard. One command is
easy to reproduce, automate, test, and document:

```bash
python -m pyrisklab run --config configs/demo.yaml --overwrite
```

This keeps the project focused on Python simulation, validation, benchmarking,
and artifact generation instead of frontend or deployment work.

## Real Package Layout

Runtime code lives under `src/pyrisklab/`, with a lightweight repo-root launcher
shim for `python -m pyrisklab` before editable installation. This shows package
structure while keeping the reviewer demo simple from the repository root.

## Config-Driven Runs

YAML configs define the seed, market assumptions, option contract, strategy,
execution settings, risk limits, benchmark settings, and output folder. Each run
copies the config and records a SHA-256 digest in metadata so outputs can be
traced back to inputs.

## Separated Domain Modules

Market simulation, pricing, Greeks, strategy, execution, portfolio accounting,
risk validation, benchmarking, and reporting live in separate modules. This
keeps numerical code testable, stateful code explicit, and reporting from
owning simulation logic.

## File-Based Artifacts

CSV, PNG, JSON, YAML, and Markdown outputs are used because they are easy to
inspect locally, open in common tools, and review on GitHub. A database would add
setup overhead without strengthening the Version 1 software-engineering signal.

## Honest Benchmarking

The benchmark compares loop-based and vectorized Black-Scholes pricing on the
same inputs, checks numerical equivalence, and reports machine-dependent timing.
It is meant to demonstrate performance-aware engineering, not universal speedup
claims.

## Simulation-Only Boundary

The project intentionally avoids live market data, brokerage APIs, real trades,
dashboards, SaaS features, cloud deployment, databases, ML trading prediction,
and investment advice. Finance is the simulation domain; software engineering is
the project signal.

## Reviewer Evidence Trail

The concise decision story here pairs with `docs/ARCHITECTURE.md` for module
flow, `docs/REQUIREMENTS_TRACEABILITY.md` for requirement evidence, and
`docs/FINAL_REVIEW_CHECKLIST.md` for the final local verification path before
using the project in a resume or interview.
