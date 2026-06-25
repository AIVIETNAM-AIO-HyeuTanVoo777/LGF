# IITD Palm-Class-Disjoint Within-Session Evaluation Summary

This document aggregates evaluation metrics for Tier-1 models on the secondary IITD palm-class-disjoint within-session protocol across three random seeds: 42, 2026, and 2705.

- **Baseline (B1)**: ResNet18 trained with Cross-Entropy and Supervised Contrastive Loss.
- **BNNeck + ArcFace (B6)**: ResNet18 trained with BNNeck and ArcFace Loss.

## 1. Seed-wise Run Details

| Model | Metric | Seed 42 | Seed 2026 | Seed 2705 | Overall (Mean &plusmn; Std) |
|---|---|---|---|---|---|
| Baseline (B1) | Rank-1 | 97.10% | 97.83% | 98.55% | 97.83% ± 0.72% |
| BNNeck + ArcFace (B6) | Rank-1 | 96.01% | 99.28% | 98.55% | 97.95% ± 1.71% |
| Baseline (B1) | Rank-5 | 98.55% | 98.91% | 99.28% | 98.91% ± 0.36% |
| BNNeck + ArcFace (B6) | Rank-5 | 98.19% | 99.28% | 99.28% | 98.91% ± 0.63% |
| Baseline (B1) | Macro-F1 | 96.91% | 97.67% | 98.52% | 97.70% ± 0.81% |
| BNNeck + ArcFace (B6) | Macro-F1 | 95.83% | 99.25% | 98.51% | 97.86% ± 1.80% |
| Baseline (B1) | EER | 4.34% | 2.79% | 2.02% | 3.05% ± 1.18% |
| BNNeck + ArcFace (B6) | EER | 4.60% | 3.19% | 1.93% | 3.24% ± 1.34% |
| Baseline (B1) | TAR@FAR=1e-2 | 91.74% | 95.35% | 97.38% | 94.82% ± 2.86% |
| BNNeck + ArcFace (B6) | TAR@FAR=1e-2 | 92.16% | 93.89% | 97.11% | 94.39% ± 2.51% |
| Baseline (B1) | TAR@FAR=1e-3 | 78.57% | 87.38% | 92.56% | 86.17% ± 7.07% |
| BNNeck + ArcFace (B6) | TAR@FAR=1e-3 | 82.49% | 84.06% | 89.81% | 85.45% ± 3.85% |

## 2. Paired Performance Delta (B6 - B1)

A positive delta (pp = percentage points) indicates B6 outperformed B1.

| Metric | Seed 42 Delta | Seed 2026 Delta | Seed 2705 Delta | Overall Mean Delta |
|---|---|---|---|---|
| Rank-1 | -1.09 pp | +1.45 pp | +0.00 pp | +0.12 pp |
| Rank-5 | -0.36 pp | +0.36 pp | +0.00 pp | +0.00 pp |
| Macro-F1 | -1.08 pp | +1.59 pp | -0.01 pp | +0.17 pp |
| EER | +0.26 pp | +0.40 pp | -0.09 pp | +0.19 pp |
| TAR@FAR=1e-2 | +0.42 pp | -1.46 pp | -0.28 pp | -0.44 pp |
| TAR@FAR=1e-3 | +3.92 pp | -3.32 pp | -2.75 pp | -0.72 pp |

## 3. Key Takeaways and Insights
- **Secondary Validation Verdict**: Superseded. The IITD gallery/probe construction was corrected after this legacy aggregator was written. Use `scripts/aggregate_iitd_rerun_results.py` and `docs/results/iitd_subject_disjoint_rerun_results.md` as the authoritative IITD evidence. The corrected IITD rerun shows a near-tie: B6 has Rank-1 +0.12 pp versus B1, slightly worse EER (+0.19 pp), and lower TAR@FAR=1e-3 (-0.72 pp). IITD remains secondary within-session palm-class-disjoint validation, not cross-session evidence or universal superiority evidence.
