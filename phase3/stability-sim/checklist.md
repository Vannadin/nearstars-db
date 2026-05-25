# Phase 3 Stability Simulation — Checklist

## Setup
- [ ] Create `.venv` at project root with Python 3.9
- [ ] Install rebound + numpy in venv
- [ ] Confirm `python -c "import rebound"` works
- [ ] Add `.venv/` to `.gitignore` if not already

## Loader
- [ ] `scripts/load_system.py` — reads `db/systems/*.json` → REBOUND `Simulation`
- [ ] Handle TRAPPIST-1: 7 planets, recommended masses from Agol+2021
- [ ] Handle Proxima Cen: 2 planets, Msini, null inclination → assume coplanar
- [ ] Handle α Cen: 2 stars (AB binary) from `binary_orbit.orbits[0]`
- [ ] Use heliocentric / barycentric Jacobi coords consistently
- [ ] Unit check: km, s internally; convert to AU/yr for REBOUND

## Integration
- [ ] `scripts/run_sim.py` — WHFast, dt = P_inner / 50
- [ ] Add MEGNO via `sim.init_megno()`
- [ ] Output: 1000 snapshots over 10⁴ yr (every 10 yr)
- [ ] Track a, e, MEGNO, energy at each snapshot
- [ ] Save `results/{system}_summary.json` + `results/{system}_timeseries.csv`

## Run
- [ ] TRAPPIST-1 (~most expensive — short inner period)
- [ ] Proxima Cen
- [ ] α Cen AB

## Report
- [ ] `STABILITY_REPORT.md` with per-system verdict
- [ ] Korean mirror at `ko/phase3/stability-sim/STABILITY_REPORT.md`
- [ ] Flag any system that fails the success criteria
- [ ] Commit to git with semantic message

## Hypothetical bodies extension
- [ ] Schema: `hypotheticals/{system}.json` with parent/type/a/e/i/mass/radius
- [ ] Pre-flight Hill sphere check (warn at 0.4 R_Hill, refuse > R_Hill)
- [ ] Loader accepts moons (parent=planet) and extra planets (parent=star)
- [ ] Sim adds them as particles in the right hierarchy
- [ ] Report includes "moon bound at sim end?" per moon
- [ ] Example: TRAPPIST-1 e with a Luna-mass moon at 0.3 R_Hill — verify it survives
- [ ] Example: same moon at 0.6 R_Hill — verify the tool flags it as unstable

## Verification
- [ ] Sanity check: energy conservation < 1e-6 for WHFast
- [ ] Sanity check: MEGNO ≈ 2 for known-stable systems
- [ ] Compare TRAPPIST-1 result to Agol+2021's reported stability claim

## Related

- [phase3 procedure (skill)](../../.agents/skills/nearstars-phase3/SKILL.md) — parent topic this workspace contributes to
