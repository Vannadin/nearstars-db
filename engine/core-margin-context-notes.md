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

## 3. Result — filled after the run

*(pending)*
