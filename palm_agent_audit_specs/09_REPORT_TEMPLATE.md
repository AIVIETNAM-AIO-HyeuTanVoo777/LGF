# Final Integrity Audit Report Template

Create exactly one report:

```text
docs/results/final_integrity_audit.md
```

Use this structure.

---

# PALM_CGK_BASE Final Integrity Audit

## 1. Executive Verdict

Overall status: `PASS` / `PASS WITH WARNINGS` / `FAIL` / `BLOCKED`

Paper claim status: `SUPPORTED` / `PARTIALLY SUPPORTED` / `NOT SUPPORTED` / `BLOCKED BY MISSING EVIDENCE`

One-paragraph conclusion.

## 2. Audit Environment

| Item | Value | Evidence |
|---|---|---|
| Working directory | | |
| Git HEAD | | |
| Branch status | | |
| Python/Conda env | | |
| Pytest result | | |

## 3. PASS/FAIL Summary

| Area | Status | Evidence | Required fix |
|---|---|---|---|
| Git hygiene | | | |
| No checkpoints in Git | | | |
| Dataset manifest | | | |
| Split integrity | | | |
| Config consistency | | | |
| Model registry | | | |
| Train/eval scripts | | | |
| Metrics consistency | | | |
| Summary correctness | | | |
| Paper claim | | | |

## 4. Dataset and Split Audit

Include manifest counts, split counts, session-direction checks, and leakage/missing-path checks.

## 5. Config and Experiment Audit

Include table:

| Experiment | Config | Split | Model | Key training recipe | Status |
|---|---|---|---|---|---|

## 6. Code Audit

Include findings for:

- model registry;
- ResNet18Baseline;
- FixedGaborResNet18;
- LGFNetSmall;
- LGFNetNoGabor;
- `train_lgf.py`;
- `eval_embedding.py`.

## 7. Metrics Verification

Include verified tables and compare saved metrics against summary.

Minimum required tables:

1. Tongji S1->S2.
2. Tongji S2->S1.
3. Tongji bidirectional average.
4. IITD within split.

For each table, indicate source file(s).

## 8. Claim Audit

State which claims are supported and rejected.

Required statements:

- Whether fixed Gabor improves strict-FAR Tongji cross-session verification.
- Whether fixed Gabor is universally superior.
- Whether learnable Gabor fusion is supported.
- Whether IITD supports or limits the claim.

## 9. Reproducibility and Artifact Policy

State what is committed, what is ignored, and what is needed to reproduce from scratch.

## 10. Required Fixes Before Paper Writing

List only necessary fixes.

## 11. Optional Next Experiments

Recommended:

1. Additional seeds for B1 and B2 on Tongji.
2. Confidence intervals or mean ± std.
3. Optional redesigned learnable-Gabor branch only if the paper direction returns to learnable fusion.

## 12. Final Decision

Use this exact format:

```text
FINAL DECISION: <PASS/PASS WITH WARNINGS/FAIL/BLOCKED>
PAPER CLAIM: <SUPPORTED/PARTIALLY SUPPORTED/NOT SUPPORTED/BLOCKED>
MAIN REASON: <one sentence>
DO NOT CLAIM: <list unsafe claims>
```
