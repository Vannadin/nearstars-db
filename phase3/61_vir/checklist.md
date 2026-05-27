# 61 Virginis stellar Phase 3 — checklist

Started 2026-05-27. Stellar-only synthesis. Planets b/c/d are a
separate follow-up workspace.

**Scope** (1 entry):
- 61 Vir (G6.5V solar twin) — slug `61-vir`

**Structural rule.** Use `docs/phase3/alpha-centauri-a.md` as the
stellar-synthesis base. Phase 2 inputs are minimal — DB has Vogt 2010
mass+radius only, no disk_measurements, no activity_measurements.
Compensate with literature-direct citations and Confidence=low for the
visual tint synth + disk geometry where Herschel doesn't constrain.

## Stage 0 — pre-flight

- [x] Phase 2 inputs spot-checked — `db/systems/61_vir.json` carries
      Vogt 2010 M=0.942 M☉, R=0.963 R☉; Gaia DR3 Teff=5552 K, parallax
      117.17 mas → d=8.53 pc. No disk_measurements; no
      activity_measurements; no rotation_measurements. Literature-direct
      sourcing for activity/disk per task spec.
- [x] Working dir `phase3/61_vir/` created
- [x] User confirmed 1–2 h budget, stellar-only scope, Wyatt 2012 +
      Lawler/Tanner 2014 + Su 2017 as the disk anchors.

## Stage 1 — Step 9.0 classification (mandatory gate)

- [x] Row-by-row classification logged in `context-notes.md`. Simple
      / quiet star → minimal divergence opportunity. Expectation:
      mostly canonical-aligned + a few interesting-first tie-breaks
      on visual tint + disk inclination.

## Stage 2 — English synthesis

- [ ] `docs/phase3/61-vir.md` — 8-section structure following
      `alpha-centauri-a.md` (intro / Decisions / Surface / Atmosphere /
      Rotation & spin / Visual / Bibliography / Open items)

## Stage 3 — Korean mirror

- [ ] `ko/docs/phase3/61-vir.md` — block-parity, natural prose, `.` /
      `?` / `!` only.

## Stage 4 — HTML + reports index + mirror check

- [ ] `python3 scripts/phase3/check_block_parity.py 61-vir`
- [ ] `python3 scripts/phase3/build_html.py 61-vir`
- [ ] `python3 scripts/pipeline/build_reports_index.py`
- [ ] `bash scripts/check-mirrors.sh`

## Stage 5 — browser visual check

- [ ] Lang toggle works
- [ ] Decisions table renders with correct columns
- [ ] Bibliography links plausible

## Related

- [61-vir entity page](../../docs/phase3/61-vir.md) — output this workspace produces
- [alpha-centauri-a](../alpha_centauri_proxima/) — stellar-synthesis template lineage
