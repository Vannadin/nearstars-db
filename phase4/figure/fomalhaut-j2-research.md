# Fomalhaut A — rotational-oblateness J₂ grounding (literature research)

**Scope.** Read-only literature research to ground the rotational J₂ of Fomalhaut A
(α PsA, HD 216956, A4V; M = 1.92 M☉, R = 1.842 R☉, T_eff = 8590 K, age 440 Myr —
all Mamajek 2012 [`2012ApJ...754L..20M`](https://ui.adsabs.harvard.edu/abs/2012ApJ...754L..20M), DB `recommended`). Early-type (A) stars have
no solar-anchored response coefficient in `body-figure-methodology.md`; this doc
grounds the **apsidal-motion-constant (k₂) path**, J₂ = (2/3)·k₂·q.
No board / DB / methodology files are modified here.

All bibcodes re-verified live against NASA ADS with the registered token. No WebSearch used.

---

## 1. Canonical source for J₂ = (2/3)·k₂·q

The relation ties the **rotationally induced second zonal harmonic** to the
dimensionless centrifugal parameter q = ω²R³/(GM) through the star's degree-2
response coefficient. Two equivalent conventions, differing only by which "k₂" is used:

- **apsidal-motion constant** k₂ (a.k.a. internal-structure constant, the quantity
  Claret tabulates):  **J₂ = (2/3)·k₂·q**
- **fluid/secular Love number** k₂ᶠ = 2·k₂ :  J₂ = (1/3)·k₂ᶠ·q

Both are the same first-order hydrostatic result.

**Canonical grounding:**

| role | bibcode | note |
|---|---|---|
| Foundational (defines internal-structure / apsidal-motion constants kⱼ from the Radau equation, and the second-harmonic distortion of a star by rotation **and** tides) | [`1939MNRAS..99..451S`](https://ui.adsabs.harvard.edu/abs/1939MNRAS..99..451S) | Sterne 1939, "Apsidal motion in binary stars" — the classical origin of the kⱼ formalism. (No ADS abstract; it is the standard citation.) |
| Modern theory + the k₂ grids we interpolate | [`1993A&A...277..487C`](https://ui.adsabs.harvard.edu/abs/1993A%26A...277..487C) (Claret & Giménez 1993) and [`2019A&A...628A..29C`](https://ui.adsabs.harvard.edu/abs/2019A%26A...628A..29C) (Claret 2019, latest grids) | define k₂ and connect it to the observable distortion |
| Accessible modern statement of the identical formula in Love-number form J₂ = (k₂ᶠ/3)(Ω²R³/GM) | [`2009ApJ...698.1778R`](https://ui.adsabs.harvard.edu/abs/2009ApJ...698.1778R) (Ragozzine & Wolf 2009) | exoplanet-interior context, but the same rotational-bulge relation |

**Self-consistency (factor) check against the repo's solar anchor.** The methodology's
FGK anchor is J₂/q = 0.0105 (from the *measured* helioseismic J₂☉ and q☉). Inverting
J₂ = (2/3)k₂q gives the **empirical solar k₂ = (3/2)(0.0105) = 0.0158** — exactly the
"Claret-family solar k₂ ≈ 0.0157" quoted in the task. The (2/3) factor is therefore the
correct one for Claret's k₂. Independent cross-check on Jupiter: k₂ᶠ ≈ 0.54, q = 0.083 →
J₂ = (1/3)(0.54)(0.083) = 0.0149 vs measured 0.0147. The relation holds.

> **Model-vs-empirical caveat (flagged, see §2/§4).** The *theoretical* solar k₂ read
> from the very same Claret 2004 grid at 1 M☉ / 4.5 Gyr is k₂ ≈ 0.020 (log k₂ ≈ −1.70),
> i.e. **~1.27× larger** than the empirical 0.0158. Claret's absolute k₂ scale runs ~20–25 %
> high relative to the Sun's measured figure. This is the dominant *systematic* on the
> coefficient and is carried into the J₂ uncertainty band below.

---

## 2. A-type k₂ from Claret grids (≈1.9 M☉, 0.44 Gyr)

**Table adopted:** Claret 2004, "New grids of stellar models including tidal-evolution
constants", [`2004A&A...424..919C`](https://ui.adsabs.harvard.edu/abs/2004A%26A...424..919C) (VizieR `J/A+A/424/919`, column `logK2`, Z = 0.02,
X = 0.70, no overshoot). Latest revision [`2019A&A...628A..29C`](https://ui.adsabs.harvard.edu/abs/2019A%26A...628A..29C) gives consistent values;
2004 was used because its VizieR track is directly machine-readable.

The mass grid brackets Fomalhaut with **logM = 0.2500 (1.78 M☉)** and **0.3000 (2.00 M☉)**.
The **2.0 M☉ track at 440 Myr independently reproduces Fomalhaut** — log T_eff = 3.930
(8515 K vs measured 8590 K), log L = 1.247 (17.6 vs ~16.6 L☉) — so it is the anchor track.

| track | Age | log T_eff (K) | log K₂ | k₂ |
|---|---|---|---|---|
| 2.00 M☉ | 425.9 Myr | 3.9312 (8535) | −2.4382 | 0.00365 |
| 2.00 M☉ | **440.8 Myr** | **3.9302 (8515)** | **−2.4424** | **0.00361** |
| 2.00 M☉ | 455.8 Myr | 3.9292 (8494) | −2.4465 | 0.00358 |
| 1.78 M☉ | 441.3 Myr | 3.9008 (7963) | −2.4363 | 0.00366 |

Interpolating to M = 1.92 M☉ at 440 Myr: **log k₂ = −2.44, k₂ = 0.0036.** The two mass
tracks agree to <0.01 dex here, so mass is not the driver.

**Uncertainty budget on k₂:**
- age 440 ± 40 Myr → ±0.004 dex (negligible; k₂ is nearly flat across the MS band)
- mass 1.92 ± 0.02 M☉ → negligible
- **model systematic (solar offset, §1) → ±0.10 dex, ~±25 %** — dominant.

Adopt **k₂ = 0.0036 (log k₂ = −2.44 ± 0.03 statistical; ~±25 % systematic).**
An A star is far more centrally condensed than the Sun, so its k₂ (0.0036) is ~4.4×
below the Sun's (0.0158) — flattens less per unit q, as expected.

---

## 3. Fomalhaut rotation literature

**v sin i (spectroscopy).** The Głębocki & Gnaciński compilation (`III/244`) lists for
HD 216956 a tight cluster: 75, 85, 85, 85, 88±2, 93±9, 93, 97, 100 km/s across FWHM /
Fourier / cross-correlation methods. **Best adopted value v sin i = 93 ± 9 km/s**
(the Fourier-transform line-profile determination; also the Di Folco 2004 / Hadjara 2014
adopted value). Royer et al. ([`2002A&A...393..897R`](https://ui.adsabs.harvard.edu/abs/2002A%26A...393..897R), [`2007A&A...463..671R`](https://ui.adsabs.harvard.edu/abs/2007A%26A...463..671R)) place it in
the same 88–93 km/s range. Fomalhaut is a **moderate rotator** for an A star
(~21 % of the Keplerian critical velocity, V_crit ≈ 446 km/s).

**Direct rotation-period measurement:** none. There is no photometric or spectroscopic
P_rot in the literature; the period is derived from v sin i + R + i (below).

**Interferometric rotation (the key modern references):**

- **Le Bouquin et al. 2009, [`2009A&A...498L..41L`](https://ui.adsabs.harvard.edu/abs/2009A%26A...498L..41L)** — AMBER/VLTI spectro-astrometry
  across the Brγ line (±3 μas astrometric precision, R = 1500), spatially+spectrally
  resolving the *rotating photosphere*. **What it measured:** the **position angle of
  the stellar rotation axis on the sky, PA_star = 65° ± 3°**, found **perpendicular to
  the disk PA (156.0° ± 0.3°)**. It did **not** newly measure v sin i or i★ (it adopted
  the literature v sin i ≈ 93 km/s as the line-broadening input). It also reported
  **unexpected backward-scattering dust grains.** **Conclusion (quoted):** the data
  "validate the standard scenario for star and planet formation in which the angular
  momentum of the planetary systems are expected to be colinear with the stellar spins"
  — i.e. **spin–disk alignment**, the first such test for a debris disk and in a
  non-eclipsing system.

- **Hadjara et al. 2014, [`2014A&A...569A..45H`](https://ui.adsabs.harvard.edu/abs/2014A%26A...569A..45H)** ("Beyond the diffraction limit… II")
  — reanalyzed the AMBER/VLTI differential phases with the fast-rotator model SCIROCCO
  and delivered the **first full 3-D rotation solution for Fomalhaut:**
  **R_eq = 1.8 ± 0.2 R☉, V_eq sin i = 93 ± 16 km/s, i★ = 90° ± 9° (equator-on),
  PA_rot = 65.6° ± 5°** (PA consistent with Le Bouquin). This is the strongest single
  source: it fixes i★ directly, so V_eq ≈ v sin i.

**Alignment note.** The **sky-projected** alignment is solid (PA_star ⊥ PA_disk, both
interferometric works). Full **3-D** alignment is only marginal: Hadjara's i★ = 90° ± 9°
sits above the disk inclination i_disk ≈ 66–67° from face-on (Kalas et al. 2005,
[`2005Natur.435.1067K`](https://ui.adsabs.harvard.edu/abs/2005Natur.435.1067K); PA_disk = 156°). They agree at ~1.5–2σ, so I treat i★ = 90° (direct
measurement) as primary and carry the disk-aligned i ≈ 66° as the low-inclination bound.

---

## 4. J₂ calculation

**Inputs:** M = 1.92 M☉ (GM = 2.548×10²⁰ m³ s⁻²), R = R_eq = 1.842 R☉ = 1.281×10⁹ m,
v sin i = 93 km/s, k₂ = 0.0036. q = ω²R³/(GM) = V_eq²R/(GM); P_rot = 2πR sin i / (v sin i);
J₂ = (2/3)k₂q; flattening f = (3/2)J₂ + (1/2)q.

| i★ assumption | V_eq (km/s) | P_rot | q | **J₂ (1st-order)** | f = 1−R_p/R_eq | R_eq/R_pol |
|---|---|---|---|---|---|---|
| **90° (Hadjara, adopt)** | 93.0 | **24.0 h (1.00 d)** | 0.0435 | **1.05×10⁻⁴** | 0.022 | 1.022 |
| 81° (Hadjara −1σ) | 94.2 | 23.8 h | 0.0446 | 1.08×10⁻⁴ | 0.022 | 1.023 |
| 66.5° (disk-aligned) | 101.4 | 22.1 h | 0.0517 | 1.25×10⁻⁴ | 0.026 | 1.027 |

**Headline (adopt i★ = 90°):  P_rot ≈ 24 h (1.0 d), q ≈ 0.044, J₂ ≈ 1.0×10⁻⁴, f ≈ 0.022.**

**Corrections / limits (both apply; they partly cancel):**

1. **Fast-rotation truncation (raises J₂).** q ≈ 0.044 is large — between Jupiter's
   0.083 and the slow-star regime, well outside the linear zone. Per the methodology's
   own note, first-order J₂ under-predicts by ~10–20 % at this q. → true J₂ likely
   **~1.1–1.25×10⁻⁴** at i = 90°.
2. **k₂ model systematic (lowers J₂).** Renormalizing Claret's k₂ by the solar
   theoretical-to-empirical offset (÷1.27, §1) gives k₂ ≈ 0.0028 and J₂ ≈ 8×10⁻⁵.

Folding both plus the i★ range, the defensible band is **J₂ ≈ (0.8 – 1.3)×10⁻⁴**, central
**1.0×10⁻⁴**. `reference_radius` = R_eq = 1.842 R☉ (equatorial, mandatory for the emit).

**Sanity check vs measured oblate A-stars.** The Roche/point-mass estimate f ≈ q/2 =
0.022 matches the k₂-derived f exactly (A stars are near the centrally-condensed limit),
giving R_eq/R_pol ≈ 1.022 — a real but modest 2.2 % flattening. This is consistent with
Fomalhaut being a *slow* fast-rotator: Altair (V_eq ≈ 240–300 km/s) and Vega
(V_eq ≈ 175–235 km/s, pole-on) reach f ≈ 0.10–0.25; Fomalhaut spins ~2.5–3× slower, so an
order-of-magnitude-smaller flattening (~0.02) is exactly where it should land. Hadjara's
own Roche treatment of the same star is internally consistent with this figure.

---

## Adopted values (for whoever fills the Principia gravity model later)

- **k₂ = 0.0036** (log k₂ = −2.44), Claret 2004 grid [`2004A&A...424..919C`](https://ui.adsabs.harvard.edu/abs/2004A%26A...424..919C), 2.0 M☉ track
  T_eff-matched to Fomalhaut at 440 Myr.
- **P_rot ≈ 24 h (1.0 d)** — derived (no direct measurement), from V_eq = 93 km/s +
  i★ = 90° + R_eq = 1.842 R☉.
- **q ≈ 0.044**, **J₂ ≈ 1.0×10⁻⁴** (band 0.8–1.3×10⁻⁴), **f ≈ 0.022 (R_eq/R_pol ≈ 1.022)**,
  reference_radius = equatorial R = 1.842 R☉.

## Key bibcodes (all ADS-verified)

- [`1939MNRAS..99..451S`](https://ui.adsabs.harvard.edu/abs/1939MNRAS..99..451S) — Sterne 1939, apsidal-motion / internal-structure constants (J₂=⅔k₂q origin)
- [`2004A&A...424..919C`](https://ui.adsabs.harvard.edu/abs/2004A%26A...424..919C) — Claret 2004, k₂ grids (VizieR J/A+A/424/919) — **k₂ source**
- [`2019A&A...628A..29C`](https://ui.adsabs.harvard.edu/abs/2019A%26A...628A..29C) — Claret 2019, latest tidal-constant grids (consistency)
- [`2009ApJ...698.1778R`](https://ui.adsabs.harvard.edu/abs/2009ApJ...698.1778R) — Ragozzine & Wolf 2009, modern Love-number form of the relation
- [`2014A&A...569A..45H`](https://ui.adsabs.harvard.edu/abs/2014A%26A...569A..45H) — Hadjara et al. 2014, **i★ = 90°±9°, V_eq sin i = 93±16 km/s, R_eq = 1.8 R☉** — **primary rotation source**
- [`2009A&A...498L..41L`](https://ui.adsabs.harvard.edu/abs/2009A%26A...498L..41L) — Le Bouquin et al. 2009, PA_star = 65°±3° ⟂ disk; spin–disk alignment
- [`2012ApJ...754L..20M`](https://ui.adsabs.harvard.edu/abs/2012ApJ...754L..20M) — Mamajek 2012, M/age/params (DB recommended)
- [`2005Natur.435.1067K`](https://ui.adsabs.harvard.edu/abs/2005Natur.435.1067K) — Kalas et al. 2005, disk PA 156° / i_disk ≈ 66° (alignment bound)
- `III/244` (Głębocki & Gnaciński), [`2002A&A...393..897R`](https://ui.adsabs.harvard.edu/abs/2002A%26A...393..897R) / [`2007A&A...463..671R`](https://ui.adsabs.harvard.edu/abs/2007A%26A...463..671R) (Royer) — v sin i = 93±9 km/s
