# File Layout

## Where the cfg files land

```
dist/
└── Principia/
    ├── Real_NearStars-GravityModel.cfg
    └── Real_NearStars-InitialState.cfg
```

`dist/` is a build artifact directory at the project root. It is regenerated from `db/` on every run; do not hand-edit. End users (or a future packaging step) copy these into their KSP install at:

```
GameData/NearStars/Patches/Principia/
├── Real_NearStars-GravityModel.cfg
└── Real_NearStars-InitialState.cfg
```

The `Patches/Principia/` subpath mirrors RSS-Reborn/Sol-Configs convention. Sol-Configs ships `Real_Sol-GravityModel.cfg` / `Real_Sol-InitialState.cfg` at the same depth; the names are chosen so they sort alongside Sol's files in mod-loader debug logs.

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

### Why no `:FOR[NearStarsSystem]`

`@principia_gravity_model { ... }` is a Module Manager **edit** of an existing node. The node was created by Sol-Configs's `:FOR[SolSystem]` block. We do not claim authorship. Adding `:FOR[NearStarsSystem]` would either be ignored or, in older MM versions, cause patch-ordering bugs.

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
