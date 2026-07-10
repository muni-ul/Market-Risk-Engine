# Feature 5 — Simple Fake Strategy

## 1. Feature Overview

### Feature name

**Simple Fake Strategy**

### One-sentence description

Generate deterministic buy, sell, or hold signals from option-pricing and Greek data using one intentionally simple rule-based strategy.

### Detailed description

Simple Fake Strategy is the fifth feature in the corrected PyRiskLab feature list. Feature 1 creates the config-driven CLI foundation. Feature 2 generates synthetic market data. Feature 3 calculates Black-Scholes prices. Feature 4 calculates Greeks. Feature 5 uses those model outputs to create simple trading signals that later features can pass into fake execution, portfolio tracking, and risk validation.

This feature should not execute trades. It should only decide what the strategy *would like* to do at each step. The output should be a clean signal table saved to:

```text
results/<run_name>/signals.csv
```

Each signal should contain the simulation step, option symbol, action, quantity, reference price, relevant Greek values, and a plain-English reason. The strategy must be deterministic so the same config, same seed, and same upstream data produce the same signals every time.

The MVP strategy should be deliberately simple. The recommended rule is a **delta-threshold strategy**:

- generate a `BUY` signal when Delta is below a configured lower threshold,
- generate a `SELL` signal when Delta is above a configured upper threshold,
- otherwise generate `HOLD`.

The exact default thresholds should come from `configs/demo.yaml`.

This feature is not meant to prove trading profitability. It exists to create structured signals so later features can prove fake execution, portfolio state transitions, risk blocking, logging, and reporting.

### Why it matters

Without a strategy layer, PyRiskLab would calculate prices and Greeks but would not create a system flow into execution and portfolio state. A simple strategy creates the bridge between mathematical outputs and software-engineering behavior.

**Decision:** Build one simple deterministic strategy, not a flexible strategy framework.

**Justification:** The project should stay finishable and portfolio-focused. A complex strategy engine would distract from the stronger skills: clean architecture, testing, reproducibility, risk checks, and reporting.

**Decision:** Use Delta thresholds for the MVP strategy.

**Justification:** Delta is already produced by Feature 4, is easy to explain in interviews, and gives the strategy a clear reason for each action without pretending to predict real markets.

**Decision:** Save signals to `signals.csv` before fake execution happens.

**Justification:** Keeping signals separate from orders and trades makes debugging easier and proves clean separation of concerns.

**Decision:** Strategy should output structured signal objects, not directly mutate portfolio state.

**Justification:** Feature 5 should not do the job of Feature 6 or Feature 7. Execution and portfolio tracking need to remain separate and independently testable.

**Decision:** Include `HOLD` signals in the CSV for the full simulation path.

**Justification:** A full signal history makes the feature easier to inspect and debug. Reviewers can see why the strategy did or did not act at each step.

### Skill it demonstrates

- Rule-based decision logic.
- Clean function boundaries.
- Separating signals from orders and trades.
- pandas DataFrame transformation.
- Config-driven behavior.
- Deterministic output design.
- Testable business logic.
- Plain-English reason generation.
- Scope control by avoiding strategy optimization.
- Interview explanation of what is intentionally fake and simplified.

### Priority

**High / P1.**

This feature is required before Fake Execution, Portfolio Tracker, and Risk Manager feel like a real pipeline. It does not need to be complex, but it must be clean.

### Complexity

**Medium.**

The rules are simple, but the feature needs careful boundaries so it does not accidentally become execution, risk management, optimization, or a trading bot.

---

## 2. User/Demo Flow

### Happy path

1. User has Features 1–4 working.
2. User runs:

```bash
python -m pyrisklab run --config configs/demo.yaml
```

3. CLI loads the config.
4. Market Simulation creates `market_path.csv`.
5. Black-Scholes Pricing creates `pricing_history.csv`.
6. Greeks Calculation creates `greeks_history.csv`.
7. Strategy module reads the relevant pricing and Greek data.
8. Strategy applies the configured delta thresholds.
9. Strategy produces one signal per simulation step.
10. App saves:

