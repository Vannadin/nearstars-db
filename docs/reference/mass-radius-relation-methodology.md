<!-- 관측된 질량 또는 반경에서 나머지 하나를 조성-근거 질량-반경 관계로 도출하고 밀도 정합성을 검증하는 방법론 레퍼런스 -->
# Mass–Radius Relation Methodology — Assigning the Missing M or R, and Gating Density

> Source: synthesis of the planetary mass–radius literature — the physical
> interior grids (Seager+ 2007, Fortney+ 2007, Zeng+ 2016, Baraffe+ 2008), the
> empirical/probabilistic relations (Weiss & Marcy 2014, Chen & Kipping 2017,
> Otegi+ 2020), and the radius-valley classification work (Rogers 2015, Fulton+
> 2017, Van Eylen+ 2018).
> Citations resolved against NASA ADS (the registered `ADS_API_TOKEN`), not
> ad-hoc web search; verified arXiv id where one exists, otherwise the
> authoritative ADS bibcode.
> Purpose: a reusable recipe for **assigning the unobserved one of {mass,
> radius}** from the observed one using a composition-grounded mass–radius
> relation, and for using the resulting **density as a consistency gate** that
> rejects unphysical composition choices.
> This is a working reference, not a textbook — see §8 for the verified citations.

## Scope

This doc does exactly two jobs:

1. **Assign the missing quantity.** An RV planet gives a (true) mass but no
   radius; a transiting planet gives a radius but often no mass. The mass–radius
   relation supplies the other one, conditioned on a composition.
2. **Gate density/composition consistency.** Given a curated (M, R, g) triple —
   which may be over-determined or art-chosen — the M–R relation plus the implied
   bulk density is the check that rejects unphysical options (e.g. a "rocky" moon
   so dense it would have to be a super-Mercury iron ball).

It is **not** the orbit (Keplerian / binary-epoch pipeline), **not** the
atmosphere (`exoplanet-atmosphere-methodology.md`), and **not** the magnetic
field (`planetary-dynamo-scaling.md`). It feeds those: surface gravity and scale
height need R; the giant-dynamo law (B ∝ (M·L²/R⁷)^(1/6)) needs R for every
**non-transiting** giant — and this doc is where that R comes from. The output is
a radius (or mass), a surface gravity, a bulk density, and a rocky-vs-volatile
classification, each with a stated composition assumption.

## Table of Contents

