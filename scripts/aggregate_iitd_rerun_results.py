from pathlib import Path
import csv
import json
import statistics as stats

ROOT = Path(".").resolve()
EXP = ROOT / "experiments"
OUT = ROOT / "docs" / "results"
OUT.mkdir(parents=True, exist_ok=True)

RUNS = [
    ("B1", "ResNet18 + CE + SupCon", 42, "b1_resnet18_ce_supcon_iitd_subject_disjoint_within_seed42"),
    ("B1", "ResNet18 + CE + SupCon", 2026, "b1_resnet18_ce_supcon_iitd_subject_disjoint_within_seed2026"),
    ("B1", "ResNet18 + CE + SupCon", 2705, "b1_resnet18_ce_supcon_iitd_subject_disjoint_within_seed2705"),
    ("B6", "ResNet18 + BNNeck + ArcFace", 42, "b6_resnet18_bnneck_arcface_iitd_subject_disjoint_within_seed42"),
    ("B6", "ResNet18 + BNNeck + ArcFace", 2026, "b6_resnet18_bnneck_arcface_iitd_subject_disjoint_within_seed2026"),
    ("B6", "ResNet18 + BNNeck + ArcFace", 2705, "b6_resnet18_bnneck_arcface_iitd_subject_disjoint_within_seed2705"),
]

METRICS = [
    ("Rank-1", ["rank1", "Rank-1", "rank_1"]),
    ("Rank-5", ["rank5", "Rank-5", "rank_5"]),
    ("Macro-F1", ["macro_f1", "Macro-F1", "macro-f1"]),
    ("EER", ["eer", "EER"]),
    ("TAR@FAR=1e-2", ["tar_far_1e_2", "TAR@FAR=1e-2", "tar@far=1e-2"]),
    ("TAR@FAR=1e-3", ["tar_far_1e_3", "TAR@FAR=1e-3", "tar@far=1e-3"]),
]

def read_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))

def get_metric(d: dict, keys: list[str]) -> float:
    for k in keys:
        if k in d:
            v = float(d[k])
            return v * 100.0 if abs(v) <= 1.5 else v
    raise KeyError(f"Missing metric keys {keys}; available keys={sorted(d.keys())}")

def mean_std(vals):
    if len(vals) == 1:
        return vals[0], 0.0
    return stats.mean(vals), stats.stdev(vals)

rows = []
for method, label, seed, run_dir in RUNS:
    metrics_path = EXP / run_dir / "metrics.json"
    d = read_json(metrics_path)
    row = {
        "method": method,
        "method_label": label,
        "seed": seed,
        "run_dir": run_dir,
        "metrics_path": str(metrics_path.relative_to(ROOT)).replace("\\", "/"),
    }
    for out_name, keys in METRICS:
        row[out_name] = get_metric(d, keys)
    # Optional runtime metadata, schema-tolerant.
    for key in ["avg_inference_time_ms", "average_inference_time_ms", "inference_time_ms", "avg_time_ms"]:
        if key in d:
            row["avg_inference_time_ms"] = float(d[key])
            break
    rows.append(row)

runs_csv = OUT / "iitd_subject_disjoint_rerun_runs.csv"
with runs_csv.open("w", newline="", encoding="utf-8") as f:
    fieldnames = ["method", "method_label", "seed", "run_dir", "metrics_path"] + [m[0] for m in METRICS] + ["avg_inference_time_ms"]
    w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
    w.writeheader()
    for r in rows:
        w.writerow(r)

summary_rows = []
for method in ["B1", "B6"]:
    sub = [r for r in rows if r["method"] == method]
    label = sub[0]["method_label"]
    out = {"method": method, "method_label": label}
    for metric, _ in METRICS:
        vals = [r[metric] for r in sub]
        mu, sd = mean_std(vals)
        out[f"{metric}_mean"] = mu
        out[f"{metric}_std"] = sd
    summary_rows.append(out)

summary_csv = OUT / "iitd_subject_disjoint_rerun_summary.csv"
with summary_csv.open("w", newline="", encoding="utf-8") as f:
    fieldnames = ["method", "method_label"]
    for metric, _ in METRICS:
        fieldnames += [f"{metric}_mean", f"{metric}_std"]
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    for r in summary_rows:
        w.writerow(r)

delta_rows = []
b1_by_seed = {r["seed"]: r for r in rows if r["method"] == "B1"}
b6_by_seed = {r["seed"]: r for r in rows if r["method"] == "B6"}
for seed in [42, 2026, 2705]:
    out = {"seed": seed}
    for metric, _ in METRICS:
        out[f"delta_{metric}_B6_minus_B1"] = b6_by_seed[seed][metric] - b1_by_seed[seed][metric]
    delta_rows.append(out)

delta_csv = OUT / "iitd_subject_disjoint_rerun_delta_b6_minus_b1.csv"
with delta_csv.open("w", newline="", encoding="utf-8") as f:
    fieldnames = ["seed"] + [f"delta_{m[0]}_B6_minus_B1" for m in METRICS]
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    for r in delta_rows:
        w.writerow(r)

def fmt(x):
    return f"{x:.2f}"

def mean_std_cell(method, metric):
    row = [r for r in summary_rows if r["method"] == method][0]
    return f"{fmt(row[f'{metric}_mean'])} $\\pm$ {fmt(row[f'{metric}_std'])}"

