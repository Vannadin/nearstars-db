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
the model's **calibration targets** — the success criteria at extraction lines 43–53 are *"(1)
successfully reproduce the inferred present-day core and mantle temperature and viscosity structure;
(2) successfully reproduce the present-day heat flux; and (3) generate enough entropy within the core
to allow a geodynamo to function over the last 3 billion years"*, with densities adopted *"so that the
outer core density profile agrees with PREM"*. *(Correction: the first version of this paragraph numbered
the mantle-temperature criterion "(3)"; it is (1), and the substance is unchanged — audit of Brief 46.)* Computing Earth's T_m(t) with this machinery, coupled or not,
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

## 4. Follow-up after audit — 2026-09-03

**① The `k_t` licence is stronger than first stated.** Line 944: *"The values of κ_t and κ_b are based on
Hofmeister's (1999) calculations of the increase in conductivity with depth"* — the authors made κ_t from a
conductivity, so κ_t·ρ_m·C_pm **undoes their step**. That sentence is the primary licence; the inversion is
the check, and the check is now between **two numbers the paper prints**: 42 TW ← 1614 K against the paper's
own *"1330 °C (McKenzie & Bickle 1988)"* = 1603 K (line 1294) — +11 K, 0.7 %. What it does not do: with
d ln Q/dT ≈ 0.0043 K⁻¹ an 11 K agreement constrains k_t to ~5 %, realistically ±10 % given the °C-level
quote — the width of the textbook band. **It confirms the transcription; it does not sharpen k_t.** (The
earlier phrase "Earth's canonical potential temperature" was our declaration's word; the paper's own
number replaces it.) Pinned: |1614 − 1603| < 15 K.

**② The CONSISTENT prose read as a passed test.** It now says *"consistent with an Earth-calibrated
parameterisation; for Earth itself this reproduces the calibration. … Not a passed test of the body."*
The recipe's Earth (declared R⊕, g = GM/R²) gives ratio **1.84**; the paper-Earth chain (R_p 6400 km,
g 9.8) gives 1.85 — two conditions, one number each.

**③ An input was read with no declared arrow — and the via gate cannot see that.** The recipe read
`radius` from `interior_layers` (derived, 1.003 R⊕ — hence 39.37 vs 39.55 TW) while `chain.yaml` declared
no `interior_layers → internal_heat_nontidal` edge and every in-edge carried `via: None`. **Route taken**:
read the **declared** `radius_earth` first (the `mass_or_radius` edge now says `via: [mass, radius]`), fall
back to `interior_layers`' derived radius only when undeclared — and that fallback is now a declared edge
(`interior_layers → internal_heat_nontidal via radius`, requires). Both nodes are inside the 16-node core, so
iteration handles the order either way; `graph.components()` unchanged (16 = `coupled_core`). The larger
finding is in `via-context-notes.md`: `check_via` catches wrong arrows, not missing ones.

**④ The 2.5 ceiling was the wrong kind of declaration.** implied/radiogenic is **1/Urey ratio**; the bound
is now a **Urey floor**, `UREY_FLOOR = 1/3` (ratio ≤ 3), the soft "roughly 2–3" that the paper's *"roughly
twice"* licenses — nothing held grounds a sharper edge, and (audit, from memory, not transcribed) much of the
literature puts Earth's mantle Urey ratio below 0.4, so 2.5 would have flagged a body sitting where a large
part of the field puts Earth. `urey_ratio` is emitted (Earth 0.54). On the paper-Earth chain ratio 2.5 sits
at T_m 1669 K and ratio 1 at 1460 K — a 210 K window whose upper edge is the contested part. **Request list**
(ADS title-checked, not read): Korenaga 2008, *Urey ratio and the structure and evolution of Earth's mantle*
(`2008RvGeo..46.2007K`); Jaupart, Labrosse & Mareschal 2007, *Temperatures, Heat and Energy in the Mantle
of the Earth* (`2007mady.book..253J`).

**⑤ Two sensitivities nobody had stated**, now in the module and on the emitted note: α_m's printed ± 0.3
moves Q_M **±4.5 %** (Q ∝ α^{1/3}); T_s = 293 K is Earth's and declared for every body — it enters as
(T_m − T_s)^{4/3}, so a **200 K surface is +10 %**. Both forward-direction, same size as ζ's.

**⑥** Criterion numbering corrected in §1 (mantle temperature is criterion (1), not (3)).

## 5. Brief 57 — the radiogenic budget inverted to a mantle-temperature *band* (pre-registration)

2026-09-03. **Consumer**: art direction — the owner wants, per body, the likelihood of each tectonic
regime as a percentage, to reference when choosing surface art; an honest wide band beats a confident
point. **This brief stops at the band; no regime classification** (boundaries are ungrounded and get
their own brief). **Nothing in `mantle_flux.py`'s constants moves and ζ is not tuned.**

**What is built.** `invert_for_flow` is already the inverse of eqs 34–36 and is called by nothing in
production (the forward `consistency` is wired at `radiogenic.py:153`). The composition: for the
radiogenic budget alone, the mantle temperature at which the top boundary layer sheds exactly that
power — a **floor** on T_m (secular cooling adds to the flow, never subtracts). Emitted from
`internal_heat_nontidal` as a family, not a point (C11): the union's endpoints plus each named width.

**Four named widths, none folded in** (all from declarations already in the path):
1. **ζ** over the module's declared `ZETA_RANGE` 0.5–1.5 ×10⁻² (Table 2's ± 0.5; Brief 55's printed
   0.005–0.016 differs at the top by 0.001 — the module's declaration is the one used, said on the note).
