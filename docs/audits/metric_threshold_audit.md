# Metric Threshold Audit

This audit documents the revision from the previous nearest-FPR TAR@FAR rule to the conservative empirical-FAR rule used in the revised metric implementation.

## Metric convention

- Previous rule: choose the ROC point whose empirical FPR is nearest to the target FAR. This can select a point above the requested FAR.
- Revised rule: choose only ROC points with empirical FPR less than or equal to the target FAR, then select the valid point with the highest TPR.
- EER convention remains unchanged: sklearn ROC with brentq/interp1d interpolation when possible, falling back to nearest |FPR-FNR|.

## Required evidence artifacts

- Strict Tongji threshold evidence: `docs/results/threshold_evidence_strict_tongji.csv`
- IITD threshold evidence: `docs/results/threshold_evidence_iitd.csv`
- Combined audit CSV: `docs/audits/metric_threshold_audit.csv`

## Summary

| Dataset | Runs | Evidence rows | Conservative failures | Nearest-FPR rows above target | Max abs delta TAR vs reported (pp) | Pair count shapes | min FAR step values |
|---|---:|---:|---:|---:|---:|---|---|
| Tongji | 36 | 72 | 0 | 26 | 1.11022e-14 | [(12000, 1428000, 1440000)] | ['7.00280112045e-07'] |
| IITD | 6 | 12 | 0 | 9 | 2.22045e-14 | [(714, 64974, 65688), (726, 66066, 66792), (753, 68523, 69276)] | ['1.45936400916e-05', '1.51363787727e-05', '1.53907716933e-05'] |
| Combined | 42 | 84 | 0 | 35 | 2.22045e-14 | [(714, 64974, 65688), (726, 66066, 66792), (753, 68523, 69276), (12000, 1428000, 1440000)] | ['7.00280112045e-07', '1.45936400916e-05', '1.51363787727e-05', '1.53907716933e-05'] |

## Definition-of-done checks

- Conservative empirical FAR never exceeds target FAR: `True`
- Strict Tongji evidence rows: `72`
- IITD evidence rows: `12`

## Per-run conservative TAR@FAR=1e-3 evidence

