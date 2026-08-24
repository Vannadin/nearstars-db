<!-- NearStars 외부 데이터 출처와 KSP 모드 attribution 정책 -->
# Data Sources and Attribution

> **Perspective.** This document is the **attribution / license**
> reference: external content NearStars reproduces (astronomical data
> values, mod cfg patterns), what license obligation each carries, and
> how NearStars discharges it.
>
> For the **install-side KSP mod list** (Required / Graphics / Compat
> classification), see [`mod-reference.md`](mod-reference.md). §2 below
> lists **every** mod NearStars touches, with a link and its license, and
> separates the ones carrying a real attribution duty (Kerbalism, whose
> algorithm is ported; Kopernicus, Principia, Sol-Configs, Firefly, whose
> cfg formats are described) from the ones referenced by name only.
>
> Triangle of license/attribution files in this repo:
> - [`LICENSE`](../../LICENSE) — NearStars' own license (CC-BY-NC-SA 4.0).
> - [`NOTICE`](../../NOTICE) — verbatim upstream license texts for any
>   third-party content this repo reproduces or describes.
> - this file — *policy*: which sources, which citation requirements,
>   how NearStars discharges them in practice.

NearStars DB synthesizes published astronomical measurements and KSP mod
configuration patterns into a single per-system JSON record. This file
lists every external source the pipeline draws from, the citation policy
of that source, and the attribution NearStars commits to provide.

---

## 1. Astronomical Data Sources

### [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu)

- **Used by:** `scripts/pipeline/fetch_planets.py`, `fetch_planets_ps.py`,
  `build_curated_from_ps.py`
- **Tables touched:** `pscomppars` (composite, reference only),
  `ps` (per-paper rows with `default_flag=1`)
- **License:** Public-domain data, citation requested
- **Citation:**
  > This research has made use of the NASA Exoplanet Archive, which is
  > operated by the California Institute of Technology, under contract
  > with the National Aeronautics and Space Administration under the
  > Exoplanet Exploration Program.
- **Reference:** Akeson, R. L. et al. 2013, PASP, 125, 989
- **Per-row paper attribution** is preserved verbatim in
  `db/planets_curated.json` (`bibcode`, `doi` fields) so each adopted
  value carries its original publication's bibcode.

### [Gaia DR3](https://www.cosmos.esa.int/gaia) (ESA)

