# Feature 4 — Greeks Calculation

## 1. Feature Overview

### Feature name

**Greeks Calculation**

### One-sentence description

Calculate option risk sensitivities — Delta, Gamma, Vega, Theta, and Rho — over the simulated market path using Black-Scholes Greek formulas.

### Detailed description

Greeks Calculation is the fourth feature in the corrected PyRiskLab feature list. Feature 1 provides the config-driven CLI. Feature 2 generates deterministic synthetic market paths. Feature 3 calculates Black-Scholes option prices. Feature 4 adds the risk-sensitivity layer that explains how the configured option responds to changes in underlying price, volatility, time, and interest rates.

This feature should read the validated `option` config and the generated market path, compute Greeks for every simulated market step, and save the output to:

```text
results/<run_name>/greeks_history.csv
```

The feature should calculate these five Greeks:

- `delta`
- `gamma`
- `vega`
- `theta`
- `rho`

The demo should remain focused on one configured option contract, such as `CALL_105`. The implementation should support both `call` and `put` option types because the Black-Scholes Pricing feature already supports both. This feature should not generate trades, update portfolio state, enforce risk rules, create charts, run benchmarks, or build a dashboard.

The purpose of this feature is not to make trading recommendations. It exists to make the simulation richer and to prove that the project can handle numerical formulas, vectorized calculations, edge cases, tests, and clean data outputs.

### Why it matters

Greeks make PyRiskLab look more like a serious simulation and risk-analysis engine instead of a basic option-price calculator. Option price alone tells the reviewer what the option is worth in the model. Greeks explain how sensitive that value is to different inputs.

**Decision:** Implement Greeks in a focused `greeks.py` module.

**Justification:** Greeks are domain logic and should be directly testable. They should not live inside the CLI, reporting code, strategy code, portfolio code, or benchmark code.

**Decision:** Calculate Delta, Gamma, Vega, Theta, and Rho for both calls and puts.

**Justification:** These are the standard first set of Greeks expected in an option-pricing project. Supporting both option types makes the engine feel complete without expanding into advanced models.

**Decision:** Use vectorized NumPy/SciPy calculations where practical.

**Justification:** PyRiskLab is meant to demonstrate performance-aware Python. Calculating Greeks over the full path using vectorized operations is cleaner and more professional than row-by-row loops.

**Decision:** Save Greeks separately from `pricing_history.csv`.

**Justification:** The corrected feature list separates Black-Scholes Pricing from Greeks Calculation. Keeping `greeks_history.csv` separate makes each feature easier to test and easier for a reviewer to inspect.

**Decision:** Use readable units in output columns.

**Justification:** Greeks can confuse non-finance reviewers if units are unclear. The output should document whether Vega and Rho are per 1% change, and whether Theta is per day or per year.

### Skill it demonstrates

- Numerical formula implementation.
- Vectorized NumPy computation.
- SciPy normal PDF/CDF usage.
- Clean separation of domain logic.
- Input validation for mathematical edge cases.
- Handling near-expiry and zero-volatility behavior.
- pandas DataFrame construction.
- Unit testing with known-value checks.
- Integration testing with generated market paths.
- Clear output design for reviewers.
- Interview-ready explanation of model assumptions.

### Priority

**Critical / P0.**

Greeks are needed before the Simple Fake Strategy becomes meaningful, because the strategy can use Delta thresholds to generate buy/sell/hold signals.

### Complexity

**Medium to High.**

The formulas are manageable, but the feature requires careful decisions about units, expiry behavior, zero volatility, vectorized shape handling, and stable outputs.

---

## 2. User/Demo Flow

### Happy path

1. User has Feature 1, Feature 2, and Feature 3 working.
2. User runs:

```bash
python -m pyrisklab run --config configs/demo.yaml
```

3. CLI loads and validates the config.
4. Market simulation generates the underlying price path.
5. Black-Scholes pricing calculates option prices.
6. Greeks module receives:
   - simulated underlying prices,
   - option type,
   - strike,
   - risk-free rate,
   - volatility,
   - time to expiry.
