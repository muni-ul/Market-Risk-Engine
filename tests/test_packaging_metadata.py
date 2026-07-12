from __future__ import annotations

import tomllib

import pyrisklab
from pyrisklab import __version__
from pyrisklab._version import __version__ as runtime_version


def test_pyproject_declares_console_script_and_dependencies():
    with open("pyproject.toml", "rb") as pyproject_file:
        pyproject = tomllib.load(pyproject_file)

    project = pyproject["project"]
    assert project["scripts"]["pyrisklab"] == "pyrisklab.cli:main"
    assert project["license"] == "MIT"
    assert {"simulation", "benchmark", "cli", "testing", "automation", "performance"}.issubset(
        project["keywords"]
    )
    assert "Development Status :: 4 - Beta" in project["classifiers"]
    assert "Environment :: Console" in project["classifiers"]
    assert "License :: OSI Approved :: MIT License" in project["classifiers"]
    assert "Programming Language :: Python :: 3.11" in project["classifiers"]
    assert "Programming Language :: Python :: 3.12" in project["classifiers"]
    assert "Topic :: Software Development :: Quality Assurance" in project["classifiers"]
    assert "Topic :: Software Development :: Testing" in project["classifiers"]
    assert "Topic :: Scientific/Engineering" in project["classifiers"]
    assert {"numpy", "pandas", "scipy", "matplotlib", "PyYAML"}.issubset(project["dependencies"])
    assert {"pytest", "ruff"}.issubset(project["optional-dependencies"]["dev"])
    assert project["urls"]["Repository"] == "https://github.com/muni-ul/Market-Risk-Engine"
    assert project["urls"]["Documentation"].endswith("/tree/main/docs")
    assert project["urls"]["Issues"].endswith("/issues")

    package_data = pyproject["tool"]["setuptools"]["package-data"]
    assert "py.typed" in package_data["pyrisklab"]


def test_runtime_version_matches_package_metadata():
    with open("pyproject.toml", "rb") as pyproject_file:
        pyproject = tomllib.load(pyproject_file)

    assert __version__ == runtime_version == pyproject["project"]["version"]


def test_package_root_exposes_stable_reviewer_surface():
    assert "ProgressCallback" in pyrisklab.__all__
    assert "run_simulation" in pyrisklab.__all__
    assert callable(pyrisklab.run_simulation)
    assert pyrisklab.ProgressCallback is not None


def test_package_declares_pep561_typed_marker():
    with open("src/pyrisklab/py.typed", encoding="utf-8") as typed_marker_file:
        typed_marker_file.read()
