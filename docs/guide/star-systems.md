<!-- v1 항성계 일곱 곳 소개(거리·구성·볼거리) -->
# Star Systems

The mod ships seven systems: 12 stellar components and 22 planets, drawn from the 145-system research database for their proximity, their planets, their public recognition, and above all their variety. Every stellar type from a white dwarf to a brown-dwarf binary shows up at least once, so no two destinations play the same way.

A quick word on the tags you will see below. Bodies marked **(fiction)** are gameplay filler: they pass a plausibility gate against published constraints and are always flagged, never mixed silently with real detections. Bodies marked **(candidate)** are real but unconfirmed detections still awaiting confirmation. Bodies marked **(disputed)** are published detections that remain debated in the literature. All of them are kept for variety and documented honestly.

One more thing runs through every entry: our own physics. Each planetary system has been put through long-term N-body integrations (REBOUND, using energy-conserving integrators plus the MEGNO chaos indicator, where a value of **MEGNO ≈ 2 means fully regular, non-chaotic motion**). The output is browsable as interactive 3D orbit viewers, linked per system and indexed at the [orbit-viewer gallery](https://vannadin.github.io/nearstars-db/phase4/orbit-viewers/).

---

## Alpha Centauri

**4.4 ly · G2 V + K1 V binary, orbited by Proxima Centauri (M5.5)**

The nearest star system and the flagship destination. A and B swing around each other every ~80 years on a notably eccentric orbit, and under Principia you can watch that barycentric dance play out in real time. The system carries planets around two of its stars:

- **Proxima b**, the famous temperate Earth-mass planet in the habitable zone of Proxima, the actual nearest star
- **Proxima c**, a cold super-Earth on a wide orbit around Proxima
- **Proxima d**, a sub-Earth skimming Proxima
- **Alpha Centauri A b (candidate)**, a Saturn-class giant in Alpha Centauri A's own habitable zone, imaged once by JWST in 2024 and not yet recovered in follow-up

**Our simulations.** The A–B binary integrated together with the A b candidate on the high-precision IAS15 integrator comes out fully regular (MEGNO 2.00), the binary's e ≈ 0.52 swing preserved and relative energy error below 10⁻¹⁰. The Proxima trio runs separately at MEGNO 2.08, all three planets calm, and the system's gated fictional moons additionally survived a 2,000-year Principia-equivalent integration. → [A/B viewer](https://vannadin.github.io/nearstars-db/phase4/orbit-viewers/alpha-centauri/interactive.html) · [Proxima viewer](https://vannadin.github.io/nearstars-db/phase4/orbit-viewers/proxima-cen/interactive.html)

## Luhman 16

**6.5 ly · L7.5 + T0.5 brown-dwarf binary**

The nearest brown dwarfs and the third-nearest system overall, discovered only in 2013. Two failed stars orbit each other across the L/T transition, one wrapped in patchy silicate clouds and the other in clearing weather cells. It is a destination unlike anything else in the roster.

## Barnard's Star

**6.0 ly · M4 red dwarf**

The fastest-moving star in the sky and the second-nearest system. It hosts four confirmed sub-Earth planets (b, c, d, e, from ESPRESSO radial-velocity detections), all packed inside Mercury's orbit around a quiet old red dwarf.

**Our simulations.** The innermost planet b, integrated long-term, comes out *stable and calm* at MEGNO 1.76, its semi-major axis constant to 8 significant digits. → [orbit viewer](https://vannadin.github.io/nearstars-db/phase4/orbit-viewers/barnards-star/interactive.html)

## Tau Ceti

**11.9 ly · G8.5 V**

The nearest single Sun-like star, a longtime SETI target and science-fiction staple. Radial-velocity analysis gives four super-Earth candidates (e, f, g, h), with e and f near the habitable-zone edges, alongside a debris disk more massive than the Kuiper belt.

**Our simulations.** All four planets run together stay regular (MEGNO 2.00), and the interesting part is what happens inside that stability: the planets visibly *exchange* eccentricity in slow secular cycles (g breathes between e ≈ 0.04 and 0.26) while every orbit stays bounded. It is a genuinely dynamic yet stable system. → [orbit viewer](https://vannadin.github.io/nearstars-db/phase4/orbit-viewers/tau-cet/interactive.html)

## 40 Eridani

**16.3 ly · K0.5 V + DA white dwarf + M4.5 flare star**

A hierarchical triple that puts three completely different suns in one system: a calm orange dwarf, the sky's most observable white dwarf, and a violently flaring red dwarf orbiting the pair. The primary's planets are:

- **40 Eridani A b (disputed)**, the published super-Earth, with the literature still debating whether the signal is stellar activity
- **40 Eridani A c (fiction)**, a Mercury-analog filler
- **40 Eridani A d (fiction)**, a temperate desert world; 40 Eri A is canonically Vulcan's sun, and this is our gated homage

**Our simulations.** This is the fiction gate in action. The two invented planets were integrated *together with* the real candidate before being accepted, and the result is fully regular (MEGNO 2.00), all three orbits stable, energy error below 10⁻¹⁰. → [orbit viewer](https://vannadin.github.io/nearstars-db/phase4/orbit-viewers/40-eridani/interactive.html)

## Fomalhaut

**25.1 ly · A4 V with the iconic debris ring**

The brightest star in the roster and the most photographed debris disk in astronomy, a vast eccentric dust ring 140 AU across. Flying a probe over that resolved, off-center ring around a blazing white star is the whole point of the system.

## TRAPPIST-1

**40.7 ly · M8 ultra-cool dwarf**

Seven Earth-sized planets in the longest known resonance chain, three of them in the habitable zone, make this the most scrutinized planetary system beyond our own (JWST observes it every cycle). The planets orbit in days around a star barely larger than Jupiter, and from planet e its neighbors appear larger than our Moon.

**Our simulations.** This is the hardest system in the roster: seven interacting planets in a resonance chain, integrated with the TRACE close-encounter integrator. The chain holds, with eccentricities never exceeding 0.013 and no orbit drifting. → [orbit viewer](https://vannadin.github.io/nearstars-db/phase4/orbit-viewers/trappist-1/interactive.html)

---

*Full per-body measurement and synthesis reports live in the [curation reports](https://vannadin.github.io/nearstars-db/reports.html). Every simulation input comes from the paper-cited database; see [Data & Methodology](data-and-methodology.md) for how that database is built.*
