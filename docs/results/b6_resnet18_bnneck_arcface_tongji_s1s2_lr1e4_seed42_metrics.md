# Palmprint Recognition Evaluation Report

## Evaluation Summary
- **Model**: ResNet18BNNeck
- **Embedding Mode**: post_bn
- **Gallery Size**: 6000
- **Probe Size**: 6000
- **Split File**: `tongji_s1_to_s2.json`

## Model Resource Efficiency
- **Total Parameters**: 11,462,552 (11.46 M)
- **Trainable Parameters**: 11,462,296 (11.46 M)
- **Average Inference Time (per image)**: 5.48 ms (batch size 1 on CUDA)
- **Estimated FLOPs**: 1.819 GFLOPs (via fvcore)

## Key Performance Metrics
| Metric | Value | Percentage | Description |
|---|---|---|---|
| **Rank-1** | 0.967833 | 96.78% | Closed-set identification accuracy (top-1 match) |
| **Rank-5** | 0.978667 | 97.87% | Closed-set identification accuracy (within top-5) |
| **Macro-F1** | 0.964478 | 96.45% | Macro-averaged F1 score over all classes |
| **EER** | 0.010933 | 1.09% | Equal Error Rate for verification |
| **TAR@FAR=1e-2** | 0.988583 | 98.86% | True Acceptance Rate at False Acceptance Rate = 1% |
| **TAR@FAR=1e-3** | 0.965583 | 96.56% | True Acceptance Rate at False Acceptance Rate = 0.1% |

---
*Report generated automatically by `eval_embedding.py`.*
