\# PALM\_CGK\_BASE — Experiment Summary



Updated after fair B1 reruns with `lr=1e-4`, `epochs=60`.



\---



\# 1. Protocols



\## 1.1 Tongji S1 -> S2



\* Train/Val/Gallery: Tongji session1

\* Probe/Test: Tongji session2

\* Matching: cosine similarity on 256-D embeddings

\* Main purpose: cross-session palmprint recognition / verification



\## 1.2 Tongji S2 -> S1



\* Train/Val/Gallery: Tongji session2

\* Probe/Test: Tongji session1

\* Matching: cosine similarity on 256-D embeddings

\* Main purpose: bidirectional cross-session robustness check



\## 1.3 IITD within split



\* Gallery/probe split within IITD

\* Easier, near-saturated within-dataset setting

\* Used as supporting evaluation, not the main claim basis



\---



\# 2. Tongji S1 -> S2 Results



\## B0: ResNet18 + CE



\* Rank-1: 5.47%

\* Rank-5: 14.27%

\* Macro-F1: 5.30%

\* EER: 24.93%

\* TAR@FAR=1e-2: 10.05%

\* TAR@FAR=1e-3: 1.77%



\## B1-old: ResNet18 + CE + SupCon, original run



Note: this was an earlier non-final run and should not be used as the main fair comparison against B2.



\* Rank-1: 58.85%

\* Rank-5: 69.17%

\* Macro-F1: 55.14%

\* EER: 6.55%

\* TAR@FAR=1e-2: 75.24%

\* TAR@FAR=1e-3: 46.04%



\## B1: ResNet18 + CE + SupCon, lr=1e-4



Config:



```text

configs/b1\_resnet18\_ce\_supcon\_tongji\_s1s2\_lr1e4.yaml

```



Experiment:



```text

experiments/b1\_resnet18\_ce\_supcon\_tongji\_s1s2\_lr1e4

```



Results:



\* Rank-1: 93.65%

\* Rank-5: 95.80%

\* Macro-F1: 92.71%

\* EER: 2.34%

\* TAR@FAR=1e-2: 96.26%

\* TAR@FAR=1e-3: 89.62%

\* Params: 11.46M

\* FLOPs: 1.819 GFLOPs

\* Average inference time: 2.03 ms/image



\## M1: LGFNetSmall Full, learnable Gabor, lr=1e-4



Config:



```text

configs/m1\_lgfnet\_full\_tongji\_s1s2\_lr1e4.yaml

```



Results:



\* Rank-1: 88.68%

\* Rank-5: 92.97%

\* Macro-F1: 87.49%

\* EER: 2.94%

\* TAR@FAR=1e-2: 94.18%

\* TAR@FAR=1e-3: 84.18%

\* Params: 17.73M

\* FLOPs: 3.788 GFLOPs

\* Average inference time: 7.35 ms/image



\## B3: CNN + DeiT, no Gabor, lr=1e-4



Config:



```text

configs/b3\_lgfnet\_no\_gabor\_tongji\_s1s2\_lr1e4.yaml

```



Results:



\* Rank-1: 89.78%

\* Rank-5: 92.97%

\* Macro-F1: 88.49%

\* EER: 2.60%

\* TAR@FAR=1e-2: 95.34%

\* TAR@FAR=1e-3: 86.83%

\* Params: 17.69M

\* FLOPs: 2.899 GFLOPs

\* Average inference time: 6.18 ms/image



\## B2: Fixed Gabor + ResNet18, lr=1e-4



Config:



```text

configs/b2\_fixed\_gabor\_resnet18\_tongji\_s1s2\_lr1e4.yaml

```



Experiment:



```text

experiments/b2\_fixed\_gabor\_resnet18\_tongji\_s1s2\_lr1e4

```



Results:



\* Rank-1: 93.62%

\* Rank-5: 95.68%

\* Macro-F1: 92.82%

\* EER: 2.13%

\* TAR@FAR=1e-2: 96.91%

\* TAR@FAR=1e-3: 91.89%

\* Params: 11.82M

\* FLOPs: 2.709 GFLOPs

\* Average inference time: 2.80 ms/image



\---



\# 3. Main Comparison on Tongji S1 -> S2



| Method                            |    Rank-1 |    Rank-5 |  Macro-F1 |      EER | TAR@FAR=1e-2 | TAR@FAR=1e-3 |     Params |      FLOPs |        Time |

| --------------------------------- | --------: | --------: | --------: | -------: | -----------: | -----------: | ---------: | ---------: | ----------: |

