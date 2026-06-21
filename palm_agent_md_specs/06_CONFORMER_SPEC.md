# Conformer Specification

## 1. Paper requirements

The paper describes a visual Conformer architecture:

- based on ViT and ResNet structures.
- parallel architecture.
- preserves local and global image features.
- contains:
  - backbone
  - dual-branch module
  - Feature Coupling Unit (FCU)
  - classifier
- Transformer encoder includes:
  - input embedding
  - positional encoding
  - class token
  - Multi-Head Attention
  - FFN
  - LayerNorm
  - residual connections

## 2. Required warning

Do not implement speech Conformer. Do not implement plain CNN. Do not implement plain ViT.

The default model must be a **visual Conformer-style CNN/ResNet + Transformer model with FCU coupling**.

## 3. Required classes

```python
class PalmConformer(nn.Module):
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Return classification logits."""

    def extract_features(self, x: torch.Tensor) -> torch.Tensor:
        """Return penultimate feature vector for KCCA."""
```

```python
class ConvBranch(nn.Module):
    ...
```

```python
class TransformerBranch(nn.Module):
    ...
```

```python
class FeatureCouplingUnit(nn.Module):
    ...
```

```python
class ConvToTransFCU(nn.Module):
    ...
```

```python
class TransToConvFCU(nn.Module):
    ...
```

## 4. Input/output

Input:

```text
x: [B, 3, 224, 224]
```

Training output:

```text
logits: [B, num_classes]
```

Feature extraction output:

```text
features: [B, d_conformer]
```

## 5. Training setup

Use paper defaults:

```yaml
training:
  batch_size: 16
  optimizer: adam
  lr: 1.0e-5
  scheduler: cosine_annealing
  min_lr: 5.0e-7
  loss: cross_entropy
```

Target:

```text
class_id corresponding to palm_id
```

Not target:

```text
gender
hand_side
session
```

## 6. Architecture config

Paper does not provide exact architecture dimensions. Use configurable assumptions:

```yaml
conformer:
  image_size: 224
  in_channels: 3
  num_classes: auto

  # IMPLEMENTATION ASSUMPTIONS:
  conv_stem_channels: 64
  embed_dim: 384
  depth: 12
  num_heads: 6
  mlp_ratio: 4.0
  patch_size: 16
  feature_dim: 512
  fcu_stages: [3, 6, 9, 12]
  dropout: 0.0
  attn_dropout: 0.0
  drop_path: 0.0
```

## 7. FCU behavior

### CNN to Transformer

```text
CNN feature map [B, C, H, W]
→ 1×1 projection to embed_dim
→ flatten spatial map to tokens
→ align token count
→ add/update transformer patch tokens
```

### Transformer to CNN

```text
Transformer patch tokens [B, N, D]
→ reshape to spatial feature map
→ 1×1 projection to CNN channels
→ interpolate to CNN resolution if needed
→ add/update CNN feature map
```

## 8. Checkpointing

Save:

```text
outputs/checkpoints/{dataset}/best_conformer.pt
outputs/checkpoints/{dataset}/last_conformer.pt
outputs/checkpoints/{dataset}/training_log.csv
```

Checkpoint must include:

```python
{
    "model_state_dict": ...,
    "optimizer_state_dict": ...,
    "scheduler_state_dict": ...,
    "epoch": ...,
    "best_metric": ...,
    "config": ...,
    "class_id_to_palm_id": ...
}
```

## 9. Feature extraction

After training:

```python
model.eval()
with torch.no_grad():
    features = model.extract_features(images)
```

Save as:

```text
outputs/features/{dataset}/conformer_train.npz
outputs/features/{dataset}/conformer_test.npz
```

## 10. Tests

- forward shape with `[2, 3, 224, 224]`.
- logits shape `[2, num_classes]`.
- feature shape `[2, d_conformer]`.
- FCU CNN→Transformer shape.
- FCU Transformer→CNN shape.
- toy training loss decreases or overfits tiny batch.
