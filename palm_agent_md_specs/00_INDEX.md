# PALM_MASTER — Agent Coding Spec Index

Project: faithful implementation of **“Palmprint Features Fusion Recognition Based on Conformer and Gabor”**.

## Critical fidelity conclusion

This project **cannot be guaranteed 100% identical to the paper at code level** because the paper does not specify several implementation-critical details: exact ROI extraction method, exact Gabor numerical hyperparameters, exact Conformer variant/depth/embedding dimensions, exact KCCA regularization/components/fusion operation, and exact matching threshold/graph-walk implementation.

Therefore the agent must implement two layers:

1. **Paper-specified requirements**: must be implemented exactly as described.
2. **Implementation assumptions**: allowed only where the paper is underspecified, and must be clearly marked in code/config/docs.

## Files in this spec pack

| File | Purpose |
|---|---|
| `01_PAPER_FIDELITY_AUDIT.md` | Audit of what is specified, underspecified, and must not be changed |
| `02_AGENT_MASTER_PROMPT.md` | Master prompt/instructions for the coding agent |
| `03_PIPELINE_SPEC.md` | End-to-end pipeline specification |
| `04_DATA_PREPROCESSING_SPEC.md` | Dataset, metadata, split, ROI, resize, grayscale/RGB rules |
| `05_GABOR_SPEC.md` | Gabor filter-bank implementation specification |
| `06_CONFORMER_SPEC.md` | Conformer model/training/feature extraction specification |
| `07_KCCA_SPEC.md` | KCCA feature-fusion specification |
| `08_KNOWLEDGE_GRAPH_MATCHING_SPEC.md` | Knowledge graph, two-stage recognition, cosine matching |
| `09_EVALUATION_EXPERIMENTS_SPEC.md` | Metrics, timing, reproduction scripts |
| `10_PROJECT_STRUCTURE_CLI_SPEC.md` | Required project tree and CLI design |
| `11_TASK_BREAKDOWN.md` | Milestones, files, classes, acceptance criteria |
| `12_TESTING_ACCEPTANCE.md` | Unit/integration/reproducibility tests |
| `13_ASSUMPTIONS_OPEN_POINTS.md` | All implementation assumptions and open points |
| `14_CONFIG_TEMPLATE.md` | YAML config template with paper-specified vs assumption fields |

## Required agent behavior

- Do not write a simplified pipeline.
- Do not replace KCCA with concatenation.
- Do not skip the knowledge graph.
- Do not treat gender/hand side as classifier targets.
- Do not claim any assumption is from the paper.
- Every assumption must be configurable.
- Every module must have tests.
- Every experiment must log seed, config, dataset split, and hardware.
