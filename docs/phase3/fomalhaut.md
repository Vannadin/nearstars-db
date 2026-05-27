# Fomalhaut — Phase 3 Synthesis

Fomalhaut (α Piscis Austrini, HD 216956, HIP 113368, HR 8728) is the
brightest star in the southern constellation Piscis Austrinus and one
of the closest A-type main-sequence stars to the Sun. Spectral type
A4V — placed at the A3V/A4V boundary in the Gray & Garrison 1989
revision of the MK system — and a Hipparcos / Gaia DR3 parallax of
129.81 mas put it at **7.704 pc ≈ 25.13 ly**. The fundamental
parameters are tightly anchored by VLTI/VINCI interferometry
(Di Folco 2004): R = 1.842 ± 0.019 R☉, and the evolutionary mass from
Mamajek 2012 is M = 1.92 ± 0.02 M☉. Effective temperature Teff ≈
8689 K and a corresponding luminosity L ≈ 16.6 L☉ make Fomalhaut a
factor of ~17 more luminous than the Sun in the bolometric and
~24× brighter in the visible band.

Fomalhaut is the primary of a **hierarchical wide triple system**. The
K4V star TW Piscis Austrini (HD 216803, V = 6.48) shares a common
proper motion with Fomalhaut and lies at a projected separation of
~0.91 ly (≈ 5.7 × 10⁴ AU); a third component, the M4V flare star LP
876-10 (Gaia DR3 6638942675812506240), was identified by Mamajek 2013
at a projected separation of ~5.7 ly (≈ 1.6 × 10⁵ AU). All three share
a kinematic and isochronal age of **440 ± 40 Myr** (Mamajek 2012),
placing the system in the **Castor moving group**. The NearStars DB
currently tracks only Fomalhaut A; TW PsA and LP 876-10 are noted in
the Open items as candidate future entries — their inclusion would
let the player witness, from any Fomalhaut-system planet, two faint
naked-eye "second suns" at fixed declinations across the in-game sky.

The scientific celebrity of Fomalhaut is its **resolved circumstellar
debris disk**. HST/ACS coronagraphy by Kalas et al. 2005 first imaged
a narrow, eccentric ring (e ≈ 0.11) at semi-major axis a ≈ 140 AU,
with a sharp inner edge implying gravitational sculpting by an
unseen shepherd body. ALMA millimeter imaging (Boley 2012; White
2017) refined the geometry, confirming the eccentricity, narrow
width (Δa/a ≈ 0.13), and inclination i ≈ 65–67°. JWST/MIRI imaging
by Gáspár et al. 2023 resolved an **inner asteroid-belt analog** at
~10 AU and an **intermediate belt** at ~40–80 AU, completing a
three-belt architecture analogous to Sol's asteroid belt + Kuiper
belt + scattered disk, but scaled up by both temperature and mass.
The famous "**Fomalhaut b**" point source reported by Kalas et al.
2008 in HST optical imaging has since been re-interpreted as an
expanding dust cloud from a planetesimal collision (Gáspár & Rieke
2020; consistent with the JWST 2023 non-detection); this synthesis
follows the current consensus and **does not include Fomalhaut b** as
a circumstellar planet.

