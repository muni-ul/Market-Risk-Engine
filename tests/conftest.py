from __future__ import annotations

import pytest

from pyrisklab.models import MarketConfig, RiskConfig, StrategyConfig


@pytest.fixture
def market_config() -> MarketConfig:
    return MarketConfig(100.0, 0.05, 0.20, 252, 10, 1)


@pytest.fixture
def strategy_config() -> StrategyConfig:
    return StrategyConfig("simple_delta_rule", 0.45, 0.70, 1, 0)


@pytest.fixture
def risk_config() -> RiskConfig:
    return RiskConfig(10000.0, 10, 2500.0, 0.15, 0.10, True)
