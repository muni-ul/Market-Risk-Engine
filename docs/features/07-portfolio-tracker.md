# Feature 7: Portfolio Tracker

## Output Path

`docs/features/07-portfolio-tracker.md`

---

## 1. Feature Overview

### Feature name

**Portfolio Tracker**

### One-sentence description

Track simulated portfolio state over time by applying fake trades to cash, positions, portfolio value, P&L, and drawdown.

### Detailed description

The Portfolio Tracker is the state-management layer of PyRiskLab. It receives deterministic fake trades from the Fake Execution feature and converts them into a time-series view of the simulated portfolio.

This feature should track:

- Starting cash
- Cash after each trade
- Position quantity
- Average cost
- Market value of open positions
- Realized P&L
- Unrealized P&L
- Total portfolio value
- Peak portfolio value
- Drawdown

The feature does **not** decide whether a trade should happen. It does **not** generate strategy signals. It does **not** enforce risk rules. Its job is to accurately update portfolio state after fake trades and produce clean portfolio history outputs.

### Why it matters

This feature makes the project feel like a real software system instead of only a pricing calculator. Pricing and Greeks are mostly mathematical functions, but portfolio tracking introduces persistent state, accounting logic, edge cases, and testable business rules.

That is valuable for a portfolio project because it shows the ability to design and test state transitions, not just formulas.

### Skill it demonstrates

- Python dataclasses or typed models
- Stateful system design
- Portfolio/accounting logic
- DataFrame generation with pandas
- Edge-case handling
- Test-driven correctness checks
- Clear separation between execution, portfolio, and risk modules

### Priority

**High**

This is a core feature because the project needs a portfolio history to make fake execution, risk controls, reporting, and demo outputs meaningful.

### Complexity

**Medium to High**

The basic version is manageable, but details like average cost, realized P&L, drawdown, empty trades, and sell validation can become error-prone if not carefully tested.

---

## 2. User/Demo Flow

### Happy path

1. User runs:

```bash
python -m pyrisklab run --config configs/demo.yaml
```

2. The config loader reads starting cash from the config.
3. Market simulation creates a synthetic price path.
4. Pricing and Greeks features create option-price history.
5. Simple fake strategy creates signals.
6. Fake execution creates simulated trades.
7. Portfolio Tracker applies each trade in chronological order.
8. Portfolio Tracker marks open positions to market at each step.
9. Portfolio Tracker saves:

```text
results/demo_run/portfolio_history.csv
```

10. Later Reporting uses this file to create portfolio charts and summary statistics.

### First-time path

For a first-time demo run, the user should not need to manually create portfolio files. The portfolio should start from `risk.starting_cash` or a clearly named config value.

Recommended config source:

```yaml
risk:
  starting_cash: 10000.0
```

[Decision] Reusing `risk.starting_cash` is acceptable because starting cash is used by both portfolio and risk checks.

[Open Question] If later architecture separates portfolio config from risk config, decide whether this should move to:

```yaml
portfolio:
  starting_cash: 10000.0
```

For MVP, keep it simple and avoid adding unnecessary config sections unless needed.

### Empty state

If no trades are generated, the portfolio should still produce a valid history.

Expected behavior:

- Cash remains equal to starting cash.
- Position quantity remains zero.
- Positions value remains zero.
- Total value remains equal to starting cash.
- Realized P&L remains zero.
- Unrealized P&L remains zero.
- Drawdown remains zero.

The output file should still be created:

```text
portfolio_history.csv
```

The report can later say:

```text
No trades were executed in this run. Portfolio value remained at starting cash.
```

### Error path

The portfolio should raise clear errors for invalid state transitions, such as:

- Selling more contracts than currently held, unless shorting is explicitly enabled.
- Applying a trade with zero or negative quantity.
- Applying a trade with negative fill price.
- Buying when there is not enough cash, unless margin is explicitly allowed.
- Receiving trades out of chronological order if the implementation requires sorted trades.
- Receiving a trade for an unknown symbol with no matching price history.

