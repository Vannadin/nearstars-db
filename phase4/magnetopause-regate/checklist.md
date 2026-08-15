# Magnetopause re-gate — Alpha Centauri + Proxima Centauri

Recompute every magnetopause in both systems from the 2026-08-14 geometry
methodology, rather than patching the values that predate it. Source of the
recipe: `docs/reference/planetary-magnetosphere-geometry-methodology.md`.

## What changed in the methodology that forces this

1. **Shape policy.** Shue wherever a fitted α exists; Shue by analogy where the
   body class has none; the generalised stock pause (`waist`/`smooth`) only
   where Shue geometrically fails (induced boundaries); a plain sphere where the
   obstacle is sub-Alfvénic (Alfvén wings — no bow shock, no swept tail).
2. **α → cfg mapping is fixed**: `pause_compression = 2^α`,
   `pause_radius = nose · 2^α`, `pause_height_scale = 1.0` (Shue is
   axisymmetric).
3. **Tail is a stated convention**: `L = 150 × nose`, hence
   `pause_extension = 2^α / 150`.
4. **Ganymede precedent**: an embedded moon in sub-Alfvénic flow gets a sphere,
   not a compression/extension pair.

## Bodies in scope

| body | current pause | regime to decide |
|---|---|---|
| Alpha Centauri A b (Polyphemus) | rad 28.2 / comp 1.2 / ext 0.05 / hs 1.1 | gas giant in a stellar wind |
| Pandora (A b III) | rad 2.99 / comp 1.15 / ext 0.6 | embedded moon — Alfvén wing? |
| Cassandra (A b IV) | standoff ~1.1 R_moon, no cfg fields | embedded moon — Alfvén wing? |
| Proxima Cen b | stock `irregular` template | multipolar dynamo in a stellar wind |
| Proxima Cen c | rad 16.84 / comp 1.414 / ext 0.135 / hs 1.0 | ice giant in a stellar wind |
| Dante, Hades, Chaos, Proxima c I | no field | confirm no pause is owed |

## Tasks

- [x] Write `scripts/refs/magnetopause_geometry.py` — one reproducible calculator
      (Chapman–Ferraro nose, α selection, cfg field emission, Alfvén Mach check).
- [x] Register it in `docs/reference/tools.md` + ko mirror.
- [x] Re-derive the Chapman–Ferraro nose for every body from its own board
      inputs; report any that fail to reproduce the recorded value.
- [x] Decide the regime per body, with the Alfvén Mach number computed (not
      asserted) for Pandora and Cassandra.
- [x] Select α per body from the fitted table, labelling fit vs analogy vs
      extrapolation.
- [x] Emit the four cfg fields per body and check them against the SDF renderer.
- [x] Update `phase4/alpha_centauri.yaml` + `phase4/proxima_cen.yaml`: fields,
      evidence, refs, ko mirrors, `process` entry.
- [ ] Update the viewer presets in `scripts/viz/render_belts_bodies.py` so the
      NearStars bodies can be compared against the Sol bodies.
- [x] `./scripts/check.sh` green; commit per logical unit.

## Owner decisions this raises

Recorded in `context-notes.md` as they arise; none may be resolved silently.

## Outcome (2026-08-16)

| body | regime | nose / standoff | alpha | radius | comp | ext | hs |
|---|---|---|---|---|---|---|---|
| Polyphemus | Shue, magnetodisc-inflated | 35.33 R_p (was 23.5) | 0.42 | 47.273 | 1.3379 | 0.0089195 | 1.0 |
| Pandora | Alfven wing, sphere | 3.386 R_moon (was 2.6) | n/a | 3.386 | 1.0 | 1.0 | 1.0 |
| Cassandra | super-Alfvenic, real tail | 1.34 R_moon (was ~1.1) | not set | prose row only | | | |
| Proxima b | Shue, Mercury analog | 1.542 R_p (unchanged) | 0.50 | 2.1813 | 1.4142 | 0.0094281 | 1.0 |
| Proxima c | Shue, ice-giant analogy | 11.942 R_c (unchanged) | 0.58 | 17.852 | 1.4948 | 0.0099657 | 1.0 |

Dante, Hades, Chaos and Proxima c I own no field, so no pause is owed. Dante keeps its
Io-style induced signature through the belt rows, not through a boundary.

Two methodology gaps were closed on the way: Part A gained the magnetodisc inflation
factor, and the tail-length section stopped contradicting itself about whether the
`L = 150 r0` convention had been adopted.

## Still open

- Cassandra is super-Alfvenic and therefore owns a real bow shock and swept tail, but its
  board carries no cfg pause fields at all, only a prose standoff. Giving it the Shue
  four-field set needs an alpha, and no fitted alpha exists for a satellite magnetosphere
  in corotating plasma; Mercury's 0.5 is the obvious analogy but it was fitted in a
  different flow regime. Left for an owner call rather than invented.
- Proxima b keeps `pause_deform 0.1`. Better grounded than before (ROKerbalism gives its
  own mercury model the same value), but the owner removed the analogous term from
  Proxima c on the judgement that multipolar fine structure should not reach the
  magnetopause. Flagged, not resolved.
- The viewer presets in `render_belts_bodies.py` still carry no NearStars bodies, so the
  re-gated shapes cannot be compared against the Sol ones in the belt viewer.
