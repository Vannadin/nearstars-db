# Phase 2 generic apply — context notes

## Design decisions

### YAML is isomorphic to curated.json (no transform layer)

Keep the YAML structure 1:1 with what `stellar_props_curated.json` and
`planets_curated.json` already store. The applier does dict-merge, not
field renaming. Two consequences:

- `stellar.*` entries use `reference` for provenance (matches existing db)
- `planets.*` entries use `source` for provenance (matches existing db)

The asymmetry is preserved because changing field names is out of scope —
that would break `build_systems.py` consumers.

### Phase 1 single-dict orbital is allowed (TRAPPIST-1 pattern)

`orbital:` can be either a single dict (Phase 1 — one source for the
orbital element set) or a list of dicts (Phase 2 — multiple papers).
`build_systems.py` already accepts both, so the YAML mirrors that.

### Merge semantics

For each host present in YAML:
- `stellar.<host>` → REPLACES the entire host entry in
  `stellar_props_curated.json[host]`. No partial merge — if you want to
  keep an existing field, write it back into YAML.
- `planets.<host>` → REPLACES the entire host entry in
  `planets_curated.json[host]` (a list of `pl_name`-keyed planet dicts).
  Same all-or-nothing rule per host.

This matches what the existing per-system scripts do (they call
`stellar["Alpha Centauri A"] = ALPHA_A` wholesale).

### Validation

- `scripts/pipeline/apply_phase2.py --check` runs in-memory only — useful
  before commit
- After write, the script invokes `scripts/pipeline/validate.py` and
  fails if validate fails

## Open questions / deferred

- Should YAML support `$extends:` for shared paper-provenance blocks?
  (Defer — paper provenance is usually system-unique. Repetition cost is
  low because YAML anchors solve it if it ever matters.)
- Should we add a `--dry-run` that prints the diff but doesn't write?
  Same as `--check` essentially — single flag is enough.

## Related

- [checklist](checklist.md)
- [`docs/reference/binary-epoch-pipeline.md`](../../docs/reference/binary-epoch-pipeline.md) — adjacent epoch-handling reference
