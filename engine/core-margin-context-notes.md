<!-- Brief 42 — core_state 의 액체/고체 판정이 얼마나 얇은 여유 위에 서 있는지를 판정과 함께 내보낸다 -->
# The core verdict carries its margin — Brief 42 (context notes)

2026-09-03. **§1–§2 are the pre-registration and were committed before any code ran.** §3 is
filled after. Verifiers: (병) parallel seat, (직) directing seat, (여기) work seat.

## 1. What was found, and what is reproduced here

The parallel seat asked whether a solid equation of state can serve a liquid core verdict. The
answer was about something else. On the Earth-like column (`interior_layers` Earth: p_cmb 135.3,
p_c 358.5 GPa; `core_cmb_temperature` 3760 K declared), all reproduced (여기) against the
directing seat's numbers (직):

- **Density cancels exactly.** `core_state._adiabat` consumes density only as a ratio on one
  curve, T(p) = T_cmb·(ρ(p)/ρ_cmb)^γ. Scaling the whole fit's ρ₀ by 0.9 or 1.1 moves the centre
  temperature by **0.000 000 000 0 K** (5296.6550314572 both ways). A liquid's density deficit
  relative to its solid — the obvious worry — has no effect.
- **The compressibility does not cancel, and it decides the verdict.** Holding everything else at
  `fe_prem` and varying K₀ alone, against a centre melting point of 5314.2 K:

| K₀ (GPa) | T_c (K) | margin (K) | verdict at centre |
|---|---|---|---|
| 150.0 | 5439.2 | +124.9 | liquid |
| 156.2 (`fe_eps`) | 5419.9 | +105.6 | liquid |
| **194.0** | 5313.7 | −0.5 | **the crossing** |
| **201.0 (`fe_prem`, what we use)** | **5296.7** | **−17.6** | **solid** |
| 250.0 | 5186.6 | −127.6 | solid |

  Crossing by bisection **194.01 GPa** (직: 194.23 on a column 0.1 GPa deeper); we sit 17.6 K past
  it — **0.33 % of a 5300 K quantity.** The K₀ gap between our own two iron fits flips it.
- **γ is tighter still.** Closed form γ_flip = ln(T_melt,c/T_cmb) / ln(ρ_c/ρ_cmb) = **1.5145**
  against the declared **1.5** — **0.97 % away** (직: 1.514).
- **And γ is already extrapolated for Earth.** `GAMMA_RANGE_PA` = 100–340 GPa (Alfè+ 2002's
  verified window); this column's centre is 358.5 GPa. `core_state` already appends a note when
  that happens — *"그 위에서 γ 가 어떻게 흐르는지를 이 레시피는 모른다 — 상수로 끌고 간다"* — but
  the note does not connect the range to the margin.

**The answer is not wrong.** Earth has a solid inner core and the recipe says `liquid_outer_solid_inner`
with the ICB near PREM's. Reassuring about the recipe; alarming about the margin — today a −17 K
verdict and a −500 K verdict are reported identically.

## 2. What is built, and the pre-registered outcomes

**The verdict carries its margin.** In the declared-adiabat branch `core_state` emits, beside
`conductor_phase`: the centre margin **in K and as a fraction of T_melt**, the CMB margin, the
**γ at which the centre verdict flips** (closed form) and the **K₀ at which it flips** (bisection
on a copy of the material with K₀ replaced; nothing else varied). ⚠ **Neither γ nor K₀ is
moved.** The standing rule bites: report the margin, do not tune the constant to widen it.

**The graded condition, pre-registered so it is not written after seeing the numbers**: the
centre verdict is labelled **thin** when |margin| is smaller than the melting curve's own
disagreement at the splice — the two fits' **6.8–7.5 %** in the overlap (`core_state` already
prints this) — i.e. |margin_c| / T_melt,c < **0.068**. A margin inside the curve's own uncertainty
cannot be read as a verdict about the planet; the condition says so on the label, and it says
whether γ is outside its verified pressure range for this body. Not a refusal: the answer stands;
the label tells a reader it is a knife-edge.

**Lower-bound branch**: the margin against the *bound* is emitted (it is what the branch already
prints in prose); the flips are not, because the bound is not an adiabat — ④ applies.

**Pre-registered outcomes**
- ① **Every roster body's core verdict has a comfortable margin and Earth is the only knife-edge**
  → the condition attaches to Earth-class only.
- ② **Several are thin** → the margin belongs in the output contract, not just the note.
- ③ **Some body's verdict flips inside the declared γ range** → a stronger finding; the grade drops.
- ④ **The margin cannot be computed where the adiabat refuses upstream** (no `core_cmb_temperature`,
  lower-bound branch, out-of-domain) → say so rather than emitting a null dressed as a number.

**Expectation, registered so it can be wrong (여기)**: Earth is thin (0.33 % < 6.8 %) with γ
outside range (358 > 340 GPa) → the condition fires on Earth. Pandora and the giant never reach
the declared branch (no `core_cmb_temperature`; giant out of domain), so ④ is what they return.
No roster body reaches ③ today because only one body has a declared core-side temperature.

## 3. Result — 2026-09-03, code `d133ad41`

**Branch fired: ① with the expected shape — Earth is the only body that reaches the declared
branch today, and it is thin.** Pandora and the giant return ④ upstream (Pandora: `core_state`
refuses for lack of a temperature; the giant is coreless by class), so ② and ③ cannot fire on
today's roster and are not claimed.

