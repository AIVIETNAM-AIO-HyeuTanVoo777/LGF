# Coding Task Breakdown

## Milestone 1 — Scaffold and config

Files:

```text
palmrec/utils/config.py
palmrec/utils/seed.py
palmrec/utils/logging.py
configs/default.yaml
requirements.txt
pyproject.toml
README.md
```

Implement:

- config loader
- seed setter
- logger
- device selection

Acceptance:

- `python scripts/run_full_pipeline.py --config configs/default.yaml --dry-run` imports successfully.

Tests:

- config load
- seed determinism

---

## Milestone 2 — Dataset and metadata

Files:

```text
palmrec/datasets/base.py
palmrec/datasets/metadata.py
palmrec/datasets/splits.py
palmrec/datasets/casia.py
palmrec/datasets/tju.py
palmrec/datasets/xjtu.py
palmrec/datasets/iitd.py
scripts/prepare_data.py
```

Implement:

- unified metadata schema
- dataset parsers
- per-palm 1:1 split
- odd sample drop logging
- PyTorch dataset

Acceptance:

- metadata CSV and split JSON created.
- no train/test overlap.
- train/test counts equal per palm ID.

Tests:

- even split
- odd drop
- reproducible split

---

## Milestone 3 — Preprocessing

Files:

```text
palmrec/preprocessing/image_io.py
palmrec/preprocessing/roi.py
palmrec/preprocessing/transforms.py
```

Implement:

- image read
- identity ROI extractor
- grayscale transform
- RGB tensor transform
- 224×224 resize

Acceptance:

- Gabor input shape `[224, 224]`.
- Conformer input shape `[3, 224, 224]`.

Tests:

- grayscale conversion
- RGB conversion
- resize

---

## Milestone 4 — Gabor extractor

Files:

```text
palmrec/features/gabor.py
palmrec/features/normalization.py
scripts/extract_gabor_features.py
tests/test_gabor.py
```

Implement:

- 7×6 filter bank
- convolution
- orientation max fusion
- scale concatenation
- optional pooling
- feature save/load

Acceptance:

- feature dimension stable.
- no NaN.
- runs on toy image.

Tests:

- filter count
- orientation values
- output shape
- determinism

---

## Milestone 5 — Conformer

Files:

```text
palmrec/models/conformer/backbone.py
palmrec/models/conformer/conv_branch.py
palmrec/models/conformer/transformer_branch.py
palmrec/models/conformer/fcu.py
palmrec/models/conformer/classifier.py
palmrec/training/loops.py
palmrec/training/optim.py
palmrec/training/schedulers.py
palmrec/training/checkpoint.py
scripts/train_conformer.py
scripts/extract_conformer_features.py
```

Implement:

- visual Conformer
- classifier training
- feature extraction
- checkpointing

Acceptance:

- forward pass works.
- train loop runs.
- checkpoint saved.
- feature extraction saved.

Tests:

- logits shape
- feature shape
- FCU shapes
- tiny overfit

---

## Milestone 6 — Feature cache

Files:

```text
palmrec/features/feature_cache.py
```

Implement:

- NPZ writer/reader
- metadata alignment validation

Acceptance:

- Gabor and Conformer features align by sample ID.

Tests:

- roundtrip
- alignment error

---

## Milestone 7 — KCCA

Files:

```text
palmrec/fusion/kernels.py
palmrec/fusion/kcca.py
palmrec/fusion/reducers.py
palmrec/fusion/serializers.py
scripts/fit_kcca.py
```

Implement:

- cosine/RBF/Laplacian kernels
- centered regularized KCCA
- fit/transform
- save/load

Acceptance:

- fit and transform toy data.
- fused features saved.
- cosine default.

Tests:

- kernels
- KCCA shape
- no singular crash
- save/load consistency

---

## Milestone 8 — Knowledge graph and matcher

Files:

```text
palmrec/graph/knowledge_graph.py
palmrec/graph/graph_builder.py
palmrec/graph/graph_query.py
palmrec/matching/cosine.py
palmrec/matching/matcher.py
palmrec/matching/two_stage.py
scripts/build_knowledge_graph.py
```

Implement:

- graph layers
- fallback query
- cosine matcher
- one-stage and two-stage recognition

Acceptance:

- graph built from train fused features.
- two-stage predicts all test samples.
- fallback works.

Tests:

- graph query
- matcher
- candidate reduction

---

## Milestone 9 — Evaluation

Files:

```text
palmrec/evaluation/metrics.py
palmrec/evaluation/timing.py
palmrec/evaluation/reports.py
palmrec/evaluation/confusion.py
scripts/evaluate.py
```

Implement:

- accuracy
- precision
- recall
- F1
- confusion matrix
- timing report

Acceptance:

- report generated in JSON/CSV/MD.
- metrics match sklearn.

Tests:

- toy metrics
- report writer

---

## Milestone 10 — Experiments and docs

Files:

```text
experiments/reproduce_table2_casia_accuracy.py
experiments/reproduce_table3_time_complexity.py
experiments/reproduce_table4_two_stage_vs_one_stage.py
experiments/reproduce_table5_feature_comparison.py
experiments/reproduce_table6_kernel_comparison.py
docs/paper_mapping.md
docs/assumptions.md
docs/reproduction.md
```

Acceptance:

- experiment scripts run on toy data.
- docs state all assumptions.
- paper mapping links code modules to paper sections.

---

## Milestone 11 — Final integration

Implement:

```text
scripts/run_full_pipeline.py
```

Acceptance:

- full toy dataset pipeline passes.
- real dataset run starts and validates paths/configs.
- all tests pass.
