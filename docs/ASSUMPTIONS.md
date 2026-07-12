# Assumptions And Limitations

PyRiskLab uses finance as a simulation domain, but the project goal is software
engineering: deterministic execution, validation, benchmarking, and reproducible
artifacts. This page centralizes the assumptions behind the Version 1 MVP.

## Market Simulation

- Market data is synthetic, generated locally, and seeded from the YAML config.
- The market path uses geometric Brownian motion with configured annualized
  drift and volatility.
- Step indexes are deterministic integers, not real calendar dates.
- The demo uses one primary path so downstream reports stay simple to inspect.

## Pricing And Greeks

- Option pricing uses Black-Scholes formulas for European calls and puts.
- Greeks are computed from the same model assumptions used by pricing.
- The model inputs are simulation assumptions, not live market observations.
- Expiry and zero-volatility edge cases are handled explicitly in code/tests.

## Strategy And Execution

- The strategy is intentionally simple and deterministic. It exists to create
  system behavior for execution, risk, portfolio, and reporting.
- Fake execution uses the configured deterministic fill model
  `deterministic_mid`.
- Simulated orders and trades are local artifacts only; no broker, exchange, or
  real account is involved.

## Portfolio And Risk

- Portfolio accounting tracks a single configured option contract for Version 1.
- Contract multiplier, commission, cash, and risk limits are config-driven local
  assumptions.
- Risk rules validate proposed simulated orders and record blocked-order
  reasons for auditability.
- Risk output is not a real financial risk model and should not be used for
  investment decisions.

## Benchmark

- The benchmark compares loop-based and vectorized Black-Scholes pricing on the
  same generated inputs.
- Speedup is machine-dependent and should be interpreted as performance
  engineering evidence, not a universal claim.
- Numerical equivalence is checked before speedup is reported.

## Out Of Scope

Version 1 intentionally excludes live market data, brokerage integration, real
trades, dashboards, databases, cloud deployment, user accounts, payments, ML
trading prediction, investment advice, and profitability claims.
