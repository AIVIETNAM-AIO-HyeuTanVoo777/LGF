# Reviewer Attack Simulation

This document simulates a peer-review audit by anticipating and answering critical reviewer questions.

---

### 1. What is new if all components are known?
**Response:**
While individual metric-learning components (like BNNeck and ArcFace) are well-known, their transferability to contactless palmprint recognition under strict biometric constraints has not been systematically evaluated. This work is not an architectural proposal but a protocol study demonstrating that recognition-head gains observed on seen-identity diagnostic splits can fail to transfer under held-out palm-class cross-session conditions. By reporting this failure mode, the paper provides essential empirical guidelines for biometric component selection.

### 2. Why is this not just an internal ablation?
**Response:**
This study addresses a methodological issue in the palmprint literature where mismatched seen-identity protocols are frequently compared against held-out-class settings, leading to incorrect ranking claims. It elevates the evaluation protocol and metric policy (like conservative TAR@FAR) to first-class contributions. By showing how split design and target false-acceptance constraints reverse component conclusions, it offers a reproducible protocol benchmark for future palmprint evaluations.

### 3. How do you know there is no leakage?
**Response:**
We ran an automated split audit checking every generated partition for leakage. The audit verified that there is zero image-level overlap, zero palm-class overlap, and zero subject-ID overlap between development (train/validation) and held-out test (gallery/probe) partitions. Furthermore, all model checkpoints were selected using development validation splits only, and no test gallery or probe data was used in hyperparameter tuning or threshold calibration.

### 4. Why is the protocol palm-class-disjoint rather than subject-disjoint?
**Response:**
While the split audit verified that the subject-ID field in the database manifest has zero overlap between development and test partitions, the raw database metadata does not independently verify person-level identities beyond these text fields. Since a single subject can have left and right hands recorded as separate palm classes, and person-level verification is not externally audited, we conservatively claim the protocol as palm-class-disjoint. This prevents overclaiming person-level disjointness when only manifest-level label partitions are guaranteed.

### 5. How is TAR@FAR computed and why is it conservative?
**Response:**
TAR@FAR is computed by sweeping cosine score thresholds to construct the ROC curve. Under our conservative empirical-FAR rule, we select the threshold where the *empirical* false-accept rate is strictly less than or equal to the target FAR, and report the corresponding true-accept rate. This is conservative because it rejects the nearest-neighbor ROC interpolation fallback when the nearest point exceeds the target FAR, ensuring that the reported verification performance is never inflated by score-space quantization.

### 6. Are the results statistically significant?
**Response:**
To assess statistical significance over a small number of random seeds (n=3) and session directions (2), we computed paired differences over the six matched seed-direction units. While the EER degradation for M6 relative to M1 is highly consistent (sign-flip permutation test p=0.03125), the bootstrap confidence intervals for Rank-1 and TAR cross zero. We therefore describe the observed component rankings as directional empirical evidence and avoid claims of universal statistical superiority.

### 7. Why is IITD not cross-session evidence?
**Response:**
The IIT Delhi (IITD) database version 1.0 contains only within-session images, with all samples recorded in a single session. Consequently, we cannot construct cross-session S1->S2 or S2->S1 partitions for this dataset. We explicitly label the IITD results as within-session secondary validation to ensure the reviewer is not misled into thinking it represents cross-session generalization.

### 8. Why are prior palmprint methods not directly compared?
**Response:**
Direct comparisons against prior published palmprint methods (such as PalmNet or CompNet) are omitted because they were evaluated under seen-identity or non-audited within-session splits. Comparing our models under a strict palm-class-disjoint cross-session protocol against prior metrics reported under looser seen-identity splits would create a false leaderboard. We focus instead on isolating component-level effects under controlled, identical split and verification policies.

### 9. Why is fixed Gabor included?
**Response:**
The fixed Gabor texture baseline is included as a protocol-normalized classical baseline to contextualize deep learning representations under the same splits and gallery/probe rules. It uses an eight-orientation Gabor filter bank with average pooling and cosine matching, requiring no learned checkpoint. The results show that while classical Gabor features can be highly competitive for Rank-1 identification (92.99%), they are substantially weaker than deep learning representations in the strict low-FAR verification regime (34.38% TAR@FAR=10^-3).

### 10. What claim remains if BNNeck+ArcFace does not improve?
**Response:**
The remaining scientific claim is methodological and diagnostic: it establishes that standard recognition components imported from face recognition do not yield protocol-invariant performance improvements for palmprint embeddings. It demonstrates that component behavior is highly direction-dependent across acquisition sessions, and that Rank-1 identification accuracy does not explain low-FAR verification behavior. This shifts the focus of the paper from claiming a new "best method" to providing a rigorous, audited framework for protocol-sensitive biometric evaluation.
