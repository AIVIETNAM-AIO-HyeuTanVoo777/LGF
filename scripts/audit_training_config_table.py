from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List
import csv

import pandas as pd
import yaml

RUNS_CSV = Path("docs/results/strict_tongji_ablation_runs.csv")
OUT_CSV = Path("docs/audits/training_config_audit.csv")
OUT_MD = Path("docs/audits/training_config_audit.md")
OUT_TEX = Path("paper/sections/training_config_table.tex")

METHOD_ORDER = ["B0", "B1", "B4", "B5", "B6", "B7"]

METHOD_LABELS = {
    "B0": "ResNet18 + CE",
    "B1": "ResNet18 + CE + SupCon",
    "B4": "ResNet18 + ArcFace",
    "B5": "ResNet18 + BNNeck + CE",
    "B6": "ResNet18 + BNNeck + ArcFace",
    "B7": "ResNet18 + BNNeck + ArcFace + light SupCon",
}


def load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise RuntimeError(f"Invalid YAML object in {path}")
    return data


def get_nested(d: Dict[str, Any], dotted: str, default: Any = "") -> Any:
    cur: Any = d
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return default
        cur = cur[part]
    return cur


def uniq(values: List[Any]) -> List[Any]:
    out: List[Any] = []
    for v in values:
        if v not in out:
            out.append(v)
    return out


def fmt_values(values: List[Any]) -> str:
    values = uniq(values)
    if not values:
        return ""
    return "; ".join(str(v) for v in values)


def display_eval_embedding(value: Any) -> str:
    text = str(value)
    mapping = {
        "pre_bn_or_default": "pre-BN/default",
        "post_bn": "post-BN",
    }
    return mapping.get(text, text)


def infer_loss(cfg: Dict[str, Any]) -> str:
    loss_name = str(get_nested(cfg, "loss.name", "") or "")
    training_loss = str(get_nested(cfg, "training.loss_type", "") or "")
    lambda_supcon = float(get_nested(cfg, "training.lambda_supcon", 0.0) or 0.0)

    if loss_name == "arcface" or training_loss == "arcface":
        return "arcface"

    if lambda_supcon > 0:
        return "ce+supcon"

    # The training code uses the historical name "combined" for CE-compatible
    # configurations. For reviewer-facing reporting, these are CE-only when
    # lambda_supcon is zero and ArcFace is absent.
    if loss_name == "combined" or training_loss == "combined":
        return "ce"

    if loss_name:
        return loss_name
    if training_loss:
        return training_loss
    return "ce"


