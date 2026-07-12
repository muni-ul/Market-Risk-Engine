# PyRiskLab Demo Walkthrough

Use this guide when preparing a GitHub profile review, resume discussion, or
short interview walkthrough. The goal is to show PyRiskLab as a local software
engineering project: deterministic CLI execution, generated artifacts, risk
auditability, and benchmark evidence.

## Before Recording Or Capturing

Start from the repository root after installing dependencies. Keep the run local
and deterministic:

```bash
python -m pyrisklab run --config configs/demo.yaml --overwrite
```

For the risk-audit variant:

```bash
python -m pyrisklab run --config configs/risk_stress.yaml --overwrite
```

That command writes `results/risk_stress_run/`, where blocked-order artifacts
make the risk audit easy to inspect.

Run `pytest` and `ruff check .` during your own final validation pass. The demo
walkthrough itself should focus on the project story and generated artifacts,
not on live trading or market prediction.

If you want the full local validation sequence in one command, run:

```bash
python scripts/local_verify.py
```

Use `python scripts/local_verify.py --list` to preview the commands before
running them.

For a shorter pre-recording check, target only the commands you need:

```bash
python scripts/local_verify.py --only ruff --only demo
```

## Thirty-Second Demo Path

1. Show the top of `README.md` and the simulation-only disclaimer.
2. Run or reference the one-command demo.
3. Open `results/demo_run/summary_report.md`.
4. Open `results/demo_run/run_metadata.json`.
5. Open `results/demo_run/benchmark.csv`.
6. Show one or two PNG charts from `results/demo_run/`.

That path demonstrates the full loop: config in, deterministic pipeline,
reports out.

## Screenshot Targets

After running the demo locally, the most useful screenshot-ready artifacts are:

- `results/demo_run/summary_report.md`: scope, risk/execution audit, benchmark,
  generated artifacts, and limitations in one readable file.
- `results/demo_run/portfolio_value.png`: visible portfolio state over the
  simulated run.
- `results/demo_run/drawdown.png`: risk-focused chart that is easy to explain.
- `results/demo_run/benchmark.csv`: loop-vs-vectorized performance evidence.
- `results/demo_run/run_metadata.json`: reproducibility metadata and artifact
  completeness evidence.

Use `docs/assets/README.md` for the recommended screenshot names if you decide
to commit a small curated image set after your final local validation pass.

Avoid screenshots that imply real trading performance, live market data, or
brokerage connectivity.

## Interview Talk Track

Use concise software-engineering framing:

> I built PyRiskLab as a local Python simulation engine. The finance domain
> gives the project realistic numerical and state-management problems, but the
> engineering signal is the package structure, deterministic config pipeline,
> tests, risk validation, benchmark, and reproducible CSV/PNG/Markdown outputs.

If asked about the benchmark:

> The benchmark compares a Python-loop Black-Scholes path against a vectorized
> NumPy path on the same deterministic inputs. It verifies numerical equivalence
> before reporting speedup, and the docs call out that timing is machine
> dependent.

If asked about scope:

> It is simulation only. There is no live market data, no brokerage integration,
> no real trades, no accounts, and no investment advice.

## What Not To Claim

Do not present PyRiskLab as:

- a trading bot
- a real risk-management platform
- an investing strategy
- a live-market dashboard
- a profitability model
- a cloud or SaaS product

The strongest story is that it is a finished local Python engineering tool with
clear boundaries and reproducible outputs.
