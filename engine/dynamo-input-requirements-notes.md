<!-- 다이나모 방법론 두 문서가 인쇄한 Needs 를 입력별로 대조한 병렬석 기록 — 5ad8f56c 인수인계 인벤토리의 doc-Needs 열 근거, 원문 무편집 -->
<!-- Landed 2026-09-04 from the parallel seat's scratch (DYNAMO-INPUT-REQUIREMENTS.md), body unedited. Line numbers refer to the engine worktree's docs/reference copies at 839b2c7c (they differ from main's). -->

# C. What the dynamo methodologies print as their required inputs
Parallel seat, 2026-09-04. Read-only; engine worktree HEAD 839b2c7c, `git status --porcelain`
empty. `rocky` = `docs/reference/rocky-planet-dynamo-methodology.md` (270 lines),
`scaling` = `docs/reference/planetary-dynamo-scaling.md` (190 lines).

## 1. `dynamo_rocky` — the doc's own **Needs** line, input by input

The doc's contract block prints Returns at `rocky:21-23` and **Needs at `rocky:24-25`**:

    :24  **Needs** — `mass_earth` [M_earth] · `radius_earth` [R_earth] · `conductor_phase` [—] · `stagnant_lid` [—] ·
    :25  `age_gyr` [Gyr] · `ice_mass_fraction` [—] · `body_class` [—] · `dynamo_regime` [—] · `locked` [—] · `rotation_period` [h]

Ten inputs. The grade the doc asks of each is not written per input; it is written once, at
`rocky:31-33`: "**Grade** — **judgment**, always: both gates are labels and ℳ_base, the regime
and the multipolar factor are declarations." The per-input expectation below is the doc's own
word for that input where it uses one.

| # | symbol (unit) | defined at | grade the doc expects | chain.yaml edge | edge status |
|---|---|---|---|---|---|
| 1 | `mass_earth` [M⊕] | `rocky:24`; "curated Phase 2 mass/radius" `rocky:196` | **measured** (Phase 2) | `:668` `mass_or_radius → dynamo_rocky, requires` | (none — live) |
| 2 | `radius_earth` [R⊕] | `rocky:24`; same | **measured** (Phase 2) | `:668` (same edge) | live |
| 3 | `conductor_phase` [—] | `rocky:24`; "`conductor_phase` from `core_state`" `rocky:28` | **a label, not a number** — `rocky:28` calls the alive gate "three labels"; `rocky:115` "the recipe uses `core_state`'s liquid-core verdict … as the gate" | `:678` `core_state → dynamo_rocky, requires, via: conductor_phase` | live |
| 4 | `stagnant_lid` [—] | `rocky:24`; "the declared `stagnant_lid`" `rocky:28` | **declared** | **no edge** | — |
| 5 | `age_gyr` [Gyr] | `rocky:25`; "the declared per-class death age" `rocky:28` | measured age + a **declared** death age | `:685` `body_age → dynamo_rocky, influences, sign: negative` | live, but `influences` not `requires` |
| 6 | `ice_mass_fraction` [—] | `rocky:25`; "the declared ice fraction" `rocky:27` | **declared** | `:684` `composition_intent → dynamo_rocky, influences, via: layer_fractions` | **status: gap** |
| 7 | `body_class` [—] | `rocky:25` | classification output | `:662` `body_class → dynamo_rocky, selects`; `:667` same via `sub_neptune` | `:662` live; `:667` **status: gap** |
| 8 | `dynamo_regime` [—] | `rocky:25`; "the regime gate, declared (`dynamo_regime`) or emitted both ways" `rocky:29-30` | **declared**, else both branches emitted | **no edge** | — |
| 9 | `locked` [—] | `rocky:25`; the C16 branch key, `rocky:120-125` | from `tidal_locking` | `:682` `tidal_locking → dynamo_rocky, selects, via: locked` | live edge, but the note says "공급자에 레시피가 없어 오늘은 모든 천체가 cannot-say (no tidal_locking)" |
| 10 | `rotation_period` [h] | `rocky:25`; enters "only through the regime gate" `rocky:86-90` | Phase 3 rotation state (`rocky:196`) | `:669` `orbit_elements → dynamo_rocky, requires, via: period` | live |

## 2. Edges the chain draws that the doc's Needs line does **not** carry

| chain edge | via | status | what the doc prints |
|---|---|---|---|
| `:677` `interior_layers → dynamo_rocky` | `core_radius` | (no status) | **`core_radius` is not in the Needs line at all.** The doc uses `r₀` only *inside RM22's own solver* (`rocky:39-40`, `rocky:46`) and states at `rocky:108-109` "NearStars does not re-run RM22's full internal-structure + thermal-evolution solver per body". The one place it claims consumption is the Related section, `rocky:258`: "supplies the core radius this recipe consumes". `engine/dynamo_rocky.py`'s `ladder(...)` signature (`:137-139`) takes `mass_earth, radius_earth, conductor_phase, stagnant_lid, age_gyr, ice_mass_fraction, …` and **no core radius**. |
| `:686` `heat_transport_mode → dynamo_rocky` | `cmb_heat_flux` | **gap** | The doc never prints `cmb_heat_flux` as a Need. It appears once as prose: `rocky:113-114` "stagnant-lid (Venus-analog, no plate tectonics → **low CMB heat flux**)". The chain note says "mode 는 라벨이고 열류는 수다. 소비처 둘(core_state · dynamo_rocky)이 원하는데 내는 노드가 없다". |
| `:687` `internal_heat_nontidal → dynamo_rocky` | `geotherm` | **gap** | Not in Needs. Ref points at `internal-heat-luminosity-methodology.md:202`, not at either dynamo doc. |
| `:683` `tidal_locking → dynamo_rocky` | `rossby` | **gap** | Not in Needs (`dynamo_regime` is the declared stand-in). Note: "Ro_ℓ 은 ν(RM22 어디에도 값 없음)·q_conv(정의 없음)·식-Table 8 불일치(4–5배) 셋이 막는다 — rotation_period 부족이 아니다." |
| `:725` `core_entropy_production → dynamo_rocky` | (φ) | **gap** | Not in Needs. Note: "C15 는 φ 를 내기까지. 문턱이 판정을 못 내므로(0.1–1000 MW/K) 사다리 교체는 별도 오너 결정 — 배선하지 않는다." |

So of the doc's ten Needs, **two have no chain edge at all** (`stagnant_lid`, `dynamo_regime`
— both things the doc calls *declared*, i.e. they are meant to be declarations, not supplied),
and of the five edges the chain draws beyond the Needs list, **four are `status: gap`** and the
fifth (`core_radius`) is the one whose requirement I cannot find printed.