| Dataset | Method | Direction | Seed | Target FAR | Selected empirical FAR | TAR | Nearest FPR | Nearest above target? | Delta vs reported (pp) |
|---|---|---|---:|---:|---:|---:|---:|---|---:|
| Tongji | B0 | S1->S2 | 42 | 0.001 | 0.001 | 0.65566667 | 0.001 | False | 0 |
| Tongji | B0 | S1->S2 | 2026 | 0.001 | 0.001 | 0.71308333 | 0.001 | False | 0 |
| Tongji | B0 | S1->S2 | 2705 | 0.001 | 0.001 | 0.78733333 | 0.001 | False | 0 |
| Tongji | B0 | S2->S1 | 42 | 0.001 | 0.00099859944 | 0.71516667 | 0.0010007003 | True | 0 |
| Tongji | B0 | S2->S1 | 2026 | 0.001 | 0.00099929972 | 0.71141667 | 0.00099929972 | False | 0 |
| Tongji | B0 | S2->S1 | 2705 | 0.001 | 0.00099929972 | 0.70883333 | 0.00099929972 | False | 0 |
| Tongji | B1 | S1->S2 | 42 | 0.001 | 0.001 | 0.59883333 | 0.001 | False | 0 |
| Tongji | B1 | S1->S2 | 2026 | 0.001 | 0.001 | 0.681 | 0.001 | False | 0 |
| Tongji | B1 | S1->S2 | 2705 | 0.001 | 0.001 | 0.75625 | 0.001 | False | 0 |
| Tongji | B1 | S2->S1 | 42 | 0.001 | 0.00099929972 | 0.762 | 0.00099929972 | False | 0 |
| Tongji | B1 | S2->S1 | 2026 | 0.001 | 0.0009964986 | 0.70283333 | 0.0010007003 | True | 0 |
| Tongji | B1 | S2->S1 | 2705 | 0.001 | 0.00099789916 | 0.80533333 | 0.0010014006 | True | 0 |
| Tongji | B4 | S1->S2 | 42 | 0.001 | 0.001 | 0.68775 | 0.001 | False | 0 |
| Tongji | B4 | S1->S2 | 2026 | 0.001 | 0.00099509804 | 0.71091667 | 0.0010007003 | True | 0 |
| Tongji | B4 | S1->S2 | 2705 | 0.001 | 0.001 | 0.76875 | 0.001 | False | 0 |
| Tongji | B4 | S2->S1 | 42 | 0.001 | 0.00099859944 | 0.70291667 | 0.00099859944 | False | 0 |
| Tongji | B4 | S2->S1 | 2026 | 0.001 | 0.00099719888 | 0.69283333 | 0.0010028011 | True | 0 |
| Tongji | B4 | S2->S1 | 2705 | 0.001 | 0.00099719888 | 0.68483333 | 0.0010007003 | True | 0 |
| Tongji | B5 | S1->S2 | 42 | 0.001 | 0.00099929972 | 0.71575 | 0.00099929972 | False | 0 |
| Tongji | B5 | S1->S2 | 2026 | 0.001 | 0.00099789916 | 0.74183333 | 0.0010021008 | True | 0 |
| Tongji | B5 | S1->S2 | 2705 | 0.001 | 0.001 | 0.79316667 | 0.001 | False | 0 |
| Tongji | B5 | S2->S1 | 42 | 0.001 | 0.001 | 0.75366667 | 0.001 | False | 0 |
| Tongji | B5 | S2->S1 | 2026 | 0.001 | 0.001 | 0.6715 | 0.001 | False | 0 |
| Tongji | B5 | S2->S1 | 2705 | 0.001 | 0.001 | 0.68316667 | 0.001 | False | 0 |
| Tongji | B6 | S1->S2 | 42 | 0.001 | 0.001 | 0.65883333 | 0.001 | False | 0 |
| Tongji | B6 | S1->S2 | 2026 | 0.001 | 0.001 | 0.74316667 | 0.001 | False | 0 |
| Tongji | B6 | S1->S2 | 2705 | 0.001 | 0.00099789916 | 0.67 | 0.0010014006 | True | 0 |
| Tongji | B6 | S2->S1 | 42 | 0.001 | 0.001 | 0.67966667 | 0.001 | False | 0 |
| Tongji | B6 | S2->S1 | 2026 | 0.001 | 0.0009964986 | 0.758 | 0.0010014006 | True | 0 |
| Tongji | B6 | S2->S1 | 2705 | 0.001 | 0.00099859944 | 0.67275 | 0.00099859944 | False | 0 |
| Tongji | B7 | S1->S2 | 42 | 0.001 | 0.00099929972 | 0.67783333 | 0.00099929972 | False | 0 |
| Tongji | B7 | S1->S2 | 2026 | 0.001 | 0.00099859944 | 0.75791667 | 0.0010007003 | True | 0 |
| Tongji | B7 | S1->S2 | 2705 | 0.001 | 0.00099859944 | 0.60891667 | 0.0010007003 | True | 0 |
| Tongji | B7 | S2->S1 | 42 | 0.001 | 0.00099929972 | 0.72075 | 0.00099929972 | False | 0 |
| Tongji | B7 | S2->S1 | 2026 | 0.001 | 0.00099789916 | 0.7955 | 0.00099789916 | False | 0 |
| Tongji | B7 | S2->S1 | 2705 | 0.001 | 0.00099859944 | 0.70366667 | 0.0010007003 | True | 0 |
| IITD | B1 | within | 42 | 0.001 | 0.00096961862 | 0.78571429 | 0.0010157909 | True | 0 |
| IITD | B1 | within | 2026 | 0.001 | 0.00096318025 | 0.87383798 | 0.0010069612 | True | 0 |
| IITD | B1 | within | 2705 | 0.001 | 0.00095359186 | 0.92561983 | 0.0010292738 | True | 0 |
| IITD | B6 | within | 42 | 0.001 | 0.00093883707 | 0.82492997 | 0.0010311817 | True | 0 |
| IITD | B6 | within | 2026 | 0.001 | 0.00094858661 | 0.84063745 | 0.0010069612 | True | 0 |
| IITD | B6 | within | 2705 | 0.001 | 0.00089304635 | 0.89807163 | 0.0010444101 | True | 0 |

## Paper wording

TAR@FAR is computed using a conservative empirical-FAR rule: among ROC points whose empirical FAR does not exceed the target, the reported TAR is the maximum observed TPR. The threshold audit exports the selected threshold, empirical FAR, TAR, genuine/impostor counts, and minimum FAR step for every method--dataset--direction--seed run.
