# Sub-Neptunes — context notes

Decisions taken while closing C1 of `interior-core.md`, and the measurements behind them.
Appended as the work goes.

## The two measurements, reproduced

**The sweep** (M 5 M⊕ · CMF 0.20 of the rock · 500 K at 1 bar, class `giant`), 2026-08-29:
gas 100 % solves at R 6.282 R⊕ but with `converged=False`; 80, 50, 30, 20, 10, 5 and 2 %
all decline with *"central pressure must exceed fe_prem's ceiling (12000 GPa)"*. Reproduced
exactly as C1 recorded it.

**The 17.7 M⊕ core.** `test_giant.py` has measured that cap at **0 M⊕** since the H/He table
landed on 2026-08-28 (the table made the envelope heavier and the silicate ceiling is
already filled by the overburden); its own comment says so. The domain row in the
methodology doc still says 17.7 M⊕. So of the two, **the row is the stale one**, and the
sweep's refusal is the false one — both are wrong, in different ways, and neither contradicts
the other once read correctly: the Jupiter-mass core cap is a real silicate-ceiling limit,
the 5 M⊕ refusal is not a ceiling at all.

## The mechanism, in one sentence

At the rock–envelope boundary the trial central temperature (2 × 500 K) leaves the envelope
base at 244 GPa · 760 K, far below the H/He table's reach line (2150 K there), and
`integrate()` mistakes that domain exit for **reaching the 1-bar surface**, so the envelope
contributes no mass, the surface mass plateaus at exactly 1 − gas fraction, and the
bracketing ladder climbs to the iron ceiling and reports it.

Measured before it was named: surface mass against central pressure from 1 bar to 12 TPa for
the 20 % case rises monotonically to 0.8000 at the first trial where the envelope is reached
(P_c 1.8 TPa) and stays at 0.8000 to the ceiling, `p_surface` sitting at 244 GPa and then
2.8 TPa. **The U-shape hypothesis is refuted for this body**: there is no falling branch and
no second root; the target is never crossed because the envelope is never integrated.

The line that does it is the table-floor stop: `if floor and not mat.in_domain(p, t): p_surface
= p; break`. It was written for Uranus, whose 1-bar temperature (76 K) sits under the table's
100 K floor, where the exit is a few bar above the surface and the 1-bar temperature can be
closed by T ∝ P^∇_ad over "three or four" in pressure. At 244 GPa the same extrapolation spans
six decades and means nothing. Nothing distinguished the two exits.

## The fix, and why it leaves every anchor alone

The exit is a surface only near the surface. Above `FLOOR_EXTRAPOLATION_MAX = 100` × 1 bar an
exit from the table's domain is what the material's own `check_temperature` says it is: too
cold for a convecting envelope (`too_cold=True`, which the temperature bracket answers by
raising the central temperature 1.6× and trying again) or above the window. The line is a
factor of ten above anything the anchors do: instrumenting every trial integration of the
Uranus, Neptune, Jupiter and both Saturn solves, the largest exit pressure was **9.04 bar**
(Neptune), so no anchor path crosses the new branch and all stay bit-identical by
construction. The pure-gas sweep case reached 203 bar on its trial paths, which is why it
came back `converged=False`: the same extrapolation, over two decades.

No ceiling moved. The iron ceiling refusal can still be reached, but only when the envelope
has actually been integrated and the surface mass is genuinely short.

## The second layer, found only after the first was fixed

With the domain exit thrown as a temperature refusal, the sweep no longer declined at the
iron ceiling — it declined at `MAX_STEPS` ("surface not reached in 40000 steps"), and that
turned out to be two more things stacked.

**A trial that overshoots the target is not a failure.** At a hot trial central temperature
the envelope balloons past the grid (40000 steps of dr = R_rock/1500 ≈ 24–42 R⊕) with the
surface mass already many times the target. The old code raised, and the raise came out of
`solve()` as a refusal. Now `integrate()` returns the partial structure with
`surface_reached=False` when the enclosed mass is already over target: all the shoot needs
from that trial is "too much mass", and a partial can never be accepted as converged
(its mass is not within `SHOOT_TOL`). Only paths that previously raised are touched.

