# Biometric Evaluation Metrics

This document defines the mathematical and conceptual definitions of the metrics used to evaluate palmprint recognition performance in this project.

## 1. Feature Representation & Similarity
All models extract a 1D embedding vector $x \in \mathbb{R}^d$ for each palmprint image.
- **Normalization**: Embeddings are $L_2$-normalized: 
  $$\hat{x} = \frac{x}{\|x\|_2}$$
- **Similarity Measure**: Cosine similarity is computed between normalized embeddings:
  $$S(\hat{x}_1, \hat{x}_2) = \hat{x}_1^T \hat{x}_2$$

---

## 2. Identification Metrics (Closed-Set)
Closed-set identification assumes that the probe palm's identity is present in the gallery.
- **Rank-$k$ Accuracy**: The percentage of probe images for which the true matching identity is within the top-$k$ most similar gallery templates. We report **Rank-1** and **Rank-5** accuracy.
- **Macro-F1**: Calculated across all classes in the evaluation set to measure the class-balanced accuracy of the classification boundary.

---

## 3. Verification Metrics (Open-Set)
Verification determines if two palmprint images belong to the same palm (one-to-one matching).
- **Pairs Generation**:
  - **Genuine Pairs**: Match probe images against gallery images of the *same* palm.
  - **Impostor Pairs**: Match probe images against gallery images of *different* palms.
- **False Accept Rate (FAR)**: The ratio of impostor pairs incorrectly accepted as genuine matches:
  $$\text{FAR}(t) = \frac{\#\{\text{Impostor Similarities} \ge t\}}{\#\text{Total Impostor Pairs}}$$
- **False Reject Rate (FRR)**: The ratio of genuine pairs incorrectly rejected as impostor matches:
  $$\text{FRR}(t) = \frac{\#\{\text{Genuine Similarities} < t\}}{\#\text{Total Genuine Pairs}}$$
- **True Accept Rate (TAR)**: The complement of FRR:
  $$\text{TAR}(t) = 1 - \text{FRR}(t)$$
- **Equal Error Rate (EER)**: The error rate at the threshold $t_{\text{EER}}$ where FAR and FRR are equal:
  $$\text{FAR}(t_{\text{EER}}) = \text{FRR}(t_{\text{EER}}) = \text{EER}$$
- **TAR @ FAR**: The verification rate (TAR) at specific false acceptance rate constraints:
  - **TAR @ FAR = $10^{-2}$**
  - **TAR @ FAR = $10^{-3}$**

---

## 4. Aggregation Protocols
To present robust and unbiased summaries, we aggregate metrics as follows:
1. **Multi-Direction Aggregation (Tongji)**:
   - Run evaluation for $S1 \rightarrow S2$ and $S2 \rightarrow S1$.
   - Calculate performance for each direction separately.
2. **Multi-Seed Aggregation**:
   - Run experiments across seeds 42, 2026, and 2705.
   - For each metric, compute the mean and standard deviation (std) across all 3 seeds (and both directions for Tongji, resulting in 6 evaluation instances in total).
3. **Paired Delta Evaluation**:
   - When comparing a metric-learning variant (e.g. BNNeck + ArcFace) against a baseline (e.g. CE + SupCon), we compute the direct difference (Delta) for each seed/direction pair before averaging, highlighting the variance in improvement.
