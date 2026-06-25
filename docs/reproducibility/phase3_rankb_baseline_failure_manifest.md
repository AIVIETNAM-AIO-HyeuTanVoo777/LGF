\# Phase 3 Rank-B Baseline and Failure Analysis Manifest



\## Purpose



This manifest records the Phase 3 Rank-B revision additions:



1\. an additional generic CosFace baseline,

2\. strict Tongji failure-case analysis,

3\. protocol-safety checklist,

4\. reproducibility commands and claim boundaries.



This manifest is intended to make the Phase 3 evidence reproducible from versioned scripts plus local non-versioned experiment artifacts.



\## Branch



Branch:



```text

phase3-rankb-baselines-failure-analysis

```



Phase 3 commits:



```text

cddaccf Add Rank-B strict protocol checklist

286da6d Add strict Tongji failure case analysis

a1de164 Add CosFace baseline audit

c203d16 Aggregate CosFace baseline results

bdbe298 Add CosFace baseline config plan

```



Base Phase 2 commit:



```text

16b4878 Add phase 2 conservative evaluation manifest

```



\## Environment



Conda environment:



```text

palm\_lgf

```



Windows command prompt setup:



```bat

conda activate palm\_lgf

cd D:\\0.Research\\PALM\_CGK\_BASE\\PALM\_CGK\_BASE

set PYTHONPATH=%CD%

```



\## Added baseline



Baseline:



```text

B8 = ResNet18 + CosFace

```



Definition:



\* model: ResNet18Baseline

\* embedding dimension: 256

\* pretrained: true

\* loss: CosFace

\* scale: 30.0

\* margin: 0.35

\* lambda\_supcon: 0.0

\* epochs: 60

\* learning rate: 0.0001

\* weight decay: 0.0001

\* gradient accumulation steps: 4

\* AMP: true

\* sampler: 8 identities x 2 instances, fallback 4



Protocol:



\* Tongji strict palm-class-disjoint cross-session protocol

\* directions:



&#x20; \* S1 -> S2

&#x20; \* S2 -> S1

\* seeds:



&#x20; \* 42

&#x20; \* 2026

&#x20; \* 2705



\## Added configs



B8 configs:



```text

configs/b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s1s2\_seed42.yaml

configs/b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s1s2\_seed2026.yaml

configs/b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s1s2\_seed2705.yaml

configs/b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s2s1\_seed42.yaml

configs/b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s2s1\_seed2026.yaml

configs/b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s2s1\_seed2705.yaml

```



Config generator:



```text

scripts/generate\_cosface\_baseline\_configs.py

```



Run plan:



```text

docs/plans/phase3\_cosface\_baseline\_run\_plan.md

```



\## B8 training commands



Each B8 run is trained from a fixed YAML config.



Template:



```bat

set PYTHONPATH=%CD%

python scripts\\train\_lgf.py --config <CONFIG>

python scripts\\eval\_embedding.py --checkpoint <EXPERIMENT>\\checkpoints\\best.pt --config <CONFIG>

```



Concrete configs:



```bat

python scripts\\train\_lgf.py --config configs\\b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s1s2\_seed42.yaml

python scripts\\eval\_embedding.py --checkpoint experiments\\b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s1s2\_seed42\\checkpoints\\best.pt --config configs\\b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s1s2\_seed42.yaml



python scripts\\train\_lgf.py --config configs\\b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s2s1\_seed42.yaml

python scripts\\eval\_embedding.py --checkpoint experiments\\b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s2s1\_seed42\\checkpoints\\best.pt --config configs\\b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s2s1\_seed42.yaml



python scripts\\train\_lgf.py --config configs\\b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s1s2\_seed2026.yaml

python scripts\\eval\_embedding.py --checkpoint experiments\\b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s1s2\_seed2026\\checkpoints\\best.pt --config configs\\b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s1s2\_seed2026.yaml



python scripts\\train\_lgf.py --config configs\\b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s2s1\_seed2026.yaml

python scripts\\eval\_embedding.py --checkpoint experiments\\b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s2s1\_seed2026\\checkpoints\\best.pt --config configs\\b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s2s1\_seed2026.yaml



python scripts\\train\_lgf.py --config configs\\b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s1s2\_seed2705.yaml

python scripts\\eval\_embedding.py --checkpoint experiments\\b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s1s2\_seed2705\\checkpoints\\best.pt --config configs\\b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s1s2\_seed2705.yaml



python scripts\\train\_lgf.py --config configs\\b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s2s1\_seed2705.yaml

python scripts\\eval\_embedding.py --checkpoint experiments\\b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s2s1\_seed2705\\checkpoints\\best.pt --config configs\\b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s2s1\_seed2705.yaml

```



\## B8 local artifacts



Required local non-versioned artifacts:



```text

experiments/b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s1s2\_seed42/metrics.json

experiments/b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s1s2\_seed42/scores.csv

experiments/b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s2s1\_seed42/metrics.json

experiments/b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s2s1\_seed42/scores.csv

experiments/b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s1s2\_seed2026/metrics.json

experiments/b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s1s2\_seed2026/scores.csv

experiments/b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s2s1\_seed2026/metrics.json

experiments/b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s2s1\_seed2026/scores.csv

experiments/b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s1s2\_seed2705/metrics.json

experiments/b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s1s2\_seed2705/scores.csv

experiments/b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s2s1\_seed2705/metrics.json

experiments/b8\_resnet18\_cosface\_tongji\_subject\_disjoint\_s2s1\_seed2705/scores.csv

```



