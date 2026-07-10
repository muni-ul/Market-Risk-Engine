# Feature 1 — Config-Driven CLI

## 1. Feature Overview

### Feature name

**Config-Driven CLI**

### One-sentence description

A local command-line interface that loads a deterministic YAML config, validates the requested PyRiskLab run, creates the correct output folder, and starts the simulation pipeline through one clear command.

### Detailed description

The Config-Driven CLI is the first feature because it establishes the professional entry point for the whole project. A reviewer should be able to open the repository, install dependencies, and run one command from the terminal:

```bash
python -m pyrisklab run --config configs/demo.yaml
```

The CLI should parse the command, load `configs/demo.yaml`, validate required settings, create `results/<run_name>/`, copy the config into that run folder as `config_used.yaml`, and print readable progress messages. It should not contain market simulation, pricing, Greeks, strategy, execution, portfolio, risk, reporting, or benchmarking logic. Instead, it should delegate orchestration to `pipeline.py`.

This feature turns PyRiskLab from “some Python files” into a local engineering tool. The CLI becomes the stable contract that every later feature plugs into.

### Why it matters

A recruiter or technical reviewer should not need to guess how the project runs. The CLI proves that the project has a real local workflow, a reproducible input file, clean error messages, and an obvious demo path.

**Decision:** Use a CLI-first local workflow instead of a web app.

**Justification:** This project is meant to show Python simulation, automation, testing, and performance-aware engineering. A CLI is simpler, more reproducible, easier to test, and less distracting than a dashboard or SaaS-style interface.

**Decision:** Use config-driven execution instead of hardcoded values.

**Justification:** Config files make runs reproducible, reviewable, and easy to modify without editing source code.

**Decision:** Use YAML for Version 1 configs.

**Justification:** YAML is readable for humans, simple for reviewers, and already fits the planned local architecture.

### Skill it demonstrates

- Python CLI design.
- Package entry points using `python -m pyrisklab`.
- `argparse` command parsing.
- YAML config loading.
- Input validation.
- Custom exception handling.
- Clean separation between CLI, config, and pipeline logic.
- Local file/folder management.
- Testable project startup flow.
- Reviewer-friendly developer experience.

### Priority

**Critical / P0.**

This feature must be built before the other features because all later work depends on a stable way to run the project.

### Complexity

**Medium.**

The CLI itself is not mathematically hard, but it touches important foundations: package structure, config validation, output folder behavior, exception handling, and the public command that reviewers will use.

---

## 2. User/Demo Flow

### Happy path

1. User opens the repo in VS Code.
2. User activates the virtual environment.
3. User runs:

```bash
python -m pyrisklab run --config configs/demo.yaml
```

4. CLI prints progress messages.
5. Config is loaded and validated.
6. `results/demo_run/` is created.
7. The config is copied to `results/demo_run/config_used.yaml`.
8. CLI calls `pipeline.run_simulation(config_path=..., overwrite=False)`.
9. For Feature 1 only, the pipeline may stop after setup or return a placeholder success result.
10. CLI prints a success message with the output path.

Expected terminal output for Feature 1:

```text
[1/4] Loading config: configs/demo.yaml
[2/4] Validating config...
[3/4] Preparing output folder: results/demo_run
[4/4] Starting pipeline...
Done. Run initialized at results/demo_run/
```

### First-time path

1. User clones or opens the project.
2. User creates a virtual environment:

```bash
python -m venv .venv
```

3. User activates it.
4. User installs dependencies:

```bash
pip install -r requirements.txt
```

5. User confirms the CLI command is discoverable:

```bash
python -m pyrisklab --help
```

6. User runs the demo config:

```bash
python -m pyrisklab run --config configs/demo.yaml
```

7. User sees a generated `results/demo_run/` folder.

### Empty state

Empty state means no run has been generated yet.

Expected behavior:

