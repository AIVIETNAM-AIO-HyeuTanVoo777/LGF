# Palmprint Recognition Evaluation Report

## Evaluation Summary
- **Model**: FixedGaborResNet18
- **Gallery Size**: 1681
- **Probe Size**: 460
- **Split File**: `iitd_within.json`

## Model Resource Efficiency
- **Total Parameters**: 11,784,236 (11.78 M)
- **Trainable Parameters**: 11,784,156 (11.78 M)
- **Average Inference Time (per image)**: 2.86 ms (batch size 1 on CUDA)
- **Estimated FLOPs**: 2.709 GFLOPs (via fvcore)

## Key Performance Metrics
| Metric | Value | Percentage | Description |
|---|---|---|---|
| **Rank-1** | 0.982609 | 98.26% | Closed-set identification accuracy (top-1 match) |
| **Rank-5** | 0.991304 | 99.13% | Closed-set identification accuracy (within top-5) |
| **Macro-F1** | 0.976812 | 97.68% | Macro-averaged F1 score over all classes |
| **EER** | 0.007139 | 0.71% | Equal Error Rate for verification |
| **TAR@FAR=1e-2** | 0.992861 | 99.29% | True Acceptance Rate at False Acceptance Rate = 1% |
| **TAR@FAR=1e-3** | 0.989292 | 98.93% | True Acceptance Rate at False Acceptance Rate = 0.1% |

---
*Report generated automatically by `eval_embedding.py`.*
