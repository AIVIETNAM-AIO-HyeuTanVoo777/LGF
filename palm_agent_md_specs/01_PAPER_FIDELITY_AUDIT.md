# Paper Fidelity Audit

Source paper: **Palmprint Features Fusion Recognition Based on Conformer and Gabor**.

## Verdict

The implementation plan can be made **faithful to the paper's pipeline**, but **cannot be 100% exact at code-level reproduction** because several operational details are not specified in the paper.

The coding agent must use this audit as the source of truth.

---

## A. Paper-specified requirements — must implement exactly

### A1. Overall algorithm

The paper proposes:

```text
Palmprint ROI image
→ Gabor texture feature extraction
→ Conformer deep feature extraction
→ KCCA feature fusion
→ Knowledge-graph-based pre-classification
→ Cosine similarity matching
→ Recognition result
```

Implementation consequence:

- The main pipeline must include both Gabor and Conformer branches.
- KCCA is mandatory for fused features.
- Knowledge graph is mandatory for two-stage recognition.
- Cosine similarity is mandatory for final matching.

### A2. Gabor branch

Paper specifies:

- Palmprint ROI image is a 2D grayscale image for Gabor.
- Use a fixed multi-scale, multi-orientation Gabor filter bank.
- Use **7 scales**.
- Use **6 directions**:
  - 0°
  - 30°
  - 60°
  - 90°
  - 120°
  - 150°
- Convolve palmprint ROI with Gabor filters.
- Use maximum response at corresponding feature-map positions to fuse directional responses.
- Fixed Gabor filters are used; learnable Gabor filters are mentioned only as future work.

Implementation consequence:

- Do not implement learnable Gabor as the default.
- Do not use LBP, HOG, WLD, BSIF, or other handcrafted feature instead of Gabor.
- Do not reduce the number of scales or directions.

### A3. Conformer branch

Paper specifies:

- Input image size: **224 × 224 × 3**.
- Conformer is described as a parallel architecture based on **ViT and ResNet**.
- It contains:
  - backbone module
  - dual-branch module
  - Feature Coupling Unit (FCU)
  - classifier module
- Transformer encoder includes:
  - patch/input embedding
  - class token
  - positional encoding
  - Multi-Head Attention
  - FFN
  - LayerNorm
  - residual connections
- FCU bridges the ResNet/CNN branch and ViT/Transformer branch.

Implementation consequence:

- Do not replace Conformer with plain ResNet, plain CNN, plain ViT, or speech Conformer.
- Must expose `extract_features()` for penultimate/deep feature extraction after training.

### A4. Conformer training setup

Paper specifies:

- Framework: PyTorch.
- Input: 224 × 224 × 3.
- Batch size: 16.
- Optimizer: Adam.
- Initial learning rate: `1e-5`.
- LR scheduler: cosine annealing.
- Minimum LR: `5e-7`.

Implementation consequence:

- These values must be defaults in config.
- Deviations are allowed only through explicit config overrides and must be logged.

### A5. KCCA feature fusion

Paper specifies:

- Gabor feature vectors form one sample space.
- Conformer feature vectors form another sample space.
- A kernel function maps both spaces into high-dimensional feature spaces.
- CCA is applied in kernel space.
- Canonical correlated components are extracted.
- Fused Gabor-Conformer feature vector is produced.
- Kernels compared:
  - Laplacian
  - RBF
  - cosine
- Cosine kernel performs best in the reported experiments.

Implementation consequence:

- Implement KCCA, not PCA-only, KPCA-only, concatenation-only, or CCA-only.
- Support Laplacian, RBF, and cosine kernels.
- Default kernel must be cosine.

### A6. Knowledge graph

Paper specifies:

- Prior information such as gender, age, and left/right hand can be used.
- Graph structure shown in the paper uses:
  - first layer: gender nodes, male/female
  - second layer: left/right hand
  - third layer: palmprint feature templates / palmprint ID
- Multiple templates can correspond to a single palmprint ID in an ordered sequence.
- The graph partitions feature space and reduces candidate search.

Implementation consequence:

- Implement graph-backed candidate filtering.
- At minimum support:
  - gender
  - hand_side
  - palm_id/template nodes
- Support fallback when prior labels are unavailable.

### A7. Two-stage recognition

Paper specifies:

1. Build graph from database ROI images, ID labels, gender, left/right hand, and prior knowledge.
2. Input ROI image to be verified plus prior knowledge.
3. Extract Gabor-Conformer fused feature.
4. Filter by first-layer graph nodes.
5. Filter by second-layer graph nodes.
6. Compute cosine similarity with third-layer/template nodes and return ID.

Implementation consequence:

- Must implement both:
  - one-stage global search baseline
  - two-stage graph-filtered search
- Two-stage search must report candidate reduction and timing.

### A8. Matching