- `results/` may only contain `.gitkeep`.
- README tells the user that results are generated locally by running the CLI.
- CLI should not require pre-existing output files.
- CLI should create `results/<run_name>/` automatically.

Empty `results/` folder should not be treated as an error.

### Error path

Common errors should produce clear messages without a scary stack trace.

#### Missing config file

Command:

```bash
python -m pyrisklab run --config configs/missing.yaml
```

Expected output:

```text
ConfigError: config file not found: configs/missing.yaml
```

#### Invalid YAML

Expected output:

```text
ConfigError: could not parse YAML in configs/demo.yaml. Check indentation and syntax.
```

#### Missing required field

Expected output:

```text
ConfigError: missing required field: run_name
```

#### Invalid numeric field

Expected output:

```text
ConfigError: market.initial_price must be > 0. Received -100.0.
```

#### Output folder already exists

Command:

```bash
python -m pyrisklab run --config configs/demo.yaml
```

If `results/demo_run/` already exists:

```text
RunError: results/demo_run already exists. Use --overwrite or choose a different run_name.
```

With overwrite:

```bash
python -m pyrisklab run --config configs/demo.yaml --overwrite
```

Expected behavior:

- Delete and recreate only `results/demo_run/`.
- Do not delete the whole `results/` folder.
- Do not delete unrelated run folders.

### Demo path for a reviewer

Reviewer should be able to run:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pytest
python -m pyrisklab run --config configs/demo.yaml
```

Then inspect:

```text
results/demo_run/config_used.yaml
```

For Feature 1, the demo proves that the repo can be installed, tested, configured, and run through a clean command. Later features will fill the same run folder with simulation outputs.

---

## 3. UX/UI Requirements

### Screens/pages

This is a local-first project, so the “screens” are:

1. **Terminal CLI experience**
   - Primary user interface.
   - Shows command help, progress, success, and errors.

2. **Config file**
   - `configs/demo.yaml` is the main input surface.
   - User edits run settings here instead of editing Python code.

3. **Generated output folder**
   - `results/<run_name>/` is the first visible artifact.
   - Later features will add CSVs, charts, benchmark outputs, and reports here.

### Components

#### CLI command group

Main command:

```bash
python -m pyrisklab run --config configs/demo.yaml
```

Optional flags:

```bash
python -m pyrisklab run --config configs/demo.yaml --overwrite
python -m pyrisklab run --config configs/demo.yaml --quiet
python -m pyrisklab run --config configs/demo.yaml --debug
```

**Decision:** Include `--overwrite` in Feature 1.

**Justification:** Reviewers and developers will rerun the demo often. Without overwrite support, the first rerun becomes annoying.

**Decision:** Include `--debug` only if it is simple.

**Justification:** Debug mode is useful for development, but the MVP should not become a full logging framework in Feature 1.

**Decision:** Treat `--quiet` as optional.

**Justification:** Quiet mode is nice but not required for reviewer value. Progress messages are more important.

### Forms/inputs

There is no web form. Inputs are CLI arguments and YAML config values.

#### CLI inputs

| Input | Required | Example | Purpose |
|---|---:|---|---|
| `run` command | Yes | `run` | Starts a local PyRiskLab run. |
| `--config` | Yes | `configs/demo.yaml` | Path to the YAML config file. |
| `--overwrite` | No | `--overwrite` | Allows replacing an existing run folder. |
| `--debug` | No | `--debug` | Shows traceback/details for development. |
| `--quiet` | No | `--quiet` | Reduces progress output. |

#### Config inputs

Minimum config structure for Feature 1:

```yaml
run_name: demo_run
seed: 42
output_dir: results

market:
  initial_price: 100.0
  drift: 0.05
  volatility: 0.20
  trading_days: 252
  steps: 252
  paths: 1

option:
  underlying_symbol: SIM_STOCK
  symbol: CALL_105
  option_type: call
  strike: 105.0
  risk_free_rate: 0.04
  volatility: 0.20
  days_to_expiry: 90

