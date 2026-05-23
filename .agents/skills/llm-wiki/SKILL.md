---
name: llm-wiki
description: >
  Maintain the NearStars project's LLM Wiki — an interlinked,
  LLM-curated documentation layer over the existing repo docs.
  Adapted from Karpathy's LLM Wiki gist (2026-04-04) for NearStars'
  3-tier structure (raw / wiki / schema). Use this skill when the
  user invokes "/wiki refresh", "/wiki ingest <path>", "/wiki lint",
  "/wiki query <topic>", or any time a new document is added or
  substantially edited and the wiki layer needs to catch up.
  Operates across the public docs tier AND the local-only mod skills
  tier (scatterer-cfg, eve-cfg, volumetrics-cfg) — same procedure,
  different gitignore boundaries.
mod_version: "karpathy-llm-wiki-2026-04-04 + nearstars-adaptation-2026-05-24"
---

# NearStars LLM Wiki — Maintenance Guide

> **Domain.** NearStars is a KSP planet-pack data engine producing
> validated per-component JSON from public astronomical catalogs, plus
> downstream mod cfg writers. The wiki layer is a living, LLM-curated
> overlay that makes the project's ~300 markdown documents
> cross-referenced, navigable, and self-aware.
>
> **Philosophy** (Karpathy): "stop re-deriving, start compiling."
> Every new source the user adds, every refinement they make, gets
> integrated into a compounding markdown wiki rather than recomputed
> per query.

