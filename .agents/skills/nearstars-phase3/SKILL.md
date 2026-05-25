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
  Visual narrative sections. Output is a bilingual web report
  (`docs/phase3/<slug>.html`) that feeds the cfg writers downstream.
  Do NOT use for Kopernicus cfg (`kopernicus-cfg`), Principia cfg
  (`principia-cfg`), new-star DB entry, or Phase 2 measurement
  curation (both handled by `nearstars-add-star`).
---

# NearStars — Phase 3 Synthesis

Phase 3 turns paper-cited Phase 2 measurements into cfg-ready decisions
for values that **no single paper provides**: surface tints under
M-dwarf illumination, atmosphere composition under escape constraints,
cloud morphology under tidally-locked GCM predictions, rotation state
under chain-resonance dynamics. The automation gathers data; **you**
synthesize the decision.

This file drives workflow + judgment. Detail lives in references/:

- [`synthesis-template.md`](references/synthesis-template.md) — the 6-section markdown template
- [`scoring-reference.md`](references/scoring-reference.md) — authority + relevance schema
- [`conflict-resolution.md`](references/conflict-resolution.md) — tie-break, divergence, failure modes
- [`mod-grounded-fields.md`](references/mod-grounded-fields.md) — which cfg fields each Phase 3 row feeds

---

## Out of scope

If the request is Kopernicus cfg generation → `kopernicus-cfg`.
Principia cfg → `principia-cfg`. Adding a new star to the DB or Phase
1/2 curation → `nearstars-add-star`. Phase 3 sits between those.

---

## Workflow Overview

```
 0. Time estimate     ← quote budget table to user, confirm before starting
 1. Pre-flight        ← confirm Phase 2 done, create checklist + context-notes
 2. Bibliography      ← per-planet ADS+arXiv queries
 3. System bib        ← system-level supplementary bibliography
 4. Expand            ← 1-hop citation graph walk to catch references
 5. Score+filter      ← authority + relevance, mark low-tier as skipped
 6. Fetch             ← arXiv full text for must-read papers
 7. Triage            ← classify deep_read / skim / skip / manual_followup
 8. Deep-read         ← extract concrete cfg-relevant numbers
 9. Draft English     ← per-planet 6-section markdown
10. Verify decisions  ← re-read every Decisions row against the cited paper
11. Korean mirror     ← natural-prose translation, block-parity
12. Build HTML        ← build_html.py + reports index + check-mirrors
13. Browser check     ← visual confirmation of lang toggle + rendered table
14. Commit            ← per-planet (default) or per-system
```

Steps 2–5 are mostly mechanical and parallelize well. Steps 7–10 are
where the synthesis judgment lives — these are where you should slow
down and verify.

---

## Step 0 — Share the time estimate with the user

**Do this before any other step.** Phase 3 is the most expensive
curation tier — quote the matching row and confirm before Step 1.
If only Phase 1 inputs exist (per [[project-nearstars-phase-distinction]]),
mention this upfront so the user can escalate Phase 2 via
`nearstars-add-star` or accept degraded confidence.

| System size | Approx model time |
|---|---|
| Single-planet system | 1–3 h |
| 2–3 planet system | 3–6 h |
| Full 7-planet system (TRAPPIST-1 scale) | 6–15 h |

Cost is dominated by deep-reading the must-read set (~15–30 papers per
planet after filtering).

---

## Step 1 — Pre-flight

Goal: cheap upfront work that prevents painful surprises later.

1. **Confirm Phase 2 is done** for every planet in the target system.
   Check `db/planets_curated.json` for `physical` array entries with
   real measurements (not just NASA-Archive auto-fill). If Phase 2 is
   incomplete, **stop and ask the user** whether to:
   - Escalate Phase 2 first (use `nearstars-add-star` with "Phase 2 격상")
   - Proceed with Phase 1 inputs (degrades synthesis confidence)
2. **Create the working dir** per CLAUDE.md §7 (registered in AGENTS.md
   §2 as `phase3/<system>/`):
   ```bash
   mkdir -p phase3/<system_slug>
   ```
   Inside, create `checklist.md` with stage-based checkboxes — the
   canonical pattern from `phase3/trappist-1-system/checklist.md`:
   ```markdown
   ## Stage 1 — bibliography builds (parallel)
   - [ ] build_bibliography.py "<System> b" — N papers, M arxiv
   - [ ] build_bibliography.py "<System> c" — N papers, M arxiv
   ## Stage 2 — arXiv fetches (sequential)
   ## Stage 3 — English synthesis
   ## Stage 4 — Korean mirrors
   ## Stage 5 — verification + HTML
   ```
   And `context-notes.md` as an append-only decision log.
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

Two thresholds matter here and they answer different questions.
`--keep-threshold N` decides what stays in the bibliography at all
(audit-trail retention). `--mark-skipped-below M` decides what gets
fetched in Step 6 (arXiv API budget). They are independent — typical
settings are `--keep-threshold 8 --mark-skipped-below 14`.

