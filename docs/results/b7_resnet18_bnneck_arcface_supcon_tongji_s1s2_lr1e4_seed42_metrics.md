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
- **Average Inference Time (per image)**: 5.03 ms (batch size 1 on CUDA)
- **Estimated FLOPs**: 1.819 GFLOPs (via fvcore)

## Key Performance Metrics
| Metric | Value | Percentage | Description |
|---|---|---|---|
| **Rank-1** | 0.967000 | 96.70% | Closed-set identification accuracy (top-1 match) |
| **Rank-5** | 0.979500 | 97.95% | Closed-set identification accuracy (within top-5) |
| **Macro-F1** | 0.963099 | 96.31% | Macro-averaged F1 score over all classes |
| **EER** | 0.012082 | 1.21% | Equal Error Rate for verification |
| **TAR@FAR=1e-2** | 0.986250 | 98.62% | True Acceptance Rate at False Acceptance Rate = 1% |
| **TAR@FAR=1e-3** | 0.958717 | 95.87% | True Acceptance Rate at False Acceptance Rate = 0.1% |

---
*Report generated automatically by `eval_embedding.py`.*