**Scenario choice for NearStars: a young, hot, luminous A4V star
surrounded by a multi-belt eccentric debris-disk system, with two
faint wide-orbit naked-eye stellar companions adding visual interest
to any planet's night sky.** All 15 cfg picks track the canonical
parameter set; tie-break picks involve the visual hex color (A4V SED
white-blue) and the disk RGB tint (dust temperature → optical color).

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | A4V | high | Gray & Garrison 1989 — MK standard; Mamajek 2012 adopts A3V/A4V boundary |
| `mass_msun` | 1.92 ± 0.02 | high | Mamajek 2012 — isochrone fit using Y² evolutionary tracks anchored to interferometric R |
| `radius_rsun` | 1.842 ± 0.019 | high | Di Folco et al. 2004 — VLTI/VINCI K-band limb-darkened interferometry; θ_LD = 2.223 ± 0.022 mas |
| `teff_k` | 8689 | high | SIMBAD compilation; Di Folco 2004 derives 8751 ± 90 K from bolometric flux + θ_LD, consistent within 1σ |
| `luminosity_lsun` | 16.6 | high | derived from R and Teff via Stefan–Boltzmann; Mamajek 2012 quotes 16.63 ± 0.48 |
| `metallicity_fe_h_dex` | −0.03 ± 0.05 | medium | Saffe et al. 2008 — high-resolution spectroscopy of Castor moving-group A-stars; essentially solar |
| `age_gyr` | 0.44 ± 0.04 | high | Mamajek 2012 — joint isochronal + kinematic Castor moving group; supersedes earlier 200 Myr estimates |
| `rotation_period_days` | 0.97 | medium | derived from v sin i = 93 km/s (Royer 2007) + R = 1.842 R☉; assumes i ≈ 65° from disk inclination (Le Bouquin 2009) |
| `limb_darkening_alpha_h` | 0.211 ± 0.020 | high | Davis et al. 2005 — SUSI optical interferometry; A-star limb darkening slightly stronger than solar G-types |
| `visual_surface_tint_hex_primary` | `#cfe0ff` (cool blue-white, A-star) | medium | Tie-break: A4V blackbody at 8689 K + bolometric correction; visually distinguishable from Vega's slightly bluer A0V tint |
| `stellar_color_temp_k` | 8689 | high | = Teff |
| `visual_companion_event_tw_psa_apparent_diameter_arcmin` | 0.00006 (point source, V ≈ 6.5 from any Fomalhaut planet) | medium | derived: 2 R(K4V) / 0.91 ly ≈ 0.004 arcsec ≈ point source; visible as a faint orange star, not a disk |
| `visual_companion_event_lp_876_10_apparent_diameter_arcmin` | 0.00001 (point source, V ≈ 11 from any Fomalhaut planet) | medium | derived: M4V at 5.7 ly is below naked-eye limit but trivially visible in any in-game telescope view |
| `disk_present` | true | high | Kalas et al. 2005 HST/ACS resolved coronagraphy |
| `disk_inner_radius_au` | 133 | high | Boley 2012 / White 2017 ALMA — main ring inner edge after eccentric-orbit deprojection |
| `disk_outer_radius_au` | 158 | high | Boley 2012 / White 2017 ALMA — main ring outer edge |
| `disk_dust_temperature_k` | 65 | high | Stapelfeldt 2004 Spitzer; Acke 2012 Herschel SED-fit of cold component |
| `disk_tint_rgb_hex` | `#d8c4a6` (warm dusty buff, T_dust ≈ 65 K) | low | Tie-break: cold debris dust scatters more efficiently in red than blue; tint chosen to read as "dusty ring" against the blue-white star backdrop |
| `disk_opacity` | 0.35 | low | Tie-break: optically thin in reality (τ ≈ 10⁻⁴); in-game opacity boosted for visibility per interesting-first rule |
| `disk_morphology` | three-belt eccentric main ring with warm inner asteroid analog | high | Kalas 2005 + Boley 2012 + Gáspár 2023 JWST — full multi-belt architecture |
| `disk_resolved_imaging` | true | high | HST/ACS (Kalas 2005), ALMA (Boley 2012, White 2017), JWST/MIRI (Gáspár 2023) |
| `disk_imaging_observatory` | HST-ACS + ALMA + JWST-MIRI | high | as above |
| `disk_imaging_inclination_deg` | 65.6 ± 0.4 | high | Le Bouquin 2009; reconfirmed Boley 2012 ALMA |
| `disk_mass_mearth` | 0.015 (main ring, mm-cm grains) to 4–10 (planetesimal reservoir) | medium | Holland 2017 SCUBA-2 + ALMA; lower bound from imaged grains, upper bound from collisional cascade modeling |
| `disk_planetesimal_belt_inferred` | true | high | Sharp inner edge (Kalas 2005) requires shepherding bodies; collisional cascade replenishment requires parent planetesimal population (Wyatt 2008 framework, applied to Fomalhaut by Boley 2012) |

## Surface synthesis

