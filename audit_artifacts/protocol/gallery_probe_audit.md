# Gallery/Probe Construction Audit

## Scope

This audit verifies that final gallery/probe partitions are constructed as closed-set enrollment/probe splits over the same held-out palm classes, with no image overlap and with the expected session direction.

## Evaluation-code evidence

The evaluation script loads `gallery` and `probe` partitions separately, extracts embeddings, computes a probe-by-gallery cosine similarity matrix, uses class-label equality for Rank-k matching, and derives EER/TAR from genuine/impostor probe-gallery pairs.

## Verdict counts

| Verdict | Count |
|---|---:|
| PASS | 9 |
| FAIL | 0 |

## Split-level audit

| Dataset | Direction | Seed | Gallery images | Probe images | Gallery classes | Probe classes | Image overlap | Gallery sessions | Probe sessions | Status | Verdict |
|---|---|---:|---:|---:|---:|---:|---:|---|---|---|---|
| Tongji | S1->S2 | 42 | 1200 | 1200 | 120 | 120 | 0 | session1 | session2 | cross-session | PASS |
| Tongji | S1->S2 | 2026 | 1200 | 1200 | 120 | 120 | 0 | session1 | session2 | cross-session | PASS |
| Tongji | S1->S2 | 2705 | 1200 | 1200 | 120 | 120 | 0 | session1 | session2 | cross-session | PASS |
| Tongji | S2->S1 | 42 | 1200 | 1200 | 120 | 120 | 0 | session2 | session1 | cross-session | PASS |
| Tongji | S2->S1 | 2026 | 1200 | 1200 | 120 | 120 | 0 | session2 | session1 | cross-session | PASS |
| Tongji | S2->S1 | 2705 | 1200 | 1200 | 120 | 120 | 0 | session2 | session1 | cross-session | PASS |
| IITD | within-session | 42 | 238 | 276 | 92 | 92 | 0 | session1 | session1 | within-session-only | PASS |
| IITD | within-session | 2026 | 251 | 276 | 92 | 92 | 0 | session1 | session1 | within-session-only | PASS |
| IITD | within-session | 2705 | 242 | 276 | 92 | 92 | 0 | session1 | session1 | within-session-only | PASS |

## Interpretation

All audited splits use matching gallery/probe palm-class sets with disjoint images. Tongji splits are cross-session in the intended direction; IITD is within-session only and must remain secondary validation rather than cross-session evidence.

Detailed machine-readable rows are stored in `audit_artifacts/protocol/gallery_probe_audit.csv`.
