import cv2
import numpy as np
import torch
from torchvision import transforms
from PIL import Image
from typing import Tuple, Optional
from .roi import ROIExtractor, IdentityROIExtractor

def preprocess_for_gabor(
    image: np.ndarray,
    roi_extractor: ROIExtractor,
    target_size: Tuple[int, int] = (224, 224)
) -> np.ndarray:
    """Preprocess image for Gabor branch.
    Input image: np.ndarray (RGB or Grayscale).
    Returns: 2D float32 numpy array [H, W] normalized to [0, 1].
    """
    # 1. Apply ROI extractor
    roi = roi_extractor.extract(image)
    
    # 2. Convert to grayscale if it is RGB/BGR
    if len(roi.shape) == 3:
        if roi.shape[2] == 3:
            roi_gray = cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY)
        elif roi.shape[2] == 4:
            roi_gray = cv2.cvtColor(roi, cv2.COLOR_RGBA2GRAY)
        else:
            roi_gray = roi[:, :, 0]
    else:
        roi_gray = roi
        
    # 3. Resize to target size
    if roi_gray.shape[:2] != target_size:
        roi_gray = cv2.resize(roi_gray, target_size, interpolation=cv2.INTER_LINEAR)
        
    # 4. Convert to float32 and normalize to [0, 1]
    roi_gray = roi_gray.astype(np.float32) / 255.0
    
    return roi_gray

def preprocess_for_conformer(
    image: np.ndarray,
    roi_extractor: ROIExtractor,
    target_size: Tuple[int, int] = (224, 224),
    mean: Tuple[float, float, float] = (0.485, 0.456, 0.406),
    std: Tuple[float, float, float] = (0.229, 0.224, 0.225)
) -> torch.Tensor:
    """Preprocess image for Conformer branch.
    Input image: np.ndarray (RGB or Grayscale).
    Returns: torch.Tensor [3, H, W] normalized with mean and std.
    """
    # 1. Apply ROI extractor
    roi = roi_extractor.extract(image)
    
    # 2. Convert to RGB if it is Grayscale
    if len(roi.shape) == 2:
        roi_rgb = cv2.cvtColor(roi, cv2.COLOR_GRAY2RGB)
    elif len(roi.shape) == 3:
        if roi.shape[2] == 4:
            roi_rgb = cv2.cvtColor(roi, cv2.COLOR_RGBA2RGB)
        else:
            roi_rgb = roi
    else:
        raise ValueError(f"Unexpected image shape: {roi.shape}")
        
    # 3. Resize to target size
    if roi_rgb.shape[:2] != target_size:
        roi_rgb = cv2.resize(roi_rgb, target_size, interpolation=cv2.INTER_LINEAR)
        
    # 4. Convert to float32 and scale to [0, 1]
    roi_rgb = roi_rgb.astype(np.float32) / 255.0
    
    # 5. Transpose to [C, H, W] and convert to tensor
    tensor = torch.from_numpy(roi_rgb.transpose(2, 0, 1))
    
    # 6. Normalize with mean and std
    mean_tensor = torch.tensor(mean, dtype=torch.float32).view(3, 1, 1)
    std_tensor = torch.tensor(std, dtype=torch.float32).view(3, 1, 1)
    
    tensor = (tensor - mean_tensor) / std_tensor
    
    return tensor

class ConformerTransform:
    """PyTorch wrapper transform for the Conformer branch."""
    def __init__(
        self,
        roi_extractor: ROIExtractor,
        target_size: Tuple[int, int] = (224, 224),
        mean: Tuple[float, float, float] = (0.485, 0.456, 0.406),
        std: Tuple[float, float, float] = (0.229, 0.224, 0.225)
    ) -> None:
        self.roi_extractor = roi_extractor
        self.target_size = target_size
        self.mean = mean
        self.std = std

    def __call__(self, img: Image.Image) -> torch.Tensor:
        # Convert PIL image to numpy RGB
        img_np = np.array(img.convert("RGB"))
        return preprocess_for_conformer(
            img_np,
            self.roi_extractor,
            self.target_size,
            self.mean,
            self.std
        )
