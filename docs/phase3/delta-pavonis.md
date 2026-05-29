<!-- δ Pavonis Phase 3 synthesis: cfg-ready decisions and reasoning -->
# δ Pavonis — Phase 3 Synthesis

δ Pavonis (HD 190248, HIP 99240, GJ 780) is one of the closest
G-type subgiants to the Sun, at 6.10 ± 0.005 pc (Gaia DR3 parallax
163.95 ± 0.12 mas). The spectral classification G8IV (Gray 2006
NStars; Houk & Cowley 1975) places it just off the main sequence —
core hydrogen exhausted, hydrogen-shell burning beginning to inflate
the envelope. The radius, temperature, and luminosity are anchored on
the Rains 2020 VLTI/PIONIER interferometric angular diameter
(θ_LD = 1.828 ± 0.025 mas → R = 1.197 ± 0.016 R☉, Teff = 5571 ± 48 K,
L = 1.24 ± 0.03 L☉) — the brightest G subgiant in the southern sky and
a textbook nearby-subgiant target.

δ Pav hosts no confirmed planets — extreme-precision RV (Tinney 2005;
Mawet 2017) and direct imaging (Lannier 2017) rule out giants above
~3 M_Jup at >1 AU — and, contrary to some earlier catalog claims, **no
debris disk**: the deepest survey (Eiroa 2013 DUNES, Herschel/PACS
70/100/160 µm) classifies δ Pav as a non-excess source with one of the
lowest fractional-luminosity limits in the sample, L_dust/L_★ < 5×10⁻⁷.

**Scenario choice for NearStars: an old, very quiet, isolated G8
subgiant — slightly inflated and slightly redder than a G8V dwarf,
standing alone with no planets and no debris ring.** All stellar
parameters are canonical-aligned and anchored on direct measurement
(interferometry for R/Teff/L, asteroseismology for mass); the only
genuinely uncertain quantity is the age, where two isochrone analyses
diverge.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | G8IV | high | Gray 2006 NStars; Houk & Cowley 1975 MK catalog; subgiant classification confirmed by HR-diagram position |
| `mass_msun` | 1.07 ± 0.13 | medium | Bruntt 2010 asteroseismic scaling (ν_max); Bensby 2014 evolutionary 1.03 agrees within 1σ |
| `radius_rsun` | 1.197 ± 0.016 | high | Rains 2020 VLTI/PIONIER interferometry, θ_LD = 1.828 ± 0.025 mas; Bruntt 2010 asteroseismic 1.20 agrees |
| `teff_k` | 5571 ± 48 | high | Rains 2020 interferometric θ_LD + bolometric flux; Bruntt 2010 spectroscopic 5550 K agrees (Gaia DR3 GSP-Phot biased for this metal-rich star) |
| `luminosity_lsun` | 1.24 ± 0.03 | high | Rains 2020 bolometric flux integration; Bruntt 2010 1.22 L☉ agrees |
| `metallicity_fe_h_dex` | +0.36 ± 0.02 | high | Gomes da Silva 2021 AMBRE-HARPS; Bensby 2014 +0.37 and Bruntt 2010 +0.33 corroborate, super-solar |
| `age_gyr` | 9.3 (5.8–10.7) | medium | Holmberg 2009 GCS III isochrone, consistent with very low activity (log R'HK −5.13) + slow rotation; Bensby 2014 isochrone 4.9 Gyr (3.3–9.6) diverges — ranges overlap, age genuinely uncertain |
| `rotation_period_days` | ~35 (uncertain) | low | No measured period; vsini ≈ 1.7 km/s (Bruntt 2010) + R = 1.197 R☉ gives P_rot ≲ 36 d (sin i ≤ 1); very low activity supports slow rotation |
| `activity_log_rhk` | −5.13 | high | Gomes da Silva 2021 HARPS (6002 spectra, 2003–2016); Henry 1996 −4.999 agrees; among the most chromospherically quiet G subgiants known |
| `activity_cycle_years` | unknown | low | No long-term Mt. Wilson program coverage; subgiants in this evolutionary phase often show weakened or irregular cycles |
| `x_ray_log_lx_cgs_max` | 27.3 | medium | Hünsch 1998 ROSAT detection (0.073 ct/s) → log L_X ≈ 27.3 erg/s, log(L_X/L_bol) ≈ −6.4; weak but detected corona |
| `limb_darkening_alpha_h` | 0.16 ± 0.02 | medium | Claret 2011 LD tables for G8IV at Teff = 5571 (Rains 2020); no direct interferometric LD measurement |
| `visual_surface_tint_hex_primary` | `#ffe8c8` (amber-cream, redder than G2V Sol) | medium | Tie-break: G8IV blackbody at 5571 K + +0.36 dex metallicity reddening; subgiant envelope inflation shifts disk-integrated color slightly redder than a G8V dwarf at same Teff |
| `stellar_color_temp_k` | 5571 | high | derived from Teff (Rains 2020) |
| `visual_corona_extent_radii` | 1.6 | low | Tie-break: weak chromosphere + low log R'HK = −5.13 → muted corona band; rendered as a thin ring rather than the brighter Sun-like halo |
| `disk_present` | false | high | Eiroa 2013 DUNES non-detection, L_dust/L_★ < 5×10⁻⁷ (Herschel/PACS 70/100/160 µm all photospheric); no debris ring |

## Surface synthesis

δ Pavonis sits in the brief but visually consequential subgiant
phase: core hydrogen has been exhausted, a thin hydrogen-burning
shell is beginning to inflate the envelope, and the star is climbing
the subgiant branch toward the base of the red-giant branch. The
result is a photosphere ~20% larger and ~200 K cooler than a G8V
dwarf would be at the same mass. The luminosity of 1.24 L☉ — slightly
higher than its G8V analogs because the radius gain outpaces the
temperature drop — gives the star a paradoxical character: redder than
the Sun in color, but still slightly brighter.

The integrated disk color shifts noticeably toward amber-cream
compared to a G2V Sun. At Teff = 5571 K the blackbody peak sits near
520 nm — yellow-green still, but the slope across visible wavelengths
is shallower than a G2V, with more red and less blue than Sol.
Compounded by the +0.36 dex super-solar metallicity (which reddens the
visible continuum via line blanketing), the cfg tint `#ffe8c8`
captures the warmer cream of an evolved G8 star. The contrast with
α Cen A's `#fff4e8` (a G2V at 5847 K) is real and visible in
side-by-side renders.

Limb darkening is stronger than for a G2V because the cooler, more
extended atmosphere has a longer photon mean-free-path near the
limb. The H-band α exponent of ≈0.16 (Claret 2011 LD tables
interpolated to G8IV) is ~15% higher than α Cen A's measured 0.14 —
a subtle but real visual effect in fly-by renders, with the limb
appearing distinctly more shadowed than for a G2V dwarf.

Spot coverage is modest. Without a measured rotation period or
cycle, photometric variability constraints are loose (Hipparcos
H_p amplitude < 0.005 mag), but log R'HK = −5.13 (Gomes da Silva
2021) places δ Pav firmly in the inactive G subgiant locus — quieter
than α Cen A, comparable to the most magnetically dead stars in the
Mt. Wilson sample. For the cfg renderer, spot density is set to
half the solar-maximum value and randomly distributed, with no
strong cycle modulation.