| ResNet18 + CE                     |      5.47 |     14.27 |      5.30 |    24.93 |        10.05 |         1.77 |          - |          - |           - |

| ResNet18 + CE + SupCon, old run   |     58.85 |     69.17 |     55.14 |     6.55 |        75.24 |        46.04 |          - |          - |           - |

| ResNet18 + CE + SupCon, lr=1e-4   | \*\*93.65\*\* | \*\*95.80\*\* |     92.71 |     2.34 |        96.26 |        89.62 | \*\*11.46M\*\* | \*\*1.819G\*\* | \*\*2.03 ms\*\* |

| LGFNetSmall full, learnable Gabor |     88.68 |     92.97 |     87.49 |     2.94 |        94.18 |        84.18 |     17.73M |     3.788G |     7.35 ms |

| CNN + DeiT, no Gabor              |     89.78 |     92.97 |     88.49 |     2.60 |        95.34 |        86.83 |     17.69M |     2.899G |     6.18 ms |

| Fixed Gabor + ResNet18            |     93.62 |     95.68 | \*\*92.82\*\* | \*\*2.13\*\* |    \*\*96.91\*\* |    \*\*91.89\*\* |     11.82M |     2.709G |     2.80 ms |



\## Observation for Tongji S1 -> S2



The fair B1 rerun changes the earlier conclusion.



\* B1 ResNet18 + CE + SupCon is extremely strong after using the same `lr=1e-4`, `epochs=60` recipe.

\* B1 slightly beats B2 on Rank-1, Rank-5, FLOPs, parameter count, and inference time.

\* B2 beats B1 on Macro-F1, EER, TAR@FAR=1e-2, and TAR@FAR=1e-3.

\* The most important B2 advantage is strict verification robustness: `TAR@FAR=1e-3` is 91.89% for B2 vs 89.62% for B1.

\* The original claim “learnable Gabor fusion improves recognition” is not supported because M1 is weaker than B1, B2, and B3.



\---



\# 4. Tongji S2 -> S1 Results



\## B1: ResNet18 + CE + SupCon, lr=1e-4



Config:



```text

configs/b1\_resnet18\_ce\_supcon\_tongji\_s2s1\_lr1e4.yaml

```



Experiment:



```text

experiments/b1\_resnet18\_ce\_supcon\_tongji\_s2s1\_lr1e4

```



Results:



\* Rank-1: 93.13%

\* Rank-5: 95.13%

\* Macro-F1: 92.15%

\* EER: 2.27%

\* TAR@FAR=1e-2: 96.19%

\* TAR@FAR=1e-3: 89.89%

\* Params: 11.46M

\* FLOPs: 1.819 GFLOPs

\* Average inference time: 1.59 ms/image



\## B2: Fixed Gabor + ResNet18, lr=1e-4



Config:



```text

configs/b2\_fixed\_gabor\_resnet18\_tongji\_s2s1\_lr1e4.yaml

```



Experiment:



```text

experiments/b2\_fixed\_gabor\_resnet18\_tongji\_s2s1\_lr1e4

```



Results:



\* Rank-1: 93.52%

\* Rank-5: 95.23%

\* Macro-F1: 92.51%

\* EER: 2.40%

\* TAR@FAR=1e-2: 96.46%

\* TAR@FAR=1e-3: 91.81%

\* Params: 11.82M

\* FLOPs: 2.709 GFLOPs

\* Average inference time: 3.14 ms/image



\---



\# 5. Main Comparison on Tongji S2 -> S1



| Method                          |    Rank-1 |    Rank-5 |  Macro-F1 |      EER | TAR@FAR=1e-2 | TAR@FAR=1e-3 |     Params |      FLOPs |        Time |

| ------------------------------- | --------: | --------: | --------: | -------: | -----------: | -----------: | ---------: | ---------: | ----------: |

| ResNet18 + CE + SupCon, lr=1e-4 |     93.13 |     95.13 |     92.15 | \*\*2.27\*\* |        96.19 |        89.89 | \*\*11.46M\*\* | \*\*1.819G\*\* | \*\*1.59 ms\*\* |

| Fixed Gabor + ResNet18          | \*\*93.52\*\* | \*\*95.23\*\* | \*\*92.51\*\* |     2.40 |    \*\*96.46\*\* |    \*\*91.81\*\* |     11.82M |     2.709G |     3.14 ms |



\## Observation for Tongji S2 -> S1



\* B2 beats B1 on Rank-1, Rank-5, Macro-F1, TAR@FAR=1e-2, and TAR@FAR=1e-3.

\* B1 beats B2 on EER, FLOPs, parameter count, and inference time.

