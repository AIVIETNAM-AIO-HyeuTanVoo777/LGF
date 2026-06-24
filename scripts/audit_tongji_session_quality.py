from __future__ import annotations

import csv
from pathlib import Path
from statistics import mean, stdev

import numpy as np
import pandas as pd
from PIL import Image


REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = REPO_ROOT / "data" / "metadata" / "palm_segmented_manifest.csv"

OUT_CSV = REPO_ROOT / "docs" / "audits" / "tongji_session_quality.csv"
OUT_MD = REPO_ROOT / "docs" / "audits" / "tongji_session_quality.md"
OUT_TEX = REPO_ROOT / "paper" / "sections" / "tongji_session_quality_table.tex"

OPENCV_AVAILABLE = False
try:
    import cv2
    OPENCV_AVAILABLE = True
except Exception:
    cv2 = None


def compute_sharpness(gray: np.ndarray) -> float:
    if OPENCV_AVAILABLE and cv2 is not None:
        return float(cv2.Laplacian(gray, cv2.CV_32F).var())
    gx = np.diff(gray, axis=1)
    gy = np.diff(gray, axis=0)
    return float(np.var(gx) + np.var(gy))


def analyze_image(path: Path) -> dict[str, float | int | bool]:
    try:
        with Image.open(path) as img:
            gray = np.asarray(img.convert("L"), dtype=np.float32)
            return {
                "corrupt": False,
                "width": int(img.size[0]),
                "height": int(img.size[1]),
                "mean_intensity": float(np.mean(gray)),
                "std_intensity": float(np.std(gray)),
                "near_black_pct": float(np.mean(gray < 10.0) * 100.0),
                "near_white_pct": float(np.mean(gray > 245.0) * 100.0),
                "sharpness": compute_sharpness(gray),
            }
    except Exception:
        return {
            "corrupt": True,
            "width": 0,
            "height": 0,
            "mean_intensity": 0.0,
            "std_intensity": 0.0,
            "near_black_pct": 0.0,
            "near_white_pct": 0.0,
            "sharpness": 0.0,
        }


def summarize(values: list[float]) -> tuple[float, float]:
    if len(values) == 0:
        return 0.0, 0.0
    if len(values) == 1:
        return values[0], 0.0
    return mean(values), stdev(values)


def fmt(x: float) -> str:
    return f"{x:.2f}"


