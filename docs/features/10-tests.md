# Feature 10: Tests

## Output Path

`docs/features/10-tests.md`

---

## 1. Feature Overview

### Feature name

**Tests**

### One-sentence description

Build a focused pytest suite that verifies PyRiskLab’s config loading, simulation, pricing, Greeks, strategy, execution, portfolio, risk, and reporting behavior.

### Detailed description

The Tests feature is the correctness and reliability layer of PyRiskLab. It ensures that the project is not just a demo that works once, but a maintainable local Python system with repeatable validation.

This feature should create a practical pytest test suite covering the most important logic in the project:

- Config loading and validation
- Deterministic market simulation
- Black-Scholes pricing correctness
- Greeks calculation sanity and edge cases
- Fake strategy signal rules
- Fake execution order/trade conversion
- Portfolio accounting
- Risk Manager blocking rules
- Reporting output generation
- Pipeline smoke behavior

The goal is not to chase meaningless 100% coverage. The goal is to prove that the important math, state transitions, validation paths, and generated outputs are tested.

### Why it matters

Tests are one of the strongest signals that PyRiskLab is a real software engineering project, not a notebook or copied finance script. For internship recruiting, tests show discipline, debugging skill, edge-case thinking, and maintainability.

A reviewer should be able to run:

```bash
pytest
```

and see that the core system is validated.

### Skill it demonstrates

- pytest usage
- Unit testing
- Integration testing
- Deterministic test design
- Edge-case validation
- Floating-point comparison
- Temporary directory testing
- Error-path testing
- Regression-test mindset
- Professional repo quality

### Priority

**High**

Tests are core to the project’s job-market value. They should be built alongside features, not added as an afterthought.

### Complexity

**Medium**

Individual tests are straightforward, but the challenge is choosing meaningful tests and keeping them deterministic.

---

## 2. User/Demo Flow

### Happy path

1. User opens the repo in VS Code.
2. User creates and activates a virtual environment.
3. User installs dependencies:

```bash
pip install -r requirements.txt
```

4. User runs:

```bash
pytest
```

5. The test suite runs successfully.
6. The terminal shows all tests passing.
7. User can then run the demo command with more confidence:

```bash
python -m pyrisklab run --config configs/demo.yaml
```

### First-time path

For a first-time reviewer, the README should later make the test command obvious:

```bash
pytest
```

Optional verbose mode:

```bash
pytest -v
```

Recommended targeted test commands:

```bash
pytest tests/test_pricing.py
pytest tests/test_portfolio.py
pytest tests/test_risk.py
```

### Empty state

If no tests exist yet, that is not acceptable for the finished project.

During early scaffolding only, one placeholder test can exist to prove pytest is wired correctly:

```python
def test_placeholder() -> None:
    assert True
```

But by the finished MVP, placeholder tests should be removed or replaced with meaningful tests.

### Error path

When a test fails, pytest should provide a normal assertion failure.

Example:

```text
E assert 10.45 == 10.44 ± 0.01
```

For expected application errors, tests should assert the specific exception type:

```python
with pytest.raises(ConfigError):
    load_config(path)
```

Test failures should not depend on live market data, internet access, current dates, random outputs without seeds, or local machine state.

### Demo path for a reviewer

Reviewer runs:

```bash
pytest
```

Then optionally:

```bash
python -m pyrisklab run --config configs/demo.yaml --overwrite
```

The reviewer should see that PyRiskLab has both automated validation and a working demo run.

---

## 3. UX/UI Requirements

### Screens/pages

There are no UI screens for this feature.

The user-facing surfaces are:

1. Terminal pytest output
2. `tests/` folder organization
3. README testing instructions later
4. Optional CI output in a future repo polish step

### Components

#### Test folder

Required folder:

```text
tests/
```

Recommended files:

```text
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
  test_pipeline_smoke.py
```

#### pytest configuration

Recommended location:

```text
pyproject.toml
```

