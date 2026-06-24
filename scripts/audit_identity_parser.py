from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "metadata" / "palm_segmented_manifest.csv"
OUT_DIR = ROOT / "docs" / "audits"
OUT_CSV = OUT_DIR / "identity_parser_audit.csv"
OUT_MD = OUT_DIR / "identity_parser_audit.md"

SPLIT_FILES = [
    ("Tongji", "S1->S2", 42, ROOT / "data/splits/tongji_subject_disjoint_s1_to_s2_seed42.json"),
    ("Tongji", "S1->S2", 2026, ROOT / "data/splits/tongji_subject_disjoint_s1_to_s2_seed2026.json"),
    ("Tongji", "S1->S2", 2705, ROOT / "data/splits/tongji_subject_disjoint_s1_to_s2_seed2705.json"),
    ("Tongji", "S2->S1", 42, ROOT / "data/splits/tongji_subject_disjoint_s2_to_s1_seed42.json"),
    ("Tongji", "S2->S1", 2026, ROOT / "data/splits/tongji_subject_disjoint_s2_to_s1_seed2026.json"),
    ("Tongji", "S2->S1", 2705, ROOT / "data/splits/tongji_subject_disjoint_s2_to_s1_seed2705.json"),
    ("IITD", "within-session", 42, ROOT / "data/splits/iitd_subject_disjoint_within_seed42.json"),
    ("IITD", "within-session", 2026, ROOT / "data/splits/iitd_subject_disjoint_within_seed2026.json"),
    ("IITD", "within-session", 2705, ROOT / "data/splits/iitd_subject_disjoint_within_seed2705.json"),
]


def rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except Exception:
        return path.as_posix()


def norm_path(x: Any) -> str:
    return str(x).replace("\\", "/").strip()


