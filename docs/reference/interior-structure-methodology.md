<!-- 질량과 조성에서 정수압 평형을 적분해 반지름·핵 경계·관성모멘트·중심압을 내는 방법(논문 근거) — J₂·다이나모·핵 상태의 입력 -->
# Interior structure grounding: integrating the layers instead of assuming them

Method reference for the question underneath the figure, the field and the core: **how is
this body's mass arranged inside it?** The answer is a density profile, and four numbers
fall out of it: the radius, the core boundary, the normalised moment of inertia C/MR², and
the central pressure. None of the four is measurable for anything outside the Solar
System, so all four have to be derived, and the derivation has to say where it stops being
trustworthy.

The consumers are the [body figure](body-figure-methodology.md) recipe, which turns C/MR²
into J₂ through Radau–Darwin; the [rocky-planet dynamo](rocky-planet-dynamo-methodology.md),
which needs the core radius; the [mass–radius relation](mass-radius-relation-methodology.md),
which now takes its radius from here rather than from a power-law fit; and `core_state`,
which will compare the central pressure against a melting curve. A class-table constant in
this slot propagates into J₂, into the Cassini precession constant, into obliquity, and
from there into tidal dissipation, which is why it is worth deriving rather than looking up.

This doc covers the **static** half of an interior: the density profile and what follows
from it. Whether the core is a conducting liquid is a thermal question (`core_state`), and
what k₂ and Q are is a viscoelastic one (`tidal_response`). Different inputs, different
literature, separate recipes.

## What changed on 2026-08-25, and why it had to

Until this revision the recipe assumed **uniform layers** and evaluated two closed-form
expressions. Layer densities came from a composition lookup table, and that table only held
near Earth's mass. The cost was not subtle:

- Earth's C/MR² came out 4.8 % high, and the error only ever pointed one way, because
  uniform layers ignore self-compression and a real interior concentrates mass inward.
- Mercury came back 8.6 % out, and the cause was the table rather than the algebra:
  Mercury's core sits near 7800 kg/m³ where Earth's runs near 10900, the same iron
  differently squeezed. Fitting a power law in mass gave an exponent scattering from 0.10
  to 0.23 across bodies, so there was no single scaling to hide behind.
- The mass–radius recipe carried a second table of composition radius scalings, derived
  from *prose ordering* in its own document rather than from a solved interior, and its
  pure-iron threshold was therefore not a real curve.

Both tables are now gone. Layer density is an output of the integration, not an input to
it, and the pure-iron curve is an integration of a published iron equation of state. Earth's
C/MR² error dropped from 4.8 % to 0.3 %.

Later the same day the water ice column was completed. The revision above left a named hole
between 209.5 MPa and 2.216 GPa, where ices III, V and VI belong, and returned it as a
result whenever an ice column reached into it. Three phases now fill it, read from a
published Gibbs representation rather than fitted, so the ladder runs unbroken from ice Ih
to ice VII. Chaos (Alpha Centauri A b V) was the body the hole was blocking and it solves;
Ganymede, whose water column bottoms out inside ice VI, is what shows the phases carrying a
measured body rather than merely unblocking a search.

## Contract — `interior_layers`

