# Palmprint Recognition Evaluation Report

## Evaluation Summary
- **Model**: ResNet18Baseline
- **Gallery Size**: 6000
- **Probe Size**: 6000
- **Split File**: `tongji_s1_to_s2.json`

## Model Resource Efficiency
- **Total Parameters**: 11,462,040 (11.46 M)
- **Trainable Parameters**: 11,462,040 (11.46 M)
- **Average Inference Time (per image)**: 2.02 ms (batch size 1 on CUDA)
- **Estimated FLOPs**: 1.819 GFLOPs (via fvcore)

## Key Performance Metrics
| Metric | Value | Percentage | Description |
|---|---|---|---|
| **Rank-1** | 0.947500 | 94.75% | Closed-set identification accuracy (top-1 match) |
| **Rank-5** | 0.964833 | 96.48% | Closed-set identification accuracy (within top-5) |
| **Macro-F1** | 0.941576 | 94.16% | Macro-averaged F1 score over all classes |
| **EER** | 0.019483 | 1.95% | Equal Error Rate for verification |
| **TAR@FAR=1e-2** | 0.971633 | 97.16% | True Acceptance Rate at False Acceptance Rate = 1% |
| **TAR@FAR=1e-3** | 0.925350 | 92.53% | True Acceptance Rate at False Acceptance Rate = 0.1% |

---
*Report generated automatically by `eval_embedding.py`.*
