# Git and Reproducibility Audit

## Required Git checks

Run:

```bat
git status
git log --oneline -5
git rev-parse HEAD
git ls-tree -r --name-only HEAD | findstr /i /c:"experiments/" /c:".pt" /c:".pth" /c:".ckpt"
```

Expected:

```text
working tree clean
branch up to date with origin/main
no output from checkpoint/model artifact check
```

Known pushed clean commit:

```text
9d36333 Add palmprint recognition pipeline and experiment summaries
```

Do not fail the audit solely because HEAD differs, but if HEAD differs, report it.

## Required `.gitignore` checks

`.gitignore` should include:

```text
experiments/
*.pt
*.pth
*.ckpt
*.onnx
```

It should also continue ignoring raw/segmented data:

```text
data/raw/
data/segmented/
data/toy/
```

## Large-file policy

The repo must not commit:

```text
experiments/
*.pt
*.pth
*.ckpt
*.onnx
```

Saved metrics/configs under `docs/results/` are allowed.

Dataset metadata and split JSON files may be committed if they are small and do not contain private data. Verify file sizes if needed.

## Reproducibility checks

The report must say whether each item is reproducible from Git alone:

1. Code import and tests: yes if `pytest -q` passes.
2. Dataset metadata/splits: yes if metadata/splits are committed.
3. Actual training: no, requires external dataset under ignored `data/segmented`.
4. Exact checkpoint eval: no if checkpoints are ignored and not supplied separately.
5. Saved metrics: yes from `docs/results`.

## Required final note

The audit must explicitly state:

```text
Checkpoints are intentionally not versioned in Git. Reproducing metrics from scratch requires the segmented datasets and training time. Saved metrics are versioned for documentation, not as a substitute for raw reproducibility.
```
