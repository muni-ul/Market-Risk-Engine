# Feature 2 — Market Simulation

## 1. Feature Overview

### Feature name

**Market Simulation**

### One-sentence description

Generate deterministic synthetic stock-price paths using geometric Brownian motion and save the simulated market data as the first real dataset produced by a PyRiskLab run.

### Detailed description

Market Simulation is the first numerical feature after the Config-Driven CLI. The CLI already gives PyRiskLab a professional way to start a run. This feature gives the project its first real output: a synthetic underlying price path that later features can use for Black-Scholes pricing, Greeks calculation, fake strategy decisions, execution, portfolio tracking, risk checks, reporting, tests, and benchmarking.

The market simulator should read the validated `market` section from `configs/demo.yaml`, use the configured random seed, generate one or more synthetic stock-price paths, return the results as a pandas DataFrame, and save the primary path to:

```text
results/<run_name>/market_path.csv
```

The simulator should use geometric Brownian motion because it is a standard, simple, explainable model for producing positive simulated asset prices. The model does not need to be perfect or realistic enough for trading. Its job is to create deterministic, offline-friendly, reviewable market data that makes the rest of the project possible.

This feature should not price options, calculate Greeks, generate trades, update a portfolio, apply risk rules, produce the final report, or benchmark performance. Those are later features. Feature 2 should focus only on clean, validated, reproducible market-path generation.

### Why it matters

Without market simulation, the project has no data pipeline. Using synthetic data keeps PyRiskLab fully local, free to run, deterministic, and safe. It also avoids the scope problems that come from live market APIs, scraping, brokerage integrations, API keys, network failures, rate limits, and financial-data licensing issues.

**Decision:** Use synthetic market paths instead of live market data.

**Justification:** The project is meant to demonstrate Python simulation, automation, testing, reproducibility, and performance-aware design. Live data would add external dependency risk without improving the core software-engineering signal for Version 1.

**Decision:** Use geometric Brownian motion for the Version 1 market model.

**Justification:** GBM is simple enough to implement cleanly, common enough to explain in interviews, and useful enough to generate realistic-looking positive price paths for an options-pricing simulation.

**Decision:** Make the simulator deterministic when the same config and seed are used.

**Justification:** Determinism makes the project easier to test, debug, demo, and review. A recruiter or interviewer should be able to rerun the demo and get the same market path.

**Decision:** Save market data as CSV.

**Justification:** CSV works naturally with pandas, is easy to inspect in VS Code or Excel, and keeps the project local and simple without needing a database.

### Skill it demonstrates

- NumPy numerical computation.
- Random number generation.
- Deterministic seeds.
- Geometric Brownian motion simulation.
- pandas DataFrame creation.
- Data validation.
- Clean function design.
- Separation between simulation logic and CLI orchestration.
- Reproducible data generation.
- Testable numerical code.
- Local artifact generation.

### Priority

**Critical / P0.**

Market Simulation is required before Black-Scholes pricing, Greeks, strategy, execution, portfolio tracking, risk, reporting, and benchmarking can become meaningful.

### Complexity

**Medium.**

The model is not extremely advanced, but the feature must be implemented carefully because it affects every downstream feature. The important difficulty is not the formula alone. The important difficulty is deterministic behavior, validation, data shape, edge-case handling, and clean integration with the run pipeline.

---

## 2. User/Demo Flow

### Happy path

1. User has already built Feature 1: Config-Driven CLI.
2. User opens the repo in VS Code.
3. User verifies `configs/demo.yaml` contains a valid `market` section.
4. User runs:

```bash
python -m pyrisklab run --config configs/demo.yaml --overwrite
```

5. CLI loads and validates the config.
6. Pipeline prepares `results/demo_run/`.
7. Pipeline calls the market simulation service.
8. Market simulator generates a deterministic stock-price path.
9. Market path is returned as a pandas DataFrame.
10. Market path is saved to:

```text
results/demo_run/market_path.csv
```

11. CLI prints a progress message showing the number of generated steps.
12. User opens `market_path.csv` and sees step-by-step simulated prices.

Expected terminal output after this feature:

