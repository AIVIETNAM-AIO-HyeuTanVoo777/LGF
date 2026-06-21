# Evaluation and Experiment Specification

## 1. Required metrics

Paper metrics:

- Accuracy
- Precision
- Recall
- F1-score

Implement:

```python
compute_accuracy(y_true, y_pred)
compute_precision_recall_f1(y_true, y_pred, average="macro")
compute_confusion_matrix(y_true, y_pred)
classification_report(y_true, y_pred)
```

For multi-class palm ID recognition, report:

- accuracy
- macro precision/recall/F1
- weighted precision/recall/F1
- per-class report
- confusion matrix path

## 2. Timing metrics

Required timing fields:

```text
gabor_extraction_ms
conformer_extraction_ms
kcca_fusion_ms
graph_query_ms
matching_ms
total_ms
candidate_count
```

Report mean, std, min, max over test samples.

## 3. Experiments to implement

### E1. Proposed method

```text
Gabor + Conformer + KCCA cosine + knowledge graph + cosine matching
```

### E2. Feature comparison

Compare:

- Gabor only
- Conformer only
- KCCA fused features

Paper feature comparison mentions Euclidean distance in that specific experiment. Implement distance metric as configurable:

```yaml
experiment:
  matcher_for_feature_comparison: euclidean
```

Default final matcher remains cosine.

### E3. Kernel comparison

Compare KCCA kernels:

- Laplacian
- RBF
- cosine

Expected paper direction:

```text
cosine kernel should be strongest
```

### E4. Two-stage vs one-stage

Same fused features and same cosine matcher:

- one-stage global search
- two-stage graph-filtered search

Report:

- accuracy
- timing
- candidate count
- speedup

### E5. Dataset-level evaluation

Run on:

- CASIA
- TJU
- XJTU
- IITD

## 4. Experiment scripts

```text
experiments/reproduce_table2_casia_accuracy.py
experiments/reproduce_table3_time_complexity.py
experiments/reproduce_table4_two_stage_vs_one_stage.py
experiments/reproduce_table5_feature_comparison.py
experiments/reproduce_table6_kernel_comparison.py
```

## 5. Result artifacts

Each experiment writes:

```text
outputs/reports/{dataset}/{experiment}.json
outputs/reports/{dataset}/{experiment}.csv
outputs/reports/{dataset}/{experiment}.md
outputs/reports/{dataset}/{experiment}_confusion.npy
outputs/logs/{dataset}/{experiment}.log
```

## 6. Report schema

```json
{
  "dataset": "CASIA",
  "experiment": "fused_cosine_kcca_two_stage",
  "seed": 42,
  "num_train": 0,
  "num_test": 0,
  "num_classes": 0,
  "metrics": {
    "accuracy": 0.0,
    "macro_precision": 0.0,
    "macro_recall": 0.0,
    "macro_f1": 0.0,
    "weighted_precision": 0.0,
    "weighted_recall": 0.0,
    "weighted_f1": 0.0
  },
  "timing_ms": {
    "gabor_mean": 0.0,
    "conformer_mean": 0.0,
    "kcca_mean": 0.0,
    "graph_query_mean": 0.0,
    "matching_mean": 0.0,
    "total_mean": 0.0
  },
  "config_path": "",
  "config_hash": "",
  "hardware": {},
  "notes": []
}
```

## 7. Baseline policy

The paper compares against multiple external methods. The agent must not fabricate baseline reproduction.

Allowed:

1. Implement proposed method first.
2. Implement baselines only if code/specs are available.
3. If using paper-reported baseline numbers, label them as:

```text
paper_reported_not_reproduced
```

## 8. Tests

- metrics match scikit-learn on toy labels.
- timing meter records all stages.
- report writer outputs JSON/CSV/MD.
- experiment dry-run works on toy dataset.
