import os
import sys
import argparse
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from palmrec.utils.config import load_config
from palmrec.utils.seed import set_seed
from palmrec.utils.logging import get_logger
from palmrec.preprocessing.roi import IdentityROIExtractor
from palmrec.preprocessing.transforms import ConformerTransform
from palmrec.datasets.base import PalmprintDataset
from palmrec.models.conformer import PalmConformer
from palmrec.training import get_optimizer, get_scheduler, run_training

def main():
    parser = argparse.ArgumentParser(description="Train Conformer Model")
    parser.add_argument("--config", type=str, required=True, help="Path to config file")
    args = parser.parse_args()

    config = load_config(args.config)
    set_seed(config.project.seed)

    # Output checkpoint directory
    checkpoint_dir = os.path.join(config.project.output_dir, "checkpoints", config.dataset.name)
    os.makedirs(checkpoint_dir, exist_ok=True)
    
    # Logger
    log_file = os.path.join(config.project.output_dir, "logs", f"train_conformer_{config.dataset.name}.log")
    logger = get_logger("TrainConformer", log_file=log_file)
    logger.info(f"Training Conformer for dataset: {config.dataset.name}")

    # Load metadata
    metadata_csv = config.dataset.metadata_csv
    if not os.path.exists(metadata_csv):
        logger.error(f"Metadata file not found: {metadata_csv}. Please run prepare_data.py first.")
        sys.exit(1)
    df = pd.read_csv(metadata_csv)

    # Filter train and test
    train_df = df[df["split"] == "train"].reset_index(drop=True)
    test_df = df[df["split"] == "test"].reset_index(drop=True)
    
    if train_df.empty:
        logger.error("No training samples found in metadata.")
        sys.exit(1)
        
    num_classes = int(df["class_id"].max() + 1)
    logger.info(f"Detected {num_classes} unique palm classes from metadata.")
    
    # Configure Conformer model classes count
    config.conformer.num_classes = num_classes

    # Setup transform
    roi_extractor = IdentityROIExtractor()
    transform = ConformerTransform(
        roi_extractor=roi_extractor,
        target_size=tuple(config.preprocessing.resize),
        mean=tuple(config.preprocessing.normalize_conformer.mean),
        std=tuple(config.preprocessing.normalize_conformer.std)
    )

    # Create PyTorch datasets
    train_dataset = PalmprintDataset(train_df, transform=transform)
    test_dataset = PalmprintDataset(test_df, transform=transform)

    # Create DataLoaders
    batch_size = int(config.training.batch_size)
    num_workers = int(config.training.get("num_workers", 0))
    
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True
    )
    
    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True
    )

    # Device selection
    device_str = config.project.device
    if device_str == "cuda" and not torch.cuda.is_available():
        logger.warning("CUDA is configured but not available. Falling back to CPU.")
        device_str = "cpu"
    device = torch.device(device_str)
    logger.info(f"Using device: {device}")

    # Build model
    logger.info("Building Conformer model...")
    model = PalmConformer(config.conformer)
    model.to(device)

    # Setup optimizer, scheduler, loss
    optimizer = get_optimizer(model, config.training)
    scheduler = get_scheduler(optimizer, config.training)
    
    # Default loss: cross entropy
    if config.training.loss == "cross_entropy":
        criterion = nn.CrossEntropyLoss()
    else:
        raise ValueError(f"Unsupported loss: {config.training.loss}")

    # Map class_id to palm_id for checkpoint storage
    class_id_to_palm_id = dict(zip(df["class_id"], df["palm_id"]))
    # Convert keys to int (json/state standard)
    class_id_to_palm_id = {int(k): str(v) for k, v in class_id_to_palm_id.items()}

    # Run training
    logger.info("Starting training loop...")
    epochs = int(config.training.epochs)
    mixed_precision = config.training.get("mixed_precision", False)
    
    run_training(
        model=model,
        train_loader=train_loader,
        val_loader=test_loader,
        optimizer=optimizer,
        scheduler=scheduler,
        criterion=criterion,
        epochs=epochs,
        device=device,
        checkpoint_dir=checkpoint_dir,
        class_id_to_palm_id=class_id_to_palm_id,
        config_dict=dict(config),
        mixed_precision=mixed_precision
    )

if __name__ == "__main__":
    main()
