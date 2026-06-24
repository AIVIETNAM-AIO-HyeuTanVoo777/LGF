# Checkpoint-Selection Audit

## Scope

This audit covers the final strict Tongji rows in `docs/results/strict_tongji_ablation_runs.csv`.

## Training-code rule

scripts/train_lgf.py selects best.pt using validation Rank-1 when available, otherwise validation loss.

The audit checks that the validation split does not overlap gallery/probe/test paths and attempts to reconstruct the selected epoch from training logs or `best.pt`.

## Verdict counts

| Verdict | Count |
|---|---:|
| PASS | 36 |
| PARTIAL | 0 |
| UNCLEAR | 0 |
| FAIL | 0 |

## Audit table

| Method | Direction | Seed | Metric | Selected epoch | Uses gallery/probe/test | Verdict |
|---|---|---:|---|---:|---|---|
| B0 | S1->S2 | 42 | val_rank1 | 15 | NO | PASS |
| B0 | S1->S2 | 2026 | val_rank1 | 23 | NO | PASS |
| B0 | S1->S2 | 2705 | val_rank1 | 31 | NO | PASS |
| B0 | S2->S1 | 42 | val_rank1 | 21 | NO | PASS |
| B0 | S2->S1 | 2026 | val_rank1 | 22 | NO | PASS |
| B0 | S2->S1 | 2705 | val_rank1 | 21 | NO | PASS |
| B1 | S1->S2 | 42 | val_rank1 | 14 | NO | PASS |
| B1 | S1->S2 | 2026 | val_rank1 | 24 | NO | PASS |
| B1 | S1->S2 | 2705 | val_rank1 | 26 | NO | PASS |
| B1 | S2->S1 | 42 | val_rank1 | 23 | NO | PASS |
| B1 | S2->S1 | 2026 | val_rank1 | 23 | NO | PASS |
| B1 | S2->S1 | 2705 | val_rank1 | 38 | NO | PASS |
| B4 | S1->S2 | 42 | val_rank1 | 15 | NO | PASS |
| B4 | S1->S2 | 2026 | val_rank1 | 19 | NO | PASS |
| B4 | S1->S2 | 2705 | val_rank1 | 25 | NO | PASS |
| B4 | S2->S1 | 42 | val_rank1 | 16 | NO | PASS |
| B4 | S2->S1 | 2026 | val_rank1 | 19 | NO | PASS |
| B4 | S2->S1 | 2705 | val_rank1 | 18 | NO | PASS |
| B5 | S1->S2 | 42 | val_rank1 | 23 | NO | PASS |
| B5 | S1->S2 | 2026 | val_rank1 | 29 | NO | PASS |
| B5 | S1->S2 | 2705 | val_rank1 | 31 | NO | PASS |
| B5 | S2->S1 | 42 | val_rank1 | 27 | NO | PASS |
| B5 | S2->S1 | 2026 | val_rank1 | 19 | NO | PASS |
| B5 | S2->S1 | 2705 | val_rank1 | 20 | NO | PASS |
| B6 | S1->S2 | 42 | val_rank1 | 16 | NO | PASS |
| B6 | S1->S2 | 2026 | val_rank1 | 23 | NO | PASS |
| B6 | S1->S2 | 2705 | val_rank1 | 18 | NO | PASS |
| B6 | S2->S1 | 42 | val_rank1 | 16 | NO | PASS |
| B6 | S2->S1 | 2026 | val_rank1 | 24 | NO | PASS |
| B6 | S2->S1 | 2705 | val_rank1 | 20 | NO | PASS |
| B7 | S1->S2 | 42 | val_rank1 | 18 | NO | PASS |
| B7 | S1->S2 | 2026 | val_rank1 | 22 | NO | PASS |
| B7 | S1->S2 | 2705 | val_rank1 | 15 | NO | PASS |
| B7 | S2->S1 | 42 | val_rank1 | 20 | NO | PASS |
| B7 | S2->S1 | 2026 | val_rank1 | 27 | NO | PASS |
| B7 | S2->S1 | 2705 | val_rank1 | 19 | NO | PASS |

## Interpretation

All audited strict Tongji runs support validation-only checkpoint selection with no gallery/probe/test influence.

Detailed per-run notes are in `docs/audits/checkpoint_selection_audit.csv`.
