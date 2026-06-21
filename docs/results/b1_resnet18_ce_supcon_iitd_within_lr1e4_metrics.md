# Palmprint Recognition Evaluation Report

## Evaluation Summary
- **Model**: ResNet18Baseline
- **Gallery Size**: 1681
- **Probe Size**: 460
- **Split File**: `iitd_within.json`

## Model Resource Efficiency
- **Total Parameters**: 11,426,060 (11.43 M)
- **Trainable Parameters**: 11,426,060 (11.43 M)
- **Average Inference Time (per image)**: 2.26 ms (batch size 1 on CUDA)
- **Estimated FLOPs**: 1.819 GFLOPs (via fvcore)

## Key Performance Metrics
| Metric | Value | Percentage | Description |
|---|---|---|---|
| **Rank-1** | 0.991304 | 99.13% | Closed-set identification accuracy (top-1 match) |
| **Rank-5** | 0.995652 | 99.57% | Closed-set identification accuracy (within top-5) |
| **Macro-F1** | 0.988406 | 98.84% | Macro-averaged F1 score over all classes |
| **EER** | 0.003569 | 0.36% | Equal Error Rate for verification |
| **TAR@FAR=1e-2** | 0.997026 | 99.70% | True Acceptance Rate at False Acceptance Rate = 1% |
| **TAR@FAR=1e-3** | 0.994051 | 99.41% | True Acceptance Rate at False Acceptance Rate = 0.1% |

---
*Report generated automatically by `eval_embedding.py`.*
