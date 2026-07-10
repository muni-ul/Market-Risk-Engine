# Feature 11: Benchmark

## Output Path

`docs/features/11-benchmark.md`

---

## 1. Feature Overview

### Feature name

**Benchmark**

### One-sentence description

Compare loop-based Black-Scholes pricing against vectorized NumPy pricing and save honest runtime results as a local benchmark artifact.

### Detailed description

The Benchmark feature demonstrates performance awareness in PyRiskLab. It should run a controlled local benchmark that prices many simulated option inputs using two implementations:

1. A simple Python loop implementation.
2. A vectorized NumPy implementation.

The benchmark should measure runtime using `time.perf_counter()`, calculate speedup, verify both methods produce equivalent numerical results within tolerance, and save the result to:

```text
results/<run_name>/benchmark.csv
```

It should also provide a small benchmark summary that can be included in `summary_report.md` and the README.

This feature is not about claiming extreme performance. It is about proving the project measures performance responsibly and explains why vectorization matters.

### Why it matters

For a software engineering portfolio, performance measurement is a strong signal. It shows that PyRiskLab is not only correct and organized, but also performance-aware.

This is especially valuable because the project targets Python simulation, automation, testing, and performance tooling roles. A benchmark gives reviewers a concrete artifact showing that the code compares implementation choices instead of only saying “NumPy is faster.”

### Skill it demonstrates

- Performance measurement
- NumPy vectorization
- Fair baseline comparison
- Runtime timing with `time.perf_counter()`
- Numerical equivalence checks
- pandas benchmark output
- Reproducible local experiments
- Honest communication of performance results

### Priority

**High**

Benchmarking is one of the key features that makes the project more impressive than a basic finance calculator.

### Complexity

**Medium**

The benchmark is conceptually simple, but it must be implemented carefully so it is fair, deterministic, and not misleading.

---

## 2. User/Demo Flow

### Happy path

1. User runs:

```bash
python -m pyrisklab run --config configs/demo.yaml
```

2. Config loader reads benchmark settings.
3. Benchmark module generates deterministic benchmark inputs.
4. Loop-based pricing runs on the same inputs.
5. Vectorized pricing runs on the same inputs.
6. Benchmark verifies both outputs are numerically close.
7. Runtime results are saved to:

```text
results/demo_run/benchmark.csv
```

8. Reporting includes a short benchmark summary.

### First-time path

The demo config should include benchmark settings:

```yaml
benchmark:
  enabled: true
  num_prices: 100000
  seed: 42
```

The first-time user should not need to understand benchmarking details. They should simply run the normal demo command and get the benchmark output automatically.

### Empty state

If benchmarking is disabled:

```yaml
benchmark:
  enabled: false
```

Then the pipeline should skip the benchmark cleanly.

Recommended behavior:

- Do not create misleading runtime rows.
- Summary report says:

```text
Benchmark was disabled in the config.
```

[Decision] For the main portfolio demo, keep benchmarking enabled because it is a strong project signal.

### Error path

Invalid benchmark config should fail early with a clear message:

```text
ConfigError: benchmark.num_prices must be greater than 0. Received 0.
ConfigError: benchmark.seed must be an integer. Received 'abc'.
```

If benchmark outputs disagree numerically:

```text
BenchmarkError: loop and vectorized pricing results differed beyond tolerance.
```

If timing fails unexpectedly, raise:

```text
BenchmarkError: pricing benchmark could not be completed.
```

### Demo path for a reviewer

Reviewer runs:

```bash
pytest tests/test_benchmark.py
python -m pyrisklab run --config configs/demo.yaml --overwrite
```

Reviewer opens:

```text
results/demo_run/benchmark.csv
```

They should see runtime rows for loop pricing and vectorized pricing, plus a readable speedup value.

---

## 3. UX/UI Requirements

### Screens/pages

No traditional UI screen is needed.

User-facing surfaces:

1. CLI progress message
2. `benchmark.csv`
3. Benchmark section in `summary_report.md`
4. README benchmark explanation later

### Components

#### CLI progress message

Recommended message:

```text
[11/12] Running loop-vs-vectorized pricing benchmark...
```

If disabled:

```text
[11/12] Benchmark disabled by config. Skipping...
```

#### Benchmark CSV

Required output when enabled:

```text
results/<run_name>/benchmark.csv
```

Recommended columns:

| Column | Description |
|---|---|
| `method` | `loop` or `vectorized` |
| `num_prices` | Number of option prices computed |
| `runtime_seconds` | Measured runtime |
| `speedup_vs_loop` | Speedup compared with loop baseline |
| `max_abs_error_vs_loop` | Maximum absolute pricing difference from loop baseline |
| `passed_equivalence_check` | Whether outputs matched within tolerance |

