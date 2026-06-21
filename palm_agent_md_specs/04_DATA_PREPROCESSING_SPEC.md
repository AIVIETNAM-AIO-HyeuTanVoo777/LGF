# Data and Preprocessing Specification

## 1. Supported datasets

The codebase must support:

- CASIA
- TJU
- XJTU
- IITD

## 2. Unified metadata schema

Create one CSV per dataset:

```csv
sample_id,dataset,image_path,subject_id,palm_id,class_id,gender,hand_side,session,image_index,is_valid,notes
```

### Field definitions

| Field | Required | Description |
|---|---:|---|
| `sample_id` | yes | Unique stable sample identifier |
| `dataset` | yes | CASIA/TJU/XJTU/IITD |
| `image_path` | yes | Absolute or project-relative image path |
| `subject_id` | yes | Person ID |
| `palm_id` | yes | Unique palm class, usually subject + left/right |
| `class_id` | yes | Integer label for model training |
| `gender` | no | male/female/unknown |
| `hand_side` | yes if available | left/right/unknown |
| `session` | no | Session ID, especially TJU |
| `image_index` | no | Image sequence number |
| `is_valid` | yes | Whether sample is retained |
| `notes` | no | Cleaning/parsing note |

## 3. Split protocol

Paper protocol:

- Remove defective data first.
- Split remaining images into train/test with 1:1 ratio per category.
- If a category has odd number of samples, randomly remove one before split.

Implementation:

```python
def create_half_split(metadata, class_key="palm_id", seed=42):
    for palm_id, rows in groupby(metadata, class_key):
        valid_rows = rows[rows.is_valid]
        shuffled = deterministic_shuffle(valid_rows, seed)
        if len(shuffled) % 2 == 1:
            dropped = shuffled.pop()
            log_drop(dropped)
        n = len(shuffled) // 2
        train += shuffled[:n]
        test += shuffled[n:]
    return train, test
```

Acceptance:

- Train and test counts are equal per palm ID.
- No overlap.
- Dropped samples are logged.
- Same seed gives identical split.

## 4. ROI policy

The paper assumes palmprint ROI images but does not give a concrete ROI extractor.

Default:

```text
IMPLEMENTATION ASSUMPTION:
Input images are already ROI images.
Use IdentityROIExtractor.
```

Required interface:

```python
class ROIExtractor:
    def extract(self, image: np.ndarray) -> np.ndarray:
        raise NotImplementedError

class IdentityROIExtractor(ROIExtractor):
    def extract(self, image: np.ndarray) -> np.ndarray:
        return image
```

## 5. Image preprocessing

### For Gabor

```text
read image
→ ROI extractor
→ convert to grayscale
→ resize to 224×224
→ convert to float32
→ normalize to [0, 1]
```

### For Conformer

```text
read image
→ ROI extractor
→ convert to RGB
→ resize to 224×224
→ convert to tensor [3, 224, 224]
→ normalize with configured mean/std
```

## 6. Dataset-specific notes

### CASIA

Expected metadata:

- subject ID
- left/right hand
- gender if available

If gender mapping is not available in files:

```text
gender = unknown
```

or use a user-provided metadata file:

```text
data/metadata/casia_subject_gender.csv
```

### TJU

Expected:

- subject ID
- left/right hand
- session

TJU has two acquisition sessions.

### XJTU

Expected:

- color images
- subject ID
- left/right hand if available

For Gabor, convert color to grayscale.

### IITD

Expected:

- grayscale images
- subject ID
- left/right hand if available

Gender may be missing; use unknown.

## 7. PyTorch dataset contract

```python
class PalmprintDataset(torch.utils.data.Dataset):
    def __getitem__(self, idx):
        return {
            "image": tensor,
            "label": class_id,
            "sample_id": sample_id,
            "subject_id": subject_id,
            "palm_id": palm_id,
            "gender": gender,
            "hand_side": hand_side,
            "image_path": image_path,
        }
```
