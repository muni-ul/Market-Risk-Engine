# PyRiskLab Validation Notes

PyRiskLab is intentionally defensive. The goal is not only to produce a happy
path demo, but to show that the modules reject invalid configs, non-finite
numeric inputs, unsafe state transitions, and misleading benchmark results with
clear project errors.

## Validation Layers

| Layer | What it protects |
| --- | --- |
| CLI | Catches expected `PyRiskLabError` exceptions and prints concise messages unless `--debug` is used. |
| Config loader | Validates YAML shape, required fields, enum values, booleans, finite numbers, integer fields, output paths, and ranges before simulation starts. |
| Market simulation | Rejects invalid drift, volatility, initial price, steps, paths, and generated non-finite or nonpositive prices. |
| Pricing and Greeks | Reject invalid option types, non-finite inputs, nonpositive underlying prices, invalid strikes, invalid trading-day counts, and bad time-to-expiry values. |
| Strategy | Validates required pricing/Greeks columns, finite numeric inputs, threshold ordering, supported strategy names, and integer trade quantities. |
| Execution | Rejects invalid actions, missing pricing rows, bad fill models, invalid quantities, non-finite prices, invalid multipliers, and bad commissions. |
| Portfolio | Protects cash, multiplier, position quantity, sell quantity, fill price, commission, market price, and drawdown state transitions. |
| Risk manager | Blocks normal simulated orders through configured limits and raises `RiskError` for unsafe validation inputs. |
| Benchmark | Ensures loop and vectorized paths use comparable finite inputs, verifies numerical equivalence, and raises `BenchmarkError` before reporting misleading speedup. |
| Reporting | Validates expected columns and generated artifacts so CSV, PNG, Markdown, JSON, and copied-config outputs remain auditable. |

## Important Failure Paths

Useful examples to inspect in tests:

- Invalid YAML or missing config sections raise `ConfigError`.
- Non-finite numeric config values such as `NaN` or infinity fail before the
  pipeline starts.
- Boolean values are rejected for numeric and integer fields.
- Unsupported option, strategy, and fill-model names fail with field-specific
  messages.
- Non-finite market, pricing, Greeks, strategy, execution, risk, and benchmark
  inputs raise domain-specific project errors.
- Selling more contracts than the current simulated position raises a portfolio
  error instead of silently creating impossible state.
- Blocked simulated orders are recorded as valid risk events, not treated as
  crashes.
- Benchmark output mismatch raises `BenchmarkError` instead of publishing a
  speedup number.
- Existing output folders require `--overwrite` or a different `run_name`.

## Error-Type Contract

All expected project errors inherit from `PyRiskLabError`, which lets the CLI
present clean messages during normal runs. `--debug` keeps the same exception
type but prints traceback details for development.

Domain-specific exceptions make failures easier to locate:

- `ConfigError`
- `MarketSimulationError`
- `PricingError`
- `GreeksError`
- `StrategyError`
- `ExecutionError`
- `PortfolioError`
- `RiskError`
- `ReportingError`
- `BenchmarkError`
- `RunError`

## Interview Framing

The strongest way to discuss this layer is:

> I treated invalid inputs and boundary cases as part of the design, not just as
> test cleanup. Config validation catches bad user input early, domain modules
> protect their own invariants, and the CLI keeps expected project errors
> readable while still offering `--debug` for tracebacks.

This helps position PyRiskLab as a maintainable software system rather than a
single demo script.
