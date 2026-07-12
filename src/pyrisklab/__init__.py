"""PyRiskLab: local options-pricing and risk-simulation engine."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from ._version import __version__
from .models import RunResult

__all__ = ["__version__", "run_simulation"]


def run_simulation(
    config_path: str | Path,
    overwrite: bool = False,
    progress: Callable[[str], None] | None = None,
) -> RunResult:
    """Run the local simulation pipeline from a config path.

    The CLI remains the primary interface, but this lazy wrapper gives reviewers
    and extension code a small stable import surface without importing the full
    pipeline on a plain `import pyrisklab`.
    """
    from .pipeline import run_simulation as _run_simulation

    return _run_simulation(config_path, overwrite=overwrite, progress=progress)
