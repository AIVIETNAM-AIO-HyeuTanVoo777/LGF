from __future__ import annotations

from pathlib import Path
import csv
import json
import math
from typing import Dict, List

import numpy as np
import pandas as pd
from sklearn.metrics import roc_curve
from scipy.optimize import brentq
from scipy.interpolate import interp1d

ROOT = Path(".").resolve()
RUNS_CSV = ROOT / "docs/results/strict_tongji_ablation_runs.csv"
OUT_CSV = ROOT / "docs/audits/metric_threshold_audit.csv"
OUT_MD = ROOT / "docs/audits/metric_threshold_audit.md"

TARGET_FARS = [1e-2, 1e-3]

def load_metrics(path: Path) -> Dict[str, float]:
    return json.loads(path.read_text(encoding="utf-8"))

def count_score_labels(scores_path: Path) -> tuple[int, int, int]:
    genuine = 0
    impostor = 0
    total = 0
    for chunk in pd.read_csv(scores_path, usecols=["label"], chunksize=500_000):
        labels = chunk["label"].astype(int).to_numpy()
        total += int(labels.size)
        genuine += int((labels == 1).sum())
        impostor += int((labels == 0).sum())
    return total, genuine, impostor

def read_scores(scores_path: Path) -> tuple[np.ndarray, np.ndarray]:
    df = pd.read_csv(scores_path, usecols=["score", "label"])
    y_scores = df["score"].astype(float).to_numpy()
    y_true = df["label"].astype(int).to_numpy()
    return y_true, y_scores

def compute_thresholds(y_true: np.ndarray, y_scores: np.ndarray) -> Dict[str, float]:
    fpr, tpr, thresholds = roc_curve(y_true, y_scores)
    fnr = 1.0 - tpr

    nearest_eer_idx = int(np.nanargmin(np.absolute(fpr - fnr)))
    nearest_eer = float(fpr[nearest_eer_idx])
    nearest_eer_threshold = float(thresholds[nearest_eer_idx])

    interpolated_eer = nearest_eer
    interpolation_status = "fallback_nearest"
    try:
        interpolated_eer = float(brentq(lambda x: 1.0 - x - interp1d(fpr, tpr)(x), 0.0, 1.0))
        interpolation_status = "brentq_interp1d"
    except Exception as exc:
        interpolation_status = f"fallback_nearest:{type(exc).__name__}"

    out = {
        "roc_points": int(len(fpr)),
        "nearest_eer": nearest_eer,
        "nearest_eer_threshold": nearest_eer_threshold,
        "interpolated_eer": interpolated_eer,
        "eer_interpolation_status": interpolation_status,
    }

    for target in TARGET_FARS:
        idx = int(np.argmin(np.abs(fpr - target)))
        out[f"target_far_{target:g}"] = float(target)
        out[f"nearest_far_{target:g}"] = float(fpr[idx])
        out[f"nearest_far_abs_error_{target:g}"] = float(abs(fpr[idx] - target))
        out[f"tar_at_nearest_far_{target:g}"] = float(tpr[idx])
        out[f"threshold_at_nearest_far_{target:g}"] = float(thresholds[idx])

        le_idxs = np.where(fpr <= target)[0]
        if len(le_idxs) > 0:
            le_idx = int(le_idxs[-1])
            out[f"tar_at_max_far_le_{target:g}"] = float(tpr[le_idx])
            out[f"threshold_at_max_far_le_{target:g}"] = float(thresholds[le_idx])
            out[f"max_far_le_{target:g}"] = float(fpr[le_idx])
        else:
            out[f"tar_at_max_far_le_{target:g}"] = float("nan")
            out[f"threshold_at_max_far_le_{target:g}"] = float("nan")
            out[f"max_far_le_{target:g}"] = float("nan")

    return out

def fmt_float(x: float, digits: int = 10) -> str:
    if isinstance(x, float) and math.isnan(x):
        return "nan"
    return f"{x:.{digits}g}"