strategy:
  name: simple_delta_rule
  buy_delta_below: 0.45
  sell_delta_above: 0.70
  trade_quantity: 1

risk:
  starting_cash: 10000.0
  max_position_quantity: 10
  max_trade_notional: 2500.0
  max_drawdown_pct: 0.15
  max_loss_pct: 0.10

benchmark:
  enabled: true
  num_prices: 100000
```

**Decision:** Feature 1 should validate the full config shape even though later features implement the behavior.

**Justification:** Catching bad config early prevents confusing failures later in the pipeline.

### Buttons/actions

There are no graphical buttons. Actions are terminal commands.

| Action | Command |
|---|---|
| Show help | `python -m pyrisklab --help` |
| Show run help | `python -m pyrisklab run --help` |
| Run demo | `python -m pyrisklab run --config configs/demo.yaml` |
| Rerun demo | `python -m pyrisklab run --config configs/demo.yaml --overwrite` |
| Run tests | `pytest` |

### Validation messages

Validation messages must be specific and actionable.

Good:

```text
ConfigError: option.option_type must be 'call' or 'put'. Received 'calls'.
```

Bad:

```text
Error: invalid config
```

Good:

```text
ConfigError: benchmark.num_prices must be > 0 when benchmark.enabled is true. Received 0.
```

Bad:

```text
ValueError
```

### Empty states

| Empty state | Expected behavior |
|---|---|
| No `results/demo_run/` yet | CLI creates it. |
| Empty `results/` folder | Not an error. |
| Missing `results/` folder | CLI creates `results/` and `results/<run_name>/`. |
| Missing optional run artifacts | Not an error in Feature 1 because later features create them. |

### Loading states

CLI progress messages are the loading states.

Expected default progress:

```text
[1/4] Loading config...
[2/4] Validating config...
[3/4] Preparing output directory...
[4/4] Starting pipeline...
```

**Decision:** Use numbered progress steps.

**Justification:** Numbered steps make the tool feel organized and help a reviewer see where the run failed.

### Error states

Errors should be handled through custom exceptions:

- `PyRiskLabError`
- `ConfigError`
- `RunError`

Normal user-caused errors should not show a full traceback unless `--debug` is passed.

### Responsive behavior if relevant

Not relevant for Feature 1.

This is a terminal-based local tool. There is no mobile or responsive UI requirement.

---

## 4. Data Requirements

### Entities involved

#### 1. CLIArgs

Represents parsed command-line arguments.

Fields:

| Field | Type | Required | Example |
|---|---|---:|---|
| `command` | `str` | Yes | `run` |
| `config_path` | `Path` | Yes | `configs/demo.yaml` |
| `overwrite` | `bool` | No | `False` |
| `debug` | `bool` | No | `False` |
| `quiet` | `bool` | No | `False` |

#### 2. RunConfig

Top-level validated config object.

Fields:

| Field | Type | Required | Example |
|---|---|---:|---|
| `run_name` | `str` | Yes | `demo_run` |
| `seed` | `int` | Yes | `42` |
| `output_dir` | `str` | Yes | `results` |
| `market` | `MarketConfig` | Yes | See below |
| `option` | `OptionConfig` | Yes | See below |
| `strategy` | `StrategyConfig` | Yes | See below |
| `risk` | `RiskConfig` | Yes | See below |
| `benchmark` | `BenchmarkConfig` | Yes | See below |

#### 3. MarketConfig

Fields:

| Field | Type | Validation |
|---|---|---|
| `initial_price` | `float` | `> 0` |
| `drift` | `float` | Any real number allowed |
| `volatility` | `float` | `>= 0` |
| `trading_days` | `int` | `> 0` |
| `steps` | `int` | `> 0` |
| `paths` | `int` | `>= 1` |

#### 4. OptionConfig

Fields:

| Field | Type | Validation |
|---|---|---|
| `underlying_symbol` | `str` | Non-empty |
| `symbol` | `str` | Non-empty |
| `option_type` | `str` | `call` or `put` |
| `strike` | `float` | `> 0` |
| `risk_free_rate` | `float` | Any real number allowed |
| `volatility` | `float` | `>= 0` |
| `days_to_expiry` | `int` | `>= 0` |

#### 5. StrategyConfig

Fields:

| Field | Type | Validation |
|---|---|---|
| `name` | `str` | Non-empty; Version 1 supports `simple_delta_rule` later |
| `buy_delta_below` | `float` | Numeric |
| `sell_delta_above` | `float` | Numeric |
| `trade_quantity` | `int` | `> 0` |

#### 6. RiskConfig

Fields:

| Field | Type | Validation |
|---|---|---|
| `starting_cash` | `float` | `> 0` |
| `max_position_quantity` | `int` | `>= 0` |
| `max_trade_notional` | `float` | `>= 0` |
| `max_drawdown_pct` | `float` | `>= 0` and preferably `<= 1` |
| `max_loss_pct` | `float` | `>= 0` and preferably `<= 1` |

#### 7. BenchmarkConfig

Fields:

| Field | Type | Validation |
|---|---|---|
| `enabled` | `bool` | Required |
| `num_prices` | `int` | `> 0` if benchmark is enabled |

#### 8. RunResult

For Feature 1, this can be minimal.

Fields:

| Field | Type | Example |
|---|---|---|
| `run_name` | `str` | `demo_run` |
| `output_path` | `Path` | `results/demo_run` |
| `config_path` | `Path` | `configs/demo.yaml` |
| `status` | `str` | `initialized` |

### Relationships

- One CLI command points to one config file.
- One config file creates one `RunConfig`.
- One `RunConfig` creates one run folder.
- One run folder stores one copied `config_used.yaml`.
- Later features will use the same `RunConfig` to generate market data, pricing data, portfolio data, risk events, reports, tests, and benchmark outputs.

### Example seed data

Use `configs/demo.yaml` as the canonical seed config:

```yaml
run_name: demo_run
seed: 42
output_dir: results

