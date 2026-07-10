from __future__ import annotations

import tomllib


def test_pyproject_declares_console_script_and_dependencies():
    with open("pyproject.toml", "rb") as pyproject_file:
        pyproject = tomllib.load(pyproject_file)

    project = pyproject["project"]
    assert project["scripts"]["pyrisklab"] == "pyrisklab.cli:main"
    assert {"numpy", "pandas", "scipy", "matplotlib", "PyYAML"}.issubset(project["dependencies"])
    assert {"pytest", "ruff"}.issubset(project["optional-dependencies"]["dev"])
