# CSV Output Contracts

The demo run writes CSV files under `results/<run_name>/`. These files are designed to be easy to inspect in GitHub, VS Code, Excel, pandas, or any plain text editor.

## Core Pipeline Outputs

| File | Purpose | Key columns |
| --- | --- | --- |
| `market_path.csv` | Synthetic underlying path | `step`, `time_years`, `underlying_price`, `path_id` |
| `pricing_history.csv` | Black-Scholes price over the path | `step`, `symbol`, `option_type`, `strike`, `underlying_price`, `time_to_expiry`, `option_price` |
| `greeks_history.csv` | Option sensitivities over the path | `step`, `symbol`, `delta`, `gamma`, `vega`, `theta`, `rho` |
| `signals.csv` | Deterministic fake strategy decisions | `step`, `symbol`, `action`, `quantity`, `reason`, `reference_price` |
| `orders.csv` | Proposed orders plus risk status | `order_id`, `step`, `symbol`, `side`, `quantity`, `requested_price`, `status`, `risk_reason` |
| `trades.csv` | Simulated fills for approved orders | `trade_id`, `order_id`, `step`, `symbol`, `side`, `quantity`, `fill_price`, `commission`, `notional` |
| `portfolio_history.csv` | Cash, position, value, and drawdown over time | `step`, `symbol`, `cash`, `position_quantity`, `position_market_value`, `total_value`, `drawdown_pct` |
| `risk_events.csv` | Blocked-order events | `step`, `event_type`, `severity`, `symbol`, `limit_name`, `observed_value`, `reason` |
| `benchmark.csv` | Loop-vs-vectorized pricing comparison | `method`, `num_prices`, `runtime_seconds`, `speedup_vs_loop`, `max_abs_error_vs_loop`, `passed_equivalence_check` |

## Valid Empty Outputs

Some files can be empty while still being correct:

- `trades.csv` can have headers and zero rows if no simulated orders are approved.
- `risk_events.csv` can have headers and zero rows if no risk limits are breached.
- `benchmark.csv` can have headers and zero rows when benchmark execution is disabled.

These empty states are intentional because they keep the output contract stable across demo configurations.
