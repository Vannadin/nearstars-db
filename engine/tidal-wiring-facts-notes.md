<!-- 조석열 → 내부구조 열 예산 배선(C30)의 근거 사실 — 조석 문서 식·간선·판도라 입력·tidal_transport 상태를 인쇄된 문장으로 모은 병렬석 기록, 원문 무편집 -->
<!-- Landed 2026-09-04 from the parallel seat's scratch (TIDAL-WIRING-FACTS.md, 19:15 KST), body unedited. Line numbers refer to the engine worktree copies at 839b2c7c. Consumed by C30 (interior-core.md, tidal-heating-context-notes.md). -->

# Facts for the tidal-heat → interior-budget wiring brief
Parallel seat, 2026-09-04. Read-only; worktree HEAD 839b2c7c, `git status --porcelain` empty.
All paths under `/Users/vana/Desktop/NearStars-wt/engine-prototype/`. `tidal` =
`docs/reference/tidal-heating-methodology.md` (799 lines); `heat` =
`docs/reference/internal-heat-luminosity-methodology.md`. Printed facts only; no judgment.

## 1. The tidal-heating doc

### 1a. The law (`tidal:47-89`)

    :56  Ė  =  (21/2) · (k₂/Q) · (G M_p² R⁵ n e²) / a⁶
    :58  n = √(G(M_p + m)/a³) ≈ √(G M_p / a³)   (for m ≪ M_p)
    :61  Ė  ∝  (k₂/Q) · R⁵ · e² · M_p^(3/2) · a^(−15/2)

Symbol table verbatim (`tidal:65-74`), including the column the doc calls "Where it comes from":

| Symbol | Meaning | Where it comes from |
|---|---|---|
| `k₂` | degree-2 tidal Love number (potential response of the body) | **interior structure (§5)** |
| `Q` | tidal quality factor (1/Q ≈ phase lag = fraction of energy lost per cycle) | **rheology (§5)** |
| `G` | gravitational constant | – |
| `M_p` | mass of the **perturber** (the planet, for a moon; the star, for a planet) | DB |
| `R` | radius of the **heated** body | DB |
| `n` | mean motion = `2π/P_orb` = `√(G M_p / a³)` | orbit |
| `e` | orbital eccentricity | orbit (must be *maintained*, §4) |
| `a` | semi-major axis of the heated body's orbit about the perturber | orbit |

Units are not printed in that table. Reductions: `F = Ė/(4πR²)` (`tidal:81-82`); prefactor
`(21/2)` is "standard for the synchronous, zero-obliquity, small-`e` case" (`:76-77`); the form
is "a *first-order* tool: `k₂` and `Q` are treated as constant numbers" (`:87-89`).

### 1b. The four chain-referenced lines, verbatim

