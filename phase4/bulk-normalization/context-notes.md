# Bulk-row normalization — context notes

## Why (2026-07-12)

Owner: the bulk grouping criteria differ per moon and the axis sets differ per
body — confusing. Root cause confirmed in git history: the moon bulk rows were
bundled on 2026-06-19 (pre-skill era; un-chosen elements got lumped per body
with whatever fields were at hand), while A b and the star rows were walked
axis-by-axis post-skill (2026-07-10+). Two generations coexist on one board.

## Owner decisions

1. **Class-based 3 templates** (not one universal fieldset).
   - Core (all classes): mass, radius, gravity, rotation_period,
     spin_axis_orientation, geopotential_j2 + reference_radius, age.
   - star: core (cooling_age satisfies the age slot for WDs).
   - tidally_locked: core + obliquity (≈0 confirm) + geopotential_c22 +
     internal_heat (+ tidal_heating for Io-types, optional).
   - free_rotator: core + obliquity (real choice) + internal_heat; c22 absent
     physically → `value: null` + `na_reason`.
2. **gravity kept** despite being derived — it maps straight onto the
   Kopernicus geeASL slot. Guard: must equal GM/R² (validator warns on drift).
3. **n/a representation**: field always present, `value: null` + `na_reason`
   string. Machine-distinguishable from an accidental omission.

## Design choices made while implementing

- **Union rule instead of pointer duplication.** A template field is satisfied
  either by an entry in the body's bulk group row or by a live dedicated
  `bulk.<name>` row (the post-skill style: J2, spin-axis, heavy-narrative
  decisions). No value duplication in the group row → no drift risk; the
  per-body HTML page already renders them adjacent.
- **`body_class` key** (star | tidally_locked | free_rotator) added on bulk
  group rows so the validator can pick the right template mechanically.
- **Anchor-row requirement**: every real body (not `*`) with any live row must
  carry exactly one live bulk group row. This is what surfaces αCen A/B, which
  had only dedicated J2/spin rows and no bulk anchor at all.
- internal_heat slot is satisfied by `internal_heat` OR `intrinsic_luminosity`
  (SPEC treats them as alternates for self-luminous bodies); age slot by `age`
  OR `cooling_age`.
- Chaos gaps filled from its own existing decisions, no new owner input:
  internal_heat = negligible (narrative already said so → na_reason),
  spin_axis = orbit normal + the already-gated 15° obliquity, azimuth handled
  by the synthetic-orbit-noise de-perfect-at-emit policy.
- All five αCen moons had J2 without reference_radius — filled with their
  radius values (J2 emit policy requires the pair).

## Mid-run design revision: severity split (2026-07-12)

Rolling the template onto proxima/40 eri surfaced slots that are **genuinely
undecided physics** (Proxima c obliquity/spin axis, planet J2/C22/internal_heat
not yet figure-walked). The owner has said planets get their own one-by-one
Phase 4 walks later — inventing those values here would pre-empt that. So the
validator's severity was split: template *structure* (anchor row, body_class,
value-less field without na_reason) stays a hard error; template *coverage*
(a slot not yet walked) is a warning. The warning list IS the forgotten-vs-
omitted detector, and it doubles as the work-list for the future planet walks.

Left open by design (12 warnings): Proxima b internal_heat; Proxima c
obliquity/spin_axis/J2/internal_heat; Proxima c I J2/C22/internal_heat;
Proxima d J2/C22/internal_heat; 40 Eri A d J2.

Filled during normalization only where a decision already existed somewhere:
tidal-lock trivial consequences (rotation = orbital period, spin = orbit
normal — blessed by the skill's silent-passthrough rules), figure values
already worked in body-figure-methodology §6 (Proxima b J2 2.8e-5 / C22 8e-6),
narrative-only values promoted to typed fields (40 Eri c C22 9.6e-8 + J2 =
10/3·C22; Erid gravity 2.09 g / rotation 5.1 h / internal_heat active;
40 Eri d gravity 0.2 g / spin axis), coeval age echoes (40 Eri 1.8 Gyr), and
GM/R² gravity echoes everywhere.

40 Eri B's statistical rotation (35 h) went into the dedicated
bulk.geopotential_j2 row, not the passthrough anchor — provenance: the anchor
echoes measurements, and the 35 h adoption is a documented-divergence decision
that lives with the J2 gate. Union rule covers the slot either way.

Agent outcome: the 3-single-star-board agent delivered clean minimal diffs
(gravity values re-verified by hand). The proxima+40eri agent stalled with
zero file changes; its boards were finished inline instead.
