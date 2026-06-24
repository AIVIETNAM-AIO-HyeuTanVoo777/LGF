from __future__ import annotations

from pathlib import Path
import yaml


CONFIG_DIR = Path("configs")
SPLIT_DIR = Path("data/splits")

SEEDS = [42, 2026, 2705]
DIRECTIONS = {
    "s1s2": {
        "label": "S1 -> S2",
        "split_pattern": "tongji_subject_disjoint_s1_to_s2_seed{seed}.json",
    },
    "s2s1": {
        "label": "S2 -> S1",
        "split_pattern": "tongji_subject_disjoint_s2_to_s1_seed{seed}.json",
    },
}

COMMON = {
    "device": "cuda",
    "dataset": {"name": "Tongji"},
    "sampler": {
        "num_identities": 8,
        "num_instances": 2,
        "fallback_identities": 4,
    },
    "loader": {"num_workers": 0},
    "training": {
        "epochs": 60,
        "lr": 0.0001,
        "weight_decay": 0.0001,
        "grad_accumulation_steps": 4,
        "temperature": 0.07,
        "amp": True,
    },
}

METHODS = {
    "b0": {
        "title": "B0: ResNet18 + CE",
        "name_stub": "b0_resnet18_ce",
        "model": {
            "name": "ResNet18Baseline",
            "embedding_dim": 256,
            "pretrained": True,
        },
        "loss": {"name": "combined"},
        "training_extra": {
            "loss_type": "combined",
            "lambda_supcon": 0.0,
        },
    },
    "b4": {
        "title": "B4: ResNet18 + ArcFace",
        "name_stub": "b4_resnet18_arcface",
        "model": {
            "name": "ResNet18Baseline",
            "embedding_dim": 256,
            "pretrained": True,
        },
        "loss": {
            "name": "arcface",
            "scale": 30.0,
            "margin": 0.5,
        },
        "training_extra": {
            "loss_type": "arcface",
            "lambda_supcon": 0.0,
        },
    },
    "b5": {
        "title": "B5: ResNet18 + BNNeck + CE",
        "name_stub": "b5_resnet18_bnneck_ce",
        "model": {
            "name": "ResNet18BNNeck",
            "embedding_dim": 256,
            "pretrained": True,
            "eval_embedding": "post_bn",
        },
        "eval": {"embedding": "post_bn"},
        "loss": {"name": "combined"},
        "training_extra": {
            "loss_type": "combined",
            "lambda_supcon": 0.0,
        },
    },
    "b7": {
        "title": "B7: ResNet18 + BNNeck + ArcFace + light SupCon",
        "name_stub": "b7_resnet18_bnneck_arcface_light_supcon",
        "model": {
            "name": "ResNet18BNNeck",
            "embedding_dim": 256,
            "pretrained": True,
            "eval_embedding": "post_bn",
        },
        "eval": {"embedding": "post_bn"},
        "loss": {
            "name": "arcface",
            "scale": 30.0,
            "margin": 0.5,
        },
        "training_extra": {
            "loss_type": "arcface",
            "lambda_supcon": 0.02,
        },
    },
}


def ordered_config(method_key: str, direction_key: str, seed: int) -> dict:
    method = METHODS[method_key]
    direction = DIRECTIONS[direction_key]

    split_file = SPLIT_DIR / direction["split_pattern"].format(seed=seed)
    if not split_file.exists():
        raise FileNotFoundError(split_file)

    save_name = f"{method['name_stub']}_tongji_subject_disjoint_{direction_key}_seed{seed}"

    cfg = {
        "seed": seed,
        "device": COMMON["device"],
        "save_dir": f"experiments/{save_name}",
        "dataset": {
            "name": "Tongji",
            "split_file": split_file.as_posix(),
        },
        "sampler": dict(COMMON["sampler"]),
        "loader": dict(COMMON["loader"]),
        "model": dict(method["model"]),
    }

    if "eval" in method:
        cfg["eval"] = dict(method["eval"])

    cfg["loss"] = dict(method["loss"])

    training = dict(COMMON["training"])
    training.update(method["training_extra"])
    cfg["training"] = training

    return cfg


def write_config(method_key: str, direction_key: str, seed: int) -> Path:
    method = METHODS[method_key]
    path = CONFIG_DIR / f"{method['name_stub']}_tongji_subject_disjoint_{direction_key}_seed{seed}.yaml"

    cfg = ordered_config(method_key, direction_key, seed)

    header = (
        f"# {method['title']} on Tongji palm-class-disjoint {DIRECTIONS[direction_key]['label']}, seed {seed}\n"
        "# Note: filenames retain historical 'subject_disjoint' naming, while the paper claim is capped at palm-class-disjoint by audit.\n"
    )

    text = yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True)
    path.write_text(header + text, encoding="utf-8")
    return path


def main() -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    written = []

    for method_key in ["b0", "b4", "b5", "b7"]:
        for direction_key in ["s1s2", "s2s1"]:
            for seed in SEEDS:
                written.append(write_config(method_key, direction_key, seed))

    print("WROTE_CONFIGS=")
    for p in written:
        print(p.as_posix())
    print(f"TOTAL={len(written)}")


if __name__ == "__main__":
    main()