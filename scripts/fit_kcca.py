import os
import sys
import argparse
import numpy as np
from palmrec.utils.config import load_config
from palmrec.utils.seed import set_seed
from palmrec.utils.logging import get_logger
from palmrec.features.feature_cache import load_features, verify_alignment, save_features
from palmrec.fusion.kcca import KCCAFusion

def main():
    parser = argparse.ArgumentParser(description="Fuse Features using KCCA")
    parser.add_argument("--config", type=str, required=True, help="Path to config file")
    args = parser.parse_args()

    config = load_config(args.config)
    set_seed(config.project.seed)

    # Directory resolving
    feature_dir = os.path.join(config.project.output_dir, "features", config.dataset.name)
    os.makedirs(feature_dir, exist_ok=True)
    
    # Logger
    log_file = os.path.join(config.project.output_dir, "logs", f"fit_kcca_{config.dataset.name}.log")
    logger = get_logger("FitKCCA", log_file=log_file)
    logger.info(f"Fusing Gabor and Conformer features for dataset: {config.dataset.name}")

    # Paths to source features
    gabor_train_path = os.path.join(feature_dir, "gabor_train.npz")
    gabor_test_path = os.path.join(feature_dir, "gabor_test.npz")
    conformer_train_path = os.path.join(feature_dir, "conformer_train.npz")
    conformer_test_path = os.path.join(feature_dir, "conformer_test.npz")

    # Verify existence
    for path in [gabor_train_path, gabor_test_path, conformer_train_path, conformer_test_path]:
        if not os.path.exists(path):
            logger.error(f"Required feature file not found: {path}. Run feature extraction scripts first.")
            sys.exit(1)

    # 1. Load Train Features
    logger.info("Loading training features...")
    gabor_train = load_features(gabor_train_path)
    conformer_train = load_features(conformer_train_path)
    
    # Verify alignment
    verify_alignment(gabor_train, conformer_train)
    logger.info("Training features successfully aligned.")

    # 2. Fit KCCA model
    kcca = KCCAFusion(config.kcca)
    logger.info("Fitting KCCA model on training set...")
    kcca.fit(gabor_train.features, conformer_train.features)

    # Save KCCA model
    kcca_model_path = config.kcca.get("save_path", os.path.join(feature_dir, "kcca_model.pkl"))
    os.makedirs(os.path.dirname(kcca_model_path), exist_ok=True)
    kcca.save(kcca_model_path)
    logger.info(f"Saved KCCA model checkpoint to {kcca_model_path}")

    # 3. Fuse Train features
    logger.info("Fusing training features...")
    fused_train_features = kcca.transform(gabor_train.features, conformer_train.features)
    
    fused_train_path = os.path.join(feature_dir, "fused_train.npz")
    save_features(
        path=fused_train_path,
        features=fused_train_features,
        sample_ids=np.array(gabor_train.sample_ids),
        palm_ids=np.array(gabor_train.palm_ids),
        subject_ids=np.array(gabor_train.subject_ids),
        gender=np.array(gabor_train.gender),
        hand_side=np.array(gabor_train.hand_side),
        image_paths=np.array(gabor_train.image_paths),
        split="train",
        dataset=config.dataset.name,
        config_hash=gabor_train.config_hash
    )
    logger.info(f"Saved fused training features to {fused_train_path} (shape: {fused_train_features.shape})")

    # 4. Load Test Features and Fuse
    logger.info("Loading testing features...")
    gabor_test = load_features(gabor_test_path)
    conformer_test = load_features(conformer_test_path)
    
    verify_alignment(gabor_test, conformer_test)
    logger.info("Testing features successfully aligned.")
    
    logger.info("Fusing testing features...")
    fused_test_features = kcca.transform(gabor_test.features, conformer_test.features)
    
    fused_test_path = os.path.join(feature_dir, "fused_test.npz")
    save_features(
        path=fused_test_path,
        features=fused_test_features,
        sample_ids=np.array(gabor_test.sample_ids),
        palm_ids=np.array(gabor_test.palm_ids),
        subject_ids=np.array(gabor_test.subject_ids),
        gender=np.array(gabor_test.gender),
        hand_side=np.array(gabor_test.hand_side),
        image_paths=np.array(gabor_test.image_paths),
        split="test",
        dataset=config.dataset.name,
        config_hash=gabor_test.config_hash
    )
    logger.info(f"Saved fused testing features to {fused_test_path} (shape: {fused_test_features.shape})")

if __name__ == "__main__":
    main()