```text
results/<run_name>/signals.csv
```

11. CLI prints:

```text
[5/12] Generating strategy signals...
Saved signals: results/demo_run/signals.csv
```

### First-time path

1. User opens `configs/demo.yaml`.
2. User sees a strategy section such as:

```yaml
strategy:
  name: simple_delta_rule
  buy_delta_below: 0.45
  sell_delta_above: 0.70
  trade_quantity: 1
  min_steps_between_trades: 5
```

3. User runs the normal demo command.
4. CLI explains that a simple fake strategy is being used.
5. User opens `signals.csv` and sees `BUY`, `SELL`, and `HOLD` rows with reasons.
6. User understands this is a fake strategy used for simulation flow, not a real trading system.

### Empty state

The strategy may produce only `HOLD` signals if thresholds are never crossed.

Expected behavior:

- `signals.csv` should still be created.
- CLI should not fail.
- Later execution feature should be able to handle no actionable signals.
- Summary/reporting later can say: “No actionable strategy signals were generated.”

Example empty-state rows:

```csv
step,symbol,action,quantity,reference_price,delta,reason
0,CALL_105,HOLD,0,3.21,0.52,"Delta 0.52 is between buy and sell thresholds."
1,CALL_105,HOLD,0,3.35,0.54,"Delta 0.54 is between buy and sell thresholds."
```

### Error path

Expected config or data errors should raise clear exceptions.

Examples:

```text
ConfigError: strategy.buy_delta_below must be less than strategy.sell_delta_above.
ConfigError: strategy.trade_quantity must be greater than 0.
StrategyError: greeks_history is missing required column 'delta'.
StrategyError: pricing_history and greeks_history have mismatched step values.
```

The CLI should catch expected project errors and print readable messages without a scary stack trace.

### Demo path for a reviewer

Reviewer runs:

```bash
python -m pyrisklab run --config configs/demo.yaml --overwrite
```

Then opens:

```text
results/demo_run/signals.csv
```

Reviewer should quickly see:

- the strategy name,
- the action chosen per step,
- the delta value used for each decision,
- the reference option price,
- the configured quantity,
- a readable reason column.

Recommended reviewer explanation:

> The strategy is intentionally simple. It reads the Greeks produced by the pricing engine and generates deterministic fake signals. I kept it simple because the purpose is to feed a testable execution and portfolio pipeline, not to claim market profitability.

---

## 3. UX/UI Requirements

### Screens/pages

This is a local CLI project, so the “screens” for this feature are:

1. **CLI progress output**
   - Shows that strategy signals are being generated.

2. **Generated `signals.csv` file**
   - Main inspectable artifact for the feature.

3. **Future summary report section**
   - Feature 9 Reporting may later summarize number of buy/sell/hold signals.

No web page, dashboard, login screen, or SaaS UI should be added for this feature.

### Components

#### CLI progress message

Minimum message:

```text
[5/12] Generating strategy signals...
Saved signals: results/demo_run/signals.csv
```

Optional helpful message:

```text
Strategy: simple_delta_rule | BUY below delta 0.45 | SELL above delta 0.70
```

#### Generated CSV table

`signals.csv` should be the main output.

Required columns:

```text
step
symbol
action
quantity
reference_price
delta
reason
```

Recommended additional columns:

```text
underlying_price
option_price
gamma
vega
time_to_expiry
strategy_name
```

### Forms/inputs

No interactive forms are needed.

Inputs come from `configs/demo.yaml`.

Recommended strategy config:

```yaml
strategy:
  name: simple_delta_rule
  buy_delta_below: 0.45
  sell_delta_above: 0.70
  trade_quantity: 1
  min_steps_between_trades: 5
```

#### Field meanings

