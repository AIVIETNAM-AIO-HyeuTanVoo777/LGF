import torch
from torch.optim.lr_scheduler import CosineAnnealingLR, StepLR
from typing import Dict, Any

def get_scheduler(
    optimizer: torch.optim.Optimizer,
    config: Dict[str, Any]
) -> Any:
    """Create learning rate scheduler based on configuration.
    Default in paper is cosine annealing with T_max=epochs, eta_min=5e-7.
    """
    sched_name = config.get("scheduler", "cosine_annealing").lower()
    epochs = int(config.get("epochs", 100))
    min_lr = float(config.get("min_lr", 5e-7))
    
    if sched_name == "cosine_annealing":
        return CosineAnnealingLR(
            optimizer,
            T_max=epochs,
            eta_min=min_lr
        )
    elif sched_name == "step":
        return StepLR(
            optimizer,
            step_size=int(config.get("step_size", 30)),
            gamma=float(config.get("gamma", 0.1))
        )
    else:
        # Return a dummy scheduler if None
        return torch.optim.lr_scheduler.LambdaLR(optimizer, lambda epoch: 1.0)
