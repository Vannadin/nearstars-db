# Phase 4 고증 gate — criteria by axis

From `phase4/SPEC.md §2`. The gate is **hybrid**: quantifiable axes are checked
automatically; perceptual axes are a human checklist. Every decision resolves to
`pass-in-window`, `documented-divergence` (+ `divergence_note` + `refs[]`), or `owner-override`.

| Axis group | Criterion | Automated? | Tool / source of the check |
|---|---|---|---|
| Orbital (`orbit.a` / `.eccentricity` / `.inclination_deg`) | dynamical stability (survives the play window **and** Principia fixed-step fidelity) **and** within Phase 2 error bars | **yes** | `phase3/stability-sim/scripts/run.py --set/--scale`; verdict + numbers in `STABILITY_REPORT.md`; error-bar bound from the DB |
| `bulk.mass` | within M·sin i → true-mass envelope; below the dynamical ceiling | **yes** | isotropic-prior median (×1/sin i); stability ceiling check |
| `bulk.geopotential_j2` / figure | hydrostatic (Radau–Darwin) at the adopted mass/rotation | derived-grounding | `docs/reference/body-figure-methodology.md`; `phase4/figure/values.md` ledger |
| `atmosphere.*` (composition / pressure / temperature) | physical & chemical consistency with the Phase 3 synthesis bounds | checklist | Phase 3 report; retention / cosmic-shoreline reasoning |
| `appearance.*` (color / banding / haze / aurora / rings) | blackbody / SED plausibility + the Phase 3 color window | checklist | Phase 3 color window; `docs/reference/*-color-methodology.md` |
| `magnetism.*` / `environment.*` | consistency with the stellar-wind / dynamo synthesis layer | checklist / derived-grounding | `phase3/stellar_wind_synthesis`; `docs/reference/planetary-dynamo-scaling.md` |
| Fiction body (class **D**) | Hill-bound (moon) + HZ-stable (host) + composition plausibility | **yes** (stability) + checklist (composition) | stability sim + composition checklist — **not** `culture`/`classification` |

## Verdict decision — three verdicts

Distinguish divergence **from a paper** vs **from a non-paper baseline** — never collapse them.

- **`pass-in-window`** — value inside a Phase 3 error bar, a `## Canonical
  alternatives` reading, or a physical bound. A choice among Phase 3 alternatives
  is pass-in-window by construction (Phase 3 already vetted those readings).
- **`documented-divergence`** — the value departs from a **paper-cited value or
  model** (the science). `divergence_note` (required) states the literature value,
  the magnitude, and why; and `refs[]` (required) names the paper(s) diverged from.
  The test: *is there a paper whose value/model we are contradicting?*
- **`owner-override`** — the value departs from a **non-paper baseline**: a prior
  art-direction choice, an AI-synthesized Phase 3 default, canon ([GAME]/[FILM]/wiki),
  or an analogy / heuristic. Put the rationale in the **`narrative`** — NOT in a
  `divergence_note` (that field is paper-divergence-only). e.g. "film color over an
  AI-default color", "art-forward turbulence", "canon ranking film>game" are all
  `owner-override`, not `documented-divergence`.

`divergence_note` may appear **iff** verdict is `documented-divergence`.

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
