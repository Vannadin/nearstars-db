# Phase 3 Stability Simulation — Context Notes

Append-only log of decisions and reasoning as work proceeds.

---

## 2026-05-22 — Initial scoping

**Decision**: Sim horizon = 10,000 years.
- Rationale: User picked this as the Principia play horizon. Long enough to see chaos in TRAPPIST-1 (~2.4M inner orbits) but cheap to run.
- α Cen AB inner: P=80 yr → 125 cycles. Short for secular but enough to confirm closed Kepler.
- α Cen ABP outer: P=547 kyr → 1.8% of orbit. Effectively static. Not a stability concern at this horizon.

**Decision**: Integrator = WHFast + MEGNO. IAS15 only if WHFast fails.
- WHFast: symplectic, energy-conserving, fast for nearly-Keplerian. Ideal for resonant chains.
- IAS15: high-order non-symplectic; needed if close encounters or strong perturbations. Not expected here.

**Decision**: dt = P_inner / 50.
- For TRAPPIST-1 b: P=1.51 d → dt ≈ 0.03 d ≈ 0.00008 yr.
- 10⁴ yr / dt → ~1.25×10⁸ steps. WHFast can do this in minutes.

**Decision**: Use `curated.physical[recommended=true]` masses.
- TRAPPIST-1: Agol et al. 2021 (TTV-derived, true masses).
- Proxima: Suárez Mascareño 2025 (RV, Msini — using as-is and flagging).
  - For inclination-unknown RV planets, using Msini underestimates the true mass. If true i is small, real mass could be much larger. But there's no transit constraint on Proxima planets, so we have no better number.

**Decision**: For null orbital phases (Ω, ω, M), use 0.
- On 10⁴ yr, the *long-term* stability doesn't depend on phase — chaotic systems blow up regardless of starting phase, stable ones stay stable. We sacrifice the ability to reproduce specific transit times for simplicity.
- TRAPPIST-1: could reconstruct from `tranmid_bjd`. Skip for now — flag as follow-up if results look ambiguous.

**Decision**: Coplanar fallback when inclination is null.
- Proxima b, d: null inclination. Assume coplanar (i=0 for both relative to a chosen ref plane).
- Real i could differ — if i_b ≠ i_d, mutual i could pump eccentricities. Worth flagging as a sensitivity test.

**Decision**: Eccentricity source.
- TRAPPIST-1: `raw.eccentricity` (Agol+2021 individual planet fits — values are 0.002–0.01, tiny).
  - Note: `derived.eccentricity` is forced to 0 in the DB. Suspicious — using `raw` is correct.
- Proxima: `curated.orbital[recommended=true].eccentricity` — e=0 for both b and d in the recommended Suárez Mascareño 2025 fit. RV detection limits.

**Decision**: α Cen AB simulated as 2-body only.
- Outer Proxima orbit excluded (phase_reliable=false in DB, and irrelevant on 10⁴ yr).
- Result is a closed Kepler ellipse — included as a sanity check rather than a stability test.

## 2026-05-22 — Hypothetical bodies feature

**Decision**: Tool doubles as a "moon stability sandbox" via `hypotheticals/{system}.json`.
- Rationale: User wants to evaluate game-design "what if I put a moon here?" before committing to a Kopernicus cfg.
- Schema mirrors `db/systems/*.json` planet entries but adds `parent` (star name or planet name) and `type` (planet / moon).

**Decision**: Hill-sphere pre-flight check before integration.
- For prograde moons, the empirical stable region is ~0.4–0.5 R_Hill (Domingos, Winter & Yokoyama 2006).
- Warn at 0.4 R_Hill, refuse > R_Hill (definitely unbound).
- Reality check for NearStars: Hill radii are *tiny* for close-in M-dwarf planets.
  - TRAPPIST-1 e: R_Hill ≈ 9,400 km → stable moon zone ~3,700 km.
  - Proxima d: R_Hill ≈ 5,400 km → stable zone ~2,200 km (close to planet's surface).
  - Most KSP-style moon configs are likely physically implausible — the tool will make this visible.

**Decision**: Moons go in as plain REBOUND particles with the right hierarchical Keplerian setup.
- REBOUND's `add(primary=...)` lets us specify the parent body directly. No manual Jacobi math.

## 2026-05-22 — Findings from baseline runs

**Finding**: All three systems pass the dynamical-stability test.
- TRAPPIST-1: chaotic (MEGNO=1265, T_L ≈ 16 yr) but Hill-stable. Matches published literature.
- Proxima Cen: regular (MEGNO=2.000), trivially stable.
- α Cen AB: 2-body, MEGNO=2.001, energy error 10⁻¹².

**Finding**: Default-zero initial phases (all planets at conjunction) caused artificially strong chaos in the first TRAPPIST-1 run (MEGNO=1659 vs corrected 1265 — same order, but the un-phased version produced larger e oscillations). Always set Ω/ω/M from DB or randomise — never leave as 0.

**Finding**: REBOUND 5.0 changed the integrator API.
- `sim.add(name=...)` instead of `hash=`.
- `sim.particles["name"]` lookup still works.
- `sim.ri_whfast.safe_mode` is gone — safe_mode is now the WHFast default.

**Finding**: WHFast handles ejection events poorly (energy error 10⁻³). For unstable scenarios the tool's verdict is still right (e diverges, body leaves Hill sphere), but the post-ejection trajectory is not reliable. IAS15 fallback would fix this — not added since the unstable verdict alone is the actionable signal.

**Finding**: TRAPPIST-1 e Hill radius is ~86,000 km — much larger than my early hand calc suggested. The Domingos+2006 0.5 R_Hill stable zone leaves ~43,000 km of room, plenty for Mun-class moons in the KSP sense.

## Open questions / follow-ups
- Should we run a 10⁶-yr secular sweep for α Cen AB to confirm long-term? (Not required by user goal.)
- For Proxima, would a mutual-inclination sensitivity run change the verdict? (TBD after baseline.)
- Retrograde-moon Hill-fraction limit (~0.7 R_Hill) — add when needed.
- IAS15 fallback for unstable scenarios (would make post-ejection trajectory believable).
- Pull eccentricities from Agol+2021 joint TTV fit instead of raw discovery-paper values (would slightly reduce TRAPPIST-1 MEGNO).

## Related

- [phase3 procedure (skill)](../../.agents/skills/nearstars-phase3/SKILL.md) — parent topic this workspace contributes to
