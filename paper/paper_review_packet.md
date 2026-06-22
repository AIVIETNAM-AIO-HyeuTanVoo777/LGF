# Paper Review Packet (Restart Aggregation Update)

## 1. Title and Abstract Summary

Paper title: "Protocol-Sensitive Evaluation of BNNeck and ArcFace Embeddings for Cross-Session Palmprint Recognition"

Abstract summary: The draft evaluates B6 (ResNet18 + BNNeck + ArcFace) against B1 (ResNet18 + CE + SupCon) under both the original seen-identity Tongji protocol and a stricter subject-disjoint Tongji protocol. In the seen-identity setting, B6 shows improvements. However, under the subject-disjoint cross-session protocol, B6 does not improve over B1 overall. An IITD subject-disjoint protocol is prepared but not used as current experimental evidence.

## 2. Main Claim and Scope

- **Main Supported Claim**: Protocol-sensitive evaluation on Tongji. The test protocol is a first-order determinant of embedding performance under session shift.
- **Key Finding**: B6 (BNNeck + ArcFace) does not improve over B1 overall under the stricter subject-disjoint cross-session Tongji protocol.
  - Bidirectional 3-seed Rank-1 average: B6 trails B1 by -1.18 percentage points (92.21% vs 93.39%).
  - Bidirectional 3-seed EER average: B6 is 1.01 percentage points worse than B1 (5.27% vs 4.25%).
- **IITD Status**: IITD within-dataset subject-disjoint protocol is a placeholder and not used as experimental evidence in the current version of the paper.
- **Universal Superiority**: No universal superiority, broad benchmark leadership, or cross-dataset robustness claims are made.

## 3. Core Result Verification

| Dataset/Protocol | Model | Metric | Value (Paper) | Evidence Source | Verdict |
|---|---|---|---|---|---|
| Tongji Subject-Disjoint | Baseline (B1) | Rank-1 | 93.39% ± 2.11% | `docs/results/tongji_subject_disjoint_summary.md` | Match |
| Tongji Subject-Disjoint | BNNeck+ArcFace (B6) | Rank-1 | 92.21% ± 1.69% | `docs/results/tongji_subject_disjoint_summary.md` | Match |
| Tongji Subject-Disjoint | Delta (B6 - B1) | Rank-1 | -1.18 pp | `docs/results/tongji_subject_disjoint_summary.md` | Match |
| Tongji Subject-Disjoint | Baseline (B1) | EER | 4.25% ± 0.44% | `docs/results/tongji_subject_disjoint_summary.md` | Match |
| Tongji Subject-Disjoint | BNNeck+ArcFace (B6) | EER | 5.27% ± 0.49% | `docs/results/tongji_subject_disjoint_summary.md` | Match |
| Tongji Subject-Disjoint | Delta (B6 - B1) | EER | +1.01 pp | `docs/results/tongji_subject_disjoint_summary.md` | Match |
| IITD | N/A | N/A | N/A | `docs/results/iitd_subject_disjoint_summary.md` (Placeholder) | Match |

## 4. Overall Review Verdict

VERDICT: PASS (With Scoped Evidence)

Reason: The paper draft has been successfully aligned with the restart evidence. Stale claims and fake tables regarding IITD metrics have been removed, and the Tongji metrics match the aggregated experimental logs perfectly.
