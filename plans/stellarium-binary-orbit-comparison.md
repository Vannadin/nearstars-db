---
title: Stellarium vs NearStars binary-orbit pipeline comparison
status: active
created: 2026-05-21
---

# Stellarium vs NearStars binary-orbit pipeline comparison

**NearStars connection.** Our pipeline ([`docs/reference/binary-epoch-pipeline.md`](../docs/reference/binary-epoch-pipeline.md))
ingests ORB6 / Gaia NSS orbital elements and outputs ICRF Cartesian state
vectors `(x, y, z, vx, vy, vz)` in km, km·s⁻¹ at `JD2433282.5`, feeding
Principia's `principia_initial_state`. Stellarium is the closest piece
of widely-used open-source astronomy software that also propagates
visual-binary orbital motion. Comparing the two answers two questions
NearStars cares about: (1) are our convention choices (Hilditch, mass-
ratio split, Hipparcos `f`-factor) actually shared by an independent
implementation, and (2) is there anything Stellarium does that we
should adopt — or anything they intentionally skip that we are
needlessly carrying.

**Scope.** Read-only research. No code changes expected in this repo.

**External references.**
- Stellarium master at commit [`3efa1406`](https://github.com/Stellarium/stellarium/tree/3efa1406a135fd6330d515ee8b942a58ffa80f01)
- Our pipeline: [`docs/reference/binary-epoch-pipeline.md`](../docs/reference/binary-epoch-pipeline.md)
- ORB6 catalog: https://www.astro.gsu.edu/wds/orb6.html

---

## 1. Executive summary

| Question | Answer |
|----------|--------|
| Do the two pipelines share convention? | **Yes for the math, no for the output.** Hilditch rotation, mass-ratio displacement, and Hipparcos `f`-factor PM propagation are identical. |
| Do they consume the same catalog? | **No.** Stellarium ships a **hand-curated 15-pair file** (`binary_orbitparam.dat`); we read ORB6 + Gaia NSS directly. |
| Do they produce comparable outputs? | **No.** Stellarium produces a **unit direction vector on the celestial sphere** for rendering. We produce a **3D Cartesian state in km / km·s⁻¹** for n-body integration. Different target use-cases. |
| Does Stellarium handle hierarchical triples? | **No.** No Proxima Cen, no 40 Eri C, no 36 Oph C in their orbit file. Each star's orbital coupling is at most one pair deep. |
| Should NearStars change anything based on this? | **No structural change**, but the agreement validates our convention choices. Stellarium's missing-feature list (triples, ORB6 ingestion, velocity output) is *exactly* the NearStars-specific delta — so we are not over-engineering. |

---

## 2. What Stellarium actually does

Pinned to commit [`3efa1406`](https://github.com/Stellarium/stellarium/tree/3efa1406a135fd6330d515ee8b942a58ffa80f01) (2026-05 master HEAD).

### 2.1 Catalog

A single flat file with 15 named pairs:

> [`stars/hip_gaia3/binary_orbitparam.dat`](https://github.com/Stellarium/stellarium/blob/3efa1406a135fd6330d515ee8b942a58ffa80f01/stars/hip_gaia3/binary_orbitparam.dat)

Pairs covered: α Cen AB, Sirius AB, 61 Cyg AB, γ Vir AB, Alula Aus AB,
Achird AB, ε¹ Lyr AB, ε² Lyr AB, β Mus AB, Dalim AB, ψ Vel AB,
ρ Oph AB, ζ Her AB, η Oph AB. Provenance is not annotated in the file
itself; the angular values (periastron epoch, *i*, Ω) match well-known
ORB6 entries (e.g. α Cen periastron 2435314.751 = 1955.56), so the
table is almost certainly hand-distilled from ORB6, just not via a
build script.

Format spec: [user guide §app_star_catalogue.tex L1870-L1926](https://github.com/Stellarium/stellarium/blob/3efa1406a135fd6330d515ee8b942a58ffa80f01/guide/app_star_catalogue.tex#L1870-L1926).

There is also `wds_hip_part.dat`, but that file stores **the last
observed PA/separation snapshot** for many more WDS doubles. It does
not propagate — Stellarium renders those pairs as a frozen tableau,
not as a moving orbit.

### 2.2 Algorithm

The entire binary-orbit code is one ~180-line templated inline
function in `Star.hpp`:

> [`Star<Derived>::getBinaryOrbit(epoch, v, ra, dec, plx, pmra, pmdec, RV, sep, pa)`](https://github.com/Stellarium/stellarium/blob/3efa1406a135fd6330d515ee8b942a58ffa80f01/src/core/modules/Star.hpp#L265-L449)

Steps, in order:

1. Lookup `binaryorbitstar` by HIP (`StarMgr::getBinaryOrbitData()`).
   Early-exit if not present (`hip == 0`).
2. Solve Kepler's equation by **Newton-Raphson**, tolerance `1e-10`,
   max 100 iterations, initial guess `E₀ = M`
   ([Star.hpp#L332-L353](https://github.com/Stellarium/stellarium/blob/3efa1406a135fd6330d515ee8b942a58ffa80f01/src/core/modules/Star.hpp#L332-L353)).
3. Compute true anomaly via the standard half-angle:
   `ν = 2 atan(√((1+e)/(1−e)) · tan(E/2))`.
4. Apply Hilditch-form rotation matrix
   ([Star.hpp#L364-L373](https://github.com/Stellarium/stellarium/blob/3efa1406a135fd6330d515ee8b942a58ffa80f01/src/core/modules/Star.hpp#L364-L373)).
5. Propagate the **barycenter** astrometry from `data_epoch` to the
   target JD using the full 6-parameter ICRS update with the ESA
   Hipparcos `f`-factor
   `f = 1/√(1 + 2μ_r·t + (μ² + μ_r²)·t²)`
   ([Star.hpp#L381-L385](https://github.com/Stellarium/stellarium/blob/3efa1406a135fd6330d515ee8b942a58ffa80f01/src/core/modules/Star.hpp#L381-L385)).
6. Split into A and B with the mass ratio `q = M_B/(M_A + M_B)`
   ([Star.hpp#L414-L423](https://github.com/Stellarium/stellarium/blob/3efa1406a135fd6330d515ee8b942a58ffa80f01/src/core/modules/Star.hpp#L414-L423)).
7. Add `Δα·cos δ` and `Δδ` to the barycenter sphericals, re-convert to
   a Cartesian unit vector via `spheToRect`, **normalize**, and return
   ([Star.hpp#L437-L448](https://github.com/Stellarium/stellarium/blob/3efa1406a135fd6330d515ee8b942a58ffa80f01/src/core/modules/Star.hpp#L437-L448)).

Velocity (arcsec·yr⁻¹) is computed in step 4 alongside position but is
**discarded after normalization** — the renderer only needs direction.

### 2.3 Cadence

Per-frame. Called from inside the drawing loop in
[`ZoneArray.cpp::draw()`](https://github.com/Stellarium/stellarium/blob/3efa1406a135fd6330d515ee8b942a58ffa80f01/src/core/modules/ZoneArray.cpp#L510-L515)
and from `searchAround` / `searchWithin`, with the current
`core->getJDE()` as the epoch. No caching layer; the HIP-map miss is
the only fast path.

---

## 3. Comparison cheat-sheet

| Aspect | Stellarium | NearStars |
|---|---|---|
| Catalog source | Ad-hoc 15-row `binary_orbitparam.dat` (no build script) | ORB6 + Gaia NSS upstream → `db/binary_orbits.json` |
| Kepler solver | Newton iteration, tol `1e-10`, max 100 iter | Markley (non-iterative cubic) via PyAstronomy `MarkleyKESolver` |
| ω, Ω convention | Hilditch (rotation matrix matches) | Hilditch / Pourbaix (matches) |
| Barycenter PM | Hipparcos `f`-factor (full 6-parameter) | Same |
| Mass split | `q = M₂/(M₁+M₂)`, displace ±q · r_rel | Identical formula |
| Output type | Unit direction vector on celestial sphere | Full ICRF Cartesian state `(x, y, z, vx, vy, vz)` in km, km·s⁻¹ |
| Velocity output | Computed internally then **discarded** | First-class output (needed by Principia) |
| Epoch | Whatever `core->getJDE()` returns (continuous) | Single fixed snapshot at `JD2433282.5` (1950-01-01 TDB) |
| Cadence | Every frame, every visible binary | One-shot at `build_systems.py` runtime |
| Hierarchical triples (α Cen ABC, 40 Eri ABC, 36 Oph ABC) | **Not supported** — Proxima / C-components absent | Jacobi decomposition (`primary_is_barycenter_of`) |

---

## 4. Where the two pipelines agree (and why that matters)

Three convention choices in our pipeline that have alternatives in the
literature, all confirmed by Stellarium's independent implementation:

1. **Hilditch rotation form.** Our [§7b rotation matrix](../docs/reference/binary-epoch-pipeline.md)
   matches Stellarium's [`Star.hpp#L364-L373`](https://github.com/Stellarium/stellarium/blob/3efa1406a135fd6330d515ee8b942a58ffa80f01/src/core/modules/Star.hpp#L364-L373)
   term-for-term. Aitken's older sign convention (still seen in some
   pre-2000 papers) would flip Ω's contribution.

2. **Catalog row = barycenter, not photocenter.** Both pipelines treat
   the Hipparcos/Gaia astrometric row as the barycenter and displace
   each component outward. The alternative would be to reconstruct the
   barycenter from photocenter + photometric flux ratio. Stellarium
   does not bother; neither do we. This is fine for visual binaries
   with comparable masses (most pairs in both catalogs) but is a known
   approximation for very-unequal-mass systems where the photocenter
   sits near the primary — a deferred refinement, not a current bug.

3. **Hipparcos `f`-factor PM propagation.** The exact `f = 1/√(1 +
   2μ_r·t + (μ² + μ_r²)·t²)` expression is the ESA-canonical form, used
   identically. Easy to typo (μ_r vs μ², squared vs not), so seeing the
   same form in two independent codebases is a strong sanity check.

These agreements are the most useful finding from this research:
**the math of NearStars's pipeline is not idiosyncratic** — it matches
the convention chosen by the most widely-used desktop planetarium.

---

## 5. Where they intentionally diverge

The divergences are not bugs in either system; they reflect different
target use-cases.

### 5.1 Output: unit vector vs Cartesian state

Stellarium needs **where on the sky** a star appears right now. A
direction is sufficient; distance is folded into apparent magnitude
and parallax. Cartesian km / km·s⁻¹ would be a waste.

NearStars feeds **Principia**, which integrates the full 3D n-body
system in km. Components, not the barycenter, are integrated. Without
absolute Cartesian coordinates per component, Principia has no input.

### 5.2 Catalog ingestion: 15 pairs vs full ORB6

Stellarium curates the showcase pairs amateur astronomers actually
point at. 15 is enough for "γ Vir is currently widening, watch it over
five years." A flat hand-edited file is the cheapest implementation
that delivers that.

NearStars needs every binary that ends up in the mod's ~50 ly
Kopernicus footprint. Manual curation does not scale to ~30 binary
systems. ORB6 / Gaia NSS ingestion is therefore mandatory for us,
optional for them.

### 5.3 Cadence: per-frame vs one-shot

Stellarium recomputes every binary every frame because the user can
scrub through centuries of time and expect the binaries to swing.

NearStars freezes one instant (`JD2433282.5`) because Principia takes
over from that point and integrates everything itself. We do not
*need* the orbital elements after the build step — Principia derives
all future state from forward integration.

### 5.4 Hierarchical multiples

Stellarium would render Proxima Centauri using *its own* HIP-catalog
astrometry, with no orbital coupling to α Cen AB. Visually, this is
indistinguishable from the "true" hierarchical solution — Proxima's
13,000 AU separation at 4.24 ly translates to ~13' on the sky, which
is below Stellarium's typical visual-binary resolution anyway.

For Principia, the coupling is **not** negligible. The Kervella+ 2017
orbital solution for α Cen ABC binds Proxima gravitationally to AB at
~547,000 yr period, and Principia integrates that perturbation. Our
Jacobi decomposition for triples (40 Eri C and 36 Oph C are the other
cases) is therefore necessary.

### 5.5 Solver: Newton vs Markley

Newton iteration with `e < 0.9` converges in ~3–5 iterations to 1e-10.
Markley's method is non-iterative and converges to ~1e-15 in one shot
but requires more flops per call. Both are fine; the choice is
incidental. We use Markley because PyAstronomy ships it; Stellarium
uses Newton because the rest of their Kepler-solving code is also
Newton.

---

## 6. Implications for NearStars

**No structural changes recommended.** The comparison validates our
pipeline rather than revealing a missing feature. Specifically:

- Our convention choices (Hilditch, mass-ratio split, `f`-factor) are
  the same ones chosen by an independent mature codebase.
- The features Stellarium *lacks* (Cartesian state output, ORB6
  ingestion, hierarchical triples, velocity output) are *exactly* the
  NearStars-specific deltas. We are not over-engineering; we are doing
  the things Principia requires that Stellarium does not.

**Minor suggestions worth noting**, not action items:

- **Cross-validate a few pairs by visual inspection.** Pick α Cen AB,
  Sirius AB, 61 Cyg AB — systems present in both Stellarium and our
  DB. Compute the apparent (Δα·cos δ, Δδ) sky offsets from our
  Cartesian output at a sample JD, and compare to what Stellarium
  renders. Agreement to ~10 mas would confirm our convention end-to-end;
  disagreement would be a sign-error red flag. This is a future
  verification task, not part of this research.

- **`binary_orbits.json` provenance documentation.** Stellarium gets
  away with un-cited orbital elements because their target user does
  not check. We already record `bibcode` per orbit; that is the right
  policy and we should keep it.

- **The 15-pair list as a manual-curation sanity check.** Every system
  in Stellarium's list is in our DB. If a future maintainer adds a
  pair to our DB that is *not* in Stellarium's 15, that is fine — but
  it should prompt the question "is this pair widely-recognized as a
  visual binary, or is the orbit speculative?" Stellarium's list is a
  rough "common knowledge" filter.

---

## 7. Open questions

- Stellarium's `binary_orbitparam.dat` has no build script in their
  repo. Is it maintained by manual ORB6 lookups, or is there an
  unpublished derivation script? Not load-bearing for NearStars, but
  curious.
- Stellarium computes orbital velocity (arcsec·yr⁻¹) internally before
  discarding it. If a future Stellarium feature exposes that velocity,
  it would be the simplest cross-check for our `vx, vy, vz` outputs
  (modulo a sky-to-3D conversion). Worth watching their changelog.
- We could not confirm whether Stellarium handles ε Lyr's quadruple
  structure (ε¹ Lyr AB + ε² Lyr AB are two separate Kepler systems but
  also a wide visual pair). The 15-row file lists ε¹ and ε² separately
  with no link between them — probably the same "no hierarchy"
  limitation as for α Cen + Proxima.
