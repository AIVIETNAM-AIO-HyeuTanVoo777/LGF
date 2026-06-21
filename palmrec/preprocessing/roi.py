import numpy as np

class ROIExtractor:
    """Base interface for ROI Extraction."""
    def extract(self, image: np.ndarray) -> np.ndarray:
        raise NotImplementedError("Subclasses must implement ROI extraction.")

class IdentityROIExtractor(ROIExtractor):
    """Default ROI extractor that returns the image unmodified.
    Maps to paper section: Palmprint ROI image preprocessing (assumed already cropped).
    """
    def extract(self, image: np.ndarray) -> np.ndarray:
        return image
