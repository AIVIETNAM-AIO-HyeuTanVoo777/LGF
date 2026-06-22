# Tongji Subject-Disjoint Cross-Session Protocol

This document defines the subject-disjoint cross-session evaluation protocol for the Tongji dataset.

## 1. Dataset Overview
The Tongji dataset contains palmprint images collected in two separate sessions (Session 1 and Session 2) from 800 palms (400 subjects, 2 palms per subject: left and right). Each palm has 10 images per session, resulting in $800 \times 10 = 8000$ images per session, and $16000$ images in total.

---

## 2. Subject-Disjoint Partitions
To avoid identity leakage and ensure realistic validation:
1. **Development Set (Train & Validation)**:
   - Contains a subset of subjects (e.g., 480 palms/240 subjects).
   - Used for training and validation tuning.
2. **Evaluation Set (Gallery & Probe)**:
   - Contains the remaining subjects (e.g., 320 palms/160 subjects).
   - Used only for generating gallery and probe templates.
   
**Crucially, there is absolutely zero overlap in subject/palm identities between the development set and the evaluation set.**

---

## 3. Session-Disjoint Cross-Session Directions
Biometric matching is evaluated across separate acquisition sessions:
* **S1 -> S2**:
  - **Gallery**: Session 1 images of evaluation subjects.
  - **Probe**: Session 2 images of evaluation subjects.
* **S2 -> S1**:
  - **Gallery**: Session 2 images of evaluation subjects.
  - **Probe**: Session 1 images of evaluation subjects.

---

## 4. Seeds and Reproducibility
To ensure statistical robustness and eliminate random split bias, the partitions are generated using three pre-selected seeds:
* **Seed 42**
* **Seed 2026**
* **Seed 2705**

For each seed, the subjects are randomly shuffled and assigned to development/evaluation sets, ensuring identical partitions across all compared methods.

---

## 5. Gallery and Probe Construction Details
Within the evaluation partition:
- **Gallery**: For the source session, a fixed number of images per palm (typically all 10 images or a representative subset) are stored as reference templates.
- **Probe**: All images from the target session of the evaluation subjects are matched against the gallery.
- Similarity matches are computed using **Cosine Similarity** on L2-normalized embeddings.
