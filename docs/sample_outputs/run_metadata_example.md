# Run Metadata Example

Each run writes `run_metadata.json` next to the CSV, PNG, config copy, and summary report artifacts. This JSON file is meant to make a run reproducible and easy to audit.

Representative shape:

```json
{
  "schema_version": 3,
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
  "benchmark_settings": {
    "enabled": true,
    "num_prices": 100000,
    "seed": 42,
    "tolerance": 1e-8
  },
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
  "order_status_counts": {
    "APPROVED": 0,
    "BLOCKED": 0,
    "SKIPPED": 0
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
  ],
  "generated_artifact_sizes_bytes": {
    "benchmark.csv": 180,
    "config_used.yaml": 720,
    "drawdown.png": 48123,
    "greeks.png": 71234,
    "greeks_history.csv": 18200,
    "market_path.csv": 9400,
    "market_path.png": 52344,
    "option_price.png": 50122,
    "orders.csv": 96,
    "portfolio_history.csv": 16800,
    "portfolio_value.png": 48890,
    "pricing_history.csv": 15100,
    "risk_events.csv": 132,
    "run_metadata.json": 2400,
    "signals.csv": 14600,
    "summary_report.md": 2200,
    "trades.csv": 88
  }
}
```

The exact row counts depend on the config. For the default demo, the configured `market.steps: 252` produces `253` path rows because the initial step is included.

`schema_version` and `project_version` make the metadata format explicit as the project evolves. Schema version `3` includes generated artifact byte-size auditing and benchmark settings for reproducibility. `config_sha256` lets a reviewer confirm which config produced the run, while `expected_artifacts`, `generated_artifacts`, and `generated_artifact_sizes_bytes` make output completeness auditable without opening every file. Byte sizes vary by machine and matplotlib metadata, so the example values are representative rather than fixed.
