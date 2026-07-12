# Support

PyRiskLab is a local Python simulation portfolio project. Support is focused on
reproducible local runs, documentation clarity, output contracts, and
simulation-only scope.

## Best Starting Points

- For a quick technical review path, read `docs/REVIEWER_GUIDE.md`.
- For installation, demo commands, outputs, and troubleshooting, read
  `README.md`.
- For final validation before using the project publicly, read
  `docs/FINAL_REVIEW_CHECKLIST.md`.
- For security and no-secrets boundaries, read `SECURITY.md`.

## Reporting Bugs

Use the GitHub bug report template for reproducible local issues. Include:

- Python version and operating system
- Command or config used
- Commit or version
- Relevant generated artifact names, row counts, or short excerpts

Generated `results/` folders should stay local. Share only the details needed
to reproduce or inspect the issue.

## Requesting Enhancements

Use the feature request template for scoped improvements that strengthen the
software-engineering signal: CLI automation, deterministic configs, validation,
tests, benchmark reporting, debugging, packaging, or reviewer documentation.

Feature requests should not add live market data, brokerage integration, real
orders, dashboards, SaaS features, databases, cloud deployment, accounts,
payments, ML trading prediction, or investment advice.

## Security Issues

PyRiskLab should not require secrets. If a secret is accidentally committed,
remove it immediately and rotate the affected credential outside this project.
See `SECURITY.md` for the local-only boundary.
