<!-- 태양계 자기권 천체 7종의 실제 방사선대 물리 vs Kerbalism 스톡 cfg 비교 (ADS 근거, 위키 시각화 연동) -->
# Solar-System radiation belts: stock Kerbalism cfg vs the physics

A body-by-body audit of every Solar-System object that has a **magnetosphere with
trapped-particle belts** (or a magnetosphere at all), comparing the **Kerbalism /
ROKerbalism stock cfg** against the **real, ADS-grounded physics**. It exists to
calibrate the NearStars magnetosphere-geometry recipe against real bodies before
that recipe emits belts for fictional ones, and to feed the physics-accurate cfg
values back where the stock model is a rough placeholder.

Cross-section visualizations (in-game `RadiationModel` SDF rendered exactly) are on
the wiki: **[Radiation Belts](https://github.com/Vannadin/nearstars-db/wiki/Radiation-Belts)**.
The renderer is `scripts/viz/render_belts.py` (+ `render_belts_bodies.py` driver;
reproduces `Radiation.cs` SDFs), see
[`planetary-magnetosphere-geometry-methodology.md`](planetary-magnetosphere-geometry-methodology.md)
for the field-shape schema.

## Scope — only magnetized bodies

Belts require an intrinsic dynamo strong enough to trap particles. In the Solar
System that is **7 bodies**: Earth, Jupiter, Saturn, Uranus, Neptune (planetary
dynamos), Mercury (tiny), and Ganymede (embedded moon dynamo). **Venus, Mars, the
Moon, Io, Europa, Callisto, Titan, Triton, Pluto** have no intrinsic global field →
no belts → surface dose is the direct wind/GCR flux (`radiation_surface` only, no
`RadiationModel` belt). They are out of scope here.

## Summary table — physics anchors (all ADS-pinned)

| Body | Magnetopause standoff | Dipole tilt | Offset | Belt structure | Peak dose (order) |
|---|---|---|---|---|---|
| **Earth** | ~10 R_E | 11° | small | two separated belts (D inner + hollow outer) | ~10² rad/day (peak) |
| **Jupiter** | **63 R_J** (compressed) / 92 (expanded) | 10.3° | ~0.13 R_J | dipolar inner (D-cut) + flat magnetodisc | ~10³–10⁴ rad/day |
| **Saturn** | **22–27 R_S** | **<0.007°** | 0.047 R_S N | **no classic inner belt** (rings sweep it); weak moon-chopped outer; CRAND-only | ≪ Jupiter |
| **Uranus** | **18 R_U** | **59°** | **0.3 R_U** | offset+tilted, moon-swept, helical tail | e⁻ ≥1.2 MeV |
| **Neptune** | **26.5 R_N** | **47°** | **0.55 R_N** | offset+tilted, peak L≈7, Triton cut ~14 R_N | e⁻ >1 MeV |
| **Mercury** | **1.45 R_M** (1.35–1.55) | <3° | 0.20 R_M N (484 km) | **no stable belt** — surface is the loss cone | (surface direct) |
| **Ganymede** | **~2 R_G** (upstream) | ~176° (≈anti-aligned) | — | weak embedded, **open polar caps**, source-starved | shield −50–60% of ambient |

The headline findings: **(1)** stock Kerbalism/RSS already captures the ice-giant
offset-tilted dipoles (Uranus/Neptune) and Mercury's offset reasonably well; **(2)**
the big stock errors are **Jupiter** (belt too far out, no D-cut, no magnetodisc) and
**belt-intensity provenance** everywhere (stock values are tuned, not derived); **(3)**
**Saturn's "outer-only, no inner belt"** stock choice is *physically correct* — the
rings occupy and absorb the inner-belt zone.

---

## Per-body: stock cfg vs physical

Each block gives the stock `RadiationBody`/`RadiationModel` (ROKerbalism `System/
Radiation.cfg` + RSS anchors), the physical values with ADS pins, and the delta.

### Earth (anchor — stock = physical)
Stock `earth`: inner 0.813/0.70 (border 0.915 → **D-cut**), outer 2.63/2.48 (border
1.44 → **hollow O**), pause 15, `radiation_inner` 10.376 / `radiation_outer` 2.214 /
pause −0.010, `geomagnetic_pole_lat` 80.37, offset 0.07. This is the calibration
anchor; belt dose ~10.4 rad/h at the inner peak matches the observed inner-belt
proton peak order. No change.

### Jupiter
| Field | Stock (RSS `jupiter`) | Physical | Source |
|---|---|---|---|
| inner_dist / radius | 6.0 / 1.0 | **2.0 / 2.0** (dipolar, ~1.5–2 R_J peak) | Divine & Garrett 1983 [`1983JGR....88.6889D`](https://ui.adsabs.harvard.edu/abs/1983JGR....88.6889D) |
| inner_border_radius | (none) | **1.3** (loss-cone D-cut) | (belt physics) |
| outer_dist / radius | 6.5 / 6.5 (concentric) | **4.17 / 2.5, deform_xy 0.174** (flat magnetodisc) | Khurana 1989 [`1989JGR....9411791K`](https://ui.adsabs.harvard.edu/abs/1989JGR....9411791K) |
| pause_radius | 60 | **63** (compressed; 92 expanded) | Joy 2002 [`2002JGRA..107.1309J`](https://ui.adsabs.harvard.edu/abs/2002JGRA..107.1309J) |
| radiation_inner | 300 | **~1500** (order 10³–10⁴; conf low) | Divine & Garrett 1983 |
| geomagnetic_pole_lat | −81.4 | **−80** (tilt 10.3°, reversed) | Connerney 2022 JRM33 [`2022JGRE..12707055C`](https://ui.adsabs.harvard.edu/abs/2022JGRE..12707055C) |
| geomagnetic_offset | (none) | **0.1** (eccentric dipole) | JRM33 |

Inner belt is **dipolar** (equatorial + non-equatorial electrons, pitch 0–90°;
Santos-Costa 2001 [`2001P&SS...49..303S`](https://ui.adsabs.harvard.edu/abs/2001P%26SS...49..303S)) → round, not flat. Outer belt is a **hinged
magnetodisc** (equatorially confined current sheet; Khurana 1989) → flat. Io/Amalthea/
ring absorption gaps (Santos-Costa 2001) cannot be rendered by two shells — a fidelity
ceiling. Stock puts the strong belt ~3× too far out (6 vs ~2 R_J) and omits both the
D-cut and the magnetodisc flattening.

### Saturn
| Field | Stock (RSS anchor) | Physical | Source |
|---|---|---|---|
| has_inner | false (outer only) | **false — correct** (rings absorb) | Cooper 1983 [`1983JGR....88.3945C`](https://ui.adsabs.harvard.edu/abs/1983JGR....88.3945C) |
| pause_radius | 20 | **~24** (22–27 bimodal) | Achilleos 2008 [`2008JGRA..11311209A`](https://ui.adsabs.harvard.edu/abs/2008JGRA..11311209A) |
| outer belt | 7/7 | ~2.3–6 R_S, moon-chopped corridors | Kollmann 2013 [`2013Icar..222..323K`](https://ui.adsabs.harvard.edu/abs/2013Icar..222..323K) |
| radiation_outer | 150 | **weak** (CRAND-only, ≪ Jupiter) | Kollmann 2017 [`2017NatAs...1..872K`](https://ui.adsabs.harvard.edu/abs/2017NatAs...1..872K) |
| dipole tilt | (near 0) | **<0.007°** (25.2 arcsec!) | Cao 2020 [`2020Icar..34413541C`](https://ui.adsabs.harvard.edu/abs/2020Icar..34413541C) |
| offset | — | 0.047 R_S north | Cao 2020 |

**Stock "outer-only, no inner belt" is physically right**: the dense A–C rings sit
exactly where an inner belt would form and absorb it (Cooper 1983); the surviving
belt is chopped into inter-moon corridors (Kollmann 2013, Roussos 2007
[`2007JGRA..112.6214R`](https://ui.adsabs.harvard.edu/abs/2007JGRA..112.6214R)). Source is passive CRAND, so intensity is orders below Jupiter
(Kollmann 2017). A thin isolated proton belt exists between atmosphere and D-ring
(Roussos 2018 [`2018Sci...362.1962R`](https://ui.adsabs.harvard.edu/abs/2018Sci...362.1962R)) — real but negligible for gameplay. Dipole is
near-perfectly axisymmetric (Cao 2020), so tilt ≈ 0.

### Uranus
| Field | Stock (RSS anchor) | Physical | Source |
|---|---|---|---|
| geomagnetic tilt | pole_lat 31 (=59°) | **59–60°** ✓ | Ness 1986 [`1986Sci...233...85N`](https://ui.adsabs.harvard.edu/abs/1986Sci...233...85N) |
| geomagnetic_offset | 0.3 | **0.3 R_U** ✓ | Ness 1986 |
| pause_radius | (≈18) | **18.0 R_U** (bow shock 23.7) | Ness 1986 |
| belt peak | — | **413 nT at 4.19 R_U** | Ness 1986 |
| radiation_inner | 75 | e⁻ ≥1.2 MeV, p ≥4 MeV | Krimigis 1986 [`1986Sci...233...97K`](https://ui.adsabs.harvard.edu/abs/1986Sci...233...97K) |
| quadrupole | — | large (Q3 model) | Connerney 1987 [`1987JGR....9215329C`](https://ui.adsabs.harvard.edu/abs/1987JGR....9215329C) |

**Stock already captures the extreme offset-tilted dipole** (tilt 59°, offset 0.3) —
its main gap is that the belt intensity is a tuned placeholder, not derived. Moons
(Miranda→Titania) sweep the belts across a huge L-range every 17.24 h (Stone 1986
[`1986Sci...233...93S`](https://ui.adsabs.harvard.edu/abs/1986Sci...233...93S)); the near-sunward spin axis winds the tail into a helix (pitch
5.5°; Behannon 1987 [`1987JGR....9215354B`](https://ui.adsabs.harvard.edu/abs/1987JGR....9215354B)). Polarity sign not stated in the primary
abstracts (not fabricated).

### Neptune
| Field | Stock (RSS anchor) | Physical | Source |
|---|---|---|---|
| geomagnetic tilt | pole_lat 43 (=47°) | **47°** ✓ | Ness 1989 [`1989Sci...246.1473N`](https://ui.adsabs.harvard.edu/abs/1989Sci...246.1473N) |
| geomagnetic_offset | 0.55 | **0.55 R_N** ✓ | Ness 1989 |
| pause_radius | 26.5 | **26.5 R_N** ✓ (bow shock 34.9) | Ness 1989 |
| belt peak | — | **magnetic L ≈ 7** | Stone 1989 [`1989Sci...246.1489S`](https://ui.adsabs.harvard.edu/abs/1989Sci...246.1489S) |
| outer cutoff | — | **~14 R_N (Triton)** | Krimigis 1989 [`1989Sci...246.1483K`](https://ui.adsabs.harvard.edu/abs/1989Sci...246.1483K) |
| quadrupole/octupole | — | quad ≈ dipole at surface | Connerney 1991 [`1991JGR....9619023C`](https://ui.adsabs.harvard.edu/abs/1991JGR....9619023C) |

Like Uranus, **stock captures the offset-tilted dipole** (tilt 47°, offset 0.55).
Belts peak at L≈7 (just outside Proteus at 4.75 R_N), carved by ring/moon absorption
(Paranicas 1991 [`1991JGR....9619131P`](https://ui.adsabs.harvard.edu/abs/1991JGR....9619131P)), hard outer cut at Triton's orbit. Field is
strongly non-dipolar near the planet (quad/octupole comparable to dipole).

### Mercury
| Field | Stock (ROKerbalism `mercury`) | Physical | Source |
|---|---|---|---|
| pause_radius | 1.6 | **1.45 R_M** (1.35–1.55, → 1.28 in storms) | Winslow 2013 [`2013JGRA..118.2213W`](https://ui.adsabs.harvard.edu/abs/2013JGRA..118.2213W) |
| belts | none | **none** ✓ (too small/dynamic) | Schriver 2015 [`2015AGUFM.P53A2089S`](https://ui.adsabs.harvard.edu/abs/2015AGUFM.P53A2089S) |
| geomagnetic_offset | 0.208 | **0.198** (484 km north) | Anderson 2011 [`2011Sci...333.1859A`](https://ui.adsabs.harvard.edu/abs/2011Sci...333.1859A) |
| tilt | (small) | **<3°** (<0.8° refined) | Anderson 2011/2012 |
| moment | — | 190–195 nT·R_M³, southward | Anderson 2011, Korth 2015 [`2015JGRA..120.4503K`](https://ui.adsabs.harvard.edu/abs/2015JGRA..120.4503K) |

**Stock correctly models no belt** — Mercury's magnetosphere is too small and dynamic
to trap a stable population (only a quasi-trapped 1–10 keV equatorial cloud + transient
bursts). The northward offset (484 km ≈ 0.2 R_M) concentrates surface dose in the
**southern** hemisphere/cusps; SEP electrons reach the surface near-instantly on open
field lines (Gershman 2015 [`2015JGRA..120.8559G`](https://ui.adsabs.harvard.edu/abs/2015JGRA..120.8559G)). Stock pause 1.6 is slightly generous
vs the physical 1.45.

### Ganymede
| Field | Stock (ROKerbalism `ganymede`) | Physical | Source |
|---|---|---|---|
| surface dipole | (implicit) | **719 nT eq** (tilt 176°) | Kivelson 2002 [`2002Icar..157..507K`](https://ui.adsabs.harvard.edu/abs/2002Icar..157..507K) |
| has_pause | (none) | **~2 R_G upstream** (5.5 across) | Kivelson 1998 [`1998JGR...10319963K`](https://ui.adsabs.harvard.edu/abs/1998JGR...10319963K) |
| inner belt | 0.8/0.6, rad 0.33 | single weak, source-starved | Allioux 2013 [`2013AdSpR..51.1204A`](https://ui.adsabs.harvard.edu/abs/2013AdSpR..51.1204A) |
| open caps | — | **poleward of 30–45°** (leaky) | Pappalardo 1998 [`1998DPS....30.5401P`](https://ui.adsabs.harvard.edu/abs/1998DPS....30.5401P) |
| net role | — | **shield −50–60%** of ambient | Allioux 2013 |

The Solar System's only **weak-field embedded moon** — a dynamo inside a giant's
magnetosphere (the weak-field sub-regime of the geometry methodology). Ganymede's 719 nT
only modestly exceeds the local Jovian field → small ~2 R_G standoff, **open polar caps**
(reconnection with Jupiter), no bow shock (sub-Alfvénic → Alfvén wings; Saur 2018
[`2018ASSL..448..153S`](https://ui.adsabs.harvard.edu/abs/2018ASSL..448..153S)). It molds only <~100 keV ions into thin belts; the dominant dose
is Jupiter's ambient belt at ~15 R_J, which Ganymede's field attenuates by ~50–60% for
a low orbiter. **Stock omits the pause entirely** — a fix worth adding.

---

## What the two-shell model cannot represent (fidelity ceilings)

- **Moon/ring absorption gaps** (Saturn corridors, Neptune Proteus notch, Uranus moon
  sweeping) — Kerbalism has only inner+outer tori, no per-L depletion.
- **Time variation** — the ice-giant belts wobble every rotation (tilt+offset); cfg is static.
- **Multipole distortion** near the planet (Uranus/Neptune quad≈dipole) — the dipole
  `geomagnetic_offset` is the only handle.
- **Belt intensity from first principles** — governed by source/loss/Kennel–Petschek, not
  field strength (see geometry methodology Part B); all `radiation_*` values are regime
  calls, conf low.

## Citations (ADS-pinned, by body)

- **Jupiter**: Joy 2002 [`2002JGRA..107.1309J`](https://ui.adsabs.harvard.edu/abs/2002JGRA..107.1309J); Divine & Garrett 1983 [`1983JGR....88.6889D`](https://ui.adsabs.harvard.edu/abs/1983JGR....88.6889D);
  Connerney 2022 (JRM33) [`2022JGRE..12707055C`](https://ui.adsabs.harvard.edu/abs/2022JGRE..12707055C); Santos-Costa 2001 [`2001P&SS...49..303S`](https://ui.adsabs.harvard.edu/abs/2001P%26SS...49..303S);
  Khurana 1989 [`1989JGR....9411791K`](https://ui.adsabs.harvard.edu/abs/1989JGR....9411791K).
- **Saturn**: Cooper 1983 [`1983JGR....88.3945C`](https://ui.adsabs.harvard.edu/abs/1983JGR....88.3945C); Achilleos 2008 [`2008JGRA..11311209A`](https://ui.adsabs.harvard.edu/abs/2008JGRA..11311209A);
  Kollmann 2013 [`2013Icar..222..323K`](https://ui.adsabs.harvard.edu/abs/2013Icar..222..323K); Kollmann 2017 [`2017NatAs...1..872K`](https://ui.adsabs.harvard.edu/abs/2017NatAs...1..872K); Roussos 2007
  [`2007JGRA..112.6214R`](https://ui.adsabs.harvard.edu/abs/2007JGRA..112.6214R); Roussos 2018 [`2018Sci...362.1962R`](https://ui.adsabs.harvard.edu/abs/2018Sci...362.1962R); Cao 2020 [`2020Icar..34413541C`](https://ui.adsabs.harvard.edu/abs/2020Icar..34413541C).
- **Uranus**: Ness 1986 [`1986Sci...233...85N`](https://ui.adsabs.harvard.edu/abs/1986Sci...233...85N); Krimigis 1986 [`1986Sci...233...97K`](https://ui.adsabs.harvard.edu/abs/1986Sci...233...97K); Stone
  1986 [`1986Sci...233...93S`](https://ui.adsabs.harvard.edu/abs/1986Sci...233...93S); Connerney 1987 [`1987JGR....9215329C`](https://ui.adsabs.harvard.edu/abs/1987JGR....9215329C); Behannon 1987
  [`1987JGR....9215354B`](https://ui.adsabs.harvard.edu/abs/1987JGR....9215354B).
- **Neptune**: Ness 1989 [`1989Sci...246.1473N`](https://ui.adsabs.harvard.edu/abs/1989Sci...246.1473N); Krimigis 1989 [`1989Sci...246.1483K`](https://ui.adsabs.harvard.edu/abs/1989Sci...246.1483K); Stone
  1989 [`1989Sci...246.1489S`](https://ui.adsabs.harvard.edu/abs/1989Sci...246.1489S); Connerney 1991 [`1991JGR....9619023C`](https://ui.adsabs.harvard.edu/abs/1991JGR....9619023C); Paranicas 1991
  [`1991JGR....9619131P`](https://ui.adsabs.harvard.edu/abs/1991JGR....9619131P).
- **Mercury**: Winslow 2013 [`2013JGRA..118.2213W`](https://ui.adsabs.harvard.edu/abs/2013JGRA..118.2213W); Anderson 2011 [`2011Sci...333.1859A`](https://ui.adsabs.harvard.edu/abs/2011Sci...333.1859A);
  Schriver 2015 [`2015AGUFM.P53A2089S`](https://ui.adsabs.harvard.edu/abs/2015AGUFM.P53A2089S); Gershman 2015 [`2015JGRA..120.8559G`](https://ui.adsabs.harvard.edu/abs/2015JGRA..120.8559G); Korth 2015
  [`2015JGRA..120.4503K`](https://ui.adsabs.harvard.edu/abs/2015JGRA..120.4503K).
- **Ganymede**: Kivelson 2002 [`2002Icar..157..507K`](https://ui.adsabs.harvard.edu/abs/2002Icar..157..507K); Kivelson 1998 [`1998JGR...10319963K`](https://ui.adsabs.harvard.edu/abs/1998JGR...10319963K);
  Kivelson 1996 [`1996Natur.384..537K`](https://ui.adsabs.harvard.edu/abs/1996Natur.384..537K); Pappalardo 1998 [`1998DPS....30.5401P`](https://ui.adsabs.harvard.edu/abs/1998DPS....30.5401P); Allioux 2013
  [`2013AdSpR..51.1204A`](https://ui.adsabs.harvard.edu/abs/2013AdSpR..51.1204A); Saur 2018 [`2018ASSL..448..153S`](https://ui.adsabs.harvard.edu/abs/2018ASSL..448..153S).

## Related

- [`planetary-magnetosphere-geometry-methodology.md`](planetary-magnetosphere-geometry-methodology.md)
  — the field-shape recipe + Kerbalism SDF schema this audit renders.
- [`planetary-dynamo-scaling.md`](planetary-dynamo-scaling.md) /
  [`rocky-planet-dynamo-methodology.md`](rocky-planet-dynamo-methodology.md) — the B-field
  inputs.
- Wiki: [Radiation Belts](https://github.com/Vannadin/nearstars-db/wiki/Radiation-Belts)
  (cross-section images).
- [methodology-index](methodology-index.md).
