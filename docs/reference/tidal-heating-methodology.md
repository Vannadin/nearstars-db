<!-- 궤도·내부물성에서 조석가열 출력(Ė)을 도출하고 화산·지하해·플룸 가능성을 판정하는 방법론 레퍼런스 -->
# Tidal-Heating Methodology — Internal Power, Volcanism & Subsurface Oceans

Method reference for deriving the **internal tidal-heating power** `Ė` of a
synchronously rotating body — a moon around a planet, or a planet around its star —
from its orbit and interior, and for deciding whether that heat can sustain
volcanism, a subsurface ocean, or plumes. Same spirit as the
[dynamo-scaling doc](planetary-dynamo-scaling.md): cite the relation + a calibration
that reproduces known bodies, not a fabricated measurement.

This is the **single most repeated derived value in NearStars Phase 4** (it was
recomputed four separate times in one α Cen session, for the moons Dante, Hades,
Pandora and Chaos), so it gets a canonical grounded recipe here.

> Citations resolved against NASA ADS (the registered `ADS_API_TOKEN`), not ad-hoc
> web search; arXiv id where one exists, otherwise the authoritative ADS bibcode
> (flagged "no arXiv"). See §9 for the verified list.
> This is a working reference, not a textbook.

**Scope note:** this doc is about tidal *heating* (the dissipated power). The related
question of tidal *locking* — the despin timescale that decides whether a body is
synchronous in the first place — is a **planned separate sibling doc**; do not
conflate the two. The recipe below *assumes* synchronous rotation (the usual state
for the close-in bodies where heating matters); a non-synchronous body needs the
locking treatment first.

## Table of Contents

