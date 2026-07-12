# Platform Notes

PyRiskLab is designed as a local Python CLI project. It should not require
Docker, databases, compilers, cloud services, accounts, API keys, or operating
system-specific services for the Version 1 MVP.

## Supported Local Workflow

- Python 3.11 or newer
- A normal virtual environment such as `.venv`
- `pip install -r requirements.txt` or `pip install -e ".[dev]"`
- Commands run from the repository root

The README includes setup commands for Windows PowerShell and macOS/Linux
shells. The runtime code uses `pathlib` and UTF-8 file reads/writes for local
paths and text artifacts.

## Generated Artifacts

Generated outputs are written under `results/<run_name>/` and are ignored by
Git except for `results/.gitkeep`. The report metadata records the local Python
version and platform so reviewers can understand where a run was produced.

PNG charts are generated with matplotlib's non-interactive `Agg` backend, so a
desktop plotting window is not required.

## Expected Differences By Machine

- Benchmark timings and speedup vary by CPU, Python version, library versions,
  and background load.
- PNG metadata or rendering details may differ slightly by matplotlib version.
- File path separators differ by platform, but docs use forward slashes for
  GitHub readability.

These differences should not change the stable output contracts documented in
`docs/sample_outputs/`.

## Validation On Different Machines

Use `python scripts/local_verify.py --list` to preview the local validation
sequence on a new machine before running it. For a narrower first check, use a
targeted helper command such as `python scripts/local_verify.py --only ruff
--only demo`.

If a platform-specific issue appears during setup, artifact generation, or
benchmark review, use `docs/DEBUGGING_GUIDE.md` for triage and
`docs/FINAL_REVIEW_CHECKLIST.md` for the full resume-ready validation gate.
