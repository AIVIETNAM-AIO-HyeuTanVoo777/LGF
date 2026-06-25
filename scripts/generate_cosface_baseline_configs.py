from __future__ import annotations

from pathlib import Path
import yaml


ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / "configs"

SEEDS = [42, 2026, 2705]

DIRECTIONS = {
    "s1s2": {
        "label": "S1 -> S2",
        "split_template": "data/splits/tongji_subject_disjoint_s1_to_s2_seed{seed}.json",
    },
    "s2s1": {
        "label": "S2 -> S1",
        "split_template": "data/splits/tongji_subject_disjoint_s2_to_s1_seed{seed}.json",
    },
}


def make_config(seed: int, direction_key: str, direction: dict[str, str]) -> dict:
    run_name = f"b8_resnet18_cosface_tongji_subject_disjoint_{direction_key}_seed{seed}"

    return {
        "seed": seed,
        "device": "cuda",
        "save_dir": f"experiments/{run_name}",
        "dataset": {
            "name": "Tongji",
            "split_file": direction["split_template"].format(seed=seed),
        },
        "sampler": {
            "num_identities": 8,
            "num_instances": 2,
            "fallback_identities": 4,
        },
        "loader": {
            "num_workers": 0,
        },
        "model": {
            "name": "ResNet18Baseline",
            "embedding_dim": 256,
            "pretrained": True,
        },
        "loss": {
            "name": "cosface",
            "scale": 30.0,
            "margin": 0.35,
        },
        "training": {
            "loss_type": "cosface",
            "epochs": 60,
            "lr": 0.0001,
            "weight_decay": 0.0001,
            "grad_accumulation_steps": 4,
            "lambda_supcon": 0.0,
            "temperature": 0.07,
            "amp": True,
        },
    }


def main() -> None:
    generated = []

    for seed in SEEDS:
        for direction_key, direction in DIRECTIONS.items():
            cfg = make_config(seed, direction_key, direction)
            path = CONFIG_DIR / f"b8_resnet18_cosface_tongji_subject_disjoint_{direction_key}_seed{seed}.yaml"

            header = (
                f"# B8: ResNet18 + CosFace on Tongji palm-class-disjoint "
                f"{direction['label']}, seed {seed}\n"
            )
            text = header + yaml.safe_dump(cfg, sort_keys=False)
            path.write_text(text, encoding="utf-8")
            generated.append(path)

    print("Generated CosFace baseline configs:")
    for path in generated:
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
