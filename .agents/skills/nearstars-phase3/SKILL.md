---
name: nearstars-phase3
description: >
  Run NearStars Phase 3 synthesis — turn paper-cited Phase 2 measurements
  into cfg-ready decisions for KSP visual + atmosphere + rotation + interior
  cfg writing. Trigger this skill whenever the user wants planet-level
  cfg-ready values or full Phase 3 reports — phrases like "Phase 3 진행",
  "행성 합성", "<별/행성 이름> Phase 3", "<planet> 합성 격상", "행성 합성
  데이터", "cfg-ready 값 만들어줘", "이 행성 Phase 3 까지 올려줘",
  "synthesize <planet>", or any time the conversation involves drafting
  the per-planet Decisions table + Surface / Atmosphere / Rotation /
  Visual narrative sections. The output is a bilingual web report
  (`docs/phase3/<slug>.html`) that feeds downstream cfg writers
  (`kopernicus-cfg`, `principia-cfg`). Do NOT trigger this skill for
  Kopernicus cfg writing (use `kopernicus-cfg`) or Principia cfg writing
  (use `principia-cfg`) — Phase 3 is the synthesis layer that *feeds*
  those cfg writers, not the cfg writers themselves. Also do NOT trigger
  for adding a new star to the DB (use `nearstars-add-star`) or for
  Phase 2 (paper-cited measurement curation, handled inside
  `nearstars-add-star`).
---

# NearStars — Phase 3 Synthesis

This skill drives the per-planet "cfg-ready synthesis" pass that sits
between Phase 2 (paper-cited measurements) and the downstream cfg
writers. Phase 3 decides values that **no single paper provides**:
surface tints under M-dwarf illumination, atmosphere composition under
escape constraints, cloud morphology under tidally-locked GCM
predictions, rotation state under chain-resonance dynamics. It is
intentionally a human-judgment-driven step — the automation handles
data gathering, but **you** synthesize the decision.

---

> **Scope.** This skill drives the **workflow and judgment** of
> producing Phase 3 outputs. The standard 6-section markdown template
> (intro / Decisions / Surface / Atmosphere / Rotation / Visual /
> Bibliography / Open items) is documented in
> [`references/synthesis-template.md`](references/synthesis-template.md).
> The authority + relevance scoring schema is in
> [`references/scoring-reference.md`](references/scoring-reference.md).
> Conflict resolution rules are in
> [`references/conflict-resolution.md`](references/conflict-resolution.md).

---

## Trigger Recap

You are running this skill if any of these hold:
- The user named a planet (or star with planets) and asked for Phase 3,
  cfg-ready synthesis, "행성 합성", or "<planet> 합성 격상".
- The user wants to extend the existing 7-planet TRAPPIST-1 Phase 3
  template to a new system.
- The user explicitly references the Decisions table, surface tint,
  atmosphere composition, or cloud morphology cfg values.

If the request is about **writing the Kopernicus cfg**, stop — that's
`kopernicus-cfg` and reads Phase 3 outputs. If it's **Principia cfg**,
use `principia-cfg`. If it's **adding a new star to the DB**, use
`nearstars-add-star`. Phase 3 sits between those.

---

## Time and scope warning

Phase 3 is the most expensive curation tier. Realistic budget:

| System size | Approx model time |
|---|---|
| Single-planet system | 1–3 h |
| 2–3 planet system | 3–6 h |
| Full 7-planet system (TRAPPIST-1 scale) | 6–15 h |

The cost is dominated by deep-reading the must-read paper set (~15–30
papers per planet after filtering). Tell the user up front so they can
budget the session.

Phase 3 outputs need Phase 2 measurements as inputs (per
[[project-nearstars-phase-distinction]]). If the target system has
only Phase 1 curation, escalate per
[[feedback-planet-curation]] first.

---

## Workflow Overview

```
1. Pre-flight    ← confirm Phase 2 done, create checklist + context-notes
2. Bibliography  ← per-planet + system-level ADS+arXiv queries
3. Expand        ← 1-hop citation graph walk to catch references
4. Score+filter  ← authority + relevance scoring, mark low-tier as skipped
5. Fetch         ← arXiv full text for must-read papers
6. Triage        ← classify must-read / skim / skip explicitly
7. Deep-read     ← extract concrete cfg-relevant numbers
8. Draft English ← per-planet 6-section markdown
9. Verify        ← re-read every Decisions row against the cited paper
10. Korean mirror← natural-prose translation, block-parity
11. Build HTML   ← + reports index + visual browser check
12. Followup doc ← non-arXiv papers tiered as A/B/C
13. Commit       ← per-planet (default) or per-system
```

