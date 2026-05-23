# AGENTS.md — NearStars contributor guide

Read this before opening a PR. Conventions here are load-bearing; the
pipeline and downstream skills depend on them.

This file is for AI coding agents (Claude Code, etc.) and human
contributors alike. It is the **canonical pointer** into the project's
detailed reference docs; do not duplicate content from
`docs/reference/` here — link to it.

---

## 1. What this repo is

NearStars is the **data engine** of a KSP 1.12.x mod that adds real
nearby star systems. This repo produces validated per-component JSON
in `db/systems/` from public astronomical catalogs (Gaia DR3, SIMBAD,
NASA Exoplanet Archive, ORB6). Downstream cfg writers (Kopernicus,
Principia) live in separate repos and consume `db/systems/*.json`.

License: **CC-BY-NC-SA-4.0** (matches Sol-Configs). See [LICENSE](LICENSE)
and [NOTICE](NOTICE) for third-party attributions.

Primary references — read these before touching the area they cover:

| If you are working on… | Read first |
|---|---|
| Adding/editing stars in the DB | [`docs/reference/adding_stars.md`](docs/reference/adding_stars.md) |
| Understanding the schema and layers | [`docs/reference/methodology.md`](docs/reference/methodology.md) |
| Binary / multiple system orbits | [`docs/reference/binary-epoch-pipeline.md`](docs/reference/binary-epoch-pipeline.md) |
| Project phases, dependencies, scope | [`docs/reference/guideline.md`](docs/reference/guideline.md) |
| Mod-release repo layout (separate repo) | [`docs/reference/mod-release-layout.md`](docs/reference/mod-release-layout.md) |
| Principia cfg format | [`docs/reference/principia-cfg-reference.md`](docs/reference/principia-cfg-reference.md) |

---

## 2. Document hierarchy

The repo has **four** documentation homes — `docs/reference/`,
`phase2/<topic>/`, `phase3/<system>/`, and `plans/<topic>.md`. The
phase2/ and phase3/ trees are both "active implementation work" with
the CLAUDE.md §7 trio structure; they differ in scope (Phase 2 =
paper-cited measurement curation, Phase 3 = cfg-ready synthesis).
Pick the right home before you start writing.

```
docs/reference/        Permanent reference. Schemas, methodology, format specs.
                       Append-mostly, rarely deleted. Source of truth.

phase2/<topic>/        Active implementation work (Phase 2: paper-cited
                       measurement curation). Carries a checklist.
                       Trio: plan.md + checklist.md + context-notes.md.
                       Lives outside docs/ because it has code/data deltas.
                       (Historical: some older work lives in docs/<topic>/.
                       New implementation work goes under phase2/.)

phase3/<system>/       Active Phase 3 synthesis work (cfg-ready value
                       drafting from Phase 2 measurements). Same trio
                       structure as phase2/. Driven by the
                       nearstars-phase3 skill. Per-system rather than
                       per-topic because synthesis is gated on the host
                       star (e.g. phase3/trappist-1-system/).

plans/<topic>.md       Research notes and external-system analyses.
                       Single file. No checklist. No implementation in this repo.
                       Use when you read source code of an upstream mod, study
                       a paper's methodology, or scope an idea that has not
                       been greenlit for implementation.
```

**The decision rule:** *"Will this work touch the DB pipeline, schema, or
generated configs?"*

- **Yes, Phase 2 curation (paper-cited measurements)** → `phase2/<topic>/`
  trio (CLAUDE.md §7).
- **Yes, Phase 3 synthesis (cfg-ready values per planet)** → `phase3/<system>/`
  trio, driven by the `nearstars-phase3` skill.
- **No** → `plans/<topic>.md` single file.

When a `plans/` document graduates into actual work, promote it: move
the relevant sections into a new `phase2/<topic>/plan.md` and leave the
original as historical context (or delete if subsumed). Alternatively
promote to `docs/reference/` if the output is a long-lived reference
document; in that case create both English source and Korean mirror
per §2.1 below.

See [`plans/README.md`](plans/README.md) for the research-note format
and [`plans/_template.md`](plans/_template.md) for the starting scaffold.

### 2.1 Bilingual mirror — `ko/` tree

Every human-readable document has an English source-of-truth and a
Korean mirror under `ko/<same-path>`.

