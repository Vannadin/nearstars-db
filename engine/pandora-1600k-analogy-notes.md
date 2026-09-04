<!-- 판도라 1600 K 지구 유비의 근거 수준 — Unterborn+ 2019 원문·질량/나이 스케일링 부재·C20 자기도출 −75 K 를 인쇄된 사실로 모은 병렬석 기록, 원문 무편집 -->
<!-- Landed 2026-09-04 from the parallel seat's scratch (PANDORA-1600K-ANALOGY.md, 19:08 KST), body unedited. Line numbers refer to the engine worktree's docs/ and engine/ copies at 839b2c7c. Consumed by interior-core.md C29. -->

# C29 — the grounding level of the 1600 K Earth analogy, as printed facts
Parallel seat, 2026-09-04. Read-only; worktree HEAD 839b2c7c, `git status --porcelain` empty
before and after every run. All doc line numbers are the **worktree** copies under
`/Users/vana/Desktop/NearStars-wt/engine-prototype/`. The declaration stands; nothing below
is a recommendation.

## 1. Where Earth's 1600 K comes from in our documents

| where | what it says | verbatim |
|---|---|---|
| `engine/bodies/earth.yaml:15-17` | the declaration and its attribution | `# 맨틀 포텐셜 온도. **선언** 이다 — Unterborn+ 2019 §2 의 지구형 값이고, / # 암석-금속 상들의 적합 기준이 이 단열선이라 여기서 열압력이 정확히 0 이다.` then `potential_temperature: 1600.0` |
| `docs/reference/interior-structure-methodology.md:393-396` | why the whole rock/metal column is referenced to it | "The rock-and-metal column is therefore referenced to **Earth's adiabat**, anchored at the 1600 K mantle potential temperature of Unterborn+ 2019 §2. Declaring 1600 K makes ΔT identically zero and the answer bit-for-bit the isothermal one" |
| same, `:399-404` | that it is a declaration and not a surface temperature | "**The anchor is a declaration, and it is not the surface temperature.** … the surface sits below it across a conductive lid worth roughly 1300 K on Earth … `potential_temperature` enters as a declaration beside `ice_allowed` and `tidal_heating`, with the coupling recorded in the chain as an `influences` edge carrying `status: gap`." |
| same, `:70` | ranked among the declarations | "`potential_temperature` is the third declaration" |
| same, `:169`, `:171`, `:172`, `:173` | four EOS rows whose fit reference is this adiabat | each prints "Earth adiabat, 1600 K" in the reference column |
| same, `:1261-1263` | what changes if the declaration moves off 1600 | "`potential_temperature` unset, or set to 1600 K → unset … returns the isothermal answer bit for bit; 1600 K integrates the adiabat … ΔT identically zero"; "**temperature declared away from the reference** … The answer now leans on a declaration this recipe cannot derive" |
| same, `:1135-1139` | the CMB cross-check built on it | "Unterborn+ 2019 … fit their models' CMB temperature to a cubic in radius at 1600 K potential temperature (eq. 7, valid 0.75 to 1.5 R⊕) with a shift for other anchors (eq. 8); at 1 R⊕ it returns 2635 K" |
| `engine/core-thermal-history-context-notes.md:198` | C20 uses it only as a report line | "*report line, not a gate*: present-day T_m against the declared 1 600 K potential temperature." |

**Paper**: the only citation is Unterborn+ 2019, and the docs print it as **arXiv:1905.06530**
(`interior-structure-methodology.md:1136`). `check_paper_held.py 1905.06530` → **HELD (as
bibcode)**; `ls` cross-check confirms `1905.06530.html` + `1905.06530.md` in the cache. ⚠ I do
not report a journal bibcode for it: the docs do not print one at the citation, and guessing one
is the banned move.

**What the paper actually says at the cited place** (from the cached text, `1905.06530.md`):

