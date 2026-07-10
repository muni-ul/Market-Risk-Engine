from __future__ import annotations


def test_readme_contains_required_demo_and_scope_language():
    readme = open("README.md", encoding="utf-8").read()
    assert "python -m pyrisklab run --config configs/demo.yaml --overwrite" in readme
    assert "pytest" in readme
    assert "ruff check ." in readme
    assert "not a trading bot" in readme
    assert "does not connect to real brokerage accounts" in readme
    assert "results/demo_run/" in readme
