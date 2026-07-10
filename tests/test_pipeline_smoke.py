from __future__ import annotations

import pandas as pd
import pytest
import yaml

from pyrisklab.exceptions import RunError
from pyrisklab.pipeline import _as_order_quantity, run_simulation


def test_pipeline_smoke_creates_core_artifacts(tmp_path):
    with open("configs/demo.yaml", encoding="utf-8") as config_file:
        config = yaml.safe_load(config_file)
    config["run_name"] = "smoke_run"
    config["output_dir"] = str(tmp_path)
    config["market"]["steps"] = 5
    config["option"]["days_to_expiry"] = 5
    config["benchmark"]["num_prices"] = 10
    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(config), encoding="utf-8")

    result = run_simulation(path, overwrite=True)

    assert result.output_path.exists()
    assert (result.output_path / "market_path.csv").exists()
    assert (result.output_path / "pricing_history.csv").exists()
    assert (result.output_path / "portfolio_history.csv").exists()
    assert (result.output_path / "risk_events.csv").exists()
    assert (result.output_path / "summary_report.md").exists()


def test_pipeline_respects_disabled_fake_execution(tmp_path):
    with open("configs/demo.yaml", encoding="utf-8") as config_file:
        config = yaml.safe_load(config_file)
    config["run_name"] = "execution_disabled_run"
    config["output_dir"] = str(tmp_path)
    config["market"]["steps"] = 5
    config["option"]["days_to_expiry"] = 5
    config["execution"]["enabled"] = False
    config["benchmark"]["num_prices"] = 10
    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(config), encoding="utf-8")

    result = run_simulation(path, overwrite=True)

    orders = pd.read_csv(result.output_path / "orders.csv")
    trades = pd.read_csv(result.output_path / "trades.csv")
    assert {"status", "risk_reason"}.issubset(orders.columns)
    assert trades.empty
    if not orders.empty:
        assert set(orders["status"]) == {"SKIPPED"}


def test_pipeline_preserves_empty_order_schema(tmp_path):
    with open("configs/demo.yaml", encoding="utf-8") as config_file:
        config = yaml.safe_load(config_file)
    config["run_name"] = "no_orders_run"
    config["output_dir"] = str(tmp_path)
    config["market"]["steps"] = 5
    config["option"]["days_to_expiry"] = 5
    config["strategy"]["buy_delta_below"] = -1.0
    config["strategy"]["sell_delta_above"] = 1.0
    config["benchmark"]["num_prices"] = 10
    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(config), encoding="utf-8")

    result = run_simulation(path, overwrite=True)

    orders = pd.read_csv(result.output_path / "orders.csv")
    trades = pd.read_csv(result.output_path / "trades.csv")
    assert orders.empty
    assert {"status", "risk_reason"}.issubset(orders.columns)
    assert trades.empty


def test_pipeline_rejects_fractional_order_quantity_before_risk():
    with pytest.raises(RunError, match="order quantity"):
        _as_order_quantity(1.5)


def test_pipeline_rejects_nonfinite_order_quantity_before_risk():
    with pytest.raises(RunError, match="order quantity"):
        _as_order_quantity(float("inf"))


def test_pipeline_rejects_numpy_fractional_order_quantity_before_risk():
    with pytest.raises(RunError, match="order quantity"):
        _as_order_quantity(pd.Series([1.5]).iloc[0])
