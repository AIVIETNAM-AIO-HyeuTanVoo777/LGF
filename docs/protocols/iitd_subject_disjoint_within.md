# IITD Subject-Disjoint Within-Dataset Protocol

This document defines the subject-disjoint within-dataset evaluation protocol for the IITD dataset.

## 1. Protocol Clarification
Unlike the Tongji dataset, the IITD dataset does not provide distinct multi-session metadata or timestamps indicating separate sessions. Therefore:
- **Terminology**: We **do not** call the IITD evaluation "cross-session".
- **Nature**: It is strictly a **subject-disjoint within-dataset** protocol.
- **Role**: It acts as a secondary validation protocol to test the generalization of protocol sensitivity.

---

## 2. Subject-Disjoint Partitions
The identities in the dataset are divided into disjoint partitions:
1. **Development Set (Train & Validation)**:
   - Contains a subset of subjects (e.g., 140 subjects out of 230).
   - Used for training and validation.
2. **Evaluation Set (Gallery & Probe)**:
   - Contains the remaining subjects (e.g., 90 subjects).
   - Used for testing.

**There is zero overlap in identities between development and evaluation partitions.**

---

## 3. Seed-Based Runs
To match the rigor of the primary Tongji evaluation, three seeds are used to partition the subjects:
* **Seed 42**
* **Seed 2026**
* **Seed 2705**

All results reported for IITD must average metrics across these three seeds.

---

## 4. Evaluation Scheme
Since there are no sessions, gallery and probe sets are constructed by splitting the images of the evaluation subjects:
- **Gallery**: A set of images per palm (e.g., first few images) from the evaluation subjects.
- **Probe**: The remaining images of the evaluation subjects.
- The precise gallery/probe split is controlled by the split configuration files.
