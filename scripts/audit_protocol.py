from __future__ import annotations

import argparse
import subprocess
import sys


BASE_AUDITS = [
    "scripts/audit_splits.py",
    "scripts/audit_gallery_probe_construction.py",
    "scripts/audit_rankb_protocol.py",
    "scripts/audit_checkpoint_selection.py",
    "scripts/audit_training_config_table.py",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic protocol audits for the artifact.")
    parser.add_argument(
        "--include-thresholds",
        action="store_true",
        help="Also recompute threshold evidence. Requires local experiment score CSV files.",
    )
    args = parser.parse_args()

    audits = list(BASE_AUDITS)
    if args.include_thresholds:
        audits.append("scripts/audit_metric_thresholds.py")

    for script in audits:
        cmd = [sys.executable, script]
        print("Running:", " ".join(cmd))
        result = subprocess.run(cmd)
        if result.returncode != 0:
            return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
