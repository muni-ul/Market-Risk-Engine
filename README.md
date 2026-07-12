# PyRiskLab

PyRiskLab is a local Python simulation engine for options pricing and portfolio
risk analysis. It uses simulated market paths, Black-Scholes pricing, Greeks,
fake execution, risk controls, and reproducible reporting to demonstrate Python
software engineering, numerical computing, testing, and performance-aware
design.

It is not a trading bot and does not connect to real brokerage accounts.

## Best Reviewer Signal

PyRiskLab is strongest as a software-engineering portfolio project: one command
runs a deterministic local pipeline, validates inputs and risk rules, tracks
state transitions, benchmarks vectorized computation, and writes reproducible
CSV/PNG/Markdown/JSON artifacts.

## Quick Facts

- Local CLI project using a real `src/pyrisklab/` package layout
- Deterministic YAML configs and seeded synthetic market data
- NumPy, pandas, SciPy, matplotlib, pytest, and ruff
- CSV, PNG, Markdown, and benchmark outputs under `results/demo_run/`
- Simulation only: no live market data, brokerage integration, real trades, or
  investment advice

## What This Project Demonstrates

- Clean Python modules for config, pricing, Greeks, strategy, execution,
  portfolio, risk, reporting, and benchmarking
- Typed dataclasses and a packaged `py.typed` marker for type-aware tooling
- Stable programmatic entry point through `pyrisklab.run_simulation(...)` with
  a typed `ProgressCallback`
- Vectorized NumPy computation over a simulated market path
- pandas data pipelines and reproducible local artifacts
- SciPy-based Black-Scholes pricing for European calls and puts
- Stateful portfolio accounting with cash, positions, P&L, and drawdown
- Config-driven risk validation and readable blocked-order events
- pytest coverage for important formulas, state transitions, and outputs
- A benchmark comparing Python-loop pricing with vectorized NumPy pricing

## Reviewer Checklist

- Run one command: `python -m pyrisklab run --config configs/demo.yaml --overwrite`
- Inspect `results/demo_run/summary_report.md` for the simulation-only summary,
  risk/execution audit counts, benchmark evidence, metadata section, artifact
  list, and limitations
- Inspect `results/demo_run/run_metadata.json` for config SHA-256, benchmark
  settings, row counts, order status counts, expected/generated artifacts, and
  artifact byte sizes
- Inspect `orders.csv`, `risk_events.csv`, and `portfolio_history.csv` for
  stateful execution, risk validation, and portfolio accounting
- Run `pytest` and `ruff check .` when you want to validate the code locally

## Software Engineering Positioning

PyRiskLab uses options pricing as the domain, but the project is really about
building a reliable local Python engineering tool. For software internships at
AMD-like companies, the strongest signals are CLI automation, deterministic
configs, numerical simulation, vectorized computation, tests, debugging-friendly
errors, benchmark reporting, and technical documentation.

## Simulation Only

PyRiskLab does not place real trades, connect to brokerages, use live market
data, scrape options chains, provide investment advice, make profitability
claims, or require API keys, accounts, Docker, databases, or cloud services.

The finance domain is used to create interesting simulation, state-management,
validation, and performance problems.

## What It Does

The demo run loads `configs/demo.yaml`, simulates a synthetic stock path, prices
a configured option, calculates Greeks, generates simple fake delta-threshold
signals, validates proposed orders against risk rules, executes allowed
simulated trades, tracks portfolio value, runs a loop-vs-vectorized benchmark,
and writes local reports.

## What It Does Not Do

PyRiskLab does not do live trading, brokerage integration, market prediction,
SaaS user accounts, dashboards, payments, databases, cloud deployment, or
investment recommendations.

## Tech Stack

Python 3.11+, NumPy, pandas, SciPy, matplotlib, PyYAML, pytest, and ruff.

## Architecture

```mermaid
flowchart LR
    A["YAML config"] --> B["CLI"]
    B --> C["Simulation pipeline"]
    C --> D["Pricing and Greeks"]
    D --> E["Fake strategy, risk, execution"]
    E --> F["Portfolio state"]
    F --> G["CSV, PNG, Markdown, JSON reports"]
    C --> H["Loop-vs-NumPy benchmark"]
    H --> G
```

```text
configs/demo.yaml
  -> CLI / config loader
  -> market simulation
  -> Black-Scholes pricing
  -> Greeks calculation
  -> simple fake strategy
  -> risk validation
  -> fake execution
  -> portfolio tracker
  -> benchmark
  -> reporting
  -> results/demo_run/
```

See `docs/ARCHITECTURE.md` for the longer design explanation.

For a documentation map, see `docs/README.md`.

For a quick implemented-vs-user-verified status summary, see
`docs/PROJECT_STATUS.md`.

For a quick evaluator walkthrough, see `docs/REVIEWER_GUIDE.md`.

For the ordered feature plan mapped to implementation evidence, see
`docs/features/README.md`.