def load_split(path: Path) -> dict[str, list[dict[str, Any]]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    out: dict[str, list[dict[str, Any]]] = {}
    for key in ["train", "val", "gallery", "probe", "support"]:
        value = data.get(key, [])
        if value is None:
            value = []
        if not isinstance(value, list):
            raise ValueError(f"{path}: split key `{key}` is not a list")
        out[key] = value
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


def sample_paths(df: pd.DataFrame, dataset: str, n: int = 3) -> list[str]:
    return [norm_path(x) for x in df[df["dataset"] == dataset]["path"].head(n).tolist()]


def infer_path_pattern(paths: list[str]) -> str:
    if not paths:
        return "UNAVAILABLE"
    parts = []
    for p in paths:
        base = p.split("/")[-1]
        base = re.sub(r"\d+", "<num>", base)
        parts.append(base)
    uniq = sorted(set(parts))
    return "; ".join(uniq[:3])


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

    rows_out: list[dict[str, Any]] = []

    for dataset, direction, seed, split_path in SPLIT_FILES:
        split = load_split(split_path)
        dev_items = split["train"] + split["val"]
        test_items = split["gallery"] + split["probe"] + split["support"]

        dev_rows, dev_unresolved = rows_for_items(df_by_path, dev_items)
        test_rows, test_unresolved = rows_for_items(df_by_path, test_items)

        dev_paths = values(dev_rows, "path_norm")
        test_paths = values(test_rows, "path_norm")
        dev_classes = values(dev_rows, "class_id")
        test_classes = values(test_rows, "class_id")
        dev_palms = values(dev_rows, "palm_id")
        test_palms = values(test_rows, "palm_id")
        dev_subjects = values(dev_rows, "subject_id")
        test_subjects = values(test_rows, "subject_id")

        image_overlap = len(dev_paths & test_paths)
        class_overlap = len(dev_classes & test_classes)
        palm_overlap = len(dev_palms & test_palms)
        subject_overlap = len(dev_subjects & test_subjects)

        unresolved_total = len(dev_unresolved) + len(test_unresolved)

        if unresolved_total:
            verdict = "FAIL"
            notes = f"unresolved split items: dev={len(dev_unresolved)}, test={len(test_unresolved)}"
        elif image_overlap or class_overlap or palm_overlap or subject_overlap:
            verdict = "FAIL"
            notes = "development/test overlap detected"
        else:
            verdict = "PASS"
            notes = (
                "No development/test image, class_id, palm_id, or subject_id overlap. "
                "Claim remains capped at palm-class-disjoint because no independent person-level identifier is verified."
            )

        rows_out.append({
            "dataset": dataset,
            "direction": direction,
            "seed": seed,
            "split_file": rel(split_path),
            "dev_images": len(dev_rows),
            "test_images": len(test_rows),
            "dev_palm_classes": len(dev_classes),
            "test_palm_classes": len(test_classes),
            "dev_palms": len(dev_palms),
            "test_palms": len(test_palms),
            "dev_subjects": len(dev_subjects),
            "test_subjects": len(test_subjects),
            "image_overlap": image_overlap,
            "palm_class_overlap": class_overlap,
            "palm_overlap": palm_overlap,
            "subject_overlap": subject_overlap,
            "person_overlap_status": "unavailable",
            "claim_allowed": "palm-class-disjoint",
            "verdict": verdict,
            "notes": notes,
        })

    fields = [
        "dataset", "direction", "seed", "split_file",
        "dev_images", "test_images",
        "dev_palm_classes", "test_palm_classes",
        "dev_palms", "test_palms", "dev_subjects", "test_subjects",
        "image_overlap", "palm_class_overlap", "palm_overlap", "subject_overlap",
        "person_overlap_status", "claim_allowed", "verdict", "notes",
    ]

    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows_out)

    counts = df.groupby(["dataset", "session"]).size().reset_index(name="images")
    uniques = df.groupby("dataset")[["subject_id", "palm_id", "class_id"]].nunique()

    md: list[str] = []
    md.append("# Identity and Palm-Class Parser Audit")
    md.append("")
    md.append("## Scope")
    md.append("")
    md.append("This audit documents the manifest fields used as image, session, hand, subject, palm, and class identifiers, then verifies development/test overlap for the final Tongji and IITD split files.")
    md.append("")
    md.append("## Manifest")
    md.append("")
    md.append(f"- Source manifest: `{rel(MANIFEST)}`")
    md.append(f"- Columns: `{', '.join(df.columns.drop('path_norm'))}`")
    md.append(f"- Total rows: {len(df)}")
    md.append("")
    md.append("### Counts by dataset/session")
    md.append("")
    md.append("| Dataset | Session | Images |")
    md.append("|---|---|---:|")
    for _, r in counts.iterrows():
        md.append(f"| {r['dataset']} | {r['session']} | {int(r['images'])} |")
    md.append("")
    md.append("### Unique identifiers by dataset")
    md.append("")
    md.append("| Dataset | subject_id | palm_id | class_id |")
    md.append("|---|---:|---:|---:|")
    for dataset, r in uniques.iterrows():
        md.append(f"| {dataset} | {int(r['subject_id'])} | {int(r['palm_id'])} | {int(r['class_id'])} |")
    md.append("")
    md.append("## Parser field semantics")
    md.append("")
    for dataset in ["Tongji", "IITD"]:
        paths = sample_paths(df, dataset)
        md.append(f"### {dataset} parser")
        md.append("")
        md.append(f"- Source manifest: `{rel(MANIFEST)}`")
        md.append(f"- Path examples: `{'; '.join(paths)}`")
        md.append(f"- Filename pattern examples: `{infer_path_pattern(paths)}`")
        md.append("- `subject_id`: manifest field used for subject-ID overlap audit, but not treated as independently verified person-level identity.")
        md.append("- `palm_id`: manifest field used as palm identifier.")
        md.append("- `class_id`: manifest field used as palm-class label for training/evaluation split construction.")
        md.append("- `session`: manifest field used for session assignment.")
        md.append("- `hand`: manifest field used for left/right-hand metadata.")
        md.append("- Left/right handling: left and right palms are represented as separate palm/classes through `palm_id` and `class_id`; the final paper claim is capped at palm-class-disjoint.")
        md.append("")

    md.append("## Split-level overlap audit")
    md.append("")
    md.append("| Dataset | Direction | Seed | Dev classes | Test classes | Image overlap | Class overlap | Palm overlap | Subject-ID overlap | Verdict |")
    md.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---|")
    for r in rows_out:
        md.append(
            f"| {r['dataset']} | {r['direction']} | {r['seed']} | "
            f"{r['dev_palm_classes']} | {r['test_palm_classes']} | "
            f"{r['image_overlap']} | {r['palm_class_overlap']} | {r['palm_overlap']} | {r['subject_overlap']} | {r['verdict']} |"
        )
    md.append("")
    md.append("## Interpretation")
    md.append("")
    if any(r["verdict"] != "PASS" for r in rows_out):
        md.append("At least one split failed the parser/overlap audit. Do not strengthen paper claims until the split is corrected.")
    else:
        md.append("All audited splits have zero development/test image, class_id, palm_id, and subject_id overlap. Because no independent person-level identifier is verified by this audit, the paper should continue to use the conservative term `palm-class-disjoint` rather than `person-disjoint`.")
    md.append("")
    md.append(f"Detailed machine-readable rows are stored in `{rel(OUT_CSV)}`.")

    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    verdict_counts: dict[str, int] = {}
    for r in rows_out:
        verdict_counts[r["verdict"]] = verdict_counts.get(r["verdict"], 0) + 1

    print(f"Wrote {rel(OUT_CSV)}")
    print(f"Wrote {rel(OUT_MD)}")
    print(f"Rows: {len(rows_out)}")
    print("Verdicts:", ", ".join(f"{k}={verdict_counts.get(k, 0)}" for k in ["PASS", "FAIL"]))
    return 1 if verdict_counts.get("FAIL", 0) else 0


if __name__ == "__main__":
    raise SystemExit(main())