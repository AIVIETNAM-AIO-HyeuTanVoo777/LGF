import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, Any, List
import logging

from .conv_branch import ConvBranch
from .transformer_branch import TransformerBranch
from .fcu import ConvToTransFCU, TransToConvFCU

logger = logging.getLogger(__name__)

class PalmConformer(nn.Module):
    """Visual Conformer architecture combining CNN and Transformer branches with FCUs.
    Maps to paper section: Conformer visual architecture.
    """
    def __init__(self, config: Dict[str, Any]) -> None:
        super().__init__()
        self.config = config
        
        # Load hyperparameters
        self.image_size = int(config.get("image_size", 224))
        self.in_channels = int(config.get("in_channels", 3))
        self.num_classes = config.get("num_classes", 10) # can be overridden during training
        
        # Conv Branch configs
        self.conv_stem_channels = int(config.get("conv_stem_channels", 64))
        self.depth = int(config.get("depth", 12))
        
        # Transformer Branch configs
        self.embed_dim = int(config.get("embed_dim", 384))
        self.num_heads = int(config.get("num_heads", 6))
        self.mlp_ratio = float(config.get("mlp_ratio", 4.0))
        self.patch_size = int(config.get("patch_size", 16))
        
        # Feature dimension for KCCA
        self.feature_dim = int(config.get("feature_dim", 512))
        
        # FCU stages (e.g. blocks at which coupling occurs, 1-indexed)
        self.fcu_stages = list(config.get("fcu_stages", [3, 6, 9, 12]))
        
        # Dropout
        dropout = float(config.get("dropout", 0.0))
        attn_dropout = float(config.get("attn_dropout", 0.0))

        # 1. Conv Stem (Backbone)
        # Downsamples [B, 3, 224, 224] to [B, conv_stem_channels, 56, 56]
        self.conv_stem = nn.Sequential(
            nn.Conv2d(self.in_channels, self.conv_stem_channels, kernel_size=7, stride=2, padding=3, bias=False),
            nn.BatchNorm2d(self.conv_stem_channels),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        )
        
        # 2. Dual branches
        self.conv_branch = ConvBranch(self.conv_stem_channels, self.conv_stem_channels, self.depth)
        self.trans_branch = TransformerBranch(
            image_size=self.image_size,
            patch_size=self.patch_size,
            in_channels=self.in_channels,
            embed_dim=self.embed_dim,
            depth=self.depth,
            num_heads=self.num_heads,
            mlp_ratio=self.mlp_ratio,
            dropout=dropout,
            attn_dropout=attn_dropout
        )
        
        # 3. Feature Coupling Units
        self.conv_to_trans_fcus = nn.ModuleDict()
        self.trans_to_conv_fcus = nn.ModuleDict()
        
        patch_resolution = self.image_size // self.patch_size
        for stage in self.fcu_stages:
            stage_str = str(stage)
            self.conv_to_trans_fcus[stage_str] = ConvToTransFCU(
                in_channels=self.conv_stem_channels,
                embed_dim=self.embed_dim,
                patch_resolution=patch_resolution
            )
            self.trans_to_conv_fcus[stage_str] = TransToConvFCU(
                embed_dim=self.embed_dim,
                out_channels=self.conv_stem_channels,
                patch_resolution=patch_resolution
            )

        # 4. Joint Feature Projection
        # Concatenate pooled CNN features and class token: [B, conv_stem_channels + embed_dim]
        # Project to [B, feature_dim]
        self.feature_proj = nn.Sequential(
            nn.Linear(self.conv_stem_channels + self.embed_dim, self.feature_dim),
            nn.BatchNorm1d(self.feature_dim),
            nn.ReLU(inplace=True)
        )
        
        # 5. Classifier Head
        self.classifier = nn.Linear(self.feature_dim, self.num_classes)

    def extract_features(self, x: torch.Tensor) -> torch.Tensor:
        """Extract penultimate feature representation [B, feature_dim] for KCCA fusion."""
        # 1. Run Stem on CNN branch
        x_conv = self.conv_stem(x) # [B, conv_stem_channels, 56, 56]
        
        # 2. Initialize Transformer branch sequence
        x_trans = self.trans_branch.forward_features(x) # [B, num_patches + 1, embed_dim]
        
        # 3. Dual-branch processing with coupling
        for i in range(self.depth):
            # Block index (1-indexed for matching stage config)
            stage = i + 1
            stage_str = str(stage)
            
            # Forward pass through individual branch blocks
            x_conv = self.conv_branch.blocks[i](x_conv)
            x_trans = self.trans_branch.blocks[i](x_trans)
            
            # Apply coupling if configured for this stage
            if stage_str in self.conv_to_trans_fcus:
                # CNN to Transformer
                # Separate class token and patch tokens
                cls_tok = x_trans[:, :1]
                patch_toks = x_trans[:, 1:]
                
                coupled_trans = self.conv_to_trans_fcus[stage_str](x_conv)
                patch_toks = patch_toks + coupled_trans
                
                x_trans = torch.cat([cls_tok, patch_toks], dim=1)
                
                # Transformer to CNN
                coupled_conv = self.trans_to_conv_fcus[stage_str](patch_toks, target_shape=x_conv.shape)
                x_conv = x_conv + coupled_conv
                
        # 4. Global pooling of both branches
        # Conv branch: global average pooling
        pooled_conv = F.adaptive_avg_pool2d(x_conv, (1, 1)).flatten(1) # [B, conv_stem_channels]
        
        # Transformer branch: Class token
        x_trans_norm = self.trans_branch.norm(x_trans)
        pooled_trans = x_trans_norm[:, 0] # [B, embed_dim]
        
        # 5. Joint feature fusion and projection
        joint_features = torch.cat([pooled_conv, pooled_trans], dim=1) # [B, conv_stem_channels + embed_dim]
        projected_features = self.feature_proj(joint_features) # [B, feature_dim]
        
        return projected_features

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass returning class logits of shape [B, num_classes]."""
        features = self.extract_features(x)
        logits = self.classifier(features)
        return logits
