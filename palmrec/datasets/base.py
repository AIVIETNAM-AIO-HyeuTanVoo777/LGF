import torch
from torch.utils.data import Dataset
from PIL import Image
import pandas as pd
import os
from typing import Dict, Any, Callable

class PalmprintDataset(Dataset):
    """PyTorch Dataset for Palmprint Recognition matching spec.
    Maps to paper section: Dataset & preprocessing.
    """
    def __init__(
        self,
        metadata: pd.DataFrame,
        transform: Callable[[Image.Image], torch.Tensor] = None,
        image_loader: Callable[[str], Image.Image] = None
    ) -> None:
        self.metadata = metadata.reset_index(drop=True)
        self.transform = transform
        
        # Default image loader using PIL
        if image_loader is None:
            self.image_loader = lambda path: Image.open(path).convert("RGB")
        else:
            self.image_loader = image_loader

    def __len__(self) -> int:
        return len(self.metadata)

    def __getitem__(self, idx: int) -> Dict[str, Any]:
        row = self.metadata.iloc[idx]
        image_path = row["image_path"]
        
        # Load image
        image = self.image_loader(image_path)
        
        # Apply transform if provided
        if self.transform:
            image_tensor = self.transform(image)
        else:
            # Fallback to simple tensor conversion
            from torchvision.transforms import functional as F
            image_tensor = F.to_tensor(image)

        return {
            "image": image_tensor,
            "label": int(row["class_id"]),
            "sample_id": str(row["sample_id"]),
            "subject_id": str(row["subject_id"]),
            "palm_id": str(row["palm_id"]),
            "gender": str(row["gender"]),
            "hand_side": str(row["hand_side"]),
            "image_path": str(image_path),
        }
