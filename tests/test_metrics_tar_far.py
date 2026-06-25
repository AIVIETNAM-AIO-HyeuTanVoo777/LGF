import numpy as np
import pytest

from palmrec.evaluation.metrics import tar_at_far_conservative


def test_tar_at_far_never_exceeds_target_far():
    fpr = np.array([0.0, 0.0008, 0.0012, 0.01])
    tpr = np.array([0.2, 0.7, 0.9, 0.99])
    thresholds = np.array([0.9, 0.8, 0.7, 0.6])

    out = tar_at_far_conservative(fpr, tpr, thresholds, 0.001)

    assert out["empirical_far"] <= 0.001
    assert out["tar"] == 0.7
    assert out["threshold"] == 0.8


def test_tar_at_far_returns_zero_when_no_valid_far():
    fpr = np.array([0.002, 0.003])
    tpr = np.array([0.5, 0.8])
    thresholds = np.array([0.7, 0.6])

    out = tar_at_far_conservative(fpr, tpr, thresholds, 0.001)

    assert out["tar"] == 0.0
    assert out["threshold"] == float("inf")
    assert out["empirical_far"] == 0.0


def test_tar_at_far_rejects_length_mismatch():
    fpr = np.array([0.0, 0.001])
    tpr = np.array([0.2, 0.7])
    thresholds = np.array([0.9])

    with pytest.raises(ValueError):
        tar_at_far_conservative(fpr, tpr, thresholds, 0.001)
