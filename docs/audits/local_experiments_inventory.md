# Local Experiments Inventory

This document lists the local experimental outputs present in the `experiments/` directory.

> [!WARNING]
> The `experiments/` directory serves as a local results store (containing checkpoints, embeddings, and raw evaluation files). These files are large, local-only artifacts and **MUST NOT** be committed to Git. They are explicitly excluded in `.gitignore`.

## Top-Level Directories in `experiments/`

As of the pre-cleanup audit, the following experimental directories are present:

- `b0_resnet18_ce_tongji_s1s2`
- `b1_resnet18_ce_supcon_iitd_subject_disjoint_within_seed2026`
- `b1_resnet18_ce_supcon_iitd_subject_disjoint_within_seed2705`
- `b1_resnet18_ce_supcon_iitd_subject_disjoint_within_seed42`
- `b1_resnet18_ce_supcon_iitd_within_lr1e4`
- `b1_resnet18_ce_supcon_tongji_s1s2`
- `b1_resnet18_ce_supcon_tongji_s1s2_lr1e4`
- `b1_resnet18_ce_supcon_tongji_s1s2_lr1e4_seed2026`
- `b1_resnet18_ce_supcon_tongji_s1s2_lr1e4_seed2705`
- `b1_resnet18_ce_supcon_tongji_s2s1_lr1e4`
- `b1_resnet18_ce_supcon_tongji_s2s1_lr1e4_seed2026`
- `b1_resnet18_ce_supcon_tongji_s2s1_lr1e4_seed2705`
- `b1_resnet18_ce_supcon_tongji_subject_disjoint_s1s2_seed2026`
- `b1_resnet18_ce_supcon_tongji_subject_disjoint_s1s2_seed2705`
- `b1_resnet18_ce_supcon_tongji_subject_disjoint_s1s2_seed42`
- `b1_resnet18_ce_supcon_tongji_subject_disjoint_s2s1_seed2026`
- `b1_resnet18_ce_supcon_tongji_subject_disjoint_s2s1_seed2705`
- `b1_resnet18_ce_supcon_tongji_subject_disjoint_s2s1_seed42`
- `b2_fixed_gabor_resnet18_iitd_within_lr1e4`
- `b2_fixed_gabor_resnet18_tongji_s1s2`
- `b2_fixed_gabor_resnet18_tongji_s1s2_lr1e4`
- `b2_fixed_gabor_resnet18_tongji_s1s2_lr1e4_seed2026`
- `b2_fixed_gabor_resnet18_tongji_s1s2_lr1e4_seed2705`
- `b2_fixed_gabor_resnet18_tongji_s2s1_lr1e4`
- `b2_fixed_gabor_resnet18_tongji_s2s1_lr1e4_seed2026`
- `b2_fixed_gabor_resnet18_tongji_s2s1_lr1e4_seed2705`
- `b3_lgfnet_no_gabor_tongji_s1s2`
- `b3_lgfnet_no_gabor_tongji_s1s2_lr1e4`
- `b4_resnet18_arcface_tongji_s1s2_lr1e4_seed42`
- `b4_resnet18_arcface_tongji_s2s1_lr1e4_seed42`
- `b6_resnet18_bnneck_arcface_iitd_subject_disjoint_within_seed2026`
- `b6_resnet18_bnneck_arcface_iitd_subject_disjoint_within_seed2705`
- `b6_resnet18_bnneck_arcface_iitd_subject_disjoint_within_seed42`
- `b6_resnet18_bnneck_arcface_iitd_within_lr1e4_seed42`
- `b6_resnet18_bnneck_arcface_tongji_s1s2_lr1e4_seed2026`
- `b6_resnet18_bnneck_arcface_tongji_s1s2_lr1e4_seed2705`
- `b6_resnet18_bnneck_arcface_tongji_s1s2_lr1e4_seed42`
- `b6_resnet18_bnneck_arcface_tongji_s2s1_lr1e4_seed2026`
- `b6_resnet18_bnneck_arcface_tongji_s2s1_lr1e4_seed2705`
- `b6_resnet18_bnneck_arcface_tongji_s2s1_lr1e4_seed42`
- `b6_resnet18_bnneck_arcface_tongji_subject_disjoint_s1s2_seed2026`
- `b6_resnet18_bnneck_arcface_tongji_subject_disjoint_s1s2_seed2705`
- `b6_resnet18_bnneck_arcface_tongji_subject_disjoint_s1s2_seed42`
- `b6_resnet18_bnneck_arcface_tongji_subject_disjoint_s2s1_seed2026`
- `b6_resnet18_bnneck_arcface_tongji_subject_disjoint_s2s1_seed2705`
- `b6_resnet18_bnneck_arcface_tongji_subject_disjoint_s2s1_seed42`
- `b7_resnet18_bnneck_arcface_supcon_tongji_s1s2_lr1e4_seed42`
- `b7_resnet18_bnneck_arcface_supcon_tongji_s2s1_lr1e4_seed42`
- `debug_m1_lgfnet_full_p8k2_lr1e4`
- `debug_m1_lgfnet_full_tongji_s1s2`
- `debug_resnet18_ce_tongji_s1s2`
- `m1_lgfnet_full_tongji_s1s2`
- `m1_lgfnet_full_tongji_s1s2_lr1e4`
- `resnet18_ce_tongji_s1s2`

## Top-Level Files in `experiments/`
- `reproduce_table2_casia_accuracy.py`
- `reproduce_table3_time_complexity.py`
- `reproduce_table4_two_stage_vs_one_stage.py`
- `reproduce_table5_feature_comparison.py`
- `reproduce_table6_kernel_comparison.py`
