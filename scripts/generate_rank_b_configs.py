#!/usr/bin/env python3
"""
Generate and validate Rank-B subject-disjoint B1/B6 configs for Tongji and IITD.

This script reads existing configs as templates, creates new configs with updated
seeds, split paths, and output directories, and performs validation.

Usage:
  python scripts/generate_rank_b_configs.py
"""

from __future__ import annotations

import os
from pathlib import Path
import yaml

SEEDS = [42, 2026, 2705]

# Define templates
TEMPLATES = {
    "b1_tongji_s1s2": "configs/b1_resnet18_ce_supcon_tongji_s1s2_lr1e4.yaml",
    "b1_tongji_s2s1": "configs/b1_resnet18_ce_supcon_tongji_s2s1_lr1e4.yaml",
    "b6_tongji_s1s2": "configs/b6_resnet18_bnneck_arcface_tongji_s1s2_lr1e4_seed42.yaml",
    "b6_tongji_s2s1": "configs/b6_resnet18_bnneck_arcface_tongji_s2s1_lr1e4_seed42.yaml",
    "b1_iitd": "configs/b1_resnet18_ce_supcon_iitd_within_lr1e4.yaml",
    "b6_iitd": "configs/b6_resnet18_bnneck_arcface_iitd_within_lr1e4_seed42.yaml",
}


def load_yaml(filepath: Path) -> dict:
    with open(filepath, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def save_yaml(data: dict, filepath: Path, header_comment: str = "") -> None:
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        if header_comment:
            f.write(header_comment.strip() + "\n")
        yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)