- **Used by:** `scripts/pipeline/fetch_astrometry.py`
- **TAP endpoint:** [`https://gea.esac.esa.int/tap-server/tap`](https://gea.esac.esa.int/tap-server/tap) · [archive](https://gea.esac.esa.int/archive/)
- **License:** CC BY 4.0 (data); citation required for publications
- **Citation:**
  > This work has made use of data from the European Space Agency (ESA)
  > mission Gaia (https://www.cosmos.esa.int/gaia), processed by the
  > Gaia Data Processing and Analysis Consortium (DPAC). Funding for
  > the DPAC has been provided by national institutions, in particular
  > the institutions participating in the Gaia Multilateral Agreement.
- **References:**
  - Gaia Collaboration et al. 2016, A&A, 595, A1 (mission)
  - Gaia Collaboration et al. 2023, A&A, 674, A1 (DR3)

### [SIMBAD](https://simbad.cds.unistra.fr) (CDS Strasbourg)

- **Used by:** `scripts/pipeline/fetch_astrometry.py` (fallback),
  `fetch_stellar_props.py`
- **TAP endpoint:** `https://simbad.u-strasbg.fr/simbad/sim-tap/sync` ([TAP docs](https://simbad.cds.unistra.fr/simbad/sim-tap), [SIMBAD](https://simbad.cds.unistra.fr))
- **License:** Free for academic use; citation requested
- **Citation:**
  > This research has made use of the SIMBAD database, operated at CDS,
  > Strasbourg, France.
- **Reference:** Wenger, M. et al. 2000, A&AS, 143, 9
- **Tables used:** `basic`, `ident`, `mesDiameter`, `mesFe_H`

### [TEPCat](https://www.astro.keele.ac.uk/jkt/tepcat/) (Transiting Exoplanet Catalogue)

- **Used by:** `scripts/pipeline/fetch_planets.py` (transit fallback)
- **URL:** [`allplanets-csv.csv`](https://www.astro.keele.ac.uk/jkt/tepcat/allplanets-csv.csv) · [TEPCat](https://www.astro.keele.ac.uk/jkt/tepcat/)
- **License:** Free for academic use; citation requested
- **Citation:**
  > This paper makes use of data from the TEPCat catalogue available at
  > https://www.astro.keele.ac.uk/jkt/tepcat/
- **Reference:** Southworth, J. 2011, MNRAS, 417, 2166

### [DACE](https://dace.unige.ch) (Geneva Observatory)

- **Used by:** Manual lookup during Curation Phase 1 / Curation Phase 2 for
  RV-detected planets missing `omega_deg` / `tperi_bjd`
- **URL:** [`https://dace.unige.ch/exoplanets/`](https://dace.unige.ch/exoplanets/)
- **License:** Free for academic use; citation requested
- **Reference:** Buchschacher, N. & Alesina, F. 2019, ASP Conf. Series

### [Crossref](https://www.crossref.org)

- **Used by:** `scripts/pipeline/build_curated_from_ps.py` (DOI lookup)
- **API:** [`api.crossref.org/works/<doi>`](https://api.crossref.org) · [Crossref](https://www.crossref.org)
- **License:** Free, no authentication required
- **Note:** Crossref data is used to resolve bibcode → DOI; underlying
  paper metadata remains property of the original publisher.

### [NASA ADS](https://ui.adsabs.harvard.edu) (Astrophysics Data System)

- **Used by:** `scripts/phase3/build_bibliography.py`,
  `expand_citations.py`, `scripts/check_citation_links.py`, and every
  curation session (the project rule is that paper discovery and
  verification go through ADS, never a web search)
- **API:** [`api.adsabs.harvard.edu`](https://ui.adsabs.harvard.edu/help/api/)
  with a registered token
- **License:** Free with an account; ADS asks that its use be acknowledged
- **Citation:**
  > This research has made use of NASA's Astrophysics Data System
  > Bibliographic Services.
- **How discharged:** every citation in this repository is pinned by ADS
  bibcode or arXiv id, rendered as a clickable ADS/arXiv link (gate
  `check_citation_links.py`).

### [arXiv](https://arxiv.org) / [ar5iv](https://ar5iv.labs.arxiv.org)

- **Used by:** `scripts/phase3/fetch_arxiv_texts.py`
- **License:** per-paper (arXiv's non-exclusive license or a CC variant);
  ar5iv is an HTML rendering service
- **How discharged:** full texts are cached under `docs/phase3/_papers/`
  **for verification only** and are never redistributed or published; the
  cache is a read path for agents, not a mirror.

### [Stellarium Web](https://stellarium-web.org)

- **Used by:** `scripts/pipeline/fetch_stellarium_ids.py`,
  `scripts/verification/stellarium_crosscheck.py`
- **License:** Stellarium is GPL-2.0-or-later; only skysource IDs and
  displayed positions are read, for an independent cross-check of our own
  astrometry ([`plans/stellarium-binary-orbit-comparison.md`](../../plans/stellarium-binary-orbit-comparison.md),
  internal note)
- **Note:** no Stellarium data ships in `db/`; it is a verification oracle.

### [NIST Atomic Spectra Database](https://physics.nist.gov/asd)

- **Used by:** `scripts/refs/build_atomic_lines.py`,
  `build_lte_plasma_colors.py` (the plasma-color engine)
- **License:** US government work, free to use; NIST requests citation
- **Reference:** Kramida, A., Ralchenko, Yu., Reader, J. and NIST ASD Team,
  *NIST Atomic Spectra Database* (version 5.11), <https://physics.nist.gov/asd>
- **How discharged:** cited in
  [`element-plasma-colors.md`](element-plasma-colors.md) and the element-color
  tables generated from it.

### [USGS Spectral Library](https://pubs.usgs.gov/ds/1035/)

- **Used by:** the surface-color work
  ([`surface-color-albedo-methodology.md`](surface-color-albedo-methodology.md))
- **License:** US government work, free to use; citation requested
- **Reference:** Kokaly, R. F. et al. 2017, USGS Data Series 1035
  (*USGS Spectral Library Version 7*)

---

## 2. KSP Mod References

NearStars is downstream of several KSP mods. The skills in `.claude/skills/`
describe how to generate cfg compatible with them, citing upstream source
lines where a schema claim needs grounding. Entries are ordered by how strong
the obligation is: a ported algorithm first, then described cfg formats, then
the mods named only as targets.

### [Kerbalism](https://github.com/Kerbalism/Kerbalism)

- **License:** [Unlicense](https://github.com/Kerbalism/Kerbalism/blob/master/LICENSE)
  (public domain) — no permission needed; attribution given as a courtesy
- **NearStars use:** the **only ported algorithm** in this repository.
  `scripts/viz/render_belts.py` and `scripts/viz/fit_belts.py` reproduce the
  radiation-field signed-distance functions and the dose ramp
  `clamp(gradient·−SDF/radius,0,1)·intensity` from
  [`src/Kerbalism/Radiation/Radiation.cs`](https://github.com/Kerbalism/Kerbalism/blob/master/src/Kerbalism/Radiation/Radiation.cs),
  and [`docs/belt-viewer.html`](../belt-viewer.html) evaluates the same
  functions in the browser. Frame semantics (belts tilted, magnetopause
  star-aligned) are read from that file too.
- **Also:** [ROKerbalism](https://github.com/KSP-RO/ROKerbalism) supplies the
  RSS-scale `RadiationModel` values this project calibrates against
  ([`solar-system-radiation-belts.md`](solar-system-radiation-belts.md)).

### [Kopernicus](https://github.com/ballisticfox/Kopernicus) (ballisticfox fork)

- **License:** LGPL-3.0
- **NearStars use:** Skill `kopernicus-cfg` describes cfg syntax derived
  from reading the public source and documentation. No verbatim C# source
  is copied into this repository.

### [Principia](https://github.com/mockingbirdnest/Principia) (mockingbirdnest)

- **License:** [MIT](https://github.com/mockingbirdnest/Principia/blob/master/LICENSE.txt),
  Copyright (c) 2014 Robin Leroy
- **NearStars use:** `docs/reference/principia-cfg-reference.md` describes
  the cfg node structure with parameter tables and short syntax examples.
  Numeric values shown (e.g. Sun μ = 1.327e+11 km³/s²) are public-domain
  physical constants from IAU 2009, not Principia-specific data.

### [Sol-Configs](https://github.com/RSS-Reborn/Sol-Configs) (RSS-Reborn / ballisticfox)

- **License:** CC-BY-NC-SA 4.0 (same as NearStars; per upstream NOTICE)
- **NearStars use:** Skill `kopernicus-cfg` reference files
  (`planet-body.md`, `star-body.md`, `ocean.md`) link to upstream
  Sol-Configs files via raw URLs and pair each link with a generic
  KSP-Kopernicus pattern. Verbatim reproduction would also be
  license-compatible (both CC-BY-NC-SA 4.0), but the raw-link approach
  is preferred so upstream edits propagate automatically.

### [Firefly](https://github.com/M1rageDev/Firefly)

- **License:** code GPL-3.0, **model/texture assets All Rights Reserved**
  ([LICENSE](https://github.com/M1rageDev/Firefly/blob/master/LICENSE))
- **NearStars use:** the `firefly-cfg` skill documents its cfg schema with
  `ConfigManager.cs:line` citations and this repo writes reentry-effect cfg
  for its bodies. No asset is copied, and the plasma colours come from our
  own spectroscopy ([`element-plasma-colors.md`](element-plasma-colors.md)), not
  from Firefly's textures. Pack conventions cross-checked against
  [Firefly-Planet-Pack-Configs](https://github.com/SPACEMAN9813/Firefly-Planet-Pack-Configs).

### Every other KSP mod — referenced by name only

NearStars writes cfg that *targets* these mods' patch syntax but reproduces
no source, asset or cfg content from them, so no attribution obligation
arises. Listed here so the set is complete and each one is reachable; the
install-side classification is in [`mod-reference.md`](mod-reference.md).

| Mod | Role here |
|---|---|
| [Module Manager](https://github.com/sarbian/ModuleManager) | the patch runtime our cfg is written in (`NEEDS[]`, `FOR[]`, `@`) |
| [BurstPQS](https://github.com/Phantomical/BurstPQS) | faster terrain generation for our PQS bodies |
| [Parallax Continued](https://github.com/Gameslinx/Parallax-Continued) | terrain shaders + scatters; we emit per-body cfg |
| [OPM-Parallax](https://github.com/OneSaltyPringle/OPM-Parallax) | convention reference for those cfg |
| [Scatterer](https://github.com/LGhassen/Scatterer) | atmospheric scattering; we emit per-body cfg |
| [EVE (Redux / Volumetrics)](https://github.com/LGhassen/EnvironmentalVisualEnhancements) | clouds and aurorae. The Volumetrics early-access build is Patreon-distributed; **no EA asset or schema from it is committed here** |
| [Deferred Rendering](https://github.com/LGhassen/Deferred) | lighting path the visual work assumes |
| [Textures Unlimited](https://github.com/shadowmage45/TexturesUnlimited) | PBR shader stack |
| [TUFX](https://github.com/KSPModStewards/TUFX) | post-processing profiles |
| [Distant Object Enhancement](https://github.com/KSPModStewards/DistantObjectEnhancement) | far-away body visibility |
| [PlanetShine](https://github.com/PapaJoesSoup/ksp-planetshine) | albedo lighting |
| [ResearchBodies](https://github.com/JPLRepo/ResearchBodies) | discoverability; our patch layer is retired but documented |
| [BetterTimeWarpContinued](https://github.com/linuxgurugamer/BetterTimeWarpContinued) | warp rates for interstellar coasting |
| [Relativity](https://github.com/Vannadin/Relativity) | our own companion mod |

Kerbal Space Program itself is © Squad / Private Division / Intercept Games;
NearStars is an unofficial fan modification.

---

## 2b. Vendored web assets (the published site)

These ship **inside** `docs/`, so their licenses travel with this repository.

| Asset | Where | License |
|---|---|---|
| [marked](https://github.com/markedjs/marked) 12.0.2 | `docs/assets/marked.min.js` | MIT |
| [github-markdown-css](https://github.com/sindresorhus/github-markdown-css) 5.5.0 | `docs/assets/github-markdown-{dark,light}.min.css` | MIT |
| [Plotly.js](https://github.com/plotly/plotly.js) | `docs/assets/plotly.min.js` | MIT |
| [Geist / Geist Mono](https://github.com/vercel/geist-font) | `docs/assets/fonts/*.woff2` | SIL OFL 1.1 |
| [three.js](https://github.com/mrdoob/three.js) 0.160.0 | **not vendored** — ES module loaded from [jsDelivr](https://cdn.jsdelivr.net/npm/three@0.160.0) by the star map and orbit viewers | MIT |

One more ported implementation, from the literature rather than a mod:
**Mauk & Fox 2010**'s own Kennel–Petschek code
([Zenodo](https://zenodo.org/records/4782323)) is ported to
`scripts/refs/kp_limit.py` and validated against their printed
intermediates. [REBOUND](https://github.com/hannorein/rebound) (GPL-3.0) is
used as an installed library by the stability sandbox, not vendored.

---

## 3. NearStars-Originated Content

The following are produced by NearStars itself and are not derived
from any of the above:

- The pipeline scripts in `scripts/pipeline/`
- The schema design in `scripts/pipeline/schema.py` and the cfg-layer
  decisions in `docs/reference/methodology.md`
- The binary-system epoch resolution logic
  ([`binary-epoch-pipeline.md`](binary-epoch-pipeline.md))
- The curated JSON files (`db/*_curated.json`) — these are aggregations
  of cited measurements; the aggregation, method-tier selection, and
  `recommended` flag are NearStars editorial decisions

These are licensed **CC-BY-NC-SA 4.0** — see [`LICENSE`](../../LICENSE), and
[`NOTICE`](../../NOTICE) for the third-party texts this file summarizes.

---

## 4. Reporting Upstream Issues

When NearStars cross-validation discovers a defect in any of the data
sources above, the issue is recorded in
[`archive_issues.md`](archive_issues.md) and, when appropriate, reported
to the catalog maintainer using the contact in that file.

## Related

- [methodology](methodology.md) — cluster hub; data-sources documents the citations this methodology requires
- [archive_issues](archive_issues.md) — defects discovered in the sources cited here
- [mod-reference](mod-reference.md) — downstream mods (some shared attribution path: Kopernicus, Principia, Sol-Configs)
- [guideline](guideline.md) — project-level scope referencing these sources
- [rex-data-comparison](rex-data-comparison.md) — REX's license-declaration discrepancy noted in §1
