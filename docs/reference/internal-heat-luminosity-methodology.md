<!-- 행성·갈색왜성 내부열(잔여+Kelvin-Helmholtz+방사성) → T_int → 유효온도 T_eff를 도출하는 방법론 레퍼런스 -->
# Internal-Heat / Self-Luminosity Methodology: T_int and the Effective Temperature

Method reference for deriving a planet's or brown dwarf's **non-tidal internal heat**
(its self-luminosity `L_int`), turning it into an internal-only effective temperature
`T_int`, and combining that with the irradiation equilibrium temperature `T_eq` to get
the body's true effective temperature. Same spirit as the
[dynamo-scaling doc](planetary-dynamo-scaling.md) and the
[tidal-heating doc](tidal-heating-methodology.md): cite the relation + a calibration
that reproduces known bodies, not a fabricated measurement.

This is a **recurring NearStars derived value**, used ad-hoc for Alpha Centauri A b (Polyphemus)
(α Cen A b), ε Ind A b, and now Proxima c, so it gets a canonical grounded recipe here.

> Citations resolved against NASA ADS (the registered `ADS_API_TOKEN`), not ad-hoc
> web search; arXiv id where one exists, otherwise the authoritative ADS bibcode
> (flagged "no arXiv"). See §9 for the verified list.
> This is a working reference, not a textbook.

**Scope note: this doc is the NON-tidal internal heat.** The internal energy budget of
a sub-stellar/planetary body has four sibling sources, split across two docs:

| Source | Covered where |
|---|---|
| Residual heat of formation (accretion + initial entropy) | **this doc** |
| Kelvin–Helmholtz gravitational contraction (the dominant giant-planet term) | **this doc** |
| Radiogenic (U/Th/K decay) + secular cooling (rocky bodies) | **this doc** |
| Helium rain / phase separation (Saturn-type), deuterium burning (>~13 M_J) | **this doc** |
| **Tidal dissipation** | [`tidal-heating-methodology.md`](tidal-heating-methodology.md) |

The **irradiation / equilibrium temperature** `T_eq` (what the star delivers) is the
[tidally-locked-temperature doc](tidally-locked-temperature-methodology.md). All of these
**combine** through the single relation in §1: `T_eff⁴ = T_eq⁴ + T_int⁴`, where `T_int`
here folds in only the non-tidal sources (add the tidal flux into `T_int` if it is
non-negligible, see that doc).

## Contract — `internal_heat_nontidal`

**Returns** — `l_int` [W] · `t_int` [K] · `radiogenic_power` [W] · `mantle_radiogenic_power` [W] ·
`crust_radiogenic_power` [W] · `radiogenic_power_low` [W] · `radiogenic_heat_w_m2` [W/m2] ·
`radiogenic_power_history_4gyr` [—] · `mantle_top_boundary_layer` [km] · `implied_surface_heat_flux` [W/m2] ·
`implied_surface_heat_flow` [W] · `heat_flow_consistency` [—] · `urey_ratio` [—] ·
`mantle_temperature_floor_min` [K] · `mantle_temperature_floor_max` [K] · `mantle_temperature_floor_verdict` [—] ·
`mantle_temperature_width_zeta` [K] · `mantle_temperature_width_set` [K] · `mantle_temperature_width_denominator` [K] ·
`mantle_temperature_width_surface` [K]
**Needs** — `mass_earth` [M_earth] · `core_mass_fraction` [—] · `ice_mass_fraction` [—] ·
`radius_earth` [R_earth] · `body_class` [—] · `age_gyr` [Gyr] · `potential_temperature` [K]
**Discriminating keys** — `body_class`: rocky bodies get the present-day radiogenic budget; giant,
sub-Neptune, brown-dwarf and stellar classes are refused, because their internal heat is the cooling
luminosity L(M, age) and this recipe does not supply an unverified cooling track (the same refusal
`dynamo.py` makes). `core_mass_fraction` undeclared → refused (no silicate mass to hang the
concentrations on).
**Grade** — **analog**: the concentration set (Earth (1) chondritic, with Earth (2) non-chondritic
emitted beside it as `radiogenic_power_low`) and the 70 % mantle share are declarations; the
silicate mass is derived from the body's own `core_mass_fraction`. Reproducing Earth's ~21 TW is
a closure on the constants, not a prediction.

