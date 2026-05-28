# Teegarden's Star Phase 3 — checklist

Started 2026-05-28. 4-component system (host + b + c + d). All RV-only —
no transits. Earth-mass terrestrial planets; b in inner HZ, c in outer
HZ, d cold outside HZ. M7.0 V ultra-cool host, very quiet, old (~8 Gyr
thick-disc kinematic age).

**Scope** (4 entries):
- Teegarden's Star (M7.0 V host) — slug `teegarden-s-star`
- Teegarden's Star b (inner HZ Earth-mass) — slug `teegarden-s-star-b`
- Teegarden's Star c (outer HZ Earth-mass) — slug `teegarden-s-star-c`
- Teegarden's Star d (cold sub-Earth, Dreizler 2024 discovery) — slug `teegarden-s-star-d`

**Structural rule.** Use `docs/phase3/trappist-1-e.md` (planet) and
`docs/phase3/proxima-cen.md` / `alpha-centauri-a.md` (stellar) as
templates. **Do NOT copy from `trappist-1-d.md`** — predates
documented-divergence policy. Section order: intro → Decisions →
Surface → Atmosphere → Rotation & spin → Visual → `## Canonical
alternatives` (if any) → Bibliography → Open items → Related.

**Slug note.** Pipeline `slugify("Teegarden's Star")` deterministically
emits `teegarden-s-star`, not `teegardens-star` as the brief suggested.
Following pipeline output for reproducibility — matches Barnard's
precedent.

## Stage 0 — pre-flight (done)

- [x] Phase 2 inputs spot-checked — `db/systems/teegardens_star.json`
      contains multi-paper measurement arrays with `recommended` flags
      (Schweitzer 2019, Dreizler 2024, Zechmeister 2019, Cifuentes 2020,
      Passegger 2019, Mann calibrations).
- [x] Radius reconciliation noted: Schweitzer 2019 R=0.107 R☉
      (recommended) vs Dreizler 2024 R=0.12 R☉ (3σ disagreement).
- [x] Working dir `phase3/teegardens_star/` created.
- [x] `system.yaml` with injections for Zechmeister 2019, Dreizler 2024,
      Schweitzer 2019, Cifuentes 2020, Passegger 2019, habitability papers.

## Stage 1 — bibliography builds (Steps 2–6)

- [ ] `python3 scripts/phase3/run_phase3.py teegardens_star`
      → all 5 stages (per-planet bibs, system bib, expand, score, inject, fetch)
- [ ] Verify per-planet paper counts after stage 2

## Stage 2 — triage (Step 7)

- [ ] Every `combined_score >= 14` paper classified
      deep_read / skim / skip / manual_followup
- [ ] Recorded in `context-notes.md` with arxiv_id beside each
- [ ] `manual-paper-followup.md` for non-arXiv high-score papers (if any)
- [ ] `verify_triage.py teegardens_star` → exit 0

## Stage 3 — deep-read (Step 8)

- [ ] All deep_read papers read with cfg-decision focus
- [ ] Extracted numbers logged in `context-notes.md` with arxiv_id

## Stage 4 — Step 9.0 pre-draft classification (mandatory gate)

- [ ] Teegarden's Star classification table → context-notes.md
- [ ] Teegarden b classification table
- [ ] Teegarden c classification table
- [ ] Teegarden d classification table
- [ ] Row counts (N canonical / M tie-break / K divergence) logged

## Stage 5 — English synthesis (Step 9)

Stellar base: `proxima-cen.md` / `alpha-centauri-a.md`.
Planet base: `trappist-1-e.md` (HZ) or `trappist-1-f.md` (cold edge).

- [ ] `docs/phase3/teegardens-star.md`
- [ ] `docs/phase3/teegardens-star-b.md`
- [ ] `docs/phase3/teegardens-star-c.md`
- [ ] `docs/phase3/teegardens-star-d.md`

## Stage 6 — Decisions VERIFY (Step 10)

For every Decisions row, open cited paper in
`docs/phase3/_papers/<arxiv_id>.md` and confirm author, year, number,
method. No row may stand unverified.

- [ ] Teegarden's Star — all rows verified
- [ ] Teegarden b — all rows verified
- [ ] Teegarden c — all rows verified
- [ ] Teegarden d — all rows verified

## Stage 7 — Korean mirrors (Step 11)

Block-parity required. Sentence terminator `.` / `?` / `!` only —
no `:`. 존댓말. Natural Korean prose, not literal translation.

- [ ] `ko/docs/phase3/teegardens-star.md`
- [ ] `ko/docs/phase3/teegardens-star-b.md`
- [ ] `ko/docs/phase3/teegardens-star-c.md`
- [ ] `ko/docs/phase3/teegardens-star-d.md`

## Stage 8 — HTML build + parity check (Step 12)

- [ ] `check_block_parity.py` for all 4 slugs
- [ ] `build_html.py` for all 4 slugs
- [ ] Coordinator handles `build_reports_index.py` + `check-mirrors.sh`
      (per task brief — DO NOT touch reports index)

## Stage 9 — coordinator handoff (Step 14 — no commit)

- [ ] Report bibliography sizes per planet + stellar
- [ ] Report classification counts per file
- [ ] Report VERIFY pass summary
- [ ] List any manual_followup TODOs

## Related

- `docs/phase3/teegardens-star.md` and planets — output entity pages
- `db/systems/teegardens_star.json` — Phase 2 input
