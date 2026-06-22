# Split Integrity Summary

This document provides verification results for all subject-disjoint split files, checking for duplicate paths, image existence, partition size, and identity leakage (overlap between development and test subsets).

## Split File: `iitd_subject_disjoint_within_seed2026.json`

- **SHA256 Checksum**: `ef4fa4c8a7d010950f2638258bd2877dbfd74cda9967221a3b7c6363b52c6026`
### Partition Sizes

| Partition | Images | Subjects | Palms | Classes |
|-----------|--------|----------|-------|---------|
| train | 1659 | 184 | 368 | 368 |
| val | 415 | 168 | 261 | 261 |
| gallery | 263 | 46 | 89 | 89 |
| probe | 264 | 46 | 89 | 89 |

### Security & Leakage Checks

- [x] **Duplicate Paths**: None found (passed).
- [x] **File Existence**: All referenced images exist on disk (passed).
- [x] **Subject Leakage**: 0 overlapping subjects (passed subject-disjoint constraint).
- [x] **Palm Leakage**: 0 overlapping palms (passed).
- [x] **Class Leakage**: 0 overlapping classes (passed).

---

## Split File: `iitd_subject_disjoint_within_seed2705.json`

- **SHA256 Checksum**: `912f145726859f4f0b211e45f997b96fc091031f8deabdd22f1240f3dc0d306e`
### Partition Sizes

| Partition | Images | Subjects | Palms | Classes |
|-----------|--------|----------|-------|---------|
| train | 1666 | 184 | 368 | 368 |
| val | 417 | 170 | 267 | 267 |
| gallery | 259 | 46 | 89 | 89 |
| probe | 259 | 46 | 91 | 91 |

### Security & Leakage Checks

- [x] **Duplicate Paths**: None found (passed).
- [x] **File Existence**: All referenced images exist on disk (passed).
- [x] **Subject Leakage**: 0 overlapping subjects (passed subject-disjoint constraint).
- [x] **Palm Leakage**: 0 overlapping palms (passed).
- [x] **Class Leakage**: 0 overlapping classes (passed).

---

## Split File: `iitd_subject_disjoint_within_seed42.json`

- **SHA256 Checksum**: `9e0e0014980293fac7068220d9806ac764286acc27b72cc0f87f98a292b10cc3`
### Partition Sizes

| Partition | Images | Subjects | Palms | Classes |
|-----------|--------|----------|-------|---------|
| train | 1670 | 184 | 368 | 368 |
| val | 417 | 172 | 270 | 270 |
| gallery | 257 | 46 | 89 | 89 |
| probe | 257 | 46 | 88 | 88 |

### Security & Leakage Checks

- [x] **Duplicate Paths**: None found (passed).
- [x] **File Existence**: All referenced images exist on disk (passed).
- [x] **Subject Leakage**: 0 overlapping subjects (passed subject-disjoint constraint).
- [x] **Palm Leakage**: 0 overlapping palms (passed).
- [x] **Class Leakage**: 0 overlapping classes (passed).

---

## Split File: `tongji_subject_disjoint_s1_to_s2_seed2026.json`

- **SHA256 Checksum**: `62b35375625f29293073602c0e171618615c21d975714c87ef339d46dc8fc265`
### Partition Sizes

| Partition | Images | Subjects | Palms | Classes |
|-----------|--------|----------|-------|---------|
| train | 3840 | 480 | 480 | 480 |
| val | 960 | 432 | 432 | 432 |
| gallery | 1200 | 120 | 120 | 120 |
| probe | 1200 | 120 | 120 | 120 |

### Security & Leakage Checks

- [x] **Duplicate Paths**: None found (passed).
- [x] **File Existence**: All referenced images exist on disk (passed).
- [x] **Subject Leakage**: 0 overlapping subjects (passed subject-disjoint constraint).
- [x] **Palm Leakage**: 0 overlapping palms (passed).
- [x] **Class Leakage**: 0 overlapping classes (passed).

---

## Split File: `tongji_subject_disjoint_s1_to_s2_seed2705.json`

- **SHA256 Checksum**: `301cb16134bc992bc0348e3bd136883c88f698c35af59571c3a4f547c867a1bf`
### Partition Sizes

| Partition | Images | Subjects | Palms | Classes |
|-----------|--------|----------|-------|---------|
| train | 3840 | 480 | 480 | 480 |
| val | 960 | 433 | 433 | 433 |
| gallery | 1200 | 120 | 120 | 120 |
| probe | 1200 | 120 | 120 | 120 |