| Field | Type | Required | Meaning |
|---|---:|---:|---|
| `strategy.name` | string | yes | Strategy identifier. MVP supports `simple_delta_rule`. |
| `strategy.buy_delta_below` | float | yes | Generate a buy signal when Delta is below this value. |
| `strategy.sell_delta_above` | float | yes | Generate a sell signal when Delta is above this value. |
| `strategy.trade_quantity` | int | yes | Requested quantity for actionable signals. |
| `strategy.min_steps_between_trades` | int | recommended | Prevents noisy buy/sell signals on every adjacent step. |

### Buttons/actions

No GUI buttons are needed.

CLI action:

```bash
python -m pyrisklab run --config configs/demo.yaml
```

This action should eventually run the entire pipeline, including strategy generation.

### Validation messages

Config validation should catch:

```text
ConfigError: strategy.name must be 'simple_delta_rule'. Received 'macd_bot'.
ConfigError: strategy.buy_delta_below must be between -1 and 1. Received 1.3.
ConfigError: strategy.sell_delta_above must be between -1 and 1. Received -1.2.
ConfigError: strategy.buy_delta_below must be less than strategy.sell_delta_above.
ConfigError: strategy.trade_quantity must be greater than 0. Received 0.
ConfigError: strategy.min_steps_between_trades must be >= 0. Received -2.
```

Data validation should catch:

```text
StrategyError: greeks_history must include a 'delta' column.
StrategyError: pricing_history must include an 'option_price' column.
StrategyError: strategy input data cannot be empty.
```

### Empty states

Handle these states cleanly:

#### No actionable signals

Expected output:

- `signals.csv` contains only `HOLD` rows.
- No error is raised.
- Later features should produce empty `orders.csv` or `trades.csv` gracefully.

#### Empty input data

Expected output:

- Raise `StrategyError`.
- Do not create misleading empty signals unless upstream explicitly allows empty simulation paths.

#### Missing Greeks

Expected output:

- Raise `StrategyError`.
- Tell the user that Feature 4 must run before Feature 5.

### Loading states

CLI progress is enough.

Example:

```text
[5/12] Generating strategy signals from Greeks history...
```

No spinners or live progress bars are required.

### Error states

Expected errors should be clear and actionable.

Bad threshold example:

```text
ConfigError: strategy.buy_delta_below must be less than strategy.sell_delta_above. Received 0.75 and 0.70.
```

Missing data example:

```text
StrategyError: Cannot generate signals because greeks_history is missing required column 'delta'.
```

### Responsive behavior if relevant

Not relevant for MVP.

This feature is CLI/file-output based. If a local dashboard is added much later, it may display `signals.csv`, but that is not part of this feature.

---

## 4. Data Requirements

### Entities involved

#### StrategyConfig

Controls how signals are generated.

Fields:

```text
name
buy_delta_below
sell_delta_above
trade_quantity
min_steps_between_trades
```

#### PricingRecord

Produced by Feature 3.

Required fields for this feature:

```text
step
symbol
underlying_price
option_price
time_to_expiry
```

#### GreekRecord

Produced by Feature 4.

Required fields for this feature:

```text
step
symbol
delta
gamma
vega
theta
rho
```

#### Signal

Created by this feature.

Required fields:

```text
step
symbol
action
quantity
reference_price
delta
reason
```

Recommended fields:

```text
underlying_price
option_price
gamma
vega
time_to_expiry
strategy_name
```

### Fields

#### Signal fields

| Field | Type | Example | Notes |
|---|---:|---|---|
| `step` | int | `35` | Simulation step. |
| `symbol` | string | `CALL_105` | Option symbol from config. |
| `action` | string | `BUY` | One of `BUY`, `SELL`, `HOLD`. |
| `quantity` | int | `1` | `0` for hold, configured quantity for actionable signals. |
| `reference_price` | float | `4.72` | Option price used as reference for later fake execution. |
| `underlying_price` | float | `101.34` | Useful for debugging. |
| `option_price` | float | `4.72` | Same as reference price unless renamed later. |
| `delta` | float | `0.43` | Main decision variable. |
| `gamma` | float | `0.035` | Optional but useful context. |
| `vega` | float | `0.112` | Optional but useful context. |
| `time_to_expiry` | float | `0.238` | In years. |
| `strategy_name` | string | `simple_delta_rule` | Helps scenario comparison later. |
| `reason` | string | `Delta 0.43 is below buy threshold 0.45.` | Human-readable explanation. |

