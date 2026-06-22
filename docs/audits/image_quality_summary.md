# Image Quality Summary

This document presents a quality analysis of the palmprint images in the dataset manifest.

- **Total Images Checked**: 14601
- **Corrupt Images Count**: 0
- **OpenCV Used**: True (Laplacian Variance)
- **Total Outliers Flagged**: 74

## Global Statistics (Valid Images)

- **Average Width**: 131.92 pixels
- **Average Height**: 131.92 pixels
- **Average Intensity Mean**: 139.66 (0-255)
- **Average Intensity Std**: 21.21
- **Average Near-Black Pixels**: 0.03%
- **Average Near-White Pixels**: 0.06%
- **Average Sharpness/Blur Score**: 142.04

## Dataset-wise Quality Breakdown

### Dataset: `IITD`

- **Total Images**: 2601
- **Corrupt Images**: 0
- **Avg Size**: 150.0 x 150.0
- **Avg Intensity Mean**: 174.77
- **Avg Intensity Std**: 37.25
- **Avg Sharpness Score**: 669.60

### Dataset: `Tongji`

- **Total Images**: 12000
- **Corrupt Images**: 0
- **Avg Size**: 128.0 x 128.0
- **Avg Intensity Mean**: 132.05
- **Avg Intensity Std**: 17.73
- **Avg Sharpness Score**: 27.69

## Quality Outliers & Potential Issues

Outliers have been compiled and exported to `docs/audits/image_quality_outliers.csv`. Issues checked include:
1. **Corrupt / unreadable image files**
2. **Extreme exposure** (Mean intensity < 15 or > 240)
3. **Flat/no-contrast images** (Std intensity < 5)
4. **Severe blurriness** (Bottom 0.5% lowest sharpness scores per dataset)
