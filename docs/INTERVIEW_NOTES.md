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
- `docs/RESUME_SNIPPETS.md` gives resume-ready bullet options and wording
  boundaries.
- `docs/FINAL_REVIEW_CHECKLIST.md` gives the final local validation path before
  using the project on a resume.
- `docs/FAQ.md` gives concise answers to common reviewer and interview
  questions.

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
