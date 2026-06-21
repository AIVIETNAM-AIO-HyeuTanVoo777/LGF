import os
import sys
import argparse
import numpy as np
import pandas as pd
import hashlib
import joblib
from tqdm import tqdm
from palmrec.utils.config import load_config
from palmrec.utils.seed import set_seed
from palmrec.utils.logging import get_logger
from palmrec.preprocessing.image_io import read_image
from palmrec.preprocessing.roi import IdentityROIExtractor
from palmrec.preprocessing.transforms import preprocess_for_gabor
from palmrec.features.gabor import GaborFeatureExtractor
from palmrec.features.normalization import FeatureNormalizer

def compute_config_hash(gabor_config: dict) -> str:
    """Compute MD5 hash of the Gabor configuration."""
    gabor_str = str(sorted(gabor_config.items()))
    return hashlib.md5(gabor_str.encode('utf-8')).hexdigest()

def main():
    parser = argparse.ArgumentParser(description="Extract Gabor Features")
    parser.add_argument("--config", type=str, required=True, help="Path to config file")
    parser.add_argument("--split", type=str, default="train,test", help="Comma-separated splits to process")
    args = parser.parse_args()

    config = load_config(args.config)
    set_seed(config.project.seed)

    # Output directory
    output_dir = os.path.join(config.project.output_dir, "features", config.dataset.name)
    os.makedirs(output_dir, exist_ok=True)
    
    # Logger
    log_file = os.path.join(config.project.output_dir, "logs", f"extract_gabor_{config.dataset.name}.log")
    logger = get_logger("ExtractGabor", log_file=log_file)
    logger.info(f"Extracting Gabor features for dataset: {config.dataset.name}")

    # Load metadata
    metadata_csv = config.dataset.metadata_csv
    if not os.path.exists(metadata_csv):
        logger.error(f"Metadata file not found: {metadata_csv}. Please run prepare_data.py first.")
        sys.exit(1)
    df = pd.read_csv(metadata_csv)

    # Initialize Gabor extractor
    extractor = GaborFeatureExtractor(config.gabor)
    roi_extractor = IdentityROIExtractor() # default assumption

    # Filter target splits
    target_splits = [s.strip() for s in args.split.split(",")]
    
    # Extract features for all splits first
    raw_features = {}
    split_dfs = {}
    
    for split in target_splits:
        split_df = df[df["split"] == split].reset_index(drop=True)
        if split_df.empty:
            logger.warning(f"No samples found for split: {split}")
            continue
            
        logger.info(f"Extracting raw Gabor features for split '{split}' ({len(split_df)} samples)...")
        features_list = []
        
        for idx, row in tqdm(split_df.iterrows(), total=len(split_df)):
            image_path = row["image_path"]
            try:
                # Read image as grayscale or color and preprocess to grayscale
                img = read_image(image_path, grayscale=False)
                gray_roi = preprocess_for_gabor(img, roi_extractor, tuple(config.gabor.image_size))
                feat = extractor.extract(gray_roi)
                features_list.append(feat)
            except Exception as e:
                logger.error(f"Error extracting Gabor features for {image_path}: {e}")
                # Append zero vector as fallback to maintain alignment, though we expect no errors
                dummy_dim = extractor.extract(np.zeros(config.gabor.image_size, dtype=np.float32)).shape[0]
                features_list.append(np.zeros(dummy_dim, dtype=np.float32))
                
        raw_features[split] = np.stack(features_list, axis=0)
        split_dfs[split] = split_df

    # Normalize features: Fit on train only, transform both
    logger.info("Normalizing features (Standardizing and L2-normalizing)...")
    normalizer = FeatureNormalizer(
        standardize=config.gabor.normalize.get("standardize", True),
        l2=config.gabor.normalize.get("l2", True)
    )
    
    if "train" in raw_features:
        # Fit on train
        normalizer.fit(raw_features["train"])
        # Save normalizer model
        normalizer_path = os.path.join(output_dir, "gabor_normalizer.pkl")
        joblib.dump(normalizer, normalizer_path)
        logger.info(f"Saved Gabor normalizer to {normalizer_path}")
    else:
        # If train not in requested splits, try loading saved normalizer
        normalizer_path = os.path.join(output_dir, "gabor_normalizer.pkl")
        if os.path.exists(normalizer_path):
            normalizer = joblib.load(normalizer_path)
            logger.info(f"Loaded Gabor normalizer from {normalizer_path}")
        else:
            logger.warning("No train features available and no normalizer found. Fitting on whatever split is processed.")
            # Fit on first available split
            first_split = list(raw_features.keys())[0]
            normalizer.fit(raw_features[first_split])
            
    # Compute config hash
    config_hash = compute_config_hash(config.gabor)
    
    # Transform and save
    for split, feats in raw_features.items():
        split_df = split_dfs[split]
        norm_feats = normalizer.transform(feats)
        
        save_path = os.path.join(output_dir, f"gabor_{split}.npz")
        np.savez(
            save_path,
            features=norm_feats,
            sample_ids=split_df["sample_id"].to_numpy(),
            palm_ids=split_df["palm_id"].to_numpy(),
            subject_ids=split_df["subject_id"].to_numpy(),
            gender=split_df["gender"].to_numpy(),
            hand_side=split_df["hand_side"].to_numpy(),
            image_paths=split_df["image_path"].to_numpy(),
            split=split,
            dataset=config.dataset.name,
            config_hash=config_hash
        )
        logger.info(f"Saved Gabor features for split '{split}' (shape: {norm_feats.shape}) to {save_path}")

if __name__ == "__main__":
    main()