**The mechanism under the sweep is that the envelope is unbound.** Trace at 20 % gas
(`scratchpad/trace20.txt`): the temperature loop's second pass asks for a central
temperature of 26 600 K, because at 4096 K the 1-bar level comes out at 77 K and the loop
scales proportionally. At 26 600 K the surface-mass curve has **no root**: just below
P_c = 657.8 GPa the rock alone holds 0.8009 of the target at 1 bar with no envelope, and any
envelope above that pressure (base 1343 bar, 22 900 K) is still short of 1 bar at 42 R⊕ while
holding 3.9 targets. The isothermal sound speed at that base, c_T² = kT/μm_H ≈ (9 km/s)², is
half the escape speed at the core surface (19 km/s): the atmosphere's pressure asymptotes to
P_b·exp(−r_b/H) with r_b/H ≈ 4.3, so for any base below about 75 bar the 1-bar level lies at
infinity, and above it the envelope mass runs away. `Unbound` names that: raised when the
pressure bracket closes to 1e-9 with the low side surface-reached-and-short and the high side
a partial, and carried out of `shoot()` with **both reached states in the sentence** — the
hottest bound solution (T_c, R, T_1bar) and the temperature above which nothing binds. The
sentence the sweep now returns: *"no solution reaches the declared 500 K; the hottest bound
central temperature is 4096 K with the 1-bar level at 77 K and R 3.49 R⊕; above 26 633 K the
envelope is unbound … the adiabat from 1 bar is hotter than this mass binds"*. That reads
aloud as physics, and the physics is real: a 4 M⊕ core cannot hold a 1 M⊕ envelope whose
adiabat passes 23 000 K at its base. Real sub-Neptunes at T_eq ≈ 500 K have a radiative zone
that keeps the deep adiabat far cooler (Nettelmann+ 2011 need an isothermal region to
80–800 bar on GJ 1214 b; Valencia+ 2013 use Guillot 2010's radiative atmosphere as the upper
boundary); this recipe anchors the adiabat at 1 bar and has no such zone. The declaration
that makes the sweep body bound is a colder 1-bar temperature.

**And the temperature loop itself diverges on thin envelopes.** With a bound wall in place,
GJ 1214 b at 2 % H/He still failed: the 1-bar temperature scales as T_c^2.3 there (8380 K →
298 K, 14 720 K → 1851 K), so the proportional update T_c·T_pot/T_surf, which multiplies the
error by (1 − n), oscillates without shrinking — two points, forever. The giants sit at
n ≈ 0.7 and contract by 0.3 each pass (Jupiter 0.30 → 1.37 → 0.92 → 1.02 → 0.994 …, traced),
which is why nobody had seen it. The loop now switches to a bracketed regula falsi in
log T_c – log T_surf **only when the deviation has not shrunk over a full oscillation** (or a
wall was hit); every anchor contracts every pass and never enters that branch, which is the
bit-identity argument, measured rather than hoped: Earth, Mars, Mercury, the Moon, Ganymede
(dump compared field by field) and the ice-giant gate's bit line all unchanged after the
change. GJ 1214 b then converges in eight passes.

The hypothesis in the brief — a U-shaped surface-mass curve with a root on the falling
branch that the climbing ladder never sees — was **tested and refuted for these bodies**: the
curve is monotone to the plateau, and the failure was that the envelope was never integrated
at all. The ladder's own U-shape handling (the `rung` low end) is untouched.

## Two more, found by the pure-gas case and by GJ 1214 b

**The brief's U-shape is real, one body over.** With the wall in place, the 100 % gas body
returned two different solutions at the *same* central temperature on alternate passes:
11.4 R⊕ with the 1-bar level at 145 K, and 131 R⊕ at 2396 K. That is the falling branch the
ladder's own comment describes. The ladder only ever handled it when it climbed from a
short seed (`rung`); when the seed already holds the target it broke out at once with no
rung, and the secant's second point (hi × 10⁻³) landed on the inflated branch. For a gas
body whose seed is over target the ladder now climbs while the mass *falls* — the falling
branch — until the mass drops under the target (that trial becomes the rung and the rising
branch takes over) or starts rising again while still over target, in which case the
U-minimum sits above the target and there is **no compact root**: `NoCompactRoot`, treated
by the temperature loop as the same wall as `Unbound`. The physical branch is the rising
one — mass grows with central pressure, and every published giant sits on it — and the
refusal says so. Anchors never take this path (their seeds are short; measured by the
bit line).

**Grid limit as a wall, not a verdict.** A trial hotter than the grid can hold
(`GridExceeded`: mass still short at 27 core radii) also enters the loop as a wall, so the
refusal quotes the hottest solution the grid holds instead of the discarded trial. With that,
20 % gas at 500 K actually *solves*: 12.7 R⊕, which is what a 1 M⊕ adiabatic envelope at
that entropy on a 4 M⊕ core is. Absurd for a real planet, honest for the declaration.

**The proportional update also merely crawls.** GJ 1214 b at 5 % gas / 250 K contracted by
only 0.9 per oscillation (n ≈ 1.9) and ran out of fourteen passes at 5 %. The switch to
regula falsi therefore fires when the deviation over one oscillation shrinks by less than
half (`T_CONTRACTION_MIN = 0.5`) while still above 5 % (`T_DIVERGENCE_MIN`); the anchors
contract by 0.01–0.1 per oscillation (Jupiter 0.70 → 0.37 → 0.08 → 0.022, Uranus
0.067 → 0.006 → 0.0004) and never reach either condition. The first draft of the rule had no
size floor and was tripped by 10⁻⁴ round-off wobbles near convergence — Uranus and Neptune
moved in the ice-giant bit line, which is exactly what that gate exists for. With the floor
the gate is green again and the condensed anchors compare equal field by field.

