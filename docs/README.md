# PyRiskLab Documentation Index

Use this page as the map for the project docs. PyRiskLab is a local Python
simulation and reporting engine; the docs are organized around reviewer
navigation, implementation architecture, reproducibility, and interview framing.

For SWE-intern review, start with `PROJECT_STATUS.md`, `REVIEWER_GUIDE.md`,
`FINAL_REVIEW_CHECKLIST.md`, and `RESUME_SNIPPETS.md`. Those pages frame the
project as local Python simulation, automation, testing, debugging, and
performance tooling rather than a trading product.

## Fast Reviewer Path

| Doc | Use it for |
| --- | --- |
| `PROJECT_STATUS.md` | Implemented scope, checks, and reviewer starting points. |
| `RECRUITER_BRIEF.md` | One-page SWE-intern recruiter framing and quick-skim evidence. |
| `REVIEWER_GUIDE.md` | Five-minute path, demo command, and strongest files to inspect. |
| `REQUIREMENTS_TRACEABILITY.md` | Version 1 requirements mapped to current repo evidence. |
| `DEMO_WALKTHROUGH.md` | Short demo path, screenshot targets, and interview talk track. |
| `assets/README.md` | Optional screenshot naming and curation guide after local validation. |
| `SAMPLE_OUTPUT.md` | Expected terminal output and summary-report shape. |
| `sample_outputs/artifact_manifest.md` | Generated files and their reviewer signal. |
| `FINAL_REVIEW_CHECKLIST.md` | Final local validation checklist and resume-ready gate. |

## Engineering References

| Doc | Use it for |
| --- | --- |
| `ARCHITECTURE.md` | Module responsibilities, data flow, and scope boundaries. |
| `API_REFERENCE.md` | Main modules, public functions/classes, and intended import surface. |
| `CONFIG_REFERENCE.md` | Field-by-field explanation of both committed YAML configs. |
| `ASSUMPTIONS.md` | Model assumptions, simplifications, and Version 1 limitations. |
| `VALIDATION_NOTES.md` | Defensive validation layers, error types, and edge-case map. |
| `IMPLEMENTATION_AUDIT.md` | Static source/test audit notes and placeholder-scan guidance. |
| `DEPENDENCY_POLICY.md` | Small-stack dependency boundaries for the local MVP. |
| `PERFORMANCE_NOTES.md` | Benchmark assumptions, output columns, and speedup caveats. |
| `VERSIONING.md` | Version sources, changelog alignment, and release boundary. |
| `DEBUGGING_GUIDE.md` | Clean errors, `--debug`, metadata triage, and local checks. |
| `PLATFORM_NOTES.md` | Cross-platform local-run expectations and artifact differences. |
| `TESTING_STRATEGY.md` | Test organization, reviewer commands, and validation philosophy. |
| `../scripts/local_verify.py` | Optional helper for pytest, ruff, demo, and risk-stress. |
| `sample_outputs/csv_contracts.md` | CSV output contracts and stable column expectations. |
| `sample_outputs/chart_artifacts.md` | PNG artifacts and what each chart communicates. |
| `sample_outputs/run_metadata_example.md` | Shape of run reproducibility metadata. |
| `sample_outputs/risk_stress_demo.md` | Blocked-order preset and risk-event review. |

## Portfolio And Planning

| Doc | Use it for |
| --- | --- |
| `../CHANGELOG.md` | Version 1 MVP release summary and scope boundaries. |
| `../CONTRIBUTING.md` | Local setup, checks, scope rules, and doc-update expectations. |
| `../SUPPORT.md` | Bug, enhancement, and security support routing. |
| `../SECURITY.md` | No-secrets policy and local-only security boundaries. |
| `../.github/CODEOWNERS` | Repository ownership metadata for GitHub review surfaces. |
| `../.github/ISSUE_TEMPLATE/bug_report.md` | Bug checklist for local simulation issues. |
| `../.github/ISSUE_TEMPLATE/feature_request.md` | Enhancement template for engineering signal. |
| `../.github/PULL_REQUEST_TEMPLATE.md` | Review checklist for reproducible local changes. |
| `PORTFOLIO_CASE_STUDY.md` | Interview story, tradeoffs, and resume positioning. |
| `INTERVIEW_NOTES.md` | One-minute pitch, talking points, and resume bullets. |
| `RESUME_SNIPPETS.md` | Resume-ready project description, bullet options, and keywords. |
| `GITHUB_PROFILE_SETUP.md` | Suggested GitHub About text, topics, and pinned-repo wording. |
| `PROJECT_SELECTION_BRIEF.md` | Original project-selection rationale. |
| `PROJECT_MASTER_BLUEPRINT.md` | Full source blueprint used to build the project. |
| `TECH_STACK_AND_ARCHITECTURE.md` | Original stack and architecture planning notes. |
| `features/README.md` | Ordered feature map from build plan to implementation evidence. |
| `features/` | Feature-by-feature planning documents for the Version 1 build. |

The generated `results/` folder is intentionally not committed beyond
`results/.gitkeep`; run the demo locally to reproduce CSV, PNG, JSON, YAML, and
Markdown artifacts from the deterministic configs.
