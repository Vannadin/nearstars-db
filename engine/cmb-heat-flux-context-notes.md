<!-- 브리프 60 — 핵-맨틀 경계 열류 노드: Nimmo+ 2004 식 37–39 (하단 경계층) 전사 + 선언된 철 열전도 + 단열 열류. 사전등록 → 실행 기록 -->
# CMB heat flux — context notes (Brief 60)

2026-09-03. **§1–§3 are the pre-registration, committed before any code ran.** §4 onward is filled in
after the run. Verifiers: (직) directing seat, (병) parallel seat, (여기) work seat.

## 1. What is being built, and what is deliberately not

**Owner-approved (relayed by the directing seat): the CMB heat-flux node** — the one item that
re-opens three rows at once (`property-consumer-audit-context-notes.md` §4: iron k, φ, the parked
ladder decision). Built here: **`Q_CMB` and `Q_adiabat` only**. **Not built: φ** (core entropy
production) and nothing in the dynamo — those are the next step, on top of a landed and checked
`Q_CMB`.

**What already exists.** `core_state` answers the core side of the boundary: the declared core-side
CMB temperature (`core_cmb_temperature_used`), the adiabat `T(P) = T_cmb (ρ/ρ_cmb)^γ` with
γ = 1.5. `interior_layers` answers the mantle side: `cmb_temperature` (the mantle adiabat's real
temperature at the CMB), `cmb_pressure`, `core_radius`. `mantle_flux.py` carries the *top* boundary
layer and says in its own header that eq. 39 (bottom layer) is not there.

**What is missing — exactly two things**, and both are supplied by sources we hold:
1. **The mantle's bottom boundary layer** — Nimmo+ 2004 (`2004GeoJI.156..363N`, cached, read 여기)
   eqs 37–39, extraction lines 741–749, with Table 2 (layout extraction line 532 ff.):

       δ_b = [Ra_c κ_b η_b(T_a) / (ρ_m g α_m (T_c − T̃_m))]^(1/3)     (37)
       F_b = k_b (T_c − T̃_m) / δ_b                                   (38)
       η_b(T_a) = f η₀ exp[−ζ (T_a − T₁)]                            (39)
       Q_C = 4π R² F_b                                                (line 578)

   Table 2: κ_b = 10 ± 2 ×10⁻⁷ m²/s (eq. 37), f = 10, T₁ = 3400 K (eq. 39), η₀ = 10²¹ Pa s, ζ = 1.0 ± 0.5
   ×10⁻², Ra_c = 600, ρ_m = 4800, α_m = 2.2 ± 0.3 ×10⁻⁵, g = 9.8, C_pm = 1200 — the last six are the
   ones `mantle_flux.py` already declares from the same table. *"T_a is the mean of T_c and T_m"* (line
   903). **k_b is derived exactly as k_t was**: κ_b ρ_m C_pm = **5.76 W/(m·K)**, licensed by the same
   Hofmeister sentence (line 944: κ_t and κ_b are both *"based on Hofmeister's (1999) calculations"*).
   ⚠ **The T_m of eq. 37 is the real temperature at the base of the mantle, not the potential
   temperature** — eq. 29 (line 550): T_m = T̃_m(z) exp(−α_m g z/C_pm). Recovered by closure, not read
   (§2); the potential-temperature reading gives δ_b = 738 km against the printed 140.
2. **A declared iron thermal conductivity.** Nimmo Table 1 (layout line 444): **k = 50 ± 20 W/(m·K)**,
   eq. 25. Gaidos+ 2010 (lines 972–989) span 28–100 for iron; 50 ± 20 sits inside. **Declared the way ζ
   is: a value, a band, a source; the band carried into everything it produces.** This does **not**
   reverse Brief 54's refusal of a `k(P,T)` *front* — the literature supplies a constant with a band,
   which is what this node needs and all it declares.

**Composition.** `Q_adiabat = 4π r_cmb² · k · |dT/dr|_ad` at the CMB, core side, from the existing
adiabat: dT/dr = γ (T/ρ)(dρ/dP)(−ρ g_cmb) with dρ/dP from the core material's own `density(P, T)`
(finite difference) and g_cmb = G M_core / r_cmb², M_core = mass × core_mass_fraction (declared). The
paper's own Q_k (eq. 25, its density model) is **6.2 TW** (line 1341) at k = 50.

