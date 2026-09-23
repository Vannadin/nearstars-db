# Samuel+ 2021 매개변수 열진화의 상수 한 벌 — 식은 2021, 맞춰진 값과 그 모형의 상수는 Samuel+ 2019 BML main (판 1: 상수만)
"""Constants for the Samuel+ 2021 parameterized thermal evolution, one set, not mixed.

Plate 1 of the thermal-evolution item: **constants only**. Nothing reads this module yet, so no
contract declares it. The equations arrive in plate 2 and sit beside `core_history`, not inside it.

Sources, and why the set is not mixed:

* **Equations** — Samuel, Ballmer, Padovan, Tosi, Rivoldini & Plesa 2021, JGR Planets 126,
  e2020JE006613 (`2021JGRE..12606613S`), eqs (10)–(22).
* **Fitted values** — Samuel, Lognonné, Panning & Lainey 2019, Nature 569, 523
  (`2019Natur.569..523S`), Extended Data Table 1, **BML (main set)** column. They were inverted
  inside the 2019 model, so they are one object with that model's own constants: swapping one of
  them for a 2021 value (`E* 200` · `V* 5` · `η₀ 10²⁰` · `Λ 10`) leaves the rest without the fit that
  chose them.
* **Fixed constants** — from the 2019 Supplementary Information Tables 1–2. Where the 2021 Table 1
  prints the same value this is noted; where it prints a different one, **the 2019 value is taken**
  and the difference is written next to it (`Λ`, `ϵ_c`).

Page numbers are **PDF pages** of the cached files, read off a rendered page — the text layer drops
superscripts (`L_m = 6×10⁵` comes out as `6 × 10`) and cannot tell `10^(20.5±0.3)` from
`10^20.5 ± 0.3`. Where a phrase survives in the text layer intact it is also given as an anchor.
⚠ **Nothing checks those anchors.** The paper cache is not tracked and `check_refs` does not scan
this file; each phrase was counted by hand against the cached text (one match each, 2026-09-23).
They are pointers for a reader, not a guarded citation.

⚠ **`η₀`'s uncertainty is inside the exponent.** It is stored as a base-10 logarithm with its own σ,
so the two readings cannot be confused in code — the difference is an order of magnitude.

⚠ **`η₀` only means something with its reference state.** 2019 SI Table 2 (PDF p44) gives
`P_ref = 3×10⁹ Pa` and `T_ref = 1600 K`, and 2021 Table 1 (PDF p5) prints the same pair — that is
what lets the 2019 viscosity stand inside the 2021 equations.

⚠ **Not constants, so not here.** `ϵ_m` is *"constantly updated"* (2021 PDF p11) and the Stefan
number `S_t` is *"time-dependent"* (2021 PDF p12); both are `variable` in 2019 SI Table 1. Initial
temperatures, surface gravity and the two radii are inputs of a run, not constants of the model.
"""

# ── Fitted — Samuel+ 2019 Extended Data Table 1, BML (main set) — 2019 PDF p10 ─────────────────
# (value, 1σ). Transcription blob 4038984b. "Quantities listed correspond to constant or to
# present-day values unless specified otherwise."
E_STAR_J_PER_MOL = (120.0e3, 15.0e3)        # E*   mantle effective activation energy
V_STAR_M3_PER_MOL = (7.3e-6, 2.0e-6)        # V*   mantle effective activation volume
ETA0_LOG10_PA_S = (20.5, 0.3)               # η₀ = 10^(20.5 ± 0.3) Pa s — σ is on the exponent
K_D_W_PER_M_K = (5.0, 1.0)                  # k_d  thermal conductivity of the basal layer
D_D_M = (165.0e3, 20.0e3)                   # D_d  thickness of the basal layer
D_CR_M = (67.0e3, 2.0e3)                    # D_cr crustal thickness (present day)

# ── Viscosity reference state — 2019 SI Table 2, PDF p44 (= 2021 Table 1, PDF p5) ─────────────
P_REF_PA = 3.0e9
T_REF_K = 1600.0
R_GAS_J_PER_MOL_K = 8.31                    # as printed by both, not CODATA — the fit used this

# ── Fixed constants — 2019 SI Table 1, PDF p43 (2021 Table 1, PDF p5, prints the same) ─────────
T_SURFACE_K = 220.0
RHO_MANTLE_KG_M3 = 3500.0
RHO_CORE_KG_M3 = 7200.0
RHO_CRUST_KG_M3 = 2900.0
CP_MANTLE_J_PER_KG_K = 1142.0
CP_CRUST_J_PER_KG_K = 1000.0
CP_CORE_J_PER_KG_K = 840.0
K_MANTLE_W_PER_M_K = 4.0                    # ⚠ not our 3.456 (Nimmo+ 2004 Earth closure) — one set
K_CRUST_W_PER_M_K = 2.5
ALPHA_SILICATE_PER_K = 2.0e-5
L_MANTLE_J_PER_KG = 6.0e5                   # latent heat of fusion/crystallization
RA_CRITICAL = 450.0                         # 2021JGRE..12606613S.txt@«Rac = 450» (2021 PDF p12)

# ── The two where the papers differ — 2019 SI Table 1, PDF p43, taken ─────────────────────────
# ⚠ Crustal HPE enrichment, crust ÷ primitive mantle
#   (2019Natur.569..523S-si.txt@«constant crustal enrichment factor», 2019 SI PDF p7).
#   2021 Table 1 (PDF p5) prints 10 and says the approach is the 2019 one; the 2019 table prints 5,
#   and the fitted values above were inverted with 5.
CRUST_ENRICHMENT = 5.0
# ⚠ Mean core temperature ÷ temperature at the top of the core. 2019 prints 1.05; 2021 gives no
#   number, only that it is 2021JGRE..12606613S.txt@«computed only once» (2021 PDF p11).
EPSILON_CORE = 1.05

# ── Boundary-layer coefficients — printed in the body text, identical in both papers ───────────
A_RH = 2.54        # T_l = T_m − a_rh R T_m²/E*  2021JGRE..12606613S.txt@«with arh = 2.54» (2021 PDF p11)
BETA_U = 0.335     # δ_u = (…)(Ra_c/Ra)^β_u     2021JGRE..12606613S.txt@«where βu = 0.335» (2021 PDF p12)
RA_DELTA_B_COEFF = 0.28   # Ra_δb = 0.28 Ra_i^0.21  2021JGRE..12606613S.txt@«0.28 Rai» (2021 PDF p12)
RA_DELTA_B_EXP = 0.21

# ── Layered case only — 2021 eq (20), PDF p13 ─────────────────────────────────────────────────
DELTA_T_B_COEFF = 1.43    # ΔT′_b = 1.43 R T_m²/E*  2021JGRE..12606613S.txt@«1.43RT» (Deschamps & Sotin 2000)

# ── Heat-producing elements — Wänke & Dreibus 1994, as printed by 2021 on PDF p4 ──────────────
# 2021JGRE..12606613S.txt@«inferred by Wänke and Dreibus (1994) (i.e., U = 16 ppb, Th = 56 ppb,»
U_PPB = 16.0
TH_PPB = 56.0
K_PPM = 305.0
