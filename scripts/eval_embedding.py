import os
import json
import yaml
import argparse
import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader
from sklearn.metrics import f1_score, roc_curve
from palmrec.evaluation.metrics import tar_at_far_conservative
from scipy.optimize import brentq
from scipy.interpolate import interp1d

from palmrec.datasets.palm_dataset import PalmDataset
from palmrec.models.baselines import ResNet18Baseline

def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate Palmprint Embeddings.")
    parser.add_argument("--checkpoint", type=str, required=True, help="Path to best.pt checkpoint.")
    parser.add_argument("--config", type=str, required=True, help="Path to config YAML file.")
    parser.add_argument("--split_file", type=str, default="", help="Override split file path.")
    parser.add_argument("--output_dir", type=str, default="", help="Override output directory.")
    return parser.parse_args()

def extract_embeddings(model, dataloader, device, embedding_mode="post_bn"):
    model.eval()
    embeddings_list = []
    labels_list = []
    paths_list = []
    
    with torch.no_grad():
        for batch in dataloader:
            images = batch["image"].to(device)
            labels = batch["label"] # use label (original class_id as remap_classes=False)
            paths = batch["path"]
            
            if hasattr(model, "extract_embedding"):
                embeddings = model.extract_embedding(images, embedding_mode=embedding_mode)
            else:
                _, embeddings = model(images)
            
            embeddings_list.append(embeddings.cpu())
            labels_list.append(labels)
            paths_list.extend(paths)
            
    all_embeddings = torch.cat(embeddings_list, dim=0)
    all_labels = torch.cat(labels_list, dim=0)
    return all_embeddings, all_labels, paths_list

