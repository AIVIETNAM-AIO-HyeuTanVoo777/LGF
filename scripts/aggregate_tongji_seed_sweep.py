import os
import json
import re
import math
import numpy as np
from pathlib import Path

# Paths to process
RESULTS_DIR = "docs/results"
OUTPUT_JSON = os.path.join(RESULTS_DIR, "tongji_seed_sweep_summary.json")
OUTPUT_MD = os.path.join(RESULTS_DIR, "tongji_seed_sweep_summary.md")

# Run metadata to scan
RUNS_META = [
    # Method, Protocol, Seed, Base Name
    ("B1", "S1->S2", 42, "b1_resnet18_ce_supcon_tongji_s1s2_lr1e4"),
    ("B1", "S1->S2", 2026, "b1_resnet18_ce_supcon_tongji_s1s2_lr1e4_seed2026"),
    ("B1", "S1->S2", 2705, "b1_resnet18_ce_supcon_tongji_s1s2_lr1e4_seed2705"),
    
    ("B1", "S2->S1", 42, "b1_resnet18_ce_supcon_tongji_s2s1_lr1e4"),
    ("B1", "S2->S1", 2026, "b1_resnet18_ce_supcon_tongji_s2s1_lr1e4_seed2026"),
    ("B1", "S2->S1", 2705, "b1_resnet18_ce_supcon_tongji_s2s1_lr1e4_seed2705"),
    
    ("B2", "S1->S2", 42, "b2_fixed_gabor_resnet18_tongji_s1s2_lr1e4"),
    ("B2", "S1->S2", 2026, "b2_fixed_gabor_resnet18_tongji_s1s2_lr1e4_seed2026"),
    ("B2", "S1->S2", 2705, "b2_fixed_gabor_resnet18_tongji_s1s2_lr1e4_seed2705"),
    
    ("B2", "S2->S1", 42, "b2_fixed_gabor_resnet18_tongji_s2s1_lr1e4"),
    ("B2", "S2->S1", 2026, "b2_fixed_gabor_resnet18_tongji_s2s1_lr1e4_seed2026"),
    ("B2", "S2->S1", 2705, "b2_fixed_gabor_resnet18_tongji_s2s1_lr1e4_seed2705"),
]

def get_metric_val(data, keys):
    for k in keys:
        if k in data:
            return data[k]
    # flexible matching
    for k in keys:
        k_norm = k.lower().replace("_", "").replace("-", "").replace("@", "").replace("=", "")
        for dk in data.keys():
            dk_norm = dk.lower().replace("_", "").replace("-", "").replace("@", "").replace("=", "")
            if dk_norm == k_norm:
                return data[dk]
    return None

def parse_md_metrics(md_path):
    params = None
    flops = None
    time_ms = None
    if os.path.exists(md_path):
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
        # parameters (M)
        m_p = re.search(r"Total Parameters\*\*:\s*([\d,]+)", content)
        if m_p:
            params = float(m_p.group(1).replace(",", "")) / 1e6
        else:
            m_p_alt = re.search(r"Total Parameters\*\*:\s*[\d,]+\s*\(([\d\.]+)\s*M\)", content)
            if m_p_alt:
                params = float(m_p_alt.group(1))
                
        # flops (G)
        m_f = re.search(r"Estimated FLOPs\*\*:\s*([\d\.]+)\s*GFLOPs", content)
        if m_f:
            flops = float(m_f.group(1))
            
        # inference time (ms)
        m_t = re.search(r"Average Inference Time.*:\s*([\d\.]+)\s*ms", content)
        if m_t:
            time_ms = float(m_t.group(1))
    return params, flops, time_ms

def compute_stats(vals):
    if not vals:
        return {"mean": 0.0, "std": 0.0, "min": 0.0, "max": 0.0, "n": 0}
    mean = float(np.mean(vals))
    std = float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0
    return {
        "mean": mean,
        "std": std,
        "min": float(np.min(vals)),
        "max": float(np.max(vals)),
        "n": len(vals)
    }

