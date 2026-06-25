from __future__ import annotations

from pathlib import Path
import csv
import math
import sys
from typing import Dict, Iterable, List

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from scipy.optimize import brentq
from sklearn.metrics import roc_curve

ROOT = Path(".").resolve()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from palmrec.evaluation.metrics import tar_at_far_conservative

STRICT_TONGJI_RUNS_CSV = ROOT / "docs/results/strict_tongji_ablation_runs.csv"
IITD_RUNS_CSV = ROOT / "docs/results/iitd_subject_disjoint_rerun_runs.csv"

STRICT_EVIDENCE_CSV = ROOT / "docs/results/threshold_evidence_strict_tongji.csv"
IITD_EVIDENCE_CSV = ROOT / "docs/results/threshold_evidence_iitd.csv"
COMBINED_AUDIT_CSV = ROOT / "docs/audits/metric_threshold_audit.csv"
OUT_MD = ROOT / "docs/audits/metric_threshold_audit.md"

TARGET_FARS = [1e-2, 1e-3]


def fmt_float(x: float, digits: int = 10) -> str:
    if isinstance(x, float) and math.isnan(x):
        return "nan"
    return f"{x:.{digits}g}"


def read_scores(scores_path: Path) -> tuple[np.ndarray, np.ndarray]:
    df = pd.read_csv(scores_path, usecols=["score", "label"])
    y_scores = df["score"].astype(float).to_numpy()
    y_true = df["label"].astype(int).to_numpy()
    return y_true, y_scores


def resolve_scores_from_metrics_path(metrics_path: str) -> Path:
    p = Path(metrics_path)
    candidates = [
        p.parent / "scores.csv",
        ROOT / p.parent / "scores.csv",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"Missing scores.csv for metrics_path={metrics_path!r}; tried={candidates}")


