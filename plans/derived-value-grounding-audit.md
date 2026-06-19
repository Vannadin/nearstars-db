<!-- 도출값 논문 근거화 규칙의 소급 전수 감사 결과 (2026-06-20) — 수정 백로그 -->
# Derived-Value Grounding Audit (retroactive, 2026-06-20)

Full-corpus audit applying the new derived-value method-grounding rule
(`phase2/curation-data-contract/SPEC.md` "Derived astrophysical values") to all
existing work. Method: 3 method-level subagents (color / stellar-physics /
orbital-structural) + 4 exhaustive per-body coverage subagents (giant B-fields,
rocky B-fields, stellar-wind fields, disk colors).

**Headline.** The discipline + machinery are largely sound — textbook closed-forms
are correctly exempt, most synthesised values cite a real relation or are honestly
flagged low-confidence, and no value was *fabricated*. The real gaps cluster in
**gas-giant/substellar magnetic fields** and **debris-disk blend colors**, plus a
distinct **phantom-citation** failure mode. Stellar-wind fields are not yet
cfg-emitted (Kerbalism writer deferred), so those are provenance-only.

---

## The phantom-citation pattern (the most important systemic finding)

Some derived values name a real paper that is **absent from the `_papers/` cache
and the bib YAMLs** — laundering a back-of-envelope guess as grounded. This is
*worse* than an honest "no citation, low-confidence" label, and it also violates
the convergence rule (cite by `bibcode` + `arxiv_id` + cache). Confirmed cases:
**Yadav & Thorngren 2017** (no arXiv/bibcode, already flagged uncacheable by the
2026-06-03 audit) cited by au-mic-b/c/e; **Reiners & Christensen 2010** cited by
eps-eri-b and au-mic-d but not in this repo's cache. Fix = cache the real paper, or
rewrite the basis honestly.

---

## Tier 1 — real, cfg-emitting, fix needed

### 1a. Gas-giant / substellar magnetic field + dipole (gates aurora / radiation belts)

