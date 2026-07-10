# TECH_STACK_AND_ARCHITECTURE.md

# PyRiskLab — Tech Stack and Architecture

## Source Inputs

[Confirmed] This architecture document is based on two planning documents: `PROJECT_SELECTION_BRIEF.md` and `PROJECT_MASTER_BLUEPRINT.md`.

[Confirmed] The selected project is **PyRiskLab**, a local Python options-pricing and risk-simulation engine.

[Confirmed] The project is intended to demonstrate Python software engineering, numerical computing, testing, reproducible local execution, and performance-aware design.

[Confirmed] The project is **not** a SaaS product, not a real trading bot, not an investment app, and not a live brokerage integration.

[Decision] The stack should prioritize a finished, clean, local Python engineering tool over a flashy dashboard or complex infrastructure.

---

## 1. Target Role Interpretation

### 1.1 Role this project should support

[Confirmed] The strongest target role is **Software Engineering Intern — Python Simulation, Automation, Testing, and Performance Tooling**.

[Confirmed] Secondary fits include data engineering intern, test automation intern, performance tools intern, and quant/financial engineering intern only when the target company is finance-related.

[Decision] For AMD-like software roles, the best positioning is **Python tooling and performance-aware engineering**, not finance, SaaS, or trading.

[Decision] The repo should communicate this story:

> PyRiskLab uses options pricing as the domain, but the real project is a local Python simulation system with clean architecture, deterministic configs, tests, vectorized computation, risk validation, benchmarking, and reproducible reports.

### 1.2 Skills the stack should prove

[Decision] The stack should prove these skills clearly:

- Python package structure using a real `src/` layout.
- CLI-based local tool execution.
- Config-driven reproducibility.
- NumPy vectorization.
- pandas data pipelines.
- SciPy numerical/statistical usage.
- matplotlib report-ready charts.
- Clean dataclass-based domain models.
- pytest-based correctness testing.
- ruff-based formatting and linting.
- Explicit error handling through custom exceptions.
- Loop-versus-vectorized benchmarking.
- Clear generated outputs in `results/`.

[Decision] The stack should not distract from the main goal by adding login, cloud deployment, a web API, a database, payments, real trading, or complex ML.

---

## 2. Stack Options

## Option A — Lean Professional Python CLI Engine

### Stack

[Decision] This option uses a local-first Python CLI with a simple dependency set.

**Language**

- [Decision] Python 3.11+ or Python 3.12.

**Frontend / UI**

- [Decision] No web frontend for MVP.
- [Decision] CLI interface through Python standard-library `argparse`.
- [Decision] Markdown summary reports and PNG charts serve as the reviewable user interface.

**Backend / API**

- [Decision] No web backend.
- [Decision] Internal Python package modules under `src/pyrisklab/`.
- [Decision] A `pipeline.py` or `runner.py` module coordinates the end-to-end run.

**Database / storage**

- [Decision] No database for MVP.
- [Decision] Store run artifacts as CSV, YAML, Markdown, and PNG files under `results/<run_name>/`.

**Data / numerical tools**

- [Decision] NumPy for GBM simulation, vectorized pricing inputs, and benchmark arrays.
- [Decision] pandas for market paths, pricing history, Greeks history, trades, portfolio history, risk events, and benchmark tables.
- [Decision] SciPy for normal distribution functions used in Black-Scholes pricing and Greeks.
- [Decision] matplotlib for saved charts.
- [Decision] PyYAML for config files.

**Testing tools**

- [Decision] pytest for unit tests.
- [Decision] ruff for formatting and linting.
- [Decision] pyright or mypy as optional type checking after MVP is working.

**Local development tools**

- [Decision] VS Code.
- [Decision] `.venv` virtual environment.
- [Decision] `requirements.txt` for simple installation.
- [Decision] `pyproject.toml` for package metadata and tool configuration.

### Why this stack fits

[Decision] This is the best fit for the stated project because it keeps Python as the main focus while still looking like real software.

[Decision] It gives strong evidence of modular design, tests, reproducible outputs, numerical programming, and performance awareness without adding unnecessary infrastructure.

