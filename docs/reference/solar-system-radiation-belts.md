<!-- 태양계 자기권 천체 7종의 실제 방사선대 물리 vs Kerbalism 스톡 cfg 비교 (ADS 근거, 위키 시각화 연동) -->
# Solar-System radiation belts: stock Kerbalism cfg vs the physics

A body-by-body audit of every Solar-System object that has a **magnetosphere with
trapped-particle belts** (or a magnetosphere at all), comparing the **Kerbalism /
ROKerbalism stock cfg** against the **real, ADS-grounded physics**. It exists to
calibrate the NearStars magnetosphere-geometry recipe against real bodies before
that recipe emits belts for fictional ones, and to feed the physics-accurate cfg
values back where the stock model is a rough placeholder.

Cross-section visualizations are on the wiki:
**[Radiation Belts](https://github.com/Vannadin/nearstars-db/wiki/Radiation-Belts)** —
two renders per body, both the in-game `RadiationModel` SDF: **stock** = the shipped
cfg (verified 2026-07-24 against `KSP-RO/ROKerbalism` `System/Radiation.cfg` +
`Support/RSS.cfg`), **physical** = the same SDF with its six belt-shape parameters
**numerically fitted** (`scripts/viz/fit_belts.py`, Nelder-Mead multi-start) to the real
dipole drift-shell region between the ADS-anchored field lines (r = L cos²λ, loss-cone
cut at the atmosphere top). Fit quality is stated per belt as IoU (cross-section area
overlap): **≥ 0.96 everywhere** except Jupiter's flat magnetodisc (0.87, a torus-model
ceiling). The fitted parameter sets live in the render driver; two-shell tori still
can't capture every real feature (moon/ring gaps, time variation), noted below.
The renderer is `scripts/viz/render_belts.py` (+ `render_belts_bodies.py` driver); the SDF
is reproduced from [`src/Kerbalism/Radiation/Radiation.cs`](https://github.com/Kerbalism/Kerbalism/blob/master/src/Kerbalism/Radiation/Radiation.cs)
([Kerbalism](https://github.com/Kerbalism/Kerbalism), public domain / [Unlicense](https://github.com/Kerbalism/Kerbalism/blob/master/LICENSE)); see
[`planetary-magnetosphere-geometry-methodology.md`](planetary-magnetosphere-geometry-methodology.md)
for the field-shape schema.

## Scope — only magnetized bodies

Belts require an intrinsic dynamo strong enough to trap particles. In the Solar
System that is **7 bodies**: Earth, Jupiter, Saturn, Uranus, Neptune (planetary
dynamos), Mercury (tiny), and Ganymede (embedded moon dynamo). **Venus, Mars, the
Moon, Io, Europa, Callisto, Titan, Triton, Pluto** have no intrinsic global field →
no belts → surface dose is the direct wind/GCR flux (`radiation_surface` only, no
`RadiationModel` belt). They are out of scope here.

## Reading the cfg correctly (two traps)

An earlier revision of this audit (and its hand-placed "physical" renders) misread two
SDF parameters; both are corrected throughout and worth recording:

1. **Belt `dist`/`radius` live in `deform_xy`-squashed coordinates.** The SDF tests
   `√((x²+z²)·deform_xy) − dist`, so a belt's *equatorial* extent is
   `(dist ± radius)/√deform_xy`, further carved by the border torus. Stock Earth's outer
   belt (2.6338/2.48, deform_xy 0.7225, border 1.4412/1.4875) actually spans
   **3.45–6.0 R_E at the equator** — close to the physical outer-belt heart (L 3–7),
   not "centred at 2.6 R_E" as a naive read of `outer_dist` suggests.
2. **`pause_radius` is not the sub-solar standoff.** Dayside x is multiplied by
   `pause_compression` before the sphere test, so nose = `pause_radius/pause_compression`,
   flank = `pause_radius`, tail = `pause_radius/pause_extension`. Stock Earth (15,
   comp 1.5) → nose exactly **10 R_E** = the Shue standoff, with flank/nose 1.5 = 2^0.585
   (Shue α). Any NearStars emit of a Chapman–Ferraro standoff must therefore set
   `pause_radius = R_mp × pause_compression`.

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

The headline findings: **(1)** stock ROKerbalism **Earth is well-calibrated on both
character and position** once the cfg is read correctly (D-cut inner belt 1.3–2.0 R_E,
hollow outer 3.45–6.0, magnetopause nose 10 R_E) — an earlier revision claimed position
drift from the two cfg traps above, retracted; **(2)** the real stock errors are
**Jupiter** (belt ~3× too far out, no D-cut, no magnetodisc) and the **ice giants
sharing an untuned copy of the generic `saturn` model** (outer 7/7 blob spanning
0–14 R, pause 20 — only tilt/offset are per-body; Uranus `radiation_inner = 75` and
Neptune `= 39` are dead cfg, the model has `has_inner = false`); **(3)** **Saturn's
"outer-only, no inner belt"** stock choice is *physically correct* — the rings occupy
and absorb the inner-belt zone — though its 7/7 blob still floods the swept ring zone;
**(4)** **belt-intensity provenance** is tuned, not derived, everywhere.

---

## Per-body: stock cfg vs physical

Each block gives the stock `RadiationBody`/`RadiationModel` (ROKerbalism `System/
Radiation.cfg` + RSS anchors), the physical values with ADS pins, and the delta.

### Earth (calibration anchor — and, read correctly, a good one)
| Field | Stock (`earth`) | Physical | Source |
|---|---|---|---|
| pause | 15 / comp 1.5 → **nose 10 R_E** | ~10 R_E sub-solar ✓ | Shue 1997 [`1997JGR...102.9497S`](https://ui.adsabs.harvard.edu/abs/1997JGR...102.9497S), Fairfield 1971 [`1971JGR....76.6700F`](https://ui.adsabs.harvard.edu/abs/1971JGR....76.6700F) |
| inner belt | 0.813/0.70 dxy 0.572, border 0.915 → equator **1.29–2.0 R_E** | peak **L≈1.5**, ~1.1–2 R_E, lower edge ~1000 km (loss-cone-depleted below; SAA dips to ~200 km via the dipole offset) ✓ | (AP9; Ripoll 2016) |
| outer belt | 2.63/2.48 dxy 0.7225, border carve → equator **3.45–6.0 R_E** | **heart L≈4–5**, L 3–7 (≈; edge 6 vs 7) | Reeves 2013 [`2013Sci...341..991R`](https://ui.adsabs.harvard.edu/abs/2013Sci...341..991R), Thorne 2013 [`2013Natur.504..411T`](https://ui.adsabs.harvard.edu/abs/2013Natur.504..411T) |
| slot region | the gap 2.0–3.45 R_E ✓ | **L≈2–3** (hiss-cleared) | Ripoll 2016 [`2016GeoRL..43.5616R`](https://ui.adsabs.harvard.edu/abs/2016GeoRL..43.5616R) |
| radiation_inner/outer | 10.376 / 2.214 | order-consistent | — |
| geomagnetic_pole_lat / offset | 80.37 (tilt 9.6°) / 0.07 | tilt ~11° / ~0.08 R_E | IGRF (accurate) |

Read with the correct SDF semantics, the stock anchor is good on **both character and
position**: D-cut inner belt at 1.29–2.0 R_E, slot, hollow outer at 3.45–6.0, magnetopause
nose exactly 10 R_E, accurate tilt/offset, inner dose ~10.4 rad/h at the observed proton
peak. (An earlier revision of this doc claimed the pause was 1.5× generous and the outer
belt 2× inward — both were the cfg-reading traps above; retracted.) The physical render
refits the exact L-shells (inner L 1.1–2 with the ~1000 km lower boundary, outer L 3–7:
IoU 0.99/0.98); the visible deltas vs stock are small — outer edge 7 vs 6 R_E and a
slightly thicker inner crescent. The outer-belt horns keep a low (~300 km) cut — unlike
the inner belt, outer-zone electrons routinely precipitate into the bounce/drift loss
cone at low altitude (POES observations; Liu 2024
[`2024JGRA..12932171L`](https://ui.adsabs.harvard.edu/abs/2024JGRA..12932171L)).

### Jupiter
| Field | Stock (RSS `jupiter`) | Physical | Source |
|---|---|---|---|
| inner belt | 6.0/1.0 (no dxy) → equator **5–7 R_J** | dipolar shell **L 1.2–3** (peak ~1.5–2 R_J; fit IoU .98) | Divine & Garrett 1983 [`1983JGR....88.6889D`](https://ui.adsabs.harvard.edu/abs/1983JGR....88.6889D) |
| inner border | (none) | loss-cone D-cut at the atmosphere | (belt physics) |
| outer belt | 6.5/6.5 (concentric blob) | **magnetodisc slab 3–16 R_J × ±3** (half-width ~3–3.5 R_J canonical; 3–16 is a frame truncation of a disc extending past 50 R_J) (fit IoU .87 — torus ceiling) | Khurana 1989 [`1989JGR....9411791K`](https://ui.adsabs.harvard.edu/abs/1989JGR....9411791K) |
| pause | 60 / comp 1.05 → nose 57 | nose **63** (compressed; 92 expanded) | Joy 2002 [`2002JGRA..107.1309J`](https://ui.adsabs.harvard.edu/abs/2002JGRA..107.1309J) |
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
| Field | Stock (`saturn` model, RSS.cfg) | Physical | Source |
|---|---|---|---|
| has_inner | false (outer only) | **false — correct** (rings absorb) | Cooper 1983 [`1983JGR....88.3945C`](https://ui.adsabs.harvard.edu/abs/1983JGR....88.3945C) |
| pause | 20 / comp 1.02 → nose 19.6 | nose **~24** (22–27 bimodal) | Achilleos 2008 [`2008JGRA..11311209A`](https://ui.adsabs.harvard.edu/abs/2008JGRA..11311209A) |
| outer belt | 7/7 → equator **0–14 R_S** (floods the swept ring zone) | shell **L 2.3–6** (fit IoU .98), moon-chopped corridors | Kollmann 2013 [`2013Icar..222..323K`](https://ui.adsabs.harvard.edu/abs/2013Icar..222..323K) |
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
| Field | Stock (generic `saturn` model, RSS.cfg) | Physical | Source |
|---|---|---|---|
| geomagnetic tilt | pole_lat 31.4 (=58.6°) | **59–60°** ✓ | Ness 1986 [`1986Sci...233...85N`](https://ui.adsabs.harvard.edu/abs/1986Sci...233...85N) |
| geomagnetic_offset | 0.3 | **0.3 R_U** ✓ | Ness 1986 |
| pause | 20 / comp 1.02 → nose 19.6 | nose **18.0 R_U** (bow shock 23.7) | Ness 1986 |
| belts | generic outer 7/7 blob (0–14 R_U); **radiation_inner 75 is dead cfg** (`has_inner = false`) | two shells **L 1.5–5 / L 5–10** bounded by moon sweeping — Miranda L 5.1 ("except inside the orbit of Miranda"), electron minima at Miranda/Ariel/Umbriel L 5.1/7.5/10.4 with broad maxima between; trapping detectable to Titania ~L 17 (fit IoU .98/.97) | Krimigis 1986, Cheng 1987 [`1987JGR....9215315C`](https://ui.adsabs.harvard.edu/abs/1987JGR....9215315C) |
| radiation_inner | 75 (unused) | e⁻ ≥1.2 MeV, p ≥4 MeV | Krimigis 1986 [`1986Sci...233...97K`](https://ui.adsabs.harvard.edu/abs/1986Sci...233...97K) |
| quadrupole | — | large (Q3 model) | Connerney 1987 [`1987JGR....9215329C`](https://ui.adsabs.harvard.edu/abs/1987JGR....9215329C) |

**Stock captures the extreme offset-tilted dipole axis** (pole_lat 31.4, offset 0.3) but
the field *shape* is an untuned copy of the generic `saturn` model (single 7/7 outer
blob, pause 20) shared verbatim with Neptune — and its `radiation_inner = 75` never
fires, since the model has no inner belt. The belt intensity is a tuned placeholder. Moons
(Miranda→Titania) sweep the belts across a huge L-range every 17.24 h (Stone 1986
[`1986Sci...233...93S`](https://ui.adsabs.harvard.edu/abs/1986Sci...233...93S)); the near-sunward spin axis winds the tail into a helix (pitch
5.5°; Behannon 1987 [`1987JGR....9215354B`](https://ui.adsabs.harvard.edu/abs/1987JGR....9215354B)). Polarity sign not stated in the primary
abstracts (not fabricated).

### Neptune
| Field | Stock (generic `saturn` model, RSS.cfg) | Physical | Source |
|---|---|---|---|
| geomagnetic tilt | pole_lat 43 (=47°) | **47°** ✓ | Ness 1989 [`1989Sci...246.1473N`](https://ui.adsabs.harvard.edu/abs/1989Sci...246.1473N) |
| geomagnetic_offset | 0.55 | **0.55 R_N** ✓ | Ness 1989 |
| pause | 20 / comp 1.02 → nose 19.6 (an earlier revision claimed 26.5 ✓ — wrong, the model is the shared `saturn` one) | nose **26.5 R_N** (bow shock 34.9) | Ness 1989 |
| belts | generic outer 7/7 blob; **radiation_inner 39 is dead cfg** (`has_inner = false`) | shells **L 1.5–5 / L 5–14** (fit IoU .98/.97), peak **L ≈ 7** | Stone 1989 [`1989Sci...246.1489S`](https://ui.adsabs.harvard.edu/abs/1989Sci...246.1489S) |
| outer cutoff | — | **~14 R_N (Triton)** | Krimigis 1989 [`1989Sci...246.1483K`](https://ui.adsabs.harvard.edu/abs/1989Sci...246.1483K) |
| quadrupole/octupole | — | quad ≈ dipole at surface | Connerney 1991 [`1991JGR....9619023C`](https://ui.adsabs.harvard.edu/abs/1991JGR....9619023C) |

Like Uranus, **stock captures the offset-tilted dipole axis** (tilt 47°, offset 0.55)
on top of the shared generic field shape.
Belts peak at L≈7 (just outside Proteus at 4.75 R_N), carved by ring/moon absorption
(Paranicas 1991 [`1991JGR....9619131P`](https://ui.adsabs.harvard.edu/abs/1991JGR....9619131P)), hard outer cut at Triton's orbit. Field is
strongly non-dipolar near the planet (quad/octupole comparable to dipole).

### Mercury
| Field | Stock (ROKerbalism `mercury`) | Physical | Source |
|---|---|---|---|
| pause | 1.6 / comp 1.4 → nose **1.14** | nose **1.45 R_M** (1.35–1.55, → 1.28 in storms) | Winslow 2013 [`2013JGRA..118.2213W`](https://ui.adsabs.harvard.edu/abs/2013JGRA..118.2213W) |
| belts | none | **none** ✓ (too small/dynamic) | Schriver 2015 [`2015AGUFM.P53A2089S`](https://ui.adsabs.harvard.edu/abs/2015AGUFM.P53A2089S) |
| geomagnetic_offset | 0.208 | **0.198** (484 km north) | Anderson 2011 [`2011Sci...333.1859A`](https://ui.adsabs.harvard.edu/abs/2011Sci...333.1859A) |
| tilt | (small) | **<3°** (<0.8° refined) | Anderson 2011/2012 |
| moment | — | 190–195 nT·R_M³, southward | Anderson 2011, Korth 2015 [`2015JGRA..120.4503K`](https://ui.adsabs.harvard.edu/abs/2015JGRA..120.4503K) |

**Stock correctly models no belt** — Mercury's magnetosphere is too small and dynamic
to trap a stable population (only a quasi-trapped 1–10 keV equatorial cloud + transient
bursts). The northward offset (484 km ≈ 0.2 R_M) concentrates surface dose in the
**southern** hemisphere/cusps; SEP electrons reach the surface near-instantly on open
field lines (Gershman 2015 [`2015JGRA..120.8559G`](https://ui.adsabs.harvard.edu/abs/2015JGRA..120.8559G)). Stock's nose (1.6/1.4 = 1.14 R_M) is
slightly *tight* vs the physical 1.45 — not generous, as an earlier revision (reading
pause_radius as the standoff) had it.

### Ganymede
| Field | Stock (ROKerbalism `ganymede`) | Physical | Source |
|---|---|---|---|
| surface dipole | (implicit) | **719 nT eq** (tilt 176°) | Kivelson 2002 [`2002Icar..157..507K`](https://ui.adsabs.harvard.edu/abs/2002Icar..157..507K) |
| has_pause | (none) | **~2 R_G upstream** (5.5 across) | Kivelson 1998 [`1998JGR...10319963K`](https://ui.adsabs.harvard.edu/abs/1998JGR...10319963K) |
| inner belt | 0.8/0.6, rad 0.33 | single weak closed-line belt **L 1.1–1.9**, absorbed at the surface itself (airless — no altitude cut) (fit IoU .97), source-starved | Allioux 2013 [`2013AdSpR..51.1204A`](https://ui.adsabs.harvard.edu/abs/2013AdSpR..51.1204A) |
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
- **A flat magnetodisc's sharp radial edges** — the best torus fit is a lens (Jupiter
  outer IoU 0.87 vs ≥0.96 for every dipolar shell); real discs taper, so the lens is
  arguably closer to nature than the slab target itself.
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
  1986 [`1986Sci...233...93S`](https://ui.adsabs.harvard.edu/abs/1986Sci...233...93S); Cheng 1987 [`1987JGR....9215315C`](https://ui.adsabs.harvard.edu/abs/1987JGR....9215315C); Connerney 1987 [`1987JGR....9215329C`](https://ui.adsabs.harvard.edu/abs/1987JGR....9215329C); Behannon 1987
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
- `scripts/viz/fit_belts.py` — the numerical fitter (dipole-shell targets → SDF
  parameters, IoU-scored); fitted parameter sets live in `render_belts_bodies.py`.
- [`planetary-dynamo-scaling.md`](planetary-dynamo-scaling.md) /
  [`rocky-planet-dynamo-methodology.md`](rocky-planet-dynamo-methodology.md) — the B-field
  inputs.
- Wiki: [Radiation Belts](https://github.com/Vannadin/nearstars-db/wiki/Radiation-Belts)
  (cross-section images).
- [methodology-index](methodology-index.md).
