# Feature 3 — Black-Scholes Pricing

## 1. Feature Overview

### Feature name

**Black-Scholes Pricing**

### One-sentence description

Calculate European call and put option prices over the simulated market path using a validated, vectorized Black-Scholes pricing engine.

### Detailed description

Black-Scholes Pricing is the third feature in the corrected PyRiskLab feature list. Feature 1 gives the project a config-driven CLI. Feature 2 generates deterministic synthetic market data. Feature 3 turns that market path into option-pricing data by applying the Black-Scholes formula to each simulated underlying price.

This feature should read the validated `option` section from `configs/demo.yaml`, combine it with `market_path.csv` or the in-memory market DataFrame, calculate call or put prices at each step, and save the pricing output to:

```text
results/<run_name>/pricing_history.csv
```

The pricing engine should support both European calls and European puts. The demo can focus on one configured option contract, such as `CALL_105`, but the function design should not hardcode one option type. The pricing logic must be separated from CLI, reporting, strategy, execution, portfolio, risk, Greeks, and benchmarking. This feature does not calculate Greeks. Greeks are Feature 4.

The project should present Black-Scholes as a controlled mathematical model used for simulation and software-engineering practice. It should not claim to predict real markets, recommend trades, or produce investment advice.

### Why it matters

Black-Scholes Pricing gives PyRiskLab its first real domain engine. Market Simulation creates the input data, but pricing turns that input into something technically meaningful: option values over time. This creates a strong software-engineering feature because the formula must be implemented cleanly, validated, tested with known values, vectorized for performance, and integrated into the run pipeline.

**Decision:** Implement Black-Scholes pricing as a reusable Python function in `pricing.py`.

**Justification:** Pricing is core domain logic and should not live in the CLI, pipeline, notebook, or reporting code. Keeping it in a focused module makes it easier to test, debug, benchmark, and explain in interviews.

**Decision:** Support both `call` and `put` option types.

**Justification:** Supporting both makes the pricing engine complete enough to look professional, while still staying within Version 1 scope. It also enables important tests such as put-call parity.

**Decision:** Use vectorized NumPy operations where practical.

**Justification:** The project is meant to demonstrate performance-aware Python. Vectorized pricing over a full price path is more impressive and more scalable than looping through one row at a time in ordinary Python.

**Decision:** Use SciPy's normal distribution functions for the standard normal CDF.

**Justification:** SciPy is already part of the chosen numerical stack and avoids hand-rolled approximations that could make correctness harder to defend.

**Decision:** Keep Greeks out of this feature.

**Justification:** Greeks are a separate feature in the corrected list. Splitting them prevents the pricing spec from becoming bloated and gives Codex a cleaner build sequence.

### Skill it demonstrates

- Numerical model implementation.
- Vectorized NumPy computation.
- SciPy statistical functions.
- Clean domain-module design.
- Input validation for mathematical functions.
- Handling financial edge cases such as expiry and zero volatility.
- pandas output construction.
- Known-value unit testing.
- Put-call parity testing.
- Separation of pricing logic from CLI/reporting code.
- Interview-ready explanation of assumptions and limitations.

### Priority

**Critical / P0.**

Black-Scholes Pricing is required before Greeks, strategy, execution, portfolio tracking, risk reporting, and benchmark comparisons become meaningful.

### Complexity

**Medium to High.**

The formula itself is manageable, but the feature needs careful validation, vectorized shape handling, expiry behavior, zero-volatility behavior, known-value tests, and clean integration with the pipeline.

---

## 2. User/Demo Flow

### Happy path

1. User has already built Feature 1 and Feature 2.
2. User runs:

```bash
python -m pyrisklab run --config configs/demo.yaml
```

3. CLI loads the config.
4. Market simulation generates the underlying path.
5. Pricing module receives:
   - simulated underlying prices,
   - option type,
   - strike,
   - risk-free rate,
   - volatility,
   - time to expiry.
6. Pricing module calculates the option price for every market step.
7. App saves:

```text
results/<run_name>/pricing_history.csv
```

8. CLI prints a clear progress message such as:

