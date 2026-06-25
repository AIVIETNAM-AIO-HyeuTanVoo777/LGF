import os
import json
import csv
import subprocess
import yaml
from pathlib import Path
import numpy as np

# Resolve Paths
REPO_ROOT = Path(__file__).resolve().parent.parent
EXP_DIR = REPO_ROOT / "experiments"
RESULTS_DIR = REPO_ROOT / "docs" / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

def get_git_commit():
    try:
        out = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(REPO_ROOT)).decode("utf-8").strip()
        return out
    except Exception:
        return "NA"

def get_metric(metrics, possible_keys):
    for k in possible_keys:
        if k in metrics:
            val = metrics[k]
            if val is not None:
                return float(val)
    return "NA"

def write_paper_ready_tables(runs):
    # Filter runs
    tongji_runs = [r for r in runs if r["dataset"] == "tongji" and r["protocol"] == "tongji_subject_disjoint_cross_session"]
    iitd_runs = [r for r in runs if r["dataset"] == "iitd" and r["protocol"] == "iitd_subject_disjoint_within_session"]
    
    # We expect 12 Tongji runs (B1/B6 x 2 directions x 3 seeds) and 6 IITD runs (B1/B6 x 3 seeds)
    has_all_tongji = len(tongji_runs) == 12
    has_all_iitd = len(iitd_runs) == 6
    
    md_content = "# Paper Ready Core Results Tables\n\n"
    
    if has_all_tongji:
        tongji_summary = {}
        for method in ["B1", "B6"]:
            tongji_summary[method] = {}
            for metric in ["rank1", "rank5", "macro_f1", "eer", "tar_far_1e_2", "tar_far_1e_3"]:
                seed_averages = []
                for seed in [42, 2026, 2705]:
                    s1s2_run = [r for r in tongji_runs if r["method"] == method and r["seed"] == seed and r["direction"] == "s1_to_s2"]
                    s2s1_run = [r for r in tongji_runs if r["method"] == method and r["seed"] == seed and r["direction"] == "s2_to_s1"]
                    if s1s2_run and s2s1_run:
                        val1 = s1s2_run[0][metric]
                        val2 = s2s1_run[0][metric]
                        if isinstance(val1, float) and isinstance(val2, float):
                            seed_averages.append((val1 + val2) / 2.0)
                if len(seed_averages) == 3:
                    mean = np.mean(seed_averages)
                    std = np.std(seed_averages, ddof=1)
                    tongji_summary[method][metric] = (mean, std)
                else:
                    tongji_summary[method][metric] = ("NA", "NA")
                    
        md_content += "## 1. Tongji Palm-Class-Disjoint Cross-Session Results (Bidirectional 3-Seed Average)\n\n"
        md_content += "| Method | Rank-1 | Rank-5 | Macro-F1 | EER | TAR@FAR=1e-2 | TAR@FAR=1e-3 |\n"
        md_content += "|---|---|---|---|---|---|---|\n"
        for method in ["B1", "B6"]:
            m_data = tongji_summary[method]
            row = f"| {method} "
            for metric in ["rank1", "rank5", "macro_f1", "eer", "tar_far_1e_2", "tar_far_1e_3"]:
                mean, std = m_data[metric]
                if mean != "NA":
                    row += f"| {mean*100:.4f}% ± {std*100:.4f}% "
                else:
                    row += "| NA "
            row += "|\n"
            md_content += row
        md_content += "\n"
    else:
        md_content += "## 1. Tongji Palm-Class-Disjoint Cross-Session Results\n\n"
        md_content += "*Summary generation pending (incomplete Tongji runs)*\n\n"
        
    if has_all_iitd:
        iitd_summary = {}
        for method in ["B1", "B6"]:
            iitd_summary[method] = {}
            for metric in ["rank1", "rank5", "macro_f1", "eer", "tar_far_1e_2", "tar_far_1e_3"]:
                seed_vals = []
                for seed in [42, 2026, 2705]:
                    run = [r for r in iitd_runs if r["method"] == method and r["seed"] == seed]
                    if run:
                        val = run[0][metric]
                        if isinstance(val, float):
                            seed_vals.append(val)
                if len(seed_vals) == 3:
                    mean = np.mean(seed_vals)
                    std = np.std(seed_vals, ddof=1)
                    iitd_summary[method][metric] = (mean, std)
                else:
                    iitd_summary[method][metric] = ("NA", "NA")
                    
        md_content += "## 2. IITD Palm-Class-Disjoint Within-Session Results (3-Seed Average)\n\n"
        md_content += "| Method | Rank-1 | Rank-5 | Macro-F1 | EER | TAR@FAR=1e-2 | TAR@FAR=1e-3 |\n"
        md_content += "|---|---|---|---|---|---|---|\n"
        for method in ["B1", "B6"]:
            m_data = iitd_summary[method]
            row = f"| {method} "
            for metric in ["rank1", "rank5", "macro_f1", "eer", "tar_far_1e_2", "tar_far_1e_3"]:
                mean, std = m_data[metric]
                if mean != "NA":
                    row += f"| {mean*100:.4f}% ± {std*100:.4f}% "
                else:
                    row += "| NA "
            row += "|\n"
            md_content += row
        md_content += "\n"
    else:
        md_content += "## 2. IITD Palm-Class-Disjoint Within-Session Results\n\n"
        md_content += "*Summary generation pending (incomplete IITD runs)*\n\n"
        
    md_file = RESULTS_DIR / "paper_ready_tables.md"
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Wrote paper ready tables to {md_file}")

