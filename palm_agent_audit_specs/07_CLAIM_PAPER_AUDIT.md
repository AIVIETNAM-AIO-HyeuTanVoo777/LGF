# Paper Claim Audit

## Main question

Does the current evidence support the intended paper claim?

## Claim decisions

Use one of:

```text
SUPPORTED
PARTIALLY SUPPORTED
NOT SUPPORTED
BLOCKED BY MISSING EVIDENCE
```

## Supported claim candidate

The current strongest defensible claim is:

```text
A fixed Gabor prior improves strict-FAR cross-session verification robustness over a strong ResNet18 + supervised contrastive baseline on Tongji, although the baseline remains more efficient and performs better on the near-saturated IITD within split.
```

This claim is supported only if all are true:

1. B2 average TAR@FAR=1e-3 > B1 average TAR@FAR=1e-3.
2. B2 average Macro-F1 >= B1 average Macro-F1.
3. B2 average EER <= B1 average EER, or the report explicitly acknowledges mixed EER per direction.
4. B1 efficiency advantage is acknowledged.
5. IITD B1 > B2 is acknowledged.
6. The claim is limited to Tongji cross-session strict-FAR robustness, not universal superiority.

## Current expected evidence

Expected strict-FAR advantage:

```text
B1 average TAR@FAR=1e-3: 89.75%
B2 average TAR@FAR=1e-3: 91.85%
Difference: +2.10 percentage points for B2
```

Expected efficiency tradeoff:

```text
B1 FLOPs: 1.819G
B2 FLOPs: 2.709G
B1 average time: 1.81 ms/image
B2 average time: 2.97 ms/image
```

Expected IITD limitation:

```text
IITD B1 Rank-1: 99.13%
IITD B2 Rank-1: 98.26%
```

## Claims to reject

Reject if present:

```text
Learnable Gabor fusion improves palmprint recognition.
```

Reason:

```text
M1 learnable-Gabor full is weaker than B1, B2, and B3 on Tongji S1->S2.
```

Reject if present:

```text
Fixed Gabor is universally better than ResNet18 + SupCon.
```

Reason:

```text
B1 beats B2 on IITD within split and is more efficient.
```

Reject if present:

```text
B2 is best on every metric.
```

Reason:

```text
B1 beats B2 on some Rank metrics and efficiency metrics.
```

## Recommended title decision

Acceptable titles:

```text
Fixed Gabor Priors for Robust Cross-Session Palmprint Verification
Gabor-Guided Metric Learning for Cross-Session Palmprint Recognition
FG-ResNet: Fixed Gabor Prior with Supervised Contrastive Learning for Cross-Session Palmprint Recognition
```

Less safe title:

```text
Learnable Gabor Fusion Network for Palmprint Recognition
```

This less safe title should be rejected unless new M1 results reverse the current evidence.
