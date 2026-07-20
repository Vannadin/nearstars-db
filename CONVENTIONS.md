# NearStars — Working Conventions

**What this is.** The working conventions for NearStars — behavioral rules and project-specific curation/data disciplines — collected in one place (they previously lived scattered across memory). `CLAUDE.md` carries the always-on essentials and points here; this file is the full reference. **PORTABLE** conventions (apply to any project) are tagged separately from **NEARSTARS-SPECIFIC** ones — the portable set is the basis a sibling repo can reuse.

---

## 1. Communication & Language — PORTABLE

### 1.1 Korean speech level
**Rule:** Always use formal Korean (존댓말/합쇼체 or 해요체) in all responses to the user.
**Why:** User explicitly requested it.
**Source:** `feedback_speech_level.md`

### 1.2 Markdown source-of-truth language
**Rule:** All public-facing `.md` documents (docs/, plans/, README.md) are written in **English as the source**. A Korean mirror is auto-generated to `ko/<same-path>`.
**Why:** (1) Consistency with codebase language, (2) future collaborators may reference docs, (3) mirrors allow easy ko/en toggling. Canonical reads are English; LLM agents also read English to avoid repeated parsing overhead.
**Details:** 
- Mirrored: `docs/`, `plans/`, root `README.md` → auto-sync `ko/` tree in same commit
- Not mirrored: `CLAUDE.md`, `AGENTS.md`, `db/**`, `scripts/**`, PR/issue templates, underscore-prefix dirs
- Promotion: when a plan graduates to reference, move to `docs/reference/` in both EN + KO and delete the original plan file (archive via git log)
**Source:** `feedback_md_language.md`

### 1.3 Korean mirror prose style
**Rule:** Korean mirrors must read as naturally written Korean, not as word-for-word translations. Restructure sentences freely within each paragraph block (block count must match EN for build_html.py). Use Korean idiom and natural clause order.
**Why:** Literal translation produces stilted prose. Sentence structure differs fundamentally (verb-final, particle-heavy).
**Details:** End sentences with `.` / `?` / `!` never `:`. Keep table structure identical; translate only flowing prose columns.
**Source:** `feedback_ko_mirror_style.md`

