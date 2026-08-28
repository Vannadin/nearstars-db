# Speed — context notes

Decisions taken while trying to bring the ice-giant anchor back under `scripts/check.sh`,
and the reasoning behind them. Appended as the work goes. The one rule this work runs
under: **every anchor stays bit-identical.** A change that moves the last bit of any
converged value is a different calculation, not an optimisation, however fast it is.

## 1. The budget, decided before measuring

The brief put the gate at about two minutes. Timed on a quiet machine before any change,
`bash scripts/check.sh` takes **14 min 12 s** (HEAD 8dda4b68); the two-minute figure
predates the H/He table, which made every giant solve 25× slower and the engine tests are
where the gate's minutes go (§10 has the per-test split). The budget is set against the
brief's intent rather than against that number: **the ice giants may add three minutes to
whatever the gate already costs.** Three minutes for the two ice giants means **one ice giant must solve in 90 s**,
against 1038 s now — a factor of 11.5. Whether that factor exists without
moving a bit is the question this work answers; "no" is an allowed answer, and then the
anchor goes under the gate by one of the three other routes the brief names.

Why three minutes and not "whatever it takes": the gate is run by hand before a commit,
and every minute added is a minute the next person is tempted to skip. The gate being
already at fourteen is a separate debt, named in §10 and not paid here.

## 2. What the existing `--icegiant` flag actually protects: nothing, any more

The first measurement was not the profile. Running `test_interior.py --icegiant` as it
stands takes 23 s and **declines** both planets: it declares `potential_temperature = 2500 K`,
a value written when the H/He envelope was a polytrope with no temperature and the
declaration landed on top of the ice mantle. Since the Chabrier table came in, the
declaration is the 1-bar temperature, and 2500 K at 1 bar drives the shoot into the
silicate ceiling. The 1038 s Uranus in the H/He checklist is the 76 K body, run by hand.

So the anchor behind the flag is stale, and the flag would have kept printing a refusal
table without failing. Recorded here because it changes what "bring the anchor back" means:
the anchor to protect is Uranus at 76 K, +5.46 % radius, 6158 K centre — the numbers in
the methodology's giants table.

## 3. Where the time goes — one integrate, profiled before touching anything

A single `integrate()` on a Uranus-like body (P_c = 800 GPa, T_c = 6158 K, 1500 steps,
stack silicate → `h2o_hot` → H/He) takes 0.69 s cold. cProfile on it, HEAD before any change:

| what | calls | share of the integrate |
|---|---|---|
| `water_hot.pressure` (everything below is inside it) | 71 323 | **85 %** |
| `fermi.inverse_f_half` — Newton on the forward table | 74 143 | **76 %** |
| `fermi._hermite` — the cubic Hermite cell (each call recomputed the cell and called two lambdas) | 273 700 | 21 % |
| `fermi._sommerfeld` — degenerate branch (each call rebuilt three π-constants from j) | 251 208 | 13 % |
| `water_hot.density` — the log-log secant inversion | 11 260 | 4 % own |
| `hhe_table` (bicubic) | – | < 2 % |

The whole solve, profiled once end to end on HEAD (cProfile roughly doubles the wall
clock, so shares are what matter): 1927 `integrate()` calls from 23 pressure shoots in 15
temperature attempts; `water_hot.pressure` 81 % of the total (144.7 million calls),
`fermi.inverse_f_half` 58 % (150.4 million), `_hermite` 14 % (294 million), the H/He table
3 %, `integrate()`'s own bookkeeping 1 %. The per-integrate picture above scales.

The multipliers, counted rather than guessed:

* **6.3 pressure evaluations per density inversion.** Not "one or two": two of them are the
  bracket ends `pressure(RHO_MIN, t)` and `pressure(RHO_MAX, t)` that every call re-evaluates,
  and the secant from the warm start needs three or four more to reach 10⁻¹².
