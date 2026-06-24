# Metric Threshold Audit

This audit verifies verification pair counts and threshold conventions for the strict Tongji ablation runs.

## Summary

- Audited runs: 36
- Verdicts: PASS=36, WARN=0, FAIL=0
- Pair count shapes `(genuine, impostor, total)`: [(12000, 1428000, 1440000)]
- Minimum empirical FAR step values: ['7.00280112045e-07']
- EER convention: sklearn ROC with brentq/interp1d interpolation when possible; fallback is nearest |FPR-FNR|.
- EER interpolation statuses: ['brentq_interp1d']
- TAR@FAR convention in `scripts/eval_embedding.py`: choose the ROC point with nearest empirical FPR to the target FAR, not necessarily the largest FPR less than or equal to the target.

## Protocol note for paper

Verification thresholds are swept over observed cosine scores using `sklearn.metrics.roc_curve`. A pair is accepted when its cosine score is greater than or equal to the threshold. EER is computed by interpolating the ROC curve with `brentq`/`interp1d` when possible, with a nearest `|FPR-FNR|` fallback. TAR@FAR is reported at the ROC point whose empirical FPR is nearest to the target FAR (`10^{-2}` or `10^{-3}`). The audit reports genuine/impostor comparison counts, minimum empirical FAR step, and the threshold selected for each seed-direction-method run.

## Per-run threshold audit

| Method | Direction | Seed | Genuine | Impostor | min FAR step | EER | TAR@1e-2 nearest FPR | TAR@1e-3 nearest FPR | Verdict |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| B0 | S1->S2 | 42 | 12000 | 1428000 | 7.0028e-07 | 0.0644468 | 0.0100028 | 0.001 | PASS |
| B0 | S1->S2 | 2026 | 12000 | 1428000 | 7.0028e-07 | 0.0477493 | 0.01 | 0.001 | PASS |
| B0 | S1->S2 | 2705 | 12000 | 1428000 | 7.0028e-07 | 0.0403333 | 0.0100133 | 0.001 | PASS |
| B0 | S2->S1 | 42 | 12000 | 1428000 | 7.0028e-07 | 0.0499167 | 0.0099958 | 0.0010007 | PASS |
| B0 | S2->S1 | 2026 | 12000 | 1428000 | 7.0028e-07 | 0.0420287 | 0.0100035 | 0.0009993 | PASS |
| B0 | S2->S1 | 2705 | 12000 | 1428000 | 7.0028e-07 | 0.0466134 | 0.00998739 | 0.0009993 | PASS |
| B1 | S1->S2 | 42 | 12000 | 1428000 | 7.0028e-07 | 0.05675 | 0.0099881 | 0.001 | PASS |
| B1 | S1->S2 | 2026 | 12000 | 1428000 | 7.0028e-07 | 0.0391106 | 0.0099958 | 0.001 | PASS |
| B1 | S1->S2 | 2705 | 12000 | 1428000 | 7.0028e-07 | 0.0390091 | 0.01 | 0.001 | PASS |
| B1 | S2->S1 | 42 | 12000 | 1428000 | 7.0028e-07 | 0.0382731 | 0.0099909 | 0.0009993 | PASS |
| B1 | S2->S1 | 2026 | 12000 | 1428000 | 7.0028e-07 | 0.04325 | 0.0100105 | 0.0010007 | PASS |
| B1 | S2->S1 | 2705 | 12000 | 1428000 | 7.0028e-07 | 0.0388985 | 0.0100014 | 0.0010014 | PASS |
| B4 | S1->S2 | 42 | 12000 | 1428000 | 7.0028e-07 | 0.05375 | 0.0099944 | 0.001 | PASS |
| B4 | S1->S2 | 2026 | 12000 | 1428000 | 7.0028e-07 | 0.0537066 | 0.0100042 | 0.0010007 | PASS |
| B4 | S1->S2 | 2705 | 12000 | 1428000 | 7.0028e-07 | 0.0405 | 0.0100021 | 0.001 | PASS |
| B4 | S2->S1 | 42 | 12000 | 1428000 | 7.0028e-07 | 0.0463326 | 0.0099937 | 0.000998599 | PASS |
| B4 | S2->S1 | 2026 | 12000 | 1428000 | 7.0028e-07 | 0.0563739 | 0.0099902 | 0.0010028 | PASS |
| B4 | S2->S1 | 2705 | 12000 | 1428000 | 7.0028e-07 | 0.0525 | 0.0100028 | 0.0010007 | PASS |
| B5 | S1->S2 | 42 | 12000 | 1428000 | 7.0028e-07 | 0.0513137 | 0.01 | 0.0009993 | PASS |
| B5 | S1->S2 | 2026 | 12000 | 1428000 | 7.0028e-07 | 0.0430224 | 0.0099979 | 0.0010021 | PASS |
| B5 | S1->S2 | 2705 | 12000 | 1428000 | 7.0028e-07 | 0.039 | 0.0099888 | 0.001 | PASS |
| B5 | S2->S1 | 42 | 12000 | 1428000 | 7.0028e-07 | 0.0455 | 0.0100049 | 0.001 | PASS |
| B5 | S2->S1 | 2026 | 12000 | 1428000 | 7.0028e-07 | 0.0529083 | 0.0099986 | 0.001 | PASS |
| B5 | S2->S1 | 2705 | 12000 | 1428000 | 7.0028e-07 | 0.05175 | 0.010007 | 0.001 | PASS |
| B6 | S1->S2 | 42 | 12000 | 1428000 | 7.0028e-07 | 0.05725 | 0.0100112 | 0.001 | PASS |
| B6 | S1->S2 | 2026 | 12000 | 1428000 | 7.0028e-07 | 0.0491772 | 0.0099923 | 0.001 | PASS |
| B6 | S1->S2 | 2705 | 12000 | 1428000 | 7.0028e-07 | 0.054 | 0.0099972 | 0.0010014 | PASS |
| B6 | S2->S1 | 42 | 12000 | 1428000 | 7.0028e-07 | 0.05625 | 0.0099986 | 0.001 | PASS |
| B6 | S2->S1 | 2026 | 12000 | 1428000 | 7.0028e-07 | 0.0454167 | 0.0099986 | 0.0010014 | PASS |
| B6 | S2->S1 | 2705 | 12000 | 1428000 | 7.0028e-07 | 0.0540833 | 0.0099965 | 0.000998599 | PASS |
| B7 | S1->S2 | 42 | 12000 | 1428000 | 7.0028e-07 | 0.0515833 | 0.0100084 | 0.0009993 | PASS |
| B7 | S1->S2 | 2026 | 12000 | 1428000 | 7.0028e-07 | 0.04725 | 0.0100084 | 0.0010007 | PASS |
| B7 | S1->S2 | 2705 | 12000 | 1428000 | 7.0028e-07 | 0.061 | 0.0100014 | 0.0010007 | PASS |
| B7 | S2->S1 | 42 | 12000 | 1428000 | 7.0028e-07 | 0.0456695 | 0.0099958 | 0.0009993 | PASS |
| B7 | S2->S1 | 2026 | 12000 | 1428000 | 7.0028e-07 | 0.0393683 | 0.0099979 | 0.000997899 | PASS |
| B7 | S2->S1 | 2705 | 12000 | 1428000 | 7.0028e-07 | 0.0474167 | 0.0099958 | 0.0010007 | PASS |
