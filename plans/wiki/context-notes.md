# GitHub Wiki program — context notes (append-only)

## 2026-07-20 — program opened

- Owner picked "1+2" (repo wiki + player-facing content merged into the
  GitHub Wiki tab). Internal-docs reinforcement (option 3) not chosen.
- Wiki tab is enabled (`has_wiki: true`) but the `.wiki.git` repo 404s —
  GitHub only materializes it after the first page is saved in the web
  UI, and there is no REST API for wiki pages. Bootstrap therefore needs
  one manual owner step; drafts staged in the session scratchpad
  meanwhile (`wiki-staging/`), NOT committed to this repo (the wiki repo
  is its own git store; duplicating here would drift).
- Language: `-ko` suffix pages instead of a separate ko wiki — GitHub
  wikis have no i18n mechanism; suffix pages + top-of-page toggle links
  is the common pattern and matches the repo's en-canonical rule.
- Content honesty decisions:
  - Pre-release status stated on Home and Installation (no download yet;
    emit/cfg generation is deliberately deferred to project end).
  - Synthetic fiction bodies (40 Eri A c/d etc.) explicitly labeled as
    gated fiction in Star-Systems — the mod's credibility rests on the
    real/fiction boundary staying visible.
  - 40 Eridani A b listed with its dispute note (activity-artifact
    debate), consistent with the gameplay-variety policy (kept, flagged).
  - Installation lists the two planned physics profiles (Principia
    n-body vs stock+warp endgame) as *planned*, per the 2026-06 interstellar
    expansion decision — no promises of unbuilt features as existing.
- Trio lives in `plans/wiki/` (no pipeline/schema impact → plans/ home
  per AGENTS.md §2 decision rule); ko mirrors created same-change per
  §2.1.

## 2026-07-20 — owner review round (structure shown before writing)

- Owner reviewed the sitemap mid-draft ("하기전에 구성 먼저") — future
  sessions: show the page roster BEFORE staging drafts.
- Additions requested: publish the methodology docs; surface other
  wiki-worthy content. Survey produced 4 candidate groups; owner kept
  Methodology-Library + Showcase + Viewers-Gallery, **dropped the
  For-Modders portal and cultural-context**.
- Publication mode decided: portal + link to canonical
  `docs/reference/` files (GitHub renders in-repo md), NOT full-copy —
  wiki sits outside the mirror/dead-link gates, full copies would
  drift. `-ko` wiki pages link the `ko/docs/reference/` mirrors.
- Owner: Star-Systems must include our orbit-simulation results.
  Facts pulled from `phase3/stability-sim/results/*_summary.json`
  (MEGNO ≈ 2 regular across the roster; 40 Eri fiction bodies
  validated alongside the real candidate; TRAPPIST-1 chain via TRACE)
  and the live viewers at `docs/phase4/orbit-viewers/` (6 systems).
  Barnard summary covers planet b only — wiki phrasing kept to what
  the run actually shows.
- Convention docs (CLAUDE.md, CONVENTIONS.md, AGENTS.md, live skills)
  confirmed all public/tracked; Data-and-Methodology links them as a
  reproducibility point.
- `docs/wiki/` in the repo = HTML render gallery of internal docs
  (current, tracked) — unrelated to the GitHub Wiki; no conflict.