* **3.5 forward + 2.5 derivative evaluations per Fermi inverse** — about three Newton steps.
* **~8 density inversions per integration step** in the ice layer: one for the adiabatic
  gradient, two for the finite-difference K_T, one inside `dpdt_v` (same P, T as the first),
  four in the Runge-Kutta stages (the first at the same P, T again).

So the Fermi inverse is not "called by the hot water"; it *is* the hot water. The H/He table
lookup the H/He notes measured at 2.2 µs is irrelevant to the ice giant's cost.

## 4. What was taken back without moving a bit — the op-identical class

The one class of change that needs no empirical bit check is the one that leaves every
floating-point operation in place and in order, and removes only Python work around it.
Each item below was still checked (a 1000-point sweep of all four Fermi functions, one
integrate and one pressure shoot, `repr` for `repr`), and each came out identical.

1. `_hermite` split into `_hermite_cell` (cell index + the four basis values, table-agnostic)
   and `_hermite_on` (one table on that cell). A Newton step needs F₁/₂ and F₋₁/₂ at the same
   η, so the cell is built once and applied twice. The two lambdas that fetched slopes are
   gone; the slope tables are passed directly.
2. `_sommerfeld`'s coefficients `a, b, c, j+1` computed once per j at import, by the same
   expressions. The Newton loop uses them inline for j = ±½, sharing `e2 = η·η`.
3. `inverse_f_half`'s loop: `min`/`max` builtins replaced by comparisons with the same result,
   `1e-13 · value` hoisted (the same double every iteration).

Measured on one pressure shoot at fixed T_c (seven integrations): 6.37 s → 4.75 s, **−25 %**.
One integrate: 0.69 → 0.53 s.

## 5. Rejected: caching the inversion's bracket ends (E1)

Two of the 6.3 pressure evaluations per inversion are `pressure(RHO_MIN, t)` and
`pressure(RHO_MAX, t)`, and t is constant across the ~8 inversions of a step. Caching the pair
per t cuts one integrate from 0.53 s to **0.31 s** — the single biggest lever found.

It moves bits. One integrate's radius went from 16346294.64445802 to 16346294.644458175
(1e-14 relative), the surface temperature from 2244.7561428835315 to 2244.756142884339, and
the shoot's converged central pressure by 7e-14. The reason is structural, not a coding slip:
`pressure()` is not a pure function of (ρ, T). Its Fermi inverse warm-starts from the previous
inverse's solution (`fermi._LAST_INVERSE`), so a cached bracket value differs from a freshly
computed one by the last ulp of a Newton run that started elsewhere — and the bracket ends
feed the secant formula directly, so the ulp propagates. The same warm-start state means
that **any** change to the sequence of `pressure()` calls is a change of path. Recorded so the
next person does not measure it again; the 40 % is real and it is not available under the
bit line.

## 6. The finding: the 1038 s is a shoot that cannot converge, not an equation of state

Tracing every `integrate()` call of the full Uranus solve (76 K at 1 bar) answers the
brief's question about iteration counts, and the answer is not what the H/He notes assumed.

The temperature loop runs about fifteen passes. The first eight are cheap: the bracketing
ladder hits the H/He table's cold wall at once (two integrations each), and `attempt()`
raises the central temperature by 1.6× until pass 9 lands at 6528 K. From there every pass
looks like this:

```
int#20  P_c 1.0848e12  m/M 0.822    ← ladder
int#21  P_c 4.3390e12  m/M 11.46    ← ladder, bracket closed
int#22  P_c 4.3390e12  m/M 11.46    ← the same point again (the redo after the ladder)
int#23  P_c 1.2025e12  m/M 0.96889  ← secant
int#24  P_c 1.2224e12  m/M 1.00717
int#25  P_c 1.2187e12  m/M 1.00035
…
int#33  P_c 1.218723e12  m/M 0.999442
int#34  P_c 1.218724e12  m/M 1.000321
int#35  P_c 1.218723e12  m/M 1.000321
…  (170 more lines with P_c fixed to seven digits and m/M alternating)
int#222 P_c 1.218723e12  m/M 1.000320
```