```text
[1/5] Loading config: configs/demo.yaml
[2/5] Validating config...
[3/5] Preparing output folder: results/demo_run
[4/5] Simulating market path: 252 steps, 1 path, seed=42
[5/5] Saving market_path.csv
Done. Results saved to results/demo_run/
```

### First-time path

1. User follows the README setup from Feature 1.
2. User runs tests:

```bash
pytest
```

3. User runs the demo command:

```bash
python -m pyrisklab run --config configs/demo.yaml
```

4. User sees `results/demo_run/market_path.csv` created.
5. User reruns the same command with `--overwrite`.
6. User confirms the generated prices are identical because the same seed was used.

First-time experience should make the project feel like a reproducible local simulation system, not a random script.

### Empty state

Empty state means the run folder exists, but no market path has been generated yet.

Expected behavior:

- If `results/demo_run/` does not exist, Feature 1 creates it.
- If `market_path.csv` does not exist, Feature 2 creates it.
- Missing `market_path.csv` before simulation is not an error.
- After successful simulation, `market_path.csv` must exist.

For Feature 2, the run folder can contain only:

```text
results/demo_run/
  config_used.yaml
  market_path.csv
```

Later features will add pricing, Greeks, trades, portfolio, risk, benchmark, charts, and reports.

### Error path

Common errors should be caught before or during market simulation and shown clearly.

#### Missing market section

Expected output:

```text
ConfigError: missing required section: market
```

#### Invalid initial price

Config example:

```yaml
market:
  initial_price: 0
```

Expected output:

```text
ConfigError: market.initial_price must be > 0. Received 0.
```

#### Invalid volatility

Config example:

```yaml
market:
  volatility: -0.20
```

Expected output:

```text
ConfigError: market.volatility must be >= 0. Received -0.2.
```

#### Invalid step count

Config example:

```yaml
market:
  steps: 0
```

Expected output:

```text
ConfigError: market.steps must be > 0. Received 0.
```

#### Invalid path count

Config example:

```yaml
market:
  paths: 0
```

Expected output:

```text
ConfigError: market.paths must be >= 1. Received 0.
```

#### Output write failure

Expected output:

```text
RunError: could not write market_path.csv to results/demo_run/. Check folder permissions.
```

### Demo path for a reviewer

Reviewer should run:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pytest
python -m pyrisklab run --config configs/demo.yaml
```

Then inspect:

```text
results/demo_run/market_path.csv
```

Reviewer should be able to quickly understand:

- The market data is simulated.
- The same seed gives the same output.
- The output is saved locally.
- No internet or live market account is required.
- This dataset will feed the later pricing and portfolio features.

---

## 3. UX/UI Requirements

### Screens/pages

This is a local CLI project, so the user-facing surfaces are:

1. **Terminal progress output**
   - Shows that market simulation started and completed.
   - Shows number of steps, number of paths, and seed.

2. **Config file**
   - `configs/demo.yaml` controls the market model.
   - User can change initial price, drift, volatility, trading days, steps, paths, and seed.

3. **Generated CSV output**
   - `results/<run_name>/market_path.csv` is the main output for Feature 2.
   - Later reporting features may generate `market_path.png`, but that is not required for this feature unless implemented early as a small helper.

### Components

#### Market config section

Required config section:

```yaml
market:
  initial_price: 100.0
  drift: 0.05
  volatility: 0.20
  trading_days: 252
  steps: 252
  paths: 1