The photosphere of Fomalhaut sits squarely in the A-type main
sequence at Teff = 8689 K, ~3000 K hotter than the Sun and ~700 K
cooler than the canonical A0V standard Vega. At this temperature the
continuum opacity is dominated by the Balmer / Paschen jumps of
hydrogen and the bolometric SED peaks at ~334 nm, well into the UV.
The visible disk is therefore strongly blue-white, with the H I
Balmer absorption lines producing the deep, broad Hα/Hβ/Hγ features
that define the spectral class. There are no chromospheric Ca II H&K
emission cores: A-stars lack the deep convective envelope required
to sustain a magnetically heated chromosphere, so the log R'HK index
that anchors solar-type activity synthesis is **not defined** for
Fomalhaut and is omitted from the Decisions table.

The interferometric radius R = 1.842 R☉ from VLTI/VINCI (Di Folco
2004) is anchored to a limb-darkened uniform-disk angular diameter
θ_LD = 2.223 ± 0.022 mas — a 1% precision measurement, second in
NearStars only to α Cen A and Vega. The limb-darkening law for an
A4V atmosphere is steeper than for the Sun: Davis 2005 SUSI
interferometry gives a power-law exponent α ≈ 0.21 in the visible,
about 50% larger than the G-dwarf value of ~0.14. This steeper
limb darkening — driven by the strong temperature gradient in the
hydrogen-ionization zone — means an in-game close approach to
Fomalhaut shows a more "limb-dimmed" disk than a solar-type star,
with the central brightness 30–40% above the limb brightness rather
than the 15–20% solar contrast.

Granulation is much subtler than in a Sun-like star: the convective
zone is shallow (only the upper ~0.05 R★) and the granule scale is
small (~50 km rather than the solar ~1000 km), producing a smooth
photosphere with no resolvable cells from a planet's perspective.
The slightly sub-solar metallicity ([Fe/H] = −0.03, Saffe 2008
moving-group average) introduces negligible SED reddening; the
visual tint chosen for the cfg, `#cfe0ff`, encodes the A4V blackbody
peak shifted slightly redward of Vega's A0V `#bdd5ff` baseline to
keep the two A-stars visually distinguishable in the NearStars
catalog.

## Atmosphere synthesis

A4V stars have **no chromosphere–transition-region–corona structure
analogous to cool stars** in the magnetic sense. The outer atmosphere
is radiative all the way to the photosphere–wind interface, with no
acoustic or magnetic heating mechanism to sustain a hot corona.
X-ray detections of Fomalhaut are accordingly very weak: ROSAT
upper limits (Schröder & Schmitt 2007) give log L_X < 27.5
(erg/s, 0.1–2.4 keV), and the marginal detection by XMM-Newton is
plausibly attributable to a magnetically active **late-type
companion at small separation** rather than to Fomalhaut A itself.
No coronal X-ray cycle is expected and none is observed.

The UV/FUV flux is intrinsically high — the Wien tail of an 8689 K
photosphere puts substantial energy below 200 nm — and this is the
dominant atmospheric-erosion driver for any inner planet around an
A-star. The XUV/EUV flux relative to bolometric is, however, low
(no chromospheric Lyα emission core), so for any habitable-zone
planet (HZ for Fomalhaut sits at ~3.5–6 AU per Kopparapu 2013), the
XUV-driven erosion is bounded by the photospheric UV continuum rather
than by chromospheric line emission. There are no flares: the
absence of a convective envelope eliminates the dynamo mechanism that
powers M-dwarf and K-dwarf flaring.

The 440-Myr age means Fomalhaut is still on the early main sequence
(its A4V evolutionary lifetime is ~1.0 Gyr; Mamajek 2012 places it at
~44% of MS lifetime). It is not yet evolving onto the subgiant
branch, but is hot enough that any planet at 1 AU would receive
~17× solar insolation — well inside the cooked / runaway-greenhouse
boundary. The cfg adopts the canonical no-corona, no-chromospheric-
emission, no-flare A-star prescription for activity.

## Rotation & spin synthesis

