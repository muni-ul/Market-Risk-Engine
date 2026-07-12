from __future__ import annotations

from pyrisklab.reporting import EXPECTED_ARTIFACT_NAMES


def test_readme_contains_required_demo_and_scope_language():
    with open("README.md", encoding="utf-8") as readme_file:
        readme = readme_file.read()
    assert "python -m pyrisklab run --config configs/demo.yaml --overwrite" in readme
    assert "pytest" in readme
    assert "ruff check ." in readme
    assert "python scripts/local_verify.py" in readme
    assert "python scripts/local_verify.py --list" in readme
    assert "python scripts/local_verify.py --only ruff --only demo" in readme
    assert "not a trading bot" in readme
    assert "does not connect to real brokerage accounts" in readme
    assert "results/demo_run/" in readme
    assert "docs/SAMPLE_OUTPUT.md" in readme
    assert "docs/sample_outputs/" in readme
    assert "docs/sample_outputs/artifact_manifest.md" in readme
    assert "docs/sample_outputs/chart_artifacts.md" in readme
    assert "docs/sample_outputs/risk_stress_demo.md" in readme
    assert "docs/README.md" in readme
    assert "docs/PROJECT_STATUS.md" in readme
    assert "docs/REVIEWER_GUIDE.md" in readme
    assert "docs/REQUIREMENTS_TRACEABILITY.md" in readme
    assert "docs/DEMO_WALKTHROUGH.md" in readme
    assert "docs/API_REFERENCE.md" in readme
    assert "docs/CONFIG_REFERENCE.md" in readme
    assert "docs/VALIDATION_NOTES.md" in readme
    assert "docs/PERFORMANCE_NOTES.md" in readme
    assert "docs/DEBUGGING_GUIDE.md" in readme
    assert "docs/TESTING_STRATEGY.md" in readme
    assert "docs/PORTFOLIO_CASE_STUDY.md" in readme
    assert "docs/RESUME_SNIPPETS.md" in readme
    assert "docs/FINAL_REVIEW_CHECKLIST.md" in readme
    assert "CHANGELOG.md" in readme
    assert "CONTRIBUTING.md" in readme
    assert "SECURITY.md" in readme
    assert "issue tracker" in readme
    assert "## Reviewer Checklist" in readme
    assert "```mermaid" in readme
    assert "Simulation pipeline" in readme
    assert "Loop-vs-NumPy benchmark" in readme
    assert "py.typed" in readme
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
    assert 'pip install -e ".[dev]"' in readme
    assert "ConfigError: market.volatility must be >= 0" in readme
    assert "## Resume And Interview Framing" in readme
    assert "local Python engineering project" in readme
    assert "vectorized NumPy pricing" in readme
    assert "repository hygiene" in readme
    assert "## License" in readme
    assert "MIT License" in readme
    assert "## Future Improvements" in readme
    assert "small portfolio of contracts" in readme
    assert "simulation-only" in readme


