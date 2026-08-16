<!-- 자기권 레시피의 증거·도출 기록. Part 1 = 태양계 7천체 스톡 대 물리 감사, Part 2 = 도출 과정과 기각된 접근 -->
# Magnetosphere evidence and derivation record

The evidence and derivation record behind the magnetosphere-geometry recipe, in two halves.
**Part 1** is a body-by-body audit of every Solar-System object that has a **magnetosphere
with trapped-particle belts** (or a magnetosphere at all), comparing the **Kerbalism /
ROKerbalism stock cfg** against the **real, ADS-grounded physics**. **Part 2** is the
derivation record: how the recipe's harder numbers were reached, and mostly the approaches
tried and rejected on the way.

The split exists because the methodology had become half recipe and half working notes. A
reader applying the recipe should never have to read a dead end; a session about to
re-derive something should be able to find out it has already been tried. Every block in
Part 2 is reachable from a one-line pointer in the methodology. It exists to
calibrate the NearStars magnetosphere-geometry recipe against real bodies before
that recipe emits belts for fictional ones, and to feed the physics-accurate cfg
values back where the stock model is a rough placeholder.

Each body below carries its **two cross-sections**, both the in-game `RadiationModel` SDF:
**stock** = the shipped
cfg (verified 2026-07-24 against `KSP-RO/ROKerbalism` `System/Radiation.cfg` +
`Support/RSS.cfg`), **physical** = the same SDF with its six belt-shape parameters
**numerically fitted** (`scripts/viz/fit_belts.py`, Nelder-Mead multi-start) to the real
dipole drift-shell region between the ADS-anchored field lines (r = L cos²λ, loss-cone
cut at the atmosphere top). Fit quality is stated per belt as IoU (cross-section area
overlap): **≥ 0.96 everywhere** except Jupiter's flat magnetodisc (0.87, a torus-model
ceiling). The fitted parameter sets live in the render driver; two-shell tori still
can't capture every real feature (moon/ring gaps, time variation), noted below.
The renderer is `scripts/viz/render_belts.py` (+ `render_belts_bodies.py` driver); the SDF
is reproduced from [`src/Kerbalism/Radiation/Radiation.cs`](https://github.com/Kerbalism/Kerbalism/blob/master/src/Kerbalism/Radiation/Radiation.cs)
([Kerbalism](https://github.com/Kerbalism/Kerbalism), public domain / [Unlicense](https://github.com/Kerbalism/Kerbalism/blob/master/LICENSE)); see
[`planetary-magnetosphere-geometry-methodology.md`](planetary-magnetosphere-geometry-methodology.md)
for the field-shape schema.

**Reading the renders.** Colour = dose (inferno), cyan = the cfg's magnetopause, orange
dashed = the **Shue magnetopause** for the same standoff (the empirical spacecraft-fit
shape, drawn for comparison; the dot marks `r0`), grey = the body, rings = body radii,
star toward +x. Belts are drawn in the tilted magnetic frame and the magnetopause in the
star-aligned one, which is how Kerbalism itself evaluates them — it renders and doses the
pause from `Gsm_space(rb, false)` and reserves the tilted frame for the belts. Since
2026-08-13 the two fields that shape a belt's *interior* are derived rather than copied
from stock (the dose ramp `radiation_*_gradient` and the belt `*_compression`/`*_extension`);
the recipes, and what they overturn, are in the methodology doc's Part C. Jupiter's and
Saturn's magnetopause stands off at 63 and 24 body radii, far enough that fitting it in
frame would shrink the belts past readability, so those two stay zoomed on the belts.

**The magnetopause flaring is grounded as of 2026-08-14.** Every magnetized body's physical
preset now sets `pause_compression` = `2^α` for a **full-text-verified** Shue flaring
parameter, so `log₂(compression)` recovers α exactly and `pause_radius` = nose × `2^α`:
Mercury 0.500 (Winslow 2013), Earth 0.580 (Shue 1998 eq. 11), Jupiter 0.423 (Rutala 2025
S97*), Saturn 0.736 (Kanani 2010, cross-checked against Arridge 2006 to 0.0002 at the same
nose). Uranus and Neptune have no published fit and take Earth's 0.580 **by analogy**,
justified by Voyager 2 finding them the emptiest magnetospheres measured — no Io- or
Enceladus-class plasma source, so their loading sits nearer Earth's than the gas giants'.
The previous `compression` 1.2 on all four outer planets was a placeholder, and it
understated the flank by 25–39%. Derivations, citations and the reason no α(pressure) law
extrapolates are in the methodology's Part A. Tail length is now measured where a measurement
exists: **Mercury 2.9 R_M** (Winslow 2013, flaring ceases by ~2 R_ss) and **Earth 120 R_E**
(Slavin 1985, 120 ± 10). Both come with a published tail width, and the α-surface reproduces
both without being fitted to them — 2.71 R_M against Winslow's ~2.7 at x = −3, and 28.1 R_E
in radius against Slavin's 60 ± 5 diameter. The four outer planets keep inherited
placeholders; the two anchors are 5–6× apart in nose units where α explains only 3.6×, and
Winslow states the governing factors "are not well understood", so nothing supports an
extrapolation.

# Part 1 — per-body evidence

## Scope — only magnetized bodies

Belts require an intrinsic dynamo strong enough to trap particles. In the Solar
System that is **7 bodies**: Earth, Jupiter, Saturn, Uranus, Neptune (planetary
dynamos), Mercury (tiny), and Ganymede (embedded moon dynamo). **Venus, Mars, the
Moon, Io, Europa, Callisto, Titan, Triton, Pluto** have no intrinsic global field →
no belts, so their radiation is the direct wind/GCR flux. They are out of scope for
the belt audit.

**They are not cfg-less, though** (corrected 2026-08-14). Kerbalism gives several of
them a *pause-only* `RadiationModel` — a boundary with no belt fields — and those
are worth knowing before assuming a body has nothing:

| Model | Shape | Used by | Reading |
|---|---|---|---|
| `ionosphere` | pause 1.1 R, extension 0.2, no belts | **Venus** (`radiation_pause` −0.005), Titan (RSS.cfg) | the induced magnetosphere: no dynamo, so the solar wind ionizes the upper atmosphere into a thin conducting shell |
| `irregular` | pause 1.25 R, compression 1.1, extension 0.75, **`pause_deform` 0.1** | **Mars** (upstream `Duna`, `radiation_pause` −0.003) | crustal remanent magnetism — the deform term is what makes it read as a lumpy, patchy weak field rather than a dipole |
| `anomaly` | pause 0.5 R, extension 0.8, height 0.45, `pause_deform` 0.05 | Io | a sub-surface-scale patch, not a magnetosphere |
| `solidiron` / `metallic` | small pause shells | Bop; unassigned in stock | placeholders for dense airless bodies |
| `surface` | pause 1.075 R | (abused as a surface-dose shell) | not a field at all |

### Venus — the induced branch, derived

| Stock | Physical |
|---|---|
| ![venus Stock](../img/belts/venus_stock.png) | ![venus Physical](../img/belts/venus_phys.png) |

The physical preset is computed with the induced-magnetosphere recipe rather than
the dipole one. Venus' mean ionopause sits 330 km above the subsolar point, 700 km
at the dusk terminator and 1000 km at dawn (Brace 1980, [`1980JGR....85.7663B`](https://ui.adsabs.harvard.edu/abs/1980JGR....85.7663B)), which
on `R_V` 6051.8 km is a **nose at 1.055 R_V and a terminator mean of 1.140 R_V**.
Mapped through the cfg semantics (`nose = pause_radius/compression`,
flank = `pause_radius`, tail = `pause_radius/extension`) that is
`pause_radius` **1.14**, `compression` **1.0151**, `extension` **0.0072038**, plus the two
generalizing fields `pause_smooth` **0.57** and `pause_waist` **0** (neither exists in stock
Kerbalism; see below). Nose 1.055 and terminator 1.13 come out exact, and the tail closes at
158 R_V under the project-wide `L` = 150 × nose convention — comfortably beyond the farthest
confirmed crossing of the induced magnetospheric boundary at 20 R_V (Edberg 2024,
[`2024JGRA..12932603E`](https://ui.adsabs.harvard.edu/abs/2024JGRA..12932603E), [2410.21856](https://arxiv.org/abs/2410.21856)). No belts, and
`radiation_pause` stays at the shipped −0.005: an induced boundary screens GCR far less than
a dipole magnetopause.

Against stock, the derived dayside hugs the planet more tightly (1.05 vs a uniform 1.1 R)
and the tail runs far longer (158 vs 5.5 R_V).

**The shape is the stock function generalized — the fallback, not the default.** Project
policy is to use Shue wherever a fitted α exists (Earth, Mercury, Jupiter) and to fall back
to the generalized stock function only where Shue geometrically cannot represent the
boundary. Venus and Mars are that exception. The literature's own model for this boundary is
a dayside circle joined to a 5.77° nightside cone (Martinecz 2009,
[`2009JGRA..114.0B30M`](https://ui.adsabs.harvard.edu/abs/2009JGRA..114.0B30M), validated unchanged to 20 R_V by Edberg 2024), and
reproducing it would mean carrying a second shape family in-game. Instead two fields fix the
shipped function in place: `pause_smooth` removes the slope corner where the two hemispheres
meet, and `pause_waist` unpins the widest cross-section from the planet's centre. Both are
zero-default, so stock behaviour is bit-for-bit unchanged — every stock preset re-renders to
an identical PNG. Neither is read by any shipped Kerbalism yet; they wait on the Harmony
patch, and the emitter keeps them out of cfg.

The binding requirement was that **the boundary must not bulge behind the terminator**.
Since the width is `√(radius² − px²)`, it can never exceed `radius`, so setting `radius` to
the measured terminator width makes a rear bulge impossible by construction. The cost is
wake width: 15% narrow at 2 R_V, 33% at 5, 54% at 10 against the measured cone. Every Shue
parameterization does far worse there (−83% to −100%), and the full candidate table — six
shapes measured, including a conic that dipped below the planet's surface — is in the
methodology's Part A.

### Mars — the MPB dayside, derived

| Stock | Physical |
|---|---|
| ![mars Stock](../img/belts/mars_stock.png) | ![mars Physical](../img/belts/mars_phys.png) |

Mars' boundary is the **magnetic pileup boundary**, and Vignes 2000
([`2000GeoRL..27...49V`](https://ui.adsabs.harvard.edu/abs/2000GeoRL..27...49V), Table 2, direct fit over 488 MGS crossings) gives the conic
directly: `X₀` 0.78 ± 0.01, eccentricity 0.90 ± 0.01, semi-latus rectum `L`
0.96 ± 0.01, **subsolar `R_SD` 1.29 ± 0.04 R_M** and **terminator `R_TD`
1.47 ± 0.08 R_M**. Mapping those:

- `pause_radius` = flank = **1.47**, `compression` = 1.47/1.29 = **1.1395** (which
  recovers the 1.29 nose);
- the dayside overlay is a circle through those two points: **radius 1.4833 centred at
  x −0.1983**;
- the nightside is **not** taken from their conic. Vignes' own abstract calls the
  "nightside MPB position… highly variable", and Němec 2020
  ([`2020JGRA..12528509N`](https://ui.adsabs.harvard.edu/abs/2020JGRA..12528509N)) states that even the MAVEN-based models "are deemed
  unreliable beyond the terminator". Extended into that gap, their ellipse bulges to
  2.20 R_M — 1.5× the terminator width — at x ≈ −3.8 and closes at −8.8, both in a
  region with no crossings.

Instead the nightside uses Venus' measured flare scaled by terminator radius, giving
**7.49°**, on the strength of a Phobos-2 / Pioneer Venus comparison that found no
significant difference between the two planets' induced magnetotail structure
([`2001AGUSM..SM32D06K`](https://ui.adsabs.harvard.edu/abs/2001AGUSM..SM32D06K)). That is an **analogy, not a Mars measurement**, and is
labelled as one in the render. One check it was not designed to pass: at that angle the
dayside circle meets the terminator with slope 0.135 against the cone's 0.131, joining
smoothly to within 3%, but that check belongs to the circle-plus-cone form, which is not
what ships. The shipped numbers are `pause_radius` **1.47**, `compression` **1.0684**,
`extension` **0.0076265** with `pause_smooth` **0.735**, putting the tail at 193 R_M under
the same `L` = 150 × nose convention.

`pause_deform` stays at the stock `irregular` value 0.1: the crustal remanent field
is genuinely non-axisymmetric, but Vignes does not quantify that asymmetry, so the
amplitude is inherited rather than derived — flagged, not fabricated. Against stock,
the derived boundary stands further off (1.29 vs 1.25 nose, 1.47 vs a rounder
flank) and trails a much longer tail (193 vs 1.7 R_M).

Both Venus and Mars remain belt-free: no dynamo, no trapping.

**A distribution gap worth flagging.** ROKerbalism's `Support/RSS.cfg` renames
`+RadiationBody[Duna] { @name = Mars }`, but its own `System/Radiation.cfg` — which
replaces the upstream KerbalismConfig wholesale — defines no `Duna` body (verified
2026-08-14 against `KSP-RO/ROKerbalism@master`). The copy therefore has no source,
so under ROKerbalism **Mars ends up with no `RadiationBody` at all**, while upstream
Kerbalism gives it the `irregular` model. Anyone who remembers seeing Mars' lumpy
weak-field boundary in game was running the upstream config, not RSS.

## Reading the cfg correctly (two traps)

An earlier revision of this audit (and its hand-placed "physical" renders) misread two
SDF parameters; both are corrected throughout and worth recording:

1. **Belt `dist`/`radius` live in `deform_xy`-squashed coordinates.** The SDF tests
   `√((x²+z²)·deform_xy) − dist`, so a belt's *equatorial* extent is
   `(dist ± radius)/√deform_xy`, further carved by the border torus. Stock Earth's outer
   belt (2.6338/2.48, deform_xy 0.7225, border 1.4412/1.4875) actually spans
   **3.45–6.0 R_E at the equator** — close to the physical outer-belt heart (L 3–7),
   not "centred at 2.6 R_E" as a naive read of `outer_dist` suggests.
2. **`pause_radius` is not the sub-solar standoff.** Dayside x is multiplied by
   `pause_compression` before the sphere test, so nose = `pause_radius/pause_compression`,
   flank = `pause_radius`, tail = `pause_radius/pause_extension`. Stock Earth (15,
   comp 1.5) → nose exactly **10 R_E** = the Shue standoff, with flank/nose 1.5 = 2^0.585
   (Shue α). Any NearStars emit of a Chapman–Ferraro standoff must therefore set
   `pause_radius = R_mp × pause_compression`.

## Summary table — physics anchors (all ADS-pinned)

| Body | Magnetopause standoff | Dipole tilt | Offset | Belt structure | Peak dose (order) |
|---|---|---|---|---|---|
| **Earth** | ~10 R_E | 11° | small | two separated belts (D inner + hollow outer) | ~10² rad/day (peak) |
| **Jupiter** | **63 R_J** (compressed) / 92 (expanded) | 10.3° | ~0.13 R_J | dipolar inner (D-cut) + flat magnetodisc | ~10³–10⁴ rad/day |
| **Saturn** | **22–27 R_S** | **<0.007°** | 0.047 R_S N | **no classic inner belt** (rings sweep it); weak moon-chopped outer; CRAND-only | ≪ Jupiter |
| **Uranus** | **18 R_U** | **59°** | **0.3 R_U** | offset+tilted, moon-swept, helical tail | e⁻ ≥1.2 MeV |
| **Neptune** | **26.5 R_N** | **47°** | **0.55 R_N** | offset+tilted, peak L≈7, Triton cut ~14 R_N | e⁻ >1 MeV |
| **Mercury** | **1.45 R_M** (1.35–1.55) | <3° | 0.20 R_M N (484 km) | **no stable belt** — surface is the loss cone | (surface direct) |
| **Ganymede** | **~2 R_G** (upstream) | ~176° (≈anti-aligned) | — | weak embedded, **open polar caps**, source-starved | shield −50–60% of ambient |

The headline findings: **(1)** stock ROKerbalism **Earth is well-calibrated on both
character and position** once the cfg is read correctly (D-cut inner belt 1.3–2.0 R_E,
hollow outer 3.45–6.0, magnetopause nose 10 R_E) — an earlier revision claimed position
drift from the two cfg traps above, retracted; **(2)** the real stock errors are
**Jupiter** (belt ~3× too far out, no D-cut, no magnetodisc) and the **ice giants
sharing an untuned copy of the generic `saturn` model** (outer 7/7 blob spanning
0–14 R, pause 20 — only tilt/offset are per-body; Uranus `radiation_inner = 75` and
Neptune `= 39` are dead cfg, the model has `has_inner = false`); **(3)** **Saturn's
"outer-only, no inner belt"** stock choice is *physically correct* — the rings occupy
and absorb the inner-belt zone — though its 7/7 blob still floods the swept ring zone;
**(4)** **belt-intensity provenance** is tuned, not derived, everywhere.

---

## Per-body: stock cfg vs physical

Each block gives the stock `RadiationBody`/`RadiationModel` (ROKerbalism `System/
Radiation.cfg` + RSS anchors), the physical values with ADS pins, and the delta.

### Earth (calibration anchor — and, read correctly, a good one)

| Stock | Physical |
|---|---|
| ![earth Stock](../img/belts/earth_stock.png) | ![earth Physical](../img/belts/earth_phys.png) |

| Field | Stock (`earth`) | Physical | Source |
|---|---|---|---|
| pause | 15 / comp 1.5 → **nose 10 R_E** | ~10 R_E sub-solar ✓ | Shue 1997 [`1997JGR...102.9497S`](https://ui.adsabs.harvard.edu/abs/1997JGR...102.9497S), Fairfield 1971 [`1971JGR....76.6700F`](https://ui.adsabs.harvard.edu/abs/1971JGR....76.6700F) |
| inner belt | 0.813/0.70 dxy 0.572, border 0.915 → equator **1.29–2.0 R_E** | peak **L≈1.5**, ~1.1–2 R_E, lower edge ~1000 km (loss-cone-depleted below; SAA dips to ~200 km via the dipole offset) ✓ | (AP9; Ripoll 2016) |
| outer belt | 2.63/2.48 dxy 0.7225, border carve → equator **3.45–6.0 R_E** | **heart L≈4–5**, L 3–7 (≈; edge 6 vs 7) | Reeves 2013 [`2013Sci...341..991R`](https://ui.adsabs.harvard.edu/abs/2013Sci...341..991R), Thorne 2013 [`2013Natur.504..411T`](https://ui.adsabs.harvard.edu/abs/2013Natur.504..411T) |
| slot region | the gap 2.0–3.45 R_E ✓ | **L≈2–3** (hiss-cleared) | Ripoll 2016 [`2016GeoRL..43.5616R`](https://ui.adsabs.harvard.edu/abs/2016GeoRL..43.5616R) |
| radiation_inner/outer | 10.376 / 2.214 | order-consistent | — |
| geomagnetic_pole_lat / offset | 80.37 (tilt 9.6°) / 0.07 | tilt ~11° / ~0.08 R_E | IGRF (accurate) |

Read with the correct SDF semantics, the stock anchor is good on **both character and
position**: D-cut inner belt at 1.29–2.0 R_E, slot, hollow outer at 3.45–6.0, magnetopause
nose exactly 10 R_E, accurate tilt/offset, inner dose ~10.4 rad/h at the observed proton
peak. (An earlier revision of this doc claimed the pause was 1.5× generous and the outer
belt 2× inward — both were the cfg-reading traps above; retracted.) The physical render
refits the exact L-shells (inner L 1.1–2 with the ~1000 km lower boundary, outer L 3–7:
IoU 0.99/0.98); the visible deltas vs stock are small — outer edge 7 vs 6 R_E and a
slightly thicker inner crescent. The outer-belt horns keep a low (~300 km) cut — unlike
the inner belt, outer-zone electrons routinely precipitate into the bounce/drift loss
cone at low altitude (POES observations; Liu 2024
[`2024JGRA..12932171L`](https://ui.adsabs.harvard.edu/abs/2024JGRA..12932171L)).

### Jupiter

| Stock | Physical |
|---|---|
| ![jupiter Stock](../img/belts/jupiter_stock.png) | ![jupiter Physical](../img/belts/jupiter_phys.png) |

| Field | Stock (RSS `jupiter`) | Physical | Source |
|---|---|---|---|
| inner belt | 6.0/1.0 (no dxy) → equator **5–7 R_J** | dipolar shell **L 1.2–3** (peak ~1.5–2 R_J; fit IoU .98) | Divine & Garrett 1983 [`1983JGR....88.6889D`](https://ui.adsabs.harvard.edu/abs/1983JGR....88.6889D) |
| inner border | (none) | loss-cone D-cut at the atmosphere | (belt physics) |
| outer belt | 6.5/6.5 (concentric blob) | **magnetodisc slab 3–16 R_J × ±3** (half-width ~3–3.5 R_J canonical; 3–16 is a frame truncation of a disc extending past 50 R_J) (fit IoU .87 — torus ceiling) | Khurana 1989 [`1989JGR....9411791K`](https://ui.adsabs.harvard.edu/abs/1989JGR....9411791K) |
| pause | 60 / comp 1.05 → nose 57 | nose **63** (compressed; 92 expanded) | Joy 2002 [`2002JGRA..107.1309J`](https://ui.adsabs.harvard.edu/abs/2002JGRA..107.1309J) |
| radiation_inner | 300 | **~1500** (order 10³–10⁴; conf low) | Divine & Garrett 1983 |
| geomagnetic_pole_lat | −81.4 | **−80** (tilt 10.3°, reversed) | Connerney 2022 JRM33 [`2022JGRE..12707055C`](https://ui.adsabs.harvard.edu/abs/2022JGRE..12707055C) |
| geomagnetic_offset | (none) | **0.1** (eccentric dipole) | JRM33 |

Inner belt is **dipolar** (equatorial + non-equatorial electrons, pitch 0–90°;
Santos-Costa 2001 [`2001P&SS...49..303S`](https://ui.adsabs.harvard.edu/abs/2001P%26SS...49..303S)) → round, not flat. Outer belt is a **hinged
magnetodisc** (equatorially confined current sheet; Khurana 1989) → flat. Io/Amalthea/
ring absorption gaps (Santos-Costa 2001) cannot be rendered by two shells — a fidelity
ceiling. Stock puts the strong belt ~3× too far out (6 vs ~2 R_J) and omits both the
D-cut and the magnetodisc flattening.

### Saturn

| Stock | Physical |
|---|---|
| ![saturn Stock](../img/belts/saturn_stock.png) | ![saturn Physical](../img/belts/saturn_phys.png) |

| Field | Stock (`saturn` model, RSS.cfg) | Physical | Source |
|---|---|---|---|
| has_inner | false (outer only) | **false — correct** (rings absorb) | Cooper 1983 [`1983JGR....88.3945C`](https://ui.adsabs.harvard.edu/abs/1983JGR....88.3945C) |
| pause | 20 / comp 1.02 → nose 19.6 | nose **~24** (22–27 bimodal) | Achilleos 2008 [`2008JGRA..11311209A`](https://ui.adsabs.harvard.edu/abs/2008JGRA..11311209A) |
| outer belt | 7/7 → equator **0–14 R_S** (floods the swept ring zone) | shell **L 2.3–6** (fit IoU .98), moon-chopped corridors | Kollmann 2013 [`2013Icar..222..323K`](https://ui.adsabs.harvard.edu/abs/2013Icar..222..323K) |
| radiation_outer | 150 | **weak** (CRAND-only, ≪ Jupiter) | Kollmann 2017 [`2017NatAs...1..872K`](https://ui.adsabs.harvard.edu/abs/2017NatAs...1..872K) |
| dipole tilt | (near 0) | **<0.007°** (25.2 arcsec!) | Cao 2020 [`2020Icar..34413541C`](https://ui.adsabs.harvard.edu/abs/2020Icar..34413541C) |
| offset | — | 0.047 R_S north | Cao 2020 |

**Stock "outer-only, no inner belt" is physically right**: the dense A–C rings sit
exactly where an inner belt would form and absorb it (Cooper 1983); the surviving
belt is chopped into inter-moon corridors (Kollmann 2013, Roussos 2007
[`2007JGRA..112.6214R`](https://ui.adsabs.harvard.edu/abs/2007JGRA..112.6214R)). Source is passive CRAND, so intensity is orders below Jupiter
(Kollmann 2017). A thin isolated proton belt exists between atmosphere and D-ring
(Roussos 2018 [`2018Sci...362.1962R`](https://ui.adsabs.harvard.edu/abs/2018Sci...362.1962R)) — real but negligible for gameplay. Dipole is
near-perfectly axisymmetric (Cao 2020), so tilt ≈ 0.

### Uranus

| Stock | Physical |
|---|---|
| ![uranus Stock](../img/belts/uranus_stock.png) | ![uranus Physical](../img/belts/uranus_phys.png) |

| Field | Stock (generic `saturn` model, RSS.cfg) | Physical | Source |
|---|---|---|---|
| geomagnetic tilt | pole_lat 31.4 (=58.6°) | **59–60°** ✓ | Ness 1986 [`1986Sci...233...85N`](https://ui.adsabs.harvard.edu/abs/1986Sci...233...85N) |
| geomagnetic_offset | 0.3 | **0.3 R_U** ✓ | Ness 1986 |
| pause | 20 / comp 1.02 → nose 19.6 | nose **18.0 R_U** (bow shock 23.7) | Ness 1986 |
| belts | generic outer 7/7 blob (0–14 R_U); **radiation_inner 75 is dead cfg** (`has_inner = false`) | two shells **L 1.5–5 / L 5–10** bounded by moon sweeping — Miranda L 5.1 ("except inside the orbit of Miranda"), electron minima at Miranda/Ariel/Umbriel L 5.1/7.5/10.4 with broad maxima between; trapping detectable to Titania ~L 17 (fit IoU .98/.97) | Krimigis 1986, Cheng 1987 [`1987JGR....9215315C`](https://ui.adsabs.harvard.edu/abs/1987JGR....9215315C) |
| radiation_inner | 75 (unused) | e⁻ ≥1.2 MeV, p ≥4 MeV | Krimigis 1986 [`1986Sci...233...97K`](https://ui.adsabs.harvard.edu/abs/1986Sci...233...97K) |
| quadrupole | — | large (Q3 model) | Connerney 1987 [`1987JGR....9215329C`](https://ui.adsabs.harvard.edu/abs/1987JGR....9215329C) |

**Stock captures the extreme offset-tilted dipole axis** (pole_lat 31.4, offset 0.3) but
the field *shape* is an untuned copy of the generic `saturn` model (single 7/7 outer
blob, pause 20) shared verbatim with Neptune — and its `radiation_inner = 75` never
fires, since the model has no inner belt. The belt intensity is a tuned placeholder. Moons
(Miranda→Titania) sweep the belts across a huge L-range every 17.24 h (Stone 1986
[`1986Sci...233...93S`](https://ui.adsabs.harvard.edu/abs/1986Sci...233...93S)); the near-sunward spin axis winds the tail into a helix (pitch
5.5°; Behannon 1987 [`1987JGR....9215354B`](https://ui.adsabs.harvard.edu/abs/1987JGR....9215354B)). Polarity sign not stated in the primary
abstracts (not fabricated).

### Neptune

| Stock | Physical |
|---|---|
| ![neptune Stock](../img/belts/neptune_stock.png) | ![neptune Physical](../img/belts/neptune_phys.png) |

| Field | Stock (generic `saturn` model, RSS.cfg) | Physical | Source |
|---|---|---|---|
| geomagnetic tilt | pole_lat 43 (=47°) | **47°** ✓ | Ness 1989 [`1989Sci...246.1473N`](https://ui.adsabs.harvard.edu/abs/1989Sci...246.1473N) |
| geomagnetic_offset | 0.55 | **0.55 R_N** ✓ | Ness 1989 |
| pause | 20 / comp 1.02 → nose 19.6 (an earlier revision claimed 26.5 ✓ — wrong, the model is the shared `saturn` one) | nose **26.5 R_N** (bow shock 34.9) | Ness 1989 |
| belts | generic outer 7/7 blob; **radiation_inner 39 is dead cfg** (`has_inner = false`) | shells **L 1.5–5 / L 5–14** (fit IoU .98/.97), peak **L ≈ 7** | Stone 1989 [`1989Sci...246.1489S`](https://ui.adsabs.harvard.edu/abs/1989Sci...246.1489S) |
| outer cutoff | — | **~14 R_N (Triton)** | Krimigis 1989 [`1989Sci...246.1483K`](https://ui.adsabs.harvard.edu/abs/1989Sci...246.1483K) |
| quadrupole/octupole | — | quad ≈ dipole at surface | Connerney 1991 [`1991JGR....9619023C`](https://ui.adsabs.harvard.edu/abs/1991JGR....9619023C) |

Like Uranus, **stock captures the offset-tilted dipole axis** (tilt 47°, offset 0.55)
on top of the shared generic field shape.
Belts peak at L≈7 (just outside Proteus at 4.75 R_N), carved by ring/moon absorption
(Paranicas 1991 [`1991JGR....9619131P`](https://ui.adsabs.harvard.edu/abs/1991JGR....9619131P)), hard outer cut at Triton's orbit. Field is
strongly non-dipolar near the planet (quad/octupole comparable to dipole).

### Mercury

| Stock | Physical |
|---|---|
| ![mercury Stock](../img/belts/mercury_stock.png) | ![mercury Physical](../img/belts/mercury_phys.png) |

| Field | Stock (ROKerbalism `mercury`) | Physical | Source |
|---|---|---|---|
| pause | 1.6 / comp 1.4 → nose **1.14** | nose **1.45 R_M** (1.35–1.55, → 1.28 in storms) | Winslow 2013 [`2013JGRA..118.2213W`](https://ui.adsabs.harvard.edu/abs/2013JGRA..118.2213W) |
| belts | none | **none** ✓ (too small/dynamic) | Schriver 2015 [`2015AGUFM.P53A2089S`](https://ui.adsabs.harvard.edu/abs/2015AGUFM.P53A2089S) |
| geomagnetic_offset | 0.208 | **0.198** (484 km north) | Anderson 2011 [`2011Sci...333.1859A`](https://ui.adsabs.harvard.edu/abs/2011Sci...333.1859A) |
| pause_deform | **0.1** | keep — the lobed, non-axisymmetric boundary of a multipolar field | Anderson 2011/2012 (offset dipole + higher multipoles); stock `mercury` and `irregular` both use 0.1 |
| tilt | (small) | **<3°** (<0.8° refined) | Anderson 2011/2012 |
| moment | — | 190–195 nT·R_M³, southward | Anderson 2011, Korth 2015 [`2015JGRA..120.4503K`](https://ui.adsabs.harvard.edu/abs/2015JGRA..120.4503K) |

**Stock correctly models no belt** — Mercury's magnetosphere is too small and dynamic
to trap a stable population (only a quasi-trapped 1–10 keV equatorial cloud + transient
bursts). The northward offset (484 km ≈ 0.2 R_M) concentrates surface dose in the
**southern** hemisphere/cusps; SEP electrons reach the surface near-instantly on open
field lines (Gershman 2015 [`2015JGRA..120.8559G`](https://ui.adsabs.harvard.edu/abs/2015JGRA..120.8559G)). Stock's nose (1.6/1.4 = 1.14 R_M) is
slightly *tight* vs the physical 1.45 — not generous, as an earlier revision (reading
pause_radius as the standoff) had it.

### Ganymede

| Stock | Physical |
|---|---|
| ![ganymede Stock](../img/belts/ganymede_stock.png) | ![ganymede Physical](../img/belts/ganymede_phys.png) |

| Field | Stock (ROKerbalism `ganymede`) | Physical | Source |
|---|---|---|---|
| surface dipole | (implicit) | **719 nT eq** (tilt 176°) | Kivelson 2002 [`2002Icar..157..507K`](https://ui.adsabs.harvard.edu/abs/2002Icar..157..507K) |
| has_pause | (none) | **~2 R_G upstream** (5.5 across) | Kivelson 1998 [`1998JGR...10319963K`](https://ui.adsabs.harvard.edu/abs/1998JGR...10319963K) |
| inner belt | 0.8/0.6, rad 0.33 | single weak closed-line belt **L 1.1–1.9**, absorbed at the surface itself (airless — no altitude cut) (fit IoU .97), source-starved | Allioux 2013 [`2013AdSpR..51.1204A`](https://ui.adsabs.harvard.edu/abs/2013AdSpR..51.1204A) |
| open caps | — | **poleward of 30–45°** (leaky) | Pappalardo 1998 [`1998DPS....30.5401P`](https://ui.adsabs.harvard.edu/abs/1998DPS....30.5401P) |
| net role | — | **shield −50–60%** of ambient | Allioux 2013 |

The Solar System's only **weak-field embedded moon** — a dynamo inside a giant's
magnetosphere (the weak-field sub-regime of the geometry methodology). Ganymede's 719 nT
only modestly exceeds the local Jovian field → small ~2 R_G standoff, **open polar caps**
(reconnection with Jupiter), no bow shock (sub-Alfvénic → Alfvén wings; Saur 2018
[`2018ASSL..448..153S`](https://ui.adsabs.harvard.edu/abs/2018ASSL..448..153S)). It molds only <~100 keV ions into thin belts; the dominant dose
is Jupiter's ambient belt at ~15 R_J, which Ganymede's field attenuates by ~50–60% for
a low orbiter. **Stock omits the pause entirely** — a fix worth adding.

---

## What the two-shell model cannot represent (fidelity ceilings)

- **Moon/ring absorption gaps** (Saturn corridors, Neptune Proteus notch, Uranus moon
  sweeping) — Kerbalism has only inner+outer tori, no per-L depletion.
- **A flat magnetodisc's sharp radial edges** — the best torus fit is a lens (Jupiter
  outer IoU 0.87 vs ≥0.96 for every dipolar shell); real discs taper, so the lens is
  arguably closer to nature than the slab target itself.
- **Time variation** — the ice-giant belts wobble every rotation (tilt+offset); cfg is static.
- **Multipole distortion** near the planet (Uranus/Neptune quad≈dipole) — the dipole
  `geomagnetic_offset` is the only handle.
- **Belt intensity from first principles** — governed by source/loss/Kennel–Petschek, not
  field strength (see geometry methodology Part B); all `radiation_*` values are regime
  calls, conf low.

# Part 2 — derivation record

Moved out of `planetary-magnetosphere-geometry-methodology.md` on 2026-08-16, verbatim
where the prose was already settled. Nothing here is needed in order to apply the recipe.

## Why the tail has no derivable length

`L`, the distance at which the bounded cfg volume closes, is the one geometric quantity in
the recipe with no derivation behind it. Eight attempts are on record. Six are tabulated in
the methodology's dead-end table; the seventh and eighth are below, and between them they
establish that the quantity is not derivable rather than merely underderived.

**Seventh attempt, 2026-08-16: the boundary never fades, so there is no fade point.**
The idea was to end the tail where the inside/outside contrast blurs, and to let a
weak-field body get a proportionally shorter tail than a strong one. Three calculations
kill it.

The lobe field is set by pressure balance, `B_lobe = sqrt(2 mu0 P_ext)`, which depends on
the ambient wind at that orbital distance and **not at all on the planet's own field**. It
therefore does not decay downtail: at each station the boundary re-balances against the
same external pressure.

The lobes are Kelvin-Helmholtz stable. With the lobe field aligned to the flow, the
instability threshold `dv^2 > (1/mu0)(1/rho_1 + 1/rho_2)(B_1^2 + B_2^2)` puts the critical
shear at 1540 to 1880 km/s along Earth's distant tail, against a magnetosheath flow of
~400. The boundary layer does not turbulently thicken, so a mixing-layer criterion never
consumes the tail radius (Miura 1987, [`1987JGR....92.3195M`](https://ui.adsabs.harvard.edu/abs/1987JGR....92.3195M);
Walker 1981, [`1981P&SS...29.1119W`](https://ui.adsabs.harvard.edu/abs/1981P%26SS...29.1119W)).

And the contrast itself is scale-free: dividing the two expressions gives
`B_lobe / B_IMF = sqrt(2) * M_A`, a **constant along the tail**, because both fields fall
off the same way. Earth 13.5x, Jupiter 14.7x, Polyphemus 13.5x. The tail interior stays
an order of magnitude above its surroundings forever.

One byproduct is worth keeping: `sqrt(2) * M_A` is a cheap contrast diagnostic that needs
no field model. Proxima b scores **4.5x** against everyone else's 13 to 15, because its
wind is nearly Alfvenic (M_A ~ 3) - its tail is a genuinely faint structure, even though it
is not a short one.

Also retracted here: an intermediate step in that attempt backed a shear-layer spreading
rate `S = R_T / L` out of the published tail extents and read the spread (Earth 0.13,
Jupiter 0.014) as a physical difference in tail length. It is not. Every `L` is a
spacecraft-coverage bound, so every `S` is an upper bound, and the spread measures how far
each mission flew, not how long each tail is.

**A real termination mechanism does exist, and it is topological rather than diffusive**
(three-agent literature sweep, 2026-08-16). The tail is not erased by fading; it is *cut*.
Kurth 1982 ([`1982JGR....8710373K`](https://ui.adsabs.harvard.edu/abs/1982JGR....8710373K)) conjectured a "pinch-off or disconnection" of the
distant Jovian tail, and Goldstein 1985 ([`1985JGR....90.8223G`](https://ui.adsabs.harvard.edu/abs/1985JGR....90.8223G)) confirmed it: an
interplanetary sector crossing appeared in the Voyager 1 solar-wind data during the event,
"as predicted by Kurth et al. (1982). This supports their conjecture that the tail had
disconnected from Jupiter." This is the planetary counterpart of a cometary disconnection
event. The same paper finds the distant-tail magnetic spectra at 6000–7500 R_J follow
`f^−5/3`, indistinguishable from the ambient wind.

That gives a computable length: the attached tail can only grow for as long as the planet
goes between current-sheet crossings, so `L = v_wind × T_sector`, where `T_sector` is the
synodic period of the two-sector pattern (stellar rotation / 2) against the orbit. Every
Solar-System planet lands near **3 AU** (12.7–13.5 d sector period against a 400 km/s
wind), which is where the distant detections actually sit — Jupiter 4.5 AU, comet Hyakutake
3.8 AU. NearStars: Polyphemus 2.58 AU, Proxima b 12.83, Proxima c 35.5, Proxima d 4.89.

**Computed and deliberately not adopted** (owner decision 2026-08-16). Two reasons. It
agrees with `150 × nose` for the giants (Jupiter 6157 against 9450 R_J, Polyphemus 5398
against 5300) and diverges by two to three orders of magnitude for small bodies, because it
is an absolute distance rather than a multiple of the nose — Venus would go from 158 to
76,868 R_V, whose `extension` of 1.5e-5 is a cylinder that never visibly closes. And the
mechanism is a *duty cycle*, not a wall: the severed tail keeps travelling, which is why
comet 153P was detected 6.5 AU downstream (Jones 2022, [2006.00500](https://arxiv.org/abs/2006.00500)) and why
Jones argues some ion tails "may survive as recognizable structures to the edge of the
heliosphere."

**The flux budget does not terminate the tail either.** The premise — that the tail ends
where its finite open flux has all reconnected — fails on measurement: Slavin 1985
([`1985JGR....9010875S`](https://ui.adsabs.harvard.edu/abs/1985JGR....9010875S)) finds flaring ceases at |X| = 120 ± 10 R_E with `B_L` = 9.2 nT
and a 60 R_E diameter both **constant out to 225 R_E**, so the lobe flux is flat at the full
polar-cap value rather than draining. Milan 2004 ([`2004JGRA..109.7210M`](https://ui.adsabs.harvard.edu/abs/2004JGRA..109.7210M)) built the
model anyway and reports the length "can vary by almost a factor of 10, between ~400 and
4000 R_E, in just a few hours", adding that "a much longer disconnected tail and wake can
exist beyond this". A quantity that moves 3600 R_E in three hours is not an edge. It does
leave a useful internal marker: the boundary between the Dungey-connected tail and the
disconnected wake, 400–4000 R_E at Earth, which brackets our 1500.

**The one field that has solved this problem is heliotail research, and its solution does
not transfer.** Izmodenov & Alexashov 2003 ([astro-ph/0308211](https://arxiv.org/abs/astro-ph/0308211)) state the difficulty
in our own terms — "in the heliotail we cannot assume the heliopause to be the heliospheric
boundary … the solar wind fills the whole space into the downwind direction" — and then get
numbers only by invoking charge exchange with interstellar neutrals: the density and
tangential-velocity jumps vanish at **~3000 AU**, and the plasma converges to interstellar
values at **20,000–40,000 AU**. Their summary sentence is the one to carry: "unlike the
upwind direction the solar system boundary has **diffusive nature** in the heliotail." A
planetary magnetotail sits in a fully ionised magnetosheath and has no comparable neutral
sink, which is exactly why no equivalent number exists for planets.


## The near-tail X-line

**The comparison only works if the same structure is compared.** An earlier pass put Earth's
*distant* neutral line (100–140 R_E, 10–14 `r₀`) beside everyone else's *near* line and
concluded the scatter was 12×, which killed several candidate recipes. The names carried the
answer: Mercury's is literally the "Near-Mercury Neutral Line". Compared like with like the
spread is **1.04–3.00, a factor of 2.9**, and Earth's distant line is a separate structure
measured nowhere else.

Two refinements are available, and they differ in how much they can be trusted.


**Grade: empirical, anchors reproduced, predictive power unverified.** Two things keep it
from being more. There is no fourth body to test it on — Neptune's tail has no plasmoid or
X-line measurement (searched 2026-08-15). And the grouping rationale is contested: Turner
2024 ([`2024JGRA..12932723T`](https://ui.adsabs.harvard.edu/abs/2024JGRA..12932723T)) places Uranus in a **third** category, "unlike the other
magnetospheric systems that are Dungey-cycle driven (i.e., Mercury and Earth) or
rotationally driven (Jupiter and Saturn)", and Gershman 2020 ([`2020EPSC...14..258G`](https://ui.adsabs.harvard.edu/abs/2020EPSC...14..258G))
reports Voyager 2 measuring `M_A` ~23 at Uranus with a plasmoid "suggestive of more internal
planetary plasma driven" transport. That encounter's geometry is itself extreme — the
rotation axis pointed within ~8° of the Sun, so the 59° dipole tilt swept the current sheet
through a full turn each rotation, against a 24° flap at Earth; it is laid out in
[`uranus-geometry.html`](../uranus-geometry.html). So Uranus may not belong with Mercury and Earth at all,
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


## Induced boundary shape families, measured and rejected

The adopted form for Venus and Mars is the generalised stock pause. Everything else that
was tried is here, with the measured error against nose, terminator and wake.

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


## The widest cross-section is pinned to the body plane

The stock pause fixes its maximum cross-section at `x` = 0, while every real magnetopause
is widest behind the planet. This is the largest single source of shape error in the
encoding. The fix that worked - retiring `compression` to 1.0 and moving the section with
`pause_waist` - is in the methodology; the two attempts that did not work are here.

This does **not** fix the tail-width deficit — that needs the Shue-native mode. A first
attempt to use `pause_smooth` for the width, by fitting it against the Shue curve rather
than against the corner, drove it to 3 × nose and turned the piecewise-linear `px` into a
quadratic. That is a change of function family, not a smoothing, and was rejected.

Nose (1.055 / 1.285) and terminator (1.13 / 1.47) come out exact, the tail closes at
158 / 193 R_p (the 150 x nose convention; an earlier revision of this table carried
`extension` 0.0567 / 0.0737, a 20 R_p closure from before that convention existed, which
the shipped presets had already moved past), and the bulge is 0.000%. The cost is wake width: against the measured cone the
boundary is 15% narrow at 2 R_p, 33% at 5 and 54% at 10 — accepted, because no-bulge
outranks wake fidelity here, and because every Shue parameterization does far worse
(−83% to −100%; see Part A).


**`pause_offset`** is the cheap fallback if the full Shue mode is rejected: shift
the sphere centre tailward before the scaling (`p.x += pause_offset`), which fixes
the "widest at the body plane" defect in one line. A least-squares fit against the
softened Shue curve for Proxima c (nose 11.905, α 0.5, tail 125) reproduces the
nose, the body-plane width, the maximum width and the tail closure within a few
percent at `pause_offset` 19.7 / radius 21.5 / compression 0.68 / extension 0.204.
Every shipped stock and ROKerbalism pause underrepresents tail width the same way
(Earth flank 15 vs an observed 25–30 R_E tail radius), so this is a general defect,
not a NearStars quirk.


## Night-side alpha, trialled and rolled back

Tried 2026-08-16, rejected the same day. The aim was art: reduce the tail width behind the
planet, which the owner found too fat, by giving the night side a lower Shue α than the
fitted dayside value.

Three variants were built and measured against Slavin 1985's 30 R_E radius at x = −120 R_E,
the only place a planetary tail width is actually measured:

| variant | how α is blended | width at x = −120 | vs measured |
|---|---|---|---|
| single α 0.58 | — | 27.9 | −7.0% |
| night α 0.48, by angle | smoothstep over θ 90°→180° | ~18.0 | −40.1% |
| night α 0.52, by angle | same | 22.1 | −26.5% |
| night α 0.52, by distance, onset at 0.66 L | untouched until 34% down the tail | 27.9 | −7.0% |
| night α 0.52, by distance, complete by 0.66 L | blend finishes 34% down the tail | 27.0 | −10.1% |

The angle-based blend was the original implementation and is the reason the boundary
appeared to pinch immediately behind the planet: most of the θ 90°→180° range maps to the
near tail, so at θ = 120° (x = −11 R_E for Earth) the blend is already 33% applied. Moving
the blend onto downtail *distance* fixes that, and either distance variant keeps the Slavin
agreement.

It still did not look right, and the reason turned out not to be α at all. The softened
Shue closure taper is fixed at `m` = 1, which spreads the closing over half the tail — the
width is already down 19% at 70% of L. That, not the α blend, is what reads as "narrowing in
the middle". Raising `m` holds the width out to 80% of L and then closes sharply, but `m` is
pinned at 1 by an earlier owner decision and reopening it was out of scope.

Rolled back in full: every body keeps a single α, and the night-side slider stays in the
viewer as an exploration knob with no body setting it. The `m` finding is the one to pick up
if this is revisited.

## Citations (ADS-pinned, by body)

- **Jupiter**: Joy 2002 [`2002JGRA..107.1309J`](https://ui.adsabs.harvard.edu/abs/2002JGRA..107.1309J); Divine & Garrett 1983 [`1983JGR....88.6889D`](https://ui.adsabs.harvard.edu/abs/1983JGR....88.6889D);
  Connerney 2022 (JRM33) [`2022JGRE..12707055C`](https://ui.adsabs.harvard.edu/abs/2022JGRE..12707055C); Santos-Costa 2001 [`2001P&SS...49..303S`](https://ui.adsabs.harvard.edu/abs/2001P%26SS...49..303S);
  Khurana 1989 [`1989JGR....9411791K`](https://ui.adsabs.harvard.edu/abs/1989JGR....9411791K).
- **Saturn**: Cooper 1983 [`1983JGR....88.3945C`](https://ui.adsabs.harvard.edu/abs/1983JGR....88.3945C); Achilleos 2008 [`2008JGRA..11311209A`](https://ui.adsabs.harvard.edu/abs/2008JGRA..11311209A);
  Kollmann 2013 [`2013Icar..222..323K`](https://ui.adsabs.harvard.edu/abs/2013Icar..222..323K); Kollmann 2017 [`2017NatAs...1..872K`](https://ui.adsabs.harvard.edu/abs/2017NatAs...1..872K); Roussos 2007
  [`2007JGRA..112.6214R`](https://ui.adsabs.harvard.edu/abs/2007JGRA..112.6214R); Roussos 2018 [`2018Sci...362.1962R`](https://ui.adsabs.harvard.edu/abs/2018Sci...362.1962R); Cao 2020 [`2020Icar..34413541C`](https://ui.adsabs.harvard.edu/abs/2020Icar..34413541C).
- **Uranus**: Ness 1986 [`1986Sci...233...85N`](https://ui.adsabs.harvard.edu/abs/1986Sci...233...85N); Krimigis 1986 [`1986Sci...233...97K`](https://ui.adsabs.harvard.edu/abs/1986Sci...233...97K); Stone
  1986 [`1986Sci...233...93S`](https://ui.adsabs.harvard.edu/abs/1986Sci...233...93S); Cheng 1987 [`1987JGR....9215315C`](https://ui.adsabs.harvard.edu/abs/1987JGR....9215315C); Connerney 1987 [`1987JGR....9215329C`](https://ui.adsabs.harvard.edu/abs/1987JGR....9215329C); Behannon 1987
  [`1987JGR....9215354B`](https://ui.adsabs.harvard.edu/abs/1987JGR....9215354B).
- **Neptune**: Ness 1989 [`1989Sci...246.1473N`](https://ui.adsabs.harvard.edu/abs/1989Sci...246.1473N); Krimigis 1989 [`1989Sci...246.1483K`](https://ui.adsabs.harvard.edu/abs/1989Sci...246.1483K); Stone
  1989 [`1989Sci...246.1489S`](https://ui.adsabs.harvard.edu/abs/1989Sci...246.1489S); Connerney 1991 [`1991JGR....9619023C`](https://ui.adsabs.harvard.edu/abs/1991JGR....9619023C); Paranicas 1991
  [`1991JGR....9619131P`](https://ui.adsabs.harvard.edu/abs/1991JGR....9619131P).
- **Mercury**: Winslow 2013 [`2013JGRA..118.2213W`](https://ui.adsabs.harvard.edu/abs/2013JGRA..118.2213W); Anderson 2011 [`2011Sci...333.1859A`](https://ui.adsabs.harvard.edu/abs/2011Sci...333.1859A);
  Schriver 2015 [`2015AGUFM.P53A2089S`](https://ui.adsabs.harvard.edu/abs/2015AGUFM.P53A2089S); Gershman 2015 [`2015JGRA..120.8559G`](https://ui.adsabs.harvard.edu/abs/2015JGRA..120.8559G); Korth 2015
  [`2015JGRA..120.4503K`](https://ui.adsabs.harvard.edu/abs/2015JGRA..120.4503K).
- **Ganymede**: Kivelson 2002 [`2002Icar..157..507K`](https://ui.adsabs.harvard.edu/abs/2002Icar..157..507K); Kivelson 1998 [`1998JGR...10319963K`](https://ui.adsabs.harvard.edu/abs/1998JGR...10319963K);
  Kivelson 1996 [`1996Natur.384..537K`](https://ui.adsabs.harvard.edu/abs/1996Natur.384..537K); Pappalardo 1998 [`1998DPS....30.5401P`](https://ui.adsabs.harvard.edu/abs/1998DPS....30.5401P); Allioux 2013
  [`2013AdSpR..51.1204A`](https://ui.adsabs.harvard.edu/abs/2013AdSpR..51.1204A); Saur 2018 [`2018ASSL..448..153S`](https://ui.adsabs.harvard.edu/abs/2018ASSL..448..153S).

## Related

- [`planetary-magnetosphere-geometry-methodology.md`](planetary-magnetosphere-geometry-methodology.md)
  — the field-shape recipe + Kerbalism SDF schema this audit renders.
- `scripts/viz/fit_belts.py` — the numerical fitter (dipole-shell targets → SDF
  parameters, IoU-scored); fitted parameter sets live in `render_belts_bodies.py`.
- [`planetary-dynamo-scaling.md`](planetary-dynamo-scaling.md) /
  [`rocky-planet-dynamo-methodology.md`](rocky-planet-dynamo-methodology.md) — the B-field
  inputs.
- Published page (renders included): [Solar-System radiation belts](https://vannadin.github.io/nearstars-db/wiki/reference__solar-system-radiation-belts.html)
  (cross-section images).
- [methodology-index](methodology-index.md).
