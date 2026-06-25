# Tongji Directional Delta: B6 - B1

## Interpretation
- Positive Rank/TAR deltas favor B6.
- Positive EER deltas indicate B6 is worse.

## Per-seed delta table

| Direction | Seed | Delta Rank-1 | Delta Rank-5 | Delta Macro-F1 | Delta EER | Delta TAR@1e-2 | Delta TAR@1e-3 |
|---|---|---|---|---|---|---|---|
| s1_to_s2 | 42 | +3.33 pp | +1.67 pp | +3.91 pp | +0.05 pp | +2.92 pp | +5.99 pp |
| s1_to_s2 | 2026 | +0.50 pp | -0.25 pp | +0.49 pp | +1.01 pp | +0.36 pp | +6.20 pp |
| s1_to_s2 | 2705 | -4.25 pp | -3.75 pp | -4.57 pp | +1.50 pp | -5.02 pp | -8.61 pp |
| s2_to_s1 | 42 | -4.08 pp | -2.25 pp | -4.64 pp | +1.80 pp | -6.99 pp | -8.24 pp |
| s2_to_s1 | 2026 | +1.17 pp | -0.17 pp | +1.06 pp | +0.22 pp | +0.50 pp | +5.52 pp |
| s2_to_s1 | 2705 | -3.75 pp | -1.25 pp | -4.10 pp | +1.52 pp | -6.10 pp | -13.27 pp |

## Direction-level mean delta

| Direction | Mean Delta Rank-1 | Mean Delta EER | Mean Delta TAR@FAR=1e-3 |
|---|---|---|---|
| s1_to_s2 | -0.14 pp | +0.85 pp | +1.19 pp |
| s2_to_s1 | -2.22 pp | +1.18 pp | -5.33 pp |

## Main finding
For the S1->S2 direction, B6 exhibits a limited verification gain of 1.19 percentage points at TAR@FAR=1e-3, accompanied by a small EER increase (worse) of 0.85 percentage points. For the S2->S1 direction, B6 consistently underperforms B1 across key identification and verification metrics, showing a drop of -2.22 percentage points in Rank-1 accuracy and a degradation of -5.33 percentage points in TAR@FAR=1e-3. The bidirectional average hides this directional asymmetry, where the overall negative delta is heavily driven by the S2->S1 direction.