### 1.4 Opening documents (preview-md.sh)
**Rule:** When user says "열어줘" (open it), render the Korean mirror (`ko/<same-path>`) as HTML via `scripts/preview-md.sh` and auto-open in browser (macOS `open`).
**Why:** User reads more comfortably in Korean. Mirror policy exists exactly for read scenarios.
**Details:** If no KO mirror exists (AGENTS.md, CLAUDE.md, db/**, etc.), fall back to EN original. Explicit "open in English" request overrides.
**Source:** `feedback_open_doc.md`

### 1.5 Plan review language & structure
**Rule:** When presenting a plan or long document for review, draft it **bilingual**: Korean (for reading) + English (for execution/code reference). Bilingual plan files use EN/KO section pairs so Obsidian and approval UI show Korean first.
**Why:** User can review in native language; actual implementation stays English-grounded.
**Source:** `feedback_plan_review_korean.md`

### 1.6 No orbital-element abbreviations in prose
**Rule:** In explanatory writing, spell out orbital elements: 이심률 (not e), 경사각 (not i), 장반경 (not a), 근일점/원일점 (not q/Q).
**Why:** User found abbreviations confusing in explanations.
**Details:** Code field names, chart axes, and formal notation (equations) keep abbreviations. Rule is "write e/i/a when labeling; spell it out when explaining."
**Source:** `feedback_no_orbital_abbreviations.md`

### 1.7 No rest suggestions
**Rule:** After completing a task unit, report state and propose next steps. Do **not** offer "take a break / rest / manage your energy" suggestions.
**Why:** User is decisive about pacing (sends "ㄱㄱ" to go, ends turn to stop). Unsolicited rest suggestions feel condescending.
**Details:** If there's a genuine blocker (external dependency, missing decision), say "I need X before proceeding" not "you should rest."
**Source:** `feedback_no_rest_suggestions.md`

### 1.8 Git commit language
**Rule:** All git commit messages (subject + body) are written in **English**. Co-Authored-By trailer included.
**Why:** Public GitHub surface; English is language of code/file-names/identifiers in the same line. Consistency with feedback_md_language (English source-of-truth).
**Details:** Use domain terminology in English ("synthesis", "curation", "audit pass" not 합성/큐레이션/감사 in commits). Past commits in Korean are not rewritten. Conversation remains Korean 존댓말.
**Source:** `feedback_commit_language.md`

### 1.9 Git identity (fixed)
**Rule:** All commits use the identity: **user.name = `VaNnadin`**, **user.email = `vannadin00@gmail.com`** (local config, not --global).
**Why:** User explicitly requested unified author identity across repos.
**Source:** `feedback_git_identity.md`

---

## 2. Workflow & Autonomy — PORTABLE

### 2.1 Autonomous execution
**Rule:** Once a direction is agreed, execute to completion without pausing for step-by-step approval. Only stop for genuinely irreversible actions (file deletion, destructive git operations) not covered by the original scope.
**Why:** Repeated "may I proceed?" breaks flow. Clear task direction makes intermediate steps safe.
**Details:** File writes, script runs, data transforms—proceed without confirmation. But judgment applies: read first before modifying, always confirm before deleting.
**Source:** `feedback_autonomy.md`

### 2.2 Subagent delegation for token economy
**Rule:** Delegate heavy reads (cache grep, paper body text, DB JSON generation, Phase 3 drafts, ko mirror prose) to subagents with frozen cache. Main thread does **value-check via spec** (deterministic grep + parity, not re-reading).
**Why:** Concentrating reads into few agents with frozen bibcode/arxiv cache prevents re-download bloat and keeps main context lean.
**Details:** Subagent returns structured output + citations. Main does check.sh + block parity verification. For curated DB: never use json.dump directly—use `apply_phase2.py` or `schema.write_canonical` to preserve indent/key-order invariant.
**Source:** `feedback_agent_token_saving.md`

### 2.3 Audit cost discipline
**Rule:** Batch verify per **report** (one agent re-checks one report's full finding set), never per finding. Most findings are deterministic (grep, recompute); only "paper value differs" needs agent reading. Binding constraint is **daily token quota**, not session context.
**Why:** Fan-out per finding multiplies agents by finding count (232 findings → 232 agents = daily quota burn). Session context stays alive; daily quota is the real scarce resource.
**Details:** Before large fan-outs, estimate cost. When near daily limit, persist durable state and resume next session.
**Source:** `feedback_audit_cost_discipline.md`

### 2.4 Tools lookup (docs/reference/tools.md is canonical)
**Rule:** User asks "is there a tool for X?" → Always read `docs/reference/tools.md` (EN) or `ko/docs/reference/tools.md` (KO) first. That index is canonical. Only expand via grep if not found.
**Why:** ~30 tools scattered across 7 dirs; canonical index prevents redundant search + inconsistency. Index stale = memory useless.
**Details:** New tools require index update + ko mirror sync + check-mirrors.sh validation.
**Source:** `feedback_tools_lookup.md`

### 2.5 Reference document placement
**Rule:** Documents worth reading → `docs/reference/` (EN) + `ko/docs/reference/` (KO mirror). Skills **link** to them, never embed duplicates.
**Why:** check.sh §2 already validates reference doc mirrors. Docs are user-readable; skill folders hold only pure scaffolding (conflict tie-break, scoring rubrics) or EA-protected content.
**Details:** EA-derived documents stay in `.claude/skills/*/references/` (English-only, gitignored). Public knowledge goes to docs/reference first.
**Source:** `feedback_reference_doc_location.md`

---

## 3. Papers, Data Grounding & Discipline — PORTABLE + NEARSTARS-SPECIFIC

### 3.1 Derived value grounding (PORTABLE)
**Rule:** Non-trivial astrophysical derived values (J2, tidal heating, atmospheric escape, effective temperature with greenhouse, interior structure, Love number, rotational evolution) **must cite the method paper**. Back-of-envelope estimates don't count.
**Why:** Project DNA = Phase 2 is paper-cited. Naive approximation masks real model assumptions (e.g., interior structure → J2 range 0.105–0.165; guessing 0.028 hides this).
**Details:**
- Method must be grounded: theory-of-figures paper + calibration source (e.g., gas-giant measured J2 from Iess 2018)
- Textbook closed-form (Roche, Hill, Kepler, solid-angle, unit conversion) is self-justifying
- State assumptions + result range
- Don't cite fabricated papers; use real ADS bibcodes or arxiv_ids
**Source:** `feedback_derived_value_grounding.md`

### 3.2 ADS paper discipline (NEARSTARS)
**Rule:** All paper/citation work uses **registered ADS API key** (`ADS_API_TOKEN` in `~/.zshrc`). No ad-hoc WebSearch. Cache arxiv text via `scripts/phase3/fetch_arxiv_texts.py` and read cache only (no live web re-query). For literature discovery, let agent run ADS `citation_count DESC` query independently (don't hand-list papers).
**Why:** 2026-06-23 incident: subagent used WebSearch + my hard-coded arXiv ids → multiple wrong ids (Pierrehumbert paper was unrelated math, Hu & Yang id was actually Leconte 2013) + missed canonical papers. Switched to ADS-curated authority + frozen cache.
**Details:**
- Flow: pin arxiv_id in `docs/phase3/_bib/<slug>.yaml` → run `fetch_arxiv_texts.py` → read cache (not web) → subagent value-checks citing cache lines → main verifies
- Phantom-paper prevention (2026-06-20 lesson): before flagging a paper as fabricated, **verify non-existence via web/ADS/arXiv**. "Not in our cache" ≠ "doesn't exist." Yadav & Thorngren 2017 ([1709.05676](https://arxiv.org/abs/1709.05676)) and Reiners & Christensen 2010 ([1007.1514](https://arxiv.org/abs/1007.1514)) were both real but out-of-range/uncached.
**Source:** `feedback_ads_paper_discipline.md`

### 3.3 Paper references are links (NEARSTARS)
**Rule:** Every paper reference in a human-readable doc is a **markdown link**, not a bare id:
bibcode → `[2018Icar..305..262I](https://ui.adsabs.harvard.edu/abs/2018Icar..305..262I)`,
arXiv id → `[1007.1514](https://arxiv.org/abs/1007.1514)`. DOI links acceptable where no
bibcode exists. Bare ids stay only in machine fields (YAML `bibcode:`/`arxiv_id:`, JSON,
code) and inside code blocks.
**Why:** Owner directive 2026-07-20 — references should be one click away when reviewing
docs; bare bibcodes force a manual ADS round-trip.
**Details:** applies to `docs/`, `plans/`, `phase2–4/*.md` narrative text + their ko
mirrors. Existing docs are being retrofitted by script (pipeline-flow-program WP6);
new writing complies immediately.
**Source:** owner directive 2026-07-20 (pipeline-flow-program).

### 3.4 Generalize over hardcode (PORTABLE)
**Rule:** New features must work for any case via **data-driven config**, not hardcoded for one instance. First case is first consumer of the general path.
**Why:** One-off hacks scale poorly. Next system needs code+config, not code rewrite.
**Example:** Polyphemus stability-sim visualization reused the general `load_stability()` (already body-name-agnostic), not a custom parser for Polyphemus.
**Source:** `feedback_generalize_over_hardcode.md`

---

## 4. NearStars Star & Planet Curation — NEARSTARS-SPECIFIC

### 4.1 Star addition decision automation
**Rule:** On star-add requests: (1) Gaia DR3 source_id via SIMBAD TAP (`ident` → `oidref`), no asking. (2) `recommended` measurement via stellar_db_methodology method-priority, no asking.
**Why:** User pre-delegated these via clear methodology rules. Autonomy principle [[feedback_autonomy]].
**Details:**
- Method priority: Mass = binary_orbit > asteroseismology > evolutionary_model > spectroscopic > spectroscopic_calibration. Radius = interferometry > eclipsing_binary > evolutionary_model.
- Tie-break: lowest fractional uncertainty wins. Record 1-line reason in meta.notes.
- Fallback: if SIMBAD Gaia lookup fails (saturation), use HIPPARCOS_V path.
**Source:** `feedback_star_addition.md`

### 4.2 Planet curation depth (two-tier)
**Rule:** **Phase 1 (default, all stars):** Methodology standard. Find discovery paper (or latest reanalysis) in ADS → curated entry. Batch rebuild: use NASA Archive `ps` table + per-planet bibcode validation; no "batch shortcut" skipping method verification. RV planets: check DACE for missing ω, T_peri. **Phase 2 (on decision to implement in-game):** Full source pool. Methodology priorities 1–5 all checked; all published measurements accumulated; method-tier conflicts reported.
**Why:** Phase 1 everywhere = 144 stars × 5+ hours each = infeasible. Phase 2 for in-game systems only (1–2 per release cycle) = reasonable depth. DB completeness + work efficiency tradeoff.
**Details:**
- Phase 1: method labels can be `unverified` (marks Phase 2 targets)
- Phase 2: manually read each paper, verify method type
- Never: fabricate method labels or use batch pseudonyms
- For batch: use NASA Archive composite (`pscomppars`) is forbidden; use per-paper rows (`ps`) + `default_flag=1`
**Source:** `feedback_planet_curation.md`

### 4.3 Skip metallicity [Fe/H]
**Rule:** New Phase 2 hosts: skip metallicity investigation. Existing entries are retained (not deleted).
**Why:** Impact on KSP gameplay is negligible. (1) Stellar color: [Fe/H] is 3rd-order line-blanketing tie-break, all Phase 3 notes say "below perception." (2) Magnetic field: driven by rotation + activity, not [Fe/H]. (3) Kopernicus: no metallicity field. (4) Age: weak secondary use; age itself doesn't affect KSP render.
**Details:** Priority order (highest→lowest impact): rotation > activity > Teff/R/L/mass > age > metallicity(skip).
**Source:** `feedback_skip_metallicity.md`

### 4.4 Interesting-first & cascade coupled values
**Rule:** When applying interesting-first to one Decisions value, cascade all physically-coupled values (albedo, extent, temperature basis, atmosphere framing, prose, visual) to stay internally consistent. Document canonical (literature-faithful) alternative in "## Canonical alternatives" table.
**Why:** One cell change ripples. Theory must still support the "interesting" pick (theory-ruled-out interesting is bad). Canonical must be preserved alongside.
**Example:** TRAPPIST-1 f eyeball-ocean support collapsed under snowball GCMs → pick Europa-analog subglacial ocean instead (still interesting, supported by theory).
**Source:** `feedback_interesting_first_cascade.md`

### 4.5 Gameplay variety bias
**Rule:** Unless "must not exist" (confirmed non-existence, retraction, fabrication), always choose gameplay richness. Include borderline cases: tentative detections, M sin i candidates, astrometric singles. Document cultural divergences (40 Eri A b Trek-Vulcan retraction, tau Ceti e false-positive) in "Canonical alternatives" + cultural-context.md.
**Why:** NearStars is KSP content first; scientific conservatism is secondary.
**Details:**
- Satellites: add generously; verify dynamics via stability-sim
- Ring caution: search-and-verify only; never generate-to-satisfy (burned by delta Pav fabrication)
- Retracted planets with cultural weight (Trek, PHM Adrian): keep with dissenting prose + variant; never re-retract
**Source:** `feedback_gameplay_variety.md`

### 4.6 Phase 4 art-direction facets & choices
**Rule:** Phase 4 must present every visual facet (color, feature, surface, atmosphere) to the owner with 2–4 options each. Owner chooses explicitly at least once per facet. Art-direction document (`phase4/<body>-art-direction.md`) accumulates rich context (palette hex, feature scale, mood, signature landscapes) separately from terse board (phase4/*.yaml).
**Why:** Owner wants explicit agency over all visual decisions, supported by rich reference material.
**Details:** Don't silent-passthrough. Board entries are gated outputs; art-direction docs hold research depth (Parallax grain size, EVE cloud physics, Firefly temperature anchors) for texture/visual pass. Science-report text (per-biome context) is separate future work.
**Source:** `feedback_phase4_facet_choices.md`

---

## 5. Database & Pipeline Architecture — NEARSTARS-SPECIFIC

### 5.1 DB principle: null ≠ zero
**Rule:** The `derived` block in `db/systems/*.json` performs **unit conversion + measurement merging only**. No measurement → `null` (not default like 0 or 90°). Defaults (inclination=90, eccentricity=0) are Kopernicus cfg responsibility.
**Why:** Measured 0 (e.g., Proxima b ecc=0) must be distinguishable from assumed-absent. Downstream cfg writers need null to pick mod-appropriate defaults.
**Details:** `build_planet_derived` must use priority merge (curated > tepcat > raw) → null, never fallback to `0.0`.
**Source:** `project_nearstars_db_principle.md`

### 5.2 Canonical naming: _naming.py single module
**Rule:** All slug/filename transformations (`to_url_slug`, `to_file_slug`, `to_filename`) live in **`scripts/pipeline/_naming.py`** only. All builders import from it; no reimplementation.
**Why:** Barnard's split into `barnard-s` / `barnards` (git history) → manifest mismatches. Single source prevents divergence.
**Details:** URL slug `-` separator; file slug `_` separator. Lowercase → apostrophe-drop → compress non-alnum.
**Source:** `project_naming_canonical.md`

### 5.3 Curation data contract & convergence discipline
**Rule:** `phase2/curation-data-contract/SPEC.md` is the canonical definition of Phase 2/3 data requirements. Convergence discipline: pin every cited value's arxiv_id in `docs/phase3/_bib/<slug>.yaml` → fetch **once** into gitignored cache via `fetch_arxiv_texts.py` → read cache only (never live web). One host at a time; multi-layer edits (DB + narrative + ko mirror) in one commit; `check.sh` gate after each.
**Why:** Non-deterministic live web search caused audit divergence (each run found different papers, different values). Frozen cache + single-pass + one-host-at-a-time = reproducible.
**Details:** Host 1 template becomes verified pattern; parallel subagent batch only after template proven. 40 Eri A/B/C verified clean (all 20 arxiv_ids resolved) on 2026-05-29.
**Source:** `project_nearstars_curation_contract.md`

### 5.4 db/systems/*.json is strictly derived (not hand-edited)
**Rule:** `db/systems/*.json` is **output** of `build_systems.py`. Never edit directly. All enrichment lives in source layer: `stellar_props_curated.json`, `planets_curated.json`, `binary_orbits.json`, `disks_curated.json`. Rebuild reproducibility invariant: no substantive diffs unless source layer changed.
**Why:** 2026-05-27 fix (commit 3ac7f55). Phase 3 work had written hand-curated entries directly to system files; next build would silently erase them (~44 disk entries + narrative notes). Mechanical invariant prevents human-error surprise.
**Details:** Extension points exist (`meta_notes`, `sources_extra`, per-measurement build-control fields) for enrichment. Use them instead of hand-editing output.
**Source:** `project_build_systems_wipes_phase3_enrichment.md`

### 5.5 Ring/disk fabrication — search-and-verify discipline
**Rule:** Never invent debris/circumplanetary rings to satisfy a "add stars with rings" request. Always search-and-verify from cited sources.
**Why:** 2026-05-29 delta Pav fabrication (fake "Lawler & Tanner 2014" paper + invented 30–80 AU geometry). DUNES actually non-detected it. Positive precedent: Alpha Cen A b ring (Beichman 2025 JWST F1550C brightness admits optically-thick ring model) was search-verified.
**Details:** All disk hosts audited for source validity (7 done 2026-05-29). Multi-belt support added; disk color synthesized via Mie scattering (grain+composition) for IR/mm-only disks (Vega, Fomalhaut inner, eps Eri); measured-color disks (Fomalhaut main = grey, AU Mic = blue) anchored directly.
**Source:** `project_nearstars_ring_fabrication.md`

---

## 6. Rolled-Back Patterns — Do Not Re-Propose

### 6.1 LLM wiki (Karpathy pattern) — rolled back 2026-05-25
**Rule:** Do NOT propose YAML frontmatter, wikilink flow-lists, `[[related]]` metadata injection, slash commands `/wiki-*`, pre-commit hooks, or weekly lint cron for docs automation. This was tried (commits 5661c4d → 7f40a77) and rolled back in 1d1c43b.
**Why:** (1) User goal = "minimum interference with project files"; 14-line YAML in 59 files violated that. (2) Wikilinks in YAML violate spec (Obsidian special-case; breaks in other viewers). (3) Weekly cron + 4 slash commands = overkill for personal project scale. (4) Standard `## Related` sections (markdown links) give same Obsidian graph density without file body modification.
**Details:** Use `.obsidian/` overlay + entity/concept/synthesis files for structure (already retained in rollback). Semantic similarity was tried (Smart Connections + Ollama) but Pro subscription required ($30/mo).
**Source:** `feedback_llm_wiki_rolled_back.md`

### 6.2 NearStars paper (methodology) — parked 2026-06-18
**Rule:** Formal paper write-up (figures, venue submission, quantified reproducibility) is **parked**. Current action = accumulate methodology rigor in context-notes.md (per-workspace). Don't initiate paper figures, don't propose venues, don't actively draft.
**Why:** User said "for now, just write context-notes carefully." Paper work would distract from core Phase 2/3/4 gameplay build.
**Details:** Four foundational columns identified (reproducible pipeline, multi-star epoch propagation, stability re-verification, external-observer benchmark) would form one astro-ph.IM paper. Plan saved in `plans/paper-scoping.md` (PARKED tag). Resume signal awaits.
**Source:** `project_nearstars_paper_parked.md`

---

## Cross-Memo Observations & Potential Gaps

### Overlaps & Reinforcements
- **Autonomy family:** [[feedback_autonomy]] (do the work) + [[feedback_agent_token_saving]] (delegate heavy reads) + [[feedback_star_addition]] (pre-delegated rules) form a coherent autonomy philosophy.
- **Paper discipline:** [[feedback_derived_value_grounding]] + [[feedback_ads_paper_discipline]] both enforce frozen-cache, avoid web re-search.
- **Curation depth:** [[feedback_planet_curation]] (two-tier) + [[feedback_skip_metallicity]] (impact-driven prioritization) together shape resource allocation.
- **Interesting-first loop:** [[feedback_interesting_first_cascade]] (cascade values) ↔ [[feedback_gameplay_variety]] (bias toward richness) ↔ [[feedback_phase4_facet_choices]] (owner drives options).

### Potential Conflicts or Clarifications Needed
1. **Subagent cost vs. value-check:** [[feedback_agent_token_saving]] trusts subagents with frozen cache. [[feedback_audit_cost_discipline]] warns against per-finding fan-out. These are compatible (use frozen cache + batch per report), but the transition point (when to use agents vs. main-thread check.sh) could be clearer for future sessions.

2. **Interesting-first theory override:** [[feedback_interesting_first_cascade]] says "observation/theory still wins" but [[feedback_gameplay_variety]] says "bias toward richness unless must-not-exist." Both are true: interesting-first picks a *supported* reading, not an unsupported one. Theory-ruled-out is the only hard constraint; borderline/marginal cases lean toward gameplay.

3. **Metadata in derived values:** [[project_nearstars_db_principle]] says no defaults in derived; [[feedback_derived_value_grounding]] says cite method. These don't conflict but could be clearer: curated entries have source citations (in sources_extra); derived just transforms them without re-justifying.

### Recommendations for Formalization
- **High priority (formalize to CLAUDE.md or CONVENTIONS.md soon):**
  - Sections 1.1–1.9 (Communication & Language) are broadly applicable + stable
  - Sections 2.1–2.5 (Autonomy & Workflow) are portable and well-tested
  - Sections 3.1–3.3 (Grounding & Papers) are portable and reduce recurring errors

- **Medium priority (document in project README or nearstars-specific doc):**
  - Sections 4.1–4.6 (NearStars curation). These are good but NearStars-specific; could graduate to `NEARSTARS-CONVENTIONS.md` or live in skill SKILL.md files.

- **Lower priority (keep as memory, reference as-needed):**
  - Sections 5 (Database & Pipeline). These are architectural and rarely change; memory references (and code comments in the builders) may be sufficient.
  - Section 6 (Rolled-back patterns). These are warnings to future sessions; valuable as persistent memory to prevent re-proposing.

---

**Draft completed:** 2026-07-01  
**Consolidation scope:** 21 feedback_*.md files + 5 project_*.md files + 2 rolled-back patterns  
**Word count:** ~3,500 words
