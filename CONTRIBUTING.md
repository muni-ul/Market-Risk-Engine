# Contributing

PyRiskLab is a local Python simulation project, so development should keep the
repo easy to clone, inspect, and run without external services.

## Local Setup

```bash
python -m venv .venv
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

On Windows PowerShell, activate the environment with:

```bash
.venv\Scripts\activate
```

## Development Checks

Before presenting or submitting changes, run:

```bash
pytest
ruff check .
python -m pyrisklab run --config configs/demo.yaml --overwrite
python -m pyrisklab run --config configs/risk_stress.yaml --overwrite
```

You can also run the local helper, which wraps the same reviewer validation sequence:

```bash
python scripts/local_verify.py
```

Preview the selected helper commands without running them:

```bash
python scripts/local_verify.py --list
```

The main demo should create `results/demo_run/`; the risk-stress demo should
create blocked simulated orders and readable risk events.

## Scope Rules

- Keep the project local and file-based.
- Do not add live market data, brokerage APIs, real order execution, dashboards,
  SaaS features, databases, cloud deployment, payments, accounts, or investment
  advice.
- Prefer deterministic configs, seeded simulation, focused modules, readable
  errors, and inspectable CSV/PNG/JSON/Markdown outputs.
- Keep formatting consistent with `.editorconfig`, `.gitattributes`, and the
  Ruff settings in `pyproject.toml`.
- Keep generated run outputs out of git; `results/.gitkeep` is the only tracked
  file expected under `results/`.

## Documentation Updates

When behavior changes, update the relevant docs:

- `README.md` for the primary reviewer path.
- `docs/CONFIG_REFERENCE.md` for config fields.
- `docs/sample_outputs/` for output contracts.
- `CHANGELOG.md` for version-level project changes.
- `.github/ISSUE_TEMPLATE/bug_report.md` if issue-report expectations change.
- `.github/PULL_REQUEST_TEMPLATE.md` if review expectations change.
