<!-- 브리프 54 — 세 물성(열전도·전기전도·점성)의 소비처 감사. 셋 다 새 물질 메서드 없이 닫힌다 — 두 거절과 하나의 이미-지어짐 -->
# The property set's consumer audit — what Brief 54 measured (context notes)

2026-09-03. **Measurement only; no material method was built, `mantle_flux.py` and
`tidal_transport.py` untouched.** The three properties were resolved as *transcribable* by
surveys ⑱–㉑ (`electrical-conductivity-`, `thermal-conductivity-`,
`viscosity-context-notes.md`). This note does the other half C5 demands — *who would call it* —
and records the answer where the next session will find it, with the transcriptions left intact
in their survey notes so they are ready if a consumer ever appears. Verifiers: (직) directing
seat, (병) parallel seat, (여기) work seat re-ran the greps and reproduced every number below.

**Outcome: the directing seat's branch ② by the letter, ① in effect.** Exactly one property
(viscosity) has a live consumer that a transcription serves — and that transcription **already
landed in Brief 39** (`rheology.py`). The other two refuse for two different causes that share
one root, the missing CMB heat flux (`chain.yaml@«heat_transport_mode 안에 들어 있었는데, 그건 안에서 나오는 열이고»`, both `status: gap`). **Nothing is
built; the work-order item closes.**

## 0. The greps, re-run rather than trusted (여기)

The directing seat's leads reproduce, with one addition it did not have:

- `q_cmb | cmb_flux | core_flux | \bq_c\b | adiabatic heat flux` over `engine/*.py`,
  `chain.yaml` → **nothing executable**. The only hits are prose (`mantle_flux.py@«thermal conductivity at the to»` on
  Nimmo's κ_t, `rheology.py@«# the 1-bar or ice-surface temperature — the ice-giant anchors declare 76 K and 72 K through»,198` "no conductive lid") and one *name*:
  `tidal_transport.py@«conductive_flux=dict(value_wm2»` emits `conductive_flux = HD − F_m`, a residual **derived from Ė**,
  not from any conductivity.
- Thermal conductivities in the engine: exactly two, both constants —
  `mantle_flux.py@«KAPPA_T = 6.0e-7             # m²/s, mantle thermal diffusivity (eq. 34)»,60` (`KAPPA_T = 6.0e-7` → `K_T = 3.456 W/(m·K)`) and
  `tidal_transport.py@«k=4.0,            # W/(m K), Table 5»` (`k = 4.0`, Kankanamge & Moore Table 5).
- Electrical conductivity / magnetic Reynolds: `dynamo_rocky.py@«* **`Rm > 40` is QUOTED, NEVER EVALUATED.** The doc lists it at step 2 as a disqualifier beside two class»,79` and
  `rocky-planet-dynamo-methodology.md@«**quoted, not evaluated here**» and rocky-planet-dynamo-methodology.md@«evaluated** — this document carries no magnetic-Reynolds formula»,103-104`, every hit saying **quoted, not evaluated**.
  No `sigma`, no `μ₀`, no velocity anywhere executable.
- Viscosity: **two** consumers, not one — `rheology.py@«"unobtained Karato & Wu 1993; the temperature is the top of the convecting adiabat "»` (Rovira-Navarro eq. 5, Monteux
  eq. 8, Maxwell time) consumed at `interior.py@«RECIPE, VERSION, "3층 역산에는 포텐셜 온도 선언이»`, and `mantle_flux.py@«def viscosity(t_m_k: float, zeta: float = ZETA) -> float:»`
  (Nimmo+ 2004 eq. 35, `η₀ exp[−ζ(T−T₀)]`) consumed by `implied_flux`.
- **Named non-consumers — the words a grep for these properties will hit, and what they are:**
  `tidal_transport.py@«conductive_flux=dict(value_wm2»` `conductive_flux` is `HD − F_m`, a residual from Ė, no k in it;
  `fermi.py`'s `ETA_*` is the electron degeneracy parameter η, not a viscosity;
  `mantle_flux.py@«thermal conductivity at the to»` and `rheology.py@«# the 1-bar or ice-surface temperature — the ice-giant anchors declare 76 K and 72 K through»,198` say "conductivity"/"conductive" in prose only.

## 1. Thermal conductivity — refuse: no consumer; both holders are reproduction constants

**Who consumes it today.** Nobody consumes a *property*. Two published models we reproduce carry
a constant:

| site | value | what it is inside | what pins it |
|---|---|---|---|
| `mantle_flux.py@«K_T = KAPPA_T * RHO_M * C_PM   # 3.456 W/(m·K)»` | `K_T = κ_t ρ_m C_pm = 3.456` | Nimmo+ 2004 eqs 34–36, F_t = k ΔT/δ_t (line 96) | `test_mantle_flux.py` §1: 42 TW ← **1614 K** against the paper's printed 1603 K; the derivation is licensed by Nimmo's own Hofmeister sentence (`mantle_flux.py@«Hofmeister's (1999) calculatio»`) |
| `tidal_transport.py@«k=4.0,            # W/(m K), Table 5»` | `k = 4.0` | K&M 2019 eq. 36 rearranged: κ (line 90), F_conv (105), Pe (107), G (108) | the §6 printed-flux closure HD = 2.509 (`tidal-interior-context-notes.md` §4) |

**What would change if either asked a material instead.** Q_M is linear in k (δ_t carries no k),
so the closure moves with it — measured (여기): at T_m = 1600 K, k = 3.456 → **39.55 TW**;
k = 4.0 (the other constant we hold) → **45.77 TW**; the inversion for the paper's 42 TW moves
**1614 → 1580 K**, outside the ±15 K test band around the printed 1603 K. A material k that
differs from 3.456 at Nimmo's top-of-mantle state does not refine the model, it breaks the
reproduction that makes the consistency verdict trustworthy. Same shape for K&M's Io closure.
**So the refusal is the directing seat's reading, confirmed on the numbers.**

**The nearest future consumer, and why it is the worst place to start.** The one node that
*would* want a physical k is the CMB heat flux (`chain.yaml@«heat_transport_mode 안에 들어 있었는데, 그건 안에서 나오는 열이고»` `cmb_heat_flux`, `:418`
`geotherm`, both gap) — and Gaidos+ 2010 eq. 14 (now cached, read 여기, extraction line 398)
shows what it needs: `Q_K ≈ 4π R_c² k α_c g_c T_c / c_p`, the **iron** conductivity, which no
survey touched and which Gaidos themselves span 28–29 vs ~100 W/(m·K) (lines 972-989). The
mantle-side flux would want the lower-mantle k at ~136 GPa / ~4000 K — outside the Manthilake
chain's measured box (8–26 GPa, ≤ 1273 K; `thermal-conductivity-context-notes.md` §5), where it
returns ~1.6× Ohta+ 2012 with no error-bar overlap and the two are not independent (Ohta adopts
Manthilake's eq. 1 and a = 0.43). Reading more papers does not close that; a consumer that needs
the value exactly there is not a reason to transcribe it now.

## 2. Electrical conductivity — refuse: the gate is blocked on φ, and σ has no leverage on it

**Who consumes it today.** `Rm > 40` at `dynamo_rocky.py@«1: (1.0, 1.0),             # d»` — a *label* in the ladder, quoted
from Gaidos+ 2010 and never evaluated. Brief 52 wrote the formula into the methodology
(`Rm = V L/λ`, `λ = 1/(μ₀σ)`) as quoted-not-evaluated. Survey ⑱'s transcription (Stixrude+ 2020)
is **silicate liquid**, the input of a basal-magma-ocean dynamo that is not a node; the core
dynamo needs **iron** σ, which neither ⑱ paper prints (the Pozzo 2012 request was withdrawn in
Brief 47 for lack of a consumer, and that stands). The one iron-alloy σ paper we hold, Pommier 2018
(`2018E&PSL.496...37P`, Brief 58), is points without a law at ≤ 8 GPa — two orders below our bodies
— so "no cross-check" is now "no law, wrong domain" (`core-melt-depression-context-notes.md` §8 ③).

**Cause correction, recorded so nobody inherits it (directing seat, on reading this): the brief
said the block was V. It is φ.** The brief's expectation was made from the `Rem ~ 16(B_c/1 µT)`
shortcut; the cached paper's general form eliminates V. The refusal reads "blocked on φ".

**Is V reachable from anything we solve? — checked against the cached paper, not the summary.**
L is: `interior_layers` emits `core_radius` and `chain.yaml@«tidal_locking:»` already wires it. V is **not** —
but Gaidos's own route never uses V. Their eq. 3–4 (lines 183-200, 여기):

    Rem ≈ a₂′ [φ T̄ (R_c − R_i)]^{1/3} (R_c − R_i) / λ,   p = φT̄ / (Ω³(R_c−R_i)²),  φ = Φ/M_c

V is eliminated through the dimensionless convective power p; what remains is **φ, the entropy
available per unit mass and time in the core** — set by the CMB heat flow minus the adiabatic
conduction Q_K (eq. 14). That is `chain.yaml@«heat_transport_mode 안에 들어 있었는데, 그건 안에서 나오는 열이고»` again: **no node emits a core-side heat
flux**, `internal_heat_nontidal` stops at the mantle top (`implied_surface_heat_flow`) and has no
thermal evolution. The directing seat's "`Rem ~ 16(B_c/1 µT)` needs the field we predict" is
Gaidos's *terrestrial shortcut* (line 207), not the general form; the general form is not
circular, it is blocked on φ. **Ordering does not change**: nothing we solve reaches φ, so the
gate stays a quotation until a CMB-heat-flux node exists.

**And σ is the small lever.** Gaidos fix λ ≈ 2 m²/s (Stevenson 2009) and note that for an
Earth-size core L ~ 3×10⁶ m, V as small as 10⁻⁴ m/s gives Rm > 40 (lines 101-103; 여기:
10⁻⁴·3×10⁶/2 = 150); their terrestrial estimate is Rem ~ 10⁴. A factor-2 uncertainty in σ moves
Rm by a factor 2 against a threshold it clears by 2–3 decades. This is the Zhang & Rogers §2.8
point already recorded at `dynamo_rocky.py@«Zhang & Rogers 2022 §2.8 argue the threshold is generically met while the liquid core convects — which»`: the gate is generically met while the liquid core
convects, and *whether it convects* is the φ question. **A transcribed σ would therefore be the
least informative input to a gate that cannot be evaluated anyway.**

## 3. Viscosity — a live consumer, already served; nothing further to transcribe

**What Brief 39 actually concluded** (`figure-relaxation-context-notes.md` §4, `21665370`; read
in full, not the handoff's one line):

- Consumer named by the owner: `body_figure`'s fossil-bulge caveat. Built as one labelled
  verdict (`figure_relaxation`, `maxwell_time_mantle_top`, `relaxation_threshold_max`) composed
  in the `interior_layers` wrapper (`interior.py@«RECIPE, VERSION, "3층 역산에는 포텐셜 온도 선언이»`), not in `solve()`; anchors bit-identical
  by construction.
- **The two transcribable laws of survey ㉑ are exactly `rheology.py`'s two laws** —
  Rovira-Navarro+ 2021 eq. 5 (`viscosity_rovira`) and Monteux+ 2016 eq. 8
  (`viscosity_monteux`). The survey came after the code and grounds it; there is no third law
  to add.
- Every constant is a declaration, read as a **family**: `RN_E_A_RANGE × RN_ETA_S_RANGE` gives
  the threshold 700–1009 K at 4.54 Gyr (engine solidus 1661 K), and the verdict reads the whole
  grid. The verdict is insensitive to the constants because τ_M spans 20+ decades.
- Branch ① fired: Earth (1600 K) relaxes with ~590 K to spare; Pandora refuses by name (no
  temperature); the giant is refused upstream. The consumer never branches **on today's roster
  declarations** — a fact about the roster, not the code, and the cold branches are pinned
  reachable (`test_rheology.py` §4).

**What would change if it asked a material instead of a constant.** It already does — that is
what `rheology.py` is. The gaps survey ㉑ §4 names (activation volume, grain size for diffusion
creep) have **no source in the cache** and end as not found, not as a build.

**Two live consumers that both already have what they need is a stronger closed state than
one** — the refusal to build a third viscosity law is safe on both sides, not just on the figure
verdict's. **The second consumer is a reproduction constant, same verdict as §1.** `mantle_flux.py@«def viscosity(t_m_k: float, zeta: float = ZETA) -> float:»`
is Nimmo's Frank-Kamenetskii form with ζ = 0.01 (declared, ±0.5×10⁻² kept). Substituting
`rheology.py`'s Arrhenius law there would move the 1614 K closure for the reason §1 gives.
Recorded here from Brief 55, reproduced (여기): ζ = E/(RT²) over E = 250–350 kJ/mol,
T = 1600–2500 K gives **0.00481–0.01644** against the printed 0.005–0.016 (Solomatov 1995);
the *adopted* ζ = 0.01 back-converts to **E ≈ 212.8 kJ/mol at 1600 K**, below the quoted 250
floor, re-entering it only at **T ≈ 1734 K**. Internally consistent, but ζ = 0.01 sits at the
low edge of its band, not the midpoint. It matters only if ζ is ever varied; it needs no paper.

**What "wired" in the handoff's row 3 turned out to mean — a missing call, not missing physics,
and an unstated denominator.** `radiogenic.py@«# Brief 46 — the declared potential temperature, checked against this budget (Nimmo+ 2004 eqs 34–36).»` *does* pass its budget into
`mantle_flux.consistency` (forward direction wired; `test_mantle_flux.py` §4 exercises it through
`rg.solve`). What nobody calls in production is `invert_for_flow` — the inverse, budget → T_m —
which is what Brief 57 composes. Found on the way: the forward direction compares Q_M against
**`total_w`** (21.15 TW) and Brief 57's inverse uses **`mantle_w`** (14.81 TW), and neither
`mantle_flux.py`'s header nor `consistency`'s notes nor the consistency context notes state the
choice. Physics is one-sided — F_t crosses the mantle's *top* boundary layer and crustal production
is generated above it, so `mantle_w` is like-for-like (Korenaga 2008's *convective* Urey ratio, the
one the methodology names as the geotherm consumer's). Cost of aligning the forward, measured
(여기): Earth at 1600 K, Q_M 39.22 TW → ratio 1.84 / Urey 0.54 against total, **2.63 / 0.38**
against mantle — same label (floor 1/3), different number; a body at 2.2 flips to too-hot. **Not
changed here; named for the owner.**

## 4. What closes, what stays open

- **Closed**: the work-order item "three missing properties" — no new material methods. The
  transcriptions stay where they are (survey notes §1/§3 each) and are ready if a consumer
  appears.
- **The one thing that would re-open three rows at once** (directing seat drew the third): a CMB
  heat flux node (`chain.yaml@«heat_transport_mode 안에 들어 있었는데, 그건 안에서 나오는 열이고»`). It is the consumer for iron k (eq. 14), for φ (eq. 3–4)
  and hence for σ — **and φ ~ 100 MW/K is the same quantity as the parked owner decision on
  replacing the dynamo ladder with Nimmo+ 2004's entropy-production criterion**, whose threshold is
  uncertain over four orders (0.1–1000 MW/K). It is also the thermal-evolution model Nimmo & Primack
  2020 delegate to Nimmo+ 2004. One owner question with three payoffs, not three asks; a much larger
  item, not proposed here.
- **Not a refusal cause anywhere**: Karato & Wu 1993 — Brief 55 withdrew it (every constant is
  cited jointly; only Rovira-Navarro's E_a = 300 rests on it alone, labelled as an unchecked
  secondary citation at `rheology.py@«# "Mantle solidus viscosity" 1·10¹⁶ Pa·s and "Activation energy" 300 kJ/mol, footnote 4 =»` and `viscosity-context-notes.md` §1).

## 5. The stress finding — and "blocked" has meant two different things (Brief 59, c4 + 직, 여기 re-run)

- **The engine carries no stress.** `stress|yield|strain|deviatoric|sigma_y` over `engine/*.py`
  (tests excluded) and `chain.yaml`: the only hits are the word "constrains" in `mantle_flux.py`'s prose
  (lines 19, 31). No stress exponent anywhere; every viscosity law held is Newtonian as transcribed.
- **But the buoyancy stress scale αρgDΔT_rh is constructible from what is already computed.** α is not
  stored; it recovers as `alpha_k / K_T` — silicate **2.32×10⁻⁵ /K at 24 GPa, 1.03×10⁻⁵ at 135 GPa**
  (여기 reproduced through `Phase.k_t`). ΔT_rh from two overlapping routes: 1/ζ gives 67–200 K,
  Frank-Kamenetskii RT²/E_v gives 53–106 K.
- ⚠ **Caveat that rides with any α by this route**: `alpha_k` is a stored constant under the
  volume-independent Anderson & Goto approximation — **6.92×10⁶ Pa/K at both pressures** (여기 checked;
  it does not move) — so the 2.3× fall in α across that range is **K_T growing in the denominator, not a
  measured α(P)**. Probably the right direction, wrong provenance for the magnitude. Nothing should emit
  an α this way without saying so. **Not built.**
- **The point.** What a regime criterion lacks is not the stress but **the threshold to compare it
  against** — a yield strength, which nothing in the corpus prints. That is a *different kind* of gap from
  the dynamo gate's: `Rm` was blocked on another computed quantity (φ, §2) that only Earth could anchor,
  so it closed on itself; this is blocked on a material property with a value, which a paper can simply
  supply. **A citation can close this one and could not close that one.** Solomatov 1995 is **not held** — and
  not with the owner either: the owner gave up on it at 15:18 KST (*"논문에 돈내야한대...ㅠㅠ 방법이 없다."*,
  1588ff47, 09-03 15:18; request cancelled 15:20). This line was committed in `ef6a40ca` at 15:37, nineteen
  minutes after that; corrected by Brief 64.

## Related

- [`engine/thermal-conductivity-context-notes.md`](thermal-conductivity-context-notes.md) — the transcription, kept
- [`engine/electrical-conductivity-context-notes.md`](electrical-conductivity-context-notes.md) — the transcription, kept
- [`engine/viscosity-context-notes.md`](viscosity-context-notes.md) — the two laws `rheology.py` carries
- [`engine/figure-relaxation-context-notes.md`](figure-relaxation-context-notes.md) — Brief 39, the live consumer
- [`engine/mantle-flux-consistency-context-notes.md`](mantle-flux-consistency-context-notes.md) — where ζ and K_T live
- [`engine/rocky-dynamo-context-notes.md`](rocky-dynamo-context-notes.md) — the quoted gate
- [`engine/SESSION-HANDOFF.md`](SESSION-HANDOFF.md) — "three missing properties", now closed