1. [Why One of M, R Is Almost Always Missing](#1-why-one-of-m-r-is-almost-always-missing)
2. [The Composition Grids — the Physical M–R Curves](#2-the-composition-grids--the-physical-mr-curves)
3. [The Rocky Scaling and Where It Turns Over — Domain of Validity](#3-the-rocky-scaling-and-where-it-turns-over--domain-of-validity)
4. [The Relation Is a Band, Not a Line](#4-the-relation-is-a-band-not-a-line)
5. [The Radius-Valley Classification Gate](#5-the-radius-valley-classification-gate)
6. [The Density Consistency Gate](#6-the-density-consistency-gate)
7. [Worked Examples](#7-worked-examples)
8. [Annotated Bibliography](#8-annotated-bibliography)
9. [Related](#related)

---

## 1. Why One of M, R Is Almost Always Missing

The two ways we discover a NearStars planet measure **different** quantities:

- **Radial velocity** returns the **mass** (a minimum mass `M sin i`, promoted to a
  true mass via the isotropic-inclination prior — see the temperature/atmosphere
  docs) and **nothing about the radius**. The planet never crosses the stellar disk.
- **Transit** returns the **radius** (the depth of the dip) and **nothing about the
  mass** unless an independent RV or TTV measurement is folded in.

So for almost every curated body we have one of {M, R} and must **assign the
other**. There is no measurement that returns it — the assignment is a *principled
choice conditioned on an assumed composition*, exactly the same honesty as the
atmosphere doc's "the surface pressure is a choice within bounds." The mass–radius
relation is the tool that makes that choice physical and reproducible instead of
ad-hoc.

The relation also runs the other direction as a **gate**: given both M and R (or
M, R and a curated gravity), the implied bulk density `ρ = M / (4/3 π R³)` must be
consistent with a real composition. A triple that demands an impossible
composition is rejected (§6).

---

## 2. The Composition Grids — the Physical M–R Curves

A planet's radius at fixed mass is set by what it is made of. The foundational
theoretical work integrates the equations of hydrostatic structure with
laboratory equations of state for the relevant materials and produces **mass–radius
curves, one per composition**. Two references anchor this:

- **Seager+ 2007** is the foundational paper: it derives M–R relations for
  homogeneous and differentiated solid planets from pure iron, through silicate
  rock (perovskite/MgSiO₃), to water ice, across the full solid-planet mass range,
  and shows the curves are nearly composition-universal in dimensionless form.
- **Zeng+ 2016** is the **canonical practical rocky grid**: M–R curves for
  two-layer (iron core + silicate mantle) planets calibrated on the Preliminary
  Reference Earth Model (PREM), parameterised by **core mass fraction**. The
  "Earth-like" curve (≈ 32.5 % iron by mass, the terrestrial value) is the default
  rocky reference NearStars reads radii off of. Zeng provides a closed-form fit
  good to a few percent below ~8 M⊕.

The ordering of the curves, at any fixed mass, is the physics you must keep
straight (denser material → smaller radius):

| Composition | Relative radius at fixed M | Bulk density vs Earth |
|---|---|---|
| Pure iron (super-Mercury) | smallest | highest (≳ 1.5 ρ⊕) |
| Earth-like rock (≈ 1/3 Fe) | reference | ≈ 1 ρ⊕ (5.5 g/cm³) |
| Pure silicate (Moon/Mars-like, Fe-poor) | larger | lower (~0.7 ρ⊕) |
| Water/ice world (50 % H₂O) | larger still | ~0.5 ρ⊕ |
| H/He envelope (sub-Neptune → giant) | much larger | ≪ Earth |

For the volatile-rich and giant regimes the canonical grid is **Fortney+ 2007**,
which spans **five orders of magnitude in mass** with rock/ice cores plus H/He
envelopes and includes the stellar-irradiation dependence (insolation puffs up a
H/He envelope). **Baraffe+ 2008** carries the H/He interior models from
super-Earth to super-Jupiter and is the reference for the giant regime where the
equation of state becomes electron-degenerate.

A radius read off a composition grid is only as good as the composition
assumption — which is why §4 (the band) and §5 (the classification gate) constrain
*which* curve you are allowed to use.

---

## 3. The Rocky Scaling and Where It Turns Over — Domain of Validity

Across the **rocky** regime the Zeng/Seager grids are well approximated by a power
law:

    R ∝ M^β,   β ≈ 0.27   (Earth-like composition, M ≲ 8 M⊕)

The small exponent is the signature of self-compression: doubling the mass adds
less than 21 % to the radius because the deep interior is squeezed to higher
density. (Pure-iron and pure-rock curves have similar exponents, offset in
normalisation per the table above.) This is the formula to use for the **RV
true-mass → radius tie-break** when the mass says the body is rocky.

But β ≈ 0.27 holds only in one regime. The M–R relation has **four regimes**, and
choosing the wrong one is the dominant error:

1. **Rocky, M ≲ ~6–8 M⊕ (R ≲ ~1.5–1.6 R⊕).** Solid Fe/rock/water grids; R ∝ M^~0.27.
   The radius is a *tight* function of mass once composition is fixed. This is the
   NearStars terrestrial regime (Proxima b, the TRAPPIST-1 worlds, Pandora-class
   moons).

2. **Sub-Neptune / volatile-inflated, ~1.6 ≲ R ≲ ~4 R⊕.** A small mass of H/He or
   a deep water/steam envelope inflates the radius far beyond the rocky grid. Here
   **radius is a poor proxy for mass**: a given radius admits a wide mass range
   because a few percent of H/He by mass dominates the radius (Fortney+ 2007,
   Lopez & Fortney 2014). Use the **probabilistic relation** (§4), not a single
   grid curve.

3. **Giant, ~0.1 ≲ M ≲ ~13 M_J.** The H/He becomes **electron-degenerate**, and
   degeneracy pressure makes the radius **nearly independent of mass** — R sits
   near 1 R_J across roughly a decade in mass (Fortney+ 2007, Baraffe+ 2008).
   Mass therefore *barely* constrains radius and vice versa: for a non-transiting
   giant, adopt R ≈ 1.0–1.2 R_J and treat it as flat, not a power law.

4. **Above the giant peak (≳ 1–4 M_J).** R actually **decreases** with increasing
   mass — added mass compresses the degenerate interior faster than it adds volume
   — until the brown-dwarf / low-mass-star regime. (Irradiation and youth inflate
   the radius and shift this peak; a young or hot-Jupiter giant can exceed 1 R_J
   substantially.)

Mis-applying a rocky exponent to a sub-Neptune (regime 2) over-predicts the mass
by an order of magnitude; applying a power law in the giant regime (3–4) is simply
wrong because the relation is flat-to-decreasing. Pick the regime from the
observed quantity *and* the classification gate (§5) before reading off the other.

---

## 4. The Relation Is a Band, Not a Line

A single (M, R) point is consistent with **multiple compositions** — the curves in
§2 are stacked, and observational scatter plus envelope fraction smears them into
a **band**. This is the central honesty of the M–R method, the analogue of the
atmosphere doc's "principled choice within bounds":

- **In the rocky regime** the band is narrow (a factor ~1.5 in radius from pure
  iron to pure rock), so a rocky mass pins the radius to ~10 % once you commit to
  Earth-like composition. Reading Proxima b off the Earth-like curve is defensible.
- **In the volatile regime** the band is wide — the relation is genuinely a
  scatter cloud, and the right tool is a **probabilistic / empirical** relation fit
  to the observed sample, not a physical grid:
  - **Weiss & Marcy 2014** — an empirical broken power law for planets < 4 R⊕,
    the first widely-used statistical M–R fit.
  - **Chen & Kipping 2017 (Forecaster)** — a probabilistic, broken-power-law M–R
    relation across **four regimes** (dwarf-planet → terrestrial → Neptunian →
    stellar) with quantified intrinsic scatter. It is the right tool when you have
    a mass (or radius) and want a *radius (or mass) with honest error bars* rather
    than a single grid number. The break near ~2 M⊕ marks the terrestrial→Neptunian
    transition.
  - **Otegi+ 2020** — a two-population M–R relation (separate fits for the rocky
    and the volatile-rich populations below 120 M⊕), which makes the
    composition-dependent band explicit: the same radius lands on two different
    mass relations depending on which population the body belongs to.

Practical rule: **physical grid (Zeng) when the body is confidently rocky;
probabilistic relation (Forecaster / Otegi) when it is volatile-rich or
ambiguous.** Always state which curve/relation produced the assigned value and
carry the band as the uncertainty.

---

## 5. The Radius-Valley Classification Gate

Before reading a radius off the *rocky* grid you must confirm the body **is**
rocky. The observed small-planet population has a **bimodal radius distribution**
with a gap — the **radius valley** — that separates two physically distinct
populations:

- **Rogers 2015** — "Most 1.6 Earth-radius planets are not rocky": above
  ~1.6 R⊕ the typical planet has a volatile envelope, not a bare rock surface.
- **Fulton+ 2017** (California-Kepler Survey III) — measures the gap directly: a
  deficit of planets at **~1.5–2.0 R⊕** splits **super-Earths (≲ 1.5 R⊕, rocky)**
  from **sub-Neptunes (~2–3 R⊕, volatile-enveloped)**.
- **Van Eylen+ 2018** — sharpens the valley with asteroseismic stellar radii and
  shows its slope matches **photoevaporation / core-powered mass loss** (Owen & Wu;
  see the atmosphere doc): the sub-Neptunes are **stripped cores**, not "born
  rocky." The valley centre sits near ~1.8 R⊕ and shifts slightly with orbital
  period and stellar mass.

The classification rule for NearStars:

- **R ≲ 1.5 R⊕** → rocky is the default; read mass/radius off the Earth-like Zeng
  grid; expect a secondary (outgassed) atmosphere at most (atmosphere doc Gate 1).
- **R ≳ 1.6–1.8 R⊕** → **statistically NOT rocky.** A "rocky" curated body is not
  allowed up here; a larger radius **forces a volatile (H/He or steam) envelope**,
  which changes the atmosphere assumption (a primordial/thick envelope, not a thin
  outgassed one) and the bulk-density expectation. Do not put an Earth-like surface
  on a 2.5 R⊕ body.
- **In the valley (~1.5–1.8 R⊕)** the body is genuinely ambiguous — flag it and
  carry both readings.

This gate runs *before* §3's regime choice: it tells you whether you are even
allowed to use the rocky power law.

---

## 6. The Density Consistency Gate

When a curated body is **over-determined** — mass *and* radius *and* gravity all
specified, e.g. by art direction or by a fictional canon — the three are coupled by

    g = G M / R²,        ρ = M / (4/3 π R³),

so only two are free. The M–R relation plus the implied **bulk density** is the
gate that rejects the unphysical combination:

1. Compute ρ from whatever pair is fixed.
2. Compare ρ (and R) against the composition grids of §2. If the point sits
   **denser than the pure-iron curve at that radius**, it implies a composition
   more iron-rich than Mercury — physically unreasonable for anything but a
   collisionally-stripped fragment. Reject it.
3. Re-solve for a physical option by **fixing the two most defensible quantities**
   (usually the radius and a target surface gravity, or the radius and an
   Earth-like composition) and letting the third follow.

The canonical NearStars case is the moon **"Pandora"** (consistency-gate worked
example, §7): a canon that implied a bulk density of **~1.2 ρ⊕** at its size was
**rejected as a super-Mercury** — too iron-rich to be a physical body at that
radius. Option B — fix surface gravity at 0.8 g and the radius, solve for mass —
gave **0.645 M⊕** and **~0.89 ρ⊕** (~4900 kg/m³), a realistic Mars-to-Earth rocky
density. The density gate is what turned an arbitrary art number into a defensible
rocky body.

The gate is symmetric with the assignment use: assignment *reads* a radius from a
mass off a chosen curve; the gate *checks* that a given (M, R) doesn't fall off the
edge of the composition family.

---

## 7. Worked Examples

**Proxima b — RV true-mass → radius (rocky tie-break).** Proxima b is
non-transiting: RV gives a minimum mass, promoted to a true mass ~1.22 M⊕ (the
isotropic-prior median; see the temperature doc). The classification gate (§5):
the mass is small, so the body is firmly in the rocky regime (its rocky radius is
well below the ~1.6 R⊕ valley). Read off the **Earth-like Zeng grid**:
1.22 M⊕ → **~1.07 R⊕** (consistent with R ∝ M^0.27: 1.22^0.27 ≈ 1.055). Then
g = G·M/R² ≈ **1.07 g** and ρ ≈ **5.5 g/cm³** (≈ 1 ρ⊕) — a rocky planet, below the
radius valley, so **no H/He envelope** and a secondary atmosphere at most (feeds
the atmosphere doc's Proxima b lake-world: g ≈ 10.5 m/s², H ≈ 7–8 km).

**Pandora — the density consistency gate (frame qualitatively).** A moon whose
canon implied ρ ≈ 1.2 ρ⊕ at its radius. That density at that size lands **denser
than the pure-iron curve** — a "super-Mercury," not a physical rocky moon — so it
was **rejected**. Option B fixes g = 0.8 g and the radius, solving for mass
M = 0.645 M⊕, which gives ρ ≈ 0.89 ρ⊕ (~4900 kg/m³), a realistic Mars↔Earth rocky
body. (Decision lives on the Phase 4 board; the gate reasoning is what matters
here.)

**A sub-Neptune — the relation flattens into a band.** For a transiting ~2.5 R⊕
body the classification gate says **not rocky** (above the valley). Reading a mass
off the rocky grid would give ~10–15 M⊕ and a nonsensical density; the real body
carries a H/He or steam envelope and its mass is **poorly constrained by the
radius** — a few percent of H/He by mass swings the radius across the whole
sub-Neptune range (Fortney+ 2007, Lopez & Fortney 2014). The right tool is the
**probabilistic relation** (Chen & Kipping Forecaster / Otegi volatile population),
which returns a mass *with a wide error band* rather than a false-precision grid
number. The lesson: in this regime the M–R relation is explicitly a band.

**A giant — degeneracy makes R ≈ constant.** For a non-transiting giant (e.g. an
RV/astrometry M sin i near 1 M_J), the mass **barely constrains the radius**:
across ~0.3–4 M_J the H/He interior is electron-degenerate and R ≈ 1.0–1.2 R_J
(Fortney+ 2007, Baraffe+ 2008), flat to slightly decreasing with mass. Adopt
**R ≈ 1.0–1.2 R_J** (raised for youth/irradiation), not a power-law extrapolation.
This is the radius the giant-dynamo doc consumes: B_dip depends on R⁷, so the
flat-degenerate R assignment here directly sets the field there for every
non-transiting giant.

---

## 8. Annotated Bibliography

Each entry: authors, year, journal, **verified** arXiv id (or a flag where none
exists), citation count (ADS, at survey time), and one line on what it contributes.

- **Seager, S. et al. (2007)** — *ApJ* 669, 1279. **arXiv:0707.2895.** (702 cites)
  The foundational theoretical M–R relations for solid exoplanets — pure iron,
  silicate rock, water ice — from first-principles interior structure. §2.

- **Fortney, J. J., Marley, M. S. & Barnes, J. W. (2007)** — *ApJ* 659, 1661.
  **arXiv:astro-ph/0612671.** (949 cites) Planetary radii across **five orders of
  magnitude** in mass: rock/ice cores plus H/He envelopes, including irradiation.
  The canonical grid for the volatile and giant regimes. §2, §3, §7.

- **Baraffe, I. et al. (2008)** — *A&A* 482, 315. **arXiv:0802.1810.** (311 cites)
  Structure and evolution from super-Earth to super-Jupiter — the H/He interior
  models for the degenerate **giant regime** where R turns over. §3, §7.

- **Weiss, L. M. & Marcy, G. W. (2014)** — *ApJ* 783, L6. **arXiv:1312.0936.**
  (587 cites) Empirical broken-power-law M–R relation for planets < 4 R⊕ — the
  first widely-used statistical fit. §4.

- **Rogers, L. A. (2015)** — *ApJ* 801, 41. **arXiv:1407.4457.** (710 cites)
  "Most 1.6 Earth-radius planets are not rocky" — the classification rule that a
  body above ~1.6 R⊕ statistically carries a volatile envelope. §5.

- **Zeng, L., Sasselov, D. D. & Jacobsen, S. B. (2016)** — *ApJ* 819, 127.
  **arXiv:1512.08827.** (399 cites) The canonical practical **rocky grid**:
  two-layer (Fe core + silicate mantle) M–R curves on PREM, parameterised by core
  mass fraction, with a closed-form fit. The default Earth-like curve NearStars
  reads rocky radii off. §2, §3, §7.

- **Chen, J. & Kipping, D. (2017)** — *ApJ* 834, 17. **arXiv:1603.08614.**
  (663 cites) **Forecaster**: a probabilistic, four-regime broken-power-law M–R
  relation with quantified intrinsic scatter — predicts radius from mass (or vice
  versa) with honest error bars. The right tool in the volatile/ambiguous regime. §4.

- **Fulton, B. J. et al. (2017)** — *AJ* 154, 109. **arXiv:1703.10375.**
  (1331 cites) California-Kepler Survey III: measures the **radius valley** — the
  ~1.5–2.0 R⊕ gap splitting rocky super-Earths from volatile sub-Neptunes. §5.

- **Van Eylen, V. et al. (2018)** — *MNRAS* 479, 4786. **arXiv:1710.05398.**
  (496 cites) "An asteroseismic view of the radius valley: stripped cores, not
  born rocky" — sharpens the valley and matches its slope to photoevaporation. §5.

- **Otegi, J. F., Bouchy, F. & Helled, R. (2020)** — *A&A* 634, A43.
  **arXiv:1911.04745.** (250 cites) Revisited two-population (rocky vs volatile-rich)
  M–R relations below 120 M⊕ — makes the composition-dependent band explicit. §4.

---

## Related

- `docs/reference/tidally-locked-temperature-methodology.md` — the temperature
  `T` that, with the surface gravity `g` this doc assigns, sets the scale height in
  the atmosphere doc; rocky-vs-volatile classification (§5) decides which
  temperature/atmosphere branch applies.
- `docs/reference/exoplanet-atmosphere-methodology.md` — radius → surface gravity
  → scale height; the §5 radius-valley gate is the same rocky-vs-sub-Neptune
  boundary that gate-keeps whether the atmosphere is a thin outgassed one or a
  primordial H/He envelope.
- `docs/reference/surface-color-albedo-methodology.md` — the rocky-vs-volatile
  classification and bulk density here constrain the surface/cloud regime that
  color and albedo are assigned from.
- `docs/reference/tidal-heating-methodology.md` — the tidal-heating rate goes as
  R⁵, so the radius assigned here is **high-leverage** for heating; a non-transiting
  body's radius tie-break propagates strongly into its tidal energy budget.
- `docs/reference/planetary-dynamo-scaling.md` — the giant-dynamo law
  B ∝ (M·L²/R⁷)^(1/6) **needs R**; for every non-transiting giant the
  flat-degenerate radius assigned in §3/§7 here is the R that doc consumes.