### Relationships

- One `RunConfig` contains one `StrategyConfig`.
- One strategy run reads one pricing history and one Greeks history.
- Each simulation step produces one `Signal`.
- Actionable `BUY` and `SELL` signals can become fake orders in Feature 6.
- `HOLD` signals do not become orders.
- This feature does not modify positions or cash.

### Example seed data

Recommended config section:

```yaml
strategy:
  name: simple_delta_rule
  buy_delta_below: 0.45
  sell_delta_above: 0.70
  trade_quantity: 1
  min_steps_between_trades: 5
```

Example input row from `pricing_history.csv`:

```csv
step,symbol,underlying_price,time_to_expiry,option_price
35,CALL_105,99.84,0.218,3.95
```

Example input row from `greeks_history.csv`:

```csv
step,symbol,delta,gamma,vega,theta,rho
35,CALL_105,0.43,0.038,0.115,-0.021,0.086
```

Example output row in `signals.csv`:

```csv
step,symbol,action,quantity,reference_price,underlying_price,option_price,delta,gamma,vega,time_to_expiry,strategy_name,reason
35,CALL_105,BUY,1,3.95,99.84,3.95,0.43,0.038,0.115,0.218,simple_delta_rule,"Delta 0.43 is below buy threshold 0.45."
```

### Local persistence needs

This feature should save:

```text
results/<run_name>/signals.csv
```

No database is needed.

**Decision:** Use CSV for strategy signals.

**Justification:** CSV is easy to inspect, works naturally with pandas, is simple to test, and fits the local portfolio-project architecture.

---

## 5. Logic Requirements

### Business rules

#### Supported strategy names

MVP supports only:

```text
simple_delta_rule
```

Any other strategy name should raise `ConfigError`.

#### Action rules

For each row:

1. If `delta < buy_delta_below`, generate `BUY`.
2. Else if `delta > sell_delta_above`, generate `SELL`.
3. Else generate `HOLD`.

#### Quantity rules

- `BUY` uses `strategy.trade_quantity`.
- `SELL` uses `strategy.trade_quantity`.
- `HOLD` uses quantity `0`.

#### Reason rules

Each signal should have a clear reason.

Examples:

```text
Delta 0.43 is below buy threshold 0.45.
Delta 0.72 is above sell threshold 0.70.
Delta 0.55 is between buy threshold 0.45 and sell threshold 0.70.
```

#### Cooldown rule

`min_steps_between_trades` should prevent too many repeated actionable signals.

Recommended behavior:

- Track the most recent actionable signal step.
- If another actionable signal appears before the cooldown is reached, convert it to `HOLD`.
- Reason should explain the cooldown.

Example:

```text
Signal suppressed by cooldown: only 2 steps since last actionable signal; minimum is 5.
```

**Decision:** Include cooldown in the strategy config.

**Justification:** Without a cooldown, a threshold strategy can produce unrealistic repeated buy/sell signals on every step. A simple cooldown keeps the demo readable without adding complex trading logic.

#### No profitability claims

The strategy must not output performance claims. It only outputs signals.

### Calculations

No advanced calculations are needed beyond comparing Delta to thresholds.

Pseudo-code:

```python
if delta < config.buy_delta_below:
    action = "BUY"
elif delta > config.sell_delta_above:
    action = "SELL"
else:
    action = "HOLD"
```

Cooldown pseudo-code:

```python
if action in {"BUY", "SELL"}:
    if last_actionable_step is not None:
        if step - last_actionable_step < config.min_steps_between_trades:
            action = "HOLD"
            quantity = 0
            reason = "Signal suppressed by cooldown..."
    if action in {"BUY", "SELL"}:
        last_actionable_step = step
```

