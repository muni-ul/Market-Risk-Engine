# PyRiskLab Final Review Checklist

Use this checklist when you are ready to do the last local verification pass before adding PyRiskLab to a resume, portfolio, or GitHub profile.

## Clean Repo State

- Confirm the working tree is clean with `git status`.
- Confirm generated run folders are not staged or committed.
- Confirm `results/.gitkeep` is still present.

## Local Validation

Run these from the repository root after installing dependencies:

```bash
pytest
ruff check .
python -m pyrisklab run --config configs/demo.yaml --overwrite
python -m pyrisklab run --config configs/risk_stress.yaml --overwrite
```

The main demo should print the seven progress steps and create `results/demo_run/`. The risk-stress demo should create blocked simulated orders and readable risk events without making trading or profitability claims.

## Demo Output Inspection

Open `results/demo_run/` and confirm these files exist:

- `benchmark.csv`
- `config_used.yaml`
- `drawdown.png`
- `greeks.png`
- `greeks_history.csv`
- `market_path.csv`
- `market_path.png`
- `option_price.png`
- `orders.csv`
- `portfolio_history.csv`
- `portfolio_value.png`
- `pricing_history.csv`
- `risk_events.csv`
- `run_metadata.json`
- `signals.csv`
- `summary_report.md`
- `trades.csv`

In `summary_report.md`, check that the report includes:

- Simulation-only language
- Market, option, Greeks, strategy, portfolio, execution, risk, benchmark, generated-artifact, run-metadata, and limitations sections
- Approved, blocked, and skipped simulated-order counts
- Benchmark assumptions and numerical-equivalence result
- Run metadata notes pointing to `run_metadata.json`

In `run_metadata.json`, check that it includes:

- `config_sha256`
- `benchmark_settings`
- `csv_row_counts`
- `order_status_counts`
- `expected_artifacts`
- `generated_artifacts`
- `generated_artifact_sizes_bytes`

## GitHub Presentation

- README explains the project in the first 30 seconds.
- README frames the project as Python simulation, automation, testing, and performance tooling.
- README clearly says this is simulation only, not a trading bot, not live market data, not brokerage integration, and not investment advice.
- README links to `docs/REVIEWER_GUIDE.md`, `docs/SAMPLE_OUTPUT.md`, `docs/sample_outputs/`, `docs/sample_outputs/artifact_manifest.md`, `docs/PORTFOLIO_CASE_STUDY.md`, and this checklist.
- Resume bullets match what the project actually implements.

## Resume Readiness

Use the project when you can confidently say:

> I built a local Python simulation engine with deterministic configs, a CLI pipeline, NumPy/SciPy numerical code, pandas outputs, fake execution, risk validation, pytest coverage, benchmark reporting, and reproducible CSV/PNG/Markdown artifacts.

Keep the interview framing focused on software engineering: clean modules, validation, deterministic runs, state management, generated artifacts, and performance-aware design.
