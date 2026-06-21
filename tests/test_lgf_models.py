import torch
import pytest
from palmrec.models.learnable_gabor import LearnableGaborStem
from palmrec.models.lgf_net import LGFNetSmall, LGFNetNoGabor, FixedGaborResNet18

def test_learnable_gabor_stem_forward():
    # Test LearnableGaborStem forward on [2,1,224,224]
    x = torch.randn(2, 1, 224, 224)
    stem = LearnableGaborStem(num_filters=16, kernel_size=31, fixed=False)
    y = stem(x)
    assert y.shape == (2, 16, 224, 224)
    
    # Check that fixed=True sets requires_grad=False
    stem_fixed = LearnableGaborStem(num_filters=16, kernel_size=31, fixed=True)
    assert not stem_fixed.raw_theta.requires_grad
    assert not stem_fixed.raw_sigma.requires_grad
    assert not stem_fixed.raw_lambd.requires_grad
    assert not stem_fixed.raw_gamma.requires_grad
    assert not stem_fixed.raw_psi.requires_grad
    
    # Check that fixed=False sets requires_grad=True
    assert stem.raw_theta.requires_grad
    assert stem.raw_sigma.requires_grad
    assert stem.raw_lambd.requires_grad
    assert stem.raw_gamma.requires_grad
    assert stem.raw_psi.requires_grad

def test_lgf_net_small_forward():
    # Test LGFNetSmall forward on [2,3,224,224]
    num_classes = 100
    embedding_dim = 256
    model = LGFNetSmall(num_classes=num_classes, embedding_dim=embedding_dim, pretrained=False)
    x = torch.randn(2, 3, 224, 224)
    logits, embedding = model(x)
    
    # Test classifier logits shape [2,num_classes]
    assert logits.shape == (2, num_classes)
    # Test output embedding shape [2,256]
    assert embedding.shape == (2, embedding_dim)
    
    # Verify L2-normalized output
    norm = torch.norm(embedding, p=2, dim=1)
    assert torch.allclose(norm, torch.ones_like(norm), atol=1e-5)

def test_lgf_net_no_gabor_forward():
    # Test LGFNetNoGabor forward on [2,3,224,224]
    num_classes = 100
    embedding_dim = 256
    model = LGFNetNoGabor(num_classes=num_classes, embedding_dim=embedding_dim, pretrained=False)
    x = torch.randn(2, 3, 224, 224)
    logits, embedding = model(x)
    
    assert logits.shape == (2, num_classes)
    assert embedding.shape == (2, embedding_dim)
    
    norm = torch.norm(embedding, p=2, dim=1)
    assert torch.allclose(norm, torch.ones_like(norm), atol=1e-5)

def test_fixed_gabor_resnet18_forward():
    # Test FixedGaborResNet18 forward on [2,3,224,224]
    num_classes = 100
    embedding_dim = 256
    model = FixedGaborResNet18(num_classes=num_classes, embedding_dim=embedding_dim, pretrained=False)
    x = torch.randn(2, 3, 224, 224)
    logits, embedding = model(x)
    
    assert logits.shape == (2, num_classes)
    assert embedding.shape == (2, embedding_dim)
    
    norm = torch.norm(embedding, p=2, dim=1)
    assert torch.allclose(norm, torch.ones_like(norm), atol=1e-5)