**The surface mass is a staircase in the central pressure**, and the target sits on a
riser. Layer boundaries are placed at cumulative fractions of the *target* mass, but the
switch happens at the first integration step whose enclosed mass crosses the fraction — so
the boundary radius is quantised to one step, `dr = R/1500`. Between two central pressures
that move the crossing by one step, the ice → H/He boundary jumps by one shell of ice
replaced by gas: `3·(dr/R)·(Δρ/ρ̄)·M ≈ 3 × (1/1500) × 0.45 ≈ 9 × 10⁻⁴ M`. The trace shows
exactly that riser: 0.999443 and 1.000320 straddle 1 with nothing in between. `SHOOT_TOL`
is 10⁻⁸. The secant therefore cannot converge, walks its bracket down to the riser, and
spends the remaining **~190 of its 200 iterations re-integrating the same central pressure**
— 0.45 s each, about 90 s per pass, fourteen passes: the 1038 s, to within the noise.

The rocky anchors have the same staircase (core/mantle at the same 1/1500 quantum) but a
smaller density contrast, and their targets happen not to sit on a riser; Jupiter and
Saturn have no ice/gas boundary at all. This is why the ice giant alone is two orders of
magnitude slower, and why the earlier notes blamed the Fermi integrals: they measured the
cost per integration and multiplied by an iteration count they had not counted.

**Why it still ends `converged=True`.** Whether the target sits on a riser depends on the
central temperature, which the outer loop keeps moving. Counted per shoot, the 23 pressure
shoots of the full solve cost `2 2 2 2 2 2 2 3 · 205 205 11 205 11 205 11 205 11 11 205 205
205 205 · 10` integrations: eight cheap temperature-bracketing passes, then nine that spin to
the cap and six — including the last one, at 6157.5 K — that land between risers and
converge in ten or eleven. So the frozen Uranus is a converged solution to both boundary
conditions; it just took 1927 integrations to get there, 1845 of them re-integrating one
central pressure.

**What it means for this task.** The fix is obvious and small — interpolate the layer
switch inside the step so the surface mass is continuous, or let the shoot recognise a
riser below the step quantum and stop with the badge saying so. Either one **changes the
answer**: a continuous boundary moves every anchor by up to one step's worth of mass, and a
riser-aware stop returns a different iterate. That is exactly the accuracy-for-speed trade
the brief reserves for the owner, so it is not done here. It is handed up with its price
tag: the passes that did converge took ten or eleven integrations, so the same solve with
every pass converging would cost **15 × 11 × 0.45 s + 17 × 0.02 s ≈ 75 s** — under the
90 s budget from §1, with the op-identical savings of §4 already counted. The budget is reachable; the bit line, not the
equation of state, is what stands between here and there.

## 7. Landing: the anchor is frozen and the gate compares, because that is what the bit line allows

Of the three routes the brief names, the third fits this repository's existing habit
(ices III/V/VI, the Fermi table): compute once, freeze, and let the gate check cheaply
that the frozen value is still what the code would produce. `test_ice_giant.py` does it;
`ice_giant_anchor.json` holds it; `scripts/check.sh` runs it after `test_interior.py`.

What catches the frozen value going stale is stated in that file's docstring and repeated
here because it is the part that had to be designed rather than copied:

* **One integration at the frozen (P_c, T_c)** must reproduce the frozen radius, mass,
  moment of inertia and surface temperature bit for bit. That integration *is* the solve's
  last integration (checked at freeze time: `standalone_reproduces_solve`), so any change in
  an equation of state, the Fermi integrals, the layer stack or the integrator fails it.
  Cost: 0.5 s.
* **A fingerprint of the shooting path** — the bytecode of `solve`, `shoot`,
  `_shoot_pressure`, `_narrow_bracket`, `_surface_temperature_met`, `_stack` and the twelve
  constants that steer them, docstrings excluded. One integration cannot see a change that
  would lead the loops to a *different* converged point; the fingerprint can, and a
  changed fingerprint fails the gate until `--refresh` re-freezes. Comments do not trip it.
  The interpreter version is part of it, deliberately.
