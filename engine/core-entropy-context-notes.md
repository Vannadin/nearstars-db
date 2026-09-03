<!-- C15 — Nimmo+ 2004 식 (43) 의 현재 시점 엔트로피 생성 φ 여섯 항. 판정이 아니라 밴드. 3 Gyr 진술은 C20 없이는 거절. 사전등록 → 실행 기록 -->
# Core entropy production φ — context notes (C15)

2026-09-04. **§1–§3 are the pre-registration, committed before any code ran.** Owner's evening goal, relayed:
*"자기장쪽 배선 최대한"*; C14 (`core-energy-balance-context-notes.md`) is the prerequisite and stands. The
parallel seat's survey fixed the scope: **φ can be built; a verdict cannot.**

## 1. What is built, and what is refused by name

Nimmo+ 2004 eq. (43), present day: **ΔE = E_R + E_s + E_L + E_H + E_g − E_k**, six terms, each transcribed at its
place (⚠ the paper is two-column; whole-page `-layout` mixes the columns — read with `pdftotext -x 30 -W 290` /
`-x 310 -W 290`, the parallel seat's cut; eq. 26 had the neighbouring column's δ_t bleeding into it and was
filtered by closure):

    E_R = (M_c/T_c − I_T) H                                  (16)
    E_s = (C_p/T_c)(M_c − I_S/T_c) dT_c/dt                    (10)  ⚠ the 1/T_c prefactor: without it E_s is 4×10⁵ off
    E_L = Q_L (T_i − T_c)/(T_c T_i)                          (17)
    E_g = Q_g / T_c                                          text: "E_g is simply Q_g/T_c"
    E_H = −R_H [ … ] C_c dR_i/dt                             (24)  ⚠ bracket order unreadable in the text layer; sign
                                                                   recovered by closure on the printed −134 — see §2
    E_k = 16π k R⁵ / (5 D⁴)                                  (26)
    I_T = ∫ ρ/T dV                                           (11)/(13) by D ≷ L — evaluated numerically here on the
                                                                   analytic profile, closed on E_R = 89

E_s cannot be obtained by scaling Q_s — Q_s ∝ I_S while E_s ∝ (M_c − I_S/T_c), not a constant ratio; I_S is kept
separately (C14 has it). E_H has no energy-side partner (*"The quantity Q_H = 0"*) yet is −134 MW/K on Earth — a
term that has to be built, and it is negative and large.

**Refused by name — the 3 Gyr statement.** The paper's criteria are three (§5.2, read in the column cut): *"first,
ΔE at the present day must be positive; secondly, the mean of the entropy production over the last 3.1 Gyr (ΔĒ)
must also be positive; and finally, the minimum value of entropy production, ΔE_min, must be positive over the
same period."* Two of the three are history quantities, and **the discriminating one is ΔE_min** (Table 5: eight of
nine rows negative; §5.3: increasing χ₀ *"increases the present-day entropy production by 25 per cent but has no
effect on ΔE_min"* — present value and minimum move independently). **A present-day φ > 0 does not imply a
3-Gyr dynamo.** That statement needs the integrator — **C20 is its consumer, and this is C20's first real one.**

**The output is a band, not a verdict.** §5.2: *"the excess entropy required is probably ∼ 100 MW K⁻¹, but could lie
anywhere within the range 0.1–1000 MW K⁻¹"*, and the paper itself uses no threshold: *"any positive ΔE is assumed
sufficient to drive the geodynamo"*. §6.2 (the last-page discussion): Roberts+ 2003's 2 TW Ohmic heating *"implies
ΔE ≈ 400 MW K⁻¹"*, while *"a less extreme value of ≈100 MW K⁻¹ makes it easier for models lacking potassium"* —
**the paper's own Earth, 351, sits between the two readings** (fails at 400, passes at 100), and k = 50 ± 20 alone
sweeps ΔE across both (E_k ∝ k — a proportional estimate, **not a printed number**, labelled so). → `ΔE > 0` is
adopted as the paper's choice **and labelled as threshold-avoidance**; φ is emitted with the k · H · dT_c/dt bands.

