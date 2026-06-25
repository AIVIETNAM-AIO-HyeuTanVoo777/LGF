from .baselines import ResNet18Baseline, ResNet18BNNeck

def build_model(name: str, num_classes: int, embedding_dim: int = 256, pretrained: bool = True):
    """
    Factory function for the model variants used by the current paper.
    """
    if name == "ResNet18Baseline":
        return ResNet18Baseline(num_classes=num_classes, embedding_dim=embedding_dim, pretrained=pretrained)
    elif name == "ResNet18BNNeck":
        return ResNet18BNNeck(num_classes=num_classes, embedding_dim=embedding_dim, pretrained=pretrained)
    else:
        raise ValueError(f"Unknown model name: {name}")