```

#### CLI progress message

During a successful run:

```text
[4/5] Simulating market path: 252 steps, 1 path, seed=42
```

After save:

```text
Saved market_path.csv with 253 rows.
```

**Decision:** Include the starting price row as step `0`.

**Justification:** The output should show the initial condition before any simulated movement. With `steps: 252`, the CSV should contain `253` rows: step 0 plus 252 simulated steps.

#### Output file

Required output:

```text
results/<run_name>/market_path.csv
```

Optional early output:

```text
results/<run_name>/market_path.png
```

**Decision:** `market_path.csv` is required for Feature 2.

**Justification:** Later features need a structured price path to read from the pipeline.

**Decision:** `market_path.png` should wait until the Reporting feature unless it is trivial.

**Justification:** Feature 2 should stay focused on data generation. Chart styling and report polish belong to Feature 9: Reporting.

### Forms/inputs

There is no web form. Inputs are YAML config fields.

| Input | Type | Required | Example | Validation |
|---|---|---:|---|---|
| `seed` | `int` | Yes | `42` | Must be integer. |
| `market.initial_price` | `float` | Yes | `100.0` | Must be `> 0`. |
| `market.drift` | `float` | Yes | `0.05` | Any real number allowed. |
| `market.volatility` | `float` | Yes | `0.20` | Must be `>= 0`. |
| `market.trading_days` | `int` | Yes | `252` | Must be `> 0`. |
| `market.steps` | `int` | Yes | `252` | Must be `> 0`. |
| `market.paths` | `int` | Yes | `1` | Must be `>= 1`. |

[Open Question] Should `seed` be required globally, or should the simulator allow an optional random seed for non-deterministic experimentation?

Recommended decision: require `seed` for Version 1 because reproducibility matters more than random experimentation.

### Buttons/actions

There are no graphical buttons. Actions are commands.

| Action | Command |
|---|---|
| Run demo simulation | `python -m pyrisklab run --config configs/demo.yaml` |
| Rerun and replace output | `python -m pyrisklab run --config configs/demo.yaml --overwrite` |
| Run market tests | `pytest tests/test_market.py` |
| Inspect output | Open `results/demo_run/market_path.csv` |

### Validation messages

Validation should happen before simulation when possible.

Good messages:

```text
ConfigError: market.initial_price must be > 0. Received -10.0.
```

```text
ConfigError: market.trading_days must be > 0. Received 0.
```

```text
ConfigError: market.paths must be >= 1. Received 0.
```

Bad messages:

```text
ValueError
```

```text
bad market config
```

```text
simulation failed
```

### Empty states

| Empty state | Expected behavior |
|---|---|
| No previous run folder | CLI creates run folder, then market simulation writes CSV. |
| Run folder exists but no market output | Market simulation writes `market_path.csv`. |
| `results/` contains only `.gitkeep` | Not an error. |
| `paths > 1` but no chart exists | Not an error. Charting is Reporting feature. |

### Loading states

The simulator should not silently run. It should show progress through the CLI.

Expected message:

```text
Simulating market path with GBM: initial_price=100.0, drift=0.05, volatility=0.20, steps=252, paths=1
```

For normal demo output, avoid overly verbose logs. The full parameter message can be shown only in debug mode if preferred.

### Error states

Expected market-related errors:

- `ConfigError` for invalid config values.
- `MarketSimulationError` for unexpected simulation-specific problems.
- `RunError` for file-writing or output-folder problems.

**Decision:** Add `MarketSimulationError` in Feature 2.

**Justification:** Market simulation is now its own domain module. Having a specific exception improves debugging and keeps errors readable.

### Responsive behavior if relevant

Not relevant.

This feature has no mobile UI, web page, or dashboard.

---

## 4. Data Requirements

### Entities involved

#### 1. RunConfig

Already created in Feature 1.

Relevant fields:

| Field | Type | Purpose |
|---|---|---|
| `run_name` | `str` | Names the output folder. |
| `seed` | `int` | Controls deterministic random generation. |
| `output_dir` | `str` | Root results folder. |
| `market` | `MarketConfig` | Controls simulation inputs. |

#### 2. MarketConfig

Fields:

| Field | Type | Required | Example | Notes |
|---|---|---:|---|---|
| `initial_price` | `float` | Yes | `100.0` | Starting price at step 0. |
| `drift` | `float` | Yes | `0.05` | Annualized expected return assumption. |
| `volatility` | `float` | Yes | `0.20` | Annualized volatility assumption. |
| `trading_days` | `int` | Yes | `252` | Number of trading days in one year. |
| `steps` | `int` | Yes | `252` | Number of simulation increments. |
| `paths` | `int` | Yes | `1` | Number of simulated paths. |

#### 3. MarketPath

This can be represented as a pandas DataFrame instead of a dataclass.

Required columns for `paths: 1`:

| Column | Type | Example | Purpose |
|---|---|---|---|
| `step` | `int` | `0` | Simulation step index. |
| `time_years` | `float` | `0.0` | Time elapsed in years. |
| `underlying_price` | `float` | `100.0` | Simulated stock price. |

Recommended columns for `paths > 1`:

| Column | Type | Example | Purpose |
|---|---|---|---|
| `step` | `int` | `0` | Simulation step index. |
| `time_years` | `float` | `0.0` | Time elapsed in years. |
| `path_id` | `int` | `0` | Identifies simulated path. |
| `underlying_price` | `float` | `100.0` | Simulated stock price for that path. |

**Decision:** Use long-format data for multiple paths.

**Justification:** Long format is easier to filter, group, save as CSV, and use with pandas than dynamically creating columns like `path_1`, `path_2`, and `path_3`.

### Fields

#### `market_path.csv` for one path

Example:

```csv
step,time_years,underlying_price
0,0.000000,100.000000
1,0.003968,100.639743
2,0.007937,100.476546
3,0.011905,101.311860
```

#### `market_path.csv` for multiple paths

Example:

```csv
step,time_years,path_id,underlying_price
0,0.000000,0,100.000000
1,0.003968,0,100.639743
2,0.007937,0,100.476546
0,0.000000,1,100.000000
1,0.003968,1,99.813221
2,0.007937,1,100.102445
```

[Open Question] Should Version 1 fully support `paths > 1`, or should the config allow it while the main demo uses only `paths: 1`?

Recommended decision: implement `paths >= 1` if it does not complicate the code. Keep the main demo and downstream pipeline focused on `paths: 1` until scenario comparison or later analysis needs multiple paths.

### Relationships

- One `RunConfig` contains one `MarketConfig`.
- One `MarketConfig` produces one market path DataFrame.
- One market path DataFrame is saved as one `market_path.csv` file.
- Feature 3, Black-Scholes Pricing, will read/use `underlying_price` values from this DataFrame.
- Feature 4, Greeks Calculation, will use the same price path and time index.
- Feature 5, Simple Fake Strategy, will use pricing/Greek records derived from this market path.
- Feature 9, Reporting, will later turn this market path into a chart.

### Example seed data

Canonical demo config section:

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
```

