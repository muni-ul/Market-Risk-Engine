# PyRiskLab Portfolio Case Study

## Problem

I wanted to build a local Python project that looked like an engineering tool instead of a notebook or one-off script. Options pricing gave the project a useful simulation domain, but the real goal was to demonstrate package structure, deterministic execution, numerical computation, tests, risk validation, benchmarking, and reproducible outputs.

PyRiskLab is intentionally not a trading bot. It does not use live market data, connect to brokerages, place real trades, or provide investment advice.

## Approach

The project is built around one local command:

```bash
python -m pyrisklab run --config configs/demo.yaml --overwrite
```

That command loads a YAML config, generates a synthetic market path, prices a European option with Black-Scholes, calculates Greeks, creates simple fake strategy signals, validates proposed orders against risk rules, executes approved simulated trades, tracks portfolio value, runs a loop-vs-vectorized benchmark, and exports CSV, PNG, JSON, and Markdown artifacts.

## Engineering Decisions

- Kept the project local-first so reviewers can run it without accounts, API keys, Docker, databases, or cloud services.
- Used `argparse` and a thin CLI so orchestration stays in `pipeline.py`.
- Used dataclasses for typed config and domain objects instead of passing raw dictionaries through the whole system.
- Used deterministic seeds and copied `config_used.yaml` into every run folder to make outputs reproducible.
- Recorded order status counts, expected and generated artifact names, and artifact byte sizes in run metadata so reviewers can audit execution behavior and output completeness.
- Kept strategy logic intentionally simple because its purpose is to drive execution, portfolio, and risk behavior, not to claim profitability.
- Stored outputs as CSV, PNG, JSON, and Markdown because those formats are easy to inspect in GitHub, VS Code, Excel, and pandas.
- Added `configs/risk_stress.yaml` as an optional reviewer demo for blocked orders and readable risk events.

## System Flow

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

## Testing And Correctness

The test suite is designed around behavior that would matter in a real engineering tool:

- Config validation catches bad inputs with field-specific messages.
- Market simulation is deterministic for the same seed and rejects non-finite assumptions defensively.
- Pricing tests cover known call/put values, parity, expiry, finite parameters, and vectorized inputs.
- Greeks tests cover finite outputs, finite parameters, and call/put delta behavior.
- Strategy tests cover threshold decisions, non-finite Delta handling, and invalid pricing context.
- Execution tests cover deterministic fills, notional calculation, and invalid order quantities.
- Portfolio tests cover cash, positions, realized P&L, and drawdown.
- Risk tests cover allowed trades, blocked trades, available cash, defensive order validation, and readable event reasons.
- Reporting tests cover empty output states and metadata artifacts.

## Performance Signal

PyRiskLab includes a small benchmark that compares Python-loop Black-Scholes pricing with vectorized NumPy pricing on the same generated inputs. It reports runtime, speedup, and numerical-equivalence checks in `benchmark.csv`. The benchmark is intentionally honest: numbers vary by machine, and the README does not claim a fixed universal speedup.

## Result

The finished demo produces a reviewer-friendly results folder:

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

For a committed preview of the report and CSV shapes, see `docs/sample_outputs/`.

The strongest interview story is that PyRiskLab uses finance as the domain, but the project is really about building a reliable Python simulation pipeline with clean modules, deterministic configs, testable state transitions, risk guardrails, benchmark evidence, and inspectable local reports.

## What I Would Improve Next

- Add a curated `docs/assets/` screenshot set after final demo outputs are generated.
- Add multiple option contracts while preserving the single-contract MVP path.
- Add optional Numba benchmarking only after the baseline NumPy benchmark remains well documented.
- Add richer report styling while keeping the project local and dependency-light.
