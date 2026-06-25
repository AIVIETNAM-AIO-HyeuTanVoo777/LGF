# LaTeX Source Integrity Audit

This audit verifies that the LaTeX source files, tables, figures, and bibliographic files are complete, exist on disk, and are correctly packaged for Overleaf upload.

## 1. LaTeX Main Entry Point
- **File**: `paper/main.tex`
- **Status**: Checked and verified.
- **Input files**:
  - `sections/01_introduction` (Exists)
  - `sections/02_related_work` (Exists)
  - `sections/03_method` (Exists)
  - `sections/04_experiments` (Exists)
  - `sections/05_results` (Exists)
  - `sections/06_ablation` (Exists)
  - `sections/07_discussion` (Exists)
  - `sections/08_conclusion` (Exists)

## 2. Table Files Verification
Verified that all dynamically inputted table files in `paper/sections/` exist and are populated with correct data:
- `paper/sections/tongji_session_quality_table.tex` (Exists)
- `paper/sections/strict_tongji_ablation_table.tex` (Exists)
- `paper/sections/paired_statistics_component_ablation_table.tex` (Exists)
- `paper/sections/strict_tongji_ablation_by_direction_table.tex` (Exists)
- `paper/sections/strict_tongji_score_diagnostics_table.tex` (Exists)
- `paper/sections/strict_tongji_failure_tail_table.tex` (Exists)
- `paper/sections/palmprint_specific_baseline_table.tex` (Exists)
- `paper/sections/iitd_subject_disjoint_table.tex` (Exists)
- `paper/sections/rankb_protocol_audit_table.tex` (Exists)
- `paper/sections/training_config_table.tex` (Exists)

## 3. Figure Files Verification
Verified that all figure files referenced in `strict_tongji_score_figures.tex` exist on disk:
- `paper/figures/roc_tongji_b1_b5_b6_s1_to_s2.pdf` (Exists, 22.7 KB)
- `paper/figures/roc_tongji_b1_b5_b6_s2_to_s1.pdf` (Exists, 22.7 KB)
- `paper/figures/det_tongji_b1_b5_b6_s1_to_s2.pdf` (Exists, 19.3 KB)
- `paper/figures/det_tongji_b1_b5_b6_s2_to_s1.pdf` (Exists, 19.2 KB)
- `paper/figures/score_hist_tongji_b1_b5_b6_s1_to_s2.pdf` (Exists, 21.6 KB)
- `paper/figures/score_hist_tongji_b1_b5_b6_s2_to_s1.pdf` (Exists, 21.6 KB)

## 4. Overleaf ZIP Package Verification
- **Package path**: `paper_overleaf_upload.zip`
- **Total files**: 29 files
- **Root structure**: Verified that the root of the ZIP file contains `main.tex`, `references.bib`, `sections/`, and `figures/` directories directly without any nested outer container directory.