| chain edge | ref | the line it lands on |
|---|---|---|
| `chain.yaml:622` `tidal_heating → interior_layers, influences, sign: non-monotonic` | `tidal:199` | a **row of the k₂/Q class table**: `\| **Rocky / silicate** (Io-like, terrestrial) \| ~0.1–0.3 \| ~10–100 \| ~10⁻³–10⁻² \| strongly T-dependent; a partially molten interior raises k₂ and lowers Q (more dissipation) \|` — i.e. the ref documents the *reverse* direction (interior → k₂/Q), which is what "non-monotonic" is pointing at |
| `chain.yaml:631` `tidal_heating → heat_transport_mode, requires, via: surface_flux` | `tidal:273` | "A body's surface has exactly three ways to pass internal heat, and they differ by **four orders of magnitude in capacity**. Which one the body is in is set by the flux itself, so the mode is an output of §6.1, not a free choice." — **lands** |
| (brief's pointer) | `tidal:442` | "it. Size is therefore the strongest transport knob, and the transport test above turns into a hard radius ceiling." (the sentence begins `:440` "Because `Ė ∝ R⁵` while area ∝ `R²`, **surface flux scales as `R³` at fixed density**") |
| (brief's pointer) | `tidal:460` | "leaves the plains at their external-budget 223 K — cold enough that elemental sulfur is stable while SO₂ frost is not" (inside the Dante 521 km worked example, `:445` ff.) |

Two more refs the chain draws on the same doc, for completeness: `:632`
`internal_heat_nontidal → heat_transport_mode via mantle_radiogenic_power` → `tidal:266`;
`:633` `global_fluid_layer → heat_transport_mode, selects` → `tidal:332`; `:634`
`t_eq_stellar → heat_transport_mode, requires` → `tidal:341`.

### 1c. Every place the doc says how tidal heat enters mantle temperature / potential temperature / core cooling

**There is no such place.** The grep set (`potential temperature`, `mantle temperature`,
`core cool*`, `geotherm`, `heat budget`, `interior_layers`, `super-adiabat`) returns eight hits
in 799 lines, and each is one of the following:

| line | verbatim | what it is |
|---|---|---|
| `:67` | "`k₂` \| degree-2 tidal Love number (potential response of the body) \| interior structure (§5)" | the *reverse* arrow (interior → k₂), and "potential" here is the tidal potential, not potential temperature |
| `:265-267` | "tidal heating is one heat source among several (radiogenic, accretional, primordial). For an Earth-mass body radiogenic heating alone is ~0.08 W/m²; **tidal heating matters when it *exceeds* that**" | the only place the two budgets are compared, and it is a comparison, not a sum into a temperature |
| `:302-311` | "For lid thickness, **mantle temperature** and the residual conductive flux, Kankanamge & Moore 2019 (`2019JGRE..124..114K`) give a heat-pipe parameterization validated to <15 % against numerical simulation." | names the paper that would do it |
| `:313-321` | "**high flux gives a THICK lid, not a thin one** … a lid that by conduction passes only **3–7 % of Io's flux**" | lid, not mantle temperature |
| `:507` | inside §7's worked reasoning, "High internal heat, but a small rigid moon has a low k₂/Q, so the energy…" | a k₂/Q remark |
| `:568` | "the doc had named the paper that answers **\"what sets the mantle temperature\"** and had recorded, 254 lines later, that it had not been read. **The gap was between our own reference and the literature, not in either.**" | the doc's own record that this coupling was unread |
| `:583-598` | "**Correction (2026-09-02, Briefs 35+37)** … wired verbatim and solved to machine residual, the paper's §4 equations with its Table 5 put Io's lithosphere **8–42× off the paper's own 12.6 km** … the exact-root inversion … requires α ≈ 9×10⁻⁷ K⁻¹ — 1/34 of the 3×10⁻⁵ … The axis is wired in `engine/tidal_transport.py` with a permanent `validation: failed-io-reproduction` label" | the transport axis exists and its Io reproduction failed |
| `:600-606` | "**And the expensive part turns out not to be required.** The first reading was that this axis needs Ė(T) … **It does not, for what we want.** Ė(T) is needed to *predict* an equilibrium; **evaluating the conversion at a given heating rate does not need it** … **Our own Ė is likewise a computed input, not a prediction**, so declaring the transport mode and taking Ė as given closes the system." | the printed statement that the conversion is tractable |
| `:788` | "*additional* internal heat source layered on top of the irradiation that doc treats" | pointer to the tidally-locked-temperature doc |

⚠ **And the doc routes Pandora away from the lid branch by name** (`tidal:330-338`, the §6.3
scope box): "**Scope — lid-bearing bodies only.** … Where a **global fluid layer** exists, it
redistributes the interior flux and the whole argument below is void — the tidal term then
belongs in the body's global energy balance instead, via
[`moon-energy-budget-methodology.md`](moon-energy-budget-methodology.md). Which of the two
applies is a *selector*, not a number … **Dante (silicate, airless) takes this branch; Alpha
Centauri A b III (Pandora), half ocean under 1.1 bar, takes the other one.**"

### 1d. §6's four outputs, as the doc defines them

`chain.yaml:400-401` declares `outputs: [power, surface_flux, radius_ceiling, plains_temperature]`
with the note "radius_ceiling 은 수송 테스트가 돌려주는 하드 반지름 상한 (§6, Dante 521 km 가
그 산물), plains_temperature 는 외부 예산의 평원 온도 (§6.3·6.5, Dante 223 K)". In the doc:

| output | definition in the doc | line |
|---|---|---|
| `power` | `Ė` of §1's formula | `:56` |
| `surface_flux` | "Convert `Ė` to a **surface heat flux** `F = Ė / (4πR²)`"; the regime table is "guides, not sharp lines" — ≳1 W/m² vigorous silicate volcanism (Io ~2 W/m²) / 0.1–1 active resurfacing / 0.01–0.1 subsurface ocean / ≲10⁻³ geologically dead | `:243-251` |
| `radius_ceiling` | from §6.4's `required areal flux = F / (lake area fraction)` (`:378`) having to fall inside a **measured** lava-lake capacity (`:380`), combined with §6.5's published envelope "**1–3 orders of magnitude above Io = 25–2,500 W/m²**" (`:432-434`) and the `R³` flux scaling (`:440-443`): "the transport test above turns into a hard radius ceiling". Worked: Dante **521 km**, "sits inside the published super-Io envelope (2,231 < 2,500 W/m², which caps the radius at 541 km), gives an area-averaged 452 K" | `:376-380`, `:430-443`, `:457-459` |
| `plains_temperature` | "the terrain between volcanic centres is thermally **inert**: it sits at radiative equilibrium with its external budget (starlight, plus the parent's contribution for a moon)" — Io's plains "**110–130 K, purely insolation-driven**"; the design rule "Set the plains from the external budget and leave them there" | `:340-351`, `:367-372` |

⚠ §6.5 also prints "there is **no published W/m² boundary** between the modes, because the real
criterion is melt fraction and any flux threshold is a conversion, not a citation" (`:436-438`).

## 2. `internal_heat_nontidal` and the floor inversion

### 2a. The sentence `chain.yaml:653` cites (`heat:31-35`)

    :31  The **irradiation / equilibrium temperature** `T_eq` (what the star delivers) is the
    :32  [tidally-locked-temperature doc](tidally-locked-temperature-methodology.md). All of these
    :33  **combine** through the single relation in §1: `T_eff⁴ = T_eq⁴ + T_int⁴`, where `T_int`
    :34  here folds in only the non-tidal sources (add the tidal flux into `T_int` if it is
    :35  non-negligible, see that doc).

That is the whole of it. The doc's routing table two lines above sends tidal dissipation
elsewhere: `heat:29` "| **Tidal dissipation** | [`tidal-heating-methodology.md`](tidal-heating-methodology.md) |".

⚠ **`tidal_heating` is not in this recipe's Needs line.** `heat:46-47`: "**Needs** —
`mass_earth` [M_earth] · `core_mass_fraction` [—] · `ice_mass_fraction` [—] · `radius_earth`
[R_earth] · `body_class` [—] · `age_gyr` [Gyr] · `potential_temperature` [K]". So the
`requires` edge at `chain.yaml:653` rests on `:34`'s parenthetical instruction, not on a
declared input. Consistent with the code: `grep -n tidal engine/radiogenic.py` → **zero hits**.

Also, `heat:58-59`: "`l_int` for a rocky body **is** the radiogenic power, and `t_int = (F/σ)^¼`
is §1's relation applied to the **radiogenic flux alone** (Earth ≈ 29 K; §1's ≈ 35 K uses the
total 0.087 W/m², radiogenic + secular, so this `t_int` is a floor on that)."

