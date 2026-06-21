import os
import sys
import argparse
import numpy as np
import pandas as pd
import hashlib
import torch
import joblib
from torch.utils.data import DataLoader
from tqdm import tqdm
from palmrec.utils.config import load_config
from palmrec.utils.seed import set_seed
from palmrec.utils.logging import get_logger
from palmrec.preprocessing.roi import IdentityROIExtractor
from palmrec.preprocessing.transforms import ConformerTransform
from palmrec.datasets.base import PalmprintDataset
from palmrec.models.conformer import PalmConformer
from palmrec.training.checkpoint import load_checkpoint
from palmrec.features.normalization import FeatureNormalizer

def compute_config_hash(conformer_config: dict) -> str:
    """Compute MD5 hash of the Conformer configuration."""
    conf_str = str(sorted(conformer_config.items()))
    return hashlib.md5(conf_str.encode('utf-8')).hexdigest()

def main():
    parser = argparse.ArgumentParser(description="Extract Conformer Features")
    parser.add_argument("--config", type=str, required=True, help="Path to config file")
    parser.add_argument("--split", type=str, default="train,test", help="Comma-separated splits to process")
    args = parser.parse_args()

    config = load_config(args.config)
    set_seed(config.project.seed)

    # Output directory
    output_dir = os.path.join(config.project.output_dir, "features", config.dataset.name)
    os.makedirs(output_dir, exist_ok=True)
    
    # Logger
    log_file = os.path.join(config.project.output_dir, "logs", f"extract_conformer_{config.dataset.name}.log")
    logger = get_logger("ExtractConformer", log_file=log_file)
    logger.info(f"Extracting Conformer features for dataset: {config.dataset.name}")

    # Load metadata
    metadata_csv = config.dataset.metadata_csv
    if not os.path.exists(metadata_csv):
        logger.error(f"Metadata file not found: {metadata_csv}. Run prepare_data.py first.")
        sys.exit(1)
    df = pd.read_csv(metadata_csv)

    # Resolve device
    device_str = config.project.device
    if device_str == "cuda" and not torch.cuda.is_available():
        device_str = "cpu"
    device = torch.device(device_str)

    # Determine classes count
    num_classes = int(df["class_id"].max() + 1)
    config.conformer.num_classes = num_classes

    # Load trained model
    logger.info("Initializing model and loading checkpoint weights...")
    model = PalmConformer(config.conformer)
    
    checkpoint_path = config.conformer.get("checkpoint_path", "")
    if os.path.exists(checkpoint_path):
        checkpoint = load_checkpoint(checkpoint_path, device)
        model.load_state_dict(checkpoint["model_state_dict"])
        logger.info(f"Successfully loaded trained weights from {checkpoint_path}")
    else:
        logger.warning(f"Trained checkpoint not found at {checkpoint_path}. Using randomly initialized model weights!")
        
    model.to(device)
    model.eval()

    # Preprocessing transform
    roi_extractor = IdentityROIExtractor()
    transform = ConformerTransform(
        roi_extractor=roi_extractor,
        target_size=tuple(config.preprocessing.resize),
        mean=tuple(config.preprocessing.normalize_conformer.mean),
        std=tuple(config.preprocessing.normalize_conformer.std)
    )

    target_splits = [s.strip() for s in args.split.split(",")]
    raw_features = {}
    split_dfs = {}

    # Extract deep features split-by-split
    for split in target_splits:
        split_df = df[df["split"] == split].reset_index(drop=True)
        if split_df.empty:
            continue
            
        logger.info(f"Extracting deep Conformer features for split '{split}' ({len(split_df)} samples)...")
        dataset = PalmprintDataset(split_df, transform=transform)
        loader = DataLoader(dataset, batch_size=int(config.training.batch_size), shuffle=False, num_workers=0)
        
        features_list = []
        with torch.no_grad():
            for batch in tqdm(loader):
                images = batch["image"].to(device)
                feats = model.extract_features(images) # [B, feature_dim]
                features_list.append(feats.cpu().numpy())
                
        raw_features[split] = np.concatenate(features_list, axis=0)
        split_dfs[split] = split_df

    # Normalize: Standardize and L2-normalize Conformer features (standardize fit on train only)
    logger.info("Normalizing Conformer features...")
    # For deep features, standardize might be set to False or True. Let's make it configurable
    standardize = config.conformer.get("standardize_features", False) # usually False for pre-trained activations, let's allow configuring it
    normalizer = FeatureNormalizer(standardize=standardize, l2=True)
    
    if "train" in raw_features:
        normalizer.fit(raw_features["train"])
        normalizer_path = os.path.join(output_dir, "conformer_normalizer.pkl")
        joblib.dump(normalizer, normalizer_path)
    else:
        normalizer_path = os.path.join(output_dir, "conformer_normalizer.pkl")
        if os.path.exists(normalizer_path):
            normalizer = joblib.load(normalizer_path)
            logger.info("Loaded Conformer normalizer.")
        else:
            first_split = list(raw_features.keys())[0]
            normalizer.fit(raw_features[first_split])
            
    config_hash = compute_config_hash(config.conformer)

    # Save features
    for split, feats in raw_features.items():
        split_df = split_dfs[split]
        norm_feats = normalizer.transform(feats)
        
        save_path = os.path.join(output_dir, f"conformer_{split}.npz")
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
        logger.info(f"Saved Conformer features for split '{split}' (shape: {norm_feats.shape}) to {save_path}")

if __name__ == "__main__":
    main()
