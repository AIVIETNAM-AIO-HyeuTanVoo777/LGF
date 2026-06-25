import os
import sys
import hashlib
from pathlib import Path
import pandas as pd
import numpy as np
import torch

ROOT = Path(".").resolve()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from palmrec.evaluation.metrics import conservative_tar_at_far

STRICT_TONGJI_RUNS_CSV = ROOT / "docs/results/strict_tongji_ablation_runs.csv"
IITD_RUNS_CSV = ROOT / "docs/results/iitd_subject_disjoint_rerun_runs.csv"
OUTPUT_CSV = ROOT / "docs/audits/threshold_audit.csv"

def get_split_hash(split_file):
    p = Path(split_file)
    if not p.exists():
        p = ROOT / split_file
    if not p.exists():
        return "missing"
    with open(p, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def get_ckpt_info(run_dir):
    p = Path(run_dir)
    if not p.is_absolute():
        p = ROOT / p
    p = p.resolve()
    
    ckpt_path = p / "checkpoints" / "best.pt"
    if not ckpt_path.exists():
        ckpt_path = p / "best.pt"
        
    if not ckpt_path.exists():
        return "N/A", "N/A"
        
    try:
        ckpt = torch.load(ckpt_path, map_location="cpu")
        epoch = ckpt.get("epoch", "N/A")
        rel_path = ckpt_path.relative_to(ROOT).as_posix()
        return str(rel_path), str(epoch)
    except Exception:
        rel_path = ckpt_path.relative_to(ROOT).as_posix()
        return str(rel_path), "error"

def read_scores(scores_path):
    p = Path(scores_path)
    if not p.exists():
        p = ROOT / scores_path
    if not p.exists():
        raise FileNotFoundError(f"Missing scores.csv at {scores_path}")
    df = pd.read_csv(p, usecols=["score", "label"])
    y_scores = df["score"].astype(float).to_numpy()
    y_true = df["label"].astype(int).to_numpy()
    return y_true, y_scores

def main():
    rows = []
    
    # 1. Process Tongji Runs
    if STRICT_TONGJI_RUNS_CSV.exists():
        print(f"Loading Tongji runs from {STRICT_TONGJI_RUNS_CSV}...")
        tongji_df = pd.read_csv(STRICT_TONGJI_RUNS_CSV)
        for _, r in tongji_df.iterrows():
            method = str(r["method"])
            direction = str(r["direction"])
            seed = int(r["seed"])
            metrics_path = Path(r["metrics_path"])
            run_dir = metrics_path.parent
            
            # Locate scores.csv
            scores_path = run_dir / "scores.csv"
            if not scores_path.exists():
                scores_path = ROOT / run_dir / "scores.csv"
            if not scores_path.exists():
                scores_path = ROOT / "experiments" / run_dir / "scores.csv"
            
            if not scores_path.exists():
                print(f"Warning: scores.csv not found for Tongji run {method} {direction} seed {seed} at {scores_path}")
                continue
                
            # Determine split file
            # e.g., tongji_subject_disjoint_s1_to_s2_seed42.json
            dir_str = "s1_to_s2" if "s1->s2" in direction.lower() else "s2_to_s1"
            split_file = f"data/splits/tongji_subject_disjoint_{dir_str}_seed{seed}.json"
            split_hash = get_split_hash(split_file)
            
            # Checkpoint info
            ckpt_path, ckpt_epoch = get_ckpt_info(run_dir)
            if ckpt_path == "N/A":
                ckpt_path, ckpt_epoch = get_ckpt_info(ROOT / "experiments" / run_dir)
            
            # Read scores and compute
            y_true, y_scores = read_scores(scores_path)
            pos_scores = y_scores[y_true == 1]
            neg_scores = y_scores[y_true == 0]
            
            for target_far in [1e-2, 1e-3]:
                res = conservative_tar_at_far(pos_scores, neg_scores, target_far)
                passed = "true" if res["empirical_far"] <= target_far + 1e-12 else "false"
                
                rows.append({
                    "dataset": "Tongji",
                    "direction": direction,
                    "seed": seed,
                    "split_hash": split_hash,
                    "method": method,
                    "checkpoint_path": ckpt_path,
                    "checkpoint_epoch": ckpt_epoch,
                    "far_target": target_far,
                    "threshold": res["threshold"],
                    "empirical_far": res["empirical_far"],
                    "tar": res["tar"],
                    "n_genuine": res["n_genuine"],
                    "n_impostor": res["n_impostor"],
                    "far_step": res["far_step"],
                    "pass": passed
                })
    else:
        print(f"Skipping Tongji: {STRICT_TONGJI_RUNS_CSV} not found")

    # 2. Process IITD Runs
    if IITD_RUNS_CSV.exists():
        print(f"Loading IITD runs from {IITD_RUNS_CSV}...")
        iitd_df = pd.read_csv(IITD_RUNS_CSV)
        for _, r in iitd_df.iterrows():
            method = str(r["method"])
            seed = int(r["seed"])
            run_dir = Path(r["run_dir"])
            
            # Locate scores.csv
            scores_path = run_dir / "scores.csv"
            if not scores_path.exists():
                scores_path = ROOT / run_dir / "scores.csv"
            if not scores_path.exists():
                scores_path = ROOT / "experiments" / run_dir / "scores.csv"
                
            if not scores_path.exists():
                print(f"Warning: scores.csv not found for IITD run {method} seed {seed} at {scores_path}")
                continue
                
            # Determine split file
            split_file = f"data/splits/iitd_subject_disjoint_within_seed{seed}.json"
            split_hash = get_split_hash(split_file)
            
            # Checkpoint info
            ckpt_path, ckpt_epoch = get_ckpt_info(run_dir)
            if ckpt_path == "N/A":
                ckpt_path, ckpt_epoch = get_ckpt_info(ROOT / "experiments" / run_dir)
            
            # Read scores and compute
            y_true, y_scores = read_scores(scores_path)
            pos_scores = y_scores[y_true == 1]
            neg_scores = y_scores[y_true == 0]
            
            for target_far in [1e-2, 1e-3]:
                res = conservative_tar_at_far(pos_scores, neg_scores, target_far)
                passed = "true" if res["empirical_far"] <= target_far + 1e-12 else "false"
                
                rows.append({
                    "dataset": "IITD",
                    "direction": "within",
                    "seed": seed,
                    "split_hash": split_hash,
                    "method": method,
                    "checkpoint_path": ckpt_path,
                    "checkpoint_epoch": ckpt_epoch,
                    "far_target": target_far,
                    "threshold": res["threshold"],
                    "empirical_far": res["empirical_far"],
                    "tar": res["tar"],
                    "n_genuine": res["n_genuine"],
                    "n_impostor": res["n_impostor"],
                    "far_step": res["far_step"],
                    "pass": passed
                })
    else:
        print(f"Skipping IITD: {IITD_RUNS_CSV} not found")
        
    # Write to CSV
    if rows:
        out_df = pd.DataFrame(rows)
        # Ensure directory exists
        OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
        out_df.to_csv(OUTPUT_CSV, index=False)
        print(f"Successfully wrote {len(rows)} rows to {OUTPUT_CSV}")
    else:
        print("No audit rows generated.")

if __name__ == "__main__":
    main()
