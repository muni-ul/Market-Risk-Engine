# Feature 8: Risk Manager

## Output Path

`docs/features/08-risk-manager.md`

---

## 1. Feature Overview

### Feature name

**Risk Manager**

### One-sentence description

Validate simulated orders against configurable risk limits before fake execution and log clear risk events when orders are blocked.

### Detailed description

The Risk Manager is the guardrail layer of PyRiskLab. It receives proposed simulated orders from the strategy/order-generation flow, checks them against local config-driven limits, and decides whether each order is allowed or blocked.

This feature should enforce simple, understandable rules:

- Maximum position quantity
- Maximum trade notional
- Maximum drawdown percentage
- Maximum loss percentage
- Optional stop-trading flag after a major breach

The Risk Manager should not generate strategy signals, execute trades, update portfolio accounting, or connect to real brokerages. It only validates proposed simulated trades and records why an order was allowed or blocked.

### Why it matters

This feature makes PyRiskLab feel more professional and less like a toy trading script. It shows that the project has defensive programming, validation, failure handling, and rule-based system design.

For software engineering portfolio value, this is strong because it proves the project can enforce system constraints and produce audit-style logs without becoming a real trading system.

### Skill it demonstrates

- Rule-based validation
- Defensive programming
- Clean separation of concerns
- Dataclasses or typed result objects
- Config-driven behavior
- Edge-case testing
- Clear error/event messages
- State-aware validation using portfolio snapshots

### Priority

**High**

The Risk Manager is a core feature because it connects strategy, fake execution, portfolio state, reporting, and tests into a more serious simulation pipeline.

### Complexity

**Medium**

The rules are intentionally simple, but the logic must be carefully separated from execution and portfolio accounting.

---

## 2. User/Demo Flow

### Happy path

1. User runs:

```bash
python -m pyrisklab run --config configs/demo.yaml
```

2. Config is loaded.
3. Strategy generates fake signals.
4. Proposed orders are created.
5. Risk Manager checks each order against configured limits.
6. Allowed orders continue to Fake Execution.
7. Blocked orders are skipped and recorded as risk events.
8. The pipeline saves:

```text
results/demo_run/risk_events.csv
```

9. Reporting later summarizes allowed trades, blocked orders, and risk-limit behavior.

### First-time path

A first-time user should not need to configure advanced risk settings. The demo config should include simple default limits:

```yaml
risk:
  starting_cash: 10000.0
  max_position_quantity: 10
  max_trade_notional: 2500.0
  max_drawdown_pct: 0.15
  max_loss_pct: 0.10
  stop_trading_on_breach: true
```

The default demo should ideally produce either no risk events, proving all trades stayed inside limits, or one or two easy-to-understand blocked trades, proving the system works.

[Decision] It is better for the demo to include at least one controlled risk event in a separate config preset later, but the main demo can stay clean.

### Empty state

If no orders are blocked, the system should still create:

```text
risk_events.csv
```

The file should contain headers and zero rows.

Recommended report behavior later:

```text
No risk events were triggered in this run.
```

### Error path

Risk Manager should raise clear config errors for invalid risk settings, such as:

```text
ConfigError: risk.max_position_quantity must be >= 0. Received -1.
ConfigError: risk.max_trade_notional must be >= 0. Received -500.
ConfigError: risk.max_drawdown_pct must be between 0 and 1. Received 1.5.
```

For blocked orders, it should not crash. It should return a structured blocked result and create a risk event.

Example blocked message:

```text
Blocked BUY 5 CALL_105 at step 88: trade notional 3100.00 exceeds max_trade_notional 2500.00.
```

### Demo path for a reviewer

Reviewer runs:

```bash
pytest tests/test_risk.py
python -m pyrisklab run --config configs/demo.yaml --overwrite
```

Reviewer checks:

```text
results/demo_run/risk_events.csv
```

A reviewer should be able to understand exactly why any order was blocked.

---

## 3. UX/UI Requirements

### Screens/pages

No traditional UI screens are required.

User-facing surfaces:

1. CLI progress messages
2. `risk_events.csv`
3. Later summary report risk section
4. Later README/demo explanation

### Components

#### CLI progress message

Pipeline should include:

```text
[8/12] Applying risk checks...
```

or:

```text
Validating simulated orders against risk limits...
```

