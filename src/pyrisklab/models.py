from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class MarketConfig:
    initial_price: float
    drift: float
    volatility: float
    trading_days: int
    steps: int
    paths: int


@dataclass(frozen=True)
class OptionConfig:
    underlying_symbol: str
    symbol: str
    option_type: str
    strike: float
    risk_free_rate: float
    volatility: float
    days_to_expiry: int


@dataclass(frozen=True)
class StrategyConfig:
    name: str
    buy_delta_below: float
    sell_delta_above: float
    trade_quantity: int
    min_steps_between_trades: int = 0


@dataclass(frozen=True)
class ExecutionConfig:
    enabled: bool = True
    fill_model: str = "deterministic_mid"
    commission_per_contract: float = 0.0
    contract_multiplier: int = 100


@dataclass(frozen=True)
class RiskConfig:
    starting_cash: float
    max_position_quantity: int
    max_trade_notional: float
    max_drawdown_pct: float
    max_loss_pct: float
    stop_trading_on_breach: bool = True


@dataclass(frozen=True)
class BenchmarkConfig:
    enabled: bool
    num_prices: int
    seed: int = 42
    tolerance: float = 1e-8


@dataclass(frozen=True)
class RunConfig:
    run_name: str
    seed: int
    output_dir: str
    market: MarketConfig
    option: OptionConfig
    strategy: StrategyConfig
    execution: ExecutionConfig
    risk: RiskConfig
    benchmark: BenchmarkConfig


@dataclass(frozen=True)
class OptionContract:
    underlying_symbol: str
    symbol: str
    option_type: str
    strike: float
    risk_free_rate: float
    volatility: float
    initial_days_to_expiry: int


@dataclass(frozen=True)
class Signal:
    step: int
    symbol: str
    action: str
    quantity: int
    reference_price: float
    delta: float
    reason: str


@dataclass(frozen=True)
class Order:
    order_id: str
    step: int
    symbol: str
    side: str
    quantity: int
    order_type: str
    requested_price: float
    source_signal_reason: str = ""


@dataclass(frozen=True)
class Trade:
    trade_id: str
    order_id: str
    step: int
    symbol: str
    side: str
    quantity: int
    fill_price: float
    commission: float
    contract_multiplier: int
    notional: float
    fill_model: str


@dataclass
class Position:
    symbol: str
    quantity: int = 0
    average_cost: float = 0.0


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


@dataclass(frozen=True)
class RiskCheckResult:
    allowed: bool
    events: list[RiskEvent]


@dataclass(frozen=True)
class BenchmarkResult:
    method: str
    num_prices: int
    runtime_seconds: float
    speedup_vs_loop: float
    max_abs_error_vs_loop: float
    passed_equivalence_check: bool


@dataclass(frozen=True)
class RunResult:
    run_name: str
    output_path: Path
    config_path: Path
    status: str
