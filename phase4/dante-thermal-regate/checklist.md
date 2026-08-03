# Dante thermal re-gate (audit C5) + Chaos ice-stability grounding (audit C9)

Owner call 2026-08-03: keep the yellow sulfur look, move the *temperature* below
sulfur's melting point instead. Rationale: a wrong melting point is legible to
anyone with school chemistry, a wrong tidal-heat partition is not.

## C5 — Dante ambient temperature

- [x] Re-derive the ambient/hotspot partition that closes the 11,500 W/m2 budget
      with ambient below 388 K
- [x] `Dante/bulk.tidal_heating` — flux note, hotspot fraction, lid thickness
- [x] `Dante/surface` — `surface_temperature`, albedo override retirement, narrative
- [x] `Dante/appearance` — sulfur now a stable phase, verdict
- [x] `Dante/gameplay` — heat claim, Sulfur Plains biome kept
- [x] `Hades/surface` — the Dante-vs-Hades contrast line (audit M7 neighbourhood)
- [x] `provenance` line on every row whose value moved

## C9 — Chaos ice stability

- [ ] `docs/reference/ice-stability-methodology.md` (ADS-verified recipe)
- [ ] ko mirror
- [ ] `docs/reference/methodology-index.md` entry
- [ ] `Chaos/surface` + `Chaos/satellites` refs point at the recipe, not at papers
      lifted from inside the tool

## Close-out

- [ ] `python3 scripts/check_phase4_gate.py` clean
- [ ] `./scripts/check.sh`
- [ ] rebuild the alpha_centauri board pages
- [ ] commits (one per logical change)