**Not wired into `dynamo_rocky`'s verdict.** A threshold that cannot decide has no standing to overwrite the
ladder; the paper keeps Q_C-vs-Q_k and φ side by side. C15 ends at the φ node; replacing the ladder is an owner
decision. Anchors, γ, `core_state`, `interior` untouched; nothing fed back; no default changed.

**The all-liquid Earth (C14's finding) is the paper's own case**: abstract — *"prior to this time the geodynamo was
sustained by cooling and radioactive heat production within a completely liquid core"*; §5.2 — *"ΔE reaches its
minimum value of 134 MW K⁻¹"* before solidification. Without an inner core E_L = E_g = E_H = 0 (all carry
dR_i/dt) and **ΔE = E_R + E_s − E_k**. What keeps that positive in the paper is core potassium (§5.3: no potassium
→ *"a reduction in present-day core entropy production of 45 per cent"*); **our H band's floor is 0, so the H = 0
corner's φ sign is the honest corner and is emitted.**

## 2. Pre-measured on the paper's inputs (scratch, before code; the code must reproduce these)

Route A (test file only, as in C14), Table 1/2/4 inputs, C_r = the Table 4 ratio: E_R 89.3 (89) · E_s 64 (64, once
the 1/T_c prefactor is in) · E_L 148.8 (159, −6 %) · E_g 353 (375, −6 %) · E_k 202.1 (202) MW/K; Q_k 6.18 TW
(6.2). **E_H: with the bracket read as [∫_oc ρ/T dV − M_oc/T_i] the term comes out +125; the printed value is
−134. The magnitude matches to −6 % (the same C_r factor as E_L, E_g); the sign does not.** The bracket order
[M_oc/T_i − ∫_oc ρ/T dV] gives −125. **Adopted with that label — "sign recovered by closure, not read"** — the
same class as Brief 60's eq. 29 reading; the alternative (a sign convention on R_H between G2 and this paper)
is not distinguishable from the text layer. **ΔE 328 vs printed 351 (−6.5 %)** on that reading. E_L · E_g · E_H
all carry C_r, so **the C14 diagnosis (−8 % in Q_L/Q_g from C_r) reappears as −6 % here** and is not tuned. **Correction 2026-09-04**: the factor's name is not C_r — C_r's rounding band is ±1.7 % and dR_i/dt is printed — but the shared `R_i²ρ_i·dR_i/dt` that E_L, E_g, E_H carry and E_R, E_s, E_k do not; the −8 % vs −6 % gap is the Q column's two-digit rounding (E_g/Q_g = 1/T_c exactly). Cause unresolved; see `core-energy-balance-context-notes.md` §retraction.
Two more scratch numbers on the *paper's* inputs, recorded because they shape the engine-Earth expectation
that is deliberately not written: with the inner-core terms removed (E_L = E_g = E_H = 0), present-day Earth
values give **E_R + E_s − E_k = −49 MW/K**, and at H = 0 **−138 MW/K** — i.e. on this model a completely liquid
core at *today's* T_c and cooling rate does not make entropy; the paper's early all-liquid dynamo lives at a
hotter, faster-cooling epoch (its minimum 134 is a history value). Whether the engine's Earth lands there is ②.

## 3. Pre-registered outcomes

- **①** Route A reproduces Table 4's six entropy components within 10 % each (E_R, E_s, E_k expected exact;
  E_L, E_g, E_H expected ≈ −6 %, the C_r factor, left low); ΔE within 10 % of 351; E_k = 202.0 and Q_k = 6.17
  closed by the parallel seat and re-closed here.
- **②** The engine's Earth: φ at the solved T_c (3 978 K, C14) with three bands — k 30–70, H 0–1.5 pW/kg,
  dT_c/dt 33–126 K/Gyr. **No expectation written.**
- **③** No inner core → E_L = E_g = E_H = 0 exactly, ΔE = E_R + E_s − E_k (the solved Earth is that case).
- **④** The H = 0 corner's φ sign on the engine's Earth: **reported, no expectation.**
- **⑤** The 3-Gyr refusal goes out by name on every emitted φ, naming C20 as the consumer.
- **⑥** Anchors byte-identical, no `--refresh` (new node).
- **⑦** Gate FAIL 0, time, `pmset` at both ends.
- **⑧** Needs/Returns and the domain row (en + ko) in the same commit as the code.

