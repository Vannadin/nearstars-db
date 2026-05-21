<!-- Phase 3 web report pipeline — design decisions and rationale -->
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

## (Append further entries below as work progresses)
