# Checklist — Delta Pavonis Phase 2 (Tier 1, first host under the new contract)

Host: Delta Pavonis (δ Pav, HD 190248, HIP 99240), G8 IV subgiant, 6.1 pc.
Goal: build Phase 2 stellar measurements (currently NONE — Phase 3 sits on Phase 1),
anchored on the Rains 2020 VLTI/PIONIER direct interferometry, then reconcile the
existing (contaminated) Phase 3 markdown. Discipline per
`phase2/curation-data-contract/SPEC.md`.

## Stage 0 — Pre-flight (DONE 2026-05-29)
- [x] Confirm no Phase 2 exists for δ Pav in stellar_props_curated.json
- [x] Confirm existing Phase 3 md uses R=1.22 (Bruntt 2010) / Teff=5604 (Gaia), NOT Rains 2020
- [x] Existing `phase3/delta_pavonis/system.yaml` noted (drives the eventual Phase 3 re-run)
- [x] Candidate sources gathered from the md bibliography (see context-notes)

## Stage 1 — Pre-curation lit search (gate: no false-negative interferometry)
- [ ] Search `"delta Pavonis" interferometry OR angular diameter` — confirm Rains 2020
      is the direct anchor; check for any newer/other interferometric measurement
- [ ] Confirm δ Pav observability: VLTI@Paranal (lat -24°) + SUSI@Narrabri (lat -30°)
      both reach dec -66° — the "too far south for CHARA" claim must NOT become "no interferometry"

## Stage 2 — Bib-first (convergence)
- [ ] Author `docs/phase3/_bib/delta-pavonis.yaml` pinning every candidate source by arxiv_id
- [ ] `fetch_arxiv_texts.py` → cache to `_papers/` (0 failed = arxiv integrity)

## Stage 3 — Phase 2 measurements (DONE — written to db/stellar_props_curated.json)
- [x] mass — Bruntt 2010 asteroseismology 1.07±0.13 (rec); Bensby 2014 1.03 (alt)
- [x] radius — Rains 2020 interferometry 1.197±0.016 (rec); Bruntt 2010 asteroseismic 1.20 (alt)
- [x] teff — Rains 2020 interferometry 5571±48 (rec); Bruntt 2010 spec 5550 (alt)
- [x] luminosity — Rains 2020 bolometric_flux 1.24±0.03 (rec)
- [x] age — DOCUMENTED DIVERGENCE: Holmberg 2009 9.3 (rec, low-activity consistent); Bensby 2014 4.9 (alt)
- [x] metallicity — Gomes da Silva 2021 +0.36±0.02 (rec); Bensby +0.37 / Bruntt +0.33 (alt)
- [x] activity — GdS 2021 log R'HK -5.13 (rec, recency upgrade); Henry 1996 -4.999 (alt); Hünsch 1998 X-ray (alt)
- [x] rotation — OMITTED (only vsini 1.7 km/s; no period; documented in meta_notes, not fabricated)
- [ ] disk: Eiroa 2013 DUNES → disks_curated entry (separate, deferred)
- [x] schema additions: asteroseismology→radius methods (+ SPEC sync); empirical_relation done earlier

## Stage 4 — Validate (DONE)
- [x] schema passes (0 errors); exactly 0-or-1 recommended per category confirmed
- [x] rebuild systems + site (build_systems/validate/build_site); `check.sh` all pass

## Stage 5 — Phase 3 reconciliation (DONE, multi-layer)
- [x] delta-pavonis.md Decisions: radius 1.22→1.197, teff 5604→5571, lum 1.20→1.24,
      mass 1.05→1.07, [Fe/H] +0.33→+0.36, age 7.0→9.3(div), activity -5.10→-5.13, x-ray 26.6→27.3
- [x] intro prose numbers fixed (Teff, age)
- [x] ko mirror updated, block parity 37 OK
- [x] build_html.py + reports index + check-mirrors (only pre-existing tools.md WARN)

## Stage 6 — Gate + commit (DONE)
- [x] check.sh all pass (0 FAIL)
- [x] single commit (DB + systems + data.json + phase3 md/html + ko + bib + schema + SPEC + workdir)

## Extra catches found vs the contaminated template (value of the new discipline)
- radius "1.22 Bruntt" was actually Bruntt's luminosity; real R 1.20, recommended Rains 1.197
- age "7.0±0.5" fabricated midpoint; actual Holmberg 9.3 / Bensby 4.9
- activity "-5.10" → Henry 1996 is -4.999; recency upgrade to GdS 2021 -5.13
- x-ray "non-detection 26.6" → Hünsch 1998 actually DETECTED at log L_X ≈ 27.3

## Discipline (from contract)
One host at a time. Read the `_papers` cache, never live web, for value-check.
No parallel subagent batch. Multi-layer edits in one commit. check.sh after.
