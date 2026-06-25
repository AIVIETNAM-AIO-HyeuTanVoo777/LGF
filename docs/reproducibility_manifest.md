# Reproducibility Manifest

This document records the exact system configuration, dataset details, split properties, and commands necessary to reproduce the evaluation and table generation results presented in the paper.

## 1. Repository State
- **Repository URL**: `https://github.com/AIVIETNAM-AIO-HyeuTanVoo777/LGF`
- **Commit Hash**: `ce0611fcfbc9dbf8cf2727edf7998e2164157979`
- **Branch**: `rankb-protocol-study-revision`
- **Generated on**: 2026-06-25

## 2. Environment Configuration
- **OS**: Windows (version details captured in pip_freeze.txt)
- **Python**: 3.13.13 (tags/v3.13.13:01104ce, Apr 7 2026, 19:25:48) [MSC v.1944 64 bit (AMD64)]
- **PyTorch**: 2.12.0+cu126
- **CUDA**: 12.6
- **GPU**: NVIDIA GeForce RTX 4050 Laptop GPU
- **CPU**: AMD Ryzen 5 or equivalent
- **Conda Environment / Requirements File**: Environment package list is recorded in [pip_freeze.txt](file:///D:/0.Research/PALM_CGK_BASE/PALM_CGK_BASE/docs/agent_logs/pip_freeze.txt).

## 3. Data Properties
### Tongji Palmprint Dataset
- **Dataset name**: Tongji Palmprint Dataset
- **Raw/segmented data location**: `data/tongji/`
- **Manifest file**: `data/tongji/manifest.json`
- **Image count**: 12,000 images
- **Palm-class count**: 600 classes (each corresponding to a specific palm direction of a subject)
- **Session count**: 2 sessions (Session 1 and Session 2)
- **Image size**: 128x128 pixels (normalized crop)
- **License/access note**: Academic research use only. Proprietary database from Tongji University.
- **Included in repo?**: No (restricted distribution)

### IIT Delhi (IITD) Palmprint Database
- **Dataset name**: IIT Delhi (IITD) Palmprint Image Database version 1.0
- **Raw/segmented data location**: `data/iitd/`
- **Manifest file**: `data/iitd/manifest.json`
- **Image count**: 2,601 images
- **Palm-class count**: 460 classes (230 subjects, left and right hands)
- **Session count**: 1 session
- **Image size**: 128x128 pixels (normalized crop)
- **License/access note**: Academic research use only. Proprietary database from IIT Delhi.
- **Included in repo?**: No (restricted distribution)

## 4. Splits Properties
All 9 official splits are fully audited, subject-disjoint, and verified to prevent leakage:
- Split audits are summarized in [split_audit.csv](file:///D:/0.Research/PALM_CGK_BASE/PALM_CGK_BASE/docs/audits/split_audit.csv).
- Summaries of partition shapes and disjoint verify logs are available in [split_audit.md](file:///D:/0.Research/PALM_CGK_BASE/PALM_CGK_BASE/docs/audits/split_audit.md) and [gallery_probe_audit.md](file:///D:/0.Research/PALM_CGK_BASE/PALM_CGK_BASE/docs/audits/gallery_probe_audit.md).

## 5. Configurations Matrix
The full final configurations mapping method names (M0–M7) to their run details is recorded in [rankb_run_manifest.csv](file:///D:/0.Research/PALM_CGK_BASE/PALM_CGK_BASE/docs/results/rankb_run_manifest.csv).
The configuration YAML files are stored under `configs/rankb_final/`.

## 6. Training and Evaluation Commands
- **Full experiment run list**: To train and evaluate the full matrix of experiments, see commands in `configs/rankb_final/`.
- **Smoke Tests**: Run the following scripts to verify that model loading and metric extraction function correctly on checkpoints:
  - Bash/Linux: `bash scripts/run_rankb_smoke_tests.sh`
  - PowerShell/Windows: `powershell -ExecutionPolicy Bypass -File scripts/run_rankb_smoke_tests.ps1`

## 7. Result Collection and Table Generation
To collect raw JSON metrics and generate LaTeX tables:
1. **Collect Results**:
   ```bash
   python scripts/collect_results.py --manifest docs/results/rankb_run_manifest.csv --out-dir docs/results
   ```
2. **Compute Paired Deltas**:
   ```bash
   python scripts/compute_paired_statistics.py --input docs/results/main_tongji_results.csv --out docs/results/paired_deltas.csv
   ```
3. **Generate LaTeX Tables**:
   ```bash
   python scripts/make_result_tables.py --results-dir docs/results --out-dir paper/sections
   ```

## 8. Metric Implementation
- **Canonical metric implementation**: Vectorized conservative TAR@FAR metric is defined in `palmrec/evaluation/metrics.py` under the function `conservative_tar_at_far`.
- **Unit test file**: Verification of correct/conservative metric behavior is in `tests/test_metrics_tar_far.py`.

## 9. Generated Results Artifacts
- **Tongji main results**: [main_tongji_results.csv](file:///D:/0.Research/PALM_CGK_BASE/PALM_CGK_BASE/docs/results/main_tongji_results.csv)
- **IITD secondary validation**: [iitd_secondary_results.csv](file:///D:/0.Research/PALM_CGK_BASE/PALM_CGK_BASE/docs/results/iitd_secondary_results.csv)
- **Paired deltas**: [paired_deltas.csv](file:///D:/0.Research/PALM_CGK_BASE/PALM_CGK_BASE/docs/results/paired_deltas.csv)
- **Score-tail diagnostics**: [score_tail_diagnostics.csv](file:///D:/0.Research/PALM_CGK_BASE/PALM_CGK_BASE/docs/results/score_tail_diagnostics.csv)

## 10. Paper Build
- **LaTeX Entry Point**: `paper/main.tex`
- **Build command**:
  ```bash
  cd paper && latexmk -pdf -interaction=nonstopmode main.tex
  ```
- **Expected PDF path**: `paper/main.pdf`
- **Bibliography file**: `paper/main.bib`

## 11. Non-reproducible / Omitted Artifacts
- **Raw Images**: The raw palmprint images in `data/tongji/` and `data/iitd/` are not committed to Git due to dataset distribution agreements. To access them, request authorization from Tongji University and IIT Delhi.
- **Model Checkpoints**: Model checkpoints (`experiments/**/*.pt`) are omitted from Git due to file size limits. They can be requested from the authors or trained locally using `scripts/train_lgf.py` with the configuration files in `configs/rankb_final/`.
