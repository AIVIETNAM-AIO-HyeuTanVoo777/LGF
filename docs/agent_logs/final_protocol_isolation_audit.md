# Final Protocol Isolation Audit

This audit verifies that the evaluation protocol preserves strict information isolation between the development partitions (used for training and checkpoint selection) and the held-out test partitions (used for final metric reporting).

## 1. Split Audit
All 9 splits used in the evaluation (6 for Tongji, 3 for IITD) were re-audited.
- **Leakage Check**: Verified zero image-level overlap between train/val and gallery/probe partitions.
- **Identity Check**: Verified zero palm-class-ID and subject-ID overlap between development (train/val) and held-out test (gallery/probe) partitions.
- **Verdict**: **PASS** for all 9 splits.

## 2. Checkpoint Selection Audit
All 42 deep learning configurations (7 methods on Tongji across 3 seeds and 2 directions; 2 methods on IITD across 3 seeds) were re-audited.
- **Selection Policy**: Model checkpoints (`best.pt`) were selected using the validation split of the development palm classes only.
- **Test Isolation**: Verified that `uses_test_gallery_probe` is **False** for all 42 checkpoint selection events.
- **Verdict**: **PASS**. No checkpoint selection utilized any image or class from the held-out test gallery/probe sets.
