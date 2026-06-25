from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "metadata" / "palm_segmented_manifest.csv"
OUT_DIR = ROOT / "audit_artifacts" / "protocol"
OUT_CSV = OUT_DIR / "gallery_probe_audit.csv"
OUT_MD = OUT_DIR / "gallery_probe_audit.md"

SPLIT_FILES = [
    ("Tongji", "S1->S2", 42, "session1", "session2", ROOT / "data/splits/tongji_subject_disjoint_s1_to_s2_seed42.json"),
    ("Tongji", "S1->S2", 2026, "session1", "session2", ROOT / "data/splits/tongji_subject_disjoint_s1_to_s2_seed2026.json"),
    ("Tongji", "S1->S2", 2705, "session1", "session2", ROOT / "data/splits/tongji_subject_disjoint_s1_to_s2_seed2705.json"),
    ("Tongji", "S2->S1", 42, "session2", "session1", ROOT / "data/splits/tongji_subject_disjoint_s2_to_s1_seed42.json"),
    ("Tongji", "S2->S1", 2026, "session2", "session1", ROOT / "data/splits/tongji_subject_disjoint_s2_to_s1_seed2026.json"),
    ("Tongji", "S2->S1", 2705, "session2", "session1", ROOT / "data/splits/tongji_subject_disjoint_s2_to_s1_seed2705.json"),
    ("IITD", "within-session", 42, "session1", "session1", ROOT / "data/splits/iitd_subject_disjoint_within_seed42.json"),
    ("IITD", "within-session", 2026, "session1", "session1", ROOT / "data/splits/iitd_subject_disjoint_within_seed2026.json"),
    ("IITD", "within-session", 2705, "session1", "session1", ROOT / "data/splits/iitd_subject_disjoint_within_seed2705.json"),
]


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except Exception:
        return path.as_posix()


def norm_path(x: Any) -> str:
    return str(x).replace("\\", "/").strip()


