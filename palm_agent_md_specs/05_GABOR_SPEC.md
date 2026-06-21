# Gabor Feature Extraction Specification

## 1. Paper requirements

The Gabor module must implement:

- 2D Gabor filters.
- Palmprint ROI as 2D grayscale image.
- 7 scales.
- 6 orientations:
  - 0°
  - 30°
  - 60°
  - 90°
  - 120°
  - 150°
- Convolution with palmprint ROI.
- Maximum response fusion at corresponding positions across feature maps.
- Fixed filters, not learnable filters.

## 2. Required class

```python
class GaborFeatureExtractor:
    def __init__(self, config: GaborConfig):
        ...

    def build_filter_bank(self) -> list[np.ndarray]:
        ...

    def extract_maps(self, gray_roi: np.ndarray) -> np.ndarray:
        ...

    def extract(self, gray_roi: np.ndarray) -> np.ndarray:
        ...
```

## 3. Config

```yaml
gabor:
  image_size: [224, 224]
  num_scales: 7
  orientations_deg: [0, 30, 60, 90, 120, 150]
  response_mode: magnitude
  orientation_fusion: max
  scale_fusion: concat

  # IMPLEMENTATION ASSUMPTIONS:
  kernel_size: 31
  sigma: 4.0
  gamma: 0.5
  phase_offset: 0.0
  kmax: 1.57079632679
  spacing_factor: 1.41421356237
  padding: same

  pooling:
    enabled: false
    type: adaptive_avg
    output_size: [28, 28]

  normalize:
    standardize: true
    l2: true
```

## 4. Filter bank construction

Must support the paper's complex Gabor form conceptually.

Implementation may use either:

1. Direct spatial Gabor equation with `lambda`, `theta`, `phi`, `sigma`, `gamma`.
2. Paper's `k_{u,v}` frequency-vector form.

The implementation must document which one is used.

Required bank shape:

```text
num_scales × num_orientations × kernel_height × kernel_width
= 7 × 6 × K × K
```

## 5. Response computation

```python
responses = []
for scale in range(7):
    scale_responses = []
    for theta in orientations:
        kernel = filter_bank[scale][theta]
        response = convolve(gray_roi, kernel)
        if response_mode == "magnitude":
            response = abs(response)
        scale_responses.append(response)

    fused_scale_map = max(scale_responses, axis=0)
    responses.append(fused_scale_map)

if scale_fusion == "concat":
    feature_maps = stack(responses)  # [7, H, W]
elif scale_fusion == "max":
    feature_maps = max(responses, axis=0)
```

Default faithful assumption:

```text
responses for 7 × 6 filters
→ max over 6 orientations per scale
→ concatenate 7 scale maps
```

## 6. Feature vector

Without pooling:

```text
dim = 7 × 224 × 224 = 351232
```

If memory is too high, pooling may be enabled only as implementation assumption:

```text
dim = 7 × 28 × 28 = 5488
```

## 7. Normalization

Implement:

```python
feature = feature.astype(np.float32)
feature = standard_scaler.transform(feature)  # fit on train only
feature = l2_normalize(feature)
```

## 8. Tests

Required tests:

- filter bank has 7 scales.
- filter bank has 6 orientations.
- orientations equal `[0, 30, 60, 90, 120, 150]`.
- output feature dimension is deterministic.
- no NaN/Inf.
- same input and config produce same feature.
