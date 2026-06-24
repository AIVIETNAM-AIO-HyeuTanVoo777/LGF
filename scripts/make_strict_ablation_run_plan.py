from __future__ import annotations

from pathlib import Path
import yaml


CONFIG_DIR = Path("configs")
OUT = Path("docs/reproducibility/strict_ablation_run_plan.md")

METHOD_LABELS = {
    "b0": "B0",
    "b4": "B4",
    "b5": "B5",
    "b7": "B7",
}


def infer_method(name: str) -> str:
    return name.split("_", 1)[0].upper()


def infer_direction(name: str) -> str:
    if "_s1s2_" in name:
        return "S1->S2"
    if "_s2s1_" in name:
        return "S2->S1"
    return "unknown"


def infer_seed(name: str) -> str:
    stem = Path(name).stem
    idx = stem.rfind("seed")
    return stem[idx + 4 :] if idx >= 0 else "unknown"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)

    configs = []
    for method in ["b0", "b4", "b5", "b7"]:
        configs.extend(sorted(CONFIG_DIR.glob(f"{method}_*_tongji_subject_disjoint_*_seed*.yaml")))

    lines = [
        "# Strict Tongji Ablation Run Plan",
        "",
        "This checklist covers the missing strict-protocol Tongji ablation rows required for the rank-B plan.",
        "",
        "Paper terminology is `palm-class-disjoint`; config filenames retain historical `subject_disjoint` naming for compatibility.",
        "",
        "| method | direction | seed | config | save_dir | train status | eval status | metrics path |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]

    for cfg_path in configs:
        cfg = yaml.safe_load(cfg_path.read_text(encoding="utf-8"))
        method = infer_method(cfg_path.name)
        direction = infer_direction(cfg_path.name)
        seed = infer_seed(cfg_path.name)
        save_dir = cfg["save_dir"]
        metrics_path = f"{save_dir}/metrics.json"
        lines.append(
            f"| {method} | {direction} | {seed} | `{cfg_path.as_posix()}` | `{save_dir}` | pending | pending | `{metrics_path}` |"
        )

    lines.append("")
    lines.append(f"Total planned runs: {len(configs)}")
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT}")
    print(f"TOTAL={len(configs)}")


if __name__ == "__main__":
    main()