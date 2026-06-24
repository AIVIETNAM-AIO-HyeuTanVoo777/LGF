from __future__ import annotations

import argparse
import glob
from pathlib import Path
import sys
import yaml


REQUIRED_TOP = ["seed", "device", "save_dir", "dataset", "sampler", "loader", "model", "training"]


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    raise SystemExit(1)


def validate_one(path: Path) -> None:
    cfg = yaml.safe_load(path.read_text(encoding="utf-8"))

    if not isinstance(cfg, dict):
        fail(f"{path}: YAML root is not a mapping")

    for key in REQUIRED_TOP:
        if key not in cfg:
            fail(f"{path}: missing top-level key {key}")

    dataset = cfg["dataset"]
    model = cfg["model"]
    training = cfg["training"]

    if dataset.get("name") != "Tongji":
        fail(f"{path}: dataset.name must be Tongji")

    split_file = Path(dataset.get("split_file", ""))
    if not split_file.exists():
        fail(f"{path}: split_file not found: {split_file}")

    save_dir = str(cfg.get("save_dir", ""))
    if not save_dir.startswith("experiments/"):
        fail(f"{path}: save_dir must start with experiments/: {save_dir}")

    if "subject_disjoint" not in path.name:
        fail(f"{path}: config filename should identify strict split naming with subject_disjoint")

    if "tongji_subject_disjoint" not in save_dir:
        fail(f"{path}: save_dir should identify strict split naming with tongji_subject_disjoint")

    seed = int(cfg["seed"])
    if seed not in {42, 2026, 2705}:
        fail(f"{path}: unexpected seed {seed}")

    if f"seed{seed}" not in path.name:
        fail(f"{path}: filename seed mismatch")

    if f"seed{seed}" not in str(split_file):
        fail(f"{path}: split_file seed mismatch")

    if "s1s2" in path.name and "s1_to_s2" not in str(split_file):
        fail(f"{path}: s1s2 config does not use s1_to_s2 split")
    if "s2s1" in path.name and "s2_to_s1" not in str(split_file):
        fail(f"{path}: s2s1 config does not use s2_to_s1 split")

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

    epochs = int(training.get("epochs", -1))
    if epochs != 60:
        fail(f"{path}: epochs must be 60")

    lr = float(training.get("lr", -1))
    if abs(lr - 0.0001) > 1e-12:
        fail(f"{path}: lr must be 0.0001")

    wd = float(training.get("weight_decay", -1))
    if abs(wd - 0.0001) > 1e-12:
        fail(f"{path}: weight_decay must be 0.0001")

    if int(training.get("grad_accumulation_steps", -1)) != 4:
        fail(f"{path}: grad_accumulation_steps must be 4")

    loss = cfg.get("loss", {}) or {}
    loss_name = str(loss.get("name") or training.get("loss_type") or "combined").lower()
    lambda_supcon = float(training.get("lambda_supcon", -999))

    name = path.name.lower()

    if name.startswith("b0_"):
        if model_name != "ResNet18Baseline":
            fail(f"{path}: B0 must use ResNet18Baseline")
        if loss_name != "combined":
            fail(f"{path}: B0 must use combined loss with lambda_supcon=0")
        if lambda_supcon != 0.0:
            fail(f"{path}: B0 lambda_supcon must be 0.0")

    if name.startswith("b4_"):
        if model_name != "ResNet18Baseline":
            fail(f"{path}: B4 must use ResNet18Baseline")
        if loss_name != "arcface":
            fail(f"{path}: B4 must use arcface")
        if lambda_supcon != 0.0:
            fail(f"{path}: B4 lambda_supcon must be 0.0")

    if name.startswith("b5_"):
        if model_name != "ResNet18BNNeck":
            fail(f"{path}: B5 must use ResNet18BNNeck")
        if loss_name != "combined":
            fail(f"{path}: B5 must use combined loss with lambda_supcon=0")
        if lambda_supcon != 0.0:
            fail(f"{path}: B5 lambda_supcon must be 0.0")

    if name.startswith("b7_"):
        if model_name != "ResNet18BNNeck":
            fail(f"{path}: B7 must use ResNet18BNNeck")
        if loss_name != "arcface":
            fail(f"{path}: B7 must use arcface")
        if abs(lambda_supcon - 0.02) > 1e-12:
            fail(f"{path}: B7 lambda_supcon must be 0.02")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--glob", required=True, help="Config glob pattern")
    args = parser.parse_args()

    paths = [Path(p) for p in sorted(glob.glob(args.glob))]
    if not paths:
        fail(f"No configs matched: {args.glob}")

    for p in paths:
        validate_one(p)
        print(f"OK {p}")

    print(f"VALIDATED={len(paths)}")


if __name__ == "__main__":
    main()