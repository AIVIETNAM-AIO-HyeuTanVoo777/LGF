# Palmprint Recognition Evaluation Report

## Evaluation Summary
- **Model**: ResNet18Baseline
- **Embedding Mode**: post_bn
- **Gallery Size**: 6000
- **Probe Size**: 6000
- **Split File**: `tongji_s2_to_s1.json`

## Model Resource Efficiency
- **Total Parameters**: 11,462,040 (11.46 M)
- **Trainable Parameters**: 11,462,040 (11.46 M)
- **Average Inference Time (per image)**: 4.83 ms (batch size 1 on CUDA)
- **Estimated FLOPs**: 1.819 GFLOPs (via fvcore)

## Key Performance Metrics
| Metric | Value | Percentage | Description |
|---|---|---|---|
| **Rank-1** | 0.962333 | 96.23% | Closed-set identification accuracy (top-1 match) |
| **Rank-5** | 0.976000 | 97.60% | Closed-set identification accuracy (within top-5) |
| **Macro-F1** | 0.957397 | 95.74% | Macro-averaged F1 score over all classes |
| **EER** | 0.013983 | 1.40% | Equal Error Rate for verification |
| **TAR@FAR=1e-2** | 0.982900 | 98.29% | True Acceptance Rate at False Acceptance Rate = 1% |
| **TAR@FAR=1e-3** | 0.954933 | 95.49% | True Acceptance Rate at False Acceptance Rate = 0.1% |

---
*Report generated automatically by `eval_embedding.py`.*