[Decision] It is the easiest option to finish cleanly while still producing a professional GitHub repo.

### Risks

[Assumption] The CLI/report experience may look less visually flashy than a dashboard if screenshots are not prepared well.

[Decision] This risk is handled by making the generated charts, summary report, terminal output, README screenshots, and architecture diagram polished.

[Assumption] Manual config validation with dataclasses requires discipline.

[Decision] This risk is handled by adding focused tests for config loading and validation errors.

### Job-market signal

[Decision] Strong signal for Python tooling, automation, testing, simulation, data processing, debugging, and performance-aware software engineering.

[Decision] Good fit for internships where reviewers want evidence that the project is more than a notebook.

---

## Option B — Python Engine + Streamlit Local Dashboard

### Stack

[Decision] This option adds a local dashboard on top of the Python engine.

**Language**

- [Decision] Python 3.11+ or Python 3.12.

**Frontend / UI**

- [Decision] Streamlit for a local dashboard.
- [Decision] Plotly for interactive charts.
- [Decision] CLI remains available for reproducible runs.

**Backend / API**

- [Decision] No web API.
- [Decision] The Streamlit app imports the same engine modules used by the CLI.

**Database / storage**

- [Decision] CSV and Markdown outputs remain the primary storage.
- [Decision] Optional SQLite only if comparing many historical runs becomes important.

**Data / numerical tools**

- [Decision] NumPy, pandas, SciPy, PyYAML.
- [Decision] matplotlib for report PNGs.
- [Decision] Plotly for dashboard-only interactive visuals.

**Testing tools**

- [Decision] pytest for engine logic.
- [Decision] ruff for formatting and linting.
- [Decision] Minimal dashboard testing only; avoid spending MVP time testing Streamlit UI details.

**Local development tools**

- [Decision] VS Code.
- [Decision] `.venv`.
- [Decision] `requirements.txt`.
- [Decision] `pyproject.toml`.

### Why this stack fits

[Decision] This option improves demo quality because recruiters can click through a dashboard instead of only opening files.

[Decision] It can make the project feel more visually impressive if the backend is already complete.

### Risks

[Decision] This option risks becoming a dashboard project instead of a software engineering project.

[Decision] Streamlit can hide weak architecture if the engine is not built first.

[Decision] More dependencies increase setup complexity.

[Decision] Dashboard polish can consume time that should go to tests, architecture, and correctness.

### Job-market signal

[Decision] Stronger visual signal than Option A.

[Decision] Weaker engineering signal if the dashboard becomes the center of the repo.

[Decision] Best as a future enhancement after the CLI engine is complete.

---

## Option C — Performance-Heavy Python + Numba / Optional Native Extension

### Stack

[Decision] This option emphasizes performance engineering and benchmarking.

**Language**

- [Decision] Python 3.11+ or Python 3.12.
- [Decision] Optional C++ only as a stretch benchmark extension.

**Frontend / UI**

- [Decision] CLI-first.
- [Decision] Markdown benchmark report and PNG charts.

**Backend / API**

- [Decision] Internal Python package modules.
- [Decision] Optional Numba-accelerated pricing or simulation functions.
- [Decision] Optional pybind11 C++ pricing kernel only after MVP.

**Database / storage**

- [Decision] CSV and Markdown for MVP outputs.
- [Decision] No database.

**Data / numerical tools**

- [Decision] NumPy, pandas, SciPy, matplotlib, PyYAML.
- [Decision] Numba for selected hot paths only after baseline vectorization is correct.
- [Decision] Optional pytest-benchmark after the basic benchmark works.

**Testing tools**

- [Decision] pytest.
- [Decision] ruff.
- [Decision] pyright or mypy optional.
- [Decision] pytest-benchmark optional after MVP.

**Local development tools**

- [Decision] VS Code.
- [Decision] `.venv`.
- [Decision] `requirements.txt`.
- [Decision] `pyproject.toml`.
- [Decision] Optional compiler toolchain only if adding native extension later.

### Why this stack fits

[Decision] This option gives the strongest performance engineering discussion if completed cleanly.

