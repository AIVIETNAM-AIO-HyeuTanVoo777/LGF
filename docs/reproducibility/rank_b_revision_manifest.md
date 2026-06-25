# Rank-B Revision Reproducibility Manifest

Generated: 2026-06-25T15:28:57

## Git state

- Branch: `rankb-revision-metric-protocol`
- HEAD: `961aff93c40c2a91d40b9a5eaa854d11b3bd8489`
- Short HEAD: `961aff9`
- Working tree status at manifest generation: `clean`

## Recent commit chain

~~~text
961aff9 Add ArcFace sensitivity plan and evidence
fe0ed8a Clarify palm-class protocol and scoped claims
dc0ace1 Revise protocol wording and claims
99b43be Regenerate conservative TAR@FAR result tables
5703712 Fix conservative TAR@FAR metric
b4b5453 Add final Rank-B submission readiness audit
9edc959 Add fixed Gabor strict Tongji reference baseline
b30b945 Add strict Tongji score-tail failure analysis
c125336 Fix LaTeX package and protocol table layout
4f25aa8 Strengthen protocol-sensitive evaluation framing
~~~

## Revision scope

This revision addresses the Rank-B metric/protocol review items without adding a new architecture claim or a state-of-the-art claim.

Completed scope:

- Conservative TAR@FAR implementation and tests.
- Regenerated strict Tongji and IITD conservative verification results.
- Metric-threshold audit export with selected threshold, empirical FAR, TAR, pair counts, and minimum FAR step.
- Paper/protocol wording revised from nearest-FPR TAR@FAR to conservative empirical-FAR TAR@FAR.
- Claims scoped to palm-class-disjoint evaluation with manifest-level subject-field audit; independently verified person-disjointness is not asserted.
- Abstract, Table 6, Table 14, and B5/B6 wording revised to avoid unsupported superiority claims.
- ArcFace sensitivity recorded as fixed-recipe component evidence, not a margin/scale hyperparameter sweep.

## Metric convention

TAR@FAR is computed using the conservative empirical-FAR rule:

> among ROC points with empirical FAR less than or equal to the target, report the maximum observed TAR/TPR.

This replaces the previous nearest empirical-FPR reporting rule.

## Protocol convention

- Primary protocol: Tongji palm-class-disjoint cross-session evaluation.
- Directions: S1->S2 and S2->S1.
- Seeds: 42, 2026, 2705.
- Main table unit: bidirectional average per seed, then mean ± standard deviation over three seed-level bidirectional averages.
- Strict component-ablation unit: six seed-direction units, without pre-averaging directions.
- IITD is secondary within-dataset validation only, not cross-session evidence.

## ArcFace sensitivity boundary

The current revision does not run a new margin/scale sweep. It records fixed-recipe component sensitivity using B4, B6, and B7 against non-ArcFace controls B1 and B5.

Locked ArcFace recipe in the strict ablation:

- scale `s=30.0`
- margin `m=0.5`

No gallery/probe/test data are used for ArcFace hyperparameter selection.

## Verification commands run before manifest generation

~~~bat
git status --short
python -m py_compile palmrec\evaluation\metrics.py palmrec\evaluation\__init__.py scripts\eval_embedding.py scripts\evaluate_gabor_strict_tongji_baseline.py scripts\audit_metric_thresholds.py
python -m pytest tests\test_metrics_tar_far.py tests\test_evaluation.py -q
python -c "<terminology scan for unsupported subject/person wording>"
~~~

Observed verification result before manifest generation:

- Working tree clean.
- Python compile check passed.
- Evaluation tests passed: 7 tests.
- Terminology scan reported `HITS=0` for unsupported subject-disjoint/person-disjoint wording patterns.

## Artifact inventory

