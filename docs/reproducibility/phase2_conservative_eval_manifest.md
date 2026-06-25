\# Phase 2 Conservative Evaluation Manifest



\## Repository state



Repository:



```text

D:\\0.Research\\PALM\_CGK\_BASE\\PALM\_CGK\_BASE

```



Branch:



```text

phase2-eval-regenerate-arcface-sensitivity

```



Phase 2 HEAD before this manifest:



```text

6c4a017 Add training recipe reproducibility audit

```



Immediate commit chain:



```text

6c4a017 Add training recipe reproducibility audit

7b1047d Export conservative threshold evidence supplement

ac5ee88 Regenerate conservative evaluation tables

31febd4 Update final audit generator wording

4b59299 Add reproducibility manifest

961aff9 Add ArcFace sensitivity plan and evidence

fe0ed8a Clarify palm-class protocol and scoped claims

```



\## Purpose



This manifest records the Phase 2 conservative-evaluation supplement added after the corrected Rank-B revision baseline.



Phase 2 does not introduce a new model architecture claim. It strengthens reproducibility around:



1\. conservative TAR@FAR table exports,

2\. threshold-level conservative evidence,

3\. training/preprocessing recipe documentation,

4\. claim boundaries for B1/B6/B5 interpretation.



\## Phase 2 commits



\### `ac5ee88 Regenerate conservative evaluation tables`



Added or regenerated paper-facing conservative evaluation outputs:



```text

docs/audits/conservative\_tar\_far\_recompute.md

docs/results/gabor\_reference\_summary.csv

docs/results/iitd\_corrected\_summary.csv

docs/results/iitd\_subject\_disjoint\_summary\_SUPERSEDED\_USE\_RERUN.md

docs/results/paired\_delta\_b6\_vs\_b1.md

docs/results/paper\_ready\_tables.md

docs/results/strict\_tongji\_directional\_deltas.csv

docs/results/strict\_tongji\_main\_b1\_b6.csv

docs/results/strict\_tongji\_paired\_tests.csv

docs/results/tongji\_directional\_metrics\_full.md

docs/results/tongji\_subject\_disjoint\_summary.md

scripts/phase2\_export\_required\_tables.py

```



Key output check:



```text

strict\_tongji\_main\_b1\_b6.csv rows=2

strict\_tongji\_directional\_deltas.csv rows=6

strict\_tongji\_ablation\_summary.csv rows=18

strict\_tongji\_paired\_tests.csv rows=6

iitd\_corrected\_summary.csv rows=2

gabor\_reference\_summary.csv rows=4

```



\### `7b1047d Export conservative threshold evidence supplement`



Added threshold-level conservative evidence:



```text

docs/audits/threshold\_evidence\_conservative\_tar\_far.md

docs/results/threshold\_evidence\_conservative\_tar\_far.csv

scripts/export\_conservative\_threshold\_evidence.py

```



Observed check:



```text

Rows exported: 84

Rows with target and empirical FAR available: 84

Violations: 0

MAX(empirical\_far - target\_far): 0.0

```



\### `6c4a017 Add training recipe reproducibility audit`



Added training recipe audit:



```text

docs/audits/training\_recipe\_full\_audit.md

```



Confirmed B1/B6 strict Tongji recipe:



```text

epochs: 60

lr: 0.0001

weight\_decay: 0.0001

grad\_accumulation\_steps: 4

amp: true

sampler.num\_identities: 8

sampler.num\_instances: 2

sampler.fallback\_identities: 4

effective configured sampler batch: 8 identities x 2 instances = 16 samples

embedding\_dim: 256

pretrained: true

```



B1 confirmed recipe:



```text

model.name: ResNet18Baseline

loss family: CE + SupCon

lambda\_supcon: 0.1

temperature: 0.07

```



B6 confirmed recipe:



```text

model.name: ResNet18BNNeck

model.eval\_embedding: post\_bn

eval.embedding: post\_bn

loss.name: arcface

loss.scale: 30.0

loss.margin: 0.5

training.loss\_type: arcface

lambda\_supcon: 0.0

temperature: 0.07

```



Sampler implementation check:



```text

palmrec/datasets/samplers.py

class RandomIdentitySampler(Sampler)

num\_instances is K

num\_identities is P

fallback\_identities is fallback P

```



\## Scientific interpretation after Phase 2



The Phase 2 outputs preserve the corrected central interpretation:



```text

B6 does not provide reliable improvement over B1 under the audited strict Tongji palm-class-disjoint cross-session protocol.

```



The strict Tongji summary after conservative recomputation shows:



```text

B1 Rank-1 mean: 93.388888 pp

B6 Rank-1 mean: 92.208334 pp



B1 EER mean: 4.254855 pp

B6 EER mean: 5.269620 pp



B1 TAR@FAR=1e-3 mean: 71.770833 pp

B6 TAR@FAR=1e-3 mean: 69.706944 pp

```



B5 remains only an observed-mean finding:



```text

B5 has the highest observed mean among the listed learned variants for selected strict Tongji metrics, but this is not a statistical superiority claim.

```



\## Claim boundaries



Safe wording:



```text

conservative TAR@FAR

palm-class-disjoint strict Tongji protocol

validation-only checkpoint selection

fixed ArcFace recipe with scale 30.0 and margin 0.5

B6 does not reliably improve over B1 under the audited strict Tongji protocol

B5 has the highest observed mean on selected metrics, without statistical superiority claim

```



Unsafe wording:



```text

nearest-FPR TAR@FAR

B6 improves over B1 under strict Tongji

full ArcFace margin/scale sensitivity sweep

state-of-the-art claim

true subject-disjoint claim unless true subject\_id supports it

test/gallery/probe-driven checkpoint or hyperparameter selection

```



\## Final verification commands for this Phase 2 state



Run from repository root:



```bat

git status --short

git --no-pager log --oneline -8

python -m py\_compile scripts\\phase2\_export\_required\_tables.py scripts\\export\_conservative\_threshold\_evidence.py

python scripts\\phase2\_export\_required\_tables.py

python scripts\\export\_conservative\_threshold\_evidence.py

python -m py\_compile palmrec\\evaluation\\metrics.py palmrec\\evaluation\\\_\_init\_\_.py scripts\\eval\_embedding.py scripts\\evaluate\_gabor\_strict\_tongji\_baseline.py scripts\\audit\_metric\_thresholds.py scripts\\audit\_training\_config\_table.py scripts\\audit\_paper\_references.py scripts\\finalize\_rank\_b\_protocol\_audit.py

python -m pytest tests\\test\_metrics\_tar\_far.py tests\\test\_evaluation.py -q

```



Expected:



```text

working tree clean

threshold evidence Violations: 0

7 passed

```



\## Status



PASS.



