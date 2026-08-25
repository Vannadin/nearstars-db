# Field standard — establish it on α Cen, then roll it out

α Cen is the board being edited. Everything found on the other six is kept in
[FINDINGS.md](FINDINGS.md); each fix here is meant to land as a rule plus a check, so
applying it elsewhere is running the check, not repeating the analysis.

## The shape we are moving to

NearStars becomes a **computation tool**, and what it computes is **physical state, not
KSP config**. The engine derives the physics; an adapter turns it into cfg.

```
engine  →  physical state (game-agnostic)  →  adapter  →  KSP cfg
```

A methodology becomes a **deterministic function**. Its output is a physical quantity —
one quantity, one unit, one producing node. Same inputs, same values, and a machine can
compare them.

Admission to the engine layer is decided by **"is this a quantity with a unit, or a
declared dimensionless or categorical state?"** — not by whether it reaches a cfg field.
The two layers are bounded separately (physics on one side, an external schema on the
other), so neither grows the other. See [FINDINGS §0](FINDINGS.md).

The boards mix the layers today: 90 field kinds are physical state, 68 are game encoding,
and the encoding clusters are where every accident happened — sixteen `pause_*`
parameters standing in for one number, R_mp.

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

### 0. Layer
- [ ] Mark every field in `bindings.yaml` as `layer: physical` or `layer: encoding`.
      → verify: every field has a layer; `backflow.py` can report the two separately.
- [ ] **Take the `pause_*` / `inner_*` / `outer_*` / `radiation_*` families off the board.**
      52 hand-maintained kinds over 148 rows encode belt and magnetopause geometry that
      follows from R_mp, belt extent and belt intensity. The engine should record those
      three; the adapter should regenerate the rest each build.
      → verify: changing R_mp regenerates every dependant with no hand edit, and
      `backflow.py after pause_nose` has nothing left to warn about.

### 1. Names
- [x] `base_colour` → `base_color`; menu variants removed; `fields[].name` validated
      against `engine/bindings.yaml`; menu-widening blocked. (`92041e6e`)
- [ ] **Resolve the R_mp triple alias** — `magnetosphere`, `magnetopause_standoff_rp`,
      `pause_nose` are three names for one quantity (A b: 35.33 in all three).
      Under the layer split this is nearly settled: R_mp is the physical value, the other
      two are its encodings.
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
