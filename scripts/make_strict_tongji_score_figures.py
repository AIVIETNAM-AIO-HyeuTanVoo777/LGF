from __future__ import annotations

from pathlib import Path
from statistics import mean
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from scipy.stats import norm

RUNS_CSV = Path("docs/results/strict_tongji_ablation_runs.csv")

FIG_DIR = Path("paper/figures")
OUT_MD = Path("docs/results/strict_tongji_roc_det_score_figures.md")
OUT_CSV = Path("docs/results/strict_tongji_roc_det_score_figures.csv")
OUT_TEX = Path("paper/sections/strict_tongji_score_figures.tex")

METHODS = ["B1", "B5", "B6"]
METHOD_LABELS = {
    "B1": "B1 CE+SupCon",
    "B5": "B5 BNNeck+CE",
    "B6": "B6 BNNeck+ArcFace",
}
DIRECTIONS = ["S1->S2", "S2->S1"]
DIRECTION_SLUG = {
    "S1->S2": "s1_to_s2",
    "S2->S1": "s2_to_s1",
}

# Common grid for seed-averaged ROC/DET curves.
FPR_GRID = np.concatenate([
    np.array([0.0]),
    np.logspace(-6, 0, 600),
])
FPR_GRID = np.unique(np.clip(FPR_GRID, 0.0, 1.0))


def load_runs() -> pd.DataFrame:
    if not RUNS_CSV.exists():
        raise FileNotFoundError(RUNS_CSV)
    df = pd.read_csv(RUNS_CSV)
    df = df[df["method"].isin(METHODS)].copy()
    if len(df) != 18:
        raise RuntimeError(f"Expected 18 B1/B5/B6 runs, found {len(df)}")

    for col in ["method", "direction", "seed", "metrics_path", "status"]:
        if col not in df.columns:
            raise RuntimeError(f"Missing column: {col}")

    bad = df[df["status"].astype(str).str.upper() != "OK"]
    if not bad.empty:
        raise RuntimeError(f"Non-OK rows:\n{bad}")

    return df


def read_roc(metrics_path: str) -> pd.DataFrame:
    p = Path(metrics_path).with_name("roc.csv")
    if not p.exists():
        raise FileNotFoundError(p)
    df = pd.read_csv(p)
    required = {"fpr", "tpr"}
    missing = required - set(df.columns)
    if missing:
        raise RuntimeError(f"{p} missing columns {missing}")
    df = df[["fpr", "tpr"]].dropna().sort_values("fpr")
    df["fpr"] = df["fpr"].clip(0.0, 1.0)
    df["tpr"] = df["tpr"].clip(0.0, 1.0)
    return df


def interp_tpr_at_grid(roc: pd.DataFrame) -> np.ndarray:
    fpr = roc["fpr"].to_numpy(dtype=float)
    tpr = roc["tpr"].to_numpy(dtype=float)

    # Merge duplicate FPR points by taking max TPR.
    tmp = pd.DataFrame({"fpr": fpr, "tpr": tpr}).groupby("fpr", as_index=False)["tpr"].max()
    fpr = tmp["fpr"].to_numpy(dtype=float)
    tpr = tmp["tpr"].to_numpy(dtype=float)

    if fpr[0] > 0.0:
        fpr = np.insert(fpr, 0, 0.0)
        tpr = np.insert(tpr, 0, 0.0)
    if fpr[-1] < 1.0:
        fpr = np.append(fpr, 1.0)
        tpr = np.append(tpr, 1.0)

    return np.interp(FPR_GRID, fpr, tpr)


def read_scores(metrics_path: str) -> pd.DataFrame:
    p = Path(metrics_path).with_name("scores.csv")
    if not p.exists():
        raise FileNotFoundError(p)
    df = pd.read_csv(p)
    required = {"score", "label"}
    missing = required - set(df.columns)
    if missing:
        raise RuntimeError(f"{p} missing columns {missing}")
    df = df[["score", "label"]].dropna()
    return df


def aggregate_rocs(df: pd.DataFrame, direction: str, method: str) -> Tuple[np.ndarray, np.ndarray]:
    sub = df[(df["direction"] == direction) & (df["method"] == method)].copy()
    if len(sub) != 3:
        raise RuntimeError(f"Expected 3 runs for {method} {direction}, found {len(sub)}")

    tprs = []
    for r in sub.itertuples(index=False):
        roc = read_roc(r.metrics_path)
        tprs.append(interp_tpr_at_grid(roc))

    arr = np.vstack(tprs)
    return arr.mean(axis=0), arr.std(axis=0, ddof=1)


