from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from scipy.optimize import brentq
from sklearn.metrics import f1_score, roc_curve


SPLIT_DIR = Path("data/splits")
RUNS_CSV = Path("docs/results/strict_tongji_ablation_runs.csv")

OUT_RUNS_CSV = Path("docs/results/gabor_strict_tongji_runs.csv")
OUT_SUMMARY_CSV = Path("docs/results/gabor_strict_tongji_summary.csv")
OUT_MD = Path("docs/results/gabor_strict_tongji_summary.md")
OUT_TEX = Path("paper/sections/palmprint_specific_baseline_table.tex")

SEEDS = [42, 2026, 2705]
DIRECTIONS = {
    "s1_to_s2": "S1->S2",
    "s2_to_s1": "S2->S1",
}

IMAGE_SIZE = (128, 128)
N_ORIENTATIONS = 8
POOL_SIZE = (8, 8)

COMPARE_METHODS = ["B1", "B5", "B6"]

METHOD_LABELS = {
    "Gabor": "Fixed Gabor texture",
    "B1": "B1 CE+SupCon",
    "B5": "B5 BNNeck+CE",
    "B6": "B6 BNNeck+ArcFace",
}

METHOD_ROLE = {
    "Gabor": "Palmprint-specific classical reference",
    "B1": "Learned baseline",
    "B5": "Highest observed strict variant",
    "B6": "Hypothesized BNNeck+ArcFace variant",
}


def as_percent(x: float) -> float:
    x = float(x)
    return x * 100.0 if abs(x) <= 1.5 else x


def fmt_mean_sd(mean: float, sd: float) -> str:
    return f"{mean:.2f} +/- {sd:.2f}"


def fmt_tex_mean_sd(mean: float, sd: float) -> str:
    return f"{mean:.2f} $\\pm$ {sd:.2f}"


def build_gabor_kernels() -> list[np.ndarray]:
    kernels = []
    for theta in np.linspace(0, np.pi, N_ORIENTATIONS, endpoint=False):
        kernel = cv2.getGaborKernel(
            ksize=(15, 15),
            sigma=4.0,
            theta=float(theta),
            lambd=10.0,
            gamma=0.5,
            psi=0.0,
            ktype=cv2.CV_32F,
        )
        kernel = kernel - kernel.mean()
        norm = np.sqrt(np.sum(kernel * kernel))
        if norm > 0:
            kernel = kernel / norm
        kernels.append(kernel.astype(np.float32))
    return kernels


KERNELS = build_gabor_kernels()


def split_path(direction_key: str, seed: int) -> Path:
    return SPLIT_DIR / f"tongji_subject_disjoint_{direction_key}_seed{seed}.json"


