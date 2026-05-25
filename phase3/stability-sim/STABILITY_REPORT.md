---
type: synthesis
title: "Phase 3 Stability Report — 10,000 yr N-body Integration"
slug: stability-sim-STABILITY_REPORT
cluster: phase3-procedure
cluster_role: member
status: active
related: [[stability-sim-checklist]], [[stability-sim-context-notes]], [[stability-sim-plan]]
created: 2026-05-21
updated: 2026-05-25
tier: public
---
# Phase 3 Stability Report — 10,000 yr N-body Integration

**Generated:** 2026-05-22
**Integrator:** REBOUND 5.0 WHFast + MEGNO
**Horizon:** 10,000 yr (Principia play window)
**Phase initialisation:** raw.omega_deg from DB where available, Ω and M randomised with deterministic seed (`phase_seed=0`).

## Verdict summary

| System            | Bodies         | MEGNO      | dynamic verdict             | Lyapunov time |
|-------------------|----------------|------------|------------------------------|---------------|
| TRAPPIST-1        | 7 planets      | 1265       | chaotic but Hill-stable     | ≈16 yr        |
| Proxima Cen       | 2 planets      | 2.000      | stable (regular)            | ∞             |
| α Centauri AB     | 2 stars        | 2.001      | stable (regular)            | ∞             |

**All three systems** survive the 10,000-year window with no escapes and bounded eccentricities. TRAPPIST-1 shows formal chaos (Lyapunov-positive trajectory divergence) but the resonant chain keeps every planet Hill-bounded — consistent with Tamayo et al. 2017 / Agol et al. 2021.

## TRAPPIST-1 — 7 planets

| Body | a range (AU) | Δa/a | e range | status |
|------|--------------|------|---------|--------|
| b | 0.01153–0.01154 | 9.4×10⁻⁴ | 0.0004–0.0105 | stable |
| c | 0.01579–0.01581 | 1.2×10⁻³ | 0.0003–0.0114 | stable |
| d | 0.02223–0.02229 | 2.6×10⁻³ | 0.0007–0.0238 | stable |
| e | 0.02920–0.02929 | 3.1×10⁻³ | 0.0002–0.0188 | stable |
| f | 0.03845–0.03855 | 2.6×10⁻³ | 0.0016–0.0158 | stable |
| g | 0.04678–0.04689 | 2.5×10⁻³ | 0.0004–0.0130 | stable |
| h | 0.06175–0.06214 | 6.3×10⁻³ | 0.0007–0.0169 | stable |

- |ΔE/E| = 1.8×10⁻⁸ — excellent energy conservation.
- MEGNO = 1265 at t=10⁴ yr → Lyapunov time ≈ 16 yr. Formal chaos.
- No body escapes; e_max < 0.025 for all seven; a-drift < 0.7% everywhere.
- **Game-play implication:** the canonical Agol+2021 configuration is safe to ship as-is. Players' 10⁴-yr Principia warp will not destabilise the chain.

## Proxima Cen — 2 planets

| Body | a range (AU) | Δa/a | e range | status |
|------|--------------|------|---------|--------|
| d | 0.02881–0.02881 | 6.0×10⁻⁵ | 0–0.0004 | stable |
| b | 0.04848–0.04848 | 4.5×10⁻⁵ | 0–0.0001 | stable |

- Mass type is **Msini** (RV-only detection). Real masses may be larger if inclinations are small; for the recommended values from Suárez Mascareño 2025 the system is regular and well-separated.
- |ΔE/E| = 3.4×10⁻⁹. MEGNO = 2.000 — textbook regular.
- Wide mutual separation (P_b/P_d ≈ 2.18, non-resonant) and tiny eccentricities → no risk in any reasonable horizon.

## α Centauri AB — binary star (no planets)

