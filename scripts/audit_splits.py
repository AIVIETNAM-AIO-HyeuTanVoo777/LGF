import os
import sys
import json
import hashlib
from pathlib import Path
import pandas as pd

ROOT = Path(".").resolve()

SPLIT_DIR = ROOT / "data" / "splits"
OUT_DIR = ROOT / "docs" / "audits"
OUT_CSV = OUT_DIR / "split_audit.csv"
OUT_MD = OUT_DIR / "split_audit.md"
OUT_GP_MD = OUT_DIR / "gallery_probe_audit.md"

def stable_json_hash(path):
    with open(path, 'r', encoding='utf-8') as f:
        obj = json.load(f)
    payload = json.dumps(obj, sort_keys=True, separators=(',', ':')).encode('utf-8')
    return hashlib.sha256(payload).hexdigest()[:12]

def infer_info(filename):
    name = filename.lower()
    
    # Check dataset
    if "tongji" in name:
        dataset = "Tongji"
    elif "iitd" in name:
        dataset = "IITD"
    elif "toy" in name:
        dataset = "Toy"
    else:
        dataset = "Unknown"
        
    # Check direction
    if "s1_to_s2" in name:
        direction = "s1_to_s2"
    elif "s2_to_s1" in name:
        direction = "s2_to_s1"
    elif "within" in name:
        direction = "within"
    else:
        direction = "unknown"
        
    # Check seed
    import re
    m = re.search(r"seed(\d+)", name)
    if m:
        seed = m.group(1)
    else:
        seed = "N/A"
        
    return dataset, direction, seed