| Body | Value | Problem | Verdict |
|---|---|---|---|
| ε Eri b | 400 µT, dipole 13200× | linear-mass "scaled jovian"; cites Reiners&Christensen 2010 **not in cache** + physics contradicts (real dynamo scaling is energy-flux, not linear-mass) | AD-HOC + phantom-cite |
| GJ 896 A b | 900 µT | "scaled jovian, ~2× Jupiter" — **no citation** | AD-HOC |
| ε Ind A b | 1000 µT | "~2× Jupiter by mass/convection" — no citation (self-labels "aesthetic, no measurement" → partially mitigated) | AD-HOC (flagged) |
| AU Mic b | 100 µT | cites **Yadav & Thorngren 2017** (phantom — not in cache) | phantom-cite |
| AU Mic c | 50 µT | same phantom Yadav & Thorngren 2017 | phantom-cite |
| AU Mic d | 5 µT | cites **Reiners & Christensen 2010** (phantom — not in this report's biblio/cache) | phantom-cite |
| AU Mic e | 30 µT | same phantom Yadav & Thorngren 2017 | phantom-cite |

**Fix:** ground on a real, cached dynamo scaling — **Christensen, Holzwarth & Reiners
2009** (energy-flux scaling, `2009Natur.457..167C`) or Reiners & Christensen 2010
(cache it properly) — recomputing field from energy flux, NOT linear mass; OR demote
to an honest low-confidence analog (the compliant pattern, below). Note the dipole
moments are *internally* consistent (ε Eri 13200 = 0.66×20000), so it's the method,
not arithmetic.

**Already compliant (honest analog, no false citation — the pattern to copy):**
α Cen A b / Polyphemus (500 µT, "Saturn-analog, no measurement", low), HD 69830 b
(Neptune-analog, low). **But HD 69830 c/d** mark confidence medium/high on an uncited
Neptune-analog ratio — should be `low` (Tier 2).

### 1b. Debris-disk blend optical constants

`ice_sil` and `sil_org` in `scripts/phase3/disk_color_mie.py` are **invented** — exact
linear n,k averages of their endpoints (verified), not an effective-medium theory
(Maxwell-Garnett / Bruggeman) and not from any optical-constants paper. They drive two
emitted (low-conf-flagged) tints: **eps Eri cold ring** (`#fffcfc`) and **tau Cet broad
belt** (`#ffe4bd`). `ice_sil` is also the Fomalhaut-grey validation anchor → slightly
circular validation. The five single materials (astrosil/carbon/ice/olivine/tholin) ARE
grounded (Draine 2003, Warren & Brandt 2008, Jäger 2003, Khare 1984, Rouleau & Martin
1991), literature-consistent. **Fix:** apply Maxwell-Garnett mixing to ε=(n+ik)² for the
blends, or pick a single cited material, or flag the blend n,k as an explicit assumption.

---

## Tier 2 — mitigated / honest, polish at emit time

- **Flare boost on `stellar_radiation_surface`** (Proxima ~5 over quiescent ~0.3; Barnard
  ~0.1 over ~0.03): the boost *magnitude* cites no flare-energy→dose scaling. Mitigated —
  quiescent-only alternative flagged inline, pre-declared low–medium. **Not cfg-emitted
  yet.** Fix: pin an SEP-fluence / flare-FFD→dose relation, or demote headline to quiescent.
- **`astrosphere_standoff` v_wind = 400 km/s** assumption + LIC-density cancellation: documented
  at the spec/workspace level but **not restated at point-of-use**; "Wood" attribution unpinned.
  Fix: one line per host + pin the wind-speed source.
- **HD 69830 c/d B-field confidence overstated** (medium/high → should be low for an uncited analog).
- **Barnard b/c/d/e dipoles**: uncited Mercury-analog ordinal guesses, flagged low, none drive
  Kerbalism (belts off). Add an RM22/Zuluaga anchor or an explicit "analogy, not modeled" note.
- **Disk `rho = 2.5 g/cc` and `q = 3.5`** hardcoded uncited (load-bearing for a_min); q=3.5 is the
  standard Dohnanyi 1969 value — cite it; flag rho.

---

## Tier 3 — citation hygiene

- tau-cet-e/f label "RM22 (Reiners-Christensen)" — conflates two distinct papers (RM22 =
  Rodríguez-Mozos & Moya 2022, the value's real source; Reiners & Christensen 2010 = a
  separate rotation-dynamo law). De-conflate the names.
- `disk_color_mie.py` comment "50/50 mass-ish blends" overstates rigor (they're unweighted
  linear n,k averages).
- Barnard `surface_radiation_dose` cites Atri 2020 / France 2020 as "context-cite, not in
  cache" — honest, but uncached.

---

## Confirmed grounded / exempt (the bulk — no action)

- **Color engine:** Saha-Boltzmann LTE (Cristoforetti 2010 + NIST), CIE→sRGB (Wyman 2013),
  Mie algorithm (Bohren & Huffman, validated vs AU Mic blue / Fomalhaut grey), molecular
  bands (Huber & Herzberg + per-species sources). Chromophore catalog (textbook, veto-gated).
- **Rocky-planet B-fields:** RM22 (Rodríguez-Mozos & Moya 2022, `2203.01065`, cached) carries
  the TRAPPIST-1 family; proxima-b (Zuluaga 2018), yz-cet-b (Trigilio 2023 measurement),
  Wang 2025, Garraffo, Driscoll & Olson — all grounded or honestly low-conf.
- **Closed-forms (exempt):** T_eq / insolation / surface gravity / scale height (recompute-gate
  enforced), Roche, Hill, Kepler, angular size, Planck, blowout radius, x=2πa/λ.
- **Greenhouse temps:** from cited GCMs (Boutle 2017, Del Genio 2019); Venus benchmark grounds
  the "T_eq is a lower bound" guardrail.
- **aspect_ratio** (Boley 2012 / Daley 2019), **J2** (Radau–Darwin, Helled+2011, calibration-
  verified), **C22 = 0.3·J2** (hydrostatic, Galilean-verified).
- **Stability-sim selections** (Barnard, α Cen, moons): sound integrator policy (TRACE Lu+2024),
  Solar-System self-validation, literature cross-checks (GH2024, Basant 2025, Domingos+2006).
- **Stellar-wind inputs** (mass-loss Wood, L_X Wargelin/France, rotation/activity) — Phase 2
  measured + cited.
- **Phase 4 art-direction** (Pandora +70 K greenhouse, Hades e, synthetic-noise e≲0.05): flagged
  art-direction / documented-limitation, not yet emitting.

---

## Recommended fix order

1. **Giant/substellar B-fields (1a)** — highest impact (emit + gate aurora/belts) and the
   phantom-citation core. Ground on Christensen 2009 / Reiners 2010 (cached) per body, or demote
   to honest analog. ~7 bodies + cache the dynamo paper.
2. **Disk blends (1b)** — 2 emitted tints; Maxwell-Garnett or single-material or flag.
3. **Tier 2 polish** — flare-boost grounding, v_wind point-of-use, HD 69830 c/d confidence,
   Barnard dipole anchors, Dohnanyi/rho cites.
4. **Tier 3 hygiene** — label/comment cleanups.

Each fix follows the J2 template: read the method paper (cache it), recompute, record with
citation + assumption + uncertainty.
