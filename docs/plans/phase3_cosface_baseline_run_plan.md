\# Phase 3 CosFace Baseline Run Plan



\## Purpose



Add one strong generic learned baseline outside the existing B0--B7 component matrix.



\## Baseline



B8 = ResNet18 + CosFace



\## Why CosFace



CosFace is already implemented in the repository margin-head loss module. It is the lowest-risk additional baseline because it reuses the existing margin-loss training path.



\## Scope



Dataset/protocol:



\- Tongji strict palm-class-disjoint cross-session protocol

\- directions: S1 -> S2 and S2 -> S1

\- seeds: 42, 2026, 2705



Configs:



\- `configs/b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s1s2\_seed42.yaml`

\- `configs/b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s1s2\_seed2026.yaml`

\- `configs/b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s1s2\_seed2705.yaml`

\- `configs/b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s2s1\_seed42.yaml`

\- `configs/b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s2s1\_seed2026.yaml`

\- `configs/b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s2s1\_seed2705.yaml`



\## Fixed recipe



\- model: `ResNet18Baseline`

\- embedding dimension: 256

\- pretrained: true

\- loss: CosFace

\- scale: 30.0

\- margin: 0.35

\- lambda\_supcon: 0.0

\- epochs: 60

\- lr: 0.0001

\- weight\_decay: 0.0001

\- grad\_accumulation\_steps: 4

\- AMP: true

\- sampler: 8 identities x 2 instances, fallback 4



\## Training commands



```bat

python scripts\\train\_lgf.py --config configs\\b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s1s2\_seed42.yaml

python scripts\\train\_lgf.py --config configs\\b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s1s2\_seed2026.yaml

python scripts\\train\_lgf.py --config configs\\b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s1s2\_seed2705.yaml

python scripts\\train\_lgf.py --config configs\\b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s2s1\_seed42.yaml

python scripts\\train\_lgf.py --config configs\\b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s2s1\_seed2026.yaml

python scripts\\train\_lgf.py --config configs\\b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s2s1\_seed2705.yaml

