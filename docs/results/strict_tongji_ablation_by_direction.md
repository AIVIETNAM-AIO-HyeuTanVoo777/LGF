# Strict Tongji Ablation by Direction

This table summarizes the strict Tongji palm-class-disjoint ablation separately for S1->S2 and S2->S1.

- Input: `docs/results/strict_tongji_ablation_runs.csv`.
- Values are mean ± sample standard deviation over three seeds: 42, 2026, and 2705.
- Higher is better for Rank-1, Rank-5, Macro-F1, and TAR. Lower is better for EER.
- This by-direction view is used to support the session-direction sensitivity analysis.

## Full by-direction summary

| Method | Direction | Rank-1 | Rank-5 | Macro-F1 | EER | TAR@FAR=1e-2 | TAR@FAR=1e-3 |
|---|---|---:|---:|---:|---:|---:|---:|
| B0 ResNet18 + CE | S1->S2 | 92.94 +/- 2.91 | 96.75 +/- 2.24 | 92.48 +/- 3.07 | 5.08 +/- 1.24 | 87.08 +/- 4.26 | 71.86 +/- 6.60 |
| B0 ResNet18 + CE | S2->S1 | 93.00 +/- 0.44 | 96.72 +/- 0.38 | 92.28 +/- 0.51 | 4.62 +/- 0.40 | 87.32 +/- 0.71 | 71.17 +/- 0.32 |
| B1 ResNet18 + CE + SupCon | S1->S2 | 91.69 +/- 4.06 | 96.17 +/- 2.46 | 90.80 +/- 4.76 | 4.50 +/- 1.02 | 86.71 +/- 4.43 | 67.86 +/- 7.87 |
| B1 ResNet18 + CE + SupCon | S2->S1 | 95.08 +/- 1.26 | 97.75 +/- 0.55 | 94.63 +/- 1.30 | 4.01 +/- 0.27 | 90.54 +/- 1.63 | 75.67 +/- 5.14 |
| B4 ResNet18 + ArcFace | S1->S2 | 93.03 +/- 1.41 | 96.64 +/- 0.51 | 92.18 +/- 1.52 | 4.93 +/- 0.76 | 87.63 +/- 2.62 | 72.24 +/- 4.16 |
| B4 ResNet18 + ArcFace | S2->S1 | 92.25 +/- 0.71 | 96.14 +/- 1.39 | 91.37 +/- 0.97 | 5.17 +/- 0.51 | 86.38 +/- 1.30 | 69.35 +/- 0.90 |
| B5 ResNet18 + BNNeck + CE | S1->S2 | 94.17 +/- 0.52 | 97.28 +/- 0.75 | 93.65 +/- 0.59 | 4.44 +/- 0.63 | 89.12 +/- 2.26 | 75.02 +/- 3.94 |
| B5 ResNet18 + BNNeck + CE | S2->S1 | 93.47 +/- 2.10 | 96.97 +/- 1.41 | 92.76 +/- 2.48 | 5.01 +/- 0.40 | 86.49 +/- 2.24 | 70.27 +/- 4.45 |
| B6 ResNet18 + BNNeck + ArcFace | S1->S2 | 91.56 +/- 1.62 | 95.39 +/- 1.16 | 90.74 +/- 1.78 | 5.35 +/- 0.41 | 86.12 +/- 2.05 | 69.05 +/- 4.58 |
| B6 ResNet18 + BNNeck + ArcFace | S2->S1 | 92.86 +/- 1.77 | 96.53 +/- 0.84 | 92.07 +/- 1.89 | 5.19 +/- 0.57 | 86.34 +/- 2.64 | 70.34 +/- 4.74 |
| B7 ResNet18 + BNNeck + ArcFace + light SupCon | S1->S2 | 90.89 +/- 3.21 | 95.50 +/- 2.43 | 89.77 +/- 3.51 | 5.33 +/- 0.70 | 85.28 +/- 3.30 | 68.14 +/- 7.46 |
| B7 ResNet18 + BNNeck + ArcFace + light SupCon | S2->S1 | 94.03 +/- 1.06 | 97.08 +/- 0.00 | 93.26 +/- 1.18 | 4.42 +/- 0.42 | 88.80 +/- 2.14 | 73.99 +/- 4.88 |

## Paper compact subset

The paper table reports B1, B5, and B6 because these are the baseline, the strongest strict component variant, and the originally evaluated BNNeck+ArcFace variant.

