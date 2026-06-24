# Paired Delta Analysis: B6 vs B1

## Scope
- This analysis uses six paired seed-direction units from Tongji subject-disjoint cross-session evaluation.
- Each unit compares B6 and B1 under the same direction and seed.
- Positive Rank/TAR deltas favor B6.
- Positive EER deltas indicate worse performance for B6.
- Because there are only six paired units, this is descriptive paired evidence, not a formal significance claim.

## Per-unit paired deltas

| Unit | Direction | Seed | Delta Rank-1 | Delta Rank-5 | Delta Macro-F1 | Delta EER | Delta TAR@1e-2 | Delta TAR@1e-3 |
|---|---|---|---|---|---|---|---|---|
| s1_to_s2_42 | s1_to_s2 | 42 | +3.33 pp | +1.67 pp | +3.91 pp | +0.05 pp | +2.92 pp | +5.99 pp |
| s1_to_s2_2026 | s1_to_s2 | 2026 | +0.50 pp | -0.25 pp | +0.49 pp | +1.01 pp | +0.36 pp | +6.20 pp |
| s1_to_s2_2705 | s1_to_s2 | 2705 | -4.25 pp | -3.75 pp | -4.57 pp | +1.50 pp | -5.02 pp | -8.61 pp |
| s2_to_s1_42 | s2_to_s1 | 42 | -4.08 pp | -2.25 pp | -4.64 pp | +1.80 pp | -6.99 pp | -8.24 pp |
| s2_to_s1_2026 | s2_to_s1 | 2026 | +1.17 pp | -0.17 pp | +1.06 pp | +0.22 pp | +0.50 pp | +5.52 pp |
| s2_to_s1_2705 | s2_to_s1 | 2705 | -3.75 pp | -1.25 pp | -4.10 pp | +1.52 pp | -6.10 pp | -13.27 pp |

## Mean paired deltas over six units

- Rank-1: -1.18 pp
- Rank-5: -1.00 pp
- Macro-F1: -1.31 pp
- EER: +1.01 pp
- TAR@1e-2: -2.39 pp
- TAR@1e-3: -2.07 pp

## Direction-level notes
- For the S1→S2 evaluation direction, the performance comparison between B6 and B1 is mixed, showing small gains on some seeds/metrics and drops on others.
- For the S2→S1 evaluation direction, the performance differences are more consistently negative for B6, indicating that B6 performs worse than B1 under this cross-session direction.
- Due to the small sample size (six paired units), this analysis presents descriptive evidence only and does not make a formal significance claim.