`l_int` for a rocky body **is** the radiogenic power, and `t_int = (F/σ)^¼` is §1's relation applied to
the **radiogenic flux alone** (Earth ≈ 29 K; §1's ≈ 35 K uses the total 0.087 W/m², radiogenic + secular,
so this `t_int` is a floor on that). `mantle_radiogenic_power` replaces the former `geotherm` output, which was one
word covering a heat budget here and a T(P) profile in `interior_layers`. The four isotope constants
are standard nuclear data read from Nimmo & Primack 2020's **unpublished draft table** (LaTeX source
after `\end{document}`; absent from the PDF) and checked by closure against that draft's own totals
and the appendix's printed 22 TW — see `engine/radiogenic-budget-context-notes.md`.
`mantle_top_boundary_layer`, `implied_surface_heat_flux` and `implied_surface_heat_flow` are Nimmo+ 2004 eqs 34–36
evaluated at the **declared** `potential_temperature` (top boundary layer only; `k_t` derived as κ_t ρ_m C_pm, not
printed; calibrated at source on present-day Earth), and `heat_flow_consistency` compares that implied flow with
`radiogenic_power` — a consistency check on the declaration with secular cooling as the expected difference, never
the body's actual heat flux; `cannot-say` when no temperature is declared. `engine/mantle-flux-consistency-context-notes.md`.
`mantle_temperature_floor_min/max` (Brief 57) is the same chain **inverted**: the potential temperature at which the
top boundary layer sheds exactly the radiogenic power — a **floor** on T_m (secular cooling adds to the flow), emitted
as a family, never a point: the union over ζ (Table 2's ± 0.5), the two concentration sets, and both denominators
(`mantle_w`, like-for-like with the top boundary layer, against `total_w`, what `heat_flow_consistency` uses — carried
both ways, the inconsistency named in `engine/property-consumer-audit-context-notes.md` §3), with each width emitted
by name (`mantle_temperature_width_*`; `surface` re-evaluates at T_s = 200 K). Consumer: art direction's tectonic-regime
likelihood, which is **not** classified here. Outside the 1000–2500 K bisection bracket the verdict refuses by name
instead of returning the bracket end. For a tidally heated body the floor is not its mantle temperature.
`radiogenic_power_history_4gyr` = H(−4 Gyr)/H(now) is decay physics only; thermal evolution
is not built (Nimmo+ 2004 is held — its bottom boundary layer is `q_cmb`, below), and the edge to `dynamo_rocky`
stays a gap because its consumer wiring is the φ step, not for want of the paper.

## Contract — `cmb_heat_flux`

**Returns** — `q_cmb` [W] · `q_cmb_min` [W] · `q_cmb_max` [W] · `cmb_boundary_layer` [km] ·
`cmb_heat_flux_density` [W/m2] · `eta_bottom` [Pa s] · `q_adiabat` [W] · `q_adiabat_min` [W] · `q_adiabat_max` [W] ·
`adiabat_gradient_cmb` [K/km] · `g_cmb` [m/s2] · `k_core` [W/(m K)] · `cmb_jump` [K] · `cmb_flux_verdict` [—] ·
`q_cmb_in_paper_range` [—]
**Needs** — `mass_earth` [M_earth] · `core_mass_fraction` [—] · `core_radius` [R_earth] · `cmb_pressure` [GPa] ·
`cmb_temperature` [K] · `core_cmb_temperature_used` [K] · `core_cmb_temperature` [K] · `core_material` [—] · `body_class` [—]
**Discriminating keys** — `body_class`: rocky bodies only (a giant has no silicate bottom boundary layer).
`core_cmb_temperature` undeclared → refused by name: `core_state`'s lower-bound branch sets the core-side
temperature equal to the mantle adiabat, so there is no jump to drive a boundary layer. `core_radius` or
`core_mass_fraction` absent → refused.
**Grade** — **analog**: Nimmo+ 2004 eqs 37–39 are calibrated at source on present-day Earth; `k_b` is derived
(κ_b ρ_m C_pm = 5.76, the same step as `k_t`); the iron conductivity `k_core` = 50 ± 20 W/(m·K) (Nimmo Table 1;
inside Gaidos+ 2010's 28–100) is a **declaration**, not a material method — Brief 54's refusal of a k(P,T) front
stands; γ = 1.5 is the solid value used on a liquid core (the `core_state` caveat, now riding on `q_adiabat`).

`q_cmb` is Nimmo's eq. 37–39 bottom boundary layer: δ_b from the local Rayleigh number with η_b(T_a) = f η₀ exp[−ζ(T_a − T₁)],
T_a the mean of the core-side CMB temperature and the mantle's **real** base temperature (eq. 29 — the potential-temperature
reading misses the paper's own 140 km by 5×; recovered by closure: 144 km / 8.9 TW against the printed 140 km / 9 TW).
`q_cmb_min/max` span ζ ± 0.5 × κ_b ± 2. `q_adiabat` = 4π r² k |dT/dr| with dT/dr from the core adiabat T ∝ ρ^γ and
dP/dr = −ρ g_cmb; `q_adiabat_min/max` span k 30–70. `cmb_flux_verdict` says only which is larger — no dynamo statement
is made here (φ is the next step). `q_cmb_in_paper_range` compares with Nimmo's printed 4.5–9 TW; on the engine's own
Earth (declared core-side 3760 K, adiabat base 2526 K) it lands **outside** (≈ 2.75 TW) and is reported, not tuned.
⚠ **`q_cmb` is a lower bound** (Brief 62): the declared core-side temperature is itself a lower bound whose two named
biases point down (`core-state-methodology.md:60`), and η_b is exponential in T_a, so a lower-bound input yields a
lower-bound flux — the true value is higher, and 2.75 TW must not be read as "no dynamo". Turning the bound into a
solution is the core energy-balance closure (Brief 62 B, `engine/cmb-heat-flux-context-notes.md` §5).
`engine/cmb-heat-flux-context-notes.md`.

## Contract — `core_energy_balance`

**Returns** — `core_cmb_temperature_solved` [K] · `core_cmb_temperature_solved_min` [K] · `core_cmb_temperature_solved_max` [K] ·
`core_cmb_temperature_declared` [K] · `core_cmb_solved_minus_declared` [K] · `q_cmb_solved` [W] · `q_s` [W] · `q_l` [W] · `q_g` [W] ·
`q_r` [W] · `icb_radius_solved` [km] · `icb_pressure_solved` [GPa] · `c_r_km_per_k` [km/K] · `has_inner_core_solved` [—] ·
`core_profile_mass_residual` [—] · `core_center_pressure_solved` [GPa] · `balance_residual` [—] · `band_corners_with_root` [—]
**Needs** — `mass_earth` [M_earth] · `core_mass_fraction` [—] · `core_radius` [R_earth] · `cmb_pressure` [GPa] ·
`cmb_temperature` [K] · `core_cmb_temperature` [K] · `core_material` [—] · `body_class` [—] · `dtc_dt_k_per_gyr` [K/Gyr] · `core_h_w_per_kg` [W/kg]
**Discriminating keys** — `body_class`: rocky bodies only. `core_cmb_temperature` undeclared, or no `cmb_temperature` →
refused by name (the balance needs both sides — the declared value is only the number the solution is reported beside).
No root in the physical bracket → refused by name; the bracket is not widened.
**Grade** — **analog**: Nimmo+ 2004 eq. 30 closed at the present epoch on an Earth-calibrated model whose success
criterion is "reproduce present-day Earth"; `dT_c/dt` (−33 K/Gyr) and core `H` (1.5 pW/kg) are **declarations** with
bands (33–126 K/Gyr between two published Earth models; H from 0 to 1.5); γ = 1.5 is the solid value on a liquid core;
Q_H omitted by name.

`core_cmb_temperature_solved` turns the declared **lower bound** of `core_state` into a solution: the root of
`bottom_layer(T_c) = Q_s + Q_L + Q_g + Q_R` (eqs 37–39 on the left; eqs 10, 17, 19–21, 16 on the right, every cooling term
linear in the declared `dT_c/dt`, so no time integration — Brief 62 step 1's measurement). The core profile
(ρ, g, T, ψ on r) is **built by the node** from the CMB inward with `material.density` and hydrostatics (the engine emits
no radial profile); the inner core is where that adiabat meets the material's melting curve, `c_r_km_per_k` = dR_i/dT_c
from the two slopes there (a ratio of two nearly parallel slopes — knife-edge, reported as such). `_min/_max` re-solve
the four corners of the dT_c/dt × H bands. **The solved value is not fed back to `core_state`** (C14's scope; feeding it
back moves anchors and is a separate decision). Transcription closure: on the paper's own inputs Nimmo's analytic core
(test file only) reproduces Table 4 component by component within 10 % and the root lands at 4152 K against the printed
4155. The profile is RK4 from the CMB inward and is anchored: its centre pressure must match `interior.solve()`'s own
`core_pressure` for the same body (Earth: 358.47 vs 358.46 GPa, ±0.1 %, inputs taken from `interior.solve()` itself so no
transcribed constant can round; the inner 2 % of the radius, 0.03 %, not integrated), and at
the declared 3760 K it finds the same inner core as `core_state` (ICB 351.3 vs 351.4 GPa). On the engine's own Earth
the solved T_c is 3978 K, and there the core is **all liquid** — closing the loop removes Earth's inner core
(`fe_prem` is temperature-independent, so the pressure stays while the adiabat rises through the melting curve);
reported, not tuned. `engine/core-energy-balance-context-notes.md`.

## Contract — `core_entropy_production`

**Returns** — `entropy_production` [W/K] · `entropy_production_min` [W/K] · `entropy_production_max` [W/K] ·
`entropy_production_h0` [W/K] · `e_r` [W/K] · `e_s` [W/K] · `e_l` [W/K] · `e_g` [W/K] · `e_h` [W/K] · `e_k` [W/K] ·
`entropy_positive_present` [—] · `entropy_band_straddles_zero` [—] · `entropy_corners_positive` [—] ·
`has_inner_core_solved` [—] · `entropy_history_verdict` [—] · `entropy_integration_width` [W/K]
**Needs** — `mass_earth` [M_earth] · `core_mass_fraction` [—] · `core_radius` [R_earth] · `cmb_pressure` [GPa] ·
`core_cmb_temperature_solved` [K] · `core_material` [—] · `body_class` [—] · `k_core_w_m_k` [W/(m K)] · `core_h_w_per_kg` [W/kg] ·
`dtc_dt_k_per_gyr` [K/Gyr]
**Discriminating keys** — `body_class`: rocky bodies only. No solved core-side temperature (C14 refused) → refused by
name. `entropy_history_verdict` is **always** `cannot-say (needs C20)`.
**Grade** — **analog**: the same Earth-calibrated model as C14, with the same declared bands (k 50 ± 20, H 0–1.5 pW/kg,
dT_c/dt 33–126 K/Gyr) and the same γ; E_H's bracket order recovered by closure on the printed −134 MW/K (the text
layer does not resolve it), E_s's 1/T_c prefactor confirmed by closure on the printed 64 — both *found by working
back, not by reading*.

`entropy_production` is Nimmo+ 2004 eq. 43 at the present epoch, **ΔE = E_R + E_s + E_L + E_H + E_g − E_k**, on the
route-B core profile at C14's solved T_c: E_R (eq. 16) with I_T = ∫ρ/T dV numeric; E_s = (C_p/T_c)(M_c − I_S/T_c) dT_c/dt
(eq. 10 — I_S kept separately, E_s is not a rescaling of Q_s); E_L (17) and E_g (= Q_g/T_c) from C14's Q_L, Q_g; E_H
(24) with the closure-recovered bracket; E_k = k ∫(∇T/T)² dV (eq. 25 on the profile; eq. 26's closed form belongs to
the analytic core and lives in the test). `_min/_max` are the eight corners of k × H × dT_c/dt; `_h0` is the H = 0
corner, emitted as the honest corner because our H band's floor is 0. **The output is a band, not a verdict**: the
paper itself uses `ΔE > 0` (*"any positive ΔE is assumed sufficient"*) because the required excess is *"probably
∼100 MW K⁻¹, but could lie anywhere within the range 0.1–1000"* (§5.2) — 400 (Roberts+ 2003's 2 TW) and 100 (§6.2)
straddle the paper's own Earth (351) — and `entropy_positive_present` carries that label. **Not wired into
`dynamo_rocky`**: a threshold that cannot decide has no standing to overwrite the ladder; the paper keeps Q_C-vs-Q_k
and φ side by side. **The 3-Gyr statement is refused by name**: two of the paper's three criteria (mean and minimum
ΔE over 3.1 Gyr) are history quantities, ΔE_min is the discriminating one (Table 5), and a present-day φ > 0 does
not imply a sustained dynamo — C20 is this node's consumer for that. Without an inner core (the solved Earth, C14)
E_L = E_g = E_H = 0 and ΔE = E_R + E_s − E_k — the paper's *"completely liquid core"* case, kept positive there by
core potassium (§5.3: no potassium → −45 %). Transcription closure: on the paper's inputs the analytic core (test
file only) reproduces Table 4's six entropy components within 10 % (E_L, E_g, E_H ≈ −6 %, the C_r factor of C14)
and ΔE 328 vs 351. `entropy_integration_width` = |ΔE at 4× the profile steps − ΔE|, emitted live: the profile is
RK4 (0.003 % converged) but the integrals on its samples are first-order sums, O(h), and E_R, E_s are differences of
nearly equal quantities (one digit cancels) — measured ≈ 2.7 MW/K on Earth at 400 steps, two orders below the
declaration band, gated at < 10 MW/K. `engine/core-entropy-context-notes.md`.

