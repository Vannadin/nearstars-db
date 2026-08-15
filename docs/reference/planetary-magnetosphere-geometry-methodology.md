<!-- 쌍극 자기장 세기+항성풍에서 자기권 크기·모양과 방사선대 강도(다요인)를 도출해 Kerbalism 지오메트리로 매핑하는 방법(논문 근거) -->
# Planetary magnetosphere geometry grounding: standoff, belts, and Kerbalism mapping

Method reference for turning a body's **dipole field strength** (from the
[rocky](rocky-planet-dynamo-methodology.md) or [giant](planetary-dynamo-scaling.md)
dynamo recipes) into the **shape and size of its magnetosphere** — the
magnetopause standoff, the radiation-belt extent, and the belt intensity — and
for mapping those onto the fields Kerbalism actually consumes. Kerbalism carries
no physical field in Tesla; it models the radiation environment as *geometry*
(`RadiationModel` belt/pause shells) + *intensity* (`radiation_inner/outer/pause/
surface` in rad/h) + a dipole-axis direction (`geomagnetic_pole_lat/lon`). This
doc is the recipe that derives those from the physics.

**Key discipline (the reason this doc exists):** the field strength sets the
*container*, not the *contents*. Standoff and belt radii scale with the field,
but **belt intensity is governed by separate factors** — the particle source and
loss balance, capped by the Kennel–Petschek stably-trapped-flux limit — and is
*not* a function of field strength alone. Deriving belt intensity from B is the
classic mistake this doc guards against.

## Part A — geometry (shape + size) from the field

### Magnetopause standoff (Chapman–Ferraro balance)