def normalize_partition(part):
    out = []
    for item in part:
        if isinstance(item, str):
            # Parse session from path if possible
            sess = "unknown"
            if "session1" in item.lower():
                sess = "session1"
            elif "session2" in item.lower():
                sess = "session2"
            out.append({
                "path": item,
                "class_id": "unknown",
                "palm_id": "unknown",
                "subject_id": "unknown",
                "session": sess
            })
        else:
            out.append(item)
    return out

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    
    split_paths = sorted(
        list(SPLIT_DIR.glob("tongji_subject_disjoint_s*_to_s*_seed*.json")) +
        list(SPLIT_DIR.glob("iitd_subject_disjoint_within_seed*.json"))
    )
    
    rows = []
    gp_rows = []
    
    for path in split_paths:
        filename = path.name
        dataset, direction, seed = infer_info(filename)
        
        split_hash = stable_json_hash(path)
        
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        train = normalize_partition(data.get("train", []))
        val = normalize_partition(data.get("val", []))
        gallery = normalize_partition(data.get("gallery", []))
        probe = normalize_partition(data.get("probe", []))
        
        # Get path sets
        train_paths = set(item["path"] for item in train)
        val_paths = set(item["path"] for item in val)
        gallery_paths = set(item["path"] for item in gallery)
        probe_paths = set(item["path"] for item in probe)
        
        dev_paths = train_paths | val_paths
        test_paths = gallery_paths | probe_paths
        
        # Image overlap checks
        img_dev_test_overlap = len(dev_paths & test_paths)
        img_gp_overlap = len(gallery_paths & probe_paths)
        img_train_val_overlap = len(train_paths & val_paths)
        
        image_overlap = img_dev_test_overlap + img_gp_overlap
        
        # Class sets
        train_classes = set(item["class_id"] for item in train)
        val_classes = set(item["class_id"] for item in val)
        gallery_classes = set(item["class_id"] for item in gallery)
        probe_classes = set(item["class_id"] for item in probe)
        
        dev_classes = train_classes | val_classes
        test_classes = gallery_classes | probe_classes
        
        class_overlap = len(dev_classes & test_classes)
        
        # Palm and Subject fields
        train_palms = set(item.get("palm_id") for item in train if item.get("palm_id") is not None)
        val_palms = set(item.get("palm_id") for item in val if item.get("palm_id") is not None)
        gallery_palms = set(item.get("palm_id") for item in gallery if item.get("palm_id") is not None)
        probe_palms = set(item.get("palm_id") for item in probe if item.get("palm_id") is not None)
        
        dev_palms = train_palms | val_palms
        test_palms = gallery_palms | probe_palms
        palm_id_overlap = len(dev_palms & test_palms)
        
        train_subjects = set(item.get("subject_id") for item in train if item.get("subject_id") is not None)
        val_subjects = set(item.get("subject_id") for item in val if item.get("subject_id") is not None)
        gallery_subjects = set(item.get("subject_id") for item in gallery if item.get("subject_id") is not None)
        probe_subjects = set(item.get("subject_id") for item in probe if item.get("subject_id") is not None)
        
        dev_subjects = train_subjects | val_subjects
        test_subjects = gallery_subjects | probe_subjects
        subject_overlap = len(dev_subjects & test_subjects)
        
        # Class support checks
        if len(probe_classes) > 0:
            every_probe_class_has_gallery_support = "yes" if probe_classes.issubset(gallery_classes) else "no"
        else:
            every_probe_class_has_gallery_support = "N/A"
            
        if len(gallery_classes) > 0:
            every_gallery_class_has_probe_support = "yes" if gallery_classes.issubset(probe_classes) else "no"
        else:
            every_gallery_class_has_probe_support = "N/A"
            
        # Direction matching session checks
        direction_mismatch = False
        gallery_sessions = set(item.get("session") for item in gallery if item.get("session") is not None)
        probe_sessions = set(item.get("session") for item in probe if item.get("session") is not None)
        
        if direction == "s1_to_s2":
            if not (gallery_sessions <= {"session1"} and probe_sessions <= {"session2"}):
                direction_mismatch = True
        elif direction == "s2_to_s1":
            if not (gallery_sessions <= {"session2"} and probe_sessions <= {"session1"}):
                direction_mismatch = True
                
        # Exclude legacy/toy splits from final study verdict if they do not meet our criteria
        is_official = filename.startswith("tongji_subject_disjoint_") or filename.startswith("iitd_subject_disjoint_")
        
        # Allowed claim
        if image_overlap > 0 or class_overlap > 0:
            claim_allowed = "invalid"
        else:
            claim_allowed = "palm-class-disjoint"
            
        # Verdict calculation
        passed = (
            image_overlap == 0 and 
            class_overlap == 0 and 
            every_probe_class_has_gallery_support == "yes" and 
            not direction_mismatch
        )
        verdict = "PASS" if passed else "FAIL"
        
        # Exclude non-official splits from forcing overall study failure, but record their result
        status_str = verdict
        if not is_official:
            status_str = f"FAIL (EXCLUDED)" if verdict == "FAIL" else "PASS (EXCLUDED)"
            
        rows.append({
            "dataset": dataset,
            "direction": direction,
            "seed": seed,
            "split file": filename,
            "split hash": split_hash,
            "train images": len(train),
            "val images": len(val),
            "gallery images": len(gallery),
            "probe images": len(probe),
            "development palm classes": len(dev_classes),
            "held-out palm classes": len(test_classes),
            "image overlap": image_overlap,
            "palm-class overlap": class_overlap,
            "palm-id overlap if available": palm_id_overlap,
            "manifest subject-field overlap if available": subject_overlap,
            "every probe class has gallery support? yes/no": every_probe_class_has_gallery_support,
            "every gallery class has probe support? yes/no": every_gallery_class_has_probe_support,
            "claim allowed": claim_allowed,
            "verdict": verdict
        })
        
        gp_rows.append({
            "split_file": filename,
            "gallery_images": len(gallery),
            "probe_images": len(probe),
            "gallery_classes": len(gallery_classes),
            "probe_classes": len(probe_classes),
            "every_probe_class_has_gallery_support": every_probe_class_has_gallery_support,
            "every_gallery_class_has_probe_support": every_gallery_class_has_probe_support,
            "direction_mismatch": str(direction_mismatch),
            "status": status_str
        })
        
    df_audit = pd.DataFrame(rows)
    df_audit.to_csv(OUT_CSV, index=False)
    print(f"Wrote {OUT_CSV}")
    
    # Write split_audit.md
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("# Split Audit Summary\n\n")
        f.write("This audit verifies dataset leakage, partition overlap, and class support across all splits.\n\n")
        f.write(df_audit.to_markdown(index=False))
        f.write("\n")
        
    print(f"Wrote {OUT_MD}")
    
    # Write gallery_probe_audit.md
    df_gp = pd.DataFrame(gp_rows)
    with open(OUT_GP_MD, "w", encoding="utf-8") as f:
        f.write("# Gallery/Probe Construction Audit\n\n")
        f.write("Detailed audit of gallery and probe partitions, class support, and session-direction verification.\n\n")
        f.write(df_gp.to_markdown(index=False))
        f.write("\n")
        
    print(f"Wrote {OUT_GP_MD}")

if __name__ == "__main__":
    main()