### 2b. What `mantle_temperature_floor` inverts against — **radiogenic only**

`heat:65-76`, verbatim on the two relevant clauses:

    :65  `mantle_top_boundary_layer`, `implied_surface_heat_flux` and `implied_surface_heat_flow` are Nimmo+ 2004 eqs 34–36
    :66  evaluated at the **declared** `potential_temperature` (top boundary layer only; `k_t` derived as κ_t ρ_m C_pm, not
    :67  printed; calibrated at source on present-day Earth), and `heat_flow_consistency` compares that implied flow with
    :68  `radiogenic_power` — a consistency check on the declaration with secular cooling as the expected difference, never
    :69  the body's actual heat flux; `cannot-say` when no temperature is declared.
    :70  `mantle_temperature_floor_min/max` (Brief 57) is the same chain **inverted**: the potential temperature at which the
    :71  top boundary layer sheds exactly the radiogenic power — a **floor** on T_m (secular cooling adds to the flow), emitted
    :72  as a family, never a point: the union over ζ (Table 2's ± 0.5), the two concentration sets, and both denominators
    :73  (`mantle_w`, like-for-like with the top boundary layer, against `total_w`, what `heat_flow_consistency` uses …)

Code confirms both denominators are radiogenic: `engine/radiogenic.py:99` returns
`{"total_w": total, "mantle_w": MANTLE_SHARE * total, …}` from the four-isotope budget, and
`:162-163` passes exactly `mantle_w`/`total_w` of the two concentration sets into the band. The
relation is Nimmo+ 2004 eqs 34–36, the bisection bracket is 1000–2500 K (`heat:76`), and the
doc names the consumer as "art direction's tectonic-regime likelihood, which is **not**
classified here" (`heat:75-76`). **No tidal term enters anywhere in that inversion.**

For the adjacent edge: `chain.yaml:693` `internal_heat_nontidal → interior_layers, influences,
via mantle_radiogenic_power` carries the note "열 예산이 내부 단열선의 앵커(포텐셜 온도)를
정한다 … 공급자가 맨틀 방사성 출력(70 % 선언)을 낸다; **그것을 포텐셜 온도로 바꾸는 열 모형은
없어 소비처는 여전히 potential_temperature 를 선언한다.** gap 은 풀렸고 선언은 남았다."

## 3. Pandora's tidal inputs — with the body named on every row

⚠ **Pandora has no `bulk.tidal_heating` axis.** Its axes are `identity` (`:2076`), `bulk`
(`:2106`), `atmosphere` (`:2172`), `surface` (`:2241`), `magnetism.magnetic_field` (`:2282`),
`magnetism.magnetosphere` (`:2324`), `magnetism.radiation_belts` (`:2339`), `appearance`
(`:2406`), `environment.radiation` (`:2483`), `gameplay` (`:2498`). Dante (`:1524`) and Hades
(`:1871`) each have one; Pandora's tidal numbers are spread across `bulk`, `atmosphere` and
`magnetism` instead. All line numbers below are `phase4/alpha_centauri.yaml`.

| body | where | value as printed |
|---|---|---|
| **Dante** (A b I) | `:1553` `bulk.tidal_heating` | `tidal_heating` = "**~1200× Io** (simulated e_rms 0.0186, k₂/Q ~0.0155)" |
| **Dante** | `:1554` same axis | `tidal_surface_flux` = "**~11,500 W/m²** (360 K plains; the exposed melt at 1350 K covers ~5.7% of the area)" |
| **Dante** | `:1482` `bulk` | `internal_heat` = "tidal (see bulk.tidal_heating row, ~1200× Io)" (`:1486` records the correction ~820× → ~1200×) |
| **Hades** (A b II) | `:1888` `bulk.tidal_heating` | `tidal_heating` = "**~15× Io** (207 W/m² surface flux; the bottom of the rocky band, k₂/Q = 1e-3, e_rms 0.0385)" |
| **Pandora** (A b III) | `:2139` `bulk` | `internal_heat` = "**Radiogenic plus weak tidal heating (forced e ~0.005)**, enough to drive volcanism, continental drift and a dynamo" |
| **Pandora** | `:2195` `atmosphere` | `temperature` = 290 K, note: "Four-term Teq 220.6 K plus **45 W/m² of tidal heating** gives Teq 237 K, and +54 K of CO₂ greenhouse brings it to …" |
| **Pandora** | `:2211-2215` `atmosphere` evidence | "plus solid-body tidal heating **45 W/m²**, giving Teq 237K; +54K greenhouse = 291K. So the lift IS partly tidal. **The tidal term needs k₂/Q ≈ 0.0016 at the simulated e ≈ 0.005, which is fitted rather than predicted** … Io-like k₂/Q = 0.015 would make Pandora a **369K steam world**. Ocean tidal dissipation is a separate, [deeper term]" — and `:2232` (ko) prints the runaway ceiling as "**~101 W/m² 폭주 천장**" |
| **Pandora** | `:2200` `atmosphere` refs | `["…/greenhouse-warming-methodology.md", "…/moon-energy-budget-methodology.md", "…/tidal-heating-methodology.md", …]` |
| **Pandora** | `:2176-2177` (ko evidence) | "refs에서 tidally-locked-temperature 제거(위성은 4항 예산이 Layer 1을 대체), **moon-energy-budget·tidal-heating·cassini-state 추가**" |
| **Pandora** | `:2259` `surface` | `tectonics` = "Active volcanic belts and fast continental drift (**tidal plus radiogenic**)" |
| **Pandora** | `:2296` `magnetism.magnetic_field` | `magnetic_field` = "75 µT (~1.8× Earth; the upper bound of the rocky-dynamo M+ ladder, **a tidally driven iron-core dynamo**, dipolar at a 32 h rotation)" |
| **Pandora** | `:2304`, `:2307` same axis | "**tidal heat (forced e ~0.005)**+radiogenic [convect vigorously]"; "Shares the same heat source (tidal heat) as the volcanism·fast continental drift (causally linked)" |
| **Pandora** | `:2114`, `:2124` (narrative) | 32 h "chosen over the film's 27 because the wider orbit keeps the ocean's **tidal budget** safely below [runaway]" |
| **Pandora** | `:2141` `bulk` | `geopotential_c22` = 6.2e-4, note "**Tidal triaxiality**; flattening 0.83% (a-c ~47 km)" |

⚠ **No `tidal_surface_flux` row exists for Pandora** — the 45 W/m² lives in an `atmosphere`
temperature note, not in a bulk tidal row. ⚠ **"~78× Io" does not appear anywhere in
`phase4/alpha_centauri.yaml`** (grep for "78× Io" / "78x Io" / "78배" → zero hits). For scale,
the doc's Io reference flux is 2.5 W/m² (`tidal:350-351`, "On a body radiating 2.5 W/m² on
average") or "~2 W/m²" in the regime table (`tidal:248`); 45 W/m² against those is 18× / 22×.

### Stability-sim (`phase3/stability-sim/`)

| body | quantity | value | file:line |
|---|---|---|---|
| Pandora | `e_min` | 0.00016422372329501632 | `results/_final32b/alpha_centauri_summary.json`, key `/per_body/Pandora/e_min` |
| Pandora | `e_max` | 0.007215479742978246 | same, `/per_body/Pandora/e_max`; `/judgment/per_body/Pandora/e_max` repeats it |
| Pandora | `a_min` / `a_max` (AU) | 0.001686783851726199 / 0.001687784632918313 | same, `/per_body/Pandora/a_*` |
| Pandora | Hill fraction max, bound | 0.0221067188588289, `True` | same, `/hill_track/Pandora/*` |
| Pandora | status / `ecc_class` | `stable` / `calm` | same, `/judgment/per_body/Pandora/*` |
| Pandora | `semi_major_axis_km`, `eccentricity` (input) | 252 393 km, 0.0 | `hypotheticals/alpha_centauri.json:33`, `:34` |
| Pandora | tidal-lock day → a | "only Pandora is Kepler-derivable from its tidal-lock 27 h day → a = 225,000 km" | `context-notes.md:191` |
| Dante | `e_rms` band | 0.017–0.022 | `DANTE_HEAT_TRANSPORT_EVIDENCE.md:154` |
| Hades | `e_rms` band | 0.033–0.046 | same line |
| — | which board rows take e_rms | "`bulk.tidal_heating` (both take e_rms), Hades `identity`/`bulk` (the elements themselves)" | `context-notes.md:665` |
| — | Dante e_rms spread | "Dante's e_rms varies by 2× across [realizations]" | `context-notes.md:654` |

⚠ **No `k₂/Q` and no output in watts is produced by the stability sim** — it emits orbital
elements (e, a, Hill fraction) and the boards convert. The k₂/Q values are board declarations:
Dante 0.0155 (`:1553`), Hades 1e-3 (`:1888`), Pandora 0.0016 fitted (`:2212`).

### Orbital inputs (from my `TIDAL-LOCKING-INVENTORY.md`, repeated here with bodies named)

| body | a | e | orbital period | parent mass |
|---|---|---|---|---|
| Pandora (A b III) | 252 393 km — `hypotheticals/alpha_centauri.json:33` | 0.0 (sim input) — `:34`; sim **output** e_max 0.007215; board **forced e ~0.005** — `phase4:2139` | 32 h — `phase4:2137` ("Tidally locked") | 120 M⊕ (Polyphemus) — `phase4:354` |
| Dante (A b I) | 110 000 km — `…json:9` | 0.01 (input) — `:10`; e_rms 0.0186 on the board — `phase4:1553` | 9.2 h — `phase4:1478` | 120 M⊕ |
| Hades (A b II) | 148 000 km — `…json:21` | 0.05 (input) — `:22`; e_rms 0.0385 on the board — `phase4:1888` | 14.4 h — `phase4:1836` | 120 M⊕ |

Pandora's own `m` / `R` (the heated body's terms in `Ė`): 3.85e24 kg / 5724 km
(`phase4:2133`, `:2132`); as engine units 0.6447 M⊕ / 0.8984 R⊕
(`engine/bodies/pandora.yaml:7`, `:11`).

