import numpy as np
import os
from typing import Dict, Any, List

class CachedFeatures:
    """Helper class containing cached features and metadata."""
    def __init__(self, data: Dict[str, Any]) -> None:
        self.features = data["features"]
        self.sample_ids = [str(x) for x in data["sample_ids"]]
        self.palm_ids = [str(x) for x in data["palm_ids"]]
        self.subject_ids = [str(x) for x in data["subject_ids"]]
        self.gender = [str(x) for x in data["gender"]]
        self.hand_side = [str(x) for x in data["hand_side"]]
        self.image_paths = [str(x) for x in data["image_paths"]]
        self.split = str(data["split"])
        self.dataset = str(data["dataset"])
        self.config_hash = str(data["config_hash"])

def save_features(
    path: str,
    features: np.ndarray,
    sample_ids: np.ndarray,
    palm_ids: np.ndarray,
    subject_ids: np.ndarray,
    gender: np.ndarray,
    hand_side: np.ndarray,
    image_paths: np.ndarray,
    split: str,
    dataset: str,
    config_hash: str
) -> None:
    """Save features and metadata to an NPZ file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    np.savez(
        path,
        features=features,
        sample_ids=sample_ids,
        palm_ids=palm_ids,
        subject_ids=subject_ids,
        gender=gender,
        hand_side=hand_side,
        image_paths=image_paths,
        split=split,
        dataset=dataset,
        config_hash=config_hash
    )

def load_features(path: str) -> CachedFeatures:
    """Load features and metadata from an NPZ file."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Feature cache file not found: {path}")
    with np.load(path, allow_pickle=True) as data:
        return CachedFeatures(dict(data))

def verify_alignment(
    feat_x: CachedFeatures,
    feat_y: CachedFeatures
) -> None:
    """Assert that two feature caches are perfectly aligned by sample_id."""
    assert len(feat_x.sample_ids) == len(feat_y.sample_ids), (
        f"Length mismatch: X has {len(feat_x.sample_ids)} samples, Y has {len(feat_y.sample_ids)} samples."
    )
    
    assert list(feat_x.sample_ids) == list(feat_y.sample_ids), (
        "Sample ID sequence mismatch between Gabor and Conformer features. Features must be perfectly aligned."
    )
