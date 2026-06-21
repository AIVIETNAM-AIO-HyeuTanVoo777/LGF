# Paper Review Packet

## 1. Title and Abstract Summary

Paper title: "Margin-Aware BNNeck Embeddings for Cross-Session Palmprint Recognition"

Abstract summary: The draft proposes B6, a ResNet18 + BNNeck + ArcFace embedding model, for cross-session palmprint recognition. It reports bidirectional 3-seed Tongji gains over B1 ResNet18 + CE + SupCon: Rank-1 +1.70 pp, EER -0.51 pp, and TAR@FAR=1e-3 +3.63 pp. It also reports that B6 outperforms B2 FixedGaborResNet18 on Tongji while using fewer parameters and FLOPs than B2. The abstract correctly limits the IITD result: B6 is competitive but does not outperform B1 on every IITD metric.

## 2. Main Claim

Main paper claim: BNNeck + ArcFace improves cross-session Tongji palmprint verification over a strong ResNet18 + CE + SupCon baseline under 3-seed bidirectional evaluation.

Verdict on claim scope: Appropriate. The draft does not claim broad benchmark leadership, dataset-wide dominance, IITD-best performance, or Gabor superiority.

## 3. Numerical Claims and Evidence Trace

| Numerical claim in paper | Location | Evidence source | Check |
|---|---|---|---|
| B1 bidirectional Rank-1 = 94.37% | Introduction, Table 1 | `docs/results/b6_multiseed_summary.md`, Section 3; `docs/results/final_paper_tables.md`, Table A | Match |
| B1 bidirectional TAR@FAR=1e-3 = 91.56% | Introduction, Table 1 | `docs/results/b6_multiseed_summary.md`, Section 3; `docs/results/final_paper_tables.md`, Table A | Match |
| B6 - B1 Rank-1 = +1.70 pp | Abstract, Introduction, Results, Conclusion | `docs/results/b6_multiseed_summary.md`, Direct Comparison; `docs/results/final_paper_evidence.md` | Match |
| B6 - B1 Rank-5 = +1.21 pp | Results Table 2 | `docs/results/b6_multiseed_summary.md`, Direct Comparison | Match |
| B6 - B1 Macro-F1 = +1.95 pp | Results Table 2 | `docs/results/b6_multiseed_summary.md`, Direct Comparison | Match |
| B6 - B1 EER = -0.51 pp | Abstract, Introduction, Results, Discussion, Conclusion | `docs/results/b6_multiseed_summary.md`, Direct Comparison | Match |
| B6 - B1 TAR@FAR=1e-2 = +1.31 pp | Results Table 2 | `docs/results/b6_multiseed_summary.md`, Direct Comparison | Match |
| B6 - B1 TAR@FAR=1e-3 = +3.63 pp | Abstract, Introduction, Results, Discussion, Conclusion | `docs/results/b6_multiseed_summary.md`, Direct Comparison | Match |
| B6 latency overhead vs B1 = +3.14 ms | Abstract implied tradeoff, Results Table 2, Discussion | `docs/results/b6_multiseed_summary.md`, Direct Comparison | Match |
| B6 - B2 Rank-1 = +2.36 pp | Abstract, Introduction, Results | `docs/results/b6_multiseed_summary.md`, Direct Comparison; `docs/results/final_paper_evidence.md` | Match |
| B6 - B2 EER = -0.65 pp | Results Table 2 | `docs/results/b6_multiseed_summary.md`, Direct Comparison | Match |
| B6 - B2 TAR@FAR=1e-3 = +3.41 pp | Abstract, Introduction, Results | `docs/results/b6_multiseed_summary.md`, Direct Comparison | Match |
| B6 - B2 Params = -0.36M | Abstract, Results | `docs/results/b6_multiseed_summary.md`, Direct Comparison; `docs/results/final_paper_evidence.md` | Match |
| B6 - B2 FLOPs = -0.89G | Abstract, Results | `docs/results/b6_multiseed_summary.md`, Direct Comparison; `docs/results/final_paper_evidence.md` | Match |
| B6 bidirectional Rank-1 = 96.07 +/- 0.73 | Results Table 1 | `docs/results/b6_multiseed_summary.md`, Aggregated table; `docs/results/final_paper_tables.md`, Table A | Match |
| B6 bidirectional EER = 1.45 +/- 0.30 | Results Table 1 | `docs/results/b6_multiseed_summary.md`, Aggregated table; `docs/results/final_paper_tables.md`, Table A | Match |
| B6 bidirectional TAR@FAR=1e-3 = 95.20 +/- 1.21 | Results Table 1 | `docs/results/b6_multiseed_summary.md`, Aggregated table; `docs/results/final_paper_tables.md`, Table A | Match |
| IITD B1 Rank-1 = 99.13, B6 Rank-1 = 98.48 | Results Table 3 | `docs/results/final_paper_tables.md`, IITD table; `docs/results/final_paper_evidence.md` | Match |
| IITD B1 TAR@FAR=1e-3 = 99.41, B6 TAR@FAR=1e-3 = 99.11 | Results Table 3 | `docs/results/final_paper_tables.md`, IITD table; `docs/results/final_paper_evidence.md` | Match |
| B4 seed42 Rank-1 = 94.35, TAR@FAR=1e-3 = 91.86 | Ablation Table 4 | `docs/results/final_paper_tables.md`, Ablation table; `docs/results/margin_head_seed42_summary.md` | Match |
| B6 seed42 Rank-1 = 96.80, TAR@FAR=1e-3 = 96.53 | Ablation Table 4 | `docs/results/final_paper_tables.md`, Ablation table; `docs/results/margin_head_seed42_summary.md` | Match |
| B7 seed42 TAR@FAR=1e-3 = 96.50, slightly below B6 | Ablation text | `docs/results/final_paper_tables.md`, Ablation table; `docs/results/margin_head_seed42_summary.md` | Match |

