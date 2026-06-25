from __future__ import annotations

import subprocess
import sys


def main() -> int:
    return subprocess.run([sys.executable, "scripts/make_strict_tongji_score_figures.py"]).returncode


if __name__ == "__main__":
    raise SystemExit(main())
