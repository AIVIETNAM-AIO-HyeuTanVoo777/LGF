# Audit Policy

Audit-supported means deterministic checks are provided for split construction, gallery/probe construction, checkpoint-selection policy, metric-threshold handling, run manifests, and table-generation provenance.

The audits do not certify dataset identity beyond the fields available in the manifests. Wording should use palm-class-disjoint unless stronger identity evidence is independently verified.

Do not commit raw images, checkpoints, local run directories, score tensors, private paths, generated ZIPs, or LaTeX build artifacts. Public audit summaries belong in `audit_artifacts/`.
