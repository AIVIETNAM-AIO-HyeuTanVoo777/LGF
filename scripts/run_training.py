from __future__ import annotations

import subprocess
import sys


def main() -> int:
    return subprocess.run([sys.executable, "scripts/train_lgf.py", *sys.argv[1:]]).returncode


if __name__ == "__main__":
    raise SystemExit(main())
