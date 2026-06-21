# PALM_CGK_BASE Final Integrity Audit

## 1. Executive Verdict

Overall status: `PASS WITH WARNINGS`

Paper claim status: `PARTIALLY SUPPORTED`

### Conclusion
The codebase is technically consistent, correct, and matches the configuration templates. Pytest suite passes successfully (45 tests passed), and there are no data leakage or split issues. However, the original research claim that "learnable Gabor fusion improves palmprint recognition" is **not supported** by the experimental results. The full model $M1$ (LGFNetSmall) is significantly outperformed by the baseline $B1$ (ResNet18 + CE + SupCon) and the ablation $B3$ (CNN + DeiT, no Gabor) on the Tongji S1 -> S2 cross-session dataset. Conversely, the alternative claim that "a fixed Gabor prior combined with supervised contrastive metric learning improves strict-FAR cross-session palmprint verification robustness on Tongji" is **fully supported** by the results ($B2$ improves average TAR@FAR=1e-3 by +2.10 percentage points over $B1$). A few documentation gaps exist where experiment metrics were not copied to the results folder, which must be fixed before writing the paper.

---

## 2. Audit Environment

| Item | Value | Evidence |
|---|---|---|
| Working directory | `d:\0.Research\PALM_CGK_BASE\PALM_CGK_BASE` | Checked |
| Git HEAD | `9d3633369b05f300e85348d4a444bd32e35c201b` | `git rev-parse HEAD` |
| Branch status | Up to date with `origin/main`, clean tree | `git status` |
| Python/Conda env | `palm_lgf` | Configured environment |
| Pytest result | 45 passed | `pytest -q` command output |

---

## 3. PASS/FAIL Summary

| Area | Status | Evidence | Required fix |
|---|---|---|---|
| Git hygiene | PASS | `git status` is clean with only untracked audit specs. | None |
| No checkpoints in Git | PASS | `git ls-tree` shows zero committed `.pt`, `.pth`, `.ckpt`, or `.onnx` files. | None |
| Dataset manifest | PASS | `palm_segmented_manifest.csv` verified with exactly 14,601 rows. | None |
| Split integrity | PASS | `verify_splits.py` shows correct session directions and zero missing paths. | None |
| Config consistency | PASS | All 8 config files match their respective save directories and model recipes. | None |
| Model registry | PASS | `palmrec/models/__init__.py` successfully registers and builds all 4 architectures. | None |
| Train/eval scripts | PASS | Scripts build models from configs, run AMP/accumulation, and report standard metrics. | None |
| Metrics consistency | PASS WITH WARNINGS | Saved JSON and MD metrics match the summary, but two metric files are missing in `docs/results/`. | Copy metrics for `b1_iitd` and `m1` from `experiments/` to `docs/results/`. |
| Summary correctness | PASS WITH WARNINGS | `tongji_s1s2_summary.md` is correct but retains outdated conclusions about $M1$. | Update the summary text to explicitly deprecate the learnable Gabor claim. |
| Paper claim | PASS WITH WARNINGS | Original learnable claim is rejected; alternative fixed Gabor claim is supported. | Restructure the paper's scope to focus on fixed Gabor priors. |

---

## 4. Dataset and Split Audit

### Manifest Counts
- **Total rows**: 14,601 in `data/metadata/palm_segmented_manifest.csv`.
- **IITD dataset**: 2,601 images (Left: 1,301, Right: 1,300), image size 150x150, 460 classes/palms.
- **Tongji dataset**: 12,000 images (Session 1: 6,000, Session 2: 6,000), image size 128x128, 600 classes/palms.

### Split Integrity Results
1. **`tongji_s1_to_s2.json`**:
   - **Train**: 4,800 images (Session 1)
   - **Val**: 1,200 images (Session 1)
   - **Gallery**: 6,000 images (Session 1)
   - **Probe**: 6,000 images (Session 2)
   - **Support**: 0 images
   - *Status*: PASS (Perfect session separation, zero missing manifest paths, 600 classes).
