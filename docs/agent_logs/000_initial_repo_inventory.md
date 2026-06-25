# 000 Initial Repository Inventory

## Git Status
- **Current Branch**: `rankb-protocol-study-revision`
- **Current Commit**: `45c3932723ababae797ccd3ffd93e31e3d93aa70`
- **Dirty Files**:
  - `docs/protocols/rankb_protocol_lock.md` (untracked/uncommitted)

## Environment
- **Python Version**: `3.13.13`

## Detected Datasets
- **Tongji**:
  - total images: 12,000 (6,000 in `session1`, 6,000 in `session2`)
  - unique classes: 600
  - image size: 128x128
- **IITD**:
  - total images: 2,601 (all in `session1`)
  - unique classes: 460 (representing 230 subjects, left/right hand)
  - image size: 150x150

## Detected Split Files
Located in `data/splits/`:
- `tongji_subject_disjoint_s1_to_s2_seed42.json`
- `tongji_subject_disjoint_s1_to_s2_seed2026.json`
- `tongji_subject_disjoint_s1_to_s2_seed2705.json`
- `tongji_subject_disjoint_s2_to_s1_seed42.json`
- `tongji_subject_disjoint_s2_to_s1_seed2026.json`
- `tongji_subject_disjoint_s2_to_s1_seed2705.json`
- `iitd_subject_disjoint_within_seed42.json`
- `iitd_subject_disjoint_within_seed2026.json`
- `iitd_subject_disjoint_within_seed2705.json`
- `iitd_within.json`
- `cross_dataset_fewshot.json`
- `toy_split_seed42.json`

## Detected Configs
Located in `configs/`:
- Config files matching baselines B0, B1, B2, B3, B4, B5, B6, B7, B8 for different seeds and directions.
- Default configuration `configs/default.yaml`.

## Detected Result Files
Located in `docs/results/`:
- `tongji_subject_disjoint_summary.md`
- `iitd_subject_disjoint_rerun_results.md`
- `strict_tongji_ablation_results.md`
- Numerous JSON and Markdown files containing metric logs and evaluation parameters for the seed sweeps and baseline runs.

## Detected Paper Files
Located in `paper/`:
- `paper/main.tex`
- `paper/sections/01_introduction.tex`
- `paper/sections/02_related_work.tex`
- `paper/sections/03_method.tex`
- `paper/sections/04_experiments.tex`
- `paper/sections/05_results.tex`
- `paper/sections/06_ablation.tex`
- `paper/sections/07_discussion.tex`
- `paper/sections/08_conclusion.tex`
- LaTeX tables (e.g. `paper/sections/rankb_protocol_audit_table.tex`, `paper/sections/strict_tongji_ablation_table.tex`)
- DET/ROC plots in `paper/figures/`

## Suspected Metric Implementation Files
- `palmrec/evaluation/metrics.py` (implements classification metrics, Equal Error Rate calculation, and the conservative TAR@FAR rule `tar_at_far_conservative`).

## Unresolved Uncertainties
- None. Codebase is clean and well-structured, audit scripts pass, and datasets/splits are completely in place.
