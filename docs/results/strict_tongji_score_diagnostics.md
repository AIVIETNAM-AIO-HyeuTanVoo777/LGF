# Strict Tongji Score Diagnostics

This table summarizes genuine/impostor cosine-score distributions for the strict Tongji palm-class-disjoint ablation runs. Values are aggregated over two session directions and three seeds unless a direction is specified.

## Overall summary

| Method | Direction | Genuine mean | Impostor mean | Impostor q0.999 | Genuine q0.001 | d-prime |
|---|---|---:|---:|---:|---:|---:|
| B0 ResNet18 + CE | ALL | 0.499218+/-0.009679 | 0.031390+/-0.005784 | 0.405444+/-0.016796 | 0.026418+/-0.032645 | 3.411386+/-0.144206 |
| B1 ResNet18 + CE + SupCon | ALL | 0.548214+/-0.014095 | 0.029694+/-0.003511 | 0.459162+/-0.049781 | 0.038909+/-0.027529 | 3.666429+/-0.123709 |
| B4 ResNet18 + ArcFace | ALL | 0.485175+/-0.004275 | 0.037654+/-0.006492 | 0.397037+/-0.016058 | 0.001651+/-0.016433 | 3.336682+/-0.086688 |
| B5 ResNet18 + BNNeck + CE | ALL | 0.498042+/-0.006120 | 0.020625+/-0.003111 | 0.402241+/-0.021684 | -0.001106+/-0.020209 | 3.481496+/-0.112779 |
| B6 ResNet18 + BNNeck + ArcFace | ALL | 0.481032+/-0.008767 | 0.026407+/-0.005444 | 0.396793+/-0.024949 | -0.004941+/-0.020623 | 3.323267+/-0.091907 |
| B7 ResNet18 + BNNeck + ArcFace + light SupCon | ALL | 0.486603+/-0.007490 | 0.027715+/-0.005477 | 0.395453+/-0.035908 | 0.008150+/-0.036505 | 3.385006+/-0.133792 |

## Interpretation

- `impostor_q0.999` approximates the high-impostor-score tail relevant to strict low-FAR behavior.
- Higher `d-prime` indicates stronger separation between genuine and impostor score distributions.
- These diagnostics should be interpreted together with TAR@FAR and EER, not as replacement metrics.