## Atmosphere synthesis

δ Pav's chromosphere and corona are correspondingly weak. The
chromospheric Ca II H&K core flux of log R'HK = −5.13 (Gomes da Silva
2021, from 6002 HARPS spectra; Henry 1996 −4.999) lies near the
chromospheric "basal flux floor" where no further activity decline is
observed — δ Pav is essentially at the magnetic-quiescence asymptote
for its evolutionary stage. The ROSAT detection (Hünsch 1998) gives
log L_X ≈ 27.3 (cgs, 0.5–2 keV), i.e. log(L_X/L_bol) ≈ −6.4 — a weak
but real corona, an order of magnitude below the Sun at activity
minimum, consistent with the convective weakening expected as a star
expands off the main sequence.

The transition-region UV emission is correspondingly faint, but δ
Pav has been observed by IUE and HST/STIS, with Mg II h&k and Si IV
emission lines detected at weak but non-zero intensity. No measured
flares — δ Pav is among the most flare-quiet stars in the local
sample, with no events reported in any monitoring campaign.
Integrated XUV luminosity is ≲ 10⁻⁵ L_bol, well below thresholds
that would erode atmospheres on candidate inner planets even over
the full ~9 Gyr age of the system.

The benign space-weather state has interesting implications for any
hypothetical (currently unconfirmed) planet: at δ Pav's habitable
zone — roughly 1.0–1.7 AU based on Kopparapu 2013 conservative
limits scaled to 1.24 L☉ — XUV-driven atmospheric escape would be
negligible across the system's full lifetime. The cfg encodes a
benign stellar-wind environment with no significant CME flux for
in-game atmospheric retention modeling.

The stellar atmosphere itself, at the photosphere, shows the
canonical G8IV temperature inversion at the chromospheric onset:
T drops from 5571 K at τ=1 to a temperature minimum near 4200 K
around τ ≈ 10⁻⁴, then rises through the chromosphere to ~10⁴ K and
the transition region to ~10⁵ K. The cool temperature minimum is
deeper and broader than in G2V Sol, characteristic of the lower
acoustic flux from the larger, slower-convecting envelope.

