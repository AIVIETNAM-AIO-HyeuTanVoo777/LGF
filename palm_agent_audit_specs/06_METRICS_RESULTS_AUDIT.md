# Metrics and Results Audit

All percentages below are percentage values, not fractions. Example: `93.65` means `93.65%`.

## Required Tongji S1 -> S2 metrics

| Method | Rank-1 | Rank-5 | Macro-F1 | EER | TAR@FAR=1e-2 | TAR@FAR=1e-3 | Params | FLOPs | Time |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ResNet18 + CE | 5.47 | 14.27 | 5.30 | 24.93 | 10.05 | 1.77 | - | - | - |
| ResNet18 + CE + SupCon, old run | 58.85 | 69.17 | 55.14 | 6.55 | 75.24 | 46.04 | - | - | - |
| ResNet18 + CE + SupCon, lr=1e-4 | 93.65 | 95.80 | 92.71 | 2.34 | 96.26 | 89.62 | 11.46M | 1.819G | 2.03 ms |
| LGFNetSmall full, learnable Gabor | 88.68 | 92.97 | 87.49 | 2.94 | 94.18 | 84.18 | 17.73M | 3.788G | 7.35 ms |
| CNN + DeiT, no Gabor | 89.78 | 92.97 | 88.49 | 2.60 | 95.34 | 86.83 | 17.69M | 2.899G | 6.18 ms |
| Fixed Gabor + ResNet18 | 93.62 | 95.68 | 92.82 | 2.13 | 96.91 | 91.89 | 11.82M | 2.709G | 2.80 ms |

## Required Tongji S2 -> S1 metrics

| Method | Rank-1 | Rank-5 | Macro-F1 | EER | TAR@FAR=1e-2 | TAR@FAR=1e-3 | Params | FLOPs | Time |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ResNet18 + CE + SupCon, lr=1e-4 | 93.13 | 95.13 | 92.15 | 2.27 | 96.19 | 89.89 | 11.46M | 1.819G | 1.59 ms |
| Fixed Gabor + ResNet18 | 93.52 | 95.23 | 92.51 | 2.40 | 96.46 | 91.81 | 11.82M | 2.709G | 3.14 ms |

## Required Tongji bidirectional averages

### B1 ResNet18 + CE + SupCon, lr=1e-4

| Metric | Expected average |
|---|---:|
| Rank-1 | 93.39 |
| Rank-5 | 95.47 |
| Macro-F1 | 92.43 |
| EER | 2.31 |
| TAR@FAR=1e-2 | 96.23 |
| TAR@FAR=1e-3 | 89.75 |
| Time | 1.81 ms |

### B2 Fixed Gabor + ResNet18

| Metric | Expected average |
|---|---:|
| Rank-1 | 93.57 |
| Rank-5 | 95.46 |
| Macro-F1 | 92.67 |
| EER | 2.27 |
| TAR@FAR=1e-2 | 96.69 |
| TAR@FAR=1e-3 | 91.85 |
| Time | 2.97 ms |

## Required IITD within metrics

| Method | Rank-1 | Rank-5 | Macro-F1 | EER | TAR@FAR=1e-2 | TAR@FAR=1e-3 | Params | FLOPs | Time |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ResNet18 + CE + SupCon | 99.13 | 99.57 | 98.84 | 0.36 | 99.70 | 99.41 | 11.43M | 1.819G | 2.26 ms |
| Fixed Gabor + ResNet18 | 98.26 | 99.13 | 97.68 | 0.71 | 99.29 | 98.93 | 11.78M | 2.709G | 2.86 ms |

## Metric consistency rules

The AGENT must verify:

1. `metrics.json`, `metrics.md`, and `tongji_s1s2_summary.md` agree for each experiment.
2. Fraction-to-percent conversions are correct:
   - `0.936500` -> `93.65%`
   - `0.023400` -> `2.34%`
3. No table uses old B1 `58.85%` as the main fair B1 comparison.
4. Summary clearly labels old B1 as `old run` or non-final.
5. B2 is not marked best on every metric if B1 is faster and slightly better on some Rank metrics.
6. M1 is not claimed to beat B1 after fair B1 rerun.
7. B3 is correctly described as beating M1 on Tongji S1->S2.
8. IITD is described as near-saturated and not the main evidence for fixed Gabor superiority.

## Tolerance

For saved text/JSON consistency:

```text
±0.01 percentage points for percentage metrics
```

For rerun eval consistency:

```text
±0.05 percentage points for Rank/F1/EER/TAR
```

For inference time:

```text
informational only unless off by >50% with same hardware and batch settings
```
