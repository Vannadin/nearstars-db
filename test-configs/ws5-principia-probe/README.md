# WS5 Principia probe — test star configs

Four NearStars stars (α Centauri A, α Centauri B, Proxima Centauri, TRAPPIST-1),
**stars only, no planets**, with placeholder textures. Built for the WS5 probe so it
can load a vessel near a real distant star and watch a self-gravitating subsystem form.

This is a **committed snapshot of generated output**. The normal build path writes to
`dist/` (gitignored); the files are checked in here only so the probe install can pull
them from GitHub. Do not hand-edit — see "Regenerating" below.

## Install (stock Kerbol + Principia Keplerian path)

Copy `GameData/` over the probe install's `GameData/`, and add **Kopernicus** (required —
no Kopernicus, no bodies).

```
GameData/
├── Kopernicus/                         ← you supply this
├── NearStars-Configs/
│   ├── NearStars-Stars-Kopernicus.cfg          4 star bodies (@Kopernicus:FOR[NearStarsSystem])
│   ├── NearStars-StockKeplerian-Orbits.cfg     real orbital hierarchy (@Kopernicus:AFTER[...])
│   └── NearStars-StockKeplerian-GravityModel.cfg   @principia_gravity_model, no initial_state
└── NearStars-Textures/PluginData/…             placeholder sunspot + corona DDS
```

That is the whole install. `NearStarsSystem` is not a real mod folder — the `:FOR[NearStarsSystem]`
pass in the Kopernicus cfg is what declares the tag the other two patches need.

### Why this is the Keplerian path

There is **no `principia_initial_state`**. Principia therefore derives every body's state from
its Kopernicus osculating elements (`InsertCelestialJacobiKeplerian`), so stock Kerbol / Kerbin /
Mun need no Cartesian entries and the all-bodies-or-`Log.Fatal` consistency check never runs.

Side effect of having no `initial_state`: Principia applies `StabilizeKSP()` to the stock Jool
system (Vall/Tylo mean motions shifted out of the 1:2:4 resonance, Bop flipped retrograde). That
is true of any Keplerian-mode install, not something these configs introduce.

## Do NOT install `cartesian-sol-base/`

`cartesian-sol-base/` holds the **release-path** Principia patches: `gravity_model` +
`initial_state`, Cartesian, `NEEDS[NearStarsSystem,SolSystem,!SolQuarterScale]`, state vectors in
the Sol barycentric ICRS frame at `solar_system_epoch = JD 2433282.5`.

Cartesian is all-or-nothing: every body in `FlightGlobals.Bodies` must have an `initial_state`
entry. Stock Kerbol bodies have none, so dropping these into a stock install is a guaranteed
`Log.Fatal`. They are kept here only as the reference for what the real Sol-Configs-based build
emits. It sits outside `GameData/` on purpose.

## The bodies

| Body | Parent | Orbit |
|---|---|---|
| `AlphaCentauriA` | `Sun` | 4.158e16 m (4.395 ly, real distance), circular placeholder |
| `AlphaCentauriB` | `AlphaCentauriA` | a = 23.675 AU, e = 0.5179, i = 79.205° — real ORB6 grade-1 elements |
| `ProximaCen` | `AlphaCentauriA` | a = 8700 AU, e = 0.5 |
| `TRAPPIST1` | `Sun` | 3.848e17 m (40.7 ly), circular placeholder |

`Sun` is the stock star's internal body name, so `referenceBody = Sun` resolves on both stock
Kerbol and Sol-Configs.

α Cen A–B carries real measured elements (Pourbaix & Correia 2017), so the pair forms a genuine
self-gravitating binary under Principia — that is the subsystem the probe is there to watch.

**No Kopernicus barycenter body.** Principia has no barycenter concept; a barycenter body carrying
`M_A + M_B` would enter `FlightGlobals.Bodies` as a real gravitating mass and double-count the
system. B is a child of A instead, and Principia's Jacobi conversion resolves it into the correct
mutual orbit. A barycenter is only needed for a Principia-less Kopernicus 2-body fallback build.

### Caveats

- **Proxima's phase is arbitrary.** Its periastron epoch is unconstrained in the literature
  (`phase_reliable: false` in `db/binary_orbits.json`), so `meanAnomalyAtEpochD = 0` is a
  placeholder. The orbit's shape is measured; "where it is right now" is not.
- **A–B period is 0.9% off catalog.** Catalog a (23.675 AU, from parallax 742.12 mas) combined
  with our GM values gives P = 80.60 yr against the catalogued 79.91 yr. a and GM are kept and the
  period is emergent — Principia integrates from a + GM, not P.
- **Distances are uncompressed.** If KSP map-view or float precision misbehaves at 1e16–1e17 m,
  shrink `semiMajorAxis` on the two `Sun`-referenced bodies (`AlphaCentauriA`, `TRAPPIST1`). The
  A–B binary is a child orbit and is unaffected.
- **SOI is overridden.** `NearStars-Stars-Kopernicus.cfg` ships `sphereOfInfluence = Infinity` on
  every star (valid only for a root body). The orbits patch replaces it: A = 3e15 m (must enclose
  Proxima's 1.952e15 m apoapsis), B = 1e12, Proxima = 1.5e14, TRAPPIST-1 = 1e15.
- **`flightGlobalsIndex` is auto-assigned** by Kopernicus. Fine for a test load; the release build
  must allocate from the 1000+ block per `.claude/skills/kopernicus-cfg/references/file-structure.md`.
- **Textures are 64×64 stand-ins** — flat white sunspots, radial-alpha corona. They exist so the
  star shader does not get a null `noiseMap`, nothing more.

## Regenerating

```sh
python3 .claude/skills/kopernicus-cfg/scripts/emit_kopernicus_cfg.py \
    alpha_centauri_a alpha_centauri_b proxima_cen trappist_1
python3 .claude/skills/principia-cfg/scripts/emit_principia_cfg.py \
    --system alpha_centauri_a --system alpha_centauri_b \
    --system proxima_cen --system trappist_1
python3 scripts/make_placeholder_textures.py
```

That regenerates `NearStars-Stars-Kopernicus.cfg` (as `dist/…/Kopernicus/stars.cfg`),
`cartesian-sol-base/*`, and the textures. The two `NearStars-StockKeplerian-*.cfg` files are
**hand-written** — no emitter produces them, because the release path is Cartesian/Sol. If the DB's
α Cen orbit or GM values change, their numbers have to be recomputed by hand from
`db/binary_orbits.json`.
