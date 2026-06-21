# Code, Model, Training, and Evaluation Audit

## Required tests

Run:

```bat
pytest -q
```

Expected previous result:

```text
45 passed
```

If result differs, report exact failure.

## Required model registry checks

Check `palmrec/models/__init__.py` and related model files for these registered or buildable names:

```text
ResNet18Baseline
LGFNetSmall
LGFNetNoGabor
FixedGaborResNet18
```

## Required model intent checks

### B1

Expected:

```text
ResNet18Baseline + CE + SupCon
256-D L2-normalized embedding if implemented by baseline
ImageNet pretrained when config says pretrained: true
```

### B2

Expected:

```text
FixedGaborResNet18
fixed Gabor stem or fixed Gabor prior
ResNet18 branch
256-D embedding
CE + SupCon
```

### M1

Expected:

```text
LGFNetSmall full
CNN branch + DeiT/Transformer branch + learnable Gabor branch + gated fusion
CE + SupCon
```

### B3

Expected:

```text
LGFNetNoGabor
CNN branch + DeiT/Transformer branch
No Gabor branch
CE + SupCon
```

## Required eval script checks

Check `scripts/eval_embedding.py`:

1. It must build the model using config values, not hardcoded defaults.
2. It must read:
   - `model.name`
   - `model.embedding_dim`
   - `model.pretrained`
3. It must load `checkpoint["model_state_dict"]` into the same architecture used for training.
4. It must evaluate gallery/probe split via cosine similarity.
5. It must report:
   - Rank-1
   - Rank-5
   - Macro-F1
   - EER
   - TAR@FAR=1e-2
   - TAR@FAR=1e-3
   - params
   - FLOPs
   - average inference time
6. It must save results under experiment directory or requested output directory.

## Required train script checks

Check `scripts/train_lgf.py`:

1. It loads config from `--config`.
2. It respects split file from config.
3. It builds model from config.
4. It uses CE and SupCon when `lambda_supcon > 0`.
5. It uses AMP if `amp: true`.
6. It saves `best.pt` and `last.pt` under `save_dir/checkpoints`.
7. It does not silently ignore `lambda_supcon` or model name.

## Known warning

This warning is acceptable but should be documented:

```text
FutureWarning: torch.cuda.amp.autocast is deprecated; use torch.amp.autocast('cuda')
```

Do not treat it as a correctness failure unless it breaks execution.

## Optional checkpoint-based verification

If local checkpoints exist under ignored `experiments/`, AGENT may rerun eval only, not train:

```bat
python scripts/eval_embedding.py --checkpoint experiments/<exp>/checkpoints/best.pt --config configs/<config>.yaml
```

Rerun metric tolerance:

- Rank/F1/EER/TAR should match within ±0.05 percentage points.
- Params and FLOPs should match exactly or within formatting difference.
- Inference time may vary; do not use exact time as a hard failure unless it is grossly inconsistent.

If checkpoints are missing, mark checkpoint reproduction as `BLOCKED`, but still audit saved metrics and configs.
