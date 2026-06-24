from __future__ import annotations

from pathlib import Path
import csv
import math
from typing import Dict, List

import pandas as pd

INPUT_CSV = Path("docs/results/strict_tongji_ablation_runs.csv")
OUT_CSV = Path("docs/results/strict_tongji_ablation_by_direction.csv")
OUT_MD = Path("docs/results/strict_tongji_ablation_by_direction.md")
OUT_TEX = Path("paper/sections/strict_tongji_ablation_by_direction_table.tex")

METRICS = [
    ("Rank-1", "Rank-1", "higher"),
    ("Rank-5", "Rank-5", "higher"),
    ("Macro-F1", "Macro-F1", "higher"),
    ("EER", "EER", "lower"),
    ("TAR@FAR=1e-2", "TAR@FAR=1e-2", "higher"),
    ("TAR@FAR=1e-3", "TAR@FAR=1e-3", "higher"),
]

METHOD_ORDER = ["B0", "B1", "B4", "B5", "B6", "B7"]
PAPER_METHODS = ["B1", "B5", "B6"]

METHOD_LABELS = {
    "B0": "ResNet18 + CE",
    "B1": "ResNet18 + CE + SupCon",
    "B4": "ResNet18 + ArcFace",
    "B5": "ResNet18 + BNNeck + CE",
    "B6": "ResNet18 + BNNeck + ArcFace",
    "B7": "ResNet18 + BNNeck + ArcFace + light SupCon",
}

DIRECTIONS = ["S1->S2", "S2->S1"]


def pct(x: float) -> float:
    return 100.0 * float(x)


def mean_sd(values: List[float]) -> tuple[float, float]:
    s = pd.Series(values, dtype="float64")
    return float(s.mean()), float(s.std(ddof=1))


def fmt_mean_sd(mean: float, sd: float) -> str:
    return f"{mean:.2f} $\\pm$ {sd:.2f}"


def fmt_md(mean: float, sd: float) -> str:
    return f"{mean:.2f} +/- {sd:.2f}"


def main() -> None:
    if not INPUT_CSV.exists():
        raise FileNotFoundError(INPUT_CSV)

    df = pd.read_csv(INPUT_CSV)
    required = {"method", "method_label", "direction", "seed", "status"} | {m[1] for m in METRICS}
    missing = sorted(required - set(df.columns))
    if missing:
        raise RuntimeError(f"Missing required columns: {missing}")

    bad_status = df[df["status"].astype(str).str.upper() != "OK"]
    if not bad_status.empty:
        raise RuntimeError(f"Found non-OK runs:\n{bad_status[['method','direction','seed','status']]}")

    rows: List[Dict[str, object]] = []

    for method in METHOD_ORDER:
        for direction in DIRECTIONS:
            sub = df[(df["method"] == method) & (df["direction"] == direction)].copy()
            if len(sub) != 3:
                raise RuntimeError(f"Expected 3 seeds for {method} {direction}, found {len(sub)}")

            out: Dict[str, object] = {
                "method": method,
                "method_label": METHOD_LABELS.get(method, str(sub.iloc[0]["method_label"])),
                "direction": direction,
                "n_seeds": len(sub),
                "seeds": ",".join(str(int(x)) for x in sorted(sub["seed"].tolist())),
            }

            for metric_name, col, _ in METRICS:
                vals = [pct(v) for v in sub[col].tolist()]
                mu, sd = mean_sd(vals)
                out[f"{metric_name}_mean_pp"] = mu
                out[f"{metric_name}_sd_pp"] = sd

            rows.append(out)

    write_csv(rows)
    write_md(rows)
    write_tex(rows)

    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_TEX}")
    print(f"ROWS={len(rows)}")
    print("METHODS=" + ",".join(METHOD_ORDER))
    print("DIRECTIONS=" + ",".join(DIRECTIONS))


