# Alpha Cen + Proxima Cen system Phase 3 — checklist

Started 2026-05-22. Re-do after revert of commit 0cd8b2f. This pass
applies the documented-divergence policy (§ `## Canonical alternatives`
structural section + Step 9.0 pre-draft classification gate) from
the start.

**Scope** (5 entries):
- ★ Alpha Cen A (G2V) — slug `alpha-centauri-a`
- ★ Alpha Cen B (K1V) — slug `alpha-centauri-b`
- ★ Proxima Cen / Alpha Cen C (M5.5Ve flare star) — slug `proxima-cen`
- Proxima Cen b (eyeball aquaplanet candidate) — slug `proxima-cen-b`
- Proxima Cen d (Mercury-analog USP) — slug `proxima-cen-d`

**Structural rule.** Use `docs/phase3/trappist-1-e.md` or
`trappist-1-f.md` as base. **Do NOT copy from `trappist-1-d.md`** —
d predates the documented-divergence policy and has no
`## Canonical alternatives` section. Copying d's shape is exactly how
the Alpha Cen first pass failed.

## Stage 0 — pre-flight (done)

- [x] Phase 2 inputs spot-checked — `db/systems/{alpha_centauri_a,alpha_centauri_b,proxima_cen}.json` contain multi-paper `*_measurements` arrays with `recommended` flags. SM25, Pourbaix&Boffin 2016, Kervella 2017, Joyce&Chaboyer 2018, Faria 2022 all attributed.
- [x] Working dir `phase3/alpha-cen-proxima-system/` created
- [x] User confirmed 6–9h budget, Step 9.0 mandatory gate, e/f as base

## Stage 1 — bibliography builds (sequential, arXiv 3 s rate limit)

- [ ] `python3 scripts/phase3/build_bibliography.py "Alpha Centauri A"`
- [ ] `python3 scripts/phase3/build_bibliography.py "Alpha Centauri B"`
- [ ] `python3 scripts/phase3/build_bibliography.py "Proxima Cen"`
- [ ] `python3 scripts/phase3/build_bibliography.py "Proxima Cen b"`
- [ ] `python3 scripts/phase3/build_bibliography.py "Proxima Cen d"`

## Stage 2 — system-level supplementary bibliography

- [ ] `python3 scripts/phase3/build_bibliography.py "Alpha Centauri" --system --max 200`
- [ ] `python3 scripts/phase3/build_bibliography.py "Proxima Cen" --system --max 200`

## Stage 3 — expand citations + score+filter

- [ ] `expand_citations.py` for all 5 per-entry bibs (1-hop, since-year 2000)
- [ ] `score_papers.py --keep-threshold 8 --mark-skipped-below 14` for all 5

## Stage 4 — arXiv text fetches

- [ ] `fetch_arxiv_texts.py` for all 5 yamls (cached in docs/phase3/_papers/, gitignored)

## Stage 5 — triage

- [ ] Every `combined_score >= 14` paper classified deep_read / skim / skip / manual_followup
- [ ] Recorded in `context-notes.md` with arxiv_id beside each
- [ ] `manual-paper-followup.md` created with Tier A/B/C entries for non-arXiv high-score papers

## Stage 6 — deep-read

- [ ] All deep_read papers read with cfg-decision focus
- [ ] Extracted numbers logged in `context-notes.md` with arxiv_id

## Stage 7 — Step 9.0 pre-draft classification (mandatory gate)

For each of the 5 entries, build a per-row classification table:
- **canonical-aligned** — cfg pick matches canonical reading
- **tie-break** — obs/theory silent within window; cfg picks interesting
- **documented-divergence** — canonical has weight advantage but cfg picks differently

- [ ] α Cen A classification table → context-notes.md
- [ ] α Cen B classification table → context-notes.md
- [ ] Proxima Cen classification table → context-notes.md
- [ ] Proxima b classification table → context-notes.md
- [ ] Proxima d classification table → context-notes.md
- [ ] **Report row counts to user** (N canonical / M tie-break / K divergence) and get confirmation before drafting prose

## Stage 8 — English synthesis (after Step 9.0 sign-off)

Structure base: `trappist-1-e.md` or `trappist-1-f.md` (NOT d).
Stars include rotation/activity/X-ray/age + planet-perspective visual.
Mod-grounded fields from start (`mod-grounded-fields.md`):
- Kerbalism: magnetic_field_*, magnetosphere_*, radiation_*
- EVE: aurora_* (color = emission species)
- Scatterer: sunset_color_hex (optional)

- [ ] `docs/phase3/alpha-centauri-a.md`
- [ ] `docs/phase3/alpha-centauri-b.md`
- [ ] `docs/phase3/proxima-cen.md`
- [ ] `docs/phase3/proxima-cen-b.md`
- [ ] `docs/phase3/proxima-cen-d.md`

## Stage 9 — Decisions verify (Step 10)

For every row in every Decisions table, open the cited paper at
`docs/phase3/_papers/<arxiv_id>.md` and confirm author, year, number,
method. Common errors from TRAPPIST-1 first pass: wrong author from
memory, wrong number magnitude, missing context constraint.

- [ ] α Cen A — all rows verified against source
- [ ] α Cen B — all rows verified
- [ ] Proxima Cen — all rows verified
- [ ] Proxima b — all rows verified
- [ ] Proxima d — all rows verified

## Stage 10 — Korean mirrors

Block-parity required. Sentence terminator `.` / `?` / `!` only —
no `:` per CLAUDE.md §5. Speech level: 존댓말.

- [ ] `ko/docs/phase3/alpha-centauri-a.md`
- [ ] `ko/docs/phase3/alpha-centauri-b.md`
- [ ] `ko/docs/phase3/proxima-cen.md`
- [ ] `ko/docs/phase3/proxima-cen-b.md`
- [ ] `ko/docs/phase3/proxima-cen-d.md`

## Stage 11 — HTML + reports index + mirror check

- [ ] `python3 scripts/phase3/build_html.py {alpha-centauri-a,alpha-centauri-b,proxima-cen,proxima-cen-b,proxima-cen-d}`
- [ ] `python3 scripts/pipeline/build_reports_index.py`
- [ ] `bash scripts/check-mirrors.sh` → no stale/missing

## Stage 12 — browser visual check

- [ ] Lang toggle works on all 5
- [ ] Decisions tables render with correct columns
- [ ] `## Canonical alternatives` section appears where divergences exist
- [ ] Bibliography links plausible

## Stage 13 — commit

- [ ] Single per-system commit "Alpha Cen + Proxima Cen Phase 3 synthesis (documented-divergence policy from start)"
- [ ] VaNnadin git identity inline

## Related

- [system-alpha-cen entity pages](../../docs/phase3/alpha-centauri-a.md) — parent topic this workspace contributes to
