# Field standard — establish it on α Cen, then roll it out

α Cen is the board being edited. Everything found on the other six is kept in
[FINDINGS.md](FINDINGS.md); each fix here is meant to land as a rule plus a check, so
applying it elsewhere is running the check, not repeating the analysis.

## The shape we are moving to

A methodology becomes a **deterministic function**. Its output is the board's typed
`fields[]` — one field, one quantity, one unit, one producing node. Same inputs, same
values, and a machine can compare them.

**Prose is demoted to a settings book.** Today `narrative` carries decisions, which is
exactly why four field kinds bundle several nodes' outputs into one string
(`body_type` packs composition, mass, T_eq and cloud class). After this, prose explains
and colours; it does not hold values.

**Approved narratives are not rewritten.** The work is to *extract* the values out of the
prose into typed fields, leaving the prose in place as the settings-book text. Nothing
already approved gets reworded to fit the machine.

**Not everything is deterministic, and that is fine.** The six owner nodes
(`composition_intent`, `ocean_fraction`, `ocean_depth`, `resonance_architecture`,
`ring_system`, `star_metallicity`) and art direction stay owner choices — but they become
*declared inputs*, not prose. Deterministic given the owner's picks.

## Tasks

### 1. Names
- [x] `base_colour` → `base_color`; menu variants removed; `fields[].name` validated
      against `engine/bindings.yaml`; menu-widening blocked. (`92041e6e`)
- [ ] **Resolve the R_mp triple alias** — `magnetosphere`, `magnetopause_standoff_rp`,
      `pause_nose` are three names for one quantity (A b: 35.33 in all three).
      → verify: one name survives in α Cen; `backflow.py field <name>` shows a single
      node and the full dependant list; a check rejects the retired names.

### 2. Units
- [ ] Write the per-class unit table into `field_alignment.yaml` — it declares `star` and
      `planet` where the boards use **star / planet / moon**, so every moon's `kg` and
      `km` is currently off-contract.
      → verify: every α Cen unit string matches a declared (field, class) pair.
- [ ] Settle the three α Cen splits: `reference_radius` m vs km (factor 1000),
      `pressure` atm vs bar, `radius` R_jup vs R_sun vs km.
      → verify: one unit per (field, body class), enforced by the gate.
- [ ] Declare the dimensionless fields as dimensionless instead of leaving `unit` absent
      and inferred (`geopotential_j2`, `flattening`, `albedo`, `eccentricity`, `hapke_*`,
      `pause_compression`…).
      → verify: a numeric field with no `unit` and not on the dimensionless list fails.

### 3. Structure
- [ ] **Cassandra's magnetism axis** — 13 fields crammed into `magnetism.magnetic_field`
      where A b and Pandora split them across `magnetic_field` / `magnetosphere` /
      `radiation_belts`.
      → verify: the same field never appears under two different axes across bodies.
- [ ] `cliff_height` moved off Chaos's `identity` axis.
- [ ] **Unbundle the four prose-carried kinds** — `body_type`, `surface_type`,
      `composition`, `spin_axis_orientation`, 25 rows in α Cen. Extract each quantity into
      its own typed field; leave the narrative text untouched.
      → verify: `backflow.py debt` reports zero bundled fields for α Cen.

### 4. Close what α Cen can of the missing nodes
- [ ] `color` and `ring_color` — both already have methodology docs
      (`stellar-photospheric-color-methodology.md`, `debris-disk-color-methodology.md`)
      and no chain node. Cheapest two.
      → verify: `backflow.py check` drops those two warnings.

### 5. Make it a standard, not a cleanup
- [ ] Every rule above expressed as a check in `check_phase4_gate.py`.
      → verify: reverting any α Cen fix by hand makes the gate fail.
- [ ] Write the rules down where the boards are authored (SPEC §0/§3.1).

## Deferred — needs the owner or another board

- `gravity` in `g` on 40 Eri where the contract says `m/s²`. Changes shipped numbers and
  the notes quote them (`2.09 g` → `20.50 m/s²`, `0.38` → `3.73`, `0.20` → `1.96`).
- 40 Eri `fictional: true` on bodies that exist in the DB.
- Prose hygiene on `tau_cet` (14 missing `_ko` pairs, off-vocabulary driver tokens, `**`
  markup, em-dash) and `fomalhaut` (em-dash). α Cen is clean, so it cannot drive these.
