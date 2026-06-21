import os
import time
import joblib
import numpy as np
from dataclasses import dataclass
from typing import Dict, Any, List, Tuple

@dataclass
class PalmTemplate:
    sample_id: str
    palm_id: str
    subject_id: str
    gender: str
    hand_side: str
    feature: np.ndarray
    image_path: str

@dataclass
class MatchResult:
    predicted_palm_id: str
    predicted_subject_id: str
    score: float
    candidate_count: int
    used_fallback: bool
    timing: dict

class PalmKnowledgeGraph:
    """Graph structure partition manager storing templates by gender, hand side and palm ID.
    Maps to paper section: Knowledge graph construction and candidate matching.
    """
    def __init__(self, config: Dict[str, Any] = None) -> None:
        self.config = config or {}
        self.match_gender = self.config.get("use_gender", True)
        self.match_hand = self.config.get("use_hand_side", True)
        
        # gender -> hand_side -> palm_id -> [PalmTemplate]
        self.graph = {}
        self.templates_list = []

    def add_template(self, template: PalmTemplate) -> None:
        gender = str(template.gender).lower()
        if gender not in ["male", "female"]:
            gender = "unknown"
            
        hand = str(template.hand_side).lower()
        if hand not in ["left", "right"]:
            hand = "unknown"
            
        if gender not in self.graph:
            self.graph[gender] = {}
        if hand not in self.graph[gender]:
            self.graph[gender][hand] = {}
        if template.palm_id not in self.graph[gender][hand]:
            self.graph[gender][hand][template.palm_id] = []
            
        self.graph[gender][hand][template.palm_id].append(template)
        self.templates_list.append(template)

    def query_candidates(self, gender: str = None, hand_side: str = None) -> List[PalmTemplate]:
        g = str(gender).lower() if gender else "unknown"
        h = str(hand_side).lower() if hand_side else "unknown"
        
        # Determine genders to search
        genders_to_search = []
        if self.match_gender and g in ["male", "female"]:
            genders_to_search.append(g)
        else:
            genders_to_search = list(self.graph.keys())
            
        # Determine hands to search
        hands_to_search = []
        if self.match_hand and h in ["left", "right"]:
            hands_to_search.append(h)
        else:
            hands_to_search = ["left", "right", "unknown"]
            
        candidates = []
        for gender_key in genders_to_search:
            gender_dict = self.graph.get(gender_key, {})
            for hand_key in hands_to_search:
                palm_dict = gender_dict.get(hand_key, {})
                for palm_id, templates in palm_dict.items():
                    candidates.extend(templates)
        return candidates

    def all_templates(self) -> List[PalmTemplate]:
        return self.templates_list

    def save(self, path: str) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump(self, path)

    @classmethod
    def load(cls, path: str) -> "PalmKnowledgeGraph":
        return joblib.load(path)


class CosineMatcher:
    """Perform cosine similarity matching between a query feature and candidate templates."""
    def __init__(self, config: Dict[str, Any] = None) -> None:
        self.config = config or {}
        self.threshold = self.config.get("threshold", None)

    def match(self, query: np.ndarray, candidates: List[PalmTemplate]) -> Tuple[str, str, float]:
        """Returns: (predicted_palm_id, predicted_subject_id, similarity_score)"""
        if not candidates:
            return "unknown", "unknown", 0.0

        max_sim = -2.0
        best_palm = "unknown"
        best_subject = "unknown"
        
        # Normalize query vector
        q_norm = np.linalg.norm(query)
        q_normed = query / (q_norm + 1e-12) if q_norm > 0 else query
        
        for cand in candidates:
            c_feat = cand.feature
            c_norm = np.linalg.norm(c_feat)
            c_normed = c_feat / (c_norm + 1e-12) if c_norm > 0 else c_feat
            
            sim = float(np.dot(q_normed, c_normed))
            if sim > max_sim:
                max_sim = sim
                best_palm = cand.palm_id
                best_subject = cand.subject_id
                
        if self.threshold is not None and max_sim < self.threshold:
            return "unknown", "unknown", max_sim
            
        return best_palm, best_subject, max_sim


class TwoStageRecognizer:
    """Two-stage classifier utilizing the Knowledge Graph to partition candidates and match features."""
    def __init__(self, graph: PalmKnowledgeGraph, config: Dict[str, Any] = None) -> None:
        self.graph = graph
        self.config = config or {}
        self.matcher = CosineMatcher(self.config.get("matcher", {}))
        self.fallback_global = self.config.get("matcher", {}).get("fallback_global", True)
        self.one_stage = self.config.get("matcher", {}).get("one_stage", False)

    def predict_feature(self, feature: np.ndarray, gender: str = None, hand_side: str = None) -> MatchResult:
        t_start = time.perf_counter()
        
        used_fallback = False
        if self.one_stage:
            candidates = self.graph.all_templates()
        else:
            candidates = self.graph.query_candidates(gender, hand_side)
            if not candidates and self.fallback_global:
                candidates = self.graph.all_templates()
                used_fallback = True
                
        candidate_count = len(candidates)
        predicted_palm, predicted_sub, score = self.matcher.match(feature, candidates)
        
        elapsed = time.perf_counter() - t_start
        timing = {"matching_time_seconds": elapsed}
        
        return MatchResult(
            predicted_palm_id=predicted_palm,
            predicted_subject_id=predicted_sub,
            score=score,
            candidate_count=candidate_count,
            used_fallback=used_fallback,
            timing=timing
        )
