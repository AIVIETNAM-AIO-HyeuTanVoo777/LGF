# Final Paper Tables

All values are percentages unless otherwise stated. Mean and standard deviation are reported as `mean +/- std`.

## A. Tongji Multi-Seed Mean +/- Std

Bidirectional average over Tongji S1->S2 and S2->S1, seeds 42, 2026, 2705.

| Method | Protocol | Rank-1 | Rank-5 | Macro-F1 | EER | TAR@FAR=1e-2 | TAR@FAR=1e-3 | Time | Params | FLOPs |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| B1 ResNet18 + CE + SupCon | Bidirectional Average | 94.37 +/- 0.88 | 96.24 +/- 0.67 | 93.61 +/- 1.05 | 1.95 +/- 0.30 | 96.92 +/- 0.66 | 91.56 +/- 1.91 | 1.75 +/- 0.07 ms | 11.46 +/- 0.00M | 1.82 +/- 0.00G |
| B2 FixedGaborResNet18 | Bidirectional Average | 93.71 +/- 0.55 | 95.60 +/- 0.26 | 92.81 +/- 0.60 | 2.09 +/- 0.21 | 96.90 +/- 0.37 | 91.78 +/- 0.74 | 4.87 +/- 1.71 ms | 11.82 +/- 0.00M | 2.71 +/- 0.00G |
| B6 ResNet18 + BNNeck + ArcFace | Bidirectional Average | 96.07 +/- 0.73 | 97.45 +/- 0.59 | 95.56 +/- 0.84 | 1.45 +/- 0.30 | 98.23 +/- 0.53 | 95.20 +/- 1.21 | 4.89 +/- 0.81 ms | 11.46 +/- 0.00M | 1.82 +/- 0.00G |

## B. Direct Comparison

Bidirectional 3-seed average deltas.

| Comparison | Delta Rank-1 | Delta Rank-5 | Delta Macro-F1 | Delta EER | Delta TAR@FAR=1e-2 | Delta TAR@FAR=1e-3 | Delta Time | Delta Params | Delta FLOPs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| B6 - B1 | +1.70 pp | +1.21 pp | +1.95 pp | -0.51 pp | +1.31 pp | +3.63 pp | +3.14 ms | +0.00M | +0.00G |
| B6 - B2 | +2.36 pp | +1.85 pp | +2.75 pp | -0.65 pp | +1.33 pp | +3.41 pp | +0.03 ms | -0.36M | -0.89G |

## C. Ablation Seed42 Table

Tongji bidirectional average for seed42.

| Method | Description | Rank-1 | Rank-5 | Macro-F1 | EER | TAR@FAR=1e-2 | TAR@FAR=1e-3 |
|---|---|---:|---:|---:|---:|---:|---:|
| B1 | ResNet18 + CE + SupCon | 93.39 | 95.47 | 92.43 | 2.30 | 96.23 | 89.75 |
| B4 | ResNet18 + ArcFace | 94.35 | 96.40 | 93.65 | 2.03 | 96.83 | 91.86 |
| B6 | ResNet18 + BNNeck + ArcFace | 96.80 | 97.88 | 96.40 | 1.14 | 98.77 | 96.53 |
| B7 | ResNet18 + BNNeck + ArcFace + light SupCon | 96.97 | 97.98 | 96.60 | 1.13 | 98.77 | 96.50 |

## D. IITD Table

IITD within split, seed42.

| Method | Rank-1 | Rank-5 | Macro-F1 | EER | TAR@FAR=1e-2 | TAR@FAR=1e-3 |
|---|---:|---:|---:|---:|---:|---:|
| B1 ResNet18 + CE + SupCon | 99.13 | 99.57 | 98.84 | 0.36 | 99.70 | 99.41 |
| B2 FixedGaborResNet18 | 98.26 | 99.13 | 97.68 | 0.71 | 99.29 | 98.93 |
| B6 ResNet18 + BNNeck + ArcFace | 98.48 | 99.13 | 97.97 | 0.66 | 99.41 | 99.11 |

IITD note: B6 is competitive and better than B2, but B1 remains strongest on this saturated within-dataset split.
