import math
import torch
import torch.nn as nn
import torch.nn.functional as F

class LearnableGaborStem(nn.Module):
    """
    Learnable Gabor Filter bank implemented as a PyTorch module.
    Parameters are theta, sigma, lambd, gamma, and psi.
    sigma, lambd, and gamma are forced to remain positive using softplus.
    """
    def __init__(self, num_filters: int = 16, kernel_size: int = 31, fixed: bool = False):
        super().__init__()
        self.num_filters = num_filters
        self.kernel_size = kernel_size
        self.fixed = fixed
        
        if kernel_size % 2 == 0:
            raise ValueError(f"kernel_size must be odd, got {kernel_size}")
            
        # Grid coordinates
        half_size = (kernel_size - 1) / 2
        y, x = torch.meshgrid(
            torch.linspace(-half_size, half_size, kernel_size),
            torch.linspace(-half_size, half_size, kernel_size),
            indexing="ij"
        )
        self.register_buffer("x_grid", x, persistent=False)
        self.register_buffer("y_grid", y, persistent=False)
        
        # Initial parameters
        # theta covers orientations uniformly in [0, pi)
        theta_init = torch.linspace(0.0, math.pi, num_filters + 1)[:num_filters]
        
        # Parameters (theta, sigma, lambd, gamma, psi)
        self.raw_theta = nn.Parameter(theta_init, requires_grad=not fixed)
        self.raw_sigma = nn.Parameter(torch.full((num_filters,), 5.0), requires_grad=not fixed)
        self.raw_lambd = nn.Parameter(torch.full((num_filters,), 10.0), requires_grad=not fixed)
        self.raw_gamma = nn.Parameter(torch.full((num_filters,), 1.0), requires_grad=not fixed)
        self.raw_psi = nn.Parameter(torch.full((num_filters,), 0.0), requires_grad=not fixed)
        
    def _get_kernels(self):
        # Apply softplus to ensure positivity for sigma, lambd, gamma
        sigma = F.softplus(self.raw_sigma) + 1e-5
        lambd = F.softplus(self.raw_lambd) + 1e-5
        gamma = F.softplus(self.raw_gamma) + 1e-5
        theta = self.raw_theta
        psi = self.raw_psi
        
        # Reshape to [num_filters, 1, 1] for broadcasting
        theta = theta.view(-1, 1, 1)
        sigma = sigma.view(-1, 1, 1)
        lambd = lambd.view(-1, 1, 1)
        gamma = gamma.view(-1, 1, 1)
        psi = psi.view(-1, 1, 1)
        
        # Rotate coordinates
        x_prime = self.x_grid.unsqueeze(0) * torch.cos(theta) + self.y_grid.unsqueeze(0) * torch.sin(theta)
        y_prime = -self.x_grid.unsqueeze(0) * torch.sin(theta) + self.y_grid.unsqueeze(0) * torch.cos(theta)
        
        # Gaussian envelope
        envelope = torch.exp(-(x_prime**2 + (gamma**2) * (y_prime**2)) / (2 * (sigma**2)))
        
        # Sinusoidal carrier
        carrier = torch.cos(2 * math.pi * x_prime / lambd + psi)
        
        # Gabor kernels of shape [num_filters, 1, kernel_size, kernel_size]
        kernels = (envelope * carrier).unsqueeze(1)
        return kernels
        
    def forward(self, x):
        # Input shape: [B, 1, H, W]
        # Output shape: [B, num_filters, H, W]
        kernels = self._get_kernels()
        padding = self.kernel_size // 2
        return F.conv2d(x, kernels, padding=padding)

if __name__ == "__main__":
    # Quick unit test forward pass
    x = torch.randn(2, 1, 224, 224)
    stem = LearnableGaborStem(num_filters=16, kernel_size=31, fixed=False)
    y = stem(x)
    print(f"LearnableGaborStem output shape: {y.shape}")
