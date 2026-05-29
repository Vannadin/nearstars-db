# Tier 1 — stellar Phase 2 build for the 7 inversion hosts

Goal: remove the "Phase 3 sits on Phase 1" inversion by building measured
Phase 2 stellar layers (8 categories) for each host, one at a time, under the
curation-data-contract discipline. Deliverable = `db/stellar_props_curated.json`
entries (cited + arxiv-pinned + cache-verified) + per-host `_bib/<slug>.yaml`.
Phase 3 md re-synthesis (consuming the new values) is the downstream follow-on.

## Per-host procedure (from SPEC + delta-pavonis template)
1. Research: identify anchor paper per category (bibcode + arxiv_id + value + table loc)
2. Pin to `docs/phase3/_bib/<slug>.yaml`
3. `fetch_arxiv_texts.py` → cache to `_papers/<arxiv_id>.md`
4. VALUE-CHECK every recommended number against the cached text (never live web)
5. Write the 8-category entry + meta_notes (document divergences)
6. `check.sh` gate (schema + mirrors + dead-link + convention)
7. Commit (DB + bib + this working dir in one commit)

## Discipline (non-negotiable)
- One host at a time. Research agent proposes; main thread value-checks against cache.
- 0-or-1 `recommended: true` per category. Forbidden `error_*` prefix.
- Phase 3 inputs must be Phase 2 (no Phase 1 leakage).

## Hosts
- [x] eps Eri   (K2 V) — 8 cats anchored on Baines 2012 interferometry; age divergence documented
- [x] tau Cet   (G8.5 V) — mass/L Teixeira 2009 astero, Teff Korolik 2023 interf; old-isochrone age (inactive); rotation gyro-only (unverified)
- [x] AU Mic    (M1 Ve) — radius divergence (Gallenne 2022 refereed 0.862 vs White unrefereed 0.75); Cristofari/Donati Teff/L, BPMG age 23 Myr, X-ray activity
- [x] HD 69830  (K0 V) — single-anchor Tanner 2015 (CHARA interf R/Teff/L + SME/Y2 mass/age/[Fe/H]); old-age divergence ~6-10 Gyr; no rotation period (7 cats)
- [ ] 61 Vir    (G7 V; solar analog, super-Earths)  ← CURRENT
- [ ] Vega      (A0 V; pole-on rapid rotator, gravity darkening)
- [ ] Fomalhaut (A4 V; young A star, eccentric ring)

## Done
(none yet — delta Pav was host #1, committed 8e9b4b7 before this campaign dir existed)