Example error messages:

```text
PortfolioError: cannot sell 3 CALL_105 contracts when current position is 1.
PortfolioError: trade quantity must be greater than 0. Received 0.
PortfolioError: insufficient cash for BUY order. Required 1240.00, available 900.00.
```

### Demo path for a reviewer

Reviewer runs:

```bash
pytest tests/test_portfolio.py
python -m pyrisklab run --config configs/demo.yaml --overwrite
```

Reviewer opens:

```text
results/demo_run/portfolio_history.csv
```

They should see a clean step-by-step portfolio table showing how fake trades affected cash, position value, total portfolio value, and drawdown.

---

## 3. UX/UI Requirements

### Screens/pages

This is a local CLI project, so there are no traditional screens.

The user-facing surfaces are:

1. CLI progress messages
2. Generated `portfolio_history.csv`
3. Generated summary report section in a later Reporting feature
4. Portfolio charts in a later Reporting feature

### Components

#### CLI progress message

The pipeline should include a progress message similar to:

```text
[7/12] Updating portfolio history...
```

or:

```text
Tracking portfolio value and drawdown...
```

#### Portfolio history CSV

Required output:

```text
results/<run_name>/portfolio_history.csv
```

Recommended columns:

| Column | Description |
|---|---|
| `step` | Simulation step |
| `cash` | Cash balance after applying trades at this step |
| `position_quantity` | Current quantity held |
| `average_cost` | Average cost per contract |
| `market_price` | Current option market price |
| `positions_value` | Current market value of open positions |
| `realized_pnl` | Profit/loss from closed trades |
| `unrealized_pnl` | Profit/loss on open position |
| `total_value` | Cash plus positions value |
| `peak_value` | Highest total value reached so far |
| `drawdown` | Dollar drawdown from peak |
| `drawdown_pct` | Percentage drawdown from peak |

### Forms/inputs

No direct form is needed.

Inputs come from:

- `trades.csv` or in-memory `Trade` objects
- Pricing history DataFrame
- Starting cash from config
- Optional commission from execution config if implemented

### Buttons/actions

No buttons are needed for MVP.

CLI actions involved:

```bash
python -m pyrisklab run --config configs/demo.yaml
python -m pyrisklab run --config configs/demo.yaml --overwrite
```

### Validation messages

Recommended validation messages:

```text
PortfolioError: starting_cash must be greater than 0. Received -1000.
PortfolioError: cannot apply trade with negative fill_price. Received -2.50.
PortfolioError: cannot sell more than current position unless shorting is enabled.
PortfolioError: missing market price for symbol CALL_105 at step 87.
```

### Empty states

Empty trades should not crash the portfolio tracker.

Expected empty-state output:

```text
No trades were executed. Portfolio history was generated using starting cash only.
```

The CSV should still have one row per market/pricing step.

### Loading states

CLI progress is enough:

```text
Updating portfolio history...
Saved portfolio_history.csv
```

### Error states

For expected user/data errors, raise `PortfolioError` and let `cli.py` display a clean message without a giant stack trace.

For programmer errors, pytest should expose them during development.

### Responsive behavior if relevant

Not relevant for MVP.

[Decision] Do not add dashboard-specific responsive design to this feature.

---

## 4. Data Requirements

### Entities involved

#### Input entities

- `RunConfig`
- `Trade`
- `PricingRecord`
- `OptionContract`

#### Main portfolio entities

- `Portfolio`
- `Position`
- `PortfolioSnapshot`

#### Output entities

- `portfolio_history.csv`
- In-memory list of `PortfolioSnapshot` objects

### Fields

#### Portfolio

Recommended fields:

```python
Portfolio:
  starting_cash: float
  cash: float
  positions: dict[str, Position]
  realized_pnl: float
  peak_value: float
  snapshots: list[PortfolioSnapshot]
  allow_short: bool = False
```

