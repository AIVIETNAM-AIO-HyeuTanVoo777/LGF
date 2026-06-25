# Fixed Gabor Strict Tongji Baseline

This report adds a palmprint-specific fixed Gabor texture reference baseline under the same audited strict Tongji gallery/probe splits.

- The baseline uses deterministic Gabor magnitude features over segmented 128x128 images.
- The feature standardizer is fit on the training partition only for each seed-direction split.
- No learned checkpoint, experiment tensor, or score file is written.
- This is not a reimplementation of PalmNet, CompNet, or Competitive Code; it is a protocol-normalized classical texture reference point.

| Method | Role | n | Rank-1 | EER | TAR@FAR=1e-3 |
|---|---|---:|---:|---:|---:|
| Fixed Gabor texture | Palmprint-specific classical reference | 6 | 92.99 +/- 1.01 | 9.61 +/- 0.52 | 34.38 +/- 8.66 |
| B1 CE+SupCon | Learned baseline | 6 | 93.39 +/- 3.27 | 4.25 +/- 0.72 | 71.77 +/- 7.32 |
| B5 BNNeck+CE | Highest observed strict variant | 6 | 93.82 +/- 1.42 | 4.72 +/- 0.56 | 72.65 +/- 4.57 |
| B6 BNNeck+ArcFace | Hypothesized BNNeck+ArcFace variant | 6 | 92.21 +/- 1.68 | 5.27 +/- 0.45 | 69.71 +/- 4.23 |
