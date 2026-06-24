<!-- Teegarden's Star Phase 3 synthesis: cfg-ready decisions and reasoning -->
# Teegarden's Star — Phase 3 Synthesis

Teegarden's Star (GJ — none; Karmn J02530+168; LSPM J0253+1652) is an
M7.0 V ultracool dwarf at 3.831 pc (Gaia parallax 261.01 mas), the
24th-nearest star to the Sun and the brightest known representative of
spectral type M7 V and later (Zechmeister et al. 2019). Despite that
proximity it is invisible to the naked eye — at V = 15.08 (J = 8.39)
the optical flux is almost entirely strangled by molecular bands, and
the star radiates overwhelmingly in the near-infrared. It is one of
the coolest hosts in the NearStars catalog: at Teff = 2904 K its
photosphere is some 290 K cooler than Barnard's Star (3195 K) and
renders as a deeper, more saturated red.

The fundamental parameters come from the frozen Phase 2 layer, all
from Schweitzer et al. 2019 (CARMENES). The effective temperature
Teff = 2904 ± 51 K is from PHOENIX synthetic-spectrum fitting; the
luminosity L = 0.00073 ± 0.00001 L☉ — about 1/1370 of the Sun, the
faintest host in the set — is from the bolometric flux (Gaia DR2
parallax plus integrated photometry); the radius R = 0.107 ± 0.004 R☉
follows from L and Teff through the **Stefan-Boltzmann law**, not from
interferometry. This is a structural point worth stating plainly: at
3.831 pc with R = 0.107 R☉ the limb-darkened angular diameter is only
~0.032 mas, more than an order of magnitude below the resolution floor
of any existing optical interferometer — so unlike Barnard's Star
(whose 0.95 mas diameter CHARA could resolve directly), Teegarden's
Star has **no interferometric radius and never will from the ground**;
SED fitting is the only route. The mass M = 0.089 ± 0.009 M☉ comes
from Schweitzer's own linear mass-radius relation applied to that SED
radius. The metallicity [Fe/H] = −0.19 ± 0.16 (Schweitzer 2019) is
the recommended value but carries a documented divergence (see
Canonical alternatives), and the radius/mass themselves carry a second
divergence against the Dreizler 2024 re-derivation.

What characterizes Teegarden's Star for NearStars is extreme age and
extreme quiescence at the very bottom of the main sequence. The age
is 7 ± 3 Gyr (Zechmeister et al. 2019), a PARSEC Bayesian estimate
consistent with the thick-disc kinematics (W = −58.7 km/s) and with
the Hα-activity-floor age of 8.0(+0.5/−1.0) Gyr — the star sits in an
evolved Galactic population. The rotation is correspondingly very
slow: P_rot = 96.2 d (Lafarga et al. 2021, spectroscopic activity
indices, adopted by Dreizler 2024), making Teegarden's Star a near
outlier even among slow-rotating very-low-mass dwarfs. The coronal
activity is low: log(Lx/Lbol) = −4.9 (Fuhrmeister et al. 2025,
quiescent Chandra detection), and the chromosphere is quiet for an
M7 V — the average Hα is filled in rather than in emission. "Quiet"
does not mean inert: the same Fuhrmeister 2025 campaign caught two
large TESS flares (total energy ~10³¹–10³² erg, comparable to the
largest solar flares) and hints of an erupting prominence.

Teegarden's Star hosts a **compact system of temperate Earth-mass
planets**: b and c (each ~1.1 M⊕ minimum mass, P = 4.91 d and 11.4 d;
Zechmeister et al. 2019) — the first Earth-mass planets found around
an ultracool dwarf by radial velocity — plus a third planet d
(0.82 M⊕, P = 26.13 d; Dreizler et al. 2024). Each is characterized
in its own per-planet Phase 3 synthesis (`teegardens-star-b/c/d`).