#### Risk events CSV

Required output:

```text
results/<run_name>/risk_events.csv
```

Recommended columns:

| Column | Description |
|---|---|
| `step` | Simulation step |
| `event_type` | Type of event, such as `ORDER_BLOCKED` or `TRADING_STOPPED` |
| `severity` | `INFO`, `WARNING`, or `CRITICAL` |
| `symbol` | Option symbol |
| `proposed_side` | `BUY` or `SELL` |
| `proposed_quantity` | Quantity requested |
| `proposed_notional` | Estimated notional value |
| `portfolio_value` | Portfolio value at validation time |
| `limit_name` | Limit that was violated |
| `limit_value` | Configured risk limit |
| `observed_value` | Actual value that violated the limit |
| `reason` | Human-readable reason |

### Forms/inputs

No direct form is needed.

Inputs come from:

- Risk config
- Proposed `Order`
- Current `Portfolio` or `PortfolioSnapshot`
- Current/estimated market price
- Existing position quantity

### Buttons/actions

No buttons are needed.

Main CLI action:

```bash
python -m pyrisklab run --config configs/demo.yaml
```

### Validation messages

Config validation messages:

```text
ConfigError: risk.max_drawdown_pct must be between 0 and 1. Received -0.20.
ConfigError: risk.max_loss_pct must be between 0 and 1. Received 2.0.
ConfigError: risk.max_trade_notional must be >= 0. Received -100.
```

Blocked order messages:

```text
RiskEvent: blocked BUY order because proposed position quantity 12 exceeds max_position_quantity 10.
RiskEvent: blocked BUY order because trade notional 2750.00 exceeds max_trade_notional 2500.00.
RiskEvent: trading stopped because drawdown_pct 0.18 exceeded max_drawdown_pct 0.15.
```

### Empty states

If no risk events exist:

- `risk_events.csv` should still be created.
- Later report should say:

```text
No risk events were triggered.
```

If risk config disables all limits, which is not recommended:

```text
Risk Manager ran with no active blocking rules.
```

[Open Question] Decide whether disabling all risk rules should be allowed. Recommended MVP: allow high limits, but do not add a special disable mode.

### Loading states

CLI progress is enough:

```text
Applying risk checks...
Saved risk_events.csv
```

### Error states

Expected user/config errors should use `ConfigError`.

Unexpected risk logic failures should use `RiskError`.

Blocked orders are not errors. They are valid simulation events.

### Responsive behavior if relevant

Not relevant for MVP.

---

## 4. Data Requirements

### Entities involved

#### Input entities

- `RunConfig`
- `RiskConfig`
- `Order`
- `PortfolioSnapshot`
- `Position`
- Current market/fill price

#### Main risk entities

- `RiskManager`
- `RiskCheckResult`
- `RiskEvent`

#### Output entities

- `risk_events.csv`

### Fields

#### RiskConfig

Recommended fields:

```python
RiskConfig:
  starting_cash: float
  max_position_quantity: int
  max_trade_notional: float
  max_drawdown_pct: float
  max_loss_pct: float
  stop_trading_on_breach: bool
```

[Decision] `starting_cash` can live in `risk` for MVP because risk and portfolio both need it.

[Open Question] If config grows later, decide whether starting cash belongs under a separate `portfolio` section.

#### RiskCheckResult

Recommended fields:

```python
RiskCheckResult:
  allowed: bool
  reason: str | None
  events: list[RiskEvent]
```

[Decision] Use a list of events so multiple failed rules can be recorded if desired.

#### RiskEvent

Recommended fields:

```python
RiskEvent:
  step: int
  event_type: str
  severity: str
  symbol: str
  proposed_side: str
  proposed_quantity: int
  proposed_notional: float
  portfolio_value: float
  limit_name: str
  limit_value: float
  observed_value: float
  reason: str
```

### Relationships

- One run has one Risk Manager.
- One Risk Manager uses one Risk Config.
- One order receives one risk validation result.
- One blocked order creates one or more risk events.
- Risk events are saved to `risk_events.csv`.
- Fake Execution only receives allowed orders.
- Portfolio Tracker should not apply blocked orders.

### Example seed data

Recommended config:

```yaml
risk:
  starting_cash: 10000.0
  max_position_quantity: 10
  max_trade_notional: 2500.0
  max_drawdown_pct: 0.15
  max_loss_pct: 0.10
  stop_trading_on_breach: true
```

Example risk event output:

```csv
step,event_type,severity,symbol,proposed_side,proposed_quantity,proposed_notional,portfolio_value,limit_name,limit_value,observed_value,reason
88,ORDER_BLOCKED,WARNING,CALL_105,BUY,5,3100.00,9825.50,max_trade_notional,2500.00,3100.00,"Trade notional exceeds configured maximum."
```

### Local persistence needs

Required output:

```text
results/<run_name>/risk_events.csv
```

No database is needed.

Justification:

- Risk events are generated per run.
- CSV is easy for reviewers to inspect.
- Reporting can read CSV directly.
- Database scope is unnecessary for MVP.

---

## 5. Logic Requirements

### Business rules

#### Rule 1: Max position quantity

Before allowing an order, estimate the resulting position quantity.

For BUY:

```text
resulting_quantity = current_quantity + order.quantity
```

For SELL:

```text
resulting_quantity = current_quantity - order.quantity
```

Block if:

```text
abs(resulting_quantity) > max_position_quantity
```

#### Rule 2: Max trade notional

Calculate proposed notional:

```text
proposed_notional = order.requested_price * order.quantity * contract_multiplier
```

Block if:

```text
proposed_notional > max_trade_notional
```

If `max_trade_notional` is zero, the rule blocks all nonzero trades.

#### Rule 3: Max drawdown percentage

Use current portfolio snapshot:

```text
drawdown_pct = snapshot.drawdown_pct
```

If:

```text
drawdown_pct >= max_drawdown_pct
```

Then block new trades when `stop_trading_on_breach` is true.

#### Rule 4: Max loss percentage

Calculate loss relative to starting cash:

```text
loss_pct = max(0, (starting_cash - portfolio_value) / starting_cash)
```

If:

```text
loss_pct >= max_loss_pct
```

Then block new trades when `stop_trading_on_breach` is true.

#### Rule 5: Stop trading after breach

If a major breach occurs and `stop_trading_on_breach` is true:

- Set internal flag `trading_stopped = True`.
- Block all future orders.
- Create a risk event explaining trading has stopped.

[Decision] Keep this simple. Do not add complex recovery logic in MVP.

### Calculations

Required calculations:

- Proposed notional
- Resulting position quantity
- Drawdown percentage check
- Loss percentage check
- Blocking reason generation

### API/service functions if needed

Recommended class:

```python
class RiskManager:
    def __init__(self, config: RiskConfig, contract_multiplier: int = 100) -> None:
        ...

    def validate_order(
        self,
        order: Order,
        current_position_quantity: int,
        portfolio_snapshot: PortfolioSnapshot,
    ) -> RiskCheckResult:
        ...

    def get_events(self) -> list[RiskEvent]:
        ...
```

Recommended helper functions:

```python
def calculate_order_notional(price: float, quantity: int, multiplier: int) -> float:
    ...

def build_risk_events_frame(events: list[RiskEvent]) -> pd.DataFrame:
    ...
```

### State management

Risk Manager may keep one internal state flag:

```python
trading_stopped: bool
```

It may also keep:

```python
events: list[RiskEvent]
```

Do not store portfolio cash/positions inside Risk Manager. Portfolio owns portfolio state.

### Edge cases

#### Multiple rule failures at once

Example: an order violates both max position size and max trade notional.

[Decision] Record first failure in MVP. Add all-failure reporting later if needed.

#### Threshold equality

If drawdown is exactly equal to max allowed:

```text
drawdown_pct >= max_drawdown_pct
```

should count as a breach.

Same for max loss.

#### Zero limits

- `max_position_quantity = 0` means no positions allowed.
- `max_trade_notional = 0` means no trades allowed.
- `max_drawdown_pct = 0` means any drawdown triggers stop.
- `max_loss_pct = 0` means any loss triggers stop.

These values should be valid but strict.

#### Missing portfolio snapshot

Risk validation needs current portfolio state. If missing, raise `RiskError`.

#### Negative order quantity

Should already be rejected by Order/Fake Execution validation, but Risk Manager should not silently allow it.

#### Negative price

Reject with `RiskError` or rely on earlier validation. Defensive check is acceptable.

