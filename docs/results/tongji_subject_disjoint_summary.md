# Tongji Subject-Disjoint Evaluation Summary

This document aggregates palmprint recognition metrics across three seeds (42, 2026, 2705) under the development/test subject-disjoint protocol on the Tongji dataset. It compares B1 (ResNet18 baseline with CE + SupCon) and B6 (ResNet18 BNNeck with ArcFace).

## 1. Per-Seed Raw Metrics (All 12 Runs)

| Method | Protocol | Seed | Rank-1 | Rank-5 | Macro-F1 | EER | TAR@FAR=1e-2 | TAR@FAR=1e-3 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| B1 | S1->S2 | 42 | 87.1667% | 93.4167% | 85.4722% | 5.6750% | 81.7417% | 59.8667% |
| B1 | S1->S2 | 2026 | 92.9167% | 96.9167% | 92.2701% | 3.9111% | 88.1083% | 68.0917% |
| B1 | S1->S2 | 2705 | 95.0000% | 98.1667% | 94.6454% | 3.9009% | 90.2667% | 75.6083% |
| B1 | S2->S1 | 42 | 95.5000% | 98.3333% | 95.2491% | 3.8273% | 91.0250% | 76.1917% |
| B1 | S2->S1 | 2026 | 93.6667% | 97.6667% | 93.1408% | 4.3250% | 88.7250% | 70.2833% |
| B1 | S2->S1 | 2705 | 96.0833% | 97.2500% | 95.4994% | 3.8898% | 91.8750% | 80.5333% |
| B6 | S1->S2 | 42 | 90.5000% | 95.0833% | 89.3846% | 5.7250% | 84.6583% | 65.8583% |
| B6 | S1->S2 | 2026 | 93.4167% | 96.6667% | 92.7581% | 4.9177% | 88.4667% | 74.2917% |
| B6 | S1->S2 | 2705 | 90.7500% | 94.4167% | 90.0781% | 5.4000% | 85.2417% | 67.0000% |
| B6 | S2->S1 | 42 | 91.4167% | 96.0833% | 90.6057% | 5.6250% | 84.0333% | 67.9500% |
| B6 | S2->S1 | 2026 | 94.8333% | 97.5000% | 94.2052% | 4.5417% | 89.2250% | 75.8000% |
| B6 | S2->S1 | 2705 | 92.3333% | 96.0000% | 91.4004% | 5.4083% | 85.7750% | 67.2667% |

## 2. Bidirectional Per-Seed Averages

| Method | Seed | Rank-1 Average | Rank-5 Average | Macro-F1 Average | EER Average | TAR@FAR=1e-2 Average | TAR@FAR=1e-3 Average |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| B1 | 42 | 91.3333% | 95.8750% | 90.3606% | 4.7512% | 86.3833% | 68.0292% |
| B1 | 2026 | 93.2917% | 97.2917% | 92.7054% | 4.1180% | 88.4167% | 69.1875% |
| B1 | 2705 | 95.5417% | 97.7083% | 95.0724% | 3.8954% | 91.0708% | 78.0708% |
| B6 | 42 | 90.9583% | 95.5833% | 89.9952% | 5.6750% | 84.3458% | 66.9042% |
| B6 | 2026 | 94.1250% | 97.0833% | 93.4817% | 4.7297% | 88.8458% | 75.0458% |
| B6 | 2705 | 91.5417% | 95.2083% | 90.7392% | 5.4042% | 85.5083% | 67.1333% |

## 3. Aggregated Performance (Mean ± Std)

