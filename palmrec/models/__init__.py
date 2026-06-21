from .conformer import PalmConformer
from .baselines import ResNet18Baseline, ResNet18BNNeck
from .lgf_net import LGFNetSmall, LGFNetNoGabor, FixedGaborResNet18

def build_model(name: str, num_classes: int, embedding_dim: int = 256, pretrained: bool = True):
    """
    Factory function to construct palmprint recognition models.
    """
    if name == "ResNet18Baseline":
        return ResNet18Baseline(num_classes=num_classes, embedding_dim=embedding_dim, pretrained=pretrained)
    elif name == "ResNet18BNNeck":
        return ResNet18BNNeck(num_classes=num_classes, embedding_dim=embedding_dim, pretrained=pretrained)
    elif name == "LGFNetSmall":
        return LGFNetSmall(num_classes=num_classes, embedding_dim=embedding_dim, pretrained=pretrained)
    elif name == "LGFNetNoGabor":
        return LGFNetNoGabor(num_classes=num_classes, embedding_dim=embedding_dim, pretrained=pretrained)
    elif name == "FixedGaborResNet18":
        return FixedGaborResNet18(num_classes=num_classes, embedding_dim=embedding_dim, pretrained=pretrained)
    else:
        raise ValueError(f"Unknown model name: {name}")
