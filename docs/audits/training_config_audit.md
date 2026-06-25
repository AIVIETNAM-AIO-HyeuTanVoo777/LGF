# Training Configuration Audit

This audit summarizes the training/evaluation configuration fields used by the final strict Tongji component-ablation runs.

- Source run table: `docs/results/strict_tongji_ablation_runs.csv`.
- Source configs: YAML files listed in the `config` column of the run table.
- Scope: B0/B1/B4/B5/B6/B7 under the strict Tongji palm-class-disjoint protocol.
- Each method has six configs: two session directions and three seeds.
- Fields that intentionally vary across configs are seed, split file, save directory, and session direction.

## Method-level summary

| Method | Model | Loss | Eval embedding | SupCon lambda | ArcFace | Epochs | LR | WD | Sampler | AMP | Verdict |
|---|---|---|---|---:|---|---:|---:|---:|---|---|---|
| B0 ResNet18 + CE | ResNet18Baseline | ce | pre-BN/default | 0.0 | - | 60 | 0.0001 | 0.0001 | 8x2 | True | PASS |
| B1 ResNet18 + CE + SupCon | ResNet18Baseline | ce+supcon | pre-BN/default | 0.1 | - | 60 | 0.0001 | 0.0001 | 8x2 | True | PASS |
| B4 ResNet18 + ArcFace | ResNet18Baseline | arcface | pre-BN/default | 0.0 | s=30.0, m=0.5 | 60 | 0.0001 | 0.0001 | 8x2 | True | PASS |
| B8 ResNet18 + CosFace | ResNet18Baseline | cosface | pre-BN/default | 0.0 | s=30.0, m=0.35 | 60 | 0.0001 | 0.0001 | 8x2 | True | PASS |
| B5 ResNet18 + BNNeck + CE | ResNet18BNNeck | ce | post-BN | 0.0 | - | 60 | 0.0001 | 0.0001 | 8x2 | True | PASS |
| B6 ResNet18 + BNNeck + ArcFace | ResNet18BNNeck | arcface | post-BN | 0.0 | s=30.0, m=0.5 | 60 | 0.0001 | 0.0001 | 8x2 | True | PASS |
| B7 ResNet18 + BNNeck + ArcFace + light SupCon | ResNet18BNNeck | arcface | post-BN | 0.02 | s=30.0, m=0.5 | 60 | 0.0001 | 0.0001 | 8x2 | True | PASS |

## Reviewer-facing notes

- All final strict Tongji methods use 60 epochs, learning rate 1e-4, weight decay 1e-4, AMP enabled, and gradient accumulation of four steps.
- B1 uses supervised contrastive regularization with lambda 0.1 and temperature 0.07.
- B5 isolates BNNeck with cross-entropy by using BNNeck/post-BN evaluation and lambda_supcon 0.0.
- B6 isolates BNNeck+ArcFace by using BNNeck/post-BN evaluation, ArcFace scale 30.0, margin 0.5, and lambda_supcon 0.0.
- B7 adds a light supervised contrastive term to BNNeck+ArcFace with lambda_supcon 0.02.
- Config filenames retain historical `subject_disjoint` naming, but the paper claim remains palm-class-disjoint according to the identity/parser and gallery/probe audits.
