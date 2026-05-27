# 61 Virginis stellar + planets Phase 3 — checklist

Started 2026-05-27. Stellar synthesis (host star) complete. This
revision adds the b/c/d planet workspaces in the same directory.

**Scope** (4 entries):
- 61 Vir (G6.5V solar twin) — slug `61-vir` (DONE)
- 61 Vir b (hot super-Earth, 5.1 M⊕ Msini, 0.050 AU, P=4.215 d) — slug `61-vir-b`
- 61 Vir c (warm sub-Neptune, 18.2 M⊕ Msini, 0.22 AU, P=38 d) — slug `61-vir-c`
- 61 Vir d (cooler sub-Neptune, 22.9 M⊕ Msini, 0.476 AU, P=123 d) — slug `61-vir-d`

**Structural rule.** Use `docs/phase3/trappist-1-e.md` as the
planet-synthesis structural template (8 sections, divergence rules).
Phase 2 inputs are minimal — only Vogt 2010 Msini + orbit. Atmosphere
characterization is in the reflected-light regime (no JWST transit
spectrum because none of the three planets transit). Most decisions
are theoretical / interesting-first tie-breaks.

## Stage 0 — pre-flight (planets)

- [x] Phase 2 inputs spot-checked — `db/systems/61_vir.json` carries
      Vogt 2010 mass+orbit for b/c/d. All non-transiting (RV-only).
      `pl_controv_flag = 0` for all three.
- [x] Working dir `phase3/61_vir/` reused
- [x] User confirmed 4–6 h budget, all three planets in scope.

## Stage 1 — Step 9.0 classification (mandatory gate)

- [x] Per-planet classification logged in `context-notes-planets.md`
- [x] b: hot rocky / runaway steam category — expect many tie-breaks
      on surface mineralogy, atmosphere retention
- [x] c: warm sub-Neptune — expect H/He envelope canonical-aligned,
      cloud/haze tie-breaks
- [x] d: cooler sub-Neptune with high e=0.35 — expect water-world OR
      H/He-envelope tie-break; eccentricity-driven seasonal variation

## Stage 2 — English synthesis

- [x] `docs/phase3/61-vir.md` (host star — pre-existing)
- [ ] `docs/phase3/61-vir-b.md` — 8-section structure
- [ ] `docs/phase3/61-vir-c.md` — 8-section structure
- [ ] `docs/phase3/61-vir-d.md` — 8-section structure

## Stage 3 — Korean mirror

- [x] `ko/docs/phase3/61-vir.md` (host star — pre-existing)
- [ ] `ko/docs/phase3/61-vir-b.md` — block-parity, natural prose
- [ ] `ko/docs/phase3/61-vir-c.md` — block-parity, natural prose
- [ ] `ko/docs/phase3/61-vir-d.md` — block-parity, natural prose

## Stage 4 — HTML + reports index + mirror check

- [ ] `python3 scripts/phase3/check_block_parity.py 61-vir-b`
- [ ] `python3 scripts/phase3/check_block_parity.py 61-vir-c`
- [ ] `python3 scripts/phase3/check_block_parity.py 61-vir-d`
- [ ] `python3 scripts/phase3/build_html.py 61-vir-b`
- [ ] `python3 scripts/phase3/build_html.py 61-vir-c`
- [ ] `python3 scripts/phase3/build_html.py 61-vir-d`
- [ ] `bash scripts/check-mirrors.sh` exits 0

## Stage 5 — browser visual check (deferred, optional)

- [ ] Lang toggle works
- [ ] Decisions table renders with correct columns
- [ ] Bibliography links plausible

## Related

- [61-vir entity page](../../docs/phase3/61-vir.md) — host star Phase 3
- [trappist-1-e](../trappist_1/) — planet-synthesis structural template
- [proxima-cen-d](../alpha_centauri_proxima/) — non-transiting RV-only planet template (sub-Earth)