| line | verbatim |
|---|---|
| `:50` (their §2, model setup) | "we adopt `T(R) = T_Pot`, where `T_Pot` is the potential temperature: the temperature of the mantle if it were adiabatically decompressed. In reality, a colder, conductive layer is likely present at the surface of planets … Effects of temperature on the calculated radius are minor (Dorn et al. 2015; Unterborn et al. 2016), and thus **we first run calculations assuming a single mantle potential temperature, T(M) = 1600 K, relaxing this constraint in section 3.2**" |
| `:94` (their §3.1) | "Assuming an **Earth-like** mantle potential temperature of 1600 K (Figure 6), we find CMB temperature increases with planetary radius reaching a maximum of T ~ 4100 K at 1.5 R⊕ planets" |
| `:98` (their §3.2) | "**Relaxing the constraint** of an Earth-like mantle potential temperature, we further consider planets with potential temperatures of **1400 K and 1900 K**. As compositions of 0.5 ≤ Mg/Si ≤ 1.2 … will be liquid at the surface at 1900 K potential temperature. Thus, considering hotter adiabatic temperature profiles would not be representative of a solid planet, but one marked by surface magma oceans." |
| `:100` | "Tidal heating and thermal boundary layers within the mantle can all lead to significantly super-adiabatic temperature profiles." |

So the source calls 1600 K **"Earth-like"** and a **single-value simplification it then relaxes**;
the span it explores is **1400–1900 K**, with 1900 K flagged as a surface-magma-ocean case.
Nothing at the cited place ties 1600 K to a mass or an age.

## 2. Is a mass/age scaling of mantle potential temperature printed anywhere we hold?

| candidate | what is printed | verdict |
|---|---|---|
| Unterborn+ 2019 eq. 7 / eq. 8 | eq. 7 = T_CMB as a cubic in **radius at fixed T_Pot = 1600 K**; eq. 8 = a **shift for a different declared T_Pot** (`interior-structure-methodology.md:1137`, `:1639`) | **T_Pot is the input, not the output.** No scaling of T_Pot itself |
| Noack & Lasbleis 2020 `2020A&A...638A.129N` (**HELD**, `2020A&A...638A.129N.pdf`) eq. (22) | `T_CMB = T_um · exp(dT · g_m,av α_m,av / C_p,m,av · (R_p − R_c − D_l))` with "**`T_um = 2000 K` at the base of a 250 km lithosphere and an empirical `dT ≈ 0.5`**", parameterised over **0.8–2 M⊕** (`interior-structure-methodology.md:1156-1161`) | `T_um` is held **fixed at 2000 K across the whole mass range** — again an input, and a different quantity from T_Pot. No mass scaling |
| same, their eqs. (20) and (21) | "**not** used: those are initial, post-magma-ocean temperatures built to exceed the literature by thousands of kelvin, a claim about early planets and not a present-day adiabat" (`:1162-1164`) | excluded by our own docs |
| Nimmo+ 2004 `2004GeoJI.156..363N` (**HELD**, `2004GeoJI.156..363N.pdf` + PROVENANCE) | a **thermal-evolution integration** of (T_c, T_m), eqs 30/32; its own present-day Earth value is **T_m = 1 613 K** (`engine/core-thermal-history-context-notes.md:336`, reproducing his Table 4: η_t 6.7e20, Q_M 41.8 TW). Initial conditions are declarations: "T_c(0) and T_m(0) are **declarations**" (`:190`) | an **Earth-calibrated integration**, not a mass/age closed form. Gives a second published Earth number (1613 K), no scaling law |
| parameterized-convection literature (Stevenson-1983 class) | `grep` over `docs/reference/` and `engine/*.md`: **no hit** for "Stevenson 1983", "parameterized/parameterised convection", or `1983Icar` in this context | **none held / none cited** |
| Mars / Venus potential-temperature estimates | `grep` over `docs/reference/*.md` and `engine/*.md`: **no hit**. (The only nearby number, `engine/rocky-dynamo-context-notes.md:35` "T_eq 255–1350 K", is an *equilibrium* surface temperature axis, not a potential temperature) | **none** |

