from __future__ import annotations

import json
from pathlib import Path
import statistics
import yaml


CONFIG_DIR = Path("configs")
OUT_DIR = Path("docs/results")
OUT_DIR.mkdir(parents=True, exist_ok=True)

METHODS = {
    "b0": "ResNet18 + CE",
    "b1": "ResNet18 + CE + SupCon",
    "b4": "ResNet18 + ArcFace",
    "b5": "ResNet18 + BNNeck + CE",
    "b6": "ResNet18 + BNNeck + ArcFace",
    "b7": "ResNet18 + BNNeck + ArcFace + light SupCon",
}

METRIC_KEYS = [
    "Rank-1",
    "Rank-5",
    "Macro-F1",
    "EER",
    "TAR@FAR=1e-2",
    "TAR@FAR=1e-3",
]


def direction_from_name(name: str) -> str:
    if "_s1s2_" in name:
        return "S1->S2"
    if "_s2s1_" in name:
        return "S2->S1"
    return "unknown"


def seed_from_name(name: str) -> int:
    stem = Path(name).stem
    return int(stem.rsplit("seed", 1)[1])


def method_from_name(name: str) -> str:
    return name.split("_", 1)[0]


def read_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def fmt_pct(x: float | None) -> str:
    if x is None:
        return "NA"
    return f"{x * 100:.2f}"


def fmt_raw(x: float | None) -> str:
    if x is None:
        return "NA"
    return f"{x:.6f}"


def row_from_config(cfg_path: Path) -> dict:
    cfg = read_yaml(cfg_path)
    method = method_from_name(cfg_path.name)
    direction = direction_from_name(cfg_path.name)
    seed = seed_from_name(cfg_path.name)
    save_dir = Path(cfg["save_dir"])
    metrics_path = save_dir / "metrics.json"

    row = {
        "method": method.upper(),
        "method_label": METHODS.get(method, method),
        "direction": direction,
        "seed": seed,
        "config": cfg_path.as_posix(),
        "save_dir": save_dir.as_posix(),
        "metrics_path": metrics_path.as_posix(),
        "status": "OK" if metrics_path.exists() else "MISSING",
    }

    if metrics_path.exists():
        metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
        for k in METRIC_KEYS:
            row[k] = float(metrics[k])
    else:
        for k in METRIC_KEYS:
            row[k] = None

    return row


def collect_rows() -> list[dict]:
    rows = []
    for method in METHODS:
        for cfg_path in sorted(CONFIG_DIR.glob(f"{method}_*_tongji_subject_disjoint_*_seed*.yaml")):
            rows.append(row_from_config(cfg_path))
    rows.sort(key=lambda r: (r["method"], r["direction"], r["seed"]))
    return rows


def write_csv(rows: list[dict], path: Path) -> None:
    headers = [
        "method",
        "method_label",
        "direction",
        "seed",
        "status",
        "Rank-1",
        "Rank-5",
        "Macro-F1",
        "EER",
        "TAR@FAR=1e-2",
        "TAR@FAR=1e-3",
        "config",
        "metrics_path",
    ]
    lines = [",".join(headers)]
    for r in rows:
        vals = []
        for h in headers:
            v = r.get(h)
            if isinstance(v, float):
                vals.append(f"{v:.10f}")
            else:
                vals.append(str(v).replace(",", ";"))
        lines.append(",".join(vals))
    path.write_text("\n".join(lines), encoding="utf-8")


def summarize(rows: list[dict]) -> list[dict]:
    summaries = []
    ok_rows = [r for r in rows if r["status"] == "OK"]

    for method in sorted({r["method"] for r in ok_rows}):
        mr = [r for r in ok_rows if r["method"] == method]
        for direction in ["S1->S2", "S2->S1", "ALL"]:
            dr = mr if direction == "ALL" else [r for r in mr if r["direction"] == direction]
            if not dr:
                continue
            s = {
                "method": method,
                "method_label": mr[0]["method_label"],
                "direction": direction,
                "n": len(dr),
            }
            for k in METRIC_KEYS:
                vals = [r[k] for r in dr if r[k] is not None]
                s[f"{k}_mean"] = statistics.mean(vals) if vals else None
                s[f"{k}_std"] = statistics.stdev(vals) if len(vals) >= 2 else 0.0
            summaries.append(s)

    summaries.sort(key=lambda r: (r["method"], r["direction"]))
    return summaries


