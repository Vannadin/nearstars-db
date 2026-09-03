<!-- Brief 45(종결)·46 — 선언된 포텐셜 온도가 함의하는 표면 열류를 Nimmo+ 2004 식 34–36 으로 내고 방사성 예산과 대조하는 일관성 검사 -->
# The declared potential temperature, checked against the budget — Briefs 45 and 46 (context notes)

2026-09-03. Verifiers: (병) parallel seat (survey ㉕, read Nimmo+ 2004), (직) directing seat, (여기) work
seat. **§2 is Brief 46's pre-registration and was committed before any code ran.**

Source: `docs/phase3/_papers/2004GeoJI.156..363N.pdf` (+ PROVENANCE) — Nimmo, Price, Brodholt & Gubbins
2004, *The influence of potassium on core and geodynamo evolution*, GJI 156, 363
([ADS](https://ui.adsabs.harvard.edu/abs/2004GeoJI.156..363N)). Line numbers are `pdftotext`
extraction lines; Table 2 was read with `-layout` because the plain extraction interleaves its columns.

## 1. Brief 45 — closed at its pre-registered ending ⑤

Brief 45 asked for the **mantle half** of Nimmo+ 2004's thermal evolution, eqs 32–36, to give T_m(t) —
the potential-temperature anchor `interior_layers` declares by hand — with the core half (37–39 and the
entropy terms) left out because it needs dT_c/dt and the owner's fork. **The split cannot be drawn
there** (⑤, pre-registered; found by the work seat before the pre-registration was written, confirmed at
source by the directing seat):

- eq. 32: `H_m·M_m − Q_M + Q_C = M_m·C_pm·dT_m/dt` (line 596); `Q_C` is *"the heat extracted from the
  core by the mantle"*, `Q_C = 4πR²F_b` (lines 572–574);
- `F_b = k_b (T_c − T_m)/δ_b`, `δ_b = [Ra_c κ_b η_b(T_a)/(ρ_m g α_m (T_c − T_m))]^(1/3)`,
  `η_b(T_a) = f η₀ exp[−ζ(T_a − T₁)]` (eqs 37–39, lines 735–746) — **Q_C depends on T_c at every step**;
- and the core balance `Q_R − Q_C = (Q̃_L + Q̃_g + Q̃_s)·dT_c/dt` (lines 557–568) is driven by the same Q_C.

So eqs 32–36 are not closed without T_c(t). Three routes were put to the directing seat: (a) hold T_c as
a declared constant over 4.5 Gyr — rejected, because core cooling is what the paper is about and a
frozen core is a different model sharing equations; (b) full coupling — the core half, out by the
brief's own line; (c) stop. **(c) chosen.**

**Recorded beside it, because the two together are what stops a re-attempt**: present-day T_m is one of
the model's **calibration targets** — *"(3) the present-day mantle temperature, viscosity and heat
flux"* (success criteria, layout lines ~569–572), with densities adopted *"so that the outer core
density profile agrees with PREM"*. Computing Earth's T_m(t) with this machinery, coupled or not,
reproduces a number the model was tuned to produce; for any other body it is an Earth-tuned model
extrapolated. "We now compute the geotherm instead of declaring it" would be an overstatement in any
of (a)–(c).

**Independent cross-check for Brief 44, found on the way (병, 직, 여기).** Table 2 prints
**H_m = 5.3 pW/kg**, present-day, *"obtained from the radiogenic abundances of Sun & McDonough
(1989)"*; Brief 44's Earth budget, 21.32 TW / 4.031×10²⁴ kg = **5.29 pW/kg** (O'Neill 2020 via N&P's
draft table) — **0.2 %**. ⚠ Two **compilations** of Earth's bulk silicate composition agreeing, not two
methods; a shared primitive-meteorite anchor upstream is not excluded (the Queyroux/Prakapenka shape).
And `H_m` is per kg of **whole silicate**: against the 70 % mantle share it is off by 43 %, against the
total by 0.2 % — use it as a total-silicate rate.

**Corrections to Brief 44's labels from this paper** (병, 직): `ζ = 1.0 ± 0.5 ×10⁻² K⁻¹` and `Ra_c = 600`
**originate here** (Table 2) — N&P dropped ζ's ±0.5; cite both at source, with ζ's own basis deferred by
this paper to Solomatov 1995 / Karato & Wu 1993 (unobtained, now wanted from a fourth direction). The
**100 ppm K in the core** is N&P's choice, **not** this paper's — this paper's fitted value is ≈ 400 ppm
(fitted so four constraints close; three escape routes listed), against 120 and 50 ppm cited from others.

## 2. Brief 46 — the consistency check (pre-registration)

**What is closed and buildable.** Eqs 34–36 are **algebraic in T_m** and use the **top** boundary layer
only (lines 655–693, 여기 read at source):

    δ_t = [Ra_c κ_t η_t(T_m) / (ρ_m g α_m (T_m − T_s))]^(1/3)      (34)
    η_t(T_m) = η₀ · exp[−ζ (T_m − T₀)]                               (35)
    F_t = k_t (T_m − T_s) / δ_t                                       (36)

No time-evolved quantity enters; `f` and `T₁` belong to eq. 39 (bottom layer) and are not needed.
Table 2 (layout read): R_p 6400 km · T₀ 1573 K · ζ 1.0 ± 0.5 ×10⁻² K⁻¹ · η₀ 1.0×10²¹ Pa s · g 9.8 m/s² ·
α_m 2.2 ± 0.3 ×10⁻⁵ K⁻¹ · κ_t 6.0×10⁻⁷ m²/s · ρ_m 4800 kg/m³ · C_pm 1200 J/(kg·K) · T_s 293 K · Ra_c 600.

**④ fires on `k_t` and is resolved by derivation, with the check that licenses it.** *"k_t is the thermal
conductivity at the top of the mantle"* (line 352) has **no printed value**; Table 1's 50 ± 20 W/(m·K) is
the **core's**. `k_t = κ_t·ρ_m·C_pm = 3.456 W/(m·K)` is the definition of thermal diffusivity applied to
Table 2 — **derived by the identity, not printed**, labelled so — and it **closes**: at T_m 1600 K the
chain gives δ_t 58.8 km, F_t 0.0768 W/m², Q_M **39.5 TW**; **inverting for the paper's own present-day
target of ~42 TW gives T_m = 1613.8 K**, Earth's canonical mantle potential temperature (직, 여기
independently). Textbook mantle-rock 3–4 W/(m·K) beside it.

