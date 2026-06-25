# Fix Table 11 and Table 12 Layout Overflow — Report

## Summary

Tables that previously overflowed horizontally in the compiled PDF have been
fixed by removing the wide `Description` column and switching to compact TAR
header notation. **No result values, captions' scientific meaning, claims, or
experiment outputs were changed.**

---

## Files Changed

| File | Change |
|---|---|
| `scripts/make_result_tables.py` | Fixed generators for both tables (see below) |
| `paper/sections/palmprint_specific_baseline_table.tex` | Regenerated — compact layout |
| `paper/sections/iitd_subject_disjoint_table.tex` | Regenerated — compact layout |
| `docs/agent_logs/fix_table_11_12_layout_report.md` | This report |
| `paper_overleaf_upload.zip` | Rebuilt |

---

## Generator Changes (`scripts/make_result_tables.py`)

Both the IITD (section 4, `iitd_subject_disjoint_table.tex`) and Gabor
(section 5, `palmprint_specific_baseline_table.tex`) generator blocks were updated:

1. **Removed `Description` column** — the `{llcccccc}` tabular was replaced by
   `{lcccccc}` and the corresponding data cell was removed from each row.

2. **Compact TAR headers** — `TAR@FAR=$10^{-2}$` and `TAR@FAR=$10^{-3}$`
   replaced by `TAR@$10^{-2}$` and `TAR@$10^{-3}$`.

3. **`\small`** inserted immediately after `\label{…}`.

4. **`\setlength{\tabcolsep}{4pt}`** inserted after `\small`.

5. **`\resizebox{\linewidth}{!}{%…}`** wraps the `tabular` environment.

6. **Caption note** `"TAR columns denote TAR@FAR at the indicated FAR target."`
   appended to each caption. Scientific meaning of the caption is unchanged.

---

## Verification

- **Generator fixed**: Yes — `scripts/make_result_tables.py` passes `py_compile` with no errors.
- **Tables regenerated**: Yes — both `.tex` files written by the script on this run.
- **No result values changed**: Confirmed. The numerical values in both tables
  are identical to the pre-fix versions:
  - Gabor: `92.99 ± 1.01`, `94.42 ± 0.62`, `92.59 ± 1.04`, `9.61 ± 0.52`, `62.81 ± 5.83`, `34.38 ± 8.66`
  - M1: `97.83 ± 0.72`, `98.91 ± 0.36`, `97.70 ± 0.81`, `3.05 ± 1.18`, `94.82 ± 2.86`, `86.17 ± 7.07`
  - M6: `97.95 ± 1.71`, `98.91 ± 0.63`, `97.86 ± 1.80`, `3.24 ± 1.34`, `94.39 ± 2.51`, `85.45 ± 3.85`
- **`paper_overleaf_upload.zip` regenerated**: Yes.
- **`\usepackage{graphicx}` present**: Yes — already present in `paper/main.tex` (line 6).
- **Table labels preserved**:
  - Gabor: `\label{tab:palmprint_specific_baseline}` (unchanged)
  - IITD: `\label{tab:iitd_subject_disjoint}` (unchanged)