market:
  initial_price: 100.0
  drift: 0.05
  volatility: 0.20
  trading_days: 252
  steps: 252
  paths: 1

option:
  underlying_symbol: SIM_STOCK
  symbol: CALL_105
  option_type: call
  strike: 105.0
  risk_free_rate: 0.04
  volatility: 0.20
  days_to_expiry: 90

strategy:
  name: simple_delta_rule
  buy_delta_below: 0.45
  sell_delta_above: 0.70
  trade_quantity: 1

risk:
  starting_cash: 10000.0
  max_position_quantity: 10
  max_trade_notional: 2500.0
  max_drawdown_pct: 0.15
  max_loss_pct: 0.10

benchmark:
  enabled: true
  num_prices: 100000
```

### Local persistence needs

Feature 1 should create:

```text
results/demo_run/
  config_used.yaml
```

Optional Feature 1 metadata file:

```text
results/demo_run/
  run_metadata.json
```

**Decision:** `config_used.yaml` should be required.

**Justification:** It proves reproducibility. A reviewer can always see which inputs produced a run.

**Decision:** `run_metadata.json` is optional.

**Justification:** It can be useful later, but the reporting feature will handle richer run summaries.

[Open Question] Should `run_metadata.json` be included in the MVP, or should run metadata wait until the Reporting feature?

---

## 5. Logic Requirements

### Business rules

1. CLI must support the `run` command.
2. `--config` must be required for `run`.
3. Config path must exist.
4. Config must parse as YAML.
5. Config must include required top-level sections.
6. Config values must be validated before pipeline execution.
7. `run_name` must be safe for a local folder name.
8. Output path must resolve to `output_dir/run_name`.
9. Existing run folder should fail unless `--overwrite` is passed.
10. `--overwrite` must only delete the selected run folder.
11. CLI should print helpful progress unless `--quiet` is enabled.
12. CLI should catch expected project errors and print clean messages.
13. CLI should show full traceback only in debug mode.
14. No internet, API key, database, cloud service, login, or live market data should be required.

### Calculations

This feature has no finance calculations.

Small path calculation:

```text
run_output_path = Path(output_dir) / run_name
```

Path safety rule:

- `run_name` should not contain path traversal such as `../`.
- `run_name` should not be empty.
- Recommended allowed pattern: letters, numbers, underscore, hyphen.

Example valid run names:

```text
demo_run
high_volatility
low-vol-demo
run_001
```

Example invalid run names:

```text
../demo_run
my/run