Source of truth:
- **Concept reference**: [Karpathy LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — abstract; instantiated below for NearStars.
- **Concrete template**: [ScrapingArt/Karpathy-LLM-Wiki-Stack](https://github.com/ScrapingArt/Karpathy-LLM-Wiki-Stack) — Obsidian + Claude Code stack; folder/frontmatter/log conventions cherry-picked for this skill.

---

## 1. Three-tier architecture

```
NearStars repo (~/Desktop/claude/)
│
├── RAW TIER (immutable; never write)
│   ├── db/                              # validated catalog data (per-component JSON)
│   ├── docs/phase3/_papers/             # arXiv paper text cache (gitignored, regenerable)
│   ├── docs/phase3/_bib/                # bibliography YAML
│   ├── phase2/<topic>/                  # per-topic Phase 2 curation artifacts
│   └── phase3/<system>/                 # per-system Phase 3 synthesis workspaces (HTML, audits)
│
├── PUBLIC WIKI TIER (read+write; commit to GitHub)
│   ├── docs/reference/*.md              # concept pages
│   ├── docs/phase3/*.md                 # per-body entity pages (top-level, not _papers/)
│   ├── plans/*.md                       # synthesis-like research notes
│   ├── docs/wiki/                       # NEW — LLM-maintained index/log/hot/overview
│   ├── AGENTS.md                        # contributor entry-point (read-mostly; small edits OK)
│   ├── README.md                        # repo entry-point (read-mostly)
│   └── ko/<mirror>                      # Korean mirrors (do not auto-edit here;
│                                        # user regenerates from English source)
│
├── LOCAL-ONLY WIKI TIER (read+write; gitignored)
│   ├── .agents/skills/scatterer-cfg{,-workspace}/
│   ├── .agents/skills/eve-cfg{,-workspace}/         # future
│   ├── .agents/skills/volumetrics-cfg{,-workspace}/ # future
│   └── .agents/skills/raymarched-*/                 # future
│
└── SCHEMA TIER (read+small edits)
    ├── CLAUDE.md                        # behavioral guidelines
    ├── AGENTS.md §wiki-operations       # wiki-specific directives (NEW section)
    └── .agents/skills/llm-wiki/SKILL.md # this file
```

**Tier rules.**
- **Raw tier**: read-only. Never modify. If a fact in raw conflicts with
  a wiki claim, flag the contradiction on the wiki page, don't touch
  the raw file.
- **Public wiki tier**: full read+write. Output is publishable.
  EA-derived field names / behaviors / paid-content schema MUST NOT
  appear in this tier's content (see §10 cross-tier rules).
- **Local-only wiki tier**: full read+write within the same gitignored
  boundary. May include full EA schema cross-references. Output never
  enters git.
- **Schema tier**: rarely edited. Small additions OK; structural
  changes require user confirmation.

**Out of scope (never touch).**
- `dist/` (generated artifacts)
- `~/Desktop/ksp-mod-refs/` (external EA bundle)
- `.venv/`, `__pycache__/`, `.git/`
- `node_modules/`, `.DS_Store`

---

## 2. Wiki page types and frontmatter

Every wiki page (in either tier) MUST have YAML frontmatter declaring
its type. Types are mutually exclusive.

### `concept` — technical reference

`docs/reference/*.md`, mod-cfg skill `SKILL.md` and `references/*.md`.

```yaml
---
type: concept
title: "Methodology"
slug: methodology
aliases: [methodology, db-schema]
cluster: methodology
cluster_role: hub | member
sources: [[db-schema]], [[adding_stars]]
related: [[binary-epoch-pipeline]], [[principia-cfg-reference]]
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: high
tier: public | local-only
---
```

### `entity` — concrete object the project tracks

Per-star / per-planet pages in `docs/phase3/*.md`.

```yaml
---
type: entity
entity_kind: star | planet | brown-dwarf | white-dwarf | system | mod
title: "TRAPPIST-1 e"
slug: trappist-1-e
kopernicus_name: Trappist1e
host_star: Trappist1
cluster: system-trappist-1
cluster_role: member
sources: [[phase3/_papers/...]], [[binary-epoch-pipeline]]
related: [[trappist-1-d]], [[trappist-1-f]], [[methodology]]
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: high | medium | low
tier: public
---
```

### `source` — summary of an immutable source

Used inside `docs/phase3/_papers/*.md` if frontmatter is wanted. (Phase 3
papers are arXiv-text cache, gitignored; frontmatter is optional.)

```yaml
---
type: source
title: "Paper Title"
arxiv: "2305.10414"
doi: "10.1234/..."
authors: [...]
year: 2025
cited_by: [[trappist-1-b]], [[trappist-1-c]]
ingested: YYYY-MM-DD
---
```

### `synthesis` — analytical comparison or research note

`plans/*.md`, `docs/reference/rex-data-comparison.md`, similar.

```yaml
---
type: synthesis
title: "REX vs NearStars Data Comparison"
slug: rex-data-comparison
sources: [[Real-Exoplanets-repo]], multiple [[db/systems/*]]
related: [[methodology]], [[trappist-1-b]], [[barnards-star]]
date: YYYY-MM-DD
status: active | promoted | archived
tier: public
---
```

### `workspace` — active implementation work

`phase2/<topic>/`, `phase3/<system>/`. Workspace pages have their own
checklist/plan/context-notes trio; frontmatter is light.

```yaml
---
type: workspace
title: "TRAPPIST-1 system Phase 3"
slug: trappist-1-system
status: active | promoted | archived
related: [[trappist-1-b]], [[trappist-1-c]], [[trappist-1-d]], [[trappist-1-e]], [[trappist-1-f]], [[trappist-1-g]], [[trappist-1-h]]
tier: public
---
```

### `index`, `log`, `hot` — wiki state pages

These live in `docs/wiki/` and have a fixed schema (see §6).

---

## 3. Clusters

A cluster is a coherent topic with one or more **hub** pages and many
**member** pages. Hubs have `cluster_role: hub` and a body section
`## In this cluster` listing members. Members have `cluster_role: member`
and link back to the hub.

### Public clusters

| Cluster | Hub | Members |
|---|---|---|
| `methodology` | `docs/reference/methodology.md` | adding_stars, binary-epoch-pipeline, data-sources, archive_issues, tools, mod-reference, mod-release-layout, guideline |
| `physics-epoch` | `docs/reference/binary-epoch-pipeline.md` | (overlap with methodology + principia-cfg-reference) |
| `mod-kopernicus` | `.agents/skills/kopernicus-cfg/SKILL.md` | kopernicus references/* |
| `mod-principia` | `docs/reference/principia-cfg-reference.md` | principia-cfg skill |
| `mod-firefly` | `.agents/skills/firefly-cfg/SKILL.md` | firefly references/*, phase3-mapping |
| `phase3-procedure` | `.agents/skills/nearstars-phase3/SKILL.md` | phase3 references/* |
| `system-trappist-1` | `docs/phase3/trappist-1-system` workspace | trappist-1-b through h |
| `system-alpha-cen` | `docs/phase3/alpha-cen-proxima-system` workspace | alpha-centauri-a, -b, proxima-cen, proxima-cen-b, proxima-cen-d |
| `system-<other>` | (per system as Phase 3 advances) | per-body pages |
| `comparisons` | (no single hub) | rex-data-comparison, stellarium-binary-orbit-comparison |
| `attribution` | `docs/reference/data-sources.md` | LICENSE, NOTICE links |

### Local-only clusters

| Cluster | Hub | Tier |
|---|---|---|
| `mod-scatterer` | `.agents/skills/scatterer-cfg/SKILL.md` | local-only |
| `mod-eve` | `.agents/skills/eve-cfg/SKILL.md` (future) | local-only |
| `mod-volumetrics` | `.agents/skills/volumetrics-cfg/SKILL.md` (future) | local-only |

---

## 4. Ingest workflow

Triggered by `/wiki ingest <path>` or by detecting an unindexed file
during `/wiki refresh`.

1. **Read the source file.** Determine its type (concept / entity /
   synthesis / workspace).
2. **Determine its tier** (public / local-only) from its path.
3. **If frontmatter missing**: add minimal frontmatter per §2. Assign
   `cluster:` per §3. Set `confidence:` from a quick read of the body
   (high if cited extensively, medium if mostly assertions, low if
   sketchy or marked TBD).
4. **Discover cross-references.** Read the body. For every concept,
   entity, paper, or skill the file *should* reference, propose a
   `[[wikilink]]` or `[text](path.md)` markdown link.
   - **Public-tier file**: links to public-tier targets only by name;
     links to local-only targets use the path explicitly (will appear
     broken to public viewers, fine locally).
   - **Local-only file**: may link freely to either tier.
5. **Add a `## Related` section** near the end of the file (before
   "See also" if one exists; otherwise as the last section). Each
   entry: a link + a one-line description of the relationship.
   ```markdown
   ## Related
   - [methodology](../reference/methodology.md) — schema rules these decisions inherit
   - [proxima-cen-b](proxima-cen-b.md) — sibling M-dwarf HZ planet
   - [adding_stars](../reference/adding_stars.md) — workflow that produced this row
   ```
6. **Update `docs/wiki/index.md`**: add this page under its cluster
   section. Increment source counts on the hub's `## In this cluster`
   if hub pages exist.
7. **Update related pages**: when ingesting page X, the pages X links
   to should have X in *their* `## Related` (back-link). Add if
   missing.
8. **Contradiction check**: if the new page contradicts a claim on an
   existing page, flag using:
   ```markdown
   > [!contradiction]
   > [[other-page]] claims X; this page asserts Y. Recommendation: ...
   ```
9. **Append to `docs/wiki/log.md`** (see §6).
10. **A single ingest typically touches 3–10 wiki pages.**

---

## 5. Lint workflow

Triggered by `/wiki lint` or by scheduled weekly run.

1. **Frontmatter audit**: scan every `.md` file in the wiki tiers. List
   any missing frontmatter, missing required fields, or invalid
   `cluster:`/`type:` values.
2. **Orphan check**: list pages with 0 inbound links (no other page
   `[[…]]`s them). Exclude entry-point pages (AGENTS.md, README.md,
   wiki/index.md).
3. **Stale-claim check**: pages with `updated:` older than 90 days
   AND `cluster:` actively edited recently. Suggest re-read.
4. **Confidence-low audit**: list pages with `confidence: low`.
   Suggest follow-up sources to investigate.
5. **Cluster health**:
   - Every cluster's hub exists and has `cluster_role: hub`.
   - Every hub has an `## In this cluster` section.
   - Every member is listed in its hub's `## In this cluster`.
   - Every member has `cluster_role: member`.
6. **Cross-tier link audit**:
   - Public pages must NOT inline EA-derived field names. Scan for
     `sunReflectionStrength`, `cloudColorMultiplier`,
     `cloudScatteringMultiplier`, `cloudSkyIrradianceMultiplier`,
     `volumetricsColorMultiplier`, `EVEIntegration_preserveCloudColors`,
     `layerRaymarchedVolumeV5`, `reflectionColor`, `ambientColor`,
     and any other EA-specific identifiers known to be present in
     local-only references. List violations.
   - Public-tier `[name](path)` links pointing into local-only paths
     are OK (broken-on-public is the intended behavior).
7. **Missing-page suggestion**: concepts mentioned 3+ times across
   pages but lacking their own concept page. List with link targets.
8. **Append a lint entry to `docs/wiki/log.md`**.
9. **Update `docs/wiki/hot.md`** with the lint summary.

Lint output is informational by default — it does NOT auto-fix.
User reviews the lint report and asks for follow-up edits.

---

## 6. Wiki state pages

### `docs/wiki/index.md`

Master catalog. Organized by cluster.

```markdown
---
type: index
updated: YYYY-MM-DD
---

# NearStars Wiki Index

Start here → [[overview]] → cluster hub → member pages → syntheses.

---

## Cluster: methodology
> The DB-side schema, fetch pipeline, and curation workflow.
**Hub:** [methodology](../reference/methodology.md) — schema + epoch rules (~10 sources)

| Page | Summary |
|---|---|
| [adding_stars](../reference/adding_stars.md) | Add a new component to the pipeline |
| [binary-epoch-pipeline](../reference/binary-epoch-pipeline.md) | Kepler → ICRS for multi-star systems |
| [data-sources](../reference/data-sources.md) | External catalog attribution |
| ... | ... |

---

## Cluster: mod-scatterer (LOCAL-ONLY)
> Scatterer cfg generation. EA-derived; commit-blocked.
**Hub:** `.agents/skills/scatterer-cfg/SKILL.md` (existence only; full content local)

(member listing only in the local-only wiki overlay)

---

## Syntheses
- [rex-data-comparison](../reference/rex-data-comparison.md) — REX v0.9.6 vs NearStars current
- [stellarium-binary-orbit-comparison](../../plans/stellarium-binary-orbit-comparison.md)

## Recent log entries
*(auto-pulled from log.md head — top 5)*
```

### `docs/wiki/log.md`

Append-only activity record.

```markdown
# Wiki Activity Log

## [YYYY-MM-DD] ingest | <title>
Source: <path>
Pages created: <path>, ...
Pages updated: <path>, ...
Contradictions flagged: <path> (or none)
Tier: public | local-only

## [YYYY-MM-DD] lint | weekly
Frontmatter gaps: N
Orphans: N
Stale-claim candidates: N
Cluster health: OK / issues at <hub>
Cross-tier violations: 0 / N (see report)
Missing-page suggestions: N (see report)

## [YYYY-MM-DD] query | <topic>
Question: <user's question>
Pages read: <paths>
Output filed: <path> (if synthesis created)
```

### `docs/wiki/hot.md`

Session context cache (~500 words). Read silently at session start
before responding when wiki context is relevant.

```markdown
---
type: hot
updated: YYYY-MM-DD
---

### Current focus
*(1–2 sentences: what's actively being worked on)*

### Open questions
- ...

### Recent decisions
- ...

### Last 3 log entries
*(pasted from log.md)*

### Active pages
*(list of pages edited in the last 7 days)*
```

### `docs/wiki/overview.md`

Cluster map + high-level synthesis. Revised after major ingests
(monthly cadence). NOT generated per-ingest.

---

## 7. Query workflow

Triggered by `/wiki query <topic>` or by any open-ended user question
the model judges to benefit from wiki context.

1. **Read `docs/wiki/index.md`** to identify relevant cluster + pages.
2. **Read the candidate pages** directly (Read tool).
3. **Synthesize the answer** with `[[wikilink]]` citations to specific
   source pages.
4. **If the answer is a substantial analysis** (would benefit future
   sessions), offer to file it as a synthesis page in
   `docs/wiki/syntheses/` or `plans/`.
5. **Append a `query` entry to `docs/wiki/log.md`**.

---

## 8. Triggers

This skill is invoked by:

| Trigger | Form | Purpose |
|---|---|---|
| Manual ingest | `/wiki ingest <path>` | User adds/edits a file, runs this to integrate |
| Manual refresh | `/wiki refresh` | Scan repo for unindexed files, ingest each |
| Manual lint | `/wiki lint` | Run §5 health check |
| Manual query | `/wiki query <topic>` | Run §7 |
| Weekly cron | (TBD — Phase 3) | Automatic `/wiki lint` once per week |
| Pre-commit hook | (TBD — Phase 3, opt-in) | Auto-ingest any `.md` staged for commit |

The actual trigger setup (cron entry, slash command registration) is
defined separately under `scripts/wiki/` (TBD when bootstrap completes).
This skill defines the *procedure*; the triggers invoke the procedure.

---

## 9. Cross-tier link rules

The single thing that distinguishes NearStars from a generic wiki: the
tier partition. Rules:

### Public → public

Standard wiki link.
`[methodology](../reference/methodology.md)`
`[[trappist-1-e]]` (Obsidian-style; works in vault, plain text on GitHub)
Both render correctly on GitHub and in Obsidian.

### Public → local-only

Allowed when **referencing existence only**, not enumerating
EA-derived schema. The path link will broken-render on public GitHub
but resolve locally.

Example (in `docs/reference/methodology.md`):
> Atmosphere optics for Scatterer-bearing bodies are handled by the
> local-only [scatterer-cfg](../../.agents/skills/scatterer-cfg/SKILL.md)
> skill.

OK because: mentions the skill exists, doesn't list EA fields.

NOT OK:
> Atmosphere cfg includes `sunReflectionStrength`, `reflectionColor`,
> `ambientColor` (Patreon EA build only).

NOT OK because: leaks the EA-only field names into a public file.

### Local-only → public

Fine, unrestricted. Local-only files can cite any public file.

### Local-only → local-only

Fine, unrestricted.

### Lint enforcement

§5 step 6 scans public files for known EA-only identifiers and flags
violations. The list:
- `sunReflectionStrength`, `reflectionColor`, `ambientColor` (Scatterer EA ocean)
- `cloudColorMultiplier`, `cloudScatteringMultiplier`, `cloudSkyIrradianceMultiplier`, `volumetricsColorMultiplier`, `EVEIntegration_preserveCloudColors` (Scatterer EA cloud bridge)
- `layerRaymarchedVolumeV5` (EVE V5)
- (extend the list as new EA-only identifiers are discovered)

---

## 10. Safety rules

These are absolute. Violating any means the skill's output should be
discarded and the run logged as failed.

1. **Never write to the raw tier.** `db/`, `docs/phase3/_papers/`,
   `phase2/<topic>/`, `phase3/<system>/` are immutable for this skill.
2. **Never delete wiki pages.** Mark as `status: archived` in
   frontmatter and add an `> [!archived]` callout at the top. Move to
   `_archive/` subfolder only on user request.
3. **Always update `wiki/index.md` and `wiki/log.md` on every
   ingest/lint/query operation.**
4. **Never commit local-only content.** Skill output in
   `.agents/skills/{scatterer,eve,volumetrics,raymarched}-*/` paths
   stays gitignored. Git status before any commit should be clean of
   those paths.
5. **Never inline EA-derived field names into public-tier files.**
   See §9 for the enforced identifier list.
6. **Never `git add -A`.** Stage files explicitly. (User memory
   `user_parallel_sessions` requires this.)
7. **English in .md files** for all body content. Frontmatter values
   in English. Korean only in user-facing prose where memory
   convention says so (`feedback_md_language`).
8. **When uncertain about a claim**, set `confidence: low` and flag in
   page body. Do not invent.
9. **Do not modify `ko/` mirrors.** Korean mirrors are regenerated
   from English source by user; auto-edits there cause drift.
10. **Read-back verification**: after any non-trivial write to a wiki
    page, do not re-Read it (harness tracks state). But for the
    multi-file ingest case, verify the final `wiki/index.md` and
    `wiki/log.md` reflect the operation.

---

## 11. Bootstrap state (2026-05-24)

The wiki is being initialized. Current bootstrap status:

| Step | Status |
|---|---|
| Skill defined (this file) | DONE 2026-05-24 |
| `docs/wiki/{index,log,hot,overview}.md` scaffolded | DONE 2026-05-24 |
| Frontmatter added to `docs/reference/*` | TBD |
| Frontmatter added to `docs/phase3/*` (entities) | TBD |
| `## Related` sections added across wiki tier | TBD |
| First full lint pass | TBD |
| Smart Connections data dropped (`.smart-env/` removed) | TBD |
| Trigger setup (cron / slash command) | TBD (Phase 3) |

Until bootstrap completes, partial wiki state is expected. After
bootstrap, ongoing operation is incremental ingest + weekly lint.

---

## 12. References

- [Karpathy LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — concept paper
- [ScrapingArt/Karpathy-LLM-Wiki-Stack](https://github.com/ScrapingArt/Karpathy-LLM-Wiki-Stack) — concrete Obsidian + Claude Code template; this skill cherry-picks its frontmatter/log conventions
- `CLAUDE.md §wiki-operations` (this repo) — schema directive set by user
- `AGENTS.md §2` (this repo) — document hierarchy this skill respects
- `feedback-patreon-assets` memory — local-only policy this skill enforces
