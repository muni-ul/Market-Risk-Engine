from __future__ import annotations

from dataclasses import asdict, dataclass

MARKET_PRESETS = {
    "Baseline Market": {"drift": 0.07, "volatility": 0.18, "seed": 42},
    "Growth Environment": {"drift": 0.12, "volatility": 0.16, "seed": 17},
    "Elevated Volatility": {"drift": 0.04, "volatility": 0.35, "seed": 91},
    "Market Correction": {"drift": -0.12, "volatility": 0.28, "seed": 73},
    "Prolonged Downturn": {"drift": -0.20, "volatility": 0.24, "seed": 108},
    "Recovery Cycle": {"drift": 0.10, "volatility": 0.30, "seed": 2026},
}

PORTFOLIO_PROFILES = {
    "Capital Preservation": (60, 35, 5),
    "Conservative": (35, 55, 10),
    "Balanced Growth": (20, 65, 15),
    "Growth Focused": (10, 70, 20),
}


@dataclass(frozen=True)
class ScenarioInputs:
    name: str = "Baseline Market"
    starting_capital: float = 10_000.0
    horizon_days: int = 252
    paths: int = 500
    initial_price: float = 100.0
    drift: float = 0.07
    volatility: float = 0.18
    seed: int = 42
    cash_pct: float = 20.0
    stock_pct: float = 65.0
    option_pct: float = 15.0
    option_type: str = "call"
    strike: float = 105.0
    option_volatility: float = 0.22
    risk_free_rate: float = 0.04
    option_expiry_days: int = 252
    max_trade_notional: float = 25_000.0
    max_drawdown_pct: float = 20.0

    def validate(self) -> list[str]:
        errors = []
        if not 1_000 <= self.starting_capital <= 1_000_000:
            errors.append("Starting capital must be between $1,000 and $1,000,000.")
        if self.horizon_days <= 0 or self.paths not in {100, 500, 1000, 5000}:
            errors.append("Choose a positive horizon and a supported path count.")
        if self.initial_price <= 0 or self.strike <= 0:
            errors.append("Stock price and option strike must be greater than zero.")
        if self.volatility < 0 or self.option_volatility < 0:
            errors.append("Volatility cannot be negative.")
        if abs(self.cash_pct + self.stock_pct + self.option_pct - 100) > 0.01:
            errors.append("Cash, stock, and options allocations must total 100%.")
        if min(self.cash_pct, self.stock_pct, self.option_pct) < 0:
            errors.append("Allocations cannot be negative.")
        if self.option_expiry_days <= 0:
            errors.append("Option expiry must be after the scenario start.")
        return errors

    def to_dict(self) -> dict[str, object]:
        return asdict(self)
