# Paper Review Packet (Restart Aggregation Update)

## 1. Title and Abstract Summary

Paper title: "Protocol-Sensitive Evaluation of BNNeck and ArcFace Embeddings for Cross-Session Palmprint Recognition"

Abstract summary: The draft evaluates B6 (ResNet18 + BNNeck + ArcFace) against B1 (ResNet18 + CE + SupCon) under both the original seen-identity Tongji protocol and a stricter palm-class-disjoint Tongji protocol. In the seen-identity setting, B6 shows improvements. However, under the palm-class-disjoint cross-session protocol, B6 does not improve over B1 overall. An IITD palm-class-disjoint within-session protocol is included as secondary validation and is best interpreted as a near-tie between B6 and B1.

## 2. Main Claim and Scope

- **Main Supported Claim**: Protocol-sensitive evaluation on Tongji. The test protocol is a first-order determinant of embedding performance under session shift.
- **Key Finding**: B6 (BNNeck + ArcFace) does not improve over B1 overall under the stricter palm-class-disjoint cross-session Tongji protocol.
  - Bidirectional 3-seed Rank-1 average: B6 trails B1 by -1.18 percentage points (92.21% vs 93.39%).
  - Bidirectional 3-seed EER average: B6 is 1.01 percentage points worse than B1 (5.27% vs 4.25%).
- **IITD Status**: IITD palm-class-disjoint within-session validation is now included as secondary evidence. B6 is near-tied with B1: Rank-1 is 89.99% +/- 0.78% for B6 versus 89.85% +/- 2.67% for B1, with a mean Rank-1 delta of +0.14 pp; B6 trails B1 at TAR@FAR=1e-3 by -1.82 pp.
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
| IITD Palm-Class-Disjoint Within-Session | B1 vs B6 | Rank-1 / TAR@FAR=1e-3 | B6 Rank-1 +0.14 pp; B6 TAR@FAR=1e-3 -1.82 pp | `docs/results/iitd_subject_disjoint_summary.md` | Match |

## 4. Overall Review Verdict

VERDICT: PASS (With Scoped Evidence)

Reason: The paper draft is aligned with the restart evidence and uses conservative palm-class-disjoint terminology. Tongji remains the primary cross-session palm-class-disjoint evidence, while IITD is included only as secondary within-session palm-class-disjoint validation. The IITD result supports a near-tie interpretation rather than a universal BNNeck + ArcFace improvement claim.
