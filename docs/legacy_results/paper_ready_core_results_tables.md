# Paper-Ready Core Results Tables

This document consolidates the core Tongji and IITD subject-disjoint evaluation results for paper drafting.

## Table 1. Tongji primary cross-session subject-disjoint results

Metrics are reported as three-seed bidirectional mean +/- standard deviation across S1->S2 and S2->S1.

| Method | Rank-1 | Rank-5 | Macro-F1 | EER | TAR@FAR=1e-2 | TAR@FAR=1e-3 |
|---|---:|---:|---:|---:|---:|---:|
| B1 CE+SupCon | 93.3889 +/- 2.1058 | 96.9583 +/- 0.9610 | 92.7128 +/- 2.3559 | 4.2549 +/- 0.4440 | 88.6236 +/- 2.3506 | 71.7625 +/- 5.4938 |
| B6 BNNeck+ArcFace | 92.2083 +/- 1.6853 | 95.9583 +/- 0.9922 | 91.4053 +/- 1.8362 | 5.2696 +/- 0.4868 | 86.2333 +/- 2.3360 | 69.6944 +/- 4.6359 |

Delta (B6 - B1): Rank-1 -1.1806 pp; Rank-5 -1.0000 pp; Macro-F1 -1.3075 pp; EER +1.0148 pp (worse); TAR@FAR=1e-2 -2.3903 pp; TAR@FAR=1e-3 -2.0681 pp.

### Tongji paper verdict

Under the stricter development/test subject-disjoint Tongji protocol, B6 does not improve over B1 overall. B1 is stronger in the bidirectional three-seed average, and B6 only shows a limited S1->S2 low-FAR gain in TAR@FAR=1e-3.

## Table 2. IITD secondary within-dataset subject-disjoint results

Metrics are reported as three-seed mean +/- standard deviation across seeds 42, 2026, and 2705.

| Method | Rank-1 | Rank-5 | Macro-F1 | EER | TAR@FAR=1e-2 | TAR@FAR=1e-3 |
|---|---:|---:|---:|---:|---:|---:|
| B1 CE+SupCon | 89.8547 +/- 2.6733 | 92.0404 +/- 1.2768 | 90.3162 +/- 3.4373 | 2.9323 +/- 1.3236 | 94.9696 +/- 3.1926 | 86.0474 +/- 8.1076 |
| B6 BNNeck+ArcFace | 89.9943 +/- 0.7755 | 92.4300 +/- 1.2358 | 90.0528 +/- 1.7032 | 2.8778 +/- 1.5169 | 95.3141 +/- 2.5335 | 84.2259 +/- 4.9801 |

Delta (B6 - B1): Rank-1 +0.1396 pp; Rank-5 +0.3895 pp; Macro-F1 -0.2635 pp; EER -0.0545 pp (better); TAR@FAR=1e-2 +0.3445 pp; TAR@FAR=1e-3 -1.8216 pp.

### IITD paper verdict

IITD shows a mixed/near-tie secondary result. B6 slightly improves Rank-1, Rank-5, EER, and TAR@FAR=1e-2 on average, but loses MacroF1 and strict TAR@FAR=1e-3. This supports the protocol-sensitivity narrative, not a universal dominance claim.

## Safe paper claim

BNNeck + ArcFace improves the original seen-identity Tongji protocol, but it does not improve over CE + SupCon overall under the stricter development/test subject-disjoint Tongji protocol. IITD provides only mixed secondary validation. The paper should be framed as a protocol-sensitivity evaluation, not as a universal method improvement paper.
