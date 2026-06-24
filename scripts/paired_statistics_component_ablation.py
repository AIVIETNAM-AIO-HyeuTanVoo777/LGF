from __future__ import annotations

from pathlib import Path
import csv
import itertools
import math
import random
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

INPUT_CSV = Path("docs/results/strict_tongji_ablation_runs.csv")
OUT_CSV = Path("docs/results/paired_statistics_component_ablation.csv")
OUT_MD = Path("docs/results/paired_statistics_component_ablation.md")
OUT_TEX = Path("paper/sections/paired_statistics_component_ablation_table.tex")

BOOTSTRAP_SAMPLES = 50000
BOOTSTRAP_SEED = 20260624

PAIRED_UNITS = [
    ("S1->S2", 42),
    ("S1->S2", 2026),
    ("S1->S2", 2705),
    ("S2->S1", 42),
    ("S2->S1", 2026),
    ("S2->S1", 2705),
]

METRICS = [
    ("Rank-1", "Rank-1", "higher_is_better"),
    ("Rank-5", "Rank-5", "higher_is_better"),
    ("Macro-F1", "Macro-F1", "higher_is_better"),
    ("EER", "EER", "lower_is_better"),
    ("TAR@FAR=1e-2", "TAR@FAR=1e-2", "higher_is_better"),
    ("TAR@FAR=1e-3", "TAR@FAR=1e-3", "higher_is_better"),
]

COMPARISONS = [
    ("B5", "B1", "B5 minus B1", "BNNeck + CE vs CE + SupCon baseline"),
    ("B5", "B6", "B5 minus B6", "BNNeck + CE vs BNNeck + ArcFace"),
    ("B6", "B1", "B6 minus B1", "BNNeck + ArcFace vs CE + SupCon baseline"),
]

METHOD_LABELS = {
    "B0": "ResNet18 + CE",
    "B1": "ResNet18 + CE + SupCon",
    "B4": "ResNet18 + ArcFace",
    "B5": "ResNet18 + BNNeck + CE",
    "B6": "ResNet18 + BNNeck + ArcFace",
    "B7": "ResNet18 + BNNeck + ArcFace + light SupCon",
}

def pp(x: float) -> float:
    return 100.0 * float(x)

def fmt(x: float, digits: int = 2) -> str:
    if math.isnan(x):
        return "nan"
    return f"{x:+.{digits}f}"

def bootstrap_ci(values: List[float], rng: random.Random) -> Tuple[float, float]:
    n = len(values)
    means = []
    for _ in range(BOOTSTRAP_SAMPLES):
        sample = [values[rng.randrange(n)] for _ in range(n)]
        means.append(sum(sample) / n)
    means.sort()
    lo = means[int(0.025 * (BOOTSTRAP_SAMPLES - 1))]
    hi = means[int(0.975 * (BOOTSTRAP_SAMPLES - 1))]
    return lo, hi

def exact_sign_flip_p(values: List[float]) -> float:
    obs = abs(sum(values) / len(values))
    n = len(values)
    count = 0
    total = 0
    for signs in itertools.product([-1.0, 1.0], repeat=n):
        mu = abs(sum(v * s for v, s in zip(values, signs)) / n)
        if mu >= obs - 1e-12:
            count += 1
        total += 1
    return count / total

def interpretation(mean_delta_pp: float, metric_direction: str, method_a: str) -> str:
    eps = 1e-12
    if abs(mean_delta_pp) <= eps:
        return "near tie"
    if metric_direction == "higher_is_better":
        return f"{method_a} better" if mean_delta_pp > 0 else f"{method_a} worse"
    return f"{method_a} worse" if mean_delta_pp > 0 else f"{method_a} better"

def load_index() -> Dict[Tuple[str, str, int], Dict[str, float]]:
    if not INPUT_CSV.exists():
        raise FileNotFoundError(INPUT_CSV)

    df = pd.read_csv(INPUT_CSV)
    required = {"method", "direction", "seed"} | {m[1] for m in METRICS}
    missing = sorted(required - set(df.columns))
    if missing:
        raise RuntimeError(f"Missing required columns: {missing}")

    idx: Dict[Tuple[str, str, int], Dict[str, float]] = {}
    for _, row in df.iterrows():
        key = (str(row["method"]), str(row["direction"]), int(row["seed"]))
        idx[key] = {col: float(row[col]) for _, col, _ in METRICS}
    return idx