## 4. Run record — 2026-09-04

**Branches: ① fired · ② answered (no expectation was written) · ③ exercised both ways · ④ answered · ⑤ by
name · ⑥ untouched · ⑧ same commit.**

- **① Route A reproduces Table 4's six entropy components** (`test_core_entropy.py` §1, Table 1/2/4 inputs,
  C_r = the Table 4 ratio): E_R 89.3 (89) · E_s 63.8 (64) · E_L 148.8 (159, −6 %) · E_H −125.3 (−134, −6 %) ·
  E_g 353.3 (375, −6 %) · E_k 202.1 (202) MW/K; **ΔE 327.7 vs printed 351 (−7 %)** — every component inside
  the pre-registered 10 %; the three C_r-bearing terms sit 6 % low and stay low (C14's diagnosis, not tuned).
  E_k (eq. 26) 202.1 and Q_k 6.18 TW re-close the parallel seat's 202.0 / 6.17. The two closure-recovered
  readings are pinned in the test: E_s without the 1/T_c prefactor is 2.6×10⁵ MW/K (the relayed formula);
  E_H with the other bracket order is +125 against the printed −134. **Found by working back, not by reading.**
- **② The engine's Earth at C14's solved T_c = 3 978 K** (inputs from `interior.solve()`): **ΔE = −69 MW/K**
  = E_R 99 + E_s 74 + E_L 0 + E_H 0 + E_g 0 − E_k 242. **Band −264 … +238 MW/K** over the eight corners of
  k 30–70 × H 0–1.5 pW/kg × dT_c/dt 33–126 K/Gyr — **4 of 8 corners positive; the band straddles zero.**
  Scan of the single axes (scratch `c15_proto.py`): k 30 → +28, k 70 → −166; dT_c/dt −126 K/Gyr → +141;
  **H = 0 → −167 (④)** — **and that corner is the structure the paper names, not a coincidence**: what keeps
  the paper's inner-core-free early Earth positive is core potassium (*"no potassium in the core results in …
  a reduction in present-day core entropy production of 45 per cent"*, §5.3); our H band's floor is 0, so the
  budget collapses there by construction. **Three labels ride on the −69, large, because without them it
  reads as "Earth has no dynamo" — the same misreading Q_CMB 2.75 TW invited this morning**: the required
  excess is 0.1–1 000 MW/K (no threshold decides); the band straddles zero (4 of 8 corners positive); **any one
  of the three declarations alone flips the sign** (k 30 / dT_c/dt −126 / H nominal vs 0). That is the honest
  summary of ②. **E_k 242 vs 202 is two models, not a disagreement**: 202 is eq. 26's closed form, derived
  under the Gaussian core's ∇T/T = −2r/D², which does not hold on our ρ^γ adiabat; 242 is eq. 25 integrated
  on our own profile. Route A (the test) uses the paper's model throughout and route B (the recipe) uses our
  profile throughout — **checked: `entropy_terms` reads only the C14 profile, C14's terms and the declared
  constants; no term of route B comes from the paper's model.** E_k is ~20 % sensitive to the core temperature
  model, and **the sign does not turn on that choice**: with E_k set to 202, ΔE is −29 — still negative.
  **Cross-check between the two budgets**: in C14 the two C_r-bearing energy terms (Q_L, Q_g) sit 8 % low; here
  the three C_r-bearing entropy terms (E_L, E_g, E_H) sit 6 % low, same direction, and the C_r-free terms are
  exact in both — the energy and entropy budgets independently point at the same unprinted C_r
  (`core-energy-balance-context-notes.md` §4 ①).
- **③** Same profile, two T_c: at the declared 3 760 K (inner core 566 km) ΔE = **+125** with E_L 69, E_g 170,
  E_H −56; at 4 000 K (all liquid) ΔE = −70 with E_L = E_g = E_H = 0 exactly.
- **What ② means, said carefully.** On this model the engine's Earth *at the energy balance's own solution*
  makes **no** present-day entropy at the nominal declarations — and it does at the declared lower-bound T_c,
  where the inner core still exists. That is C14's finding (closing the loop removes the inner core, and with
  it the two largest entropy terms) arriving at the entropy budget, exactly as C14 §5 ④ predicted it would.
  The paper's own all-liquid case keeps ΔE positive only at an earlier, hotter, faster-cooling epoch (its
  134 minimum is a history value) and with core potassium; at *today's* T_c and cooling rate even the paper's
  numbers give E_R + E_s − E_k = −49 (§2). **This is not a verdict about Earth's dynamo** — the threshold cannot
  decide (0.1–1 000), the band straddles zero, E_k is model-dependent by 20 %, and the whole thing sits on a
  declared cooling rate and a declared H. It is the honest present-day number on an Earth-calibrated model,
  with its bands, and the 3-Gyr question is refused by name (C20).
