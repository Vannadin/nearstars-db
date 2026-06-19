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

## 2026-06-18 — Barnard's Star re-verification + Msini→true-mass boundary scan

**Context**: The shipped `results/barnards_star_summary.json` predated the F1 recovery
that added planets c, d, e — it held only Barnard b. The DB now carries the 4-planet
system (Basant+2025 / González Hernández+2024): d 0.0188 AU, b 0.0229, c 0.0274,
e 0.0381 AU; all sub-Earth M·sin i (0.19–0.34 M⊕); star 0.162 M☉. A genuinely packed
compact system — the interesting stability case.

**Method — re-verification**: rebuild via the standard planetary loader (`run.py
--system barnards_star`, 10⁴ yr, WHFast+MEGNO, phase_seed=0) so the canonical summary
matches the suite's uniform policy.

**Method — boundary scan** (`scripts/barnard_inclination_scan.py`): all four are RV
detections → the DB masses are minima. True mass M = M_min / sin i. Assuming the system
is **coplanar** (one shared i), lowering i scales every planet mass by 1/sin(i),
strengthening the mutual perturbations. Walk i down and find the first inclination that
fails the suite's instability test (e_max ≥ 0.9 or a_max/a_min ≥ 10×, early-stopped at
e ≥ 0.95). That i_crit is a **dynamical upper limit on the true masses / lower limit on
i** — the standard packed-RV-system argument.

**Implementation choice**: scale masses *after* `build` (orbits/phases fixed at build
time; only m changes), so every inclination shares identical initial conditions — a
clean one-variable scan. Grid 90°→6°.

**Known limitation (follow-up, not done in first pass)**: single phase realization
(seed=0). A chaotic boundary is phase-sensitive; a multi-seed survival-fraction
refinement near i_crit is the rigorous version. Also WHFast can spuriously eject during
close encounters (the AU Mic lesson) — any inclination flagged unstable here must be
re-confirmed with IAS15 before it goes in a report or paper.

**Findings (2026-06-18)**:
- **Nominal (i=90°, 4 planets)**: chaotic (MEGNO 248, Lyapunov ≈ 81 yr) but Hill-stable
  on 10⁴ yr — same category as TRAPPIST-1. a-drift ~10⁻³, e calm (≤0.11). The shipped
  1-planet summary is now replaced by the 4-planet run.
- **WHFast artifact caught by TRACE** (textbook §10 case): the WHFast screen reported
  i=20° disrupting (Barnard b ejecting @ 8475 yr, e_max 0.96). TRACE re-verifies i=20°
  as *stable* (e_max 0.11) — the WHFast "ejection" was a spurious fixed-step
  close-encounter artifact (AU Mic failure mode). Had I reported the WHFast boundary
  (i_crit≈20–30°, M≲0.7 M⊕) it would have been WRONG and too restrictive.
- **True boundary (TRACE)**: i_crit ≈ 19° (bracket 18–20°). Stable for true masses up to
  ≈3× minimum (heaviest ≲1 M⊕); disrupts only near face-on. Prior P(i<19°)=1−cos19°≈5.5%,
  so dynamics exclude only ~5% of orientations — a real but weak bound that does NOT
  exclude the nominal system.
- Results: `results/barnards_star_inclination_scan{,_trace,_trace_low}.json`; report
  section added under STABILITY_REPORT.md.
- **Literature cross-check (independent validation)**: both discovery papers ran their
  own SPOCK+REBOUND stability analysis over 10⁹ orbits and reached the SAME ×3 ceiling —
  González Hernández et al. 2024 (arXiv 2410.00569): m=3·Msini ↔ i=19.5°, stable; Basant
  et al. 2025 (arXiv 2503.08095): stable for masses up to ×3, i=20–90°. Our i_crit≈19°/×3
  from a 10⁴-yr WHFast→TRACE screen reproduces their ~19.5–20°/×3 from a 6-Myr ML ensemble.
  Same league as the TRAPPIST-1 vs Agol+2021 check. Caveat: Basant flags strong
  e-sensitivity (<80% stable if any e>0.02); we used the DB β-prior e (0.03–0.08), papers
  favor e<0.02 — so the exact boundary is conditional on the adopted eccentricities.

