from pathlib import Path
import math
import numpy as np
import pandas as pd

RUNS_CSV = Path("docs/results/strict_tongji_ablation_runs.csv")
OUT_CSV = Path("docs/results/strict_tongji_failure_tail_table.csv")
OUT_MD = Path("docs/results/strict_tongji_failure_tail_table.md")
OUT_TEX = Path("paper/sections/strict_tongji_failure_tail_table.tex")

METHODS = ["B1", "B5", "B6"]
COMPARISONS = [("B5", "B1"), ("B6", "B1")]
DIRECTIONS = ["S1->S2", "S2->S1"]


def require_columns(df, cols, where):
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise ValueError(f"{where} missing columns: {missing}; existing={df.columns.tolist()}")


def metric_as_percent(x):
    x = float(x)
    return x * 100.0 if abs(x) <= 1.5 else x


def read_score_summary(metrics_path):
    score_path = Path(metrics_path).with_name("scores.csv")
    if not score_path.exists():
        raise FileNotFoundError(f"Missing scores.csv: {score_path}")

    scores = pd.read_csv(score_path, usecols=["score", "label"])
    require_columns(scores, ["score", "label"], str(score_path))

    genuine = scores.loc[scores["label"] == 1, "score"].to_numpy(dtype=float)
    impostor = scores.loc[scores["label"] == 0, "score"].to_numpy(dtype=float)

    if len(genuine) == 0 or len(impostor) == 0:
        raise ValueError(f"Empty genuine or impostor scores in {score_path}")

    genuine_mean = float(np.mean(genuine))
    impostor_mean = float(np.mean(impostor))
    genuine_std = float(np.std(genuine, ddof=1))
    impostor_std = float(np.std(impostor, ddof=1))
    pooled = math.sqrt(0.5 * (genuine_std * genuine_std + impostor_std * impostor_std))
    dprime = float((genuine_mean - impostor_mean) / pooled) if pooled > 0 else float("nan")

    return {
        "score_path": str(score_path),
        "n_genuine": int(len(genuine)),
        "n_impostor": int(len(impostor)),
        "genuine_mean": genuine_mean,
        "genuine_q001": float(np.quantile(genuine, 0.001)),
        "impostor_mean": impostor_mean,
        "impostor_q999": float(np.quantile(impostor, 0.999)),
        "impostor_q9999": float(np.quantile(impostor, 0.9999)),
        "dprime": dprime,
    }


def signed(x, digits=3):
    return f"{float(x):+.{digits}f}"


def signed_pp(x, digits=2):
    return f"{float(x):+.{digits}f}"


def direction_tex(direction):
    if direction == "S1->S2":
        return r"S1$\rightarrow$S2"
    if direction == "S2->S1":
        return r"S2$\rightarrow$S1"
    return direction


def comparison_tex(comparison):
    return comparison.replace(" minus ", r"$-$")


def interpretation(comparison, direction):
    if comparison == "B5 minus B1" and direction == "S1->S2":
        return "BNNeck+CE improves low-FAR TAR in this direction."
    if comparison == "B5 minus B1" and direction == "S2->S1":
        return "BNNeck+CE gain does not transfer to the reverse direction."
    if comparison == "B6 minus B1" and direction == "S1->S2":
        return "BNNeck+ArcFace shows only direction-limited low-FAR behavior."
    if comparison == "B6 minus B1" and direction == "S2->S1":
        return "BNNeck+ArcFace degrades the reverse-direction low-FAR result."
    return "Direction-dependent score-tail behavior."


