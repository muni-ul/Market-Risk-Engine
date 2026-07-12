# PyRiskLab Testing Strategy

PyRiskLab uses pytest to validate the behavior that matters most for a local
simulation engine: deterministic inputs, numerical correctness, state
transitions, risk decisions, output contracts, and repo hygiene.

## What The Suite Covers

| Area | Test files | Main signal |
| --- | --- | --- |
| CLI and config | `test_cli.py`, `test_config.py` | Commands, clean errors, YAML validation, and supported flags. |
| Market simulation | `test_market.py` | Deterministic seeds, positive prices, shape, and edge cases. |
| Pricing and Greeks | `test_pricing.py`, `test_greeks.py` | Known Black-Scholes values, put/call behavior, vectorized inputs, and invalid inputs. |
| Strategy and execution | `test_strategy.py`, `test_execution.py` | Deterministic signals, fake order creation, fill records, and input validation. |
| Portfolio and risk | `test_portfolio.py`, `test_risk.py` | Cash, positions, P&L, drawdown, blocked orders, and readable risk events. |
| Benchmarking | `test_benchmark.py` | Loop-vs-vectorized input validation, equivalence checks, and stable CSV columns. |
| Reporting and pipeline | `test_reporting.py`, `test_pipeline_smoke.py` | CSV/PNG/Markdown/metadata artifacts, empty-output states, and end-to-end wiring. |
| Repo contracts | `test_packaging_metadata.py`, `test_readme_contract.py`, `test_repo_hygiene.py`, `test_exceptions.py` | Packaging metadata, documentation links, ignored artifacts, typed package marker, and exception hierarchy. |

## Reviewer Commands

```bash
pytest
pytest tests/test_pricing.py
pytest tests/test_portfolio.py
pytest tests/test_risk.py
```

Use the full suite for the final local verification pass. Use targeted files
when discussing one subsystem in an interview.

## Design Choices

- Tests use deterministic seeds and local files, not live market data or network
  calls.
- Reporting tests use temporary directories so they do not pollute
  `results/demo_run/`.
- Floating-point tests use approximate comparisons where exact equality would
  be brittle.
- Documentation and repo-hygiene tests intentionally protect the GitHub
  reviewer experience, not just runtime behavior.

## What Is Intentionally Not Included

- No live-market, brokerage, account, cloud, database, or dashboard tests.
- No profitability or trading-performance assertions.
- No coverage-percentage target; the suite prioritizes meaningful behavior over
  superficial coverage numbers.