**Answer to (2): no mass/age scaling of mantle potential temperature is printed in anything we
hold.** The only printed *range* for the quantity is Unterborn's own 1400 / 1600 / 1900 K
exploration, and the only second published Earth point is Nimmo's 1613 K.

### The one thing in the engine that does vary with mass and age
`internal-heat-luminosity-methodology.md:70-76` describes `mantle_temperature_floor_min/max`
(Brief 57) — "the same chain **inverted**: the potential temperature at which the top boundary
layer sheds exactly the radiogenic power — a **floor** on T_m (secular cooling adds to the
flow), emitted as a family, never a point". Run in the scratch shell against the worktree
(`PYTHONDONTWRITEBYTECODE=1 python3 run.py bodies/<b>.yaml`):

| body | inputs used | `mantle_temperature_floor_min` | `_max` | verdict string |
|---|---|---|---|---|
| Earth | 1.0 M⊕, 1.0 R⊕, 4.54 Gyr | **1060 K** | **1492 K** | `band (radiogenic-only floor on the mantl…)` |
| Pandora | 0.6447 M⊕, 0.8984 R⊕, 5.3 Gyr | **1017 K** | **1468 K** | same |

Pandora's band sits 43 K lower at the bottom and 24 K lower at the top than Earth's; both bands'
maxima are below 1600 K, which is what "floor, secular cooling adds to it" means by
construction. Widths emitted by name for Pandora: `zeta` 282.7 K, `set` 222.7 K,
`denominator` 118.4 K, `surface` 45.0 K. ⚠ This is a **floor family, not an estimate of T_Pot**,
and the doc names its consumer as "art direction's tectonic-regime likelihood, which is **not**
classified here".

## 3. C20's self-derived present-day T_m on Earth, against the declared 1600 K

Run: `PYTHONDONTWRITEBYTECODE=1 python3 run.py bodies/earth.yaml` in the worktree (read-only;
`git status --porcelain` empty afterwards). Node `core_thermal_history`:

    core_cmb_temperature_present=4028 K, mantle_potential_temperature_present=1525 K,
    dtc_dt_present_k_per_gyr=-35.59 K/Gyr, q_cmb_present=5.069e+12 W, q_mantle_present=2.828e+13 W,
    inner_core_radius_present_km=0 km, inner_core_case=never,
    entropy_history_verdict=cannot-say (the four-corner band straddl…), history_steps=1135

| quantity | value |
|---|---|
| declared `potential_temperature` (`earth.yaml:17`) | **1600 K** |
| C20 `mantle_potential_temperature_present` | **1525 K** |
| difference | **−75 K = −4.69 %** |
| for comparison, Nimmo's own present-day T_m | **1613 K** (`core-thermal-history-context-notes.md:336`) → C20 is **−88 K** against that |

This reproduces the recorded report line exactly — `core-thermal-history-context-notes.md:264`:
"Report lines, not gates: present T_m **1 525 K** against the declared 1 600 K (**−75 K**);
present surface heat flow **Q_M 28.3 TW** against Nimmo's / the observed **42 TW**". The same
note at `:337-338` places the flux gap on the temperature rather than the viscosity law: "Put
Nimmo's own present T_m = 1 613 K in: η_t 6.70e20 Pa·s, Q_M 41.8 TW — his Table 4 exactly. At our
endpoint 1 525 K the same law gives 28.5. **The shortfall is the mantle temperature, not the
viscosity law**." And `:198` records that this comparison is deliberately not a gate: "*report
line, not a gate*".

⚠ My run prints `q_mantle_present=2.828e+13 W` = **28.28 TW**, against the note's "28.3 TW" —
same number to the note's printed digits.