def resolve_scores_from_run_dir(run_dir: str) -> Path:
    p = Path(run_dir)
    candidates = [
        p / "scores.csv",
        ROOT / p / "scores.csv",
        ROOT / "experiments" / p / "scores.csv",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(f"Missing scores.csv for run_dir={run_dir!r}; tried={candidates}")


def compute_eer_info(fpr: np.ndarray, tpr: np.ndarray, thresholds: np.ndarray) -> Dict[str, object]:
    fnr = 1.0 - tpr

    nearest_idx = int(np.nanargmin(np.absolute(fpr - fnr)))
    nearest_eer = float((fpr[nearest_idx] + fnr[nearest_idx]) / 2.0)
    nearest_eer_threshold = float(thresholds[nearest_idx])

    interpolated_eer = nearest_eer
    interpolation_status = "fallback_nearest"
    try:
        interpolated_eer = float(brentq(lambda x: 1.0 - x - interp1d(fpr, tpr)(x), 0.0, 1.0))
        interpolation_status = "brentq_interp1d"
    except Exception as exc:
        interpolation_status = f"fallback_nearest:{type(exc).__name__}"

    return {
        "nearest_eer": nearest_eer,
        "nearest_eer_threshold": nearest_eer_threshold,
        "interpolated_eer": interpolated_eer,
        "eer_interpolation_status": interpolation_status,
    }


def evidence_rows_for_run(
    *,
    dataset: str,
    method: str,
    method_label: str,
    direction: str,
    seed: int,
    status: str,
    reported_tar_far_1e_2: float,
    reported_tar_far_1e_3: float,
    scores_path: Path,
    metrics_path: str,
) -> List[Dict[str, object]]:
    y_true, y_scores = read_scores(scores_path)
    fpr, tpr, thresholds = roc_curve(y_true, y_scores)

    if not (len(fpr) == len(tpr) == len(thresholds)):
        raise RuntimeError(
            f"ROC length mismatch for {scores_path}: "
            f"len(fpr)={len(fpr)}, len(tpr)={len(tpr)}, len(thresholds)={len(thresholds)}"
        )

    num_genuine = int((y_true == 1).sum())
    num_impostor = int((y_true == 0).sum())
    total_pairs = int(y_true.size)
    min_far_step = 1.0 / num_impostor if num_impostor else float("nan")
    eer_info = compute_eer_info(fpr, tpr, thresholds)

    rows: List[Dict[str, object]] = []
    for target_far in TARGET_FARS:
        reported_tar = reported_tar_far_1e_2 if target_far == 1e-2 else reported_tar_far_1e_3

        nearest_idx = int(np.nanargmin(np.abs(fpr - target_far)))
        nearest_empirical_far = float(fpr[nearest_idx])
        nearest_tar = float(tpr[nearest_idx])
        nearest_threshold = float(thresholds[nearest_idx])

        conservative = tar_at_far_conservative(fpr, tpr, thresholds, target_far)
        empirical_far = float(conservative["empirical_far"])
        tar = float(conservative["tar"])
        selected_threshold = float(conservative["threshold"])

        verdict = "PASS" if empirical_far <= target_far else "FAIL"
        nearest_exceeds_target = nearest_empirical_far > target_far

        rows.append({
            "dataset": dataset,
            "method": method,
            "method_label": method_label,
            "direction": direction,
            "seed": seed,
            "status": status,
            "target_far": float(target_far),
            "selected_threshold": selected_threshold,
            "empirical_far": empirical_far,
            "tar": tar,
            "num_genuine": num_genuine,
            "num_impostor": num_impostor,
            "total_pairs": total_pairs,
            "min_far_step": min_far_step,
            "reported_tar": float(reported_tar),
            "delta_conservative_minus_reported_pp": (tar - float(reported_tar)) * 100.0,
            "nearest_threshold": nearest_threshold,
            "nearest_empirical_far": nearest_empirical_far,
            "nearest_tar": nearest_tar,
            "nearest_exceeds_target": bool(nearest_exceeds_target),
            "nearest_minus_target_far": nearest_empirical_far - float(target_far),
            "roc_points": int(len(fpr)),
            **eer_info,
            "metrics_path": metrics_path,
            "scores_path": str(scores_path.resolve().relative_to(ROOT)).replace("\\", "/"),
            "verdict": verdict,
        })

    return rows


def load_strict_tongji_rows() -> List[Dict[str, object]]:
    if not STRICT_TONGJI_RUNS_CSV.exists():
        raise FileNotFoundError(STRICT_TONGJI_RUNS_CSV)

    df = pd.read_csv(STRICT_TONGJI_RUNS_CSV)
    rows: List[Dict[str, object]] = []

    for i, r in enumerate(df.to_dict("records"), start=1):
        print(f"[strict {i:02d}/{len(df)}] {r['method']} {r['direction']} seed {r['seed']}")
        scores_path = resolve_scores_from_metrics_path(str(r["metrics_path"]))
        rows.extend(evidence_rows_for_run(
            dataset="Tongji",
            method=str(r["method"]),
            method_label=str(r.get("method_label", "")),
            direction=str(r["direction"]),
            seed=int(r["seed"]),
            status=str(r.get("status", "")),
            reported_tar_far_1e_2=float(r["TAR@FAR=1e-2"]),
            reported_tar_far_1e_3=float(r["TAR@FAR=1e-3"]),
            scores_path=scores_path,
            metrics_path=str(r["metrics_path"]),
        ))

    return rows


def load_iitd_rows() -> List[Dict[str, object]]:
    if not IITD_RUNS_CSV.exists():
        raise FileNotFoundError(IITD_RUNS_CSV)

    df = pd.read_csv(IITD_RUNS_CSV)
    rows: List[Dict[str, object]] = []

    for i, r in enumerate(df.to_dict("records"), start=1):
        print(f"[iitd {i:02d}/{len(df)}] {r['method']} within seed {r['seed']}")
        scores_path = resolve_scores_from_run_dir(str(r["run_dir"]))
        rows.extend(evidence_rows_for_run(
            dataset="IITD",
            method=str(r["method"]),
            method_label=str(r.get("method_label", "")),
            direction="within",
            seed=int(r["seed"]),
            status="OK",
            # IITD rerun CSV stores metrics in percent units.
            reported_tar_far_1e_2=float(r["TAR@FAR=1e-2"]) / 100.0,
            reported_tar_far_1e_3=float(r["TAR@FAR=1e-3"]) / 100.0,
            scores_path=scores_path,
            metrics_path=str(r["metrics_path"]),
        ))

    return rows


def write_csv(path: Path, rows: Iterable[Dict[str, object]]) -> None:
    rows = list(rows)
    path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "dataset",
        "method",
        "method_label",
        "direction",
        "seed",
        "status",
        "target_far",
        "selected_threshold",
        "empirical_far",
        "tar",
        "num_genuine",
        "num_impostor",
        "total_pairs",
        "min_far_step",
        "reported_tar",
        "delta_conservative_minus_reported_pp",
        "nearest_threshold",
        "nearest_empirical_far",
        "nearest_tar",
        "nearest_exceeds_target",
        "nearest_minus_target_far",
        "roc_points",
        "nearest_eer",
        "nearest_eer_threshold",
        "interpolated_eer",
        "eer_interpolation_status",
        "verdict",
        "metrics_path",
        "scores_path",
    ]

    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def summarize_rows(rows: List[Dict[str, object]]) -> Dict[str, object]:
    if not rows:
        return {
            "n_rows": 0,
            "n_runs": 0,
            "fail_count": 0,
            "nearest_exceeds_count": 0,
            "max_delta_abs_pp": float("nan"),
            "min_far_steps": [],
            "pair_shapes": [],
        }

    return {
        "n_rows": len(rows),
        "n_runs": len({(r["dataset"], r["method"], r["direction"], r["seed"]) for r in rows}),
        "fail_count": sum(1 for r in rows if r["verdict"] != "PASS"),
        "nearest_exceeds_count": sum(1 for r in rows if bool(r["nearest_exceeds_target"])),
        "max_delta_abs_pp": max(abs(float(r["delta_conservative_minus_reported_pp"])) for r in rows),
        "min_far_steps": sorted({float(r["min_far_step"]) for r in rows}),
        "pair_shapes": sorted({(int(r["num_genuine"]), int(r["num_impostor"]), int(r["total_pairs"])) for r in rows}),
    }


