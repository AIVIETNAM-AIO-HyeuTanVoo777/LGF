import os
import yaml
import argparse
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from collections import Counter

from palmrec.datasets.palm_dataset import PalmDataset
from palmrec.datasets.samplers import RandomIdentitySampler
from palmrec.losses import build_loss

def set_seed(seed):
    import random
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

def parse_args():
    parser = argparse.ArgumentParser(description="Train Baseline model for Palmprint Recognition.")
    parser.add_argument("--config", type=str, required=True, help="Path to config YAML file.")
    return parser.parse_args()

def compute_val_rank1(embeddings, labels):
    """
    Computes Rank-1 identification accuracy using all-to-all similarity.
    For each sample, we find the closest other sample and check if their labels match.
    """
    # Compute similarity matrix
    sim_matrix = torch.matmul(embeddings, embeddings.T) # [N, N]
    
    # Mask out self-similarity (diagonal)
    sim_matrix.fill_diagonal_(-999999.0)
    
    # Get closest match index for each sample
    closest_indices = torch.argmax(sim_matrix, dim=1)
    
    # Compare labels
    correct = (labels[closest_indices] == labels).float()
    return correct.mean().item()

def train():
    args = parse_args()
    
    # Load config
    with open(args.config, "r") as f:
        config = yaml.safe_load(f)
        
    seed = config.get("seed", 42)
    set_seed(seed)
    
    device = torch.device("cuda" if torch.cuda.is_available() and config.get("device", "cuda") == "cuda" else "cpu")
    print(f"Using device: {device}")
    
    # Directories
    save_dir = config.get("save_dir", "experiments/default")
    os.makedirs(save_dir, exist_ok=True)
    os.makedirs(os.path.join(save_dir, "checkpoints"), exist_ok=True)
    
    # Load splits
    dataset_cfg = config["dataset"]
    split_file = dataset_cfg["split_file"]
    
    print(f"Loading datasets from split file: {split_file}...")
    train_dataset = PalmDataset(split_file, "train", remap_classes=True)
    
    # Pass train class mapping to validation set to align class indices
    val_dataset = PalmDataset(
        split_file, 
        "val", 
        remap_classes=True, 
        class_mapping=train_dataset.class_mapping
    )
    
    num_classes = len(train_dataset.class_mapping)
    print(f"Number of classes in training split: {num_classes}")
    print(f"Train samples: {len(train_dataset)}, Val samples: {len(val_dataset)}")
    
    # Sampler and Dataloaders
    sampler_cfg = config.get("sampler", {})
    P = sampler_cfg.get("num_identities", 8)
    K = sampler_cfg.get("num_instances", 2)
    fallback = sampler_cfg.get("fallback_identities", 4)
    
    train_sampler = RandomIdentitySampler(
        train_dataset, 
        num_instances=K, 
        num_identities=P, 
        fallback_identities=fallback
    )
    
    loader_cfg = config.get("loader", {})
    num_workers = loader_cfg.get("num_workers", 0)
    
    train_loader = DataLoader(
        train_dataset, 
        batch_sampler=train_sampler, 
        num_workers=num_workers
    )
    
    # Val loader (uses standard sequential loader)
    val_loader = DataLoader(
        val_dataset, 
        batch_size=P * K, 
        shuffle=False, 
        num_workers=num_workers
    )
    
    # Build Model
    model_cfg = config.get("model", {})
    model_name = model_cfg.get("name", "ResNet18Baseline")
    from palmrec.models import build_model
    model = build_model(
        name=model_name,
        num_classes=num_classes,
        embedding_dim=model_cfg.get("embedding_dim", 256),
        pretrained=model_cfg.get("pretrained", True)
    )
    model = model.to(device)
    
    # Criterion & Optimizer
    train_cfg = config.get("training", {})
    lambda_supcon = train_cfg.get("lambda_supcon", 0.10)
    temperature = train_cfg.get("temperature", 0.07)
    embedding_dim = model_cfg.get("embedding_dim", 256)
    criterion = build_loss(config, num_classes=num_classes, embedding_dim=embedding_dim)
    criterion = criterion.to(device)
    
    lr = train_cfg.get("lr", 0.001)
    weight_decay = train_cfg.get("weight_decay", 0.0001)
    optimizer = torch.optim.AdamW(
        list(model.parameters()) + list(criterion.parameters()),
        lr=lr,
        weight_decay=weight_decay,
    )
    
    # AMP and Gradient Accumulation
    use_amp = train_cfg.get("amp", True)
    scaler = torch.cuda.amp.GradScaler(enabled=use_amp)
    grad_accumulation_steps = train_cfg.get("grad_accumulation_steps", 1)
    
    epochs = train_cfg.get("epochs", 10)
    
    # CSV Logger setup
    log_file = os.path.join(save_dir, "metrics.csv")
    csv_headers = ["epoch", "train_loss", "train_loss_ce", "train_loss_supcon", "val_loss", "val_loss_ce", "val_loss_supcon", "val_rank1"]
    
    # Initialize log dataframe
    if os.path.exists(log_file):
        log_df = pd.read_csv(log_file)
    else:
        log_df = pd.DataFrame(columns=csv_headers)
        
    best_metric = -1.0 # If we save by Rank-1
    best_loss = float("inf") # If we save by val_loss fallback
    save_by_rank1 = False
    
    # Check if we can compute validation Rank-1
    val_labels_list = [val_dataset.samples[i]["class_id"] for i in range(len(val_dataset))]
    val_counts = Counter(val_labels_list)
    can_compute_val_rank1 = any(count >= 2 for count in val_counts.values())
    if can_compute_val_rank1:
        save_by_rank1 = True
        print("Validation set supports Rank-1 computation. Best model will be selected by validation Rank-1.")
    else:
        print("Validation set has too few samples per class. Best model will be selected by validation loss.")

    for epoch in range(1, epochs + 1):
        print(f"\n--- Epoch {epoch}/{epochs} ---")
        
        # --- Training ---
        model.train()
        train_loss_accum = 0.0
        train_ce_accum = 0.0
        train_supcon_accum = 0.0
        
        optimizer.zero_grad()
        
        for batch_idx, batch in enumerate(train_loader):
            images = batch["image"].to(device)
            labels = batch["label"].to(device)
            
            with torch.cuda.amp.autocast(enabled=use_amp):
                logits, embeddings = model(images)
                loss, loss_dict = criterion(logits, embeddings, labels)
                # Scale loss for gradient accumulation
                loss = loss / grad_accumulation_steps
                
            scaler.scale(loss).backward()
            
            if (batch_idx + 1) % grad_accumulation_steps == 0 or (batch_idx + 1) == len(train_loader):
                scaler.step(optimizer)
                scaler.update()
                optimizer.zero_grad()
                
            train_loss_accum += loss.item() * grad_accumulation_steps
            train_ce_accum += loss_dict["loss_ce"]
            train_supcon_accum += loss_dict["loss_supcon"]
            
        num_batches = len(train_loader)
        train_loss_mean = train_loss_accum / num_batches
        train_ce_mean = train_ce_accum / num_batches
        train_supcon_mean = train_supcon_accum / num_batches
        
        print(f"Train Loss: {train_loss_mean:.4f} | CE: {train_ce_mean:.4f} | SupCon: {train_supcon_mean:.4f}")
        
        # --- Validation ---
        model.eval()
        val_loss_accum = 0.0
        val_ce_accum = 0.0
        val_supcon_accum = 0.0
        
        val_embeddings_list = []
        val_labels_list = []
        
        with torch.no_grad():
            for batch in val_loader:
                images = batch["image"].to(device)
                labels = batch["label"].to(device)
                
                # Exclude samples with target label -1 (not present in train set)
                valid_mask = labels != -1
                if not valid_mask.any():
                    continue
                images = images[valid_mask]
                labels = labels[valid_mask]
                
                with torch.cuda.amp.autocast(enabled=use_amp):
                    logits, embeddings = model(images)
                    loss, loss_dict = criterion(logits, embeddings, labels)
                    
                val_loss_accum += loss.item()
                val_ce_accum += loss_dict["loss_ce"]
                val_supcon_accum += loss_dict["loss_supcon"]
                
                val_embeddings_list.append(embeddings)
                val_labels_list.append(labels)
                
        num_val_batches = len(val_loader)
        val_loss_mean = val_loss_accum / num_val_batches
        val_ce_mean = val_ce_accum / num_val_batches
        val_supcon_mean = val_supcon_accum / num_val_batches
        
        # Compute Rank-1 on validation set if possible
        val_rank1 = None
        if len(val_embeddings_list) > 0 and can_compute_val_rank1:
            all_val_embeddings = torch.cat(val_embeddings_list, dim=0)
            all_val_labels = torch.cat(val_labels_list, dim=0)
            val_rank1 = compute_val_rank1(all_val_embeddings, all_val_labels)
            print(f"Val Loss: {val_loss_mean:.4f} | CE: {val_ce_mean:.4f} | SupCon: {val_supcon_mean:.4f} | Rank-1: {val_rank1:.4f}")
        else:
            print(f"Val Loss: {val_loss_mean:.4f} | CE: {val_ce_mean:.4f} | SupCon: {val_supcon_mean:.4f}")
            
        # Log to CSV
        log_row = {
            "epoch": epoch,
            "train_loss": train_loss_mean,
            "train_loss_ce": train_ce_mean,
            "train_loss_supcon": train_supcon_mean,
            "val_loss": val_loss_mean,
            "val_loss_ce": val_ce_mean,
            "val_loss_supcon": val_supcon_mean,
            "val_rank1": val_rank1 if val_rank1 is not None else ""
        }
        log_df = pd.concat([log_df, pd.DataFrame([log_row])], ignore_index=True)
        log_df.to_csv(log_file, index=False)
        
        # Checkpoint Saving Logic
        checkpoint = {
            "epoch": epoch,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "criterion_state_dict": criterion.state_dict(),
            "class_mapping": train_dataset.class_mapping,
            "config": config
        }
        
        # Always save last checkpoint
        torch.save(checkpoint, os.path.join(save_dir, "checkpoints", "last.pt"))
        
        is_best = False
        if save_by_rank1 and val_rank1 is not None:
            if val_rank1 > best_metric:
                best_metric = val_rank1
                is_best = True
        else:
            if val_loss_mean < best_loss:
                best_loss = val_loss_mean
                is_best = True
                
        if is_best:
            print(f"==> Saving new best checkpoint (Epoch {epoch})")
            torch.save(checkpoint, os.path.join(save_dir, "checkpoints", "best.pt"))

if __name__ == "__main__":
    train()
