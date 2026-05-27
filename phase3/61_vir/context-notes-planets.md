# 61 Virginis planets b/c/d Phase 3 — context notes

Append-only decision log. Started 2026-05-27. Companion to
`context-notes.md` which holds the host-star synthesis trail.

## Source inventory (Phase 2 from DB)

DB `db/systems/61_vir.json` `planets` array carries Vogt 2010 for all
three:

- **b**: P=4.215 d, a=0.050201 AU, e=0.12, Msini=5.1±0.5 M⊕, ω=105°.
  Tperi BJD 2455200.597 ± 0.05. Tranmid only — does not transit.
- **c**: P=38.021 d, a=0.2175 AU, e=0.14, Msini=18.2±1.1 M⊕, ω=341°.
- **d**: P=123.01 d, a=0.476 AU, e=0.35, Msini=22.9±2.6 M⊕, ω=314°.

`radius_rearth` is **literature placeholder** (2.11, 4.46, 5.11 R⊕)
copied from a mass–radius estimate, not measured. Inclination is null
(RV-only). `pl_controv_flag = 0` for all.

## Classification reasoning (Step 9.0 pre-write)

### b — hot super-Earth

**Mass.** 5.1 M⊕ Msini. True mass ≥ 5.1 M⊕; for the Vogt 2010 system
inclination posterior (consistent with edge-on) the most probable true
mass is in 5–7 M⊕.

**Insolation.** L=0.82 L☉, a=0.050 AU → S = 0.82 / 0.050² =
328 S⊕. T_eq (A=0) = 278 × (S)^0.25 = 278 × 4.26 ≈ 1184 K
gives way too hot — re-derive: T_eq = T★ × (R★/2a)^0.5 = 5552 ×
(0.963 R☉ / (2×0.050 AU × 215 R☉/AU))^0.5 = 5552 × (0.963/21.5)^0.5
= 5552 × 0.2117 = 1175 K. Better: T_eq(A=0)
= [(1-A) L / (16πσa²)]^0.25.
L=0.82 L☉=3.14e26 W. a=0.050 AU=7.48e9 m. a²=5.6e19.
16πσa² = 16π × 5.67e-8 × 5.6e19 = 1.6e14.
(1·3.14e26 / 1.6e14)^0.25 = (1.96e12)^0.25 = 1183 K. OK so T_eq(A=0) ≈
1180 K. With A=0.3, T_eq ≈ 1080 K. **Very hot.**

**Tidal lock.** Vinson 2017 / Makarov 2018 timescale for 5 M⊕ at 0.05
AU around 0.94 M☉ G-star is ~10⁵–10⁶ yr — orders of magnitude shorter
than 6 Gyr system age. **Strongly locked, 1:1.**

**Atmosphere.** Initial H/He envelope photoevaporated long ago (Owen
2017 / Lopez 2017 scaling: even a 5 M⊕ core at 0.05 AU around a Sun
loses any H/He on <100 Myr). Secondary atmosphere depends on
outgassing balance. T_eq 1080 K is above silicate melting on the
dayside → magma-ocean dayside likely. Steam atmosphere from ongoing
volatile outgassing is possible if any H₂O survived initial loss.
Reference: Léger 2009 CoRoT-7b template (very similar planet:
4.8 M⊕, 0.017 AU, T_eq ~1800 K, magma ocean dayside).

**Scenario for cfg.** Hot tidally-locked super-Earth, basaltic/magma
surface, partial-melt dayside, possibly thin steam exosphere. Most
fields tie-break (no transit, no JWST). Interesting-first picks magma
glow visual.

**Per-row classification:**
- Orbital (P, a, e, ω) → canonical-aligned (Vogt 2010 direct)
- Mass → canonical-aligned (Vogt 2010 Msini = lower bound)
- Radius → tie-break (no transit; mass-radius scaling Zeng 2016 gives
  R = 1.5–2.0 R⊕ for rocky 5–7 M⊕)
- Tidal-lock → canonical-aligned (Vinson 2017 timescale)
- T_eq → canonical-aligned (derived; standard formula)
- Surface temp dayside → tie-break (magma ocean assumption)
- Surface tint primary/accent → tie-break (interesting-first
  lava/magma palette)
