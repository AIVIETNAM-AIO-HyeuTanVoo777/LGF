import os
import sys
import json
import argparse
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw
from palmrec.utils.config import load_config
from palmrec.utils.seed import set_seed
from palmrec.utils.logging import get_logger
from palmrec.datasets.metadata import build_metadata_dataframe
from palmrec.datasets.splits import create_half_split

def generate_toy_dataset(raw_dir: str, num_subjects: int = 2, num_images_per_palm: int = 4):
    """Generate a synthetic toy dataset with geometric shapes to act as distinct feature footprints.
    2 subjects, 2 hands each, 4 images per palm = 16 images total.
    """
    os.makedirs(raw_dir, exist_ok=True)
    logger = get_logger("ToyGenerator")
    logger.info(f"Generating synthetic TOY dataset with {num_subjects} subjects, 2 hands each, {num_images_per_palm} images/palm.")
    
    rng = np.random.RandomState(42)
    
    hands = ['l', 'r']
    for sub in range(1, num_subjects + 1):
        sub_str = str(sub).zfill(3)
        for hand in hands:
            for img_idx in range(1, num_images_per_palm + 1):
                # Create a 224x224 RGB image
                img = Image.new("RGB", (224, 224), color=(255, 255, 255))
                draw = ImageDraw.Draw(img)
                
                # Draw unique pattern based on subject and hand to simulate different palms
                # Subject 1 left: circles, Subject 1 right: rectangles, etc.
                color = (rng.randint(50, 200), rng.randint(50, 200), rng.randint(50, 200))
                if sub == 1:
                    if hand == 'l':
                        # Circles
                        draw.ellipse([50, 50, 170, 170], fill=color, outline=(0, 0, 0))
                        draw.ellipse([80, 80, 140, 140], fill=(255, 255, 255))
                    else:
                        # Rectangles
                        draw.rectangle([40, 40, 180, 180], fill=color, outline=(0, 0, 0))
                        draw.rectangle([70, 70, 150, 150], fill=(255, 255, 255))
                else:
                    if hand == 'l':
                        # Cross/Lines
                        draw.line([20, 20, 204, 204], fill=color, width=15)
                        draw.line([20, 204, 204, 2], fill=color, width=15)
                    else:
                        # Polygon/Triangle
                        draw.polygon([(112, 30), (30, 190), (190, 190)], fill=color, outline=(0, 0, 0))
                
                # Add some random lines to simulate palm lines
                for _ in range(5):
                    x1 = rng.randint(10, 214)
                    y1 = rng.randint(10, 214)
                    x2 = rng.randint(10, 214)
                    y2 = rng.randint(10, 214)
                    draw.line([x1, y1, x2, y2], fill=(50, 50, 50), width=rng.randint(1, 3))
                
                # Save the image
                filename = f"sub_{sub_str}_{hand}_{img_idx}.jpg"
                filepath = os.path.join(raw_dir, filename)
                img.save(filepath, "JPEG")
                
    logger.info(f"Finished generating {num_subjects * 2 * num_images_per_palm} synthetic images under {raw_dir}.")

def main():
    parser = argparse.ArgumentParser(description="Prepare Palmprint Dataset")
    parser.add_argument("--config", type=str, required=True, help="Path to config file")
    args = parser.parse_args()

    config = load_config(args.config)
    set_seed(config.project.seed)

    # Resolve paths
    raw_dir = config.dataset.raw_dir
    metadata_csv = config.dataset.metadata_csv
    split_json = config.dataset.split_json
    
    # Initialize logger
    os.makedirs(os.path.dirname(metadata_csv), exist_ok=True)
    os.makedirs(os.path.dirname(split_json), exist_ok=True)
    log_file = os.path.join(config.project.output_dir, "logs", f"prepare_{config.dataset.name}.log")
    logger = get_logger("PrepareData", log_file=log_file)
    logger.info(f"Preparing data for dataset: {config.dataset.name}")

    # If it is the TOY dataset and raw_dir doesn't exist or is empty, generate it
    if config.dataset.name.upper() == "TOY":
        if not os.path.exists(raw_dir) or len(os.listdir(raw_dir)) == 0:
            generate_toy_dataset(raw_dir)

    # 1. Build metadata
    logger.info(f"Scanning raw files in {raw_dir}...")
    try:
        metadata_df = build_metadata_dataframe(
            raw_dir=raw_dir,
            dataset_name=config.dataset.name,
            gender_mapping_file=config.dataset.gender_mapping_file
        )
    except Exception as e:
        logger.error(f"Failed to build metadata dataframe: {e}")
        sys.exit(1)

    # 2. Perform Train/Test Split
    logger.info("Splitting dataset into Train and Test...")
    train_df, test_df, dropped_ids = create_half_split(
        metadata_df,
        class_key=config.dataset.class_target,
        seed=config.project.seed
    )

    # 3. Add Split Column to Metadata
    # We assign split label to each row: train, test, or dropped
    metadata_df["split"] = "dropped"
    metadata_df.loc[metadata_df["sample_id"].isin(train_df["sample_id"]), "split"] = "train"
    metadata_df.loc[metadata_df["sample_id"].isin(test_df["sample_id"]), "split"] = "test"

    # Save metadata CSV
    metadata_df.to_csv(metadata_csv, index=False)
    logger.info(f"Saved metadata to {metadata_csv}")

    # Compile split JSON
    split_data = {
        "train": train_df["sample_id"].tolist(),
        "test": test_df["sample_id"].tolist(),
        "dropped": dropped_ids,
        "seed": config.project.seed
    }
    
    with open(split_json, "w", encoding="utf-8") as f:
        json.dump(split_data, f, indent=4)
    logger.info(f"Saved split JSON to {split_json}")

    # Output statistics
    logger.info(f"Dataset Prep Summary:")
    logger.info(f"  Total samples found: {len(metadata_df)}")
    logger.info(f"  Train samples: {len(train_df)}")
    logger.info(f"  Test samples: {len(test_df)}")
    logger.info(f"  Dropped samples: {len(dropped_ids)}")
    logger.info(f"  Unique palms: {metadata_df['palm_id'].nunique()}")

if __name__ == "__main__":
    main()