**Earth (`interior_layers` column, `core_cmb_temperature` 3760 K declared)**, from
`test_core_state.py` and `run.py bodies/earth.yaml`:

| output | value | anchor |
|---|---|---|
| `conductor_phase` | `liquid_outer_solid_inner` | unchanged |
| `center_margin` | **−17.6 K** | `center_margin_fraction` −0.33 % |
| `cmb_margin` | +545.0 K | |
| `gamma_flip` | **1.5145** | declared `GAMMA_CORE` 1.5 → +0.97 % |
| `k0_flip` | **194.0 GPa** | `fe_prem` K₀ 201.0 GPa |
| `margin_condition` | **thin** | 0.33 % < `MARGIN_THIN_FRACTION` 6.8 %; γ outside `GAMMA_RANGE_PA` (358.5 > 340 GPa) — both said on the label |

Density invariance measured, not asserted: ρ₀ × 0.9 / × 1.1 moves the centre temperature by
**4.5×10⁻¹² K**. Directing seat's numbers reproduced: crossing 194.0 vs 194.2 GPa (its column is
0.1 GPa deeper), γ_flip 1.5145 vs 1.514, margin −17.6 vs −17.0 K (same column difference).

**Lower-bound branch** (Earth without the declaration): `margin_condition` =
`not-computable (lower bound, no core adiabat)`, `gamma_flip` and `k0_flip` `None`, margins
against the bound emitted — ④ as an output.

**Nothing tuned.** `GAMMA_CORE` and `fe_prem`'s K₀ are untouched; the standing rule held.

**For the audit — variable names and `file:line` at `d133ad41`, not values**:
`engine/core_state.py:74` `GAMMA_CORE`, `:75` `GAMMA_RANGE_PA`, `:89` `MARGIN_THIN_FRACTION`,
`:101` `gamma_flip()`, `:108` `k0_flip_gpa()`, `:372–376` `frac_c` / `thin`; `engine/eos.py`
`FE_PREM` phase `k0 = 201.0 * GPA`, `FE_EPS` `156.2 * GPA`. Anchors: `test_core_state.py`
section "판정의 여유".

**Gate**: `check_contracts` 5/5 with the six new outputs, `chain.py check` pass, path fingerprint
unchanged (`708ff4627f24c448`); full `check.sh` result recorded in the report.

## 4. Follow-up after audit — 2026-09-03, code `ce87de81`

**③ fired, and §3 read it as ①.** Branch ③ said *"some body's verdict flips inside the declared
γ range"* and was read as the **pressure** window `GAMMA_RANGE_PA`; the range that matters is
the **value** range, and the flip is inside it. `core_state.py`'s own comment quotes Alfè+ 2002
twice: h.c.p. **solid** *"ca. 1.5"* (what `GAMMA_CORE` is) and **liquid** Hugoniot *"1.51 to
1.52 as p goes from 280 to 340 GPa"*. `fe_prem` is the liquid fit (Brief 41 `fit_state`), so the
adiabat puts the solid's exponent on a liquid density — the same disease Brief 41 catches on
density, one level up. Measured (감, 직, 여기 on my column): centre margin **−17.6 K at γ 1.50,
−5.5 K at 1.51, +6.7 K at 1.52** — the paper's own liquid range straddles the crossing
(γ_flip 1.5145). And Earth's centre (358.5 GPa) is outside **both** verified bands (340 GPa).

**What changed**: `GAMMA_LIQUID_RANGE = (1.51, 1.52)` with `GAMMA_LIQUID_RANGE_PA = (280e9, 340e9)`
beside the solid constants (no new source); output `gamma_flip_in_alfe_range`; **thin now means
γ_flip ∈ [1.50, 1.52]**, Alfè's own span — the margin is an adiabat-side quantity and its
uncertainty is measured on the adiabat side. The label says the solid's γ sits on a liquid fit
and that the liquid value would make the verdict ambiguous. **`GAMMA_CORE` and K₀ untouched.**

**② The borrowed threshold was wrong as printed, and the pre-registration's framing was too
kind to itself.** The melting splice disagreement over the two iron fits' overlap (300–365 GPa,
high/low − 1) runs **7.52 % → 3.98 %**, monotone; the prose said "6.8–7.5 %", and 0.068 was one
pressure's value (≈312 GPa), not Earth's centre (4.30 %). It is now `melt_splice_disagreement(p)`,
local, basis stated, **information only**. And §2 said the threshold was pre-registered before
the numbers; the commit timestamps (감) show `230deeee` 03:21:51 already carried 0.33 % / 1.514 /
194 — **the threshold was written after the margin was known.** No tuning risk (any threshold above
0.4 % labels Earth thin), but it is said this way, not the other.

**③ `k0_flip` null semantics** are in the contract (EN/ko): not computable — multi-phase material
or no sign change in 0.5–2× K₀ — never "no flip exists"; the multi-phase refusal is pinned on the
silicate material in `test_core_state.py`.

Earth's outputs after the follow-up: `margin_condition` thin, `gamma_flip_in_alfe_range` True,
`melt_splice_disagreement` 0.0430, `gamma_flip` 1.5145, `k0_flip` 194.0 GPa, `center_margin`
−17.6 K — unchanged numbers, corrected meaning.
