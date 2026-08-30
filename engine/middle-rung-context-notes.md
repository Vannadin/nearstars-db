# The middle rung (C11) — context notes

## What it is, and what it is not

C7 refuses a body that is neither fully mixed nor fully layered, because ice mixed through
rock *where liquid water reached it* is a reaction (hydrated minerals with their own density)
and a transport history (how far the water got). Nothing here disturbs that; **C7 stays
closed and C11 is not its repair.** C11 is the other case F3 found in Malamud & Prialnik
2015's full text: take the depth the melting reached as a **declaration**, and the body is
static and four-zone — metal core, rock, water/ice mantle, and above the front a crust that
**never melted**: cold ice and rock grains that were never in contact with liquid water.
Hydration is a story about places liquid water reached, so C7's reaction argument does not
apply there, and for that state a mixing rule *does* exist — the two-layer model of Yasui &
Arakawa 2009 that Malamud & Prialnik adopt as their eq. (1) and report does *"a very good job
of reproducing the compaction curve of the mixture"* (§3.1.3). That is the shape C10 already
uses for antigorite plus enstatite.

Opened by the owner on 2026-08-30 on F3's grounds (`engine/malamud-readthrough-context-notes.md`,
Proposal). It is the first row added after the list closed.

## The design, and why two declarations

- `differentiation_front` — cumulative mass fraction from the centre that melted and
  differentiated; 1.0 is today's body. Everything above it (below any gas envelope) is crust.
- `crust_rock_fraction` — the crust's rock mass fraction. **A second declaration because the
  source does not let the front fix it**: in Malamud & Prialnik 2015 the outer mantle is
  ice-enriched by water that rose from the core and refroze in the rock's pores (§5.1), so
  its rock fraction is below the primordial value; the primordial (bulk) fraction is an upper
  bound on it, not its value.
- `crust_porosity` — optional: the same paper's eqs. (4)–(6) with Γ = 1 (the crust never
  melted, T_max < T_m; with the text-consistent form of eq. (7), Γ(273 K) = 0.9999) as a
  two-layer porosity on the crust's density only. The paper's curves are laboratory
  compaction (764 MPa, ice I data), so this is an **upper bound** on void, and creep (C9)
  would close it further. The ice's homologous temperature is taken against the ladder's own
  melting temperature at that pressure.

Both are declarations in C1's sense: history sets them, this recipe does not derive them
(in the source both are outputs of a 4.6 Gyr multiphase-flow run, never inputs), and the
grade is analog when they are used.

**Directions, registered before the sweep**: rock held in the crust raises C/MR² (mass moves
outward); porosity lowers it (mass moves inward). That is why porosity is optional and
bounded rather than a second free knob — a body could otherwise be fitted from both sides.

## The crust in the code

