Terminology note: current submission wording is palm-class-disjoint with manifest-level subject-field audit; independently verified person-disjointness is not asserted.

# Rank-B Scope Lock — Tongji + IITD Only

This project upgrade is locked to two datasets:

```text
Primary: Tongji
Secondary: IITD
```

No third dataset should be added in this submission cycle.

Main upgrade:

```text
development/test palm-class-disjoint Tongji cross-session protocol
```

Secondary validation:

```text
IITD secondary palm-class-disjoint within-dataset validation
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
We use a development/test palm-class-disjoint protocol. Training and validation images are drawn from development subjects, while gallery and probe images are drawn from held-out test palm classes. No manifest palm class appears in both the development set and the gallery/probe evaluation set.
```

## Post-result pivot after Tongji palm-class-disjoint evaluation

The original aspirational claim (that B6 improves over B1 under palm-class-disjoint Tongji protocol) is not supported by the new palm-class-disjoint evaluation results.

Therefore, any claim stating that B6 improves performance under palm-class-disjoint Tongji is replaced with:
"BNNeck + ArcFace improves the original seen-identity Tongji protocol but does not improve over CE + SupCon overall under the stricter development/test palm-class-disjoint Tongji protocol. The paper is therefore framed as a protocol-sensitivity evaluation rather than a universal improvement claim."

Scope Constraints:
- Keep scope locked to Tongji + IITD.
- Keep IITD as secondary validation only.

