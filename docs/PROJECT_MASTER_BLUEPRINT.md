# PROJECT_MASTER_BLUEPRINT.md

# PyRiskLab — Master Project Blueprint

## 1. Project Summary

### Project name

[Decision] **PyRiskLab**

### One-sentence description

[Decision] PyRiskLab is a local Python options-pricing and risk-simulation engine that generates synthetic market paths, prices options, calculates Greeks, simulates fake trades, enforces risk rules, benchmarks vectorized computation, and exports reproducible reports.

### Longer description

[Decision] PyRiskLab uses options pricing as the project domain, but the main purpose is to demonstrate strong Python software engineering. The project should run locally from VS Code through a command-line interface. It should generate simulated stock-price paths, price European call and put options using Black-Scholes, calculate option Greeks, run a simple rule-based fake strategy, track a simulated portfolio, apply risk controls, and save charts, CSVs, logs, and a summary report into a `results/` folder.

[Decision] The finished project should look like a small but professional engineering tool: modular package structure, deterministic configs, tests, clean error handling, benchmark evidence, and clear documentation.

[Confirmed] This is **not** a SaaS product, not a real trading bot, not an investment app, and not a live brokerage integration.

### Target role

[Decision] Primary target role:

**Software Engineering Intern — Python Simulation, Automation, Testing, and Performance Tooling**

[Decision] Secondary target roles:

- Data Engineering Intern, if the project emphasizes pandas pipelines, generated datasets, and reproducible outputs.
- Test Automation Intern, if the project emphasizes pytest, edge cases, deterministic runs, and validation.
- Performance Tools Intern, if the project emphasizes vectorization, benchmarking, profiling, and runtime comparisons.
- Quant/Financial Engineering Intern, only if applying to finance-related roles.

### Target reviewer

[Decision] The project should be understandable to three reviewer types:

1. **Recruiter**
   - Needs a quick, visual, impressive repo.
   - Should immediately understand what the project does from the README, screenshots, and demo output.

2. **Hiring manager**
   - Wants evidence that the project is scoped, finished, organized, and relevant to software work.
   - Should see clean architecture, tests, outputs, and a practical demo path.

3. **Technical interviewer**
   - Will ask how the system works.
   - Should be able to discuss pricing formulas, simulation design, state management, testing, edge cases, and vectorization tradeoffs.

### Main skill signal

[Decision] The main skill signal is:

**Building a complete local Python simulation tool with clean architecture, deterministic execution, tests, performance-aware numerical computing, and polished outputs.**

[Decision] The finance domain is only the vehicle. The actual employer-facing signal is software engineering discipline.

---

## 2. Why This Project Is Worth Building

### What it proves

[Decision] PyRiskLab proves that you can build more than a script or notebook. It shows:

- Python package structure.
- Numerical computation with NumPy and SciPy.
- Data processing with pandas.
- Command-line execution.
- Config-driven reproducibility.
- State management through portfolio and order objects.
- Risk-rule validation.
- Automated tests with pytest.
- Saved charts and reports.
- Performance awareness through loop-versus-vectorized benchmarking.
- Clear documentation and demo artifacts.

[Decision] This is stronger than a basic Black-Scholes calculator because the project includes a full simulation pipeline: inputs, model, decision logic, execution, portfolio state, risk checks, outputs, tests, and benchmark reporting.

### Why it is not just a tutorial clone

[Decision] A tutorial clone would usually stop at one pricing formula or one notebook chart.

[Decision] PyRiskLab becomes more original because it combines:

- Synthetic market-path generation.
- Vectorized option pricing.
- Greeks calculation.
- Fake execution and portfolio accounting.
- Risk controls that can block trades.
- Deterministic config files.
- Exported results.
- Tests for correctness.
- Benchmark comparisons.

[Decision] The project should be presented as an engineering system, not as “I copied a finance formula.”

### What makes it memorable

[Decision] The memorable part is the end-to-end demo:

> One command runs a complete simulation and generates a results folder containing market charts, option price charts, Greeks, trade logs, portfolio history, risk events, benchmark results, and a summary report.

[Decision] This makes the project easy for a reviewer to understand quickly.

[Decision] The strongest visual hook is a clean `results/demo_run/` folder with:

- `market_path.png`
- `option_price.png`
- `portfolio_value.png`
- `drawdown.png`
- `greeks.png`
- `trades.csv`
- `portfolio_history.csv`
- `risk_events.csv`
- `benchmark.csv`
- `summary_report.md`

### What interview questions it can create

[Decision] This project should create interview discussion around:

1. How geometric Brownian motion was used to simulate stock paths.
2. Why deterministic random seeds matter.
3. How Black-Scholes pricing works at a high level.
4. What assumptions Black-Scholes makes.
5. How Greeks measure option sensitivity.
6. How vectorized pricing differs from loop-based pricing.
7. How the fake execution system updates cash and positions.
8. How risk rules block invalid trades.
9. How pytest validates formulas and state transitions.
10. What edge cases were handled.
11. What was intentionally kept out of scope.
12. What would be improved in a second version.

[Decision] The best interview story is:

> I used a finance domain because it creates interesting numerical and state-management problems, but I built it like a software engineering tool: modular design, configs, tests, deterministic outputs, benchmarks, and clean reports.

---

## 3. User / Use Case

### Who would use it locally

[Assumption] The main local users are:

- A student or developer learning Python simulation systems.
- A software internship applicant demonstrating Python engineering.
- A technical reviewer evaluating code quality and project structure.
- A learner experimenting with option pricing, portfolio state, and risk controls.

[Confirmed] The project is meant to run locally, not as a hosted service.

### Main use case

[Decision] The main use case is:

**Run a deterministic local simulation that shows how option prices, Greeks, fake trades, portfolio value, and risk rules evolve over a synthetic market path.**

### Example scenario

[Assumption] A user opens the project in VS Code and runs:

```bash
python -m pyrisklab run --config configs/demo.yaml
```

The app then:

1. Loads the config.
2. Generates a synthetic stock price path.
3. Prices a selected call and put option over time.
4. Calculates Greeks.
5. Runs a simple fake trading strategy.
6. Executes allowed trades.
7. Blocks trades that violate risk rules.
8. Tracks portfolio value and drawdown.
9. Saves charts, CSVs, benchmark results, and a Markdown summary report.

### Demo story

[Decision] The demo story should be simple:

> PyRiskLab starts with a simulated stock path. It prices options across that path, calculates risk sensitivities, makes simple fake trade decisions, updates a portfolio, blocks trades that exceed risk limits, and produces a reproducible report. The whole project is local, deterministic, tested, and designed as a Python engineering system.

[Decision] The demo should not claim the strategy is profitable.

[Decision] The demo should not use real money or live market data.

---

## 4. Core Feature Set

[Decision] Version 1 should have exactly five core features. These features are connected enough to feel like one system, but limited enough to finish.

---

### Feature 1: Market Simulation and Config-Driven Runs

#### Description

[Decision] Generate synthetic stock price paths using geometric Brownian motion. The simulation should be controlled by a local YAML or JSON config file.

#### Why it matters for the project

[Decision] This gives the project a realistic input layer without depending on external APIs or live market data.

[Decision] Simulated data keeps the project reproducible, offline-friendly, and safe to run locally.

#### Skill it demonstrates

- NumPy vectorization.
- Random number generation.
- Deterministic seeds.
- Config parsing.
- Clean function design.
- Data validation.

#### User flow

1. User edits `configs/demo.yaml`.
2. User runs the CLI command.
3. App loads config values such as initial price, drift, volatility, time horizon, steps, and random seed.
4. App generates one or more synthetic price paths.
5. App saves the path to `results/demo_run/market_path.csv`.
6. App saves a chart to `results/demo_run/market_path.png`.

#### Data needed

[Decision] Minimum config fields:

```yaml
run_name: demo_run
seed: 42

market:
  initial_price: 100.0
  drift: 0.05
  volatility: 0.20
  trading_days: 252
  steps: 252
  paths: 1
```

#### UI/UX requirements

[Decision] Since this is a local project, the main UX is the CLI and generated report.

CLI should print readable progress messages:

```text
Loaded config: configs/demo.yaml
Generated market path: 252 steps
Saved market_path.csv
Saved market_path.png
```

[Decision] Output files should be named clearly and placed in a predictable folder.

#### Backend or logic requirements

- Implement `simulate_gbm_path(...)`.
- Validate that price, volatility, and time steps are sensible.
- Use a deterministic random seed.
- Return a pandas DataFrame with date/index and price values.
- Avoid hidden global state.

#### Local-run considerations

[Decision] No internet should be required.

[Decision] The same config and seed should generate the same output every time.

#### Acceptance criteria

- Running the demo config creates a market path CSV.
- Running the same config twice produces the same values.
- Invalid volatility or step count raises a clear error.
- A market path chart is saved to the results folder.
- Unit tests cover deterministic behavior and invalid inputs.

#### Edge cases

- Zero volatility.
- Negative volatility.
- Initial price less than or equal to zero.
- Steps less than or equal to zero.
- Missing config fields.
- Extremely high volatility.
- Multiple paths requested but reporting supports only one main demo path.

#### Complexity

[Decision] Medium.

#### Job-market value

[Decision] High.

Reason: shows simulation logic, reproducibility, data validation, and NumPy usage.

---

### Feature 2: Black-Scholes Pricing and Greeks Engine

#### Description

[Decision] Implement vectorized Black-Scholes pricing for European call and put options, plus key Greeks.

Minimum Greeks:

- Delta
- Gamma
- Vega
- Theta
- Rho

#### Why it matters for the project

[Decision] This is the mathematical core of the project.

[Decision] It creates technical depth beyond basic data processing.

#### Skill it demonstrates

- Numerical computing.
- SciPy statistical functions.
- Vectorized formula implementation.
- Function testing with known values.
- Handling numerical edge cases.
- Separating domain logic from UI/reporting.

#### User flow

1. User defines option settings in config.
2. Simulation produces stock prices over time.
3. Pricing engine calculates option values at each step.
4. Greeks engine calculates sensitivities at each step.
5. Results are saved to CSV and charts.

#### Data needed

[Decision] Minimum option config:

```yaml
option:
  option_type: call
  strike: 105.0
  risk_free_rate: 0.04
  volatility: 0.20
  days_to_expiry: 90
```

[Decision] DataFrame columns after pricing:

- `step`
- `underlying_price`
- `time_to_expiry`
- `option_type`
- `strike`
- `option_price`
- `delta`
- `gamma`
- `vega`
- `theta`
- `rho`

#### UI/UX requirements

[Decision] Output should include:

- Option price chart.
- Greeks chart.
- Pricing CSV.
- Clear labels and units.

[Decision] Chart titles should be readable to a non-finance reviewer.

Example title:

```text
Call Option Value Across Simulated Market Path
```

#### Backend or logic requirements

- Implement `black_scholes_price(...)`.
- Implement `calculate_greeks(...)`.
- Support scalar and vectorized NumPy inputs where practical.
- Validate option type.
- Validate strike, volatility, and time to expiry.
- Handle expiry cleanly.

#### Local-run considerations

[Decision] The pricing engine should not depend on live market data.

[Decision] The formulas should be deterministic and testable.

#### Acceptance criteria

- Call and put prices are calculated correctly for known benchmark values.
- Greeks return finite values for normal inputs.
- Expired option pricing is handled with intrinsic value.
- Invalid inputs raise helpful exceptions.
- Vectorized pricing works over a full price path.
- Tests cover call pricing, put pricing, Greeks, expiry, zero volatility, and invalid option types.

