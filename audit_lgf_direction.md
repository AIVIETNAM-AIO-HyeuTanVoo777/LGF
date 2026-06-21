# LGF-Net Direction Audit

## 1. Verdict

**GO**: The project is on the correct track for LGF-Net research. All Phase 1 modules (manifest generation, splits, dataset loaders, samplers, baseline models, SupCon loss, training, and evaluation scripts) are implemented, verified, and run end-to-end on GPU.

## 2. Repository Status

| Component | Existing files | Status | Comment |
|---|---|---|---|
| **Datasets** | `base.py`, `metadata.py`, `splits.py` | Reproduction | Original Gabor-Conformer-KCCA pipeline files |
| | `palm_dataset.py`, `samplers.py` | LGF-Net Ready | Custom dataloader and RandomIdentitySampler implemented |
| **Preprocessing** | `image_io.py`, `roi.py`, `transforms.py` | Reproduction | Image loading and ROI extraction utilities |
| **Features** | `feature_cache.py`, `gabor.py`, `normalization.py` | Reproduction | Fixed Gabor feature extractors |
| **Fusion** | `kcca.py`, `kernels.py` | Reproduction | Post-processing kernel-CCA fusion |
| **Losses** | `supcon.py`, `combined.py` | LGF-Net Ready | Vectorized Supervised Contrastive Loss and CE+SupCon combined loss |
| **Models** | `conformer/` | Reproduction | Conformer model for the original pipeline |
| | `baselines.py` | LGF-Net Ready | ResNet18 baseline with 256-D L2-normalized embedding projection |
| **Training** | `checkpoint.py`, `loops.py`, `optim.py`, `schedulers.py` | Reproduction | Training loop code for original conformer |
| **Evaluation** | `metrics.py`, `timing.py` | Reproduction | Traditional classification metrics |
| **Scripts** | Conformer/Gabor/KCCA scripts | Reproduction | Original reproduction pipeline scripts |
| | `build_manifest.py`, `make_splits.py` | LGF-Net Ready | Script for manifest and JSON splits generation |
| | `train_lgf.py`, `eval_embedding.py` | LGF-Net Ready | Training script (AMP, Grad Accum) and optimized evaluation script |
| **Configs** | `default.yaml`, `toy.yaml` | Reproduction | Original config files |
| | `resnet18_ce_tongji_s1s2.yaml` | LGF-Net Ready | ResNet18 baseline config for Tongji S1->S2 |

## 3. Dataset Status

| Dataset | Folder | Image count | Extensions | Readable | Notes |
|---|---|---|---|---|---|
| **IITD Left** | `data/segmented/IITD/Left` | 1301 | `.bmp` | Yes | Fixed image size: 150x150 |
| **IITD Right** | `data/segmented/IITD/Right` | 1300 | `.bmp` | Yes | Fixed image size: 150x150 |
| **Tongji S1** | `data/segmented/Tongji/session1` | 6000 | `.bmp` | Yes | Fixed image size: 128x128 |
| **Tongji S2** | `data/segmented/Tongji/session2` | 6000 | `.bmp` | Yes | Fixed image size: 128x128 |

## 4. Label/Protocol Risk

- **IITD Labeling**: Filename scheme `001_1.bmp` correctly maps to subject `001` and sample `1`. Class IDs are constructed as `IITD_{hand}_{subject_id}` (e.g., `IITD_Left_001`). There is no label overlap between different hand sides or datasets.
- **Tongji Labeling**: Verified formula `palm_idx = (image_number - 1) // 10 + 1` correctly maps filenames `00001.bmp` to `06000.bmp` into 600 unique palms. Filenames are identical in `session1` and `session2` for the same palm.
- **Leakage Prevention**: For `tongji_s1_to_s2`, Session 1 is used for training and validation, while Session 2 is used exclusively for testing. Gallery and probe splits map to the same classes, but utilize different sessions.
- **Class Alignment**: In multi-dataset/few-shot scenarios, class indexing is aligned by passing the training set class mapping dictionary to the validation/testing datasets, mapping labels to a contiguous range `[0, C-1]` and preventing index out-of-bounds in classification heads.

## 5. Missing Files for Phase 1

