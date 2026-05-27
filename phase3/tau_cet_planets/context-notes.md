# τ Cet f / g / h — context notes

Three Feng 2017 RV-only candidates around metal-poor G8V τ Cet. All
flagged controversial in NEA. No transit, no direct imaging, no JWST
follow-up. Synthesis is more cfg-conservative than for TRAPPIST-1.

## User-input discrepancy (h)

User request stated tau Cet h: P=4562 d, M sin i ~4.29 M⊕, a ~5 AU
(near asteroid-analog belt inner edge). DB authoritative values:
P=49.41 d, M sin i = 1.83 M⊕, a = 0.243 AU. The DB values are what
Feng 2017 §3 publishes as planet h. The user's 4562 d / 5 AU
candidate is plausibly a Feng 2017 §6 "additional candidate" or a
Feng 2018 candidate (a separate paper) that NS DB has not ingested.
DB is authoritative for Phase 3; the discrepancy is logged as an
open item under tau-cet-h.md, and the synthesis describes the
P=49.41 d / 0.243 AU planet that the DB names h.

Practical effect on classification:
- h is *inner* (0.24 AU, hot), not outer.
- The 1.33 AU f is the actual cold edge of HZ.
- g at 0.13 AU is hottest.

## Common host context (from docs/phase3/tau-cet.md)

- Spectral G8V, M = 0.783 M☉, R = 0.793 R☉, L = 0.457 L☉,
  Teff = 5344 K, [Fe/H] = -0.55 (metal-poor), age 7 ± 1.5 Gyr.
- log R'HK = -4.95 (exceptionally inactive), log L_X ≤ 26.5,
  no detected flares, basal FUV. Atmospheric escape is thermal Jeans
  only — no XUV-driven hydrodynamic loss at any of f/g/h.
- Debris disk inner edge ~6 AU — all three planets well inside.
- Metal-poor host → less heavy-metal opacity in any thin atmosphere
  the planets retain; CO₂/N₂ secondary atmospheres lose some of their
  warming efficiency vs. solar-metallicity hosts at the same insolation
  (Carone 2018-type calculation). Flag in atmosphere synthesis.

## Insolation and equilibrium temperature

Using L_bol = 0.457 L☉:

| Planet | a (AU) | S/S⊕ = L/a² | Teq (A=0) | Teq (A=0.3) |
|---|---|---|---|---|
| g | 0.133 | 25.85 | 627 K | 574 K |
| h | 0.243 | 7.74  | 466 K | 426 K |
| f | 1.334 | 0.257 | 199 K | 182 K |

(Earth Teq formula: Teq = 278 × (L/a²)^(1/4) for A=0, ×(1-A)^(1/4) for albedo A; a in AU, L in L☉. Earth Teq A=0 = 278×1=278 K; here Teq_g_A0 = 278 × 25.85^0.25 = 278 × 2.255 = 627 K, etc.)

Per planet:
- **g**: 25.85 S⊕, Teq 627 K — well inside Mercury-like / Venus-hot.
  Likely tidally heated and possibly molten dayside.
- **h**: 7.74 S⊕, Teq 466 K — Venus-like insolation neighborhood
  but at the cooler edge. Runaway-greenhouse / Venus-analog
  scenario relevant.
- **f**: 0.257 S⊕, Teq 199 K — beyond outer edge of conservative HZ
  (Kopparapu 2014 gives 0.36 S⊕ as maximum-greenhouse limit for G8V).
  Snowball or thin-atmosphere frozen body.

Note: user said f is "cold edge of HZ" — at 0.26 S⊕, f is actually
beyond Kopparapu maximum-greenhouse outer edge, NOT at the cold edge
*of* HZ. f is a snowball candidate, not a habitable candidate. Phase 3
will present it as such.

## Per-planet row classifications

### τ Cet f (P=636 d, a=1.334 AU, Msini=3.93 M⊕, e=0.16)

**Mass note.** Msini = 3.93 ± 1.05 M⊕. True mass M = Msini / sin(i),
unknown i. Statistical expectation E[1/sin(i)] = π/2 for uniform i,
so most-probable true mass ~5.0 M⊕. For radius we adopt Feng 2017's
catalogued 1.81 R⊕ (DB raw.radius_rearth = 1.81) — this is the
"radius from M-R relation" assumption Feng 2017 uses for the catalog.

**Density.** With M = 3.93 M⊕ and R = 1.81 R⊕: ρ = 3.93 × 5.97e24 kg /
(4/3 × π × (1.81 × 6.371e6 m)³) = 3.66 g/cc — sub-Earth, suggesting
volatile-rich envelope. If sin(i)~0.7 → M~5.6, ρ~5.2 g/cc, more
Earth-like.

**Classification (~25 rows total).**
- Orbital (6): all canonical-aligned from Feng 2017 DB curated.
- Physical (5): mass / radius canonical (DB); density derived;
  insolation derived; Teq derived. All canonical-aligned (medium
  confidence due to RV-only, sin i unknown).
- Atmosphere (5): no observation, theoretical only. atmosphere_present
  + composition + pressure: medium confidence per outer-HZ snowball
  outgassing literature (Wordsworth 2015, Pierrehumbert 2011).
  Scale height derived. Tint hex low (tie-break, interesting-first).
- Surface (5): no observation. Tints, morphology all low (tie-break).
- Sky (2): canonical-aligned derived.

Counts: ~14 canonical-aligned, ~9 tie-break, 0 documented-divergence.

### τ Cet g (P=20 d, a=0.133 AU, Msini=1.75 M⊕, e=0.06)

