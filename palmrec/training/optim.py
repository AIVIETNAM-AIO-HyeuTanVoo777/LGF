import torch
import torch.nn as nn
from typing import Dict, Any

def get_optimizer(
    model: nn.Module,
    config: Dict[str, Any]
) -> torch.optim.Optimizer:
    """Create optimizer based on configuration.
    Default in paper is Adam with lr=1e-5.
    """
    opt_name = config.get("optimizer", "adam").lower()
    lr = float(config.get("lr", 1e-5))
    weight_decay = float(config.get("weight_decay", 0.0))
    
    if opt_name == "adam":
        return torch.optim.Adam(
            model.parameters(),
            lr=lr,
            weight_decay=weight_decay
        )
    elif opt_name == "sgd":
        return torch.optim.SGD(
            model.parameters(),
            lr=lr,
            momentum=0.9,
            weight_decay=weight_decay
        )
    else:
        raise ValueError(f"Unsupported optimizer: {opt_name}")
