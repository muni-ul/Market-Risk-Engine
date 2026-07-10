from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd
import pytest

from pyrisklab.config import load_config
from pyrisklab.exceptions import ReportingError, RunError
from pyrisklab.reporting import (
    prepare_output_dir,
    save_csv_outputs,
    write_run_metadata,
    write_summary_report,
)


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


def test_csv_write_failure_raises_readable_run_error(tmp_path, monkeypatch):
    run_dir = prepare_output_dir(tmp_path, "demo")

    def fail_to_csv(_self, _path, **_kwargs):
        raise OSError("disk is unavailable")

    monkeypatch.setattr(pd.DataFrame, "to_csv", fail_to_csv)

    with pytest.raises(RunError, match="could not write market_path.csv"):
        save_csv_outputs(run_dir, {"market_path.csv": pd.DataFrame({"step": [0]})})


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


def test_run_metadata_records_reproducible_artifact_context(tmp_path):
    run_dir = prepare_output_dir(tmp_path, "demo")
    config = load_config("configs/demo.yaml")
    outputs = {
        "market_path.csv": pd.DataFrame({"step": [0, 1], "underlying_price": [100.0, 101.0]}),
        "trades.csv": pd.DataFrame(columns=["step", "symbol"]),
    }

    metadata_path = write_run_metadata(run_dir, config, Path("configs/demo.yaml"), outputs)
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

    assert metadata["project"] == "PyRiskLab"
    assert metadata["run_name"] == "demo_run"
    assert metadata["seed"] == 42
    assert metadata["simulation_only"] is True
    expected_digest = hashlib.sha256(Path("configs/demo.yaml").read_bytes()).hexdigest()
    assert metadata["config_sha256"] == expected_digest
    assert metadata["csv_row_counts"] == {"market_path.csv": 2, "trades.csv": 0}
    assert "run_metadata.json" in metadata["generated_artifacts"]
    assert "summary_report.md" in metadata["generated_artifacts"]


def test_summary_report_lists_metadata_artifact(tmp_path):
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

    assert "`run_metadata.json`" in report
    assert "`summary_report.md`" in report


def test_summary_report_requires_nonempty_core_frames(tmp_path):
    run_dir = prepare_output_dir(tmp_path, "demo")
    config = load_config("configs/demo.yaml")
    outputs = {
        "market_path.csv": pd.DataFrame(columns=["underlying_price"]),
        "pricing_history.csv": pd.DataFrame({"option_price": [3.0]}),
        "trades.csv": pd.DataFrame(columns=["step", "symbol"]),
        "portfolio_history.csv": pd.DataFrame({"total_value": [10000.0], "drawdown_pct": [0.0]}),
        "risk_events.csv": pd.DataFrame(columns=["step", "reason"]),
        "benchmark.csv": pd.DataFrame(),
    }

    with pytest.raises(ReportingError, match="market_path"):
        write_summary_report(run_dir, config, outputs)


def test_summary_report_requires_vectorized_benchmark_row(tmp_path):
    run_dir = prepare_output_dir(tmp_path, "demo")
    config = load_config("configs/demo.yaml")
    outputs = {
        "market_path.csv": pd.DataFrame({"underlying_price": [100.0, 101.0]}),
        "pricing_history.csv": pd.DataFrame({"option_price": [3.0, 4.0]}),
        "trades.csv": pd.DataFrame(columns=["step", "symbol"]),
        "portfolio_history.csv": pd.DataFrame({"total_value": [10000.0], "drawdown_pct": [0.0]}),
        "risk_events.csv": pd.DataFrame(columns=["step", "reason"]),
        "benchmark.csv": pd.DataFrame({"method": ["python_loop"], "speedup_vs_loop": [1.0]}),
    }

    with pytest.raises(ReportingError, match="numpy_vectorized"):
        write_summary_report(run_dir, config, outputs)


def test_summary_report_validates_benchmark_columns(tmp_path):
    run_dir = prepare_output_dir(tmp_path, "demo")
    config = load_config("configs/demo.yaml")
    outputs = {
        "market_path.csv": pd.DataFrame({"underlying_price": [100.0, 101.0]}),
        "pricing_history.csv": pd.DataFrame({"option_price": [3.0, 4.0]}),
        "trades.csv": pd.DataFrame(columns=["step", "symbol"]),
        "portfolio_history.csv": pd.DataFrame({"total_value": [10000.0], "drawdown_pct": [0.0]}),
        "risk_events.csv": pd.DataFrame(columns=["step", "reason"]),
        "benchmark.csv": pd.DataFrame({"runtime_seconds": [0.1]}),
    }

    with pytest.raises(ReportingError, match="benchmark"):
        write_summary_report(run_dir, config, outputs)
