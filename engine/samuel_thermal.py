# Samuel 매개변수 열진화의 입력 한 벌 — 식은 Samuel+ 2021, 재현 목표는 Samuel+ 2023 그림 1 BML 예시 모형 (판 1: 상수만)
"""Inputs for the Samuel parameterized thermal evolution, one set, not mixed.

Plate 1 of the thermal-evolution item: **values only**. Nothing reads this module yet, so no
contract declares it. The equations arrive in plate 2 and sit beside `core_history`, not inside it.

What each block is, and where it comes from:

* **Equations** — Samuel, Ballmer, Padovan, Tosi, Rivoldini & Plesa 2021, JGR Planets 126,
  e2020JE006613 (`2021JGRE..12606613S`), eqs (10)–(22).
* **The reproduction targets** — Samuel et al. 2023, Nature 622, 712 (`2023Natur.622..712S`),
  Fig. 1: *"One model among the best 50"*, twice. Panels g–l are the **BML** (heterogeneous-mantle)
  case, plate 4's target; panels a–f are the model **without** a BML, plate 2's target.
  ⚠ In the source data both columns carry `Tc.dat` and `Tm.dat` of the same name and the same size
  (23 903 B), and they run in opposite directions. Both sit in `METADATA_BML/DATA_FIG1/` inside
  `41586_2023_6601_MOESM3_ESM_rev.zip`: `PANEL_A`–`PANEL_F` and `PANEL_G`–`PANEL_L`.
* **Fixed values** — 2023's SI §3 says the parameters it inverts for *"are those listed in Drilleau
  et al. [2022]"*; the values that are held fixed are in Drilleau et al. 2022, JGR Planets 127,
  e2021JE007067 (`2022JGRE..12707067D`), §4.1.2.
* **Inherited by equation reference** — Drilleau §4.1.2 hands the equations to *"Samuel et al.
  (2019) and references therein"*; neither 2023 nor Drilleau prints these values. They are taken
  from the 2019 SI (Tables 1–2 and the body text) and **graded lower** than a printed value: no sentence says 2023 used
  them.
* **Auxiliary reference** — 2023 Extended Data Table 1, BML (main set): the mean ± σ of the best
  1 000 models. Kept for reporting a distance only; a run on mean inputs has no duty to produce
  the mean output.

Page numbers are **PDF pages** of the cached files, read off a rendered page — the text layer drops
superscripts (`5×10²⁰` comes out as `5 × 1020`). Source-data values were read from the files
themselves.

⚠ **Not constants, so not here.** `ϵ_m` and the Stefan number `S_t` are updated every step. The
crustal enrichment `Λ` and the basal-layer conductivity `k_d` were **inverted** in 2023 and the
example model's values are not published, so only the range each is to be scanned over is given.
The basal-layer enrichment (`Λ_d`, `‾Fe#_d`) belongs to plate 3.
"""

# ── Reproduction target — 2023 Fig. 1 g–l, the BML example model ──────────────────────────────
# Printed in the caption (2023 PDF p2): "g–l, With a BML (heterogeneous mantle), with
# η₀ = 5 × 10²⁰ Pa s, E* = 110 kJ mol⁻¹, V* = 4.4 cm³ mol⁻¹."
ETA0_PA_S = 5.0e20
E_STAR_J_PER_MOL = 110.0e3
V_STAR_M3_PER_MOL = 4.4e-6
# Read from the source data, not printed. `PANEL_J/rho_profile.dat` (density, radius [km]):
#   rows 102–103 are the largest density step (Δρ 1 334.28) at 1 646.1762690 km — the core;
#   rows 202–203 are the next (Δρ 729.78) at 1 814.9469300 km — the top of the BML.
R_CORE_M = 1646.1762690e3
R_BML_TOP_M = 1814.9469300e3
D_D_M = R_BML_TOP_M - R_CORE_M              # 168.770661 km
# `PANEL_H/Tm.dat` and `Tc.dat`, first row. ⚠ That row is t = 0.001 Gyr, not t = 0.
T_MANTLE_0_K = 1815.5593199821958
T_CORE_0_K = 2158.1024424461625
T_INITIAL_ROW_GYR = 0.001

