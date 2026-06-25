from __future__ import annotations

import argparse
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Regenerate main paper tables from audit artifact CSVs.")
    parser.add_argument("--results-dir", default="audit_artifacts/results")
    parser.add_argument("--out-dir", default="paper/sections")
    args = parser.parse_args()
    return subprocess.run([
        sys.executable,
        "scripts/make_result_tables.py",
        "--results-dir",
        args.results_dir,
        "--out-dir",
        args.out_dir,
    ]).returncode


if __name__ == "__main__":
    raise SystemExit(main())
