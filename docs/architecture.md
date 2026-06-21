# PFFR Architecture & Module Specifications

This document outlines the software design, module boundaries, and execution logic of the **Palmprint Features Fusion Recognition** (PFFR) system.

---

## 1. System Architecture

The pipeline consists of the following components:

```mermaid
graph TD
    A[Input ROI Image] --> B[Gabor Branch]
    A --> C[Conformer Branch]
    B -->|7x6 orientations| D[Max orientation fusion & scale concat]
    C -->|ViT + ResNet + FCUs| E[Penultimate Deep Features]
    D --> F[Regularized KCCA Fusion]
    E --> F
    F -->|Fused features| G[Knowledge Graph Pre-classification]
    G -->|Candidate list filtering| H[Cosine Similarity Matcher]
    H --> I[Predicted Palm ID]
```

---

## 2. Module Specifications

### `palmrec/datasets`
Handles metadata CSV building, metadata normalization, and deterministic split generation (1:1 split, dropping odd samples per palm class).

### `palmrec/preprocessing`
Responsible for grayscaling/resizing images to $224 \times 224$ for the Gabor branch, and resizing/channel transposing/standard normalizations for the Conformer branch.

### `palmrec/features`
Extracted feature vector managers:
- Gabor filter bank convolution and orientations maximum pooling.
- normalizers caching feature vectors to `.npz`.

### `palmrec/models`
Visual Conformer PyTorch architecture implementation, coupling ResNet convolutional streams with ViT attention streams through Feature Coupling Units (FCUs).

### `palmrec/fusion`
Regularized Kernel CCA fitting and transformation, centering kernel matrices and projecting high-dimensional descriptors to canonical spaces.

### `palmrec/matching`
Knowledge Graph structural partitions, implementing two-stage candidate search and Cosine similarity threshold matching.
