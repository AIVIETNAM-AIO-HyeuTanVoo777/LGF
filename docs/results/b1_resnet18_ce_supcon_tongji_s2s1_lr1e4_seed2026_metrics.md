# Palmprint Recognition Evaluation Report

## Evaluation Summary
- **Model**: ResNet18Baseline
- **Gallery Size**: 6000
- **Probe Size**: 6000
- **Split File**: `tongji_s2_to_s1.json`

## Model Resource Efficiency
- **Total Parameters**: 11,462,040 (11.46 M)
- **Trainable Parameters**: 11,462,040 (11.46 M)
- **Average Inference Time (per image)**: 1.53 ms (batch size 1 on CUDA)
- **Estimated FLOPs**: 1.819 GFLOPs (via fvcore)

## Key Performance Metrics
| Metric | Value | Percentage | Description |
|---|---|---|---|
| **Rank-1** | 0.954333 | 95.43% | Closed-set identification accuracy (top-1 match) |
| **Rank-5** | 0.968833 | 96.88% | Closed-set identification accuracy (within top-5) |
| **Macro-F1** | 0.947643 | 94.76% | Macro-averaged F1 score over all classes |
| **EER** | 0.016100 | 1.61% | Equal Error Rate for verification |
| **TAR@FAR=1e-2** | 0.979267 | 97.93% | True Acceptance Rate at False Acceptance Rate = 1% |
| **TAR@FAR=1e-3** | 0.945850 | 94.58% | True Acceptance Rate at False Acceptance Rate = 0.1% |

---
*Report generated automatically by `eval_embedding.py`.*
