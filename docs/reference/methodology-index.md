<!-- NS의 논문-근거화 derived-value 방법론 문서 전체 인덱스 (Phase 3/4가 도출에 사용) -->
# Methodology Index: Paper-Grounded Derived-Value Recipes

NearStars assigns many physical values that are **derived, not measured**: a body's
color, magnetic field, atmosphere, internal heat, and so on. Each such value has a
dedicated **methodology reference**: an ADS-verified recipe (relation + regimes +
worked examples + an annotated, citation-checked bibliography), modeled on the
`planetary-dynamo-scaling.md` gold standard.

This page is the single index of those recipes. Phase 3 derives cfg-ready values
through them; Phase 4 validates owner art-direction against them. Every methodology
doc has a Korean mirror under `ko/docs/reference/`.

> Discipline: citations are resolved against NASA ADS (registered API token), not
> ad-hoc web search; arXiv id where one exists, else the authoritative ADS bibcode.
> Textbook relations (e.g. Darwin–Radau, the Planck function) are the allowed
> exception to "derived values must be paper-grounded."

## Magnetism, structure & dynamics

| Methodology | Grounds | Key references |
|---|---|---|
| [planetary-dynamo-scaling](planetary-dynamo-scaling.md) | Giant/BD magnetic field strength (energy-flux) | Christensen 2009; Reiners & Christensen 2010 ([arXiv:1007.1514](https://arxiv.org/abs/1007.1514)); Yadav & Thorngren 2017 |
| [rocky-planet-dynamo-methodology](rocky-planet-dynamo-methodology.md) | Rocky (Earth/super-Earth) magnetic moment + surface field | Rodríguez-Mozos & Moya 2022 ([arXiv:2203.01065](https://arxiv.org/abs/2203.01065)); Olson & Christensen 2006; Gaidos 2010; Driscoll & Olson 2011 |
| [planetary-magnetosphere-geometry-methodology](planetary-magnetosphere-geometry-methodology.md) | Magnetosphere standoff + belt extent/intensity from B (→ Kerbalism); exact K–P ceiling calculator `scripts/refs/kp_limit.py` | Chapman & Ferraro 1931; Shue 1997/98; Kennel & Petschek 1966; Summers 2009/2014; Mauk & Fox 2010 (+Zenodo port); Seltzer 1979/92; Schulz & Lanzerotti 1974; Thorne 2010 |
| [mass-radius-relation-methodology](mass-radius-relation-methodology.md) | Mass ↔ radius ↔ density tie-break | Seager 2007; Zeng 2016; Fortney 2007; Chen & Kipping 2017 |
| [tidal-locking-timescale-methodology](tidal-locking-timescale-methodology.md) | Spin state / synchronization timescale | Goldreich & Soter 1966; Hut 1981; Leconte 2015 |
| [tidal-heating-methodology](tidal-heating-methodology.md) | Tidal heating flux (Io/Enceladus-calibrated) | Peale, Cassen & Reynolds 1979; Segatz 1988; Henning 2009 |
| [body-figure-methodology](body-figure-methodology.md) | Oblateness J₂ + tidal triaxiality C₂₂ (Principia gravity model) | Helled 2011 ([arXiv:1109.1627](https://arxiv.org/abs/1109.1627)); Murray & Dermott 1999; Radau–Darwin / Maclaurin; Io/Titan anchors |
| [cassini-state-obliquity-methodology](cassini-state-obliquity-methodology.md) | Equilibrium spin-axis tilt of a tidally-damped body (locked ≠ obliquity 0) | Peale 1969; Ward 1975; Ward & Hamilton 2004; Bills 2005; Baland 2011; Margot 2007 (Mercury anchor) |

## Orbits & epoch

| Methodology | Grounds | Key references |
|---|---|---|
| [emit-orbit-phase-match-methodology](emit-orbit-phase-match-methodology.md) | Emit orbital phase (Ω/ω/M) of a directly-detected planet: sky-PA match + epoch rewind to 1950.0 | Beichman 2025 ([arXiv:2508.03814](https://arxiv.org/abs/2508.03814)); Pourbaix & Correia 2017; Murray & Dermott 1999 (textbook) |

## Atmosphere & thermal

| Methodology | Grounds | Key references |
|---|---|---|
| [exoplanet-atmosphere-methodology](exoplanet-atmosphere-methodology.md) | Atmosphere retention + pressure/composition | Zahnle & Catling 2017 (cosmic shoreline); Owen 2019; Dong 2017/2018 |
| [tidally-locked-temperature-methodology](tidally-locked-temperature-methodology.md) | Surface temperature / climate state | Joshi 1997; Wordsworth 2015; Koll & Abbot 2016; Koll 2022 |
| [internal-heat-luminosity-methodology](internal-heat-luminosity-methodology.md) | Internal heat + self-luminosity (T_int) | Burrows 1997; Baraffe 2003; Fortney 2007; Marley 2007 |

## Color (shared CIE 1931 → sRGB engine)

All four reflected/emitted color recipes share one colorimetry engine (CIE 1931 CMF →
XYZ → IEC 61966-2-1 sRGB), owned by the reflected-color doc.

| Methodology | Grounds | Key references |
|---|---|---|
| [stellar-photospheric-color-methodology](stellar-photospheric-color-methodology.md) | Star incandescent color (Teff → sRGB) | Husser 2013 (PHOENIX); Castelli & Kurucz 2003; Allard BT-Settl 2011; Mann 2015; Pickles 1998 |
| [atmosphere-reflected-color-methodology](atmosphere-reflected-color-methodology.md) | Sky/cloud reflected color | Sneep & Ubachs 2005 (Rayleigh); Gao 2021; Irwin 2024; CIE 1931 / IEC sRGB |
| [surface-color-albedo-methodology](surface-color-albedo-methodology.md) | Surface mineral color + Bond albedo | Burns 1993; Hapke 1981/2012; Kokaly (USGS) 2017; Grundy |
| [debris-disk-color-methodology](debris-disk-color-methodology.md) | Debris-disk dust scattering color (Mie) | Draine 2003; Bohren & Huffman 1983; Khare 1984 |
| [element-plasma-colors](element-plasma-colors.md) | Emission/plasma color (aurora, reentry, lines) | NIST ASD; Pearse & Gaydon; Park 1990 |

## Validation (not derivation, but Phase-4 gates)

- **Orbital/stability simulation**: REBOUND N-body (WHFast / TRACE / IAS15) + MEGNO
  chaos indicator + Hill-stability + resonance analysis, under `phase3/stability-sim/`.
  Confirms a system architecture survives (bounded eccentricities, no ejections) before
  a Phase-4 orbit is locked.
- [principia-cfg-reference](principia-cfg-reference.md) / [principia-geopotential-data](principia-geopotential-data.md): n-body gravity-model (J2/geopotential) cfg conventions.
- [gravity-significance-floor-methodology](gravity-significance-floor-methodology.md): literature grounding for the far-field gravity-truncation floor `a_floor` + switching-shell ratio (Principia fork). Folkner 2014 / Park 2021 (ephemeris perturber selection); Chesley 2014 (Yarkovsky detectability); Jiang & Tremaine 2010 (Jacobi radius); Rein & Spiegel 2015 (force-error budgets).
- [binary-epoch-pipeline](binary-epoch-pipeline.md): multi-star Keplerian → ICRS epoch propagation.
- [solar-system-radiation-belts](solar-system-radiation-belts.md): stock Kerbalism cfg vs ADS-grounded physics for all 7 magnetized Solar-System bodies (Earth/Jupiter/Saturn/Uranus/Neptune/Mercury/Ganymede) — calibrates the magnetosphere-geometry recipe; in-game SDF cross-section renders on the [wiki](https://github.com/Vannadin/nearstars-db/wiki/Radiation-Belts). Joy 2002; Cooper 1983; Ness 1986/1989; Winslow 2013; Kivelson 2002; +18 more.

## Related

- [methodology](methodology.md): the upstream DB-building workflow (Phase 1–3 data pipeline) these recipes feed.
- [tools](tools.md): the tool/script index.