**Decision (2026-06-18) — adopt the median true mass (×1.155, i=60°)**: for downstream
game/cfg use the planets get their *median* true mass, not the bare RV minimum. M·sin i
is a minimum; for isotropic orbital orientation the median inclination is 60° (cos i
uniform → median cos i = 0.5), so the median true mass = M·sin i / sin 60° = ×1.155. NB
this is NOT the arithmetic midpoint of [×1, ×3]: ×3 is the instability boundary, not a
physical maximum (true max → ∞ as i→0), and the mass-factor distribution is sharply
skewed toward edge-on — P(true mass ≤ ×f) = √(1−1/f²), so ×2 is the ~87th percentile,
not the median. Median masses: d 0.304, b 0.345, c 0.387, e 0.223 M⊕. Verdict at this
mass: identical to nominal — chaotic (MEGNO 349, Lyapunov ~58 yr) but Hill-stable, calm,
well below the ×3 boundary.
- **This is a downstream (cfg/Phase-3) assumption, NOT a DB edit.** The DB keeps M·sin i
  (strictly measurement; no assumed defaults — see project_nearstars_db_principle). The
  ×1.155 lives wherever the cfg mass is finally assigned.
- Reproducible via `run.py --mass-incl-deg 60` (general flag for any RV planetary system;
  writes `{system}_i{deg}_*` so the canonical edge-on summary is preserved). Output:
  `results/barnards_star_i60_summary.json` + `_timeseries.csv`.

(Paper note: this would have fed Pillar 3 of `plans/paper-scoping.md`, now PARKED — kept
as ordinary stability-suite work, no paper framing.)

## 2026-06-18 — fixed-step eccentricity finding + `--ecc` override

**`--ecc` override added** (run.py/load.py): set every planet's eccentricity at run
time (DB unchanged) — a downstream adopted-config knob like `--mass-incl-deg` / acen's
`--acen-e`. Threaded through `build → build_planetary_system → _planet_orbital`.

**Finding — β-prior is fixed-step-fragile; low-e is the playable config.** Principia
integrates bodies fixed-step (Quinlan–Tremaine 10 min). WHFast (same class) at the DB
β-prior e (0.03–0.08) blew up over **1 Myr** (|dE/E|=6.2, e→10²–10³). At low-e
(`--ecc 0.015`, Basant favored <0.02) WHFast 1 Myr is **clean** (|dE/E|=9.5e-9, MEGNO
8.2, e_max≤0.031, calm). TRACE keeps β-prior bounded → the blow-up is fixed-step
numerics, not physics. + 10 Gyr survival argues for the low-e architecture.
→ staged as a **Phase 4 candidate** (`phase4/barnards_star.yaml`); DB/viewer/cfg
untouched. Run artifact: `results/_phase4_lowe/` (not committed; reproducible via the
documented override command).

## 2026-06-19 — generalized the element override (--ecc/--ecc-scale → --set/--scale)

The one-off `--ecc` / `--ecc-scale` flags were ad-hoc. Replaced with a single general
mechanism: repeatable **`--set BODY.FIELD=VALUE`** / **`--scale BODY.FIELD=FACTOR`**,
applied strictly in command-line order. BODY = planet name or `*`; FIELD ∈ e | a_au |
inc_deg | omega_deg | Omega_deg | M_deg | mass_mearth (natural units, converted to sim
units in `build_planetary_system`). Any element of any planet is now controllable
without bespoke flags; fields/bodies are validated up front. DB still untouched
(run-time only). `--ecc 0.015` → `--set '*.e=0.015'`; `--ecc-scale 0.5` → `--scale
'*.e=0.5'`. `--mass-incl-deg` kept (semantic 1/sin i + output-naming sugar).

## 2026-06-19 — Polyphemus named-moon orbits (Avatar: The Game), stability-designed

Set up the orbits of Polyphemus's 5 *named* moons (Dante, Hades, Pandora, Cassandra,
Chaos) from *Avatar: The Game* canon. The wiki gives **no a/e/period** for any moon
(only Pandora is Kepler-derivable from its tidal-lock 27 h day → a = 225,000 km), so the
elements are **designed** under physical bounds (Roche inner edge ~94,000 km, 0.5 R_Hill
prograde outer ~5e6 km, canon radial ordering) and verified with IAS15.