def main():
    args = parse_args()
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # Load config
    with open(args.config, "r") as f:
        config = yaml.safe_load(f)
        
    split_file = args.split_file if args.split_file else config["dataset"]["split_file"]
    output_dir = args.output_dir if args.output_dir else config.get("save_dir", "experiments/default")
    os.makedirs(output_dir, exist_ok=True)
    
    # Load checkpoint
    print(f"Loading checkpoint from {args.checkpoint}...")
    checkpoint = torch.load(args.checkpoint, map_location=device)
    
    class_mapping = checkpoint["class_mapping"]
    num_classes = len(class_mapping)
    embedding_dim = config["model"].get("embedding_dim", 256)
    
    # Build model and load weights
    model_cfg = config.get("model", {})
    model_name = model_cfg.get("name", "ResNet18Baseline")
    embedding_dim = model_cfg.get("embedding_dim", embedding_dim)
    pretrained = model_cfg.get("pretrained", True)

    from palmrec.models import build_model

    model = build_model(
        name=model_name,
        num_classes=num_classes,
        embedding_dim=embedding_dim,
        pretrained=pretrained,
    )

    model.load_state_dict(checkpoint["model_state_dict"])
    model = model.to(device)
    eval_cfg = config.get("eval", {})
    embedding_mode = eval_cfg.get(
        "embedding",
        model_cfg.get("eval_embedding", model_cfg.get("embedding_mode", "post_bn")),
    )
    
    # Measure Resource Efficiency
    print("Measuring model resource efficiency...")
    num_params = sum(p.numel() for p in model.parameters())
    num_trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    
    # Inference time per image (batch size 1)
    model.eval()
    dummy_input = torch.randn(1, 3, 224, 224, device=device)
    # Warmup
    for _ in range(10):
        with torch.no_grad():
            _ = model(dummy_input)
    # Measure
    import time
    start_time = time.time()
    num_runs = 100
    with torch.no_grad():
        for _ in range(num_runs):
            _ = model(dummy_input)
    avg_inference_time_ms = ((time.time() - start_time) / num_runs) * 1000
    
    # FLOPs
    flops = None
    flops_method = None
    try:
        from fvcore.nn import FlopCountAnalysis
        import logging
        logging.getLogger("fvcore").setLevel(logging.ERROR)
        flops_analyzer = FlopCountAnalysis(model, dummy_input)
        flops = flops_analyzer.total()
        flops_method = "fvcore"
    except ImportError:
        try:
            from thop import profile
            flops, _ = profile(model, inputs=(dummy_input,), verbose=False)
            flops_method = "thop"
        except ImportError:
            pass
    
    # Load Gallery & Probe
    print("Loading Gallery and Probe datasets...")
    # remap_classes=False to preserve original class_ids for direct comparison
    gallery_dataset = PalmDataset(split_file, "gallery", remap_classes=False)
    probe_dataset = PalmDataset(split_file, "probe", remap_classes=False)
    
    print(f"Gallery size: {len(gallery_dataset)}, Probe size: {len(probe_dataset)}")
    
    if len(gallery_dataset) == 0 or len(probe_dataset) == 0:
        print("Error: Gallery or Probe split is empty.")
        return
        
    num_workers = config.get("loader", {}).get("num_workers", 0)
    gallery_loader = DataLoader(gallery_dataset, batch_size=64, shuffle=False, num_workers=num_workers)
    probe_loader = DataLoader(probe_dataset, batch_size=64, shuffle=False, num_workers=num_workers)
    
    # Extract features
    print("Extracting gallery embeddings...")
    gallery_embeds, gallery_labels, gallery_paths = extract_embeddings(
        model, gallery_loader, device, embedding_mode=embedding_mode
    )
    
    print("Extracting probe embeddings...")
    probe_embeds, probe_labels, probe_paths = extract_embeddings(
        model, probe_loader, device, embedding_mode=embedding_mode
    )
    
    # Compute similarity matrix
    print("Computing cosine similarity matrix...")
    sim_matrix = torch.matmul(probe_embeds, gallery_embeds.T) # [N_p, N_g]
    
    # Create mask for self-matches (same image path)
    gallery_path_to_idx = {path: idx for idx, path in enumerate(gallery_paths)}
    self_mask = torch.zeros_like(sim_matrix, dtype=torch.bool)
    for i, p_path in enumerate(probe_paths):
        if p_path in gallery_path_to_idx:
            self_mask[i, gallery_path_to_idx[p_path]] = True
            
    # Masked similarity for identification (Rank metrics)
    sim_matrix_masked = sim_matrix.clone()
    sim_matrix_masked[self_mask] = -999999.0
    
    # Sort matches
    sorted_indices = torch.argsort(sim_matrix_masked, dim=1, descending=True)
    
    # --- 1. Vectorized Rank and CMC Computation ---
    N_p = len(probe_labels)
    N_g = len(gallery_labels)
    
    # Sort matches
    # gallery_labels: [N_g] -> index with sorted_indices of shape [N_p, N_g]
    # to get sorted labels of matches: [N_p, N_g]
    sorted_labels = gallery_labels[sorted_indices]
    
    # Compare with probe labels
    # probe_labels: [N_p] -> unsqueeze to [N_p, 1] to broadcast
    match_matrix = (sorted_labels == probe_labels.unsqueeze(1))
    
    # Cumulative sum along rank dimension to find if a match occurred at or before rank k
    cum_matches = match_matrix.cumsum(dim=1)
    correct_at_rank = (cum_matches > 0).float().mean(dim=0)
    
    rank1_acc = correct_at_rank[0].item()
    rank5_acc = correct_at_rank[4].item()
    
    # --- 2. Cumulative Match Characteristic (CMC) ---
    max_cmc_rank = min(N_g, 50)
    cmc_data = [{"rank": k, "accuracy": correct_at_rank[k-1].item()} for k in range(1, max_cmc_rank + 1)]
    cmc_df = pd.DataFrame(cmc_data)
    cmc_df.to_csv(os.path.join(output_dir, "cmc.csv"), index=False)

    
    # --- 3. Macro-F1 ---
    closest_gallery_indices = sorted_indices[:, 0].numpy()
    pred_labels = gallery_labels[closest_gallery_indices].numpy()
    true_labels = probe_labels.numpy()
    macro_f1 = f1_score(true_labels, pred_labels, average="macro", zero_division=0)
    
    # --- 4. EER & TAR @ FAR ---
    # Create label match mask
    label_mask = (probe_labels.unsqueeze(1) == gallery_labels.unsqueeze(0)) # [N_p, N_g]
    
    gen_mask = label_mask & (~self_mask)
    imp_mask = (~label_mask) & (~self_mask)
    
    pos_scores = sim_matrix[gen_mask].numpy()
    neg_scores = sim_matrix[imp_mask].numpy()
    
    if len(pos_scores) == 0 or len(neg_scores) == 0:
        print("Warning: Cannot compute verification metrics. Genuine or Impostor pairs list is empty.")
        eer, tar_1e2, tar_1e3 = 0.0, 0.0, 0.0
        roc_df = pd.DataFrame(columns=["fpr", "tpr"])
    else:
        y_true = np.concatenate([np.ones_like(pos_scores), np.zeros_like(neg_scores)])
        y_scores = np.concatenate([pos_scores, neg_scores])
        
        fpr, tpr, thresholds = roc_curve(y_true, y_scores)
        
        fnr = 1.0 - tpr
        
        # Simple EER
        eer = fpr[np.nanargmin(np.absolute(fpr - fnr))]
        
        # Interpolated EER
        try:
            eer = brentq(lambda x : 1.0 - x - interp1d(fpr, tpr)(x), 0.0, 1.0)
        except Exception:
            pass
            
        # Conservative TAR @ FAR: selected empirical FPR never exceeds the target FAR.
        tar_1e2_info = tar_at_far_conservative(fpr, tpr, thresholds, 1e-2)
        tar_1e3_info = tar_at_far_conservative(fpr, tpr, thresholds, 1e-3)
        tar_1e2 = tar_1e2_info["tar"]
        tar_1e3 = tar_1e3_info["tar"]
        
        # Downsample ROC curve to save space
        if len(fpr) > 10000:
            indices = np.linspace(0, len(fpr) - 1, 10000, dtype=int)
            fpr = fpr[indices]
            tpr = tpr[indices]
            
        roc_df = pd.DataFrame({"fpr": fpr, "tpr": tpr})
        # Score export and diagnostics.
        # Store per-pair scores as CSV rather than npy/npz so the artifacts are inspectable.
        scores_df = pd.DataFrame({
            "score": y_scores.astype(float),
            "label": y_true.astype(int),
        })
        scores_df.to_csv(os.path.join(output_dir, "scores.csv"), index=False)

        genuine_mean = float(np.mean(pos_scores))
        genuine_std = float(np.std(pos_scores, ddof=1)) if len(pos_scores) > 1 else 0.0
        impostor_mean = float(np.mean(neg_scores))
        impostor_std = float(np.std(neg_scores, ddof=1)) if len(neg_scores) > 1 else 0.0
        pooled_std = float(np.sqrt(0.5 * (genuine_std ** 2 + impostor_std ** 2)))
        d_prime = float((genuine_mean - impostor_mean) / pooled_std) if pooled_std > 0 else 0.0

        score_diag = {
            "num_genuine_pairs": int(len(pos_scores)),
            "num_impostor_pairs": int(len(neg_scores)),
            "genuine_mean": genuine_mean,
            "genuine_std": genuine_std,
            "impostor_mean": impostor_mean,
            "impostor_std": impostor_std,
            "impostor_q0.990": float(np.quantile(neg_scores, 0.990)),
            "impostor_q0.999": float(np.quantile(neg_scores, 0.999)),
            "genuine_q0.001": float(np.quantile(pos_scores, 0.001)),
            "genuine_q0.010": float(np.quantile(pos_scores, 0.010)),
            "d_prime": d_prime,
        }

        with open(os.path.join(output_dir, "score_diagnostics.json"), "w", encoding="utf-8") as f:
            json.dump(score_diag, f, indent=4)

        score_diag_md = f"""# Score Distribution Diagnostics

## Pair Counts
- Genuine pairs: {score_diag['num_genuine_pairs']}
- Impostor pairs: {score_diag['num_impostor_pairs']}

## Score Summary
| Group | Mean | Std | Tail quantiles |
|---|---:|---:|---|
| Genuine | {score_diag['genuine_mean']:.6f} | {score_diag['genuine_std']:.6f} | q0.001={score_diag['genuine_q0.001']:.6f}, q0.010={score_diag['genuine_q0.010']:.6f} |
| Impostor | {score_diag['impostor_mean']:.6f} | {score_diag['impostor_std']:.6f} | q0.990={score_diag['impostor_q0.990']:.6f}, q0.999={score_diag['impostor_q0.999']:.6f} |

## Separation
- d-prime: {score_diag['d_prime']:.6f}
"""
        with open(os.path.join(output_dir, "score_diagnostics.md"), "w", encoding="utf-8") as f:
            f.write(score_diag_md)

        roc_df.to_csv(os.path.join(output_dir, "roc.csv"), index=False)
        
    metrics = {
        "Rank-1": float(rank1_acc),
        "Rank-5": float(rank5_acc),
        "Macro-F1": float(macro_f1),
        "EER": float(eer),
        "TAR@FAR=1e-2": float(tar_1e2),
        "TAR@FAR=1e-3": float(tar_1e3)
    }
    
    # Save metrics.json
    with open(os.path.join(output_dir, "metrics.json"), "w") as f:
        json.dump(metrics, f, indent=4)
        
    # Save metrics.md
    flops_str = f"{flops / 1e9:.3f} GFLOPs (via {flops_method})" if flops is not None else "N/A"
    md_content = f"""# Palmprint Recognition Evaluation Report

## Evaluation Summary
- **Model**: {model_name}
- **Embedding Mode**: {embedding_mode}
- **Gallery Size**: {N_g}
- **Probe Size**: {N_p}
- **Split File**: `{os.path.basename(split_file)}`

## Model Resource Efficiency
- **Total Parameters**: {num_params:,} ({num_params / 1e6:.2f} M)
- **Trainable Parameters**: {num_trainable_params:,} ({num_trainable_params / 1e6:.2f} M)
- **Average Inference Time (per image)**: {avg_inference_time_ms:.2f} ms (batch size 1 on {device.type.upper()})
- **Estimated FLOPs**: {flops_str}

## Key Performance Metrics
| Metric | Value | Percentage | Description |
|---|---|---|---|
| **Rank-1** | {metrics['Rank-1']:.6f} | {metrics['Rank-1']*100:.2f}% | Closed-set identification accuracy (top-1 match) |
| **Rank-5** | {metrics['Rank-5']:.6f} | {metrics['Rank-5']*100:.2f}% | Closed-set identification accuracy (within top-5) |
| **Macro-F1** | {metrics['Macro-F1']:.6f} | {metrics['Macro-F1']*100:.2f}% | Macro-averaged F1 score over all classes |
| **EER** | {metrics['EER']:.6f} | {metrics['EER']*100:.2f}% | Equal Error Rate for verification |
| **TAR@FAR=1e-2** | {metrics['TAR@FAR=1e-2']:.6f} | {metrics['TAR@FAR=1e-2']*100:.2f}% | True Acceptance Rate at False Acceptance Rate = 1% |
| **TAR@FAR=1e-3** | {metrics['TAR@FAR=1e-3']:.6f} | {metrics['TAR@FAR=1e-3']*100:.2f}% | True Acceptance Rate at False Acceptance Rate = 0.1% |

---
*Report generated automatically by `eval_embedding.py`.*
"""
    with open(os.path.join(output_dir, "metrics.md"), "w", encoding="utf-8") as f:
        f.write(md_content)
        
    print("\n--- Evaluation Results ---")
    print(f"Model Name: {model_name}")
    print(f"Total Params: {num_params:,} ({num_params / 1e6:.2f} M)")
    print(f"Average Inference Time: {avg_inference_time_ms:.2f} ms")
    if flops is not None:
        print(f"Estimated FLOPs: {flops_str}")
    for k, v in metrics.items():
        print(f"{k}: {v:.6f} ({v*100:.2f}%)")
    print(f"Results saved to {output_dir}")

if __name__ == "__main__":
    main()
