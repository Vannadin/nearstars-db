<!-- C20 — 맨틀·핵 결합 열진화 적분기. 사전등록(코드 전) → 설계 고정 → 실행 기록 -->
# Core thermal history — the C20 integrator — context notes

**Released by the owner 2026-09-04 ("C20 ㄱㄱ", relayed by the directing seat). This is stem work: three of the six open edges wait on it. §1–§2 are the directing seat's pre-registration, copied verbatim before any code; §3 fixes the design choices, each labelled; §4 is the run record.**

## 1–2. Pre-registration (directing seat, written 2026-09-04 ~04:30, updated in the afternoon — verbatim)

##### C20 pre-registration — DRAFT, not committed, not started

**Status.** The owner has approved C20 *as a listed item* (`4b8e06ba`, 09-03 17:55) but has **not**
released it to start. This file exists so that, if the answer is "go", the branches are already
named and no threshold gets written after the numbers are on screen. **Do not commit this into
`interior-core.md` until the owner releases C20.**

Written by the directing seat 2026-09-04 ~04:30 KST. The C20 row in `interior-core.md` already
carries the *why / what / cost / relation*; this adds only the part that row lacks — **the outcomes,
named in advance.**

---

#### 0. Why this file is not optional

The C14 retraction of 2026-09-04 01:15 (`db402d92`) happened because a forward-Euler integration at
400 steps was **not converged** and the unconverged output was read as a physical finding ("two codes
disagree on Earth's inner core"). C20 is a ~1 100-step integration of a stiffer, coupled system.
**The same failure is available here and it is the most likely way C20 produces a wrong result that
looks right.** Branch ⑤ exists for that reason and is not a formality.

---

#### 1. Prerequisite to settle *before* the first line of code

`body_age` vs `system_age`. `chain.yaml:90` calls `body_age` `kind: measured, domain: given` with a
note (`:94`) saying the body's age *differs* from the star's. The roster does not do that —
`alpha_centauri_a_b.yaml` and `pandora.yaml` both carry the **system** age 5.3 Gyr, `earth.yaml` 4.54.

**Recorded finding (already in the C20 row, restated so the fix is unambiguous): the note is out of
step with the roster; the owner's condition is not a new rule.** Planet formation ends within about
one integration step of the star's birth — Lichtenberg+ 2019 `.tex:216` *"Disk lifetimes are
distributed around 5 Myr"*; Neumann & Kruse t₀ ≈ 1.3–1.9 Ma. A 4 Myr step cannot resolve a 5 Myr
offset.

⚠ **The trap that rides with it.** Unifying the age does **not** make `body_age` the input for
everything. The Ma-scale consumers (porosity, the C21 formation pulse) need **`t_form` (Ma after
CAI)**, which **no body declares**. Do not draw `body_age → porosity`. Fixing the note must not be
read as supplying `t_form`.

**Action: edit the `:94` note only. Change no node kind, no edge.**

⚠ **And edit only HALF of it.** Verified by the directing seat 2026-09-04 against the roster:

    chain.yaml:94  "천체 자신의 나이. 항성 나이와 다르고, 거대행성 냉각광도의 실입력이다."
                    ^^^^^^^^^^^^^^^^^ out of step   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^ TRUE, keep

    roster: alpha_centauri_a_b 5.3 · pandora 5.3  (both the SYSTEM age)
            earth 4.54 · luhman_16_{a,b} 0.5

The first clause ("differs from the star's age") is what the roster contradicts. **The second
clause is not only true, it was CONFIRMED by C19 on 2026-09-04** — the giant branch was measured
consuming `t_body` directly, and the edge was relabelled `via: t_body` because of it. Deleting
the note wholesale would throw away a statement today's work established. Rewrite the first
clause, keep the second, and cite C19 beside it.

---

#### 2. Branches — every outcome named before code

##### ① Earth calibration — *the tolerance goes here, before the run*
The integrator is Earth-calibrated by construction, so "it reproduces Earth" is not a result; it is
the **entry condition**. Declare the tolerance now.

- Target: the present-epoch state C14 already solves — **T_c 3 978 K** (band 3 750–4 284) and
  **Q_C 4.91 TW**.
- **Pre-registered tolerance: the integrated present-day T_c must land inside C14's own band.**
  That band is the honest width of the declared inputs; anything tighter would be invented here.
- **①a inside the band** → calibrated; proceed to ②–④.
- **①b outside** → report the miss and **stop**. Name in the report which constant would have to move
  and by how much, and **do not move it**. (This is the C14 §"Not adopted" discipline: landing the
  printed number by moving a constant is the thing this project forbids.)

##### ② Inner-core nucleation time — *the sharpest one, because C14 predicts the answer*
C14's finding: **at the solved T_c, Earth has no inner core** (all liquid above ≈3 600 K). A forward
integration therefore has a strong prior.

- **②a nucleation lands in the published window** (commonly quoted ~0.5–1.5 Gyr ago) → **this
  contradicts C14 and the contradiction is the finding.** Do not celebrate agreement with the
  literature; find what differs between the two paths and report it before anything else.
- **②b nucleates earlier than Earth's formation** → the model says the inner core always existed;
  report as a model artefact, not a result.
- **②c never nucleates** → **consistent with C14.** Then Q_L = Q_g = 0 for the whole history, and
  ΔE loses its two largest terms at every epoch — which propagates straight into ③.

⚠ ②c is the *expected* outcome. **Expecting it does not license reporting it without the convergence
test in ⑤.** An unconverged integration will happily never nucleate.

##### ③ ΔE_min over the last 3.1 Gyr — *the actual consumer*
C15 emits `entropy_history_verdict = "cannot-say (needs C20)"` on every result. Nimmo's three criteria
are mean ΔE, minimum ΔE, and the present value; **the discriminating one is ΔE_min**. Present-day
C15 gives **ΔE −69 MW/K, band −264…+238, 4 of 8 corners positive**.

- **③a ΔE_min > 0 across the window on every corner** → dynamo sustained; the verdict string changes.
- **③b ΔE_min < 0 somewhere on every corner** → dynamo fails; **report the epoch**, do not average it away.
- **③c the band still crosses zero over the whole history** → **the verdict stays `cannot-say`, and
  C20 does not resolve C15.**

⚠ **③c must be named now or it will not be reportable later.** With four of eight corners already
positive at the present epoch, a band that keeps straddling zero for 3.1 Gyr is a live outcome. If it
happens, the correct output is *"C20 built, C15 still cannot say"* — **not** a narrowed band chosen
after seeing the curve. Narrowing the corners post hoc is the failure this branch exists to block.

##### ④ `dT_c/dt` stops being a declaration
C14 declares 33–126 K/Gyr — a **4× spread between two published Earth models**. C20 computes it.

- **④a the integrated present-day rate falls inside 33–126** → C14's declared band is vindicated and
  can narrow; say by how much.
- **④b it falls outside** → **C14's published numbers must be re-read at the new rate before C20 is
  reported.** Do not report C20 while C14 stands on a rate C20 contradicts.

##### ⑤ Step convergence — *declare the test before the first run*
- Run the full history at **h, h/2, h/4** (nominal h ≈ 4 Myr, ~1 100 steps).
- **Pre-registered criterion: the quantity that must converge is `ΔE_min` over the 3.1 Gyr window —
  not the endpoint T_c.** Endpoint state can converge while the minimum of a curve has not.
- **Pass: |ΔE_min(h/4) − ΔE_min(h/2)| is under 10 % of |ΔE_min(h/2)|**, and the inner-core branch (②)
  returns the same case at all three step sizes.
- **Fail → the step is the result, not the physics.** Report the non-convergence and stop, exactly as
  C14 should have on the first evening.
- Emit the convergence width as a gate line, the way C15 emits `entropy_integration_width`.

##### ⑥ What C20 will **not** claim
- The model is **Earth-calibrated**; outputs read *"consistent with an Earth-calibrated model"*, never
  *"this body's value"*.
- **Radiogenic heating means the long-lived half only** (K · Th · U, via `radiogenic.history_factor`,
  already built). The short-lived pulse (²⁶Al · ⁵³Mn · ⁶⁰Fe) is **C21**, closed as a named refusal for
  want of `t_form`, and lies outside a 4.5 Gyr window regardless. The row must say which half, or the
  next seat reads "radiogenic heat included" as complete.
- C20 does **not** supply `t_form` to anyone (see §1).

##### ⑦ Anchors and gate
- C20 adds a **new node**; if it changes no path-fingerprint function or constant, **anchors are
  untouched and `test_ice_giant.py --refresh` must not be run.** State this explicitly in the commit.
- Gate **FAIL 0**, and state what C20 adds to gate time. ⚠ A 1 100-step integration run three times
  for ⑤ is not free — if it is heavy, the gate carries the **converged single run** and the
  convergence sweep is a separate on-demand script.

---

#### 3. What this costs, honestly

A dozen-odd core constants (heat capacity, expansivity, latent heat, gravitational-energy coefficient,
light-element content), an initial-condition declaration, and the Earth-calibration condition. **Every
one of those is a declaration**, and C20's output is only as good as the weakest. The row should carry
the count of declarations the way the other rows do.

#### 4. Order

`chain.yaml:94` note fix → ⑤ convergence harness → ① calibration → ② → ④ → ③.

⚠ **③ is last on purpose.** It is the one everybody wants the answer to, and it is the one most
easily produced by an unconverged run. **Do not read ③ off a run that has not passed ⑤.**

## 3. Design fixed before code (main seat, 2026-09-04 11:45; every choice labelled)

**Equations (Nimmo+ 2004, cached):** core eq. 30, `Q_R − Q_C = (Q̃_s + Q̃_L + Q̃_g) dT_c/dt`; mantle eq. 32,
`H_m M_m − Q_M + Q_C = M_m C_pm dT_h/dt`; `Q_C = 4πR² F_b` (31, eqs 37–39 → `cmb_flux.bottom_layer`);
`Q_M = 4πR_p² F_t` (33, eqs 34–36 → `mantle_flux.implied_flux`); potential ↔ real temperature by eq. 29
(`T_m = T(z) exp(−α_m g z / C_pm)`). Nimmo integrates eqs 30 and 32 forward *"using a constant timestep of
4 Myr; reducing the timestep to 1 Myr changes the …"* (line 419–420) — the 4 Myr step is theirs.

**State**: (T_c, T_m). Everything else is a function of the state at that instant.
- **T̃_m (mantle base, real) = T_m × r_b**, with r_b the ratio the interior solve gives at the reference
  potential temperature (Earth: 2 526 / 1 600 = 1.579, `interior.solve(1.0, cmf 0.325, T_pot 1600)`). This
  *is* eq. 29's form (the exponential factor does not depend on T), with the factor measured on our own
  adiabat instead of Nimmo's constants (which give 1.69 for z = 2 920 km) — chosen so the present-day
  balance is the one C14 solved. **Declaration count: 0 new** (r_b is read from a solve).
- **T_h (half-depth) = T_m × r_b^½** — eq. 29 is exponential in z, so the half-depth factor is the square root.
  Nimmo: *"the results are insensitive to the depth chosen"*.
- **M_m = (1 − CMF) M** (silicate mass, as `radiogenic.budget` already takes it); **C_pm = 1 200** (Table 2, in
  `mantle_flux.C_PM`).
- **H_m M_m(t) = `radiogenic.budget(M_m)["mantle_w"] × history_factor(t)`** — the long-lived half only (K·Th·U;
  the owner's condition 2). ⚠ Present-day value **14.9 TW** here vs Nimmo's Table 4 **23.4 TW** (their H_m
  5.3 pW/kg on their M_m): a real difference of inputs (our chondritic set with the 0.70 mantle share vs their
  declared H_m), **not tuned** — recorded so a mantle-side miss can be traced to it.
- **Q̃ coefficients** from `core_energy.core_terms(prof, dtc_dt = −1)` (linear in the rate) on the profile at
  the current T_c; the inner core is whatever `inner_core(prof)` says at each step (② is read off that).
- **dT_c/dt = (Q_R − Q_C) / (Q̃_s + Q̃_L + Q̃_g)** (eq. 30 rearranged); **dT_m/dt = (H_m M_m − Q_M + Q_C) /
  (M_m C_pm r_b^½)** (eq. 32 with dT_h = r_b^½ dT_m).
- **Stepper**: classical RK4 in time, h = 4 Myr nominal (Nimmo's), sweep h, h/2, h/4 (⑤). Cost measured:
  one balance evaluation 11 ms → ~12 s per history at h, ~85 s for the sweep. **The test runs the sweep**
  (adds ~90 s to the gate; stated in the commit).
- **Initial condition**: T_c(0) and T_m(0) are **declarations** (2 new). Nimmo: *"increasing the initial
  temperature (T_m = T_c) by 1000 K results in changes of less than 8 per cent in E"* — the mantle time
  constant is short at high T. The values used are written in the body file, not in the module.
- **Entropy over time**: `core_entropy.entropy_terms(prof, terms, dtc_dt, h, k)` at each step with the
  *computed* dT_c/dt. ⚠ **The eight-corner band of C15 collapses to four corners** (k × H): the third axis,
  the declared rate, is what C20 computes. Pre-registered: ③ is read on those four corners, and ③c ("the
  band straddles zero for 3.1 Gyr") stays a live outcome on four corners as on eight.
- **① calibration target**: present-day T_c inside C14's band 3 750–4 284 K (pre-registered). A second
  *report line, not a gate*: present-day T_m against the declared 1 600 K potential temperature.
- **New declarations, counted**: T_c(0), T_m(0) → **2**; everything else is read from modules that already
  declare (core constants of C14/C15, mantle constants of Brief 46/60, radiogenic set). Earth calibration
  condition: ①.
- **H_m — the ①b risk named before the run (directing seat)**: our 14.9 TW and Nimmo's 23.4 TW are **the same
  kind of quantity** — Nimmo's H_m *"is obtained from the radiogenic abundances of Sun & McDonough (1989)"*
  (line 488–489), i.e. long-lived radiogenic heat, nothing else. The gap is mostly ours to name: our budget is
  the whole silicate Earth's 21.3 TW × the 0.70 mantle share (the crust's 30 % is withheld from the mantle
  equation), whereas Nimmo's 5.3 pW/kg × M_m puts all of it in the mantle equation (≈21 TW; their Table 4
  prints 23.4). **Rule, pre-registered: if ① fails, raising H_m to 23.4 — or dropping the 0.70 share — to land
  the calibration is forbidden.** 14.9 is a computed value from the built radiogenic module; 23.4 is Nimmo's
  declaration; replacing a computed value by someone else's declaration to land a printed number is what C14
  §Not adopted forbids. ① failing is reported as a failure, with what would have to move and by how much,
  unmoved.
- **Declarations, two numbers side by side**: **new = 2** (T_c(0), T_m(0)); **the result stands on ≈ 24**:
  core — H_core 1.5 pW/kg, C_P 840, α_c 1.35e-5 (through γ), L_h 750 kJ/kg, β_c 1.1, χ₀ 0.042, γ 1.5, the
  fe_prem material and its melting curve; CMB layer — κ_b 1e-6, f 10, T₁ 3400, k_core 50; mantle — Ra_c 600,
  κ_t 6e-7, η₀ 1e21, ζ 0.01, T₀ 1573, ρ_m 4800, α_m 2.2e-5, C_pm 1200, T_s 293; radiogenic — the chondritic
  concentration set and the 0.70 mantle share; C20 — r_b (read from a solve, not declared) and the two initial
  temperatures. The Earth-calibration condition sits on all of them.
- **The four-corner band is not comparable to C15's eight-corner present-day band (−264…+238 MW/K)**: one axis
  changed from a declaration to a computation, so a narrower band is not a more precise one, and "C20 narrowed
  the band" is not a result to report.
- **What a ① failure would mean — written as a prediction, before the run (directing seat)**: the 0.70 mantle
  share is a *convention* and it is testable. The question is what the H_m M_m term of eq. 32 stands for:
  (가) heat generated inside the convecting mantle only → excluding the crust is right (our 0.70);
  (나) the whole silicate shell's heat, including what leaves through the surface → including it is right
  (Nimmo's 1.0). Crustal radiogenic heat does not drive mantle convection; it leaves through the surface. So if
  the equation balances the convective drive, (가); if it balances the surface heat flow, (나). **The direction
  of a ① miss is the diagnosis**: a history systematically colder than Nimmo's with a low surface heat flow →
  evidence for (나), the equation wants the crust-inclusive convention; any other direction or size → 0.70 is
  not the cause, look elsewhere. **Either way 0.70 does not move in this run; the diagnosis is recorded.**
  Nimmo's own reason: the cached text does not say why the crust is not separated — the word "crust" does not
  occur in the paper — so the convention question is ours, not his.
- **Initial condition — printed, not declared** (found while reading the Fig. 2 caption, before the first run):
  *"The starting temperature of both mantle and core was 4800 K"* (Nimmo Fig. 2 caption). Read as the **real**
  temperatures — T_c(0) = 4 800 K and the mantle base T̃_m(0) = 4 800 K, i.e. potential T_m(0) = 4 800 / r_b
  (= 3 040 K on our r_b 1.579) — because if it meant the potential temperature the mantle would start hotter
  than the core and eq. 37 has no jump. So the two "new declarations" are Nimmo's printed starting values on
  Earth, and only a body without such a printed pair would declare them. **Consequence for the code**: at
  t = 0 the jump is zero; F_b ∝ ΔT^{4/3} → 0 continuously (eq. 37–38), so `Q_C = 0 for ΔT ≤ 0` is the
  continuous limit, not a patch — the module takes it instead of raising, and says so.
- **Not claimed**: any value for a body other than "consistent with an Earth-calibrated model"; `t_form`
  (§1 trap); the short-lived radiogenic pulse (C21).
- **Anchors**: the new module touches no path-fingerprint function; `--refresh` not run.


## 4. Run record — 2026-09-04 (Earth; order kept: ⑤ → ① → ② → ④ → ③)

**Inputs**: interior solve (1 M⊕, CMF 0.325, T_pot 1 600 K → core_radius 0.5470 R⊕, P_cmb 135.28 GPa, T̃_m 2 526 K,
r_b 1.579); T_c(0) = 4 800 K, T̃_m(0) = 4 800 K (Nimmo's printed start, read as real temperatures → T_m(0) = 3 040 K);
age 4.54 Gyr; H_m M_m(0) = 14.9 TW × history factor; H_core 1.5 pW/kg on the nominal path.

**⑤ Convergence — passed, on record** (`test_core_history.py --sweep`, 414 s):

    step     n      T_c(0) K   T_m(0) K   inner core   ΔE_min band (3.1 Gyr, 4 corners) MW/K
    h        1135   4027.4     1525.5     never        −259.2 … +31.7
    h/2      2270   4027.4     1525.5     never        −259.2 … +31.7
    h/4      4540   4027.4     1525.5     never        −259.2 … +31.7
    width |ΔE_min(h/4) − ΔE_min(h/2)| / |ΔE_min(h/2)| = 0.001 % (< 10 %), same inner-core case at all three → converged.

Cost was mis-estimated in §3: each time step builds **four** core profiles (RK4) plus four corner evaluations, so a
history at h costs ~53 s, not 12, and the sweep ~400 s. **The gate carries the single h run (+53 s); the sweep is on
demand** — the brief's rule for a heavy sweep.

**① Earth calibration — ①a, inside the band**: present T_c **4 027 K** (C14's band 3 750–4 284; C14's solved 3 978).
Report lines, not gates: present T_m **1 525 K** against the declared 1 600 K (**−75 K**); present surface heat flow
**Q_M 28.3 TW** against Nimmo's / the observed **42 TW**; present Q_C 5.07 TW (C14 4.91).
**The pre-registered diagnosis applies even though ① passed**: the history ends *colder* than the declaration and
with a *low* surface flow — the direction named in advance as evidence for (나), that eq. 32's H_m M_m term wants
the crust-inclusive convention (Nimmo's 1.0, not our 0.70). It is evidence, not a decision: **0.70 did not move**, and
the alternative reading (the mantle constants ζ / η₀ of Brief 46, declared on present-day Earth) was not tested here.

**② Inner core — ②c**: never nucleates over 4.54 Gyr (r_i = 0 throughout) — consistent with C14's "no inner core at
the solved T_c". Not celebrated: Nimmo's nominal model *does* grow an inner core (IC age 1.10 Gyr, ξ 0.36) — with
400 ppm K, a hotter melting curve (T_m0 1 695 K-based) and 23.4 TW of mantle heating. Our core is 130 K cooler at
present than Nimmo's 4 155 K and our melting curve is `fe_prem`'s. The disagreement with Earth's *observed* inner
core is the standing C14 finding, unchanged by C20.

**④ dT_c/dt — ④a**: present **−36 K/Gyr**, inside the declared 33–126. C14's declared band can narrow to the computed
value **on this model** (the 126 was Gubbins' k = 60 model; our history sits at Nimmo's end). Not applied to C14
tonight — it is a report.

**③ ΔE_min over the last 3.1 Gyr — ③c, cannot-say** (read last, on the ⑤ record):

    corner (k W/m/K, H pW/kg)   ΔE_min MW/K   at t (Gyr)   mean   present
    30, 0.0                      −66           0 (now)      +10    −66
    30, 1.5                      +32           0 (now)      +106   +32
    70, 0.0                     −259           0 (now)     −183   −259
    70, 1.5                     −162           0 (now)      −88   −162
    band −259 … +32 · positive corners 1/4 · the minimum sits at the present epoch on every corner (ΔE declines monotonically)

**Verdict string**: `cannot-say (the four-corner band straddles zero inside the last 3.1 Gyr — C20 built, C15 still
cannot say)`. The band is **not** narrowed. What the curve does say, labelled: ΔE is strongly positive early
(+429…+710 MW/K at −4.1 Gyr on all corners) and declines through zero on three corners — the model's dynamo weakens
toward the present, and the corner that stays positive is the one with low conductivity *and* core potassium.
**Not comparable to C15's present-day −264…+238** (one axis changed from declaration to computation).

**Beside it, observed**: Q_C runs 26 TW at −4.1 Gyr to 5.1 TW now — a factor 5 — where Nimmo writes that an acceptable
model needs the CMB heat flux to have *"varied by less than a factor of 2 over 4.5 Gyr"*. Recorded, not acted on.

**Anchors**: none traverse `core_history.py`; `test_ice_giant.py --fast` 모두 통과; no `--refresh`.
**What C20 does not do**: feed `entropy_history_verdict` into C15 (that node's string stays `cannot-say (needs C20)`
until a wiring decision); supply `t_form`; include the short-lived pulse (C21).

## 5. After the first run — observation, diagnostics, and what closed (2026-09-04 afternoon; directing seat's review, everything re-read here)

**① against the observation, not against Nimmo — like for like.** Davies 2013 (`2013GGG....14.4608D`, cached,
owner-obtained) prints Earth's total surface heat flow: *"refined and are agreeing at around 44–47 TW"* (line 58),
its own map's *"final value of 45 TW"* (line 501). That total **includes the crust's radiogenic heat**, which never
passes through mantle convection; our share-0.70 Q_M is the heat the convecting mantle carries with the crust's
share withheld, so 28.3 against 44–47 compares two different quantities (a first version of this paragraph did
exactly that and called it "~37–40 % low" — withdrawn). Like for like, with the numbers this project already holds
(Nimmo & Primack 2020 `main.tex:261`, citing Davies 2013 and Sclater+ 1980, in `radiogenic-context-notes.md`):
total **42–47 TW**, and **35–40 TW with the crust's radiogenic share removed**, total radiogenic ≈ 22 TW.

    share 1.00 (crust in the mantle equation)   Q_M 34.8 TW   vs total 44–47          → ~25 % low
    share 0.70 (crust withheld)                 Q_M 28.3 TW   vs crust-removed 35–40   → ~20–30 % low
    Nimmo's own 42 (crust included)                            vs total 44–47          → ~5–10 % low

So the shortfall against the observation is **about a quarter**, on either convention, and Nimmo's model is itself
a little low. The crust-removed 35–40 is a secondary relay (Nimmo & Primack's reading of Davies / Sclater), not
a value read from Davies here — a strict like-for-like number of our own is not held.

**The line that matters most in this section — a hypothesis, neither adopted nor tested.** The two convention
differences push the same way, and undoing both lands near Nimmo's 42, which is near the observation; the more
physically faithful inputs (Earth's actual silicate mass, the crust withheld) move the result *away* from the
observation. One reading: *the parametrised equations and their conventions are a package — calibrated to
reproduce Earth under those conventions — and importing the equations without the conventions leaves the
calibration undone.* If so, the way C20 is applied to other bodies changes: "more correct inputs" would be a
mis-use of this equation set, not an improvement. The opposite reading, written beside it: *the equations were
fitted to one Earth point, and the conventions were merely the free choices used to hit it* — in which case the
equations carry no more than that point either way. Deciding between the two needs a third body the model can
be checked on, which we do not have. Until then ① reads: **passed on T_c, ~25 % low on surface heat flow, and
the miss may be a usage question, not a precision one.**

**Eq. 35 cross-check — the implementation is clean.** Term by term, `mantle_flux` is eq. 35 with η₀ 1e21, ζ 0.01,
T₀ 1 573 K, evaluated at the **potential** temperature (Nimmo line 341: *"viscosity at the mantle potential
temperature η_t(T_m)"*), and eqs 34/36 as printed. Put Nimmo's own present T_m = 1 613 K in: η_t **6.70e20 Pa·s**,
Q_M **41.8 TW** — his Table 4 exactly (6.7e20, 41.8). At our endpoint 1 525 K the same law gives 28.5. **The
shortfall is the mantle temperature, not the viscosity law**; the mantle temperature is the heat budget.

**Initial condition — a reading, counted as a declaration (24 → 25).** The Fig. 2 caption plots potential and real
curves for both mantle and core and says only *"the starting temperature of both mantle and core was 4800 K"*; it
does not say which. We read it as the **real** temperatures (T_c(0) = T̃_m(0) = 4 800 K, potential T_m(0) = 3 040 K).
Support from the paper's own eq. 35: at a *potential* 4 800 K the viscosity is η₀ exp(−32) ≈ 1e7 Pa·s and Q_M runs
away — our integrator blows up on the first RK4 substep at 4, 0.5 and 0.1 Myr (T_m −86 000 / −6 578 / 256 K) — and
Nimmo prints that he integrated at 4 Myr, so his own law excludes the potential reading. Not a printed statement,
hence a declaration; the sensitivity to the alternative reading could not be measured because the alternative does
not integrate in this model at any step tried.

**Share diagnostic — report, not adopt** (three outcomes named before the run, `scratchpad/c20-share-diagnostic-prereg.txt`
12:3x; the same kind of diagnostic as C14's "×1.083 lands both — observed, not adopted"):

    mantle share   H_m(0) TW   T_m(0) K   Q_M(0) TW   T_c(0) K   Q_C(0) TW   dT_c/dt   ΔE_min band (3.1 Gyr) MW/K   positive corners
    0.70 (ours)    14.9        1 525      28.3        4 027      5.07        −36       −259 … +32                    1/4
    1.00 (Nimmo)   21.3        1 573      34.8        4 009      5.15        −37       −256 … +35                    1/4

Outcome **⓶**: the crust-inclusive convention closes **55 %** of the T_m gap (48 of 88 K) and **48 %** of the Q_M gap
(6.5 of 13.5 TW). The crust convention is the main cause and a second cause of about the same size exists.
The linear arithmetic "add 6.4 TW back → 34.7" happens to sit near the integrated 34.8 but is not the right test
— the budget has to be integrated with the viscosity feedback; keep the coincidence from being read as a
confirmation of the arithmetic. **0.70 did not move.**
**ΔE_min is insensitive to the convention** (−259…+32 → −256…+35, still 1 of 4 corners positive): the possibility
raised before the run — that the dynamo verdict hangs on one convention — is **closed, not open**.

**Two unresolved items, kept apart (they were briefly one):**
- **(i) The other half of the T_m / Q_M shortfall — closed as Nimmo's construction, not our defect.** At share 1.00
  the remaining H_m gap (21.3 vs 23.4 TW) is entirely the mantle mass: the same 5.3 pW/kg on our (1 − CMF) M =
  4.031e24 kg gives 21.4, on his implied 23.4 / 5.3 = 4.415e24 gives 23.4 (mass ratio 0.913, H_m ratio 0.910 —
  directing seat's check). That mass is not printed; it is what his printed constants **construct**: a uniform
  mantle of ρ_m = 4 800 kg m⁻³ (Table 2) between R = 3 480 km (Table 1) and R_p = 6 400 km (Table 2) — (4/3)π(R_p³
  − R³)ρ_m = **4.423e24 kg**, ratio 1.002 to the division. Earth's real silicate shell (mantle + crust, CMF 0.325)
  is 4.031e24 kg, a mean density of 4 446 kg m⁻³ over that shell; his Earth's mantle is ~10 % heavier by
  construction (a core mass fraction of 0.26 instead of 0.325). So **both halves of the shortfall are Nimmo's
  conventions** — the crust inside the mantle equation, and a uniform-density mantle — and our history is
  colder because it carries Earth's actual silicate mass and withholds the crust. Neither is adopted; neither
  is a defect to chase. Beside it, sized and labelled: the mantle-base adiabat ratio (ours 1.579 from the
  interior solve vs 1.69 from his eq. 29 constants) is a computed value against printed constants — a difference
  of source, not an error; and R_p: our history uses Earth's 6 371 km (`cmb_flux.R_EARTH_M`), his 6 400 appeared
  here only in the cross-check that reproduces his Table 4 (Q_M ∝ R², +0.9 %). A one-point comparison with
  Fig. 2's early T_m is not possible — the figure is an image with no values in the text layer — and is left
  undone rather than read off tick marks.
- **(ii) Q_C's decline — closed as a property of the model family, not a defect.** Ours: time-average 13.2 TW, present
  5.07, peak 93 TW in the first 20 Myr (the mantle collapsing from its 3 040 K start), average/present **2.6×**.
  Nimmo's nominal (Table 6): time-average **21.5** TW, present 9.0, average/present **2.4×** — the same shape. The
  *"varied by less than a factor of 2 over 4.5 Gyr"* sentence (line 892) is the condition on the **eq. 44
  alternative** (exponential F_b, Table 6 col. 2), not a constraint his nominal model meets; an earlier line of this
  file called it a violated constraint — that reading was wrong and is withdrawn.

**Nothing adopted; the recipe path is unchanged.** Declarations: new 2 (+1 reading) · standing ≈ 25.

**Both conventions at once — the last diagnostic (pre-registered 12:31:31, `scratchpad/c20-both-conventions-prereg.txt`;
report, not adopt).** Mantle share 1.00 *and* Nimmo's constructed mantle mass 4.4234e24 kg (H_m M_m(0) = 23.4 TW),
one history at h = 4 Myr; the discriminator named in advance was the inner core (Nimmo's nominal: IC age 1.10 Gyr).

    conventions                       T_m(0) K   Q_M(0) TW   T_c(0) K   Q_C(0) TW   inner core   ΔE_min band MW/K (positive)
    ours (0.70, Earth's mass)         1 525      28.3        4 027      5.07        never        −259 … +32 (1/4)
    share 1.00                        1 573      34.8        4 009      5.15        never        −256 … +35 (1/4)
    share 1.00 + Nimmo's M_m          1 592      37.8        4 001      5.17        never        −255 … +36 (1/4)
    Nimmo Table 4                     1 613      41.8        4 155      9.0         IC 1.10 Gyr  E_min 134 (his single model)

Outcome **Ⓑ, with a sized residual**: the two conventions close **70 %** of the Q_M gap to his 41.8 (9.5 of 13.5 TW)
and **76 %** of the T_m gap (67 of 88 K); ~4 TW / ~20 K remain (third, smaller cause — the adiabat ratio 1.579 vs
1.69 and R_p are the sized candidates, untested). **The inner core still never appears, and T_c ends 150 K below
his 4 155 K on every convention.** So the heat budget is (mostly) the conventions and the core side is not — the
mantle conventions do not reach it. **The promotion written here at 12:40 ("C14's finding is now independent of
the conventions") was reversed the same afternoon by the next diagnostic** — see "Melting curve" below: the
inner core's absence is the light-element depression factor, a declaration, not a consequence of closing the
loop. Q_C 5.2 vs his 9.0 TW is the core-side number the table leaves as the next question (it moves 2 % across
the conventions while Q_M moves 70 %, and it is what drives the entropy budget) — *not* a claim that 9 TW would
turn ΔE positive.

**Melting curve — the diagnostic that demotes C14's finding (pre-registered Ⓧ/Ⓨ/Ⓩ, `scratchpad/c14-melting-curve-prereg.txt`;
one evaluation, no integration).** At ICB pressures Nimmo's eq. 40 (θ = 0.11) is **~540 K hotter** than `fe_prem`
(330 GPa: 5 621 vs 5 074 K). Our adiabat at the C20 T_c 4 027 K (centre 358 GPa, 5 672 K) does not meet our curve
and **does meet his — at 277 GPa, an inner core of ≈ 2 000 km** (Earth's is 1 220; at his own T_c 4 155 our
adiabat only grazes his curve, so the crossing is extremely sensitive there). **Ⓧ**: "closing the loop removes
Earth's inner core" is **demoted** to "our melting curve is colder than his". Provenance sharpens it further: the
pure-iron curves agree (Zhang+ 2015 Simon fit 6 342 K vs Alfè+ 2002's 6 300 ± 300 K at 330 GPa); the whole gap is
the **light-element depression** — ours ×0.80 (`IRON_LIGHT_ELEMENT_FACTOR`, a declared convention of
thermal-evolution models, checked against Sinmyo+ 2019's measured ICB 5 120 ± 390 K at −0.12 σ), his ×0.89 (Alfè
2002b's ab initio 700 ± 100 K for 8 mol % S/Si). Sinmyo's measurement sits on our curve and 1.3 σ below his. The decomposition the directing seat asked for (pure-iron
anchor vs depression) therefore lands on **Ⓟ, not Ⓠ**: the pure-iron anchor is not low — three sources agree
at the ICB (Zhang+ 2015 fit 6 342 K; Alfè+ 2002 6 300 ± 300 K; Anzellini+ 2013 via Mori+ 2017 `2017E&PSL.464..135M`,
secondary: Fe–Fe₃S eutectic ≈ 4 100 K at the ICB is *"about 2000 K lower than the melting points of pure Fe"* →
≈ 6 100 K) — and our 5 074 K is the pure-iron curve × 0.80, sitting between the eutectic (4 100) and pure iron
(6 100–6 300), as a depressed alloy curve should. Scope of the factor: `IRON_LIGHT_ELEMENT_FACTOR` is one declared
constant applied engine-wide through `fe_prem` (C14's inner core at the declared 3 760 K, C15's E_L/E_g, C20's
nucleation all stand on it), so **every body's inner-core verdict hangs on the same declaration** — the range is
"all of them", by construction, not by defect. So:
**on the 20 % convention (consistent with the measured ICB temperature) this model's core is too cool to freeze;
on the 11 % ab-initio depression it freezes an oversized inner core. The inner core's existence hangs on one
declared factor, and this session does not decide it.** **The honest statement this model can make is not "which factor is right" but this: in this model the
inner core's existence and size are not robust** — a declared depression factor and a few per cent of T_c
dominate the result: on his curve, T_c 4 027 → r_i ≈ 1 995 km and T_c 4 155 → 0 (128 K, 3 %, takes the inner
core from 2 000 km to nothing); on our factor there is none. **This sentence must accompany any inner-core
output of C20 on another body.** Inversion (pre-registered, report not adopt — the same kind as C14's C_r ×
1.083): with T_c fixed at 4 027 K, the factor that puts the crossing at Earth's 1 220 km is **f ≈ 0.866** —
between the two published values (0.80, 0.89), so the model *can* reproduce Earth's inner core with the factor
as the knob; at C14's 3 978 K f ≈ 0.86, at Nimmo's 4 155 K f ≈ 0.895 (his own 0.89 gives ≈ 1 228 km there —
his pair fits). Hypersensitivity in numbers: r_i runs 0 → 1 673 km across f 0.85 → 0.88 (3.5 %). The knob is
really (f, T_c) jointly and they are degenerate. Labels: Sinmyo's 5 120 ± 390 K sitting on our curve is a check
of the *curve*, not evidence that the model reproduces Earth — the model has no inner core, so it has no ICB
temperature at all; 0.80 (Stevenson-1981-lineage convention) and 0.89 (Alfè 2002b, 8 mol % S/Si) are **both
declarations, neither our derivation**. **The measurement breaks the (f, T_c) degeneracy — read against Sinmyo+ 2019 directly** (pre-registered):
our adiabat at 330 GPa is **5 490 K at the C20 T_c 4 027** (+0.9 σ of the measured ICB 5 120 ± 390), 5 424 at
C14's 3 978 (+0.8 σ), and **5 126 K at the declared 3 760 K — Sinmyo's own measured CMB temperature — matching
the measured ICB to 6 K (+0.0 σ) and sitting 53 K above our melting curve, i.e. with an inner core** (C14's 566–
572 km at 3 760). So the measured pair (CMB 3 760 ± 290, ICB 5 120 ± 390) is reproduced by our adiabat and our
factor together: **γ and f are both measurement-consistent; what is hot is the *solved* T_c**, 220–270 K above the
measured CMB value (+0.8–0.9 σ) — inside the measurement's band, but in this hypersensitive region those degrees
are the whole inner core. The tension is therefore not "f is low" (the measurement backs f) but "the energy
balance (C14) and the history (C20) close on a T_c ~1 σ above the measured one, and there the inner core is gone".
That puts the cause on the **T_c side — Q_C / the CMB boundary-layer law (eqs 37–39) at the declared bottom-layer
constants — at 1 σ significance, not more.** The two open items (inner core, Q_C 5.2 vs 9.0 TW) are one chain on
measurement evidence, held at that significance. Nothing moved; f stays 0.80, T_c stays solved.
**Not circular** — the declared 3 760 K is Sinmyo's measured CMB value, so this must be spelled out:

    input     the measured CMB temperature, 3 760 K
    through   our adiabat (γ = 1.5) and our melting curve (f = 0.80) — two independent declarations
    output    5 126 K at 330 GPa
    compared  with the measured ICB temperature 5 120 ± 390 K, which was never used → 6 K, +0.0 σ

One measured point was fed in and the other predicted to 6 K; γ and f are checked *together* by it — the
strongest comparison of the day.
**The chain, in one piece** (direction, not proof — 1 σ):

    CMB bottom boundary-layer law (eqs 37–39, declared constants κ_b, f, T₁)
      → Q_C 5.2 vs 9.0 TW (43 % low; unresponsive to the mantle conventions)
      → less heat leaves the core → the energy balance closes at a hotter T_c
      → solved T_c 4 027, +220–270 K over the measured 3 760 ± 290 (+0.8–0.9 σ)
      → a hotter adiabat (5 490 K at 330 GPa, +0.9 σ of the measured ICB)
      → in the hypersensitive region, no inner core

Q_C low ⇒ the core stays hot: the direction is right, and since Q_C did not respond to the mantle conventions,
what sets it is the boundary-layer law. **Next target, named: eqs 37–39 — listed (C25), not touched today.**
**The day's trajectory, kept on purpose** (the phenomenon stayed the same; the mechanism changed three times):
early morning — "closing the loop removes Earth's inner core" (found again after the Euler-artefact
retraction); afternoon — demoted to "our melting curve is 540 K colder" (thought to be a source difference);
re-decomposed — "the whole gap is the declared factor, 0.80 vs 0.89"; now — "f and γ both match the
measurement; what is hot is the solved T_c, and its cause is Q_C = the boundary-layer law". **Excluded today,
and to stay excluded**: the melting-curve source (pure-iron anchors agree) and the depression factor as the
cause (the measurement backs 0.80). The inversion's 0.866 is a measurement of "what this model would need to
fit Earth", not a value. The "package" hypothesis
above is *partly* supported inside our model (two conventions account for most of the mantle-side miss) and not
tested on the core side. **Nothing adopted.**

**Gate lines** (recorded, not interpreted): gate82 on `d5ac48b7` (C20 code): `GATE END sha=d5ac48b7 rc=0`, 507 PASS
(+9), FAIL 0, 12:12:43 → 12:36:59 = 1456 s, powermode 2 both ends.
