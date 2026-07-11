# Run Metadata Example

Each run writes `run_metadata.json` next to the CSV, PNG, config copy, and summary report artifacts. This JSON file is meant to make a run reproducible and easy to audit.

Representative shape:

```json
{
  "schema_version": 1,
  "project": "PyRiskLab",
  "project_version": "0.1.0",
  "python_version": "3.12.x",
  "platform": "<local OS and architecture>",
  "run_name": "demo_run",
  "seed": 42,
  "config_path": "configs/demo.yaml",
  "config_sha256": "<sha256 digest of the config file>",
  "output_dir": "results/demo_run",
  "execution_enabled": true,
  "benchmark_enabled": true,
  "simulation_only": true,
  "csv_row_counts": {
    "benchmark.csv": 2,
    "greeks_history.csv": 253,
    "market_path.csv": 253,
    "orders.csv": 0,
    "portfolio_history.csv": 253,
    "pricing_history.csv": 253,
    "risk_events.csv": 0,
    "signals.csv": 253,
    "trades.csv": 0
  },
  "expected_artifacts": [
    "benchmark.csv",
    "config_used.yaml",
    "drawdown.png",
    "greeks.png",
    "greeks_history.csv",
    "market_path.csv",
    "market_path.png",
    "option_price.png",
    "orders.csv",
    "portfolio_history.csv",
    "portfolio_value.png",
    "pricing_history.csv",
    "risk_events.csv",
    "run_metadata.json",
    "signals.csv",
    "summary_report.md",
    "trades.csv"
  ],
  "generated_artifacts": [
    "benchmark.csv",
    "config_used.yaml",
    "drawdown.png",
    "greeks.png",
    "greeks_history.csv",
    "market_path.csv",
    "market_path.png",
    "option_price.png",
    "orders.csv",
    "portfolio_history.csv",
    "portfolio_value.png",
    "pricing_history.csv",
    "risk_events.csv",
    "run_metadata.json",
    "signals.csv",
    "summary_report.md",
    "trades.csv"
  ]
}
```

The exact row counts depend on the config. For the default demo, the configured `market.steps: 252` produces `253` path rows because the initial step is included.
