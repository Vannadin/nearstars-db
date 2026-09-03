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
all carry C_r, so **the C14 diagnosis (−8 % in Q_L/Q_g from C_r) reappears as −6 % here** and is not tuned.
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
