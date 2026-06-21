import torch
import torch.nn as nn
import torch.nn.functional as F

class GatedFusionModule(nn.Module):
    """
    Gated Fusion Module:
    Applies a gating mechanism via a sigmoid MLP on the concatenated features,
    projects the gated features to the embedding dimension using a projection MLP,
    and returns the L2-normalized embedding.
    """
    def __init__(self, input_dim: int, embedding_dim: int = 256):
        super().__init__()
        
        # Gate: Sigmoid MLP (e.g. input_dim -> input_dim // 2 -> input_dim)
        self.gate = nn.Sequential(
            nn.Linear(input_dim, input_dim // 2),
            nn.ReLU(),
            nn.Linear(input_dim // 2, input_dim),
            nn.Sigmoid()
        )
        
        # Projection: MLP to embedding_dim
        self.project = nn.Sequential(
            nn.Linear(input_dim, input_dim // 2),
            nn.ReLU(),
            nn.Linear(input_dim // 2, embedding_dim)
        )
        
    def forward(self, x):
        # Compute gates
        g = self.gate(x)
        # Apply gate (element-wise multiplication)
        fused = g * x
        # Project to embedding space
        embedding = self.project(fused)
        # L2-normalize
        normalized_embedding = F.normalize(embedding, p=2, dim=1)
        return normalized_embedding