---

## 6. Acceptance Criteria

### AC1: Allowed order passes risk checks

Given a valid order within all configured limits  
When the Risk Manager validates the order  
Then the result is allowed  
And no risk event is created.

### AC2: Max position quantity blocks oversized order

Given current position quantity is `9`  
And max position quantity is `10`  
When a BUY order for quantity `2` is validated  
Then the order is blocked  
And a risk event is created explaining the position limit breach.

### AC3: Max trade notional blocks expensive order

Given max trade notional is `2500`  
When an order has proposed notional `3000`  
Then the order is blocked  
And the risk event identifies `max_trade_notional`.

### AC4: Max drawdown breach stops trading

Given portfolio drawdown percentage is `0.16`  
And max drawdown percentage is `0.15`  
And `stop_trading_on_breach` is true  
When any new order is validated  
Then the order is blocked  
And the Risk Manager marks trading as stopped.

### AC5: Max loss breach stops trading

Given starting cash is `10000`  
And portfolio value is `8900`  
And max loss percentage is `0.10`  
When a new order is validated  
Then the order is blocked  
And a risk event explains the max loss breach.

### AC6: Trading stopped blocks future orders

Given the Risk Manager has already triggered `trading_stopped`  
When a later order is validated  
Then the order is blocked  
And the reason says trading has stopped after a prior risk breach.

### AC7: Empty risk events file is still produced

Given no orders are blocked  
When the run completes  
Then `risk_events.csv` is still created  
And it contains the expected headers.

### AC8: Invalid risk config fails early

Given `max_drawdown_pct` is `-0.2`  
When config is loaded  
Then the system raises `ConfigError`  
And the message names the invalid field.

---

## 7. Test Plan

### Unit tests

Create:

```text
tests/test_risk.py
```

Recommended tests:

1. `test_allowed_order_passes`
2. `test_position_limit_blocks_buy_order`
3. `test_trade_notional_limit_blocks_order`
4. `test_drawdown_breach_blocks_order`
5. `test_loss_breach_blocks_order`
6. `test_trading_stopped_blocks_future_orders`
7. `test_zero_position_limit_blocks_all_position_increasing_orders`
8. `test_zero_trade_notional_blocks_nonzero_trade`
9. `test_threshold_equality_counts_as_breach`
10. `test_risk_event_contains_readable_reason`
11. `test_risk_events_frame_has_required_columns`
12. `test_invalid_negative_order_quantity_fails_defensively`

### Integration tests if useful

Create:

```text
tests/test_pipeline_risk_integration.py
```

Recommended test:

- Use a tiny fake order list.
- Set max trade notional very low.
- Confirm at least one order is blocked.
- Confirm blocked order is not passed to Fake Execution.
- Confirm `risk_events.csv` is created.

### Manual QA checklist

- [ ] Run demo config.
- [ ] Confirm `risk_events.csv` exists.
- [ ] Confirm no-risk-event runs do not crash.
- [ ] Temporarily lower `max_trade_notional` and rerun.
- [ ] Confirm trades are blocked.
- [ ] Confirm blocked trades do not appear in `trades.csv`.
- [ ] Confirm risk event reason is readable.
- [ ] Temporarily lower `max_position_quantity` and rerun.
- [ ] Confirm position-limit event appears.
- [ ] Confirm invalid risk config raises clear error.

### Demo verification checklist

- [ ] `pytest tests/test_risk.py` passes.
- [ ] Full demo run completes.
- [ ] `risk_events.csv` is generated.
- [ ] Risk events are understandable without reading source code.
- [ ] README later states this is simulated risk control only.
- [ ] No real compliance, brokerage, or financial advice claims are added.

---

## 8. Portfolio Value

### How this feature helps the project stand out

Risk Manager adds a serious engineering signal. It shows that PyRiskLab is not just calculating numbers; it is enforcing constraints and making controlled decisions based on system state.

This helps the project stand out because it demonstrates:

- Guardrail design
- Data validation
- Failure-path thinking
- Clear logging
- State-aware checks
- Testable rule logic

### What to mention in README

Mention:

```text
A config-driven Risk Manager validates simulated orders before fake execution. It can block orders that exceed max position size, trade notional, drawdown, or loss limits, then records the reason in risk_events.csv.
```

Also mention:

```text
Risk controls are part of the local simulation only. PyRiskLab does not perform real trading, connect to brokerages, or provide investment advice.
```

### What to mention in interviews

Strong interview points:

- “I separated risk validation from portfolio accounting and fake execution.”
- “Blocked trades are treated as valid simulation events, not crashes.”
- “The Risk Manager returns structured validation results instead of just True or False.”
- “I tested both allowed and blocked trade paths.”
- “I kept the risk rules simple because the project goal is software engineering, not real financial compliance.”

---

## 9. Implementation Notes For Codex

### Likely files/folders

Primary files:

```text
src/pyrisklab/risk.py
tests/test_risk.py
```

Related files:

```text
src/pyrisklab/models.py
src/pyrisklab/config.py
src/pyrisklab/exceptions.py
src/pyrisklab/pipeline.py
src/pyrisklab/reporting.py
configs/demo.yaml
```

Generated output:

```text
results/<run_name>/risk_events.csv
```

### Suggested models

Add or confirm in `models.py`:

```python
@dataclass(frozen=True)
class RiskConfig:
    starting_cash: float
    max_position_quantity: int
    max_trade_notional: float
    max_drawdown_pct: float
    max_loss_pct: float
    stop_trading_on_breach: bool = True
```

```python
@dataclass(frozen=True)
class RiskEvent:
    step: int
    event_type: str
    severity: str
    symbol: str
    proposed_side: str
    proposed_quantity: int
    proposed_notional: float
    portfolio_value: float
    limit_name: str
    limit_value: float
    observed_value: float
    reason: str
```

```python
@dataclass(frozen=True)
class RiskCheckResult:
    allowed: bool
    events: list[RiskEvent]
```

### Suggested exception

In `exceptions.py`:

```python
class RiskError(PyRiskLabError):
    """Raised when risk validation cannot be completed safely."""
```

### Build order

1. Add/confirm `RiskConfig`, `RiskEvent`, and `RiskCheckResult`.
2. Add/confirm `RiskError`.
3. Add risk config validation in `config.py`.
4. Implement `calculate_order_notional(...)`.
5. Implement `RiskManager.__init__`.
6. Implement max trade notional rule.
7. Implement max position quantity rule.
8. Implement drawdown/loss stop rules.
9. Implement trading stopped behavior.
10. Implement risk-events DataFrame export.
11. Add unit tests in `tests/test_risk.py`.
12. Add simple pipeline integration so blocked orders do not execute.
13. Confirm `risk_events.csv` is produced even when empty.

### Risks

#### Risk 1: Mixing Risk Manager with Portfolio Tracker

Do not make Risk Manager update cash, positions, average cost, or P&L. Portfolio Tracker owns accounting.

#### Risk 2: Mixing Risk Manager with Fake Execution

Do not make Risk Manager fill trades. Fake Execution owns fills. Risk Manager only approves or blocks orders.

#### Risk 3: Overbuilding finance compliance

Do not add:

- Compliance dashboards
- Audit permissions
- Regulatory rules
- User accounts
- Enterprise controls
- Real broker checks

This is a local simulation guardrail only.

#### Risk 4: Making strategy seem profit-focused

Do not optimize the strategy based on risk results. The project is not about profitable trading.

#### Risk 5: Hidden blocked trades

Every blocked order should create a readable risk event so reviewers can see the system behavior.

### What not to change

Do not change:

- CLI command format
- Market simulation outputs
- Black-Scholes formulas
- Greeks formulas
- Simple fake strategy rules
- Fake execution fill method
- Portfolio accounting logic
- Reporting architecture beyond adding `risk_events.csv`

This feature should add risk validation between order creation and fake execution.

---

## Move-On Checklist

- [ ] Risk config validates correctly.
- [ ] Allowed orders pass.
- [ ] Oversized position orders are blocked.
- [ ] Oversized notional orders are blocked.
- [ ] Drawdown/loss breaches can stop future trades.
- [ ] Blocked orders generate readable `RiskEvent` rows.
- [ ] Blocked orders are not fake-executed.
- [ ] Empty `risk_events.csv` still gets created.
- [ ] Unit tests cover allowed and blocked paths.
- [ ] Feature does not add real trading, brokerage APIs, compliance systems, SaaS scope, dashboards, or databases.
