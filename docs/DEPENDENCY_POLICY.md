# Dependency Policy

PyRiskLab intentionally uses a small local Python stack. Dependencies should
support the Version 1 goal: a reproducible CLI simulation engine with numerical
computation, tests, benchmark evidence, and inspectable local artifacts.

## Runtime Dependencies

Runtime dependencies are limited to:

- `numpy` for vectorized numerical arrays
- `pandas` for tabular simulation and artifact pipelines
- `scipy` for Black-Scholes normal distribution calculations
- `matplotlib` for static PNG charts
- `PyYAML` for deterministic config files

## Development Dependencies

Development dependencies are limited to:

- `pytest` for behavior-focused tests
- `ruff` for linting and import hygiene

## What Not To Add In Version 1

Do not add dependencies for:

- live market data
- brokerage APIs
- dashboards or web apps
- databases
- cloud deployment
- user accounts or payments
- ML trading prediction
- notebooks as the primary execution path

Optional future performance tooling, such as Numba or multiprocessing examples,
should only be considered after the baseline loop-vs-NumPy benchmark remains
clear, reproducible, and documented.

## Review Rule

Before adding a dependency, ask whether it strengthens one of the core
software-engineering signals: deterministic execution, validation, numerical
correctness, testability, benchmark reporting, debugging, packaging, or
reviewer documentation. If it does not, keep the project dependency-light.
