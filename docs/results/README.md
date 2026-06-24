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

The current paper uses a palm-class-disjoint Tongji cross-session protocol audit, a checkpoint-selection audit, and an identity/parser audit. The paper does not claim universal superiority for BNNeck + ArcFace. The strict Tongji ablation shows that B5 is the strongest tested variant by Rank-1 and TAR@FAR=1e-3, while B1 has the strongest average genuine/impostor separation by d-prime.

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
