# Risk Stress Demo

The default demo is designed to show the complete pipeline with normal risk limits. PyRiskLab also includes `configs/risk_stress.yaml` as a small audit-focused preset for reviewers who want to see blocked simulated orders.

Run it locally with:

```bash
python -m pyrisklab run --config configs/risk_stress.yaml --overwrite
```

This preset keeps the synthetic market, option contract, strategy, fake execution model, benchmark, and report flow local and deterministic. It changes the risk limits so proposed orders are rejected before fake execution:

```yaml
risk:
  max_position_quantity: 0
  max_trade_notional: 100.0
```

## Expected Reviewer Signals

- `orders.csv` still records proposed orders.
- Blocked rows in `orders.csv` use `status: BLOCKED`.
- `risk_reason` explains the violated limit in plain English.
- `risk_events.csv` records the audit trail with `ORDER_BLOCKED` events.
- `trades.csv` may have headers and zero rows because blocked orders are not filled.
- `summary_report.md` reports blocked simulated order counts and risk-event counts instead of claiming a profitable strategy.
- `run_metadata.json` records `order_status_counts` for machine-readable audit checks.

## Representative Risk Event Shape

```text
event_type: ORDER_BLOCKED
severity: WARNING
limit_name: max_position_quantity
reason: Blocked BUY 1 CALL_105 at step <generated step>: resulting quantity 1 exceeds max_position_quantity 0.
```

The exact step numbers depend on the generated strategy signals, but the config is seeded so the local run is reproducible. This demo is still simulation only: it does not use live market data, place real trades, connect to a brokerage, or provide investment advice.