For a requirement-by-requirement evidence map, see
`docs/REQUIREMENTS_TRACEABILITY.md`.

For a short demo and screenshot-capture path, see `docs/DEMO_WALKTHROUGH.md`.

For a module-level implementation reference, see `docs/API_REFERENCE.md`.

For field-by-field YAML settings, see `docs/CONFIG_REFERENCE.md`.

For defensive validation, error types, and edge-case handling, see
`docs/VALIDATION_NOTES.md`.

For benchmark assumptions, output columns, and speedup caveats, see
`docs/PERFORMANCE_NOTES.md`.

For local failure triage and `--debug` usage, see `docs/DEBUGGING_GUIDE.md`.

For a portfolio-style narrative of the problem, engineering decisions,
tradeoffs, and interview story, see `docs/PORTFOLIO_CASE_STUDY.md`.

For resume-ready project wording and bullet options, see `docs/RESUME_SNIPPETS.md`.

For the Version 1 release summary, see `CHANGELOG.md`.

For local development workflow and scope rules, see `CONTRIBUTING.md`.

For no-secrets and local-only security boundaries, see `SECURITY.md`.

Package metadata points to the repository, docs folder, and issue tracker for
standard GitHub navigation, and classifies the project as a console-based
testing, automation, quality, and performance-tooling portfolio project.

## Local Setup

Windows PowerShell:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The repo also includes a tiny root launcher so `python -m pyrisklab ...` works
from the repository root without an editable install. If you prefer a standard
editable package workflow, run `pip install -e .` after installing requirements;
that also exposes the shorter `pyrisklab` console command.

For package-style development, you can install the project and dev tools in one step:

```bash
pip install -e ".[dev]"
```

No API keys, accounts, or local secrets are required. `.env.example` is included
only to document that the Version 1 MVP runs without environment variables;
real `.env` files stay ignored.

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## One-Command Demo

```bash
python -m pyrisklab run --config configs/demo.yaml --overwrite
```

Expected terminal shape:

```text
[1/7] Loading config...
[2/7] Simulating market path...
[3/7] Pricing option and calculating Greeks...
[4/7] Running strategy, risk checks, and fake execution...
[5/7] Tracking portfolio value and drawdown...
[6/7] Running benchmark...
[7/7] Saving reports...
Done. Results saved to results/demo_run/
```

Quiet mode keeps progress output off while still printing the final result:

```bash
python -m pyrisklab run --config configs/demo.yaml --overwrite --quiet
```

Debug mode prints a traceback for expected project errors when you are
developing or diagnosing a failure:

```bash
python -m pyrisklab run --config configs/demo.yaml --debug
```

Show the installed package version:

```bash
python -m pyrisklab --version
```

After an editable install, the equivalent console command is:

```bash
pyrisklab run --config configs/demo.yaml --overwrite
```

Optional risk-control demo:

```bash
python -m pyrisklab run --config configs/risk_stress.yaml --overwrite
```

This uses the same synthetic market and strategy settings as the main demo, but
sets `risk.max_position_quantity: 0` and lowers `risk.max_trade_notional` so
proposed orders are blocked and written to `risk_events.csv`.

For the expected blocked-order output shape, see `docs/sample_outputs/risk_stress_demo.md`.

## Testing

```bash
pytest
```

For the test-suite rationale and coverage map, see `docs/TESTING_STRATEGY.md`.

Code quality check:

```bash
ruff check .
```

Local verification helper:

```bash
python scripts/local_verify.py
```

That helper runs the reviewer validation sequence locally: pytest, ruff, the
main demo, and the risk-stress demo. Use
`python scripts/local_verify.py --list` to preview the selected commands without
running them, or `python scripts/local_verify.py --only ruff --only demo` to
target a smaller subset. The helper is optional; the individual commands above
are still the source of truth.

Targeted examples:

```bash
pytest tests/test_pricing.py
pytest tests/test_portfolio.py
pytest tests/test_risk.py
```

## Generated Outputs

The demo creates:

```text
results/demo_run/
  config_used.yaml
  market_path.csv
  pricing_history.csv
  greeks_history.csv
  signals.csv
  orders.csv
  trades.csv
  portfolio_history.csv
  risk_events.csv
  benchmark.csv
  run_metadata.json
  market_path.png
  option_price.png
  greeks.png
  portfolio_value.png
  drawdown.png
  summary_report.md
```

The `results/demo_run/` folder is created locally after running the demo.
Generated outputs are not required before setup, and the repository keeps
`results/` mostly empty so reviewers can reproduce the run themselves.

`orders.csv` includes proposed simulated orders with risk approval status.
`summary_report.md` summarizes approved, blocked, and skipped simulated orders
so the risk/execution audit trail is visible without opening every CSV.
`run_metadata.json` records deterministic run context, the config SHA-256
digest, benchmark settings, row counts, order status counts, expected artifact
names, generated artifact names, and generated artifact byte sizes. Empty
`trades.csv`, `risk_events.csv`, or disabled-benchmark `benchmark.csv` files are
valid outcomes and still include headers.

