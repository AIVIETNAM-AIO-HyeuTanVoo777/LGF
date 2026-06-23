from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(".")
SPLIT_DIR = ROOT / "data" / "splits"
MANIFEST_PATH = ROOT / "data" / "metadata" / "palm_segmented_manifest.csv"
OUT_DIR = ROOT / "docs" / "audits"

OUT_CSV = OUT_DIR / "rankb_protocol_audit.csv"
OUT_MD = OUT_DIR / "rankb_protocol_audit.md"
OUT_TEX = OUT_DIR / "rankb_protocol_audit_table.tex"

PARTITIONS = ("train", "val", "gallery", "probe")
DEV_PARTITIONS = ("train", "val")
TEST_PARTITIONS = ("gallery", "probe")

FIELDS = [
    "dataset",
    "protocol",
    "seed",
    "direction",
    "train_count",
    "val_count",
    "gallery_count",
    "probe_count",
    "dev_class_count",
    "test_class_count",
    "dev_subject_count",
    "test_subject_count",
    "image_overlap",
    "class_overlap",
    "palm_overlap",
    "subject_overlap",
    "person_overlap_status",
    "split_file",
    "split_sha256",
    "claim_allowed",
    "audit_status",
    "notes",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_split(path: Path) -> dict[str, list[dict[str, Any]]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    for key in PARTITIONS:
        if key not in data:
            raise ValueError(f"{path}: missing partition {key}")
        if not isinstance(data[key], list):
            raise TypeError(f"{path}: partition {key} is not a list")
    return data


def values(records: list[dict[str, Any]], key: str) -> set[str]:
    out: set[str] = set()
    for r in records:
        v = r.get(key)
        if v is None or v == "":
            continue
        out.add(str(v))
    return out


def collect(data: dict[str, list[dict[str, Any]]], parts: tuple[str, ...]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for p in parts:
        rows.extend(data.get(p, []))
    return rows


def infer_metadata_from_filename(path: Path) -> tuple[str, str, str, str]:
    name = path.name

    m = re.match(r"tongji_subject_disjoint_(s1_to_s2|s2_to_s1)_seed(\d+)\.json$", name, re.I)
    if m:
        direction_raw = m.group(1).lower()
        direction = "S1->S2" if direction_raw == "s1_to_s2" else "S2->S1"
        return "Tongji", "held-out cross-session", m.group(2), direction

    m = re.match(r"iitd_subject_disjoint_within_seed(\d+)\.json$", name, re.I)
    if m:
        return "IITD", "held-out within-session", m.group(1), "within-session"

    return "unknown", "unknown", "unknown", "unknown"


def audit_one(path: Path) -> dict[str, Any]:
    data = read_split(path)
    dataset, protocol, seed, direction = infer_metadata_from_filename(path)

    train = data["train"]
    val = data["val"]
    gallery = data["gallery"]
    probe = data["probe"]

    dev = collect(data, DEV_PARTITIONS)
    test = collect(data, TEST_PARTITIONS)

    dev_paths = values(dev, "path")
    test_paths = values(test, "path")
    dev_classes = values(dev, "class_id")
    test_classes = values(test, "class_id")
    dev_palms = values(dev, "palm_id")
    test_palms = values(test, "palm_id")
    dev_subjects = values(dev, "subject_id")
    test_subjects = values(test, "subject_id")

    image_overlap = len(dev_paths & test_paths)
    class_overlap = len(dev_classes & test_classes)
    palm_overlap = len(dev_palms & test_palms)
    subject_overlap = len(dev_subjects & test_subjects)

    # Conservative rank-B wording:
    # The manifest has subject_id, but this script does not independently verify
    # that subject_id is a human-level person identifier across datasets.
    # Therefore the audit claim is deliberately capped at palm-class-disjoint.
    person_overlap_status = "unavailable"

    invalid_reasons: list[str] = []
    if image_overlap:
        invalid_reasons.append("dev/test image overlap")
    if class_overlap:
        invalid_reasons.append("dev/test class overlap")
    if palm_overlap:
        invalid_reasons.append("dev/test palm overlap")
    if subject_overlap:
        invalid_reasons.append("dev/test subject_id overlap")

    if invalid_reasons:
        claim_allowed = "invalid"
        audit_status = "FAIL"
        notes = "; ".join(invalid_reasons)
    else:
        claim_allowed = "palm-class-disjoint"
        audit_status = "PASS"
        notes = (
            "No dev/test image, class, palm, or subject_id overlap. "
            "Claim is conservatively capped at palm-class-disjoint because no "
            "independent person-level identifier is verified by this audit."
        )

    return {
        "dataset": dataset,
        "protocol": protocol,
        "seed": seed,
        "direction": direction,
        "train_count": len(train),
        "val_count": len(val),
        "gallery_count": len(gallery),
        "probe_count": len(probe),
        "dev_class_count": len(dev_classes),
        "test_class_count": len(test_classes),
        "dev_subject_count": len(dev_subjects),
        "test_subject_count": len(test_subjects),
        "image_overlap": image_overlap,
        "class_overlap": class_overlap,
        "palm_overlap": palm_overlap,
        "subject_overlap": subject_overlap,
        "person_overlap_status": person_overlap_status,
        "split_file": path.name,
        "split_sha256": sha256_file(path),
        "claim_allowed": claim_allowed,
        "audit_status": audit_status,
        "notes": notes,
    }


def md_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = []
    lines.append("| " + " | ".join(fields) + " |")
    lines.append("| " + " | ".join(["---"] * len(fields)) + " |")
    for row in rows:
        vals = [str(row.get(f, "")).replace("|", "\\|") for f in fields]
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def tex_escape(s: Any) -> str:
    text = str(s)
    repl = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(repl.get(ch, ch) for ch in text)


def write_tex(rows: list[dict[str, Any]]) -> None:
    # Compact table intended for inclusion or manual copy into the paper.
    cols = [
        ("Dataset", "dataset"),
        ("Direction", "direction"),
        ("Seed", "seed"),
        ("Img ov.", "image_overlap"),
        ("Palm/class ov.", "palm_class_overlap"),
        ("Subj. ov.", "subject_overlap"),
        ("Split hash", "split_hash_short"),
        ("Claim", "claim_allowed"),
    ]

    lines = [
        r"\begin{table*}[t]",
        r"\centering",
        r"\caption{Protocol audit summary. Image, palm/class, and subject-id overlaps are measured between development (train+validation) and held-out test (gallery+probe) partitions. Split hashes identify the exact JSON split files.}",
        r"\label{tab:protocol_audit}",
        r"\footnotesize",
        r"\setlength{\tabcolsep}{3pt}",
        r"\begin{tabular}{llccclll}",
        r"\toprule",
        " & ".join(c[0] for c in cols) + r" \\",
        r"\midrule",
    ]

    for row in rows:
        compact = dict(row)
        compact["palm_class_overlap"] = f"{row['palm_overlap']}/{row['class_overlap']}"
        compact["split_hash_short"] = str(row["split_sha256"])[:12]
        lines.append(" & ".join(tex_escape(compact[k]) for _, k in cols) + r" \\")

    lines.extend(
        [
            r"\bottomrule",
            r"\end{tabular}",
            r"\end{table*}",
            "",
        ]
    )
    OUT_TEX.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    split_files = sorted(
        list(SPLIT_DIR.glob("tongji_subject_disjoint_s*_to_s*_seed*.json"))
        + list(SPLIT_DIR.glob("iitd_subject_disjoint_within_seed*.json"))
    )

    if not split_files:
        raise FileNotFoundError("No rank-B split files found.")

    if not MANIFEST_PATH.exists():
        raise FileNotFoundError(f"Manifest not found: {MANIFEST_PATH}")

    rows = [audit_one(p) for p in split_files]

    # Stable order for paper/debugging.
    direction_order = {"S1->S2": 0, "S2->S1": 1, "within-session": 2}
    rows.sort(
        key=lambda r: (
            r["dataset"],
            direction_order.get(r["direction"], 99),
            int(r["seed"]) if str(r["seed"]).isdigit() else 999999,
        )
    )

    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    md = [
        "# Rank-B Protocol Audit",
        "",
        "This audit measures overlap between development partitions (`train` + `val`) and held-out test partitions (`gallery` + `probe`).",
        "",
        "The `claim_allowed` field is deliberately conservative. It is capped at `palm-class-disjoint` unless independent person-level identity is verified.",
        "",
        md_table(rows, FIELDS),
        "",
    ]
    OUT_MD.write_text("\n".join(md), encoding="utf-8")

    write_tex(rows)

    n_fail = sum(1 for r in rows if r["audit_status"] != "PASS")
    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_TEX}")
    print(f"Rows: {len(rows)}")
    print(f"Failures: {n_fail}")
    if n_fail:
        raise SystemExit(1)


if __name__ == "__main__":
    main()