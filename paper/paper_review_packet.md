# Paper Review Packet (Restart Aggregation Update)

## 1. Title and Abstract Summary

Paper title: "Protocol-Sensitive Evaluation of BNNeck and ArcFace Embeddings for Cross-Session Palmprint Recognition"

Abstract summary: The draft evaluates B6 (ResNet18 + BNNeck + ArcFace) against B1 (ResNet18 + CE + SupCon) under both the original seen-identity Tongji protocol and a stricter palm-class-disjoint Tongji protocol. In the seen-identity setting, B6 shows improvements. However, under the palm-class-disjoint cross-session protocol, B6 does not improve over B1 overall. An IITD palm-class-disjoint within-session protocol is included as secondary validation and is best interpreted as a near-tie between B6 and B1.

## 2. Main Claim and Scope

- **Main Supported Claim**: Protocol-sensitive evaluation on Tongji. The test protocol is a first-order determinant of embedding performance under session shift.
- **Key Finding**: B6 (BNNeck + ArcFace) does not improve over B1 overall under the stricter palm-class-disjoint cross-session Tongji protocol.
- **Metric-Threshold Audit**: Strict Tongji verification metrics use 12,000 genuine and 1,428,000 impostor comparisons per run; TAR@FAR uses the conservative empirical-FAR rule, with threshold evidence exported for strict Tongji and IITD.
  - Bidirectional 3-seed Rank-1 average: B6 trails B1 by -1.18 percentage points (92.21% vs 93.39%).
  - Bidirectional 3-seed EER average: B6 is 1.01 percentage points worse than B1 (5.27% vs 4.25%).
- **IITD Status**: IITD palm-class-disjoint within-session validation is now included as secondary evidence. After the corrected gallery/probe rerun, B6 is near-tied with B1: Rank-1 is 97.95% +/- 1.71% for B6 versus 97.83% +/- 0.72% for B1, with a mean Rank-1 delta of +0.12 pp; B6 trails B1 at TAR@FAR=1e-3 by -0.72 pp and has slightly worse EER.
- **Universal Superiority**: No universal superiority, broad benchmark leadership, or cross-dataset robustness claims are made.

## 3. Core Result Verification

| Dataset/Protocol | Model | Metric | Value (Paper) | Evidence Source | Verdict |
|---|---|---|---|---|---|
| Tongji Palm-Class-Disjoint | Baseline (B1) | Rank-1 | 93.39% ± 2.11% | `docs/results/tongji_subject_disjoint_summary.md` | Match |
| Tongji Palm-Class-Disjoint | BNNeck+ArcFace (B6) | Rank-1 | 92.21% ± 1.69% | `docs/results/tongji_subject_disjoint_summary.md` | Match |
| Tongji Palm-Class-Disjoint | Delta (B6 - B1) | Rank-1 | -1.18 pp | `docs/results/tongji_subject_disjoint_summary.md` | Match |
| Tongji Palm-Class-Disjoint | Baseline (B1) | EER | 4.25% ± 0.44% | `docs/results/tongji_subject_disjoint_summary.md` | Match |
| Tongji Palm-Class-Disjoint | BNNeck+ArcFace (B6) | EER | 5.27% ± 0.49% | `docs/results/tongji_subject_disjoint_summary.md` | Match |
| Tongji Palm-Class-Disjoint | Delta (B6 - B1) | EER | +1.01 pp | `docs/results/tongji_subject_disjoint_summary.md` | Match |
| Strict Tongji Component Paired Stats | B5 vs B1 / B5 vs B6 / B6 vs B1 | Rank-1 / EER / TAR@FAR=1e-3 | B5 modestly improves Rank-1/TAR@FAR=1e-3 vs B1 but has worse EER; B5 is stronger than B6 on paired means | `docs/results/paired_statistics_component_ablation.md` | Match |
| Strict Tongji By-Direction Ablation | B1/B5/B6 by S1->S2 and S2->S1 | Rank-1 / EER / TAR@FAR=1e-3 | B5 improves B1 in S1->S2 but trails B1 in S2->S1; B6 trails B1 on Rank-1/EER in both directions | `docs/results/strict_tongji_ablation_by_direction.md` | Match |
| Strict Tongji ROC/DET/Score Figures | B1/B5/B6 by S1->S2 and S2->S1 | ROC / DET / score distributions | B5 has stronger low-FAR TPR in S1->S2, while B1 is strongest in S2->S1; B6 does not show robust low-FAR improvement | `docs/results/strict_tongji_roc_det_score_figures.md` | Match |
| Training Configuration Audit | B0/B1/B4/B5/B6/B7 strict Tongji configs | Model / loss / embedding / optimizer / sampler | All final strict Tongji configs are parsed from YAML; B5 isolates BNNeck+CE and B6 isolates BNNeck+ArcFace with post-BN evaluation | `docs/audits/training_config_audit.md` | Match |
| IITD Palm-Class-Disjoint Within-Session | B1 vs B6 | Rank-1 / TAR@FAR=1e-3 | B6 Rank-1 +0.12 pp; B6 TAR@FAR=1e-3 -0.72 pp; B6 EER +0.19 pp | `docs/results/iitd_subject_disjoint_rerun_results.md` | Match |

## 4. Overall Review Verdict

VERDICT: PASS (With Scoped Evidence)

Reason: The paper draft is aligned with the restart evidence and uses conservative palm-class-disjoint terminology. Tongji remains the primary cross-session palm-class-disjoint evidence, while IITD is included only as secondary within-session palm-class-disjoint validation. The corrected IITD rerun supports a near-tie interpretation rather than a universal BNNeck + ArcFace improvement claim.
