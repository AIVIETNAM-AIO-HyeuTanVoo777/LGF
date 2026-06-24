from __future__ import annotations

import csv
import itertools
import random
from pathlib import Path
from statistics import mean, stdev


IN_CSV = Path("docs/results/paired_delta_b6_vs_b1.csv")
OUT_CSV = Path("docs/results/paired_statistics_b6_vs_b1.csv")
OUT_MD = Path("docs/results/paired_statistics_b6_vs_b1.md")
OUT_TEX = Path("paper/sections/paired_statistics_b6_vs_b1_table.tex")

BOOTSTRAP_SAMPLES = 50000
BOOTSTRAP_SEED = 20260624

METRICS = [
    ("Rank-1", "delta_rank1_b6_minus_b1", "higher_is_better"),
    ("Rank-5", "delta_rank5_b6_minus_b1", "higher_is_better"),
    ("Macro-F1", "delta_macro_f1_b6_minus_b1", "higher_is_better"),
    ("EER", "delta_eer_b6_minus_b1", "lower_is_better"),
    ("TAR@FAR=1e-2", "delta_tar_far_1e_2_b6_minus_b1", "higher_is_better"),
    ("TAR@FAR=1e-3", "delta_tar_far_1e_3_b6_minus_b1", "higher_is_better"),
]


def percentile(xs: list[float], q: float) -> float:
    if not xs:
        raise ValueError("Empty list")
    ys = sorted(xs)
    pos = (len(ys) - 1) * q
    lo = int(pos)
    hi = min(lo + 1, len(ys) - 1)
    frac = pos - lo
    return ys[lo] * (1.0 - frac) + ys[hi] * frac


def bootstrap_ci(values: list[float], rng: random.Random) -> tuple[float, float]:
    n = len(values)
    boots = []
    for _ in range(BOOTSTRAP_SAMPLES):
        sample = [values[rng.randrange(n)] for _ in range(n)]
        boots.append(mean(sample))
    return percentile(boots, 0.025), percentile(boots, 0.975)


def exact_sign_flip_p(values: list[float]) -> float:
    """Two-sided exact paired sign-flip p-value for mean delta under symmetric null."""
    observed = abs(mean(values))
    n = len(values)
    count = 0
    total = 0
    for signs in itertools.product([-1.0, 1.0], repeat=n):
        flipped_mean = mean([s * v for s, v in zip(signs, values)])
        if abs(flipped_mean) >= observed - 1e-15:
            count += 1
        total += 1
    return count / total


def pp(x: float) -> float:
    return 100.0 * x


def pp_str(x: float) -> str:
    return f"{pp(x):+.2f}"


def ci_str(lo: float, hi: float) -> str:
    return f"[{pp(lo):+.2f}, {pp(hi):+.2f}]"