### Security & Leakage Checks

- [x] **Duplicate Paths**: None found (passed).
- [x] **File Existence**: All referenced images exist on disk (passed).
- [x] **Subject Leakage**: 0 overlapping subjects (passed subject-disjoint constraint).
- [x] **Palm Leakage**: 0 overlapping palms (passed).
- [x] **Class Leakage**: 0 overlapping classes (passed).

---

## Split File: `tongji_subject_disjoint_s1_to_s2_seed42.json`

- **SHA256 Checksum**: `75238463a4561033a19532fe20fffca9f32f79d79ae4a9318b6d6e19eb309c15`
### Partition Sizes

| Partition | Images | Subjects | Palms | Classes |
|-----------|--------|----------|-------|---------|
| train | 3840 | 480 | 480 | 480 |
| val | 960 | 427 | 427 | 427 |
| gallery | 1200 | 120 | 120 | 120 |
| probe | 1200 | 120 | 120 | 120 |

### Security & Leakage Checks

- [x] **Duplicate Paths**: None found (passed).
- [x] **File Existence**: All referenced images exist on disk (passed).
- [x] **Subject Leakage**: 0 overlapping subjects (passed subject-disjoint constraint).
- [x] **Palm Leakage**: 0 overlapping palms (passed).
- [x] **Class Leakage**: 0 overlapping classes (passed).

---

## Split File: `tongji_subject_disjoint_s2_to_s1_seed2026.json`

- **SHA256 Checksum**: `2c2e1764a427ff266507094af25d9f60d21ca88a1fe1e061f6d7f0c0dc685d38`
### Partition Sizes

| Partition | Images | Subjects | Palms | Classes |
|-----------|--------|----------|-------|---------|
| train | 3840 | 480 | 480 | 480 |
| val | 960 | 432 | 432 | 432 |
| gallery | 1200 | 120 | 120 | 120 |
| probe | 1200 | 120 | 120 | 120 |

### Security & Leakage Checks

- [x] **Duplicate Paths**: None found (passed).
- [x] **File Existence**: All referenced images exist on disk (passed).
- [x] **Subject Leakage**: 0 overlapping subjects (passed subject-disjoint constraint).
- [x] **Palm Leakage**: 0 overlapping palms (passed).
- [x] **Class Leakage**: 0 overlapping classes (passed).

---

## Split File: `tongji_subject_disjoint_s2_to_s1_seed2705.json`

- **SHA256 Checksum**: `6e768a21d33202d01d67ff86bf1794211531cbdb694aff1352b9d6e5edf6c3d6`
### Partition Sizes

| Partition | Images | Subjects | Palms | Classes |
|-----------|--------|----------|-------|---------|
| train | 3840 | 480 | 480 | 480 |
| val | 960 | 433 | 433 | 433 |
| gallery | 1200 | 120 | 120 | 120 |
| probe | 1200 | 120 | 120 | 120 |

### Security & Leakage Checks

- [x] **Duplicate Paths**: None found (passed).
- [x] **File Existence**: All referenced images exist on disk (passed).
- [x] **Subject Leakage**: 0 overlapping subjects (passed subject-disjoint constraint).
- [x] **Palm Leakage**: 0 overlapping palms (passed).
- [x] **Class Leakage**: 0 overlapping classes (passed).

---

## Split File: `tongji_subject_disjoint_s2_to_s1_seed42.json`

- **SHA256 Checksum**: `c302c8b966efa5c52b3abd1a821273fa0f36702b992548c8be5788fc097c375e`
### Partition Sizes

| Partition | Images | Subjects | Palms | Classes |
|-----------|--------|----------|-------|---------|
| train | 3840 | 480 | 480 | 480 |
| val | 960 | 427 | 427 | 427 |
| gallery | 1200 | 120 | 120 | 120 |
| probe | 1200 | 120 | 120 | 120 |

### Security & Leakage Checks

- [x] **Duplicate Paths**: None found (passed).
- [x] **File Existence**: All referenced images exist on disk (passed).
- [x] **Subject Leakage**: 0 overlapping subjects (passed subject-disjoint constraint).
- [x] **Palm Leakage**: 0 overlapping palms (passed).
- [x] **Class Leakage**: 0 overlapping classes (passed).

---