Example alternate config for testing zero volatility:

```yaml
run_name: zero_vol_run
seed: 42
output_dir: results

market:
  initial_price: 100.0
  drift: 0.05
  volatility: 0.0
  trading_days: 252
  steps: 252
  paths: 1
```

Example high-volatility config:

```yaml
run_name: high_vol_run
seed: 42
output_dir: results

market:
  initial_price: 100.0
  drift: 0.05
  volatility: 0.50
  trading_days: 252
  steps: 252
  paths: 1
```

### Local persistence needs

Feature 2 should persist:

```text
results/demo_run/
  config_used.yaml
  market_path.csv
```

Do not require:

- Database.
- Cloud storage.
- External market data cache.
- API response files.
- User-uploaded files.

**Decision:** Market simulation output should be written during the main pipeline run, not through a separate command.

**Justification:** The portfolio project should keep the reviewer demo simple: one command should gradually produce all outputs as features are added.

---

## 5. Logic Requirements

### Business rules

1. Market simulation must run after config validation and output-folder preparation.
2. Market simulation must use only config values and a deterministic random seed.
3. Simulation must not call the internet or any live market data API.
4. `initial_price` must be greater than zero.
5. `volatility` must be nonnegative.
6. `trading_days` must be greater than zero.
7. `steps` must be greater than zero.
8. `paths` must be at least one.
9. The returned DataFrame must include step 0.
10. The returned DataFrame must not contain negative prices.
11. The same config and seed must produce identical prices.
12. Different seeds should usually produce different prices when volatility is greater than zero.
13. Zero volatility should produce a deterministic drift-only path.
14. Output should be saved to `market_path.csv` in the current run folder.
15. The simulator should be independent of option pricing and portfolio logic.

### Calculations

Use geometric Brownian motion with annualized drift and volatility.

Recommended discrete form:

```text
S_next = S_current * exp((mu - 0.5 * sigma^2) * dt + sigma * sqrt(dt) * z)
```

Where:

| Symbol | Meaning |
|---|---|
| `S_current` | Current simulated underlying price. |
| `S_next` | Next simulated underlying price. |
| `mu` | Annualized drift from config. |
| `sigma` | Annualized volatility from config. |
| `dt` | Time increment in years. Recommended: `1 / trading_days`. |
| `z` | Standard normal random draw. |

