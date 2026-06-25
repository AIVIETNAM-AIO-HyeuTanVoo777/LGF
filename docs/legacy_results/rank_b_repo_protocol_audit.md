# Rank-B Repo and Protocol Audit

> [!NOTE]
> Superseded for final protocol verdict by [rank_b_final_split_verdict.md](file:///d:/0.Research/PALM_CGK_BASE/PALM_CGK_BASE/docs/results/rank_b_final_split_verdict.md). The earlier FAIL_OVERLAP flag treated train-val subject overlap as invalid; final protocol treats train and val as development sets and audits development/test subject disjointness.

## Manifest schema

- Manifest: `data/metadata/palm_segmented_manifest.csv`
- Total rows: 14601
- Columns: `path, dataset, session, hand, subject_id, palm_id, class_id, sample_id`
- Detected dataset column: `dataset`
- Detected subject column: `subject_id`
- Detected identity column: `subject_id`
- Detected palm_or_class column: `palm_id`
- Detected session column: `session`
- Detected path column: `path`
- Detected width column: `None`
- Detected height column: `None`
- Safe paper terminology based on detected schema: **subject-disjoint**

## Dataset rows

- Dataset value counts:
  - `Tongji`: 12000
  - `IITD`: 2601
- Tongji rows detected: 12000
- IITD rows detected: 2601

## Existing Tongji disjoint split files

- Found files: 6

### data/splits/tongji_subject_disjoint_s1_to_s2_seed2026.json

- SHA256: `62b35375625f29293073602c0e171618615c21d975714c87ef339d46dc8fc265`
- Split item counts:
  - train: 3840
  - val: 960
  - gallery: 1200
  - probe: 1200
  - support: 0
- Identity counts:
  - train: 480
  - val: 432
  - gallery: 120
  - probe: 120
  - support: 0
- Session counts:
  - train: {'session1': 3840}
  - val: {'session1': 960}
  - gallery: {'session1': 1200}
  - probe: {'session2': 1200}
  - support: {}
- Resolution diagnostics:
  - train: unresolved_items=0, ambiguous_path_matches=3840
  - val: unresolved_items=0, ambiguous_path_matches=960
  - gallery: unresolved_items=0, ambiguous_path_matches=1200
  - probe: unresolved_items=0, ambiguous_path_matches=1200
  - support: unresolved_items=0, ambiguous_path_matches=0
- Overlap checks:
  - train∩val: 432
  - train∩test: 0
  - val∩test: 0
  - gallery∩probe: 120 (expected: nonzero and usually equal held-out test identities)
- VERDICT: FAIL_OVERLAP

### data/splits/tongji_subject_disjoint_s1_to_s2_seed2705.json

- SHA256: `301cb16134bc992bc0348e3bd136883c88f698c35af59571c3a4f547c867a1bf`
- Split item counts:
  - train: 3840
  - val: 960
  - gallery: 1200
  - probe: 1200
  - support: 0
- Identity counts:
  - train: 480
  - val: 433
  - gallery: 120
  - probe: 120
  - support: 0
- Session counts:
  - train: {'session1': 3840}
  - val: {'session1': 960}
  - gallery: {'session1': 1200}
  - probe: {'session2': 1200}
  - support: {}
- Resolution diagnostics:
  - train: unresolved_items=0, ambiguous_path_matches=3840
  - val: unresolved_items=0, ambiguous_path_matches=960
  - gallery: unresolved_items=0, ambiguous_path_matches=1200
  - probe: unresolved_items=0, ambiguous_path_matches=1200
  - support: unresolved_items=0, ambiguous_path_matches=0
- Overlap checks:
  - train∩val: 433
  - train∩test: 0
  - val∩test: 0
  - gallery∩probe: 120 (expected: nonzero and usually equal held-out test identities)
- VERDICT: FAIL_OVERLAP

### data/splits/tongji_subject_disjoint_s1_to_s2_seed42.json

- SHA256: `75238463a4561033a19532fe20fffca9f32f79d79ae4a9318b6d6e19eb309c15`
- Split item counts:
  - train: 3840
  - val: 960
  - gallery: 1200
  - probe: 1200
  - support: 0
- Identity counts:
  - train: 480
  - val: 427
  - gallery: 120
  - probe: 120
  - support: 0
- Session counts:
  - train: {'session1': 3840}
  - val: {'session1': 960}
  - gallery: {'session1': 1200}
  - probe: {'session2': 1200}
  - support: {}
- Resolution diagnostics:
  - train: unresolved_items=0, ambiguous_path_matches=3840
  - val: unresolved_items=0, ambiguous_path_matches=960
  - gallery: unresolved_items=0, ambiguous_path_matches=1200
  - probe: unresolved_items=0, ambiguous_path_matches=1200
  - support: unresolved_items=0, ambiguous_path_matches=0
- Overlap checks:
  - train∩val: 427
  - train∩test: 0
  - val∩test: 0
  - gallery∩probe: 120 (expected: nonzero and usually equal held-out test identities)
- VERDICT: FAIL_OVERLAP

### data/splits/tongji_subject_disjoint_s2_to_s1_seed2026.json

- SHA256: `2c2e1764a427ff266507094af25d9f60d21ca88a1fe1e061f6d7f0c0dc685d38`
- Split item counts:
  - train: 3840
  - val: 960
  - gallery: 1200
  - probe: 1200
  - support: 0
- Identity counts:
  - train: 480
  - val: 432
  - gallery: 120
  - probe: 120
  - support: 0
- Session counts:
  - train: {'session2': 3840}
  - val: {'session2': 960}
  - gallery: {'session2': 1200}
  - probe: {'session1': 1200}
  - support: {}
- Resolution diagnostics:
  - train: unresolved_items=0, ambiguous_path_matches=3840
  - val: unresolved_items=0, ambiguous_path_matches=960
  - gallery: unresolved_items=0, ambiguous_path_matches=1200
  - probe: unresolved_items=0, ambiguous_path_matches=1200
  - support: unresolved_items=0, ambiguous_path_matches=0
- Overlap checks:
  - train∩val: 432
  - train∩test: 0
  - val∩test: 0
  - gallery∩probe: 120 (expected: nonzero and usually equal held-out test identities)
- VERDICT: FAIL_OVERLAP

### data/splits/tongji_subject_disjoint_s2_to_s1_seed2705.json

- SHA256: `6e768a21d33202d01d67ff86bf1794211531cbdb694aff1352b9d6e5edf6c3d6`
- Split item counts:
  - train: 3840
  - val: 960
  - gallery: 1200
  - probe: 1200
  - support: 0
- Identity counts:
  - train: 480
  - val: 433
  - gallery: 120
  - probe: 120
  - support: 0
- Session counts:
  - train: {'session2': 3840}
  - val: {'session2': 960}
  - gallery: {'session2': 1200}
  - probe: {'session1': 1200}
  - support: {}
- Resolution diagnostics:
  - train: unresolved_items=0, ambiguous_path_matches=3840
  - val: unresolved_items=0, ambiguous_path_matches=960
  - gallery: unresolved_items=0, ambiguous_path_matches=1200
  - probe: unresolved_items=0, ambiguous_path_matches=1200
  - support: unresolved_items=0, ambiguous_path_matches=0
- Overlap checks:
  - train∩val: 433
  - train∩test: 0
  - val∩test: 0
  - gallery∩probe: 120 (expected: nonzero and usually equal held-out test identities)
- VERDICT: FAIL_OVERLAP

### data/splits/tongji_subject_disjoint_s2_to_s1_seed42.json

- SHA256: `c302c8b966efa5c52b3abd1a821273fa0f36702b992548c8be5788fc097c375e`
- Split item counts:
  - train: 3840
  - val: 960
  - gallery: 1200
  - probe: 1200
  - support: 0
- Identity counts:
  - train: 480
  - val: 427
  - gallery: 120
  - probe: 120
  - support: 0
- Session counts:
  - train: {'session2': 3840}
  - val: {'session2': 960}
  - gallery: {'session2': 1200}
  - probe: {'session1': 1200}
  - support: {}
- Resolution diagnostics:
  - train: unresolved_items=0, ambiguous_path_matches=3840
  - val: unresolved_items=0, ambiguous_path_matches=960
  - gallery: unresolved_items=0, ambiguous_path_matches=1200
  - probe: unresolved_items=0, ambiguous_path_matches=1200
  - support: unresolved_items=0, ambiguous_path_matches=0
- Overlap checks:
  - train∩val: 427
  - train∩test: 0
  - val∩test: 0
  - gallery∩probe: 120 (expected: nonzero and usually equal held-out test identities)
- VERDICT: FAIL_OVERLAP

## IITD disjoint split files

- Found files: 3
  - `data/splits/iitd_subject_disjoint_within_seed2026.json` SHA256 `ef4fa4c8a7d010950f2638258bd2877dbfd74cda9967221a3b7c6363b52c6026`
  - `data/splits/iitd_subject_disjoint_within_seed2705.json` SHA256 `912f145726859f4f0b211e45f997b96fc091031f8deabdd22f1240f3dc0d306e`
  - `data/splits/iitd_subject_disjoint_within_seed42.json` SHA256 `9e0e0014980293fac7068220d9806ac764286acc27b72cc0f87f98a292b10cc3`

## Final recommendation

- Do not start B1/B6 training until the Tongji split audit verdicts are PASS or only documented PASS_WITH_WARNINGS.
- If no true `subject_id` column exists, use `identity-disjoint`, `palm-disjoint`, or `class-disjoint` in the paper instead of `subject-disjoint`.
- IITD should remain secondary validation and must not be described as cross-session unless a real session column supports that claim.