### API/service functions if needed

Recommended functions in `strategy.py`:

```python
def generate_signals(
    pricing_history: pd.DataFrame,
    greeks_history: pd.DataFrame,
    strategy_config: StrategyConfig,
) -> pd.DataFrame:
    """Generate deterministic strategy signals from pricing and Greeks history."""
```

Recommended helper functions:

```python
def validate_strategy_config(strategy_config: StrategyConfig) -> None:
    """Validate strategy config values."""


def validate_strategy_inputs(
    pricing_history: pd.DataFrame,
    greeks_history: pd.DataFrame,
) -> None:
    """Validate required columns and matching steps."""


def decide_action(
    delta: float,
    buy_delta_below: float,
    sell_delta_above: float,
) -> tuple[str, str]:
    """Return action and reason before cooldown handling."""
```

Optional dataclass in `models.py`:

```python
@dataclass(frozen=True)
class Signal:
    step: int
    symbol: str
    action: Literal["BUY", "SELL", "HOLD"]
    quantity: int
    reference_price: float
    delta: float
    reason: str
```

### State management

Strategy should be mostly stateless.

The only small internal state may be:

```text
last_actionable_step
```

This is used for cooldown handling inside a single call to `generate_signals(...)`.

Do not store strategy state globally.

Do not mutate pricing or Greeks input DataFrames in place.

### Edge cases

#### Delta exactly equals threshold

Recommended behavior:

- Use strict comparisons:
  - `delta < buy_delta_below` means buy.
  - `delta > sell_delta_above` means sell.
- If Delta equals either threshold exactly, output `HOLD`.

Justification: strict comparisons avoid ambiguous double-trigger behavior.

#### Missing `delta`

Raise `StrategyError`.

#### Missing `option_price`

Raise `StrategyError` because fake execution needs a reference price later.

#### Empty DataFrames

Raise `StrategyError`.

#### Mismatched steps

Raise `StrategyError` if pricing and Greeks rows do not align by `step` and `symbol`.

#### NaN Delta

Recommended behavior:

- Generate `HOLD` for that row.
- Reason: `Delta is missing or not finite; holding.`

Alternative:

- Raise `StrategyError`.

**Decision:** Use `HOLD` for isolated non-finite Delta values, but raise an error if the entire Delta column is invalid.

**Justification:** One bad edge value near expiry should not crash the whole demo, but a fully broken Greeks output should fail clearly.

#### Negative quantity

Config validation should reject it.

#### Zero quantity

Config validation should reject it.

#### Unknown action

Strategy should only produce `BUY`, `SELL`, or `HOLD`.

#### Multiple option symbols

[Open Question] Version 1 is expected to focus on one option contract. If multiple option contracts are added later, strategy output should include symbol-specific signals.

---

## 6. Acceptance Criteria

### Config validation

**Given** `strategy.name` is `simple_delta_rule`  
**When** the config is loaded  
**Then** the strategy config is accepted.

**Given** `strategy.name` is not supported  
**When** the config is loaded  
**Then** a `ConfigError` explains that only `simple_delta_rule` is supported in MVP.

**Given** `buy_delta_below` is greater than or equal to `sell_delta_above`  
**When** the config is loaded  
**Then** a `ConfigError` explains the threshold ordering problem.

**Given** `trade_quantity` is less than or equal to zero  
**When** the config is loaded  
**Then** a `ConfigError` explains that trade quantity must be greater than zero.

### Signal generation

**Given** a row has Delta below the buy threshold  
**When** strategy signals are generated  
**Then** the row receives action `BUY` with configured trade quantity.

**Given** a row has Delta above the sell threshold  
**When** strategy signals are generated  
**Then** the row receives action `SELL` with configured trade quantity.

**Given** a row has Delta between the thresholds  
**When** strategy signals are generated  
**Then** the row receives action `HOLD` with quantity `0`.

