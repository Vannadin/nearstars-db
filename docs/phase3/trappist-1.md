# TRAPPIST-1 — Phase 3 Synthesis

TRAPPIST-1 (2MASS J23062928−0502285) is the ultra-cool dwarf hosting
the nearby seven-planet resonant chain — an M8 V star at a Gaia DR3
distance of 12.47 pc (parallax 80.21 mas), with seven Earth-sized
worlds at orbital periods of 1.5–19 days. It is one of the smallest,
coldest, and faintest exoplanet host stars characterized to date:
log L*/L☉ = −3.28, just 0.052% of Sol's bolometric output. The
fundamental parameters have been refined repeatedly since the
2016 discovery — most recently by Agol 2021's TTV-anchored model,
which the DB Phase 2 layer adopts as the recommended set: M* =
0.0898 ± 0.0023 M☉, R* = 0.1192 ± 0.0013 R☉, T_eff = 2566 ± 26 K.

The star is moderately active for its spectral type. K2 photometry
gives a rotation period of 3.295 ± 0.003 days (Vida 2017, confirmed
by Luger 2017), and the K2 light curve shows 42 detected flares over
80 days with energies spanning 10³⁰–10³³ erg (Vida 2017). Longer-baseline
Evryscope monitoring constrains the superflare (≥10³³ erg) rate to
4.2 +1.9/−0.2 per year (Glazier 2020). XMM-Newton detects a soft,
two-temperature corona at log L_X (cgs) = 26.6–26.9 (Wheatley 2017),
and HST/STIS resolves the Ly-α line — making TRAPPIST-1 the
coldest exoplanet host with a measured UV line (Bourrier 2017). The
star's age is 7.6 ± 2.2 Gyr (Burgasser & Mamajek 2017, concordance
of CMD, density, kinematics, no-lithium constraint, rotation, and
activity proxies), placing the planetary system in the long
post-pre-main-sequence equilibrium phase.

