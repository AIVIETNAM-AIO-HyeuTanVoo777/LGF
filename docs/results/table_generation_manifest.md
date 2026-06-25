# Table Generation Manifest

This manifest tracks the generation of LaTeX tables from aggregated CSV results, ensuring full auditability of the paper's results.

## Tables Log

| Table Name | Input CSV | Script Command | Output .tex Path | Date Generated | Git Commit | Number of Rows | Notes |
|---|---|---|---|---|---|---|---|
| Strict Tongji Ablation Summary | `main_tongji_results.csv`, `classical_reference_results.csv` | `python scripts/make_result_tables.py` | `paper/sections/strict_tongji_ablation_table.tex` | 2026-06-25 | 1cc3130 | 7 | Deep learning ablation summary and Gabor reference |
| Direction-Specific Strict Tongji | `tongji_directional_results.csv` | `python scripts/make_result_tables.py` | `paper/sections/strict_tongji_ablation_by_direction_table.tex` | 2026-06-25 | 1cc3130 | 14 | Results split by S1->S2 and S2->S1 directions |
| Paired Delta Statistics | `paired_deltas.csv` | `python scripts/make_result_tables.py` | `paper/sections/paired_statistics_component_ablation_table.tex` | 2026-06-25 | 1cc3130 | 18 | M6-M1, M4-M1, M4-M6 paired comparisons |
| IITD Secondary Validation | `iitd_secondary_results.csv` | `python scripts/make_result_tables.py` | `paper/sections/iitd_subject_disjoint_table.tex` | 2026-06-25 | 1cc3130 | 2 | Within-session secondary validation results |
| Gabor Reference Baseline | `classical_reference_results.csv` | `python scripts/make_result_tables.py` | `paper/sections/palmprint_specific_baseline_table.tex` | 2026-06-25 | 1cc3130 | 1 | Baseline Gabor texture reference |

## Verification Check

Run the following test to verify the consistency of the collected files:
```bash
python -c "import pandas as pd; main='docs/results/main_tongji_results.csv'; df=pd.read_csv(main); required=['method','dataset','direction','seed','rank1','eer','tar_far_1e_3']; missing=[c for c in required if c not in df.columns]; assert not missing, missing; print(df.groupby(['dataset','method']).size())"
```
