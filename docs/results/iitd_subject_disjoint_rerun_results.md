# IITD Palm-Class-Disjoint Within-Session Rerun Results

IITD remains secondary within-session validation and is not cross-session evidence. TAR@FAR uses the conservative empirical-FAR rule.

| method   | method_label                |   Rank-1_mean |   Rank-1_std |   Rank-5_mean |   Rank-5_std |   Macro-F1_mean |   Macro-F1_std |   EER_mean |   EER_std |   TAR@FAR=1e-2_mean |   TAR@FAR=1e-2_std |   TAR@FAR=1e-3_mean |   TAR@FAR=1e-3_std |
|:---------|:----------------------------|--------------:|-------------:|--------------:|-------------:|----------------:|---------------:|-----------:|----------:|--------------------:|-------------------:|--------------------:|-------------------:|
| B1       | ResNet18 + CE + SupCon      |       97.8261 |     0.724638 |        98.913 |     0.362319 |         97.6984 |       0.805366 |    3.04892 |   1.1844  |              94.914 |            2.93391 |             86.1724 |            7.07351 |
| B6       | ResNet18 + BNNeck + ArcFace |       97.9469 |     1.71225  |        98.913 |     0.627554 |         97.8649 |       1.80062  |    3.24018 |   1.33906 |              94.431 |            2.58677 |             85.4546 |            3.85035 |

## B6 minus B1 deltas

|   seed |   delta_Rank-1_B6_minus_B1 |   delta_Rank-5_B6_minus_B1 |   delta_Macro-F1_B6_minus_B1 |   delta_EER_B6_minus_B1 |   delta_TAR@FAR=1e-2_B6_minus_B1 |   delta_TAR@FAR=1e-3_B6_minus_B1 |
|-------:|---------------------------:|---------------------------:|-----------------------------:|------------------------:|---------------------------------:|---------------------------------:|
|     42 |                   -1.08696 |                  -0.362319 |                    -1.07919  |                0.263182 |                         0.420168 |                          3.92157 |
|   2026 |                    1.44928 |                   0.362319 |                     1.58903  |                0.398406 |                        -1.59363  |                         -3.32005 |
|   2705 |                    0       |                   0        |                    -0.010352 |               -0.087791 |                        -0.275482 |                         -2.75482 |
