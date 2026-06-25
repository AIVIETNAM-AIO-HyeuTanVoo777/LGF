# IITD Subject-Disjoint Within-Session Evaluation Summary

This document aggregates evaluation metrics for Tier-1 models on the secondary IITD subject-disjoint within-session protocol across three random seeds: 42, 2026, and 2705.

- **Baseline (B1)**: ResNet18 trained with Cross-Entropy and Supervised Contrastive Loss.
- **BNNeck + ArcFace (B6)**: ResNet18 trained with BNNeck and ArcFace Loss.

## 1. Seed-wise Run Details

| Model | Metric | Seed 42 | Seed 2026 | Seed 2705 | Overall (Mean &plusmn; Std) |
|---|---|---|---|---|---|
| Baseline (B1) | Rank-1 | 86.77% | 91.29% | 91.51% | 89.85% ± 2.67% |
| BNNeck + ArcFace (B6) | Rank-1 | 89.11% | 90.53% | 90.35% | 89.99% ± 0.78% |
| Baseline (B1) | Rank-5 | 90.66% | 93.18% | 92.28% | 92.04% ± 1.28% |
| BNNeck + ArcFace (B6) | Rank-5 | 91.05% | 92.80% | 93.44% | 92.43% ± 1.24% |
| Baseline (B1) | Macro-F1 | 86.35% | 92.20% | 92.40% | 90.32% ± 3.44% |
| BNNeck + ArcFace (B6) | Macro-F1 | 88.09% | 90.96% | 91.11% | 90.05% ± 1.70% |
| Baseline (B1) | EER | 4.44% | 2.37% | 1.98% | 2.93% ± 1.32% |
| BNNeck + ArcFace (B6) | EER | 4.62% | 2.20% | 1.82% | 2.88% ± 1.52% |
| Baseline (B1) | TAR@FAR=1e-2 | 91.45% | 95.77% | 97.69% | 94.97% ± 3.19% |
| BNNeck + ArcFace (B6) | TAR@FAR=1e-2 | 92.48% | 96.11% | 97.36% | 95.31% ± 2.53% |
| Baseline (B1) | TAR@FAR=1e-3 | 77.09% | 88.16% | 92.89% | 86.05% ± 8.11% |
| BNNeck + ArcFace (B6) | TAR@FAR=1e-3 | 78.80% | 85.28% | 88.60% | 84.23% ± 4.98% |

## 2. Paired Performance Delta (B6 - B1)

A positive delta (pp = percentage points) indicates B6 outperformed B1.

| Metric | Seed 42 Delta | Seed 2026 Delta | Seed 2705 Delta | Overall Mean Delta |
|---|---|---|---|---|
| Rank-1 | +2.33 pp | -0.76 pp | -1.16 pp | +0.14 pp |
| Rank-5 | +0.39 pp | -0.38 pp | +1.16 pp | +0.39 pp |
| Macro-F1 | +1.74 pp | -1.24 pp | -1.29 pp | -0.26 pp |
| EER | +0.17 pp | -0.17 pp | -0.17 pp | -0.05 pp |
| TAR@FAR=1e-2 | +1.03 pp | +0.34 pp | -0.33 pp | +0.34 pp |
| TAR@FAR=1e-3 | +1.71 pp | -2.88 pp | -4.30 pp | -1.82 pp |

## 3. Key Takeaways and Insights
- **Secondary Validation Verdict**: On IITD, B6 is best interpreted as near-tied with B1 rather than clearly superior. Mean deltas are small for Rank-1 (+0.14 pp), Rank-5 (+0.39 pp), EER (-0.05 pp; lower is better), and TAR@FAR=1e-2 (+0.34 pp), while B6 trails B1 on Macro-F1 (-0.26 pp) and TAR@FAR=1e-3 (-1.82 pp). This supports protocol-sensitive behavior, not universal improvement.