#### Position

Recommended fields:

```python
Position:
  symbol: str
  quantity: int
  average_cost: float
```

Optional fields if useful:

```python
market_price: float
market_value: float
unrealized_pnl: float
```

[Decision] Keep `Position` small and compute market-value fields during snapshot creation.

#### PortfolioSnapshot

Recommended fields:

```python
PortfolioSnapshot:
  step: int
  cash: float
  symbol: str
  position_quantity: int
  average_cost: float
  market_price: float
  positions_value: float
  realized_pnl: float
  unrealized_pnl: float
  total_value: float
  peak_value: float
  drawdown: float
  drawdown_pct: float
```

[Open Question] If multiple option contracts are added later, decide whether snapshots should have one row per step or one row per step per symbol. For MVP, one option contract is enough.

### Relationships

- One run has one portfolio.
- One portfolio has zero or more positions.
- One position belongs to one symbol.
- One trade updates one portfolio.
- One pricing record provides the current market price for marking positions.
- One portfolio produces many portfolio snapshots.
- Reporting later reads `portfolio_history.csv`.

### Example seed data

#### Starting cash

```yaml
risk:
  starting_cash: 10000.0
```

#### Example trade input

```csv
step,symbol,side,quantity,fill_price,commission,notional
12,CALL_105,BUY,1,4.50,0.00,450.00
43,CALL_105,SELL,1,7.25,0.00,725.00
```

[Decision] Option contracts should use a contract multiplier of `100` if modeling option contract notional realistically.

[Open Question] Decide whether MVP uses contract multiplier `100` or simplified multiplier `1`.

Recommended MVP decision:

```yaml
execution:
  contract_multiplier: 100
```

Justification:

- Real options contracts commonly use a 100-share multiplier.
- It makes notional and cash movement more realistic.
- It gives better interview discussion.
- It should be kept simple and config-driven.

If using multiplier `100`, then:

```text
notional = fill_price * quantity * contract_multiplier
```

### Local persistence needs

Required output:

```text
results/<run_name>/portfolio_history.csv
```

Optional later output:

```text
results/<run_name>/positions_final.csv
```

[Decision] Do not use a database.

Justification:

- Portfolio history is generated per run.
- CSV is easy to inspect.
- pandas works naturally with CSV.
- A database adds unnecessary complexity for MVP.

---

## 5. Logic Requirements

### Business rules

#### Starting cash

- Starting cash must be greater than zero.
- Portfolio begins with cash equal to starting cash.
- Portfolio begins with no positions.

#### Buy trade

When applying a buy trade:

- Quantity must be positive.
- Fill price must be nonnegative.
- Notional should be calculated as:

```text
fill_price * quantity * contract_multiplier
```

- Total cash impact should be:

```text
notional + commission
```

- Cash decreases by total cash impact.
- Position quantity increases.
- Average cost updates using weighted average cost.

Weighted average cost:

```text
new_average_cost =
  ((old_quantity * old_average_cost) + (buy_quantity * fill_price))
  / (old_quantity + buy_quantity)
```

#### Sell trade

When applying a sell trade:

- Quantity must be positive.
- Fill price must be nonnegative.
- If shorting is disabled, sell quantity cannot exceed current position quantity.
- Cash increases by:

```text
notional - commission
```

- Position quantity decreases.
- Realized P&L updates based on average cost:

```text
realized_pnl += (fill_price - average_cost) * quantity * contract_multiplier - commission
```

- If quantity becomes zero, average cost should reset to `0.0`.

#### Mark-to-market

At each step, the portfolio should calculate:

```text
positions_value = position_quantity * market_price * contract_multiplier
total_value = cash + positions_value
unrealized_pnl = (market_price - average_cost) * position_quantity * contract_multiplier
```

If there is no open position:

```text
positions_value = 0
unrealized_pnl = 0
average_cost = 0
```

#### Drawdown

Track peak total value:

