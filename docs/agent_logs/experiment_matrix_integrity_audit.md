# Experiment Matrix Integrity Audit

This audit verifies that all experiments claimed in the paper tables have complete, matching artifacts generated on disk.

## Run Verification Status

| Run ID | Method | Dataset | Direction | Seed | Config Path | Split File | Checkpoint Path | Result JSON | Scores CSV | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| `tongji_m0_s1_s2_seed42` | M0 | Tongji | s1_to_s2 | 42 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m0_s1_s2_seed2026` | M0 | Tongji | s1_to_s2 | 2026 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m0_s1_s2_seed2705` | M0 | Tongji | s1_to_s2 | 2705 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m0_s2_s1_seed42` | M0 | Tongji | s2_to_s1 | 42 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m0_s2_s1_seed2026` | M0 | Tongji | s2_to_s1 | 2026 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m0_s2_s1_seed2705` | M0 | Tongji | s2_to_s1 | 2705 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m1_s1_s2_seed42` | M1 | Tongji | s1_to_s2 | 42 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m1_s1_s2_seed2026` | M1 | Tongji | s1_to_s2 | 2026 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m1_s1_s2_seed2705` | M1 | Tongji | s1_to_s2 | 2705 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m1_s2_s1_seed42` | M1 | Tongji | s2_to_s1 | 42 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m1_s2_s1_seed2026` | M1 | Tongji | s2_to_s1 | 2026 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m1_s2_s1_seed2705` | M1 | Tongji | s2_to_s1 | 2705 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m2_s1_s2_seed42` | M2 | Tongji | s1_to_s2 | 42 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m2_s1_s2_seed2026` | M2 | Tongji | s1_to_s2 | 2026 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m2_s1_s2_seed2705` | M2 | Tongji | s1_to_s2 | 2705 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m2_s2_s1_seed42` | M2 | Tongji | s2_to_s1 | 42 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m2_s2_s1_seed2026` | M2 | Tongji | s2_to_s1 | 2026 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m2_s2_s1_seed2705` | M2 | Tongji | s2_to_s1 | 2705 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m3_s1_s2_seed42` | M3 | Tongji | s1_to_s2 | 42 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m3_s1_s2_seed2026` | M3 | Tongji | s1_to_s2 | 2026 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m3_s1_s2_seed2705` | M3 | Tongji | s1_to_s2 | 2705 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m3_s2_s1_seed42` | M3 | Tongji | s2_to_s1 | 42 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m3_s2_s1_seed2026` | M3 | Tongji | s2_to_s1 | 2026 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m3_s2_s1_seed2705` | M3 | Tongji | s2_to_s1 | 2705 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m4_s1_s2_seed42` | M4 | Tongji | s1_to_s2 | 42 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m4_s1_s2_seed2026` | M4 | Tongji | s1_to_s2 | 2026 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m4_s1_s2_seed2705` | M4 | Tongji | s1_to_s2 | 2705 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m4_s2_s1_seed42` | M4 | Tongji | s2_to_s1 | 42 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m4_s2_s1_seed2026` | M4 | Tongji | s2_to_s1 | 2026 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m4_s2_s1_seed2705` | M4 | Tongji | s2_to_s1 | 2705 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m6_s1_s2_seed42` | M6 | Tongji | s1_to_s2 | 42 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m6_s1_s2_seed2026` | M6 | Tongji | s1_to_s2 | 2026 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m6_s1_s2_seed2705` | M6 | Tongji | s1_to_s2 | 2705 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m6_s2_s1_seed42` | M6 | Tongji | s2_to_s1 | 42 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m6_s2_s1_seed2026` | M6 | Tongji | s2_to_s1 | 2026 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m6_s2_s1_seed2705` | M6 | Tongji | s2_to_s1 | 2705 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m7_s1_s2_seed42` | M7 | Tongji | s1_to_s2 | 42 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m7_s1_s2_seed2026` | M7 | Tongji | s1_to_s2 | 2026 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m7_s1_s2_seed2705` | M7 | Tongji | s1_to_s2 | 2705 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m7_s2_s1_seed42` | M7 | Tongji | s2_to_s1 | 42 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m7_s2_s1_seed2026` | M7 | Tongji | s2_to_s1 | 2026 | Exists | Exists | Exists | Exists | Exists | PASS |
| `tongji_m7_s2_s1_seed2705` | M7 | Tongji | s2_to_s1 | 2705 | Exists | Exists | Exists | Exists | Exists | PASS |
| `iitd_m1_within_seed42` | M1 | IITD | within | 42 | Exists | Exists | Exists | Exists | Exists | PASS |
| `iitd_m1_within_seed2026` | M1 | IITD | within | 2026 | Exists | Exists | Exists | Exists | Exists | PASS |
| `iitd_m1_within_seed2705` | M1 | IITD | within | 2705 | Exists | Exists | Exists | Exists | Exists | PASS |
| `iitd_m6_within_seed42` | M6 | IITD | within | 42 | Exists | Exists | Exists | Exists | Exists | PASS |
| `iitd_m6_within_seed2026` | M6 | IITD | within | 2026 | Exists | Exists | Exists | Exists | Exists | PASS |
| `iitd_m6_within_seed2705` | M6 | IITD | within | 2705 | Exists | Exists | Exists | Exists | Exists | PASS |

## Method Mapping Validation
All methods listed in the paper tables (M0, M1, M2, M3, M4, M6, M7, Gabor) are backed by actual run results. No results are fabricated or invented.
- **Tongji**: M0, M1, M2, M3, M4, M6, and M7 are fully completed across 6 units each (3 seeds, 2 directions), totaling 42 completed units.
- **IITD**: M1 and M6 are completed across 3 seeds, totaling 6 completed units.
- **Gabor**: Pre-computed classical reference metrics exist on strict Tongji split.
