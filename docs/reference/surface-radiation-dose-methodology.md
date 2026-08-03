<!-- 항성 플레어 입자가 대기 기둥을 통과해 지표에 남기는 방사선 선량을 도출하는 방법(논문 근거) -->
# Surface radiation dose grounding: stellar particle events through an atmospheric column

Method reference for the dose a **surface** receives, as distinct from the trapped-belt
dose that [`planetary-magnetosphere-geometry-methodology.md`](planetary-magnetosphere-geometry-methodology.md)
owns. Those are different chains: belts are about particles a magnetosphere *captures*,
while this doc is about particles that arrive from the star, shower through whatever
atmosphere is above the ground, and deposit energy where a lander stands.

This matters for NearStars because most of our terrestrial targets orbit flare-active M
dwarfs at a few hundredths of an AU. "The surface is hostile" is easy to assert and
easy to get wrong by orders of magnitude, and the answer drives the gameplay hazard
layer (Kerbalism dose zones, EVA limits) rather than the visual layer.

## The relation

Three inputs decide the number, and they are not equally important.

**1. The event.** There are no measurements of charged-particle emission from any star
other than the Sun, so the standard practice is to use the 70 well-characterised major
solar proton events (SPEs) of 1956–2012 as spectral proxies and scale their fluence.
Dose scales **linearly with fluence** at fixed spectrum, because the transport code
tracks one particle at a time.

**2. The spectrum, which matters as much as the fluence.** At a *fixed* fluence of
10⁹ protons cm⁻², the surface dose across those 70 events varies by about **five orders
of magnitude**. Only the hard end of the spectrum reaches the ground: particles below
roughly 0.5 GeV do not contribute to surface dose at all, and above the 290 MeV pion
threshold the shower becomes hadronic, which is why analytic solutions fail and the
literature uses GEANT4 Monte Carlo.

**3. The shielding, atmosphere first and magnetic field second.** Both scale as power
laws, and the atmosphere dominates:

    dose  ∝  C^(−p)        C = atmospheric column density [g cm⁻²]
    dose  ∝  B^(−1.48)     B = planetary field in Earth units

The field exponent comes straight from Atri 2020's stated result, "the dose is reduced
by a factor of about 30 corresponding to an increase in the magnetospheric strength by
an order of magnitude" (10^1.48 ≈ 30). The column exponent needs care — see Validation.

**The column, from board values.** Phase 4 carries pressure and gravity, not column
density, so convert:

    C [g cm⁻²]  =  0.1 · P [Pa] / g [m s⁻²]

## Practical formula

    dose(C, B, Φ, spectrum)  =  dose_ref · (C/C_ref)^(−p) · (B/B_ref)^(−1.48) · (Φ/Φ_ref)

Anchor on a published case rather than deriving absolutely, exactly as the dynamo doc
anchors on tabulated dipoles. The two usable anchors from Atri 2020, both for a 1-hour
10 GeV monoenergetic event:

| column | dose per event |
|---|---|
| 30 g cm⁻² | 1.23 Gy |
| 1000 g cm⁻² | 1.3 × 10⁻³ Gy |

For context on what the numbers mean: ~1 Gy is harmful to mammals, 7–10 Gy was the
dose 1 km from the hypocentre at Hiroshima and Nagasaki, and ~100 Gy is the survival
scale for radioresistant extremophiles.

## Validation

- **The transport is calibrated against a real surface.** Atri 2020 reproduce the
  Mars Science Laboratory RAD instrument's measured GCR background of
  **210 ± 40 µGy/day** with a modelled **218.5 µGy/day**, using the BON10 GCR spectrum
  and the Mars Climate Database atmosphere. That is the only in-situ anchor available
  for this chain, and it is within the measurement uncertainty.
- **The column exponent is internally inconsistent in the source, and you must know
  which one you are using.** Atri 2020's conclusion states "radiation dose is reduced by
  3 orders of magnitude corresponding to an increase in the atmospheric depth by an
  order of magnitude", i.e. `p = 3`. But that paper's own two tabulated anchors give

      p = log(1.23 / 1.3e-3) / log(1000 / 30) = 2.98 / 1.52 = 1.95

  i.e. `p ≈ 2` for the hard 10 GeV case. The likely reading is that `p = 3` describes a
  softer SPE spectrum, whose particles are stopped far more effectively by added column,
  while a 10 GeV beam punches through. **Practical rule: quote a range spanning
  `p = 2` to `p = 3`, and say which anchor the number came from.** A single-point dose
  claim from this chain is not defensible.
- **Direction checks.** Thinner atmosphere → higher dose; weaker field → higher dose;
  closer orbit → higher fluence. All three hold in Atri 2017's and 2020's tables, and
  the field term is always the weaker of the two shielding terms.

## Domain of validity, and what this recipe does not do

1. **Composition barely matters, column does.** Atri 2020 use Earth's atmospheric
   composition throughout and treat only the depth as free, because dose depends on the
   column density rather than on the chemistry (unlike photochemistry or escape, where
   composition is the whole question).