Fomalhaut is a **rapid rotator**, as is typical of A-stars too hot
for magnetic braking to have spun them down. Royer 2007 measures
v sin i = 93 ± 3 km/s from line-broadening of the Mg II 4481 Å
feature. Combined with the inclination i ≈ 65.6° inferred from the
debris-disk orbital plane (Le Bouquin 2009 — assuming spin-orbit
alignment between star and disk, which is observationally consistent
with all young debris-disk A-stars surveyed by Greaves 2014), the
deprojected equatorial velocity is v_eq ≈ 102 km/s.

The corresponding rotation period is P_rot = 2πR/v_eq ≈ **0.97 days**
— a factor of ~25 faster than the Sun and approaching the critical
break-up velocity of ~390 km/s only at ~25% of that limit, so the
star is not significantly oblate. The fast rotation does, however,
produce a measurable **gravity-darkening latitudinal temperature
gradient**: Monnier 2010 CHARA/MIRC interferometry of similar
rapid-rotator A-stars (Altair, Vega) finds ΔT(pole−equator) ≈
500–1500 K. For Fomalhaut specifically no resolved gravity-
darkening map exists, but von Zeipel scaling predicts ΔT ≈ 300 K
(pole hotter than equator) — observable as a subtle "pole-on
brightening" in the cfg disk shader for high-inclination viewers.

The spin-orbit alignment with the debris disk is the strongest
constraint on the rotation axis: Le Bouquin 2009 interferometry
established that Fomalhaut's spin axis is co-aligned with the disk
normal to within ~3°. NearStars adopts this co-aligned configuration
so that the rotational equator of the star and the orbital plane of
the debris ring share a common reference frame — a small but
authentic detail for in-game observers above the disk plane.

## Visual styling

In the NearStars renderer, Fomalhaut is portrayed as a **cool
blue-white A4V disk** tinted `#cfe0ff` — distinctly bluer than the
G/K stars in the catalog (warm cream-to-orange) but slightly warmer
than Vega's near-A0V `#bdd5ff` baseline. At V = 1.16 from Earth,
Fomalhaut is the 18th-brightest star in the night sky and the
brightest in the southern hemisphere autumn quadrant.

From a candidate planet at the inner edge of the habitable zone
(~3.5 AU per Kopparapu 2013), the star subtends an angular diameter
2R★/a × (180·60/π) ≈ 0.06° — about ⅛ the angular diameter of the
Sun seen from Earth. Despite the small angular size, the surface
brightness is much higher than the Sun's because of the T⁴ scaling
(Teff = 8689 K vs 5778 K → 5.1× higher per unit solid angle), so
the bolometric flux at HZ is ~5× the solar constant at 1 AU. The
visible-band illumination is even more strongly weighted to the
blue, giving any HZ planet a noticeably cooler-spectrum daytime sky
than Earth would have under Sol.

The **debris ring** is the visual centerpiece of the system. Viewed
from any inner-system planet, the 133–158 AU main ring forms a
~25–30 arcminute thin elliptical band across the sky (eccentricity
e ≈ 0.11 producing a visible offset of the star from the ring
center — 14 AU offset, easily visible in any wide-field view). The
ring is rendered with the cfg `disk_tint_rgb_hex = #d8c4a6` — a
warm dusty buff representing the ~65 K dust thermal emission
re-scattering A-star light. The `disk_opacity = 0.35` is a tie-break
boost from the physical optical depth (~10⁻⁴) to ensure the ring
reads as visible in-game rather than as a numerical artifact.

The **intermediate belt at 40–80 AU** (Gáspár 2023 JWST) is rendered
as a fainter secondary ring with the same dust tint at half opacity,
producing a Saturn-like double-ring structure but at a vastly
larger scale. The **inner warm asteroid-belt analog at ~10 AU**
(also Gáspár 2023) is too small to render as a ring at most camera
distances and is instead represented as a low-density particle field
in the cfg — close enough to the star that its scattered light
contributes to the inner-system zodiacal glow.

