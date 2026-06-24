#!/usr/bin/env python3
"""
Generate candidate Tongji/IITD disjoint-identity split JSON files.

Run from repo root, after auditing the existing split schema:

    python scripts/make_tongji_iitd_disjoint_splits.py
    python scripts/make_tongji_iitd_disjoint_splits.py --write

Important:
- This script preserves simple split formats: index lists, path lists, or record dictionaries.
- If the existing repo uses a more complex split schema, adapt this script before using final splits.
- Use `subject_disjoint` only when a reliable subject_id column is used.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any

import pandas as pd

SEEDS = [42, 2026, 2705]

DATASET_COLS = ["dataset", "source", "db", "database", "dataset_name"]
IDENTITY_COLS_STRICT = ["subject_id", "subject", "person_id", "identity", "identity_id"]
IDENTITY_COLS_FALLBACK = ["palm_id", "class_id", "label", "target", "id"]
SESSION_COLS = ["session", "session_id", "sess", "capture_session"]
PATH_COLS = ["image_path", "path", "filepath", "file_path", "img_path", "filename"]


def infer_col(df: pd.DataFrame, candidates: list[str]) -> str | None:
    lower = {c.lower(): c for c in df.columns}
    for c in candidates:
        if c.lower() in lower:
            return lower[c.lower()]
    return None


def normalize_dataset_value(x: Any) -> str:
    return str(x).strip().lower().replace("-", "_").replace(" ", "_")


def normalize_session_value(x: Any) -> str:
    s = str(x).strip().lower()
    if s in {"1", "s1", "session1", "session_1", "session 1"}:
        return "s1"
    if s in {"2", "s2", "session2", "session_2", "session 2"}:
        return "s2"
    return s


def load_template_mode(template_path: Path | None) -> tuple[str, list[str] | None]:
    if not template_path or not template_path.exists():
        return "records", None
    obj = json.loads(template_path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        return "records", None
    for key in ["train", "val", "gallery", "probe", "support"]:
        items = obj.get(key)
        if isinstance(items, list) and items:
            sample = items[0]
            if isinstance(sample, int):
                return "indices", None
            if isinstance(sample, str):
                return "paths", None
            if isinstance(sample, dict):
                return "records", list(sample.keys())
    return "records", None


def materialize(df: pd.DataFrame, indices: list[int], mode: str, path_col: str | None, record_fields: list[str] | None) -> list[Any]:
    if mode == "indices":
        return [int(i) for i in indices]
    if mode == "paths":
        if not path_col:
            raise ValueError("Existing split appears path-based, but no image path column was inferred.")
        return [str(df.loc[i, path_col]) for i in indices]
    # record dictionaries
    if record_fields:
        fields = [f for f in record_fields if f in df.columns]
        if fields:
            return df.loc[indices, fields].to_dict(orient="records")
    return df.loc[indices].to_dict(orient="records")


def split_ids(ids: list[Any], seed: int, train_ratio: float = 0.8) -> tuple[set[Any], set[Any]]:
    ids = list(ids)
    rng = random.Random(seed)
    rng.shuffle(ids)
    n_train = int(round(len(ids) * train_ratio))
    train_ids = set(ids[:n_train])
    test_ids = set(ids[n_train:])
    if not train_ids or not test_ids:
        raise ValueError("Identity split produced an empty train or test set.")
    return train_ids, test_ids


def half_split(indices: list[int], seed: int, val_ratio: float = 0.2) -> tuple[list[int], list[int]]:
    indices = list(indices)
    rng = random.Random(seed)
    rng.shuffle(indices)
    n_val = max(1, int(round(len(indices) * val_ratio))) if len(indices) > 1 else 0
    val = indices[:n_val]
    train = indices[n_val:]
    return train, val


def indices_for(df: pd.DataFrame, mask) -> list[int]:
    return [int(i) for i in df.index[mask].tolist()]


def make_tongji_splits(
    df: pd.DataFrame,
    dataset_col: str,
    identity_col: str,
    identity_name: str,
    session_col: str,
    path_col: str | None,
    out_dir: Path,
    template_path: Path | None,
    write: bool,
    force: bool,
) -> list[str]:
    mode, record_fields = load_template_mode(template_path)
    dataset_norm = df[dataset_col].map(normalize_dataset_value)
    tongji = df[dataset_norm.str.contains("tongji", na=False)].copy()
    if tongji.empty:
        raise ValueError("No Tongji rows found in manifest.")
    tongji["__session_norm"] = tongji[session_col].map(normalize_session_value)
    sessions = set(tongji["__session_norm"].unique())
    if not {"s1", "s2"}.issubset(sessions):
        raise ValueError(f"Tongji requires s1/s2 sessions, found: {sorted(sessions)}")

    audit_lines = []
    prefix = "tongji_subject_disjoint" if identity_name == "subject_id" else "tongji_disjoint_identity"

    for seed in SEEDS:
        ids = sorted(tongji[identity_col].dropna().unique().tolist(), key=lambda x: str(x))
        train_ids, test_ids = split_ids(ids, seed, train_ratio=0.8)
        overlap = train_ids & test_ids
        if overlap:
            raise AssertionError("Train/test identity overlap detected.")

        for direction, train_session, probe_session in [
            ("s1_to_s2", "s1", "s2"),
            ("s2_to_s1", "s2", "s1"),
        ]:
            train_pool = indices_for(tongji, tongji[identity_col].isin(train_ids) & (tongji["__session_norm"] == train_session))
            train_idx, val_idx = half_split(train_pool, seed + 17, val_ratio=0.2)
            gallery_idx = indices_for(tongji, tongji[identity_col].isin(test_ids) & (tongji["__session_norm"] == train_session))
            probe_idx = indices_for(tongji, tongji[identity_col].isin(test_ids) & (tongji["__session_norm"] == probe_session))

            split = {
                "train": materialize(df, train_idx, mode, path_col, record_fields),
                "val": materialize(df, val_idx, mode, path_col, record_fields),
                "gallery": materialize(df, gallery_idx, mode, path_col, record_fields),
                "probe": materialize(df, probe_idx, mode, path_col, record_fields),
                "support": [],
            }
            out_path = out_dir / f"{prefix}_{direction}_seed{seed}.json"
            audit_lines.append(f"## {out_path.name}")
            audit_lines.append(f"- identity column: {identity_col} ({identity_name})")
            audit_lines.append(f"- split record mode: {mode}")
            audit_lines.append(f"- train identities: {len(train_ids)}")
            audit_lines.append(f"- test identities: {len(test_ids)}")
            audit_lines.append(f"- train images: {len(train_idx)}")
            audit_lines.append(f"- val images: {len(val_idx)}")
            audit_lines.append(f"- gallery images: {len(gallery_idx)}")
            audit_lines.append(f"- probe images: {len(probe_idx)}")
            audit_lines.append(f"- train/test identity overlap: {len(overlap)}")
            audit_lines.append("")
            if write:
                if out_path.exists() and not force:
                    raise FileExistsError(f"Refusing to overwrite existing split without --force: {out_path}")
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_text(json.dumps(split, ensure_ascii=False, indent=2), encoding="utf-8")
    return audit_lines


def make_iitd_splits(
    df: pd.DataFrame,
    dataset_col: str,
    identity_col: str,
    identity_name: str,
    path_col: str | None,
    out_dir: Path,
    template_path: Path | None,
    write: bool,
    force: bool,
) -> list[str]:
    mode, record_fields = load_template_mode(template_path)
    dataset_norm = df[dataset_col].map(normalize_dataset_value)
    iitd = df[dataset_norm.str.contains("iitd", na=False)].copy()
    if iitd.empty:
        return ["# IITD", "", "No IITD rows found; skipped.", ""]
    prefix = "iitd_subject_disjoint" if identity_name == "subject_id" else "iitd_disjoint_identity"
    audit_lines = ["# IITD secondary within-dataset candidate splits", ""]
    for seed in SEEDS:
        ids = sorted(iitd[identity_col].dropna().unique().tolist(), key=lambda x: str(x))
        train_ids, test_ids = split_ids(ids, seed, train_ratio=0.8)
        train_pool = indices_for(iitd, iitd[identity_col].isin(train_ids))
        train_idx, val_idx = half_split(train_pool, seed + 31, val_ratio=0.2)
        test_pool = indices_for(iitd, iitd[identity_col].isin(test_ids))

        # Same-session within-dataset enrollment/probe split for held-out test identities.
        # IMPORTANT: split inside each held-out palm class, not across the pooled image
        # list. A pooled image-level split can put an entire palm class only in gallery
        # or only in probe, which breaks closed-set identification/verification.
        gallery_idx = []
        probe_idx = []
        rng_test = random.Random(seed + 53)

        # `identity_col` controls development/test disjointness. For IITD, the final
        # evaluation label is palm/class, so gallery/probe must both contain each
        # evaluated class_id/palm_id.
        eval_group_col = "class_id" if "class_id" in iitd.columns else identity_col
        test_groups = sorted(iitd.loc[test_pool, eval_group_col].dropna().unique().tolist())

        for eval_group in test_groups:
            group_idx = indices_for(iitd, iitd.index.isin(test_pool) & (iitd[eval_group_col] == eval_group))
            group_idx = list(group_idx)
            rng_test.shuffle(group_idx)
            if len(group_idx) < 2:
                raise ValueError(f"IITD evaluation group {eval_group!r} has fewer than 2 images.")
            cut = max(1, len(group_idx) // 2)
            if cut >= len(group_idx):
                cut = len(group_idx) - 1
            gallery_idx.extend(group_idx[:cut])
            probe_idx.extend(group_idx[cut:])

        split = {
            "train": materialize(df, train_idx, mode, path_col, record_fields),
            "val": materialize(df, val_idx, mode, path_col, record_fields),
            "gallery": materialize(df, gallery_idx, mode, path_col, record_fields),
            "probe": materialize(df, probe_idx, mode, path_col, record_fields),
            "support": [],
        }
        out_path = out_dir / f"{prefix}_within_seed{seed}.json"
        audit_lines.append(f"## {out_path.name}")
        audit_lines.append(f"- identity column: {identity_col} ({identity_name})")
        audit_lines.append(f"- split record mode: {mode}")
        audit_lines.append(f"- train identities: {len(train_ids)}")
        audit_lines.append(f"- test identities: {len(test_ids)}")
        audit_lines.append(f"- train images: {len(train_idx)}")
        audit_lines.append(f"- val images: {len(val_idx)}")
        audit_lines.append(f"- gallery images: {len(gallery_idx)}")
        audit_lines.append(f"- probe images: {len(probe_idx)}")
        audit_lines.append(f"- train/test identity overlap: {len(train_ids & test_ids)}")
        audit_lines.append("- note: IITD is secondary within-dataset validation, not cross-session evidence.")
        audit_lines.append("")
        if write:
            if out_path.exists() and not force:
                raise FileExistsError(f"Refusing to overwrite existing split without --force: {out_path}")
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(json.dumps(split, ensure_ascii=False, indent=2), encoding="utf-8")
    return audit_lines


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default="data/metadata/palm_segmented_manifest.csv")
    ap.add_argument("--out-dir", default="data/splits")
    ap.add_argument("--audit", default="docs/results/disjoint_identity_split_audit.md")
    ap.add_argument("--template-split", default="", help="Optional existing split JSON to infer split record format.")
    ap.add_argument("--write", action="store_true", help="Actually write JSON splits. Without this, only audit is printed/written.")
    ap.add_argument("--force", action="store_true", help="Allow overwriting generated split files.")
    args = ap.parse_args()

    manifest = Path(args.manifest)
    if not manifest.exists():
        raise SystemExit(f"Manifest not found: {manifest}")

    df = pd.read_csv(manifest)
    dataset_col = infer_col(df, DATASET_COLS)
    session_col = infer_col(df, SESSION_COLS)
    path_col = infer_col(df, PATH_COLS)

    subject_col = infer_col(df, IDENTITY_COLS_STRICT)
    fallback_col = infer_col(df, IDENTITY_COLS_FALLBACK)
    if subject_col:
        identity_col = subject_col
        identity_name = "subject_id"
    elif fallback_col:
        identity_col = fallback_col
        identity_name = "palm_or_class_id"
    else:
        raise SystemExit("No usable identity column found. Add subject_id, palm_id, class_id, label, or equivalent.")

    if not dataset_col:
        raise SystemExit("No dataset/source column found in manifest.")
    if not session_col:
        raise SystemExit("No session column found in manifest; Tongji cross-session split cannot be generated.")

    out_dir = Path(args.out_dir)
    template_path = Path(args.template_split) if args.template_split else None
    audit_lines = [
        "# Disjoint-Identity Split Audit",
        "",
        f"- manifest: `{manifest}`",
        f"- dataset column: `{dataset_col}`",
        f"- identity column: `{identity_col}` ({identity_name})",
        f"- session column: `{session_col}`",
        f"- path column: `{path_col}`",
        f"- write mode: `{args.write}`",
        "",
        "Terminology rule: use `subject-disjoint` only if identity column is true subject_id. Otherwise use `disjoint-identity` or `palm-disjoint`.",
        "",
        "# Tongji",
        "",
    ]
    audit_lines += make_tongji_splits(
        df=df,
        dataset_col=dataset_col,
        identity_col=identity_col,
        identity_name=identity_name,
        session_col=session_col,
        path_col=path_col,
        out_dir=out_dir,
        template_path=template_path,
        write=args.write,
        force=args.force,
    )
    audit_lines += make_iitd_splits(
        df=df,
        dataset_col=dataset_col,
        identity_col=identity_col,
        identity_name=identity_name,
        path_col=path_col,
        out_dir=out_dir,
        template_path=template_path,
        write=args.write,
        force=args.force,
    )

    audit_path = Path(args.audit)
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    audit_text = "\n".join(audit_lines)
    audit_path.write_text(audit_text, encoding="utf-8")
    print(audit_text)
    print(f"\nAudit written to: {audit_path}")


if __name__ == "__main__":
    main()