#### Edge cases

- Time to expiry equals zero.
- Volatility equals zero.
- Strike equals zero or negative.
- Underlying price equals zero or negative.
- Deep in-the-money options.
- Deep out-of-the-money options.
- Very short time to expiry.
- Option type typo.

#### Complexity

[Decision] High.

#### Job-market value

[Decision] High.

Reason: demonstrates math implementation, validation, testing, and vectorization.

---

### Feature 3: Fake Execution and Portfolio Tracker

#### Description

[Decision] Add a simple fake execution engine that receives strategy signals, creates simulated orders, updates cash and positions, and tracks portfolio value over time.

[Decision] This is fake execution only. It does not connect to brokerages or real markets.

#### Why it matters for the project

[Decision] This turns the project from a calculator into a system with state.

[Decision] State management creates stronger software engineering discussion than formula-only code.

#### Skill it demonstrates

- Dataclasses or typed classes.
- Object-oriented design or structured data modeling.
- State transitions.
- Portfolio accounting.
- pandas logging.
- Testing business logic.

#### User flow

1. User runs demo.
2. Strategy module creates simple signals such as buy, sell, or hold.
3. Execution module converts allowed signals into fake trades.
4. Portfolio module updates cash, positions, and account value.
5. Portfolio history is saved as CSV and chart.

#### Data needed

[Decision] Main data objects:

```python
Order:
  step
  symbol
  side
  quantity
  order_type
  requested_price

Trade:
  step
  symbol
  side
  quantity
  fill_price
  commission
  notional

Position:
  symbol
  quantity
  average_cost

PortfolioSnapshot:
  step
  cash
  positions_value
  total_value
  realized_pnl
  unrealized_pnl
  drawdown
```

#### UI/UX requirements

[Decision] Generated output should include:

- `trades.csv`
- `portfolio_history.csv`
- `portfolio_value.png`
- `drawdown.png`

[Decision] The summary report should explain:

- Number of trades.
- Final portfolio value.
- Max drawdown.
- Whether risk controls stopped trading.

#### Backend or logic requirements

- Implement basic `Order`, `Trade`, and `Position` models.
- Implement `Portfolio.apply_trade(...)`.
- Track cash changes from buys and sells.
- Track current position quantity and average cost.
- Mark portfolio to market using current simulated prices.
- Apply a simple commission or keep commission at zero for MVP.

#### Local-run considerations

[Decision] Use simple deterministic fills at the simulated price.

[Decision] Do not simulate complex order books, spreads, partial fills, latency, or slippage in MVP.

#### Acceptance criteria

- A buy trade decreases cash and increases position.
- A sell trade increases cash and decreases position.
- Portfolio value updates across the path.
- Drawdown is calculated.
- The app saves trade and portfolio CSVs.
- Tests verify portfolio accounting.

#### Edge cases

- Selling more than the current position.
- Buying without enough cash.
- Zero quantity order.
- Negative quantity order.
- Unknown symbol.
- Duplicate trade step.
- Portfolio value goes below risk limit.
- Final open position at end of simulation.

#### Complexity

[Decision] Medium to High.

#### Job-market value

[Decision] High.

Reason: demonstrates state management, accounting logic, edge cases, and testable software design.

---

### Feature 4: Risk-Control Layer

#### Description

[Decision] Add a risk layer that checks proposed orders before execution and logs risk events when trades are blocked.

Minimum rules:

- Max position size.
- Max trade notional.
- Max drawdown.
- Max daily or per-run loss.

#### Why it matters for the project

[Decision] Risk controls make the project feel more professional and less like a toy trading script.

[Decision] They create strong interview questions around validation, guardrails, edge cases, and system behavior.

#### Skill it demonstrates

- Rule-based validation.
- Defensive programming.
- Clear error/event logging.
- Separation of concerns.
- Testing with edge cases.

#### User flow

1. Strategy proposes an order.
2. Risk module checks the order against config limits and current portfolio state.
3. If allowed, execution processes the order.
4. If blocked, the app logs a risk event.
5. Report summarizes blocked trades and reasons.

#### Data needed

[Decision] Risk config:

```yaml
risk:
  starting_cash: 10000.0
  max_position_quantity: 10
  max_trade_notional: 2500.0
  max_drawdown_pct: 0.15
  max_loss_pct: 0.10
```

[Decision] Risk event fields:

- `step`
- `event_type`
- `severity`
- `symbol`
- `proposed_side`
- `proposed_quantity`
- `reason`
- `portfolio_value`
- `limit_value`

#### UI/UX requirements

[Decision] Risk events should be understandable in plain English.

Example:

```text
Blocked BUY 5 CALL_105 at step 88: trade notional 3100.00 exceeds max_trade_notional 2500.00.
```

[Decision] Summary report should include a risk section.

#### Backend or logic requirements

- Implement `RiskManager.validate_order(...)`.
- Return a structured result, not just `True` or `False`.
- Log blocked trades to `risk_events.csv`.
- Stop new trades after max drawdown breach if configured.
- Keep risk rules simple and testable.

#### Local-run considerations

[Decision] Risk rules should be deterministic and config-driven.

[Decision] No compliance, enterprise permissions, or real finance regulation features.

#### Acceptance criteria

- Position limit blocks oversized trades.
- Trade notional limit blocks expensive trades.
- Max drawdown rule stops future trades after breach.
- Risk events are saved to CSV.
- Tests cover allowed and blocked trades.

#### Edge cases

- Risk config missing.
- Max limit set to zero.
- Existing position already above limit.
- Portfolio value exactly at drawdown threshold.
- Multiple risk rules fail at once.
- Trade blocked but portfolio history still updates.

#### Complexity

[Decision] Medium.

#### Job-market value

[Decision] High.

Reason: shows reliability thinking, validation, and clean guardrail design.

---