```text
[3/12] Pricing option with Black-Scholes...
Saved pricing history: results/demo_run/pricing_history.csv
```

### First-time path

1. User opens `configs/demo.yaml`.
2. User sees an `option` section with readable values:

```yaml
option:
  underlying_symbol: SIM_STOCK
  symbol: CALL_105
  option_type: call
  strike: 105.0
  risk_free_rate: 0.04
  volatility: 0.20
  days_to_expiry: 90
```

3. User runs the normal CLI command.
4. App uses the option config without requiring any manual Python editing.
5. User opens `pricing_history.csv` and sees a row-by-row pricing table.

### Empty state

Black-Scholes pricing depends on a market path. If no market path exists in memory or on disk, the pricing step should not silently produce an empty output.

Expected behavior:

```text
PricingError: market path is empty. Run market simulation before pricing options.
```

If `market_path.csv` exists but contains zero rows:

```text
PricingError: market_path.csv has no rows to price.
```

### Error path

Common user/config errors should produce clean messages.

Examples:

```text
ConfigError: option.option_type must be 'call' or 'put'. Received 'calls'.
ConfigError: option.strike must be greater than 0. Received 0.
ConfigError: option.volatility must be >= 0. Received -0.1.
ConfigError: option.days_to_expiry must be >= 0. Received -5.
PricingError: underlying_price must be greater than 0. Received 0 at step 14.
```

The CLI should catch expected project errors and print readable output without a giant stack trace.

### Demo path for a reviewer

1. Reviewer clones repo.
2. Reviewer installs dependencies.
3. Reviewer runs:

```bash
pytest tests/test_pricing.py
python -m pyrisklab run --config configs/demo.yaml --overwrite
```

4. Reviewer opens:

```text
results/demo_run/pricing_history.csv
```

5. Reviewer verifies columns such as:

```text
step, time_years, underlying_price, time_to_expiry, option_symbol, option_type, strike, risk_free_rate, volatility, option_price
```

6. Reviewer sees that pricing is deterministic when the same seed/config is used.
7. Reviewer can inspect `src/pyrisklab/pricing.py` and see a focused, testable implementation.

---

## 3. UX/UI Requirements

### Screens/pages

This is a local CLI project, so the main user-facing surfaces are:

1. **CLI progress output**
   - Shows when pricing starts and ends.
   - Shows where `pricing_history.csv` was saved.

2. **Config file**
   - User edits `option` fields in `configs/demo.yaml`.
   - Values should be readable and commented if helpful.

3. **Generated pricing CSV**
   - Main output of Feature 3.
   - Must be easy to inspect in VS Code, Excel, pandas, or GitHub.

4. **Tests**
   - Pricing tests should make the mathematical correctness visible to technical reviewers.

Charting is not the responsibility of Feature 3. Price charts belong to the Reporting feature.

### Components

Expected code-level components:

- `OptionConfig` dataclass or equivalent config object.
- `OptionContract` dataclass or equivalent model.
- `black_scholes_price(...)` function.
- `price_market_path(...)` service-style function.
- `PricingError` custom exception.
- `pricing_history` pandas DataFrame.

### Forms/inputs

No web forms are needed.

Inputs come from YAML config and market-path data.

Minimum option config fields:

```yaml
option:
  underlying_symbol: SIM_STOCK
  symbol: CALL_105
  option_type: call
  strike: 105.0
  risk_free_rate: 0.04
  volatility: 0.20
  days_to_expiry: 90
```

Field meanings:

| Field | Type | Required | Purpose |
|---|---:|---:|---|
| `underlying_symbol` | string | Yes | Human-readable symbol for simulated stock. |
| `symbol` | string | Yes | Human-readable option symbol used in outputs. |
| `option_type` | string | Yes | Must be `call` or `put`. |
| `strike` | float | Yes | Option strike price. |
| `risk_free_rate` | float | Yes | Annualized risk-free rate used in pricing. |
| `volatility` | float | Yes | Annualized option volatility. |
| `days_to_expiry` | int/float | Yes | Initial calendar/trading-day style time to expiry used by the simulation. |

[Open Question] Should `days_to_expiry` decrease by calendar days, trading days, or simply proportional simulation steps?

