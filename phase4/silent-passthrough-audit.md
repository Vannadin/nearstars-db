<!-- 전 로스터 Phase 4 silent-passthrough 감사 — 측정값 없이 엔진 기본값으로 조용히 통과된 (body×axis) 셀 추적 (2026-06-26) -->
# Phase 4 — Silent-Passthrough Audit (full roster, 2026-06-26)

Companion to `phase4-coverage-audit.md` (α Cen only). This sweeps the **whole confirmed
roster** for cells the owner never explicitly chose. Trigger: the obliquity question —
which turned out to be one instance of a broader pattern.

## The pattern — "free-emit geometry" defaults

The real gap is **not** "every untouched axis." Most untouched axes carry a measured
Phase 2 value that emits unchanged — that is legitimate `passthrough` per SPEC §0. The
genuine *silent* gap is the family of axes that have **no measurement** and silently took
an **engine default**:

- `bulk.obliquity` → 0° (the original question)
- `bulk.spin_axis_orientation` → orbit-normal / arbitrary pole
- `orbit.inclination_deg` → 0°/90° (non-transiting RV planets: truly unconstrained)
- `orbit.longitude_ascending_node` (Ω) / `argument_periapsis` (ω) / `mean_anomaly` → null/arbitrary
- `bulk.rotation_period` → unforced free-rotator value (no measurement)
- `orbit.eccentricity` → **e = 0** (and the Kopernicus eccentricity-curve divide-by-zero trap)

For **tidal-locked** bodies most of these are trivial (obliquity ≈ 0, spin = orbit normal,
rotation = orbital period) — but the policy (silent passthrough 금지) still wants them
**explicitly confirmed**, not assumed. For **free rotators** they are real owner choices.

## Status by system

Legend: ✅ clean (gated/walked) · ⚠️ partial · ❌ no board · 🎯 = genuine owner decision owed

| system | board | verdict | genuine gaps |
|---|---|---|---|
| α Centauri (+ Proxima) | ✅ full | ✅ clean | none (Silent 0; only emit-time Ω/ω/M phase-consistency + A/B wind split, both technical) |
| 40 Eridani | ✅ full | ✅ resolved (2026-06-26) | obliquity/spin filled: b 30°(film), c ≈0(locked), d 4.7d/17°(free); stars A/C figure OMIT-confirmed. **Also fixed a real bug**: d's CO₂ dry-ice/SO₂ frost-buffer (G4) retracted — impossible at 268K mean (frost point ~148K/~130K); d → bare cratered rock + escaping thin envelope |
| Tau Ceti | ⚠️ skeletal (5 rows) | ❌ big gaps | **debris disk (14 Phase-3 decisions, 0 board rows)** 🎯; f/g/h full geometry set 🎯 |
| Barnard | ⚠️ skeletal (2 rows) | ❌ big gaps | star fundamentals (all measured → passthrough-confirm); d/b/c/e geometry defaults 🎯 |
| Fomalhaut | ✅ full | ✅ resolved (2026-06-26) | board created: star (measured passthrough + visual oblateness 2.1% emit + fossil-field nuance documented) + 3-belt disk (warm/intermediate/cold, all emit; colors re-run via current Mie methodology; cold measured grey kept) + gameplay/satellites. Companions B/C = backlog. 8 axes gated |
| TRAPPIST-1 | ❌ none | ❌ no board | **e = 0 → synthetic-e decision + Kopernicus div-by-zero risk** 🎯; 7× obliquity/spin (locked, confirm); appearance per planet 🎯 |
| Luhman 16 | ❌ none | ❌ no board | **P_rot A (tentative, Apai 2021)** + **age (unverified 1.5 Gyr)** keep/override 🎯; spin_axis |

## Genuine decision backlog (filtered — not raw axis count)

The Tau Ceti+Barnard sweep counted ~380 untouched axes; **most are legitimate passthrough**
(measured Phase 2 stellar/planet values). The actionable set is much smaller:

### A. Free-rotator obliquity / spin (real art choices) 🎯
- 40 Eri b (Erid, free, 5.1 h), 40 Eri d
- Tau Ceti f (P 636 d, not locked), g, h
- (αCen Cassandra/Chaos/Polyphemus, Proxima c already done — the template)

### B. Tidal-locked geometry (trivial — batch-confirm as passthrough)
- 40 Eri c; Tau Ceti planets if locked; Barnard d/b/c/e (close-in → locked); TRAPPIST-1 b–h
- obliquity ≈ 0, spin = orbit normal, rotation = orbital period. One confirmation row each.

### C. Non-transiting RV geometry (free-emit, confirm not derive)
- Barnard d/b/c/e and Tau Ceti f/g/h: inclination/Ω/ω/M unconstrained → free emit, but record the decision.

### D. Eccentricity / synthetic noise
- TRAPPIST-1 b–h: **e = 0** → decide seeded synthetic-e (per `synthetic-orbit-noise.md`) vs keep 0.
  ⚠️ Kopernicus `temperatureEccentricityBiasCurve` divides by (ApR−PeR): e≈0 silently kills the
  atmosphere. Either emit e ≳ 0.02 or suppress the curve. Same trap noted for α Cen.

### E. System-identity features with Phase 3 but no board row
- **Tau Ceti cold debris disk** (6–55 AU, MacGregor 2016; 14 Phase-3 disk decisions incl.
  tint #ffe2bb, mass 1.2 M⊕). The headline feature of the system, entirely un-boarded. 🎯
- Fomalhaut 3-belt disk (appearance/composition/visibility art choices). 🎯

### F. Data-quality flags needing explicit keep/override 🎯
- Luhman 16 A `rotation_period` 0.2892 d — Apai 2021 "we speculate" (Gillon 2013 negative).
- Luhman 16 A/B `age` 1.5 Gyr — unverified.

### G. Whole boards to create
- `phase4/fomalhaut.yaml`, `phase4/trappist_1.yaml`, `phase4/luhman_16.yaml`.

## What is NOT a gap (reassurance)
- α Cen + Proxima: fully walked, Silent 0.
- All measured Phase 2 stellar values (Barnard B-field 430 G, Tau Ceti spin i 7°, masses,
  radii, Teff, ages, activity) → emit unchanged; passthrough is correct, only needs a one-line
  confirm row if we want strict policy compliance.
- Stellar `obliquity`/`j2`/`spin_axis` (40 Eri A/C, Fomalhaut, Barnard, Luhman): figure ledger
  already decided OMIT for stars/dense BDs — confirm, don't re-derive.

## Related
- `phase4/phase4-coverage-audit.md` — α Cen deep audit (the template)
- `phase4/facet-checklist.md` — α Cen + Proxima per-(body×axis) tracker
- `phase4/synthetic-orbit-noise.md` — the e=0 / obliquity de-perfecting policy
- `phase4/figure/values.md` — per-body J2/C̄₂₂ ledger (roster-complete)
