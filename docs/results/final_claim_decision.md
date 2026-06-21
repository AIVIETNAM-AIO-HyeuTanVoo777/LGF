# Final Claim Decision

## Supported Claims

- B6, defined as ResNet18 + BNNeck + ArcFace, substantially improves cross-session Tongji palmprint recognition over B1 under 3-seed bidirectional evaluation.
- The strongest B6 improvement is in strict-FAR verification: B6 improves TAR@FAR=1e-3 over B1 by +3.63 percentage points.
- B6 also improves Rank-1 by +1.70 percentage points and reduces EER by -0.51 percentage points relative to B1.
- B6 outperforms B2 FixedGaborResNet18 on Tongji bidirectional multi-seed results while using fewer parameters and lower FLOPs than B2.
- ArcFace alone helps: B4 improves over B1 in seed42 bidirectional average.
- BNNeck + ArcFace provides the main gain: B6 is much stronger than B4 on Tongji seed42.

## Partially Supported Claims

- B7, which adds light SupCon to BNNeck + ArcFace, is competitive with B6 but not materially better. It can be discussed as an ablation, not as the main method.
- B6 remains competitive on IITD within split and improves over B2, but this does not establish universal superiority.
- B6 is paper-ready for a scoped cross-session Tongji claim, but the scope must explicitly separate cross-session Tongji from saturated IITD within-dataset behavior.

## Unsupported Claims

- B6 is universally better than B1 across all datasets.
- B6 is the best method on IITD within split.
- Light SupCon is required for the main improvement.
- Fixed or learnable Gabor is the strongest project direction after B6.
- The current results prove a broad state-of-the-art claim without external benchmark comparison.

## Final Recommended Claim

BNNeck + ArcFace substantially improves cross-session Tongji palmprint verification over a strong ResNet18 + CE + SupCon baseline under 3-seed bidirectional evaluation.

Scope limit: On IITD within split, the proposed method remains competitive but does not universally outperform the CE + SupCon baseline.

## Reviewer-Risk Notes

- The main claim should be framed around cross-session Tongji, not universal palmprint recognition.
- IITD is a within-dataset split with near-saturated performance. It should be used as a secondary sanity check, not as the primary contribution evidence.
- B6 increases latency over B1 by +3.14 ms on the recorded bidirectional average, despite matching B1 parameter count and FLOPs in the reported tables.
- The paper should avoid claiming that SupCon and ArcFace are complementary unless additional evidence shows B7 consistently improves over B6.
- The paper should not reuse the earlier Gabor superiority framing, because B6 provides the stronger and cleaner evidence.

## How To Phrase Contribution In Paper

- Present B6 as a margin-aware embedding method using BNNeck and ArcFace for cross-session palmprint verification.
- Emphasize the low-FAR verification improvement, especially TAR@FAR=1e-3.
- State that the baseline is strong: ResNet18 + CE + SupCon already performs well, making the B6 gain meaningful.
- Include B4/B6/B7 as an ablation sequence: ArcFace helps, BNNeck + ArcFace is the key improvement, light SupCon is not necessary.
- Include the IITD result as a limitation-aware secondary check: competitive but not universally superior.