7. Greeks module calculates Delta, Gamma, Vega, Theta, and Rho for every market step.
8. App saves:

```text
results/<run_name>/greeks_history.csv
```

9. CLI prints a progress message such as:

```text
[4/12] Calculating option Greeks...
Saved Greeks history: results/demo_run/greeks_history.csv
```

### First-time path

1. User opens `configs/demo.yaml`.
2. User sees the same `option` config used by Feature 3:

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
4. App calculates Greeks without requiring manual Python edits.
5. User opens `greeks_history.csv` and sees sensitivity values row by row.

### Empty state

Greeks depend on valid market-path data and option configuration. If the market path is missing or empty, the app should fail clearly instead of producing an empty file.

Expected behavior:

```text
GreeksError: market path is empty. Run market simulation before calculating Greeks.
```

If required option fields are missing:

```text
ConfigError: option section is required before calculating Greeks.
```

If the option is already expired at every step, that is not an empty state. It is valid, but Greeks should use the explicit expiry behavior described in this spec.

### Error path

Common user/config mistakes should produce clean messages.

Examples:

```text
ConfigError: option.option_type must be 'call' or 'put'. Received 'calls'.
ConfigError: option.strike must be greater than 0. Received 0.
ConfigError: option.volatility must be >= 0. Received -0.1.
GreeksError: market path must include column 'underlying_price'.
GreeksError: underlying_price must be greater than 0. Received 0 at step 14.
GreeksError: Greek calculation produced non-finite values. Check volatility and time_to_expiry.
```

Expected project errors should be caught by the CLI and printed as readable messages without a large stack trace.

### Demo path for a reviewer

1. Reviewer clones the repo.
2. Reviewer installs dependencies.
3. Reviewer runs:

```bash
pytest tests/test_greeks.py
python -m pyrisklab run --config configs/demo.yaml --overwrite
```

4. Reviewer opens:

```text
results/demo_run/greeks_history.csv
```

5. Reviewer verifies columns such as:

```text
step, time_years, underlying_price, time_to_expiry, option_symbol, option_type, strike, risk_free_rate, volatility, delta, gamma, vega, theta, rho
```

6. Reviewer sees that Greeks are deterministic for the same market path and config.
7. Reviewer can inspect `src/pyrisklab/greeks.py` and see focused formulas and tests.

---

## 3. UX/UI Requirements

### Screens/pages

This is a local CLI project, so the main user-facing surfaces are:

1. **CLI progress output**
   - Shows when Greek calculation starts and finishes.
   - Shows where `greeks_history.csv` was saved.

2. **Config file**
   - User edits the same `option` section used by Black-Scholes Pricing.
   - No separate Greeks config should be required for MVP.

3. **Generated Greeks CSV**
   - Main output of Feature 4.
   - Must be easy to inspect in VS Code, Excel, pandas, or GitHub.

4. **Tests**
   - `tests/test_greeks.py` should make the formula behavior visible to a technical reviewer.

Charting is not the responsibility of Feature 4. Greeks charts belong to the Reporting feature.

### Components

Expected code-level components:

- `OptionConfig` or `OptionContract` from existing model/config layer.
- `calculate_greeks(...)` function.
- `calculate_greeks_for_market_path(...)` service-style function.
- Optional helper for `d1` and `d2` calculation.
- `GreeksError` custom exception.
- `greeks_history` pandas DataFrame.

### Forms/inputs

No web forms are needed.

Inputs come from YAML config and market-path data.

Minimum option config fields used by this feature:

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

Required market-path columns:

```text
step
time_years
underlying_price
```

Optional market-path column:

```text
path_id
```

[Open Question] Should Greeks be computed from `market_path.csv`, `pricing_history.csv`, or the in-memory market DataFrame?

Recommended MVP decision: calculate Greeks from the in-memory market DataFrame and the validated option config, then save `greeks_history.csv`. This avoids coupling Greeks to the pricing CSV file format.

