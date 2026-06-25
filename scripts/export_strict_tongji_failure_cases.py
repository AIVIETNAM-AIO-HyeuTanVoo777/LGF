from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import roc_curve


ROOT = Path(__file__).resolve().parents[1]
EXP_DIR = ROOT / "experiments"
OUT_DIR = ROOT / "docs" / "results"

TARGET_FAR = 1e-3
TOP_K = 20
SEEDS = [42, 2026, 2705]

METHODS = {
    "B1": {
        "label": "ResNet18 + CE + SupCon",
        "run_template": "b1_resnet18_ce_supcon_tongji_subject_disjoint_{direction}_seed{seed}",
    },
    "B5": {
        "label": "ResNet18 + BNNeck + CE",
        "run_template": "b5_resnet18_bnneck_ce_tongji_subject_disjoint_{direction}_seed{seed}",
    },
    "B6": {
        "label": "ResNet18 + BNNeck + ArcFace",
        "run_template": "b6_resnet18_bnneck_arcface_tongji_subject_disjoint_{direction}_seed{seed}",
    },
    "B8": {
        "label": "ResNet18 + CosFace",
        "run_template": "b8_resnet18_cosface_tongji_subject_disjoint_{direction}_seed{seed}",
    },
}

DIRECTIONS = {
    "s1s2": {
        "label": "S1->S2",
        "split_template": "data/splits/tongji_subject_disjoint_s1_to_s2_seed{seed}.json",
    },
    "s2s1": {
        "label": "S2->S1",
        "split_template": "data/splits/tongji_subject_disjoint_s2_to_s1_seed{seed}.json",
    },
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def load_split(split_path: Path) -> dict:
    return json.loads(split_path.read_text(encoding="utf-8"))


def conservative_threshold(y_true: np.ndarray, y_score: np.ndarray, target_far: float) -> dict:
    fpr, tpr, thresholds = roc_curve(y_true, y_score)
    valid = np.where(fpr <= target_far)[0]
    if len(valid) == 0:
        idx = int(np.argmin(fpr))
    else:
        best_tpr = np.max(tpr[valid])
        best = valid[np.where(tpr[valid] == best_tpr)[0]]
        idx = int(best[-1])

    return {
        "selected_threshold": float(thresholds[idx]),
        "empirical_far": float(fpr[idx]),
        "tar": float(tpr[idx]),
        "roc_index": int(idx),
    }


def meta_fields(prefix: str, item: dict) -> dict:
    return {
        f"{prefix}_path": item.get("path", ""),
        f"{prefix}_dataset": item.get("dataset", ""),
        f"{prefix}_session": item.get("session", ""),
        f"{prefix}_hand": item.get("hand", ""),
        f"{prefix}_subject_id": item.get("subject_id", ""),
        f"{prefix}_palm_id": item.get("palm_id", ""),
        f"{prefix}_class_id": item.get("class_id", ""),
        f"{prefix}_sample_id": item.get("sample_id", ""),
    }


def build_pair_coordinates(split: dict) -> dict:
    gallery = split["gallery"]
    probe = split["probe"]

    gallery_labels = np.array([x["class_id"] for x in gallery])
    probe_labels = np.array([x["class_id"] for x in probe])

    gallery_paths = np.array([x["path"] for x in gallery])
    probe_paths = np.array([x["path"] for x in probe])

    label_mask = probe_labels[:, None] == gallery_labels[None, :]
    self_mask = probe_paths[:, None] == gallery_paths[None, :]

    gen_mask = label_mask & (~self_mask)
    imp_mask = (~label_mask) & (~self_mask)

    return {
        "gallery": gallery,
        "probe": probe,
        "gallery_labels": gallery_labels,
        "probe_labels": probe_labels,
        "gen_coords": np.argwhere(gen_mask),
        "imp_coords": np.argwhere(imp_mask),
        "n_probe": len(probe),
        "n_gallery": len(gallery),
    }


def base_row(
    *,
    method: str,
    method_label: str,
    direction: str,
    seed: int,
    run_name: str,
    split_path: Path,
    scores_path: Path,
    threshold_info: dict,
    error_type: str,
    rank_within_type: int,
    score: float,
    probe_index: int,
    gallery_index: int,
    probe_item: dict,
    gallery_item: dict,
    is_error_at_threshold: bool | str,
) -> dict:
    row = {
        "method": method,
        "method_label": method_label,
        "direction": direction,
        "seed": seed,
        "run_name": run_name,
        "error_type": error_type,
        "rank_within_type": rank_within_type,
        "score": float(score),
        "target_far": TARGET_FAR,
        "selected_threshold": threshold_info["selected_threshold"],
        "empirical_far": threshold_info["empirical_far"],
        "tar_at_far": threshold_info["tar"],
        "is_error_at_threshold": is_error_at_threshold,
        "probe_index": int(probe_index),
        "gallery_index": int(gallery_index),
        "same_class": bool(probe_item.get("class_id") == gallery_item.get("class_id")),
        "split_file": rel(split_path),
        "scores_path": rel(scores_path),
    }
    row.update(meta_fields("probe", probe_item))
    row.update(meta_fields("gallery", gallery_item))
    return row


def analyze_run(method: str, method_cfg: dict, direction_key: str, direction_cfg: dict, seed: int) -> tuple[list[dict], dict]:
    direction_label = direction_cfg["label"]
    run_name = method_cfg["run_template"].format(direction=direction_key, seed=seed)
    split_path = ROOT / direction_cfg["split_template"].format(seed=seed)
    scores_path = EXP_DIR / run_name / "scores.csv"

    if not split_path.exists():
        raise FileNotFoundError(split_path)
    if not scores_path.exists():
        raise FileNotFoundError(scores_path)

    split = load_split(split_path)
    pair = build_pair_coordinates(split)

    df = pd.read_csv(scores_path)
    scores = df["score"].to_numpy(dtype=float)
    labels = df["label"].to_numpy(dtype=int)

    gen_coords = pair["gen_coords"]
    imp_coords = pair["imp_coords"]
    n_gen = len(gen_coords)
    n_imp = len(imp_coords)

    if len(df) != n_gen + n_imp:
        raise ValueError(f"{run_name}: score rows {len(df)} != reconstructed pairs {n_gen + n_imp}")
    if not np.all(labels[:n_gen] == 1):
        raise ValueError(f"{run_name}: first reconstructed genuine block does not match scores.csv labels")
    if not np.all(labels[n_gen:] == 0):
        raise ValueError(f"{run_name}: impostor block does not match scores.csv labels")

    pos_scores = scores[:n_gen]
    neg_scores = scores[n_gen:]

    threshold_info = conservative_threshold(labels, scores, TARGET_FAR)
    threshold = threshold_info["selected_threshold"]

    false_accepts_at_threshold = int(np.sum(neg_scores >= threshold))
    false_rejects_at_threshold = int(np.sum(pos_scores < threshold))

    cases: list[dict] = []

    # 1. False accepts: highest impostor scores.
    fa_order = np.argsort(-neg_scores)[:TOP_K]
    for rank, local_idx in enumerate(fa_order, start=1):
        probe_idx, gallery_idx = gen_imp_idx = imp_coords[int(local_idx)]
        probe_item = pair["probe"][int(probe_idx)]
        gallery_item = pair["gallery"][int(gallery_idx)]
        score = float(neg_scores[int(local_idx)])
        cases.append(
            base_row(
                method=method,
                method_label=method_cfg["label"],
                direction=direction_label,
                seed=seed,
                run_name=run_name,
                split_path=split_path,
                scores_path=scores_path,
                threshold_info=threshold_info,
                error_type="false_accept_top_score",
                rank_within_type=rank,
                score=score,
                probe_index=int(probe_idx),
                gallery_index=int(gallery_idx),
                probe_item=probe_item,
                gallery_item=gallery_item,
                is_error_at_threshold=bool(score >= threshold),
            )
        )

    # 2. False rejects: lowest genuine scores.
    fr_order = np.argsort(pos_scores)[:TOP_K]
    for rank, local_idx in enumerate(fr_order, start=1):
        probe_idx, gallery_idx = gen_coords[int(local_idx)]
        probe_item = pair["probe"][int(probe_idx)]
        gallery_item = pair["gallery"][int(gallery_idx)]
        score = float(pos_scores[int(local_idx)])
        cases.append(
            base_row(
                method=method,
                method_label=method_cfg["label"],
                direction=direction_label,
                seed=seed,
                run_name=run_name,
                split_path=split_path,
                scores_path=scores_path,
                threshold_info=threshold_info,
                error_type="false_reject_low_score",
                rank_within_type=rank,
                score=score,
                probe_index=int(probe_idx),
                gallery_index=int(gallery_idx),
                probe_item=probe_item,
                gallery_item=gallery_item,
                is_error_at_threshold=bool(score < threshold),
            )
        )

    # 3. Rank-1 misidentifications reconstructed from all pair scores.
    sim = np.full((pair["n_probe"], pair["n_gallery"]), -np.inf, dtype=np.float32)
    sim[gen_coords[:, 0], gen_coords[:, 1]] = pos_scores.astype(np.float32)
    sim[imp_coords[:, 0], imp_coords[:, 1]] = neg_scores.astype(np.float32)

    top_gallery_idx = np.argmax(sim, axis=1)
    top_scores = sim[np.arange(pair["n_probe"]), top_gallery_idx]
    pred_labels = pair["gallery_labels"][top_gallery_idx]
    true_labels = pair["probe_labels"]

    wrong_probe_indices = np.where(pred_labels != true_labels)[0]
    wrong_order = wrong_probe_indices[np.argsort(-top_scores[wrong_probe_indices])[:TOP_K]]

    for rank, probe_idx in enumerate(wrong_order, start=1):
        gallery_idx = int(top_gallery_idx[int(probe_idx)])
        probe_item = pair["probe"][int(probe_idx)]
        gallery_item = pair["gallery"][gallery_idx]
        cases.append(
            base_row(
                method=method,
                method_label=method_cfg["label"],
                direction=direction_label,
                seed=seed,
                run_name=run_name,
                split_path=split_path,
                scores_path=scores_path,
                threshold_info=threshold_info,
                error_type="rank1_misidentification",
                rank_within_type=rank,
                score=float(top_scores[int(probe_idx)]),
                probe_index=int(probe_idx),
                gallery_index=gallery_idx,
                probe_item=probe_item,
                gallery_item=gallery_item,
                is_error_at_threshold="NA",
            )
        )

    summary = {
        "method": method,
        "method_label": method_cfg["label"],
        "direction": direction_label,
        "seed": seed,
        "run_name": run_name,
        "target_far": TARGET_FAR,
        "selected_threshold": threshold_info["selected_threshold"],
        "empirical_far": threshold_info["empirical_far"],
        "tar_at_far": threshold_info["tar"],
        "num_genuine_pairs": int(n_gen),
        "num_impostor_pairs": int(n_imp),
        "false_accepts_at_threshold": false_accepts_at_threshold,
        "false_rejects_at_threshold": false_rejects_at_threshold,
        "rank1_misidentifications": int(len(wrong_probe_indices)),
        "num_probes": int(pair["n_probe"]),
        "rank1_misidentification_rate": float(len(wrong_probe_indices) / pair["n_probe"]),
        "rank1_accuracy_reconstructed": float(1.0 - len(wrong_probe_indices) / pair["n_probe"]),
        "split_file": rel(split_path),
        "scores_path": rel(scores_path),
    }

    return cases, summary


def write_markdown(summary_df: pd.DataFrame, cases_df: pd.DataFrame, out_path: Path) -> None:
    md: list[str] = []
    md.append("# Strict Tongji Failure Case Analysis")
    md.append("")
    md.append("This file summarizes reconstructed failure cases from saved `scores.csv` files.")
    md.append("")
    md.append("The reconstruction uses the split JSON gallery/probe order and the score export order from `eval_embedding.py`: genuine scores first, followed by impostor scores.")
    md.append("")
    md.append("## Summary")
    md.append("")
    md.append("| Method | Direction | Seed | Threshold | FAR | TAR | FA@thr | FR@thr | Rank-1 errors | Rank-1 acc. |")
    md.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for _, r in summary_df.iterrows():
        md.append(
            f"| {r['method']} | {r['direction']} | {int(r['seed'])} | "
            f"{r['selected_threshold']:.6f} | {r['empirical_far']:.6f} | {r['tar_at_far']:.6f} | "
            f"{int(r['false_accepts_at_threshold'])} | {int(r['false_rejects_at_threshold'])} | "
            f"{int(r['rank1_misidentifications'])} | {r['rank1_accuracy_reconstructed']:.6f} |"
        )

    md.append("")
    md.append("## Top failure cases by type")
    md.append("")
    for error_type in ["false_accept_top_score", "false_reject_low_score", "rank1_misidentification"]:
        subset = cases_df[cases_df["error_type"] == error_type].head(20)
        md.append(f"### {error_type}")
        md.append("")
        md.append("| Method | Direction | Seed | Rank | Score | Probe class | Gallery class | Probe path | Gallery path |")
        md.append("|---|---|---:|---:|---:|---:|---:|---|---|")
        for _, r in subset.iterrows():
            md.append(
                f"| {r['method']} | {r['direction']} | {int(r['seed'])} | {int(r['rank_within_type'])} | "
                f"{r['score']:.6f} | {r['probe_class_id']} | {r['gallery_class_id']} | "
                f"`{r['probe_path']}` | `{r['gallery_path']}` |"
            )
        md.append("")

    md.append("## Claim boundary")
    md.append("")
    md.append("- Safe: this analysis identifies score-tail and rank-1 failure cases reconstructed from saved score files and split metadata.")
    md.append("- Safe: paths/classes are reconstructed using the same gallery/probe ordering used by evaluation.")
    md.append("- Unsafe: this analysis does not by itself diagnose visual image quality, unless image-quality features are separately computed.")
    md.append("- Unsafe: do not include image figures unless dataset policy permits image display.")
    md.append("")

    out_path.write_text("\n".join(md), encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    all_cases: list[dict] = []
    all_summaries: list[dict] = []

    for method, method_cfg in METHODS.items():
        for direction_key, direction_cfg in DIRECTIONS.items():
            for seed in SEEDS:
                cases, summary = analyze_run(method, method_cfg, direction_key, direction_cfg, seed)
                all_cases.extend(cases)
                all_summaries.append(summary)
                print(
                    f"OK {method} {direction_cfg['label']} seed{seed}: "
                    f"cases={len(cases)} rank1_acc={summary['rank1_accuracy_reconstructed']:.6f} "
                    f"FAR={summary['empirical_far']:.6f} TAR={summary['tar_at_far']:.6f}"
                )

    cases_df = pd.DataFrame(all_cases)
    summary_df = pd.DataFrame(all_summaries)

    cases_path = OUT_DIR / "strict_tongji_failure_cases.csv"
    summary_path = OUT_DIR / "strict_tongji_failure_case_summary.csv"
    md_path = OUT_DIR / "strict_tongji_failure_case_summary.md"

    cases_df.to_csv(cases_path, index=False)
    summary_df.to_csv(summary_path, index=False)
    write_markdown(summary_df, cases_df, md_path)

    print(f"Wrote {rel(cases_path)} rows={len(cases_df)}")
    print(f"Wrote {rel(summary_path)} rows={len(summary_df)}")
    print(f"Wrote {rel(md_path)}")


if __name__ == "__main__":
    main()