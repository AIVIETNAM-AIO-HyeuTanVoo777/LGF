# Metric Recompute Decision

## Old Implementation Found
The previous implementation of `tar_at_far_conservative` in `palmrec/evaluation/metrics.py` accepted pre-computed `fpr`, `tpr`, and `thresholds` (from `sklearn.metrics.roc_curve`) and selected a point whose empirical FPR satisfied `fpr <= target_far`.
However, some result tables in the repository (e.g. for IITD or Tongji) were previously compiled using a nearest-FPR metric convention (or other unverified methods) which sometimes selected points exceeding the target FAR (known as nearest-FPR violating target FAR).
In our audit, we discovered **35** instances where the nearest-FPR rule selected a threshold exceeding the target FAR.

## Nearest ROC Point Usage
- **Nearest ROC Point Used**: Yes, in legacy runs and previous scripts before our strict audit.
- **Audited status**: 35 rows had nearest empirical FAR exceeding the target FAR.

## List of Stale Result Files
- `docs/results/gabor_strict_tongji_runs.csv`
- `docs/results/gabor_strict_tongji_summary.csv`
- `docs/results/gabor_strict_tongji_summary.md`
- `paper/sections/palmprint_specific_baseline_table.tex`
- `docs/results/strict_tongji_ablation_results.md`
- `docs/results/strict_tongji_ablation_runs.csv`
- `docs/results/strict_tongji_ablation_summary.csv`
- `docs/results/iitd_subject_disjoint_rerun_results.md`
- `docs/results/iitd_subject_disjoint_rerun_runs.csv`
- `docs/results/iitd_subject_disjoint_rerun_summary.csv`
- `docs/results/iitd_subject_disjoint_rerun_table.tex`

## List of Recomputed Outputs
- All Gabor strict baseline runs (6 runs, recalculated using the new `conservative_tar_at_far` rule)
- Re-aggregated Tongji strict ablation summaries
- Re-aggregated IITD subject-disjoint summaries and LaTeX tables
- Threshold audit evidence outputs (`docs/audits/threshold_audit.csv`, `docs/audits/metric_threshold_audit.csv`, `docs/audits/metric_threshold_audit.md`)

## Date/Time and Command
- **Date/Time**: 2026-06-25 15:35 UTC
- **Commands run**:
  - `python scripts/export_threshold_audit.py`
  - `python scripts/audit_metric_thresholds.py`
  - `python scripts/evaluate_gabor_strict_tongji_baseline.py`
  - `python scripts/aggregate_strict_ablation_results.py`
  - `python scripts/aggregate_iitd_rerun_results.py`
