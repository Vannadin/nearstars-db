# REX vs NearStars Data Comparison

> Source: Real Exoplanets mod v0.9.6 (commit
> [`e32c0ab`](https://github.com/andikisare/Real-Exoplanets/commit/e32c0abcbdf87fdd0f2de42165b23a16d2346afa),
> 2020-04-11) compared against NearStars `db/systems/` recommended values
> as of 2026-05-21.
> Purpose: Quantify the gap between REX (the KSP 1.8.0-era predecessor
> that NearStars's README cites as inspiration) and NearStars. Covers
> coverage, numeric values, multi-star topology, and provenance. No DB
> changes — findings only.

---

## TL;DR

> **No coverage gap.** All 5 REX systems are already in our DB. REX
> has zero stars or planets we don't have.

> **Three planet rosters are out of date in REX.** Barnard b
> (Ribas 2018) was retracted; Proxima c is disputed; Teegarden d
> wasn't discovered yet. NearStars has the post-2020 corrections.

> **REX can't model hierarchical multi-star systems.** It encodes
> Proxima as a Sun-orbiting Body. NearStars does Jacobi decomposition
> + ICRF Cartesian for Principia n-body compatibility. This is the
> structural reason NearStars exists as a separate project, not a
> REX patch.

> **Stellar values agree where both projects pull from the same era.**
> Three rows differ ≥10% (Barnard mass, Teegarden mass, Teegarden
> T_eff) — all because REX froze in 2020-04 and we have newer
> measurements.

---

## Context

NearStars's README declares the project "spiritual successor to REX
(KSP 1.8.0 era)" but never quantifies what changed. This document
pins down coverage, numeric values, multi-star topology, and
provenance differences between the two datasets.

**Scope.** REX `v0.9.6` at upstream commit
[`e32c0ab`](https://github.com/andikisare/Real-Exoplanets/commit/e32c0abcbdf87fdd0f2de42165b23a16d2346afa)
(2020-04-11). NearStars side: `db/systems/` recommended values as of
`2026-05-21`. No DB changes from this comparison.

**External references.**

- REX repo: <https://github.com/andikisare/Real-Exoplanets>
- REX SpaceDock: <https://spacedock.info/mod/2286/Real%20Exoplanets>
- REX KSP Forum:
  <https://forum.kerbalspaceprogram.com/topic/187033-181-real-exoplanets-v096-04032020/>
- NASA Exoplanet Archive: <https://exoplanetarchive.ipac.caltech.edu/>
- License — REX README says "All Rights Reserved", SpaceDock says
  CC-BY-NC-SA. The two declarations conflict; treat as ARR for any
  reuse.

---

## 1. At-a-glance comparison

| | REX v0.9.6 | NearStars 2026-05 |
|---|---|---|
| **Coverage** | 5 systems / 8 stars / 15 planets | ~50 systems / 152 components |
| **Last update** | 2020-04-11 (frozen) | active |
| **Multi-star** | Kopernicus barycenter `Body`, flat | Jacobi (`primary_is_barycenter_of`), ICRF Cartesian |
| **Frame** | KSP equatorial (via Space Engine) | ICRF / J2000 |
| **Solver** | none — Kopernicus renders at runtime | Markley non-iterative cubic, offline |
| **Provenance** | inline prose comments in cfg | per-measurement `bibcode` + `doi` |
| **Epoch** | KSP game-time seconds, opaque origin | explicit JD (B1950 = JD 2433282.5) |

---

## 2. Coverage

### REX systems

| System | Stars | Planets |
|---|---|---|
| Alpha Centauri | A, B, Proxima (+ barycenter Body) | Proxima b, c |
| Barnard's Star | Barnard | b (0.40 AU) |
| Tau Ceti | Tau Ceti | e, f, g, h |
| TRAPPIST-1 | TRAPPIST-1 | b, c, d, e, f, g, h |
| Teegarden's Star | Teegarden | b, c |

### Overlap

REX 5-system mapping to NearStars files:

- `alpha_centauri_a.json`, `alpha_centauri_b.json`, `proxima_cen.json`
- `barnards_star.json`
- `tau_cet.json`
- `trappist_1.json`
- `teegardens_star.json`

> **REX-only stars: 0.** REX never expanded past these five since 2020.

NearStars covers ~45 additional systems (36 Oph, 40 Eri, 47 UMa,
55 Cnc, 61 Cyg, 61 Vir, 70 Oph, Altair, Arcturus, AU Mic, Sirius,
Fomalhaut, Eps Eri, Eps Ind, Eta Cas, plus a long GJ tail and the
implementation shortlist).

---

## 3. Stellar parameters

REX cfg values converted via `M_⊙ = 1.989e30 kg`,
`R_⊙ = 6.957e8 m`. REX T_eff is read from
`Atmosphere.temperatureSeaLevel` on each star body — Kopernicus
encodes the star's "surface temperature" in that field, and REX
actually uses it this way.

### Mass (M_⊙)

| Star | REX | NearStars | Δ |
|---|---|---|---|
| α Cen A | 1.100 | **1.1055** | −0.5% |
| α Cen B | 0.907 | **0.9373** | −3.2% |
| Proxima | 0.123 | **0.1221** | +0.7% |
| Barnard | 0.144 | **0.161** | **−10.5%** ⚠ |
| Tau Ceti | 0.793 | **0.783** | +1.3% |
| TRAPPIST-1 | 0.089 | **0.0898** | −0.9% |
| Teegarden | 0.080 | **0.097** | **−17.5%** ⚠ |

### Radius (R_⊙)

| Star | REX | NearStars | Δ |
|---|---|---|---|
| α Cen A | 1.227 | **1.2234** | +0.3% |
| α Cen B | 0.865 | **0.8632** | +0.2% |
| Proxima | 0.141 | **0.141** | 0% |
| Barnard | 0.196 | **0.1868** | +4.9% |
| Tau Ceti | 0.793 | **null** | n/a |
| TRAPPIST-1 | 0.121 | **0.1192** | +1.5% |
| Teegarden | 0.127 | **0.12** | +5.8% |

### T_eff (K)

| Star | REX | NearStars | Δ |
|---|---|---|---|
| α Cen A | 5790 | **5790** | — |
| α Cen B | 5260 | **5260** | — |
| Proxima | 3042 | **3498** | **−13.0%** ⚠ |
| Barnard | 3134 | **3278** | −4.4% |
| Tau Ceti | 5344 | **5320** | +0.5% |
| TRAPPIST-1 | 2511 | **2566** | −2.1% |
| Teegarden | 2637 | **3034** | **−13.1%** ⚠ |

### Flagged disagreements (≥10%)

> **Barnard mass −10.5%.** REX pre-dates Mann 2015. NS is current.

> **Teegarden mass −17.5%.** REX pre-dates CARMENES (Zechmeister
> 2019, Dreizler 2024). NS is current.

> **Proxima T_eff −13%.** REX 3042 K matches Boyajian 2012
> interferometry. NS 3498 K is from Suárez Mascareño 2025 — at the
> upper end of the published range (literature spans 2900–3500 K).
> Worth re-checking which calibration we trust.

> **Teegarden T_eff −13%.** REX value pre-dates modern M-dwarf
> T_eff calibrations. NS is current.

---

## 4. α Centauri AB orbit

| Element | REX | NearStars |
|---|---|---|
| P (yr) | 79.92 | **79.91 ± 0.01** |
| e | 0.5179 | **0.5179 ± 0.0003** |
| a (AU) | 23.52 | 23.46 |
| i (°) | 234.5 (KSP equatorial) | 79.205 ± 0.05 (ICRF) |
| Ω (°) | 190.486 | 204.85 ± 0.08 |
| ω_A (°) | −17.143 | 231.65 ± 0.08 |
| Epoch | KSP seconds | T_jd_tt = 2435035.7 (= 1954.8) |
| Source | "Space Engine" (cfg comment) | Pourbaix & Correia 2017 / Kervella 2016 |

> **Shape agrees to 0.01%.** Both encode the Pourbaix 2002/2017
> solution. Orientation angles differ only because REX uses KSP
> equatorial and NS uses ICRF — same physical orbit, different frame.

**Mass-ratio check.** Implied M_A/M_B is 1.184 in REX (from a_A/a_B
ratio) and 1.179 in NS (from explicit masses) — effectively identical.

---

## 5. α Cen AB ↔ Proxima topology

This is the most substantive methodology divergence between REX and
NearStars.

### REX

- Proxima orbits the **Sun** directly with `mode = 0`,
  `semiMajorAxis = 4.015e16 m` (= 4.24 ly),
  `period = 1.061e13 s` (= 336,000 yr — arbitrary, since "orbits"
  for non-bound stars aren't physical).
- α Cen AB barycenter likewise orbits the Sun.
- **No hierarchical binding** between Proxima and AB.

### NearStars

`alpha_centauri_a.json::binary_orbit` declares `hierarchy = "triple"`
with two orbits:

- **AB** (inner) — ORB6 grade 1, full Keplerian elements.
- **AB-Proxima** (outer) — P = 547,000 yr, e = 0.5, a = 8,700 AU,
  i = 107.6°, source Kervella 2017,
  `primary_is_barycenter_of = ["Alpha Centauri A", "Alpha Centauri B"]`.
  Periastron epoch not constrained → `phase_reliable = false`. Build
  pipeline skips Kepler composition and uses direct Gaia DR3
  astrometry for Proxima at JD 2433282.5. Schema-level grouping is
  ready for future Gaia DR4 NSS solutions.

> **Why REX can't model this.** Kopernicus orbits are pure
> Keplerian-around-parent — no n-body, no Jacobi. NearStars exports
> ICRF Cartesian state to Principia precisely to bypass this. This is
> the structural reason NearStars is a separate project, not a REX
> patch.

For three-way comparison with Stellarium, see
`docs/reference/stellarium-binary-orbit-comparison.md` (when promoted)
or `plans/stellarium-binary-orbit-comparison.md` — Stellarium also
lacks hierarchical multi-star support but matches NS's Hilditch
rotation convention.

---

## 6. Planet rosters

### Proxima Cen

| | REX | NearStars |
|---|---|---|
| Planets | **b, c** | **b, d** |
| b (a/e) | 0.0480 AU / e=0.21 | 0.04848 AU / e=0.0 |
| Source (b) | Anglada-Escudé 2016 | Suárez Mascareño 2025 |
| Other | c at 1.480 AU (Damasso 2020, disputed) | d at 0.02881 AU (Faria 2022) |

### Barnard

| | REX | NearStars |
|---|---|---|
| Planets | **b only** | **d, b, c, e** |
| b (a/mass) | 0.404 AU / 3.75 M_⊕ | 0.0229 AU / 0.30 M_⊕ Msini |
| Source | Ribas 2018 | González Hernández 2024 / Basant 2025 |

> **REX's Barnard b is retracted.** Lubin et al. 2021 showed it was
> a stellar-activity artifact. ESPRESSO surveys then found a
> different 4-planet sub-Earth system at 0.02–0.04 AU. REX value is
> obsolete.

### Tau Ceti

| | REX | NearStars |
|---|---|---|
| Planets | **e, f, g, h** | **f, g, h** (no e) |
| Source | Feng 2017 | Feng 2017, `pl_controv_flag=1` |

> **NS is missing Tau Ceti e.** Same source paper, same dispute
> flag. Probably intentional curation (e was the most disputed of
> the four), but unverified. → open question.

### TRAPPIST-1

| | REX | NearStars |
|---|---|---|
| Planets | **b–h** (7) | **b–h** (7) |
| Source | Gillon 2017 era | Agol 2021 |
| Agreement | sub-percent on `a` for all 7 | TTV-refined masses |

Example: TRAPPIST-1b a = 0.01155 AU (REX) vs 0.01154 AU (NS).

### Teegarden

| | REX | NearStars |
|---|---|---|
| Planets | **b, c** | **b, c, d** |
| Source | Zechmeister 2019 | Dreizler 2024 |

> **NS has the third planet (d).** REX froze before its discovery.

### Headline finding for planets

> Three systems most surveyed post-2020 are the three where REX is
> behind: **Barnard** (overhauled), **Proxima** (new inner d, c
> demoted), **Teegarden** (new outer d). TRAPPIST-1 and Tau Ceti have
> been refined but not restructured.

---

## 7. Provenance and methodology

| | REX | NearStars |
|---|---|---|
| Attribution | inline cfg comments, e.g. `// Used Space Engine to approximate` | per-measurement `bibcode`, `doi`, `method`, `recommended` |
| Source pinning | none | NEA / SIMBAD / Gaia DR3 with `accessed` date |
| Competing values | one value, silently picked | full `*_measurements[]` arrays, e.g. TRAPPIST-1 has 6 mass entries from Gillon 2016 → Agol 2021 |
| Units | SI mixed with runtime scale factors | SI raw, solar derived, ICRF Cartesian km/km·s⁻¹ |
| Epoch | KSP game seconds, opaque origin | explicit JD + label |

> **NS's most defensible advantage.** REX's prose attribution isn't
> machine-checkable and silently freezes whichever paper the author
> read at the time. NS's per-measurement catalog with `recommended`
> flags makes curation auditable and enables freshness checks.

---

## 8. Implications for NearStars

1. **No coverage gap to fill.** Implementation shortlist work isn't
   blocked by anything REX did.

2. **Retraction watch.** REX's Barnard b is a now-invalidated
   discovery. NS's `bibcode` + `recommended` flag policy protects us —
   but only if the curation step actively monitors retractions. Worth
   confirming that NEA's `pl_controv_flag` propagates into our review
   path.

3. **Tau Ceti e investigation.** Either deliberately dropped (most
   disputed of the four Feng 2017 detections) or oversight. Document
   in `db/systems/tau_cet.json::meta.notes` either way.

4. **Proxima T_eff worth a second look.** NS's 3498 K sits at the
   upper bound of the published range. Document the choice in
   `proxima_cen.json::meta.notes`.

5. **Validation of the Jacobi multi-star choice.** REX's flat
   "Proxima-around-Sun" encoding shows what NS buys by going
   Jacobi + ICRF Cartesian. This is the convention validation that
   motivates the binary-epoch pipeline existing at all.

6. **License clarity.** REX README says "All Rights Reserved";
   SpaceDock says CC-BY-NC-SA. Don't reuse REX assets without
   resolving this with the author. (Currently we reuse nothing.)

---

## 9. Open questions

- Why is Tau Ceti **'e' missing** from `tau_cet.json` but not f/g/h
  (same paper, same dispute flag)? Curation or oversight?
- Does our build pipeline currently **flag NEA `pl_controv_flag=1`**
  rows in a review report? If not, future retractions could slip in.
- **REX atmosphere curves**: REX hand-tunes `temperatureCurve` /
  `pressureCurve` per body. If we ever ship Kopernicus configs, do
  we synthesize, copy REX, or hand-curate? Out of scope here.
- **REX upstream status.** Last commit 2020-04-11; appears
  abandoned. If we ever wanted to push retraction fixes back, we'd
  need to fork.