Steps 2–5 are mostly mechanical and parallelize well. Steps 7–10 are
where the synthesis judgment lives — these are where you should slow
down and verify.

---

## Step 1 — Pre-flight

Goal: cheap upfront work that prevents painful surprises later.

1. **Confirm Phase 2 is done** for every planet in the target system.
   Check `db/planets_curated.json` for `physical` array entries with
   real measurements (not just NASA-Archive auto-fill). If Phase 2 is
   incomplete, **stop and ask the user** whether to:
   - Escalate Phase 2 first (use `nearstars-add-star` with "Phase 2 격상")
   - Proceed with Phase 1 inputs (degrades synthesis confidence)
2. **Create the working dir** per CLAUDE.md §7:
   ```bash
   mkdir -p phase3/<system_slug>
   ```
   Inside, create:
   - `checklist.md` — per-planet items as checkboxes
   - `context-notes.md` — append-only log of decisions during the work
3. **Set the per-system Phase 3 directory** as the working state — not
   `docs/phase3/` (which is the output area).

---

## Step 2 — Per-planet bibliographies

For each planet, build a focused bibliography:

```bash
python3 scripts/phase3/build_bibliography.py "<System> <letter>"
# e.g. "TRAPPIST-1 d"
```

Output: `docs/phase3/_bib/<slug>.yaml` with ADS + arXiv hits, status
field `pending`. Idempotent — re-running merges new entries.

If the system has 6+ planets, run them sequentially (arXiv 3 s rate
limit is per-IP; parallel hits 429).

---

## Step 3 — System-level supplementary bibliography

ADS+arXiv keyword search by planet letter misses system-wide papers
(e.g. Lincowski 2018 "Evolved Climates and Observational
Discriminants for the TRAPPIST-1 Planetary System" — discusses all 7,
appears only inconsistently per-planet). Run the system-level query
separately:

```bash
python3 scripts/phase3/build_bibliography.py "<System>" --system --max 200
# → docs/phase3/_bib/_system-<slug>.yaml
```

The synthesis files for each planet draw from both the per-planet bib
AND this system pool.

---

## Step 4 — Expand 1-hop citations

