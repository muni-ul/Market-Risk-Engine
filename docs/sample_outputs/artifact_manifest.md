# Generated Artifact Manifest

The main demo writes a complete local results folder under `results/demo_run/`.
This manifest explains why each file exists and what a reviewer should inspect.

## Data And Metadata

- `config_used.yaml`: YAML copy of the exact config used for the run.
- `market_path.csv`: deterministic synthetic market path from the configured
  seed.
- `pricing_history.csv`: Black-Scholes option pricing over the generated path.
- `greeks_history.csv`: Delta, gamma, vega, theta, and rho over the same path.
- `signals.csv`: deterministic fake strategy decisions and readable reasons.
- `orders.csv`: proposed simulated orders plus approved, blocked, or skipped
  status.
- `trades.csv`: simulated fills for approved orders, including fill model and
  notional.
- `portfolio_history.csv`: cash, position, P&L, total value, peak value, and
  drawdown.
- `risk_events.csv`: blocked-order explanations when risk limits are breached.
- `benchmark.csv`: loop-vs-vectorized runtimes, speedup, and equivalence check.
- `run_metadata.json`: config digest, row counts, benchmark settings, artifact
  names, and byte sizes.

## Charts And Report

- `market_path.png`: visual check of the generated underlying path.
- `option_price.png`: visual check of option price behavior over the simulation.
- `greeks.png`: visual check of option sensitivity calculations.
- `portfolio_value.png`: visual check of simulated portfolio value through time.
- `drawdown.png`: visual check of peak-to-trough risk behavior.
- `summary_report.md`: human-readable run summary, audit counts, benchmark
  notes, metadata notes, and limitations.

The stable artifact set is part of the project contract. `run_metadata.json`
records both the expected artifact names and the generated artifact names, while
the summary report lists the generated files for quick review.