* The gate prints `[SKIP]` for the full solve and `[FROZEN]` for Neptune's refusal, so the
  output says what is not being run instead of staying quiet.

What it does not protect: a change that alters the answer *and* leaves both the integrator
and the path bytecode untouched. Nothing in the engine can do that except the data
tables, which are Python modules and therefore covered by the integration.

**Rejected on the way: E2**, skipping the redo integration after the bracketing ladder (the
`int#22` above). It was bit-identical on one shoot and would save one integration in
~200 per pass — not worth carrying an unprovable change for half a percent. Recorded so it
is not re-measured; it becomes worth revisiting only after the shoot converges, when it is
one in eight.

## 8. Neptune integrates now — the frozen file carries two anchors, not one

`hhe-eos-context-notes.md` records Neptune declining on the class-based ice dispatch, 3 K
below the hot-water floor. Run at 72 K with the code as it stands, **it integrates**:
465 s, `converged=True`, 4.2122 R⊕ against 3.8646 published (+9.0 %), central pressure
1534 GPa. Nothing in this work touched the dispatch (`interior.py`'s `ice_material` line is
untouched, as the brief requires); the notes describing the refusal predate the c_P-weighted
mixture gradient and the temperature-converged badge, and one of those moved the envelope
base past 1800 K. The refusal is no longer the anchor, the radius is. It is frozen with the
same two checks as Uranus. Whether +9.0 % is the ices' fault or the envelope's is the
question the ice-giant notes set out — still open, and now measurable.

## 9. Numbers, before and after

| | before (HEAD 8dda4b68) | after |
|---|---|---|
| one integrate, Uranus-like, cold | 0.69 s | 0.53 s |
| one pressure shoot at fixed T_c (7 integrations) | 6.37 s | 4.75 s |
| full Uranus solve (76 K), 1927 integrations | 1257 s traced · 1360 s plain (both under load from parallel runs; the checklist's 1038 s was a quiet machine) | 890 s traced (same load) |
| Uranus radius | 4.198258073397856 R⊕ | **4.198258073397856 R⊕** |
| Uranus C/MR², T_c, P_c | 0.17409532698563532 · 6157.521157536532 K · 1220.254153430657 GPa | **identical** |
| twenty fast anchors (condensed 5, moons 6, icy 5, Jupiter, Saturn ×2, Earth core) | – | **all bit-identical** |
| what `check.sh` runs for the ice giants | nothing | one integration each + path fingerprint, 0.8 s |
| whole gate, quiet machine | 14 min 12 s | 14 min 39 s (the difference is the new test plus run-to-run noise) |

The budget from §1 is **not** reached under the bit line: 890 s against 90 s, a factor of
ten short, and §6 says exactly where the factor is and what it costs to take. The anchor
is nevertheless under the gate, by the third route.

## 10. Where the gate's fourteen minutes go — a debt this work names and does not pay

Each engine test timed alone on the final tree, quiet machine:

| test | seconds |
|---|---|
| `test_mixture.py` | 262 |
| `test_giant.py` | 226 |
| `test_interior.py` | 223 |
| `test_porosity.py` | 40 |
| `test_mass_radius.py` | 16 |
| `test_core_state.py` | 15 |
| `test_fermi.py` | 11 |
| `run.py earth` · `check_contracts.py` · `test_rocky_roster.py` | 7 · 7 · 5 |
| `test_ice_giant.py` (this work) | **1** |
| everything else (nine files) | ≤ 1 each |

Three files are twelve of the fourteen minutes, and all three grew when the H/He table
replaced the polytrope — every giant solve went from 0.2 s to 5–20 s and those tests
sweep compositions (Saturn's Z ladder, Jupiter's core ladder, the mixture sanity grid).
That is the same shape as the ice-giant debt one size smaller: anchors that are cheap to
declare and expensive to run, protected by the gate only as long as nobody minds waiting.
Whether they should be frozen the same way, or the sweeps thinned, is a separate decision;
it is written here so the "two minutes" the brief remembered is replaced by a number.
