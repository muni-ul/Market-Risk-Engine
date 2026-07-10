from __future__ import annotations

import argparse
import traceback

from pyrisklab.exceptions import PyRiskLabError
from pyrisklab.pipeline import run_simulation


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pyrisklab", description="Local options-pricing and risk-simulation engine.")
    subparsers = parser.add_subparsers(dest="command")
    run_parser = subparsers.add_parser("run", help="Run a complete local simulation.")
    run_parser.add_argument("--config", required=True, help="Path to a YAML run config.")
    run_parser.add_argument("--overwrite", action="store_true", help="Replace an existing run output folder.")
    run_parser.add_argument("--quiet", action="store_true", help="Only print final success or error messages.")
    run_parser.add_argument("--debug", action="store_true", help="Show traceback for expected project errors.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command != "run":
        parser.print_help()
        return 2

    try:
        progress = None if args.quiet else print
        result = run_simulation(args.config, overwrite=args.overwrite, progress=progress)
    except PyRiskLabError as exc:
        if args.debug:
            traceback.print_exc()
        else:
            print(f"{exc.__class__.__name__}: {exc}")
        return 1
    print(f"Done. Results saved to {result.output_path}/")
    return 0
