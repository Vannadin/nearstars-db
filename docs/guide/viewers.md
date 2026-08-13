<!-- 브라우저에서 바로 열리는 뷰어·보고서 목록 -->
# Viewers Gallery

You do not have to wait for a release to see the project. Everything it produces is browsable in your browser today, and all of it is static HTML generated straight from the database, so what you are looking at is exactly what the mod will be built from. Here is what is worth opening, roughly from the widest view down to the paper trail.

## [3D star map](https://vannadin.github.io/nearstars-db/starmap.html)

The whole research database laid out in space: every curated system within ~50 ly, positioned from Gaia astrometry. Click a system to drop into an AU-scale view with planet orbits (the Solar System is included for scale). You can toggle heliospheres (per-star astrosphere bubbles), interstellar wind vectors, stellar spin axes (measured versus assumed), space velocities, and a background layer of all ~1,300 field stars within 50 ly. A Korean/English toggle is built in.

## [Database viewer](https://vannadin.github.io/nearstars-db/)

The tabular front-end: every system, star, and planet with its measurements, provenance, and derived values, all filterable and sortable. This is the actual `db/systems/` content rendered, not a summary of it.

## [Orbit viewers](https://vannadin.github.io/nearstars-db/phase4/orbit-viewers/)

Interactive 3D (Plotly) renders of our N-body simulation output for the six planetary systems of the roster. Rotate, zoom, and inspect the very orbits the stability runs produced; the [Star Systems](star-systems.md) page has the per-system results that go with them.

## [Radiation-belt viewer](https://vannadin.github.io/nearstars-db/belt-viewer.html)

Kerbalism's radiation fields, computed live: the exact in-game signed-distance-field
model with a slider for every cfg parameter, presets for all seven magnetized
solar-system bodies (shipped stock cfg vs our physics-fitted version, side by side)
plus the NearStars bodies, a 3D volume-raymarched mode, and a one-click export of the
current shape as a Kerbalism cfg block. The [Radiation Belts](../reference/solar-system-radiation-belts.md) page
has the physics behind every preset.

## [Curation reports](https://vannadin.github.io/nearstars-db/reports.html)

The paper trail. Phase 2 reports give every measurement with its source paper, and Phase 3 reports give every in-game decision with its basis, its confidence, and, wherever the mod diverges from the canonical reading, a documented alternatives section. Each report has an English/Korean toggle.

## [Phase 4 boards](https://vannadin.github.io/nearstars-db/phase4/)

The art-direction layer: per-body boards where the owner's final in-game choices are frozen, each one gated against the Phase 2/3 evidence window.

## [Reference library (rendered)](https://vannadin.github.io/nearstars-db/wiki/)

HTML renders of the repository's internal reference and planning documents, the same files the [Methodology Library](../reference/methodology-index.md) indexes, plus the research notes behind them.
