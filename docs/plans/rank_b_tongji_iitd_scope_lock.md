# Rank-B Scope Lock — Tongji + IITD Only

This project upgrade is locked to two datasets:

```text
Primary: Tongji
Secondary: IITD
```

No third dataset should be added in this submission cycle.

Main upgrade:

```text
development/test subject-disjoint Tongji cross-session protocol
```

Secondary validation:

```text
IITD secondary subject-disjoint within-dataset validation
```

Forbidden claims:

```text
state-of-the-art
universal superiority
Gabor superiority
B6 dominates IITD
cross-dataset robustness
```

Terminology rule:

```text
We use a development/test subject-disjoint protocol. Training and validation images are drawn from development subjects, while gallery and probe images are drawn from held-out test subjects. No subject appears in both the development set and the gallery/probe evaluation set.
```

## Post-result pivot after Tongji subject-disjoint evaluation

The original aspirational claim (that B6 improves over B1 under subject-disjoint Tongji protocol) is not supported by the new subject-disjoint evaluation results. 

Therefore, any claim stating that B6 improves performance under subject-disjoint Tongji is replaced with:
"BNNeck + ArcFace improves the original seen-identity Tongji protocol but does not improve over CE + SupCon overall under the stricter development/test subject-disjoint Tongji protocol. The paper is therefore framed as a protocol-sensitivity evaluation rather than a universal improvement claim."

Scope Constraints:
- Keep scope locked to Tongji + IITD.
- Keep IITD as secondary validation only.

