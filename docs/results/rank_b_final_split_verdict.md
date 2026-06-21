# Rank-B Final Split Protocol Audit & Verdict

## Protocol Overview & Scope

### Paper Terminology & Definitions

> [!IMPORTANT]
> **Tongji Protocol (Primary)**: We use a development/test subject-disjoint protocol. Training and validation images are drawn from development subjects, while gallery and probe images are drawn from held-out test subjects. No subject appears in both the development set and the gallery/probe evaluation set.
> 
> **IITD Protocol (Secondary)**: IITD is used as a secondary subject-disjoint within-dataset validation. Because session metadata is not used to define a cross-session split, IITD is not treated as cross-session evidence.

### Train/Val Subject Overlap Justification
In the development phase, train and validation sets are both parts of the development set (development = train ∪ val). Since validation is used to tune hyperparameters during development rather than serving as the final held-out test evaluation, subject overlap between train and validation is allowed and does not constitute data leakage. The critical boundary is between development and test (gallery ∪ probe ∪ support). This audit enforces strict subject disjointness between the development set and the test set.

## Dataset Manifest Summary

- **Manifest path**: `data/metadata/palm_segmented_manifest.csv`
- **Total manifest rows**: 14601
- **Rows by dataset**:
  - `Tongji`: 12000
  - `IITD`: 2601

## Audit Verdict Summary

| Split File | Dataset | Total Items | Unresolved | Train-Val Overlap | Dev-Test Overlap | Gallery-Probe Overlap | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `iitd_subject_disjoint_within_seed2026.json` | IITD | 2601 | 0 | 168 | 0 | 46 | `PASS_DEVELOPMENT_TEST_SUBJECT_DISJOINT` |
| `iitd_subject_disjoint_within_seed2705.json` | IITD | 2601 | 0 | 170 | 0 | 46 | `PASS_DEVELOPMENT_TEST_SUBJECT_DISJOINT` |
| `iitd_subject_disjoint_within_seed42.json` | IITD | 2601 | 0 | 172 | 0 | 46 | `PASS_DEVELOPMENT_TEST_SUBJECT_DISJOINT` |
| `tongji_subject_disjoint_s1_to_s2_seed2026.json` | Tongji | 7200 | 0 | 432 | 0 | 120 | `PASS_DEVELOPMENT_TEST_SUBJECT_DISJOINT` |
| `tongji_subject_disjoint_s1_to_s2_seed2705.json` | Tongji | 7200 | 0 | 433 | 0 | 120 | `PASS_DEVELOPMENT_TEST_SUBJECT_DISJOINT` |
| `tongji_subject_disjoint_s1_to_s2_seed42.json` | Tongji | 7200 | 0 | 427 | 0 | 120 | `PASS_DEVELOPMENT_TEST_SUBJECT_DISJOINT` |
| `tongji_subject_disjoint_s2_to_s1_seed2026.json` | Tongji | 7200 | 0 | 432 | 0 | 120 | `PASS_DEVELOPMENT_TEST_SUBJECT_DISJOINT` |
| `tongji_subject_disjoint_s2_to_s1_seed2705.json` | Tongji | 7200 | 0 | 433 | 0 | 120 | `PASS_DEVELOPMENT_TEST_SUBJECT_DISJOINT` |
| `tongji_subject_disjoint_s2_to_s1_seed42.json` | Tongji | 7200 | 0 | 427 | 0 | 120 | `PASS_DEVELOPMENT_TEST_SUBJECT_DISJOINT` |

## Detailed File Audits

### `iitd_subject_disjoint_within_seed2026.json`

- **SHA256**: `ef4fa4c8a7d010950f2638258bd2877dbfd74cda9967221a3b7c6363b52c6026`
- **Dataset**: IITD
- **Split Item Counts**:
  - train: 1659
  - val: 415
  - gallery: 263
  - probe: 264
  - support: 0
- **Unique Subject Counts**:
  - train: 184
  - val: 168
  - gallery: 46
  - probe: 46
  - support: 0
- **Session Counts**:
  - train: `{'session1': 1659}`
  - val: `{'session1': 415}`
  - gallery: `{'session1': 263}`
  - probe: `{'session1': 264}`
  - support: `{}`
- **Resolution Diagnostics**:
  - train: unresolved_items=0
  - val: unresolved_items=0
  - gallery: unresolved_items=0
  - probe: unresolved_items=0
  - support: unresolved_items=0
- **Overlap Checks**:
  - Train ∩ Val Subject Overlap: 168
  - Dev ∩ Test Subject Overlap: 0
  - Gallery ∩ Probe Subject Overlap: 46
- **VERDICT**: `PASS_DEVELOPMENT_TEST_SUBJECT_DISJOINT`

### `iitd_subject_disjoint_within_seed2705.json`

