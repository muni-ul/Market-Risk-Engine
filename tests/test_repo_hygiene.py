from __future__ import annotations


def test_gitignore_protects_generated_and_local_artifacts():
    with open(".gitignore", encoding="utf-8") as gitignore_file:
        gitignore = gitignore_file.read()

    for pattern in (
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
    assert "future optional features" in env_example
