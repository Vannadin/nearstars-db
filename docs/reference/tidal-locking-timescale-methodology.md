<!-- 조석고정(despin) 타임스케일로 동기자전 여부와 자전 상태(1:1·3:2·유사동기)를 판정하는 방법론 레퍼런스 -->
# Tidal-Locking Methodology — Despin Timescale, Rotation State & the Thermal-Tide Exception

Method reference for deciding **whether a body is tidally locked, and into which
rotation state**, by comparing its tidal-synchronization (despin) timescale `τ_lock`
to the system age. Same "cite the relation + a calibration that reproduces known
bodies, not a fabricated measurement" spirit as the
[tidal-heating doc](tidal-heating-methodology.md) and the
[dynamo-scaling doc](planetary-dynamo-scaling.md).

This is the doc the heating and temperature siblings flagged as a needed prerequisite:
both *assume* the close-in body rotates synchronously. This doc is what **justifies**
that assumption — and, where the assumption fails, says into what state the body
locks instead (a higher spin–orbit resonance, pseudo-synchronous, or an atmosphere-
driven asynchronous state).

> Citations resolved against NASA ADS (the registered `ADS_API_TOKEN`), not ad-hoc
> web search; arXiv id where one exists, otherwise the authoritative ADS bibcode
> (flagged "no arXiv"). See §8 for the verified list.
> This is a working reference, not a textbook.

**Scope note:** this doc decides *whether* and *into what state* a body is locked — it
**underwrites the synchronous assumption** the
[temperature doc](tidally-locked-temperature-methodology.md) (substellar-point
geometry) and the [tidal-heating doc](tidal-heating-methodology.md) (the `(21/2)e²`
synchronous form) both make. It is **not** the heating: the heating doc gives the
dissipated power `Ė`, this doc gives the spin evolution. The two share the **same
`Q/k₂` interior unknown** — and, helpfully, the same lesson that a steep power of
orbital distance usually makes the call robust *despite* that unknown (here `a⁶`,
there `a⁻⁷·⁵`).

## Table of Contents

