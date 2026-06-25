# Final Rank-B Submission Readiness Audit

- Generated: 2026-06-25T13:38:49
- Branch: `restart-rankb-protocol-eval`
- HEAD: `9edc959`
- Working tree status at audit creation: `clean`

## Recent commits

```
9edc959 Add fixed Gabor strict Tongji reference baseline
b30b945 Add strict Tongji score-tail failure analysis
c125336 Fix LaTeX package and protocol table layout
4f25aa8 Strengthen protocol-sensitive evaluation framing
0308e54 Update paper narrative and references
0081d53 Add strict Tongji training config audit
b8a8f7d Add strict Tongji ROC DET score figures
3e1c7c0 Fix by-direction summary whitespace
```

## Export package

- Export directory exists: `True`
- Zip package exists: `True`
- Zip entries: `8`
- Expected package contents: `main.tex`, `references.bib`, and controlled PDF figures only.

## Structural audit

- DUP_LABELS: `[]`
- MISSING_REFS: `[]`
- MISSING_CITES: `[]`
- UNUSED_BIB_KEYS: `['kumar2008cohort']`
- MISSING_FIGS: `[]`
- RAW_INPUTS: `[]`
- ZIP_BAD: `[]`
- ZIP_MISSING: `[]`
- Counts: labels=23, refs=18, unique_cites=16, bib_keys=17, figures=6, zip_entries=8

## Claim-scope audit

Manual interpretation: hits are acceptable only when scoped, negative, background-only, or explicitly limited to the tested protocol.

### Pattern: `state-of-the-art` ? 3 hit(s)
- L21: Evaluation protocols can reverse conclusions about metric-learning components in contactless palmprint recognition. This paper presents a protocol-sensitive component evaluation of BNNeck and ArcFace under cross-session palmprint recognition, focusing on whether gains observed in a seen-identity dia
- L37: The stronger component-level observation is more specific: BNNeck with standard cross-entropy supervision has the highest observed mean among the tested variants on the main strict Tongji Rank-1 and TAR@FAR=$10^{-3}$ metrics, whereas ArcFace-based variants are not consistently beneficial. The correc
- L159: Fixed-Gabor texture features are included as a palmprint-specific reference baseline because Gabor-style orientation coding is historically important in palmprint recognition \cite{kong2004competitive,genovese2019palmnet,liang2021compnet}. However, this baseline is not the main method and is not tre

### Pattern: `SOTA` ? 0 hit(s)

### Pattern: `best` ? 3 hit(s)
- L272: For learned ResNet variants, evaluation uses the \texttt{best.pt} checkpoint produced by the training script. For every strict Tongji learned run, \texttt{best.pt} is selected using only the validation split from development palm classes. Held-out gallery and probe samples are not used for checkpoin
- L522: Table~\ref{tab:iitd_palm_class_disjoint} reports the corrected IITD rerun. B6 is again best interpreted as near-tied with B1 rather than clearly superior. Its mean Rank-1 is 97.95 $\pm$ 1.71 compared with 97.83 $\pm$ 0.72 for B1, corresponding to a small +0.12 percentage-point delta. However, B6 has
- L543: The key result is not that one component is universally best, but that the apparent ranking of BNNeck and ArcFace depends on whether the evaluation admits seen identities or enforces held-out palm classes across sessions.

### Pattern: `outperform` ? 1 hit(s)
- L727: The palm-class-disjoint results change the interpretation of the BNNeck + ArcFace variant. In the original seen-identity Tongji protocol, B6 appears favorable. However, when development and test identities are made palm-class-disjoint, B6 does not outperform the B1 CE + SupCon baseline overall. This

