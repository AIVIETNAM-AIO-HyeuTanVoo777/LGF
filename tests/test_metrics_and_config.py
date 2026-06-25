from __future__ import annotations

from pathlib import Path

import numpy as np

from palmrec.evaluation.metrics import calculate_eer, conservative_tar_at_far
from palmrec.utils.config import load_config


def test_conservative_tar_never_exceeds_target_far():
    result = conservative_tar_at_far(
        genuine_scores=np.array([0.95, 0.90, 0.85]),
        impostor_scores=np.array([0.70, 0.40, 0.10]),
        target_far=0.0,
    )

    assert result["empirical_far"] <= result["target_far"]
    assert result["tar"] == 1.0


def test_eer_sanity_for_separated_scores():
    eer, threshold = calculate_eer([0.9, 0.8], [0.2, 0.1])

    assert eer == 0.0
    assert 0.2 <= threshold <= 0.9


def test_rankb_config_loads():
    cfg = load_config("configs/rankb_final/m6_resnet18_bnneck_arcface_tongji_s1s2_seed42.yaml")

    assert cfg.dataset.name == "Tongji"
    assert cfg.protocol.direction == "s1_to_s2"
    assert cfg.model.name == "ResNet18BNNeck"
    assert Path(cfg.dataset.split_file).exists()
