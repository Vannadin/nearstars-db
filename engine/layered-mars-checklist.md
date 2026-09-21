# Layered Mars — checklist

Pre-registration: frozen artefact `3be84248` (chain `48322b7e` → `ed714214` → `a77a855e`).
Branch `layered-mars`, forked from `16110413`. One plate covers all three parts.

## Part 1 — the device, before the physics

- [ ] **1a. Negative control for prediction ㉣.** A line that binds "the three nodes that do not
      read the core boundary stay unchanged": `dynamo_rocky` (declared edge, no code consumer),
      `body_figure` and `cassini_state` (no module at all).
      → verify: the check is red when a boundary name is introduced into `dynamo_rocky`.
- [ ] **1b. Split the two names.** The *declared* board value is the apparent radius
      (iron core + molten layer); the *solved* value is the iron core. They share one name today.
      → verify: every site listed in the context notes carries the name that says which it is.
- [ ] **1c. Re-freeze the sulphur anchor** — the declared key changes, so the digests change.
      → verify: `test_mars_sulphur.py` passes against the regenerated anchor.

## Part 2 — the acceptance line

- [ ] **2a. Remove `recorded_disagreement`** from `expected.nmoi` and
      `expected.core_radius_fraction` in `bodies/mars.yaml` (owner decision `e112c81f`).
      → verify: `nmoi` turns the run red (−1.669 % against a 1 % tolerance); this is the
      expected intermediate state, not a defect.
      → verify: `[기록·해소?]` no longer prints for the radius axis (prediction ㉤).
- [ ] ⚠ **2a lands in the same plate as Part 1 and Part 3.** Pushing it alone would publish a red
      gate with nothing to fix.

## Part 3 — the physics

- [ ] **3a. Join the existing melt verdict to the structure.** `_silicate_melt_verdict` already
      labels a molten silicate column per body; its own docstring says the verdict is a name for a
      state and not a change of radius. This item carries that label into the boundary.
      → verify: a body with no molten column keeps both radii equal, and that equality is printed.
- [ ] ⚠ **No Martian constant is hard-coded.** Khan+ 2023's 150 ± 15 km is what we compare
      against, not what we install.

## Gate

- [ ] One gate run covers all three parts.
- [ ] Blob list to the directing seat before the gate.
- [ ] Audit clearance before the gate.

## Predictions (direction only, from the pre-registration)

| # | Prediction |
|---|---|
| ㉠ | `nmoi` moves in one direction only — down |
| ㉡ | the `core_radius_fraction` comparison leaves the apparent-radius window |
| ㉢ | of the five thermal nodes, `cmb_heat_flux` moves first |
| ㉣ | the three nodes that do not read the boundary stay unchanged |
| ㉤ | the radius axis's `[기록·해소?]` line disappears |
