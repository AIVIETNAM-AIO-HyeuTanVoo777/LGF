# Refactoring Fix Plan — Palmprint Gabor-Conformer

This document details the refactoring roadmap to transition the codebase from **PARTIAL** alignment to **PASS** across all specifications in `palm_agent_md_specs/`.

---

## 1. P0 — Must Fix Before Any Experiment (Strict API & CLI Alignment)

### Patch 1: Refactoring Knowledge Graph & Matching Classes
- **File**: `palmrec/matching/kg.py`
- **Problem**: Gaps between the current `PalmprintKnowledgeGraph` class and the requested classes: `PalmTemplate` dataclass, `PalmKnowledgeGraph`, `CosineMatcher`, `TwoStageRecognizer`, and `MatchResult`.
- **Required Change**:
  1. Add `@dataclass class PalmTemplate` containing `sample_id`, `palm_id`, `subject_id`, `gender`, `hand_side`, `feature`, `image_path`.
  2. Implement `class PalmKnowledgeGraph` supporting:
     - `add_template(self, template: PalmTemplate)`
     - `query_candidates(self, gender=None, hand_side=None) -> list[PalmTemplate]`
     - `all_templates(self) -> list[PalmTemplate]`
     - `save(self, path: str) -> None`
     - `@classmethod load(cls, path: str) -> "PalmKnowledgeGraph"`
  3. Implement `class CosineMatcher` with `match(self, query: np.ndarray, candidates: list[PalmTemplate]) -> MatchResult` returning the best match using cosine similarity (or handling threshold constraints).
  4. Implement `class TwoStageRecognizer` with `predict_feature(self, feature, gender=None, hand_side=None) -> MatchResult` using `PalmKnowledgeGraph` and `CosineMatcher`.
  5. Expose these classes in `palmrec/matching/__init__.py`.
- **Acceptance Test**: Run `pytest tests/test_kg.py` (which will be updated to use the new class names and APIs).

### Patch 2: Renaming & Creating Standard CLI Scripts
- **Files**:
  - Rename `scripts/fuse_features.py` to `scripts/fit_kcca.py`.
  - Create `scripts/build_knowledge_graph.py`.
  - Create `scripts/evaluate.py` (migrated/adapted from `scripts/evaluate_matching.py`).
  - Update `scripts/run_full_pipeline.py` to invoke the newly named scripts.
- **Problem**: Current script names do not match the expected naming layout in `10_PROJECT_STRUCTURE_CLI_SPEC.md`.
- **Required Change**:
  1. `scripts/fit_kcca.py`: Fits KCCA and saves the KCCA checkpoint and fused train/test feature files.
  2. `scripts/build_knowledge_graph.py`: Loads train features, constructs `PalmKnowledgeGraph` using the refactored classes, and serializes it to `outputs/graphs/{dataset}_graph.pkl`.
  3. `scripts/evaluate.py`: Loads the serialized graph, matching threshold, and probe features, runs the search matching, and computes metrics.
- **Acceptance Test**: Run the full pipeline command using `python scripts/run_full_pipeline.py --config configs/toy.yaml` and verify all scripts execute successfully in order.

---

## 2. P1 — Must Fix Before Paper Reproduction (Table Generation & Docs)

### Patch 3: Creating Table Reproduction Scripts in `experiments/`
- **Files**: Create `experiments/` folder and populate it with:
  1. `experiments/reproduce_table2_casia_accuracy.py`
  2. `experiments/reproduce_table3_time_complexity.py`
  3. `experiments/reproduce_table4_two_stage_vs_one_stage.py`
  4. `experiments/reproduce_table5_feature_comparison.py`
  5. `experiments/reproduce_table6_kernel_comparison.py`
- **Problem**: Missing the 5 experiment scripts required by section 4 of `09_EVALUATION_EXPERIMENTS_SPEC.md`.
- **Required Change**: Write clean scripts that:
  - Load the required config.
  - Run the specific pipeline components or load appropriate feature caches.
  - Print/save the results using the standard report format.
  - Label all non-reproduced external baseline numbers from the paper with `"paper_reported_not_reproduced"`.
- **Acceptance Test**: Run `python experiments/reproduce_table4_two_stage_vs_one_stage.py --config configs/toy.yaml` and verify it generates the summary report without errors.

### Patch 4: Adding `README.md`
- **File**: `README.md`
- **Problem**: Missing general guide on how to install and execute the codebase.
- **Required Change**: Write a README outlining:
  - Prerequisites (`pip install -r requirements.txt`).
  - Dataset structure guidelines.
  - Data preparation and pipeline execution commands.
  - Testing commands (`pytest`).
- **Acceptance Test**: Verify file existence and readability.

---

## 3. P2 — Quality and Reproducibility Improvements

### Patch 5: Creating the `docs/` Folder
- **File**: Create `docs/`
- **Problem**: Missing structured place for documentation assets.
- **Required Change**: Create the `docs/` folder and copy relevant specifications or walkthroughs into it.
- **Acceptance Test**: Verify directory existence.
