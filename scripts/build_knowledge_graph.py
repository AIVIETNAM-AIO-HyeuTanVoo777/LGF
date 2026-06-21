import os
import sys
import argparse
import numpy as np
from palmrec.utils.config import load_config
from palmrec.utils.seed import set_seed
from palmrec.utils.logging import get_logger
from palmrec.features.feature_cache import load_features
from palmrec.matching.kg import PalmTemplate, PalmKnowledgeGraph

def main():
    parser = argparse.ArgumentParser(description="Build Knowledge Graph")
    parser.add_argument("--config", type=str, required=True, help="Path to config file")
    args = parser.parse_args()

    config = load_config(args.config)
    set_seed(config.project.seed)

    feature_dir = os.path.join(config.project.output_dir, "features", config.dataset.name)
    fused_train_path = os.path.join(feature_dir, "fused_train.npz")
    
    log_file = os.path.join(config.project.output_dir, "logs", f"build_graph_{config.dataset.name}.log")
    logger = get_logger("BuildGraph", log_file=log_file)
    logger.info(f"Building Knowledge Graph for dataset: {config.dataset.name}")

    if not os.path.exists(fused_train_path):
        logger.error(f"Fused training features not found at {fused_train_path}. Run fit_kcca.py first.")
        sys.exit(1)

    # Load training features
    logger.info("Loading fused training features...")
    fused_train = load_features(fused_train_path)

    # Initialize graph
    kg = PalmKnowledgeGraph(config.graph)

    # Add templates to graph
    logger.info("Populating Knowledge Graph templates...")
    for i in range(len(fused_train.sample_ids)):
        template = PalmTemplate(
            sample_id=str(fused_train.sample_ids[i]),
            palm_id=str(fused_train.palm_ids[i]),
            subject_id=str(fused_train.subject_ids[i]),
            gender=str(fused_train.gender[i]),
            hand_side=str(fused_train.hand_side[i]),
            feature=fused_train.features[i],
            image_path=str(fused_train.image_paths[i])
        )
        kg.add_template(template)

    # Save graph
    graph_save_path = config.graph.get("save_path", os.path.join(config.project.output_dir, "graphs", f"{config.dataset.name}_graph.pkl"))
    logger.info(f"Saving Knowledge Graph to {graph_save_path}...")
    kg.save(graph_save_path)

    # Summary
    all_t = kg.all_templates()
    logger.info(f"Knowledge Graph successfully built.")
    logger.info(f"  Total templates: {len(all_t)}")
    
    # Calculate partition details
    genders = list(kg.graph.keys())
    for g in genders:
        for h in kg.graph[g].keys():
            count = sum(len(templates) for templates in kg.graph[g][h].values())
            if count > 0:
                logger.info(f"  Partition ({g}, {h}): {count} templates")

if __name__ == "__main__":
    main()
