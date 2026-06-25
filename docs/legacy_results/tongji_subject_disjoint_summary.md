# Tongji Subject-Disjoint Cross-Session Evaluation Summary

This document aggregates evaluation metrics for Tier-1 models on the Tongji subject-disjoint cross-session protocol across three random seeds: 42, 2026, and 2705.

- **Baseline (B1)**: ResNet18 trained with Cross-Entropy and Supervised Contrastive Loss.
- **BNNeck + ArcFace (B6)**: ResNet18 trained with BNNeck and ArcFace Loss.

## 1. Direction-Specific Run Details

### Direction: Session 1 &rarr; Session 2 (S1 &rarr; S2)

| Model | Seed 42 | Seed 2026 | Seed 2705 | Mean &plusmn; Std |
|---|---|---|---|---|
| Baseline (B1) | 87.17% | 92.92% | 95.00% | 91.69% ± 4.06% |
| BNNeck + ArcFace (B6) | 90.50% | 93.42% | 90.75% | 91.56% ± 1.62% |

### Direction: Session 2 &rarr; Session 1 (S2 &rarr; S1)

| Model | Seed 42 | Seed 2026 | Seed 2705 | Mean &plusmn; Std |
|---|---|---|---|---|
| Baseline (B1) | 95.50% | 93.67% | 96.08% | 95.08% ± 1.26% |
| BNNeck + ArcFace (B6) | 91.42% | 94.83% | 92.33% | 92.86% ± 1.77% |

## 2. Bidirectional Seed Averages (Overall Performance)

For each seed, we compute the average of the two directions (S1 &rarr; S2 and S2 &rarr; S1) to obtain the robust cross-session performance.

| Model | Metric | Seed 42 Avg | Seed 2026 Avg | Seed 2705 Avg | Overall (Mean &plusmn; Std) |
|---|---|---|---|---|---|
| Baseline (B1) | Rank-1 | 91.33% | 93.29% | 95.54% | 93.39% ± 2.11% |
| BNNeck + ArcFace (B6) | Rank-1 | 90.96% | 94.12% | 91.54% | 92.21% ± 1.69% |
| Baseline (B1) | Rank-5 | 95.88% | 97.29% | 97.71% | 96.96% ± 0.96% |
| BNNeck + ArcFace (B6) | Rank-5 | 95.58% | 97.08% | 95.21% | 95.96% ± 0.99% |
| Baseline (B1) | Macro-F1 | 90.36% | 92.71% | 95.07% | 92.71% ± 2.36% |
| BNNeck + ArcFace (B6) | Macro-F1 | 90.00% | 93.48% | 90.74% | 91.41% ± 1.84% |
| Baseline (B1) | EER | 4.75% | 4.12% | 3.90% | 4.25% ± 0.44% |
| BNNeck + ArcFace (B6) | EER | 5.68% | 4.73% | 5.40% | 5.27% ± 0.49% |
| Baseline (B1) | TAR@FAR=1e-2 | 86.38% | 88.42% | 91.07% | 88.62% ± 2.35% |
| BNNeck + ArcFace (B6) | TAR@FAR=1e-2 | 84.35% | 88.85% | 85.51% | 86.23% ± 2.34% |
| Baseline (B1) | TAR@FAR=1e-3 | 68.03% | 69.19% | 78.07% | 71.76% ± 5.49% |
| BNNeck + ArcFace (B6) | TAR@FAR=1e-3 | 66.90% | 75.05% | 67.13% | 69.69% ± 4.64% |

## 3. Paired Performance Delta (B6 - B1)

A positive delta (pp = percentage points) indicates B6 outperformed B1.

| Metric | Seed 42 Delta | Seed 2026 Delta | Seed 2705 Delta | Overall Mean Delta |
|---|---|---|---|---|
| Rank-1 | -0.37 pp | +0.83 pp | -4.00 pp | -1.18 pp |
| Rank-5 | -0.29 pp | -0.21 pp | -2.50 pp | -1.00 pp |
| Macro-F1 | -0.37 pp | +0.78 pp | -4.33 pp | -1.31 pp |
| EER | +0.92 pp | +0.61 pp | +1.51 pp | +1.01 pp |
| TAR@FAR=1e-2 | -2.04 pp | +0.43 pp | -5.56 pp | -2.39 pp |
| TAR@FAR=1e-3 | -1.13 pp | +5.86 pp | -10.94 pp | -2.07 pp |

## 4. Key Takeaways and Insights
- **Protocol-Sensitivity Verdict**: Rather than providing a universal improvement, the BNNeck + ArcFace (B6) pipeline exhibits a degradation or neutral behavior compared to Baseline (B1) under the cross-session subject-disjoint protocol on Tongji.
- These results show that the BNNeck + ArcFace variant evaluated here does not transfer into a consistent cross-session improvement, reinforcing the need for protocol-sensitive benchmarking rather than single-protocol claims.