def plot_roc(df: pd.DataFrame, direction: str) -> Path:
    slug = DIRECTION_SLUG[direction]
    out = FIG_DIR / f"roc_tongji_b1_b5_b6_{slug}.pdf"

    plt.figure(figsize=(5.2, 3.8))
    for method in METHODS:
        mean_tpr, _ = aggregate_rocs(df, direction, method)
        plt.plot(FPR_GRID, mean_tpr, label=METHOD_LABELS[method])

    plt.xscale("log")
    plt.xlim(1e-6, 1.0)
    plt.ylim(0.0, 1.01)
    plt.xlabel("False accept rate / FPR")
    plt.ylabel("True accept rate / TPR")
    plt.title(f"Tongji strict ROC ({direction})")
    plt.grid(True, which="both", linewidth=0.4)
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(out)
    plt.close()
    return out


def plot_det(df: pd.DataFrame, direction: str) -> Path:
    slug = DIRECTION_SLUG[direction]
    out = FIG_DIR / f"det_tongji_b1_b5_b6_{slug}.pdf"

    plt.figure(figsize=(5.2, 3.8))
    eps = 1e-6

    for method in METHODS:
        mean_tpr, _ = aggregate_rocs(df, direction, method)
        fpr = np.clip(FPR_GRID, eps, 1.0 - eps)
        fnr = np.clip(1.0 - mean_tpr, eps, 1.0 - eps)
        x = norm.ppf(fpr)
        y = norm.ppf(fnr)
        plt.plot(x, y, label=METHOD_LABELS[method])

    tick_probs = np.array([1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 0.5])
    tick_pos = norm.ppf(tick_probs)
    tick_lab = ["1e-5", "1e-4", "1e-3", "1e-2", "1e-1", "0.5"]

    plt.xticks(tick_pos, tick_lab)
    plt.yticks(tick_pos, tick_lab)
    plt.xlabel("FAR / FPR")
    plt.ylabel("FRR / FNR")
    plt.title(f"Tongji strict DET ({direction})")
    plt.grid(True, linewidth=0.4)
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(out)
    plt.close()
    return out


def sample_scores_for_hist(df: pd.DataFrame, direction: str, method: str, max_impostor_per_seed: int = 50000) -> Tuple[np.ndarray, np.ndarray]:
    sub = df[(df["direction"] == direction) & (df["method"] == method)].copy()
    if len(sub) != 3:
        raise RuntimeError(f"Expected 3 runs for {method} {direction}, found {len(sub)}")

    genuine_parts = []
    impostor_parts = []

    for r in sub.itertuples(index=False):
        scores = read_scores(r.metrics_path)
        genuine = scores.loc[scores["label"] == 1, "score"].to_numpy(dtype=float)
        impostor = scores.loc[scores["label"] == 0, "score"].to_numpy(dtype=float)

        rng = np.random.default_rng(int(r.seed) + 20260624)
        if len(impostor) > max_impostor_per_seed:
            idx = rng.choice(len(impostor), size=max_impostor_per_seed, replace=False)
            impostor = impostor[idx]

        genuine_parts.append(genuine)
        impostor_parts.append(impostor)

    return np.concatenate(genuine_parts), np.concatenate(impostor_parts)


def plot_hist(df: pd.DataFrame, direction: str) -> Path:
    slug = DIRECTION_SLUG[direction]
    out = FIG_DIR / f"score_hist_tongji_b1_b5_b6_{slug}.pdf"

    # Three separate density outlines in one figure per direction.
    plt.figure(figsize=(5.8, 3.8))
    bins = np.linspace(-1.0, 1.0, 120)

    for method in METHODS:
        genuine, impostor = sample_scores_for_hist(df, direction, method)
        plt.hist(impostor, bins=bins, density=True, histtype="step", linewidth=1.0, label=f"{METHOD_LABELS[method]} impostor")
        plt.hist(genuine, bins=bins, density=True, histtype="step", linewidth=1.0, linestyle="--", label=f"{METHOD_LABELS[method]} genuine")

    plt.xlabel("Cosine similarity score")
    plt.ylabel("Density")
    plt.title(f"Tongji strict score distributions ({direction})")
    plt.grid(True, linewidth=0.4)
    plt.legend(fontsize=6, ncol=2)
    plt.tight_layout()
    plt.savefig(out)
    plt.close()
    return out


def nearest_tpr_at_fpr(mean_tpr: np.ndarray, target: float) -> float:
    idx = int(np.argmin(np.abs(FPR_GRID - target)))
    return float(mean_tpr[idx])