Time index:

```text
time_years = step / trading_days
```

For `steps: 252` and `trading_days: 252`, the simulation covers roughly one trading year.

**Decision:** Use `dt = 1 / trading_days`.

**Justification:** The config already expresses values in trading-day terms. This keeps the relationship between `steps`, `trading_days`, and `time_years` easy to explain.

**Decision:** Generate random shocks with NumPy's modern random generator.

Recommended:

```python
rng = np.random.default_rng(seed)
```

**Justification:** `default_rng` is the preferred modern NumPy random API and avoids hidden global random state.

### API/service functions if needed

#### `market.py`

```python
def simulate_gbm_path(
    *,
    initial_price: float,
    drift: float,
    volatility: float,
    trading_days: int,
    steps: int,
    paths: int,
    seed: int,
) -> pd.DataFrame:
    """Generate one or more deterministic GBM price paths."""
```

Alternative if using dataclasses:

```python
def simulate_market_path(config: RunConfig) -> pd.DataFrame:
    """Generate a market path from a validated RunConfig."""
```

Recommended split:

```python
def simulate_gbm_path(config: MarketConfig, seed: int) -> pd.DataFrame:
    """Generate one or more deterministic GBM price paths."""
```

**Decision:** Pass `MarketConfig` and `seed`, not the entire `RunConfig`, into the core simulator.

**Justification:** The market simulator should not know about option settings, strategy settings, risk settings, benchmark settings, or output folders. This keeps the function focused and easy to test.

#### `pipeline.py`

Add after output folder setup:

```python
market_path = simulate_gbm_path(config.market, seed=config.seed)
save_market_path(market_path, output_path / "market_path.csv")
```

#### `reporting.py` or `market.py`

For Feature 2, CSV saving can live in `pipeline.py` or a small helper. Final reporting polish belongs later.

Possible helper:

```python
def save_market_path_csv(market_path: pd.DataFrame, output_path: Path) -> None:
    """Save simulated market data to CSV."""
```

**Decision:** Use a simple CSV save in Feature 2, then move output-generation polish to Reporting if needed.

**Justification:** The feature should not get blocked by over-designing a reporting layer before the reporting feature exists.

#### `exceptions.py`

Add:

```python
class MarketSimulationError(PyRiskLabError):
    """Raised when market simulation cannot be completed."""
```

### State management

Market simulation should avoid mutable global state.

State flow:

```text
RunConfig
  -> MarketConfig + seed
  -> market.simulate_gbm_path()
  -> market_path DataFrame
  -> pipeline saves market_path.csv
  -> later modules consume market_path DataFrame
```

Do not store market path as a global variable.

Do not mutate `RunConfig` inside `market.py`.

Do not make the simulator depend on current date/time.

**Decision:** Use deterministic numeric step indexes, not real calendar dates, in Version 1.

**Justification:** Calendar dates add complexity around weekends, holidays, and time zones. Step indexes are simpler and enough for a local simulation engine.

[Open Question] Should a later reporting feature add calendar-like dates to charts for readability?

Recommended decision: not in Version 1. Use `step` and `time_years`.

### Edge cases

| Edge case | Expected behavior |
|---|---|
| `initial_price <= 0` | Config validation fails. |
| `volatility < 0` | Config validation fails. |
| `volatility == 0` | Generate drift-only deterministic path. |
| `drift == 0` | Generate random movement from volatility only. |
| `drift < 0` | Allowed; path may trend downward. |
| `steps <= 0` | Config validation fails. |
| `trading_days <= 0` | Config validation fails. |
| `paths < 1` | Config validation fails. |
| Very high volatility | Allowed but output remains positive because GBM uses exponential form. |
| Very large steps | Should work within reasonable memory limits; no need for massive simulation in MVP. |
| Same seed and config | Output must match exactly or within floating tolerance. |
| Different seed and positive volatility | Output should usually differ. |
| CSV write fails | Raise `RunError` with readable message. |
| DataFrame has NaN or infinite values | Raise `MarketSimulationError`. |

[Open Question] Should the simulator warn for unrealistic values like `volatility > 2.0`?

