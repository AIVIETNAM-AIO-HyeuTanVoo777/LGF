import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models

class ResNet18Baseline(nn.Module):
    """
    ResNet18 Baseline model for palmprint recognition.
    Extracts features using a pretrained ResNet18 backbone,
    projects to a 256-D embedding space, L2-normalizes the embedding,
    and classifies using a linear head.
    """
    def __init__(self, num_classes: int, embedding_dim: int = 256, pretrained: bool = True):
        super().__init__()
        
        # Load backbone
        if pretrained:
            try:
                from torchvision.models import ResNet18_Weights
                self.backbone = models.resnet18(weights=ResNet18_Weights.DEFAULT)
            except ImportError:
                self.backbone = models.resnet18(pretrained=True)
        else:
            self.backbone = models.resnet18(pretrained=False)
            
        # Get output features of original fc layer (which is 512 for ResNet18)
        num_features = self.backbone.fc.in_features
        
        # Replace original fc with nn.Identity
        self.backbone.fc = nn.Identity()
        
        # Projection layer to embedding_dim (e.g., 256-D)
        self.fc_embedding = nn.Linear(num_features, embedding_dim)
        
        # Classifier head
        self.classifier = nn.Linear(embedding_dim, num_classes)
        
    def forward(self, x):
        # Forward through backbone to get 512-D features
        features = self.backbone(x)
        
        # Project to embedding space
        embedding = self.fc_embedding(features)
        
        # L2 normalize the embedding
        normalized_embedding = F.normalize(embedding, p=2, dim=1)
        
        # Get classification logits
        logits = self.classifier(normalized_embedding)
        
        return logits, normalized_embedding


class ResNet18BNNeck(nn.Module):
    """
    ResNet18 baseline with a BNNeck layer after the embedding projection.

    The model keeps the same forward contract as the other recognition models:
    it returns ``(logits, embedding)``. The default returned embedding is the
    post-BN L2-normalized representation, which is also the default evaluation
    embedding for verification.
    """
    def __init__(self, num_classes: int, embedding_dim: int = 256, pretrained: bool = True):
        super().__init__()

        if pretrained:
            try:
                from torchvision.models import ResNet18_Weights
                self.backbone = models.resnet18(weights=ResNet18_Weights.DEFAULT)
            except ImportError:
                self.backbone = models.resnet18(pretrained=True)
        else:
            self.backbone = models.resnet18(pretrained=False)

        num_features = self.backbone.fc.in_features
        self.backbone.fc = nn.Identity()

        self.fc_embedding = nn.Linear(num_features, embedding_dim)
        self.bnneck = nn.BatchNorm1d(embedding_dim)
        self.bnneck.bias.requires_grad_(False)
        self.classifier = nn.Linear(embedding_dim, num_classes)

    def _features(self, x):
        features = self.backbone(x)
        pre_bn = self.fc_embedding(features)
        post_bn = self.bnneck(pre_bn)
        return pre_bn, post_bn

    def extract_embedding(self, x, embedding_mode: str = "post_bn"):
        pre_bn, post_bn = self._features(x)
        if embedding_mode == "pre_bn":
            embedding = pre_bn
        elif embedding_mode == "post_bn":
            embedding = post_bn
        else:
            raise ValueError(f"Unknown BNNeck embedding mode: {embedding_mode}")
        return F.normalize(embedding, p=2, dim=1)

    def forward(self, x):
        embedding = self.extract_embedding(x, embedding_mode="post_bn")
        logits = self.classifier(embedding)
        return logits, embedding
