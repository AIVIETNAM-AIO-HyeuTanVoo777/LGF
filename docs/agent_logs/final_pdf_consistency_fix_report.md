# final_pdf_consistency_fix_report.md

This report documents the audited consistency fixes applied to the palmprint recognition paper's LaTeX files, tables, and packaging scripts.

## Applied Fixes

### 1. B-Code Translation and Removal
- **Section 3.1 (Component Matrix)**: Removed the parenthetical mappings `(B0)`, `(B1)`, `(B4)`, `(B8)`, `(B5)`, `(B6)`, and `(B7)` from the ResNet18 component configurations list. The main configurations are now cleanly labeled as `M0` through `M7`.
- **Section 2.2 (Metric Learning)**: Replaced references to `"B1 baseline"` with `"M1 baseline"`, and `"B6 adapts"` with `"M6 combines"`.
- **Figures (strict_tongji_score_figures.tex)**: Replaced `"B1, B5, and B6"` references in the captions of the ROC, DET, and score distribution figures with `"M1, M4, and M6"`.
- **Additional Baselines Table (strict_tongji_additional_baselines_table.tex)**: Replaced `"B8"` references with `"M3"`.
- **Paired Statistics Table (paired_statistics_b6_vs_b1_table.tex)**: Regenerated the table using the updated script (`scripts/rankb_paired_statistics.py`) which translates `"B6 minus B1"` to `"M6 minus M1"`.
- **Scripts**: Updated `scripts/aggregate_cosface_baseline_results.py` to label CosFace as `M3` in the output CSV and Markdown.

### 2. Table 5 (Training Configuration Summary) Audit and Fixes
- **Non-BNNeck Eval Embeddings**: Modified the generator `scripts/audit_training_config_table.py` so that any non-BNNeck model configuration (M0, M1, M2, M3) is explicitly labeled with `pre-BN/default` instead of `post-BN`.
- **Margin Head Scale/Margin Header**: Renamed the column header from `ArcFace (s,m)` to `Margin head (s,m)`.
- **Missing M3 CosFace Row**: Injected B8/M3 CosFace runs dynamically during the audit loop. The final table now lists:
  - `M0`: `pre-BN/default` eval embedding, no margin parameters.
  - `M1`: `pre-BN/default` eval embedding, no margin parameters.
  - `M2`: `pre-BN/default` eval embedding, ArcFace `(30.0,0.5)`.
  - `M3`: `pre-BN/default` eval embedding, CosFace `(30.0,0.35)`.
  - `M4`: `post-BN` eval embedding, no margin parameters.
  - `M6`: `post-BN` eval embedding, ArcFace `(30.0,0.5)`.
  - `M7`: `post-BN` eval embedding, ArcFace `(30.0,0.5)`.

### 3. Undefined Figure References Resolution
- **Inclusion of Score Figures**: Appended `\input{sections/strict_tongji_score_figures}` at the end of `paper/sections/06_ablation.tex`, ensuring that the figures (`fig:strict_tongji_roc_by_direction`, `fig:strict_tongji_det_by_direction`, and `fig:strict_tongji_score_hist_by_direction`) are parsed and defined.
- **Reference Checks**: Verified that no `??` or unresolved references remain in the LaTeX files or the packaged output.

### 4. Table 3 (Protocol Audit Table) Direction Encoding
- **LaTeX Safe Arrows**: Modified `scripts/audit_rankb_protocol.py` to output `S1$\to$S2` and `S2$\to$S1` instead of `S1->S2` and `S2->S1`. This avoids font encoding issues in compiled PDF where `->` could render as `¿` or other unexpected glyphs.
- **Regenerated Table**: Ran the protocol audit script and copied the updated `rankb_protocol_audit_table.tex` into the `paper/sections/` directory.

### 5. Softened Protocol Wording in Section 4.1
- **Experimental Setup Rewrite**: Softened the wording of the Tongji cross-session protocol description:
  - *Previous*: `training, validation, and gallery data from session 1; probe data from session 2.`
  - *Softened*: `development training/validation images are drawn from session 1 development palm classes, while final held-out evaluation uses session 1 images as gallery and session 2 images as probe for held-out palm classes.`
  - Updated both directions symmetrically.

### 6. Component Matrix Wording
- **Method Section**: Replaced `"isolates the effect"` with `"probes selected effects and interactions"` in Section 3.1 to soften claims about complete factor isolation.

## Packaging and Verification
- Ran `scripts/make_result_tables.py` to regenerate all standard tables.
- Ran `build_overleaf_package.py` to regenerate the `paper_overleaf_upload.zip` file.
- Verified that no B-codes or malformed direction characters remain in the packaged tex files.