2. **`tongji_s2_to_s1.json`**:
   - **Train**: 4,800 images (Session 2)
   - **Val**: 1,200 images (Session 2)
   - **Gallery**: 6,000 images (Session 2)
   - **Probe**: 6,000 images (Session 1)
   - **Support**: 0 images
   - *Status*: PASS (Perfect session separation, zero missing manifest paths, 600 classes).
3. **`iitd_within.json`**:
   - **Train**: 1,681 images (Left: 841, Right: 840)
   - **Val**: 460 images (Left: 230, Right: 230)
   - **Gallery**: 1,681 images (Left: 841, Right: 840)
   - **Probe**: 460 images (Left: 230, Right: 230)
   - **Support**: 0 images
   - *Status*: PASS (Gallery-probe matched, zero missing manifest paths, 460 classes).
4. **`cross_dataset_fewshot.json`**:
   - **Train/Val**: 4,800/1,200 images (Tongji Session 1)
   - **Gallery/Probe/Support**: 920/1,681/920 images (IITD Session 1)
   - *Status*: PASS (Zero missing manifest paths).

---

## 5. Config and Experiment Audit

The 8 required configurations were audited against their respective experiment outputs:

| Experiment | Config | Split | Model | Key training recipe | Status |
|---|---|---|---|---|---|
| `b1_resnet18_ce_supcon_tongji_s1s2_lr1e4` | `configs/b1_resnet18_ce_supcon_tongji_s1s2_lr1e4.yaml` | `tongji_s1_to_s2.json` | `ResNet18Baseline` | lr=1e-4, epochs=60, $\lambda_{supcon}=0.1$, amp=true | PASS |
| `b1_resnet18_ce_supcon_tongji_s2s1_lr1e4` | `configs/b1_resnet18_ce_supcon_tongji_s2s1_lr1e4.yaml` | `tongji_s2_to_s1.json` | `ResNet18Baseline` | lr=1e-4, epochs=60, $\lambda_{supcon}=0.1$, amp=true | PASS |
| `b2_fixed_gabor_resnet18_tongji_s1s2_lr1e4` | `configs/b2_fixed_gabor_resnet18_tongji_s1s2_lr1e4.yaml` | `tongji_s1_to_s2.json` | `FixedGaborResNet18` | lr=1e-4, epochs=60, $\lambda_{supcon}=0.1$, amp=true | PASS |
| `b2_fixed_gabor_resnet18_tongji_s2s1_lr1e4` | `configs/b2_fixed_gabor_resnet18_tongji_s2s1_lr1e4.yaml` | `tongji_s2_to_s1.json` | `FixedGaborResNet18` | lr=1e-4, epochs=60, $\lambda_{supcon}=0.1$, amp=true | PASS |
| `b1_resnet18_ce_supcon_iitd_within_lr1e4` | `configs/b1_resnet18_ce_supcon_iitd_within_lr1e4.yaml` | `iitd_within.json` | `ResNet18Baseline` | lr=1e-4, epochs=60, $\lambda_{supcon}=0.1$, amp=true | PASS |
| `b2_fixed_gabor_resnet18_iitd_within_lr1e4` | `configs/b2_fixed_gabor_resnet18_iitd_within_lr1e4.yaml` | `iitd_within.json` | `FixedGaborResNet18` | lr=1e-4, epochs=60, $\lambda_{supcon}=0.1$, amp=true | PASS |
| `m1_lgfnet_full_tongji_s1s2_lr1e4` | `configs/m1_lgfnet_full_tongji_s1s2_lr1e4.yaml` | `tongji_s1_to_s2.json` | `LGFNetSmall` | lr=1e-4, epochs=60, $\lambda_{supcon}=0.1$, amp=true | PASS |
| `b3_lgfnet_no_gabor_tongji_s1s2_lr1e4` | `configs/b3_lgfnet_no_gabor_tongji_s1s2_lr1e4.yaml` | `tongji_s1_to_s2.json` | `LGFNetNoGabor` | lr=1e-4, epochs=60, $\lambda_{supcon}=0.1$, amp=true | PASS |