**Given** a row has Delta exactly equal to a threshold  
**When** strategy signals are generated  
**Then** the row receives action `HOLD`.

### Cooldown handling

**Given** an actionable signal was generated at step 10  
**And** `min_steps_between_trades` is `5`  
**When** another actionable signal appears at step 12  
**Then** the second signal is converted to `HOLD` with a cooldown reason.

**Given** an actionable signal was generated at step 10  
**And** `min_steps_between_trades` is `5`  
**When** another actionable signal appears at step 15  
**Then** the second actionable signal is allowed.

### Output

**Given** valid pricing and Greeks histories  
**When** strategy generation completes  
**Then** `results/<run_name>/signals.csv` is created.

**Given** no buy or sell conditions are triggered  
**When** strategy generation completes  
**Then** `signals.csv` still exists and contains `HOLD` rows.

**Given** signals are generated  
**When** the reviewer opens `signals.csv`  
**Then** each row has a readable `reason` explaining the action.

### Error handling

**Given** `greeks_history` is missing the `delta` column  
**When** strategy generation runs  
**Then** a `StrategyError` identifies the missing column.

**Given** `pricing_history` is missing the `option_price` column  
**When** strategy generation runs  
**Then** a `StrategyError` identifies the missing column.

**Given** pricing and Greeks histories have mismatched steps  
**When** strategy generation runs  
**Then** a `StrategyError` explains that the inputs are misaligned.

---

## 7. Test Plan

### Unit tests

Create or update:

```text
tests/test_strategy.py
```

Recommended tests:

1. **Valid config accepted**
   - `simple_delta_rule` with valid thresholds loads successfully.

2. **Invalid strategy name fails**
   - Unknown strategy name raises `ConfigError`.

3. **Invalid threshold ordering fails**
   - `buy_delta_below >= sell_delta_above` raises `ConfigError`.

4. **Invalid quantity fails**
   - Zero or negative quantity raises `ConfigError`.

5. **Delta below buy threshold creates BUY**
   - Input Delta `0.40`, buy threshold `0.45`, output action `BUY`.

6. **Delta above sell threshold creates SELL**
   - Input Delta `0.75`, sell threshold `0.70`, output action `SELL`.

7. **Delta between thresholds creates HOLD**
   - Input Delta `0.55`, output action `HOLD`.

8. **Delta equal to threshold creates HOLD**
   - Input Delta exactly `0.45` or `0.70`, output action `HOLD`.

9. **Hold quantity is zero**
   - Every `HOLD` row has quantity `0`.

10. **Actionable quantity uses config value**
    - `BUY` and `SELL` rows use `trade_quantity`.

11. **Cooldown suppresses repeated actionable signals**
    - Second actionable signal inside cooldown becomes `HOLD`.

12. **Missing delta column fails**
    - Raise `StrategyError`.

13. **Missing option price column fails**
    - Raise `StrategyError`.

14. **Empty input fails**
    - Empty pricing or Greeks history raises `StrategyError`.

15. **Output has required columns**
    - Generated DataFrame contains `step`, `symbol`, `action`, `quantity`, `reference_price`, `delta`, and `reason`.

16. **Input DataFrames are not mutated**
    - Make copies and verify original columns/values remain unchanged.

### Integration tests if useful

Create integration-style test after Features 1–5 are connected:

```text
tests/test_strategy_integration.py
```

Recommended integration tests:

1. Run config loading, market simulation, pricing, Greeks, and strategy generation together.
2. Verify `signals.csv` is saved to a temporary results folder.
3. Verify the signal row count matches the pricing/Greeks row count.
4. Verify at least one action is one of `BUY`, `SELL`, or `HOLD`.
5. Verify the run is deterministic for the same seed and config.

### Manual QA checklist

