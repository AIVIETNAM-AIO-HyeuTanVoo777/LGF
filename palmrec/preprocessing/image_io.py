import cv2
import numpy as np
from PIL import Image

def read_image(path: str, grayscale: bool = False) -> np.ndarray:
    """Read an image from disk using OpenCV."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Image not found: {path}")
    
    # Read image
    if grayscale:
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise ValueError(f"Could not load image as grayscale: {path}")
    else:
        img = cv2.imread(path, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError(f"Could not load image: {path}")
        # Convert BGR to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
    return img

import os
