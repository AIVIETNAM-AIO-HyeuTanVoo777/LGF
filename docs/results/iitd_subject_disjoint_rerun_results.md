# IITD Palm-Class-Disjoint Within-Session Rerun Results

These results were regenerated after fixing the IITD gallery/probe construction so that each held-out palm class appears in both gallery and probe with no image overlap. IITD remains secondary within-session validation and is not cross-session evidence.

## Per-seed results

| Method | Seed | Rank-1 | Rank-5 | Macro-F1 | EER | TAR@FAR=1e-2 | TAR@FAR=1e-3 |
|---|---:|---:|---:|---:|---:|---:|---:|
| B1 ResNet18 + CE + SupCon | 42 | 97.10 | 98.55 | 96.91 | 4.34 | 91.74 | 78.57 |
| B1 ResNet18 + CE + SupCon | 2026 | 97.83 | 98.91 | 97.67 | 2.79 | 95.35 | 87.38 |
| B1 ResNet18 + CE + SupCon | 2705 | 98.55 | 99.28 | 98.52 | 2.02 | 97.38 | 92.56 |
| B6 ResNet18 + BNNeck + ArcFace | 42 | 96.01 | 98.19 | 95.83 | 4.60 | 92.16 | 82.49 |
| B6 ResNet18 + BNNeck + ArcFace | 2026 | 99.28 | 99.28 | 99.25 | 3.19 | 93.89 | 84.06 |
| B6 ResNet18 + BNNeck + ArcFace | 2705 | 98.55 | 99.28 | 98.51 | 1.93 | 97.11 | 89.81 |

## Three-seed mean +/- standard deviation

| Method | Rank-1 | Rank-5 | Macro-F1 | EER | TAR@FAR=1e-2 | TAR@FAR=1e-3 |
|---|---:|---:|---:|---:|---:|---:|
| B1 ResNet18 + CE + SupCon | 97.83 $\pm$ 0.72 | 98.91 $\pm$ 0.36 | 97.70 $\pm$ 0.81 | 3.05 $\pm$ 1.18 | 94.82 $\pm$ 2.86 | 86.17 $\pm$ 7.07 |
| B6 ResNet18 + BNNeck + ArcFace | 97.95 $\pm$ 1.71 | 98.91 $\pm$ 0.63 | 97.86 $\pm$ 1.80 | 3.24 $\pm$ 1.34 | 94.39 $\pm$ 2.51 | 85.45 $\pm$ 3.85 |

## Paired B6 minus B1 deltas

Positive Rank/TAR/Macro-F1 deltas favor B6. Positive EER deltas are worse for B6.

| Seed | Delta Rank-1 | Delta Rank-5 | Delta Macro-F1 | Delta EER | Delta TAR@FAR=1e-2 | Delta TAR@FAR=1e-3 |
|---:|---:|---:|---:|---:|---:|---:|
| 42 | -1.09 | -0.36 | -1.08 | 0.26 | 0.42 | 3.92 |
| 2026 | 1.45 | 0.36 | 1.59 | 0.40 | -1.46 | -3.32 |
| 2705 | 0.00 | 0.00 | -0.01 | -0.09 | -0.28 | -2.75 |

## Interpretation

The rerun supports a near-tie interpretation rather than a clear B6 improvement. B6 has a very small mean Rank-1 gain over B1, but it does not improve the low-FAR verification metrics on average and has slightly worse mean EER. This is consistent with the paper's protocol-sensitive conclusion and should not be written as universal superiority of BNNeck + ArcFace.
