import numpy as np
import pytest
from palmrec.features.gabor import GaborFeatureExtractor

@pytest.fixture
def gabor_config():
    return {
        "image_size": [224, 224],
        "num_scales": 7,
        "orientations_deg": [0, 30, 60, 90, 120, 150],
        "response_mode": "magnitude",
        "orientation_fusion": "max",
        "scale_fusion": "concat",
        "kernel_size": 31,
        "sigma": 4.0,
        "gamma": 0.5,
        "phase_offset": 0.0,
        "kmax": 1.57079632679,
        "spacing_factor": 1.41421356237,
        "pooling": {
            "enabled": False
        }
    }

def test_filter_bank_num_scales(gabor_config):
    extractor = GaborFeatureExtractor(gabor_config)
    assert len(extractor.filter_bank) == 7

def test_filter_bank_num_orientations(gabor_config):
    extractor = GaborFeatureExtractor(gabor_config)
    for scale_filters in extractor.filter_bank:
        assert len(scale_filters) == 6

def test_orientation_values(gabor_config):
    extractor = GaborFeatureExtractor(gabor_config)
    expected_orientations = [0, np.pi/6, np.pi/3, np.pi/2, 2*np.pi/3, 5*np.pi/6]
    for actual, expected in zip(extractor.orientations, expected_orientations):
        assert np.allclose(actual, expected)

def test_gabor_feature_dim(gabor_config):
    # Without pooling: 7 * 224 * 224 = 351232
    extractor = GaborFeatureExtractor(gabor_config)
    dummy_img = np.random.rand(224, 224).astype(np.float32)
    feat = extractor.extract(dummy_img)
    assert feat.shape == (351232,)
    
    # With pooling enabled to output_size [14, 14]: 7 * 14 * 14 = 1372
    gabor_config["pooling"] = {
        "enabled": True,
        "type": "adaptive_avg",
        "output_size": [14, 14]
    }
    extractor_pooled = GaborFeatureExtractor(gabor_config)
    feat_pooled = extractor_pooled.extract(dummy_img)
    assert feat_pooled.shape == (1372,)

def test_gabor_no_nan(gabor_config):
    extractor = GaborFeatureExtractor(gabor_config)
    # Test on all zeros
    dummy_img = np.zeros((224, 224), dtype=np.float32)
    feat = extractor.extract(dummy_img)
    assert not np.isnan(feat).any()
    assert not np.isinf(feat).any()

def test_gabor_deterministic(gabor_config):
    extractor1 = GaborFeatureExtractor(gabor_config)
    extractor2 = GaborFeatureExtractor(gabor_config)
    dummy_img = np.random.rand(224, 224).astype(np.float32)
    
    feat1 = extractor1.extract(dummy_img)
    feat2 = extractor2.extract(dummy_img)
    
    assert np.array_equal(feat1, feat2)
