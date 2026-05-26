# Phase 2 generic apply pipeline — checklist

Goal: replace per-system `apply_phase2.py` (775+131 lines) with a single
declarative YAML + generic applier. Started 2026-05-26.

## Stage 1 — Schema + applier

- [ ] Define `phase2/<system>/measurements.yaml` schema (isomorphic to
  the curated.json subset that Phase 2 writes)
- [ ] Write `scripts/pipeline/apply_phase2.py <system>` — reads YAML,
  merges into `db/stellar_props_curated.json` + `db/planets_curated.json`
- [ ] Add `--check` mode that loads YAML, builds in-memory result, diffs
  against current db files without writing

## Stage 2 — Migration (Alpha Cen)

- [ ] Snapshot current `db/stellar_props_curated.json` + `db/planets_curated.json`
- [ ] Convert `phase2/alpha_centauri_proxima/apply_phase2.py` → `measurements.yaml`
- [ ] Run new applier, diff against snapshot — must be byte-identical
- [ ] Delete `phase2/alpha_centauri_proxima/apply_phase2.py`

## Stage 3 — Migration (TRAPPIST-1)

- [ ] Convert `phase2/trappist_1/apply_phase2.py` → `measurements.yaml`
- [ ] Run new applier, diff — byte-identical
- [ ] Delete `phase2/trappist_1/apply_phase2.py`

## Stage 4 — Wire into skill + tools

- [ ] Update `.claude/skills/nearstars-add-star/references/planet-curation.md`
  Phase 2 procedure: stop writing per-system Python, write YAML instead
- [ ] Register `apply_phase2.py` in `docs/reference/tools.md` (en + ko)
- [ ] Add example YAML stub at `phase2/_template/measurements.yaml`

## Verification

- [ ] `python3 scripts/pipeline/apply_phase2.py alpha_centauri_proxima --check` exit 0
- [ ] `python3 scripts/pipeline/apply_phase2.py trappist_1 --check` exit 0
- [ ] `python3 scripts/pipeline/validate.py` FAIL=0
- [ ] `./scripts/check.sh` clean

## Related

- [Phase 3 generic-driver workspace](../../phase3/generic-driver/checklist.md) — paired refactor track
- [nearstars-add-star skill](../../.claude/skills/nearstars-add-star/SKILL.md) — Phase 2 procedure caller