def write_csv(rows: List[Dict[str, object]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = ["method", "method_label", "direction", "n_seeds", "seeds"]
    for metric_name, _, _ in METRICS:
        fieldnames.extend([f"{metric_name}_mean_pp", f"{metric_name}_sd_pp"])

    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def write_md(rows: List[Dict[str, object]]) -> None:
    md: List[str] = []
    md.append("# Strict Tongji Ablation by Direction")
    md.append("")
    md.append("This table summarizes the strict Tongji palm-class-disjoint ablation separately for S1->S2 and S2->S1.")
    md.append("")
    md.append("- Input: `docs/results/strict_tongji_ablation_runs.csv`.")
    md.append("- Values are mean ± sample standard deviation over three seeds: 42, 2026, and 2705.")
    md.append("- Higher is better for Rank-1, Rank-5, Macro-F1, and TAR. Lower is better for EER.")
    md.append("- This by-direction view is used to support the session-direction sensitivity analysis.")
    md.append("")
    md.append("## Full by-direction summary")
    md.append("")
    md.append("| Method | Direction | Rank-1 | Rank-5 | Macro-F1 | EER | TAR@FAR=1e-2 | TAR@FAR=1e-3 |")
    md.append("|---|---|---:|---:|---:|---:|---:|---:|")

    for r in rows:
        md.append(
            f"| {r['method']} {r['method_label']} | {r['direction']} | "
            f"{fmt_md(float(r['Rank-1_mean_pp']), float(r['Rank-1_sd_pp']))} | "
            f"{fmt_md(float(r['Rank-5_mean_pp']), float(r['Rank-5_sd_pp']))} | "
            f"{fmt_md(float(r['Macro-F1_mean_pp']), float(r['Macro-F1_sd_pp']))} | "
            f"{fmt_md(float(r['EER_mean_pp']), float(r['EER_sd_pp']))} | "
            f"{fmt_md(float(r['TAR@FAR=1e-2_mean_pp']), float(r['TAR@FAR=1e-2_sd_pp']))} | "
            f"{fmt_md(float(r['TAR@FAR=1e-3_mean_pp']), float(r['TAR@FAR=1e-3_sd_pp']))} |"
        )

    md.append("")
    md.append("## Paper compact subset")
    md.append("")
    md.append("The paper table reports B1, B5, and B6 because these are the baseline, the strongest strict component variant, and the originally evaluated BNNeck+ArcFace variant.")
    md.append("")

    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")


def write_tex(rows: List[Dict[str, object]]) -> None:
    paper_rows = [r for r in rows if r["method"] in PAPER_METHODS]

    tex: List[str] = []
    tex.append(r"\begin{table*}[t]")
    tex.append(r"\centering")
    tex.append(r"\caption{Strict Tongji palm-class-disjoint ablation by session direction. Values are mean $\pm$ standard deviation over three seeds. Lower EER is better; higher values are better for all other metrics. The table focuses on B1, B5, and B6 to highlight the baseline, the strongest tested component variant, and the BNNeck+ArcFace variant.}")
    tex.append(r"\label{tab:strict_tongji_ablation_by_direction}")
    tex.append(r"\resizebox{\textwidth}{!}{%")
    tex.append(r"\begin{tabular}{llccccc}")
    tex.append(r"\toprule")
    tex.append(r"Method & Direction & Rank-1 & Macro-F1 & EER & TAR@FAR=$10^{-2}$ & TAR@FAR=$10^{-3}$ \\")
    tex.append(r"\midrule")

    for r in paper_rows:
        method = f"{r['method']} {r['method_label']}"
        direction = str(r["direction"]).replace("->", r"$\rightarrow$")
        tex.append(
            f"{method} & {direction} & "
            f"{fmt_mean_sd(float(r['Rank-1_mean_pp']), float(r['Rank-1_sd_pp']))} & "
            f"{fmt_mean_sd(float(r['Macro-F1_mean_pp']), float(r['Macro-F1_sd_pp']))} & "
            f"{fmt_mean_sd(float(r['EER_mean_pp']), float(r['EER_sd_pp']))} & "
            f"{fmt_mean_sd(float(r['TAR@FAR=1e-2_mean_pp']), float(r['TAR@FAR=1e-2_sd_pp']))} & "
            f"{fmt_mean_sd(float(r['TAR@FAR=1e-3_mean_pp']), float(r['TAR@FAR=1e-3_sd_pp']))} \\\\"
        )

    tex.append(r"\bottomrule")
    tex.append(r"\end{tabular}%")
    tex.append(r"}")
    tex.append(r"\end{table*}")

    OUT_TEX.write_text("\n".join(tex) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()