def write_summary_csv(summaries: list[dict], path: Path) -> None:
    headers = ["method", "method_label", "direction", "n"]
    for k in METRIC_KEYS:
        headers += [f"{k}_mean", f"{k}_std"]

    lines = [",".join(headers)]
    for r in summaries:
        vals = []
        for h in headers:
            v = r.get(h)
            if isinstance(v, float):
                vals.append(f"{v:.10f}")
            else:
                vals.append(str(v))
        lines.append(",".join(vals))
    path.write_text("\n".join(lines), encoding="utf-8")


def write_markdown(rows: list[dict], summaries: list[dict], path: Path) -> None:
    lines = [
        "# Strict Tongji Ablation Results",
        "",
        "Terminology: the paper claim is capped at palm-class-disjoint by audit; config filenames retain historical `subject_disjoint` naming for compatibility.",
        "",
        "## Summary by method and direction",
        "",
        "| Method | Direction | n | Rank-1 mean+/-std (%) | Rank-5 mean+/-std (%) | EER mean+/-std (%) | TAR@1e-3 mean+/-std (%) |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]

    for s in summaries:
        lines.append(
            "| {method} {label} | {direction} | {n} | {r1m}+/-{r1s} | {r5m}+/-{r5s} | {eerm}+/-{eers} | {tar3m}+/-{tar3s} |".format(
                method=s["method"],
                label=s["method_label"],
                direction=s["direction"],
                n=s["n"],
                r1m=fmt_pct(s["Rank-1_mean"]),
                r1s=fmt_pct(s["Rank-1_std"]),
                r5m=fmt_pct(s["Rank-5_mean"]),
                r5s=fmt_pct(s["Rank-5_std"]),
                eerm=fmt_pct(s["EER_mean"]),
                eers=fmt_pct(s["EER_std"]),
                tar3m=fmt_pct(s["TAR@FAR=1e-3_mean"]),
                tar3s=fmt_pct(s["TAR@FAR=1e-3_std"]),
            )
        )

    lines += [
        "",
        "## Per-run results",
        "",
        "| Method | Direction | Seed | Status | Rank-1 (%) | Rank-5 (%) | Macro-F1 (%) | EER (%) | TAR@1e-2 (%) | TAR@1e-3 (%) |",
        "| --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]

    for r in rows:
        lines.append(
            f"| {r['method']} {r['method_label']} | {r['direction']} | {r['seed']} | {r['status']} | "
            f"{fmt_pct(r['Rank-1'])} | {fmt_pct(r['Rank-5'])} | {fmt_pct(r['Macro-F1'])} | "
            f"{fmt_pct(r['EER'])} | {fmt_pct(r['TAR@FAR=1e-2'])} | {fmt_pct(r['TAR@FAR=1e-3'])} |"
        )

    missing = [r for r in rows if r["status"] != "OK"]
    lines += [
        "",
        f"Missing metrics: {len(missing)}",
    ]
    for r in missing:
        lines.append(f"- `{r['metrics_path']}`")

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows = collect_rows()
    summaries = summarize(rows)

    write_csv(rows, OUT_DIR / "strict_tongji_ablation_runs.csv")
    write_summary_csv(summaries, OUT_DIR / "strict_tongji_ablation_summary.csv")
    write_markdown(rows, summaries, OUT_DIR / "strict_tongji_ablation_results.md")

    print(f"RUN_ROWS={len(rows)}")
    print(f"OK_ROWS={sum(r['status'] == 'OK' for r in rows)}")
    print(f"MISSING_ROWS={sum(r['status'] != 'OK' for r in rows)}")
    print(f"WROTE={OUT_DIR / 'strict_tongji_ablation_runs.csv'}")
    print(f"WROTE={OUT_DIR / 'strict_tongji_ablation_summary.csv'}")
    print(f"WROTE={OUT_DIR / 'strict_tongji_ablation_results.md'}")


if __name__ == "__main__":
    main()