# PyRiskLab Documentation Index

Use this page as the map for the project docs. PyRiskLab is a local Python
simulation and reporting engine; the docs are organized around reviewer
navigation, implementation architecture, reproducibility, and interview framing.

## Fast Reviewer Path

| Doc | Use it for |
| --- | --- |
| `REVIEWER_GUIDE.md` | Five-minute evaluation path, demo command, and the strongest files to inspect. |
| `SAMPLE_OUTPUT.md` | Expected terminal output and summary-report shape. |
| `sample_outputs/artifact_manifest.md` | Every generated file and the reviewer signal it provides. |
| `FINAL_REVIEW_CHECKLIST.md` | Final local validation checklist before using the project on a resume. |

## Engineering References

| Doc | Use it for |
| --- | --- |
| `ARCHITECTURE.md` | Module responsibilities, data flow, and scope boundaries. |
| `API_REFERENCE.md` | Main modules, public functions/classes, and intended import surface. |
| `CONFIG_REFERENCE.md` | Field-by-field explanation of `configs/demo.yaml` and `configs/risk_stress.yaml`. |
| `TESTING_STRATEGY.md` | Test-suite organization, reviewer commands, and validation philosophy. |
| `sample_outputs/csv_contracts.md` | CSV output contracts and stable column expectations. |
| `sample_outputs/chart_artifacts.md` | PNG chart artifacts and what each chart communicates. |
| `sample_outputs/run_metadata_example.md` | Shape of the reproducibility metadata written with each run. |
| `sample_outputs/risk_stress_demo.md` | Optional preset for blocked simulated orders and risk-event review. |

## Portfolio And Planning

| Doc | Use it for |
| --- | --- |
| `../CHANGELOG.md` | Version 1 MVP release summary and scope boundaries. |
| `../CONTRIBUTING.md` | Local setup, development checks, scope rules, and documentation update expectations. |
| `../SECURITY.md` | No-secrets policy, supported version, and local-only security boundaries. |
| `PORTFOLIO_CASE_STUDY.md` | Interview story, tradeoffs, and resume positioning. |
| `INTERVIEW_NOTES.md` | One-minute pitch, talking points, and resume bullets. |
| `PROJECT_SELECTION_BRIEF.md` | Original project-selection rationale. |
| `PROJECT_MASTER_BLUEPRINT.md` | Full source blueprint used to build the project. |
| `TECH_STACK_AND_ARCHITECTURE.md` | Original stack and architecture planning notes. |
| `features/` | Feature-by-feature planning documents for the Version 1 build. |

The generated `results/` folder is intentionally not committed beyond
`results/.gitkeep`; run the demo locally to reproduce CSV, PNG, JSON, YAML, and
Markdown artifacts from the deterministic configs.