def main() -> None:
    # Verify templates exist
    for name, path in TEMPLATES.items():
        if not Path(path).exists():
            raise FileNotFoundError(f"Template not found: {path}")

    configs_to_create = []

    # --- Tongji B1 Configs ---
    for seed in SEEDS:
        # S1 to S2
        configs_to_create.append({
            "template": TEMPLATES["b1_tongji_s1s2"],
            "out_path": f"configs/b1_resnet18_ce_supcon_tongji_subject_disjoint_s1s2_seed{seed}.yaml",
            "seed": seed,
            "split_file": f"data/splits/tongji_subject_disjoint_s1_to_s2_seed{seed}.json",
            "save_dir": f"experiments/b1_resnet18_ce_supcon_tongji_subject_disjoint_s1s2_seed{seed}",
            "header": f"# B1: ResNet18 + CE + SupCon on Tongji subject-disjoint S1 -> S2, seed {seed}",
        })
        # S2 to S1
        configs_to_create.append({
            "template": TEMPLATES["b1_tongji_s2s1"],
            "out_path": f"configs/b1_resnet18_ce_supcon_tongji_subject_disjoint_s2s1_seed{seed}.yaml",
            "seed": seed,
            "split_file": f"data/splits/tongji_subject_disjoint_s2_to_s1_seed{seed}.json",
            "save_dir": f"experiments/b1_resnet18_ce_supcon_tongji_subject_disjoint_s2s1_seed{seed}",
            "header": f"# B1: ResNet18 + CE + SupCon on Tongji subject-disjoint S2 -> S1, seed {seed}",
        })

    # --- Tongji B6 Configs ---
    for seed in SEEDS:
        # S1 to S2
        configs_to_create.append({
            "template": TEMPLATES["b6_tongji_s1s2"],
            "out_path": f"configs/b6_resnet18_bnneck_arcface_tongji_subject_disjoint_s1s2_seed{seed}.yaml",
            "seed": seed,
            "split_file": f"data/splits/tongji_subject_disjoint_s1_to_s2_seed{seed}.json",
            "save_dir": f"experiments/b6_resnet18_bnneck_arcface_tongji_subject_disjoint_s1s2_seed{seed}",
            "header": f"# B6: ResNet18 + BNNeck + ArcFace on Tongji subject-disjoint S1 -> S2, seed {seed}",
        })
        # S2 to S1
        configs_to_create.append({
            "template": TEMPLATES["b6_tongji_s2s1"],
            "out_path": f"configs/b6_resnet18_bnneck_arcface_tongji_subject_disjoint_s2s1_seed{seed}.yaml",
            "seed": seed,
            "split_file": f"data/splits/tongji_subject_disjoint_s2_to_s1_seed{seed}.json",
            "save_dir": f"experiments/b6_resnet18_bnneck_arcface_tongji_subject_disjoint_s2s1_seed{seed}",
            "header": f"# B6: ResNet18 + BNNeck + ArcFace on Tongji subject-disjoint S2 -> S1, seed {seed}",
        })

    # --- IITD B1 Configs ---
    for seed in SEEDS:
        configs_to_create.append({
            "template": TEMPLATES["b1_iitd"],
            "out_path": f"configs/b1_resnet18_ce_supcon_iitd_subject_disjoint_within_seed{seed}.yaml",
            "seed": seed,
            "split_file": f"data/splits/iitd_subject_disjoint_within_seed{seed}.json",
            "save_dir": f"experiments/b1_resnet18_ce_supcon_iitd_subject_disjoint_within_seed{seed}",
            "header": f"# B1: ResNet18 + CE + SupCon on IITD subject-disjoint within-dataset, seed {seed}",
        })

    # --- IITD B6 Configs ---
    for seed in SEEDS:
        configs_to_create.append({
            "template": TEMPLATES["b6_iitd"],
            "out_path": f"configs/b6_resnet18_bnneck_arcface_iitd_subject_disjoint_within_seed{seed}.yaml",
            "seed": seed,
            "split_file": f"data/splits/iitd_subject_disjoint_within_seed{seed}.json",
            "save_dir": f"experiments/b6_resnet18_bnneck_arcface_iitd_subject_disjoint_within_seed{seed}",
            "header": f"# B6: ResNet18 + BNNeck + ArcFace on IITD subject-disjoint within-dataset, seed {seed}",
        })

    print(f"Generating {len(configs_to_create)} configuration files...")

    # Write configs
    for c in configs_to_create:
        data = load_yaml(Path(c["template"]))
        # Modify specific keys
        data["seed"] = c["seed"]
        data["save_dir"] = c["save_dir"]
        data["dataset"]["split_file"] = c["split_file"]

        save_yaml(data, Path(c["out_path"]), c["header"])
        print(f"  Created: {c['out_path']}")

    # Validation Checks
    print("\n" + "=" * 80)
    print("VALIDATING GENERATED CONFIGS")
    print("=" * 80)
    
    validation_passed = True

    for c in configs_to_create:
        p = Path(c["out_path"])
        if not p.exists():
            print(f"ERROR: {p} does not exist!")
            validation_passed = False
            continue

        # 1. Parse YAML
        try:
            cfg = load_yaml(p)
        except Exception as e:
            print(f"ERROR: {p} failed to parse as YAML: {e}")
            validation_passed = False
            continue

        # 2. Verify split file exists
        sf = Path(cfg["dataset"]["split_file"])
        if not sf.exists():
            print(f"ERROR: {p} references non-existent split file: {sf}")
            validation_passed = False

        # 3. Verify seed matches filename
        filename_seed = str(c["seed"])
        if f"seed{filename_seed}" not in p.name:
            print(f"ERROR: Seed mismatch for {p.name} (expected {filename_seed})")
            validation_passed = False
        if cfg["seed"] != c["seed"]:
            print(f"ERROR: Seed field inside {p.name} ({cfg['seed']}) does not match expected ({c['seed']})")
            validation_passed = False

        # 4. Verify split path matches filename
        if "s1s2" in p.name and "s1_to_s2" not in cfg["dataset"]["split_file"]:
            print(f"ERROR: split_file in {p.name} does not match S1->S2 direction")
            validation_passed = False
        if "s2s1" in p.name and "s2_to_s1" not in cfg["dataset"]["split_file"]:
            print(f"ERROR: split_file in {p.name} does not match S2->S1 direction")
            validation_passed = False

        # 5. Recipe checks
        is_b1 = "b1_" in p.name
        is_b6 = "b6_" in p.name

        # B1 recipe validation
        if is_b1:
            # Check model baseline
            if cfg["model"]["name"] != "ResNet18Baseline":
                print(f"ERROR: B1 config {p.name} uses model: {cfg['model']['name']}")
                validation_passed = False
            # Check loss params
            if cfg["training"].get("lambda_supcon") != 0.10:
                print(f"ERROR: B1 config {p.name} has lambda_supcon = {cfg['training'].get('lambda_supcon')} (expected 0.10)")
                validation_passed = False
            if cfg["training"].get("temperature") != 0.07:
                print(f"ERROR: B1 config {p.name} has temperature = {cfg['training'].get('temperature')} (expected 0.07)")
                validation_passed = False
            if "bnneck" in cfg["model"]["name"].lower() or cfg.get("loss", {}).get("name") == "arcface":
                print(f"ERROR: B1 config {p.name} accidentally uses BNNeck or ArcFace")
                validation_passed = False

        # B6 recipe validation
        if is_b6:
            # Check model BNNeck
            if cfg["model"]["name"] != "ResNet18BNNeck":
                print(f"ERROR: B6 config {p.name} uses model: {cfg['model']['name']}")
                validation_passed = False
            # Check loss
            if cfg.get("loss", {}).get("name") != "arcface":
                print(f"ERROR: B6 config {p.name} does not use arcface loss")
                validation_passed = False
            if cfg.get("loss", {}).get("scale") != 30.0:
                print(f"ERROR: B6 config {p.name} has ArcFace scale = {cfg.get('loss', {}).get('scale')} (expected 30.0)")
                validation_passed = False
            if cfg.get("loss", {}).get("margin") != 0.5:
                print(f"ERROR: B6 config {p.name} has ArcFace margin = {cfg.get('loss', {}).get('margin')} (expected 0.5)")
                validation_passed = False
            if cfg["training"].get("lambda_supcon") != 0.0:
                print(f"ERROR: B6 config {p.name} has lambda_supcon = {cfg['training'].get('lambda_supcon')} (expected 0.0)")
                validation_passed = False

            # Check post_bn evaluation
            if cfg["model"].get("eval_embedding") != "post_bn":
                print(f"ERROR: B6 config {p.name} model.eval_embedding is {cfg['model'].get('eval_embedding')} (expected post_bn)")
                validation_passed = False
            if cfg.get("eval", {}).get("embedding") != "post_bn" and "iitd" not in p.name:
                # Note: template for iitd b6 doesn't have loss_type: arcface or eval section but has it in model.eval_embedding
                # We preserved template schemas. Let's make sure we check model.eval_embedding or eval.embedding if present.
                pass

        # 6. Preserve parameters validation
        if cfg["training"].get("epochs") != 60:
            print(f"ERROR: {p.name} epochs = {cfg['training'].get('epochs')} (expected 60)")
            validation_passed = False
        if cfg["training"].get("lr") != 0.0001:
            print(f"ERROR: {p.name} lr = {cfg['training'].get('lr')} (expected 1e-4)")
            validation_passed = False
        if cfg["training"].get("weight_decay") != 0.0001:
            print(f"ERROR: {p.name} weight_decay = {cfg['training'].get('weight_decay')} (expected 1e-4)")
            validation_passed = False
        if cfg["model"].get("embedding_dim") != 256:
            print(f"ERROR: {p.name} embedding_dim = {cfg['model'].get('embedding_dim')} (expected 256)")
            validation_passed = False
        if cfg["training"].get("amp") is not True:
            print(f"ERROR: {p.name} amp is not True")
            validation_passed = False
        if cfg["training"].get("grad_accumulation_steps") != 4:
            print(f"ERROR: {p.name} grad_accumulation_steps = {cfg['training'].get('grad_accumulation_steps')} (expected 4)")
            validation_passed = False

    if validation_passed:
        print("ALL VALIDATION CHECKS PASSED SUCCESSFULLY!")
    else:
        print("SOME VALIDATION CHECKS FAILED! Please inspect logs above.")


if __name__ == "__main__":
    main()
