from __future__ import annotations

import pytest
import yaml

from pyrisklab.config import load_config
from pyrisklab.exceptions import ConfigError


def demo_config() -> dict:
    with open("configs/demo.yaml", encoding="utf-8") as config_file:
        return yaml.safe_load(config_file)


def write_config(tmp_path, data: dict):
    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(data), encoding="utf-8")
    return path


def test_valid_config_loads(tmp_path):
    config = load_config(write_config(tmp_path, demo_config()))
    assert config.run_name == "demo_run"


def test_missing_required_section_fails(tmp_path):
    data = demo_config()
    data.pop("market")
    with pytest.raises(ConfigError, match="market"):
        load_config(write_config(tmp_path, data))


def test_invalid_volatility_fails(tmp_path):
    data = demo_config()
    data["market"]["volatility"] = -0.2
    with pytest.raises(ConfigError, match="market.volatility"):
        load_config(write_config(tmp_path, data))


def test_invalid_option_type_fails(tmp_path):
    data = demo_config()
    data["option"]["option_type"] = "calls"
    with pytest.raises(ConfigError, match="option.option_type"):
        load_config(write_config(tmp_path, data))


def test_invalid_risk_limit_fails(tmp_path):
    data = demo_config()
    data["risk"]["max_trade_notional"] = -1
    with pytest.raises(ConfigError, match="risk.max_trade_notional"):
        load_config(write_config(tmp_path, data))
