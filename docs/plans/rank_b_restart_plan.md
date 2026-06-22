# Rank-B Restart Plan: Protocol-Sensitive Palmprint Evaluation

This document outlines the strategic pivot and implementation plan to restart the project from scratch, positioning it for a Rank-B conference publication.

## 1. New Core Thesis

The project is repositioned from a **"method paper"** (claiming universal improvement of a specific model configuration, e.g., BNNeck + ArcFace) to a **"protocol-sensitive benchmark/evaluation paper"** for subject-disjoint cross-session palmprint recognition.

### Key Conceptual Shifts:
- **No SOTA Claims**: We do not claim state-of-the-art performance or universal superiority of any investigated variant.
- **Protocol Sensitivity**: We show that standard deep biometric pipeline components (like BNNeck + ArcFace, designated as candidate B6) perform well on standard "seen-identity" protocols but fail to show consistent or universal improvement under stricter, more realistic "subject-disjoint" protocols.
- **Primary Evidence**: The **Tongji** dataset is our primary evidence because it supports a true cross-session protocol (S1 -> S2 and S2 -> S1) under subject-disjoint splits.
- **Secondary Validation**: The **IITD** dataset is used as secondary validation for subject-disjoint within-dataset evaluation (no multi-session metadata is available).
- **Training from Scratch**: All models in the final matrix will be retrained from scratch under the documented protocols to ensure full reproducibility.

---

## 2. Dataset Roles & Protocols

### Primary: Tongji Dataset
- **Protocol**: Subject-disjoint cross-session.
- **Directions**: $S1 \rightarrow S2$ and $S2 \rightarrow S1$.
- **Setup**:
  - Development set (train/validation) is disjoint in identities from the test set (gallery/probe).
  - Seed-controlled splits (Seeds: 42, 2026, 2705) to ensure statistical significance.
  - Zero identity leakage between development and test.

### Secondary: IITD Dataset
- **Protocol**: Subject-disjoint within-dataset validation.
- **Setup**:
  - Identities split into disjoint development and evaluation partitions.
  - Seeds: 42, 2026, 2705.
  - Used as validation to assess whether protocol-sensitivity holds across different acquisition setups.

---

## 3. Minimal Experiment Matrix

To provide comprehensive evidence, we evaluate a structured set of methods across both datasets, all seeds, and directions:

### Methods/Variants:
1. **ResNet18 + CE** (Base classification baseline)
2. **ResNet18 + CE + SupCon** (Base classification + Supervised Contrastive Loss)
3. **ResNet18 + ArcFace** (Standard angular margin softmax)
4. **ResNet18 + BNNeck + CE** (Classification with Batch Normalization Neck)
5. **ResNet18 + BNNeck + ArcFace** (Metric learning candidate variant, previously B6)
6. **ResNet18 + BNNeck + ArcFace + SupCon** (Hybrid representation learning candidate)

### Evaluation Metrics:
- **Identification**: Rank-1, Rank-5 accuracy, Macro-F1.
- **Verification**: EER (Equal Error Rate), TAR @ FAR = $10^{-2}$, TAR @ FAR = $10^{-3}$.
- Cosine similarity computed on L2-normalized embeddings.

---

## 4. Execution Workflow

1. **Audit Splits and Data**: Validate that no subject ID overlap exists in any split json files.
2. **Standardize Configurations**: Maintain YAML templates for all 6 methods above.
3. **Train & Evaluate**: Run multi-seed, multi-direction trials for both Tongji and IITD.
4. **Aggregate**: Use structured scripts to parse metrics and write summary tables directly to `docs/results/`.
5. **LaTeX Updates**: Revise all text in `paper/` to replace method superiority claims with protocol-sensitivity findings.
