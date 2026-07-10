from __future__ import annotations

import pandas as pd

from pyrisklab.config import load_config
from pyrisklab.reporting import prepare_output_dir, save_csv_outputs, write_summary_report


def test_output_directory_is_created(tmp_path):
    assert prepare_output_dir(tmp_path, "demo").exists()


def test_empty_trades_still_produce_trades_csv(tmp_path):
    run_dir = prepare_output_dir(tmp_path, "demo")
    save_csv_outputs(run_dir, {"trades.csv": pd.DataFrame(columns=["step", "symbol"])})
    assert (run_dir / "trades.csv").exists()


def test_empty_risk_events_still_produce_risk_events_csv(tmp_path):
    run_dir = prepare_output_dir(tmp_path, "demo")
    save_csv_outputs(run_dir, {"risk_events.csv": pd.DataFrame(columns=["step", "reason"])})
    assert (run_dir / "risk_events.csv").exists()


def test_summary_report_is_created_by_full_reporting_surface(tmp_path):
    run_dir = prepare_output_dir(tmp_path, "demo")
    (run_dir / "summary_report.md").write_text("# Summary", encoding="utf-8")
    assert (run_dir / "summary_report.md").exists()


def test_summary_report_mentions_empty_trades_and_risk_events(tmp_path):
    run_dir = prepare_output_dir(tmp_path, "demo")
    config = load_config("configs/demo.yaml")
    outputs = {
        "market_path.csv": pd.DataFrame({"underlying_price": [100.0, 101.0]}),
        "pricing_history.csv": pd.DataFrame({"option_price": [3.0, 4.0]}),
        "trades.csv": pd.DataFrame(columns=["step", "symbol"]),
        "portfolio_history.csv": pd.DataFrame({"total_value": [10000.0], "drawdown_pct": [0.0]}),
        "risk_events.csv": pd.DataFrame(columns=["step", "reason"]),
        "benchmark.csv": pd.DataFrame(),
    }

    report = write_summary_report(run_dir, config, outputs).read_text(encoding="utf-8")

    assert "No simulated trades were executed" in report
    assert "No risk events were triggered" in report
