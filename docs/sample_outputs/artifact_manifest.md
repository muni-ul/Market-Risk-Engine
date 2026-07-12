# Generated Artifact Manifest

The main demo writes a complete local results folder under `results/demo_run/`.
This manifest explains why each file exists and what a reviewer should inspect.

| Artifact | Type | Reviewer signal |
| --- | --- | --- |
| `config_used.yaml` | YAML config copy | Reproducibility: the exact run config is preserved next to the outputs. |
| `market_path.csv` | CSV data | Deterministic synthetic market path produced from the configured seed. |
| `pricing_history.csv` | CSV data | Black-Scholes option pricing over the generated path. |
| `greeks_history.csv` | CSV data | Delta, gamma, vega, theta, and rho calculations over the same path. |
| `signals.csv` | CSV data | Simple deterministic fake strategy decisions and readable reasons. |
| `orders.csv` | CSV data | Proposed simulated orders plus risk approval, blocked, or skipped status. |
| `trades.csv` | CSV data | Simulated fills for approved orders, including fill model and notional. |
| `portfolio_history.csv` | CSV data | Cash, position, P&L, total value, peak value, and drawdown tracking. |
| `risk_events.csv` | CSV data | Blocked-order explanations when configured risk limits are breached. |
| `benchmark.csv` | CSV data | Loop-vs-vectorized pricing runtimes, speedup, and equivalence check. |
| `run_metadata.json` | JSON metadata | Config digest, row counts, order status counts, benchmark settings, artifact list, and byte sizes. |
| `market_path.png` | PNG chart | Visual check of the generated underlying path. |
| `option_price.png` | PNG chart | Visual check of option price behavior over the simulation. |
| `greeks.png` | PNG chart | Visual check of option sensitivity calculations. |
| `portfolio_value.png` | PNG chart | Visual check of simulated portfolio value through time. |
| `drawdown.png` | PNG chart | Visual check of peak-to-trough risk behavior. |
| `summary_report.md` | Markdown report | Human-readable run summary, audit counts, benchmark notes, metadata notes, and limitations. |

The stable artifact set is part of the project contract. `run_metadata.json`
records both the expected artifact names and the generated artifact names, while
the summary report lists the generated files for quick review.