**Scenario choice for NearStars: a deeply red, slowly rotating
ultra-cool dwarf with moderate chromospheric activity, soft X-ray
corona, frequent low-energy flares plus rare superflares, evolving
magnetic-feature pattern, and a 7.6 Gyr age that has long since
shaped its seven irradiated rocky planets.** 24 cfg picks; 22
canonical-aligned, 2 tie-break (spot filling fraction and spot
temperature contrast, where the Roettenbacher dark-spot vs.
Morris bright-spot interpretations are both observation-consistent).

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | M8 V | high | Liebert & Gizis 2006; Gillon 2016; Burgasser 2017 (Gonzales 2019 gives M7.5 — DB tag M7.5e via Gaia conversion; M8 is the modal classification) |
| `mass_msun` | 0.0898 ± 0.0023 | high | Agol 2021 TTV-anchored evolutionary fit; converges with Van Grootel 2018 (0.089 ± 0.006) within 1σ |
| `radius_rsun` | 0.1192 ± 0.0013 | high | Agol 2021 SED+transit-density; Van Grootel 2018 gave 0.121 ± 0.003, Gonzales 2019 0.119 ± 0.003 |
| `teff_k` | 2566 ± 26 | high | Agol 2021 SED fit; Van Grootel 2018 gave 2516 ± 41, Gonzales 2019 gave 2628 ± 42 |
| `luminosity_lsun` | 5.22e-4 ± 0.19e-4 | high | Van Grootel 2018 parallax-revised bolometric flux; Gonzales 2019 gives 6.09e-4 from FIRE NIR SED |
| `metallicity_fe_h_dex` | +0.04 ± 0.08 | medium | Gillon 2017 NIR low-res spec; Burgasser 2017 CMD-position suggests +0.06; Van Grootel notes possible +0.4 to reconcile density |
| `age_gyr` | 7.6 ± 2.2 | high | Burgasser & Mamajek 2017 — concordance of CMD, density, no-Li, kinematics, rotation, activity proxies |
| `log_g_cgs` | 5.21 ± 0.06 | high | Gonzales 2019 SED-derived |
| `rotation_period_days` | 3.295 ± 0.003 | medium | Vida 2017 K2 short-cadence; Roettenbacher & Kane 2017 caveat: surface evolves; Spitzer epoch gave 0.819 d period — true rotation may be ~1 d (v sin i 6 km/s × R*) with K2's 3.3 d signal as an active-region lifetime |
| `v_sin_i_km_s` | 6 ± 2 | high | Reiners & Basri 2010 FeH Zeeman-broadened lines |
| `activity_log_lhalpha_lbol` | −4.7 (range −4.85 to −4.60) | high | Burgasser 2017 collation of Gizis 2000 / Reiners & Basri 2010 / Schmidt 2007 |
| `activity_log_lx_lbol` | −3.52 ± 0.17 | high | Wheatley 2017 XMM-Newton APEC fit |
| `x_ray_log_lx_cgs_quiescent` | 26.6–26.9 | high | Wheatley 2017 — L_X (0.1–2.4 keV) = (3.8–7.9) × 10²⁶ erg/s |
| `xuv_log_lxuv_lbol` | −3.1 (range 6–9 × 10⁻⁴) | high | Wheatley 2017 XMM extrapolation |
| `lyman_alpha_flux_erg_s_cm2_at_earth` | 0.05 +0.01/−0.02 | high | Bourrier 2017 HST/STIS reconstructed intrinsic line (at d = 12 pc); much weaker than L_X relation predicts → chromosphere quieter than corona |
| `magnetic_field_gauss_mean` | 600 +200/−400 | medium | Reiners & Basri 2010 FeH Zeeman; in Wheatley 2017 (Reiners & Basri 2010 referenced as "Reiners & Basri 2010" therein) the value is "~600 G" — weaker than mid-M average of 1.6 ± 0.9 kG |
| `flare_rate_per_day_e_above_e30_erg` | 0.53 | high | Vida 2017 — 42 flares over the K2 Campaign 12 baseline (~80 d), energies 1.26×10³⁰ – 1.24×10³³ erg |
| `flare_rate_superflare_per_year_e_above_e33_erg` | 4.2 +1.9/−0.2 | high | Glazier 2020 Evryscope+K2 combined cumulative-FFD |
| `flare_xuv_contribution_relative_quiescent_per_yr` | 1.35 +2.0/−0.15 | medium | Howard 2025 RADYN beam-heating model + TESS-band FFD scaled into 6–912 Å |
| `spot_filling_fraction_max` | 0.02 (1–5% allowed) | low | Tie-break: interesting-first. Roettenbacher 2017 dark-spot model + Morris 2018a bright-spot model both observation-consistent; cfg picks intermediate ~2% (Berdyugina-style TiO band modeling implies up to 5% for M8 at this activity level) |
| `spot_temperature_contrast_k` | +2800 (bright facular-plage interpretation) | low | Tie-break: interesting-first. Morris 2018a bright-spot model T_spot ≈ 5300 K fits both K2 modulation + Spitzer non-detection; Roettenbacher dark-spot T = 2200 K is the alternative; cfg picks bright because it explains the wavelength-dependent K2-vs-Spitzer disagreement and offers visually distinctive facular regions on the deep-red disk |
| `visual_surface_tint_hex_primary` | `#ff5520` (deep red-orange ultra-cool M8 V) | high | Blackbody at 2566 K + TiO/VO band suppression below 6500 Å; CIE chromaticity for 2566 K thermal continuum biased toward 1 μm peak |
| `visual_spot_tint_hex` | `#ffa860` (warm yellow-orange bright facular plage) | low | Tie-break paired with the bright-spot interpretation; warmer ~5300 K spots present as warmer cream-yellow patches against the red photosphere |
| `stellar_color_temp_k` | 2566 | high | Derived from Teff for cfg illumination color |
| `limb_darkening_alpha_h` | ~0.4 | low | Tie-break: no direct interferometric measurement for an M8 V; interpolated from Claret 2018 M-dwarf grid as on Proxima Cen |

## Surface synthesis

The photosphere of TRAPPIST-1 is the smallest and coldest of any
NearStars target star with a confirmed planetary system. The visible
disk emits at T_eff = 2566 K (Agol 2021), with the spectral energy
distribution heavily depressed shortward of 6500 Å by molecular TiO
and VO opacity — most of the radiated flux emerges in the
1–3 μm range (Wilson 2021 Mega-MUSCLES). The bolometric luminosity
is just 5.22 × 10⁻⁴ L☉ (Van Grootel 2018), about 1/1900 of Sol.

**Color choice.** The blackbody chromaticity for 2566 K places the
human-perceived color in the deep orange-red, near `#ff5520`, with
the band-suppression effect on the bluer continuum biasing the
visual signature even further into the red. Compared to the Proxima
Centauri tint `#c54c2a` (2980 K), TRAPPIST-1 is darker and more
saturated. From any habitable-zone planet — e and f at 0.029
and 0.038 AU — the star fills 1.8–2.5° angular diameter, several
times the Sun's apparent diameter from Earth.

