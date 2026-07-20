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
  González Hernández et al. 2024 (arXiv [2410.00569](https://arxiv.org/abs/2410.00569)): m=3·Msini ↔ i=19.5°, stable; Basant
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

**Phase scan overturns the "no-lock, phase-robust" claim (`scripts/phase_scan.py` →
`results/_moons_phase_scan.md`).** The lock study used a single fixed seed (all moons at
M=0). Capture is phase-sensitive, so this scanned Hades's initial mean anomaly across the
full circle at the exact 3:2 (131k). Result: **at M0 ≈ 180° (Hades starting anti-aligned /
at apoapsis) the 3:2 DOES librate** (φ-coverage 258° vs 358° elsewhere), and it is the
*calmest* phase (MEGNO 8.1 vs 60–550 for the others) **with Hades e pumped to ~0.122 —
about double the non-resonant 0.056.** That higher, resonance-maintained eccentricity is
exactly what would physically sustain the canon tidal heating, and it needs no change to
Pandora (observation-first intact). So the earlier "no lock available" was an artifact of
the M=0 seed. CAVEATS: it is a wide-amplitude libration (~130°, near the resonance edge)
on a mildly chaotic trajectory (MEGNO 8) over only 300 yr — a longer (1000+ yr) run at
Hades 131k / M0≈180° is needed to confirm the lock persists and stays bound before adopting
it. The currently-gated layout (Hades 135k gap, e frozen) is unchanged pending that
confirmation; the 3:2-locked anti-aligned config is now the leading candidate to supersede
it (would also bump Hades a 135k→131k and set the moon's epoch mean anomaly ≈180°).

**3:2-lock 1000-yr confirmation — PASSES (`results/_moons_3to2lock/`, variant
`hypotheticals/_acen_3to2lock.json`).** Hades 131k / M0=180°, 1000 yr IAS15:
CHAOTIC_BUT_HILL_STABLE, all 5 bound and calm. The 3:2 libration **persists** — φ-coverage
261° over the full run, first-half 257° vs last-half 261° (no drift, the lock holds), and
Hades's eccentricity is resonance-maintained at **mean 0.086, max 0.124** (≈1.5–2× the
non-resonant 0.056). So the lock is real and durable, and it physically sustains the canon
tidal heating **without moving Pandora** (observation-first intact). It is a wide-amplitude
(~130°) libration on a chaotic-but-bound trajectory — ship-safe, same class as the gap
config. → Recommended to supersede the 135k gap as the gated moon config (Hades a 135k→131k,
epoch mean anomaly ≈180°), pending the owner's call (and a combined re-check if larger
inclinations are also adopted — the lock was confirmed coplanar).

**Inclination-spread scan (`scripts/inclination_scan.py` → `results/_moons_inclination_scan.md`).**
Art-direction wants larger inclinations so the moons spread over different sky latitudes
from Pandora. Scanned a spread s (Dante 0.5s, Hades 1.0s, Pandora 0, Cassandra/Chaos
retrograde-tilted), 300 yr each. Result: **stable (bound) up to s≈30°; ejects at s=40°** —
the limit is the **Kozai-Lidov critical inclination (~39°)** for the most-inclined moon
(Hades at 1.0s): at 40° the host star pumps Hades's e to ejection. So inclinations can be
pushed generously (Hades ≤~30°) for the visual spread; the comfortable sweet spot is
**s≈15–20°** (clear spread, MEGNO ~90, Chaos's e pumped to ~0.2). NOTE: scanned on the
coplanar 135k gap base — combining a large spread with the 3:2 lock needs its own re-check
(inclination can detune a resonance).

Masses/radii for Dante/Hades/Cassandra/Chaos are invented (only Pandora's mass + diameter
and Cassandra's >6500 km diameter are canon). Poly-L4/L5 are **not** moons — they are
Polyphemus's *heliocentric* L4/L5 co-orbital planetoids (separate star-centred Trojan
sim). The 9 unnamed moonlets are deferred. Gated layout frozen in
`../../phase4/alpha_centauri.yaml` (satellites axis); bodies in
`hypotheticals/alpha_centauri.json`.

## 2026-06-19 — PLAN (not yet run): inner-pair co-tilt + J2 fidelity

**Co-tilt experiment (user idea).** To get both the self-consistent heating (3:2 lock) AND
a visual sky-latitude spread, tilt Dante+Hades *together* (same inclination + shared node →
mutual inclination 0) instead of independently (which creates mutual inclination and detunes
the 3:2). Setup: fix the 3:2-lock config (Dante 100k, Hades 131k, Hades M0=180°, Pandora
225k equatorial, Cassandra/Chaos retrograde); scan a common tilt θ = 0–35° applied to both
inner moons. Measure (4 axes): 3:2 φ-libration persistence, bound/MEGNO, Hades e (still
pumped to ~0.09?), and **Dante–Hades mutual inclination over time** (the prime detune risk
— differential nodal precession from different a). Decision tree: lock survives to θ≈20–30°
→ adopt both; only small θ → heating-vs-spread trade-off; θ-independent break → pick one.
Hard ceiling is Kozai (~39°). Tool: add a "co-tilt mode" to inclination_scan.py + φ/mutual-
incl tracking; loader already takes phase/inclination (would add per-body node Ω for
generality).

**J2 oblateness — fidelity gap (the key caveat).** Our REBOUND moon sims use POINT masses
(no J2). For moons J2 is a *first-order* term (dominant nodal precession + it anchors close-
in moons to the planet's equatorial = local Laplace plane), unlike the wide planet orbits
where J2 is negligible. Consequences: (1) our moon results are CONSERVATIVE for the co-tilt
lock — real J2 co-precesses the inner pair and suppresses the mutual-inclination drift that
would detune the 3:2, so the lock is likely *more* robust in-game; (2) J2 forces inner moons
toward the equatorial plane, so large inner tilts are physically resisted (big visual tilt is
more natural for OUTER moons); (3) J2 nodal precession slowly rotates the sky configuration
in-game.

**Principia supports it (confirmed, docs/reference/principia-cfg-reference.md).**
`principia_gravity_model` takes `j2` (unnormalized zonal harmonic, requires `reference_radius`)
OR a full `geopotential_row` (degree/order Cnm/Snm), mutually exclusive. So Principia models
oblateness in-game — the J2 anchor our sim omits IS present in the game (same sim↔game
fidelity theme as the Barnard fixed-step finding). Actions next session: (a) add J2 to the
moon sim via REBOUNDx `gravitational_harmonics` (`pip install reboundx`), Polyphemus J2
estimated from its ~10 h rotation + low density (Darwin–Radau); (b) set Polyphemus `j2` +
`reference_radius` in the emitted Principia cfg (Phase 4 emit); (c) re-run the co-tilt +
3:2-lock experiments with J2 on for the faithful answer.

**UPDATE — the J2 gap is a PREREQUISITE, not just a fidelity nicety (dependency inverted).**
Confirmed Principia applies the geopotential to the **celestial–celestial** integration, not
only to vessels: `geopotential_tolerance` lives in the *ephemeris* numerics blueprint (the
celestial integrator's "drop negligible harmonics" threshold), and Principia's whole point is
reproducing real body-body effects (e.g. lunar precession). So the natural moons
(Pandora/Dante/Hades) **do** feel Polyphemus's J2 in-game → J2 is an **input** to the moon
dynamics, and the point-mass results above (3:2-lock, co-tilt, inclination, resonance scans)
are **provisional / pre-J2**, to be re-confirmed with J2 on before any moon orbit is final.
Documented reference of the real values: `docs/reference/principia-geopotential-data.md` (+ko).

**Polyphemus J2 computed (working value).** Giant-calibrated q = ω²R³/GM: Polyphemus
q ≈ 0.22 (vs Jupiter 0.089 / Saturn 0.155 — 2×+, from its low GM at 120 M⊕ + fast ~10 h
spin). With J2/q ∈ [0.105 Saturn, 0.165 Jupiter] → **J2 ≈ 0.022–0.038, central ≈ 0.028**
(~1.7× Saturn), J4 ≈ −0.001. Frozen in `phase4/alpha_centauri.yaml` (bulk.geopotential_j2).
This is the value to inject in step (a). Order of finalization is now: **J2 first → reboundx
into the sim → re-run moon experiments → finalize moon orbits.**

## 2026-06-20 — J2 injected into the moon sims; it REVERSES the moon-orbit choice

**J2 force, self-implemented (reboundx dead-end).** `pip install reboundx` force-
downgraded rebound 5.0.0 → 4.6.0 (reboundx 4.6.2 pins rebound 4.x), which broke the
whole codebase (rebound 5's named-particle API: `sim.add(name=...)`). reboundx has no
rebound-5 release. Rather than revert the codebase to 4.x, dropped reboundx and wrote
J2 as a rebound `additional_forces` term: `scripts/j2.py` (Murray & Dermott vectorial
J2 accel about an arbitrary spin axis = the body's orbit-normal by default; back-
reaction on the planet for momentum conservation). **Validated** to <0.1 % against the
analytic secular apsidal (ϖ̇) and nodal (Ω̇) precession rates at i = 0/30/60° (the i=0
Ω̇=0 check passes too). J2 = 0.023 (the gated `bulk.geopotential_j2`, Helled+2011 RD),
R_eq = 1.0 R_Jup. Wired into run.py as `--j2 / --j2-body / --j2-radius-rjup`; scan
scripts forward it via `STAB_J2` env.

**Performance: the Python force callback is the bottleneck → TRACE not IAS15.** The
`additional_forces` closure is called every step, and IAS15 evaluates forces ~12×/step
→ 1000 yr went from ~5 min (point-mass) to ~3 h. TRACE calls forces ~1–2×/step (~11×
faster, ~16 min/1000 yr) and handles the near-equal A–B binary; it loses MEGNO, but the
moon verdict rests on Hill-fraction + a/e drift, not MEGNO. Scan scripts auto-switch to
TRACE when `STAB_J2` is set. (NB: TRACE returns `megno_final=None` → fixed the scans'
`{megno:.1f}` formatting to handle None, which had silently emptied their result tables.)

**THE RESULT — J2 reverses the recommendation (`results/_moons_j2/`).**
- **135k gap (off-resonance, the currently-gated layout): STABLE with J2** (TRACE 1000
  yr, all 5 moons bound/calm, Hades e 0.02–0.05, |ΔE/E| 8.7e-9).
- **3:2 lock (131k, M0=180°, the prior leading candidate): UNSTABLE with J2** — Hades
  ejects at t ≈ 510 yr (TRACE 1000 yr, e→2.6e4, Hill-frac→unbound). J2's apsidal/nodal
  precession detunes the marginal (~130° wide, resonance-edge) libration → circulation →
  e-pump to ejection. The lock was attractive because it self-consistently pumped Hades's
  e (~0.12) for the canon tidal heating; **J2 kills that**, so Hades e ≈ 0.05 reverts to an
  *adopted given* (documented limitation), as it was before the phase-scan lock discovery.
- **Decision: keep the 135k gap, retract the 3:2-lock adoption.**

**Principia-fidelity pass (new `--integrator leapfrog --dt-minutes 10`).** Leapfrog =
fixed-step symplectic in ABSOLUTE coordinates → a faithful structural proxy for
Principia's fixed-step QUINLAN_TREMAINE_1990_ORDER_12 (10 min ephemeris step), which
WHFast's Jacobi coordinates cannot mimic for a moon→planet→star hierarchy (this is *why*
the moon runs were always IAS15/TRACE, never WHFast — the binary AND the hierarchy break
WHFast). Note our default base step P_inner/50 ≈ 9.6 min already ≈ Principia's 10 min.
Results: **gap STABLE under leapfrog too** (|ΔE/E| 1.5e-10) — accurate (TRACE) and
Principia-class agree → the adopted layout is robustly game-faithful. **Lock is
integrator-sensitive**: leapfrog (2nd order) keeps Hades, TRACE ejects it — the ejection
is a delicate resonant effect a low-order fixed step misses (Principia's order-12 is
closer to TRACE). Integrator-sensitivity is itself a reason to avoid the knife-edge lock.
Caveat: leapfrog-10min is a *conservative* proxy — "leapfrog stable" does NOT prove
"Principia stable" for a knife-edge config; it only confirms robustness for the gap
(where all three integrators agree).

**Inclinations — J2 raises the ceiling (`results/_moons_inclination_scan.md`, TRACE 300
yr).** J2 anchors inner moons to the equatorial plane vs the star's Kozai pump: bound now
to s = 40° (point-mass ejected at 40°), limiter shifted from inner Hades to outer
retrograde Chaos (e_max 0.88 @ s=40). Visual sky-latitude spread can go to s ≈ 25–30°.
Co-tilt (`results/_moons_cotilt_scan.md`): with the lock gone, tilted inner pairs (θ
10–30°) stay bound but circulate; differential nodal precession drifts their mutual
inclination to ~60° → co-tilt does NOT keep Dante/Hades coplanar.

**Can ANY resonance survive J2? No (`results/_moons_resonance_j2_scan.md`,
`scripts/resonance_j2_scan.py`, TRACE 600 yr, Hades M0=180°).** Swept the Dante:Hades
resonances that dodge Pandora — 5:4 (116k), 4:3 (121k), 3:2 (129/131/133k), gap (135k) —
with J2 on. Result: **no lock survives.** Sitting on an exact resonance EJECTS (131k 3:2
and 121k 4:3 both eject — J2 precession destabilizes the resonance); off-resonance
positions (129/133/135k) are bound but **circulate** (φ-cov >355°, no libration) = same
class as the gap. The 5:4 (116k) pumps Hades e to 0.44+ but its periapsis then dips
INSIDE Polyphemus (q ≈ 47,000 km < R_p 71,492 km) → planet collision, non-viable (the
Hill-based "bound" verdict misses this — periapsis-vs-planet-radius is an unchecked
collision mode, follow-up). So the documented limitation is confirmed by sweeping the
whole resonance space: no self-consistent resonant tidal-heating config exists under J2.
Small bonus: J2's secular forcing alone holds Hades e ≈ 0.12 at the gap (133–135k, M0=180)
— higher than the point-mass 0.056, so the heating plausibility is mildly improved even
without a lock. (Moving Dante is boxed in: Roche floor ~98k leaves ~2k inward; the Pandora
resonance wall at Hades ~140k caps the 3:2 outward move at Dante ~107k.)

**Still point-mass-vs-J2 open / not done:** an IAS15+J2 gold-standard spot-check of the
lock ejection (TRACE is trustworthy here + we're dropping the lock, so skipped — ~3 h
cost); J2-sensitivity across the 0.017–0.033 range (central 0.023 is decisive; the gap is
off-resonance so insensitive, the lock is dead at central so a bound-test sweep wouldn't
rescue it). Desktop (7900X/WSL2) staged in another session for future heavy sweeps —
`DESKTOP_WSL_SETUP.md`.

## Related

- [phase3 procedure (skill)](../../.claude/skills/nearstars-phase3/SKILL.md) — parent topic this workspace contributes to
- [paper scoping note](../../plans/paper-scoping.md) — Pillar 3 consumer of this work
- [Phase 4 Barnard decision board](../../phase4/barnards_star.yaml) — Barnard low-e candidate (process + scan tables now in STABILITY_REPORT.md)
- [Phase 4 α Cen decision board](../../phase4/alpha_centauri.yaml) — satellites + bulk.geopotential_j2 axes consume this J2 result
