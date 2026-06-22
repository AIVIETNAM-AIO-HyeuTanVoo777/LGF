#!/usr/bin/env python
"""
Rank-B split audit and IITD fallback split generator for PALM_CGK_BASE.

Purpose:
- Audit existing Tongji disjoint cross-session split JSON files.
- Diagnose manifest schema, dataset rows, identity/session/path columns.
- Generate a populated docs/results/rank_b_repo_protocol_audit.md.
- Optionally create IITD identity-disjoint within-dataset split JSON files if the manifest schema is sufficient.

Safe defaults:
- Does not modify training/eval/model code.
- Does not overwrite split files unless --force is passed.
- Does not write IITD splits unless --write-iitd is passed.
- Does not touch raw biometric data, checkpoints, embeddings, or experiment folders.

Usage from repo root:
  python scripts\\rank_b_split_audit_and_iitd_fix.py --write-audit
  python scripts\\rank_b_split_audit_and_iitd_fix.py --write-audit --write-iitd
  python scripts\\rank_b_split_audit_and_iitd_fix.py --write-audit --write-iitd --force
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

SEEDS = [42, 2026, 2705]
TONGJI_SPLIT_PATTERNS = [
    "tongji_subject_disjoint_s1_to_s2_seed*.json",
    "tongji_subject_disjoint_s2_to_s1_seed*.json",
    "tongji_identity_disjoint_s1_to_s2_seed*.json",
    "tongji_identity_disjoint_s2_to_s1_seed*.json",
    "tongji_palm_disjoint_s1_to_s2_seed*.json",
    "tongji_palm_disjoint_s2_to_s1_seed*.json",
]
SPLIT_KEYS = ["train", "val", "gallery", "probe", "support"]

def norm_name(s: str) -> str:
    return s.strip().lower().replace("-", "_").replace(" ", "_")

def find_col(fieldnames: List[str], candidates: Iterable[str], contains: bool = False) -> Optional[str]:
    normalized = {norm_name(c): c for c in fieldnames}
    for cand in candidates:
        key = norm_name(cand)
        if key in normalized:
            return normalized[key]
    if contains:
        for raw in fieldnames:
            n = norm_name(raw)
            for cand in candidates:
                if norm_name(cand) in n:
                    return raw
    return None

def read_manifest(path: Path) -> Tuple[List[Dict[str, str]], List[str]]:
    if not path.exists():
        raise FileNotFoundError(f"Manifest not found: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames or []
    if not rows:
        raise ValueError(f"Manifest is empty: {path}")
    return rows, fieldnames

def detect_schema(fieldnames: List[str]) -> Dict[str, Optional[str]]:
    dataset_col = find_col(fieldnames, ["dataset", "dataset_name", "source_dataset", "source", "database", "db"], contains=True)
    subject_col = find_col(fieldnames, ["subject_id", "subject", "person_id", "person", "user_id", "user"])
    palm_col = find_col(fieldnames, ["palm_id", "palm", "class_id", "class", "identity", "label", "target"])
    session_col = find_col(fieldnames, ["session_id", "session", "sess", "capture_session"], contains=True)
    path_col = find_col(fieldnames, ["image_path", "img_path", "filepath", "file_path", "path", "filename", "file"], contains=True)
    width_col = find_col(fieldnames, ["width", "w"])
    height_col = find_col(fieldnames, ["height", "h"])
    return {
        "dataset": dataset_col,
        "subject": subject_col,
        "identity": subject_col or palm_col,
        "palm_or_class": palm_col,
        "session": session_col,
        "path": path_col,
        "width": width_col,
        "height": height_col,
    }

def dataset_rows(rows: List[Dict[str, str]], dataset_col: Optional[str], name: str) -> List[Tuple[int, Dict[str, str]]]:
    if dataset_col is None:
        return []
    lname = name.lower()
    out = []
    for idx, row in enumerate(rows):
        v = str(row.get(dataset_col, "")).lower()
        if lname in v:
            out.append((idx, row))
    return out

def path_variants(p: str) -> List[str]:
    p = str(p).strip()
    variants = {p, p.replace("\\", "/"), p.replace("/", "\\")}
    try:
        pp = Path(p)
        variants.add(pp.name)
        variants.add(pp.as_posix())
    except Exception:
        pass
    return [v for v in variants if v]

def build_row_lookup(rows: List[Dict[str, str]], schema: Dict[str, Optional[str]]) -> Dict[Any, List[int]]:
    lookup: Dict[Any, List[int]] = defaultdict(list)
    path_col = schema.get("path")
    for idx, row in enumerate(rows):
        lookup[("index", idx)].append(idx)
        lookup[("index_str", str(idx))].append(idx)
        if path_col and row.get(path_col):
            for v in path_variants(row[path_col]):
                lookup[("path", v)].append(idx)
    return lookup

def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def extract_split_lists(data: Any) -> Optional[Dict[str, List[Any]]]:
    """Try common split JSON layouts and return train/val/gallery/probe/support lists."""
    if isinstance(data, dict):
        if all(k in data for k in ["train", "val", "gallery", "probe"]):
            return {k: list(data.get(k, [])) for k in SPLIT_KEYS}
        # Common nested wrappers.
        for wrapper_key in ["split", "splits", "data", "items"]:
            if wrapper_key in data and isinstance(data[wrapper_key], dict):
                nested = extract_split_lists(data[wrapper_key])
                if nested is not None:
                    return nested
    return None

def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def resolve_item_to_row_indices(
    item: Any,
    rows: List[Dict[str, str]],
    schema: Dict[str, Optional[str]],
    lookup: Dict[Any, List[int]],
) -> List[int]:
    if isinstance(item, int):
        return lookup.get(("index", item), [])
    if isinstance(item, str):
        s = item.strip()
        if s.isdigit():
            by_i = lookup.get(("index", int(s)), [])
            if by_i:
                return by_i
        hits: List[int] = []
        for v in path_variants(s):
            hits += lookup.get(("path", v), [])
        return sorted(set(hits))
    if isinstance(item, dict):
        # Direct row index keys.
        for k in ["index", "idx", "row_index", "manifest_index", "manifest_idx"]:
            if k in item:
                try:
                    return lookup.get(("index", int(item[k])), [])
                except Exception:
                    pass
        # Direct path keys.
        for k in ["image_path", "img_path", "filepath", "file_path", "path", "filename", "file"]:
            if k in item and item[k]:
                hits: List[int] = []
                for v in path_variants(str(item[k])):
                    hits += lookup.get(("path", v), [])
                if hits:
                    return sorted(set(hits))
    return []

def item_identity(item: Any, row_indices: List[int], rows: List[Dict[str, str]], schema: Dict[str, Optional[str]]) -> Optional[str]:
    ident_col = schema.get("identity")
    subject_col = schema.get("subject")
    palm_col = schema.get("palm_or_class")
    # Prefer direct item metadata if present.
    if isinstance(item, dict):
        for k in [subject_col, palm_col, ident_col, "subject_id", "palm_id", "class_id", "identity", "label", "target"]:
            if k and k in item and item[k] not in [None, ""]:
                return str(item[k])
    if row_indices:
        row = rows[row_indices[0]]
        if ident_col and row.get(ident_col) not in [None, ""]:
            return str(row[ident_col])
    return None

def item_session(item: Any, row_indices: List[int], rows: List[Dict[str, str]], schema: Dict[str, Optional[str]]) -> Optional[str]:
    sess_col = schema.get("session")
    if isinstance(item, dict):
        for k in [sess_col, "session_id", "session", "sess"]:
            if k and k in item and item[k] not in [None, ""]:
                return str(item[k])
    if row_indices:
        row = rows[row_indices[0]]
        if sess_col and row.get(sess_col) not in [None, ""]:
            return str(row[sess_col])
    return None

def audit_split_file(path: Path, rows: List[Dict[str, str]], schema: Dict[str, Optional[str]], lookup: Dict[Any, List[int]]) -> List[str]:
    lines: List[str] = []
    lines.append(f"### {path.as_posix()}")
    lines.append("")
    try:
        data = load_json(path)
        splits = extract_split_lists(data)
    except Exception as e:
        lines.append(f"- STATUS: FAIL_LOAD_JSON: `{e}`")
        lines.append("")
        return lines
    if splits is None:
        lines.append("- STATUS: FAIL_SCHEMA: Could not find train/val/gallery/probe lists.")
        lines.append("")
        return lines

    lines.append(f"- SHA256: `{file_sha256(path)}`")
    lines.append("- Split item counts:")
    for k in SPLIT_KEYS:
        lines.append(f"  - {k}: {len(splits.get(k, []))}")

    id_sets: Dict[str, set] = {}
    sess_counts: Dict[str, Counter] = {}
    unresolved_counts: Dict[str, int] = {}
    ambiguous_counts: Dict[str, int] = {}

    for key, items in splits.items():
        ids = set()
        sess = Counter()
        unresolved = 0
        ambiguous = 0
        for item in items:
            row_idxs = resolve_item_to_row_indices(item, rows, schema, lookup)
            if len(row_idxs) > 1:
                ambiguous += 1
            if not row_idxs and not isinstance(item, dict):
                unresolved += 1
            ident = item_identity(item, row_idxs, rows, schema)
            if ident is not None:
                ids.add(ident)
            session = item_session(item, row_idxs, rows, schema)
            if session is not None:
                sess[session] += 1
        id_sets[key] = ids
        sess_counts[key] = sess
        unresolved_counts[key] = unresolved
        ambiguous_counts[key] = ambiguous

    lines.append("- Identity counts:")
    for k in SPLIT_KEYS:
        lines.append(f"  - {k}: {len(id_sets.get(k, set()))}")
    lines.append("- Session counts:")
    for k in SPLIT_KEYS:
        lines.append(f"  - {k}: {dict(sess_counts.get(k, Counter()))}")
    lines.append("- Resolution diagnostics:")
    for k in SPLIT_KEYS:
        lines.append(f"  - {k}: unresolved_items={unresolved_counts[k]}, ambiguous_path_matches={ambiguous_counts[k]}")

    train = id_sets.get("train", set())
    val = id_sets.get("val", set())
    gallery = id_sets.get("gallery", set())
    probe = id_sets.get("probe", set())
    support = id_sets.get("support", set())
    test = gallery | probe | support

    checks = {
        "train∩val": train & val,
        "train∩test": train & test,
        "val∩test": val & test,
        "gallery∩probe_expected_nonempty": gallery & probe,
    }
    lines.append("- Overlap checks:")
    lines.append(f"  - train∩val: {len(checks['train∩val'])}")
    lines.append(f"  - train∩test: {len(checks['train∩test'])}")
    lines.append(f"  - val∩test: {len(checks['val∩test'])}")
    lines.append(f"  - gallery∩probe: {len(checks['gallery∩probe_expected_nonempty'])} (expected: nonzero and usually equal held-out test identities)")
    if checks["train∩val"] or checks["train∩test"] or checks["val∩test"]:
        lines.append("- VERDICT: FAIL_OVERLAP")
    elif unresolved_counts["train"] or unresolved_counts["val"] or unresolved_counts["gallery"] or unresolved_counts["probe"]:
        lines.append("- VERDICT: PASS_WITH_WARNINGS_UNRESOLVED_ITEMS")
    elif len(gallery & probe) == 0:
        lines.append("- VERDICT: PASS_WITH_WARNINGS_EMPTY_GALLERY_PROBE_ID_OVERLAP")
    else:
        lines.append("- VERDICT: PASS")
    lines.append("")
    return lines

def infer_split_item_style(template_path: Path) -> str:
    if not template_path.exists():
        return "path"
    try:
        splits = extract_split_lists(load_json(template_path))
    except Exception:
        return "path"
    if not splits:
        return "path"
    for k in ["train", "val", "gallery", "probe"]:
        items = splits.get(k, [])
        if items:
            sample = items[0]
            if isinstance(sample, int):
                return "index"
            if isinstance(sample, str):
                return "path"
            if isinstance(sample, dict):
                return "dict"
    return "path"

def encode_item(row_idx: int, row: Dict[str, str], schema: Dict[str, Optional[str]], style: str) -> Any:
    if style == "index":
        return row_idx
    path_col = schema.get("path")
    if style == "path":
        if not path_col or not row.get(path_col):
            return row_idx
        return row[path_col]
    # Dict style: include conservative fields expected by many loaders.
    out: Dict[str, Any] = {}
    if path_col and row.get(path_col):
        out["image_path"] = row[path_col]
    for k in ["dataset", "identity", "palm_or_class", "subject", "session"]:
        col = schema.get(k)
        if col and row.get(col) not in [None, ""]:
            out[col] = row[col]
    out["manifest_index"] = row_idx
    return out

def make_iitd_disjoint_splits(
    rows: List[Dict[str, str]],
    schema: Dict[str, Optional[str]],
    out_dir: Path,
    template_path: Path,
    force: bool,
) -> List[str]:
    lines: List[str] = []
    ident_col = schema.get("identity")
    dataset_col = schema.get("dataset")
    path_col = schema.get("path")
    if not dataset_col:
        return ["## IITD Split Generation", "", "- VERDICT: FAIL_NO_DATASET_COLUMN", ""]
    if not ident_col:
        return ["## IITD Split Generation", "", "- VERDICT: FAIL_NO_IDENTITY_COLUMN", ""]
    iitd = dataset_rows(rows, dataset_col, "iitd")
    if not iitd:
        # Some manifests may use "IIT Delhi".
        iitd = [(idx, row) for idx, row in enumerate(rows) if "iit" in str(row.get(dataset_col, "")).lower() and "tongji" not in str(row.get(dataset_col, "")).lower()]
    lines.append("## IITD Split Generation")
    lines.append("")
    lines.append(f"- IITD candidate rows: {len(iitd)}")
    if not iitd:
        lines.append("- VERDICT: SKIP_NO_IITD_ROWS")
        lines.append("")
        return lines
    if not path_col:
        lines.append("- WARNING: no path column detected; will encode row indices.")
    by_id: Dict[str, List[Tuple[int, Dict[str, str]]]] = defaultdict(list)
    for idx, row in iitd:
        ident = str(row.get(ident_col, "")).strip()
        if ident:
            by_id[ident].append((idx, row))
    ids = sorted(by_id)
    lines.append(f"- Identity column used: `{ident_col}`")
    lines.append(f"- IITD identities: {len(ids)}")
    too_small = [i for i in ids if len(by_id[i]) < 2]
    lines.append(f"- IITD identities with <2 images: {len(too_small)}")
    if len(ids) < 10:
        lines.append("- VERDICT: FAIL_TOO_FEW_IDENTITIES")
        lines.append("")
        return lines

    style = infer_split_item_style(template_path)
    lines.append(f"- Output item style inferred from `{template_path.as_posix()}`: `{style}`")

    n = len(ids)
    n_train = int(round(n * 0.60))
    n_val = int(round(n * 0.20))
    if n_train + n_val >= n:
        n_val = max(1, n - n_train - 1)

    out_dir.mkdir(parents=True, exist_ok=True)
    for seed in SEEDS:
        rng = random.Random(seed)
        shuffled = ids[:]
        rng.shuffle(shuffled)
        train_ids = set(shuffled[:n_train])
        val_ids = set(shuffled[n_train:n_train + n_val])
        test_ids = set(shuffled[n_train + n_val:])

        split = {k: [] for k in SPLIT_KEYS}
        for ident in sorted(train_ids):
            for idx, row in by_id[ident]:
                split["train"].append(encode_item(idx, row, schema, style))
        for ident in sorted(val_ids):
            for idx, row in by_id[ident]:
                split["val"].append(encode_item(idx, row, schema, style))

        skipped_test_ids = 0
        for ident in sorted(test_ids):
            samples = by_id[ident][:]
            rng.shuffle(samples)
            if len(samples) < 2:
                skipped_test_ids += 1
                continue
            cut = max(1, len(samples) // 2)
            gallery_samples = samples[:cut]
            probe_samples = samples[cut:]
            if not probe_samples:
                probe_samples = gallery_samples[-1:]
                gallery_samples = gallery_samples[:-1]
            for idx, row in gallery_samples:
                split["gallery"].append(encode_item(idx, row, schema, style))
            for idx, row in probe_samples:
                split["probe"].append(encode_item(idx, row, schema, style))
        split["support"] = []

        out_path = out_dir / f"iitd_identity_disjoint_within_seed{seed}.json"
        if out_path.exists() and not force:
            lines.append(f"- seed {seed}: SKIP_EXISTS `{out_path.as_posix()}`")
            continue
        with out_path.open("w", encoding="utf-8") as f:
            json.dump(split, f, indent=2, ensure_ascii=False)
        lines.append(f"- seed {seed}: wrote `{out_path.as_posix()}`")
        lines.append(f"  - train_ids={len(train_ids)}, val_ids={len(val_ids)}, test_ids={len(test_ids)}, skipped_test_ids={skipped_test_ids}")
        lines.append(f"  - train={len(split['train'])}, val={len(split['val'])}, gallery={len(split['gallery'])}, probe={len(split['probe'])}, support=0")
    lines.append("- VERDICT: PASS_WITH_WARNINGS_WITHIN_DATASET_NOT_CROSS_SESSION")
    lines.append("")
    return lines

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="data/metadata/palm_segmented_manifest.csv")
    parser.add_argument("--splits-dir", default="data/splits")
    parser.add_argument("--audit", default="docs/results/rank_b_repo_protocol_audit.md")
    parser.add_argument("--template-iitd", default="data/splits/iitd_within.json")
    parser.add_argument("--write-audit", action="store_true")
    parser.add_argument("--write-iitd", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    manifest = Path(args.manifest)
    splits_dir = Path(args.splits_dir)
    audit_path = Path(args.audit)

    rows, fieldnames = read_manifest(manifest)
    schema = detect_schema(fieldnames)
    lookup = build_row_lookup(rows, schema)

    lines: List[str] = []
    lines.append("# Rank-B Repo and Protocol Audit")
    lines.append("")
    lines.append("## Manifest schema")
    lines.append("")
    lines.append(f"- Manifest: `{manifest.as_posix()}`")
    lines.append(f"- Total rows: {len(rows)}")
    lines.append(f"- Columns: `{', '.join(fieldnames)}`")
    for k, v in schema.items():
        lines.append(f"- Detected {k} column: `{v}`")
    disjoint_term = "subject-disjoint" if schema.get("subject") else "identity-disjoint / palm-disjoint / class-disjoint"
    lines.append(f"- Safe paper terminology based on detected schema: **{disjoint_term}**")
    lines.append("")

    lines.append("## Dataset rows")
    lines.append("")
    dcol = schema.get("dataset")
    if dcol:
        ds_counts = Counter(str(r.get(dcol, "")) for r in rows)
        lines.append("- Dataset value counts:")
        for k, v in ds_counts.most_common():
            lines.append(f"  - `{k}`: {v}")
        lines.append(f"- Tongji rows detected: {len(dataset_rows(rows, dcol, 'tongji'))}")
        iitd_count = len(dataset_rows(rows, dcol, 'iitd'))
        if iitd_count == 0:
            iitd_count = sum(1 for r in rows if "iit" in str(r.get(dcol, "")).lower() and "tongji" not in str(r.get(dcol, "")).lower())
        lines.append(f"- IITD rows detected: {iitd_count}")
    else:
        lines.append("- FAIL: No dataset column detected.")
    lines.append("")

    lines.append("## Existing Tongji disjoint split files")
    lines.append("")
    split_files: List[Path] = []
    for pat in TONGJI_SPLIT_PATTERNS:
        split_files.extend(sorted(splits_dir.glob(pat)))
    # De-duplicate while preserving order.
    seen = set()
    unique_split_files = []
    for p in split_files:
        if p not in seen:
            seen.add(p)
            unique_split_files.append(p)
    if not unique_split_files:
        lines.append("- VERDICT: FAIL_NO_TONGJI_DISJOINT_SPLITS_FOUND")
        lines.append("")
    else:
        lines.append(f"- Found files: {len(unique_split_files)}")
        lines.append("")
        for p in unique_split_files:
            lines += audit_split_file(p, rows, schema, lookup)

    lines.append("## IITD disjoint split files")
    lines.append("")
    iitd_files = sorted(splits_dir.glob("iitd*disjoint*.json"))
    if iitd_files:
        lines.append(f"- Found files: {len(iitd_files)}")
        for p in iitd_files:
            lines.append(f"  - `{p.as_posix()}` SHA256 `{file_sha256(p)}`")
    else:
        lines.append("- Found files: 0")
        lines.append("- VERDICT: MISSING_IITD_DISJOINT_SPLITS")
    lines.append("")

    if args.write_iitd:
        lines += make_iitd_disjoint_splits(rows, schema, splits_dir, Path(args.template_iitd), args.force)

    lines.append("## Final recommendation")
    lines.append("")
    lines.append("- Do not start B1/B6 training until the Tongji split audit verdicts are PASS or only documented PASS_WITH_WARNINGS.")
    lines.append("- If no true `subject_id` column exists, use `identity-disjoint`, `palm-disjoint`, or `class-disjoint` in the paper instead of `subject-disjoint`.")
    lines.append("- IITD should remain secondary validation and must not be described as cross-session unless a real session column supports that claim.")
    lines.append("")

    text = "\n".join(lines)
    print(text)

    if args.write_audit:
        audit_path.parent.mkdir(parents=True, exist_ok=True)
        audit_path.write_text(text, encoding="utf-8")
        print(f"\n[write] {audit_path}")

if __name__ == "__main__":
    main()
