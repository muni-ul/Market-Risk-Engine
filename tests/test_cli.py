from __future__ import annotations

from pathlib import Path

import pytest

from pyrisklab import cli
from pyrisklab.exceptions import ConfigError
from pyrisklab.models import RunResult


def test_help_includes_run_command(capsys):
    parser = cli.build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["--help"])
    output = capsys.readouterr().out
    assert "run" in output


def test_run_help_includes_config_flag(capsys):
    parser = cli.build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["run", "--help"])
    output = capsys.readouterr().out
    assert "--config" in output
    assert "--quiet" in output


def test_main_returns_nonzero_for_project_error(monkeypatch, capsys):
    def fail_run(config_path, overwrite=False, progress=None):
        raise ConfigError("config file not found: missing.yaml")

    monkeypatch.setattr(cli, "run_simulation", fail_run)

    assert cli.main(["run", "--config", "missing.yaml"]) == 1
    assert "ConfigError" in capsys.readouterr().out


def test_main_returns_zero_for_success(monkeypatch):
    def fake_run(config_path, overwrite=False, progress=None):
        if progress:
            progress("[1/7] Loading config...")
        return RunResult("demo_run", Path("results/demo_run"), Path(config_path), "completed")

    monkeypatch.setattr(cli, "run_simulation", fake_run)

    assert cli.main(["run", "--config", "configs/demo.yaml", "--overwrite"]) == 0


def test_quiet_suppresses_progress_messages(monkeypatch, capsys):
    def fake_run(config_path, overwrite=False, progress=None):
        assert progress is None
        return RunResult("demo_run", Path("results/demo_run"), Path(config_path), "completed")

    monkeypatch.setattr(cli, "run_simulation", fake_run)

    assert cli.main(["run", "--config", "configs/demo.yaml", "--quiet"]) == 0
    output = capsys.readouterr().out
    assert "[1/7]" not in output
    assert "Done. Results saved" in output
