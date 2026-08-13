<!-- 모드 개요 — 무엇을 만드는 모드이고 v1 로스터가 무엇인지 -->
# NearStars

Sometime deep into a career save, with reusable rockets flying and the tech tree nearly bare, you point a probe not at another planet but at a *star*, and spend years of mission time coasting toward it. NearStars exists to make that arrival worth the wait. You leave a fully realistic Sol system behind and reach a real stellar neighbor, and every world waiting there is built from what astronomers have actually measured.

It is a mod for **Kerbal Space Program 1.12.x**. It sits on top of a Real Solar System install (through [Sol-Configs](https://github.com/RSS-Reborn/Sol-Configs)) and fills in the real solar neighborhood out to about 50 light-years: Alpha Centauri, Barnard's Star, Tau Ceti, TRAPPIST-1, and more.

Flying to nearby stars in KSP is not a new idea. What sets NearStars apart is that it refuses to make anything up. Every star's temperature and color, every planet's orbit and mass, every debris ring carries a citation to the paper or catalog it came from. Where a value simply has not been measured, such as the color of a surface no telescope has resolved or the air of a planet seen only as a dot, the mod does not guess quietly. It works out a defensible answer decision by decision, writes down which papers constrain it, and marks the confidence. The few worlds invented outright for gameplay variety are held to the same honesty: each is checked against the physics, flagged as fiction, and never slipped in among the real detections.

That discipline pays off most in the systems other packs tend to simplify. Multiple-star systems here actually behave like multiple-star systems. Alpha Centauri's A and B swing through their real 80-year orbit, and the whole roster is validated with long-term n-body simulations so it stays stable under Principia's gravity rather than merely looking right at a glance.

> **Status: in development, no release yet.** The data engine (this repository) has reached its curated-database milestone, and final KSP config generation is deliberately saved for last. Watch this repo for release news.

## The v1 roster

The mod itself will ship a focused set of seven systems, drawn from a much larger research database and chosen for their proximity, their planets, and their sheer variety, so that no two destinations feel the same:

| System | Distance | What's there |
|---|---|---|
| [Alpha Centauri](star-systems.md#alpha-centauri) | 4.4 ly | G+K binary + Proxima with 3 planets |
| [Luhman 16](star-systems.md#luhman-16) | 6.5 ly | nearest brown-dwarf binary |
| [Barnard's Star](star-systems.md#barnards-star) | 6.0 ly | 4 sub-Earths |
| [Tau Ceti](star-systems.md#tau-ceti) | 11.9 ly | Sun-like star, 4 super-Earths |
| [40 Eridani](star-systems.md#40-eridani) | 16.3 ly | K dwarf + white dwarf + flare star triple |
| [Fomalhaut](star-systems.md#fomalhaut) | 25.1 ly | A-type star with the iconic debris ring |
| [TRAPPIST-1](star-systems.md#trappist-1) | 40.7 ly | 7 Earth-sized planets in a resonance chain |

Behind those seven sits the full research database, **145 systems and 157 stellar components**, which you can browse right now in the [live viewer](https://vannadin.github.io/nearstars-db/).

## Where to go next

If you are new here, [Star Systems](star-systems.md) is the tour of what you will fly to, and [Data & Methodology](data-and-methodology.md) explains how it is all built and checked. From there:

- **[Methodology Library](../reference/methodology-index.md)** collects the papers behind each derived value
- **[Showcase](showcase.md)** walks through a few results we are proud of, including one honest failure
- **[Viewers Gallery](viewers.md)** puts every map and report in your browser
- **[Installation & Compatibility](installation.md)** and the **[FAQ](faq.md)** cover the practical questions