**Scenario choice for NearStars: an ancient, deeply red, very quiet
M7 V ultracool dwarf — the brightest of its spectral class, the
faintest host in the catalog — rotating very slowly on a 96-day
period, with low quiescent activity punctuated by rare large flares.**
The stellar layer is anchored on the frozen Phase 2 sources
(Schweitzer 2019 Teff/luminosity/radius/mass/metallicity, Zechmeister
2019 age and spectral type, Lafarga 2021 via Dreizler 2024 rotation,
Fuhrmeister 2025 activity). Two parameters carry documented
divergences across the literature — the radius/mass pair (Schweitzer
SED vs Dreizler evolutionary, ~3σ in radius) and the metallicity
(Schweitzer vs Rojas-Ayala, ~0.36 dex) — handled in `## Canonical
alternatives`. One tie-break sets the visual surface tint for the
2904 K M7 V SED.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | M7.0 V | high | Alonso-Floriano et al. 2015 (via Zechmeister 2019 Table 1); ultracool dwarf, the brightest known representative of M7 V and later |
| `mass_msun` | 0.089 ± 0.009 | high | Schweitzer et al. 2019 — CARMENES, linear mass-radius relation applied to the SED radius (Phase 2 recommended). DOCUMENTED DIVERGENCE: Dreizler 2024 evolutionary re-derivation gives 0.097 ± 0.010 — see Canonical alternatives |
| `radius_rsun` | 0.107 ± 0.004 | high | Schweitzer et al. 2019 — Stefan-Boltzmann from L and Teff (SED fitting); **no interferometric radius possible** (θ_LD ~0.032 mas, far below the interferometer floor). DOCUMENTED DIVERGENCE: Dreizler 2024 gives 0.120 ± 0.012 (~3σ) — see Canonical alternatives |
| `teff_k` | 2904 ± 51 | high | Schweitzer et al. 2019 — PHOENIX synthetic-spectrum fit to CARMENES spectra (Phase 2 recommended); ~290 K cooler than Barnard's Star, one of the coolest hosts in the set |
| `luminosity_lsun` | 0.00073 ± 0.00001 | high | Schweitzer et al. 2019 — bolometric flux from Gaia DR2 parallax + integrated photometry (Phase 2 recommended); ~1/1370 of the Sun, the faintest host in the catalog |
| `metallicity_fe_h_dex` | −0.19 ± 0.16 | medium | Schweitzer et al. 2019 — high-resolution spectroscopy (Phase 2 recommended). DOCUMENTED DIVERGENCE: Rojas-Ayala 2012 K-band gives −0.55 ± 0.17 (~0.36 dex) — see Canonical alternatives |
| `age_gyr` | 7 ± 3 | medium | Zechmeister et al. 2019 — PARSEC Bayesian (kinematic / thick-disc; W = −58.7 km/s); consistent with the Hα-activity-floor age 8.0(+0.5/−1.0) Gyr and the broader 8–10 Gyr range |
| `rotation_period_days` | 96.2 | medium | Lafarga et al. 2021 (spectroscopic activity indices), adopted by Dreizler 2024 (Phase 2 recommended); no formal uncertainty quoted. Independent estimates cluster at 96–100 d (Terrien 2022, Kemmer 2023) |
| `activity_log_lx_lbol` | −4.9 | high | Fuhrmeister et al. 2025 — quiescent Chandra X-ray detection (Phase 2 recommended); XMM-Newton quiescent range −5.0 to −4.81, consistent. Supersedes the Zechmeister 2019 upper limit <−4.23 |
| `flare_state` | rare large flares | medium | Fuhrmeister et al. 2025 — two TESS flares, total energy ~10³¹–10³² erg (comparable to the largest solar flares), plus hints of an erupting prominence; flare rate ~2.6 ± 1.8 per 100 d, but concentrated — quiescent most of the time |
| `v_sin_i_km_s` | ~0.06 | low | Derived from R = 0.107 R☉ and P_rot = 96.2 d (equatorial velocity ~0.056 km/s); far below any spectroscopic line-broadening threshold — effectively a non-rotator for line-broadening purposes |
| `visual_surface_tint_hex_primary` | `#ffcc75` (pale warm orange, M7 V) | medium | Real photospheric color: a Pickles 1998 observed late-M SED near 2900 K integrated through the shared CIE→sRGB engine (`scripts/refs/stellar_photospheric_color.py`), peak-channel normalized. A pale warm orange; the ~2900 K blackbody is a fair first approximation, and even with heavy TiO/VO/H₂O bands the displayed chromaticity shifts only modestly (the large molecular effect is on the color index and luminosity, not the visible hue). Only very slightly warmer than the M4 V Barnard `#ffd487` (Teff ~290 K hotter) and indistinguishable from the M5.5 Proxima `#ffcc75` — all within the pale-warm-orange family. (Supersedes the earlier render-saturated brick-red estimate `#c23a1c`.) |
| `stellar_color_temp_k` | 2904 | high | derived from Teff (Schweitzer 2019) |
| `apparent_magnitude_v_from_earth` | 15.08 | high | Zechmeister 2019 / Carmencita; far below naked-eye visibility despite the 3.831 pc proximity, because of the tiny 0.00073 L☉ luminosity (the star is much brighter in J, 8.39 mag) |
| `distance_pc` | 3.831 ± 0.004 | high | Gaia DR2 (via Zechmeister 2019); the 24th-nearest star to the Sun |