- **Consistency Check**: All `save_dir` configurations map exactly to the directory names, model names correspond to config variables, and hyperparameters match the reported settings.
- **Documentation Gap**: Metrics for `b1_resnet18_ce_supcon_iitd_within_lr1e4` and `m1_lgfnet_full_tongji_s1s2_lr1e4` are saved under `experiments/` but are missing from `docs/results/`.

---

## 6. Code Audit

- **Model Registry (`palmrec/models/__init__.py`)**: Implements `build_model(name, num_classes, embedding_dim, pretrained)` which dynamically returns the correct class. No hardcoded configuration values were found.
- **`ResNet18Baseline`**: Extends standard ResNet18. The fc layer is replaced with `nn.Identity`, followed by a projection to embedding dimension (256-D), an L2-normalization step (`F.normalize`), and a classifier head. Matches target intent.
- **`FixedGaborResNet18`**: Integrates a `LearnableGaborStem` with `fixed=True`. The Gabor branch output (16-D after pooling) is concatenated with the CNN backbone output (512-D), giving a 528-D vector. A `GatedFusionModule` projects this to the final 256-D normalized embedding.
- **`LGFNetSmall`**: Uses `LearnableGaborStem` with `fixed=False` (learnable). It features a CNN branch (ResNet18, 512-D), a Transformer branch (DeiT-Tiny, 192-D), and the Gabor branch (16-D). Gated Fusion fuses the concatenated 720-D representation to 256-D.
- **`LGFNetNoGabor`**: Similar to `LGFNetSmall` but omits the Gabor branch (concatenates CNN and DeiT to 704-D, fused to 256-D).
- **`train_lgf.py`**: Properly reads config yaml, initializes `CombinedLoss` (CE + SupCon) with temperature and $\lambda_{supcon}$ weight, incorporates mixed-precision training (`torch.cuda.amp.autocast`), gradient accumulation steps, and saves `best.pt`/`last.pt` under checkpoints.
- **`eval_embedding.py`**: Correctly loads config and checkpoint, extracts normalized embeddings, computes cosine similarity, applies self-match masking to ensure zero leakage, and calculates standard metrics (Rank-1, Rank-5, Macro-F1, EER, and TAR@FAR=1e-2/1e-3) alongside FLOPs (via `fvcore`/`thop`) and average inference time (batch size 1).

---

## 7. Metrics Verification

The tables below contrast the ground-truth JSON files with the values in the summary file `tongji_s1s2_summary.md`.

### 7.1. Tongji S1 -> S2 Metrics
*Sources*: `docs/results/b1_resnet18_ce_supcon_tongji_s1s2_lr1e4_metrics.json`, `docs/results/b2_fixed_gabor_resnet18_tongji_s1s2_lr1e4_metrics.json`, `docs/results/b3_lgfnet_no_gabor_tongji_s1s2_lr1e4_metrics.json`, `experiments/m1_lgfnet_full_tongji_s1s2_lr1e4/metrics.json`

| Method | Rank-1 (%) | Rank-5 (%) | Macro-F1 (%) | EER (%) | TAR@FAR=1e-2 (%) | TAR@FAR=1e-3 (%) | Params | FLOPs | Time |
|---|---|---|---|---|---|---|---|---|---|
| ResNet18 + CE | 5.47 | 14.27 | 5.30 | 24.93 | 10.05 | 1.77 | - | - | - |
| ResNet18 + CE + SupCon, old run | 58.85 | 69.17 | 55.14 | 6.55 | 75.24 | 46.04 | - | - | - |
| ResNet18 + CE + SupCon, lr=1e-4 | 93.65 | 95.80 | 92.71 | 2.34 | 96.26 | 89.62 | 11.46M | 1.819G | 2.03 ms |
| LGFNetSmall full, learnable Gabor | 88.68 | 92.97 | 87.49 | 2.94 | 94.18 | 84.18 | 17.73M | 3.788G | 7.35 ms |
| CNN + DeiT, no Gabor | 89.78 | 92.97 | 88.49 | 2.60 | 95.34 | 86.83 | 17.69M | 2.899G | 6.18 ms |
| Fixed Gabor + ResNet18 | 93.62 | 95.68 | 92.82 | 2.13 | 96.91 | 91.89 | 11.82M | 2.709G | 2.80 ms |