def load_split(path: Path) -> dict[str, list[Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    out = {}
    for key in ["train", "val", "gallery", "probe", "support"]:
        val = data.get(key, [])
        if val is None:
            val = []
        if not isinstance(val, list):
            raise ValueError(f"{path}: `{key}` is not a list")
        out[key] = val
    return out


def item_path(item: Any) -> str:
    if isinstance(item, dict):
        for key in ["path", "image_path", "filepath", "file_path", "filename", "file"]:
            if key in item:
                return norm_path(item[key])
    if isinstance(item, str):
        return norm_path(item)
    raise ValueError(f"Cannot infer path from split item: {item!r}")


def rows_for_items(df_by_path: dict[str, dict[str, Any]], items: list[Any]) -> tuple[list[dict[str, Any]], list[str]]:
    rows = []
    unresolved = []
    for item in items:
        p = item_path(item)
        row = df_by_path.get(p)
        if row is None:
            unresolved.append(p)
        else:
            rows.append(row)
    return rows, unresolved


def values(rows: list[dict[str, Any]], col: str) -> set[str]:
    return {str(r[col]) for r in rows if col in r and pd.notna(r[col])}


def counts(rows: list[dict[str, Any]], col: str) -> str:
    vals = sorted(values(rows, col))
    return ",".join(vals)


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(MANIFEST)
    required = ["path", "dataset", "session", "hand", "subject_id", "palm_id", "class_id", "sample_id"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise SystemExit(f"Missing manifest columns: {missing}")

    df = df.copy()
    df["path_norm"] = df["path"].map(norm_path)
    df_by_path = {str(r["path_norm"]): r.to_dict() for _, r in df.iterrows()}

    out_rows: list[dict[str, Any]] = []

    for dataset, direction, seed, expected_gallery_session, expected_probe_session, split_path in SPLIT_FILES:
        split = load_split(split_path)
        gallery_rows, gallery_unresolved = rows_for_items(df_by_path, split["gallery"])
        probe_rows, probe_unresolved = rows_for_items(df_by_path, split["probe"])

        gallery_paths = values(gallery_rows, "path_norm")
        probe_paths = values(probe_rows, "path_norm")
        gallery_classes = values(gallery_rows, "class_id")
        probe_classes = values(probe_rows, "class_id")
        gallery_palms = values(gallery_rows, "palm_id")
        probe_palms = values(probe_rows, "palm_id")
        gallery_subjects = values(gallery_rows, "subject_id")
        probe_subjects = values(probe_rows, "subject_id")
        gallery_sessions = values(gallery_rows, "session")
        probe_sessions = values(probe_rows, "session")

        image_overlap = len(gallery_paths & probe_paths)
        class_intersection = len(gallery_classes & probe_classes)
        class_symmetric_diff = len(gallery_classes ^ probe_classes)
        palm_intersection = len(gallery_palms & probe_palms)
        palm_symmetric_diff = len(gallery_palms ^ probe_palms)
        subject_intersection = len(gallery_subjects & probe_subjects)
        subject_symmetric_diff = len(gallery_subjects ^ probe_subjects)

        unresolved_total = len(gallery_unresolved) + len(probe_unresolved)

        reasons = []
        if unresolved_total:
            reasons.append(f"unresolved gallery/probe items: {unresolved_total}")
        if not gallery_rows or not probe_rows:
            reasons.append("empty gallery or probe")
        if image_overlap != 0:
            reasons.append(f"gallery/probe image overlap={image_overlap}")
        if class_symmetric_diff != 0:
            reasons.append(f"gallery/probe class mismatch symmetric_diff={class_symmetric_diff}")
        if palm_symmetric_diff != 0:
            reasons.append(f"gallery/probe palm mismatch symmetric_diff={palm_symmetric_diff}")
        if subject_symmetric_diff != 0:
            reasons.append(f"gallery/probe subject-id mismatch symmetric_diff={subject_symmetric_diff}")
        if gallery_sessions != {expected_gallery_session}:
            reasons.append(f"gallery sessions {sorted(gallery_sessions)} != expected {expected_gallery_session}")
        if probe_sessions != {expected_probe_session}:
            reasons.append(f"probe sessions {sorted(probe_sessions)} != expected {expected_probe_session}")

        verdict = "PASS" if not reasons else "FAIL"

        out_rows.append({
            "dataset": dataset,
            "direction": direction,
            "seed": seed,
            "split_file": rel(split_path),
            "gallery_images": len(gallery_rows),
            "probe_images": len(probe_rows),
            "gallery_classes": len(gallery_classes),
            "probe_classes": len(probe_classes),
            "gallery_probe_class_intersection": class_intersection,
            "gallery_probe_class_symmetric_diff": class_symmetric_diff,
            "gallery_probe_palm_intersection": palm_intersection,
            "gallery_probe_palm_symmetric_diff": palm_symmetric_diff,
            "gallery_probe_subject_intersection": subject_intersection,
            "gallery_probe_subject_symmetric_diff": subject_symmetric_diff,
            "gallery_probe_image_overlap": image_overlap,
            "gallery_sessions": counts(gallery_rows, "session"),
            "probe_sessions": counts(probe_rows, "session"),
            "expected_gallery_session": expected_gallery_session,
            "expected_probe_session": expected_probe_session,
            "cross_session_status": "cross-session" if dataset == "Tongji" else "within-session-only",
            "verdict": verdict,
            "notes": " | ".join(reasons) if reasons else "Gallery/probe class/palm/subject sets match, images are disjoint, and sessions match expected protocol direction.",
        })

    fields = [
        "dataset", "direction", "seed", "split_file",
        "gallery_images", "probe_images", "gallery_classes", "probe_classes",
        "gallery_probe_class_intersection", "gallery_probe_class_symmetric_diff",
        "gallery_probe_palm_intersection", "gallery_probe_palm_symmetric_diff",
        "gallery_probe_subject_intersection", "gallery_probe_subject_symmetric_diff",
        "gallery_probe_image_overlap",
        "gallery_sessions", "probe_sessions",
        "expected_gallery_session", "expected_probe_session",
        "cross_session_status", "verdict", "notes",
    ]

    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(out_rows)

    counts_by_verdict: dict[str, int] = {}
    for r in out_rows:
        counts_by_verdict[r["verdict"]] = counts_by_verdict.get(r["verdict"], 0) + 1

    md: list[str] = []
    md.append("# Gallery/Probe Construction Audit")
    md.append("")
    md.append("## Scope")
    md.append("")
    md.append("This audit verifies that final gallery/probe partitions are constructed as closed-set enrollment/probe splits over the same held-out palm classes, with no image overlap and with the expected session direction.")
    md.append("")
    md.append("## Evaluation-code evidence")
    md.append("")
    md.append("The evaluation script loads `gallery` and `probe` partitions separately, extracts embeddings, computes a probe-by-gallery cosine similarity matrix, uses class-label equality for Rank-k matching, and derives EER/TAR from genuine/impostor probe-gallery pairs.")
    md.append("")
    md.append("## Verdict counts")
    md.append("")
    md.append("| Verdict | Count |")
    md.append("|---|---:|")
    for key in ["PASS", "FAIL"]:
        md.append(f"| {key} | {counts_by_verdict.get(key, 0)} |")
    md.append("")
    md.append("## Split-level audit")
    md.append("")
    md.append("| Dataset | Direction | Seed | Gallery images | Probe images | Gallery classes | Probe classes | Image overlap | Gallery sessions | Probe sessions | Status | Verdict |")
    md.append("|---|---|---:|---:|---:|---:|---:|---:|---|---|---|---|")
    for r in out_rows:
        md.append(
            f"| {r['dataset']} | {r['direction']} | {r['seed']} | "
            f"{r['gallery_images']} | {r['probe_images']} | "
            f"{r['gallery_classes']} | {r['probe_classes']} | "
            f"{r['gallery_probe_image_overlap']} | {r['gallery_sessions']} | {r['probe_sessions']} | "
            f"{r['cross_session_status']} | {r['verdict']} |"
        )
    md.append("")
    md.append("## Interpretation")
    md.append("")
    if any(r["verdict"] != "PASS" for r in out_rows):
        md.append("At least one gallery/probe split failed the audit. Do not strengthen evaluation claims until corrected.")
    else:
        md.append("All audited splits use matching gallery/probe palm-class sets with disjoint images. Tongji splits are cross-session in the intended direction; IITD is within-session only and must remain secondary validation rather than cross-session evidence.")
    md.append("")
    md.append(f"Detailed machine-readable rows are stored in `{rel(OUT_CSV)}`.")

    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    print(f"Wrote {rel(OUT_CSV)}")
    print(f"Wrote {rel(OUT_MD)}")
    print(f"Rows: {len(out_rows)}")
    print("Verdicts:", ", ".join(f"{k}={counts_by_verdict.get(k, 0)}" for k in ["PASS", "FAIL"]))
    return 1 if counts_by_verdict.get("FAIL", 0) else 0


if __name__ == "__main__":
    raise SystemExit(main())