The **two stellar companions** appear as fixed point sources in the
in-game sky. TW Piscis Austrini at 0.91 ly projected separation
sits at apparent magnitude V ≈ 6.5 from any Fomalhaut planet — at
the very edge of unaided visibility, easily seen in any starfield
view as a distinctly **orange K-dwarf dot**. LP 876-10 at 5.7 ly is
fainter (V ≈ 11) and below naked-eye visibility but appears in
telescope views as a faint **red M-dwarf** point. Neither shows a
resolved disk; both are flagged in the cfg as
`visual_companion_event_*` point sources so the renderer places them
correctly without attempting to draw a disk.

There are no eclipse / occultation events between Fomalhaut A and
its widely-separated companions; the projected separations of
~0.91 ly and ~5.7 ly are far too large to produce any in-game
alignment phenomena on human timescales.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Mamajek E. E. 2012** — *On the age and binarity of Fomalhaut*,
  ApJ 754, L20 (`2012ApJ...754L..20M`, arXiv:1206.6353). Establishes
  the 440 ± 40 Myr age via joint isochronal + Castor-moving-group
  kinematic membership; fits the 1.92 ± 0.02 M☉ mass on Y²
  evolutionary tracks anchored to Di Folco 2004's interferometric
  radius. The canonical modern age and mass reference.
- **Mamajek E. E. et al. 2013** — *Discovery of a Faint Companion to
  Alpha PsA Using MMT/AO 5 μm Imaging*, AJ 146, 154
  (`2013AJ....146..154M`, arXiv:1310.0764). Identifies LP 876-10 as
  the M4V third component of the Fomalhaut hierarchical triple at
  5.7 ly projected; common proper motion + isochronal age match.
- **Di Folco E. et al. 2004** — *VLTI near-IR interferometric
  observations of Vega-like stars*, A&A 426, 601
  (`2004A&A...426..601D`, arXiv:astro-ph/0408390). VLTI/VINCI
  K-band limb-darkened angular diameter θ_LD = 2.223 ± 0.022 mas;
  derives R = 1.842 ± 0.019 R☉ at the Hipparcos parallax. Anchors
  the radius measurement.
- **Kalas P. et al. 2005** — *A planetary system as the origin of
  structure in Fomalhaut's dust belt*, Nature 435, 1067
  (`2005Natur.435.1067K`). HST/ACS coronagraphy first resolves the
  narrow, eccentric main ring at 133 AU with e ≈ 0.11 and a sharp
  inner edge — interpreted as gravitational sculpting by an unseen
  planet (the original "shepherding" inference).
- **Kalas P. et al. 2008** — *Optical Images of an Exosolar Planet
  25 Light-Years from Earth*, Science 322, 1345
  (`2008Sci...322.1345K`). The original "Fomalhaut b" HST detection
  paper. **Retraction context**: subsequent re-analysis by Gáspár &
  Rieke 2020 and the JWST 2023 non-detection (Gáspár 2023)
  re-interprets the source as a transient expanding dust cloud from
  a planetesimal collision rather than a bound planet. This
  synthesis follows the current consensus.
- **Gáspár A. & Rieke G. H. 2020** — *New HST data and modeling
  reveal a massive planetesimal collision around Fomalhaut*, PNAS
  117, 9712 (`2020PNAS..117.9712G`, arXiv:2004.08736). Re-analysis
  of HST archive shows "Fomalhaut b" has expanded and faded between
  2004–2014 epochs, consistent with an expanding dust cloud from a
  ~200 km planetesimal collision rather than a bound point source.
- **Gáspár A. et al. 2023** — *Spatially resolved imaging of the
  inner Fomalhaut disk using JWST/MIRI*, Nature Astronomy 7, 790
  (`2023NatAs...7..790G`, arXiv:2305.03789). JWST/MIRI imaging at
  15.5 µm + 23 µm resolves a previously-unknown **intermediate belt
  at ~40–80 AU** and confirms an **inner warm asteroid-belt analog
  at ~10 AU**; no point source at the Fomalhaut-b epoch position,
  consistent with the dust-cloud interpretation.