### 7.2. Tongji S2 -> S1 Metrics
*Sources*: `docs/results/b1_resnet18_ce_supcon_tongji_s2s1_lr1e4_metrics.json`, `docs/results/b2_fixed_gabor_resnet18_tongji_s2s1_lr1e4_metrics.json`

| Method | Rank-1 (%) | Rank-5 (%) | Macro-F1 (%) | EER (%) | TAR@FAR=1e-2 (%) | TAR@FAR=1e-3 (%) | Params | FLOPs | Time |
|---|---|---|---|---|---|---|---|---|---|
| ResNet18 + CE + SupCon, lr=1e-4 | 93.13 | 95.13 | 92.15 | 2.27 | 96.19 | 89.89 | 11.46M | 1.819G | 1.59 ms |
| Fixed Gabor + ResNet18 | 93.52 | 95.23 | 92.51 | 2.40 | 96.46 | 91.81 | 11.82M | 2.709G | 3.14 ms |

### 7.3. Tongji Bidirectional Average
*Sources*: Calculated from Tables 7.1 and 7.2

- **B1 (ResNet18 + CE + SupCon, lr=1e-4)**:
  - Rank-1: 93.39%
  - Rank-5: 95.47%
  - Macro-F1: 92.43%
  - EER: 2.31%
  - TAR@FAR=1e-2: 96.23%
  - TAR@FAR=1e-3: 89.75%
  - Time: 1.81 ms
- **B2 (Fixed Gabor + ResNet18)**:
  - Rank-1: 93.57%
  - Rank-5: 95.46%
  - Macro-F1: 92.67%
  - EER: 2.27%
  - TAR@FAR=1e-2: 96.69%
  - TAR@FAR=1e-3: 91.85%
  - Time: 2.97 ms

### 7.4. IITD Within Split Metrics
*Sources*: `experiments/b1_resnet18_ce_supcon_iitd_within_lr1e4/metrics.json`, `docs/results/b2_fixed_gabor_resnet18_iitd_within_lr1e4_metrics.json`

| Method | Rank-1 (%) | Rank-5 (%) | Macro-F1 (%) | EER (%) | TAR@FAR=1e-2 (%) | TAR@FAR=1e-3 (%) | Params | FLOPs | Time |
|---|---|---|---|---|---|---|---|---|---|
| ResNet18 + CE + SupCon | 99.13 | 99.57 | 98.84 | 0.36 | 99.70 | 99.41 | 11.43M | 1.819G | 2.26 ms |
| Fixed Gabor + ResNet18 | 98.26 | 99.13 | 97.68 | 0.71 | 99.29 | 98.93 | 11.78M | 2.709G | 2.86 ms |

- **Verification Verdict**: The values mapped in `tongji_s1s2_summary.md` exactly align (within <0.01% error margin) with the ground-truth JSON logs.

---

## 8. Claim Audit

1. **Intended original claim (Learnable Gabor fusion improves palmprint recognition)**: **NOT SUPPORTED**.
   - *Evidence*: $M1$ (LGFNetSmall) with learnable Gabor (88.68% Rank-1, 84.18% TAR@FAR=1e-3) is significantly worse than baseline $B1$ (93.65% Rank-1, 89.62% TAR) and worse than the ablation $B3$ without Gabor (89.78% Rank-1, 86.83% TAR).
