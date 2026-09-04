<!-- 궤도·내부물성에서 조석가열 출력(Ė)을 도출하고 화산·지하해·플룸 가능성을 판정하는 방법론 레퍼런스 -->
# Tidal-Heating Methodology: Internal Power, Volcanism & Subsurface Oceans

Method reference for deriving the **internal tidal-heating power** `Ė` of a
synchronously rotating body (a moon around a planet, or a planet around its star)
from its orbit and interior, and for deciding whether that heat can sustain
volcanism, a subsurface ocean, or plumes. Same spirit as the
[dynamo-scaling doc](planetary-dynamo-scaling.md): cite the relation + a calibration
that reproduces known bodies, not a fabricated measurement.

This is the **single most repeated derived value in NearStars Phase 4** (it was
recomputed four separate times in one α Cen session, for the moons
Alpha Centauri A b I–III and A b V (Dante, Hades, Pandora, Chaos)), so it gets a canonical grounded recipe here.

> Citations resolved against NASA ADS (the registered `ADS_API_TOKEN`), not ad-hoc
> web search; arXiv id where one exists, otherwise the authoritative ADS bibcode
> (flagged "no arXiv"). See §9 for the verified list.
> This is a working reference, not a textbook.

**Scope note:** this doc is about tidal *heating* (the dissipated power). The related
question of tidal *locking*, the despin timescale that decides whether a body is
synchronous in the first place, is a **planned separate sibling doc**; do not
conflate the two. The recipe below *assumes* synchronous rotation (the usual state
for the close-in bodies where heating matters); a non-synchronous body needs the
locking treatment first.

## Table of Contents