def test_sample_output_docs_are_linked_and_present():
    with open("docs/sample_outputs/README.md", encoding="utf-8") as sample_index_file:
        sample_index = sample_index_file.read()
        assert "docs/FINAL_REVIEW_CHECKLIST.md" in sample_index
        assert "full expected artifact set" in sample_index

    for filename in (
        "summary_report_excerpt.md",
        "csv_contracts.md",
        "chart_artifacts.md",
        "artifact_manifest.md",
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
        assert "config SHA-256 digest" in case_study
        assert "benchmark settings" in case_study
        assert "artifact byte sizes" in case_study
        assert "auditable run metadata" in case_study
        assert "small portfolio of contracts" in case_study
        assert "simulation-only" in case_study
    with open("docs/sample_outputs/artifact_manifest.md", encoding="utf-8") as manifest_file:
        artifact_manifest = manifest_file.read()
        assert "Generated Artifact Manifest" in artifact_manifest
        assert "Reviewer signal" in artifact_manifest
        for artifact_name in EXPECTED_ARTIFACT_NAMES:
            assert artifact_name in artifact_manifest
    with open("docs/INTERVIEW_NOTES.md", encoding="utf-8") as interview_file:
        interview_notes = interview_file.read()
        assert "config SHA-256" in interview_notes
        assert "docs/FINAL_REVIEW_CHECKLIST.md" in interview_notes
        assert "docs/DEMO_WALKTHROUGH.md" in interview_notes
        assert "docs/RESUME_SNIPPETS.md" in interview_notes
        assert "ready to discuss" in interview_notes
    with open("docs/FINAL_REVIEW_CHECKLIST.md", encoding="utf-8") as checklist_file:
        checklist = checklist_file.read()
        assert "pytest" in checklist
        assert "ruff check ." in checklist
        assert "python scripts/local_verify.py" in checklist
        assert "--list" in checklist
        assert "--only ruff --only demo" in checklist
        assert "python -m pyrisklab run --config configs/demo.yaml --overwrite" in checklist
        assert "docs/README.md" in checklist
        assert "CHANGELOG.md" in checklist
        assert "CONTRIBUTING.md" in checklist
        assert "SECURITY.md" in checklist
        assert "docs/API_REFERENCE.md" in checklist
        assert "docs/PROJECT_STATUS.md" in checklist
        assert "docs/REQUIREMENTS_TRACEABILITY.md" in checklist
        assert "docs/DEMO_WALKTHROUGH.md" in checklist
        assert "docs/CONFIG_REFERENCE.md" in checklist
        assert "docs/VALIDATION_NOTES.md" in checklist
        assert "docs/PERFORMANCE_NOTES.md" in checklist
        assert "docs/DEBUGGING_GUIDE.md" in checklist
        assert "docs/TESTING_STRATEGY.md" in checklist
        assert "docs/RESUME_SNIPPETS.md" in checklist
        assert "docs/sample_outputs/artifact_manifest.md" in checklist
        assert "Simulation-only language" in checklist
        assert "config_used.yaml" in checklist
        assert "pricing_history.csv" in checklist
        assert "signals.csv" in checklist
        assert "generated_artifact_sizes_bytes" in checklist
        for artifact_name in EXPECTED_ARTIFACT_NAMES:
            assert artifact_name in checklist
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
    assert "docs/PROJECT_STATUS.md" in reviewer_guide
    assert "docs/REQUIREMENTS_TRACEABILITY.md" in reviewer_guide
    assert "docs/CONFIG_REFERENCE.md" in reviewer_guide
    assert "docs/VALIDATION_NOTES.md" in reviewer_guide
    assert "docs/DEMO_WALKTHROUGH.md" in reviewer_guide
    assert "docs/FINAL_REVIEW_CHECKLIST.md" in reviewer_guide
    assert "docs/sample_outputs/artifact_manifest.md" in reviewer_guide
    assert "benchmark settings" in reviewer_guide
    assert "generated artifact byte sizes" in reviewer_guide
    assert "benchmark.csv" in reviewer_guide
    assert "pytest" in reviewer_guide
    assert "ruff check ." in reviewer_guide
    assert "not a trading bot" in reviewer_guide


def test_config_reference_documents_demo_settings():
    with open("docs/CONFIG_REFERENCE.md", encoding="utf-8") as config_reference_file:
        config_reference = config_reference_file.read()

    assert "configs/demo.yaml" in config_reference
    assert "configs/risk_stress.yaml" in config_reference
    assert "simulation-only" in config_reference
    for section in ("market", "option", "strategy", "execution", "risk", "benchmark"):
        assert f"## `{section}`" in config_reference
    for field in ("run_name", "seed", "output_dir", "contract_multiplier", "max_trade_notional"):
        assert f"`{field}`" in config_reference


def test_docs_index_links_reviewer_and_engineering_docs():
    with open("docs/README.md", encoding="utf-8") as docs_index_file:
        docs_index = docs_index_file.read()

    assert "PyRiskLab Documentation Index" in docs_index
    for doc_name in (
        "../CHANGELOG.md",
        "../CONTRIBUTING.md",
        "../SECURITY.md",
        "../.github/ISSUE_TEMPLATE/bug_report.md",
        "../.github/ISSUE_TEMPLATE/feature_request.md",
        "../.github/PULL_REQUEST_TEMPLATE.md",
        "PROJECT_STATUS.md",
        "REVIEWER_GUIDE.md",
        "REQUIREMENTS_TRACEABILITY.md",
        "DEMO_WALKTHROUGH.md",
        "SAMPLE_OUTPUT.md",
        "FINAL_REVIEW_CHECKLIST.md",
        "ARCHITECTURE.md",
        "API_REFERENCE.md",
        "CONFIG_REFERENCE.md",
        "VALIDATION_NOTES.md",
        "PERFORMANCE_NOTES.md",
        "DEBUGGING_GUIDE.md",
        "TESTING_STRATEGY.md",
        "../scripts/local_verify.py",
        "PORTFOLIO_CASE_STUDY.md",
        "INTERVIEW_NOTES.md",
        "RESUME_SNIPPETS.md",
        "sample_outputs/artifact_manifest.md",
    ):
        assert doc_name in docs_index
    assert "results/.gitkeep" in docs_index


def test_project_status_summarizes_implemented_scope_without_overclaiming():
    with open("docs/PROJECT_STATUS.md", encoding="utf-8") as status_file:
        project_status = status_file.read()

    assert "PyRiskLab Project Status" in project_status
    assert "Implemented" in project_status
    assert "User-Run Verification" in project_status
    assert "bug report, feature request, and pull request templates" in project_status
    assert "python -m pyrisklab run --config configs/demo.yaml --overwrite" in project_status
    assert "python scripts/local_verify.py --list" in project_status
    assert "python scripts/local_verify.py --only ruff --only demo" in project_status
    assert "Generated run outputs are intentionally not committed" in project_status
    assert "Not Included" in project_status
    assert "live market data" in project_status
    assert "brokerage" in project_status


def test_requirements_traceability_maps_original_requirements_to_evidence():
    with open("docs/REQUIREMENTS_TRACEABILITY.md", encoding="utf-8") as traceability_file:
        traceability = traceability_file.read()

    assert "PyRiskLab Requirements Traceability" in traceability
    assert "python -m pyrisklab run --config configs/demo.yaml --overwrite" in traceability
    assert "src/pyrisklab/" in traceability
    assert "configs/demo.yaml" in traceability
    assert "docs/CONFIG_REFERENCE.md" in traceability
    assert "docs/TESTING_STRATEGY.md" in traceability
    assert "docs/PERFORMANCE_NOTES.md" in traceability
    assert "docs/FINAL_REVIEW_CHECKLIST.md" in traceability
    assert "python scripts/local_verify.py --list" in traceability
    assert "python scripts/local_verify.py --only ruff --only demo" in traceability
    assert "benchmark.csv" in traceability
    assert "no live data" in traceability
    assert "no brokerage integration" in traceability


def test_resume_snippets_keep_project_positioning_software_focused():
    with open("docs/RESUME_SNIPPETS.md", encoding="utf-8") as snippets_file:
        resume_snippets = snippets_file.read()

    assert "PyRiskLab Resume Snippets" in resume_snippets
    assert "Software engineering" in resume_snippets or "software engineering" in resume_snippets
    assert "CLI automation" in resume_snippets
    assert "deterministic YAML configs" in resume_snippets
    assert "NumPy/SciPy numerical computation" in resume_snippets
    assert "pytest coverage" in resume_snippets
    assert "benchmark reporting" in resume_snippets
    assert "reproducible CSV/PNG/Markdown artifacts" in resume_snippets
    assert "What Not To Say" in resume_snippets
    assert "trading bot" in resume_snippets


def test_validation_notes_explain_defensive_error_contracts():
    with open("docs/VALIDATION_NOTES.md", encoding="utf-8") as validation_file:
        validation_notes = validation_file.read()

    assert "PyRiskLab Validation Notes" in validation_notes
    assert "PyRiskLabError" in validation_notes
    assert "ConfigError" in validation_notes
    assert "MarketSimulationError" in validation_notes
    assert "PricingError" in validation_notes
    assert "GreeksError" in validation_notes
    assert "StrategyError" in validation_notes
    assert "ExecutionError" in validation_notes
    assert "PortfolioError" in validation_notes
    assert "RiskError" in validation_notes
    assert "ReportingError" in validation_notes
    assert "BenchmarkError" in validation_notes
    assert "RunError" in validation_notes
    assert "non-finite" in validation_notes
    assert "Selling more contracts" in validation_notes
    assert "Blocked simulated orders" in validation_notes
    assert "--debug" in validation_notes


def test_architecture_doc_contains_reviewable_data_flow_diagram():
    with open("docs/ARCHITECTURE.md", encoding="utf-8") as architecture_file:
        architecture = architecture_file.read()

    assert "PyRiskLab Architecture" in architecture
    assert "```mermaid" in architecture
    assert "flowchart TD" in architecture
    assert "configs/demo.yaml" in architecture
    assert "config.py validates YAML" in architecture
    assert "market.py synthetic path" in architecture
    assert "pricing.py Black-Scholes" in architecture
    assert "greeks.py sensitivities" in architecture
    assert "risk.py validation" in architecture
    assert "benchmark.py loop vs NumPy" in architecture
    assert "reporting.py CSV, PNG, Markdown, JSON" in architecture
    assert "results/<run_name>/" in architecture


def test_demo_walkthrough_documents_screenshot_and_scope_path():
    with open("docs/DEMO_WALKTHROUGH.md", encoding="utf-8") as demo_file:
        demo_walkthrough = demo_file.read()

    assert "PyRiskLab Demo Walkthrough" in demo_walkthrough
    assert "python -m pyrisklab run --config configs/demo.yaml --overwrite" in demo_walkthrough
    assert "python -m pyrisklab run --config configs/risk_stress.yaml --overwrite" in demo_walkthrough
    assert "python scripts/local_verify.py" in demo_walkthrough
    assert "python scripts/local_verify.py --list" in demo_walkthrough
    assert "python scripts/local_verify.py --only ruff --only demo" in demo_walkthrough
    assert "Screenshot Targets" in demo_walkthrough
    assert "summary_report.md" in demo_walkthrough
    assert "portfolio_value.png" in demo_walkthrough
    assert "drawdown.png" in demo_walkthrough
    assert "benchmark.csv" in demo_walkthrough
    assert "run_metadata.json" in demo_walkthrough
    assert "simulation only" in demo_walkthrough
    assert "no live market data" in demo_walkthrough
    assert "no brokerage integration" in demo_walkthrough


def test_performance_notes_explain_benchmark_contract():
    with open("docs/PERFORMANCE_NOTES.md", encoding="utf-8") as performance_file:
        performance_notes = performance_file.read()

    assert "PyRiskLab Performance Notes" in performance_notes
    assert "python_loop" in performance_notes
    assert "numpy_vectorized" in performance_notes
    assert "benchmark.csv" in performance_notes
    assert "benchmark.enabled" in performance_notes
    assert "benchmark.num_prices" in performance_notes
    assert "passed_equivalence_check" in performance_notes
    assert "max_abs_error_vs_loop" in performance_notes
    assert "machine-dependent" in performance_notes
    assert "Numba" in performance_notes


def test_changelog_summarizes_version_one_mvp():
    with open("CHANGELOG.md", encoding="utf-8") as changelog_file:
        changelog = changelog_file.read()

    assert "0.1.0" in changelog
    assert "Version 1 MVP" in changelog
    assert "python -m pyrisklab run --config configs/demo.yaml --overwrite" in changelog
    assert "Loop-vs-vectorized NumPy" in changelog
    assert "Requirement traceability" in changelog
    assert "local verification helper" in changelog
    assert "project status summary" in changelog
    assert "resume snippets" in changelog
    assert "scoped GitHub issue/PR templates" in changelog
    assert "typed package marker" in changelog
    assert "Simulation only" in changelog
    assert "no live market data" in changelog


def test_contributing_documents_local_workflow_and_scope():
    with open("CONTRIBUTING.md", encoding="utf-8") as contributing_file:
        contributing = contributing_file.read()

    assert "pip install -e" in contributing
    assert "pytest" in contributing
    assert "ruff check ." in contributing
    assert "configs/risk_stress.yaml" in contributing
    assert "Do not add live market data" in contributing
    assert "results/.gitkeep" in contributing
    assert ".github/ISSUE_TEMPLATE/bug_report.md" in contributing
    assert ".github/ISSUE_TEMPLATE/feature_request.md" in contributing
    assert ".github/PULL_REQUEST_TEMPLATE.md" in contributing


def test_security_policy_documents_no_secrets_boundary():
    with open("SECURITY.md", encoding="utf-8") as security_file:
        security = security_file.read()

    assert "does not require accounts" in security
    assert "API keys" in security
    assert "broker credentials" in security
    assert "0.1.x" in security
    assert "Keep real `.env` files" in security
    assert "Do not add live brokerage integrations" in security


def test_api_reference_documents_module_surface():
    with open("docs/API_REFERENCE.md", encoding="utf-8") as api_reference_file:
        api_reference = api_reference_file.read()

    assert "PyRiskLab Module Reference" in api_reference
    assert "PEP 561" in api_reference
    assert "py.typed" in api_reference
    for module_name in (
        "cli.py",
        "pipeline.py",
        "config.py",
        "pricing.py",
        "greeks.py",
        "portfolio.py",
        "risk.py",
        "reporting.py",
    ):
        assert module_name in api_reference
    for public_name in (
        "run_simulation",
        "load_config",
        "black_scholes_price",
        "calculate_greeks",
        "run_pricing_benchmark",
    ):
        assert public_name in api_reference


def test_testing_strategy_documents_validation_map():
    with open("docs/TESTING_STRATEGY.md", encoding="utf-8") as testing_strategy_file:
        testing_strategy = testing_strategy_file.read()

    assert "PyRiskLab Testing Strategy" in testing_strategy
    assert "pytest" in testing_strategy
    assert "docs/VALIDATION_NOTES.md" in testing_strategy
    for test_file in (
        "test_config.py",
        "test_pricing.py",
        "test_greeks.py",
        "test_execution.py",
        "test_portfolio.py",
        "test_risk.py",
        "test_reporting.py",
        "test_pipeline_smoke.py",
    ):
        assert test_file in testing_strategy
    assert "No live-market" in testing_strategy
    assert "No profitability" in testing_strategy


def test_debugging_guide_documents_error_triage():
    with open("docs/DEBUGGING_GUIDE.md", encoding="utf-8") as debugging_guide_file:
        debugging_guide = debugging_guide_file.read()

    assert "PyRiskLab Debugging Guide" in debugging_guide
    assert "--debug" in debugging_guide
    assert "ConfigError" in debugging_guide
    assert "RunError" in debugging_guide
    assert "run_metadata.json" in debugging_guide
    assert "risk_events.csv" in debugging_guide
    assert "benchmark.csv" in debugging_guide
    assert "docs/CONFIG_REFERENCE.md" in debugging_guide