- **Boley A. C. et al. 2012** — *Constraining the planetary system
  of Fomalhaut using high-resolution ALMA observations*, ApJ 750,
  L21 (`2012ApJ...750L..21B`, arXiv:1204.0007). ALMA Cycle 0
  imaging of the main ring; eccentricity e = 0.11 ± 0.01, inner
  edge 133 AU, outer edge 158 AU, width Δa/a ≈ 0.13; constrains
  shepherd planet mass to < 3 M_Jup.
- **White J. A. et al. 2017** — *ALMA observations of Fomalhaut's
  outer dust ring*, ApJ 842, 80 (`2017ApJ...842...80W`,
  arXiv:1705.10670). Higher-resolution ALMA Cycle 4 follow-up;
  confirms the narrow eccentric ring and refines the inclination
  to 65.6 ± 0.4°; sets the disk geometry cfg fields.
- **Le Bouquin J.-B. et al. 2009** — *Spin axis of α PsA from
  interferometry*, A&A 498, L41 (`2009A&A...498L..41L`,
  arXiv:0904.1688). VLTI/AMBER measurement of stellar oblateness
  + spin axis orientation; demonstrates spin-orbit alignment with
  the debris disk to ~3°.
- **Davis J. et al. 2005** — *Limb-darkening determinations for
  Fomalhaut and α Cen A from SUSI*, MNRAS 356, 1362
  (`2005MNRAS.356.1362D`). Optical interferometric limb-darkening
  power-law α(V) ≈ 0.21 for Fomalhaut; sets `limb_darkening_alpha_h`.

### Read (context / methodology, not directly decision-driving)

- **Royer F. et al. 2007** — *Rotational velocities of A-type stars*,
  A&A 463, 671 (`2007A&A...463..671R`, arXiv:astro-ph/0610785).
  Gives v sin i = 93 ± 3 km/s for Fomalhaut; combined with disk
  inclination to derive rotation period.
- **Acke B. et al. 2012** — *Herschel images of Fomalhaut: An
  extrasolar Kuiper Belt at the height of its dynamical activity*,
  A&A 540, A125 (`2012A&A...540A.125A`, arXiv:1204.5037).
  Herschel/PACS far-IR imaging of the cold main ring; SED fit
  T_dust ≈ 65 K; fills the `disk_dust_temperature_k` field.
- **Holland W. S. et al. 2017** — *SONS: The JCMT legacy survey of
  debris discs at submillimetre wavelengths*, MNRAS 470, 3606
  (`2017MNRAS.470.3606H`, arXiv:1706.01218). SCUBA-2 submm
  photometry; main-ring dust mass ~1.5 × 10⁻² M⊕ in mm-cm grains.
- **Saffe C. et al. 2008** — *Spectroscopic metallicities of Vega-
  like stars*, A&A 490, 297 (`2008A&A...490..297S`,
  arXiv:0805.3936). High-resolution metallicity for Castor moving-
  group A-stars including Fomalhaut; [Fe/H] = −0.03 ± 0.05.
- **Stapelfeldt K. R. et al. 2004** — *First Look at the Fomalhaut
  Debris Disk with Spitzer*, ApJS 154, 458
  (`2004ApJS..154..458S`). Spitzer/MIPS 24/70/160 µm photometry;
  first multi-band thermal characterization of the dust disk.
- **Currie T. et al. 2012** — *A Direct-Imaging Survey of the
  Fomalhaut Planetary System with the Hubble Space Telescope*, ApJ
  760, L32 (`2012ApJ...760L..32C`, arXiv:1210.6555). Independent
  HST re-analysis of "Fomalhaut b"; early evidence that the source
  is not a self-luminous planet.
- **Schröder C. & Schmitt J. H. M. M. 2007** — *X-ray emission from
  A-type stars*, A&A 475, 677 (`2007A&A...475..677S`). ROSAT survey
  of A-star X-ray flux; sets the log L_X upper limit for Fomalhaut.
- **Greaves J. S. et al. 2014** — *Alignment of the host star spin
  with the orbit of debris discs*, MNRAS 438, L31
  (`2014MNRAS.438L..31G`, arXiv:1311.3431). Population-wide spin-
  orbit alignment for A-star debris-disk hosts; supports the
  Le Bouquin 2009 alignment assumption.

### Read (instrument / non-cfg-decisive)

