# Feature 9: Reporting

## Output Path

`docs/features/09-reporting.md`

---

## 1. Feature Overview

### Feature name

**Reporting**

### One-sentence description

Generate clean local run artifacts including CSV files, PNG charts, a copied config file, and a Markdown summary report under `results/<run_name>/`.

### Detailed description

The Reporting feature turns a completed PyRiskLab simulation run into reviewer-friendly local artifacts. It takes the outputs from earlier features and writes them into a predictable results folder.

This feature should create:

- `config_used.yaml`
- `market_path.csv`
- `pricing_history.csv`
- `greeks_history.csv`
- `signals.csv`
- `orders.csv`
- `trades.csv`
- `portfolio_history.csv`
- `risk_events.csv`
- PNG charts for key outputs
- `summary_report.md`

Reporting should make the project easy to inspect without reading the source code. A reviewer should be able to open `results/demo_run/` and immediately understand what happened in the simulation.

This feature should not create a dashboard, database, cloud report, hosted website, login system, or live market-data integration.

### Why it matters

Reporting is what makes PyRiskLab portfolio-ready. The code may be strong, but recruiters and reviewers need visible outputs. Clean reports show that the project is complete, reproducible, and easy to demo.

This feature also proves practical software skills: file I/O, pandas exports, chart generation, formatting, empty-state handling, and readable output organization.

### Skill it demonstrates

- pandas CSV export
- matplotlib chart generation
- Markdown report generation
- Local artifact organization
- Clean file naming
- Empty-state handling
- Reproducible output structure
- User-facing communication through generated reports

### Priority

**High**

This is a core feature because PyRiskLab needs visible outputs to be impressive on GitHub and in interviews.

### Complexity

**Medium**

The logic is not mathematically difficult, but the feature requires polish, consistency, and careful handling of empty or missing data.

---

## 2. User/Demo Flow

### Happy path

1. User runs:

```bash
python -m pyrisklab run --config configs/demo.yaml
```

2. The pipeline completes all earlier feature steps.
3. Reporting creates:

```text
results/demo_run/
```

4. Reporting saves all available tables as CSV files.
5. Reporting saves readable PNG charts.
6. Reporting copies the used config into the run folder.
7. Reporting generates:

```text
summary_report.md
```

8. CLI prints:

```text
Done. Results saved to results/demo_run/
```

### First-time path

A first-time user should not need to manually create result folders.

The app should:

- Create `results/` if it does not exist.
- Create `results/<run_name>/`.
- Fail clearly if the run folder already exists and `--overwrite` is not used.
- Save every report artifact in one predictable place.

Expected first-time output:

```text
results/demo_run/
  config_used.yaml
  market_path.csv
  pricing_history.csv
  greeks_history.csv
  signals.csv
  orders.csv
  trades.csv
  portfolio_history.csv
  risk_events.csv
  market_path.png
  option_price.png
  greeks.png
  portfolio_value.png
  drawdown.png
  summary_report.md
```

### Empty state

Reporting must handle valid empty states gracefully.

#### No trades

Still create:

```text
trades.csv
```

with headers and zero rows.

Summary report should say:

```text
No trades were executed in this run.
```

#### No risk events

Still create:

```text
risk_events.csv
```

with headers and zero rows.

Summary report should say:

```text
No risk events were triggered in this run.
```

#### Benchmark disabled

Benchmark belongs to Feature 11, but reporting should eventually handle:

```text
Benchmark was skipped by config.
```

[Decision] For Feature 9, only reserve the report section. Actual benchmark generation belongs to Feature 11.

### Error path

Expected reporting errors should be clear:

```text
ReportingError: results/demo_run already exists. Use --overwrite or choose a different run_name.
ReportingError: cannot write portfolio_history.csv because output directory is missing.
ReportingError: missing required DataFrame for market_path.csv.
```

If chart generation fails due to bad data, the error should identify the chart:

```text
ReportingError: failed to create market_path.png because column 'underlying_price' was missing.
```

### Demo path for a reviewer

Reviewer runs:

```bash
python -m pyrisklab run --config configs/demo.yaml --overwrite
```

Reviewer opens:

```text
results/demo_run/summary_report.md
```

Then checks:

```text
results/demo_run/market_path.png
results/demo_run/option_price.png
results/demo_run/portfolio_value.png
results/demo_run/drawdown.png
```

The reviewer should understand the project outputs quickly without needing a dashboard.

---

## 3. UX/UI Requirements

### Screens/pages

