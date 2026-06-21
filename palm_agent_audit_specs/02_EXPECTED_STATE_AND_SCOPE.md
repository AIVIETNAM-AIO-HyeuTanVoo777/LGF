# Expected State and Audit Scope

## Project identity

Project: `PALM_CGK_BASE`, under broader `PALM_MASTER`.

Research area: palmprint recognition.

Current implementation direction: experiments around ResNet18, supervised contrastive learning, fixed Gabor priors, learnable Gabor fusion, and ablations.

## Current defensible paper direction

The original direction was close to:

```text
Learnable Gabor fusion improves palmprint recognition.
```

That direction is not currently supported by the logged results.

Current safer direction:

```text
Fixed Gabor priors for robust cross-session palmprint verification.
```

or:

```text
Gabor-Guided Metric Learning for Cross-Session Palmprint Recognition.
```

## Current strongest defensible claim

```text
A fixed Gabor prior improves strict-FAR cross-session verification robustness over a strong ResNet18 + supervised contrastive baseline on Tongji, although the baseline remains more efficient and performs better on the near-saturated IITD within split.
```

## Claims that must be rejected if found

Reject these unless new evidence exists:

1. Fixed Gabor is universally superior to ResNet18 + SupCon.
2. Learnable Gabor fusion improves palmprint recognition.
3. B2 is best on every dataset and every metric.
4. IITD within-split proves universal superiority of fixed Gabor.
5. The project reproduces the original Conformer+Gabor+KCCA+KG paper exactly.
6. The project implements full KCCA fusion and knowledge-graph two-stage recognition as the final experimental pipeline, unless verified in code and experiments.

## Scope of audit

The AGENT must audit:

- repository state and Git hygiene;
- dataset manifest and split integrity;
- config correctness;
- model definitions and naming consistency;
- train/eval script behavior;
- metrics files and summary tables;
- paper-claim alignment;
- reproducibility limitations.

The AGENT should not:

- retrain models by default;
- rewrite code;
- push to Git;
- delete files;
- rewrite history;
- invent paper claims.
