import os
import torch
import numpy as np
import random
from palmrec.utils.config import load_config
from palmrec.utils.seed import set_seed

def test_config_load():
    # Test that default config loads correctly
    config_path = "configs/default.yaml"
    assert os.path.exists(config_path), "default.yaml must exist"
    config = load_config(config_path)
    assert config.project.name == "palm_gabor_conformer"
    assert config.project.seed == 42
    assert config.gabor.num_scales == 7

def test_seed_determinism():
    # Test that setting seed makes random processes deterministic
    set_seed(42)
    r1 = random.random()
    n1 = np.random.rand()
    t1 = torch.rand(1).item()

    set_seed(42)
    r2 = random.random()
    n2 = np.random.rand()
    t2 = torch.rand(1).item()

    assert r1 == r2
    assert n1 == n2
    assert t1 == t2
