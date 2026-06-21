# Palmprint Recognition Evaluation Report

## Evaluation Summary
- **Model**: ResNet18Baseline
- **Embedding Mode**: post_bn
- **Gallery Size**: 6000
- **Probe Size**: 6000
- **Split File**: `tongji_s1_to_s2.json`

## Model Resource Efficiency
- **Total Parameters**: 11,462,040 (11.46 M)
- **Trainable Parameters**: 11,462,040 (11.46 M)
- **Average Inference Time (per image)**: 2.32 ms (batch size 1 on CUDA)
- **Estimated FLOPs**: 1.819 GFLOPs (via fvcore)

## Key Performance Metrics
| Metric | Value | Percentage | Description |
|---|---|---|---|
| **Rank-1** | 0.924667 | 92.47% | Closed-set identification accuracy (top-1 match) |
| **Rank-5** | 0.952000 | 95.20% | Closed-set identification accuracy (within top-5) |
| **Macro-F1** | 0.915554 | 91.56% | Macro-averaged F1 score over all classes |
| **EER** | 0.026533 | 2.65% | Equal Error Rate for verification |
| **TAR@FAR=1e-2** | 0.953717 | 95.37% | True Acceptance Rate at False Acceptance Rate = 1% |
| **TAR@FAR=1e-3** | 0.882300 | 88.23% | True Acceptance Rate at False Acceptance Rate = 0.1% |

---
*Report generated automatically by `eval_embedding.py`.*
