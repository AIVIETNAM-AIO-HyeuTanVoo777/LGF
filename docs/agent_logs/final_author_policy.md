# Author Policy — Submission Mode

**Mode**: Non-anonymous submission (open author names).

## Rationale

The repository was set up for an original, non-anonymous submission. No
conference anonymity requirements are in effect for this build. The author
block was therefore updated with real author names, affiliation, and contact
emails.

## Author Block Used

```latex
\author{%
  Nguyen Duc Bao Lam\thanks{lam01662052827@gmail.com} \and
  Nguyen Cong Thinh\thanks{nguyencongthinh17122006@gmail.com} \and
  Tran Trung Tin\thanks{trungtin1218@gmail.com} \and
  Vo Hieu Thang\thanks{thangvo27052006@gmail.com}\\[4pt]
  FPT University, Vietnam
}
```

Names are written in ASCII without Vietnamese diacritics for maximum
compatibility with the standard LaTeX article class. Emails appear as
footnote marks via `\thanks{}`.

## Double-Blind Alternative

If the submission target requires double-blind review, replace the author
block in `paper/main.tex` with:

```latex
\author{Anonymous Authors}
```

and remove the `\thanks{…}` calls and affiliation line. Do not include any
identifying information in the PDF or supplementary material.