1. [The law — the fixed-Q tidal-heating formula](#1-the-law--the-fixed-q-tidal-heating-formula)
2. [Calibration — the formula reproduces Io and Enceladus](#2-calibration--the-formula-reproduces-io-and-enceladus)
3. [The a⁻⁷·⁵ distance gate (the hard lesson)](#3-the-a⁷·⁵-distance-gate-the-hard-lesson)
4. [The eccentricity-maintenance requirement](#4-the-eccentricity-maintenance-requirement)
5. [Domain of validity — k₂/Q by body class, and the rheology problem](#5-domain-of-validity--kq-by-body-class-and-the-rheology-problem)
6. [Deciding the outcome — volcanism / ocean / plumes](#6-deciding-the-outcome--volcanism--ocean--plumes)
7. [Worked examples](#7-worked-examples)
8. [Honesty & uncertainty](#8-honesty--uncertainty)
9. [Annotated Bibliography](#9-annotated-bibliography)
10. [Related](#related)

---

## 1. The law — the fixed-Q tidal-heating formula

Peale, Cassen & Reynolds 1979 (*Science* 203, 892, `1979Sci...203..892P`) predicted
— famously days before Voyager imaged the eruptions — that Io would be melted by
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
| `G` | gravitational constant | — |
| `M_p` | mass of the **perturber** (the planet, for a moon; the star, for a planet) | DB |
| `R` | radius of the **heated** body | DB |
| `n` | mean motion = `2π/P_orb` = `√(G M_p / a³)` | orbit |
| `e` | orbital eccentricity | orbit (must be *maintained* — §4) |
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

## 2. Calibration — the formula reproduces Io and Enceladus

The formula is only trustworthy because it reproduces the two bodies whose internal
output is actually *measured*. These observed numbers calibrate `k₂/Q`.

| Body | Perturber | a (R_p) | e (forced) | observed Ė | observed flux | formula reproduces with |
|---|---|---|---|---|---|---|
| **Io** | Jupiter | ~5.9 R_J | ~0.0041 | ~0.6–1.6 ×10¹⁴ W | ~2 W/m² (global) | k₂/Q ~ 0.015 (k₂≈0.3, Q≈20) |
| **Enceladus** | Saturn | ~3.95 R_Sat | ~0.0047 | ~5–16 GW (≈10¹⁰ W) | ~5 GW from the SPT | k₂/Q ~ 0.002–0.01 (soft ice + ocean) |

- **Io** — the calibration anchor. Infrared radiometry (Veeder+ 1994
  `1994JGR....9917095V`; Veeder+ 2012 `2012Icar..219..701V`) puts the global heat
  output at ~10¹⁴ W, i.e. a surface flux ~2 W/m² — an order of magnitude above
  Earth's ~0.08 W/m². Lainey+ 2009 (`2009Natur.459..957L`) confirmed *active*
  strong dissipation in the Io–Jupiter system from astrometry, closing the loop:
  the dissipation the formula needs is the dissipation the orbit shows. With Io's
  `a`, `e`, `R`, `M_J` and `k₂/Q ≈ 0.015`, the formula returns ~10¹⁴ W. ✓
- **Enceladus** — the low-mass-body anchor. Cassini found an active south-polar
  thermal anomaly and plumes (Spencer+ 2006 `2006Sci...311.1401S`); Howett+ 2011
  (`2011JGRE..116.3003H`) measured ~15.8 GW from the south-polar terrain, and the
  endogenic total is several GW (~10¹⁰ W). Nimmo+ 2007 (`2007Natur.447..289N`)
  attributes the plumes to shear heating along the tiger stripes. Enceladus is tiny
  (`R ≈ 252 km`) so its `R⁵` is ~10⁹× smaller than Io's; the formula returns the
  ~GW scale with a soft-ice + ocean `k₂/Q` (Meyer & Wisdom 2007 `2007Icar..188..535M`).
  ✓

The calibration spans **four orders of magnitude in Ė** (10¹⁴ → 10¹⁰ W) and a
factor ~25 in radius, and the same single formula covers both. That is the evidence
that the order-of-magnitude recipe is sound — *provided* `k₂/Q` is chosen for the
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
heating collapses to **MW-level** — utterly negligible for melting ice or driving
plumes (Enceladus, by contrast, sits at only ~4 R_Sat — *close in* — which is why a
252 km moon still musters GW).

**The NearStars Chaos lesson.** In the α Cen Phase-4 work, the moon **Chaos** at
~20 planetary radii was shown by exactly this calculation to receive only
**~MW-level** tidal power — *orders of magnitude too little* to sustain a subsurface
ocean or cryovolcanic plumes. The favourable narrative (resonance, soft interior)
could not lift it past the `a⁻⁷·⁵` gate. So Chaos's plumes were accepted as an
**art-first documented divergence** on the Phase-4 board — explicitly *not* a
physically derived feature. By contrast a moon placed close-in (a few R_p) clears
the gate and its heating *is* derivable.

The gate is a one-line sanity check before any detailed estimate: **compute `a` in
perturber radii.** Beyond ~10–15 R_p, expect heating to be negligible for anything
short of a giant, eccentric, resonance-pumped body — and if the design wants a
feature there anyway, flag it as a documented divergence, not a derivation.

---

## 4. The eccentricity-maintenance requirement

Tidal heating runs on `e²`. But tidal dissipation **damps `e`**: the same friction
that heats the body circularizes its orbit, on a timescale that can be far shorter
than the system's age. A body left alone therefore heats *transiently*, then `e → 0`
and the heating **shuts off**. Sustained heating requires something to keep pumping
`e`.

The pump is almost always a **mean-motion resonance** with another body:

- **Io** — the Laplace resonance (Io:Europa:Ganymede 1:2:4). Yoder 1979
  (`1979Natur.279..767Y`) showed how tidal heating in Io *drives and locks* this
  resonance, which in turn forces Io's `e ≈ 0.0041` against damping. Without it Io's
  orbit would circularize and the volcanism would die.
- **Enceladus** — the 2:1 mean-motion resonance with Dione forces `e ≈ 0.0047`
  (Meyer & Wisdom 2007 `2007Icar..188..535M`; Meyer & Wisdom 2008
  `2008Icar..193..213M`). The resonance is what makes a tiny moon geologically alive.

Practical rule: **if you are claiming sustained tidal heating, name the resonance
(or other forcing) that maintains `e`.** A single moon with a measured/assumed `e`
but no maintaining mechanism may simply be in the middle of circularizing — its
`e` (and thus its heating) is a snapshot, not a steady state. For NearStars
synthetic systems, a multi-moon resonant chain (Laplace-like) is the physically
honest way to justify a moon that needs to *stay* hot; a lone eccentric moon should
be flagged as transient unless its circularization time exceeds the system age.

---

## 5. Domain of validity — k₂/Q by body class, and the rheology problem

`k₂/Q` is the **dominant uncertainty** — it spans ~3 orders of magnitude across body
types and is rarely measured for the body in hand. Pick it by class:

| Class | k₂ | Q | k₂/Q | notes |
|---|---|---|---|---|
| **Rocky / silicate** (Io-like, terrestrial) | ~0.1–0.3 | ~10–100 | ~10⁻³–10⁻² | strongly T-dependent; a partially molten interior raises k₂ and lowers Q (more dissipation) |
| **Icy + subsurface ocean** (Enceladus, Europa) | ~0.01–0.1 | ~1–100 | ~10⁻⁴–10⁻² | an ocean decouples the shell and can *raise* dissipation enormously; very model-dependent |
| **Gas / ice giant** | ~0.1–0.6 | ~10³–10⁵ | ~10⁻⁵–10⁻³ | high Q (low dissipation per cycle); relevant when the *giant itself* is the heated body close to a star |

Four regimes / cautions decide whether the fixed-Q recipe is even the right tool:

1. **Rocky synchronous body, small e** — the recipe's home turf (Peale+ 1979;
   calibrated on Io). Use the rocky `k₂/Q` band and report an order of magnitude.
2. **Icy body with an ocean** — the fixed-Q number is a *floor*; an ocean-decoupled
   shell can dissipate far more than a homogeneous-Q estimate, so a low fixed-Q
   `Ė` does **not** rule out an active ocean. Cross-check against a viscoelastic
   model before declaring a moon dead.
3. **Viscoelastic / rheological regime** — when `Ė` from §1 is near a melting or
   ocean threshold, the fixed-Q answer is unreliable and must be replaced by a
   frequency- and temperature-dependent **Maxwell / Andrade** treatment: Segatz+
   1988 (`1988Icar...75..187S`, the founding viscoelastic-Io model), Henning,
   O'Connell & Sasselov 2009 (`2009ApJ...707.1000H`, tidally heated terrestrial
   exoplanets), Henning & Hurford 2014 (`2014ApJ...789...30H`, multilayered),
   Renaud & Henning 2018 (`2018ApJ...857...98R`, Andrade vs Maxwell — heating can
   differ by **large factors**, often >10×, and peaks at a resonant interior
   temperature). The fixed-Q and Andrade answers can disagree by an order of
   magnitude; that gap *is* the error bar.
4. **Spin-orbit / non-synchronous, or near a spin-orbit resonance** — the `(21/2)e²`
   leading term is wrong; use the Efroimsky & Makarov frequency-dependent formalism
   (Efroimsky & Williams 2012 `2012CeMDA.112..283E`). Mostly relevant to bodies
   *not* yet locked — i.e. the locking-doc territory flagged at the top.

For NearStars, the practical posture: use the fixed-Q formula with a class-`k₂/Q`
band, report the **range** (not a point), and where the answer lands near a
volcanism/ocean threshold, defer to the viscoelastic literature and widen the
uncertainty rather than over-claim.

---

## 6. Deciding the outcome — volcanism / ocean / plumes

Convert `Ė` to a **surface heat flux** `F = Ė / (4πR²)` and compare to thresholds
(these are guides, not sharp lines):

| Surface flux F | regime | analog |
|---|---|---|
| ≳ 1 W/m² | vigorous silicate volcanism, possible magma ocean | Io (~2 W/m²) |
| ~0.1–1 W/m² | active resurfacing, episodic volcanism | active icy/rocky worlds |
| ~0.01–0.1 W/m² | enough to maintain a subsurface ocean under an ice shell | Enceladus SPT, Europa |
| ≲ 10⁻³ W/m² | geologically dead; no ocean, no plumes from tides alone | far/airless moons |

The chain: **(1)** compute `a` in R_p — apply the §3 gate first (if `a ≳ 10–15 R_p`
and the body is small, the answer is almost certainly "dead", stop). **(2)** confirm
`e` is *maintained* (§4) — name the resonance, or flag the heating as transient.
**(3)** pick a class `k₂/Q` band (§5) and compute `Ė` and `F` as a range. **(4)**
map `F` to the table; if it lands near a threshold, escalate to a viscoelastic
cross-check (§5 regime 3) before committing. **(5)** record the chosen `k₂/Q`, the
maintaining resonance, and the resulting `F`-range on the Phase-4 board — and where
art overrides a "dead" verdict, mark it a **documented divergence**, never a silent
upgrade.

Note that tidal heating is one heat source among several (radiogenic, accretional,
primordial). For an Earth-mass body radiogenic heating alone is ~0.08 W/m²; tidal
heating matters when it *exceeds* that. For small icy moons radiogenic heat is
negligible and tides are essentially the only knob — which is why the distance gate
is so decisive for them.

---

## 7. Worked examples

**Io (the calibration).** `M_p = M_Jupiter`, `R = 1822 km`, `a = 421,700 km`
(~5.9 R_J), `e = 0.0041` (Laplace-maintained), rocky `k₂/Q ≈ 0.015`. The fixed-Q
formula returns `Ė ~ 10¹⁴ W`, `F ~ 2 W/m²` — matching Veeder+ 2012. Verdict:
vigorous silicate volcanism, **derived** (resonance named, flux measured). This is
the anchor every other estimate is scaled against.

**Enceladus (the small-body calibration).** `M_p = M_Saturn`, `R = 252 km`,
`a ≈ 238,000 km` (~3.95 R_Sat — *close in*), `e = 0.0047` (Dione 2:1), soft-ice +
ocean `k₂/Q ~ 10⁻³`. Despite `R⁵` being ~10⁹× smaller than Io's, the small `a` keeps
it inside the gate and the formula returns the observed ~GW / ~10⁻² W/m² over the
south-polar terrain. Verdict: subsurface ocean + plumes, **derived**. The lesson:
*close-in beats big* — a tiny moon at 4 R_p outperforms a large one at 20 R_p.

**α Cen application — close vs far (the project case).** Treat the α Cen Phase-4
moons qualitatively (board values, not reproduced here):
- A moon placed **close-in (a few R_p)**, in a resonant chain that maintains `e`,
  clears the §3 gate. Its `Ė` is in the GW–TW range depending on `R` and `k₂/Q`,
  enough for an active ocean or volcanism — a **derived** feature with the resonance
  named on the board.
- **Chaos at ~20 R_p** fails the gate: the `a⁻⁷·⁵` collapse drops `Ė` to
  **~MW-level**, ~5×10⁻⁴ of the close-in case, far below any ocean/plume threshold.
  Its cryovolcanic plumes are therefore an **art-first documented divergence** on the
  Phase-4 board — recorded as a deliberate choice that overrides the physics, not a
  value the recipe produced. This is the canonical example of §8's honesty rule.

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
  feature the gate forbids (Chaos), that is a **documented divergence** — flagged on
  the board as art overriding physics, never dressed up as a derivation. The method's
  value is precisely that it tells you honestly when a feature is *not* physically
  supported, so the override is an explicit, recorded choice.

The method is grounded and calibrated (it reproduces Io and Enceladus across 4 dex
in `Ė`); the *inputs* (`k₂/Q`, the rheology, the maintenance of `e`) carry the
uncertainty. Confidence is **order-of-magnitude**, and that is enough to make the
volcanism/ocean/plume call correctly in nearly every case — because the `a⁻⁷·⁵`
distance term usually decides the answer long before `k₂/Q` matters.

---

## 9. Annotated Bibliography

Each entry: authors, year, journal, **verified** arXiv id (or "no arXiv" + bibcode),
ADS citation count, and one line on the contribution.

- **Peale, S. J., Cassen, P. & Reynolds, R. T. (1979)** — *Science* 203, 892.
  **No arXiv** (`1979Sci...203..892P`). Cites: 530. The founding tidal-heating
  paper: the fixed-Q formula and the pre-Voyager prediction that Io would be melted.
  §1.
- **Yoder, C. F. (1979)** — *Nature* 279, 767. **No arXiv** (`1979Natur.279..767Y`).
  Cites: 178. How tidal heating in Io drives and locks the Galilean (Laplace)
  resonance that maintains Io's eccentricity. §4.
- **Segatz, M. et al. (1988)** — *Icarus* 75, 187. **No arXiv**
  (`1988Icar...75..187S`). Cites: 258. Founding viscoelastic (Maxwell) Io model —
  tidal dissipation, surface heat flow and figure beyond fixed-Q. §5.
- **Veeder, G. J. et al. (1994)** — *JGR* 99, 17095. **No arXiv**
  (`1994JGR....9917095V`). Cites: 217. Io's global heat flow from infrared
  radiometry (~10¹⁴ W) — the Io calibration. §2.
- **Spencer, J. R. et al. (2006)** — *Science* 311, 1401. **No arXiv**
  (`2006Sci...311.1401S`). Cites: 518. Cassini's discovery of Enceladus's active
  south-polar thermal anomaly and plumes. §2.
- **Meyer, J. & Wisdom, J. (2007)** — *Icarus* 188, 535. **No arXiv**
  (`2007Icar..188..535M`). Cites: 152. Tidal heating in Enceladus and the
  Enceladus–Dione 2:1 resonance maintaining its eccentricity. §2, §4.
- **Nimmo, F. et al. (2007)** — *Nature* 447, 289. **No arXiv**
  (`2007Natur.447..289N`). Cites: 239. Shear heating along the tiger stripes as the
  origin of Enceladus's plumes and heat flux. §2.
- **Jackson, B., Barnes, R. & Greenberg, R. (2008)** — *ApJ* 681, 1631.
  **arXiv:0803.0026.** Cites: 155. "Tidal Heating of Extrasolar Planets" — applies
  the fixed-Q heating formula to close-in exoplanets and its surface-condition
  magnitude. §1, §3. (Companion: Jackson+ 2008 *ApJ* 678, 1396, **arXiv:0802.1543**,
  cites 382, the tidal-evolution / eccentricity-damping side.)
- **Lainey, V. et al. (2009)** — *Nature* 459, 957. **No arXiv**
  (`2009Natur.459..957L`). Cites: 359. Astrometric detection of *active* strong tidal
  dissipation in the Io–Jupiter system — empirically closes the heating loop. §2.
- **Henning, W. G., O'Connell, R. J. & Sasselov, D. D. (2009)** — *ApJ* 707, 1000.
  **arXiv:0912.1907.** Cites: 158. Tidally heated terrestrial exoplanets with a
  viscoelastic response model — the exoplanet-rheology bridge. §5.
- **Howett, C. J. A. et al. (2011)** — *JGR Planets* 116, E03003. **No arXiv**
  (`2011JGRE..116.3003H`). Cites: 136. ~15.8 GW measured from Enceladus's south-polar
  region — the Enceladus calibration number. §2.
- **Veeder, G. J. et al. (2012)** — *Icarus* 219, 701. **No arXiv**
  (`2012Icar..219..701V`). Cites: 92. Io's volcanic thermal sources and global heat
  flow — the updated ~10¹⁴ W census. §2.
- **Efroimsky, M. & Williams, J. G. (2012)** — *Celest. Mech. Dyn. Astron.* 112, 283.
  **arXiv:1105.6086.** Cites: 128. Bodily tides near spin-orbit resonances — the
  frequency-dependent formalism beyond fixed-Q for non-synchronous bodies. §5.
- **Barnes, R. et al. (2013)** — *Astrobiology* 13, 225. **arXiv:1203.5104.** Cites:
  120. "Tidal Venuses": tidal heating can trigger a runaway greenhouse, the upper
  habitability bound on tidal heat. §6 context.
- **Heller, R. & Barnes, R. (2013)** — *Astrobiology* 13, 18. **arXiv:1209.5323.**
  Cites: 129. Exomoon habitability constrained by illumination *and* tidal heating —
  the moon-specific habitability bound directly relevant to NearStars moons. §6.
- **Henning, W. G. & Hurford, T. (2014)** — *ApJ* 789, 30. **No arXiv**
  (`2014ApJ...789...30H`). Cites: 55. Tidal heating in multilayered terrestrial
  exoplanets — layered viscoelastic structure. §5.
- **Driscoll, P. E. & Barnes, R. (2015)** — *Astrobiology* 15, 739.
  **arXiv:1509.07452.** Cites: 108. Tidal heating of Earth-like planets around M
  stars and its coupling to thermal/magnetic evolution and habitability. §6.
- **Renaud, J. P. & Henning, W. G. (2018)** — *ApJ* 857, 98. **arXiv:1707.06701.**
  Cites: 82. Increased tidal dissipation using advanced (Andrade) rheology — shows
  fixed-Q and Andrade can differ by large factors. §5, §8.

**Topics with no single canonical paper:** the surface-flux → "ocean vs dead"
*thresholds* in §6 are a synthesis of the Enceladus/Europa and Io literature above,
not a single citable threshold paper — treated as order-of-magnitude guides, not a
derived law.

---

## Related

- `docs/reference/tidally-locked-temperature-methodology.md` — sibling recipe for the
  surface/equilibrium temperature of synchronous bodies; tidal heating here is an
  *additional* internal heat source layered on top of the irradiation that doc treats.
- `docs/reference/exoplanet-atmosphere-methodology.md` — for the gate-then-document
  framing and the "principled choice within bounds" honesty convention mirrored here.
- `docs/reference/planetary-dynamo-scaling.md` — the gold-standard sibling
  scaling-law doc (law + calibration table + domain-of-validity + worked examples)
  this doc is modelled on; note Driscoll & Barnes 2015 links tidal heating to the
  magnetic evolution that doc derives.
- **Tidal *locking* / despin-timescale methodology** — a **planned future sibling
  doc**. Locking (does the body rotate synchronously?) is a *separate* question from
  heating (how much power is dissipated). This doc assumes synchronous rotation; do
  not conflate the two.