ADS+arXiv keyword search alone misses papers cited by the primary
references (e.g. Piaulet 2025 cites Greene 2023; if the keyword query
doesn't find both, the synthesis misses one). Walk the citation graph
1 hop:

```bash
python3 scripts/phase3/expand_citations.py docs/phase3/_bib/<slug>.yaml \
    --max-per-seed 60 --since-year 2000
```

Expect 10–25× growth in bib size. Most of the new entries are noise
(cited methodology, unrelated comparison objects) — filter in Step 5.

---

## Step 5 — Score + filter

Apply authority + relevance scoring to weed out the noise:

```bash
python3 scripts/phase3/score_papers.py docs/phase3/_bib/<slug>.yaml \
    --keep-threshold 8
```

Score interpretation (full schema in `references/scoring-reference.md`):

| Combined score | Decision | Action |
|---|---|---|
| ≥ 14 | must-read | deep-read in Step 7 |
| 8–13 | borderline / cite-only | OK as bibliography entry, skim only |
| < 8 | skip | mark `status: skipped` to prevent arXiv fetch |

After scoring, mark low-tier papers as `status: skipped` so
fetch_arxiv_texts.py won't waste arXiv API calls on them:

```python
import yaml
for slug in ['<planet-slugs>...']:
    with open(f'docs/phase3/_bib/{slug}.yaml') as f:
        bib = yaml.safe_load(f)
    for p in bib['papers']:
        if p.get('combined_score', 0) < 14 and p.get('status') == 'pending':
            p['status'] = 'skipped'
            p['skip_reason'] = f"below_score_threshold ({p['combined_score']} < 14)"
    with open(f'docs/phase3/_bib/{slug}.yaml', 'w') as f:
        yaml.safe_dump(bib, f, sort_keys=False, allow_unicode=True, width=140)
```

---

## Step 6 — Fetch arXiv texts

For all papers still `status: pending` with `arxiv_id` set, fetch
ar5iv HTML + extracted markdown:

```bash
python3 scripts/phase3/fetch_arxiv_texts.py docs/phase3/_bib/<slug>.yaml
```

Output: `docs/phase3/_papers/<arxiv_id>.{html,md}` (git-ignored,
regenerable).

Idempotent: already-fetched papers are skipped. arXiv rate limit 3 s
is enforced.

---

## Step 7 — Triage explicitly

Write a triage decision per paper. The score from Step 5 is a first
pass; you still need to confirm each `combined_score >= 14` paper is
genuinely useful.

For each high-score paper, classify into:
- **deep_read**: visual/scenario-informative — drives a Decisions row
- **skim**: methodology only, or sister-planet comparison only
- **skip**: turns out to be irrelevant on closer look (other system,
  proposal, biosignature without atmosphere)

This is the gate before Step 8. Don't draft synthesis prose without
having explicitly read the deep_read set in full — abstract-only
drafting introduces sloppy citations (see
[[feedback-phase3-validation]]).

---

## Step 8 — Deep-read with cfg-decision focus

For each deep_read paper, open `docs/phase3/_papers/<arxiv_id>.md`
and extract:

| Looking for | Why |
|---|---|
| Specific surface temperature numbers (substellar, nightside, global mean) | `dayside_surface_temp_k`, `nightside_surface_temp_k` |
| Atmospheric pressure / composition with σ bounds | `atmosphere_surface_pressure_pa`, `atmosphere_composition` |
| GCM cloud morphology predictions (latitude/longitude patterns) | `cloud_morphology`, `cloud_cover_fraction` |
| Surface albedo, dayside brightness temperature | `bond_albedo`, `dayside_brightness_temp_k_*` |
| Tidal / induction / radiogenic heating flux (W/m²) | `tidal_heating_w_m2`, `induction_heating_w_m2` |
| Water mass fraction, ocean depth, basal-melt physics | `water_mass_fraction`, `ocean_present`, `ocean_extent_substellar_radius_deg` |
| Spin-orbit state (1:1 vs 3:2), obliquity damping | `tidally_locked`, `obliquity_deg` |
| Mineralogy / surface composition predictions | `surface_tint_rgb_hex_*`, `surface_morphology` |
| Stellar XUV flux, microflare statistics | (atmosphere retention caveats) |

Record findings in `phase3/<system>/context-notes.md` as you go, with
the paper's arxiv_id beside each number. This is the audit trail.

If a paper conflicts with current cfg decisions, see
[`references/conflict-resolution.md`](references/conflict-resolution.md).

---

## Step 9 — Draft English synthesis

Standard 6-section structure at `docs/phase3/<slug>.md` (use
TRAPPIST-1 d as the canonical example — `docs/phase3/trappist-1-d.md`):

```
<!-- one-line Korean header comment (CLAUDE.md §6) -->
# <Planet> — Phase 3 Synthesis

(intro paragraphs — observational state, adopted scenario, alternatives)

## Decisions
| Field | Value | Confidence | Basis |

## Surface synthesis
## Atmosphere synthesis
## Rotation & spin synthesis
## Visual styling

## Bibliography
### Read (visual-informative, drove decisions above)
### Read (context / methodology, not decision-driving)
### Read (instrument-only, not visual-informative)
### Not read — no arXiv preprint or low-priority (~N papers)

## Open items for follow-up
```

Full annotated template + decision-table field reference:
[`references/synthesis-template.md`](references/synthesis-template.md).

---

## Step 10 — VERIFY the Decisions table

Single most important step. For every row in the Decisions table:

1. **Open the cited paper** in `docs/phase3/_papers/<arxiv_id>.md`.
2. **Search for the specific number** you wrote in the Value column.
3. **Confirm author and year** match the actual paper header (not
   from memory — the markdown file has the header).
4. **Confirm method** matches the paper's actual methodology.

Common errors caught at this step (from the TRAPPIST-1 b/c/e/g/h
first pass):

- Citing "Bolmont 2020" when the paper is actually Brasser 2019
  (1905.00512). Always confirm author from arxiv ID, not reconstructed
  memory.
- Citing a number that's 5–10× off the actual paper (b's
  `tidal_heating_w_m2` was 0.04–0.2 in first pass, actual paper says
  0.5–1 W/m²). Re-read the paper's number; don't trust prior cfg.
