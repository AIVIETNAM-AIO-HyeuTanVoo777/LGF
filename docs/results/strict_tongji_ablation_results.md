# Strict Tongji Ablation Results

Terminology: the paper claim is capped at palm-class-disjoint by audit; config filenames retain historical `subject_disjoint` naming for compatibility.

## Summary by method and direction

| Method | Direction | n | Rank-1 mean+/-std (%) | Rank-5 mean+/-std (%) | EER mean+/-std (%) | TAR@1e-3 mean+/-std (%) |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| B0 ResNet18 + CE | ALL | 6 | 92.97+/-1.86 | 96.74+/-1.44 | 4.85+/-0.86 | 71.52+/-4.20 |
| B0 ResNet18 + CE | S1->S2 | 3 | 92.94+/-2.91 | 96.75+/-2.24 | 5.08+/-1.24 | 71.86+/-6.60 |
| B0 ResNet18 + CE | S2->S1 | 3 | 93.00+/-0.44 | 96.72+/-0.38 | 4.62+/-0.40 | 71.17+/-0.32 |
| B1 ResNet18 + CE + SupCon | ALL | 6 | 93.39+/-3.27 | 96.96+/-1.82 | 4.25+/-0.72 | 71.76+/-7.33 |
| B1 ResNet18 + CE + SupCon | S1->S2 | 3 | 91.69+/-4.06 | 96.17+/-2.46 | 4.50+/-1.02 | 67.86+/-7.87 |
| B1 ResNet18 + CE + SupCon | S2->S1 | 3 | 95.08+/-1.26 | 97.75+/-0.55 | 4.01+/-0.27 | 75.67+/-5.14 |
| B4 ResNet18 + ArcFace | ALL | 6 | 92.64+/-1.09 | 96.39+/-0.97 | 5.05+/-0.59 | 70.79+/-3.12 |
| B4 ResNet18 + ArcFace | S1->S2 | 3 | 93.03+/-1.41 | 96.64+/-0.51 | 4.93+/-0.76 | 72.24+/-4.16 |
| B4 ResNet18 + ArcFace | S2->S1 | 3 | 92.25+/-0.71 | 96.14+/-1.39 | 5.17+/-0.51 | 69.35+/-0.90 |
| B5 ResNet18 + BNNeck + CE | ALL | 6 | 93.82+/-1.42 | 97.12+/-1.02 | 4.72+/-0.56 | 72.64+/-4.57 |
| B5 ResNet18 + BNNeck + CE | S1->S2 | 3 | 94.17+/-0.52 | 97.28+/-0.75 | 4.44+/-0.63 | 75.02+/-3.94 |
| B5 ResNet18 + BNNeck + CE | S2->S1 | 3 | 93.47+/-2.10 | 96.97+/-1.41 | 5.01+/-0.40 | 70.27+/-4.45 |
| B6 ResNet18 + BNNeck + ArcFace | ALL | 6 | 92.21+/-1.68 | 95.96+/-1.10 | 5.27+/-0.45 | 69.69+/-4.23 |
| B6 ResNet18 + BNNeck + ArcFace | S1->S2 | 3 | 91.56+/-1.62 | 95.39+/-1.16 | 5.35+/-0.41 | 69.05+/-4.58 |
| B6 ResNet18 + BNNeck + ArcFace | S2->S1 | 3 | 92.86+/-1.77 | 96.53+/-0.84 | 5.19+/-0.57 | 70.34+/-4.74 |
| B7 ResNet18 + BNNeck + ArcFace + light SupCon | ALL | 6 | 92.46+/-2.75 | 96.29+/-1.76 | 4.87+/-0.72 | 71.07+/-6.48 |
| B7 ResNet18 + BNNeck + ArcFace + light SupCon | S1->S2 | 3 | 90.89+/-3.21 | 95.50+/-2.43 | 5.33+/-0.70 | 68.14+/-7.46 |
| B7 ResNet18 + BNNeck + ArcFace + light SupCon | S2->S1 | 3 | 94.03+/-1.06 | 97.08+/-0.00 | 4.42+/-0.42 | 73.99+/-4.88 |

## Per-run results

