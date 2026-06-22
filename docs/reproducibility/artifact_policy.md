# Artifact Policy

Do not commit or redistribute:

- raw biometric images
- model checkpoints (`*.pt`, `*.pth`, `*.ckpt`, `*.onnx`)
- embeddings or biometric templates (`*.npy`, `*.npz`)
- local experiment directories (`experiments/`)
- generated zip bundles

Allowed in Git:

- source code
- configs
- split JSON files
- audit summaries
- aggregated result summaries
- paper source files

Rationale: biometric data and templates may be sensitive; experiment artifacts are large and machine-specific.