- Atmosphere present → tie-break (vestigial steam exosphere)
- Atmosphere pressure → tie-break (< 0.01 bar, below visible)
- All visual styling fields → tie-break

### c — warm sub-Neptune

**Mass.** 18.2 M⊕ Msini. With ~14× Earth this is solidly in the
sub-Neptune / mini-Neptune bin.

**Radius (no transit).** Mass-radius for 18 M⊕ has two branches:
- Rocky/iron: R ~ 2.0 R⊕ (Zeng 2016 pure rocky scaling)
- H/He envelope (1–10% mass): R ~ 3.5–6 R⊕ (Lopez 2014, Howe 2014)

For a 38 d period at 0.22 AU around a G-star, the atmospheric
mass-loss rate is moderate. Owen 2017 scaling: at L = 0.82 L☉,
a=0.22 AU, S_XUV ~ 1× Earth's modern. Over 6 Gyr a 1-3% H/He envelope
is retained for 18 M⊕ cores (cosmic shoreline well outside the loss
regime). **Canonical reading: H/He envelope, R ≈ 4–5 R⊕.**

**Insolation.** S = 0.82 / 0.22² = 17 S⊕. T_eq(A=0.3) = 478 K.
T_eq(A=0) = 525 K. **Warm sub-Neptune category** (HD 97658 b, 55 Cnc e
adjacent but slightly cooler).

**Atmosphere.** H/He primary atmosphere with H₂O, CH₄, CO₂, NH₃
condensates. Hazes from photochemistry plausible. Clouds: at 480 K,
H₂O clouds form in cool upper atmosphere; KCl and Na₂S clouds at
deeper layers. Hazy sub-Neptune visual archetype (GJ 1214b parallel).

**Per-row classification:**
- Orbital → canonical-aligned (Vogt 2010)
- Mass → canonical-aligned (Vogt 2010)
- Radius → tie-break (mass-radius scaling; no transit; pick ~4.5 R⊕
  H/He envelope as canonical sub-Neptune reading)
- Tidal lock → tie-break (Henning & Hurford 2014: 38 d period at 0.22
  AU has tidal lock timescale ~ Gyr but eccentricity 0.14 sustains
  pseudo-synchronous; cfg picks pseudo-synchronous or weak lock)
- Atmosphere composition → canonical-aligned (H/He primary)
- Cloud tint / morphology → tie-break (interesting-first; pick
  cyan/teal hazy sub-Neptune)

### d — cooler eccentric sub-Neptune

**Mass.** 22.9 M⊕ Msini. Larger than c.

**Eccentricity.** e = 0.35 is high — significant orbital variation:
- a=0.476 AU, q (peri) = a(1-e) = 0.309 AU, Q (apo) = a(1+e) = 0.643 AU
- S at peri = 0.82 / 0.309² = 8.6 S⊕; T_eq(A=0.3) ≈ 410 K
- S at apo = 0.82 / 0.643² = 1.98 S⊕; T_eq(A=0.3) ≈ 270 K
- Mean S = 0.82 / 0.476² × (1 + e²/2)^0 ≈ 3.6 S⊕ (time-averaged
  proper formula); T_eq(A=0.3) ≈ 330 K

This is a **strongly seasonal** sub-Neptune — apo near Earth's
insolation, peri near 8× — straddling the inner edge of the
conventional HZ for a sub-Neptune envelope.

**Radius (no transit).** Mass-radius for 23 M⊕ with H/He envelope:
4.5–6 R⊕ (Howe 2014). Pure-rocky bound: R ~ 2.2 R⊕. Adopt 5.0 R⊕
canonical for H/He envelope reading.

**Atmosphere.** H/He primary at 23 M⊕ at 0.48 AU around a 0.82 L☉
G-star is solidly retained over 6 Gyr (Owen 2017). H₂O cloud condensation
is possible at apo phase; clouds rise/fall through eccentric cycle.