Recommended decision: allow high volatility but document that this is a simulation input, not a real market forecast. Add warnings only if it stays simple.

---

## 6. Acceptance Criteria

### Successful market generation

**Given** `configs/demo.yaml` has a valid market section  
**When** the user runs `python -m pyrisklab run --config configs/demo.yaml`  
**Then** PyRiskLab generates a market path using the configured seed, initial price, drift, volatility, trading days, steps, and paths.

**Given** `configs/demo.yaml` has `market.steps: 252` and `market.paths: 1`  
**When** the market path is generated  
**Then** the DataFrame contains `253` rows including step `0`.

**Given** a market path is generated  
**When** the run completes  
**Then** `results/demo_run/market_path.csv` exists.

**Given** `market_path.csv` exists  
**When** the user opens it  
**Then** it contains `step`, `time_years`, and `underlying_price` columns for the one-path demo.

### Deterministic behavior

**Given** the same config file and same seed  
**When** the user runs the market simulation twice with `--overwrite`  
**Then** the generated `underlying_price` values are identical.

**Given** two configs differ only by seed and volatility is greater than zero  
**When** the market simulation runs for both configs  
**Then** the generated price paths are usually different.

### Validation

**Given** `market.initial_price` is less than or equal to zero  
**When** the user runs the CLI  
**Then** the run fails with a clear `ConfigError`.

**Given** `market.volatility` is negative  
**When** the user runs the CLI  
**Then** the run fails with a clear `ConfigError`.

**Given** `market.steps` is zero or negative  
**When** the user runs the CLI  
**Then** the run fails with a clear `ConfigError`.

**Given** `market.paths` is less than one  
**When** the user runs the CLI  
**Then** the run fails with a clear `ConfigError`.

### Zero volatility

**Given** `market.volatility` is `0.0`  
**When** the simulator runs  
**Then** the path is deterministic and contains no random shock component.

**Given** zero volatility and positive drift  
**When** the simulator runs  
**Then** prices follow the drift-only GBM path and remain positive.

### Scope control

**Given** Feature 2 is implemented  
**When** the market simulation completes  
**Then** it does not price options, calculate Greeks, generate trades, update a portfolio, run risk rules, create a final summary report, benchmark pricing, call live market APIs, or connect to a brokerage.

---

## 7. Test Plan

### Unit tests

#### `tests/test_market.py`

Test cases:

1. Valid config returns a pandas DataFrame.
2. DataFrame includes expected columns for one path.
3. DataFrame row count equals `steps + 1` for `paths: 1`.
4. Step `0` price equals `initial_price`.
5. All generated prices are positive.
6. Same seed and config produce identical DataFrames.
7. Different seeds usually produce different paths when volatility is positive.
8. Zero volatility produces deterministic drift-only path.
9. Negative drift is allowed.
10. Very high volatility still produces positive prices.
11. Multiple paths produce a `path_id` column if supported.
12. Multiple paths produce `(steps + 1) * paths` rows if supported.
13. Invalid `initial_price` raises `ConfigError` or validation failure before simulation.
14. Invalid `volatility` raises `ConfigError` or validation failure before simulation.
15. Invalid `steps` raises `ConfigError` or validation failure before simulation.
16. Invalid `trading_days` raises `ConfigError` or validation failure before simulation.
17. Invalid `paths` raises `ConfigError` or validation failure before simulation.

Recommended deterministic test:

```python
def test_same_seed_produces_same_path():
    path_a = simulate_gbm_path(config, seed=42)
    path_b = simulate_gbm_path(config, seed=42)
    pd.testing.assert_frame_equal(path_a, path_b)
```

Recommended shape test:

```python
def test_single_path_has_steps_plus_initial_row():
    path = simulate_gbm_path(config, seed=42)
    assert len(path) == config.steps + 1
```

Recommended positivity test:

```python
def test_gbm_prices_are_positive():
    path = simulate_gbm_path(config, seed=42)
    assert (path["underlying_price"] > 0).all()
```

### Integration tests if useful

#### Pipeline integration test

