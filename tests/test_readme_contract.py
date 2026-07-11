from __future__ import annotations


def test_readme_contains_required_demo_and_scope_language():
    with open("README.md", encoding="utf-8") as readme_file:
        readme = readme_file.read()
    assert "python -m pyrisklab run --config configs/demo.yaml --overwrite" in readme
    assert "pytest" in readme
    assert "ruff check ." in readme
    assert "not a trading bot" in readme
    assert "does not connect to real brokerage accounts" in readme
    assert "results/demo_run/" in readme
    assert "docs/SAMPLE_OUTPUT.md" in readme
    assert "docs/sample_outputs/" in readme
    assert "docs/sample_outputs/chart_artifacts.md" in readme
    assert "docs/PORTFOLIO_CASE_STUDY.md" in readme
    assert "results/demo_run/greeks.png" in readme
    assert "expected artifact names" in readme
    assert "Generated outputs are not required before setup" in readme
    assert "## Troubleshooting" in readme
    assert "pip install -e ." in readme
    assert "ConfigError: market.volatility must be >= 0" in readme


def test_sample_output_docs_are_linked_and_present():
    with open("docs/sample_outputs/README.md", encoding="utf-8") as sample_index_file:
        sample_index = sample_index_file.read()

    for filename in (
        "summary_report_excerpt.md",
        "csv_contracts.md",
        "chart_artifacts.md",
        "run_metadata_example.md",
    ):
        assert filename in sample_index
        with open(f"docs/sample_outputs/{filename}", encoding="utf-8") as sample_file:
            assert sample_file.read().strip()