Recommended MVP decision: decrease it linearly across the simulated steps using the configured market `trading_days` value. This is easy to test and explain.

### Buttons/actions

No buttons are needed.

CLI action:

```bash
python -m pyrisklab run --config configs/demo.yaml
```

Optional future CLI action after the core pipeline works:

```bash
python -m pyrisklab price --config configs/demo.yaml --market-path results/demo_run/market_path.csv
```

Do not add the standalone `price` command unless it provides clear debugging value. The main supported path should remain the full `run` command.

### Validation messages

Required validation messages:

```text
ConfigError: option section is required.
ConfigError: option.symbol is required.
ConfigError: option.option_type must be 'call' or 'put'. Received '<value>'.
ConfigError: option.strike must be greater than 0. Received <value>.
ConfigError: option.volatility must be >= 0. Received <value>.
ConfigError: option.days_to_expiry must be >= 0. Received <value>.
ConfigError: option.risk_free_rate must be numeric. Received <value>.
PricingError: market path must include column 'underlying_price'.
PricingError: market path is empty. Run market simulation before pricing options.
```

### Empty states

- Empty market path: fail clearly.
- Missing option config: fail clearly.
- Expired option at start: valid state if `days_to_expiry` is `0`; price should equal intrinsic value.
- All option prices are `0`: valid state for deep out-of-the-money expired options; do not treat as an error.

### Loading states

CLI progress output is enough.

Example:

```text
[3/12] Pricing option with Black-Scholes...
Calculated 253 option prices for CALL_105.
Saved pricing history: results/demo_run/pricing_history.csv
```

### Error states

Expected errors should be custom project errors. They should not appear as raw NumPy warnings, SciPy tracebacks, or pandas key errors during normal user mistakes.

Examples:

```text
PricingError: market path must include column 'underlying_price'.
PricingError: option pricing produced non-finite values. Check volatility, rate, and time_to_expiry.
```

### Responsive behavior if relevant

Not relevant for MVP. There is no web UI for this feature.

---

## 4. Data Requirements

### Entities involved

#### 1. `OptionConfig`

Represents the validated option section from the config file.

Fields:

- `underlying_symbol`
- `symbol`
- `option_type`
- `strike`
- `risk_free_rate`
- `volatility`
- `days_to_expiry`

#### 2. `OptionContract`

Represents the option being priced inside the domain model.

Fields:

- `underlying_symbol`
- `symbol`
- `option_type`
- `strike`
- `risk_free_rate`
- `volatility`
- `initial_days_to_expiry`

Decision:

Use a dataclass for `OptionContract`.

Justification:

A dataclass is lightweight, typed, readable, and avoids adding heavier validation libraries before they are needed.

#### 3. `MarketPath`

Input generated by Feature 2.

Minimum columns:

- `step`
- `time_years`
- `underlying_price`
- Optional: `path_id`

#### 4. `PricingRecord`

One output row per market step.

Fields:

- `step`
- `time_years`
- `underlying_price`
- `time_to_expiry`
- `option_symbol`
- `option_type`
- `strike`
- `risk_free_rate`
- `volatility`
- `option_price`

### Fields

Required `pricing_history.csv` columns:

```text
step
time_years
underlying_price
time_to_expiry
option_symbol
option_type
strike
risk_free_rate
volatility
option_price
```

Optional columns:

```text
path_id
intrinsic_value
extrinsic_value
```

Decision:

Include `intrinsic_value` and `extrinsic_value` only if they are simple and tested.

Justification:

They are helpful for understanding option value, but the core acceptance criteria should not depend on optional columns.

### Relationships

- One `RunConfig` contains one `OptionConfig` for MVP.
- One `MarketPath` feeds one `pricing_history` table.
- One `OptionContract` is priced across many market steps.
- One row in `market_path.csv` maps to one row in `pricing_history.csv` for the configured option.
- Greeks in Feature 4 will read the same market path and option settings, but this feature should not calculate or store Greek columns.

### Example seed data

Recommended `configs/demo.yaml` section:

```yaml
option:
  underlying_symbol: SIM_STOCK
  symbol: CALL_105
  option_type: call
  strike: 105.0
  risk_free_rate: 0.04
  volatility: 0.20
  days_to_expiry: 90
```

Example `pricing_history.csv` rows:

```csv
step,time_years,underlying_price,time_to_expiry,option_symbol,option_type,strike,risk_free_rate,volatility,option_price
0,0.000000,100.000000,0.357143,CALL_105,call,105.0,0.04,0.20,3.621442
1,0.003968,100.639743,0.353175,CALL_105,call,105.0,0.04,0.20,3.925771
2,0.007937,100.476546,0.349206,CALL_105,call,105.0,0.04,0.20,3.804119
```

The exact values will depend on the implementation and time-to-expiry convention.

### Local persistence needs

Feature 3 should write:

```text
results/<run_name>/pricing_history.csv
```

It may also return the pricing DataFrame to the pipeline so later features can use it in memory.

Decision:

Save CSV in the results folder and pass the DataFrame forward in the pipeline.

Justification:

CSV gives reviewers a visible artifact. Passing the DataFrame avoids rereading files unnecessarily inside one run.

No database is needed.

---

## 5. Logic Requirements

### Business rules

1. Option type must be either `call` or `put`.
2. Strike must be greater than `0`.
3. Underlying prices must be greater than `0`.
4. Volatility must be greater than or equal to `0`.
5. Days to expiry must be greater than or equal to `0`.
6. Time to expiry should never become negative in the pricing table.
7. At expiry, option price should equal intrinsic value:
   - Call: `max(S - K, 0)`
   - Put: `max(K - S, 0)`
8. For normal non-expired options, use the Black-Scholes formula.
9. Pricing output must be deterministic for the same market path and config.
10. Pricing should not mutate the input market path DataFrame in surprising ways.

### Calculations

Use these Black-Scholes concepts:

- `S`: underlying price.
- `K`: strike price.
- `r`: annualized risk-free rate.
- `sigma`: annualized volatility.
- `T`: time to expiry in years.
- `N(x)`: standard normal cumulative distribution function.

For `T > 0` and `sigma > 0`:

```text
d1 = [ln(S / K) + (r + 0.5 * sigma^2) * T] / [sigma * sqrt(T)]
d2 = d1 - sigma * sqrt(T)
```

Call price:

```text
C = S * N(d1) - K * exp(-r * T) * N(d2)
```

Put price:

```text
P = K * exp(-r * T) * N(-d2) - S * N(-d1)
```

At `T == 0`, use intrinsic value instead of the formula.

At `sigma == 0`, use the discounted deterministic payoff:

```text
call = max(S - K * exp(-r * T), 0)
put = max(K * exp(-r * T) - S, 0)
```

Decision:

Handle `T == 0` and `sigma == 0` explicitly before computing `d1` and `d2`.

Justification:

This prevents division-by-zero warnings and makes edge-case behavior testable.

### API/service functions if needed

Recommended functions in `src/pyrisklab/pricing.py`:

```python
def black_scholes_price(
    underlying_price: float | np.ndarray,
    strike: float,
    risk_free_rate: float,
    volatility: float,
    time_to_expiry: float | np.ndarray,
    option_type: str,
) -> float | np.ndarray:
    """Return Black-Scholes price for a European call or put."""
```

```python
def price_market_path(
    market_path: pd.DataFrame,
    option: OptionContract,
    trading_days: int,
) -> pd.DataFrame:
    """Return pricing history for the configured option over the market path."""
```

Recommended helper functions:

```python
def intrinsic_value(
    underlying_price: float | np.ndarray,
    strike: float,
    option_type: str,
) -> float | np.ndarray:
    ...
```

```python
def validate_pricing_inputs(...):
    ...
```

### State management

Feature 3 should be stateless.

- It receives config/domain objects and market path data.
- It returns a pricing DataFrame.
- It does not store global state.
- It does not update portfolio state.
- It does not create trades.
- It does not apply risk rules.

Decision:

Keep pricing as pure as possible.

Justification:

Pure pricing logic is easier to unit test and easier to benchmark later.

### Edge cases

