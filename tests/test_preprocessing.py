import numpy as np
import torch
from palmrec.preprocessing.roi import IdentityROIExtractor
from palmrec.preprocessing.transforms import preprocess_for_gabor, preprocess_for_conformer

def test_identity_roi():
    # Verify IdentityROIExtractor returns original array
    extractor = IdentityROIExtractor()
    dummy_img = np.zeros((100, 100, 3), dtype=np.uint8)
    out = extractor.extract(dummy_img)
    assert np.array_equal(dummy_img, out)

def test_resize_224():
    # Verify that preprocessing resizes to 224x224
    extractor = IdentityROIExtractor()
    dummy_img = np.zeros((100, 150, 3), dtype=np.uint8)
    
    gabor_out = preprocess_for_gabor(dummy_img, extractor, target_size=(224, 224))
    conformer_out = preprocess_for_conformer(dummy_img, extractor, target_size=(224, 224))
    
    assert gabor_out.shape == (224, 224)
    assert conformer_out.shape == (3, 224, 224)

def test_gabor_grayscale_shape():
    # Verify color to grayscale conversion and float32 normalization
    extractor = IdentityROIExtractor()
    # Create image with specific values
    dummy_img = np.ones((100, 100, 3), dtype=np.uint8) * 128
    
    out = preprocess_for_gabor(dummy_img, extractor, target_size=(224, 224))
    
    assert out.dtype == np.float32
    assert out.shape == (224, 224)
    # 128 / 255.0 ~= 0.5019
    assert np.allclose(out, 128.0/255.0, atol=1e-3)

def test_conformer_rgb_shape():
    # Verify RGB output and standardization normalization
    extractor = IdentityROIExtractor()
    # Create image with specific values
    dummy_img = np.ones((100, 100, 3), dtype=np.uint8) * 255
    
    # Standard mean/std: mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
    out = preprocess_for_conformer(
        dummy_img, 
        extractor, 
        target_size=(224, 224),
        mean=(0.5, 0.5, 0.5),
        std=(0.5, 0.5, 0.5)
    )
    
    assert isinstance(out, torch.Tensor)
    assert out.dtype == torch.float32
    assert out.shape == (3, 224, 224)
    
    # (1.0 - 0.5) / 0.5 = 1.0
    expected = torch.ones((3, 224, 224), dtype=torch.float32)
    assert torch.allclose(out, expected)
