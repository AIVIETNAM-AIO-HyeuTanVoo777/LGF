\# Related Work and Protocol Sensitivity Audit



\## Purpose



This audit records the Phase 3 related-work and protocol-sensitivity positioning.



The goal is not to add a new literature survey or new benchmark claim. The goal is to ensure that the paper’s related-work framing, protocol interpretation, and baseline claims remain aligned with the evidence currently exported in the repository.



\## Current paper positioning



The current paper already uses a protocol-sensitive framing:



\* the strict Tongji result is treated as the primary evidence,

\* the IITD corrected protocol is treated as secondary validation,

\* B6 is not claimed to improve over B1 overall,

\* B5 is described as the highest observed mean on selected strict metrics, not as a statistically established winner,

\* Gabor is described as a classical palmprint texture reference, not as a reimplementation of PalmNet, CompNet, or Competitive Code,

\* external benchmark leadership and cross-dataset robustness are not claimed.



This framing should be preserved.



\## Related-work scope



The paper should distinguish four comparator categories:



\### 1. Classical palmprint texture references



Examples:



\* Gabor texture reference

\* Competitive-Code-style orientation coding, where cited as prior work only



Allowed framing:



\* Classical texture representations remain relevant as palmprint-specific references.

\* The fixed Gabor row is a protocol-normalized classical reference.

\* The fixed Gabor row is not a full reimplementation of Competitive Code.



Disallowed framing:



\* Do not claim that the fixed Gabor baseline equals Competitive Code.

\* Do not claim that the paper fully benchmarks all classical palmprint systems.



\### 2. Palmprint-specific deep models



Examples:



\* PalmNet

\* CompNet

\* other palmprint-specific CNN/transformer systems if cited



Allowed framing:



\* These methods motivate the need for palmprint-specific comparisons.

\* They may be cited as prior palmprint-specific architectures.



Disallowed framing:



\* Do not claim direct superiority over PalmNet, CompNet, or other external models unless they are reimplemented or evaluated under the same strict protocol.

\* Do not mix numbers from incompatible protocols into a direct leaderboard.



\### 3. Generic learned embedding baselines



Examples in this repository:



\* B1: ResNet18 + CE + SupCon

\* B5: ResNet18 + BNNeck + CE

\* B6: ResNet18 + BNNeck + ArcFace

\* B8: ResNet18 + CosFace



Allowed framing:



\* These are generic learned embedding baselines under the same strict Tongji protocol.

\* B8 adds a generic CosFace margin-loss comparator outside the original B0--B7 component matrix.

\* B8 helps answer whether another angular-margin family behaves differently from the fixed ArcFace recipe.



Disallowed framing:



\* Do not call B8 palmprint-specific.

\* Do not treat B8 as a replacement for palmprint-specific baselines.

\* Do not claim that CosFace is generally superior based only on the current six strict Tongji runs.



\### 4. Protocol-sensitive evaluation studies



The paper’s strongest contribution is not a new architecture. It is an audited protocol-sensitive evaluation showing that conclusions can change between seen-identity diagnostics and stricter development/test palm-class-disjoint evaluation.



Allowed framing:



\* Protocol design is a first-order determinant of the empirical conclusion.

\* Seen-identity gains do not necessarily transfer to held-out palm-class cross-session evaluation.

\* Session direction can change the ranking of component choices.

\* Low-FAR score-tail behavior should be reported separately from Rank-1 identification.



Disallowed framing:



\* Do not frame the paper as a state-of-the-art architecture paper.

\* Do not claim dataset-independent superiority.

\* Do not claim cross-dataset robustness from the current evidence.



\## B8 interpretation



B8 result summary:



| Method             | Direction |  n |           Rank-1 |             EER |     TAR@FAR=1e-3 |

| ------------------ | --------- | -: | ---------------: | --------------: | ---------------: |

| ResNet18 + CosFace | S1 -> S2  |  3 | 92.361 +/- 1.754 | 5.150 +/- 0.213 | 71.703 +/- 0.959 |

| ResNet18 + CosFace | S2 -> S1  |  3 | 92.889 +/- 1.143 | 4.844 +/- 0.350 | 74.619 +/- 1.524 |

| ResNet18 + CosFace | Both      |  6 | 92.625 +/- 1.504 | 4.997 +/- 0.328 | 73.161 +/- 1.936 |



Evidence-safe interpretation:



\* B8 is competitive with the existing learned baselines.

\* B8 improves the comparator set by adding another generic margin-loss formulation.

\* B8 does not overturn the main conclusion that B6 is protocol-sensitive and not reliably superior to B1.

\* B8 does not establish a broad CosFace superiority claim.



\## Relationship to B1/B5/B6/Gabor



Suggested comparator language:



\* B1 remains the main CE + SupCon baseline.

\* B5 remains the strongest observed strict component variant on selected mean metrics among the original component-ablation rows.

\* B6 remains the originally hypothesized BNNeck + ArcFace variant and is retained because it is the main protocol-sensitivity subject.

\* B8 is an additional generic CosFace comparator.

\* Fixed Gabor remains the palmprint-specific classical reference.



Do not collapse these into a single leaderboard without explaining protocol and method category.



\## Paper-section implications



\### Related work



Recommended addition:



\* Add a short paragraph clarifying that the revision separates palmprint-specific methods, classical texture references, and generic metric-learning baselines.

\* Mention that B8 is included as a generic CosFace comparator, not as a palmprint-specific baseline.

\* Avoid claiming direct comparison to PalmNet, CompNet, or Competitive Code.



\### Discussion



Recommended addition:



\* Add one paragraph noting that the CosFace result reinforces the protocol-sensitive interpretation: changing the margin-loss formulation changes some low-FAR behavior but does not create a universal improvement.

\* Keep the conclusion scoped to strict Tongji and corrected IITD evidence.



\### Results/tables



Recommended addition:



\* Add a compact table or appendix table for B8.

\* The table should label B8 as “generic learned margin-loss baseline.”

\* Do not merge B8 into palmprint-specific baseline tables without a category column.



\## Safe wording candidates



Safe:



```text

We additionally evaluate a ResNet18 + CosFace baseline as a generic learned margin-loss comparator under the same strict Tongji protocol. This baseline expands the comparator set beyond the original component matrix, but it is not a palmprint-specific architecture and is not treated as a replacement for specialized palmprint methods.

```



Safe:



```text

The CosFace baseline is competitive on the strict Tongji runs, particularly at the low-FAR operating point, but the evidence remains protocol-scoped. It supports the need to report margin-loss behavior under fixed split and operating-point conventions rather than claiming dataset-independent superiority.

```



Safe:



```text

Our comparisons are protocol-normalized within this repository. External palmprint-specific methods are discussed as related work unless they are reimplemented and evaluated under the same split, metric, and checkpoint-selection discipline.

```



\## Unsafe wording to avoid



Unsafe:



```text

CosFace outperforms palmprint-specific methods.

```



Unsafe:



```text

Our method is state of the art.

```



Unsafe:



```text

B8 proves that margin losses solve cross-session palmprint recognition.

```



Unsafe:



```text

The Gabor row is Competitive Code.

```



Unsafe:



```text

PalmNet and CompNet are directly beaten by our method.

```



\## Decision



The current paper wording is mostly consistent with the Phase 2 and Phase 3 claim boundaries.



Recommended next action:



1\. keep this audit as the Phase 3 related-work/protocol-sensitivity record,

2\. add a compact B8 table or appendix table,

3\. add a short related-work/discussion patch only if the paper submission version must explicitly mention B8.



\## Status



PASS.



