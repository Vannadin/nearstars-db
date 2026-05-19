<!-- NearStars 외부 데이터 출처와 KSP 모드 attribution 정책 -->
# Data Sources and Attribution

NearStars DB synthesizes published astronomical measurements and KSP mod
configuration patterns into a single per-system JSON record. This file
lists every external source the pipeline draws from, the citation policy
of that source, and the attribution NearStars commits to provide.

---

## 1. Astronomical Data Sources

### NASA Exoplanet Archive

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

### Gaia DR3 (ESA)

- **Used by:** `scripts/pipeline/fetch_astrometry.py`
- **TAP endpoint:** `https://gea.esac.esa.int/tap-server/tap`
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

### SIMBAD (CDS Strasbourg)

- **Used by:** `scripts/pipeline/fetch_astrometry.py` (fallback),
  `fetch_stellar_props.py`
- **TAP endpoint:** `https://simbad.u-strasbg.fr/simbad/sim-tap/sync`
- **License:** Free for academic use; citation requested
- **Citation:**
  > This research has made use of the SIMBAD database, operated at CDS,
  > Strasbourg, France.
- **Reference:** Wenger, M. et al. 2000, A&AS, 143, 9
- **Tables used:** `basic`, `ident`, `mesDiameter`, `mesFe_H`

### TEPCat (Transiting Exoplanet Catalogue)

- **Used by:** `scripts/pipeline/fetch_planets.py` (transit fallback)
- **URL:** `https://www.astro.keele.ac.uk/jkt/tepcat/allplanets-csv.csv`
- **License:** Free for academic use; citation requested
- **Citation:**
  > This paper makes use of data from the TEPCat catalogue available at
  > https://www.astro.keele.ac.uk/jkt/tepcat/
- **Reference:** Southworth, J. 2011, MNRAS, 417, 2166

### DACE (Geneva Observatory)

- **Used by:** Manual lookup during Phase 1 / Phase 2 curation for
  RV-detected planets missing `omega_deg` / `tperi_bjd`
- **URL:** `https://dace.unige.ch/exoplanets/`
- **License:** Free for academic use; citation requested
- **Reference:** Buchschacher, N. & Alesina, F. 2019, ASP Conf. Series

### Crossref

- **Used by:** `scripts/pipeline/build_curated_from_ps.py` (DOI lookup)
- **API:** `https://api.crossref.org/works/<bibcode>`
- **License:** Free, no authentication required
- **Note:** Crossref data is used to resolve bibcode → DOI; underlying
  paper metadata remains property of the original publisher.

---

## 2. KSP Mod References

NearStars is downstream of several KSP mods. The skills in `.agents/skills/`
describe how to generate cfg files compatible with these mods, sometimes
citing example fragments from upstream repositories.

### Kopernicus (ballisticfox fork)

- **Repo:** `ballisticfox/Kopernicus`
- **License:** LGPL-3.0
- **NearStars use:** Skill `kopernicus-cfg` describes cfg syntax derived
  from reading the public source and documentation. No verbatim C# source
  is copied into this repository.

### Principia (mockingbirdnest)

- **Repo:** `mockingbirdnest/Principia`
- **License:** MIT
- **NearStars use:** `docs/reference/principia-cfg-reference.md` describes
  the cfg node structure with parameter tables and short syntax examples.
  Numeric values shown (e.g. Sun μ = 1.327e+11 km³/s²) are public-domain
  physical constants from IAU 2009, not Principia-specific data.

### Sol-Configs (RSS-Reborn / ballisticfox)

- **Repo:** `RSS-Reborn/Sol-Configs`
- **License:** Not specified (no LICENSE file as of 2026-05-19)
- **NearStars use:** Skill `kopernicus-cfg` reference files
  (`planet-body.md`, `star-body.md`, `ocean.md`) link to upstream
  Sol-Configs files via raw URLs and pair each link with a generic
  KSP-Kopernicus pattern. No Sol-Configs cfg content is reproduced
  verbatim in this repository, because Sol-Configs has no published
  license.

### Module Manager, Parallax Continued, EVE, Scatterer, Firefly, etc.

- **Use:** Mentioned by name in skill reference files for cfg-compat
  contexts; no source or cfg content is copied. See
  [`docs/reference/mod-reference.md`](mod-reference.md) for the full
  dependency list and upstream links.

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

These are subject to whichever license the NearStars repository adopts
(see top-level `LICENSE`).

---

## 4. Reporting Upstream Issues

When NearStars cross-validation discovers a defect in any of the data
sources above, the issue is recorded in
[`archive_issues.md`](archive_issues.md) and, when appropriate, reported
to the catalog maintainer using the contact in that file.