**Finding — the canonical Hades-grazes-Dante orbit is dynamically lethal.** Canon: Hades
(2nd moon) has an elliptical orbit "bringing it close to Dante" (innermost), tidal-heating
it >900 K. Taken literally (Hades e=0.30, periapsis crossing Dante's apoapsis) → Hades
**ejects within 100 yr** (scatters off Dante, e→2.6e4, Hill-frac 3.4; IAS15). Even e=0.13
with comparable-mass moons mutually pumps Dante to e=0.28 and still ejects (Lyapunov 0.2
yr — violently chaotic inner pair). **Fix (physical):** tidal heating comes from a
*maintained* eccentricity (Io's forced e is only 0.0041 yet it is the most volcanic body
known), not orbit crossing. So Dante/Hades made small inner **moonlets** (8e21 / 5e21 kg,
like Jupiter's Metis/Adrastea coexisting with Io) at e=0.01 / 0.05, Hades a=135,000 km
(period ratio 1.57 to Dante, between 3:2 and 5:3). Result: **MEGNO 1.944 (regular,
non-chaotic), |dE/E|=0, all 5 moons Hill-bound and calm over 100 yr** (Hades holds
e≈0.05, ample for >900 K). **1000-yr confirmation: CHAOTIC_BUT_HILL_STABLE** (MEGNO 15.5,
Lyapunov 148 yr — weak chaos, but all 5 moons stay bound and calm, Hades holds e≈0.05, no
ejection; same ship-safe class as Barnard/TRAPPIST-1). `results/_moons_alpha_centauri`.

**Resonance scan** (`scripts/resonance_scan.py` → `results/_moons_resonance_scan.md`):
stepped Hades a 125k→172.5k (Dante/Pandora fixed, IAS15 40 yr) to map the resonance
landscape. The safe zone is the **low-a gaps (127.5k–135k, MEGNO≈2)**; strong resonances
*backfire* — Hades:Dante 2:1 (157.5k) sits in an **ejection** zone because it overlaps
Pandora's 5:3, and the whole 140k–170k band is chaotic→ejecting (massive Pandora disrupts
every strong MMR via resonance overlap). So a Galilean-style 2:1 chain is NOT available
here; the eccentricity that heats Hades is sustained secularly in a regular gap, not by a
protective resonance. 135k sits squarely in a regular island (flanked by chaos at 132.5k
and e-pumping from 140k) → the off-resonance gap placement is the resonance-aware optimum.

**Follow-ups (2026-06-19, user).** (1) No unnamed moons — named 5 only (all fictional
anyway). (2) Canon says the two outermost moons orbit **retrograde**, so Cassandra/Chaos
set to inclination 178°/175°; 100-yr re-run = STABLE (retrograde is Hill-stable to a larger
radius, ~0.7 vs 0.5, so it only helps); 1000-yr re-confirm running. (3) The Laplace 1:2:4
chain was **rejected** under observation-first: it needed Polyphemus inflated 120→168 M⊕
to keep Pandora's 27 h lock at the 4:1 distance (252k) — bending the observed planet to a
film moon layout. So Pandora a stays 225,000 km. (4) Corrected the Polyphemus radius in
`phase4/alpha_centauri.yaml`: cfg-ready is the **ring-model 1.0 R_Jup** (ρ~0.47), not the
raw imaging 1.05/0.40 — coupled to keeping the ring (small radius only works because the
ring carries the extra cross-section). Mass ~120 M⊕ in both ring/ring-free solutions; only
the radius differs (1.0 vs 1.1–1.15).

**Resonance-lock study (`scripts/resonance_lock_study.py` → `results/_moons_resonance_lock.md`).**
Tested whether the (fiction-free) Dante-Hades pair can be put in a *locked* MMR that
dodges the fixed Pandora — computing the resonant argument φ over 300 yr / 1500 samples to
tell libration (locked) from circulation (not locked). Result: **no lock is achievable.**
The 3:2 (even at the exact period ratio, Hades 131k) **circulates** (φ-coverage 358°,
capture fails — Pandora's secular forcing washes out the weak first-order resonance), and
the 2:1 (Hades 167k) **ejects** (caught between Pandora's 5:3 and 3:2). Hades e_max is
~0.056 across the whole 128–135k band, independent of position → zero resonant pumping.
So the off-resonance gap (135k) is the *only* stable option, not a preference. Physical
caveat recorded in `phase4/alpha_centauri.yaml`: with no resonance maintaining e, real
tides would damp Hades's eccentricity and the canon >900 K heating would fade — it is not
self-consistent in a fixed-Pandora (observation-first) system; the Laplace-chain fix is
barred by keeping Pandora at the observed 225k. e=0.056 is adopted as a given (documented
limitation), not a dynamically sustained value.

Masses/radii for Dante/Hades/Cassandra/Chaos are invented (only Pandora's mass + diameter
and Cassandra's >6500 km diameter are canon). Poly-L4/L5 are **not** moons — they are
Polyphemus's *heliocentric* L4/L5 co-orbital planetoids (separate star-centred Trojan
sim). The 9 unnamed moonlets are deferred. Gated layout frozen in
`../../phase4/alpha_centauri.yaml` (satellites axis); bodies in
`hypotheticals/alpha_centauri.json`.

## Related

- [phase3 procedure (skill)](../../.claude/skills/nearstars-phase3/SKILL.md) — parent topic this workspace contributes to
- [paper scoping note](../../plans/paper-scoping.md) — Pillar 3 consumer of this work
- [Phase 4 Barnard decision board](../../phase4/barnards_star.yaml) — Barnard low-e candidate (process + scan tables now in STABILITY_REPORT.md)