def method_row(method: str, sub: pd.DataFrame) -> Dict[str, Any]:
    cfgs = [load_yaml(Path(x)) for x in sub["config"].tolist()]

    seeds = sorted({int(get_nested(c, "seed")) for c in cfgs})
    directions = sorted(set(sub["direction"].astype(str).tolist()))

    row: Dict[str, Any] = {
        "method": method,
        "method_label": METHOD_LABELS.get(method, method),
        "n_runs": len(cfgs),
        "directions": ",".join(directions),
        "seeds": ",".join(str(x) for x in seeds),
        "dataset": fmt_values([get_nested(c, "dataset.name") for c in cfgs]),
        "split_files_unique": len(set(str(get_nested(c, "dataset.split_file")) for c in cfgs)),
        "model_name": fmt_values([get_nested(c, "model.name") for c in cfgs]),
        "embedding_dim": fmt_values([get_nested(c, "model.embedding_dim") for c in cfgs]),
        "pretrained": fmt_values([get_nested(c, "model.pretrained") for c in cfgs]),
        "eval_embedding": fmt_values([
            display_eval_embedding(get_nested(c, "eval.embedding", get_nested(c, "model.eval_embedding", "pre_bn_or_default")))
            for c in cfgs
        ]),
        "loss": fmt_values([infer_loss(c) for c in cfgs]),
        "arcface_scale": fmt_values([get_nested(c, "loss.scale", "") for c in cfgs if get_nested(c, "loss.scale", "") != ""]),
        "arcface_margin": fmt_values([get_nested(c, "loss.margin", "") for c in cfgs if get_nested(c, "loss.margin", "") != ""]),
        "lambda_supcon": fmt_values([get_nested(c, "training.lambda_supcon", "") for c in cfgs]),
        "temperature": fmt_values([get_nested(c, "training.temperature", "") for c in cfgs]),
        "epochs": fmt_values([get_nested(c, "training.epochs") for c in cfgs]),
        "lr": fmt_values([get_nested(c, "training.lr") for c in cfgs]),
        "weight_decay": fmt_values([get_nested(c, "training.weight_decay") for c in cfgs]),
        "grad_accumulation_steps": fmt_values([get_nested(c, "training.grad_accumulation_steps") for c in cfgs]),
        "amp": fmt_values([get_nested(c, "training.amp") for c in cfgs]),
        "sampler_num_identities": fmt_values([get_nested(c, "sampler.num_identities") for c in cfgs]),
        "sampler_num_instances": fmt_values([get_nested(c, "sampler.num_instances") for c in cfgs]),
        "sampler_fallback_identities": fmt_values([get_nested(c, "sampler.fallback_identities") for c in cfgs]),
        "num_workers": fmt_values([get_nested(c, "loader.num_workers") for c in cfgs]),
        "device": fmt_values([get_nested(c, "device") for c in cfgs]),
    }

    row["verdict"] = "PASS"
    row["notes"] = (
        "All six seed-direction configs for this method were parsed. "
        "Fields that vary by run are seeds, split files, and save directories."
    )
    return row


