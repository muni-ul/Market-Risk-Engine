# PyRiskLab Interview Notes

## One-Minute Pitch

PyRiskLab is a local Python simulation engine that uses options pricing as the domain, but the real focus is software engineering. It has deterministic YAML configs, a CLI pipeline, NumPy/SciPy numerical code, pandas outputs, fake execution, portfolio state tracking, risk validation, pytest tests, benchmark reporting, and generated CSV/PNG/Markdown artifacts.

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
- The strategy is intentionally simple because it exists to drive system behavior, not profitability.
- Risk validation is separate from portfolio accounting and fake execution.
- `configs/risk_stress.yaml` intentionally tightens position and notional limits so reviewers can see blocked orders and readable risk events.
- Reporting uses CSV, PNG, and Markdown so reviewers can inspect outputs without a dashboard.
- The benchmark verifies numerical equivalence before reporting speedup.

## Resume Bullets

General:

> Built PyRiskLab, a modular local Python simulation engine using NumPy, pandas, SciPy, matplotlib, and pytest to simulate market paths, price options, calculate Greeks, execute fake trades, enforce risk controls, benchmark vectorized computation, and export reproducible portfolio reports.

Performance/tooling:

> Developed a performance-aware Python simulation and analytics tool with deterministic YAML configs, CLI automation, vectorized numerical computation, pytest coverage, benchmark reporting, and reproducible local artifacts.

## Scope Boundaries

PyRiskLab is simulation only. It does not use live market data, connect to brokerages, place real trades, make investment recommendations, or claim profitability.