- [ ] Run `python -m pyrisklab run --config configs/demo.yaml --overwrite`.
- [ ] Confirm CLI prints strategy generation progress.
- [ ] Confirm `signals.csv` exists.
- [ ] Confirm `signals.csv` has readable headers.
- [ ] Confirm action values are only `BUY`, `SELL`, or `HOLD`.
- [ ] Confirm `HOLD` rows have quantity `0`.
- [ ] Confirm `BUY` and `SELL` rows use configured quantity.
- [ ] Confirm each row has a readable reason.
- [ ] Temporarily set impossible thresholds and confirm mostly/all `HOLD` rows.
- [ ] Temporarily set invalid threshold order and confirm a clear config error.
- [ ] Confirm no orders, trades, cash changes, or portfolio changes happen inside this feature.

### Demo verification checklist

- [ ] README can mention the strategy in one sentence.
- [ ] `signals.csv` looks understandable to a reviewer.
- [ ] The strategy is clearly labeled as fake/simulation-only.
- [ ] The strategy creates useful input for Feature 6 Fake Execution.
- [ ] No claims are made about profitability.
- [ ] No broker API, live market data, dashboard, or SaaS scope was added.

---

## 8. Portfolio Value

### How this feature helps the project stand out

Simple Fake Strategy makes PyRiskLab feel like an end-to-end system instead of a formula demo. It shows that the project can take model outputs and transform them into structured decisions that downstream modules can process.

The feature also creates a strong software-engineering discussion around boundaries:

- Pricing calculates values.
- Greeks calculate sensitivities.
- Strategy generates signals.
- Execution converts allowed signals into fake trades.
- Portfolio updates state.
- Risk manager blocks unsafe trades.

That separation is exactly what makes the project look more professional than a single notebook.

### What to mention in README

Recommended README wording:

```text
PyRiskLab includes a deliberately simple delta-threshold strategy that converts option Greeks into deterministic BUY, SELL, or HOLD signals. The strategy is not designed to predict markets or make money; it exists to drive the fake execution, portfolio, and risk-control pipeline in a reproducible way.
```

README should show example output:

```text
results/demo_run/signals.csv
```

Possible README table:

| Step | Delta | Action | Reason |
|---:|---:|---|---|
| 35 | 0.43 | BUY | Delta is below buy threshold. |
| 36 | 0.47 | HOLD | Delta is between thresholds. |
| 82 | 0.72 | SELL | Delta is above sell threshold. |

### What to mention in interviews

Strong interview explanation:

> I kept the strategy intentionally simple because the goal was not to build a trading algorithm. I wanted a deterministic decision layer that converts Greeks into structured signals, so the rest of the system could demonstrate execution, portfolio accounting, risk validation, logging, and testing.

If asked why not make a profitable strategy:

> Profitability was out of scope. The project is a simulation and software-engineering tool. The strategy exists to exercise system behavior, not to make investment claims.

If asked why use Delta:

> Delta was already produced by the Greeks engine and is easy to reason about. A threshold rule makes the strategy explainable and testable without adding ML or optimization complexity.

### Resume relevance

This feature supports resume language like:

```text
Implemented a deterministic rule-based signal generator that converts option Greeks into structured buy/sell/hold decisions for a local Python simulation pipeline.
```

Or as part of a bigger bullet:

```text
Built a modular Python options-risk simulator with config-driven runs, Black-Scholes pricing, Greeks, deterministic strategy signals, fake execution, portfolio tracking, risk checks, tests, and reproducible reports.
```

---

## 9. Implementation Notes For Codex

### Likely files/folders

Add or modify:

```text
src/pyrisklab/strategy.py
src/pyrisklab/models.py
src/pyrisklab/config.py
src/pyrisklab/exceptions.py
src/pyrisklab/pipeline.py
tests/test_strategy.py
configs/demo.yaml
```

Later related files:

```text
src/pyrisklab/reporting.py
README.md
```

### Recommended code structure

#### `models.py`

Add:

```python
@dataclass(frozen=True)
class StrategyConfig:
    name: str
    buy_delta_below: float
    sell_delta_above: float
    trade_quantity: int
    min_steps_between_trades: int = 0
```

