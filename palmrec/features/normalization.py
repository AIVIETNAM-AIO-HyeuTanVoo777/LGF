import numpy as np
from sklearn.preprocessing import StandardScaler
from typing import Tuple, Optional

def l2_normalize(features: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    """Perform L2 normalization along the last dimension (samples, features)."""
    if len(features.shape) == 1:
        norm = np.linalg.norm(features)
        return features / (norm + eps)
    else:
        norm = np.linalg.norm(features, axis=1, keepdims=True)
        return features / (norm + eps)

class FeatureNormalizer:
    """Fits StandardScaler on train set and scales features, followed by L2 normalization."""
    def __init__(self, standardize: bool = True, l2: bool = True) -> None:
        self.standardize = standardize
        self.l2 = l2
        self.scaler = StandardScaler() if standardize else None
        self._fitted = False

    def fit(self, X_train: np.ndarray) -> "FeatureNormalizer":
        """Fit standardizer on training features."""
        if self.standardize:
            self.scaler.fit(X_train)
        self._fitted = True
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        """Apply standardization and L2 normalization."""
        X_out = X.copy().astype(np.float32)
        if self.standardize:
            if not self._fitted:
                raise ValueError("Normalizer must be fit before calling transform.")
            X_out = self.scaler.transform(X_out)
        if self.l2:
            X_out = l2_normalize(X_out)
        return X_out

    def fit_transform(self, X_train: np.ndarray) -> np.ndarray:
        """Fit and transform training features."""
        return self.fit(X_train).transform(X_train)
