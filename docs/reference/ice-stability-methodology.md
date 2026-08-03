<!-- 노출/매장 얼음의 승화 수명과 존속 알베도 임계를 증기압 곡선+Hertz-Knudsen으로 도출하는 방법(논문 근거) -->
# Surface-ice survival grounding: sublimation lifetime and the albedo threshold

Method reference for deciding whether a body can **keep exposed ice** at its orbit,
and what albedo it takes to do so. The question is not cosmetic: an icy surface, a
bright albedo, an ice-cap map and a cryovolcanic look all rest on the same claim,
so the claim needs a recipe rather than an intuition. "It's far from the star, so
ice is fine" is the failure mode this doc exists to stop — a body can sit at 1.6 AU
of Sun-equivalent insolation and still lose its entire radius to sublimation in a
few Myr.

The calculator that implements this recipe is [`docs/ice-stability.html`](../ice-stability.html)
(single-page, in-browser). This doc is the grounding the calculator's numbers are
cited by; the calculator is the tool, not the source of authority.

## The relation

Three pieces compose, in this order.

**1. Vapour pressure of the solid.** Fray & Schmitt 2009
([`2009P&SS...57.2053F`](https://ui.adsabs.harvard.edu/abs/2009P%26SS...57.2053F))
review every published measurement and thermodynamic relation for 53 pure molecular
solids and publish fitted curves with stated validity ranges and deviations. Their
polynomial form (their Eq. 4) is

    ln(P / bar)  =  A₀ + Σ Aᵢ / Tⁱ

with per-species, per-phase-band coefficients (their Table 5) and validity intervals
(their Table 4). For H₂O below the triple point they instead recommend the
Feistel & Wagner 2007 semi-empirical curve
([`2007GeCoA..71...36F`](https://ui.adsabs.harvard.edu/abs/2007GeCoA..71...36F)),
built from the 2006 Gibbs potential of ice Ih and valid 20–273.16 K (their Eqs. 5–6):

    ln(P / P_t)  =  1.5 · ln θ  +  (1 − 1/θ) · Σ eᵢ θⁱ ,        θ = T / T_t

**2. Free-sublimation mass flux.** Into vacuum, with no returning flux, the
Hertz–Knudsen relation gives the loss per unit area

    Φ(T)  =  P_vap(T) · √( m / 2πkT )        [kg m⁻² s⁻¹]

This is the form Schörghofer 2008
([`2008ApJ...682..697S`](https://ui.adsabs.harvard.edu/abs/2008ApJ...682..697S))
uses for planetary ice loss, and it is the upper bound on loss: any atmosphere,
lag layer, or mixed-ice matrix reduces it.

**3. Surface temperature with sublimation cooling.** The surface is *not* at
radiative equilibrium, because sublimation carries away latent heat. Solve

    σT⁴  +  L_sub(T) · Φ(T)  =  F_abs

for T. This self-limitation is what decides the answer for volatile species: a CO₂
surface at Chaos's orbit sits at 105 K rather than its 234 K radiative value, because
the sublimation term dominates long before radiation can balance the input. `F_abs`
comes from the four-term satellite energy budget (starlight minus eclipses, plus the
parent's thermal emission and reflected light) in
[`moon-energy-budget-methodology.md`](moon-energy-budget-methodology.md).

**Latent heat is not an independent input.** Taking it from a separate source would
risk inconsistency with the vapour-pressure curve, so it is derived from the same
curve through Clausius–Clapeyron:

    L_sub(T)  =  −R · d(ln P) / d(1/T)  /  M

## Practical formula

For a quick verdict without the full solve, exposed water ice is governed by its
loss rate in metres per year,

    ṙ(T)  =  Φ(T) / ρ_ice ,        ρ_ice = 930 kg m⁻³ (H₂O)

and the **survival criterion** is that the loss integrated over the body's age stays
small against the body's own scale (radius, or ice-shell thickness where that is what
matters). Because Φ is exponential in T, the criterion is effectively a temperature
threshold, and since T follows the absorbed flux, it converts into an **albedo
threshold** for a given orbit: raise the albedo until T drops below it.

| exposed H₂O ice | loss rate | loss in 5.3 Gyr |
|---|---|---|
| 110 K | 1.5 × 10⁻¹⁰ m/yr | 0.8 m |
| 120 K | 1.4 × 10⁻⁸ m/yr | 76 m |
| 134 K | 2.6 × 10⁻⁶ m/yr | 14 km |
| 145 K | 7.9 × 10⁻⁵ m/yr | 420 km |
| 160 K | 3.9 × 10⁻³ m/yr | 20 000 km |

Read that as: **~145 K is where exposed water ice stops surviving Gyr timescales**
on a body of a few hundred km, and every 10–15 K above it costs another order of
magnitude.

## Validation

The implementation reproduces published values it was not fitted to:

| Check | Reference value | This recipe | Match |
|---|---|---|---|
| H₂O triple-point pressure | 611.657 Pa | 611.657 Pa | exact |
| L_sub(H₂O) at 200 K | 2.83 × 10⁶ J/kg | 2.833 × 10⁶ J/kg | 0.1 % |
| H₂O vapour pressure, 170–250 K | Marti & Mauersberger 1993 experimental fit | ratio 0.981–0.995 | within 2 % |
| CO₂ / CH₄ / CO triple-point pressures | Fray & Schmitt Table 4 | 0.35 % / 1.5 % / 0.08 % | ✓ |
| Exposed-ice Gyr threshold | ~145 K mean surface (Schörghofer 2008, buried under dust) | 145 K (exposed, 400 km body) | see caveat |
| Ceres illuminated polar cap | stable only if albedo > 0.5 (Hayne & Aharonson 2015) | same direction, same magnitude | ✓ |
| Ceres perennial cold traps | < ~110 K for 1 Gyr stability (Hayne & Aharonson 2015) | 110 K → 0.8 m in 5.3 Gyr | ✓ |

**Caveat on the 145 K coincidence.** Schörghofer's threshold is for ice *buried*
under a dusty lag layer, surviving within the top few metres over solar-system age;
ours is for *exposed* ice on a 400 km body over 5.3 Gyr. The two criteria are not the
same statement, and they land on the same temperature only because both ask for
"loss ≲ the scale that matters over Gyr". Treat the agreement as a sanity check on
the flux law, not as a shared threshold.

Independent-anchor check against known bodies (Solar-System presets in the
calculator): Europa and Enceladus return stable ice crusts, Ceres returns exposed
ice unstable outside permanent shadow, and a bare ice surface at 1 AU returns
~1 m per perihelion-scale passage, the observed order for cometary erosion.

## Domain of validity: four regimes

1. **Exposed ice, refractory-poor.** The recipe applies directly; Φ is the answer.
2. **Buried ice under a lag layer.** Loss drops by orders of magnitude and becomes
   diffusion-limited through the dry mantle, `z = √(2 D ρ_v t / ρ_ice)`. Schörghofer
   2008 and Schörghofer 2016
   ([`2016Icar..276...88S`](https://ui.adsabs.harvard.edu/abs/2016Icar..276...88S))
   are the standard treatments; the diffusion coefficient D is an assumed input in
   our calculator, so **retreat depths are order-of-magnitude, and only the exposed
   case is quotable as a derived value.** Whether a lag layer forms at all depends on
   the ice-to-refractory ratio, which is a separate question.
3. **Energy-limited (species cannot exist as a solid).** When even sublimation at the
   triple point cannot radiate away the absorbed flux, no solid surface of that
   species is possible at that orbit; the loss rate is then the upper bound set by
   routing the entire absorbed flux into phase change. Surface temperature is capped
   at the triple point and the verdict is a hard "no solid", not a slow loss.
4. **Bodies with significant internal heat.** The energy budget here is external only.
   A tidally heated body must have its surface temperature raised by the internal
   flux first (see [`tidal-heating-methodology.md`](tidal-heating-methodology.md)),
   which can move it several regimes; an icy surface on a strongly heated body is a
   contradiction the recipe will not catch on its own.

Two further limits apply throughout. Only **pure single species** are computed, and
real surfaces are mixtures whose vapour pressure is lower than any pure component,
so the loss rates are upper bounds. And solid densities are nominal per species: they
enter the depth and lifetime linearly but not the sublimation physics.

## Worked example: Chaos (Alpha Centauri A b V)

Inputs from the Phase 2/3 anchors: L = 1.521 L☉, orbital distance 1.6 AU equivalent,
radius 400 km, age 5.3 Gyr, plus the parent terms from the satellite energy budget
(thermal 0.33 W/m², reflected 0.14 W/m², eclipse loss 1.3 %).

| albedo | F_abs | T_rad | T_surf | loss rate | 400 km lost in | loss over 5.3 Gyr |
|---|---|---|---|---|---|---|
| 0.70 | 60.0 W/m² | 180 K | 175 K | 8.8 × 10⁻² m/yr | 4.5 Myr | body destroyed |
| 0.80 | 40.0 | 163 | 162 | 6.7 × 10⁻³ | 60 Myr | body destroyed |
| 0.85 | 30.0 | 152 | 152 | 4.8 × 10⁻⁴ | 830 Myr | body destroyed |
| **0.875** | 25.0 | 145 | 145 | 7.7 × 10⁻⁵ | 5.2 Gyr | **≈ the whole radius: the threshold** |
| 0.91 | 18.0 | 134 | 134 | 2.3 × 10⁻⁶ | 180 Gyr | 12 km of 400 km |
| 0.95 | 10.1 | 115 | 115 | 2.0 × 10⁻⁹ | 2 × 10⁵ Gyr | 10 m |

The board reads this as: the original albedo 0.70 was not merely dark, it was
**impossible** — the moon would have sublimated away in 4.5 Myr against a 5.3 Gyr
age. Survival requires albedo ≥ 0.875, which is above the fresh-water-ice band
(0.6–0.8) in [`surface-color-albedo-methodology.md`](surface-color-albedo-methodology.md)
§6 and above Enceladus (0.81), the brightest body known. The adopted 0.91 clears the
threshold by a factor ~33 in loss rate rather than marginally. That the required
albedo exceeds every measured analogue is exactly why the Phase 4 row carries an
owner-override rather than a pass: the recipe does not license 0.91, it prices it.

## Citations

- **Fray & Schmitt 2009**, Planet. Space Sci. 57, 2053
  ([`2009P&SS...57.2053F`](https://ui.adsabs.harvard.edu/abs/2009P%26SS...57.2053F)).
  The vapour-pressure source for every species: reviewed measurements, fitted
  curves, per-band validity intervals and deviations. *Paywalled (Elsevier), no arXiv
  preprint*; obtained through the owner's institutional access and cached outside git
  at `docs/phase3/_papers/_fray2009.pdf` with provenance in
  `_fray2009.PROVENANCE.txt` (that folder is gitignored, so the paper itself is not
  in the repo).
- **Feistel & Wagner 2007**, Geochim. Cosmochim. Acta 71, 36
  ([`2007GeCoA..71...36F`](https://ui.adsabs.harvard.edu/abs/2007GeCoA..71...36F)).
  The H₂O sublimation curve used below the triple point, from the 2006 Gibbs
  potential of ice Ih, valid 20–273.16 K. Recommended by Fray & Schmitt for water.
- **Marti & Mauersberger 1993**, Geophys. Res. Lett. 20, 363
  ([`1993GeoRL..20..363M`](https://ui.adsabs.harvard.edu/abs/1993GeoRL..20..363M)).
  Independent experimental water-ice vapour pressures, 170–250 K. Used only as the
  cross-check in the validation table, never as an input.
- **Schörghofer 2008**, ApJ 682, 697
  ([`2008ApJ...682..697S`](https://ui.adsabs.harvard.edu/abs/2008ApJ...682..697S)).
  The standard ice-lifetime treatment for airless bodies: Hertz–Knudsen loss, the
  dusty-lag-layer regime, and the ~145 K buried-ice threshold over solar-system age.
- **Schörghofer 2016**, Icarus 276, 88
  ([`2016Icar..276...88S`](https://ui.adsabs.harvard.edu/abs/2016Icar..276...88S)).
  Asynchronous coupling of temperature, ice loss and impact stirring; the reference
  for depth-to-ice when the lag-layer regime is what matters.
- **Hayne & Aharonson 2015**, JGR Planets 120, 1567
  ([`2015JGRE..120.1567H`](https://ui.adsabs.harvard.edu/abs/2015JGRE..120.1567H)).
  Ceres thermal-stability modelling: the ~110 K / 1 Gyr criterion for perennial
  surface ice and the finding that an illuminated polar cap needs albedo > 0.5. The
  closest published analogue to the albedo-threshold logic used here, and the
  independent check that the threshold behaves in the right direction.
- **Brown & Ziegler 1979**, Adv. Cryogenic Engineering 25, 662. Upstream source of
  the CO₂ and CH₄ coefficients as compiled by Fray & Schmitt. *Non-ADS exception*: a
  book-series volume with no ADS record; it is used only through Fray & Schmitt's
  compilation, which is what we cite and validate against.
- **Heller & Barnes 2013** ([arXiv:1209.5323](https://arxiv.org/abs/1209.5323), cached).
  The satellite energy budget supplying `F_abs`; see
  [`moon-energy-budget-methodology.md`](moon-energy-budget-methodology.md).

## Related

- [`moon-energy-budget-methodology.md`](moon-energy-budget-methodology.md) — supplies
  `F_abs`, the input this recipe is most sensitive to.
- [`surface-color-albedo-methodology.md`](surface-color-albedo-methodology.md) — the
  per-surface Bond albedo bands the threshold is judged against; §6 is what makes an
  albedo of 0.91 an override rather than a choice.
- [`tidal-heating-methodology.md`](tidal-heating-methodology.md) — internal heat is
  excluded from the budget here and must be added before judging a heated body.
- [`exoplanet-atmosphere-methodology.md`](exoplanet-atmosphere-methodology.md) — the
  atmospheric-escape counterpart; the same "can it keep what it has" question one
  layer up.
- [methodology-index](methodology-index.md) — the living index of all derived-value recipes.