Must handle:

- `option_type = call`.
- `option_type = put`.
- `option_type` typo.
- Expired option: `days_to_expiry = 0`.
- Time to expiry reaches zero before final step.
- Zero volatility.
- Negative volatility.
- Strike equal to zero.
- Strike less than zero.
- Underlying price equal to zero.
- Underlying price less than zero.
- Very deep in-the-money call.
- Very deep out-of-the-money call.
- Very deep in-the-money put.
- Very deep out-of-the-money put.
- Empty market path.
- Missing `underlying_price` column.
- Non-finite values: `NaN`, `inf`, `-inf`.
- Vectorized array input returns the expected shape.

[Open Question] Should negative risk-free rates be allowed?

Recommended MVP decision: allow negative risk-free rates if they are numeric and finite, because Black-Scholes can mathematically handle them. Add a README note that the demo uses a positive value.

---

## 6. Acceptance Criteria

### AC1 — Valid call pricing works

**Given** a valid market path and an option config with `option_type: call`  
**When** the pricing step runs  
**Then** the app calculates a call option price for every market step  
**And** saves `results/<run_name>/pricing_history.csv`.

### AC2 — Valid put pricing works

**Given** a valid market path and an option config with `option_type: put`  
**When** the pricing step runs  
**Then** the app calculates a put option price for every market step  
**And** the output file uses `option_type` value `put`.

### AC3 — Output file has required columns

**Given** pricing has completed successfully  
**When** the user opens `pricing_history.csv`  
**Then** it includes `step`, `time_years`, `underlying_price`, `time_to_expiry`, `option_symbol`, `option_type`, `strike`, `risk_free_rate`, `volatility`, and `option_price`.

### AC4 — Same inputs produce same prices

**Given** the same config and same generated market path  
**When** the pricing step is run twice  
**Then** `pricing_history.csv` contains the same option prices.

### AC5 — Invalid option type fails clearly

**Given** `option.option_type` is `calls`  
**When** the user runs the CLI  
**Then** the run fails with a clear config error  
**And** the message says the option type must be `call` or `put`.

### AC6 — Invalid strike fails clearly

**Given** `option.strike` is `0` or negative  
**When** the user runs the CLI  
**Then** the run fails before pricing  
**And** the message identifies `option.strike` as the invalid field.

### AC7 — Expiry uses intrinsic value

**Given** `time_to_expiry` is `0`  
**When** Black-Scholes pricing is called  
**Then** the returned price equals the option's intrinsic value  
**And** no division-by-zero warning is produced.

### AC8 — Zero volatility is handled

**Given** `option.volatility` is `0`  
**When** Black-Scholes pricing is called for `T > 0`  
**Then** the returned price uses deterministic discounted payoff behavior  
**And** no division-by-zero warning is produced.

### AC9 — Missing market path fails clearly

**Given** no market path data is available  
**When** the pricing step starts  
**Then** the run fails with `PricingError`  
**And** the message explains that market simulation must run before pricing.

### AC10 — Vectorized input works

**Given** an array of underlying prices and an array of times to expiry  
**When** `black_scholes_price(...)` is called  
**Then** it returns an array with the expected shape  
**And** all normal-case prices are finite.

---

## 7. Test Plan

### Unit tests

Create or update:

```text
tests/test_pricing.py
```

Required tests:

1. **Known call price test**
   - Use a standard known-value case.
   - Assert price is approximately expected within tolerance.

2. **Known put price test**
   - Use a standard known-value case.
   - Assert price is approximately expected within tolerance.

3. **Put-call parity test**
   - Check that `C - P ≈ S - K * exp(-rT)` for normal inputs.

4. **Expired call intrinsic value test**
   - `T = 0`, call price equals `max(S - K, 0)`.

5. **Expired put intrinsic value test**
   - `T = 0`, put price equals `max(K - S, 0)`.

6. **Zero volatility call test**
   - No crash and deterministic payoff behavior.

7. **Zero volatility put test**
   - No crash and deterministic payoff behavior.

8. **Invalid option type test**
   - `option_type="calls"` raises a clear error.

