import cv2
import numpy as np
import torch
import torch.nn.functional as F
from typing import List, Dict, Any, Union
import logging

logger = logging.getLogger(__name__)

class GaborFeatureExtractor:
    """Multi-scale, multi-orientation Gabor filter bank extractor.
    Maps to paper section: Gabor feature extraction.
    """
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        
        # Load parameters
        self.image_size = tuple(config.get("image_size", [224, 224]))
        self.num_scales = int(config.get("num_scales", 7))
        
        # Convert orientation degrees to radians
        orientations_deg = config.get("orientations_deg", [0, 30, 60, 90, 120, 150])
        self.orientations = [np.deg2rad(d) for d in orientations_deg]
        
        # Assumptions/parameters
        self.kernel_size = int(config.get("kernel_size", 31))
        self.sigma = float(config.get("sigma", 4.0))
        self.gamma = float(config.get("gamma", 0.5))
        self.phase_offset = float(config.get("phase_offset", 0.0))
        self.kmax = float(config.get("kmax", np.pi / 2))
        self.spacing_factor = float(config.get("spacing_factor", np.sqrt(2)))
        self.response_mode = config.get("response_mode", "magnitude")
        self.orientation_fusion = config.get("orientation_fusion", "max")
        self.scale_fusion = config.get("scale_fusion", "concat")
        
        # Optional pooling
        self.pooling_config = config.get("pooling", {"enabled": False})
        
        # Build filter bank
        self.filter_bank = self.build_filter_bank()

    def build_filter_bank(self) -> List[List[np.ndarray]]:
        """Construct filter bank of shape [num_scales, num_orientations, K, K].
        Uses Gabor frequency schedule to define wavelengths.
        """
        filter_bank = []
        for v in range(self.num_scales):
            scale_filters = []
            # Calculate wave vector magnitude k_v and corresponding wavelength lambda_v
            # k_v = kmax / (spacing_factor^v)
            kv = self.kmax / (self.spacing_factor ** v)
            lambd = (2 * np.pi) / kv
            
            for theta in self.orientations:
                # Construct real Gabor filter
                kernel = cv2.getGaborKernel(
                    ksize=(self.kernel_size, self.kernel_size),
                    sigma=self.sigma,
                    theta=theta,
                    lambd=lambd,
                    gamma=self.gamma,
                    psi=self.phase_offset,
                    ktype=cv2.CV_32F
                )
                
                # Normalize kernel to avoid scaling bias
                kernel /= np.linalg.norm(kernel) + 1e-12
                scale_filters.append(kernel)
            filter_bank.append(scale_filters)
            
        return filter_bank

    def extract_maps(self, gray_roi: np.ndarray) -> np.ndarray:
        """Extract multi-scale feature maps from 2D grayscale ROI.
        Returns: np.ndarray of shape [num_scales, H, W] after orientation max-fusion.
        """
        assert len(gray_roi.shape) == 2, "Gabor input must be a 2D grayscale image."
        assert gray_roi.shape == self.image_size, f"Input size {gray_roi.shape} != expected image_size {self.image_size}"
        
        scale_maps = []
        for v in range(self.num_scales):
            orientation_responses = []
            for u, theta in enumerate(self.orientations):
                kernel = self.filter_bank[v][u]
                # Convolve using same padding
                response = cv2.filter2D(gray_roi, cv2.CV_32F, kernel, borderType=cv2.BORDER_REPLICATE)
                
                if self.response_mode == "magnitude":
                    response = np.abs(response)
                    
                orientation_responses.append(response)
                
            # Perform orientation fusion (e.g. pixel-wise max)
            if self.orientation_fusion == "max":
                fused_map = np.max(orientation_responses, axis=0)
            elif self.orientation_fusion == "mean":
                fused_map = np.mean(orientation_responses, axis=0)
            else:
                raise ValueError(f"Unknown orientation fusion: {self.orientation_fusion}")
                
            scale_maps.append(fused_map)
            
        scale_maps_arr = np.stack(scale_maps, axis=0) # [num_scales, H, W]
        return scale_maps_arr

    def extract(self, gray_roi: np.ndarray) -> np.ndarray:
        """Extract flat Gabor feature vector from 2D grayscale ROI.
        Handles optional pooling and scale-fusion.
        Returns: 1D np.ndarray feature vector.
        """
        # 1. Get multi-scale maps
        maps = self.extract_maps(gray_roi) # [num_scales, H, W]
        
        # 2. Perform pooling if enabled
        if self.pooling_config.get("enabled", False):
            # Convert to PyTorch tensor to use adaptive pooling
            maps_tensor = torch.from_numpy(maps).unsqueeze(0) # [1, num_scales, H, W]
            out_size = tuple(self.pooling_config.get("output_size", [28, 28]))
            pool_type = self.pooling_config.get("type", "adaptive_avg")
            
            if pool_type == "adaptive_avg":
                pooled = F.adaptive_avg_pool2d(maps_tensor, out_size)
            elif pool_type == "adaptive_max":
                pooled = F.adaptive_max_pool2d(maps_tensor, out_size)
            else:
                raise ValueError(f"Unknown pooling type: {pool_type}")
                
            maps = pooled.squeeze(0).numpy() # [num_scales, out_h, out_w]
            
        # 3. Perform scale fusion
        if self.scale_fusion == "concat":
            features = maps.flatten()
        elif self.scale_fusion == "max":
            features = np.max(maps, axis=0).flatten()
        elif self.scale_fusion == "mean":
            features = np.mean(maps, axis=0).flatten()
        else:
            raise ValueError(f"Unknown scale fusion: {self.scale_fusion}")
            
        return features
