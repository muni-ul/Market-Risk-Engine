from __future__ import annotations

from dataclasses import replace
import hashlib
import json
from pathlib import Path

import pandas as pd
import pytest

import pyrisklab.reporting as reporting
from pyrisklab.config import load_config
from pyrisklab.exceptions import ReportingError, RunError
from pyrisklab.models import (
    BenchmarkConfig,
    ORDER_STATUS_COLUMN,
    ORDER_STATUS_APPROVED,
    ORDER_STATUS_BLOCKED,
    ORDER_STATUS_SKIPPED,
)
from pyrisklab.reporting import (
    generate_charts,
    plot_greeks,
    prepare_output_dir,
    save_csv_outputs,
    write_run_metadata,
    write_summary_report,
)


def test_output_directory_is_created(tmp_path):
    assert prepare_output_dir(tmp_path, "demo").exists()


def test_output_directory_create_failure_raises_readable_run_error(tmp_path, monkeypatch):
    def fail_mkdir(_self, **_kwargs):
        raise OSError("disk is unavailable")

    monkeypatch.setattr(Path, "mkdir", fail_mkdir)

    with pytest.raises(RunError, match="could not create"):
        prepare_output_dir(tmp_path, "demo")


def test_output_directory_overwrite_failure_raises_readable_run_error(tmp_path, monkeypatch):
    run_dir = prepare_output_dir(tmp_path, "demo")

    def fail_rmtree(_path):
        raise OSError("directory is locked")

    monkeypatch.setattr("pyrisklab.reporting.shutil.rmtree", fail_rmtree)

    with pytest.raises(RunError, match="could not overwrite"):
        prepare_output_dir(tmp_path, run_dir.name, overwrite=True)


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


def test_non_dataframe_csv_output_raises_reporting_error(tmp_path):
    run_dir = prepare_output_dir(tmp_path, "demo")

    with pytest.raises(ReportingError, match="market_path.csv"):
        save_csv_outputs(run_dir, {"market_path.csv": [{"step": 0}]})


def test_greeks_chart_write_failure_raises_readable_run_error(tmp_path, monkeypatch):
    run_dir = prepare_output_dir(tmp_path, "demo")
    greeks_history = pd.DataFrame(
        {
            "step": [0],
            "delta": [0.5],
            "gamma": [0.01],
            "vega": [0.2],
            "theta": [-0.01],
            "rho": [0.1],
        }
    )

    def fail_savefig(_self, _path, **_kwargs):
        raise OSError("disk is unavailable")

    monkeypatch.setattr("matplotlib.figure.Figure.savefig", fail_savefig)

    with pytest.raises(RunError, match="could not write greeks.png"):
        plot_greeks(greeks_history, run_dir)


def test_missing_required_chart_output_raises_reporting_error(tmp_path):
    run_dir = prepare_output_dir(tmp_path, "demo")

    with pytest.raises(ReportingError, match="market_path.csv"):
        generate_charts(run_dir, {})


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
        "greeks_history.csv": pd.DataFrame(
            {
                "delta": [0.50, 0.55],
                "gamma": [0.010, 0.012],
                "vega": [0.20, 0.22],
                "theta": [-0.030, -0.028],
                "rho": [0.10, 0.11],
            }
        ),
        "trades.csv": pd.DataFrame(columns=["step", "symbol"]),
        "portfolio_history.csv": pd.DataFrame(
            {
                "cash": [10000.0],
                "position_quantity": [0],
                "realized_pnl": [0.0],
                "unrealized_pnl": [0.0],
                "total_value": [10000.0],
                "peak_value": [10000.0],
                "drawdown_pct": [0.0],
            }
        ),
        "risk_events.csv": pd.DataFrame(columns=["step", "reason"]),
        "benchmark.csv": pd.DataFrame(),
    }

    report = write_summary_report(run_dir, config, outputs).read_text(encoding="utf-8")

    assert "No simulated trades were executed" in report
    assert "No risk events were triggered" in report
    assert "## Greeks" in report
    assert "Final delta: 0.5500" in report
    assert "## Strategy Signals" in report
    assert "Strategy: `simple_delta_rule`" in report
    assert "Buy when delta is below: 0.4500" in report
    assert "Sell when delta is above: 0.7000" in report
    assert "Trade quantity: 1" in report
    assert "Minimum steps between trades: 5" in report
    assert "Final cash: $10,000.00" in report
    assert "Final position quantity: 0" in report
    assert "Final realized P&L: $0.00" in report
    assert "Final unrealized P&L: $0.00" in report
    assert "Peak portfolio value: $10,000.00" in report
    assert "## Fake Execution" in report
    assert "Enabled: true" in report
    assert "Fill model: `deterministic_mid`" in report
    assert "Commission per contract: $0.00" in report
    assert "Contract multiplier: 100" in report
    assert "## Risk Events" in report
    assert "Max position quantity: 10" in report
    assert "Max trade notional: $2,500.00" in report
    assert "Max drawdown: 15.00%" in report
    assert "Max loss: 10.00%" in report
    assert "Stop trading on breach: true" in report
    assert "## Run Metadata" in report
    assert "Metadata schema version: 3" in report
    assert "Config SHA-256 digest: recorded in `run_metadata.json`" in report
    assert "Benchmark prices: 100,000" in report
    assert "Artifact audit: expected artifacts, generated artifacts, and byte sizes" in report


