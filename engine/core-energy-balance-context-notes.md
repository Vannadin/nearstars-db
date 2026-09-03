<!-- C14 — 핵 에너지 수지(Nimmo+ 2004 식 30)로 핵 쪽 CMB 온도 T_c 를 근찾기로 푼다. 하한 선언 → 해. 사전등록 → 실행 기록 -->
# Core energy balance — context notes (C14)

2026-09-03. **§1–§3 are the pre-registration, committed before any code ran.** Owner: *"c14 진행하자"*, earlier
*"B로 가야지"* (15:51), and *"ㄱㄱ"* on running the gate on battery (`4b8e06ba`). Brief 62 step 1
(`cmb-heat-flux-context-notes.md` §5) is the measurement this stands on and is not repeated.

## 1. What is solved, and what is not

`T_c` (core-side CMB temperature) is today a **declared lower bound** (Earth 3760 K, `earth.yaml`), so `Q_CMB`
is a lower bound (2.75 TW < Q_adiabat 6.79 TW on the engine's Earth). C14 turns the bound into a **solution**:

    bottom_layer(T_c) = Q̃(T_c) · (−dT_c/dt) + M_c · H            Nimmo+ 2004 eq. 30 with eq. 31
    left: what the mantle extracts (eqs 37–39, built — cmb_flux.bottom_layer)
    right: what the core can supply — secular cooling (Q_s + Q_L + Q_g, all ∝ dT_c/dt) + radiogenic Q_R

with `dT_c/dt` **declared** (no integrator; step 1 measured that every cooling term is linear in it), so the
balance is one equation in `T_c`: **a root-find**. **Not done here**: feeding the solved `T_c` back into
`core_state` (anchors would move — a separate decision, the same reason C22's dial sits at 0); φ / dynamo
wiring (C15); Q_H (named as omitted, R_H = −27.7 MJ/kg Table 1; small and negative in entropy).

**Code facts checked before writing this** (work seat, 2026-09-03):
- `bottom_layer(t_c, t_m_base, r_cmb, …)` takes the mantle's base temperature as its own argument, from
  `interior_layers`' `cmb_temperature` (the potential-temperature declaration); **independent of T_c**. So the
  interior is solved once and the root-find sits on top — no shoot inside a shoot.
- The engine emits **no radial core profile**: `Structure` holds scalars; `core_state`'s adiabat is T(P) =
  T_cmb (ρ(P)/ρ_cmb)^γ, a function of P via `material.density`; **no gravitational potential ψ exists
  anywhere** (`interior.py`'s `psi` is porosity). Q_s (I_S = ∫ρT dV), Q_g (∫_oc ρψ dV) and Q_L (ρ_i, R_i)
  need one, so a core profile has to be **built** by this node, by one of two routes (§2).

## 2. Design — two routes, both built, each labelled

**Route A — Nimmo's analytic core, transcribed** (eqs 1–7, 9–10, 16–21; Table 1). This is the model that
produced Table 4, so **① (component-wise reproduction) is only meaningful on it**.

    ρ(r) = ρ_cen exp(−r²/L²)                                       (1)   L from (2), or Table 1's 7272 km
    M_c  = 4π ρ_cen [ −(L²/2) r e^{−r²/L²} + (L³√π/4) erf(r/L) ]₀^R   (3)
    g(r) = (4π/3) G ρ_cen r (1 − 3r²/5L²)                          (4)
    T(r) = T_cen exp(−r²/D²),  D = √(3 C_p / 2π α_c ρ_cen G)       (5)(6)   Table 1: D 5969 km
    p(r) = p_c + (4π G ρ_cen²/3)[ (3r²/10 − L²/5) e^{−r²/L²} ]_r^R  (7)
    I_S  = 4π T_cen ρ_cen [ −(A²R/2) e^{−R²/A²} + (A³√π/4) erf(R/A) ],  A² = (1/L² + 1/D²)⁻¹   (8)(9)
    Q_s  = −(C_p/T_c) I_S dT_c/dt                                  (10)
    Q_R  = M_c H                                                    (16)
    Q_L  = 4π R_i² L_h ρ_i dR_i/dt                                  (17)
    ψ(r) = (2π/3) G ρ_cen r² (1 − 3r²/10L²)   (zero at the CMB, per the text — checked by closure) (18)
    Q_g  = [ ∫_oc ρψ dV − M_oc ψ(R_i) ] β_c C_c C_r dT_c/dt          (19)
    C_c  = 4π R_i² ρ_i χ / M_oc                                     (20)
    β_c  ≈ Δρ/(χ ρ)  → Table 1's 1.1 ± 0.1 declared                  (21)
    C_r  = dR_i/dT_c — the ICB moves where the adiabat meets the melting curve:
           C_r = (T_i/T_c) / (dT_melt/dr − dT_ad/dr)|_{R_i}   (derived, textbook chain rule; the paper prints
           Gubbins' −9.56 km/K in Table 3's note as the comparison value, and for its own model dR_i/dt 444 km/Gyr
           ÷ dT_c/dt −33 K/Gyr = **−13.5 km/K** from Table 4 — the closure target for C_r)
  ⚠ `∫_oc ρψ dV` is printed as eq. 22 (with C₂, eq. 23) but the text layer garbles it; **it is evaluated
  numerically from eqs (1) and (18)** and checked by closure on Table 4's Q_g rather than transcribed.
  Constants, all Table 1 (Nimmo Table 1, layout line 436 ff.): ρ_cen 12 500, ρ₀ 7019, R 3480 km, R_i 1220 km,
  L 7272 km, D 5969 km, T_c 4100 ± 300, T_i 5500 ± 300, α_c 1.35 ± 0.15e−5, C_p 840, L_h 750 kJ/kg,
  β_c 1.1 ± 0.1, k 50 ± 20, R_H −27.7 MJ/kg. Table 2: χ₀ 4.2 (+1.5 −1.7) wt %. Table 4: dT_c/dt −33 K/Gyr,
  H 1.5 pW/kg (400 ppm K), χ 4.30 wt %, T_c 4155, T_i 5581, Q_C 9.0 = Q_s 2.0 + Q_L 2.6 + Q_g 1.6 + Q_R 2.9,
  Q_k 6.2, η_b 6.7e21, dR_i/dt 444 km/Gyr.
  For a body other than Earth, L and D are **Earth fits** and would be declarations — route A is the
  reproduction instrument, not the general path.

**Route B — the engine's own core, integrated.** From `P_cmb` inward with `material.density(P, T_ad(P))`
(T_ad the `core_state` adiabat), hydrostatics dP/dr = −ρ g, g from the enclosed mass, ψ(r) = −∫_r^R g dr
(zero at the CMB): ρ(r), g(r), T(r), ψ(r) on a 1-D grid; the same integrals numerically; R_i from
`core_state`'s `icb_pressure` mapped to radius on this grid; C_r from the two slopes at R_i (our melting curve
`iron_t_melt × 0.80` and our adiabat). **General** (any body with a core), no Earth fit. Closure check of the
route itself: its M_c must reproduce `mass × core_mass_fraction` and its P(0) the `interior_layers` centre
pressure (both are the same hydrostatics the interior solver ran).

**Three boundaries, set by the directing seat before code (2026-09-03):**
- **Route A lives in the test file only, never in the recipe.** Its consumer is the transcription test; a
  recipe-side copy would invite someone to declare Earth's core shape (ρ_cen 12 500 · L 7 272 · D 5 969) on
  another body.
- **The ∫ρψ closure is an independent calculation checked against an independent printed value, not a
  circle — and if it misses, it is reported, not adjusted.** Re-reading the garbled eq. 22 is what happens
  then.
- **C_r has two printed contexts and one derived value; none are mixed.** Gubbins' comparison model:
  −9.56 km/K (Table 3 note, printed). This paper's nominal model: dR_i/dt 444 km/Gyr ÷ dT_c/dt −33 K/Gyr =
  **−13.5 km/K — our division of two printed Table 4 values, not a printed number.** The slope derivation
  (T_i/T_c)/(dT_melt/dr − dT_ad/dr) at R_i is a third thing, derived here, carried with its own label.

*Scratch prototype before the code, recorded because it fixes what the code must reproduce (same numbers
expected in the test):* on Table 1/2/4 inputs, Q_s 1.96 (2.0) · Q_L 2.40 (2.6) · Q_g 1.47 (1.6) · Q_R 2.89
(2.9) · Q_k 6.18 (6.2) TW; T_i(model) 5 598 K (5 581); M_c 1.927e24 kg; ψ's zero point cancels in
∫ρψ − M_oc ψ(R_i) (both choices give Q_g 1.47 — checked, not assumed); root-find on the paper's own mantle
side (eq. 29 base 2 694 K) → **T_c 4 152 K (Table 4: 4 155)**, Q_C = rhs = 8.71 TW there. **All within the
pre-registered 10 %; Q_L and Q_g sit 8 % low and are reported low, not tuned.** The slope-derived C_r on the
paper's own curves (eq. 40 with Table 2's T_m0/T_m1/T_m2/θ, eq. 5, p(r) from eq. 7) is **−26.4 km/K against
the −13.5 from Table 4's ratio — a factor 2**, because the melting curve and the adiabat are nearly parallel
at the ICB (5 603 vs 5 598 K, the same knife-edge `core_state` already carries): C_r is a ratio of two nearly
equal slopes and the printed ratio is not recoverable from the printed curves at this precision. The
reproduction uses the Table 4 ratio (labelled as such); the slope route is what route B has to use, and its
sensitivity is reported with it.

**Both on the engine's Earth**, side by side: the spread between A and B on the same inputs is the width of
the density-model choice (Brief 60 saw Q_k 6.79 vs 6.2 TW for the same reason).

**Declarations, with bands** (each carried into the emitted values): `dT_c/dt` −33 K/Gyr nominal, band
**33–126 K/Gyr** (Table 3 note: Gubbins' comparison model, k = 60 — model-to-model, 4×; for an exoplanet this
is the thermal history the engine does not compute, so the solved T_c is *"T_c under an Earth-like present-day
cooling rate"* and says so); `H` 1.5 pW/kg nominal (Table 4, 400 ppm K), band **0 – 1.5 pW/kg** — floor H = 0
(the paper's own no-potassium case — §5.3 *"A model (not shown) identical to Fig. 2 but with no potassium in the core"*, extraction line 1332, and Fig. 4 *"Entropy generated with no potassium in the core"*), and the same first author uses 100 ppm K in 2020
(`2020ApJ...903L..37N`, parallel seat), 4×; C_p 840 · α_c 1.35 ± 0.15e−5 · L_h 750 kJ/kg · β_c 1.1 ± 0.1 ·
χ 4.2 wt % · R_H −27.7 MJ/kg (Table 1/2, Earth's).

**Labels on every emitted value**: Earth-calibrated model (its success criterion is "reproduce present Earth");
dT_c/dt 4× band; H 4× band with floor 0; γ = 1.5 solid on a liquid core (now under a heat flow twice over);
Q_H omitted; route (A: Earth-fit density model / B: engine profile).

**Root-find**: `f(T_c) = bottom_layer(T_c) − [Q̃(T_c)(−dT_c/dt) + M_c H]` bracketed on [T̃_m + 1 K, T_melt at
the CMB × (some factor)?] — **no**: the bracket is a physical one, stated in advance: lower end the mantle base
temperature (no jump → Q_C = 0 < right side), upper end the core adiabat's own ceiling where the whole core
would be liquid AND the ICB vanishes (R_i → 0, Q_L = Q_g = 0) — beyond that the model's terms change kind. If
f does not change sign in that bracket → ③ by name; **the bracket is not widened to make a root.**

**Contract**: new node `core_energy_balance` (name to be confirmed against `chain.yaml` conventions), recipe
`internal-heat-luminosity-methodology`, **Needs/Returns written into the methodology doc (en + ko) in the same
commit as the code** (the gate66 checklist line); edges from `cmb_heat_flux`, `core_state`, `interior_layers`,
`internal_heat_nontidal` (H is separate: core H is *not* the mantle budget — declared).

## 3. Pre-registered outcomes

- **① Table 4 reproduced component-wise on the paper's inputs (route A)** — acceptance: with T_c = 4155 K,
  dT_c/dt = −33 K/Gyr, H = 1.5 pW/kg, Table 1/2 constants: Q_s ≈ 2.0, Q_L ≈ 2.6, Q_g ≈ 1.6, Q_R ≈ 2.9 TW
  (sum 9.1 vs printed Q_C 9.0), C_r ≈ −13.5 km/K, Q_k ≈ 6.2 TW; and the root-find on the paper's own mantle
  side (eq. 29 base 2694 K, Brief 60) returns T_c near 4155 K. Tolerance stated before running: **each
  component within 10 % of its printed one-decimal value** (the printed values carry one decimal, and the
  paper's own sum is 9.1 against 9.0); a component off by more → the transcription is wrong somewhere named,
  not "close enough". *A sum that matches with components that do not is not a reproduction.*
- **② The engine's own Earth** (route B, and route A on the engine's inputs): the solved T_c reported beside
  the declared 3760 K, with the dT_c/dt and H bands as a T_c band. **No expectation written.**
- **③ No root / bracket end** → named, stop; bracket not widened.
- **④ Solved T_c outside a material domain** (core melting curve range, `GAMMA_RANGE_PA`, adiabat
  extrapolation) → refused by name. And: does the solved T_c flip `core_state`'s Earth verdict (inner core
  exists only at γ = 1.5, the C6 watch)? **Measured and reported; γ untouched.**
- **⑤ No inner core** (core_state says all-liquid): Q_L = Q_g = 0, Q_C = Q_s + Q_R — the branch exists and is
  exercised on a body that has no inner core (which roster body: to be found; if none, a synthetic input).
- **⑥ Anchors byte-identical, `--refresh` not needed** — new module, new node; `interior.py`, `core_state.py`,
  `solve()` untouched. If needed → stop and trace.
- **⑦ Gate FAIL 0, cost stated, `pmset -g` state recorded beside the time.**
- **⑧ New declarations/outputs → Needs line + domain row (en + ko) in the same commit.**

## 4. Run record — 2026-09-03

**Branches fired: ① exactly · ② answered (no expectation was written) · ③ did not fire · ④ answered, and
the answer is the finding · ⑤ both branches exercised · ⑥ anchors untouched · ⑧ done in the same commit.**

- **① Route A reproduces Table 4 component by component** (`test_core_energy.py` §1, on Table 1/2/4 inputs):
  Q_s 1.96 (2.0, −2 %) · Q_L 2.40 (2.6, −8 %) · Q_g 1.47 (1.6, −8 %) · Q_R 2.89 (2.9) · Q_k 6.18 (6.2) TW;
  T_i 5 598 K (5 581); M_c 1.927e24 kg; sum 8.71 against the printed Q_C 9.0 / component sum 9.1. Every
  component inside the pre-registered 10 %; **Q_L and Q_g sit 8 % low and stay low** — the shortfall is
  reported, not tuned (a candidate cause, not verified: the paper's ρ_i may carry the ICB density jump it
  says it "incorporates" for compositional convection; eq. 1 alone does not). ψ's zero point cancels in Q_g
  (both choices identical to 1e-6). Root-find on the paper's own mantle side (eq. 29 base 2 694 K):
  **T_c 4 152 K against the printed 4 155.** C_r's three values kept apart: Gubbins −9.56 (printed, other
  model) · Table 4 ratio −13.45 (our division) · slope-derived **−26.5 km/K** (ours; melting curve −0.434 vs
  adiabat −0.383 K/km at the ICB — nearly parallel, so the ratio is a knife-edge and the printed ratio is not
  recoverable from the printed curves; the reproduction uses the Table 4 ratio, labelled).
- **② The engine's own Earth, route B** (`core_energy.solve(1.0, 0.325, 0.547, 135.3, 2526, 3760)`):
  **T_c solved 3 978 K, band 3 750–4 284 K** (the four corners of dT_c/dt 33–126 K/Gyr × H 0–1.5 pW/kg, all
  four with a root), **+218 K above the declared 3 760 K**. There Q_C = **4.91 TW = Q_s 2.00 + Q_R 2.91**,
  Q_L = Q_g = 0 (see ④). Balance residual 8e-16; profile mass residual −0.33 %; profile centre pressure
  346 GPa. Solve 1.6 s. So the declared lower bound is a lower bound by 218 K on this model, and the flux it
  implied (2.75 TW, Brief 60) rises to 4.91 TW — **now inside Nimmo's printed 4.5–9 TW range**, on this
  model's terms (Earth-calibrated; dT_c/dt and H declared). Still below Q_adiabat 6.79 TW at k = 50 (Brief
  60) — that comparison is C15's, not made here.
- **④ — the finding.** On the route-B profile **Earth has no inner core at any T_c above ≈ 3 600 K**, the
  declared 3 760 K included, while `core_state` at the same 3 760 K reports an inner core at 351.4 GPa with a
  centre margin of −17.6 K (its own "thin"; the in-chain Earth run, `run.py bodies/earth.yaml`). The
  mechanism, read from both codes and not tuned: `core_state` takes P(r) from `interior_layers`, which solved
  the **lower-bound** temperature column (core 2 526–2 671 K, centre 358.5 GPa), and lays the **hot** adiabat
  (from 3 760 K) on that cold pressure axis; route B integrates the pressure **at the hot adiabat's own
  temperature**, reaches only 346 GPa at the centre (a hotter, less dense column), and its adiabat then stays
  above the melting curve everywhere. **Both are self-consistent to their own assumption and they disagree on
  whether Earth's inner core exists** — the γ = 1.5 knife-edge `core_state` already reports (Brief 42:
  the verdict flips at γ 1.514), now shown to flip also on *which temperature the pressure profile is
  evaluated at*. Nothing is moved: γ stays 1.5, `core_state` is untouched, `interior_layers` is untouched.
  What this means for the emitted numbers: `has_inner_core_solved` is False for Earth here and True in
  `core_state`; both are emitted with their assumption. Whether the interior solver should carry the hot
  core (a declared core-side temperature entering the density integration) is an **owner decision** — it
  moves anchors and is exactly the feed-back C14 was scoped not to do.