## 4. Overclaim Audit

| Risk category | Finding | Evidence |
|---|---|---|
| State-of-the-art | No overclaim found. The draft says no external benchmark-leadership claim is made. | `paper/main.tex`, `paper/sections/07_discussion.tex`, Related Work |
| Universal superiority | No overclaim found. The draft avoids universal wording and states B6 does not dominate every dataset. | Abstract, Introduction, Results, Discussion, Conclusion |
| IITD best | No overclaim found. The draft explicitly says B1 remains strongest on IITD. | Results IITD subsection, Introduction, Conclusion |
| Gabor superiority | No overclaim found. The draft says Gabor variants are not the main supported method and B6 is the final direction. | Related Work, Method, Results |

## 5. Table Number Consistency

| Table | Paper location | Evidence source | Result |
|---|---|---|---|
| Tongji multi-seed mean +/- std | `paper/sections/05_results.tex`, Table `tab:tongji_multiseed` | `docs/results/b6_multiseed_summary.md`, Section 3; `docs/results/final_paper_tables.md`, Table A | PASS |
| Direct comparison | `paper/sections/05_results.tex`, Table `tab:direct_comparison` | `docs/results/b6_multiseed_summary.md`, Section 4; `docs/results/final_paper_tables.md`, Table B | PASS |
| IITD within split | `paper/sections/05_results.tex`, Table `tab:iitd` | `docs/results/final_paper_tables.md`, Table D; `docs/results/final_paper_evidence.md` | PASS |
| Ablation seed42 | `paper/sections/06_ablation.tex`, Table `tab:ablation` | `docs/results/final_paper_tables.md`, Table C; `docs/results/margin_head_seed42_summary.md` | PASS |

Note: the paper uses `+/-`, not the Windows-risky plus-minus glyph, which is good for encoding stability.

## 6. Related Work and Citation Audit

Related Work currently cites:
- `gao2025deeplearning`
- `khosla2020supervised`
- `deng2019arcface`
- `luo2019strong`