def write_markdown(strict_rows: List[Dict[str, object]], iitd_rows: List[Dict[str, object]]) -> None:
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)

    all_rows = strict_rows + iitd_rows
    strict_summary = summarize_rows(strict_rows)
    iitd_summary = summarize_rows(iitd_rows)
    all_summary = summarize_rows(all_rows)

    md: List[str] = []
    md.append("# Metric Threshold Audit")
    md.append("")
    md.append("This audit documents the revision from the previous nearest-FPR TAR@FAR rule to the conservative empirical-FAR rule used in the revised metric implementation.")
    md.append("")
    md.append("## Metric convention")
    md.append("")
    md.append("- Previous rule: choose the ROC point whose empirical FPR is nearest to the target FAR. This can select a point above the requested FAR.")
    md.append("- Revised rule: choose only ROC points with empirical FPR less than or equal to the target FAR, then select the valid point with the highest TPR.")
    md.append("- EER convention remains unchanged: sklearn ROC with brentq/interp1d interpolation when possible, falling back to nearest |FPR-FNR|.")
    md.append("")
    md.append("## Required evidence artifacts")
    md.append("")
    md.append(f"- Strict Tongji threshold evidence: `{STRICT_EVIDENCE_CSV.relative_to(ROOT).as_posix()}`")
    md.append(f"- IITD threshold evidence: `{IITD_EVIDENCE_CSV.relative_to(ROOT).as_posix()}`")
    md.append(f"- Combined audit CSV: `{COMBINED_AUDIT_CSV.relative_to(ROOT).as_posix()}`")
    md.append("")
    md.append("## Summary")
    md.append("")
    md.append("| Dataset | Runs | Evidence rows | Conservative failures | Nearest-FPR rows above target | Max abs delta TAR vs reported (pp) | Pair count shapes | min FAR step values |")
    md.append("|---|---:|---:|---:|---:|---:|---|---|")
    for dataset_name, summary in [
        ("Tongji", strict_summary),
        ("IITD", iitd_summary),
        ("Combined", all_summary),
    ]:
        md.append(
            f"| {dataset_name} | {summary['n_runs']} | {summary['n_rows']} | "
            f"{summary['fail_count']} | {summary['nearest_exceeds_count']} | "
            f"{fmt_float(float(summary['max_delta_abs_pp']), 6)} | "
            f"{summary['pair_shapes']} | "
            f"{[fmt_float(x, 12) for x in summary['min_far_steps']]} |"
        )
    md.append("")
    md.append("## Definition-of-done checks")
    md.append("")
    md.append(f"- Conservative empirical FAR never exceeds target FAR: `{all_summary['fail_count'] == 0}`")
    md.append(f"- Strict Tongji evidence rows: `{strict_summary['n_rows']}`")
    md.append(f"- IITD evidence rows: `{iitd_summary['n_rows']}`")
    md.append("")
    md.append("## Per-run conservative TAR@FAR=1e-3 evidence")
    md.append("")
    md.append("| Dataset | Method | Direction | Seed | Target FAR | Selected empirical FAR | TAR | Nearest FPR | Nearest above target? | Delta vs reported (pp) |")
    md.append("|---|---|---|---:|---:|---:|---:|---:|---|---:|")
    for r in all_rows:
        if abs(float(r["target_far"]) - 1e-3) > 1e-15:
            continue
        md.append(
            f"| {r['dataset']} | {r['method']} | {r['direction']} | {r['seed']} | "
            f"{fmt_float(float(r['target_far']), 4)} | "
            f"{fmt_float(float(r['empirical_far']), 8)} | "
            f"{fmt_float(float(r['tar']), 8)} | "
            f"{fmt_float(float(r['nearest_empirical_far']), 8)} | "
            f"{r['nearest_exceeds_target']} | "
            f"{fmt_float(float(r['delta_conservative_minus_reported_pp']), 6)} |"
        )
    md.append("")
    md.append("## Paper wording")
    md.append("")
    md.append("TAR@FAR is computed using a conservative empirical-FAR rule: among ROC points whose empirical FAR does not exceed the target, the reported TAR is the maximum observed TPR. The threshold audit exports the selected threshold, empirical FAR, TAR, genuine/impostor counts, and minimum FAR step for every method--dataset--direction--seed run.")

    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")


def main() -> None:
    strict_rows = load_strict_tongji_rows()
    iitd_rows = load_iitd_rows()
    all_rows = strict_rows + iitd_rows

    write_csv(STRICT_EVIDENCE_CSV, strict_rows)
    write_csv(IITD_EVIDENCE_CSV, iitd_rows)
    write_csv(COMBINED_AUDIT_CSV, all_rows)
    write_markdown(strict_rows, iitd_rows)

    print(f"Wrote {STRICT_EVIDENCE_CSV}")
    print(f"Wrote {IITD_EVIDENCE_CSV}")
    print(f"Wrote {COMBINED_AUDIT_CSV}")
    print(f"Wrote {OUT_MD}")
    print(f"Conservative failures: {sum(1 for r in all_rows if r['verdict'] != 'PASS')}")
    print(f"Nearest-FPR rows above target: {sum(1 for r in all_rows if bool(r['nearest_exceeds_target']))}")


if __name__ == "__main__":
    main()
