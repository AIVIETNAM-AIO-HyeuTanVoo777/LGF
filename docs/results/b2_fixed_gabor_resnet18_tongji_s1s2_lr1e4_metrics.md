# Palmprint Recognition Evaluation Report

## Evaluation Summary
- **Model**: FixedGaborResNet18
- **Gallery Size**: 6000
- **Probe Size**: 6000
- **Split File**: `tongji_s1_to_s2.json`

## Model Resource Efficiency
- **Total Parameters**: 11,820,216 (11.82 M)
- **Trainable Parameters**: 11,820,136 (11.82 M)
- **Average Inference Time (per image)**: 2.80 ms (batch size 1 on CUDA)
- **Estimated FLOPs**: 2.709 GFLOPs (via fvcore)

## Key Performance Metrics
| Metric | Value | Percentage | Description |
|---|---|---|---|
| **Rank-1** | 0.936167 | 93.62% | Closed-set identification accuracy (top-1 match) |
| **Rank-5** | 0.956833 | 95.68% | Closed-set identification accuracy (within top-5) |
| **Macro-F1** | 0.928199 | 92.82% | Macro-averaged F1 score over all classes |
| **EER** | 0.021333 | 2.13% | Equal Error Rate for verification |
| **TAR@FAR=1e-2** | 0.969100 | 96.91% | True Acceptance Rate at False Acceptance Rate = 1% |
| **TAR@FAR=1e-3** | 0.918883 | 91.89% | True Acceptance Rate at False Acceptance Rate = 0.1% |

---
*Report generated automatically by `eval_embedding.py`.*