### Feature 5: Reproducible Reports, Tests, and Benchmarking

#### Description

[Decision] One command should generate all demo artifacts: charts, CSVs, a Markdown summary report, and a small benchmark comparing loop-based versus vectorized option pricing.

#### Why it matters for the project

[Decision] This is what makes the project portfolio-ready.

[Decision] Recruiters and hiring managers should not need to run deep code inspection to understand the project.

#### Skill it demonstrates

- Automation.
- Reporting pipelines.
- File I/O.
- pandas exports.
- matplotlib charts.
- pytest.
- Runtime benchmarking.
- Performance communication.

#### User flow

1. User runs the CLI demo.
2. App creates `results/demo_run/`.
3. App saves all CSVs and charts.
4. App runs or loads benchmark output.
5. App creates `summary_report.md`.
6. README points to example outputs and screenshots.

#### Data needed

[Decision] Generated files:

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

#### UI/UX requirements

[Decision] Report should use plain Markdown.

[Decision] Charts should have readable titles, axis labels, and legends.

[Decision] README should show:

- What the project does.
- How to install.
- How to run.
- Example command.
- Example outputs.
- Screenshot/GIF.
- Architecture diagram.
- What is out of scope.

#### Backend or logic requirements

- Implement `reporting.py`.
- Implement `benchmark.py`.
- Write pytest tests.
- Use `ruff` for linting and formatting.
- Optional: use `mypy` or `pyright` after MVP works.

#### Local-run considerations

[Decision] The project should run from VS Code terminal without cloud setup.

[Decision] Benchmark should be small enough to run quickly on a normal laptop.

#### Acceptance criteria

- Demo run creates a complete results folder.
- Summary report contains key run statistics.
- Benchmark CSV compares loop and vectorized pricing.
- Tests can be run with `pytest`.
- README explains how to reproduce the demo.
- Output files are not confusing or scattered.

#### Edge cases

- Results folder already exists.
- File permission issues.
- Empty trades.
- No risk events.
- Benchmark too slow.
- matplotlib backend issues.
- Missing optional dependencies.

#### Complexity

[Decision] Medium.

#### Job-market value

[Decision] High.

Reason: turns the project into a polished portfolio artifact and proves testing/performance awareness.

---

## 5. Out-of-Scope List

### Features not worth building in Version 1

[Decision] Do not build these for MVP:

- Live stock-market data ingestion.
- Real options-chain scraping.
- Real brokerage integration.
- Real order execution.
- Complex multi-strategy framework.
- Machine learning price prediction.
- Advanced stochastic volatility models.
- American option pricing.
- Multi-asset portfolio optimization.
- Docker setup before the local version works.
- Full web dashboard before the CLI and report system work.
- Database layer before CSV outputs become painful.

### Features that would make it too SaaS-like

[Confirmed] This is not a SaaS project.

[Decision] Avoid:

- Login system.
- User accounts.
- Payment system.
- Subscription tiers.
- Cloud deployment.
- Team permissions.
- Enterprise security.
- Compliance dashboards.
- Admin panel.
- Growth analytics.
- Sales or monetization pages.
- Multi-tenant architecture.

### Features that can be future improvements

[Decision] Reasonable future improvements after MVP:

- Streamlit local dashboard.
- Plotly interactive charts.
- Numba acceleration for hot functions.
- cProfile or pyinstrument profiling report.
- Optional pybind11/C++ pricing kernel benchmark.
- Multiple option contracts.
- Multiple simulated paths.
- More strategy rules.
- More risk metrics such as VaR or expected shortfall.
- HTML report generation.

[Decision] Future improvements should only be added after the core system is working, tested, and documented.

---

## 6. UX Blueprint

### Main screens/pages

[Decision] Since PyRiskLab is local-first, the main “screens” are not traditional app screens. They are:

1. **CLI run experience**
   - User runs one command.
   - Terminal prints clear progress.

2. **Generated results folder**
   - User opens output files after the run.
   - File names are predictable.

3. **Summary report**
   - Markdown report explains the run.

4. **README demo section**
   - Reviewer sees screenshots, commands, and architecture.

[Decision] Optional later screen:

5. **Streamlit dashboard**
   - Only after MVP.
   - Would show charts and tables locally.

### Main flows

#### Flow A: First-time setup

1. Clone repo.
2. Create virtual environment.
3. Install dependencies.
4. Run tests.
5. Run demo config.
6. Open results folder.

#### Flow B: Run demo simulation

1. Run:

```bash
python -m pyrisklab run --config configs/demo.yaml
```

2. Terminal displays progress.
3. Results are saved to `results/demo_run/`.
4. User opens `summary_report.md`.

#### Flow C: Modify config

1. User changes seed, volatility, strike, or risk limits.
2. User reruns command.
3. App creates new output folder.
4. User compares outputs.

#### Flow D: Reviewer demo path

1. Reviewer opens README.
2. Sees one-sentence project description.
3. Sees architecture diagram.
4. Sees screenshot/GIF of generated charts.
5. Copies one command to run demo.
6. Checks tests and benchmark section.
7. Reads limitations.

### Empty states

[Decision] The app should handle these gracefully:

- No trades generated.
  - Report: “No trades were executed in this run.”
- No risk events.
  - Report: “No risk events were triggered.”
- Results folder empty before first run.
  - README explains that results are generated by running the demo command.
- Benchmark disabled.
  - Report: “Benchmark was skipped by config.”

### Loading states

[Decision] CLI progress messages should be enough.

Example:

```text
[1/7] Loading config...
[2/7] Simulating market path...
[3/7] Pricing options and Greeks...
[4/7] Running strategy and fake execution...
[5/7] Applying risk checks...
[6/7] Saving reports...
[7/7] Done. Results saved to results/demo_run/
```

### Error states

[Decision] Error messages should be specific and useful.

Examples:

```text
ConfigError: market.volatility must be >= 0. Received -0.2.
ConfigError: option.option_type must be 'call' or 'put'. Received 'calls'.
RunError: results/demo_run exists. Use --overwrite or choose a new run_name.
```

[Decision] Avoid giant stack traces for normal user mistakes.

### Mobile/responsive needs

[Decision] Not relevant for MVP.

[Decision] If a local Streamlit dashboard is added later, it only needs to be readable on desktop/laptop.

### Demo path for a reviewer

[Decision] The ideal reviewer demo path should be:

```bash
git clone <repo>
cd pyrisklab
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
pytest
python -m pyrisklab run --config configs/demo.yaml
```

Then the reviewer opens:

```text
results/demo_run/summary_report.md
```

[Decision] The README should make this path impossible to miss.

---

## 7. Data Blueprint

### Main entities

[Decision] Keep the data model small.

#### 1. RunConfig

Fields:

- `run_name`
- `seed`
- `output_dir`
- `market`
- `option`
- `strategy`
- `risk`
- `benchmark`

Purpose:

- Controls reproducibility and demo behavior.

#### 2. MarketPath

Fields:

- `step`
- `time_years`
- `underlying_price`
- Optional: `path_id`

Purpose:

- Represents synthetic market data.

#### 3. OptionContract

Fields:

- `symbol`
- `option_type`
- `strike`
- `risk_free_rate`
- `volatility`
- `days_to_expiry`
- `underlying_symbol`

Purpose:

- Defines the instrument being priced.

#### 4. PricingRecord

Fields:

- `step`
- `underlying_price`
- `time_to_expiry`
- `option_price`
- `delta`
- `gamma`
- `vega`
- `theta`
- `rho`

Purpose:

- Stores model outputs over time.

#### 5. Signal

Fields:

- `step`
- `symbol`
- `action`
- `reason`

Purpose:

- Represents a strategy decision before order creation.

#### 6. Order

Fields:

- `step`
- `symbol`
- `side`
- `quantity`
- `requested_price`
- `order_type`

Purpose:

- Represents a requested fake trade.

#### 7. Trade

Fields:

- `step`
- `symbol`
- `side`
- `quantity`
- `fill_price`
- `commission`
- `notional`

Purpose:

- Represents a completed fake trade.

#### 8. Position

Fields:

- `symbol`
- `quantity`
- `average_cost`
- `market_price`
- `market_value`
- `unrealized_pnl`

Purpose:

- Tracks holdings.

#### 9. PortfolioSnapshot

Fields:

- `step`
- `cash`
- `positions_value`
- `total_value`
- `realized_pnl`
- `unrealized_pnl`
- `drawdown`

Purpose:

- Tracks portfolio state over time.

#### 10. RiskEvent

Fields:

- `step`
- `event_type`
- `severity`
- `symbol`
- `reason`
- `portfolio_value`
- `limit_value`

Purpose:

- Logs blocked trades and risk breaches.

#### 11. BenchmarkResult

Fields:

- `method`
- `num_prices`
- `runtime_seconds`
- `speedup_vs_loop`

Purpose:

- Shows performance awareness.

### Relationships

[Decision] Main relationships:

- One `RunConfig` creates one simulation run.
- One simulation run creates one `MarketPath`.
- One `MarketPath` feeds many `PricingRecord` rows.
- Strategy reads `PricingRecord` rows and emits `Signal` objects.
- Signals become `Order` objects.
- Risk manager validates `Order` objects.
- Allowed orders become `Trade` objects.
- Trades update `Position` and `PortfolioSnapshot` objects.
- Blocked orders create `RiskEvent` objects.
- Reports summarize all generated artifacts.

### Example seed data

[Decision] Use one deterministic demo config.

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

### Local storage/database needs

[Decision] Use CSV and Markdown files for MVP.

[Decision] Do not use a database in Version 1.

Justification:

- The project is local.
- The data is run-generated.
- CSVs are easy to inspect.
- Avoiding a database keeps the scope focused.
- pandas works naturally with CSV outputs.

[Decision] Add SQLite only as a future improvement if repeated runs and history comparison become genuinely useful.

---

## 8. Engineering Blueprint

### Main modules/folders

[Decision] Use a real package structure.

```text
pyrisklab/
  README.md
  pyproject.toml
  requirements.txt
  configs/
    demo.yaml
  docs/
    PROJECT_MASTER_BLUEPRINT.md
    architecture.md
  src/
    pyrisklab/
      __init__.py
      cli.py
      config.py
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
    test_portfolio.py
    test_risk.py
    test_reporting.py
  results/
    .gitkeep
```

### Module responsibilities

#### `cli.py`

[Decision] CLI entry point.

Responsibilities:

- Parse command-line arguments.
- Call main run pipeline.
- Print progress messages.
- Handle user-facing errors.

#### `config.py`

[Decision] Config loading and validation.

Responsibilities:

- Load YAML or JSON.
- Validate required fields.
- Convert raw config into typed objects or dictionaries.
- Raise clean config errors.

#### `market.py`

[Decision] Market simulation.

Responsibilities:

- Generate geometric Brownian motion paths.
- Return DataFrames.
- Handle random seeds.

#### `pricing.py`

[Decision] Option pricing formulas.

Responsibilities:

- Black-Scholes call/put pricing.
- Intrinsic value handling at expiry.
- Input validation.
- Vectorized computation.

#### `greeks.py`

[Decision] Greeks calculation.

Responsibilities:

- Delta, gamma, vega, theta, rho.
- Vectorized calculations.
- Edge case handling.

#### `strategy.py`

[Decision] Simple rule-based fake strategy.

Responsibilities:

- Generate buy/sell/hold signals.
- Keep strategy intentionally simple.
- Use pricing and Greek outputs.

#### `execution.py`

[Decision] Fake order execution.

Responsibilities:

- Convert approved orders into trades.
- Apply deterministic fills.
- Keep execution simple and local.

