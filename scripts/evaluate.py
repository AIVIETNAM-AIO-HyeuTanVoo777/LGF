import os
import sys
import time
import json
import argparse
import numpy as np
import pandas as pd
from typing import Dict, Any, List
from palmrec.utils.config import load_config
from palmrec.utils.seed import set_seed
from palmrec.utils.logging import get_logger
from palmrec.features.feature_cache import load_features
from palmrec.matching.kg import PalmTemplate, PalmKnowledgeGraph, TwoStageRecognizer
from palmrec.evaluation.metrics import calculate_classification_metrics, calculate_eer, get_confusion_matrix_df
from palmrec.evaluation.timing import LatencyTracker

def main():
    parser = argparse.ArgumentParser(description="Evaluate Palmprint Matching Pipeline")
    parser.add_argument("--config", type=str, required=True, help="Path to config file")
    parser.add_argument("--mode", type=str, choices=["one_stage", "two_stage"], default="two_stage", 
                        help="Evaluation mode (one_stage global search or two_stage graph search)")
    args = parser.parse_args()

    config = load_config(args.config)
    set_seed(config.project.seed)

    # Directories
    feature_dir = os.path.join(config.project.output_dir, "features", config.dataset.name)
    eval_dir = os.path.join(config.project.output_dir, "evaluation", config.dataset.name)
    report_dir = os.path.join(config.project.output_dir, "reports", config.dataset.name)
    os.makedirs(eval_dir, exist_ok=True)
    os.makedirs(report_dir, exist_ok=True)
    
    # Logger
    log_file = os.path.join(config.project.output_dir, "logs", f"evaluate_{config.dataset.name}.log")
    logger = get_logger("Evaluate", log_file=log_file)
    logger.info(f"Evaluating Palmprint Recognition for dataset: {config.dataset.name} in {args.mode} mode")

    # Load Graph
    graph_path = config.graph.get("save_path", os.path.join(config.project.output_dir, "graphs", f"{config.dataset.name}_graph.pkl"))
    if not os.path.exists(graph_path):
        logger.error(f"Knowledge Graph file not found: {graph_path}. Run build_knowledge_graph.py first.")
        sys.exit(1)
    logger.info(f"Loading Knowledge Graph from {graph_path}...")
    kg = PalmKnowledgeGraph.load(graph_path)

    # Load Fused Test Features (Probes)
    fused_test_path = os.path.join(feature_dir, "fused_test.npz")
    if not os.path.exists(fused_test_path):
        logger.error(f"Fused test features not found at {fused_test_path}. Run fit_kcca.py first.")
        sys.exit(1)
    logger.info("Loading fused test features...")
    fused_test = load_features(fused_test_path)

    # Reconfigure KG matching parameters using --mode or config
    matcher_config = dict(config.get("matcher", {}))
    if args.mode == "one_stage":
        matcher_config["one_stage"] = True
    else:
        matcher_config["one_stage"] = False

    recognizer = TwoStageRecognizer(kg, {"matcher": matcher_config})

    # Perform evaluation
    logger.info(f"Matching {len(fused_test.sample_ids)} probe samples...")
    y_true = []
    y_pred = []
    
    genuine_scores = []
    impostor_scores = []
    candidate_counts = []
    
    tracker = LatencyTracker()
    tracker.start("matching_loop")
    
    for i in range(len(fused_test.sample_ids)):
        probe_palm = str(fused_test.palm_ids[i])
        probe_feat = fused_test.features[i]
        probe_meta = {
            "gender": str(fused_test.gender[i]),
            "hand_side": str(fused_test.hand_side[i])
        }
        
        # Predict class
        res = recognizer.predict_feature(
            feature=probe_feat,
            gender=probe_meta["gender"],
            hand_side=probe_meta["hand_side"]
        )
        
        y_true.append(probe_palm)
        y_pred.append(res.predicted_palm_id)
        candidate_counts.append(res.candidate_count)
        
        # Genuine vs Impostor scores for EER calculation
        # Retrieve candidate templates matching metadata filter
        candidates = kg.query_candidates(probe_meta["gender"], probe_meta["hand_side"])
        if not candidates:
            candidates = kg.all_templates()
            
        q_norm = np.linalg.norm(probe_feat)
        q_normed = probe_feat / (q_norm + 1e-12) if q_norm > 0 else probe_feat
        
        for cand in candidates:
            c_norm = np.linalg.norm(cand.feature)
            c_normed = cand.feature / (c_norm + 1e-12) if c_norm > 0 else cand.feature
            sim_score = float(np.dot(q_normed, c_normed))
            
            if cand.palm_id == probe_palm:
                genuine_scores.append(sim_score)
            else:
                impostor_scores.append(sim_score)
                
    tracker.stop("matching_loop")
    latencies = tracker.get_latencies()
    total_matching_time = latencies.get("matching_loop", 0.0)
    mean_matching_latency = total_matching_time / len(fused_test.sample_ids) if len(fused_test.sample_ids) > 0 else 0.0

    # Compute classification metrics
    logger.info("Computing metrics...")
    clf_metrics = calculate_classification_metrics(y_true, y_pred)
    
    # Calculate EER
    eer, eer_thresh = calculate_eer(genuine_scores, impostor_scores)
    clf_metrics["eer"] = eer
    clf_metrics["eer_threshold"] = eer_thresh
    
    # Confusion matrix
    cm, labels = get_confusion_matrix_df(y_true, y_pred)
    cm_df = pd.DataFrame(cm, index=labels, columns=labels)
    cm_csv_path = os.path.join(eval_dir, f"{args.mode}_confusion_matrix.csv")
    cm_df.to_csv(cm_csv_path)
    logger.info(f"Saved confusion matrix to {cm_csv_path}")

    # Prepare standard JSON report
    metrics_summary = {
        "dataset": config.dataset.name,
        "experiment": config.get("experiment", {}).get("name", f"{config.dataset.name.lower()}_{args.mode}"),
        "seed": config.project.seed,
        "num_train": len(kg.all_templates()),
        "num_test": len(fused_test.sample_ids),
        "num_classes": len(labels),
        "metrics": {
            "accuracy": clf_metrics["accuracy"],
            "macro_precision": clf_metrics["precision"],
            "macro_recall": clf_metrics["recall"],
            "macro_f1": clf_metrics["f1_score"],
            "weighted_precision": clf_metrics.get("weighted_precision", clf_metrics["precision"]),
            "weighted_recall": clf_metrics.get("weighted_recall", clf_metrics["recall"]),
            "weighted_f1": clf_metrics.get("weighted_f1", clf_metrics["f1_score"]),
            "eer": clf_metrics["eer"]
        },
        "timing_ms": {
            "gabor_mean": 0.0, # Filled by experiments or timing reports
            "conformer_mean": 0.0,
            "kcca_mean": 0.0,
            "graph_query_mean": 0.0,
            "matching_mean": mean_matching_latency * 1000,
            "total_mean": mean_matching_latency * 1000
        },
        "config_path": args.config,
        "config_hash": "",
        "hardware": {},
        "notes": [f"Evaluation Mode: {args.mode}", f"Average candidates: {np.mean(candidate_counts):.2f}"]
    }

    # Save metrics JSON
    metrics_json_path = os.path.join(report_dir, f"{config.dataset.name.lower()}_{args.mode}_metrics.json")
    with open(metrics_json_path, "w", encoding="utf-8") as f:
        json.dump(metrics_summary, f, indent=4)
    logger.info(f"Saved metrics summary JSON to {metrics_json_path}")

    # Save metrics MD
    metrics_md_path = os.path.join(report_dir, f"{config.dataset.name.lower()}_{args.mode}_metrics.md")
    with open(metrics_md_path, "w", encoding="utf-8") as f:
        f.write(f"# Palmprint Recognition Report — {config.dataset.name}\n\n")
        f.write(f"- **Experiment**: {metrics_summary['experiment']}\n")
        f.write(f"- **Mode**: {args.mode}\n")
        f.write(f"- **Accuracy**: {metrics_summary['metrics']['accuracy']*100:.2f}%\n")
        f.write(f"- **Macro F1**: {metrics_summary['metrics']['macro_f1']*100:.2f}%\n")
        f.write(f"- **EER**: {metrics_summary['metrics']['eer']*100:.2f}%\n")
        f.write(f"- **Average Candidate Subset Size**: {np.mean(candidate_counts):.1f} / {metrics_summary['num_train']}\n")
        f.write(f"- **Mean Matching Latency**: {metrics_summary['timing_ms']['matching_mean']:.2f} ms\n")
    logger.info(f"Saved markdown report to {metrics_md_path}")

    # Output stats
    logger.info("\n" + "="*50 + "\n" + f"      PALMPRINT RECOGNITION RESULTS ({args.mode.upper()})\n" + "="*50)
    logger.info(f"Dataset:            {metrics_summary['dataset']}")
    logger.info(f"Test Probes:        {metrics_summary['num_test']}")
    logger.info(f"Accuracy (Rank-1):  {metrics_summary['metrics']['accuracy']*100:.2f}%")
    logger.info(f"Precision (Macro):  {metrics_summary['metrics']['macro_precision']*100:.2f}%")
    logger.info(f"Recall (Macro):     {metrics_summary['metrics']['macro_recall']*100:.2f}%")
    logger.info(f"F1-Score (Macro):   {metrics_summary['metrics']['macro_f1']*100:.2f}%")
    logger.info(f"Equal Error Rate:   {metrics_summary['metrics']['eer']*100:.2f}% (Thresh: {eer_thresh:.4f})")
    logger.info(f"Mean Latency/Probe: {metrics_summary['timing_ms']['matching_mean']:.2f} ms")
    logger.info(f"Candidate subset:   {np.mean(candidate_counts):.1f} / {metrics_summary['num_train']} templates")
    logger.info("="*50)

if __name__ == "__main__":
    main()
