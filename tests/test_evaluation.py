import numpy as np
import pytest
from palmrec.evaluation.metrics import calculate_classification_metrics, calculate_eer, get_confusion_matrix_df
from palmrec.evaluation.timing import LatencyTracker

def test_classification_metrics():
    y_true = ["P1", "P1", "P2", "P2"]
    y_pred = ["P1", "P2", "P2", "P2"]
    
    metrics = calculate_classification_metrics(y_true, y_pred)
    
    assert metrics["accuracy"] == 0.75
    assert "precision" in metrics
    assert "recall" in metrics
    assert "f1_score" in metrics

def test_calculate_eer():
    # Genuine scores should be higher, impostor scores lower
    genuine_scores = [0.8, 0.9, 0.85, 0.95]
    impostor_scores = [0.1, 0.2, 0.15, 0.3]
    
    eer, threshold = calculate_eer(genuine_scores, impostor_scores)
    
    # Perfect separation: EER should be 0.0
    assert eer == 0.0
    assert 0.3 <= threshold <= 0.8

def test_confusion_matrix():
    y_true = ["P1", "P2", "P1"]
    y_pred = ["P1", "P2", "P2"]
    
    cm, labels = get_confusion_matrix_df(y_true, y_pred, labels=["P1", "P2"])
    
    assert labels == ["P1", "P2"]
    # P1 matching P1: 1, P1 matching P2: 1
    # P2 matching P1: 0, P2 matching P2: 1
    expected = np.array([[1, 1], [0, 1]])
    assert np.array_equal(cm, expected)

def test_latency_tracker():
    tracker = LatencyTracker()
    tracker.start("gabor")
    # Simulate work
    import time
    time.sleep(0.1)
    elapsed = tracker.stop("gabor")
    
    assert elapsed >= 0.09
    assert tracker.get_latencies()["gabor"] == elapsed
