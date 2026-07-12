# Versioning

PyRiskLab uses simple semantic-style version labels for portfolio clarity. The
current Version 1 MVP is `0.1.0`.

## Version Sources

Keep these values aligned when the project version changes:

- `pyproject.toml` under `[project].version`
- `src/pyrisklab/_version.py`
- `CHANGELOG.md`
- sample metadata docs such as `docs/sample_outputs/run_metadata_example.md`

The runtime report metadata records `project_version` from the package
`__version__`, so reviewers can connect generated artifacts back to the source
version that produced them.

## When To Change Versions

- Patch-level changes: documentation polish, small bug fixes, clearer errors,
  or output wording that does not change artifact contracts.
- Minor-level changes: new local simulation features, new generated artifacts,
  changed CSV/report contracts, or meaningful API additions.
- Major-level changes: reserved for a future version that changes the project
  shape substantially.

Version changes should update `CHANGELOG.md` and any reviewer docs affected by
new commands, outputs, configs, or validation steps.

## Current Release Boundary

Version `0.1.0` is the local-only MVP:

- one-command CLI demo
- deterministic YAML configs
- synthetic market simulation
- Black-Scholes pricing and Greeks
- fake execution, portfolio state, and risk validation
- loop-vs-vectorized benchmark
- CSV, PNG, JSON, copied-config, and Markdown outputs
- pytest and ruff local validation path

It intentionally excludes live market data, brokerage integration, real trades,
databases, dashboards, SaaS features, cloud deployment, and investment advice.