## Rotation & spin synthesis

δ Pavonis rotates slowly — exactly how slowly is poorly determined.
The projected rotational velocity v sin i ≈ 1.7 km/s (Bruntt 2010;
Valenti & Fischer 2005 give similar values) combined with
R = 1.197 R☉ bounds the period only from above: P_rot · sin i ≤ 36 d,
so for i = 90° (equator-on) P_rot ≤ 36 d, and for typical random
inclinations the most probable period is ~30 d.

Skumanich braking applied from a G8V zero-age main-sequence rotation
of ~5 d, scaled to ~9 Gyr by P ∝ √t, predicts ~55 d — but the
subgiant expansion further slows the surface rotation by angular
momentum conservation as the envelope inflates. The Spada & Lanzafame
2020 subgiant rotation models predict 30–45 d at this evolutionary
stage. The cfg adopts 35 d as a within-window estimate, flagged
Confidence=low, and notes the open item for future photometric
monitoring.

Asteroseismic oscillations are detected — Bruntt 2010 first measured
the p-modes, and Lund 2025 (TESS) refines them to ν_max = 2269.8 ±
64.4 µHz and Δν = 107.9 ± 0.2 µHz — but no campaign has yet resolved
the rotational splitting of the modes, which would pin the period and
inclination. A future PLATO campaign would tighten this; the cfg open
items log the dependency.

Obliquity is unconstrained observationally. For an isolated single
star with no companion to torque the spin axis, default to obliquity
= 0° relative to the spin angular momentum reference frame; the cfg
encodes 0° as a within-window default with no special tilt for
visual flair.

## Visual styling

In the NearStars renderer, δ Pavonis is portrayed as an old, quiet,
isolated G8 subgiant — no planets, no debris ring, no companion. Key
visual choices:

- **Global appearance** — a warm amber-cream stellar disk
  (`#ffe8c8`), distinctly redder than the cream-white of α Cen A
  but warmer in tint than a K-dwarf orange. Side-by-side with G2V
  Sol the contrast is subtle but real; alone in a planet sky δ Pav
  reads as "a tired Sun, slightly redder, slightly larger."
- **Disk detail** — at a hypothetical close fly-by, the photospheric
  granulation is rendered with ~5% lower contrast than G2V because
  the larger, slower-convecting envelope produces shallower
  temperature differentials between hot rising plumes and cool
  intergranular lanes. Granulation cells are ~30% larger in angular
  size (scaled by R★).
- **Limb appearance** — visibly more darkened toward the limb than
  α Cen A, due to the cooler photosphere and stronger H⁻ opacity at
  oblique viewing angles. The limb appears noticeably shadowed in
  fly-by renders.
- **Corona / chromosphere** — rendered as a thin, faint ring at
  1.6 R★ (`visual_corona_extent_radii`), reflecting the very weak
  chromospheric and coronal emission. No active prominence
  rendering; no flare visual.
- **Spots / faculae** — set to half the solar-minimum amplitude,
  randomly distributed at low latitudes, with no cycle modulation
  in the current cfg.
- **No debris ring** — earlier NearStars drafts attached a cold
  debris ring at 30–80 AU, but that was traced to a fabricated
  citation; Eiroa 2013 DUNES is a clean non-detection
  (L_dust/L_★ < 5×10⁻⁷). δ Pav is rendered with no circumstellar
  ring of any kind.
- **Apparent diameter from candidate HZ** — a hypothetical 1 M⊕
  planet at 1.3 AU would see δ Pav fill ~0.50° angular diameter,
  comparable to Sol from Earth (0.53°).
- **Isolation cue** — unlike the α Cen system's binary-pair
  rendering, δ Pav stands alone. No second sun, no orbital
  conjunction events, no ring. The visual styling leans on the
  subgiant color and the inflated, limb-darkened disk to give the
  star personality.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Rains A. D. et al. 2020** — *Precision angular diameters for 16
  southern stars with VLTI/PIONIER* (`2020MNRAS.493.2377R`,
  arXiv:2004.02343). Direct interferometric θ_LD = 1.828 ± 0.025 mas →
  R = 1.197 ± 0.016 R☉, Teff = 5571 ± 48 K, L = 1.24 ± 0.03 L☉. The
  anchor for radius, temperature, and luminosity.
- **Bruntt H. et al. 2010** — *Accurate fundamental parameters for
  23 bright solar-type stars* (`2010MNRAS.405.1907B`,
  arXiv:1002.4268). Asteroseismic + spectroscopic analysis of δ Pav:
  asteroseismic M = 1.07 ± 0.13 M☉, R = 1.20 R☉, Teff ≈ 5550 K,
  [Fe/H] = +0.33, v sin i ≈ 1.7 km/s. Anchors mass and rotation.