Example:

```csv
method,num_prices,runtime_seconds,speedup_vs_loop,max_abs_error_vs_loop,passed_equivalence_check
loop,100000,1.2400,1.00,0.0,true
vectorized,100000,0.0350,35.43,0.00000001,true
```

### Forms/inputs

No direct form is needed.

Inputs come from config:

```yaml
benchmark:
  enabled: true
  num_prices: 100000
  seed: 42
```

Optional future inputs:

```yaml
benchmark:
  repeats: 3
  tolerance: 1.0e-8
```

[Decision] Keep MVP benchmark simple with one measured run. Add repeats only if needed later.

### Buttons/actions

No buttons are needed.

Main command:

```bash
python -m pyrisklab run --config configs/demo.yaml
```

Optional later command:

```bash
python -m pyrisklab benchmark --config configs/demo.yaml
```

[Decision] Do not add a separate benchmark command for MVP unless the main pipeline becomes too slow.

### Validation messages

Recommended validation messages:

```text
ConfigError: benchmark.num_prices must be greater than 0. Received -100.
ConfigError: benchmark.enabled must be true or false. Received 'yes'.
BenchmarkError: benchmark input arrays must all have the same length.
BenchmarkError: loop and vectorized results failed equivalence check.
```

### Empty states

If benchmark is disabled, the report should not pretend a benchmark ran.

Recommended summary:

```text
Benchmark skipped because benchmark.enabled is false.
```

### Loading states

CLI progress is enough.

Benchmark should run quickly enough that no complex loading state is needed.

### Error states

Expected benchmark failures should use a custom exception:

```python
BenchmarkError
```

CLI should display clean errors.

### Responsive behavior if relevant

Not relevant for MVP.

---

## 4. Data Requirements

### Entities involved

Input entities/data:

- `BenchmarkConfig`
- Deterministic benchmark input arrays
- Black-Scholes pricing functions

Output entities:

- `BenchmarkResult`
- `benchmark.csv`

### Fields

#### BenchmarkConfig

Recommended fields:

```python
BenchmarkConfig:
  enabled: bool
  num_prices: int
  seed: int
  tolerance: float = 1e-8
```

Optional later:

```python
repeats: int
```

#### BenchmarkResult

Recommended fields:

```python
BenchmarkResult:
  method: str
  num_prices: int
  runtime_seconds: float
  speedup_vs_loop: float
  max_abs_error_vs_loop: float
  passed_equivalence_check: bool
```

### Relationships

- One run may have one benchmark.
- One benchmark creates deterministic input arrays.
- The loop method and vectorized method use the same inputs.
- Benchmark results are saved to `benchmark.csv`.
- Reporting summarizes benchmark results.

### Example seed data

Recommended config:

```yaml
benchmark:
  enabled: true
  num_prices: 100000
  seed: 42
  tolerance: 1.0e-8
```

Recommended deterministic benchmark inputs:

- Underlying prices: random uniform values, for example 50 to 150
- Strike: fixed, for example 105
- Risk-free rate: fixed, for example 0.04
- Volatility: fixed, for example 0.20
- Time to expiry: fixed or generated in a sensible range

[Decision] Use deterministic generated inputs instead of real market data.

### Local persistence needs

Required file when enabled:

```text
results/<run_name>/benchmark.csv
```

Optional later:

```text
results/<run_name>/benchmark_summary.md
```

[Decision] Do not use a database or profiling server.

---

## 5. Logic Requirements

### Business rules

#### Rule 1: Same inputs for both methods

The loop and vectorized functions must use identical generated input arrays.

#### Rule 2: Deterministic inputs

The benchmark should use a fixed seed from config so repeated runs are comparable.

#### Rule 3: Numerical equivalence check

After both methods run, compare outputs:

```text
max_abs_error = max(abs(loop_prices - vectorized_prices))
```

Pass if:

```text
max_abs_error <= tolerance
```

If equivalence fails, raise `BenchmarkError`.

#### Rule 4: Honest speedup calculation

Calculate speedup:

```text
speedup_vs_loop = loop_runtime / method_runtime
```

For the loop row, speedup is `1.0`.

If runtime is zero or extremely tiny, avoid division errors.

Recommended safe behavior:

```text
if method_runtime <= 0:
    speedup_vs_loop = None
```

or use a tiny epsilon with clear handling.

#### Rule 5: Benchmark should not dominate runtime

The default benchmark should be large enough to show a real difference but small enough to run on a normal laptop.

Recommended default:

```yaml
num_prices: 100000
```

[Open Question] If this is too slow on the user's laptop, reduce to `50000`.

### Calculations

Required calculations:

- Loop runtime
- Vectorized runtime
- Speedup versus loop
- Max absolute error
- Equivalence pass/fail