# ── Reproduction target for plate 2 — 2023 Fig. 1 a–f, the model without a BML ─────────────────
# Same caption (2023 PDF p2, 600 dpi render): "a–f, Without a BML (homogeneous mantle), with
# η₀ = 6 × 10²¹ Pa s, E* = 300 kJ mol⁻¹, V* = 3.8 cm³ mol⁻¹."
ETA0_NO_BML_PA_S = 6.0e21
E_STAR_NO_BML_J_PER_MOL = 300.0e3
V_STAR_NO_BML_M3_PER_MOL = 3.8e-6
# `PANEL_D/rho_profile.dat`: rows 102–103 are the largest density step (Δρ 1 796.02) at
# 1 834.637473 km — the core. The next step (rows 402–403, Δρ 389.85 at 3 317.74 km) is the crust;
# there is no BML step.
R_CORE_NO_BML_M = 1834.637473e3
# `PANEL_B/Tm.dat` and `Tc.dat`, first row — t = 0.001 Gyr again, the same T_INITIAL_ROW_GYR.
T_MANTLE_0_NO_BML_K = 1752.7913502870781
T_CORE_0_NO_BML_K = 2191.8284607057844

# ── Fixed — Drilleau et al. 2022 §4.1.2, PDF p9 ────────────────────────────────────────────────
R_PLANET_M = 3389.5e3
T_SURFACE_K = 220.0
K_MANTLE_W_PER_M_K = 4.0                    # ⚠ not our 3.456 (Nimmo+ 2004 Earth closure) — one set
K_CRUST_W_PER_M_K = 2.5
L_MANTLE_J_PER_KG = 6.0e5                   # latent heat of melting–crystallization
MELT_EXTRACTION_BELOW_PA = 7.4e9            # melt rises to build crust only at P < 7.4 GPa
P_REF_PA = 3.0e9                            # viscosity reference state, "3 GPa and 1600 K"
T_REF_K = 1600.0
# Bulk silicate HPE — the EH45 chondrite composition (K/Th 5 300).
# ⚠ U 16 ppb · Th 56 ppb · K 305 ppm is printed on the same page as a **comparison** (Wänke &
#   Dreibus 1994, G. J. Taylor 2013) — the set 2023 did not use. It is also what Samuel+ 2021 used.
U_PPB = 14.0
TH_PPB = 54.0
K_PPM = 284.0

# ── Scanned, not fixed — the example model's values are not published ─────────────────────────
# Crustal enrichment factor. Range: Drilleau Table 2, PDF p10 ("5–20", Gaussian). ⚠ Pre-registration
# v2-4 supersedes amendment 27's reading: Drilleau's "crust to the bulk silicate envelope" is a ratio of
# concentrations, the same Λ as 2019 SI's "relative to the primitive mantle", and it is used in 2019 SI
# eq. (22)'s form, the volumetric ratio H_cr/H_pm (our interpretation). Its ceiling is Λ ≤ V_sil/V_cr;
# a run that crosses it refuses by name, not clips (`samuel_model.heat_split`).
CRUST_ENRICHMENT_SCAN = (5.0, 20.0)
# Basal-layer conductivity: 2023 SI §3, PDF p11 — "sampled between 4 and 16 W m⁻¹ K⁻¹", and its
# posterior "was similar to the regular mantle value that we fixed to 4".
K_D_SCAN_W_PER_M_K = (4.0, 16.0)