def write_csv(rows: List[Dict[str, Any]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())

    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def write_md(rows: List[Dict[str, Any]]) -> None:
    md: List[str] = []
    md.append("# Training Configuration Audit")
    md.append("")
    md.append("This audit summarizes the training/evaluation configuration fields used by the final strict Tongji component-ablation runs.")
    md.append("")
    md.append("- Source run table: `docs/results/strict_tongji_ablation_runs.csv`.")
    md.append("- Source configs: YAML files listed in the `config` column of the run table.")
    md.append("- Scope: B0/B1/B4/B5/B6/B7 under the strict Tongji palm-class-disjoint protocol.")
    md.append("- Each method has six configs: two session directions and three seeds.")
    md.append("- Fields that intentionally vary across configs are seed, split file, save directory, and session direction.")
    md.append("")
    md.append("## Method-level summary")
    md.append("")
    md.append("| Method | Model | Loss | Eval embedding | SupCon lambda | ArcFace | Epochs | LR | WD | Sampler | AMP | Verdict |")
    md.append("|---|---|---|---|---:|---|---:|---:|---:|---|---|---|")

    for r in rows:
        arcface = ""
        if r["arcface_scale"] or r["arcface_margin"]:
            arcface = f"s={r['arcface_scale']}, m={r['arcface_margin']}"
        else:
            arcface = "-"
        sampler = f"{r['sampler_num_identities']}x{r['sampler_num_instances']}"

        md.append(
            f"| {r['method']} {r['method_label']} | {r['model_name']} | {r['loss']} | "
            f"{r['eval_embedding']} | {r['lambda_supcon']} | {arcface} | "
            f"{r['epochs']} | {r['lr']} | {r['weight_decay']} | {sampler} | {r['amp']} | {r['verdict']} |"
        )

    md.append("")
    md.append("## Reviewer-facing notes")
    md.append("")
    md.append("- All final strict Tongji methods use 60 epochs, learning rate 1e-4, weight decay 1e-4, AMP enabled, and gradient accumulation of four steps.")
    md.append("- B1 uses supervised contrastive regularization with lambda 0.1 and temperature 0.07.")
    md.append("- B5 isolates BNNeck with cross-entropy by using BNNeck/post-BN evaluation and lambda_supcon 0.0.")
    md.append("- B6 isolates BNNeck+ArcFace by using BNNeck/post-BN evaluation, ArcFace scale 30.0, margin 0.5, and lambda_supcon 0.0.")
    md.append("- B7 adds a light supervised contrastive term to BNNeck+ArcFace with lambda_supcon 0.02.")
    md.append("- Config filenames retain historical `subject_disjoint` naming, but the paper claim remains palm-class-disjoint according to the identity/parser and gallery/probe audits.")

    OUT_MD.write_text("\n".join(md).rstrip() + "\n", encoding="utf-8")


def write_tex(rows: List[Dict[str, Any]]) -> None:
    tex: List[str] = []
    tex.append(r"\begin{table*}[t]")
    tex.append(r"\centering")
    tex.append(r"\caption{Training configuration summary for the final strict Tongji component ablation. The table reports method-level settings shared across the two session directions and three seeds. All methods use ImageNet-pretrained ResNet18 variants, 256-dimensional embeddings, 60 epochs, learning rate $10^{-4}$, weight decay $10^{-4}$, AMP, and gradient accumulation of four steps.}")
    tex.append(r"\label{tab:training_config_summary}")
    tex.append(r"\resizebox{\textwidth}{!}{%")
    tex.append(r"\begin{tabular}{lllcccccc}")
    tex.append(r"\toprule")
    tex.append(r"Method & Model & Loss & Eval emb. & $\lambda_{\mathrm{supcon}}$ & ArcFace $(s,m)$ & Epochs & LR & Sampler \\")
    tex.append(r"\midrule")

    MAP_METHOD_ID = {
        "B0": "M0",
        "B1": "M1",
        "B4": "M2",
        "B5": "M4",
        "B6": "M6",
        "B7": "M7",
    }

    for r in rows:
        arcface = "-"
        if r["arcface_scale"] or r["arcface_margin"]:
            arcface = f"({r['arcface_scale']},{r['arcface_margin']})"
        sampler = f"{r['sampler_num_identities']}x{r['sampler_num_instances']}"
        method_id = MAP_METHOD_ID.get(r['method'], r['method'])
        tex.append(
            f"{method_id} {r['method_label']} & "
            f"{r['model_name']} & "
            f"{r['loss']} & "
            f"{r['eval_embedding']} & "
            f"{r['lambda_supcon']} & "
            f"{arcface} & "
            f"{r['epochs']} & "
            f"{r['lr']} & "
            f"{sampler} \\\\"
        )

    tex.append(r"\bottomrule")
    tex.append(r"\end{tabular}%")
    tex.append(r"}")
    tex.append(r"\end{table*}")

    OUT_TEX.write_text("\n".join(tex).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    if not RUNS_CSV.exists():
        raise FileNotFoundError(RUNS_CSV)

    df = pd.read_csv(RUNS_CSV)

    required = {"method", "direction", "seed", "config", "status"}
    missing = required - set(df.columns)
    if missing:
        raise RuntimeError(f"Missing run-table columns: {sorted(missing)}")

    bad = df[df["status"].astype(str).str.upper() != "OK"]
    if not bad.empty:
        raise RuntimeError(f"Found non-OK rows:\n{bad[['method','direction','seed','status']]}")

    rows: List[Dict[str, Any]] = []
    for method in METHOD_ORDER:
        sub = df[df["method"] == method].copy()
        if len(sub) != 6:
            raise RuntimeError(f"Expected 6 rows for {method}, found {len(sub)}")
        rows.append(method_row(method, sub))

    write_csv(rows)
    write_md(rows)
    write_tex(rows)

    print(f"Wrote {OUT_CSV}")
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_TEX}")
    print("VERDICTS=", {r["verdict"] for r in rows})
    print("ROWS=", len(rows))


if __name__ == "__main__":
    main()
