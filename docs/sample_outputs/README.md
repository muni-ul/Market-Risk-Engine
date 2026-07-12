# PyRiskLab Sample Outputs

This folder gives reviewers a quick preview of the files produced by a local
demo run without committing generated `results/demo_run/` artifacts.

The actual demo command is still the source of truth:

```bash
python -m pyrisklab run --config configs/demo.yaml --overwrite
```

Generated benchmark timings vary by machine, so these examples describe output
shape instead of claiming fixed performance numbers. When benchmark execution is
disabled, PyRiskLab still writes the benchmark artifact with headers and calls
out the disabled config in the summary report.

## Included References

- `summary_report_excerpt.md`: representative Markdown report structure.
- `csv_contracts.md`: expected CSV files and the columns reviewers should see.
- `chart_artifacts.md`: expected PNG chart files and what each chart communicates.
- `artifact_manifest.md`: every generated file, its type, and the reviewer
  signal it provides.
- `run_metadata_example.md`: reproducibility metadata shape, including config
  digest, benchmark settings, order status counts, expected artifacts, generated
  artifacts, and generated artifact byte sizes.
- `risk_stress_demo.md`: optional blocked-order demo using `configs/risk_stress.yaml`.

## Why These Are Docs Instead Of Generated Results

PyRiskLab is designed to produce deterministic local artifacts, but benchmark
timing and chart image metadata can vary by machine. Keeping compact
sample-output docs gives GitHub reviewers a stable preview while leaving the
real `results/` folder generated locally.

For the final local verification path, use `docs/FINAL_REVIEW_CHECKLIST.md`
after running the demo. It lists the full expected artifact set and the metadata
fields to inspect before presenting the project.
