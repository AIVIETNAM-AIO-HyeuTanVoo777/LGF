import numpy as np
import pytest

from palmrec.evaluation.metrics import conservative_tar_at_far, tar_at_far_conservative


def test_conservative_tar_does_not_exceed_far():
    genuine = np.array([0.9, 0.8, 0.7])
    impostor = np.array([0.85, 0.1, 0.0])
    # Target FAR = 0.2
    # thresholds swept include 0.9 (empirical FAR = 0.0 <= 0.2)
    # So maximum TAR with FAR <= 0.2 is 1/3 (0.3333333333333333) at threshold 0.9
    out = conservative_tar_at_far(genuine, impostor, target_far=0.2)
    assert out["empirical_far"] <= 0.2
    assert out["empirical_far"] == 0.0
    assert out["tar"] == pytest.approx(1.0 / 3.0)
    assert out["threshold"] == 0.9


def test_toy_example_nearest_exceeds_conservative_correct():
    # Construct a toy example where nearest ROC point would exceed target.
    # genuine: 5 scores of 0.8, 4 of 0.7, 1 of 0.1
    # impostor: 5 scores of 0.8, 4 of 0.7, 41 of 0.1 (50 total)
    # Target FAR = 0.15
    # Thresholds:
    # 0.8: FAR = 5/50 = 0.1 (distance to 0.15 is 0.05), TAR = 5/10 = 0.5
    # 0.7: FAR = 9/50 = 0.18 (distance to 0.15 is 0.03), TAR = 9/10 = 0.9
    # The nearest ROC point is 0.7 (FAR = 0.18, which exceeds target 0.15)
    # The conservative rule must select 0.8 (FAR = 0.1 <= 0.15, TAR = 0.5)
    genuine = np.array([0.8]*5 + [0.7]*4 + [0.1]*1)
    impostor = np.array([0.8]*5 + [0.7]*4 + [0.1]*41)
    
    out = conservative_tar_at_far(genuine, impostor, target_far=0.15)
    assert out["empirical_far"] <= 0.15
    assert out["empirical_far"] == 0.1
    assert out["tar"] == 0.5
    assert out["threshold"] == 0.8


def test_far_step_is_one_over_n_impostor():
    genuine = np.array([0.9, 0.8])
    impostor = np.array([0.5, 0.4, 0.3, 0.2, 0.1])
    out = conservative_tar_at_far(genuine, impostor, target_far=0.5)
    assert out["far_step"] == 1.0 / 5.0
    assert out["n_genuine"] == 2
    assert out["n_impostor"] == 5


def test_accept_rule_score_gte_threshold():
    genuine = np.array([0.8])
    impostor = np.array([0.8])
    # threshold = 0.8 should accept both since score >= threshold (0.8 >= 0.8 is True)
    out = conservative_tar_at_far(genuine, impostor, target_far=1.0)
    assert out["empirical_far"] == 1.0
    assert out["tar"] == 1.0
    assert out["threshold"] == 0.8


def test_empty_arrays_raise_errors():
    with pytest.raises(ValueError):
        conservative_tar_at_far(np.array([]), np.array([0.5]), 0.1)
    with pytest.raises(ValueError):
        conservative_tar_at_far(np.array([0.5]), np.array([]), 0.1)


# Legacy tests for compatibility/regression check on tar_at_far_conservative
def test_legacy_tar_at_far_never_exceeds_target_far():
    fpr = np.array([0.0, 0.0008, 0.0012, 0.01])
    tpr = np.array([0.2, 0.7, 0.9, 0.99])
    thresholds = np.array([0.9, 0.8, 0.7, 0.6])

    out = tar_at_far_conservative(fpr, tpr, thresholds, 0.001)

    assert out["empirical_far"] <= 0.001
    assert out["tar"] == 0.7
    assert out["threshold"] == 0.8


def test_legacy_tar_at_far_returns_zero_when_no_valid_far():
    fpr = np.array([0.002, 0.003])
    tpr = np.array([0.5, 0.8])
    thresholds = np.array([0.7, 0.6])

    out = tar_at_far_conservative(fpr, tpr, thresholds, 0.001)

    assert out["tar"] == 0.0
    assert out["threshold"] == float("inf")
    assert out["empirical_far"] == 0.0


def test_legacy_tar_at_far_rejects_length_mismatch():
    fpr = np.array([0.0, 0.001])
    tpr = np.array([0.2, 0.7])
    thresholds = np.array([0.9])

    with pytest.raises(ValueError):
        tar_at_far_conservative(fpr, tpr, thresholds, 0.001)
