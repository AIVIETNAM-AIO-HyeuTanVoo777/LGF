# Identity and Palm-Class Parser Audit

## Scope

This audit documents the manifest fields used as image, session, hand, subject, palm, and class identifiers, then verifies development/test overlap for the final Tongji and IITD split files.

## Manifest

- Source manifest: `data/metadata/palm_segmented_manifest.csv`
- Columns: `path, dataset, session, hand, subject_id, palm_id, class_id, sample_id`
- Total rows: 14601

### Counts by dataset/session

| Dataset | Session | Images |
|---|---|---:|
| IITD | session1 | 2601 |
| Tongji | session1 | 6000 |
| Tongji | session2 | 6000 |

### Unique identifiers by dataset

| Dataset | subject_id | palm_id | class_id |
|---|---:|---:|---:|
| IITD | 230 | 460 | 460 |
| Tongji | 600 | 600 | 600 |

## Parser field semantics

### Tongji parser

- Source manifest: `data/metadata/palm_segmented_manifest.csv`
- Path examples: `data/segmented/Tongji/session1/00001.bmp; data/segmented/Tongji/session1/00002.bmp; data/segmented/Tongji/session1/00003.bmp`
- Filename pattern examples: `<num>.bmp`
- `subject_id`: manifest field used for subject-ID overlap audit, but not treated as independently verified person-level identity.
- `palm_id`: manifest field used as palm identifier.
- `class_id`: manifest field used as palm-class label for training/evaluation split construction.
- `session`: manifest field used for session assignment.
- `hand`: manifest field used for left/right-hand metadata.
- Left/right handling: left and right palms are represented as separate palm/classes through `palm_id` and `class_id`; the final paper claim is capped at palm-class-disjoint.

### IITD parser

- Source manifest: `data/metadata/palm_segmented_manifest.csv`
- Path examples: `data/segmented/IITD/Left/001_1.bmp; data/segmented/IITD/Left/001_2.bmp; data/segmented/IITD/Left/001_3.bmp`
- Filename pattern examples: `<num>_<num>.bmp`
- `subject_id`: manifest field used for subject-ID overlap audit, but not treated as independently verified person-level identity.
- `palm_id`: manifest field used as palm identifier.
- `class_id`: manifest field used as palm-class label for training/evaluation split construction.
- `session`: manifest field used for session assignment.
- `hand`: manifest field used for left/right-hand metadata.
- Left/right handling: left and right palms are represented as separate palm/classes through `palm_id` and `class_id`; the final paper claim is capped at palm-class-disjoint.

## Split-level overlap audit

| Dataset | Direction | Seed | Dev classes | Test classes | Image overlap | Class overlap | Palm overlap | Subject-ID overlap | Verdict |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| Tongji | S1->S2 | 42 | 480 | 120 | 0 | 0 | 0 | 0 | PASS |
| Tongji | S1->S2 | 2026 | 480 | 120 | 0 | 0 | 0 | 0 | PASS |
| Tongji | S1->S2 | 2705 | 480 | 120 | 0 | 0 | 0 | 0 | PASS |
| Tongji | S2->S1 | 42 | 480 | 120 | 0 | 0 | 0 | 0 | PASS |
| Tongji | S2->S1 | 2026 | 480 | 120 | 0 | 0 | 0 | 0 | PASS |
| Tongji | S2->S1 | 2705 | 480 | 120 | 0 | 0 | 0 | 0 | PASS |
| IITD | within-session | 42 | 368 | 92 | 0 | 0 | 0 | 0 | PASS |
| IITD | within-session | 2026 | 368 | 92 | 0 | 0 | 0 | 0 | PASS |
| IITD | within-session | 2705 | 368 | 92 | 0 | 0 | 0 | 0 | PASS |

## Interpretation

All audited splits have zero development/test image, class_id, palm_id, and subject_id overlap. Because no independent person-level identifier is verified by this audit, the paper should continue to use the conservative term `palm-class-disjoint` rather than `person-disjoint`.

Detailed machine-readable rows are stored in `docs/audits/identity_parser_audit.csv`.