def main() -> None:
    if not IN_CSV.exists():
        raise FileNotFoundError(IN_CSV)

    with IN_CSV.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    if len(rows) != 6:
        raise RuntimeError(f"Expected 6 paired units, found {len(rows)}")

    expected_units = {
        ("s1_to_s2", "42"),
        ("s1_to_s2", "2026"),
        ("s1_to_s2", "2705"),
        ("s2_to_s1", "42"),
        ("s2_to_s1", "2026"),
        ("s2_to_s1", "2705"),
    }
    observed_units = {(r["direction"], r["seed"]) for r in rows}
    if observed_units != expected_units:
        raise RuntimeError(f"Unexpected paired units: {observed_units}")

    rng = random.Random(BOOTSTRAP_SEED)
    out_rows = []

    for metric_name, col, directionality in METRICS:
        values = [float(r[col]) for r in rows]
        mu = mean(values)
        sd = stdev(values)
        ci_lo, ci_hi = bootstrap_ci(values, rng)
        p_sign = exact_sign_flip_p(values)

        if directionality == "higher_is_better":
            interpretation = "B6 better" if mu > 0 else "B6 worse"
        else:
            interpretation = "B6 worse" if mu > 0 else "B6 better"

        out_rows.append({
            "metric": metric_name,
            "n": len(values),
            "mean_delta_pp": pp(mu),
            "sd_delta_pp": pp(sd),
            "bootstrap_ci95_low_pp": pp(ci_lo),
            "bootstrap_ci95_high_pp": pp(ci_hi),
            "exact_sign_flip_p_two_sided": p_sign,
            "directionality": directionality,
            "mean_interpretation": interpretation,
        })

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "metric",
            "n",
            "mean_delta_pp",
            "sd_delta_pp",
            "bootstrap_ci95_low_pp",
            "bootstrap_ci95_high_pp",
            "exact_sign_flip_p_two_sided",
            "directionality",
            "mean_interpretation",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(out_rows)

    md = []
    md.append("# Paired Statistical Evidence: B6 vs B1")
    md.append("")
    md.append("## Scope")
    md.append("- Dataset: Tongji.")
    md.append("- Protocol: palm-class-disjoint cross-session evaluation.")
    md.append("- Paired units: six seed-direction units: S1->S2 and S2->S1 for seeds 42, 2026, and 2705.")
    md.append("- Delta definition: B6 minus B1.")
    md.append("- Positive Rank/TAR/Macro-F1 deltas favor B6.")
    md.append("- Positive EER deltas indicate worse performance for B6.")
    md.append(f"- Bootstrap CI: percentile bootstrap over paired units, {BOOTSTRAP_SAMPLES} resamples, seed {BOOTSTRAP_SEED}.")
    md.append("- Permutation test: exact two-sided sign-flip test over the six paired deltas.")
    md.append("- Because n=6, p-values are coarse and should be treated as uncertainty diagnostics, not definitive significance claims.")
    md.append("")
    md.append("## Summary")
    md.append("")
    md.append("| Metric | Mean delta (pp) | SD (pp) | Bootstrap 95% CI (pp) | Exact sign-flip p | Mean interpretation |")
    md.append("|---|---:|---:|---:|---:|---|")
    for r in out_rows:
        md.append(
            f"| {r['metric']} | "
            f"{float(r['mean_delta_pp']):+.2f} | "
            f"{float(r['sd_delta_pp']):.2f} | "
            f"[{float(r['bootstrap_ci95_low_pp']):+.2f}, {float(r['bootstrap_ci95_high_pp']):+.2f}] | "
            f"{float(r['exact_sign_flip_p_two_sided']):.4f} | "
            f"{r['mean_interpretation']} |"
        )
    md.append("")
    md.append("## Interpretation")
    md.append("- The mean paired deltas are negative for Rank-1, Rank-5, Macro-F1, TAR@FAR=1e-2, and TAR@FAR=1e-3, and positive for EER.")
    md.append("- This direction of change is consistently unfavorable to B6 on the bidirectional average.")
    md.append("- However, the bootstrap intervals are wide because there are only six paired units.")
    md.append("- Therefore the paper should report these results as paired uncertainty evidence, not as a strong formal significance claim.")
    md.append("")
    OUT_MD.write_text("\n".join(md), encoding="utf-8")

    tex = []
    tex.append(r"\begin{table}[t]")
    tex.append(r"\centering")
    tex.append(r"\scriptsize")
    tex.append(r"\setlength{\tabcolsep}{3pt}")
    tex.append(r"\caption{Paired statistical evidence for B6 minus B1 on Tongji palm-class-disjoint cross-session evaluation. Deltas are in percentage points over six paired seed-direction units. Positive EER is worse for B6; positive values are better for all other metrics.}")
    tex.append(r"\label{tab:paired_statistics_b6_vs_b1}")
    tex.append(r"\resizebox{\columnwidth}{!}{")
    tex.append(r"\begin{tabular}{lccc}")
    tex.append(r"\toprule")
    tex.append(r"Metric & Mean $\Delta$ & 95\% bootstrap CI & Sign-flip $p$ \\")
    tex.append(r"\midrule")
    for r in out_rows:
        tex.append(
            f"{r['metric']} & "
            f"{float(r['mean_delta_pp']):+.2f} & "
            f"[{float(r['bootstrap_ci95_low_pp']):+.2f}, {float(r['bootstrap_ci95_high_pp']):+.2f}] & "
            f"{float(r['exact_sign_flip_p_two_sided']):.4f} \\\\"
        )
    tex.append(r"\bottomrule")
    tex.append(r"\end{tabular}%")
    tex.append(r"}")
    tex.append(r"\end{table}")
    tex.append("")
    OUT_TEX.write_text("\n".join(tex), encoding="utf-8")

    print(f"PAIRED_UNITS={len(rows)}")
    print(f"METRICS={len(out_rows)}")
    print(f"WROTE={OUT_CSV}")
    print(f"WROTE={OUT_MD}")
    print(f"WROTE={OUT_TEX}")


if __name__ == "__main__":
    main()