**Photospheric inflation.** TRAPPIST-1's measured stellar density
(51 ρ☉, Delrez via Van Grootel 2018) is lower than solar-metallicity
evolutionary models predict for a 0.089 M☉, 7.6 Gyr star. The radius
appears inflated by 8–14% relative to the BHAC15 / CLES isochrone
predictions (Burgasser 2017, Van Grootel 2018). Two interpretations
remain viable: enhanced metallicity (perhaps approaching [Fe/H] = +0.40)
that inflates the envelope via increased opacity, and magnetic-activity
inflation through suppressed convective transport. Gonzales 2019 adds
a third hypothesis — tidal forcing from the seven planets keeping the
star's outer layers slightly inflated. None of these can be
definitively distinguished with current data; for cfg purposes the
adopted R = 0.1192 R☉ (Agol 2021) is well-measured directly from
transit duration + TTV-derived M, regardless of the inflation
mechanism.

**Surface features.** TRAPPIST-1's spotted surface is one of the most
contested topics in its activity literature, with two viable
interpretations. Roettenbacher & Kane 2017 model the 3.3-day K2
variability with cool dark spots at T_spot ≈ 2200 K, comparable in
contrast to typical mid-M dwarfs. This model explains the K2 light
curve but predicts comparable variability at Spitzer 4.5 μm, which is
not observed (the Spitzer epoch instead shows a 0.819-day period
suggestive of evolved active regions). Morris 2018a explains the
wavelength-dependent observations with three bright spots at
T_spot ≳ 5300 K and tiny areal extent (R_spot / R* ≈ 0.004 each).
These hot patches dominate the Kepler bandpass where the photospheric
emission is heavily suppressed by molecular bands, but contribute
negligibly at 4.5 μm where the photospheric Planck function dominates.
Vasilyev 2025 adds JWST/NIRISS evidence for cool magnetic features —
"at most a few hundred K below the photosphere" — that occasionally
disappear during flares.

For the NearStars cfg, the bright-spot picture is adopted as the
visual primary because it (a) explains the wavelength-dependent
photometric signatures self-consistently, (b) offers a visually
distinctive feature against the otherwise uniform red disk, and (c)
matches the post-flare brightening that Vasilyev 2025 attributes to
magnetic-feature disappearance. The dark-spot interpretation is
preserved as a cfg variant in Open items. Realistically, both
populations probably coexist on the disk.

## Atmosphere synthesis

TRAPPIST-1's stellar atmosphere — chromosphere, transition region,
corona — is characterized by Bourrier 2017 (Ly-α), Wheatley 2017
(X-ray), and Wilson 2021 (full UV-to-X-ray SED via the
Mega-MUSCLES program). The defining tension is that the X-ray
luminosity is comparable to Proxima Centauri's (log L_X cgs = 26.6–
26.9 vs. Proxima's quiescent ≈ 27.0), but the Ly-α line emission
is roughly three times weaker than predicted from the L_X →
L_Lyα relation calibrated on warmer M dwarfs. Bourrier 2017
interprets this as evidence that TRAPPIST-1's chromosphere is
moderately active while its corona retains warmer-M-dwarf flux
levels — consistent with the late M-dwarf trend toward decoupling
of the cooler atmospheric layers from the hot corona.

**Chromospheric activity.** log L_Hα / L_bol = −4.85 to −4.60
(Burgasser 2017 collation across multiple epochs). This places
TRAPPIST-1 in the moderate-activity bracket for M8 V — neither the
extremely quiet inactive M8 dwarfs nor the saturated-emission rapid
rotators. Equivalent width measurements span 2.3–7.7 Å of Hα emission
(Reiners & Basri 2010 / Schmidt 2007 / Burgasser 2015), with the
variation likely tracking either rotational modulation or the spot-
filling-fraction evolution that Roettenbacher 2017 documents.

**Coronal X-rays.** XMM-Newton observed TRAPPIST-1 for 30 ks in
December 2014 (Wheatley 2017), revealing a soft, two-temperature
APEC plasma at kT = 0.15 and 0.83 keV. Variability over the 7.8 hr
observation is statistically significant — likely a combination of
rotational modulation (covering ~23% of the then-assumed 1.4-day
period) and possible small flares. log L_X / L_bol = (2–4) × 10⁻⁴
puts the star in the saturated regime (Rossby number << 0.1; per
Roettenbacher 2017 §3.2). The integrated XUV luminosity is
log L_XUV / L_bol = (6–9) × 10⁻⁴, sufficient to drive hydrodynamic
mass loss from all seven planets (Bourrier 2017 calculations: total
escape rates from 13–46 ton/s scaled across the planets).

