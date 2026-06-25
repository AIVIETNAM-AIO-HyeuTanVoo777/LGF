import argparse
import csv
import json
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=str, default="docs/results/rankb_run_manifest.csv")
    parser.add_argument("--out-dir", type=str, default="docs/results")
    return parser.parse_args()

def stable_json_load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    args = parse_args()
    manifest_path = Path(args.manifest)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    
    if not manifest_path.exists():
        print(f"Manifest not found: {manifest_path}")
        return 1
        
    with open(manifest_path, "r", encoding="utf-8") as f:
        runs = list(csv.DictReader(f))
        
    tongji_rows = []
    iitd_rows = []
    diag_rows = []
    
    for r in runs:
        method = r["method"]
        dataset = r["dataset"]
        direction = r["direction"]
        seed = int(r["seed"])
        result_json_path = Path(r["result_json"])
        
        if not result_json_path.exists():
            print(f"Result JSON not found: {result_json_path}")
            continue
            
        metrics = stable_json_load(result_json_path)
        
        row = {
            "method": method,
            "dataset": dataset,
            "direction": direction,
            "seed": seed,
            "rank1": float(metrics.get("Rank-1", 0.0)),
            "rank5": float(metrics.get("Rank-5", 0.0)),
            "macro_f1": float(metrics.get("Macro-F1", 0.0)),
            "eer": float(metrics.get("EER", 0.0)),
            "tar_far_1e_2": float(metrics.get("TAR@FAR=1e-2", 0.0)),
            "tar_far_1e_3": float(metrics.get("TAR@FAR=1e-3", 0.0))
        }
        
        if dataset == "Tongji":
            tongji_rows.append(row)
        elif dataset == "IITD":
            iitd_rows.append(row)
            
        # Collect score diagnostics
        output_dir = Path(r["output_dir"])
        diag_path = output_dir / "score_diagnostics.json"
        if diag_path.exists():
            diag = stable_json_load(diag_path)
            diag_rows.append({
                "method": method,
                "dataset": dataset,
                "direction": direction,
                "seed": seed,
                "num_genuine_pairs": int(diag.get("num_genuine_pairs", 0)),
                "num_impostor_pairs": int(diag.get("num_impostor_pairs", 0)),
                "genuine_mean": float(diag.get("genuine_mean", 0.0)),
                "genuine_std": float(diag.get("genuine_std", 0.0)),
                "impostor_mean": float(diag.get("impostor_mean", 0.0)),
                "impostor_std": float(diag.get("impostor_std", 0.0)),
                "impostor_q0.990": float(diag.get("impostor_q0.990", 0.0)),
                "impostor_q0.999": float(diag.get("impostor_q0.999", 0.0)),
                "genuine_q0.001": float(diag.get("genuine_q0.001", 0.0)),
                "genuine_q0.010": float(diag.get("genuine_q0.010", 0.0)),
                "d_prime": float(diag.get("d_prime", 0.0))
            })
            
    # Write main Tongji results
    tongji_fields = ["method", "dataset", "direction", "seed", "rank1", "rank5", "macro_f1", "eer", "tar_far_1e_2", "tar_far_1e_3"]
    
    main_tongji_csv = out_dir / "main_tongji_results.csv"
    with open(main_tongji_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=tongji_fields)
        writer.writeheader()
        writer.writerows(tongji_rows)
    print(f"Wrote {len(tongji_rows)} rows to {main_tongji_csv}")
    
    # Write directional Tongji results (same raw rows, can be used directly or summarized by script)
    tongji_dir_csv = out_dir / "tongji_directional_results.csv"
    with open(tongji_dir_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=tongji_fields)
        writer.writeheader()
        writer.writerows(tongji_rows)
    print(f"Wrote {len(tongji_rows)} rows to {tongji_dir_csv}")
    
    # Write IITD results
    iitd_csv_path = out_dir / "iitd_secondary_results.csv"
    with open(iitd_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=tongji_fields)
        writer.writeheader()
        writer.writerows(iitd_rows)
    print(f"Wrote {len(iitd_rows)} rows to {iitd_csv_path}")
    
    # Write score tail diagnostics
    diag_fields = [
        "method", "dataset", "direction", "seed", "num_genuine_pairs", "num_impostor_pairs",
        "genuine_mean", "genuine_std", "impostor_mean", "impostor_std",
        "impostor_q0.990", "impostor_q0.999", "genuine_q0.001", "genuine_q0.010", "d_prime"
    ]
    diag_csv = out_dir / "score_tail_diagnostics.csv"
    with open(diag_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=diag_fields)
        writer.writeheader()
        writer.writerows(diag_rows)
    print(f"Wrote {len(diag_rows)} rows to {diag_csv}")
    
    # Process and write classical reference results (Gabor)
    gabor_src_csv = out_dir / "gabor_strict_tongji_runs.csv"
    gabor_rows = []
    if gabor_src_csv.exists():
        with open(gabor_src_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                gabor_rows.append({
                    "method": "Gabor",
                    "dataset": "Tongji",
                    "direction": r["direction"],
                    "seed": int(r["seed"]),
                    "rank1": float(r["Rank-1"]),
                    "rank5": float(r["Rank-5"]),
                    "macro_f1": float(r["Macro-F1"]),
                    "eer": float(r["EER"]),
                    "tar_far_1e_2": float(r["TAR@FAR=1e-2"]),
                    "tar_far_1e_3": float(r["TAR@FAR=1e-3"])
                })
                
    gabor_csv = out_dir / "classical_reference_results.csv"
    with open(gabor_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=tongji_fields)
        writer.writeheader()
        writer.writerows(gabor_rows)
    print(f"Wrote {len(gabor_rows)} rows to {gabor_csv}")
    
    return 0

if __name__ == "__main__":
    main()