\* Again, B2 shows a stronger strict-FAR verification result: `TAR@FAR=1e-3` is 91.81% for B2 vs 89.89% for B1.



\---



\# 6. Tongji Bidirectional Average



\## B1: ResNet18 + CE + SupCon, lr=1e-4



| Protocol | Rank-1 | Rank-5 | Macro-F1 |  EER | TAR@FAR=1e-2 | TAR@FAR=1e-3 |    Time |

| -------- | -----: | -----: | -------: | ---: | -----------: | -----------: | ------: |

| S1 -> S2 |  93.65 |  95.80 |    92.71 | 2.34 |        96.26 |        89.62 | 2.03 ms |

| S2 -> S1 |  93.13 |  95.13 |    92.15 | 2.27 |        96.19 |        89.89 | 1.59 ms |

| Average  |  93.39 |  95.47 |    92.43 | 2.31 |        96.23 |        89.75 | 1.81 ms |



\## B2: Fixed Gabor + ResNet18, lr=1e-4



| Protocol |    Rank-1 | Rank-5 |  Macro-F1 |      EER | TAR@FAR=1e-2 | TAR@FAR=1e-3 |    Time |

| -------- | --------: | -----: | --------: | -------: | -----------: | -----------: | ------: |

| S1 -> S2 |     93.62 |  95.68 |     92.82 |     2.13 |        96.91 |        91.89 | 2.80 ms |

| S2 -> S1 |     93.52 |  95.23 |     92.51 |     2.40 |        96.46 |        91.81 | 3.14 ms |

| Average  | \*\*93.57\*\* |  95.46 | \*\*92.67\*\* | \*\*2.27\*\* |    \*\*96.69\*\* |    \*\*91.85\*\* | 2.97 ms |



\## Direct Average Comparison: B1 vs B2



| Method                          |    Rank-1 |    Rank-5 |  Macro-F1 |      EER | TAR@FAR=1e-2 | TAR@FAR=1e-3 |     Params |      FLOPs |        Time |

| ------------------------------- | --------: | --------: | --------: | -------: | -----------: | -----------: | ---------: | ---------: | ----------: |

| ResNet18 + CE + SupCon, lr=1e-4 |     93.39 | \*\*95.47\*\* |     92.43 |     2.31 |        96.23 |        89.75 | \*\*11.46M\*\* | \*\*1.819G\*\* | \*\*1.81 ms\*\* |

| Fixed Gabor + ResNet18, lr=1e-4 | \*\*93.57\*\* |     95.46 | \*\*92.67\*\* | \*\*2.27\*\* |    \*\*96.69\*\* |    \*\*91.85\*\* |     11.82M |     2.709G |     2.97 ms |



\## Observation for Tongji Bidirectional Average



\* B2 has slightly better average Rank-1, Macro-F1, EER, TAR@FAR=1e-2, and TAR@FAR=1e-3.

\* B1 has slightly better average Rank-5 and clearly better efficiency.

\* The strongest evidence in favor of B2 is strict-FAR verification:



&#x20; \* B1 average TAR@FAR=1e-3: 89.75%

&#x20; \* B2 average TAR@FAR=1e-3: 91.85%

&#x20; \* Difference: +2.10 percentage points for B2

\* The strongest evidence in favor of B1 is efficiency:



&#x20; \* B1 FLOPs: 1.819G

&#x20; \* B2 FLOPs: 2.709G

&#x20; \* B1 average inference time: 1.81 ms/image

&#x20; \* B2 average inference time: 2.97 ms/image



\---



\# 7. IITD Within Split Results



\## B1: ResNet18 + CE + SupCon, lr=1e-4



Config:



```text

configs/b1\_resnet18\_ce\_supcon\_iitd\_within\_lr1e4.yaml

```



Results:



\* Rank-1: 99.13%

\* Rank-5: 99.57%

\* Macro-F1: 98.84%

\* EER: 0.36%

\* TAR@FAR=1e-2: 99.70%

\* TAR@FAR=1e-3: 99.41%

\* Params: 11.43M

\* FLOPs: 1.819 GFLOPs

\* Average inference time: 2.26 ms/image



\## B2: Fixed Gabor + ResNet18, lr=1e-4



Config:



```text

configs/b2\_fixed\_gabor\_resnet18\_iitd\_within\_lr1e4.yaml

```



Results:



\* Rank-1: 98.26%

\* Rank-5: 99.13%

\* Macro-F1: 97.68%

\* EER: 0.71%

\* TAR@FAR=1e-2: 99.29%

\* TAR@FAR=1e-3: 98.93%

\* Params: 11.78M

