# GitHub Wiki program — plan

**Goal.** Stand up the `nearstars-db` GitHub Wiki as the public-facing
documentation layer, merging two audiences the owner picked (2026-07-20):
repo readers (what this data engine is) and future players (what the mod
will contain, how it will install).

**Why a wiki, not more `docs/`.** `docs/` is the rendered database viewer
and reference tree — deep, internal, en/ko mirrored via the pipeline.
The wiki is the shallow, welcoming front door: five pages, no build step,
editable without touching the data engine.

## Page roster (v1)

| Page | Audience | Content |
|---|---|---|
| `Home` | both | what NearStars is, status, differentiators, navigation |
| `Star-Systems` | players | v1 confirmed roster (7 systems), per-system highlights **+ our N-body stability results & orbit-viewer links** (owner 2026-07-20) |
| `Data-and-Methodology` | repo readers | 4-phase pipeline, evidence policy, fiction gating |
| `Installation-and-Compatibility` | players | pre-release notice, planned mod stack, profiles |
| `FAQ` | both | release, data honesty, license, REX lineage, Principia, RP-1 |
| `Methodology-Library` | both | portal to the 17 grounded methodology docs (summary + canonical link — no full-copy, drift avoidance) |
| `Showcase` | both | external-observer benchmark, LISM heliospheres, REX data comparison (cultural-context excluded — owner) |
| `Viewers-Gallery` | both | hub for star map, DB viewer, orbit viewers, reports, phase4 boards |

Plus `_Sidebar` (bilingual nav) and `_Footer` (license line).
Dropped by owner decision (2026-07-20): For-Modders portal, cultural-context.

## Language policy

English page + `-ko` suffixed Korean counterpart (natural Korean per
repo convention, not literal). Language toggle link at the top of every
page. English is canonical; edit English first, re-sync `-ko`.

## Source of truth + sync

The **wiki git repo** (`nearstars-db.wiki.git`) is the canonical store
once initialized — wiki pages are NOT duplicated in this repo (drift
risk). This `plans/wiki/` trio records decisions and the page roster
only. Update flow: clone wiki repo → edit → push.

## Bootstrap constraint

GitHub exposes no API to create a wiki; the `.wiki.git` repo only comes
into existence after the first page is created in the web UI. Owner
does that once (any placeholder content), then we clone, replace with
the staged drafts, and push.

## Facts baseline (verified 2026-07-20 against db/)

- Research DB: 145 systems / 157 stellar components, ~50 ly (+ flagged
  beyond-range specials).
- v1 roster (db/roster.yaml): Alpha Centauri (A+B+Proxima), Barnard's
  Star, tau Ceti, 40 Eridani (A+B+C), Fomalhaut, TRAPPIST-1,
  Luhman 16 (A+B) — 12 components, 22 planets (incl. gated synthetic
  fiction bodies, e.g. 40 Eri A c/d).
