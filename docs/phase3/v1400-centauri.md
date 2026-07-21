# V1400 Centauri / J1407b — Phase 3 Synthesis

V1400 Centauri (1SWASP J140747.93−394542.6) is a young
pre-main-sequence K5 star in Centaurus, a ~16 Myr member of the Upper
Centaurus-Lupus subgroup of the Sco-Cen association, at a Gaia DR3
distance of 138 pc (~451 ly). It sits **far beyond the 50 ly Kopernicus
cap** and is curated as a beyond-implementation-range data / Phase-3
entry, not a placeable NearStars body. It earns its place for one
reason: its companion **J1407b** is the candidate host of the largest
ring system ever proposed — a "super-Saturn" some 200× the span of
Saturn's rings.

The evidence is a single, spectacular event. Over 56 days in 2007 the
star underwent a deep (≳3 mag), intricately structured dimming, found
in archival SuperWASP photometry and published by Mamajek et al. 2012.
Kenworthy & Mamajek 2015 modelled the light curve as the transit of a
substellar companion girdled by ~37 concentric rings extending to
~0.6 AU (~90 million km), with a sharp gap near 0.4 AU plausibly swept
clean by a forming exomoon (< 0.8 M⊕). The companion mass is poorly
pinned — ~24 M_Jup from the photometric ring fit, but 60–100 M_Jup if
the rings are to stay bound (Rieder & Kenworthy 2016), so anywhere
from a giant planet to a brown dwarf. The same dynamical work found
the rings must be **retrograde** to survive.

**This is a genuinely tentative detection, and the synthesis treats it
as such.** Only one eclipse has ever been seen. Mentel et al. 2018
searched photographic plates spanning 1890–2018 and found no second
dimming — they could not confirm that the 2007 event was even a bound
object. Later work has floated the alternative that the eclipser was a
free-floating, disc-bearing object that happened to drift in front of
the star. What is solid is the light curve and the well-characterised
young host; the ringed planet is a compelling but unconfirmed,
model-dependent interpretation.

**Scenario choice for NearStars: depict the iconic super-Saturn — a
substellar companion wrapped in a vast, retrograde, multi-ring system
with an exomoon-swept gap — around a young orange K-dwarf, while
flagging the whole companion as tentative.** Picking the ringed-planet
reading over the null is an interesting-first tie-break on a
genuinely open question; the skeptical canonical reading is recorded
in *Canonical alternatives*.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `host_spectral_type` | K5 IV(e) Li (pre-main-sequence) | high | Mamajek et al. 2012 |
| `host_mass_msun` | 0.9 | medium | Mamajek 2012 — PMS evolutionary model |
| `host_radius_rsun` | 0.99 ± 0.11 | medium | Kenworthy & Mamajek 2015 |
| `host_teff_k` | 4500 (+100/−200) | medium | Mamajek 2012 (post-Gaia ~4343 K) |
| `host_age_myr` | ~16 | medium | Mamajek 2012 — Sco-Cen UCL membership |
| `host_rotation_days` | 3.20 | high | Mamajek 2012 — photometric variability (fast, active) |
| `host_visual_tint_hex` | `#ffd2a1` (warm orange) | medium | tie-break: K5 at ~4500 K blackbody |
| `companion_mass_mjup` | ~24 (range 8–100) | low | KM2015 photometric vs Rieder 2016 dynamics — order-of-magnitude spread |
| `companion_class` | substellar — giant planet / brown dwarf boundary | medium | KM2015 (>3σ substellar) |
| `companion_a_au` | ~5 | low | inferred from ring model; period ~13–17 yr unconfirmed |
| `companion_eccentricity` | 0.7–0.9 | low | KM2015 |
| `ring_outer_radius_au` | ~0.6 (~90 million km) | medium | KM2015 — ~200× Saturn's rings |
| `ring_count` | ~37 | medium | KM2015 — ≥24 edges firm |
| `ring_total_mass_mearth` | ~1 (≈100 lunar masses) | low | KM2015 |
| `ring_gap_radius_au` | ~0.4 | medium | KM2015 — clean swept gap |
| `ring_exomoon_mass_mearth` | < 0.8 (upper) | low | KM2015 — gap-carving satellite, P ~1.7 yr |
| `ring_inclination_deg` | 70.0 | medium | KM2015 — disc inclination |
| `ring_prograde` | false (retrograde) | medium | Rieder & Kenworthy 2016 — prograde rings ruled out |
| `ring_visual_tint_hex` | `#c99878` (dusty reddish-tan) | tie-break | proto-satellite dust + ice around a young object; interesting-first |
| `detection_status` | tentative (single 2007 eclipse, unconfirmed) | high | Mentel 2018 — no repeat eclipse 1890–2018 |

## Surface (host star)

The host is an ordinary young orange dwarf: K5, Teff ~4500 K, so a
warm-orange tint (`#ffd2a1`). Its youth shows in fast rotation (3.2 d)
and strong activity — near-saturation X-rays (log L_X/L_bol ≈ −3.4),
weak Hα emission, and strong lithium absorption, all consistent with a
~16 Myr Sco-Cen member still settling onto the main sequence. Nothing
about the star itself is unusual; it is the stage, not the show.