### Buttons/actions

No buttons are needed.

Main CLI action:

```bash
python -m pyrisklab run --config configs/demo.yaml
```

Optional future debugging action:

```bash
python -m pyrisklab greeks --config configs/demo.yaml --market-path results/demo_run/market_path.csv
```

Do not add the standalone `greeks` command unless the main run command already works and the extra command improves debugging.

### Validation messages

Required validation messages:

```text
ConfigError: option section is required.
ConfigError: option.option_type must be 'call' or 'put'. Received '<value>'.
ConfigError: option.strike must be greater than 0. Received <value>.
ConfigError: option.volatility must be >= 0. Received <value>.
ConfigError: option.days_to_expiry must be >= 0. Received <value>.
GreeksError: market path must include column 'underlying_price'.
GreeksError: market path is empty. Run market simulation before calculating Greeks.
GreeksError: underlying_price must be greater than 0. Received <value> at step <step>.
```

### Empty states

- Empty market path: fail clearly.
- Missing option config: fail clearly.
- Expired option at start: valid state; return stable expiry Greek values.
- All Vega values are `0`: valid if volatility is zero or option is expired.
- All Gamma values are `0`: valid for expired options or zero-volatility boundary behavior.

### Loading states

CLI progress output is enough.

Example:

```text
[4/12] Calculating option Greeks...
Calculated Greeks for 253 market steps.
Saved Greeks history: results/demo_run/greeks_history.csv
```

### Error states

Expected errors should use custom project exceptions and readable messages.

Examples:

```text
GreeksError: Greek calculation produced non-finite values at step 92.
GreeksError: market path must include column 'time_years'.
```

Do not expose raw NumPy warnings or pandas `KeyError` messages for normal user mistakes.

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

Represents the option being analyzed inside the domain model.

Fields:

- `underlying_symbol`
- `symbol`
- `option_type`
- `strike`
- `risk_free_rate`
- `volatility`
- `initial_days_to_expiry`

Decision:

Reuse the same `OptionContract` model from Feature 3.

Justification:

Greeks and pricing operate on the same option contract. Creating a separate Greek-specific contract object would add unnecessary duplication.

#### 3. `MarketPath`

Input generated by Feature 2.

Minimum columns:

- `step`
- `time_years`
- `underlying_price`
- Optional: `path_id`

#### 4. `GreeksRecord`

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
- `delta`
- `gamma`
- `vega`
- `theta`
- `rho`

### Fields

