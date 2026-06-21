# Rank-B Core Run Matrix

This document contains the complete experiment matrix, configuration files, and exact command lines to train and evaluate the core baseline models (B1 and B6) for the PALM_CGK_BASE upgrade.

## Scope Lock & Protocol Rules
* **Tongji (Primary)**: Evaluated using the **development/test subject-disjoint cross-session protocol**.
* **IITD (Secondary)**: Evaluated using the **secondary subject-disjoint within-dataset validation** (no cross-session claims).
* **Git/Training Safety**: No training was executed during this configuration stage. All checkpoints, raw images, and temporary experiment outputs are strictly excluded from git staging.

## Protocol Audit Verdict
All split configurations audited below are verified to be strictly subject-disjoint between development (train ∪ val) and test (gallery ∪ probe ∪ support) subsets.
* **Audit Report**: [rank_b_final_split_verdict.md](file:///d:/0.Research/PALM_CGK_BASE/PALM_CGK_BASE/docs/results/rank_b_final_split_verdict.md)

---

## 1. Primary Dataset: Tongji (12 Configs)

### B1: ResNet18 + CE + SupCon
* **Recipe**: `ResNet18Baseline`, `lambda_supcon = 0.10`, `temperature = 0.07`, `lr = 1e-4`, `epochs = 60`, `grad_accumulation = 4`, `amp = true`.

| Config File | Seed | Split / Direction | Train Command | Eval Command |
| :--- | :--- | :--- | :--- | :--- |
| `configs/b1_resnet18_ce_supcon_tongji_subject_disjoint_s1s2_seed42.yaml` | 42 | S1 -> S2 | `python scripts/train_lgf.py --config configs/b1_resnet18_ce_supcon_tongji_subject_disjoint_s1s2_seed42.yaml` | `python scripts/eval_embedding.py --checkpoint experiments/b1_resnet18_ce_supcon_tongji_subject_disjoint_s1s2_seed42/checkpoints/best.pt --config configs/b1_resnet18_ce_supcon_tongji_subject_disjoint_s1s2_seed42.yaml` |
| `configs/b1_resnet18_ce_supcon_tongji_subject_disjoint_s1s2_seed2026.yaml` | 2026 | S1 -> S2 | `python scripts/train_lgf.py --config configs/b1_resnet18_ce_supcon_tongji_subject_disjoint_s1s2_seed2026.yaml` | `python scripts/eval_embedding.py --checkpoint experiments/b1_resnet18_ce_supcon_tongji_subject_disjoint_s1s2_seed2026/checkpoints/best.pt --config configs/b1_resnet18_ce_supcon_tongji_subject_disjoint_s1s2_seed2026.yaml` |
| `configs/b1_resnet18_ce_supcon_tongji_subject_disjoint_s1s2_seed2705.yaml` | 2705 | S1 -> S2 | `python scripts/train_lgf.py --config configs/b1_resnet18_ce_supcon_tongji_subject_disjoint_s1s2_seed2705.yaml` | `python scripts/eval_embedding.py --checkpoint experiments/b1_resnet18_ce_supcon_tongji_subject_disjoint_s1s2_seed2705/checkpoints/best.pt --config configs/b1_resnet18_ce_supcon_tongji_subject_disjoint_s1s2_seed2705.yaml` |
| `configs/b1_resnet18_ce_supcon_tongji_subject_disjoint_s2s1_seed42.yaml` | 42 | S2 -> S1 | `python scripts/train_lgf.py --config configs/b1_resnet18_ce_supcon_tongji_subject_disjoint_s2s1_seed42.yaml` | `python scripts/eval_embedding.py --checkpoint experiments/b1_resnet18_ce_supcon_tongji_subject_disjoint_s2s1_seed42/checkpoints/best.pt --config configs/b1_resnet18_ce_supcon_tongji_subject_disjoint_s2s1_seed42.yaml` |
| `configs/b1_resnet18_ce_supcon_tongji_subject_disjoint_s2s1_seed2026.yaml` | 2026 | S2 -> S1 | `python scripts/train_lgf.py --config configs/b1_resnet18_ce_supcon_tongji_subject_disjoint_s2s1_seed2026.yaml` | `python scripts/eval_embedding.py --checkpoint experiments/b1_resnet18_ce_supcon_tongji_subject_disjoint_s2s1_seed2026/checkpoints/best.pt --config configs/b1_resnet18_ce_supcon_tongji_subject_disjoint_s2s1_seed2026.yaml` |
| `configs/b1_resnet18_ce_supcon_tongji_subject_disjoint_s2s1_seed2705.yaml` | 2705 | S2 -> S1 | `python scripts/train_lgf.py --config configs/b1_resnet18_ce_supcon_tongji_subject_disjoint_s2s1_seed2705.yaml` | `python scripts/eval_embedding.py --checkpoint experiments/b1_resnet18_ce_supcon_tongji_subject_disjoint_s2s1_seed2705/checkpoints/best.pt --config configs/b1_resnet18_ce_supcon_tongji_subject_disjoint_s2s1_seed2705.yaml` |

### B6: ResNet18 + BNNeck + ArcFace
* **Recipe**: `ResNet18BNNeck`, ArcFace `scale = 30.0`, `margin = 0.5`, `lambda_supcon = 0.0`, `eval_embedding = post_bn`, `lr = 1e-4`, `epochs = 60`, `grad_accumulation = 4`, `amp = true`.

| Config File | Seed | Split / Direction | Train Command | Eval Command |
| :--- | :--- | :--- | :--- | :--- |
| `configs/b6_resnet18_bnneck_arcface_tongji_subject_disjoint_s1s2_seed42.yaml` | 42 | S1 -> S2 | `python scripts/train_lgf.py --config configs/b6_resnet18_bnneck_arcface_tongji_subject_disjoint_s1s2_seed42.yaml` | `python scripts/eval_embedding.py --checkpoint experiments/b6_resnet18_bnneck_arcface_tongji_subject_disjoint_s1s2_seed42/checkpoints/best.pt --config configs/b6_resnet18_bnneck_arcface_tongji_subject_disjoint_s1s2_seed42.yaml` |
| `configs/b6_resnet18_bnneck_arcface_tongji_subject_disjoint_s1s2_seed2026.yaml` | 2026 | S1 -> S2 | `python scripts/train_lgf.py --config configs/b6_resnet18_bnneck_arcface_tongji_subject_disjoint_s1s2_seed2026.yaml` | `python scripts/eval_embedding.py --checkpoint experiments/b6_resnet18_bnneck_arcface_tongji_subject_disjoint_s1s2_seed2026/checkpoints/best.pt --config configs/b6_resnet18_bnneck_arcface_tongji_subject_disjoint_s1s2_seed2026.yaml` |
| `configs/b6_resnet18_bnneck_arcface_tongji_subject_disjoint_s1s2_seed2705.yaml` | 2705 | S1 -> S2 | `python scripts/train_lgf.py --config configs/b6_resnet18_bnneck_arcface_tongji_subject_disjoint_s1s2_seed2705.yaml` | `python scripts/eval_embedding.py --checkpoint experiments/b6_resnet18_bnneck_arcface_tongji_subject_disjoint_s1s2_seed2705/checkpoints/best.pt --config configs/b6_resnet18_bnneck_arcface_tongji_subject_disjoint_s1s2_seed2705.yaml` |
| `configs/b6_resnet18_bnneck_arcface_tongji_subject_disjoint_s2s1_seed42.yaml` | 42 | S2 -> S1 | `python scripts/train_lgf.py --config configs/b6_resnet18_bnneck_arcface_tongji_subject_disjoint_s2s1_seed42.yaml` | `python scripts/eval_embedding.py --checkpoint experiments/b6_resnet18_bnneck_arcface_tongji_subject_disjoint_s2s1_seed42/checkpoints/best.pt --config configs/b6_resnet18_bnneck_arcface_tongji_subject_disjoint_s2s1_seed42.yaml` |
| `configs/b6_resnet18_bnneck_arcface_tongji_subject_disjoint_s2s1_seed2026.yaml` | 2026 | S2 -> S1 | `python scripts/train_lgf.py --config configs/b6_resnet18_bnneck_arcface_tongji_subject_disjoint_s2s1_seed2026.yaml` | `python scripts/eval_embedding.py --checkpoint experiments/b6_resnet18_bnneck_arcface_tongji_subject_disjoint_s2s1_seed2026/checkpoints/best.pt --config configs/b6_resnet18_bnneck_arcface_tongji_subject_disjoint_s2s1_seed2026.yaml` |
| `configs/b6_resnet18_bnneck_arcface_tongji_subject_disjoint_s2s1_seed2705.yaml` | 2705 | S2 -> S1 | `python scripts/train_lgf.py --config configs/b6_resnet18_bnneck_arcface_tongji_subject_disjoint_s2s1_seed2705.yaml` | `python scripts/eval_embedding.py --checkpoint experiments/b6_resnet18_bnneck_arcface_tongji_subject_disjoint_s2s1_seed2705/checkpoints/best.pt --config configs/b6_resnet18_bnneck_arcface_tongji_subject_disjoint_s2s1_seed2705.yaml` |

---

## 2. Secondary Dataset: IITD (6 Configs)

### B1: ResNet18 + CE + SupCon
* **Recipe**: `ResNet18Baseline`, `lambda_supcon = 0.10`, `temperature = 0.07`, `lr = 1e-4`, `epochs = 60`, `grad_accumulation = 4`, `amp = true`.

| Config File | Seed | Split / Direction | Train Command | Eval Command |
| :--- | :--- | :--- | :--- | :--- |
| `configs/b1_resnet18_ce_supcon_iitd_subject_disjoint_within_seed42.yaml` | 42 | Within-dataset | `python scripts/train_lgf.py --config configs/b1_resnet18_ce_supcon_iitd_subject_disjoint_within_seed42.yaml` | `python scripts/eval_embedding.py --checkpoint experiments/b1_resnet18_ce_supcon_iitd_subject_disjoint_within_seed42/checkpoints/best.pt --config configs/b1_resnet18_ce_supcon_iitd_subject_disjoint_within_seed42.yaml` |
| `configs/b1_resnet18_ce_supcon_iitd_subject_disjoint_within_seed2026.yaml` | 2026 | Within-dataset | `python scripts/train_lgf.py --config configs/b1_resnet18_ce_supcon_iitd_subject_disjoint_within_seed2026.yaml` | `python scripts/eval_embedding.py --checkpoint experiments/b1_resnet18_ce_supcon_iitd_subject_disjoint_within_seed2026/checkpoints/best.pt --config configs/b1_resnet18_ce_supcon_iitd_subject_disjoint_within_seed2026.yaml` |
| `configs/b1_resnet18_ce_supcon_iitd_subject_disjoint_within_seed2705.yaml` | 2705 | Within-dataset | `python scripts/train_lgf.py --config configs/b1_resnet18_ce_supcon_iitd_subject_disjoint_within_seed2705.yaml` | `python scripts/eval_embedding.py --checkpoint experiments/b1_resnet18_ce_supcon_iitd_subject_disjoint_within_seed2705/checkpoints/best.pt --config configs/b1_resnet18_ce_supcon_iitd_subject_disjoint_within_seed2705.yaml` |

### B6: ResNet18 + BNNeck + ArcFace
* **Recipe**: `ResNet18BNNeck`, ArcFace `scale = 30.0`, `margin = 0.5`, `lambda_supcon = 0.0`, `eval_embedding = post_bn`, `lr = 1e-4`, `epochs = 60`, `grad_accumulation = 4`, `amp = true`.

| Config File | Seed | Split / Direction | Train Command | Eval Command |
| :--- | :--- | :--- | :--- | :--- |
| `configs/b6_resnet18_bnneck_arcface_iitd_subject_disjoint_within_seed42.yaml` | 42 | Within-dataset | `python scripts/train_lgf.py --config configs/b6_resnet18_bnneck_arcface_iitd_subject_disjoint_within_seed42.yaml` | `python scripts/eval_embedding.py --checkpoint experiments/b6_resnet18_bnneck_arcface_iitd_subject_disjoint_within_seed42/checkpoints/best.pt --config configs/b6_resnet18_bnneck_arcface_iitd_subject_disjoint_within_seed42.yaml` |
| `configs/b6_resnet18_bnneck_arcface_iitd_subject_disjoint_within_seed2026.yaml` | 2026 | Within-dataset | `python scripts/train_lgf.py --config configs/b6_resnet18_bnneck_arcface_iitd_subject_disjoint_within_seed2026.yaml` | `python scripts/eval_embedding.py --checkpoint experiments/b6_resnet18_bnneck_arcface_iitd_subject_disjoint_within_seed2026/checkpoints/best.pt --config configs/b6_resnet18_bnneck_arcface_iitd_subject_disjoint_within_seed2026.yaml` |
| `configs/b6_resnet18_bnneck_arcface_iitd_subject_disjoint_within_seed2705.yaml` | 2705 | Within-dataset | `python scripts/train_lgf.py --config configs/b6_resnet18_bnneck_arcface_iitd_subject_disjoint_within_seed2705.yaml` | `python scripts/eval_embedding.py --checkpoint experiments/b6_resnet18_bnneck_arcface_iitd_subject_disjoint_within_seed2705/checkpoints/best.pt --config configs/b6_resnet18_bnneck_arcface_iitd_subject_disjoint_within_seed2705.yaml` |
