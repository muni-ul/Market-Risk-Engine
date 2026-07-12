# Security Policy

PyRiskLab is a local simulation project. It does not require accounts, API keys,
broker credentials, live market-data feeds, databases, hosted services, or cloud
deployment to run the Version 1 MVP.

## Supported Version

| Version | Supported |
| --- | --- |
| `0.1.x` | Yes |

## Local-Only Boundary

- Keep real `.env` files, secrets, generated run outputs, virtual environments,
  caches, coverage reports, and build artifacts out of git.
- Do not add live brokerage integrations, real order execution, live market-data
  clients, account logins, payment systems, hosted dashboards, or investment
  advice features.
- Treat generated CSV, PNG, JSON, YAML, and Markdown artifacts as local outputs
  created by deterministic demo configs.

## Reporting Issues

For normal project issues, use the repository issue tracker linked from
`pyproject.toml`.

If you notice accidentally committed secrets or credentials, remove them from
the working tree immediately and rotate the affected credential outside this
project. PyRiskLab should not need secrets in the first place.
