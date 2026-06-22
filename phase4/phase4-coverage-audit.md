<!-- α Cen 시스템 Phase 4 완결성 감사 — (바디 × 축) 커버리지 매트릭스 + 백로그 (2026-06-22) -->
# α Centauri — Phase 4 Coverage Audit (2026-06-22)

Systematic `(body × axis)` readiness sweep for the confirmed α Cen system. The board
(`alpha_centauri.yaml`) records only **deltas**, so "few rows" hid a large un-boarded
surface. This audit enumerates the whole surface and classifies each cell.

Legend: **gated** (finalized) · **needs-decision** (a Phase 4 choice is owed) ·
**pass-ok** (Phase 3 value emits unchanged, defensible) · **pass?** (probably passthrough,
never verified) · **menu-gap** (real element with NO axis in SPEC §0) · **N/A**.

## Findings that are not just backlog (correctness)

1. **Aurora contradicted Phase 3 → reclassified (fixed).** Phase 3 `aurora_present=false`
   ("quiet G2V wind, cfg renders none"); the board had gated it `pass-in-window`. Corrected
   to **documented-divergence** (Phase 4 art-directs a *visible* rose-magenta aurora; only
   the *color* is composition-locked). Also given `depends_on: magnetosphere`.
2. **Ring: Phase 3 ≠ Phase 4 (emit must use Phase 4).** Phase 3 synthesizes a **dark thick
   Roche-zone ring** (1.4–2.5 R_p, `#6e6253`, opacity 0.85). Phase 4 gated a **faint far
   Chaos-fed E-ring** (800k–2.5M km, τ 9e-5, in Chaos's plane). The Phase 4 decision
   overrides, but the Phase 3 ring fields are **superseded** — the emitter must not read them.

## Menu gaps (axes missing from SPEC §0 entirely)

The fixed menu is orbit / bulk / atmosphere / appearance / satellites. These real elements
have **no axis**, so they cannot be tracked on any board as-is:

- **magnetosphere / magnetic field** — planet `magnetic_field=500 µT` (low); stars carry
  B-field in the `phase3/stellar_wind_synthesis` layer. Drives aurora + moon radiation.
- **radiation environment** — Kerbalism zones; Dante noted >4500 rem/day. Depends on
  magnetosphere + stellar wind.
- **stellar wind / mass-loss / activity / X-ray** — lives in `stellar_wind_synthesis`, not
  the board. Drives heliosphere + radiation.
- **rotation / spin axis / obliquity** — planet rotation 10 h + obliquity 27° (both low).
  Drives J2, day length, seasons, ring plane. (Note: J2 was gated assuming obliquity 0 in
  the moon sim — mild tension with the 27° Phase 3 tie-break.)
- **heliosphere / astrosphere**.

## Per-body matrix

### α Cen A b (Polyphemus) — board exists
| axis | Phase 3 (conf) | board | class |
|---|---|---|---|
| orbit.a / e | 1.6 AU / 0.1 | gated | **gated** |
| orbit.inclination_deg | mutual 16° | open | **needs-decision** (sky-frame, bimodal) |
| bulk.mass | 120 M⊕ (med) | — | pass-ok |
| bulk.radius | 1.0 R_Jup (low) | gated | **gated** |
| bulk.geopotential_j2 | (gated) | gated | **gated** |
| atmosphere.composition | H₂/He metal-enriched (med) | — | pass-ok (drives banding/haze) |
| atmosphere.pressure | 1 bar ref (med) | — | pass-ok |
| atmosphere.temperature | 225 K (med) | — | pass-ok |
| appearance.banding | white/faint (low) | gated | **gated** (partial) |
| appearance.haze | — | gated | **gated** |
| appearance.aurora | present=false (med) | gated | **gated (divergence, fixed)** |
| appearance.clouds | cover 0.9 / morph (low) | — | **pass?** (folded into banding, not gated alone) |
| appearance.rings | dark Roche ring (low) | gated→E-ring | **gated** (Phase 3 superseded) |
| appearance.surface | — | — | N/A (gas giant) |
| satellites | 5 moons | gated | **gated** |
| **magnetic_field** | 500 µT (low) | — | **menu-gap / needs-decision** |
| **radiation_env** | — | — | **menu-gap** |
| **rotation / obliquity** | 10 h / 27° (low) | — | **menu-gap / needs-decision** |
| internal_heat | T_int<110 K | — | pass-ok |

### α Cen A (star) — NO board rows
identity/bulk (type/mass/radius/Teff/L/[Fe/H]/age) all **high** → pass-ok. Appearance:
`visual_surface_tint #fff4e8` (med tie-break) → pass-ok / optional art. **menu-gap**:
rotation 22 d, activity log R'HK −4.95, cycle 19 yr, X-ray log Lx 27.0–27.6, B-field/wind
(stellar_wind layer), radiation it imposes, corona-during-eclipse event (gameplay tie-break).

### α Cen B (star) — NO board rows
K1V analog of A (same field structure, different values). Same menu-gaps (activity / wind /
B-field / X-ray / radiation). Identity = pass-ok.

### Moons — only `satellites` LIST gated
orbit a/e/i = **gated via list**. Per-moon, none individually boarded:
- **Pandora**: atmosphere (canon, dense N₂ + toxic trace), surface/biosphere look (cyan
  bioluminescence), climate (art-direction study, not a gated row), **radiation env** (from
  planet magnetosphere) → several **needs-decision / menu-gap**.
- **Cassandra**: N–H atmosphere (canon) → atmosphere needs-decision.
- **Dante**: >4500 rem/day, volcanic glow surface → **menu-gap (radiation)** + appearance.
- **Hades**: tidal-heated >900 K ember glow → appearance needs-decision.
- **Chaos**: fractured surface → appearance pass?.
- Dependency: moon radiation needs the **planet magnetosphere** decision first.

## Backlog, ranked

1. ✅ **DONE (2026-06-22).** Added `magnetism` + `environment` axis groups (+ bulk
   `rotation_period`/`obliquity`) to SPEC §0; gated the planet's `magnetism.magnetic_field`
   (**170 µT** via Reiners & Christensen 2010 dynamo scaling — the Phase 3 **500 µT was an
   ungrounded ~3× guess**, documented-divergence), `magnetism.magnetosphere` (R_mp ≈ 21 R_p,
   all 5 moons inside, inner 3 in belts), and `environment.radiation` (Dante extreme →
   Pandora moderate-shielded). Unblocked the aurora dependency. **Follow-up owed:** correct
   Phase 3 doc's 500 µT → 170 µT (+ ko mirror); reconcile the stale 225k/27 h Pandora prose
   (line 261) to the 252,393 km / 32 h JSON.
2. ✅ **DONE (2026-06-22).** Stars A & B `magnetism`/`environment` rows added. Activity /
   radiation / heliosphere = **passthrough** (Phase 2 measured: A P_rot 22 d / log Lx 27.0–27.6;
   B clean 8.84 yr cycle / X-ray ×10 swing; shared astrosphere ~176 AU). Gated: `magnetic_field`
   as an **activity-proxy** (A ~1–2 G solar-twin, B ~2–4 G — no direct ZDI, low-conf, ZDI pull
   flagged) and `stellar_wind` as **documented-divergence** (Wood measured only the combined
   ~2 Ṁ⊙; per-star split A≈1 / B≈0.6 is X-ray-weighted). The planet dynamo method does NOT
   apply to stellar fields (used activity/Rossby instead). **Owner choices left open:** the
   A/B wind-partition rule; whether to upgrade the B-field rows with a ZDI literature pull.
   Star *appearance* (color/granulation/limb-darkening/spots) still un-boarded → pass-ok.
3. **Planet rotation/obliquity axis** — reconcile obliquity 27° with the J2-at-0 sim assumption.
4. **Pandora as its own body** — atmosphere / surface-biosphere / radiation (the hero moon).
5. ✅ **DONE (2026-06-22).** `orbit.inclination_deg` gated. The only constrained quantity is
   the **mutual inclination 16° to the AB plane** (stability-selected; observed ~50°/130° is
   Kozai-unstable — documented-divergence, already in Phase 3). The absolute sky-frame
   inclination is a free emit-orientation that preserves the 16° mutual (prograde); not a
   separate observational value (Beichman sky-plane is bimodal/weak). No "emit-coupling"
   blocker — the emitter just realizes the gated 16° mutual deterministically.
   **→ Polyphemus (the planet) is now fully gated: no `open` rows remain.**
6. Other moons' appearance/atmosphere; planet `appearance.clouds` explicit gate.

Note: actual cfg **emit/writers** remain deferred to project-end (owner decision 2026-06-11).
This backlog is Phase 4 *decisions*, not emission.