```

### API/service functions if needed

#### `cli.py`

```python
def main(argv: list[str] | None = None) -> int:
    """Parse CLI arguments and dispatch commands."""
```

```python
def build_parser() -> argparse.ArgumentParser:
    """Create the PyRiskLab command parser."""
```

#### `config.py`

```python
def load_config(config_path: str | Path) -> RunConfig:
    """Load, validate, and return a RunConfig."""
```

```python
def validate_config(raw: dict) -> RunConfig:
    """Validate raw config dictionary and convert it to dataclasses."""
```

#### `pipeline.py`

```python
def run_simulation(config_path: str | Path, overwrite: bool = False) -> RunResult:
    """Coordinate a PyRiskLab run."""
```

For Feature 1, this function can:

1. Load config.
2. Prepare output directory.
3. Copy config.
4. Return `RunResult`.

Later features will extend the internal pipeline after this setup step.

#### `exceptions.py`

```python
class PyRiskLabError(Exception):
    """Base exception for expected PyRiskLab errors."""

class ConfigError(PyRiskLabError):
    """Raised for invalid config files or config values."""

class RunError(PyRiskLabError):
    """Raised for run setup and output folder problems."""
```

### State management

Feature 1 should avoid global mutable state.

State should flow like this:

```text
CLI args
  -> config path
  -> load_config()
  -> RunConfig dataclass
  -> pipeline.run_simulation()
  -> output folder
  -> RunResult
  -> CLI success/error message
