import os
import sys
import yaml
import argparse
import subprocess
import shutil
from pathlib import Path

# Base configs and their corresponding save directories
BASE_CONFIGS = [
    "configs/b1_resnet18_ce_supcon_tongji_s1s2_lr1e4.yaml",
    "configs/b1_resnet18_ce_supcon_tongji_s2s1_lr1e4.yaml",
    "configs/b2_fixed_gabor_resnet18_tongji_s1s2_lr1e4.yaml",
    "configs/b2_fixed_gabor_resnet18_tongji_s2s1_lr1e4.yaml",
]

def parse_args():
    parser = argparse.ArgumentParser(description="Sweep seeds for Tongji cross-session experiments.")
    parser.add_argument("--seeds", type=int, nargs="+", default=[2026, 2705], help="List of seeds to sweep.")
    parser.add_argument("--force", action="store_true", help="Force rerun training and evaluation even if outputs exist.")
    parser.add_argument("--dry_run", action="store_true", help="Print commands without running them.")
    parser.add_argument("--only_generate_configs", action="store_true", help="Only generate configs and exit.")
    parser.add_argument("--skip_train", action="store_true", help="Skip training phase.")
    parser.add_argument("--skip_eval", action="store_true", help="Skip evaluation phase.")
    return parser.parse_args()

def generate_configs(seeds):
    generated = []
    print("Generating config files...")
    for base_path in BASE_CONFIGS:
        if not os.path.exists(base_path):
            print(f"Error: Base config not found at {base_path}")
            sys.exit(1)
            
        with open(base_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            
        base_name = Path(base_path).stem
        for seed in seeds:
            new_config = config.copy()
            new_config["seed"] = seed
            new_config["save_dir"] = f"experiments/{base_name}_seed{seed}"
            
            new_config_path = f"configs/{base_name}_seed{seed}.yaml"
            generated.append((base_path, new_config_path, new_config["save_dir"]))
            
            if not os.path.exists(new_config_path):
                print(f"Creating config: {new_config_path}")
                with open(new_config_path, "w", encoding="utf-8") as f_out:
                    yaml.dump(new_config, f_out, default_flow_style=False)
            else:
                print(f"Config already exists: {new_config_path}")
    return generated

def main():
    args = parse_args()
    seeds = args.seeds
    print(f"Seeds to sweep: {seeds}")
    
    # Step 1: Generate configs
    configs_meta = generate_configs(seeds)
    
    if args.only_generate_configs:
        print("Config generation completed. Exiting as --only_generate_configs is set.")
        return

    # Step 2: Run training and evaluation
    for base_config, config_path, save_dir in configs_meta:
        experiment_name = Path(config_path).stem
        checkpoint_path = os.path.join(save_dir, "checkpoints", "best.pt")
        local_metrics_json = os.path.join(save_dir, "metrics.json")
        local_metrics_md = os.path.join(save_dir, "metrics.md")
        
        # Output paths under docs/results/
        dest_metrics_json = f"docs/results/{experiment_name}_metrics.json"
        dest_metrics_md = f"docs/results/{experiment_name}_metrics.md"
        dest_yaml = f"docs/results/{experiment_name}.yaml"
        
        print("\n" + "=" * 80)
        print(f"Experiment: {experiment_name}")
        print(f"Save dir: {save_dir}")
        print("=" * 80)
        
        # --- Training ---
        train_skipped = False
        if os.path.exists(checkpoint_path) and not args.force:
            print(f"Checkpoint already exists at {checkpoint_path}. Skipping training.")
            train_skipped = True
        elif args.skip_train:
            print("Skipping training as --skip_train is set.")
            train_skipped = True
        else:
            cmd_train = ["python", "scripts/train_lgf.py", "--config", config_path]
            print(f"Running train command: {' '.join(cmd_train)}")
            if not args.dry_run:
                res = subprocess.run(cmd_train)
                if res.returncode != 0:
                    print(f"Error: Training failed for {experiment_name} with exit code {res.returncode}")
                    sys.exit(1)
                    
        # --- Evaluation ---
        eval_skipped = False
        if os.path.exists(local_metrics_json) and not args.force:
            print(f"Metrics already exist at {local_metrics_json}. Skipping evaluation.")
            eval_skipped = True
        elif args.skip_eval:
            print("Skipping evaluation as --skip_eval is set.")
            eval_skipped = True
        else:
            if not args.dry_run and not os.path.exists(checkpoint_path):
                print(f"Error: Missing checkpoint: {checkpoint_path}")
                sys.exit(1)
                
            cmd_eval = [
                "python", "scripts/eval_embedding.py",
                "--checkpoint", checkpoint_path,
                "--config", config_path
            ]
            print(f"Running eval command: {' '.join(cmd_eval)}")
            if not args.dry_run:
                res = subprocess.run(cmd_eval)
                if res.returncode != 0:
                    print(f"Error: Evaluation failed for {experiment_name} with exit code {res.returncode}")
                    sys.exit(1)
                    
                if not os.path.exists(local_metrics_json):
                    print(f"Error: Missing metrics.json after eval: {local_metrics_json}")
                    sys.exit(1)
                    
        # --- Copy Outputs to docs/results/ ---
        if not args.dry_run:
            os.makedirs("docs/results", exist_ok=True)
            
            # Copy metrics.json
            if os.path.exists(local_metrics_json):
                print(f"Copying {local_metrics_json} -> {dest_metrics_json}")
                shutil.copy(local_metrics_json, dest_metrics_json)
            else:
                if not eval_skipped:
                    print(f"Warning: {local_metrics_json} not found to copy.")
            
            # Copy metrics.md
            if os.path.exists(local_metrics_md):
                print(f"Copying {local_metrics_md} -> {dest_metrics_md}")
                shutil.copy(local_metrics_md, dest_metrics_md)
            else:
                if not eval_skipped:
                    print(f"Warning: {local_metrics_md} not found to copy.")
                    
            # Copy config yaml
            print(f"Copying {config_path} -> {dest_yaml}")
            shutil.copy(config_path, dest_yaml)
            
    print("\nSweep processing completed successfully.")

if __name__ == "__main__":
    main()
