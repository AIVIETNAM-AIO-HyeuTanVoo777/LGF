# Final Polish Report

This report summarizes the final polish changes applied to the paper, figures, and generator scripts to ensure consistent and correct presentation in the compiled PDF.

## Summary of Changes

### 1. Figure Legend Polish
- **Script modified**: `scripts/make_strict_tongji_score_figures.py`
- **Updates**:
  - Replaced all `B1`, `B5`, and `B6` labels in the figure legends with clean, paper-friendly IDs:
    - `M1 CE+SupCon` (previously `B1 CE+SupCon`)
    - `M4 BNNeck+CE` (previously `B5 BNNeck+CE`)
    - `M6 BNNeck+ArcFace` (previously `B6 BNNeck+ArcFace`)
  - Updated `write_summary` and `write_tex` to write and summarize using `M1`, `M4`, and `M6` respectively.
  - Re-ran the figure generation script to rebuild all 6 figure PDFs in `paper/figures/`. Captions and references remain consistent.

### 2. Elimination of Contiguous Model Range Labeling
- **Files modified**:
  - `paper/sections/05_results.tex` (line 6)
  - `scripts/aggregate_cosface_baseline_results.py` (line 115)
- **Updates**:
  - Replaced the range labels `"M0–M7"` and `"M0-M7"` with the explicit list `"M0, M1, M2, M3, M4, M6, and M7"` to avoid implying that configuration M5 is reported.

### 3. Minor Wording Edits
- **Files modified**:
  - `paper/sections/02_related_work.tex`:
    - Replaced `"in this project"` with `"in this study"` in Section 2.2.
    - Replaced `"M6 combines these two ideas to the palmprint setting"` with `"M6 adapts these ideas to the palmprint setting"`.
  - `paper/sections/05_results.tex`:
    - Replaced `"reinforces our main conclusion"` with `"is consistent with our main conclusion"` when describing the secondary IITD validation.
  - `scripts/audit_training_config_table.py` & `paper/sections/training_config_table.tex`:
    - Replaced the embedding label `"pre-BN/default"` for non-BNNeck models (M0, M1, M2, M3) with `"default L2"`.

### 4. Table 1 Layout Improvements
- **File modified**: `paper/sections/02_related_work.tex` (Table 1: `tab:literature_protocol_positioning`)
- **Updates**:
  - Replaced the dataset string `"IITD/CASIA/PolyU/NTU"` with `"IITD, CASIA, PolyU, NTU"` (including spaces). This prevents LaTeX from treating it as a single long word, enabling text wrapping and avoiding a visual merge with the adjacent "Yes" cell in the compiled PDF.
  - Set the dataset column width to `0.22\textwidth` for cleaner rendering.
  - Clarified in the table caption that the table is for protocol positioning and contextualization, and is not a direct numerical leaderboard comparison.

### 5. Rebuilt Outputs
- Re-executed:
  - `python scripts/make_strict_tongji_score_figures.py`
  - `python scripts/audit_training_config_table.py`
  - `python scripts/aggregate_cosface_baseline_results.py`
  - `python scripts/make_result_tables.py --results-dir docs/results --out-dir paper/sections`
  - `python build_overleaf_package.py`
- Regenerated the Overleaf zip package: `paper_overleaf_upload.zip`.

## Verification and Scientific Claims
- All numeric results, metrics, experiment definitions, and scientific claims remain unchanged.
- Checked that all B-code labels have been eliminated from the text and figure legends in the final LaTeX sources.
- Checked that there are no remaining double question marks `??` in the paper sections.