2. **Concentration set** — Earth (1) chondritic vs Earth (2) non-chondritic, both already emitted.
3. **Denominator** — `mantle_w` (like-for-like: F_t crosses the *top* boundary layer, crustal
   production is above it; Korenaga's convective Urey ratio) against `total_w` (what the forward
   verdict uses). Both carried on the face of the result; the inconsistency is named, not resolved
   (`property-consumer-audit-context-notes.md` §3).
4. **T_s** — 293 K is Earth's, declared for every body; the band is re-evaluated at 200 K to show the
   width (the module documents +10 % on the forward flow).

**Refusal by name below the bracket.** `invert_for_flow` bisects on [1000, 2500] K and returns the
boundary when the root is outside it — a plain float that looks like an answer (directing seat's
Io-scale case: 0.10 TW budget, returned 1000.0 K where Q_M(1000 K) = 0.11 TW already exceeds the
budget). Fixed in this brief: the function returns `None` when Q_M at either bracket end already brackets
the root out, and the recipe emits a named label instead of a temperature. Both ends are checked.

**Pre-measured before this text was written** (여기, `python3` on the landed modules — recorded as
measurement, not prediction): Earth, `mantle_w` × ζ 0.005/0.010/0.016 → 1276 / 1383 / 1441 K;
`total_w` → 1397 / 1462 / 1496 K; Earth (2) at ζ 0.01 → 1235 K (mantle). Widths ζ ~165 K, set ~148 K,
denominator ~80 K — **three of the same order, none dominating**. Union 1060–1496 K. A Mars-mass body
on the low set and an Io-mass body on any set hit the 1000 K floor.

**Pre-registered outcomes:**
- ① the band is narrow enough that regime assignment is mostly determined → say so; percentages are
  near-degenerate. *Not expected: the pre-measurement already shows ~440 K of union width.*
- ② the band spans several plausible regimes → the percentage output is the right shape. *Expected —
  but the statement that matters is "three comparable widths, structural, nothing to tighten by choosing".*
- ③ an Earth-calibrated input does not transport → *already fired in pre-measurement*: the bracket floor
  clamp (fixed here, refusal by name) and T_s = 293 K (carried as width 4). Pandora, tidally heated,
  gets a radiogenic-only floor that is not its mantle temperature — that is what "floor" on the label means.
- ④ anchors: bit-identical by construction (`solve()` untouched; `interior.py` untouched); gate FAIL 0.

### 5.1 Run record — 2026-09-03, code `736c461d`

**Branch fired: ② with ③ riding on it, as pre-measured.** Earth's floor band **1060–1492 K**; Pandora
**1017–1468 K**. Widths as emitted — each is the *largest* spread that declaration carries across the
others, which is wider than the nominal-row spread quoted in the pre-registration (ζ 165 K on the
Earth (1)/mantle row; 263 K on the Earth (2)/mantle row — the low set is where ζ bites hardest):

| body | ζ | set | denominator | T_s 293→200 K | union |
|---|---|---|---|---|---|
| Earth | 263 K | 228 K | 121 K | 47 K | 1060–1492 K |
| Pandora | 283 K | 223 K | 118 K | 45 K | 1017–1468 K |
| Mars-like (0.107 M⊕, cmf 0.24) | 286 K | 209 K | 111 K | 45 K | open below – 1406 K |

**Three widths of one order, none dominating** — the honest statement for a percentage consumer is
that the width is structural, not a gap in our work; T_s is the smallest and is carried by name anyway.

**③, twice.** (a) The bracket clamp: `invert_for_flow` returned 1000.0 K for an Io-scale 0.10 TW
budget where Q_M(1000 K) = 0.11 TW already exceeds it — now `None`, both ends checked, and the recipe
says **"open below"** when only a corner of the family is under the floor (Mars-like on the low set;
Io-like) and **"cannot-say"** when the whole family is (no roster-shaped body reaches it — a 0.001 M⊕
body still has a corner at 1235 K, because the budget scales with M and Q_M(1000 K) with R²; pinned on the
function directly). (b) T_s = 293 K, carried as width 4. Pandora's band is a radiogenic-only floor on a
tidally heated body — not its mantle temperature; the label says so.

**Not classified.** Regime boundaries get their own brief. What `consistency`'s vocabulary already
carries for a classifier: a heat-budget judgement with named refusals (`cannot-say (no potential
temperature)`, `cannot-say (no radiogenic budget)`) and two flags on a declaration — the *shape* a
percentage output wants underneath it, but its inputs are a declared T_m, whereas the band needs none;
a classifier would sit on the band, and reuse the labels' discipline rather than their values.

**Anchors** bit-identical by construction (`interior.py` and `solve()` untouched; `test_ice_giant.py
--fast` 모두 통과). `check_contracts` 7/7 with the seven new outputs; `chain.py check` 47 nodes / 176 edges.
**Width definition, stated after the directing seat reproduced different numbers from the same grid**
(its "hold the other three fixed" maximised over the T_s = 200 K rows too: ζ 293.6 / set 239.1 /
denominator 123.7 K on Earth-shaped inputs g 9.8, r_m 6.4e6, silicate 4.0e24 kg, against the function's
265.3 / 233.7 / 121.1). The function's definition, now in its docstring and on the emitted note: for
ζ / set / denominator, **at T_s = 293 K**, hold the other two fixed, take max − min along the axis, report
the largest such span; for surface, the largest |T(200 K) − T(293 K)| over all (set, denominator, ζ).
Both are legitimate; the phrase "across the others" had not said which others or at which T_s. Widths are
the body's own (g, R, budget) — Pandora's row already differs from Earth's. ζ's upper end is the module's
declared 0.015 (Table 2's ± 0.5); the paper's printed range tops at 0.016, where a reader recomputing from
the paper lands.

Gate on `eb863569`: **FAIL 0, 14:53:38 → 15:14:32 = 1254 s.** The definition commit that follows is
re-gated before push.
