# Audited Protocol-Sensitive Evaluation of Recognition Heads and Losses for Cross-Session Palmprint Recognition

This repository is the reproducibility artifact for the paper "Audited Protocol-Sensitive Evaluation of Recognition Heads and Losses for Cross-Session Palmprint Recognition".

The artifact supports an audit-supported evaluation of recognition heads and losses under controlled palmprint protocols. It is an evaluation/protocol paper, not a new architecture paper. The main evidence is the audited Tongji cross-session protocol; IITD is included only as secondary within-session validation.

## Scope

- Primary dataset: Tongji, audited cross-session S1->S2 and S2->S1 evaluation.
- Secondary dataset: IITD, corrected within-session validation.
- Model variants: M0, M1, M2, M3, M4, M6, and M7.
- Claim boundary: results are reported under the audited Tongji cross-session protocol and the IITD within-session validation protocol. The repository does not claim SOTA or external cross-dataset robustness.
- Audit boundary: deterministic checks support the reported protocol and metric handling. They are not third-party certification.

## What Is Included

- Source code under `palmrec/` for dataset loading, ResNet18/BNNeck model variants, losses, training, embedding evaluation, metrics, and config loading.
- Canonical YAML configs under `configs/rankb_final/`.
- Public metadata manifests and split definitions under `data/metadata/` and `data/splits/`.
- Non-sensitive audit summaries and result manifests under `audit_artifacts/`.
- Paper LaTeX source under `paper/`.
- Lightweight tests under `tests/`.

## What Is Not Included

Raw datasets, segmented images, trained checkpoints, generated experiment directories, score tensors, local machine paths, submission ZIPs, and private data are not part of the artifact. Users must obtain Tongji and IITD from their official sources and place local data outside Git-tracked paths.

## Installation

Expected environment: Python 3.10+, PyTorch, torchvision, NumPy, SciPy, scikit-learn, pandas, Pillow, OpenCV, PyYAML, matplotlib, and pytest.

```bash
pip install -r requirements.txt
```

## Dataset Manifests

After obtaining the datasets from official sources, prepare segmented images in this local structure:

```text
data/segmented/Tongji/session1/*.bmp
data/segmented/Tongji/session2/*.bmp
data/segmented/IITD/Left/*.bmp
data/segmented/IITD/Right/*.bmp
```

Then rebuild the manifest:

```bash
python scripts/prepare_manifest.py --segmented-root data/segmented --output data/metadata/palm_segmented_manifest.csv
```

The tracked manifest and split files contain relative paths only; they do not redistribute image data.

## Reproduction Commands

Verify split integrity:

```bash
python scripts/verify_splits.py
```

Run deterministic protocol audits:

```bash
python scripts/audit_protocol.py
```

Recompute conservative threshold evidence when local `scores.csv` files from experiment runs are available:

```bash
python scripts/audit_protocol.py --include-thresholds
```

Regenerate main paper tables from bundled summary CSVs:

```bash
python scripts/reproduce_main_tables.py
```

Regenerate supplementary audit tables:

```bash
python scripts/reproduce_supplementary_tables.py
```

Regenerate ROC/DET/score figures when local `roc.csv` and `scores.csv` files are available:

```bash
python scripts/plot_roc_det.py
```

Run a training job:

```bash
python scripts/run_training.py --config configs/rankb_final/m6_resnet18_bnneck_arcface_tongji_s1s2_seed42.yaml
```

Evaluate a checkpoint:

```bash
python scripts/evaluate.py --checkpoint experiments/<run>/checkpoints/best.pt --config configs/rankb_final/m6_resnet18_bnneck_arcface_tongji_s1s2_seed42.yaml
```

Run tests:

```bash
pytest
```

## Repository Layout

```text
README.md
LICENSE
CITATION.cff
pyproject.toml
requirements.txt
configs/
scripts/
palmrec/
tests/
docs/
audit_artifacts/
paper/
supplementary/
data/metadata/
data/splits/
```

Legacy Conformer, LGF/Gabor-fusion, KCCA, knowledge-graph, CASIA, and working-note material from the previous project has been removed from the public artifact. The Git history preserves prior development context, but those components are not part of the submitted paper artifact.

## Citation

If you use this artifact, cite the paper using `CITATION.cff`.

## License

Code is released under the MIT License. Dataset files are not redistributed and remain subject to their original dataset licenses and access terms.