[Decision] It aligns well with roles involving simulation, profiling, numerical computation, and performance tooling.

### Risks

[Decision] This option has the highest setup risk.

[Decision] Native extensions and acceleration libraries can introduce debugging problems that distract from finishing the core project.

[Decision] If the performance layer is unfinished, it can make the project look overbuilt.

### Job-market signal

[Decision] Potentially excellent for performance-oriented roles.

[Decision] Too risky for Version 1 because the project must first prove correctness, architecture, and reproducible execution.

---

## 3. Stack Scoring Table

[Decision] Scores are from 1 to 10, where 10 is strongest for this specific project and target role.

| Category | Option A: Lean Professional Python CLI | Option B: Python + Streamlit Dashboard | Option C: Performance-Heavy Python |
|---|---:|---:|---:|
| Target role alignment | 9 | 7 | 9 |
| Technical depth | 8 | 8 | 10 |
| Local-run simplicity | 10 | 7 | 5 |
| Maintainability | 9 | 7 | 6 |
| Testability | 9 | 7 | 7 |
| Demo value | 8 | 10 | 8 |
| Recruiter readability | 8 | 9 | 7 |
| Interviewer discussion value | 9 | 8 | 10 |
| **Total / 80** | **70** | **63** | **62** |

### Scoring interpretation

[Decision] Option A wins because it has the best balance of finishability, engineering signal, local simplicity, maintainability, and interview value.

[Decision] Option B has the best visual demo potential but risks shifting attention away from the Python engine.

[Decision] Option C has the highest technical ceiling but is too risky for the first finished version.

---

## 4. Final Stack Decision

## Recommended stack

[Decision] Use **Option A: Lean Professional Python CLI Engine** for Version 1.

### Final Version 1 stack

**Core language and runtime**

- [Decision] Python 3.11+ or Python 3.12.

**Project structure**

- [Decision] `src/` package layout.
- [Decision] `pyproject.toml` for tool configuration and package metadata.
- [Decision] `requirements.txt` for simple local installation.

**CLI**

- [Decision] `argparse` for the MVP CLI.
- [Decision] Keep the command compatible with:

```bash
python -m pyrisklab run --config configs/demo.yaml
```

**Numerical and data stack**

- [Decision] NumPy.
- [Decision] pandas.
- [Decision] SciPy.
- [Decision] matplotlib.
- [Decision] PyYAML.

**Testing and quality tools**

- [Decision] pytest.
- [Decision] ruff.
- [Decision] pyright or mypy optional after the MVP works.

**Storage**

- [Decision] YAML configs.
- [Decision] CSV data outputs.
- [Decision] PNG chart outputs.
- [Decision] Markdown summary report.
- [Decision] No database for Version 1.

**Performance**

- [Decision] Built-in `time.perf_counter()` benchmarking for loop-based versus vectorized Black-Scholes pricing.
- [Decision] Numba is delayed until after the baseline engine is complete.

## Why this is the best choice

[Decision] This stack directly supports the strongest project story: a complete local Python simulation engine with tests, deterministic execution, clear outputs, and benchmark evidence.

[Decision] It avoids generic tutorial energy because the project is not just one formula or one notebook; it includes config loading, market simulation, pricing, Greeks, fake execution, portfolio state, risk validation, reporting, and benchmarking.

[Decision] It is simple enough to finish in VS Code without cloud setup, database setup, Docker setup, account setup, or frontend debugging.

[Decision] It creates strong interview discussion around architecture, numerical correctness, validation, state transitions, risk rules, deterministic seeds, and vectorization.

## Alternatives rejected and why

[Decision] Streamlit is rejected for Version 1 because it can make the project visually attractive while weakening focus on backend correctness and architecture.

[Decision] Plotly is rejected for Version 1 because static matplotlib charts are enough for README screenshots and generated reports.

[Decision] SQLite is rejected for Version 1 because all data is generated per run and CSV files are easier for reviewers to inspect.

[Decision] DuckDB is rejected for Version 1 because the data size is small and query analytics are not the core skill signal.

