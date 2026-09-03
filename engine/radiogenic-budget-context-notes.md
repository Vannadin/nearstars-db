<!-- Brief 44 — 방사성 가열의 현재값 절반: 네 핵종 상수의 출처와 폐합, internal_heat_nontidal 암석 갈래의 사전등록·설계·결과 -->
# Radiogenic heating, the present-day half — Brief 44 (context notes)

2026-09-03. **§1–§3 are the pre-registration and were committed before any code ran.** §4 is
filled after. Verifiers: (병) parallel seat (read the paper), (직) directing seat (verified the
source lines and the closure), (여기) work seat (re-read the source, recomputed the closure).
Survey ㉓'s record is `engine/radiogenic-context-notes.md`; this note is what the paper changed.

## 1. ⚠ The table is not in the paper — cite it three ways or not at all

The isotope table exists **only in the LaTeX source, after `\end{document}`**, and the authors
marked it unfinished. Verified (직, 여기): `docs/phase3/_papers/2020ApJ...903L..37N.src/main.tex`
line 489 `\end{document}`; line 492 `\begin{table}` — dead LaTeX, never compiled; the caption ends
`\textcolor{red}{check}`; the next line reads *"Need supplementary table of parameter values
used…"*. Every one of its numbers (`2.92`, `2.64`, `9.46`, `5.69`, `99.275`, `21.4`, `25.5`,
"Heating rate") returns **0 hits** in the PDF text (여기). **There is no "Nimmo & Primack 2020
Table 1" and it must never be cited as one.**

So every use says all three things: **the four constants are standard nuclear data, not this
paper's findings** (that is *why* the closure works — any handbook prints the same values);
**this paper's unpublished draft table is where we read them**; **the closure below is the check
that we read them right.**

Verbatim from `main.tex:494–499` (여기):

| isotope | t½ (Gyr) | isotopic wt % | heating rate (W/kg of isotope) |
|---|---|---|---|
| ⁴⁰K | 1.25 | 0.0117 | 2.92×10⁻⁵ |
| ²³²Th | 14.0 | 100. | 2.64×10⁻⁵ |
| ²³⁸U | 4.47 | 99.275 | 9.46×10⁻⁵ |
| ²³⁵U | 0.704 | 0.72 | 5.69×10⁻⁴ |

Elemental concentrations in the same table: **Earth (1)** K 260 ppm / Th 85 ppb / U 22 ppb
(Palme & O'Neill 2014, chondritic); **Earth (2)** 130 / 43 / 11 (O'Neill & Palme 2008,
non-chondritic); geoneutrino total **25.5–51.8 TW** (Agostini 2019 — the table prints the range,
not a central value). The **appendix** (`main.tex:420`) uses **K 260 ppm, U 23 ppb, Th 85 ppb →
"22 TW of heat production at the present day"**.

**The closure (여기, with BSE mass 4.0×10²⁴ kg — a declared standard value, not from this paper):**
Earth (1) → **21.15 TW** vs the table's 21.4 (1.1 %); Earth (2) → **10.63 TW** vs 10.8 (1.6 %);
appendix set → **21.55 TW** vs "22 TW" (2.1 %). Directing and parallel seats got the same three.

**⚠ Caption defect, with its resolution.** The caption says *"Heating rate refers to the initial
composition of Earth"*. Read that way — decay the set 4.5 Gyr forward — Earth (1) gives **11.59 TW**
against the appendix's present-day 22, off by 1.90×. **The concentrations are present-day**,
settled by the paper's own appendix; that is very likely what the authors' red `check` refers to.
Recorded here (ours to read correctly), not in `paper-defects.md`: the table was never published.

**The 3.5× sentence** (`main.tex:212`): *"Four billion years ago, heat production was 3.5 times as
large"*. Our four exponentials on the appendix set give **H(−4 Gyr)/H(now) = 3.67** (여기); the
difference is the paper's rounding and set. **Pinned as a test, in the past direction** — the
parallel seat first computed it *forward* and got 1.67, a believable number one sign away.
**²³⁵U carries it**: 0.38 TW today, 51× over 4 Gyr; drop it and the factor is 2.8; Th + ²³⁸U alone
give 1.5. A reader who prunes ²³⁵U from a present-day budget silently breaks the history.

## 2. Design, argued

**Where it lives.** `internal_heat_nontidal` is declared in `chain.yaml` (recipe
`internal-heat-luminosity-methodology`, outputs `[l_int, t_int, geotherm]`) and has **no `@recipe`**.
Brief 44 registers it — **for rocky bodies only**. The giant branch is the cooling luminosity
L(M, age), which `dynamo.py` already refuses to supply rather than ground an unverified cooling
track; the registration returns out-of-domain there, naming that refusal. `l_int` for a rocky body
**is** the radiogenic power, and `t_int = (F/σ)^¼` is the methodology's own §1 (≈ 35 K for Earth) —
so the existing contract names are honest for rocky bodies without inventing a giant model.

**The `geotherm` name is retired, as Brief 40 §4 required before wiring.** `chain.yaml:99–102`
already said one word covered two quantities (a heat *budget* here, a T(P) *profile* in
`interior_layers`). The output becomes **`mantle_radiogenic_power`** [W] (the 70 % share that heats
the convecting mantle) beside `radiogenic_power` [W] (total), `crust_radiogenic_power` [W],
`radiogenic_heat_w_m2` [W/m²] (total over the surface — the Phase-3 field of the same name),
`radiogenic_power_history_4gyr` [—] (H(−4 Gyr)/H(now)), and `l_int` / `t_int`.