2. **Claim (Fixed Gabor is universally superior)**: **NOT SUPPORTED**.
   - *Evidence*: Baseline $B1$ beats Fixed Gabor $B2$ on IITD within split (99.13% vs 98.26% Rank-1). $B1$ is also significantly more computationally efficient (1.819G FLOPs, 1.81ms) compared to $B2$ (2.709G FLOPs, 2.97ms).
3. **Alternative claim (Fixed Gabor prior improves strict-FAR cross-session verification robustness on Tongji)**: **SUPPORTED**.
   - *Evidence*: $B2$ average TAR@FAR=1e-3 is 91.85% vs $B1$ average TAR@FAR=1e-3 of 89.75% (+2.10 percentage points). Average Macro-F1 also increases from 92.43% to 92.67%.

---

## 9. Reproducibility and Artifact Policy

- **Committed Artifacts**: Code files, config files, dataset metadata, and split JSONs are fully tracked.
- **Ignored Artifacts**: Dataset images (`data/segmented/`) and experiment checkpoints (`best.pt`, `last.pt` under `experiments/`) are excluded from Git to keep the repository clean.
- **Reproducibility Limit**: Checkpoints are intentionally not versioned in Git. Reproducing metrics from scratch requires the segmented datasets and training time. Saved metrics are versioned for documentation, not as a substitute for raw reproducibility.

---

## 10. Required Fixes Before Paper Writing

1. **Fill Documentation Gaps**:
   Copy the ground-truth metric files for `b1_iitd` and `m1` from `experiments/` to the `docs/results/` folder for unified tracking:
   - Copy `experiments/b1_resnet18_ce_supcon_iitd_within_lr1e4/metrics.json` to `docs/results/b1_resnet18_ce_supcon_iitd_within_lr1e4_metrics.json`
   - Copy `experiments/b1_resnet18_ce_supcon_iitd_within_lr1e4/metrics.md` to `docs/results/b1_resnet18_ce_supcon_iitd_within_lr1e4_metrics.md`
   - Copy `experiments/m1_lgfnet_full_tongji_s1s2_lr1e4/metrics.json` to `docs/results/m1_lgfnet_full_tongji_s1s2_lr1e4_metrics.json`
   - Create `docs/results/m1_lgfnet_full_tongji_s1s2_lr1e4_metrics.md` based on the metrics inside `experiments/m1_lgfnet_full_tongji_s1s2_lr1e4/metrics.md`.
2. **Reformulate the Paper Scope**:
   Pivoting the paper title and claim structure away from learnable Gabor fusion to fixed Gabor prior is necessary. Safe and approved titles include:
   - *Fixed Gabor Priors for Robust Cross-Session Palmprint Verification*
   - *Gabor-Guided Metric Learning for Cross-Session Palmprint Recognition*

---

## 11. Optional Next Experiments

1. **Multiple Seeds**: Run B1 and B2 on Tongji with seed 43 and 44 to compute mean and standard deviation.
2. **Confidence Intervals**: Report confidence intervals for TAR@FAR=1e-3 to prove statistical significance.
3. **Alternative Learnable Fusion**: If returning to learnable fusion, redesign the Gabor feature extraction path (e.g., using channel-attention or multi-scale fusion) rather than the current stem design.

---

## 12. Final Decision

```text
FINAL DECISION: PASS WITH WARNINGS
PAPER CLAIM: PARTIALLY SUPPORTED
MAIN REASON: The original claim that learnable Gabor fusion improves recognition is unsupported because M1 is weaker than the baselines and ablation B3, but the alternative claim that a fixed Gabor prior improves strict-FAR cross-session verification robustness on Tongji is strongly and consistently supported.
DO NOT CLAIM:
- Learnable Gabor fusion improves palmprint recognition in the current architecture.
- Fixed Gabor is universally superior to ResNet18 + SupCon across all settings and datasets.
- Fixed Gabor is more computationally efficient than the baseline.
- IITD within-split evaluation proves the superiority of Fixed Gabor.
```