def test_summary_report_validates_greeks_columns_when_present(tmp_path):
    run_dir = prepare_output_dir(tmp_path, "demo")
    config = load_config("configs/demo.yaml")
    outputs = {
        "market_path.csv": pd.DataFrame({"underlying_price": [100.0, 101.0]}),
        "pricing_history.csv": pd.DataFrame({"option_price": [3.0, 4.0]}),
        "greeks_history.csv": pd.DataFrame({"delta": [0.55]}),
        "trades.csv": pd.DataFrame(columns=["step", "symbol"]),
        "portfolio_history.csv": pd.DataFrame({"total_value": [10000.0], "drawdown_pct": [0.0]}),
        "risk_events.csv": pd.DataFrame(columns=["step", "reason"]),
        "benchmark.csv": pd.DataFrame(),
    }

    with pytest.raises(ReportingError, match="greeks_history"):
        write_summary_report(run_dir, config, outputs)


def test_summary_report_mentions_disabled_benchmark_config(tmp_path):
    run_dir = prepare_output_dir(tmp_path, "demo")
    config = replace(
        load_config("configs/demo.yaml"),
        benchmark=BenchmarkConfig(enabled=False, num_prices=1, seed=42),
    )
    outputs = {
        "market_path.csv": pd.DataFrame({"underlying_price": [100.0, 101.0]}),
        "pricing_history.csv": pd.DataFrame({"option_price": [3.0, 4.0]}),
        "trades.csv": pd.DataFrame(columns=["step", "symbol"]),
        "portfolio_history.csv": pd.DataFrame({"total_value": [10000.0], "drawdown_pct": [0.0]}),
        "risk_events.csv": pd.DataFrame(columns=["step", "reason"]),
        "benchmark.csv": pd.DataFrame(),
    }

    report = write_summary_report(run_dir, config, outputs).read_text(encoding="utf-8")

    assert "benchmark.enabled is false" in report


def test_summary_report_describes_benchmark_evidence(tmp_path):
    run_dir = prepare_output_dir(tmp_path, "demo")
    config = load_config("configs/demo.yaml")
    outputs = {
        "market_path.csv": pd.DataFrame({"underlying_price": [100.0, 101.0]}),
        "pricing_history.csv": pd.DataFrame({"option_price": [3.0, 4.0]}),
        "trades.csv": pd.DataFrame(columns=["step", "symbol"]),
        "portfolio_history.csv": pd.DataFrame({"total_value": [10000.0], "drawdown_pct": [0.0]}),
        "risk_events.csv": pd.DataFrame(columns=["step", "reason"]),
        "benchmark.csv": pd.DataFrame(
            {
                "method": ["python_loop", "numpy_vectorized"],
                "num_prices": [1000, 1000],
                "option_type": ["call", "call"],
                "strike": [105.0, 105.0],
                "risk_free_rate": [0.04, 0.04],
                "volatility": [0.20, 0.20],
                "runtime_seconds": [0.2, 0.01],
                "speedup_vs_loop": [1.0, 20.0],
                "max_abs_error_vs_loop": [0.0, 1e-10],
                "passed_equivalence_check": [True, True],
            }
        ),
    }

    report = write_summary_report(run_dir, config, outputs).read_text(encoding="utf-8")

    assert "20.00x faster" in report
    assert "Option type: `call`" in report
    assert "Strike: $105.00" in report
    assert "Risk-free rate: 4.00%" in report
    assert "Volatility: 20.00%" in report
    assert "Prices compared: 1,000" in report
    assert "Python loop runtime: 0.200000 seconds" in report
    assert "NumPy vectorized runtime: 0.010000 seconds" in report
    assert "Max absolute error vs loop: 1.000e-10" in report
    assert "Numerical equivalence check: passed" in report


