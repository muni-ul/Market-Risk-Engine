from __future__ import annotations

import pytest

from pyrisklab.exceptions import (
    BenchmarkError,
    ConfigError,
    ExecutionError,
    GreeksError,
    MarketSimulationError,
    PortfolioError,
    PricingError,
    PyRiskLabError,
    ReportingError,
    RiskError,
    RunError,
    StrategyError,
)


@pytest.mark.parametrize(
    "exception_type",
    [
        ConfigError,
        PricingError,
        GreeksError,
        StrategyError,
        ExecutionError,
        MarketSimulationError,
        PortfolioError,
        RiskError,
        ReportingError,
        BenchmarkError,
        RunError,
    ],
)
def test_project_errors_share_cli_catchable_base(exception_type):
    assert issubclass(exception_type, PyRiskLabError)