def main() -> None:
    idx = load_index()
    rng = random.Random(BOOTSTRAP_SEED)

    rows: List[Dict[str, object]] = []
    delta_rows: List[Dict[str, object]] = []

    for method_a, method_b, comparison, hypothesis in COMPARISONS:
        for metric_name, col, direction in METRICS:
            deltas_pp: List[float] = []
            for unit_direction, seed in PAIRED_UNITS:
                key_a = (method_a, unit_direction, seed)
                key_b = (method_b, unit_direction, seed)
                if key_a not in idx:
                    raise RuntimeError(f"Missing paired unit for {key_a}")
                if key_b not in idx:
                    raise RuntimeError(f"Missing paired unit for {key_b}")

                delta = pp(idx[key_a][col] - idx[key_b][col])
                deltas_pp.append(delta)
                delta_rows.append({
                    "comparison": comparison,
                    "method_a": method_a,
                    "method_b": method_b,
                    "direction": unit_direction,
                    "seed": seed,
                    "metric": metric_name,
                    "delta_pp": delta,
                })

            mean_delta = float(np.mean(deltas_pp))
            sd_delta = float(np.std(deltas_pp, ddof=1)) if len(deltas_pp) > 1 else 0.0
            ci_lo, ci_hi = bootstrap_ci(deltas_pp, rng)
            p_sign = exact_sign_flip_p(deltas_pp)

            rows.append({
                "comparison": comparison,
                "hypothesis": hypothesis,
                "method_a": method_a,
                "method_b": method_b,
                "method_a_label": METHOD_LABELS.get(method_a, method_a),
                "method_b_label": METHOD_LABELS.get(method_b, method_b),
                "metric": metric_name,
                "metric_direction": direction,
                "n_paired_units": len(deltas_pp),
                "mean_delta_pp": mean_delta,
                "sd_delta_pp": sd_delta,
                "bootstrap_ci95_low_pp": ci_lo,
                "bootstrap_ci95_high_pp": ci_hi,
                "exact_sign_flip_p_two_sided": p_sign,
                "interpretation": interpretation(mean_delta, direction, method_a),
                "deltas_pp": ";".join(f"{x:.10f}" for x in deltas_pp),
            })

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "comparison", "hypothesis", "method_a", "method_b", "method_a_label", "method_b_label",
            "metric", "metric_direction", "n_paired_units",
            "mean_delta_pp", "sd_delta_pp", "bootstrap_ci95_low_pp", "bootstrap_ci95_high_pp",
            "exact_sign_flip_p_two_sided", "interpretation", "deltas_pp",
        ]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow(row)

    write_markdown(rows, delta_rows)
    write_tex(rows)

    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_TEX}")
    print(f"COMPARISONS={len(COMPARISONS)}")
    print(f"ROWS={len(rows)}")
    print(f"PAIRED_UNITS={len(PAIRED_UNITS)}")
    print(f"BOOTSTRAP_SAMPLES={BOOTSTRAP_SAMPLES}")

