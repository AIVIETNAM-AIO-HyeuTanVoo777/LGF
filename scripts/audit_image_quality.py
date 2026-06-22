import os
import csv
import pandas as pd
import numpy as np
from pathlib import Path
from PIL import Image

# Paths
REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "data" / "metadata" / "palm_segmented_manifest.csv"
OUTPUT_SUMMARY = REPO_ROOT / "docs" / "audits" / "image_quality_summary.md"
OUTPUT_OUTLIERS = REPO_ROOT / "docs" / "audits" / "image_quality_outliers.csv"

# Try importing OpenCV for Laplacian variance, else use numpy fallback
OPENCV_AVAILABLE = False
try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    pass

def compute_blur_score(img_np):
    """Compute sharpness score. If OpenCV is available, try Laplacian variance.
    Else, or if OpenCV fails, use the variance of the gradients in X and Y directions."""
    if OPENCV_AVAILABLE:
        try:
            # Try CV_32F first as it is more compatible and faster than CV_64F
            return cv2.Laplacian(img_np, cv2.CV_32F).var()
        except Exception:
            pass
            
    # Fallback: compute simple gradients variance
    grad_x = np.diff(img_np, axis=1)
    grad_y = np.diff(img_np, axis=0)
    return np.var(grad_x) + np.var(grad_y)

def analyze_image(filepath):
    """Analyzes an image and returns quality metrics."""
    try:
        with Image.open(filepath) as img:
            width, height = img.size
            # Convert to grayscale for metric computation
            img_gray = img.convert("L")
            img_np = np.array(img_gray, dtype=np.float32)
            
            mean_intensity = float(np.mean(img_np))
            std_intensity = float(np.std(img_np))
            
            # Near black/white percentages (pixel intensity < 10 or > 245)
            near_black_pct = float(np.mean(img_np < 10.0) * 100.0)
            near_white_pct = float(np.mean(img_np > 245.0) * 100.0)
            
            blur_score = float(compute_blur_score(img_np))
            
            return {
                "corrupt": False,
                "width": width,
                "height": height,
                "mean": mean_intensity,
                "std": std_intensity,
                "near_black_pct": near_black_pct,
                "near_white_pct": near_white_pct,
                "blur_score": blur_score
            }
    except Exception as e:
        return {
            "corrupt": True,
            "error_msg": str(e),
            "width": 0,
            "height": 0,
            "mean": 0.0,
            "std": 0.0,
            "near_black_pct": 0.0,
            "near_white_pct": 0.0,
            "blur_score": 0.0
        }

