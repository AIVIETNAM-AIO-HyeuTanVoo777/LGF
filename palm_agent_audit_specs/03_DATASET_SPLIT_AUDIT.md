# Dataset and Split Integrity Audit

## Required files

Check existence:

```text
data/metadata/palm_segmented_manifest.csv
data/splits/cross_dataset_fewshot.json
data/splits/iitd_within.json
data/splits/tongji_s1_to_s2.json
data/splits/tongji_s2_to_s1.json
data/splits/toy_split_seed42.json
```

## Expected manifest schema

Expected columns:

```text
path,dataset,session,hand,subject_id,palm_id,class_id,sample_id,norm_path
```

Expected total rows:

```text
14601
```

Expected dataset counts:

```text
IITD: 2601
Tongji: 12000
```

## Expected IITD state

Expected image layout:

```text
data/segmented/IITD/Left/*.bmp
data/segmented/IITD/Right/*.bmp
```

Expected counts:

```text
IITD total: 2601
Left: 1301
Right: 1300
Image size: 150x150
Classes: 460 palms/classes
```

Expected labeling rule:

```text
filename example: 001_1.bmp
class_id: IITD_Left_001 or IITD_Right_001
left/right are separate classes
```

## Expected Tongji state

Expected image layout:

```text
data/segmented/Tongji/session1/*.bmp
data/segmented/Tongji/session2/*.bmp
```

Expected counts:

```text
Tongji total: 12000
session1: 6000
session2: 6000
Image size: 128x128
Classes: 600 palms/classes
```

Expected labeling rule:

```text
In each session, 00001~00010 = first palm, 00011~00020 = second palm, etc.
palm_id = (image_number - 1) // 10 + 1
sample_id = (image_number - 1) % 10 + 1
same filename in session1/session2 = same palm
class_id: Tongji_0001, Tongji_0002, ...
```

## Expected split counts

```text
cross_dataset_fewshot.json:
  train: 4800
  val: 1200
  gallery: 920
  probe: 1681
  support: 920

iitd_within.json:
  train: 1681
  val: 460
  gallery: 1681
  probe: 460
  support: 0

tongji_s1_to_s2.json:
  train: 4800
  val: 1200
  gallery: 6000
  probe: 6000
  support: 0

tongji_s2_to_s1.json:
  train: 4800
  val: 1200
  gallery: 6000
  probe: 6000
  support: 0
```

## Required checks

The AGENT must verify:

1. All split paths exist in manifest.
2. Missing path count is zero for every split.
3. Tongji S1->S2:
   - train/val/gallery must be session1;
   - probe must be session2.
4. Tongji S2->S1:
   - train/val/gallery must be session2;
   - probe must be session1.
5. IITD within:
   - train/gallery size 1681;
   - val/probe size 460;
   - 460 classes;
   - no missing manifest paths.
6. No accidental raw-data dependency is required for evaluation summaries.

## Suggested commands

Use existing scripts if available:

```bat
python inspect_splits.py
python verify_splits.py
```

If those scripts are missing or incomplete, write a temporary one-off Python check in terminal or report `BLOCKED` with reason.
