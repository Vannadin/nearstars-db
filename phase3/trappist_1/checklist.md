# TRAPPIST-1 system Phase 3 — checklist

Started 2026-05-21. d is already done as the pilot
(`docs/phase3/trappist-1-d.md`). Goal: extend full d-level synthesis
to the remaining six planets b, c, e, f, g, h.

## Stage 1 — bibliography builds (parallel)

- [x] `python3 scripts/phase3/build_bibliography.py "TRAPPIST-1 b"` — 66 papers, 35 arxiv
- [x] `python3 scripts/phase3/build_bibliography.py "TRAPPIST-1 c"` — 32 papers, 12 arxiv
- [x] `python3 scripts/phase3/build_bibliography.py "TRAPPIST-1 e"` — 64 papers, 30 arxiv
- [x] `python3 scripts/phase3/build_bibliography.py "TRAPPIST-1 f"` — 15 papers, 6 arxiv
- [x] `python3 scripts/phase3/build_bibliography.py "TRAPPIST-1 g"` — 66 papers, 52 arxiv
- [x] `python3 scripts/phase3/build_bibliography.py "TRAPPIST-1 h"` — 53 papers, 43 arxiv

## Stage 2 — arXiv text fetches (sequential per arXiv rate limit)

- [x] All 6 fetched, 0 failures (cached in docs/phase3/_papers/, gitignored)

## Stage 3 — synthesis (English markdown)

Each follows the d template: intro, Decisions table, Surface synthesis,
Atmosphere synthesis, Rotation & spin, Visual styling, Bibliography
(Read / Read — context / Read — instrument / Not read — no arXiv),
Open items.

- [x] `docs/phase3/trappist-1-b.md` — airless ultramafic bare rock (Greene 2023, Ducrot 2024/2025)
- [x] `docs/phase3/trappist-1-c.md` — thin O₂-dominated fossil atmo (Zieba 2023, Lincowski 2023)
- [x] `docs/phase3/trappist-1-e.md` — temperate aquaplanet (Glidden 2025 DREAMS, Wolf 2017)
- [x] `docs/phase3/trappist-1-f.md` — frozen ocean world (Acuña 2025, Wolf 2017)
- [x] `docs/phase3/trappist-1-g.md` — full snowball + sub-glacial ocean (Bourgeois 2024)
- [x] `docs/phase3/trappist-1-h.md` — Mars-Pluto hybrid frozen rocky (Luger 2017, Gressier 2022)

## Stage 4 — Korean mirrors

H2/H3 structure must match English source by position (build_html.py
will fail loudly otherwise).

- [x] `ko/docs/phase3/trappist-1-b.md`
- [x] `ko/docs/phase3/trappist-1-c.md`
- [x] `ko/docs/phase3/trappist-1-e.md`
- [x] `ko/docs/phase3/trappist-1-f.md`
- [x] `ko/docs/phase3/trappist-1-g.md`
- [x] `ko/docs/phase3/trappist-1-h.md`

## Stage 5 — HTML + report index

- [x] `python3 scripts/phase3/build_html.py trappist-1-{b,c,e,f,g,h}` ×6 — all built clean
- [x] `python3 scripts/pipeline/build_reports_index.py` — 7 P3 reports listed
- [x] `bash scripts/check-mirrors.sh` — 23/23 mirrors OK
- [x] `docs/reports-manifest.json` shows P3 chips for all 7 TRAPPIST-1 planets

## Stage 6 — commit

- [ ] `git add` the 6 .md, 6 ko/.md, 6 _bib/.yaml, 6 .html, docs/reports*.html docs/reports*.json
- [ ] Commit: "Phase 3 synthesis for TRAPPIST-1 b/c/e/f/g/h"

## Stellar synthesis pass — 2026-05-28

Goal: extend the system's Phase 3 to the host star itself. The seven
planets are already done; this pass produces `docs/phase3/trappist-1.md`,
its ko mirror, and the stellar-specific bibliography.

### Stage S1 — stellar bib + canonical-ref injections

- [x] `build_bibliography.py "TRAPPIST-1"` → `_bib/trappist-1.yaml` (323 papers, 202 arXiv)
- [x] Append 21 stellar canonical-ref `injections` to `system.yaml`
  (Van Grootel 2018, Burgasser 2017, Vida 2017, Wheatley 2017,
  Bourrier 2017, Reiners 2018 CARMENES, Reiners & Basri 2010,
  Filippazzo 2015, Roettenbacher & Kane 2017, Luger 2017, Morris 2018a/b,
  Wilson 2021 Mega-MUSCLES, Paudel 2018, Glazier 2020, Howard 2023,
  Gonzales 2019, Garraffo 2017, Ducrot 2020, Gillon 2016, Gillon 2017)
- [x] `inject_papers.py trappist_1` → 21/21 added (after bibcode fixes)
- [x] `score_papers.py` → 51 papers ≥14 (must-read), 159 keep
- [x] `fetch_arxiv_texts.py` → 58 fetched (1 failed: Howard 2023 / 2310.03792)

### Stage S2 — stellar deep-read

Deep-read set (12 papers):
- [x] Van Grootel 2018 (1712.01911) — M, R, L*, Teff
- [x] Burgasser & Mamajek 2017 (1706.02018) — age 7.6 ± 2.2 Gyr + activity table
- [x] Vida 2017 (1703.10130) — K2 P_rot 3.295 d, 42 flares
- [x] Wheatley 2017 (1605.01564) — XMM X-ray L_X / L_XUV
- [x] Bourrier 2017 (1702.07004) — Ly-α detection + XUV
- [x] Roettenbacher & Kane 2017 (1711.02676) — evolving spot pattern, P_rot unreliable
- [x] Morris 2018a (1803.04543) — bright-spot model (R/R*=0.004, T~5300 K)
- [x] Wilson 2021 (2102.11415) — Mega-MUSCLES SED
- [x] Glazier 2020 (2006.14712) — superflare rate 4.2/yr
- [x] Vasilyev 2025 (2508.04793) — flare spectra of magnetic features
- [x] Howard 2025 (2512.04265) — RADYN beam-heating, flare→XUV scaling
- [x] Gonzales 2019 (1909.13859) — reanalysis, intermediate-gravity classification

### Stage S3 — synthesis draft

- [ ] `docs/phase3/trappist-1.md` (stellar Decisions + 8-section structure)
- [ ] VERIFY pass (every row → paper)
- [ ] `ko/docs/phase3/trappist-1.md` (natural prose, block-parity)
- [ ] `python3 scripts/phase3/build_html.py trappist-1` → `.html`
- [ ] `python3 scripts/phase3/check_block_parity.py trappist-1` → pass

### Stage S4 — coordinator commit

Coordinator handles commits (not this subagent).

## Related

- [system-trappist-1 entity pages](../../docs/phase3/trappist-1-e.md) — parent topic this workspace contributes to
