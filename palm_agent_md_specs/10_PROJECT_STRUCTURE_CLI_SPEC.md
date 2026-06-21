# Project Structure and CLI Specification

## 1. Required project tree

```text
palm_gabor_conformer/
├── configs/
│   ├── default.yaml
│   ├── casia.yaml
│   ├── tju.yaml
│   ├── xjtu.yaml
│   ├── iitd.yaml
│   └── experiments/
│       ├── gabor_only.yaml
│       ├── conformer_only.yaml
│       ├── fused_cosine_kcca.yaml
│       ├── fused_rbf_kcca.yaml
│       └── fused_laplacian_kcca.yaml
├── data/
│   ├── raw/
│   ├── processed/
│   ├── metadata/
│   └── splits/
├── palmrec/
│   ├── datasets/
│   ├── preprocessing/
│   ├── features/
│   ├── models/
│   │   └── conformer/
│   ├── fusion/
│   ├── graph/
│   ├── matching/
│   ├── evaluation/
│   ├── training/
│   └── utils/
├── scripts/
├── experiments/
├── tests/
├── docs/
├── outputs/
├── README.md
├── requirements.txt
└── pyproject.toml
```

## 2. Required scripts

### `scripts/prepare_data.py`

```bash
python scripts/prepare_data.py --config configs/casia.yaml
```

Outputs:

```text
metadata CSV
split JSON
drop/cleaning log
```

### `scripts/train_conformer.py`

```bash
python scripts/train_conformer.py --config configs/casia.yaml
```

Outputs:

```text
best checkpoint
last checkpoint
training log
```

### `scripts/extract_gabor_features.py`

```bash
python scripts/extract_gabor_features.py --config configs/casia.yaml --split train,test
```

Outputs:

```text
gabor_train.npz
gabor_test.npz
```

### `scripts/extract_conformer_features.py`

```bash
python scripts/extract_conformer_features.py --config configs/casia.yaml --split train,test
```

Outputs:

```text
conformer_train.npz
conformer_test.npz
```

### `scripts/fit_kcca.py`

```bash
python scripts/fit_kcca.py --config configs/experiments/fused_cosine_kcca.yaml
```

Outputs:

```text
kcca model
fused_train.npz
fused_test.npz
```

### `scripts/build_knowledge_graph.py`

```bash
python scripts/build_knowledge_graph.py --config configs/casia.yaml
```

Outputs:

```text
graph pkl/json
graph summary
```

### `scripts/evaluate.py`

```bash
python scripts/evaluate.py --config configs/casia.yaml --mode two_stage
```

Outputs:

```text
metrics report
timing report
confusion matrix
```

### `scripts/run_full_pipeline.py`

```bash
python scripts/run_full_pipeline.py --config configs/casia.yaml
```

Runs all stages end-to-end.

## 3. Module boundaries

### Dataset module

Responsible only for:

- metadata parsing
- split
- image loading through preprocessing hooks

### Feature modules

Responsible only for:

- Gabor features
- Conformer features
- feature cache

### Fusion module

Responsible only for:

- KCCA fit/transform/save/load

### Graph/matching module

Responsible only for:

- graph build/query
- candidate filtering
- cosine matching

### Evaluation module

Responsible only for:

- metrics
- reports
- timing

## 4. README commands

README must include:

```bash
pip install -r requirements.txt
python scripts/prepare_data.py --config configs/casia.yaml
python scripts/run_full_pipeline.py --config configs/casia.yaml
pytest
```

## 5. Requirements

Minimum packages:

```text
torch
torchvision
numpy
scipy
scikit-learn
pandas
opencv-python
Pillow
PyYAML
tqdm
joblib
pytest
matplotlib
```
