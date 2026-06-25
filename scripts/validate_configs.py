from __future__ import annotations

import argparse
import glob
from pathlib import Path
from typing import Any

import yaml


REQUIRED_TOP = ["seed", "device", "save_dir", "dataset", "sampler", "loader", "model", "training"]
EXPECTED_METHODS = {"m0", "m1", "m2", "m3", "m4", "m6", "m7"}


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    raise SystemExit(1)


def nested(cfg: dict[str, Any], path: str, default: Any = None) -> Any:
    cur: Any = cfg
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return default
        cur = cur[part]
    return cur


def validate_one(path: Path) -> None:
    cfg = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(cfg, dict):
        fail(f"{path}: YAML root is not a mapping")

    for key in REQUIRED_TOP:
        if key not in cfg:
            fail(f"{path}: missing top-level key {key}")

    method = path.name.split("_", 1)[0].lower()
    if method not in EXPECTED_METHODS:
        fail(f"{path}: filename must start with one of {sorted(EXPECTED_METHODS)}")

    seed = int(cfg["seed"])
    if seed not in {42, 2026, 2705}:
        fail(f"{path}: unexpected seed {seed}")
    if f"seed{seed}" not in path.name:
        fail(f"{path}: filename seed mismatch")

    dataset = cfg["dataset"]
    dataset_name = dataset.get("name")
    if dataset_name not in {"Tongji", "IITD"}:
        fail(f"{path}: dataset.name must be Tongji or IITD")

    split_file = Path(dataset.get("split_file", ""))
    if not split_file.exists():
        fail(f"{path}: split_file not found: {split_file}")
    if f"seed{seed}" not in str(split_file):
        fail(f"{path}: split_file seed mismatch")

    if dataset_name == "Tongji":
        if "tongji_subject_disjoint" not in str(split_file):
            fail(f"{path}: Tongji config must use the audited subject_disjoint split files")
        if "s1s2" in path.name and "s1_to_s2" not in str(split_file):
            fail(f"{path}: s1s2 config does not use s1_to_s2 split")
        if "s2s1" in path.name and "s2_to_s1" not in str(split_file):
            fail(f"{path}: s2s1 config does not use s2_to_s1 split")
    else:
        if "iitd_subject_disjoint_within" not in str(split_file):
            fail(f"{path}: IITD config must use the corrected within-session split files")
        if "within" not in path.name:
            fail(f"{path}: IITD config filename must identify within-session validation")

    save_dir = str(cfg.get("save_dir", ""))
    if not save_dir.startswith("experiments/"):
        fail(f"{path}: save_dir must start with experiments/: {save_dir}")

    model = cfg["model"]
    model_name = model.get("name")
    if model_name not in {"ResNet18Baseline", "ResNet18BNNeck"}:
        fail(f"{path}: unsupported model.name {model_name}")
    if int(model.get("embedding_dim", -1)) != 256:
        fail(f"{path}: embedding_dim must be 256")

    if model_name == "ResNet18BNNeck":
        if model.get("eval_embedding") != "post_bn":
            fail(f"{path}: BNNeck requires model.eval_embedding=post_bn")
        if cfg.get("eval", {}).get("embedding") != "post_bn":
            fail(f"{path}: BNNeck requires eval.embedding=post_bn")

    training = cfg["training"]
    if int(training.get("epochs", -1)) != 60:
        fail(f"{path}: epochs must be 60")
    if abs(float(training.get("lr", -1)) - 0.0001) > 1e-12:
        fail(f"{path}: lr must be 0.0001")
    if abs(float(training.get("weight_decay", -1)) - 0.0001) > 1e-12:
        fail(f"{path}: weight_decay must be 0.0001")
    if int(training.get("grad_accumulation_steps", -1)) != 4:
        fail(f"{path}: grad_accumulation_steps must be 4")

    loss_name = str(nested(cfg, "loss.name", training.get("loss_type", "combined"))).lower()
    lambda_supcon = float(training.get("lambda_supcon", 0.0))

    expected_model = {
        "m0": "ResNet18Baseline",
        "m1": "ResNet18Baseline",
        "m2": "ResNet18Baseline",
        "m3": "ResNet18Baseline",
        "m4": "ResNet18BNNeck",
        "m6": "ResNet18BNNeck",
        "m7": "ResNet18BNNeck",
    }[method]
    if model_name != expected_model:
        fail(f"{path}: {method.upper()} must use {expected_model}")

    if method in {"m2", "m6", "m7"} and loss_name != "arcface":
        fail(f"{path}: {method.upper()} must use arcface")
    if method == "m3" and loss_name != "cosface":
        fail(f"{path}: M3 must use cosface")
    if method in {"m0", "m4"} and lambda_supcon != 0.0:
        fail(f"{path}: {method.upper()} must not use SupCon")
    if method == "m1" and lambda_supcon <= 0.0:
        fail(f"{path}: M1 must use SupCon")
    if method == "m7" and lambda_supcon <= 0.0:
        fail(f"{path}: M7 must use light SupCon")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--glob", default="configs/rankb_final/*.yaml", help="Config glob pattern")
    args = parser.parse_args()

    paths = [Path(p) for p in sorted(glob.glob(args.glob))]
    if not paths:
        fail(f"No configs matched: {args.glob}")

    for path in paths:
        validate_one(path)
        print(f"OK {path}")

    print(f"VALIDATED={len(paths)}")


if __name__ == "__main__":
    main()