Required `greeks_history.csv` columns:

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
delta
gamma
vega
theta
rho
```

Optional columns:

```text
path_id
moneyness
d1
d2
```

Decision:

Do not include `d1` and `d2` by default unless they are useful for debugging and tested.

Justification:

`d1` and `d2` are intermediate formula values. They can clutter the user-facing CSV if the main goal is to show Greeks clearly.

### Relationships

- One `RunConfig` contains one `OptionConfig` for MVP.
- One `MarketPath` feeds one `greeks_history` table.
- One `OptionContract` is analyzed across many market steps.
- One row in `market_path.csv` maps to one row in `greeks_history.csv` for the configured option.
- Feature 5, Simple Fake Strategy, may read `greeks_history.csv` or the in-memory Greeks DataFrame to use Delta thresholds.
- Reporting later may combine `pricing_history.csv` and `greeks_history.csv`, but Feature 4 should not own report formatting or charting.

### Example seed data

Recommended `configs/demo.yaml` option section:

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

Example `greeks_history.csv` rows:

```csv
step,time_years,underlying_price,time_to_expiry,option_symbol,option_type,strike,risk_free_rate,volatility,delta,gamma,vega,theta,rho
0,0.000000,100.000000,0.357143,CALL_105,call,105.0,0.04,0.20,0.430000,0.032100,0.236000,-0.018200,0.150000
1,0.003968,100.639743,0.353175,CALL_105,call,105.0,0.04,0.20,0.454000,0.032400,0.238000,-0.018500,0.158000
2,0.007937,100.476546,0.349206,CALL_105,call,105.0,0.04,0.20,0.447000,0.032700,0.237000,-0.018400,0.155000
```

The example numbers are illustrative only. Exact values depend on the implementation, time-to-expiry convention, and unit choices.

### Local persistence needs

Feature 4 should write:

```text
results/<run_name>/greeks_history.csv
```

It should also return the Greeks DataFrame to the pipeline so Feature 5 can use it without rereading from disk.

Decision:

Save CSV and pass the DataFrame forward in memory.

Justification:

CSV gives reviewers a visible artifact. Passing the DataFrame forward keeps the pipeline efficient and simple.

No database is needed.

---

## 5. Logic Requirements

### Business rules

1. Option type must be either `call` or `put`.
2. Strike must be greater than `0`.
3. Underlying prices must be greater than `0`.
4. Volatility must be greater than or equal to `0`.
5. Days to expiry must be greater than or equal to `0`.
6. Time to expiry should never become negative in the Greeks table.
7. For `T > 0` and `sigma > 0`, use standard Black-Scholes Greek formulas.
8. At expiry, return explicit stable boundary values instead of `NaN` or `inf`.
9. At zero volatility, return explicit stable boundary values instead of raising a division-by-zero warning.
10. Greeks output must be deterministic for the same market path and config.
11. Greek calculation should not mutate the input market path DataFrame in surprising ways.
12. This feature should not generate trades or decide whether to buy/sell/hold.

### Calculations

Use these Black-Scholes variables:

- `S`: underlying price.
- `K`: strike price.
- `r`: annualized risk-free rate.
- `sigma`: annualized volatility.
- `T`: time to expiry in years.
- `N(x)`: standard normal cumulative distribution function.
- `phi(x)`: standard normal probability density function.

For `T > 0` and `sigma > 0`:

```text
d1 = [ln(S / K) + (r + 0.5 * sigma^2) * T] / [sigma * sqrt(T)]
d2 = d1 - sigma * sqrt(T)
```

Call Greeks:

```text
delta = N(d1)
gamma = phi(d1) / (S * sigma * sqrt(T))
vega = S * phi(d1) * sqrt(T) / 100
theta = [-(S * phi(d1) * sigma) / (2 * sqrt(T)) - r * K * exp(-rT) * N(d2)] / 365
rho = K * T * exp(-rT) * N(d2) / 100
```

Put Greeks:

```text
delta = N(d1) - 1
gamma = phi(d1) / (S * sigma * sqrt(T))
vega = S * phi(d1) * sqrt(T) / 100
theta = [-(S * phi(d1) * sigma) / (2 * sqrt(T)) + r * K * exp(-rT) * N(-d2)] / 365
rho = -K * T * exp(-rT) * N(-d2) / 100
```

Unit decisions:

- `vega` means price change for a **1 percentage point** volatility change.
- `rho` means price change for a **1 percentage point** interest-rate change.
- `theta` means price change for **one calendar day** passing.

Decision:

Use `vega / 100`, `rho / 100`, and `theta / 365` in the output.

Justification:

These units are easier to understand in a generated CSV and README than raw per-1.00 annualized values.

### Expiry behavior

At `T == 0`, Greeks are mathematically discontinuous or undefined at-the-money. For this project, use stable boundary values:

For a call:

```text
if S > K: delta = 1.0
if S < K: delta = 0.0
if S == K: delta = 0.5
gamma = 0.0
vega = 0.0
theta = 0.0
rho = 0.0
```

For a put:

```text
if S < K: delta = -1.0
if S > K: delta = 0.0
if S == K: delta = -0.5
gamma = 0.0
vega = 0.0
theta = 0.0
rho = 0.0
```

Decision:

Use explicit expiry Greeks instead of returning `NaN`.

Justification:

This makes the generated CSV stable, keeps downstream strategy logic from crashing, and gives tests a clear expected behavior.

### Zero-volatility behavior

At `sigma == 0`, standard Greek formulas divide by zero. For MVP, use deterministic boundary behavior:

- For calls, `delta = 1.0` when `S > K * exp(-rT)`, else `0.0`.
- For puts, `delta = -1.0` when `S < K * exp(-rT)`, else `0.0`.
- `gamma = 0.0`.
- `vega = 0.0`.
- `theta = 0.0`.
- `rho = 0.0`.

Decision:

Use stable finite values at zero volatility instead of trying to over-model a boundary case.

Justification:

The project is a software-engineering portfolio project. Stable, documented edge-case behavior is more valuable than surprising warnings or inconsistent infinities.

### API/service functions if needed

Recommended functions in `src/pyrisklab/greeks.py`:

```python
def calculate_greeks(
    underlying_price: float | np.ndarray,
    strike: float,
    risk_free_rate: float,
    volatility: float,
    time_to_expiry: float | np.ndarray,
    option_type: str,
) -> dict[str, float | np.ndarray]:
    """Return Delta, Gamma, Vega, Theta, and Rho for a European option."""
