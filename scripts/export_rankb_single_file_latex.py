from __future__ import annotations

import re
import shutil
import zipfile
from pathlib import Path


ROOT = Path(".")
PAPER_DIR = ROOT / "paper"
OUT_DIR = ROOT / "paper_export_rankb_single_file"
OUT_ZIP = ROOT / "rankb_single_file_latex_package.zip"

SRC_MAIN = PAPER_DIR / "main.tex"
SRC_BIB = PAPER_DIR / "references.bib"

OUT_MAIN = OUT_DIR / "main.tex"
OUT_BIB = OUT_DIR / "references.bib"
REQUIRED_FIGURES = [
    ROOT / "paper" / "figures" / "roc_tongji_b1_b5_b6_s1_to_s2.pdf",
    ROOT / "paper" / "figures" / "roc_tongji_b1_b5_b6_s2_to_s1.pdf",
    ROOT / "paper" / "figures" / "det_tongji_b1_b5_b6_s1_to_s2.pdf",
    ROOT / "paper" / "figures" / "det_tongji_b1_b5_b6_s2_to_s1.pdf",
    ROOT / "paper" / "figures" / "score_hist_tongji_b1_b5_b6_s1_to_s2.pdf",
    ROOT / "paper" / "figures" / "score_hist_tongji_b1_b5_b6_s2_to_s1.pdf",
]



INPUT_RE = re.compile(r"^[ \t]*\\input\{([^}]+)\}[ \t]*$", re.MULTILINE)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def resolve_input_path(input_target: str, current_file: Path) -> Path:
    target = input_target.strip()

    candidates = []

    raw = Path(target)
    if raw.suffix:
        candidates.append(PAPER_DIR / raw)
        candidates.append(current_file.parent / raw)
        candidates.append(ROOT / raw)
    else:
        candidates.append(PAPER_DIR / (target + ".tex"))
        candidates.append(current_file.parent / (target + ".tex"))
        candidates.append(ROOT / (target + ".tex"))

    for c in candidates:
        if c.exists():
            return c

    raise FileNotFoundError(
        f"Cannot resolve \\input{{{input_target}}} from {current_file}. "
        f"Tried: {', '.join(str(c) for c in candidates)}"
    )


def inline_inputs(text: str, current_file: Path, seen: set[Path]) -> str:
    def repl(match: re.Match[str]) -> str:
        target = match.group(1)
        path = resolve_input_path(target, current_file).resolve()

        if path in seen:
            raise RuntimeError(f"Recursive input detected: {path}")

        rel = path.relative_to(ROOT.resolve()) if path.is_relative_to(ROOT.resolve()) else path
        body = read_text(path)
        body = inline_inputs(body, path, seen | {path})

        return (
            "\n\n"
            f"% ===== BEGIN INLINED FILE: {rel} =====\n"
            f"{body.rstrip()}\n"
            f"% ===== END INLINED FILE: {rel} =====\n"
        )

    return INPUT_RE.sub(repl, text)


def fail_if_contains(path: Path, patterns: list[str]) -> None:
    text = read_text(path)
    bad = []
    for pat in patterns:
        if re.search(pat, text, flags=re.IGNORECASE):
            bad.append(pat)
    if bad:
        print(f"WARNING: {path} contains patterns:")
        for pat in bad:
            print(f"  - {pat}")


def main() -> None:
    if not SRC_MAIN.exists():
        raise FileNotFoundError(SRC_MAIN)
    if not SRC_BIB.exists():
        raise FileNotFoundError(SRC_BIB)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    main_text = read_text(SRC_MAIN)
    merged = inline_inputs(main_text, SRC_MAIN.resolve(), {SRC_MAIN.resolve()})

    # Keep bibliography external as references.bib.
    # This package contains main.tex, references.bib, and any external figures referenced by main.tex.
    OUT_MAIN.write_text(merged.rstrip() + "\n", encoding="utf-8")
    shutil.copyfile(SRC_BIB, OUT_BIB)

    if OUT_ZIP.exists():
        OUT_ZIP.unlink()

    # Copy external figures referenced by the exported main.tex.
    export_fig_dir = OUT_DIR / "figures"
    export_fig_dir.mkdir(parents=True, exist_ok=True)
    for fig in REQUIRED_FIGURES:
        if not fig.exists():
            raise FileNotFoundError(f"Missing required export figure: {fig}")
        dst = export_fig_dir / fig.name
        shutil.copy2(fig, dst)
        print(f"Wrote {dst}")

    with zipfile.ZipFile(OUT_ZIP, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.write(OUT_MAIN, arcname="main.tex")
        z.write(OUT_BIB, arcname="references.bib")
        for fig in REQUIRED_FIGURES:
            z.write(OUT_DIR / "figures" / fig.name, arcname=f"figures/{fig.name}")

    print(f"Wrote {OUT_MAIN}")
    print(f"Wrote {OUT_BIB}")
    print(f"Wrote {OUT_ZIP}")

    fail_if_contains(
        OUT_MAIN,
        [
            r"REPLACE BEFORE SUBMISSION",
            r"required before submission",
            r"before this manuscript is submitted",
            r"must be completed",
            r"current draft",
            r"palm-class-disjoint",
            r"person-disjoint",
            r"\\input\{",
        ],
    )


if __name__ == "__main__":
    main()