[Decision] Numba is rejected for Version 1 because baseline vectorized NumPy should be correct and benchmarked before acceleration is added.

[Decision] pybind11/C++ is rejected for Version 1 because compiler setup adds friction and makes the project less local-simple.

[Decision] FastAPI is rejected because this is not a web service and does not need HTTP boundaries.

[Decision] React is rejected because a frontend would not strengthen the target Python simulation/tooling signal enough to justify the scope.

[Decision] Docker is rejected for Version 1 because a normal Python virtual environment is simpler and better aligned with a local VS Code project.

## What this stack proves to employers

[Decision] This stack proves the user can build a real Python project instead of a loose script.

[Decision] It proves the user can write modular numerical code, validate assumptions, test edge cases, manage state, produce clean outputs, and measure performance.

[Decision] It proves the user understands scope control by refusing unnecessary SaaS, cloud, frontend, and real-trading features.

---

## 5. Architecture Plan

## 5.1 Folder structure

[Decision] Use this repo structure:

```text
pyrisklab/
  README.md
  pyproject.toml
  requirements.txt
  .gitignore
  .env.example

  configs/
    demo.yaml

  docs/
    PROJECT_SELECTION_BRIEF.md
    PROJECT_MASTER_BLUEPRINT.md
    TECH_STACK_AND_ARCHITECTURE.md
    ARCHITECTURE.md

  src/
    pyrisklab/
      __init__.py
      __main__.py
      cli.py
      pipeline.py
      config.py
      models.py
      market.py
      pricing.py
      greeks.py
      strategy.py
      execution.py
      portfolio.py
      risk.py
      reporting.py
      benchmark.py
      exceptions.py

  tests/
    test_config.py
    test_market.py
    test_pricing.py
    test_greeks.py
    test_strategy.py
    test_execution.py
    test_portfolio.py
    test_risk.py
    test_reporting.py
    test_benchmark.py

  results/
    .gitkeep
```

[Decision] `docs/ARCHITECTURE.md` can later contain a shorter human-friendly version, while this file records the stack decision and full plan.

[Decision] `results/` should exist in Git with `.gitkeep`, but generated run folders should usually be ignored unless intentionally committing small sample outputs.

---

## 5.2 Main modules

### `__main__.py`

[Decision] Allows the project to run through:

```bash
python -m pyrisklab run --config configs/demo.yaml
```

[Decision] It should delegate to `cli.py` and contain almost no business logic.

### `cli.py`

[Decision] Owns command-line parsing and user-facing progress messages.

Responsibilities:

- Parse `run` command.
- Accept `--config`.
- Accept `--overwrite`.
- Call `pipeline.run_simulation(...)`.
- Catch expected project exceptions.
- Print clean error messages.

### `pipeline.py`

[Decision] Coordinates the full simulation workflow.

Responsibilities:

- Load config.
- Prepare output directory.
- Call market simulation.
- Call pricing and Greeks engines.
- Run strategy.
- Validate orders through risk manager.
- Execute allowed trades.
- Update portfolio snapshots.
- Run benchmark.
- Generate reports.
- Return a `RunResult`.

[Decision] This module prevents `cli.py` from becoming too large.

### `config.py`

[Decision] Loads and validates YAML configs.

Responsibilities:

- Read `configs/demo.yaml`.
- Validate required sections.
- Convert raw dictionaries into dataclasses.
- Raise `ConfigError` for invalid user inputs.

### `models.py`

[Decision] Contains core dataclasses and typed domain objects.

Recommended models:

- `RunConfig`
- `MarketConfig`
- `OptionConfig`
- `StrategyConfig`
- `RiskConfig`
- `BenchmarkConfig`
- `OptionContract`
- `Signal`
- `Order`
- `Trade`
- `Position`
- `PortfolioSnapshot`
- `RiskEvent`
- `BenchmarkResult`
- `RunResult`

[Decision] Use plain dataclasses for MVP.

[Decision] Do not use pydantic unless manual validation becomes painful.

### `market.py`

[Decision] Generates synthetic market paths.

Responsibilities:

- Implement geometric Brownian motion path generation.
- Use deterministic random seeds.
- Return pandas DataFrames.
- Validate initial price, volatility, number of steps, and number of paths.

### `pricing.py`

[Decision] Implements Black-Scholes option pricing.

Responsibilities:

- Price European calls.
- Price European puts.
- Support scalar and vectorized inputs.
- Handle expiry through intrinsic value.
- Validate option type, strike, volatility, underlying price, and time to expiry.

### `greeks.py`

[Decision] Calculates option Greeks.

Responsibilities:

- Delta.
- Gamma.
- Vega.
- Theta.
- Rho.
- Vectorized calculations over the simulated path.
- Edge-case handling near expiry or zero volatility.

### `strategy.py`

[Decision] Contains one intentionally simple strategy.

Responsibilities:

- Read pricing and Greeks history.
- Generate buy, sell, or hold signals.
- Keep strategy simple enough that the project does not become about profitability.

### `execution.py`

[Decision] Converts approved orders into fake trades.

Responsibilities:

- Fill orders deterministically at simulated option price.
- Apply optional fixed commission.
- Reject structurally invalid orders before portfolio update.

### `portfolio.py`

[Decision] Owns stateful portfolio accounting.

Responsibilities:

- Track cash.
- Track positions.
- Apply trades.
- Calculate current position value.
- Calculate realized and unrealized P&L if implemented.
- Calculate total value.
- Calculate drawdown.
- Produce `PortfolioSnapshot` records.

### `risk.py`

[Decision] Owns pre-trade and portfolio-level risk checks.

Responsibilities:

- Enforce max position quantity.
- Enforce max trade notional.
- Enforce max drawdown.
- Enforce max loss.
- Return structured validation results.
- Create `RiskEvent` objects for blocked trades or breached limits.

### `reporting.py`

[Decision] Owns all generated artifacts.

Responsibilities:

- Save CSV files.
- Save PNG charts.
- Copy `config_used.yaml` into the run folder.
- Generate `summary_report.md`.
- Handle empty trades or empty risk events gracefully.

### `benchmark.py`

[Decision] Benchmarks loop-based versus vectorized pricing.

Responsibilities:

- Generate a fixed set of prices.
- Run a loop implementation.
- Run the vectorized implementation.
- Measure runtime with `time.perf_counter()`.
- Save `benchmark.csv`.
- Report speedup honestly.

### `exceptions.py`

[Decision] Contains custom exception classes.

Recommended exceptions:

- `PyRiskLabError`
- `ConfigError`
- `PricingError`
- `MarketSimulationError`
- `PortfolioError`
- `RiskError`
- `ReportingError`
- `RunError`

---

## 5.3 Data flow

[Decision] The app should follow this data flow:

```text
configs/demo.yaml
  -> config.load_config()
  -> RunConfig dataclass
  -> pipeline.run_simulation()
  -> market.simulate_gbm_path()
  -> market_path DataFrame
  -> pricing.black_scholes_price()
  -> greeks.calculate_greeks()
  -> pricing_history / greeks_history DataFrames
  -> strategy.generate_signals()
  -> Order objects
  -> risk.validate_order()
  -> execution.execute_order()
  -> Trade objects
  -> portfolio.apply_trade()
  -> PortfolioSnapshot records
  -> benchmark.run_pricing_benchmark()
  -> reporting.write_results()
  -> results/<run_name>/
```

[Decision] The core run should be deterministic when the same config and seed are used.

[Decision] Pricing, Greeks, and market simulation should be mostly pure functions.

[Decision] Portfolio and risk manager should be the main stateful components.

---

## 5.4 State flow

[Decision] State should be explicit and testable.

```text
RunConfig
  controls all deterministic run settings

Portfolio
  owns mutable cash, positions, realized P&L, peak value, and snapshots

RiskManager
  owns risk limits and blocked-trading state after major breaches

DataFrames
  carry generated history tables, not hidden app state
```

[Decision] Avoid module-level global variables.

[Decision] Avoid passing giant untyped dictionaries through the system after config validation.

[Decision] Use dataclasses for long-lived domain objects and DataFrames for time-series outputs.

