# Paired Statistical Evidence for Strict Component Ablation

This analysis extends the existing B6-vs-B1 paired uncertainty analysis to the component-ablation comparisons needed by the paper claim, especially B5.

## Method

- Input: `docs/results/strict_tongji_ablation_runs.csv`.
- Paired units: six matched seed-direction units: S1->S2 and S2->S1 for seeds 42, 2026, and 2705.
- Delta definition: method A minus method B, in percentage points.
- Positive Rank-1, Rank-5, Macro-F1, and TAR deltas favor method A.
- Positive EER deltas are worse for method A.
- Bootstrap CI: percentile bootstrap over paired units, 50000 resamples, seed 20260624.
- Exact sign-flip test: two-sided paired sign-flip test over six deltas.
- Because n=6, p-values are coarse uncertainty diagnostics, not definitive significance claims.

## Summary table

| Comparison | Metric | Mean delta (pp) | SD (pp) | Bootstrap 95% CI (pp) | Exact sign-flip p | Interpretation |
|---|---|---:|---:|---:|---:|---|
| B5 minus B1 | Rank-1 | +0.43 | 3.41 | [-1.74, +3.13] | 0.8125 | B5 better |
| B5 minus B1 | Rank-5 | +0.17 | 1.63 | [-0.90, +1.47] | 0.8125 | B5 better |
| B5 minus B1 | Macro-F1 | +0.49 | 3.93 | [-2.01, +3.62] | 0.8438 | B5 better |
| B5 minus B1 | EER | +0.47 | 0.67 | [-0.03, +0.94] | 0.1875 | B5 worse |
| B5 minus B1 | TAR@FAR=1e-2 | -0.82 | 4.06 | [-3.73, +2.23] | 0.6562 | B5 worse |
| B5 minus B1 | TAR@FAR=1e-3 | +0.88 | 8.28 | [-5.38, +6.63] | 0.8125 | B5 better |
| B5 minus B6 | Rank-1 | +1.61 | 2.83 | [-0.64, +3.51] | 0.1562 | B5 better |
| B5 minus B6 | Rank-5 | +1.17 | 1.77 | [-0.17, +2.43] | 0.1875 | B5 better |
| B5 minus B6 | Macro-F1 | +1.80 | 3.08 | [-0.62, +3.85] | 0.1562 | B5 better |
| B5 minus B6 | EER | -0.54 | 0.77 | [-1.07, +0.05] | 0.1562 | B5 better |
| B5 minus B6 | TAR@FAR=1e-2 | +1.57 | 3.79 | [-1.27, +4.20] | 0.3125 | B5 better |
| B5 minus B6 | TAR@FAR=1e-3 | +2.95 | 7.25 | [-2.49, +8.00] | 0.4375 | B5 better |
| B6 minus B1 | Rank-1 | -1.18 | 3.26 | [-3.32, +1.26] | 0.4688 | B6 worse |
| B6 minus B1 | Rank-5 | -1.00 | 1.87 | [-2.35, +0.37] | 0.2500 | B6 worse |
| B6 minus B1 | Macro-F1 | -1.31 | 3.62 | [-3.67, +1.44] | 0.4688 | B6 worse |
| B6 minus B1 | EER | +1.01 | 0.73 | [+0.48, +1.52] | 0.0312 | B6 worse |
| B6 minus B1 | TAR@FAR=1e-2 | -2.39 | 4.15 | [-5.29, +0.58] | 0.2500 | B6 worse |
| B6 minus B1 | TAR@FAR=1e-3 | -2.07 | 8.91 | [-8.46, +3.63] | 0.5625 | B6 worse |

## Paper-relevant interpretation

- B5 versus B1: B5 has positive mean paired deltas for Rank-1 and TAR@FAR=1e-3, with Rank-1 +0.43 pp and TAR@FAR=1e-3 +0.88 pp. This supports describing B5 as a modestly favorable BNNeck+CE component variant rather than a large statistically established improvement.
- B5 versus B6: B5 has better mean paired low-FAR behavior than B6, including TAR@FAR=1e-3 +2.95 pp and EER -0.54 pp (negative EER favors B5). This supports the paper statement that B5 is stronger than the ArcFace-based B6 under the strict Tongji protocol.
- B6 versus B1: B6 remains unfavorable on the bidirectional paired average, with Rank-1 -1.18 pp and EER +1.01 pp (positive EER is worse). This is consistent with the existing B6-vs-B1 paired analysis.

## Per-unit deltas

The machine-readable per-unit deltas are embedded in the `deltas_pp` column of the CSV output.