def write_summary(df: pd.DataFrame, figure_paths: List[Path]) -> None:
    rows = []

    for direction in DIRECTIONS:
        for method in METHODS:
            mean_tpr, std_tpr = aggregate_rocs(df, direction, method)
            rows.append({
                "method": method,
                "method_label": METHOD_LABELS[method],
                "direction": direction,
                "mean_tpr_at_fpr_1e-2": nearest_tpr_at_fpr(mean_tpr, 1e-2),
                "mean_tpr_at_fpr_1e-3": nearest_tpr_at_fpr(mean_tpr, 1e-3),
                "mean_tpr_at_fpr_1e-4": nearest_tpr_at_fpr(mean_tpr, 1e-4),
            })

    out = pd.DataFrame(rows)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT_CSV, index=False)

    md = []
    md.append("# Strict Tongji ROC/DET/Score Figure Summary")
    md.append("")
    md.append("This file records reviewer-facing ROC, DET, and score-distribution figures for B1, B5, and B6 under the strict Tongji palm-class-disjoint protocol.")
    md.append("")
    md.append("- Source run table: `docs/results/strict_tongji_ablation_runs.csv`.")
    md.append("- Source curves: per-run `roc.csv` files from the corresponding experiment directories.")
    md.append("- Source scores: per-run `scores.csv` files; each run has 12,000 genuine and 1,428,000 impostor pairs.")
    md.append("- Curves are seed-averaged by interpolating TPR onto a common log-spaced FPR grid.")
    md.append("- Histograms use all genuine scores and a deterministic impostor subsample of up to 50,000 impostor scores per seed to keep the plot readable.")
    md.append("")
    md.append("## Generated figures")
    md.append("")
    for p in figure_paths:
        md.append(f"- `{p.as_posix()}`")
    md.append("")
    md.append("## Mean TPR on common grid")
    md.append("")
    md.append("| Method | Direction | TPR@FPR=1e-2 | TPR@FPR=1e-3 | TPR@FPR=1e-4 |")
    md.append("|---|---|---:|---:|---:|")
    for r in rows:
        md.append(
            f"| {r['method_label']} | {r['direction']} | "
            f"{100*r['mean_tpr_at_fpr_1e-2']:.2f} | "
            f"{100*r['mean_tpr_at_fpr_1e-3']:.2f} | "
            f"{100*r['mean_tpr_at_fpr_1e-4']:.2f} |"
        )
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")


def write_tex() -> None:
    tex = []
    tex.append(r"\begin{figure*}[t]")
    tex.append(r"\centering")
    tex.append(r"\includegraphics[width=0.48\textwidth]{figures/roc_tongji_b1_b5_b6_s1_to_s2.pdf}")
    tex.append(r"\includegraphics[width=0.48\textwidth]{figures/roc_tongji_b1_b5_b6_s2_to_s1.pdf}")
    tex.append(r"\caption{Strict Tongji ROC curves for B1, B5, and B6, averaged over three seeds within each session direction. The curves emphasize low-FAR verification behavior under the palm-class-disjoint cross-session protocol.}")
    tex.append(r"\label{fig:strict_tongji_roc_by_direction}")
    tex.append(r"\end{figure*}")
    tex.append("")
    tex.append(r"\begin{figure*}[t]")
    tex.append(r"\centering")
    tex.append(r"\includegraphics[width=0.48\textwidth]{figures/det_tongji_b1_b5_b6_s1_to_s2.pdf}")
    tex.append(r"\includegraphics[width=0.48\textwidth]{figures/det_tongji_b1_b5_b6_s2_to_s1.pdf}")
    tex.append(r"\caption{Strict Tongji DET curves for B1, B5, and B6. The DET view highlights that component behavior changes with session direction and that BNNeck+ArcFace does not provide a direction-invariant improvement.}")
    tex.append(r"\label{fig:strict_tongji_det_by_direction}")
    tex.append(r"\end{figure*}")
    tex.append("")
    tex.append(r"\begin{figure*}[t]")
    tex.append(r"\centering")
    tex.append(r"\includegraphics[width=0.48\textwidth]{figures/score_hist_tongji_b1_b5_b6_s1_to_s2.pdf}")
    tex.append(r"\includegraphics[width=0.48\textwidth]{figures/score_hist_tongji_b1_b5_b6_s2_to_s1.pdf}")
    tex.append(r"\caption{Strict Tongji genuine and impostor score distributions for B1, B5, and B6. Dashed curves denote genuine-pair scores and solid curves denote impostor-pair scores. The distributions provide a score-level view of the direction-sensitive verification behavior.}")
    tex.append(r"\label{fig:strict_tongji_score_hist_by_direction}")
    tex.append(r"\end{figure*}")
    OUT_TEX.write_text("\n".join(tex) + "\n", encoding="utf-8")


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    df = load_runs()
    figure_paths = []

    for direction in DIRECTIONS:
        figure_paths.append(plot_roc(df, direction))
        figure_paths.append(plot_det(df, direction))
        figure_paths.append(plot_hist(df, direction))

    write_summary(df, figure_paths)
    write_tex()

    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_TEX}")
    for p in figure_paths:
        print(f"Wrote {p}")
    print(f"N_FIGURES={len(figure_paths)}")


if __name__ == "__main__":
    main()