## Contract — `core_thermal_history`

**Returns** — `core_cmb_temperature_present` [K] · `mantle_potential_temperature_present` [K] · `dtc_dt_present_k_per_gyr` [K/Gyr] ·
`q_cmb_present` [W] · `q_mantle_present` [W] · `inner_core_radius_present_km` [km] · `inner_core_case` [—] ·
`inner_core_nucleation_gyr_ago` [Gyr] · `delta_e_min_3gyr_lo` [W/K] · `delta_e_min_3gyr_hi` [W/K] · `delta_e_present_lo` [W/K] ·
`delta_e_present_hi` [W/K] · `entropy_history_verdict` [—] · `history_converged` [—] · `history_convergence_width` [—] · `history_steps` [—]
**Needs** — `mass_earth` [M_earth] · `core_mass_fraction` [—] · `core_radius` [R_earth] · `cmb_pressure` [GPa] · `cmb_temperature` [K] ·
`potential_temperature` [K] · `radius_earth` [R_earth] · `age_gyr` [Gyr] · `core_initial_temperature` [K] ·
`mantle_initial_potential_temperature` [K] · `core_material` [—] · `body_class` [—] · `step_myr` [Myr] · `core_h_w_per_kg` [W/kg]
**Discriminating keys** — `body_class`: rocky bodies only. No interior solution or no initial temperatures → refused by name.
**Grade** — **analog**: Nimmo+ 2004 eqs 30 and 32 integrated forward (RK4, Nimmo's 4 Myr step) on the state (T_c, T_m); the
mantle base temperature by the interior solve's own adiabat ratio (eq. 29's form); long-lived radiogenic heat only (K·Th·U);
the initial temperatures are Nimmo's printed 4 800 K on Earth and declarations elsewhere; the result stands on ≈24
declarations in all and reads "consistent with an Earth-calibrated model". The entropy band is over the four k × H corners —
the declared-rate axis of C15's eight is what this node computes, so the two bands are not comparable. Step convergence
(ΔE_min over 3.1 Gyr at h, h/2, h/4) is the pre-registered test and runs on demand (`test_core_history.py --sweep`).

## Table of Contents

