# Feature Build Index

This folder keeps the original feature-by-feature build plan for PyRiskLab
Version 1. The specs show the intended order of work, acceptance criteria, test
ideas, and portfolio value for each feature.

The implementation now lives in `src/pyrisklab/`, `configs/`, `tests/`, and the
reviewer docs. This index gives a quick map from the planning docs to the
current evidence in the repository.

## Historical Spec Notes

The individual feature files are preserved as build-planning documents. Some of
them intentionally keep early-stage language such as "Open Question",
"placeholder", or "later features" because they record the sequence used to
build Version 1.

For current project status, use the implemented evidence below,
`docs/REQUIREMENTS_TRACEABILITY.md`, and `docs/PROJECT_STATUS.md` rather than
treating every planning note as an unresolved task.

## Build Order

1. Config-driven CLI: implemented in `src/pyrisklab/cli.py`,
   `src/pyrisklab/config.py`, `src/pyrisklab/pipeline.py`, and
   `configs/demo.yaml`.
2. Market simulation: implemented in `src/pyrisklab/market.py`, with tests in
   `tests/test_market.py` and market-path output contract docs.
3. Black-Scholes pricing: implemented in `src/pyrisklab/pricing.py`, with tests
   in `tests/test_pricing.py` and pricing-history output contract docs.
4. Greeks calculation: implemented in `src/pyrisklab/greeks.py`, with tests in
   `tests/test_greeks.py` and Greeks CSV/chart contract docs.
5. Simple fake strategy: implemented in `src/pyrisklab/strategy.py`, with tests
   in `tests/test_strategy.py` and signal output contract docs.
6. Fake execution: implemented in `src/pyrisklab/execution.py`, with tests in
   `tests/test_execution.py` and order/trade output contract docs.
7. Portfolio tracker: implemented in `src/pyrisklab/portfolio.py`, with tests
   in `tests/test_portfolio.py` and portfolio-history contract docs.
8. Risk manager: implemented in `src/pyrisklab/risk.py`, with tests in
   `tests/test_risk.py` and the stress config at `configs/risk_stress.yaml`.
9. Reporting: implemented in `src/pyrisklab/reporting.py`, with sample output
   docs under `docs/sample_outputs/` and `docs/SAMPLE_OUTPUT.md`.
10. Tests: implemented under `tests/`, with strategy notes in
    `docs/TESTING_STRATEGY.md` and helper automation in `scripts/local_verify.py`.
11. Benchmark: implemented in `src/pyrisklab/benchmark.py`, with tests in
    `tests/test_benchmark.py` and performance notes in
    `docs/PERFORMANCE_NOTES.md`.
12. Polished README: implemented in `README.md`, with reviewer support in
    `docs/REVIEWER_GUIDE.md` and resume wording in `docs/RESUME_SNIPPETS.md`.

## Reviewer Notes

- The feature specs are planning artifacts, not generated output.
- Runtime artifacts are generated locally under `results/<run_name>/` and are
  intentionally ignored by Git.
- The primary run command remains:

```bash
python -m pyrisklab run --config configs/demo.yaml --overwrite
```

- Local verification is intentionally user-run:

```bash
pytest
ruff check .
python -m pyrisklab run --config configs/demo.yaml --overwrite
python -m pyrisklab run --config configs/risk_stress.yaml --overwrite
```

## Best Follow-Up Docs

- `docs/REQUIREMENTS_TRACEABILITY.md`
- `docs/REVIEWER_GUIDE.md`
- `docs/FINAL_REVIEW_CHECKLIST.md`
- `docs/PROJECT_STATUS.md`
