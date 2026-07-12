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
    assert "docs/sample_outputs/risk_stress_demo.md" in readme
    assert "docs/REVIEWER_GUIDE.md" in readme
    assert "docs/PORTFOLIO_CASE_STUDY.md" in readme
    assert "docs/FINAL_REVIEW_CHECKLIST.md" in readme
    assert "## Reviewer Checklist" in readme
    assert "risk/execution audit counts" in readme
    assert "config SHA-256" in readme
    assert "results/demo_run/greeks.png" in readme
    assert "expected artifact names" in readme
    assert "approved, blocked, and skipped simulated orders" in readme
    assert "order status counts" in readme
    assert "benchmark.enabled" in readme
    assert "benchmark settings" in readme
    assert "pricing assumptions" in readme
    assert "--debug" in readme
    assert "traceback" in readme
    assert "Generated outputs are not required before setup" in readme
    assert "## Troubleshooting" in readme
    assert "pip install -e ." in readme
    assert "ConfigError: market.volatility must be >= 0" in readme
    assert "## Resume And Interview Framing" in readme
    assert "local Python engineering project" in readme
    assert "vectorized NumPy pricing" in readme
    assert "repository hygiene" in readme


def test_sample_output_docs_are_linked_and_present():
    with open("docs/sample_outputs/README.md", encoding="utf-8") as sample_index_file:
        sample_index = sample_index_file.read()

    for filename in (
        "summary_report_excerpt.md",
        "csv_contracts.md",
        "chart_artifacts.md",
        "run_metadata_example.md",
        "risk_stress_demo.md",
    ):
        assert filename in sample_index
        with open(f"docs/sample_outputs/{filename}", encoding="utf-8") as sample_file:
            assert sample_file.read().strip()

    with open("docs/sample_outputs/summary_report_excerpt.md", encoding="utf-8") as report_file:
        report_excerpt = report_file.read()
        assert "benchmark.enabled is false" in report_excerpt
        assert "Risk-free rate" in report_excerpt
        assert "Volatility" in report_excerpt
        assert report_excerpt.index("## Strategy Signals") < report_excerpt.index("## Portfolio Results")
        assert report_excerpt.index("## Greeks") < report_excerpt.index("## Strategy Signals")
        assert "Buy when delta is below" in report_excerpt
        assert "Minimum steps between trades" in report_excerpt
        assert "Final cash" in report_excerpt
        assert "Peak portfolio value" in report_excerpt
        assert "## Run Metadata" in report_excerpt
        assert "Config SHA-256 digest" in report_excerpt
        assert "## Fake Execution" in report_excerpt
        assert "Fill model" in report_excerpt
        assert "Contract multiplier" in report_excerpt
        assert "## Risk Events" in report_excerpt
        assert "Max trade notional" in report_excerpt
        assert "Stop trading on breach" in report_excerpt
        assert "## Limitations" in report_excerpt
        assert report_excerpt.index("## Fake Execution") < report_excerpt.index("## Risk Events")
        assert report_excerpt.index("## Risk Events") < report_excerpt.index("## Benchmark")
    with open("docs/sample_outputs/run_metadata_example.md", encoding="utf-8") as metadata_file:
        metadata_doc = metadata_file.read()
        assert "order_status_counts" in metadata_doc
        assert "schema_version" in metadata_doc
        assert '"schema_version": 3' in metadata_doc
        assert "config_sha256" in metadata_doc
        assert "benchmark_settings" in metadata_doc
        assert "generated_artifact_sizes_bytes" in metadata_doc
    with open("docs/sample_outputs/risk_stress_demo.md", encoding="utf-8") as risk_demo_file:
        risk_demo = risk_demo_file.read()
        assert "blocked simulated order counts" in risk_demo
        assert "order_status_counts" in risk_demo
    with open("docs/SAMPLE_OUTPUT.md", encoding="utf-8") as sample_output_file:
        sample_output = sample_output_file.read()
        assert "order status counts" in sample_output
        assert "`status` and `risk_reason` audit columns" in sample_output
        assert "benchmark settings" in sample_output
        assert "generated artifact byte sizes" in sample_output
    with open("docs/PORTFOLIO_CASE_STUDY.md", encoding="utf-8") as case_study_file:
        case_study = case_study_file.read()
        assert "artifact byte sizes" in case_study
    with open("docs/INTERVIEW_NOTES.md", encoding="utf-8") as interview_file:
        interview_notes = interview_file.read()
        assert "config SHA-256" in interview_notes
        assert "docs/FINAL_REVIEW_CHECKLIST.md" in interview_notes
        assert "ready to discuss" in interview_notes
    with open("docs/FINAL_REVIEW_CHECKLIST.md", encoding="utf-8") as checklist_file:
        checklist = checklist_file.read()
        assert "pytest" in checklist
        assert "ruff check ." in checklist
        assert "python -m pyrisklab run --config configs/demo.yaml --overwrite" in checklist
        assert "Simulation-only language" in checklist
        assert "generated_artifact_sizes_bytes" in checklist
    with open("docs/sample_outputs/csv_contracts.md", encoding="utf-8") as contracts_file:
        csv_contracts = contracts_file.read()
        assert "`benchmark.enabled` is false" in csv_contracts
        assert "`risk_free_rate`" in csv_contracts
        assert "`volatility`" in csv_contracts
        assert "`APPROVED`" in csv_contracts
        assert "`BLOCKED`" in csv_contracts
        assert "`SKIPPED`" in csv_contracts


def test_reviewer_guide_contains_demo_and_scope_contracts():
    with open("docs/REVIEWER_GUIDE.md", encoding="utf-8") as reviewer_file:
        reviewer_guide = reviewer_file.read()

    assert "python -m pyrisklab run --config configs/demo.yaml --overwrite" in reviewer_guide
    assert "python -m pyrisklab run --config configs/risk_stress.yaml --overwrite" in reviewer_guide
    assert "summary_report.md" in reviewer_guide
    assert "run_metadata.json" in reviewer_guide
    assert "docs/FINAL_REVIEW_CHECKLIST.md" in reviewer_guide
    assert "benchmark settings" in reviewer_guide
    assert "generated artifact byte sizes" in reviewer_guide
    assert "benchmark.csv" in reviewer_guide
    assert "pytest" in reviewer_guide
    assert "ruff check ." in reviewer_guide
    assert "not a trading bot" in reviewer_guide
