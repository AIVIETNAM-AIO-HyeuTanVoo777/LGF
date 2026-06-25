import os
import json
import numpy as np
import pandas as pd
from pathlib import Path

# Paths
REPO_ROOT = Path(__file__).resolve().parent.parent
EXP_DIR = REPO_ROOT / "experiments"
RESULTS_DIR = REPO_ROOT / "docs" / "results"

# Create results directory if it doesn't exist
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Configurations
SEEDS = [42, 2026, 2705]
METRIC_KEYS = ["Rank-1", "Rank-5", "Macro-F1", "EER", "TAR@FAR=1e-2", "TAR@FAR=1e-3"]

def get_metrics_from_dir(dir_name):
    path = EXP_DIR / dir_name / "metrics.json"
    if not path.exists():
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Ensure all values are floats
            return {k: float(v) for k, v in data.items() if k in METRIC_KEYS}
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return None

def has_complete_metrics(metrics):
    return metrics is not None and all(k in metrics for k in METRIC_KEYS)

def compute_mean_std(values_list):
    if not values_list:
        return 0.0, 0.0
    mean = float(np.mean(values_list))
    std = float(np.std(values_list, ddof=1)) if len(values_list) > 1 else 0.0
    return mean, std

def format_cell(mean, std=None):
    if std is not None:
        return f"{mean*100:.2f}% ± {std*100:.2f}%" if mean <= 1.0 else f"{mean:.4f} ± {std:.4f}"
    return f"{mean*100:.2f}%" if mean <= 1.0 else f"{mean:.4f}"

def format_cell_diff(diff):
    sign = "+" if diff >= 0 else ""
    return f"{sign}{diff*100:.2f} pp"

