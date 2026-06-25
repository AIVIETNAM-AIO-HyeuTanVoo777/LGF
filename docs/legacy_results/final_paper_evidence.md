# Final Paper Evidence

## Executive Decision

Executive decision: `PAPER_READY_WITH_SCOPE_LIMITS`

Main method: B6 = ResNet18 + BNNeck + ArcFace.

Evidence scope:
- Primary evidence: Tongji cross-session multi-seed evaluation with seeds 42, 2026, 2705 and both S1->S2 and S2->S1 directions.
- Secondary evidence: IITD within split seed42.
- Ablation evidence: B1, B4, B6, B7 seed42 on Tongji bidirectional average.
- No retraining or evaluation was done while creating this evidence packet.

Primary sources:
- `docs/results/b6_multiseed_summary.md`
- `docs/results/b6_multiseed_summary.json`
- `docs/results/margin_head_seed42_summary.md`
- `docs/results/tongji_seed_sweep_summary.md`
- `docs/results/b6_resnet18_bnneck_arcface_iitd_within_lr1e4_seed42_metrics.json`
- `docs/results/b1_resnet18_ce_supcon_iitd_within_lr1e4_metrics.json`
- `docs/results/b2_fixed_gabor_resnet18_iitd_within_lr1e4_metrics.json`

## Main Result: Tongji Multi-Seed

B6 vs B1 on Tongji bidirectional 3-seed average:

| Metric | B6 - B1 |
|---|---:|
| Rank-1 | +1.70 pp |
| Rank-5 | +1.21 pp |
| Macro-F1 | +1.95 pp |
| EER | -0.51 pp |
| TAR@FAR=1e-2 | +1.31 pp |
| TAR@FAR=1e-3 | +3.63 pp |

B6 vs B2 on Tongji bidirectional 3-seed average:

| Metric | B6 - B2 |
|---|---:|
| Rank-1 | +2.36 pp |
| EER | -0.65 pp |
| TAR@FAR=1e-3 | +3.41 pp |
| Params | -0.36M |
| FLOPs | -0.89G |

Interpretation: B6 clears the STRONG_GO rule from `b6_multiseed_summary.json`: Rank-1 improves by more than +1.0 pp, TAR@FAR=1e-3 improves by more than +2.0 pp, and EER improves by more than 0.5 pp relative to B1.

## IITD Secondary Result

IITD within split seed42:

| Method | Rank-1 | Rank-5 | Macro-F1 | EER | TAR@FAR=1e-2 | TAR@FAR=1e-3 |
|---|---:|---:|---:|---:|---:|---:|
| B1 ResNet18 + CE + SupCon | 99.13% | 99.57% | 98.84% | 0.36% | 99.70% | 99.41% |
| B2 FixedGaborResNet18 | 98.26% | 99.13% | 97.68% | 0.71% | 99.29% | 98.93% |
| B6 ResNet18 + BNNeck + ArcFace | 98.48% | 99.13% | 97.97% | 0.66% | 99.41% | 99.11% |

IITD conclusion: B6 remains competitive and improves over B2 on IITD, but it does not universally outperform B1. B1 remains best on IITD Rank-1, Rank-5, Macro-F1, EER, TAR@FAR=1e-2, and TAR@FAR=1e-3.

## Ablation Insight

Tongji seed42 bidirectional average:

| Method | Description | Rank-1 | EER | TAR@FAR=1e-3 | Interpretation |
|---|---|---:|---:|---:|---|
| B1 | ResNet18 + CE + SupCon | 93.39% | 2.30% | 89.75% | Strong baseline |
| B4 | ResNet18 + ArcFace | 94.35% | 2.03% | 91.86% | ArcFace improves over B1 |
| B6 | ResNet18 + BNNeck + ArcFace | 96.80% | 1.14% | 96.53% | BNNeck + ArcFace improves strongly |
| B7 | ResNet18 + BNNeck + ArcFace + light SupCon | 96.97% | 1.13% | 96.50% | SupCon does not materially improve over B6 |

Ablation conclusion:
- B4 shows that a margin head alone improves the B1 baseline.
- B6 shows that adding BNNeck to ArcFace gives the main gain.
- B7 is very close to B6 and does not materially improve the strict-FAR result over B6.

## Final Safe Claim

BNNeck + ArcFace substantially improves cross-session Tongji palmprint verification over a strong ResNet18 + CE + SupCon baseline under 3-seed bidirectional evaluation.

Scope limit: On IITD within split, B6 remains competitive but does not universally outperform the CE + SupCon baseline.

## Unsafe Claims

- Do not claim universal superiority across all datasets.
- Do not claim B6 is best on IITD within split.
- Do not claim light SupCon in B7 is necessary for the observed gain.
- Do not revive the earlier Gabor superiority claim; B6 is the supported method direction, not B2/M1.
- Do not claim a broad state-of-the-art result without external benchmark comparison and literature review.