Citation status:
- No fabricated citations found in the LaTeX draft.
- Risky palmprint/domain-adaptation citations are intentionally not in `references.bib`.
- Related Work is intentionally conservative and acknowledges that broader cross-domain literature needs verified metadata before citation.

Warning: `gao2025deeplearning` has year 2026 in `references.bib` while the key name is 2025. This is acceptable if the key follows the arXiv/report naming, but the final bibliography should keep the IEEE publication year as 2026 and mention arXiv availability if needed.

## 7. Method Check

B6 method description in `paper/sections/03_method.tex` matches implementation/evidence:
- ResNet18 backbone: present.
- 256-D embedding projection: present.
- BNNeck after projection: present.
- ArcFace normalized classifier: present.
- ArcFace scale and margin: `s=30.0`, `m=0.5`, present.
- Post-BN L2-normalized embedding for evaluation: present.
- Cosine similarity for gallery/probe matching: present.
- B1 baseline as CE + SupCon: present.
- Gabor not described as main method: correct.

Verdict: PASS.

## 8. Experimental Setup Check

Covered:
- Tongji S1->S2 and S2->S1 protocols.
- IITD within split as secondary validation.
- Compared methods B1, B2, B4, B6, B7.
- Seeds 42, 2026, 2705 for Tongji.
- Metrics Rank-1, Rank-5, Macro-F1, EER, TAR@FAR=1e-2, TAR@FAR=1e-3, params, FLOPs, latency.
- Recipe: 60 epochs, lr=1e-4, weight decay=1e-4, embedding dim 256.
- B6 ArcFace scale/margin: 30.0 / 0.5.

Gaps before final paper:
- Hardware/software environment is not fully specified.
- Dataset counts and split sizes are not yet written in the LaTeX experiment section.
- Batch sampler details, batch composition, augmentation/preprocessing, and checkpoint selection rule are not yet described in paper form.
- No LaTeX compile check has been reported in this review.

Verdict: PASS_WITH_WARNINGS.

## 9. Results, Ablation, Discussion Consistency

Results:
- Consistent with evidence.
- Correctly states B6 improves B1 on Tongji multi-seed.
- Correctly states B6 improves B2 on Tongji and is lighter than B2.
- Correctly states IITD B1 remains strongest.

Ablation:
- Correctly states B4 improves B1.
- Correctly states B6 provides the main gain.
- Correctly states B7 does not materially improve over B6, especially strict-FAR.

Discussion:
- Correctly scopes the claim to Tongji cross-session.
- Correctly notes IITD saturation/secondary role.
- Correctly notes latency overhead.
- Correctly avoids broad benchmark leadership.

Verdict: PASS.

## 10. Overall Verdict

VERDICT: PASS_WITH_WARNINGS

Reason: The draft is numerically consistent with the evidence and avoids the major overclaims requested in the audit. The warnings are paper-completeness issues rather than correctness failures: hardware/software details, dataset counts/split sizes, preprocessing/augmentation details, and final verified literature comparison are still incomplete.

## 11. Action List Before Full Paper

1. Add verified hardware/software environment, including GPU/CPU, PyTorch/CUDA versions if available, and latency measurement context.
2. Add dataset counts and split sizes for Tongji and IITD directly in `04_experiments.tex`.
3. Add preprocessing and ROI assumptions used by the project.
4. Add training details not yet in the paper: sampler P/K, grad accumulation, AMP, checkpoint selection, batch size/effective batch size.
5. Add a reproducibility paragraph listing exact config names and aggregate scripts.
6. Verify and cite the Tongji dataset paper before submission.
7. Expand Related Work only after author/title/venue/year metadata are verified for palmprint/domain-adaptation papers.
8. Compile LaTeX locally and fix formatting issues, especially wide tables.
9. Decide whether to report latency as a limitation in the abstract or only in discussion.
10. Keep the final claim scoped to Tongji cross-session; do not broaden it without external validation.