1. [The timescale — the despin (synchronization) formula](#1-the-timescale--the-despin-synchronization-formula)
2. [Calibration — the formula reproduces the locked Solar-System bodies](#2-calibration--the-formula-reproduces-the-locked-solar-system-bodies)
3. [The a⁶ distance gate (the dominant term)](#3-the-a-distance-gate-the-dominant-term)
4. [Rotation-state taxonomy — 1:1, p:q resonance, pseudo-synchronous](#4-rotation-state-taxonomy--11-pq-resonance-pseudo-synchronous)
5. [The atmospheric thermal-tide exception](#5-the-atmospheric-thermal-tide-exception)
6. [Domain of validity & honesty — Q/k₂ and initial spin](#6-domain-of-validity--honesty--qk-and-initial-spin)
7. [Worked examples](#7-worked-examples)
8. [Annotated Bibliography](#8-annotated-bibliography)
9. [Related](#related)

---

## 1. The timescale — the despin (synchronization) formula

A body that starts with some primordial spin `ω₀` feels a tidal torque from its
perturber (the star, for a planet; the planet, for a moon). The raised bulge lags by
a small angle set by internal friction, and that lagging bulge applies a torque that
drives the spin toward the orbital mean motion `n`. The **despin (synchronization)
timescale** is the time for that torque to remove the excess spin angular momentum.
For a homogeneous body of moment of inertia `I = α m R²` the constant-phase-lag
("fixed-Q") result — as derived in Goldreich & Soter 1966 (`1966Icar....5..375G`)
and laid out textbook-form in Murray & Dermott 1999, *Solar System Dynamics*
(`1999ssd..book.....M`), §5 — is

    τ_lock  ≈  (ω₀ − n) · (Q / k₂) · (I a⁶) / (3 G M_p² R⁵)

Dropping the (order-unity) spin excess and writing `I = α m R²`, the practical scaling is

    τ_lock  ∝  (Q / k₂) · ω₀ · a⁶ · I / (G M_p² R⁵)
            ∝  (Q / k₂) · ω₀ · α · (m / R³) · a⁶ / (G M_p²)

Every term:

| Symbol | Meaning | Where it comes from |
|---|---|---|
| `Q` | tidal quality factor (1/Q ≈ phase lag = fraction of energy lost per cycle) | rheology (§6) |
| `k₂` | degree-2 tidal Love number (potential response of the body) | interior structure (§6) |
| `ω₀` | initial (primordial) spin rate of the **locking** body | unknown; order-of-magnitude (§6) |
| `n` | orbital mean motion = `2π/P_orb` = `√(G M_p / a³)` — the target spin | orbit |
| `I = α m R²` | moment of inertia of the locking body (`α ≈ 0.33–0.4` for differentiated rock) | interior |
| `m`, `R` | mass and radius of the **locking** body | DB / [mass-radius doc](mass-radius-relation-methodology.md) |
| `M_p` | mass of the **perturber** (the star, for a planet; the planet, for a moon) | DB |
| `a` | semi-major axis of the locking body's orbit about the perturber | orbit |
| `G` | gravitational constant | — |

Note the **inversion of roles relative to the heating doc**: there, `R⁵` and `M_p²`
sit in the numerator (a big perturber and a big body dissipate more power); here the
same factors sit in the *denominator* (a stronger raising torque despins *faster*, so
shorter `τ_lock`). It is the same tidal physics read for spin rather than heat. The
grouping `Q/k₂` (note: **inverted** relative to the heating formula's `k₂/Q`) is what
the body's material contributes; everything else is geometry, the perturber's mass,
and the unknown initial spin.

The decision rule is a single comparison:

> Compute `τ_lock`; compare to the **system age** `t_sys`.
> **`τ_lock ≪ t_sys` → locked** (assume synchronous unless §5 applies).
> **`τ_lock ≳ t_sys` → not necessarily locked** — keep the measured/primordial spin.

The fixed-Q form is a *first-order* tool: `Q` and `k₂` are treated as constant
numbers, and `ω₀` is unknown. §6 covers when that matters — and why it usually does
not change the lock/no-lock verdict.

---

## 2. Calibration — the formula reproduces the locked Solar-System bodies

The formula is trustworthy because, with sensible class `Q/k₂`, it reproduces which
Solar-System bodies *are* locked and which are not — the same logic the heating doc
uses to calibrate on Io and Enceladus.

| Body | Perturber | a | class Q/k₂ | τ_lock (order) | t_sys | observed state | match |
|---|---|---|---|---|---|---|---|
| **Moon** | Earth | 3.84×10⁵ km | rocky ~10²–10³ | ~10⁷–10⁸ yr | 4.5 Gyr | 1:1 synchronous | ✓ locked |
| **Mercury** | Sun | 0.39 AU | rocky ~10²–10³ | ~few ×10⁸–10⁹ yr | 4.5 Gyr | **3:2** (not 1:1!) | ✓ despun, §4 |
| **Galilean moons** | Jupiter | 6–26 R_J | icy/rocky | ≪ Gyr (close in) | 4.5 Gyr | all 1:1 | ✓ locked |
| **Venus** | Sun | 0.72 AU | rocky + atmosphere | ~10⁹ yr (gravitational) | 4.5 Gyr | **slow retrograde** | ✗ thermal tide, §5 |

- **The Moon** — the canonical 1:1 lock. With Earth as perturber at 3.84×10⁵ km and a
  rocky `Q/k₂`, `τ_lock` comes out far below a Gyr; the Moon was despun to synchronous
  rotation early in Solar-System history and shows us one face ever since. This is the
  textbook anchor (Murray & Dermott 1999 §5; Peale 1977, `1977plsa.conf...87P`,
  "Rotation Histories of the Natural Satellites"). ✓
- **Mercury** — despun (its primordial fast spin is long gone, so `τ_lock ≪ t_sys`),
  but it locked into a **3:2 spin–orbit resonance**, not 1:1, because of its
  eccentricity plus a permanent quadrupole moment (Goldreich & Peale 1966,
  `1966AJ.....71..425G`; capture explained by Correia & Laskar 2004,
  `2004Natur.429..848C`). The "despin happened" call is right; "1:1" would be wrong.
  This is the §4 example. ✓ for despin, ✗ for naively assuming 1:1.
- **Venus** — `τ_lock` for the *gravitational* tide alone is ≲ system age, so a
  naive application says "should be near-synchronous." Instead Venus rotates **slowly
  retrograde**. The resolution is the atmospheric **thermal tide** (Gold & Soter 1969,
  `1969Icar...11..356G`; Dobrovolskis & Ingersoll 1980, `1980Icar...41....1D`): a thick
  atmosphere's thermally-driven bulge applies a torque that opposes the gravitational
  one and parks the spin away from 1:1. This is the §5 exception. ✗ for the bare formula.

The calibration message: the despin *timescale* correctly tells you Mercury, the Moon
and the Galilean moons all despun within the age — the formula gets the **yes/no**
right across bodies spanning planet/moon and rock/ice. What it does *not* tell you by
itself is the final **state** (Mercury's 3:2) or the **atmospheric override** (Venus).
Those need §4 and §5.

---

## 3. The a⁶ distance gate (the dominant term)

**This is the section to read if you read only one** — it is the mirror of the heating
doc's `a⁻⁷·⁵` gate. Because `τ_lock ∝ a⁶`, the orbital distance dominates every other
knob. A factor-2 in distance changes the locking time by `2⁶ = 64×`.

Hold a rocky body's `Q/k₂`, `ω₀`, `m`, `R`, and the perturber's mass fixed, and move
it out:

| relative a | relative τ_lock | implication |
|---|---|---|
| 0.5× | ~1/64 | locks ~60× faster — essentially instant if it was marginal |
| 1× | 1 | reference |
| 2× | ~64× | a marginal case becomes "may never lock within the age" |
| 4× | ~4000× | almost certainly never locks (Earth-like → Gyr ≫ age) |

The consequence for the two regimes NearStars cares about:

- **Close-in (M-dwarf HZ planets; moons a few R_p from their planet).** The habitable
  zone of an M dwarf sits at ~0.02–0.2 AU, and a moon orbits its planet at a few
  planetary radii. The `a⁶` term makes `τ_lock` plunge to **≪ Gyr** — far below any
  realistic system age. **These bodies are locked.** This is *exactly* why the
  temperature and heating docs are entitled to assume synchronous rotation for them
  (Kasting, Whitmire & Reynolds 1993, `1993Icar..101..108K`, note locking in the M-dwarf
  HZ; Barnes 2017, `2017CeMDA.129..509B`, gives the magnitudes — see §7).
- **Far out (Earth at 1 AU around a Sun-like star; a distant moon).** The same `a⁶`
  blows `τ_lock` up to ≫ age. **These bodies are not locked** and keep their primordial
  spin. Earth at 1 AU has `τ_lock ≫ 4.5 Gyr` — which is why Earth is not tidally locked
  to the Sun.

**Robustness:** the lock/no-lock verdict is usually secure *despite* the order-of-
magnitude uncertainty in `Q/k₂` and `ω₀` (§6), because `a⁶` dominates. A close-in
M-dwarf HZ planet locks in 10⁶–10⁸ yr; even a ×100 swing in `Q/k₂` leaves it ≪ Gyr.
The gate is a one-line sanity check before any detailed estimate: **plug `a` into the
formula and compare powers of ten to the age.** Only bodies sitting *near* the
`τ_lock ≈ t_sys` boundary (a few ×0.1 AU around a K/M star, intermediate cases) require
care with `Q/k₂`; the deep-inside and far-outside cases are robust.

---

## 4. Rotation-state taxonomy — 1:1, p:q resonance, pseudo-synchronous

"Locked" is not synonymous with "1:1." Once `τ_lock ≪ t_sys` establishes that the body
*has* despun, the **eccentricity** decides the final state. Record which one — it
matters because the temperature doc's substellar-point geometry assumes a *fixed*
substellar point, which only the 1:1 state provides.

**(a) Circular orbit (e ≈ 0) → 1:1 synchronous.** The equilibrium spin equals the mean
motion; one face permanently toward the perturber, a fixed substellar point. This is
the default for tidally-circularized close-in bodies and the state the sibling docs
assume. *(Moon; Galilean moons; most M-dwarf HZ planets on near-circular orbits.)*

**(b) Significant eccentricity → pseudo-synchronous (super-synchronous).** For a body
with a smooth (no strong permanent quadrupole) response on an eccentric orbit, the
equilibrium is **not** `ω = n`. Tidal torque is strongest near periapse, where the
body moves fastest, so the equilibrium spin settles *above* the mean motion. Hut 1981
(`1981A&A....99..126H`) gives the equilibrium spin rate of the equilibrium-tide model:

    ω_eq / n  =  (1 + (15/2)e² + (45/8)e⁴ + (5/16)e⁶) / [(1 + 3e² + (3/8)e⁴)(1 − e²)^{3/2}]

which reduces to `ω_eq/n ≈ 1 + 6e²` for small `e` — slightly faster than synchronous,
so the substellar point **drifts** rather than staying fixed. Dobrovolskis 2007
(`2007Icar..192....1D`) works the climate consequences of these eccentric spin states.
*This is the state to assign an eccentric NearStars body whose interior is fluid-like
and has no large permanent figure.*

**(c) Eccentricity + permanent quadrupole → higher p:q spin–orbit resonance.** A rocky
body with a frozen-in permanent quadrupole (a non-axisymmetric figure) can be **captured
into a p:q resonance** where it rotates `p` times per `q` orbits — Mercury's **3:2** is
the type case (Goldreich & Peale 1966, `1966AJ.....71..425G`). Capture is *probabilistic*
and depends on eccentricity and the tidal model: Correia & Laskar 2004
(`2004Natur.429..848C`) showed Mercury's chaotic orbital evolution makes 3:2 the most
likely outcome; Makarov 2012 (`2012ApJ...752...73M`) and Noyelles et al. 2014
(`2014Icar..241...26N`) give capture probabilities and show that with a realistic
(frequency-dependent) tidal model 3:2 capture is essentially certain for Mercury's `e`.
A body in 3:2 has a **slowly moving substellar point** (two "hot longitudes" over an
orbit), so the temperature doc's fixed-substellar geometry does **not** apply directly.

Practical rule for NearStars: **record `e` for every locked body and pick the state.**
Near-circular → 1:1 (sibling docs valid as-is). Eccentric, fluid → pseudo-synchronous
(Hut). Eccentric, rocky with a likely permanent figure → flag the **possibility of a
p:q resonance** (Mercury 3:2) and note the substellar point moves — a gameplay-relevant
distinction for surface-temperature mapping.

---

## 5. The atmospheric thermal-tide exception

A locked-by-`τ_lock` body in the habitable zone is **not automatically 1:1** if it
carries a thick atmosphere. Stellar heating drives a daily **thermal tide** — a
pressure bulge in the atmosphere — whose gravitational pull on the planet applies a
torque. Crucially that thermal-tide torque can act in the **opposite sense** to the
solid-body gravitational tide, and for a sufficiently thick atmosphere it can balance
or overpower it, parking the spin in an **asynchronous** state away from 1:1.

- **Venus is the Solar-System proof.** Its slow *retrograde* spin is the signature:
  Gold & Soter 1969 (`1969Icar...11..356G`) proposed the atmospheric-tide mechanism,
  and Dobrovolskis & Ingersoll 1980 (`1980Icar...41....1D`) worked the torque balance —
  the thermal tide holds Venus off the 1:1 state the gravitational tide would otherwise
  enforce.
- **Terrestrial exoplanets generalize it.** Leconte et al. 2015 (`2015Sci...347..632L`,
  arXiv:1502.01952) showed that **Earth-mass HZ planets around lower-mass stars can be
  driven into asynchronous rotation by the atmospheric thermal tide** — i.e. the naive
  "M-dwarf HZ planet ⇒ 1:1 locked" inference can fail if the atmosphere is thick enough.
  Correia, Levrard & Laskar 2008 (`2008A&A...488L..63C`, arXiv:0808.1071) earlier mapped
  the equilibrium-rotation regimes including the atmospheric-tide branch.

**When it applies:** the thermal tide scales with atmospheric mass/surface pressure, so
the caveat **mainly matters for thick atmospheres** (≳ Earth-like, and especially
Venus-like ≫ 1 bar). **Thin- or no-atmosphere bodies lock to 1:1** — the airless Moon
and Mercury are not deflected by it; their state is set by §4 alone. The coupling to
atmosphere thickness is why this exception is owned jointly with the
[exoplanet-atmosphere doc](exoplanet-atmosphere-methodology.md): you cannot decide the
final rotation state of a thick-atmosphere HZ planet from the despin timescale alone.

Practical rule: if a NearStars HZ body has `τ_lock ≪ t_sys` **and** a thin/no atmosphere
→ assert 1:1 (temperature doc valid). If it has a **thick** atmosphere → flag the
**Leconte thermal-tide caveat**: the body may be asynchronous, the substellar point may
circulate, and the 1:1-substellar climate is one possibility among several — choose it
as an explicit, documented art/physics call, not a silent default.

---

## 6. Domain of validity & honesty — Q/k₂ and initial spin

In the spirit of the dynamo and heating docs' caveats, the **method is grounded; the
inputs carry the uncertainty** — and the `a⁶` gate usually swamps that uncertainty.

- **`Q/k₂` is the shared interior unknown** (same one the heating doc carries, inverted).
  It spans ~2–3 orders of magnitude across body classes — rocky `Q/k₂ ~ 10²–10³`, icy
  ~10²–10⁴, giants ~10⁴–10⁶ — and is essentially never measured for an exo-body. It
  enters `τ_lock` **linearly**, so a ×100 swing moves `τ_lock` by ×100.
- **The initial spin `ω₀` is unknown.** It enters linearly too, but it is bounded: a
  primordial spin period of hours–days spans only ~1–2 dex, and it only sets *how much*
  excess angular momentum must be removed, not the scaling. It does not change the
  lock/no-lock verdict for bodies deep inside or far outside the gate.
- **Why the call is still robust:** because `τ_lock ∝ a⁶`, the distance term dominates.
  A close-in body (`a` small) has `τ_lock` so far below the age that even ×100 in
  `Q/k₂` and ×10 in `ω₀` together (×1000) leave it ≪ Gyr — still locked. A far-out body
  (Earth at 1 AU) is so far above the age that the same swings leave it ≫ Gyr — still
  not locked. **Only bodies within ~1 dex of `τ_lock ≈ t_sys`** are genuinely
  uncertain; for those, report the verdict as a *range* and treat the rotation state as
  undecided rather than asserting one.
- **The formula is fixed-Q / equilibrium-tide.** Near a spin–orbit resonance boundary,
  or for capture *probabilities* (§4 (c)), the constant-`Q` model is too crude; the
  frequency-dependent treatments (Makarov 2012; Noyelles et al. 2014; Correia & Laskar
  2009) are needed to decide *which* resonance and with what probability. The despin
  *timescale* is robust; the *captured state* for an eccentric rocky body is not, and
  should be flagged as such.
- **The thermal-tide override (§5) is not in the formula at all.** A thick-atmosphere
  body can have `τ_lock ≪ t_sys` and still not be 1:1. Never assert 1:1 for a thick-
  atmosphere HZ body on the strength of `τ_lock` alone.

The honest posture for NearStars: compute `τ_lock`, compare to the age, and **state the
verdict with its rotation state**. Deep-inside bodies → locked, 1:1 (or pseudo-sync /
p:q per §4) — high confidence, this licenses the sibling docs. Borderline bodies →
"locked within a factor of a few of the age," state undecided. Thick-atmosphere HZ
bodies → locked-but-possibly-asynchronous, flag the Leconte caveat. Where art wants a
particular state the physics leaves open, that is a **documented choice**, never a
silent default — exactly as the heating doc treats its `a⁻⁷·⁵` gate.

---

## 7. Worked examples

**The Moon — the canonical 1:1 lock.** Perturber Earth, `a = 3.84×10⁵ km`, rocky
`Q/k₂ ~ 10²–10³`, `α ≈ 0.39`. The formula returns `τ_lock` of order 10⁷–10⁸ yr —
**≪ 4.5 Gyr**. The Moon despun early and, on its near-circular orbit, settled into
**1:1 synchronous** rotation (one face toward Earth). Verdict: locked, 1:1 — the
textbook anchor and the simplest case the sibling docs assume.

**Mercury — the "not always 1:1" case.** Perturber Sun, `a = 0.39 AU`, `e ≈ 0.206`,
rocky. `τ_lock` is well below the age (Mercury *has* despun), but because of its
eccentricity *and* a permanent quadrupole, it was captured into a **3:2 spin–orbit
resonance** (Goldreich & Peale 1966; capture made likely by Correia & Laskar 2004,
made near-certain with realistic tides by Makarov 2012 / Noyelles+ 2014). It rotates
three times per two orbits, so the substellar point **moves** — the warning case for
blindly applying the temperature doc's fixed-substellar geometry to an eccentric rocky
body. Verdict: despun, but **3:2, not 1:1**.

**Venus — the thermal-tide exception.** Perturber Sun, `a = 0.72 AU`, thick CO₂
atmosphere (~92 bar). The gravitational-tide `τ_lock` is ≲ age, so a naive read says
"near-synchronous." Instead Venus spins **slowly retrograde**, because the atmospheric
**thermal tide** (Gold & Soter 1969; Dobrovolskis & Ingersoll 1980) opposes and
overpowers the gravitational tide. Verdict: **asynchronous — atmosphere wins.** The
lesson the sibling docs need: a thick atmosphere can break the 1:1 assumption even when
`τ_lock` says "locked."

**Proxima b / a generic M-dwarf HZ planet — the assumption-licensing case.** Host an
M dwarf, HZ at `a ~ 0.05 AU` (Proxima b: 0.0485 AU). The `a⁶` term drives `τ_lock` to
**≪ Gyr** — Barnes 2017 (`2017CeMDA.129..509B`) gives locking times of order 10⁶–10⁸ yr
for such orbits, far below the multi-Gyr host ages. **So the body is locked**, and on a
near-circular orbit that means **1:1 synchronous** — which is precisely the state the
[temperature](tidally-locked-temperature-methodology.md) and
[heating](tidal-heating-methodology.md) docs assume for the NearStars terrestrial
roster (Proxima b, the TRAPPIST-1 planets, etc.). **Caveat:** if such a planet has a
*thick* atmosphere, the Leconte 2015 (`2015Sci...347..632L`) thermal-tide caveat (§5)
applies and the 1:1 state is no longer guaranteed — flag it, don't assert it. Turbet
et al. 2016 (`2016A&A...596A.112T`) explores exactly this range of possible Proxima b
spin/climate states.

**A NearStars moon locked to its planet (α Cen system, qualitative).** A moon orbiting
its planet at a few planetary radii sits deep inside the `a⁶` gate: `τ_lock ≪ t_sys`,
so it locks to **1:1 essentially immediately** on the system timescale. This is the
state the [tidal-heating doc](tidal-heating-methodology.md) *assumes* for the α Cen
Phase-4 moons (Dante, Hades, Pandora) when it applies the `(21/2)e²` synchronous
heating form — and this doc is what justifies that assumption. (The same `a⁶` that
locks a close-in moon fast is the inverse of the `a⁻⁷·⁵` that *heats* a close-in moon
hard: close-in moons both lock fastest **and** heat most, which is why they are the
geologically interesting ones.) A moon far out (e.g. the heating doc's Chaos at ~20 R_p)
has a much longer `τ_lock` and need not be assumed 1:1 — consistent with its also being
tidally cold.

---

## 8. Annotated Bibliography

Each entry: authors, year, journal/book, **verified** arXiv id (or "no arXiv" +
bibcode), ADS citation count, and one line on the contribution.

- **Goldreich, P. & Soter, S. (1966)** — *Icarus* 5, 375. **No arXiv**
  (`1966Icar....5..375G`). Cites: 977. "Q in the Solar System" — the founding treatment
  of the tidal quality factor and the despin/tidal-evolution timescales; the source of
  the `Q/k₂` framing used throughout. §1.
- **Goldreich, P. & Peale, S. (1966)** — *AJ* 71, 425. **No arXiv**
  (`1966AJ.....71..425G`). Cites: 351. "Spin-orbit coupling in the solar system" — the
  founding theory of spin–orbit resonance capture; why an eccentric body with a
  permanent quadrupole locks into a p:q resonance (Mercury 3:2) rather than 1:1. §4.
- **Gold, T. & Soter, S. (1969)** — *Icarus* 11, 356. **No arXiv**
  (`1969Icar...11..356G`). Cites: 111. "Atmospheric Tides and the Resonant Rotation of
  Venus" — proposes the atmospheric thermal-tide torque that holds a thick-atmosphere
  body off 1:1; the origin of the §5 exception. §5.
- **Peale, S. J. (1977)** — in *Planetary Satellites* (IAU Colloq. 28). **No arXiv**
  (`1977plsa.conf...87P`). Cites: 58. "Rotation Histories of the Natural Satellites" —
  the classic review of how satellites despin and reach their present rotation states;
  the worked-physics companion to the Moon/Galilean-moon calibration. §2.
- **Dobrovolskis, A. R. & Ingersoll, A. P. (1980)** — *Icarus* 41, 1. **No arXiv**
  (`1980Icar...41....1D`). Cites: 73. "Atmospheric tides and the rotation of Venus I" —
  the quantitative torque balance between the gravitational and thermal tides that sets
  Venus's spin; the mechanism behind §5. §5.
- **Hut, P. (1981)** — *A&A* 99, 126. **No arXiv** (`1981A&A....99..126H`). Cites: 1367.
  "Tidal evolution in close binary systems" — the equilibrium-tide model giving the
  **pseudo-synchronous** equilibrium spin (`ω_eq/n ≈ 1 + 6e²`) for eccentric orbits; the
  source of the §4 (b) formula. §4.
- **Kasting, J. F., Whitmire, D. P. & Reynolds, R. T. (1993)** — *Icarus* 101, 108.
  **No arXiv** (`1993Icar..101..108K`). Cites: 1951. "Habitable Zones around Main
  Sequence Stars" — defines the classical HZ and notes that HZ planets around low-mass
  stars are close enough to become tidally locked; the locking motivation for the
  M-dwarf HZ. §3.
- **Murray, C. D. & Dermott, S. F. (1999)** — *Solar System Dynamics* (Cambridge Univ.
  Press). **Book** (`1999ssd..book.....M`). Cites: 2002. The standard textbook
  derivation of the tidal torque, the despin timescale, and spin–orbit dynamics (§5);
  the canonical source for the §1 formula rather than any single journal paper. §1, §2.
- **Correia, A. C. M. & Laskar, J. (2004)** — *Nature* 429, 848. **No arXiv**
  (`2004Natur.429..848C`). Cites: 122. "Mercury's capture into the 3/2 spin-orbit
  resonance as a result of its chaotic dynamics" — explains why Mercury sits in 3:2 (the
  capture-probability problem) via chaotic orbital evolution. §4, §7.
- **Dobrovolskis, A. R. (2007)** — *Icarus* 192, 1. **No arXiv** (`2007Icar..192....1D`).
  Cites: 40. "Spin states and climates of eccentric exoplanets" — works out the
  rotation states (including pseudo-synchronous) and the climate consequences for
  eccentric exoplanets. §4.
- **Correia, A. C. M., Levrard, B. & Laskar, J. (2008)** — *A&A* 488, L63.
  **arXiv:0808.1071.** Cites: 44. "On the equilibrium rotation of Earth-like extra-solar
  planets" — maps the equilibrium-rotation regimes including the atmospheric-thermal-tide
  branch; the exoplanet bridge for §5. §5.
- **Makarov, V. V. (2012)** — *ApJ* 752, 73. **arXiv:1110.2658.** Cites: 56. "Conditions
  of Passage and Entrapment of Terrestrial Planets in Spin-orbit Resonances" — capture
  probabilities for p:q resonances with a realistic (frequency-dependent) tidal model;
  3:2 capture near-certain for Mercury's eccentricity. §4, §6.
- **Noyelles, B., Frouard, J., Makarov, V. V. & Efroimsky, M. (2014)** — *Icarus* 241,
  26. **arXiv:1307.0136.** Cites: 77. "Spin-orbit evolution of Mercury revisited" —
  the modern frequency-dependent-rheology treatment of Mercury's 3:2 capture; shows the
  fixed-Q model is too crude for the *captured state* (not the timescale). §4, §6.
- **Leconte, J., Wu, H., Menou, K. & Murray, N. (2015)** — *Science* 347, 632.
  **arXiv:1502.01952.** Cites: 166. "Asynchronous rotation of Earth-mass planets in the
  habitable zone of lower-mass stars" — the key result that the atmospheric thermal tide
  can drive HZ terrestrial exoplanets into asynchronous rotation; the modern form of the
  §5 caveat that breaks the naive "M-dwarf HZ ⇒ 1:1" inference. §5, §7.
- **Barnes, R. (2017)** — *Celest. Mech. Dyn. Astron.* 129, 509. **arXiv:1708.02981.**
  Cites: 190. "Tidal locking of habitable exoplanets" — the review-level treatment of
  whether and how fast HZ planets lock, with the locking-timescale magnitudes; the
  source for the "M-dwarf HZ planet locks in 10⁶–10⁸ yr" magnitudes that license the
  sibling docs' synchronous assumption. §3, §7.

Cross-referenced (from the sibling temperature doc, not re-derived here):

- **Turbet, M. et al. (2016)** — *A&A* 596, A112. **arXiv:1608.06827.** Cites: 230. "The
  habitability of Proxima Centauri b. II" — explores the range of possible spin/climate
  states (including the thermal-tide-driven ones) for the Proxima b worked example. §7.

**Topics with no single canonical paper:** the class `Q/k₂` *bands* in §6 are a
synthesis of the Goldreich & Soter 1966 / Murray & Dermott literature (shared with the
heating doc's §5), not a single citable table — treated as order-of-magnitude guides.
The *initial spin* `ω₀` has no canonical value (it is a primordial unknown); it is
bounded by argument, not cited.

---

## Related

- `docs/reference/tidal-heating-methodology.md` — the sibling that **assumes the lock
  this doc establishes**: it applies the `(21/2)e²` synchronous heating form to close-in
  bodies, which is valid precisely because their `τ_lock ≪ age` here. The two share the
  same `Q/k₂` interior unknown (inverted: heating uses `k₂/Q`, locking uses `Q/k₂`) and
  the same "steep power of `a` makes the call robust" lesson (`a⁻⁷·⁵` there, `a⁶` here).
- `docs/reference/tidally-locked-temperature-methodology.md` — its substellar-point
  geometry assumes the **1:1 state this doc confirms**; the eccentric pseudo-synchronous
  / 3:2 cases (§4) and the thermal-tide exception (§5) **complicate** that geometry (a
  moving or circulating substellar point), so check the rotation state before applying it.
- `docs/reference/exoplanet-atmosphere-methodology.md` — the **thermal-tide exception
  (§5) couples to atmosphere thickness**: a thick atmosphere can prevent 1:1 locking, so
  the final rotation state of an HZ planet cannot be decided from `τ_lock` alone.
- `docs/reference/mass-radius-relation-methodology.md` — `R` (and `m`, via `I`) enter the
  despin timescale; for non-transiting / mass-only bodies the radius comes from here.
- `docs/reference/planetary-dynamo-scaling.md` — the gold-standard sibling scaling-law
  doc (law + calibration + domain-of-validity + worked examples) this doc is modelled on.
