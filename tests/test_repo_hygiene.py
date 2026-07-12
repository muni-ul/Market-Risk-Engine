from __future__ import annotations


def test_gitignore_protects_generated_and_local_artifacts():
    with open(".gitignore", encoding="utf-8") as gitignore_file:
        gitignore = gitignore_file.read()

    for pattern in (
        ".venv/",
        "__pycache__/",
        ".pytest_cache/",
        ".ruff_cache/",
        "results/*",
        "!results/.gitkeep",
        "build/",
        "dist/",
        ".coverage",
        "htmlcov/",
        ".env",
    ):
        assert pattern in gitignore


def test_editorconfig_documents_basic_formatting_contract():
    with open(".editorconfig", encoding="utf-8") as editorconfig_file:
        editorconfig = editorconfig_file.read()

    assert "root = true" in editorconfig
    assert "charset = utf-8" in editorconfig
    assert "end_of_line = lf" in editorconfig
    assert "insert_final_newline = true" in editorconfig
    assert "indent_style = space" in editorconfig


def test_gitattributes_documents_line_endings_and_binary_artifacts():
    with open(".gitattributes", encoding="utf-8") as gitattributes_file:
        gitattributes = gitattributes_file.read()

    assert "* text=auto eol=lf" in gitattributes
    assert "*.py text eol=lf" in gitattributes
    assert "*.md text eol=lf" in gitattributes
    assert "*.yaml text eol=lf" in gitattributes
    assert "*.csv text eol=lf" in gitattributes
    assert "*.png binary" in gitattributes


def test_env_example_documents_no_required_secrets():
    with open(".env.example", encoding="utf-8") as env_example_file:
        env_example = env_example_file.read()

    assert "does not require secrets" in env_example
    assert "local configs" in env_example
    assert "deterministic seeds" in env_example


def test_repo_declares_license():
    with open("LICENSE", encoding="utf-8") as license_file:
        license_text = license_file.read()

    assert "MIT License" in license_text
    assert "Muni Ul" in license_text


def test_github_issue_template_keeps_scope_local():
    with open(".github/ISSUE_TEMPLATE/bug_report.md", encoding="utf-8") as template_file:
        bug_template = template_file.read()

    assert "python -m pyrisklab run --config configs/demo.yaml --overwrite" in bug_template
    assert "run_metadata.json" in bug_template
    assert "simulation-only" in bug_template
    assert "brokerage integration" in bug_template


def test_github_pull_request_template_keeps_review_reproducible():
    with open(".github/PULL_REQUEST_TEMPLATE.md", encoding="utf-8") as template_file:
        pr_template = template_file.read()

    assert "pytest" in pr_template
    assert "ruff check ." in pr_template
    assert "python -m pyrisklab run --config configs/demo.yaml --overwrite" in pr_template
    assert "python -m pyrisklab run --config configs/risk_stress.yaml --overwrite" in pr_template
    assert "results/demo_run/run_metadata.json" in pr_template
    assert "simulation-only" in pr_template


def test_local_verification_helper_documents_reviewer_commands():
    with open("scripts/local_verify.py", encoding="utf-8") as helper_file:
        helper = helper_file.read()

    assert "pytest" in helper
    assert "ruff" in helper
    assert "configs/demo.yaml" in helper
    assert "configs/risk_stress.yaml" in helper
    assert "--skip-tests" in helper
    assert "--skip-lint" in helper
    assert "--skip-demo" in helper
    assert "--skip-risk-demo" in helper
    assert "--keep-going" in helper
    assert "--list" in helper
    assert "print_commands" in helper

    with open("CONTRIBUTING.md", encoding="utf-8") as contributing_file:
        contributing = contributing_file.read()

    assert "python scripts/local_verify.py" in contributing
    assert "python scripts/local_verify.py --list" in contributing
