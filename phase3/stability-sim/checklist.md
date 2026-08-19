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


## Validation suite promotion (2026-08-18)

Promote the one-off α Cen validation runs into a manifest-driven suite that runs
on every system, and put Proxima Cen through it.

- [x] `validation-manifest.yaml` — per-system matrix params + page prose
- [x] `scripts/validate_orbits.py` — build cells, run, render, generate pages
- [x] Long horizon derived from `long_inner_orbits` (orbits, not years); standard
      set to a round 1e8 innermost orbits, satellite hierarchy keeps 10⁴ yr
- [x] A cell short of its manifest horizon reports `[stale]` and re-runs
- [x] Moon mass auto-folded into the parent for the planetary rows
- [x] Migrate the four existing α Cen result dirs into the generated layout
- [x] Regenerate the α Cen page from the manifest — matrix numbers unchanged
- [x] Validation index page + link from the orbit-viewer gallery and tools
- [x] STABILITY_REPORT.md + `docs/reference/tools.md` (+ ko mirror)
- [x] `--jobs N` parallel cells (one core each; REBOUND is single-threaded per run)
- [x] Plots rendered in both palettes; pages swap them via `<picture>` on `prefers-color-scheme`
- [x] Light/dark verified by headless capture on both pages, no console errors
- [x] `./scripts/check.sh` clean
- [ ] **Run on the desktop:** `validate_orbits.py --systems proxima_cen`
      (planets_leapfrog ~30 s, planets_accurate 1.4×10⁶ yr ≈ 6.6 h)
- [ ] **Run on the desktop:** α Cen `--cells planets_accurate` to the new
      1e8-orbit standard (1.92×10⁸ yr ≈ 7 h; the stored 10⁸ yr run is 5.2×10⁷ orbits)
- [ ] Re-run `validate_orbits.py --pages-only` afterwards to refresh both pages

## J2 force in C (handoff, 2026-08-19)

- [x] Measure why the moon leapfrog cell is slow — J2 Python callback, 69x
- [x] `scripts/j2force.c` + `scripts/j2c.py` written and compiling
- [x] Gated behind `STAB_J2_C=1`; the default path is unchanged
- [x] **Fix the stride bug**: `ctypes.sizeof(rebound.Particle)` passed into
      `ns_j2_setup`, array walked by that stride in bytes
- [x] Cross-check against the Python force — `scripts/verify_j2c.py`: leapfrog 5 yr
      and ias15+MEGNO 2 yr, every particle's x/y/z/vx/vy/vz **bitwise identical**
      (`-ffp-contract=off`, no double axis normalization); 27.6x / 9.2x measured
- [x] Enabled by default (`STAB_J2_C=0` forces the Python callback)
- [ ] Then re-run the satellite leapfrog cells — 10 h becomes ~10 min

Do not install `reboundx`: it pins `rebound<5` and downgrades the engine.

Both queued cells are independent, so one `validate_orbits.py --jobs 2` covers them in
~7 h wall clock rather than ~14 h serial.

Note: `STABILITY_REPORT.md` lives under `phase3/`, outside the `ko/` mirror scope
(`docs/`, `plans/`, root `README.md`, `CONVENTIONS.md`), so it has no Korean mirror.

## Related

- [phase3 procedure (skill)](../../.claude/skills/nearstars-phase3/SKILL.md) — parent topic this workspace contributes to