The dayside magnetopause sits where the planetary magnetic pressure balances the
ambient ram pressure (Chapman & Ferraro 1931, [`1931TeMAE..36...77C`](https://ui.adsabs.harvard.edu/abs/1931TeMAE..36...77C); empirical
form Shue et al. 1997/1998, [`1997JGR...102.9497S`](https://ui.adsabs.harvard.edu/abs/1997JGR...102.9497S) / [`1998JGR...10317691S`](https://ui.adsabs.harvard.edu/abs/1998JGR...10317691S)).
With the dipole field falling as `B(r) = B_eq·(R_p/r)³` and the Chapman–Ferraro
surface currents roughly doubling the field at the boundary (factor `f ≈ 2`):

    R_mp / R_p  =  [ f² · B_eq² / (2 μ₀ · P_ram) ]^(1/6)      (μ₀ = 4π×10⁻⁷)

where `P_ram = ρ v²` is the ram pressure of whatever flows past the body —
the **stellar wind** for a planet, or the **parent's co-rotating magnetospheric
plasma** for an embedded moon (see regimes). The `^(1/6)` power makes the standoff
very robust to input error: an 8× error in either B or P moves R_mp by only 2×.

Only the **equatorial (sub-solar) field** enters — the magnetopause nose is on the
magnetic equator. The polar field never appears here; for a pure dipole it is just
`2·B_eq` and carries no independent geometric information (it becomes informative
only for multipolar fields — see regimes).

### Belt extent

Trapped particles ride closed dipole field lines (L-shells), so the belts are
**bounded outside by the magnetopause** (`R_outer ≲ 0.6–0.8 R_mp`) and inside by
the atmosphere/surface (`R_inner ≈ 1.1–2 R_p`). A stronger field → larger standoff
→ room for belts farther out. This is the one place field strength directly sizes
the belts.

### Induced magnetospheres — the no-dynamo branch

Everything above assumes an intrinsic dipole. A body with **no dynamo but an
atmosphere** still gets a magnetosphere-like structure: sunlight photoionizes the
upper atmosphere, the conducting ionosphere excludes the wind's draped field, and
the boundary that forms is the **ionopause / induced magnetosphere boundary**
(Bertucci 2011, [`2011SSRv..162..113B`](https://ui.adsabs.harvard.edu/abs/2011SSRv..162..113B), the Mars/Venus/Titan review; Luhmann 1991,
[`1991SSRv...55..201L`](https://ui.adsabs.harvard.edu/abs/1991SSRv...55..201L)). It is a near-permanent feature, not an occasional one
(Zhang 2009, [`2009GeoRL..3620203Z`](https://ui.adsabs.harvard.edu/abs/2009GeoRL..3620203Z)).

**Standoff.** The balance is ionospheric *thermal* pressure against the shocked-wind
pressure, not magnetic pressure against ram pressure, so Part A's `^(1/6)` law does
not apply. Use the measured scale instead: at Venus the mean ionopause sits **330 km
above the subsolar point, 700 km at the dusk terminator and 1000 km at dawn**, and it
expands and contracts with wind pressure (Brace 1980, [`1980JGR....85.7663B`](https://ui.adsabs.harvard.edu/abs/1980JGR....85.7663B)) — that
is **1.05 R_V subsolar, 1.12–1.17 R_V at the terminator**. Adopt `1.05–1.2 R_p` for
an Earth-to-Venus-class atmosphere and say which end you took; there is no useful
field parameter to derive it from.

**Which branch a body takes.** Not simply "does it have a dynamo": a *weak* dipole
can be worse than none. In hybrid simulations of a Mars-sized planet, increasing the
field **increases** ion escape until the dipole's standoff exceeds the induced
boundary, and only past that does a field start shielding (Egan 2019,
[`2019MNRAS.488.2108E`](https://ui.adsabs.harvard.edu/abs/2019MNRAS.488.2108E)). So the crossover test is `R_mp(B_eq) > r_ionopause`, not
`B_eq > 0`. Below it, treat the body as induced.

**Close-in caution.** The induced magnetosphere can disappear outright when the IMF
turns nearly radial, and by extension under the extreme wind pressures of a close-in
orbit (Zhang 2009) — worth stating for any tidally-locked planet inside ~0.1 AU
rather than assuming a permanent boundary.

**Shape function: the stock pause function, generalized.** The literature has its own
form for this boundary and it is not Shue: the published induced-magnetosphere-boundary
model is "a circle on the dayside and a straight line on the nightside" (Martinecz 2009,
[`2009JGRA..114.0B30M`](https://ui.adsabs.harvard.edu/abs/2009JGRA..114.0B30M)), which Edberg 2024 ([`2024JGRA..12932603E`](https://ui.adsabs.harvard.edu/abs/2024JGRA..12932603E),
[2410.21856](https://arxiv.org/abs/2410.21856)) tested against Solar Orbiter, BepiColombo and Parker
Solar Probe crossings and found valid to at least 20 R_V unchanged, the nightside line
being `ρ = 1.13 − 0.101·X'` — a 5.77° flare. Conic sections are used at these planets for
the *bow shock*, not for this boundary.

That form is **not implemented**, and this is where the project's shape policy applies
(owner decisions, 2026-08-14):

> Unify on Shue wherever possible. Fall back to the generalized stock function **only where
> Shue geometrically cannot represent the boundary**, or where no fitted α exists to use.

| condition | shape | bodies |
|---|---|---|
| a fitted α exists | **Shue** | Mercury, Earth, Jupiter, Saturn |
| an α adopted by analogy | **Shue**, labelled as an analogy | Uranus, Neptune |
| Shue geometrically impossible | generalized stock (`pause_waist` / `pause_smooth`) | **Venus, Mars** — the induced branch |

**Every α is now verified against full text** (papers cached under `docs/phase3/_papers/`),
and each body's `pause_compression` is set to `2^α` so that `log₂(compression)` recovers it
exactly, with `pause_radius` = nose × `2^α`:

| body | α | nose | flank = nose·2^α | source |
|---|---|---|---|---|
| Mercury | 0.500 | 1.45 R_M | 2.051 | Winslow 2013 ([`2013JGRA..118.2213W`](https://ui.adsabs.harvard.edu/abs/2013JGRA..118.2213W)) — `R_ss` 1.45 R_M, flaring 0.5 at mean `P_Ram` 14.3 nPa |
| Earth | 0.580 | 10 R_E | 14.948 | Shue 1998 ([`1998JGR...10317691S`](https://ui.adsabs.harvard.edu/abs/1998JGR...10317691S)) eq. (11): `α = (0.58 − 0.007 Bz)[1 + 0.024 ln Dp]` |
| Jupiter | 0.423 | 63 R_J | 84.465 | Rutala 2025 ([2502.09186](https://arxiv.org/abs/2502.09186)) S97* Table 2: `α = 0.28 + 1.08 p_SW`, `r_SS = 38.0 p_SW^−0.25` |
| Saturn | 0.736 | 24 R_S | 39.968 | Kanani 2010 ([`2010JGRA..115.6207K`](https://ui.adsabs.harvard.edu/abs/2010JGRA..115.6207K)) eq. (12): `α = 0.73 ± 0.07 + (0.4 ± 0.5) Dp` |
| Uranus | 0.580 | 18 R_U | 26.907 | **analogy** — Earth's α, on the grounds below |
| Neptune | 0.580 | 26.5 R_N | 39.614 | **analogy** — Earth's α, on the grounds below |

Saturn earns a genuine cross-check: Kanani's `a₄` = 0.4 ± 0.5 is not distinguishable from
zero, so α is effectively pressure-independent at 0.73, while the earlier Arridge 2006 fit
([`2006JGRA..11111227A`](https://ui.adsabs.harvard.edu/abs/2006JGRA..11111227A)) has the *opposite* pressure sign, `α = 0.77 − 1.5 Dp`. Both
nevertheless land on **0.7356 and 0.7358** at our adopted 24 R_S nose — two fits with
different coefficients and different crossing sets agreeing to 0.0002. Kanani is taken as
primary: it uses 191 crossings against 64, adds magnetospheric plasma pressure, and its
higher RMS is a dataset effect, not a regression (the paper notes that A06's coefficients on
the new crossings give RMS 3.82 against the new model's 3.603).

**Why Uranus and Neptune take Earth's α by analogy.** No Shue-form fit exists for either
planet, and the four fitted anchors do not support extrapolation: ordered by dynamic
pressure they run 14.3 nPa → 0.500, 1 → 0.580, 0.132 → **0.423**, 0.0146 → 0.736. Jupiter
breaks the ordering — the lowest α at an intermediate pressure — because α is governed by
internal plasma loading as much as by the wind, and Jupiter's Io torus inflates a
magnetodisc that suppresses flaring. So there is no α(pressure) law to extrapolate along.
What can be argued is the *loading*: Voyager 2 found the ice giants to be the emptiest
magnetospheres measured. At Uranus "the Uranian moons do not appear to be a significant
plasma source", with a peak density near 2 cm⁻³ (Bridge 1986,
[`1986Sci...233...89B`](https://ui.adsabs.harvard.edu/abs/1986Sci...233...89B)); at Neptune the maximum density is 1.4 cm⁻³, "the smallest
observed by Voyager in any magnetosphere" (Belcher 1989, [`1989Sci...246.1478B`](https://ui.adsabs.harvard.edu/abs/1989Sci...246.1478B)). With
no Io- or Enceladus-class source, their loading sits nearer Earth's than the gas giants', so
Earth's α is the defensible stand-in. It is an **analogy, not a fit**, and is labelled as
one wherever it appears.

**Tail length (`L`) is an engine artifact, and it is still unset.** `L` is where the bounded
cfg volume closes. Shue has no counterpart for it — the family has exactly two parameters,
`r₀` and `α`, and no α gives a finite endpoint (α < 0.5 decays to zero asymptotically,
α = 0.5 is a cylinder of radius `2 r₀`, α > 0.5 diverges; Winslow 2013 states the same
threshold). So `L` cannot be derived, and six attempts to derive it are tabulated below as
dead ends.

The values currently shipped are **inherited and ungrounded**: `pause_extension` was
recomputed only to preserve each body's pre-existing tail, which for the four outer planets
was itself an arbitrary `rad` divided by a stock `ext`. Mercury (32 R_M) and Earth (200 R_E)
carry the stock numbers unchanged.

Two things are measured and must not be confused with `L`:

| body | flaring ceases at | source |
|---|---|---|
| Mercury | 2.9 R_M (2 R_ss) | Winslow 2013 — "the downstream flaring of Mercury's tail ceases by ~2 R_ss" |
| Earth | 120 R_E (12 R_ss) | Slavin 1985 — flaring ceases at \|X\| = 120 ± 10 R_E |

That is where the **shape** stops changing, not where the tail ends; beyond it the boundary
continues as a constant-radius cylinder. Setting `L` to those distances was tried and is
wrong: at Earth it drives the width to zero at exactly the place Slavin measures a 30 R_E
radius. `L` must sit outside the measured range, and the further out it sits the better the
measured widths are reproduced (at Earth, `L` 200 gives 12.1 R_E at −180 against a measured
30; `L` 1500 gives 29.4).

Both anchors do confirm the α-derived **shape**, which was not fitted to them: at x = −3 R_M
Winslow reports a nearly cylindrical radius of ~2.7 R_M and our surface gives **2.71**; at
x = −120 R_E Slavin reports a diameter of 60 ± 5 R_E and ours gives **28.1** in radius.

Every published tail extent is a spacecraft-coverage **lower bound**, not an endpoint — the
largest is Jupiter's, at least 9000 R_J = 143 `r₀` (Lepping 1983,
[`1983JGR....88.8801L`](https://ui.adsabs.harvard.edu/abs/1983JGR....88.8801L); Voyager 2 detected it to ~4.5 AU, Kurth 1982
[`1982JGR....8710373K`](https://ui.adsabs.harvard.edu/abs/1982JGR....8710373K), with Saturn itself immersed in it, Desch 1983
[`1983JGR....88.6904D`](https://ui.adsabs.harvard.edu/abs/1983JGR....88.6904D)). A convention that contradicts none of them therefore has to
put `L` beyond 143 `r₀`. **The convention is not yet chosen**; the leading candidate is
`L = 150 r₀`, which depends only on `r₀` and so inherits no unverified relation.

Venus and Mars fall into the last row because Shue's single α cannot hold a tight waist
and a widening tail apart at any value — the measured failure modes are tabulated below.
Their fields and derivation live in Part C's ⚗ section; the values are:

| | radius | compression | extension | smooth | waist |
|---|---|---|---|---|---|
| Venus | 1.14 | 1.0151 | 0.0567 | 0.57 | 0 |
| Mars | 1.47 | 1.0684 | 0.0737 | 0.735 | 0 |

The binding constraint is that **the boundary must not bulge behind the terminator**. The
width is `√(radius² − px²)` and so can never exceed `radius`; setting `radius` = the
measured terminator width therefore makes a rear bulge structurally impossible, and the
profile is monotone behind the shoulder. Nose and terminator then come out exact, the tail
closes at 20 R_p, and the bulge is 0.000%. The cost is wake width — 15% narrow at 2 R_p,
33% at 5, 54% at 10 against the measured cone.

Every alternative was measured before this one was adopted, and each is recorded so it is
not re-attempted:

| candidate | nose | terminator | wake | verdict |
|---|---|---|---|---|
| stock, unmodified | −15% | +47% | −47% | both measured values wrong |
| Shue, α = log₂(comp) | 0.00% | +0.9% | −83% … −100% | tail vanishes 2 R_p behind the planet |
| Shue, α ≈ 0.44 (min-max fit) | 0.00% | +23% | ±31% | `pause_alpha` and `pause_compression` would describe different daysides |
| softened Shue, α and L fitted | 0.00% | +32.5% | −32.5% | best the family allows; ε ≪ 0.5 whenever L ≫ r₀, so the terminator collapses to r₀·2^α |
| conic about a focus | — | — | +60% | closed as an ellipse it dips to 0.9745 R_V, **below the surface** |
| circle + cone + closure cap | 0.00% | 0.00% | 0.00% | exact, but needs a shape family of its own |
| **generalized stock** | **0.00%** | **0.00%** | −15% … −54% | adopted |

Why no Shue member can do better, structurally: its tail width goes as `ρ ∝ u^(1−2α)` for
`u = π − θ`, so α = 0.5 is exactly the cylindrical-tail threshold, while the *same* α fixes
the terminator width at `r₀·2^α`. One knob, two jobs, and an induced boundary needs a tight
waist together with a widening tail.

Mars keeps its dayside from Vignes 2000 ([`2000GeoRL..27...49V`](https://ui.adsabs.harvard.edu/abs/2000GeoRL..27...49V), Table 2, N = 488)
and takes nothing from its nightside: that paper's own abstract calls the "nightside MPB
position… highly variable", and Němec 2020 ([`2020JGRA..12528509N`](https://ui.adsabs.harvard.edu/abs/2020JGRA..12528509N)) states the
MAVEN-era models "are deemed unreliable beyond the terminator".

**Kerbalism mapping.** The engine already has this branch: the `ionosphere` model is
a **pause-only** shell, `pause_radius` 1.1 R with `pause_extension` 0.2 (a long
induced tail) and no belt fields at all, carrying `radiation_pause` ≈ −0.005 —
weaker than a dipole magnetopause, which is right, since an induced boundary screens
GCR far less. Venus and Titan ship with it. For NearStars:

- **no dynamo + atmosphere** → `ionosphere`-style pause at the ionopause estimate,
  no belts, small negative `radiation_pause`;
- **no dynamo + airless** → no `RadiationModel` at all; the surface dose is the
  direct wind/GCR flux (that chain is `surface-radiation-dose-methodology.md`);
- **weak dynamo** → run the crossover test above before assuming belts exist at all.

Per-model cfg values and the bodies that use them are tabulated in
[`solar-system-radiation-belts.md`](solar-system-radiation-belts.md).

### Near-tail X-line distance — the one magnetotail scale that generalises

The magnetotail's **near reconnection line** — Earth's near-Earth neutral line (NENL), and
its counterpart at every other magnetised planet — sits at a distance that scales with the
subsolar standoff, and it is the only tail structure with enough measurements to build a
recipe on. Five planets have it:

| body | `r₀` | near X-line | `X/r₀` | source |
|---|---|---|---|---|
| Mercury | 1.45 R_M | 2–3 R_M | 1.38–2.07 | Poh 2017 ([`2017GeoRL..44..678P`](https://ui.adsabs.harvard.edu/abs/2017GeoRL..44..678P)) "average X-line location at −3 R_M"; Sun 2016 ([`2016JGRA..121.7590S`](https://ui.adsabs.harvard.edu/abs/2016JGRA..121.7590S)) −2 to −3 (NMNL) |
| Earth | 10 R_E | 20–30 R_E | 2.00–3.00 | Nagai 2021 ([`2021JGRA..12629691N`](https://ui.adsabs.harvard.edu/abs/2021JGRA..12629691N)), >50 Geotail encounters; Baumjohann 1999 ([`1999JGR...10424995B`](https://ui.adsabs.harvard.edu/abs/1999JGR...10424995B)) narrows to 21–26 |
| Saturn | 24 R_S | 20–30 R_S | 0.83–1.25 | Smith 2016 ([`2016JGRA..121.2984S`](https://ui.adsabs.harvard.edu/abs/2016JGRA..121.2984S)) |
| Jupiter | 63 R_J | 80 R_J | 1.27 | Ge 2010 ([`2010P&SS...58.1455G`](https://ui.adsabs.harvard.edu/abs/2010P%26SS...58.1455G)) |
| Uranus | 18 R_U | ~54 R_U | 3.00 | DiBraccio 2019 ([`2019AGUFMSM33E3247D`](https://ui.adsabs.harvard.edu/abs/2019AGUFMSM33E3247D)), Voyager 2 plasmoid |

**The comparison only works if the same structure is compared.** An earlier pass put Earth's
*distant* neutral line (100–140 R_E, 10–14 `r₀`) beside everyone else's *near* line and
concluded the scatter was 12×, which killed several candidate recipes. The names carried the
answer: Mercury's is literally the "Near-Mercury Neutral Line". Compared like with like the
spread is **1.04–3.00, a factor of 2.9**, and Earth's distant line is a separate structure
measured nowhere else.

Two refinements are available, and they differ in how much they can be trusted.

**Grouped constant.** The two gas giants sit at 1.04 and 1.27, everything else at 1.72–3.00.
Taking `X ≈ 1.16 r₀` for Jupiter and Saturn is a two-point average with a clear physical
reading — heavy internal plasma (Io, Enceladus) plus fast rotation drives Vasyliunas-cycle
reconnection just behind the standoff distance.

**Size-dependent fit for the rest.** Across three orders of magnitude in `r₀` the remaining
three fall on a line:

    X/r₀ = −0.420 + 0.6055 · log₁₀(r₀ [km])        residuals ≤ 0.011

Mercury 1.72 (fit 1.73), Earth 2.50 (2.49), Uranus 3.00 (3.01). Neptune, which has no
measurement, is predicted at **3.10 `r₀` = 82 R_N**.

**How much that residual is worth.** With three points and two parameters there is one
degree of freedom, so any variable ordering the bodies the same way will fit *somehow*. It
was tested: refitting against planet mass gives a worst residual of 0.075, planet radius
0.167, rotation period 0.218, heliocentric distance 0.285. `r₀` beats them by 7–26×, so the
choice of variable is not arbitrary — but the fit still reproduces only the points it was
built from.

**Grade: empirical, anchors reproduced, predictive power unverified.** Two things keep it
from being more. There is no fourth body to test it on — Neptune's tail has no plasmoid or
X-line measurement (searched 2026-08-15). And the grouping rationale is contested: Turner
2024 ([`2024JGRA..12932723T`](https://ui.adsabs.harvard.edu/abs/2024JGRA..12932723T)) places Uranus in a **third** category, "unlike the other
magnetospheric systems that are Dungey-cycle driven (i.e., Mercury and Earth) or
rotationally driven (Jupiter and Saturn)", and Gershman 2020 ([`2020EPSC...14..258G`](https://ui.adsabs.harvard.edu/abs/2020EPSC...14..258G))
reports Voyager 2 measuring `M_A` ~23 at Uranus with a plasmoid "suggestive of more internal
planetary plasma driven" transport. So Uranus may not belong with Mercury and Earth at all,
even though it lands on their line. Neptune is the first test if a measurement ever appears.

For an exoplanet the recipe needs nothing but `r₀`, which Part A already produces:

    strong internal plasma source (Io/Enceladus-class torus + fast rotation)
        X ≈ 1.16 · r₀
    otherwise
        X ≈ (−0.420 + 0.6055 · log₁₀ r₀[km]) · r₀        fall back to 1.9 · r₀ if unsure

**This is not the tail length, and Shue has no tail length.** The Shue family has exactly two
parameters, `r₀` and `α`: `r₀ · 2^α` is the terminator width, and α alone fixes the far-tail
behaviour — below 0.5 the width decays to zero asymptotically, at exactly 0.5 the tail is a
cylinder of radius `2 r₀`, above 0.5 it diverges (Winslow 2013 states the same threshold:
"a … governs whether the magnetotail is closed (a<0.5) or open (a≥0.5)"). **No α yields a
finite endpoint.** `pause_extension`'s `L` is therefore an engine artifact — the place the
bounded cfg volume closes — not a physical quantity, and it must be placed outside the
measured range or it destroys the widths α reproduces.

**Criteria tried and rejected**, recorded so none is re-attempted:

| criterion | why it failed |
|---|---|
| lobe pressure = ambient static pressure | pressure balance is satisfied indefinitely; beyond flaring cessation the tail is a constant-radius cylinder (Slavin 1985: `B_L` fixed at 9.2 nT past 120 R_E) |
| flaring cessation as `L` | it is where the *shape* stops changing, not where the tail closes; setting `L` = 120 R_E drove Earth's width to zero exactly where 30 R_E is measured |
| nose-contrast threshold | the contrast excess at cessation is 5.3% at Earth against 32.7% at Mercury |
| "fully interior region vanishes" (contrast × cross-section) | the only criterion that stays finite for every α, and the closest yet — but Earth 1.57% vs Mercury 5.94%, and Saturn's α 0.736 pushes its answer to 676 `r₀` |
| 12 × nose, Earth-calibrated | falsified by Mercury; its claimed Jupiter check used Kurth 1981's ">700 R_J" (a lower bound on brief encounters) when Lepping 1983 ([`1983JGR....88.8801L`](https://ui.adsabs.harvard.edu/abs/1983JGR....88.8801L)) documents ≥9000 R_J |

**One side result worth keeping.** At the stagnation point the balance is
`B²/2μ₀ = k·P_dyn`, so the pressure contrast against the ambient static pressure is
`k·P_dyn/P_static` — and because both scale as `r⁻²` with heliocentric distance, that ratio
is **the same 48.7× at every planet**. It gives the magnetopause nose field directly for any
body, `B = √(2μ₀ k P_dyn)`, which returns 62 nT at Earth against an observed 60–70 nT.
Useful for exoplanets, where `P_dyn` follows from the stellar wind.

## Part B — belt intensity is multi-factor (NOT field strength)

Belt intensity is a **source − loss balance, capped by a field/plasma ceiling**:

1. **Source** sets the floor: stellar-wind capture; **CRAND** — cosmic-ray albedo
   neutron decay, the inner-belt proton source (Lenchek 1961, [`1961JGR....66.4027L`](https://ui.adsabs.harvard.edu/abs/1961JGR....66.4027L));
   radial diffusion transporting particles inward (Schulz & Lanzerotti 1974,
   [`1974pdrb.book.....S`](https://ui.adsabs.harvard.edu/abs/1974pdrb.book.....S)); and **internal plasma sources** — a volcanic moon can
   dominate everything (Io feeds ~1 ton/s into Jupiter's belts; Bagenal 1994 Io
   torus, [`1994JGR....9911043B`](https://ui.adsabs.harvard.edu/abs/1994JGR....9911043B); Divine & Garrett 1983 Jovian model, [`1983JGR....88.6889D`](https://ui.adsabs.harvard.edu/abs/1983JGR....88.6889D)).
2. **Kennel–Petschek ceiling** caps it: there is a *maximum stably-trapped flux*
   above which the particles' own whistler-mode waves grow and scatter them into
   the loss cone (Kennel & Petschek 1966, [`1966JGR....71....1K`](https://ui.adsabs.harvard.edu/abs/1966JGR....71....1K), 2600+ citations).
   The limit depends on the field and cold-plasma density but is **independent of
   source strength** — so a strong-source magnetosphere (Earth, Jupiter) *saturates*
   at the K–P ceiling, and adding more source does not raise the intensity.
3. **Losses** pull it down: wave–particle scattering (chorus/hiss/EMIC; Thorne 2010,
   [`2010GeoRL..3722107T`](https://ui.adsabs.harvard.edu/abs/2010GeoRL..3722107T); review Ripoll 2020, [`2020JGRA..12526735R`](https://ui.adsabs.harvard.edu/abs/2020JGRA..12526735R)), Coulomb/
   atmospheric losses, and **absorption by moons and rings** — Saturn's belts are
   swept out by its rings/moons (Cooper 1983, [`1983JGR....88.3945C`](https://ui.adsabs.harvard.edu/abs/1983JGR....88.3945C)).

Consequence for derivation: **you cannot read belt intensity off B_eq.** Two
bodies with identical fields can differ by orders of magnitude in belt dose
depending on source (a volcanic moon vs none) and loss (rings/moons sweeping). The
field tells you *whether* and *where* belts trap; the source/loss/K–P balance tells
you *how intense*. Belt intensity therefore stays a **regime call with a stated
source and loss**, not a formula output.

### The exact K–P ceiling (computable) and what it does — and does not — set

The K–P limit is now **directly computable** for any body:
[`scripts/refs/kp_limit.py`](../../scripts/refs/kp_limit.py) is a validated
Python port of Mauk & Fox's own published implementation (their open Zenodo
software [`10.5281/zenodo.4782323`](https://zenodo.org/records/4782323),
bibcode [`2021zndo...4782323M`](https://ui.adsabs.harvard.edu/abs/2021zndo...4782323M) — the paper itself,
[`2010JGRA..11512220M`](https://ui.adsabs.harvard.edu/abs/2010JGRA..11512220M),
is paywalled with no preprint). The chain: flexible differential spectrum
`j(E) = C·E·(kT(γ₁+1)+E)^(−γ₁−1)/(1+(E/E₀)^γ₂)` with pitch factor sin^2s α →
relativistic cyclotron resonance (Summers, Tang & Thorne 2009
[`2009JGRA..11410210S`](https://ui.adsabs.harvard.edu/abs/2009JGRA..11410210S),
eqs A4–A8) → whistler growth rate from the A1/A2 integrals → marginal
stability `CmCk = L·R_p·w_i/(3·v_g)` (wave gain 3; independently confirmed by
Mourenas 2024 [`2024JGRA..12932193M`](https://ui.adsabs.harvard.edu/abs/2024JGRA..12932193M)).
The limited spectrum is ~E⁻¹ (relativistic coefficient 2× non-relativistic;
Summers 2014 [`2014JGRA..119.6313S`](https://ui.adsabs.harvard.edu/abs/2014JGRA..119.6313S)).

**Validation (all five magnetized planets).** With the three source papers in
the local cache (AGU's 24-month free-access archive; owner-downloaded PDFs in
`docs/phase3/_papers/`), the port's normalisations are the *published* Summers
2009 A2/A3 prefactors, and the notebook's Earth L=5 printed intermediates are
reproduced to ~10⁻⁶ (w_i 0.658455, CmCk peak 0.607879 at 102.9 keV — exact to
their printed digits). The Mauk & Fox per-planet analyses (their Table 1
spectra + per-figure B/N/D) are then reproduced at the level their figures
state:

| Case (their figure) | Their finding | Our CmCk peak |
|---|---|---|
| Earth L=4 (Fig 7) | well below the limit | 0.28 ✓ |
| Earth L=5 (Fig 5) | 0.60, near the limit | 0.6079 (exact) |
| Earth L=6 (Fig 7) | near the limit | 1.46 ✓ |
| Uranus L=4.73 (Fig 8, N=5) | matched/exceeded | 1.11 ✓ |
| Jupiter L=8.3 (Fig 9, N=200, D=3) | near the limit | 0.68 ✓ |
| Neptune L=7.4 (Fig 11, N=0.3) | ~30× below at 1 MeV | peak 0.91; 1 MeV factor 27.8 ✓ |

These run in the module's `__main__` self-test.

Two structural facts the exact machinery establishes:

1. **The ceiling's controlling variable is We/wpe ∝ B/√n_cold** (plus the
   spectral and pitch indices) — *not* B alone and not B². Where the local
   field is strong and the cold plasma thin (deep inner belts at small L),
   the resonant energy runs to tens of MeV and the ~MeV ceiling is
   effectively unbound — those belts are **source/loss-set, not K–P-set**.
   Worked check (Alpha Centauri A b (Polyphemus) inner-belt peak, L = 2.07, B_local ≈ 129× Earth's
   L=5 field): across torus densities 10²–5×10³ cm⁻³ the computed 1 MeV
   ceiling is ≥ 5×10²–10¹⁶ × Earth's — never the binding constraint.
2. **The K–P cap does not set the dose contrast between planets.** Mauk & Fox
   find Earth, Jupiter and Uranus all *at* comparable differential caps near
   ~0.1–1 MeV, yet their doses differ by orders of magnitude: the dose is the
   spectrally-integrated, shield-transported quantity, dominated by the
   **hardness of the tail** above the shield transmission cutoff (a 1 MeV
   electron's CSDA range ≈ 2.0 mm Al) and by belt size. The community-standard
   transport is SHIELDOSE-2 (Seltzer
   [`1979ITNS...26.4896S`](https://ui.adsabs.harvard.edu/abs/1979ITNS...26.4896S),
   [`1992STIN...9315580S`](https://ui.adsabs.harvard.edu/abs/1992STIN...9315580S));
   textbook free-field factor ≈ 2.3×10⁻⁸ rad(Si) per e⁻ cm⁻² at 1 MeV,
   de-rated ~10× behind ~2.5 mm Al.

**Practical rad/h recipe (corrected status).** For a source-saturated
Jupiter-architecture system, interpolate between the two audited saturated
*dose anchors* — Earth 31 µT → 10.4 rad/h, Jupiter 428 µT → ~1500 rad/h —
`dose ≈ 10.4 × (B_eq/31 µT)^1.9`. This is an **empirical dose-anchor
interpolation** that bundles the hardness + belt-size effects; it is *not*
the K–P scaling (an earlier revision mislabeled it so — retracted). Outer/inner
ratio ~0.1 torus-driven (Jupiter), ~0.2 wind-fed (Earth). Then apply the two
hard checks: (a) the chosen intensity must sit below the computed K–P ceiling
at the belt's (B, L, n_cold) via `kp_limit.py` (A b 300 rad/h ≈ 29×
Earth ≪ ceiling ≥ 5×10²× Earth at the densest plausible torus — passes); and
(b) source-starved / gap-starved belts sit *below* any of this and stay plain
regime calls (Alpha Centauri A b III (Pandora) 0.4× Earth). Confidence remains low — the interpolation
exponent is a two-anchor fit, and n_cold for a fiction torus is a stated
assumption — but every factor is now mechanistic, pinned, and bounded.

**Worked case — Proxima d (16 G SPI polar field, wind/flare-fed, no torus).**
B_eq = 800 µT → the anchor interpolation gives inner ~5×10³ rad/h and outer
~1×10³ (wind-fed 0.2 ratio). This extrapolates 1.9× beyond the Jupiter anchor,
so confidence is low, and the 3–280 G field range spans 2×10²–10⁶ rad/h.
`kp_limit.py` at L = 4 (B_local 1.25×10⁴ nT; n_cold 1–100 cm⁻³ — an airless
planet feeds no ionospheric plasmasphere) gives CmCk ≪ 1 at every density: the
K–P ceiling never binds and the belts are source/loss-set, the same structural
regime as every strong-field small-L case. Viz entry: `render_belts_bodies.py
proxima_d_phys`.

## Part C — mapping to Kerbalism

| Physical quantity | Kerbalism field | Derivation |
|---|---|---|
| Magnetopause standoff | `pause_radius` (+ `has_pause`) | **`pause_radius = R_mp × pause_compression`** — dayside x is compressed before the sphere test, so the sub-solar nose sits at `pause_radius/pause_compression` (flank = `pause_radius`). R_mp from Part A is the *nose* |
| Magnetopause shield | `radiation_pause` (small negative) | the shield comes from *having* a pause at `pause_radius`; the value itself is small and stock-uniform (~−0.01), NOT scaled to standoff |
| Belt extent | `inner_dist`/`inner_radius`, `outer_dist`/`outer_radius` (body radii) | Part A bounds |
| Belt intensity (rad/h) | `radiation_inner`/`radiation_outer` | Part B regime: source − loss, K–P-capped — **set from the stated source/loss, not from B** |
| Dipole-axis direction | `geomagnetic_pole_lat`/`lon` | = `magnetic_dipole_tilt_deg` |
| Belt existence gate | (belts present at all) | `B_eq ≳ 0.1× Earth`; below this no stable trapping |

### The RadiationModel geometry (grounded in Kerbalism source)

Kerbalism models each field as a signed-distance shape, all lengths **in body radii**
([Kerbalism modding docs](https://kerbalism.readthedocs.io/en/latest/modders/radiation.html);
stock values from `KerbalismConfig/System/Radiation.cfg`):

- **inner belt** = a torus minus a border torus: `inner_dist` (major radius) +
  `inner_radius` (section radius), carved by `inner_border_dist/radius/deform_xy`
  (a border with `border_dist ≈ 0` is a sphere cut — the loss-cone D-shape). All in
  `deform_xy`-squashed coordinates: equatorial extent = `(dist ± radius)/√deform_xy`.
  (`*_border_start/end`, still present in some shipped cfgs, are legacy — the current
  parser reads only `border_dist/radius/deform_xy`.)
- **outer belt** = same construction: `outer_dist` + `outer_radius` minus its border.
- **magnetopause** = a sphere `pause_radius`, deformable toward the star (`*_compression`) and into a tail (`*_extension`); `*_quality` is a raymarch setting.
- **`*_deform` is the engine's non-dipolar knob, not decoration** (corrected 2026-08-04).
  It adds `sin(x·5)·sin(y·7)·sin(z·6)·A` to the signed distance, and because it depends on
  all three coordinates *separately* it is the only parameter that **breaks axisymmetry**,
  producing longitude-dependent lobes. `geomagnetic_offset`, by contrast, translates along
  the axis: it is a dipole + quadrupole but stays axisymmetric. So a multipolar field's
  irregular, lobed boundary is expressed through `deform`, and ROKerbalism uses it exactly
  that way: `mercury` and the model literally named `irregular` both carry
  `pause_deform = 0.1`, and `metallic` / `solidiron` / `anomaly` use 0.04–0.1
  (`KSP-RO/ROKerbalism`, `GameData/KerbalismConfig/System/Radiation.cfg`). Kerbalism's own
  modding docs describe it only as "deform the surface using a sum of sine waves", which is
  what led an earlier revision of this doc to call it cosmetic.
- Intensities + axis live on the `RadiationBody`: `radiation_inner/outer/pause` (rad/h, pause negative), `geomagnetic_pole_lat/lon`.

**`inner` and `outer` are always two tori with `inner_dist < outer_dist`** — but whether
they *look* like two separated Van Allen belts or one nested/concentric structure is set
by the section-radius-vs-spacing ratio:

| Stock model | inner `dist / radius` | outer `dist / radius` | `pause_radius` | `radiation_inner / outer / pause` | look |
|---|---|---|---|---|---|
| **earth** (Kerbin) | 0.81 / 0.70 | 2.63 / 2.48 | 13.65 | 10.4 / 2.2 / −0.011 | two **separated** belts |
| **giant** (Jool) | 2.2 / 1.0 | 6.0 / 6.0 | 60 | 200 / 11 / −0.012 | outer section = its radius → hole closes → **concentric** look enclosing the inner |

So the body-class choice is: **rocky / Earth-like → `earth`-style (distinct tori, separated
belts); giant → `giant`-style (fat overlapping tori, concentric look).** Both are just
inner+outer with different `dist/radius` ratios — the "concentric vs separated" question that
recurs in NearStars is a rendering consequence, not two different mechanisms.

Two stock-anchored facts that correct earlier NearStars drafts:
- `radiation_pause` is **small and roughly body-independent in stock** (Kerbin −0.011, Jool
  −0.012) — it is *not* a large standoff-scaled shield term. (An earlier A b III draft used
  −3.8, a Promised-Worlds pack tuning; regrounded to the ~−0.01 stock scale.)
- `geomagnetic_pole_lat ≈ 80` for an Earth-tilt body matches stock Kerbin (80.37).

### Sol / RSS anchors (NearStars is Sol-based — prefer these over stock)

NearStars runs at Sol real-scale, so the **ROKerbalism / RSS** radiation config is the
better anchor than stock Kerbin/Jool (ROKerbalism `KerbalismConfig/System/Radiation.cfg`
+ KerbalismConfig `Support/RSS.cfg`):

| Body | geometry (R_body) | `radiation_inner / outer / pause` | note |
|---|---|---|---|
| Sun | heliopause, `pause_radius` 1000 | surface 46.5, cycle 11 yr | dose source + GCR shield |
| Earth | inner 0.81/0.70, outer 2.63/2.48, pause 15 | 10.4 / 2.2 / **−0.010**, pole 80.4 | **separated** belts |
| Jupiter | inner 6.0/1.0, outer 6.5/6.5, pause 60 | 300 / 50 / **−0.010**, pole −81 | **concentric** (inner at the outer shell's inner edge) |
| Saturn | outer 7/7 only (**no inner**), pause 20 | — / 150 / **−0.011** | inner belt absent — **rings sweep it** (Cooper 1983) |
| Uranus | offset dipole | 75 / 4 / −0.010, pole 31, `geomagnetic_offset` 0.3 | tilted/offset |
| Neptune | offset dipole | 39 / 2.5 / −0.007, pole 43, `geomagnetic_offset` 0.55 | strongly offset |

Three facts this settles for NearStars:
1. **`radiation_pause` ≈ −0.01 for every body** (Earth/Jupiter −0.010, Saturn −0.011,
   Neptune −0.007) — confirms it is a small body-independent term, not a shield
   magnitude. (A b III's −0.01 is right.)
2. **Gas giant → concentric, rocky → separated** is real-body, not just stock KSP.
3. **Ring-loss vs volcanic-source is a competition** — Saturn is modeled *outer only,
   no inner* because ring absorption (Part D loss) wins and guts the inner belt; Jupiter
   keeps an intense inner belt because Io's plasma source (Part D source) wins. A ringed
   giant can go either way. **A b follows Jupiter, not Saturn:** its volcanic inner
   moon Alpha Centauri A b I (Dante) (~820× Io) is an overwhelming source that dominates any ring sweeping →
   an *intensified* inner belt, which the strong intrinsic field of the habitable moon
   A b III then shields against (the design's central drama).
   `geomagnetic_offset` (Uranus 0.3, Neptune 0.55) is the handle for the offset/
   multipolar dipoles of ice giants like Proxima c.

### `radiation_*_gradient` — the radial dose ramp inside a shell

The belt shells are geometry only; the dose a vessel actually takes inside one is

    dose = clamp( gradient · (−SDF) / radius , 0 , 1 ) · radiation_inner|outer

(`Radiation.cs`; reproduced verbatim in `scripts/viz/render_belts.py:50` and in the
belt viewer, which is why the viewer's readout can be trusted as a preview). `−SDF`
is the depth below the shell surface and `radius` is that belt's own `*_radius`, so
the dose ramps **linearly from zero at the boundary to the full intensity at depth**

    d* = *_radius / gradient          (body radii, in the deform_xy-squashed metric)

i.e. `1/gradient` is the fraction of the section radius spent climbing to the
plateau. The shipped values are inner **3.3** (plateau at 30 % of the section
radius) and outer **2.2** (45 %); the emitter and the viewer treat those two as the
omit-if-equal default, so a written `radiation_inner_gradient` line always means a
deliberate departure.

**How to derive it.** The gradient is the one field that encodes the *shape* of the
radial profile rather than its bounds or its peak, so it comes from the same profile
Part B already needs:

1. Take the radial dose (or >MeV flux) profile along the magnetic equator, from the
   Part B source − loss model — anchored bodies can read it off a published model
   (Divine & Garrett 1983 for the Jovian belts, [`1983JGR....88.6889D`](https://ui.adsabs.harvard.edu/abs/1983JGR....88.6889D); radial-diffusion
   profiles per Schulz & Lanzerotti 1974, [`1974pdrb.book.....S`](https://ui.adsabs.harvard.edu/abs/1974pdrb.book.....S)).
2. Evaluate the shell's **own SDF** at that peak on the equator: `d* = −SDF(r_peak)`.
   Do this numerically rather than as `|r_peak − r_edge|` — the border cut,
   `deform_xy` and `deform` all move which boundary is nearest, and for Earth's inner
   belt the binding one is the loss-cone cut, not the torus wall. Evaluating the SDF
   also removes the need to convert into the squashed metric by hand.
3. Clamp `d*` to `d_max`, the depth of the **deepest point that survives the border
   cut** (found the same way, by scanning the SDF over the shell). The cut usually
   carves the torus core away, so `d_max` runs 0.5–0.65 `*_radius` in practice, and an
   evidence peak can land in space the shell no longer occupies.
4. `gradient = *_radius / d*`. The binding floor is therefore
   **`gradient ≥ *_radius / d_max`**, not `≥ 1`: below it the belt never reaches its
   stated `radiation_*` anywhere, and the whole belt is silently scaled down by
   `gradient · d_max / *_radius`.
5. **No profile of its own?** Inherit the *plateau fraction* of the class analog
   rather than the stock number: Earth's inner belt for CRAND proton belts, Earth's
   outer belt for wind- and diffusion-fed electron belts, Jupiter's inner belt for
   torus-fed ones. That keeps an ungrounded body on a measured shape instead of a
   round default.

A profile that peaks right at its core circle gives `gradient ≈ 1` (a long, gentle
climb); a profile that saturates immediately inside the boundary gives a large
gradient (a hard-edged shell).

**Anchor check.** Run on the Solar-System fits, the recipe puts Earth's **outer** belt
at 2.15 against the shipped 2.2 — it recovers a stock value it was never told, which
is the validation. Earth's **inner** belt lands at 2.09 against the shipped 3.3, so it
is the inner-belt steepness that turns out unsupported: the proton peak at L ≈ 1.5
(AE9/AP9, Ginet 2013 [`2013SSRv..179..579G`](https://ui.adsabs.harvard.edu/abs/2013SSRv..179..579G); slot per Ripoll 2016,
[`2016GeoRL..43.5616R`](https://ui.adsabs.harvard.edu/abs/2016GeoRL..43.5616R)) sits 0.37 R_E below the loss-cone cut, not
0.23 R_E. Jupiter's inner belt (peak 1.5–2 R_J, Divine & Garrett 1983) gives 2.24. Uranus
is the case the floor rule exists for: its electron profile is a broad maximum between
moon-swept minima (Cheng 1987, [`1987JGR....9215315C`](https://ui.adsabs.harvard.edu/abs/1987JGR....9215315C)), which reads as a peak at the shell
core — but the core is carved away, so the value clamps to the floor at **1.57** inner
and **1.85** outer. Taken literally (peak at the core, `gradient` 1.0) the belt would
have saturated nowhere and run at 0.64× its stated intensity. Per-body peak positions
and their sources are tabulated in
[`solar-system-radiation-belts.md`](solar-system-radiation-belts.md).

One consequence worth expecting: with the ramp this long, the **fully saturated core is
thin**. Measured on the meridian cross-section, it is 9 % of the shell for Earth's outer
belt and only 1.5 % for the inner one (against 23 % under the stock 3.3). That is the
honest reading of a narrow measured peak, not an artifact — but it does mean the stated
`radiation_inner` is a value a vessel touches only near the belt's heart, and the dose
ladder the moons see should be read off the SDF, not off the headline number.

**Two couplings that bite.**

- **`gradient` ↔ `*_radius`.** They appear only as the ratio `radius/gradient`, so
  any re-fit that moves the section radius silently moves the ramp depth. Re-derive
  the gradient whenever `fit_belts.py` is re-run.
- **`gradient < 1` never reaches the stated intensity.** The clamp saturates at 1,
  and the deepest point of the shell only reaches `−SDF = radius`, so the realized
  peak is `gradient · radiation_*`. If a soft profile forces `gradient < 1`, the
  intensity has to be divided by it to keep the peak dose honest — otherwise the
  board's rad/h number is not what the game applies. (Proxima c's inner belt at
  `gradient 1.9` is inside the safe range; nothing in NearStars currently goes
  below 1.)

Worked example — A b's inner belt: the design puts the peak at A b II's L-shell
(2.07 R_p), which the SDF reports 0.70 R_p below the boundary, so with
`inner_radius` 1.159 the recipe gives `gradient` **1.65** — a much gentler ramp than
the 3.3 default the board still carries, and one that moves the full 300 rad/h out to
where the moon actually orbits.

### Deriving the rest — what fixes each field, and what it drags with it

Derivation order matters: everything downstream of `R_mp` changes when the field or
the wind changes, so run the chain top-down rather than patching single fields.

    B_eq + P_ram  →  R_mp (Part A)  →  pause fields
                                   →  belt L-shell bounds  →  fit_belts.py  →  belt geometry
    source − loss (Part B) + K–P ceiling  →  radiation_inner/outer
    radial profile shape                  →  radiation_*_gradient
    harmonic content / tilt / offset      →  deform, pole_lat/lon, geomagnetic_offset

| Field | What fixes it | Derivation | Couples to |
|---|---|---|---|
| `has_pause` | does the body trap at all | `B_eq ≳ 0.1×` Earth (regime 5 below is `false`) | belts exist only if this does |
| `pause_radius` | Part A nose | `R_mp × pause_compression` — the compression is applied to x *before* the sphere test | `pause_compression`; re-derive both together |
| `pause_compression` | dayside/flank asymmetry | flank/nose ratio; Shue-equivalent `α = log₂(comp)`, so ROK Earth 1.5 ⇒ α 0.585 | `pause_radius`, and the Shue `α` below |
| `pause_extension` | tail closure length | `L = pause_radius / extension`; pick `L` where the lobe field stops mattering for GCR (Earth ≈ 200 R_E) | tail length only; nose unaffected |
| `pause_height_scale` | polar flattening of the pause | ratio of polar to equatorial standoff (1.0 = spherical; giants ~1.1) | independent |
| `radiation_pause` | GCR shield presence | **not** scaled to standoff: ~−0.01 stock-uniform | nothing (see the correction above) |
| `inner_dist` / `outer_dist` | L-shell of the belt core | `L_core` of the drift shell, `r = L cos²λ`, fitted by `fit_belts.py` | `*_radius`, `*_deform_xy` (one joint fit) |
| `inner_radius` / `outer_radius` | shell thickness | half-width of the L-shell band, same fit | `gradient` (ratio, above) |
| `*_deform_xy` | latitudinal squash of the drift shell | from `cos²λ` closure; equatorial extent = `(dist ± radius)/√deform_xy` | reported extents; convert before comparing to profiles |
| `*_border_dist` / `*_border_radius` / `*_border_deform_xy` | the atmospheric loss cone | subtracted shell; `border_dist ≈ 0` degenerates to a sphere cut at the loss-cone altitude (~1.05 R_p) | inner edge of the dose region |
| `*_compression` / `*_extension` (belts) | how much of the boundary's asymmetry reaches the shell | the pause asymmetry damped by `(r_core/R_mp)³` — see below | `pause_compression`/`pause_extension`, and `R_mp` |
| `*_deform` | non-dipolar lumpiness | amplitude in body radii added to the SDF, so the boundary wanders by up to ±A; anchor on ROKerbalism (`mercury` / `irregular` 0.1, `metallic`/`solidiron`/`anomaly` 0.04–0.1) | the (pending) `*_deform_scale` sets its *size* |
| `radiation_inner` / `radiation_outer` | Part B regime call | source − loss, K–P-capped; check against `scripts/refs/kp_limit.py` | `gradient` when it is < 1 |
| `radiation_*_gradient` | radial profile shape | `*_radius / d*` (above) | `*_radius` |
| `geomagnetic_pole_lat` / `_lon` | dipole tilt | `lat = 90° − magnetic_dipole_tilt_deg` (sign follows a reversed dipole: Jupiter −80) | the aurora row's oval offset |
| `geomagnetic_offset` | dipole centre offset | offset distance / R_p, along the magnetic axis (Mercury 0.198, Uranus 0.3, Neptune 0.55) — axisymmetric, unlike `deform` | belts inherit the shift; do not double-count with `deform` |
| `*_quality` | raymarch step count | rendering only, no physics | nothing |
| `radiation_surface` | star-level field | **stars only** — a planetary surface dose does not live here (that chain is `surface-radiation-dose-methodology.md`) | nothing |

### Belt `*_compression` / `*_extension` — the boundary's asymmetry, damped inward

A belt shell is not the magnetopause, and it is not a circle either. It sits between the
two, so the honest question is *how much* of the boundary's day–night asymmetry reaches
it. Two limits fix the answer:

- deep inside (`r ≪ R_mp`) the field is the undistorted dipole, so the shell is
  **symmetric** — `compression = extension = 1`;
- at the boundary the shell *is* the boundary, so it carries the pause's own asymmetry
  (and beyond it drift shells split and open — Pfitzer 1969,
  [`1969JGR....74.4687P`](https://ui.adsabs.harvard.edu/abs/1969JGR....74.4687P); Öztürk & Wolf 2007, [`2007JGRA..112.7207O`](https://ui.adsabs.harvard.edu/abs/2007JGRA..112.7207O)).

The weight between those limits is the ratio of the **external (boundary-current) field
to the dipole field** at that radius. Chapman–Ferraro currents contribute a nearly
uniform field in the inner region whose magnitude is about the dipole's own field at the
boundary — this is the same `f ≈ 2` doubling Part A already relies on — so

    ε(r) = ( r / R_mp )³ ,      r_core = *_dist / √(*_deform_xy)

and the shell inherits that fraction of the pause's distortion:

    *_compression = 1 + ε · (pause_compression − 1)
    *_extension   = 1 − ε · (1 − pause_extension)

Evaluate ε at the shell's **core circle**, not its outer edge: Kerbalism applies one
x-scale to the whole shell, and the core carries both the dose peak and the shell's
characteristic L, so the core value is the shell average rather than its worst point.
The edge value is worth computing as the upper bound — for Earth's outer belt it is
`ε 0.35` against `0.05` at the core, which is the size of the approximation Kerbalism's
one-scale-per-shell design forces on us.

Mead 1964 ([`1964JGR....69.1181M`](https://ui.adsabs.harvard.edu/abs/1964JGR....69.1181M)) is the grounding for the shape of the distortion: the
Chapman–Ferraro solution compresses field lines on **both** the day and night sides, and
the day–night asymmetry proper comes from the distributed tail currents that the
spacecraft-fitted models quantify (Mead & Fairfield 1975,
[`1975JGR....80..523M`](https://ui.adsabs.harvard.edu/abs/1975JGR....80..523M)). Interpolating toward the adopted pause shape is a proxy for
that asymmetric term, not a derivation of it, so this recipe is **medium-low
confidence** — but it is anchored at both ends and it replaces what was previously a
copied constant. Mead's 1964 *numbers* have long been superseded for quantitative work
by the spacecraft-fitted Tsyganenko family (T02, [`2002JGRA..107.1179T`](https://ui.adsabs.harvard.edu/abs/2002JGRA..107.1179T)), which is the
route to take if this ever needs to be better than an interpolation: fit a T-class field
and read the shell asymmetry off it, rather than refine the ansatz.

**Validation.** The recipe recovers ROKerbalism's Ganymede belt compression, 1.05,
without being told (core `ε` 0.139, since an embedded moon's belt fills a large fraction
of its 2 R_moon standoff), and it reproduces Earth's near-symmetric inner belt
(1.001 against the shipped 1.01). At geosynchronous, `ε` 0.29 gives a nightside stretch
of 1.36×, the right order for the well-known day–night asymmetry there. Where it
*disagrees* is instructive: the giants' shipped 1.05 / 0.9 is unreachable, because a
belt at 8 R_J inside a 63 R_J standoff has `ε` 0.002 — those numbers are stylistic, not
physical. The bodies where the term genuinely bites are the compressed ones: **Proxima d**
(outer belt `ε` 0.107 → 1.05 / 0.90, against the Earth-copied 1.01 / 1.0 it carries
today) and the embedded moons Ganymede and A b III (`ε` 0.099 → 1.015 / 0.96).

Two habits that keep this reproducible: derive the belt geometry with
`fit_belts.py` rather than by hand (it optimizes IoU against the actual SDF, so the
numbers you write are the numbers the engine renders), and record the *inputs*
(`B_eq`, `P_ram`, `L`-bounds, source term) on the board next to the outputs, because
the fields above are all downstream of four or five physical numbers.

### ⚗ Fields that do not exist yet — the KerbalismShuePause plugin

Five of the knobs the belt viewer exposes are **not consumed by any shipped
Kerbalism**. They are derived and recorded now, and wait on an in-house Harmony 2
patch (or an upstream PR) — the brief, including the rejected alternatives, is
[`plugins/KerbalismShuePause/README.md`](../../plugins/KerbalismShuePause/README.md).
Pipeline discipline: the emitter keeps them in `PENDING_MODEL_KEYS` and **never**
writes them as cfg lines, the viewer marks them `⚗` and exports them as comments,
and a board may carry the value with an explicit unused marker. So the derivation
happens once, and stock renders stock behaviour until the plugin lands.

**`*_deform_scale`** (`pause_` / `inner_` / `outer_`). Kerbalism's deform adds
`sin(x·5)·sin(y·7)·sin(z·6)·A`: the amplitude `A` is tunable but the wavenumbers are
hardcoded, so *how big* the lumps are cannot be set. At a Mercury-like standoff of
1.54 R_p those wavenumbers put 8–11 lobes around the boundary, far finer than the
multipolar fields the dynamo recipes actually produce. The scale is a multiplier on
the wavenumbers (`1.0` = stock exactly, so no shipped cfg changes), and it is
derived from the field, not chosen for looks:

    k = ℓ / R_mp                deform_scale = k / 5

with `ℓ` the dominant spherical-harmonic degree of the field (from the dynamo
recipe's regime call). A dynamo with power out to `ℓ = 4` at `R_mp` 1.54 wants
`k ≈ 2.6`, i.e. `deform_scale ≈ 0.52`. Amplitude and scale are orthogonal: `A` is
how far the boundary wanders, `scale` is how many lobes it wanders in.

**Generalized stock pause** (`pause_waist`, `pause_smooth`) — the **fallback** route, used
only where Shue geometrically cannot represent the boundary (see the shape policy in
Part A). Today that is Venus and Mars. Rather than adding a second shape family, it
fixes two defects in the shipped function, which is

    px = x·(x < 0 ? extension : compression);   √(px² + (y·height_scale)² + z²) − radius

Both defects are visible: `px` is continuous at `x = 0` but its slope is not, so the two
hemispheres meet at a corner; and because the scale switches exactly at the body plane,
the **widest cross-section is pinned to the planet's centre**, whereas a real boundary's
waist sits downstream. The generalization replaces the piecewise absolute value with its
hyperbolic smoothing and lets the switch plane move:

    u = x − pause_waist
    px = ½(comp+ext)·u + ½(comp−ext)·√(u² + pause_smooth²)

`u → ±∞` recovers `comp·u` and `ext·u`, so the two half-scales keep their stock meaning,
and **`pause_waist` = `pause_smooth` = 0 reproduces stock exactly** — verified by
re-rendering every stock preset to a byte-identical PNG. Neither field exists today: the
[Kerbalism modding docs](https://kerbalism.readthedocs.io/en/latest/modders/radiation.html)
list exactly six `pause_` fields on a `RadiationModel` — `pause_radius`,
`pause_compression`, `pause_extension`, `pause_height_scale`, `pause_deform`,
`pause_quality` — with nothing for a waist offset, a split-plane position, or a smoothing
of the hemisphere junction (checked 2026-08-14). `pause_waist` is signed, positive
sunward. It supersedes the older experimental `pause_offset`, which applied the same
operation with the opposite sign; the emitter keeps the old key for board compatibility.

Deriving them for an induced boundary, with the constraint that **the tail must not bulge**
(owner call, 2026-08-14): the width is `√(radius² − px²)`, which can never exceed `radius`,
so setting `radius` = the measured terminator width makes a rear bulge structurally
impossible and the profile monotone behind the shoulder. Then `compression` and `extension`
solve for the measured nose and the chosen tail length, and `pause_smooth` moves the flat
shoulder back to erase the corner at no cost, since the width ceiling is unchanged.

`pause_smooth` is **a convention, not a derived value** — the residual against the
literature target is nearly flat in it (Venus RMS 18.6% at 0 against 18.5% at the optimum),
because removing the corner is a C¹ continuity property rather than a fit. The convention is
**`pause_smooth` = 0.5 × `pause_radius`**, adopted because the shallow optima computed
independently for three bodies land at 0.50, 0.54 and 0.57 × radius (Venus, Mars, Mercury).
`compression` is then re-solved so the nose stays exact at that smoothing.

| | radius | compression | extension | smooth | waist |
|---|---|---|---|---|---|
| Venus | 1.14 | 1.0151 | 0.0567 | 0.57 | 0 |
| Mars | 1.47 | 1.0684 | 0.0737 | 0.735 | 0 |

Nose (1.055 / 1.285) and terminator (1.13 / 1.47) come out exact, the tail closes at
20 R_p, and the bulge is 0.000%. The cost is wake width: against the measured cone the
boundary is 15% narrow at 2 R_p, 33% at 5 and 54% at 10 — accepted, because no-bulge
outranks wake fidelity here, and because every Shue parameterization does far worse
(−83% to −100%; see Part A).

**Shue-native pause** (`pause_shue`, `pause_nose` = r0, `pause_alpha` = α,
`pause_tail` = L). Kerbalism's pause is a sphere with piecewise x-scaling, which is
too blunt at the nose, pins the widest cross-section at the body plane, and closes
the tail into a spindle — three coupled fields faking what Shue et al. 1997/1998
([`1997JGR...102.9497S`](https://ui.adsabs.harvard.edu/abs/1997JGR...102.9497S) / [`1998JGR...10317691S`](https://ui.adsabs.harvard.edu/abs/1998JGR...10317691S)) do with two physical
ones. The adopted form is the **softened Shue**, a single C∞ closed curve:

    r(θ) = r0 · [ (1+ε) / (ε + cos²(θ/2)) ]^α        ε = 1 / ( (L/r0)^(1/α) − 1 )

`ε → 0` recovers exact Shue; `ε > 0` closes the tail at `r(180°) = L` with zero
slope and no join anywhere. Derivation of the three fields: **r0** is the Part A
Chapman–Ferraro nose directly (no compression-ratio encoding); **α** comes from the
Shue 98 fit against ram pressure and IMF `Bz` (0.58 is the quiet-wind default, and
`α ≥ 0.5` means an intrinsically open tail — closure is the `ε` term's job, not
α's); **L** is where the lobe field becomes GCR-irrelevant. Legacy conversion is
free: `α = log₂(compression)`, `r0 = pause_radius / compression`,
`L = pause_radius / extension`. It is shape-faithful for Earth-style configs only —
RSS Jupiter's `compression` 1.05 converts to α 0.07, an unphysically spherical
dayside, so giants need α re-tuned after conversion rather than converted blindly.
(An earlier revision of this paragraph claimed giant magnetopauses are never
fitted in the Shue form. That was wrong and is retracted — see the fitted α table
below.)

**Fitted α by body.** Use a published α wherever one exists; only fall back to the
compression conversion when none does, and say so.

| Body | α | Source |
|---|---|---|
| Earth | 0.58 (quiet wind; Dp/Bz-dependent) | Shue 1998, [`1998JGR...10317691S`](https://ui.adsabs.harvard.edu/abs/1998JGR...10317691S) |
| Mercury | **0.5**, `R_ss` 1.45 R_M | Winslow 2013, [`2013JGRA..118.2213W`](https://ui.adsabs.harvard.edu/abs/2013JGRA..118.2213W) — MESSENGER crossings fitted in exactly this form |
| Jupiter | **α = 0.28 + 1.08·p_SW** (nPa), with `r_SS = 38.0·p_SW^−0.25` R_J → 0.31–0.42 across the observed pressure range | Rutala 2025, [`2025JGRA..13033842R`](https://ui.adsabs.harvard.edu/abs/2025JGRA..13033842R) / [2502.09186](https://arxiv.org/abs/2502.09186), their "S97*" form, Table 2 |
| Saturn | Shue-form fit exists; flaring **decreases** with rising Dp, size ∝ Dp^−1/4.3 | Arridge 2006, [`2006JGRA..11111227A`](https://ui.adsabs.harvard.edu/abs/2006JGRA..11111227A) — coefficients are in the paywalled text, not yet pulled |
| Uranus, Neptune | no Shue-form fit found | — |

The instructive part is the *direction*: Jupiter's flaring is **smaller** than
Earth's (0.31–0.42 against 0.58), because a rotation-dominated, plasma-inflated
magnetosphere sits closer to an axisymmetric ellipsoid than Earth's does. So a
giant α below Earth's is not the error — reading it off `pause_compression` is,
since that number is an authoring choice with no fit behind it. Jupiter's older
polynomial model (Joy 2002, [`2002JGRA..107.1309J`](https://ui.adsabs.harvard.edu/abs/2002JGRA..107.1309J)) and Saturn's
pressure-balance shape (Kanani 2010, [`2010JGRA..115.6207K`](https://ui.adsabs.harvard.edu/abs/2010JGRA..115.6207K); Achilleos 2008,
[`2008JGRA..11311209A`](https://ui.adsabs.harvard.edu/abs/2008JGRA..11311209A)) remain the alternatives where a Shue-form α is not
wanted.

**`pause_offset`** is the cheap fallback if the full Shue mode is rejected: shift
the sphere centre tailward before the scaling (`p.x += pause_offset`), which fixes
the "widest at the body plane" defect in one line. A least-squares fit against the
softened Shue curve for Proxima c (nose 11.905, α 0.5, tail 125) reproduces the
nose, the body-plane width, the maximum width and the tail closure within a few
percent at `pause_offset` 19.7 / radius 21.5 / compression 0.68 / extension 0.204.
Every shipped stock and ROKerbalism pause underrepresents tail width the same way
(Earth flank 15 vs an observed 25–30 R_E tail radius), so this is a general defect,
not a NearStars quirk.

## Part D — moon ↔ parent interaction (embedded magnetospheres)

A moon orbiting *inside* a giant's magnetosphere is a common NearStars case (every
A b moon). It is not a scaled-down planet: three couplings dominate, all
radiation-relevant, and the moon's *own* field is a minor player.

1. **The moon lives inside the parent's belt.** The radiation the moon's surface
   sees is overwhelmingly the *parent's* trapped flux at the moon's L-shell — not
   anything the moon generates. So the first question is always *where in the
   parent's belt does the moon sit* (orbital distance in R_parent, bounded by the
   parent standoff from Part A): a moon deep in the belt is baked (Io; A b I,
   1.54 R_p), a moon in a belt gap is spared (A b III, 3.53 R_p). The moon's own
   field only *modulates* this ambient dose by shielding.

2. **The moon is a loss (or source) term for the parent's belt.** A solid moon or
   ring **absorbs** trapped particles sweeping past it, carving depletion corridors
   and, for a whole moon+ring system, pulling the parent's belt well *below* its
   Kennel–Petschek ceiling (Cooper 1983 — Saturn is the archetype, its rings and
   moons gut its belts). This is why a heavily-mooned giant is **not** automatically
   Jupiter-class: the moons + ring are a large distributed sink. Conversely a
   volcanic moon is a **source** — Io / A b I feed a plasma torus that drives the
   belt up toward the ceiling (Bagenal 1994). The same moon can be both: A b I
   feeds the torus globally while sweeping particles locally.

3. **The moon's own mini-magnetosphere** (only if it has an intrinsic dynamo).
   Its standoff balances the moon's field against the **parent's co-rotating
   magnetospheric plasma**, not the stellar wind — Part A with `P_ram` = the parent
   plasma. Ganymede is the sole Solar-System example (Kivelson 1996). Properties:
   - **Small and partly open.** The parent's field threads the moon; where the
     moon's field is only a few× the local parent field, field lines reconnect and
     the magnetosphere leaks at the poles (Ganymede: ~6× local Jovian field →
     standoff ~2 R_G, open polar caps). A stronger moon field → a larger, less-leaky
     mini-magnetosphere.
   - **Own belt is weak and source-starved.** The closed-field trapping volume is
     tiny and the only sources are inward diffusion from the parent's belt (low if
     the moon is in a gap) + CRAND from any atmosphere. The own belt therefore rarely
     reaches its K–P ceiling — it is **source-limited, not field-limited**, and is a
     single narrow belt (no room for Earth's two).
   - **Net role = shield, not generator.** The mini-magnetosphere's main effect on
     surface habitability is deflecting the *parent's* belt flux; the particles it
     does trap and precipitate feed aurorae rather than baking the ground. An
     intrinsic moon field is protective, not a self-inflicted hazard.

**Strong-field embedded moon (a distinct sub-regime — the Ganymede analogy breaks).**
The bullets above assume a *weak* moon field (Ganymede, ~6× local → leaky, negligible
own belt). A moon with an intrinsically **planet-class dynamo** — Earth-class or stronger
in *absolute* terms, not merely a few× the local parent field — is a qualitatively
different case that must **not** be forced onto the Ganymede template:

- **Small size, opposite cause.** In isolation such a moon would carry an *Earth-plus*
  magnetosphere (its standalone standoff, moon field vs stellar-wind ram, exceeds
  Earth's). Embedding then compresses it, because the external pressure is now the
  parent's **local magnetic pressure** `B_parent²/2μ₀`, which deep in a giant's field
  is *orders of magnitude* above the stellar-wind ram — so the standoff collapses to a
  few moon-radii **regardless of how strong the moon's field is**. The compact size is
  *imposed by the high-pressure environment*, not by a weak field. The field-crossover
  standoff is `R_mp/R_moon ≈ (B_eq^moon / B_parent^local)^(1/3)` (the radius where the
  moon's dipole magnitude equals the ambient parent field); the co-rotating plasma ram
  trims it slightly further.
- **Belt is Earth-*kind*, not Ganymede-negligible.** A high dominance ratio (≳15–20×)
  gives *mostly closed* field lines — small polar cusps, little reconnection leak — so a
  genuine closed trapping volume exists; and a **thick atmosphere supplies CRAND**
  (Lenchek 1961), the same internal proton source that fills Earth's inner belt. A real
  inner belt therefore forms, unlike Ganymede's. Two parent effects still *moderate* it:
  the parent magnetosphere **screens galactic cosmic rays**, throttling the CRAND driver,
  and a belt-gap orbit starves radial diffusion. Net intensity is **modest but
  non-negligible** — well below an unshielded Earth, well above Ganymede. Still one belt
  (the compressed volume has no room for Earth's two).
- **Net role = strong shield + a real orbital-altitude belt.** The large dominance ratio
  makes the shield robust (surface dose ≈ the ambient parent flux at the moon's L-shell,
  heavily reduced); the CRAND belt it sustains is a hazard for *orbiting* craft, not the
  surface, and its precipitation drives a genuine auroral oval. Heller & Zuluaga 2013
  ([`2013ApJ...776L..33H`](https://ui.adsabs.harvard.edu/abs/2013ApJ...776L..33H), arXiv 1309.0811) frame exactly this shield-vs-belt tension for
  exomoons — and note that formation models make an Earth-mass, strong-field moon
  *unlikely*, so this sub-regime is physically coherent but **observationally
  unprecedented** (a fiction-premise regime; flag confidence low, and never claim a
  Solar-System exemplar — Ganymede is the only real intrinsic-dynamo moon and it is weak).

**Kerbalism mapping (embedded moon):** give the moon its own compact `RadiationModel`
(small `pause_radius` in moon radii; a single narrow belt) + a `RadiationBody` with a
small stock-scale `radiation_pause` (~−0.01; the shield is the *presence* of a pause at
`pause_radius`, not a big value). The moon's net surface dose = the parent's belt at its
L-shell, reduced by its own pause. For `radiation_inner`, split by sub-regime: a
**weak-field** moon (Ganymede) is source-starved → *weak* (~0.2× stock Kerbin); a
**strong-field** moon (A b III) sustains a real CRAND belt → *modest* (~0.3–0.5× Kerbin),
GCR-screened below Earth but well above the Ganymede-negligible value. Neither is a field
readout (Part B); both are the source–loss regime call.

**Worked (A b III = strong-field, vs Ganymede = weak-field):** A b III (75 µT eq,
3.53 R_p, in A b's belt gap) → field ~19× the 3.9 µT local parent field. In
isolation it would carry a magnetosphere *bigger than Earth's* (standalone standoff
~17 R_moon vs A b's stellar-wind ram); embedded, the parent's local magnetic
pressure (~6 µPa, ~3000× a solar-wind ram) compresses it ~7× to a field-crossover
standoff `(75/3.9)^(1/3) ≈ 2.6 R_moon`. The high 19× dominance keeps it mostly closed,
so its thick habitable atmosphere sustains a **real CRAND inner belt**, not a
Ganymede-negligible one — `radiation_inner ≈ 4` rad/h (~0.4× stock Kerbin's 10.4:
GCR-screened by A b + gap-starved, but a genuine Earth-*kind* belt),
`radiation_pause ≈ −0.01`. Ganymede (0.72 µT, ~6× local Jovian, no atmosphere) →
standoff ~2 R_G, open polar caps, a negligible own belt. **Both are shields, not
generators for the surface**: A b III's habitability rests on the (gap + shield)
ambient reduction, and its CRAND belt is an orbital-altitude hazard that feeds the
aurora — not a surface one.

## Validation

- **Earth**: B_eq = 31 µT, solar-wind P_ram ≈ 2 nPa → R_mp/R_p = [2²·(3.1e-5)²/(2μ₀·2e-9)]^(1/6) ≈ **9.6** — matches the observed ~10 R_E sub-solar magnetopause. Inner belt ~1.2 R_E (CRAND protons), outer ~3–7 R_E (diffusion + chorus), intensity near the K–P ceiling. ✓
- **Jupiter**: the field alone (~4.3 G equatorial) would not predict the extreme belts; the Io plasma source drives them to (and past) the K–P limit for electrons — the textbook proof that intensity ≠ f(B). ✓
- **A b** (NearStars): 170 µT vs α Cen A wind ram 0.38 nPa → R_mp ≈ **22 R_p** (the Phase 4 board's independent 23.5 R_p, same balance). ✓

## Domain of validity: regimes

1. **Dipolar intrinsic** (Earth, A b III): standoff formula applies; belts on
   L-shells; K–P-capped if the source is strong.
2. **Multipolar intrinsic** (Uranus/Neptune, Proxima c; rocky multipolar regime
   with `Ro_ℓ > 0.12`): offset/tilted field → **asymmetric, patchy belts** and
   an offset auroral oval. The standoff formula is only approximate, and here the
   **polar-to-equatorial ratio ≠ 2** genuinely encodes the multipole content —
   the one case where carrying both fields is informative rather than redundant.
3. **Embedded moon** (a moon inside a giant's magnetosphere): the standoff balances
   against the **parent's co-rotating magnetospheric plasma / field**, not the stellar
   wind; the result is a mini-magnetosphere. Belt dose at the moon is set by the
   *parent's* belt at that L-shell (a loss/source term for the parent), plus the moon's
   own shielding. Two sub-regimes (see Part D):
   - **3a weak-field** (Ganymede, Kivelson 1996 [`1996Natur.384..537K`](https://ui.adsabs.harvard.edu/abs/1996Natur.384..537K)): a few× local →
     leaky, open polar caps, a negligible own belt. Pure shield.
   - **3b strong-field** (planet-class dynamo, e.g. A b III; Heller & Zuluaga 2013
     [`2013ApJ...776L..33H`](https://ui.adsabs.harvard.edu/abs/2013ApJ...776L..33H)): intrinsically Earth-plus but compressed by the parent's
     magnetic pressure to a few R_moon; ≳15–20× dominance → mostly closed → a real
     CRAND belt (if it has an atmosphere), moderated by parent GCR-screening. Strong
     shield **plus** a genuine orbital-altitude belt. No Solar-System exemplar (low conf).
4. **Induced / no dynamo** (Venus, Io, a dead rocky planet) — recipe in Part A's
   induced-magnetosphere subsection: no intrinsic trapping,
   no belts; the interaction is ionospheric/induced and the surface dose is the
   direct wind + GCR flux.
5. **Weak/airless**: `B_eq < 0.1× Earth` → no stable belts; surface dose direct.

## Worked examples (NearStars)

- **A b**: 170 µT → R_mp ≈ 22 R_p; **all five moons orbit inside the
  magnetosphere**. Belt intensity is a *source − loss* story, not a field readout:
  A b I's extreme volcanism (~820× Io) feeds an intense inner belt (source), while
  the ring + five moons sweep particles (loss) — but A b I's volcanism (~820× Io) is the
  far bigger term, so A b is **source-dominated like Jupiter, not ring-swept like
  Saturn**. The Kerbalism template is Jupiter (RSS): a strong A b I-fed *inner* belt
  (`radiation_inner` ~300, Jupiter's value, or higher), a lesser outer belt, a large
  `pause_radius`, and the small stock-scale `radiation_pause` (~−0.01). The design's core
  is exactly this: an intensified inner belt bakes the inner moons (A b I >4500 rem/day),
  while habitable A b III survives in a gap on its own strong-field shielding.
- **A b III** (embedded, **strong-field** sub-regime 3b — *not* a Ganymede analog):
  own 75 µT dipole → intrinsically an Earth-plus magnetosphere (standalone ~17 R_moon),
  compressed ~7× to a ~2.6 R_moon mini-magnetosphere *inside* A b's field. It
  sits in the **gap between A b's two belts** and its own field adds shielding →
  the physical basis for habitability. The high 19× dominance + thick atmosphere sustain
  a real CRAND belt (`radiation_inner ≈ 4` rad/h, an orbital hazard feeding the aurora,
  not a surface one). Standoff is set against A b's local field, not the stellar wind.
- **Proxima b** (weak dipole ~0.06–0.1 ℳ⊕): a small magnetosphere, standoff only a
  few R_p; belts marginal; surface dose dominated by the direct M-dwarf wind + flares.
- **Proxima c** (ice-giant, offset/tilted multipolar): asymmetric belts, offset oval;
  standoff formula approximate; the tilt (47°) drives off-axis aurorae.

Confidence: standoff geometry is **medium** (robust `^(1/6)` law, validated on
Earth/Polyphemus); belt intensity is **low** by nature — it depends on source and
loss terms that are themselves uncertain for exoplanets, which is exactly why it is
a documented regime call rather than a computed number.

## Citations

- **Chapman & Ferraro 1931**, Terr. Magn. Atmos. Electr. 36, 77 ([`1931TeMAE..36...77C`](https://ui.adsabs.harvard.edu/abs/1931TeMAE..36...77C)).
  Origin of the magnetopause / pressure-balance concept.
- **Shue et al. 1997 / 1998**, JGR 102, 9497 ([`1997JGR...102.9497S`](https://ui.adsabs.harvard.edu/abs/1997JGR...102.9497S)) / JGR 103, 17691
  ([`1998JGR...10317691S`](https://ui.adsabs.harvard.edu/abs/1998JGR...10317691S)). Empirical magnetopause standoff + shape under varying wind.
- **Kennel & Petschek 1966**, JGR 71, 1 ([`1966JGR....71....1K`](https://ui.adsabs.harvard.edu/abs/1966JGR....71....1K)). The stably-trapped
  flux limit — the source-independent ceiling on belt intensity. Load-bearing for Part B.
- **Summers, Tang & Thorne 2009**, JGRA 114, A10210 ([`2009JGRA..11410210S`](https://ui.adsabs.harvard.edu/abs/2009JGRA..11410210S));
  **Summers et al. 2014**, JGRA 119, 6313 ([`2014JGRA..119.6313S`](https://ui.adsabs.harvard.edu/abs/2014JGRA..119.6313S)).
  The relativistic K–P formulation (eqs A1–A8) and the ~E⁻¹ limited spectrum
  (relativistic coefficient 2× non-relativistic). Both paywalled, no preprint —
  equations recovered via the Mauk & Fox Zenodo software below.
- **Mauk & Fox 2010**, JGRA 115, A12220 ([`2010JGRA..11512220M`](https://ui.adsabs.harvard.edu/abs/2010JGRA..11512220M)).
  The cross-planet differential K–P framework: Earth/Jupiter/Uranus at the cap,
  Neptune below (injection-starved), Saturn below (material losses). Paywalled;
  **their open implementation** ([Zenodo 10.5281/zenodo.4782323](https://zenodo.org/records/4782323),
  [`2021zndo...4782323M`](https://ui.adsabs.harvard.edu/abs/2021zndo...4782323M)) is cached (`_papers/mauk_fox_KP.nb` + run) and ported to
  `scripts/refs/kp_limit.py` (validated to ≤0.05 % on 11 printed intermediates).
- **Mourenas et al. 2024**, JGRA 129, e32193 ([`2024JGRA..12932193M`](https://ui.adsabs.harvard.edu/abs/2024JGRA..12932193M)).
  Independent confirmation of the ~3 wave-power-gain criterion (ELFIN).
- **Seltzer 1979 / 1992** (SHIELDOSE / SHIELDOSE-2,
  [`1979ITNS...26.4896S`](https://ui.adsabs.harvard.edu/abs/1979ITNS...26.4896S),
  [`1992STIN...9315580S`](https://ui.adsabs.harvard.edu/abs/1992STIN...9315580S)).
  The standard electron/proton fluence → dose-behind-Al transport — the reason
  dose contrast is set by spectral hardness, not the ~1 MeV differential cap.
- **Schulz & Lanzerotti 1974**, *Particle Diffusion in the Radiation Belts* ([`1974pdrb.book.....S`](https://ui.adsabs.harvard.edu/abs/1974pdrb.book.....S)).
  Radial-diffusion transport that populates the belts.
- **Lenchek et al. 1961**, JGR 66, 4027 ([`1961JGR....66.4027L`](https://ui.adsabs.harvard.edu/abs/1961JGR....66.4027L)). CRAND inner-belt source.
- **Divine & Garrett 1983**, JGR 88, 6889 ([`1983JGR....88.6889D`](https://ui.adsabs.harvard.edu/abs/1983JGR....88.6889D)); **Bagenal 1994**,
  JGR 99, 11043 ([`1994JGR....9911043B`](https://ui.adsabs.harvard.edu/abs/1994JGR....9911043B)). Jovian radiation + the Io internal plasma
  source — the canonical "intensity set by source, not field" case.
- **Ripoll et al. 2016**, GRL 43, 5616 ([`2016GeoRL..43.5616R`](https://ui.adsabs.harvard.edu/abs/2016GeoRL..43.5616R)); **Cheng et al. 1987**, JGR 92,
  15315 ([`1987JGR....9215315C`](https://ui.adsabs.harvard.edu/abs/1987JGR....9215315C)). Where each belt's flux actually peaks — Earth's inner-belt
  peak and slot, and Uranus' broad maxima between moon-swept minima. These are the
  profile shapes the `radiation_*_gradient` recipe reads `d*` from.
- **Ginet et al. 2013**, SSRv 179, 579 ([`2013SSRv..179..579G`](https://ui.adsabs.harvard.edu/abs/2013SSRv..179..579G)). AE9/AP9/SPM, the current
  standard trapped-flux specification — the successor to AE8/AP8 and the model to read a
  radial profile off for Earth. Cite this rather than "AP9" loosely.
- **Mead 1964**, JGR 69, 1181 ([`1964JGR....69.1181M`](https://ui.adsabs.harvard.edu/abs/1964JGR....69.1181M)); **Mead & Fairfield 1975**, JGR 80,
  523 ([`1975JGR....80..523M`](https://ui.adsabs.harvard.edu/abs/1975JGR....80..523M)); **Tsyganenko 2002**, JGRA 107, 1179
  ([`2002JGRA..107.1179T`](https://ui.adsabs.harvard.edu/abs/2002JGRA..107.1179T)). How the boundary currents deform the inner field — Mead for the
  Chapman–Ferraro solution's shape (compression on both day and night sides), Mead &
  Fairfield for the distributed tail currents the theory understates, Tsyganenko for the
  modern quantitative standard. Mead's *description* is still the canonical statement and
  is cited as such today; its *coefficients* are superseded by the T-family. Load-bearing
  for the belt `*_compression`/`*_extension` recipe.
- **Pfitzer et al. 1969**, JGR 74, 4687 ([`1969JGR....74.4687P`](https://ui.adsabs.harvard.edu/abs/1969JGR....74.4687P)); **Öztürk & Wolf 2007**,
  JGRA 112, A07207 ([`2007JGRA..112.7207O`](https://ui.adsabs.harvard.edu/abs/2007JGRA..112.7207O)). Drift-shell splitting in the distorted
  magnetosphere, observed and then mapped near the dayside magnetopause — the outer limit
  of the asymmetry recipe, where shells stop being closed surfaces at all.
- **Thorne 2010**, GRL 37, L22107 ([`2010GeoRL..3722107T`](https://ui.adsabs.harvard.edu/abs/2010GeoRL..3722107T)); **Ripoll et al. 2020**,
  JGRA 125, e26735 ([`2020JGRA..12526735R`](https://ui.adsabs.harvard.edu/abs/2020JGRA..12526735R)). Wave–particle acceleration and loss;
  modern belt-dynamics review.
- **Cooper 1983**, JGR 88, 3945 ([`1983JGR....88.3945C`](https://ui.adsabs.harvard.edu/abs/1983JGR....88.3945C)). Ring/moon absorption as a
  belt loss — the A b ring + moons case.
- **Kivelson et al. 1996**, Nature 384, 537 ([`1996Natur.384..537K`](https://ui.adsabs.harvard.edu/abs/1996Natur.384..537K)). Ganymede's
  embedded magnetosphere — the weak-field embedded-moon (sub-regime 3a) exemplar.
- **Heller & Zuluaga 2013**, ApJ 776, L33 ([`2013ApJ...776L..33H`](https://ui.adsabs.harvard.edu/abs/2013ApJ...776L..33H), arXiv
  **[1309.0811](https://arxiv.org/abs/1309.0811)**). Exomoon magnetic shielding within a
  giant planet's magnetosphere — the shield-vs-radiation-belt tension, and the note that
  Earth-mass strong-field moons are formation-unlikely. Grounds the strong-field
  embedded-moon (sub-regime 3b) as coherent-but-unprecedented (fiction-premise).
- **Bertucci et al. 2011**, SSRv 162, 113 ([`2011SSRv..162..113B`](https://ui.adsabs.harvard.edu/abs/2011SSRv..162..113B)); **Luhmann 1991**, SSRv
  55, 201 ([`1991SSRv...55..201L`](https://ui.adsabs.harvard.edu/abs/1991SSRv...55..201L)); **Brace et al. 1980**, JGR 85, 7663
  ([`1980JGR....85.7663B`](https://ui.adsabs.harvard.edu/abs/1980JGR....85.7663B)); **Zhang et al. 2009**, GRL 36, L20203
  ([`2009GeoRL..3620203Z`](https://ui.adsabs.harvard.edu/abs/2009GeoRL..3620203Z)); **Egan et al. 2019**, MNRAS 488, 2108
  ([`2019MNRAS.488.2108E`](https://ui.adsabs.harvard.edu/abs/2019MNRAS.488.2108E)). The induced-magnetosphere branch: the review, the Venus
  ionospheric field, the measured ionopause heights, its disappearance under a radial
  IMF (with the close-in-exoplanet implication), and the weak-dipole crossover where a
  field starts shielding instead of enhancing escape.

- **Griessmeier et al. 2004**, A&A 425, 753 ([`2004A&A...425..753G`](https://ui.adsabs.harvard.edu/abs/2004A%26A...425..753G)); **Vidotto et al.
  2013**, A&A 557, A67 ([`2013A&A...557A..67V`](https://ui.adsabs.harvard.edu/abs/2013A%26A...557A..67V)). Exoplanet magnetosphere size vs
  stellar wind / tidal locking — the close-in-planet standoff application.

## Related

- [`surface-radiation-dose-methodology.md`](surface-radiation-dose-methodology.md) —
  the **surface** dose from stellar particle events arriving through the atmosphere. This
  doc owns the trapped-belt dose; that one owns what reaches the ground, and the two are
  separate chains that must not be conflated.
- [`rocky-planet-dynamo-methodology.md`](rocky-planet-dynamo-methodology.md) and
  [`planetary-dynamo-scaling.md`](planetary-dynamo-scaling.md) — supply the `B_eq`
  this method consumes.
- `../../.claude/skills/nearstars-phase3/references/mod-grounded-fields.md` — the
  Kerbalism `RadiationBody`/`RadiationModel` field schema this method emits into.
- `methodology-index.md` — the living index of all derived-value recipes.
