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


def conservative_tar_at_far(genuine_scores, impostor_scores, target_far, eps=1e-12):
    genuine_scores = np.asarray(genuine_scores, dtype=np.float64)
    impostor_scores = np.asarray(impostor_scores, dtype=np.float64)
    if genuine_scores.size == 0:
        raise ValueError("genuine_scores is empty")
    if impostor_scores.size == 0:
        raise ValueError("impostor_scores is empty")
    if not (0.0 <= target_far <= 1.0):
        raise ValueError(f"target_far must be in [0,1], got {target_far}")

    # Sort genuine and impostor scores
    gen_sorted = np.sort(genuine_scores)
    imp_sorted = np.sort(impostor_scores)

    # Get unique thresholds, including sentinels
    unique_thresholds = np.unique(np.concatenate([gen_sorted, imp_sorted]))
    thresholds = np.concatenate([[np.inf], unique_thresholds[::-1], [-np.inf]])

    # Vectorized computation of empirical FAR and TAR
    imp_counts = imp_sorted.size - np.searchsorted(imp_sorted, thresholds, side='left')
    gen_counts = gen_sorted.size - np.searchsorted(gen_sorted, thresholds, side='left')

    empirical_fars = imp_counts / imp_sorted.size
    tars = gen_counts / gen_sorted.size

    # Filter by FAR constraint
    valid = empirical_fars <= target_far + eps
    if not np.any(valid):
        raise RuntimeError("No threshold satisfies conservative FAR constraint")

    valid_indices = np.where(valid)[0]
    valid_tars = tars[valid_indices]

    # Find maximum TAR
    max_tar = np.max(valid_tars)
    # Get all indices with max TAR (within epsilon)
    tie_indices = valid_indices[np.abs(valid_tars - max_tar) <= eps]
    
    # Among ties, select the one with the maximum empirical FAR
    best_idx = tie_indices[np.argmax(empirical_fars[tie_indices])]

    best_tar = float(tars[best_idx])
    best_threshold = float(thresholds[best_idx])
    best_far = float(empirical_fars[best_idx])

    if best_far > target_far + eps:
        raise AssertionError(f"Conservative FAR violated: {best_far} > {target_far}")

    return {
        "tar": best_tar,
        "threshold": best_threshold,
        "empirical_far": best_far,
        "target_far": float(target_far),
        "n_genuine": int(genuine_scores.size),
        "n_impostor": int(impostor_scores.size),
        "far_step": float(1.0 / impostor_scores.size),
    }


def tar_at_far_conservative(
    fpr: np.ndarray,
    tpr: np.ndarray,
    thresholds: np.ndarray,
    target_far: float,
) -> Dict[str, float]:
    """Return TAR at a target FAR using a conservative empirical-FAR rule.

    The selected ROC point must satisfy empirical FPR <= target_far.
    Among valid points, the function returns the point with the highest TPR.
    """
    fpr = np.asarray(fpr, dtype=float)
    tpr = np.asarray(tpr, dtype=float)
    thresholds = np.asarray(thresholds, dtype=float)

    if fpr.ndim != 1 or tpr.ndim != 1 or thresholds.ndim != 1:
        raise ValueError(
            "fpr, tpr, and thresholds must be one-dimensional arrays; "
            f"got shapes {fpr.shape}, {tpr.shape}, {thresholds.shape}"
        )

    if not (len(fpr) == len(tpr) == len(thresholds)):
        raise ValueError(
            "fpr, tpr, and thresholds must have identical lengths; "
            f"got {len(fpr)}, {len(tpr)}, {len(thresholds)}"
        )

    if target_far < 0.0 or target_far > 1.0:
        raise ValueError(f"target_far must be in [0, 1], got {target_far}")

    valid = fpr <= target_far
    if not valid.any():
        return {
            "tar": 0.0,
            "threshold": float("inf"),
            "empirical_far": 0.0,
            "target_far": float(target_far),
        }

    idx_valid = np.where(valid)[0]
    best_local = idx_valid[np.argmax(tpr[idx_valid])]

    return {
        "tar": float(tpr[best_local]),
        "threshold": float(thresholds[best_local]),
        "empirical_far": float(fpr[best_local]),
        "target_far": float(target_far),
    }

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
