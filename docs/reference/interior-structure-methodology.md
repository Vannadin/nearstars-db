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

**2026-08-26 added compaction.** The solver had treated every layer as solid throughout, so
a small body whose self-gravity cannot crush what it accreted from came back as a body made
of something lighter, or came back declined. Porosity is now a function of the local
pressure, taken from a published relation rather than fitted to any of our bodies, and the
two moons the previous revision refused on that mechanism return numbers. The section on
[porosity](#porosity-what-the-pressure-has-not-crushed-yet) has the relation, and
[what it says about Dante and Hades](#what-the-compaction-relation-says-about-dante-and-hades)
has the part that matters: the relation accounts for their volume deficits arithmetically
and rules itself out physically, which is a finding about two invented radii rather than a
solved interior.

**2026-08-26, later, added giants.** The recipe had refused every hydrogen-helium body, and
the refusal was right about the cause and wrong about the remedy: what giants needed was not
another recipe but another equation of state. A polytrope joined `bm2`, `bme3` and `vinet` as
a fourth functional form, an H/He material joined the four condensed ones, and the same
integrator now solves a giant as a body with one more layer on the outside. No new node, no
new methodology document. Jupiter comes out within 0.6 % of its mean radius from its mass
alone; Saturn comes out 20.7 % too large, which the source paper predicts and explains. The
consequence worth reading is
[what it opens](#what-the-giant-branch-opens-alpha-centauri-a-b-and-the-class-table): Alpha
Centauri A b now has a derived C/MR² of 0.2614 against the 0.23 the class table carries, and
that difference propagates into J₂ and from there into a 21-hour moon integration.

## Contract — `interior_layers`

**Returns** — `nmoi` [—] · `core_radius_fraction` [—] · `core_radius` [R_earth] ·
`radius` [R_earth] · `core_pressure` [GPa] · `bulk_porosity` [—] · `voids_expected` [—]
**Needs** — `mass_earth` [M_earth] · `core_mass_fraction` [—] · `ice_mass_fraction` [—] ·
`composition` [—] · `differentiated` [—] · `body_class` [—] · `radius_earth` [R_earth] ·
`initial_porosity` [—] · `porosity_cap` [Pa] · `gas_mass_fraction` [—] ·
`tidal_heating` [—] · `envelope_z` [—]
**Discriminating keys** — the material stack chosen by `composition`, and the pressure
reached at each layer boundary, which decides whether a grounded phase exists there.
Regimes and their numeric conditions are in [Domain of validity](#domain-of-validity).
**Grade** — calibrated, dropping to **analog** whenever `initial_porosity` is greater than
zero, and for any giant below Jupiter's mass, where the branch has never been checked. The equations of state are published fits and the recipe reproduces four measured
moments of inertia without being handed layer densities; the compaction relation is a
laboratory curve extrapolated past the pressures it was measured at, and the initial
porosity it needs is a declaration this recipe cannot derive.

`radius_earth` is **not used to compute anything**: radius is an output. When supplied it
is compared against the derived radius, so a composition declaration that fails to
reproduce a known body says so instead of passing quietly. The inversion below is what
consumes it for real.

`tidal_heating` is not used to compute anything either. It is one of the three indicators
behind `voids_expected`, and it is a declaration rather than an inference because tidal
heating is another node's output; estimating it here from mass or orbit would put a second
copy of that node inside this recipe.

`voids_expected` answers a question the compaction relation does not: whether this body is
in a regime where pore space survives at all. It is false when any of three indicators
fires — mass above the observed transition, central pressure above the grain-fracture
threshold, or declared tidal heating — and a porous solution returned alongside
`voids_expected: false` is an envelope, not a prediction.

This block is checked against the code: `engine/check_contracts.py` compares what is
declared here with what `interior_layers` actually consumes and produces at run time, so
the two cannot drift.

## The relation

A body in hydrostatic equilibrium satisfies mass conservation and the balance of pressure
against self-gravity, closed by an equation of state. These are Seager+ 2007's equations
(1) to (3) ([arXiv:0707.2895](https://arxiv.org/abs/0707.2895)):

    dm/dr = 4π r² ρ(r)
    dP/dr = −G m(r) ρ(r) / r²
    ρ     = ρ_solid(P) · (1 − φ(P))     ← the equation of state, per material,
                                          times the solid fraction left at that pressure

The porosity term φ(P) is zero unless the body is declared porous, and the section on
[compaction](#porosity-what-the-pressure-has-not-crushed-yet) below says where it comes
from. Everything in this document up to that section is the φ = 0 case.

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

**Polytrope**, P = K ρ^(1+1/n), which is not a condensed-matter fit at all. It is the form a
hydrogen-helium envelope takes, and it is worth being precise about what adding it did: a
polytrope is **a fourth functional form, not a separate branch of the recipe**. The same
integrator, the same shooting method and the same moment-of-inertia accumulation run
unchanged; a giant planet is a body with one more layer on the outside. That is why the
giant row in the domain table below moved from "declines" to "integrates" without a new
node, a new recipe or a new methodology document. The [giant branch](#giants-the-polytrope-is-a-fourth-eos-form-not-a-fifth-recipe)
section has the constants and the limits.

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
| `h_he` (giant envelope) | polytrope, n = 1 | 0 (see note) | K = 2.1 × 10⁵ m⁵ kg⁻¹ s⁻² | n = 1 | 0 to 653 TPa | Helled+ 2022 §2, unit-checked against their own R = 70,300 km |

Six things about that table are worth stating out loud, because each of them is a
decision rather than a transcription. `h_he` has ρ₀ = 0 because a polytrope really does go
to zero density at zero pressure: the envelope has no surface, it fades out, and the
integration stops where the pressure does. Every row carries both ends of its validity range,
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
coefficients sit in Choukroun & Grasset 2007/2010, neither of which we could obtain in full
text (the request stands). The coefficients in the table above come from somewhere else,
and they are not a fit to anybody's data.

### Mixing two materials in one layer

The four forms above each describe **one pure substance**. A layer holding two at once needs
no new form, only a rule for combining the ones already here, and the rule is the
**additive volume law**: at a given pressure each component occupies its own volume, and
the volumes add by mass fraction.

    1/ρ_mix(P) = Σ_i  w_i / ρ_i(P)              Σ w_i = 1

Baraffe+ 2008 §3.3 ([arXiv:0802.1810](https://arxiv.org/abs/0802.1810)) states this form
directly, as "the mass-weighted interpolation of each species contribution at constant
intensive variables, P and T", calls it "exact in the ideal gas limit, without restriction
on the species mass fractions and densities", and is equally direct about the cost: "the
interactions between the three different fluids … are not taken into account". It is the
standard rule rather than a choice made here. Saumon+ 1995 built their H/He tables with
"the additive volume rule and an additional ideal entropy-of-mixing term", and Chabrier+
2019 ([arXiv:1902.01852](https://arxiv.org/abs/1902.01852)) restate it twenty-four years
later in the same words.

| constant | value | what it is | source |
|---|---|---|---|
| volume deviation | ≤ 8 % | error the rule introduces, at constant pressure, for H–He | Vorberger+ 2007, DFT-MD test |
| worst regime | molecular dissociation | where that 8 % is reached; near zero in the pure molecular phase | same |
| ceiling of a mixture | lowest component ceiling | above it the mixture density has no grounding, whatever the other components can still do | this recipe |
| envelope Z carrier | `silicate` | the material that carries heavy elements in a giant envelope | see below |

**The 8 % is the only quantified bound, and it covers H–He only.** Vorberger+ 2007
([arXiv:cond-mat/0609476](https://arxiv.org/abs/cond-mat/0609476)) ran first-principles
DFT-MD specifically to "investigate the validity of the widely used linear mixing
approximation", and found "deviations of up to 8% in energy and volume from linear mixing
at constant pressure in the region of molecular dissociation": near zero in the pure
molecular phase, up to 10 % in pressure at a Jupiter-like ratio at 5000 K, with the volume
error "slightly smaller than the one in the pressure". No comparable measurement was found
for a rock–metal mixture, and none is quoted here: the H–He number is not carried across.

**No material in this file is the right carrier for a giant envelope's heavy elements**, and
each fails differently. `h2o` matches the composition best, since Z in giants is
ice-dominated, and is unusable because it stops at 37.4 GPa. `fe_prem` reaches 12 TPa but
iron is the dense end of Z rather than its middle. `silicate` is the plausible middle and
stops at 3.5 TPa, which covers Saturn's centre and not Jupiter's; it is the one used, and
the ceiling it imposes is reported rather than avoided.

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

## Porosity: what the pressure has not crushed yet

Everything above treats a layer as solid all the way through. Small bodies are not. Their
self-gravity is too weak to crush the material they accreted from, so void space survives,
and the mean density comes out below what the composition alone would give. Ignoring that
is how a rubble pile gets mistaken for a body made of something lighter.

There is a threshold, and it is a pressure rather than a size. **Silicate grains begin to
fracture at about 10⁷ Pa**, which Britt+ 2002 established and Carry 2012 §5.2 restates as
"silicate grains start to fracture when the pressure reaches ∼10⁷ Pa". Below it an
aggregate keeps its voids; above it they collapse. The observational record agrees with the
threshold read as a pressure: Carry 2012 §5.2 notes that "the pressure inside an object
with a mass lower than ≈10²⁰ kg never reaches 10⁷ Pa", and reports that bodies above
10²⁰ kg all sit at macroporosity ≈ 0 while everything below is scattered from 0 to 70 %.

### The relation

The recipe uses Bierson, Nimmo & McKinnon 2019's equations (1) and (2)
([`2019Icar..326...10B`](https://ui.adsabs.harvard.edu/abs/2019Icar..326...10B)), which is
the formulation that has been checked against real bodies: they used it to explain the
observed density-versus-size trend of the Kuiper Belt.

    ice     φ(P) = max( φ₀ · exp(b_ice · P),  φ_floor )
    rock    φ(P) = min( φ₀ · P^(b_rock),      φ₀      )

P is the local lithostatic pressure in **MPa**. The two functional forms differ because
Yasui & Arakawa 2009 fitted the two materials that way, not because we chose it: in their
compaction experiments an exponential fitted ice in the low-porosity regime and a power law
fitted silica across the whole pressure range (their §3.3).

| constant | value | what it is | source |
|---|---|---|---|
| `b_ice` | −0.1 MPa⁻¹ | exponential rate for water ice | Bierson+ 2019 Table 1, from Yasui & Arakawa 2009 |
| `b_rock` | −0.11 | power-law exponent for silicate | Bierson+ 2019 Table 1, from Yasui & Arakawa 2009 |
| `φ_floor` | 0.20 | porosity the ice matrix supports on strength alone | Bierson+ 2019 Table 1, from Durham+ 2005 |
| `φ₀` | 0.60 (nominal) | initial porosity, a **declared input** | Bierson+ 2019 Table 1 |
| grain-fracture threshold | 10⁷ Pa | where silicate grains start to break | Britt+ 2002, via Carry 2012 §5.2 |
| experimental ceiling | 150 MPa | highest pressure the compaction experiments reached | Durham+ 2005 |

`b_rock` can be checked against its own source rather than taken on trust. Yasui & Arakawa
2009's Table 1, last row (run 090210-5, pure silica at −10 °C) reports a power-law fit with
a₃ = 0.53 and b₃ = 0.11, an initial porosity of 0.64 falling to 0.38 at 30 MPa. The
exponent is the same number Bierson+ 2019 carry, read from two papers independently.

**Iron gets no porosity law.** Not because the literature is silent but because the question
does not arise: a core forms by metal melting and sinking, so applying an unsintered-granular
curve to it contradicts how it got there. `porosity.py` records that reasoning next to the
material map rather than leaving the omission to be guessed at.

### Four limits, and the last one is the load-bearing one

**Pressure.** Yasui & Arakawa 2009 pressed to 30 MPa at −10 °C and 80 MPa at −55 to −67 °C;
Durham+ 2005 reached 150 MPa. Above that the curve is extrapolated, and the power-law tail
decays so slowly that the extrapolation is visibly wrong at planetary pressures: pushed to
Earth's central 358 GPa it still returns 15 % porosity. So the recipe carries a
`porosity_cap`, which claims nothing above a stated pressure, and the verdict below is taken
under the cap so that no conclusion rests on unmeasured extrapolation. Each result also
reports the fraction of the body's mass that sits above the ceiling.

**Cold and unsintered.** Bierson+ 2019 §2.2 lists what their model leaves out: "melt
production, differentiation, convection, impacts, and tidal heating". All five remove
porosity, which is why they describe their runs as "a lower bound on the bulk density (the
most porosity that can be retained)". The same holds here, one stage earlier: this recipe
implements only their brittle stage, so what it returns is the **most** porosity a body
could keep, not an estimate of what it kept.

**The ice branch is the cold branch.** With `b_ice` = −0.1 MPa⁻¹ and a floor of 0.20, the
relation describes ice at Durham's 77 to 120 K. Yasui & Arakawa's pure ice at −10 °C
compacted to 0.02 at 30 MPa, where this relation still returns 0.20. Warm ice is not
described here, and the test prints both numbers side by side rather than letting the gap
pass unnoticed.

**φ₀ is not derived.** Accretion sets it and heating erases it, and this recipe carries
neither, so it arrives as a declaration and defaults to **zero**. Zero is not a claim that
a body has no voids: it is the statement that this recipe cannot decide. That default is
also what keeps the anchors still, and the test measures the alternative rather than
asserting it, by reporting what declaring φ₀ = 0.60 would do to the Moon.

## Giants: the polytrope is a fourth EOS form, not a fifth recipe

Until 2026-08-26 this recipe refused every giant planet, and the refusal named the reason
correctly: iron, silicate and the water ices are all condensed matter, and a
hydrogen-helium envelope is not. What it got wrong was the implied conclusion, that giants
therefore needed somewhere else to live. They needed one more equation of state.

### The relation

For a hydrogen-helium mixture at giant-planet envelope conditions, Helled, Movshovitz &
Nettelmann 2022 §2 ([arXiv:2202.10046](https://arxiv.org/abs/2202.10046)) call P ∝ ρ² "a
simple and artificial assumption" that is "nevertheless a surprisingly reasonable
approximation of the compressibility of a hydrogen-helium mixture at conditions typical of
giant planet envelopes", and give the constant. Combined with hydrostatic equilibrium it
has a closed-form non-rotating solution, which is the polytrope of index one:

    P = K ρ²,   K = 2.1 × 10⁵ m⁵ kg⁻¹ s⁻²
    ρ(r) = ρ_c · sin(kr)/(kr),   k = √(2πG/K)
    R = √(πK/2G)                     ← independent of mass

The mass-independent radius is the signature of n = 1, and it is why Jupiter-mass planets
all come out about the same size. Two more numbers fall out of the same solution and both
are used below as checks: the central density is ρ_c = πM/(4R³), and the normalised moment
of inertia is a pure number,

    C/MR² = (2/3)(1 − 6/π²) = 0.261380

which is a textbook integral of the Lane–Emden solution rather than anything this
repository decided.

**The constant carried a unit trap, and the paper's own arithmetic caught it.** That paper
prints K = 2.1 × 10¹² and labels it m⁵ kg⁻¹ s⁻², which is SI. Read in SI it puts the radius
at 1.49 AU. Read as cgs, which is what the number actually is, it converts to
2.1 × 10⁵ SI and gives R = 70,302 km against the 70,300 km the same paragraph states. So
the value in the code is 2.1 × 10⁵, chosen by checking it against the source's own
downstream number rather than by transcribing the digits. `engine/test_giant.py` re-runs
both readings, so the trap cannot be walked into again. This repository has been 54× wrong
in a hand-keyed table before, and that is the discipline that catches it.

### Three limits, and one of them is a planet

**Mass, by declaration.** `body_class` decides. `giant` and `gas_giant` integrate;
`ice_giant`, `sub_neptune`, `brown_dwarf` and `star` still decline, and each decline names
what it would need rather than saying "out of scope". An ice giant's envelope is a
water-ammonia-methane mixture whose equation of state is not in this file, and n = 1 is
tuned to H/He compressibility, so it cannot stand in. A sub-Neptune's envelope thickness is
set by age and irradiation rather than by composition, and this recipe is isothermal with no
evolution, so it cannot choose the gas fraction (given one, the integration runs). A brown
dwarf burns deuterium above about 13 M_J, which makes its luminosity a function of age;
Spiegel, Burrows & Milsom 2011 ([arXiv:1008.5150](https://arxiv.org/abs/1008.5150)) call
13 M_J "generally a reasonable rule of thumb" while noting it depends on helium, deuterium
and metal abundance. A star's C/MR² comes from the n = 3/2 polytrope value 0.205
(Chandrasekhar 1939) on a separate branch in `body_figure`, and that branch is not touched
here.

**Pressure, and the literature is silent on it.** The source paper states no pressure
ceiling for the approximation, because the way it fails is not a pressure cutoff: the same
paragraph attributes the poorer fit for Saturn to composition and to the shape of Saturn's
envelope, not to reaching some pressure. So the ceiling in the code is a **second fence
rather than the load-bearing one**: it is the central pressure this relation reaches at
13 M_J, above which `body_class` declines anyway.

**Saturn, which is the interesting limit.** The relation reproduces Jupiter and does not
reproduce Saturn, and the source predicts exactly that. See the
[validation](#giants-checked-against-the-analytic-solution-and-against-two-planets) below.

### Which radius, and why it matters by 2 %

A non-rotating spherical model must be compared against a **volumetric mean radius**, not
against an equatorial one. Rotation inflates Jupiter's equator by 2.3 % over its mean, and
this recipe does not compute that. So the anchors are the IAU/IAG Working Group values
(Archinal+ 2011): Jupiter mean 69,911 km against equatorial 1 bar 71,492 km, Saturn mean
58,232 km against equatorial 1 bar 60,268 km. Both are stated in the validation table so
that no comparison silently changes convention.

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
core mass fraction. A body less dense needs either ice or void space, and which of the two
is a declaration rather than a deduction: where the board allows ice the recipe solves for
the ice mass fraction, and where the board excludes it the recipe solves for the initial
porosity against the published compaction relation instead.

The axis is **scanned before it is bisected**. Bisecting straight away will eventually
probe a value inside the phase gap and stop there, and nothing then distinguishes "the
answer is unreachable" from "a trial point happened to land in a hole". Scanning first
means the recipe can say which of the two it is, and that distinction is the whole point of
the exercise for the low-density moons below.

**The inversion is not unique, and the result says so.** At the pressures small bodies
reach, void space survives, and porosity and ice lower the mean density in the same
direction. An icy body at 30 % ice and a less icy body at 15 % ice with 15 % porosity are
not distinguished by mass and radius alone. Having a compaction model does not fix that: it
makes both branches computable rather than one of them computable and the other a gap. So
every inverted result carries the degeneracy in its notes, names which axis it took and on
whose declaration, and is graded **analog** rather than calibrated.

The porosity inversion has one extra honesty requirement, because its free variable is the
initial porosity and that is exactly the quantity the relation cannot derive. So the
recipe brackets before it inverts: it reports the radius at zero porosity, the radius at the
published nominal φ₀ = 0.60 read to the letter, and the radius at that nominal under the
conservative cap. Only if the declared radius falls inside that envelope does it read back a
φ₀, and it reads it back under the cap so the answer never depends on extrapolation. Outside
the envelope it declines and says the declared mass-radius pair is what wants revisiting.
The number that comes back is a **read-back, not a fitted constant**, and the notes say so.

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

### Compaction, checked on published measurements and published bodies

The compaction relation needs its own anchors, and none of them is our own output.

**Against the laboratory.** Yasui & Arakawa 2009's pure-silica run compacted from 0.64 to
0.38 at 30 MPa, and their own power-law fit through it gives 0.365. Our implementation
returns 0.440 for the same starting porosity, 16 % high, because Bierson+ 2019 normalise the
prefactor to φ₀ rather than to Yasui's fitted a₃. That bias gives **more** porosity, which is
the direction their "lower bound on the bulk density" is meant to err in, so it is
conservative rather than wrong. On the ice side Durham+ 2005 measured about 0.10 residual
porosity at 150 MPa; the floor Bierson adopted, and this recipe uses, is 0.20, twice the
measurement and again conservative.

**Against the published model.** Bierson+ 2019 §2.1 justifies their nominal initial porosity
by stating that "a nominal value of 60% is used as this gives an object with f_m = 70% a
density of ~750 kg/m³". Running our integration at φ₀ = 0.60 and a 70 % rock mass fraction
over the seven smallest bodies below returns **749 kg/m³**, 0.1 % from the published figure.
That is the transcription check: the relation as implemented reproduces the number its source
paper quotes for it.

**The transition mass falls out, and it is not an input.** Nothing in the integration is told
about 10²⁰ kg. Given only the compaction relation and the 10 MPa grain-fracture threshold,
the mass at which a porous silicate body's central pressure first crosses that threshold
comes out at **3.0 × 10¹⁹ kg** (a 168 km radius), inside the 10¹⁹ to 10²⁰ kg transition Carry
2012 §5.2 reports from observed asteroid macroporosities. A curve fitted in mass would have
no reason to land there.

**Against measured bodies.** The fifteen Kuiper Belt objects Bierson+ 2019 list in their
Table A.2, each run at their nominal 70 % rock mass fraction, under the conservative cap:

| body | D (km) | ρ observed | ρ brittle-only | ρ zero-porosity | source |
|---|---|---|---|---|---|
| Altjira | 123 | 300 | 736 | 1837 | Vilenius+ 2014 |
| Typhon | 157 | 600 | 738 | 1837 | Stansberry+ 2012 |
| Ceto | 174 | 1370 | 747 | 1837 | Grundy+ 2007 |
| Teharonhiawako | 178 | 600 | 739 | 1837 | Vilenius+ 2014 |
| 2001 QC298 | 235 | 1140 | 765 | 1837 | Vilenius+ 2014 |
| Sila | 249 | 730 | 756 | 1837 | Vilenius+ 2014 |
| Lempo | 304 | 500 | 762 | 1837 | Stansberry+ 2006 |
| 2002 UX25 | 652 | 820 | 920 | 1837 | Brown 2013 |
| Varda | 705 | 1270 | 989 | 1841 | Vilenius+ 2014 |
| Salacia | 866 | 1260 | 1069 | 1841 | Brown & Butler 2017 |
| Orcus | 958 | 1520 | 1136 | 1841 | Fornasier+ 2013 |
| Quaoar | 1070 | 2180 | 1243 | 1842 | Vilenius+ 2014 |
| Charon | 1212 | 1700 | 1276 | 1842 | Nimmo+ 2016 |
| Haumea | 1595 | 1885 | 1466 | 1843 | Ortiz+ 2017 |
| Eris | 2326 | 2520 | 1638 | 1871 | Brown+ 2011 |

Three things in that table are the point, and a fourth is a limit worth naming.

The brittle-only density **rises monotonically with mass**, from 736 to 1638 kg/m³ across
five orders of magnitude in mass, while the zero-porosity column barely moves (1837 to
1871). The size-density trend is the thing Bierson+ 2019 set out to explain, and it comes
out of the pressure dependence rather than out of any compositional change: the rock mass
fraction is held fixed at 0.70 for every row.

**Six bodies sit below the curve** (Altjira, Typhon, Teharonhiawako, Sila, Lempo,
2002 UX25). Five of them are the small, low-density objects whose rock mass fraction the
paper solves for individually (their Fig. 1b treats f_m as free per object); holding it
fixed at the nominal 0.70, as we do, must scatter rows both ways. The sixth is the one
Bierson+ 2019 §3 flag themselves: "2002 UX25 is below our expected density. We are not
aware of any processes that might significantly lower the bulk density without lowering
f_m." Our implementation puts it below the curve too, which is the agreement worth having.

**Eight bodies sit more than 20 % above the curve**, and that gap is the missing stage
rather than a failure. Bierson+ 2019 run a brittle pass and then a thermal-ductile pass that
closes pores by viscous creep; this recipe carries only the first, because the second needs a
thermal history and this solver is isothermal. Denser-than-predicted large bodies are exactly
the signature that would leave. It is a stated limit, not a decline.

The last check is that none of this leaks upward. With porosity undeclared the integration is
byte-identical to before: Earth 0.3297 and the Moon 0.3945, unchanged. Declaring φ₀ = 0.60
on the Moon would grow its radius from 1745 to 1764 km, which is why the default is zero and
why the test prints that number rather than claiming the effect is negligible.

The KBO table is regenerated by `python3 engine/test_porosity.py --kbo`.

### Giants, checked against the analytic solution and against two planets

The polytrope needs a different kind of check from the condensed materials, because for
n = 1 the answer is known in closed form. That makes the first check exact rather than
tolerant.

**Against the analytic solution.** Integrating the H/He envelope numerically must reproduce
the Lane–Emden solution it is a discretisation of. The radius comes out mass-independent to
4 × 10⁻⁵ across 95 to 1200 M⊕, matches √(πK/2G) to 8 × 10⁻⁶, and the moment of inertia
comes out 0.26138 against the textbook (2/3)(1 − 6/π²) = 0.261380. Nothing about that
agreement is tuned: it is the integrator being shown to integrate.

**Against the published number, which is also the unit check.** The same K gives 70,302 km
against the 70,300 km Helled+ 2022 §2 states, and the same digits read as SI give 1.49 AU.
The test asserts both, so the reading that was chosen stays chosen for a reason on the
record rather than by habit.

**Against two planets.** Regenerated by `python3 engine/test_giant.py --table`:

| body | M (M⊕) | R derived | R mean (IAU) | ΔR vs mean | R eq 1 bar | C/MR² derived | P_c (GPa) |
|---|---|---|---|---|---|---|---|
| Jupiter | 317.8 | 70302 km | 69911 km | +0.6 % | 71492 km | 0.2614 | 3866 |
| Saturn | 95.2 | 70302 km | 58232 km | +20.7 % | 60268 km | 0.2614 | 347 |
| Alpha Centauri A b | 120.0 | 70302 km | – | – | 71492 km (declared) | 0.2614 | 551 |

**Jupiter is reproduced to 0.6 % from its mass alone**, and the central pressure of
3866 GPa (38.7 Mbar) lands where Jupiter's is independently believed to be. That is the
result which says the polytrope actually went in.

**Saturn is 20.7 % too large, and that is the honest answer rather than a bug.** The source
paper predicts it in the same paragraph it gives the constant in: the index-1 approximation
"is more appropriate for Jupiter than it is for Saturn", both because P ∝ ρ² does not fit
Saturn's present-day envelope as well and because Saturn's interior is more enriched in
heavy elements. Guillot 1999 ([arXiv:astro-ph/9907402](https://arxiv.org/abs/astro-ph/9907402))
puts the total heavy-element mass at 11 to 42 M⊕ for Jupiter and 19 to 31 M⊕ for Saturn,
which is 3 to 13 % of Jupiter against 20 to 33 % of Saturn. Saturn is the metal-rich one and
a pure-H/He relation cannot know that. Closing it would need an envelope equation of state
with metals dissolved in it, which is the same **mixture** equation of state this document
already declines to invent for undifferentiated rocky bodies. The test pins the residual
into a band rather than tolerating it, so the limit cannot be quietly fixed or quietly made
worse.

**A heavy-element core does not rescue it, and running into that found a second limit.**
Putting Guillot's heavy elements into a compact central core makes the planet smaller, which
is the wrong direction for Jupiter and not nearly enough for Saturn. It also runs out of
material: a 19 M⊕ rock core self-compresses to about 3.4 TPa on its own, which is at the
stated ceiling of the PREM lower-mantle fit (3.5 TPa, Zeng+ 2016), and Jupiter's centre at
3.9 TPa is past it. So this recipe cannot put a large rock core inside a giant, and it
declines by naming that ceiling. Real giant models do not use a compact core for all of Z
either: Guillot's own core limits are below the total heavy-element mass precisely because
much of it is dissolved in the envelope.

**Jupiter's moment of inertia, and why this document names one value out of three.** Three
numbers circulate and they are not equally grounded.

| value | where it comes from | why it is not the anchor |
|---|---|---|
| 0.254 | the NASA Jupiter fact sheet lineage | an ADS-indexed full text notes that this value "actually translates into λ = 0.243 when it is normalised using R_eq", so its normalising radius is ambiguous |
| 0.2756 | Ni 2018 ([`2018A&A...613A..32N`](https://ui.adsabs.harvard.edu/abs/2018A%26A...613A..32N)), re-quoted by later papers as "a Jupiter-like value determined from the Juno probe" | its full text was not reachable from here, so whether that paper *infers* it or *scans* it as an input could not be confirmed. What could be confirmed is that no interior-model study read in full produces it, and that it sits 4.5 % above the ones that do |
| **0.2634 to 0.2644** | Neuenschwander+ 2021 ([arXiv:2101.12508](https://arxiv.org/abs/2101.12508)) get 0.2634 < MoI < 0.2639 from piecewise-polytropic profiles fitted to the Juno gravity field, and quote Wahl+ 2017 at 0.2640 to 0.2644 | **this is the anchor.** Post-Juno, fitted to the measured field, two independent studies, and the union sits inside the 0.2629 to 0.2645 that Helled+ 2011 ([arXiv:1109.1627](https://arxiv.org/abs/1109.1627)) obtained separately |

The coreless polytrope gives 0.2614, which is 0.77 % below the anchor band's lower edge. The
sign is expected: real Jupiter has heavy elements concentrated inward, and every mechanism
that concentrates mass pushes C/MR² **down** from the polytrope value, not up. That the
residual is under one percent while the two rejected values are off by 3.8 % and 4.4 % is
the argument for the anchor as much as the provenance is.

### Mixtures, checked on Saturn and on a discrimination

Heavy-element masses are Guillot 1999's constraints, 11 to 42 M⊕ for Jupiter and 19 to
31 M⊕ for Saturn, divided by the planet mass. Nothing is tuned: Z = 0.200 is the **bottom
edge** of the published Saturn budget, taken as a boundary. Regenerated by
`python3 engine/test_mixture.py --table`:

| body | Z (M⊕) | Z fraction | R derived | R mean (IAU) | ΔR | C/MR² | grade |
|---|---|---|---|---|---|---|---|
| Jupiter | 0 | 0.000 | 70302 km | 69911 km | +0.6 % | 0.2614 | calibrated |
| Jupiter | 11 | 0.035 | declined | 69911 km | – | – | – |
| Jupiter | 26 | 0.083 | declined | 69911 km | – | – | – |
| Jupiter | 42 | 0.132 | declined | 69911 km | – | – | – |
| Saturn | 0 | 0.000 | 70302 km | 58232 km | +20.7 % | 0.2614 | analog |
| Saturn | 19 | 0.200 | 58198 km | 58232 km | -0.1 % | 0.2650 | analog |
| Saturn | 25 | 0.263 | 54544 km | 58232 km | -6.3 % | 0.2667 | analog |
| Saturn | 31 | 0.326 | 50988 km | 58232 km | -12.4 % | 0.2687 | analog |

**Saturn goes from +20.7 % to −0.1 %** at the bottom of its published Z budget. What remains
is the difference between heavy elements spread evenly through the envelope, which is what
this rule does, and their real distribution: post-Juno models favour a **diluted core**,
heavy elements graded inward rather than uniform. That distribution is not modelled here,
and the residual belongs to it.

**Jupiter declines at every Z in its budget.** With heavy elements mixed in, its centre
passes 4 TPa while the silicate fit stops at 3.5 TPa, and the decline names that component
rather than reporting electron degeneracy, which is what a pure material at its ceiling
would mean. The same ceiling stopped the previous revision's attempt to place Guillot's Z
as a compact core, so two different mechanisms meet one limit.

**Adding Z does not restore a mass axis.** R = √(πK/2G) has no M in it whether or not the
envelope carries metals, so two giants of the same Z still receive the same radius. That
axis is piecewise polytropes (Neuenschwander+ 2021) and is not opened here.

**Undifferentiated bodies have no measured anchor**, so what is tested is the discrimination
a real anchor would perform. Mercury at its measured mass and metal fraction returns C/MR²
0.3933 undifferentiated against the measured 0.3460, 13.7 % higher: the recipe correctly
says Mercury cannot be undifferentiated. Two further properties are asserted rather than
assumed. C/MR² comes out 0.3714 / 0.3721 / 0.3719 for metal fractions 0.0 / 0.325 / 0.70,
flat to 0.0007, because a homogeneous body's concentration is set by self-compression and
not by what it is made of; and undifferentiated Earth sits at 0.3721 against 0.3297
differentiated, 12.9 % apart, which is the axis doing something.

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
| porous rock or ice | `initial_porosity` > 0, central pressure inside the 150 MPa experimental ceiling | integrates with φ(P) from the published relation | analog |
| **porosity above the experimental ceiling** | `initial_porosity` > 0, pressure above 150 MPa | the relation is **extrapolated**: results report the mass fraction affected, and `porosity_cap` gives the reading that claims nothing there | analog |
| **porosity on a heated body** | `initial_porosity` > 0 and the body has melt, differentiation, convection, impacts or tidal heating | **not decided here**: all five remove porosity (Bierson+ 2019 §2.2), so what this recipe returns is an upper bound on the voids, never an estimate | — |
| ice X / superionic | ice column base above 37.4 GPa | declines, naming the phase (Goncharov+ 2005; French+ 2009) | — |
| electron degeneracy | central pressure above the core material's ceiling | declines, naming Thomas–Fermi–Dirac | — |
| undifferentiated rock + metal | `differentiated: false` with no ice or gas | integrates one mixed layer by the same rule. No measured C/MR² anchor exists for such a body, so the check is a discrimination: undifferentiated Mercury does not reproduce the measured value | analog |
| **undifferentiated with ice or gas** | `differentiated: false` and `ice_mass_fraction` or `gas_mass_fraction` > 0 | **declines**: this rule mixes rock and metal only, and ice mixed through rock is partial differentiation, which is neither fully mixed nor fully layered | — |
| **too light for any rock/ice mix** | mean density below the porous envelope | **declines**, saying the declared mass-radius pair is outside what the published relation allows | — |
| gas giant | `body_class` is `giant` or `gas_giant` and a `gas_mass_fraction` is given | integrates, H/He envelope on the n = 1 polytrope | calibrated |
| **unvalidated giant mass** | `gas_mass_fraction` > 0 and mass below Jupiter's 317.8 M⊕ | **integrates at grade analog**: the two anchors are Jupiter at +0.6 % and Saturn at +20.7 %, and nothing between them has been checked. Since n = 1 returns the same radius and C/MR² for every giant, there is no basis for saying which end the residual resembles | analog |
| metal-rich giant | as above with `envelope_z` > 0, central pressure under the Z carrier's ceiling | integrates, H/He and heavy elements mixed by the additive volume law. Saturn lands at −0.1 % at the bottom of its published Z budget | analog |
| **giant whose centre passes the Z carrier's ceiling** | `envelope_z` > 0 and central pressure above 3.5 TPa (Jupiter) | **declines**, naming the component whose fit ended rather than reporting degeneracy. Needs a rock equation of state fitted further up | — |
| **diluted core** | heavy elements graded inward rather than uniform through the envelope | **not decided here**: this rule mixes one homogeneous Z, and the residual after it belongs to the distribution | — |
| **large rock core in a giant** | heavy elements placed as a compact core massive enough to self-compress past 3.5 TPa | **declines**, naming the PREM lower-mantle fit's stated ceiling | — |
| ice giant | `body_class` is `ice_giant` | declines: the envelope is a water-ammonia-methane mixture, and n = 1 is tuned to H/He compressibility | — |
| sub-Neptune | `body_class` is `sub_neptune` | declines: envelope thickness is set by age and irradiation, and this recipe is isothermal with no evolution. Given a gas fraction the integration runs | — |
| brown dwarf | `body_class` is `brown_dwarf` | declines, naming deuterium burning above ~13 M_J (Spiegel+ 2011) and the age-dependent luminosity this recipe has no track for | — |
| star | `body_class` is `star` | declines: the stellar C/MR² is the n = 3/2 polytrope value 0.205 (Chandrasekhar 1939) on a separate `body_figure` branch, untouched here | — |

Out of domain is a **returned value**, not an error: each row comes back with its reason
attached, so a body that cannot be derived says why instead of being extrapolated.

Three of those rows are refusals the previous revision could not phrase, and the phrasing is
the deliverable:

**Undifferentiated is not CMF = 0.** Setting the core mass fraction to zero says there is no
metal. An undifferentiated body has metal that never segregated, so it sits mixed through
the silicate. This solver stacks pure materials layer by layer and has no way to express a
mixed phase; what it would need is a mixture equation of state (volume-additive, or a
Voigt–Reuss–Hill average). That is the named starting point, and with it the body solves.

**Porosity is not ice, and now both are modelled.** Both lower the mean density, and at the
central pressures of a few-hundred-kilometre body both are live, so mass and radius alone
cannot separate them. What changed on 2026-08-26 is that the porosity side is no longer a
gap: a body whose board excludes ice is now solved on the porosity axis instead of being
turned away, and a body whose board allows ice is still solved on the ice axis. The
degeneracy is real and every result says so in its notes. What the recipe will not do is
pick between them from density, because density does not contain that information; the
board's composition declaration does, and it is an input for exactly that reason.

**A missing phase was not a missing layer, and closing it was a citation rather than a
model.** Until 2026-08-25 an ice column reaching into the 209.5 MPa to 2.216 GPa window
came back declined, because the recipe did not know what ices III, V and VI weigh. That row
is gone from the table above: the ladder now runs unbroken from ice Ih to ice VII, and the
test asserts the contiguity rather than trusting it, since editing one transition pressure
out of step with its neighbour would silently reopen a hole. What remains above the ladder
is ice X and the superionic phase, and that decline is unchanged.

## What the roster asks for

Six moons in the Alpha Centauri and Proxima systems have both a mass and a radius on the
board, and four of them sit below 3000 kg/m³, which two revisions ago was refused outright.
Running the inversion on all six:

| body | ρ̄ (kg/m³) | ice declared | outcome | what it took, or what is missing |
|---|---|---|---|---|
| Pandora (A b III) | 4901 | allowed | solved | solved — core_mass_fraction 0.255, C/MR² 0.3384, P_c 220903 MPa |
| Cassandra (A b IV) | 5467 | allowed | solved | solved — core_mass_fraction 0.654, C/MR² 0.3311, P_c 81809 MPa |
| Hades (A b II) | 2829 | **excluded** | solved | solved — initial_porosity 0.478, C/MR² 0.3742, P_c 738 MPa |
| Dante (A b I) | 2620 | **excluded** | solved | solved — initial_porosity 0.389, C/MR² 0.3771, P_c 317 MPa |
| Chaos (A b V) | 2014 | allowed | solved | solved — ice_mass_fraction 0.240, C/MR² 0.3150, P_c 162 MPa |
| Proxima Cen c I | 1599 | allowed | solved | solved — ice_mass_fraction 0.406, C/MR² 0.3052, P_c 85 MPa |

All six solve, and the table is now less interesting than what sits behind two of its rows.

**The `ice declared` column is a declaration, not a measurement, and it still decides the
answer.** The board states what each body is made of, and for two of them it excludes water
ice outright: Dante is a silicate volcanic moon of the Io type with an SO₂ outgassing
atmosphere, and Hades is recorded as "silicate and ice-free". Handing the inversion only a
mass and a radius lets it pick the ice axis on density alone. Now that the porosity axis
exists, that would be worse rather than better, because both axes return a number: the
recipe would silently choose the wrong mechanism instead of declining. The declaration is
what makes the choice, and it is an input for that reason.

**Chaos and Proxima Centauri c I are untouched by any of this.** Their boards allow ice, so
they take the ice axis exactly as before: 24 % ice at C/MR² 0.3150 and 41 % ice at 0.3052,
the same numbers to four figures. Porosity would fit them too, and that is the degeneracy
the notes carry; what stops the recipe drifting onto the new axis is the declaration, not a
tolerance.

### What the compaction relation says about Dante and Hades

This is the question the porosity work was for, and the answer has three parts. It is worth
being careful here, because **the mass and radius of both bodies are invented.** The board
marks them `INVENTED`, and Dante's radius was set by the surface heat-transport gate rather
than by any observation. So the relation was built and validated first, on Solar System
bodies and laboratory compaction curves, and only then pointed at these two.

**First: the numbers fit inside the envelope.** Both declared radii lie between the
zero-porosity radius and the radius the published relation allows, and they lie inside it
under the conservative cap as well, so this conclusion does not rest on extrapolating the
compaction curve past the pressures it was measured at.

| body | R at φ = 0 | R at published φ₀ = 0.60 | same, capped at 150 MPa | R declared | φ₀ read back | bulk porosity |
|---|---|---|---|---|---|---|
| Dante (A b I) | 486 km | 575 km | 558 km | 521 km | 0.389 | 0.186 |
| Hades (A b II) | 718 km | 834 km | 765 km | 750 km | 0.478 | 0.124 |

Both read-back values sit below the published nominal of 0.60, and the bulk porosities they
imply, 18.6 % and 12.4 %, are the volume deficits the previous revision could only name.
Taken on its own that is the first of the three legitimate outcomes: the model explains the
voids.

**Second: the regime is wrong, and the observations say so.** Dante is 1.6 × 10²¹ kg and
Hades 5.0 × 10²¹ kg, which is 16 and 50 times the mass above which Carry 2012 §5.2 reports
that bodies are observed to have **no macroporosity at all**. Their central pressures, 317
and 738 MPa, are 32 and 74 times the grain-fracture threshold. And 34 % of Dante's mass and
69 % of Hades's sits above the pressures the compaction experiments ever reached. Every one
of those is a statement that these bodies are outside the population the relation was
calibrated on, in the direction of less porosity rather than more.

**Third: their own board rows close it.** Bierson+ 2019 §2.2 lists the processes their model
excludes, and tidal heating is on that list. Dante's board carries about 1200 times Io's
tidal heat flux, and Hades's about 15 times Io's, with surface temperatures of 278 to 444 K.
Cold unsintered granular rock is the one thing the relation requires, and the board declares
the opposite for both bodies. The relation therefore returns an **upper bound on the voids
they could hold**, and the physical expectation for a body heated like that is that the
voids are gone.

So the honest verdict is the third of the three outcomes rather than the first: **the
relation accounts for the deficit arithmetically and rules itself out physically, and what
is left over is the thermal history.** Two readings survive that, and both are for the owner
rather than for this recipe. Either the declared radii are too large for the declared masses,
which is a finding about art-direction values that were invented rather than observed, or the
rock is genuinely lighter than the enstatite-plus-PREM silicate this recipe carries, in which
case the question becomes which rock and the answer is a composition rather than a void
fraction. Nothing here changes the board: it reports.

What did change is that the recipe now says all of that with numbers instead of declining
with a mechanism name. The previous revision could only report "porosity, and a compaction
curve is what unlocks it". The curve arrived, and the answer it gives is that these two
bodies are the wrong size to use it on.

## What the giant branch opens: Alpha Centauri A b and the class table

The moons above are condensed bodies and none of them moved. The body that moved is their
primary, and it moved a number that other work is already standing on.

Alpha Centauri A b is declared at 120 M⊕ with a radius of 1.0 R_J and `body_class: giant`.
Before this revision the recipe refused it, so its C/MR² came from `nmoi_class_table`, a
per-class lookup carrying **0.23** with no citation behind it. The integration now returns a
value for the same body:

| quantity | class table | integrated | difference |
|---|---|---|---|
| C/MR² | 0.23 | 0.2614 | **+13.6 %** |
| radius | not produced | 70,302 km = 0.983 R_J | −1.7 % against the declared 1.0 R_J |
| central pressure | not produced | 551 GPa | – |

**That radius agreement is not evidence, and saying so is part of the result.** The n = 1
solution has R = √(πK/2G) with a single constant K, so it returns 70,302 km for *every*
giant regardless of mass or composition — this document establishes exactly that, two
sections up, as the signature of the form. The board's 1.0 R_J was an art-direction
tie-break set near Jupiter's size, and K is the constant Helled+ 2022 fit to Jupiter. Two
Jupiter-shaped numbers agreeing tells us nothing about this body: had the board declared a
Saturn-sized radius, the same solution would have been 20 % out, exactly as it is for
Saturn.

The mass makes this concrete. Alpha Centauri A b is 120 M⊕, or 0.38 M_J. Jupiter, where the
branch is right to 0.6 %, is 1.0 M_J; Saturn, where it is wrong by 20.7 %, is 0.30 M_J. The
body sits between the two anchors and roughly eight times nearer the one that fails, in a
gap that has never been checked. The recipe therefore returns the value at grade **analog**
with a note naming both anchors, rather than at calibrated.

What survives is a narrower claim, and it is still worth having: 0.23 has no source and
0.2614 has one. The 0.2614 is the value the physics predicts for a body with no substantial
core, and 0.23 is what a body with a large concentrated core would give. Which one is right for a
fictional planet is not a question this recipe can settle. What it can say is that 0.23 has
no source and 0.2614 has one, plus the caveat attached to it: the coreless polytrope is
0.77 % *below* Jupiter's measured band, so for a real giant the integrated value is a mild
over-estimate of C/MR² rather than an under-estimate.

**This is reported, not applied.** The board is untouched, and the reason to be careful is
in `engine/backflow.py impact body_figure`: changing `body_figure` obliges 87 rows across
seven boards to be regenerated, invalidates the 21-hour Alpha Centauri moon integration, and
touches 21 methodology documents plus their mirrors. The stability report records that the
oblateness reverses which moon orbit is selected, so J₂ moving is not a cosmetic change.
Whether to move it is the owner's call.

**`nmoi_class_table` is now replaceable, and that is all this document claims.** The class
table survived the previous revision with a deliberately narrowed domain, "lookup, for the
class the integration cannot reach", and giants were that class. They are not any more. Two
consumers read `nmoi` from it, `body_figure` and `cassini_state`, and both would have to move
together for the same reason they moved together last time. Removing the table and rewiring
those edges is a separate task with its own consequences; recording that the debt is now
payable is this one's job.

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
- **Bierson, C. J., Nimmo, F. & McKinnon, W. B. 2019**, Icarus 326, 10
  ([`2019Icar..326...10B`](https://ui.adsabs.harvard.edu/abs/2019Icar..326...10B), DOI
  [10.1016/j.icarus.2019.01.027](https://doi.org/10.1016/j.icarus.2019.01.027)). **Cached** in
  `docs/phase3/_papers/2019Icar..326...10B.txt`. The pressure-dependent porosity relation
  this recipe implements (their eqs. 1 and 2), its constants (their Table 1), the nominal
  initial porosity and the ~750 kg/m³ figure the validation reproduces, the fifteen Kuiper
  Belt densities of their Table A.2, and the §2.2 list of processes their model excludes,
  which is where this recipe's "cold and unsintered" limit comes from. *No arXiv preprint*:
  read from the author-accepted manuscript in PubMed Central
  ([PMC7058130](https://pmc.ncbi.nlm.nih.gov/articles/PMC7058130/)), a **non-ADS-fulltext
  exception** noted here so a later audit knows the route.
- **Yasui, M. & Arakawa, M. 2009**, JGR Planets 114, E09004
  ([`2009JGRE..114.9004Y`](https://ui.adsabs.harvard.edu/abs/2009JGRE..114.9004Y), DOI
  [10.1029/2009JE003374](https://doi.org/10.1029/2009JE003374)). **Cached** in
  `docs/phase3/_papers/2009JGRE..114.9004Y.pdf`. The compaction experiments the two
  exponents come from: their §3.3 chooses the exponential and power-law forms per material,
  and their Table 1 last row gives the pure-silica fit (a₃ = 0.53, b₃ = 0.11, porosity 0.64
  falling to 0.38 at 30 MPa) against which `b_rock` is independently checked. *No arXiv
  preprint*; open access, read from the Kobe University repository copy.
- **Durham, W. B., McKinnon, W. B. & Stern, L. A. 2005**, GRL 32, L18202
  ([`2005GeoRL..3218202D`](https://ui.adsabs.harvard.edu/abs/2005GeoRL..3218202D)). The cold
  hydrostatic compaction of granulated water ice at 77 to 120 K up to 150 MPa, which sets
  both the experimental ceiling this recipe reports against and the strength-supported
  porosity floor. *No arXiv preprint and not reachable in full text from here*: the residual
  porosity of about 0.10 at maximum pressure and the 10 to 20 % retained beyond 100 MPa are
  quoted from the ADS abstract, and the floor value actually used (0.20) is taken from
  Bierson+ 2019's Table 1 rather than from this paper. Marked as **abstract-only** so the
  distinction is not lost.
- **Carry, B. 2012**, P&SS 73, 98
  ([`2012P&SS...73...98C`](https://ui.adsabs.harvard.edu/abs/2012P%26SS...73...98C), arXiv
  **[1203.4336](https://arxiv.org/abs/1203.4336)**). **Cached** in
  `docs/phase3/_papers/1203.4336.md`. Densities and macroporosities for 287 small bodies.
  §5.2 supplies the 10⁷ Pa silicate grain-fracture threshold (attributing it to Britt+ 2002),
  the statement that pressure inside a body below ≈10²⁰ kg never reaches it, and the observed
  transition from scattered macroporosity below that mass to macroporosity ≈ 0 above it.
  This is the number the derived transition mass is checked against.
- **Britt, D. T., Yeomans, D., Housen, K. & Consolmagno, G. 2002**, in *Asteroids III*, 485
  ([`2002aste.book..485B`](https://ui.adsabs.harvard.edu/abs/2002aste.book..485B)). The
  original source of the grain-fracture threshold and of the three-way split of asteroids
  into essentially solid bodies, heavily fractured bodies at ~20 % macroporosity, and rubble
  piles above 30 %. A book chapter with no preprint and no online full text here: it is cited
  through Carry 2012, which quotes the threshold explicitly, and no number is taken from it
  directly.
- **Bezacier+ 2014 was obtained** ([`2014JChPh.141j4505B`](https://ui.adsabs.harvard.edu/abs/2014JChPh.141j4505B),
  no arXiv; full text in hand 2026-08-26). It measures the equations of state of ices VI and
  VII by synchrotron X-ray diffraction, and checking our two phases against its Table II puts
  the density curves within **0.37 %** and **1.95 %** across their windows. Nothing was
  changed: ice VII stays on the Hemley+ 1987 line (via Seager+ 2007), whose K₀ the authors'
  own measurement undercuts by 12 %. Both agreements sit inside the anchor tolerance, and
  moving would break the shared-source consistency the silicate and iron phases rely on.
- **Helled, R., Movshovitz, N. & Nettelmann, N. 2022**, arXiv preprint
  ([`2022arXiv220210046H`](https://ui.adsabs.harvard.edu/abs/2022arXiv220210046H), arXiv
  **[2202.10046](https://arxiv.org/abs/2202.10046)**). **Cached** in
  `docs/phase3/_papers/2202.10046.md`. The n = 1 polytrope for hydrogen-helium envelopes:
  the statement that P ∝ ρ² is "a surprisingly reasonable approximation of the
  compressibility of a hydrogen-helium mixture at conditions typical of giant planet
  envelopes", the constant K, the closed-form solution and R = √(πK/2G), the resulting
  70,300 km, and the explanation of why the approximation suits Jupiter better than Saturn.
  Also the source of the unit discrepancy recorded in `engine/eos.py`: the paper prints the
  cgs value of K with an SI label, and its own radius is what resolves which reading is
  meant.
- **Guillot, T. 1999**, P&SS 47, 1183
  ([`1999P&SS...47.1183G`](https://ui.adsabs.harvard.edu/abs/1999P%26SS...47.1183G), arXiv
  **[astro-ph/9907402](https://arxiv.org/abs/astro-ph/9907402)**). **Cached** in
  `docs/phase3/_papers/astro-ph_9907402.md`. The heavy-element budgets this document uses as
  the composition input and as the explanation for Saturn: total heavy-element mass 11 to
  42 M⊕ in Jupiter and 19 to 31 M⊕ in Saturn, with core masses below 14 and 22 M⊕
  respectively and no lower bound on either.
- **Neuenschwander, B. A., Helled, R., Movshovitz, N. & Fortney, J. J. 2021**, ApJ 910, 38
  ([`2021ApJ...910...38N`](https://ui.adsabs.harvard.edu/abs/2021ApJ...910...38N), arXiv
  **[2101.12508](https://arxiv.org/abs/2101.12508)**). **Cached** in
  `docs/phase3/_papers/2101.12508.md`. The Jupiter C/MR² anchor: 0.2634 < MoI < 0.2639 from
  piecewise-polytropic density profiles fitted to the Juno gravity field, together with the
  Wahl+ 2017 range 0.2640 to 0.2644 that the same paper quotes and does not overlap.
- **Helled, R., Anderson, J. D., Schubert, G. & Stevenson, D. J. 2011**, Icarus 216, 440
  ([`2011Icar..216..440H`](https://ui.adsabs.harvard.edu/abs/2011Icar..216..440H), arXiv
  **[1109.1627](https://arxiv.org/abs/1109.1627)**). **Cached** in
  `docs/phase3/_papers/1109.1627.md`. The independent pre-Juno determination, 0.2629 to
  0.2645, which the adopted anchor band sits inside, plus the Radau–Darwin value 0.2648 and
  the note that a dynamical inference of ~0.236 exists and is much lower.
- **Spiegel, D. S., Burrows, A. & Milsom, J. A. 2011**, ApJ 727, 57
  ([`2011ApJ...727...57S`](https://ui.adsabs.harvard.edu/abs/2011ApJ...727...57S), arXiv
  **[1008.5150](https://arxiv.org/abs/1008.5150)**). The 13 M_J deuterium-burning boundary
  used as the polytrope's declared mass ceiling, quoted with the paper's own caveat that it
  is "generally a reasonable rule of thumb" whose value depends on helium, deuterium and
  metal abundance. Verified by abstract; the full text was not needed for a boundary the
  class gate enforces anyway.
- **Archinal, B. A. et al. 2011**, CeMDA 109, 101
  ([`2011CeMDA.109..101A`](https://ui.adsabs.harvard.edu/abs/2011CeMDA.109..101A)); same
  values in **Seidelmann, P. K. et al. 2007**, CeMDA 98, 155
  ([`2007CeMDA..98..155S`](https://ui.adsabs.harvard.edu/abs/2007CeMDA..98..155S)). The
  IAU/IAG Working Group radii: Jupiter mean 69,911 km and equatorial 1 bar 71,492 km, Saturn
  mean 58,232 km and equatorial 1 bar 60,268 km. Cited for the **radius convention** as much
  as for the numbers, since a non-rotating model compared against an equatorial radius is
  wrong by 2 to 3 %.
- **Ni, D. 2018**, A&A 613, A32
  ([`2018A&A...613A..32N`](https://ui.adsabs.harvard.edu/abs/2018A%26A...613A..32N)).
  **Not used for any number, and recorded here because it is the source of one that
  circulates.** The value 0.2756 appears in its full text and later papers re-quote it as a
  Juno-determined Jovian moment of inertia. Its full text was not reachable from here (the
  publisher's open-access PDF returned a bot challenge), so whether that paper infers the
  value or scans it as an input **could not be confirmed**, and this document does not claim
  either. What is on the record is that it lies 4.5 % above the range of every interior-model
  study that was read in full.
- **Baraffe, I., Chabrier, G. & Barman, T. 2008**, A&A 482, 315
  ([`2008A&A...482..315B`](https://ui.adsabs.harvard.edu/abs/2008A%26A...482..315B), arXiv
  **[0802.1810](https://arxiv.org/abs/0802.1810)**). **Cached** in
  `docs/phase3/_papers/0802.1810.md`. The additive volume law in the form this recipe uses
  (their §3.3), its stated exactness in the ideal gas limit and its stated omission of
  interspecies interactions, applied to H/He plus heavy elements up to Z = 50 %.
- **Vorberger, J., Tamblyn, I., Militzer, B. & Bonev, S. A. 2007**, PhRvB 75, 024206
  ([`2007PhRvB..75b4206V`](https://ui.adsabs.harvard.edu/abs/2007PhRvB..75b4206V), arXiv
  **[cond-mat/0609476](https://arxiv.org/abs/cond-mat/0609476)**). **Cached** in
  `docs/phase3/_papers/cond-mat_0609476.md`. The DFT-MD test of the rule and therefore its
  only quantified validity bound: ≤ 8 % in volume at constant pressure for H–He, worst in
  the region of molecular dissociation and near zero in the pure molecular phase.
- **Saumon, D., Chabrier, G. & van Horn, H. M. 1995**, ApJS 99, 713
  ([`1995ApJS...99..713S`](https://ui.adsabs.harvard.edu/abs/1995ApJS...99..713S)); and
  **Chabrier, G., Mazevet, S. & Soubiran, F. 2019**, ApJ 872, 51
  ([`2019ApJ...872...51C`](https://ui.adsabs.harvard.edu/abs/2019ApJ...872...51C), arXiv
  **[1902.01852](https://arxiv.org/abs/1902.01852)**). The rule's standing: the reference
  H/He tables are built on it, twenty-four years apart, both saying so explicitly.
- **No source found** for a quantified deviation from the additive volume law in a
  rock–metal mixture. The rule is applied there by analogy, and the H–He bound above is
  deliberately not carried across.
- **Still not obtained, and still not used.** Choukroun & Grasset 2007
  ([`2007JChPh.127l4506C`](https://ui.adsabs.harvard.edu/abs/2007JChPh.127l4506C)) and 2010
  ([`2010JChPh.133n4502C`](https://ui.adsabs.harvard.edu/abs/2010JChPh.133n4502C))
  carry their own equation-of-state coefficients for ices III, V and VI. Neither has an
  arXiv preprint and neither is reachable in full text from here. The **transition pressures**
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
