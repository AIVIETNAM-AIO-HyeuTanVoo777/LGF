\# Conservative TAR@FAR Recompute Audit



\## Purpose



This audit records the recomputation of result tables after replacing the previous nearest-FPR TAR@FAR rule with the conservative TAR@FAR rule.



\## Old metric rule



TAR@FAR was selected at the ROC point whose empirical false-positive rate was nearest to the requested target FAR.



This rule can be optimistic because the selected empirical FAR may exceed the requested target FAR.



\## New metric rule



For target FAR alpha, TAR@FAR is selected as the maximum TAR among thresholds satisfying:



empirical FPR <= alpha



Therefore, a reported threshold-level TAR@FAR row must not have empirical FAR above the requested target FAR.



\## Commands executed



```bat

python -m py\_compile palmrec\\evaluation\\metrics.py palmrec\\evaluation\\\_\_init\_\_.py scripts\\eval\_embedding.py scripts\\evaluate\_gabor\_strict\_tongji\_baseline.py scripts\\audit\_metric\_thresholds.py scripts\\audit\_training\_config\_table.py scripts\\audit\_paper\_references.py scripts\\finalize\_rank\_b\_protocol\_audit.py

python -m pytest tests\\test\_metrics\_tar\_far.py tests\\test\_evaluation.py -q

python scripts\\aggregate\_all\_results.py

python scripts\\aggregate\_results.py

python scripts\\make\_directional\_tables.py

python scripts\\analyze\_paired\_deltas.py

python scripts\\evaluate\_gabor\_strict\_tongji\_baseline.py

python scripts\\audit\_metric\_thresholds.py

python scripts\\finalize\_rank\_b\_protocol\_audit.py

python scripts\\phase2\_export\_required\_tables.py

