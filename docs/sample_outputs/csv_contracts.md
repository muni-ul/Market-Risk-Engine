# CSV Output Contracts

The demo run writes CSV files under `results/<run_name>/`. These files are
designed to be easy to inspect in GitHub, VS Code, Excel, pandas, or any plain
text editor.

## Core Pipeline Outputs

- `market_path.csv`: synthetic underlying path.
  Key columns: `step`, `time_years`, `underlying_price`.
- `pricing_history.csv`: Black-Scholes price over the path.
  Key columns: `step`, `time_years`, `underlying_price`, `time_to_expiry`,
  `symbol`, `option_symbol`, `option_type`, `strike`, `risk_free_rate`,
  `volatility`, `option_price`.
- `greeks_history.csv`: option sensitivities over the path.
  Key columns: `step`, `time_years`, `underlying_price`, `time_to_expiry`,
  `symbol`, `option_symbol`, `option_type`, `strike`, `risk_free_rate`,
  `volatility`, `delta`, `gamma`, `vega`, `theta`, `rho`.
- `signals.csv`: deterministic fake strategy decisions.
  Key columns: `step`, `symbol`, `action`, `quantity`, `reference_price`,
  `underlying_price`, `option_price`, `delta`, `gamma`, `vega`,
  `time_to_expiry`, `strategy_name`, `reason`.
- `orders.csv`: proposed orders plus risk status.
  Key columns: `order_id`, `step`, `symbol`, `side`, `quantity`, `order_type`,
  `requested_price`, `source_signal_reason`, `status`, `risk_reason`.
- `trades.csv`: simulated fills for approved orders.
  Key columns: `trade_id`, `order_id`, `step`, `symbol`, `side`, `quantity`,
  `fill_price`, `commission`, `contract_multiplier`, `notional`, `fill_model`.
- `portfolio_history.csv`: cash, position, value, and drawdown over time.
  Key columns: `step`, `cash`, `symbol`, `position_quantity`, `average_cost`,
  `market_price`, `positions_value`, `realized_pnl`, `unrealized_pnl`,
  `total_value`, `peak_value`, `drawdown`, `drawdown_pct`.
- `risk_events.csv`: blocked-order events.
  Key columns: `step`, `event_type`, `severity`, `symbol`, `proposed_side`,
  `proposed_quantity`, `proposed_notional`, `portfolio_value`, `limit_name`,
  `limit_value`, `observed_value`, `reason`.
- `benchmark.csv`: loop-vs-vectorized pricing comparison.
  Key columns: `method`, `num_prices`, `option_type`, `strike`,
  `risk_free_rate`, `volatility`, `runtime_seconds`, `speedup_vs_loop`,
  `max_abs_error_vs_loop`, `passed_equivalence_check`.

`market_path.csv` also includes `path_id` when `market.paths` is greater than
`1`. The main demo config uses one path, so the default output focuses on the
single-path contract.

## Order Audit Statuses

`orders.csv` uses a small status vocabulary so reviewers can scan execution and
risk behavior quickly:

- `APPROVED`: the simulated order passed risk validation and was eligible for
  fake execution.
- `BLOCKED`: the risk manager rejected the simulated order and wrote a reason to
  `risk_reason`.
- `SKIPPED`: fake execution was disabled in config, so proposed orders were not
  filled.

## Valid Empty Outputs

Some files can be empty while still being correct:

- `trades.csv` can have headers and zero rows if no simulated orders are approved.
- `risk_events.csv` can have headers and zero rows if no risk limits are breached.
- `benchmark.csv` can have headers and zero rows when `benchmark.enabled` is false.

These empty states are intentional because they keep the output contract stable
across demo configurations.