9. **Invalid strike test**
   - `strike <= 0` raises a clear error.

10. **Invalid underlying price test**
   - `S <= 0` raises a clear error.

11. **Negative volatility test**
   - `volatility < 0` raises a clear error.

12. **Vectorized shape test**
   - Array input returns array output of the same expected shape.

13. **Non-finite input test**
   - `NaN` or `inf` fails clearly.

### Integration tests if useful

Create or update:

```text
tests/test_pipeline_pricing_integration.py
```

Useful integration tests:

1. Valid demo config creates `pricing_history.csv`.
2. Pricing history row count matches market path row count.
3. Pricing history contains required columns.
4. Invalid option config fails before writing pricing output.
5. Re-running with `--overwrite` replaces the old pricing output cleanly.

Keep integration tests lightweight. Do not require plotting, strategy, execution, portfolio, risk, reporting, or benchmark features for Feature 3.

### Manual QA checklist

- [ ] Run `pytest tests/test_pricing.py`.
- [ ] Run the normal demo command.
- [ ] Confirm `results/demo_run/pricing_history.csv` exists.
- [ ] Confirm row count matches `market_path.csv`.
- [ ] Confirm all `option_price` values are finite for normal config.
- [ ] Change `option_type` from `call` to `put` and rerun.
- [ ] Confirm output says `put` and prices are generated.
- [ ] Set invalid `option_type: calls` and confirm clear error.
- [ ] Set `strike: 0` and confirm clear error.
- [ ] Set `volatility: 0` and confirm no crash.
- [ ] Set `days_to_expiry: 0` and confirm intrinsic-value behavior.

### Demo verification checklist

- [ ] README/demo instructions still show one main command.
- [ ] The CLI output includes a pricing progress step.
- [ ] `pricing_history.csv` is easy to inspect.
- [ ] `src/pyrisklab/pricing.py` is focused and readable.
- [ ] `tests/test_pricing.py` proves correctness with known values and edge cases.
- [ ] There are no claims about real trading or profitability.

---

## 8. Portfolio Value

### How this feature helps the project stand out

Black-Scholes Pricing makes PyRiskLab feel more technical than a generic data project. It shows that the project has a real mathematical engine, not just CSV manipulation. More importantly, it gives interviewers something concrete to inspect: function design, vectorization, input validation, known-value tests, and edge-case handling.

This feature also supports the project’s main positioning: finance is the domain, but the real skill signal is clean Python engineering.

### What to mention in README

Mention:

- PyRiskLab prices European call and put options using Black-Scholes.
- Pricing is run over a deterministic synthetic market path.
- The output is saved as `pricing_history.csv`.
- The implementation is local and reproducible.
- Tests validate known pricing values, put-call parity, expiry handling, zero volatility, and invalid inputs.
- This is simulation only and not investment advice.

Suggested README wording:

```text
The pricing engine applies Black-Scholes call/put formulas over the simulated market path and exports a reproducible pricing history. Tests cover known benchmark values, put-call parity, expiry behavior, zero-volatility cases, and invalid inputs.
```

### What to mention in interviews

Strong interview talking points:

- “I kept pricing logic separate from CLI and reporting so it could be tested directly.”
- “I used vectorized NumPy inputs so pricing can run across a full path efficiently.”
- “I added explicit handling for expiry and zero volatility to avoid hidden divide-by-zero bugs.”
- “I tested known call/put prices and put-call parity instead of trusting the formula blindly.”
- “I intentionally kept Greeks as a separate module/feature so the pricing engine stayed focused.”
- “This is not a trading bot; it is a local simulation system designed to demonstrate correctness and software design.”

---

## 9. Implementation Notes For Codex

### Likely files/folders

Create or update:

```text
src/pyrisklab/pricing.py
src/pyrisklab/models.py
src/pyrisklab/config.py
src/pyrisklab/pipeline.py
src/pyrisklab/exceptions.py
tests/test_pricing.py
tests/test_pipeline_pricing_integration.py
configs/demo.yaml
results/.gitkeep
```

Feature 3 should produce:

```text
results/<run_name>/pricing_history.csv
```

### Build order

