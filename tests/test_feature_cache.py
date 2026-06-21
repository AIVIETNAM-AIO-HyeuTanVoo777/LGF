import os
import numpy as np
import pytest
from palmrec.features.feature_cache import save_features, load_features, verify_alignment

@pytest.fixture
def tmp_npz_path(tmp_path):
    return os.path.join(tmp_path, "test_features.npz")

def test_npz_roundtrip(tmp_npz_path):
    # Save dummy features
    feats = np.random.randn(5, 10).astype(np.float32)
    sample_ids = np.array([f"S_{i}" for i in range(5)])
    palm_ids = np.array([f"P_{i}" for i in range(5)])
    subject_ids = np.array([f"Sub_{i}" for i in range(5)])
    gender = np.array(["male"] * 5)
    hand_side = np.array(["left"] * 5)
    image_paths = np.array([f"/path/to/{i}.jpg" for i in range(5)])
    
    save_features(
        path=tmp_npz_path,
        features=feats,
        sample_ids=sample_ids,
        palm_ids=palm_ids,
        subject_ids=subject_ids,
        gender=gender,
        hand_side=hand_side,
        image_paths=image_paths,
        split="train",
        dataset="TOY",
        config_hash="abc123hash"
    )
    
    assert os.path.exists(tmp_npz_path)
    
    # Load back
    loaded = load_features(tmp_npz_path)
    assert np.allclose(loaded.features, feats)
    assert list(loaded.sample_ids) == list(sample_ids)
    assert list(loaded.palm_ids) == list(palm_ids)
    assert list(loaded.subject_ids) == list(subject_ids)
    assert list(loaded.gender) == list(gender)
    assert list(loaded.hand_side) == list(hand_side)
    assert list(loaded.image_paths) == list(image_paths)
    assert loaded.split == "train"
    assert loaded.dataset == "TOY"
    assert loaded.config_hash == "abc123hash"

def test_sample_id_alignment(tmp_npz_path, tmp_path):
    # Create two aligned caches
    feats = np.random.randn(3, 4)
    sample_ids = np.array(["S_1", "S_2", "S_3"])
    
    path_a = os.path.join(tmp_path, "feat_a.npz")
    path_b = os.path.join(tmp_path, "feat_b.npz")
    
    save_features(
        path=path_a, features=feats, sample_ids=sample_ids,
        palm_ids=sample_ids, subject_ids=sample_ids, gender=sample_ids,
        hand_side=sample_ids, image_paths=sample_ids, split="train",
        dataset="TOY", config_hash="h1"
    )
    
    save_features(
        path=path_b, features=feats, sample_ids=sample_ids,
        palm_ids=sample_ids, subject_ids=sample_ids, gender=sample_ids,
        hand_side=sample_ids, image_paths=sample_ids, split="train",
        dataset="TOY", config_hash="h2"
    )
    
    cache_a = load_features(path_a)
    cache_b = load_features(path_b)
    
    # Verify no assertion error
    verify_alignment(cache_a, cache_b)

def test_alignment_error_on_mismatch(tmp_path):
    # Create two mismatched caches
    feats = np.random.randn(3, 4)
    sample_ids_a = np.array(["S_1", "S_2", "S_3"])
    sample_ids_b = np.array(["S_1", "S_2", "S_4"]) # "S_4" instead of "S_3"
    
    path_a = os.path.join(tmp_path, "feat_a.npz")
    path_b = os.path.join(tmp_path, "feat_b.npz")
    
    save_features(
        path=path_a, features=feats, sample_ids=sample_ids_a,
        palm_ids=sample_ids_a, subject_ids=sample_ids_a, gender=sample_ids_a,
        hand_side=sample_ids_a, image_paths=sample_ids_a, split="train",
        dataset="TOY", config_hash="h1"
    )
    
    save_features(
        path=path_b, features=feats, sample_ids=sample_ids_b,
        palm_ids=sample_ids_b, subject_ids=sample_ids_b, gender=sample_ids_b,
        hand_side=sample_ids_b, image_paths=sample_ids_b, split="train",
        dataset="TOY", config_hash="h2"
    )
    
    cache_a = load_features(path_a)
    cache_b = load_features(path_b)
    
    # Assert raise AssertionError
    with pytest.raises(AssertionError):
        verify_alignment(cache_a, cache_b)