This project is local-first, so Reporting uses file-based UX instead of app screens.

Main surfaces:

1. CLI progress messages
2. Results folder
3. CSV tables
4. PNG charts
5. Markdown summary report

### Components

#### CLI progress messages

Recommended messages:

```text
[9/12] Saving CSV outputs...
[9/12] Creating charts...
[9/12] Writing summary report...
```

or one simpler message:

```text
Generating local reports...
```

Final success message:

```text
Done. Results saved to results/demo_run/
```

#### Results folder

Required structure:

```text
results/<run_name>/
```

For the demo config:

```text
results/demo_run/
```

#### CSV outputs

Minimum expected CSV files after Feature 9:

```text
market_path.csv
pricing_history.csv
greeks_history.csv
signals.csv
orders.csv
trades.csv
portfolio_history.csv
risk_events.csv
```

[Decision] Reporting should save whatever has been produced by earlier pipeline steps, but the full demo should produce all of these.

#### PNG charts

Recommended charts:

```text
market_path.png
option_price.png
greeks.png
portfolio_value.png
drawdown.png
```

Chart requirements:

- Clear title
- Labeled x-axis
- Labeled y-axis
- Readable size
- Saved as PNG
- No unnecessary styling complexity

#### Markdown summary report

Required file:

```text
summary_report.md
```

Recommended sections:

```markdown
# PyRiskLab Run Summary

## Run Configuration
## Market Simulation
## Option Pricing
## Greeks
## Strategy Signals
## Fake Execution
## Portfolio Results
## Risk Events
## Generated Artifacts
## Limitations
```

### Forms/inputs

No forms are needed.

Inputs come from:

- `RunConfig`
- DataFrames from earlier features
- Lists of model objects if not converted yet
- Output directory path
- Original config path

### Buttons/actions

No buttons are needed.

Main commands:

```bash
python -m pyrisklab run --config configs/demo.yaml
python -m pyrisklab run --config configs/demo.yaml --overwrite
```

### Validation messages

Reporting should validate required columns before creating charts.

Examples:

```text
ReportingError: market_path DataFrame must include 'step' and 'underlying_price'.
ReportingError: pricing_history DataFrame must include 'step' and 'option_price'.
ReportingError: portfolio_history DataFrame must include 'step' and 'total_value'.
```

### Empty states

Required empty states:

- Empty trades
- Empty risk events
- Empty signals
- Empty orders

These should not crash the report.

Empty CSVs should still be written with headers.

The summary report should explain empty sections plainly.

### Loading states

CLI progress messages are enough.

No spinner or dashboard loading state is required.

### Error states

Expected errors should use `ReportingError`.

The CLI should catch the error and print a readable message.

### Responsive behavior if relevant

Not relevant for MVP.

Do not add responsive dashboard behavior in this feature.

---

## 4. Data Requirements

### Entities involved

Input entities/data:

- `RunConfig`
- Market path DataFrame
- Pricing history DataFrame
- Greeks history DataFrame
- Signals DataFrame or list
- Orders DataFrame or list
- Trades DataFrame or list
- Portfolio history DataFrame
- Risk events DataFrame or list

Output artifacts:

- CSV files
- PNG charts
- Markdown report
- Copied config

### Fields

#### market_path.csv

Required columns:

```text
step
time_years
underlying_price
```

Optional:

```text
path_id
```

#### pricing_history.csv

Required columns:

```text
step
underlying_price
time_to_expiry
option_type
strike
option_price
```

#### greeks_history.csv

Required columns:

```text
step
delta
gamma
vega
theta
rho
```

Recommended also:

```text
underlying_price
time_to_expiry
option_price
```

#### signals.csv

Required columns:

```text
step
symbol
action
reason
```

Optional:

```text
delta
option_price
```

#### orders.csv

Required columns:

```text
step
symbol
side
quantity
order_type
requested_price
status
reason
```

#### trades.csv

Required columns:

```text
step
symbol
side
quantity
fill_price
commission
notional
```

#### portfolio_history.csv

Required columns:

```text
step
cash
position_quantity
average_cost
market_price
positions_value
realized_pnl
unrealized_pnl
total_value
peak_value
drawdown
drawdown_pct
```

#### risk_events.csv

Required columns:

```text
step
event_type
severity
symbol
proposed_side
proposed_quantity
proposed_notional
portfolio_value
limit_name
limit_value
observed_value
reason
```

### Relationships