---

## 5.5 API / service boundaries

[Decision] Do not create a web API in Version 1.

[Decision] Use internal service boundaries instead:

```python
def run_simulation(config_path: str, overwrite: bool = False) -> RunResult:
    ...
```

[Decision] The CLI should call this internal service function.

[Decision] Future Streamlit or API layers should call the same internal service function instead of duplicating logic.

---

## 5.6 Local database / storage plan

[Decision] Use file-based storage for Version 1.

Expected output:

```text
results/demo_run/
  config_used.yaml
  market_path.csv
  pricing_history.csv
  greeks_history.csv
  trades.csv
  portfolio_history.csv
  risk_events.csv
  benchmark.csv
  market_path.png
  option_price.png
  greeks.png
  portfolio_value.png
  drawdown.png
  summary_report.md
```

[Decision] CSV is preferred because it is easy to inspect, easy to test, and natural for pandas.

[Decision] Markdown is preferred for the summary report because it is readable on GitHub and does not need a browser app.

[Decision] PNG charts are preferred for README screenshots and portfolio presentation.

[Decision] SQLite should be delayed until repeated historical run comparison becomes genuinely useful.

---

## 5.7 Error handling approach

[Decision] Validate early at system boundaries.

Validation boundaries:

- Config loading.
- CLI arguments.
- Market simulation inputs.
- Option pricing inputs.
- Greeks inputs.
- Order creation.
- Risk validation.
- Portfolio state updates.
- Output folder creation.

[Decision] Expected user mistakes should raise custom exceptions with clear messages.

Examples:

```text
ConfigError: market.volatility must be >= 0. Received -0.20.
ConfigError: option.option_type must be 'call' or 'put'. Received 'calls'.
RunError: results/demo_run already exists. Use --overwrite or choose a different run_name.
PricingError: strike must be greater than 0. Received 0.
PortfolioError: cannot sell 3 contracts when current position is 1.
```

[Decision] `cli.py` should catch `PyRiskLabError` and print readable messages without a scary stack trace.

[Decision] Unexpected programmer errors can still show stack traces during development.

---

## 5.8 Testing approach

[Decision] Use pytest from the beginning.

[Decision] Tests should focus on logic that can break, not on superficial coverage percentages.

### Minimum tests

**`test_config.py`**

- [Decision] Valid config loads.
- [Decision] Missing required section fails.
- [Decision] Invalid volatility fails.
- [Decision] Invalid option type fails.
- [Decision] Invalid risk limit fails.

**`test_market.py`**

- [Decision] Same seed produces same path.
- [Decision] Different seed can produce different path.
- [Decision] Zero volatility behaves predictably.
- [Decision] Negative volatility fails.
- [Decision] Nonpositive initial price fails.

**`test_pricing.py`**

- [Decision] Known call price test.
- [Decision] Known put price test.
- [Decision] Put-call parity test.
- [Decision] Expiry intrinsic value test.
- [Decision] Invalid option type fails.
- [Decision] Vectorized input returns expected shape.

**`test_greeks.py`**

- [Decision] Greeks return finite values for normal inputs.
- [Decision] Call delta is within a reasonable range.
- [Decision] Put delta is within a reasonable range.
- [Decision] Near-expiry handling does not crash.

**`test_execution.py`**

- [Decision] Valid order creates trade.
- [Decision] Zero quantity order fails.
- [Decision] Negative quantity order fails.

**`test_portfolio.py`**

- [Decision] Buy trade decreases cash and increases position.
- [Decision] Sell trade increases cash and decreases position.
- [Decision] Cannot sell more than held unless shorting is explicitly enabled.
- [Decision] Portfolio total value updates correctly.
- [Decision] Drawdown updates correctly.

**`test_risk.py`**

- [Decision] Position limit blocks oversized order.
- [Decision] Trade notional limit blocks expensive order.
- [Decision] Max drawdown breach stops future trades.
- [Decision] Allowed trade passes.
- [Decision] Risk event includes a readable reason.

**`test_reporting.py`**