```bash
python3 scripts/phase3/score_papers.py docs/phase3/_bib/<slug>.yaml \
    --keep-threshold 8 --mark-skipped-below 14
```

Score buckets: **≥ 14** must-read (Step 6 fetches), **8–13** cite-only
(`status: skipped`, kept in bib), **< 8** dropped. Full schema +
sanity-check counts in [`references/scoring-reference.md`](references/scoring-reference.md).
Idempotent — re-running on `fetched` / `skipped` papers is a no-op.

**verify:** score distribution within ±50% of the sanity-check counts
in `references/scoring-reference.md`. If 14+ count is <5 for a major
system or >50, the keyword set or thresholds need adjustment before
proceeding.

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
- **manual_followup**: high-score (`combined_score >= 14`) but no
  `arxiv_id` — recent Nature / Nature Astronomy, JWST conference
  proceedings, PSJ early access etc. The skill cannot fetch these;
  log them in `phase3/<system>/manual-paper-followup.md` with tiered
  priority:
  - **Tier A** — likely to change cfg decisions; flag for user paste
  - **Tier B** — useful context; can wait
  - **Tier C** — conference summaries / catalogs; safe to skip

  See `phase3/trappist-1-system/manual-paper-followup.md` for the
  established format. When the user later pastes back an abstract or
  full text, save it as `docs/phase3/_papers/<bibcode>.md` and
  integrate via Step 8 / Step 10 (verify pass).

This is the gate before Step 8. Don't draft synthesis prose without
having explicitly read the deep_read set in full — abstract-only
drafting introduces sloppy citations (caught at Step 10 VERIFY).

**verify:** every `combined_score >= 14` paper has an explicit
deep_read / skim / skip / manual_followup classification recorded
in `phase3/<system>/context-notes.md`. No high-score paper left as
`pending`.

---

## Step 8 — Deep-read with cfg-decision focus

For each deep_read paper, open `docs/phase3/_papers/<arxiv_id>.md`
and extract the cfg-relevant numbers. The per-field "what to look for
in the paper" map is in
[`references/synthesis-template.md`](references/synthesis-template.md)
under "Decision-table field map" — use it as the extraction checklist.

Record findings in `phase3/<system>/context-notes.md` as you go, with
the paper's arxiv_id beside each number. This is the audit trail.

If a paper conflicts with current cfg decisions, see
[`references/conflict-resolution.md`](references/conflict-resolution.md).

**verify:** every deep_read paper has at least one extracted number
or qualitative finding logged in context-notes.md alongside its
arxiv_id. A deep_read paper with zero notes means it was actually
"skim" — re-classify in Step 7.

---

## Step 9 — Draft English synthesis

### Step 9.0 — Pre-draft classification (mandatory)

Before writing the synthesis prose, build a per-row classification
table in `phase3/<system>/context-notes.md`. For every Decisions row
you plan to write, apply the diagnostic question from
[`references/conflict-resolution.md`](references/conflict-resolution.md)
§ "Tie-break vs. divergence" and label the row as one of:

- **canonical-aligned** — cfg pick matches the canonical reading.
- **tie-break** — observation/theory silent within the allowed window;
  cfg picks the more interesting option. Basis note suffices.
- **documented-divergence** — canonical has clear weight advantage but
  cfg picks differently. Requires `## Canonical alternatives` row.

Example log entry in `context-notes.md`:

```markdown
## Decisions-row classification — Proxima b

- atmosphere_surface_pressure_pa = 50000     → divergence (Boutle 2017 GCM
  1 bar consensus vs cfg 0.5 bar for clearer ocean-edge visibility)
- ocean_extent_substellar_radius_deg = 60    → divergence (downstream of pressure)
- surface_tint_rgb_hex_primary = #2a4060     → tie-break (within obs window)
- bond_albedo = 0.30                         → canonical-aligned (Boutle 2017)
- ...
```

This step exists because the Alpha Cen first pass (2026-05-22) named
"documented divergence" in prose without creating the section — the
classification log forces every row to have an explicit policy label
*before* the prose is written, so the `## Canonical alternatives`
section can't be silently dropped.

Once the log is complete, report the row counts to the user
(`N canonical-aligned, M tie-break, K divergence`) before moving on
to drafting the markdown.

### Step 9.1 — Standard structure

Use `docs/phase3/trappist-1-e.md` or `trappist-1-f.md` as the
structural template — both apply the documented-divergence policy
in full (`## Canonical alternatives` section + Basis notes).

**Do not** copy from `trappist-1-d.md` as a structural base. d predates
the documented-divergence policy and has no `## Canonical alternatives`
section, so its shape silently omits the section even when the new
planet has a divergence (this is how the Alpha Cen first pass failed).

Section order (full annotated template in
[`references/synthesis-template.md`](references/synthesis-template.md)):
intro → Decisions → Surface → Atmosphere → Rotation & spin → Visual →
`## Canonical alternatives` (optional, only if cfg diverges) →
Bibliography (Read / context / instrument-only / not-read) → Open items.