## 3. `dynamo_giant` (`scaling`)

Contract at `scaling:17-21`:

    :18  **Needs** — `mass_mj` [M_J] · `radius_rj` [R_jup] · `age_gyr` [Gyr] · `body_class` [—] · brown-dwarf branch only: `luminosity_lsun` [L_sun] · `rotation_period_h` [h] · `radius_rj_min` [R_jup] · `radius_rj_max` [R_jup] · `isolated` [—]
    :21  **Grade** — calibrated.

**Nothing in this list comes from the interior-structure domain.** The giant law is
`B_dip^pol(M, age) = 9 G · (age/4.5 Gyr)^(−0.33) · (M/M_Jup)^0.93` (`scaling:83`), and
`scaling:78-81` says explicitly it does *not* re-derive internal cooling luminosities: "Rather
than re-derive internal cooling luminosities L(M, age) from scratch … we anchor on the
published, depth-corrected dipole values that Reiners & Christensen 2010 tabulate". The
brown-dwarf branch takes a **measured** bolometric luminosity (`scaling:27`: "from the
**measured** bolometric luminosity (an isolated brown dwarf's L_bol is its cooling luminosity —
no track derived)"). `scaling:35-37` records that this block is machine-checked against the
code by `engine/check_contracts.py`.

Chain edges into `dynamo_giant`: `:656` `mass_or_radius, requires`; `:657` `body_age, requires,
via t_body`; `:658` `star_physical, requires, via luminosity`; `:659` `internal_heat_nontidal,
requires, via l_int`; `:660` `body_class, selects`; `:661` `tidal_locking, selects`. Only
`:659` reaches an internal-heat node, and its ref is to
`internal-heat-luminosity-methodology.md:472`, not to `scaling`.

## 4. ⚠ The line references in chain.yaml do not land where they claim

Every ref below was printed verbatim. This is a printed-fact comparison, not a diagnosis.

| chain edge | its ref | what that line actually says |
|---|---|---|
| `:668` mass_or_radius | `rocky:22` | `` `b_eq` [uT] · `b_pol` [uT] · … `` — a **Returns** line (Needs is `:24-25`) |
| `:669` orbit_elements via period | `rocky:22` | same Returns line |
| `:677` interior_layers via core_radius | `rocky:23` | `` `ladder_regime` [—] · `dynamo_alive` [—] · `rossby_verdict` [—] `` — also **Returns** |
| `:678` core_state via conductor_phase | `rocky:25` | the second Needs line; `conductor_phase` is on `:24` |
| `:685` body_age / `:686` heat_transport_mode via cmb_heat_flux | `rocky:70` | "organized field); `Ro_ℓ > 0.12` → **multipolar** (the moment collapses to" — the Rossby gate, neither age nor CMB flux |
| `:725` core_entropy_production | `rocky:60` | "1. **Dynamo-alive gate** — the magnetic Reynolds number must exceed the critical" — no φ and no MW/K anywhere near it; the doc's only `MW/K` is `rocky:183` |
| `:684` composition_intent via layer_fractions | `rocky:109` | "solver per body. We instead anchor on the **moments RM22 tabulate** (Solar System" |
| `:682`/`:683` tidal_locking | `rocky:69` | "2. **Regime gate (local Rossby number)** — `Ro_ℓ < 0.12` → **dipolar** (strong," — **this one lands** |
| `:656` mass_or_radius → giant | `scaling:29` | "| stellar | M > 70 M_J | declines — not a dynamo of this kind | — |" |
| `:657` body_age → giant | `scaling:83` | the `B_dip^pol` formula — **lands** |
| `:658` star_physical via luminosity | `scaling:34` | **a blank line** |
| `:660` body_class → giant | `scaling:82` | **a blank line** |
| `:661` tidal_locking → giant | `scaling:33` | "reason attached, so a body that cannot be derived says why rather than being extrapolated." |
| `:662`/`:667` body_class → rocky | `scaling:97` | "| 1 M_J young end | 1.00 | 0.003 | 101 G | ~100 G | ✓ |" — a validation-table row |

Also, the brief's own pointers do not land either: `rocky:22-25` is the contract block (Returns
+ Needs), not "core_radius·conductor_phase"; `rocky:60` is the `Rm > 40` gate, not an entropy
threshold; `rocky:70` is the Rossby gate, not `cmb_heat_flux·age`; `rocky:109` is the "we do not
re-run RM22's solver" sentence, not `layer_fractions`. The **0.1–1000 MW/K** figure is not in
either methodology doc: it is at `engine/core-entropy-context-notes.md:107` — "the required
excess is 0.1–1 000 MW/K (no threshold decides)".