**The two gap edges this closes.** `internal_heat_nontidal → interior_layers` (the
potential-temperature anchor, `chain.yaml:410`) and `→ core_state` (the CMB flux, `:422`) both
carried *"저쪽이 프로파일도 열류도 내지 않으므로 지금은 선언으로 받는다"*. The supplier now emits the
budget; **the consumers keep declaring** `potential_temperature` and `core_cmb_temperature`, because
turning a budget into a temperature or a boundary-layer flux is the thermal model this paper defers
to Nimmo+ 2004 (`2004GeoJI.156..363N`, **not cached**). The edges lose `status: gap` and gain
`via: mantle_radiogenic_power`; the notes say what is supplied and what is still declared.

**H(t) is built and NOT wired to the third consumer.** `→ dynamo_rocky via geotherm` (`:404`)
asks whether the core is *still* convecting, which needs thermal evolution — Nimmo+ 2004. The decay
physics is ours; the thermal evolution is not. That edge becomes `status: gap` with the reason.
`→ heat_transport_mode via geotherm` (`:354`) wants the internal budget and takes
`mantle_radiogenic_power`.

**Declarations (the family, C11):**
- **Concentration set** — Earth (1) chondritic is the default; Earth (2) is emitted beside it as
  `radiogenic_power_low`. Both labelled; neither elected as "the" value.
- **Crust share 0.30 / mantle share 0.70** — the appendix's sentence: *"the convecting mantle is
  responsible for 70 % of the total radiogenic heat at all times; the remainder is assumed to
  reside in the crust"*. One number, Earth's, declared.
- **Silicate mass** — **derived, not declared**: mass × (1 − core_mass_fraction) from the body's
  own inputs (Earth: 5.972×10²⁴ × 0.675 = 4.03×10²⁴ kg, 0.8 % from the standard 4.0×10²⁴). The
  test's closure uses 4.0×10²⁴ to match the paper's own arithmetic; the recipe uses the body's.
- Bodies without a silicate composition (giants, or `core_mass_fraction` undeclared) → named
  refusal, not a default (④).

## 3. Pre-registered outcomes

① both gap edges close and the roster's rocky bodies get a budget; ② the 70 % split is the only
declaration needed; ③ more declarations surface (a crust fraction per class, a BSE mass per body)
→ listed as a family with a grid, never one elected tuple; ④ some roster body has no composition
to hang concentrations on → named refusal, not a default; ⑤ the closure does not reproduce on the
implementation → **that is the finding; report it, do not adjust the constants.**

**Expectation (여기, before code)**: ① fires for Earth and Pandora; ③ fires in part — the
concentration set is a second declaration beside the 70 % (§2), but the BSE mass is derived from
`core_mass_fraction` rather than declared, so ③'s "per-body BSE mass" half does *not* fire;
④ fires for Alpha Centauri A b (giant). ⑤ is not expected: the closure already reproduces in
scratch to 1.1–2.1 %. (The directing seat's expectation was ③ with both halves; it noted its prior
has been wrong twice tonight in the same direction.)

## 4. Result — 2026-09-03, code `c7ab5ed5`

**Branches fired: ① for Earth and Pandora; ③ in part; ④ for the giant. ⑤ did not fire.**

- **①** Both gap edges (`→ interior_layers`, `→ core_state`) now carry `via: mantle_radiogenic_power`
  with no `status: gap`; the notes say the budget is supplied and the temperatures are still declared.
  Earth: **21.32 TW** total from its own silicate mass (5.972×10²⁴ × 0.675 = 4.03×10²⁴ kg), mantle
  14.92 TW, crust 6.40 TW, surface-equivalent flux 0.0416 W/m², `radiogenic_power_low` 10.71 TW,
  history factor 3.67. Pandora: 13.74 TW, 27.9 K.
- **③, in part, as expected**: two declarations (concentration set, 70 % share), not one; the
  silicate mass is **derived** from `core_mass_fraction`, so the "per-body BSE mass" half of ③ did not
  fire. The directing seat's prior (both halves) was wrong in the direction it had flagged.
- **④** Alpha Centauri A b refuses by name: the giant's internal heat is the cooling luminosity this
  recipe does not supply. A rocky body without `core_mass_fraction` also refuses (pinned).
- **⑤ did not fire** — closure 21.15 / 10.63 / 21.55 TW against 21.4 / 10.8 / 22, all within 2.1 %;
  the constants were read correctly and none was adjusted.

**Two expectations of mine that were wrong, corrected in the test rather than the code:**
- *t_int.* I expected ≈ 35 K. The recipe gives **29.3 K**, because it converts the **radiogenic**
  flux alone (0.042 W/m²); the methodology's ≈ 35 K uses the **total** 0.087 W/m² (radiogenic +
  secular). Not a defect — a semantic line the label now draws: this `t_int` is a floor.
- *The wrong-direction factor.* The brief relayed "1.67" for the parallel seat's forward mistake; at
  ±4 Gyr from now the forward reading is **1.74**. The relayed digit came without its condition (which
  two times were compared), so the test pins the *shape* — forward ≈ 1.7 against past 3.67 — not the
  digit. Reported to the directing seat as such.

**Retired name.** `geotherm` is no longer an output of `internal_heat_nontidal`; `heat_transport_mode`
takes `mantle_radiogenic_power`; `→ dynamo_rocky via geotherm` is `status: gap` (thermal evolution,
Nimmo+ 2004 not held). `check_via --gate`: 85 via-edges, 16 mismatches = 8 allowlisted + 8 gap +
0 open. Graph: coupled core 16 = `coupled_core`, `undeclared()` empty. `check_contracts` 6/6.
Path fingerprint unchanged.

**Tooltip** (`radiogenic_heat_w_m2`) now carries the 22 TW radiogenic / 42–47 TW total pair with the
geoneutrino range as the contested side; Sclater 1980 and Davies 2010 leave the paper-request list.
