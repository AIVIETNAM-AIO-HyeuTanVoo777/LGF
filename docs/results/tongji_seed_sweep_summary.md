# Tongji Cross-Session Seed Sweep Summary

This report aggregates the palmprint recognition results across multiple seeds (42, 2026, 2705) on the Tongji dataset to verify stability, robustness, and the core claim regarding fixed Gabor priors.

## 1. Per-Run Raw Metrics

| Method | Protocol | Seed | Rank-1 | Rank-5 | Macro-F1 | EER | TAR@1e-2 | TAR@1e-3 | Time | Params | FLOPs |
|---|---|---|---|---|---|---|---|---|---|---|---|
| B1 | S1->S2 | 42 | 93.65% | 95.80% | 92.71% | 2.34% | 96.26% | 89.62% | 2.03 ms | 11.46M | 1.819G |
| B1 | S1->S2 | 2026 | 94.75% | 96.48% | 94.16% | 1.95% | 97.16% | 92.53% | 2.02 ms | 11.46M | 1.819G |
| B1 | S1->S2 | 2705 | 91.93% | 94.83% | 90.82% | 2.63% | 94.88% | 85.66% | 1.69 ms | 11.46M | 1.819G |
| B1 | S2->S1 | 42 | 93.13% | 95.13% | 92.15% | 2.27% | 96.19% | 89.89% | 1.59 ms | 11.46M | 1.819G |
| B1 | S2->S1 | 2026 | 95.43% | 96.88% | 94.76% | 1.61% | 97.93% | 94.58% | 1.53 ms | 11.46M | 1.819G |
| B1 | S2->S1 | 2705 | 97.33% | 98.30% | 97.04% | 0.93% | 99.11% | 97.08% | 1.65 ms | 11.46M | 1.819G |
| B2 | S1->S2 | 42 | 93.62% | 95.68% | 92.82% | 2.13% | 96.91% | 91.89% | 2.80 ms | 11.82M | 2.709G |
| B2 | S1->S2 | 2026 | 92.18% | 94.75% | 90.98% | 2.40% | 96.05% | 89.27% | 4.11 ms | 11.82M | 2.709G |
| B2 | S1->S2 | 2705 | 93.67% | 95.73% | 92.71% | 1.87% | 97.20% | 91.75% | 6.40 ms | 11.82M | 2.709G |
| B2 | S2->S1 | 42 | 93.52% | 95.23% | 92.51% | 2.40% | 96.46% | 91.81% | 3.14 ms | 11.82M | 2.709G |
| B2 | S2->S1 | 2026 | 94.32% | 96.13% | 93.61% | 1.91% | 97.32% | 92.75% | 6.60 ms | 11.82M | 2.709G |
| B2 | S2->S1 | 2705 | 94.98% | 96.05% | 94.22% | 1.84% | 97.45% | 93.23% | 6.16 ms | 11.82M | 2.709G |

## 2. Aggregated Performance (Mean ± Std)

Aggregated over $n=3$ seeds (42, 2026, 2705). All accuracy and verification thresholds are in percentage values (%).

| Method | Protocol | Rank-1 | Rank-5 | Macro-F1 | EER | TAR@1e-2 | TAR@1e-3 | Time | Params | FLOPs |
|---|---|---|---|---|---|---|---|---|---|---|
| B1 | S1->S2 | 93.44% ± 1.42% | 95.71% ± 0.83% | 92.56% ± 1.67% | 2.31% ± 0.34% | 96.10% ± 1.15% | 89.27% ± 3.45% | 1.91 ms ± 0.19 ms | 11.46M ± 0.00M | 1.82G ± 0.00G |
| B1 | S2->S1 | 95.30% ± 2.10% | 96.77% ± 1.59% | 94.65% ± 2.45% | 1.60% ± 0.67% | 97.74% ± 1.47% | 93.85% ± 3.65% | 1.59 ms ± 0.06 ms | 11.46M ± 0.00M | 1.82G ± 0.00G |
| B1 | Bidirectional Average | 94.37% ± 0.88% | 96.24% ± 0.67% | 93.61% ± 1.05% | 1.95% ± 0.30% | 96.92% ± 0.66% | 91.56% ± 1.91% | 1.75 ms ± 0.07 ms | 11.46M ± 0.00M | 1.82G ± 0.00G |
| B2 | S1->S2 | 93.16% ± 0.84% | 95.39% ± 0.55% | 92.17% ± 1.03% | 2.14% ± 0.27% | 96.72% ± 0.60% | 90.97% ± 1.48% | 4.44 ms ± 1.82 ms | 11.82M ± 0.00M | 2.71G ± 0.00G |
| B2 | S2->S1 | 94.27% ± 0.73% | 95.81% ± 0.50% | 93.45% ± 0.87% | 2.05% ± 0.30% | 97.08% ± 0.53% | 92.60% ± 0.72% | 5.30 ms ± 1.88 ms | 11.82M ± 0.00M | 2.71G ± 0.00G |
| B2 | Bidirectional Average | 93.71% ± 0.55% | 95.60% ± 0.26% | 92.81% ± 0.60% | 2.09% ± 0.21% | 96.90% ± 0.37% | 91.78% ± 0.74% | 4.87 ms ± 1.71 ms | 11.82M ± 0.00M | 2.71G ± 0.00G |

## 3. Direct Comparison (B2 - B1 on Bidirectional Average)

Comparison of mean values:

- **Rank-1 Difference**: -0.66%
- **Macro-F1 Difference**: -0.80%
- **EER Difference**: +0.14%
- **TAR@FAR=1e-2 Difference**: -0.02%
- **TAR@FAR=1e-3 Difference**: +0.22%
- **Inference Time Difference**: +3.12 ms

## 4. Claim Decision

**Decision**: `WEAKENED`

The fixed-Gabor strict-FAR verification robustness claim is **WEAKENED**. Although B2 outperforms B1 on average (91.78% vs 91.56%), the advantage shrinks to 0.22 percentage points (below the 1.0 percentage point threshold).

---
*Report generated automatically by `aggregate_tongji_seed_sweep.py`.*
