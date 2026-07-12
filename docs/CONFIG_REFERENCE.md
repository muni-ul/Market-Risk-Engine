# PyRiskLab Config Reference

PyRiskLab runs from YAML config files. The default demo uses
`configs/demo.yaml`, and the risk-audit preset uses `configs/risk_stress.yaml`.
Both configs are local, deterministic, and simulation-only.

## Top-Level Fields

| Field | Meaning |
| --- | --- |
| `run_name` | Safe folder name created under `output_dir`. |
| `seed` | Integer seed used for deterministic market simulation and benchmark inputs. |
| `output_dir` | Parent folder for generated run outputs. Defaults to `results` when omitted. |

## `market`

| Field | Meaning |
| --- | --- |
| `initial_price` | Starting synthetic underlying price. Must be positive. |
| `drift` | Annualized drift assumption for the geometric Brownian motion path. |
| `volatility` | Annualized synthetic market volatility. Must be nonnegative. |
| `trading_days` | Trading-day convention used to convert steps into years. |
| `steps` | Number of simulated steps after the initial row. |
| `paths` | Number of generated paths. The main demo uses one path for a focused output contract. |

## `option`

| Field | Meaning |
| --- | --- |
| `underlying_symbol` | Label for the simulated underlying. |
| `symbol` | Label for the configured option contract. |
| `option_type` | `call` or `put`. |
| `strike` | Option strike price. Must be positive. |
| `risk_free_rate` | Black-Scholes risk-free rate assumption. |
| `volatility` | Black-Scholes volatility assumption. Must be nonnegative. |
| `days_to_expiry` | Initial expiry horizon in days. Zero uses intrinsic-value behavior. |

## `strategy`

| Field | Meaning |
| --- | --- |
| `name` | Strategy name. Version 1 supports `simple_delta_rule`. |
| `buy_delta_below` | Generate a simulated buy signal when delta falls below this value. |
| `sell_delta_above` | Generate a simulated sell signal when delta rises above this value. |
| `trade_quantity` | Proposed contract quantity for buy or sell signals. |
| `min_steps_between_trades` | Cooldown between non-hold signals. |

## `execution`

| Field | Meaning |
| --- | --- |
| `enabled` | Whether fake execution should turn approved simulated orders into fills. |
| `fill_model` | Fill model name. Version 1 supports `deterministic_mid`. |
| `commission_per_contract` | Simulated commission applied per contract. Must be nonnegative. |
| `contract_multiplier` | Contract multiplier used for notional and portfolio accounting. |

## `risk`

| Field | Meaning |
| --- | --- |
| `starting_cash` | Initial simulated portfolio cash. Must be positive. |
| `max_position_quantity` | Maximum allowed simulated position size. |
| `max_trade_notional` | Maximum allowed notional for one proposed simulated order. |
| `max_drawdown_pct` | Drawdown threshold for blocking future orders. |
| `max_loss_pct` | Loss threshold for risk validation. |
| `stop_trading_on_breach` | Whether breached loss limits stop future simulated orders. |

## `benchmark`

| Field | Meaning |
| --- | --- |
| `enabled` | Whether to run the loop-vs-vectorized Black-Scholes benchmark. |
| `num_prices` | Number of deterministic benchmark inputs when benchmark is enabled. |
| `seed` | Optional benchmark seed. Defaults to the top-level `seed` when omitted. |
| `tolerance` | Numerical-equivalence tolerance for comparing loop and vectorized prices. |

## Reviewer Presets

- `configs/demo.yaml`: standard end-to-end run with normal risk limits.
- `configs/risk_stress.yaml`: same pipeline, but with tighter position and
  notional limits so blocked simulated orders and risk events are easy to
  inspect in `results/risk_stress_run/`.

For the blocked-order audit walkthrough, see
`docs/sample_outputs/risk_stress_demo.md`. For final validation across both
configs, use `docs/FINAL_REVIEW_CHECKLIST.md`.

Config mistakes are reported as clean `ConfigError` messages instead of normal
stack traces. Use `--debug` only when you want traceback details while developing.