**Sensitivity, with its direction stated.** Forward, at fixed T_m 1600 K: Q_M = **37.8 / 39.5 / 41.4 TW**
across ζ = 0.5 / 1.0 / 1.5 ×10⁻² — about ±4 %. Inverted, for 42 TW: T_m = **1639 / 1614 / 1603 K** across
the same ζ — about ±1 %; because Q_M is steep in T_m (~×1.5 per 100 K), solving for a flux is robust in
T_m. The steepness cuts the other way on the forward number and that is the direction the check uses.

**What is built.** In the `interior_layers` recipe wrapper (not `solve()`), after the interior result:
take the declared `potential_temperature`, evaluate 34–36 with the body's own g and R (from the solved
structure) and Table 2's mantle constants, emit **`mantle_top_boundary_layer`** [km] (δ_t) and
**`implied_surface_heat_flux`** [W/m²] and **`implied_surface_heat_flow`** [W] (F_t · 4πR²) beside the
declared temperature, and compare the implied flow with `internal_heat_nontidal`'s `radiogenic_power`
when that result exists — **a labelled consistency verdict, not a refusal**: the two are not required to
match; **secular cooling is the expected difference** (Earth: 42 TW implied against 21–22 TW radiogenic,
i.e. the paper's own *"Earth loses heat roughly twice as fast as it is being generated"*). Verdict
strings: `consistent-within-secular-gap` (implied/budget between 1 and ~2.5), `declaration-implies-more-
heat-than-secular-cooling-allows` (ratio above that), `declaration-implies-less-than-radiogenic` (ratio
below 1 — a declared T_m colder than the body's own heat production can sustain), `cannot-say (…)` for
missing inputs. The ~2.5 ceiling is the paper's *"roughly twice"* with room; **it is a declaration and
says so.**

**Every value carries `calibrated-at-source`**: a parameterisation tuned on four simultaneous
present-day Earth constraints plus PREM. The verdict reads *"consistent with an Earth-calibrated
parameterisation"*, never *"the body's actual heat flux"*.

**Pre-registered outcomes**: ① some roster body's declared T_m implies a flow far from its budget → the
check earns its place; ② all agree within the secular-cooling gap → tripwire, said so; ③ ζ's ±0.5 swamps
the comparison for some body → cannot grade there, refuse by name; ④ a constant is still missing → name
it rather than deriving a second one; ⑤ declared T_m absent → cannot-say, not a default.

**Expectation (여기, the directing seat declined to register one at 0-for-4)**: Earth → ②, ratio ≈ 39.5 /
21.3 ≈ 1.85, inside the secular gap; Pandora → ⑤ (no potential temperature declared); the giant → out of
domain upstream. ③ does not fire: the ζ band moves the forward flow ±4 %, far less than the gap between
"consistent" and either failure mode. ①: not expected on today's roster — it needs a body with a declared
T_m and a budget, and Earth is the only one.

## 3. Result — 2026-09-03, code `ff90ab6b`

**Branch fired: ② for Earth, ⑤ for Pandora, out of domain for the giant — as the work seat registered.**
① did not fire (only Earth has both a declared temperature and a budget); ③ did not fire (the ζ band
moves the forward flow ±4 %, the verdict's bands are far wider); ④ fired once, on `k_t`, and was resolved
by derivation with the inversion closure (§2), not by a second derivation.

| body | declared T_m | δ_t | F_t | implied Q_M | budget | ratio | verdict |
|---|---|---|---|---|---|---|---|
| Earth | 1600 K | 58.9 km | 0.0771 W/m² | 39.37 TW | 21.32 TW | **1.84** | consistent-within-secular-gap |
| Pandora | — | — | — | — | 13.74 TW | — | cannot-say (no potential temperature declared) |
| α Cen A b | — | | | | (giant, refused upstream) | | |

Earth's 1.84 sits against the paper's own *"roughly twice"* — the recipe reproduces the calibration it was
built from, which is what ② means and no more. The two flag branches are reachable and pinned: 1400 K →
less-than-radiogenic; 1800 K → more-than-secular-cooling-allows.

**Transcription checks** (직, 여기 independently): 1600 K → 58.8 km / 0.0768 W/m² / 39.5 TW with the paper's
R_p and g; 42 TW ← **1613.8 K**; ζ forward 37.8 / 39.5 / 41.4 TW; ζ inverted 1639 / 1614 / 1603 K.

**Where it lives.** In `radiogenic.py`'s recipe rather than `interior_layers`' wrapper: both ends of the loop
are already there (the budget is this recipe's; the temperature is the declaration it reads from the state),
so no ordering inside the coupled core is assumed and `solve()`'s path fingerprint is untouched.

**Gate**: `test_mantle_flux.py` (< 0.1 s) in `check.sh`; `check_contracts` 6/6; `chain.py check` and
`check_via --gate` pass; anchors bit-identical (fingerprint `708ff4627f24c448`). Full `check.sh` result in the
report.
