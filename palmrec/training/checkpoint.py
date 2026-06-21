import os
import torch
from typing import Dict, Any, Optional

def save_checkpoint(
    state: Dict[str, Any],
    checkpoint_dir: str,
    filename: str = "best_conformer.pt"
) -> None:
    """Save training checkpoint to disk."""
    os.makedirs(checkpoint_dir, exist_ok=True)
    filepath = os.path.join(checkpoint_dir, filename)
    torch.save(state, filepath)

def load_checkpoint(
    filepath: str,
    device: torch.device = torch.device("cpu")
) -> Dict[str, Any]:
    """Load training checkpoint from disk."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Checkpoint not found at: {filepath}")
    return torch.load(filepath, map_location=device, weights_only=False)
