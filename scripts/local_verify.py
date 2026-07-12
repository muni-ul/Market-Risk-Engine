from __future__ import annotations

import argparse
import subprocess
import sys
from collections.abc import Sequence


Command = tuple[str, list[str]]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run PyRiskLab's local reviewer validation commands."
    )
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip the pytest suite.",
    )
    parser.add_argument(
        "--skip-lint",
        action="store_true",
        help="Skip ruff linting.",
    )
    parser.add_argument(
        "--skip-demo",
        action="store_true",
        help="Skip the main demo run.",
    )
    parser.add_argument(
        "--skip-risk-demo",
        action="store_true",
        help="Skip the risk-stress demo run.",
    )
    parser.add_argument(
        "--keep-going",
        action="store_true",
        help="Continue running later checks after a command fails.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Print selected commands without running them.",
    )
    parser.add_argument(
        "--only",
        choices=("pytest", "ruff", "demo", "risk-demo"),
        action="append",
        help=(
            "Run only the named check. May be passed more than once; skip flags "
            "still apply."
        ),
    )
    return parser


def planned_commands(args: argparse.Namespace) -> list[Command]:
    selected = set(args.only or ())
    commands: list[Command] = []
    if not args.skip_tests and (not selected or "pytest" in selected):
        commands.append(("pytest", [sys.executable, "-m", "pytest"]))
    if not args.skip_lint and (not selected or "ruff" in selected):
        commands.append(("ruff", [sys.executable, "-m", "ruff", "check", "."]))
    if not args.skip_demo and (not selected or "demo" in selected):
        commands.append(
            (
                "demo run",
                [
                    sys.executable,
                    "-m",
                    "pyrisklab",
                    "run",
                    "--config",
                    "configs/demo.yaml",
                    "--overwrite",
                ],
            )
        )
    if not args.skip_risk_demo and (not selected or "risk-demo" in selected):
        commands.append(
            (
                "risk-stress demo",
                [
                    sys.executable,
                    "-m",
                    "pyrisklab",
                    "run",
                    "--config",
                    "configs/risk_stress.yaml",
                    "--overwrite",
                ],
            )
        )
    return commands


def run_commands(commands: Sequence[Command], *, keep_going: bool) -> int:
    failures: list[str] = []
    for index, (label, command) in enumerate(commands, start=1):
        print(f"[{index}/{len(commands)}] Running {label}: {' '.join(command)}")
        result = subprocess.run(command, check=False)
        if result.returncode != 0:
            failures.append(label)
            print(f"{label} failed with exit code {result.returncode}.")
            if not keep_going:
                return result.returncode

    if failures:
        print("Failed checks: " + ", ".join(failures))
        return 1

    print("All selected local verification commands completed successfully.")
    return 0


def print_commands(commands: Sequence[Command]) -> None:
    for index, (label, command) in enumerate(commands, start=1):
        print(f"[{index}/{len(commands)}] {label}: {' '.join(command)}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    commands = planned_commands(args)
    if not commands:
        print("No checks selected.")
        return 0
    if args.list:
        print_commands(commands)
        return 0
    return run_commands(commands, keep_going=args.keep_going)


if __name__ == "__main__":
    raise SystemExit(main())
