---
type: workspace
title: "Phase 3 web report pipeline — context notes"
slug: html-pipeline-context-notes
cluster: phase3-procedure
cluster_role: member
status: active
related: [[html-pipeline-checklist]]
created: 2026-05-21
updated: 2026-05-25
tier: public
---
# Phase 3 web report pipeline — context notes

Append-only log of decisions during this work.

## 2026-05-21 — Goal and scope

User wants `docs/` to act as a coherent website where the DB
(`db/systems/`, `db/stellar_props_curated.json`, etc.) is the source
of truth and the per-system Phase 2 + per-planet Phase 3 web pages
regenerate automatically when the curation work is done.

Current state (just before this work):
- `docs/index.html` — DB viewer, fetches DB JSON at runtime, has ko/en
  toggle and rich UX (sky surveys, filters).
- `docs/phase2-trappist-1.html` — paper-by-paper measurement viewer
  for TRAPPIST-1, fetches DB JSON at runtime. Host name is hardcoded.
- `docs/phase3-trappist-1-d.html` — static synthesis report in
  Korean, one-off. Content embedded; not regenerable.

Diagnosis: the gap is the Phase 3 page (no generator) and the Phase 2
page's hardcoded host. Style is also copy-pasted across three pages.

## 2026-05-21 — Architecture choice

Adopted: bilingual markdown source + JS-driven i18n in the generated
HTML. Alternative options considered:

- (a-1) Sidecar files (`<planet>.md` + `<planet>.ko.md`) — rejected
  because curating two files doubles the synthesis workload and
  invites drift.
- (a-3) LLM translation step in the build — rejected because every
  build incurs API cost and produces non-deterministic phrasing.
- (a-2, adopted) Bilingual `<planet>.md` with explicit `[en]`/`[ko]`
  blocks, heading `|` split, table `(한국어)` column suffix, inline
  list `{{ko: ...}}` marker. One file, deterministic build.

The HTML output uses the same `T = {ko: {...}, en: {...}}` pattern
already proven in `index.html` so the toggle behavior is consistent
across the whole site.

## 2026-05-21 — Bilingual markdown grammar (locked)

Heading: `## English | 한국어` — both required for headings shown
in the page. If only English is given, fall back to English in both
locales (graceful degradation).

Paragraph blocks:

```
[en]
First English paragraph,
possibly across multiple lines.

Continuing English paragraph in the same [en] block.

[ko]
첫 번째 한국어 단락,
줄바꿈 가능.

같은 [ko] 블록 안의 다음 단락.
```

The `[en]` / `[ko]` marker introduces a block that lasts until the
next `[en]` / `[ko]` marker or until a non-prose construct (heading,
table, list, fenced code).

Tables: number of columns is the same in both languages. Any column
intended for translation is paired with a sibling column whose header
is `<English Name> (한국어)`. The English column is shown when
`lang='en'`, the Korean column when `lang='ko'`. Columns without a
sibling (e.g. `Field`, `Value`) are language-neutral.

Lists: inline marker `{{ko: 한국어 문구}}` follows the English text
in the same bullet. If absent, English is shown in both locales.

Code blocks (fenced) and link URLs: language-neutral, shown as-is.

## 2026-05-21 — Filesystem layout

Decided:

```
docs/
  style.css                    [common, new in Stage 1]
  index.html                   [unchanged behavior, gains Phase 2/3 buttons]
  reports.html                 [new in Stage 5]
  phase2/
    <host_slug>.html           [autogen, replaces docs/phase2-<host>.html]
  phase3/
    <planet_slug>.md           [bilingual source]
    <planet_slug>.html         [autogen]
    _bib/                      [unchanged]
    _papers/                   [unchanged, gitignored]
```

The old `docs/phase2-trappist-1.html` and `docs/phase3-trappist-1-d.html`
flat-file URLs will redirect or be removed; bookmarks (memory MEMORY.md,
index.html howto) need to be updated to the new paths.

Slug convention: TRAPPIST-1 → `trappist-1`, TRAPPIST-1 d → `trappist-1-d`
(lowercase, hyphenated, space-collapsed). Already matches the existing
bibliography slug convention used by `scripts/phase3/build_bibliography.py`.

## 2026-05-21 — CSS extraction strategy

Three pages currently duplicate dark-theme tokens (`#080c14` body,
`#0c121e` card, `#5a88b8` accent, etc.) and basic typography
(`Segoe UI` stack, `13px` font size, `1.5–1.65` line-height).

Plan: `docs/style.css` owns the shared subset. Page-specific styles
remain inline (the JS-driven detail panel in `index.html`, the SVG
plot styling in `phase2-<host>.html`, etc.) so we don't fight
specificity across files.

## 2026-05-21 — Policy collision: bilingual markdown superseded by `ko/` mirror tree

While Stage 1 (CSS extraction) was being committed, two upstream
commits landed (17b758a, 0396545) that codify a different policy:
English markdown source lives at its canonical path, Korean mirror
lives at `ko/<same-path>`. Documented in AGENTS.md §2.1 and §3.7,
with `scripts/check-mirrors.sh` to detect missing or stale mirrors.

This supersedes the bilingual-in-one-file syntax I had planned (the
`[en]/[ko]` block grammar and `(한국어)` column suffix). Reasons the
mirror approach wins:

- Reuses an already-agreed project convention rather than inventing
  new markdown grammar.
- Each language file reads naturally on its own (no `[en]`/`[ko]`
  noise interleaved with prose).
- `check-mirrors.sh` provides validation for free.
- Translation can be done as a separate concern (e.g. by a different
  agent or a translator) without touching the source.
- PR template already has a mirror checkbox so reviewers catch drift.

Adapted plan:

- Stage 2 (revised) — Create `ko/docs/phase3/trappist-1-d.md` as the
  natural-Korean mirror of the existing English synthesis. No new
  syntax retrofit needed in the English source.
- Stage 3 (revised) — Generator reads the English `<path>.md` and
  the corresponding `ko/<path>.md`, splits both by H2 headings (which
  must match between locales), and builds the JS `T = {en, ko}`
  table from paired sections.
- Stage 4+ — Phase 2 generator and reports index follow the same
  English + ko/-mirror pattern.

Headings paired by order: the generator assumes the English and
Korean files have the same H2/H3 structure. If they diverge,
check-mirrors.sh catches the staleness but the generator should also
fail loudly rather than silently dropping content.


## Related

- [checklist](checklist.md) — sibling workspace doc in `html-pipeline/`
- [phase3 procedure (skill)](../../.agents/skills/nearstars-phase3/SKILL.md) — parent topic this workspace contributes to
