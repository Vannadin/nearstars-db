<!-- 크레이터가 다른 지형에 지워지기까지 걸리는 시간을 풍화 채널별로 도출하는 방법(논문 근거) — 표면 비주얼(크레이터 밀도) 결정용 -->
# Crater degradation grounding: how long a crater survives each resurfacing process

Method reference for the question every surface visual depends on: **does this
body render cratered, partially cratered, or crater-free?** The answer is a race
between two clocks — the rate at which impacts *add* craters and the rate at
which resurfacing processes *erase* them — and each erasure channel has its own
timescale law. This doc grounds the channels, calibrates each on a Solar-System
anchor, and reduces the decision to one comparison.

The consumer is the Phase 4 `surface` / `appearance` axis: a terrain whose
erasure time is shorter than its crater-accumulation time renders smooth, and
the crossover diameter (small craters die first) sets *which* craters survive.

## The race, stated once

    t_erase(D, process)  <  t_accumulate(D)   →  terrain renders smooth at size D
    t_erase(D, process)  >  t_age (or t_saturate)  →  craters persist / saturate

`t_accumulate` comes from the impact flux (Neukum/Hartmann chronology for the
inner Solar System; Zahnle 2003 for the outer). `t_saturate` is the ceiling:
beyond saturation equilibrium the surface *look* stops changing no matter how
long bombardment continues (Hartmann 1984). Everything body-specific lives in
`t_erase`, which is the subject of this doc.

## The erasure channels

### 1. Topographic diffusion (impact gardening) — the airless default

On an airless surface with no other geology, countless small impacts random-walk
material downslope and crater topography obeys the diffusion equation. Fassett &
Thomson 2014 calibrated the lunar-maria diffusivity over 3 Gyr:

    κ ≈ 5.5 m²/Myr        (lunar maria, 3 Ga average)

and their own worked numbers are: after 3 Gyr a 1 km crater retains ~52 % of its
depth, a 300 m crater ~7 %, and craters below ~200–300 m are degraded beyond
recognition. Because diffusion scales as length², the erasure time is

    t_erase ≈ C · D² / κ,    C ≈ 0.26
    (calibrated so 250 m craters die at exactly 3 Gyr on the maria)

Two consequences worth internalizing: small craters vanish first (the smooth
look starts at small scales), and a 1 km crater on a Moon-like surface takes
~47 Gyr to fully erase — **diffusion alone never de-craters a surface at
kilometre scale.** A world with only this channel is a cratered world.

Cross-system scaling: κ is set by the small-impactor flux, so in another
planetary system it is unknown to a factor of several. That uncertainty almost
never changes the *visual class*, because the channels below beat diffusion by
orders of magnitude when they operate at all.

### 2. Burial (volcanic / plume / sediment deposition)

A crater disappears when deposits overtop its topography. Simple craters have
depth ≈ 0.2 D and rim height ≈ 0.04 D, so

    t_erase ≈ 0.2 · D / ḣ        (ḣ = deposition rate; rims linger ~×0.2 longer as ghost rings)

Anchors: Io accumulates plume and lava deposits fast enough that **zero impact
craters have ever been identified** despite sitting in Jupiter's focused
impactor flux (mechanism: Johnson et al. 1979; flux: Zahnle 2003) — at the
few-mm/yr scale a 1 km crater (200 m deep) is gone in well under a Myr. Venus is
the *episodic* version of the same channel: 84 % of its craters are pristine and
only 2.5 % lava-embayed, which is inconsistent with steady resurfacing and
implies a global volcanic repaving followed by quiet (Strom, Schaber & Kirk
1994). Burial therefore renders either **crater-free** (continuous supply) or
**uniformly lightly cratered** (episodic, all craters younger than the last
event) — it does not produce a mixed old/young look on one terrain.

### 3. Viscous relaxation (warm ice)

Ice flows. A crater in an ice crust relaxes away bottom-up: long wavelengths
relax fastest, so **large craters die first** — the exact opposite ordering of
diffusion — leaving tell-tale shallow "pancakes" with intact rims before they
vanish (Passey & Shoemaker 1981, who first inverted crater shapes on Ganymede/
Callisto for viscosity structure). The rate is exponentially sensitive to
temperature through the ice viscosity, which makes it a switch more than a dial:

- **Cold water ice is rigid.** Enceladus' relaxed craters (relaxation fractions
  >90 % at diameters as small as 2 km) require heat fluxes **>150 mW/m²** even
  granting a 120 K lithosphere top — ordinary radiogenic fluxes (a few mW/m²)
  relax nothing observable (Bland et al. 2012). At outer-system surface
  temperatures (40–100 K), water-ice bedrock keeps its craters for the age of
  the system unless the body had an Enceladus-grade heating episode.