md = []
md.append("# IITD Palm-Class-Disjoint Within-Session Rerun Results")
md.append("")
md.append("These results were regenerated after fixing the IITD gallery/probe construction so that each held-out palm class appears in both gallery and probe with no image overlap. IITD remains secondary within-session validation and is not cross-session evidence.")
md.append("")
md.append("## Per-seed results")
md.append("")
md.append("| Method | Seed | Rank-1 | Rank-5 | Macro-F1 | EER | TAR@FAR=1e-2 | TAR@FAR=1e-3 |")
md.append("|---|---:|---:|---:|---:|---:|---:|---:|")
for r in rows:
    md.append(
        f"| {r['method']} {r['method_label']} | {r['seed']} | "
        f"{fmt(r['Rank-1'])} | {fmt(r['Rank-5'])} | {fmt(r['Macro-F1'])} | "
        f"{fmt(r['EER'])} | {fmt(r['TAR@FAR=1e-2'])} | {fmt(r['TAR@FAR=1e-3'])} |"
    )

md.append("")
md.append("## Three-seed mean +/- standard deviation")
md.append("")
md.append("| Method | Rank-1 | Rank-5 | Macro-F1 | EER | TAR@FAR=1e-2 | TAR@FAR=1e-3 |")
md.append("|---|---:|---:|---:|---:|---:|---:|")
for method in ["B1", "B6"]:
    label = [r for r in summary_rows if r["method"] == method][0]["method_label"]
    md.append(
        f"| {method} {label} | "
        f"{mean_std_cell(method, 'Rank-1')} | {mean_std_cell(method, 'Rank-5')} | "
        f"{mean_std_cell(method, 'Macro-F1')} | {mean_std_cell(method, 'EER')} | "
        f"{mean_std_cell(method, 'TAR@FAR=1e-2')} | {mean_std_cell(method, 'TAR@FAR=1e-3')} |"
    )

md.append("")
md.append("## Paired B6 minus B1 deltas")
md.append("")
md.append("Positive Rank/TAR/Macro-F1 deltas favor B6. Positive EER deltas are worse for B6.")
md.append("")
md.append("| Seed | Delta Rank-1 | Delta Rank-5 | Delta Macro-F1 | Delta EER | Delta TAR@FAR=1e-2 | Delta TAR@FAR=1e-3 |")
md.append("|---:|---:|---:|---:|---:|---:|---:|")
for r in delta_rows:
    md.append(
        f"| {r['seed']} | "
        f"{fmt(r['delta_Rank-1_B6_minus_B1'])} | {fmt(r['delta_Rank-5_B6_minus_B1'])} | "
        f"{fmt(r['delta_Macro-F1_B6_minus_B1'])} | {fmt(r['delta_EER_B6_minus_B1'])} | "
        f"{fmt(r['delta_TAR@FAR=1e-2_B6_minus_B1'])} | {fmt(r['delta_TAR@FAR=1e-3_B6_minus_B1'])} |"
    )

md.append("")
md.append("## Interpretation")
md.append("")
md.append("The rerun supports a near-tie interpretation rather than a clear B6 improvement. B6 has a very small mean Rank-1 gain over B1, but it does not improve the low-FAR verification metrics on average and has slightly worse mean EER. This is consistent with the paper's protocol-sensitive conclusion and should not be written as universal superiority of BNNeck + ArcFace.")

md_path = OUT / "iitd_subject_disjoint_rerun_results.md"
md_path.write_text("\n".join(md) + "\n", encoding="utf-8")

tex = []
tex.append(r"\begin{table*}[t]")
tex.append(r"\centering")
tex.append(r"\caption{IITD palm-class-disjoint within-session rerun after gallery/probe split correction. Values are mean $\pm$ standard deviation over three seeds. Lower EER is better; higher values are better for all other metrics.}")
tex.append(r"\label{tab:iitd_rerun}")
tex.append(r"\begin{tabular}{lcccccc}")
tex.append(r"\toprule")
tex.append(r"Method & Rank-1 & Rank-5 & Macro-F1 & EER & TAR@FAR=$10^{-2}$ & TAR@FAR=$10^{-3}$ \\")
tex.append(r"\midrule")
for method in ["B1", "B6"]:
    label = [r for r in summary_rows if r["method"] == method][0]["method_label"]
    tex.append(
        f"{method} {label} & "
        f"{mean_std_cell(method, 'Rank-1')} & {mean_std_cell(method, 'Rank-5')} & "
        f"{mean_std_cell(method, 'Macro-F1')} & {mean_std_cell(method, 'EER')} & "
        f"{mean_std_cell(method, 'TAR@FAR=1e-2')} & {mean_std_cell(method, 'TAR@FAR=1e-3')} \\\\"
    )
tex.append(r"\bottomrule")
tex.append(r"\end{tabular}")
tex.append(r"\end{table*}")

tex_path = OUT / "iitd_subject_disjoint_rerun_table.tex"
tex_path.write_text("\n".join(tex) + "\n", encoding="utf-8")

print(f"Wrote {runs_csv}")
print(f"Wrote {summary_csv}")
print(f"Wrote {delta_csv}")
print(f"Wrote {md_path}")
print(f"Wrote {tex_path}")