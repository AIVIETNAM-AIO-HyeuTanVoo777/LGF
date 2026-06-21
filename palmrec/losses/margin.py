import math

import torch
import torch.nn as nn
import torch.nn.functional as F

from .supcon import SupConLoss


class ArcFaceLoss(nn.Module):
    """
    ArcFace margin head and loss.

    Input features are expected to be embeddings from the model. The module
    normalizes both features and class weights, applies the angular margin, and
    computes cross entropy on scaled logits.
    """
    def __init__(self, embedding_dim: int, num_classes: int, scale: float = 30.0, margin: float = 0.5):
        super().__init__()
        self.embedding_dim = embedding_dim
        self.num_classes = num_classes
        self.scale = scale
        self.margin = margin
        self.weight = nn.Parameter(torch.empty(num_classes, embedding_dim))
        nn.init.xavier_uniform_(self.weight)

        self.cos_m = math.cos(margin)
        self.sin_m = math.sin(margin)
        self.th = math.cos(math.pi - margin)
        self.mm = math.sin(math.pi - margin) * margin

    def forward(self, embeddings, labels):
        cosine = F.linear(F.normalize(embeddings, p=2, dim=1), F.normalize(self.weight, p=2, dim=1))
        sine = torch.sqrt(torch.clamp(1.0 - cosine.pow(2), min=0.0))
        phi = cosine * self.cos_m - sine * self.sin_m
        phi = torch.where(cosine > self.th, phi, cosine - self.mm)

        one_hot = F.one_hot(labels, num_classes=self.num_classes).to(dtype=cosine.dtype, device=cosine.device)
        logits = (one_hot * phi) + ((1.0 - one_hot) * cosine)
        logits = logits * self.scale
        return F.cross_entropy(logits, labels), logits


class CosFaceLoss(nn.Module):
    """
    CosFace margin head and loss with normalized features and class weights.
    """
    def __init__(self, embedding_dim: int, num_classes: int, scale: float = 30.0, margin: float = 0.35):
        super().__init__()
        self.embedding_dim = embedding_dim
        self.num_classes = num_classes
        self.scale = scale
        self.margin = margin
        self.weight = nn.Parameter(torch.empty(num_classes, embedding_dim))
        nn.init.xavier_uniform_(self.weight)

    def forward(self, embeddings, labels):
        cosine = F.linear(F.normalize(embeddings, p=2, dim=1), F.normalize(self.weight, p=2, dim=1))
        one_hot = F.one_hot(labels, num_classes=self.num_classes).to(dtype=cosine.dtype, device=cosine.device)
        logits = self.scale * (cosine - one_hot * self.margin)
        return F.cross_entropy(logits, labels), logits


class MarginHeadLoss(nn.Module):
    """
    ArcFace/CosFace loss with optional lightweight supervised contrastive term.
    """
    def __init__(
        self,
        loss_name: str,
        embedding_dim: int,
        num_classes: int,
        scale: float = 30.0,
        margin: float = None,
        lambda_supcon: float = 0.0,
        temperature: float = 0.07,
    ):
        super().__init__()
        loss_name = loss_name.lower()
        if loss_name == "arcface":
            self.margin_head = ArcFaceLoss(
                embedding_dim=embedding_dim,
                num_classes=num_classes,
                scale=scale,
                margin=0.5 if margin is None else margin,
            )
        elif loss_name == "cosface":
            self.margin_head = CosFaceLoss(
                embedding_dim=embedding_dim,
                num_classes=num_classes,
                scale=scale,
                margin=0.35 if margin is None else margin,
            )
        else:
            raise ValueError(f"Unsupported margin loss: {loss_name}")

        self.loss_name = loss_name
        self.lambda_supcon = lambda_supcon
        self.supcon_loss = SupConLoss(temperature=temperature)

    def forward(self, logits, embeddings, labels):
        loss_margin, margin_logits = self.margin_head(embeddings, labels)
        if self.lambda_supcon > 0:
            loss_supcon = self.supcon_loss(embeddings, labels)
        else:
            loss_supcon = embeddings.new_tensor(0.0)
        loss = loss_margin + self.lambda_supcon * loss_supcon
        return loss, {
            "loss": loss.item(),
            "loss_ce": loss_margin.item(),
            "loss_supcon": loss_supcon.item(),
            "loss_margin": loss_margin.item(),
            "margin_logits": margin_logits.detach(),
        }


def build_loss(config, num_classes: int, embedding_dim: int):
    loss_cfg = config.get("loss", {}) or {}
    train_cfg = config.get("training", {}) or {}
    loss_name = loss_cfg.get("name") or train_cfg.get("loss_type") or "combined"
    loss_name = str(loss_name).lower()

    if loss_name in {"arcface", "cosface"}:
        return MarginHeadLoss(
            loss_name=loss_name,
            embedding_dim=embedding_dim,
            num_classes=num_classes,
            scale=float(loss_cfg.get("scale", train_cfg.get("scale", 30.0))),
            margin=loss_cfg.get("margin", train_cfg.get("margin")),
            lambda_supcon=float(train_cfg.get("lambda_supcon", loss_cfg.get("lambda_supcon", 0.0))),
            temperature=float(train_cfg.get("temperature", loss_cfg.get("temperature", 0.07))),
        )

    from .combined import CombinedLoss

    return CombinedLoss(
        lambda_supcon=float(train_cfg.get("lambda_supcon", 0.10)),
        temperature=float(train_cfg.get("temperature", 0.07)),
    )
