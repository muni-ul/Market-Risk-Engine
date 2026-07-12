# PyRiskLab FAQ

## Is this a trading bot?

No. PyRiskLab is simulation only. It does not use live market data, connect to a
brokerage, place real orders, provide investment advice, or claim profitability.

## Why use finance as the domain?

Options pricing creates useful software-engineering problems: numerical
calculation, state transitions, validation rules, benchmark comparisons, and
auditable outputs. The project signal is the local Python system, not trading.

## Why a CLI instead of a dashboard?

The target signal is Python simulation, automation, testing, and performance
tooling. A CLI keeps the demo reproducible, scriptable, and easy for reviewers
to run without accounts, cloud services, databases, or frontend setup.

## Why synthetic data?

Synthetic market paths keep the project deterministic, local, and safe to run.
They avoid API keys, network failures, licensing concerns, and accidental claims
that the project is using real market data.

## What should a reviewer inspect first?

Start with `README.md`, then run or review:

```bash
python -m pyrisklab run --config configs/demo.yaml --overwrite
```

After a local run, inspect `results/demo_run/summary_report.md`,
`run_metadata.json`, `benchmark.csv`, `orders.csv`, and `risk_events.csv`.

## What does the benchmark prove?

It compares loop-based Black-Scholes pricing with vectorized NumPy pricing on
the same generated inputs, verifies numerical equivalence, and records
machine-dependent timing. It proves performance-aware engineering, not a fixed
universal speedup.

## Why is the strategy simple?

The strategy exists to drive system behavior for fake execution, portfolio
state, risk validation, and reporting. Profitability is intentionally out of
scope.

## How do I know the outputs are reproducible?

Runs are config-driven and seeded. Each run copies `config_used.yaml` and writes
`run_metadata.json` with the config SHA-256 digest, project version, row counts,
order status counts, expected/generated artifacts, and artifact byte sizes.

## What makes this relevant for SWE internships?

PyRiskLab demonstrates package structure, CLI automation, deterministic configs,
defensive validation, pandas output contracts, pytest coverage, benchmark
reporting, debugging docs, and clean scope control.

## How should I validate it before sharing?

Use `docs/FINAL_REVIEW_CHECKLIST.md` as the resume-ready gate. The direct local
commands are `pytest`, `ruff check .`, the main demo command, and the
risk-stress demo command. The helper `python scripts/local_verify.py --list`
previews the same sequence, and `python scripts/local_verify.py --only ruff
--only demo` runs a targeted subset.

## How should I describe it on a resume or in an interview?

Use `docs/RESUME_SNIPPETS.md` for concise resume wording and
`docs/INTERVIEW_NOTES.md` for the one-minute pitch, talking points, and
scope boundaries. Keep the framing on local Python tooling, testing,
validation, reproducibility, and performance-aware engineering.