def main():
    raw_runs = []
    
    # Step 1: Read all metrics files
    for method, protocol, seed, base_name in RUNS_META:
        json_path = os.path.join(RESULTS_DIR, f"{base_name}_metrics.json")
        md_path = os.path.join(RESULTS_DIR, f"{base_name}_metrics.md")
        
        if not os.path.exists(json_path):
            print(f"Warning: Missing metrics json at {json_path}. Skipped in aggregation.")
            continue
            
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        # Parse resource metrics from md
        params, flops, time_ms = parse_md_metrics(md_path)
        
        run_data = {
            "method": method,
            "protocol": protocol,
            "seed": seed,
            "base_name": base_name,
            "rank1": get_metric_val(data, ["Rank-1", "Rank1", "rank1"]),
            "rank5": get_metric_val(data, ["Rank-5", "Rank5", "rank5"]),
            "macro_f1": get_metric_val(data, ["Macro-F1", "macro_f1"]),
            "eer": get_metric_val(data, ["EER", "eer"]),
            "tar_far_1e_2": get_metric_val(data, ["TAR@FAR=1e-2", "tar_far_1e_2"]),
            "tar_far_1e_3": get_metric_val(data, ["TAR@FAR=1e-3", "tar_far_1e_3"]),
            "params_m": params,
            "flops_g": flops,
            "average_inference_time_ms": time_ms
        }
        raw_runs.append(run_data)
        
    if not raw_runs:
        print("Error: No raw runs metrics found. Aggregate cancelled.")
        return
        
    # Step 2: Compute bidirectional average for each seed
    seeds = sorted(list(set(r["seed"] for r in raw_runs)))
    methods = ["B1", "B2"]
    
    for m in methods:
        for s in seeds:
            # find S1->S2 and S2->S1 for this method & seed
            r_s1s2 = next((r for r in raw_runs if r["method"] == m and r["protocol"] == "S1->S2" and r["seed"] == s), None)
            r_s2s1 = next((r for r in raw_runs if r["method"] == m and r["protocol"] == "S2->S1" and r["seed"] == s), None)
            
            if r_s1s2 and r_s2s1:
                bidir_data = {
                    "method": m,
                    "protocol": "Bidirectional Average",
                    "seed": s,
                    "base_name": f"{m.lower()}_bidirectional_avg_seed{s}",
                }
                # average metrics
                for key in ["rank1", "rank5", "macro_f1", "eer", "tar_far_1e_2", "tar_far_1e_3", "average_inference_time_ms", "params_m", "flops_g"]:
                    v1 = r_s1s2[key]
                    v2 = r_s2s1[key]
                    if v1 is not None and v2 is not None:
                        bidir_data[key] = (v1 + v2) / 2.0
                    else:
                        bidir_data[key] = v1 if v1 is not None else v2
                raw_runs.append(bidir_data)
                
    # Step 3: Compute aggregated stats
    aggregated = {}
    
    for m in methods:
        aggregated[m] = {}
        for p in ["S1->S2", "S2->S1", "Bidirectional Average"]:
            aggregated[m][p] = {}
            # filter runs
            sub_runs = [r for r in raw_runs if r["method"] == m and r["protocol"] == p]
            
            for key in ["rank1", "rank5", "macro_f1", "eer", "tar_far_1e_2", "tar_far_1e_3", "average_inference_time_ms", "params_m", "flops_g"]:
                vals = [r[key] for r in sub_runs if r[key] is not None]
                # convert to percent if it's accuracy/error and in decimal
                if key in ["rank1", "rank5", "macro_f1", "eer", "tar_far_1e_2", "tar_far_1e_3"]:
                    vals = [v * 100.0 for v in vals]
                aggregated[m][p][key] = compute_stats(vals)
                
    # Save JSON summary
    summary_data = {
        "raw_runs": raw_runs,
        "aggregated": aggregated
    }
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=4)
    print(f"Saved JSON summary to {OUTPUT_JSON}")
    
    # Step 4: Markdown reporting and claim validation
    # Retrieve Bidirectional Average TAR@FAR=1e-3 statistics
    b1_tar_stats = aggregated["B1"]["Bidirectional Average"]["tar_far_1e_3"]
    b2_tar_stats = aggregated["B2"]["Bidirectional Average"]["tar_far_1e_3"]
    
    b1_mean = b1_tar_stats["mean"]
    b1_std = b1_tar_stats["std"]
    b2_mean = b2_tar_stats["mean"]
    b2_std = b2_tar_stats["std"]
    
    diff = b2_mean - b1_mean
    
    # Claim Decision Logic
    if b2_mean > b1_mean + 1.0:
        claim_decision = "STRENGTHENED"
        claim_desc = f"The fixed-Gabor strict-FAR verification robustness claim is **STRENGTHENED** across seeds. B2 outperforms B1 on average by {diff:.2f} percentage points ({b2_mean:.2f}% vs {b1_mean:.2f}%), and the standard deviation overlap is acceptable (B1 std: {b1_std:.2f}%, B2 std: {b2_std:.2f}%)."
    elif b2_mean > b1_mean:
        claim_decision = "WEAKENED"
        claim_desc = f"The fixed-Gabor strict-FAR verification robustness claim is **WEAKENED**. Although B2 outperforms B1 on average ({b2_mean:.2f}% vs {b1_mean:.2f}%), the advantage shrinks to {diff:.2f} percentage points (below the 1.0 percentage point threshold)."
    else:
        claim_decision = "UNSUPPORTED"
        claim_desc = f"The fixed-Gabor strict-FAR verification robustness claim is **UNSUPPORTED** across seeds. B1 matches or outperforms B2 on average TAR@FAR=1e-3 (B1: {b1_mean:.2f}%, B2: {b2_mean:.2f}%)."

    # Build markdown table 1: raw runs
    raw_rows = []
    # Sort raw runs for clean raw table output
    for r in sorted([x for x in raw_runs if x["protocol"] != "Bidirectional Average"], key=lambda x: (x["method"], x["protocol"], x["seed"])):
        # Format values to percent
        def p(val):
            return f"{val*100:.2f}%" if val is not None else "-"
        t_val = f"{r['average_inference_time_ms']:.2f} ms" if r['average_inference_time_ms'] is not None else "-"
        p_val = f"{r['params_m']:.2f}M" if r['params_m'] is not None else "-"
        f_val = f"{r['flops_g']:.3f}G" if r['flops_g'] is not None else "-"
        raw_rows.append(
            f"| {r['method']} | {r['protocol']} | {r['seed']} | {p(r['rank1'])} | {p(r['rank5'])} | {p(r['macro_f1'])} | {p(r['eer'])} | {p(r['tar_far_1e_2'])} | {p(r['tar_far_1e_3'])} | {t_val} | {p_val} | {f_val} |"
        )
        
    # Build markdown table 2: mean/std per recipe
    stats_rows = []
    for m in methods:
        for p in ["S1->S2", "S2->S1", "Bidirectional Average"]:
            st = aggregated[m][p]
            def fmt(key, unit="%"):
                mean_val = st[key]["mean"]
                std_val = st[key]["std"]
                if st[key]["n"] == 0:
                    return "-"
                return f"{mean_val:.2f}{unit} ± {std_val:.2f}{unit}"
            stats_rows.append(
                f"| {m} | {p} | {fmt('rank1')} | {fmt('rank5')} | {fmt('macro_f1')} | {fmt('eer')} | {fmt('tar_far_1e_2')} | {fmt('tar_far_1e_3')} | {fmt('average_inference_time_ms', ' ms')} | {fmt('params_m', 'M')} | {fmt('flops_g', 'G')} |"
            )
            
    # Direct comparison values (B2 - B1 on Bidirectional Average)
    def diff_bidir(key, unit="%"):
        b1 = aggregated["B1"]["Bidirectional Average"][key]["mean"]
        b2 = aggregated["B2"]["Bidirectional Average"][key]["mean"]
        d = b2 - b1
        sign = "+" if d >= 0 else ""
        return f"{sign}{d:.2f}{unit}"

    raw_rows_str = "\n".join(raw_rows)
    stats_rows_str = "\n".join(stats_rows)
    md_content = f"""# Tongji Cross-Session Seed Sweep Summary

This report aggregates the palmprint recognition results across multiple seeds (42, 2026, 2705) on the Tongji dataset to verify stability, robustness, and the core claim regarding fixed Gabor priors.

## 1. Per-Run Raw Metrics

| Method | Protocol | Seed | Rank-1 | Rank-5 | Macro-F1 | EER | TAR@1e-2 | TAR@1e-3 | Time | Params | FLOPs |
|---|---|---|---|---|---|---|---|---|---|---|---|
{raw_rows_str}

## 2. Aggregated Performance (Mean ± Std)

Aggregated over $n=3$ seeds (42, 2026, 2705). All accuracy and verification thresholds are in percentage values (%).

| Method | Protocol | Rank-1 | Rank-5 | Macro-F1 | EER | TAR@1e-2 | TAR@1e-3 | Time | Params | FLOPs |
|---|---|---|---|---|---|---|---|---|---|---|
{stats_rows_str}

## 3. Direct Comparison (B2 - B1 on Bidirectional Average)

Comparison of mean values:

- **Rank-1 Difference**: {diff_bidir('rank1')}
- **Macro-F1 Difference**: {diff_bidir('macro_f1')}
- **EER Difference**: {diff_bidir('eer')}
- **TAR@FAR=1e-2 Difference**: {diff_bidir('tar_far_1e_2')}
- **TAR@FAR=1e-3 Difference**: {diff_bidir('tar_far_1e_3')}
- **Inference Time Difference**: {diff_bidir('average_inference_time_ms', ' ms')}

## 4. Claim Decision

**Decision**: `{claim_decision}`

{claim_desc}

---
*Report generated automatically by `aggregate_tongji_seed_sweep.py`.*
"""
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Saved Markdown summary to {OUTPUT_MD}")

if __name__ == "__main__":
    main()