- Number rounding error (h's `insolation_s_earth` was 0.16, actual
  Agol 2021 is 0.144). Use the paper's value, not the rounded one.
- Composition row contradicts a constraint in the cited paper (h had
  CO₂ 70%, but Bolmont 2018 review caps CO₂ partial pressure at
  100–1000 ppm regardless of background).

See [[feedback-phase3-validation]] for the full failure-mode list.

---

## Step 11 — Korean mirror (natural prose, block-parity)

Write `ko/docs/phase3/<slug>.md` with the SAME block structure as
the English source (`build_html.py` will fail loudly otherwise).
Block structure = number of paragraphs, table rows/columns, list
items, heading levels — must match exactly.

The Korean must read as **natural Korean**, not literal translation
(per [[feedback-ko-mirror-style]] — user explicit complaint after the
TRAPPIST-1 first pass). Rewrite each paragraph for natural flow:
verb-final, particle-driven, drop redundant English connectives.

Style policy:

| Item | Rule |
|---|---|
| Sentence terminator | `.`, `?`, `!` — never `:` (per CLAUDE.md §5) |
| Speech level | 존댓말 informal (`-입니다 / -합니다`) |
| Decisions-table field names | Keep in English/code form (e.g. `tidally_locked`) |
| "Basis" column prose | Translate to Korean |
| Established Korean terms | Use (조석 고정, 맨 암석, 거주 가능 영역, 암석 행성) |
| Romanized technical terms | Keep when no natural Korean (ultramafic, albedo, Rayleigh, GCM, ppm) |
| Bibliography paper titles | Keep in English |
| Bibliography descriptions | Translate to Korean |

---

## Step 12 — Build HTML + reports index

```bash
python3 scripts/phase3/build_html.py <slug>
python3 scripts/pipeline/build_reports_index.py
bash scripts/check-mirrors.sh
```

`build_html.py` pairs the English + Korean files by block order. It
fails loudly on mismatch — fix the ko mirror (not the en source) if
counts diverge.

`build_reports_index.py` refreshes `docs/reports.html` +
`docs/reports-manifest.json` with the new Phase 3 chips.

`check-mirrors.sh` verifies all `docs/` ↔ `ko/docs/` pairs are in
sync per AGENTS.md §2.1.

---

## Step 13 — Browser visual check (don't trust build success alone)

Start the preview server:
```bash
python3 -m http.server 8765 --directory docs > /dev/null 2>&1 &
open http://localhost:8765/phase3/<slug>.html
```