**Flares and the saturated-activity regime.** Vida 2017 catalogued
42 K2 flares spanning 1.26 × 10³⁰ to 1.24 × 10³³ erg over the K2
Campaign 12 baseline of ~80 days, giving a flare rate of
approximately 0.5/day above 10³⁰ erg. Cumulative-FFD analysis by Glazier 2020 extends the
distribution to superflares using two years of Evryscope ground-based
photometry, finding a rate of 4.2 +1.9/−0.2 superflares (≥10³³ erg)
per year — moderate by ultracool dwarf standards, low enough that
ozone-shielded habitable-zone atmospheres (if present) could
recover between events. Howard 2025 applied RADYN radiative-
hydrodynamic beam-heating models to six JWST-observed flares
(2.2–8.7 × 10³⁰ erg) and found relatively weak electron beams
(F_e = 10¹² erg/s/cm², E_cutoff ≤ 37 keV) compared to typical M-dwarf
flares — consistent with the lower-than-expected optical flare
temperatures noted by Maas 2022 and Howard 2023. Cumulatively,
flares contribute ~1.35 +2.0/−0.15 × the quiescent XUV emission
integrated over a year, so over the system's 7.6 Gyr the flaring
component has roughly doubled the total XUV irradiation history at
the planets relative to a non-flaring star of the same quiescent
luminosity.

**Magnetic field and dynamo.** Reiners & Basri 2010 measured a
mean Zeeman-broadened magnetic field of approximately 600 G from FeH
absorption lines — weaker than the mid-M average of 1.6 ± 0.9 kG.
TRAPPIST-1 is fully convective (M < 0.35 M☉), so the dynamo is
inevitably turbulent rather than α-Ω. The relatively slow rotation
(if 3.3 d is the true period; or ~1 d if Spitzer's faster modulation
is the actual rotation) combined with the kG-class field puts the
star in the saturated activity regime (Roettenbacher 2017 §3.2),
where additional rotation would not increase the magnetic flux. Wilson
2021 Mega-MUSCLES provides the full UV-to-X-ray SED including a
Differential Emission Measure model for the unobserved 100–912 Å
EUV — a critical input for atmospheric escape calculations on the
planets.

## Rotation & spin synthesis

TRAPPIST-1's photometric rotation period has been a source of
considerable confusion. The discovery paper (Gillon 2016) reported
P_rot = 1.40 ± 0.05 d from TRAPPIST-South ground photometry,
consistent with the v sin i = 6 ± 2 km/s rotational velocity from
Reiners & Basri 2010 if R = 0.117 R☉ and i = 90°. K2 Campaign 12
short-cadence observations gave a strong 3.295 ± 0.003 d signal
(Vida 2017, Luger 2017) that is the canonical literature value.
Spitzer observations 76 days before the K2 epoch, however, show a
0.819-day periodicity consistent with the v sin i prediction
(Roettenbacher & Kane 2017). 

The Spitzer/K2 disagreement implies that the surface evolves on
weeks-to-months timescales — possibly fast enough that the "rotation
period" measured photometrically is in fact an active-region
lifetime rather than the literal stellar spin period (Morris 2018a
makes the same argument). For the cfg we adopt P_rot = 3.295 d
(Vida 2017) as the canonical literature value, with the caveat that
the underlying spin period may be closer to ~1 d. This matters for
the saturated-activity dynamo discussion (Section 4) but does not
materially change the cfg visual rendering at typical KSP framerates.

**Differential rotation.** Vida 2017 detected a possible second
photometric period at 2.915 d after pre-whitening the K2 light
curve with the 3.295-day signal. If both signals represented true
rotation at different latitudes, the implied surface shear (P_1 − P_2)/P̄
≈ 0.12 would be too large for a fully convective M dwarf and is
considered inconsistent with the deep-convection physics. The
secondary signal is more likely a finite-lifetime active region
than a differential-rotation signature.

**Inclination of the spin axis.** No direct measurement exists for
TRAPPIST-1's rotation axis. The planetary orbital plane is inclined
89.7°–89.9° to the line of sight (Agol 2021); if the stellar spin is
roughly aligned with the orbital plane (as in Brady 2022 obliquity
constraints from MAROON-X), the rotation axis tilts ≈ 60° from the
line of sight (cfg-adopted value). For KSP rendering, this gives a
visible polar tilt rather than the equator-on view that would happen
for an exactly aligned binary system.

**KSP implementation note.** Sidereal rotation period in seconds =
3.295 d × 86400 s/d = 284,688 s. The Kopernicus `rotationPeriod`
should be set to this value (or the alternative 0.819 d ≈ 70,766 s
if the cfg variant chooses the Spitzer-epoch interpretation).

**No detected activity cycle.** Roettenbacher & Kane 2017 search the
combined K2+Spitzer epoch for periodicities longer than the rotation
period and find no compelling cycle signal. Wargelin 2024 found a
~7-yr cycle for Proxima Centauri using comparable X-ray + UV
monitoring, but TRAPPIST-1 has not been observed long enough for a
similar detection. Until a multi-decade XMM/Swift campaign closes
this gap, the cfg treats the X-ray + Hα emission as steady at
quiescent levels with stochastic flare events on top.

