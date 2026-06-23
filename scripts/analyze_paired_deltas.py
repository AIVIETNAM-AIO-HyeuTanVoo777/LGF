import os
import csv
from pathlib import Path
import numpy as np

# Resolve Paths
REPO_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = REPO_ROOT / "docs" / "results"
INPUT_CSV = RESULTS_DIR / "tongji_directional_delta_b6_minus_b1.csv"
OUTPUT_CSV = RESULTS_DIR / "paired_delta_b6_vs_b1.csv"
OUTPUT_MD = RESULTS_DIR / "paired_delta_b6_vs_b1.md"

def main():
    print("Analyzing paired deltas B6 vs B1...")
    
    if not INPUT_CSV.exists():
        print(f"Error: {INPUT_CSV} does not exist.")
        return
        
    # Read input CSV
    rows = []
    with open(INPUT_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            # Parse values
            r["seed"] = int(r["seed"])
            for col in [
                "delta_rank1_b6_minus_b1",
                "delta_rank5_b6_minus_b1",
                "delta_macro_f1_b6_minus_b1",
                "delta_eer_b6_minus_b1",
                "delta_tar_far_1e_2_b6_minus_b1",
                "delta_tar_far_1e_3_b6_minus_b1"
            ]:
                r[col] = float(r[col])
            rows.append(r)
            
    # Construct output CSV rows
    # Columns:
    # dataset, protocol, unit, direction, seed,
    # delta_rank1_b6_minus_b1, delta_rank5_b6_minus_b1, delta_macro_f1_b6_minus_b1,
    # delta_eer_b6_minus_b1, delta_tar_far_1e_2_b6_minus_b1, delta_tar_far_1e_3_b6_minus_b1
    
    out_rows = []
    for r in rows:
        direction = r["direction"]
        seed = r["seed"]
        # unit is direction_seed, so we use f"{direction}_{seed}"
        unit = f"{direction}_{seed}"
        out_rows.append({
            "dataset": "tongji",
            "protocol": "subject_disjoint_cross_session",
            "unit": unit,
            "direction": direction,
            "seed": seed,
            "delta_rank1_b6_minus_b1": r["delta_rank1_b6_minus_b1"],
            "delta_rank5_b6_minus_b1": r["delta_rank5_b6_minus_b1"],
            "delta_macro_f1_b6_minus_b1": r["delta_macro_f1_b6_minus_b1"],
            "delta_eer_b6_minus_b1": r["delta_eer_b6_minus_b1"],
            "delta_tar_far_1e_2_b6_minus_b1": r["delta_tar_far_1e_2_b6_minus_b1"],
            "delta_tar_far_1e_3_b6_minus_b1": r["delta_tar_far_1e_3_b6_minus_b1"]
        })
        
    # Write to CSV
    csv_headers = [
        "dataset", "protocol", "unit", "direction", "seed",
        "delta_rank1_b6_minus_b1", "delta_rank5_b6_minus_b1", "delta_macro_f1_b6_minus_b1",
        "delta_eer_b6_minus_b1", "delta_tar_far_1e_2_b6_minus_b1", "delta_tar_far_1e_3_b6_minus_b1"
    ]
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=csv_headers)
        writer.writeheader()
        for orow in out_rows:
            writer.writerow(orow)
    print(f"Wrote {len(out_rows)} rows to {OUTPUT_CSV}")
    
    # Calculate means
    mean_rank1 = np.mean([r["delta_rank1_b6_minus_b1"] for r in out_rows])
    mean_rank5 = np.mean([r["delta_rank5_b6_minus_b1"] for r in out_rows])
    mean_macro_f1 = np.mean([r["delta_macro_f1_b6_minus_b1"] for r in out_rows])
    mean_eer = np.mean([r["delta_eer_b6_minus_b1"] for r in out_rows])
    mean_tar_1e_2 = np.mean([r["delta_tar_far_1e_2_b6_minus_b1"] for r in out_rows])
    mean_tar_1e_3 = np.mean([r["delta_tar_far_1e_3_b6_minus_b1"] for r in out_rows])
    
    # Format diff helper
    def format_diff(val):
        sign = "+" if val >= 0 else ""
        return f"{sign}{val*100:.2f} pp"
        
    # Write to MD
    # Requirements:
    # 1. Scope:
    # - This analysis uses six paired seed-direction units from Tongji subject-disjoint cross-session evaluation.
    # - Each unit compares B6 and B1 under the same direction and seed.
    # - Positive Rank/TAR deltas favor B6.
    # - Positive EER deltas indicate worse performance for B6.
    # - Because there are only six paired units, this is descriptive paired evidence, not a formal significance claim.
    # 2. Per-unit paired deltas table (6 rows)
    # 3. Mean paired deltas over six units
    # 4. Direction-level notes:
    # - S1→S2 mixed.
    # - S2→S1 more consistently negative for B6.
    # - No significance claim.
    
    md_content = f"""# Paired Delta Analysis: B6 vs B1

## Scope
- This analysis uses six paired seed-direction units from Tongji subject-disjoint cross-session evaluation.
- Each unit compares B6 and B1 under the same direction and seed.
- Positive Rank/TAR deltas favor B6.
- Positive EER deltas indicate worse performance for B6.
- Because there are only six paired units, this is descriptive paired evidence, not a formal significance claim.

## Per-unit paired deltas

| Unit | Direction | Seed | Delta Rank-1 | Delta Rank-5 | Delta Macro-F1 | Delta EER | Delta TAR@1e-2 | Delta TAR@1e-3 |
|---|---|---|---|---|---|---|---|---|
"""
    for orow in out_rows:
        md_content += (f"| {orow['unit']} | {orow['direction']} | {orow['seed']} | "
                       f"{format_diff(orow['delta_rank1_b6_minus_b1'])} | "
                       f"{format_diff(orow['delta_rank5_b6_minus_b1'])} | "
                       f"{format_diff(orow['delta_macro_f1_b6_minus_b1'])} | "
                       f"{format_diff(orow['delta_eer_b6_minus_b1'])} | "
                       f"{format_diff(orow['delta_tar_far_1e_2_b6_minus_b1'])} | "
                       f"{format_diff(orow['delta_tar_far_1e_3_b6_minus_b1'])} |\n")
                       
    md_content += f"""
## Mean paired deltas over six units

- Rank-1: {format_diff(mean_rank1)}
- Rank-5: {format_diff(mean_rank5)}
- Macro-F1: {format_diff(mean_macro_f1)}
- EER: {format_diff(mean_eer)}
- TAR@1e-2: {format_diff(mean_tar_1e_2)}
- TAR@1e-3: {format_diff(mean_tar_1e_3)}

## Direction-level notes
- For the S1→S2 evaluation direction, the performance comparison between B6 and B1 is mixed, showing small gains on some seeds/metrics and drops on others.
- For the S2→S1 evaluation direction, the performance differences are more consistently negative for B6, indicating that B6 performs worse than B1 under this cross-session direction.
- Due to the small sample size (six paired units), this analysis presents descriptive evidence only and does not make a formal significance claim.
"""

    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Wrote paired delta markdown to {OUTPUT_MD}")

if __name__ == "__main__":
    main()
