# Strict Tongji ROC/DET/Score Figure Summary

This file records reviewer-facing ROC, DET, and score-distribution figures for B1, B5, and B6 under the strict Tongji palm-class-disjoint protocol.

- Source run table: `docs/results/strict_tongji_ablation_runs.csv`.
- Source curves: per-run `roc.csv` files from the corresponding experiment directories.
- Source scores: per-run `scores.csv` files; each run has 12,000 genuine and 1,428,000 impostor pairs.
- Curves are seed-averaged by interpolating TPR onto a common log-spaced FPR grid.
- Histograms use all genuine scores and a deterministic impostor subsample of up to 50,000 impostor scores per seed to keep the plot readable.

## Generated figures

- `paper/figures/roc_tongji_b1_b5_b6_s1_to_s2.pdf`
- `paper/figures/det_tongji_b1_b5_b6_s1_to_s2.pdf`
- `paper/figures/score_hist_tongji_b1_b5_b6_s1_to_s2.pdf`
- `paper/figures/roc_tongji_b1_b5_b6_s2_to_s1.pdf`
- `paper/figures/det_tongji_b1_b5_b6_s2_to_s1.pdf`
- `paper/figures/score_hist_tongji_b1_b5_b6_s2_to_s1.pdf`

## Mean TPR on common grid

| Method | Direction | TPR@FPR=1e-2 | TPR@FPR=1e-3 | TPR@FPR=1e-4 |
|---|---|---:|---:|---:|
| B1 CE+SupCon | S1->S2 | 86.67 | 67.76 | 48.18 |
| B5 BNNeck+CE | S1->S2 | 89.08 | 74.92 | 57.20 |
| B6 BNNeck+ArcFace | S1->S2 | 86.09 | 68.97 | 49.16 |
| B1 CE+SupCon | S2->S1 | 90.50 | 75.57 | 58.28 |
| B5 BNNeck+CE | S2->S1 | 86.44 | 70.19 | 54.17 |
| B6 BNNeck+ArcFace | S2->S1 | 86.31 | 70.24 | 53.32 |