- One run creates one results folder.
- One results folder contains all output artifacts for that run.
- Each CSV corresponds to one pipeline stage.
- Charts are generated from specific CSV/DataFrame outputs.
- `summary_report.md` summarizes all outputs.

### Example seed data

Example config:

```yaml
run_name: demo_run
seed: 42
output_dir: results
```

Example output folder:

```text
results/demo_run/
```

Example report excerpt:

```markdown
# PyRiskLab Run Summary

Run name: demo_run  
Seed: 42  
Output directory: results/demo_run/

## Portfolio Results

Starting cash: $10,000.00  
Final portfolio value: $10,245.30  
Max drawdown: 3.20%

## Risk Events

No risk events were triggered in this run.
```

### Local persistence needs

Use local files only.

Do not use:

- Database
- Cloud storage
- Hosted report server
- External analytics service

Justification:

- The project is local-first.
- CSV/PNG/Markdown are easy to inspect.
- GitHub reviewers can understand artifacts quickly.
- File outputs are simpler and more reproducible than a database for MVP.

---

## 5. Logic Requirements

### Business rules

#### Results folder creation

- Use `output_dir` and `run_name` from config.
- Default path should be:

```text
results/<run_name>/
```

- If the folder exists and `--overwrite` is false, raise `RunError` or `ReportingError`.
- If `--overwrite` is true, safely delete/recreate only that run folder.
- Never delete the entire `results/` folder.

#### Config copy

Copy the config used for the run into:

```text
config_used.yaml
```

This proves reproducibility.

#### CSV writing

- Every CSV should have clear column names.
- Empty valid outputs should still produce CSV headers.
- Do not silently skip expected outputs.

#### Chart generation

Charts should be deterministic and saved as PNG.

Recommended chart functions:

- Market path line chart
- Option price line chart
- Greeks chart
- Portfolio value line chart
- Drawdown line chart

[Decision] Keep charts simple. Do not over-style them.

#### Summary report generation

The Markdown report should include:

- Run name
- Seed
- Major config values
- Number of steps
- Initial/final underlying price
- Initial/final option price
- Number of signals
- Number of orders
- Number of trades
- Final portfolio value
- Max drawdown
- Number of risk events
- List of generated artifacts
- Limitations

#### Limitations section

Every summary report should state:

```text
This is a local simulation only. It does not use live market data, place real trades, connect to a brokerage, or provide investment advice.
```

### Calculations

Reporting may compute summary values from existing DataFrames:

- Initial underlying price
- Final underlying price
- Minimum/maximum underlying price
- Initial option price
- Final option price
- Number of signals
- Number of orders
- Number of trades
- Final cash
- Final portfolio value
- Max drawdown
- Number of risk events

Reporting should not recalculate pricing, Greeks, risk, or portfolio accounting.

### API/service functions if needed

Recommended functions in `reporting.py`:

```python
def prepare_output_dir(output_dir: Path, run_name: str, overwrite: bool = False) -> Path:
    ...

def save_config_copy(config_path: Path, run_dir: Path) -> Path:
    ...

def save_csv_outputs(run_dir: Path, outputs: dict[str, pd.DataFrame]) -> list[Path]:
    ...

def plot_market_path(market_path: pd.DataFrame, run_dir: Path) -> Path:
    ...

def plot_option_price(pricing_history: pd.DataFrame, run_dir: Path) -> Path:
    ...

def plot_greeks(greeks_history: pd.DataFrame, run_dir: Path) -> Path:
    ...

def plot_portfolio_value(portfolio_history: pd.DataFrame, run_dir: Path) -> Path:
    ...

def plot_drawdown(portfolio_history: pd.DataFrame, run_dir: Path) -> Path:
    ...

def write_summary_report(run_dir: Path, config: RunConfig, outputs: dict[str, pd.DataFrame]) -> Path:
    ...
```

Optional wrapper:

```python
def generate_reports(
    run_dir: Path,
    config: RunConfig,
    config_path: Path,
    outputs: dict[str, pd.DataFrame],
) -> list[Path]:
    ...
```

### State management

Reporting should be mostly stateless.

It should receive data and write files.

Do not make reporting own simulation state, portfolio state, strategy decisions, or risk rules.

### Edge cases

#### Results folder already exists

Raise clear error unless `--overwrite` is true.

#### Empty trades

Write empty `trades.csv` with headers and report “No trades were executed.”

#### Empty risk events

Write empty `risk_events.csv` with headers and report “No risk events were triggered.”

#### Missing optional outputs

If a feature is not built yet, reporting can skip optional files only during development.