- **SHA256**: `912f145726859f4f0b211e45f997b96fc091031f8deabdd22f1240f3dc0d306e`
- **Dataset**: IITD
- **Split Item Counts**:
  - train: 1666
  - val: 417
  - gallery: 259
  - probe: 259
  - support: 0
- **Unique Subject Counts**:
  - train: 184
  - val: 170
  - gallery: 46
  - probe: 46
  - support: 0
- **Session Counts**:
  - train: `{'session1': 1666}`
  - val: `{'session1': 417}`
  - gallery: `{'session1': 259}`
  - probe: `{'session1': 259}`
  - support: `{}`
- **Resolution Diagnostics**:
  - train: unresolved_items=0
  - val: unresolved_items=0
  - gallery: unresolved_items=0
  - probe: unresolved_items=0
  - support: unresolved_items=0
- **Overlap Checks**:
  - Train ∩ Val Subject Overlap: 170
  - Dev ∩ Test Subject Overlap: 0
  - Gallery ∩ Probe Subject Overlap: 46
- **VERDICT**: `PASS_DEVELOPMENT_TEST_SUBJECT_DISJOINT`

### `iitd_subject_disjoint_within_seed42.json`

- **SHA256**: `9e0e0014980293fac7068220d9806ac764286acc27b72cc0f87f98a292b10cc3`
- **Dataset**: IITD
- **Split Item Counts**:
  - train: 1670
  - val: 417
  - gallery: 257
  - probe: 257
  - support: 0
- **Unique Subject Counts**:
  - train: 184
  - val: 172
  - gallery: 46
  - probe: 46
  - support: 0
- **Session Counts**:
  - train: `{'session1': 1670}`
  - val: `{'session1': 417}`
  - gallery: `{'session1': 257}`
  - probe: `{'session1': 257}`
  - support: `{}`
- **Resolution Diagnostics**:
  - train: unresolved_items=0
  - val: unresolved_items=0
  - gallery: unresolved_items=0
  - probe: unresolved_items=0
  - support: unresolved_items=0
- **Overlap Checks**:
  - Train ∩ Val Subject Overlap: 172
  - Dev ∩ Test Subject Overlap: 0
  - Gallery ∩ Probe Subject Overlap: 46
- **VERDICT**: `PASS_DEVELOPMENT_TEST_SUBJECT_DISJOINT`

### `tongji_subject_disjoint_s1_to_s2_seed2026.json`

- **SHA256**: `62b35375625f29293073602c0e171618615c21d975714c87ef339d46dc8fc265`
- **Dataset**: Tongji
- **Split Item Counts**:
  - train: 3840
  - val: 960
  - gallery: 1200
  - probe: 1200
  - support: 0
- **Unique Subject Counts**:
  - train: 480
  - val: 432
  - gallery: 120
  - probe: 120
  - support: 0
- **Session Counts**:
  - train: `{'session1': 3840}`
  - val: `{'session1': 960}`
  - gallery: `{'session1': 1200}`
  - probe: `{'session2': 1200}`
  - support: `{}`
- **Resolution Diagnostics**:
  - train: unresolved_items=0
  - val: unresolved_items=0
  - gallery: unresolved_items=0
  - probe: unresolved_items=0
  - support: unresolved_items=0
- **Overlap Checks**:
  - Train ∩ Val Subject Overlap: 432
  - Dev ∩ Test Subject Overlap: 0
  - Gallery ∩ Probe Subject Overlap: 120
- **VERDICT**: `PASS_DEVELOPMENT_TEST_SUBJECT_DISJOINT`

### `tongji_subject_disjoint_s1_to_s2_seed2705.json`

- **SHA256**: `301cb16134bc992bc0348e3bd136883c88f698c35af59571c3a4f547c867a1bf`
- **Dataset**: Tongji
- **Split Item Counts**:
  - train: 3840
  - val: 960
  - gallery: 1200
  - probe: 1200
  - support: 0
- **Unique Subject Counts**:
  - train: 480
  - val: 433
  - gallery: 120
  - probe: 120
  - support: 0
- **Session Counts**:
  - train: `{'session1': 3840}`
  - val: `{'session1': 960}`
  - gallery: `{'session1': 1200}`
  - probe: `{'session2': 1200}`
  - support: `{}`
- **Resolution Diagnostics**:
  - train: unresolved_items=0
  - val: unresolved_items=0
  - gallery: unresolved_items=0
  - probe: unresolved_items=0
  - support: unresolved_items=0
- **Overlap Checks**:
  - Train ∩ Val Subject Overlap: 433
  - Dev ∩ Test Subject Overlap: 0
  - Gallery ∩ Probe Subject Overlap: 120
- **VERDICT**: `PASS_DEVELOPMENT_TEST_SUBJECT_DISJOINT`

### `tongji_subject_disjoint_s1_to_s2_seed42.json`

