<!-- 엔진 구조 지도 — 어느 파일이 무슨 일을 하고, 왜 그렇게 갈렸는지 -->
# The engine

Derives a body's **physical state** from declared inputs. Not a config file for whatever
renders it — an adapter does that, and does not exist yet. The reasoning behind the split,
and behind the rules the code enforces, is in
[derivation-discipline](../docs/reference/derivation-discipline.md).

```
declared inputs  ──▶  recipes  ──▶  physical state  ──▶  (adapter)  ──▶  KSP cfg
   bodies/*.yaml       *.py          BodyState              not built        phase4 → emit
```

## Layout

| file | role |
|---|---|
| `chain.yaml` | **the declaration.** 44 nodes, 161 edges, four edge kinds, one coupled core. Nothing computes; this says what depends on what. |
| `bindings.yaml` | **the backflow.** Which node should produce each already-shipped field, which shipped fields derive from others, what consumes them. |
| `graph.py` | ordering and cycle rules. **The only place they live** — see below. |
| `chain.py` | validates `chain.yaml`; answers `affects` / `needs` / `gaps`. |
| `backflow.py` | validates `bindings.yaml`; answers `impact` / `after` / `field` / `debt`. |
| `payload.py` | the return contract. A recipe returns a state, not a number. |
| `registry.py` | binds a node name to the function that computes it. |
| `state.py` | one body's `BodyState`: declared inputs plus recorded `Result`s. |
| `run.py` | executes the graph over a body, then compares against already-shipped values. |
| `dynamo.py` | the giant-dynamo recipe. |
| `eos.py` | equations of state, one per material, every constant carrying its source. |
| `interior.py` | the interior solver: shoots on central pressure, integrates the layers. |
| `mass_radius.py` | mass to radius and density, reading its radius from `interior.py`. |
| `bodies/*.yaml` | declared inputs per body, plus `expected` — the shipped values the engine must reproduce. |
| `build_graph_page.py` | generates `chain-explorer.html` from the two declarations. |

```
python3 engine/run.py bodies/alpha_centauri_a_b.yaml     엔진을 돌린다
python3 engine/chain.py check                            선언 무결성
python3 engine/backflow.py impact body_figure            무엇이 되열리나
```

## What building the runner found

The runner is the piece that had been missing: `chain.py` knew the order and `dynamo.py`
knew the arithmetic, and nothing connected them, so the graph existed only as a picture.
Connecting them surfaced two things immediately.

**The validator was looking for the wrong kind of cycle.** It followed `requires` only, so
every loop passing through a `selects` edge was invisible to it. A `selects` edge chooses
which model applies; if the choice's consequences come back round and change the choice,
that is a fixed point exactly like a numeric one. Topological sort refused to run and that
is how it came out.

**The six declared cycles are one cycle.** Following `requires` and `selects` together
yields a single strongly-connected component of fifteen nodes, and all six named cycles are
sub-loops of it. `body_class`, `moon_energy_budget` and `spin_axis_inclination` were in no
declaration at all. The six names are still worth keeping — each names a physical mechanism
— but the runner iterates the core as one block, because sub-loops trade values with each
other and iterating them separately does not converge.

`interior_structure` was declared in two of those cycles but sat outside the core, because
its edges were still `status: gap`. On 2026-08-25 the layer integration landed and started
producing the radius, which turned the edge into `requires`, and the node joined exactly as
predicted. The core is sixteen nodes now.

**Class tables are not ordering constraints.** A lookup needs its key, not a turn in the
sequence. Counting them as computation steps invents loops that are not there — with them
in, the undeclared-cycle count goes from one to twelve. They are excluded from ordering and
consulted whenever asked.

## Rules the code holds

- **Ordering and cycle rules live in `graph.py` only.** Two copies drift, and these two had:
  the validator passed a graph the runner could not execute. `chain.py` and `run.py` both
  call it now.
- **A missing recipe is a state, not an error.** 27 of 28 nodes have no implementation yet;
  the runner counts them and keeps going, so the runner is usable from the first recipe
  rather than the twenty-eighth.
- **Out of domain is a returned value.** It occupies `results` like any other outcome and
  is reported separately from "not computed".
- **Shipped values are constraints, not inputs.** `bodies/*.yaml` carries `expected:` with
  a source; the engine never reads it to compute, only to be checked against. A mismatch
  means the engine is wrong or the board is wrong, and both are worth finding.

## Where it stands

Three recipes of 28.

`dynamo_giant` reproduces the shipped Alpha Centauri A b field to 0.1 % on the polar
component and 1.4 % on the equatorial, the first time a board value had been regenerated
rather than trusted.

`interior_layers` integrates hydrostatic equilibrium with published equations of state and
reproduces Earth's C/MR² to 0.3 % and its radius to 0.3 % from mass and core mass fraction
alone. The uniform-layer model it replaced was 4.8 % out on Earth, and it needed layer
densities handed to it for every body except Earth. Two lookup tables went away with it:
`LAYER_DENSITY` here and `COMPOSITION` in `mass_radius.py`.

`mass_radius_relation` now reads its rocky radius, and its pure-iron density gate, off that
integration instead of off a scaling table derived from prose.

## What it costs, and what the gate protects

The rocky and icy anchors solve in under a second each; the gas giants in 5–20 s. An ice
giant is the exception: one Uranus solve is about 13 minutes (2026-08-28), not because the
hot-water equation of state is slow but because the pressure shoot cannot converge on a
mass staircase and runs to its iteration cap — measured in `speed-context-notes.md`. So the
Uranus anchor is **frozen** in `ice_giant_anchor.json` and `scripts/check.sh` runs
`test_ice_giant.py`, which re-integrates the frozen converged point once and fingerprints
the shooting path; either drifting fails the gate and asks for `--refresh`. The gate says
what it skips.
