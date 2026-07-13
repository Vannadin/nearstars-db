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
  body_class: free_rotator       # bulk ANCHOR rows only — star | tidally_locked | free_rotator (SPEC §3.2)
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
      note: "= 10/3·C̄₂₂, φ0.95"  # optional short annotation (canon anchor, caveat, derivation tag)
      phase3_default: "..."      # optional — the Phase 3 value this decision overrides
    - name: banding_storm_eye    # color fields: value is a #RRGGBB hex
      value: "#214a72"
      window: "#1e4068–#2a5480"  # optional — the defensible range backing pass-in-window
      op: set
    - name: science_biomes       # biome rows: colors maps biome name → biome-map hex
      value: "6: Seas / ..."
      colors: { "Seas": "#2E5680", "Polar Ice": "#CBDEE6" }   # each value must be #RRGGBB (validated)
      op: set
  depends_on: ["Chaos / surface"]  # optional — other rows this gate's inputs came from
  moons:                           # satellites rows only — invented-system body-def ledger,
    - name: Dante                  # one entry per moon, Kopernicus Orbit ↔ Principia 1:1:
      a_km: 110000                 # full 6 elements (a_km/e/inc_deg/lan_deg/argp_deg/ma_deg)
      e: 0.01                      # + epoch (0 = game epoch) + mass_kg/radius_km.
      inc_deg: 9.0                 # GM is derived from mass_kg at emit — never duplicated.
      lan_deg: 89
      argp_deg: 178
      ma_deg: 35
      epoch: 0
      mass_kg: 8.0e21
      radius_km: 900
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

## Bulk template convention (SPEC §3.2)

Every real body (not `*`) with any live row carries **exactly one live `axis: bulk`
anchor row** tagged `body_class: star | tidally_locked | free_rotator`. Required slots:

- core (all classes): `mass` `radius` `gravity` `rotation_period`
  `spin_axis_orientation` `geopotential_j2` `reference_radius` `age`
- `tidally_locked` / `free_rotator`: core + `obliquity` + `geopotential_c22` +
  `internal_heat` (`star` = core only)
- alternates: `cooling_age` satisfies the age slot, `intrinsic_luminosity` the
  internal_heat slot.

**Union rule** — a slot counts if it appears in the anchor's `fields[]` OR in a live
dedicated `bulk.<name>` row for the same body (including that row's inner fields,
e.g. `reference_radius` inside a J2 row). Never duplicate a value in both places.

**n/a slots** stay present: `value: null` + non-empty `na_reason` (e.g. free rotator →
c22 "고정축 없음"). A field with neither value nor na_reason is a hard FAIL.

`gravity` is a derived echo of GM/R² (Kopernicus geeASL slot, owner decision
2026-07-12); the validator warns when it drifts >2% from the row's own mass/radius.
Exemplar rows: `phase4/alpha_centauri.yaml` (star anchors for A/B, free_rotator A b /
Cassandra / Chaos, tidally_locked Dante / Hades / Pandora).

## Enums

| field | allowed |
|---|---|
| `status` | `passthrough` · `open` · `art-directed` · `gated` · `emitted` · `superseded` |
| `gate.verdict` / `fields[].verdict` | `pass-in-window` · `documented-divergence` |
| `op` | `set` · `scale` · `passthrough` |
| `body_class` (bulk anchors) | `star` · `tidally_locked` · `free_rotator` |
| `axis` group | `identity` `orbit` `bulk` `atmosphere` `surface` `appearance` `magnetism` `environment` `rings` `satellites` `gameplay` |

## Validator rules (what fails vs warns)

**Hard FAIL (v2 boards only):**
- board has no `decisions:` list at top level (catches a misspelled key that would
  otherwise skip every row).
- row missing `body` / `axis` / `status`; `status` or `verdict` off-enum;
  `axis` group not in the §0 menu.
- two non-`superseded` rows sharing the same `(body, axis)` — supersede one.
- a `fields[]` entry that is not a mapping, lacks `name` or `value` (an emit number
  living only in prose is illegal), or has an `op` outside `set|scale|passthrough`.
- `refs` that is not a list of strings; a `colors` value that is not `#RRGGBB`.
- `gated`/`emitted` row with no `gate` block, or with an invalid `verdict`.
- `documented-divergence` (row or field) with a null/empty `divergence_note`.
- `passthrough` row that carries a `gate` block.
- §3.2 structure: a real body with live rows but no bulk anchor row; an anchor without
  a valid `body_class`; a field with neither `value` nor `na_reason`. (A template slot
  not yet walked is a WARNING — coverage is open work, structure is hard.)

**WARN (non-fatal):** empty `gate.evidence`; a gated row with no machine-readable
value/`fields`; a gated row with no `refs`; an `axis` name not in the §0 menu;
an empty `decisions` list.

`schema_version` is normalized: `2`, `2.0`, and `"2"` all count as v2 — a quoting
slip cannot silently downgrade a board to the legacy soft path.

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
