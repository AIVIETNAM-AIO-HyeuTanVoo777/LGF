from __future__ import annotations

import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PAPER = ROOT / "paper"
OUT = ROOT / "overleaf_package"
ZIP_PATH = ROOT / "paper_overleaf_upload.zip"

if OUT.exists():
    shutil.rmtree(OUT)
OUT.mkdir(parents=True)

# Copy main paper files to Overleaf root
for name in ["main.tex", "references.bib"]:
    src = PAPER / name
    if not src.exists():
        raise FileNotFoundError(src)
    shutil.copy2(src, OUT / name)

# Copy sections and figures
shutil.copytree(PAPER / "sections", OUT / "sections")
shutil.copytree(PAPER / "figures", OUT / "figures")

# Copy protocol audit table used by main.tex into sections/
audit_src = ROOT / "docs" / "audits" / "rankb_protocol_audit_table.tex"
audit_dst = OUT / "sections" / "rankb_protocol_audit_table.tex"
if not audit_src.exists():
    raise FileNotFoundError(audit_src)
shutil.copy2(audit_src, audit_dst)

# Patch sections/04_experiments.tex path for Overleaf package layout
exp_path = OUT / "sections" / "04_experiments.tex"
exp_text = exp_path.read_text(encoding="utf-8")
exp_text = exp_text.replace(
    r"\input{../docs/audits/rankb_protocol_audit_table}",
    r"\input{sections/rankb_protocol_audit_table}",
)
exp_path.write_text(exp_text, encoding="utf-8")

# Basic sanity checks
required = [
    OUT / "main.tex",
    OUT / "references.bib",
    OUT / "sections" / "01_introduction.tex",
    OUT / "sections" / "02_related_work.tex",
    OUT / "sections" / "03_method.tex",
    OUT / "sections" / "04_experiments.tex",
    OUT / "sections" / "05_results.tex",
    OUT / "sections" / "06_ablation.tex",
    OUT / "sections" / "07_discussion.tex",
    OUT / "sections" / "08_conclusion.tex",
    OUT / "sections" / "strict_tongji_additional_baselines_table.tex",
    OUT / "sections" / "rankb_protocol_audit_table.tex",
]
for path in required:
    if not path.exists():
        raise FileNotFoundError(path)

# Create zip
if ZIP_PATH.exists():
    ZIP_PATH.unlink()

with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as zf:
    for path in sorted(OUT.rglob("*")):
        if path.is_file():
            zf.write(path, path.relative_to(OUT))

print(f"Created folder: {OUT}")
print(f"Created zip: {ZIP_PATH}")
print("Top-level files:")
for p in sorted(OUT.iterdir()):
    print(" -", p.name)
print("Sections containing B8 table:")
print(" -", OUT / "sections" / "strict_tongji_additional_baselines_table.tex")