## Surface synthesis

Teegarden's Star has the deepest, most saturated red photosphere in
the catalog. At Teff = 2904 K (Schweitzer 2019) the SED peaks far into
the near-infrared near ~1.0 μm, and the optical continuum is almost
entirely suppressed — at this temperature TiO, VO, and water bands
dominate the spectrum so thoroughly that, as Fuhrmeister 2025 notes,
"late M dwarfs do not show an identifiable continuum." This is why the
star is the brightest M7 V representative yet shines at only V = 15.08
from Earth while reaching J = 8.39 in the near-infrared. With
R = 0.107 R☉ the luminosity is only 0.00073 L☉ — about 1/1370 of the
Sun — making Teegarden's Star the faintest host in the set.

The radius itself is a key surface fact. Unlike Barnard's Star, whose
0.187 R☉ rests on a directly resolved CHARA interferometric diameter,
Teegarden's Star cannot be resolved by any existing interferometer:
its limb-darkened angular diameter is only ~0.032 mas, more than ten
times below the resolution floor. The cfg radius is therefore an SED
quantity — Schweitzer 2019 obtained L from Gaia photometry and Teff
from spectral fitting, then closed Stefan-Boltzmann for R. This is the
only route available at the bottom of the main sequence, and it is the
reason the radius carries a documented ~3σ divergence against the
Dreizler 2024 evolutionary value (0.120 R☉). The sub-solar metallicity
[Fe/H] = −0.19 (Schweitzer 2019) marginally reduces molecular-band
blanketing relative to a solar-metallicity M7 V, but this is invisible
at the resolution of the in-game illumination color.

The defining surface property is quiescence at the bottom of the
main sequence. Teegarden's Star is "relatively magnetically quiet for
its spectral type" (Zechmeister 2019): of 24 M7–M7.5 V dwarfs in
Reiners & Basri 2010, only one is as Hα-faint. The average
log(LHα/Lbol) = −5.25 places it below the West 2008 activity
threshold — formally inactive for an M7 V, the signature of old age.
For cfg rendering this means a near-uniform deep-red disk with low
spot coverage, in deliberate contrast to the saturated young flare
stars elsewhere in the catalog. Granulation is M-dwarf-typical with
small convection cells set by the shallow photospheric pressure scale
height.

## Atmosphere synthesis

Teegarden's Star's outer atmosphere is dominated by quiescence with
rare violent punctuation. The coronal activity log(Lx/Lbol) = −4.9
(Fuhrmeister 2025, quiescent Chandra detection; XMM-Newton quiescent
range −5.0 to −4.81) is low, and the chromosphere is quiet: the
average Hα is filled in rather than in emission, and the He I infrared
triplet is absent in all spectra — both markers of a low quiescent
activity floor for the spectral type. The 96-day rotation period and
the resulting very large Rossby number put the star deep in the
unsaturated, magnetically-braked regime, exactly where the
rotation–activity relation predicts floor-level emission.

A crucial caveat is that the standard chromospheric index Ca II H&K
log R'HK is **not measurable** for Teegarden's Star from the ground.
At M7 V there is no identifiable photospheric continuum against which
to define the index, so activity must be characterized through
pseudo-equivalent widths of emission lines (Hα, higher Balmer lines)
and through X-rays instead — which is precisely the route Fuhrmeister
2025 took. This is flagged as an open item: the cfg uses
log(Lx/Lbol) = −4.9 as the activity anchor in place of the
log R'HK used for warmer hosts.

