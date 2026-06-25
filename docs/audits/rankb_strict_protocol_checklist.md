\# Rank-B Strict Protocol Checklist



\## Purpose



This checklist records the protocol safeguards used for the Rank-B revision branch.



The purpose is to prevent overclaiming and to make clear which evidence is supported by versioned scripts, split files, conservative metric exports, and local non-versioned experiment artifacts.



\## Protocol scope



Primary strict protocol:



\* Dataset: Tongji

\* Setting: palm-class-disjoint cross-session evaluation

\* Directions:



&#x20; \* S1 -> S2

&#x20; \* S2 -> S1

\* Seeds:



&#x20; \* 42

&#x20; \* 2026

&#x20; \* 2705



Secondary corrected protocol:



\* Dataset: IITD

\* Setting: corrected development/test subject-disjoint evaluation

\* Seeds:



&#x20; \* 42

&#x20; \* 2026

&#x20; \* 2705



\## Split discipline



Checklist:



\* \[x] Train/validation data are separated from final gallery/probe evaluation.

\* \[x] Tongji strict split uses cross-session gallery/probe evaluation.

\* \[x] Tongji strict split uses palm-class-disjoint development versus evaluation classes.

\* \[x] IITD corrected split separates development subjects from final test subjects.

\* \[x] Gallery/probe labels are not used for checkpoint selection.

\* \[x] Test/gallery/probe results are used only for final evaluation and analysis.

\* \[x] Any claim of subject-disjointness is restricted to protocols where subject identity is explicitly available and audited.



Boundary:



\* Safe: “palm-class-disjoint” for strict Tongji.

\* Safe: “development/test subject-disjoint” for corrected IITD.

\* Unsafe: “fully subject-disjoint Tongji” unless the split and metadata explicitly support that exact claim.



\## Metric discipline



Checklist:



\* \[x] TAR@FAR uses the conservative rule.

\* \[x] The selected empirical FAR must not exceed the target FAR.

\* \[x] Threshold evidence is exported for auditability.

\* \[x] EER and TAR@FAR are computed from score files, not manually copied from logs.

\* \[x] Low-FAR claims are treated cautiously because the number of impostor pairs determines FAR resolution.

\* \[x] Rank-1, Rank-5, Macro-F1, EER, TAR@FAR=1e-2, and TAR@FAR=1e-3 are reported separately.



Boundary:



\* Safe: “conservative TAR@FAR=1e-3.”

\* Unsafe: “nearest ROC point TAR@FAR” if it can exceed the target FAR.



\## Checkpoint-selection discipline



Checklist:



\* \[x] Checkpoints are selected using validation performance/loss, not final gallery/probe evaluation.

\* \[x] Final evaluation is run after checkpoint selection.

\* \[x] Gallery/probe score files are not used to tune hyperparameters.

\* \[x] The fixed ArcFace recipe is reported as fixed, not as a completed margin/scale sweep.



Boundary:



\* Safe: “fixed ArcFace recipe.”

\* Unsafe: “ArcFace margin/scale sensitivity sweep” unless a locked sweep is actually run and exported.



\## Baseline discipline



Checklist:



\* \[x] B1 is the main ResNet18 + CE + SupCon baseline.

\* \[x] B5 is the ResNet18 + BNNeck + CE ablation/baseline.

\* \[x] B6 is the ResNet18 + BNNeck + ArcFace fixed-recipe baseline.

\* \[x] B8 is added as an additional generic ResNet18 + CosFace margin-loss baseline.

\* \[x] Gabor is treated as a classical reference baseline.

\* \[x] Palmprint-specific external baselines are not claimed unless implemented or evaluated under the same strict protocol.



Boundary:



\* Safe: “B8 provides an additional generic learned margin-loss comparator.”

\* Unsafe: “B8 is a palmprint-specific baseline.”

\* Unsafe: “B8 replaces PalmNet, CompNet, or Competitive Code.”

\* Unsafe: “state of the art.”



\## Statistical discipline



Checklist:



\* \[x] Results are aggregated across 2 directions x 3 seeds where available.

\* \[x] Mean and standard deviation are reported for multi-run summaries.

\* \[x] Paired tests are exported for supported B1/B6 comparisons.

\* \[x] Non-significant differences are not written as improvements.

\* \[x] Best observed mean is not written as statistical superiority unless supported by the paired test.



Boundary:



\* Safe: “observed mean.”

\* Safe: “does not reliably improve.”

\* Unsafe: “significant improvement” without the corresponding test.



\## Failure-analysis discipline



Checklist:



\* \[x] Failure cases are reconstructed from saved score files and split metadata.

\* \[x] The reconstruction rule follows the evaluation script’s gallery/probe ordering.

\* \[x] Exported failure types are:



&#x20; \* false-accept top score

&#x20; \* false-reject low score

&#x20; \* rank-1 misidentification

\* \[x] Failure-case rows include probe/gallery paths and class metadata.

\* \[x] Image-quality causes are not claimed unless image-quality features are separately computed.

\* \[x] Dataset images are not inserted into figures unless display/redistribution permission is confirmed.



Boundary:



\* Safe: “score-tail failure analysis.”

\* Unsafe: “visual-quality failure cause” without additional image-quality measurements.



\## Reproducibility discipline



Checklist:



\* \[x] Scripts used for regenerated tables are versioned.

\* \[x] Markdown/CSV result tables are versioned.

\* \[x] Local experiment artifacts are used as inputs but not committed.

\* \[x] Checkpoints are not committed.

\* \[x] Binary arrays and model files are not committed.

\* \[x] Branch history is split into small commits by task.



Do not commit:



\* `experiments/`

\* `revision\_patches/`

\* `\*.pt`

\* `\*.pth`

\* `\*.ckpt`

\* `\*.onnx`

\* `\*.zip`

\* `\*.npy`

\* `\*.npz`



\## Current supported claims



Supported:



\* Conservative TAR@FAR reporting is used.

\* B6 does not reliably improve over B1 under the strict Tongji summary.

\* B8 adds a generic learned CosFace comparator under the same strict Tongji setup.

\* Failure-case analysis identifies score-tail and rank-1 error cases from saved score files and split metadata.

\* The revision package includes scripts, tables, audits, and manifests sufficient to reproduce the exported evidence from local experiment artifacts.



Not supported:



\* State-of-the-art claim.

\* Fully subject-disjoint Tongji claim unless explicitly audited as such.

\* Palmprint-specific superiority claim for B8.

\* Full ArcFace hyperparameter sensitivity sweep.

\* Visual failure-cause claim without additional image-quality analysis.



\## Status



PASS.