### API/service functions if needed

Recommended functions in `benchmark.py`:

```python
def generate_benchmark_inputs(num_prices: int, seed: int) -> dict[str, np.ndarray]:
    ...
```

```python
def price_loop(inputs: dict[str, np.ndarray]) -> np.ndarray:
    ...
```

```python
def price_vectorized(inputs: dict[str, np.ndarray]) -> np.ndarray:
    ...
```

```python
def run_pricing_benchmark(config: BenchmarkConfig) -> pd.DataFrame:
    ...
```

Recommended helper:

```python
def time_function(fn: Callable[[], np.ndarray]) -> tuple[np.ndarray, float]:
    start = time.perf_counter()
    result = fn()
    elapsed = time.perf_counter() - start
    return result, elapsed
```

### State management

Benchmark should be stateless.

It should receive config, generate deterministic inputs, run both methods, return a DataFrame, and let Reporting save it.

Do not store hidden global benchmark state.

### Edge cases

#### `num_prices` is small

If `num_prices = 1`, benchmark should still work, but speedup may not be meaningful.

#### `num_prices` is very large

Large values can make the project slow. Config validation may set a practical upper warning.

[Decision] Do not fail on large values unless memory becomes a real issue. Keep demo config reasonable.

#### Outputs mismatch

Raise `BenchmarkError` because performance numbers are meaningless if methods do not match.

#### Runtime near zero

Handle speedup safely.

#### Benchmark disabled

Skip cleanly and do not create fake benchmark data.

#### Non-finite prices

If either method returns NaN or infinity for normal benchmark inputs, raise `BenchmarkError`.

---

## 6. Acceptance Criteria

### AC1: Benchmark runs when enabled

Given `benchmark.enabled` is true  
When the user runs the demo command  
Then the benchmark runs  
And `benchmark.csv` is created.

### AC2: Benchmark skips when disabled

Given `benchmark.enabled` is false  
When the user runs the demo command  
Then benchmarking is skipped cleanly  
And the report says benchmark was disabled.

### AC3: Loop and vectorized methods use the same inputs

Given benchmark inputs are generated  
When loop and vectorized pricing run  
Then both methods receive identical underlying prices, strike, volatility, rate, and time-to-expiry values.

### AC4: Numerical equivalence is verified

Given loop and vectorized pricing outputs  
When benchmark compares the outputs  
Then the max absolute error is calculated  
And the benchmark passes only if the error is within tolerance.

### AC5: Speedup is calculated

Given loop runtime and vectorized runtime are measured  
When benchmark results are created  
Then vectorized speedup is calculated relative to the loop runtime.

### AC6: Benchmark CSV has required columns

Given a successful benchmark run  
When `benchmark.csv` is saved  
Then it includes `method`, `num_prices`, `runtime_seconds`, `speedup_vs_loop`, `max_abs_error_vs_loop`, and `passed_equivalence_check`.

### AC7: Invalid benchmark config fails early

Given `benchmark.num_prices` is less than or equal to zero  
When config is loaded  
Then the system raises a clear `ConfigError`.

### AC8: Mismatched outputs fail benchmark

Given loop and vectorized outputs differ beyond tolerance  
When benchmark validation runs  
Then a `BenchmarkError` is raised.

---

## 7. Test Plan

### Unit tests

Create:

```text
tests/test_benchmark.py
```

Recommended tests:

1. `test_generate_benchmark_inputs_is_deterministic`
2. `test_generate_benchmark_inputs_has_expected_length`
3. `test_loop_and_vectorized_prices_match_within_tolerance`
4. `test_run_pricing_benchmark_returns_dataframe`
5. `test_benchmark_dataframe_has_required_columns`
6. `test_speedup_vs_loop_is_calculated`
7. `test_invalid_num_prices_fails_config_validation`
8. `test_benchmark_disabled_skips_cleanly`
9. `test_output_mismatch_raises_benchmark_error`
10. `test_nonfinite_benchmark_output_raises_error`

### Integration tests if useful

Create:

```text
tests/test_pipeline_benchmark_integration.py
```

Recommended integration test:

- Run a tiny config with benchmark enabled and `num_prices: 1000`.
- Confirm `benchmark.csv` is created.
- Confirm both loop and vectorized rows exist.
- Confirm equivalence check passed.

### Manual QA checklist

- [ ] Run `pytest tests/test_benchmark.py`.
- [ ] Run `python -m pyrisklab run --config configs/demo.yaml --overwrite`.
- [ ] Confirm `results/demo_run/benchmark.csv` exists.
- [ ] Confirm loop and vectorized rows exist.
- [ ] Confirm vectorized method is faster for a large enough `num_prices`.
- [ ] Confirm speedup is not exaggerated in README/report.
- [ ] Disable benchmark in config and confirm clean skip.
- [ ] Set invalid `num_prices` and confirm clear error.