### Dual-track: when to add Canonical alternatives

The Step 9.0 classification log already labeled each row. Apply the
labels in the prose:

- **tie-break** → Basis: `Tie-break: interesting-first`. No section row.
- **documented-divergence** → Basis: `Documented divergence: see
  Canonical alternatives` + add a row in `## Canonical alternatives` +
  list canonical variant in `## Open items for follow-up`.

Full rules + diagnostic question + worked example in
[`references/conflict-resolution.md`](references/conflict-resolution.md)
§ "Tie-break vs. divergence" and § "Documented divergence". Don't
pad the section with tie-breaks; don't hide divergences inside Basis.

---

## Step 10 — VERIFY the Decisions table

Single most important step. For every row in the Decisions table:

1. **Open the cited paper** in `docs/phase3/_papers/<arxiv_id>.md`.
2. **Search for the specific number** you wrote in the Value column.
3. **Confirm author and year** match the actual paper header (not
   from memory — the markdown file has the header).
4. **Confirm method** matches the paper's actual methodology.

Common failure modes (wrong author, 5–10× off number, rounding error,
composition contradicting a cited constraint) are catalogued in
[`references/conflict-resolution.md`](references/conflict-resolution.md)
§ "Common failure modes" with the actual TRAPPIST-1 first-pass
examples.

**verify:** every Decisions-table row's author/year/number traces back
to a specific page or section in `docs/phase3/_papers/<arxiv_id>.md`.
If any row can't be sourced, fix the row or mark Confidence=low with
an Open-items entry — never commit an unverified Decisions row.

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

**verify:** `build_html.py` exits 0 **and** `check-mirrors.sh` reports
no stale or missing mirrors. A build pass alone is not sufficient —
the mirror check catches the case where en was edited after ko.

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

## Step 14 — Commit

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

## Phase 3-specific policies

Four gates that govern workflow decisions; each is enforced by a
specific step or reference in this skill:

- **Phase 3 needs Phase 2 inputs.** Step 1 pre-flight.
  See [[project-nearstars-phase-distinction]].
- **Every Decisions row re-checked against source.** Step 10 VERIFY.
- **Tie-break defaults to visually distinctive** when observation
  allows multiple readings. Step 8+ plus `references/synthesis-template.md` §
  "Confidence=low rows and the interesting-first rule".
- **Canonical-vs-cfg divergence requires a `## Canonical alternatives`
  section.** Step 9 plus `references/conflict-resolution.md` §
  "Documented divergence".

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

| Symptom | Likely cause | Fix |
|---|---|---|
| `build_html.py` block count mismatch | Korean file edited without keeping block structure | Rewrite the affected ko paragraph/table/list block to match en exactly |
| `check-mirrors.sh` reports a stale mirror | en source edited after ko mirror was finalized | Rewrite ko block-for-block; re-run check |
| Bibliography ballooned to 1000+ entries after expansion | Citation expansion added noise | Re-run `score_papers.py --keep-threshold 8 --mark-skipped-below 14` to filter the bib and exclude low-tier rows from the next fetch |
| Synthesis prose cites "Bolmont 2020" but paper is Brasser 2019 | Author reconstruction from memory | Always confirm author from `docs/phase3/_papers/<arxiv_id>.md` header before drafting |
| Number in Decisions table doesn't match the cited paper | First-pass draft from prior cfg or abstract | Re-read the paper's specific number; update both the table and the prose |
| Phase 2 missing for one planet in the system | Phase 1 auto-fill only | Stop, escalate Phase 2 via `nearstars-add-star`, then resume Phase 3 |

---

## Related documents

- `docs/phase3/trappist-1-{e,f}.md` — canonical structural examples (with divergence section)
- `docs/phase3/trappist-1-d.md` — pilot, predates divergence policy (don't use as template)
- `phase3/trappist-1-system/{checklist,context-notes,manual-paper-followup}.md` — working artifacts as templates
- `docs/reference/{guideline,methodology}.md` — project scope + curation philosophy
- Upstream: `nearstars-add-star` (Phase 1/2). Downstream: `kopernicus-cfg`, `principia-cfg`

---

## Related

- [methodology](../../../docs/reference/methodology.md) — DB-side schema (Phase 1/2 → Phase 3 boundary)
- [data-sources](../../../docs/reference/data-sources.md) — paper citation policy that Phase 3 inherits
- [tools](../../../docs/reference/tools.md) — Phase 3 script index (§3)
- [mod-reference](../../../docs/reference/mod-reference.md) — downstream cfg writers consuming Phase 3 output
- [kopernicus-cfg](../kopernicus-cfg/SKILL.md), [firefly-cfg](../firefly-cfg/SKILL.md) — direct downstream consumers
- [principia-cfg-reference](../../../docs/reference/principia-cfg-reference.md) — Principia-side consumer
- entity pages in `docs/phase3/*.md` — the synthesis output this skill produces
