from __future__ import annotations

import pandas as pd
import pytest

from pyrisklab.exceptions import MarketSimulationError
from pyrisklab.market import simulate_gbm_path
from pyrisklab.models import MarketConfig


def test_same_seed_produces_same_path(market_config):
    pd.testing.assert_frame_equal(simulate_gbm_path(market_config, 42), simulate_gbm_path(market_config, 42))


def test_different_seed_can_produce_different_path(market_config):
    assert not simulate_gbm_path(market_config, 42)["underlying_price"].equals(simulate_gbm_path(market_config, 43)["underlying_price"])


def test_zero_volatility_behaves_predictably():
    config = MarketConfig(100.0, 0.05, 0.0, 252, 10, 1)
    path = simulate_gbm_path(config, 42)
    assert (path["underlying_price"] > 0).all()
    pd.testing.assert_frame_equal(path, simulate_gbm_path(config, 99))


def test_negative_volatility_should_be_rejected_by_config_layer():
    config = MarketConfig(100.0, 0.05, -0.1, 252, 10, 1)
    with pytest.raises(MarketSimulationError):
        simulate_gbm_path(config, 42)


def test_nonpositive_initial_price_is_invalid_contract_for_config_layer():
    config = MarketConfig(0.0, 0.05, 0.2, 252, 10, 1)
    with pytest.raises(MarketSimulationError):
        simulate_gbm_path(config, 42)
