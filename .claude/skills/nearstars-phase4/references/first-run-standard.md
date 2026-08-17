# Phase 4 first-run standard — authoring a body's board from zero

The fixed procedure for the FIRST authoring pass of a body — "first run" =
**that body has zero live rows on its board** (a half-authored body resumes at
its first missing block in the §1 order, with the coverage table rebuilt from
what exists; a fully-walked body is per-decision work, not a first run). It exists
because ad-hoc first runs each miss different things (observed 2026-08-17,
Luhman 16: the orbit axis was forgotten until the owner flagged it, magnetism
was first gated as prose without running the geometry methodology, and the
stability validation initially ran 363 orbits against an orbit-counted
standard). Follow it in order; do not improvise the sequence.

## 0. Pre-flight (before any row)

- Read the body's Phase 3 report AND its DB record in full.
- Build a **coverage table**: all 11 axis groups from SPEC §0 (identity /
  orbit / bulk / atmosphere / surface / appearance / magnetism / environment /
  rings / satellites / gameplay), each with a planned disposition —
  `gated`, `passthrough`, or `open` — and the input that will decide it.
  **No axis may be discovered mid-run.** Show the table to the owner before
  the first block.
- Locate every derived value's recipe in `docs/reference/methodology-index.md`
  **before** deriving anything by hand. Recipe missing → commission it via
  `nearstars-methodology` first (that is a feature of the run, not a detour).
  Registered tools (`scripts/refs/*.py`) are run, not re-implemented, and the
  reproduce path goes in the field note.

## 1. Block order (fixed)

1. `identity` + the `bulk` anchor, written as ONE validation unit — an
   identity-only body hard-fails the validator (no live bulk anchor), so the
   first checkpoint comes after both rows exist. Owner review still happens
   per block; only the validator run is joint.
2. `bulk` anchor (§3.2; body_class from {star, free_rotator, tidally_locked})
3. `orbit` — including the **epoch phase**: rewind to JD 2433282.5 (1950.0)
   per the phase-match methodology step 3, then **validate round-trip** with
   the stability sim (see §3) before freezing.
4. dedicated bulk rows: `bulk.spin_axis_orientation`, `bulk.geopotential_j2`
   (+ reference_radius + flattening; stellar-class J2 is always computed)
5. `atmosphere`
6. `surface` (or explicit n/a)
7. `appearance` (+ split rows like `appearance.aurora` where the owner
   diverges)
8. `magnetism` — mandatory tooling, never prose-only ("present but
   non-emitting" is not a row): the recipe is
   `docs/reference/planetary-magnetosphere-geometry-methodology.md` and the
   calculator is `scripts/refs/magnetopause_geometry.py` (run it; add the
   body to its report registry so the numbers reproduce); belts decided with
   the current class precedents in refs
9. `environment`
10. `rings`, `satellites` (explicit none is fine)
11. `gameplay` last (biome shape per the SPEC three-part rule)

## 1b. Anchor composition (thin-anchor style, new boards)

The union rule lets a template slot live in the anchor OR a dedicated row,
which historically split the boards into "fat anchor" (everything inline) and
"thin anchor" styles. **New boards use the thin-anchor style**:

- The anchor carries the measured passthrough echoes: mass, radius, gravity,
  intrinsic_luminosity (stars/BDs) or internal_heat, age, rotation_period,
  plus the class na fields (obliquity/c22 where they are structurally absent).
- `bulk.spin_axis_orientation` and `bulk.geopotential_j2` (+ reference_radius
  + flattening) are ALWAYS dedicated rows — they carry real derivations and
  deserve their own narrative.
- Field order inside any bulk row: mass, radius, gravity, flattening,
  intrinsic_luminosity/internal_heat, age, rotation_period, obliquity,
  geopotential_* , reference_radius, spin_axis_orientation. (Cosmetic, but it
  makes cross-body diffs readable.)
- Existing fat-anchor boards are left as they are; do not churn them.

## 2. The owner loop (per block)

- Propose ONE block at a time: full row YAML including narrative in both
  languages. Never batch-write the board.
- narrative_ko is composed as Korean, not translated (no translationese; the
  register is plain "~다"; no em-dash in any rendered field; sentences end
  `.`/`?`/`!`).
- When the owner edits the prose, **give feedback before merging** (spelling,
  register consistency, nuance lost by compression, subject clarity) — then
  write the agreed final. Never paste owner text unreviewed, never silently
  rewrite it either.

## 3. Validation cadence

- `python3 scripts/check_phase4_gate.py` after EVERY row write; fix to
  0 errors before proposing the next block.
- Stability runs use the **orbit-counted** duration standard: read the
  "Duration by hierarchy" section of `phase3/stability-sim/STABILITY_REPORT.md`
  *for the number* before integrating (satellite systems 1e4 yr; two-body /
  planetary hierarchies: enough orbits that the verdict is duration-stable,
  >=1e4 orbits as the floor — a 1e4-yr run on a 27-yr binary is 363 orbits and
  fails the standard). Two
  integrators (IAS15+MEGNO, leapfrog) per the validation standard; process
  and numbers go to the STABILITY_REPORT, the conclusion goes to the row,
  and the report path goes in `refs[]`.
- `build_phase4_html.py <system>` at milestones; eyeball the rendered page
  (owner reads it there, not in the YAML).

## 4. Schema gotchas (all observed in real runs)

- `driver:` tokens are exactly {window-selection, engine, synthetic, fiction,
  art-direction}; `passthrough` rows carry **no** driver and **no** gate.
- `refs[]` entries are quoted strings (a bare arXiv id parses as a float).
- Em-dash is banned in every rendered field (narrative, evidence, notes).
- `documented-divergence` requires `divergence_note`; `owner-override` must
  NOT have one. A gated row without `gate.evidence` warns — fill it
  (① conclusion ② the check performed ③ one honest caveat).
- Value changed on an existing row → same-edit `provenance:` line.
- refs provenance: measured passthrough → all measurement papers; derived →
  the methodology doc (never its internal papers); sim-derived → the sim
  report; gameplay/identity → refs-exempt.

## 5. Exit criteria (first run is DONE when)

- Coverage table fully dispositioned: no `open` rows left except ones the
  owner explicitly parked.
- `check_phase4_gate.py`: 0 errors, and 0 warnings **attributed to this
  board** (the validator prints all boards; other systems' warnings are not
  this run's exit blocker and their boards are not to be churned).
- Board HTML built and eyeballed; checklist.md ticked; context-notes.md
  carries the decisions-with-reasons; one commit per logical unit throughout.
