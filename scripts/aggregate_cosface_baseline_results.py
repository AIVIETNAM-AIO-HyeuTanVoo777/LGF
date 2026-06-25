from __future__ import annotations

import csv
import json
from pathlib import Path
from statistics import mean, pstdev


ROOT = Path(__file__).resolve().parents[1]
EXP_DIR = ROOT / "experiments"
OUT_DIR = ROOT / "docs" / "results"

SEEDS = [42, 2026, 2705]
DIRECTIONS = {
    "s1s2": "S1->S2",
    "s2s1": "S2->S1",
}

RUN_TEMPLATE = "b8_resnet18_cosface_tongji_subject_disjoint_{direction}_seed{seed}"

METRIC_KEYS = {
    "rank1": ["rank1", "rank_1", "Rank-1", "rank_1_accuracy"],
    "rank5": ["rank5", "rank_5", "Rank-5", "rank_5_accuracy"],
    "macro_f1": ["macro_f1", "Macro-F1", "macro_f1_score"],
    "eer": ["eer", "EER"],
    "tar_far_1e_2": ["tar_far_1e-2", "tar@far=1e-2", "TAR@FAR=1e-2", "tar_at_far_1e-2"],
    "tar_far_1e_3": ["tar_far_1e-3", "tar@far=1e-3", "TAR@FAR=1e-3", "tar_at_far_1e-3"],
}


def read_metric(metrics: dict, canonical_key: str) -> float:
    for key in METRIC_KEYS[canonical_key]:
        if key in metrics:
            return float(metrics[key])
    raise KeyError(f"Missing metric {canonical_key}. Available keys: {sorted(metrics)}")


def to_pp(x: float) -> float:
    return 100.0 * float(x)


def fmt_mean_std(values: list[float]) -> str:
    return f"{mean(values):.3f} +/- {pstdev(values):.3f}"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    rows = []
    for direction_key, direction_label in DIRECTIONS.items():
        for seed in SEEDS:
            run_name = RUN_TEMPLATE.format(direction=direction_key, seed=seed)
            metrics_path = EXP_DIR / run_name / "metrics.json"
            scores_path = EXP_DIR / run_name / "scores.csv"

            if not metrics_path.exists():
                raise FileNotFoundError(metrics_path)
            if not scores_path.exists():
                raise FileNotFoundError(scores_path)

            metrics = json.loads(metrics_path.read_text(encoding="utf-8"))

            rows.append({
                "method": "B8",
                "method_label": "ResNet18 + CosFace",
                "palmprint_specific": "No",
                "learned": "Yes",
                "direction": direction_label,
                "seed": seed,
                "rank1_pp": to_pp(read_metric(metrics, "rank1")),
                "rank5_pp": to_pp(read_metric(metrics, "rank5")),
                "macro_f1_pp": to_pp(read_metric(metrics, "macro_f1")),
                "eer_pp": to_pp(read_metric(metrics, "eer")),
                "tar_far_1e_2_pp": to_pp(read_metric(metrics, "tar_far_1e_2")),
                "tar_far_1e_3_pp": to_pp(read_metric(metrics, "tar_far_1e_3")),
                "comment": "Generic learned margin-loss baseline; not palmprint-specific.",
                "metrics_path": str(metrics_path.relative_to(ROOT)).replace("\\", "/"),
                "scores_path": str(scores_path.relative_to(ROOT)).replace("\\", "/"),
            })

    detail_csv = OUT_DIR / "strict_tongji_b8_cosface_detail.csv"
    with detail_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    summary_rows = []
    for direction_label in [*DIRECTIONS.values(), "Both"]:
        subset = rows if direction_label == "Both" else [r for r in rows if r["direction"] == direction_label]
        summary_rows.append({
            "method": "B8",
            "method_label": "ResNet18 + CosFace",
            "palmprint_specific": "No",
            "learned": "Yes",
            "direction": direction_label,
            "n": len(subset),
            "rank1_pp_mean_std": fmt_mean_std([r["rank1_pp"] for r in subset]),
            "rank5_pp_mean_std": fmt_mean_std([r["rank5_pp"] for r in subset]),
            "macro_f1_pp_mean_std": fmt_mean_std([r["macro_f1_pp"] for r in subset]),
            "eer_pp_mean_std": fmt_mean_std([r["eer_pp"] for r in subset]),
            "tar_far_1e_2_pp_mean_std": fmt_mean_std([r["tar_far_1e_2_pp"] for r in subset]),
            "tar_far_1e_3_pp_mean_std": fmt_mean_std([r["tar_far_1e_3_pp"] for r in subset]),
            "comment": "Generic learned margin-loss baseline; not palmprint-specific.",
        })

    summary_csv = OUT_DIR / "strict_tongji_additional_baselines.csv"
    with summary_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary_rows[0].keys()))
        writer.writeheader()
        writer.writerows(summary_rows)

    md = []
    md.append("# Strict Tongji Additional Baselines")
    md.append("")
    md.append("This table adds B8, a generic learned CosFace baseline, outside the B0--B7 component matrix.")
    md.append("")
    md.append("B8 is not palmprint-specific. It is included as a stronger generic metric-learning baseline using the existing margin-head training path.")
    md.append("")
    md.append("## Summary")
    md.append("")
    md.append("| Method | Palmprint-specific? | Learned? | Direction | n | Rank-1 | EER | TAR@FAR=1e-3 | Comment |")
    md.append("|---|---:|---:|---|---:|---:|---:|---:|---|")
    for r in summary_rows:
        md.append(
            f"| {r['method_label']} | {r['palmprint_specific']} | {r['learned']} | "
            f"{r['direction']} | {r['n']} | {r['rank1_pp_mean_std']} | "
            f"{r['eer_pp_mean_std']} | {r['tar_far_1e_3_pp_mean_std']} | {r['comment']} |"
        )
    md.append("")
    md.append("## Detail")
    md.append("")
    md.append("| Direction | Seed | Rank-1 | Rank-5 | Macro-F1 | EER | TAR@FAR=1e-2 | TAR@FAR=1e-3 |")
    md.append("|---|---:|---:|---:|---:|---:|---:|---:|")
    for r in rows:
        md.append(
            f"| {r['direction']} | {r['seed']} | {r['rank1_pp']:.3f} | {r['rank5_pp']:.3f} | "
            f"{r['macro_f1_pp']:.3f} | {r['eer_pp']:.3f} | "
            f"{r['tar_far_1e_2_pp']:.3f} | {r['tar_far_1e_3_pp']:.3f} |"
        )
    md.append("")
    md.append("## Claim boundary")
    md.append("")
    md.append("- Safe: B8 is an additional generic learned CosFace baseline under the same strict Tongji protocol.")
    md.append("- Unsafe: B8 is a palmprint-specific baseline, PalmNet/CompNet/Competitive-Code replacement, or state-of-the-art method.")
    md.append("")

    summary_md = OUT_DIR / "strict_tongji_additional_baselines.md"
    summary_md.write_text("\n".join(md), encoding="utf-8")

    print(f"Wrote {detail_csv.relative_to(ROOT)} rows={len(rows)}")
    print(f"Wrote {summary_csv.relative_to(ROOT)} rows={len(summary_rows)}")
    print(f"Wrote {summary_md.relative_to(ROOT)}")


if __name__ == "__main__":
    main()