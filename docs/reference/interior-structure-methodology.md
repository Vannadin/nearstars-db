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

## What changed, and why each change had to

| date | what changed | what it cost before, or what it opened |
|---|---|---|
| 2026-08-25 | uniform layers replaced by an integration | layer densities came from a composition table that only held near Earth's mass: Earth's C/MR² was 4.8 % high and always in the same direction, Mercury 8.6 % out because its core sits near 7800 kg/m³ where Earth's runs near 10900. The table is gone, layer density is an output, Earth's error is 0.3 % |
| 2026-08-25 | the water ice column completed | the named hole between 209.5 MPa and 2.216 GPa filled by ices III, V and VI, read from a published Gibbs representation rather than fitted |
| 2026-08-26 | compaction added | a small body whose self-gravity cannot crush what it accreted is solved rather than declined or mistaken for lighter rock. [What it says about Dante and Hades](#what-the-compaction-relation-says-about-dante-and-hades) is the part that matters |
| 2026-08-26 | giants added | what they needed was not another recipe but another equation of state, so a polytrope joined the functional forms. [What that opens](#what-the-giant-branch-opens-alpha-centauri-a-b-and-the-class-table) was a derived C/MR² for Alpha Centauri A b against the 0.23 the class table carries — the polytrope's 0.2614, superseded on 2026-08-28 |
| 2026-08-28 | the H/He envelope stopped being a polytrope | one constant fitted to Jupiter was carrying every giant, and it inflated any envelope that was only part of a planet: Saturn +20.7 %, Uranus +23.8 %, Neptune +29.2 %. The published Chabrier+ 2019 mixture table replaced it — Jupiter −0.83 %, Saturn at Z = 0 +7.06 %, Uranus +5.46 %. The same table carries ∇_ad, which is what finally gave the envelope a temperature; and its entropy columns gave the c_P weights that a metal-loaded envelope needs, closing a silent fallback to an assembled gradient |
| 2026-08-27 | the silicate carried above 3.5 TPa | one phase, spliced where the PREM fit's author stops it and running to where Seager+ 2007 hands silicate to Thomas–Fermi–Dirac. Three separate refusals shared that ceiling: the rocky mass limit rose from 6.84 to 22.78 M⊕ at Earth composition and 19.32 to 53.38 M⊕ for pure silicate, Jupiter's whole heavy-element budget integrates, and a compact rock core inside a Jupiter-mass giant is possible up to 17.66 M⊕. The third only half opened, and its row says so |

## Contract — `interior_layers`

**Returns** — `nmoi` [—] · `core_radius_fraction` [—] · `core_radius` [R_earth] ·
`radius` [R_earth] · `core_pressure` [GPa] · `cmb_pressure` [GPa] ·
`core_temperature` [K] · `cmb_temperature` [K] · `ice_column_state` [—] ·
`ocean_thickness` [km] · `ice_shell_thickness` [km] · `bulk_porosity` [—] · `voids_expected` [—]
**Needs** — `mass_earth` [M_earth] · `core_mass_fraction` [—] · `ice_mass_fraction` [—] ·
`composition` [—] · `differentiated` [—] · `body_class` [—] · `radius_earth` [R_earth] ·
`initial_porosity` [—] · `porosity_cap` [Pa] · `gas_mass_fraction` [—] ·
`tidal_heating` [—] · `envelope_z` [—] · `potential_temperature` [K] ·
`boundary_temperature_jump` [K] · `mantle_rock_fraction` [—] · `serpentinisation` [—]
**Discriminating keys** — the material stack chosen by `composition`, and the pressure
reached at each layer boundary, which decides whether a grounded phase exists there.
Regimes and their numeric conditions are in [Domain of validity](#domain-of-validity).
**Grade** — calibrated, dropping to **analog** whenever `initial_porosity` is greater than
zero, whenever `potential_temperature` departs from the 1600 K reference, and for any giant
below Jupiter's mass, where the branch has never been checked. The equations of state are published fits and the recipe reproduces four measured
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

`potential_temperature` is the third declaration, and it is **not the surface
temperature**: it is the temperature the convecting interior would have if decompressed to
the surface, which is Unterborn+ 2019's boundary condition `T(R) = T_Pot`. Between the two
sits a conductive lid worth roughly 1300 K on Earth, and its thickness is a function of the
heat flux, which is `internal_heat_nontidal`'s output rather than this recipe's. Left unset
the recipe carries no temperature at all and reproduces the isothermal result bit for bit.

`core_temperature` and `cmb_temperature` are a **lower bound on the core**, not the core's
temperature. One adiabat is drawn from the surface to the centre, so the core sits on the
mantle's: the D″ thermal boundary layer is missing (over 1200 K on Earth), and the iron
Grüneisen the γ identity produces from Seager+ 2007's thermal-pressure αK₀ is 0.22 at core
pressures against the ab-initio 1.5. Both biases point down, which is what makes the number
a bound rather than noise, and [`core_state`](core-state-methodology.md) is built on that
property.

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
    dT/dP = γ T / K_S                   ← the adiabat, carried only when a potential
                                          temperature is declared
    ρ     = ρ_solid(P, T) · (1 − φ(P))  ← the equation of state, per material,
                                          times the solid fraction left at that pressure

The porosity term φ(P) is zero unless the body is declared porous, and the section on
[compaction](#porosity-what-the-pressure-has-not-crushed-yet) below says where it comes
from. Everything in this document up to that section is the φ = 0 case. The temperature
term is likewise off unless declared, and the same section pattern applies:
[temperature](#temperature-what-the-fits-already-contain) has the relation and, more
importantly, what it must not be applied to twice.

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
expansion of the elastic potential energy. Both are in Seager's Table 1. **Fourth-order
Birch–Murnaghan (BME4)** adds K₀″, and Seager uses it for one material only, the deep silicate,
because it "is the only fit we found that smoothly matches the TFD EOS at high pressures".
Third order will not approximate it: the published K₀″ sits 2.3 % from the third-order
implied value, and that gap reaches 9.1 % in density at the ceiling.

**Polytrope**, P = K ρ^(1+1/n), which is not a condensed-matter fit at all. It is the form a
hydrogen-helium envelope takes, and it is worth being precise about what adding it did: a
polytrope is **a fourth functional form, not a separate branch of the recipe**. The same
integrator, the same shooting method and the same moment-of-inertia accumulation run
unchanged; a giant planet is a body with one more layer on the outside. That is why the
giant row in the domain table below moved from "declines" to "integrates" without a new
node, a new recipe or a new methodology document. The [giant branch](#giants-the-polytrope-is-a-fourth-eos-form-not-a-fifth-recipe)
section has the constants and the limits.

The materials, with the source of every constant:

| material | form | ρ₀ (kg/m³) | K₀ (GPa) | K₀′ | valid range | αK_T (GPa/K) | T_ref | source |
|---|---|---|---|---|---|---|---|---|
| `fe_prem` (planet core) | BM2 | 7050 | 201 | 4 | 0 to 12 TPa | 0.00121 + 7.8e-7·ΔT | Earth adiabat, 1600 K | Zeng+ 2016 §II, PREM outer-core fit  |
| `fe_eps` (pure iron limit) | Vinet | 8300 | 156.2 | 6.08 | 0 to 20.9 TPa | 0.00121 + 7.8e-7·ΔT | 300 K | Seager+ 2007 Table 1, Fe(ε), Anderson+ 2001 data  |
| `mgsio3_en` (upper mantle) | BME3 | 3220 | 125 | 5 | 0 to 23.83 GPa | 0.00692 | Earth adiabat, 1600 K | Seager+ 2007 Table 1, MgSiO₃ enstatite  |
| `mgsio3_prem` (lower mantle) | BM2 | 3980 | 206 | 4 | 23.83 GPa to 3.5 TPa | 0.00692 | Earth adiabat, 1600 K | Zeng+ 2016 §II, PREM lower-mantle fit  |
| `mgsio3_pv` (deep mantle) | BME4, K₀″ = −0.016 GPa⁻¹ | 4100 | 247 | 3.97 | 3.5 to 13.5 TPa | 0.00692 | Earth adiabat, 1600 K | Seager+ 2007 Table 1 + §III.3, Karki+ 2000 DFT  |
| `antigorite` (serpentinised rock, the light end of one declared axis) | BM2 | 2640.5 (**derived**: 273.50 u per m = 1 unit / 172 Å³) | 67.27 | 4 (fixed) | 0 to 10 GPa | **none published** — room temperature only; T passes through | – | Hilairet+ 2006 §3 [13] BM2 (V₀ 2926.23 Å³), ρ₀ from the structural formula §2 [6] and the m = 1 volume §4 [15]; Holland & Powell 1998 requested for the thermal term  |
| `ice_ih` | BM2 | 916.72 | 8.490 | 4 | 0 to 209.5 MPa | 0.001357 | 273.15 K | IAPWS-06 (Feistel & Wagner 2006) Table 6  |
| `ice_iii` | BME3 | 1126.384 | 7.8349 | 6.7097 | 209.5 to 355.0 MPa | 0.002048 | 251.15 K | SeaFreeze v1.1.0 (Journaux+ 2020), evaluated at P = 0, T = 251.15 K  |
| `ice_v` | BME3 | 1207.842 | 10.6368 | 6.7460 | 355.0 to 618.4 MPa | 0.002369 | 256.43 K | SeaFreeze v1.1.0 (Journaux+ 2020), evaluated at P = 0, T = 256.43 K  |
| `ice_vi` | BME3 | 1263.386 | 10.3686 | 7.8219 | 618.4 MPa to 2.216 GPa | 0.003740 | 272.73 K | SeaFreeze v1.1.0 (Journaux+ 2020), evaluated at P = 0, T = 272.73 K  |
| `ice_vii` | BME3 | 1460 | 23.7 | 4.15 | 2.216 to 37.4 GPa | 0.005922 | 300 K | Seager+ 2007 Table 1, Hemley+ 1987 data; thermal constants from SeaFreeze v1.1.0 `VII_X_French` (French & Redmer 2015) at 2.216 GPa, 300 K  |
| `ice_x` | Vinet | 1644.295 | 22.2868 | 6.7507 | 37.4 GPa to 1 TPa, T ≤ 1800 K | 0.004337 | 300 K | **Fitted**, not read: SeaFreeze v1.1.0 `VII_X_French` (French & Redmer 2015) 300 K isotherm over the range used  |
| `h2o_liquid` (ocean) | baked table, bilinear in (P, T) | – | – | – | 0 to 2.3 GPa, 240 to 500 K | published slope dT/dP\|_S read, not assembled | – | SeaFreeze v1.1.0 `water1` (Bollengier+ 2019), baked by `tools/make_water_table.py`; 2×10⁻⁴ against the source where an ocean sits (252 to 360 K)  |
| `h_he` (giant envelope) | polytrope, n = 1 | 0 (see note) | K = 2.1 × 10⁵ m⁵ kg⁻¹ s⁻² | n = 1 | 0 to 653 TPa | **not applicable** | – | Helled+ 2022 §2, unit-checked against their own R = 70,300 km  |

The two thermal columns have two sources and must not be mixed: rock and metal take αK_T
from Seager+ 2007 §IV.2.2 (Anderson & Masuda 1994 for the silicate, Isaak & Anderson 2003
for the metal and its electron term), the ices from SeaFreeze at the same reference state
their ρ₀, K₀ and K₀′ were read at.

`ice_x` is the one row **fitted rather than read**, and the only one with a temperature
ceiling. The representation's knots start at 1.7 GPa, so the P = 0 reference state the other
ices use is not evaluable, and a Birch-Murnaghan solved backwards from (ρ, K_T, K′) at
37.4 GPa is 15.5 % out by 1 TPa: a local reading does not span a 27× pressure range. A
least-squares Vinet over exactly its range of use holds the source to **1.475 %**, worst at
the two ends, which is this ladder's widest rung and why reaching it drops the grade to
analog. Vinet for the reason Seager+ 2007 §III.1 gives and Fe(ε) already uses. The 1800 K
ceiling is the knot boundary rather than a phase boundary, and it is usable because it sits
**below** the superionic phase this recipe cannot model at all (Millot+ 2019: above 100 GPa
and 2000 K). At 37.4 GPa the two curves meet with a **−2.26 %** step, a disagreement between
Hemley+ 1987 extrapolated and French & Redmer's 2015 potential rather than an error in
either; the test measures it and neither curve was pulled toward the other.

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

**The mantle is three materials, not one.** Earth's upper-to-lower mantle transition sits at
23.83 GPa with a 10 % density jump from 4.0 to 4.4 g/cc (Zeng+ 2016 §II.1). Below it the
recipe uses Seager's enstatite fit, above it the PREM lower-mantle fit. Evaluated at the
transition the two give 3688 and 4379 kg/m³, so the jump the code produces is the jump the
paper describes. Bodies smaller than Mars never reach the transition and are enstatite all
the way down.

**Above 3.5 TPa it is a calculation, not a measured planet.** 3.5 TPa is where Zeng+ 2016 §II
stop their PREM fit, prescribing Thomas–Fermi–Dirac above it; this recipe declines degeneracy
by name instead, so the third phase comes from the paper it already uses for iron. Seager+
2007 §III.3 carries MgSiO₃ on a fourth-order BME to 1.35 × 10⁴ GPa and switches to TFD there,
exactly as its Fe(ε) row does at 2.09 × 10⁴ GPa. The seam is measured rather than invented:
at 3.5 TPa the seismic fit and the DFT fit give 14292 and 14263 kg/m³, **0.21 %** apart, so
no density jump is placed there. Name and substance differ, since post-perovskite has
dissociated to MgO + SiO₂ by 3.10 TPa (Umemoto+ 2017, whose conclusion also settles how many
phases to splice), and what licenses ignoring that is composition rather than structure:
above ~1 TPa Mg/Si stops setting the density. The `SILICATE` comment in `engine/eos.py`
carries the argument in full; being an argument and not a measurement, it costs a result that
steps into this segment its grade, which drops to **analog** with a note naming why.

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

The five forms above each describe **one pure substance**. A layer holding two at once needs
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
| volume deviation, planetary ices | ≤ 4 % binary, ≤ 2.1 % ternary | same error for water–ammonia–methane; the LMA overestimates density and underestimates internal energy | Bethkenhagen+ 2017, DFT-MD test |
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

**Planetary ices do have one, and it is tighter.** Bethkenhagen+ 2017 ran the same kind of
test on water, ammonia and methane up to 1000 GPa and 20 000 K: the three 1:1 binaries
deviate by "4 % or less", which they call an upper limit rather than a typical value, and
the 2:1:4 ternary along three Uranus profiles by at most 2.1 %, falling under 0.5 % above
10 000 K. The deviation has a sign — density over, internal energy under — and it is worst
where one component becomes superionic and another does not. That constant has no consumer
yet, because the envelope it belongs to is still declined; it is recorded so the next
survey does not re-walk the search.

**What that number does not cover.** It bounds the step of mixing three *complete* pure
equations of state by additive volume. It is not the cost of the common shortcut of letting
water stand in for all the ices, which never takes that step: that cost is the difference
between a water EOS and a mixture EOS, a different quantity, and one the cited literature
does not measure. The same paper's conclusion proposes building thermodynamic potentials for
all three pure compounds as future work, which is itself the statement that water alone is
not enough. Under the rule that kept H–He's 8 % away from rock, this number is likewise not
carried across.

**No material in this file is the right carrier for a giant envelope's heavy elements**, and
each fails differently. `h2o` matches the composition best, since Z in giants is
ice-dominated, and is unusable because it stops at 37.4 GPa. `fe_prem` reaches 12 TPa but
iron is the dense end of Z rather than its middle. `silicate` is the plausible middle; it is
the one used, and since 2026-08-27 it reaches 13.5 TPa, which covers both planets' centres
across the whole published Z budget. The ceiling it still imposes is reported, not avoided.

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

### Temperature: what the fits already contain

Thermal pressure adds to the cold curve in the form Seager+ 2007 §IV.2.2 uses, which is
Anderson & Goto 1989's: above the Debye temperature αK_T is nearly volume-independent, so
`P(ρ,T) = P_cold(ρ) + αK_T·ΔT`, with a second-order term for metals whose electrons are
thermally excited. The adiabat supplying T is `dT/dP = γT/K_S`, and γ is not a new constant:
`γ = (∂P/∂T)_V / (ρ c_V)` closes on the thermal-pressure slope already present. That
identity is checked rather than asserted, against SeaFreeze's own Grüneisen parameter for
four ice phases, where it agrees to every digit printed.

**ΔT is measured from each fit's own reference, and getting that wrong would heat Earth
twice.** `fe_prem` and `mgsio3_prem` are fits to PREM, a measurement of the real, hot Earth,
so its geotherm is already inside their effective ρ₀; a 300 K-referenced expansion on top
would double-count it, exactly as the giant branch double-counted heavy elements by adding Z
to a polytrope constant fitted to a Jupiter that already has them. The rock-and-metal column
is therefore referenced to **Earth's adiabat**, anchored at the 1600 K mantle potential
temperature of Unterborn+ 2019 §2. Declaring 1600 K makes ΔT identically zero and the answer
bit-for-bit the isothermal one, which the test asserts as equality rather than closeness.
Ice phases are referenced to the real isotherms already recorded above.

**The anchor is a declaration, and it is not the surface temperature.** In a convecting
interior the adiabat's intercept is the potential temperature; the surface sits below it
across a conductive lid worth roughly 1300 K on Earth, whose thickness is a function of the
heat flux. That flux is `internal_heat_nontidal`'s output, so `potential_temperature` enters
as a declaration beside `ice_allowed` and `tidal_heating`, with the coupling recorded in the
chain as an `influences` edge carrying `status: gap`.

**That edge settles a naming question.** `internal_heat_nontidal`'s `geotherm` is a heat
budget: it produces `l_int` and `t_int` (≈ 35 K for a rocky body) and never writes a T(P),
its text containing no adiabat, Grüneisen parameter or potential temperature. An equation of
state needs T at each pressure along the profile, which only the integration can produce.
Two quantities, one word; the outputs added here are named `core_temperature` and
`cmb_temperature`, and renaming `geotherm` belongs to the recipe that owns it.

### The melting curve: whether the layer is solid at all

With P and T at every depth, the phase question can finally be asked. The curve is a
property of the material and lives beside `phase_at(P)` in `engine/eos.py`, because it needs
the same branch selection: `T_melt(P)` is not single-valued for water, ice Ih's curve running
backwards while ices III, V and VI run forwards.

Water takes the melting-pressure equations of **IAPWS R14-08(2011)**, the same body and the
same kind of document as the IAPWS-06 release ice Ih's ρ₀ and K_T are read from. Each branch
is `p_melt(T)`, inverted numerically at the few pressures the recipe asks about.

| branch | equation | reduced at | valid | uncertainty |
|---|---|---|---|---|
| ice Ih | π = 1 + Σ aᵢ(1 − θ^bᵢ) | 273.16 K, 611.657 Pa | 273.16 → 251.165 K | 2 % |
| ice III | π = 1 − 0.299948(1 − θ⁶⁰) | 251.165 K, 208.566 MPa | 251.165 → 256.164 K | 3 % |
| ice V | π = 1 − 1.18721(1 − θ⁸) | 256.164 K, 350.1 MPa | 256.164 → 273.31 K | 3 % |
| ice VI | π = 1 − 1.07476(1 − θ⁴·⁶) | 273.31 K, 632.4 MPa | 273.31 → 355 K | 3 % |
| ice VII | ln π = 1.73683(1 − θ⁻¹) − 0.0544606(1 − θ⁵) + 8.06106×10⁻⁸(1 − θ²²) | 355 K, 2216 MPa | 355 → 715 K | 7 % |

Ices III, V and VI cover the warm ice window end to end, so the row that used to refuse it is
now a verdict. The release's §7 lists one calculated pressure per equation for program
verification; `test_interior.py` reproduces all five.

**The curve keeps its own triple points.** IAPWS constrains its equations to its own
triple-point table, which differs from the transition pressures this recipe takes from
Choukroun & Grasset 2007 by 0.45 %, 1.4 % and 2.3 %. Neither is moved to match the other,
because moving either breaks the fit it belongs to; the melting curve branches on its own
break pressures instead. Within about 2 % of a triple point the two disagree about which ice
melts, which is inside IAPWS's own 3 %.

**The verdict moves the density.** Wherever the local (P, T) in the water column sits above
the melting curve the integrator uses liquid water, `h2o_liquid` in the table above, so a
body reported `molten` carries an ocean in its radius and C/MR², and reports its thickness
and the ice shell above it. The ocean is not a layer of the stack: it is the same substance
as the shell and the high-pressure ice, so the phase is decided **inside the `h2o` material**,
once per integration step from the state at the step's start, and pinned for the step. The
step is cut where the interpolated (P, T) crosses the curve, exactly as at a layer boundary,
because letting the four Runge–Kutta stages each decide would quantise the ocean's edges to
the grid (measured: 2 × 10⁻³ in radius between 1499 and 1501 steps without the cut, 10⁻⁷ with
it). A liquid above the ocean table's 2.3 GPa goes to the hot-water fit (`h2o_hot`, below) from
1000 K up, the floor Mazevet+ 2019 §3.1 states for ρ ≳ 1 g/cc; a liquid between 500 K and
1000 K has no equation of state here and declines by name, the shelf being SeaFreeze's `water2`
(Brown 2018, to 100 GPa and 10 000 K).

**The ocean's thickness follows the declaration.** The top of an ocean under a shell sits at
the ice Ih melting point of that depth, 273.16 to 251.2 K, and the adiabat decompressed to the
surface is what `potential_temperature` declares: 270 K is a 20 to 30 km shell. The thermal
history that fixes it is not in this recipe, so every result with an ocean is graded analog on
that declaration, the same standing as `core_cmb_temperature` in [core-state](core-state-methodology.md).
**Above 20.6 GPa the curve is a simulation, and it says so.** Where IAPWS equation (5) ends
(715 K), the recipe continues on **Reinhardt+ 2022**'s liquid–solid coexistence line — eleven
thermodynamic-integration points over 10–52.4 GPa, generated into `engine/ice_melt_table.py`
from the paper's published data by `tools/make_ice_melt_table.py` (never transcribed by hand)
and interpolated linearly between points. It is a machine-learned potential fitted to PBE
DFT, not a measurement; the one experimental check available is the triple point (Queyroux+
2020: 14.6 GPa · 850 K against the simulation's ~20 GPa · 875 K), and every experiment that
would check the line itself is paywalled. Any verdict that leans on it is graded **analog**.

**The seam at 20.6 GPa is measured: +26 %.** IAPWS gives 715 K there and Reinhardt's line
interpolates to 903 K; in pressure, Reinhardt reaches 715 K at 16.5 GPa, 20 % below. The two
curves cross near 15–16 GPa, and splicing at the crossing was rejected: it would trade the
last five gigapascals of a measured curve for a simulation where both exist, and the splice
pressure would be ours rather than either source's. The splice is at the source's end, the
width is stated, and `test_interior.py` re-measures it. A column sitting in the disputed band
(715–903 K near 20.6 GPa) is named as such by the verdict.

**The same paper gives the boundary the dispatch needs.** Its ice VII′–VII″ coexistence line
(20–70 GPa, first order by the chemical-potential slope) separates the insulating bcc ices —
VII, VII′ and X, which the paper shows to be one thermodynamic phase — from ice VII″, the
superionic bcc solid that coexists with the liquid above ~1000 K. Below that line the column
is integrated on the condensed ladder (French & Redmer 2015); above it, VII″ and the liquid
alike go to Mazevet+ 2019's single-phase fit, which the paper says covers the superionic
regime, and the liquid line only decides the *name* (liquid or VII″) inside that. So the
material is chosen by the local (P, T) against two published lines, not by `body_class`, and
the verdict says which phase each end of the column got and how far from which line.

**Revisited against a measurement (F1, 2026-08-30).** Kimura & Murakami 2023
([`2023JChPh.158m4504K`](https://ui.adsabs.harvard.edu/abs/2023JChPh.158m4504K), PDF in
the cache) measure melting by Brillouin spectroscopy from 25.9 to 53.6 GPa, ±130–150 K per
point. With the criterion fixed beforehand (inside the measurement's own error), Reinhardt's
line sits inside it at six of seven melting points, and the one outside (25.9 GPa) has the
measurement 171 K *hotter* than the simulation — away from IAPWS. Their Simon–Glatzel fit
(their eq. (2), anchored on Queyroux+ 2020's triple point) puts 1028 K at 20.6 GPa, +14 % over
Reinhardt and +44 % over IAPWS's 715 K. The step is not an artefact of the simulation; the
splice, the seam number and the grade (analog — the check's own error is 8–11 % and does not
reach the seam) all stand, and `test_interior.py` re-runs the six-of-seven count.

**Above 52.4 GPa no liquid line is carried and none is invented.** The VII′–VII″ line reaches
70 GPa; past it the state is `undecided`, the representation is chosen by availability — the
ladder while its fit stands (to 1 TPa and 1800 K, both knot limits rather than phase
boundaries), Mazevet's fit beyond — and the verdict says "fluid or superionic" with the one
measurement that would place it: Millot+ 2018's "ice melts near 5,000 K at 190 GPa". Neptune's
adiabat is at 3 440 K there. A column with any sample past the curve is `molten` or
`undecided`, never `solid`.

Iron's melting curve is documented with its consumer, in
[core-state](core-state-methodology.md). Silicate has none here: a mantle solidus is a
different literature (a solidus and a liquidus for a mixture, not one melting point for a
pure compound), and `melt_free_phases()` names the silicate phases the way `cold_phases()`
names the phases without thermal constants.

### Hot water: the branch the ice giants needed

The ladder above is condensed insulating ice, and its fit stops at 1 TPa and 1800 K. An ice
giant's ice mantle is fluid from the base of its envelope down (Neptune: 39 GPa · 2 555 K, a
kilokelvin above Reinhardt's line) and climbs to 5500–6100 K at the centre, so it needs a
different phase rather than another rung. `water_hot.py` carries Mazevet+ 2019's analytic
free-energy fit, which covers liquid, plasma and superionic water in one object; Scheibe+ 2019
build their Uranus and Neptune models on it. Its floor is the paper's own, 1000 K at ρ ≳ 1 g/cc
(§3.1), and it is a different number from the ladder's 1800 K ceiling: which of the two
representations a given (P, T) gets is decided by the melting curve above, not by a hand-off
temperature. Until 2026-08-30 the two numbers were the same, 1800 K, and the class chose. Its constants come from the authors' reference implementation rather
than the paper, because the paper omits the explicit moderate-density term.

Two consequences follow from the fit being P(ρ, T) rather than a cold curve plus a thermal
correction. Temperature is an argument, so an isothermal ice giant is not available and the
recipe declines without a declaration. And the Fermi integrals it needs are evaluated from
their definition in `fermi.py`, not from the reference's Padé tables: the definition is the
canonical object, and the construction's own error is measured at 4.5 × 10⁻⁷.

Regenerated by `python3 engine/test_ice_giant.py --refresh` (about 50 s per planet since
the layer boundaries were interpolated inside the integration step, 2026-08-28; 1038 s
before) and printed from the frozen result by `--table`. `scripts/check.sh` solves both
planets live and compares them bit for bit with the frozen file, so a change that moves the
answer fails the gate and asks for a refresh. Where the 1038 s went is measured in
`engine/speed-context-notes.md`: not the Fermi integrals but a pressure shoot that could not
converge on a mass staircase.

| planet | R derived | R published | Δ | C/MR² | T_c | P_c | grade |
|---|---|---|---|---|---|---|---|
| Uranus | 4.930 R⊕ | 3.981 R⊕ | +23.8 % | 0.1358 | 5978 K | 1040 GPa | analog |
| Neptune | 4.992 R⊕ | 3.865 R⊕ | +29.2 % | 0.1439 | 10017 K | 1208 GPa | analog |
| Uranus, no H/He | 3.092 R⊕ | 3.981 R⊕ | −22.3 % | 0.3175 | 12370 K | 968 GPa | analog |

Compositions are Scheibe+ 2019's Table 1 rows built on this same water equation of state, so
the comparison borrows their structure rather than fitting our own. **The third row is the
result.** Both planets come out too large, and removing the H/He envelope overshoots the
other way, which brackets the measured radius and puts the error in the envelope: 13.8 % of
Uranus's mass in H/He adds 1.84 R⊕ on the n = 1 polytrope where the real envelope adds about
0.9. That polytrope is calibrated to Jupiter, and this is the same objection the ice-giant
refusal used to raise before the ices were in. Water alone standing in for all three ices is
field practice, and its cost is not quantified anywhere cited; the tables that would quantify
it are not reachable except by author request (C4, closed unbuilt 2026-08-30 — three routes
and why each fails are in `engine/interior-core.md`). What can be said is in three tiers:
the composition term widens the residual (the solar-ratio mixture's mean molecular weight is
17.28 against water's 18.02, a 4.27 % density overestimate at equal number density,
*derived*); the thermal term has a mechanism (more atoms per unit mass, a higher heat
capacity, a colder interior) but no defended sign once dissociation is in; the net needs the
tables.

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

## Giants: a published mixture table, and what the polytrope is still for

Until 2026-08-26 this recipe refused every giant planet, and the refusal named the reason
correctly: iron, silicate and the water ices are all condensed matter, and a
hydrogen-helium envelope is not. The answer was one more equation of state — first a
polytrope, and since 2026-08-28 the published mixture itself.

### The relation

The envelope reads two quantities out of a table: the density and the adiabatic gradient.

| | source | domain | representation | measured width |
|---|---|---|---|---|
| H/He mixture, Y = 0.275, Z = 0 | **Chabrier, Mazevet & Soubiran 2019**, ApJ 872, 51 | 1 bar – 10⁴ GPa, 100 – 25 119 K, above the reachable-envelope line | log ρ and ∇_ad on the distributed 0.05-dex grid, bicubic | ρ 2.0×10⁻³, ∇_ad 9.1×10⁻³ |

**Y = 0.275, not the Y_eff = 0.292 the same archive offers.** The second is that mixture
with Z = 0.017 folded into the helium so two components can stand in for three. This recipe
already carries `envelope_z` and mixes metals itself, so taking Y_eff would count them
twice — the trap this repository walked into with Jupiter's Z and with Earth's geotherm.

**∇_ad is read, not rebuilt.** Every other material here assembles its adiabatic gradient
from γ and K_S, because a Birch–Murnaghan phase has nothing else to offer. The table
carries (∂lnT/∂lnP)_S computed by the authors from their own entropy, so the recipe uses
it. That is also what gave the envelope a temperature at all: the polytrope had no thermal
constants, `cold_phases()` named it, and the declared potential temperature landed on the
top of the ice mantle instead of on the surface.

**A gas has no P = 0 surface.** Density goes to zero with pressure, and every published
giant radius is quoted at a pressure level. So the integration stops at the table's floor,
1 bar, and the declared `potential_temperature` is the temperature there — 165 K for
Jupiter, 135 K for Saturn, 76 K for Uranus (Voyager radio occultation). Below 100 K the
table stops; where a body's adiabat crosses that floor before reaching 1 bar, the surface
temperature is closed to the 1-bar level by the adiabat's own power law T ∝ P^∇_ad.

**Mixtures weight by heat capacity, not by volume.** Density mixes by additive volume, but
∇_ad is a derivative of the entropy and entropy is additive itself. Chabrier+ 2019 states
the rule as "the additivity of the extensive variables (volume, energy, **entropy**, …) at
constant intensive variables (P,T)", the same sentence this file already cites for density.
From that,

    ∇_ad,mix = Σ wᵢ c_P,ᵢ ∇_ad,ᵢ / Σ wᵢ c_P,ᵢ

with c_P for H/He read off the table's entropy columns and c_P for the metals closed from
constants already here as c_V(1 + αγT). Leaving this out was a silent defect rather than a
missing feature: without it a mixture fell back to the assembled γ/K_S gradient, which is
the thing the table was brought in to stop doing, and one part in fifty of metal put
Saturn's surface at 19 K instead of 135 K.

**The polytrope is still in the file, and it now does one job.** P = Kρ² with
K = 2.1 × 10⁵ SI (Helled, Movshovitz & Nettelmann 2022 §2,
[arXiv:2202.10046](https://arxiv.org/abs/2202.10046)) has a closed-form n = 1 solution
whose radius R = √(πK/2G) is independent of mass, which makes it a cheap density scale for
bracketing the shooting. It no longer supplies a density. **The constant carried a unit
trap and the paper's own arithmetic caught it**: the paper prints 2.1 × 10¹² labelled
m⁵ kg⁻¹ s⁻², which read as SI puts the radius at 1.49 AU, while read as cgs it converts to
2.1 × 10⁵ and gives 70,302 km against the 70,300 km the same paragraph states.
`engine/test_giant.py` re-runs both readings.

### Three limits, and one of them is composition

**Mass, by declaration and now also by the table.** `body_class` decides which branch
applies — `giant`, `gas_giant` and (since 2026-08-29) `sub_neptune` integrate; `brown_dwarf` and
`star` still decline, each naming what it would need. On top of that the baked window has a pressure
ceiling of 10⁴ GPa, which caps a pure H/He body at **519 M⊕ (1.63 M_J)**. That is lower
than the polytrope's declared 13 M_J fence and it is *our* window rather than the EOS's:
the distributed table runs to 10¹³ GPa, so baking more columns raises it.

**Temperature, on both sides.** The window is 100 – 25 119 K. Below it lies the region no
convective envelope reaches, where the distributed table also carries its own flaws — seven
cells with a sentinel where a density belongs, and grad_ad pinned at the ends of a clamp —
so the recipe declines there rather than repairing published numbers.

**Composition, which is the interesting limit.** With Z = 0 the model has no metals at all,
and Saturn comes out 7.1 % large. Guillot 1999 gives Saturn 19–31 M⊕ of heavy elements; the
envelope metallicity that reproduces the measured radius is now 0.0825, or 7.85 M⊕ — see the
[validation](#giants-checked-against-the-analytic-solution-and-against-two-planets) below.

**Which radius.** A non-rotating spherical model is compared against the **volumetric mean**
radius, not the equatorial one — rotation inflates Jupiter's equator by 2.3 % over its mean
and this recipe does not compute that. The anchors are the IAU/IAG values (Archinal+ 2011):
Jupiter mean 69,911 km against equatorial 1-bar 71,492 km, Saturn 58,232 against 60,268. The
validation table states both so no comparison silently changes convention.

## Practical recipe

1. **Choose the material stack** from `composition`. Four are defined: `earth_like`
   (CMF 0.325), `iron` (pure Fe(ε)), `silicate` (no metal), and `water` (50 % H₂O over an
   Earth-like rock). Numeric fractions passed explicitly override the preset.
2. **Mix the undifferentiated case.** `differentiated: false` is one rock-metal layer, not CMF = 0.
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

**Three layers make it a band, and the band is the answer.** A body with a metal core, rock
and a water column has two free fractions, and mass and radius fix only one. `infer_three_layer`
scans the core mass fraction (0, 0.15, 0.30, 0.45), solves at each the ice fraction that
reproduces the radius (with the ocean the declaration puts in it), and returns that family with
its C/MR² range: the engine narrows and does not pick. Given a measured C/MR² it narrows the
band to the one member that reproduces it, on the secant in core fraction, and says it did so on
a third observation; a value outside the band names the mechanism the band cannot reach
(above it, rock lighter than this silicate; below it, a larger core than the grid).

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
| Earth | 1.0030 | 1.0000 | +0.3 % | 0.3297 | 0.3307 | 0.3 % | 0.545 | 0.546 | 358.5 |
| Mars | 0.5318 | 0.5320 | -0.0 % | 0.3545 | 0.3644 | 2.7 % | 0.492 | 0.540 | 45.9 |
| Mercury | 0.3821 | 0.3829 | -0.2 % | 0.3388 | 0.3460 | 2.1 % | 0.795 | 0.828 | 38.2 |
| Moon | 0.2739 | 0.2727 | +0.4 % | 0.3945 | 0.3931 | 0.4 % | 0.206 | 0.201 | 5.7 |

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
| 1.0 | 0.325 | 1.0030 | 1.0018 | 0.0012 |
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
| `ice_iii` | P = 0, T = 251.15 K | 1126.3840 | 7.8349 | 6.7097 | 209.5 to 355.0 MPa | 0.002048 | 251.15 K | 0.006 %  |
| `ice_v` | P = 0, T = 256.43 K | 1207.8419 | 10.6368 | 6.7460 | 355.0 to 618.4 MPa | 0.002369 | 256.43 K | 0.014 %  |
| `ice_vi` | P = 0, T = 272.73 K | 1263.3858 | 10.3686 | 7.8219 | 618.4 MPa to 2.216 GPa | 0.003740 | 272.73 K | 0.118 %  |

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
real body. Five Solar System icy satellites, inverted from mass and radius: the two-layer
column (one free fraction, no temperature) beside the three-layer band (core, rock, water
column with the ocean the 270 K declaration puts in it), and whether the published C/MR² lies
inside that band:

| moon | ρ̄ (kg/m³) | two-layer C/MR² | three-layer band (core 0 → 0.45) | published | inside? | narrowed by C/MR² | source |
|---|---|---|---|---|---|---|---|
| Ganymede | 1936 | 0.3179 | 0.2836 – 0.3128 | 0.3115 | yes | core 0.008 · ice 0.421 · ocean 500 km / shell 24 km | Schubert+ 2004 (Anderson+ 1996) |
| Callisto | 1834 | 0.3158 | 0.2856 – 0.3119 | 0.3549 | no | outside the band: rock lighter than this silicate — and than antigorite (C10) | Anderson+ 2001 |
| Titan | 1880 | 0.3172 | 0.2853 – 0.3126 | 0.3414 | no | outside the band: rock lighter than this silicate — and than antigorite (C10) | Iess+ 2010 (Cassini) |
| Europa | 3014 | 0.3793 | 0.2774 – 0.3655 | 0.3460 | yes | core 0.070 · ice 0.078 · ocean 104 km / shell 26 km | Anderson+ 1998 |
| Enceladus | 1610 | 0.3051 | 0.2682 – 0.3008 | 0.3350 | no | outside the band: rock lighter than this silicate — and than antigorite (C10) | Iess+ 2014 (Cassini) |

**Two of the five are now inside, and the ocean is what moved them.** Ganymede's band starts at
0.3128 with no core, 0.4 % from the measurement where the two-layer column was 2.1 % high:
500 km of liquid replaced ices III, V and VI, which are denser, so the column lightened and
the moment of inertia came down. Europa's column is ice Ih and liquid only (there the liquid
is the denser), and what brought it inside was the iron core the two-layer inversion could
not express; C/MR² narrows it to a 7 % core under a 104 km ocean and a 26 km shell.

**The other three are outside the band, above it, and that is a different sentence from the one
this table used to carry.** Every member of every band lowers C/MR² as the core grows, so a
published value above the zero-core end cannot be reached by any layering: the mass must be
*less* centrally concentrated than rock over water allows, which means the rock itself is
lighter than the silicate this recipe carries (hydrated or porous, the published reading for all
three) or is partially differentiated. The reason is a **material**, not a missing layer. At
Enceladus the 270 K declaration puts no ocean in a 10 MPa column at all (ice Ih melts above
272 K there), so that row is the two-layer answer with a core axis, and porosity is live too.

**Measured on 2026-08-30 (C10): hydrated rock alone does not reach them.** The rock now has a
declared serpentinisation axis — antigorite (Hilairet+ 2006, ρ₀ 2640.5 kg/m³ derived) mixed
by additive volume into the enstatite/PREM silicate, two solids as grains — and the
three-layer band was re-run on the three moons at fractions 0, 0.25, 0.5, 0.75 and 1
(`test_interior.py --serpentine`). The band's top (the zero-core end) rises with the fraction
and **stays under the published value at every fraction, including fully serpentinised rock**:

| moon | published | band top at f = 0 | 0.25 | 0.5 | 0.75 | f = 1 | fraction in [0, 1] that closes it |
|---|---|---|---|---|---|---|---|
| Callisto | 0.3549 | 0.3119 | 0.3165 | 0.3213 | 0.3265 | 0.3321 | none — 0.023 short at f = 1 |
| Titan | 0.3414 | 0.3126 | 0.3172 | 0.3222 | 0.3276 | 0.3334 | none — 0.008 short at f = 1 |
| Enceladus | 0.3350 | 0.3008 | 0.3058 | 0.3109 | 0.3162 | 0.3216 | none — 0.013 short at f = 1 |

So "rock lighter than this silicate" is now a measured sentence with a limit: lightening the
rock all the way to pure antigorite closes 40–75 % of each gap and no more. What remains is
not a composition on this axis; it is **void space** — C9's branch, porosity retained on a
heated body — or a partial differentiation that C7 declined to model. Two items answer one
question from two sides. No fraction was chosen to close anything; the grid is the report.
(At f > 0 the band collapses to its zero-core member on Callisto and Titan: with a lighter rock
no core fraction on the grid reproduces the radius, which is the same statement.)

The table is regenerated by `python3 engine/test_interior.py --icy` (about twenty minutes);
the default run asserts Ganymede's two-layer row and Europa's three-layer narrowing.

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

**Against the analytic solution — and the sign of this check flipped on 2026-08-28.** While
the envelope was a polytrope the test asserted that the radius does *not* move with mass,
because that is the signature of n = 1. With the table in, that insensitivity would be a
defect, so the test asserts the opposite: the radius moves 22 % across 95 to 500 M⊕ where
the polytrope moved 0.00004 %. The same inversion applies to C/MR², which now sits 6.5 %
away from the Lane–Emden value that used to be the answer.

**Against the published number, which is also the unit check.** K still gives 70,302 km
against the 70,300 km Helled+ 2022 §2 states, and the same digits read as SI give 1.49 AU.
The test asserts both. The constant no longer supplies a density — it is the bracketing
scale — but the trap is still worth a standing check.

**Against four planets.** Regenerated by `python3 engine/test_giant.py --table`; the ice
giants by `python3 engine/test_ice_giant.py --table` (from the frozen anchor; `--refresh`
recomputes it).

| body | M (M⊕) | T at 1 bar | R derived | R mean (IAU) | ΔR | C/MR² | T_c (K) | P_c (GPa) | before |
|---|---|---|---|---|---|---|---|---|---|
| Jupiter | 317.8 | 165 K | 69333 km | 69911 km | **−0.83 %** | 0.2774 | 14314 | 3453 | +0.6 % |
| Saturn, Z = 0 | 95.2 | 135 K | 62344 km | 58232 km | **+7.06 %** | 0.2710 | 6930 | 481 | +20.7 % |
| Uranus | 14.5 | 76 K | 4.199 R⊕ | 3.981 R⊕ | **+5.48 %** | 0.1741 | 6160 | 1220 | +23.8 % |
| Neptune | 17.1 | 72 K | 4.210 R⊕ | 3.865 R⊕ | **+8.94 %** | 0.1799 | 6296 | 1533 | +29.2 % |
| Alpha Centauri A b | 120.0 | 165 K (declared) | 64934 km | – | – | 0.2697 | 8930 | 659 | – |

The T_c column went in on 2026-08-30 (C5): Neptune's central temperature lived only in
`engine/ice_giant_anchor.json` and went missing when the core list was first written. The
giants' rows are regenerated by `python3 engine/test_giant.py --table`, the ice giants' by
`test_ice_giant.py --table`.

**Jupiter got slightly worse, and that is the evidence rather than a regression.** The old
+0.6 % came from a constant fitted to Jupiter; −0.83 % is what a published mixture says
about the same planet with nothing left to tune. The sign flipped and the magnitude did
not, which is what a fit looks like when it is replaced by a prediction. Its central
temperature comes out 14 300 K.

**Saturn's fitting metallicity moved, and that was the question worth asking.** Under the
polytrope the envelope needed Z = 0.200 — 19.0 M⊕, sitting exactly at the bottom edge of
Guillot 1999's 19–31 M⊕ budget — to reach the measured radius. With the table it needs
**Z = 0.0825, or 7.85 M⊕**, which is *below* that budget. The old value was doing two jobs
at once: supplying Saturn's metals and compensating an envelope the polytrope drew three
times too fluffy. The comparison is not like for like, because this model has no core and
so must put every metal in the envelope while Guillot's budget is a total; what is
unambiguous is that the requirement fell by a factor of 2.4.

**Uranus is the gate this work was measured against**, and it moved from +23.8 % to +5.48 %
with a central temperature of 6 160 K against the 5 700 K of Scheibe+ 2019 — an 8 %
overshoot in the same direction as the radius. Neptune declined on the morning this table was
first made (its envelope base landed 3 K under the hot-water floor); once the layer boundary
was interpolated inside the integration step (2026-08-28, `engine/speed-context-notes.md`
§11) it landed above the floor and integrated at +8.97 % — by luck, it turned out: the 1-bar
temperature was a jagged function of the central temperature (±0.4 K, the adiabatic gradient
used to close the last extrapolation being read at a grid-bound step start), and that trial
path happened to sit in a trough. Since 2026-08-30 the gradient is read at the exit point
itself and the temperature loop keeps its best pass, and Neptune converges at +8.94 % with a
central temperature of 6 296 K, its envelope base fluid for a stated reason
(`engine/melting-curve-context-notes.md`). Whether the excess belongs to the ices or to the
envelope is not analysed here; the number is anchored and measurable.

**A heavy-element core no longer fits inside Jupiter at all, and that is the envelope
getting heavier.** With the polytrope a Jupiter-mass giant integrated a silicate core up to
17.66 M⊕ before the envelope's overburden pushed the silicate past its 13.5 TPa ceiling.
The table makes the envelope denser at depth — Jupiter's own central pressure is 3.45 TPa —
and the ceiling is now reached with no core at all. What blocks it is unchanged (the
silicate fit's ceiling, loaded by the envelope); the load is larger.

**Jupiter's moment of inertia, and why this document names one value out of three.** Three
numbers circulate and they are not equally grounded.

| value | where it comes from | why it is not the anchor |
|---|---|---|
| 0.254 | the NASA Jupiter fact sheet lineage | an ADS-indexed full text notes that this value "actually translates into λ = 0.243 when it is normalised using R_eq", so its normalising radius is ambiguous |
| 0.2756 | Ni 2018 ([`2018A&A...613A..32N`](https://ui.adsabs.harvard.edu/abs/2018A%26A...613A..32N)), re-quoted by later papers as "a Jupiter-like value determined from the Juno probe" | its full text was not reachable from here, so whether that paper *infers* it or *scans* it as an input could not be confirmed. What could be confirmed is that no interior-model study read in full produces it, and that it sits 4.5 % above the ones that do |
| **0.2634 to 0.2644** | Neuenschwander+ 2021 ([arXiv:2101.12508](https://arxiv.org/abs/2101.12508)) get 0.2634 < MoI < 0.2639 from piecewise-polytropic profiles fitted to the Juno gravity field, and quote Wahl+ 2017 at 0.2640 to 0.2644 | **this is the anchor.** Post-Juno, fitted to the measured field, two independent studies, and the union sits inside the 0.2629 to 0.2645 that Helled+ 2011 ([arXiv:1109.1627](https://arxiv.org/abs/1109.1627)) obtained separately |

The coreless table model gives **0.2774, 4.9 % above** the anchor band, and above is the
right side to be on: this is a non-rotating homogeneous H/He sphere with no core and no
metals, so its mass is less concentrated inward than real Jupiter's and C/MR² must come out
high. The polytrope's 0.2614 looked closer, but that number was a property of n = 1 rather
than a statement about Jupiter — it is the same 0.2614 for every giant. The test asserts the
sign and the size, not membership of the band.

### Temperature, checked against a published core-mantle boundary

The adiabat has no anchor of its own, so it is checked against someone else's. Unterborn+
2019 ([arXiv:1905.06530](https://arxiv.org/abs/1905.06530)) fit their models' CMB temperature
to a cubic in radius at 1600 K potential temperature (eq. 7, valid 0.75 to 1.5 R⊕) with a
shift for other anchors (eq. 8); at 1 R⊕ it returns 2635 K, which they call "in good
agreement" with Lay+ 2008's 2500 to 2800 K for Earth. Regenerated by
`test_interior.py --thermal`:

| body | T_Pot (K) | T_CMB derived | Unterborn+ 2019 eq. 7–8 | Δ | R | C/MR² | grade |
|---|---|---|---|---|---|---|---|
| Earth (reference) | 1600 | 2526 K | 2642 K | -4.4 % | 1.003 R⊕ | 0.3297 | calibrated |
| Earth, cool mantle | 1400 | 2191 K | 2273 K | -3.6 % | 1.001 R⊕ | 0.3302 | analog |
| Earth, hot mantle | 1900 | 2969 K | 3198 K | -7.2 % | 1.006 R⊕ | 0.3290 | analog |
| 2 M⊕ super-Earth | 1600 | 2884 K | 3186 K | -9.5 % | 1.216 R⊕ | 0.3247 | analog |
| 4 M⊕ super-Earth | 1600 | 3331 K | 4010 K | -16.9 % | 1.461 R⊕ | 0.3178 | analog |

**Earth's 2526 K lands inside the measured band, and the drift above it is a limit rather
than a tolerance.** The residual grows with radius because holding αK_T volume-independent
makes γ fall as 1/ρ, while a Debye treatment of α(P,T) and C_P(P,T) lets it fall more
slowly. The test pins the near field at 5 % and the far field into a recorded band, and the
domain row declares 1.05 R⊕ as where this branch stops being checked.

**A second anchor, and the engine sits between the two (C8, 2026-08-30).** Noack &
Lasbleis 2020 ([`2020A&A...638A.129N`](https://ui.adsabs.harvard.edu/abs/2020A%26A...638A.129N), the PDF in the cache) parameterise their own
interior-structure model for Earth-like planets over 0.8–2 M⊕ and carry the mantle adiabat
to the core–mantle boundary in their eq. (22): `T_CMB = T_um · exp(dT · g_m,av α_m,av /
C_p,m,av · (R_p − R_c − D_l))` with `T_um = 2000 K` at the base of a 250 km lithosphere and an
empirical `dT ≈ 0.5`, the mantle averages from their eqs. (15), (18) and (19). Every constant
was read from the PDF. Their eqs. (20) and (21) are **not** used: those are initial,
post-magma-ocean temperatures built to exceed the literature by thousands of kelvin, a claim
about early planets and not a present-day adiabat. Evaluated in the engine's own geometry
(its R_p and R_c) and in the paper's (eqs. 5 and 9), regenerated by
`test_interior.py --adiabat`:

| M (M⊕) | R (R⊕) | engine T_CMB | eq. (22), engine R_p, R_c | Δ | eq. (22), paper R_p, R_c | Δ | Unterborn eq. 7 | Δ |
|---|---|---|---|---|---|---|---|---|
| 0.8 | 0.942 | 2430 K | 2485 K | −2.2 % | 2536 K | −4.2 % | 2503 K | −2.9 % |
| 1.0 | 1.003 | 2526 K | 2563 K | −1.4 % | 2622 K | −3.7 % | 2642 K | −4.4 % |
| 1.2 | 1.056 | 2611 K | 2637 K | −1.0 % | 2702 K | −3.4 % | 2767 K | −5.6 % |
| 1.5 | 1.123 | 2724 K | 2742 K | −0.7 % | 2814 K | −3.2 % | 2936 K | −7.2 % |
| 2.0 | 1.216 | 2884 K | 2906 K | −0.8 % | 2984 K | −3.3 % | 3186 K | −9.5 % |

The Earth point, 2563 K from the paper's constants in the engine's geometry, reproduces the
2562 K an independent reading of the paper reported — a transcription check of the kind
Seager's Table 3 gives the EOS. Across the whole window the engine is 0.7–2.2 % under
eq. (22) and 2.9–9.5 % under Unterborn's cubic, while **the two published estimates disagree
with each other by 4.4–9.7 % from 1 to 2 M⊕**; the engine sits between them. That is what the
grade above 1.05 R⊕ now rests on: a measured spread, not an absence. One caveat is measured
rather than hidden: the agreement in absolute CMB temperature is partly the cancellation of
two differences — the paper starts 2000 K at 250 km where the engine's adiabat is at
1736 K, and the engine's rise from that depth to the CMB is 12–14 % steeper than the paper's
damped exponent (`dT = 0.5` is their empirical correction for using mantle averages). The
test pins both numbers. **Above 2 M⊕ (1.22 R⊕) the paper's own ceiling is reached** and the
recipe is back to one anchor; that is now a stated boundary rather than a silence.

**A second check needs no planet.** The thermal term reproduces, from an independent
constant, the ice-ladder numbers recorded above: 0.107 %, 0.267 % and 1.283 % for ices III,
V and VI against the 0.11 %, 0.27 % and 1.3 % measured earlier against SeaFreeze. Those were
the honest error width of an isothermal treatment; they are now a computed consequence.

### Mixtures, checked on Saturn and on a discrimination

Heavy-element masses are Guillot 1999's constraints, 11 to 42 M⊕ for Jupiter and 19 to
31 M⊕ for Saturn, divided by the planet mass. Nothing is tuned: Z = 0.200 is the **bottom
edge** of the published Saturn budget, taken as a boundary. Regenerated by
`python3 engine/test_mixture.py --table`:

| body | Z (M⊕) | Z fraction | R derived | R mean (IAU) | ΔR | C/MR² | grade |
|---|---|---|---|---|---|---|---|
| Jupiter | 0 | 0.000 | 69333 km | 69911 km | -0.8 % | 0.2774 | analog |
| Jupiter | 11 | 0.035 | 67504 km | 69911 km | -3.4 % | 0.2780 | analog |
| Jupiter | 26 | 0.083 | 64936 km | 69911 km | -7.1 % | 0.2790 | analog |
| Jupiter | 42 | 0.132 | 62407 km | 69911 km | -10.7 % | 0.2798 | analog |
| Saturn | 0 | 0.000 | 62344 km | 58232 km | +7.1 % | 0.2710 | analog |
| Saturn | 19 | 0.200 | 52541 km | 58232 km | -9.8 % | 0.2805 | analog |
| Saturn | 25 | 0.263 | 49551 km | 58232 km | -14.9 % | 0.2836 | analog |
| Saturn | 31 | 0.326 | 46610 km | 58232 km | -20.0 % | 0.2867 | analog |

**Saturn's fitting metallicity left the published budget, and that is the interesting
result.** Under the polytrope Z = 0.200 — the bottom edge of Guillot's 19–31 M⊕ — put Saturn
at −0.1 %. With a real envelope the same Z overshoots to −9.8 %, and the radius is matched at
**Z = 0.0825, or 7.85 M⊕**, below the budget. The old agreement was a coincidence of two
errors: a polytrope that inflated the envelope and a metal fraction large enough to squash
it back. Two caveats keep this from being a contradiction of Guillot. This model has no core,
so every heavy element must sit in the envelope while Guillot's number is a total; and heavy
elements spread evenly are not their real distribution, since post-Juno models favour a
**diluted core** graded inward. Both push the same way.

**Jupiter now gets monotonically worse with Z**, from −0.8 % at Z = 0 to −10.7 % at 42 M⊕,
and unlike before that is no longer a double-count of a Jupiter-fitted constant — the table
is not fitted to Jupiter. It is the same missing distribution: uniform metals over-compress a
planet whose metals are concentrated. C/MR² moves the same way for the same reason, away from
the 0.2634–0.2644 anchor band rather than into it.

**Adding Z now moves the mass axis too.** With the polytrope R = √(πK/2G) had no M in it, so
two giants of the same Z received the same radius; the table responds to mass, composition
and temperature separately, and the sweep above shows the composition axis alone.

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
| rock + ice VII | ice column base above 2.216 GPa and below 37.4 GPa | integrates, ice VII. Since 2026-08-27 it carries thermal pressure as well: with a temperature declared the density there moves, and with none it is unchanged bit for bit | calibrated |
| rock + ice III / V / VI | ice column base in 209.5 MPa – 2.216 GPa | integrates, switching phase at each triple point | calibrated |
| **ocean** | ice column below 2.3 GPa with a `potential_temperature` declared | **integrates the liquid** wherever the local (P, T) is above the IAPWS melting curve, on SeaFreeze `water1`; returns `ocean_thickness` and `ice_shell_thickness`, and `ice_column_state` is `solid` or `molten`. The thickness is set by the declaration | analog |
| **liquid above 2.3 GPa** | a column warm enough to melt ice VII | **declines**, naming the shelf: `water1` ends at 2.3 GPa and `water2` (Brown 2018) is not baked | — |
| **ice with no temperature declared** | any ice column, `potential_temperature` unset | `ice_column_state: undecided`. The curve and the pressures are both there; nothing flows without the declaration | — |
| porous rock or ice | `initial_porosity` > 0, central pressure inside the 150 MPa experimental ceiling | integrates with φ(P) from the published relation | analog |
| **porosity above the experimental ceiling** | `initial_porosity` > 0, pressure above 150 MPa | the relation is **extrapolated**: results report the mass fraction affected, and `porosity_cap` gives the reading that claims nothing there | analog |
| **porosity on a heated body** | `initial_porosity` > 0 and the body has melt, differentiation, convection, impacts or tidal heating | **not decided here**: all five remove porosity (Bierson+ 2019 §2.2), so what this recipe returns is an upper bound on the voids, never an estimate. **A relation exists for three of the five, and it depends on rheology** (C9, closed 2026-08-30): Neumann & Kruse 2019 (open access, full text in the cache) carry tidal heating, differentiation and melting for Enceladus and compact the core by creep (their §2.5, creep laws of Mei & Kohlstedt 2000 for olivine and Amiguet+ 2012 for antigorite, coefficients in their Table 3), retaining a porous core layer of 4–70 km for olivine and **none for antigorite**. It is one body at one size and needs a thermal history this recipe does not integrate, so it is recorded as a branch — reached, specified, no consumer yet; Bierson's bound stays the general case (validated over 123–2326 km). Convection and impacts are still carried by nobody | — |
| **rock + ice X** | ice column base in 37.4 GPa – 1 TPa | integrates on `ice_x`, at grade **analog** with a note: this is the one ice rung fitted rather than read, holding its source to 1.475 % against the others' 0.006–0.118 %, and its source is a first-principles potential rather than measured compression | analog |
| **ice above 1 TPa** | ice column base above 1 TPa | **declines**, naming what ended: the representation's knot domain, not the physics. Zeng & Sasselov 2013 carry the same family of data to 8.893 TPa before handing over to Thomas–Fermi–Dirac, so roughly a factor of nine of published headroom sits above this fence | — |
| **superionic** | ice column above the VII′–VII″ line (20–70 GPa), or above 52.4 GPa and 1800 K | **integrates on the hot-water fit**, which Mazevet+ 2019 state covers the superionic regime as one phase with the liquid, and the verdict names it: ice VII″ where Reinhardt's lines place it, "fluid or superionic" where no line reaches (above 52.4 GPa the liquid line ends; Millot+ 2019 put superionic water above 100 GPa and 2000 K, Millot+ 2018 melt it near 5000 K at 190 GPa). The ladder never returns ice X where the material is superionic; French & Redmer 2016's potentials would make the superionic solid a phase of its own | analog |
| temperature at or below the reference declaration | `potential_temperature` unset, or set to 1600 K | unset carries no temperature and returns the isothermal answer bit for bit; 1600 K integrates the adiabat and returns `core_temperature` / `cmb_temperature` with ΔT identically zero, so density does not move either way | unchanged |
| **temperature declared away from the reference** | `potential_temperature` ≠ 1600 K | integrates with thermal pressure. The answer now leans on a declaration this recipe cannot derive, and the adiabat holds only where the layer convects: tidal heating and internal thermal boundary layers make the real profile super-adiabatic (Unterborn+ 2019 §3.2) | analog |
| **temperature on a body above 1.05 R⊕** | `potential_temperature` declared at any value | integrates, and the adiabat is checked against **two** published estimates that disagree with each other: Unterborn+ 2019 eq. 7 (engine −4.4 % at 1 R⊕, −9.5 % at 1.22 R⊕, −17 % at 1.46 R⊕) and Noack & Lasbleis 2020 eq. (22) (engine −2.2 to −0.8 % over 0.8–2 M⊕); the two anchors differ by 4.4–9.7 % from 1 to 2 M⊕ and the engine sits between them (C8, measured 2026-08-30). The grade drops by that spread even where density did not move, because `core_state` consumes the number. **Above 2 M⊕ (1.22 R⊕) the second anchor ends** and only Unterborn's cubic remains, to 1.5 R⊕ | analog |
| **deep silicate (3.5 to 13.5 TPa)** | the silicate layer's base passes 3.5 TPa | integrates on `mgsio3_pv`, at grade **analog** with a note: below 3.5 TPa the silicate is a fit to a measured planet (PREM), above it a DFT calculation extrapolated through a dissociation | analog |
| electron degeneracy | central pressure above the core material's ceiling | declines, naming Thomas–Fermi–Dirac | — |
| undifferentiated rock + metal | `differentiated: false` with no ice or gas | integrates one mixed layer by the same rule. No measured C/MR² anchor exists for such a body, so the check is a discrimination: undifferentiated Mercury does not reproduce the measured value | analog |
| **undifferentiated with ice or gas** | `differentiated: false` and `ice_mass_fraction` or `gas_mass_fraction` > 0 | **declines**, and the reason is structural rather than a missing rule (C7, closed 2026-08-30): water mixed into silicate is a **reaction** — hydrated minerals with their own density, volume change and heat — and what makes a body neither fully mixed nor fully layered is a **transport history**, how far the water got. The literature models that as thermal evolution (Malamud & Prialnik 2015, 2013; Prialnik & Merk 2008 — abstracts only, full texts paywalled), not as a composition a hydrostatic solver takes. No mixing rule for an ice-bearing layer was found and no published bound on the error of using one. This does **not** cover C10: antigorite with enstatite is two solids as grains, and volume additivity between them is the rock–metal rule's own shape | — |
| **too light for any rock/ice mix** | mean density below the porous envelope | **declines**, saying the declared mass-radius pair is outside what the published relation allows | — |
| gas giant | `body_class` is `giant` or `gas_giant`, a `gas_mass_fraction`, and a declared `potential_temperature` (the 1-bar level) | integrates, H/He envelope on the Chabrier+ 2019 table, stopping at 1 bar because a gas has no P = 0 surface. Jupiter −0.83 %, Saturn at Z = 0 +7.06 % | analog |
| **gas giant with no temperature declared** | as above, `potential_temperature` unset | declines: the table is a function of (P, T), so there is no isothermal path the way there was for a polytrope | — |
| **gas envelope past 10⁴ GPa** | pure H/He above about 519 M⊕ (1.63 M_J) | declines at the baked window's pressure ceiling. The distributed table runs to 10¹³ GPa, so this is our window and not the EOS's | — |
| **envelope colder than convection reaches** | below log T = 2.72 + 0.257 log P, or below 100 K | declines. That region is where the distributed table carries its own flaws — seven sentinel densities and grad_ad pinned at the ends of a clamp — and no convective envelope reaches it; the published numbers are left alone rather than repaired | — |
| metal-rich giant | as above with `envelope_z` > 0, central pressure under the Z carrier's ceiling | integrates. Density mixes by additive volume; **∇_ad mixes by heat capacity**, which is what entropy additivity gives. Saturn reaches its measured radius at Z = 0.0825 (7.85 M⊕), below Guillot's 19–31 M⊕ total — and this model has no core to put them in | analog |
| **giant whose centre passes the Z carrier's ceiling** | `envelope_z` > 0 and central pressure above 13.5 TPa | **declines**, naming the component whose fit ended rather than reporting degeneracy. Jupiter's whole Guillot range now integrates (centres of 4.3 to 5.8 TPa); the branch runs out at Z = 0.383, or 122 M⊕ of heavy elements | — |
| **diluted core** | heavy elements graded inward rather than uniform through the envelope | **not decided here**: this rule mixes one homogeneous Z, and the residual after it belongs to the distribution | — |
| **large rock core in a giant** | heavy elements placed as a compact core whose base passes 13.5 TPa. In a Jupiter-mass giant that is a core above **11.5 M⊕** (measured 2026-08-29; the polytrope envelope allowed 17.7, and the "0 M⊕ since the table" of 2026-08-28 was the envelope-base defect fixed with the sub-Neptunes, not physics) | **partly open**: cores below that integrate at grade analog; above it the recipe declines, naming the silicate ceiling. The limit is the envelope's overburden, not the core's own weight, so it depends on the pair rather than on the core mass | analog |
| ice giant | `body_class` is `ice_giant`, with an ice fraction and a declared 1-bar temperature | **integrates**, ice mantle on `h2o_hot` (Mazevet+ 2019) between the rock and the H/He envelope. Uranus comes out **+5.48 %** with a central temperature of 6 160 K against Scheibe+ 2019's 5 700 K, Neptune **+8.94 %** (6 296 K); before the envelope table they were +24 % and +29 % | analog |
| **ice material chosen by (P, T), not by class** | any body with water above 2.3 GPa and a declared temperature | the ice layer's material is decided per step by the local state against two published lines: IAPWS's melting curve to 20.6 GPa, then Reinhardt+ 2022's liquid line (to 52.4 GPa) and VII′–VII″ line (to 70 GPa). Neptune's envelope base at convergence is 39 GPa · 2 555 K, **999 K above the liquid line**, so it is fluid for a stated reason; its "1797 K, three kelvin under the floor" was a trial path, and the converged point never sat there. `body_class` no longer picks the material; it only requires a temperature and an ice fraction of an ice giant. The lines are simulation (grade analog), and above 70 GPa no line reaches | analog |
| **ice giant with no declared temperature** | `body_class` is `ice_giant`, `potential_temperature` unset | **declines**: the hot-water fit is P(ρ, T) as one object, so temperature is an argument rather than a correction, and at fixed pressure 2000 K against 5700 K is 14 % in density at 30 GPa | — |
| **thermal boundary layer** | `boundary_temperature_jump` > 0 on a body with an ice mantle, a gas envelope and a declared 1-bar temperature | **integrates**, the interior warmer by the declared step across the mantle/envelope boundary (Nettelmann+ 2016's stably stratified TBL; their U15-II 2500 K, U15-III 4700 K, near 0.1 Mbar — this recipe's boundary sits where the composition puts it, 30–40 GPa for the anchors). A declaration: the layer's stability and width are thermal history. A warmer interior is less dense, so the step **enlarges** a planet the adiabatic model already makes too large; it closes nothing by itself | analog |
| **rock in the ice mantle** | `mantle_rock_fraction` > 0 with a declared temperature | **integrates**, silicate mixed by additive volume into every water phase above the ocean table's 2.3 GPa, ∇_ad weighted by c_P (the hot-water fit gained c_P and ∇_ad from its own P and U for this). A declaration: the ice:rock ratio is formation, and Nettelmann+ 2016 write that the mixing behaviour of rocks with ices "is not well-understood". Denser, so it **shrinks** the planet | analog |
| **serpentinised rock** | `serpentinisation` in (0, 1] on a differentiated body | **integrates**, the rock layer a volume-additive mixture of the enstatite/PREM silicate and antigorite (Hilairet+ 2006 BM2 to 10 GPa; ρ₀ derived, not printed) — two solids as grains, the rock–metal rule's own shape and not the reaction C7 declined. A declaration: how far the water got is history. antigorite carries **no thermal term** (room temperature only; Holland & Powell 1998 requested), so temperature passes through that component and the grade is set by that deficiency, not by the fit. Above 10 GPa the antigorite end declines by name (dehydration). On Callisto, Titan and Enceladus no fraction in [0, 1] reaches the published C/MR² | analog |
| **hot water outside its fit** | a liquid below 1000 K above 2.3 GPa (or above 500 K below it), or any water above 50 000 K | **declines** by name at both ends. The floor is Mazevet+ 2019 §3.1's own for ρ ≳ 1 g/cc ("10³ K ≲ T"), and a liquid under it has no equation of state here — the shelf is SeaFreeze `water2` (Brown 2018); the refusal is thrown as too cold, since the fluid opens above. The ceiling is the paper's 50 000 K | — |
| sub-Neptune | `body_class` is `sub_neptune`, a declared `gas_mass_fraction` and a declared 1-bar temperature | **integrates**: iron core, rock, H/He envelope on the same integrator as the giants. The gas fraction is the seventh declaration (age and irradiation set it; no evolution here) and drops the grade. GJ 1214 b at 2 % H/He reaches its radius with 300 K at 1 bar, inside Valencia+ 2013's < 7 % | analog |
| **envelope hotter than the mass binds** | any H/He envelope whose 1-bar adiabat is too hot for the body | **declines**, citing the hottest bound solution and the temperature above which the 1-bar level is never reached: the declared adiabat from 1 bar puts the envelope base above what the core can hold. A radiative zone would lower the deep adiabat, and this recipe has none | — |
| brown dwarf | `body_class` is `brown_dwarf` | declines, naming deuterium burning above ~13 M_J (Spiegel+ 2011) and the age-dependent luminosity this recipe has no track for | — |
| star | `body_class` is `star` | declines: the stellar C/MR² is the n = 3/2 polytrope value 0.205 (Chandrasekhar 1939) on a separate `body_figure` branch, untouched here | — |

Two of those rows are a mass limit. The limit is a property of the material rather than of
any body, so it is measured rather than asserted (`test_interior.py --ceiling`):

| composition | mass ceiling | what stops it | its stated ceiling | R at the ceiling | C/MR² |
|---|---|---|---|---|---|
| earth_like (CMF 0.325) | 22.79 M⊕ | `fe_prem` | 12.0 TPa | 2.208 R⊕ | 0.2959 |
| pure silicate (CMF 0) | 53.38 M⊕ | `silicate` | 13.5 TPa | 2.856 R⊕ | 0.3291 |
| pure iron (fe_eps) | 24.92 M⊕ | `fe_eps` | 20.9 TPa | 1.717 R⊕ | 0.3364 |
| water (ice 0.50, ice is the outer layer) | 21.29 M⊕ | `h2o` | 1.0 TPa | 2.700 R⊕ | 0.2771 |

Out of domain is a **returned value**, not an error: each row comes back with its reason
attached, so a body that cannot be derived says why instead of being extrapolated.

Three of those rows are refusals the previous revision could not phrase, and the phrasing is
the deliverable:

**Undifferentiated is not CMF = 0.** Setting the core mass fraction to zero says there is no
metal. An undifferentiated body has metal that never segregated, so it sits mixed through
the silicate. This solver stacks pure materials layer by layer and has no way to express a
mixed phase; what it would need is a mixture equation of state (volume-additive, or a
Voigt–Reuss–Hill average). That is the named starting point, and with it the body solves.

**Porosity is not ice, and both are modelled.** Both lower the mean density, and at the
central pressures of a few-hundred-kilometre body both are live, so mass and radius alone
cannot separate them: a body whose board excludes ice is solved on the porosity axis, one
whose board allows it on the ice axis, and every result names the degeneracy. The recipe
will not pick between them from density, because density does not contain that information.

**A missing phase was not a missing layer.** The ladder runs unbroken from ice Ih to
ice X and the test asserts the contiguity; the ocean is likewise not a layer but a phase of
the same column. What remains above the ladder is the superionic phase, declined by
temperature rather than by pressure.

## What the roster asks for

Six moons in the Alpha Centauri and Proxima systems have both a mass and a radius on the
board, and four of them sit below 3000 kg/m³, which two revisions ago was refused outright.
Running the inversion on all six:

| body | ρ̄ (kg/m³) | ice declared | outcome | what it took, or what is missing |
|---|---|---|---|---|
| Pandora (A b III) | 4901 | allowed | solved | solved — core_mass_fraction 0.255, C/MR² 0.3384, P_c 220804 MPa |
| Cassandra (A b IV) | 5467 | allowed | solved | solved — core_mass_fraction 0.654, C/MR² 0.3311, P_c 81805 MPa |
| Hades (A b II) | 2829 | **excluded** | solved | solved — initial_porosity 0.478, C/MR² 0.3742, P_c 738 MPa |
| Dante (A b I) | 2620 | **excluded** | solved | solved — initial_porosity 0.389, C/MR² 0.3771, P_c 317 MPa |
| Chaos (A b V) | 2014 | allowed | solved | solved — ice_mass_fraction 0.239, C/MR² 0.3150, P_c 162 MPa |
| Proxima Cen c I | 1599 | allowed | solved | solved — ice_mass_fraction 0.403, C/MR² 0.3052, P_c 85 MPa |

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
fraction. Nothing here changes the board: it reports. (Since 2026-08-30 the second reading has
a tool — the `serpentinisation` axis, C10 — and the question is the owner's; it is not run
here.)

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
| C/MR² | 0.23 | 0.2874 | **+24.9 %** |
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

What survives is a narrower claim, and it is still worth having: **0.23 has no source and
0.2874 has one.** The 0.2874 is what the physics predicts for a body with no substantial
core, and 0.23 is what a large concentrated core would give; which is right for a fictional
planet this recipe cannot settle. The caveat travels with it: the coreless polytrope sits
0.77 % *below* Jupiter's measured band, so for a real giant the integrated value
over-estimates C/MR² mildly rather than under-estimating it.

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
  MgSiO₃ enstatite, H₂O ice VII and the deep-mantle MgSiO₃ BME4. §III.3 supplies both
  materials' ceilings, the pressures at which that paper hands over to Thomas–Fermi–Dirac
  (2.09 × 10⁴ GPa for iron, 1.35 × 10⁴ GPa for silicate), and Table 3's merged-EOS refit
  ρ = ρ₀ + cPⁿ, which the test uses as an independent check on the transcription.
- **Zeng, L., Sasselov, D. D. & Jacobsen, S. B. 2016**, ApJ 819, 127
  ([`2016ApJ...819..127Z`](https://ui.adsabs.harvard.edu/abs/2016ApJ...819..127Z), arXiv
  **[1512.08827](https://arxiv.org/abs/1512.08827)**). **Cached** in
  `docs/phase3/_papers/1512.08827.md`. The BM2 fits to PREM's outer core and lower mantle
  that carry the rocky part of this recipe, the 23.83 GPa mantle transition, the stated
  3.5 TPa ceiling of the lower-mantle fit and the argument that above ~1 TPa Mg/Si stops
  setting the density, and the semi-empirical M–R relation used as an independent validation
  curve.
- **Zeng, L. & Sasselov, D. 2013**, PASP 125, 227
  ([`2013PASP..125..227Z`](https://ui.adsabs.harvard.edu/abs/2013PASP..125..227Z), arXiv
  **[1301.0818](https://arxiv.org/abs/1301.0818)**). **Cached** in
  `docs/phase3/_papers/1301.0818.md`. The H₂O phase sequence along the melting curve and
  its transition pressures (Ih → III at 209.5 MPa, VI → VII at 2.216 GPa, VII → X at
  47 GPa), which is where this recipe's ice-phase gates come from.
- **French, M. & Redmer, R. 2015**, Phys. Rev. B 91, 014308
  ([`2015PhRvB..91a4308F`](https://ui.adsabs.harvard.edu/abs/2015PhRvB..91a4308F)). The DFT-MD
  potential for ices VII and X, reached through the `VII_X_French` representation in
  **SeaFreeze v1.1.0** (pinned in `engine/requirements.txt`; attribution from the package
  README, knot domain read out of the shipped spline). *No preprint*: verified by bibcode.
- **French, M. & Redmer, R. 2016**, Phys. Rev. E 93, 022140
  ([`2016PhRvE..93b2140F`](https://ui.adsabs.harvard.edu/abs/2016PhRvE..93b2140F)). The
  superionic potentials and their boundary against ices VII and X: named by the 1800 K
  refusal as what would open it, not transcribable from the abstract. *No preprint*.
- **Millot, M. et al. 2019**, Nature 569, 251
  ([`2019Natur.569..251M`](https://ui.adsabs.harvard.edu/abs/2019Natur.569..251M)).
  Superionic water above "100 gigapascals and ... 2,000 kelvin", which the ceiling is checked
  against. *No preprint*: verified by bibcode.
- **Millot, M. et al. 2018**, Nature Physics 14, 297
  ([`2018NatPh..14..297M`](https://ui.adsabs.harvard.edu/abs/2018NatPh..14..297M)). "Ice
  melts near 5,000 K at 190 GPa" — the one melting measurement above 52.4 GPa this recipe
  quotes, as a point the verdict measures a deep mantle against, not as a curve. *No preprint*:
  verified by bibcode; abstract only.
- **Reinhardt, A., Bethkenhagen, M., Coppari, F., Millot, M., Hamel, S. & Cheng, B. 2022**,
  Nat. Commun. 13, 4707
  ([`2022NatCo..13.4707R`](https://ui.adsabs.harvard.edu/abs/2022NatCo..13.4707R),
  [2203.12897](https://arxiv.org/abs/2203.12897)). The liquid–solid coexistence line
  (10–52.4 GPa) and the ice VII′–VII″ coexistence line (20–70 GPa) from thermodynamic
  integration with a machine-learned potential fitted to PBE DFT, and the finding that ices
  VII, VII′ and X are one thermodynamic phase while VII″ is first-order distinct. Baked from
  the paper's published data repository (`BingqingCheng/highP-ice`), never from the figure.
  *Open access*; the text is in the cache.
- **Queyroux, J.-A. et al. 2020**, Phys. Rev. Lett. 125, 195501
  ([`2020PhRvL.125s5501Q`](https://ui.adsabs.harvard.edu/abs/2020PhRvL.125s5501Q)). The
  measured triple point at 14.6 GPa · 850 K and the identification of the high-temperature
  bcc phase with superionic ice VII″ — the one experimental check on Reinhardt's lines this
  recipe can quote. *No preprint*: abstract only, verified by bibcode.
- **IAPWS R14-08(2011)**, *Revised Release on the Pressure along the Melting and
  Sublimation Curves of Ordinary Water Substance*
  ([iapws.org/relguide/MeltSub.html](http://www.iapws.org/relguide/MeltSub.html)). The
  melting-pressure equations for ices Ih, III, V, VI and VII with their reducing constants,
  validity ranges, uncertainties and the §7 verification values the test reproduces. *A
  standards release rather than an ADS record*, pinned by release number, the same route by
  which IAPWS-06 supplies ice Ih's equation of state below. The companion article
  ([Wagner, W., Riegert, T. & Pruß, A. 2011](https://ui.adsabs.harvard.edu/abs/2011JPCRD..40d3103W),
  [`2011JPCRD..40d3103W`](https://ui.adsabs.harvard.edu/abs/2011JPCRD..40d3103W)) derives the
  new ice Ih equation and reprints the ice III–VII ones unchanged.
- **Feistel, R. & Wagner, W. 2006**, J. Phys. Chem. Ref. Data 35, 1021
  ([`2006JPCRD..35.1021F`](https://ui.adsabs.harvard.edu/abs/2006JPCRD..35.1021F)).
  The IAPWS-06 Gibbs-potential equation of state for ice Ih. *No arXiv preprint*: verified
  by bibcode, and the two constants used here (ρ and κ_T at the normal pressure melting
  point) were read from Table 6 of the IAPWS release document
  [R10-06(2009)](http://www.iapws.org/relguide/Ice-2009.pdf), which is the authoritative
  publication of the same equation. Marked as a **non-ADS-fulltext exception**: the release
  document was read directly, not summarised.
- **Bollengier, O., Brown, J. M. & Shaw, G. H. 2019**, J. Chem. Phys. 151, 054501
  ([`2019JChPh.151e4501B`](https://ui.adsabs.harvard.edu/abs/2019JChPh.151e4501B), DOI
  [10.1063/1.5097179](https://doi.org/10.1063/1.5097179)). Sound speeds in liquid water to
  700 MPa down to the freezing point and the Gibbs-energy equation of state to 2300 MPa over
  240–500 K, distributed as SeaFreeze's `water1`; baked into `water_table.py` for the ocean.
  The shelf above it, **Brown, J. M. 2018**, Fluid Phase Equilibria 463, 18
  ([`2018FlPEq.463...18B`](https://ui.adsabs.harvard.edu/abs/2018FlPEq.463...18B)), `water2`
  to 100 GPa, is named in the refusal and not baked. *No arXiv preprints.*
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
- **Chabrier, G., Mazevet, S. & Soubiran, F. 2019**, ApJ 872, 51
  ([`2019ApJ...872...51C`](https://ui.adsabs.harvard.edu/abs/2019ApJ...872...51C), arXiv
  **[1902.01852](https://arxiv.org/abs/1902.01852)**). **Cached** in
  `docs/phase3/_papers/1902.01852.md`. The hydrogen-helium equation of state this recipe's
  envelope reads, taken as the distributed tables rather than transcribed: the archive at
  `perso.ens-lyon.fr/gilles.chabrier/DirEOS` carries the Y = 0.275 mixture on a
  (log T, log P) grid with log ρ and ∇_ad, and its README attributes them to this paper.
  The same paper supplies the mixing rule used for a metal-loaded envelope — "the
  additivity of the extensive variables (volume, energy, entropy, …) at constant intensive
  variables (P,T)" — from which the heat-capacity-weighted ∇_ad follows.
- **Umemoto, K., Wentzcovitch, R. M., Wu, S., Ji, M., Wang, C.-Z. & Ho, K.-M. 2017**,
  E&PSL 478, 40
  ([`2017E&PSL.478...40U`](https://ui.adsabs.harvard.edu/abs/2017E%26PSL.478...40U), arXiv
  **[1708.04767](https://arxiv.org/abs/1708.04767)**). **Cached** in
  `docs/phase3/_papers/1708.04767.md`. The first-principles dissociation sequence of MgSiO₃
  post-perovskite (0.75, 1.31 and 3.10 TPa), and the conclusion that the break-up into
  MgO + SiO₂ is "the last solid-solid transition identified so far", which is why one phase
  covers 3.5 to 13.5 TPa rather than several.
- **Noack, L. & Lasbleis, M. 2020**, A&A 638, A129
  ([`2020A&A...638A.129N`](https://ui.adsabs.harvard.edu/abs/2020A%26A...638A.129N),
  doi [10.1051/0004-6361/202037723](https://doi.org/10.1051/0004-6361/202037723)).
  *Parameterisations of interior properties of rocky planets. An investigation of planets with
  Earth-like compositions but variable iron content.* **Cached** as
  `docs/phase3/_papers/2020A&A...638A.129N.pdf` (open access; fetched by the owner). The
  second anchor for the adiabat: eq. (22) with its supports (5), (9), (13)–(15), (18), (19),
  valid 0.8–2 M⊕; all constants read from the PDF. Eqs. (20)–(21) are initial temperatures and
  are deliberately not used. Verified by bibcode and title.
- **Unterborn, C. T., Dismukes, E. E. & Panero, W. R. 2019**, JGR Planets 124, 1704
  ([`2019JGRE..124.1704U`](https://ui.adsabs.harvard.edu/abs/2019JGRE..124.1704U), arXiv
  **[1905.06530](https://arxiv.org/abs/1905.06530)**). **Cached** in
  `docs/phase3/_papers/1905.06530.md`. The adiabatic boundary condition `T(R) = T_Pot` and
  the statement that a conductive lid sits between it and the surface; the Earth-like 1600 K
  potential temperature this recipe references rock and metal to; eq. 7 and eq. 8, the
  published CMB-temperature fits the adiabat is checked against (valid 0.75 to 1.5 R⊕),
  including the 2500 to 2800 K Earth value they quote from **Lay, Hernlund & Buffett 2008**
  ([`2008NatGe...1...25L`](https://ui.adsabs.harvard.edu/abs/2008NatGe...1...25L)); and the
  caveat that tidal heating and mantle boundary layers make real profiles super-adiabatic.
- **Anderson, O. L. & Goto, T. 1989**, PEPI 55, 241
  ([`1989PEPI...55..241A`](https://ui.adsabs.harvard.edu/abs/1989PEPI...55..241A)); with
  **Anderson & Masuda 1994** and **Isaak & Anderson 2003**. The thermal-pressure
  approximation `P_th = αK_T·ΔT` and its basis, that αK_T is nearly volume-independent above
  the Debye temperature, plus the silicate and metal coefficients (0.00692 GPa/K, and
  0.00121 GPa/K with a 7.8 × 10⁻⁷ GPa/K² electron term). *No arXiv preprints.* All three are
  used **through Seager+ 2007 §IV.2.2**, the cached full text that quotes the coefficients,
  the Debye temperatures bounding them and the resulting density changes — named here so a
  later audit knows the route.
- **Salpeter, E. E. & Zapolsky, H. S. 1967**, Phys. Rev. 158, 876
  ([`1967PhRv..158..876S`](https://ui.adsabs.harvard.edu/abs/1967PhRv..158..876S)). The
  Thomas–Fermi–Dirac equation of state with a correlation-energy correction. *No arXiv
  preprint; pinned by bibcode.* **Not implemented here**: it is what both source papers switch
  to at the pressures this recipe stops at, and what every ceiling's refusal names.
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
- **Neumann, W. & Kruse, A. 2019**, ApJ 882, 47
  ([`2019ApJ...882...47N`](https://ui.adsabs.harvard.edu/abs/2019ApJ...882...47N),
  doi [10.3847/1538-4357/ab2fcf](https://doi.org/10.3847/1538-4357/ab2fcf)). *Differentiation
  of Enceladus and Retention of a Porous Core.* **Cached** as
  `docs/phase3/_papers/2019ApJ...882...47N.html` (open access, fetched through the ADS gateway
  2026-08-30) with a text extraction beside it. The branch for porosity on a heated body: tidal
  heating, differentiation and melting, core compaction by creep (§2.5) with the creep
  coefficients of three rheologies in Table 3; a porous core layer of 4–70 km for olivine, none
  for antigorite. Reached and specified, not wired (C9). Verified by bibcode and title.
- **Mei, S. & Kohlstedt, D. L. 2000**, JGR 105, 21457 and 21471
  ([`2000JGR...10521457M`](https://ui.adsabs.harvard.edu/abs/2000JGR...10521457M),
  [`2000JGR...10521471M`](https://ui.adsabs.harvard.edu/abs/2000JGR...10521471M)). The
  olivine diffusion- and dislocation-creep laws Neumann & Kruse compact with. Cited for the
  branch's specification only; not transcribed. Verified by bibcode and title.
- **Amiguet, E. et al. 2012**, EPSL 345, 142
  ([`2012E&PSL.345..142A`](https://ui.adsabs.harvard.edu/abs/2012E%26PSL.345..142A)). *Creep
  of phyllosilicates at the onset of plate tectonics* — the antigorite creep law (Peierls
  stress, grain-size independent). Same standing. Verified by bibcode and title.
- **Hilairet, N., Daniel, I. & Reynard, B. 2006**, GRL 33, L02302
  ([`2006GeoRL..33.2302H`](https://ui.adsabs.harvard.edu/abs/2006GeoRL..33.2302H),
  doi [10.1029/2005GL024728](https://doi.org/10.1029/2005GL024728)). *Equation of state of
  antigorite, stability field of serpentines, and seismicity in subduction zones.* **Cached** as
  `docs/phase3/_papers/2006GeoRL..33.2302H.pdf` (open access; fetched by the owner). The BM2 the
  paper adopts (V₀ 2926.23(50) Å³, K₀ 67.27(123) GPa, K₀′ = 4, reversible to 10 GPa), the
  structural formula and the m = 1 volume from which ρ₀ is derived here, and the one printed
  density (2765 kg/m³ at 5.7 GPa and 470 °C) it is checked against. Room temperature only.
  Verified by bibcode and title.
- **Capitani, G. & Mellini, M. 2004**, Am. Mineral. 89, 147
  ([`2004AmMin..89..147C`](https://ui.adsabs.harvard.edu/abs/2004AmMin..89..147C)). *The
  modulated crystal structure of antigorite: The m = 17 polysome* — the structure Hilairet+ index
  with, which is why 2926.23 / 172 = 17.01. Cited for that check only. Verified by title.
- **Vance, S. D. et al. 2018**, JGR Planets 123, 180
  ([`2018JGRE..123..180V`](https://ui.adsabs.harvard.edu/abs/2018JGRE..123..180V),
  [1705.03999](https://arxiv.org/abs/1705.03999)). *Geophysical Investigations of Habitability
  in Ice-Covered Ocean Worlds* — the published rock-density targets the icy moons are read
  against, and the two routes to Enceladus's ~2700 kg/m³ (hydrous rock, or anhydrous rock plus
  pores) that C9's rheology discriminator tells apart. *Open access*; not yet in the cache, cited
  from ADS for the targets only. Verified by bibcode and title.
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
- **Malamud, U. & Prialnik, D. 2015**, Icarus 246, 21
  ([`2015Icar..246...21M`](https://ui.adsabs.harvard.edu/abs/2015Icar..246...21M),
  doi [10.1016/j.icarus.2014.02.027](https://doi.org/10.1016/j.icarus.2014.02.027)). *Modeling
  Kuiper belt objects Charon, Orcus and Salacia by means of a new equation of state for porous
  icy bodies*: an initially homogeneous ice–rock body, multiphase flow of water through porous
  rock, the differentiation that results, aqueous alteration, with serpentinisation and
  compaction's gravitational energy as heat sources — the treatment partial differentiation
  actually gets (C7), and two of C9's exclusions. *Paywalled, abstract only*; on the owner's
  request list, serving C7 and C9 at once. Verified by bibcode and title.
- **Malamud, U. & Prialnik, D. 2013**, Icarus 225, 763
  ([`2013Icar..225..763M`](https://ui.adsabs.harvard.edu/abs/2013Icar..225..763M),
  doi [10.1016/j.icarus.2013.04.024](https://doi.org/10.1016/j.icarus.2013.04.024)).
  Serpentinisation as an exothermic reaction in the evolution of Enceladus and Mimas — why
  water in rock is a reaction, not a mixture. *Paywalled, abstract only*.
- **Prialnik, D. & Merk, R. 2008**, Icarus 197, 211
  ([`2008Icar..197..211P`](https://ui.adsabs.harvard.edu/abs/2008Icar..197..211P),
  doi [10.1016/j.icarus.2008.03.024](https://doi.org/10.1016/j.icarus.2008.03.024)). The
  porous icy-body thermal-evolution code the two above stand on. *Paywalled, abstract only*.
- **Bethkenhagen, M., French, M. & Redmer, R. 2013**, J. Chem. Phys. 138, 234504
  ([`2013JChPh.138w4504B`](https://ui.adsabs.harvard.edu/abs/2013JChPh.138w4504B),
  doi [10.1063/1.4810883](https://doi.org/10.1063/1.4810883)). The ammonia equation of state
  Bethkenhagen+ 2017 extend — 330 GPa, 500–10 000 K. *Paywalled*, the route back to C4's tables;
  on the owner's paper-request list. Verified by bibcode and title.
- **Militzer, B., González-Cataldo, F., Zhang, S., Driver, K. P. & Soubiran, F. 2021**,
  Phys. Rev. E 103, 013203
  ([`2021PhRvE.103a3203M`](https://ui.adsabs.harvard.edu/abs/2021PhRvE.103a3203M),
  [2012.07093](https://arxiv.org/abs/2012.07093)). The FPEOS database: CH₄ but no NH₃, and
  10⁴–10⁹ K, above the ice-giant adiabat — checked as a route to C4 and declined for those two
  reasons. *Open access*.
- **Nettelmann, N., Wang, K., Fortney, J. J., Hamel, S., Yellamilli, S., Bethkenhagen, M. &
  Redmer, R. 2016**, Icarus 275, 107
  ([`2016Icar..275..107N`](https://ui.adsabs.harvard.edu/abs/2016Icar..275..107N),
  [1605.00171](https://arxiv.org/abs/1605.00171)). Uranus models with a thermal boundary at the
  ice/rock–H/He transition and an ice:rock ratio, which is where the ice giants' residual is
  attributed (C5). *Open access*; cited here only for that attribution.
- **Helled, R., Nettelmann, N. & Guillot, T. 2020**, Space Sci. Rev. 216, 38
  ([`2020SSRv..216...38H`](https://ui.adsabs.harvard.edu/abs/2020SSRv..216...38H),
  [1909.04891](https://arxiv.org/abs/1909.04891)). The Uranus/Neptune review: "even a very
  small (in mass) H-He atmosphere can imply high interior temperatures, if an adiabatic
  temperature profile is assumed" — the central-temperature excess named as the adiabatic
  envelope's signature — and whether layer transitions are sharp or gradual left open
  (their Fig. 4). *Open access*; text in the cache (the sentence sits in the HTML, which the
  markdown extraction dropped).
- **Helled, R. & Stevenson, D. 2017**, ApJ 840, L4
  ([`2017ApJ...840L...4H`](https://ui.adsabs.harvard.edu/abs/2017ApJ...840L...4H),
  [1704.01299](https://arxiv.org/abs/1704.01299)). A closed form for a diluted core,
  Z(m) = (2a/√π)(1 − Z_e) exp(−a²m²/m_c²) + Z_e — the transcribable shape for Jupiter's
  heavy-element distribution, reached and not implemented (no consumer). *Open access*.
- **Howard, S., Guillot, T. & Bazot, M. 2023**, A&A 672, A33
  ([`2023A&A...672A..33H`](https://ui.adsabs.harvard.edu/abs/2023A%26A...672A..33H),
  [2302.09082](https://arxiv.org/abs/2302.09082)). Juno-constrained Jupiter models with a
  dilute core, the second transcribable route; reached, not implemented. *Open access*.
- **Debras, F. & Chabrier, G. 2019**, ApJ 872, 100
  ([`2019ApJ...872..100D`](https://ui.adsabs.harvard.edu/abs/2019ApJ...872..100D),
  [1901.05697](https://arxiv.org/abs/1901.05697)). §4.1 "Inward decreasing abundance of heavy
  elements in some part of the outer envelope": the heavy-element profile is not monotonic, and
  the structure needs four regions. *Open access*; text in the cache.
- **Kimura, T. 2023**, J. Chem. Phys. 158, 134504
  ([`2023JChPh.158m4504K`](https://ui.adsabs.harvard.edu/abs/2023JChPh.158m4504K),
  doi [10.1063/5.0137943](https://doi.org/10.1063/5.0137943)). *Revisiting the melting curve of
  H₂O by Brillouin spectroscopy to 54 GPa*. **Cached** as
  `docs/phase3/_papers/2023JChPh.158m4504K.pdf` (fetched by the owner, 2026-08-30). Table I
  (melting points 25.9–53.6 GPa, ±130–150 K; the rows below 26 GPa are liquid runs at a
  temperature estimated from Queyroux's curve) and eq. (2), the Simon–Glatzel fit anchored on
  Queyroux+ 2020's triple point. The arbiter of the 20.6 GPa seam: it sits with Reinhardt (F1).
  Bibcode verified by title.
- **Bethkenhagen, M. et al. 2017**, ApJ 848, 67
  ([`2017ApJ...848...67B`](https://ui.adsabs.harvard.edu/abs/2017ApJ...848...67B), arXiv
  **[1709.04133](https://arxiv.org/abs/1709.04133)**). **Cached** in
  `docs/phase3/_papers/1709.04133.md`. The additive volume law's quantified bound for
  planetary ices, and the solar-abundance ice ratio Z(CH₄):Z(NH₃):Z(H₂O) = 0.31:0.08:0.61
  that an ice-giant envelope would be declared with.
- **Scheibe, L., Nettelmann, N. & Redmer, R. 2019**, A&A 632, A70
  ([`2019A&A...632A..70S`](https://ui.adsabs.harvard.edu/abs/2019A%26A...632A..70S), arXiv
  **[1911.00447](https://arxiv.org/abs/1911.00447)**). **Cached** in
  `docs/phase3/_papers/1911.00447.md`. The interior temperatures the ice-giant refusal
  quotes, and the finding that adiabatic models cannot reproduce both planets.
- **Mazevet, S., Licari, A., Chabrier, G. & Potekhin, A. Y. 2019**, A&A 621, A128
  ([`2019A&A...621A.128M`](https://ui.adsabs.harvard.edu/abs/2019A%26A...621A.128M), arXiv
  **[1810.05658](https://arxiv.org/abs/1810.05658)**). **Cached** in
  `docs/phase3/_papers/1810.05658.md`. The hot-water equation of state, taken from the
  authors' reference implementation `eoswater21.f`; the critical point their fit produces
  (683 K, 0.331 g/cc) is what the transcription is checked against.
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
- [Core state](core-state-methodology.md) — takes the core pressures and the geotherm bound
  from here and decides whether the metal is liquid
- [Rocky-planet dynamo](rocky-planet-dynamo-methodology.md) — consumes the core radius
- [Derivation discipline](derivation-discipline.md) — why the contract block is checked
  against the code, and why tables are generated rather than typed

<!-- Validation and roster tables regenerated by `python3 engine/test_interior.py --table`
     and `--roster`. -->