## 4. `engine/tidal_transport.py` — what it computes, and who calls it

**What it computes** (module docstring, `:1-9`): "조석 가열률을 내부 온도·리소스피어 두께로
바꾸는 수송 축 — Kankanamge & Moore 2019 heat-pipe 계" / "Ė → (internal temperature,
lithosphere thickness) under a DECLARED transport mode … 수송 모드는 **선언**이고 도출이
아니다". Functions: `residuals` (`:78`), `_newton` (`:119`), `all_roots` (`:163`),
`stability_label` (`:195`), `transport_result` (`:214`), **`derive_potential_temperature`
(`:276`)**, `roster_inputs` (`:355`), `roster_measurement` (`:416`).

⚠ **`derive_potential_temperature` is exactly the function this wiring would consume, and it
already exists**, docstring (`:277-282`): "조석 가열 천체의 potential_temperature 도출 —
**선언이 도출값이 되는 자리.** 지금 솔버의 potential_temperature는 세 번째 선언이다
(interior.py). 이 함수가 그 값을 Ė에서 도출하되, 출력은 **어느 쪽인지** 반드시 말한다 … 검증
실패 라벨이 그대로 실려 간다." Signature: `derive_potential_temperature(surface_flux_wm2,
radius_m, **kw)`; returns `potential_temperature`, `provenance` ("derived-from-Edot — 선언
아님; Kankanamge & Moore 2019 eqs. (36)+(38), 선언된 heat-pipe 모드 아래"), `validation`,
`stability`, and returns `potential_temperature=None` with `provenance="derived-from-Edot (근
없음)"` when there is no root.

