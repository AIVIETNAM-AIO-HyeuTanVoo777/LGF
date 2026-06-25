from __future__ import annotations

import subprocess
import sys


def main() -> int:
    commands = [
        [sys.executable, "scripts/audit_splits.py"],
        [sys.executable, "scripts/audit_rankb_protocol.py"],
    ]
    for cmd in commands:
        print("Running:", " ".join(cmd))
        result = subprocess.run(cmd)
        if result.returncode != 0:
            return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