def load_split(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Missing split: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    for key in ["train", "val", "gallery", "probe"]:
        if key not in data or not isinstance(data[key], list):
            raise ValueError(f"{path} missing list partition: {key}")
    return data


def item_path(item) -> Path:
    if isinstance(item, str):
        return Path(item)
    if isinstance(item, dict):
        for key in ["path", "image_path", "filepath", "file"]:
            if key in item:
                return Path(str(item[key]))
    raise ValueError(f"Cannot infer path from split item: {item!r}")


def item_label(item) -> int:
    if isinstance(item, dict):
        for key in ["class_id", "palm_id", "label"]:
            if key in item:
                v = item[key]
                try:
                    return int(v)
                except Exception:
                    return abs(hash(str(v))) % (2**31)
    raise ValueError(f"Cannot infer class label from split item: {item!r}")


def extract_raw_gabor_feature(path: Path) -> np.ndarray:
    img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Cannot read image: {path}")

    img = cv2.resize(img, IMAGE_SIZE, interpolation=cv2.INTER_AREA)
    img = img.astype(np.float32) / 255.0
    img = (img - float(img.mean())) / (float(img.std()) + 1e-6)

    parts = []
    for kernel in KERNELS:
        response = cv2.filter2D(img, cv2.CV_32F, kernel)
        mag = np.abs(response)
        pooled = cv2.resize(mag, POOL_SIZE, interpolation=cv2.INTER_AREA)
        parts.append(pooled.reshape(-1))

    return np.concatenate(parts).astype(np.float32)


def features_for_items(items: list, cache: dict[str, np.ndarray]) -> tuple[np.ndarray, np.ndarray, list[str]]:
    feats = []
    labels = []
    paths = []
    for item in items:
        p = item_path(item)
        key = str(p)
        if key not in cache:
            cache[key] = extract_raw_gabor_feature(p)
        feats.append(cache[key])
        labels.append(item_label(item))
        paths.append(key)
    return np.vstack(feats).astype(np.float32), np.array(labels, dtype=np.int64), paths


def fit_standardizer(train_feats: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    mean = train_feats.mean(axis=0, keepdims=True)
    std = train_feats.std(axis=0, keepdims=True)
    std[std < 1e-6] = 1.0
    return mean.astype(np.float32), std.astype(np.float32)


def transform_features(feats: np.ndarray, mean: np.ndarray, std: np.ndarray) -> np.ndarray:
    out = (feats - mean) / std
    norms = np.linalg.norm(out, axis=1, keepdims=True)
    norms[norms < 1e-12] = 1.0
    return (out / norms).astype(np.float32)


def compute_eer_and_tar(scores: np.ndarray, labels: np.ndarray) -> tuple[float, float, float]:
    fpr, tpr, _ = roc_curve(labels, scores)
    fnr = 1.0 - tpr

    nearest_idx = int(np.nanargmin(np.abs(fpr - fnr)))
    eer = float((fpr[nearest_idx] + fnr[nearest_idx]) / 2.0)

    try:
        interp = interp1d(fpr, tpr, bounds_error=False, fill_value=(float(tpr[0]), float(tpr[-1])))
        eer = float(brentq(lambda x: 1.0 - x - float(interp(x)), 0.0, 1.0))
    except Exception:
        pass

    idx_1e2 = int(np.nanargmin(np.abs(fpr - 1e-2)))
    idx_1e3 = int(np.nanargmin(np.abs(fpr - 1e-3)))
    tar_1e2 = float(tpr[idx_1e2])
    tar_1e3 = float(tpr[idx_1e3])
    return eer, tar_1e2, tar_1e3


def evaluate_one(direction_key: str, seed: int, cache: dict[str, np.ndarray]) -> dict:
    sp = split_path(direction_key, seed)
    split = load_split(sp)

    print(f"Evaluating fixed Gabor baseline: {DIRECTIONS[direction_key]} seed {seed}")
    train_feats_raw, _, _ = features_for_items(split["train"], cache)
    gallery_feats_raw, gallery_labels, gallery_paths = features_for_items(split["gallery"], cache)
    probe_feats_raw, probe_labels, probe_paths = features_for_items(split["probe"], cache)

    mean, std = fit_standardizer(train_feats_raw)
    gallery_feats = transform_features(gallery_feats_raw, mean, std)
    probe_feats = transform_features(probe_feats_raw, mean, std)

    sim = probe_feats @ gallery_feats.T

    order = np.argsort(-sim, axis=1)
    sorted_labels = gallery_labels[order]

    rank1 = float(np.mean(sorted_labels[:, 0] == probe_labels))
    top5 = sorted_labels[:, : min(5, sorted_labels.shape[1])]
    rank5 = float(np.mean(np.any(top5 == probe_labels[:, None], axis=1)))

    pred = sorted_labels[:, 0]
    macro_f1 = float(f1_score(probe_labels, pred, average="macro"))

    pair_labels = (probe_labels[:, None] == gallery_labels[None, :]).astype(np.uint8).reshape(-1)
    pair_scores = sim.reshape(-1).astype(np.float32)

    n_genuine = int(pair_labels.sum())
    n_pairs = int(pair_labels.size)
    n_impostor = int(n_pairs - n_genuine)

    eer, tar_1e2, tar_1e3 = compute_eer_and_tar(pair_scores, pair_labels)

    return {
        "method": "Gabor",
        "method_label": METHOD_LABELS["Gabor"],
        "direction": DIRECTIONS[direction_key],
        "seed": seed,
        "status": "OK",
        "Rank-1": rank1,
        "Rank-5": rank5,
        "Macro-F1": macro_f1,
        "EER": eer,
        "TAR@FAR=1e-2": tar_1e2,
        "TAR@FAR=1e-3": tar_1e3,
        "gallery_size": len(gallery_labels),
        "probe_size": len(probe_labels),
        "genuine_pairs": n_genuine,
        "impostor_pairs": n_impostor,
        "split_path": str(sp),
        "feature_dim": int(gallery_feats.shape[1]),
        "normalizer_fit": "train partition only",
    }


def summarize_rows(rows: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    out = []
    for method, sub in df.groupby("method", sort=False):
        row = {
            "method": method,
            "method_label": METHOD_LABELS.get(method, method),
            "role": METHOD_ROLE.get(method, ""),
            "n_runs": int(len(sub)),
        }
        for metric in ["Rank-1", "Rank-5", "Macro-F1", "EER", "TAR@FAR=1e-2", "TAR@FAR=1e-3"]:
            vals = np.array([as_percent(x) for x in sub[metric].to_numpy(dtype=float)], dtype=float)
            row[f"{metric}_mean_pp"] = float(vals.mean())
            row[f"{metric}_sd_pp"] = float(vals.std(ddof=1)) if len(vals) > 1 else 0.0
        out.append(row)
    return pd.DataFrame(out)


def load_learned_comparison_rows() -> list[dict]:
    if not RUNS_CSV.exists():
        raise FileNotFoundError(f"Missing learned run table: {RUNS_CSV}")

    runs = pd.read_csv(RUNS_CSV)
    rows = []
    for _, r in runs[runs["method"].isin(COMPARE_METHODS)].iterrows():
        rows.append({
            "method": str(r["method"]),
            "method_label": METHOD_LABELS.get(str(r["method"]), str(r.get("method_label", r["method"]))),
            "direction": str(r["direction"]),
            "seed": int(r["seed"]),
            "status": str(r.get("status", "OK")),
            "Rank-1": float(r["Rank-1"]),
            "Rank-5": float(r["Rank-5"]),
            "Macro-F1": float(r["Macro-F1"]),
            "EER": float(r["EER"]),
            "TAR@FAR=1e-2": float(r["TAR@FAR=1e-2"]),
            "TAR@FAR=1e-3": float(r["TAR@FAR=1e-3"]),
        })
    return rows


def write_outputs(gabor_rows: list[dict]) -> None:
    learned_rows = load_learned_comparison_rows()
    all_rows = gabor_rows + learned_rows

    OUT_RUNS_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_SUMMARY_CSV.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_TEX.parent.mkdir(parents=True, exist_ok=True)

    pd.DataFrame(gabor_rows).to_csv(OUT_RUNS_CSV, index=False)

    summary = summarize_rows(all_rows)
    method_order = ["Gabor", "B1", "B5", "B6"]
    summary["order"] = summary["method"].map({m: i for i, m in enumerate(method_order)})
    summary = summary.sort_values("order").drop(columns=["order"])
    summary.to_csv(OUT_SUMMARY_CSV, index=False)

    md = []
    md.append("# Fixed Gabor Strict Tongji Baseline")
    md.append("")
    md.append("This report adds a palmprint-specific fixed Gabor texture reference baseline under the same audited strict Tongji gallery/probe splits.")
    md.append("")
    md.append("- The baseline uses deterministic Gabor magnitude features over segmented 128x128 images.")
    md.append("- The feature standardizer is fit on the training partition only for each seed-direction split.")
    md.append("- No learned checkpoint, experiment tensor, or score file is written.")
    md.append("- This is not a reimplementation of PalmNet, CompNet, or Competitive Code; it is a protocol-normalized classical texture reference point.")
    md.append("")
    md.append("| Method | Role | n | Rank-1 | EER | TAR@FAR=1e-3 |")
    md.append("|---|---|---:|---:|---:|---:|")
    for _, r in summary.iterrows():
        md.append(
            f"| {r['method_label']} | {r['role']} | {int(r['n_runs'])} | "
            f"{fmt_mean_sd(r['Rank-1_mean_pp'], r['Rank-1_sd_pp'])} | "
            f"{fmt_mean_sd(r['EER_mean_pp'], r['EER_sd_pp'])} | "
            f"{fmt_mean_sd(r['TAR@FAR=1e-3_mean_pp'], r['TAR@FAR=1e-3_sd_pp'])} |"
        )
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    tex = []
    tex.append(r"\begin{table*}[t]")
    tex.append(r"\centering")
    tex.append(r"\caption{Palmprint-specific fixed Gabor texture reference under the same strict Tongji palm-class-disjoint protocol. The Gabor row is a deterministic classical texture baseline, not a reimplementation of PalmNet, CompNet, or Competitive Code. Values are mean $\pm$ standard deviation over two session directions and three seeds. Lower EER is better; higher Rank-1 and TAR are better.}")
    tex.append(r"\label{tab:palmprint_specific_gabor_baseline}")
    tex.append(r"\small")
    tex.append(r"\setlength{\tabcolsep}{4pt}")
    tex.append(r"\begin{tabular}{llrrr}")
    tex.append(r"\toprule")
    tex.append(r"Method & Role & Rank-1 & EER & TAR@FAR=$10^{-3}$ \\")
    tex.append(r"\midrule")
    for _, r in summary.iterrows():
        tex.append(
            f"{r['method_label']} & {r['role']} & "
            f"{fmt_tex_mean_sd(r['Rank-1_mean_pp'], r['Rank-1_sd_pp'])} & "
            f"{fmt_tex_mean_sd(r['EER_mean_pp'], r['EER_sd_pp'])} & "
            f"{fmt_tex_mean_sd(r['TAR@FAR=1e-3_mean_pp'], r['TAR@FAR=1e-3_sd_pp'])} \\\\"
        )
    tex.append(r"\bottomrule")
    tex.append(r"\end{tabular}")
    tex.append(r"\end{table*}")
    OUT_TEX.write_text("\n".join(tex) + "\n", encoding="utf-8")

    print(f"Wrote {OUT_RUNS_CSV}")
    print(f"Wrote {OUT_SUMMARY_CSV}")
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_TEX}")
    print(summary[["method", "method_label", "n_runs", "Rank-1_mean_pp", "EER_mean_pp", "TAR@FAR=1e-3_mean_pp"]].to_string(index=False))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", nargs="*", type=int, default=SEEDS)
    ap.add_argument("--directions", nargs="*", default=list(DIRECTIONS.keys()))
    args = ap.parse_args()

    bad_directions = [d for d in args.directions if d not in DIRECTIONS]
    if bad_directions:
        raise ValueError(f"Unsupported directions: {bad_directions}. Valid: {list(DIRECTIONS)}")

    cache: dict[str, np.ndarray] = {}
    gabor_rows = []
    for direction_key in args.directions:
        for seed in args.seeds:
            gabor_rows.append(evaluate_one(direction_key, seed, cache))

    write_outputs(gabor_rows)
    print(f"RAW_FEATURE_CACHE_SIZE={len(cache)}")


if __name__ == "__main__":
    main()
