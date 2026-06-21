# Agent Master Prompt

You are a coding agent implementing the paper:

**Palmprint Features Fusion Recognition Based on Conformer and Gabor**

Your task is to build a faithful PyTorch-based reproduction of the paper's pipeline. You must not simplify or substitute the main algorithm.

## Primary objective

Implement the following palmprint recognition pipeline:

```text
Palmprint ROI image
→ Gabor feature extraction
→ Conformer feature extraction
→ KCCA fusion
→ Knowledge graph candidate filtering
→ Cosine similarity matching
→ Evaluation
```

## Mandatory pipeline components

You must implement:

1. Dataset loaders and metadata normalization for CASIA, TJU, XJTU, IITD.
2. ROI/preprocessing interface.
3. Fixed Gabor filter bank:
   - 7 scales
   - 6 orientations: 0°, 30°, 60°, 90°, 120°, 150°
4. Visual Conformer:
   - ResNet/CNN branch
   - ViT/Transformer branch
   - Feature Coupling Unit
   - classifier head
   - feature extraction mode
5. KCCA feature fusion:
   - cosine kernel
   - RBF kernel
   - Laplacian kernel
   - cosine as default
6. Knowledge graph:
   - gender layer
   - hand-side layer
   - palm ID/template layer
7. Two-stage recognition.
8. Cosine similarity matching.
9. Accuracy, precision, recall, F1-score.
10. Timing benchmarks.

## Strict constraints

- Do not write a different palmprint method.
- Do not replace KCCA with concatenation.
- Do not skip knowledge graph.
- Do not replace Conformer with plain CNN or plain ViT.
- Do not use learnable Gabor filters as default.
- Do not invent ROI extraction as paper-specified.
- Do not treat soft biometrics as Conformer classifier labels.
- Do not train classifier on subject gender or hand side; train on palm ID/class ID.
- Do not hardcode one dataset's filename convention into the base dataset code.

## Assumptions policy

Where the paper lacks details, implement the most reasonable default but label it:

```text
IMPLEMENTATION ASSUMPTION
```

Every assumption must be configurable in YAML.

## Coding style

- Use PyTorch for deep learning.
- Use NumPy/SciPy/scikit-learn where appropriate for numerical features.
- Use type hints.
- Add docstrings that map modules to paper sections.
- Keep feature arrays and metadata aligned.
- Prefer deterministic behavior.
- Save all intermediate outputs.

## Required output quality

The repository must support:

```bash
python scripts/prepare_data.py --config configs/casia.yaml
python scripts/train_conformer.py --config configs/casia.yaml
python scripts/extract_gabor_features.py --config configs/casia.yaml
python scripts/extract_conformer_features.py --config configs/casia.yaml
python scripts/fit_kcca.py --config configs/casia.yaml
python scripts/build_knowledge_graph.py --config configs/casia.yaml
python scripts/evaluate.py --config configs/casia.yaml
python scripts/run_full_pipeline.py --config configs/casia.yaml
```

## Acceptance bar

The implementation is accepted only if:

- The full toy pipeline runs end-to-end.
- CASIA pipeline can run with real data when paths are supplied.
- KCCA model can be fit, saved, loaded, and used for test transform.
- Two-stage recognition returns same number of predictions as test samples.
- Evaluation reports all four paper metrics.
- Timing report includes Gabor, Conformer, KCCA, graph query, matching, total.
- Tests pass.
