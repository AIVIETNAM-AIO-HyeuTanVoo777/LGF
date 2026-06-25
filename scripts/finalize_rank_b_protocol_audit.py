#!/usr/bin/env python3
"""
Finalize Rank-B split audit for PALM_CGK_BASE.

This script audits the palm-class-disjoint split manifests of Tongji and IITD datasets.
It ensures that:
1. Development (train ∪ val) and Test (gallery ∪ probe ∪ support) are disjoint by the manifest identity field used for palm-class protocol construction.
2. All items in the splits are successfully resolved against the manifest (unresolved_items == 0).
3. Gallery and probe have subject overlap when both are non-empty (to enable identification evaluation).
4. Subject overlap between train and validation is allowed and reported.

Usage:
  python scripts/finalize_rank_b_protocol_audit.py --write
"""

from __future__ import annotations

import argparse
import glob
import hashlib
import json
from pathlib import Path
import pandas as pd


def calculate_sha256(filepath: Path) -> str:
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def normalize_path(p: str) -> str:
    return str(Path(p)).replace("\\", "/")


def item_path(x: str | dict) -> str | None:
    if isinstance(x, str):
        return x.replace("\\", "/")
    if isinstance(x, dict):
        for k in ["path", "image_path", "filepath", "file"]:
            if k in x:
                return str(x[k]).replace("\\", "/")
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Finalize Rank-B Protocol Audit")
    parser.add_argument("--write", action="store_true", help="Write final split verdict md file")
    args = parser.parse_args()

    manifest_path = Path("data/metadata/palm_segmented_manifest.csv")
    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")

    # Read manifest and verify required columns
    df = pd.read_csv(manifest_path)
    required_cols = ["path", "dataset", "session", "subject_id"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Required manifest column '{col}' is missing. Existing columns: {df.columns.tolist()}")

    df["norm_path"] = df["path"].apply(normalize_path)
    path_to_row = {row["norm_path"]: row for _, row in df.iterrows()}

    # Find split files matching patterns
    tongji_files = sorted(glob.glob("data/splits/tongji_subject_disjoint_s*_to_s*_seed*.json"))
    iitd_files = sorted(glob.glob("data/splits/iitd_subject_disjoint_within_seed*.json"))
    split_files_paths = sorted([Path(p) for p in tongji_files + iitd_files])

    if not split_files_paths:
        print("No split files found matching the patterns.")
        return

    results = []
    keys = ["train", "val", "gallery", "probe", "support"]

    for sf in split_files_paths:
        sha = calculate_sha256(sf)
        with open(sf, "r", encoding="utf-8") as f:
            split_data = json.load(f)

        item_counts = {}
        subject_sets = {}
        session_counts = {}
        unresolved_counts = {}
        total_unresolved = 0

        for k in keys:
            items = split_data.get(k, [])
            item_counts[k] = len(items)

            subjects = set()
            sessions = {}
            unresolved = 0

            for item in items:
                p = item_path(item)
                if p is None:
                    unresolved += 1
                    continue
                np = normalize_path(p)
                if np in path_to_row:
                    row = path_to_row[np]
                    sub_id = str(row["subject_id"])
                    subjects.add(sub_id)

                    sess = str(row["session"])
                    sessions[sess] = sessions.get(sess, 0) + 1
                else:
                    unresolved += 1

            subject_sets[k] = subjects
            session_counts[k] = sessions
            unresolved_counts[k] = unresolved
            total_unresolved += unresolved

        # Compute overlap metrics
        S_train = subject_sets["train"]
        S_val = subject_sets["val"]
        S_gallery = subject_sets["gallery"]
        S_probe = subject_sets["probe"]
        S_support = subject_sets["support"]

        train_val_overlap = len(S_train.intersection(S_val))
        S_dev = S_train.union(S_val)
        S_test = S_gallery.union(S_probe).union(S_support)
        dev_test_overlap = len(S_dev.intersection(S_test))
        gallery_probe_overlap = len(S_gallery.intersection(S_probe))

        # Check conditions
        cond_dev_test = (dev_test_overlap == 0)
        cond_unresolved = (total_unresolved == 0)

        gallery_non_empty = (item_counts["gallery"] > 0)
        probe_non_empty = (item_counts["probe"] > 0)
        if gallery_non_empty and probe_non_empty:
            cond_gal_probe = (gallery_probe_overlap > 0)
        else:
            cond_gal_probe = True

        is_pass = cond_dev_test and cond_unresolved and cond_gal_probe
        verdict = "PASS_DEVELOPMENT_TEST_SUBJECT_DISJOINT" if is_pass else "FAIL"

        results.append({
            "filename": sf.name,
            "path": str(sf),
            "sha256": sha,
            "item_counts": item_counts,
            "subject_counts": {k: len(subject_sets[k]) for k in keys},
            "session_counts": session_counts,
            "unresolved_counts": unresolved_counts,
            "total_unresolved": total_unresolved,
            "train_val_subject_overlap": train_val_overlap,
            "development_test_subject_overlap": dev_test_overlap,
            "gallery_probe_subject_overlap": gallery_probe_overlap,
            "verdict": verdict,
            "dataset": "Tongji" if "tongji" in sf.name.lower() else "IITD"
        })

    # Print summary to stdout
    print("\n" + "=" * 80)
    print("RANK-B PROTOCOL AUDIT SUMMARY")
    print("=" * 80)
    for r in results:
        print(f"File: {r['filename']}")
        print(f"  Dataset: {r['dataset']}")
        print(f"  Verdict: {r['verdict']}")
        print(f"  Unresolved Items: {r['total_unresolved']}")
        print(f"  Train-Val Subject Overlap: {r['train_val_subject_overlap']}")
        print(f"  Dev-Test Subject Overlap: {r['development_test_subject_overlap']}")
        print(f"  Gallery-Probe Subject Overlap: {r['gallery_probe_subject_overlap']}")
        print("-" * 80)

    if args.write:
        # Build markdown report
        md = []
        md.append("# Rank-B Final Split Protocol Audit & Verdict")
        md.append("")
        md.append("## Protocol Overview & Scope")
        md.append("")
        md.append("### Paper Terminology & Definitions")
        md.append("")
        md.append("> [!IMPORTANT]")
        md.append("> **Tongji Protocol (Primary)**: We use a development/test palm-class-disjoint protocol. Training and validation images are drawn from development subjects, while gallery and probe images are drawn from held-out test palm classes. No subject appears in both the development set and the gallery/probe evaluation set.")
        md.append("> ")
        md.append("> **IITD Protocol (Secondary)**: IITD is used as a secondary palm-class-disjoint within-dataset validation. Because session metadata is not used to define a cross-session split, IITD is not treated as cross-session evidence.")
        md.append("")
        md.append("### Train/Val Subject Overlap Justification")
        md.append("In the development phase, train and validation sets are both parts of the development set (development = train ∪ val). Since validation is used to tune hyperparameters during development rather than serving as the final test evaluation, manifest-field overlap between train and validation is allowed and does not constitute data leakage. The critical boundary is between development and test (gallery ∪ probe ∪ support). This audit enforces strict subject disjointness between the development set and the test set.")
        md.append("")
        md.append("## Dataset Manifest Summary")
        md.append("")
        md.append(f"- **Manifest path**: `{manifest_path.as_posix()}`")
        md.append(f"- **Total manifest rows**: {len(df)}")
        md.append("- **Rows by dataset**:")
        for ds, count in df["dataset"].value_counts().items():
            md.append(f"  - `{ds}`: {count}")
        md.append("")
        md.append("## Audit Verdict Summary")
        md.append("")
        md.append("| Split File | Dataset | Total Items | Unresolved | Train-Val Overlap | Dev-Test Overlap | Gallery-Probe Overlap | Verdict |")
        md.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
        for r in results:
            tot_items = sum(r["item_counts"].values())
            md.append(
                f"| `{r['filename']}` | {r['dataset']} | {tot_items} | {r['total_unresolved']} | {r['train_val_subject_overlap']} | {r['development_test_subject_overlap']} | {r['gallery_probe_subject_overlap']} | `{r['verdict']}` |"
            )
        md.append("")
        md.append("## Detailed File Audits")
        md.append("")

        for r in results:
            md.append(f"### `{r['filename']}`")
            md.append("")
            md.append(f"- **SHA256**: `{r['sha256']}`")
            md.append(f"- **Dataset**: {r['dataset']}")
            md.append("- **Split Item Counts**:")
            for k in keys:
                md.append(f"  - {k}: {r['item_counts'][k]}")
            md.append("- **Unique Subject Counts**:")
            for k in keys:
                md.append(f"  - {k}: {r['subject_counts'][k]}")
            md.append("- **Session Counts**:")
            for k in keys:
                md.append(f"  - {k}: `{r['session_counts'][k]}`")
            md.append("- **Resolution Diagnostics**:")
            for k in keys:
                md.append(f"  - {k}: unresolved_items={r['unresolved_counts'][k]}")
            md.append("- **Overlap Checks**:")
            md.append(f"  - Train ∩ Val Subject Overlap: {r['train_val_subject_overlap']}")
            md.append(f"  - Dev ∩ Test Subject Overlap: {r['development_test_subject_overlap']}")
            md.append(f"  - Gallery ∩ Probe Subject Overlap: {r['gallery_probe_subject_overlap']}")
            md.append(f"- **VERDICT**: `{r['verdict']}`")
            md.append("")

        output_path = Path("docs/results/rank_b_final_split_verdict.md")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("\n".join(md), encoding="utf-8")
        print(f"Wrote final split verdict report to {output_path}")


if __name__ == "__main__":
    main()