**Water-world variant.** Alternative: water-rich envelope (Madhusudhan
2021 "Hycean" — high-pressure water envelope under H₂ atmosphere).
For 23 M⊕ at d's insolation this is observationally indistinguishable
from H/He but produces a different visual (deeper-blue, less hazy).
Document as cfg variant in Open items; cfg primary picks H/He.

**Tidal lock.** 124 d period — tidal lock timescale >> system age. Not
locked. Free rotation, expect Saturn/Neptune-analog rotation rate
(~10–16 h).

**Per-row classification:**
- Orbital → canonical-aligned (Vogt 2010)
- Mass → canonical-aligned (Vogt 2010)
- Radius → tie-break (mass-radius scaling)
- Tidal lock → canonical-aligned (free rotation; timescale >> age)
- Atmosphere → canonical-aligned (H/He primary at 23 M⊕)
- Eccentric seasons → canonical-aligned (orbital geometry)
- Hycean variant → documented in Open items, cfg picks H/He as primary
  reading (more conventional sub-Neptune visual; Hycean is a documented
  alternative scenario, not a divergence — observationally
  indistinguishable, so cfg pick by aesthetic preference for the more
  common interpretation)
- Cloud morphology → tie-break (eccentric-driven dynamics; pick banded
  Saturn/Neptune-analog visual with seasonal cloud-deck shifts)

## Decision summary per planet

### b
- 27 cfg picks: ~7 canonical-aligned (Orbital + Mass + tidal-lock +
  T_eq derivations), ~20 tie-break (every visual + atmosphere + surface
  field is interesting-first within the wide window).
- No documented divergences.
- No `## Canonical alternatives` section.

### c
- 25 cfg picks: ~10 canonical-aligned (Orbital + Mass + H/He envelope
  + insolation), ~15 tie-break (radius, clouds, tint, hazes).
- No documented divergences.
- No `## Canonical alternatives` section.

### d
- 28 cfg picks: ~12 canonical-aligned (Orbital + Mass + H/He envelope
  + eccentric seasons + free rotation), ~16 tie-break (radius, clouds,
  visual hex).
- No documented divergences. Hycean variant captured in Open items as
  a cfg variant, not a divergence (observationally degenerate).
- No `## Canonical alternatives` section.

## Bibliography plan

### Read (visual-informative, all three planets share most refs)

- Vogt et al. 2010 — discovery paper, three RV planets + stellar
  parameters
- Zeng et al. 2016 — mass-radius relationships for low-mass planets
- Lopez & Fortney 2014 — H/He envelope mass-radius for sub-Neptunes
- Howe et al. 2014 — sub-Neptune mass-radius diversity
- Owen & Wu 2017 — photoevaporation valley physics (drives b's
  airless / c+d retained-envelope distinction)
- Léger 2009 — CoRoT-7b magma-ocean precursor (b template)
- Madhusudhan et al. 2021 — Hycean worlds (d alternative scenario)
- Henning & Hurford 2014 — sub-Neptune tidal heating + pseudo-sync
- Kreidberg et al. 2014 — GJ 1214b clouds/hazes (c/d sub-Neptune
  visual template)
- Wyatt et al. 2012 — host star debris ring (cited briefly)

### Read (context / methodology)

- Mamajek & Hillenbrand 2008 — host star age (inherits stellar synth)
- Pavlenko et al. 2012 — host star spectroscopy (inherits)

### Not read

- ~25 conference abstracts, dynamical-stability follow-ups, transit
  search non-detections (no direct visual content)

## Open items snapshot per planet

### b
- True mass / radius from direct imaging or astrometric follow-up
- Phase curve / secondary eclipse if a future MIRI proposal targets
- Surface mineralogy from JWST MIRI (none scheduled)

### c
- True mass / radius from direct imaging or transit follow-up
- HZ-edge climate modeling for the H/He envelope variant
- Cloud composition from future direct-imaging reflectance spectra

### d
- True mass / radius from direct imaging
- Eccentricity-driven climate model (GCM with seasonal forcing)
- Hycean variant as cfg alternative
- Sub-Neptune vs. water-world degeneracy resolution
