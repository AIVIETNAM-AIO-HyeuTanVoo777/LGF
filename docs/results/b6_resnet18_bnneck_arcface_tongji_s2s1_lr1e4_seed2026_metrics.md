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
- **Average Inference Time (per image)**: 5.32 ms (batch size 1 on CUDA)
- **Estimated FLOPs**: 1.819 GFLOPs (via fvcore)

## Key Performance Metrics
| Metric | Value | Percentage | Description |
|---|---|---|---|
| **Rank-1** | 0.946833 | 94.68% | Closed-set identification accuracy (top-1 match) |
| **Rank-5** | 0.962667 | 96.27% | Closed-set identification accuracy (within top-5) |
| **Macro-F1** | 0.939719 | 93.97% | Macro-averaged F1 score over all classes |
| **EER** | 0.017875 | 1.79% | Equal Error Rate for verification |
| **TAR@FAR=1e-2** | 0.975300 | 97.53% | True Acceptance Rate at False Acceptance Rate = 1% |
| **TAR@FAR=1e-3** | 0.933650 | 93.36% | True Acceptance Rate at False Acceptance Rate = 0.1% |

---
*Report generated automatically by `eval_embedding.py`.*