1. Confirm Feature 1 CLI and Feature 2 market simulation work.
2. Add or confirm `OptionConfig` validation in `config.py`.
3. Add or confirm `OptionContract` model in `models.py`.
4. Add `PricingError` in `exceptions.py`.
5. Implement `intrinsic_value(...)` in `pricing.py`.
6. Implement `black_scholes_price(...)` for scalar normal inputs.
7. Add known call and put tests.
8. Add expiry and zero-volatility handling.
9. Add invalid-input tests.
10. Add vectorized input support.
11. Implement `price_market_path(...)`.
12. Connect pricing step inside `pipeline.py` after market simulation.
13. Save `pricing_history.csv` in the run folder.
14. Add integration test for generated pricing history.
15. Update README later when Feature 12/Polished README is reached.

### Risks

| Risk | Why it matters | Mitigation |
|---|---|---|
| Mixing Greeks into pricing too early | Bloats Feature 3 and breaks the corrected feature list | Keep Greek columns out of `pricing_history.csv` for now. |
| Formula works for scalars but fails for arrays | Benchmark and path pricing need vectorization | Add vectorized shape tests. |
| Division by zero at expiry | Causes warnings or broken values | Handle `T == 0` explicitly. |
| Division by zero at zero volatility | Causes warnings or broken values | Handle `sigma == 0` explicitly. |
| Weak tests | Formula bugs may look correct visually | Add known-value and put-call parity tests. |
| Hidden dependency on market feature internals | Makes future refactors painful | Require a simple market DataFrame contract: `step`, `time_years`, `underlying_price`. |
| Output format changes later | Breaks downstream features | Lock required `pricing_history.csv` columns in tests. |

### What not to change

- Do not change the main CLI command.
- Do not add live market data.
- Do not add broker APIs.
- Do not add real trading.
- Do not add a web API.
- Do not add Streamlit for this feature.
- Do not add database storage.
- Do not calculate Greeks in this feature.
- Do not implement strategy, execution, portfolio, risk, reporting charts, tests suite expansion, or benchmark here beyond the pricing-specific tests.
- Do not claim the model predicts market prices.
- Do not claim the strategy is profitable.

### Suggested implementation skeleton

```python
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import norm

from pyrisklab.exceptions import PricingError
from pyrisklab.models import OptionContract


def intrinsic_value(underlying_price, strike: float, option_type: str):
    prices = np.asarray(underlying_price, dtype=float)
    if option_type == "call":
        return np.maximum(prices - strike, 0.0)
    if option_type == "put":
        return np.maximum(strike - prices, 0.0)
    raise PricingError(f"option_type must be 'call' or 'put'. Received {option_type!r}.")


def black_scholes_price(
    underlying_price,
    strike: float,
    risk_free_rate: float,
    volatility: float,
    time_to_expiry,
    option_type: str,
):
    # Validate inputs first.
    # Convert to arrays.
    # Handle T == 0.
    # Handle volatility == 0.
    # Compute d1, d2.
    # Return call or put price.
    ...


def price_market_path(
    market_path: pd.DataFrame,
    option: OptionContract,
    trading_days: int,
) -> pd.DataFrame:
    # Validate required market columns.
    # Compute time_to_expiry per row.
    # Price option over the full path.
    # Return pricing_history DataFrame.
    ...
```

Do not copy this skeleton blindly if the existing project structure uses slightly different names. Preserve the established architecture from Feature 1 and Feature 2.

---

## Move-On Checklist

- [ ] `black_scholes_price(...)` supports call and put pricing.
- [ ] `price_market_path(...)` returns a clean pricing DataFrame.
- [ ] `pricing_history.csv` is saved under `results/<run_name>/`.
- [ ] Required pricing output columns are tested.
- [ ] Known call and put tests pass.
- [ ] Put-call parity test passes.
- [ ] Expiry behavior is tested.
- [ ] Zero-volatility behavior is tested.
- [ ] Invalid inputs raise clear errors.
- [ ] Vectorized input behavior is tested.
- [ ] No Greeks are implemented in this feature.
- [ ] No SaaS, dashboard, live market data, broker integration, or database scope is added.