- [Decision] Output directory is created.
- [Decision] Empty trades still produce `trades.csv`.
- [Decision] Empty risk events still produce `risk_events.csv`.
- [Decision] Summary report is created.

**`test_benchmark.py`**

- [Decision] Benchmark returns loop and vectorized rows.
- [Decision] Benchmark saves a CSV.
- [Decision] Speedup calculation handles zero or tiny runtimes safely.

---

## 6. Local Development Plan

## 6.1 Install dependencies

[Decision] Use a normal virtual environment for local setup.

Windows PowerShell:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

[Decision] Recommended `requirements.txt` for MVP:

```text
numpy
pandas
scipy
matplotlib
pyyaml
pytest
ruff
```

[Decision] Optional later dependencies:

```text
pyright
mypy
numba
streamlit
plotly
pytest-benchmark
```

---

## 6.2 Run the app

[Decision] The main command should be:

```bash
python -m pyrisklab run --config configs/demo.yaml
```

[Decision] Add overwrite support:

```bash
python -m pyrisklab run --config configs/demo.yaml --overwrite
```

[Decision] Expected terminal flow:

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

---

## 6.3 Seed data

[Decision] Use `configs/demo.yaml` as the deterministic seed data.

Recommended demo config:

```yaml
run_name: demo_run
seed: 42
output_dir: results

market:
  initial_price: 100.0
  drift: 0.05
  volatility: 0.20
  trading_days: 252
  steps: 252
  paths: 1

option:
  underlying_symbol: SIM_STOCK
  symbol: CALL_105
  option_type: call
  strike: 105.0
  risk_free_rate: 0.04
  volatility: 0.20
  days_to_expiry: 90

strategy:
  name: simple_delta_rule
  buy_delta_below: 0.45
  sell_delta_above: 0.70
  trade_quantity: 1

risk:
  starting_cash: 10000.0
  max_position_quantity: 10
  max_trade_notional: 2500.0
  max_drawdown_pct: 0.15
  max_loss_pct: 0.10

benchmark:
  enabled: true
  num_prices: 100000
```

[Decision] Do not require internet access or external market data for seed data.

---

## 6.4 Run tests

[Decision] Test command:

```bash
pytest
```

[Decision] Optional verbose command:

```bash
pytest -v
```

[Decision] Lint command:

```bash
ruff check .
```

[Decision] Format command:

```bash
ruff format .
```

[Decision] Optional type check after MVP:

```bash
pyright
```

or:

```bash
mypy src
```

---

## 6.5 Reset local state

[Decision] Generated output should be disposable.

Reset command on macOS / Linux:

```bash
rm -rf results/demo_run
```

Reset command on Windows PowerShell:

```powershell
Remove-Item -Recurse -Force results/demo_run
```

[Decision] Safer reset command through the app can be added later, but it is not required for MVP.

[Decision] `--overwrite` should delete and recreate only the selected run folder, not the entire `results/` directory.

---

## 7. Minimum Professional Quality Rules

## 7.1 Secrets and environment variables

[Decision] Do not commit secrets.

[Decision] Version 1 should not need API keys.

[Decision] Include `.env.example` only to show professional hygiene.

Recommended `.env.example`:

```text
# PyRiskLab does not require secrets for the local MVP.
# Keep this file as a placeholder if future optional features need environment variables.
```

[Decision] Do not add live market data APIs in Version 1.

---

## 7.2 Input validation

[Decision] Validate config values before running the simulation.

[Decision] Validate all numerical fields that can cause broken math or confusing outputs.

Minimum validations:

- `market.initial_price > 0`
- `market.volatility >= 0`
- `market.steps > 0`
- `market.trading_days > 0`
- `market.paths >= 1`
- `option.option_type in {'call', 'put'}`
- `option.strike > 0`
- `option.volatility >= 0`
- `option.days_to_expiry >= 0`
- `risk.starting_cash > 0`
- `risk.max_position_quantity >= 0`
- `risk.max_trade_notional >= 0`
- `risk.max_drawdown_pct >= 0`
- `risk.max_loss_pct >= 0`
- `benchmark.num_prices > 0` when benchmark is enabled

---