- **③** did not fire: the physical bracket [max(T̃_m, T_melt(P_cmb)) + 1 K, 3 T̃_m] = [3 216, 7 578] K holds one
  sign change. (Two bracket corrections were needed before code ran right, both narrowing, neither widening:
  the low end must sit above the CMB melting temperature — below it the core is solid at the CMB and
  eq. 30's outer-core terms do not apply; and an all-liquid core is **not** a bracket end but the Q_L = Q_g = 0
  regime, which the first draft had wrongly used as the top.)
- **⑤** Both branches on one profile: at 3 300 K an inner core of 3 254 km with Q_L 3.11, Q_g 0.25 TW; at
  4 000 K all liquid, Q_L = Q_g = 0.
- **⑥** `--fast` passes; `interior.py`, `core_state.py`, `solve()` untouched; no `--refresh`.
- **⑧** Needs line and contract section written in the same commit (en + ko); `check_contracts` passes with the
  new node; `chain.py check` 49 nodes / 188 edges; `check_via --gate` passes.
- **Profile method, for the record**: inward from the CMB, m falling from M_core, the innermost 2 % of the
  radius (10⁻⁵ of the volume) not integrated because the 0.3 % mass residual diverges as G m/r² at r → 0; the
  residual is emitted as `core_profile_mass_residual`.
- **⑦** Gate: below, with `pmset -g` beside the time.