```text
peak_value = max(previous_peak_value, total_value)
drawdown = peak_value - total_value
drawdown_pct = drawdown / peak_value
```

If `peak_value <= 0`, `drawdown_pct` should be `0` to avoid division by zero.

### Calculations

Required calculations:

- Cash balance
- Position quantity
- Average cost
- Position market value
- Realized P&L
- Unrealized P&L
- Total value
- Peak value
- Drawdown
- Drawdown percentage

### API/service functions if needed

Recommended functions/classes:

```python
class Portfolio:
    def __init__(self, starting_cash: float, contract_multiplier: int = 100, allow_short: bool = False) -> None:
        ...

    def apply_trade(self, trade: Trade) -> None:
        ...

    def mark_to_market(self, step: int, symbol: str, market_price: float) -> PortfolioSnapshot:
        ...

    def to_history_frame(self) -> pd.DataFrame:
        ...
```

Recommended pipeline function:

```python
def build_portfolio_history(
    trades: list[Trade],
    pricing_history: pd.DataFrame,
    starting_cash: float,
    contract_multiplier: int = 100,
) -> pd.DataFrame:
    ...
```

### State management

State should live inside the `Portfolio` object.

Do not use:

- Module-level global cash variables
- Hidden mutable dictionaries passed around loosely
- Direct edits to portfolio CSV files during calculations

[Decision] The portfolio should be updated in memory first, then exported once.

### Edge cases

#### No trades

Should still create a full portfolio history with starting cash.

#### Buy without enough cash

Recommended MVP behavior:

- Raise `PortfolioError`.

Alternative:

- Let Risk Manager block the trade before portfolio sees it.

[Decision] Portfolio should still protect itself even if Risk Manager misses something.

#### Sell without position

Raise `PortfolioError` if `allow_short=False`.

#### Same-step multiple trades

Recommended behavior:

- Apply all trades at that step before taking the snapshot for that step.

[Open Question] If same-step trades include both buy and sell for the same symbol, decide order. Recommended MVP: preserve original trade order from execution.

#### Missing price at a trade step

Raise `PortfolioError`.

#### Market price missing for non-trade step

If a snapshot is required for every step, missing prices should fail clearly.

#### Negative or zero market price

- Negative market price should fail.
- Zero option price can be valid near expiry or deep out-of-the-money.

#### Floating-point rounding

- Internal calculations can use floats.
- CSV outputs should be rounded only when saving/reporting, not during internal calculations.

---

## 6. Acceptance Criteria

### AC1: Portfolio initializes correctly

Given a valid starting cash value  
When the portfolio is created  
Then cash equals starting cash  
And there are no open positions  
And realized P&L equals zero.

### AC2: Buy trade updates cash and position

Given a portfolio with starting cash of `10000`  
And contract multiplier `100`  
When a buy trade for `1` contract at price `5.00` is applied  
Then cash decreases by `500` plus commission  
And position quantity increases to `1`  
And average cost equals `5.00`.

### AC3: Sell trade updates cash and realized P&L

Given a portfolio holding `1` contract with average cost `5.00`  
When a sell trade for `1` contract at price `7.00` is applied  
Then cash increases by `700` minus commission  
And position quantity becomes `0`  
And realized P&L increases by `200` minus commission.

### AC4: Cannot sell more than held

Given shorting is disabled  
And the portfolio holds `1` contract  
When a sell trade for `2` contracts is applied  
Then the system raises a `PortfolioError`  
And the error explains that the sell quantity exceeds the current position.

### AC5: Portfolio history is generated with no trades

Given no trades are executed  
When portfolio history is built  
Then `portfolio_history.csv` is still created  
And total value remains equal to starting cash  
And drawdown remains zero.

### AC6: Mark-to-market updates unrealized P&L

Given the portfolio holds `1` contract with average cost `5.00`  
And the current market price is `6.50`  
When the portfolio is marked to market  
Then positions value equals `650` with multiplier `100`  
And unrealized P&L equals `150`.