### Demo verification checklist

- [ ] Reviewer can open `benchmark.csv`.
- [ ] Reviewer can understand what was compared.
- [ ] README later explains benchmark limitations.
- [ ] Benchmark does not claim universal speedup across all machines.
- [ ] Benchmark does not require Numba, C++, GPU, cloud, or special hardware.

---

## 8. Portfolio Value

### How this feature helps the project stand out

The Benchmark feature gives PyRiskLab a stronger software engineering signal. It shows the project is not only about finance formulas; it is about measuring implementation tradeoffs.

This stands out because many portfolio projects say they use NumPy, but fewer prove why vectorization matters with a reproducible benchmark artifact.

It demonstrates:

- Performance awareness
- Experimental thinking
- Reproducible measurement
- Honest engineering communication
- Understanding of Python loops versus NumPy vectorization

### What to mention in README

Mention:

```text
PyRiskLab includes a local benchmark comparing loop-based Black-Scholes pricing with vectorized NumPy pricing on the same generated inputs. The benchmark saves runtime, speedup, and numerical-equivalence checks to benchmark.csv.
```

Also mention:

```text
Benchmark results vary by machine and are intended to demonstrate performance-aware design, not guarantee fixed speedups.
```

### What to mention in interviews

Strong interview points:

- “I benchmarked loop-based pricing against vectorized NumPy pricing using the same inputs.”
- “I verified numerical equivalence before reporting speedup.”
- “I used deterministic inputs so the benchmark is reproducible.”
- “I kept the benchmark simple and honest instead of adding premature Numba or C++ acceleration.”
- “This feature helped me discuss performance tradeoffs in Python.”

---

## 9. Implementation Notes For Codex

### Likely files/folders

Primary files:

```text
src/pyrisklab/benchmark.py
tests/test_benchmark.py
```

Related files:

```text
src/pyrisklab/pricing.py
src/pyrisklab/config.py
src/pyrisklab/models.py
src/pyrisklab/exceptions.py
src/pyrisklab/pipeline.py
src/pyrisklab/reporting.py
configs/demo.yaml
```

Generated output:

```text
results/<run_name>/benchmark.csv
```

### Suggested exception

In `exceptions.py`:

```python
class BenchmarkError(PyRiskLabError):
    """Raised when benchmark execution or validation fails."""
```

### Suggested config model

In `models.py` or config models:

```python
@dataclass(frozen=True)
class BenchmarkConfig:
    enabled: bool
    num_prices: int
    seed: int
    tolerance: float = 1e-8
```

### Build order

1. Add `BenchmarkError`.
2. Add `BenchmarkConfig` validation.
3. Implement deterministic input generation.
4. Implement loop pricing wrapper.
5. Implement vectorized pricing wrapper.
6. Implement timing helper with `time.perf_counter()`.
7. Implement numerical equivalence check.
8. Implement speedup calculation.
9. Return benchmark results as DataFrame.
10. Save `benchmark.csv` through Reporting.
11. Add tests.
12. Add benchmark summary to `summary_report.md`.

### Risks

#### Risk 1: Misleading benchmark claims

Do not claim speedup is universal. Results depend on machine, Python version, and input size.

#### Risk 2: Benchmark compares different logic

The loop and vectorized methods must use the same Black-Scholes formula and same inputs.

#### Risk 3: Benchmark skips correctness check

Do not report speedup unless outputs match within tolerance.

#### Risk 4: Benchmark makes demo too slow

Keep default `num_prices` reasonable.

#### Risk 5: Overbuilding acceleration

Do not add Numba, C++, GPU, multiprocessing, or profiling tools in MVP.

### What not to change

Do not change:

- CLI command format
- Black-Scholes formula behavior
- Market simulation logic
- Greeks calculation logic
- Strategy rules
- Fake execution behavior
- Portfolio accounting
- Risk rules
- Reporting structure beyond adding `benchmark.csv` and summary text

This feature should only add a benchmark layer.

---

## Move-On Checklist

- [ ] Benchmark config validates correctly.
- [ ] Benchmark can be enabled or disabled.
- [ ] Deterministic benchmark inputs are generated.
- [ ] Loop and vectorized methods use the same inputs.
- [ ] Numerical equivalence is checked.
- [ ] Runtime and speedup are calculated safely.
- [ ] `benchmark.csv` is saved.
- [ ] Tests cover benchmark behavior and edge cases.
- [ ] Report/README wording avoids exaggerated performance claims.
- [ ] Feature does not add Numba, C++, GPU, cloud, live data, broker APIs, dashboard, SaaS scope, or real trading.