## Benchmark

PyRiskLab benchmarks two Black-Scholes pricing approaches on the same
deterministic generated inputs:

- `python_loop`
- `numpy_vectorized`

The benchmark writes pricing assumptions, runtime, speedup, and
numerical-equivalence checks to `benchmark.csv`. Results vary by machine and
input size, so the benchmark demonstrates performance-aware engineering rather
than guaranteeing a fixed speedup.

If `benchmark.enabled` is false in a config, the report calls that out
explicitly and writes an empty `benchmark.csv` with the same stable file
contract.

For the full benchmark interpretation guide, see `docs/PERFORMANCE_NOTES.md`.

## Screenshots Or Sample Output References

For a committed example of the expected terminal and report shape, see
`docs/SAMPLE_OUTPUT.md`. For a short demo and screenshot-capture path, see
`docs/DEMO_WALKTHROUGH.md`. For more concrete output contracts, see
`docs/sample_outputs/`, including `docs/sample_outputs/artifact_manifest.md` for
the full generated file set, `docs/sample_outputs/chart_artifacts.md` for the
generated PNG chart set, and `docs/sample_outputs/risk_stress_demo.md` for the
risk-audit preset.

For the project story and resume/interview framing, see
`docs/REVIEWER_GUIDE.md`, `docs/PORTFOLIO_CASE_STUDY.md`, and
`docs/INTERVIEW_NOTES.md`.

For the final local verification pass and resume-ready gate, use
`docs/FINAL_REVIEW_CHECKLIST.md`.

After running the demo, open:

- `results/demo_run/market_path.png`
- `results/demo_run/option_price.png`
- `results/demo_run/greeks.png`
- `results/demo_run/portfolio_value.png`
- `results/demo_run/drawdown.png`
- `results/demo_run/summary_report.md`

These generated files are the screenshot-ready project artifacts.

## Resume And Interview Framing

Use PyRiskLab to describe a local Python engineering project, not a trading product:

- Built a modular Python simulation engine with deterministic YAML configs, CLI
  automation, NumPy/SciPy numerical code, pandas pipelines, fake execution, risk
  validation, and reproducible CSV/PNG/Markdown reports.
- Implemented performance-aware Black-Scholes benchmarking that compares
  Python-loop pricing against vectorized NumPy pricing, records pricing
  assumptions, and verifies numerical equivalence before reporting speedup.
- Added pytest coverage for config validation, pricing formulas, Greeks,
  execution state, portfolio accounting, risk rules, benchmark behavior,
  reporting contracts, packaging metadata, and repository hygiene.

## Troubleshooting

If `python -m pyrisklab` cannot import the package, run the command from the
repository root after installing dependencies, or use `pip install -e .` for an
editable install.

If `results/demo_run/` already exists, rerun with `--overwrite` or change
`run_name` in `configs/demo.yaml`.

Config mistakes are reported as clean project errors, for example:

```text
ConfigError: market.volatility must be >= 0. Received -0.20.
RunError: results/demo_run already exists. Use --overwrite or choose a different run_name.
```

For normal reviewer runs, PyRiskLab prints concise project errors without a
traceback. Add `--debug` when you want the traceback while developing.

If matplotlib behaves differently on a local machine, the project forces a
non-interactive PNG backend for report generation, so no desktop plotting window
is required.

## Project Structure

```text
configs/
docs/
src/pyrisklab/
tests/
results/
```

The core implementation lives in `src/pyrisklab/`, while `tests/` contains
focused pytest coverage for the main modules.

## License

MIT License. See `LICENSE`.

## Limitations

PyRiskLab uses one configured option contract and a simplified deterministic
fill model. It does not model order books, spreads, slippage, margin,
assignment, taxes, liquidity, real market microstructure, or real financial
risk.

## Future Improvements

- Add a curated `docs/assets/` screenshot set generated from a final local demo run.
- Extend the pipeline from one configured option contract to a small portfolio
  of contracts while preserving the same deterministic CLI workflow.
- Add optional Numba or multiprocessing benchmark variants only after the
  baseline loop-vs-NumPy comparison remains documented and reproducible.
- Add richer Markdown report styling and comparison tables while keeping the
  project local, dependency-light, and simulation-only.

## Resume Bullet

Built PyRiskLab, a modular local Python simulation engine using NumPy, pandas,
SciPy, matplotlib, and pytest to simulate market paths, price options, calculate
Greeks, execute fake trades, enforce risk controls, benchmark vectorized
computation, and export reproducible portfolio reports.

Performance/tooling version:

Developed a performance-aware Python simulation and analytics tool with
deterministic YAML configs, CLI automation, vectorized numerical computation,
pytest coverage, benchmark reporting, and reproducible local artifacts.
