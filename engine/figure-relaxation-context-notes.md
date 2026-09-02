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
ratio is *computed from our curves* rather than declared 0.80. At 0 GPa the chain gives
**1661.2 / 1982.1 K = 0.838**, at 1 GPa 0.880, at 5 GPa 0.930 (여기, `eos.silicate_solidus` /
`silicate_liquidus`, peridotitic), so the two laws' 18 % agreement at 0.80 does **not** transfer
and is measured, not assumed. *Correction (38340556 → this commit, work seat's own error): the
first version of this paragraph printed "1393.6 / 1954.4 K = 0.713" — numbers written before the
evaluation that was meant to produce them had been read. They were not from the chain. The
pre-registration's design is unchanged; the number was false and is replaced by the measured one.*

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

## 4. Run record — 2026-09-03, code `21665370`

**Branch fired: ① — with ⑥ riding on it.** Earth (the only engine body with a declared
potential temperature) relaxes on both laws with room to spare: top-of-mantle 1600 K against
the threshold family **700–1009 K** (engine 0 GPa solidus 1661.2 K; τ_M(Rovira-Navarro) =
3.53×10⁵ s = 0.011 yr; Monteux/Abe agrees). Pandora returns `cannot-say (no temperature)`
— refused by name, not defaulted. Alpha Centauri A b is out of domain upstream (interior refuses
the giant), so no verdict is composed. **So the hydrostatic declaration is supported for the
convecting mantle of every body that has a temperature, and the consumer never branches on
today's roster** — said plainly, as ① requires. **But the reason it never branches is ⑥**: the
solver's coldest temperature is the adiabat top, ≥ 1300 K for any declared value, while the
threshold sits at 700–1009 K; a conductive lid hundreds of K colder would land inside or below
the family, and the solver has no lid. **The product is therefore the condition on the label,
not a hydrostatic verdict** — the wire is kept because it carries that condition to the figure
solver, and because the `cannot-say` and `cannot-relax` branches are reachable and pinned
(`test_rheology.py` §4: 850 K → inside spread, 600 K → cannot relax).

**Branches not fired**: ② (no body refuses), ③ (laws agree wherever a verdict exists), ④ (Earth
is 590 K above the family's top; ④ is an *output* for any body inside it), ⑤ (age 0.1 → 10 Gyr
moves the threshold 794 → 721 K, 73 K, below any margin measured).

**Reproductions** (여기): directing seat's threshold table reproduces to < 1.5 K **at T_s = 1600 K**
(689 / 720 / 755 / 922 / 953 / 986) — the seat's T_s was not stated; 1600 K is the value that
reproduces all six, recovered by inversion, and the test pins it. On the engine's own solidus the
family is 700–1009 K. Age sensitivity 73 K here against the seat's 70 K. Monteux self-check
8.0×10²² Pa·s at (4500, 2400) and 1.7×10¹⁹ at (4000, 2600) — ~10²³ and four orders, as surveyed.

**Anchors — bit-identical, verified not asserted.** `solve()` untouched; the verdict composes in
the recipe wrapper. Full `test_ice_giant.py`: all pass, Uranus and Neptune values identical to the
frozen file. ⚠ **Pre-existing drift found on the way, not mine**: `test_ice_giant.py --fast`
reports the path fingerprint differs from the frozen one (`708ff4627f24c448` vs
`67690e8df3a65544`). Measured at HEAD *before* my change with a copy of `interior.py` from
`c4768b18`: same `708ff…`. The anchor JSON was last refreshed at `764da03e` (Brief 26); the one
commit touching `interior.py` since is **`9ff07deb` (Brief 36, silicate melting curve)**, which
edited `solve` and `integrate` without `--refresh`. Values still match, so the gate passes; the
fingerprint alone is stale. Left for the directing seat to route — refreshing it in this commit
would attach Brief 36's change to Brief 39's label.

**Gate**: `check.sh` FAIL 0, all checks pass, **01:59:34 → 02:19:50 = 1216 s**; `test_rheology.py`
adds **0.03 s**. No new runtime dependency. Contract check 5/5 with the three new outputs and
`age_gyr`. `chain.py check` passes with the new edge.

**Noticed, not touched**: the ko contract mirror was already missing `crust_thickness` before
this brief (EN has it); I added only my three outputs and did not repair the pre-existing gap.