```

```python
def calculate_greeks_for_market_path(
    market_path: pd.DataFrame,
    option: OptionContract,
    trading_days: int,
) -> pd.DataFrame:
    """Return Greeks history for the configured option over the market path."""
```

Recommended helper functions:

```python
def _d1_d2(...):
    ...
```

```python
def validate_greeks_inputs(...):
    ...
```

[Open Question] Should `_d1_d2(...)` live in `pricing.py`, `greeks.py`, or a shared `option_math.py` file?

Recommended MVP decision: start with a private helper in `greeks.py`. If pricing and Greeks later duplicate too much code, refactor into a small shared helper only after tests are passing.

### State management

Feature 4 should be stateless.

- It receives config/domain objects and market-path data.
- It returns a Greeks DataFrame.
- It does not store global state.
- It does not create orders.
- It does not update portfolio state.
- It does not enforce risk limits.

Decision:

Keep Greeks as pure as practical.

Justification:

Pure numerical logic is easier to unit test, debug, benchmark, and explain in interviews.

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
- Deep in-the-money call.
- Deep out-of-the-money call.
- Deep in-the-money put.
- Deep out-of-the-money put.
- Empty market path.
- Missing `underlying_price` column.
- Missing `time_years` column.
- Non-finite values: `NaN`, `inf`, `-inf`.
- Vectorized array input returns expected shapes.

[Open Question] Should Greek values be clipped to prevent extreme near-expiry Gamma?

Recommended MVP decision: do not clip normal formula outputs for `T > 0`. Only handle `T == 0` explicitly. If near-expiry values become visually extreme, explain that Greeks can become unstable near expiry instead of hiding the behavior.

---

## 6. Acceptance Criteria

### AC1 — Valid call Greeks work

**Given** a valid market path and an option config with `option_type: call`  
**When** the Greeks step runs  
**Then** the app calculates Delta, Gamma, Vega, Theta, and Rho for every market step  
**And** saves `results/<run_name>/greeks_history.csv`.

### AC2 — Valid put Greeks work

**Given** a valid market path and an option config with `option_type: put`  
**When** the Greeks step runs  
**Then** the app calculates put-option Greeks for every market step  
**And** the output file uses `option_type` value `put`.

### AC3 — Output file has required columns

**Given** Greek calculation has completed successfully  
**When** the user opens `greeks_history.csv`  
**Then** it includes `step`, `time_years`, `underlying_price`, `time_to_expiry`, `option_symbol`, `option_type`, `strike`, `risk_free_rate`, `volatility`, `delta`, `gamma`, `vega`, `theta`, and `rho`.

### AC4 — Same inputs produce same Greeks

**Given** the same config and same generated market path  
**When** the Greeks step is run twice  
**Then** `greeks_history.csv` contains the same Greek values.

### AC5 — Delta ranges are reasonable

**Given** normal non-expired option inputs  
**When** Greeks are calculated  
**Then** call Delta is between `0` and `1`  
**And** put Delta is between `-1` and `0`.

### AC6 — Gamma and Vega are non-negative in normal cases

**Given** normal non-expired inputs with positive volatility  
**When** Greeks are calculated  
**Then** Gamma is greater than or equal to `0`  
**And** Vega is greater than or equal to `0`.

### AC7 — Expiry behavior is stable

**Given** `time_to_expiry` is `0`  
**When** Greeks are calculated  
**Then** the returned values are finite  
**And** no division-by-zero warning is produced.

### AC8 — Zero volatility is handled

**Given** `option.volatility` is `0`  
**When** Greeks are calculated for `T > 0`  
**Then** the returned values are finite  
**And** no division-by-zero warning is produced.

### AC9 — Invalid option type fails clearly

**Given** `option.option_type` is `calls`  
**When** the user runs the CLI  
**Then** the run fails with a clear config or Greeks error  
**And** the message says the option type must be `call` or `put`.

### AC10 — Missing market path fails clearly

**Given** no market path data is available  
**When** the Greeks step starts  
**Then** the run fails with `GreeksError`  
**And** the message explains that market simulation must run before calculating Greeks.

### AC11 — Vectorized input works

**Given** an array of underlying prices and an array of times to expiry  
**When** `calculate_greeks(...)` is called  
**Then** it returns arrays with expected shapes for each Greek  
**And** all normal-case values are finite.

---

## 7. Test Plan

### Unit tests

Create:

```text
tests/test_greeks.py
```

Required tests:

1. **Known call Delta test**
   - Use a standard input case.
   - Assert call Delta is approximately expected.

2. **Known put Delta test**
   - Use the same input case.
   - Assert put Delta is approximately expected.

3. **Gamma same for call and put**
   - For the same inputs, call Gamma and put Gamma should match.

4. **Vega same for call and put**
   - For the same inputs, call Vega and put Vega should match.

5. **Call Rho positive in normal case**
   - Assert call Rho is positive for normal positive-rate inputs.

6. **Put Rho negative in normal case**
   - Assert put Rho is negative for normal positive-rate inputs.

7. **Theta finite test**
   - Assert Theta is finite for call and put normal inputs.

8. **Delta range test**
   - Call Delta between `0` and `1`.
   - Put Delta between `-1` and `0`.

9. **Expired call Greeks test**
   - `T = 0` returns finite boundary values.

10. **Expired put Greeks test**
   - `T = 0` returns finite boundary values.

11. **Zero volatility test**
   - `volatility = 0` returns finite values and no crash.

12. **Invalid option type test**
   - `option_type="calls"` raises a clear error.

13. **Invalid strike test**
   - `strike <= 0` raises a clear error.

14. **Invalid underlying price test**
   - `S <= 0` raises a clear error.

15. **Negative volatility test**
   - `volatility < 0` raises a clear error.

16. **Vectorized shape test**
   - Array input returns arrays of expected shape for all five Greeks.

17. **Non-finite input test**
   - `NaN` or `inf` fails clearly.

### Integration tests if useful

Create:

```text
tests/test_pipeline_greeks_integration.py
```

Useful integration tests:

1. Valid demo config creates `greeks_history.csv`.
2. Greeks history row count matches market path row count.
3. Greeks history contains required columns.
4. Invalid option config fails before writing Greeks output.
5. Re-running with `--overwrite` replaces the old Greeks output cleanly.
6. Feature 5 strategy can read Delta from the Greeks DataFrame later.

Keep integration tests lightweight. Do not require fake strategy, execution, portfolio, risk, reporting charts, or benchmark features for Feature 4.

### Manual QA checklist

- [ ] Run `pytest tests/test_greeks.py`.
- [ ] Run the normal demo command.
- [ ] Confirm `results/demo_run/greeks_history.csv` exists.
- [ ] Confirm row count matches `market_path.csv`.
- [ ] Confirm all Greek values are finite for normal config.
- [ ] Confirm call Delta values are mostly between `0` and `1`.
- [ ] Change `option_type` from `call` to `put` and rerun.
- [ ] Confirm put Delta values are mostly between `-1` and `0`.
- [ ] Set invalid `option_type: calls` and confirm clear error.
- [ ] Set `strike: 0` and confirm clear error.
- [ ] Set `volatility: 0` and confirm no crash.
- [ ] Set `days_to_expiry: 0` and confirm finite expiry behavior.

### Demo verification checklist

- [ ] README/demo instructions still show one main command.
- [ ] CLI output includes a Greeks progress step.
- [ ] `greeks_history.csv` is easy to inspect.
- [ ] `src/pyrisklab/greeks.py` is focused and readable.
- [ ] `tests/test_greeks.py` proves core Greek behavior and edge cases.
- [ ] There are no claims about real trading, profitability, or investment advice.

---

## 8. Portfolio Value

### How this feature helps the project stand out

Greeks Calculation gives PyRiskLab stronger technical depth. Many simple finance projects stop at option price. Adding Greeks shows that the project handles sensitivity analysis, not just one formula.

For a software-engineering portfolio, this feature is useful because it creates real implementation and testing challenges:

- vectorized formulas,
- edge cases near expiry,
- zero-volatility behavior,
- stable outputs for downstream features,
- validation and custom errors,
- clear unit decisions.

It also gives a strong bridge into Feature 5, because a simple fake strategy can use Delta thresholds without pretending to predict markets.

### What to mention in README

Mention:

- PyRiskLab calculates Delta, Gamma, Vega, Theta, and Rho.
- Greeks are computed over the deterministic simulated market path.
- Output is saved as `greeks_history.csv`.
- Vega and Rho are shown per 1 percentage point change.
- Theta is shown per day.
- Tests cover normal cases, call/put behavior, expiry, zero volatility, invalid inputs, and vectorized arrays.
- This is a simulation and learning/engineering tool, not investment advice.

Suggested README wording:

```text
The Greeks engine calculates Delta, Gamma, Vega, Theta, and Rho across the simulated market path. Outputs are saved to greeks_history.csv and tested against expected call/put behavior, expiry handling, zero-volatility boundaries, and vectorized input shapes.
```

### What to mention in interviews

Strong interview talking points:

- “I separated Greeks from pricing so the sensitivity engine could be tested independently.”
- “I used vectorized NumPy/SciPy formulas to calculate Greeks over the full path.”
- “I made explicit unit choices for Vega, Theta, and Rho so the CSV is readable.”
- “I handled expiry and zero volatility explicitly instead of letting divide-by-zero warnings leak into the output.”
- “The next strategy feature uses Delta as a deterministic signal input, which creates state changes without pretending the model predicts markets.”
- “The finance formulas are the domain, but the real project signal is modular design, validation, testing, and reproducible outputs.”

---

## 9. Implementation Notes For Codex

### Likely files/folders

Create or update:

```text
src/pyrisklab/greeks.py
src/pyrisklab/models.py
src/pyrisklab/config.py
src/pyrisklab/pipeline.py
src/pyrisklab/exceptions.py
tests/test_greeks.py
tests/test_pipeline_greeks_integration.py
configs/demo.yaml
results/.gitkeep
```

Feature 4 should produce:

```text
results/<run_name>/greeks_history.csv
```

### Build order

1. Confirm Feature 1 CLI, Feature 2 market simulation, and Feature 3 pricing work.
2. Add `GreeksError` in `exceptions.py`.
3. Create `src/pyrisklab/greeks.py`.
4. Implement input validation helpers.
5. Implement `_d1_d2(...)` or reuse a clean helper if one already exists.
6. Implement scalar `calculate_greeks(...)` for normal `T > 0`, `sigma > 0` cases.
7. Add tests for known Delta/Gamma/Vega/Theta/Rho behavior.
8. Add call/put tests.
9. Add expiry handling.
10. Add zero-volatility handling.
11. Add invalid-input tests.
12. Add vectorized input support.
13. Implement `calculate_greeks_for_market_path(...)`.
14. Connect Greek calculation inside `pipeline.py` after pricing.
15. Save `greeks_history.csv` in the run folder.
16. Add integration test for generated Greeks history.
17. Leave charts and README polish for later features.

### Risks

| Risk | Why it matters | Mitigation |
|---|---|---|
| Mixing Greeks back into pricing | Breaks the corrected feature separation | Keep Greeks in `greeks.py` and output `greeks_history.csv`. |
| Unit confusion | Vega/Theta/Rho can be misunderstood | Document units in this spec, code comments, and README later. |
| Near-expiry instability | Gamma and Theta can become extreme near expiry | Handle `T == 0`; do not hide normal near-expiry behavior without documenting it. |
| Zero-volatility divide-by-zero | Can create `NaN` or warnings | Add explicit zero-volatility behavior. |
| Formula bugs pass visually | Greek values are hard to eyeball | Add known-value and property-style tests. |
| Strategy depends on missing Delta | Feature 5 needs Delta reliably | Lock `delta` output column in tests. |
| Duplicate `d1/d2` logic | Pricing and Greeks may drift apart | Refactor to a shared helper only after tests are green if duplication becomes messy. |

### What not to change

- Do not change the main CLI command.
- Do not add live market data.
- Do not add broker APIs.
- Do not add real trading.
- Do not add a web API.
- Do not add Streamlit for this feature.
- Do not add database storage.
- Do not generate strategy signals in this feature.
- Do not execute fake trades in this feature.
- Do not update portfolio state in this feature.
- Do not enforce risk rules in this feature.
- Do not create charts in this feature unless the Reporting feature already owns chart generation.
- Do not run benchmarks in this feature.
- Do not claim Greeks predict future market movement.

### Suggested implementation skeleton

```python
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import norm