2. **The magnetic field enters only as a filter function.** The shielding is applied as
   an energy-dependent entry probability from Grießmeier 2015, not as a modelled
   magnetosphere. A body with a genuinely exotic field geometry is outside what the
   1.48 exponent describes.
3. **GCR background is a separate, additive term.** For thin atmospheres and weak
   fields the galactic-cosmic-ray background is itself significant, and
   Grießmeier 2016 is the reference for it (including the result that up to 20 % of
   stratospheric ozone can be destroyed, which couples back into UV at the surface).
   SPE dose is episodic on top of that continuous floor.
4. **Fluence for superflares is extrapolated, not observed.** The linear
   flare-energy-to-fluence scaling is acknowledged in the source as the dominant
   uncertainty, and some models argue strong stellar magnetic fields may actually
   *suppress* particle escape in superflares. Treat superflare doses as order-of-magnitude.
5. **Subsurface is out of scope**, but is the obvious mitigation: shielding scales with
   the column of rock or water overhead, on the same physics.

## Worked example: Proxima Cen b at 0.3 bar

Board values: pressure 0.3 bar, gravity 10.5 m s⁻², field weak (≲ 0.1–0.3 × Earth).

    C = 0.1 · 30000 / 10.5 = 286 g cm⁻²      (1 bar would be 952)

Scaling the Phase 3 anchor of ~5 Sv/yr at a 1 bar column, with the field term left at
the board's weak value rather than Earth's:

| column exponent | dose multiplier vs 1 bar | annual dose |
|---|---|---|
| p = 2 | 10.6 × | ~53 Sv/yr |
| p = 3 | 37 × | ~185 Sv/yr |

Either end is far past the ~1 Gy mammalian harm threshold and into the extremophile
band, which is the decision-relevant conclusion: **at 0.3 bar the surface is a hard
radiation environment by tens to hundreds of Sv per year, and the hazard is continuous
rather than event-limited.** The board should carry the range and the exponent
ambiguity, not a single number. Note also that the 5 Sv/yr Phase 3 starting point is
itself flagged low-confidence (a conversion estimate from Atri's per-event Grays), so
this is a two-stage estimate and the honest statement is an order of magnitude.

For the fiction layer this reads as: no habitability question (the board already has the
planet lifeless), but a serious EVA and habitat-shielding constraint, and the reason the
night side and any subsurface volume are the interesting places to put a base.

## Citations

- **Atri 2020**, MNRAS 492, L28 ([`2020MNRAS.492L..28A`](https://ui.adsabs.harvard.edu/abs/2020MNRAS.492L..28A),
  arXiv **[1910.09871](https://arxiv.org/abs/1910.09871)**, **cached** in
  `docs/phase3/_papers/1910.09871.md`). The primary source: GEANT4 transport of 70 SPE
  spectra, the column and field scalings, the Mars RAD validation, and the Proxima b /
  TRAPPIST-1 tables. Also the source of the internal `p = 2` vs `p = 3` tension above.
- **Atri 2017**, MNRAS 465, L34 ([`2017MNRAS.465L..34A`](https://ui.adsabs.harvard.edu/abs/2017MNRAS.465L..34A),
  arXiv **[1606.07027](https://arxiv.org/abs/1606.07027)**). The earlier, wider
  parameter sweep over column depth, magnetic moment and orbital radius; the conclusion
  that superflare dose on a shielded close-in planet is an extinction-level rather than
  a sterilising event.
- **Grießmeier 2016**, A&A 587, A159 ([`2016A&A...587A.159G`](https://ui.adsabs.harvard.edu/abs/2016A%26A...587A.159G),
  arXiv **[1603.06500](https://arxiv.org/abs/1603.06500)**). The galactic-cosmic-ray
  surface-dose floor for weakly magnetised Earth-like planets, plus the ozone
  destruction that couples this chain to surface UV. Paper I of the pair supplies the
  magnetospheric filter functions Atri's transport uses.
- **Hassler 2014** (MSL RAD surface measurements) and **O'Neill 2010** (BON10 GCR
  model) are the calibration inputs inside Atri 2020; cited there rather than used
  directly here.

## Related

- [`planetary-magnetosphere-geometry-methodology.md`](planetary-magnetosphere-geometry-methodology.md)
  — the trapped-belt dose and its Kerbalism mapping. Different chain, different physics:
  that doc is about captured particles, this one about particles reaching the ground.
- [`rocky-planet-dynamo-methodology.md`](rocky-planet-dynamo-methodology.md) — supplies
  the `B` this recipe needs, and the reason a tidally locked slow rotator has little of it.
- [`exoplanet-atmosphere-methodology.md`](exoplanet-atmosphere-methodology.md) — supplies
  the pressure that becomes the column, and treats the same stellar particle flux as an
  atmospheric *loss* term rather than a surface dose.
- [methodology-index](methodology-index.md) — the living index of all derived-value recipes.
