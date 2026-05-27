# ε Eri b — Phase 3 checklist

Single planet, jovian gas giant. Workspace anchored on host star
`docs/phase3/eps-eri.md` which already triaged the planet-relevant
papers (Mawet 2019, Llop-Sayson 2021, Roettenbacher 2022, MacGregor
2015, Booth 2017, Su 2017, Hatzes 2000, Quillen 2002, Benedict 2006).

## Stage 0 — pre-flight
- [x] Phase 2 present (`db/systems/eps_eri.json` has curated orbital + physical for b)
- [x] Host Phase 3 done (`docs/phase3/eps-eri.md`)
- [x] No prior `docs/phase3/eps-eri-b.md` to overwrite

## Stage 1 — classification log
- [x] Per-row classification table in context-notes.md
- [x] Report canonical-aligned / tie-break / divergence counts

## Stage 2 — English draft
- [x] Header + intro paragraphs
- [x] Decisions table
- [x] Surface synthesis (no hard surface; rephrase as "cloud-deck")
- [x] Atmosphere synthesis
- [x] Rotation & spin synthesis
- [x] Visual styling
- [x] Canonical alternatives (if any divergence)
- [x] Bibliography (4 sub-sections)
- [x] Open items

## Stage 3 — VERIFY pass
- [x] Every Decisions row author/year/number cross-checked against the
      host-Phase-3 extracted numbers (which are sourced from primary papers)
- [x] Mass M_b ≈ 0.78 M_Jup confirmed (Llop-Sayson 2021 deprojected)
- [x] a = 3.53 AU, P = 7.36 yr, e ≈ 0.07 (DB-curated from Llop-Sayson)
- [x] i ≈ 34° (Roettenbacher 2022 + disk plane Booth 2017)

## Stage 4 — Korean mirror
- [x] Block-parity match with English source
- [x] Natural Korean prose, not literal translation
- [x] Sentence terminators are . / ? / ! (no closing colon)

## Stage 5 — verification + HTML
- [x] `python3 scripts/phase3/check_block_parity.py eps-eri-b` exit 0
- [x] `python3 scripts/phase3/build_html.py eps-eri-b` exit 0
- [x] `bash scripts/check-mirrors.sh` exit 0