## How it came out

**The sweep** (5 M⊕ · CMF 0.20 of the rock · 500 K at 1 bar):

| gas | before | after |
|---|---|---|
| 2 · 5 · 10 · 20 · 30 % | iron-ceiling refusal (false) | solves: 3.67 · 5.21 · 7.58 · 12.70 · 18.8 R⊕, converged |
| 50 · 80 % | iron-ceiling refusal (false) | declines: hottest bound solution at 459 K / 297 K on 29 / 25 R⊕, the grid (27 core radii) above it |
| 100 % | "solved", R 6.28, converged=False | declines: hottest compact solution 11.3 R⊕ at 145 K; above 2460 K no compact root (U-minimum above the target) |

The radii that solve are what a 1-bar-anchored adiabat at 500 K gives a 5 M⊕ body; they are
absurd against real sub-Neptunes for the reason every refusal now states (no radiative
zone), and that is a property of the declaration, recorded in the domain row.

**GJ 1214 b** (8.41 M⊕ · 2.733 R⊕, Mahajan+ 2024 via `db/planets_curated.json`; Earth-like
nucleus, CMF 0.325 of the rock). The gas fraction that reproduces the radius, by bisection
at each declared 1-bar temperature:

| 1-bar temperature | H/He mass fraction |
|---|---|
| 250 K | 2.4 % |
| 300 K | 1.9 % |
| 350 K | 1.5 % |

Valencia+ 2013 (full text, §5): "the total amount of H/He in GJ 1214b can be robustly
constrained to be less than 7 % by mass", and "∼3 % by mass" for a solar-metallicity
envelope. The branch lands inside that on every declaration in the range, so it is
answering, not merely running — with the declared temperature carrying the residual spread
(1.5–2.4 %), which is the honest width of a model that anchors the adiabat at 1 bar.
Nettelmann+ 2011's models put the adiabat's onset at 80–800 bar under an isothermal
layer; a declared 1-bar temperature of 250–350 K is the same statement folded onto this
recipe's single knob.

**What must not move, checked.** Condensed anchors and Ganymede: field-by-field equal to
the pre-task dump. Ice-giant bit line: green (after the size floor on the divergence switch;
the first draft moved it, and that is the gate's job). Giant anchors: `test_giant.py`
unchanged values. Grid-phase asserts untouched.

**Papers.** Nettelmann+ 2011 (1010.0277), Valencia+ 2013 (1305.2629) and Mahajan+ 2024
(2402.05991) pinned in `docs/phase3/_bib/_method-interior-structure.yaml` and fetched to
the cache; the numbers above are from their body text, not abstracts.

**The Jupiter core cap was the same bug, and it reopened.** `test_giant.py` asserted the cap at
0 M⊕ "since the table", with a comment blaming the envelope's overburden. The first run after
the fix measured **11.46 M⊕** (an 11 M⊕ core solves at P_c 9.79 TPa, under the 13.5 TPa
silicate ceiling; 11.5 declines at it). The 0 was the envelope base leaving the table's
reach line at the trial temperature and being taken for the surface — exactly the sweep's
defect, seen from the other side of the mass range. So "one of the two measurements is
wrong" resolved as *both*: 17.7 was the polytrope's, 0 was the bug's, 11.46 is the answer
with the envelope integrated *(interim, superseded 2026-08-30 F2: 16.69 M⊕ — the 11.46 was
itself half a defect, the K_T finite difference poking past the 13.5 TPa ceiling on the
shooting's ceiling trial; see antigorite-thermal-context-notes.md)*. The assertion, the domain row and C1's closing text now carry
11.46, and this is reported here as a physically justified change rather than absorbed: the
giant anchors themselves (Jupiter Z = 0, Saturn Z = 0 and 0.0825) are unchanged.

**One regression caught by the giant gate.** The narrowing branch's "one more set of
passes" re-armed itself on every exhaustion, so a declaration the table's own temperature
ceiling forbids (Saturn with 3000 K at 1 bar — the badge test) looped forever: the bracket
kept bouncing off the ceiling back to the same central temperature. Two lines: the extension
is granted once, and a pass whose bracket returns the temperature it was given stops the loop.
The 3000 K case now declines in 2 s as the badge test expects.

**Cost** (wall clock, same machine; before = the ocean-layer run of the same day):

| test | before | after | why |
|---|---|---|---|
| test_giant | 223 s | 393 s | the Jupiter core-cap bisection now *solves* cores up to 11.46 M⊕ (~13 s each) where it used to decline them in a second |
| test_mixture | 263 s | 306 s | the same cores inside its Jupiter checks |
| test_ice_giant | 93 s | 101 s | noise; bit line unchanged |
| test_interior | 396 s | 428 s | the three sub-Neptune regression solves |

The gate's growth is the price of the false refusals being real solves now; measured, not
repaid.