- **⑤** `entropy_history_verdict = "cannot-say (needs C20)"` on every result; the gate row asserts it.
- **⑥** `--fast` passes; no path function touched; no `--refresh`. Test cost 6.6 s.
- **⑧** Contract (en + ko), chain node + six edges (the `→ dynamo_rocky` one `status: gap` by design — not
  wired), registry import, `check.sh` row; `chain.py check` 50 nodes / 194 edges; `check_via --gate` and
  `check_contracts` 10/10 pass.
- **Numerical condition of E_R and E_s (directing seat's question, measured 2026-09-04, values unchanged).**
  Both are differences of nearly equal quantities. On the engine's Earth at 3 978 K:

      steps   I_T         M_c/T_c     left (% of M_c/T_c)  E_R    | I_S/T_c     M_c        left   E_s    E_k     ΔE
       100    4.271e20    4.879e20    12.5 %               91.2   | 2.297e24    1.941e24   18.4 % 78.7   249.5   −79.6
       400    4.221e20    4.879e20    13.5 %               98.7   | 2.278e24    1.941e24   17.4 % 74.4   241.8   −68.8  ← shipped
      1600    4.209e20    4.879e20    13.7 %              100.6   | 2.273e24    1.941e24   17.1 % 73.3   239.8   −66.0
      6400    4.206e20    4.879e20    13.8 %              101.0   | 2.272e24    1.941e24   17.0 % 73.0   239.4   −65.3

  **One digit cancels** (13–14 % of M_c/T_c survives in E_R, 17 % of M_c in E_s) — not a significant-figure
  warning. **Step sensitivity ≈ 5 % on ΔE** (−68.8 → −65.3 from 400 to 6 400 steps; I_T itself moves 0.4 %,
  amplified ~5× by the difference), **two orders below the declaration band (−264 … +238); the sign does not
  turn on it.** Cause, in one sentence: *the profile is RK4 and converges to 0.003 %, but the integrals on its
  samples are first-order midpoint sums, O(h) — two layers, two convergence orders*; it applies to every term
  built on I_S, I_T, ∫ρψ, including C14's Q terms, where without cancellation it is 0.1–0.5 % (Q_s 2.0006 →
  1.9951 TW, total 0.13 %, 400 → 6 400 steps). Route A's 10 % reproduction on the paper's model (4 000-point
  analytic integrals) is the evidence that the conditioning is not destructive. **Frozen as gate rows** rather
  than left as a label: `entropy_integration_width` = |ΔE(4× steps) − ΔE| is emitted live (≈ 2.7 MW/K) and
  gated at < 10 MW/K; C14's test gates the energy total's 4× move at < 0.5 %. The shipped step count stays
  400 — the width rides on every result, so nothing is quoted that the code does not re-measure.
- **⑦ Gate on `ffd9602c`: FAIL 0, 484 PASS (+12 = `test_core_entropy`'s rows), 02:11:52 → 02:32:36 = 1 244 s,
  AC 100 % `powermode 2` at both ends** — mains branch (1 224–1 362); the new test's 6.6 s is inside the noise.
