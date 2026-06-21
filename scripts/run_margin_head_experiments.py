import argparse
import copy
import json
import shutil
import subprocess
import sys
from pathlib import Path

import yaml


RESULTS_DIR = Path("docs/results")
SEED42_CONFIGS = {
    "B4": {
        "S1->S2": "configs/b4_resnet18_arcface_tongji_s1s2_lr1e4_seed42.yaml",
        "S2->S1": "configs/b4_resnet18_arcface_tongji_s2s1_lr1e4_seed42.yaml",
    },
    "B6": {
        "S1->S2": "configs/b6_resnet18_bnneck_arcface_tongji_s1s2_lr1e4_seed42.yaml",
        "S2->S1": "configs/b6_resnet18_bnneck_arcface_tongji_s2s1_lr1e4_seed42.yaml",
    },
    "B7": {
        "S1->S2": "configs/b7_resnet18_bnneck_arcface_supcon_tongji_s1s2_lr1e4_seed42.yaml",
        "S2->S1": "configs/b7_resnet18_bnneck_arcface_supcon_tongji_s2s1_lr1e4_seed42.yaml",
    },
}
B1_BASELINE = {
    "S1->S2": "docs/results/b1_resnet18_ce_supcon_tongji_s1s2_lr1e4_metrics.json",
    "S2->S1": "docs/results/b1_resnet18_ce_supcon_tongji_s2s1_lr1e4_metrics.json",
}
GO_THRESHOLDS = {
    "rank1_pp": 0.5,
    "tar_far_1e_3_pp": 1.0,
    "eer_pp": -0.2,
}


def parse_args():
    parser = argparse.ArgumentParser(description="Run B4/B6/B7 margin-head seed42 experiments.")
    parser.add_argument("--force", action="store_true", help="Rerun train/eval even if outputs exist.")
    parser.add_argument("--dry_run", action="store_true", help="Print commands without running them.")
    parser.add_argument("--only_generate_configs", action="store_true", help="Generate missing configs and exit.")
    parser.add_argument("--skip_train", action="store_true", help="Skip training phase.")
    parser.add_argument("--skip_eval", action="store_true", help="Skip evaluation phase.")
    return parser.parse_args()


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def write_yaml_if_missing(path, data):
    path = Path(path)
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False)
    return True


def metric_path_for_config(config_path):
    name = Path(config_path).stem
    return RESULTS_DIR / f"{name}_metrics.json"


def local_paths(config_path):
    cfg = load_yaml(config_path)
    save_dir = Path(cfg["save_dir"])
    return {
        "config": Path(config_path),
        "save_dir": save_dir,
        "checkpoint": save_dir / "checkpoints" / "best.pt",
        "metrics_json": save_dir / "metrics.json",
        "metrics_md": save_dir / "metrics.md",
        "docs_json": RESULTS_DIR / f"{Path(config_path).stem}_metrics.json",
        "docs_md": RESULTS_DIR / f"{Path(config_path).stem}_metrics.md",
        "docs_yaml": RESULTS_DIR / f"{Path(config_path).stem}.yaml",
    }


def seed42_template(method, direction):
    cfg = {
        "seed": 42,
        "device": "cuda",
        "dataset": {
            "name": "Tongji",
            "split_file": "data/splits/tongji_s1_to_s2.json" if direction == "S1->S2" else "data/splits/tongji_s2_to_s1.json",
        },
        "sampler": {"num_identities": 8, "num_instances": 2, "fallback_identities": 4},
        "loader": {"num_workers": 0},
        "model": {"name": "ResNet18Baseline", "embedding_dim": 256, "pretrained": True},
        "loss": {"name": "arcface", "scale": 30.0, "margin": 0.5},
        "training": {
            "loss_type": "arcface",
            "epochs": 60,
            "lr": 0.0001,
            "weight_decay": 0.0001,
            "grad_accumulation_steps": 4,
            "lambda_supcon": 0.0,
            "temperature": 0.07,
            "amp": True,
        },
    }
    if method == "B4":
        slug = "b4_resnet18_arcface"
    elif method == "B6":
        slug = "b6_resnet18_bnneck_arcface"
        cfg["model"]["name"] = "ResNet18BNNeck"
        cfg["model"]["eval_embedding"] = "post_bn"
        cfg["eval"] = {"embedding": "post_bn"}
    elif method == "B7":
        slug = "b7_resnet18_bnneck_arcface_supcon"
        cfg["model"]["name"] = "ResNet18BNNeck"
        cfg["model"]["eval_embedding"] = "post_bn"
        cfg["eval"] = {"embedding": "post_bn"}
        cfg["training"]["lambda_supcon"] = 0.05
    else:
        raise ValueError(method)
    dir_slug = "s1s2" if direction == "S1->S2" else "s2s1"
    cfg["save_dir"] = f"experiments/{slug}_tongji_{dir_slug}_lr1e4_seed42"
    return cfg


