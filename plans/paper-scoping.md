<!-- NearStars paper-scoping note (exploration phase) — honest claim/have/gap tally across the four pillars -->
# NearStars paper — scoping note (exploration phase)

**Status:** ⏸ **PARKED (2026-06-18).** Owner decision — the only active action at this stage is "write context-notes more diligently going forward." The paper effort keeps an exploration record only, no active work. This document is the starting point if it ever resumes.
This note is an exploration record that honestly tallies "what becomes a paper and what does not."
**Written:** 2026-06-18
**Owner intent:** turn the whole project arc into a paper. Interested in all four angles — reproducible pipeline (method) · multiple-system epoch propagation · uniform stability re-verification · external-observer benchmark.

---

## 0. The big premise (nail this down first)

Most NearStars values are a **re-curation / re-derivation of existing published measurements**. There are no new observations, so "a new astronomical discovery about a star/planet" cannot be claimed. Any novelty must live on the **method · synthesis · reproducibility · education** axes.

Two traps.
- **License**: the project is CC-BY-NC-SA 4.0. NC is not OSI-approved and conflicts with the licensing requirements of some open-science venues such as JOSS. A real obstacle on the software-paper track.
- **Measurement vs synthesis separation**: Phase 3 synthesis / art direction is not measurement. Mixing them in a paper would be over-claiming. It must be described cleanly as an "art-direction layer stacked on top of a measurement gate."

## 1. Real-world scale (numbers that go in the paper body)

- **157** system files (multiple systems use the one-file-per-component layout)
- **227** planets
- **27** files carrying a `binary_orbit` node (a count showing the multiplicity handling is real)
- **1314** field stars in the within-50-ly layer (SIMBAD spine + Gaia color)
- **13** systems with stability-simulation results
- **78** Phase 3 web reports
- 1 external-observer benchmark document (13 KB, complete)
- Provenance cache: `docs/phase3/_papers`

> Note: a direct arXiv-id search caught only 24 entries, but bibcode citations are tracked separately, so the actual provenance coverage is likely higher. To turn this into a paper, the **"fraction of all values with a pinned source" must be computed precisely** (a provenance-coverage metric).

## 2. The four pillars — claim / have / gap

### Pillar 1. Reproducible pipeline (method) — *the center of the paper*
- **Claim**: a provenance-tracked end-to-end pipeline. Measurements (arXiv/bibcode-pinned curation) → strictly-derived layer (unit conversion + priority merge only, no default-value assumptions, nulls preserved) → Phase 3 synthesis (documented divergence) → deterministic cfg emit. Reproducibility is enforced by the 6 check.sh gates + canonical JSON.
- **Have**: the data-contract SPEC, check.sh, the single `_naming` module, the build_systems strictly-derived invariant, 157 systems / 227 planets.
- **Gap**: (a) one architecture diagram. (b) a "rebuild DB→cfg with one command" reproducibility claim + measurement. (c) provenance-coverage quantification. (d) a comparison table against prior ad-hoc approaches.

### Pillar 2. Multiple-system epoch propagation — *the differentiator*
- **Claim**: hierarchical multi-body astrometric propagation Kepler→Thiele-Innes→ICRS + epoch handling. The part REX and Stellarium do not handle properly (= NS's reason to exist).
- **Have**: the `binary-epoch-pipeline.md` reference, 27 systems with binary_orbit, α Cen and Sirius worked examples, 2 comparison documents (REX, Stellarium).
- **Gap**: a **verification figure** — compare α Cen's predicted separation–PA against orb6 ephemeris on a time axis, quantifying the error. Right now there is only a "we do this" narrative, no "it's correct" figure.

### Pillar 3. Uniform stability re-verification — *validation result A*
- **Claim**: re-verify compact multi-planet systems under a single policy with REBOUND (WHFast+MEGNO screen → TRACE/IAS15). A 3-axis verdict (survival / chaos / eccentricity grade). Plus a Msini→true-mass boundary scan to derive dynamical mass and inclination constraints (Barnard as the leading case).
- **Have**: 13 systems run, STABILITY_REPORT, the α Cen boundary scan, energy/MEGNO sanity, TRAPPIST-1 cross-check against Agol+2021.
- **Gap**: a **Barnard 4-planet re-run + inclination boundary scan** (the current summary is a stale copy holding only planet b — pre-F1-recovery). A uniform table across all multi-planet systems. Comparison against each system's published stability claim.

### Pillar 4. External-observer benchmark — *validation result B*
- **Claim**: a calibration of what a 10 pc observer can and cannot infer about Solar System bodies using the same Phase 2/3 method. Reliability grade ↔ observability mapped 1:1. Killer result: the Venus greenhouse blind spot (Teq 227–299 K vs actual 737 K).
- **Have**: 1 completed document (13 KB, 2026-06-03).
- **Gap**: reframe as a methods-validation section. (Optional) extend by one body class.

## 3. Recommended form

**A single methodology paper (astro-ph.IM)** is the most natural bundling.
- Pillar 1 = the method body
- Pillar 2 = the differentiator (why existing tools fail)
- Pillars 3 · 4 = the two validation results
- Secure a DOI first via an arXiv preprint → later promote to a formal IM review, or split into RNAAS short notes.
- **RNAAS fallback**: just one of pillar 3 or 4 in ~1000 words. Best for a first "we published a paper" experience.

## 4. Cheapest next step (gains for both exploration and project)

Finish the **Barnard 4-planet re-verification + inclination (→ true-mass) boundary scan**.
- Produces one concrete result + fills the stability pillar's biggest gap + tests whether a "uniform stability survey" can stand as a pillar.
- Byproduct: keep recording method, decisions, and rationale in the stability-sim `context-notes.md` (practicing the method-recording discipline flagged earlier).

## 5. Open questions

- Author lineup? Whether to include Schultz (Principia) and Firefly contributors.
- Whether to set a provenance-coverage target (e.g. ≥95% of measurements with a pinned source) as a gate.
- License: whether to split the code portion under an OSI license for the paper-companion code release (DB/art stay CC-BY-NC-SA).

## Related
- [stability-sim STABILITY_REPORT](../phase3/stability-sim/STABILITY_REPORT.md)
- [external observer benchmark](../docs/reference/solar-system-external-observer.md)
- [REX comparison](../docs/reference/rex-data-comparison.md) · [Stellarium comparison](stellarium-binary-orbit-comparison.md)