def main():
    print("Aggregating results...")

    # -------------------------------------------------------------
    # 1. Tongji Palm-Class-Disjoint Cross-Session Aggregation
    # -------------------------------------------------------------
    tongji_data = {}

    for method in ["b1", "b6"]:
        tongji_data[method] = {}
        for direction in ["s1s2", "s2s1"]:
            tongji_data[method][direction] = {}
            for seed in SEEDS:
                # Resolve directory name
                if method == "b1":
                    dir_name = f"b1_resnet18_ce_supcon_tongji_subject_disjoint_{direction}_seed{seed}"
                else:
                    dir_name = f"b6_resnet18_bnneck_arcface_tongji_subject_disjoint_{direction}_seed{seed}"

                metrics = get_metrics_from_dir(dir_name)
                tongji_data[method][direction][seed] = metrics

    has_tongji_metrics = all(
        has_complete_metrics(tongji_data[method][direction][seed])
        for method in ["b1", "b6"]
        for direction in ["s1s2", "s2s1"]
        for seed in SEEDS
    )

    if has_tongji_metrics:
        # Build Tongji report
        tongji_report = """# Tongji Palm-Class-Disjoint Cross-Session Evaluation Summary

This document aggregates evaluation metrics for Tier-1 models on the Tongji palm-class-disjoint cross-session protocol across three random seeds: 42, 2026, and 2705.

- **Baseline (B1)**: ResNet18 trained with Cross-Entropy and Supervised Contrastive Loss.
- **BNNeck + ArcFace (B6)**: ResNet18 trained with BNNeck and ArcFace Loss.

## 1. Direction-Specific Run Details

### Direction: Session 1 &rarr; Session 2 (S1 &rarr; S2)

| Model | Seed 42 | Seed 2026 | Seed 2705 | Mean &plusmn; Std |
|---|---|---|---|---|
"""
        # S1->S2 Rank-1 table
        for method_name, method_key in [("Baseline (B1)", "b1"), ("BNNeck + ArcFace (B6)", "b6")]:
            r1_vals = []
            cells = []
            for seed in SEEDS:
                metrics = tongji_data[method_key]["s1s2"][seed]
                if metrics and "Rank-1" in metrics:
                    r1_vals.append(metrics["Rank-1"])
                    cells.append(format_cell(metrics["Rank-1"]))
                else:
                    cells.append("N/A")
            mean_val, std_val = compute_mean_std(r1_vals)
            tongji_report += f"| {method_name} | {' | '.join(cells)} | {format_cell(mean_val, std_val)} |\n"

        tongji_report += """
### Direction: Session 2 &rarr; Session 1 (S2 &rarr; S1)

| Model | Seed 42 | Seed 2026 | Seed 2705 | Mean &plusmn; Std |
|---|---|---|---|---|
"""
        # S2->S1 Rank-1 table
        for method_name, method_key in [("Baseline (B1)", "b1"), ("BNNeck + ArcFace (B6)", "b6")]:
            r1_vals = []
            cells = []
            for seed in SEEDS:
                metrics = tongji_data[method_key]["s2s1"][seed]
                if metrics and "Rank-1" in metrics:
                    r1_vals.append(metrics["Rank-1"])
                    cells.append(format_cell(metrics["Rank-1"]))
                else:
                    cells.append("N/A")
            mean_val, std_val = compute_mean_std(r1_vals)
            tongji_report += f"| {method_name} | {' | '.join(cells)} | {format_cell(mean_val, std_val)} |\n"

        # Complete Summary Table (Averaging Bidirectional Runs)
        tongji_report += """
## 2. Bidirectional Seed Averages (Overall Performance)

For each seed, we compute the average of the two directions (S1 &rarr; S2 and S2 &rarr; S1) to obtain the robust cross-session performance.

| Model | Metric | Seed 42 Avg | Seed 2026 Avg | Seed 2705 Avg | Overall (Mean &plusmn; Std) |
|---|---|---|---|---|---|
"""

        # Store aggregated seed values for B1 and B6
        overall_stats = {"b1": {}, "b6": {}}

        for metric in METRIC_KEYS:
            for method_key in ["b1", "b6"]:
                overall_stats[method_key][metric] = []
                row_cells = []
                for seed in SEEDS:
                    m_s1s2 = tongji_data[method_key]["s1s2"][seed]
                    m_s2s1 = tongji_data[method_key]["s2s1"][seed]

                    if m_s1s2 and m_s2s1 and metric in m_s1s2 and metric in m_s2s1:
                        avg_val = (m_s1s2[metric] + m_s2s1[metric]) / 2.0
                        overall_stats[method_key][metric].append(avg_val)
                        row_cells.append(format_cell(avg_val))
                    else:
                        row_cells.append("N/A")

                vals = overall_stats[method_key][metric]
                mean_val, std_val = compute_mean_std(vals)
                method_lbl = "Baseline (B1)" if method_key == "b1" else "BNNeck + ArcFace (B6)"
                tongji_report += f"| {method_lbl} | {metric} | {' | '.join(row_cells)} | {format_cell(mean_val, std_val)} |\n"

        # Paired Delta Table
        tongji_report += """
## 3. Paired Performance Delta (B6 - B1)

A positive delta (pp = percentage points) indicates B6 outperformed B1.

| Metric | Seed 42 Delta | Seed 2026 Delta | Seed 2705 Delta | Overall Mean Delta |
|---|---|---|---|---|
"""
        for metric in METRIC_KEYS:
            deltas = []
            row_cells = []
            for i, seed in enumerate(SEEDS):
                b1_vals = overall_stats["b1"][metric]
                b6_vals = overall_stats["b6"][metric]
                if len(b1_vals) > i and len(b6_vals) > i:
                    d = b6_vals[i] - b1_vals[i]
                    deltas.append(d)
                    row_cells.append(format_cell_diff(d))
                else:
                    row_cells.append("N/A")
            mean_d = float(np.mean(deltas)) if deltas else 0.0
            tongji_report += f"| {metric} | {' | '.join(row_cells)} | {format_cell_diff(mean_d)} |\n"

        tongji_report += """
## 4. Key Takeaways and Insights
- **Protocol-Sensitivity Verdict**: Rather than providing a universal improvement, the BNNeck + ArcFace (B6) pipeline exhibits a degradation or neutral behavior compared to Baseline (B1) under the cross-session palm-class-disjoint protocol on Tongji.
- These results show that the BNNeck + ArcFace variant evaluated here does not transfer into a consistent cross-session improvement, reinforcing the need for protocol-sensitive benchmarking rather than single-protocol claims.
"""
    else:
        tongji_report = """# Tongji Palm-Class-Disjoint Cross-Session Evaluation Summary

Status: restart aggregation placeholder.

No valid restart metrics were found by the current aggregation script. This file must not be used as experimental evidence until metrics from the restart experiments are available and parsed correctly.

## Intended protocol

- Dataset: Tongji
- Protocol: palm-class-disjoint cross-session evaluation
- Seeds: 42, 2026, 2705
- Metrics: Rank-1, Rank-5, Macro-F1, EER, TAR@FAR=1e-2, TAR@FAR=1e-3

## Current claim status

No new result claim is made in this file. Tongji should be treated as primary cross-session evaluation, not as evidence for universal improvement.
"""

    with open(RESULTS_DIR / "tongji_subject_disjoint_summary.md", "w", encoding="utf-8") as f:
        f.write(tongji_report)
    print("Wrote tongji_subject_disjoint_summary.md")

    # -------------------------------------------------------------
    # 2. IITD Palm-Class-Disjoint Within-Session Aggregation
    # -------------------------------------------------------------
    iitd_data = {}
    for method in ["b1", "b6"]:
        iitd_data[method] = {}
        for seed in SEEDS:
            if method == "b1":
                dir_name = f"b1_resnet18_ce_supcon_iitd_subject_disjoint_within_seed{seed}"
            else:
                dir_name = f"b6_resnet18_bnneck_arcface_iitd_subject_disjoint_within_seed{seed}"

            metrics = get_metrics_from_dir(dir_name)
            iitd_data[method][seed] = metrics

    has_iitd_metrics = all(
        has_complete_metrics(iitd_data[method][seed])
        for method in ["b1", "b6"]
        for seed in SEEDS
    )

    if has_iitd_metrics:
        iitd_report = """# IITD Palm-Class-Disjoint Within-Session Evaluation Summary

This document aggregates evaluation metrics for Tier-1 models on the secondary IITD palm-class-disjoint within-session protocol across three random seeds: 42, 2026, and 2705.

- **Baseline (B1)**: ResNet18 trained with Cross-Entropy and Supervised Contrastive Loss.
- **BNNeck + ArcFace (B6)**: ResNet18 trained with BNNeck and ArcFace Loss.

## 1. Seed-wise Run Details

| Model | Metric | Seed 42 | Seed 2026 | Seed 2705 | Overall (Mean &plusmn; Std) |
|---|---|---|---|---|---|
"""
        overall_stats_iitd = {"b1": {}, "b6": {}}
        for metric in METRIC_KEYS:
            for method_key in ["b1", "b6"]:
                overall_stats_iitd[method_key][metric] = []
                row_cells = []
                for seed in SEEDS:
                    m = iitd_data[method_key][seed]
                    if m and metric in m:
                        val = m[metric]
                        overall_stats_iitd[method_key][metric].append(val)
                        row_cells.append(format_cell(val))
                    else:
                        row_cells.append("N/A")

                vals = overall_stats_iitd[method_key][metric]
                mean_val, std_val = compute_mean_std(vals)
                method_lbl = "Baseline (B1)" if method_key == "b1" else "BNNeck + ArcFace (B6)"
                iitd_report += f"| {method_lbl} | {metric} | {' | '.join(row_cells)} | {format_cell(mean_val, std_val)} |\n"

        # Paired Delta Table
        iitd_report += """
## 2. Paired Performance Delta (B6 - B1)

A positive delta (pp = percentage points) indicates B6 outperformed B1.

| Metric | Seed 42 Delta | Seed 2026 Delta | Seed 2705 Delta | Overall Mean Delta |
|---|---|---|---|---|
"""
        for metric in METRIC_KEYS:
            deltas = []
            row_cells = []
            for i, seed in enumerate(SEEDS):
                b1_vals = overall_stats_iitd["b1"][metric]
                b6_vals = overall_stats_iitd["b6"][metric]
                if len(b1_vals) > i and len(b6_vals) > i:
                    d = b6_vals[i] - b1_vals[i]
                    deltas.append(d)
                    row_cells.append(format_cell_diff(d))
                else:
                    row_cells.append("N/A")
            mean_d = float(np.mean(deltas)) if deltas else 0.0
            iitd_report += f"| {metric} | {' | '.join(row_cells)} | {format_cell_diff(mean_d)} |\n"

        iitd_report += """
## 3. Key Takeaways and Insights
- **Secondary Validation Verdict**: Superseded. The IITD gallery/probe construction was corrected after this legacy aggregator was written. Use `scripts/aggregate_iitd_rerun_results.py` and `docs/results/iitd_subject_disjoint_rerun_results.md` as the authoritative IITD evidence. The corrected IITD rerun shows a near-tie: B6 has Rank-1 +0.12 pp versus B1, slightly worse EER (+0.19 pp), and lower TAR@FAR=1e-3 (-0.72 pp). IITD remains secondary within-session palm-class-disjoint validation, not cross-session evidence or universal superiority evidence.
"""
    else:
        iitd_report = """# IITD Palm-Class-Disjoint Within-Dataset Evaluation Summary

Status: restart aggregation placeholder.

No valid restart metrics were found by the current aggregation script. This file must not be used as experimental evidence until metrics from the restart experiments are available and parsed correctly.

## Intended protocol

- Dataset: IITD
- Protocol: palm-class-disjoint within-dataset secondary validation
- Seeds: 42, 2026, 2705
- Metrics: Rank-1, Rank-5, Macro-F1, EER, TAR@FAR=1e-2, TAR@FAR=1e-3

## Current claim status

No new result claim is made in this file. IITD should be treated as secondary validation, not as evidence for cross-session robustness or universal improvement.
"""

    with open(RESULTS_DIR / "iitd_subject_disjoint_summary_SUPERSEDED_USE_RERUN.md", "w", encoding="utf-8") as f:
        f.write(iitd_report)
    print("Wrote iitd_subject_disjoint_summary_SUPERSEDED_USE_RERUN.md")

if __name__ == "__main__":
    main()
