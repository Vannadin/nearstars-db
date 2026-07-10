# Phase 4 board — schema v2 quick reference

Condensed from `phase4/SPEC.md §3.1` + `phase4/emit-hardening/context-notes.md`.
The SPEC is authoritative; this is the at-hand authoring card. Validator:
`scripts/check_phase4_gate.py` (check.sh gate 8).

## File header

```yaml
schema_version: 2          # opt-in; absence ⟹ legacy v1 (soft-checked, not emit-ready)
system: alpha_centauri     # board slug (scripts/pipeline/_naming.to_file_slug) — may differ from db filename
status: staged             # file-level: staged until Phase 4 is activated
updated: 2026-07-10
decisions:
  - ...                    # one row per (body × axis group)
```

## Row shape

```yaml
- body: "Alpha Centauri A b"     # exact display name
  kopernicus_name: Polyphemus    # optional — cfg-internal name emitters/RB need, if different
  axis: bulk                     # a §0 GROUP (with fields[]) or group.name (single field + top-level value)
  status: gated                  # passthrough | open | art-directed | gated | emitted | superseded
  driver: [window-selection, art-direction]   # taxonomy class(es), SPEC §1
  narrative: >                   # human prose — reasoning/context (Korean OK)
    ...
  fields:                        # one typed entry per emit field — the machine layer
    - name: radius               # → bulk.radius (a §0 axis name)
      value: 1.0
      unit: R_jup
      op: set                    # set | scale | passthrough
      phase3_default: "1.0 R_Jup (low)"
    - name: geopotential_j2
      value: 0.023
      reference_radius_km: 71492
      op: set
      verdict: pass-in-window    # optional per-field; else inherits gate.verdict
      divergence_note: null      # required iff THIS field's verdict == documented-divergence
  gate:
    criterion: [observation]     # see gate-criteria.md
    verdict: pass-in-window      # pass-in-window | documented-divergence
    evidence: >
      reproducible pointer / error bar / window the value sits in
    divergence_note: null        # required (non-null) iff row verdict == documented-divergence
  refs: ["2508.03814"]           # bibcodes / arXiv ids, machine-readable list (no author names)
  discoverability_cfg:           # identity axis — promoted structured block (ResearchBodies)
    category: naked_eye
    ignorelevels: "T T T T"
    message: null                # ONDISCOVERY text; required for candidate/disputed
    ref: "2018AJ....155..117M"   # detection bibcode (not prose)
```

## Enums

| field | allowed |
|---|---|
| `status` | `passthrough` · `open` · `art-directed` · `gated` · `emitted` · `superseded` |
| `gate.verdict` / `fields[].verdict` | `pass-in-window` · `documented-divergence` |
| `op` | `set` · `scale` · `passthrough` |
| `axis` group | `identity` `orbit` `bulk` `atmosphere` `surface` `appearance` `magnetism` `environment` `rings` `satellites` `gameplay` |

## Validator rules (what fails vs warns)

**Hard FAIL (v2 boards only):**
- row missing `body` / `axis` / `status`; `status` or `verdict` off-enum;
  `axis` group not in the §0 menu.
- `gated`/`emitted` row with no `gate` block, or with an invalid `verdict`.
- `documented-divergence` (row or field) with a null/empty `divergence_note`.
- `passthrough` row that carries a `gate` block.

**WARN (non-fatal):** empty `gate.evidence`; a gated row with no machine-readable
value/`fields`; a gated row with no `refs`; a `fields[].name` not in the §0 menu.

## Authoring rules (the discipline the validator backs)

1. Prose → `narrative`. Every emit number → a typed `fields[]` entry. Never a
   number living only in prose.
2. Gate keys are exactly `criterion` / `verdict` / `evidence` / `divergence_note`.
   Not `note` / `paper` / `rationale`. Citations → `refs`.
3. `verdict: partial` is illegal → split into a pass field + a divergence field.
4. A replaced decision → `status: superseded` (kept for provenance, no live gate);
   the replacement is a separate live row with a distinct axis or the live axis.
5. Class-D fiction body: full body definition as fields (mass/radius/parent/orbit).
6. Board slug via `_naming`; do not hand-name. `kopernicus_name` carries the
   cfg-internal name when it differs from the display `body`.

## Legacy → v2 migration

Migrate one file at a time (soft-warn keeps check.sh green until then):
1. Add `schema_version: 2`.
2. Split each group-only prose row into `narrative` + typed `fields[]`.
3. Rename gate keys; lift bibcodes into `refs`.
4. Fix any `verdict: partial`, null `divergence_note`, or off-enum status.
5. Run `check_phase4_gate.py` → 0 errors; rebuild the board HTML.
`alpha_centauri.yaml` is the worked migration reference.
