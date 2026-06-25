from __future__ import annotations

from pathlib import Path
import shutil
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
R = ROOT / "docs" / "results"
R.mkdir(parents=True, exist_ok=True)


def copy_csv(src: str, dst: str) -> None:
    src_path = R / src
    dst_path = R / dst
    if not src_path.exists():
        raise FileNotFoundError(f"Missing source: {src_path}")
    shutil.copyfile(src_path, dst_path)
    print(f"COPIED {src} -> {dst}")


def export_strict_tongji_main() -> None:
    src = R / "gabor_strict_tongji_summary.csv"
    if not src.exists():
        raise FileNotFoundError(src)

    df = pd.read_csv(src)
    out = df[df["method"].isin(["B1", "B6"])].copy()

    if len(out) != 2:
        raise RuntimeError(
            "Expected exactly B1 and B6 rows in gabor_strict_tongji_summary.csv"
        )

    out.to_csv(R / "strict_tongji_main_b1_b6.csv", index=False)
    print("WROTE strict_tongji_main_b1_b6.csv")


def export_iitd_corrected() -> None:
    src = R / "iitd_subject_disjoint_rerun_summary.csv"
    if not src.exists():
        raise FileNotFoundError(src)

    df = pd.read_csv(src)
    out = df[df["method"].isin(["B1", "B6"])].copy()

    if len(out) != 2:
        raise RuntimeError(
            "Expected exactly B1 and B6 rows in iitd_subject_disjoint_rerun_summary.csv"
        )

    out.to_csv(R / "iitd_corrected_summary.csv", index=False)
    print("WROTE iitd_corrected_summary.csv")


def verify_required() -> None:
    required = [
        "strict_tongji_main_b1_b6.csv",
        "strict_tongji_directional_deltas.csv",
        "strict_tongji_ablation_summary.csv",
        "strict_tongji_paired_tests.csv",
        "iitd_corrected_summary.csv",
        "gabor_reference_summary.csv",
    ]

    print("\nREQUIRED OUTPUT CHECK")
    missing = []
    for name in required:
        path = R / name
        if path.exists():
            rows = len(pd.read_csv(path))
            print(f"OK      {name} rows={rows}")
        else:
            print(f"MISSING {name}")
            missing.append(name)

    if missing:
        raise SystemExit("Missing required outputs: " + ", ".join(missing))


def main() -> None:
    export_strict_tongji_main()

    copy_csv(
        "tongji_directional_delta_b6_minus_b1.csv",
        "strict_tongji_directional_deltas.csv",
    )

    copy_csv(
        "paired_delta_b6_vs_b1.csv",
        "strict_tongji_paired_tests.csv",
    )

    copy_csv(
        "gabor_strict_tongji_summary.csv",
        "gabor_reference_summary.csv",
    )

    export_iitd_corrected()

    # strict_tongji_ablation_summary.csv already exists from the prior audited run.
    ablation = R / "strict_tongji_ablation_summary.csv"
    if not ablation.exists():
        raise FileNotFoundError(ablation)
    print("FOUND strict_tongji_ablation_summary.csv")

    verify_required()


if __name__ == "__main__":
    main()