import torch
import torch.nn as nn
import torch.nn.functional as F

class ConvToTransFCU(nn.Module):
    """CNN to Transformer Feature Coupling Unit.
    Projects spatial CNN feature map to match Transformer embedding dimension and sequence length.
    """
    def __init__(
        self,
        in_channels: int,
        embed_dim: int,
        patch_resolution: int = 14
    ) -> None:
        super().__init__()
        self.patch_resolution = patch_resolution
        
        # 1x1 Conv to align channels
        self.proj = nn.Conv2d(in_channels, embed_dim, kernel_size=1)
        self.norm = nn.LayerNorm(embed_dim)

    def forward(self, x_conv: torch.Tensor) -> torch.Tensor:
        """Input x_conv: [B, C, H, W]
        Output: [B, H_t*W_t, embed_dim]
        """
        # Align channels
        x = self.proj(x_conv) # [B, embed_dim, H, W]
        
        # Resize spatial dimensions to match patch resolution (typically 14x14)
        if x.shape[2:] != (self.patch_resolution, self.patch_resolution):
            x = F.interpolate(x, size=(self.patch_resolution, self.patch_resolution), mode='bilinear', align_corners=False)
            
        # Flatten spatial dimensions to tokens: [B, embed_dim, 14, 14] -> [B, embed_dim, 196] -> [B, 196, embed_dim]
        x = x.flatten(2).transpose(1, 2)
        
        # Layer normalization
        x = self.norm(x)
        return x

class TransToConvFCU(nn.Module):
    """Transformer to CNN Feature Coupling Unit.
    Reshapes sequence tokens, projects embedding dimension to match CNN channels, and resizes to CNN map size.
    """
    def __init__(
        self,
        embed_dim: int,
        out_channels: int,
        patch_resolution: int = 14
    ) -> None:
        super().__init__()
        self.patch_resolution = patch_resolution
        
        # 1x1 Conv to align channels
        self.proj = nn.Conv2d(embed_dim, out_channels, kernel_size=1)
        self.norm = nn.BatchNorm2d(out_channels)

    def forward(self, x_trans: torch.Tensor, target_shape: torch.Size) -> torch.Tensor:
        """Input x_trans: [B, patch_resolution^2, embed_dim]
        target_shape: [B, C, H_conv, W_conv]
        Output: [B, C, H_conv, W_conv]
        """
        B, N, D = x_trans.shape
        # Reshape to spatial map: [B, 196, D] -> [B, D, 14, 14]
        x = x_trans.transpose(1, 2).reshape(B, D, self.patch_resolution, self.patch_resolution)
        
        # Align channels
        x = self.proj(x)
        x = self.norm(x)
        
        # Resize to CNN target resolution [H_conv, W_conv]
        H_target, W_target = target_shape[2], target_shape[3]
        if x.shape[2:] != (H_target, W_target):
            x = F.interpolate(x, size=(H_target, W_target), mode='bilinear', align_corners=False)
            
        return x
