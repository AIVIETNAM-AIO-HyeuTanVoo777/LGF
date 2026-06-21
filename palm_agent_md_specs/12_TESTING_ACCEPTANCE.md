# Testing and Acceptance Specification

## 1. Test categories

Required:

1. Unit tests.
2. Integration tests.
3. Reproducibility tests.
4. Shape tests.
5. Numerical stability tests.
6. CLI smoke tests.

## 2. Unit tests

### Dataset

```text
test_metadata_schema
test_split_even_class
test_split_odd_class_drops_one
test_split_reproducibility
test_no_train_test_overlap
```

### Preprocessing

```text
test_identity_roi
test_resize_224
test_gabor_grayscale_shape
test_conformer_rgb_shape
```

### Gabor

```text
test_filter_bank_num_scales
test_filter_bank_num_orientations
test_orientation_values
test_gabor_feature_dim
test_gabor_no_nan
test_gabor_deterministic
```

### Conformer

```text
test_conformer_forward_logits_shape
test_conformer_extract_features_shape
test_fcu_conv_to_trans_shape
test_fcu_trans_to_conv_shape
test_tiny_batch_train_step
```

### Feature cache

```text
test_npz_roundtrip
test_sample_id_alignment
test_alignment_error_on_mismatch
```

### KCCA

```text
test_cosine_kernel_symmetry
test_rbf_kernel_symmetry
test_laplian_kernel_symmetry
test_kcca_fit_transform_shape
test_kcca_no_nan
test_kcca_save_load_same_output
```

### Graph and matching

```text
test_graph_add_template
test_graph_query_gender_hand
test_graph_query_missing_gender
test_graph_query_missing_hand
test_graph_global_fallback
test_cosine_matcher_best
test_cosine_matcher_threshold
test_two_stage_candidate_reduction
```

### Evaluation

```text
test_accuracy_matches_sklearn
test_macro_precision_recall_f1_matches_sklearn
test_confusion_matrix_shape
test_timing_meter
test_report_writer
```

## 3. Integration test: toy pipeline

Create a synthetic dataset:

```text
2 subjects
2 hands each
4 images per palm
16 total images
```

Run:

```bash
python scripts/prepare_data.py --config configs/toy.yaml
python scripts/run_full_pipeline.py --config configs/toy.yaml
```

Acceptance:

- all output files exist.
- no stage crashes.
- number of predictions equals number of test samples.
- metrics are numeric.
- timing report exists.

## 4. Reproducibility acceptance

Same seed must produce:

- same split JSON
- same dropped odd samples
- same Gabor features
- same KCCA transformed features when using deterministic solver/settings
- same predictions from cached features

## 5. Numerical acceptance

- No NaN/Inf in features.
- KCCA regularization prevents singular crashes.
- Cosine similarity handles zero vectors with epsilon.
- Feature dimensions are logged.

## 6. Paper-fidelity acceptance

The build is rejected if:

- KCCA is missing.
- Knowledge graph is missing.
- Conformer is replaced by plain CNN.
- Gabor filter bank does not have 7 scales and 6 orientations.
- Final matcher is not cosine in the main pipeline.
- Train/test split is not per palm ID.
- Conformer training defaults differ from paper without explicit config override.
- Assumptions are not documented.
