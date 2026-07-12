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
