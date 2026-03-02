---
title: "Known issues and solutions"
linkTitle: "Known issues"
weight: 80
---

Chronological log of bugs and issues discovered and resolved during development of SAMT-BU Docs. Each entry documents symptom, root cause, and fix — making it easier to diagnose similar problems in the future.

See the Norwegian version (`_index.nb.md`) for full details. Key entries summarised below.

---

## 2026-03-02: Search not working (jQuery defer conflict)

**Symptom:** Search field accepted input but returned no results.

**Root cause:** jQuery loaded with `defer` in `header.html`, but `search.js`, `lunr.min.js`, and `horsey.js` were loaded synchronously. `search.js` ran before `$` (jQuery) was available → `$.getJSON()` threw an error → `lunrIndex` remained `null` → silent failure.

**Fix:** Added `defer` to all three search scripts in `layouts/partials/search.html`.

**Lesson:** When one script has `defer`, all scripts depending on it must also have `defer`.

---

## Procedure: GitHub Pages stuck deploy

```bash
"/c/Program Files/GitHub CLI/gh.exe" api -X DELETE repos/SAMT-BU/samt-bu-docs/pages
"/c/Program Files/GitHub CLI/gh.exe" api -X POST repos/SAMT-BU/samt-bu-docs/pages \
  --field build_type=workflow \
  --field source[branch]=main \
  --field source[path]="/"
git commit --allow-empty -m "Reset Pages"
git push
```

---

## Windows: `git mv` fails for directories with many files

Use `cp -r` + `git rm` + `git add` instead.