from pyrisklab.exceptions import GreeksError
from pyrisklab.models import OptionContract


def calculate_greeks(
    underlying_price,
    strike: float,
    risk_free_rate: float,
    volatility: float,
    time_to_expiry,
    option_type: str,
) -> dict[str, object]:
    """Calculate Delta, Gamma, Vega, Theta, and Rho for call/put options."""
    # Validate option_type, strike, underlying_price, volatility, and T.
    # Convert scalar/array inputs to NumPy arrays.
    # Handle T == 0 explicitly.
    # Handle volatility == 0 explicitly.
    # Compute d1/d2 for normal cases.
    # Return a dict with delta, gamma, vega, theta, rho.
    ...


def calculate_greeks_for_market_path(
    market_path: pd.DataFrame,
    option: OptionContract,
    trading_days: int,
) -> pd.DataFrame:
    """Return Greeks history for the configured option over the market path."""
    # Validate required market columns.
    # Compute time_to_expiry per row.
    # Call calculate_greeks on vectorized arrays.
    # Return greeks_history DataFrame with required columns.
    ...
```

Do not copy this skeleton blindly if the existing project structure uses slightly different names. Preserve the established architecture from Features 1 to 3.

---

## Move-On Checklist

- [ ] `calculate_greeks(...)` supports call and put options.
- [ ] Delta, Gamma, Vega, Theta, and Rho are implemented.
- [ ] Unit choices for Vega, Theta, and Rho are documented.
- [ ] `calculate_greeks_for_market_path(...)` returns a clean DataFrame.
- [ ] `greeks_history.csv` is saved under `results/<run_name>/`.
- [ ] Required Greeks output columns are tested.
- [ ] Call and put Delta tests pass.
- [ ] Gamma and Vega tests pass.
- [ ] Theta and Rho tests pass for normal inputs.
- [ ] Expiry behavior is tested.
- [ ] Zero-volatility behavior is tested.
- [ ] Invalid inputs raise clear errors.
- [ ] Vectorized input behavior is tested.
- [ ] No strategy, execution, portfolio, risk, reporting, benchmark, dashboard, live data, or broker scope is added.