Suggested config:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
addopts = "-q"
```

[Decision] Use simple pytest configuration. Do not overcomplicate with coverage tools unless the core suite is already working.

### Forms/inputs

No forms are needed.

Inputs are:

- Test fixtures
- Small hardcoded test data
- Temporary config files
- Temporary output directories
- Deterministic random seeds

### Buttons/actions

No buttons are needed.

Commands:

```bash
pytest
pytest -v
pytest tests/test_pricing.py
pytest tests/test_risk.py
```

### Validation messages

Tests should validate that application errors are clear.

Examples:

```python
assert "market.volatility" in str(exc.value)
assert "option_type" in str(exc.value)
assert "max_trade_notional" in str(exc.value)
```

### Empty states

Tests should explicitly check important valid empty states:

- No trades
- No risk events
- No signals
- Empty output DataFrames with headers

### Loading states

Not relevant.

### Error states

pytest failures should be readable and focused.

Avoid giant integration tests where one failure makes it unclear what broke.

### Responsive behavior if relevant

Not relevant.

---

## 4. Data Requirements

### Entities involved

Tests should cover these entities and modules:

- `RunConfig`
- `MarketConfig`
- `OptionConfig`
- `StrategyConfig`
- `RiskConfig`
- `OptionContract`
- `Signal`
- `Order`
- `Trade`
- `Position`
- `PortfolioSnapshot`
- `RiskEvent`
- `BenchmarkResult`, later in Feature 11
- `config.py`
- `market.py`
- `pricing.py`
- `greeks.py`
- `strategy.py`
- `execution.py`
- `portfolio.py`
- `risk.py`
- `reporting.py`

### Fields

Tests should verify required fields in generated DataFrames.

#### Market path columns

```text
step
time_years
underlying_price
```

#### Pricing history columns

```text
step
underlying_price
time_to_expiry
option_type
strike
option_price
```

#### Greeks columns

```text
step
delta
gamma
vega
theta
rho
```

#### Signals columns

```text
step
symbol
action
reason
```

#### Orders columns

```text
step
symbol
side
quantity
order_type
requested_price
status
reason
```

#### Trades columns

```text
step
symbol
side
quantity
fill_price
commission
notional
```

#### Portfolio history columns

```text
step
cash
position_quantity
average_cost
market_price
positions_value
realized_pnl
unrealized_pnl
total_value
peak_value
drawdown
drawdown_pct
```

#### Risk events columns

```text
step
event_type
severity
symbol
proposed_side
proposed_quantity
proposed_notional
portfolio_value
limit_name
limit_value
observed_value
reason
```

### Relationships

- Config tests validate data before the pipeline runs.
- Market tests validate deterministic input data generation.
- Pricing and Greeks tests validate mathematical outputs.
- Strategy tests validate signals from pricing/Greek data.
- Execution tests validate order-to-trade behavior.
- Portfolio tests validate state transitions after trades.
- Risk tests validate blocked/allowed orders.
- Reporting tests validate generated artifacts.
- Pipeline smoke tests validate that the pieces connect.

### Example seed data

Use tiny deterministic data in tests.

Example market path:

```python
prices = [100.0, 101.0, 99.0]
```

Example option settings:

```python
underlying_price = 100.0
strike = 100.0
risk_free_rate = 0.05
volatility = 0.20
time_to_expiry = 1.0
```

Example trade:

```python
Trade(
    step=1,
    symbol="CALL_105",
    side="BUY",
    quantity=1,
    fill_price=5.0,
    commission=0.0,
    notional=500.0,
)
```

### Local persistence needs

Tests should use temporary directories for file-writing behavior.

Use pytest `tmp_path`:

```python
def test_report_writes_file(tmp_path):
    ...
```

Do not write test artifacts into the real `results/demo_run/` folder unless it is a specific manual demo run.

---

## 5. Logic Requirements

### Business rules

#### Test deterministic behavior

Any random process must be tested with a fixed seed.

Expected:

```text
same config + same seed = same market path
```

#### Test invalid inputs

Each major module should have tests for invalid inputs.

Examples:

- Negative volatility
- Nonpositive initial price
- Invalid option type
- Negative strike
- Negative trade quantity
- Selling more than held
- Risk limit below zero
- Missing required output columns

#### Test empty states

Empty valid states should not crash:

- Empty trades
- Empty risk events
- No generated signals

#### Test floating-point calculations carefully

Use approximate comparisons:

```python
import pytest

assert actual == pytest.approx(expected, rel=1e-6)
```

Do not compare floats with exact equality unless values are intentionally exact.

#### Test one behavior per test

Each test should focus on one clear behavior.

Good:

```python
def test_buy_trade_decreases_cash():
    ...