## The ring system (J1407b)

This is the headline. The 2007 light curve required a structure far
larger than any planetary ring in the Solar System: an outer radius of
~0.6 AU, roughly 200× the span of Saturn's rings, resolved by the
sharp sub-eclipses into ~37 distinct rings totalling around an Earth
mass of material. A clean gap near 0.4 AU is the tell-tale of a body
sweeping its lane — modelled as a forming exomoon below ~0.8 M⊕,
orbiting the companion every ~1.7 yr. The dynamical requirement that
the rings be **retrograde** to survive the 56-day eclipse is itself a
striking, unusual prediction.

Physically the rings are best read as a young circumplanetary disc of
proto-satellite material — dust and ice that may still be coalescing
into moons — rather than the bright water-ice debris of mature Saturn.
That argues for a dusty, reddish-tan tint (`#c99878`) rather than
Saturn's pale gold, though no colour has been measured; this is a
tie-break.

## Rotation & dynamics

| Property | Value |
|---|---|
| Host rotation | 3.20 d (fast, active) |
| Companion orbit | a ~5 AU, e 0.7–0.9, P ~13–17 yr (unconfirmed) |
| Ring orientation | i ≈ 70°, retrograde |
| Exomoon | < 0.8 M⊕, P ~1.7 yr (gap-carver) |

The companion's orbit is the weakest link — the period is bounded only
loosely and no orbit has been independently verified. The retrograde
ring geometry and the high orbital eccentricity together make this a
dynamically peculiar system even by the standards of its tentative
status.

## Visual styling

If depicted, J1407b is the spectacle: a small substellar globe encased
in a vast, finely-banded, dusty-tan ring disc (`#c99878`) tilted ~70°,
with at least one clean gap, set against a young orange K-dwarf
(`#ffd2a1`). The scale is the point — rings filling a region ~0.6 AU
across would, seen from the host, span a large fraction of the sky.
Because the detection is tentative, this is the "interesting-first"
rendering of an unconfirmed object, and should be labelled as such in
any presentation.

## Canonical alternatives

The cfg adopts the ringed-companion interpretation. The skeptical
canonical reading, which the literature increasingly entertains, is:

| Field | cfg pick | Canonical-skeptic alternative |
|---|---|---|
| `detection` | bound ringed companion J1407b | no confirmed companion — a single unrepeated eclipse |
| `eclipser` | substellar planet/BD on a ~5 AU orbit | possibly a **free-floating disc-bearing object** that drifted across the star, with no bound orbit |
| `rings` | ~37-ring retrograde super-Saturn | one of several models that fit a single light curve; gap may not be exomoon-carved (Sutton 2019) |

The interesting-first choice is defensible because the 2007 light
curve is real and the ring model is the most developed explanation —
but the null/free-floating reading cannot be excluded and is the more
conservative position.

## Bibliography

**Read / used for decisions:**
- Mamajek et al. 2012, AJ 143, 72 ([arXiv:1108.4070](https://arxiv.org/abs/1108.4070)) — discovery; host characterisation; 2007 eclipse.
- Kenworthy & Mamajek 2015, ApJ 800, 126 ([arXiv:1501.05652](https://arxiv.org/abs/1501.05652)) — the ring model (37 rings, gap, exomoon).
- Rieder & Kenworthy 2016, A&A ([arXiv:1609.08485](https://arxiv.org/abs/1609.08485)) — ring size/dynamics; retrograde requirement; 60–100 M_Jup.
- Mentel et al. 2018 ([arXiv:1810.05171](https://arxiv.org/abs/1810.05171)) — photographic-plate search; no confirming eclipse.

**Context / not read in full:**
- Sutton 2019, MNRAS 486, 1681 ([arXiv:1902.09285](https://arxiv.org/abs/1902.09285)) — argues the gap is unlikely from mean-motion resonances with nearby moons.
- Gaia DR3 — host parallax (138 pc) and proper motion.

## Open items for follow-up

- **Confirmation** is the whole game: a second eclipse (or a direct detection of the companion) would move this from tentative to real. None seen 1890–2018.
- **Companion mass** spans an order of magnitude (8–100 M_Jup) — the photometric and dynamical estimates disagree.
- **Orbit / period** unconfirmed (~13–17 yr range); the free-floating alternative would dissolve the orbit entirely.
- **Ring colour** is a pure tie-break; no photometric colour of the ring material exists.

## Related

- [psr-j0108-1431](psr-j0108-1431.md) — the other beyond-implementation-range curation in the roster (the nearest known pulsar).
- [debris-disk-color-methodology](../reference/debris-disk-color-methodology.md) — the Mie-scattering method behind the ring-colour tie-break.
- [methodology-index](../reference/methodology-index.md) — the derived-value recipe index behind these decisions.
- [methodology](../reference/methodology.md) — schema source for the Decisions table.
