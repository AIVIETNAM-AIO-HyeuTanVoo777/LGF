import os
import glob
import pandas as pd
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Build manifest CSV for IITD and Tongji datasets.")
    parser.add_argument("--output", type=str, default="data/metadata/manifest.csv", help="Path to output manifest CSV.")
    return parser.parse_args()

def build_manifest():
    args = parse_args()
    
    records = []
    
    # --- Process IITD ---
    print("Processing IITD dataset...")
    iitd_pattern = os.path.join("data", "segmented", "IITD", "*", "*.bmp")
    iitd_files = glob.glob(iitd_pattern)
    print(f"Found {len(iitd_files)} IITD files.")
    
    for file_path in iitd_files:
        # Convert path to use forward slashes for cross-platform compatibility
        rel_path = os.path.relpath(file_path).replace("\\", "/")
        parts = rel_path.split("/")
        
        # Expected parts: ['data', 'segmented', 'IITD', 'Left' or 'Right', 'filename.bmp']
        if len(parts) < 5:
            continue
            
        hand = parts[3]  # Left or Right
        filename = parts[4]
        filename_stem, _ = os.path.splitext(filename)
        
        # IITD filename: 001_1.bmp
        # Let's split by '_' to get subject_id and sample index
        sub_parts = filename_stem.split("_")
        if len(sub_parts) < 2:
            continue
            
        subject_id = sub_parts[0]
        # label class is dataset + hand + subject_id
        palm_id = f"IITD_{hand}_{subject_id}"
        sample_id = f"IITD_session1_{hand}_{filename_stem}"
        
        records.append({
            "path": rel_path,
            "dataset": "IITD",
            "session": "session1",
            "hand": hand,
            "subject_id": subject_id,
            "palm_id": palm_id,
            "sample_id": sample_id
        })
        
    # --- Process Tongji ---
    print("Processing Tongji dataset...")
    tongji_pattern = os.path.join("data", "segmented", "Tongji", "*", "*.bmp")
    tongji_files = glob.glob(tongji_pattern)
    print(f"Found {len(tongji_files)} Tongji files.")
    
    for file_path in tongji_files:
        rel_path = os.path.relpath(file_path).replace("\\", "/")
        parts = rel_path.split("/")
        
        # Expected parts: ['data', 'segmented', 'Tongji', 'session1' or 'session2', 'filename.bmp']
        if len(parts) < 5:
            continue
            
        session = parts[3]  # session1 or session2
        filename = parts[4]
        filename_stem, _ = os.path.splitext(filename)
        
        try:
            val = int(filename_stem)
        except ValueError:
            continue
            
        # Tongji: 00001~00010 is palm 1, 00011~00020 is palm 2, etc.
        palm_idx = (val - 1) // 10 + 1
        subject_id = f"{palm_idx:05d}"
        hand = "none"
        palm_id = f"Tongji_{subject_id}"
        sample_id = f"Tongji_{session}_{hand}_{filename_stem}"
        
        records.append({
            "path": rel_path,
            "dataset": "Tongji",
            "session": session,
            "hand": hand,
            "subject_id": subject_id,
            "palm_id": palm_id,
            "sample_id": sample_id
        })
        
    if not records:
        print("No records found! Please check the dataset paths.")
        return
        
    # Create DataFrame
    df = pd.DataFrame(records)
    
    # Assign class_id: sort palm_id and map to integers
    unique_palms = sorted(df["palm_id"].unique())
    palm_to_class = {palm: idx for idx, palm in enumerate(unique_palms)}
    df["class_id"] = df["palm_id"].map(palm_to_class)
    
    # Reorder columns as requested:
    # path,dataset,session,hand,subject_id,palm_id,class_id,sample_id
    columns = ["path", "dataset", "session", "hand", "subject_id", "palm_id", "class_id", "sample_id"]
    df = df[columns]
    
    # Save to CSV
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    df.to_csv(args.output, index=False)
    print(f"Manifest written successfully with {len(df)} entries to {args.output}")

if __name__ == "__main__":
    build_manifest()