- **Gomes da Silva J. et al. 2021** — *Stellar chromospheric activity
  of 1674 FGK stars from the AMBRE-HARPS sample* (`2021A&A...646A..77G`).
  log R'HK = −5.13 from 6002 HARPS spectra; [Fe/H] = +0.36 ± 0.02.
  Anchors activity and metallicity.
- **Eiroa C. et al. 2013** — *DUNES: DUst around NEarby Stars,
  observational results* (`2013A&A...555A..11E`, arXiv:1305.0155).
  Herschel/PACS survey; δ Pav is a **non-excess source** with
  L_dust/L_★ < 5×10⁻⁷ — the basis for `disk_present = false`.
- **Bensby T. et al. 2014** — *Exploring the Milky Way stellar disk:
  714 F and G dwarf stars* (`2014A&A...562A..71B`, arXiv:1309.2631).
  FEROS high-resolution spectroscopy: [Fe/H] = +0.37, mass 1.03 M☉,
  isochrone age 4.9 Gyr — the younger arm of the age divergence.
- **Holmberg J., Nordström B., Andersen J. 2009** — *The
  Geneva-Copenhagen survey III* (`2009A&A...501..941H`,
  arXiv:0811.3982). Isochrone age 9.3 Gyr (5.8–10.7) — the adopted
  (older) age, consistent with the very low activity.

### Read (context / methodology, not directly decision-driving)

- **Lund M. N. et al. 2025** — *The TESS Legacy Sample of Bright
  Stars. I.* (`2025A&A...701A.285L`, arXiv:2508.08699). Modern TESS
  asteroseismic detection of δ Pav: ν_max = 2269.8 ± 64.4 µHz,
  Δν = 107.9 ± 0.2 µHz (no published modeled M/R/age).
- **Spada F. et al. 2011** — *Stellar evolutionary models*
  (`2011MNRAS.416..447S`, arXiv:1105.3125). Subgiant evolutionary
  context for δ Pav's mass/age.
- **Mawet D. et al. 2017** — *Characterization of Exoplanets from
  Their Formation. I.* (`2017AJ....153...44M`, arXiv:1609.06163).
  NIRC2 vortex coronagraph; companion limits ~3 M_Jup at >1 AU.
- **Lannier J. et al. 2017** — *Combining direct imaging and radial
  velocity* (`2017A&A...603A..54L`, arXiv:1705.03477). δ Pav in the
  SPHERE direct-imaging survey; no companions detected.
- **Tinney C. G. et al. 2005** — *The Anglo-Australian Planet Search*
  (`2005ApJ...623L.121T`). RV monitoring of δ Pav; no planet
  detection — the RV non-detection baseline.
- **Henry T. J. et al. 1996** — *A survey of Ca II H and K
  chromospheric emission in southern solar-type stars*
  (`1996AJ....111..439H`). log R'HK = −4.999; corroborates the
  inactive classification.
- **Hünsch M. et al. 1998** — *ROSAT all-sky survey catalogue of
  nearby stars* (`1998A&AS..132..155H`). δ Pav X-ray detection,
  0.073 ct/s → log L_X ≈ 27.3 cgs.
- **Gray R. O. et al. 2006** — *NStars: Spectral Classifications of
  Nearby Stars* (`2006AJ....132..161G`, arXiv:astro-ph/0603770).
  Confirms the G8IV classification.

## Open items for follow-up

- **Asteroseismic mass/age from the TESS modes**. Lund 2025 published
  ν_max + Δν for δ Pav but no modeled M/R/age. A scaling-relation or
  grid-modeled solution (or a PLATO campaign resolving rotational
  splitting) would tighten the mass and resolve the Holmberg-vs-Bensby
  age divergence (9.3 vs 4.9 Gyr), raising `age_gyr` Confidence to high.
- **Photometric rotation period**. TESS Cycle 4+ should observe δ Pav
  (favorable southern declination); a clean rotation-period detection
  would replace the current Confidence=low ~35 d estimate.
- **Metallicity uncertainty**. The Bensby 2014 catalog [Fe/H]
  uncertainty was not cleanly pinned; the adopted +0.36 ± 0.02 (Gomes
  da Silva 2021) should be cross-checked against Bensby's formal error
  if a future pass needs a tighter abundance.

## Related

- [methodology](../reference/methodology.md) — schema source for the Decisions table
- [alpha-centauri-a](alpha-centauri-a.md) — G2V comparison anchor (cream-white at 5847 K vs δ Pav's amber-cream at 5571 K)
- [conflict-resolution](../../.claude/skills/nearstars-phase3/references/conflict-resolution.md) — tie-break policy used for visual tint and corona extent picks