def main():
    if not RUNS_CSV.exists():
        raise FileNotFoundError(f"Missing input: {RUNS_CSV}")

    runs = pd.read_csv(RUNS_CSV)
    require_columns(
        runs,
        ["method", "method_label", "direction", "seed", "status", "TAR@FAR=1e-3", "EER", "metrics_path"],
        str(RUNS_CSV),
    )

    sub = runs[runs["method"].isin(METHODS)].copy()
    if len(sub) != 18:
        raise ValueError(f"Expected 18 rows for B1/B5/B6; found {len(sub)}")

    per_run_rows = []
    for _, row in sub.iterrows():
        score_summary = read_score_summary(str(row["metrics_path"]))
        base = {
            "method": row["method"],
            "method_label": row["method_label"],
            "direction": row["direction"],
            "seed": int(row["seed"]),
            "tar_far_1e_3_percent": metric_as_percent(row["TAR@FAR=1e-3"]),
            "eer_percent": metric_as_percent(row["EER"]),
            "metrics_path": row["metrics_path"],
        }
        base.update(score_summary)
        per_run_rows.append(base)

    per_run = pd.DataFrame(per_run_rows)

    delta_rows = []
    for method_a, method_b in COMPARISONS:
        for direction in DIRECTIONS:
            a_rows = per_run[(per_run["method"] == method_a) & (per_run["direction"] == direction)]
            b_rows = per_run[(per_run["method"] == method_b) & (per_run["direction"] == direction)]
            common_seeds = sorted(set(a_rows["seed"]).intersection(set(b_rows["seed"])))
            if len(common_seeds) != 3:
                raise ValueError(f"Expected 3 common seeds for {method_a}-{method_b} {direction}; found {common_seeds}")

            seed_rows = []
            for seed in common_seeds:
                a = a_rows[a_rows["seed"] == seed].iloc[0]
                b = b_rows[b_rows["seed"] == seed].iloc[0]
                seed_rows.append({
                    "delta_genuine_mean": a["genuine_mean"] - b["genuine_mean"],
                    "delta_genuine_q001": a["genuine_q001"] - b["genuine_q001"],
                    "delta_impostor_mean": a["impostor_mean"] - b["impostor_mean"],
                    "delta_impostor_q999": a["impostor_q999"] - b["impostor_q999"],
                    "delta_impostor_q9999": a["impostor_q9999"] - b["impostor_q9999"],
                    "delta_dprime": a["dprime"] - b["dprime"],
                    "delta_tar_far_1e_3_pp": a["tar_far_1e_3_percent"] - b["tar_far_1e_3_percent"],
                    "delta_eer_pp": a["eer_percent"] - b["eer_percent"],
                })

            d = pd.DataFrame(seed_rows)
            comparison = f"{method_a} minus {method_b}"
            out = {
                "comparison": comparison,
                "direction": direction,
                "n_paired_seeds": len(common_seeds),
                "interpretation": interpretation(comparison, direction),
            }
            for col in [
                "delta_genuine_mean",
                "delta_genuine_q001",
                "delta_impostor_mean",
                "delta_impostor_q999",
                "delta_impostor_q9999",
                "delta_dprime",
                "delta_tar_far_1e_3_pp",
                "delta_eer_pp",
            ]:
                out[col] = float(d[col].mean())
                out[col + "_std"] = float(d[col].std(ddof=1))
            delta_rows.append(out)

    delta = pd.DataFrame(delta_rows)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_TEX.parent.mkdir(parents=True, exist_ok=True)

    delta.to_csv(OUT_CSV, index=False)

    md = []
    md.append("# Strict Tongji Failure/Tail Analysis")
    md.append("")
    md.append("This table summarizes matched-seed score-tail deltas for B5 and B6 relative to B1 under the strict Tongji palm-class-disjoint protocol.")
    md.append("")
    md.append("- Input run table: `docs/results/strict_tongji_ablation_runs.csv`.")
    md.append("- Source scores: per-run `scores.csv` files located next to each metrics file.")
    md.append("- Each strict Tongji run contains 12,000 genuine and 1,428,000 impostor comparisons.")
    md.append("- Deltas are averaged over three matched seeds within each session direction.")
    md.append("- Positive TAR deltas favor the first method; positive EER deltas are worse for the first method.")
    md.append("- Positive impostor-tail deltas indicate a higher high-score impostor tail, which is generally unfavorable at low FAR.")
    md.append("")
    md.append("| Comparison | Direction | Delta genuine mean | Delta impostor q0.999 | Delta d-prime | Delta TAR@FAR=1e-3 (pp) | Interpretation |")
    md.append("|---|---:|---:|---:|---:|---:|---|")
    for _, r in delta.iterrows():
        md.append(
            f"| {r['comparison']} | {r['direction']} | "
            f"{signed(r['delta_genuine_mean'])} | "
            f"{signed(r['delta_impostor_q999'])} | "
            f"{signed(r['delta_dprime'])} | "
            f"{signed_pp(r['delta_tar_far_1e_3_pp'])} | "
            f"{r['interpretation']} |"
        )
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    tex = []
    tex.append(r"\begin{table*}[t]")
    tex.append(r"\centering")
    tex.append(r"\caption{Score-tail evidence for protocol-dependent component behavior on strict Tongji. Deltas are averaged over three matched seeds within each direction. Positive TAR deltas favor the first method; positive impostor-tail deltas indicate a higher high-score impostor tail and are generally unfavorable at low FAR.}")
    tex.append(r"\label{tab:strict_tongji_failure_tail}")
    tex.append(r"\small")
    tex.append(r"\setlength{\tabcolsep}{3pt}")
    tex.append(r"\begin{tabular}{llrrrrp{0.28\textwidth}}")
    tex.append(r"\toprule")
    tex.append(r"Comparison & Direction & $\Delta\mu_{\mathrm{gen}}$ & $\Delta q^{\mathrm{imp}}_{0.999}$ & $\Delta d'$ & $\Delta$TAR@FAR=$10^{-3}$ & Interpretation \\")
    tex.append(r"\midrule")
    for _, r in delta.iterrows():
        tex.append(
            f"{comparison_tex(r['comparison'])} & "
            f"{direction_tex(r['direction'])} & "
            f"{signed(r['delta_genuine_mean'])} & "
            f"{signed(r['delta_impostor_q999'])} & "
            f"{signed(r['delta_dprime'])} & "
            f"{signed_pp(r['delta_tar_far_1e_3_pp'])} pp & "
            f"{r['interpretation']} \\\\"
        )
    tex.append(r"\bottomrule")
    tex.append(r"\end{tabular}")
    tex.append(r"\end{table*}")
    OUT_TEX.write_text("\n".join(tex) + "\n", encoding="utf-8")

    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_TEX}")
    print(f"N_RUN_ROWS={len(per_run)}")
    print(f"N_DELTA_ROWS={len(delta)}")
    print(delta[["comparison", "direction", "delta_genuine_mean", "delta_impostor_q999", "delta_dprime", "delta_tar_far_1e_3_pp"]].to_string(index=False))


if __name__ == "__main__":
    main()
