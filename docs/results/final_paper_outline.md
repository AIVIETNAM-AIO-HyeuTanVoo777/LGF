# Final Paper Outline

Title: Margin-Aware BNNeck Embeddings for Cross-Session Palmprint Recognition

## 1. Introduction

- Motivate cross-session palmprint recognition as a harder setting than within-session or saturated within-dataset evaluation.
- State the project problem: improving embedding geometry and low-FAR verification beyond a strong ResNet18 + CE + SupCon baseline.
- Summarize the final supported method: ResNet18 + BNNeck + ArcFace.
- Preview the main Tongji multi-seed result: B6 improves Rank-1, EER, and TAR@FAR=1e-3 over B1 under bidirectional 3-seed evaluation.
- State the scope limit: IITD within split remains near-saturated and B6 is competitive but not universally better than B1.

## 2. Related Work

- Discuss palmprint recognition with CNN-based embeddings at a high level.
- Discuss metric learning and classification-margin objectives conceptually: CE, SupCon, ArcFace-style angular margins.
- Discuss BNNeck as an embedding-normalization design for separating representation learning and retrieval geometry.
- Discuss low-FAR verification metrics and why TAR@FAR=1e-3 is important for deployment-style evaluation.
- Do not invent literature citations here; add citations only after a separate literature review.

## 3. Method

- Define the B1 baseline: ResNet18 + CE + SupCon.
- Define B6: ResNet18 backbone, 256-D embedding projection, BNNeck, ArcFace margin head.
- Explain normalized feature and normalized class-weight geometry used by ArcFace.
- Explain why post-BN L2-normalized embeddings are used for cosine verification.
- Clarify that B7 adds a light SupCon term only for ablation and is not the final method.

## 4. Experimental Setup

- Describe Tongji cross-session protocols: S1->S2 and S2->S1.
- State seeds: 42, 2026, 2705.
- Define metrics: Rank-1, Rank-5, Macro-F1, EER, TAR@FAR=1e-2, TAR@FAR=1e-3, latency, parameters, FLOPs.
- List compared methods: B1, B2, B4, B6, B7.
- Describe IITD within split as secondary validation.
- State reproducibility constraints: no checkpoint tensors in Git, metrics summarized from JSON/MD artifacts, and train/eval commands separated from aggregate scripts.

## 5. Results

- Present Tongji multi-seed bidirectional table for B1, B2, B6.
- Highlight B6 vs B1: +1.70 pp Rank-1, -0.51 pp EER, +3.63 pp TAR@FAR=1e-3.
- Highlight B6 vs B2: +2.36 pp Rank-1, -0.65 pp EER, +3.41 pp TAR@FAR=1e-3, -0.36M parameters, -0.89G FLOPs.
- Discuss latency: B6 improves accuracy and verification but has +3.14 ms overhead versus B1 in the recorded summary.
- Present IITD as secondary evidence and explicitly state the scope limit.

## 6. Ablation Study

- Present seed42 ablation table: B1, B4, B6, B7.
- Explain B4: ArcFace alone improves over B1.
- Explain B6: BNNeck + ArcFace gives the strongest improvement.
- Explain B7: adding light SupCon does not materially improve over B6.
- Use the ablation to justify the final method choice as B6, not B7.

## 7. Discussion and Limitations

- Discuss why margin-aware BNNeck embeddings may improve cross-session geometry and low-FAR verification.
- Discuss that the claim is strongest on Tongji cross-session, not universal across all datasets.
- Discuss IITD saturation and why it is not the primary contribution evidence.
- Discuss latency overhead versus B1.
- Discuss that broader claims require external datasets or stronger session-robust experiments.

## 8. Conclusion

- Restate the supported claim: B6 improves cross-session Tongji verification over a strong B1 baseline under 3-seed bidirectional evaluation.
- State the practical takeaway: margin-aware BNNeck embeddings are a stronger direction than the earlier Gabor variants in this repo.
- Restate the scope limit for IITD.
- Recommend future work: external validation and session-robust metric learning.