Quiescent does not mean inert. The Fuhrmeister 2025 TESS monitoring
caught two large flares with total optical energy ~10³¹–10³² erg —
comparable to the largest solar flares ever recorded — plus X-ray
flares (one showing the Neupert effect, implying hard-X-ray
production) and hints of an erupting prominence that may have driven a
coronal mass ejection. The implied flare rate is ~2.6 ± 1.8 per 100 d,
but the two flares clustered in a single TESS sector, hinting that the
star alternates between calm stretches and more active episodes. For
cfg purposes flares are rare-event punctuation — not the
near-continuous flaring of an active young M dwarf — riding on an
otherwise low quiescent XUV background. For the close-in Earth-mass
planets (b at P = 4.91 d) the time-averaged irradiation is gentle, but
the rare large flares and orbital proximity still impose a
non-negligible cumulative XUV dose over the star's multi-Gyr lifetime.

## Rotation & spin synthesis

The 96.2-day rotation period (Lafarga et al. 2021, from spectroscopic
activity indices; adopted by Dreizler 2024) is among the longest in
the M-dwarf catalog and is the direct fingerprint of age. Over its
~7 Gyr lifetime Teegarden's Star has shed nearly all of its initial
angular momentum through magnetic (Skumanich-type) braking, spinning
down to the present near-stationary state. Independent determinations
cluster tightly — 96 d (Lafarga 2021), ~100 d (Terrien 2022), 98 d
(Kemmer 2023) — so the period is robust even though no formal
uncertainty is quoted; the cfg records it at medium confidence. The
implied equatorial velocity is only ~0.056 km/s, so v sin i is far
below the detection threshold of any spectroscopic line-broadening
analysis — recorded as ~0.06 km/s with low confidence as a derived
quantity, not a measurement.

There is a genuine ambiguity worth noting: Dreizler 2024 found a
coherent ~172 d signal in the radial velocities and activity
indicators and considered whether *it* might be the true rotation
period (which would make Teegarden's Star an extreme slow-rotation
outlier), but concluded the conservative interpretation is that 172 d
is an activity-related signal and 96 d is the rotation period. The cfg
follows that conclusion. Dreizler 2024 additionally reports very
long-period variability spanning ~2500 d or longer in both RV and
activity indicators, which they suggest may indicate a long activity
cycle — analogous to Barnard's Star's decadal cycle, though here it is
not resolved into a definite period.

No asteroseismic constraint is available — Teegarden's Star is far too
cool and too small for detectable p-mode oscillations. The
rotation-axis inclination is unconstrained; for visual rendering
NearStars adopts a generic axis orientation, since the near-zero
rotational velocity makes spin-related foreshortening visually
negligible. One striking kinematic accident: the star's ecliptic
latitude is only 0.30°, so from Teegarden's Star the Solar System
planets transit the Sun — Earth will enter Teegarden's transit band in
2044 (Zechmeister 2019). This is a viewpoint curiosity rather than a
cfg-decisive fact, but it underscores how nearly edge-on the system
sits to the Solar ecliptic.

## Canonical alternatives

Two parameters carry documented divergences across the Phase 2
literature. In both cases the cfg adopts the Phase 2 recommended
value, but the spread between analyses is large enough to warrant
explicit documentation.