```

**Decision:** Use dataclasses for config objects.

**Justification:** Dataclasses make the config structure explicit without adding a heavy dependency like Pydantic.

**Decision:** Avoid passing raw dictionaries around after validation.

**Justification:** Typed config objects reduce confusion and make later features easier to test.

### Edge cases

| Edge case | Expected behavior |
|---|---|
| Config file missing | Raise `ConfigError` with path. |
| Config file is empty | Raise `ConfigError` explaining that config is empty. |
| YAML syntax error | Raise `ConfigError` with readable parse hint. |
| Missing `run_name` | Raise `ConfigError`. |
| Empty `run_name` | Raise `ConfigError`. |
| Unsafe `run_name` | Raise `ConfigError`. |
| Missing `output_dir` | Either default to `results` or raise `ConfigError`. |
| Existing output folder without `--overwrite` | Raise `RunError`. |
| Existing output folder with `--overwrite` | Delete only that folder and recreate it. |
| Invalid volatility | Raise `ConfigError`. |
| Invalid option type | Raise `ConfigError`. |
| Invalid benchmark count | Raise `ConfigError`. |
| User runs unknown command | Show CLI help. |
| User passes no args | Show CLI help and nonzero exit code. |
| User runs from different working directory | Relative paths should resolve from current working directory. |
| Output directory cannot be created | Raise `RunError`. |

[Open Question] Should missing `output_dir` default to `results`, or should the config require it explicitly?

Recommended decision: default to `results` for smoother local demo, but still write the resolved value into `config_used.yaml` or metadata.

---

## 6. Acceptance Criteria

### CLI help

**Given** the project is installed or run from the repo root  
**When** the user runs `python -m pyrisklab --help`  
**Then** the CLI shows available commands including `run`.

**Given** the project is installed or run from the repo root  
**When** the user runs `python -m pyrisklab run --help`  
**Then** the CLI explains `--config`, `--overwrite`, and any supported optional flags.

### Successful run initialization

**Given** `configs/demo.yaml` exists and is valid  
**When** the user runs `python -m pyrisklab run --config configs/demo.yaml`  
**Then** the CLI loads the config, validates it, creates `results/demo_run/`, copies `config_used.yaml`, and exits successfully.

**Given** `configs/demo.yaml` exists and is valid  
**When** the command completes  
**Then** the terminal output includes the final output path.

### Config validation

**Given** a config file is missing `run_name`  
**When** the user runs the CLI with that config  
**Then** the CLI exits with a `ConfigError` explaining that `run_name` is missing.

**Given** a config file has `market.volatility: -0.2`  
**When** the user runs the CLI with that config  
**Then** the CLI exits with `ConfigError: market.volatility must be >= 0`.

**Given** a config file has `option.option_type: calls`  
**When** the user runs the CLI with that config  
**Then** the CLI exits with a message explaining that option type must be `call` or `put`.

### Output folder behavior

**Given** `results/demo_run/` does not exist  
**When** the user runs the demo command  
**Then** the folder is created.

**Given** `results/demo_run/` already exists  
**When** the user runs the demo command without `--overwrite`  
**Then** the CLI exits with a `RunError` telling the user to use `--overwrite` or change `run_name`.

**Given** `results/demo_run/` already exists  
**When** the user runs the demo command with `--overwrite`  
**Then** only `results/demo_run/` is replaced and unrelated folders under `results/` remain untouched.

### Error handling

**Given** a normal user-caused error occurs  
**When** debug mode is not enabled  
**Then** the CLI prints a clean message without a full traceback.

**Given** a normal user-caused error occurs  
**When** debug mode is enabled  
**Then** the CLI may show extra diagnostic details useful for development.

### Scope control

**Given** Feature 1 is implemented  
**When** the CLI run completes  
**Then** it should not require internet, live market data, brokerage credentials, a database, cloud services, login, or a dashboard.

---

## 7. Test Plan

### Unit tests

#### `tests/test_cli.py`

Test cases:

1. `python -m pyrisklab --help` returns help text.
2. `run --help` includes `--config`.
3. Missing `--config` returns a useful parser error.
4. Unknown command returns a nonzero exit code.
5. CLI catches `ConfigError` and returns nonzero exit code.
6. CLI catches `RunError` and returns nonzero exit code.

Implementation note:

- Prefer testing `main(argv=[...])` directly instead of shelling out for every test.
- Add one subprocess smoke test if useful.

#### `tests/test_config.py`

Test cases:

1. Valid demo config loads.
2. Missing file raises `ConfigError`.
3. Empty YAML raises `ConfigError`.
4. Invalid YAML raises `ConfigError`.
5. Missing top-level section raises `ConfigError`.
6. Missing nested field raises `ConfigError`.
7. Invalid `market.initial_price` fails.
8. Invalid `market.volatility` fails.
9. Invalid `market.steps` fails.
10. Invalid `option.option_type` fails.
11. Invalid `option.strike` fails.
12. Invalid `risk.starting_cash` fails.
13. Invalid `benchmark.num_prices` fails when enabled.
14. Unsafe `run_name` fails.

#### `tests/test_pipeline.py`

Test cases:

1. Valid config creates output folder.
2. Valid config copies `config_used.yaml`.
3. Existing folder without overwrite raises `RunError`.
4. Existing folder with overwrite succeeds.
5. Overwrite does not delete sibling folders.
6. Returned `RunResult` includes run name and output path.

#### `tests/test_exceptions.py`

Test cases:

1. `ConfigError` inherits from `PyRiskLabError`.
2. `RunError` inherits from `PyRiskLabError`.
3. Exception string is readable.

### Integration tests if useful

#### CLI subprocess smoke test

Use `subprocess.run` on:

```bash
python -m pyrisklab run --config <temp_demo_config>
```

Expected:

- Return code is `0`.
- Output folder exists.
- `config_used.yaml` exists.
- Terminal output contains `Done`.

#### Rerun test

1. Run once successfully.
2. Run again without `--overwrite` and expect failure.
3. Run again with `--overwrite` and expect success.

### Manual QA checklist

- [ ] `python -m pyrisklab --help` works.
- [ ] `python -m pyrisklab run --help` works.
- [ ] `python -m pyrisklab run --config configs/demo.yaml` works.
- [ ] `results/demo_run/` is created.
- [ ] `results/demo_run/config_used.yaml` is created.
- [ ] Rerunning without `--overwrite` gives a clear error.
- [ ] Rerunning with `--overwrite` succeeds.
- [ ] Bad config path gives a clear error.
- [ ] Bad YAML gives a clear error.
- [ ] Negative volatility gives a clear error.
- [ ] Invalid option type gives a clear error.
- [ ] No stack trace appears for normal user mistakes.
- [ ] The command works from VS Code terminal on Windows.

### Demo verification checklist

- [ ] Fresh clone setup instructions lead to a working CLI.
- [ ] `pytest` passes before the demo command.
- [ ] Demo command is short and obvious.
- [ ] Output path is printed.
- [ ] Config copy proves reproducibility.
- [ ] README can point to this command as the main project entry point.

---

## 8. Portfolio Value

### How this feature helps the project stand out

This feature makes the project feel like a real local tool instead of a collection of scripts. Recruiters may not inspect every function, but they can immediately understand a project that runs from one command and produces a predictable output folder.

It also creates the foundation for stronger claims later:

- Config-driven reproducibility.
- Local CLI automation.
- Clean package structure.
- Testable startup flow.
- Clear error handling.
- No dependency on external services.

### What to mention in README

README should say:

```text
Run a full local PyRiskLab simulation with one command:

python -m pyrisklab run --config configs/demo.yaml
```

README should also explain:

- The config file controls the run.
- The same config and seed produce reproducible outputs.
- Results are written under `results/<run_name>/`.
- The project is local-only and does not connect to brokerages or live market APIs.
- `--overwrite` can be used for rerunning a demo.

### What to mention in interviews

Strong interview explanation:

> I started with the CLI and config system because I wanted the project to behave like a real engineering tool, not a notebook. The CLI gives reviewers one command to run, and the YAML config makes the simulation reproducible. I also separated CLI parsing, config validation, and pipeline orchestration so later modules like pricing, portfolio tracking, risk, and reporting could plug into a stable entry point.

Talking points:

- Why CLI-first matched the local portfolio goal.
- Why config files are better than hardcoded constants.
- How validation prevents broken downstream calculations.
- How custom exceptions improve developer experience.
- How `--overwrite` supports repeatable demos.
- Why this feature intentionally avoids dashboards, databases, login, and live data.

---

## 9. Implementation Notes For Codex

### Likely files/folders

Create or update:

```text
pyrisklab/
  configs/
    demo.yaml

  src/
    pyrisklab/
      __init__.py
      __main__.py
      cli.py
      config.py
      pipeline.py
      models.py
      exceptions.py

  tests/
    test_cli.py
    test_config.py
    test_pipeline.py
    test_exceptions.py

  results/
    .gitkeep

  requirements.txt
  pyproject.toml
  README.md