def main() -> None:
    if not RUNS_CSV.exists():
        raise FileNotFoundError(RUNS_CSV)

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    with RUNS_CSV.open("r", encoding="utf-8", newline="") as f:
        runs = list(csv.DictReader(f))

    rows: List[Dict[str, object]] = []
    for i, r in enumerate(runs, start=1):
        method = r["method"]
        direction = r["direction"]
        seed = r["seed"]
        metrics_path = ROOT / r["metrics_path"]
        run_dir = metrics_path.parent
        scores_path = run_dir / "scores.csv"

        print(f"[{i:02d}/{len(runs)}] auditing {method} {direction} seed {seed}")

        if not metrics_path.exists():
            raise FileNotFoundError(metrics_path)
        if not scores_path.exists():
            raise FileNotFoundError(scores_path)

        total_pairs, genuine_pairs, impostor_pairs = count_score_labels(scores_path)
        y_true, y_scores = read_scores(scores_path)
        threshold_info = compute_thresholds(y_true, y_scores)
        metrics = load_metrics(metrics_path)

        min_far_step = 1.0 / impostor_pairs if impostor_pairs else float("nan")

        row: Dict[str, object] = {
            "method": method,
            "method_label": r.get("method_label", ""),
            "direction": direction,
            "seed": seed,
            "metrics_path": r["metrics_path"],
            "scores_path": str(scores_path.relative_to(ROOT)).replace("\\", "/"),
            "total_pairs": total_pairs,
            "genuine_pairs": genuine_pairs,
            "impostor_pairs": impostor_pairs,
            "min_empirical_far_step": min_far_step,
            "reported_eer": float(metrics["EER"]),
            "reported_tar_far_1e_2": float(metrics["TAR@FAR=1e-2"]),
            "reported_tar_far_1e_3": float(metrics["TAR@FAR=1e-3"]),
            "verdict": "PASS",
            "notes": "scores.csv counts verified; metrics use sklearn roc_curve, brentq EER if available, and nearest empirical FPR for TAR@FAR.",
        }
        row.update(threshold_info)

        # Consistency checks against metrics.json.
        if abs(row["reported_eer"] - row["interpolated_eer"]) > 1e-8:
            row["verdict"] = "WARN"
            row["notes"] += " reported EER differs from recomputed interpolated EER."
        if abs(row["reported_tar_far_1e_2"] - row["tar_at_nearest_far_0.01"]) > 1e-8:
            row["verdict"] = "WARN"
            row["notes"] += " reported TAR@FAR=1e-2 differs from recomputed nearest-FPR TAR."
        if abs(row["reported_tar_far_1e_3"] - row["tar_at_nearest_far_0.001"]) > 1e-8:
            row["verdict"] = "WARN"
            row["notes"] += " reported TAR@FAR=1e-3 differs from recomputed nearest-FPR TAR."

        rows.append(row)

    fieldnames = [
        "method", "method_label", "direction", "seed",
        "total_pairs", "genuine_pairs", "impostor_pairs", "min_empirical_far_step",
        "roc_points",
        "reported_eer", "nearest_eer", "nearest_eer_threshold", "interpolated_eer", "eer_interpolation_status",
        "reported_tar_far_1e_2", "nearest_far_0.01", "nearest_far_abs_error_0.01",
        "tar_at_nearest_far_0.01", "threshold_at_nearest_far_0.01",
        "max_far_le_0.01", "tar_at_max_far_le_0.01", "threshold_at_max_far_le_0.01",
        "reported_tar_far_1e_3", "nearest_far_0.001", "nearest_far_abs_error_0.001",
        "tar_at_nearest_far_0.001", "threshold_at_nearest_far_0.001",
        "max_far_le_0.001", "tar_at_max_far_le_0.001", "threshold_at_max_far_le_0.001",
        "verdict", "notes", "metrics_path", "scores_path",
    ]

    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow(row)

    pass_count = sum(1 for r in rows if r["verdict"] == "PASS")
    warn_count = sum(1 for r in rows if r["verdict"] == "WARN")
    fail_count = len(rows) - pass_count - warn_count

    pair_shapes = sorted({(r["genuine_pairs"], r["impostor_pairs"], r["total_pairs"]) for r in rows})
    min_far_steps = sorted({r["min_empirical_far_step"] for r in rows})
    interp_statuses = sorted({str(r["eer_interpolation_status"]) for r in rows})

    md: List[str] = []
    md.append("# Metric Threshold Audit")
    md.append("")
    md.append("This audit verifies verification pair counts and threshold conventions for the strict Tongji ablation runs.")
    md.append("")
    md.append("## Summary")
    md.append("")
    md.append(f"- Audited runs: {len(rows)}")
    md.append(f"- Verdicts: PASS={pass_count}, WARN={warn_count}, FAIL={fail_count}")
    md.append(f"- Pair count shapes `(genuine, impostor, total)`: {pair_shapes}")
    md.append(f"- Minimum empirical FAR step values: {[fmt_float(x, 12) for x in min_far_steps]}")
    md.append(f"- EER convention: sklearn ROC with brentq/interp1d interpolation when possible; fallback is nearest |FPR-FNR|.")
    md.append(f"- EER interpolation statuses: {interp_statuses}")
    md.append(f"- TAR@FAR convention in `scripts/eval_embedding.py`: choose the ROC point with nearest empirical FPR to the target FAR, not necessarily the largest FPR less than or equal to the target.")
    md.append("")
    md.append("## Protocol note for paper")
    md.append("")
    md.append("Verification thresholds are swept over observed cosine scores using `sklearn.metrics.roc_curve`. A pair is accepted when its cosine score is greater than or equal to the threshold. EER is computed by interpolating the ROC curve with `brentq`/`interp1d` when possible, with a nearest `|FPR-FNR|` fallback. TAR@FAR is reported at the ROC point whose empirical FPR is nearest to the target FAR (`10^{-2}` or `10^{-3}`). The audit reports genuine/impostor comparison counts, minimum empirical FAR step, and the threshold selected for each seed-direction-method run.")
    md.append("")
    md.append("## Per-run threshold audit")
    md.append("")
    md.append("| Method | Direction | Seed | Genuine | Impostor | min FAR step | EER | TAR@1e-2 nearest FPR | TAR@1e-3 nearest FPR | Verdict |")
    md.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---|")
    for r in rows:
        md.append(
            f"| {r['method']} | {r['direction']} | {r['seed']} | "
            f"{r['genuine_pairs']} | {r['impostor_pairs']} | {fmt_float(float(r['min_empirical_far_step']), 6)} | "
            f"{fmt_float(float(r['reported_eer']), 6)} | "
            f"{fmt_float(float(r['nearest_far_0.01']), 6)} | "
            f"{fmt_float(float(r['nearest_far_0.001']), 6)} | {r['verdict']} |"
        )

    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    print(f"Verdicts: PASS={pass_count}, WARN={warn_count}, FAIL={fail_count}")

if __name__ == "__main__":
    main()