# Palmprint Recognition Evaluation Report

## Evaluation Summary
- **Model**: LGFNetNoGabor
- **Gallery Size**: 6000
- **Probe Size**: 6000
- **Split File**: `tongji_s1_to_s2.json`

## Model Resource Efficiency
- **Total Parameters**: 17,690,328 (17.69 M)
- **Trainable Parameters**: 17,690,328 (17.69 M)
- **Average Inference Time (per image)**: 6.18 ms (batch size 1 on CUDA)
- **Estimated FLOPs**: 2.899 GFLOPs (via fvcore)

## Key Performance Metrics
| Metric | Value | Percentage | Description |
|---|---|---|---|
| **Rank-1** | 0.897833 | 89.78% | Closed-set identification accuracy (top-1 match) |
| **Rank-5** | 0.929667 | 92.97% | Closed-set identification accuracy (within top-5) |
| **Macro-F1** | 0.884942 | 88.49% | Macro-averaged F1 score over all classes |
| **EER** | 0.026000 | 2.60% | Equal Error Rate for verification |
| **TAR@FAR=1e-2** | 0.953367 | 95.34% | True Acceptance Rate at False Acceptance Rate = 1% |
| **TAR@FAR=1e-3** | 0.868300 | 86.83% | True Acceptance Rate at False Acceptance Rate = 0.1% |

---
*Report generated automatically by `eval_embedding.py`.*
