# Method Label Consistency Audit

This audit verifies that all method labels and identifiers used throughout the paper text consistently match the rows and definitions in the generated results tables.

## Method Mapping Matrix

| Paper Identifier | Config Identifier | Neck Layer | Classification Supervision / Loss | Primary evaluation status |
|---|---|---|---|---|
| **M0** | B0 | None | Cross-Entropy (CE) | Completed |
| **M1** | B1 | None | CE + Supervised Contrastive Loss (SupCon) | Completed |
| **M2** | B4 | None | ArcFace | Completed |
| **M3** | B8 | None | CosFace | Completed |
| **M4** | B5 | BNNeck | CE | Completed |
| **M6** | B6 | BNNeck | ArcFace | Completed |
| **M7** | B7 | BNNeck | ArcFace + light SupCon | Completed |
| **Gabor** | - | N/A | Classical Gabor texture features (Reference) | Completed |

## Consistency Check Results

1. **B-Codes Elimination**: No raw configuration B-codes (B0, B1, B4, B5, B6, B7, B8) remain in the final compiled text of the paper sections. They have all been replaced by their paper-friendly counterparts (M0-M7).
2. **Text Reference Matching**: Every method referenced in `01_introduction.tex`, `03_method.tex`, `04_experiments.tex`, `05_results.tex`, `06_ablation.tex`, `07_discussion.tex`, and `08_conclusion.tex` is present in the main ablation tables:
   - `strict_tongji_ablation_table.tex`
   - `strict_tongji_ablation_by_direction_table.tex`
   - `paired_statistics_component_ablation_table.tex`
   - `iitd_subject_disjoint_table.tex`
3. **No Phantom Rows**: There are no references to any M5 method or undocumented B-codes anywhere in the document.
4. **Captions alignment**: Caps and text descriptions consistently refer to M1 as the baseline, M6 as the BNNeck+ArcFace setup, M4 as BNNeck+CE (the highest observed mean on key metrics), and M3 as the CosFace comparator.
