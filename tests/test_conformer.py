import torch
import torch.nn as nn
import pytest
from palmrec.models.conformer.backbone import PalmConformer
from palmrec.models.conformer.fcu import ConvToTransFCU, TransToConvFCU

@pytest.fixture
def conformer_config():
    return {
        "image_size": 224,
        "in_channels": 3,
        "num_classes": 5,
        "conv_stem_channels": 16,
        "embed_dim": 32,
        "depth": 2,
        "num_heads": 2,
        "mlp_ratio": 2.0,
        "patch_size": 16,
        "feature_dim": 64,
        "fcu_stages": [1, 2],
        "dropout": 0.0,
        "attn_dropout": 0.0
    }

def test_conformer_forward_logits_shape(conformer_config):
    model = PalmConformer(conformer_config)
    dummy_input = torch.randn(2, 3, 224, 224)
    logits = model(dummy_input)
    assert logits.shape == (2, 5) # Batch size 2, 5 classes

def test_conformer_extract_features_shape(conformer_config):
    model = PalmConformer(conformer_config)
    dummy_input = torch.randn(2, 3, 224, 224)
    features = model.extract_features(dummy_input)
    assert features.shape == (2, 64) # Batch size 2, 64 feature dimensions

def test_fcu_conv_to_trans_shape():
    # CNN to Transformer coupling unit shape check
    # CNN feature map size: [B, C, H, W] = [2, 16, 56, 56]
    # Target: [B, 14*14, embed_dim] = [2, 196, 32]
    fcu = ConvToTransFCU(in_channels=16, embed_dim=32, patch_resolution=14)
    x_conv = torch.randn(2, 16, 56, 56)
    out = fcu(x_conv)
    assert out.shape == (2, 196, 32)

def test_fcu_trans_to_conv_shape():
    # Transformer to CNN coupling unit shape check
    # Transformer tokens size: [B, 196, 32]
    # Target CNN size: [B, 16, 56, 56]
    fcu = TransToConvFCU(embed_dim=32, out_channels=16, patch_resolution=14)
    x_trans = torch.randn(2, 196, 32)
    target_shape = (2, 16, 56, 56)
    out = fcu(x_trans, target_shape=torch.Size(target_shape))
    assert out.shape == target_shape

def test_tiny_batch_train_step(conformer_config):
    model = PalmConformer(conformer_config)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
    criterion = nn.CrossEntropyLoss()
    
    dummy_input = torch.randn(2, 3, 224, 224)
    dummy_labels = torch.tensor([0, 1])
    
    # Train step
    model.train()
    logits = model(dummy_input)
    loss = criterion(logits, dummy_labels)
    
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    assert loss.item() > 0
