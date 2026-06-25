# ArcFace Sensitivity Evidence

## Scope

This document records the ArcFace-related sensitivity evidence available in the current revision.

The evidence is a fixed-recipe component sensitivity analysis, not a hyperparameter sweep. The strict Tongji ablation includes:

- B1: CE + SupCon baseline without ArcFace.
- B4: ArcFace without BNNeck.
- B5: BNNeck + CE without ArcFace.
- B6: BNNeck + ArcFace.
- B7: BNNeck + ArcFace + light SupCon.

All ArcFace rows use the locked ArcFace recipe recorded in the training configuration audit: scale `s=30.0` and margin `m=0.5`. No gallery/probe/test data are used for ArcFace hyperparameter selection.

## Strict Tongji fixed-recipe summary

The table below is derived from `docs/results/strict_tongji_ablation_summary.csv`. Values are mean ± standard deviation over six seed-direction units under the strict Tongji palm-class-disjoint protocol.

| Method | Role | Rank-1 (%) | EER (%) | TAR@FAR=1e-3 (%) |
|---|---|---:|---:|---:|
| B1 | CE + SupCon baseline, no ArcFace | 93.39 ± 3.27 | 4.25 ± 0.72 | 71.77 ± 7.32 |
| B4 | ArcFace without BNNeck | 92.64 ± 1.09 | 5.05 ± 0.59 | 70.80 ± 3.13 |
| B5 | BNNeck + CE, no ArcFace | 93.82 ± 1.42 | 4.72 ± 0.56 | 72.65 ± 4.57 |
| B6 | BNNeck + ArcFace | 92.21 ± 1.68 | 5.27 ± 0.45 | 69.71 ± 4.23 |
| B7 | BNNeck + ArcFace + light SupCon | 92.46 ± 2.75 | 4.87 ± 0.72 | 71.08 ± 6.48 |

## Paired component evidence

The table below is derived from `docs/results/paired_statistics_component_ablation.csv`.

| Comparison | Metric | Mean delta (pp) | Bootstrap 95% CI (pp) | Sign-flip p | Interpretation |
|---|---|---:|---:|---:|---|
| B5 minus B1 | Rank-1 | +0.43 | [-1.77, +3.13] | 0.8125 | B5 better |
| B5 minus B1 | EER | +0.47 | [-0.03, +0.94] | 0.1875 | B5 worse |
| B5 minus B1 | TAR@FAR=1e-3 | +0.88 | [-5.37, +6.75] | 0.8125 | B5 better |
| B5 minus B6 | Rank-1 | +1.61 | [-0.64, +3.51] | 0.1562 | B5 better |
| B5 minus B6 | EER | -0.54 | [-1.07, +0.05] | 0.1562 | B5 better |
| B5 minus B6 | TAR@FAR=1e-3 | +2.94 | [-2.48, +8.00] | 0.4375 | B5 better |
| B6 minus B1 | Rank-1 | -1.18 | [-3.32, +1.26] | 0.4688 | B6 worse |
| B6 minus B1 | EER | +1.01 | [+0.48, +1.52] | 0.0312 | B6 worse |
| B6 minus B1 | TAR@FAR=1e-3 | -2.06 | [-8.47, +3.63] | 0.5625 | B6 worse |

## Interpretation

The fixed ArcFace recipe does not provide a reliable gain under the strict Tongji palm-class-disjoint protocol. ArcFace alone (B4) does not improve the non-ArcFace baseline on the selected strict metrics. Adding ArcFace to BNNeck (B6) is also weaker than the BNNeck+CE variant (B5) on the observed Rank-1 and TAR@FAR=1e-3 means, while B6 remains unfavorable relative to B1 on the bidirectional paired average.

This evidence supports the paper's protocol-sensitive interpretation: ArcFace-related gains observed in easier or seen-identity diagnostic settings should not be treated as sufficient evidence for held-out palm-class cross-session deployment.

## Limitation

This is not a margin-sensitivity sweep over multiple ArcFace margins or scales. A true margin sweep would require pre-registered training configurations over development-only selection criteria and must not use gallery/probe/test data for hyperparameter choice.