- Pourbaix & Correia 2017 elements: P=79.91 yr, e=0.518.
- 125 orbital cycles integrated. MEGNO = 2.001, |ΔE/E| = 3.8×10⁻¹².
- Trivially stable (2-body system). Proxima outer orbit (P=547 kyr) excluded — phase unreliable per DB, and only 1.8% of one orbit elapses in 10⁴ yr.

## Hypothetical moons — demonstration

With `hypotheticals/trappist_1.json` containing two moons:

| Moon                       | Parent | a (km) | Hill frac | Outcome |
|----------------------------|--------|--------|-----------|---------|
| TRAPPIST-1 e moon (safe)   | e | 20,000  | 0.23 | bound, stable |
| TRAPPIST-1 g moon (risky)  | g | 110,000 | 0.64 → ∞ | **ejected within 1000 yr**, e → 358,283 |

The risky moon at 0.64 R_Hill exceeds the Domingos et al. 2006 prograde stability limit (~0.5 R_Hill) and is ejected from the system. Its escape also perturbs TRAPPIST-1 g (e_max grows from 0.013 to 0.028) — a small but real cascade visible in the integration.

This confirms the tool resolves the **full star–planets–moons hierarchy** in a single N-body sim: solar tide on the moon, mutual planet perturbations on the moon, and the moon's gravity back on its parent are all tracked.

## How to use

```bash
# Baseline system stability
.venv/bin/python phase3/stability-sim/scripts/run.py --system trappist_1 --years 10000

# With hypothetical moons / extra planets
.venv/bin/python phase3/stability-sim/scripts/run.py \
    --system trappist_1 --years 1000 \
    --hypotheticals phase3/stability-sim/hypotheticals/trappist_1.json \
    --out-dir phase3/stability-sim/results/with_moons
```

Add bodies by editing `hypotheticals/<system>.json`:
```json
{
  "system": "<system_key>",
  "bodies": [
    {"name": "...", "parent": "<star or planet name>", "type": "moon|planet",
     "semi_major_axis_km": ..., "eccentricity": 0, "inclination_deg": 0,
     "mass_kg": ..., "radius_km": ...}
  ]
}
```

Pre-flight Hill-sphere check refuses moons placed outside R_Hill and warns above 0.5 R_Hill.

## Caveats

1. **TRAPPIST-1 eccentricities** come from `raw.eccentricity` (per-planet discovery-paper fits, ≈0.005–0.01). The Agol+2021 joint TTV fit gives tighter constraints (mostly < 0.01 with correlated phases). Using those would slightly reduce the measured chaos.
2. **Initial orbital phases** for null DB fields are randomised. The exact Lyapunov number depends weakly on this seed; the qualitative verdict (chaotic vs regular) does not.
3. **Msini masses** for Proxima planets: stability is robust at the published values, but a true-mass sensitivity sweep is left for follow-up.
4. **Energy error** balloons during ejection events (e.g. the risky moon case reaches |ΔE/E|=1.7×10⁻³). For unstable scenarios, re-run with IAS15 if a precise post-ejection trajectory is needed.
5. **10⁴ yr is short** for true secular evolution of α Cen ABP (outer orbit P = 547 kyr). A 10⁶-yr follow-up could confirm long-term Proxima binding — left for follow-up.

## Files

- `scripts/load.py` — DB JSON → REBOUND loader.
- `scripts/run.py` — Main entry, runs WHFast + MEGNO, writes summary.
- `hypotheticals/*.json` — Per-system extra-body specs.
- `results/*_summary.json` — Per-system numerical summary + verdict.
- `results/*_timeseries.csv` — Sampled (t, body, a, e) for plotting.

## Related

- [checklist](checklist.md) — sibling workspace doc in `stability-sim/`
- [context-notes](context-notes.md) — sibling workspace doc in `stability-sim/`
- [plan](plan.md) — sibling workspace doc in `stability-sim/`
- [phase3 procedure (skill)](../../.agents/skills/nearstars-phase3/SKILL.md) — parent topic this workspace contributes to
