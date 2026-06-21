# AGENT Master Prompt — Audit PALM_CGK_BASE

You are a Senior ML Engineering Auditor and Research Integrity Reviewer. Audit the local repository `PALM_CGK_BASE` for palmprint recognition.

Working directory:

```bat
D:\0.Research\PALM_CGK_BASE\PALM_CGK_BASE
```

Environment:

```bat
conda activate palm_lgf
```

Your task is to verify whether the project is technically correct, internally consistent, numerically honest, and aligned with the current defensible paper direction.

Read and apply all audit specs:

```text
palm_agent_audit_specs/02_EXPECTED_STATE_AND_SCOPE.md
palm_agent_audit_specs/03_DATASET_SPLIT_AUDIT.md
palm_agent_audit_specs/04_CONFIG_EXPERIMENT_AUDIT.md
palm_agent_audit_specs/05_CODE_MODEL_TRAIN_EVAL_AUDIT.md
palm_agent_audit_specs/06_METRICS_RESULTS_AUDIT.md
palm_agent_audit_specs/07_CLAIM_PAPER_AUDIT.md
palm_agent_audit_specs/08_GIT_REPRODUCIBILITY_AUDIT.md
palm_agent_audit_specs/09_REPORT_TEMPLATE.md
```

## Hard rules

1. Do not train models unless explicitly instructed.
2. Do not modify source code, configs, metrics, or Git history during the audit.
3. You may create one audit report file only: `docs/results/final_integrity_audit.md`.
4. Do not guess missing data. Mark it as `BLOCKED` or `UNKNOWN`.
5. Every conclusion must include evidence: file path, command output, metric file, config value, or test result.
6. Distinguish between:
   - `verified from files`
   - `verified by command`
   - `not verifiable because checkpoint/log is missing`
7. Treat `docs/results/tongji_s1s2_summary.md` as a summary, not a ground-truth source. Ground truth should be per-experiment `metrics.md`, `metrics.json`, configs, split files, and available command output.
8. Final decision must say whether the paper claim is:
   - `SUPPORTED`
   - `PARTIALLY SUPPORTED`
   - `NOT SUPPORTED`
   - `BLOCKED BY MISSING EVIDENCE`

## Required commands to run first

```bat
git status
git rev-parse HEAD
git ls-tree -r --name-only HEAD | findstr /i /c:"experiments/" /c:".pt" /c:".pth" /c:".ckpt"
pytest -q
```

Expected:

- `git status` should be clean and up to date with `origin/main`.
- no committed `experiments/` or model checkpoint files.
- `pytest -q` should pass, expected previous value: `45 passed`.

## Required final output

Use `09_REPORT_TEMPLATE.md`. The report must include:

1. Executive verdict.
2. PASS/FAIL/BLOCKED table.
3. Dataset and split integrity results.
4. Config-to-result consistency results.
5. Metric verification against expected values.
6. Code/model/eval audit findings.
7. Git and reproducibility audit.
8. Paper claim decision.
9. Required fixes before paper writing.
10. Optional next experiments.

Do not produce a vague summary. Produce an evidence-backed audit.