**Validation label** (module docstring `:12-21`): "**검증 상태: 실패 (사전등록 분기 ③+④,
tidal-interior-context-notes.md §4).** … 논문 자신의 이오 결과(1471 K, 12.6 km)는 자연 독법의
상수 어디에서도 재현되지 않고 … α = 8.71e-7 1/K (암석의 ~1/34), ΔT_rh = 354 K … 그러므로
여기서 나오는 수는 **unvalidated 라벨을 달고 측정으로만** 쓰인다. **채택 금지.**"

**Registry**: `engine/registry.py:56-72`'s `load_all()` imports eleven modules — `dynamo`,
`mass_radius`, `interior`, `core_state`, `cmb_flux`, `core_energy`, `core_entropy`,
`core_history`, `body_class`, `radiogenic`, `dynamo_rocky`. **`tidal_transport` is not among
them**, and `registry.registered()` after `load_all()` returns exactly eleven names:
`body_class`, `cmb_heat_flux`, `core_energy_balance`, `core_entropy_production`, `core_state`,
`core_thermal_history`, `dynamo_giant`, `dynamo_rocky`, `interior_layers`,
`internal_heat_nontidal`, `mass_radius_relation`. There is no `@recipe(...)` decorator anywhere
in `tidal_transport.py`.

**Callers**: `grep -rn tidal_transport engine/*.py scripts/**/*.py` finds only
`engine/test_tidal_transport.py` (`:4`, `:19` `import tidal_transport as tt`, `:141`, `:145`).
**No production caller.**

**`engine/bodies/pandora.yaml`** — its full `inputs` block (`:6-12`) is `mass_earth: 0.6447`,
`age_gyr: 5.3`, `body_class: rocky`, `composition_intent: earth_like`, `radius_earth: 0.8984`,
`core_mass_fraction: 0.325`. ⚠ **No tidal input of any kind**, and **no
`potential_temperature`** either — which is why the C29 run reported
`heat_flow_consistency=cannot-say (no potential temperature declared)`. Earth's file, by
contrast, declares `potential_temperature: 1600.0` (`engine/bodies/earth.yaml:17`).