- **Volatile ices near their melting point flow on human-history timescales.**
  Nitrogen ice (T_melt = 63 K) at Pluto's 38 K not only relaxes, it *convects*:
  a layer thicker than ~1 km overturns in the sluggish-lid regime at a few
  cm/yr, renewing the surface in **~500 kyr** (crater retention <10 Myr) —
  McKinnon et al. 2016, and the reason Sputnik Planitia is crater-free.

Rule of thumb by homologous temperature T/T_melt of the *surface material*
(textbook creep scaling, the allowed non-paper exception): below ~0.5, treat
relaxation as off; above ~0.6, treat the material as self-renewing at Myr scale
or faster; in between, only the largest craters shallow noticeably over Gyr.
The decisive trick: **the same 40 K surface is "cold" for water ice
(T/T_m = 0.15) and "hot" for nitrogen ice (T/T_m = 0.6)** — one body renders
both cratered bedrock and smooth volatile basins, which is exactly Pluto's face.

### 4. Fluvial / aeolian (thick-atmosphere worlds)

Rain, rivers and wind fill craters from the floor up. The Martian-highlands
calibration (Forsberg-Taylor, Howard & Craddock 2004) shows the channel's
signature: infilling is **fast at first and self-limiting** (rates fall as wall
height drops and the deposition floor widens), producing a bimodal population —
old craters all strongly infilled, young ones barely touched. Titan is the
modern anchor: its crater areal density is comparable to Venus' (Neish & Lorenz
2012), i.e. an actively resurfaced world a few hundred Myr "old" despite Gyr of
bombardment. Use this channel only where a working hydrological/aeolian cycle
exists; its effective erasure time for D ≳ 10 km craters is a few hundred Myr
at Mars/Titan vigor.

### 5. Wholesale renewal (convective overturn, tectonic repaving)

Not gradual: the terrain itself is replaced. Anchors are Sputnik Planitia
(~500 kyr, channel 3's convective extreme) and Venus (episodic global
volcanism, channel 2's extreme). Europa's ~40–90 Myr surface age (Zahnle 2003
flux applied to its observed crater count) shows the tectonic version. Render:
crater-free, with the process's own texture (cells, flows, bands) instead.

## Practical recipe

1. List the body's active processes per terrain unit (from `bulk` internal heat,
   `atmosphere`, tidal heating, volatile inventory).
