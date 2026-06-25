# Results Manifest

Public result summaries used by the paper tables are stored under `audit_artifacts/results/`.

Key files:

- `main_tongji_results.csv`: M0/M1/M2/M3/M4/M6/M7 strict Tongji rows over both directions and three seeds.
- `iitd_secondary_results.csv`: IITD within-session validation rows.
- `paired_deltas.csv`: paired seed-direction delta summaries.
- `classical_reference_results.csv`: fixed-Gabor texture reference summary used only as a protocol-normalized classical baseline.
- `strict_tongji_ablation_by_direction.csv`: direction-specific Tongji summaries.
- `strict_tongji_additional_baselines.csv`: additional baseline rows and notes.
- `strict_tongji_score_diagnostics.csv`: aggregate score diagnostic summaries.
- `threshold_evidence_conservative_tar_far.csv`: conservative TAR@FAR evidence summary.

Run and table-generation provenance are stored under `audit_artifacts/manifests/`.
