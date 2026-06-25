from __future__ import annotations

import argparse
import glob
import os
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a Tongji/IITD segmented-image manifest.")
    parser.add_argument("--segmented-root", default="data/segmented", help="Root containing Tongji/ and IITD/ folders.")
    parser.add_argument("--output", default="data/metadata/palm_segmented_manifest.csv", help="Output manifest CSV.")
    return parser.parse_args()


def rel(path: str) -> str:
    return os.path.relpath(path).replace("\\", "/")


def iitd_records(root: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for file_path in sorted(glob.glob(str(root / "IITD" / "*" / "*.bmp"))):
        rel_path = rel(file_path)
        parts = rel_path.split("/")
        hand = parts[-2]
        stem = Path(file_path).stem
        bits = stem.split("_")
        if len(bits) < 2:
            continue
        subject_id = bits[0]
        palm_id = f"IITD_{hand}_{subject_id}"
        rows.append({
            "path": rel_path,
            "dataset": "IITD",
            "session": "session1",
            "hand": hand,
            "subject_id": subject_id,
            "palm_id": palm_id,
            "sample_id": f"IITD_session1_{hand}_{stem}",
        })
    return rows


def tongji_records(root: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for file_path in sorted(glob.glob(str(root / "Tongji" / "*" / "*.bmp"))):
        rel_path = rel(file_path)
        parts = rel_path.split("/")
        session = parts[-2]
        stem = Path(file_path).stem
        try:
            value = int(stem)
        except ValueError:
            continue
        palm_idx = (value - 1) // 10 + 1
        subject_id = f"{palm_idx:05d}"
        palm_id = f"Tongji_{subject_id}"
        rows.append({
            "path": rel_path,
            "dataset": "Tongji",
            "session": session,
            "hand": "none",
            "subject_id": subject_id,
            "palm_id": palm_id,
            "sample_id": f"Tongji_{session}_none_{stem}",
        })
    return rows


def main() -> int:
    args = parse_args()
    root = Path(args.segmented_root)
    rows = iitd_records(root) + tongji_records(root)
    if not rows:
        raise SystemExit(f"No .bmp records found under {root}. Obtain datasets from official sources first.")

    df = pd.DataFrame(rows)
    palm_to_class = {palm: idx for idx, palm in enumerate(sorted(df["palm_id"].unique()))}
    df["class_id"] = df["palm_id"].map(palm_to_class)
    df = df[["path", "dataset", "session", "hand", "subject_id", "palm_id", "class_id", "sample_id"]]

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    print(f"Wrote {out} rows={len(df)}")
    print(df.groupby("dataset").size().to_string())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
