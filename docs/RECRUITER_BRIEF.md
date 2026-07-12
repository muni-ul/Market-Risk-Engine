# PyRiskLab Recruiter Brief

PyRiskLab is a local Python engineering project that uses options pricing as a
simulation domain. The project is not meant to present trading expertise; it is
meant to show that the candidate can build, document, and validate a
production-style local tool.

## Target Role Signal

Best-fit framing:

> Software Engineering Intern - Python Simulation, Automation, Testing, and
> Performance Tooling

PyRiskLab is especially relevant for roles that value Python tooling,
deterministic workflows, test automation, debugging, numerical computation, and
performance-aware engineering.

## What To Notice Quickly

- Real Python package layout under `src/pyrisklab/`
- One-command CLI demo:
  `python -m pyrisklab run --config configs/demo.yaml --overwrite`
- Deterministic YAML configs and copied run config for reproducibility
- Modular pipeline for config, market simulation, pricing, Greeks, strategy,
  fake execution, portfolio state, risk validation, benchmarking, and reporting
- pytest suite covering formulas, state transitions, risk rules, reporting
  contracts, packaging metadata, and repo hygiene
- Benchmark comparing Python-loop Black-Scholes pricing with vectorized NumPy
  pricing on the same generated inputs
- Generated CSV, PNG, JSON, YAML, and Markdown artifacts under
  `results/demo_run/` after a local run
- Optional risk-stress config that writes `results/risk_stress_run/` with
  blocked simulated orders and readable risk events

## Best Files To Skim

- `README.md`: project overview, setup, demo command, outputs, and boundaries
- `docs/REVIEWER_GUIDE.md`: five-minute technical review path
- `docs/FAQ.md`: direct answers to common reviewer and interview questions
- `docs/DESIGN_DECISIONS.md`: concise summary of major engineering tradeoffs
- `docs/PROJECT_STATUS.md`: implemented scope and user-run validation commands
- `docs/REQUIREMENTS_TRACEABILITY.md`: Version 1 requirements mapped to evidence
- `docs/FINAL_REVIEW_CHECKLIST.md`: final local validation and resume-ready gate
- `docs/INTERVIEW_NOTES.md`: one-minute pitch and technical talking points
- `docs/RESUME_SNIPPETS.md`: resume-ready bullets and keywords

## What This Project Is Not

PyRiskLab is not a trading bot, live-market dashboard, brokerage integration,
investment tool, SaaS product, or profitability model. It does not use live
market data, broker accounts, cloud services, databases, API keys, or real
orders.

The strongest signal is software engineering: package structure, deterministic
automation, validation, tests, benchmark evidence, debugging documentation, and
reproducible local artifacts.
