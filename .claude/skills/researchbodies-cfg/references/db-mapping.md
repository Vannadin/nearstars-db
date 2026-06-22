# Phase 4 discoverability → ResearchBodies cfg mapping

The discoverability axis lives in Phase 4 (`identity > discoverability`,
`phase4/SPEC.md`). Each body's category is driven by its **real detection
status**; this file defines how a category becomes an `IGNORELEVELS` tuple
+ an `ONDISCOVERY` message. The emitter (`scripts/emit_researchbodies_cfg.py`)
implements exactly this table.

## Category → IGNORELEVELS (canonical, revised 2026-06-22)

`E N M H` = Easy Normal Medium Hard; `T`=visible at start, `F`=must discover.

| Category | E N M H | Rationale |
|---|---|---|
| `naked_eye` | `T T T T` | host stars — naked-eye visible, never hidden |
| `confirmed` | `T F F F` | confirmed planet — discover by observation; Easy shows it |
| `candidate` | `T F F F` | provisional / imaging candidate — same |
| `disputed` | `T F F F` | contested RV / stability-predicted — same |
| `fictional` | `F F F F` | synthetic body, no real detection — always discover |

**Decision history.** Originally Scheme A (`confirmed = T T T T`, planets
always visible). Revised 2026-06-22 once the owner saw that "discovering by
observation" is the whole point of installing RB — confirmed planets now
also discover-by-observation, only differing from candidates in their
ONDISCOVERY message (solid vs provisional detection). Stars stay always
visible; fictional moons stay always-discover. The original A/B/C menu is
in the workspace `mapping-proposal.md`.

## Phase 4 input schema (what the emitter reads)

Add a `discoverability:` list to a `phase4/<system>.yaml`. One entry per
body that should get a ResearchBodies patch:

```yaml
discoverability:
  - body: AlphaCentauriA          # EXACT internal Kopernicus body name
    category: naked_eye
  - body: Polyphemus              # in-game name = Kopernicus Body { name }
    category: candidate
    message: >
      JWST/MIRI 15.5 um direct imaging resolves a faint companion to
      Alpha Centauri A — the candidate "S1".
    ref: "2025arXiv250803812S"    # bibcode for the detection (candidate/disputed)
  - body: Pandora
    category: fictional
    message: First survey of the gas giant's habitable moon.
```

- `body` (required) — the exact Kopernicus internal body name (matches
  `IGNORELEVELS` by `==` and `ONDISCOVERY` by substring). NOT the
  `displayName`. Barycenter anchors (radius<100m) must be omitted.
- `category` (required) — one of the five above.
- `message` (optional) — `ONDISCOVERY` text. If omitted, RB shows its
  generic default; the emitter only writes an `ONDISCOVERY` line when a
  message is given.
- `ref` (optional but expected for `candidate`/`disputed`) — bibcode of
  the real detection paper, sourced from the body's DB `sources[]` or the
  Phase 4 discoverability note. **Never invent one.** The emitter appends
  it to the message if not already present.

## Body without a discoverability entry

The emitter does **not** fabricate one. RB's default (no `IGNORELEVELS`
entry) = hidden at all difficulties. So an un-authored NearStars body is
silently discover-only — acceptable, but author the host stars explicitly
(`naked_eye → T T T T`) so they are never hidden.

## ONDISCOVERY message policy

- `candidate`/`disputed`: paraphrase the real detection, name the paper.
- `confirmed`: brief real-detection flavor (method, year).
- `fictional`: in-universe flavor, no paper claim.
- `naked_eye`: usually omit (the body is never hidden).
