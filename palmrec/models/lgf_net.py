import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
import timm

from .learnable_gabor import LearnableGaborStem
from .fusion import GatedFusionModule

class LGFNetSmall(nn.Module):
    """
    LGF-Net-Small architecture:
    - Gabor branch (Learnable Gabor Stem + Conv-BN-SiLU + AdaptiveAvgPool)
    - CNN branch (Pretrained ResNet18 backbone, output 512)
    - Transformer branch (Pretrained DeiT-Tiny, output 192)
    - Gated Fusion (GatedFusionModule) to 256-D normalized embedding
    - Classifier head
    """
    def __init__(self, num_classes: int, embedding_dim: int = 256, pretrained: bool = True):
        super().__init__()
        
        # 1. Gabor branch (Learnable)
        self.gabor_stem = LearnableGaborStem(num_filters=16, kernel_size=31, fixed=False)
        self.gabor_conv = nn.Sequential(
            nn.Conv2d(16, 16, kernel_size=3, padding=1),
            nn.BatchNorm2d(16),
            nn.SiLU()
        )
        self.gabor_pool = nn.AdaptiveAvgPool2d(1)
        
        # 2. CNN branch (ResNet18)
        from torchvision.models import ResNet18_Weights

        weights = ResNet18_Weights.DEFAULT if pretrained else None
        self.cnn = models.resnet18(weights=weights)
        self.cnn.fc = nn.Identity()
        
        # 3. Transformer branch (DeiT-Tiny)
        self.transformer = timm.create_model(
            "deit_tiny_patch16_224", 
            pretrained=pretrained, 
            num_classes=0
        )
        
        # 4. Gated Fusion Module
        # Dimensions: 512 (CNN) + 192 (DeiT) + 16 (Gabor) = 720
        self.fusion = GatedFusionModule(input_dim=720, embedding_dim=embedding_dim)
        
        # 5. Classifier Head
        self.classifier = nn.Linear(embedding_dim, num_classes)
        
    def forward(self, x):
        # x: [B, 3, 224, 224]
        
        # Create grayscale internally by channel mean
        x_gray = x.mean(dim=1, keepdim=True) # [B, 1, 224, 224]
        
        # Forward Gabor branch
        x_gabor = self.gabor_stem(x_gray)
        x_gabor = self.gabor_conv(x_gabor)
        x_gabor = self.gabor_pool(x_gabor)
        x_gabor = torch.flatten(x_gabor, 1) # [B, 16]
        
        # Forward CNN branch
        x_cnn = self.cnn(x) # [B, 512]
        
        # Forward Transformer branch
        x_vit = self.transformer(x) # [B, 192]
        
        # Concatenate branches
        x_concat = torch.cat([x_cnn, x_vit, x_gabor], dim=1) # [B, 720]
        
        # Gated fusion and L2 normalization
        embedding = self.fusion(x_concat) # [B, embedding_dim]
        
        # Classifier
        logits = self.classifier(embedding) # [B, num_classes]
        
        return logits, embedding


class LGFNetNoGabor(nn.Module):
    """
    LGF-Net ablation without the Gabor branch:
    - CNN branch (Pretrained ResNet18 backbone, output 512)
    - Transformer branch (Pretrained DeiT-Tiny, output 192)
    - Gated Fusion (GatedFusionModule) to 256-D normalized embedding
    - Classifier head
    """
    def __init__(self, num_classes: int, embedding_dim: int = 256, pretrained: bool = True):
        super().__init__()
        
        # 1. CNN branch (ResNet18)
        from torchvision.models import ResNet18_Weights

        weights = ResNet18_Weights.DEFAULT if pretrained else None
        self.cnn = models.resnet18(weights=weights)
        self.cnn.fc = nn.Identity()
        
        # 2. Transformer branch (DeiT-Tiny)
        self.transformer = timm.create_model(
            "deit_tiny_patch16_224", 
            pretrained=pretrained, 
            num_classes=0
        )
        
        # 3. Gated Fusion Module
        # Dimensions: 512 (CNN) + 192 (DeiT) = 704
        self.fusion = GatedFusionModule(input_dim=704, embedding_dim=embedding_dim)
        
        # 4. Classifier Head
        self.classifier = nn.Linear(embedding_dim, num_classes)
        
    def forward(self, x):
        # x: [B, 3, 224, 224]
        
        # Forward CNN branch
        x_cnn = self.cnn(x) # [B, 512]
        
        # Forward Transformer branch
        x_vit = self.transformer(x) # [B, 192]
        
        # Concatenate branches
        x_concat = torch.cat([x_cnn, x_vit], dim=1) # [B, 704]
        
        # Gated fusion and L2 normalization
        embedding = self.fusion(x_concat) # [B, embedding_dim]
        
        # Classifier
        logits = self.classifier(embedding) # [B, num_classes]
        
        return logits, embedding


class FixedGaborResNet18(nn.Module):
    """
    Ablation with Fixed Gabor stem and ResNet18 backbone:
    - Fixed Gabor stem (Learnable Gabor Stem with fixed=True)
    - Lightweight projection (Conv-BN-SiLU + AdaptiveAvgPool)
    - CNN branch (Pretrained ResNet18 backbone, output 512)
    - Gated Fusion to 256-D normalized embedding
    - Classifier head
    """
    def __init__(self, num_classes: int, embedding_dim: int = 256, pretrained: bool = True):
        super().__init__()
        
        # 1. Gabor branch (Fixed parameters)
        self.gabor_stem = LearnableGaborStem(num_filters=16, kernel_size=31, fixed=True)
        self.gabor_conv = nn.Sequential(
            nn.Conv2d(16, 16, kernel_size=3, padding=1),
            nn.BatchNorm2d(16),
            nn.SiLU()
        )
        self.gabor_pool = nn.AdaptiveAvgPool2d(1)
        
        # 2. CNN branch (ResNet18)
        from torchvision.models import ResNet18_Weights

        weights = ResNet18_Weights.DEFAULT if pretrained else None
        self.cnn = models.resnet18(weights=weights)
        self.cnn.fc = nn.Identity()
        
        # 3. Gated Fusion Module
        # Dimensions: 512 (CNN) + 16 (Gabor) = 528
        self.fusion = GatedFusionModule(input_dim=528, embedding_dim=embedding_dim)
        
        # 4. Classifier Head
        self.classifier = nn.Linear(embedding_dim, num_classes)
        
    def forward(self, x):
        # x: [B, 3, 224, 224]
        
        # Create grayscale internally by channel mean
        x_gray = x.mean(dim=1, keepdim=True) # [B, 1, 224, 224]
        
        # Forward Gabor branch
        x_gabor = self.gabor_stem(x_gray)
        x_gabor = self.gabor_conv(x_gabor)
        x_gabor = self.gabor_pool(x_gabor)
        x_gabor = torch.flatten(x_gabor, 1) # [B, 16]
        
        # Forward CNN branch
        x_cnn = self.cnn(x) # [B, 512]
        
        # Concatenate branches
        x_concat = torch.cat([x_cnn, x_gabor], dim=1) # [B, 528]
        
        # Gated fusion and L2 normalization
        embedding = self.fusion(x_concat) # [B, embedding_dim]
        
        # Classifier
        logits = self.classifier(embedding) # [B, num_classes]
        
        return logits, embedding