def test_summary_report_counts_order_audit_statuses(tmp_path):
    run_dir = prepare_output_dir(tmp_path, "demo")
    config = load_config("configs/demo.yaml")
    outputs = {
        "market_path.csv": pd.DataFrame({"underlying_price": [100.0, 101.0]}),
        "pricing_history.csv": pd.DataFrame({"option_price": [3.0, 4.0]}),
        "orders.csv": pd.DataFrame(
            {
                ORDER_STATUS_COLUMN: [
                    ORDER_STATUS_APPROVED,
                    ORDER_STATUS_BLOCKED,
                    ORDER_STATUS_SKIPPED,
                    ORDER_STATUS_BLOCKED,
                ],
            }
        ),
        "trades.csv": pd.DataFrame({"step": [1], "symbol": ["CALL_105"]}),
        "portfolio_history.csv": pd.DataFrame({"total_value": [10000.0], "drawdown_pct": [0.0]}),
        "risk_events.csv": pd.DataFrame({"step": [2, 3], "reason": ["limit", "limit"]}),
        "benchmark.csv": pd.DataFrame(),
    }

    report = write_summary_report(run_dir, config, outputs).read_text(encoding="utf-8")

    assert "Approved simulated orders: 1" in report
    assert "Blocked simulated orders: 2" in report
    assert "Skipped simulated orders: 1" in report


def test_run_metadata_records_reproducible_artifact_context(tmp_path):
    run_dir = prepare_output_dir(tmp_path, "demo")
    config = load_config("configs/demo.yaml")
    outputs = {
        "market_path.csv": pd.DataFrame({"step": [0, 1], "underlying_price": [100.0, 101.0]}),
        "trades.csv": pd.DataFrame(columns=["step", "symbol"]),
    }
    save_csv_outputs(run_dir, outputs)
    (run_dir / "summary_report.md").write_text("# Summary\n", encoding="utf-8")

    metadata_path = write_run_metadata(run_dir, config, Path("configs/demo.yaml"), outputs)
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

    assert metadata["project"] == "PyRiskLab"
    assert metadata["schema_version"] == reporting.METADATA_SCHEMA_VERSION
    assert metadata["run_name"] == "demo_run"
    assert metadata["seed"] == 42
    assert metadata["python_version"]
    assert metadata["platform"]
    assert metadata["simulation_only"] is True
    assert metadata["benchmark_settings"] == {
        "enabled": config.benchmark.enabled,
        "num_prices": config.benchmark.num_prices,
        "seed": config.benchmark.seed,
        "tolerance": config.benchmark.tolerance,
    }
    expected_digest = hashlib.sha256(Path("configs/demo.yaml").read_bytes()).hexdigest()
    assert metadata["config_sha256"] == expected_digest
    assert metadata["csv_row_counts"] == {"market_path.csv": 2, "trades.csv": 0}
    assert metadata["order_status_counts"] == {
        ORDER_STATUS_APPROVED: 0,
        ORDER_STATUS_BLOCKED: 0,
        ORDER_STATUS_SKIPPED: 0,
    }
    assert set(metadata["expected_artifacts"]) == reporting.EXPECTED_ARTIFACT_NAMES
    assert "run_metadata.json" in metadata["generated_artifacts"]
    assert "summary_report.md" in metadata["generated_artifacts"]
    assert metadata["generated_artifact_sizes_bytes"]["market_path.csv"] > 0
    assert metadata["generated_artifact_sizes_bytes"]["trades.csv"] > 0
    assert metadata["generated_artifact_sizes_bytes"]["run_metadata.json"] > 0


