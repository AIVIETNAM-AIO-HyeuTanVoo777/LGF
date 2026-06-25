from __future__ import annotations

from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "docs" / "results"
AUDIT_DIR = ROOT / "docs" / "audits"

INPUTS = [
    RESULTS_DIR / "threshold_evidence_strict_tongji.csv",
    RESULTS_DIR / "threshold_evidence_iitd.csv",
]

OUTPUT_CSV = RESULTS_DIR / "threshold_evidence_conservative_tar_far.csv"
OUTPUT_AUDIT = AUDIT_DIR / "threshold_evidence_conservative_tar_far.md"

REQUIRED_COLUMNS = [
    "dataset",
    "method",
    "direction",
    "seed",
    "num_genuine",
    "num_impostor",
    "target_far",
    "selected_threshold",
    "empirical_far",
    "tar",
    "eer",
    "eer_threshold",
]

SOURCE_PRIORITY = {
    "dataset": ["dataset"],
    "method": ["method", "model", "variant"],
    "direction": ["direction"],
    "seed": ["seed"],
    "num_genuine": ["num_genuine", "n_genuine"],
    "num_impostor": ["num_impostor", "n_impostor", "num_imposter"],
    "target_far": ["target_far"],
    "selected_threshold": ["selected_threshold", "threshold"],
    "empirical_far": ["empirical_far", "far", "fpr"],
    "tar": ["tar", "tar_at_far"],
    # Prefer interpolated EER if present; fallback to nearest EER.
    "eer": ["interpolated_eer", "nearest_eer", "eer"],
    "eer_threshold": ["nearest_eer_threshold", "eer_threshold"],
}


def first_available_series(df: pd.DataFrame, candidates: list[str]) -> pd.Series:
    lower_to_original = {c.lower().strip(): c for c in df.columns}

    for cand in candidates:
        key = cand.lower().strip()
        if key in lower_to_original:
            value = df[lower_to_original[key]]
            if isinstance(value, pd.DataFrame):
                # Defensive handling for duplicate source columns.
                value = value.iloc[:, 0]
            return value

    return pd.Series([pd.NA] * len(df), index=df.index)


def normalize(df: pd.DataFrame, source: Path) -> pd.DataFrame:
    out = pd.DataFrame(index=df.index)

    for col in REQUIRED_COLUMNS:
        out[col] = first_available_series(df, SOURCE_PRIORITY[col]).values

    out["source_file"] = str(source.relative_to(ROOT))
    return out


def main() -> None:
    frames = []

    for path in INPUTS:
        if not path.exists():
            print(f"MISSING {path}")
            continue

        df = pd.read_csv(path)
        frames.append(normalize(df, path))

    if not frames:
        raise SystemExit("No threshold evidence files found.")

    out = pd.concat(frames, ignore_index=True)

    for col in ["seed", "num_genuine", "num_impostor"]:
        out[col] = pd.to_numeric(out[col], errors="coerce").astype("Int64")

    for col in [
        "target_far",
        "selected_threshold",
        "empirical_far",
        "tar",
        "eer",
        "eer_threshold",
    ]:
        out[col] = pd.to_numeric(out[col], errors="coerce")

    checkable = out.dropna(subset=["target_far", "empirical_far"]).copy()
    violations = checkable[
        checkable["empirical_far"] > checkable["target_far"] + 1e-12
    ]

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)

    out.to_csv(OUTPUT_CSV, index=False)

    lines = [
        "# Threshold-Level Evidence for Conservative TAR@FAR",
        "",
        "## Purpose",
        "",
        "This audit exports threshold-level evidence for conservative TAR@FAR.",
        "",
        "## Conservative invariant",
        "",
        "`empirical_far <= target_far` for every checkable row.",
        "",
        "## Output",
        "",
        f"`{OUTPUT_CSV.relative_to(ROOT)}`",
        "",
        "## Summary",
        "",
        f"- Rows exported: {len(out)}",
        f"- Rows with target and empirical FAR available: {len(checkable)}",
        f"- Conservative FAR violations: {len(violations)}",
        "",
        "## Columns",
        "",
        "| Column | Meaning |",
        "|---|---|",
        "| dataset | Dataset name |",
        "| method | Method or variant name |",
        "| direction | Evaluation direction |",
        "| seed | Random seed |",
        "| num_genuine | Number of genuine pairs |",
        "| num_impostor | Number of impostor pairs |",
        "| target_far | Requested FAR target |",
        "| selected_threshold | Conservative threshold selected for target FAR |",
        "| empirical_far | Empirical FAR at selected threshold |",
        "| tar | TAR at selected threshold |",
        "| eer | Interpolated EER when available, otherwise nearest EER |",
        "| eer_threshold | EER threshold associated with the run |",
        "| source_file | Source evidence file |",
        "",
        "## Status",
        "",
        "PASS" if len(violations) == 0 else "FAIL",
        "",
    ]

    if len(violations):
        lines.extend([
            "## Violations",
            "",
            violations.to_markdown(index=False),
            "",
        ])

    OUTPUT_AUDIT.write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {OUTPUT_CSV}")
    print(f"Wrote {OUTPUT_AUDIT}")
    print(f"Rows exported: {len(out)}")
    print(f"Rows with target and empirical FAR available: {len(checkable)}")
    print(f"Violations: {len(violations)}")

    if len(violations):
        raise SystemExit(1)


if __name__ == "__main__":
    main()