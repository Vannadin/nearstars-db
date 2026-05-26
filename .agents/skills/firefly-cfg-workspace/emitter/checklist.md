# Firefly emitter — checklist

Started 2026-05-26. Build the Phase 3 → Firefly cfg emitter + the
foundational element plasma color DB.

## Stage 1 — Element plasma color DB

- [ ] Design `db/refs/element_plasma_colors.yaml` schema (per-element
  hex + status + basis + source)
- [ ] Populate alkali metals (Li, Na, K, Rb, Cs, Fr) — canonical
  flame-test colors from chemistry refs
- [ ] Populate alkaline earth (Be–Ra) — same source
- [ ] Populate halogens + noble gases (F, Cl, Br, I, At, Ts | He, Ne, Ar, Kr, Xe, Rn, Og)
- [ ] Populate period 1–4 main-group (H, C, N, O, P, S, Al, Ga, Ge, As, Se, Sb, Te, Bi, Pb, etc.)
- [ ] Populate transition metals row 1 (Sc–Zn) — Cu green, Fe gold are well-known; rest mostly checkered in Helmenstine chart
- [ ] Populate transition metals row 2–3 (Y–Cd, La–Hg) — most no-data
- [ ] Populate lanthanides — Eu, Sm, Tb, Dy have observable flame; rest no-data
- [ ] Populate actinides — U has yellow-green; rest no-data or radioactive
- [ ] Populate superheavy / synthetic (Rf+) — all "too_short_to_observe"
- [ ] Add explicit `status` enum: visible / no_data / not_visible_to_humans
  / too_radioactive / too_short / no_flame_color (mirrors Helmenstine legend)

## Stage 2 — DB validation + companion doc

- [ ] Write `scripts/refs/validate_element_colors.py` — every hex
  6-digit lowercase; every entry has status + name + atomic_number;
  visible entries have hex + basis; no_data entries have null hex
- [ ] Write `docs/reference/element-plasma-colors.md` — bilingual
  human-readable companion (rendered from db YAML if practical, else
  manual mirror)

## Stage 3 — Firefly emitter

- [ ] Write `.claude/skills/firefly-cfg/scripts/emit_firefly_cfg.py`
  modeled on `emit_principia_cfg.py`. Inputs: `db/systems/*.json` +
  `docs/phase3/<slug>.md` Decisions (Phase 3 atmosphere fields).
  Outputs: `dist/NearStars-Configs/Patches/Firefly/<Body>.cfg` per
  body + one `NearStarsPlanetPack.cfg`
- [ ] Bulk-gas color lookup: hardcoded table mirroring
  composition-color.md §3 (N2+O2, CO2, H2+He, CH4, H2O, pure H2)
- [ ] Secondary-species streak lookup: composition-color.md §4 table
  → in-emitter Python dict
- [ ] Pressure → strength_multiplier formula (clamp 0.3 + 0.7 × log10)
- [ ] Temperature → particle_threshold (≤ 300 K → 1500, else 1800)
- [ ] Phase 3 `atmofx_*_hex_intensity` overrides take precedence over
  composition-derived defaults
- [ ] `--dry-run` + `--system <slug>` flags (match principia-cfg CLI)

## Stage 4 — Wire + verify

- [ ] Update `.claude/skills/firefly-cfg/SKILL.md` Steps 1–8 to call
  `emit_firefly_cfg.py` as the primary path; manual Steps 1–8 become
  fallback/audit
- [ ] Update `composition-color.md` element-table (Li/Na/K/etc.) to
  reference the new DB
- [ ] Register new scripts + DB in `docs/reference/tools.md` (en + ko)
- [ ] `./scripts/check.sh` clean

## Related

- [Phase 2 generic-apply](../../../../phase2/generic-apply/checklist.md) — sibling pattern (declarative YAML + generic applier)
- [Phase 3 generic-driver](../../../../phase3/generic-driver/checklist.md) — sibling pattern (system.yaml + driver)
- [composition-color reference](../../../../.claude/skills/firefly-cfg/references/composition-color.md) — input to Stage 3
