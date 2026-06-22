# Pitfalls — ResearchBodies cfg authoring

All source-cited to JPLRepo/ResearchBodies v1.13.0.0.

## Will throw / silently fail

- **`loadAs = mod` missing** → the mod node's `ONDISCOVERY`/`IGNORELEVELS`
  are silently ignored; only observatory-range keys are read
  (`Database.cs:289`, `403-406`). The single most likely "my patch does
  nothing" cause.
- **`IGNORELEVELS` value not exactly 4 `true`/`false`** → `bool.Parse`
  throws (`Database.cs:258-259`). `1`/`0` are invalid.
- **Cost/reward arrays not exactly 4 ints** → `int.Parse` throws
  (`Database.cs:228,232,236`).

## Behavioral surprises

- **Silence = hidden.** A body with no `IGNORELEVELS` entry is hidden at
  every difficulty (`CelestialBodyInfo.cs:40`). To keep a body visible
  (e.g. a host star) you MUST write `true true true true`.
- **ONDISCOVERY matches by substring `Contains`** (`Database.cs:244`)
  while **IGNORELEVELS matches by exact `==`** (`Database.cs:255`). A
  body name that is a substring of another can get the wrong discovery
  message. Use exact, distinct internal body names.
- **Body name = internal `bodyName`, not `displayName`** — case-sensitive
  (`Database.cs:244,255`). Get it from the Kopernicus `Body { name = }`,
  not the in-game label.
- **Barycenters auto-dropped.** Bodies with `Radius < 100` m are detected
  as Kopernicus barycenters and removed from the discovered-list UI
  (`Database.cs:91,164-173`). **Do not author `ONDISCOVERY`/`IGNORELEVELS`
  for binary/multiple-system barycenter anchors** — wasted lines.

## Dead / legacy — don't author

- **`NOTHING` node** — a stale code comment references it, but the
  "nothing here" strings are hardcoded; no `NOTHING` node is read
  (`Database.cs:268-271`).
- **`IGNORE { body = ... }`** — legacy pre-1.5 path, honored only inside
  `loadAs = mod` nodes and inert in the master file (`Database.cs:304`).
  Prefer `IGNORELEVELS`, which is per-difficulty and clearer.

## MM timing

- RB's own patches run `:FOR[ResearchBodies]`. NearStars guards with
  `:NEEDS[ResearchBodies&Kopernicus]`; if you must override an RB default,
  use `:AFTER[ResearchBodies]`.