`_stack` partitions by mass: core (cmf) → rock (total rock minus the crust's) → ice (imf
minus the crust's) → crust (`crust_primordial`) → gas. `solve` refuses a partition that asks
for more rock or ice than the body has, a crust with no rock (that is the ice layer), a
front on an undifferentiated or ice-free body, and `crust_porosity` together with
`initial_porosity` (two laws on one void). The crust is `mix(h2o ladder, silicate)` — no
serpentinisation in it, because water never reached it (the source's outer-mantle rock is
"mostly unprocessed"). Inside `integrate`, a crust step whose (P, T) the melting curve calls
liquid raises a `PhaseGap` with the "lower it" direction; the temperature bracket then walks
the centre down until the crust is solid, and the solution it settles on cannot meet the
declared surface temperature. `solve` reads that outcome — a declared crust, the shooting
not converged, the surface colder than the declaration — and refuses by name: a never-melted
crust cannot sit at that temperature, and the fix is the declaration (colder potential
temperature or a higher front), not the bracket. (The first version let this through as
`converged=False` with a note; the test caught it — a self-contradictory declaration must not
pass as a merely unconverged solve.) `ice_samples` are not taken in the crust, so the column verdict speaks
of the mantle only. `Structure` gains the crust base radius and pressure and the crust's
void volume; `solve` returns `crust_thickness` [km].

**One bug caught on the way, worth recording.** The first `_stack` computed the crust mass as
(1 − gmf) − front without clamping at zero, so a body with a gas envelope and front = 1.0
got a *negative* crust, the ice bound went to 1.0, and the first `--refresh` froze Uranus and
Neptune as refusals. Clamped; the stack's bounds for the ice giants are now bit-identical to
the old expressions (checked with `repr`), and the anchor was re-frozen with identical values.
Also the ice search in `_solve_ice_for_radius` must be bounded by the crust's demand at both
ends, or every sweep point declines.

## The sweep

Grid, declared before running: potential temperature **200 K** (the roster's 270 K refuses
any crust of substance — ice Ih/III/V melt at 251–273 K between 0.02 and 0.6 GPa — so the
whole grid, reference included, runs at 200 K); front 1.0 / 0.9 / 0.8 / 0.7 / 0.6; crust rock
fraction 0.3 / 0.6; one porous point per moon at front 0.7 · X_d 0.6; core fractions
0 / 0.15 / 0.30 / 0.45 inside `infer_three_layer`. The table is in the C11 row; the raw
members (core / ice / C/MR²) are in `test_interior.py --middle-rung`'s output. 22 jobs were
launched six at a time; the two 270 K jobs were stopped unfinished (below).

Reading it without moving the grid:

- **Titan 0.3414 is inside the front 0.8 · X_d 0.6 band** (0.3384 at core 0.15, 0.3498 at
  core 0). That closes along the core axis — the third observation narrowing the band, the
  way Europa's does — with both declarations left at grid values.
- **Callisto 0.3549 is between two declared pairs**: above front 0.8 · X_d 0.6 (0.3393) and
  0.0012 under the low end of front 0.7 · X_d 0.6 (0.3561–0.3643). No band contains it. A
  front of ~0.72 at X_d 0.6 evidently would; that number is not written into any body,
  because writing it would be fitting a declaration to the answer — C5 declined to write the
  ice giants' rock fraction, C10 declined to extrapolate serpentinisation, and this is the
  third application of the same rule. What the grid says is enough: C10's grid lay entirely
  below the published value and C11's brackets it.
- **Porosity lowers the band by ≈ 0.015** on the front 0.7 · X_d 0.6 pair on both moons — the
  registered direction, and the size of a laboratory-cold upper bound on crust void (the
  crust's void fraction is reported in the note). It is not a knob: with it on, Titan's band
  still contains its value (0.3386–0.3496) and Callisto's still does not.
- Trends are monotone as expected: deeper front (more crust) and more crust rock both raise
  the band; at fixed front the X_d 0.3 → 0.6 step is worth ≈ 0.015–0.035.
- One member did not converge: Callisto, front 0.9 · X_d 0.3, core 0.30 (its band is quoted
  with that member's value marked in the raw output).

**Costs, recorded.** Points took 2–7 min on a machine also running the water2 gate and the
270 K jobs; Titan's first three points took 31 min each under that load, the later ones
2–7 min. **The 270 K refusal through the inversion route is expensive**: `infer_three_layer`
calls `solve` many times per core fraction, and each `solve` exhausts the temperature bracket
(T_BRACKET_TRIES × 1.6 steps, both walls) before the crust's `PhaseGap` surfaces as a
refusal — 17 and 24 CPU-minutes without finishing, against about 12 s for one direct `solve`.
Not fixed here; noted as the place to look when that route is next touched.

**A test declaration that was wrong, and why.** The first C11 test declared front 0.8 ·
X_d 0.4 on the Europa-type body (core 0.12, ice 0.10): a crust of 0.20 mass with 0.6 ice
asks for 0.12 ice, more than the body's 0.10, so `solve` refused it *for the ice budget*,
not for the melting curve the test meant to exercise. The grid must respect
crust × (1 − X_d) ≤ ice fraction and crust × X_d ≤ rock fraction; for this body X_d 0.6
does (ice 0.08, rock 0.12). The same check bit `_solve_ice_for_radius`, whose ice search must
start at the crust's ice demand and stop below the point where the crust's rock demand
exceeds the rock left — without the upper bound every sweep point declined.

## Parking (superseded the same day — kept as history)

**Parked 2026-08-30, before the first commit, by the owner's decision: the liquid-water gap
(water2) is closed first, because putting ice into a mixture walks trial paths into that
gap.** C11 stays in the queue. What was built before parking is kept on the branch
`c11-wip-parked` (the stash commit's hash, e42ab852; the stash entry itself was dropped afterwards because the
stash stack is shared by the repository's three worktrees), so nothing is lost and nothing
uncommitted lingers in the worktree. Next time: a WIP commit on a branch, not a stash.

## Where it got to

Design, executed in `interior.py` and `porosity.py` on the parked branch:

- three declarations — `differentiation_front` (cumulative mass fraction from the centre
  that melted and differentiated; 1.0 = no crust), `crust_rock_fraction` (rock mass fraction
  inside the never-melted crust, the second declaration F3 insisted on), `crust_porosity`
  (optional, Malamud & Prialnik 2015 eqs. (4)–(6) with Γ = 1 on the crust) — threaded through
  `_stack` → `integrate` → `_shoot_pressure` → `shoot` → `solve` → `infer_three_layer`;
- `_stack` gains a fourth layer: core → rock (total rock minus the crust's) → ice (imf minus
  the crust's) → crust (`crust_primordial`: ice ladder + silicate as grains by additive
  volume) → gas; `solve` refuses inconsistent partitions with the numbers;
- the never-melted declaration is enforced: a crust step whose (P, T) is above the melting
  curve raises a `PhaseGap` naming C11 (a self-contradictory declaration, not a temperature
  bracket problem);
- `PorousCrust(Mixture)` applies the two-layer porosity to the crust's density only;
  Malamud's constants live in `porosity.py` with the eq. (7) note;
- smoke test on a 0.025 M⊕ icy body (core 0.1, ice 0.5): front 1.0 reproduces the default
  bit for bit; at 270 K a crust is refused (liquid); at 200 K, front 0.8 with crust rock 0.4
  gives C/MR² 0.3236 against 0.3020 without a crust (radius −1.1 %); with porosity 0.3181
  (direction as pre-registered: crust rock raises C/MR², porosity lowers it).

Not done: tests, `--refresh`, docs, chain.yaml, the Callisto/Titan sweep, the C11 row.

## What the sweep will need (noted while parking)

The moons' roster temperature is 270 K, at which any crust thicker than the surface skin is
above ice Ih/III/V's melting curve (251–273 K between 0.02 and 0.6 GPa), so the crust
declaration is self-contradictory there. The sweep needs a colder declared potential
temperature (e.g. 200–240 K), stated as part of the grid, with the no-crust reference re-run
at the same temperature. That is a consistency requirement of the declaration, not a knob.
