<!-- 암석형 외계행성 대기 표면기압·평균분자량·스케일높이 결정 방법론 레퍼런스 -->
# Rocky-Exoplanet Atmosphere Methodology — Surface Pressure & Scale Height

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
> This is a working reference, not a textbook — see §8 for the verified citations.

## Table of Contents

1. [Why Surface Pressure Is (Almost) Unconstrained](#1-why-surface-pressure-is-almost-unconstrained)
2. [Gate 1 — Retention (the Cosmic Shoreline)](#2-gate-1--retention-the-cosmic-shoreline)
3. [Gate 2 — M-Dwarf / Flare Stripping](#3-gate-2--m-dwarf--flare-stripping)
4. [Gate 3 — Supply (Outgassing), Composition & Redox](#4-gate-3--supply-outgassing-composition--redox)
5. [Choosing the Pressure Value](#5-choosing-the-pressure-value)
6. [Mean Molecular Weight (μ) & Scale Height](#6-mean-molecular-weight-μ--scale-height)
7. [How NearStars Applies This](#7-how-nearstars-applies-this)
8. [Annotated Bibliography](#8-annotated-bibliography)
9. [Related](#related)

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
  of a substantial atmosphere — but not pin a surface pressure. JWST thermal
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
(*ARA&A*) — read it first if you read only one reference here.

---

## 2. Gate 1 — Retention (the Cosmic Shoreline)

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

- **Owen 2019** (*ARA&A* review) lays out the escape *mechanisms* — XUV-driven
  photoevaporation and core-powered mass loss — that move a planet across the
  shoreline over time. The early phase, when the host is XUV-bright, does most of
  the stripping.
- **Lopez 2017** (and the wider radius-valley work) shows escape sculpts the
  rocky/sub-Neptune boundary: planets that keep a thick H/He envelope sit above the
  **radius valley** (~1.8 R⊕), while stripped cores fall below it. A body small
  enough to be rocky has, almost by definition, already lost any primordial H/He —
  so its atmosphere (if any) is a **secondary, outgassed** one, which is what Gate 3
  is about.

Gate 1 is therefore the binary filter: clear the shoreline, or the answer is "bare
rock, no pressure curve needed."

---

## 3. Gate 2 — M-Dwarf / Flare Stripping

Most NearStars terrestrial targets orbit **M dwarfs**, and that makes Gate 1 much
less forgiving than the solar-system shoreline alone suggests. M dwarfs stay
XUV-bright for hundreds of Myr to Gyr, flare violently, and drive dense stellar
winds — all of which erode atmospheres on the close-in (and therefore tidally
locked) habitable-zone planets. The habitable zone of an M dwarf sits **right on or
just inside the shoreline**, so "has an atmosphere" is frequently a genuine
tie-break rather than a settled fact.

The Proxima/TRAPPIST literature maps this in detail:

- **Ribas+ 2016** — the irradiation environment of Proxima b: the XUV and
  particle dose the planet integrates over the star's long active lifetime. This is
  the input to every stripping estimate.
- **Dong+ 2017** — stellar-wind-driven ion escape from Proxima b. For plausible
  wind pressures the atmosphere can be eroded on geologically short timescales
  unless continually replenished; the planet sits on the knife-edge.
- **Dong+ 2018** — the same stellar-wind escape modeling extended to the
  **TRAPPIST-1** planets, with implications for which (if any) can hold an
  atmosphere against the wind.
- **Garraffo+ 2016** — the **space weather** of Proxima b: a strong, ordered
  *planetary* magnetic field can shield the atmosphere from the wind, but the
  required field strength and the wind variability make protection uncertain
  rather than guaranteed. (There is no separate Garraffo Proxima *journal* paper in
  2017 — only a conference abstract — so cite the 2016 *ApJL* for this point.)
- **Meadows+ 2018** — enumerates the plausible **environmental/atmospheric states**
  of Proxima b (desiccated O₂-dominated, CO₂, Venus-like, habitable, …) that
  follow from different escape and evolution histories. This is the explicit
  "branching set of outcomes" that a tie-break must choose among.

The JWST non-detections in §1 (Greene+ 2023, Zieba+ 2023) are the empirical
vindication of Gate 2: the innermost, most-irradiated TRAPPIST-1 worlds do appear
to be stripped. The practical rule: for an M-dwarf HZ planet, treat the atmosphere
as **plausible-but-not-assumed**, and record which Meadows-style state you picked
and why.

---

## 4. Gate 3 — Supply (Outgassing), Composition & Redox

If a planet clears retention, the pressure that actually exists is set by a balance
between **outgassing supply** (volcanism degassing the interior) and the **escape
sink** of Gate 2. Outgassing does double duty: it sets *how much* gas there is and
*what kind* — the redox state of the released volatiles, which determines whether
the atmosphere is oxidized (CO₂ / N₂ / H₂O) or reduced (CH₄ / H₂ / CO).

- **Schaefer+ 2017** (Schaefer, Redox States of Initial Atmospheres Outgassed on
  Rocky Planets; *ApJ* 843, 120 — **no arXiv**) computes the initial atmosphere
  redox from the oxidation state of the outgassing material. A more oxidized mantle
  → CO₂/H₂O-dominated; a more reduced one → CH₄/H₂/CO-dominated. This is the link
  from interior composition to the μ that Gate-6 needs.
- **Herbort+ 2020** — chemical equilibrium between common crustal rock types and an
  outgassed atmosphere, predicting the resulting gas inventory for a range of
  rock compositions. The practical "what gases does this crust give you" table.
- **Wogan+ 2020** — shows that volcanism on a reduced rocky planet can sustain an
  **abundant CH₄** atmosphere (a reduced-redox endmember), the methane counterpart
  to the oxidized CO₂/N₂ default.

The composition that emerges from Gate 3 is what feeds §6: an oxidized world lands
near a CO₂/N₂ μ (heavy), a reduced one near a CH₄/H₂ μ (light), and the difference
is large enough to change the scale height by a factor of several.

---

## 5. Choosing the Pressure Value

With the gates cleared, the surface pressure is a **documented choice within a
physically bounded band**. The procedure:

1. **Confirm retention.** Run the body through Gates 1–2. If it falls below the
   shoreline or is a stripped M-dwarf inner-HZ world, stop — it is a bare rock, and
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
   justification** — never an unstated default.

The output of §5 is a single chosen surface pressure (in pascals for Kopernicus)
plus the composition from Gate 3. Both feed §6.

---

## 6. Mean Molecular Weight (μ) & Scale Height

The scale height `H` is the e-folding height of pressure with altitude — it sets
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

**Worked example — Proxima b lake-world.** Composition N₂ + ~3% CO₂ (the Turbet/
Boutle ~1-bar habitable case), so μ ≈ 28.5 g/mol = 0.0285 kg/mol. Surface gravity
g ≈ 10.5 m/s² (≈ 1.07 g for the ~1.07–1.3 M⊕ / ~1.1 R⊕ body). Temperature T in the
substellar-to-mean range 250–290 K:

```
H = R·T/(μ·g) = 8.314 · 270 / (0.0285 · 10.5) ≈ 7.5 km
```

giving **H ≈ 7–8 km** across the 250–290 K range. This **corrects an earlier ad-hoc
"9–11 km" estimate**: the table-plus-formula route is the point — μ ≈ 28.5 (not a
guessed lighter value) and g ≈ 10.5 pin H firmly in the 7–8 km band. Always derive
H from a stated μ (mole-fraction-weighted from the Gate-3 composition) and the
body's actual g, never by analogy.

---

## 7. How NearStars Applies This

The chosen pressure and composition map directly onto the Kopernicus atmosphere
model:

- **Chosen surface pressure → `staticPressureASL`** (the sea-level pressure, in kPa
  in the Kopernicus convention — convert from the pascals of §5).

- **Composition → μ → H → the `pressureCurve` falloff.** The surface pressure sets
  the curve's value at altitude 0; the scale height `H` from §6 sets the e-folding
  rate at which it decays (`P(z) ≈ P₀ · exp(−z/H)` for an isothermal layer, which
  is the shape the pressureCurve keyframes approximate). A heavy (CO₂) atmosphere
  gives a small H and a steeply falling curve; a light (H₂/CH₄) one a large H and a
  gentle falloff.

- **Record pressure + composition + the retention-gate justification on the Phase 4
  board.** The board entry must state the chosen surface pressure, the composition
  (hence μ and H), and *which gate reasoning* supports keeping an atmosphere at all
  (shoreline clearance, M-dwarf stripping verdict, outgassing supply). Where the
  value is unconstrained, it is flagged as a documented tie-break — not a silent
  default.

This keeps the emit deterministic and reproducible: every pressure curve traces
back to a stated composition, a computed scale height, and a cited retention
argument.

---

## 8. Annotated Bibliography

Each entry: authors, year, journal, **verified** arXiv id (or a flag where none
exists), and one line on what it contributes.

- **Zahnle, K. J. & Catling, D. C. (2017)** — *ApJ* 843, 122. **arXiv:1702.03386.**
  Defines the **cosmic shoreline**: escape velocity vs cumulative XUV separates
  atmosphere-bearing from airless bodies. Gate 1.

- **Owen, J. E. (2019)** — *Annual Review of Earth and Planetary Sciences* 47, 67.
  **arXiv:1807.07609.** Review of atmospheric-escape mechanisms (photoevaporation,
  core-powered mass loss) driving close-in planet evolution. Gate 1 mechanism.

- **Lopez, E. D. (2017)** — *MNRAS* 472, 245. **arXiv:1610.01170.** "Born dry in the
  photoevaporation desert": escape sculpts the rocky/sub-Neptune boundary, so small
  rocky planets have lost primordial H/He and carry only secondary atmospheres.
  (The "born rocky vs stripped sub-Neptune" framing; companion to Lopez & Fortney
  2014, *ApJ* 792, 1, arXiv:1311.0329, the radius-valley mass-radius work.)

- **Ribas, I. et al. (2016)** — *A&A* 596, A111. **arXiv:1608.06813.** The
  irradiation, rotation and volatile inventory of Proxima b — the XUV/particle dose
  input to every stripping estimate. Gate 2.

- **Dong, C. et al. (2017)** — *ApJ Letters* 837, L26. **arXiv:1702.04089.**
  Stellar-wind-driven atmospheric ion escape from Proxima b; the atmosphere can be
  stripped on short timescales unless replenished. Gate 2.

- **Dong, C. et al. (2018)** — *PNAS* 115, 260. **arXiv:1705.05535.** The same
  stellar-wind escape modeling for the **TRAPPIST-1** planets. Gate 2.

- **Garraffo, C. et al. (2016)** — *ApJ Letters* 833, L4. **arXiv:1609.09076.** The
  space weather of Proxima b; a strong ordered planetary magnetic field could
  shield the atmosphere, but protection is uncertain. (No separate 2017 Proxima
  journal paper exists — only a conference abstract.) Gate 2.

- **Meadows, V. S. et al. (2018)** — *Astrobiology* 18, 133. **arXiv:1608.08620.**
  Enumerates the plausible environmental/atmospheric end-states of Proxima b
  (desiccated, CO₂, Venus-like, habitable) — the branching set a tie-break selects
  among. Gate 2.

- **Schaefer, L. et al. (2017)** — *ApJ* 843, 120. **No arXiv preprint found.**
  "Redox States of Initial Atmospheres Outgassed on Rocky Planets": initial
  atmosphere redox (oxidized CO₂/H₂O vs reduced CH₄/H₂/CO) from the outgassing
  material's oxidation state. Gate 3, sets composition → μ.

- **Herbort, O. et al. (2020)** — *A&A* 636, A71. **arXiv:2003.03628.** "The
  atmospheres of rocky exoplanets. I": chemical equilibrium between crustal rock
  types and the outgassed atmosphere — the gas inventory a given crust yields.
  Gate 3.

- **Wogan, N. et al. (2020)** — *PSJ* 1, 58. **arXiv:2009.07761.** Volcanism on a
  reduced rocky planet can sustain an **abundant CH₄** atmosphere — the reduced-
  redox endmember opposite the CO₂/N₂ default. Gate 3.

- **Wordsworth, R. & Kreidberg, L. (2022)** — *Annual Review of Astronomy &
  Astrophysics* 60, 159. **arXiv:2112.04663.** The canonical review of rocky-
  exoplanet atmospheres: retention, escape, outgassing, observability. Read first.

- **Greene, T. P. et al. (2023)** — *Nature* 618, 39. **arXiv:2303.14849.** JWST
  thermal emission of TRAPPIST-1 b consistent with a **bare rock / no thick
  atmosphere** — empirical confirmation that M-dwarf inner-HZ worlds can be
  stripped. The "existence bound, not pressure measurement" of §1.

- **Zieba, S. et al. (2023)** — *Nature* 620, 746. **arXiv:2306.10150.** **No thick
  CO₂ atmosphere** on TRAPPIST-1 b from JWST — a presence/absence bound, again not
  a surface-pressure measurement.

---

## Related

- `docs/reference/tidally-locked-temperature-methodology.md` — the sibling recipe
  for the temperature `T` that enters the scale-height formula here (§6); the
  Proxima b ~250–290 K range used in the worked example comes from its Layer-3 GCM
  anchors (Turbet+ 2016, Boutle+ 2017).
- `docs/reference/solar-system-external-observer.md` — the Teq-blind-to-greenhouse
  calibration that motivates the "we don't measure the atmosphere" caution in §1
  (Venus' surface conditions are invisible to the kind of data we have here).
- Phase 3 synthesis skill (`nearstars-phase3`) — where the chosen surface pressure,
  composition, μ and H are recorded per planet and the retention-gate justification
  is pinned to the Phase 4 board.