## Visual styling

In the NearStars renderer, TRAPPIST-1 is portrayed as a tiny, deeply
red-orange ultra-cool dwarf — visibly smaller and redder than
Proxima Centauri.

- **Global appearance.** Disk color `#ff5520` (deep orange-red at
  2566 K blackbody peak); apparent angular diameter at typical
  habitable-zone distances 1.5–5.5° (b at 5.5°, e at 1.8°, h at
  0.85°). The disk is among the smallest absolute physical sizes
  in the catalog at 0.1192 R☉ (about 82,930 km radius, comparable
  to Jupiter's equatorial radius). From b at 0.0115 AU, TRAPPIST-1
  is the largest single object in the sky.
- **Photospheric texture.** Granulation pattern at sub-arcsecond
  scale (M-dwarf granules ~30 km, scaled with pressure scale height)
  — visible only on extreme close-up rendering. The disk shows mild
  limb darkening (cfg α ≈ 0.4 H-band per the Claret 2018 M-dwarf
  grid extrapolation), with the deepest red at the limb.
- **Bright spots.** Three to five bright facular-plage features at
  T ≈ 5300 K appear as small warm-yellow-cream patches against the
  deep red disk (cfg `#ffa860` accent), each covering ~0.005% of the
  visible disk. These bright spots rotate into and out of view on
  the 3.3-day cycle. Per Vasilyev 2025, occasional flares trigger
  the disappearance of cooler dark magnetic features — a visual
  effect that can be implemented as a flare-time spot population
  shift in the cfg.
- **Dark spots (cfg variant).** Alternative interpretation
  (Roettenbacher 2017): cool dark spots at T ≈ 2200 K covering
  ~1–5% of the disk in patchy distribution. The dark-spot variant
  is preserved as a cfg variant for users who prefer the canonical
  M-dwarf dark-spot picture.
- **Flares.** Cumulative rate ~0.5/day above 10³⁰ erg (Vida 2017),
  with superflares (≥10³³ erg) at 4.2/yr (Glazier 2020). The Vida
  data show ~12% of flares are complex multi-peaked events. Visually,
  the cfg should brighten the star by 0.5–2 mag in the optical for
  10³¹ erg events, lasting 10 min – 1 hr with characteristic Davenport
  2014 fast-rise / slow-decay shape. The white-light flare spectrum
  is dominated by hydrogen Balmer continuum + Hα emission, so the
  flare-time color shifts slightly toward orange-red (Howard 2025
  RADYN models predict 2000–4500 K effective flare temperature).
- **Corona.** Faint blue-white halo extending out to ~2 R* during
  quiescent X-ray phases (Wheatley 2017 cycle minimum); brightens
  during flares and during the (unobserved) activity cycle peaks.
- **Stellar wind.** Not directly visible but propagates as
  in-game space-weather events affecting planetary magnetospheres
  (Garraffo 2017 simulations).
- **Lyman-α emission.** Resolved by HST/STIS (Bourrier 2017) — for
  KSP this is below the rendering threshold but represents the
  primary source of UV photolysis on the planetary atmospheres.

The seven planets are visually compact in TRAPPIST-1's sky from each
other's perspective — at conjunction, neighboring planets can reach
0.5–1° angular size, making them prominent "moons" of the host
system. The near-coplanar configuration (i = 89.7°–89.9° per Agol
2021) means most planet–planet conjunctions are also near-
transits/eclipses, with frequent mutual occultations every few days.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Van Grootel V. et al. 2018** — *Stellar Parameters for TRAPPIST-1*,
  ApJ 853, 30 (`2018ApJ...853...30V`, arXiv:1712.01911). Revised
  parallax 82.4 ± 0.8 mas; final stellar parameters M = 0.089 ± 0.006 M☉,
  R = 0.121 ± 0.003 R☉, T_eff = 2516 ± 41 K, L = (5.22 ± 0.19) × 10⁻⁴ L☉.
  Documents the radius-inflation tension with solar-metallicity
  evolutionary models.
- **Burgasser A. J. & Mamajek E. E. 2017** — *On the Age of the
  TRAPPIST-1 System*, ApJ 845, 110 (`2017ApJ...845..110B`,
  arXiv:1706.02018). Concordance age 7.6 ± 2.2 Gyr from CMD,
  density, no-Li, surface gravity, kinematics, rotation, and
  magnetic activity proxies. Defines log L_Hα/L_bol = −4.85 to
  −4.60 dex; log L_X/L_bol = −3.52 ± 0.17 dex; v sin i = 6 km/s.
- **Vida K. et al. 2017** — *Frequent flaring in the TRAPPIST-1
  system — unsuited for life?*, ApJ 841, 124
  (`2017ApJ...841..124V`, arXiv:1703.10130). K2 Campaign 12
  short-cadence Fourier analysis; P_rot = 3.295 ± 0.003 d; 42
  flares with energies 1.26 × 10³⁰ – 1.24 × 10³³ erg; 12% complex.
- **Wheatley P. J. et al. 2017** — *Strong XUV irradiation of the
  Earth-sized exoplanets orbiting the ultracool dwarf TRAPPIST-1*,
  MNRAS 465, L74 (`2017MNRAS.465L..74W`, arXiv:1605.01564). XMM-Newton
  30 ks; two-temperature APEC corona; L_X/L_bol = 2–4 × 10⁻⁴;
  L_XUV/L_bol = 6–9 × 10⁻⁴.
- **Bourrier V. et al. 2017** — *Reconnaissance of the TRAPPIST-1
  exoplanet system in the Lyman-α line*, A&A 599, L3
  (`2017A&A...599L...3B`, arXiv:1702.07004). HST/STIS Ly-α
  reconstructed line profile; coldest exoplanet host with measured UV;
  Ly-α much weaker than expected from L_X relation — implies cooler
  atmosphere quieter than corona.
- **Roettenbacher R. M. & Kane S. R. 2017** — *The Stellar Activity
  of TRAPPIST-1 and Consequences for the Planetary Atmospheres*,
  ApJ 851, 77 (`2017ApJ...851...77R`, arXiv:1711.02676). K2 vs.
  Spitzer photometric period disagreement (3.30 d vs. 0.819 d);
  evolving spot pattern; dark-spot model with T_spot ≈ 2200 K.
- **Morris B. M. et al. 2018** — *Possible Bright Starspots on
  TRAPPIST-1*, ApJ 857, 39 (`2018ApJ...857...39M`, arXiv:1803.04543).
  Bright-spot interpretation with three spots, R_spot/R* ≈ 0.004,
  T_spot ≳ 5300 K. Resolves the K2/Spitzer wavelength-dependent
  amplitude disagreement.
- **Wilson D. J. et al. 2021** — *The Mega-MUSCLES Spectral Energy
  Distribution of TRAPPIST-1*, ApJ 911, 18 (`2021ApJ...911...18W`,
  arXiv:2102.11415). 5 Å – 100 μm SED combining HST COS+STIS, XMM-
  Newton, and DEM models; semi-empirical UV spectrum for
  atmospheric modeling of the planets.
- **Glazier A. L. et al. 2020** — *Evryscope and K2 Constraints on
  TRAPPIST-1 Superflare Occurrence and Planetary Habitability*,
  ApJ 900, 27 (`2020ApJ...900...27G`, arXiv:2006.14712). Combined
  170 nights Evryscope + 80 d K2; cumulative superflare rate (≥10³³
  erg) = 4.2 +1.9/−0.2 per year.
- **Vasilyev V. et al. 2025** — *Flares on TRAPPIST-1 Reveal the
  Spectrum of Magnetic Features on Its Surface*, ApJ 989, L53
  (`2025ApJ...989L..53V`, arXiv:2508.04793). Post-flare flux
  enhancement in JWST/NIRISS; interpreted as flare-triggered
  disappearance of dark magnetic features; first inferred spectrum
  of an M8 active region.
- **Howard W. S. et al. 2025** — *Separating Flare and Secondary
  Atmospheric Signals with RADYN Modeling of JWST Transmission
  Spectroscopy*, ApJ 994, L31 (`2025ApJ...994L..31H`,
  arXiv:2512.04265). RADYN beam-heating models for six JWST flares;
  TESS-to-XUV scaling factor R_XUV/TESS = 3.6 +0.6/−2.5; cumulative
  flare XUV = 1.35 × quiescent.
- **Gonzales E. C. et al. 2019** — *A Reanalysis of the Fundamental
  Parameters and Age of TRAPPIST-1*, ApJ 886, 131
  (`2019ApJ...886..131G`, arXiv:1909.13859). FIRE NIR spectroscopy
  + Gaia parallax; log L_bol = −3.216 ± 0.016; T_eff = 2628 ± 42 K;
  intermediate-gravity classification suggesting either magnetic
  inflation or tidal interaction with planets.

### Read (context / methodology, not decision-driving)

- **Gillon M. et al. 2016** — *Temperate Earth-sized planets
  transiting a nearby ultracool dwarf star*, Nature 533, 221
  (`2016Natur.533..221G`, arXiv:1605.07211). Discovery paper;
  original stellar parameters M = 0.082 ± 0.011 M☉, R = 0.114 ±
  0.006 R☉, T = 2555 ± 85 K, P_rot = 1.40 ± 0.05 d (TRAPPIST-South
  ground photometry, now superseded by K2).
- **Gillon M. et al. 2017** — *Seven temperate terrestrial planets
  around the nearby ultracool dwarf star TRAPPIST-1*, Nature 542, 456
  (`2017Natur.542..456G`, arXiv:1703.01424). Spitzer 20-day campaign
  + planet discovery; [Fe/H] = +0.04 ± 0.08 from NIR spectroscopy.
- **Luger R. et al. 2017** — *A seven-planet resonant chain in
  TRAPPIST-1*, Nature Astronomy 1, E.129 (`2017NatAs...1E.129L`,
  arXiv:1703.04166). K2 Campaign 12 observation; confirms P_rot =
  3.3 d; characterizes TRAPPIST-1 as "low-activity, middle-aged,
  late M dwarf".
- **Reiners A. & Basri G. 2010** — *A Volume-Limited Sample of 63
  M7-M9.5 Dwarfs II. Activity, Magnetism, and the Fade of the
  Rotation-Dominated Dynamo*, ApJ 710, 924 (`2010ApJ...710..924R`,
  arXiv:0912.4259). Mean magnetic field 1.6 ± 0.9 kG for M7-M9.5
  sample; TRAPPIST-1 specifically at ~600 G (referenced by
  Wheatley 2017 and Burgasser 2017).
- **Filippazzo J. C. et al. 2015** — *Fundamental Parameters and
  Spectral Energy Distributions of Young and Field Age Objects
  with Masses Spanning the Stellar to Planetary Regime*, ApJ 810,
  158 (`2015ApJ...810..158F`, arXiv:1508.01767). Baseline SED-fit
  fundamental parameters for ultracool dwarfs including TRAPPIST-1;
  pre-Van Grootel reference.
- **Reiners A. et al. 2018** — *The CARMENES search for exoplanets
  around M dwarfs. High-resolution optical and near-infrared spectra
  of 324 survey stars*, A&A 612, A49 (`2018A&A...612A..49R`,
  arXiv:1711.06576). CARMENES Zeeman-broadening survey methodology;
  TRAPPIST-1 in the M-dwarf comparison sample.
- **Garraffo C. et al. 2017** — *The Threatening Magnetic and
  Plasma Environment of the TRAPPIST-1 Planets*, ApJ 843, L33
  (`2017ApJ...843L..33G`, arXiv:1706.04617). MHD stellar-wind
  simulations; sub-Alfvénic crossings for ~50% of inner-planet
  orbits.
- **Ducrot E. et al. 2020** — *TRAPPIST-1: Global results of the
  Spitzer Exploration Science Program SPECULOOS*, A&A 640, A112
  (`2020A&A...640A.112D`, arXiv:2006.13826). 5-year Spitzer
  campaign; alternative stellar density / R = 0.1234 R☉
  measurement; superseded by Agol 2021 in DB.
- **Paudel R. R. et al. 2018** — *K2 Ultracool Dwarfs Survey III.
  White Light Flares Are Ubiquitous in M6-L0 Dwarfs*, ApJ 858, 55
  (`2018ApJ...858...55P`, arXiv:1803.07708). M6-L0 flare statistics;
  TRAPPIST-1 in the ultracool dwarf flare-rate-vs-age context.
- **Morris B. M. et al. 2018b** — *Non-detection of Contamination
  by Stellar Activity in the Spitzer Transit Light Curves of
  TRAPPIST-1*, ApJ 863, L32 (`2018ApJ...863L..32M`,
  arXiv:1808.02808). Spitzer transit-timing residuals show no
  spot-crossing signatures; constrains the spot-on-transit-chord
  configuration.

### Read (instrument / non-cfg-decisive)

- **Davoudi F. et al. 2024** — *Updated Spectral Characteristics
  for the Ultracool Dwarf TRAPPIST-1*, ApJ 970, L4
  (`2024ApJ...970L...4D`). NIR spectral indices updated; no
  cfg-decisive parameters revised.
- **Seli B. et al. 2021** — *Activity of TRAPPIST-1 analogue stars
  observed with TESS*, A&A 650, A138 (arXiv:2103.13540).
  Comparison sample of M8 V dwarfs; provides flare-rate context
  but no TRAPPIST-1-specific new measurements.
- **TRAPPIST-1 JWST Community Initiative et al. 2024** — *A
  roadmap for the atmospheric characterization of terrestrial
  exoplanets with JWST* (arXiv:2310.15895). System-level
  observational program rationale; cites stellar parameters from
  Agol 2021 + activity from Wilson 2021.
- **Howard W. S. et al. 2023** — *Characterizing the Near-infrared
  Spectra of Flares from TRAPPIST-1 during JWST Transits*, ApJ
  959, 64 (`2023ApJ...959...64H`, arXiv:2310.03792 — full text
  fetch failed, only abstract available). Predecessor to Howard
  2025; characterizes lower-than-expected flare temperatures.

### Not read — no arXiv preprint or low-priority (~280 papers)

The stellar-focused bibliography includes ~280 lower-relevance papers
filtered to `status: skipped` in `_bib/trappist-1.yaml`. Categories:

- Mid-to-late-M-dwarf statistical papers that include TRAPPIST-1 in
  a sample but do not characterize it individually (~80 papers)
- Planet-atmospheric-modeling papers that cite TRAPPIST-1 stellar
  parameters but contribute no new stellar measurement (~50 papers,
  many already covered in per-planet bibs b–h)
- Conference proceedings, abstracts, mission-concept papers without
  arXiv (~80 papers)
- SETI / radio-technosignature surveys targeting TRAPPIST-1 (~10 papers)
- Pre-discovery brown-dwarf / ultracool-dwarf surveys with TRAPPIST-1
  as one of many targets (~30 papers)
- Theoretical M-dwarf habitability papers using TRAPPIST-1 as a
  reference target (~30 papers)

The full filtered bib is preserved in
`docs/phase3/_bib/trappist-1.yaml` with `status: skipped` annotations
on every dropped entry.

## Open items for follow-up

- **Spot model resolution.** The dark-spot (Roettenbacher 2017) vs.
  bright-spot (Morris 2018a) interpretations remain
  observation-degenerate. A dedicated multi-band JWST + ground
  campaign (or future ELT high-resolution disk imaging) could
  break the degeneracy. Cfg variant: dark-spot scenario with
  T_spot = 2200 K and 1–5% filling fraction.
- **True rotation period.** Whether the actual stellar spin is the
  K2-derived 3.295 d (Vida 2017) or closer to 0.819 d (Spitzer epoch,
  Roettenbacher 2017) is not resolved. v sin i = 6 km/s favors the
  shorter period for any reasonable R. A long-baseline multi-band
  photometric campaign tracking the periodicity-vs-epoch evolution
  would clarify whether the photometric signal is rotational or
  active-region-lifetime in origin.
- **Activity cycle detection.** No clear chromospheric or coronal
  cycle has been detected. Comparison with Proxima Cen's 7-yr
  X-ray cycle (Wargelin 2024) motivates a TRAPPIST-1 multi-decade
  XMM/Chandra monitoring program. Cfg phase synchronization at
  J2000.0 currently arbitrary; if a cycle is detected, the cfg's
  activity-driven CME flux can track real-time progression.
- **Radius inflation mechanism.** The 8–14% radius inflation over
  solar-metallicity evolutionary models (Burgasser 2017, Van Grootel
  2018) remains unexplained. High-resolution optical spectroscopy
  for α-element abundances (Veyette 2016 method) could test the
  high-metallicity hypothesis. Alternatively, deeper magnetic-
  activity modeling (Feiden & Chaboyer 2014) could test the
  spot-blocking interpretation.
- **Howard 2023 (arXiv:2310.03792) full text refetch.** The arXiv
  full-text fetch failed during this synthesis pass; only the
  abstract was available for the bibliography entry. A retry against
  ar5iv (or manual paste) would let the cfg record the specific
  near-infrared flare effective temperatures.
- **Re-check Gillon 2016 TRAPPIST-South 1.40-d photometric period.**
  Roettenbacher 2017 dismisses it as a spot-active-region artifact;
  if the bright-spot Morris 2018a interpretation is correct, the
  1.40 d could be physical — half the K2 period from a two-spot
  symmetric configuration. The cfg adopts 3.295 d without prejudice.

## Related

- [trappist-1-b](trappist-1-b.md) through [trappist-1-h](trappist-1-h.md) — the seven Earth-sized planets in the resonant chain
- [proxima-cen](proxima-cen.md) — nearest M-dwarf comparison; warmer (2980 K vs 2566 K), faster-rotating (82.6 d vs 3.3 d), more energetic flares
- [methodology](../reference/methodology.md) — DB schema for the Decisions table
- [mod-reference](../reference/mod-reference.md) — downstream KSP mods consuming these Phase 3 stellar values
- [rex-data-comparison](../reference/rex-data-comparison.md) — §10 quantifies the Phase 3 → REX delta for the TRAPPIST-1 system
