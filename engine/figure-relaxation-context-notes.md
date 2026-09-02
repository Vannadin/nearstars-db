<!-- Brief 39 — 정유체 도형 가정을 완화시간으로 판정하는 relaxation verdict 의 사전등록·설계·결과 -->
# Figure relaxation verdict — context notes (Brief 39)

2026-09-03. **§1–§3 are the pre-registration and were committed before any code ran.** §4
onward is filled in after the run. Verifiers per item: (병) parallel seat, (직) directing seat,
(감) audit seat, (여기) work seat.

## 1. What is being built, and what is deliberately not

**Scope (owner, 2026-09-03):** *"편평도 솔버를 직접 만들지 않고 냅둘 거야. 편평도 솔버에 줄 수
있는 값을 구할 수 있도록 내부구조 솔버 안에서의 배선만 해놓는 거지."* So:

- `scripts/refs/body_figure.py` is **not touched**. Its `C22 = 0.3·J2` (hydrostatic 10/3) stays
  as the blanket declaration `body-figure-methodology.md:131-137` says it is.
- What is built: **one labelled verdict the interior solver emits** — *could this body's
  degree-2 figure have relaxed to hydrostatic within its age?* — so the figure solver has a
  grounded input for the fossil-bulge caveat instead of a blanket assumption. `chain.yaml:315`
  wires `fossil_bulge` out of `body_figure` with nothing setting it; this supplies the value
  *upstream* of it.
- **Not built**: a fossil-bulge predictor. A fossil figure needs a history (earlier spin or
  orbit); the recipe declares evolution out of scope. The verdict is a **gate**, and the
  refusing branch refuses by name rather than emitting a fossil ratio.

## 2. Design decisions, argued

**Placement — `engine/rheology.py` for the material law, composition in the `interior_layers`
recipe wrapper.** The viscosity laws are material physics (they sit beside `eos.py`, the same
layer that answers density and specific heat). The verdict needs the solver's temperatures plus
the body's age, so it is composed in `interior.py`'s `@recipe("interior_layers")` wrapper
(`_from_state`), **not inside `solve()`**: `solve` is one of `test_ice_giant.py`'s
`PATH_FUNCTIONS`, so touching it would move the path fingerprint for a change that does not
alter any solved number. Reading the verdict off the finished `Result` keeps the anchors
bit-identical **by construction**, and that is checkable rather than asserted. `dataclasses.replace`
adds the values (precedent: `eos.py:2073`).

