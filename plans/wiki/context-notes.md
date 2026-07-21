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

## 2026-07-21 — flow rewrite + em-dash purge

- Owner reviewed the published wiki: content felt "두서 없음" (no
  narrative flow / missing context), NOT a TOC problem. Clarified that
  bullets and tables themselves are fine; the fix is connective prose +
  context around them, not removing them.
- All 8 English pages rewritten for flow: each opens with a context
  paragraph, sections are bridged with a lead-in line, tables/bullets
  kept. Home approved as the voice sample before applying to the rest.
- Owner directive: remove ALL em-dashes (—, U+2014) from the whole wiki
  AND the methodology docs. En-dashes (–, U+2013) in ranges/compounds
  (227–299 K, Radau–Darwin) are NOT touched.
- Scope of "methodology 문서" = the 17 methodology docs indexed by the
  Methodology-Library page + methodology-index (en+ko = 36 files). Other
  reference docs (external-observer, lism, rex, principia-cfg, etc.) NOT
  in scope unless owner extends. Counts at start: wiki 141, methodology
  en 1308 + ko 1124 = 2432.
- Owner decisions (AskUserQuestion): table empty-cell "—" → en-dash "–";
  execution → Sonnet agent pass (fanout approved, ~0.6-0.9M tokens).
- Em-dash replacement rules given to agents: prose → contextual
  punctuation (comma/colon/period/parens); table cell "—" → "–";
  heading "—" → colon + MUST update the in-page TOC anchor in lockstep
  (dead-link gate). Korean headings avoid sentence-ending colons.
- Wiki ko mirrors re-translated fresh by Sonnet (per owner pref) from
  the new English, em-dash-free, block-parity preserved.
- Publish plan: after ko lands + check.sh green, copy staging → wiki-repo
  and push; methodology docs commit to main separately.
