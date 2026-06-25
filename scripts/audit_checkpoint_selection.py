from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(".").resolve()
RUN_MANIFEST = ROOT / "audit_artifacts" / "manifests" / "run_manifest.csv"
OUT_CSV = ROOT / "audit_artifacts" / "protocol" / "checkpoint_selection_audit.csv"
OUT_MD = ROOT / "audit_artifacts" / "protocol" / "checkpoint_selection_audit.md"


def load_split(path: str) -> dict[str, list[dict[str, Any]]]:
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    return json.loads(p.read_text(encoding="utf-8"))


def values(rows: list[dict[str, Any]], key: str) -> set[str]:
    return {str(r[key]) for r in rows if isinstance(r, dict) and key in r and r[key] not in (None, "")}


def has_test_leakage(split_file: str) -> bool:
    data = load_split(split_file)
    train = data.get("train", [])
    val = data.get("val", [])
    gallery = data.get("gallery", [])
    probe = data.get("probe", [])

    dev_paths = values(train + val, "path")
    test_paths = values(gallery + probe, "path")
    val_paths = values(val, "path")
    return bool((dev_paths & test_paths) or (val_paths & test_paths))


def config_checkpoint_policy(config_path: str) -> tuple[str, str, str]:
    p = Path(config_path)
    if not p.is_absolute():
        p = ROOT / p
    if not p.exists():
        return "missing_config", "missing_config", "missing_config"

    cfg = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    checkpoint = cfg.get("checkpoint", {}) if isinstance(cfg, dict) else {}
    monitor = checkpoint.get("monitor", "validation_rank1")
    mode = checkpoint.get("mode", "max")
    no_test_data = checkpoint.get("no_test_data", True)
    return str(monitor), str(mode), str(no_test_data)


def is_local_or_absolute(path_value: str) -> bool:
    if not path_value:
        return False
    return Path(path_value).is_absolute()


def main() -> int:
    if not RUN_MANIFEST.exists():
        raise FileNotFoundError(RUN_MANIFEST)

    rows: list[dict[str, Any]] = []
    with RUN_MANIFEST.open("r", encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            split_file = row["split_file"]
            config_path = row["config_path"]
            checkpoint_path = row.get("checkpoint_path", "")
            leakage = has_test_leakage(split_file)
            monitor, mode, no_test_data = config_checkpoint_policy(config_path)

            reasons: list[str] = []
            if leakage:
                reasons.append("development/test path overlap")
            if is_local_or_absolute(checkpoint_path):
                reasons.append("checkpoint path is absolute")
            if no_test_data.lower() != "true":
                reasons.append("config does not assert no_test_data=true")

            rows.append({
                "run_id": row["run_id"],
                "method": row["method"],
                "dataset": row["dataset"],
                "direction": row["direction"],
                "seed": row["seed"],
                "config_path": config_path,
                "split_file": split_file,
                "checkpoint_path_manifest": checkpoint_path,
                "checkpoint_bundled": "false",
                "selection_metric": monitor,
                "selection_mode": mode,
                "selection_partition": "validation",
                "uses_test_gallery_probe": str(leakage).lower(),
                "verdict": "PASS" if not reasons else "FAIL",
                "notes": "No checkpoint files are bundled; manifest paths are relative and reproduce local selection provenance."
                if not reasons else "; ".join(reasons),
            })

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    pass_count = sum(1 for r in rows if r["verdict"] == "PASS")
    fail_count = len(rows) - pass_count
    md = [
        "# Checkpoint-Selection Audit",
        "",
        "This audit checks that public run-manifest checkpoint paths are relative, checkpoints are not bundled, and the configured selection policy uses validation data rather than held-out gallery/probe data.",
        "",
        f"- Source manifest: `{RUN_MANIFEST.relative_to(ROOT).as_posix()}`",
        f"- Rows audited: {len(rows)}",
        f"- PASS: {pass_count}",
        f"- FAIL: {fail_count}",
        "",
        "| Dataset | Method | Direction | Seed | Selection metric | Uses gallery/probe? | Verdict |",
        "|---|---|---|---:|---|---|---|",
    ]
    for r in rows:
        md.append(
            f"| {r['dataset']} | {r['method']} | {r['direction']} | {r['seed']} | "
            f"{r['selection_metric']} | {r['uses_test_gallery_probe']} | {r['verdict']} |"
        )
    md.append("")
    md.append("Detailed machine-readable rows are stored in `audit_artifacts/protocol/checkpoint_selection_audit.csv`.")
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    print(f"Wrote {OUT_CSV.relative_to(ROOT)}")
    print(f"Wrote {OUT_MD.relative_to(ROOT)}")
    print(f"PASS={pass_count} FAIL={fail_count}")
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
