# IITD Subject-Disjoint Within-Dataset Evaluation Summary

This document aggregates B1 and B6 performance on IITD subject-disjoint within-dataset evaluation across seeds 42, 2026, and 2705.

## Raw results

| Method | Seed | Rank-1 | Rank-5 | Macro-F1 | EER | TAR@FAR=1e-2 | TAR@FAR=1e-3 |
|---|---:|---:|---:|---:|---:|---:|---:|
| B1 CE+SupCon | 42 | 86.7704% | 90.6615% | 86.3489% | 4.4444% | 91.4530% | 77.0940% |
| B1 CE+SupCon | 2026 | 91.2879% | 93.1818% | 92.1984% | 2.3689% | 95.7699% | 88.1557% |
| B1 CE+SupCon | 2705 | 91.5058% | 92.2780% | 92.4014% | 1.9835% | 97.6860% | 92.8926% |
| B6 BNNeck+ArcFace | 42 | 89.1051% | 91.0506% | 88.0882% | 4.6154% | 92.4786% | 78.8034% |
| B6 BNNeck+ArcFace | 2026 | 90.5303% | 92.8030% | 90.9559% | 2.1997% | 96.1083% | 85.2792% |
| B6 BNNeck+ArcFace | 2705 | 90.3475% | 93.4363% | 91.1142% | 1.8182% | 97.3554% | 88.5950% |

## Three-seed mean +/- std

| Method | Rank-1 | Rank-5 | Macro-F1 | EER | TAR@FAR=1e-2 | TAR@FAR=1e-3 |
|---|---:|---:|---:|---:|---:|---:|
| B1 CE+SupCon | 89.8547% +/- 2.6733% | 92.0404% +/- 1.2768% | 90.3162% +/- 3.4373% | 2.9323% +/- 1.3236% | 94.9696% +/- 3.1926% | 86.0474% +/- 8.1076% |
| B6 BNNeck+ArcFace | 89.9943% +/- 0.7755% | 92.4300% +/- 1.2358% | 90.0528% +/- 1.7032% | 2.8778% +/- 1.5169% | 95.3141% +/- 2.5335% | 84.2259% +/- 4.9801% |

## Delta: B6 - B1

| Rank-1 | Rank-5 | Macro-F1 | EER | TAR@FAR=1e-2 | TAR@FAR=1e-3 |
|---:|---:|---:|---:|---:|---:|
| +0.1396 pp | +0.3895 pp | -0.2635 pp | -0.0545 pp | +0.3445 pp | -1.8216 pp |

## Verdict

IITD provides a mixed secondary validation result rather than a clean B6 dominance result. B6 slightly improves three-seed average Rank-1, Rank-5, EER, and TAR@FAR=1e-2, but it underperforms B1 in Macro-F1 and strict low-FAR TAR@FAR=1e-3.

Therefore, IITD should be reported as secondary within-dataset subject-disjoint validation only. It should not be used to claim universal superiority of BNNeck + ArcFace.