def main():
    print("Starting image quality audit...")
    if not MANIFEST_PATH.exists():
        print(f"Manifest path not found: {MANIFEST_PATH}")
        return
        
    df = pd.read_csv(MANIFEST_PATH)
    total_images = len(df)
    print(f"Found {total_images} images to audit in manifest.")
    
    records = []
    corrupt_count = 0
    
    # Process images
    # Since there are many images, let's report progress every 2000 images
    for idx, row in df.iterrows():
        img_rel_path = row["path"]
        img_abs_path = REPO_ROOT / img_rel_path
        
        if not img_abs_path.exists():
            records.append({
                "path": img_rel_path,
                "dataset": row["dataset"],
                "corrupt": True,
                "error_msg": "File does not exist on disk",
                "width": 0, "height": 0, "mean": 0.0, "std": 0.0,
                "near_black_pct": 0.0, "near_white_pct": 0.0, "blur_score": 0.0
            })
            corrupt_count += 1
            continue
            
        res = analyze_image(img_abs_path)
        res["path"] = img_rel_path
        res["dataset"] = row["dataset"]
        records.append(res)
        
        if res["corrupt"]:
            corrupt_count += 1
            
        if (idx + 1) % 2000 == 0 or (idx + 1) == total_images:
            print(f"Processed {idx + 1}/{total_images} images...")
            
    # Convert to DataFrame
    audit_df = pd.DataFrame(records)
    
    # Identify outliers
    # We define outliers as:
    # 1. Corrupt images
    # 2. Extreme mean intensity (mean < 15 or mean > 240)
    # 3. Very low variance/contrast (std < 5)
    # 4. Top 1% blurriest images (lowest blur scores per dataset)
    
    outliers_list = []
    
    # Extract corrupt
    corrupt_df = audit_df[audit_df["corrupt"] == True]
    outliers_list.append(corrupt_df)
    
    # Extract low contrast / extreme intensity
    extreme_df = audit_df[
        (audit_df["corrupt"] == False) & 
        ((audit_df["mean"] < 15.0) | (audit_df["mean"] > 240.0) | (audit_df["std"] < 5.0))
    ]
    outliers_list.append(extreme_df)
    
    # Low blur score per dataset (bottom 0.5% lowest blur_score)
    for dataset in audit_df["dataset"].unique():
        ds_df = audit_df[(audit_df["dataset"] == dataset) & (audit_df["corrupt"] == False)]
        if len(ds_df) > 0:
            threshold = ds_df["blur_score"].quantile(0.005)
            blurry_ds = ds_df[ds_df["blur_score"] <= threshold]
            outliers_list.append(blurry_ds)
            
    outliers_df = pd.concat(outliers_list).drop_duplicates(subset=["path"])
    outliers_df.to_csv(OUTPUT_OUTLIERS, index=False)
    print(f"Wrote outliers log to {OUTPUT_OUTLIERS}. Total outliers: {len(outliers_df)}")
    
    # Calculate global and per-dataset statistics
    valid_df = audit_df[audit_df["corrupt"] == False]
    
    summary_md = f"""# Image Quality Summary

This document presents a quality analysis of the palmprint images in the dataset manifest.

- **Total Images Checked**: {total_images}
- **Corrupt Images Count**: {corrupt_count}
- **OpenCV Used**: {OPENCV_AVAILABLE} ({"Laplacian Variance" if OPENCV_AVAILABLE else "Numpy Gradient Variance fallback"})
- **Total Outliers Flagged**: {len(outliers_df)}

## Global Statistics (Valid Images)

- **Average Width**: {valid_df['width'].mean():.2f} pixels
- **Average Height**: {valid_df['height'].mean():.2f} pixels
- **Average Intensity Mean**: {valid_df['mean'].mean():.2f} (0-255)
- **Average Intensity Std**: {valid_df['std'].mean():.2f}
- **Average Near-Black Pixels**: {valid_df['near_black_pct'].mean():.2f}%
- **Average Near-White Pixels**: {valid_df['near_white_pct'].mean():.2f}%
- **Average Sharpness/Blur Score**: {valid_df['blur_score'].mean():.2f}

## Dataset-wise Quality Breakdown

"""
    for ds in audit_df["dataset"].unique():
        ds_valid = valid_df[valid_df["dataset"] == ds]
        ds_all = audit_df[audit_df["dataset"] == ds]
        ds_corrupt = ds_all[ds_all["corrupt"] == True]
        
        summary_md += f"### Dataset: `{ds}`\n\n"
        summary_md += f"- **Total Images**: {len(ds_all)}\n"
        summary_md += f"- **Corrupt Images**: {len(ds_corrupt)}\n"
        
        if len(ds_valid) > 0:
            summary_md += f"- **Avg Size**: {ds_valid['width'].mean():.1f} x {ds_valid['height'].mean():.1f}\n"
            summary_md += f"- **Avg Intensity Mean**: {ds_valid['mean'].mean():.2f}\n"
            summary_md += f"- **Avg Intensity Std**: {ds_valid['std'].mean():.2f}\n"
            summary_md += f"- **Avg Sharpness Score**: {ds_valid['blur_score'].mean():.2f}\n"
        summary_md += "\n"
        
    summary_md += """## Quality Outliers & Potential Issues

Outliers have been compiled and exported to `docs/audits/image_quality_outliers.csv`. Issues checked include:
1. **Corrupt / unreadable image files**
2. **Extreme exposure** (Mean intensity < 15 or > 240)
3. **Flat/no-contrast images** (Std intensity < 5)
4. **Severe blurriness** (Bottom 0.5% lowest sharpness scores per dataset)
"""
    
    OUTPUT_SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_SUMMARY, "w", encoding="utf-8") as f:
        f.write(summary_md)
        
    print(f"Wrote image quality summary to {OUTPUT_SUMMARY}")

if __name__ == "__main__":
    main()