## 5. Places the docs say they cannot decide (their own sentences)

- **`Rm > 40` is quoted, never evaluated.** `rocky:63-64`: "`Rm = V L / λ`, `λ = 1/(μ₀σ)` …
  **quoted, not evaluated here**, because it needs V and σ that nothing we hold supplies."
  `rocky:114-116`: "⚠ **`Rm > 40` is quoted here, never evaluated** — this document carries no
  magnetic-Reynolds formula; the recipe uses `core_state`'s liquid-core verdict and a declared
  stagnant-lid judgement as the gate and says so on every result (owner condition, 2026-09-03)."
  And OC06's caveat, `rocky:65-66`: "*'beyond Rm_crit there is no simple relationship between
  Lo_dip and Rm'* — an on/off gate, never a strength predictor."
- **The Ro_ℓ path is refused by name (three blockers).** `rocky:122-125`: "locked → the Ro_ℓ
  path is **refused by name**: ν has no value anywhere in RM22, q_conv has no definition, and
  the printed Ro_ℓ equation misses RM22's own Table 8 by 4–5× on the slow rotators; key absent
  → `cannot-say (no tidal_locking)`, which is every roster body today because `tidal_locking`
  has no recipe."
- **Base-heated vs internally heated cannot be decided.** `rocky:82-85`: "⚠ **Base-heated
  dynamos only** … Whether a roster body's core is base-heated is **not something this recipe
  can decide**, and the label rides on every multipolar value and on the 0.12 threshold itself."
- **The C15 entropy threshold decides nothing.** `engine/core-entropy-context-notes.md:107`:
  "the required excess is 0.1–1 000 MW/K (no threshold decides); the band straddles zero (4 of 8
  corners positive)"; `rocky:183-184`: "the C15 entropy band moves (−69 → −68 → −82 MW/K) but
  still straddles zero, so the verdict stays `cannot-say`."
- **Regimes 2 and 3 have no printed anchor.** `rocky:119`: "⚠ **no per-class anchor table exists
  in this document** … regimes 2 and 3 carry no printed value and are emitted as grids without
  an elected number." Contract echo, `rocky:32-33`: "`dipole_moment` and `b_eq` are `null` for
  regimes 2 and 3 … and for cannot-say (undecided core, undeclared lid)."
- **The Ganymede regime-4 anchor is an open choice.** `rocky:144-147`: "⚠ **Ganymede's `2×10⁻³`
  carries no citation of its own here** … Which of the two the ladder's regime-4 anchor should
  carry is an open choice (C17, 2026-09-04), recorded here, not decided."
- **The whole scaling is an extrapolation, quantified.** `rocky:48-54`: "⚠ **Every value this
  scaling emits for an exoplanet is an extrapolation** … A planetary core sits near E ~ 10⁻¹² —
  **six decades below the lowest Ekman number the fit ever saw**".
- **Sub-Neptune has no dynamo path.** `chain.yaml:667` note: the on/off criterion is published
  (Tang+ 2025 §4.2, `Rm = μ₀σUD`, critical 50) but "자기모멘트·세기 스케일링은 발표돼 있지
  않다 (전문에 field 0회)"; `scaling:191-192` hands sub-Neptune off as "*below* the validated
  giant domain".
- **The multipolar grid is a width, not a value.** `rocky:80-81`: "The engine's grid is
  **OC06's own width, {0.05, 0.10}** … with RM22's Solar-System point 0.06 inside it".
