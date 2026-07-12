"""Repo-root launcher shim for running PyRiskLab without editable install."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

__path__ = [str(Path(__file__).resolve().parent)]
_SRC_PACKAGE = Path(__file__).resolve().parents[1] / "src" / "pyrisklab"
if _SRC_PACKAGE.exists():
    __path__.append(str(_SRC_PACKAGE))

from ._version import __version__  # noqa: E402
from .models import RunResult  # noqa: E402

ProgressCallback = Callable[[str], None]

__all__ = ["__version__", "ProgressCallback", "run_simulation"]


def run_simulation(
    config_path: str | Path,
    overwrite: bool = False,
    progress: ProgressCallback | None = None,
) -> RunResult:
    """Run the local simulation pipeline from a config path.

    This mirrors the installed package API while keeping the repo-root launcher
    lightweight for `python -m pyrisklab ...` usage.
    """
    from .pipeline import run_simulation as _run_simulation

    return _run_simulation(config_path, overwrite=overwrite, progress=progress)
