import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import pandas as pd
from tqdm import tqdm
import logging
from typing import Dict, Any, Tuple
from .checkpoint import save_checkpoint

logger = logging.getLogger(__name__)

def train_one_epoch(
    model: nn.Module,
    loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    criterion: nn.Module,
    device: torch.device,
    mixed_precision: bool = False
) -> Tuple[float, float]:
    """Train the model for one epoch.
    Returns: (mean_loss, accuracy)
    """
    model.train()
    total_loss = 0.0
    correct = 0
    total = 0
    
    scaler = torch.cuda.amp.GradScaler(enabled=mixed_precision)

    for batch in loader:
        images = batch["image"].to(device)
        labels = batch["label"].to(device)
        
        optimizer.zero_grad()
        
        # AMP forward
        with torch.cuda.amp.autocast(enabled=mixed_precision):
            logits = model(images)
            loss = criterion(logits, labels)
            
        # Backward and step
        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()
        
        # Track metrics
        total_loss += loss.item() * images.size(0)
        _, preds = torch.max(logits, 1)
        correct += (preds == labels).sum().item()
        total += images.size(0)
        
    mean_loss = total_loss / total
    accuracy = correct / total
    return mean_loss, accuracy

@torch.no_grad()
def validate_one_epoch(
    model: nn.Module,
    loader: DataLoader,
    criterion: nn.Module,
    device: torch.device
) -> Tuple[float, float]:
    """Evaluate the model on a validation split.
    Returns: (mean_loss, accuracy)
    """
    model.eval()
    total_loss = 0.0
    correct = 0
    total = 0
    
    for batch in loader:
        images = batch["image"].to(device)
        labels = batch["label"].to(device)
        
        logits = model(images)
        loss = criterion(logits, labels)
        
        total_loss += loss.item() * images.size(0)
        _, preds = torch.max(logits, 1)
        correct += (preds == labels).sum().item()
        total += images.size(0)
        
    mean_loss = total_loss / total
    accuracy = correct / total
    return mean_loss, accuracy

def run_training(
    model: nn.Module,
    train_loader: DataLoader,
    val_loader: DataLoader,
    optimizer: torch.optim.Optimizer,
    scheduler: Any,
    criterion: nn.Module,
    epochs: int,
    device: torch.device,
    checkpoint_dir: str,
    class_id_to_palm_id: Dict[int, str],
    config_dict: Dict[str, Any],
    mixed_precision: bool = False
) -> Dict[str, Any]:
    """Execute the training loop over specified epochs, saving best and last weights."""
    os.makedirs(checkpoint_dir, exist_ok=True)
    training_log_path = os.path.join(checkpoint_dir, "training_log.csv")
    
    best_val_acc = 0.0
    history = []
    
    # Save best by validation accuracy
    for epoch in range(1, epochs + 1):
        train_loss, train_acc = train_one_epoch(
            model, train_loader, optimizer, criterion, device, mixed_precision
        )
        val_loss, val_acc = validate_one_epoch(
            model, val_loader, criterion, device
        )
        
        current_lr = optimizer.param_groups[0]["lr"]
        scheduler.step()
        
        logger.info(
            f"Epoch {epoch:03d}/{epochs:03d} - "
            f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc*100:.2f}% | "
            f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc*100:.2f}% | "
            f"LR: {current_lr:.2e}"
        )
        
        history.append({
            "epoch": epoch,
            "train_loss": train_loss,
            "train_acc": train_acc,
            "val_loss": val_loss,
            "val_acc": val_acc,
            "lr": current_lr
        })
        
        # Save checkpoints
        state = {
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "scheduler_state_dict": scheduler.state_dict(),
            "epoch": epoch,
            "best_metric": max(best_val_acc, val_acc),
            "config": config_dict,
            "class_id_to_palm_id": class_id_to_palm_id
        }
        
        # Save last
        save_checkpoint(state, checkpoint_dir, "last_conformer.pt")
        
        # Save best
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            save_checkpoint(state, checkpoint_dir, "best_conformer.pt")
            logger.info(f"==> Saved new best model checkpoint (Val Acc: {val_acc*100:.2f}%)")
            
        # Write history to log CSV
        pd.DataFrame(history).to_csv(training_log_path, index=False)

    logger.info(f"Training completed. Best validation accuracy: {best_val_acc*100:.2f}%")
    return {"best_val_accuracy": best_val_acc, "history": history}
