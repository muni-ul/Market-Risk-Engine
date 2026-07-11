# PyRiskLab Sample Output

This page shows what a successful local demo run is designed to produce. The actual numbers may differ by machine for benchmark timing, but the artifact names and report shape should match.

## Terminal Output

```text
[1/7] Loading config...
[2/7] Simulating market path...
[3/7] Pricing option and calculating Greeks...
[4/7] Running strategy, risk checks, and fake execution...
[5/7] Tracking portfolio value and drawdown...
[6/7] Running benchmark...
[7/7] Saving reports...
Done. Results saved to results/demo_run/
```

## Results Folder

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

`orders.csv` includes `status` and `risk_reason` audit columns. Status values are `APPROVED`, `BLOCKED`, or `SKIPPED`, and the same counts are summarized in `summary_report.md` and `run_metadata.json`.

## Example Summary Report Excerpt

```markdown
# PyRiskLab Run Summary

Run name: `demo_run`
Seed: `42`

## Simulation Only

This is a local simulation only. It does not use live market data, place real trades, connect to a brokerage, provide investment advice, or make profitability claims.

## Market Simulation

- Model: geometric Brownian motion with synthetic data
- Drift assumption: 5.00%
- Volatility assumption: 20.00%
- Trading days per year: 252

## Greeks

- Final delta: generated from the final simulated option state
- Final gamma: generated from the final simulated option state
- Final vega: generated from the final simulated option state
- Final theta: generated from the final simulated option state
- Final rho: generated from the final simulated option state

## Fake Execution

- Enabled: generated from the execution config
- Fill model: deterministic simulated fill model
- Commission per contract: configured local assumption
- Contract multiplier: configured local assumption
- Result: generated from fake execution state

## Benchmark

Vectorized NumPy pricing ran faster than the Python loop on this machine.

- Prices compared: generated from the benchmark config
- Python loop runtime: measured locally
- NumPy vectorized runtime: measured locally
- Max absolute error vs loop: generated from the equivalence check
- Numerical equivalence check: passed

Benchmark results vary by hardware, Python version, and input size.
```

## Why This Matters

The generated output is meant to make the project easy to evaluate quickly: one command creates CSV tables, PNG charts, the copied config, deterministic run metadata, benchmark results, risk/trade logs, and a Markdown report. The metadata records the config path, config SHA-256 digest, row counts, order status counts, expected artifact set, generated artifact set, and generated artifact byte sizes; the summary report also enumerates the generated artifacts. The report is intentionally local and file-based so it can be inspected without a dashboard, database, account, or cloud deployment.