def main() -> None:
    if not MANIFEST.exists():
        raise FileNotFoundError(MANIFEST)

    df = pd.read_csv(MANIFEST)
    required = {"path", "dataset", "session"}
    missing = required - set(df.columns)
    if missing:
        raise RuntimeError(f"Missing manifest columns: {sorted(missing)}")

    tongji = df[df["dataset"].astype(str).str.lower() == "tongji"].copy()
    if len(tongji) != 12000:
        raise RuntimeError(f"Expected 12000 Tongji images, found {len(tongji)}")

    records: list[dict[str, object]] = []
    for idx, row in tongji.iterrows():
        rel = str(row["path"])
        session = str(row["session"])
        metrics = analyze_image(REPO_ROOT / rel)
        rec: dict[str, object] = {
            "path": rel,
            "session": session,
            **metrics,
        }
        records.append(rec)

        if len(records) % 2000 == 0 or len(records) == len(tongji):
            print(f"Processed {len(records)}/{len(tongji)} Tongji images")

    qdf = pd.DataFrame(records)
    valid = qdf[qdf["corrupt"] == False].copy()

    rows: list[dict[str, object]] = []
    for session in sorted(qdf["session"].unique()):
        all_s = qdf[qdf["session"] == session]
        val_s = valid[valid["session"] == session]

        row: dict[str, object] = {
            "dataset": "Tongji",
            "session": session,
            "n_total": int(len(all_s)),
            "n_valid": int(len(val_s)),
            "n_corrupt": int(len(all_s) - len(val_s)),
        }

        for metric in [
            "width",
            "height",
            "mean_intensity",
            "std_intensity",
            "near_black_pct",
            "near_white_pct",
            "sharpness",
        ]:
            vals = [float(x) for x in val_s[metric].tolist()]
            mu, sd = summarize(vals)
            row[f"{metric}_mean"] = mu
            row[f"{metric}_std"] = sd

        rows.append(row)

    if len(rows) != 2:
        raise RuntimeError(f"Expected 2 Tongji sessions, found {len(rows)}")

    by_session = {str(r["session"]): r for r in rows}
    s1 = by_session.get("session1")
    s2 = by_session.get("session2")
    if s1 is None or s2 is None:
        raise RuntimeError(f"Expected session1/session2, found {sorted(by_session)}")

    delta = {
        "mean_intensity_delta_s2_minus_s1": float(s2["mean_intensity_mean"]) - float(s1["mean_intensity_mean"]),
        "std_intensity_delta_s2_minus_s1": float(s2["std_intensity_mean"]) - float(s1["std_intensity_mean"]),
        "sharpness_delta_s2_minus_s1": float(s2["sharpness_mean"]) - float(s1["sharpness_mean"]),
    }

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    md: list[str] = []
    md.append("# Tongji Session Image-Quality Audit")
    md.append("")
    md.append("This audit summarizes image-quality differences between Tongji session1 and session2 using the segmented manifest. It is intended to support interpretation of cross-session direction asymmetry, not to define a new evaluation metric.")
    md.append("")
    md.append(f"- Manifest: `{MANIFEST.relative_to(REPO_ROOT)}`")
    md.append(f"- OpenCV used for Laplacian sharpness: `{OPENCV_AVAILABLE}`")
    md.append("")
    md.append("## Session summary")
    md.append("")
    md.append("| Session | Images | Mean intensity | Contrast/std | Sharpness | Near-black % | Near-white % |")
    md.append("|---|---:|---:|---:|---:|---:|---:|")
    for r in rows:
        md.append(
            f"| {r['session']} | {r['n_valid']} | "
            f"{fmt(float(r['mean_intensity_mean']))}+/-{fmt(float(r['mean_intensity_std']))} | "
            f"{fmt(float(r['std_intensity_mean']))}+/-{fmt(float(r['std_intensity_std']))} | "
            f"{fmt(float(r['sharpness_mean']))}+/-{fmt(float(r['sharpness_std']))} | "
            f"{fmt(float(r['near_black_pct_mean']))} | "
            f"{fmt(float(r['near_white_pct_mean']))} |"
        )

    md.append("")
    md.append("## Session2 minus Session1 deltas")
    md.append("")
    md.append(f"- Mean intensity delta: {delta['mean_intensity_delta_s2_minus_s1']:+.2f}")
    md.append(f"- Contrast/std delta: {delta['std_intensity_delta_s2_minus_s1']:+.2f}")
    md.append(f"- Sharpness delta: {delta['sharpness_delta_s2_minus_s1']:+.2f}")
    md.append("")
    md.append("## Interpretation")
    md.append("")
    md.append("- These statistics quantify acquisition/session differences in the segmented Tongji images.")
    md.append("- They do not by themselves prove the cause of model degradation, but they provide evidence that the two sessions are not image-quality identical.")
    md.append("- Directional performance asymmetry should therefore be interpreted together with these session-level image statistics.")
    md.append("")
    OUT_MD.write_text("\n".join(md), encoding="utf-8")

    tex: list[str] = []
    tex.append(r"\begin{table}[t]")
    tex.append(r"\centering")
    tex.append(r"\scriptsize")
    tex.append(r"\setlength{\tabcolsep}{4pt}")
    tex.append(r"\caption{Tongji session-level image-quality statistics computed from segmented images. Sharpness is Laplacian variance; higher values indicate sharper images. Values are mean $\pm$ standard deviation.}")
    tex.append(r"\label{tab:tongji_session_quality}")
    tex.append(r"\resizebox{\columnwidth}{!}{")
    tex.append(r"\begin{tabular}{lcccc}")
    tex.append(r"\toprule")
    tex.append(r"Session & Images & Mean intensity & Contrast/std & Sharpness \\")
    tex.append(r"\midrule")
    for r in rows:
        tex.append(
            f"{r['session']} & {r['n_valid']} & "
            f"{fmt(float(r['mean_intensity_mean']))} $\\pm$ {fmt(float(r['mean_intensity_std']))} & "
            f"{fmt(float(r['std_intensity_mean']))} $\\pm$ {fmt(float(r['std_intensity_std']))} & "
            f"{fmt(float(r['sharpness_mean']))} $\\pm$ {fmt(float(r['sharpness_std']))} \\\\"
        )
    tex.append(r"\bottomrule")
    tex.append(r"\end{tabular}%")
    tex.append(r"}")
    tex.append(r"\end{table}")
    tex.append("")
    OUT_TEX.write_text("\n".join(tex), encoding="utf-8")

    print(f"ROWS={len(rows)}")
    print(f"TONGJI_IMAGES={len(tongji)}")
    print(f"WROTE={OUT_CSV}")
    print(f"WROTE={OUT_MD}")
    print(f"WROTE={OUT_TEX}")
    print(f"S2_MINUS_S1_MEAN_INTENSITY={delta['mean_intensity_delta_s2_minus_s1']:+.4f}")
    print(f"S2_MINUS_S1_CONTRAST_STD={delta['std_intensity_delta_s2_minus_s1']:+.4f}")
    print(f"S2_MINUS_S1_SHARPNESS={delta['sharpness_delta_s2_minus_s1']:+.4f}")


if __name__ == "__main__":
    main()