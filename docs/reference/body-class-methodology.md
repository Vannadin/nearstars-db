<!-- 천체가 무엇인가 — 질량과 반지름을 발표된 경계에 대서 클래스를 좁히는 방법(논문 근거) -->
# Body class grounding: narrowing a body to the physics that applies to it

Eight `selects` edges leave `body_class`, and every one of them picks which model runs:
the interior integration, the three class tables, the figure, the spin axis, the two
dynamos and the core state. The key those edges read is not a preference. Calling Neptune a
gas giant runs an H/He polytrope on an ice mantle and returns a confident number that is
wrong.

This recipe derives that key from mass and radius against published boundaries. It
**narrows** rather than picks: every boundary is a band, and a body inside one comes back
with both neighbours alive.

## Contract — `body_class`

**Returns** — `class` [—] · `classes` [—] · `decided_by` [—] · `agrees_with_declared` [—]
**Needs** — `mass_earth` [M_earth] · `radius_earth` [R_earth] · `declared_class` [—] ·
`composition_intent` [—] · `gas_mass_fraction` [—] · `semi_major_axis_au` [au]
**Discriminating keys** — whether a radius is available, which decides if the lower half of
the ladder can be read at all; and whether an envelope composition is declared, which is the
only thing that separates a gas giant from an ice giant on evidence rather than convention.
**Grade** — as weak as the weakest boundary that did the narrowing, and never better than
**judgment** when more than one class survives. `calibrated` where a measured population
feature draws the line, `analog` where a formation model does, `judgment` where the line is
convention.

`class` is one of the six names below, or empty when more than one survives; `classes`
always lists every survivor. `declared_class` is **read but never used to compute**: it is
the contrast, not an input.

## The vocabulary

Six names, in ascending mass: `rocky`, `sub_neptune`, `ice_giant`, `gas_giant`,
`brown_dwarf`, `star`. A name earns a place only if a consumer branches on it, and all six
are named in `interior.py` (`FLUID_CLASSES` declines the upper four, each for a different
reason; `GAS_GIANT_CLASSES` accepts the giants; the rest is the rocky path).

`giant` is a second spelling of `gas_giant` and nothing in this repository distinguishes
them. It is normalised on read and never emitted, which is the rule
[derivation discipline](derivation-discipline.md) §7 states: one list, and a spelling
variant is not admitted to it.

Class is **what a body is made of**. What it orbits is `BodyState.kind`, a separate declared
field; this recipe never reads it, because every one of the eight consumers branches on
material physics and none on orbital role.

## The ladder

Five boundaries, one quantity and one band each. The band's edges are published numbers;
below the band the lower class holds, above it the upper one, inside it both survive.

    rocky ─── sub_neptune ─── ice_giant ─── gas_giant ─── brown_dwarf ─── star
          R                R              M             M               M