| Field | cfg value (recommended) | Canonical alternatives | Why cfg picks this value |
|---|---|---|---|
| `radius_rsun` / `mass_msun` | R = 0.107 ± 0.004 R☉, M = 0.089 ± 0.009 M☉ (Schweitzer 2019, SED + Stefan-Boltzmann + linear M-R) | R = 0.120 ± 0.012 R☉, M = 0.097 ± 0.010 M☉ (Dreizler 2024, "This work" — updated SteParSyn Teff feeding an evolutionary M-L re-derivation) | The two radii differ by ~3σ (0.107 vs 0.120 R☉) — a genuine methodological disagreement, not scatter. **No interferometric radius is possible** at θ_LD ~0.032 mas (far below the interferometer floor), so neither value can be checked against a directly resolved diameter; SED fitting is the only route. The cfg keeps the Schweitzer 2019 SED radius because it is the Phase 2 recommended value and the homogeneous CARMENES SED/Stefan-Boltzmann method used across the whole catalog (Barnard, GJ targets), preserving cross-host consistency. The Dreizler 2024 value, derived from an updated Marfil-2021-style SteParSyn Teff (3034 K) and an evolutionary mass-luminosity relation, is the more recent re-derivation and is retained as the alternative. The choice affects the rendered angular size of the disk from the planets but is sub-perceptible for the surface tint. |
| `metallicity_fe_h_dex` | −0.19 ± 0.16 (Schweitzer 2019, CARMENES high-res spectroscopy) | −0.55 ± 0.17 (Rojas-Ayala 2012, K-band) | The two determinations differ by ~0.36 dex — Zechmeister 2019 itself flags this as "disagreement of stellar parameter determination at the very cool end." Metallicity at M7 V is notoriously hard: the optical continuum is fully blanketed by molecular bands, and even K-band calibrations (Rojas-Ayala 2012) and high-resolution PHOENIX fits (Schweitzer 2019) disagree substantially. The cfg adopts the Schweitzer 2019 value as the Phase 2 recommended one and the one consistent with the recommended Teff/L/R/M (all Schweitzer, a self-consistent parameter set). The metallicity only weakly affects the rendered SED color, so this divergence is documentary rather than visually decisive. (Note: Zechmeister 2019's own age estimate used the Rojas-Ayala −0.55 as PARSEC input, so the recommended age is mildly entangled with the alternative metallicity.) |

Both Dreizler 2024 (mass/radius) and Rojas-Ayala 2012 (metallicity)
remain in the Phase 2 DB as `recommended:false` alternatives within
their respective measurement arrays, preserving the audit trail; the
recommended picks are Schweitzer 2019 throughout.

## Visual styling

In the NearStars renderer, Teegarden's Star is portrayed as the
faintest M7 V ultracool dwarf in the catalog — the brightest of its
spectral class, yet visually negligible in brightness. The surface
tint is encoded as `#ffcc75`, the real photospheric color: a Pickles
1998 observed late-M SED near 2900 K integrated through the shared
CIE→sRGB engine and peak-channel normalized. The ~2900 K blackbody is
a fair first approximation; even with near-total TiO/VO/H₂O bands the
displayed chromaticity is a pale warm orange, the molecular effect
falling on the color index and luminosity rather than the visible
hue. The M-sequence chromaticity is nearly flat, so this is only very
slightly warmer than the M4 V Barnard's Star (`#ffd487`, Teff ~290 K
hotter) and indistinguishable from the M5.5 Proxima (`#ffcc75`). The
illumination color temperature for scene lighting of any nearby body
is driven directly by the 2900 K SED, bathing the close-in Earth-mass
planets in warm, infrared-dominated light.

The disk is rendered near-uniform with only faint, slowly-drifting
spot features — the visual expression of the floor-level chromospheric
activity (Hα below the West 2008 inactive threshold) and the very slow
96-day rotation. There is a flaring layer, but it is rare-event
punctuation: the two Fuhrmeister 2025 TESS flares (each ~10³¹–10³² erg,
comparable to the largest solar flares) are rendered as occasional
brilliant transient brightenings against an otherwise calm disk,
clustered rather than near-continuous. The possible ~2500 d activity
cycle, if real, modulates the already-subtle spot pattern slowly over
the in-game equivalent of years.

From Earth, Teegarden's Star is a V = 15.08 object — far below
naked-eye visibility despite its 3.831 pc proximity, because of the
tiny 0.00073 L☉ luminosity (it is far brighter in the near-infrared at
J = 8.39). Its real-sky signature is not brightness but its near-zero
ecliptic latitude (0.30°): it sits almost exactly on the plane of the
Solar System, so from its vantage the Sun's planets transit. From the
viewpoint of its close-in Earth-mass planets, the red disk would
subtend a modest angular diameter and flood the landscape with deep-red
infrared-dominated light, calm for years at a time and then
occasionally lit by a brilliant flare.

