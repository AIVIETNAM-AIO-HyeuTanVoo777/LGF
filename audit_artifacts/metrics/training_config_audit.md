# Training Configuration Audit

This audit summarizes the training/evaluation configuration fields used by the final strict Tongji component-ablation runs.

- Source run table: `audit_artifacts/manifests/run_manifest.csv`.
- Source configs: YAML files listed in the `config_path` column of the run table.
- Scope: M0/M1/M2/M3/M4/M6/M7 under the audited Tongji palm-class-disjoint cross-session protocol.
- Each method has six configs: two session directions and three seeds.
- Fields that intentionally vary across configs are seed, split file, save directory, and session direction.

## Method-level summary

| Method | Model | Loss | Eval embedding | SupCon lambda | ArcFace | Epochs | LR | WD | Sampler | AMP | Verdict |
|---|---|---|---|---:|---|---:|---:|---:|---|---|---|
| M0 ResNet18 + CE | ResNet18Baseline | ce | default L2 | 0.0 | - | 60 | 0.0001 | 0.0001 | 8x2 | True | PASS |
| M1 ResNet18 + CE + SupCon | ResNet18Baseline | ce+supcon | default L2 | 0.1 | - | 60 | 0.0001 | 0.0001 | 8x2 | True | PASS |
| M2 ResNet18 + ArcFace | ResNet18Baseline | arcface | default L2 | 0.0 | s=30.0, m=0.5 | 60 | 0.0001 | 0.0001 | 8x2 | True | PASS |
| M3 ResNet18 + CosFace | ResNet18Baseline | cosface | default L2 | 0.0 | s=30.0, m=0.35 | 60 | 0.0001 | 0.0001 | 8x2 | True | PASS |
| M4 ResNet18 + BNNeck + CE | ResNet18BNNeck | ce | post-BN | 0.0 | - | 60 | 0.0001 | 0.0001 | 8x2 | True | PASS |
| M6 ResNet18 + BNNeck + ArcFace | ResNet18BNNeck | arcface | post-BN | 0.0 | s=30.0, m=0.5 | 60 | 0.0001 | 0.0001 | 8x2 | True | PASS |
| M7 ResNet18 + BNNeck + ArcFace + light SupCon | ResNet18BNNeck | arcface | post-BN | 0.02 | s=30.0, m=0.5 | 60 | 0.0001 | 0.0001 | 8x2 | True | PASS |

## Reviewer-facing notes

- All final strict Tongji methods use 60 epochs, learning rate 1e-4, weight decay 1e-4, AMP enabled, and gradient accumulation of four steps.
- M1 uses supervised contrastive regularization with temperature 0.07.
- M4 isolates BNNeck with cross-entropy by using BNNeck/post-BN evaluation and lambda_supcon 0.0.
- M6 isolates BNNeck+ArcFace by using BNNeck/post-BN evaluation, ArcFace scale 30.0, margin 0.5, and lambda_supcon 0.0.
- M7 adds a light supervised contrastive term to BNNeck+ArcFace.
- Config filenames retain historical `subject_disjoint` naming, but the paper claim remains palm-class-disjoint according to the identity/parser and gallery/probe audits.
