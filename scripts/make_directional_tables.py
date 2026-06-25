import os
import csv
from pathlib import Path
import numpy as np

# Resolve Paths
REPO_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = REPO_ROOT / "docs" / "results"
INPUT_CSV = RESULTS_DIR / "all_runs_raw.csv"

def main():
    print("Generating directional tables and deltas...")
    
    if not INPUT_CSV.exists():
        print(f"Error: {INPUT_CSV} does not exist. Run aggregate_all_results.py first.")
        return

    # Read all runs raw csv
    rows = []
    with open(INPUT_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            # Convert metric columns to float
            for col in ["rank1", "rank5", "macro_f1", "eer", "tar_far_1e_2", "tar_far_1e_3"]:
                if r[col] != "NA":
                    r[col] = float(r[col])
            # Convert seed to int if possible
            try:
                r["seed"] = int(r["seed"])
            except ValueError:
                pass
            rows.append(r)

    # Filter for Tongji primary palm-class-disjoint cross-session runs for B1 and B6
    tongji_rows = []
    for r in rows:
        if (r["dataset"] == "tongji" and 
            r["protocol"] == "tongji_subject_disjoint_cross_session" and 
            r["method"] in ["B1", "B6"] and 
            r["direction"] in ["s1_to_s2", "s2_to_s1"] and 
            r["seed"] in [42, 2026, 2705]):
            tongji_rows.append(r)

    print(f"Filtered {len(tongji_rows)} Tongji directional runs.")

    # Sort: method, direction, seed
    tongji_rows.sort(key=lambda x: (x["method"], x["direction"], x["seed"]))

    # Write tongji_directional_metrics_full.csv
    csv_headers = [
        "dataset", "protocol", "direction", "seed", "method", "rank1", "rank5", 
        "macro_f1", "eer", "tar_far_1e_2", "tar_far_1e_3", "run_dir", 
        "config_path", "metrics_path"
    ]
    
    out_full_csv = RESULTS_DIR / "tongji_directional_metrics_full.csv"
    with open(out_full_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=csv_headers)
        writer.writeheader()
        for r in tongji_rows:
            writer.writerow({k: r[k] for k in csv_headers})
    print(f"Wrote {len(tongji_rows)} rows to {out_full_csv}")

    # Write tongji_directional_metrics_full.md
    out_full_md = RESULTS_DIR / "tongji_directional_metrics_full.md"
    md_content = """# Tongji Directional Metrics Full

This document presents the detailed directional results for the primary Tongji palm-class-disjoint cross-session evaluation.

| Method | Direction | Seed | Rank-1 | Rank-5 | Macro-F1 | EER | TAR@1e-2 | TAR@1e-3 |
|---|---|---|---|---|---|---|---|---|
"""
    for r in tongji_rows:
        md_content += (f"| {r['method']} | {r['direction']} | {r['seed']} | "
                       f"{r['rank1']*100:.2f}% | {r['rank5']*100:.2f}% | {r['macro_f1']*100:.2f}% | "
                       f"{r['eer']*100:.2f}% | {r['tar_far_1e_2']*100:.2f}% | {r['tar_far_1e_3']*100:.2f}% |\n")

    with open(out_full_md, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Wrote full directional markdown to {out_full_md}")

    # Compute deltas: B6 - B1
    delta_rows = []
    directions = ["s1_to_s2", "s2_to_s1"]
    seeds = [42, 2026, 2705]

    for d in directions:
        for s in seeds:
            b1_run = [r for r in tongji_rows if r["method"] == "B1" and r["direction"] == d and r["seed"] == s]
            b6_run = [r for r in tongji_rows if r["method"] == "B6" and r["direction"] == d and r["seed"] == s]
            
            if b1_run and b6_run:
                b1 = b1_run[0]
                b6 = b6_run[0]
                delta_rows.append({
                    "direction": d,
                    "seed": s,
                    "delta_rank1_b6_minus_b1": b6["rank1"] - b1["rank1"],
                    "delta_rank5_b6_minus_b1": b6["rank5"] - b1["rank5"],
                    "delta_macro_f1_b6_minus_b1": b6["macro_f1"] - b1["macro_f1"],
                    "delta_eer_b6_minus_b1": b6["eer"] - b1["eer"],
                    "delta_tar_far_1e_2_b6_minus_b1": b6["tar_far_1e_2"] - b1["tar_far_1e_2"],
                    "delta_tar_far_1e_3_b6_minus_b1": b6["tar_far_1e_3"] - b1["tar_far_1e_3"]
                })

    # Write tongji_directional_delta_b6_minus_b1.csv
    delta_headers = [
        "direction", "seed", "delta_rank1_b6_minus_b1", "delta_rank5_b6_minus_b1",
        "delta_macro_f1_b6_minus_b1", "delta_eer_b6_minus_b1",
        "delta_tar_far_1e_2_b6_minus_b1", "delta_tar_far_1e_3_b6_minus_b1"
    ]
    out_delta_csv = RESULTS_DIR / "tongji_directional_delta_b6_minus_b1.csv"
    with open(out_delta_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=delta_headers)
        writer.writeheader()
        for dr in delta_rows:
            writer.writerow(dr)
    print(f"Wrote {len(delta_rows)} rows to {out_delta_csv}")

    # Compute direction-level mean deltas
    mean_deltas = {}
    for d in directions:
        d_rows = [r for r in delta_rows if r["direction"] == d]
        mean_deltas[d] = {
            "mean_delta_rank1": np.mean([r["delta_rank1_b6_minus_b1"] for r in d_rows]),
            "mean_delta_rank5": np.mean([r["delta_rank5_b6_minus_b1"] for r in d_rows]),
            "mean_delta_macro_f1": np.mean([r["delta_macro_f1_b6_minus_b1"] for r in d_rows]),
            "mean_delta_eer": np.mean([r["delta_eer_b6_minus_b1"] for r in d_rows]),
            "mean_delta_tar_far_1e_2": np.mean([r["delta_tar_far_1e_2_b6_minus_b1"] for r in d_rows]),
            "mean_delta_tar_far_1e_3": np.mean([r["delta_tar_far_1e_3_b6_minus_b1"] for r in d_rows])
        }

    # Format findings text dynamically
    findings = []
    # S1->S2 finding
    s1s2_r1 = mean_deltas["s1_to_s2"]["mean_delta_rank1"] * 100
    s1s2_eer = mean_deltas["s1_to_s2"]["mean_delta_eer"] * 100
    s1s2_tar = mean_deltas["s1_to_s2"]["mean_delta_tar_far_1e_3"] * 100
    if s1s2_tar > 0:
        findings.append(f"For the S1->S2 direction, B6 exhibits a limited verification gain of {s1s2_tar:.2f} percentage points at TAR@FAR=1e-3, accompanied by a small EER increase (worse) of {s1s2_eer:.2f} percentage points.")
    else:
        findings.append(f"For the S1->S2 direction, B6 shows a decrease in TAR@FAR=1e-3 of {s1s2_tar:.2f} percentage points and an EER increase of {s1s2_eer:.2f} percentage points.")

    # S2->S1 finding
    s2s1_r1 = mean_deltas["s2_to_s1"]["mean_delta_rank1"] * 100
    s2s1_eer = mean_deltas["s2_to_s1"]["mean_delta_eer"] * 100
    s2s1_tar = mean_deltas["s2_to_s1"]["mean_delta_tar_far_1e_3"] * 100
    findings.append(f"For the S2->S1 direction, B6 consistently underperforms B1 across key identification and verification metrics, showing a drop of {s2s1_r1:.2f} percentage points in Rank-1 accuracy and a degradation of {s2s1_tar:.2f} percentage points in TAR@FAR=1e-3.")
    
    # Bidirectional avg finding
    findings.append("The bidirectional average hides this directional asymmetry, where the overall negative delta is heavily driven by the S2->S1 direction.")
    findings_paragraph = " ".join(findings)

    # Write tongji_directional_delta_b6_minus_b1.md
    out_delta_md = RESULTS_DIR / "tongji_directional_delta_b6_minus_b1.md"
    
    def format_diff(val):
        sign = "+" if val >= 0 else ""
        return f"{sign}{val*100:.2f} pp"

    delta_md_content = f"""# Tongji Directional Delta: B6 - B1

## Interpretation
- Positive Rank/TAR deltas favor B6.
- Positive EER deltas indicate B6 is worse.

## Per-seed delta table

| Direction | Seed | Delta Rank-1 | Delta Rank-5 | Delta Macro-F1 | Delta EER | Delta TAR@1e-2 | Delta TAR@1e-3 |
|---|---|---|---|---|---|---|---|
"""
    for dr in delta_rows:
        delta_md_content += (f"| {dr['direction']} | {dr['seed']} | "
                             f"{format_diff(dr['delta_rank1_b6_minus_b1'])} | "
                             f"{format_diff(dr['delta_rank5_b6_minus_b1'])} | "
                             f"{format_diff(dr['delta_macro_f1_b6_minus_b1'])} | "
                             f"{format_diff(dr['delta_eer_b6_minus_b1'])} | "
                             f"{format_diff(dr['delta_tar_far_1e_2_b6_minus_b1'])} | "
                             f"{format_diff(dr['delta_tar_far_1e_3_b6_minus_b1'])} |\n")

    delta_md_content += """
## Direction-level mean delta

| Direction | Mean Delta Rank-1 | Mean Delta EER | Mean Delta TAR@FAR=1e-3 |
|---|---|---|---|
"""
    for d in directions:
        md = mean_deltas[d]
        delta_md_content += f"| {d} | {format_diff(md['mean_delta_rank1'])} | {format_diff(md['mean_delta_eer'])} | {format_diff(md['mean_delta_tar_far_1e_3'])} |\n"

    delta_md_content += f"""
## Main finding
{findings_paragraph}
"""

    with open(out_delta_md, "w", encoding="utf-8") as f:
        f.write(delta_md_content)
    print(f"Wrote delta markdown to {out_delta_md}")

if __name__ == "__main__":
    main()