## Bibliography

### Read (drove Decisions above)

- **Schweitzer A. et al. 2019** — *The CARMENES search for exoplanets
  around M dwarfs. Different roads to radii and masses of the target
  stars*, A&A 625, A68 (`2019A&A...625A..68S`,
  doi:10.1051/0004-6361/201834965, arXiv:1904.03231). CARMENES
  fundamental-parameter compilation. Source for the Phase 2
  recommended Teff (2904 ± 51 K, PHOENIX fit), luminosity
  (0.00073 ± 0.00001 L☉, bolometric flux), radius (0.107 ± 0.004 R☉,
  Stefan-Boltzmann from L and Teff — SED fitting, no interferometry
  possible), mass (0.089 ± 0.009 M☉, linear M-R relation), and
  metallicity (−0.19 ± 0.16). Teegarden's Star is explicitly
  highlighted in this paper as the latest-type (M7 V) object in the
  CARMENES sample.
- **Zechmeister M. et al. 2019** — *The CARMENES search for exoplanets
  around M dwarfs. Two temperate Earth-mass planet candidates around
  Teegarden's Star*, A&A 627, A49 (`2019A&A...627A..49Z`,
  doi:10.1051/0004-6361/201935460, arXiv:1906.07196). Discovery paper
  for planets b and c (each ~1.1 M⊕, P = 4.91 d and 11.4 d). Source
  for the Phase 2 recommended age (7 ± 3 Gyr, PARSEC Bayesian /
  thick-disc kinematic) and spectral type (M7.0 V, via Alonso-Floriano
  2015). Also the stellar context: distance 3.831 pc, V = 15.08,
  J = 8.39, Hα activity floor, 0.30° ecliptic latitude. Planets are
  out of scope here — flagged for the planet follow-up.
- **Dreizler S. et al. 2024** — *The CARMENES search for exoplanets
  around M dwarfs. The enigmatic planetary system of Teegarden's
  Star*, A&A 684, A117 (`2024A&A...684A.117D`,
  doi:10.1051/0004-6361/202348033, arXiv:2402.00923). Source for the
  Phase 2 recommended rotation period (P_rot = 96.2 d, from Lafarga
  2021 spectroscopic activity indices) and for the alternative
  mass/radius (0.097 ± 0.010 M☉, 0.120 ± 0.012 R☉, evolutionary
  re-derivation — the documented radius/mass divergence). Discovery
  paper for planet d (0.82 M⊕, P = 26.13 d); also the 172 d / 96 d
  rotation-vs-activity discussion and the ~2500 d possible activity
  cycle.
- **Fuhrmeister B. et al. 2025** — *Coronal and chromospheric activity
  of Teegarden's star* (arXiv:2504.02338). Source for the Phase 2
  recommended coronal activity log(Lx/Lbol) = −4.9 (quiescent Chandra
  detection; XMM-Newton quiescent range −5.0 to −4.81), superseding
  the Zechmeister 2019 X-ray upper limit. Also the two large TESS
  flares (~10³¹–10³² erg), the Neupert-effect X-ray flare, the
  erupting-prominence/CME hints, and the chromospheric picture (Hα
  filled-in in quiescence, He I IR triplet absent). The basis for the
  quiescent-with-rare-flares scenario and the log R'HK-unmeasurable
  open item.

### Read (context / methodology, not decision-driving)

- **Marfil E. et al. 2021** — *The CARMENES search for exoplanets
  around M dwarfs. Stellar atmospheric parameters of target stars with
  SteParSyn*, A&A 656, A162 (`2021A&A...656A.162M`,
  doi:10.1051/0004-6361/202141980, arXiv:2110.07329). SteParSyn
  Teff = 3034 ± 45 K and [Fe/H] = −0.11 ± 0.28; the line list and
  model grid Dreizler 2024 re-ran to get the alternative parameter
  set. Methodology context for the radius/mass divergence.
- **Cifuentes C. et al. 2020** — *CARMENES input catalogue of M dwarfs.
  Photometric and astrometric properties* (CARMENES cool-star
  catalogue). Photometric data and luminosity cross-check; context
  only.

### Read (instrument-only / methodological references)

