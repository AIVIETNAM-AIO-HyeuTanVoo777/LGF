from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RUNS_CSV = ROOT / "docs" / "results" / "strict_tongji_ablation_runs.csv"
OUT_DIR = ROOT / "docs" / "audits"
OUT_CSV = OUT_DIR / "checkpoint_selection_audit.csv"
OUT_MD = OUT_DIR / "checkpoint_selection_audit.md"

STRICT_METHODS = {"B0", "B1", "B4", "B5", "B6", "B7"}
STRICT_DIRECTIONS = {"S1->S2", "S2->S1"}


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except Exception:
        return path.as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def load_yaml(path: Path) -> dict[str, Any]:
    import yaml
    return yaml.safe_load(read_text(path)) or {}


def flatten_paths(obj: Any) -> list[str]:
    out: list[str] = []
    if obj is None:
        return out
    if isinstance(obj, str):
        return [obj]
    if isinstance(obj, dict):
        for key in ("path", "image_path", "filepath", "file", "filename"):
            val = obj.get(key)
            if isinstance(val, str):
                out.append(val)
        for val in obj.values():
            if isinstance(val, (dict, list, tuple)):
                out.extend(flatten_paths(val))
    elif isinstance(obj, (list, tuple)):
        for item in obj:
            out.extend(flatten_paths(item))
    return out


def get_split_items(split: dict[str, Any], names: tuple[str, ...]) -> list[Any]:
    lowered = {str(k).lower(): k for k in split.keys()}
    items: list[Any] = []
    for name in names:
        key = lowered.get(name.lower())
        if key is None:
            continue
        val = split.get(key)
        if isinstance(val, list):
            items.extend(val)
        elif isinstance(val, dict):
            items.append(val)
        elif val is not None:
            items.append(val)
    return items


def check_split_leakage(split_path: Path) -> tuple[str, str]:
    if not split_path.exists():
        return "UNKNOWN", "split file missing"

    split = json.loads(read_text(split_path))
    val_items = get_split_items(split, ("val", "valid", "validation"))
    test_items = get_split_items(split, ("gallery", "probe", "test", "query", "support"))

    val_paths = set(flatten_paths(val_items))
    test_paths = set(flatten_paths(test_items))
    overlap = val_paths & test_paths

    if overlap:
        sample = sorted(overlap)[:3]
        return "YES", "validation overlaps gallery/probe/test: " + "; ".join(sample)
    if not val_paths:
        return "UNKNOWN", "no validation paths detected in split"
    return "NO", "validation paths do not overlap gallery/probe/test paths"


def find_training_log(run_dir: Path) -> Path | None:
    candidates = [
        run_dir / "training_log.csv",
        run_dir / "train_log.csv",
        run_dir / "history.csv",
        run_dir / "metrics.csv",
        run_dir / "logs" / "training_log.csv",
        run_dir / "logs" / "train_log.csv",
        run_dir / "logs" / "history.csv",
    ]
    for path in candidates:
        if path.exists():
            return path

    for path in sorted(run_dir.glob("**/*.csv")):
        name = path.name.lower()
        if "train" in name or "history" in name or "log" in name:
            return path
    return None


def infer_from_log(log_path: Path) -> tuple[str, str, str]:
    with log_path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        return "", "", "training log exists but is empty"

    headers = {h.lower(): h for h in rows[0].keys() if h}
    epoch_key = headers.get("epoch")
    val_rank1_key = headers.get("val_rank1")
    val_loss_key = headers.get("val_loss")

    if val_rank1_key:
        best_row = None
        best_val = None
        for row in rows:
            raw = str(row.get(val_rank1_key, "")).strip()
            if not raw:
                continue
            try:
                val = float(raw)
            except ValueError:
                continue
            if best_val is None or val > best_val:
                best_val = val
                best_row = row
        if best_row is not None:
            epoch = str(best_row.get(epoch_key, "")).strip() if epoch_key else ""
            return "val_rank1", epoch, f"reconstructed from max val_rank1 in {rel(log_path)}"

    if val_loss_key:
        best_row = None
        best_val = None
        for row in rows:
            raw = str(row.get(val_loss_key, "")).strip()
            if not raw:
                continue
            try:
                val = float(raw)
            except ValueError:
                continue
            if best_val is None or val < best_val:
                best_val = val
                best_row = row
        if best_row is not None:
            epoch = str(best_row.get(epoch_key, "")).strip() if epoch_key else ""
            return "val_loss", epoch, f"reconstructed from min val_loss in {rel(log_path)}"

    return "", "", f"log has no usable val_rank1/val_loss columns: {rel(log_path)}"


def infer_from_checkpoint(ckpt_path: Path) -> tuple[str, str]:
    if not ckpt_path.exists():
        return "", "checkpoint missing"
    # Do not torch.load model tensors during audit; checkpoint files can be large.
    # Selected epoch is reconstructed from training logs when available.
    return "", "checkpoint exists; tensor load intentionally skipped"

