# PyRiskLab Module Reference

This reference summarizes the main `src/pyrisklab/` modules for reviewers who
want to inspect the implementation quickly. PyRiskLab does not expose a public
web API; the primary user interface is the local CLI.

## Entry Points

| Module | Key functions/classes | Responsibility |
| --- | --- | --- |
| `cli.py` | `build_parser`, `main` | Parse CLI flags, show clean project errors, and delegate to the pipeline. |
| `pipeline.py` | `run_simulation` | Orchestrate the complete config-to-results workflow. |
| `__main__.py` | `main` | Support `python -m pyrisklab ...` execution. |

## Core Engine

| Module | Key functions/classes | Responsibility |
| --- | --- | --- |
| `config.py` | `load_config`, `validate_config` | Load YAML and convert raw dictionaries into validated dataclasses. |
| `market.py` | `simulate_gbm_path` | Generate deterministic synthetic market paths from a seed. |
| `pricing.py` | `to_contract`, `intrinsic_value`, `black_scholes_price`, `price_market_path` | Price configured options over the simulated path. |
| `greeks.py` | `calculate_greeks`, `calculate_greeks_for_market_path` | Calculate option sensitivities over scalar or path inputs. |
| `strategy.py` | `generate_signals` | Generate deterministic fake buy, sell, or hold signals. |
| `execution.py` | `create_orders_from_signals`, `execute_orders` | Convert signals into proposed orders and deterministic fake fills. |
| `portfolio.py` | `Portfolio`, `build_portfolio_history` | Track cash, position, P&L, total value, peak value, and drawdown. |
| `risk.py` | `RiskManager`, `risk_events_frame` | Validate simulated orders and record blocked-order reasons. |
| `benchmark.py` | `generate_benchmark_inputs`, `price_loop`, `price_vectorized`, `run_pricing_benchmark` | Compare loop-based and vectorized Black-Scholes pricing. |
| `reporting.py` | `prepare_output_dir`, `save_csv_outputs`, `generate_charts`, `write_run_metadata`, `write_summary_report`, `generate_reports` | Write CSV, PNG, JSON, YAML, and Markdown run artifacts. |

## Data Models And Errors

| Module | Key types | Responsibility |
| --- | --- | --- |
| `models.py` | `RunConfig`, `MarketConfig`, `OptionConfig`, `StrategyConfig`, `ExecutionConfig`, `RiskConfig`, `BenchmarkConfig`, `OptionContract`, `Signal`, `Order`, `Trade`, `Position`, `PortfolioSnapshot`, `RiskEvent`, `BenchmarkResult`, `RunResult` | Typed dataclasses for config, state, audit records, benchmark output, and run results. |
| `exceptions.py` | `PyRiskLabError`, `ConfigError`, `PricingError`, `GreeksError`, `StrategyError`, `ExecutionError`, `MarketSimulationError`, `PortfolioError`, `RiskError`, `ReportingError`, `BenchmarkError`, `RunError` | Domain-specific exceptions for clean user-facing errors. |

The package includes `py.typed` so type-aware tools can treat the distributed
package as typed according to PEP 561.

## Intended Import Style

Most reviewer interaction should happen through the CLI:

```bash
python -m pyrisklab run --config configs/demo.yaml --overwrite
```

For targeted inspection or extension, start with:

- `pyrisklab.config.load_config(...)`
- `pyrisklab.pipeline.run_simulation(...)`
- `pyrisklab.pricing.black_scholes_price(...)`
- `pyrisklab.greeks.calculate_greeks(...)`
- `pyrisklab.benchmark.run_pricing_benchmark(...)`

Functions prefixed with `_` are internal helpers and are not part of the stable
reviewer-facing surface.