### Pattern: `superior` ? 9 hit(s)
- L522: Table~\ref{tab:iitd_palm_class_disjoint} reports the corrected IITD rerun. B6 is again best interpreted as near-tied with B1 rather than clearly superior. Its mean Rank-1 is 97.95 $\pm$ 1.71 compared with 97.83 $\pm$ 0.72 for B1, corresponding to a small +0.12 percentage-point delta. However, B6 has
- L530: \caption{Summary of protocol-dependent component ranking. The table summarizes observed means only and is not a claim of universal superiority.}
- L690: Table~\ref{tab:paired_statistics_component_ablation} reports paired uncertainty for the key component comparisons over the same six seed-direction units. For B5 minus B1, the paired mean deltas are +0.43 percentage points for Rank-1 and +0.88 percentage points for TAR@FAR=$10^{-3}$, while EER is +0.
- L716: The seen-identity diagnostic shows why B6 was worth evaluating under a stricter protocol: ArcFace and BNNeck improved the original diagnostic metrics, and light SupCon in B7 did not materially change the result relative to B6. However, the strict palm-class-disjoint ablation reverses the interpretat
- L733: The paired uncertainty estimates reinforce this cautious interpretation. Across the six paired Tongji seed-direction units, the mean deltas for B6 relative to B1 are unfavorable on all reported metrics, but most bootstrap intervals remain wide because of the small number of paired units. Thus, the e
- L763: The corrected IITD palm-class-disjoint within-session protocol is included as secondary validation, not as cross-session evidence. It shows that B6 is competitive with B1, but not superior: the mean Rank-1 delta is only +0.12 percentage points, while B6 has slightly worse mean EER (+0.19 percentage
- L771: These results do not imply that BNNeck or ArcFace are ineffective for palmprint embeddings. They indicate that their benefit is conditioned on protocol design, identity overlap, and session direction. A fair report must therefore distinguish seen-identity evidence from held-out palm-class evidence a
- L792: The corrected IITD palm-class-disjoint within-session protocol is included as secondary validation. It shows that B6 is near-tied with B1 rather than clearly better: B6 changes Rank-1 by only +0.12 percentage points, has slightly worse EER, and trails at TAR@FAR=$10^{-3}$ by -0.72 percentage points.
- L794: The fixed-Gabor reference additionally shows that a palmprint-specific classical texture representation can remain competitive for Rank-1 identification while failing to match learned embeddings at strict low-FAR verification. The final claim is thus scoped. The paper does not claim general superior

### Pattern: `robust` ? 5 hit(s)
- L31: Palmprint recognition is commonly evaluated as an identification and verification problem. Early online palmprint systems established the feasibility of palmprint-based personal identification \cite{zhang2003online}, while later surveys organized the field around acquisition devices, preprocessing,
- L74: Cross-session and cross-domain robustness are central issues for deployable biometric systems. Contactless and unconstrained palmprint studies show that performance can depend strongly on acquisition condition, ROI quality, and evaluation design \cite{ungureanu2020toward,matkowski2020uncontrolled}.
- L159: Fixed-Gabor texture features are included as a palmprint-specific reference baseline because Gabor-style orientation coding is historically important in palmprint recognition \cite{kong2004competitive,genovese2019palmnet,liang2021compnet}. However, this baseline is not the main method and is not tre
- L777: External benchmark leadership and cross-dataset robustness are not claimed. The fixed-Gabor baseline is included only as a protocol-normalized classical texture reference and should not be interpreted as a reimplementation of Competitive Code, PalmNet, or CompNet. The current evidence is limited to
- L794: The fixed-Gabor reference additionally shows that a palmprint-specific classical texture representation can remain competitive for Rank-1 identification while failing to match learned embeddings at strict low-FAR verification. The final claim is thus scoped. The paper does not claim general superior

### Pattern: `cross-domain` ? 1 hit(s)
- L74: Cross-session and cross-domain robustness are central issues for deployable biometric systems. Contactless and unconstrained palmprint studies show that performance can depend strongly on acquisition condition, ROI quality, and evaluation design \cite{ungureanu2020toward,matkowski2020uncontrolled}.

### Pattern: `cross-dataset` ? 4 hit(s)
- L74: Cross-session and cross-domain robustness are central issues for deployable biometric systems. Contactless and unconstrained palmprint studies show that performance can depend strongly on acquisition condition, ROI quality, and evaluation design \cite{ungureanu2020toward,matkowski2020uncontrolled}.
- L159: Fixed-Gabor texture features are included as a palmprint-specific reference baseline because Gabor-style orientation coding is historically important in palmprint recognition \cite{kong2004competitive,genovese2019palmnet,liang2021compnet}. However, this baseline is not the main method and is not tre
- L777: External benchmark leadership and cross-dataset robustness are not claimed. The fixed-Gabor baseline is included only as a protocol-normalized classical texture reference and should not be interpreted as a reimplementation of Competitive Code, PalmNet, or CompNet. The current evidence is limited to
- L794: The fixed-Gabor reference additionally shows that a palmprint-specific classical texture representation can remain competitive for Rank-1 identification while failing to match learned embeddings at strict low-FAR verification. The final claim is thus scoped. The paper does not claim general superior

### Pattern: `person-disjoint` ? 2 hit(s)
- L229: Palm-class and subject-ID fields are parsed from the repository manifest before split construction. The identity/parser audit documents the manifest fields used for \texttt{path}, \texttt{session}, \texttt{hand}, \texttt{subject\_id}, \texttt{palm\_id}, \texttt{class\_id}, and \texttt{sample\_id}. F
- L233: \caption{Schematic of the audited Tongji evaluation protocol. A palm class denotes one hand/palm instance in the manifest-level recognition labels. The split is claimed as palm-class-disjoint; independently verified person-disjointness is not asserted.}

### Pattern: `universal` ? 5 hit(s)
- L21: Evaluation protocols can reverse conclusions about metric-learning components in contactless palmprint recognition. This paper presents a protocol-sensitive component evaluation of BNNeck and ArcFace under cross-session palmprint recognition, focusing on whether gains observed in a seen-identity dia
- L159: Fixed-Gabor texture features are included as a palmprint-specific reference baseline because Gabor-style orientation coding is historically important in palmprint recognition \cite{kong2004competitive,genovese2019palmnet,liang2021compnet}. However, this baseline is not the main method and is not tre
- L530: \caption{Summary of protocol-dependent component ranking. The table summarizes observed means only and is not a claim of universal superiority.}
- L543: The key result is not that one component is universally best, but that the apparent ranking of BNNeck and ArcFace depends on whether the evaluation admits seen identities or enforces held-out palm classes across sessions.
- L545: The evidence changes the paper framing. BNNeck + ArcFace appears favorable in the original seen-identity Tongji diagnostic setting, but it does not improve over CE + SupCon overall under the stricter development/test palm-class-disjoint Tongji protocol. The supported contribution is therefore a prot

### Pattern: `novel method` ? 0 hit(s)

### Pattern: `new architecture` ? 3 hit(s)
- L21: Evaluation protocols can reverse conclusions about metric-learning components in contactless palmprint recognition. This paper presents a protocol-sensitive component evaluation of BNNeck and ArcFace under cross-session palmprint recognition, focusing on whether gains observed in a seen-identity dia
- L37: The stronger component-level observation is more specific: BNNeck with standard cross-entropy supervision has the highest observed mean among the tested variants on the main strict Tongji Rank-1 and TAR@FAR=$10^{-3}$ metrics, whereas ArcFace-based variants are not consistently beneficial. The correc
- L111: We do not introduce a new architecture. Instead, we define a controlled component matrix that isolates the effect of SupCon, ArcFace, BNNeck, and their combination under identical backbone, optimizer, embedding dimensionality, checkpoint-selection, and evaluation protocols.

## Manual claim-scope decision

- PASS: `state-of-the-art`, `universal`, `new architecture`, and `superior` hits are negative or explicitly scoped.
- PASS: `person-disjoint` hits are scoped; the paper claims palm-class-disjoint evaluation and states that independently verified person-disjointness is not asserted.
- PASS: `robust`, `cross-domain`, and `cross-dataset` hits are related-work background, future-work context, or explicit non-claims.
- PASS: `best` appears as `best.pt`, `best interpreted`, or `universally best` negation, not as an unscoped superiority claim.

## Content-scope decision

- Main claim: protocol-sensitive component evaluation of BNNeck and ArcFace under strict Tongji palm-class-disjoint cross-session evaluation.
- Not claimed: new architecture, state-of-the-art performance, universal superiority, person-disjointness beyond manifest-level fields, or cross-dataset robustness.
- Fixed-Gabor baseline: included only as a protocol-normalized palmprint-specific classical texture reference, not as Competitive Code, PalmNet, or CompNet reproduction.
- IITD: secondary within-session palm-class-disjoint validation only, not cross-session evidence.

## Page/layout note

- Current exported/Overleaf PDF build is 18 pages. Verify against the target venue page limit before submission.
- Final Overleaf compile should be checked for LaTeX errors, missing references, and large overfull boxes.

## Final status

PASS: structural/export audit is clean. Claim-scope hits were manually reviewed and are scoped, negative, or background-only.