Check command:



```bat

dir experiments /s /b | findstr /i "b8\_resnet18\_cosface\_tongji\_subject\_disjoint" | findstr /i "metrics.json scores.csv"

```



Expected:



```text

6 metrics.json files

6 scores.csv files

```



\## B8 exported results



Aggregation script:



```bat

python scripts\\aggregate\_cosface\_baseline\_results.py

```



Versioned outputs:



```text

docs/results/strict\_tongji\_b8\_cosface\_detail.csv

docs/results/strict\_tongji\_additional\_baselines.csv

docs/results/strict\_tongji\_additional\_baselines.md

docs/audits/cosface\_baseline\_audit.md

```



B8 summary:



```text

Direction S1 -> S2:

Rank-1 = 92.361 +/- 1.754

EER = 5.150 +/- 0.213

TAR@FAR=1e-3 = 71.703 +/- 0.959



Direction S2 -> S1:

Rank-1 = 92.889 +/- 1.143

EER = 4.844 +/- 0.350

TAR@FAR=1e-3 = 74.619 +/- 1.524



Both:

Rank-1 = 92.625 +/- 1.504

EER = 4.997 +/- 0.328

TAR@FAR=1e-3 = 73.161 +/- 1.936

```



\## Failure-case analysis



Failure-case export script:



```text

scripts/export\_strict\_tongji\_failure\_cases.py

```



Run command:



```bat

set PYTHONPATH=%CD%

python scripts\\export\_strict\_tongji\_failure\_cases.py

```



Versioned outputs:



```text

docs/results/strict\_tongji\_failure\_cases.csv

docs/results/strict\_tongji\_failure\_case\_summary.csv

docs/results/strict\_tongji\_failure\_case\_summary.md

docs/audits/failure\_case\_analysis\_audit.md

```



Scope:



```text

4 methods x 2 directions x 3 seeds = 24 runs

24 runs x 60 cases/run = 1440 failure-case rows

```



Methods:



```text

B1 = ResNet18 + CE + SupCon

B5 = ResNet18 + BNNeck + CE

B6 = ResNet18 + BNNeck + ArcFace

B8 = ResNet18 + CosFace

```



Failure categories:



```text

false\_accept\_top\_score

false\_reject\_low\_score

rank1\_misidentification

```



Reconstruction rule:



```text

sim\_matrix = probe\_embeddings @ gallery\_embeddings.T

gen\_mask = label\_mask \& \~self\_mask

imp\_mask = \~label\_mask \& \~self\_mask

scores.csv = concat(pos\_scores, neg\_scores)

```



Sanity check result:



```text

scores rows = 1,440,000

genuine pairs = 12,000

impostor pairs = 1,428,000

score order = genuine block first, impostor block second

```



\## Protocol checklist



Protocol checklist:



```text

docs/audits/rankb\_strict\_protocol\_checklist.md

```



Checklist covers:



\* split discipline

\* metric discipline

\* checkpoint-selection discipline

\* baseline discipline

\* statistical discipline

\* failure-analysis discipline

\* reproducibility discipline

\* supported and unsupported claims



\## Verification commands



Compile Phase 3 scripts:



```bat

set PYTHONPATH=%CD%

python -m py\_compile scripts\\generate\_cosface\_baseline\_configs.py scripts\\aggregate\_cosface\_baseline\_results.py scripts\\export\_strict\_tongji\_failure\_cases.py

```



Regenerate deterministic Phase 3 exports:



```bat

python scripts\\aggregate\_cosface\_baseline\_results.py

python scripts\\export\_strict\_tongji\_failure\_cases.py

git status --short

```



Expected:



```text

Wrote docs/results/strict\_tongji\_b8\_cosface\_detail.csv rows=6

Wrote docs/results/strict\_tongji\_additional\_baselines.csv rows=3

Wrote docs/results/strict\_tongji\_additional\_baselines.md

Wrote docs/results/strict\_tongji\_failure\_cases.csv rows=1440

Wrote docs/results/strict\_tongji\_failure\_case\_summary.csv rows=24

Wrote docs/results/strict\_tongji\_failure\_case\_summary.md

git status --short is empty

```



\## Version-control safety



Do not commit:



```text

experiments/

revision\_patches/

\*.pt

\*.pth

\*.ckpt

\*.onnx

\*.zip

\*.npy

\*.npz

```



Committed Phase 3 artifacts are scripts, configs, CSV/Markdown tables, audits, and manifests only.



\## Supported claims



Supported:



\* B8 adds a generic learned CosFace comparator under the same strict Tongji setup.

\* B8 is not palmprint-specific.

\* B8 provides an additional margin-loss baseline outside the B0--B7 component matrix.

\* Failure-case analysis reconstructs score-tail false accepts, score-tail false rejects, and rank-1 misidentifications from saved scores and split metadata.

\* Conservative TAR@FAR discipline remains active.



Not supported:



\* State-of-the-art claim.

\* B8 as a palmprint-specific baseline.

\* B8 as a replacement for PalmNet, CompNet, or Competitive Code.

\* Full ArcFace margin/scale sensitivity sweep.

\* Visual failure-cause claim without additional image-quality measurements.

\* Fully subject-disjoint Tongji claim unless explicitly audited with true subject-disjoint metadata.



\## Status



PASS.



