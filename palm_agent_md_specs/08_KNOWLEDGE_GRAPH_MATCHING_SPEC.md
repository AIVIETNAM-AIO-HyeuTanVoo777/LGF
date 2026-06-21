# Knowledge Graph and Matching Specification

## 1. Paper requirements

The knowledge graph must use prior information to reduce feature search space.

Paper graph structure:

```text
Layer 1: gender
Layer 2: left/right hand
Layer 3: palmprint ID / feature templates
```

Matching:

```text
candidate filtering by graph
→ cosine similarity inside candidate subset
→ predicted palm ID
```

## 2. Required classes

```python
@dataclass
class PalmTemplate:
    sample_id: str
    palm_id: str
    subject_id: str
    gender: str
    hand_side: str
    feature: np.ndarray
    image_path: str
```

```python
class PalmKnowledgeGraph:
    def add_template(self, template: PalmTemplate) -> None:
        ...

    def query_candidates(self, gender=None, hand_side=None) -> list[PalmTemplate]:
        ...

    def all_templates(self) -> list[PalmTemplate]:
        ...

    def save(self, path: str) -> None:
        ...

    @classmethod
    def load(cls, path: str) -> "PalmKnowledgeGraph":
        ...
```

```python
class CosineMatcher:
    def match(self, query: np.ndarray, candidates: list[PalmTemplate]) -> MatchResult:
        ...
```

```python
class TwoStageRecognizer:
    def predict_feature(self, feature, gender=None, hand_side=None) -> MatchResult:
        ...
```

## 3. Graph storage

Default efficient structure:

```python
graph = {
    gender: {
        hand_side: {
            palm_id: [PalmTemplate, PalmTemplate, ...]
        }
    }
}
```

Required canonical values:

```text
gender ∈ {"male", "female", "unknown"}
hand_side ∈ {"left", "right", "unknown"}
```

## 4. Query fallback

```python
if gender known and hand_side known:
    search graph[gender][hand_side]
elif gender known and hand_side unknown:
    search all hand sides under graph[gender]
elif gender unknown and hand_side known:
    search all genders with that hand side
else:
    global search
```

If candidate set is empty:

```text
fallback to global search if config.matcher.fallback_global = true
```

## 5. Cosine similarity

```python
def cosine_similarity(query, gallery, eps=1e-12):
    query = query / (np.linalg.norm(query) + eps)
    gallery = gallery / (np.linalg.norm(gallery, axis=1, keepdims=True) + eps)
    return gallery @ query
```

## 6. Matching result

```python
@dataclass
class MatchResult:
    predicted_palm_id: str
    predicted_subject_id: str
    score: float
    candidate_count: int
    used_fallback: bool
    timing: dict
```

## 7. Threshold

Paper mentions a predefined threshold but does not give a value.

Default assumption:

```yaml
matcher:
  threshold: null
```

Behavior:

- If `threshold = null`, return best candidate.
- If threshold is set and best similarity < threshold, return `"unknown"`.

## 8. Two-stage vs one-stage

Implement both:

### One-stage

```text
search all templates globally
```

### Two-stage

```text
filter by gender/hand_side graph partition
search only selected templates
```

Both must use same cosine matcher.

## 9. Optional graph-walk mode

Paper mentions moving toward the most similar node until no further movement is possible, but does not define edge construction.

Default reproducible mode:

```text
exhaustive cosine search inside selected partition
```

Optional experimental mode:

```text
build kNN graph inside each partition
start from centroid/entry node
walk to neighbor with higher similarity
stop at local maximum
```

Do not make graph-walk the default unless thoroughly tested.

## 10. Tests

- graph insertion.
- exact gender+hand query.
- missing gender fallback.
- missing hand fallback.
- global fallback.
- cosine matcher returns nearest candidate.
- threshold returns unknown when appropriate.
- two-stage candidate count is less than or equal to global candidate count.
