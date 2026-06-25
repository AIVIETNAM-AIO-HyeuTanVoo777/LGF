import argparse
import csv
from pathlib import Path
import numpy as np

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default="docs/results/main_tongji_results.csv")
    parser.add_argument("--out", type=str, default="docs/results/paired_deltas.csv")
    return parser.parse_args()

def exact_sign_flip_p(deltas):
    deltas = np.array(deltas, dtype=float)
    observed_mean = np.abs(np.mean(deltas))
    n = len(deltas)
    count = 0
    total = 2 ** n
    for i in range(total):
        signs = np.array([1 if (i >> j) & 1 else -1 for j in range(n)])
        permuted_mean = np.abs(np.mean(deltas * signs))
        if permuted_mean >= observed_mean - 1e-12:
            count += 1
    return count / total

def bootstrap_ci(deltas, num_resamples=10000, ci=0.95):
    deltas = np.array(deltas, dtype=float)
    rng = np.random.default_rng(42)
    means = []
    n = len(deltas)
    for _ in range(num_resamples):
        resampled = rng.choice(deltas, size=n, replace=True)
        means.append(np.mean(resampled))
    lower = np.percentile(means, (1 - ci) / 2 * 100)
    upper = np.percentile(means, (1 + ci) / 2 * 100)
    return lower, upper

def main():
    args = parse_args()
    input_path = Path(args.input)
    out_path = Path(args.out)
    
    if not input_path.exists():
        print(f"Input file not found: {input_path}")
        return 1
        
    with open(input_path, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        
    # Group runs by (direction, seed)
    units = {}
    for r in rows:
        key = (r["direction"], int(r["seed"]))
        if key not in units:
            units[key] = {}
        units[key][r["method"]] = r
        
    comparisons = [
        ("M6_minus_M1", "M6", "M1"),
        ("M4_minus_M1", "M4", "M1"),
        ("M4_minus_M6", "M4", "M6")
    ]
    
    metrics = ["rank1", "rank5", "macro_f1", "eer", "tar_far_1e_2", "tar_far_1e_3"]
    metric_labels = {
        "rank1": "Rank-1",
        "rank5": "Rank-5",
        "macro_f1": "Macro-F1",
        "eer": "EER",
        "tar_far_1e_2": "TAR@FAR=1e-2",
        "tar_far_1e_3": "TAR@FAR=1e-3"
    }
    
    out_rows = []
    
    for comp_name, method_b, method_a in comparisons:
        # Collect matched deltas
        deltas_by_metric = {m: [] for m in metrics}
        for key, methods in units.items():
            if method_b in methods and method_a in methods:
                row_b = methods[method_b]
                row_a = methods[method_a]
                for m in metrics:
                    val_b = float(row_b[m])
                    val_a = float(row_a[m])
                    deltas_by_metric[m].append(val_b - val_a)
                    
        # Check if we have 6 matched units
        n = len(next(iter(deltas_by_metric.values())))
        if n != 6:
            print(f"Warning: Expected 6 matched units for {comp_name}, found {n}")
            
        for m in metrics:
            deltas = deltas_by_metric[m]
            if not deltas:
                continue
                
            # Report in percentage points (multiplied by 100)
            deltas_pct = [d * 100.0 for d in deltas]
            mean_delta = np.mean(deltas_pct)
            std_delta = np.std(deltas_pct, ddof=1) if len(deltas_pct) > 1 else 0.0
            
            p_val = exact_sign_flip_p(deltas_pct)
            ci_low, ci_high = bootstrap_ci(deltas_pct)
            
            # Determine directionality and interpretation
            # Positive Rank/TAR deltas favor method B
            # Positive EER deltas favor method A (worse for method B)
            if m == "eer":
                favors = "M_A" if mean_delta > 0 else "M_B"
            else:
                favors = "M_B" if mean_delta > 0 else "M_A"
                
            interpretation = f"{method_b} better" if favors == "M_B" else f"{method_b} worse"
            
            out_rows.append({
                "comparison": comp_name,
                "metric": metric_labels[m],
                "n": n,
                "mean_delta_pp": mean_delta,
                "sd_delta_pp": std_delta,
                "bootstrap_ci95_low_pp": ci_low,
                "bootstrap_ci95_high_pp": ci_high,
                "exact_sign_flip_p_two_sided": p_val,
                "interpretation": interpretation
            })
            
    # Write output
    fields = [
        "comparison", "metric", "n", "mean_delta_pp", "sd_delta_pp",
        "bootstrap_ci95_low_pp", "bootstrap_ci95_high_pp",
        "exact_sign_flip_p_two_sided", "interpretation"
    ]
    
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(out_rows)
        
    print(f"Wrote {len(out_rows)} rows to {out_path}")
    return 0

if __name__ == "__main__":
    main()