- **SHA256**: `75238463a4561033a19532fe20fffca9f32f79d79ae4a9318b6d6e19eb309c15`
- **Dataset**: Tongji
- **Split Item Counts**:
  - train: 3840
  - val: 960
  - gallery: 1200
  - probe: 1200
  - support: 0
- **Unique Subject Counts**:
  - train: 480
  - val: 427
  - gallery: 120
  - probe: 120
  - support: 0
- **Session Counts**:
  - train: `{'session1': 3840}`
  - val: `{'session1': 960}`
  - gallery: `{'session1': 1200}`
  - probe: `{'session2': 1200}`
  - support: `{}`
- **Resolution Diagnostics**:
  - train: unresolved_items=0
  - val: unresolved_items=0
  - gallery: unresolved_items=0
  - probe: unresolved_items=0
  - support: unresolved_items=0
- **Overlap Checks**:
  - Train ∩ Val Subject Overlap: 427
  - Dev ∩ Test Subject Overlap: 0
  - Gallery ∩ Probe Subject Overlap: 120
- **VERDICT**: `PASS_DEVELOPMENT_TEST_SUBJECT_DISJOINT`

### `tongji_subject_disjoint_s2_to_s1_seed2026.json`

- **SHA256**: `2c2e1764a427ff266507094af25d9f60d21ca88a1fe1e061f6d7f0c0dc685d38`
- **Dataset**: Tongji
- **Split Item Counts**:
  - train: 3840
  - val: 960
  - gallery: 1200
  - probe: 1200
  - support: 0
- **Unique Subject Counts**:
  - train: 480
  - val: 432
  - gallery: 120
  - probe: 120
  - support: 0
- **Session Counts**:
  - train: `{'session2': 3840}`
  - val: `{'session2': 960}`
  - gallery: `{'session2': 1200}`
  - probe: `{'session1': 1200}`
  - support: `{}`
- **Resolution Diagnostics**:
  - train: unresolved_items=0
  - val: unresolved_items=0
  - gallery: unresolved_items=0
  - probe: unresolved_items=0
  - support: unresolved_items=0
- **Overlap Checks**:
  - Train ∩ Val Subject Overlap: 432
  - Dev ∩ Test Subject Overlap: 0
  - Gallery ∩ Probe Subject Overlap: 120
- **VERDICT**: `PASS_DEVELOPMENT_TEST_SUBJECT_DISJOINT`

### `tongji_subject_disjoint_s2_to_s1_seed2705.json`

- **SHA256**: `6e768a21d33202d01d67ff86bf1794211531cbdb694aff1352b9d6e5edf6c3d6`
- **Dataset**: Tongji
- **Split Item Counts**:
  - train: 3840
  - val: 960
  - gallery: 1200
  - probe: 1200
  - support: 0
- **Unique Subject Counts**:
  - train: 480
  - val: 433
  - gallery: 120
  - probe: 120
  - support: 0
- **Session Counts**:
  - train: `{'session2': 3840}`
  - val: `{'session2': 960}`
  - gallery: `{'session2': 1200}`
  - probe: `{'session1': 1200}`
  - support: `{}`
- **Resolution Diagnostics**:
  - train: unresolved_items=0
  - val: unresolved_items=0
  - gallery: unresolved_items=0
  - probe: unresolved_items=0
  - support: unresolved_items=0
- **Overlap Checks**:
  - Train ∩ Val Subject Overlap: 433
  - Dev ∩ Test Subject Overlap: 0
  - Gallery ∩ Probe Subject Overlap: 120
- **VERDICT**: `PASS_DEVELOPMENT_TEST_SUBJECT_DISJOINT`

### `tongji_subject_disjoint_s2_to_s1_seed42.json`

- **SHA256**: `c302c8b966efa5c52b3abd1a821273fa0f36702b992548c8be5788fc097c375e`
- **Dataset**: Tongji
- **Split Item Counts**:
  - train: 3840
  - val: 960
  - gallery: 1200
  - probe: 1200
  - support: 0
- **Unique Subject Counts**:
  - train: 480
  - val: 427
  - gallery: 120
  - probe: 120
  - support: 0
- **Session Counts**:
  - train: `{'session2': 3840}`
  - val: `{'session2': 960}`
  - gallery: `{'session2': 1200}`
  - probe: `{'session1': 1200}`
  - support: `{}`
- **Resolution Diagnostics**:
  - train: unresolved_items=0
  - val: unresolved_items=0
  - gallery: unresolved_items=0
  - probe: unresolved_items=0
  - support: unresolved_items=0
- **Overlap Checks**:
  - Train ∩ Val Subject Overlap: 427
  - Dev ∩ Test Subject Overlap: 0
  - Gallery ∩ Probe Subject Overlap: 120
- **VERDICT**: `PASS_DEVELOPMENT_TEST_SUBJECT_DISJOINT`