Optional:

```python
@dataclass(frozen=True)
class Signal:
    step: int
    symbol: str
    action: str
    quantity: int
    reference_price: float
    delta: float
    reason: str
```

#### `exceptions.py`

Add:

```python
class StrategyError(PyRiskLabError):
    """Raised when strategy signal generation fails."""
```

#### `strategy.py`

Implement:

```python
def generate_signals(
    pricing_history: pd.DataFrame,
    greeks_history: pd.DataFrame,
    strategy_config: StrategyConfig,
) -> pd.DataFrame:
    ...
```

Keep this module focused. It should not:

- execute orders,
- update cash,
- update positions,
- enforce risk rules,
- create charts,
- run benchmarks,
- read or write files directly unless the architecture already places saving here.

Preferred design:

- `strategy.py` returns a DataFrame.
- `pipeline.py` passes the DataFrame to reporting/file-output logic.

### Build order

1. Add `StrategyConfig` to config/model layer.
2. Add strategy config validation.
3. Add `StrategyError`.
4. Write tests for `decide_action(...)` or `generate_signals(...)`.
5. Implement basic `BUY` / `SELL` / `HOLD` rules.
6. Add cooldown behavior.
7. Add required output columns.
8. Connect Feature 5 inside `pipeline.py` after Greeks.
9. Save `signals.csv` under `results/<run_name>/`.
10. Add CLI progress message.
11. Run tests.
12. Run full demo command and inspect `signals.csv`.

### Risks

#### Risk: Strategy becomes too complicated

Avoid adding:

- ML prediction,
- optimization,
- backtesting engine,
- many strategy classes,
- plugin registry,
- indicators like MACD/RSI,
- strategy performance claims.

#### Risk: Strategy directly executes trades

Keep signals separate from orders and trades. Feature 6 owns fake execution.

#### Risk: Too many repeated signals

Use `min_steps_between_trades` to keep output readable.

#### Risk: Confusing financial interpretation

Clearly label the strategy as fake and simulation-only.

#### Risk: DataFrame alignment bugs

Validate that pricing and Greeks histories align by `step` and `symbol` before generating signals.

### What not to change

- Do not rename the main CLI command.
- Do not add real market data.
- Do not add brokerage integration.
- Do not add real trading.
- Do not add a dashboard.
- Do not add a database.
- Do not change pricing formulas.
- Do not move Greek logic into strategy.
- Do not move execution logic into strategy.
- Do not make the strategy profitability-focused.
- Do not turn this into a SaaS feature.

### [Open Question]

- [Open Question] Should `SELL` signals be allowed before the portfolio owns the option, or should that only be blocked later by Fake Execution / Portfolio Tracker?
  - Recommended answer: allow the strategy to emit `SELL`; let execution/portfolio/risk decide whether it is valid. This keeps strategy separate from stateful ownership logic.

- [Open Question] Should the demo thresholds be chosen to guarantee at least one `BUY` and one `SELL` signal?
  - Recommended answer: yes, tune `configs/demo.yaml` so the default demo produces at least one actionable signal, but tests should not depend on random luck.

- [Open Question] Should `signals.csv` include all `HOLD` rows or only actionable rows?
  - Recommended answer: include all rows for inspectability; downstream execution can filter actionable rows.

---

## Move-On Checklist

- [ ] Strategy config exists and is validated.
- [ ] Only `simple_delta_rule` is supported in MVP.
- [ ] Strategy reads pricing and Greeks data.
- [ ] Strategy outputs deterministic `BUY`, `SELL`, and `HOLD` signals.
- [ ] `signals.csv` is saved under `results/<run_name>/`.
- [ ] Signal reasons are readable.
- [ ] Tests cover threshold behavior, cooldown, invalid config, and missing columns.
- [ ] Feature does not execute trades or update portfolio state.
- [ ] Feature does not claim profitability.
- [ ] Demo path is obvious for reviewers.
