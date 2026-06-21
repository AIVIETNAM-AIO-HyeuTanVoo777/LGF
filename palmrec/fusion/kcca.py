import os
import numpy as np
import scipy.linalg
from sklearn.decomposition import PCA
from sklearn.preprocessing import KernelCenterer
import joblib
from typing import Dict, Any, Tuple
import logging

from .kernels import get_kernel_fn
from palmrec.features.normalization import l2_normalize

logger = logging.getLogger(__name__)

class KCCAFusion:
    """Centered Regularized Kernel Canonical Correlation Analysis (KCCA) Feature Fusion.
    Maps to paper section: KCCA feature fusion.
    """
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        
        # Hyperparameters
        self.kernel_name = config.get("kernel", "cosine")
        self.n_components = int(config.get("n_components", 256))
        self.reg = float(config.get("reg", 1e-3))
        self.center_kernels = config.get("center_kernels", True)
        
        # Pre-reduction configs (PCA to reduce dimensionality before KCCA to prevent OOM)
        self.pre_reduce = config.get("pre_reduce", True)
        self.x_reduce_dim = int(config.get("x_reduce_dim", 1024))
        self.y_reduce_dim = int(config.get("y_reduce_dim", 512))
        
        # Fusion strategy: sum, concat, or weighted_sum
        self.fusion_strategy = config.get("fusion_strategy", "sum")
        self.l2_normalize_output = config.get("l2_normalize_output", True)
        
        # PCA reducers
        self.pca_x = None
        self.pca_y = None
        
        # Centerers
        self.centerer_x = KernelCenterer() if self.center_kernels else None
        self.centerer_y = KernelCenterer() if self.center_kernels else None
        
        # Reference matrices (training references required for projecting new samples)
        self.X_train_ref = None
        self.Y_train_ref = None
        
        # Projection directions (eigenvectors)
        self.alpha = None
        self.beta = None
        
        self.kernel_fn = get_kernel_fn(self.kernel_name)
        self._fitted = False

    def fit(self, X_train: np.ndarray, Y_train: np.ndarray) -> "KCCAFusion":
        """Fit KCCA projection directions on training feature spaces X and Y."""
        logger.info(f"Fitting KCCA with kernel={self.kernel_name}, n_components={self.n_components}, reg={self.reg}...")
        
        # 1. PCA Pre-reduction
        if self.pre_reduce:
            # Fit PCA on X
            x_dim = min(X_train.shape[0], X_train.shape[1], self.x_reduce_dim)
            self.pca_x = PCA(n_components=x_dim, random_state=42)
            X_train_red = self.pca_x.fit_transform(X_train)
            
            # Fit PCA on Y
            y_dim = min(Y_train.shape[0], Y_train.shape[1], self.y_reduce_dim)
            self.pca_y = PCA(n_components=y_dim, random_state=42)
            Y_train_red = self.pca_y.fit_transform(Y_train)
            
            logger.info(f"Pre-reduced X shape from {X_train.shape} to {X_train_red.shape}")
            logger.info(f"Pre-reduced Y shape from {Y_train.shape} to {Y_train_red.shape}")
        else:
            X_train_red = X_train
            Y_train_red = Y_train
            
        # Cache training references
        self.X_train_ref = X_train_red
        self.Y_train_ref = Y_train_red
        
        N = X_train_red.shape[0]
        # Adjust n_components if training sample size is smaller
        self.n_components = min(self.n_components, N)
        
        # 2. Compute Kernel Matrices
        Kx = self.kernel_fn(X_train_red, X_train_red)
        Ky = self.kernel_fn(Y_train_red, Y_train_red)
        
        # 3. Center Kernel Matrices
        if self.center_kernels:
            Kx_c = self.centerer_x.fit_transform(Kx)
            Ky_c = self.centerer_y.fit_transform(Ky)
        else:
            Kx_c = Kx
            Ky_c = Ky
            
        # 4. Formulate generalized eigenvalue problem
        # Rx = Kxc Kxc + reg*I, Ry = Kyc Kyc + reg*I
        # We solve (Rx^-1 Kxc Kyc Ry^-1 Kyc Kxc) alpha = lambda alpha
        # And similarly for beta
        I = np.eye(N)
        Rx = Kx_c @ Kx_c + self.reg * I
        Ry = Ky_c @ Ky_c + self.reg * I
        
        # Compute covariance matrices
        # Rx^-1 Kxc Kyc Ry^-1 Kyc Kxc
        K_xc_yc = Kx_c @ Ky_c
        K_yc_xc = Ky_c @ Kx_c
        
        # Solve generalized eigenvalue problem: 
        # Cxx^-1 Cxy Cyy^-1 Cyx alpha = lambda alpha
        # Cxx = Rx, Cxy = K_xc_yc, Cyy = Ry, Cyx = K_yc_xc
        try:
            A = np.linalg.solve(Rx, K_xc_yc @ np.linalg.solve(Ry, K_yc_xc))
            eigvals, eigvecs = scipy.linalg.eig(A)
            
            # Sort eigenvalues
            idx = np.argsort(np.real(eigvals))[::-1]
            self.alpha = np.real(eigvecs[:, idx[:self.n_components]])
            
            # Solve for beta symmetrically
            B = np.linalg.solve(Ry, K_yc_xc @ np.linalg.solve(Rx, K_xc_yc))
            _, eigvecs_y = scipy.linalg.eig(B)
            self.beta = np.real(eigvecs_y[:, idx[:self.n_components]])
            
        except np.linalg.LinAlgError as e:
            logger.error(f"Numerical solver failed: {e}. Trying pseudo-inverse fallback.")
            Rx_inv = np.linalg.pinv(Rx)
            Ry_inv = np.linalg.pinv(Ry)
            A = Rx_inv @ K_xc_yc @ Ry_inv @ K_yc_xc
            eigvals, eigvecs = scipy.linalg.eig(A)
            idx = np.argsort(np.real(eigvals))[::-1]
            self.alpha = np.real(eigvecs[:, idx[:self.n_components]])
            
            B = Ry_inv @ K_yc_xc @ Rx_inv @ K_xc_yc
            _, eigvecs_y = scipy.linalg.eig(B)
            self.beta = np.real(eigvecs_y[:, idx[:self.n_components]])

        # Normalize projection vectors to ensure component variances are scale-independent
        self.alpha = self.alpha / (np.linalg.norm(Kx_c @ self.alpha, axis=0, keepdims=True) + 1e-12)
        self.beta = self.beta / (np.linalg.norm(Ky_c @ self.beta, axis=0, keepdims=True) + 1e-12)
        
        self._fitted = True
        logger.info("Successfully completed KCCA fit.")
        return self

    def transform(self, X: np.ndarray, Y: np.ndarray) -> np.ndarray:
        """Project input spaces X and Y into canonical space and fuse them."""
        if not self._fitted:
            raise ValueError("KCCA model has not been fitted yet.")
            
        # 1. Apply pre-reduction PCA
        if self.pre_reduce:
            X_red = self.pca_x.transform(X)
            Y_red = self.pca_y.transform(Y)
        else:
            X_red = X
            Y_red = Y
            
        # 2. Compute Kernels against training reference
        Kx = self.kernel_fn(X_red, self.X_train_ref) # [M, N] where M is num_samples, N is num_train
        Ky = self.kernel_fn(Y_red, self.Y_train_ref)
        
        # 3. Center Kernels using training statistics
        if self.center_kernels:
            Kx_c = self.centerer_x.transform(Kx)
            Ky_c = self.centerer_y.transform(Ky)
        else:
            Kx_c = Kx
            Ky_c = Ky
            
        # 4. Project
        U = Kx_c @ self.alpha # [M, n_components]
        V = Ky_c @ self.beta  # [M, n_components]
        
        # 5. Fuse
        if self.fusion_strategy == "sum":
            Z = U + V
        elif self.fusion_strategy == "concat":
            Z = np.concatenate([U, V], axis=1)
        elif self.fusion_strategy == "weighted_sum":
            # Default weight = 0.5 for equal contribution
            Z = 0.5 * U + 0.5 * V
        else:
            raise ValueError(f"Unknown fusion strategy: {self.fusion_strategy}")
            
        # 6. Normalize
        if self.l2_normalize_output:
            Z = l2_normalize(Z)
            
        return Z

    def transform_single(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Project a single sample pair (x, y) into fused space.
        Inputs: 1D arrays of shapes [D_x] and [D_y].
        """
        # Reshape to 2D arrays
        X = x.reshape(1, -1)
        Y = y.reshape(1, -1)
        
        Z = self.transform(X, Y)
        return Z.flatten()

    def save(self, path: str) -> None:
        """Save KCCA model to path."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(self, path)
        logger.info(f"Saved KCCA model checkpoint to {path}")

    @classmethod
    def load(cls, path: str) -> "KCCAFusion":
        """Load KCCA model from path."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"KCCA checkpoint not found: {path}")
        model = joblib.load(path)
        logger.info(f"Loaded KCCA model from {path}")
        return model
