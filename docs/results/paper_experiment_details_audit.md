# Paper Experiment Details Audit

## Scope

This audit documents the evidence used to update `paper/sections/04_experiments.tex` and `paper/sections/07_discussion.tex`. No training, evaluation, model code changes, split changes, metric changes, checkpoint reads, or commits were performed.

## Sources Read

- `paper/paper_review_packet.md`
- `paper/sections/04_experiments.tex`
- `paper/sections/07_discussion.tex`
- `docs/results/final_paper_evidence.md`
- `docs/results/final_paper_tables.md`
- `docs/results/b6_multiseed_summary.md`
- `docs/results/final_integrity_audit.md`
- `configs/b6_resnet18_bnneck_arcface_tongji_s1s2_lr1e4_seed42.yaml`
- `configs/b6_resnet18_bnneck_arcface_tongji_s2s1_lr1e4_seed42.yaml`
- `configs/b1_resnet18_ce_supcon_tongji_s1s2_lr1e4.yaml`
- `configs/b1_resnet18_ce_supcon_tongji_s2s1_lr1e4.yaml`
- `data/splits/tongji_s1_to_s2.json`
- `data/splits/tongji_s2_to_s1.json`
- `data/splits/iitd_within.json`
- `data/metadata/palm_segmented_manifest.csv`
- `audit_lgf_direction.md`
- `.gitignore`
- `README.md`

## Evidence Found

### Dataset and Manifest Evidence

- `data/metadata/palm_segmented_manifest.csv` contains 14,601 rows.
- Tongji contains 12,000 images, 600 palms/classes, 6,000 images in `session1`, and 6,000 images in `session2`.
- IITD contains 2,601 images and 460 palms/classes.
- `docs/results/final_integrity_audit.md` records Tongji image size as 128x128 and IITD image size as 150x150.

### Split Evidence

| Split file | Train | Val | Gallery | Probe | Support |
|---|---:|---:|---:|---:|---:|
| `data/splits/tongji_s1_to_s2.json` | 4,800 | 1,200 | 6,000 | 6,000 | 0 |
| `data/splits/tongji_s2_to_s1.json` | 4,800 | 1,200 | 6,000 | 6,000 | 0 |
| `data/splits/iitd_within.json` | 1,681 | 460 | 1,681 | 460 | 0 |

The Tongji split JSON samples show S1->S2 uses session 1 for train/val/gallery and session 2 for probe. S2->S1 reverses the session direction. The IITD split is a within-dataset split.

### Training Configuration Evidence

The B1 and B6 config files verify:

- epochs: 60
- learning rate: 0.0001
- weight decay: 0.0001
- embedding dimension: 256
- AMP: true
- gradient accumulation steps: 4
- sampler: `num_identities=8`, `num_instances=2`, `fallback_identities=4`
- data loader workers: 0
- B1: ResNet18Baseline, CE + SupCon, `lambda_supcon=0.10`, `temperature=0.07`
- B6: ResNet18BNNeck, ArcFace, `scale=30.0`, `margin=0.5`, `lambda_supcon=0.0`, `temperature=0.07`
- B6 eval embedding: `post_bn`

`docs/results/b6_multiseed_summary.md` verifies the Tongji multi-seed scope: seeds 42, 2026, and 2705 across S1->S2 and S2->S1.

### Checkpoint and Evaluation Evidence

- `docs/results/final_integrity_audit.md` states that `scripts/train_lgf.py` saves `best.pt` and `last.pt` under checkpoints.
- `docs/results/final_integrity_audit.md` states that `scripts/eval_embedding.py` loads config and checkpoint, extracts normalized embeddings, computes cosine similarity, applies self-match masking, and reports Rank-1, Rank-5, Macro-F1, EER, TAR@FAR=1e-2, TAR@FAR=1e-3, FLOPs, and average inference time.
- The current paper only states that evaluation uses the `best.pt` checkpoint produced by the training script; it does not claim an unverified checkpoint-selection criterion.

### Hardware and Software Evidence

- `audit_lgf_direction.md` records NVIDIA GeForce RTX 4050 Laptop GPU with 6GB VRAM.
- `audit_lgf_direction.md` records PyTorch/CUDA verification output: `2.12.0+cu126`, CUDA available, NVIDIA GeForce RTX 4050 Laptop GPU.
- `docs/results/final_integrity_audit.md` records Conda environment `palm_lgf`.

### Artifact Policy Evidence

- `.gitignore` excludes `data/segmented/`, `experiments/`, `*.pt`, `*.pth`, `*.ckpt`, and `*.onnx`.
- `docs/results/final_integrity_audit.md` states that dataset images and experiment checkpoints are excluded from Git, while configs, metadata, split JSON files, code, and saved metrics are tracked.

## Inserted Into Paper

- Added Tongji and IITD dataset sizes, class counts, sessions, and image sizes to `paper/sections/04_experiments.tex`.
- Added exact split-size table for Tongji S1->S2, Tongji S2->S1, and IITD within.
- Added B1/B6 training recipe details from configs, including AMP, gradient accumulation, sampler settings, data loader workers, SupCon weight, ArcFace scale/margin, and B6 post-BN evaluation embedding.
- Added checkpoint/evaluation protocol using `best.pt`, normalized embeddings, cosine similarity, and the reported metrics.
- Added reproducibility paragraph listing `scripts/train_lgf.py`, `scripts/eval_embedding.py`, `scripts/aggregate_b6_multiseed.py`, B6 config pattern, and `docs/results/b6_multiseed_summary.md`.
- Added verified hardware/software fields: RTX 4050 Laptop GPU 6GB, PyTorch 2.12.0+cu126, Conda env `palm_lgf`.
- Added discussion limitations for hardware-dependent latency and the Tongji dataset citation needing full verification before submission.

## Remaining TODO

- Verify OS, CPU, and RAM for the final B6 runs. The requested values Windows 11, i7-14650HX, and RAM 16GB were not found in the repository evidence read for this audit.
- Verify the full Tongji dataset paper citation before submission. `paper/references.bib` does not currently include a Tongji dataset citation.
- Document preprocessing/augmentation details for the final training/evaluation recipe if the paper needs a complete reproducibility appendix. The current update only uses segmented ROI manifest evidence and config-backed loader/training settings.
- If required by the target venue, record exact package versions beyond PyTorch/CUDA and Conda environment name.

## Uncertain Items Not Inserted

- Windows version, CPU model, and RAM were not inserted into the paper because they were not found in repo evidence.
- A specific best-checkpoint selection rule was not inserted because the read evidence confirms `best.pt` output but does not describe the selection criterion in enough detail for paper wording.
- Full Tongji publication metadata was not inserted because the bibliography does not yet contain a verified Tongji dataset entry.

## Files Changed

- `paper/sections/04_experiments.tex`
- `paper/sections/07_discussion.tex`
- `docs/results/paper_experiment_details_audit.md`
