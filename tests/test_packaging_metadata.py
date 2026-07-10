from __future__ import annotations

import tomllib

from pyrisklab import __version__
from pyrisklab._version import __version__ as runtime_version


def test_pyproject_declares_console_script_and_dependencies():
    with open("pyproject.toml", "rb") as pyproject_file:
        pyproject = tomllib.load(pyproject_file)

    project = pyproject["project"]
    assert project["scripts"]["pyrisklab"] == "pyrisklab.cli:main"
    assert {"numpy", "pandas", "scipy", "matplotlib", "PyYAML"}.issubset(project["dependencies"])
    assert {"pytest", "ruff"}.issubset(project["optional-dependencies"]["dev"])


def test_runtime_version_matches_package_metadata():
    with open("pyproject.toml", "rb") as pyproject_file:
        pyproject = tomllib.load(pyproject_file)

    assert __version__ == runtime_version == pyproject["project"]["version"]
