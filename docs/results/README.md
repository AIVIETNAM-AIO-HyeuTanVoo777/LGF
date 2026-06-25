# Final Result Sources

This directory contains the final result artifacts used by the current paper draft.

## Final evidence files

- `strict_tongji_ablation_results.md`
- `strict_tongji_ablation_runs.csv`
- `strict_tongji_ablation_summary.csv`
- `strict_tongji_score_diagnostics.md`
- `strict_tongji_score_diagnostics.csv`
- `strict_tongji_score_diagnostics_summary.csv`
- `paired_statistics_b6_vs_b1.md`
- `paired_statistics_b6_vs_b1.csv`
- `paired_delta_b6_vs_b1.csv`
- `tongji_directional_delta_b6_minus_b1.md`
- `tongji_directional_delta_b6_minus_b1.csv`

## Linked audit evidence

The final paper also depends on audit artifacts stored outside `docs/results/`:

- `docs/audits/rankb_protocol_audit.md`
- `docs/audits/rankb_protocol_audit.csv`
- `docs/audits/checkpoint_selection_audit.md`
- `docs/audits/checkpoint_selection_audit.csv`
- `docs/audits/identity_parser_audit.md`
- `docs/audits/identity_parser_audit.csv`
- `docs/audits/tongji_session_quality.md`
- `docs/audits/paper_reference_audit.md`

## Current claim boundary

The current paper uses a palm-class-disjoint Tongji cross-session protocol audit, a checkpoint-selection audit, and an identity/parser audit. The paper does not claim universal superiority for BNNeck + ArcFace. The strict Tongji ablation shows that B5 has the highest observed mean among tested variants by Rank-1 and TAR@FAR=1e-3, while B1 has the highest observed average genuine/impostor separation by d-prime.

## Legacy files

Older exploratory summaries and superseded claim drafts have been moved to `docs/legacy_results/`. They are retained for project history only and are not part of the final paper evidence package.

## IITD rerun evidence

The corrected IITD palm-class-disjoint within-session rerun is secondary validation only and is not cross-session evidence.

- `docs/results/iitd_subject_disjoint_rerun_results.md`
- `docs/results/iitd_subject_disjoint_rerun_runs.csv`
- `docs/results/iitd_subject_disjoint_rerun_summary.csv`
- `docs/results/iitd_subject_disjoint_rerun_delta_b6_minus_b1.csv`
- `docs/results/iitd_subject_disjoint_rerun_table.tex`

## Metric-threshold audit

The strict Tongji verification metrics are audited for pair counts and threshold convention.

- `docs/audits/metric_threshold_audit.md`
- `docs/audits/metric_threshold_audit.csv`

## Paired component-ablation statistics

The strict Tongji component-ablation claim is supported by paired comparisons over the six matched seed-direction units.

- `docs/results/paired_statistics_component_ablation.md`
- `docs/results/paired_statistics_component_ablation.csv`

## Strict Tongji by-direction ablation

The strict Tongji component-ablation results are also summarized separately by session direction to support the direction-sensitivity analysis.

- `docs/results/strict_tongji_ablation_by_direction.md`
- `docs/results/strict_tongji_ablation_by_direction.csv`

## Strict Tongji ROC/DET/score figures

Reviewer-facing ROC, DET, and score-distribution figures are generated for B1, B5, and B6 by session direction.

- `docs/results/strict_tongji_roc_det_score_figures.md`
- `docs/results/strict_tongji_roc_det_score_figures.csv`
- `paper/sections/strict_tongji_score_figures.tex`
- `paper/figures/roc_tongji_b1_b5_b6_s1_to_s2.pdf`
- `paper/figures/roc_tongji_b1_b5_b6_s2_to_s1.pdf`
- `paper/figures/det_tongji_b1_b5_b6_s1_to_s2.pdf`
- `paper/figures/det_tongji_b1_b5_b6_s2_to_s1.pdf`
- `paper/figures/score_hist_tongji_b1_b5_b6_s1_to_s2.pdf`
- `paper/figures/score_hist_tongji_b1_b5_b6_s2_to_s1.pdf`

## Training configuration audit

The final strict Tongji component-ablation configs are summarized for reviewer-facing reproducibility.

- `docs/audits/training_config_audit.md`
- `docs/audits/training_config_audit.csv`
- `paper/sections/training_config_table.tex`
## ArcFace sensitivity evidence

The current revision records fixed-recipe ArcFace component sensitivity evidence, not a margin hyperparameter sweep.

- `docs/results/arcface_sensitivity_evidence.md`
- `docs/plans/arcface_sensitivity_plan.md`