def generate_seed42_configs():
    created = []
    for method, dirs in SEED42_CONFIGS.items():
        for direction, path in dirs.items():
            if write_yaml_if_missing(path, seed42_template(method, direction)):
                created.append(path)
    return created


def run_cmd(cmd, dry_run=False):
    print("Running:", " ".join(str(c) for c in cmd))
    if dry_run:
        return
    result = subprocess.run(cmd)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def run_one(config_path, args):
    paths = local_paths(config_path)
    print("\n" + "=" * 80)
    print(f"Experiment: {paths['config'].stem}")
    print(f"Save dir: {paths['save_dir']}")

    if args.skip_train:
        print("Skipping training due to --skip_train.")
    elif paths["checkpoint"].exists() and not args.force:
        print(f"Checkpoint exists: {paths['checkpoint']}. Skipping training.")
    else:
        run_cmd(["python", "scripts/train_lgf.py", "--config", str(paths["config"])], dry_run=args.dry_run)

    if args.skip_eval:
        print("Skipping eval due to --skip_eval.")
    elif paths["metrics_json"].exists() and not args.force:
        print(f"Metrics exist: {paths['metrics_json']}. Skipping eval.")
    else:
        if not args.dry_run and not paths["checkpoint"].exists():
            raise FileNotFoundError(f"Missing checkpoint for eval: {paths['checkpoint']}")
        run_cmd(
            [
                "python",
                "scripts/eval_embedding.py",
                "--checkpoint",
                str(paths["checkpoint"]),
                "--config",
                str(paths["config"]),
            ],
            dry_run=args.dry_run,
        )

    if args.dry_run:
        return

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    if paths["metrics_json"].exists():
        shutil.copy(paths["metrics_json"], paths["docs_json"])
    if paths["metrics_md"].exists():
        shutil.copy(paths["metrics_md"], paths["docs_md"])
    shutil.copy(paths["config"], paths["docs_yaml"])


def load_metrics(path):
    path = Path(path)
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {
        "rank1": float(data["Rank-1"]) * 100.0,
        "rank5": float(data["Rank-5"]) * 100.0,
        "macro_f1": float(data["Macro-F1"]) * 100.0,
        "eer": float(data["EER"]) * 100.0,
        "tar_far_1e_2": float(data["TAR@FAR=1e-2"]) * 100.0,
        "tar_far_1e_3": float(data["TAR@FAR=1e-3"]) * 100.0,
    }


def average_metrics(rows):
    keys = ["rank1", "rank5", "macro_f1", "eer", "tar_far_1e_2", "tar_far_1e_3"]
    return {k: sum(r[k] for r in rows) / len(rows) for k in keys}


def generate_multiseed_configs(best_method):
    created = []
    commands = []
    for direction, seed42_path in SEED42_CONFIGS[best_method].items():
        base = load_yaml(seed42_path)
        for seed in [2026, 2705]:
            cfg = copy.deepcopy(base)
            cfg["seed"] = seed
            cfg["save_dir"] = cfg["save_dir"].replace("_seed42", f"_seed{seed}")
            new_path = Path(seed42_path.replace("_seed42.yaml", f"_seed{seed}.yaml"))
            if write_yaml_if_missing(new_path, cfg):
                created.append(str(new_path))
            commands.append(f"python scripts/train_lgf.py --config {new_path}")
            commands.append(
                "python scripts/eval_embedding.py "
                f"--checkpoint {cfg['save_dir']}/checkpoints/best.pt "
                f"--config {new_path}"
            )
    return created, commands


