# Phase 4 고증 gate — criteria by axis

From `phase4/SPEC.md §2`. The gate is **hybrid**: quantifiable axes are checked
automatically; perceptual axes are a human checklist. Every decision resolves to
`pass-in-window` or `documented-divergence` (+ a `divergence_note`).

| Axis group | Criterion | Automated? | Tool / source of the check |
|---|---|---|---|
| Orbital (`orbit.a` / `.eccentricity` / `.inclination_deg`) | dynamical stability (survives the play window **and** Principia fixed-step fidelity) **and** within Phase 2 error bars | **yes** | `phase3/stability-sim/scripts/run.py --set/--scale`; verdict + numbers in `STABILITY_REPORT.md`; error-bar bound from the DB |
| `bulk.mass` | within M·sin i → true-mass envelope; below the dynamical ceiling | **yes** | isotropic-prior median (×1/sin i); stability ceiling check |
| `bulk.geopotential_j2` / figure | hydrostatic (Radau–Darwin) at the adopted mass/rotation | derived-grounding | `docs/reference/body-figure-methodology.md`; `phase4/figure/values.md` ledger |
| `atmosphere.*` (composition / pressure / temperature) | physical & chemical consistency with the Phase 3 synthesis bounds | checklist | Phase 3 report; retention / cosmic-shoreline reasoning |
| `appearance.*` (color / banding / haze / aurora / rings) | blackbody / SED plausibility + the Phase 3 color window | checklist | Phase 3 color window; `docs/reference/*-color-methodology.md` |
| `magnetism.*` / `environment.*` | consistency with the stellar-wind / dynamo synthesis layer | checklist / derived-grounding | `phase3/stellar_wind_synthesis`; `docs/reference/planetary-dynamo-scaling.md` |
| Fiction body (class **D**) | Hill-bound (moon) + HZ-stable (host) + composition plausibility | **yes** (stability) + checklist (composition) | stability sim + composition checklist — **not** `culture`/`classification` |

## Verdict decision

- **`pass-in-window`** — value inside a Phase 3 error bar, a `## Canonical
  alternatives` reading, or a physical bound. A choice among Phase 3 alternatives
  is pass-in-window by construction (Phase 3 already vetted those readings).
- **`documented-divergence`** — outside the window but justified (gameplay /
  engine / film canon). The `divergence_note` must state: the canonical value,
  the magnitude of the departure, and why. Tells that a "pass" is really a
  divergence: "owner adopted below the visibility threshold", "film color over
  physical color", "art-forward" — if the value leaves the Phase 3 default,
  it is a divergence, full stop.

## Criterion vocabulary

Prefer the SPEC §2 set: `stability`, `error-bar`, `dynamical-ceiling`,
`observation`, `classification`, `derived-grounding`, `hill-stability`,
`composition`, `culture` (identity/naming only — never a physical-value gate).
Keep the list tight so a future strict validator can check it.

## The orbit-gate seam (important)

The transient `run.py` flags (`--set`, `--scale`, `--mass-incl-deg`) are
**experiments, not the source of truth**. The chosen value is persisted into the
board row (`fields[].value`); the process/scan tables live in
`STABILITY_REPORT.md`. Never leave the "truth" only in a sim result directory.
