from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from pathlib import Path
from statistics import mean, stdev


OUT_CSV = Path("docs/results/strict_tongji_score_diagnostics.csv")
OUT_SUMMARY_CSV = Path("docs/results/strict_tongji_score_diagnostics_summary.csv")
OUT_MD = Path("docs/results/strict_tongji_score_diagnostics.md")

METHOD_LABELS = {
    "B0": "ResNet18 + CE",
    "B1": "ResNet18 + CE + SupCon",
    "B4": "ResNet18 + ArcFace",
    "B5": "ResNet18 + BNNeck + CE",
    "B6": "ResNet18 + BNNeck + ArcFace",
    "B7": "ResNet18 + BNNeck + ArcFace + light SupCon",
}

METHOD_PATTERNS = {
    "B0": "b0_resnet18_ce_tongji_subject_disjoint_*_seed*",
    "B1": "b1_resnet18_ce_supcon_tongji_subject_disjoint_*_seed*",
    "B4": "b4_resnet18_arcface_tongji_subject_disjoint_*_seed*",
    "B5": "b5_resnet18_bnneck_ce_tongji_subject_disjoint_*_seed*",
    "B6": "b6_resnet18_bnneck_arcface_tongji_subject_disjoint_*_seed*",
    "B7": "b7_resnet18_bnneck_arcface_light_supcon_tongji_subject_disjoint_*_seed*",
}


def infer_direction(run_name: str) -> str:
    if "_s1s2_" in run_name:
        return "S1->S2"
    if "_s2s1_" in run_name:
        return "S2->S1"
    raise ValueError(f"Cannot infer direction from {run_name}")


def infer_seed(run_name: str) -> int:
    m = re.search(r"_seed(\d+)$", run_name)
    if not m:
        raise ValueError(f"Cannot infer seed from {run_name}")
    return int(m.group(1))


def summarize(values: list[float]) -> tuple[float, float]:
    if len(values) == 1:
        return values[0], 0.0
    return mean(values), stdev(values)


def fmt_float(x: float) -> str:
    return f"{x:.6f}"


def main() -> None:
    rows: list[dict[str, object]] = []

    for method, pattern in METHOD_PATTERNS.items():
        for exp_dir in sorted(Path("experiments").glob(pattern)):
            diag_path = exp_dir / "score_diagnostics.json"
            if not diag_path.exists():
                raise FileNotFoundError(diag_path)

            run_name = exp_dir.name
            diag = json.loads(diag_path.read_text(encoding="utf-8"))

            rows.append({
                "method": method,
                "method_label": METHOD_LABELS[method],
                "direction": infer_direction(run_name),
                "seed": infer_seed(run_name),
                "run_name": run_name,
                "num_genuine_pairs": int(diag["num_genuine_pairs"]),
                "num_impostor_pairs": int(diag["num_impostor_pairs"]),
                "genuine_mean": float(diag["genuine_mean"]),
                "genuine_std": float(diag["genuine_std"]),
                "impostor_mean": float(diag["impostor_mean"]),
                "impostor_std": float(diag["impostor_std"]),
                "impostor_q0.990": float(diag["impostor_q0.990"]),
                "impostor_q0.999": float(diag["impostor_q0.999"]),
                "genuine_q0.001": float(diag["genuine_q0.001"]),
                "genuine_q0.010": float(diag["genuine_q0.010"]),
                "d_prime": float(diag["d_prime"]),
            })

    if len(rows) != 36:
        raise RuntimeError(f"Expected 36 diagnostic rows, found {len(rows)}")

    rows.sort(key=lambda r: (str(r["method"]), str(r["direction"]), int(r["seed"])))

    fieldnames = [
        "method", "method_label", "direction", "seed", "run_name",
        "num_genuine_pairs", "num_impostor_pairs",
        "genuine_mean", "genuine_std", "impostor_mean", "impostor_std",
        "impostor_q0.990", "impostor_q0.999", "genuine_q0.001", "genuine_q0.010",
        "d_prime",
    ]

    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    metrics = [
        "genuine_mean",
        "genuine_std",
        "impostor_mean",
        "impostor_std",
        "impostor_q0.990",
        "impostor_q0.999",
        "genuine_q0.001",
        "genuine_q0.010",
        "d_prime",
    ]

    groups: dict[tuple[str, str, str], list[dict[str, object]]] = defaultdict(list)
    for r in rows:
        groups[(str(r["method"]), str(r["method_label"]), "ALL")].append(r)
        groups[(str(r["method"]), str(r["method_label"]), str(r["direction"]))].append(r)

    direction_order = {"ALL": 0, "S1->S2": 1, "S2->S1": 2}
    summary_rows: list[dict[str, object]] = []

    for key, items in sorted(groups.items(), key=lambda x: (x[0][0], direction_order[x[0][2]])):
        method, label, direction = key
        out: dict[str, object] = {
            "method": method,
            "method_label": label,
            "direction": direction,
            "n": len(items),
        }
        for metric in metrics:
            vals = [float(item[metric]) for item in items]
            mu, sd = summarize(vals)
            out[f"{metric}_mean"] = mu
            out[f"{metric}_std"] = sd
        summary_rows.append(out)

    if len(summary_rows) != 18:
        raise RuntimeError(f"Expected 18 summary rows, found {len(summary_rows)}")

    summary_fields = ["method", "method_label", "direction", "n"]
    for metric in metrics:
        summary_fields.extend([f"{metric}_mean", f"{metric}_std"])

    with OUT_SUMMARY_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(summary_rows)

    md: list[str] = []
    md.append("# Strict Tongji Score Diagnostics")
    md.append("")
    md.append("This table summarizes genuine/impostor cosine-score distributions for the strict Tongji palm-class-disjoint ablation runs. Values are aggregated over two session directions and three seeds unless a direction is specified.")
    md.append("")
    md.append("## Overall summary")
    md.append("")
    md.append("| Method | Direction | Genuine mean | Impostor mean | Impostor q0.999 | Genuine q0.001 | d-prime |")
    md.append("|---|---|---:|---:|---:|---:|---:|")

    for r in summary_rows:
        if r["direction"] != "ALL":
            continue
        md.append(
            f"| {r['method']} {r['method_label']} | {r['direction']} | "
            f"{fmt_float(float(r['genuine_mean_mean']))}+/-{fmt_float(float(r['genuine_mean_std']))} | "
            f"{fmt_float(float(r['impostor_mean_mean']))}+/-{fmt_float(float(r['impostor_mean_std']))} | "
            f"{fmt_float(float(r['impostor_q0.999_mean']))}+/-{fmt_float(float(r['impostor_q0.999_std']))} | "
            f"{fmt_float(float(r['genuine_q0.001_mean']))}+/-{fmt_float(float(r['genuine_q0.001_std']))} | "
            f"{fmt_float(float(r['d_prime_mean']))}+/-{fmt_float(float(r['d_prime_std']))} |"
        )

    md.append("")
    md.append("## Interpretation")
    md.append("")
    md.append("- `impostor_q0.999` approximates the high-impostor-score tail relevant to strict low-FAR behavior.")
    md.append("- Higher `d-prime` indicates stronger separation between genuine and impostor score distributions.")
    md.append("- These diagnostics should be interpreted together with TAR@FAR and EER, not as replacement metrics.")
    md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")

    print(f"RUN_ROWS={len(rows)}")
    print(f"SUMMARY_ROWS={len(summary_rows)}")
    print(f"WROTE={OUT_CSV}")
    print(f"WROTE={OUT_SUMMARY_CSV}")
    print(f"WROTE={OUT_MD}")


if __name__ == "__main__":
    main()