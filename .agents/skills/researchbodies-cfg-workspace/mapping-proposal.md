# Discoverability category → IGNORELEVELS mapping (proposal)

Phase 4 `identity > discoverability` gives each body a category derived
from its **real detection status**. This table turns the category into an
`IGNORELEVELS` 4-bool tuple (Easy Normal Medium Hard; `true`=visible at
start, `false`=must discover) + the `ONDISCOVERY` message policy.

## Category vocabulary (real-detection driven)

| Category | Real-world meaning | NearStars examples |
|---|---|---|
| `naked_eye` | host star, bright / naked-eye or near | Alpha Cen A/B, 40 Eri A, Fomalhaut |
| `confirmed` | robust, multi-method/multi-epoch confirmed planet | TRAPPIST-1 b–h, 40 Eri A b, Barnard b |
| `candidate` | provisional / single-instrument / imaging candidate | Polyphemus (Alpha Cen A b, JWST/MIRI S1) |
| `disputed` | RV signal contested / stability-predicted | (case-by-case) |
| `fictional` | synthetic body, no real detection | Pandora, Dante, Hades (α Cen A b moons) |

## Tuple grading — three schemes (owner picks)

`E N M H` = Easy Normal Medium Hard.

| Category | A · gentle | B · graded (default) | C · hardcore |
|---|---|---|---|
| `naked_eye` | `T T T T` | `T T T T` | `T T T T` |
| `confirmed` | `T T T T` | `T T T F` | `T T F F` |
| `candidate` | `T F F F` | `F F F F` | `F F F F` |
| `disputed`  | `T F F F` | `F F F F` | `F F F F` |
| `fictional` | `F F F F` | `F F F F` | `F F F F` |

- **A (gentle):** confirmed planets always visible; only candidates/
  fictional require discovery, and even candidates show on Easy. Lowest
  friction, weakest "discovery" identity.
- **B (graded, default):** stars always visible; confirmed planets
  visible except on Hard (rewards the discovery loop at high difficulty);
  candidates/disputed/fictional always discovered. Best matches the "real
  detection status → difficulty" principle while keeping easy games open.
- **C (hardcore):** stars always visible; everything else trends to
  hidden — confirmed planets already need discovery on Medium+. Maximum
  discovery gameplay; most bodies start hidden.

## ONDISCOVERY message policy (independent of grading)

- `candidate` / `disputed`: paraphrase the real detection + cite the paper
  (bibcode from Phase 4 note / DB `sources[]`). Never invent a paper.
- `confirmed`: brief real-detection flavor (method + discovery year ok).
- `fictional`: in-universe flavor, no paper claim.
- `naked_eye`: optional (body never hidden, so message rarely shown).

## DECIDED (2026-06-22), then REVISED same day

First pick = Scheme A (`confirmed = T T T T`). Revised after the owner
understood that the discovery ACTION always works per-body (only the cost/
odds/range knobs are global) — so making confirmed planets visible was
leaving the discovery gameplay on the table. New canonical:

```
naked_eye  T T T T   (stars — always visible)
confirmed  T F F F   (planet — discover by observation; Easy shows it)
candidate  T F F F
disputed   T F F F
fictional  F F F F   (always discover)
```

Stars always visible; every planet discover-by-observation (Easy-visible
concession keeps the difficulty system meaningful); fictional moons always
discovered. confirmed vs candidate now differ only in the ONDISCOVERY
message (solid vs provisional detection). This is the mapping the emitter
implements (`SCHEME` dict).
