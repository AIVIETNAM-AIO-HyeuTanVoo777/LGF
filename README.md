# Palmprint Features Fusion Recognition Based on Conformer and Gabor

This repository contains the official implementation of the palmprint recognition pipeline proposed in **"Palmprint Features Fusion Recognition Based on Conformer and Gabor"**.

---

## 1. Installation

Install all required packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## 2. Dataset Preparation

To prepare dataset metadata and generate deterministic split partitions:

```bash
python scripts/prepare_data.py --config configs/casia.yaml
```

*Note: For validation and toy runs, a synthetic `TOY` dataset is generated automatically under `data/toy` when running with `configs/toy.yaml`.*

---

## 3. Running the Full Pipeline

You can run the end-to-end training, feature extraction, fusion, graph building, and evaluation using a single command:

```bash
python scripts/run_full_pipeline.py --config configs/casia.yaml
```

---

## 4. Run Unit and Integration Tests

To run the complete test suite of 41 tests verifying all Gabor, Conformer, KCCA, and Knowledge Graph components:

```bash
pytest
```

---

## 5. Paper Experiments & Table Reproduction

We provide dedicated scripts under `experiments/` to reproduce the exact tables and results reported in the paper:

### Table 2: Proposed Method Accuracy
```bash
python experiments/reproduce_table2_casia_accuracy.py --config configs/casia.yaml
```

### Table 3: Time Complexity / Latency Analysis
```bash
python experiments/reproduce_table3_time_complexity.py --config configs/casia.yaml
```

### Table 4: Performance Comparison of Two-Stage vs One-Stage Search
```bash
python experiments/reproduce_table4_two_stage_vs_one_stage.py --config configs/casia.yaml
```

### Table 5: Feature Space Comparison (Gabor vs Conformer vs Fused)
```bash
python experiments/reproduce_table5_feature_comparison.py --config configs/casia.yaml
```

### Table 6: Comparison of KCCA Kernels (Laplacian vs RBF vs Cosine)
```bash
python experiments/reproduce_table6_kernel_comparison.py --config configs/casia.yaml
```
"# LGF" 
