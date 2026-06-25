\# Failure Case Analysis Audit



\## Purpose



This audit records the strict Tongji failure-case export added in Phase 3.



The goal is to provide diagnostic evidence beyond aggregate tables, without adding unsupported visual-quality or image-based claims.



\## Scope



Methods:



\* B1: ResNet18 + CE + SupCon

\* B5: ResNet18 + BNNeck + CE

\* B6: ResNet18 + BNNeck + ArcFace

\* B8: ResNet18 + CosFace



Protocol:



\* Tongji strict palm-class-disjoint cross-session protocol

\* directions: S1 -> S2 and S2 -> S1

\* seeds: 42, 2026, 2705



Total run summaries:



```text

4 methods x 2 directions x 3 seeds = 24 runs

```



Exported failure cases:



```text

24 runs x 60 cases/run = 1440 rows

```



\## Input artifacts



The export uses local non-versioned experiment artifacts:



\* `experiments/\*/scores.csv`

\* `data/splits/tongji\_subject\_disjoint\_s1\_to\_s2\_seed\*.json`

\* `data/splits/tongji\_subject\_disjoint\_s2\_to\_s1\_seed\*.json`



The export does not require checkpoint files.



\## Output artifacts



Versioned outputs:



\* `docs/results/strict\_tongji\_failure\_cases.csv`

\* `docs/results/strict\_tongji\_failure\_case\_summary.csv`

\* `docs/results/strict\_tongji\_failure\_case\_summary.md`

\* `scripts/export\_strict\_tongji\_failure\_cases.py`



Non-versioned local artifacts:



\* `experiments/\*/scores.csv`

\* checkpoint files under `experiments/\*/checkpoints/`



\## Reconstruction rule



The original `scores.csv` files contain only:



```text

score,label

```



The failure-case export reconstructs pair metadata using:



1\. split JSON gallery/probe order,

2\. `eval\_embedding.py` pair construction,

3\. saved score ordering.



The evaluation script computes:



```text

sim\_matrix = probe\_embeddings @ gallery\_embeddings.T

label\_mask = probe\_labels\[:, None] == gallery\_labels\[None, :]

gen\_mask = label\_mask \& \~self\_mask

imp\_mask = \~label\_mask \& \~self\_mask

pos\_scores = sim\_matrix\[gen\_mask]

neg\_scores = sim\_matrix\[imp\_mask]

scores.csv = concat(pos\_scores, neg\_scores)

```



A sanity check confirmed the reconstructed pair counts and score-label ordering for the audited split:



```text

scores rows: 1,440,000

genuine pairs: 12,000

impostor pairs: 1,428,000

score labels: 12,000 genuine and 1,428,000 impostor

boundary order: genuine block first, then impostor block

```



\## Exported failure categories



For each method/direction/seed run, the script exports:



1\. `false\_accept\_top\_score`



&#x20;  \* top 20 impostor pairs with highest similarity scores.



2\. `false\_reject\_low\_score`



&#x20;  \* top 20 genuine pairs with lowest similarity scores.



3\. `rank1\_misidentification`



&#x20;  \* top 20 probe samples whose highest-scoring gallery match has a different class.



Each row includes reconstructed:



\* probe path

\* gallery path

\* probe subject/palm/class/sample metadata

\* gallery subject/palm/class/sample metadata

\* score

\* conservative threshold at FAR=1e-3

\* empirical FAR

\* TAR at FAR=1e-3

\* whether the score is an error at the selected threshold where applicable



\## Summary outputs



The summary table reports, per method/direction/seed:



\* selected conservative threshold at FAR=1e-3

\* empirical FAR

\* TAR at FAR=1e-3

\* false accepts at threshold

\* false rejects at threshold

\* rank-1 misidentification count

\* reconstructed rank-1 accuracy



The reconstructed rank-1 accuracies match the corresponding evaluation metrics, validating the pair reconstruction.



\## Claim boundary



Safe wording:



\* Failure cases are reconstructed from saved pair scores and split metadata.

\* The analysis identifies score-tail false accepts, score-tail false rejects, and rank-1 misidentifications.

\* The analysis provides diagnostic evidence about genuine collapse and impostor-tail behavior.

\* The analysis should be reported without displaying images unless dataset policy permits image display.



Unsafe wording:



\* Do not claim image-quality causes unless brightness/sharpness/quality features are separately computed.

\* Do not claim visual identity leakage from paths alone.

\* Do not include dataset images in figures unless redistribution/display permission is confirmed.

\* Do not treat local checkpoint files as versioned reproducibility artifacts.



\## Status



PASS.