### AC7: Drawdown updates correctly

Given total portfolio value reaches a peak of `10500`  
When later total portfolio value falls to `10000`  
Then drawdown equals `500`  
And drawdown percentage equals approximately `0.0476`.

### AC8: Portfolio history saves required columns

Given a completed run  
When the portfolio history file is saved  
Then `portfolio_history.csv` includes `step`, `cash`, `position_quantity`, `average_cost`, `market_price`, `positions_value`, `realized_pnl`, `unrealized_pnl`, `total_value`, `peak_value`, `drawdown`, and `drawdown_pct`.

---

## 7. Test Plan

### Unit tests

Create:

```text
tests/test_portfolio.py
```

Recommended tests:

1. `test_portfolio_initializes_with_starting_cash`
2. `test_buy_trade_decreases_cash_and_increases_position`
3. `test_buy_trade_updates_weighted_average_cost`
4. `test_sell_trade_increases_cash_and_reduces_position`
5. `test_sell_trade_updates_realized_pnl`
6. `test_cannot_sell_more_than_held_when_shorting_disabled`
7. `test_zero_quantity_trade_fails`
8. `test_negative_quantity_trade_fails`
9. `test_negative_fill_price_fails`
10. `test_insufficient_cash_for_buy_fails`
11. `test_mark_to_market_calculates_positions_value`
12. `test_mark_to_market_calculates_unrealized_pnl`
13. `test_drawdown_updates_from_peak`
14. `test_empty_trades_generate_flat_portfolio_history`
15. `test_portfolio_history_has_required_columns`

### Integration tests if useful

Recommended integration test:

```text
tests/test_pipeline_portfolio_integration.py
```

Test:

- Run a small deterministic pipeline with a tiny pricing history and a small trade list.
- Confirm `portfolio_history.csv` is created.
- Confirm final total value matches expected calculation.
- Confirm no risk logic is required for the portfolio tracker to work.

### Manual QA checklist

- [ ] Run the demo config.
- [ ] Confirm `portfolio_history.csv` is created.
- [ ] Open the CSV and confirm column names are readable.
- [ ] Confirm starting cash appears correctly at step 0.
- [ ] Confirm buy trades reduce cash.
- [ ] Confirm sell trades increase cash.
- [ ] Confirm open positions are marked to market.
- [ ] Confirm no-trade runs still create portfolio history.
- [ ] Confirm invalid sell quantity gives a clear error.
- [ ] Confirm drawdown is not negative.
- [ ] Confirm total value equals cash plus positions value.

### Demo verification checklist

- [ ] Reviewer can run `pytest tests/test_portfolio.py`.
- [ ] Reviewer can run the full demo command.
- [ ] `results/demo_run/portfolio_history.csv` exists.
- [ ] The portfolio history shows clear state changes after trades.
- [ ] README later explains that portfolio is simulated only.
- [ ] Portfolio values do not imply real trading performance.

---

## 8. Portfolio Value

### How this feature helps the project stand out

The Portfolio Tracker turns PyRiskLab from a formula project into a stateful simulation system. Recruiters may not understand option pricing deeply, but they can understand a system that tracks cash, positions, account value, and drawdown over time.

This feature shows that the project has real software-engineering depth:

- State transitions
- Accounting logic
- Edge cases
- Testable business rules
- Clean outputs
- Separation of concerns

### What to mention in README

Mention:

```text
The portfolio tracker applies simulated trades to a local portfolio model, updating cash, open positions, realized/unrealized P&L, total value, and drawdown across the synthetic market path.
```

Also mention:

```text
This is simulated portfolio accounting only. PyRiskLab does not connect to a brokerage, place real trades, or provide investment advice.
```

### What to mention in interviews

Strong interview points:

- “I separated fake execution from portfolio tracking so fills and accounting are not mixed together.”
- “The portfolio state is explicit in a Portfolio object instead of hidden in global variables.”
- “I tested buy/sell transitions, average cost, insufficient cash, and selling more than held.”
- “The portfolio history is generated at every simulation step, which makes the report and risk manager easier to build.”
- “This feature helped me practice stateful software design, not just numerical formulas.”

---

## 9. Implementation Notes For Codex

### Likely files/folders

Primary files:

```text
src/pyrisklab/portfolio.py
tests/test_portfolio.py
```

Related files:

```text
src/pyrisklab/models.py
src/pyrisklab/exceptions.py
src/pyrisklab/pipeline.py
src/pyrisklab/reporting.py
configs/demo.yaml
```

Generated output:

```text
results/<run_name>/portfolio_history.csv
```

### Suggested models

Add or confirm these dataclasses in `models.py`:

```python
@dataclass(frozen=True)
class Trade:
    step: int
    symbol: str
    side: Literal["BUY", "SELL"]
    quantity: int
    fill_price: float
    commission: float
    notional: float
```

```python
@dataclass
class Position:
    symbol: str
    quantity: int = 0
    average_cost: float = 0.0
```

```python
@dataclass(frozen=True)
class PortfolioSnapshot:
    step: int
    cash: float
    symbol: str
    position_quantity: int
    average_cost: float
    market_price: float
    positions_value: float
    realized_pnl: float
    unrealized_pnl: float
    total_value: float
    peak_value: float
    drawdown: float
    drawdown_pct: float
```

### Suggested exception

In `exceptions.py`:

```python
class PortfolioError(PyRiskLabError):
    """Raised when portfolio state cannot be updated safely."""
```

### Build order

1. Add or confirm `PortfolioError`.
2. Add `Position` and `PortfolioSnapshot` models.
3. Implement `Portfolio.__init__`.
4. Implement buy trade handling.
5. Implement sell trade handling.
6. Implement mark-to-market snapshot creation.
7. Implement drawdown tracking.
8. Implement `build_portfolio_history(...)`.
9. Export portfolio history through the pipeline/reporting layer.
10. Add unit tests.
11. Run `pytest tests/test_portfolio.py`.
12. Run full demo command and inspect CSV.

### Risks

#### Risk 1: Mixing execution and portfolio logic

Do not make portfolio responsible for creating trades. Fake Execution creates trades. Portfolio only applies them.

#### Risk 2: Letting risk logic leak into portfolio

Risk Manager will decide whether a trade should be blocked. Portfolio should still validate impossible state transitions, but it should not own risk-limit policy.

#### Risk 3: Confusing contract multiplier

Use one clear multiplier source. Recommended:

```yaml
execution:
  contract_multiplier: 100
```

Do not hardcode multiplier in multiple modules.

#### Risk 4: Incorrect average cost after partial sells

Partial sells should not change average cost of the remaining position. Average cost resets only when position quantity becomes zero.

#### Risk 5: No-trade case crashes

No-trade runs are valid and should still produce portfolio history.

### What not to change

Do not change:

- CLI command structure
- Market simulation logic
- Black-Scholes pricing formulas
- Greeks formulas
- Strategy signal rules
- Fake execution fill logic
- Risk Manager policy logic
- Reporting chart design beyond saving portfolio CSV

This feature should add portfolio state tracking without breaking earlier features.

---

## Move-On Checklist

- [ ] Portfolio initializes from config starting cash.
- [ ] Buy trades update cash, quantity, and average cost.
- [ ] Sell trades update cash, quantity, and realized P&L.
- [ ] Cannot sell more than held unless shorting is explicitly enabled.
- [ ] Portfolio marks positions to market at each step.
- [ ] Portfolio calculates total value and drawdown.
- [ ] Empty trade runs still generate `portfolio_history.csv`.
- [ ] Unit tests cover accounting and edge cases.
- [ ] Feature does not add real trading, brokerage APIs, database, dashboard, or SaaS scope.
