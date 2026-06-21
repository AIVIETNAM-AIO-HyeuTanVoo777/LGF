import torch
import torch.nn as nn
from .supcon import SupConLoss

class CombinedLoss(nn.Module):
    """
    Combined Loss: CrossEntropy Loss + lambda_supcon * SupCon Loss.
    
    Used to train the baseline model with both classification (CE) 
    and metric learning (SupCon) objectives.
    """
    def __init__(self, lambda_supcon: float = 0.10, temperature: float = 0.07):
        super(CombinedLoss, self).__init__()
        self.lambda_supcon = lambda_supcon
        self.ce_loss = nn.CrossEntropyLoss()
        self.supcon_loss = SupConLoss(temperature=temperature)
        
    def forward(self, logits, embeddings, labels):
        """
        Args:
            logits: Classifier logits of shape [B, num_classes].
            embeddings: L2 normalized embeddings of shape [B, D].
            labels: Ground truth labels of shape [B].
        Returns:
            loss: Scalar loss tensor.
            loss_dict: Dict containing individual loss components for logging.
        """
        # Cross Entropy Loss
        loss_ce = self.ce_loss(logits, labels)
        
        # Supervised Contrastive Loss
        loss_supcon = self.supcon_loss(embeddings, labels)
        
        # Combined Loss
        loss = loss_ce + self.lambda_supcon * loss_supcon
        
        loss_dict = {
            "loss": loss.item(),
            "loss_ce": loss_ce.item(),
            "loss_supcon": loss_supcon.item()
        }
        
        return loss, loss_dict