- **Rojas-Ayala B. et al. 2012** — *Metallicity and Temperature
  Indicators in M Dwarf K-band Spectra*, ApJ 748, 93. K-band
  metallicity [Fe/H] = −0.55 ± 0.17 (the documented metallicity
  alternative) and Teff = 2637 K. Source for the
  Canonical-alternatives metallicity row.
- **Lafarga M. et al. 2021** — CARMENES activity-indicator
  time-series analysis giving the P_rot = 96.2 d rotation period
  (cited via Dreizler 2024 Table 2). The rotation Decisions row traces
  to this work.

### Not read — superseded or low-priority

The superseded Zechmeister 2019 X-ray upper limit (log(Lx/Lbol)
< −4.23, replaced by the Fuhrmeister 2025 detection), independent
rotation-period confirmations beyond the recommended Lafarga value
(Terrien 2022 ~100 d, Kemmer 2023 98 d — cited for robustness, not
decision-driving), generic ultracool-dwarf activity surveys without a
dedicated Teegarden's Star entry, and the planet-discovery /
dynamical-architecture sections of Zechmeister 2019 and Dreizler 2024
contribute no cfg-decisive content for the stellar synthesis. The
planet papers are deferred to the planet Phase 3 follow-up workspace.
The full filtered bibliography is preserved in
`docs/phase3/_bib/teegardens-star.yaml`.

## Open items for follow-up

- **Earth-mass planet Phase 3 follow-up workspace.** The system hosts
  three temperate Earth-mass planets — b and c (~1.1 M⊕, P = 4.91 d
  and 11.4 d; Zechmeister 2019) and d (0.82 M⊕, P = 26.13 d; Dreizler
  2024). These are out of scope for the stellar synthesis; a dedicated
  follow-up should produce planet Phase 3 syntheses once the
  candidates' Phase 2 measurements are curated.
- **log R'HK is unmeasurable from the ground at M7 V.** There is no
  identifiable photospheric continuum to define the Ca II H&K index,
  so the cfg uses log(Lx/Lbol) = −4.9 (Fuhrmeister 2025) as the
  activity anchor in place of the chromospheric index used for warmer
  hosts. A future space-UV chromospheric calibration could supply a
  comparable index, but no ground-based log R'HK will ever exist.
- **Radius/mass divergence resolution.** The Schweitzer 2019 SED
  radius (0.107 R☉) and the Dreizler 2024 evolutionary radius
  (0.120 R☉) differ by ~3σ, and interferometry can never adjudicate
  (θ_LD ~0.032 mas). A future SED-fitting reanalysis with a
  homogeneous Teff scale, or a JWST/ground-NIR spectrophotometric
  reanalysis, could tighten the cool-end radius scale and confirm
  which mass-radius relation is appropriate at the bottom of the main
  sequence.
- **Activity-cycle confirmation.** Dreizler 2024 reports a possible
  ~2500 d (~7 yr) long-period variability in RV and activity
  indicators that may be an activity cycle, but it is not resolved
  into a definite period. Continued monitoring would confirm whether
  Teegarden's Star has a Barnard-like decadal cycle and sharpen any
  cfg `activity_cycle_years` rendering.
- **Flare-rate characterization.** Fuhrmeister 2025 estimates ~2.6 ±
  1.8 flares per 100 d from two TESS events, but the clustering hints
  at active/calm episodes. A longer flare census would let a future
  cfg attach a quantitative `flare_rate_per_day` and
  `flare_energy_log_erg_max` to the otherwise quiescent rendering.
- **Rotation-axis inclination.** Unconstrained; the near-zero
  rotational velocity makes spin-related visual effects negligible, so
  this is low-priority.

## Related

- [methodology](../reference/methodology.md) — schema source for the Decisions table
- [barnards-star](barnards-star.md) — comparison M dwarf (M4.0 Ve, ~8.5 Gyr); the next-warmest old quiet dwarf — contrast Barnard's interferometric radius and log R'HK with Teegarden's SED radius and X-ray activity anchor
- [proxima-cen](proxima-cen.md) — comparison ultracool-ish M dwarf (M5.5 Ve, ~4.85 Gyr); intermediate in temperature between Barnard and Teegarden
