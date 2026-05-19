# File Layout

## Where the cfg files land

```
dist/
└── NearStars-Configs/
    └── Patches/
        └── Principia/
            ├── Real_NearStars-GravityModel.cfg
            └── Real_NearStars-InitialState.cfg
```

`dist/` is a build artifact directory at the project root. It is regenerated from `db/` on every run; do not hand-edit. End users (or a future packaging step) copy `dist/NearStars-Configs/` into their KSP install:

```
GameData/NearStars/NearStars-Configs/Patches/Principia/
├── Real_NearStars-GravityModel.cfg
└── Real_NearStars-InitialState.cfg
```

The `NearStars-Configs/Patches/` prefix mirrors the project's repository layout (`docs/reference/guideline.md` §4). The `Principia/` subfolder under `Patches/` is a deliberate choice over the guideline's `Patches/Sol/` slot — see `context-notes.md` for the rationale. Sol-Configs ships `Real_Sol-GravityModel.cfg` / `Real_Sol-InitialState.cfg` under the equivalent `Patches/Principia/` depth; our names sort alongside in mod-loader debug logs.

---

## File naming convention

Format: `<ScalePrefix>_NearStars-<NodeKind>.cfg`

| Prefix | Scale | NEEDS tag |
|---|---|---|
| `Real_` | Sol real scale (MVP) | `[NearStarsSystem,SolSystem,!SolQuarterScale]` |
| `Quarter_` (future) | Sol quarter scale | `[NearStarsSystem,SolSystem,SolQuarterScale]` |
| `RSS_` (future) | RealSolarSystem | `[NearStarsSystem,RSSConfig]` |

| `<NodeKind>` | Patched root |
|---|---|
| `GravityModel` | `principia_gravity_model` |
| `InitialState` | `principia_initial_state` |

The Sol-real-scale MVP emits exactly two files. Quarter-scale and RSS variants are deferred — see `planet-contract.md` for the migration plan.

---

## NEEDS tag rationale

### Gravity model — `:NEEDS[NearStarsSystem,SolSystem]`

- `NearStarsSystem` — gate on the NearStars mod itself being installed.
- `SolSystem` — gate on Sol-Configs (whose root `principia_gravity_model` we're patching).
- NO `!SolQuarterScale` — gravity parameters are scale-independent (μ = GM is a physical constant), so the same patch applies whether the user runs Sol real or Sol quarter.

### Initial state — `:NEEDS[NearStarsSystem,SolSystem,!SolQuarterScale]`

- Same first two gates.
- `!SolQuarterScale` — the Cartesian state we emit is anchored at `solar_system_epoch = JD 2433282.5`. Sol-quarter uses `JD 2433465.0`. Different epoch ⇒ different coordinates ⇒ separate file (deferred).

### Why no `:FOR[NearStarsSystem]` here

The project's general convention for NearStars patches IS `:NEEDS[...]:FOR[NearStarsSystem]` — see `docs/reference/guideline.md` §5.1, where `@EVE_CLOUDS:NEEDS[SolSystem]:FOR[NearStarsSystem]` is the canonical example. Principia patches diverge from that convention deliberately:

- For nodes NearStars **creates** (EVE_CLOUDS, Scatterer_atmosphere, Firefly), `:FOR[NearStarsSystem]` claims authorship and is correct.
- For nodes NearStars **edits** via `@` (Principia's `principia_gravity_model` / `principia_initial_state`, which Sol-Configs already authored), `:FOR[NearStarsSystem]` adds no value — the patch already runs in MM's general patching pass after all `:FOR[SolSystem]` blocks have created the root.

Either form would functionally work; the `:NEEDS[NearStarsSystem,SolSystem]` form is one character shorter and avoids implying authorship of someone else's node. Don't read this as "the guideline is wrong" — it's a node-class-specific judgment within the guideline's spirit.

---

## Load order

Module Manager processes `FOR` before `NEEDS`-only patches. Sol-Configs's root nodes are emitted in its `:FOR[SolSystem]` pass. Our `@principia_gravity_model:NEEDS[...]` patches run after, in MM's general-purpose patching pass. By the time Principia reads the GameDatabase, all body entries are merged.

No explicit `:BEFORE` / `:AFTER` ordering is needed.

---

## What is NOT emitted

- No `principia_numerics_blueprint` — Sol-Configs ships its own. Patching it is out of scope and risky (changes integrator behavior for everyone).
- No `principia_draw_styles` — trajectory colors are a UX setting, not a planet-pack concern.
- No `principia_override_version_check` — KSP-version compatibility is the user's responsibility.
- No `principia_initial_state` root with `solar_system_epoch` / `game_epoch` — patching those is what creates duplicate-root crashes.