The two halves read different quantities, and that is not a convenience. Below the giants
the discriminant is **radius**: the valley is a radius feature, and Rogers 2015's argument is
that at a given radius you can tell whether there is an envelope. Above the giants it is
**mass**: fusion thresholds are mass thresholds, and radius is nearly degenerate there
(Chen & Kipping's Jovian power index is −0.04 ± 0.02).

The deuterium limit is the one boundary with no signature in either quantity: Chen &
Kipping find brown dwarfs "merely high-mass members of a continuum of Jovians". It is a
boundary anyway, because the consumers that branch on it branch on **thermal history**:
`interior.py` and `dynamo.py` both decline brown dwarfs for a luminosity history that
deuterium burning gives them and neither recipe carries.

Surviving classes are the contiguous run the boundaries leave. If they contradict each other
the run is inverted rather than empty, and the recipe returns the whole overlap: the ladder
is monotone in mass, so a contradiction means the mass and radius handed to it are not
compatible, which is `mass_radius.density_gate`'s question.

## Constants

| boundary | quantity | band | validity | source |
|---|---|---|---|---|
| rocky / sub-Neptune | radius | 1.5 – 1.8 R⊕ | close-in planets, P < 100 d; imported from `mass_radius.py`, not re-typed | Fulton+ 2017 (measured deficit 1.5–2.0 R⊕); Rogers 2015 (R_thresh 1.48 +0.07/−0.56); Van Eylen+ 2018 |
| ” (no radius) | mass | 1.45 – 2.70 M⊕ | 316 objects, dwarf planets to late-type stars | Chen & Kipping 2017, T(1) = 2.04 (+0.66/−0.59) M⊕ |
| sub-Neptune / ice giant | radius | 3.5 R⊕, no band | **convention**: a binning line, not a measured feature | Kopparapu+ 2018 §2.1, read from Fulton+ 2017's distribution |
| ice giant / gas giant | envelope | gas mass fraction ≥ 0.5 | only when composition is declared | Lambrechts & Johansen 2014, Fig. 4 |
| ” (no composition) | mass | M_iso – 50 M⊕ | M_iso = 20 M⊕ (a/5 au)^(8/7); 50 M⊕ = 2 × the maximum observed core mass | Lambrechts & Johansen 2014 §4.1; Otegi+ 2020 (~25 M⊕) |
| gas giant / brown dwarf | mass | 11.0 – 16.3 M_J | full model range over metallicity, helium, and burnt fraction; 13.0 ± 0.8 M_J for the common case | Spiegel+ 2011, abstract |
| brown dwarf / star | mass | 0.070 – 0.083 M_sun | solar to [M/H] = −2, and dusty to grainless atmospheres | Chabrier & Baraffe 2000, Fig. 3 and §4.5.2 |
| below the ladder | radius | 200 – 300 km | icy moons and rocky asteroids; a strength problem, not a composition one | Lineweaver & Norman 2010, abstract |

Unit ratios are the IAU 2015 nominal ones (317.8 M⊕/M_J, 332946 M⊕/M_sun, 11.209 R⊕/R_J);
the M_J value is `dynamo.py`'s, so one quantity keeps one constant.

## What the envelope boundary needs, and why the others do not

Gas giants and ice giants are not separated by size. They are separated by **whether most of
the mass is H/He or heavy elements**, which is what Lambrechts & Johansen 2014 make the
definition: a core that reaches the pebble isolation mass has its solid accretion cut off,
its envelope collapses, and it becomes a gas giant; one that does not stays core-dominated.
Their Fig. 4 caption puts it in a line.

So this is the one boundary `composition_intent` carries, and its two mass edges are one-
sided readings of the same statement. A total mass below the isolation mass means the core
can never have reached it. A total mass above twice the largest core anyone has measured
(Otegi+ 2020's ~25 M⊕) means more than half the mass cannot be core; the factor of two is
not a fitted coefficient but what "dominant" means. Between the two the recipe says so and
names the declaration that would settle it.

Kopparapu+ 2018's 6.0 R⊕ line is **not** used here, because that paper calls it "the
*assumed* upper limit on Neptune-size planets". A number adopted from a source that marks it
as an assumption is not grounding.

## Validation

The eight solar-system planets are the decision line: their masses and radii are measured and
their classes are not in dispute. No boundary was fitted to them. Radii are Archinal+ 2011
Table 4 mean radii over 6371.00 km, masses are the IAU 2009 GM ratios. Regenerated by
`python3 engine/test_body_class.py --table`.

| body | M (M⊕) | R (R⊕) | derived | published | grade | decided by |
|---|---|---|---|---|---|---|
| Mercury | 0.05527 | 0.383 | rocky | rocky | calibrated | radius valley |
| Venus | 0.815 | 0.950 | rocky | rocky | calibrated | radius valley |
| Earth | 1 | 1.000 | rocky | rocky | calibrated | radius valley |
| Mars | 0.1074 | 0.532 | rocky | rocky | calibrated | radius valley |
| Jupiter | 317.8 | 10.973 | gas_giant | gas_giant | analog | envelope dominance + deuterium burning |
| Saturn | 95.16 | 9.140 | gas_giant | gas_giant | analog | envelope dominance + deuterium burning |
| Uranus | 14.54 | 3.981 | ice_giant | ice_giant | judgment | sub-Neptune ceiling + envelope dominance |
| Neptune | 17.15 | 3.865 | ice_giant | ice_giant | judgment | sub-Neptune ceiling + envelope dominance |

Saturn is the discriminating row. It is the only anchor a plausible alternative boundary
(Chen & Kipping's T(2)) gets wrong, and the grade column shows where the evidence is strong
and where it is convention: the rocky calls rest on a measured population feature, the giant
calls on a formation model, and the ice-giant calls on a binning line.

## Domain of validity

| regime | condition | what this recipe does | grade |
|---|---|---|---|
| radius available | any body above the potato radius | reads the whole ladder; the lower half in radius, the upper half in mass | boundary-dependent |
| **no radius** | mass only, as for a non-transiting RV planet | falls to Chen & Kipping's mass break for the rocky boundary and cannot draw the sub-Neptune ceiling at all, so the lower three classes stay open | judgment |
| **envelope declared** | `gas_mass_fraction` or a `composition_intent` that implies one | separates gas giant from ice giant on the criterion that defines them | analog |
| no envelope declared | mass between the isolation mass and 50 M⊕ | returns both giants and names the declaration that would settle it | judgment |
| **inside any band** | boundary-adjacent in the deciding quantity | returns both neighbours. The bands are as wide as the published readings disagree, which is the honest width | judgment |
| potato-to-sphere transition | mean radius 200 – 300 km | classifies, with a note: hydrostatic equilibrium is not assured, and `body_figure`'s J₂ comes from Radau–Darwin, which assumes it | judgment |
| **below the transition** | mean radius under 200 km | **declines**: at this size strength sets the shape, not composition, and every class in this vocabulary presumes a self-gravitating figure | – |
| mass not positive | – | **declines** | – |
| **boundaries contradict** | radius-side and mass-side verdicts point opposite ways | **does not narrow**: the ladder is monotone in mass, so this means mass and radius are incompatible | judgment |

The valley moves. Ho & Van Eylen 2023 measure its location against orbital period
(∂log R/∂log P = −0.096 +0.023/−0.027) and host mass (+0.231 +0.053/−0.064). The band here is
fixed, which is a further reason it returns "both" inside it rather than a line.

## Sources

- **Chen, J. & Kipping, D. 2017**, ApJ 834, 17
  ([`2017ApJ...834...17C`](https://ui.adsabs.harvard.edu/abs/2017ApJ...834...17C), arXiv
  **[1603.08614](https://arxiv.org/abs/1603.08614)**). **Cached** in
  `docs/phase3/_papers/1603.08614.md`. The three data-driven transition masses, inferred with
  the break points left free. Two of the three are boundaries here: T(1) = 2.04 M⊕ is the
  mass-side rocky reading, and T(3) = 0.0800 ± 0.0081 M_sun lands inside the hydrogen-burning
  band from an independent method. T(2) = 0.414 M_J is **not** the gas / ice giant line, on
  the paper's own evidence: "Saturn is close to being the largest occurring Neptunian world",
  so their Neptunian class runs from Uranus to Saturn.
- **Fulton, B. J. et al. 2017**, AJ 154, 109
  ([`2017AJ....154..109F`](https://ui.adsabs.harvard.edu/abs/2017AJ....154..109F), arXiv
  **[1703.10375](https://arxiv.org/abs/1703.10375)**). **Cached**. The measured factor-≥2
  deficit at 1.5–2.0 R⊕ that the valley band is drawn from, and the radius distribution
  Kopparapu+ 2018 read their binning lines out of.
- **Rogers, L. A. 2015**, ApJ 801, 41
  ([`2015ApJ...801...41R`](https://ui.adsabs.harvard.edu/abs/2015ApJ...801...41R), arXiv
  **[1407.4457](https://arxiv.org/abs/1407.4457)**). **Cached**. The threshold radius above
  which most planets are not rocky, 1.48 (+0.07/−0.56) R⊕ under an Earth-like limiting
  composition, and the argument that radius is what discriminates.
- **Van Eylen, V. et al. 2018**, MNRAS 479, 4786
  ([`2018MNRAS.479.4786V`](https://ui.adsabs.harvard.edu/abs/2018MNRAS.479.4786V), arXiv
  **[1710.05398](https://arxiv.org/abs/1710.05398)**). **Cached**. The valley seen with
  asteroseismic stellar radii, and its negative period slope: the sub-Neptunes are stripped
  cores, which is why the boundary is compositional and not primordial.
- **Ho, C. S. K. & Van Eylen, V. 2023**, MNRAS 519, 4056
  ([`2023MNRAS.519.4056H`](https://ui.adsabs.harvard.edu/abs/2023MNRAS.519.4056H), arXiv
  **[2301.04062](https://arxiv.org/abs/2301.04062)**). **Cached**. The valley's dependence on
  orbital period, stellar mass and age, which bounds how far a fixed band can be trusted.
- **Kopparapu, R. K. et al. 2018**, ApJ 856, 122
  ([`2018ApJ...856..122K`](https://ui.adsabs.harvard.edu/abs/2018ApJ...856..122K), arXiv
  **[1802.09602](https://arxiv.org/abs/1802.09602)**). **Cached**. The size bins used for
  direct-imaging yield estimates. The 3.5 R⊕ ceiling is taken from here as convention; their
  6.0 R⊕ line is not, because they mark it as assumed.
- **Lambrechts, M. & Johansen, A. 2014**, A&A 572, A35
  ([`2014A&A...572A..35L`](https://ui.adsabs.harvard.edu/abs/2014A%26A...572A..35L), arXiv
  **[1408.6087](https://arxiv.org/abs/1408.6087)**). **Cached**. The pebble isolation mass,
  M_iso = 20 M⊕ (a/5 au)^(8/7), and the statement that it is what divides the two giant
  classes: below it a core stays core-dominated, above it the envelope runs away.
- **Otegi, J. F., Bouchy, F. & Helled, R. 2020**, A&A 634, A43
  ([`2020A&A...634A..43O`](https://ui.adsabs.harvard.edu/abs/2020A%26A...634A..43O), arXiv
  **[1911.04745](https://arxiv.org/abs/1911.04745)**). **Cached**. The rocky population
  ending near 25 M⊕, read by its authors as the maximum core mass that can form; the upper
  edge of the envelope band is twice it.
- **Spiegel, D. S., Burrows, A. & Milsom, J. A. 2011**, ApJ 727, 57
  ([`2011ApJ...727...57S`](https://ui.adsabs.harvard.edu/abs/2011ApJ...727...57S), arXiv
  **[1008.5150](https://arxiv.org/abs/1008.5150)**). **Cached**. The deuterium-burning mass
  and its real spread: 13.0 ± 0.8 M_J for common proto-brown-dwarf conditions, 11.0 to
  16.3 M_J once metallicity, helium and the burnt-fraction definition are all varied.
- **Chabrier, G. & Baraffe, I. 2000**, ARA&A 38, 337
  ([`2000ARA&A..38..337C`](https://ui.adsabs.harvard.edu/abs/2000ARA%26A..38..337C), arXiv
  **[astro-ph/0006383](https://arxiv.org/abs/astro-ph/0006383)**). **Cached**. The
  hydrogen-burning minimum mass, 0.075 M_sun at solar composition and 0.083 M_sun at
  [M/H] = −2, dropping to 0.070–0.072 M_sun depending on how dust is treated in the
  atmosphere.
- **Lineweaver, C. H. & Norman, M. 2010**, preprint
  ([`2010arXiv1004.1091L`](https://ui.adsabs.harvard.edu/abs/2010arXiv1004.1091L), arXiv
  **[1004.1091](https://arxiv.org/abs/1004.1091)**). The potato-to-sphere transition at a
  mean radius of ~200–300 km for icy moons and rocky asteroids, read from the abstract.
  *Preprint only, not refereed, and ar5iv serves no full text*: it is used for a decline
  threshold and nothing downstream of it. Tancredi & Favre 2008
  ([`2008Icar..195..851T`](https://ui.adsabs.harvard.edu/abs/2008Icar..195..851T)) treat the
  same question observationally.
- **Archinal, B. A. et al. 2011**, Celest. Mech. Dyn. Astron. 109, 101
  ([`2011CeMDA.109..101A`](https://ui.adsabs.harvard.edu/abs/2011CeMDA.109..101A)) and
  **Luzum, B. et al. 2011**, ibid. 110, 293
  ([`2011CeMDA.110..293L`](https://ui.adsabs.harvard.edu/abs/2011CeMDA.110..293L)). The mean
  radii and the GM ratios the eight anchors are stated in. *No arXiv preprint*: verified by
  bibcode.

## Related

- [Mass–radius relation](mass-radius-relation-methodology.md) — owns the radius-valley
  constants this recipe imports, and gates its own domain with them for a different question
- [Interior structure](interior-structure-methodology.md) — the largest consumer: which
  equation of state applies, and which classes it declines by name
- [Core state](core-state-methodology.md) — declines the six coreless classes on this key
- [Planetary dynamo scaling](planetary-dynamo-scaling.md) — the giant branch, and its own
  mass-based refusal of brown dwarfs
- [Derivation discipline](derivation-discipline.md) — why one vocabulary, and why declining
  is a return value