Visually verify:
- Lang toggle (한/EN) works and swaps text
- The Decisions table renders with correct column count
- New table rows show up (a build pass doesn't guarantee rendering)
- Bibliography links resolve (or at least show plausible titles)

If anything looks wrong, fix the en or ko markdown — don't hand-edit
the HTML.

---

## Step 14 — Non-arXiv paper followup

Some high-authority papers have no arXiv preprint (especially recent
Nature / Nature Astronomy, JWST conference proceedings, PSJ early
access). They show up in the scored bibliography with
`combined_score >= 14` but no `arxiv_id`. The skill cannot fetch
them automatically.

Document them in `phase3/<system>/manual-paper-followup.md` with
tiered priority:

- **Tier A** — likely to change cfg decisions; flag for user paste
- **Tier B** — useful context; can wait
- **Tier C** — conference summaries / catalogs; safe to skip

See `phase3/trappist-1-system/manual-paper-followup.md` for the
established format.

When the user pastes back the abstract or full text from such a
paper, save it as `docs/phase3/_papers/<bibcode>.md` and integrate
findings via Step 8 / Step 10 (verify pass).

---

## Step 15 — Commit

Default granularity: per-planet (one commit per planet's synthesis).

Acceptable alternatives:
- Per-system (single commit for all planets in a system — used for
  TRAPPIST-1 b/c/d/e/f/g/h initial pass since they share host star
  context)
- Per-stage (one commit each for English drafts, then Korean mirrors,
  then HTML — useful if synthesis takes multiple sessions)

Per [[feedback-git-identity]], all commits use
`VaNnadin <vannadin00@gmail.com>` via inline `git -c user.name=... -c
user.email=...`. Per CLAUDE.md §9, commit message describes the
**why**, not the file list.

After commit, push to `origin/main` only if the user explicitly asks.

---

## Key Policies (from user memory)

These are user-confirmed defaults. Do NOT ask the user about them.

- **Phase 3 inputs are Phase 2 measurements** ([[project-nearstars-phase-distinction]]).
  Phase 3 cannot bypass Phase 2; if Phase 2 doesn't exist, escalate
  via `nearstars-add-star` first.
- **Deep-read before draft** ([[feedback-phase3-depth]]). Abstract-only
  synthesis introduces fact errors. Always read the deep_read set in
  full first.
- **Verify decisions against source** ([[feedback-phase3-validation]]).
  Every Decisions-table number gets re-checked against the cited
  paper before commit.
- **Natural Korean from the start** ([[feedback-ko-mirror-style]]).
  Don't draft a literal translation then rewrite — the user will
  notice and ask for a redo.
- **English by default** ([[feedback-md-language]]). English is the
  source of truth; Korean is the mirror at `ko/docs/...`.
- **존댓말 always** ([[feedback-speech-level]]). User-facing prose
  in Korean uses 존댓말 informal.
- **Phase 2 first, Phase 3 escalates only when needed** ([[feedback-planet-curation]]).
  Default cfg target is Phase 1 + Phase 2; Phase 3 only when user
  explicitly asks for synthesis or when an implementation decision
  requires it.
- **Workflow encoded in [[feedback-phase3-process]]** — the canonical
  per-pass order documented when the TRAPPIST-1 set was finalized.

---

## Autonomy guards (autonomy ≠ carelessness)

Autonomous execution is the default per [[feedback-autonomy]], but
these actions require explicit confirmation or a Read-first step.

- **Read before overwriting an existing synthesis.** A planet may
  already have a Phase 3 markdown from a previous session. Inspect
  the current decisions before replacing — older decisions may have
  been validated against papers that aren't in the current
  bibliography.
- **Confirm before deleting bibliography entries.** Score-filtering
  marks low-tier as `skipped`, which preserves the audit trail. Do
  not literally delete entries from the YAML — confirm with user
  first if a cleanup is requested.
- **Out-of-scope actions stop and flag.** Kopernicus cfg generation
  (use `kopernicus-cfg`), Principia cfg (use `principia-cfg`), GitHub
  push without user request — all out of scope.

---

## Common pitfalls

Quick handling reference. Full details in
[`references/troubleshooting.md`](references/troubleshooting.md) (if
issues recur often enough to need a written ref).

| Symptom | Likely cause | Fix |
|---|---|---|
| `build_html.py` block count mismatch | Korean file edited without keeping block structure | Rewrite the affected ko paragraph/table/list block to match en exactly |
| `check-mirrors.sh` reports a stale mirror | en source edited after ko mirror was finalized | Rewrite ko block-for-block; re-run check |
| Bibliography ballooned to 1000+ entries after expansion | Citation expansion added noise | Score-filter aggressively (`--keep-threshold 8`), then mark `< 14` as skipped |
| Synthesis prose cites "Bolmont 2020" but paper is Brasser 2019 | Author reconstruction from memory | Always confirm author from `docs/phase3/_papers/<arxiv_id>.md` header before drafting |
| Number in Decisions table doesn't match the cited paper | First-pass draft from prior cfg or abstract | Re-read the paper's specific number; update both the table and the prose |
| Phase 2 missing for one planet in the system | Phase 1 auto-fill only | Stop, escalate Phase 2 via `nearstars-add-star`, then resume Phase 3 |

---

## Related documents

Reference material consulted by the skill but not part of its
operating loop:

- `docs/reference/guideline.md` — project-level scope, dependencies,
  distance limits (Phase 3 is distance-agnostic; only cfg layers
  enforce 50 ly / 80 ly limits)
- `docs/phase3/trappist-1-d.md` — canonical example synthesis (pilot)
- `docs/phase3/trappist-1-{b,c,e,f,g,h}.md` — additional examples
  (extended from the pilot through the 2026-05-22 session)
- `phase3/trappist-1-system/{checklist,context-notes,manual-paper-followup,paper-count-summary}.md`
  — working artifacts from the TRAPPIST-1 build, useful as templates
- `docs/reference/methodology.md` — overall DB and curation philosophy
- `docs/reference/principia-cfg-reference.md` and the
  `principia-cfg` skill — downstream consumer of Phase 3 dynamics
  outputs
- `docs/reference/adding_stars.md` and the `nearstars-add-star` skill
  — upstream Phase 1/Phase 2 producer
