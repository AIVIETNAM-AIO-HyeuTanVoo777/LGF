import pandas as pd
import numpy as np
from typing import Tuple, Dict, List
import logging

logger = logging.getLogger(__name__)

def create_half_split(
    metadata: pd.DataFrame,
    class_key: str = "palm_id",
    seed: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame, List[str]]:
    """Split metadata into train and test 1:1 per class_key.
    If a category has an odd number of valid samples, one is randomly removed before splitting.
    """
    train_indices = []
    test_indices = []
    dropped_sample_ids = []
    
    # We group by the unique palm_id
    grouped = metadata.groupby(class_key)
    
    # For reproducibility, we sort palm_ids and use a local random generator per group or global with offsets
    # Using np.random.RandomState with seed
    rng = np.random.RandomState(seed)
    
    for class_val, group in sorted(grouped, key=lambda x: x[0]):
        # Only split valid rows
        valid_group = group[group["is_valid"] == True]
        indices = valid_group.index.tolist()
        
        # Shuffle indices deterministically
        shuffled_indices = list(rng.permutation(indices))
        
        if len(shuffled_indices) % 2 == 1:
            # Randomly remove one index (since shuffled, we pop the last one)
            dropped_idx = shuffled_indices.pop()
            dropped_sample_id = metadata.loc[dropped_idx, "sample_id"]
            dropped_sample_ids.append(dropped_sample_id)
            logger.info(f"IMPLEMENTATION ASSUMPTION: Dropped odd sample {dropped_sample_id} from class {class_val}")
            
        n = len(shuffled_indices) // 2
        train_indices.extend(shuffled_indices[:n])
        test_indices.extend(shuffled_indices[n:])
        
    train_df = metadata.loc[train_indices].copy()
    test_df = metadata.loc[test_indices].copy()
    
    return train_df, test_df, dropped_sample_ids
