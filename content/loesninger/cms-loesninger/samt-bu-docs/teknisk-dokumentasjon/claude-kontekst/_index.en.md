---
title: "Developer notes and Claude context"
linkTitle: "Developer notes"
weight: 90
---

This page is written for both human developers and for the AI assistant Claude Code, which is actively used in development and maintenance of SAMT-BU Docs. It collects context, conventions, and architectural decisions that would otherwise be lost between working sessions.

> **For Claude:** Read this file explicitly when you need deep context. `MEMORY.md` (auto-loaded) is a compact index — this file is the canonical source of detailed context.

See the Norwegian version (`_index.nb.md`) for full details. This English version covers the key points.

---

## Memory management (Claude Code)

Two levels of persistent context:

| File | Role | Limit |
|------|------|-------|
| `MEMORY.md` (in Claude projects folder) | Auto-loaded at session start — compact index | 200 lines |
| `content/loesninger/.../teknisk-dokumentasjon/` | Canonical source — read explicitly, no line limit, version-controlled | None |

**Convention:** Details belong here (in repo). `MEMORY.md` points here. Nothing important is trimmed — it is moved here instead.

---

## Key architectural decisions

- **3-column layout:** Viewport locked (`overflow: hidden`), three independently scrolling columns via Flexbox
- **CSS layers:** `designsystem.css` → `theme.css` → `custom-head.html` (last wins)
- **Presentation vs. content:** All presentation logic in `hugo-theme-samt-bu` submodule; content repo contains only `hugo.toml`, `content/`, CI scripts
- **Hugo Modules:** Team repos mount their content into `content/teams/<team>/`; no separate pilot repos
- **Search:** Lunr.js + Horsey.js; all search scripts must have `defer` (see [Known issues](../kjente-problemer/))

---

## Conventions

- **Commit messages:** Written in Norwegian
- **Frontmatter format:** YAML (`---`)
- **Page structure:** Each page in its own folder with `_index.nb.md` and `_index.en.md`
- **Presentation changes:** Commit to `hugo-theme-samt-bu`, then update submodule pointer in `samt-bu-docs`