1. [The relation: T_eff⁴ = T_eq⁴ + T_int⁴](#1-the-relation-t_eff--t_eq--t_int)
2. [The cooling track: L_int(M, age) behaviour](#2-the-cooling-track-l_intm-age-behaviour)
3. [The hot-start vs cold-start initial-entropy question](#3-the-hot-start-vs-cold-start-initial-entropy-question)
4. [Calibration: the relation reproduces Neptune (and the Uranus anomaly)](#4-calibration-the-relation-reproduces-neptune-and-the-uranus-anomaly)
5. [Domain of validity: internal heat by body class](#5-domain-of-validity-internal-heat-by-body-class)
6. [Helium rain and deuterium burning: the extra terms](#6-helium-rain-and-deuterium-burning-the-extra-terms)
7. [Worked examples](#7-worked-examples)
8. [Honesty & uncertainty](#8-honesty--uncertainty)
9. [Annotated Bibliography](#9-annotated-bibliography)
10. [Related](#related)

---

## 1. The relation: T_eff⁴ = T_eq⁴ + T_int⁴

A body radiates from its surface the sum of two power sources: the sunlight it absorbs
and re-emits (equilibrium term) and the heat leaking out of its interior (internal term).
Because both are Stefan–Boltzmann emitters from the same surface, the **fluxes add** and
the temperatures add **in the fourth power**:

    σ T_eff⁴  =  σ T_eq⁴  +  σ T_int⁴
    ⇒  T_eff⁴  =  T_eq⁴  +  T_int⁴

where

    T_int  =  ( L_int / (4 π R² σ) )^(1/4)

is the effective temperature the body would have from its **internal luminosity alone**
(`L_int` = the internal heat output, `R` = radius, `σ` = Stefan–Boltzmann constant), and
`T_eq` is the irradiation equilibrium temperature from the
[tidally-locked-temperature doc](tidally-locked-temperature-methodology.md):
`T_eq = T_★ √(R_★/2a) (1−A)^(1/4)` for the full-redistribution case.

The fourth-power addition makes the regime behaviour clean, **the larger term wins, hard**:

- **Irradiation-dominated** (`T_eq ≫ T_int`, close-in or low-`L_int`): `T_eff ≈ T_eq`.
  Internal heat is a negligible bump. Most temperate and hot planets sit here.
- **Internal-heat-dominated** (`T_int ≫ T_eq`, young giant): `T_eff ≈ T_int`. The body is
  **self-luminous**: it shines by its own thermal light regardless of the star, which is
  exactly how directly imaged young giants are detected (§3, Marois+ 2008).
- **Comparable** (`T_int ~ T_eq`, cold far-out body): both matter, and a *modest* `L_int`
  can lift `T_eff` noticeably above `T_eq` because `T_eq` is itself tiny. This is the
  **Neptune case** (§4) and the **Proxima c** case (§7).

The reason a small internal flux can dominate far from the star: `T_eq` falls as
`a^(−1/2)` while `T_int` is set by the body's own cooling and is *insolation-independent*.
Far enough out, the fixed `T_int` floor exceeds the vanishing `T_eq`.

> **Energy-balance equivalent.** Observers usually quote the **internal flux ratio**: how
> much power the body emits in excess of what it absorbs. If `f = L_int / L_absorbed`,
> then `T_eff⁴ = T_eq⁴ (1 + f)`. Neptune has `f ≈ 1.6` (it emits ~2.6× what it absorbs,
> §4); a self-luminous young giant has `f ≫ 1`; A b has `f ≲ 0.06` (§7).

---

## 2. The cooling track: L_int(M, age) behaviour

For a giant or brown dwarf with no fusion (or only transient deuterium burning), `L_int`
is **residual heat-of-formation + Kelvin–Helmholtz contraction**: the body slowly shrinks,
converts gravitational potential energy into heat, and radiates it away. This is the
**same internal cooling luminosity** the [dynamo doc](planetary-dynamo-scaling.md) uses to
set the magnetic field: one luminosity, two consequences (thermal emission here, dynamo
field there). The canonical tracks come from the Burrows, Baraffe/Chabrier, Fortney/Marley
and Saumon/Marley evolutionary-model grids (§9).

The two robust qualitative scalings off those tracks:

- **Young = bright; declines monotonically with age.** A giant is hottest and most
  luminous right after formation and cools forever after. Order of magnitude from the
  Burrows 1997 / Baraffe 2003 tracks: a ~1 M_J planet has `T_int` of order ~1000+ K at a
  few Myr, falling toward ~100 K by a few Gyr, and below ~100 K at 10 Gyr. The decline is
  steep early, then slow, roughly `L_int ∝ age^(−1.3)` over Gyr timescales (the same
  power that gives the dynamo doc its `age^(−0.33)` *field* exponent, since `B ∝ L^(1/6)`).
- **More massive = brighter and stays hot longer.** A larger gravitational reservoir and
  slower contraction keep `L_int` (and `T_int`) elevated for longer. A 10 M_J object is
  self-luminous for ~Gyr; a Saturn-mass object cools below detectability in ≲100 Myr.

The practical consequence for NearStars: **an old, low-mass giant has a faint cooling
luminosity and is irradiation-dominated** (A b, §7), whereas a **young giant of any
mass is self-luminous** (the directly imaged regime, §3). Age and mass, not the host
star, decide which regime a giant is in.

We do **not** re-derive `L_int(M, age)` from scratch here; like the dynamo doc, the honest
posture is to read it off the published tracks (Baraffe 2003 / Saumon & Marley 2008 /
Sonora Bobcat for the substellar end, Fortney 2007 for the planetary radii+luminosity)
or, for solar-system ice giants, anchor on the *measured* internal flux (§4).

---

## 3. The hot-start vs cold-start initial-entropy question

For a **young** giant (≲ few hundred Myr), `L_int` depends sharply on the **initial
entropy** the planet was born with, i.e. on its formation pathway, and this is the
single largest uncertainty at young ages:

- **Hot start**: the planet retains the high entropy of a gravitationally collapsing gas
  parcel (disk-instability-like). It begins *bright* and bright stays for ~100 Myr.
- **Cold start**: core-accretion through an accretion shock (Pollack+ 1996) radiates away
  much of the entropy, so the planet begins *much fainter* and only converges to the
  hot-start track after ~10²–10³ Myr.

Marley+ 2007 ("On the Luminosity of Young Jupiters") showed the two scenarios differ by up
to ~2 dex in `L_int` (and several hundred K in `T_int`) at ages ≲ 100 Myr. Spiegel &
Burrows 2012 mapped the spectral/photometric diagnostics that distinguish them. The tracks
**converge** once the body is older than ~1 Gyr, so the ambiguity matters *only* for young,
directly imaged giants. It is irrelevant for the Gyr-old NearStars hosts.

**NearStars rule:** for a young (≲ few hundred Myr) self-luminous giant, report `L_int` as
a **range bracketed by hot- and cold-start tracks**, not a point. For a Gyr-old body
(every confirmed NearStars host giant), the start ambiguity has washed out: use the cooled
track directly.

---

## 4. Calibration: the relation reproduces Neptune (and the Uranus anomaly)

The relation is trustworthy because the solar-system giants have *measured* energy
balances (emitted IR vs absorbed sunlight) from Voyager IRIS: the internal flux is
directly observed, not assumed.

| Body | T_eq (K) | T_eff measured (K) | emitted / absorbed | source |
|---|---|---|---|---|
| **Jupiter** | ~110 | ~124 | ~1.67 | Hanel+ 1981 |
| **Saturn** | ~81 | ~95 | ~1.78 | Hanel+ 1983 |
| **Neptune** | **~47** | **~59** | **~2.6** | Pearl & Conrath 1991 |
| **Uranus** | ~58 | ~59 | ~1.06 (≈ 1, anomalous) | Pearl+ 1990 |

**Neptune is the canonical "internal heat lifts T_eff above T_eq" case.** Pearl & Conrath
1991 (Voyager 2 IRIS) measured an effective temperature `T_eff ≈ 59.3 K` against an
equilibrium temperature `T_eq ≈ 46.6 K`: Neptune **emits ~2.6× the sunlight it absorbs**.
Plug into §1: `T_int = (T_eff⁴ − T_eq⁴)^(1/4) = (59.3⁴ − 46.6⁴)^(1/4) ≈ 52 K`, i.e. the
internal heat alone would warm Neptune to ~52 K, *comparable to* the ~47 K the Sun
delivers at 30 AU. The internal term dominates the temperature budget despite Neptune being
"only" a cooling ice giant, precisely because the insolation is so feeble that far out.

**The Uranus contrast (read this).** Uranus, Neptune's near-twin in mass and radius,
emits essentially **as much as it absorbs** (Pearl+ 1990: ratio ≈ 1.06, internal flux
consistent with zero within error). Its `T_eff ≈ T_eq`. The two otherwise-similar bodies
differ by ~2.5× in internal flux. The leading explanations (a more layered/stably
stratified interior trapping heat; a giant-impact history) are unsettled: Uranus is a
standing warning that **internal flux is not a clean function of (M, R, age)**; two twins
can differ by a large factor. For NearStars this caps our confidence: an ice-giant `L_int`
prediction is good to a factor of a few, not better.

---

## 5. Domain of validity: internal heat by body class

The body class decides which mechanism dominates and how confident the estimate is:

1. **Rocky planets: radiogenic + secular cooling dominate, but the payoff is the interior,
   not `T_eff`.** The internal flux is set by long-lived radioisotope decay (U, Th, ⁴⁰K) plus
   residual accretional/secular heat, *not* by Kelvin–Helmholtz contraction (rock barely
   contracts). The scale is the **Earth heat flux ~0.08–0.09 W/m²** (global ~46–47 TW:
   Sclater, Jaupart & Galson 1980; Davies 2013). The radiogenic share depends on the denominator:
   Korenaga 2008 ([`2008RvGeo..46.2007K`](https://ui.adsabs.harvard.edu/abs/2008RvGeo..46.2007K), cached) gives a **bulk-Earth Urey ratio ≈ 0.35**
   (radiogenic over total surface flux) and a **convective Urey ratio 0.23 ± 0.15** (radiogenic over the
   convecting mantle's budget — §3.1: *"subtracting the continental heat production of 7.5 ± 2.5 TW from
   the BSE heat production of 16 ± 3 TW gives 8.5 ± 5.5 TW for the convecting mantle"*); the convective
   one is what a geotherm consumer needs. This
   corresponds to `T_int ≈ (0.087/σ)^(1/4) ≈ 35 K`: utterly negligible against any
   temperate/warm `T_eq`, so for almost all rocky planets `T_eff ≈ T_eq` and the §1 surface-
   temperature relation simply does not care about a rocky body's internal heat.
   **That is exactly why the rocky regime is different from the giant/ice-giant ones above:
   the internal heat's relevance is not the effective temperature at all: it is the
   *interior thermal budget*.** The same radiogenic + secular luminosity sets the **geotherm**,
   and the geotherm is what drives the consequences NearStars actually art-directs for a
   rocky world:
   - **core convection → a dynamo magnetic field.** Whether the core stays hot and convecting
     long enough to sustain a dynamo is a thermal-history question (Driscoll & Bercovici 2014
     trace Earth's *surviving* geodynamo vs Venus's *failed* one to exactly this divergence in
     melting/radioactivity/conductivity). This is the **rocky regime of
     [`planetary-dynamo-scaling.md`](planetary-dynamo-scaling.md)** (the RM22 rocky scaling,
     `2203.01065`), the giant `B ∝ L^(1/6)` law does **not** apply to rock.
   - **mantle convection → volcanism → outgassing.** The interior heat budget governs whether
     the body is volcanically active, which sets the **outgassing supply** that feeds
     **Gate 3** of [`exoplanet-atmosphere-methodology.md`](exoplanet-atmosphere-methodology.md)
     (a dead, cold interior cannot resupply a secondary atmosphere).

   So for a rocky body, carry the internal heat as an *interior* quantity (geotherm →
   volcanism / outgassing / dynamo), not as a bump on `T_eff`. The §1 relation only ever
   competes for an extremely cold (far-out, dim-star) rocky body, and even then weakly.
   **Tidal heat**, by contrast, can swamp radiogenic heat for close-in eccentric bodies and
   then dominates the *same* interior budget: that is the
   [tidal-heating doc's](tidal-heating-methodology.md) territory (for an Earth-mass body
   radiogenic ≈ 0.08 W/m²; tidal heating takes over only when it exceeds that).
2. **Ice giants / mini-Neptunes: modest, but it MATTERS when the body is cold.** A residual
   cooling luminosity of the Neptune scale gives `T_int ~ 40–55 K`. Negligible against a
   warm `T_eq`, but **decisive** when `T_eq` is itself tens of K (far-out or M-dwarf
   temperate orbit), where it lifts `T_eff` well above `T_eq` (Neptune §4; Proxima c §7).
   Confidence is a **factor of a few** (the Uranus anomaly, §4).
3. **Giant planets (0.3 ≲ M ≲ 13 M_J): Kelvin–Helmholtz cooling tracks (§2).** Read
   `L_int(M, age)` off the Burrows/Baraffe/Fortney/Saumon-Marley grids. Old + low-mass →
   faint → irradiation-dominated (A b §7); young → self-luminous (§3).
4. **Brown dwarfs (13–70 M_J): cooling tracks + a transient deuterium-burning plateau
   (§6).** Self-luminous for Gyr; the Sonora and Saumon & Marley grids cover this regime.
   `L_int` here is large enough that `T_eq` from a wide companion orbit is usually
   irrelevant.
5. **Young vs old is the master switch.** Within classes 3–4, a young body is self-luminous
   and an old one approaches equilibrium. For young (≲ few hundred Myr) bodies the
   hot/cold-start ambiguity (§3) widens `L_int` by up to ~2 dex; for Gyr-old bodies it is
   resolved.

---

## 6. Helium rain and deuterium burning: the extra terms

Two additional internal-heat sources matter at the ends of the mass range:

- **Helium rain / phase separation (Saturn-type).** At Saturn's interior pressure and
  temperature, helium becomes immiscible in metallic hydrogen and rains downward; the
  release of gravitational energy by this differentiation is an **extra luminosity term on
  top of plain Kelvin–Helmholtz cooling**. Stevenson & Salpeter 1977 laid out the H–He
  phase diagram and the mechanism; Mankovich & Fortney 2020 showed it is *active in Saturn
  and largely not yet in Jupiter*, explaining why Saturn's measured internal flux is
  surprisingly high for its mass (it is "extra-luminous" relative to a pure-cooling model,
  Hanel+ 1983, §4). For NearStars: a Saturn-class giant's internal flux can exceed the
  naive cooling-track value: flag this when a worked body is Saturn-like in mass and age.
- **Deuterium burning (the brown-dwarf boundary, ~13 M_J).** Above ~13 M_J a body briefly
  fuses primordial deuterium, adding a **temporary luminosity plateau** that delays cooling.
  Spiegel, Burrows & Milsom 2011 pinned the deuterium-burning mass limit (and showed it
  depends on metallicity/helium fraction, spanning ~11–14 M_J): this is the conventional
  planet/brown-dwarf dividing line. A body just above it (e.g. a ~13–14 M_J companion) stays
  self-luminous longer than a pure planet of the same age. Below ~13 M_J there is no
  deuterium burning and the body is on the pure-cooling track.

Neither term changes the §1 relation: they only modify `L_int`, hence `T_int`.

---

## 7. Worked examples

**Neptune (the calibration).** `T_eq ≈ 47 K`, measured `T_eff ≈ 59 K`, emitted/absorbed
≈ 2.6 (Pearl & Conrath 1991). Internal-only `T_int = (59⁴ − 47⁴)^(1/4) ≈ 52 K`, comparable
to the insolation, so `T_eff` sits well above `T_eq`. **Derived** (internal flux measured).
Contrast Uranus: same class, `T_eff ≈ T_eq`, internal flux ≈ 0, the cautionary twin (§4).

**A young self-luminous giant (the directly imaged regime).** A few-M_J planet at ≲ 100 Myr
has `L_int` so large (`T_int` of several hundred to ~1000 K) that it **shines by its own
heat irrespective of the star**: this is how the HR 8799 planets were *directly imaged*
(Marois+ 2008): their detected light *is* the cooling-track luminosity (§2), and at that
age it carries the hot/cold-start ambiguity (§3).
*NearStars ε Ind A b*: a ~7.6 M_J giant at **age ≈ 3.5 Gyr** (the dynamo-doc anchor). At
several Gyr it is **well past the self-luminous phase**: the cooling track has dropped its
`T_int` to of order ~150–250 K (massive, so still warm-ish, but no longer hundreds-of-K
bright). Because it orbits ε Ind A on a wide, cold orbit, `T_eq` is low and the *internal*
heat is the larger term: its `T_eff` is set mostly by residual cooling, but it is **not**
self-luminous in the imaging sense (it would be detectable in thermal IR, but it is a cooled
old giant, not a young hot one). Report `T_int` from the Gyr-old track, no start ambiguity.

**A b = α Cen A b (old + low-mass = faint).** An **old (~5 Gyr), ~0.38 M_J
(Saturn-class)** temperate giant. Both knobs point to a *faint* cooling luminosity: low mass
(small reservoir, fast cooling) **and** old age (long since cooled). The Phase-4 board used
`T_int < 110 K` with internal flux **≲ 6 % of insolation**, i.e. `f ≲ 0.06`, so by §1
`T_eff ≈ T_eq (1+0.06)^(1/4) ≈ 1.015 T_eq`, a ~1.5 % bump. **Irradiation-dominated, not
self-luminous.** This is the textbook "old low-mass giant" case and the reason the board
treated its temperature as essentially `T_eq`: the cooling track simply has nothing left to
deliver at 5 Gyr and 0.38 M_J. (Saturn-class → watch for a small helium-rain boost, §6, but
it stays well inside the ≲6 % budget.)

**Proxima c (cold mini-Neptune: the new case).** A cold (`T_eq ≈ 40 K`) old ~8 M⊕
super-Earth/mini-Neptune on a wide orbit around Proxima. Insolation is almost zero, so even
a **modest Neptune-analog internal flux** is decisive: taking a Neptune-like `T_int ~ 45–50
K`, §1 gives `T_eff = (40⁴ + 48⁴)^(1/4) ≈ 53 K`: the internal heat **lifts the effective
atmospheric temperature from ~40 K to perhaps ~50–60 K** (a Neptune analog). This is still
cold enough to freeze CH₄ (~91 K sublimation regime) and N₂, so the qualitative outcome
(an icy, volatile-frozen world) is unchanged, but the internal term is *not* ignorable at
these temperatures and should be carried. Frame as a **range** (factor-of-a-few `L_int`
uncertainty, §4 Uranus caveat), not a point.

**Earth (the rocky calibration: the heat goes into the interior, not `T_eff`).** Earth's
global heat loss is **~46–47 TW** (Davies 2013; Sclater+ 1980), a mean surface flux of
**~0.087 W/m²**. How much of it is radiogenic (U/Th/⁴⁰K decay) versus secular (residual accretional +
core/mantle cooling) depends on which budget is the denominator (Korenaga 2008): **bulk Earth ≈ 0.35**, and
for the **convecting mantle 0.23 ± 0.15** — *"only 20% of convective heat flux seems to originate from
radiogenic elements at present, so the rest should be supported by secular cooling"*. Korenaga's argument is
that the convective ratio is *lower* than conventionally assumed, so a range and a dissent are the honest
content: Nimmo & Primack 2020's *"about 15 TW is sourced within the mantle"* sits at the very top of
Korenaga's 8.5 ± 5.5 TW — a disagreement to carry, not reconcile. (Korenaga anchors the total on 44 TW,
Pollack 1993, revised to 46 TW by Jaupart 2007, the increase entirely continental — compatible with the
46–47 TW above. His 20 ± 3 TW BSE figure is McDonough & Sun 1995's, cited to contrast; do not pick it up.)
Plug the flux into §1:
`T_int = (0.087/σ)^(1/4) ≈ 35 K`: against Earth's `T_eq ≈ 255 K` this is a
`(255⁴ + 35⁴)^(1/4) − 255 ≈ 0.001 K` correction, i.e. **completely negligible for the
surface temperature**. Yet the *same* ~47 TW is exactly what keeps the mantle convecting
(plate tectonics) and the core convecting (the **geodynamo** that gives Earth its magnetic
field). Driscoll & Bercovici 2014 show the contrast cleanly: Venus, an Earth twin in mass
and radius, took a different thermal-history path (no plate-tectonic heat-pipe, sluggish
core cooling) and has **no dynamo today**: same `T_int`-irrelevance, opposite *interior*
outcome. **The rocky lesson: report the budget (~0.08–0.09 W/m², ~half/half) and its
interior consequences (volcanism, outgassing, dynamo), not a `T_eff` bump.** **Derived /
calibration** (measured budget).

**A NearStars rocky body (Proxima b / Proxima d: radiogenic and secular in comparable measure, the question is
volcanism & dynamo).** For a temperate-to-warm rocky planet around an M dwarf, internal heat
is radiogenic and secular in comparable measure at the **Earth scale (~0.08 W/m² total, `T_int ~ 35 K`)** and therefore
**irrelevant to the surface temperature**: `T_eff ≈ T_eq` (these worlds live entirely in
the irradiation-dominated regime of §1). What the internal heat *does* decide is whether the
body is geologically alive: enough interior heat → mantle convection → **volcanic outgassing**
(Gate 3 supply of a secondary atmosphere) and a possible **core dynamo** (the RM22 rocky
field regime of the dynamo doc). Carry it as an **interior** quantity, defaulting to the
Earth budget unless mass/age argue otherwise: a more massive super-Earth has a larger
radiogenic inventory and stays hot longer, an old low-mass rock cools sooner. **Caveat for
close-in tidally-locked cases:** for the innermost M-dwarf rocky planets, **tidal dissipation
can exceed radiogenic heat** and then *it* sets the geotherm (the volcanism/dynamo driver):
hand that case to the [tidal-heating doc](tidal-heating-methodology.md). Either way the
surface temperature stays `≈ T_eq`; the internal heat's job is the interior.

---

## 8. Honesty & uncertainty

In the spirit of the dynamo and tidal docs' caveats:

- **Cooling tracks depend on initial entropy, composition and age.** For young (≲ few
  hundred Myr) giants the **hot/cold-start ambiguity** (§3) spans up to ~2 dex in `L_int`;
  quote a range. For Gyr-old bodies it is resolved, but old, low-mass bodies are then
  *intrinsically faint and hard to constrain* (small signal), so the absolute `L_int` is
  poorly pinned even when the regime ("irradiation-dominated") is certain.
- **The Uranus anomaly caps ice-giant confidence at a factor of a few.** Two near-twin ice
  giants differ by ~2.5× in internal flux (§4): `L_int` is not a clean function of
  (M, R, age). Treat any predicted ice-giant `T_int` as order-of-magnitude-plus, and carry
  it as a range.
- **Composition matters.** Helium rain (Saturn-type, §6) and metallicity (deuterium-burning
  limit, §6) move `L_int` by tens of percent to factors; a heavy-element-enriched interior
  cools differently from a solar-composition one. We do not curate these per-body unless a
  measurement exists: default to the solar-composition track and flag the omission.
- **The regime call is robust even when the number is not.** The §1 fourth-power addition
  means the *qualitative* verdict, "self-luminous", "irradiation-dominated", or
  "internal heat lifts a cold body", usually falls out cleanly from (mass, age, `T_eq`)
  long before the precise `L_int` matters. That regime call is what NearStars actually needs
  for art-direction; the exact `T_int` is a range, and where art overrides it (a deliberately
  glowing old giant, say) it is a **documented divergence**, never a silent upgrade.

The relation is grounded and calibrated (it reproduces Neptune's `T_eff` from its measured
internal flux, and the Uranus null); the *inputs* (`L_int` via cooling track or measured
energy balance, the start scenario, composition) carry the uncertainty. Confidence is
**factor-of-a-few on `T_int`, but high on the regime classification.**

---

## 9. Annotated Bibliography

Each entry: authors, year, journal, **verified** arXiv id (or "no arXiv" + bibcode),
ADS citation count, and one line on the contribution.

- **Stevenson, D. J. & Salpeter, E. E. (1977)**: *ApJS* 35, 239 (dynamics) & 35, 221
  (phase diagram). **No arXiv** ([`1977ApJS...35..239S`](https://ui.adsabs.harvard.edu/abs/1977ApJS...35..239S), [`1977ApJS...35..221S`](https://ui.adsabs.harvard.edu/abs/1977ApJS...35..221S)). Cites: 234 /
  225. Founding H–He phase-separation ("helium rain") theory: the giant-planet
  differentiation luminosity term. §6.
- **Hanel, R. et al. (1981)**: *JGR* 86, 8705. **No arXiv** ([`1981JGR....86.8705H`](https://ui.adsabs.harvard.edu/abs/1981JGR....86.8705H)).
  Cites: 133. Voyager IRIS albedo, internal heat and energy balance of **Jupiter** (emitted
  ≈ 1.67× absorbed). §4.
- **Hanel, R. A. et al. (1983)**: *Icarus* 53, 262. **No arXiv** ([`1983Icar...53..262H`](https://ui.adsabs.harvard.edu/abs/1983Icar...53..262H)).
  Cites: 114. **Saturn** internal heat flux and energy balance (emitted ≈ 1.78× absorbed,
  high for its mass, the helium-rain signature). §4, §6.
- **Pearl, J. C. et al. (1990)**: *Icarus* 84, 12. **No arXiv** ([`1990Icar...84...12P`](https://ui.adsabs.harvard.edu/abs/1990Icar...84...12P)).
  Cites: 135. Albedo, T_eff and energy balance of **Uranus** from Voyager IRIS: the
  anomalously *low* internal flux (ratio ≈ 1.06 ≈ zero), Neptune's twin that doesn't glow.
  §4.
- **Pearl, J. C. & Conrath, B. J. (1991)**: *JGR* 96, 18921. **No arXiv**
  ([`1991JGR....9618921P`](https://ui.adsabs.harvard.edu/abs/1991JGR....9618921P)). Cites: 135. Albedo, T_eff (~59 K) and energy balance of
  **Neptune**: emits ~2.6× absorbed sunlight; the canonical "internal heat > insolation"
  calibration. §1, §4, §7.
- **Pollack, J. B. et al. (1996)**: *Icarus* 124, 62. **No arXiv** ([`1996Icar..124...62P`](https://ui.adsabs.harvard.edu/abs/1996Icar..124...62P)).
  Cites: 2774. Core-accretion formation of the giant planets: the physical origin of the
  *cold-start* low-entropy initial condition. §3.
- **Burrows, A. et al. (1997)**: *ApJ* 491, 856. **arXiv:astro-ph/9705201**
  ([`1997ApJ...491..856B`](https://ui.adsabs.harvard.edu/abs/1997ApJ...491..856B)). Cites: 1300. Nongray theory and evolutionary cooling tracks for
  extrasolar giant planets and brown dwarfs: the foundational `L_int(M, age)` grid. §2.
- **Guillot, T. (1999)**: *Science* 286, 72. **No arXiv** ([`1999Sci...286...72G`](https://ui.adsabs.harvard.edu/abs/1999Sci...286...72G)).
  Cites: 454. "Interiors of Giant Planets Inside and Outside the Solar System": review
  framing internal heat, contraction and energy balance. §2 context.
- **Chabrier, G. & Baraffe, I. (2000)**: *ARA&A* 38, 337. **arXiv:astro-ph/0006383**
  ([`2000ARA&A..38..337C`](https://ui.adsabs.harvard.edu/abs/2000ARA%26A..38..337C)). Cites: 537. Review of the theory of low-mass stars and substellar
  objects: the cooling/contraction physics behind the tracks. §2.
- **Baraffe, I. et al. (2003)**: *A&A* 402, 701. **arXiv:astro-ph/0302293**
  ([`2003A&A...402..701B`](https://ui.adsabs.harvard.edu/abs/2003A%26A...402..701B)). Cites: 1528. COND evolutionary models for cool brown dwarfs and
  EGPs: the most-cited substellar cooling grid; `L_int`/`T_int` vs (M, age). §2, §7.
- **Fortney, J. J., Marley, M. S. & Barnes, J. W. (2007)**: *ApJ* 659, 1661.
  **arXiv:astro-ph/0612671** ([`2007ApJ...659.1661F`](https://ui.adsabs.harvard.edu/abs/2007ApJ...659.1661F)). Cites: 949. Planetary radii across
  five orders of magnitude in mass and insolation, from thermal-evolution models: radius +
  cooling luminosity coupling (internal heat inflates the radius). §2.
- **Marley, M. S. et al. (2007)**: *ApJ* 655, 541. **arXiv:astro-ph/0609739**
  ([`2007ApJ...655..541M`](https://ui.adsabs.harvard.edu/abs/2007ApJ...655..541M)). Cites: 454. "On the Luminosity of Young Jupiters": the
  hot-start vs cold-start initial-entropy dichotomy (~2 dex spread at young ages). §3.
- **Saumon, D. & Marley, M. S. (2008)**: *ApJ* 689, 1327. **[arXiv:0808.2611](https://arxiv.org/abs/0808.2611)**
  ([`2008ApJ...689.1327S`](https://ui.adsabs.harvard.edu/abs/2008ApJ...689.1327S)). Cites: 619. Evolution of L and T dwarfs in color-magnitude
  diagrams: the substellar cooling-track grid for the brown-dwarf regime. §2, §5.
- **Marois, C. et al. (2008)**: *Science* 322, 1348. **[arXiv:0811.2606](https://arxiv.org/abs/0811.2606)**
  ([`2008Sci...322.1348M`](https://ui.adsabs.harvard.edu/abs/2008Sci...322.1348M)). Cites: 1513. Direct imaging of the HR 8799 planets: young giants
  detected by their *own* cooling-track thermal light (the self-luminous regime). §1, §3, §7.
- **Fortney, J. J. & Nettelmann, N. (2010)**: *Space Sci. Rev.* 152, 423.
  **[arXiv:0912.0533](https://arxiv.org/abs/0912.0533)** ([`2010SSRv..152..423F`](https://ui.adsabs.harvard.edu/abs/2010SSRv..152..423F)). Cites: 314. Review of giant-planet interior
  structure, composition and evolution: internal heat, contraction, helium rain in one
  place. §2, §6.
- **Spiegel, D. S., Burrows, A. & Milsom, J. A. (2011)**: *ApJ* 727, 57.
  **[arXiv:1008.5150](https://arxiv.org/abs/1008.5150)** ([`2011ApJ...727...57S`](https://ui.adsabs.harvard.edu/abs/2011ApJ...727...57S)). Cites: 276. The deuterium-burning mass limit
  for brown dwarfs and giant planets (~11–14 M_J, composition-dependent): the planet/BD
  boundary and the transient burning luminosity. §6.
- **Spiegel, D. S. & Burrows, A. (2012)**: *ApJ* 745, 174. **[arXiv:1108.5172](https://arxiv.org/abs/1108.5172)**
  ([`2012ApJ...745..174S`](https://ui.adsabs.harvard.edu/abs/2012ApJ...745..174S)). Cites: 357. Spectral and photometric diagnostics of giant-planet
  formation scenarios: how to tell hot- from cold-start young giants observationally. §3.
- **Marley, M. S. et al. (2021)**: *ApJ* 920, 85. **[arXiv:2107.07434](https://arxiv.org/abs/2107.07434)**
  ([`2021ApJ...920...85M`](https://ui.adsabs.harvard.edu/abs/2021ApJ...920...85M)). Cites: 375. The Sonora Bobcat brown-dwarf atmosphere and
  *evolution* models: the modern substellar cooling-track grid superseding/extending
  Saumon & Marley 2008. §2, §5.
- **Mankovich, C. R. & Fortney, J. J. (2020)**: *ApJ* 889, 51. **[arXiv:1912.01009](https://arxiv.org/abs/1912.01009)**
  ([`2020ApJ...889...51M`](https://ui.adsabs.harvard.edu/abs/2020ApJ...889...51M)). Cites: 69. Helium phase separation gives a Jupiter/Saturn
  dichotomy: quantifies the helium-rain luminosity active in Saturn but not yet Jupiter.
  §6.

**Earth / rocky internal heat (radiogenic + secular):**

- **Sclater, J. G., Jaupart, C. & Galson, D. (1980)**: *Rev. Geophys. Space Phys.* 18, 269.
  **No arXiv** ([`1980RvGSP..18..269S`](https://ui.adsabs.harvard.edu/abs/1980RvGSP..18..269S)). Cites: 861. The classic global terrestrial heat-loss
  budget (oceanic + continental): the ~0.08 W/m² / ~tens-of-TW scale. §5.
- **Davies, J. Huw (2013)**: *G-cubed* 14, 4608. **No arXiv** ([`2013GGG....14.4608D`](https://ui.adsabs.harvard.edu/abs/2013GGG....14.4608D)).
  Cites: 241. Global map of solid-Earth surface heat flow: the modern ~46–47 TW
  (~0.087 W/m² mean) census. §5, §7.
- **Driscoll, P. & Bercovici, D. (2014)**: *Phys. Earth Planet. Inter.* 236, 36.
  **No arXiv** ([`2014PEPI..236...36D`](https://ui.adsabs.harvard.edu/abs/2014PEPI..236...36D), doi 10.1016/j.pepi.2014.08.004). Cites: 108. Thermal
  and magnetic histories of Earth and Venus: ties a rocky body's interior heat budget
  (melting, radioactivity, core conductivity) to whether a **dynamo survives**; the heat →
  geodynamo link and the Earth/Venus divergence behind the §5 rocky regime and §7 Earth
  example. §5, §7.

**Topics with no single canonical paper:** the surface-flux → `T_int ≈ 35 K` rocky-planet
*scale* in §5 is a Stefan–Boltzmann conversion of the Earth heat-flow budget above, not a
separate citable law; the per-body cold-start composition corrections are read off the
grids (Baraffe 2003 / Sonora) rather than from one dedicated paper. The Davies & Davies
(2010) "Earth's surface heat flux" estimate is not cleanly ADS-indexed as a primary
article; the Davies 2013 map ([`2013GGG....14.4608D`](https://ui.adsabs.harvard.edu/abs/2013GGG....14.4608D)) and Sclater+ 1980 are the cited
anchors instead.

---

## Related

- [tidal-heating-methodology](tidal-heating-methodology.md): the **sibling internal-heat source**
  (tidal dissipation). This doc covers the *non-tidal* terms (residual + Kelvin–Helmholtz +
  radiogenic + helium rain + deuterium burning); add the tidal flux into `T_int` when it is
  non-negligible (close-in eccentric bodies). They combine via the same §1 relation.
- [tidally-locked-temperature-methodology](tidally-locked-temperature-methodology.md): the **`T_eq` term** that
  combines with `T_int` here through `T_eff⁴ = T_eq⁴ + T_int⁴`. That doc delivers the
  irradiation side; this doc delivers the internal side.
- [planetary-dynamo-scaling](planetary-dynamo-scaling.md): the gold-standard sibling scaling-law doc,
  and the place that uses the **same cooling luminosity `L_int(M, age)`** to set the
  magnetic field (`B ∝ L^(1/6)`). One luminosity, two consequences: thermal emission here,
  dynamo field there, a young giant is both brighter *and* more magnetic for the same
  reason.
- [mass-radius-relation-methodology](mass-radius-relation-methodology.md): internal heat **inflates the
  radius**: a young/hot giant is physically larger (Fortney+ 2007 couples `L_int` and `R`),
  so the radius used in `T_int = (L_int/4πR²σ)^(1/4)` is itself age-dependent.
- [methodology-index](methodology-index.md) — the index of all derived-value methodology recipes.
