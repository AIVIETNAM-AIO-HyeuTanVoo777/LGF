import os
import pandas as pd
import json
import pytest
import numpy as np
from palmrec.datasets.metadata import parse_image_metadata, METADATA_COLUMNS
from palmrec.datasets.splits import create_half_split

def test_metadata_schema():
    # Test that a parsed row fits the metadata schema columns
    dummy_path = "data/raw/CASIA/001_l_1.jpg"
    meta = parse_image_metadata(dummy_path, "CASIA")
    
    # Check that all keys in METADATA_COLUMNS are present
    for col in METADATA_COLUMNS:
        if col != "class_id": # class_id is added in dataframe step
            assert col in meta, f"Metadata must contain {col}"
            
    assert meta["dataset"] == "CASIA"
    assert meta["subject_id"] == "001"
    assert meta["hand_side"] == "left"
    assert meta["palm_id"] == "001_left"

def test_split_even_class():
    # Test 1:1 split on class with even number of samples (e.g. 6 samples)
    data = []
    for i in range(6):
        data.append({
            "sample_id": f"S_{i}",
            "palm_id": "P_1",
            "is_valid": True
        })
    df = pd.DataFrame(data)
    
    train, test, dropped = create_half_split(df, class_key="palm_id", seed=42)
    
    assert len(train) == 3
    assert len(test) == 3
    assert len(dropped) == 0
    # No overlap
    assert set(train["sample_id"]).isdisjoint(set(test["sample_id"]))

def test_split_odd_class_drops_one():
    # Test 1:1 split on class with odd number of samples (e.g. 7 samples)
    data = []
    for i in range(7):
        data.append({
            "sample_id": f"S_{i}",
            "palm_id": "P_1",
            "is_valid": True
        })
    df = pd.DataFrame(data)
    
    train, test, dropped = create_half_split(df, class_key="palm_id", seed=42)
    
    assert len(train) == 3
    assert len(test) == 3
    assert len(dropped) == 1
    assert dropped[0] in df["sample_id"].tolist()
    # No overlap
    assert set(train["sample_id"]).isdisjoint(set(test["sample_id"]))

def test_split_reproducibility():
    # Test that the same seed produces identical split
    data = []
    for p in ["P_1", "P_2"]:
        for i in range(5): # 5 samples each (odd)
            data.append({
                "sample_id": f"{p}_{i}",
                "palm_id": p,
                "is_valid": True
            })
    df = pd.DataFrame(data)
    
    train1, test1, dropped1 = create_half_split(df, class_key="palm_id", seed=100)
    train2, test2, dropped2 = create_half_split(df, class_key="palm_id", seed=100)
    
    assert list(train1["sample_id"]) == list(train2["sample_id"])
    assert list(test1["sample_id"]) == list(test2["sample_id"])
    assert dropped1 == dropped2

def test_no_train_test_overlap():
    # Test that train and test have no overlap across multiple classes
    data = []
    for p in ["P_1", "P_2", "P_3"]:
        for i in range(4):
            data.append({
                "sample_id": f"{p}_{i}",
                "palm_id": p,
                "is_valid": True
            })
    df = pd.DataFrame(data)
    
    train, test, dropped = create_half_split(df, class_key="palm_id", seed=42)
    
    train_ids = set(train["sample_id"])
    test_ids = set(test["sample_id"])
    
    assert len(train_ids & test_ids) == 0
    assert len(train) == 6
    assert len(test) == 6
