# run_rankb_smoke_tests.ps1
# Smoke test to verify loading and evaluating a model checkpoint using the correct config in PowerShell.

$ErrorActionPreference = "Stop"

Write-Host "=== Running Tongji Smoke Test (M0 - ResNet18 + CE, S1->S2, Seed 42) ==="
python scripts/eval_embedding.py `
  --checkpoint experiments/b0_resnet18_ce_tongji_subject_disjoint_s1s2_seed42/checkpoints/best.pt `
  --config configs/rankb_final/m0_resnet18_ce_tongji_s1s2_seed42.yaml `
  --output_dir experiments/b0_resnet18_ce_tongji_subject_disjoint_s1s2_seed42/smoke_test_eval

Write-Host "=== Running IITD Smoke Test (M1 - ResNet18 + CE + SupCon, Within, Seed 42) ==="
python scripts/eval_embedding.py `
  --checkpoint experiments/b1_resnet18_ce_supcon_iitd_subject_disjoint_within_seed42/checkpoints/best.pt `
  --config configs/rankb_final/m1_resnet18_ce_supcon_iitd_within_seed42.yaml `
  --output_dir experiments/b1_resnet18_ce_supcon_iitd_subject_disjoint_within_seed42/smoke_test_eval

Write-Host "=== Smoke Tests Completed Successfully ==="
