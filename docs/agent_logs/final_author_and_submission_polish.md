# Final Author and Submission Polish — Report

## Summary

Final submission polish applied to `paper/main.tex` and the paper section
files. No result values, metrics, or scientific claims were changed.

---

## Files Changed

| File | Change |
|---|---|
| `paper/main.tex` | Author block replaced with real authors and affiliation |
| `paper/sections/07_discussion.tex` | Wording fix — "test identities" → "held-out evaluation palm classes" |
| `paper/sections/02_related_work.tex` | Table 1 layout: `\scriptsize`, narrower columns, header renamed to "Protocol note" |
| `docs/agent_logs/final_author_policy.md` | Policy document (this run: non-anonymous mode) |
| `docs/agent_logs/final_author_and_submission_polish.md` | This report |
| `paper_overleaf_upload.zip` | Rebuilt |

---

## Detail of Each Change

### 1. Author Block (`paper/main.tex`)

- **Before**: `PALM\_CGK\_BASE Project Team`
- **After**: Four named authors with institution (FPT University, Vietnam) and
  emails via `\thanks{}`. ASCII-safe names used for LaTeX compatibility.
- Submission mode: **non-anonymous**. See `docs/agent_logs/final_author_policy.md`.

### 2. Wording Fix (`paper/sections/07_discussion.tex`, line 3)

- **Before**: `when development and test identities are made palm-class-disjoint`
- **After**: `when development and held-out evaluation palm classes are disjoint`
- Rationale: removes the word "identities" which implies person-level identity
  verification not asserted by the audit. The new wording correctly describes
  the palm-class split design.

### 3. Table 1 Layout (`paper/sections/02_related_work.tex`)

- Font size: `\small` → `\scriptsize`
- Column widths adjusted to fit `\textwidth` more cleanly
- Header: `Directly comparable?` → `Protocol note`
- Cell values in the last column: `No` → `Not directly comparable` (clearer)
- Shortened one citation label to avoid overflow: `Smartphone verification` →
  `Smartphone verif.`
- No scientific meaning changed.

### 4. Repository Path Formatting (`paper/sections/04_experiments.tex`, line 109)

- Already correctly formatted as
  `\texttt{docs/results/rankb\_run\_manifest.csv}` — no change needed.

### 5. Search for `"in this project"` / `"project team"`

- `"in this project"` — not found in paper sections (was already replaced
  in a prior polish pass with `"in this study"`).
- `"PALM CGK BASE Project Team"` — found only in `main.tex` (now replaced).
- `"project team"` — not found in any section files.

---

## Verification Checklist (for Overleaf)

- [ ] PDF generated successfully
- [ ] Author block shows four named authors with FPT University affiliation
- [ ] No `??` undefined references
- [ ] No missing citations
- [ ] No table overflow (Tables 11 and 12 fixed in prior commit)
- [ ] No B1/B5/B6 labels in figure legends (fixed in prior commit)
- [ ] Table 1 "Protocol note" column visible without overflow
