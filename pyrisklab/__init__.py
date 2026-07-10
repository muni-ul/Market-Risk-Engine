"""Repo-root launcher shim for running PyRiskLab without editable install."""

from pathlib import Path

__path__ = [str(Path(__file__).resolve().parent)]
_SRC_PACKAGE = Path(__file__).resolve().parents[1] / "src" / "pyrisklab"
if _SRC_PACKAGE.exists():
    __path__.append(str(_SRC_PACKAGE))

__version__ = "0.1.0"