| Method | Protocol | Rank-1 | Rank-5 | Macro-F1 | EER | TAR@FAR=1e-2 | TAR@FAR=1e-3 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| B1 | S1->S2 | 91.6944% ± 4.0572% | 96.1667% ± 2.4622% | 90.7959% ± 4.7610% | 4.4957% ± 1.0214% | 86.7056% ± 4.4322% | 67.8556% ± 7.8735% |
| B1 | S2->S1 | 95.0833% ± 1.2611% | 97.7500% ± 0.5465% | 94.6298% ± 1.2955% | 4.0141% ± 0.2711% | 90.5417% ± 1.6297% | 75.6694% ± 5.1449% |
| B1 | Bidirectional Average | 93.3889% ± 2.1058% | 96.9583% ± 0.9610% | 92.7128% ± 2.3559% | 4.2549% ± 0.4440% | 88.6236% ± 2.3506% | 71.7625% ± 5.4938% |
| B6 | S1->S2 | 91.5556% ± 1.6166% | 95.3889% ± 1.1557% | 90.7403% ± 1.7816% | 5.3476% ± 0.4062% | 86.1222% ± 2.0512% | 69.0500% ± 4.5752% |
| B6 | S2->S1 | 92.8611% ± 1.7684% | 96.5278% ± 0.8430% | 92.0704% ± 1.8910% | 5.1917% ± 0.5732% | 86.3444% ± 2.6423% | 70.3389% ± 4.7418% |
| B6 | Bidirectional Average | 92.2083% ± 1.6853% | 95.9583% ± 0.9922% | 91.4053% ± 1.8362% | 5.2696% ± 0.4868% | 86.2333% ± 2.3360% | 69.6944% ± 4.6359% |

## 4. Method Deltas (B6 - B1)

Positive values indicate that B6 achieved a higher percentage value than B1. For Rank-1, Rank-5, Macro-F1, and TAR, higher is better (positive delta is favorable to B6). For EER, lower is better (negative delta is favorable to B6).

| Protocol / Metric | Rank-1 Delta | Rank-5 Delta | Macro-F1 Delta | EER Delta | TAR@FAR=1e-2 Delta | TAR@FAR=1e-3 Delta |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| S1->S2 | -0.1389 pp | -0.7778 pp | -0.0556 pp | +0.8519 pp | -0.5833 pp | +1.1944 pp |
| S2->S1 | -2.2222 pp | -1.2222 pp | -2.5593 pp | +1.1776 pp | -4.1972 pp | -5.3306 pp |
| Bidirectional Average | -1.1806 pp | -1.0000 pp | -1.3075 pp | +1.0148 pp | -2.3903 pp | -2.0681 pp |

## 5. Final Verdict and Discussion

- **Overall Comparison**: B6 does **not** improve over B1 overall under the Tongji subject-disjoint protocol. In fact, B1 is stronger overall in the bidirectional 3-seed average, outperforming B6 across almost all core metrics including Rank-1 (-1.1806 pp delta), Macro-F1 (-1.3075 pp delta), EER (+1.0148 pp delta, where lower is better), and TAR@FAR=1e-2 (-2.3903 pp delta).
- **Directional Analysis**: 
  - **S1→S2**: B6 achieves a limited low-FAR verification gain of +1.1944 pp in TAR@FAR=1e-3. However, it lags behind B1 in other metrics such as Rank-1 (-0.1389 pp), Rank-5 (-0.7778 pp), Macro-F1 (-0.0556 pp), and EER (+0.8519 pp).
  - **S2→S1**: S2→S1 is the main failure direction for B6. It underperforms B1 significantly across all metrics, with large degradation in verification robustness at strict FAR thresholds (e.g., -4.1972 pp for TAR@FAR=1e-2 and -5.3306 pp for TAR@FAR=1e-3) and identification accuracy (e.g., -2.2222 pp for Rank-1 and -2.5593 pp for Macro-F1).
- **Paper Framing Pivot**: The original aspirational claim of B6's universal superiority under subject-disjoint evaluation is unsupported by these results. Instead, the paper must pivot to a **protocol-sensitivity evaluation** claim. While BNNeck + ArcFace improves performance under the original seen-identity Tongji protocol, it does not improve over CE + SupCon overall under the stricter subject-disjoint development/test Tongji protocol.
