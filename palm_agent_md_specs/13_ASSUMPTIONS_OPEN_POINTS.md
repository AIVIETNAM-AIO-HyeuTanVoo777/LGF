# Implementation Assumptions and Open Points

This file lists every point where the paper is insufficiently detailed for exact code reproduction.

## 1. ROI extraction

Paper status:

```text
Underspecified.
```

Default:

```text
Use ROI images as input.
IdentityROIExtractor.
```

Risk:

```text
If raw datasets contain non-ROI palm images, results may not match paper.
```

## 2. Gabor hyperparameters

Paper status:

```text
Specifies equations, 7 scales, 6 directions.
Does not specify exact sigma, gamma, lambda schedule, kmax, spacing factor, kernel size, phase.
```

Default:

```yaml
kernel_size: 31
sigma: 4.0
gamma: 0.5
phase_offset: 0.0
kmax: 1.57079632679
spacing_factor: 1.41421356237
```

Risk:

```text
Recognition numbers may differ from paper.
```

## 3. Gabor fusion across scales/directions

Paper status:

```text
Says 7 scales and 6 directions, then describes max fusion across feature maps.
Exact dimension/fusion order is unclear.
```

Default:

```text
max over orientations per scale, concatenate scale maps.
```

Alternative:

```text
max over all scale-orientation responses.
```

## 4. Gabor feature dimension reduction

Paper status:

```text
Does not specify pooling/PCA before KCCA.
```

Default:

```text
No pooling for strict mode.
Optional pooling/PCA for memory mode.
```

## 5. Conformer exact architecture

Paper status:

```text
Describes ViT+ResNet structure and FCU but omits exact architecture parameters.
```

Default:

```yaml
embed_dim: 384
depth: 12
num_heads: 6
patch_size: 16
feature_dim: 512
fcu_stages: [3, 6, 9, 12]
```

Risk:

```text
Architecture may differ from authors' implementation.
```

## 6. KCCA regularization/components

Paper status:

```text
Does not specify regularization, component count, eigensolver, kernel centering.
```

Default:

```yaml
n_components: 256
reg: 1.0e-3
center_kernels: true
```

## 7. KCCA fusion operation

Paper status:

```text
Says components are fused into a new feature matrix and transformed, but not exact operation.
```

Default:

```text
Z = U + V, then L2 normalize.
```

Alternatives:

```text
concat(U, V)
weighted_sum
```

## 8. Knowledge graph threshold

Paper status:

```text
Mentions predefined threshold but does not give value.
```

Default:

```text
threshold = null, always return best match.
```

Optional:

```text
Calibrate threshold on validation data.
```

## 9. Knowledge graph-walk details

Paper status:

```text
Mentions moving toward most similar feature until no further movement is possible.
Does not define edges/neighborhood/start node.
```

Default:

```text
Exhaustive cosine search within graph-filtered partition.
```

Optional:

```text
kNN graph walk.
```

## 10. Age prior

Paper status:

```text
Mentions gender, age, left/right hand, but figure and core structure focus on gender and hand side.
```

Default:

```text
Implement gender and hand_side only.
Support age as optional metadata field but not required.
```

## 11. Gender metadata

Paper status:

```text
CASIA includes gender counts in paper. Public file structures may not expose gender directly.
```

Default:

```text
Allow user-provided gender CSV.
Use unknown if unavailable.
```

## 12. Distance metric inconsistency

Paper status:

```text
Final recognition uses cosine similarity.
Some comparison experiments mention Euclidean distance.
```

Default:

```text
Main pipeline uses cosine.
Feature comparison experiment supports Euclidean through config.
```

## 13. Exact defective-data removal

Paper status:

```text
Says defective data is removed but does not define defect criteria.
```

Default:

```text
Use metadata is_valid flag if provided.
Otherwise treat all images as valid.
Allow manual exclusion file.
```

## 14. Baselines

Paper status:

```text
Compares many methods but does not provide implementation details for all.
```

Default:

```text
Do not claim reproduced baselines unless implemented.
Paper-reported numbers must be labeled as paper_reported_not_reproduced.
```