```

Bad:

```python
def test_everything_works():
    ...
```

### Calculations

Tests should verify calculations for:

- GBM deterministic path reproducibility
- Black-Scholes call price
- Black-Scholes put price
- Put-call parity
- Intrinsic value at expiry
- Delta range
- Gamma nonnegative for standard cases
- Trade notional
- Cash after buy/sell
- Realized P&L
- Unrealized P&L
- Drawdown
- Risk notional limit
- Risk position limit

### API/service functions if needed

Testing helper fixtures can live in:

```text
tests/conftest.py
```

Potential fixtures:

```python
@pytest.fixture
def demo_config_dict():
    ...

@pytest.fixture
def sample_pricing_history():
    ...

@pytest.fixture
def sample_trade():
    ...
```

[Decision] Keep fixtures simple. Do not create a huge testing framework.

### State management

Tests should avoid shared mutable state.

Each test should create fresh objects.

Use `tmp_path` for file outputs.

Avoid test-order dependence.

### Edge cases

Required edge cases:

#### Config

- Missing required section
- Invalid market volatility
- Invalid option type
- Invalid risk limit
- Existing results folder without overwrite

#### Market

- Same seed reproducibility
- Zero volatility
- Negative volatility
- Nonpositive initial price
- Steps less than or equal to zero

#### Pricing

- Known call price
- Known put price
- Put-call parity
- Expiry intrinsic value
- Zero volatility
- Invalid option type

#### Greeks

- Finite values for normal inputs
- Delta range for call and put
- Near-expiry handling
- Zero volatility handling

#### Strategy

- Buy signal when delta below threshold
- Sell signal when delta above threshold
- Hold signal when inside thresholds
- Invalid threshold config
- Empty pricing/Greek input

#### Execution

- Valid signal/order creates trade
- Zero quantity rejected
- Negative quantity rejected
- Missing price rejected
- Empty orders produce empty trades

#### Portfolio

- Buy decreases cash
- Sell increases cash
- Cannot sell more than held
- Empty trades produce flat portfolio history
- Drawdown calculation

#### Risk

- Allowed order passes
- Position limit blocks
- Trade notional limit blocks
- Drawdown breach blocks
- Loss breach blocks
- Empty risk events CSV still generated

#### Reporting

- Output directory created
- Existing output directory blocked unless overwrite
- CSV files saved
- PNG files saved
- Summary report includes limitations
- Empty trades/risk events handled

---

## 6. Acceptance Criteria

### AC1: pytest runs from repo root

Given the project dependencies are installed  
When the user runs `pytest` from the repo root  
Then the full test suite runs without import errors.

### AC2: Config tests validate good and bad configs

Given valid and invalid config inputs  
When config tests run  
Then valid configs load successfully  
And invalid configs raise clear `ConfigError` messages.

### AC3: Market tests prove deterministic simulation

Given the same market config and seed  
When market simulation runs twice  
Then the generated market path values match.

### AC4: Pricing tests verify Black-Scholes behavior

Given known option-pricing inputs  
When pricing tests run  
Then call and put prices match expected values within tolerance  
And put-call parity holds within tolerance.

### AC5: Greeks tests verify sane sensitivity outputs

Given normal option inputs  
When Greeks are calculated  
Then outputs are finite  
And Delta/Gamma values fall within reasonable expected ranges.

### AC6: Strategy tests verify signal rules

Given sample Greek/pricing inputs  
When the fake strategy runs  
Then it emits BUY, SELL, or HOLD signals according to configured thresholds.

### AC7: Execution tests verify simulated trade conversion

Given valid orders  
When Fake Execution runs  
Then trades are created with expected fill prices and notional values.

### AC8: Portfolio tests verify state transitions

Given buy and sell trades  
When the Portfolio Tracker applies them  
Then cash, position quantity, P&L, total value, and drawdown update correctly.

### AC9: Risk tests verify allowed and blocked paths

Given orders inside and outside risk limits  
When Risk Manager validates them  
Then valid orders pass  
And invalid orders are blocked with readable risk events.

### AC10: Reporting tests verify artifacts

Given sample output DataFrames  
When Reporting runs  
Then CSV files, PNG charts, config copy, and summary report are created in a temporary run folder.

### AC11: Pipeline smoke test verifies end-to-end connection

Given a small deterministic config  
When the pipeline runs  
Then the run completes  
And a results folder with core artifacts is produced.

### AC12: Tests do not require internet or real market data

Given the test suite is run offline  
When `pytest` runs  
Then no test depends on network access, API keys, brokerage accounts, or live market data.

---

## 7. Test Plan

### Unit tests

Required files:

```text
tests/test_config.py
tests/test_market.py
tests/test_pricing.py
tests/test_greeks.py
tests/test_strategy.py
tests/test_execution.py
tests/test_portfolio.py
tests/test_risk.py
tests/test_reporting.py
```

#### `test_config.py`

Minimum tests:

- Valid config loads
- Missing required section fails
- Invalid volatility fails
- Invalid option type fails
- Invalid risk limit fails
- Bad config path fails cleanly

#### `test_market.py`

Minimum tests:

- Same seed produces same path
- Different seed can produce different path
- Zero volatility is handled predictably
- Negative volatility fails
- Nonpositive initial price fails
- Output DataFrame has required columns

#### `test_pricing.py`

Minimum tests:

- Known call price
- Known put price
- Put-call parity
- Expiry intrinsic value
- Zero volatility handling
- Invalid option type fails
- Vectorized input returns expected shape

#### `test_greeks.py`

Minimum tests:

- Greeks return finite values for normal inputs
- Call delta is between 0 and 1
- Put delta is between -1 and 0
- Gamma is nonnegative for normal cases
- Near-expiry handling does not crash
- Invalid inputs fail clearly

#### `test_strategy.py`

Minimum tests:

- Delta below buy threshold creates BUY signal
- Delta above sell threshold creates SELL signal
- Delta inside thresholds creates HOLD signal
- Empty input returns empty signals or clear result
- Invalid thresholds fail config validation

#### `test_execution.py`

Minimum tests:

- Valid order creates trade
- Trade notional is calculated correctly
- HOLD signal creates no trade
- Zero quantity fails
- Negative quantity fails
- Missing price fails
- Empty orders produce empty trades

#### `test_portfolio.py`

Minimum tests:

- Portfolio initializes with starting cash
- Buy decreases cash and increases position
- Sell increases cash and decreases position
- Cannot sell more than held
- Average cost updates correctly
- Realized P&L updates correctly
- Unrealized P&L updates correctly
- Drawdown updates correctly
- Empty trades generate flat history

#### `test_risk.py`

Minimum tests:

- Allowed order passes
- Position limit blocks order
- Trade notional limit blocks order
- Drawdown breach blocks order
- Loss breach blocks order
- Trading stopped blocks future orders
- Risk event has readable reason

#### `test_reporting.py`

Minimum tests:

- Output directory created
- Existing folder blocked without overwrite
- Overwrite only deletes target run folder
- Config copy saved
- CSV outputs saved
- PNG charts saved
- Summary report generated
- Empty trades/risk events handled
- Missing chart columns fail clearly

### Integration tests if useful

Required integration file:

```text
tests/test_pipeline_smoke.py
```

Recommended smoke test:

- Create tiny deterministic config using `tmp_path`
- Run pipeline with that config
- Confirm it completes
- Confirm output folder exists
- Confirm key files exist:
  - `market_path.csv`
  - `pricing_history.csv`
  - `portfolio_history.csv`
  - `risk_events.csv`
  - `summary_report.md`

[Decision] Keep integration tests small. They should prove wiring, not repeat every unit test.

### Manual QA checklist

- [ ] Run `pytest` from repo root.
- [ ] Run `pytest -v` and confirm readable test names.
- [ ] Run a targeted file like `pytest tests/test_pricing.py`.
- [ ] Confirm no tests require internet.
- [ ] Confirm no tests write to real `results/demo_run/` unexpectedly.
- [ ] Confirm failures show useful messages.
- [ ] Confirm tests use fixed seeds for random logic.
- [ ] Confirm tests use `pytest.approx` for floating-point comparisons.
- [ ] Confirm no placeholder-only tests remain in final MVP.

### Demo verification checklist

- [ ] README later includes `pytest` command.
- [ ] Test suite passes before demo run.
- [ ] Test names clearly map to project features.
- [ ] Tests support interview claims about correctness.
- [ ] Test suite is not bloated with meaningless coverage.

---

## 8. Portfolio Value

### How this feature helps the project stand out

Tests make PyRiskLab look like a real software project. Many portfolio projects have impressive screenshots but no validation. A clean pytest suite shows that the project was built with correctness, debugging, and maintainability in mind.

This feature helps the project stand out because it proves:

- The math was checked.
- Edge cases were considered.
- State transitions were validated.
- Error paths were tested.
- The project can be safely changed later.
- The repo is more than a demo script.

### What to mention in README

Mention:

```text
PyRiskLab includes a pytest suite covering config validation, deterministic market simulation, Black-Scholes pricing, Greeks, fake execution, portfolio accounting, risk rules, and reporting outputs.
```

Also mention:

```bash
pytest
```

Add a short note:

```text
Tests use deterministic seeds and local fixture data only. They do not require internet access, live market data, or brokerage accounts.
```

### What to mention in interviews

Strong interview points:

- “I wrote known-value tests for Black-Scholes pricing instead of just trusting the formula.”
- “I used fixed random seeds to make simulation tests deterministic.”
- “I tested failure paths like invalid configs, bad option types, and selling more than the current position.”
- “I used pytest temporary directories so reporting tests do not pollute the real results folder.”
- “I focused on meaningful tests over fake 100% coverage.”

---

## 9. Implementation Notes For Codex

### Likely files/folders

Primary folder:

```text
tests/
```

Required test files:

```text
tests/test_config.py
tests/test_market.py
tests/test_pricing.py
tests/test_greeks.py
tests/test_strategy.py
tests/test_execution.py
tests/test_portfolio.py
tests/test_risk.py
tests/test_reporting.py
tests/test_pipeline_smoke.py
```

Optional shared fixtures:

```text
tests/conftest.py
```

Related config:

```text
pyproject.toml
requirements.txt
```

### Recommended dependencies

Required:

```text
pytest
```

Already expected in project dependencies:

```text
numpy
pandas
scipy
matplotlib
pyyaml
pytest
ruff
```

[Decision] Do not add coverage tools until the basic suite is stable.

Optional later:

```text
pytest-cov
```

### Build order

1. Confirm pytest is installed in `requirements.txt`.
2. Add pytest config in `pyproject.toml`.
3. Add `tests/conftest.py` only if shared fixtures are helpful.
4. Build `test_config.py`.
5. Build `test_market.py`.
6. Build `test_pricing.py`.
7. Build `test_greeks.py`.
8. Build `test_strategy.py`.
9. Build `test_execution.py`.
10. Build `test_portfolio.py`.
11. Build `test_risk.py`.
12. Build `test_reporting.py`.
13. Build `test_pipeline_smoke.py`.
14. Remove any placeholder tests.
15. Run `pytest`.
16. Fix failures by correcting code, not weakening tests unless the test expectation is wrong.

### Risks

#### Risk 1: Tests become too shallow

Avoid tests that only check that functions run without checking output.

Bad:

```python
assert result is not None
```

Better:

```python
assert result["option_price"].iloc[0] == pytest.approx(10.45, rel=1e-3)
```

#### Risk 2: Tests become too brittle

Avoid tests that depend on exact chart pixels, system time, random outputs without seeds, or file ordering unless controlled.

#### Risk 3: Tests write into real results folder

Use `tmp_path` for test outputs.

#### Risk 4: Over-focusing on coverage percentage

Coverage is less important than testing meaningful logic.

#### Risk 5: Integration tests become huge

Keep pipeline smoke tests small and deterministic.

### What not to change

Do not change:

- CLI command format just to make tests easier
- Valid project behavior to satisfy weak tests
- Black-Scholes formulas without known-value verification
- Output file names unless the feature specs are updated consistently
- The local-only/non-SaaS project scope

This feature should strengthen confidence in the existing system, not change what the system is.

---

## Move-On Checklist

- [ ] `pytest` runs from the repo root.
- [ ] Test suite has meaningful tests for each core module.
- [ ] Pricing tests use known values and approximate comparisons.
- [ ] Market tests prove deterministic seeds.
- [ ] Portfolio tests validate cash, positions, P&L, and drawdown.
- [ ] Risk tests validate allowed and blocked orders.
- [ ] Reporting tests use temporary directories.
- [ ] Pipeline smoke test confirms core integration.
- [ ] No tests require internet, live market data, broker APIs, or external services.
- [ ] Placeholder-only tests are removed before final MVP.
