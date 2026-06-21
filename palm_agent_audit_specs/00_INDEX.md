# PALM_CGK_BASE Audit Spec — Index

Purpose: provide a strict checklist and execution prompt for an AGENT to verify whether the PALM_CGK_BASE project is technically consistent, numerically correct, and aligned with the defensible paper direction.

Use these files in order:

1. `01_AUDIT_MASTER_PROMPT.md` — main prompt to paste into the AGENT.
2. `02_EXPECTED_STATE_AND_SCOPE.md` — expected project state, non-goals, and audit boundaries.
3. `03_DATASET_SPLIT_AUDIT.md` — dataset manifest and split integrity checks.
4. `04_CONFIG_EXPERIMENT_AUDIT.md` — config, experiment, and result-file consistency checks.
5. `05_CODE_MODEL_TRAIN_EVAL_AUDIT.md` — model/code/eval/training audit criteria.
6. `06_METRICS_RESULTS_AUDIT.md` — exact metric tables to verify.
7. `07_CLAIM_PAPER_AUDIT.md` — claim validation rules.
8. `08_GIT_REPRODUCIBILITY_AUDIT.md` — Git, artifact, and reproducibility hygiene.
9. `09_REPORT_TEMPLATE.md` — required final report format.

Critical rule: the AGENT must not invent missing logs, metrics, or paper claims. Every PASS/FAIL must cite concrete evidence from files, commands, or terminal output.