def summarize():
    b1 = {}
    for direction, path in B1_BASELINE.items():
        metrics = load_metrics(path)
        if metrics is None:
            raise FileNotFoundError(f"Missing B1 baseline metrics: {path}")
        b1[direction] = metrics
    b1_avg = average_metrics([b1["S1->S2"], b1["S2->S1"]])

    methods = {}
    for method, dirs in SEED42_CONFIGS.items():
        rows = {}
        for direction, config_path in dirs.items():
            metrics = load_metrics(metric_path_for_config(config_path))
            if metrics is not None:
                rows[direction] = metrics
        if len(rows) == 2:
            avg = average_metrics([rows["S1->S2"], rows["S2->S1"]])
            delta = {
                "rank1_pp": avg["rank1"] - b1_avg["rank1"],
                "tar_far_1e_3_pp": avg["tar_far_1e_3"] - b1_avg["tar_far_1e_3"],
                "eer_pp": avg["eer"] - b1_avg["eer"],
            }
            passed = (
                delta["rank1_pp"] >= GO_THRESHOLDS["rank1_pp"]
                or delta["tar_far_1e_3_pp"] >= GO_THRESHOLDS["tar_far_1e_3_pp"]
                or delta["eer_pp"] <= GO_THRESHOLDS["eer_pp"]
            )
            methods[method] = {"directions": rows, "bidirectional_average": avg, "delta_vs_b1": delta, "go": passed}
        else:
            methods[method] = {"directions": rows, "status": "INCOMPLETE", "go": False}

    complete = {m: v for m, v in methods.items() if "bidirectional_average" in v}
    best_method = None
    if complete:
        best_method = max(
            complete,
            key=lambda m: (
                complete[m]["go"],
                complete[m]["delta_vs_b1"]["tar_far_1e_3_pp"],
                complete[m]["delta_vs_b1"]["rank1_pp"],
                -complete[m]["delta_vs_b1"]["eer_pp"],
            ),
        )

    go = best_method is not None and complete[best_method]["go"]
    created_configs, multiseed_commands = ([], [])
    if go:
        created_configs, multiseed_commands = generate_multiseed_configs(best_method)

    summary = {
        "baseline": {"method": "B1", "seed": 42, "directions": b1, "bidirectional_average": b1_avg},
        "methods": methods,
        "best_method": best_method,
        "decision": "GO" if go else "NO-GO",
        "go_thresholds": GO_THRESHOLDS,
        "generated_multiseed_configs": created_configs,
        "multiseed_command_template": multiseed_commands,
        "note": "Full multi-seed was not run by this script; generated configs/commands only after seed42 GO.",
    }
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(RESULTS_DIR / "margin_head_seed42_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4)
    write_markdown_summary(summary)
    return summary


def fmt(v):
    return "-" if v is None else f"{v:.2f}"


def write_markdown_summary(summary):
    rows = []
    b1_avg = summary["baseline"]["bidirectional_average"]
    rows.append(
        f"| B1 | baseline | {fmt(b1_avg['rank1'])} | {fmt(b1_avg['eer'])} | {fmt(b1_avg['tar_far_1e_3'])} | - | - | - |"
    )
    for method, data in summary["methods"].items():
        if "bidirectional_average" not in data:
            rows.append(f"| {method} | INCOMPLETE | - | - | - | - | - | - |")
            continue
        avg = data["bidirectional_average"]
        delta = data["delta_vs_b1"]
        rows.append(
            f"| {method} | {'GO' if data['go'] else 'NO-GO'} | "
            f"{fmt(avg['rank1'])} | {fmt(avg['eer'])} | {fmt(avg['tar_far_1e_3'])} | "
            f"{delta['rank1_pp']:+.2f} | {delta['eer_pp']:+.2f} | {delta['tar_far_1e_3_pp']:+.2f} |"
        )

    commands = "\n".join(summary["multiseed_command_template"]) or "(none; seed42 did not meet GO threshold)"
    created = "\n".join(f"- `{p}`" for p in summary["generated_multiseed_configs"]) or "(none)"
    md = f"""# Margin Head Seed42 Summary

Decision: `{summary['decision']}`

Best method: `{summary['best_method'] or 'N/A'}`

GO threshold versus B1 seed42 bidirectional average: Rank-1 >= +0.5 pp, TAR@FAR=1e-3 >= +1.0 pp, or EER <= -0.2 pp.

| Method | Decision | Rank-1 | EER | TAR@FAR=1e-3 | Delta Rank-1 | Delta EER | Delta TAR@1e-3 |
|---|---|---:|---:|---:|---:|---:|---:|
{chr(10).join(rows)}

## Generated Multi-Seed Configs

{created}

## Multi-Seed Command Template

```bat
{commands}
```

Full multi-seed is intentionally not run by this script after seed42; run the commands above only after reviewing the seed42 summary.
"""
    (RESULTS_DIR / "margin_head_seed42_summary.md").write_text(md, encoding="utf-8")


def main():
    args = parse_args()
    created = generate_seed42_configs()
    if created:
        print("Created configs:")
        for path in created:
            print(f"  {path}")
    else:
        print("Seed42 configs already exist.")

    if args.only_generate_configs:
        return

    for dirs in SEED42_CONFIGS.values():
        for config_path in dirs.values():
            run_one(config_path, args)

    if args.dry_run:
        print("Dry run completed; summary not generated because metrics may not exist.")
        return

    summary = summarize()
    print(f"Decision: {summary['decision']}")
    print(f"Summary written to {RESULTS_DIR / 'margin_head_seed42_summary.md'}")


if __name__ == "__main__":
    main()
