import argparse
import sys
from palmrec.utils.config import load_config
from palmrec.utils.seed import set_seed
from palmrec.utils.logging import get_logger

def main():
    parser = argparse.ArgumentParser(description="Run Full Pipeline")
    parser.add_argument("--config", type=str, required=True, help="Path to config file")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run (import and config load checks)")
    args = parser.parse_args()

    # Load configuration
    try:
        config = load_config(args.config)
    except Exception as e:
        print(f"Error loading config: {e}")
        sys.exit(1)

    # Set seed
    set_seed(config.project.seed, getattr(config.project, 'deterministic', True))

    # Initialize logger
    logger = get_logger("FullPipeline", log_file=None)
    logger.info(f"Loaded config from {args.config}")
    logger.info(f"Seed set to {config.project.seed}")

    if args.dry_run:
        logger.info("Dry run successful (all imports and config loading passed).")
        return

    import subprocess
    import os

    logger.info("Running full pipeline...")

    # Define steps in order conforming to specs
    steps = [
        ("Data Preparation", ["scripts/prepare_data.py"]),
        ("Conformer Training", ["scripts/train_conformer.py"]),
        ("Gabor Feature Extraction", ["scripts/extract_gabor_features.py"]),
        ("Conformer Feature Extraction", ["scripts/extract_conformer_features.py"]),
        ("KCCA Feature Fusion", ["scripts/fit_kcca.py"]),
        ("Build Knowledge Graph", ["scripts/build_knowledge_graph.py"]),
        ("Matching & Evaluation", ["scripts/evaluate.py"])
    ]

    for name, cmd_args in steps:
        logger.info(f"\n" + "="*40 + f"\n  STEP: {name}\n" + "="*40)
        cmd = [sys.executable] + cmd_args + ["--config", args.config]
        
        # Ensure PYTHONPATH includes current directory
        env = os.environ.copy()
        env["PYTHONPATH"] = os.path.abspath(".")
        
        try:
            subprocess.run(cmd, env=env, check=True)
            logger.info(f"Step '{name}' completed successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Step '{name}' failed with exit code {e.returncode}. Aborting pipeline.")
            sys.exit(e.returncode)

    logger.info("\n" + "#"*45 + "\n# FULL PIPELINE COMPLETED SUCCESSFULLY! #\n" + "#"*45)

if __name__ == "__main__":
    main()
