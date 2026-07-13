# Bulk-row normalization — checklist

Owner decisions (2026-07-12): class-based 3-template fieldset; keep `gravity`
(derived, consistency-checked); n/a fields stay present with `value: null` +
`na_reason`.

- [x] SPEC §0: add `geopotential_c22`, `gravity`, `reference_radius`, `j4`,
      `tidal_surface_flux` to the bulk menu
- [x] SPEC §3.2 (new): bulk template convention — `body_class` enum, 3 templates,
      core set, `na_reason`, dedicated-row union rule, gravity consistency
- [x] Validator: bulk menu names, `na_reason` allowance, template enforcement,
      per-body bulk anchor-row requirement (+ dedicated-row inner fields count in union)
- [x] Normalize `alpha_centauri.yaml` (hand-worked exemplar) — validator 0 errors
  - [x] A / B: new bulk anchor rows (passthrough echo + body_class star)
  - [x] A b: body_class free_rotator + gravity + c22 na + reference_radius field in J2 row
  - [x] Dante / Hades / Pandora: body_class tidally_locked + gravity + reference_radius
  - [x] Cassandra: body_class free_rotator + reference_radius + c22 na_reason
  - [x] Chaos: body_class free_rotator + internal_heat (negligible) +
        spin_axis (15° tilt, azimuth de-perfect-at-emit) + reference_radius + c22 na_reason
- [x] Normalize the other 5 boards — barnard/tau ceti/fomalhaut via Opus agent
      (verified by hand: gravity recomputation, diff review, parity); proxima/40 eri
      done inline after the second agent stalled (no file damage — it died reading)
- [x] Severity split (design revision mid-run): template *coverage* gaps downgraded
      to warnings; *structure* stays hard — per-decision philosophy (SPEC §3.2)
- [x] `check_phase4_gate.py` 0 errors on all 6 boards; decision-signature parity vs
      HEAD clean (only intended adds: αCen A/B anchor rows)
- [x] Rebuild board HTML for all 6 systems
- [x] Update skill `references/board-schema.md` with the template convention
- [x] `./scripts/check.sh` clean (only failure = mirror gate, all 7 under the other
      session's uncommitted plans/principia-interstellar-branch/ — not ours)

Follow-up (owner request 2026-07-13): `flattening` as a core slot

- [x] SPEC §0 menu + §3.2 core list + derivation note (f definition, star/free vs
      locked formulas, undecided-figure → coverage warning)
- [x] Validator: `flattening` in bulk menu + BULK_CORE
- [x] Fill all 16 figure-decided anchors (values from J₂+q via methodology relations;
      Erid/Fomalhaut/Polyphemus from doc §6 worked values) — 4 new warnings only on
      figure-undecided bodies (Proxima c / c I / d, 40 Eri A d)
- [x] Skill board-schema.md core list + derived-echo note
- [x] Validator 0 errors on all 6 boards; HTML rebuilt
