# Changelog

All notable PyRiskLab project changes are summarized here. The project follows
plain semantic version labels for portfolio clarity rather than package
distribution automation.

## 0.1.0 - Version 1 MVP

Initial local Python simulation engine for options-pricing and risk-analysis
portfolio review.

### Added

- `python -m pyrisklab run --config configs/demo.yaml --overwrite` one-command demo.
- Real `src/pyrisklab/` package layout with CLI, root `pyrisklab.run_simulation(...)` entry point, typed progress callback support, config loading, orchestration, pricing, Greeks, strategy, fake execution, portfolio, risk, reporting, and benchmark modules.
- Deterministic YAML configs, including `configs/demo.yaml` and `configs/risk_stress.yaml`.
- Synthetic geometric Brownian motion market simulation with seeded reproducibility.
- SciPy-based Black-Scholes pricing for call and put contracts.
- Delta, gamma, vega, theta, and rho calculation over the simulated path.
- Simple delta-threshold fake strategy with readable signal reasons.
- Simulated order creation, deterministic fake fills, portfolio accounting, P&L, and drawdown tracking.
- Config-driven risk validation with approved, blocked, and skipped simulated-order audit statuses.
- Loop-vs-vectorized NumPy pricing benchmark with numerical-equivalence checks.
- CSV, PNG, copied-config, JSON metadata, and Markdown summary-report outputs under `results/<run_name>/`.
- Reviewer-focused documentation, sample-output contracts, config reference, architecture diagrams, final checklist, and interview framing.
- Requirement traceability, validation notes, performance notes, debugging guide, demo walkthrough, project status summary, resume snippets, and a local verification helper with preview, skip, and targeted `--only` modes.
- Console-focused package metadata with testing, automation, quality-assurance, and performance-tooling classifiers, plus MIT license, typed package marker, repo hygiene rules, scoped GitHub issue/PR templates, and pytest coverage for core behavior, helper command planning, and documentation contracts.

### Scope Boundaries

- Simulation only: no live market data, broker integrations, real trades, dashboards, SaaS features, databases, cloud deployment, or investment advice.
- Generated run outputs stay local and are intentionally ignored except for `results/.gitkeep`.
