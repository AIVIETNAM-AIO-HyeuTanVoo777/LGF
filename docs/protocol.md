# Protocol

The primary protocol is Tongji cross-session evaluation with two directions: S1->S2 and S2->S1. Each direction is evaluated over seeds 42, 2026, and 2705.

The active claim is palm-class-disjoint, based on deterministic split audits over image paths, class IDs, palm IDs, and available subject fields. The repository does not claim independently verified person-disjointness.

Training uses train and validation partitions only. Final evaluation uses held-out gallery/probe partitions. IITD is retained as secondary within-session validation and must not be described as cross-session evidence.

The main model variants are M0, M1, M2, M3, M4, M6, and M7. Configs are stored in `configs/rankb_final/`.
