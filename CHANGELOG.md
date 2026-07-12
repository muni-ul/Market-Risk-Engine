# Changelog

All notable PyRiskLab project changes are summarized here. The project follows
plain semantic version labels for portfolio clarity rather than package
distribution automation.

For version-source alignment rules, see `docs/VERSIONING.md`.

## 0.1.0 - Version 1 MVP

Initial local Python simulation engine for options-pricing and risk-analysis
portfolio review.

### Added

- `python -m pyrisklab run --config configs/demo.yaml --overwrite`
  one-command demo.
- Real `src/pyrisklab/` package layout with CLI, config loading,
  orchestration, pricing, Greeks, strategy, fake execution, portfolio, risk,
  reporting, and benchmark modules.
- Package-root `pyrisklab.run_simulation(...)` entry point with typed progress
  callback support for package-style reuse, mirrored by the repo-root launcher
  shim before editable installs.
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
- Recruiter brief, FAQ, design-decisions summary, assumptions ledger,
  implementation audit notes, dependency policy, platform notes, versioning
  guidance, GitHub profile setup, support routing, and reviewer hand-off docs
  for final portfolio presentation.
- Interview code walkthrough path, validation-before-sharing FAQ guidance, and
  GitHub About-panel checklist to help the project move cleanly from local
  validation to resume and profile use.
- Feature build index mapping the original ordered feature specs to current
  implementation evidence.
- Final review checklist with a resume-ready gate for user-run validation before
  public portfolio use.
- Local verification helper with preview, skip, keep-going, and targeted
  `--only` modes.
- Console-focused package metadata with testing, automation, quality-assurance,
  performance-tooling classifiers, and direct reviewer/changelog/support links.
- MIT license, typed package marker, repo hygiene rules, scoped GitHub issue/PR
  templates, disabled blank issues, and pytest coverage for core behavior,
  helper command planning, GitHub presentation metadata, and documentation
  contracts.

### Scope Boundaries

- Simulation only: no live market data, broker integrations, real trades,
  dashboards, SaaS features, databases, cloud deployment, or investment advice.
- Generated run outputs stay local and are intentionally ignored except for
  `results/.gitkeep`.
