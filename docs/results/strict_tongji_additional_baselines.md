# Strict Tongji Additional Baselines

This table adds B8, a generic learned CosFace baseline, outside the B0--B7 component matrix.

B8 is not palmprint-specific. It is included as a stronger generic metric-learning baseline using the existing margin-head training path.

## Summary

| Method | Palmprint-specific? | Learned? | Direction | n | Rank-1 | EER | TAR@FAR=1e-3 | Comment |
|---|---:|---:|---|---:|---:|---:|---:|---|
| ResNet18 + CosFace | No | Yes | S1->S2 | 3 | 92.361 +/- 1.754 | 5.150 +/- 0.213 | 71.703 +/- 0.959 | Generic learned margin-loss baseline; not palmprint-specific. |
| ResNet18 + CosFace | No | Yes | S2->S1 | 3 | 92.889 +/- 1.143 | 4.844 +/- 0.350 | 74.619 +/- 1.524 | Generic learned margin-loss baseline; not palmprint-specific. |
| ResNet18 + CosFace | No | Yes | Both | 6 | 92.625 +/- 1.504 | 4.997 +/- 0.328 | 73.161 +/- 1.936 | Generic learned margin-loss baseline; not palmprint-specific. |

## Detail

| Direction | Seed | Rank-1 | Rank-5 | Macro-F1 | EER | TAR@FAR=1e-2 | TAR@FAR=1e-3 |
|---|---:|---:|---:|---:|---:|---:|---:|
| S1->S2 | 42 | 92.000 | 96.833 | 91.069 | 5.027 | 86.858 | 70.350 |
| S1->S2 | 2026 | 94.667 | 97.333 | 94.143 | 4.973 | 87.933 | 72.300 |
| S1->S2 | 2705 | 90.417 | 94.083 | 88.972 | 5.450 | 86.575 | 72.458 |
| S2->S1 | 42 | 94.417 | 97.500 | 93.862 | 4.350 | 90.092 | 76.483 |
| S2->S1 | 2026 | 92.583 | 95.667 | 91.434 | 5.075 | 88.425 | 74.625 |
| S2->S1 | 2705 | 91.667 | 95.250 | 90.429 | 5.108 | 87.025 | 72.750 |

## Claim boundary

- Safe: B8 is an additional generic learned CosFace baseline under the same strict Tongji protocol.
- Unsafe: B8 is a palmprint-specific baseline, PalmNet/CompNet/Competitive-Code replacement, or state-of-the-art method.
