<!-- 암석형 외계행성 대기 표면기압·평균분자량·스케일높이 결정 방법론 레퍼런스 -->
# Rocky-Exoplanet Atmosphere Methodology: Surface Pressure & Scale Height

> Source: synthesis of the rocky-exoplanet atmosphere-retention and outgassing
> literature (Zahnle & Catling 2017, Owen 2019, Lopez 2017, Dong+ 2017/2018,
> Garraffo+ 2016, Ribas+ 2016, Meadows+ 2018, Herbort+ 2020, Wogan+ 2020,
> Schaefer+ 2017, Wordsworth & Kreidberg 2022, plus the JWST bare-rock results
> Greene+ 2023 / Zieba+ 2023).
> Citations resolved against NASA ADS (the registered ADS_API_TOKEN), not ad-hoc
> web search; arXiv id where one exists, otherwise the authoritative ADS bibcode.
> Purpose: a reusable recipe for **choosing and justifying** the surface pressure,
> mean molecular weight, and atmospheric scale height of rocky NearStars targets
> (Proxima b, the TRAPPIST-1 worlds, etc.), and for mapping those onto KSP/
> Kopernicus pressure curves at emit.
> This is a working reference, not a textbook. See §9 for the verified citations.

## Table of Contents

1. [Why Surface Pressure Is (Almost) Unconstrained](#1-why-surface-pressure-is-almost-unconstrained)
2. [Gate 1: Retention (the Cosmic Shoreline)](#2-gate-1-retention-the-cosmic-shoreline)
3. [Gate 2: M-Dwarf / Flare Stripping](#3-gate-2-m-dwarf--flare-stripping)
4. [Gate 3: Supply (Outgassing), Composition & Redox](#4-gate-3-supply-outgassing-composition--redox)
5. [Gate 4: Which Species Survive (the Jeans Parameter)](#5-gate-4-which-species-survive-the-jeans-parameter)
6. [Choosing the Pressure Value](#6-choosing-the-pressure-value)
7. [Mean Molecular Weight (μ) & Scale Height](#7-mean-molecular-weight-μ--scale-height)
8. [How NearStars Applies This](#8-how-nearstars-applies-this)
9. [Annotated Bibliography](#9-annotated-bibliography)
10. [Related](#related)

---

## 1. Why Surface Pressure Is (Almost) Unconstrained

For nearly every rocky planet in the NearStars roster, **we do not measure the
surface pressure**. There is no observation that returns a number in bars. This is
the central honesty of this document: the surface pressure we put in the config is
a *principled choice within physical bounds*, not a measurement.

What the data actually constrains, by target type:

- **Non-transiting planets** (Proxima b, most RV-discovered worlds): nothing about
  the atmosphere is observed at all. We have a minimum mass (`m sin i`), an orbit,
  and the host's irradiation. The atmosphere is entirely inferred.

- **Transiting planets** (the TRAPPIST-1 worlds, GJ 1132 b, …): transmission and
  thermal-emission spectroscopy can sometimes **detect or rule out the *presence***
  of a substantial atmosphere, but not pin a surface pressure. JWST thermal
  emission of TRAPPIST-1 b is consistent with a **bare rock / no thick atmosphere**
  (Greene+ 2023), and TRAPPIST-1 b shows **no thick CO₂ atmosphere** (Zieba+ 2023).
  These are existence bounds ("thick atmosphere? yes/no/unlikely"), not pressure
  measurements. A 0.1-bar and a 2-bar atmosphere of the same composition are not
  distinguished by current data.

So the methodology is a chain of **gates** (can it keep an atmosphere? does the
star strip it? is there enough outgassing supply?) followed by a **documented
choice** of the value within the surviving band. The gates are physics; the final
number is a tie-break recorded on the Phase 4 board with its justification.

The canonical review for this whole picture is **Wordsworth & Kreidberg 2022**
(*ARA&A*): read it first if you read only one reference here.

---

## 2. Gate 1: Retention (the Cosmic Shoreline)

The first question is not *how much* atmosphere but *whether any survives at all*.
That is set by a competition between the planet's gravity (escape velocity) and the
cumulative high-energy dose it has absorbed (XUV + insolation integrated over the
system's lifetime).

**Zahnle & Catling 2017** formalize this as the **cosmic shoreline**: across the
solar system and the exoplanet sample, the bodies that retain atmospheres separate
cleanly from the airless ones along a line in escape-velocity-vs-cumulative-XUV
space, roughly `v_esc ∝ I_XUV^(1/4)`. It is empirical and remarkably sharp.

- **Below the shoreline** (low gravity and/or high lifetime XUV dose) → **bare
  rock**. No atmosphere is expected; the config is a vacuum or near-vacuum body.
- **Above the shoreline** → an atmosphere is **plausible** and Gates 2–3 decide its
  thickness and composition.

Two supporting results sharpen the gate:

- **Owen 2019** (*ARA&A* review) lays out the escape *mechanisms* (XUV-driven
  photoevaporation and core-powered mass loss) that move a planet across the
  shoreline over time. The early phase, when the host is XUV-bright, does most of
  the stripping.
- **Lopez 2017** (and the wider radius-valley work) shows escape sculpts the
  rocky/sub-Neptune boundary: planets that keep a thick H/He envelope sit above the
  **radius valley** (~1.8 R⊕), while stripped cores fall below it. A body small
  enough to be rocky has, almost by definition, already lost any primordial H/He,
  so its atmosphere (if any) is a **secondary, outgassed** one, which is what Gate 3
  is about.

Gate 1 is therefore the binary filter: clear the shoreline, or the answer is "bare
rock, no pressure curve needed."

---

## 3. Gate 2: M-Dwarf / Flare Stripping

Most NearStars terrestrial targets orbit **M dwarfs**, and that makes Gate 1 much
less forgiving than the solar-system shoreline alone suggests. M dwarfs stay
XUV-bright for hundreds of Myr to Gyr, flare violently, and drive dense stellar
winds, all of which erode atmospheres on the close-in (and therefore tidally
locked) habitable-zone planets. The habitable zone of an M dwarf sits **right on or
just inside the shoreline**, so "has an atmosphere" is frequently a genuine
tie-break rather than a settled fact.

The Proxima/TRAPPIST literature maps this in detail:

- **Ribas+ 2016**: the irradiation environment of Proxima b: the XUV and
  particle dose the planet integrates over the star's long active lifetime. This is
  the input to every stripping estimate.
- **Dong+ 2017**: stellar-wind-driven ion escape from Proxima b. For plausible
  wind pressures the atmosphere can be eroded on geologically short timescales
  unless continually replenished; the planet sits on the knife-edge.
- **Dong+ 2018**: the same stellar-wind escape modeling extended to the
  **TRAPPIST-1** planets, with implications for which (if any) can hold an
  atmosphere against the wind.
- **Garraffo+ 2016**: the **space weather** of Proxima b: a strong, ordered
  *planetary* magnetic field can shield the atmosphere from the wind, but the
  required field strength and the wind variability make protection uncertain
  rather than guaranteed. (There is no separate Garraffo Proxima *journal* paper in
  2017, only a conference abstract, so cite the 2016 *ApJL* for this point.)
  **Read this one against Ramstad & Barabash 2021 in §5**, which argues from
  solar-system ion-flux measurements that a dipole is not required to prevent
  wind-driven escape and may increase ion escape instead. Magnetic shielding is an
  open question here, not a mechanism to lean on.
- **Meadows+ 2018**: enumerates the plausible **environmental/atmospheric states**
  of Proxima b (desiccated O₂-dominated, CO₂, Venus-like, habitable, …) that
  follow from different escape and evolution histories. This is the explicit
  "branching set of outcomes" that a tie-break must choose among.

The JWST non-detections in §1 (Greene+ 2023, Zieba+ 2023) are the empirical
vindication of Gate 2: the innermost, most-irradiated TRAPPIST-1 worlds do appear
to be stripped. The practical rule: for an M-dwarf HZ planet, treat the atmosphere
as **plausible-but-not-assumed**, and record which Meadows-style state you picked
and why.

---

## 4. Gate 3: Supply (Outgassing), Composition & Redox

If a planet clears retention, the pressure that actually exists is set by a balance
between **outgassing supply** (volcanism degassing the interior) and the **escape
sink** of Gate 2. Outgassing does double duty: it sets *how much* gas there is and
*what kind*: the redox state of the released volatiles, which determines whether
the atmosphere is oxidized (CO₂ / N₂ / H₂O) or reduced (CH₄ / H₂ / CO).

- **Schaefer+ 2017** (Schaefer, Redox States of Initial Atmospheres Outgassed on
  Rocky Planets; *ApJ* 843, 120, **no arXiv**) computes the initial atmosphere
  redox from the oxidation state of the outgassing material. A more oxidized mantle
  → CO₂/H₂O-dominated; a more reduced one → CH₄/H₂/CO-dominated. This is the link
  from interior composition to the μ that Gate-6 needs.
- **Herbort+ 2020**: chemical equilibrium between common crustal rock types and an
  outgassed atmosphere, predicting the resulting gas inventory for a range of
  rock compositions. The practical "what gases does this crust give you" table.
- **Wogan+ 2020**: shows that volcanism on a reduced rocky planet can sustain an
  **abundant CH₄** atmosphere (a reduced-redox endmember), the methane counterpart
  to the oxidized CO₂/N₂ default.

The composition that emerges from Gate 3 is what feeds §7: an oxidized world lands
near a CO₂/N₂ μ (heavy), a reduced one near a CH₄/H₂ μ (light), and the difference
is large enough to change the scale height by a factor of several.

---

## 5. Gate 4: Which Species Survive (the Jeans Parameter)

Gates 1–3 answer "is there an atmosphere, and what was outgassed into it". They do
not answer **which of those gases stay**, and that is a separate competition:
gravity against the thermal energy of *one molecular species* at the exobase. It is
why Titan keeps nitrogen on 2.6 km/s of escape velocity while Mars loses hydrogen on
5.0 km/s. Mass and temperature decide, not gravity alone.

Calculator: [`scripts/refs/jeans_escape.py`](../../scripts/refs/jeans_escape.py).

### The Jeans parameter

    λ  =  G M m / (k T_exo r_exo)

the ratio of a molecule's gravitational to thermal energy, evaluated at the exobase.
`m` is the mass of the individual species, so λ scales linearly with molecular
weight: at the same temperature, N₂ is fourteen times more tightly bound than H₂.
This is textbook kinetic theory (Jeans; see
[Catling & Kasting 2017](https://ui.adsabs.harvard.edu/abs/2017aeil.book.....C) for
the modern treatment), so it needs no separate grounding — but the *thresholds* do.

### Regimes, and where they sit

[Volkov 2011](https://arxiv.org/abs/1009.5110) mapped the transition with direct
simulation Monte Carlo, which is what makes these numbers citable rather than
folklore:

| λ (at the lower boundary) | Regime | |
|---|---|---|
| ≲ 2.1 | isentropic supersonic outflow limit | hydrodynamic blow-off |
| ~2–3 (atomic), ~2.4–3.6 (diatomic) | the transition itself | organized outflow gives way to molecule-by-molecule |
| > 3 | escape proceeds molecule-by-molecule | |
| ≳ 6 | "the escape rate does not deviate significantly from the familiar Jeans rate" | classical Jeans |

Volkov also corrects an earlier belief: above λ ≈ 6 the rate is *not* strongly
enhanced over the classical Jeans formula, and for diatomic gases above λ ≈ 4 it
runs only a few tens of percent above the monatomic case.

The calculator adds one convention that is **not** from the literature: it labels
λ > 30 as "retained", on the grounds that the Jeans flux there is negligible over
Gyr. Treat that boundary as this doc's bookkeeping, not as a published threshold.

### The diffusion limit: why a light gas leaves at a rate its own λ does not set

For a light species mixed into a heavier background, λ is not the whole story.
[Hunten 1973](https://ui.adsabs.harvard.edu/abs/1973JAtS...30.1481H) showed that in
the "easy escape" regime the flux is instead **capped by diffusion of the light
species up through the background**, with a simple expression, so the loss rate is
set by its mixing ratio rather than by the exobase temperature. Two consequences
matter for us:

- **A trace light gas escapes at the diffusion-limited rate.** Hunten reproduces
  Earth's hydrogen flux to within a factor of 2 from the stratospheric H₂O mixing
  ratio alone. An invented atmosphere with a few tenths of a percent H₂ is losing it
  steadily however cold the exobase is.
- **The heavy gases are not dragged along.** Even in hydrodynamic blow-off of the
  light component, Hunten found the outflow "orderly, not chaotic", and "normally,
  the heavier gases are not carried along". So a world can lose all its H₂ and keep
  its N₂ inventory intact. Selective loss is the normal case, not a special one.

### Ion escape, and the magnetic-field paradigm Gate 2 inherited

Thermal escape is not the only sink, and here the literature has moved.
[Ramstad & Barabash 2021](https://ui.adsabs.harvard.edu/abs/2021SSRv..217...36R)
review the accumulated ion-flux measurements at Venus, Earth and Mars and find ion
escape is either **energy-limited** (Venus, Earth) or **supply-limited** (Mars,
"mainly due to its low gravity"), and that at Mars ion escape "has likely
contributed relatively little to the total loss of the early Martian atmosphere, in
comparison to neutral escape processes."

Their headline conclusion revises Gate 2's framing: "contrary to the current
paradigm … an intrinsic magnetic dipole field is **not required** to prevent stellar
wind-driven escape of planetary atmospheres, and the presence of one may instead
**increase** the rate of ion escape." Gate 2 above cites Garraffo+ 2016 for a
planetary field shielding the atmosphere; read that as one side of an open question,
not as the mechanism. **Do not use "it has a magnetosphere" as a retention argument
on a NearStars board row.**

### Validation

`python3 scripts/refs/jeans_escape.py`

| Body | v_esc | T_exo | λ per species | Known outcome |
|---|---|---|---|---|
| Earth | 11.2 km/s | 1000 K | H 7.0, H₂ 14, N₂ 195, O₂ 223 | H escapes, N₂/O₂ kept ✓ |
| Titan | 2.6 km/s | 175 K | H₂ 3.1, CH₄ 24, N₂ 42 | N₂ kept on weak gravity because it is cold; H₂ in the transition regime and lost ✓ |
| Mars | 5.0 km/s | 250 K | H 5.8, H₂ 12, CO₂ 253 | H escapes; CO₂ bound against *thermal* escape, its actual loss being ion/sputtering ✓ |

Earth's H at λ = 7.0 reproduces the textbook value, and the Titan row is the useful
one: it shows the recipe getting a body right *against* the naive gravity intuition,
which is the failure mode this gate exists to prevent.

### Worked example: Cassandra

Cassandra (9.0 × 10²³ kg, 3400 km, v_esc 5.9 km/s) is recorded as retaining N₂/CO₂
while H₂ "escapes but is replenished volcanically". That claim had no recipe behind
it until now. Bracketing the exobase temperature, which is the weak input:

| T_exo | H₂ | CH₄ | N₂ | CO₂ |
|---|---|---|---|---|
| 300 K | 13.5 | 107 | 187 | 294 |
| 500 K | 8.1 | 64 | 112 | 177 |
| 800 K | 5.1 | 40 | 70 | 110 |

H₂ sits between classical Jeans and the molecule-by-molecule regime across the whole
range while everything heavier is firmly bound — so the recorded entry is correct,
and now quantified. Note that H₂'s loss will in practice be diffusion-limited at
these mixing ratios, so the volcanic replenishment the row invokes is doing real
work rather than papering over a gap.

Pandora, at 3.85 × 10²⁴ kg and 9.5 km/s, holds everything including H₂S and Xe, with
H₂ leaking slowly (λ 12.9 at 800 K). Hades and Dante never reach this gate: at 0.94
and 1.09 km/s of escape velocity they fail Gate 1 outright.

### Domain of validity

1. **`T_exo` is the weak input.** It is not the surface temperature — Earth's
   exobase runs ~1000 K against a 288 K surface — and for an invented body it is
   unconstrained. Always bracket it as above rather than quoting one λ.
2. **λ is a rate regime, not a yes/no.** A species at λ = 10 is escaping; whether
   that matters depends on the inventory and the resupply, which is Gate 3's half of
   the balance.
3. **Non-thermal channels are not in λ at all**: ion escape, sputtering,
   photochemical loss. For CO₂ on a Mars-like body these dominate, which is exactly
   why Mars's λ = 253 does not mean Mars kept its atmosphere.
4. **This gate does not set the pressure**, only which species may appear in the
   composition that §6 then assigns a total pressure to.

---

## 6. Choosing the Pressure Value

With the gates cleared, the surface pressure is a **documented choice within a
physically bounded band**. The procedure:

1. **Confirm retention.** Run the body through Gates 1–2. If it falls below the
   shoreline or is a stripped M-dwarf inner-HZ world, stop: it is a bare rock, and
   the surface pressure is ~0.

2. **Take a band from solar-system analogs + outgassing expectations.** Rocky
   secondary atmospheres span four orders of magnitude:

   | Analog | Surface pressure | What it represents |
   |---|---|---|
   | Mars | ~0.006 bar | thin, escape-dominated, weak outgassing |
   | Titan | ~1.5 bar | thick N₂ on a small body (cold, low escape) |
   | Earth | ~1 bar | the canonical habitable middle |
   | Venus | ~90 bar | runaway, outgassing-dominated, no escape sink |

   The Gate-2 stripping severity sets where in this band the body plausibly sits:
   heavy stripping pushes toward the Mars end, weak stripping plus active volcanism
   toward the Venus end.

3. **Pick within the band.** For a transiting body with an existence bound, respect
   it (don't put a thick atmosphere where JWST rules one out). For a non-transiting
   body the value is a **tie-break**, chosen for physical plausibility and
   gameplay, and **recorded on the Phase 4 board together with its retention-gate
   justification**, never an unstated default.

The output of §6 is a single chosen surface pressure (in pascals for Kopernicus)
plus the composition from Gate 3. Both feed §7.

---

## 7. Mean Molecular Weight (μ) & Scale Height

The scale height `H` is the e-folding height of pressure with altitude: it sets
how fast the atmosphere thins out, and therefore the **shape** of the Kopernicus
`pressureCurve` (the chosen surface pressure sets its *height*).

```
H = R · T / (μ · g)        (R = 8.314 J/mol/K; μ in kg/mol)
  = k · T / (m̄ · g)        (k = 1.381e-23 J/K; m̄ = mean molecular mass in kg)
```

The two forms are identical (`R = k · N_A`, `μ = m̄ · N_A`). Use whichever units are
handy; keep μ in **kg/mol** for the first form (so 28 g/mol → 0.028 kg/mol).

**μ reference table** (g/mol):

| Species | μ (g/mol) | | Species | μ (g/mol) |
|---|---|---|---|---|
| H₂/He solar mix | ~2.3 | | air (N₂/O₂) | 28.97 |
| H₂ | 2.016 | | CO | 28.01 |
| He | 4.003 | | O₂ | 32.00 |
| CH₄ | 16.04 | | Ar | 39.95 |
| H₂O | 18.02 | | CO₂ | 44.01 |
| NH₃ | 17.03 | | SO₂ | 64.07 |
| N₂ | 28.01 | | | |

For a **mixture**, weight by mole fraction `xᵢ` (not mass fraction):

```
μ = Σ xᵢ μᵢ
```

So a 97% N₂ + 3% CO₂ atmosphere is `0.97·28.01 + 0.03·44.01 ≈ 28.5 g/mol`.

**Worked example: Proxima b lake-world.** Composition N₂ + ~3% CO₂ (the Turbet/
Boutle ~1-bar habitable case), so μ ≈ 28.5 g/mol = 0.0285 kg/mol. Surface gravity
g ≈ 10.5 m/s² (≈ 1.07 g for the ~1.07–1.3 M⊕ / ~1.1 R⊕ body). Temperature T in the
substellar-to-mean range 250–290 K:

```
H = R·T/(μ·g) = 8.314 · 270 / (0.0285 · 10.5) ≈ 7.5 km
```

giving **H ≈ 7–8 km** across the 250–290 K range. This **corrects an earlier ad-hoc
"9–11 km" estimate**: the table-plus-formula route is the point, μ ≈ 28.5 (not a
guessed lighter value) and g ≈ 10.5 pin H firmly in the 7–8 km band. Always derive
H from a stated μ (mole-fraction-weighted from the Gate-3 composition) and the
body's actual g, never by analogy.

---

## 8. How NearStars Applies This

The chosen pressure and composition map directly onto the Kopernicus atmosphere
model:

- **Chosen surface pressure → `staticPressureASL`** (the sea-level pressure, in kPa
  in the Kopernicus convention, convert from the pascals of §6).

- **Composition → μ → H → the `pressureCurve` falloff.** The surface pressure sets
  the curve's value at altitude 0; the scale height `H` from §7 sets the e-folding
  rate at which it decays (`P(z) ≈ P₀ · exp(−z/H)` for an isothermal layer, which
  is the shape the pressureCurve keyframes approximate). A heavy (CO₂) atmosphere
  gives a small H and a steeply falling curve; a light (H₂/CH₄) one a large H and a
  gentle falloff.

- **Record pressure + composition + the retention-gate justification on the Phase 4
  board.** The board entry must state the chosen surface pressure, the composition
  (hence μ and H), and *which gate reasoning* supports keeping an atmosphere at all
  (shoreline clearance, M-dwarf stripping verdict, outgassing supply). Where the
  value is unconstrained, it is flagged as a documented tie-break, not a silent
  default.

This keeps the emit deterministic and reproducible: every pressure curve traces
back to a stated composition, a computed scale height, and a cited retention
argument.

---

## 9. Annotated Bibliography

Each entry: authors, year, journal, **verified** arXiv id (or a flag where none
exists), and one line on what it contributes.

- **Zahnle, K. J. & Catling, D. C. (2017)**: *ApJ* 843, 122. **[arXiv:1702.03386](https://arxiv.org/abs/1702.03386).**
  Defines the **cosmic shoreline**: escape velocity vs cumulative XUV separates
  atmosphere-bearing from airless bodies. Gate 1.

- **Owen, J. E. (2019)**: *Annual Review of Earth and Planetary Sciences* 47, 67.
  **[arXiv:1807.07609](https://arxiv.org/abs/1807.07609).** Review of atmospheric-escape mechanisms (photoevaporation,
  core-powered mass loss) driving close-in planet evolution. Gate 1 mechanism.

- **Lopez, E. D. (2017)**: *MNRAS* 472, 245. **[arXiv:1610.01170](https://arxiv.org/abs/1610.01170).** "Born dry in the
  photoevaporation desert": escape sculpts the rocky/sub-Neptune boundary, so small
  rocky planets have lost primordial H/He and carry only secondary atmospheres.
  (The "born rocky vs stripped sub-Neptune" framing; companion to Lopez & Fortney
  2014, *ApJ* 792, 1, [arXiv:1311.0329](https://arxiv.org/abs/1311.0329), the radius-valley mass-radius work.)

- **Ribas, I. et al. (2016)**: *A&A* 596, A111. **[arXiv:1608.06813](https://arxiv.org/abs/1608.06813).** The
  irradiation, rotation and volatile inventory of Proxima b: the XUV/particle dose
  input to every stripping estimate. Gate 2.

- **Dong, C. et al. (2017)**: *ApJ Letters* 837, L26. **[arXiv:1702.04089](https://arxiv.org/abs/1702.04089).**
  Stellar-wind-driven atmospheric ion escape from Proxima b; the atmosphere can be
  stripped on short timescales unless replenished. Gate 2.

- **Dong, C. et al. (2018)**: *PNAS* 115, 260. **[arXiv:1705.05535](https://arxiv.org/abs/1705.05535).** The same
  stellar-wind escape modeling for the **TRAPPIST-1** planets. Gate 2.

- **Garraffo, C. et al. (2016)**: *ApJ Letters* 833, L4. **[arXiv:1609.09076](https://arxiv.org/abs/1609.09076).** The
  space weather of Proxima b; a strong ordered planetary magnetic field could
  shield the atmosphere, but protection is uncertain. (No separate 2017 Proxima
  journal paper exists, only a conference abstract.) Gate 2.

- **Meadows, V. S. et al. (2018)**: *Astrobiology* 18, 133. **[arXiv:1608.08620](https://arxiv.org/abs/1608.08620).**
  Enumerates the plausible environmental/atmospheric end-states of Proxima b
  (desiccated, CO₂, Venus-like, habitable): the branching set a tie-break selects
  among. Gate 2.

- **Schaefer, L. et al. (2017)**: *ApJ* 843, 120. **No arXiv preprint found.**
  "Redox States of Initial Atmospheres Outgassed on Rocky Planets": initial
  atmosphere redox (oxidized CO₂/H₂O vs reduced CH₄/H₂/CO) from the outgassing
  material's oxidation state. Gate 3, sets composition → μ.

- **Herbort, O. et al. (2020)**: *A&A* 636, A71. **[arXiv:2003.03628](https://arxiv.org/abs/2003.03628).** "The
  atmospheres of rocky exoplanets. I": chemical equilibrium between crustal rock
  types and the outgassed atmosphere: the gas inventory a given crust yields.
  Gate 3.

- **Wogan, N. et al. (2020)**: *PSJ* 1, 58. **[arXiv:2009.07761](https://arxiv.org/abs/2009.07761).** Volcanism on a
  reduced rocky planet can sustain an **abundant CH₄** atmosphere: the reduced-
  redox endmember opposite the CO₂/N₂ default. Gate 3.

- **Volkov, A. N. et al. (2011)**: *ApJ Letters* 729, L24
  (`2011ApJ...729L..24V`). **[arXiv:1009.5110](https://arxiv.org/abs/1009.5110).**
  Direct simulation Monte Carlo of thermally driven escape, mapping the
  hydrodynamic ↔ Jeans transition: λ₀ ~ 2–3 for an atomic gas (lower bound 2.1 = the
  isentropic supersonic outflow limit), ~2.4–3.6 diatomic, and above λ₀ ≈ 6 the rate
  matches the classical Jeans rate. Source of every λ threshold in §5. Numbers from
  the ADS abstract; *ar5iv has no usable full text*.

- **Hunten, D. M. (1973)**: *J. Atmos. Sci.* 30, 1481
  (`1973JAtS...30.1481H`). **No arXiv preprint (1973).** The diffusion limit: for a
  light gas in a heavier background the escape flux is set by diffusion up through
  the background rather than by the exobase temperature, with a simple expression;
  reproduces Earth's hydrogen flux to a factor of 2 from the stratospheric H₂O
  mixing ratio. Also establishes that in blow-off of the light component the outflow
  is "orderly, not chaotic" and "normally, the heavier gases are not carried along",
  which is the basis for selective loss in §5. Numbers from the ADS abstract.

- **Ramstad, R. & Barabash, S. (2021)**: *Space Science Reviews* 217, 36
  (`2021SSRv..217...36R`). **No arXiv preprint found.** Reviews measured ion-escape
  rates at Venus, Earth and Mars; ion escape is energy-limited (Venus, Earth) or
  supply-limited (Mars, from its low gravity), and at Mars contributed relatively
  little to the total early loss compared with neutral escape. Concludes, against the
  prevailing paradigm, that an intrinsic dipole is not required to prevent
  wind-driven escape and may increase ion escape. Revises how Gate 2's
  magnetic-shielding argument should be read. Numbers from the ADS abstract.

- **Catling, D. C. & Kasting, J. F. (2017)**: *Atmospheric Evolution on Inhabited and
  Lifeless Worlds* (`2017aeil.book.....C`). Textbook home of the Jeans parameter and
  the escape-regime taxonomy used in §5; cited as the allowed textbook exception, not
  for a specific number.

- **Wordsworth, R. & Kreidberg, L. (2022)**: *Annual Review of Astronomy &
  Astrophysics* 60, 159. **[arXiv:2112.04663](https://arxiv.org/abs/2112.04663).** The canonical review of rocky-
  exoplanet atmospheres: retention, escape, outgassing, observability. Read first.

- **Greene, T. P. et al. (2023)**: *Nature* 618, 39. **[arXiv:2303.14849](https://arxiv.org/abs/2303.14849).** JWST
  thermal emission of TRAPPIST-1 b consistent with a **bare rock / no thick
  atmosphere**: empirical confirmation that M-dwarf inner-HZ worlds can be
  stripped. The "existence bound, not pressure measurement" of §1.

- **Zieba, S. et al. (2023)**: *Nature* 620, 746. **[arXiv:2306.10150](https://arxiv.org/abs/2306.10150).** **No thick
  CO₂ atmosphere** on TRAPPIST-1 b from JWST: a presence/absence bound, again not
  a surface-pressure measurement.

---

## Related

- [tidally-locked-temperature-methodology](tidally-locked-temperature-methodology.md): the sibling recipe
  for the temperature `T` that enters the scale-height formula here (§7); the
  Proxima b ~250–290 K range used in the worked example comes from its Layer-3 GCM
  anchors (Turbet+ 2016, Boutle+ 2017).
- [greenhouse-warming-methodology](greenhouse-warming-methodology.md): consumes the
  composition decided here (CO₂ fraction, CH₄, H₂, total pressure) and turns it into the
  greenhouse increment above `T_eq`. If a body needs a warmer surface than that recipe
  allows, the composition is what has to move.
- [solar-system-external-observer](solar-system-external-observer.md): the Teq-blind-to-greenhouse
  calibration that motivates the "we don't measure the atmosphere" caution in §1
  (Venus' surface conditions are invisible to the kind of data we have here).
- Phase 3 synthesis skill (`nearstars-phase3`): where the chosen surface pressure,
  composition, μ and H are recorded per planet and the retention-gate justification
  is pinned to the Phase 4 board.
- [methodology-index](methodology-index.md) — the index of all derived-value methodology recipes.
