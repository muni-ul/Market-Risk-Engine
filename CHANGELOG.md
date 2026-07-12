# Changelog

All notable PyRiskLab project changes are summarized here. The project follows
plain semantic version labels for portfolio clarity rather than package
distribution automation.

## 0.1.0 - Version 1 MVP

Initial local Python simulation engine for options-pricing and risk-analysis
portfolio review.

### Added

- `python -m pyrisklab run --config configs/demo.yaml --overwrite`
  one-command demo.
- Real `src/pyrisklab/` package layout with CLI, config loading,
  orchestration, pricing, Greeks, strategy, fake execution, portfolio, risk,
  reporting, and benchmark modules.
- Root `pyrisklab.run_simulation(...)` entry point with typed progress callback
  support for package-style reuse.
- Deterministic YAML configs, including `configs/demo.yaml` and
  `configs/risk_stress.yaml`.
- Synthetic geometric Brownian motion market simulation with seeded
  reproducibility.
- SciPy-based Black-Scholes pricing for call and put contracts.
- Delta, gamma, vega, theta, and rho calculation over the simulated path.
- Simple delta-threshold fake strategy with readable signal reasons.
- Simulated order creation, deterministic fake fills, portfolio accounting,
  P&L, and drawdown tracking.
- Config-driven risk validation with approved, blocked, and skipped
  simulated-order audit statuses.
- Loop-vs-vectorized NumPy pricing benchmark with numerical-equivalence checks.
- CSV, PNG, copied-config, JSON metadata, and Markdown summary-report outputs
  under `results/<run_name>/`.
- Reviewer-focused docs for sample-output contracts, config reference,
  architecture, validation, performance, debugging, final review, and interview
  framing.
- Requirement traceability, project status, resume snippets, and portfolio case
  study docs for recruiter and technical-interview review.
- Local verification helper with preview, skip, keep-going, and targeted
  `--only` modes.
- Console-focused package metadata with testing, automation, quality-assurance,
  and performance-tooling classifiers.
- MIT license, typed package marker, repo hygiene rules, scoped GitHub issue/PR
  templates, and pytest coverage for core behavior, helper command planning,
  and documentation contracts.

### Scope Boundaries

- Simulation only: no live market data, broker integrations, real trades,
  dashboards, SaaS features, databases, cloud deployment, or investment advice.
- Generated run outputs stay local and are intentionally ignored except for `results/.gitkeep`.