def test_run_metadata_records_order_audit_counts(tmp_path):
    run_dir = prepare_output_dir(tmp_path, "demo")
    config = load_config("configs/demo.yaml")
    outputs = {
        "orders.csv": pd.DataFrame(
            {
                ORDER_STATUS_COLUMN: [
                    ORDER_STATUS_APPROVED,
                    ORDER_STATUS_BLOCKED,
                    ORDER_STATUS_BLOCKED,
                    ORDER_STATUS_SKIPPED,
                ]
            }
        ),
    }

    metadata_path = write_run_metadata(run_dir, config, Path("configs/demo.yaml"), outputs)
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

    assert metadata["order_status_counts"] == {
        ORDER_STATUS_APPROVED: 1,
        ORDER_STATUS_BLOCKED: 2,
        ORDER_STATUS_SKIPPED: 1,
    }


def test_run_metadata_config_hash_failure_raises_run_error(tmp_path):
    run_dir = prepare_output_dir(tmp_path, "demo")
    config = load_config("configs/demo.yaml")
    outputs = {"market_path.csv": pd.DataFrame({"step": [0]})}

    with pytest.raises(RunError, match="could not read config file"):
        write_run_metadata(run_dir, config, tmp_path / "missing.yaml", outputs)


def test_run_metadata_non_dataframe_output_raises_reporting_error(tmp_path):
    run_dir = prepare_output_dir(tmp_path, "demo")
    config = load_config("configs/demo.yaml")

    with pytest.raises(ReportingError, match="market_path.csv"):
        write_run_metadata(run_dir, config, Path("configs/demo.yaml"), {"market_path.csv": []})


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


def test_summary_report_rejects_nonnumeric_summary_values(tmp_path):
    run_dir = prepare_output_dir(tmp_path, "demo")
    config = load_config("configs/demo.yaml")
    outputs = {
        "market_path.csv": pd.DataFrame({"underlying_price": [100.0, 101.0]}),
        "pricing_history.csv": pd.DataFrame({"option_price": ["bad-price", 4.0]}),
        "trades.csv": pd.DataFrame(columns=["step", "symbol"]),
        "portfolio_history.csv": pd.DataFrame({"total_value": [10000.0], "drawdown_pct": [0.0]}),
        "risk_events.csv": pd.DataFrame(columns=["step", "reason"]),
        "benchmark.csv": pd.DataFrame(),
    }

    with pytest.raises(ReportingError, match="pricing_history.option_price"):
        write_summary_report(run_dir, config, outputs)


def test_summary_report_rejects_non_dataframe_optional_outputs(tmp_path):
    run_dir = prepare_output_dir(tmp_path, "demo")
    config = load_config("configs/demo.yaml")
    outputs = {
        "market_path.csv": pd.DataFrame({"underlying_price": [100.0, 101.0]}),
        "pricing_history.csv": pd.DataFrame({"option_price": [3.0, 4.0]}),
        "signals.csv": [{"step": 0, "action": "BUY"}],
        "trades.csv": pd.DataFrame(columns=["step", "symbol"]),
        "portfolio_history.csv": pd.DataFrame({"total_value": [10000.0], "drawdown_pct": [0.0]}),
        "risk_events.csv": pd.DataFrame(columns=["step", "reason"]),
        "benchmark.csv": pd.DataFrame(),
    }

    with pytest.raises(ReportingError, match="signals.csv"):
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
        "benchmark.csv": pd.DataFrame(
            {
                "method": ["python_loop"],
                "num_prices": [1000],
                "runtime_seconds": [0.2],
                "speedup_vs_loop": [1.0],
                "max_abs_error_vs_loop": [0.0],
                "passed_equivalence_check": [True],
            }
        ),
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


