# Checkpoint-Selection Audit

This audit checks that public run-manifest checkpoint paths are relative, checkpoints are not bundled, and the configured selection policy uses validation data rather than held-out gallery/probe data.

- Source manifest: `audit_artifacts/manifests/run_manifest.csv`
- Rows audited: 48
- PASS: 48
- FAIL: 0

| Dataset | Method | Direction | Seed | Selection metric | Uses gallery/probe? | Verdict |
|---|---|---|---:|---|---|---|
| Tongji | M0 | S1->S2 | 42 | validation_rank1 | false | PASS |
| Tongji | M0 | S1->S2 | 2026 | validation_rank1 | false | PASS |
| Tongji | M0 | S1->S2 | 2705 | validation_rank1 | false | PASS |
| Tongji | M0 | S2->S1 | 42 | validation_rank1 | false | PASS |
| Tongji | M0 | S2->S1 | 2026 | validation_rank1 | false | PASS |
| Tongji | M0 | S2->S1 | 2705 | validation_rank1 | false | PASS |
| Tongji | M1 | S1->S2 | 42 | validation_rank1 | false | PASS |
| Tongji | M1 | S1->S2 | 2026 | validation_rank1 | false | PASS |
| Tongji | M1 | S1->S2 | 2705 | validation_rank1 | false | PASS |
| Tongji | M1 | S2->S1 | 42 | validation_rank1 | false | PASS |
| Tongji | M1 | S2->S1 | 2026 | validation_rank1 | false | PASS |
| Tongji | M1 | S2->S1 | 2705 | validation_rank1 | false | PASS |
| Tongji | M2 | S1->S2 | 42 | validation_rank1 | false | PASS |
| Tongji | M2 | S1->S2 | 2026 | validation_rank1 | false | PASS |
| Tongji | M2 | S1->S2 | 2705 | validation_rank1 | false | PASS |
| Tongji | M2 | S2->S1 | 42 | validation_rank1 | false | PASS |
| Tongji | M2 | S2->S1 | 2026 | validation_rank1 | false | PASS |
| Tongji | M2 | S2->S1 | 2705 | validation_rank1 | false | PASS |
| Tongji | M4 | S1->S2 | 42 | validation_rank1 | false | PASS |
| Tongji | M4 | S1->S2 | 2026 | validation_rank1 | false | PASS |
| Tongji | M4 | S1->S2 | 2705 | validation_rank1 | false | PASS |
| Tongji | M4 | S2->S1 | 42 | validation_rank1 | false | PASS |
| Tongji | M4 | S2->S1 | 2026 | validation_rank1 | false | PASS |
| Tongji | M4 | S2->S1 | 2705 | validation_rank1 | false | PASS |
| Tongji | M6 | S1->S2 | 42 | validation_rank1 | false | PASS |
| Tongji | M6 | S1->S2 | 2026 | validation_rank1 | false | PASS |
| Tongji | M6 | S1->S2 | 2705 | validation_rank1 | false | PASS |
| Tongji | M6 | S2->S1 | 42 | validation_rank1 | false | PASS |
| Tongji | M6 | S2->S1 | 2026 | validation_rank1 | false | PASS |
| Tongji | M6 | S2->S1 | 2705 | validation_rank1 | false | PASS |
| Tongji | M7 | S1->S2 | 42 | validation_rank1 | false | PASS |
| Tongji | M7 | S1->S2 | 2026 | validation_rank1 | false | PASS |
| Tongji | M7 | S1->S2 | 2705 | validation_rank1 | false | PASS |
| Tongji | M7 | S2->S1 | 42 | validation_rank1 | false | PASS |
| Tongji | M7 | S2->S1 | 2026 | validation_rank1 | false | PASS |
| Tongji | M7 | S2->S1 | 2705 | validation_rank1 | false | PASS |
| Tongji | M3 | S1->S2 | 42 | validation_rank1 | false | PASS |
| Tongji | M3 | S1->S2 | 2026 | validation_rank1 | false | PASS |
| Tongji | M3 | S1->S2 | 2705 | validation_rank1 | false | PASS |
| Tongji | M3 | S2->S1 | 42 | validation_rank1 | false | PASS |
| Tongji | M3 | S2->S1 | 2026 | validation_rank1 | false | PASS |
| Tongji | M3 | S2->S1 | 2705 | validation_rank1 | false | PASS |
| IITD | M1 | within | 42 | validation_eer | false | PASS |
| IITD | M1 | within | 2026 | validation_eer | false | PASS |
| IITD | M1 | within | 2705 | validation_eer | false | PASS |
| IITD | M6 | within | 42 | validation_eer | false | PASS |
| IITD | M6 | within | 2026 | validation_eer | false | PASS |
| IITD | M6 | within | 2705 | validation_eer | false | PASS |

Detailed machine-readable rows are stored in `audit_artifacts/protocol/checkpoint_selection_audit.csv`.
