# Rank-B Protocol Lock

## 1. Paper Framing
Use this framing:
```text
Audited protocol-sensitive evaluation of recognition heads and losses for held-out palm-class cross-session palmprint recognition.
```

Explicitly not claimed:
- New architecture
- State-of-the-art performance
- Universal BNNeck+ArcFace superiority
- Cross-dataset robustness
- Person-disjointness unless independently verified

## 2. Datasets

### Dataset: Tongji
- **Manifest path**: `data/metadata/palm_segmented_manifest.csv`
- **Image root**: `data/segmented/Tongji`
- **Image size**: 128x128 (input resized to 224x224 in dataloader)
- **Number of images**: 12000 total (7200 used in S1->S2 or S2->S1 protocol splits)
- **Number of palm classes**: 600
- **Number of sessions**: 2
- **Session labels**: `session1`, `session2`
- **Subject/person identifier available?**: yes (`subject_id` matches palm class, as hand side is "none" in the dataset)
- **Palm-class identifier available?**: yes (`class_id` / `palm_id`)
- **Permitted claim**: `palm-class-disjoint` / `cross-session` (conservatively capped at palm-class-disjoint because no independent person-level identity is verified by audit)

### Dataset: IITD
- **Manifest path**: `data/metadata/palm_segmented_manifest.csv`
- **Image root**: `data/segmented/IITD`
- **Image size**: 150x150 (input resized to 224x224 in dataloader)
- **Number of images**: 2601 total (all used in within-session protocol splits)
- **Number of palm classes**: 460 (representing 230 subjects, left/right hand side)
- **Number of sessions**: 1
- **Session labels**: `session1`
- **Subject/person identifier available?**: yes (`subject_id` represents person since 2 hands exist per subject)
- **Palm-class identifier available?**: yes (`class_id` / `palm_id`)
- **Permitted claim**: `palm-class-disjoint` / `within-session only` (conservatively capped at palm-class-disjoint because no independent person-level identity is verified by audit)

## 3. Primary Protocol
Primary evidence must be Tongji held-out palm-class cross-session.

For each seed (42, 2026, 2705) and direction (S1->S2, S2->S1):
- Split palm classes before training.
- Development classes (480 classes) are for train/validation/checkpoint/hyperparameter decisions.
- Held-out test classes (120 classes) are for final gallery/probe evaluation only.
- **S1→S2**: session 1 gallery, session 2 probe.
- **S2→S1**: session 2 gallery, session 1 probe.

## 4. Validation Policy
```text
Same-session development validation is used for checkpoint selection. This is leakage-safe but not a cross-session validation proxy. The paper must state this limitation explicitly.
```

## 5. Hyperparameter Policy

### ArcFace Margin
- **value**: 0.5
- **source**: literature default / previous project default
- **was held-out test used?**: no

### ArcFace Scale
- **value**: 30.0
- **source**: literature default / previous project default
- **was held-out test used?**: no

### SupCon Lambda
- **value**: 0.10
- **source**: previous project default
- **was held-out test used?**: no

### Optimizer
- **value**: AdamW
- **source**: previous project default
- **was held-out test used?**: no

### Learning Rate (LR)
- **value**: 0.0001
- **source**: previous project default
- **was held-out test used?**: no

### Batch Construction
- **value**: P=8 identities, K=2 instances (effective batch size = 16)
- **source**: previous project default
- **was held-out test used?**: no

### Epoch Count
- **value**: 60
- **source**: previous project default
- **was held-out test used?**: no

### Augmentations
- **value**: Resize to 224x224, RandomAffine (degrees=(-8, 8), translate=(0.05, 0.05), scale=(0.95, 1.05)), ColorJitter (brightness=0.1, contrast=0.1), RandomGamma (0.9, 1.1), ImageNet Normalization (mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
- **source**: previous project default
- **was held-out test used?**: no

## 6. Metric Policy
```text
TAR@FAR is computed with a conservative empirical-FAR rule. The selected threshold must satisfy empirical FAR <= target FAR. Nearest ROC point selection is forbidden if it can exceed target FAR.
```

## 7. Reporting Policy
Main result unit:
```text
Report mean ± std over matched seed-direction units for Tongji unless explicitly stated otherwise.
```
Paired deltas must compare methods on the same seed and direction.