For final MVP, missing expected outputs should fail clearly.

#### Missing required columns

Raise `ReportingError`.

#### matplotlib backend issues

Use normal file-saving with `plt.savefig(...)`.

Close figures after saving to avoid memory leaks:

```python
plt.close()
```

#### Very long reports

Keep summary report readable. Do not dump entire CSV content into Markdown.

---

## 6. Acceptance Criteria

### AC1: Results folder is created

Given a valid run config  
When the user runs the CLI  
Then `results/<run_name>/` is created.

### AC2: Existing folder is protected

Given `results/demo_run/` already exists  
And `--overwrite` is not used  
When the user runs the CLI  
Then the system raises a clear error telling the user to use `--overwrite` or change `run_name`.

### AC3: Overwrite works safely

Given `results/demo_run/` already exists  
And `--overwrite` is used  
When the user runs the CLI  
Then only `results/demo_run/` is recreated  
And the app does not delete unrelated result folders.

### AC4: Config copy is saved

Given a successful run  
When reporting completes  
Then `config_used.yaml` exists in the run folder.

### AC5: CSV outputs are saved

Given successful pipeline outputs  
When reporting completes  
Then all expected CSV files are saved in the run folder.

### AC6: Charts are saved

Given valid market, pricing, Greeks, and portfolio data  
When reporting completes  
Then PNG charts are saved with readable titles and axis labels.

### AC7: Summary report is generated

Given a successful run  
When reporting completes  
Then `summary_report.md` is created  
And it includes run settings, key metrics, generated artifacts, and limitations.

### AC8: Empty trades do not crash reporting

Given no trades were executed  
When reporting runs  
Then `trades.csv` is still saved  
And `summary_report.md` says no trades were executed.

### AC9: Empty risk events do not crash reporting

Given no risk events were triggered  
When reporting runs  
Then `risk_events.csv` is still saved  
And `summary_report.md` says no risk events were triggered.

### AC10: Missing required chart columns fail clearly

Given `portfolio_history` is missing `total_value`  
When reporting tries to create `portfolio_value.png`  
Then a `ReportingError` is raised  
And the message names the missing column.

---

## 7. Test Plan

### Unit tests

Create:

```text
tests/test_reporting.py
```

Recommended tests:

1. `test_prepare_output_dir_creates_run_folder`
2. `test_prepare_output_dir_blocks_existing_folder_without_overwrite`
3. `test_prepare_output_dir_overwrites_only_target_run_folder`
4. `test_save_config_copy_creates_config_used_yaml`
5. `test_save_csv_outputs_writes_expected_files`
6. `test_empty_trades_csv_is_written_with_headers`
7. `test_empty_risk_events_csv_is_written_with_headers`
8. `test_market_path_chart_is_saved`
9. `test_option_price_chart_is_saved`
10. `test_greeks_chart_is_saved`
11. `test_portfolio_value_chart_is_saved`
12. `test_drawdown_chart_is_saved`
13. `test_summary_report_contains_limitations`
14. `test_missing_required_chart_column_raises_reporting_error`

### Integration tests if useful

Create:

```text
tests/test_pipeline_reporting_integration.py
```

Recommended integration test:

- Run the pipeline with a tiny deterministic config.
- Confirm the run folder exists.
- Confirm required CSV, PNG, and Markdown files exist.
- Confirm `summary_report.md` contains the run name and limitations.

### Manual QA checklist

- [ ] Run `python -m pyrisklab run --config configs/demo.yaml --overwrite`.
- [ ] Confirm `results/demo_run/` exists.
- [ ] Confirm CSV files are readable.
- [ ] Confirm PNG files open correctly.
- [ ] Confirm `summary_report.md` opens on GitHub/VS Code preview.
- [ ] Confirm no-trade runs still produce report files.
- [ ] Confirm no-risk-event runs still produce report files.
- [ ] Confirm existing folder error is clear without `--overwrite`.
- [ ] Confirm `--overwrite` does not delete unrelated run folders.
- [ ] Confirm limitations section says simulation only.

### Demo verification checklist

- [ ] Reviewer can run one command and get a results folder.
- [ ] Reviewer can open `summary_report.md`.
- [ ] Reviewer can inspect charts without running a dashboard.
- [ ] Reviewer can inspect CSVs directly.
- [ ] README later points to example report artifacts.
- [ ] Generated outputs look professional enough for screenshots.

---

## 8. Portfolio Value

### How this feature helps the project stand out

