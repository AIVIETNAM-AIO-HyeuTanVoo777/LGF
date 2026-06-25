# Paired Statistical Evidence: B6 vs B1

## Scope
- Dataset: Tongji.
- Protocol: palm-class-disjoint cross-session evaluation.
- Paired units: six seed-direction units: S1->S2 and S2->S1 for seeds 42, 2026, and 2705.
- Delta definition: B6 minus B1.
- Positive Rank/TAR/Macro-F1 deltas favor B6.
- Positive EER deltas indicate worse performance for B6.
- Bootstrap CI: percentile bootstrap over paired units, 50000 resamples, seed 20260624.
- Permutation test: exact two-sided sign-flip test over the six paired deltas.
- Because n=6, p-values are coarse and should be treated as uncertainty diagnostics, not definitive significance claims.

## Summary

| Metric | Mean delta (pp) | SD (pp) | Bootstrap 95% CI (pp) | Exact sign-flip p | Mean interpretation |
|---|---:|---:|---:|---:|---|
| Rank-1 | -1.18 | 3.26 | [-3.32, +1.26] | 0.4688 | B6 worse |
| Rank-5 | -1.00 | 1.87 | [-2.35, +0.39] | 0.2500 | B6 worse |
| Macro-F1 | -1.31 | 3.62 | [-3.67, +1.44] | 0.4688 | B6 worse |
| EER | +1.01 | 0.73 | [+0.48, +1.52] | 0.0312 | B6 worse |
| TAR@FAR=1e-2 | -2.39 | 4.15 | [-5.29, +0.58] | 0.2500 | B6 worse |
| TAR@FAR=1e-3 | -2.06 | 8.92 | [-8.47, +3.63] | 0.5625 | B6 worse |

## Interpretation
- The mean paired deltas are negative for Rank-1, Rank-5, Macro-F1, TAR@FAR=1e-2, and TAR@FAR=1e-3, and positive for EER.
- This direction of change is consistently unfavorable to B6 on the bidirectional average.
- However, the bootstrap intervals are wide because there are only six paired units.
- Therefore the paper should report these results as paired uncertainty evidence, not as a strong formal significance claim.
