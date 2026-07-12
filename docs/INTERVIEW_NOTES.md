# PyRiskLab Interview Notes

## One-Minute Pitch

PyRiskLab is a local Python simulation engine that uses options pricing as the
domain, but the real focus is software engineering. It has deterministic YAML
configs, a CLI pipeline, NumPy/SciPy numerical code, pandas outputs, fake
execution, portfolio state tracking, risk validation, pytest tests, benchmark
reporting, and generated CSV/PNG/Markdown artifacts.

## AMD-Style Framing

Use this framing when the interviewer cares about systems, tooling, validation,
or performance work:

> I built PyRiskLab as a local Python engineering tool. The finance domain gives
> it realistic numerical and state-management problems, but the project signal
> is deterministic automation, defensive validation, test coverage, benchmark
> evidence, and reproducible artifact generation.

## Why It Fits SWE Intern Roles

- It is a finished local tool, not a notebook.
- It shows package structure, CLI automation, config validation, and custom errors.
- It includes numerical simulation and vectorized computation.
- It tests formula behavior, state transitions, risk rules, and output contracts.
- It measures performance with an honest loop-vs-vectorized benchmark.
- It documents scope clearly and avoids real trading claims.

## Strong Talking Points

- Deterministic seeds make simulations reproducible and debuggable.
- Black-Scholes pricing and Greeks are separated into focused numerical modules.
- The strategy is intentionally simple because it exists to drive system
  behavior, not profitability.
- Defensive validation is layered: config catches user mistakes early, domain
  modules protect invariants, and the CLI keeps expected errors readable.
- Risk validation is separate from portfolio accounting and fake execution.
- `configs/risk_stress.yaml` intentionally tightens position and notional
  limits so reviewers can see blocked orders and readable risk events.
- Reporting uses CSV, PNG, and Markdown so reviewers can inspect outputs without a dashboard.
- The benchmark verifies numerical equivalence before reporting speedup.
- Benchmark input validation keeps performance numbers tied to comparable, finite input arrays.
- `run_metadata.json` records config SHA-256, benchmark settings, row counts,
  order status counts, expected/generated artifacts, and artifact byte sizes so
  the run is auditable.
- `docs/DEMO_WALKTHROUGH.md` gives a short screenshot and talk-track path for
  GitHub or interview review.
- `docs/DESIGN_DECISIONS.md` summarizes the major tradeoffs behind the local
  CLI, package layout, config-driven runs, artifacts, and benchmarking.
- `docs/RESUME_SNIPPETS.md` gives resume-ready bullet options and wording
  boundaries.
- `docs/FINAL_REVIEW_CHECKLIST.md` gives the final local validation path before
  using the project on a resume.
- `docs/FAQ.md` gives concise answers to common reviewer and interview
  questions.

## Code Walkthrough Path

For a live technical walkthrough, open files in this order:

1. `src/pyrisklab/cli.py` to show the one-command local interface and clean
   error handling.
2. `src/pyrisklab/config.py` and `configs/demo.yaml` to show deterministic,
   validated inputs.
3. `src/pyrisklab/pipeline.py` to show how the run is orchestrated without
   putting all logic in the CLI.
4. `src/pyrisklab/pricing.py` and `src/pyrisklab/greeks.py` to show focused
   numerical code.
5. `src/pyrisklab/risk.py`, `src/pyrisklab/execution.py`, and
   `src/pyrisklab/portfolio.py` to show state transitions and defensive
   boundaries.
6. `src/pyrisklab/reporting.py` and `src/pyrisklab/benchmark.py` to show
   reproducible artifacts and performance evidence.
7. `tests/` to show how the project protects formulas, validation, state
   transitions, artifact contracts, and repository hygiene.

## Resume Bullets

General:

> Built PyRiskLab, a modular local Python simulation engine using NumPy, pandas,
> SciPy, matplotlib, and pytest to simulate market paths, price options,
> calculate Greeks, execute fake trades, enforce risk controls, benchmark
> vectorized computation, and export reproducible portfolio reports.

Performance/tooling:

> Developed a performance-aware Python simulation and analytics tool with
> deterministic YAML configs, CLI automation, vectorized numerical computation,
> pytest coverage, benchmark reporting, and reproducible local artifacts.

## Scope Boundaries

PyRiskLab is simulation only. It does not use live market data, connect to
brokerages, place real trades, make investment recommendations, or claim
profitability.

## Final Verification Story

Before presenting the project, run the checklist in
`docs/FINAL_REVIEW_CHECKLIST.md`: execute `pytest`, `ruff check .`, the main
demo config, and the risk-stress config; then inspect `summary_report.md`,
`run_metadata.json`, benchmark evidence, risk events, and generated charts. That
final pass is what turns the repository from "implemented" into "ready to
discuss."
