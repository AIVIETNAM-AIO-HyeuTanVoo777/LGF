\# Training and Preprocessing Recipe Audit



\## Purpose



This audit records the exact training and evaluation recipe used for the strict Tongji B1 and B6 comparison after conservative TAR@FAR recomputation.



The purpose is reproducibility and claim control. This audit does not introduce new experimental results.



\## Scope



This file covers the seed-42 strict Tongji B1/B6 recipe for both session directions:



\* `configs/b1\_resnet18\_ce\_supcon\_tongji\_subject\_disjoint\_s1s2\_seed42.yaml`

\* `configs/b1\_resnet18\_ce\_supcon\_tongji\_subject\_disjoint\_s2s1\_seed42.yaml`

\* `configs/b6\_resnet18\_bnneck\_arcface\_tongji\_subject\_disjoint\_s1s2\_seed42.yaml`

\* `configs/b6\_resnet18\_bnneck\_arcface\_tongji\_subject\_disjoint\_s2s1\_seed42.yaml`



The same fields are also summarized by `scripts/audit\_training\_config\_table.py` for the final strict Tongji component-ablation runs.



\## Protocol files



| Method | Direction | Split file                                                 | Save directory                                                               |

| ------ | --------- | ---------------------------------------------------------- | ---------------------------------------------------------------------------- |

| B1     | S1 -> S2  | `data/splits/tongji\_subject\_disjoint\_s1\_to\_s2\_seed42.json` | `experiments/b1\_resnet18\_ce\_supcon\_tongji\_subject\_disjoint\_s1s2\_seed42`      |

| B1     | S2 -> S1  | `data/splits/tongji\_subject\_disjoint\_s2\_to\_s1\_seed42.json` | `experiments/b1\_resnet18\_ce\_supcon\_tongji\_subject\_disjoint\_s2s1\_seed42`      |

| B6     | S1 -> S2  | `data/splits/tongji\_subject\_disjoint\_s1\_to\_s2\_seed42.json` | `experiments/b6\_resnet18\_bnneck\_arcface\_tongji\_subject\_disjoint\_s1s2\_seed42` |

| B6     | S2 -> S1  | `data/splits/tongji\_subject\_disjoint\_s2\_to\_s1\_seed42.json` | `experiments/b6\_resnet18\_bnneck\_arcface\_tongji\_subject\_disjoint\_s2s1\_seed42` |



\## Shared training settings



| Field                       |    Value |

| --------------------------- | -------: |

| seed                        |       42 |

| device                      |   `cuda` |

| dataset                     | `Tongji` |

| sampler.num\_identities      |        8 |

| sampler.num\_instances       |        2 |

| sampler.fallback\_identities |        4 |

| loader.num\_workers          |        0 |

| embedding\_dim               |      256 |

| pretrained                  |   `true` |

| epochs                      |       60 |

| learning rate               |   0.0001 |

| weight decay                |   0.0001 |

| gradient accumulation steps |        4 |

| temperature                 |     0.07 |

| AMP                         |   `true` |



The effective configured sampler batch composition is therefore 8 identities × 2 instances = 16 samples before gradient accumulation.



\## B1 recipe



| Field                  | Value                                                                |

| ---------------------- | -------------------------------------------------------------------- |

| model.name             | `ResNet18Baseline`                                                   |

| loss family            | CE + SupCon                                                          |

| training.lambda\_supcon | 0.1                                                                  |

| training.temperature   | 0.07                                                                 |

| evaluation embedding   | default model embedding; no explicit BNNeck/post-BN evaluation field |



B1 is the learned CE+SupCon baseline.



\## B6 recipe



| Field                  | Value            |

| ---------------------- | ---------------- |

| model.name             | `ResNet18BNNeck` |

| model.eval\_embedding   | `post\_bn`        |

| eval.embedding         | `post\_bn`        |

| loss.name              | `arcface`        |

| loss.scale             | 30.0             |

| loss.margin            | 0.5              |

| training.loss\_type     | `arcface`        |

| training.lambda\_supcon | 0.0              |

| training.temperature   | 0.07             |



B6 is the pre-specified BNNeck+ArcFace variant. Its ArcFace setting is fixed at scale 30.0 and margin 0.5.



\## Optimizer and scheduler evidence boundary



The exact B1/B6 strict Tongji YAML files audited here do not contain an explicit optimizer or scheduler field.



Repository-level default configuration contains optimizer and scheduler fields, but this audit does not infer that those defaults were necessarily active for these specific strict Tongji YAML files unless confirmed by the training entrypoint or run metadata.



Therefore, paper-facing reproducibility wording should state the exact confirmed YAML fields above and should not claim a specific scheduler for B1/B6 unless separately verified.



\## Checkpoint selection



The training/evaluation workflow uses `checkpoints/best.pt`.



The checkpoint-selection audit and training script evidence indicate that `best.pt` is selected using validation Rank-1 when validation Rank-1 is computable, otherwise validation loss.



This rule is validation-only and must not be described as using gallery/probe/test information.



\## Preprocessing evidence boundary



Repository default preprocessing configuration includes:



\* resize: `\[224, 224]`

\* `gabor\_grayscale: true`

\* `conformer\_rgb: true`

\* ImageNet-style conformer normalization mean `\[0.485, 0.456, 0.406]`

\* ImageNet-style conformer normalization std `\[0.229, 0.224, 0.225]`



The exact B1/B6 strict Tongji YAML files audited here do not repeat those preprocessing fields. Paper-facing text may cite them only as repository default preprocessing unless the training dataset implementation confirms they are applied to these runs.



\## Claim boundary



This audit supports the following wording:



> B1 and B6 were trained under the same strict Tongji palm-class-disjoint split construction, seed, sampler, epoch count, learning rate, weight decay, gradient accumulation, AMP setting, embedding dimension, and ImageNet-pretrained ResNet18 backbone family. B6 differs by adding BNNeck/post-BN evaluation and a fixed ArcFace head with scale 30.0 and margin 0.5, while B1 uses CE+SupCon with lambda 0.1.



This audit does not support the following wording:



\* A full ArcFace margin/scale sensitivity sweep was performed.

\* B6 is superior to B1 under the strict Tongji protocol.

\* Scheduler details are known from the four audited B1/B6 YAML files.

\* Gallery/probe/test data were used for checkpoint selection.

\* The protocol is truly subject-disjoint unless a true subject-id field is available.



\## Status



PASS.



