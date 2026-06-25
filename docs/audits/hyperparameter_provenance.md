# Hyperparameter Provenance

This document records the provenance and validation status of all hyperparameters used in our study. None of these parameters were optimized or tuned using the held-out test gallery/probe partitions.

| Parameter | Value | Source | Selected using test? | Notes |
|---|---|---|---|---|
| ArcFace scale | 30.0 | Literature / Project Default | no | Not tuned on held-out test |
| ArcFace margin | 0.5 | Literature / Project Default | no | Not tuned on held-out test |
| SupCon lambda | 0.10 | Project Default / Dev Validation | no | Retained across comparative runs for fair evaluation |
| Learning rate | 0.0001 | Standard practice / Dev Validation | no | Hand-selected; not tuned on held-out test |
| Weight decay | 0.0001 | Standard regularization | no | Fixed project default |
| Embedding dimension | 256 | Project Default | no | Fixed across all learned variants |
| Training epochs | 60 | Training recipe policy | no | Sufficient convergence observed on development train |
| Gradient accumulation steps | 4 | Batch accumulation constraint | no | Configured to fit GPU memory constraints |
| Identities/Instances | 8/2 | Sampler policy | no | Set for SupCon identity/instance composition |
| Optimizer | Adam | Standard deep learning choice | no | Fixed project default |
| Scheduler | CosineAnnealingLR | Standard policy | no | Retained for learning rate decay |
