# Artifact Policy

Raw biometric images, trained checkpoints, and extracted embeddings/templates are not included in the public repository.

The repository may include:

```text
code
configuration YAML files
split JSON files
metadata manifests when license-safe
aggregate result summaries
raw per-seed metric CSV files
plotting scripts
reproducibility commands
environment summaries
```

The repository must not include:

```text
raw biometric images
experiments/
*.pt
*.pth
*.ckpt
*.onnx
extracted biometric embeddings/templates
large tensor dumps
```
