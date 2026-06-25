# Checkpoint-Selection Audit

This audit verifies that the checkpoints used for evaluation were selected using validation data only, without gallery/probe/test leakage.

| Method | Dataset | Direction | Seed | Epoch | Metric | Uses Test? | Verdict |
|---|---|---|---|---|---|---|---|
| B0 | Tongji | S1->S2 | 42 | 15 | val_rank1 | False | PASS |
| B0 | Tongji | S1->S2 | 2026 | 23 | val_rank1 | False | PASS |
| B0 | Tongji | S1->S2 | 2705 | 31 | val_rank1 | False | PASS |
| B0 | Tongji | S2->S1 | 42 | 21 | val_rank1 | False | PASS |
| B0 | Tongji | S2->S1 | 2026 | 22 | val_rank1 | False | PASS |
| B0 | Tongji | S2->S1 | 2705 | 21 | val_rank1 | False | PASS |
| B1 | Tongji | S1->S2 | 42 | 14 | val_rank1 | False | PASS |
| B1 | Tongji | S1->S2 | 2026 | 24 | val_rank1 | False | PASS |
| B1 | Tongji | S1->S2 | 2705 | 26 | val_rank1 | False | PASS |
| B1 | Tongji | S2->S1 | 42 | 23 | val_rank1 | False | PASS |
| B1 | Tongji | S2->S1 | 2026 | 23 | val_rank1 | False | PASS |
| B1 | Tongji | S2->S1 | 2705 | 38 | val_rank1 | False | PASS |
| B4 | Tongji | S1->S2 | 42 | 15 | val_rank1 | False | PASS |
| B4 | Tongji | S1->S2 | 2026 | 19 | val_rank1 | False | PASS |
| B4 | Tongji | S1->S2 | 2705 | 25 | val_rank1 | False | PASS |
| B4 | Tongji | S2->S1 | 42 | 16 | val_rank1 | False | PASS |
| B4 | Tongji | S2->S1 | 2026 | 19 | val_rank1 | False | PASS |
| B4 | Tongji | S2->S1 | 2705 | 18 | val_rank1 | False | PASS |
| B5 | Tongji | S1->S2 | 42 | 23 | val_rank1 | False | PASS |
| B5 | Tongji | S1->S2 | 2026 | 29 | val_rank1 | False | PASS |
| B5 | Tongji | S1->S2 | 2705 | 31 | val_rank1 | False | PASS |
| B5 | Tongji | S2->S1 | 42 | 27 | val_rank1 | False | PASS |
| B5 | Tongji | S2->S1 | 2026 | 19 | val_rank1 | False | PASS |
| B5 | Tongji | S2->S1 | 2705 | 20 | val_rank1 | False | PASS |
| B6 | Tongji | S1->S2 | 42 | 16 | val_rank1 | False | PASS |
| B6 | Tongji | S1->S2 | 2026 | 23 | val_rank1 | False | PASS |
| B6 | Tongji | S1->S2 | 2705 | 18 | val_rank1 | False | PASS |
| B6 | Tongji | S2->S1 | 42 | 16 | val_rank1 | False | PASS |
| B6 | Tongji | S2->S1 | 2026 | 24 | val_rank1 | False | PASS |
| B6 | Tongji | S2->S1 | 2705 | 20 | val_rank1 | False | PASS |
| B7 | Tongji | S1->S2 | 42 | 18 | val_rank1 | False | PASS |
| B7 | Tongji | S1->S2 | 2026 | 22 | val_rank1 | False | PASS |
| B7 | Tongji | S1->S2 | 2705 | 15 | val_rank1 | False | PASS |
| B7 | Tongji | S2->S1 | 42 | 20 | val_rank1 | False | PASS |
| B7 | Tongji | S2->S1 | 2026 | 27 | val_rank1 | False | PASS |
| B7 | Tongji | S2->S1 | 2705 | 19 | val_rank1 | False | PASS |
| B1 | IITD | within | 42 | 30 | val_rank1 | False | PASS |
| B1 | IITD | within | 2026 | 38 | val_rank1 | False | PASS |
| B1 | IITD | within | 2705 | 53 | val_rank1 | False | PASS |
| B6 | IITD | within | 42 | 38 | val_rank1 | False | PASS |
| B6 | IITD | within | 2026 | 36 | val_rank1 | False | PASS |
| B6 | IITD | within | 2705 | 60 | val_rank1 | False | PASS |

