# Phase 3 Stability Simulation — Plan

## Goal

Verify that the planetary systems we've curated in `db/systems/` remain dynamically stable over the Principia-relevant timescale (~10,000 years). Catch any obviously unstable configurations *before* they ship into Kopernicus/Principia cfg.

## Scope

Systems with curated Phase 3 data and ≥1 planet:

| System          | Bodies                                        | Notes |
|-----------------|-----------------------------------------------|-------|
| TRAPPIST-1      | 1 star + 7 planets (b–h)                      | Tight resonant chain — highest stability risk. |
| Proxima Cen     | 1 star + 2 planets (b, d)                     | Wide-spaced RV planets; inclination unknown. |
| α Cen A+B+Prox  | 3 stars, 0 planets                            | Trivial 2-body + outer hierarchical. Included for completeness; expect quiet. |

α Cen ABP triple: outer Proxima orbit P=547,000 yr → 10⁴ yr = 1.8% of orbit → effectively static. We integrate the AB inner orbit (P=80 yr → 125 cycles).

## Method

- **Integrator**: REBOUND WHFast (symplectic, energy-conserving for nearly-Keplerian systems). Fall back to IAS15 if WHFast can't handle close encounters (not expected for these systems).
- **Timespan**: 10,000 years.
- **Chaos indicator**: MEGNO integrated over the same window. MEGNO ≈ 2 → regular; MEGNO ≫ 2 (diverging) → chaotic.
- **Diagnostics tracked per body**: a_min, a_max, e_min, e_max, a-drift, energy error (dE/E).

## Inputs

Read from `db/systems/*.json`:
- Star: `principia.gravitational_parameter_km3_s2` → mass via μ/G.
- Planet: `curated.physical[recommended=true].true_mass_mearth` (TRAPPIST-1) or `mass_mearth` Msini (Proxima — used as-is, flagged).
- Orbital: `curated.orbital.semi_major_axis_au`, eccentricity from `raw.eccentricity` (TRAPPIST-1: Agol 2021) or curated orbital (Proxima).
- Inclination: `curated.orbital.inclination_deg` if present; else 0 (coplanar assumption).
- Phases (Ω, ω, M): mostly null in DB — use 0 with note. For TRAPPIST-1 we *could* reconstruct from `tranmid_bjd`, but for a stability check phase doesn't matter on 10⁴ yr.

## Outputs

- `phase3/stability-sim/results/{system}_summary.json` — per-body min/max/drift, MEGNO, dE.
- `phase3/stability-sim/results/{system}_timeseries.csv` — sampled e(t), a(t) for plotting.
- `phase3/stability-sim/STABILITY_REPORT.md` — human-readable verdict.

## Success criteria

For each system:
1. Integration completes without unbounded eccentricity growth (e_max < 0.9).
2. No body escapes (a_max < 10× initial a).
3. MEGNO < 5 by the end (regular orbits typically settle to ~2).
4. Relative energy error |dE/E| < 1e-6 (WHFast).

If any system fails, flag it and recommend a longer IAS15 follow-up.

## Hypothetical bodies (moons / extra planets)

The tool doubles as a "what if I add a moon" sandbox for KSP planet-pack design.

- **Input**: `hypotheticals.json` next to the system spec, listing extra bodies with a `parent` field.
  - `parent: "TRAPPIST-1"` (or any star) → extra planet.
  - `parent: "TRAPPIST-1 e"` (or any planet) → moon of that planet.
- **Hill sphere check (pre-flight)**: compute R_Hill of the parent and warn if `a_moon > 0.4 R_Hill` (prograde Domingos+2006 limit). Refuse to run if `a_moon > R_Hill` outright.
- **Integration**: moon added as a regular REBOUND particle. WHFast handles the hierarchical case fine as long as dt < 1/50 of the moon's orbital period.
- **Stability criteria for moons**: same as planets, plus a separation criterion (moon must remain bound to its parent — Jacobi energy < 0).

### Workflow for moon-stability check
1. User edits `phase3/stability-sim/hypotheticals/{system}.json`.
2. Run `python scripts/run_sim.py --system trappist_1 --with-hypotheticals`.
3. Report flags whether moon survived, planet orbits were perturbed, and Hill-sphere fraction at sim end.

## Out of scope

- Stellar tides / general relativity (small for these systems on 10⁴ yr).
- α Cen AB → planet stability windows (no planets in DB).
- TRAPPIST-1 TTV reconstruction from transit times (overkill for game-play horizon).
- Hypothetical retrograde moons (different Hill limit — skip until requested).

## Related

- [phase3 procedure (skill)](../../.claude/skills/nearstars-phase3/SKILL.md) — parent topic this workspace contributes to
