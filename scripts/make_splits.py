import os
import json
import argparse
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser(description="Create protocol train/val/gallery/probe/support splits.")
    parser.add_argument("--manifest", type=str, default="data/metadata/manifest.csv", help="Path to manifest CSV.")
    parser.add_argument("--output_dir", type=str, default="data/splits", help="Directory to save split JSON files.")
    return parser.parse_args()

def to_records(df):
    return df[["path", "class_id"]].to_dict(orient="records")

def create_splits():
    args = parse_args()
    
    if not os.path.exists(args.manifest):
        raise FileNotFoundError(f"Manifest not found: {args.manifest}")
        
    df = pd.read_csv(args.manifest)
    os.makedirs(args.output_dir, exist_ok=True)
    
    # -------------------------------------------------------------
    # 1. tongji_s1_to_s2
    # -------------------------------------------------------------
    print("Creating tongji_s1_to_s2 split...")
    tongji_df = df[df["dataset"] == "Tongji"]
    
    train_s1 = []
    val_s1 = []
    gallery_s1 = []
    probe_s2 = []
    
    # Group by palm_id (class)
    for palm_id, group in tongji_df.groupby("palm_id"):
        # Sort by path to be deterministic
        group = group.sort_values("path")
        
        # Session 1 images
        s1_group = group[group["session"] == "session1"]
        # Session 2 images
        s2_group = group[group["session"] == "session2"]
        
        s1_records = s1_group.to_dict(orient="records")
        s2_records = s2_group.to_dict(orient="records")
        
        # Split Session 1 into 8 train / 2 val
        train_s1.extend(s1_records[:8])
        val_s1.extend(s1_records[8:])
        
        # Gallery is all of Session 1
        gallery_s1.extend(s1_records)
        
        # Probe is all of Session 2
        probe_s2.extend(s2_records)
        
    split_s1_to_s2 = {
        "train": [{"path": r["path"], "class_id": int(r["class_id"])} for r in train_s1],
        "val": [{"path": r["path"], "class_id": int(r["class_id"])} for r in val_s1],
        "gallery": [{"path": r["path"], "class_id": int(r["class_id"])} for r in gallery_s1],
        "probe": [{"path": r["path"], "class_id": int(r["class_id"])} for r in probe_s2],
        "support": []
    }
    
    with open(os.path.join(args.output_dir, "tongji_s1_to_s2.json"), "w") as f:
        json.dump(split_s1_to_s2, f, indent=4)
        
    # -------------------------------------------------------------
    # 2. tongji_s2_to_s1
    # -------------------------------------------------------------
    print("Creating tongji_s2_to_s1 split...")
    train_s2 = []
    val_s2 = []
    gallery_s2 = []
    probe_s1 = []
    
    for palm_id, group in tongji_df.groupby("palm_id"):
        group = group.sort_values("path")
        s1_group = group[group["session"] == "session1"]
        s2_group = group[group["session"] == "session2"]
        
        s1_records = s1_group.to_dict(orient="records")
        s2_records = s2_group.to_dict(orient="records")
        
        # Split Session 2 into 8 train / 2 val
        train_s2.extend(s2_records[:8])
        val_s2.extend(s2_records[8:])
        
        # Gallery is all of Session 2
        gallery_s2.extend(s2_records)
        
        # Probe is all of Session 1
        probe_s1.extend(s1_records)
        
    split_s2_to_s1 = {
        "train": [{"path": r["path"], "class_id": int(r["class_id"])} for r in train_s2],
        "val": [{"path": r["path"], "class_id": int(r["class_id"])} for r in val_s2],
        "gallery": [{"path": r["path"], "class_id": int(r["class_id"])} for r in gallery_s2],
        "probe": [{"path": r["path"], "class_id": int(r["class_id"])} for r in probe_s1],
        "support": []
    }
    
    with open(os.path.join(args.output_dir, "tongji_s2_to_s1.json"), "w") as f:
        json.dump(split_s2_to_s1, f, indent=4)

    # -------------------------------------------------------------
    # 3. iitd_within
    # -------------------------------------------------------------
    print("Creating iitd_within split...")
    iitd_df = df[df["dataset"] == "IITD"]
    
    train_iitd = []
    val_iitd = []
    gallery_iitd = []
    probe_iitd = []
    
    for palm_id, group in iitd_df.groupby("palm_id"):
        group = group.sort_values("path")
        records = group.to_dict(orient="records")
        n = len(records)
        
        if n >= 3:
            train_iitd.extend(records[:n-2])
            val_iitd.append(records[n-2])
            gallery_iitd.extend(records[:n-2])
            probe_iitd.append(records[n-1])
        elif n == 2:
            train_iitd.append(records[0])
            val_iitd.append(records[1])
            gallery_iitd.append(records[0])
            probe_iitd.append(records[1])
        else:
            train_iitd.extend(records)
            val_iitd.extend(records)
            gallery_iitd.extend(records)
            probe_iitd.extend(records)
            
    split_iitd_within = {
        "train": [{"path": r["path"], "class_id": int(r["class_id"])} for r in train_iitd],
        "val": [{"path": r["path"], "class_id": int(r["class_id"])} for r in val_iitd],
        "gallery": [{"path": r["path"], "class_id": int(r["class_id"])} for r in gallery_iitd],
        "probe": [{"path": r["path"], "class_id": int(r["class_id"])} for r in probe_iitd],
        "support": []
    }
    
    with open(os.path.join(args.output_dir, "iitd_within.json"), "w") as f:
        json.dump(split_iitd_within, f, indent=4)

    # -------------------------------------------------------------
    # 4. cross_dataset_fewshot
    # -------------------------------------------------------------
    print("Creating cross_dataset_fewshot split...")
    # Train/Val: Tongji Session 1 (same as tongji_s1_to_s2)
    # Support: 2 images per IITD palm_id
    # Probe: Remaining images of IITD palm_id
    
    train_cross = []
    val_cross = []
    
    for palm_id, group in tongji_df.groupby("palm_id"):
        group = group.sort_values("path")
        s1_group = group[group["session"] == "session1"]
        s1_records = s1_group.to_dict(orient="records")
        train_cross.extend(s1_records[:8])
        val_cross.extend(s1_records[8:])
        
    support_cross = []
    probe_cross = []
    
    for palm_id, group in iitd_df.groupby("palm_id"):
        group = group.sort_values("path")
        records = group.to_dict(orient="records")
        n = len(records)
        
        # 2-shot support
        if n >= 2:
            support_cross.extend(records[:2])
            probe_cross.extend(records[2:])
        else:
            support_cross.extend(records)
            probe_cross.extend(records)
            
    split_cross = {
        "train": [{"path": r["path"], "class_id": int(r["class_id"])} for r in train_cross],
        "val": [{"path": r["path"], "class_id": int(r["class_id"])} for r in val_cross],
        "gallery": [{"path": r["path"], "class_id": int(r["class_id"])} for r in support_cross], # Gallery is the support set
        "probe": [{"path": r["path"], "class_id": int(r["class_id"])} for r in probe_cross],
        "support": [{"path": r["path"], "class_id": int(r["class_id"])} for r in support_cross]
    }
    
    with open(os.path.join(args.output_dir, "cross_dataset_fewshot.json"), "w") as f:
        json.dump(split_cross, f, indent=4)
        
    print("All splits created successfully.")

if __name__ == "__main__":
    create_splits()
