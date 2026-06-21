# Config and Experiment Audit

## Required config files

Check existence and content for:

```text
configs/b1_resnet18_ce_supcon_tongji_s1s2_lr1e4.yaml
configs/b1_resnet18_ce_supcon_tongji_s2s1_lr1e4.yaml
configs/b2_fixed_gabor_resnet18_tongji_s1s2_lr1e4.yaml
configs/b2_fixed_gabor_resnet18_tongji_s2s1_lr1e4.yaml
configs/b1_resnet18_ce_supcon_iitd_within_lr1e4.yaml
configs/b2_fixed_gabor_resnet18_iitd_within_lr1e4.yaml
configs/m1_lgfnet_full_tongji_s1s2_lr1e4.yaml
configs/b3_lgfnet_no_gabor_tongji_s1s2_lr1e4.yaml
```

## Required B1 Tongji S1->S2 config values

```yaml
save_dir: experiments/b1_resnet18_ce_supcon_tongji_s1s2_lr1e4
dataset:
  split_file: data/splits/tongji_s1_to_s2.json
model:
  name: ResNet18Baseline
  embedding_dim: 256
  pretrained: true
training:
  epochs: 60
  lr: 0.0001
  weight_decay: 0.0001
  grad_accumulation_steps: 4
  lambda_supcon: 0.10
  temperature: 0.07
  amp: true
```

## Required B1 Tongji S2->S1 config values

```yaml
save_dir: experiments/b1_resnet18_ce_supcon_tongji_s2s1_lr1e4
dataset:
  split_file: data/splits/tongji_s2_to_s1.json
model:
  name: ResNet18Baseline
  embedding_dim: 256
  pretrained: true
training:
  epochs: 60
  lr: 0.0001
  weight_decay: 0.0001
  grad_accumulation_steps: 4
  lambda_supcon: 0.10
  temperature: 0.07
  amp: true
```

## Required B2 config values

For Tongji B2 configs:

```yaml
model:
  name: FixedGaborResNet18
  embedding_dim: 256
training:
  epochs: 60
  lr: 0.0001
  lambda_supcon: 0.10
```

S1->S2 split must be:

```text
data/splits/tongji_s1_to_s2.json
```

S2->S1 split must be:

```text
data/splits/tongji_s2_to_s1.json
```

## Required result files

Check existence:

```text
docs/results/tongji_s1s2_summary.md

docs/results/b1_resnet18_ce_supcon_tongji_s1s2_lr1e4_metrics.md
docs/results/b1_resnet18_ce_supcon_tongji_s1s2_lr1e4_metrics.json
docs/results/b1_resnet18_ce_supcon_tongji_s2s1_lr1e4_metrics.md
docs/results/b1_resnet18_ce_supcon_tongji_s2s1_lr1e4_metrics.json

docs/results/b2_fixed_gabor_resnet18_tongji_s1s2_lr1e4_metrics.md
docs/results/b2_fixed_gabor_resnet18_tongji_s1s2_lr1e4_metrics.json
docs/results/b2_fixed_gabor_resnet18_tongji_s2s1_lr1e4_metrics.md
docs/results/b2_fixed_gabor_resnet18_tongji_s2s1_lr1e4_metrics.json

docs/results/b2_fixed_gabor_resnet18_iitd_within_lr1e4_metrics.md
docs/results/b2_fixed_gabor_resnet18_iitd_within_lr1e4_metrics.json
```

If B1 IITD metrics are referenced in summary but no `docs/results/b1_resnet18_ce_supcon_iitd_within_lr1e4_metrics.*` exists, mark this as a documentation gap unless metrics are available elsewhere.

## Consistency checks

The AGENT must verify:

1. `save_dir` matches experiment naming.
2. split file matches direction.
3. model name matches method label.
4. `epochs`, `lr`, `lambda_supcon`, `embedding_dim` match the summary claims.
5. no stale conclusion remains in summary, such as “M1 significantly outperforms B1” after fair B1 rerun.
6. no generic `docs/results/metrics.md` or `docs/results/metrics.json` is committed.
