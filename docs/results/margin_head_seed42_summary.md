# Margin Head Seed42 Summary

Decision: `GO`

Best method: `B6`

GO threshold versus B1 seed42 bidirectional average: Rank-1 >= +0.5 pp, TAR@FAR=1e-3 >= +1.0 pp, or EER <= -0.2 pp.

| Method | Decision | Rank-1 | EER | TAR@FAR=1e-3 | Delta Rank-1 | Delta EER | Delta TAR@1e-3 |
|---|---|---:|---:|---:|---:|---:|---:|
| B1 | baseline | 93.39 | 2.30 | 89.75 | - | - | - |
| B4 | GO | 94.35 | 2.03 | 91.86 | +0.96 | -0.28 | +2.11 |
| B6 | GO | 96.80 | 1.14 | 96.53 | +3.41 | -1.16 | +6.78 |
| B7 | GO | 96.97 | 1.13 | 96.50 | +3.57 | -1.17 | +6.74 |

## Generated Multi-Seed Configs

- `configs\b6_resnet18_bnneck_arcface_tongji_s1s2_lr1e4_seed2026.yaml`
- `configs\b6_resnet18_bnneck_arcface_tongji_s1s2_lr1e4_seed2705.yaml`
- `configs\b6_resnet18_bnneck_arcface_tongji_s2s1_lr1e4_seed2026.yaml`
- `configs\b6_resnet18_bnneck_arcface_tongji_s2s1_lr1e4_seed2705.yaml`

## Multi-Seed Command Template

```bat
python scripts/train_lgf.py --config configs\b6_resnet18_bnneck_arcface_tongji_s1s2_lr1e4_seed2026.yaml
python scripts/eval_embedding.py --checkpoint experiments/b6_resnet18_bnneck_arcface_tongji_s1s2_lr1e4_seed2026/checkpoints/best.pt --config configs\b6_resnet18_bnneck_arcface_tongji_s1s2_lr1e4_seed2026.yaml
python scripts/train_lgf.py --config configs\b6_resnet18_bnneck_arcface_tongji_s1s2_lr1e4_seed2705.yaml
python scripts/eval_embedding.py --checkpoint experiments/b6_resnet18_bnneck_arcface_tongji_s1s2_lr1e4_seed2705/checkpoints/best.pt --config configs\b6_resnet18_bnneck_arcface_tongji_s1s2_lr1e4_seed2705.yaml
python scripts/train_lgf.py --config configs\b6_resnet18_bnneck_arcface_tongji_s2s1_lr1e4_seed2026.yaml
python scripts/eval_embedding.py --checkpoint experiments/b6_resnet18_bnneck_arcface_tongji_s2s1_lr1e4_seed2026/checkpoints/best.pt --config configs\b6_resnet18_bnneck_arcface_tongji_s2s1_lr1e4_seed2026.yaml
python scripts/train_lgf.py --config configs\b6_resnet18_bnneck_arcface_tongji_s2s1_lr1e4_seed2705.yaml
python scripts/eval_embedding.py --checkpoint experiments/b6_resnet18_bnneck_arcface_tongji_s2s1_lr1e4_seed2705/checkpoints/best.pt --config configs\b6_resnet18_bnneck_arcface_tongji_s2s1_lr1e4_seed2705.yaml
```

Full multi-seed is intentionally not run by this script after seed42; run the commands above only after reviewing the seed42 summary.
