# Reproducibility

Install dependencies with:

```bash
pip install -r requirements.txt
```

Run the lightweight verification suite with:

```bash
pytest
```

Regenerate deterministic audit summaries with:

```bash
python scripts/verify_splits.py
python scripts/audit_protocol.py
```

Regenerate tables from bundled CSV summaries with:

```bash
python scripts/reproduce_main_tables.py
python scripts/reproduce_supplementary_tables.py
```

Threshold and ROC/DET recomputation requires local experiment outputs such as `scores.csv` and `roc.csv`; those files are intentionally not bundled.