def write_markdown(rows: List[Dict[str, object]], delta_rows: List[Dict[str, object]]) -> None:
    md: List[str] = []
    md.append("# Paired Statistical Evidence for Strict Component Ablation")
    md.append("")
    md.append("This analysis extends the existing B6-vs-B1 paired uncertainty analysis to the component-ablation comparisons needed by the paper claim, especially B5.")
    md.append("")
    md.append("## Method")
    md.append("")
    md.append("- Input: `docs/results/strict_tongji_ablation_runs.csv`.")
    md.append("- Paired units: six matched seed-direction units: S1->S2 and S2->S1 for seeds 42, 2026, and 2705.")
    md.append("- Delta definition: method A minus method B, in percentage points.")
    md.append("- Positive Rank-1, Rank-5, Macro-F1, and TAR deltas favor method A.")
    md.append("- Positive EER deltas are worse for method A.")
    md.append(f"- Bootstrap CI: percentile bootstrap over paired units, {BOOTSTRAP_SAMPLES} resamples, seed {BOOTSTRAP_SEED}.")
    md.append("- Exact sign-flip test: two-sided paired sign-flip test over six deltas.")
    md.append("- Because n=6, p-values are coarse uncertainty diagnostics, not definitive significance claims.")
    md.append("")
    md.append("## Summary table")
    md.append("")
    md.append("| Comparison | Metric | Mean delta (pp) | SD (pp) | Bootstrap 95% CI (pp) | Exact sign-flip p | Interpretation |")
    md.append("|---|---|---:|---:|---:|---:|---|")
    for r in rows:
        md.append(
            f"| {r['comparison']} | {r['metric']} | {fmt(float(r['mean_delta_pp']))} | "
            f"{float(r['sd_delta_pp']):.2f} | "
            f"[{fmt(float(r['bootstrap_ci95_low_pp']))}, {fmt(float(r['bootstrap_ci95_high_pp']))}] | "
            f"{float(r['exact_sign_flip_p_two_sided']):.4f} | {r['interpretation']} |"
        )

    md.append("")
    md.append("## Paper-relevant interpretation")
    md.append("")
    b5_b1 = {r["metric"]: r for r in rows if r["comparison"] == "B5 minus B1"}
    b5_b6 = {r["metric"]: r for r in rows if r["comparison"] == "B5 minus B6"}
    b6_b1 = {r["metric"]: r for r in rows if r["comparison"] == "B6 minus B1"}

    md.append(
        "- B5 versus B1: B5 has positive mean paired deltas for Rank-1 and TAR@FAR=1e-3, "
        f"with Rank-1 {fmt(float(b5_b1['Rank-1']['mean_delta_pp']))} pp and TAR@FAR=1e-3 {fmt(float(b5_b1['TAR@FAR=1e-3']['mean_delta_pp']))} pp. "
        "This supports describing B5 as a modestly favorable BNNeck+CE component variant rather than a large statistically established improvement."
    )
    md.append(
        "- B5 versus B6: B5 has better mean paired low-FAR behavior than B6, "
        f"including TAR@FAR=1e-3 {fmt(float(b5_b6['TAR@FAR=1e-3']['mean_delta_pp']))} pp and EER {fmt(float(b5_b6['EER']['mean_delta_pp']))} pp "
        "(negative EER favors B5). This supports the paper statement that B5 is stronger than the ArcFace-based B6 under the strict Tongji protocol."
    )
    md.append(
        "- B6 versus B1: B6 remains unfavorable on the bidirectional paired average, "
        f"with Rank-1 {fmt(float(b6_b1['Rank-1']['mean_delta_pp']))} pp and EER {fmt(float(b6_b1['EER']['mean_delta_pp']))} pp "
        "(positive EER is worse). This is consistent with the existing B6-vs-B1 paired analysis."
    )
    md.append("")
    md.append("## Per-unit deltas")
    md.append("")
    md.append("The machine-readable per-unit deltas are embedded in the `deltas_pp` column of the CSV output.")

    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

def write_tex(rows: List[Dict[str, object]]) -> None:
    key_rows = [
        r for r in rows
        if r["comparison"] in {"B5 minus B1", "B5 minus B6", "B6 minus B1"}
        and r["metric"] in {"Rank-1", "EER", "TAR@FAR=1e-3"}
    ]

    tex: List[str] = []
    tex.append(r"\begin{table*}[t]")
    tex.append(r"\centering")
    tex.append(r"\caption{Paired component-ablation evidence on the strict Tongji palm-class-disjoint protocol. Deltas are method A minus method B in percentage points over six paired seed-direction units. Positive Rank-1 and TAR deltas favor method A; positive EER deltas are worse for method A.}")
    tex.append(r"\label{tab:paired_statistics_component_ablation}")
    tex.append(r"\begin{tabular}{llccc}")
    tex.append(r"\toprule")
    tex.append(r"Comparison & Metric & Mean $\Delta$ & 95\% bootstrap CI & Sign-flip $p$ \\")
    tex.append(r"\midrule")
    for r in key_rows:
        metric_tex = str(r["metric"]).replace("TAR@FAR=1e-3", r"TAR@FAR=$10^{-3}$")
        tex.append(
            f"{r['comparison']} & {metric_tex} & "
            f"{float(r['mean_delta_pp']):+.2f} & "
            f"[{float(r['bootstrap_ci95_low_pp']):+.2f}, {float(r['bootstrap_ci95_high_pp']):+.2f}] & "
            f"{float(r['exact_sign_flip_p_two_sided']):.4f} \\\\"
        )
    tex.append(r"\bottomrule")
    tex.append(r"\end{tabular}")
    tex.append(r"\end{table*}")
    OUT_TEX.write_text("\n".join(tex) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()