# ── Inherited by equation reference — 2019 SI, Table 1 (PDF p43) unless the line says otherwise ─
# grade: inherited-by-equation-reference. Neither 2023 nor Drilleau prints these numbers.
EPSILON_CORE = 1.05                         # mean core temperature ÷ temperature at the top of the core
# a_rh and β_u are not rows of Table 1: both are printed in the SI body, PDF p3, under eq. (8).
A_RH = 2.54                                 # T_l = T_m − a_rh R T_m²/E*   (also 2021 PDF p11)
BETA_U = 0.335                              # δ_u = (…)(Ra_c/Ra)^β_u        (also 2021 PDF p12)
RA_CRITICAL = 450.0                         # Choblet & Sotin 2000          (also 2021 PDF p12)
R_GAS_J_PER_MOL_K = 8.31                    # SI Table 2, PDF p44 — as printed, not CODATA
# ⚠ The 2021 equations also need these. In Drilleau's framework density, thermal expansion and
#   specific heat are **not fixed** — "bulk mantle properties (density, thermal expansion, specific
#   heat) are deduced" from the composition with Perple_X (§4.1.2, PDF p9). The 2019 constants stand
#   in for them here, at the same lowered grade.
RHO_MANTLE_KG_M3 = 3500.0
RHO_CORE_KG_M3 = 7200.0
RHO_CRUST_KG_M3 = 2900.0
CP_MANTLE_J_PER_KG_K = 1142.0
CP_CRUST_J_PER_KG_K = 1000.0
CP_CORE_J_PER_KG_K = 840.0
ALPHA_SILICATE_PER_K = 2.0e-5

# ── Coefficients of the 2021 equations — printed in the 2021 body text ─────────────────────────
RA_DELTA_B_COEFF = 0.28                     # Ra_δb = 0.28 Ra_i^0.21 (Deschamps & Sotin 2000), 2021 PDF p12
RA_DELTA_B_EXP = 0.21
DELTA_T_B_COEFF = 1.43                      # ΔT′_b = 1.43 R T_m²/E*, layered case only, 2021 PDF p13

# ── Solidus depletion — Morschhauser, Grott & Breuer 2011, Icarus 212, 541 (`2011Icar..212..541M`) ──
# 2019 SI eq. (15) uses ΔT_sol and prints no value; Morschhauser eq. (18), PDF p13: "A total maximum
# solidus change of ∆Tsol = 150 K" (pre-registration v2-4 ④).
DELTA_T_SOL_K = 150.0

# ── Radiogenic heat — Ruedas 2017, G³ 18, 3530 (`2017GGG....18.3530R`), Table 2, PDF p6 (render) ──────
# ⚠ Outside the chain: none of the six chain papers prints or cites a heat table, so this is a source we
#   chose (pre-registration v2-5 ①) — the arXiv author's final manuscript, "final version, 6 September 2017".
# Present-day specific heat production of the element in its natural isotopic mix, W/kg, and half-lives, My.
H_U_W_PER_KG = 9.8314e-5
H_TH_W_PER_KG = 2.6368e-5
H_K_W_PER_KG = 3.4302e-9
HALF_LIFE_K40_MY = 1248.0
HALF_LIFE_TH232_MY = 14000.0
HALF_LIFE_U235_MY = 704.0
HALF_LIFE_U238_MY = 4468.0
X_ISO_K40 = 1.1668e-4

# ── Auxiliary reference — 2023 Extended Data Table 1, BML (main set), 2023 PDF p10 ─────────────
# (value, 1σ) over the best 1 000 models. Transcription blob 60e348cd. For reporting a distance only.
# ⚠ η₀'s σ is on the exponent — 10^(20.5 ± 0.3) — so it is stored as a base-10 logarithm.
AUX_E_STAR_J_PER_MOL = (120.0e3, 15.0e3)
AUX_V_STAR_M3_PER_MOL = (7.3e-6, 2.0e-6)
AUX_ETA0_LOG10_PA_S = (20.5, 0.3)
AUX_K_D_W_PER_M_K = (5.0, 1.0)
AUX_D_D_M = (165.0e3, 20.0e3)
AUX_D_CR_M = (67.0e3, 2.0e3)
