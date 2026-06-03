# Checklist — beyond-50ly DB additions (PSR J0108−1431 + J1407/V1400 Cen)

User decisions (2026-06-03):
- **Full pipeline**: curated DB → build_systems → Phase 3 reports + HTML (en/ko),
  treated like a catalog system but FLAGGED `beyond-50ly / Kopernicus-unplaced`.
- **Schema extension (proper)**: add pulsar/compact-object fields + circumplanetary
  ring representation to schema.py (shared structure change → must pass check.sh).
- Both far beyond the deliberate 50ly cap (V1400 Cen 451 ly, PSR J0108 ~685 ly) —
  intentional exception, NOT KSP-implementation targets.
- J1407b = tentative/disputed single-eclipse object → mark tentative (variety policy
  allows; rings are published Kenworthy & Mamajek 2015, not fabricated).

Phase 2 dossiers already gathered:
- `phase3/_survey/psr-j0108-1431/phase2-dossier.md`
- `phase3/_survey/j1407/phase2-dossier.md`

## Stage 0 — Map the canonical procedure  (delegated Explore)
- [ ] Exact add-star workflow: which source files, what order, which tooling
      (apply_phase2.py, _naming.py, build_systems, build_site), target_list location
- [ ] schema.py structure (stellar / planet / disk field sets) → what to extend
- [ ] A recent real example (eps Ind A / 40 Eri) curated entry format
- [ ] How "tentative/disputed" + "beyond-range" flags are represented today (if any)

## Stage 1 — Schema extension
- [ ] Compact-object / pulsar fields (P_spin, Pdot, B_surf, char_age, X-ray, etc.)
- [ ] Circumplanetary ring representation (ring on a companion, not circumstellar disk)
- [ ] `beyond_implementation_range` / `tentative` flags as needed
- [ ] schema validates; check.sh schema gate green

## Stage 2 — Curate PSR J0108−1431  (compact object, no planets)
- [ ] Curated star entry (canonical M/R, spin, B, distance, X-ray; planets = none)
- [ ] target_list + naming
- [ ] build_systems → db/systems entry; build_site → data.json

## Stage 3 — Curate V1400 Cen / J1407
- [ ] Host star (K5 PMS) curated entry
- [ ] Companion J1407b (planet, mass range, tentative)
- [ ] Circumplanetary ring (new schema feature)
- [ ] build_systems → build_site

## Stage 4 — Phase 3 reports (en + ko + HTML)
- [ ] psr-j0108-1431 (compact-object synthesis; visual = pulsar/X-ray/magnetosphere)
- [ ] v1400-cen / j1407 (host + ringed companion synthesis; tentative divergence)
- [ ] build_html, reports index, check-mirrors

## Stage 5 — Verify + commit
- [ ] check.sh gates, parity, mirror
- [ ] Semantic commits (VaNnadin identity)