**Returns** — `nmoi` [—] · `core_radius_fraction` [—] · `core_radius` [R_earth] ·
`radius` [R_earth] · `core_pressure` [GPa]
**Needs** — `mass_earth` [M_earth] · `core_mass_fraction` [—] · `ice_mass_fraction` [—] ·
`composition` [—] · `differentiated` [—] · `body_class` [—] · `radius_earth` [R_earth]
**Discriminating keys** — the material stack chosen by `composition`, and the pressure
reached at each layer boundary, which decides whether a grounded phase exists there.
Regimes and their numeric conditions are in [Domain of validity](#domain-of-validity).
**Grade** — calibrated. The equations of state are published fits, and the recipe
reproduces four measured moments of inertia without being handed layer densities.

`radius_earth` is **not used to compute anything**: radius is an output. When supplied it
is compared against the derived radius, so a composition declaration that fails to
reproduce a known body says so instead of passing quietly. The inversion below is what
consumes it for real.

This block is checked against the code: `engine/check_contracts.py` compares what is
declared here with what `interior_layers` actually consumes and produces at run time, so
the two cannot drift.

## The relation

A body in hydrostatic equilibrium satisfies mass conservation and the balance of pressure
against self-gravity, closed by an equation of state. These are Seager+ 2007's equations
(1) to (3) ([arXiv:0707.2895](https://arxiv.org/abs/0707.2895)):

    dm/dr = 4π r² ρ(r)
    dP/dr = −G m(r) ρ(r) / r²
    ρ     = ρ(P)                        ← the equation of state, per material

The moment of inertia integrates alongside them,

    dI/dr = (8/3)π r⁴ ρ(r)      →      C/MR² = I / (M R²)

The system is a two-point boundary-value problem: pressure is unknown at the centre and
must vanish at the surface. It is solved by shooting. Guess a central pressure, integrate
outward until P reaches zero, read off the radius and the enclosed mass, and adjust the
guess until the enclosed mass matches the mass asked for. Total mass increases
monotonically with central pressure, so the bracket never fails; the implementation uses a
secant step in log–log with a bisection fallback, because one integration is expensive and
the iteration count is the cost.

Layer boundaries are placed in **mass**, not radius: the core occupies the innermost
`core_mass_fraction` of the target mass, the ice shell the outermost `ice_mass_fraction`,
and the mantle whatever is left. Using the target mass rather than the running mass keeps
the boundaries fixed across shooting iterations, which is what preserves monotonicity.

Two limits are worth holding onto. A uniform sphere has C/MR² = 2/5 exactly, and a body
with no core, no ice and no compression would land there. Every mechanism in this
document (a dense core, self-compression, or both) pushes the value **down**, and the
deeper it sits below 0.4 the more mass is hiding in the middle. Earth at 0.3307 is the
familiar calibration point.

### The equations of state

Three functional forms appear, and which one a material uses was decided by whoever fitted
it, not by us.

**Second-order Birch–Murnaghan (BM2)**, with K₀′ fixed at 4. This is the form Zeng+ 2016
fit PREM with ([arXiv:1512.08827](https://arxiv.org/abs/1512.08827), their eq. 1):

    P = (3/2) K₀ [ (ρ/ρ₀)^(7/3) − (ρ/ρ₀)^(5/3) ]

**Third-order Birch–Murnaghan (BME3)**, which frees K₀′, and **Vinet**, which Seager+ 2007
§III.1 prefers for extrapolation above the experimental range because BME is a truncated
expansion of the elastic potential energy. Both are in Seager's Table 1.

The materials, with the source of every constant:

| material | form | ρ₀ (kg/m³) | K₀ (GPa) | K₀′ | valid range | source |
|---|---|---|---|---|---|---|
| `fe_prem` (planet core) | BM2 | 7050 | 201 | 4 | 0 to 12 TPa | Zeng+ 2016 §II, PREM outer-core fit |
| `fe_eps` (pure iron limit) | Vinet | 8300 | 156.2 | 6.08 | 0 to 20.9 TPa | Seager+ 2007 Table 1, Fe(ε), Anderson+ 2001 data |
| `mgsio3_en` (upper mantle) | BME3 | 3220 | 125 | 5 | 0 to 23.83 GPa | Seager+ 2007 Table 1, MgSiO₃ enstatite |
| `mgsio3_prem` (lower mantle) | BM2 | 3980 | 206 | 4 | 23.83 GPa to 3.5 TPa | Zeng+ 2016 §II, PREM lower-mantle fit |
| `ice_ih` | BM2 | 916.72 | 8.490 | 4 | 0 to 209.5 MPa | IAPWS-06 (Feistel & Wagner 2006) Table 6 |
| `ice_iii` | BME3 | 1126.384 | 7.8349 | 6.7097 | 209.5 to 355.0 MPa | SeaFreeze v1.1.0 (Journaux+ 2020), evaluated at P = 0, T = 251.15 K |
| `ice_v` | BME3 | 1207.842 | 10.6368 | 6.7460 | 355.0 to 618.4 MPa | SeaFreeze v1.1.0 (Journaux+ 2020), evaluated at P = 0, T = 256.43 K |
| `ice_vi` | BME3 | 1263.386 | 10.3686 | 7.8219 | 618.4 MPa to 2.216 GPa | SeaFreeze v1.1.0 (Journaux+ 2020), evaluated at P = 0, T = 272.73 K |
| `ice_vii` | BME3 | 1460 | 23.7 | 4.15 | 2.216 to 37.4 GPa | Seager+ 2007 Table 1, Hemley+ 1987 data |

Five things about that table are worth stating out loud, because each of them is a
decision rather than a transcription. Every row carries both ends of its validity range,
which is the property that lets the solver say *where* it stopped rather than only *that*
it stopped.

**`fe_prem` has a lower ρ₀ than pure iron, and that is the content, not a defect.** Earth's
core carries roughly 10 % light elements and sits on a hot geotherm. Both effects are
already inside the effective ρ₀ that Zeng+ 2016 obtained by fitting PREM, which is why an
isothermal integration with this material reproduces Earth. The recipe is not ignoring
temperature: it is using an equation of state calibrated on a real, hot planet. `fe_eps` is
the opposite object, a cold laboratory iron with no light elements, and it exists only to
draw the "nothing can be denser than this" limit that the density gate needs.

**The mantle is two materials, not one.** Earth's upper-to-lower mantle transition sits at
23.83 GPa with a 10 % density jump from 4.0 to 4.4 g/cc (Zeng+ 2016 §II.1). Below it the
recipe uses Seager's enstatite fit, above it the PREM lower-mantle fit. Evaluated at the
transition the two give 3688 and 4379 kg/m³, so the jump the code produces is the jump the
paper describes. Bodies smaller than Mars never reach the transition and are enstatite all
the way down.

**Ice Ih's two constants come from IAPWS-06's own check table.** At T = 273.152519 K and
p = 101 325 Pa the release tabulates ρ = 916.721463419 kg/m³ and κ_T = 1.17785291765 ×
10⁻¹⁰ Pa⁻¹, and the isothermal bulk modulus is the reciprocal of the latter, 8.490 GPa.
K₀′ is not in that table, so the recipe uses BM2, which fixes it at 4. That choice is
harmless here and the test proves it rather than asserting it: across the entire range
where ice Ih exists the compression only reaches 2.4 %, and moving K₀′ from 4 to 6 changes
the density at the phase boundary by 0.05 %.

**The window between 209.5 MPa and 2.216 GPa used to be a hole, and how it closed is
worth recording.** Along the melting curve, water leaves ice Ih at 209.5 MPa / 251.15 K,
leaves ice III at 355.0 MPa / 256.43 K, leaves ice V at 618.4 MPa / 272.73 K, and leaves
ice VI for ice VII at 2.216 GPa / 355 K. The first three triple points are Choukroun &
Grasset 2007's and the fourth is Daucik & Dooley 2011's; all four are read from Zeng &
Sasselov 2013 §III.3.1 ([arXiv:1301.0818](https://arxiv.org/abs/1301.0818)), which adopts
the same set for its planet models and is the source the ice Ih and ice VII gates already
came from. Using one consistent set for all four boundaries is deliberate: the Ih boundary
at 209.5 MPa is load-bearing for the roster below, and mixing sources would move it for no
gain.

What was missing was never the boundaries. It was the three equations of state, whose
coefficients sit in Choukroun & Grasset 2007/2010 and Bezacier+ 2014, none of which we
could obtain in full text (they still cannot be, and the request stands). The coefficients
in the table above come from somewhere else, and they are not a fit to anybody's data.

### Reading the three ice phases instead of fitting them

SeaFreeze v1.1.0 carries Gibbs-energy representations of ices Ih, II, III, V, VI and VII/X
(Journaux+ 2020, [`2020JGRE..12506176J`](https://ui.adsabs.harvard.edu/abs/2020JGRE..12506176J),
DOI [10.1029/2019JE006176](https://doi.org/10.1029/2019JE006176)). A Gibbs representation
returns state properties, so ρ, K_T and K′ can be **evaluated** at a stated reference point
rather than transcribed from a table of fitted parameters. Those three numbers are exactly
what a third-order Birch–Murnaghan form takes. This is the construction ice Ih already
used, one row up: read ρ and κ_T at a reference state from a released equation of state,
and put them into a Birch–Murnaghan form. The difference is only that ice Ih's reference
state was published as a check table and these are computed from the released
representation.

The reference state is **P = 0 at the temperature of the triple point where the phase
begins**: 251.15 K for ice III, 256.43 K for ice V, 272.73 K for ice VI. One rule for the
three of them, and the same idea as reading ice Ih at its normal-pressure melting point.
Zero pressure is a metastable extrapolation for all three phases, which is standard for
high-pressure ice parameters and is inside the representation's own knot domain rather than
beyond it (the ice III spline runs to 500 MPa, ice V to 1 GPa, ice VI to 3 GPa, each from
P = 0).

Whether that is good enough is a measurement, not an opinion. Rebuilding each phase's
density curve from its three constants and comparing against the representation it came
from, across the phase's whole stability window, gives **0.006 % for ice III, 0.014 % for
ice V and 0.118 % for ice VI**. There was no accuracy left for a least-squares refit to
buy, so none was done.

**Temperature is the real error bar here, and it is stated rather than hidden.** These are
isothermal forms on a melting curve that rises through each window. At the top of its
window each phase is denser on its reference isotherm than on the melting curve by 0.11 %
(ice III), 0.27 % (ice V) and 1.3 % (ice VI). Ice VI's window spans 82 K, which is why it
carries ten times the others' spread, and 1.3 % is this material's honest width. A colder
body's ice VI is denser than the reference isotherm rather than lighter, so the bias does
not point one way for all bodies.

**SeaFreeze is not a runtime dependency, and that was a decision.** Every other material in
`engine/eos.py` is a set of constants with a citation, and `scripts/check.sh` has to run on
the system interpreter without a scientific stack. So the coefficients are baked in, and
SeaFreeze is used two ways instead: once to produce them, and thereafter as a cross-check
that `engine/test_interior.py` runs **only when the package is importable**, printing SKIP
otherwise. That check re-reads all three phases at their reference states and fails if a
baked constant has drifted from the representation, which is the protection a hand-copied
table needs (this repository has been 54× wrong in a hand-keyed table before). The
development environment that reproduces it is pinned in `engine/requirements.txt`.

## Practical recipe

1. **Choose the material stack** from `composition`. Four are defined: `earth_like`
   (CMF 0.325), `iron` (pure Fe(ε)), `silicate` (no metal), and `water` (50 % H₂O over an
   Earth-like rock). Numeric fractions passed explicitly override the preset.
2. **Refuse the undifferentiated case.** `differentiated: false` is declined by name, and
   it is not the same statement as CMF = 0. See [Domain of validity](#domain-of-validity).
3. **Bracket the central pressure** from the uncompressed radius, capped at the innermost
   material's validity ceiling. Above that ceiling the physics is electron degeneracy
   (Thomas–Fermi–Dirac, Seager+ 2007 §III.2), which this recipe does not carry.
4. **Shoot.** Integrate the four equations outward with fourth-order Runge–Kutta on 1500
   steps, switching material at the mass boundaries, and iterate on central pressure until
   the enclosed mass matches to 10⁻⁸ relative. Convergence is a **returned flag**, not an
   exception.
5. **Report** the radius, the core boundary in both fraction and absolute terms, the moment
   of inertia and the central pressure, together with the phase sequence the column
   actually passed through.

### Inverting it: composition from mass and radius

Most moons arrive with a mass and a radius and no composition declaration, which
over-determines the problem: the two observations fix one free fraction. Pure silicate is
the baseline. A body denser than that baseline needs metal, so the recipe solves for the
core mass fraction; a body less dense needs ice, so it solves for the ice mass fraction.

The axis is **scanned before it is bisected**. Bisecting straight away will eventually
probe a value inside the phase gap and stop there, and nothing then distinguishes "the
answer is unreachable" from "a trial point happened to land in a hole". Scanning first
means the recipe can say which of the two it is, and that distinction is the whole point of
the exercise for the low-density moons below.

**The inversion is not unique, and the result says so.** At the pressures small bodies
reach, void space survives, and porosity and ice lower the mean density in the same
direction. An icy body at 30 % ice and a less icy body at 15 % ice with 15 % porosity are
not distinguished by mass and radius alone. Separating them needs a compaction model, which
is out of scope here, so every inverted result carries the degeneracy in its notes and is
graded **analog** rather than calibrated.

## Validation

Reproduced against four measured bodies. Radii are geodetic; the moments of inertia come
from gravity fields or precession, not from models. **No layer densities are supplied**:
the inputs are mass and core mass fraction, the latter taken from standard geochemical and
gravity-field values rather than tuned to make the answer come out.

| body | R derived | R published | ΔR | C/MR² derived | published | error | f derived | f published | P_c (GPa) |
|---|---|---|---|---|---|---|---|---|---|
| Earth | 1.0029 | 1.0000 | +0.3 % | 0.3297 | 0.3307 | 0.3 % | 0.546 | 0.546 | 358.6 |
| Mars | 0.5317 | 0.5320 | -0.1 % | 0.3545 | 0.3644 | 2.7 % | 0.492 | 0.540 | 45.9 |
| Mercury | 0.3821 | 0.3829 | -0.2 % | 0.3388 | 0.3460 | 2.1 % | 0.795 | 0.828 | 38.2 |
| Moon | 0.2739 | 0.2727 | +0.4 % | 0.3945 | 0.3931 | 0.3 % | 0.206 | 0.201 | 5.7 |

**Earth is the load-bearing row.** Self-compression is exactly what the uniform-layer model
left out, so Earth, the most compressed of the four, is where its absence showed most: 4.8 %
before, 0.3 % now. Radius is reproduced to 0.3 % from mass and core mass fraction alone,
which was not something the old model could even attempt.

The residual 2–3 % on Mars and Mercury is not compression. Both bodies sit below the
23.83 GPa mantle transition, so their entire mantle is the enstatite fit, whose zero-pressure
density (3220 kg/m³) is lower than a real olivine-dominated upper mantle; and both have core
mass fractions that are themselves model-derived to a few hundredths. Mercury's derived core
boundary at 0.795 against a measured 0.828 is the same statement in geometry.

**A second number checks the depth, not just the totals.** C/MR² is an integral, so a
profile that is wrong in two places can still land on the right answer; the pressure at a
named boundary cannot. PREM puts Earth's core-mantle boundary at 3480 km depth and
**135.8 GPa**. The integration puts it at **135.2 GPa**, 0.4 % out, which says the profile
is right where it is deepest and not merely right on average.

A third check runs against a published curve rather than against a body. Zeng+ 2016
eq. 2 gives R/R⊕ = (1.07 − 0.21·CMF)·(M/M⊕)^(1/3.7) for 1–8 M⊕ and CMF 0–0.4, quoting
agreement with their own model curves to about 0.01 R⊕:

| M (M⊕) | CMF | this recipe | Zeng+ 2016 eq. 2 | difference |
|---|---|---|---|---|
| 1.0 | 0.325 | 1.0029 | 1.0018 | 0.0011 |
| 1.0 | 0.000 | 1.0706 | 1.0700 | 0.0006 |
| 2.0 | 0.300 | 1.2223 | 1.2145 | 0.0078 |
| 4.0 | 0.200 | 1.5044 | 1.4952 | 0.0092 |

### The ice ladder, checked twice

The three new phases need two different kinds of check, because two different things could
be wrong: the constants could have been copied wrong, or the whole construction could be
wrong.

**Against the source.** Ice Ih is the control, because both this recipe and SeaFreeze take
it from IAPWS-06. Evaluated at the IAPWS-06 check state (273.152519 K, 101 325 Pa) the
representation returns 916.721463427 kg/m³ against the released 916.721463419, agreeing to
nine significant figures. That agreement is what licenses reading the other three phases
from the same representation. On top of it, each phase's constants are re-read at their
reference states and compared with what is baked into the code, and each phase's rebuilt
density curve is compared against the representation across its window:

| phase | reference state | ρ₀ (kg/m³) | K₀ (GPa) | K₀′ | window | curve reproduced to |
|---|---|---|---|---|---|---|
| `ice_iii` | P = 0, T = 251.15 K | 1126.3840 | 7.8349 | 6.7097 | 209.5 to 355.0 MPa | 0.006 % |
| `ice_v` | P = 0, T = 256.43 K | 1207.8419 | 10.6368 | 6.7460 | 355.0 to 618.4 MPa | 0.014 % |
| `ice_vi` | P = 0, T = 272.73 K | 1263.3858 | 10.3686 | 7.8219 | 618.4 MPa to 2.216 GPa | 0.118 % |

One published number anchors the representation itself rather than our use of it. SeaFreeze
publishes a single-point output for ice VI at 900 MPa and 255 K, ρ = 1356.1 kg/m³, and the
installed package returns 1356.07. Our ice VI sits on the 272.73 K isotherm, so at the same
pressure it gives 1351.06, 0.37 % below the published point. That difference is the
temperature width described above, showing up where it should.

A second, independent agreement is worth noting because nobody arranged it. SeaFreeze
locates the melting-curve triple points from its own Gibbs energies, at 207.59, 350.11 and
634.40 MPa. The boundaries this recipe uses come from Choukroun & Grasset 2007 instead, at
209.5, 355.0 and 618.4 MPa. The two sets agree to 0.9 %, 1.4 % and 2.6 %, which is a
consistency check between two literatures rather than within one.

**Against measured moons.** The construction is only worth anything if the phases carry a
real body. Inverting five Solar System icy satellites from mass and radius alone:

| moon | ρ̄ (kg/m³) | ice fraction | ice-column base | C/MR² derived | published | error | source |
|---|---|---|---|---|---|---|---|
| Ganymede | 1936 | 0.407 | 1.51 GPa (ice VI) | 0.3179 | 0.3115 | 2.1 % | Schubert+ 2004 (Anderson+ 1996) |
| Callisto | 1834 | 0.444 | 1.28 GPa (ice VI) | 0.3158 | 0.3549 | 11.0 % | Anderson+ 2001 |
| Titan | 1880 | 0.434 | 1.48 GPa (ice VI) | 0.3172 | 0.3414 | 7.1 % | Iess+ 2010 (Cassini) |
| Europa | 3014 | 0.033 | 0.0709 GPa (ice Ih) | 0.3789 | 0.3460 | 9.5 % | Anderson+ 1998 |
| Enceladus | 1610 | 0.398 | 0.00967 GPa (ice Ih) | 0.3051 | 0.3350 | 8.9 % | Iess+ 2014 (Cassini) |

**Ganymede is the row that matters, and it is the gate in the test.** Its water column
bottoms at 1.51 GPa, in the middle of ice VI, so this is the new phases doing load-bearing
work inside a converged solution rather than merely unblocking a search. C/MR² comes out
2.1 % from the measured value, the same tolerance Mars and Mercury sit at.

**The other four rows are a limit of the recipe, not of the ice.** This inversion solves
**one** free fraction over a silicate interior, and all four are three-layer bodies. Callisto
at 0.3549 is the classic partially-undifferentiated case, which a fully layered model cannot
produce at all and which the recipe already declines to model by name. Titan's high moment
of inertia is read as hydrated silicate in the core, again a mixture. Europa has an iron
core, and inverting it on the ice axis puts almost no ice on it and lands 9.5 % high.
Enceladus is small enough that porosity is live, which is the degeneracy every inverted
result already carries in its notes. None of the four is evidence against the ice phases:
each names a mechanism this document already lists as out of scope. Only Ganymede is a fair
test of the ice ladder, and it passes.

The icy-moon table is regenerated by `python3 engine/test_interior.py --icy`; the Ganymede
row alone is asserted in the default test run, because the other four take minutes.

Both tables, and the roster table below, are regenerated by
`python3 engine/test_interior.py --table` and `--roster`. None of them is hand-keyed.

## Domain of validity

| regime | condition | what this recipe does | grade |
|---|---|---|---|
| rock + metal | any mass whose central pressure stays under the core material's ceiling | integrates the profile, returns all five outputs | calibrated |
| rock + ice Ih | ice column base below 209.5 MPa | integrates, ice Ih throughout | calibrated |
| rock + ice VII | ice column base above 2.216 GPa and below 37.4 GPa | integrates, ice VII | calibrated |
| rock + ice III / V / VI | ice column base in 209.5 MPa – 2.216 GPa | integrates, switching phase at each triple point | calibrated |
| **warm ice window** | ice column base in 209.5 MPa – 2.216 GPa on a body warm enough to melt | **not decided here**: the same pressures hold liquid water, and choosing needs a thermal profile this recipe does not carry | — |
| ice X / superionic | ice column base above 37.4 GPa | declines, naming the phase (Goncharov+ 2005; French+ 2009) | — |
| electron degeneracy | central pressure above the core material's ceiling | declines, naming Thomas–Fermi–Dirac | — |
| **undifferentiated** | `differentiated: false` | **declines**, naming the mixed-phase equation of state it would need | — |
| **too light for any rock/ice mix** | mean density below pure ice | **declines**, naming porosity or an H/He envelope | — |
| gas / ice giant | `body_class` names a fluid body | declines: every equation of state here is condensed matter, and an H/He envelope is a polytrope. See [mass–radius relation](mass-radius-relation-methodology.md) §2 for that literature | — |

Out of domain is a **returned value**, not an error: each row comes back with its reason
attached, so a body that cannot be derived says why instead of being extrapolated.

Three of those rows are refusals the previous revision could not phrase, and the phrasing is
the deliverable:

**Undifferentiated is not CMF = 0.** Setting the core mass fraction to zero says there is no
metal. An undifferentiated body has metal that never segregated, so it sits mixed through
the silicate. This solver stacks pure materials layer by layer and has no way to express a
mixed phase; what it would need is a mixture equation of state (volume-additive, or a
Voigt–Reuss–Hill average). That is the named starting point, and with it the body solves.

**Porosity is not ice.** Both lower the mean density, and at the central pressures of a
few-hundred-kilometre body both are live. The recipe separates two different failures. If
the observed radius can be reached by some rock-and-ice mixture, the recipe returns that
mixture and warns that a lower-ice, higher-porosity solution fits equally well. If the
observed radius cannot be reached even by pure water ice, the recipe declines and says so:
that is the case where **a porosity model is the missing piece**, and a compaction curve is
what unlocks it.

**A missing phase was not a missing layer, and closing it was a citation rather than a
model.** Until 2026-08-25 an ice column reaching into the 209.5 MPa to 2.216 GPa window
came back declined, because the recipe did not know what ices III, V and VI weigh. That row
is gone from the table above: the ladder now runs unbroken from ice Ih to ice VII, and the
test asserts the contiguity rather than trusting it, since editing one transition pressure
out of step with its neighbour would silently reopen a hole. What remains above the ladder
is ice X and the superionic phase, and that decline is unchanged.

## What the roster asks for

Six moons in the Alpha Centauri and Proxima systems have both a mass and a radius on the
board, and four of them sit below 3000 kg/m³, which the revision before last refused
outright. Running the inversion on all six:

| body | ρ̄ (kg/m³) | ice declared | outcome | what it took, or what is missing |
|---|---|---|---|---|
| Pandora (A b III) | 4901 | allowed | solved | solved — core_mass_fraction 0.255, C/MR² 0.3384, P_c 220903 MPa |
| Cassandra (A b IV) | 5467 | allowed | solved | solved — core_mass_fraction 0.654, C/MR² 0.3311, P_c 81809 MPa |
| Hades (A b II) | 2829 | **excluded** | declined | porosity: ice is excluded by declaration, so void space is what is left. Needs a compaction curve |
| Dante (A b I) | 2620 | **excluded** | declined | porosity: ice is excluded by declaration, so void space is what is left. Needs a compaction curve |
| Chaos (A b V) | 2014 | allowed | solved | solved — ice_mass_fraction 0.240, C/MR² 0.3150, P_c 162 MPa |
| Proxima Cen c I | 1599 | allowed | solved | solved — ice_mass_fraction 0.406, C/MR² 0.3052, P_c 85 MPa |

Four of the six solve. The two that do not decline for a stated reason rather than being
turned away at a mean-density gate, and the reason is the same for both.

**The `ice declared` column is a declaration, not a measurement, and it decides the
answer.** The board states what each body is made of, and for two of them it excludes water
ice outright: Dante is a silicate volcanic moon of the Io type with an SO₂ outgassing
atmosphere, and Hades is recorded as "silicate and ice-free". Handing the inversion only a
mass and a radius lets it pick the ice axis on density alone, and it then reports an ice
result for two bodies the board says have no ice at all. That is a wrong statement about a
real question, so the declaration is an input.

**With ice excluded, Dante and Hades still decline on porosity, and the new ice phases do
not change that.** A zero-porosity silicate body of Dante's mass comes out at 486 km against
a declared 521 km, and Hades at 718 km against 750; the volume shortfall is 18.7 % and
12.3 % respectively. With ice ruled out by declaration, the mechanism left is **void
space**, and their central pressures (344 and 752 MPa) are low enough for it to survive. The
recipe has no compaction curve, so it declines and says so. A second reading is recorded
alongside: if the rock is genuinely lighter than the silicate this recipe carries, no
porosity is needed and the question becomes *which* rock, and if neither holds then the
declared mass-radius pair is what wants revisiting. Naming a porosity model is the
actionable half.

**Chaos solves, and reading why it used to decline is worth the paragraph.** The board calls
it a small icy moon of water ice with rock, so the ice axis is legitimate there. The
converged answer is 24 % ice over a silicate interior, C/MR² 0.3150, with the base of the
water column at only 20 MPa: the body is small, and every part of its ice is ice Ih.

So the ice phases are not in the answer at all. What they changed is the **path**. The
inversion scans the ice-fraction axis before bisecting, and the shooting method inside each
scan point starts from an overestimate of the central pressure. Those first trial
integrations put the base of the ice column at 0.368, 0.278 and 0.217 GPa for the three grid
points nearest the answer, all three inside the old gap. Every one of them raised the gap
and took its grid point out of the scan, and with those three gone no surviving pair of
neighbours bracketed the target radius, so the inversion declined and reported the missing
phases. The previous revision of this document read the 0.217 GPa off one of those blocked
trial points and described it as the converged mixture sitting a hair above the ice Ih
boundary. That was wrong: the converged mixture is nowhere near the boundary, and the
sentence has been removed rather than adjusted.

The mechanism it named was still the right one, and the lesson is sharper than the original
claim. **A hole in an equation of state does not only block the bodies whose answer lies
inside it; it blocks every body whose solver has to pass through it.** A shooting method
that clamped its trial pressures might have reached Chaos without ices III, V and VI. That
is a real observation about the inversion and it is recorded here rather than acted on,
because redesigning the shooter is separate work. The phases are needed regardless, and
Ganymede in the validation section is the proof: its water column bottoms out inside ice VI
in the **converged** solution, not in a trial one.

If Chaos is warm rather than cold, the pressures its ice column reaches are low enough that
part of it would be liquid instead. That needs a thermal profile, which is a different
recipe, and the domain table above records it as undecided rather than as solved.

## Worked example: Pandora (Alpha Centauri A b III)

The board fixes 3.85 × 10²⁴ kg (0.6447 M⊕) and 5724 km (0.8984 R⊕), a mean density of
4901 kg/m³. Two questions can be asked of it, and they are different questions.

**Forward, from a declared composition.** At CMF 0.325, `earth_like` materials:

    central pressure   237.7 GPa       (shot to 1e-8 in enclosed mass)
    phase sequence     fe_prem → silicate     (no ice, no lower-mantle-only column)
    radius             0.8854 R⊕ = 5641 km
    core boundary      0.5497 R  → core radius 0.4867 R⊕ = 3101 km
    C/MR²              0.3320

So an Earth-composition Pandora would be 1.5 % smaller than the board says. That is not a
failure; it is the recipe doing the job the old one could not, which is to notice.

**Inverted, from the board's own mass and radius.** Solving for the core mass fraction
instead gives **CMF 0.255**, with C/MR² 0.3384. Pandora is slightly iron-poor relative to
Earth, which is the physically sensible reading of a 4901 kg/m³ body at two thirds of an
Earth mass, and it is a number the board can now carry with its derivation attached.

The difference between 0.332 and 0.3384 propagates into J₂ through Radau–Darwin, and from
there into the moon-system integrations that the stability reports depend on. Both values
now arrive with their inputs, their regime, their phase sequence and their convergence flag
instead of as a class constant.

## Citations

- **Seager, S., Kuchner, M., Hier-Majumder, C. A. & Militzer, B. 2007**, ApJ 669, 1279
  ([`2007ApJ...669.1279S`](https://ui.adsabs.harvard.edu/abs/2007ApJ...669.1279S), arXiv
  **[0707.2895](https://arxiv.org/abs/0707.2895)**). **Cached** in
  `docs/phase3/_papers/0707.2895.md`. The structure equations this recipe integrates
  (their eqs. 1–3), and Table 1's Vinet/BME fits, from which the recipe takes Fe(ε),
  MgSiO₃ enstatite and H₂O ice VII. Also the source of the Thomas–Fermi–Dirac boundary that
  the high-pressure decline names.
- **Zeng, L., Sasselov, D. D. & Jacobsen, S. B. 2016**, ApJ 819, 127
  ([`2016ApJ...819..127Z`](https://ui.adsabs.harvard.edu/abs/2016ApJ...819..127Z), arXiv
  **[1512.08827](https://arxiv.org/abs/1512.08827)**). **Cached** in
  `docs/phase3/_papers/1512.08827.md`. The BM2 fits to PREM's outer core and lower mantle
  that carry the rocky part of this recipe, the 23.83 GPa mantle transition, and the
  semi-empirical M–R relation used as an independent validation curve.
- **Zeng, L. & Sasselov, D. 2013**, PASP 125, 227
  ([`2013PASP..125..227Z`](https://ui.adsabs.harvard.edu/abs/2013PASP..125..227Z), arXiv
  **[1301.0818](https://arxiv.org/abs/1301.0818)**). **Cached** in
  `docs/phase3/_papers/1301.0818.md`. The H₂O phase sequence along the melting curve and
  its transition pressures (Ih → III at 209.5 MPa, VI → VII at 2.216 GPa, VII → X at
  47 GPa), which is where this recipe's ice-phase gates come from.
- **Feistel, R. & Wagner, W. 2006**, J. Phys. Chem. Ref. Data 35, 1021
  ([`2006JPCRD..35.1021F`](https://ui.adsabs.harvard.edu/abs/2006JPCRD..35.1021F)).
  The IAPWS-06 Gibbs-potential equation of state for ice Ih. *No arXiv preprint*: verified
  by bibcode, and the two constants used here (ρ and κ_T at the normal pressure melting
  point) were read from Table 6 of the IAPWS release document
  [R10-06(2009)](http://www.iapws.org/relguide/Ice-2009.pdf), which is the authoritative
  publication of the same equation. Marked as a **non-ADS-fulltext exception**: the release
  document was read directly, not summarised.
- **Journaux, B., Brown, J. M., Pakhomova, A., Collings, I. E., Petitgirard, S., Espinoza,
  P., Boffa Ballaran, T., Vance, S. D., Ott, J., Cova, F., Garbarino, G. & Hanfland, M.
  2020**, JGR Planets 125, e2019JE006176
  ([`2020JGRE..12506176J`](https://ui.adsabs.harvard.edu/abs/2020JGRE..12506176J), DOI
  [10.1029/2019JE006176](https://doi.org/10.1029/2019JE006176)). The Gibbs-energy
  representations of ices Ih, II, III, V, VI and VII/X distributed as **SeaFreeze**, from
  which this recipe evaluates ρ₀, K₀ and K₀′ for ices III, V and VI. *No arXiv preprint.*
  The publisher's open-access full text was not reachable from here (Wiley and the three
  listed repository mirrors all refused), so this is a **non-ADS-fulltext exception with a
  stated verification route**: the paper is pinned by bibcode and DOI, and the numbers were
  taken from the peer-reviewed representation itself (pip package `SeaFreeze==1.1.0`, pinned
  in `engine/requirements.txt`) rather than from any summary of it. The representation is
  checked in two ways that do not depend on reading the paper: it reproduces the IAPWS-06
  ice Ih check state to nine significant figures, and it reproduces the ice VI single-point
  output published in the package's own documentation (900 MPa, 255 K, ρ = 1356.1 kg/m³) to
  2 × 10⁻⁵.
- **Dziewonski, A. M. & Anderson, D. L. 1981**, PEPI 25, 297
  ([`1981PEPI...25..297D`](https://ui.adsabs.harvard.edu/abs/1981PEPI...25..297D)).
  The Preliminary Reference Earth Model: the profile Zeng+ 2016's fits are extrapolations
  of, and the source of the measured C/MR² = 0.3307 the recipe is anchored against.
- Moment-of-inertia anchors, rocky: Mars from Konopliv+ 2011 and InSight; Mercury from
  Margot+ 2012 (MESSENGER radar); Moon from Williams+ 2014 (lunar laser ranging).
- Moment-of-inertia anchors, icy: Ganymede C/MR² = 0.3115 from **Schubert+ 2004**
  ([`2004jpsm.book..281S`](https://ui.adsabs.harvard.edu/abs/2004jpsm.book..281S)),
  originally **Anderson+ 1996**
  ([`1996Natur.384..541A`](https://ui.adsabs.harvard.edu/abs/1996Natur.384..541A));
  Callisto 0.3549 from **Anderson+ 2001**
  ([`2001Icar..153..157A`](https://ui.adsabs.harvard.edu/abs/2001Icar..153..157A));
  Titan 0.3414 ± 0.0005 from **Iess+ 2010**
  ([`2010Sci...327.1367I`](https://ui.adsabs.harvard.edu/abs/2010Sci...327.1367I));
  Europa 0.346 ± 0.005 from **Anderson+ 1998**
  ([`1998Sci...281.2019A`](https://ui.adsabs.harvard.edu/abs/1998Sci...281.2019A));
  Enceladus 0.335 ± 0.005 from **Iess+ 2014**
  ([`2014Sci...344...78I`](https://ui.adsabs.harvard.edu/abs/2014Sci...344...78I)). None of
  the five has an arXiv preprint; each value was verified against ADS-indexed full text or
  the paper's own abstract rather than taken from memory.
- **Still not obtained, and still not used.** Choukroun & Grasset 2007
  ([`2007JChPh.127l4506C`](https://ui.adsabs.harvard.edu/abs/2007JChPh.127l4506C)) and 2010
  ([`2010JChPh.133n4502C`](https://ui.adsabs.harvard.edu/abs/2010JChPh.133n4502C)), and
  Bezacier+ 2014 ([`2014JChPh.141j4505B`](https://ui.adsabs.harvard.edu/abs/2014JChPh.141j4505B)),
  carry their own equation-of-state coefficients for ices III, V, VI and VII. None has an
  arXiv preprint and none is reachable in full text from here. The **transition pressures**
  attributed to Choukroun & Grasset 2007 in this document are read from Zeng & Sasselov
  2013 §III.3.1, which states them explicitly; their coefficients are not used and are not
  cited for any number here. Two further sources that would give an independent set were
  looked for and are also paywalled: Dunaeva+ 2010
  ([`2010SoSyR..44..202D`](https://ui.adsabs.harvard.edu/abs/2010SoSyR..44..202D)), which
  tabulates thermodynamic functions for the high-pressure ices, and Gagnon+ 1990
  ([`1990JChPh..92.1909G`](https://ui.adsabs.harvard.edu/abs/1990JChPh..92.1909G)), the
  Brillouin measurement of densities and acoustic velocities for polycrystalline ices Ih,
  II, III, V and VI. Either would let the SeaFreeze-derived constants be checked against a
  second, experimental source; the request for full texts stands.

## Related

- [Mass–radius relation](mass-radius-relation-methodology.md) — takes its rocky radius and
  its pure-iron density gate from this recipe, replacing the composition scaling table
- [Body figure](body-figure-methodology.md) — turns C/MR² into J₂ via Radau–Darwin
- [Principia geopotential data](principia-geopotential-data.md) — the J₂ worked example
- [Rocky-planet dynamo](rocky-planet-dynamo-methodology.md) — consumes the core radius
- [Derivation discipline](derivation-discipline.md) — why the contract block is checked
  against the code, and why tables are generated rather than typed

<!-- Validation and roster tables regenerated by `python3 engine/test_interior.py --table`
     and `--roster`. -->