**Mass note.** Msini = 1.75 ± 0.25 M⊕. Most-probable true mass
~2.2 M⊕. Radius from M-R relation (DB raw.radius_rearth = 1.18).

**Density.** M = 1.75 M⊕, R = 1.18 R⊕: ρ = 1.75 × 5.97e24 /
(4/3 × π × (1.18 × 6.371e6)³) = 5.84 g/cc — Earth-like, rocky.

**Scenario.** 25.85 S⊕, Teq A=0 627 K, Teq A=0.3 574 K. Tidally locked
at P=20 d? τ_tidal ∝ P^(13/3); at P=20 d on a metal-poor old star,
tidal damping over 7 Gyr is borderline. Numerical: τ_lock ≈ Q' × P × (M_star/M_p) × (a/R_p)^6 × (4 × π^2 / G M_star × P²)^(1/3)... actually for
a 20-d period and 1.75 M⊕ at 0.133 AU around 0.783 M☉, the Kasting/Murray-Clay timescale is several Gyr — comparable to system age. Treat as
possibly-locked, possibly-3:2 (Mercury analog).

Adopted scenario: hot rocky world, runaway-greenhouse-like with thick
CO₂ or stripped to bare-rock airless Venus-without-atmosphere. Pick
the **bare-rock / silicate vapor** scenario (interesting-first):
- the metal-poor host produced less iron-rich primordial grain
  population → silicate-vapor / olivine-dominated bedrock palette;
- 627 K dayside temperature is below silicate melting but high enough
  for atmospheric loss; outgassed CO₂ likely escaped via Jeans on a
  metal-poor low-XUV host.

**Classification (~25 rows).**
- Orbital (6): canonical-aligned.
- Physical (5): canonical-aligned (medium).
- Atmosphere (5): atmosphere_present=false adopted; airless. Pressure
  Pa = 0 or trace. Composition n/a. Tint n/a (tie-break low for
  "imperceptible Rayleigh").
- Surface (5): bare-rock palette, all low tie-break.
- Sky (2): canonical.

Counts: ~13 canonical-aligned, ~12 tie-break, 0 divergence.

### τ Cet h (P=49.41 d, a=0.243 AU, Msini=1.83 M⊕, e=0.23)

**Mass note.** Msini = 1.83 ± 0.68 M⊕. Most-probable true mass ~2.3 M⊕.
Radius DB raw.radius_rearth = 1.19. ρ = 1.83 × 5.97e24 / (4/3 × π ×
(1.19 × 6.371e6)³) = 5.99 g/cc — Earth-like, rocky.

**Scenario.** 7.74 S⊕, Teq A=0 466 K, Teq A=0.3 426 K. Tidally locked?
P=49.41 d is longer than g; τ_tidal scales as P^(13/3) → much longer
than 7 Gyr. Most likely *not* fully locked — Mercury-like 3:2 or
asynchronous slow rotator. Eccentricity 0.23 is the highest of the
three, supporting 3:2 capture (Vinson 2017 / Makarov 2018 give 3:2 at
e ≳ 0.01).

**Insolation 7.74 S⊕ → Venus-analog territory**. Runaway-greenhouse
expected: thick CO₂, hot dry surface (~700 K with greenhouse). But on
a metal-poor low-activity host the XUV-driven escape is weaker, so a
Venus-thick CO₂ atmosphere is *more* likely retained than around an
active K/M dwarf.

Adopted scenario: **Venus-analog with runaway-greenhouse thick CO₂
atmosphere**, hot dry surface. Cloud deck dominant.

**Classification (~25 rows).**
- Orbital (6): canonical-aligned (note higher ecc 0.23 from Feng 2017).
- Physical (5): canonical-aligned.
- Atmosphere (5): atmosphere_present=true, thick CO₂ (~10–90 bar
  Venus-analog), composition CO₂-dominated, H₂SO₄ clouds. Medium
  confidence (no observation; theoretical Venus-analog).
- Surface (5): no surface visible from orbit; bedrock prose only.
- Sky (2): canonical.

Counts: ~14 canonical-aligned, ~11 tie-break, 0 divergence.

## Notes for downstream Kopernicus cfg writer

- All three planets: orbital inclination unknown → adopt
  i ≈ 35° (Feng 2017 §5.2 reports 35 ± 10° for the disk plane,
  assumed coplanar; but the DB stores null). cfg can pick i in
  Phase 4 from the disk inclination.
- Radius DB stores raw values from Feng 2017's M-R relation — these
  are NOT measured; they are assumed-from-mass.
- f: snowball or thin frozen N₂/CO₂; cold cream-white surface, faint
  haze.
- g: bare rock; silicate-dominated; no atmosphere; ash-grey palette.
- h: Venus-analog; thick CO₂; sulfate clouds; obscured surface.

## Bibliography strategy

Feng 2017 is the discovery + best constraint on all three. Beyond
that, no individual-planet papers exist (these are RV-only, recent,
disputed). Phase 3 bibliography is therefore short:
- Feng 2017 (discovery, all parameters)
- Feng 2018 (follow-up; checks signal stability; possibly relevant
  to controversial flag)
- Tuomi 2013 (earlier τ Cet RV — the original 5-planet claim that
  Feng 2017 expanded to 4 surviving + 1 dropped)
- Kopparapu 2014 (habitable-zone formulae used to place f outside)
- Lustig-Yaeger / Pierrehumbert / Wordsworth — theoretical context
  (snowball, runaway, atmospheric escape)
- Vinson 2017 / Makarov 2018 — spin-orbit capture probability for h

No JWST, no transit, no direct imaging. The Bibliography "Read"
section will be shorter than TRAPPIST-1 syntheses.