#### `portfolio.py`

[Decision] Portfolio state management.

Responsibilities:

- Track cash.
- Track positions.
- Apply trades.
- Calculate total value and drawdown.
- Export portfolio history.

#### `risk.py`

[Decision] Risk validation.

Responsibilities:

- Validate orders before execution.
- Enforce position and loss limits.
- Log risk events.
- Stop future trades if needed.

#### `reporting.py`

[Decision] Output generation.

Responsibilities:

- Save CSVs.
- Generate charts.
- Generate summary report.
- Copy config used into results folder.

#### `benchmark.py`

[Decision] Performance comparison.

Responsibilities:

- Compare loop-based and vectorized pricing.
- Save benchmark results.
- Keep benchmark small and reliable.

#### `exceptions.py`

[Decision] Custom exceptions.

Responsibilities:

- `ConfigError`
- `PricingError`
- `RiskError`
- `RunError`

### API or service layer if needed

[Decision] Do not create a web API in MVP.

[Decision] Use internal service-style functions instead:

```python
run_simulation(config_path: str, overwrite: bool = False) -> RunResult
```

[Decision] This keeps the project local and avoids unnecessary SaaS architecture.

### State management needs

[Decision] State should live in explicit objects, not globals.

Recommended objects:

- `Portfolio`
- `RiskManager`
- `RunConfig`
- `RunResult`

[Decision] The portfolio object should be the main stateful component.

[Decision] Pricing and market simulation should mostly be pure functions.

### Error handling approach

[Decision] Use clear validation at boundaries.

Boundary points:

- Config loading.
- CLI arguments.
- Pricing inputs.
- Order creation.
- Risk validation.
- Results folder creation.

[Decision] For normal user mistakes, print clean error messages.

[Decision] For programmer errors, allow tests to expose them.

### Testing approach

[Decision] Use pytest from the beginning.

Minimum tests:

1. `test_config.py`
   - Valid config loads.
   - Missing required field fails.
   - Invalid values fail.

2. `test_market.py`
   - Same seed gives same path.
   - Invalid initial price fails.
   - Invalid volatility fails.

3. `test_pricing.py`
   - Known call price.
   - Known put price.
   - Put-call parity check.
   - Expiry intrinsic value.
   - Invalid option type fails.

4. `test_greeks.py`
   - Greeks return finite values.
   - Delta range is reasonable for call and put.
   - Expiry handling does not crash.

5. `test_portfolio.py`
   - Buy updates cash and position.
   - Sell updates cash and position.
   - Cannot sell more than held unless shorting is explicitly enabled.
   - Portfolio value updates.

6. `test_risk.py`
   - Position limit blocks trade.
   - Notional limit blocks trade.
   - Drawdown breach stops new trades.
   - Allowed trade passes.

7. `test_reporting.py`
   - Output directory is created.
   - Empty trades still produce a valid report.
   - CSV files are saved.

[Decision] Do not aim for perfect coverage. Aim for meaningful tests around logic that can break.

### Local setup approach

[Decision] Keep setup simple.