| Path | Exists | SHA256-16 |
|---|---:|---|
| `palmrec/evaluation/metrics.py` | yes | `211f3476c6c99d34` |
| `palmrec/evaluation/__init__.py` | yes | `0e71c7c9d9f6f053` |
| `scripts/eval_embedding.py` | yes | `984938bbdf9d5cab` |
| `scripts/evaluate_gabor_strict_tongji_baseline.py` | yes | `7352b35759741098` |
| `scripts/audit_metric_thresholds.py` | yes | `ea78f48be3dc9f5a` |
| `tests/test_metrics_tar_far.py` | yes | `dacae8d9331835d6` |
| `tests/test_evaluation.py` | yes | `978e283305676954` |
| `docs/audits/metric_threshold_audit.md` | yes | `972ed6db719f4dc5` |
| `docs/audits/metric_threshold_audit.csv` | yes | `0698792ba3e89776` |
| `docs/results/threshold_evidence_strict_tongji.csv` | yes | `45d4f85af852dc43` |
| `docs/results/threshold_evidence_iitd.csv` | yes | `38498223596cb138` |
| `docs/results/strict_tongji_ablation_results.md` | yes | `b57dcbeb070bdb27` |
| `docs/results/strict_tongji_ablation_runs.csv` | yes | `23978aa09d34101b` |
| `docs/results/strict_tongji_ablation_summary.csv` | yes | `5b8da0b4c4741807` |
| `docs/results/paired_statistics_b6_vs_b1.md` | yes | `7a4af97f5862391e` |
| `docs/results/paired_statistics_b6_vs_b1.csv` | yes | `d110647d9a4b33db` |
| `docs/results/paired_statistics_component_ablation.md` | yes | `dc2fc92293875027` |
| `docs/results/paired_statistics_component_ablation.csv` | yes | `b785dc162f87f68f` |
| `docs/results/tongji_directional_delta_b6_minus_b1.md` | yes | `d8c9b876647576b0` |
| `docs/results/tongji_directional_delta_b6_minus_b1.csv` | yes | `8976029407ac1ac0` |
| `docs/results/strict_tongji_ablation_by_direction.md` | yes | `d69f9a68f7572f2d` |
| `docs/results/strict_tongji_ablation_by_direction.csv` | yes | `5814d81184cf02db` |
| `docs/results/strict_tongji_failure_tail_table.md` | yes | `f186fbcda1a27319` |
| `docs/results/strict_tongji_failure_tail_table.csv` | yes | `ea93a6306b123185` |
| `docs/results/arcface_sensitivity_evidence.md` | yes | `ed9b0fa181a2f0c2` |
| `docs/plans/arcface_sensitivity_plan.md` | yes | `7cdd339cc6655bc7` |
| `docs/protocols/evaluation_metrics.md` | yes | `859bad74c630d28c` |
| `docs/protocols/tongji_subject_disjoint_cross_session.md` | yes | `1819d538379aec82` |
| `docs/protocols/iitd_subject_disjoint_within.md` | yes | `42842a8a010bf96d` |
| `docs/reproducibility/rank_b_core_run_matrix.md` | yes | `851b90cc171e3a34` |
| `paper/main.tex` | yes | `d49ea78eb3aed841` |
| `paper/paper_review_packet.md` | yes | `1a27e5e6db55ff6e` |
| `paper/sections/04_experiments.tex` | yes | `69655c061a7f9fa6` |
| `paper/sections/05_results.tex` | yes | `f7a9113292d339d6` |
| `paper/sections/06_ablation.tex` | yes | `306d9a1dd06e0dd7` |
| `paper/sections/07_discussion.tex` | yes | `490022e537465623` |
| `paper/sections/rankb_protocol_audit_table.tex` | yes | `e7b30d9c71adf468` |
| `paper/sections/strict_tongji_ablation_table.tex` | yes | `41984fc47248da22` |
| `paper/sections/strict_tongji_ablation_by_direction_table.tex` | yes | `832e1c09a75cc594` |
| `paper/sections/paired_statistics_b6_vs_b1_table.tex` | yes | `5a22396410abc0e5` |
| `paper/sections/paired_statistics_component_ablation_table.tex` | yes | `1702329465922027` |
| `paper/sections/strict_tongji_failure_tail_table.tex` | yes | `a6aee5463a5074e9` |

## Safety boundary

The revision must not stage or commit raw experiments, checkpoints, model weights, NumPy arrays, archives, or generated experiment directories.

Forbidden staged path patterns include:

- `experiments/`
- `.pt`
- `.pth`
- `.ckpt`
- `.onnx`
- `.zip`
- `.npy`
- `.npz`

## Notes for reviewers

This manifest records the revised metric/protocol state after the conservative TAR@FAR correction. It should be read together with:

- `docs/audits/metric_threshold_audit.md`
- `docs/results/arcface_sensitivity_evidence.md`
- `docs/results/README.md`
- `paper/paper_review_packet.md`
