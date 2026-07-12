from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType


def load_local_verify_module() -> ModuleType:
    script_path = Path("scripts/local_verify.py")
    spec = importlib.util.spec_from_file_location("local_verify", script_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def command_labels(commands: list[tuple[str, list[str]]]) -> list[str]:
    return [label for label, _ in commands]


def test_planned_commands_include_full_reviewer_sequence_by_default():
    local_verify = load_local_verify_module()
    parser = local_verify.build_parser()
    args = parser.parse_args([])

    commands = local_verify.planned_commands(args)

    assert command_labels(commands) == [
        "pytest",
        "ruff",
        "demo run",
        "risk-stress demo",
    ]
    assert commands[0][1] == [sys.executable, "-m", "pytest"]
    assert commands[1][1] == [sys.executable, "-m", "ruff", "check", "."]
    assert commands[2][1][-2:] == ["configs/demo.yaml", "--overwrite"]
    assert commands[3][1][-2:] == ["configs/risk_stress.yaml", "--overwrite"]


def test_only_filters_commands_without_running_them():
    local_verify = load_local_verify_module()
    parser = local_verify.build_parser()
    args = parser.parse_args(["--only", "ruff", "--only", "demo"])

    commands = local_verify.planned_commands(args)

    assert command_labels(commands) == ["ruff", "demo run"]


def test_skip_flags_still_apply_with_only_selection():
    local_verify = load_local_verify_module()
    parser = local_verify.build_parser()
    args = parser.parse_args(["--only", "demo", "--skip-demo"])

    assert local_verify.planned_commands(args) == []