| Method | Direction | Seed | Status | Rank-1 (%) | Rank-5 (%) | Macro-F1 (%) | EER (%) | TAR@1e-2 (%) | TAR@1e-3 (%) |
| --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| B0 ResNet18 + CE | S1->S2 | 42 | OK | 89.58 | 94.17 | 88.93 | 6.44 | 82.59 | 65.56 |
| B0 ResNet18 + CE | S1->S2 | 2026 | OK | 94.50 | 98.00 | 94.12 | 4.77 | 87.60 | 71.30 |
| B0 ResNet18 + CE | S1->S2 | 2705 | OK | 94.75 | 98.08 | 94.39 | 4.03 | 91.06 | 78.72 |
| B0 ResNet18 + CE | S2->S1 | 42 | OK | 92.67 | 97.08 | 91.99 | 4.99 | 87.05 | 71.52 |
| B0 ResNet18 + CE | S2->S1 | 2026 | OK | 93.50 | 96.75 | 92.87 | 4.20 | 88.12 | 71.12 |
| B0 ResNet18 + CE | S2->S1 | 2705 | OK | 92.83 | 96.33 | 91.97 | 4.66 | 86.78 | 70.88 |
| B1 ResNet18 + CE + SupCon | S1->S2 | 42 | OK | 87.17 | 93.42 | 85.47 | 5.67 | 81.74 | 59.87 |
| B1 ResNet18 + CE + SupCon | S1->S2 | 2026 | OK | 92.92 | 96.92 | 92.27 | 3.91 | 88.11 | 68.09 |
| B1 ResNet18 + CE + SupCon | S1->S2 | 2705 | OK | 95.00 | 98.17 | 94.65 | 3.90 | 90.27 | 75.61 |
| B1 ResNet18 + CE + SupCon | S2->S1 | 42 | OK | 95.50 | 98.33 | 95.25 | 3.83 | 91.03 | 76.19 |
| B1 ResNet18 + CE + SupCon | S2->S1 | 2026 | OK | 93.67 | 97.67 | 93.14 | 4.32 | 88.72 | 70.28 |
| B1 ResNet18 + CE + SupCon | S2->S1 | 2705 | OK | 96.08 | 97.25 | 95.50 | 3.89 | 91.88 | 80.53 |
| B4 ResNet18 + ArcFace | S1->S2 | 42 | OK | 91.83 | 96.08 | 90.86 | 5.37 | 86.22 | 68.77 |
| B4 ResNet18 + ArcFace | S1->S2 | 2026 | OK | 92.67 | 97.08 | 91.83 | 5.37 | 86.02 | 71.09 |
| B4 ResNet18 + ArcFace | S1->S2 | 2705 | OK | 94.58 | 96.75 | 93.84 | 4.05 | 90.65 | 76.85 |
| B4 ResNet18 + ArcFace | S2->S1 | 42 | OK | 92.92 | 97.42 | 92.28 | 4.63 | 87.88 | 70.28 |
| B4 ResNet18 + ArcFace | S2->S1 | 2026 | OK | 92.33 | 96.33 | 91.46 | 5.64 | 85.47 | 69.28 |
| B4 ResNet18 + ArcFace | S2->S1 | 2705 | OK | 91.50 | 94.67 | 90.36 | 5.25 | 85.81 | 68.48 |
| B5 ResNet18 + BNNeck + CE | S1->S2 | 42 | OK | 93.75 | 96.50 | 93.05 | 5.13 | 86.80 | 71.57 |
| B5 ResNet18 + BNNeck + CE | S1->S2 | 2026 | OK | 94.00 | 97.33 | 93.67 | 4.30 | 89.23 | 74.18 |
| B5 ResNet18 + BNNeck + CE | S1->S2 | 2705 | OK | 94.75 | 98.00 | 94.23 | 3.90 | 91.32 | 79.31 |
| B5 ResNet18 + BNNeck + CE | S2->S1 | 42 | OK | 95.83 | 98.58 | 95.60 | 4.55 | 89.04 | 75.36 |
| B5 ResNet18 + BNNeck + CE | S2->S1 | 2026 | OK | 91.83 | 96.00 | 90.99 | 5.29 | 84.82 | 67.14 |
| B5 ResNet18 + BNNeck + CE | S2->S1 | 2705 | OK | 92.75 | 96.33 | 91.69 | 5.17 | 85.62 | 68.31 |
| B6 ResNet18 + BNNeck + ArcFace | S1->S2 | 42 | OK | 90.50 | 95.08 | 89.38 | 5.73 | 84.66 | 65.86 |
| B6 ResNet18 + BNNeck + ArcFace | S1->S2 | 2026 | OK | 93.42 | 96.67 | 92.76 | 4.92 | 88.47 | 74.29 |
| B6 ResNet18 + BNNeck + ArcFace | S1->S2 | 2705 | OK | 90.75 | 94.42 | 90.08 | 5.40 | 85.24 | 67.00 |
| B6 ResNet18 + BNNeck + ArcFace | S2->S1 | 42 | OK | 91.42 | 96.08 | 90.61 | 5.62 | 84.03 | 67.95 |
| B6 ResNet18 + BNNeck + ArcFace | S2->S1 | 2026 | OK | 94.83 | 97.50 | 94.21 | 4.54 | 89.22 | 75.80 |
| B6 ResNet18 + BNNeck + ArcFace | S2->S1 | 2705 | OK | 92.33 | 96.00 | 91.40 | 5.41 | 85.78 | 67.27 |
| B7 ResNet18 + BNNeck + ArcFace + light SupCon | S1->S2 | 42 | OK | 91.08 | 96.08 | 89.96 | 5.16 | 85.18 | 67.75 |
| B7 ResNet18 + BNNeck + ArcFace + light SupCon | S1->S2 | 2026 | OK | 94.00 | 97.58 | 93.18 | 4.72 | 88.62 | 75.79 |
| B7 ResNet18 + BNNeck + ArcFace + light SupCon | S1->S2 | 2705 | OK | 87.58 | 92.83 | 86.16 | 6.10 | 82.03 | 60.89 |
| B7 ResNet18 + BNNeck + ArcFace + light SupCon | S2->S1 | 42 | OK | 93.50 | 97.08 | 92.57 | 4.57 | 88.19 | 72.07 |
| B7 ResNet18 + BNNeck + ArcFace + light SupCon | S2->S1 | 2026 | OK | 95.25 | 97.08 | 94.62 | 3.94 | 91.17 | 79.54 |
| B7 ResNet18 + BNNeck + ArcFace + light SupCon | S2->S1 | 2705 | OK | 93.33 | 97.08 | 92.59 | 4.74 | 87.02 | 70.37 |

Missing metrics: 0