**Conditions that ride on every number out of this node**:
- **γ = 1.5 is a solid (h.c.p.) value used on a liquid outer core** — the standing `core_state` caveat,
  now upstream of a heat flow, so it travels on `Q_adiabat` (`GAMMA_LIQUID_RANGE` 1.51–1.52 is the
  liquid's; the spread is small and stated).
- **Calibrated at source** (Nimmo's Earth), as `mantle_flux` already says of the top layer; g in eq. 37
  is the paper's surface g (Table 2), kept as transcribed.
- **T_c is a declaration** (`core_cmb_temperature`); without it `core_state` runs its lower-bound branch
  where the core-side temperature *equals* the mantle adiabat → no jump → **refuse by name**, never a
  zero flux.

## 2. Pre-measured before this text was written (여기, `python3` on the constants — measurement, not prediction)

- **Transcription closes on the paper's own numbers.** With T_c = 4161 K (the paper's nominal CMB
  adiabat, line 941) and T̃_m from eq. 29 on the printed 1603 K potential temperature at z = 2890 km
  (2694 K): **δ_b = 144 km** against the printed **140 km** (line 1316); **Q_C = 8.9 TW** against the
  printed **9 TW** (line 1317). That licenses the eq. 29 reading and the derived k_b.
- **The engine's Earth lands outside**: declared T_c 3760 K (`earth.yaml`), mantle adiabat at the CMB
  2526 K (`interior_layers`), r_cmb 0.547 R⊕ → **δ_b 394 km, Q_CMB 2.75 TW** — below Nimmo's 4.5–9 TW.
  Cause visible without tuning: the engine's jump is 1234 K against the paper's 1467 K, and T_a is 617 K
  colder, which raises η_b 17×. **Q_adiabat at k = 50: 6.64 TW** (paper 6.2 on its density model),
  band 3.99–9.30 over k = 30–70; dT/dr 0.87 K/km at g_cmb 10.4.

## 3. Pre-registered outcomes

- ① Earth's `Q_CMB` lands inside Nimmo's printed range (4.5–9 TW) → calibrated; φ becomes worth building.
  *Fires only for the paper's own inputs (§2 first bullet).*
- ② it lands outside → built but uncalibrated; **reported, not tuned — k, γ, ζ, f, T₁ stay declared**.
  *Expected on the engine's own Earth (§2 second bullet): 2.75 TW, and `Q_CMB < Q_adiabat`, which is a
  statement about the declared T_c = 3760 K, not about Earth.* Both readings are emitted: the
  transcription closure on the paper's inputs (test) and the engine's own (recipe).
- ③ eq. 39 needs something we do not have → named, stop. *Not expected: every symbol is supplied (§1).*
- ④ anchors bit-identical (`interior.py`, `core_state.py`, `solve()` untouched — a new module, a new
  node); gate FAIL 0.

## 4. Run record — 2026-09-03, code `b73d7293`

**Branch fired: ② on the engine's own Earth, ① on the paper's own inputs — both emitted, neither tuned.**

| input set | T_c | T̃_m | jump | T_a | η_b | δ_b | Q_CMB | paper |
|---|---|---|---|---|---|---|---|---|
| Nimmo's (test §1) | 4161 K | 2694 K (eq. 29 on 1603 K) | 1467 K | 3428 K | 7.6×10²¹ Pa s | **144 km** | **8.92 TW** | 140 km / 9 TW — closes |
| engine Earth (recipe) | 3760 K (declared) | 2526 K (`interior_layers`) | 1234 K | 3143 K | 1.3×10²³ Pa s | **394 km** | **2.75 TW** (band 1.54–4.77 over ζ ± 0.5 × κ_b ± 2) | outside 4.5–9 |

**Cause of ②, visible without touching a constant**: the engine's jump is 233 K smaller and its T_a is
285 K colder than the paper's, and η_b is exponential in T_a — a 17× viscosity, a 2.7× thicker layer, a
3.2× smaller flux. Both differences trace to the declared core-side temperature 3760 K (`earth.yaml`)
against the paper's nominal 4161 K CMB adiabat and to our mantle adiabat's 2526 K against eq. 29's
2694 K. **That is a statement about the two declarations, not about Earth; k, γ, ζ, f, T₁ stay where
Table 1/2 put them.**

**Q_adiabat, engine Earth**: fe_prem at 135.3 GPa / 3760 K, ρ 9907 kg/m³, dρ/dP by finite difference,
g_cmb 10.67 m/s² (M_core = 0.325 M⊕ — the pre-registration's 6.64 TW used a rough 1.9×10²⁴ kg core;
the exact core mass gives **6.79 TW** at k = 50, band **4.07–9.50** over k 30–70; |dT/dr| 0.89 K/km).
Paper: 6.2 TW on its own density model (line 1341). **Verdict on the engine's Earth: Q_CMB < Q_adiabat**
(2.75 < 6.79) — at the declared T_c the top of the core would be thermally stratified. This is the number
φ would consume; it is **not** a dynamo statement and none is made (Brief 60's boundary).

**Refusals pinned**: undeclared core-side temperature → `cannot-say (no declared core-side CMB
temperature …)` (Pandora, which declares none, refuses by name in the chain); T_c ≤ T̃_m → refuse; giant →
out of domain. **Not touched**: `chain.yaml:417-418` (the `cmb_heat_flux` / `geotherm` gaps into
`dynamo_rocky`) — the supplier now exists, the consumer wiring is the φ step and stays a gap until then.

**Anchors** bit-identical by construction (`interior.py`, `core_state.py`, `solve()` untouched; new
module, new node). `check_contracts` 8/8; `chain.py check` 48 nodes / 182 edges; `check_via --gate` pass;
`test_cmb_flux` 0.1 s. Gate: appended after the run.
