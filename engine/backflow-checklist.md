# Backflow layer — checklist

`chain.yaml` draws methodology → methodology. It does not draw what happens *after* a
value ships: the shipped number becomes an input to a simulation, a constraint a future
recipe must reproduce, or the parent of another shipped number. Every recorded failure so
far lived in that unmapped layer. This layer maps it.

## Why

- `pause_nose` moved 23.5 → 35.33; `outer_compression` / `outer_extension` are functions
  of it and were never recomputed. Nothing could catch it — the relation was in nobody's
  file.
- `geopotential_j2 = 0.023` is not a conclusion. It is passed to the stability sim as
  `--j2 0.023` (`phase3/stability-sim/validation-manifest.yaml@«args: ["--j2", "0.023", "--j2-obliquity-deg", "5"]»`), and
  `STABILITY_REPORT.md@«### A b moons with J₂ — the oblateness reverses the moon-orbit choice»` records that the oblateness *reverses* the moon-orbit choice.
  Changing NMoI re-opens a 21 h run and the decision that came out of it.
- 40 Eri A c shipped at 0.38 R⊕. A future `mass_radius_relation` function must reproduce
  it; the standard Zeng curve gives ~0.41 at that mass. The conflict exists today and is
  invisible until the function is written.

## Three edge kinds this layer adds

| kind | meaning | example |
|---|---|---|
| `produced_by` | which chain node should emit this shipped field | `geopotential_j2` ← `body_figure` |
| `derived_from` | shipped field computed from another shipped field | `outer_compression` ← `pause_nose` |
| `consumed_by` | shipped field is an input to a run/artifact | `geopotential_j2` → α Cen moon sim (21 h) |

## Tasks

- [x] Count the surface: 7 boards, 245 decision rows, 969 fields, 158 distinct field names,
      32 axes. All 7 boards are `schema_version: 2` (an earlier claim that only α Cen was
      v2 is wrong).
- [x] Confirm the bundling problem is real and not machine-separable: ~116 of 969 field
      values pack more than one thing into one string, and a regex cannot tell
      "value + its evidence" from "outputs of four different nodes" because the
      parenthetical mixes both freely.
- [x] `engine/bindings.yaml` — 158 field names → `produced_by` / `derived_from` /
      `bundled` / `kind`. → verify: every field name present, every `produced_by` names a
      real chain node, zero silent unmapped.
- [x] `consumers:` block — runs that eat shipped values, with their cost.
      → verify: every `consumes` entry is a real field name; sim args in
      `validation-manifest.yaml` are all accounted for.
- [x] `engine/backflow.py` — `check` and `impact <node>`.
      → verify: `impact body_figure` reproduces the J₂ story end to end (rows, bundles,
      the 21 h run, the docs).
- [x] Anchor the known failure as a test. → verify: a test asserts `pause_nose` has
      dependents, so the Proxima case cannot silently recur.
- [x] Wire into `scripts/check.sh`. → verify: `check.sh` fails when a binding names a
      node that no longer exists.

## Out of scope

- Splitting the ~116 bundled fields. This layer *prioritises* that work — a bundle only
  needs splitting when a recipe actually reaches it — but does not do it.
- Deciding A/B/C/D sequencing. This layer is what makes any of them safe, not a
  substitute for the choice.

## What it found on the first run

- **19 fields no node produces.** The graph's real holes, now listed instead of assumed:
  seven stellar appearance/activity fields (`activity`, `flares`, `spots_faculae`,
  `granulation`, `limb_darkening`, `corona`, `flare_colour`) because `star_physical`
  stops at [mass, radius, teff, luminosity, sed, v_sin_i]; `color` and `ring_color`,
  which *have* methodology docs but no node; plus `aurora`, `terrain`, `specular`,
  `cloud_coverage`, `banding_morphology`, `habitable_zone`, `neutral_torus_supply`,
  `co_orbitals`, `satellite_count`, `biosphere`.
- **A triple alias at the accident site.** `magnetosphere`, `magnetopause_standoff_rp`
  and `pause_nose` are three names for the same R_mp (α Cen A b: 35.33 in all three).
  Three names for one value, updated by hand, is how the Proxima update missed two of
  its dependants.
- **An undeclared derived-value cycle**, `pause_smooth ↔ pause_radius_smoothed`. Reading
  the doc showed it is a genuine fixed point (`planetary-magnetosphere-geometry-methodology.md@«`pause_smooth` = 0.5 × `pause_radius` is solved as a fixed point»`), so the
  check now follows `chain.py`'s rule: cycles are allowed, *undeclared* cycles are not,
  and a declaration needs a citation. The doc names the partner inconsistently
  (`pause_radius` vs `pause_radius_smoothed`); recorded, to settle when the recipe is written.
- **`pause_nose` has 12 dependants over 46 rows.** Two of them are the ones that were
  missed. `backflow.py after pause_nose` now prints them.

## Next

- [ ] Resolve the `magnetosphere` / `magnetopause_standoff_rp` / `pause_nose` alias.
      Three shipped names for one quantity is a standing defect, not a naming preference.
- [ ] Give the 19 unmapped fields either a node or an explicit `kind`. Two of them
      (`color`, `ring_color`) have docs already and are the cheapest.
