# Palmprint Recognition Evaluation Report

## Evaluation Summary
- **Model**: ResNet18BNNeck
- **Embedding Mode**: post_bn
- **Gallery Size**: 6000
- **Probe Size**: 6000
- **Split File**: `tongji_s2_to_s1.json`

## Model Resource Efficiency
- **Total Parameters**: 11,462,552 (11.46 M)
- **Trainable Parameters**: 11,462,296 (11.46 M)
- **Average Inference Time (per image)**: 5.11 ms (batch size 1 on CUDA)
- **Estimated FLOPs**: 1.819 GFLOPs (via fvcore)

## Key Performance Metrics
| Metric | Value | Percentage | Description |
|---|---|---|---|
| **Rank-1** | 0.972333 | 97.23% | Closed-set identification accuracy (top-1 match) |
| **Rank-5** | 0.980000 | 98.00% | Closed-set identification accuracy (within top-5) |
| **Macro-F1** | 0.969000 | 96.90% | Macro-averaged F1 score over all classes |
| **EER** | 0.010582 | 1.06% | Equal Error Rate for verification |
| **TAR@FAR=1e-2** | 0.989117 | 98.91% | True Acceptance Rate at False Acceptance Rate = 1% |
| **TAR@FAR=1e-3** | 0.971200 | 97.12% | True Acceptance Rate at False Acceptance Rate = 0.1% |

---
*Report generated automatically by `eval_embedding.py`.*
