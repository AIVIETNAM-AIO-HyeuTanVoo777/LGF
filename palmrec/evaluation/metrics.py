import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
from typing import List, Tuple, Dict, Any

def calculate_classification_metrics(
    y_true: List[str],
    y_pred: List[str]
) -> Dict[str, float]:
    """Calculate accuracy, precision, recall, and F1-score."""
    accuracy = float(accuracy_score(y_true, y_pred))
    
    # Calculate precision, recall, f1
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true,
        y_pred,
        average="macro",
        zero_division=0
    )
    
    return {
        "accuracy": accuracy,
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1)
    }

def calculate_eer(
    genuine_scores: List[float],
    impostor_scores: List[float]
) -> Tuple[float, float]:
    """Calculate the Equal Error Rate (EER) and the corresponding threshold.
    genuine_scores: List of similarity scores of matches from the same palm class.
    impostor_scores: List of similarity scores of matches from different palm classes.
    """
    g_scores = np.array(genuine_scores)
    i_scores = np.array(impostor_scores)
    
    if len(g_scores) == 0 or len(i_scores) == 0:
        return 0.0, 0.0
        
    # Combine and sort all unique thresholds
    thresholds = np.unique(np.concatenate([g_scores, i_scores]))
    thresholds.sort()
    
    eer = 0.5
    eer_threshold = 0.5
    min_diff = 1.0
    
    # Sweep thresholds to find the intersection of FAR and FRR
    for t in thresholds:
        # False Acceptance Rate: Impostors accepted as genuine
        far = np.mean(i_scores >= t)
        # False Rejection Rate: Genuines rejected as impostors
        frr = np.mean(g_scores < t)
        
        diff = np.abs(far - frr)
        if diff < min_diff:
            min_diff = diff
            eer = (far + frr) / 2.0
            eer_threshold = t
            
    return float(eer), float(eer_threshold)

def get_confusion_matrix_df(
    y_true: List[str],
    y_pred: List[str],
    labels: List[str] = None
) -> Tuple[np.ndarray, List[str]]:
    """Generate confusion matrix array and class labels."""
    if labels is None:
        labels = sorted(list(set(y_true) | set(y_pred)))
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    return cm, labels