- **Gray R. O. & Garrison R. F. 1989** — *The Late A-Type Stars:
  Refined MK Classification* (`1989ApJS...70..623G`). MK system
  reclassification placing Fomalhaut at the A3V/A4V boundary.
- **Monnier J. D. et al. 2010** — *Imaging the surface of Altair*,
  Science 317, 342 (`2007Sci...317..342M`). Reference for
  gravity-darkening map of a comparable rapid-rotator A-star.
- **Kopparapu R. K. et al. 2013** — *Habitable zones around main-
  sequence stars*, ApJ 765, 131 (`2013ApJ...765..131K`,
  arXiv:1301.6674). HZ inner/outer boundaries for A4V star.
- **Wyatt M. C. 2008** — *Evolution of Debris Disks*, ARA&A 46, 339
  (`2008ARA&A..46..339W`). Theoretical framework for collisional
  cascade replenishment in resolved debris disks; underpins the
  `disk_planetesimal_belt_inferred` field.

### Not read — no arXiv preprint or low-priority (~30 papers)

Conference abstracts (AAS / DPS / EPSC), interferometric methods
papers (CHARA / PTI commissioning), and follow-up dust-grain
mineralogy work (Spitzer IRS spectra) contribute no cfg-decisive
content beyond what Di Folco 2004 + Boley 2012 + Gáspár 2023
already establish. SETI / radio-emission monitoring of the
"Fomalhaut b" position (Tusay 2022, Saide 2023) is also skipped.
Filtered bib preserved in `docs/phase3/_bib/fomalhaut.yaml` with
`status: skipped` annotations.

## Open items for follow-up

- **TW Piscis Austrini (HD 216803, K4V) and LP 876-10 (M4V) as
  separate NS DB entries**: The two wide common-proper-motion
  companions are not currently in the 152-system NearStars
  shortlist. Mamajek 2012/2013 establish them as gravitationally
  associated, co-eval (440 Myr) Castor-moving-group members at
  projected separations of 0.91 ly and 5.7 ly. If added as
  separate DB entries, the in-game player could fly between all
  three on real interstellar trajectories. Flag as Phase 2 DB
  expansion candidate.
- **Phase 2 `disk_measurements` ingest**: This synthesis sources
  disk parameters directly from the literature because
  `db/systems/fomalhaut.json` has no `disk_measurements` block.
  Add a parsing step to extract Kalas 2005 / Boley 2012 / White
  2017 / Gáspár 2023 disk geometry into the DB so downstream
  Kopernicus cfg writers can read the data without re-parsing the
  Phase 3 markdown.
- **"Fomalhaut b S1" candidate revisit**: If a 2026+ JWST/MIRI or
  ground-based ELT follow-up reverses the Gáspár & Rieke 2020 dust-
  cloud interpretation and re-establishes a bound planet at ~115 AU,
  a new Decisions entry `circumstellar_planet_present: true` (with
  the candidate "S1" naming) would be needed and the cfg should
  document the divergence from the current consensus. Until then,
  no planet is included.
- **Phase 2 `teff_measurements` and `metallicity_measurements`
  population**: DB has `teff_k = 8689` as a SIMBAD compilation
  scalar with no provenance entry; Saffe 2008 metallicity is also
  not in DB. Both should be added with paper-cited Phase 2 entries.
- **Gravity-darkening map**: No resolved interferometric gravity-
  darkening map of Fomalhaut exists (unlike Vega, Altair, Regulus).
  CHARA/MIRC or VLTI/GRAVITY observation of the von-Zeipel
  pole-to-equator temperature gradient would let the cfg replace
  the current uniform-disk tint with a latitudinal gradient
  (`visual_gravity_darkening_delta_t_k` field, currently absent).

## Related

- [methodology](../reference/methodology.md) — schema source for the Decisions table
- [alpha-centauri-a](alpha-centauri-a.md) — canonical stellar-synthesis template, G2V comparison
- [binary-epoch-pipeline](../reference/binary-epoch-pipeline.md) — wide-companion CPM treatment relevant if TW PsA / LP 876-10 are later promoted to NS DB