| English (source) | Korean (mirror) |
|---|---|
| `README.md` | `ko/README.md` |
| `docs/reference/<x>.md` | `ko/docs/reference/<x>.md` |
| `docs/<topic>/<x>.md` | `ko/docs/<topic>/<x>.md` |
| `plans/<x>.md` | `ko/plans/<x>.md` (create on first use) |

**Rules.**

- English is canonical. All edits land there first. The Korean version
  is regenerated from the English original — never the reverse
  (avoids drift).
- AI agents: when you create or substantively edit a mirrored doc,
  also create or update the `ko/` counterpart in the same change.
- Human contributors who do not write Korean: create the English
  version only and note in the PR description that the Korean mirror
  is pending. The repo owner regenerates Korean mirrors separately.
- Out of scope (English-only, no mirror): `AGENTS.md`, `CLAUDE.md`,
  PR/issue templates, `db/**/*.md`, `scripts/**/*.md`,
  `phase2/<topic>/{checklist,context-notes}.md`. These are
  behavioural/operational docs for agents and contributors, not
  reference material.
- To find missing or stale mirrors:
  ```bash
  scripts/check-mirrors.sh
  ```

### 2.3 LLM Wiki layer

This repo ships an **LLM-maintained wiki overlay** at `docs/wiki/`,
following Karpathy's LLM Wiki pattern (2026-04-04) adapted for
NearStars' 3-tier structure. The wiki is curated by the
[`llm-wiki`](.agents/skills/llm-wiki/SKILL.md) skill — invoked via
`/wiki refresh`, `/wiki ingest <path>`, `/wiki lint`, or `/wiki query
<topic>`.

**Tiers** (the wiki agent respects gitignore boundaries):
- **Raw** (`db/`, `docs/phase3/_papers/`, `phase2/`, `phase3/`) —
  read-only; never modified by the wiki agent.
- **Public wiki** (`docs/reference/`, `docs/phase3/` entities, `plans/`,
  `docs/wiki/`, `AGENTS.md`, `README.md`) — full read+write; output is
  publishable.
- **Local-only wiki** (`.agents/skills/{scatterer,eve,volumetrics,
  raymarched}-*/`) — full read+write but output stays gitignored
  (Patreon EA content; commits forbidden).

**Cross-tier rule**: public-tier files may *reference* local-only paths
by link (will broken-render on GitHub, resolve locally), but must NOT
inline EA-derived field names or behaviors. The lint workflow scans for
known EA identifiers and flags violations.

See `docs/wiki/{index,overview,log,hot}.md` for the wiki's catalog,
cluster map, activity log, and session cache respectively.

### 2.2 Reading the repo as an Obsidian vault

