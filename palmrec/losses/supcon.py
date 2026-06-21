import torch
import torch.nn as nn

class SupConLoss(nn.Module):
    """
    Supervised Contrastive Learning Loss.
    Adapted from: https://github.com/HobbitLong/SupContrast/blob/master/losses.py
    
    Supports both supervised contrastive learning (using labels) and 
    unsupervised contrastive learning (when labels=None).
    """
    def __init__(self, temperature=0.07, contrast_mode='all', base_temperature=0.07):
        super(SupConLoss, self).__init__()
        self.temperature = temperature
        self.contrast_mode = contrast_mode
        self.base_temperature = base_temperature

    def forward(self, features, labels=None, mask=None):
        """
        Args:
            features: hidden vector of shape [bsz, n_views, ...].
                      If features has shape [bsz, f_dim], it is unsqueezed to [bsz, 1, f_dim].
            labels: ground truth labels of shape [bsz].
            mask: contrastive mask of shape [bsz, bsz], mask[i, j]=1 if sample j
                  has the same class as sample i. Can be asymmetric.
        Returns:
            A loss scalar.
        """
        device = features.device

        # If features is 2D: [B, D] -> unsqueeze to [B, 1, D]
        if len(features.shape) < 3:
            features = features.unsqueeze(1)

        if len(features.shape) > 3:
            features = features.view(features.shape[0], features.shape[1], -1)

        batch_size = features.shape[0]
        if labels is not None and mask is not None:
            raise ValueError('Cannot define both `labels` and `mask`')
        elif labels is None and mask is None:
            mask = torch.eye(batch_size, dtype=torch.float32).to(device)
        elif labels is not None:
            labels = labels.view(-1, 1)
            if labels.shape[0] != batch_size:
                raise ValueError('Num of labels does not match num of features')
            mask = torch.eq(labels, labels.T).float().to(device)
        else:
            mask = mask.float().to(device)

        contrast_count = features.shape[1]
        contrast_feature = torch.cat(torch.unbind(features, dim=1), dim=0)
        
        if self.contrast_mode == 'one':
            anchor_feature = features[:, 0]
            anchor_count = 1
        elif self.contrast_mode == 'all':
            anchor_feature = contrast_feature
            anchor_count = contrast_count
        else:
            raise ValueError('Unknown contrast_mode: {}'.format(self.contrast_mode))

        # Compute logits (dot product similarity matrix)
        anchor_dot_contrast = torch.div(
            torch.matmul(anchor_feature, contrast_feature.T),
            self.temperature)
        
        # For numerical stability
        logits_max, _ = torch.max(anchor_dot_contrast, dim=1, keepdim=True)
        logits = anchor_dot_contrast - logits_max.detach()

        # Tile mask
        mask = mask.repeat(anchor_count, contrast_count)
        
        # Mask out self-contrast cases (diagonal of the matrix)
        logits_mask = torch.scatter(
            torch.ones_like(mask),
            1,
            torch.arange(batch_size * anchor_count).view(-1, 1).to(device),
            0
        )
        mask = mask * logits_mask

        # Compute log_prob
        exp_logits = torch.exp(logits) * logits_mask
        # Add a small epsilon to avoid log(0)
        log_prob = logits - torch.log(exp_logits.sum(1, keepdim=True) + 1e-8)

        # Compute mean of log-likelihood over positives
        # mask.sum(1) could be 0 if there are no other positives in the batch
        # We handle this by adding epsilon or checking mask.sum(1)
        mask_sum = mask.sum(1)
        mean_log_prob_pos = (mask * log_prob).sum(1) / (mask_sum + 1e-8)

        # Loss
        loss = - (self.temperature / self.base_temperature) * mean_log_prob_pos
        
        # Only average over anchors that actually have positives (mask_sum > 0)
        # However, to be fully compatible with SupContrast, we do:
        loss = loss.view(anchor_count, batch_size).mean()

        return loss