def test_summary_report_rejects_nonnumeric_benchmark_speedup(tmp_path):
    run_dir = prepare_output_dir(tmp_path, "demo")
    config = load_config("configs/demo.yaml")
    outputs = {
        "market_path.csv": pd.DataFrame({"underlying_price": [100.0, 101.0]}),
        "pricing_history.csv": pd.DataFrame({"option_price": [3.0, 4.0]}),
        "trades.csv": pd.DataFrame(columns=["step", "symbol"]),
        "portfolio_history.csv": pd.DataFrame({"total_value": [10000.0], "drawdown_pct": [0.0]}),
        "risk_events.csv": pd.DataFrame(columns=["step", "reason"]),
        "benchmark.csv": pd.DataFrame(
            {
                "method": ["python_loop", "numpy_vectorized"],
                "num_prices": [1000, 1000],
                "runtime_seconds": [0.2, 0.01],
                "speedup_vs_loop": [1.0, "bad-speedup"],
                "max_abs_error_vs_loop": [0.0, 1e-10],
                "passed_equivalence_check": [True, True],
            }
        ),
    }

    with pytest.raises(ReportingError, match="benchmark.speedup_vs_loop"):
        write_summary_report(run_dir, config, outputs)


def test_summary_report_rejects_failed_benchmark_equivalence(tmp_path):
    run_dir = prepare_output_dir(tmp_path, "demo")
    config = load_config("configs/demo.yaml")
    outputs = {
        "market_path.csv": pd.DataFrame({"underlying_price": [100.0, 101.0]}),
        "pricing_history.csv": pd.DataFrame({"option_price": [3.0, 4.0]}),
        "trades.csv": pd.DataFrame(columns=["step", "symbol"]),
        "portfolio_history.csv": pd.DataFrame({"total_value": [10000.0], "drawdown_pct": [0.0]}),
        "risk_events.csv": pd.DataFrame(columns=["step", "reason"]),
        "benchmark.csv": pd.DataFrame(
            {
                "method": ["python_loop", "numpy_vectorized"],
                "num_prices": [1000, 1000],
                "runtime_seconds": [0.2, 0.01],
                "speedup_vs_loop": [1.0, 20.0],
                "max_abs_error_vs_loop": [0.0, 1e-3],
                "passed_equivalence_check": [True, False],
            }
        ),
    }

    with pytest.raises(ReportingError, match="equivalence check"):
        write_summary_report(run_dir, config, outputs)


def test_summary_report_artifact_listing_failure_raises_run_error(tmp_path, monkeypatch):
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

    def fail_iterdir(_self):
        raise OSError("directory cannot be listed")

    monkeypatch.setattr(Path, "iterdir", fail_iterdir)

    with pytest.raises(RunError, match="could not list generated artifacts"):
        write_summary_report(run_dir, config, outputs)


def test_expected_artifact_verifier_names_missing_outputs(tmp_path):
    run_dir = prepare_output_dir(tmp_path, "demo")
    for filename in reporting.EXPECTED_ARTIFACT_NAMES - {"drawdown.png"}:
        (run_dir / filename).write_text("content", encoding="utf-8")

    with pytest.raises(RunError, match="drawdown.png"):
        reporting._verify_expected_artifacts(run_dir)


def test_expected_artifact_verifier_does_not_count_pending_metadata(tmp_path):
    run_dir = prepare_output_dir(tmp_path, "demo")
    for filename in reporting.EXPECTED_ARTIFACT_NAMES - {"run_metadata.json"}:
        (run_dir / filename).write_text("content", encoding="utf-8")

    with pytest.raises(RunError, match="run_metadata.json"):
        reporting._verify_expected_artifacts(run_dir)


def test_expected_artifact_verifier_rejects_empty_outputs(tmp_path):
    run_dir = prepare_output_dir(tmp_path, "demo")
    for filename in reporting.EXPECTED_ARTIFACT_NAMES:
        (run_dir / filename).write_text("content", encoding="utf-8")
    (run_dir / "benchmark.csv").write_text("", encoding="utf-8")

    with pytest.raises(RunError, match="benchmark.csv"):
        reporting._verify_expected_artifacts(run_dir)
