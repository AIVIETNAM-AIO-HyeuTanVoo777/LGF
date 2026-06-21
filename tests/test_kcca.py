import numpy as np
import pytest
import os
from palmrec.fusion.kernels import cosine_kernel, rbf_kernel, laplacian_kernel
from palmrec.fusion.kcca import KCCAFusion

def test_kernels_shapes():
    X = np.random.randn(4, 10)
    Y = np.random.randn(3, 10)
    
    # Cosine
    K_cos = cosine_kernel(X, Y)
    assert K_cos.shape == (4, 3)
    
    # RBF
    K_rbf = rbf_kernel(X, Y, gamma=0.1)
    assert K_rbf.shape == (4, 3)
    
    # Laplacian
    K_lap = laplacian_kernel(X, Y, gamma=0.1)
    assert K_lap.shape == (4, 3)

def test_kcca_fit_transform_shapes():
    # Fit KCCA on dummy features
    X_train = np.random.randn(10, 20)
    Y_train = np.random.randn(10, 15)
    
    X_test = np.random.randn(5, 20)
    Y_test = np.random.randn(5, 15)
    
    config = {
        "kernel": "cosine",
        "n_components": 4,
        "reg": 1e-3,
        "center_kernels": True,
        "pre_reduce": False,
        "fusion_strategy": "sum",
        "l2_normalize_output": True
    }
    
    kcca = KCCAFusion(config)
    kcca.fit(X_train, Y_train)
    
    # Check projection weights shapes
    assert kcca.alpha.shape == (10, 4)
    assert kcca.beta.shape == (10, 4)
    
    # Transform
    fused_train = kcca.transform(X_train, Y_train)
    fused_test = kcca.transform(X_test, Y_test)
    
    assert fused_train.shape == (10, 4)
    assert fused_test.shape == (5, 4)

def test_kcca_fusion_strategies():
    X_train = np.random.randn(8, 20)
    Y_train = np.random.randn(8, 15)
    
    # Test concat strategy: 2 * n_components = 8 dimensions
    config_concat = {
        "kernel": "cosine",
        "n_components": 4,
        "reg": 1e-3,
        "center_kernels": True,
        "pre_reduce": False,
        "fusion_strategy": "concat",
        "l2_normalize_output": True
    }
    
    kcca = KCCAFusion(config_concat)
    kcca.fit(X_train, Y_train)
    fused = kcca.transform(X_train, Y_train)
    assert fused.shape == (8, 8)

def test_kcca_save_load(tmp_path):
    X_train = np.random.randn(10, 20)
    Y_train = np.random.randn(10, 15)
    
    config = {
        "kernel": "cosine",
        "n_components": 5,
        "reg": 1e-3,
        "center_kernels": True,
        "pre_reduce": False,
        "fusion_strategy": "sum",
        "l2_normalize_output": True
    }
    
    kcca = KCCAFusion(config)
    kcca.fit(X_train, Y_train)
    
    model_path = os.path.join(tmp_path, "kcca.pkl")
    kcca.save(model_path)
    
    loaded = KCCAFusion.load(model_path)
    assert np.allclose(kcca.alpha, loaded.alpha)
    assert np.allclose(kcca.beta, loaded.beta)
    assert loaded.n_components == 5
