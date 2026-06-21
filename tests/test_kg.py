import numpy as np
import pytest
from palmrec.matching.kg import PalmTemplate, PalmKnowledgeGraph, CosineMatcher, TwoStageRecognizer, MatchResult

@pytest.fixture
def mock_templates():
    t1 = PalmTemplate(
        sample_id="S1", palm_id="P1", subject_id="Sub1",
        gender="male", hand_side="left",
        feature=np.array([1.0, 0.0], dtype=np.float32),
        image_path="/path/1"
    )
    t2 = PalmTemplate(
        sample_id="S2", palm_id="P2", subject_id="Sub2",
        gender="female", hand_side="left",
        feature=np.array([0.0, 1.0], dtype=np.float32),
        image_path="/path/2"
    )
    t3 = PalmTemplate(
        sample_id="S3", palm_id="P3", subject_id="Sub3",
        gender="male", hand_side="right",
        feature=np.array([0.707, 0.707], dtype=np.float32),
        image_path="/path/3"
    )
    t4 = PalmTemplate(
        sample_id="S4", palm_id="P4", subject_id="Sub4",
        gender="female", hand_side="right",
        feature=np.array([-1.0, 0.0], dtype=np.float32),
        image_path="/path/4"
    )
    return [t1, t2, t3, t4]

def test_kg_insertion(mock_templates):
    kg = PalmKnowledgeGraph({"use_gender": True, "use_hand_side": True})
    for t in mock_templates:
        kg.add_template(t)
    assert len(kg.all_templates()) == 4

def test_exact_gender_hand_query(mock_templates):
    kg = PalmKnowledgeGraph({"use_gender": True, "use_hand_side": True})
    for t in mock_templates:
        kg.add_template(t)
        
    candidates = kg.query_candidates(gender="male", hand_side="left")
    assert len(candidates) == 1
    assert candidates[0].sample_id == "S1"

def test_missing_gender_fallback(mock_templates):
    kg = PalmKnowledgeGraph({"use_gender": True, "use_hand_side": True})
    for t in mock_templates:
        kg.add_template(t)
        
    # Gender unknown -> matches both male and female left hands
    candidates = kg.query_candidates(gender="unknown", hand_side="left")
    assert len(candidates) == 2
    assert {c.sample_id for c in candidates} == {"S1", "S2"}

def test_missing_hand_fallback(mock_templates):
    kg = PalmKnowledgeGraph({"use_gender": True, "use_hand_side": True})
    for t in mock_templates:
        kg.add_template(t)
        
    # Hand unknown -> matches both left and right male hands
    candidates = kg.query_candidates(gender="male", hand_side="unknown")
    assert len(candidates) == 2
    assert {c.sample_id for c in candidates} == {"S1", "S3"}

def test_global_fallback(mock_templates):
    kg = PalmKnowledgeGraph({"use_gender": True, "use_hand_side": True})
    for t in mock_templates:
        kg.add_template(t)
        
    # Gender and Hand unknown -> fallback to all templates
    candidates = kg.query_candidates(gender="unknown", hand_side="unknown")
    assert len(candidates) == 4

def test_cosine_matcher_returns_nearest(mock_templates):
    matcher = CosineMatcher()
    query = np.array([0.9, 0.1], dtype=np.float32)
    predicted_palm, predicted_sub, score = matcher.match(query, mock_templates)
    
    assert predicted_palm == "P1"
    assert predicted_sub == "Sub1"
    assert score > 0.89

def test_threshold_returns_unknown():
    matcher = CosineMatcher({"threshold": 0.95})
    t = PalmTemplate(
        sample_id="S1", palm_id="P1", subject_id="Sub1",
        gender="male", hand_side="left",
        feature=np.array([1.0, 0.0], dtype=np.float32),
        image_path="/path/1"
    )
    query = np.array([0.5, 0.866], dtype=np.float32) # cosine sim = 0.5 < 0.95
    predicted_palm, predicted_sub, score = matcher.match(query, [t])
    
    assert predicted_palm == "unknown"
    assert predicted_sub == "unknown"
    assert score < 0.95


def test_two_stage_candidate_count_reduction(mock_templates):
    kg = PalmKnowledgeGraph({"use_gender": True, "use_hand_side": True})
    for t in mock_templates:
        kg.add_template(t)
        
    recognizer = TwoStageRecognizer(kg)
    query = np.array([0.9, 0.1], dtype=np.float32)
    
    # 2-Stage search with known metadata (reduces candidates to 1)
    res_2stage = recognizer.predict_feature(query, gender="male", hand_side="left")
    assert res_2stage.candidate_count == 1
    assert res_2stage.predicted_palm_id == "P1"
    
    # 1-Stage global search
    global_recognizer = TwoStageRecognizer(kg, {"matcher": {"one_stage": True}})
    res_1stage = global_recognizer.predict_feature(query, gender="male", hand_side="left")
    assert res_1stage.candidate_count == 4
    assert res_1stage.predicted_palm_id == "P1"