## 7.3 Error clarity

[Decision] User-caused errors should be clear and actionable.

[Decision] Avoid dumping raw stack traces for normal config mistakes.

[Decision] Error messages should name the exact config field and the received bad value when practical.

---

## 7.4 Setup simplicity

[Decision] The project should run with a normal virtual environment and `pip install -r requirements.txt`.

[Decision] Do not require Docker, databases, cloud services, compilers, accounts, or API keys for MVP.

[Decision] Keep Windows support in mind because the project is being built in VS Code.

---

## 7.5 Maintainability

[Decision] Keep modules focused and small.

[Decision] Keep CLI thin and pipeline explicit.

[Decision] Keep pricing and market simulation mostly pure.

[Decision] Keep portfolio state inside the `Portfolio` object.

[Decision] Keep risk rules in `RiskManager`, not scattered across strategy, execution, and portfolio modules.

[Decision] Avoid premature abstractions such as plugin systems, strategy registries, user systems, or service containers.

---

## 7.6 Testing realism

[Decision] Do not chase perfect test coverage.

[Decision] Prioritize tests that prove correctness of pricing, Greeks, accounting, risk rules, config validation, and generated outputs.

[Decision] Add regression tests when bugs are found.

---

## 7.7 Reporting polish

[Decision] Every generated chart needs a readable title, axis labels, and units where relevant.

[Decision] Every CSV should have clear column names.

[Decision] The summary report should be understandable without reading the code.

[Decision] Empty trades and empty risk events should be treated as valid states, not failures.

---

## 8. Final Architecture Summary

[Decision] This section can be pasted into `docs/ARCHITECTURE.md`.

````markdown
# PyRiskLab Architecture

PyRiskLab is a local Python simulation engine for options pricing and portfolio risk analysis. It is designed as a command-line engineering tool, not a SaaS app, trading bot, or live brokerage integration.

The project uses a `src/pyrisklab/` package layout with focused modules for config loading, market simulation, Black-Scholes pricing, Greeks calculation, strategy signal generation, fake execution, portfolio accounting, risk validation, reporting, and benchmarking.

The main entry point is:

```bash
python -m pyrisklab run --config configs/demo.yaml
```

A run starts by loading a deterministic YAML config. The market module generates a synthetic geometric Brownian motion price path using NumPy. The pricing and Greeks modules calculate option values and sensitivities over that path using vectorized numerical code. The strategy module emits simple buy/sell/hold signals. The risk manager validates proposed orders before execution. Approved orders become fake trades, and the portfolio module updates cash, positions, total value, and drawdown over time.

All outputs are saved locally under `results/<run_name>/`. The expected artifacts are CSV files, PNG charts, a copied config file, benchmark results, risk logs, trade logs, portfolio history, and a Markdown summary report.

The architecture intentionally avoids a database, web API, dashboard, cloud deployment, user accounts, live market data, and real trading. CSV and Markdown outputs are used because the data is generated per run, easy to inspect, and simple to reproduce.

Testing is handled with pytest. The most important tests cover config validation, deterministic market simulation, Black-Scholes pricing, Greeks, portfolio accounting, risk-rule blocking, reporting outputs, and loop-versus-vectorized benchmark behavior.

The main stateful components are `Portfolio` and `RiskManager`. Pricing, Greeks, and market simulation are kept mostly pure and vectorized. The CLI is intentionally thin and delegates orchestration to a pipeline module.

The goal of the architecture is to prove Python software engineering skill through clean modules, deterministic execution, numerical correctness, explicit validation, reproducible reports, and performance-aware design.
````

---

## Final Move-On Checklist

[Decision] The final stack is justified by the target role.

[Decision] Alternatives were compared instead of ignored.

[Decision] Local setup is simple and does not require cloud, database, Docker, accounts, or compilers.

[Decision] The architecture is understandable from the folder structure.

[Decision] The testing approach is realistic and focused on meaningful correctness.

[Decision] The next implementation step is to create the repo skeleton, add `configs/demo.yaml`, add a minimal CLI, and make one placeholder pytest test pass before building the math-heavy modules.
