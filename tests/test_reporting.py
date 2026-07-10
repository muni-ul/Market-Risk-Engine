from __future__ import annotations

import pandas as pd

from pyrisklab.reporting import prepare_output_dir, save_csv_outputs


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