def main():
    print("Starting full results aggregation...")
    
    commit_hash = get_git_commit()
    
    runs = []
    warnings = []
    
    if not EXP_DIR.exists():
        print(f"Experiments directory {EXP_DIR} does not exist!")
        return
        
    # List all subdirectories in experiments/
    run_dirs = sorted([d for d in EXP_DIR.iterdir() if d.is_dir()])
    print(f"Found {len(run_dirs)} run directories in {EXP_DIR}.")
    
    for rdir in run_dirs:
        run_name = rdir.name
        metrics_file = rdir / "metrics.json"
        
        if not metrics_file.exists():
            warnings.append(f"Warning: {run_name} is missing metrics.json. Skipping.")
            print(warnings[-1])
            continue
            
        # Try loading metrics.json
        try:
            with open(metrics_file, "r", encoding="utf-8") as f:
                metrics_data = json.load(f)
        except Exception as e:
            warnings.append(f"Warning: Failed to parse metrics.json in {run_name}: {e}. Skipping.")
            print(warnings[-1])
            continue
            
        # Map metrics
        rank1 = get_metric(metrics_data, ["Rank-1", "rank1", "rank_1", "Rank1"])
        rank5 = get_metric(metrics_data, ["Rank-5", "rank5", "rank_5", "Rank5"])
        macro_f1 = get_metric(metrics_data, ["Macro-F1", "macro_f1", "macro-f1", "Macro_F1"])
        eer = get_metric(metrics_data, ["EER", "eer"])
        tar_far_1e_2 = get_metric(metrics_data, ["TAR@FAR=1e-2", "tar_far_1e_2", "TAR@FAR=0.01", "tar_far_0.01"])
        tar_far_1e_3 = get_metric(metrics_data, ["TAR@FAR=1e-3", "tar_far_1e_3", "TAR@FAR=0.001", "tar_far_0.001"])
        
        # Load config
        config = {}
        config_path = REPO_ROOT / "configs" / f"{run_name}.yaml"
        if config_path.exists():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config = yaml.safe_load(f)
            except Exception as e:
                warnings.append(f"Warning: Failed to load config file {config_path.name}: {e}")
                print(warnings[-1])
        
        # If config is empty, try loading it from checkpoint
        checkpoint_path = rdir / "checkpoints" / "best.pt"
        if not config and checkpoint_path.exists():
            try:
                import torch
                checkpoint = torch.load(checkpoint_path, map_location="cpu")
                if "config" in checkpoint:
                    config = checkpoint["config"]
            except Exception as e:
                pass
                
        # Infer Metadata
        dataset = "unknown"
        if "tongji" in run_name.lower():
            dataset = "tongji"
        elif "iitd" in run_name.lower():
            dataset = "iitd"
        elif config.get("dataset", {}).get("name"):
            dataset = config["dataset"]["name"].lower()
            
        # protocol
        protocol = "unknown"
        if "subject_disjoint" in run_name.lower():
            if dataset == "tongji":
                protocol = "tongji_subject_disjoint_cross_session"
            elif dataset == "iitd":
                protocol = "iitd_subject_disjoint_within_session"
        elif "seen_identity" in run_name.lower() or "ablation" in run_name.lower():
            protocol = "seen_identity_diagnostic"
        else:
            # Fallback based on split_file path in config
            split_file = config.get("dataset", {}).get("split_file", "")
            if "subject_disjoint" in split_file.lower():
                if dataset == "tongji":
                    protocol = "tongji_subject_disjoint_cross_session"
                elif dataset == "iitd":
                    protocol = "iitd_subject_disjoint_within_session"
            else:
                protocol = "seen_identity_diagnostic"
                
        # direction
        direction = "unknown"
        if "s1s2" in run_name.lower() or "s1_to_s2" in run_name.lower():
            direction = "s1_to_s2"
        elif "s2s1" in run_name.lower() or "s2_to_s1" in run_name.lower():
            direction = "s2_to_s1"
        elif "within" in run_name.lower() or dataset == "iitd":
            direction = "within"
            
        # seed
        seed = "unknown"
        if "seed42" in run_name.lower():
            seed = 42
        elif "seed2026" in run_name.lower():
            seed = 2026
        elif "seed2705" in run_name.lower():
            seed = 2705
        else:
            seed = config.get("seed", "unknown")
            
        # method
        method = "unknown"
        if run_name.lower().startswith("b1"):
            method = "B1"
        elif run_name.lower().startswith("b6"):
            method = "B6"
        elif run_name.lower().startswith("b4"):
            method = "B4"
        elif run_name.lower().startswith("b7"):
            method = "B7"
        elif run_name.lower().startswith("b2"):
            method = "B2"
            
        runs.append({
            "dataset": dataset,
            "protocol": protocol,
            "direction": direction,
            "seed": seed,
            "method": method,
            "run_dir": run_name,
            "config_path": f"configs/{run_name}.yaml" if config_path.exists() else "NA",
            "checkpoint_path": f"experiments/{run_name}/checkpoints/best.pt" if checkpoint_path.exists() else "NA",
            "rank1": rank1,
            "rank5": rank5,
            "macro_f1": macro_f1,
            "eer": eer,
            "tar_far_1e_2": tar_far_1e_2,
            "tar_far_1e_3": tar_far_1e_3,
            "commit_hash": commit_hash,
            "metrics_path": f"experiments/{run_name}/metrics.json"
        })
        
    # Write docs/results/all_runs_raw.csv
    csv_file = RESULTS_DIR / "all_runs_raw.csv"
    headers = [
        "dataset", "protocol", "direction", "seed", "method", "run_dir", 
        "config_path", "checkpoint_path", "rank1", "rank5", "macro_f1", 
        "eer", "tar_far_1e_2", "tar_far_1e_3", "commit_hash", "metrics_path"
    ]
    
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for r in runs:
            writer.writerow(r)
    print(f"Wrote {len(runs)} rows to {csv_file}")
    
    # Write docs/results/all_runs_raw.md
    md_file = RESULTS_DIR / "all_runs_raw.md"
    md_content = f"""# All Runs Raw Summary

Total runs detected with valid metrics: {len(runs)}

## 1. Runs Table

| Dataset | Protocol | Direction | Seed | Method | Run Dir | Rank-1 | EER | TAR@1e-3 |
|---|---|---|---|---|---|---|---|---|
"""
    for r in runs:
        r1_str = f"{r['rank1']*100:.2f}%" if isinstance(r['rank1'], float) else str(r['rank1'])
        eer_str = f"{r['eer']*100:.2f}%" if isinstance(r['eer'], float) else str(r['eer'])
        tar_str = f"{r['tar_far_1e_3']*100:.2f}%" if isinstance(r['tar_far_1e_3'], float) else str(r['tar_far_1e_3'])
        md_content += f"| {r['dataset']} | {r['protocol']} | {r['direction']} | {r['seed']} | {r['method']} | `{r['run_dir']}` | {r1_str} | {eer_str} | {tar_str} |\n"
        
    if warnings:
        md_content += "\n## 2. Warnings / Missing Fields\n\n"
        for w in warnings:
            md_content += f"- {w}\n"
            
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Wrote summary to {md_file}")
    
    # Write docs/results/paper_ready_tables.md
    write_paper_ready_tables(runs)

if __name__ == "__main__":
    main()