| File | Required | Exists | Action |
|---|---|---|---|
| `scripts/build_manifest.py` | Yes | Yes | None (Implemented) |
| `scripts/make_splits.py` | Yes | Yes | None (Implemented) |
| `palmrec/datasets/palm_dataset.py` | Yes | Yes | None (Implemented) |
| `palmrec/datasets/samplers.py` | Yes | Yes | None (Implemented) |
| `palmrec/models/baselines.py` | Yes | Yes | None (Implemented) |
| `palmrec/losses/supcon.py` | Yes | Yes | None (Implemented) |
| `palmrec/losses/combined.py` | Yes | Yes | None (Implemented) |
| `scripts/train_lgf.py` | Yes | Yes | None (Implemented) |
| `scripts/eval_embedding.py` | Yes | Yes | None (Implemented) |
| `configs/resnet18_ce_tongji_s1s2.yaml` | Yes | Yes | None (Implemented) |

*All required files for Phase 1 are present and fully operational.*

## 6. Hardware-Aware Training Recommendation

For training on the NVIDIA GeForce RTX 4050 Laptop GPU (6GB VRAM):
- **Batch Size**: 16 (P=8, K=2) or 8 (P=4, K=2). Small batch sizes are highly recommended.
- **Gradient Accumulation**: Set `grad_accumulation_steps` to 2 or 4 to simulate a batch size of 32 or 64.
- **AMP (Automatic Mixed Precision)**: Maintain `amp: true` to save VRAM and accelerate processing.
- **Number of Workers**: Maintain `num_workers: 0` for safe multi-processing execution on Windows.
- **Image Size**: Resizing to `224x224` is optimal for ResNet18 and DeiT-Tiny.

## 7. Exact Next Actions

1. **[P0]** Implement the full `LGFNet` architecture in Phase 2:
   - Define a `LearnableGaborStem` block using custom convolutional kernels.
   - Set up the dual branch: `ResNet18` branch and `DeiT-Tiny` branch.
   - Implement the `GatedFusionModule` to merge features dynamically.
2. **[P1]** Integrate model complexity evaluation tools in `scripts/eval_embedding.py`:
   - Compute model parameters count (Params).
   - Compute FLOPs using external tools like `fvcore` or `thop` (if available).
   - Log average inference time per image.
3. **[P1]** Create full configuration YAML for LGF-Net:
   - Create `configs/lgfnet_ce_supcon_tongji_s1s2.yaml`.
4. **[P2]** Run end-to-end training and evaluation for LGF-Net on the 4 splits.

## 8. Blockers

None.

## 9. Commands Run

- **PyTorch/CUDA Verification**:
  ```powershell
  python -c "import torch; print(torch.__version__); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
  ```
  Result: `2.12.0+cu126`, `True`, `NVIDIA GeForce RTX 4050 Laptop GPU`.
- **Dataset Count and Size Stats**:
  ```powershell
  python -c "..."
  ```
  Result: IITD has 2,601 images ($150 \times 150$). Tongji has 12,000 images ($128 \times 128$). All images are readable.
- **Baseline Training Check**:
  ```powershell
  $env:PYTHONPATH="d:\0.Research\PALM_CGK_BASE\PALM_CGK_BASE"; python scripts/train_lgf.py --config configs/resnet18_ce_tongji_s1s2.yaml
  ```
  Result: Completed 2 epochs successfully on GPU. Saved checkpoint `best.pt`.
- **Embedding Evaluation Check**:
  ```powershell
  $env:PYTHONPATH="d:\0.Research\PALM_CGK_BASE\PALM_CGK_BASE"; python scripts/eval_embedding.py --checkpoint experiments/resnet18_ce_tongji_s1s2/checkpoints/best.pt --config configs/resnet18_ce_tongji_s1s2.yaml
  ```
  Result: Successfully generated evaluation reports. Output metrics: Rank-1 (8.28%), Rank-5 (16.72%), EER (27.80%).
- **Pytest Run**:
  ```powershell
  $env:PYTHONPATH="d:\0.Research\PALM_CGK_BASE\PALM_CGK_BASE"; pytest
  ```
  Result: `41 passed` successfully.
