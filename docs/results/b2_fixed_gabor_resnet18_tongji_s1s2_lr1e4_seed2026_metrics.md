# Palmprint Recognition Evaluation Report

## Evaluation Summary
- **Model**: FixedGaborResNet18
- **Gallery Size**: 6000
- **Probe Size**: 6000
- **Split File**: `tongji_s1_to_s2.json`

## Model Resource Efficiency
- **Total Parameters**: 11,820,216 (11.82 M)
- **Trainable Parameters**: 11,820,136 (11.82 M)
- **Average Inference Time (per image)**: 4.11 ms (batch size 1 on CUDA)
- **Estimated FLOPs**: 2.709 GFLOPs (via fvcore)

## Key Performance Metrics
| Metric | Value | Percentage | Description |
|---|---|---|---|
| **Rank-1** | 0.921833 | 92.18% | Closed-set identification accuracy (top-1 match) |
| **Rank-5** | 0.947500 | 94.75% | Closed-set identification accuracy (within top-5) |
| **Macro-F1** | 0.909757 | 90.98% | Macro-averaged F1 score over all classes |
| **EER** | 0.024033 | 2.40% | Equal Error Rate for verification |
| **TAR@FAR=1e-2** | 0.960483 | 96.05% | True Acceptance Rate at False Acceptance Rate = 1% |
| **TAR@FAR=1e-3** | 0.892683 | 89.27% | True Acceptance Rate at False Acceptance Rate = 0.1% |

---
*Report generated automatically by `eval_embedding.py`.*
