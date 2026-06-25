\# CosFace Baseline Audit



\## Purpose



This audit records the Phase 3 additional baseline B8.



B8 is added to address the concern that the paper should not rely only on the B0--B7 component matrix and a fixed Gabor reference.



\## Baseline definition



B8 = ResNet18 + CosFace



B8 is a generic learned metric-learning baseline. It is not a palmprint-specific architecture.



\## Protocol



Dataset/protocol:



\* Tongji strict palm-class-disjoint cross-session protocol

\* directions: S1 -> S2 and S2 -> S1

\* seeds: 42, 2026, 2705



Configs:



\* `configs/b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s1s2\_seed42.yaml`

\* `configs/b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s1s2\_seed2026.yaml`

\* `configs/b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s1s2\_seed2705.yaml`

\* `configs/b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s2s1\_seed42.yaml`

\* `configs/b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s2s1\_seed2026.yaml`

\* `configs/b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s2s1\_seed2705.yaml`



\## Recipe



\* model: `ResNet18Baseline`

\* embedding dimension: 256

\* pretrained: true

\* loss: CosFace

\* scale: 30.0

\* margin: 0.35

\* lambda\_supcon: 0.0

\* epochs: 60

\* learning rate: 0.0001

\* weight decay: 0.0001

\* gradient accumulation steps: 4

\* AMP: true

\* sampler: 8 identities x 2 instances, fallback 4



\## Result artifacts



Detail table:



\* `docs/results/strict\_tongji\_b8\_cosface\_detail.csv`



Summary table:



\* `docs/results/strict\_tongji\_additional\_baselines.csv`

\* `docs/results/strict\_tongji\_additional\_baselines.md`



Local non-versioned experiment artifacts:



\* six `metrics.json` files under `experiments/b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_\*`

\* six `scores.csv` files under `experiments/b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_\*`

\* checkpoints are local artifacts and are not committed



\## Results



\### Direction-separated summary



| Method             | Direction |  n |           Rank-1 |             EER |     TAR@FAR=1e-3 |

| ------------------ | --------- | -: | ---------------: | --------------: | ---------------: |

| ResNet18 + CosFace | S1 -> S2  |  3 | 92.361 +/- 1.754 | 5.150 +/- 0.213 | 71.703 +/- 0.959 |

| ResNet18 + CosFace | S2 -> S1  |  3 | 92.889 +/- 1.143 | 4.844 +/- 0.350 | 74.619 +/- 1.524 |

| ResNet18 + CosFace | Both      |  6 | 92.625 +/- 1.504 | 4.997 +/- 0.328 | 73.161 +/- 1.936 |



\### Per-run detail



| Direction | Seed | Rank-1 | Rank-5 | Macro-F1 |   EER | TAR@FAR=1e-2 | TAR@FAR=1e-3 |

| --------- | ---: | -----: | -----: | -------: | ----: | -----------: | -----------: |

| S1 -> S2  |   42 | 92.000 | 96.833 |   91.069 | 5.027 |       86.858 |       70.350 |

| S1 -> S2  | 2026 | 94.667 | 97.333 |   94.143 | 4.973 |       87.933 |       72.300 |

| S1 -> S2  | 2705 | 90.417 | 94.083 |   88.972 | 5.450 |       86.575 |       72.458 |

| S2 -> S1  |   42 | 94.417 | 97.500 |   93.862 | 4.350 |       90.092 |       76.483 |

| S2 -> S1  | 2026 | 92.583 | 95.667 |   91.434 | 5.075 |       88.425 |       74.625 |

| S2 -> S1  | 2705 | 91.667 | 95.250 |   90.429 | 5.108 |       87.025 |       72.750 |



\## Interpretation



B8 gives the paper an additional generic learned baseline outside the original component matrix.



B8 does not change the central Phase 2 conclusion about B6. It should be reported as an additional comparator, not as the proposed method.



\## Claim boundary



Safe wording:



\* B8 is an additional generic learned CosFace baseline.

\* B8 uses the same strict Tongji protocol and three-seed/two-direction design.

\* B8 is not palmprint-specific.

\* B8 provides a stronger generic margin-loss comparator than fixed Gabor.



Unsafe wording:



\* B8 is PalmNet, CompNet, Competitive Code, or a palmprint-specific baseline.

\* B8 is state of the art.

\* B8 proves universal superiority of margin losses.

\* B8 replaces the need for protocol-sensitive component analysis.



\## Status



PASS.



