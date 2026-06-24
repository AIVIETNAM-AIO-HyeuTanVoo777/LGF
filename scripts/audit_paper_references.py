from __future__ import annotations

import re
from pathlib import Path


PAPER_DIR = Path("paper")
TEX_FILES = [PAPER_DIR / "main.tex"] + sorted((PAPER_DIR / "sections").glob("*.tex"))
BIB_FILE = PAPER_DIR / "references.bib"

OUT_MD = Path("docs/audits/paper_reference_audit.md")


CITE_RE = re.compile(r"\\cite[t|p]?\{([^}]+)\}")
BIB_RE = re.compile(r"@\w+\s*\{\s*([^,\s]+)", re.IGNORECASE)


def extract_cites(text: str) -> set[str]:
    keys: set[str] = set()
    for match in CITE_RE.finditer(text):
        raw = match.group(1)
        for key in raw.split(","):
            key = key.strip()
            if key:
                keys.add(key)
    return keys


def main() -> None:
    if not BIB_FILE.exists():
        raise FileNotFoundError(BIB_FILE)

    cited_by_file: dict[str, set[str]] = {}
    all_cited: set[str] = set()

    for path in TEX_FILES:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        keys = extract_cites(text)
        cited_by_file[str(path)] = keys
        all_cited |= keys

    bib_text = BIB_FILE.read_text(encoding="utf-8")
    bib_keys = set(BIB_RE.findall(bib_text))

    missing = sorted(all_cited - bib_keys)
    unused = sorted(bib_keys - all_cited)

    md: list[str] = []
    md.append("# Paper Reference Audit")
    md.append("")
    md.append("This audit checks citation-key consistency between the LaTeX paper and `paper/references.bib`.")
    md.append("")
    md.append(f"- TeX files checked: {len([p for p in TEX_FILES if p.exists()])}")
    md.append(f"- Citation keys used: {len(all_cited)}")
    md.append(f"- Bibliography entries: {len(bib_keys)}")
    md.append(f"- Missing bibliography entries: {len(missing)}")
    md.append(f"- Unused bibliography entries: {len(unused)}")
    md.append("")
    md.append("## Cited keys")
    md.append("")
    for key in sorted(all_cited):
        md.append(f"- `{key}`")
    md.append("")
    md.append("## Bibliography keys")
    md.append("")
    for key in sorted(bib_keys):
        md.append(f"- `{key}`")
    md.append("")
    md.append("## Missing keys")
    md.append("")
    if missing:
        for key in missing:
            md.append(f"- `{key}`")
    else:
        md.append("- None.")
    md.append("")
    md.append("## Unused bibliography entries")
    md.append("")
    if unused:
        for key in unused:
            md.append(f"- `{key}`")
    else:
        md.append("- None.")
    md.append("")
    md.append("## Citation usage by file")
    md.append("")
    for path, keys in cited_by_file.items():
        if keys:
            md.append(f"### `{path}`")
            for key in sorted(keys):
                md.append(f"- `{key}`")
            md.append("")

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(md), encoding="utf-8")

    print(f"TEX_FILES={len([p for p in TEX_FILES if p.exists()])}")
    print(f"CITED_KEYS={len(all_cited)}")
    print(f"BIB_KEYS={len(bib_keys)}")
    print(f"MISSING_KEYS={len(missing)}")
    print(f"UNUSED_KEYS={len(unused)}")
    print(f"WROTE={OUT_MD}")

    if missing:
        raise SystemExit(1)


if __name__ == "__main__":
    main()