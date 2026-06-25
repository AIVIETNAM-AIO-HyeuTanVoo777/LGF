import os
import json
import hashlib
import pandas as pd
from pathlib import Path

# Paths
REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "data" / "metadata" / "palm_segmented_manifest.csv"
SPLIT_DIR = REPO_ROOT / "data" / "splits"
AUDIT_DIR = REPO_ROOT / "docs" / "audits"
REPRODUCIBILITY_DIR = REPO_ROOT / "docs" / "reproducibility"

# Create directories if they do not exist
AUDIT_DIR.mkdir(parents=True, exist_ok=True)
REPRODUCIBILITY_DIR.mkdir(parents=True, exist_ok=True)

def compute_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def normalize_path(p):
    return str(Path(p)).replace("\\", "/")

def get_item_path(x):
    if isinstance(x, str):
        return x
    if isinstance(x, dict):
        for k in ["path", "image_path", "filepath", "file"]:
            if k in x:
                return str(x[k])
    return None

def main():
    print("Starting dataset and split audit...")
    
    # 1. Audit Dataset Manifest
    if not MANIFEST_PATH.exists():
        print(f"Error: Manifest file not found at {MANIFEST_PATH}")
        return
        
    df = pd.read_csv(MANIFEST_PATH)
    df["norm_path"] = df["path"].apply(normalize_path)
    
    # Calculate manifest stats
    total_images = len(df)
    dataset_counts = df["dataset"].value_counts().to_dict()
    
    manifest_summary_content = f"""# Dataset Manifest Summary

This document summarizes the dataset metadata parsed from the official manifest.

- **Manifest Path**: `data/metadata/palm_segmented_manifest.csv`
- **Total Images**: {total_images}

## Images Per Dataset
"""
    for ds, count in dataset_counts.items():
        manifest_summary_content += f"- **{ds}**: {count} images\n"
        
    manifest_summary_content += "\n## Detailed Breakdown\n\n"
    
    # Breakdown by dataset, session, hand
    breakdown = df.groupby(["dataset", "session", "hand"]).size().reset_index(name="count")
    manifest_summary_content += "| Dataset | Session | Hand | Image Count |\n"
    manifest_summary_content += "|---------|---------|------|-------------|\n"
    for _, row in breakdown.iterrows():
        manifest_summary_content += f"| {row['dataset']} | {row['session']} | {row['hand']} | {row['count']} |\n"
        
    with open(AUDIT_DIR / "dataset_manifest_summary.md", "w", encoding="utf-8") as f:
        f.write(manifest_summary_content)
        
    print(f"Wrote dataset_manifest_summary.md to {AUDIT_DIR}")
    
    # 2. Audit Split Files
    split_files = sorted(list(SPLIT_DIR.glob("*subject_disjoint*.json")))
    if not split_files:
        print("Warning: No split files matching '*subject_disjoint*.json' found.")
        
    checksum_entries = []
    split_sizes_rows = []
    
    integrity_summary_content = """# Split Integrity Summary

This document provides verification results for all palm-class-disjoint split files, checking for duplicate paths, image existence, partition size, and identity leakage (overlap between development and test subsets).

"""
    
    path_to_row = {row["norm_path"]: row for _, row in df.iterrows()}
    
    for sf in split_files:
        filename = sf.name
        sha256 = compute_sha256(sf)
        checksum_entries.append((filename, sha256))
        
        with open(sf, "r", encoding="utf-8") as f:
            split_data = json.load(f)
            
        integrity_summary_content += f"## Split File: `{filename}`\n\n"
        integrity_summary_content += f"- **SHA256 Checksum**: `{sha256}`\n"
        
        partitions = ["train", "val", "gallery", "probe"]
        partition_stats = {}
        
        all_paths = []
        dev_subjects = set()
        dev_palms = set()
        dev_classes = set()
        
        test_subjects = set()
        test_palms = set()
        test_classes = set()
        
        duplicate_paths_found = 0
        missing_files_count = 0
        
        for part in partitions:
            if part not in split_data:
                integrity_summary_content += f"- [!] **Missing partition**: `{part}` not defined in JSON.\n"
                continue
                
            items = split_data[part]
            num_items = len(items)
            
            part_paths = []
            part_subjects = set()
            part_palms = set()
            part_classes = set()
            
            for item in items:
                p = get_item_path(item)
                if p:
                    np = normalize_path(p)
                    part_paths.append(np)
                    all_paths.append(np)
                    
                    # Verify physical existence
                    full_path = REPO_ROOT / np
                    if not full_path.exists():
                        missing_files_count += 1
                        
                # Extract identity fields
                for key_name, target_set in [("subject_id", part_subjects), ("palm_id", part_palms), ("class_id", part_classes)]:
                    if isinstance(item, dict) and key_name in item:
                        target_set.add(item[key_name])
                    elif np in path_to_row and key_name in path_to_row[np]:
                        target_set.add(path_to_row[np][key_name])
                        
            # Record sizes for CSV
            split_sizes_rows.append({
                "split_file": filename,
                "partition": part,
                "num_images": len(part_paths),
                "num_subjects": len(part_subjects),
                "num_palms": len(part_palms),
                "num_classes": len(part_classes)
            })
            
            partition_stats[part] = {
                "images": len(part_paths),
                "subjects": len(part_subjects),
                "palms": len(part_palms),
                "classes": len(part_classes)
            }
            
            if part in ["train", "val"]:
                dev_subjects.update(part_subjects)
                dev_palms.update(part_palms)
                dev_classes.update(part_classes)
            elif part in ["gallery", "probe"]:
                test_subjects.update(part_subjects)
                test_palms.update(part_palms)
                test_classes.update(part_classes)
                
        # Check path duplication
        total_paths_count = len(all_paths)
        unique_paths_count = len(set(all_paths))
        duplicate_paths_found = total_paths_count - unique_paths_count
        
        # Check overlap (identity leakage)
        overlap_subjects = dev_subjects & test_subjects
        overlap_palms = dev_palms & test_palms
        overlap_classes = dev_classes & test_classes
        
        # Write status for this file
        integrity_summary_content += "### Partition Sizes\n\n"
        integrity_summary_content += "| Partition | Images | Subjects | Palms | Classes |\n"
        integrity_summary_content += "|-----------|--------|----------|-------|---------|\n"
        for part in partitions:
            if part in partition_stats:
                stats = partition_stats[part]
                integrity_summary_content += f"| {part} | {stats['images']} | {stats['subjects']} | {stats['palms']} | {stats['classes']} |\n"
                
        integrity_summary_content += "\n### Security & Leakage Checks\n\n"
        if duplicate_paths_found > 0:
            integrity_summary_content += f"- [!] **Duplicate Paths**: Found {duplicate_paths_found} duplicate paths across splits.\n"
        else:
            integrity_summary_content += "- [x] **Duplicate Paths**: None found (passed).\n"
            
        if missing_files_count > 0:
            integrity_summary_content += f"- [!] **Missing Files**: {missing_files_count} paths referenced in JSON do not exist on disk.\n"
        else:
            integrity_summary_content += "- [x] **File Existence**: All referenced images exist on disk (passed).\n"
            
        if len(overlap_subjects) > 0:
            integrity_summary_content += f"- [!] **Manifest-field Leakage**: {len(overlap_subjects)} subjects overlap between Dev and Test partitions! Overlapping: {list(overlap_subjects)[:10]}\n"
        else:
            integrity_summary_content += "- [x] **Manifest-field Leakage**: 0 overlapping manifest identity fields across final partitions.\n"
            
        if len(overlap_palms) > 0:
            integrity_summary_content += f"- [!] **Palm Leakage**: {len(overlap_palms)} palms overlap between Dev and Test partitions!\n"
        else:
            integrity_summary_content += "- [x] **Palm Leakage**: 0 overlapping palms (passed).\n"
            
        if len(overlap_classes) > 0:
            integrity_summary_content += f"- [!] **Class Leakage**: {len(overlap_classes)} classes overlap between Dev and Test partitions!\n"
        else:
            integrity_summary_content += "- [x] **Class Leakage**: 0 overlapping classes (passed).\n"
            
        integrity_summary_content += "\n---\n\n"
        
    # Write docs/audits/split_integrity_summary.md
    with open(AUDIT_DIR / "split_integrity_summary.md", "w", encoding="utf-8") as f:
        f.write(integrity_summary_content)
    print(f"Wrote split_integrity_summary.md to {AUDIT_DIR}")
    
    # Write docs/audits/split_sizes.csv
    sizes_df = pd.DataFrame(split_sizes_rows)
    sizes_df.to_csv(AUDIT_DIR / "split_sizes.csv", index=False)
    print(f"Wrote split_sizes.csv to {AUDIT_DIR}")
    
    # Write docs/reproducibility/split_checksums.md
    checksum_content = "# Split Checksums\n\nThis document records the SHA256 checksums of the split files for reproducibility verification.\n\n| File Name | SHA256 Checksum |\n|---|---|\n"
    for filename, sha256 in checksum_entries:
        checksum_content += f"| `{filename}` | `{sha256}` |\n"
        
    with open(REPRODUCIBILITY_DIR / "split_checksums.md", "w", encoding="utf-8") as f:
        f.write(checksum_content)
    print(f"Wrote split_checksums.md to {REPRODUCIBILITY_DIR}")

if __name__ == "__main__":
    main()
