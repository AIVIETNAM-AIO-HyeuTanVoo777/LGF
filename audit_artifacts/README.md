# Audit Artifacts

This directory contains non-sensitive reproducibility artifacts only. It intentionally excludes raw images, checkpoints, experiment directories, score tensors, generated ZIP exports, private paths, and local machine paths.

| File | Purpose |
|---|---|
| `splits/split_audit.csv` | Machine-readable split overlap and split-hash audit. |
| `splits/split_audit.md` | Human-readable split audit summary. |
| `splits/split_sizes.csv` | Split-size summary by dataset, direction, and seed. |
| `splits/split_integrity_summary.md` | Split-integrity narrative summary. |
| `splits/split_checksums.md` | Split checksum summary. |
| `protocol/gallery_probe_audit.csv` | Machine-readable gallery/probe construction audit. |
| `protocol/gallery_probe_audit.md` | Human-readable gallery/probe construction audit. |
| `protocol/gallery_probe_audit_summary.md` | Summary emitted by `scripts/audit_splits.py` when regenerated. |
| `protocol/checkpoint_selection_audit.csv` | Machine-readable checkpoint-selection policy audit. |
| `protocol/checkpoint_selection_audit.md` | Human-readable checkpoint-selection policy audit. |
| `protocol/protocol_audit.csv` | Machine-readable protocol audit. |
| `protocol/protocol_audit.md` | Human-readable protocol audit. |
| `protocol/protocol_audit_table.tex` | LaTeX protocol-audit table generated for the paper. |
| `metrics/metric_threshold_audit.csv` | Machine-readable conservative TAR@FAR threshold audit. |
| `metrics/metric_threshold_audit.md` | Human-readable conservative TAR@FAR threshold audit. |
| `metrics/training_config_audit.csv` | Machine-readable training-configuration audit. |
| `metrics/training_config_audit.md` | Human-readable training-configuration audit. |
| `manifests/run_manifest.csv` | Public run manifest with configs, split hashes, relative output paths, and result JSON paths. |
| `manifests/strict_tongji_ablation_runs.csv` | Source manifest for score-curve and threshold recomputation when local run outputs exist. |
| `manifests/iitd_subject_disjoint_rerun_runs.csv` | Source manifest for IITD threshold recomputation when local run outputs exist. |
| `manifests/table_generation_manifest.md` | Table-generation provenance. |
| `results/main_tongji_results.csv` | Main strict Tongji result rows for M0/M1/M2/M3/M4/M6/M7. |
| `results/iitd_secondary_results.csv` | Secondary IITD within-session validation rows. |
| `results/paired_deltas.csv` | Paired seed-direction delta summaries. |
| `results/classical_reference_results.csv` | Fixed-Gabor texture reference summary. |
| `results/strict_tongji_ablation_by_direction.csv` | Direction-specific strict Tongji summaries. |
| `results/strict_tongji_additional_baselines.csv` | Additional baseline summaries. |
| `results/strict_tongji_score_diagnostics.csv` | Aggregate score diagnostic summaries. |
| `results/threshold_evidence_conservative_tar_far.csv` | Conservative threshold evidence summary. |

Regenerate deterministic split/protocol audits with:

```bash
python scripts/audit_protocol.py
```

Regenerate threshold and ROC/DET artifacts only after local experiment score files are available:

```bash
python scripts/audit_protocol.py --include-thresholds
python scripts/plot_roc_det.py
```