Reporting makes PyRiskLab visible. Without reporting, the project is just code. With reporting, the project becomes a complete local tool that produces evidence of its work.

This helps the project stand out because it shows:

- One command produces outputs
- Results are organized
- The project is reproducible
- The output is easy to inspect
- The project can be reviewed quickly on GitHub
- The user understands portfolio presentation, not just coding

### What to mention in README

Mention:

```text
Each PyRiskLab run generates a local results folder containing CSV tables, PNG charts, the exact config used, and a Markdown summary report.
```

Also mention:

```text
The generated report is designed to be readable without a dashboard or external service.
```

And include the limitations:

```text
PyRiskLab is a simulation-only project. It does not use live market data, execute real trades, connect to brokerages, or provide investment advice.
```

### What to mention in interviews

Strong interview points:

- “I designed reporting as a separate module so the simulation logic does not directly handle charting and file output.”
- “The run folder contains the config used, which makes outputs reproducible.”
- “I handled empty trades and empty risk events so valid no-action runs still produce complete reports.”
- “I chose CSV, PNG, and Markdown because they are easy for reviewers to inspect locally.”
- “I avoided a dashboard for MVP because the goal was a clean local Python engineering tool.”

---

## 9. Implementation Notes For Codex

### Likely files/folders

Primary files:

```text
src/pyrisklab/reporting.py
tests/test_reporting.py
```

Related files:

```text
src/pyrisklab/pipeline.py
src/pyrisklab/config.py
src/pyrisklab/exceptions.py
src/pyrisklab/models.py
configs/demo.yaml
results/.gitkeep
```

Generated files:

```text
results/<run_name>/config_used.yaml
results/<run_name>/market_path.csv
results/<run_name>/pricing_history.csv
results/<run_name>/greeks_history.csv
results/<run_name>/signals.csv
results/<run_name>/orders.csv
results/<run_name>/trades.csv
results/<run_name>/portfolio_history.csv
results/<run_name>/risk_events.csv
results/<run_name>/market_path.png
results/<run_name>/option_price.png
results/<run_name>/greeks.png
results/<run_name>/portfolio_value.png
results/<run_name>/drawdown.png
results/<run_name>/summary_report.md
```

### Suggested exception

In `exceptions.py`:

```python
class ReportingError(PyRiskLabError):
    """Raised when report generation or artifact writing fails."""
```

### Build order

1. Add or confirm `ReportingError`.
2. Implement `prepare_output_dir(...)`.
3. Implement safe overwrite behavior.
4. Implement `save_config_copy(...)`.
5. Implement CSV export helper.
6. Implement empty DataFrame support with headers.
7. Implement market path chart.
8. Implement option price chart.
9. Implement Greeks chart.
10. Implement portfolio value chart.
11. Implement drawdown chart.
12. Implement `write_summary_report(...)`.
13. Connect reporting to `pipeline.py`.
14. Add tests.
15. Run full demo and inspect `results/demo_run/`.

### Risks

#### Risk 1: Reporting becomes mixed with simulation logic

Do not calculate market paths, prices, Greeks, trades, portfolio state, or risk events inside `reporting.py`.

Reporting should only format and save outputs.

#### Risk 2: Outputs become scattered

All run-specific outputs must go under:

```text
results/<run_name>/
```

Do not write random files into the repo root.

#### Risk 3: Empty states crash

Empty trades and empty risk events are valid and must not crash report generation.

#### Risk 4: Charts look unprofessional

Charts should have clear titles, axis labels, and readable sizing.

Do not over-style. Simple and readable is better.

#### Risk 5: Overbuilding into dashboard scope

Do not add Streamlit, Plotly, web UI, database, cloud report hosting, or login.

### What not to change

Do not change:

- CLI command format
- Config schema beyond output/reporting fields
- Market simulation logic
- Pricing formulas
- Greeks formulas
- Strategy rules
- Fake execution logic
- Portfolio accounting logic
- Risk rules

This feature should only add local artifact generation and reporting.

---

## Move-On Checklist

- [ ] `results/<run_name>/` is created.
- [ ] Existing folder behavior is safe.
- [ ] `config_used.yaml` is copied.
- [ ] All expected CSV files are saved.
- [ ] Empty trades and risk events are handled.
- [ ] PNG charts are created.
- [ ] `summary_report.md` is generated.
- [ ] Report includes limitations and simulation-only disclaimer.
- [ ] Reporting tests pass.
- [ ] Feature does not add dashboard, database, cloud, live market data, broker APIs, SaaS systems, or real trading.