\* FLOPs: 2.709 GFLOPs

\* Average inference time: 2.86 ms/image



\## Main Comparison on IITD Within Split



| Method                 |    Rank-1 |    Rank-5 |  Macro-F1 |      EER | TAR@FAR=1e-2 | TAR@FAR=1e-3 |     Params |      FLOPs |        Time |

| ---------------------- | --------: | --------: | --------: | -------: | -----------: | -----------: | ---------: | ---------: | ----------: |

| ResNet18 + CE + SupCon | \*\*99.13\*\* | \*\*99.57\*\* | \*\*98.84\*\* | \*\*0.36\*\* |    \*\*99.70\*\* |    \*\*99.41\*\* | \*\*11.43M\*\* | \*\*1.819G\*\* | \*\*2.26 ms\*\* |

| Fixed Gabor + ResNet18 |     98.26 |     99.13 |     97.68 |     0.71 |        99.29 |        98.93 |     11.78M |     2.709G |     2.86 ms |



\## Observation for IITD



\* IITD within split is near-saturated.

\* B1 clearly beats B2 on IITD.

\* Therefore, fixed Gabor should not be claimed as universally superior.

\* IITD should be used as supporting evaluation, while the main claim should focus on Tongji cross-session behavior.



\---



\# 8. Resource Comparison



| Method                            | Params |  FLOPs |         Time | Notes                                            |

| --------------------------------- | -----: | -----: | -----------: | ------------------------------------------------ |

| ResNet18 + CE + SupCon            | 11.46M | 1.819G | 1.59-2.03 ms | Fastest strong baseline                          |

| Fixed Gabor + ResNet18            | 11.82M | 2.709G | 2.80-3.14 ms | Stronger strict-FAR cross-session verification   |

| CNN + DeiT, no Gabor              | 17.69M | 2.899G |      6.18 ms | Heavier, weaker than B1/B2                       |

| LGFNetSmall full, learnable Gabor | 17.73M | 3.788G |      7.35 ms | Heaviest and not competitive after fair B1 rerun |



\---



\# 9. Final Technical Conclusion



The final experimental conclusion is not the original learnable-Gabor fusion claim.



\## Supported conclusions



1\. Supervised contrastive metric learning is the dominant factor.



&#x20;  \* ResNet18 + CE alone performs very poorly on Tongji S1 -> S2.

&#x20;  \* ResNet18 + CE + SupCon with the correct `lr=1e-4` recipe reaches around 93% Rank-1 on both Tongji directions.



2\. Fixed Gabor + ResNet18 is useful mainly for strict cross-session verification.



&#x20;  \* B2 slightly improves bidirectional average Rank-1, Macro-F1, EER, TAR@FAR=1e-2, and especially TAR@FAR=1e-3 over B1.

&#x20;  \* The clearest advantage is average TAR@FAR=1e-3:



&#x20;    \* B1: 89.75%

&#x20;    \* B2: 91.85%



3\. Fixed Gabor is not universally superior.



&#x20;  \* B1 beats B2 on IITD within split.

&#x20;  \* B1 is faster and has lower FLOPs than B2.

&#x20;  \* Therefore, the claim must be framed around cross-session verification robustness, not universal recognition superiority.



4\. Learnable Gabor fusion is not supported by current results.



&#x20;  \* M1 learnable-Gabor full model is weaker than B1, B2, and B3 on Tongji S1 -> S2.

&#x20;  \* B3 without Gabor also beats M1.

&#x20;  \* Therefore, do not claim that the current learnable-Gabor branch improves palmprint recognition.



\---



\# 10. Recommended Paper Claim



\## Strongest defensible claim



A fixed Gabor texture prior combined with supervised contrastive metric learning improves strict-FAR cross-session palmprint verification robustness on Tongji, while maintaining a compact ResNet18-based architecture.



\## Safer wording



Fixed Gabor priors provide complementary texture bias for cross-session palmprint verification, improving strict-FAR operating points over a strong ResNet18 + supervised contrastive baseline on Tongji, but not universally outperforming the baseline across all datasets and efficiency metrics.



\## Claims to avoid



Do not claim:



\* Fixed Gabor is universally better than ResNet18 + SupCon.

\* Learnable Gabor fusion improves palmprint recognition.

\* B2 is always the best model across all datasets.

\* IITD proves general superiority of fixed Gabor.

\* The proposed model beats all baselines on every metric.



\---



\# 11. Recommended Paper Title Direction



Best current title:



```text

Fixed Gabor Priors for Robust Cross-Session Palmprint Verification

```



Alternative:



```text

Gabor-Guided Metric Learning for Cross-Session Palmprint Recognition

```



Alternative if emphasizing architecture:



```text

FG-ResNet: Fixed Gabor Prior with Supervised Contrastive Learning for Cross-Session Palmprint Recognition

```



\---



\# 12. Paper Table Candidates



\## Table 1: Tongji S1 -> S2 Ablation



| Method                 | Rank-1 | Rank-5 | Macro-F1 |   EER | TAR@1e-2 | TAR@1e-3 | Params |  FLOPs |    Time |

| ---------------------- | -----: | -----: | -------: | ----: | -------: | -------: | -----: | -----: | ------: |

| ResNet18 + CE          |   5.47 |  14.27 |     5.30 | 24.93 |    10.05 |     1.77 |      - |      - |       - |

| ResNet18 + CE + SupCon |  93.65 |  95.80 |    92.71 |  2.34 |    96.26 |    89.62 | 11.46M | 1.819G | 2.03 ms |

| LGFNetSmall full       |  88.68 |  92.97 |    87.49 |  2.94 |    94.18 |    84.18 | 17.73M | 3.788G | 7.35 ms |

| CNN + DeiT, no Gabor   |  89.78 |  92.97 |    88.49 |  2.60 |    95.34 |    86.83 | 17.69M | 2.899G | 6.18 ms |

| Fixed Gabor + ResNet18 |  93.62 |  95.68 |    92.82 |  2.13 |    96.91 |    91.89 | 11.82M | 2.709G | 2.80 ms |



\## Table 2: Tongji Bidirectional Comparison



| Method                 | Direction | Rank-1 | Rank-5 | Macro-F1 |  EER | TAR@1e-2 | TAR@1e-3 |    Time |

| ---------------------- | --------- | -----: | -----: | -------: | ---: | -------: | -------: | ------: |

| ResNet18 + CE + SupCon | S1 -> S2  |  93.65 |  95.80 |    92.71 | 2.34 |    96.26 |    89.62 | 2.03 ms |

| ResNet18 + CE + SupCon | S2 -> S1  |  93.13 |  95.13 |    92.15 | 2.27 |    96.19 |    89.89 | 1.59 ms |

| ResNet18 + CE + SupCon | Average   |  93.39 |  95.47 |    92.43 | 2.31 |    96.23 |    89.75 | 1.81 ms |

| Fixed Gabor + ResNet18 | S1 -> S2  |  93.62 |  95.68 |    92.82 | 2.13 |    96.91 |    91.89 | 2.80 ms |

| Fixed Gabor + ResNet18 | S2 -> S1  |  93.52 |  95.23 |    92.51 | 2.40 |    96.46 |    91.81 | 3.14 ms |

| Fixed Gabor + ResNet18 | Average   |  93.57 |  95.46 |    92.67 | 2.27 |    96.69 |    91.85 | 2.97 ms |



\## Table 3: IITD Within Split



| Method                 | Rank-1 | Rank-5 | Macro-F1 |  EER | TAR@1e-2 | TAR@1e-3 | Params |  FLOPs |    Time |

| ---------------------- | -----: | -----: | -------: | ---: | -------: | -------: | -----: | -----: | ------: |

| ResNet18 + CE + SupCon |  99.13 |  99.57 |    98.84 | 0.36 |    99.70 |    99.41 | 11.43M | 1.819G | 2.26 ms |

| Fixed Gabor + ResNet18 |  98.26 |  99.13 |    97.68 | 0.71 |    99.29 |    98.93 | 11.78M | 2.709G | 2.86 ms |



\---



\# 13. Next Recommended Experiments



Priority 1:



\* Confirm whether B2 advantage at strict FAR remains across another random seed.

\* Run B1 and B2 on Tongji with at least one additional seed if compute budget allows.



Priority 2:



\* Add confidence intervals or mean ± std over seeds.

\* This is important because the Rank-1 gap between B1 and B2 is small.



Priority 3:



\* If keeping the paper focused on Gabor, improve the analysis around strict-FAR verification and texture prior.

\* Do not center the paper around learnable Gabor fusion unless the learnable branch is redesigned and rerun successfully.



\---



\# 14. Current Paper Decision



Current best defensible paper direction:



```text

Fixed Gabor Priors for Robust Cross-Session Palmprint Verification

```



Main claim should be:



```text

A fixed Gabor prior improves strict-FAR cross-session verification robustness over a strong ResNet18 + supervised contrastive baseline on Tongji, although the baseline remains more efficient and performs better on the near-saturated IITD within split.

```



This is accurate, defensible, and consistent with all current logs.



