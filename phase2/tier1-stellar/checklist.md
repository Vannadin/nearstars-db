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
- [x] 61 Vir    (G7 V) — single-anchor von Braun 2014 (CHARA interf R/Teff/L + Y2 mass/age); rotation 29 d (Baliunas 1996); old-age divergence ~6-9 Gyr (8 cats)
- [x] Vega      (A0 V) — gravity-darkened Monnier 2012 (R pol/eq, mean Teff 9360, L 47.2, age 700 Myr); P 0.71 d; NO log R'HK (A star); age divergence 455-700 Myr (7 cats)
- [x] Fomalhaut (A4 V) — single-anchor Mamajek 2012 (R/Teff/L from Absil theta_LD + age 440 Myr); NO log R'HK (A star); v sin i only, no period (6 cats)

## DONE — all 7 Tier 1 inversion hosts complete (2026-05-30)
Plus delta Pav (host #1, committed 8e9b4b7 before this campaign dir existed) = 8 total.
Commits: eps-eri 78bff2a, tau-cet 5ab9bff, au-mic 82a6167, hd-69830 b46d98d,
61-vir 23c24a4, vega d757cf7, fomalhaut (this commit).
Every host: arxiv-pinned bib, cache/VizieR value-check, schema gate, systems
rebuilt (date-churn reverted), one commit. The Phase-3-on-Phase-1 inversion is
resolved for all stellar hosts.

## Remaining downstream (NOT Tier 1)
- Phase 3 md re-synthesis consuming the new measured values (the 7 hosts' Phase 3
  narratives still reflect pre-Phase-2 inputs where they exist).
- Disk Mie/grain-size color synthesis (separate follow-on from the disk detour).
