# Field-standard findings — the full inventory, all seven boards

α Cen is the board being fixed. This file is why: everything found anywhere is recorded
here so that finishing α Cen produces a standard, not a one-off cleanup. Each item says
whether α Cen carries it, because those are the ones the standard gets tested against.

Measured 2026-08-24/25 across all 7 boards: 245 decision rows, 969 fields, 158 distinct
field names, 32 axes, all `schema_version: 2`.
α Cen alone: 82 rows, 364 fields, **130 of the 158 names (82 %)**, 16 of the 19 unmapped
fields, and all 4 bundled kinds — which is why fixing it here covers most of the surface.

---

## A. The enforcement hole (fixed 2026-08-25, `92041e6e`)

**A1. `fields[].name` was never validated.** `AXIS_NAMES` only checked the suffix of the
`axis:` key. Injecting `ZZZ_totally_bogus_name` into a board passed with 0 errors.
This is the root cause of everything in section B.

**A2. Widening the menu was how drift became legal.** `base_colour` and `base_color` were
both listed in `AXIS_NAMES`, so nothing complained — even though the duplicate was written
down in three places (`_audit/consistency-audit-FINDINGS.md:269` "named 4 ways",
`emit-hardening/checklist.md:49` "a spelling duplicate", `field_alignment.yaml` "normalize
on next board touch").

Now: names check against `engine/bindings.yaml`, off-menu axis names fail instead of warn,
and `check_menu_variants` rejects a spelling variant being admitted to the menu at all.

---

## B. Naming (α Cen: partly)

| | finding | α Cen? |
|---|---|---|
| B1 | `base_colour` vs `base_color` — both shipped | **yes** (Pandora, Cassandra) — fixed |
| B2 | 36 of 158 names occur exactly once; likely off-standard coinages | partly |
| B3 | **Triple alias for R_mp**: `magnetosphere`, `magnetopause_standoff_rp`, `pause_nose` are three names for one quantity (A b: 35.33 in all three) | **yes** |
| B4 | `colour` and `ring_colour` were registered but never used | menu only — removed |

B3 is the standing defect: three hand-updated names for one value is the mechanism that
let the Proxima `pause_nose` update miss two of its dependants.

---

## C. Units (α Cen: yes)

The boards do follow a per-body-class convention. It is simply not written down, and
`field_alignment.yaml` declares only two classes (`star`, `planet`) where the boards use
three.

```
star    M_sun · R_sun · reference_radius in m
planet  M_earth · R_jup · km
moon    kg · km                          <- no class for this in the contract
```

| | finding | α Cen? |
|---|---|---|
| C1 | `reference_radius` in `m` (stars) vs `km` (everything else) — same quantity, factor 1000 | **yes** |
| C2 | `mass` in kg for moons, `radius` in km for moons and `R_jup` for A b — none declared in `field_alignment.yaml` | **yes** |
| C3 | `pressure` in `atm` (Pandora) vs `bar` (A b, Cassandra) — the one genuinely arbitrary split | **yes** |
| C4 | `gravity` in `g` (40 Eri) vs `m/s²` (everyone else); `field_alignment.yaml:60` specifies m/s², so 40 Eri violates the contract | no — **deferred, changes shipped numbers and the notes quote them** |
| C5 | 44 % of numeric fields carry no `unit`. Most are correctly dimensionless (`geopotential_j2`, `flattening`, `albedo`, `eccentricity`, `hapke_*`, `pause_compression`); the standard should say so explicitly rather than leave it inferred | **yes** |

Not defects, recorded so they are not "fixed" by mistake: `R_p` / `R_moon` / `R_bd` /
`R_d` are body-relative radii and correctly differ by body; `rotation_period` in days for
stars and hours for planets is the declared contract.

---

## D. Structure (α Cen: yes)

| | finding | α Cen? |
|---|---|---|
| D1 | **Cassandra crams 13 fields into `magnetism.magnetic_field`** — `magnetosphere`, the whole belt-geometry set, `radiation_model` — where A b and Pandora split the same content across `magnetic_field` / `magnetosphere` / `radiation_belts` | **yes** |
| D2 | 19 fields no node produces (see E) | 16 of 19 |
| D3 | 4 field kinds bundle several nodes' outputs into one prose string: `body_type`, `surface_type`, `composition`, `spin_axis_orientation` — 25 rows in α Cen, 75 across all boards | **yes, all 4** |
| D4 | `cliff_height` parked on Chaos's `identity` axis | **yes** |
| D5 | 40 Eri marks `fictional: true` on bodies that exist in `db/systems/40_eridani_a.json`, diverging from α Cen practice | no |
| D6 | 28 field names have no `field_alignment.yaml` entry and can therefore never override Phase 3 | partly |

---

## E. Fields no node produces (α Cen: 16 of 19)

Stellar appearance and activity, because `star_physical` stops at
[mass, radius, teff, luminosity, sed, v_sin_i] and nothing emits rotation or activity
indices: `activity`, `flares`, `flare_colour`, `spots_faculae`, `granulation`,
`limb_darkening`, `corona`.

Have a methodology doc but no chain node — the cheapest two to close:
`color` (`stellar-photospheric-color-methodology.md`), `ring_color`
(`debris-disk-color-methodology.md`).

No node at all: `aurora`, `banding_morphology`, `cloud_coverage`, `terrain`, `specular`,
`habitable_zone`, `neutral_torus_supply`, `co_orbitals`, `satellite_count`, `biosphere`.

---

## F. Prose hygiene (α Cen: clean)

Other boards carry these; α Cen passes. Recorded for the rollout, not for now.
`tau_cet` — 14 rows missing `narrative_ko` / `evidence_ko` pairs, 7 rows with driver
tokens outside the SPEC §1 vocabulary, 6 rows with `**` markup, 6 with em-dash.
`fomalhaut` — 10 rows with em-dash.

---

## Rollout

α Cen fixes B1–B3, C1–C3, C5, D1, D3, D4 and closes what it can of E. Each fix lands as a
rule in the standard and a check that enforces it, so applying it to the remaining six
boards is running the check and clearing what it reports — not repeating this analysis.
C4, D5 and F are the items α Cen cannot exercise; they wait for their own board.
