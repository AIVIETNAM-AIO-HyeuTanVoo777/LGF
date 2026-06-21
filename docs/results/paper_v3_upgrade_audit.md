# Paper V3 Upgrade Audit

## Scope

Tongji primary, IITD secondary. No third dataset.

## Paper changes

## Protocol changes

## Citation changes

## Ethics/privacy changes

## Reproducibility changes

### Config Generation Status
- **Status**: Successfully generated and validated core B1 & B6 configs.
- **Configs Created**: 18 configs total (12 for Tongji, 6 for IITD).
- **Skipped Configs**: None.
- **Schema Assumptions**:
  - Config files parse as standard YAML.
  - Template keys like `seed`, `save_dir`, and `dataset.split_file` are the only parameters requiring updates for seed and split sweeps.
  - Core recipes (ResNet18Baseline + CE + SupCon for B1, ResNet18BNNeck + ArcFace for B6) are preserved from the corresponding templates.

## Claims checked

```text
[x] No SOTA claim
[x] No universal superiority claim
[x] No Gabor superiority claim
[x] No IITD dominance claim
[x] No subject-disjoint wording unless subject_id is used
```

## Remaining TODOs
- Run B1/B6 models using the generated configs.