Paper specifies cosine similarity/cosine distance metric for final matching.

Implementation consequence:

- Default final matcher must be cosine.
- Euclidean distance may be supported only for experiments that reproduce feature-comparison tables where paper mentions Euclidean distance.

### A9. Dataset protocol

Paper uses:

- CASIA
- TJU
- XJTU
- IITD

Paper protocol:

- Remove defective data.
- Split remaining samples into training/testing sets with **1:1 ratio per category**.
- If a category has an odd number of images, randomly remove one image before split.
- Resize/prepare images for Conformer as 224 × 224 × 3.

Implementation consequence:

- Split must be per `palm_id`, not random globally.
- Split must be reproducible by seed.
- Dropped odd samples must be logged.

### A10. Metrics

Paper evaluates:

- Accuracy
- Precision
- Recall
- F1-score

Implementation consequence:

- All four metrics must be reported for every experiment.
- Confusion matrix and macro/weighted averages should be added for debugging, but not as substitutes.

---

## B. Underspecified details — implementation assumptions required

### B1. ROI extraction

Paper assumes palmprint ROI images but does not provide a concrete ROI extraction algorithm.

Default assumption:

```text
Use ROI images as input. Implement IdentityROIExtractor by default.
```

Do not invent ROI extraction as if it were from the paper.

### B2. Exact Gabor numerical parameters

Paper defines equations and states 7 scales/6 directions, but does not provide exact values for:

- sigma
- gamma
- lambda/wavelength schedule
- kmax
- spacing factor
- kernel size
- phase offset
- real/imag/complex magnitude selection

Default assumption:

```text
Use configurable defaults. Mark them as implementation assumptions.
```

### B3. Gabor scale/orientation fusion detail

Paper states 7 scales and 6 directions but describes "six sets of Gabor features" and max fusion across feature maps. It is unclear whether max is over:

- directions only
- scales only
- all scale-direction maps
- directions per scale, then concatenate scales

Default assumption:

```text
Compute responses for all 7 × 6 filters.
Take maximum across the 6 orientations per scale.
Concatenate 7 scale-wise max maps.
```

### B4. Conformer exact architecture

Paper does not specify:

- model depth
- number of heads
- embedding dimension
- patch size
- ResNet variant
- FCU placement
- dropout
- classifier head dimensions

Default assumption:

```text
Implement a configurable visual Conformer with CNN/ResNet branch, Transformer branch, and FCU.
Use paper-provided training hyperparameters as defaults.
```

### B5. KCCA exact math implementation details

Paper does not specify:

- regularization coefficient
- number of canonical components
- kernel centering details
- eigensolver strategy
- pre-KCCA dimensionality reduction
- exact fusion operation after canonical projection
- exact matrix transformation step

Default assumption:

```text
Use regularized, centered KCCA.
Default kernel = cosine.
Default fusion = U + V, L2-normalized.
Support concat/weighted_sum as ablations.
```

### B6. Knowledge graph traversal

Paper mentions ordered sequences and moving toward the most similar node until no further movement is possible, but does not define:

- edge construction
- neighborhood definition
- threshold value
- starting node
- graph-walk stopping rule

Default assumption:

```text
Faithful default: graph-filtered exhaustive cosine search within selected partition.
Optional experimental mode: kNN graph walk.
```

### B7. Threshold

Paper mentions a predefined threshold but does not provide value.

Default assumption:

```text
threshold = null; always return best match.
Optional: calibrate threshold on validation split.
```

### B8. Gender/age metadata availability

Paper’s graph can use gender, age, and hand side. Figure structure emphasizes gender and left/right hand. Public dataset folders may not always provide gender/age metadata.

Default assumption:

```text
Support gender and hand_side.
Treat missing values as "unknown".
Do not require age by default.
```

---

## C. Corrections to prior plan

The prior plan was directionally correct but must be tightened:

1. It mentioned "CNN + RNN" in places. The implementation must follow the **visual Conformer structure based on ViT + ResNet/CNN**, because the architecture section and figures specify ViT/Transformer and ResNet branches.
2. It proposed optional pooling/dimensionality reduction for Gabor. This is acceptable only as an **implementation assumption**, not paper-specified behavior.
3. It proposed open-source/timm Conformer fallback. This is acceptable only as **Option B**, not the primary implementation.
4. It proposed threshold calibration. This is acceptable only because paper omits threshold value.
5. It proposed graph-filtered exhaustive search. This is acceptable as the reproducible default because paper does not define exact graph-walk edges.

---

## D. Non-negotiable implementation rules

- Keep the paper pipeline intact.
- Make assumptions explicit in config and docs.
- Never silently replace one paper component with a simpler component.
- All experiments must save:
  - config
  - seed
  - dataset split
  - code commit hash if available
  - hardware
  - timing
  - metrics