**Temperature — the solver's own mantle range, verdict at the coldest end.** `interior_layers`
solves a temperature column when `potential_temperature` is declared: `st.t_surface` (top of the
adiabat, matched to the declared T_pot within `T_SURFACE_TOL`) down to `st.t_cmb`. The verdict is
taken at **`t_surface`, the coldest temperature the solver owns** — if the top of the convecting
mantle relaxes, everything below it does. ⚠ **Condition riding with every verdict**: the solver
has **no conductive lithosphere** (`interior-structure-methodology.md`'s contract says the lid is
`internal_heat_nontidal`'s business), so "relaxes" means *the convecting mantle relaxes*; whether a
cold lid could hold a fossil figure is **not** answered here. `tidal_transport`'s T_i is **not**
used (permanent `validation:"failed-io-reproduction"`, no engine import). With no declared
potential temperature the solver carries no temperature at all and the verdict is
**`cannot-say (no temperature)`** — refuse by name, not a default.

**Comparison timescale — body age, and why.** The engine has one time: `age_gyr` (Earth 4.54,
Pandora 5.3). The time since the lock established would be the sharper comparison, but
`tidal_locking` has no recipe and `t_lock` is produced nowhere. Age is the **most permissive**
window, so the two verdicts have different strengths and the label says so: *"cannot relax within
age" is a hard refusal* (no shorter window could rescue it); *"relaxes within age" is necessary,
not sufficient* (a lock established yesterday has had no time). And the threshold's sensitivity
to age is small — directing seat: **779 K at 0.1 Gyr → 709 K at 10 Gyr** — to be reproduced here.

**Viscosity — both cached solid laws, evaluated on our own melting curves.**
Rovira-Navarro+ 2021 eq. 5 (`η = η_s·exp[(E_a/(R T_s))(T_s/T − 1)]`, η_s = 1×10¹⁶ Pa·s,
E_a = 300 kJ/mol) is primary; Monteux+ 2016 eq. 8 after Abe 1997 (`η = 256·exp(25.17·T_liq/T)`)
is the second law for branch ③. T_s and T_liq come from **`eos.silicate_solidus` /
`silicate_liquidus` at the top-of-mantle pressure** (Brief 36's chain), so the `T_sol/T_liq`
ratio is *computed from our curves* rather than declared 0.80 (at 0 GPa the chain gives
1393.6 / 1954.4 K = 0.713 (여기); the two laws' 18 % agreement at 0.80 therefore does **not**
transfer automatically and is measured, not assumed).

**Rigidity — μ = 65 GPa, relayed.** Rovira-Navarro+ 2021 parameter table, *"Mantle shear
modulus"*, footnote 5 = Segatz et al. (1988), **which we do not hold**. Rovira-Navarro's own
caveat rides with it: Maxwell *"does not properly capture the complex behavior of olivine
observed in laboratory experiments"* — **Maxwell is a floor, an order-of-magnitude gate, and the
verdict says that is all it is.**

⚠ **Every solid-viscosity constant is relayed.** Karato & Wu 1993 (`1993Sci...260..771K`) is the
source Monteux's 256 / 25.17, Rovira-Navarro's 300 kJ/mol and the thesis creep law all cite;
**none reproduces it and the owner could not obtain it (2026-09-03, Science, no OA route).**

**Why relayed constants are nevertheless usable here — the insensitivity finding, to be
reproduced and written beside the constants in code.** Directing and parallel seats, 4.5 Gyr
threshold temperature (τ_M = age):

| | η_s = 1e15 | 1e16 | 1e17 |
|---|---|---|---|
| E_a = 300 kJ/mol | 689 K | 720 K | 755 K |
| E_a = 540 kJ/mol | 922 K | 953 K | 986 K |

Two decades of anchor and an 80 % swing in E_a (Rovira-Navarro's own Mars-mantle range, Nimmo &
Stevenson 2000) move the threshold **298 K total**; τ_M spans 20+ decades over the temperature
range while the parameter uncertainty is worth ~2. *The justification is not "these values are
trusted" but "the criterion is insensitive to them over the full admissible range".*

**Adopted as a declared family with a grid (C11).** The verdict compares `t_surface` against the
**whole threshold spread** {E_a} × {η_s} × {age}: above every threshold → relaxes; below every
threshold → cannot; inside the spread → **`cannot-say (inside criterion spread)`** — branch ④
made an output rather than a footnote.

## 3. Pre-registered outcome branches (before the first run)

① **Every roster body relaxes with room to spare** → the hydrostatic declaration is
  *supported*; the verdict is machinery whose consumer never branches — say so, do not pretend
  otherwise. (Directing seat's expectation: ① fires for the whole roster; indicative margins
  +1136 K Dante / +857 K Hades above the worst-case 986 K used `tidal_transport`'s T_i and are a
  **prior, not a target**. Nothing is tuned to reproduce them.)
② **Some body cannot support it** → the gate earns its wire.
③ **The two viscosity laws disagree on a verdict for the same body** → the declaration is the
  answer, not the physics.
④ **The criterion's own spread exceeds its margin for some body** → a check whose error exceeds
  its criterion cannot raise a grade; emitted as `cannot-say (inside criterion spread)`.
⑤ **The age or temperature source flips a verdict** → that choice is the answer and gets the
  label.
⑥ *(work seat, added before running)* **The verdict is decided by which layer's temperature is
  fed, not by the body.** The solver's coldest temperature is the adiabat top (~T_pot, ≥ 1300 K
  for any declared value so far); a conductive lid would be hundreds of K colder and the
  threshold sits at 690–990 K. If ① fires *only because* the solver has no lid, that is this
  branch, and the honest product is the condition in §2, not a hydrostatic verdict.

**Expected roster measurement**: Earth (T_pot 1600 K) — relaxes; Pandora (no
potential_temperature) — cannot-say (no temperature); Alpha Centauri A b (giant) — out of domain
(no silicate mantle). Uranus/Neptune anchors — untouched by construction, and the verdict is
not computed for them because they are solved through `solve()`, not the recipe wrapper.

## 4. Run record — filled in after the run

*(pending)*