```

### File responsibilities

#### `src/pyrisklab/__main__.py`

Should be tiny:

```python
from pyrisklab.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
```

#### `src/pyrisklab/cli.py`

Responsibilities:

- Build `argparse` parser.
- Define `run` command.
- Parse `--config`, `--overwrite`, optional `--debug`, optional `--quiet`.
- Call `pipeline.run_simulation(...)`.
- Catch `PyRiskLabError`.
- Return process exit codes.

#### `src/pyrisklab/config.py`

Responsibilities:

- Read YAML.
- Validate required fields.
- Convert raw dictionaries into dataclasses from `models.py`.
- Raise `ConfigError` with exact field names.

#### `src/pyrisklab/models.py`

For Feature 1, include config dataclasses:

- `RunConfig`
- `MarketConfig`
- `OptionConfig`
- `StrategyConfig`
- `RiskConfig`
- `BenchmarkConfig`
- `RunResult`

Later features can add:

- `Order`
- `Trade`
- `Position`
- `PortfolioSnapshot`
- `RiskEvent`

#### `src/pyrisklab/pipeline.py`

Feature 1 responsibilities:

- Load config.
- Resolve output path.
- Check existing output folder.
- Handle overwrite.
- Create output folder.
- Copy config to `config_used.yaml`.
- Return `RunResult`.

Do not implement market simulation or pricing here yet.

#### `src/pyrisklab/exceptions.py`

Include:

- `PyRiskLabError`
- `ConfigError`
- `RunError`

### Build order

1. Create package skeleton.
2. Add `__main__.py` and minimal `cli.py`.
3. Add `configs/demo.yaml`.
4. Add `exceptions.py`.
5. Add dataclasses in `models.py`.
6. Implement `config.load_config`.
7. Implement validation helpers.
8. Implement `pipeline.run_simulation` with output folder creation.
9. Add `--overwrite` behavior.
10. Add clean CLI error handling.
11. Add tests for config loading.
12. Add tests for pipeline output folder behavior.
13. Add tests for CLI parser behavior.
14. Run `pytest`.
15. Run `ruff check .` and `ruff format .`.
16. Update README with the command.

### Risks

#### Risk 1: CLI becomes too large

Mitigation:

- Keep `cli.py` focused on parsing and messages.
- Put orchestration in `pipeline.py`.
- Put validation in `config.py`.

#### Risk 2: Config validation becomes messy

Mitigation:

- Use small helper functions like `require_field`, `validate_positive`, and `validate_nonnegative`.
- Raise `ConfigError` with exact field paths.

#### Risk 3: Raw dictionaries spread through the app

Mitigation:

- Convert config into dataclasses immediately after validation.

#### Risk 4: Overwrite deletes too much

Mitigation:

- Resolve `output_path = output_dir / run_name`.
- Only delete `output_path`.
- Add a test proving sibling folders survive.

#### Risk 5: Feature 1 accidentally implements later features

Mitigation:

- Stop after loading config and initializing output.
- Add clear TODO placeholders for market simulation, pricing, reporting, and benchmark.

### What not to change

Do not add:

- Streamlit dashboard.
- FastAPI backend.
- React frontend.
- Login or user accounts.
- Database.
- Docker requirement.
- Cloud deployment.
- Live market data.
- Brokerage integration.
- Real trading.
- Payment or SaaS systems.
- Machine learning strategy.
- Complex plugin architecture.

Do not change the project direction:

- Keep PyRiskLab local-first.
- Keep Python as the main focus.
- Keep the CLI as the primary entry point.
- Keep the command compatible with:

```bash
python -m pyrisklab run --config configs/demo.yaml
```

### Definition of done

Feature 1 is done when:

- [ ] `python -m pyrisklab --help` works.
- [ ] `python -m pyrisklab run --help` works.
- [ ] `python -m pyrisklab run --config configs/demo.yaml` works.
- [ ] `results/demo_run/config_used.yaml` is created.
- [ ] Existing output folder behavior is correct.
- [ ] Invalid configs fail with readable messages.
- [ ] Tests cover config loading, CLI behavior, and output folder setup.
- [ ] No internet, cloud, database, dashboard, or live data is required.
- [ ] README includes the command and describes the config-driven workflow.