1. Create a temporary valid config.
2. Run `pipeline.run_simulation(config_path, overwrite=True)`.
3. Assert output folder exists.
4. Assert `config_used.yaml` exists.
5. Assert `market_path.csv` exists.
6. Read `market_path.csv` with pandas.
7. Assert expected row count and columns.

#### CLI smoke test

Use a temporary config and run:

```bash
python -m pyrisklab run --config <temp_config> --overwrite
```

Expected:

- Return code is `0`.
- Output includes market simulation progress.
- `market_path.csv` is created.

### Manual QA checklist

- [ ] `configs/demo.yaml` contains a valid `market` section.
- [ ] Running the demo creates `results/demo_run/market_path.csv`.
- [ ] `market_path.csv` has clear column names.
- [ ] Row `0` uses the configured initial price.
- [ ] Same seed produces same CSV after rerun.
- [ ] Changing seed changes the path when volatility is positive.
- [ ] Negative volatility fails with a readable message.
- [ ] Zero volatility does not crash.
- [ ] Output prices are positive.
- [ ] No internet/API key/live market data is required.
- [ ] `market.py` does not import pricing, greeks, strategy, execution, portfolio, risk, or reporting modules.

### Demo verification checklist

- [ ] Reviewer can run one command from README.
- [ ] Terminal output shows market simulation happened.
- [ ] Output folder contains `market_path.csv`.
- [ ] CSV can be opened in VS Code or Excel.
- [ ] README can explain that this is synthetic data, not live market data.
- [ ] The market path is ready for Feature 3: Black-Scholes Pricing.

---

## 8. Portfolio Value

### How this feature helps the project stand out

Market Simulation gives PyRiskLab a real data-generation engine instead of relying on hardcoded sample arrays. It shows that the project is not just a formula calculator. It has a reproducible input pipeline that generates structured time-series data and feeds later modules.

This feature helps the repo stand out because it proves:

- You can generate deterministic simulated data.
- You understand why seeds matter.
- You can use NumPy for numerical modeling.
- You can use pandas to structure outputs.
- You can validate inputs before running math.
- You can design modules that feed downstream systems.
- You can keep a project local and reproducible without external services.

### What to mention in README

README should explain:

```text
PyRiskLab starts by generating a synthetic market path using geometric Brownian motion. The path is controlled by configs/demo.yaml and a deterministic random seed, so the same run can be reproduced locally without live market data or API keys.
```

README should show:

```bash
python -m pyrisklab run --config configs/demo.yaml
```

README should list the generated file:

```text
results/demo_run/market_path.csv
```

README should clarify:

- The market path is simulated.
- It is not live market data.
- It is not a forecast.
- It is used to demonstrate a software simulation pipeline.

### What to mention in interviews

Strong interview explanation:

> I used geometric Brownian motion to generate a deterministic synthetic underlying price path. I chose synthetic data because the project is about building a local simulation engine, not relying on live data APIs. The market module uses a validated config and a fixed seed, returns a pandas DataFrame, and writes a CSV artifact that downstream pricing and portfolio modules consume.

Talking points:

- Why synthetic data is better for this local portfolio project.
- Why deterministic seeds make tests and demos reliable.
- Why GBM keeps prices positive.
- Why the market module is separated from pricing and portfolio logic.
- How config values map to output data.
- How edge cases like zero volatility and negative drift are handled.
- Why the project avoids live data, scraping, and brokerage APIs.

---

## 9. Implementation Notes For Codex

### Likely files/folders

Create or update:

```text
pyrisklab/
  configs/
    demo.yaml

  src/
    pyrisklab/
      market.py
      pipeline.py
      config.py
      models.py
      exceptions.py

  tests/
    test_market.py
    test_pipeline.py

  results/
    .gitkeep
```

### File responsibilities

#### `src/pyrisklab/market.py`

Responsibilities:

- Implement GBM simulation.
- Validate simulation output does not contain NaN, infinite, or nonpositive prices.
- Return pandas DataFrame.
- Avoid file I/O unless using a small helper.
- Avoid imports from pricing, greeks, strategy, execution, portfolio, risk, benchmark, or reporting.

Recommended public function:

```python
def simulate_gbm_path(config: MarketConfig, seed: int) -> pd.DataFrame:
    """Generate deterministic geometric Brownian motion price paths."""
```

Possible helper functions:

```python
def _validate_market_output(df: pd.DataFrame) -> None:
    """Validate generated market path before saving."""
```

```python
def save_market_path_csv(df: pd.DataFrame, path: Path) -> None:
    """Save market path to CSV."""
```

#### `src/pyrisklab/pipeline.py`

Update Feature 1 pipeline:

```text
load config
prepare output folder
copy config_used.yaml
simulate market path
save market_path.csv
return RunResult
```

Do not add pricing or Greeks yet.

#### `src/pyrisklab/models.py`

Confirm `MarketConfig` already exists from Feature 1.

If missing, add:

```python
@dataclass(frozen=True)
class MarketConfig:
    initial_price: float
    drift: float
    volatility: float
    trading_days: int
    steps: int
    paths: int
```

#### `src/pyrisklab/config.py`

Feature 1 should already validate market fields. Feature 2 may need to tighten validation if anything was missed.

Required validation:

```text
market.initial_price > 0
market.volatility >= 0
market.trading_days > 0
market.steps > 0
market.paths >= 1
```

#### `src/pyrisklab/exceptions.py`

Add:

```python
class MarketSimulationError(PyRiskLabError):
    """Raised for market simulation failures."""
```

### Build order

1. Confirm Feature 1 CLI still works.
2. Confirm `MarketConfig` exists and is validated.
3. Create `market.py`.
4. Implement `simulate_gbm_path(config, seed)` for `paths: 1`.
5. Add tests for deterministic output, shape, step 0, and positivity.
6. Add zero-volatility behavior.
7. Add optional support for `paths > 1` using long-format DataFrame.
8. Update `pipeline.py` to call market simulation after output folder setup.
9. Save `market_path.csv` to the run folder.
10. Add integration test proving the pipeline creates `market_path.csv`.
11. Run `pytest`.
12. Run `ruff check .` and `ruff format .`.
13. Update README demo output list if README exists already.

### Risks

#### Risk 1: Market simulator becomes mixed with pricing logic

Mitigation:

- Keep `market.py` focused only on underlying price paths.
- Do not import `pricing.py` or `greeks.py`.

#### Risk 2: Randomness makes tests flaky

Mitigation:

- Always use `np.random.default_rng(seed)`.
- Add deterministic seed tests.
- Avoid using NumPy global random state.

#### Risk 3: Multiple paths complicate downstream modules

Mitigation:

- Implement one-path demo as the default.
- If supporting multiple paths, use long format and document that downstream MVP uses `path_id == 0` unless later features expand support.

#### Risk 4: CSV schema changes later

Mitigation:

- Lock required columns early: `step`, `time_years`, `underlying_price`.
- Only add `path_id` when `paths > 1`.

#### Risk 5: Simulation parameters sound like investment assumptions

Mitigation:

- README and report should say these are simulation inputs only.
- Do not claim the path predicts real prices.

### What not to change

Do not add:

- Black-Scholes pricing.
- Greeks calculation.
- Trading strategy.
- Fake execution.
- Portfolio tracking.
- Risk manager logic.
- Final Markdown report.
- Benchmarking.
- Streamlit dashboard.
- Database.
- Live market API.
- Brokerage integration.
- Web backend.
- Login/user accounts.
- Cloud deployment.

Do not change:

- Main command format:

```bash
python -m pyrisklab run --config configs/demo.yaml
```

- Local-first architecture.
- CSV-based output approach.
- Config-driven workflow.
- Deterministic demo behavior.

### Definition of done

Feature 2 is done when:

- [ ] `market.py` contains a focused GBM simulator.
- [ ] Market simulation uses `MarketConfig` and `seed`.
- [ ] Same seed and config produce the same path.
- [ ] `steps: 252` produces `253` rows for one path.
- [ ] Step `0` price equals `market.initial_price`.
- [ ] All generated prices are positive.
- [ ] Zero volatility is handled.
- [ ] Invalid market config fails with clear errors.
- [ ] Pipeline saves `results/demo_run/market_path.csv`.
- [ ] Tests cover shape, determinism, positivity, and edge cases.
- [ ] No live data, database, dashboard, or trading integration is added.
- [ ] The next feature, Black-Scholes Pricing, can consume the market path DataFrame.
