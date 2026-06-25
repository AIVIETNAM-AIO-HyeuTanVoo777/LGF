from __future__ import annotations

import subprocess
import sys


def main() -> int:
    for script in ["scripts/audit_training_config_table.py", "scripts/audit_rankb_protocol.py"]:
        cmd = [sys.executable, script]
        print("Running:", " ".join(cmd))
        result = subprocess.run(cmd)
        if result.returncode != 0:
            return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