1. [The law: the fixed-Q tidal-heating formula](#1-the-law-the-fixed-q-tidal-heating-formula)
2. [Calibration: the formula reproduces Io and Enceladus](#2-calibration-the-formula-reproduces-io-and-enceladus)
3. [The a⁻⁷·⁵ distance gate (the hard lesson)](#3-the-a⁷·⁵-distance-gate-the-hard-lesson)
4. [The eccentricity-maintenance requirement](#4-the-eccentricity-maintenance-requirement)
5. [Domain of validity: k₂/Q by body class, and the rheology problem](#5-domain-of-validity-kq-by-body-class-and-the-rheology-problem)
6. [Deciding the outcome: volcanism / ocean / plumes](#6-deciding-the-outcome-volcanism-ocean-plumes)
   - [6.1 The flux → regime table](#61-the-flux--regime-table)
   - [6.2 How the heat actually leaves: the three-mode ladder](#62-how-the-heat-actually-leaves-the-three-mode-ladder)
   - [6.3 The plains are not an exit](#63-the-plains-are-not-an-exit)
   - [6.4 The lava-lake capacity test (and the two-denominator trap)](#64-the-lava-lake-capacity-test-and-the-two-denominator-trap)
   - [6.5 The super-Io ceiling: what size a lava moon can be](#65-the-super-io-ceiling-what-size-a-lava-moon-can-be)
7. [Worked examples](#7-worked-examples)
8. [Honesty & uncertainty](#8-honesty--uncertainty)
9. [Annotated Bibliography](#9-annotated-bibliography)
10. [Related](#related)

---

## 1. The law: the fixed-Q tidal-heating formula

Peale, Cassen & Reynolds 1979 (*Science* 203, 892, [`1979Sci...203..892P`](https://ui.adsabs.harvard.edu/abs/1979Sci...203..892P)) predicted,
famously days before Voyager imaged the eruptions, that Io would be melted by
tidal dissipation. Their constant-phase-lag ("fixed-Q") result is still the
first-order tool. For a synchronously rotating body of radius `R` on an eccentric
orbit of semi-major axis `a` and eccentricity `e` about a perturber of mass `M_p`,
the orbit-averaged dissipated power is

    Ė  =  (21/2) · (k₂/Q) · (G M_p² R⁵ n e²) / a⁶

with the mean motion `n = √(G(M_p + m)/a³) ≈ √(G M_p / a³)` (for `m ≪ M_p`).
Substituting `n` makes the steep distance dependence explicit:

    Ė  ∝  (k₂/Q) · R⁵ · e² · M_p^(3/2) · a^(−15/2)

Every term:

| Symbol | Meaning | Where it comes from |
|---|---|---|
| `k₂` | degree-2 tidal Love number (potential response of the body) | interior structure (§5) |
| `Q` | tidal quality factor (1/Q ≈ phase lag = fraction of energy lost per cycle) | rheology (§5) |
| `G` | gravitational constant | – |
| `M_p` | mass of the **perturber** (the planet, for a moon; the star, for a planet) | DB |
| `R` | radius of the **heated** body | DB |
| `n` | mean motion = `2π/P_orb` = `√(G M_p / a³)` | orbit |
| `e` | orbital eccentricity | orbit (must be *maintained*, §4) |
| `a` | semi-major axis of the heated body's orbit about the perturber | orbit |

The `(21/2)` prefactor is standard for the synchronous, zero-obliquity, small-`e`
case (the leading `e²` term of the tidal-potential expansion). The grouping
`k₂/Q` is what the body's material contributes; everything else is geometry and the
perturber's mass.

Two equivalent reductions are useful in practice. **(a)** The surface heat flux is
`F = Ė / (4πR²)`, the number that decides volcanism/melting (§6). **(b)** Holding
`k₂/Q`, `e`, `R` fixed, `Ė ∝ a^(−15/2)`: **a factor-2 in orbital distance changes
the heating by ~180×.** This `a⁻⁷·⁵` collapse is the dominant behaviour and the
hard lesson of §3.

The fixed-Q form is a *first-order* tool: `k₂` and `Q` are treated as
constant numbers, which hides all the temperature- and frequency-dependence of real
material response. §5 covers when that breaks and what replaces it.

---

## 2. Calibration: the formula reproduces Io and Enceladus

The formula is only trustworthy because it reproduces the two bodies whose internal
output is actually *measured*. These observed numbers calibrate `k₂/Q`.

| Body | Perturber | a (R_p) | e (forced) | observed Ė | observed flux | formula reproduces with |
|---|---|---|---|---|---|---|
| **Io** | Jupiter | ~5.9 R_J | ~0.0041 | ~0.6–1.6 ×10¹⁴ W | ~2 W/m² (global) | k₂/Q ~ 0.015 (k₂≈0.3, Q≈20) |
| **Enceladus** | Saturn | ~3.95 R_Sat | ~0.0047 | ~5–16 GW (≈10¹⁰ W) | ~5 GW from the SPT | k₂/Q ~ 0.002–0.01 (soft ice + ocean) |

- **Io**: the calibration anchor. Infrared radiometry (Veeder+ 1994
  [`1994JGR....9917095V`](https://ui.adsabs.harvard.edu/abs/1994JGR....9917095V); Veeder+ 2012 [`2012Icar..219..701V`](https://ui.adsabs.harvard.edu/abs/2012Icar..219..701V)) puts the global heat
  output at ~10¹⁴ W, i.e. a surface flux ~2 W/m², an order of magnitude above
  Earth's ~0.08 W/m². Lainey+ 2009 ([`2009Natur.459..957L`](https://ui.adsabs.harvard.edu/abs/2009Natur.459..957L)) confirmed *active*
  strong dissipation in the Io–Jupiter system from astrometry, closing the loop:
  the dissipation the formula needs is the dissipation the orbit shows. With Io's
  `a`, `e`, `R`, `M_J` and `k₂/Q ≈ 0.015`, the formula returns ~10¹⁴ W. ✓
- **Enceladus**: the low-mass-body anchor. Cassini found an active south-polar
  thermal anomaly and plumes (Spencer+ 2006 [`2006Sci...311.1401S`](https://ui.adsabs.harvard.edu/abs/2006Sci...311.1401S)); Howett+ 2011
  ([`2011JGRE..116.3003H`](https://ui.adsabs.harvard.edu/abs/2011JGRE..116.3003H)) measured ~15.8 GW from the south-polar terrain, and the
  endogenic total is several GW (~10¹⁰ W). Nimmo+ 2007 ([`2007Natur.447..289N`](https://ui.adsabs.harvard.edu/abs/2007Natur.447..289N))
  attributes the plumes to shear heating along the tiger stripes. Enceladus is tiny
  (`R ≈ 252 km`) so its `R⁵` is ~10⁹× smaller than Io's; the formula returns the
  ~GW scale with a soft-ice + ocean `k₂/Q` (Meyer & Wisdom 2007 [`2007Icar..188..535M`](https://ui.adsabs.harvard.edu/abs/2007Icar..188..535M)).
  ✓

The calibration spans **four orders of magnitude in Ė** (10¹⁴ → 10¹⁰ W) and a
factor ~25 in radius, and the same single formula covers both. That is the evidence
that the order-of-magnitude recipe is sound, *provided* `k₂/Q` is chosen for the
right body class (§5) and `e` is genuinely maintained (§4).

---

## 3. The a⁻⁷·⁵ distance gate (the hard lesson)

**This is the section to read if you read only one.** Because `Ė ∝ a^(−15/2)`, the
orbital distance dominates every other knob. No amount of favourable `e`, `k₂/Q`,
or resonance can rescue a body that orbits too far out.

Hold Io's `k₂/Q`, `e`, `R`, and Jupiter as the perturber, and move the body out:

| a (R_p) | relative Ė (Io = 1) | absolute scale |
|---|---|---|
| 6 (≈ Io) | 1 | ~10¹⁴ W |
| 10 | ~0.05 | ~10¹³ W |
| 15 | ~0.003 | ~10¹² W |
| 20 | ~5 ×10⁻⁴ | ~10¹¹ W |
| 30 | ~3 ×10⁻⁵ | ~10⁹ W |

A body at **20 R_p gets ~2000× less tidal power than the same body at 6 R_p.** Drop
the radius from Io-sized to a small icy moon (`R⁵` falls another ~10²–10³×) and the
heating collapses to **MW-level**, utterly negligible for melting ice or driving
plumes (Enceladus, by contrast, sits at only ~4 R_Sat, *close in*, which is why a
252 km moon still musters GW).

**The NearStars A b V lesson.** In the α Cen Phase-4 work, the moon **A b V** at
~20 planetary radii was shown by exactly this calculation to receive only
**~MW-level** tidal power, *orders of magnitude too little* to sustain a subsurface
ocean or cryovolcanic plumes. The favourable narrative (resonance, soft interior)
could not lift it past the `a⁻⁷·⁵` gate. So A b V's plumes were accepted as an
**art-first documented divergence** on the Phase-4 board, explicitly *not* a
physically derived feature. By contrast a moon placed close-in (a few R_p) clears
the gate and its heating *is* derivable.

The gate is a one-line sanity check before any detailed estimate: **compute `a` in
perturber radii.** Beyond ~10–15 R_p, expect heating to be negligible for anything
short of a giant, eccentric, resonance-pumped body. And if the design wants a
feature there anyway, flag it as a documented divergence, not a derivation.

---

## 4. The eccentricity-maintenance requirement

Tidal heating runs on `e²`. But tidal dissipation **damps `e`**: the same friction
that heats the body circularizes its orbit, on a timescale that can be far shorter
than the system's age. A body left alone therefore heats *transiently*, then `e → 0`
and the heating **shuts off**. Sustained heating requires something to keep pumping
`e`.

The pump is almost always a **mean-motion resonance** with another body:

- **Io**: the Laplace resonance (Io:Europa:Ganymede 1:2:4). Yoder 1979
  ([`1979Natur.279..767Y`](https://ui.adsabs.harvard.edu/abs/1979Natur.279..767Y)) showed how tidal heating in Io *drives and locks* this
  resonance, which in turn forces Io's `e ≈ 0.0041` against damping. Without it Io's
  orbit would circularize and the volcanism would die.
- **Enceladus**: the 2:1 mean-motion resonance with Dione forces `e ≈ 0.0047`
  (Meyer & Wisdom 2007 [`2007Icar..188..535M`](https://ui.adsabs.harvard.edu/abs/2007Icar..188..535M); Meyer & Wisdom 2008
  [`2008Icar..193..213M`](https://ui.adsabs.harvard.edu/abs/2008Icar..193..213M)). The resonance is what makes a tiny moon geologically alive.

Practical rule: **if you are claiming sustained tidal heating, name the resonance
(or other forcing) that maintains `e`.** A single moon with a measured/assumed `e`
but no maintaining mechanism may simply be in the middle of circularizing: its
`e` (and thus its heating) is a snapshot, not a steady state. For NearStars
synthetic systems, a multi-moon resonant chain (Laplace-like) is the physically
honest way to justify a moon that needs to *stay* hot; a lone eccentric moon should
be flagged as transient unless its circularization time exceeds the system age.

---

## 5. Domain of validity: k₂/Q by body class, and the rheology problem

`k₂/Q` is the **dominant uncertainty**: it spans ~3 orders of magnitude across body
types and is rarely measured for the body in hand. Pick it by class:

| Class | k₂ | Q | k₂/Q | notes |
|---|---|---|---|---|
| **Rocky / silicate** (Io-like, terrestrial) | ~0.1–0.3 | ~10–100 | ~10⁻³–10⁻² | strongly T-dependent; a partially molten interior raises k₂ and lowers Q (more dissipation) |
| **Icy + subsurface ocean** (Enceladus, Europa) | ~0.01–0.1 | ~1–100 | ~10⁻⁴–10⁻² | an ocean decouples the shell and can *raise* dissipation enormously; very model-dependent |
| **Gas / ice giant** | ~0.1–0.6 | ~10³–10⁵ | ~10⁻⁵–10⁻³ | high Q (low dissipation per cycle); relevant when the *giant itself* is the heated body close to a star |

Four regimes / cautions decide whether the fixed-Q recipe is even the right tool:

1. **Rocky synchronous body, small e**: the recipe's home turf (Peale+ 1979;
   calibrated on Io). Use the rocky `k₂/Q` band and report an order of magnitude.
2. **Icy body with an ocean**: the fixed-Q number is a *floor*; an ocean-decoupled
   shell can dissipate far more than a homogeneous-Q estimate, so a low fixed-Q
   `Ė` does **not** rule out an active ocean. Cross-check against a viscoelastic
   model before declaring a moon dead.
3. **Viscoelastic / rheological regime**: when `Ė` from §1 is near a melting or
   ocean threshold, the fixed-Q answer is unreliable and must be replaced by a
   frequency- and temperature-dependent **Maxwell / Andrade** treatment: Segatz+
   1988 ([`1988Icar...75..187S`](https://ui.adsabs.harvard.edu/abs/1988Icar...75..187S), the founding viscoelastic-Io model), Henning,
   O'Connell & Sasselov 2009 ([`2009ApJ...707.1000H`](https://ui.adsabs.harvard.edu/abs/2009ApJ...707.1000H), tidally heated terrestrial
   exoplanets), Henning & Hurford 2014 ([`2014ApJ...789...30H`](https://ui.adsabs.harvard.edu/abs/2014ApJ...789...30H), multilayered),
   Renaud & Henning 2018 ([`2018ApJ...857...98R`](https://ui.adsabs.harvard.edu/abs/2018ApJ...857...98R), Andrade vs Maxwell, heating can
   differ by **large factors**, often >10×, and peaks at a resonant interior
   temperature). The fixed-Q and Andrade answers can disagree by an order of
   magnitude; that gap *is* the error bar.
4. **Spin-orbit / non-synchronous, or near a spin-orbit resonance**: the `(21/2)e²`
   leading term is wrong; use the Efroimsky & Makarov frequency-dependent formalism
   (Efroimsky & Williams 2012 [`2012CeMDA.112..283E`](https://ui.adsabs.harvard.edu/abs/2012CeMDA.112..283E)). Mostly relevant to bodies
   *not* yet locked, i.e. the locking-doc territory flagged at the top.

For NearStars, the practical posture: use the fixed-Q formula with a class-`k₂/Q`
band, report the **range** (not a point), and where the answer lands near a
volcanism/ocean threshold, defer to the viscoelastic literature and widen the
uncertainty rather than over-claim.

---

## 6. Deciding the outcome: volcanism / ocean / plumes

§1–§5 answer *how much power is generated*. That is only half the problem: the power
has to **leave through the surface**, and above a few W/m² the exit is the binding
constraint, not the generation. §6.1 is the quick verdict table; §6.2–§6.5 are the
transport side, which is what decides whether a designed high-flux body is physically
possible at all.

### 6.1 The flux → regime table

Convert `Ė` to a **surface heat flux** `F = Ė / (4πR²)` and compare to thresholds
(these are guides, not sharp lines):

| Surface flux F | regime | analog |
|---|---|---|
| ≳ 1 W/m² | vigorous silicate volcanism, possible magma ocean | Io (~2 W/m²) |
| ~0.1–1 W/m² | active resurfacing, episodic volcanism | active icy/rocky worlds |
| ~0.01–0.1 W/m² | enough to maintain a subsurface ocean under an ice shell | Enceladus SPT, Europa |
| ≲ 10⁻³ W/m² | geologically dead; no ocean, no plumes from tides alone | far/airless moons |

The chain: **(1)** compute `a` in R_p, apply the §3 gate first (if `a ≳ 10–15 R_p`
and the body is small, the answer is almost certainly "dead", stop). **(2)** confirm
`e` is *maintained* (§4): name the resonance, or flag the heating as transient.
**(3)** pick a class `k₂/Q` band (§5) and compute `Ė` and `F` as a range. **(4)**
map `F` to the table; if it lands near a threshold, escalate to a viscoelastic
cross-check (§5 regime 3) before committing. **(5)** record the chosen `k₂/Q`, the
maintaining resonance, and the resulting `F`-range on the Phase-4 board, and where
art overrides a "dead" verdict, mark it a **documented divergence**, never a silent
upgrade. **(6)** if `F ≳ 1 W/m²`, the verdict "vigorous volcanism" is not the end of
the check — run the transport test of §6.2–§6.4, which is what fails for oversized
designs.

Note that tidal heating is one heat source among several (radiogenic, accretional,
primordial). For an Earth-mass body radiogenic heating alone is ~0.08 W/m²; tidal
heating matters when it *exceeds* that. For small icy moons radiogenic heat is
negligible and tides are essentially the only knob, which is why the distance gate
is so decisive for them.

### 6.2 How the heat actually leaves: the three-mode ladder

A body's surface has exactly three ways to pass internal heat, and they differ by
**four orders of magnitude in capacity**. Which one the body is in is set by the flux
itself, so the mode is an output of §6.1, not a free choice.

| Mode | Mechanism | Capacity | Anchor body |
|---|---|---|---|
| **Plate tectonics** | the lid itself is recycled | ~0.09 W/m² | Earth, **92.1 mW/m²** (47±2 TW from 38,347 measurements, [`2010SolE....1....5D`](https://ui.adsabs.harvard.edu/abs/2010SolE....1....5D)) |
| **Stagnant lid** | conduction through an immobile lid | ceiling **10–30 mW/m²** | Venus 10–20, Mars 15–30 ([`1998JGR...10313643R`](https://ui.adsabs.harvard.edu/abs/1998JGR...10313643R)) |
| **Heat pipe** | melt migrates through the lid and erupts | ≥ ~2.5 W/m², no firm upper bound | Io; early Earth ([`2019JGRE..124..114K`](https://ui.adsabs.harvard.edu/abs/2019JGRE..124..114K)) |

The decisive fact for any tidally heated body above ~0.1 W/m²: **conduction is not an
option.** Reese, Solomatov & Moresi 1998 ([`1998JGR...10313643R`](https://ui.adsabs.harvard.edu/abs/1998JGR...10313643R)) put the
stagnant-lid conductive ceiling at 10–30 mW/m² before widespread melting sets in —
two orders of magnitude below Io. Moore 2003 ([`2003JGRE..108.5096M`](https://ui.adsabs.harvard.edu/abs/2003JGRE..108.5096M)) shows even
solid-state convection *"falls an order of magnitude short"* of Io's flux. What is
left is **advection**: melt segregates, rises, and carries its latent heat to the
surface.

The governing surface energy balance is Spencer, Katz & Hewitt 2020
([arXiv:2003.08287](https://arxiv.org/abs/2003.08287)), whose eq. 33 converts a
dissipation rate `Ψ` directly into a resurfacing rate,

    q_s  =  Ψ / [ 4πR² ( ρL + ρ c (T_m − T_s) ) ]

with `ρ` density, `L` latent heat of fusion, `c` specific heat, `T_m` melt
temperature and `T_s` surface temperature. Conduction is **dropped from the balance**
because it is negligible. Their Io reference solution (Table 1: ρ=3000 kg/m³,
L=4×10⁵ J/kg, c=1200 J/kg/K, T_m=1500 K, T_s=150 K, Ψ=10¹⁴ W) returns **99.5 % of
surface heat transport as volcanic**, a resurfacing rate of 1.25 cm/yr matching Io's
observed rate, and an **80 km elastic thickness**. Their eqs. 34–35 further split
erupted from intruded melt: **~80 % of Io's magma is emplaced within the crust rather
than erupted**, which matters when converting a heat budget into visible lava. The
paper explicitly offers eq. 10 for reuse — *"provides a means of estimating eruption
rates for other tidally heated lava-worlds, utilising their tidal heating rate, size,
and surface temperature"* — so this is the sanctioned formula for a synthetic body,
not an analogy. For lid thickness, mantle temperature and the residual conductive
flux, Kankanamge & Moore 2019 ([`2019JGRE..124..114K`](https://ui.adsabs.harvard.edu/abs/2019JGRE..124..114K), doi
10.1029/2018JE005800) give a heat-pipe parameterization validated to <15 % against
numerical simulation.

**The counter-intuitive consequence: high flux gives a THICK lid, not a thin one.**
Heat piping *"produces a thick, cold, and strong lithosphere"* (Moore & Webb 2017,
[`2017E&PSL.474...13M`](https://ui.adsabs.harvard.edu/abs/2017E%26PSL.474...13M)), and O'Reilly & Davies 1981
([`1981GeoRL...8..313O`](https://ui.adsabs.harvard.edu/abs/1981GeoRL...8..313O)) titled the mechanism exactly that — *a mechanism
allowing a **thick** lithosphere*. Conduction alone would force Io's lithosphere down
to ~5 km; advection lets it be thick. Observations agree: ≥12 km from mountain volume
([`2003JGRE..108.5093J`](https://ui.adsabs.harvard.edu/abs/2003JGRE..108.5093J)), ≥30 km from mountain distribution
([`1998Icar..135..146C`](https://ui.adsabs.harvard.edu/abs/1998Icar..135..146C)), 35–80 km in models — a lid that by conduction
passes only **3–7 % of Io's flux**.

So the design rule is the inverse of the intuitive one: **you cannot buy a thicker
crust by raising the heat, and a high-flux body does not have a centimetre-scale
crust.** It has a thick cold lid pierced by discrete melt conduits, and *those* have
to carry essentially all of the power.

### 6.3 The plains are not an exit

If the lid conducts ~0.1 W/m², the terrain between volcanic centres is thermally
**inert**: it sits at radiative equilibrium with its external budget (starlight, plus
the parent's contribution for a moon — see
[`moon-energy-budget-methodology.md`](moon-energy-budget-methodology.md)) and carries
none of the interior's heat.

Io confirms this directly. Its background plains are **110–130 K, purely
insolation-driven** — a frost model with Bond albedo 0.56 and thermal inertia 250 MKS
fits 22 years of data ([arXiv:2405.19253](https://arxiv.org/abs/2405.19253);
equatorial frost 106–116 K), and between hot spots the endogenic contribution is
**<1 W/m²** ([`2004Icar..169..127R`](https://ui.adsabs.harvard.edu/abs/2004Icar..169..127R)). On a body radiating 2.5 W/m² on
average, the plains are cold.

The heat is therefore concentrated into a small fraction of the surface:

- active volcanoes occupy **≈2 %** of Io's surface ([arXiv:2310.12382](https://arxiv.org/abs/2310.12382));
- **50 % of the heat flow comes from 1.2 % of the surface** ([`2012Icar..219..701V`](https://ui.adsabs.harvard.edu/abs/2012Icar..219..701V));
- patera floors are 2.5 % of the surface but host **64 % of detected hot spots**
  ([`2011Icar..214...91W`](https://ui.adsabs.harvard.edu/abs/2011Icar..214...91W)).

The literature predicts this shape for exo-bodies too, not just Io. Henning,
O'Connell & Sasselov 2009 ([arXiv:0912.1907](https://arxiv.org/abs/0912.1907)) find
tides alone unlikely to open a *surface* magma ocean (it would take *"half a million
TW or more"*, ≈980 W/m² on an Earth-radius body), and that *"thin-layer global
resurfacing as on Io is unlikely for viscous lavas. This supports the notion of
searching for small radiantly cooled hotspots on supertidal exoplanets."*

**Two consequences for Phase-4 work.** (a) A warm plains temperature is not an art
choice — it is a claim that the lid is metres thick, which cannot support topography.
Set the plains from the external budget and leave them there. (b) Conservation still
binds: the area-weighted `σT⁴` mean must equal `F`, so concentrating the heat makes
the hot spots *hotter*, and their temperature — not the plains' — is what the
transport check has to survive.

### 6.4 The lava-lake capacity test (and the two-denominator trap)

Since the lakes carry all of it, the test for any high-flux design is arithmetic:

    required areal flux  =  F / (lake area fraction)

and that number has to fall inside the **measured** capacity of a real lava lake.

**First, the trap.** Two different denominators are in use in the literature and they
differ by two orders of magnitude. Dividing a patera's power by its *geologic floor
area* gives a crust-dominated ~300 K number; dividing by the *fitted
equivalent-blackbody area* gives a crust-corrected proxy at 600–940 K. **Never mix
them, and always state which one a quoted flux uses.** Loki Patera makes the gap
concrete: 9.6×10¹² W ([`2012Icar..219..701V`](https://ui.adsabs.harvard.edu/abs/2012Icar..219..701V)) over its 21,500 km² floor
([`2017Natur.545..199D`](https://ui.adsabs.harvard.edu/abs/2017Natur.545..199D)) is **446–465 W/m², i.e. 298–301 K** — corroborated
independently by JIRAM crust brightness temperatures of 270–355 K
([arXiv:2410.10686](https://arxiv.org/abs/2410.10686)) — while Pele's *fitted* 6.5 km²
gives **44.3 kW/m² at 940 K** ([`2016Icar..264..198D`](https://ui.adsabs.harvard.edu/abs/2016Icar..264..198D)).

**The ceiling.** Bare, crust-free melt radiates `σ T_erupt⁴`. Io's eruption
temperature was revised down from ~1600 °C to **~1340 °C = 1613 K**
([`2007Icar..192..491K`](https://ui.adsabs.harvard.edu/abs/2007Icar..192..491K)), giving **384 kW/m²**. That is an absolute
upper bound, and **no observed lake comes close** — the record is 59 % of it:

| Object | Area | Areal flux | T_eff | Note |
|---|---|---|---|---|
| Nyamuragira 2014 | 900 m² | **111 kW/m²** | 1,199 K | observed MAXIMUM ([`2023FrEaS..1140199C`](https://ui.adsabs.harvard.edu/abs/2023FrEaS..1140199C) Table 1) |
| Kilauea 2008 / Ambrym 2015 | 300 / 4,000 m² | 100 kW/m² | 1,167 K | same table |
| Erta Ale (FLIR) | ~1,000 m² | 45–76 kW/m² | 944–1,076 K | [`2008GGG.....912008S`](https://ui.adsabs.harvard.edu/abs/2008GGG.....912008S) |
| Nyiragongo 2017 | 50,000 m² | 24 kW/m² | 817 K | large ⇒ crusted |
| Kilauea 2015 | 30,000 m² | 23.3 kW/m² | 811 K | large ⇒ crusted |
| Erebus Ray Lake | ~1,400 m² | 21–25 kW/m² | 784–815 K | [`2008JVGR..177..695C`](https://ui.adsabs.harvard.edu/abs/2008JVGR..177..695C); lidar area 535–1,709 m² ([`2015JVGR..295...43J`](https://ui.adsabs.harvard.edu/abs/2015JVGR..295...43J)) |
| Kupaianaha stages 1 / 3 | sub-m² | 22 / 4.9 kW/m² | 789 / 542 K | [`1993JGR....98.6461F`](https://ui.adsabs.harvard.edu/abs/1993JGR....98.6461F) |

The reason nothing reaches 384 kW/m² is the **crust**. The crust-free fraction runs
from 10⁻⁵ (quiescent, thick crust) to ~0.3 (vigorous): organized lakes are *">80 %
covered by a cooling skin"* while chaotic ones are *"mostly crust-free and
incandescent"* (Campion & Coppola 2023, citing [`2019JVGR..381...16L`](https://ui.adsabs.harvard.edu/abs/2019JVGR..381...16L)); Erta
Ale often exceeds 90 % crust against Marum's ≤30 % ([`2016JVGR..322..105R`](https://ui.adsabs.harvard.edu/abs/2016JVGR..322..105R)).

Note the trend in the table: **bigger lakes are more crusted, hence cooler per unit
area.** That is supply-limited, not a capacity ceiling — surface speed correlates with
gas flux and lake area ([`2019JVGR..381...16L`](https://ui.adsabs.harvard.edu/abs/2019JVGR..381...16L)) and crust lifetime falls with
transit velocity ([`2005JVGR..142..207H`](https://ui.adsabs.harvard.edu/abs/2005JVGR..142..207H)) — so it does not forbid a
high-flux large lake outright. But it does mean the honest test is the band, not the
bound:

> **Transport test.** `F / f_lake` must land inside the measured band, **≲111 kW/m²**,
> and comfortably below the 384 kW/m² bare-melt ceiling. A design that needs more is
> asking for crust-free exposed melt across the lakes' entire area — which nothing
> observed does.

Worked the other way, this fixes lake area from size, or size from lake area. Sanity
check on Io itself: 2.5 W/m² through ~0.05 % of its area needs 5.0 kW/m², i.e. **545 K**
— squarely inside the observed band, so the relation is not tuned to any NearStars body.

### 6.5 The super-Io ceiling: what size a lava moon can be

Published work bounds how far past Io a sustainable body can go: **1–3 orders of
magnitude above Io = 25–2,500 W/m²**, with the sustainable branch being heat piping
through a thick cold lid rather than a global melt ([`2021PSJ.....2..119R`](https://ui.adsabs.harvard.edu/abs/2021PSJ.....2..119R),
adopted by [arXiv:2305.03410](https://arxiv.org/abs/2305.03410)). A magma ocean needs
melt fraction above ~0.45 — itself disputed (0.30 / 0.45 / 0.50), and there is **no
published W/m² boundary** between the modes, because the real criterion is melt
fraction and any flux threshold is a conversion, not a citation.

Because `Ė ∝ R⁵` while area ∝ `R²`, **surface flux scales as `R³` at fixed density**:
doubling a moon's radius multiplies its flux eightfold and its required lake flux with
it. Size is therefore the strongest transport knob, and the transport test above turns
into a hard radius ceiling.

**Worked example — Dante (Alpha Centauri A b I), 2026-08-21.** The body was drafted at
900 km, and the transport test is what rejected that. Holding density at 2,620 kg/m³
and scaling from the drafted 900 km / 1,200× Io / 11,500 W/m²:

| R | mass (kg) | output | F | 5 %-lake required areal flux | verdict |
|---|---|---|---|---|---|
| 900 km (drafted) | 8.0×10²¹ | 1,200× Io | 11,500 W/m² | 230 kW/m² | **2.1× the observed max — impossible** |
| 714 km | 3.99×10²¹ | 377× | 5,742 W/m² | 114.8 kW/m² | exactly at the record max |
| **521 km (adopted)** | **1.552×10²¹** | **78×** | **2,231 W/m²** | **44.6 kW/m²** | **Erta Ale class — inside the band** |
| 450 km | 1.0×10²¹ | 38× | 1,438 W/m² | 28.8 kW/m² | Erebus class |

At 900 km the design was implicitly demanding a centimetre-scale crust and lakes hotter
than molten rock; §6.2 says the crust cannot be thin and §6.4 says the lakes cannot be
that hot. **521 km** satisfies both, sits inside the published super-Io envelope
(2,231 < 2,500 W/m², which caps the radius at 541 km), gives an area-averaged 452 K, and
leaves the plains at their external-budget 223 K — cold enough that elemental sulfur is
stable while SO₂ frost is not (frost needs ≤120 K, [`1988Icar...75..450M`](https://ui.adsabs.harvard.edu/abs/1988Icar...75..450M);
sulfur vacuum-boils by ~500 K), which is what makes the surface read as sulfur-toned
rather than white.

Two by-products worth recording, because they are what make the check cheap to redo:

- **`J₂` and `C₂₂` are radius-independent at fixed density.** The tidal-figure
  parameter is `q = M_p / ((4/3)πρa³)`, in which the heated body's own radius does not
  appear. Resizing a moon changes its mass, gravity and flux; it does **not** change
  its flattening, its triaxial *ratios*, or its rotation period.
- The absolute relief does scale. Dante's `J₂ = 0.039` through the volume-conserving
  synchronous figure of [`body-figure-methodology.md`](body-figure-methodology.md)
  (`a/R = 1 + 7J₂/3`, `b/R = 1 − 2J₂/3`, `c/R = 1 − 5J₂/3`) gives `a = 568.4`,
  `b = 507.4`, `c = 487.1 km`: a sub-planet-to-pole relief of **81.2 km**, which is the
  height budget available to a canyon wall once a spherical sea level is imposed at the
  polar radius.

---

## 7. Worked examples

**Io (the calibration).** `M_p = M_Jupiter`, `R = 1822 km`, `a = 421,700 km`
(~5.9 R_J), `e = 0.0041` (Laplace-maintained), rocky `k₂/Q ≈ 0.015`. The fixed-Q
formula returns `Ė ~ 10¹⁴ W`, `F ~ 2 W/m²`, matching Veeder+ 2012. Verdict:
vigorous silicate volcanism, **derived** (resonance named, flux measured). This is
the anchor every other estimate is scaled against.

**Enceladus (the small-body calibration).** `M_p = M_Saturn`, `R = 252 km`,
`a ≈ 238,000 km` (~3.95 R_Sat, *close in*), `e = 0.0047` (Dione 2:1), soft-ice +
ocean `k₂/Q ~ 10⁻³`. Despite `R⁵` being ~10⁹× smaller than Io's, the small `a` keeps
it inside the gate and the formula returns the observed ~GW / ~10⁻² W/m² over the
south-polar terrain. Verdict: subsurface ocean + plumes, **derived**. The lesson:
*close-in beats big*, a tiny moon at 4 R_p outperforms a large one at 20 R_p.

**α Cen application: close vs far (the project case).** Treat the α Cen Phase-4
moons qualitatively (board values, not reproduced here):
- A moon placed **close-in (a few R_p)**, in a resonant chain that maintains `e`,
  clears the §3 gate. Its `Ė` is in the GW–TW range depending on `R` and `k₂/Q`,
  enough for an active ocean or volcanism, a **derived** feature with the resonance
  named on the board.
- **A b V at ~20 R_p** fails the gate: the `a⁻⁷·⁵` collapse drops `Ė` to
  **~MW-level**, ~5×10⁻⁴ of the close-in case, far below any ocean/plume threshold.
  Its cryovolcanic plumes are therefore an **art-first documented divergence** on the
  Phase-4 board, recorded as a deliberate choice that overrides the physics, not a
  value the recipe produced. This is the canonical example of §8's honesty rule.

**A b II — two refutations worth keeping (moved off the board, 2026-07-28).** Two
plausible-sounding arguments failed on this body and generalize to any Io-type case:

1. *"High internal heat, but a small rigid moon has a low k₂/Q, so the energy
   channels into tectonics instead of melting"* is wrong twice. A low `k₂/Q` does not
   redirect the heat — it means the heat is never **generated** (any Io-multiple
   figure already assumes a `k₂/Q`; lowering one lowers the other). And tectonics is
   not a heat sink: deformation energy still leaves the body as radiation, so
   conservation pins the area-weighted `σT⁴` mean no matter how the heat concentrates
   into hotspots. You cannot buy a cold surface with a hot interior.
2. *"Just lower the eccentricity in the initial conditions."* When a much larger
   neighbor forces `e` (A b II: A b III at 770× its mass, period ratio 2.22), the
   stability sim returns the same `e_max` for any initial `e` — three runs with
   `e_init` 0.005/0.010/0.020 all came back at 0.047–0.064. Forced eccentricity is a
   property of the architecture, not of the starting state; only moving the
   architecture changes the heat.

---

## 8. Honesty & uncertainty

In the spirit of the dynamo doc's caveats:

- **`k₂/Q` is the dominant unknown.** It spans ~3 orders of magnitude across body
  classes (§5) and is essentially never measured for an exo-body. The output is an
  **order-of-magnitude** estimate; quote a range, not a point.
- **Fixed-Q vs viscoelastic can differ by large factors.** The constant-Q formula
  (§1) is a first-order tool. Andrade/Maxwell models (Renaud & Henning 2018) can give
  >10× different `Ė`, and the heating peaks sharply at a resonant interior
  temperature the fixed-Q model cannot represent. Near any threshold, the model
  choice *is* the error bar.
- **`e` must be maintained or the heating is transient** (§4). A snapshot `e` with no
  resonance is not a steady heat source.
- **The `a⁻⁷·⁵` gate is hard physics, not a tunable.** Where a NearStars body needs a
  feature the gate forbids (A b V), that is a **documented divergence**, flagged on
  the board as art overriding physics, never dressed up as a derivation. The method's
  value is precisely that it tells you honestly when a feature is *not* physically
  supported, so the override is an explicit, recorded choice.

On the **transport** side (§6.2–§6.5) the uncertainties are different in kind — the
mechanism is solid, the numbers are noisy:

- **Emissivity is disputed and the flux scales with it.** 0.74 measured in the field at
  Erta Ale ([`2002BVol...64..472B`](https://ui.adsabs.harvard.edu/abs/2002BVol...64..472B)) against 0.95 assumed by Campion &
  Coppola: **±28 %** on every areal flux in §6.4.
- **Radiant output spans 3× by method.** Erta Ale is quoted at 5–30, 45–76 and
  100–400 MW depending on whether the number is radiative-only or total surface heat.
  Always state which. The Campion & Coppola lake areas are photographic estimates, so
  their fluxes are order-of-magnitude.
- **Fitted single-blackbody temperatures are not physical temperatures**
  ([arXiv:1906.05426](https://arxiv.org/abs/1906.05426)) — they are the proxy that goes
  with the fitted-area denominator, and only that.
- **41–46 % of Io's heat flow is from unidentified sources**
  ([`2012Icar..219..701V`](https://ui.adsabs.harvard.edu/abs/2012Icar..219..701V), [`2015Icar..245..379V`](https://ui.adsabs.harvard.edu/abs/2015Icar..245..379V)), so even the
  anchor body's hot-spot census is incomplete.
- **The mode boundaries are not citable in W/m².** §6.2's ladder is a capacity
  comparison, not a published threshold set; the physical criterion is melt fraction
  (critical value disputed: 0.30 / 0.45 / 0.50).
- Several transport sources predate arXiv or are paywalled and are therefore verified
  by ADS bibcode and abstract rather than full text: Kankanamge & Moore 2019,
  Moore 2003, Moore & Webb 2017, Reese 1998, the Veeder series, Harris 1999/2005/2008,
  Lev 2019. Harris 1999/2008 and Lev 2019 are the three whose full text would most
  improve the crust-fraction scaling if this section ever needs it quantitatively.

The method is grounded and calibrated (it reproduces Io and Enceladus across 4 dex
in `Ė`); the *inputs* (`k₂/Q`, the rheology, the maintenance of `e`) carry the
uncertainty. Confidence is **order-of-magnitude**, and that is enough to make the
volcanism/ocean/plume call correctly in nearly every case, because the `a⁻⁷·⁵`
distance term usually decides the answer long before `k₂/Q` matters.

---

## 9. Annotated Bibliography

Each entry: authors, year, journal, **verified** arXiv id (or "no arXiv" + bibcode),
ADS citation count, and one line on the contribution.

- **Peale, S. J., Cassen, P. & Reynolds, R. T. (1979)**: *Science* 203, 892.
  **No arXiv** ([`1979Sci...203..892P`](https://ui.adsabs.harvard.edu/abs/1979Sci...203..892P)). Cites: 530. The founding tidal-heating
  paper: the fixed-Q formula and the pre-Voyager prediction that Io would be melted.
  §1.
- **Yoder, C. F. (1979)**: *Nature* 279, 767. **No arXiv** ([`1979Natur.279..767Y`](https://ui.adsabs.harvard.edu/abs/1979Natur.279..767Y)).
  Cites: 178. How tidal heating in Io drives and locks the Galilean (Laplace)
  resonance that maintains Io's eccentricity. §4.
- **Segatz, M. et al. (1988)**: *Icarus* 75, 187. **No arXiv**
  ([`1988Icar...75..187S`](https://ui.adsabs.harvard.edu/abs/1988Icar...75..187S)). Cites: 258. Founding viscoelastic (Maxwell) Io model:
  tidal dissipation, surface heat flow and figure beyond fixed-Q. §5.
- **Veeder, G. J. et al. (1994)**: *JGR* 99, 17095. **No arXiv**
  ([`1994JGR....9917095V`](https://ui.adsabs.harvard.edu/abs/1994JGR....9917095V)). Cites: 217. Io's global heat flow from infrared
  radiometry (~10¹⁴ W): the Io calibration. §2.
- **Spencer, J. R. et al. (2006)**: *Science* 311, 1401. **No arXiv**
  ([`2006Sci...311.1401S`](https://ui.adsabs.harvard.edu/abs/2006Sci...311.1401S)). Cites: 518. Cassini's discovery of Enceladus's active
  south-polar thermal anomaly and plumes. §2.
- **Meyer, J. & Wisdom, J. (2007)**: *Icarus* 188, 535. **No arXiv**
  ([`2007Icar..188..535M`](https://ui.adsabs.harvard.edu/abs/2007Icar..188..535M)). Cites: 152. Tidal heating in Enceladus and the
  Enceladus–Dione 2:1 resonance maintaining its eccentricity. §2, §4.
- **Nimmo, F. et al. (2007)**: *Nature* 447, 289. **No arXiv**
  ([`2007Natur.447..289N`](https://ui.adsabs.harvard.edu/abs/2007Natur.447..289N)). Cites: 239. Shear heating along the tiger stripes as the
  origin of Enceladus's plumes and heat flux. §2.
- **Jackson, B., Barnes, R. & Greenberg, R. (2008)**: *ApJ* 681, 1631.
  **[arXiv:0803.0026](https://arxiv.org/abs/0803.0026).** Cites: 155. "Tidal Heating of Extrasolar Planets": applies
  the fixed-Q heating formula to close-in exoplanets and its surface-condition
  magnitude. §1, §3. (Companion: Jackson+ 2008 *ApJ* 678, 1396, **[arXiv:0802.1543](https://arxiv.org/abs/0802.1543)**,
  cites 382, the tidal-evolution / eccentricity-damping side.)
- **Lainey, V. et al. (2009)**: *Nature* 459, 957. **No arXiv**
  ([`2009Natur.459..957L`](https://ui.adsabs.harvard.edu/abs/2009Natur.459..957L)). Cites: 359. Astrometric detection of *active* strong tidal
  dissipation in the Io–Jupiter system: empirically closes the heating loop. §2.
- **Henning, W. G., O'Connell, R. J. & Sasselov, D. D. (2009)**: *ApJ* 707, 1000.
  **[arXiv:0912.1907](https://arxiv.org/abs/0912.1907).** Cites: 158. Tidally heated terrestrial exoplanets with a
  viscoelastic response model: the exoplanet-rheology bridge. §5.
- **Howett, C. J. A. et al. (2011)**: *JGR Planets* 116, E03003. **No arXiv**
  ([`2011JGRE..116.3003H`](https://ui.adsabs.harvard.edu/abs/2011JGRE..116.3003H)). Cites: 136. ~15.8 GW measured from Enceladus's south-polar
  region: the Enceladus calibration number. §2.
- **Veeder, G. J. et al. (2012)**: *Icarus* 219, 701. **No arXiv**
  ([`2012Icar..219..701V`](https://ui.adsabs.harvard.edu/abs/2012Icar..219..701V)). Cites: 92. Io's volcanic thermal sources and global heat
  flow: the updated ~10¹⁴ W census. §2.
- **Efroimsky, M. & Williams, J. G. (2012)**: *Celest. Mech. Dyn. Astron.* 112, 283.
  **[arXiv:1105.6086](https://arxiv.org/abs/1105.6086).** Cites: 128. Bodily tides near spin-orbit resonances: the
  frequency-dependent formalism beyond fixed-Q for non-synchronous bodies. §5.
- **Barnes, R. et al. (2013)**: *Astrobiology* 13, 225. **[arXiv:1203.5104](https://arxiv.org/abs/1203.5104).** Cites:
  120. "Tidal Venuses": tidal heating can trigger a runaway greenhouse, the upper
  habitability bound on tidal heat. §6 context.
- **Heller, R. & Barnes, R. (2013)**: *Astrobiology* 13, 18. **[arXiv:1209.5323](https://arxiv.org/abs/1209.5323).**
  Cites: 129. Exomoon habitability constrained by illumination *and* tidal heating:
  the moon-specific habitability bound directly relevant to NearStars moons. §6.
- **Henning, W. G. & Hurford, T. (2014)**: *ApJ* 789, 30. **No arXiv**
  ([`2014ApJ...789...30H`](https://ui.adsabs.harvard.edu/abs/2014ApJ...789...30H)). Cites: 55. Tidal heating in multilayered terrestrial
  exoplanets: layered viscoelastic structure. §5.
- **Driscoll, P. E. & Barnes, R. (2015)**: *Astrobiology* 15, 739.
  **[arXiv:1509.07452](https://arxiv.org/abs/1509.07452).** Cites: 108. Tidal heating of Earth-like planets around M
  stars and its coupling to thermal/magnetic evolution and habitability. §6.
- **Renaud, J. P. & Henning, W. G. (2018)**: *ApJ* 857, 98. **[arXiv:1707.06701](https://arxiv.org/abs/1707.06701).**
  Cites: 82. Increased tidal dissipation using advanced (Andrade) rheology: shows
  fixed-Q and Andrade can differ by large factors. §5, §8.

**Surface heat transport (§6.2–§6.5).** Verified in the same ADS pass, 2026-08-21.

- **O'Reilly, T. C. & Davies, G. F. (1981)**: *Geophys. Res. Lett.* 8, 313. **No arXiv**
  ([`1981GeoRL...8..313O`](https://ui.adsabs.harvard.edu/abs/1981GeoRL...8..313O)). Magma transport of heat on Io as *a mechanism
  allowing a **thick** lithosphere* — the founding statement that advection, not
  conduction, carries the heat. §6.2.
- **Reese, C. C., Solomatov, V. S. & Moresi, L.-N. (1998)**: *JGR* 103, 13643.
  **No arXiv** ([`1998JGR...10313643R`](https://ui.adsabs.harvard.edu/abs/1998JGR...10313643R)). Heat transport efficiency for
  stagnant-lid convection: the 10–30 mW/m² conductive ceiling that rules the plains out
  as an exit. §6.2.
- **Moore, W. B. (2003)**: *JGR Planets* 108, 5096. **No arXiv**
  ([`2003JGRE..108.5096M`](https://ui.adsabs.harvard.edu/abs/2003JGRE..108.5096M)). Tidal heating and convection in Io: solid-state
  convection *"falls an order of magnitude short"*, so melt segregation must dominate.
  §6.2.
- **Moore, W. B. & Webb, A. A. G. (2017)**: *Earth Planet. Sci. Lett.* 474, 13.
  **No arXiv** ([`2017E&PSL.474...13M`](https://ui.adsabs.harvard.edu/abs/2017E%26PSL.474...13M)). Heat piping *"produces a thick, cold,
  and strong lithosphere"* — the high-flux/thick-lid result. §6.2.
- **Kankanamge, D. G. J. & Moore, W. B. (2019)**: *JGR Planets* 124, 114. **No arXiv**
  ([`2019JGRE..124..114K`](https://ui.adsabs.harvard.edu/abs/2019JGRE..124..114K), doi 10.1029/2018JE005800). Quantitative heat-pipe
  parameterization (melt flux, mantle and lid-base temperature, **lid thickness**,
  residual conductive flux), validated to <15 % against numerical simulation. §6.2.
- **Spencer, D. C., Katz, R. F. & Hewitt, I. J. (2020)**: *JGR Planets* 125, e06443.
  **[arXiv:2003.08287](https://arxiv.org/abs/2003.08287).** The governing surface energy
  balance (eq. 33) and the erupted/intruded split (eqs. 34–35); 99.5 % volcanic
  transport, 80 km elastic thickness, and an explicit invitation to apply eq. 10 to other
  lava worlds. **The load-bearing citation of §6.2.**
- **Davies, J. H. & Davies, D. R. (2010)**: *Solid Earth* 1, 5. **No arXiv**
  ([`2010SolE....1....5D`](https://ui.adsabs.harvard.edu/abs/2010SolE....1....5D)). Earth's surface heat flow, 47±2 TW = 92.1 mW/m²
  from 38,347 measurements: the plate-tectonics rung of the ladder. §6.2.
- **Rathbun, J. A. et al. (2004)**: *Icarus* 169, 127. **No arXiv**
  ([`2004Icar..169..127R`](https://ui.adsabs.harvard.edu/abs/2004Icar..169..127R)). Io's background thermal emission: endogenic flux
  between hot spots is <1 W/m². §6.3.
- **Veeder, G. J. et al. (2015)**: *Icarus* 245, 379. **No arXiv**
  ([`2015Icar..245..379V`](https://ui.adsabs.harvard.edu/abs/2015Icar..245..379V)). Io's heat-flow census update; with Veeder+ 2012,
  the source of the "41–46 % unidentified" caveat. §8.
- **Veeder, G. J. et al. (2012)** — see §2 above; also supplies the "50 % of the heat
  from 1.2 % of the surface" concentration and Loki's 9.6×10¹² W. §6.3, §6.4.
- **Williams, D. A. et al. (2011)**: *Icarus* 214, 91. **No arXiv**
  ([`2011Icar..214...91W`](https://ui.adsabs.harvard.edu/abs/2011Icar..214...91W)). Io's global geologic map: patera floors are 2.5 %
  of the surface but host 64 % of detected hot spots. §6.3.
- **Davies, A. G. et al. (2024)**: *Nature Astronomy* 8, 94.
  **[arXiv:2310.12382](https://arxiv.org/abs/2310.12382).** Io's total thermal emission
  ≈106 TW with ≈56 TW from volcanic edifices; active volcanoes cover ≈2 % of the
  surface. §6.2, §6.3.
- **Giles, R. S. et al. (2024)**: *Icarus* 418, 116151.
  **[arXiv:2405.19253](https://arxiv.org/abs/2405.19253).** Io's SO₂ atmosphere and the
  frost-temperature model behind it: 22 years of data fit by insolation alone (Bond
  albedo 0.56, thermal inertia 250 MKS), equatorial frost 106–116 K. The evidence that
  the plains are radiative-equilibrium terrain. §6.3.
- **Mura, A. et al. (2025)**: *Planet. Sci. J.* 6, 43.
  **[arXiv:2410.10686](https://arxiv.org/abs/2410.10686).** Juno/JIRAM observations of
  Loki Patera: crust brightness temperatures 270–355 K, the independent corroboration of
  the geologic-area denominator. §6.4.
- **Keszthelyi, L. et al. (2007)**: *Icarus* 192, 491. **No arXiv**
  ([`2007Icar..192..491K`](https://ui.adsabs.harvard.edu/abs/2007Icar..192..491K)). Io's eruption temperature revised to ~1340 °C
  (1613 K), which sets the 384 kW/m² bare-melt ceiling. §6.4.
- **de Pater, I. et al. (2016)**: *Icarus* 264, 198. **No arXiv**
  ([`2016Icar..264..198D`](https://ui.adsabs.harvard.edu/abs/2016Icar..264..198D)). Time evolution of Pele and Pillan; Pele's
  fitted-area flux of 44.3 kW/m² at 940 K is the fitted-denominator anchor. §6.4.
- **Campion, R. & Coppola, D. (2023)**: *Front. Earth Sci.* 11, 1140199. **No arXiv**
  ([`2023FrEaS..1140199C`](https://ui.adsabs.harvard.edu/abs/2023FrEaS..1140199C)). The lava-lake compilation whose Table 1 supplies
  the measured capacity band and its 111 kW/m² maximum. §6.4.
- **Rovira-Navarro, M. et al. (2021)**: *Planet. Sci. J.* 2, 119. **No arXiv**
  ([`2021PSJ.....2..119R`](https://ui.adsabs.harvard.edu/abs/2021PSJ.....2..119R)). "Tidally Heated Exomoons around Gas Giants":
  the super-Io envelope, 1–3 dex above Io, with heat piping through a thick lid as the
  sustainable branch. Adopted by Kleisioti+ 2023 ([arXiv:2305.03410](https://arxiv.org/abs/2305.03410)),
  the ε Eridani b exomoon observability study. §6.5.

**Topics with no single canonical paper:** the surface-flux → "ocean vs dead"
*thresholds* in §6.1 are a synthesis of the Enceladus/Europa and Io literature above,
not a single citable threshold paper, treated as order-of-magnitude guides, not a
derived law. The same applies to the §6.2 mode boundaries, which compare published
*capacities* rather than quoting a published threshold (§8).

---

## Related

- [`ice-stability-methodology.md`](ice-stability-methodology.md) — an icy surface on a
  strongly heated body is a contradiction; that recipe's budget is external-only, so the
  internal flux derived here must be added before judging ice survival.
- [`crater-degradation-methodology.md`](crater-degradation-methodology.md) — consumes
  this doc's heat flux twice: as the volcanic burial rate and as the crater
  viscous-relaxation switch.
- [`moon-energy-budget-methodology.md`](moon-energy-budget-methodology.md) — the satellite
  counterpart: for a moon, replace this doc's Layer 1 `T_eq` with its four-term budget
  (eclipses, parent thermal + reflected, tidal heating).
- [tidally-locked-temperature-methodology](tidally-locked-temperature-methodology.md): sibling recipe for the
  surface/equilibrium temperature of synchronous bodies; tidal heating here is an
  *additional* internal heat source layered on top of the irradiation that doc treats.
- [exoplanet-atmosphere-methodology](exoplanet-atmosphere-methodology.md): for the gate-then-document
  framing and the "principled choice within bounds" honesty convention mirrored here.
- [planetary-dynamo-scaling](planetary-dynamo-scaling.md): the gold-standard sibling
  scaling-law doc (law + calibration table + domain-of-validity + worked examples)
  this doc is modelled on; note Driscoll & Barnes 2015 links tidal heating to the
  magnetic evolution that doc derives.
- **Tidal *locking* / despin-timescale methodology**: a **planned future sibling
  doc**. Locking (does the body rotate synchronously?) is a *separate* question from
  heating (how much power is dissipated). This doc assumes synchronous rotation; do
  not conflate the two.
- [methodology-index](methodology-index.md) — the index of all derived-value methodology recipes.
