# Palmprint Recognition Evaluation Report

## Evaluation Summary
- **Model**: LGFNetSmall
- **Gallery Size**: 6000
- **Probe Size**: 6000
- **Split File**: `tongji_s1_to_s2.json`

## Model Resource Efficiency
- **Total Parameters**: 17,729,016 (17.73 M)
- **Trainable Parameters**: 17,729,016 (17.73 M)
- **Average Inference Time (per image)**: 7.35 ms (batch size 1 on CUDA)
- **Estimated FLOPs**: 3.788 GFLOPs (via fvcore)

## Key Performance Metrics
| Metric | Value | Percentage | Description |
|---|---|---|---|
| **Rank-1** | 0.886833 | 88.68% | Closed-set identification accuracy (top-1 match) |
| **Rank-5** | 0.929667 | 92.97% | Closed-set identification accuracy (within top-5) |
| **Macro-F1** | 0.874906 | 87.49% | Macro-averaged F1 score over all classes |
| **EER** | 0.029371 | 2.94% | Equal Error Rate for verification |
| **TAR@FAR=1e-2** | 0.941833 | 94.18% | True Acceptance Rate at False Acceptance Rate = 1% |
| **TAR@FAR=1e-3** | 0.841767 | 84.18% | True Acceptance Rate at False Acceptance Rate = 0.1% |

---
*Report generated automatically by `eval_embedding.py`.*