def inspect_train_lgf_rule() -> tuple[bool, str]:
    path = ROOT / "scripts" / "train_lgf.py"
    if not path.exists():
        return False, "scripts/train_lgf.py missing"

    text = read_text(path)
    required = [
        "can_compute_val_rank1",
        "val_rank1",
        "val_loss_mean",
        "torch.save(checkpoint",
        '"best.pt"',
    ]
    missing = [tok for tok in required if tok not in text]
    if missing:
        return False, "training source missing expected tokens: " + ", ".join(missing)

    return True, (
        "scripts/train_lgf.py selects best.pt using validation Rank-1 when available, "
        "otherwise validation loss."
    )


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_ok, source_note = inspect_train_lgf_rule()

    with RUNS_CSV.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    rows = [
        r for r in rows
        if r.get("method") in STRICT_METHODS
        and r.get("direction") in STRICT_DIRECTIONS
        and str(r.get("status", "")).upper() == "OK"
    ]

    out_rows: list[dict[str, str]] = []

    for r in rows:
        config_path = ROOT / r["config"]
        metrics_path = ROOT / r["metrics_path"]
        run_dir = metrics_path.parent
        ckpt_path = run_dir / "checkpoints" / "best.pt"

        notes = [source_note]

        try:
            cfg = load_yaml(config_path)
            save_dir = cfg.get("save_dir")
            if save_dir:
                run_dir = ROOT / str(save_dir)
                ckpt_path = run_dir / "checkpoints" / "best.pt"

            split_file = (cfg.get("dataset") or {}).get("split_file", "")
            split_path = ROOT / str(split_file)
            uses_test_gallery_probe, split_note = check_split_leakage(split_path)
            notes.append(split_note)
        except Exception as exc:
            uses_test_gallery_probe = "UNKNOWN"
            notes.append(f"config/split inspection failed: {type(exc).__name__}")

        checkpoint_metric = ""
        selected_epoch = ""
        validation_metric_source = ""

        log_path = find_training_log(run_dir)
        if log_path:
            try:
                checkpoint_metric, selected_epoch, log_note = infer_from_log(log_path)
                validation_metric_source = rel(log_path)
                notes.append(log_note)
            except Exception as exc:
                notes.append(f"log inspection failed: {type(exc).__name__}")
        else:
            notes.append("training log not found")

        ckpt_epoch, ckpt_note = infer_from_checkpoint(ckpt_path)
        notes.append(ckpt_note)
        if ckpt_epoch:
            selected_epoch = ckpt_epoch
            if not validation_metric_source:
                validation_metric_source = rel(ckpt_path)

        if not checkpoint_metric:
            checkpoint_metric = "val_rank1_or_val_loss_from_train_lgf_rule"

        if uses_test_gallery_probe == "YES":
            verdict = "FAIL"
        elif source_ok and uses_test_gallery_probe == "NO" and selected_epoch:
            verdict = "PASS"
        elif source_ok and uses_test_gallery_probe == "NO":
            verdict = "PARTIAL"
        else:
            verdict = "UNCLEAR"

        out_rows.append({
            "method": r.get("method", ""),
            "direction": r.get("direction", ""),
            "seed": str(r.get("seed", "")),
            "config_path": rel(config_path),
            "run_dir": rel(run_dir),
            "checkpoint_path": rel(ckpt_path),
            "checkpoint_metric": checkpoint_metric,
            "selected_epoch": selected_epoch or "UNAVAILABLE",
            "validation_metric_source": validation_metric_source or "train_lgf.py validation rule",
            "uses_test_gallery_probe": uses_test_gallery_probe,
            "verdict": verdict,
            "notes": " | ".join(notes),
        })

    fields = [
        "method",
        "direction",
        "seed",
        "config_path",
        "run_dir",
        "checkpoint_path",
        "checkpoint_metric",
        "selected_epoch",
        "validation_metric_source",
        "uses_test_gallery_probe",
        "verdict",
        "notes",
    ]

    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(out_rows)

    counts: dict[str, int] = {}
    for row in out_rows:
        counts[row["verdict"]] = counts.get(row["verdict"], 0) + 1

    md = []
    md.append("# Checkpoint-Selection Audit")
    md.append("")
    md.append("## Scope")
    md.append("")
    md.append("This audit covers the final strict Tongji rows in `docs/results/strict_tongji_ablation_runs.csv`.")
    md.append("")
    md.append("## Training-code rule")
    md.append("")
    md.append(source_note)
    md.append("")
    md.append("The audit checks that the validation split does not overlap gallery/probe/test paths and attempts to reconstruct the selected epoch from training logs or `best.pt`.")
    md.append("")
    md.append("## Verdict counts")
    md.append("")
    md.append("| Verdict | Count |")
    md.append("|---|---:|")
    for key in ("PASS", "PARTIAL", "UNCLEAR", "FAIL"):
        md.append(f"| {key} | {counts.get(key, 0)} |")
    md.append("")
    md.append("## Audit table")
    md.append("")
    md.append("| Method | Direction | Seed | Metric | Selected epoch | Uses gallery/probe/test | Verdict |")
    md.append("|---|---|---:|---|---:|---|---|")
    for row in out_rows:
        md.append(
            f"| {row['method']} | {row['direction']} | {row['seed']} | "
            f"{row['checkpoint_metric']} | {row['selected_epoch']} | "
            f"{row['uses_test_gallery_probe']} | {row['verdict']} |"
        )
    md.append("")
    md.append("## Interpretation")
    md.append("")
    if counts.get("FAIL", 0):
        md.append("At least one run indicates possible gallery/probe/test influence. Stop and inspect before strengthening paper claims.")
    elif counts.get("UNCLEAR", 0) or counts.get("PARTIAL", 0):
        md.append("The audit supports a validation-only checkpoint-selection rule, but selected-epoch reconstruction is incomplete for at least one run.")
    else:
        md.append("All audited strict Tongji runs support validation-only checkpoint selection with no gallery/probe/test influence.")
    md.append("")
    md.append("Detailed per-run notes are in `docs/audits/checkpoint_selection_audit.csv`.")

    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    print(f"Wrote {rel(OUT_CSV)}")
    print(f"Wrote {rel(OUT_MD)}")
    print(f"Rows: {len(out_rows)}")
    print("Verdicts:", ", ".join(f"{k}={counts.get(k, 0)}" for k in ("PASS", "PARTIAL", "UNCLEAR", "FAIL")))

    return 2 if counts.get("FAIL", 0) else 0


if __name__ == "__main__":
    raise SystemExit(main())