import numpy as np
from sklearn.metrics.pairwise import rbf_kernel as sklearn_rbf, laplacian_kernel as sklearn_laplacian, cosine_similarity

def cosine_kernel(X: np.ndarray, Y: np.ndarray = None) -> np.ndarray:
    """Compute Cosine kernel matrix."""
    return cosine_similarity(X, Y)

def rbf_kernel(X: np.ndarray, Y: np.ndarray = None, gamma: float = None) -> np.ndarray:
    """Compute RBF (Gaussian) kernel matrix."""
    return sklearn_rbf(X, Y, gamma=gamma)

def laplacian_kernel(X: np.ndarray, Y: np.ndarray = None, gamma: float = None) -> np.ndarray:
    """Compute Laplacian kernel matrix."""
    return sklearn_laplacian(X, Y, gamma=gamma)

def get_kernel_fn(kernel_name: str):
    """Retrieve kernel function by name."""
    name = kernel_name.lower()
    if name == "cosine":
        return cosine_kernel
    elif name == "rbf":
        return rbf_kernel
    elif name == "laplacian":
        return laplacian_kernel
    else:
        raise ValueError(f"Unsupported kernel: {kernel_name}")