2. For each, compute `t_erase(D)` at two reference sizes — D = 1 km (the "is it
   cratered at all in-game" scale) and D = 20 km (basin scale).
3. Compare against `t_accumulate` (system age if flux unknown; state the flux
   assumption — it is the dominant cross-system unknown, easily ×10).
4. Visual verdict per terrain: **saturated / cratered / sparse / crater-free**,
   with the crossover diameter if channels disagree by size (diffusion kills
   small first; relaxation kills large first; burial kills all at once).

## Validation

- **Diffusion reproduces its own source.** `C = 0.26` with κ = 5.5 m²/Myr puts
  the 3 Gyr erasure cutoff at 250 m, inside Fassett & Thomson's stated
  200–300 m; their 1 km/52 % and 300 m/7 % depth states bracket it correctly
  (κt/D² = 0.017 → mostly intact; 0.18 → nearly gone). ✓
- **Direction checks across the anchor set.** Io (max burial) has zero craters;
  Venus (episodic burial) is uniformly young with random spatial distribution;
  Titan (fluvial) matches Venus-level density; Enceladus (relaxation) demands
  >150 mW/m², so cold icy moons keep craters; Sputnik (volatile convection)
  is crater-free under a <10 Myr retention limit. All five land in the regime
  this recipe assigns them. ✓
- **Ordering signature.** Diffusion erases small-first (lunar maria lack
  <300 m craters, keep km ones); relaxation erases large-first (Enceladus'
  2 km craters at >90 % relaxation still have rims). The recipe's crossover
  logic reproduces both. ✓

## Domain of validity, and what this recipe does not do

1. **Flux is the weak input.** Absolute `t_accumulate` for an exo-system is a
   stated assumption, not a derivation; lean on the orders-of-magnitude gaps
   between channels, which survive any plausible flux.
2. **Saturation caps the look, not the age.** Past `t_saturate` the render is
   "saturated" regardless of true age (Hartmann 1984); don't read surface age
   off a saturated unit.
3. **Secondary craters and palimpsests** are below this doc's resolution — it
   decides terrain-level looks, not individual landforms.
4. **Relaxed ≠ erased.** A relaxing crater spends most of its life as a
   shallow pancake with a rim; if the art pass wants "ancient softened basins,"
   channel 3's intermediate state is the grounded reference.

## Worked example: Proxima c I (captured KBO moon, ~40–50 K)

Two terrain materials, one temperature — the channel-3 switch does all the work:

- **Water-ice bedrock**: T/T_melt ≈ 0.17, relaxation off; no atmosphere, no
  burial source on the highlands → only diffusion runs. Even with a generous
  ×10 lunar κ, a 1 km crater outlives the system (t_erase ~ 4.7 Gyr ≫ any
  retention age) → **cratered, saturated-old highlands**.
- **N₂/CH₄ ice basins**: T/T_melt ≈ 0.65–0.8 for N₂ → Sputnik regime; any
  km-thick deposit convects and renews in ≲1 Myr → **crater-free cellular
  plains**.

Verdict: the Pluto-like dichotomy (bright smooth volatile basins set into dark
cratered tholin-stained bedrock) is not just an art homage — it is what the
timescales require. The same computation gates Dante's plains on the alpha
board from the other side: at ~800× Io's volcanic supply, channel 2 buries a
1 km crater in ≪ 10 kyr, so sulfur plains render crater-free without argument.

## Citations

- **Fassett & Thomson 2014**, JGR Planets 119, 2255
  ([`2014JGRE..119.2255F`](https://ui.adsabs.harvard.edu/abs/2014JGRE..119.2255F)).
  The topographic-diffusion calibration: κ ≈ 5.5 m²/Myr, the 52 %/7 %/200–300 m
  degradation states this recipe's constant is fitted to. Paywalled, no
  preprint — verified by bibcode + abstract (the abstract carries every number
  used here).
- **Hartmann 1984**, Icarus 60, 56
  ([`1984Icar...60...56H`](https://ui.adsabs.harvard.edu/abs/1984Icar...60...56H)).
  Crater saturation equilibrium — the ceiling on the cratered look.
- **Zahnle et al. 2003**, Icarus 163, 263
  ([`2003Icar..163..263Z`](https://ui.adsabs.harvard.edu/abs/2003Icar..163..263Z)).
  The standard outer-Solar-System impact rates: the production clock, and the
  Europa/Io retention-age arithmetic.
- **Passey & Shoemaker 1981**, Icarus 47, 100
  ([`1981Icar...47..100P`](https://ui.adsabs.harvard.edu/abs/1981Icar...47..100P)).
  Founding treatment of crater viscous relaxation on icy bodies; the
  large-craters-die-first ordering.
- **Bland et al. 2012**, GRL 39, L17204
  ([`2012GeoRL..3917204B`](https://ui.adsabs.harvard.edu/abs/2012GeoRL..3917204B)).
  Enceladus' relaxed craters: >90 % relaxation at 2 km, >150 mW/m² required —
  the proof that cold water ice keeps craters absent extreme heating.
- **McKinnon et al. 2016**, Nature 534, 82
  ([`2016Natur.534...82M`](https://ui.adsabs.harvard.edu/abs/2016Natur.534...82M)).
  Sputnik Planitia's N₂ convection: ~500 kyr renewal, <10 Myr retention, the
  volatile-ice self-renewal anchor. (Nature letter; ADS lists a later-posted
  arXiv copy, [1903.05571](https://arxiv.org/abs/1903.05571).)
- **Forsberg-Taylor, Howard & Craddock 2004**, JGR Planets 109, E05002
  ([`2004JGRE..109.5002F`](https://ui.adsabs.harvard.edu/abs/2004JGRE..109.5002F)).
  Fluvial/aeolian crater infilling on Mars: fast-then-self-limiting, bimodal
  populations.
- **Neish & Lorenz 2012**, P&SS 60, 26
  ([`2012P&SS...60...26N`](https://ui.adsabs.harvard.edu/abs/2012P%26SS...60...26N)).
  Titan's crater density comparable to Venus — the thick-atmosphere anchor.
- **Strom, Schaber & Kirk 1994**, JGR 99, 10899
  ([`1994JGR....9910899S`](https://ui.adsabs.harvard.edu/abs/1994JGR....9910899S)).
  Venus: 84 % pristine / 2.5 % embayed craters → episodic global resurfacing;
  the binary signature of the burial channel.
- **Johnson et al. 1979**, Nature 280, 746
  ([`1979Natur.280..746J`](https://ui.adsabs.harvard.edu/abs/1979Natur.280..746J)).
  Io plume deposition as a resurfacing mechanism (rates order-of-magnitude;
  the zero-crater observation itself rides on Zahnle 2003's flux).
- Homologous-temperature creep scaling (η exponential in T_melt/T) is used as a
  **textbook relation** (allowed exception), not pinned to a single paper.

## Related

- [`ice-stability-methodology.md`](ice-stability-methodology.md) — whether the
  ice survives at all (sublimation); this doc assumes it does and asks what the
  craters in it look like.
- [`tidal-heating-methodology.md`](tidal-heating-methodology.md) — supplies the
  heat flux that decides channels 2 (volcanic supply) and 3 (relaxation).
- [`surface-color-albedo-methodology.md`](surface-color-albedo-methodology.md) —
  colors the terrains this doc shapes.
- [methodology-index](methodology-index.md) — the living index of all
  derived-value recipes.
