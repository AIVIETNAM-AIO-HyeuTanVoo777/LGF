# Tongji Session Image-Quality Audit

This audit summarizes image-quality differences between Tongji session1 and session2 using the segmented manifest. It is intended to support interpretation of cross-session direction asymmetry, not to define a new evaluation metric.

- Manifest: `data\metadata\palm_segmented_manifest.csv`
- OpenCV used for Laplacian sharpness: `True`

## Session summary

| Session | Images | Mean intensity | Contrast/std | Sharpness | Near-black % | Near-white % |
|---|---:|---:|---:|---:|---:|---:|
| session1 | 6000 | 131.50+/-26.35 | 17.65+/-5.08 | 27.58+/-14.05 | 0.00 | 0.02 |
| session2 | 6000 | 132.59+/-22.40 | 17.80+/-4.41 | 27.79+/-12.94 | 0.00 | 0.00 |

## Session2 minus Session1 deltas

- Mean intensity delta: +1.09
- Contrast/std delta: +0.15
- Sharpness delta: +0.21

## Interpretation

- These statistics quantify acquisition/session differences in the segmented Tongji images.
- They do not by themselves prove the cause of model degradation, but they provide evidence that the two sessions are not image-quality identical.
- Directional performance asymmetry should therefore be interpreted together with these session-level image statistics.
