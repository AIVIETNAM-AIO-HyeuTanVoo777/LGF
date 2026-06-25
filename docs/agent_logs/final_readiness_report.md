# Final Readiness Report

**Final Readiness Label**: `RANK-B READY`

## Justification
The repository has been thoroughly audited and upgraded to meet the rigorous standards of a Rank-B conference empirical/protocol study:

1. **Protocol Rigour**: Every split has been audited for image, class, and subject-ID leakage. All audits pass with zero overlap, and the splits are safely labeled manifest-level `palm-class-disjoint`.
2. **Metric Integrity**: A canonical, vectorized, conservative `conservative_tar_at_far` implementation has been deployed, tested, and utilized across all scripts. The threshold audit confirms that no empirical FAR exceeds the target FAR.
3. **Completed Experiment Matrix**: All required runs (M0–M7, including CosFace M3) have been evaluated, and their raw JSON files compiled. Gabor texture features are included as a protocol-normalized reference.
4. **Reproducibility**: YAML configurations, split audit logs, checkpoint-selection logs, score-tail diagnostics, and a comprehensive `reproducibility_manifest.md` are provided. The evaluation pipeline has been validated via local smoke tests.
5. **Calibrated Writing**: The paper title, abstract, sections (01–08), and conclusion have been rewritten to focus on protocol sensitivity, eliminating all SOTA claims and overconfident language. LaTeX tables are dynamically imported from generated files.