This repo ships an `.obsidian/` overlay so the four documentation
homes can be navigated as a single graph. Open the repo folder in
[Obsidian](https://obsidian.md) and the graph view shows every `.md`
file as a node with edges from existing markdown links
(`[text](path)`) — no wikilink rewrite was done, so the same files
keep rendering normally in GitHub, `preview-md.sh`, and IDE
previews. Folders excluded from the vault (see
`.obsidian/app.json` → `userIgnoreFilters`): `ko/` (basename
collision with English originals), `.agents/`, `.venv/`,
`docs/phase3/_papers/`, `db/backups/`, `dist/`,
`phase3/html-pipeline/dist/`. Only `app.json`, `graph.json`, and
`appearance.json` are version-controlled; per-user workspace state
is gitignored.

---

## 3. Hard rules for any PR

These are non-negotiable. CI does not catch all of them; reviewers will.

1. **No local absolute paths.** Never commit `/home/<user>/...`,
   `/Users/<user>/...`, or `C:\Users\...`. Use repo-relative paths or
   public URLs. If you reference an external repo, link to its GitHub
   page, not your local clone.

2. **No assumptions in `derived` blocks.** The pipeline's `derived`
   section computes from `raw` with unit conversion and merge-priority
   only. If source data is `null`, derived stays `null`. Do not invent
   defaults. See `scripts/pipeline/build_systems.py` and
   [methodology.md](docs/reference/methodology.md).

3. **Per-paper attribution.** Any value in `stellar_props_curated.json`
   or `planets_curated.json` requires `bibcode` (and `doi` when available).
   Do not seed from NASA `pscomppars` composite values — use the `ps`
   table's `default_flag=1` row instead. See
   [adding_stars.md](docs/reference/adding_stars.md) Step 2.

4. **One file per stellar component.** `db/systems/` is keyed by
   component, not by system. Binary mutual orbits live in
   `db/binary_orbits.json` and are embedded into the representative
   component file at build time; siblings reference it via
   `binary_orbit_ref`.

5. **Run validation before pushing.**
   ```bash
   python3 scripts/pipeline/validate.py
   ```
   Must exit with `FAIL: 0`. Warnings on missing `vmag_v` for non-Gaia
   stars are acceptable; everything else needs to be addressed.

6. **Korean one-line header on new source files.** First line of every
   new `.py`/`.ts`/`.js`/`.sql` file is a one-line Korean comment
   stating its role. Example:
   ```python
   # SIMBAD TAP에서 별의 spectype/Teff를 fetch하는 모듈
   ```
   Skip config files (`*.config.ts`, `package.json`, etc.). See
   CLAUDE.md §6.

7. **`.md` files — English source + `ko/` mirror.** See §2.1. Mirrored
   trees (`docs/`, `plans/`, root `README.md`) require the Korean
   counterpart under `ko/<same-path>`. Non-mirrored trees (`AGENTS.md`,
   `CLAUDE.md`, `db/`, `scripts/`, `phase2/<topic>/{checklist,
   context-notes}.md`, PR/issue templates) are English-only.

---

## 4. Workflows

### 4.1 Adding a star

Use the `nearstars-add-star` skill (Claude Code). The skill drives the
field/schema decisions documented in
[`docs/reference/adding_stars.md`](docs/reference/adding_stars.md). Do
not bypass the skill unless you have read that document end-to-end.

Trigger phrases (Korean): "X 별 추가해줘", "GJ XXX 추가", etc.

### 4.2 Writing Kopernicus or Principia cfgs

These are downstream of this repo. Use:

- `kopernicus-cfg` skill for Kopernicus `.cfg` files
- `principia-cfg` skill for Principia patches

Both read `db/systems/*.json` as input and emit to `dist/`
(`.gitignore`d). Never hand-edit cfgs in `dist/` and commit them.

### 4.3 Curation phases (data depth)

Distinct from the mod development phases in
[guideline.md §9](docs/reference/guideline.md).

- **Curation Phase 1** (default): NASA Exoplanet Archive `ps` table
  `default_flag=1` row, with proper `bibcode` per measurement.
- **Curation Phase 2** (paper-by-paper): Per-measurement curation from
  the literature when a system is being implemented in-game with
  Principia. See `phase2/trappist_1/` for a worked example.
- **Curation Phase 3** (future): Synthesized values for in-game
  representation (PQS terrain color, atmospheric tinting). Not yet
  active. Will live alongside Phase 2 in the schema, distinct file set.

---

## 5. Git and commits

### 5.1 Identity

All commits in this repo must be authored by:

```
VaNnadin <vannadin00@gmail.com>
```

Set this in your local repo config, not globally:

```bash
git config user.name "VaNnadin"
git config user.email "vannadin00@gmail.com"
```

Co-author lines for AI assistants are welcome (`Co-Authored-By: Claude
Sonnet 4.6 <noreply@anthropic.com>`) but the primary author line stays
the same.

### 5.2 Semantic commits

One logical change per commit. The test: *"Can I describe this commit
in one sentence?"* If not, split it.

- Good: `Add Wolf 359 to target list`
- Bad: `Add Wolf 359, fix Sirius radius bug, refactor validate.py`

See CLAUDE.md §9.

### 5.3 PR template

Use `.github/pull_request_template.md`. The checklist is not decoration —
reviewers will reject PRs that skip it.

---

## 6. What not to do

Anti-patterns reviewers have seen repeatedly:

- **Don't add features beyond what was asked.** Three similar lines is
  better than a premature abstraction. (CLAUDE.md §2)
- **Don't "improve" adjacent code in a diff.** Surgical changes only.
  Mention dead code in the PR description; don't delete unrelated lines.
  (CLAUDE.md §3)
- **Don't commit `dist/`, `db/backups/`, `.DS_Store`, or
  `.claude/settings.local.json`.** All gitignored. Check `git status`
  before staging.
- **Don't bypass the skill workflow for star additions.** The skill
  exists because manual additions have repeatedly violated the
  per-paper attribution rule.
- **Don't conflate the two "Phase" axes.** Curation Phase 1/2/3 is
  about data depth. Development Phase 1–4 (`guideline.md §9`) is about
  mod implementation milestones.

---

## 7. Where to ask

Open a GitHub issue with the `question` label, or comment inline on a
PR. For schema-level changes (new fields in `db/systems/*.json`), open
an issue first to align on naming before writing code.
