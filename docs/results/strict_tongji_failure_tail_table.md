# Strict Tongji Failure/Tail Analysis

This table summarizes matched-seed score-tail deltas for B5 and B6 relative to B1 under the strict Tongji palm-class-disjoint protocol.

- Input run table: `docs/results/strict_tongji_ablation_runs.csv`.
- Source scores: per-run `scores.csv` files located next to each metrics file.
- Each strict Tongji run contains 12,000 genuine and 1,428,000 impostor comparisons.
- Deltas are averaged over three matched seeds within each session direction.
- Positive TAR deltas favor the first method; positive EER deltas are worse for the first method.
- Positive impostor-tail deltas indicate a higher high-score impostor tail, which is generally unfavorable at low FAR.

| Comparison | Direction | Delta genuine mean | Delta impostor q0.999 | Delta d-prime | Delta TAR@FAR=1e-3 (pp) | Interpretation |
|---|---:|---:|---:|---:|---:|---|
| B5 minus B1 | S1->S2 | -0.057 | -0.094 | -0.082 | +7.16 | BNNeck+CE improves low-FAR TAR in this direction. |
| B5 minus B1 | S2->S1 | -0.043 | -0.020 | -0.288 | -5.40 | BNNeck+CE gain does not transfer to the reverse direction. |
| B6 minus B1 | S1->S2 | -0.072 | -0.082 | -0.287 | +1.20 | BNNeck+ArcFace shows only direction-limited low-FAR behavior. |
| B6 minus B1 | S2->S1 | -0.063 | -0.043 | -0.399 | -5.33 | BNNeck+ArcFace degrades the reverse-direction low-FAR result. |