Recommended commands:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pytest
python -m pyrisklab run --config configs/demo.yaml
```

[Decision] Use `requirements.txt` for simplicity.

[Decision] Optional later: add `pyproject.toml` for package metadata, ruff, pytest settings, and editable install.

### Recommended dependencies

[Decision] Baseline dependencies:

```text
numpy
pandas
scipy
matplotlib
pyyaml
pytest
ruff
```

[Decision] Optional after MVP:

```text
mypy
typer
numba
streamlit
plotly
```

[Decision] Use `argparse` if you want fewer dependencies.

[Decision] Use `typer` if you want cleaner CLI ergonomics and are comfortable with one extra dependency.

---

## 9. Project Polish Plan

### README requirements

[Decision] The README should be treated as part of the project, not an afterthought.

Minimum README sections:

1. Project title and one-sentence summary.
2. Screenshot or GIF.
3. What this project demonstrates.
4. What it does.
5. What it does not do.
6. Tech stack.
7. Architecture diagram.
8. Local setup instructions.
9. Example command.
10. Example output folder.
11. Testing instructions.
12. Benchmark explanation.
13. Limitations.
14. Future improvements.
15. Resume bullet.

[Decision] The README opening should sound like:

> PyRiskLab is a local Python simulation engine for options pricing and portfolio risk analysis. It uses simulated market paths, Black-Scholes pricing, Greeks, fake execution, risk controls, and reproducible reporting to demonstrate Python software engineering, numerical computing, testing, and performance-aware design. It is not a trading bot and does not connect to real brokerage accounts.

### Screenshots/GIF/demo video needs

[Decision] Add these visuals:

1. Terminal running the demo command.
2. `results/demo_run/` folder view.
3. Market path chart.
4. Option value chart.
5. Portfolio value chart.
6. Drawdown chart.
7. Benchmark table or screenshot.
8. Optional short GIF showing command to generated report.

[Decision] A 30 to 60 second screen recording is enough.

Suggested demo video flow:

1. Open README.
2. Run `pytest`.
3. Run demo command.
4. Open summary report.
5. Show charts and CSV outputs.

### Seed data requirements

[Decision] Include a deterministic `configs/demo.yaml`.

[Decision] Keep the demo output stable enough for screenshots.

[Decision] Include one sample completed run in README screenshots, but do not commit large generated files unless they are small and useful.

Recommended Git behavior:

- Commit `results/.gitkeep`.
- Do not commit every generated run.
- Optionally commit `docs/sample_outputs/` with a few screenshots.

### Portfolio case study notes

[Decision] Create a short portfolio case study after the project works.

Case study structure:

1. Problem
   - I wanted to build a local Python simulation system, not a notebook.

2. Approach
   - Config-driven run pipeline.
   - Simulated market data.
   - Pricing and Greeks.
   - Fake execution.
   - Risk controls.
   - Reporting and benchmark.

3. Engineering decisions
   - Why local-first.
   - Why CSV and Markdown instead of database.
   - Why deterministic seeds.
   - Why vectorization.
   - Why simple strategy.

4. Testing
   - Pricing tests.
   - Portfolio accounting tests.
   - Risk rule tests.

5. Result
   - One command generates a full report.

6. What I would improve
   - Add Numba benchmark.
   - Add local dashboard.
   - Add multiple contracts.

### Resume bullet opportunities

[Decision] General software intern bullet:

> Built PyRiskLab, a modular local Python simulation engine using NumPy, pandas, SciPy, matplotlib, and pytest to generate market paths, price options, calculate Greeks, simulate fake trades, enforce risk controls, benchmark vectorized computation, and export reproducible portfolio reports.

[Decision] AMD-style software tooling bullet:

> Developed a performance-aware Python simulation and analytics tool with deterministic configs, vectorized numerical computation, automated tests, CLI execution, benchmark reporting, and reproducible outputs, demonstrating software design, debugging, testing, and engineering-tooling skills.

[Decision] Testing-focused bullet:

> Implemented pytest coverage for pricing formulas, Greeks, portfolio accounting, risk-rule validation, config errors, and edge cases to improve correctness and maintainability in a local Python simulation system.

---

## 10. Build Roadmap

[Decision] Build in phases. Do not start with the dashboard. Do not start with too many strategy ideas.

---

### Phase 0: Setup and Docs

Goal:

[Decision] Create the repo skeleton and project identity.

Tasks:

- Create folder structure.
- Add `README.md`.
- Add `docs/PROJECT_MASTER_BLUEPRINT.md`.
- Add `configs/demo.yaml`.
- Add `requirements.txt`.
- Add `.gitignore`.
- Add `src/pyrisklab/__init__.py`.
- Add placeholder modules.
- Add initial pytest setup.
- Add ruff configuration if using `pyproject.toml`.

Acceptance criteria:

- Repo opens cleanly in VS Code.
- Virtual environment can be created.
- Dependencies install.
- `pytest` runs, even if only one placeholder test exists.
- README clearly says what the project is and is not.

---

### Phase 1: Skeleton App

Goal:

[Decision] Make the CLI run end-to-end with placeholder logic.

Tasks:

- Implement `cli.py`.
- Implement `config.py`.
- Load `configs/demo.yaml`.
- Create output directory.
- Print progress steps.
- Save `config_used.yaml`.
- Return a basic success message.

Acceptance criteria:

- Command works:

```bash
python -m pyrisklab run --config configs/demo.yaml
```

- Results folder is created.
- Bad config path gives a clear error.
- Config validation catches missing major sections.

---

### Phase 2: Core Data / Model Layer

Goal:

[Decision] Add the main data structures before complex behavior.

Tasks:

- Create dataclasses or typed structures for:
  - `OptionContract`
  - `Order`
  - `Trade`
  - `Position`
  - `PortfolioSnapshot`
  - `RiskEvent`
- Add custom exceptions.
- Add basic tests for object creation and validation.
- Decide whether to use plain dataclasses or pydantic.

[Decision] Use plain dataclasses for MVP unless validation becomes painful.

Acceptance criteria:

- Core objects are typed and readable.
- Tests verify invalid object inputs where needed.
- No giant dictionaries passed everywhere.

---

### Phase 3: Feature Build

Goal:

[Decision] Build the five core features in order.

#### 3A: Market simulation

Tasks:

- Implement GBM path generation.
- Save `market_path.csv`.
- Save `market_path.png`.
- Add tests for deterministic seed.

#### 3B: Pricing and Greeks

Tasks:

- Implement Black-Scholes call/put.
- Implement Greeks.
- Save pricing and Greeks CSVs.
- Save option price and Greeks charts.
- Add known-value tests.

#### 3C: Strategy and fake execution

Tasks:

- Implement simple delta-based strategy.
- Generate orders.
- Fill allowed trades at simulated prices.
- Save `trades.csv`.

#### 3D: Portfolio tracker

Tasks:

- Track cash and positions.
- Calculate total value.
- Calculate drawdown.
- Save `portfolio_history.csv`.
- Save portfolio and drawdown charts.

#### 3E: Risk controls

Tasks:

- Add position limit.
- Add trade notional limit.
- Add max drawdown or max loss stop.
- Save `risk_events.csv`.
- Add tests for blocked trades.

Acceptance criteria:

- One command creates all main CSVs and charts.
- All five features connect in one pipeline.
- Tests cover the riskiest logic.

---

### Phase 4: Tests and Fixes

Goal:

[Decision] Make the project reliable.

Tasks:

- Add missing unit tests.
- Add edge case tests.
- Run `pytest`.
- Run `ruff`.
- Fix confusing names.
- Fix unclear errors.
- Remove dead code.
- Keep functions small.
- Add docstrings only where useful.

Acceptance criteria:

- Tests pass.
- Linting passes or has minimal justified ignores.
- Demo run works after clean install.
- Edge cases have clear behavior.

---

### Phase 5: UI Polish

Goal:

[Decision] Make outputs easy to understand.

Tasks:

- Improve chart titles.
- Improve axis labels.
- Improve file names.
- Improve terminal progress messages.
- Make summary report readable.
- Add a small architecture diagram.
- Add screenshot-ready sample output.

Acceptance criteria:

- A reviewer can open the report and understand the run.
- Charts are readable without reading code.
- README screenshots look clean.
- Empty states are handled.

---

### Phase 6: README, Screenshots, Demo, Resume Story

Goal:

[Decision] Turn the project into a portfolio asset.

Tasks:

- Finalize README.
- Add setup instructions.
- Add demo command.
- Add screenshots.
- Add benchmark explanation.
- Add limitations.
- Add future improvements.
- Add resume bullet.
- Write short interview explanation.
- Record optional 30 to 60 second demo video.

Acceptance criteria:

- Reviewer can understand the project in under two minutes.
- Reviewer can run it locally.
- README clearly says this is not a trading bot.
- Resume bullet is backed by actual project features.
- Demo path is obvious.

---

## 11. Risks and Simplifications

### Biggest ways this project can fail

#### Risk 1: It becomes a finance tutorial

[Decision] Avoid by emphasizing architecture, testing, benchmark, and reproducible reporting.

#### Risk 2: It becomes too large

[Decision] Avoid by keeping only five core features in MVP.

#### Risk 3: The strategy becomes the focus

[Decision] Avoid by making the strategy intentionally simple.

[Decision] The strategy exists only to create orders and portfolio state.

#### Risk 4: The project overpromises profitability

[Decision] Avoid any claim that the project predicts markets or makes money.

[Confirmed] It is a simulation only.

#### Risk 5: The math is copied without validation

[Decision] Avoid by writing tests, explaining assumptions, and handling edge cases.

#### Risk 6: The repo looks messy

[Decision] Avoid by using `src/pyrisklab/`, tests, configs, docs, and predictable outputs.

#### Risk 7: The dashboard eats the project

[Decision] Avoid building Streamlit until the CLI/report system is complete.

#### Risk 8: Benchmarking becomes fake or misleading

[Decision] Keep benchmark simple and honest.

[Decision] Compare loop versus vectorized pricing on the same generated input size.

### What to cut if it gets too big

[Decision] Cut in this order:

1. Multiple simulated paths.
2. Multiple option contracts.
3. Put option support in the demo, while keeping pricing tests for puts.
4. Advanced Greeks chart styling.
5. Commission modeling.
6. Strategy customization.
7. Benchmark extras.
8. Streamlit dashboard.
9. Numba acceleration.
10. HTML reporting.

[Decision] Do not cut:

- Pricing tests.
- Config-driven run.
- Saved outputs.
- README.
- Risk events.
- Portfolio history.
- One benchmark.

### What must be done well no matter what

[Decision] These are non-negotiable:

1. One command runs the project.
2. The project is local and reproducible.
3. README is clear.
4. Code is modular.
5. Tests cover pricing, portfolio, and risk rules.
6. Outputs are saved in a clean results folder.
7. The project does not claim to be a real trading system.
8. The demo path is obvious.
9. The repo looks finished.

---

## 12. Final Recommended MVP

### Exact features to build

[Decision] Build these exact MVP features:

1. **Config-driven CLI**
   - `python -m pyrisklab run --config configs/demo.yaml`

2. **Market simulation**
   - One deterministic GBM stock path.
   - Saved CSV and chart.

3. **Black-Scholes pricing**
   - European call and put support.
   - Demo can focus on one call option.

4. **Greeks calculation**
   - Delta, gamma, vega, theta, rho.
   - Saved CSV and chart.

5. **Simple fake strategy**
   - Delta-based buy/sell/hold rule.
   - Simple and intentionally not profit-optimized.

6. **Fake execution**
   - Deterministic fills at simulated price.
   - Trades saved to CSV.

7. **Portfolio tracker**
   - Cash.
   - Position quantity.
   - Average cost.
   - Total value.
   - Drawdown.
   - Saved CSV and charts.

8. **Risk manager**
   - Max position size.
   - Max trade notional.
   - Max drawdown or max loss.
   - Risk events saved to CSV.

9. **Reporting**
   - CSV outputs.
   - PNG charts.
   - `summary_report.md`.

10. **Tests**
    - Pricing tests.
    - Greeks tests.
    - Portfolio tests.
    - Risk tests.
    - Config tests.

11. **Benchmark**
    - Loop-based versus vectorized pricing comparison.
    - Saved benchmark CSV.
    - README explanation.

12. **Polished README**
    - Screenshots.
    - Setup.
    - Demo command.
    - Architecture.
    - Limitations.
    - Resume bullet.

### Exact features to delay

[Decision] Delay these:

- Streamlit dashboard.
- Plotly charts.
- Numba acceleration.
- C++ extension.
- Live market data.
- Options-chain scraping.
- Database.
- Docker.
- Cloud deployment.
- User accounts.
- Login.
- Real trading.
- ML prediction.
- Advanced pricing models.
- Strategy optimization.
- Multi-user features.
- Web API.

### Definition of done

[Decision] PyRiskLab MVP is done when:

- `pytest` passes.
- `python -m pyrisklab run --config configs/demo.yaml` runs successfully.
- A complete `results/demo_run/` folder is generated.
- The run produces market, pricing, Greeks, trades, portfolio, risk, benchmark, and summary outputs.
- README explains the project clearly.
- README includes screenshots or sample outputs.
- The architecture is understandable.
- The out-of-scope list is explicit.
- The project does not look like a single notebook.
- The project does not claim real trading ability.
- The resume bullet matches what was actually built.
- A reviewer can understand the project and demo path quickly.

---

## Move-On Checklist

[Decision] Move on to implementation only when:

- [x] The project is scoped to a finishable local build.
- [x] The features are connected to skill signals.
- [x] The demo path is obvious.
- [x] There is a clear out-of-scope list.
- [x] The roadmap has a setup phase, build phase, test phase, and polish phase.

---

## Final Build Instruction

[Decision] Start with the repo skeleton and a passing placeholder test.

[Decision] Then build in this order:

1. Config loading.
2. CLI run command.
3. Market simulation.
4. Pricing tests.
5. Black-Scholes pricing.
6. Greeks.
7. Reporting for first chart.
8. Portfolio state.
9. Risk rules.
10. Benchmark.
11. README polish.

[Decision] Do not start with Streamlit.

[Decision] Do not add live market data.

[Decision] Do not make this a trading bot.

[Decision] Build the clean local Python engine first.
