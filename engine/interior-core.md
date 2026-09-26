<!-- 내부구조 솔버를 "끝났다" 고 말하려면 남은 것 — 코어 작업 목록 -->
# Interior solver — the core list

What remains before the interior solver can be called finished. Not a wish list: every
entry here is something **this recipe can close by itself**, and closing all of them is the
definition of done for this tool.

The information was scattered across the methodology document's domain table, six sets of
context notes, and a review file that is now half stale. Asking "what is left" meant
re-reading all three and getting a slightly different answer each time. This is the one
place.

**Order, set by the owner 2026-08-29: C1 first, then down the list in number.** No entry
depends on another, so the numbers are a queue rather than a chain; an entry that closes as
*"recorded, not found"* still closes.

**Notation, fixed by the owner 2026-09-03 (relayed by the directing seat in Brief 64) — applied from here on.**
`C` = the open-question list of `domain: interior`, and this domain has exactly one list: C1–C13 are closed
history and are not touched; a new hole continues the numbering from **C14**. `P` = a *parked* state, marked
with the C it came from, never a new axis. Every brief title carries its C number; a side branch is announced
as "a branch of C<n>" first and returns when done. The three standing watches (γ = 1.5, `Rm > 40` quoted and
never evaluated, the 0.06 multipolar factor as a secondary citation) hang **under C6**, not in a new file —
this file stays the one place. The C14–C19 and P1–P3 rows are at the end of the list.

## Where everything stands — 2026-09-06

This file is 11 993 lines (`wc -l`, 2026-09-17; it read «2 700» until then). The table is here so that "what is open right now" does not require reading
them. **The table navigates; the entries below carry the evidence, and no closed entry is deleted** —
the record is the point of the file.

⚠ **This table was born with a wrong row.** C19 was written here as open with `status: gap` on 2026-09-06,
after both of its branches had closed on 09-04 — and its two branches were described the wrong way round
(the giant branch was already wired and mislabelled; the brown-dwarf branch is the one that was built).
Corrected the same day. The standing rule is that a summary must not show a row closed before the work
lands; this is that rule's mirror, **a summary showing closed work as open**, and it is the more
expensive direction: a stale "closed" gets challenged by the next person who looks, while a stale "open"
sends someone to redo what is already done. A summary row is checked against its own entry when written,
not only when it later drifts.

⚠ **This file now holds two tables keyed by C number** — this one and the C14–C19 detail table below.
A script that edits either must select on cell content, never on the first match; see `engine/tools/README.md`.

⚠ **A title is read by people who read nothing else.** C24's once said *fixed* twenty-five minutes
before the fix existed, and that is recorded in its own entry. Every title here was re-read against
its body on 2026-09-06; where one over-claimed it was rewritten rather than left to be caught again.

| # | what it is | state | next step, if open |
|---|---|---|---|
| C1 | sub-Neptunes, and the defect behind them | closed 2026-08-30 | — |
| C2 | the ocean layer, and multi-axis inversion | closed 2026-08-29 | — |
| C3 | the melting-curve gap, dispatch by class | closed 2026-08-30 | — |
| C4 | ammonia and methane | ammonia half closed and built 2026-08-30; methane half not | see P-row and C22 |
| C5 | where the giants' leftovers belong | closed 2026-08-30 | — |
| **C6** | material ceilings | **standing watch** — never closes | three watches hang here: γ = 1.5, `Rm > 40` quoted and never evaluated, the 0.06 multipolar factor as a secondary citation |
| C7 | partial differentiation | closed 2026-08-30 — the intermediate state is not a mixture | — |
| C8 | the temperature branch's validated window | closed 2026-08-30 | — |
| C9 | porosity on a heated body | closed 2026-08-30 | — |
| C10 | lighter rock | closed 2026-08-30 — the axis exists and does not reach | — |
| C11 | declared differentiation front, never-melted crust | closed 2026-08-30; the pair settled 2026-09-01 | — |
| C12 | a ternary anchor from a diffusion table | closed 2026-08-31, recorded | — |
| C13 | fuzzy core vs the moment-of-inertia deficit | closed 2026-09-01 as a named refusal | — |
| **C14** | `internal_heat_nontidal → dynamo_rocky via geotherm` | **open** (`status: gap`) | needs thermal evolution, not decay history alone; C20's integrator is the supplier to wire ⚠ **Two ⁴⁰K constant sets, recorded 2026-09-24:** `radiogenic.py` now uses Ruedas 2017 (2.8761e-5 W per kg of ⁴⁰K, X_iso 1.1668e-4, mass-weighted); `core_energy.py`'s core heat `H_CORE` keeps Nimmo+ 2004's own (1.917e-5 W/kg, ⁴⁰K/K 1.17e-4). Not reconciled — prereg-radiogenic §7 leaves the core source alone. |
| **C15** | `heat_transport_mode → dynamo_rocky via cmb_heat_flux` | **open** (`status: gap`) | the supplier exists (Brief 60); what is missing is the consumer wiring through φ and core entropy ⚠ **Pre-registered 2026-09-11 as C15 (a)** — and the pre-registration's own finding is that this row is **three** gap edges, not one: φ (value exists, no verdict can be drawn), `cmb_heat_flux` and `geotherm` (value exists, consumer does not read it). The item C15 (a) scopes is only the first — *whether a quantity that cannot decide may enter a gate that must decide.* ⚠ **The sign of ΔE is set by which horn is declared**: 3760 K gives **+27 MW/K** and 3770 K **−78** on the same profile, because the three inner-core terms switch on and off with it — ten kelvin, 105 MW/K. Nothing built |
| **C16** | `tidal_locking → dynamo_rocky via rossby` | **open**, one reason of three retired 2026-09-06 | DO11 read: `q_conv` resolved (super-adiabatic excess per CMB area), **`ν` and the Table 8 4–5× remain** — the paper's own ν is the mantle's, a decoy. The gate is now **reached** on a provisional `locked`; the real value is **C36**, which the owner set as the next item |
| **C17** | `ocean_fraction →` three consumers | **open** (`status: gap`) | three consumers, no supplier; nothing emits an ocean fraction |
| C18 | `body_class → dynamo_rocky via sub_neptune` | closed 2026-09-04 as a named refusal (corrected the same night) | the existence question it spawned is C23 |
| C19 | the giant dynamo's cooling luminosity | closed 2026-09-04 — the `cooling_luminosity` gap edge is gone (no edge into `dynamo_giant` carries `status: gap`, and no edge anywhere uses that `via`) | — leftover is downstream and belongs elsewhere: `magnetosphere_geometry` has no recipe, and `internal_heat_nontidal` for giants still waits |
| C20 | the thermal-history integrator | built 2026-09-04 | — |
| **C21** | the short-lived radiogenic pulse (²⁶Al · ⁶⁰Fe) | **dominance closed · differentiation open, 2026-09-07** | Pulse is **9.59×** the long-lived budget at `t₀ = 0`, decaying with `τ ≈ 1.03 Myr`. ⚠ **An ice-rich body (rock ≲ 35 %) is not melted at all.** `t₀` declared **late** from the formation order — gas-giant moons post-date their planet (Canup & Ward 2002) — so the pulse is **not available** to the five, with the caveat that the scales share an order of magnitude. One path, no branch on body kind: `t₀` is a per-body declaration and the tables serve every body. ⚠ Still open: the differentiation question's melt-fraction threshold, paper defect #23, and no heat-loss term (so small bodies read as an upper bound). Belts are last in order, after C14·C15·C17 |
| **C22** | ammonia fraction in the ice-giant mantle | **blocked** | step 1 waits on a survey; Bethkenhagen+ 2017's grid was never published, so only an author enquiry would open it (owner's call) |
| **C23** | does a sub-Neptune's iron core run a dynamo? | **existence judged 2026-09-06; strength is not available** | see the row below the table |
| C24 | water-rich rocky body does not converge | diagnosed and fixed 2026-09-04 | — |
| **C25** | measured CMB temperature vs published CMB heat flow | **listed, not started** | the two cannot both be met in this model; nobody has chosen which gives |
| **C26** | superionic ice above `ice_x`'s 1 800 K ceiling | **listed, not started** | representation question; no work done |
| **C27** | water fractions 0.05 · 0.15 · 0.20 do not converge | **listed, not started** | a convergence failure, not a physics question — same class as C24, which did close |
| C28 | dynamo ice fraction from the composition preset | built 2026-09-04 | — |
| **C29** | mantle potential temperature | **half open** — the Earth-analog declaration stands | the self-derivation loop is listed and not started |
| C30 | tidal heat into the interior budget | built 2026-09-04 | — |
| C31 | Dante's tidal and dependent board rows | built 2026-09-05 (main) | — |
| **C32** | band output and handoff choices | **structure built 2026-09-05; instances landing one at a time** | built: albedo, stagnant-lid ceiling, greenhouse cases, `k_c`. Open: whoever picks the ten unchosen options that `engine/tools/unchosen_defaults.py` counts |
| C33 | citations resolved against the document | built 2026-09-05 | — |
| **C34** | what the transport table is fed, and where its thresholds come from | ⚠ **held 2026-09-09 behind the third path** — the owner adopted building the missing term (C25 (f)), which changes this table's input, so choosing the feed now would be choosing twice. Re-drawn earlier the same day:**the question is what the table is *declared* to be fed, and the options are the owner's** (earlier status kept: *does not close by choosing — waiting on C47*, 2026-09-07) | The four candidates span 2.203× and are **not verdict-neutral**. On `transport_mode`, unchanged, the low end (tidal + radiogenic, already fed) still reproduces **3 of 4** of the document's anchor labels to the high end's 1. ⚠ On the **C46 ladder cell** it reverses — low **2 of 4**, high **2 of 3 scored plus the Moon 1 of 1 independent** — because naming the gap between the stagnant ceiling and the plate rung took away a free pass Earth's low feed had been collecting. ⚠ **And the four candidates are not four readings of one quantity — they are four quantities, two of them disqualified** (0.0418 is radiogenic production, the wrong quantity; 0.08 has no source in any version of the document and is used there under two labels). Of the two survivors the measured 0.0921 exists for no body in this project, and the computable 0.0769 is a mobile-lid law that C47 (b) shows failing on Mars. **So this is not a choice among candidates any more, and putting one to the owner would be asking them to pick among things that are all disqualified.** Held until C47 closes, which will re-draw the candidate set. Still open with it: Venus fails under both feeds, and the plate ceiling 0.135 remains authored |
| **C35** | `stellar_wind` computes with no document to be a recipe in | **listed 2026-09-06, deliberately not registered** | a stellar-wind methodology document, or a decision that the node does not get one |
| **C36** | `tidal_locking` has no recipe — the locking timescale | **landed 2026-09-06** | eight consumers wait on `locked`, and it is today a placeholder. Landing it is a controlled A/B: the wiring is already frozen and the pre-registered answers are in `regime-gate-context-notes.md` §7 |
| **C37** | `rotation_period` is spelled two ways, and the contract check cannot see it | **closed 2026-09-07** | ⚠ **Two spellings, not three** — `rotation_period_days` is a comment recording a pre-converted DB value, read by nothing. `dynamo_rocky` looked up `rotation_period` while every supplier writes `rotation_period_h`, so it received **None on every body** and recorded that as evidence. Unified across code, contract (en+ko), chain label and the evidence key; no verdict moves, because the value was never in a branch |
| **C38** | `tidal_locking` stands on two tidal models at once | **closed by record 2026-09-06** | `τ_lock` is constant-phase-lag (Goldreich & Soter, per Barnes §2.1); `ω_eq/n` is Hut 1981, which Barnes cites for constant-**time**-lag. They agree only under an assumption neither our document nor our code states, and Hut is held as an unreadable scan |
| **C39** | the same `Q/k₂` is a per-body declaration in one node and a class band in another | **closed 2026-09-06** | Unified: **a declaration wins, the class band is the fallback**, inverted at one named place (`q_over_k2_from_declaration`) and named in the output. No roster verdict moved — Dante and Hades read 1:1 before and after, the a⁶ gate deciding them by nine orders of magnitude. The class band still fails to describe them, which is now C39's finding rather than its blocker |
| **C40** | a fitted value has no seat in the value vocabulary, so it travels as a bare point | **listed 2026-09-06** | C32 gave three words for where a number came from — printed, chosen, engine-filled — and a value solved backwards from a wanted output is none of them. Observed in C39: wiring Dante's declared `k₂/Q` turned `τ` from a band into a point with no width anywhere. Every `tidal_heating` declaration is in the same position |
| **C41** | `eccentricity` has no supplier, and the recipe answered anyway | **provisional landed 2026-09-06** | `orbit_elements` has no recipe, so no body supplies `eccentricity`; the recipe substituted `0.0` and every body came out **1:1 synchronous** on a value nobody set. Owner chose the provisional pattern: `e = 0.10`, in §4's unprinted gap, so the output now declines to classify. ⚠ **One value decides the whole roster** — no body's own data can outvote it. The boards' `eccentricity_forced` is deliberately **not** read: a resonance's maintained value is not the orbit's actual one |
| **C42** | guardrail ⑤ watches an event that never happens on a measured node | **listed 2026-09-06** | `recipe_arrived()` releases a placeholder when its node gains a registered recipe. `chain.yaml` marks `orbit_elements` `kind: measured` — it is supplied, not computed, and **that day never comes**. ⚠ Not one placeholder's problem: the same hole opens under any placeholder on any measured node, and the failure it was built to prevent is a placeholder quietly becoming permanent |
| **C43** | a disc-formation criterion is applied to a moon, on an input that defaults silently | **resolved 2026-09-07** | Owner chose route 2: a satellite does not take the pebble-isolation branch, because neither formation path in the literature uses a distance from the star — giant impact or **circumplanetary** disc. The `semi_major_axis_au` / `_km` question closes with it: a moon consumes no stellar distance, so there is nothing to fill. Satellite mass budget recorded, all five exempt, no value changed |
| **C44** | a field name that misled the engine into doubting its own data | **listed 2026-09-07** | `eccentricity_forced` holds a **measured** orbital eccentricity — Dante's row says an assumed mean was replaced by an `e_rms` from the stability run — but the name reads as a theoretical forcing term. ⚠ Two seats argued from the name alone that it might not be the quantity the despin formula wants, and neither opened the board. C37's class with a documented instance of misleading |
| **C45** | the contract check compares labels, never the keys a recipe looked up | **listed 2026-09-07** | `check_contracts` matches the document's `Needs` against `set(Result.inputs)` — names the author typed — and never reads the string in `state.get(...)`. ⚠ **A recipe can read a key nobody supplies and stay green forever**, as long as it files the resulting `None` under a name the contract knows. C37 is one instance; the hole is in the checker and applies to every recipe |
| **C46** | the transport table is missing rows **and** discriminates on a different axis | **ladder built 2026-09-07, then corrected the same day; rows still absent** | The flux fixes **one** cell: **floors** at 0.09 (Earth) and 2.5 W/m² (Io), and below them a stagnant cell bounded by a **ceiling** — Venus 10–20, Mars 15–30, union 10–30 transferred to anything else — with a `plutonic-squishy lid` cell for exceeding it. The band travels beside the cell. ⚠ **The first build of this ladder stood that ceiling up as a floor at 0.010** and put every cold body one cell too high; our own §6.2 table already said `ceiling`, and one bullet under it did not — C46 (c). ⚠ Three cells, three provenances: `analogy-rung` (Io), held body text (Earth), `abstract-level` (the ceiling, body not held). ⚠ Venus's 78 is **3.9× its own ceiling**, so the ladder now contradicts our anchor column and agrees with the paper it cites; the Moon stays **independent 1/1** only because the stagnant cell was given no floor. Not added to self-scored 3/4 |
| **C47** | the transport table is fed radiogenic production, and its thresholds are defined on surface heat flow | **closed 2026-09-08 — named, not filled (C47 (k))**; earlier status kept: *measured 2026-09-07, not fixed* | Verdict: **a different quantity**, not an inaccurate one. The low feed reproduces radiogenic production on two bodies (Earth 1.07–1.33× of Korenaga 2008's 16–20 TW; Mars 1.11× of Parro+ 2017's 14.3 mW/m²) and misses surface heat flow by **body-dependent** factors (Earth 0.45×, Mars 0.84×). ⚠ **That factor is the Urey ratio** — 0.35 for Earth, 0.68–0.75 for Mars — so `1/Ur` would be 2.2–2.9 against 1.3–1.5 and **no correction constant can serve both.** The missing term is secular cooling, which our own §6 already names (*"radiogenic, accretional, primordial"*) and no node emits. ⚠ Consequence for C34: Mars passing and Earth failing at the low feed measured **how close each body's Urey ratio is to 1**, not whether the feed is right. ⚠ **Attempted 2026-09-07 (C47 (b)) and it does not close by code.** The quantity already exists — C20's `q_mantle_present` **is** `Q_M`, from Nimmo eqs 34–36, and it reads no measured flux — but one law cannot serve both bodies: at a common `T_m` Earth lands on 0.35 while Mars reads **0.209 against 0.68–0.75**, and `Ur` **falls** ×1.69 toward smaller bodies where the literature has it **rise** ×2.0. ⚠ **The ordering is wrong, so no `T_m` fixes it** — `implied_flux` is a mobile-lid law (our own docstring says it was tuned on four present-day Earth constraints) and Mars is the archetypal stagnant lid; it hands Mars 85.7 mW/m² against Reese's own 15–30 ceiling, **2.9–5.7× what C46's own bottom rung allows.** ⚠ Also blocked outright: only `earth.yaml` declares C20's two initial temperatures, so **C20 cannot run on Mars**. **The block is C46's circularity** (the flow needs the regime, the regime needs the flow) plus a paper we do not hold — Reese+ 1998's stagnant-lid scaling, abstract only **Corrected 2026-09-24 (prereg-radiogenic, `12afb7f8`):** the engine's radiogenic production quoted in this item and its sections is now Earth **21.75 TW, 0.04263 W/m²** (was 21.32 / 21.3 TW, 0.0418 — Ruedas 2017 constants and N&P 2020's published Earth set, U 22 → 23) and Mars **12.14 mW/m²** (was 15.87 — Drilleau 2022's 14/54/284), so Mars against Parro+ 2017's 14.3 mW/m² is **0.85×** (the closed table's 1.11×; 1.19× on the 09-23 tree). The same ratios elsewhere in this row, re-derived on 21.75 TW: Earth «1.07–1.33×» of Korenaga's 16–20 TW → **1.09–1.36×**. The old numbers stand where they were written. |
| **C48** | the thermal-history integrator was validated on Earth alone, and calls its flux law far outside that law's expansion point | **closed 2026-09-08 in two halves — domain (Brief 155) and step (Briefs 156–157): the fixed 4 Myr step was h/τ ≈ 75 on Mars's first step and 1.02 on Earth's; the step is now h = min(4 Myr, 0.1·τ) and Mars integrates (1382.90 / 3893.01 / 1669.22 K, within 0.1 K of the 0.25 Myr sweep) while Earth's anchors hold to two decimals (1152 steps, was 1135) — ⚠ **every one of those numbers is at the core heating H = 1.5 pW/kg, which was the nominal when they were measured; owner decision ⑤ (2026-09-09) declared 0.14 and moved them, so Brief 166 D pins each anchor to its condition instead of to the module constant.** Earlier text of this cell:** renamed and half-repaired 2026-09-08 (Brief 155): the inversion bracket had stood in for a domain nobody declared — eqs 34–36's domain is now declared from the paper (upper edge 4800 K, §3; «<8 per cent» caveat, §6; open below), eqs 37–39's for the first time (D5), and the callee keeps both. The Mars step sweep (h/τ) stays open as its own item** | C20 diverges on Mars at every pre-registered `T_pot` (`T_m` → −6244 … −8208 K). ⚠ **The divergence is not the finding** — the flux law is called at **719,546 mW/m² on Mars and 25,144 on Earth**, against measured 19 and 92.1, because Nimmo's eq. 35 is a linearisation about `T₀ = 1573 K` and C20 feeds it **+1467 K (Earth) and +2448 K (Mars)**, giving mantle viscosities of `η₀`÷2.35 M and ÷42.8 G. **Earth's own outputs come from the same out-of-range call and survive only on heat capacity.** ⚠ No published range was violated — **none is printed**; our `BRACKET_K` is a Brief 57 bisection aid. **Two values from one paper fail to compose on a second body**, which is the failure mode of this engine's Earth-number-on-every-body pattern. Blast radius counted: **one consuming edge** (`core_entropy_production`), no board row, no `db/`. Next: a usable flux law, or a grounded starting epoch — ⚠ **never a starting value chosen because it integrates**. ⚠ **The diagnosis above predates Briefs 155 and 157 and is superseded on the cause of the divergence** (kept, not deleted, as this cell's second column keeps its earlier text): the out-of-domain call is real and is still counted on every result, but Mars diverged because of the step — the fixed 4 Myr was h/τ ≈ 75 on the first step — and at h = min(4 Myr, 0.1·τ) Mars integrates |
| **C49** | one engine, two `k_core` declarations — and one file's stated ground forbids the number the other consumes | **listed 2026-09-09, not started** | Rocky: `cmb_flux.py@«K_CORE = 50.0»`, a single declared midpoint ± 20, consumed as the corners (30, 70) by `core_entropy.K_RANGE` and `core_history.K_CORNERS` and as the `q_ad` band. Sub-Neptune: `sub_neptune_dynamo.py@«CORE_CONDUCTIVITY = Band(»`, midpoint **None**, ends **40 and 100** from two papers Tang+ 2025 runs both ways, grade *calibrated*, with an unmade `Choice`. ⚠ **And the comment above it says «70 W/m/K 는 두 논문 중 어느 쪽도 말하지 않은 수다» — that very 70 is the upper corner the rocky path feeds to the entropy band.** So one file's stated ground disqualifies a number the other file uses. Two shapes as well as two values: one paper's ± against two papers' ends. Unification is part of owner decision ② (C25 (b)); listed only |
| **C50** | contracts list `Needs` that no roster body supplies — and four are C37's exact signature | **closed 2026-09-09 at (0, 0, 0) — one row still owner-pending behind the zero** | Measured by C45's new lookup check: **class ① (C37's signature — the lookup misses everywhere and the `None` is filed under that name) is live in 3 nodes / 4 keys** (`body_class` `gas_mass_fraction`·`semi_major_axis_au`, `dynamo_rocky` `dynamo_regime`, `interior_layers` `porosity_cap`), and **class ③ (a `Needs` no body supplies, the call site coping) in 8 nodes / 8 keys** (`core_material` ×4, `ice_mass_fraction` ×3, `differentiated`, `envelope_z`, `gas_mass_fraction`, `initial_porosity`, `tidal_heating`, `permanent_quadrupole`). Each is one of two faults — the contract is wrong, or the body declarations are missing — and which is not decidable from the count. Held at measured size meanwhile: the four are named in `engine/check_contracts.py@«이 집합 밖의 사례는 FAIL 이다»` and anything outside fails the gate; class ③ has a printed baseline. Repair can move values, so it is a later brief. No owner decision |
| **C51** | the engine has no mantle energy budget, so secular cooling is an input nobody supplies rather than an output | **Stage 1 built and gated 2026-09-09 (`0c494b05` · `c214b27f` · `85b1d7d2` · `21322b48`); Stage 2 (time integration) 2026-09-18** | The owner's third path (C25 (f)): build the missing term instead of picking numbers inside the entropy band. ⚠ **The flux law is not what is missing** — Foley 2018's eq. (3) is the Korenaga eq. 30 this engine already transcribed at `n = 1`. What is missing is the budget around it, eqs (1)(2)(4), whose `dT_p/dt` **is** secular cooling. Stage 1 is the present epoch only, with `dT_p/dt` as the unknown, so the gate cost is ~0. Three verdict cells and their failure sentences are fixed in the section below, before any of it exists; `L′` and `(m, p)` go in as bands because the source treats the first as an unknown and prints three disagreeing sets of the second. ⚠ **First anchor measured: one prefactor has five values across two papers (0.528 · 0.53 · 0.55 · 0.57 · 0.5) and Korenaga names the cause — his own definition of `T̄_i`** — which is also the only candidate explanation for the 3.65× absolute-flux gap. Owner decisions on `L′` and `(m, p)` come after commit D's numbers; C34's feed stays held |
| **C52** | how many recorded anchors rest on one shared module constant, and nobody counts | **named and counted 2026-09-09; no checker built** | C45 asks whether a node's lookups are declared, C50 whether a declared `Needs` is supplied; ⚠ **neither asks how many *other* nodes' recorded anchors move when one shared constant moves**, which is what fired twice this week as a gate failure. Instance 1 is `core_energy.H_CORE`, whose value re-defined C20's reproduction anchors from a C14/C15 declaration: six places were repaired in 166 D / 167 A and this item's closing sweep found the real count is **ten**, with three distinct defects left — a comment mirroring `H_CORE_RANGE` that had gone stale at `0.14e-12`, a context note naming 0.14 pW/kg as the declared value after 166 E replaced it with 0.088, and a pre-registration carrying 1525.46 K · 4027–4028 K · 1135 steps with **no condition named at all**. ⚠ **The disease changed shape**: in 166 D the numbers lacked labels, here the labels had gone stale, because the constant moved twice in one day. Instance 2 is `mantle_budget`'s four Earth defaults, where an AST count of 5 and a grep count of 3 were both right about different questions and the number of functions touching them at all is **6**. Closed at named, counted and labelled — **not fixed**: no checker exists, and instance 2 is untouched |
| **C53** | the tectonic regime is declared as a boolean, and no source surveyed uses one | **built 2026-09-09; two owner mappings still pending** | `stagnant_lid: true/false` is the *“bimodal distribution … that is typically assumed”* which **Foley & Bercovici 2014**'s abstract ([`2014GeoJI.199..580F`](https://ui.adsabs.harvard.edu/abs/2014GeoJI.199..580F)) names as its foil, and the parallel seat's P9 survey found **no scheme that is binary** (Mars and Mercury stagnant in all of them, Earth mobile *or* transitional depending on the scheme, Venus genuinely contested across five printed classifications). Registered replacement: a `tectonic_regime` enum {stagnant · mobile · transitional · episodic · heat_pipe · contested} carrying a grade and a source, with the old boolean kept as a **derived** value so that **no consumer moves**. ⚠ **The blast radius was counted before the design and it is one branch**: `dynamo_rocky`'s survival gate is the only place a value reaches an output (truthy → `DEAD_LID`, `dipole_moment` 0), `heat_transport_mode` does **not** read it — it reads the computed flux ladder — and `phase2/`, `phase4/`, `db/` and the SPEC have **zero hits**. Three owner decisions were taken before the build (`contested` → derived `True`; Earth = `mobile` with the grain-damage note; Pandora = `mobile`, owner-declared), and `episodic` · `heat_pipe` are **left unmapped by name** with their candidates recorded — owner-pending. The regression that proves nothing moved is the three roster bodies' derived booleans, bit for bit: Earth `False` · Mars `True` · Pandora `False`. ⚠ The declared-regime-versus-computed-ladder consistency check is **deliberately not built here** — its first report would be that Earth's declaration and Earth's ladder cell already disagree, which is its own item. ⚠ **Built and measured (C53 (b)): every emitted value bit-identical for all three bodies** (Earth `False` · Mars `True` · Pandora `False`, Pandora's 41.37252479971432 µT included), and the ordering rule fired as registered — `check_contracts` failed on the **evidence key** until `Result.inputs` carried `tectonic_regime` instead of the derived boolean. Two corrections to the pre-registration are recorded there: Pandora's old declaration *did* carry a reason, and Mars's `True` is not load-bearing because the core gate fires first |
| **C54** | `conductor_phase` stands in front of the lid axis, and Mars's is `undecided` | **candidate, listed 2026-09-09** | Opened by a measurement in C53 (b), not by a design opinion: the survival gate tests `conductor_phase` **before** the tectonic regime, and Mars's is `undecided`, so Mars answers `cannot-say (conductor_phase undecided)` and its declared `stagnant` never reaches `DEAD_LID`. ⚠ **Mars's dynamo output is identical whether its regime is `stagnant` or `contested`** — so *«Mars is a single-plate planet, therefore no dynamo»* is a sentence this engine does **not** execute, and the lid axis cannot be exercised on any roster body until the axis in front of it decides. What decides `conductor_phase` is `core_state`, which needs a **core-side** CMB temperature, and that is declared for Earth only (owner decision ①, C25) — which is why Mars is *undecided* rather than wrong. Candidate only: no owner decision is asked for here, and nothing beyond the one measurement C53 (b) recorded has been done. ⚠ **The root is now measured (172 (a)): `core_state.core_cmb_temperature` is supplied by Earth and undeclared on Mars and Pandora.** The core-side CMB temperature is what decides `conductor_phase`, it exists for Earth only (owner decision ①, C25), and that single asymmetry is why the axis in front of the lid never decides on Mars. Candidates for a declared Martian `T_c` are the parallel seat's |
| **C55** | the engine has two irons and Mars's core is between them | **stages 1 and 2 built 2026-09-10; the multi-component core closes ~70 % of the density gap and the 19 GPa floor cuts the corners that would close the rest (C55 (f))** | Opened by C50 (b) row 5's owner-pending cell: Mars cannot declare a `core_material` because neither of our two irons covers it. The printed Martian core density is **5.7–6.65 g/cm³** (S 13–19 wt%), while `fe_prem` sits at 7.6–8.2 and `fe_eps` at 9.0–9.6 — ⚠ **the body is outside both, so declaring either would be asserting a density we know is wrong**, which is why the cell stayed empty rather than taking the default. The owner's decision is to **build a third material, Fe–S**. Source order for the equation of state, held first: Huang 2023 (AIMD) → Xu 2021 (liquid Fe–S mixing) → Morard 2018 → Nishida 2020 → Sanloup 2000; the melting bound stays Mori 2017 with its **declared 10–21 GPa gap**. No number is elected here and nothing is built **at listing time**. **The pre-registration is the section below** (drafted as P13, moved in 2026-09-10 with its anchors resolved). ⚠ **Since then, stage 1 is built**: Huang's printed mixing reproduces its own independent anchor to 0.07 % (178 B), a high-pressure-referenced BM2 gives it a `Phase` without moving any existing material (179), and the sulphur band's **two ends are registered** with the pressure anchor in their names (178 C). ⚠ **The four verdict cells all refuse**, on the 10–21 GPa Fe–S melting gap that predates this item, and **Mars is deliberately not wired** — declaring the material would replace the answers it has with a refusal. Unblocking needs a melting bound in that interval, which is a literature question, not a modelling choice. ⚠ Two owner cells stay open — the sulphur band, and binary Fe–S versus multi-component — and **both candidate EOS anchorings need supplementary tables we do not hold** (B24 Huang Table S5, B25 Xu Table S1). ⚠ **The verdict target does not wait for them**: Durán 2022's printed core radius 1820–1870 km and density 6–6.2 g cm⁻³ anchor the cell today, and **radius and density are two independent axes that each separate the two mantle families** — layer-free 1790–1870 km and 5.7–6.3 g cm⁻³ against layered 1630–1705 km and 6.5–6.75, with gaps of about 120 km and 0.2 g cm⁻³. ⚠ *An earlier version of this row said density could not discriminate; that was built on a density for Khan 2023 which the paper argues against rather than reports, and the retraction is in the section's third amendment* |
| **C56** | `fe_prem` looks temperature-blind, and it is the reference that makes it so | **checked 2026-09-09 — not a defect; recorded so the next reader does not re-open it** | Observed: `fe_prem.density(p, T, 0.0)` returns the same number at 300 K and at 2100 K while `fe_eps` moves. ⚠ **Measured and explained rather than filed as a bug.** The two phases carry different reference kinds — `fe_eps` is `isotherm` at 300 K (laboratory ε-iron), `fe_prem` is **`adiabat` at 1600 K**, because PREM is a fit to *the hot real Earth* and its geotherm is already inside the effective ρ₀. So `Phase.delta_t` returns `t · (1 − t_ref/t_pot)`: it is **keyed on the declared potential temperature, not on T**, and it is exactly 0 whenever `t_pot` equals 1600 K — an identity, not a tolerance, and the stated reason Earth does not move. Measured at 136 GPa: `t_pot` 1600 gives ΔT 0.0 K at both 2100 K and 4000 K (ρ 9916.9370 either way), `t_pot` 2000 gives 420.0 / 800.0 K (ρ 9908.4176 / 9898.9401), `t_pot` 3040 gives 994.7 / 1894.7 K (ρ 9893.4281 / 9862.1307). ⚠ The call that raised the question passed `t_pot = 0.0`, which the same function reads as «no declared potential temperature» and returns 0 by design — heating a PREM fit from a 300 K baseline would heat Earth twice, which `eos.py` names as the trap it is avoiding. No brief; no change |
| **C57** | the inversion branch is not on the node's path at all | **built 2026-09-10 (C57 (a) pre-registration + C57 (b) results): the inversion is on the node path and the silent `earth_like` fill is gone; prediction 1 stays untested for want of a body that inverts** | ⚠ **Corrected from the first reading.** 173 reported this as an adapter default — `state.get("composition_intent", "earth_like")` always handing `solve` a composition — but the audit's call-graph read is sharper: `_from_state → _solve_from_state → solve` contains **no call** to `infer_composition`, `infer_three_layer` or `_porous_rock_verdict` at all, and the only callers are `rocky_roster.py` and `test_interior.py`. **Removing the default would not route the node to the inversion; there is no route.** So the four `inferred_*` regimes are dead code on the chain's path, C45 (d)'s inversion-convention exception guards something the checker can never make the node produce, and no body file will ever change that (173 measured it: 0). The question — should a recipe be able to infer a composition — is left open, and this row exists so the next reader does not re-derive the answer from the adapter line |
| **C58** | two of our own numbers for Mars's core-mantle boundary are 1700 K apart | **redesigned and pre-registered 2026-09-10 as C58 (a): layer 1 asks the material, not the body; `K_CORE` moved to C49; build is 180 B** | C54 (b) declared Mars's core-side CMB temperature from the literature band **1900–2100 K** (Durán+ 2022, held). C20's thermal-history integrator ends the same body at **3763 K**. ⚠ **Both are ours and both are labelled**, and they disagree by roughly **1700 K** on one quantity of one body. The declaration is an observation-constrained band; the endpoint is the output of an integration whose Mars run has never been checked against Mars literature — but «the integrator is wrong» is a conclusion, not an observation, and it is not drawn here. Candidate only ⚠ **Four gammas coexist for one core, listed 2026-09-10 and not touched.** The paper's printed **2.74** is stored and read by nothing; the value **derived** from the stored constants — **1.17 to 2.04** across the eight stage-2 corners — is what drives `grad_ad` in the structure integrator; `core_state`'s `GAMMA_LIQUID_RANGE` holds a **liquid** band **1.51–1.52** and its `GAMMA_SPAN` folds that together with the constant below into one interval; and `core_state`'s core adiabat (`engine/core_state.py@«핵 쪽 경계 온도에서 올린 단열선의 온도 [K]. T ∝ ρ^γ 다.»`) raises the temperature with a **third**, the module constant **γ = 1.5**, and a density ratio — it never asks the material, although every material implements the quantity. ⚠ **None of the four knows about the other three.** That is the same shape as the module `C_P`, in a second place, and it is C45 (f)'s shape as well. **Out of 183's scope; the code is not touched here.** ⚠ **And the two pictures of the same core disagree by a factor of 4.64**, independently of any material's thermal flags. **Anchored at the same boundary temperature** (the structure's own T_cmb, 1909.9501 K) at Mars's declared cmf: the structure integrator raises the centre by **50.98 K**, `core_state`'s adiabat by **236.75 K**. ⚠ *An earlier figure of "five times" here compared the structure's rise against a rise measured from the declared 2000 K — two anchors, so not a ratio.* ⚠ *Neither picture reaches Mars's output when an Fe–S core is used*, because the `melt_bracket` branch writes `t_top` straight through — so this is a disagreement the shipped numbers do not currently show. Audit file `audit/c58_thermal_mismatch_167ac9ee.txt`, sha256 `c76441233760ed6b…`, **3458 B**, hashed here; the two figures above are this seat's own reproduction. |
| **C59** | Mars's core radius and moment of inertia miss the board by 8.9 % and 2.7 %, and no gate had ever checked | **listed 2026-09-10 as a recorded disagreement**; **반지름 축 닫힘 2026-09-21 (오너 «닫자»)** — 황 맞춤(C55 (i), `2471c7ec`)이 착지한 뒤 core_radius_fraction 엔진 0.5431 대 보드 0.5398, 8.9 % → **0.6 %**(허용 3 %). 엔진이 `[기록·해소?]` 로 사람에게 물었고 오너가 닫았다. ⚠ **nmoi 축은 안 닫힌다** — 같은 판에서 −1.9 %(허용 1 %)이고 2026-09-21 에 보드 값이 0.3644 → 0.36340 으로 바뀌며 어긋남이 −1.939 → −1.669 % 로 **다시 계산됐다** (그 판이 `4159b1fd`, 이 행과 같은 게이트가 덮는다). ⚠ 이 행의 본문 칸이 드는 **0.3644 는 그때의 보드 값**이고, 기록이라 안 고친다 — 두 수를 화해시키는 것은 이 상태 칸이다. C99 가 nmoi 축을 든다. | Found by the **targeted** lane, which is the part worth keeping: `check.sh` ran three answer bodies named by hand and `bodies/mars.yaml` was in neither that list nor `gate_targeted`'s copy of it, so Mars's shipped-value comparison went unrun from 2026-09-08 until the body rule ran it (169 E made the list a glob). ⚠ **A narrowing found a hole in the full lane.** The engine gives `core_radius_fraction` **0.4919** against the board's **0.5398** — a core radius of about **1667 km** against **1830 km** — and `nmoi` **0.3545** against **0.3644**, which is the same cause seen through a second quantity. ⚠ **Corrected 2026-09-10 (C59 (a)): the 1667 km is what Mars's *declared* `core_mass_fraction: 0.24` produces, not the preset's 0.325** — a declaration wins over a preset, and 0.325 would give 1842 km, inside the board's window. The board's 1830 km is the layer-free family's anchor (Stähler 2021) — the family the owner chose in 174. That the engine's value falls inside the *layered* family's window (Khan 2023, 1675 ± 30 km) is **read as coincidence**: we never elected that family. Neither the board value nor the tolerance was touched; the two rows print every run and are not counted (Brief 177). What closes this is **C55** (an Fe–S material, since our iron is too dense for Mars) and a declared Martian core mass fraction — not this row. ⚠ **178 C did not move it**: the Fe–S materials exist but all four verdict cells refuse on the 10–21 GPa melting gap, so Mars stays on `fe_prem` and both rows print unchanged. 177's resolution notice has still never fired on a real change |
| **C60** | the solve asks a core material for a surface-pressure density | **built 2026-09-10 in two passes (C60 (a) · (b) · (c)); ⚠ the first pass's conclusion is retracted in (c)** | Found while 178 D was being built, and it is what actually blocks C55's verdict cells — ⚠ **and the first two descriptions of it, one per seat, were both right about different runs.** The audit measured a refusal at **18.9993 GPa**, a *boundary trial step* 0.7 MPa (0.0037 %) below the 19 GPa floor, in the body solve. This seat measured **0.0981 GPa** and traced it: it is a *trial central pressure* from `_shoot_pressure`'s bracket, reached through `integrate`'s `rho_c = mat_c.density(p_center, …)` on the radius-matching path — 23271 calls in that run, the next lowest at 59.0 GPa. **Neither pressure appears in any final profile.** So the shape is one thing seen twice: **a domain refusal raised during a trial is being read as a verdict about the body**, and the core material is only asked from the centre out to the CMB when the answer is actually computed. ⚠ **Removing the floor does not help** — with `p_min = 0` the same solve fails to converge at 9.808e7 Pa, since a 19 GPa-referenced BM2 has no root there. ⚠ **Mars's core-mantle boundary is 20.65 GPa, inside the fit**, so this is not physics telling us the material is wrong; it is the range the solver asks over. Two roads were listed — a low-pressure branch for liquid Fe–S (another fit, another paper), or a solver that asks a core material only at `P ≥ P_cmb` — and **C60 (a) takes a third**: a trial is not a verdict, so the boundary step is read against its own width and the shooting bracket's lower end is raised to the core material's floor. **No fit gains a range and no equation changes.** ⚠ **178 D's registered premise blamed the melting gap and was wrong** — the label on the material said melting, and the message was read as the mechanism |
| **C61** | a step that was never tallied reads as a step that passed | **built 2026-09-10 (184 B) — the tally is part of the gate's own rc** | The third of the 169 E / C60 family: *"did not run" and "passed" were not distinguishable to the gate's own count.* gate229 printed **`[STEP]` 71 · `[TIME]` 19 · rc=0** with **52 steps never judged**, because the pool's spool directory was deleted mid-run and the children had nowhere to write their status. Hardened four ways: the spool is probed for existence **and writability** before each launch and a failure **demotes that step to serial** rather than skipping it; launches are counted in the parent's memory against completions read from the children's **exit-status files**, ⚠ *two independent sources, because a count taken twice from the same log cannot catch the log itself going missing*; `pool_incomplete` names every launched step and sets `fail=1`; and children exit quietly when the spool is gone so the real sentence is not buried. Proved by injection in an isolated harness, which is also where the `«$var»` brace defect and the attribution-losing `step_flush` guard were found |
| **C62** | `tidal_response` does not exist, and the two bodies that need k₂ declare it fitted to our own output | **pre-registered 2026-09-10 before the build (C62 (a)); nothing built** | P28 moved into this file verbatim (parallel seat, sha256 `92b95059014d03db…`, 9211 B). A layered viscoelastic propagator (Beuthe 2015 eqs 13–18) with three rheologies (Bagheri+ 2022 §2.3–2.7) emitted as a **band**, k₂·h₂·Q. ⚠ **The engine has no shear modulus anywhere today**, so μ is a gap the node names rather than a quantity it fills — C58 (a)'s shape, one layer out. ⚠ **A liquid core is the membrane limit and says so** (Beuthe eq. 27); Saito 1974's general liquid-layer condition is paywalled and **not held**, and every output carries that label. Owner-pending: the liquid-layer treatment · μ declared per layer or printed per material · whether a body ever elects a rheology · whether this node's k₂/Q ever replaces the **declared** value C39 unified. **The standing default for the first build is emitter-only**, so C39's seam is kept and no shipped τ moves. ⚠ **The implementation pre-registration is folded as C62 (b) (P35, 2026-09-11, sha256 `bb67e2ced144f8eb…`, 29375 B)** and it closes the owner-pending list above: the liquid layer is the membrane limit with a label, μ is declared per layer then a printed substitute then a named refusal, no body elects a rheology (all three are emitted as a band), and nothing is written into `k2_over_q` — the emitted name is `k2_over_q_emitted`. ⚠ *Twelve amendments reached it, nine of them «the draft asked the engine for something it does not have»* |
| **C63** | the cold φ(P) slot has no law over our own pressure range | **closed 2026-09-10 as a named refusal — no code, no constant, no board changed** | The seven compaction papers held on 09-10 do not print a cold, unsintered φ(P) law over 1–764 MPa (P29, sha256 `8884e29ae2832870…`, 16563 B). Four saturate **at or below 1 MPa** — where our rock law begins; two are φ(P, T, t) rate laws needing a thermal history; one is shock. ⚠ **And five of the seven close a 100–170 km body's pores by ²⁶Al heating above ≈ 700 K**, while our three `voids_expected` indicators fire on mass, grain-fracture pressure and a declared tidal bool — *"tidal" appears 0 times in all seven*. So the indicator set is indexed on a different cause than the literature uses at this body scale. Dante's centre is **317 MPa**, above every cold law held and above the 150 MPa lab range of the law we ship. Owner-pending (a)–(e), none urgent |
| **C64** | one value key, two producers — and the engine's two read paths answer differently | **listed 2026-09-11; widened by measurement from one key to six** | Found while writing C15 (a). `entropy_history_verdict` is a **literal refusal** in `core_entropy` (*"needs C20"* — C20 was built 2026-09-04) and a **computed verdict** in `core_history`, and `engine/test_core_entropy.py@«2: 이 노드는 이력 판정을 **내지 않는다**»` pinned the literal — ⚠ *that anchor now points at the **repaired** test, which pins the key's **absence**; the sentence is about what the test did before 2026-09-11, and the anchor is the only text the repair left to point at* (audit seat caught the verb and the anchor saying opposite things). ⚠ **The family signature is one sentence: there was a check, and the check agreed.** The contract layer says it too — both `Returns` lists carry the key and `check_contracts` compares each node only against **its own**, so nothing counts a key claimed twice; the contract prose even asserts the literal, so a repair moves **ten** places across **six** files and each needs a name — code `values`, code `units`, `chain.yaml` `outputs`, the test's assertion, the test's module docstring, the test's print line, the English `Returns`, the English prose, the ko `Returns`, the ko prose. ⚠ *An earlier draft of this row said three, counted before the repair was written* (audit seat, 2026-09-11). Audit-seat census: **168** contract `Returns` keys, **six** claimed by two nodes (`dipole_moment`·`b_eq`·`b_pol` — the dynamo pair, expected harmless by class exclusivity but **counted, not argued**; `entropy_history_verdict`; `has_inner_core_solved`; `radius`). ⚠ **Direction must be read from `graph.order`'s execution order, not `chain.yaml`'s declaration order** — the two disagree, and for `radius` they disagree *oppositely*: `interior_layers` runs first, so `state.get` returns it and `resolved` returns `mass_radius_relation`. ⚠ *An earlier draft of this row said `resolved` is what emit, the evidence dump and the board comparison read. Measured (audit seat, 2026-09-11): `resolved` is read by `run.py`'s convergence comparison and `state.py`'s summary count — **and by nothing that ships**. So the condition for «latent» is countable: **the number of shipping consumers that receive the losing value is zero.*** **`radius` leaves this item as C65 if the run-side count says it is live.** **Measured 2026-09-11 (audit seat, `audit_dupkeys.py`)**: the dynamo trio is **closed at zero** — no roster body has both ladders applicable, so the class exclusivity holds by measurement rather than by argument; `has_inner_core_solved` is **a duplicated computation whose two values agree**, so it is untidiness rather than a defect; `entropy_history_verdict` **disagrees on earth and mars**, which confirms this item; and `radius` disagrees on **two of the four bodies where both producers run** (`mars` −1.87 %, `dante_fixture` −12.51 %) — that one leaves as **C65** ⚠ **Repaired 2026-09-11 by not emitting what this node does not compute**: `core_entropy` drops the key, `core_history` stays the sole producer, and the refusal survives as a **named sentence in `notes`** instead of a literal in `values`. The pinned test moved with it — it asserted the exact stale string, so it was the check holding the defect in place, and it now pins **absence** plus the refusal's presence in prose. ⚠ *Five anchors this ledger had into that defect rotted with the repair and were repointed at it, with the old text quoted here — four onto `test_core_entropy.py` and one onto the new `core_entropy.py` comment* — a citation cannot point at a line the fix deleted. Measured **in this tree**, five duplicated keys become **four** — the census of **six** was taken before C65 split `radius` out, so `radius` had already left the count when this repair landed (audit seat, 2026-09-11) |
| **C65** | two nodes emitted `radius`, and they were the same solver run on different inputs | **built 2026-09-11 — the name is split; the merge rule is C68** | `mass_radius_relation` does not solve for a radius: it calls `interior.solve` with **mass and a composition preset only** (`engine/mass_radius.py@«structure = solve(mass_earth, composition=composition)»`), while `interior_layers` calls the same function with **everything the body declares**. ⚠ **So the pair was never two methods disagreeing — it was one integrator asked two questions.** The screening output is renamed **`radius_mr_screen`** and its contract says it is not an independent check. ⚠ **And the two measured gaps have two different causes, which the first draft of this row ran together** (audit seat, 2026-09-11). **(a) `mars` −1.87 % is the preset overriding a declaration**: the call site carried a C45 (f) literal, `state.get("composition_intent", "earth_like")`, so Mars solved at the preset's cmf **0.325** instead of its declared **0.24** — *the very number C59 spent a day on*, and the C45 (f)/C59 link belongs to this half only. The default stays (changing it moves values, and that is C59's owner-pending cell) but it is no longer silent: `composition_preset_used` is emitted and counted. ⚠ **But that pair is not one of C45 (f)'s nineteen, and saying it was would have been wrong** (audit seat's static count on this commit: **19 → 19**). C45 (f) counts a *contract* `Needs` given a literal by its caller, and this node's Needs are `mass_earth`·`composition` — `composition_intent` is not among them. The site inside the nineteen is one layer down, the signature default `engine/mass_radius.py@«def assign(mass_earth: float, composition: str = "earth_like") -> Result:»`, and **C65 did not touch it** — that is a follow-up. *What this brief did name is a silent default that was outside the count altogether.* ⚠ *The count did not move: **nineteen before, nineteen after**, measured by the audit seat on this commit against its parent. This seat expected 19 → 18 and was wrong about which layer it had touched. **The follow-up that makes 19 → 18 real** is to write the contract's `Needs` as what the adapter actually looks up, and ⚠ **adding a key is not enough — `composition` has to leave `Needs`** (directing seat, 2026-09-11): C45 (f) counts *a contract `Needs` filled by a caller's literal*, and `composition` against `engine/mass_radius.py@«def assign(mass_earth: float, composition: str = "earth_like") -> Result:»` **is** such a pair — listing `composition_intent` beside it would have left the count at nineteen. Both mirrors now carry `mass_earth` as the only **Needs**, with `composition_intent` and `composition` as **Declared-optional** and the preset named; done in the same commit as this correction, and the re-measurement is the audit seat's. *A declared default is not a hole — calling it required while defaulting it is what made it invisible.* ⚠ **And that move failed the gate** (gate240, `acc49b09`, rc=1, 2026-09-11): `engine/test_check_refs.py` pins the **set** of `Declared-optional` exemptions, and widening a contract without moving that set is caught there and **nowhere else** — `check_contracts`, `check_refs` and `check_md_tables` all passed on the same tree. *The direction is the point: a widening exemption list is silent everywhere except the one net that names it.* Repaired in **C64 B** by registering `mass_radius_relation: {composition, composition_intent}` with the reason, moving the printed shape from «고유 10 · 슬롯 13» to «고유 12 · 슬롯 15» **Nothing in the gate counts these**, which is why the expectation went unchecked for two messages — putting the count in the gate is a follow-up candidate under C45 (f), the same shape as today's census of constants nothing reads.* **(b) `dante_fixture` −12.51 % is inverse against forward**: that body declares neither `composition_intent` nor a core mass fraction, so `interior_layers` **inverts** to match its declared radius (0.08175 R⊕, −0.034 %) while the screening node runs a preset **forward** without knowing that radius. ⚠ *Fixing the preset would not narrow that one at all* — it is the case the rename exists for. ⚠ *And the counter is 1 today, on `dante_fixture` — the same body as the larger gap, for an unrelated reason. The label says so, because a counter and a gap pointing at one body invites reading them as one fact.* Two `chain.yaml` edges that declared `via: radius` from the screening node are moved to `interior_layers`, which is where all five shipping consumers already read. ⚠ **And only one of the five actually spends the value**: `core_thermal_history` asks `get_optional("radius") or get_optional("radius_earth")` — computed first. The other four write `get_optional("radius_earth", get_optional("radius"))`, and **Python evaluates the default argument first**, so the `radius` lookup is *logged* while the value used is the declared `radius_earth` — which all four rocky bodies declare. *So «five consumers, all reading `interior_layers`» was true about lookups and misleading about use: the number itself reaches one node.* ⚠ **Candidate**: that pattern records lookups nobody spends, which is noise in C45's lookup log — the eager default is the cause |
| **C66** | constants that are stored and read by nothing | **listed 2026-09-11 — candidate, disposal is per-item** | Audit value-trace over 63 constants: **12 are stored only** — 7 read by nothing at all, 5 read only by a test — and **1 was cited but not implemented** (Dorogokupets, filled by 180 C). ⚠ **A stored constant that nothing reads tells the next reader «a decision lives here» when none does**, and that is C45 (f)'s shape without a call site. The seven: `MORI_FES_P_MEASURED_MAX` · `IRON_FES_WINDOW_HIGH_POINTS` · `XU_FES_T_REF_K` · `ALPHA_C` · `NH3_REF` · `FE_S_BAND_WT` and the remainder after tidying, plus `core_energy.py`'s twin of the dead `GAMMA` alias 180 C removed from `cmb_flux.py`. ⚠ **Disposal is not a sweep**: brief 185 is about to *read* `IRON_FES_WINDOW_HIGH_POINTS`, so each name is decided by the brief that owns its physics — deleting them together would delete the ones that are early rather than dead |
| **C67** | the core adiabat carries one exponent where the material now has two | **listed 2026-09-11 — candidate, outside 180 C** | `core_state._adiabat` raises the centre temperature as **T ∝ ρ^γ with a single γ**, asked at one pressure. That was exact while γ was a constant. ⚠ **180 C made γ a function of pressure inside one core**: Mars's γ is **2.8718** at its CMB and the fallback **1.5** at its centre, so the closed form integrates a γ the material does not have over most of the interval. The structure integrator already does this correctly — it asks per step — so the repair is to make the declared branch integrate γ(P) the same way, or to state the exponent it uses and why. **Not built here**: it moves `core_temperature` and `center_margin` on every body with a core, which is a verdict-moving change of its own |
| **C68** | nothing decides who wins when two nodes emit one name | **built 2026-09-13 — the name is split (C68 B, `347f77d2`); duplicate-producer constant 9 → 8 in this commit** | Today the winner is a side effect: `state.get` returns the first applicable node in `graph.order`'s topological order and `state.resolved` the last, so **moving a node in `chain.yaml` silently changes which value five consumers of `radius` receive.** The rule to build has **three states**, and the third is the point of it. ① **an owner is declared** → only the owner's value enters `resolved` (`radius` → `interior_layers`; ⚠ `has_inner_core_solved`'s owner is an **owner decision** — the two values agree today, so it is a duplicated *computation*, and «which computation is right» is a separate question this rule does not answer). ② **the claimants are class-exclusive** (`dynamo_giant` / `dynamo_rocky` on `b_eq`·`b_pol`·`dipole_moment`) → passes **without** an owner, but the contract check **measures and records «zero same-run co-occurrences» every run** — ⚠ *an allow-list would let the exclusivity rot silently; a measurement fails the day it stops being true.* ③ **neither** → **FAIL**. Built by neither C64 nor C65: those two supply the owner declarations this rule reads ⚠ **And the rule has to distinguish two layers**: in `chain.yaml`'s `outputs:`, `radius` is produced by **three** nodes, not one — `interior_layers` plus two of `kind: measured` (`mass_or_radius`, `star_physical`) that have no recipe at all. An owner rule written for computing nodes would either miss those or refuse them wrongly (audit seat, 2026-09-11). ⚠ **And a declaration outranks both**: a `kind: measured` output enters `state.inputs`, and `_find` reads declared inputs **before** any node's values — so the three states above are a **node-against-node** rule, and where the body declares the quantity the declaration wins before the rule is consulted. The rule must say that, or it will look like it decides cases it never sees. ⚠ **And the blast radius of the order is one node, one body, 12.51 %** — not «nothing». If the topological order flipped, `core_thermal_history` is the one consumer that spends the computed `radius`, and `dante_fixture` is the one body where the two producers differ enough to matter. *Small is not zero, and the rule is for the day it stops being small.* ⚠ **193 lands the check as reporting** (`check_contracts.c68_merge_rule`, draft `bc1584ee63fae89c`, 107 lines) — ⚠ *and not in `chain.py`, where the draft registered it*: `chain.py` sees the graph and nothing else, while «do these two producers run for the same body» is a runtime fact that exists only in `check_contracts`'s `body.results[node].applicable`. *The registered location was written before anyone asked where applicability lives* (directing seat's ruling, 2026-09-12; 193 Amendment 2): per duplicate key it prints the three states, the producers in `graph.order(g)` position, the measured overlap and the declared owner — **and it judges nothing**, because a red check and its repair in one commit hide which did what. ⚠ **The measurement found a fourth state the draft did not register, and it is a state rather than a caveat**: «잴 수 없음» — unmeasurable with today's harness. Of the nine keys only **three** are class-exclusive on evidence — `b_pol` · `b_eq` · `dipole_moment`, `dynamo_giant` applying to 3 samples and `dynamo_rocky` to 4 with **overlap 0** — **one** reports a real collision (`has_inner_core_solved`, `core_energy_balance` @34 and `core_entropy_production` @43 both applying to **Earth and Mars**), and **five** cannot be measured at all because a producer never runs in this harness: `mass` · `p_rot` · `present` (both producers silent) · **`radius`, where two of three are silent** — `mass_or_radius` @4 and `star_physical` @11 never ran while `interior_layers` @24 applied to **4** samples, so its computing producer *was* exercised and only the two `kind: measured` ones stayed quiet — and `nmoi` (`nmoi_class_table` silent). *The harness solves the **15** nodes that have a registered recipe out of **35** computed ones, so a producer that never answered and a producer that answers only elsewhere both show overlap 0* — and the first is an absence, not a measurement. *So the draft's registered «FAIL» prediction for those five is **neither confirmed nor refuted**, and saying so is the finding.* **No owner declaration exists anywhere in the contract today**, so the «owner-declared» state is unreachable and the code says where it would be read. C73's gap is **39 + 1**, unchanged across this item (measured with the audit's `c62_outputs_vs_returns.py`), and the checker is imported by no engine module, so no solved value can move. |
| **C69** | the temperature loop's update rule oscillates, and the budget cannot buy convergence | **listed 2026-09-11 — candidate, pre-registration first** | 180 D measured it: the proportional update `T_c ← T_c·(T_pot/T_surf)` **overshoots the root** for water-rich rocky bodies under 180 C's steeper core adiabat, and the oscillation damps by only **0.878 a step**, flattening near **1 %**. ⚠ **Extending the pass budget is not the answer** — measured: `imf 0.3` converges with two extra batches, `imf 0.1` does not even with **+28 passes**, and the failing path costs **123 → 334 s**. The remedy is an under-relaxation factor **α < 1** on the update, ⚠ *which is a change to the update rule rather than to trial machinery, so it moves the path of bodies that already converge* — C60's rule says that needs its own pre-registration with a bit-identity table, not a fix folded into another brief |
| **C70** | the path fingerprint watches seven functions, and the ones this work changes are not among them | **closed 2026-09-16 — `da3a10c6`** | `test_ice_giant`'s `PATH_FUNCTIONS` covers `solve`·`shoot`·`_shoot_pressure`·`_narrow_bracket`·`_surface_temperature_met`·`_stack`·`integrate` plus thirteen constants, and `_feed_code` **does not follow calls** — so a change inside a function the watched ones *call* is invisible. Measured: 180 C/D changed `_adiabatic_dtdp` and added `_core_or_own_gamma`, and the fingerprint stayed silent about both while catching `shoot`. ⚠ **That silence was not a miss** — those edits move values, and the value assertion caught them (Mars's three thermal-history anchors); on the ice giants they are a no-op because those bodies use no core material. **The residual risk is the thin case: a path-only edit to `_adiabatic_dtdp` that leaves the frozen values alone.** ⚠ *The danger is not the gap itself but reading the gap as agreement* — «21 items, 1 changed» invites «the path barely moved». Widening the list is not a one-liner: it re-freezes the stored fingerprint, which then has to be justified by the value assertions again, so it needs its own commit and its own before/after table. The rule that says «answer an interpreter-version change with `--refresh` rather than by widening the fingerprint» is about **versions**, not coverage, so it does not forbid this. ⚠ **And the cheap half is not the list but the count**: the fingerprint should **print how many functions it does not watch** — a watch list that says nothing about its own coverage is what let «1 of 21» read as reassurance |
| **C71** | the non-convergence warning is prose, so no consumer can read it | **closed 2026-09-16 — `a818d58c`** | `interior.solve` returns a full `values` dict when the shooting loop ends unconverged, and the only warning is a sentence in `engine/payload.py@«line += " ⚠ 미수렴 1차 통과값"»` — **`evidence()` prose, not a value**. ⚠ **And `converged` is structurally out of reach**: it is a `Result` field, `state._find` looks only at declared `inputs` and each result's `values`, and **no computing node touches `state.results`** (only `check_contracts` does). So the five consumers of `radius` cannot see it — **0 of 5, by construction rather than by oversight**. Sampled: the audit seat's clone without 180 D's budget extension returns **R 1.130250786008135** with `converged False` for the water-rich body `imf 0.1`, a radius that is not a solution sitting in the value slot. ⚠ *This is C58 (a)'s registered line — «prose can be grepped but only a value can be counted» — one layer down, in the object every node returns.* Repair shape: emit it as a **value** the way `core_gamma_fallback` is emitted. Verdict-line candidate: does `interior_layers`'s result carry the non-convergence as a value, and can all five consumers read it. ⚠ **Mechanism landed 2026-09-11 (189, commit 1 of two)**: `interior_layers` now emits **`converged` · `unconverged_solvers` · `bracket_invalid`** in `values`, so `state._find` reaches them and the prose line is no longer the only trace. Census: **34 solver or integration sites** (audit's `c71-loop-census-7ae0ed27.txt`, sha256 `19599ae6a5fdcb1e`) — **11 wired in commit 1** (`interior.py` and `eos.py`), the rest in commit 2. ⚠ **`converged` is three-state**: `True` · `False` · **`None` for a loop with no criterion branch**, which is 13 of the 34 by the mechanical test «no `return` and no `break` in the body» (audit's `c71-criterion-branches-7ae0ed27.txt`, sha256 `200c72b6adbe322d`) — *asking «did it exit by its criterion» there would be permanently false, and adding a criterion would change the returned midpoint, which the brief forbids*. A node whose sites are all `None` reports `None`, never `True`: «nothing to ask» and «everything passed» must not print the same. ⚠ **The sign check's cost, counted rather than asserted**: on the six-body set plus five `interior.solve` cases the two instrumented melting bisections are **never reached** — `iapws_p_melt` is called **0 times on both trees** — so the acceptance run measures no cost at all; exercised directly, `water_t_melt` on the ice branch goes **82 → 84 calls** per invocation (+2, the two entry evaluations) and returns the same value to the last digit (266.21729613628384 at 0.5 GPa). *A cost that the acceptance set cannot see is still a cost, and it is written here rather than left at «no measurable change».* ⚠ **Commit 2 wires the remaining nine modules**: 30 named sites across `interior` · `eos` · `core_state` · `core_energy` · `mantle_flux` · `stagnant_lid` · `steam_if97` · `water_hot` · `ammonia_table` · `fermi` · `fe_liquid` · `transitional_lid` · `tidal_transport`. **Four of the census's 34 are unwired, and each is named with its reason**: the three unbounded loops are C77's and get no label by decision, and **`interior.py`'s temperature relaxation loop** (`while passes > 0`) is left alone because **it already reports exhaustion by raising a named `ValueError`** — a flag there would duplicate a signal that works. ⚠ *`core_energy` :112 · :219 and `interior` :1376 are **not** in that list: they were never candidates* — section G of `19599ae6a5fdcb1e`, conditional `while`s that stop on a geometric condition and cannot exhaust. *The count and the list have to name the same set, and an earlier version of this sentence said five while listing three non-candidates and omitting the one real one.* ⚠ **`water_hot.density` and `fermi.inverse` record `bracket_checked=False`** rather than a checked bracket — their evaluation path reads and writes a warm-start global (`_LAST_DENSITY`, `_LAST_INVERSE`), so one extra `f(hi)` would change the **next** call's answer and the failure would move with call order. ⚠ **And the acceptance check reads «the three keys are present on every body, including when their value is empty»** — the audit's own JSON flattener dropped four of nine moved keys because *an empty list has no leaves*, which is exactly the value a «nothing went wrong» field carries. Bit-identity: four body files and five solve cases on the five keys, all 21 materials on the C58 grid, **and pass 1 against pass 2 in the same process** — the order-dependence a warm-start global would produce does not appear on either tree. ⚠ **And «values bit-identical» never implies «path unchanged»** — commit 1 moved three of C70's seven watched functions (`_shoot_pressure` · `_narrow_bracket` · `integrate`) while every value stood still, and the gate caught it: `[FAIL] 경로 지문 599684df3e9fa137 → 53fcf0f2577f857e`. **From here every acceptance line names three things** — the call-surface table, the anchor values hash (`anchor-baseline-7ae0ed27.values.txt`, `5499493e5d9bf6b8`, the timing-free twin, since the full file embeds wall-clock stamps and cannot hash stably) and the **C70 fingerprint, stated as moved or unmoved *with the traced functions that were edited*** — so the entry is a claim that can be wrong rather than a stamp. *The refresh commit moved `path_fingerprint` and nothing else structural: `steps` 1500 unchanged, `frozen_at` and `python` unchanged, the two bodies' radii identical to the last digit; what else moved is the per-body wall-clock `seconds` and the three new keys arriving as values (None → True/[]).* ⚠ **And a reading rule this day bought three times over**: when `git status --porcelain` is non-empty, a file or line read is labelled «worktree @&lt;tip&gt; + uncommitted», never «read at &lt;tip&gt;» — or it is read from a clean clone. *Three seats cited line numbers from dirty trees today and two of them had moved.* |
| **C72** | the ice giants come out larger than their published radii, and nothing ever printed the gap | **listed 2026-09-11 — a registered baseline, not a verdict** | Audit seat's anchor run on `c2a6a324` (`anchor-baseline-c2a6a324.txt`, sha256 `6747d42f2757c5d4`): Uranus **+5.48 %** (4.1989 against 3.9808) and Neptune **+8.94 %** (4.2101 against 3.8646), with GJ 1214 b converging too. ⚠ **The reason nobody had seen it is the shape of the check, not the size of the number**: the anchor tests assert bit-identity against the previous run, so a deviation that is stable is invisible to them — it has been the same wrong number every time, and a test that asks «did this move» answers no. *Registered as a baseline so the next change to the ice-giant path has something to move against.* Not a verdict: what the gap is made of — envelope thermal state, the gas mass fraction, the published radius's own definition — is not measured here |
| **C73** | `chain.yaml`'s `outputs` lags the contract `Returns` by forty keys, and the three layers do not read each other | **listed 2026-09-11 — candidate; the repair is a brief of its own** | Audit seat's census (`c62_outputs_vs_returns.py`, sha256 `2b299bed1210c77e`; output `b38698ac478e4c56`): **forty** keys are in a contract `Returns` and in the code's `values` but **not** in the graph's `outputs` — `interior_layers` 7, `core_state` 9, `tidal_locking` 8 and more; 180 C's nine `core_gamma_*` and two `integrator_*` are among them. ⚠ **And the count has one in the other direction** — `tidal_locking.t_lock` is in `outputs` and not in `Returns` — so it is not «the graph is behind», it is **three layers that do not look at each other**. The practical bite is that a `via:` edge on such a key fails `check_via`, so the next node that wants one becomes the first consumer of an undeclared value. *C62 (b) added exactly the one it needed (`crust_thickness`) and left the other thirty-nine* — closing all forty, plus a «`Returns` ⊆ `outputs`» rule in the checker, is a separate brief ⚠ **194 lands the check as reporting** (`check_contracts.c73_outputs_vs_returns`, draft `767c5bd98b8b0127`, 72 lines): both directions are printed against a baseline pinned as a **set** — `Returns` minus `outputs` **39**, `outputs` minus `Returns` **1** (`tidal_locking.t_lock`) — because a count cannot see one key leaving as another arrives, which is the shape C75 was bought by. It **judges nothing**; the flip to FAIL belongs to the commit that closes the gap. ⚠ **No edge is drawn and no key is declared**, so `graph.order(g)` and the nine duplicate-producer keys are fixed by construction rather than by measurement. ⚠ *The gap is real and inert*: none of the 39 appears on any edge's `via` or anywhere under `phase4/`, so nothing reads a key the graph does not declare — what it costs is **declarability**, since a consumer edge cannot be drawn to a name the graph does not know. ⚠ **The contract is the source of truth and the graph follows**: `Returns` is checked against the code by `check_contracts` while `outputs` is checked against nothing, and the direction says the same — 39 against 1. *But `outputs` is not generated from it*, which would delete the graph's ability to say «this node returns more than the graph cares about». ⚠ **Location, recorded as a cost rather than an impossibility**: both sides here are static, so `chain.py` could host this check if `parse_contract` moved out of `check_contracts.py` — it is not worth moving or duplicating a parser for one census, and *the draft never registered `chain.py` anyway* (its §4 borrows only the pin's shape). ⚠ *Unlike 193's deviation, which was structural.* ⚠ **One defect of my own, caught by the numbers**: the first run asked `parse_contract` for `"Returns"` where the key is lower-case `returns`, so it read an empty contract and printed **0 + 164** — the census script's own key is what fixed it. |
| **C74** | the silicate slot answers from a fit, and a fit cannot be asked «what if this mantle has more iron» | **listed 2026-09-11 — open on P34's A–I only; licence Q1–Q7 answered 2026-09-11 by the REBOUND precedent + owner decision (a)** | P34 (parallel seat, sha256 `10034d9c085a6dde`, 19376 B) folded with what P30 §6 and §8 have settled since. Today's mantle is **two fitted `Phase` objects**, and a fit cannot be asked what a different chemistry would do — the item is an assemblage **computed** from declared chemical ratios (BurnMan `equilibrate` over `SLB_2022`), which is owner decision (c) ② of P30 §5. ⚠ **Installed 2026-09-12 by 191, into a venv of its own** — `engine/.venv-burnman` (Python 3.9.6), pinned by the new `engine/requirements-burnman.txt`, with `engine/.venv` and `engine/requirements.txt` untouched because the latter's `mpmath==1.4.1` is the Fermi check's second oracle and `sympy 1.14.0` wants `mpmath<1.4`. **No engine module imports BurnMan**, so P34's prohibition 6 is untouched and owner row F — which interpreter the silicate node uses at runtime — stays open. ⚠ **Two decisions inside the transcription item are taken and two source readings were corrected.** The stability and reaction tables are *«Summary of phase equilibria data»*, so the refusal is «outside the data coverage» and never «outside the valid range»; a species carries several rows and each row is a **P×T box**, so **J** covers a body only when its (P, T) lies inside at least one row's box and **forbids separate unions of the P and T intervals** — 9 GPa · 1200 K can sit in the P-union and the T-envelope while sitting in no row; the reactions table (**A5** in 2022, **C5** in 2024, never C4, which is stability) carries **K**, which attributes a row's box to every participating species under a `reaction-row attribution` label. ⚠ *No table value is transcribed here or in the section — only paper, table and printed page* — because check ⑧'s transcription does not exist yet, so the only coverage sentence this material may print is «coverage not transcribed yet». ⚠ **Decision C is the eleven author-not-recommended species `SLB_2022.py` ships** (of seventeen in the held `HeFESTo_parameters_010121-README.md`, `c645fbf93a5b1ba3`) — not «four spin transitions», which was four of the eleven — and it carries three named candidates, **C1** include all · **C2** exclude by default with a declared opt-in · **C3** exclude with no opt-in, default **C2** pending owner ⑥-2. ⚠ **I and Q7 are one decision**: the cached (P, T) grid candidate builds a derived artefact of a dataset whose README forbids redistributing modified data, and whether a derived grid is that is a reading the README does not make |
| **C75** | `check_md_tables.py` does not count cells per row, so a ragged table passes | **closed 2026-09-11 — rule built, corpus repaired, baseline 0** | Found by hand, not by the checker: the C74 owner-decisions table's **C** row carried two cells in a three-column table (one column separator missing), and `check_md_tables.py` returned rc 0 over 827 files — it checks tables glued to prose, not cell counts, so the row would have rendered with its three candidates crammed into the *decision* column and the *candidates* column empty. ⚠ **The repair is not «add a cell-count rule»**: before widening the check, **measure how many existing tables are ragged**, because a rule that lands on a corpus nobody counted turns a green gate red for reasons unrelated to the change that tripped it. *Same shape as C61 and C70 — a check whose silence was read as agreement.* **Counted first, then built.** The census over the same 827 files, by the rule as built: **32 ragged rows**, **26** if code spans are stripped before splitting, and **11 of the 32 carry more cells than their header** — those are the ones where GFM truncates, so the text is in the file and not on the page. `\|` is the only escape; code-span stripping hides 8 of the 32 and invents 2 the renderer does not see, so the rule does not strip them. A table's rows run from the delimiter row to the next blank line, which is the renderer's range and not «lines that contain a pipe»: a paragraph glued straight under a table body, and a row soft-wrapped onto the following line, are both absorbed as further rows. **Nine of the 32 are that** — a different nine from the 8 above, and not the same repair either: six glued paragraph lines in one results file, fixed with a blank line, and three continuation lines of rows split across two lines, fixed by joining the row. An earlier census with the narrower range read 24 and 18; the range was corrected against a renderer and both totals moved. 31 rows repaired, 1 registered exception with its reason — a preserved-verbatim record whose row is short, which GFM pads, so nothing is hidden from the reader. Row counts and the escape behaviour were checked against markdown-it in CommonMark + table mode, not asserted. The per-row census lives in the 0911 interior-state artifacts beside this build |
| **C76** | a material method that raised on the clean tree was invisible to every body-level baseline | **listed 2026-09-11 — candidate, tooling** | `Material.c_p` computes γ = (∂P/∂T)_V / (ρ c_V) with `Phase.c_v_at`, which returns the **set's** `c_v_ref` — and an evaluator set has none, so the value is 0 and the call raises `ZeroDivisionError`. `fe_prem` had been doing this above 35 GPa since 180 C, on a green tree, because **no body calls `Material.c_p` on a core material**: the only in-engine callers are the mixture classes, the water tables and `grad_ad`'s latent-heat branch, which fires for silicate alone. ⚠ **The six-body fingerprint and the C58 thermal table both stayed bit-identical while the method was broken** — the table records `c_p` nowhere. Measured at 20dc2fe6 against the 187 patch: **30 `fe_prem` cells move, and every one of them was an exception rather than a number** (`187-cp-evaluator-cells-20dc2fe6.txt`, sha256 `af6f729f12944396`); `fe_eps` moves 108, all number-to-number. **Repaired in 187**: `c_p` asks the evaluator for c_V and γ, the constant path is untouched, and a named test walks both materials' call surface across both intervals. ⚠ *The rule this buys*: **an acceptance line measures the material's whole call surface, not only the bodies** — the C58 thermal table should carry `c_p`. ⚠ **And 187 registered a movement its own mechanism could not produce**: the pure-iron limit curve (`interior.solve` with `composition="iron"`, the branch `infer_composition` calls) returns **`core_temperature` 0.0 and `cmb_pressure` 0.0** at 0.3 · 1 · 3 M⊕ — that path carries no temperature, so **`r_iron` was unmovable by a thermal-set change at any mass**, and its bit-identity is a structural zero rather than a result. *The draft's «sign not predicted, the run will say» was wrong about the mechanism, not confirmed by the measurement* (audit seat, 2026-09-11). ⚠ **And 187 widened an API on the same page**: `thermal_label` went from `(fit_composition, p)` to `(fit_composition, p, t)` — all three in-repo callers are positional (`eos.py`, `interior.py`, `test_fe_hcp.py`), so nothing broke, but a bounded set asked without the coordinate it is bounded in now grades rather than passes |
| **C77** | an unbounded loop with no exit label | **listed 2026-09-11 — candidate, tooling** | Three loops have no budget at all: `engine/core_history.py@«맨틀·핵 결합 열진화 적분기 (C20)»` (the time integration), `engine/interior.py@«괄호를 다 올려도 거절하면 그때는 진짜 거절»` and the second bracket walk beside it (bracket walks). Each leaves on a **named** condition — a refusal, `NoCompactRoot`, a re-raised `PhaseGap`, or a `break` — and in none of them is **exhaustion** defined, because there is nothing to exhaust. ⚠ **189 labels none of them**: giving an unbounded loop an exit is a behaviour change, and 189's promise is that a converged run cannot tell it landed. *Named as three rather than one so the next reader does not meet `core_history` alone and assume the other two were examined and excused* |
| **C78** | density answers while the thermal methods refuse at the same (P, T) | **listed 2026-09-11 — candidate** | `nh3`'s `c_p` · `grad_ad` · `gruneisen` refuse by name at 100 and 200 GPa / 1000 K (Bethkenhagen+ 2013 Appendix B Table I isotherm edge, 6 cells) and `h2o`'s `liquid_at` raises `PhaseGap` at 19 and 19.5 GPa / 1000 K (2 cells), while **density answers at all four points** (2274.9 · 2839.3 · 2012.1 · 2025.0 kg/m³, measured). ⚠ **Not C76's shape** — those refusals name a source and a boundary, C76 divided by zero with nothing behind it — **but the same blind spot**: a named refusal on a method no body reaches is invisible to every body-level baseline, and the audit's call-surface table (`60c75ee934d1a85c`) is what sees it. Open question for the row: should a material whose density answers while its thermal answer refuses carry a material-level label — one `thermal_domain` narrower than `p_min`/`p_max`? *Decide when a body reaches it* |
| **C79** | the ice VII/X thermal answer was two constants from a spline nobody could re-derive | **built 2026-09-11 (190)** | `h2o`'s ice VII and ice X carried one `alpha_k`/`c_v_ref` pair each, evaluated at 300 K from SeaFreeze's `VII_X_French` spline. **190 replaces both with a `ThermalSet` that evaluates French & Redmer 2015's printed free energy** — eq (6) = (9) + (11) + (15), the assembly §VI recommends — so the grade is «printed potential, our derivative» (draft `5ba7439876545361`). ⚠ **The XC parametrization changes on purpose**: the shipped set takes the authors' recommended **HSE parametrization of Eq. (9)** (§VI, p9), while the spline behind today's constants is **PBE** — measured at ρ 2.2566 g/cm³ · 1000 K, PBE gives 30.000 GPa · K_T 102.65 against the spline's 30.000 · 102.60 (four to five digits), and HSE gives 30.324, about **1 % in P**. *Table I is the only table with XC variants; Tables II and III have none.* ⚠ **A parse-time guard names the column by its own numbers**: Table I's `a0` is negative for HSE alone, so a mislabelled load raises rather than agreeing to five digits under the wrong name (187's ambient-K_T guard, one item later). ⚠ **The window is the fit grid, not the stability field** — 92 MD points over ρ 1.6–4.25 g/cm³ and T 295–2000 K (p3), converted to 3.23–353.8 GPa by the potential itself; outside it the set is `graded-extrapolation` **because the author wrote «well behaved in extrapolation»**, a different warrant from 187's grade ②. Acceptance: four body files and five `interior.solve` cases bit-identical on all five keys including the second pass in-process, 20 of 21 materials bit-identical, **`h2o` 28 cells moved** and nothing else, C70 fingerprint **unmoved** (`3bcb4d7334472eef`, no traced function edited). ⚠ **Cost, measured after the fact**: `engine/test_interior.py` alone goes **693.11 s → 5276.14 s (7.61×)** from `f681afbd` to `587842b3`, with the two runs' **outputs byte-identical** (301 lines, `fd826ed6c9b39b30`) — *the same answers, computed 7.61 times more slowly*. Stated as a **ratio lower bound, not a benchmark** (user 4043.77 s against 5276.14 s wall; a short external job ran inside the window). **Repaired by 190 B**, whose suspect is `density_at`'s fixed 80-step bisection at ≈164 free-energy evaluations per inversion. Logs in `2026-09-11-interior-state/gate-logs/`, whose `INDEX.md` is **named without a hash on purpose** — ⚠ *an index grows whenever an artifact is added, so a hash pinned to one goes stale on the next improvement and a reader cannot tell an improvement from a tamper*. This row cited `a04161589530f0e2`; adding two `.time` files and one `.out` moved that index to its present contents, and it has moved twice more since (audit seat, 2026-09-12) — *so the destination is not pinned here either*. **The files an index lists are immutable and their hashes are not**, so the pins that matter are the artifacts: `tinterior-new-587842b3.out` `fd826ed6c9b39b30` and the two `.time` files `8d3d43ddbccb0bec` and `afa4b79d279aae19`. ⚠ **Two defects of shape rather than of value, fixed together**: `_debye` rebuilt its 32 Gauss–Legendre nodes on **every call** though they do not depend on `z`, and `thermal_at` had **no memo** where its sibling `fe_liquid` has one. The nodes are now built once and the memo is the pure-input kind, not a warm-start global. ⚠ **Each half with the question it answers, third and final form** — *the two earlier versions of this clause were generalisations of correctly measured numbers past their own scope*. **Nodes rebuilt per call: 98 % of the cold per-call cost** (130 → 2.5 ms; audit's interleaved three-way, twelve states, values identical, output `b8f4315c9ecb9f71`; `_debye` alone 244.98 µs → 3.61 µs). **Memo: −0.1 % cold per-call** — that run clears the cache before every state by design — **but on the integrator's path 12 288 of 19 024 `thermal_at` requests hit it (64.6 %) in one 200 K Europa-type solve**, so without it the inverter does **2.82× the work** (work seat's counter, 2026-09-12). The retracted «memo major, nodes ≈10 %» compared **two already-fixed variants** and measured nothing. ⚠ **The memo's effect depends on which question is asked, and the scope belongs in the sentence**: **cold per-call cost − 0.1 %** (the three-way clears the cache before every state, by design), but **on the integrator's own path 64.6 % of requests never reach the inverter** — one 200 K Europa-type solve makes 19 024 `thermal_at_hse` calls that collapse to 6 736 inversions, so without the memo the path does **2.82× the inversion work** (work seat, counter run, 2026-09-12). *This line said «memo major», then «not justified by performance», and both were generalisations of correctly measured numbers past the question they answered.* What keeps the memo safe is unchanged: 189 Amendment 2's distinction — a pure-input cache cannot move the next answer, a warm-start global can. **Values unchanged — twelve (P, T) states identical by `repr` across the change.** ⚠ *The **anchor** wall time is still unmeasured on a quiet machine*; the **per-call** figures above are not — they come from the audit's exclusive slot at load 2.58 → 2.61. *This caveat once said «the speed effect» unqualified and the row grew quiet measurements underneath it: a caveat is scoped when it is written or it disowns whatever arrives next to it.* ⚠ *The first anchor run's «four times its baseline» is **unconfirmed**: it and the timings taken to explain it were measured while another seat ran CPU-bound loops and a browser held most of a core, so both sides of that comparison are contaminated. The quiet re-run is the measurement, and it prints `uptime` load before and after* |
| **C82** | the registered pressure window overstates the domain, and outside it the inverter saturates in silence — **197 makes the clamp a written branch, 190 C moves the wall past the refusal** | **built 2026-09-13 (190 C); 197 the branch, 190 C the domain** | `ice_fr2015`'s set declares 3.23–353.8 GPa, but the honest domain is the **ρ bracket [1.6, 4.25] g/cm³ mapped through P(ρ, T)** — a **temperature-dependent band**, not a rectangle. Outside it `density_at` runs its bisection to a fixed point against one wall and returns **ρ_min or ρ_max**, with `bracket_valid=False` as the only trace and **no refusal anywhere**. ⚠ **Both demonstrations sit inside the non-graded set**: `density_at(3.30 GPa, 2000 K) = 1.6` and `density_at(345.0 GPa, 295 K) = 4.25` (audit seat, confirmed here). ⚠ *And the graded interval does not save it* — above P(4.25, T) the extrapolation set **pins rather than extrapolates**, so the label says «beyond the fit grid» while the value says «the wall». The upper mismatch is a **wedge 11.62 GPa wide at 295 K** (P(4.25, 295) = **342.18** against the declared `p_max` 353.8) **closing to zero at 2000 K** (P(4.25, 2000) = 353.82) — measured here. **190 C decided: widen** (2026-09-13) — the bracket reaches 5.75 g/cm³, which is past the pressure at which `ice_x` refuses by name, so the wedge is inverted rather than pinned and the answer carries a grade; the refusal alternative was not taken. *First real customer of 189's `bracket_invalid` list, which recorded this every time and was read by nobody.* ⚠ **And the list is the only place it shows, per call rather than per solve**: `Trace.note` uses `setdefault` for `None`, so a solve with one good inversion and one clamp reports the site's state as the good one and the clamp survives only in `bracket_invalid` (audit seat, 2026-09-12) ⚠ **And the same item was listed twice in this table with two different status cells** — one «built 2026-09-13 (190 C)», one «built 2026-09-13 (190 C); 197 the branch, 190 C the domain» — until they were merged on 2026-09-14 (C90's first finding; the fuller status and both bodies are kept, nothing is dropped). **The build, as that second row recorded it:** 97 replaces the bisection with a **safeguarded secant** (tol 1e-10 relative on ρ, one bisection step whenever a secant step leaves the bracket) and — because the old clamp was an *accident of halving against one wall* — adds an **explicit entry guard**: out of bracket it returns the wall value and notes `bracket_valid=False`. ⚠ **Demonstrated, not assumed**: `density_at(3.30, 2000.0)` = **1.6** and `density_at(345.0, 295.0)` = **4.25**, and across **1 257 unique clamp states** the two implementations differ in **0**. **Clamp rates are properties of the states asked**: `Uranus` 6.78 % · `Neptune` 0.025 % · a 200 K Europa-type solve 4.63 % — M2 turns on those. ⚠ **Cost**: `free_energy` per that solve **833 250 → 220 506** (−73.5 %), per inversion **123.70 → 32.74**, closing as guard 4 + 2 × **8.868** iterations + 11 outside; `thermal_at_hse` 19 024 and `density_at` 6 736 **unchanged**. ⚠ **Values: printed digits unmoved, ρ moved** — the payload threshold is `engine/run.py@«[{mark}] {key:14} 엔진 {got:>9.4g}»` (four significant figures) and **0** cells moved across six control rows ×2 and the anchors, which also reproduce `anchor-baseline-7ae0ed27.values.txt` (`5499493e5d9bf6b8`); but on the **8 009 states the anchors actually request**, ρ differs in **96.6 %** with worst **1.382e-9** — in-grid (T ≥ 295 K) **1.018e-9** over 4 261 states, below-grid **1.382e-9** over 3 748. ⚠ *Both exceed the ≤ 1e-9 shown to the owner, by 1.8 % and 38 %*: that figure came from a sampled grid that never contained the requested states, and the sampled prior **8.83e-10** is kept as a prior of unknown coverage (owner informed; directing seat's ruling ⓐ). ⚠ **Tolerance chosen against measurement**: 1e-11 and 1e-12 buy 3.8 % and 4.1 % of deviation for 33 % and 64 % more iterations, because the floor is `pressure`'s own noise — it scales as 1/h with `_DRHO` (scratch diagnostic; `_DRHO` untouched). ⚠ **The control table is a regression guard, not evidence** — all six rows run **0** inversions; the evidence is the anchors (**11 922** inversions), the clamp states and the bands. **Time row, built on the measures that survive contention** — `engine/test_interior.py`, system python: **user 1397.02 s against 3035.75 s = 2.173×**, **instructions 36 080 978 560 797 against 84 228 340 582 316 = 2.334×**, and **gate-to-gate 3029 s (pool 2, old code) against 1360 s (pool 8, this commit) = 2.23×**. ⚠ **The standalone wall pair is discarded, not explained**: 1914.27 s against 3064.27 s would read 1.60×, but that new-tree run spent **517 s off-CPU** (1397.02 s user under a 1914.27 s wall) and sits **46 %** above what its own instruction count predicts — *a wall that disagrees with its own CPU measure is not a result*. The old-tree re-run's wall is discarded for the same reason and more plainly: **19 949 s wall against 3 035.75 s user**, the process suspended for most of the interval. ⚠ **The baseline reproduced to 0.05 %**: today's old-tree user 3035.75 s against last night's 3037.23 s at `3716708f`, and instructions to **0.061 %**. *Two thresholds, both measured today: a contended user-time difference under ≈5 % is not evidence, an uncontended repeat inside 0.1 % is a reproduction.* Against the pre-190 baseline the tree is **2.01× by instructions** (36.08e12 against 17.96e12). ⚠ **The registered aim ≤ 1.5 × 693.11 s is still missed** and is reported as measured, not as a gate. ⚠ **And the printed output did not move at all**: both trees' runs are **301 lines, byte-identical, `fd826ed6c9b39b30`** — the hash 190 B registered between `f681afbd` and `587842b3`, so `eos.py` and `ice_fr2015.py` together moved **no printed value** across 190, 190 B and 197. Draft `59cfabc8502582e0`, results `8ab94a06414b40b1`. ⚠ **190 C decides the domain: widen the bracket, do not refuse.** `density_at` now inverts over `[FIT_RHO_MIN, EXTRAP_RHO_MAX] = [1.6, 5.75] g/cm³` instead of the fit grid's `[1.6, 4.25]`, so above the grid the answer is an **extrapolation carrying a grade** rather than a wall value carrying a label that contradicts it. ⚠ **The number is read off the engine's own refusal, not rounded**: `eos.ICE_X_P_MAX` refuses by name at **1000 GPa**, where ρ is **5.7088 g/cm³ at 295 K · 5.6899 at 2000 K** (measured), so 5.75 covers both and stops just past it. **The clamp is therefore moved past the material's own refusal rather than narrowed** — it now fires at **1025.54 GPa at 295 K · 1037.17 GPa at 2000 K** (bisection on `STATS["clamped"]`), pressures at which `ice_x` has already refused, so no converging column reaches it. ⚠ **The lower edge stays at the grid floor on purpose**: P(ρ) at 2000 K is **not monotonic** below ρ ≈ 1.2 g/cm³ — 0.50 → 18.54 GPa, 0.80 → 14.33, 1.00 → 14.19, 1.20 → 15.11, 1.60 → 19.77 — and neither bisection nor a secant can promise a root where monotonicity is broken. **The two registered demonstration states now split**: `density_at(3.30, 2000.0)` is still **1.6** and still clamps, while `density_at(345.0, 295.0)` returns **4.259294311056466** instead of the wall — the wedge is inverted rather than pinned. ⚠ **The grid departure is counted and labelled, and the label's scope is the answer**: `thermal_at` counts **above** the memo, because a counter below the cache sees misses only and a winning attempt's request goes unseen whenever a discarded attempt already filled that cell; `integrate` is itself the counting wrapper, so **an uncounted call site cannot be spelled**; and `solve` reads **only the returned structure's** delta. *The search totals are deliberately not in the note (audit seat): attempt-side counts are not statements about the body, and at two to three orders larger they take the reader's eye first.* ⚠ **Two counter streams, and they must not be converted into each other**: `inversions`/`clamped`/`iterations` rise inside `density_at`, below the memo, and count inversions; `extrapolated_rho`/`below_t_min` rise inside `thermal_at`, above it, and count **askings** — which is why moving them there took the same solve's figures 271 → 542 and 1 721 → 3 442. *The `STATS` block's own comment still described the old placement and was corrected here — true when written, false after a change that did not touch it.* ⚠ **Values: 0 of 70 printed cells moved** across the six registered control bodies and both anchors, against baselines that themselves agree cell-for-cell with the pre-197 run — **four items have now rewritten the ice path and the anchors' printed values have not moved once**. The six control rows still run **0** inversions and remain a regression guard, not evidence. ⚠ **What the extension buys, measured on the `Uranus` anchor**: clamps **275 → 3** in the same **4 057** inversions (the three that remain are the **lower** wall, which 190 C did not move). `inversions` does not rise because `STATS["inversions"] += 1` sits **above** the entry guard — a pinned request was already an inversion, and the extension turns pinning into iterating. ⚠ **What it costs, measured and decomposed**: iterations **38 130 → 45 203 (+18.55 %)**, `free_energy` **92 488 → 106 634 (+15.29 %)**. Replaying the baseline's **own 4 057 requests** through both trees — identical members, so no stream is involved — gives **+7 221**, of which the 275 converted requests take **2 432 (8.84 each, *below* the 10.082 average: the old wall was expensive because the root was **outside** it, not because it was hard to find)** and the 3 782 never-clamped requests take **4 789 more (10.082 → 11.348 steps each, 66 % of the cost)**. *The replay reproduces the baseline's recorded totals exactly (38 130 · 275), which is also the first measurement of the purity premise 197 registered by argument.* **Stream drift is therefore −148 iterations, −2.05 % of the bracket effect and of the opposite sign** — C85's amplification measured in iterations, and benign. ⚠ *The in-solve split by the same classifier gives populations of 275/3 782 against 274/3 783, which proves the two trees do not ask the same requests and so cannot attribute the cost at all; an earlier reading of «26.0 iterations per converted request» divided a delta by the wrong population.* ⚠ **The label is demonstrated on a constructed input, because no roster body exercises it**: `solve(7.234, core_mass_fraction=0.0, ice_mass_fraction=1.0, potential_temperature=150.0)` — **not a roster body** — converges at centre **400.8 GPa** with `grade analog`, its answering integration asking **1 062** times above the ρ grid and **280** times below the T floor, and it clamps **0** times where `e0009cd6` would have pinned all **290 924** of its above-grid requests. ⚠ **The registered prediction, judged against the measurement rather than left implicit**: the six control bodies were predicted to carry the flag **0 of 6**, and they carry it **0 of 6** — all six run 0 inversions, so the prediction was cheap and is recorded as such. **No prediction was written for the anchors**, and their answering integrations read **`Uranus` (0, 0)** and **`Neptune` (0, 0)**, with the edges touched only by discarded attempts (`Uranus` 542 above the grid · 3 442 below the floor; `Neptune` 0 · 4 054). *Against a control of 0 across every registered row, the constructed body's **1 062 · 280** is what says the counters are wired at all* — without it the eight zeros would not distinguish «nothing leaves the grid» from «nothing is being counted». **Neither anchor carries the label**: both leave the answer-side counters at 0, and `Neptune`'s whole search never reaches the ρ edge. ⚠ **The gate at `86dfbc11` failed twice, and both failures were this item's own doing** — *the pre-registration named neither*. ① `test_ice_giant.py`'s path fingerprint moved `3bcb4d7334472eef` → `bfeb10cbb5800cca`, because making `integrate` the counting wrapper put new bytecode behind a watched name. ② `test_interior.py`'s ammonia-reach row went `static_ok` **False**, because `inspect.getsource(interior.integrate)` read the wrapper instead of the body; *its dynamic half never broke* (positive control 1, ice-giant firings 0). **Both are closed by `e080447f`** — `integrate.__wrapped__ = _integrate_raw` for ②, the re-pin for ① — and `PATH_FUNCTIONS` gains `_integrate_raw` in this commit so the body is watched again (C87). ⚠ **Times, pool 8, like with like**: `test_interior.py` **1 433 s** at this commit against 1 360 · 1 372 · 1 381 for 190 B · 198 · 198 B, and **1 408 s** at `e080447f` — all inside the ≈5 % contended band, *recorded and not called a slowdown*. **Gate wall 1 708 → 2 025 s (+18.6 %) at `e080447f`, and all of it is one step** — `check_contracts.py` **222 → 565 s**, while 64 of the other steps sit within ±8 s (audit seat). *That step reads nothing `e080447f` changed — a static check, no `inspect`, no anchor read — so the cause is machine-side and **unmeasured**.* Results `db634320feb8362b` |
| **C85** | a 1e-10 change in one density moves a printed temperature by 1e-5 within a step | **listed 2026-09-12 — candidate, not scheduled (owner)** | 197 measured it on the registered anchors: the first ice inversion of the `Uranus` solve gets **identical arguments** in both trees and returns ρ differing by **8.58e-11** relative, and the **next** request's temperature differs by **1.677e-05** — an amplification of **≈ 2 × 10⁵ in one step**. ⚠ **And the same solve absorbs it completely**: all five printed keys are identical at the end, on both anchors, so the path amplifies and re-absorbs. *Where it absorbs is not traced* — `SHOOT_TOL = 1e-8`, `T_TOL = 1e-6`, `T_SURFACE_TOL = 1e-3` bracket the figure and no measurement here names the absorbing step. ⚠ **The in-tree precedent is the warm-start experiment above the shooter**, reverted because «*할선의 경로가 바뀌어 수렴점이 마지막 비트에서 달라진다*» — 197 is the same mechanism entered from below. ⚠ *A synthetic case shows the amplification without the absorption*: on a constructed 14.5 M⊕ body (`core_mass_fraction` 0.10 · `ice_mass_fraction` 0.60 · `potential_temperature` 1600 K — **not a roster body, and not the Uranus anchor**) the same ρ band flips `applicable` True → False, the shooter ending at 1.84 % against its 0.1 % tolerance after 28 passes (one extension, inside the rule). *The mechanism is real and that demonstration is synthetic; both halves belong in the sentence.* **Owner, 2026-09-12: candidate, not scheduled** — its one near-term output is how far roster bodies sit from the 0.1 % edge. Evidence `197-secant-results.md` `8ab94a06414b40b1` |
| **C80** | the pool barrier waited without a deadline, so a lost worker produced no verdict at all | **built 2026-09-12 (195)** | The gate on `587842b3` sat at the barrier from 21:39 to 22:15 with **71 of 72 steps already finished** and reported none of it (`c80-evidence/gate-587842b3.hung.log`, `fa09ab5a7f278211`, 184312 B; the audit's row draft `bd247b4abda083bd`). `step_flush` ended in a bare `wait`, and bash 3.2 has neither `wait -n` nor a timeout, so C61's own `pool_incomplete` count — the exact diagnosis the hang needed — sat **behind** the wait and was unreachable in the failure it was written for. ⚠ **Two states, not one**: `test_dynamo_rocky` was **complete-undrained** (rc 0 and `.done` written at 21:39, never drained because `_pool_drain` runs only in the slot loop and once after `wait`), while `test_interior` was **dead** — its `.out` ends at the entry of the block that is most of the step, with no `.rc` and no `.done`. The barrier now polls and classifies from the spool: **drained** (no files) · **complete-undrained** (`.done` — drain it) · **dead** (`.pid` written, that process gone, no `.done`, `.out` still there — `[FAIL] pool_orphan <step>`). ⚠ **A dead worker needs no deadline**: its signature completes the moment its pid is gone, so it is named at the next poll. The single ceiling **4553 s** — this commit's gate's longest step `test_interior.py` **3035 s** × 1.5, @3716708f, 2026-09-12 — applies only to a worker that is **alive but silent**, so it is a **backstop, not a response time**. ⚠ **Two new lines of state, where the draft registered one**: `$!` was discarded at launch and is now written to `$_base.pid`, and the slot's step name is kept in parent memory (`eval`), because `pool_orphan <name>` cannot be printed from a flat `_pool_names` string. ⚠ **The FAIL says what is known** — «no verdict and no live worker», never «killed»: a clean exit through the spool-vanished guards leaves the same trace, and that night's `log show` over jetsam, memorystatus, killed and low-swap predicates returned **no lines at all**. ⚠ *A fifth state falls through unnamed on purpose* — `.pid` written, pid gone, no `.done`, **no `.out`** is the clean-exit shape, and it is counted by `pool_incomplete` rather than named. ⚠ **Two results, not one**: the full gate is the **no-regression half** and it is executed by the modified `check.sh`, so it can only say the healthy path still works; the **proof** is a scratch gate with an injected kill. ⚠ *The hung run's «21:18» stop time is downgraded*: it was read from the live spool's mtime, `cp` reset every mtime to the copy time, and `0025.out`'s content carries no timestamp — so the archive no longer holds it, and the surviving anchors are the `.out`'s last line and its counterpart in the completed re-run. ⚠ **What it does not do**: it does not explain why a worker vanishes, and it adds no per-step budget — there are none today and sixty-five call sites make that C81. The stale floor comment («`test_giant` only 311 s», against 284 s measured) is restamped with a sha and a date, carrying the rule that produced the staleness. Draft `f65801ec18e55fbd` → final `51d1ef02a9e08934` |
| **C81** | step budgets are prose, and the gate has none | **listed 2026-09-12 — candidate, tooling** | `step()` takes a name and a command; all **65** call sites pass exactly that, `$SECONDS` only measures, and `step_budget`/`STEP_BUDGET`/`expected_seconds` match nothing in the repo (audit seat, 2026-09-11, measured). So 195's barrier takes **one** ceiling for the whole pool, sized by the longest step, which is generous for every other step by construction. *Per-step budgets are the better design and a sixty-five-call-site item; 195 does not foreclose them* |
| **C83** | a docstring refusal claim with no `raise` beside it is outside every sweep we have | **listed 2026-09-12 — candidate, tooling** | `audit_note_docstring_claims.py` (`0cf2b7966948d82d`) catches a docstring that claims a **convergence criterion** the code lacks — C79's own defect. It cannot catch a docstring that claims a **refusal** the code lacks, because it keys on `convergence.note(…, None)` and a refusal claim has no note to key on. `ice_fr2015.thermal_at` said «밖에서는 거절한다» and refuses nothing (C82). ⚠ **The join that would work is the same shape**: a docstring containing «거절» or «refuse», in a function whose body has no `raise` and no refusal constructor. *Registered, not built — and the count of how many such claims exist is unmeasured* |
| **C84** | `ThermalSet` has a `t_max` and no `t_min`, so every set's lower temperature edge is prose | **built 2026-09-12 (198, schema) · floors declared 2026-09-13 (198 B)** | `ThermalSet` carries `t_max` and **no floor**: `covers_t` tests `t <= t_max` and **returns `True` when `t_max <= 0.0`**. Of the **eight runtime objects** — six `ThermalSet(...)` constructions in the source, but `_ice_vii_x_gamma_sets()` is called on both the `ice_vii` and the `ice_x` phase — four declare a ceiling — `FR2015_FIT_T_MAX` 2000 K twice and `DOROGOKUPETS_FIT_T_MAX` 6000 K twice — and **the two liquid-Fe sets declare no temperature bound at all**. Lower edges exist only where an evaluator checks its own (`water_hot.T_MIN`, `ammonia_table.T_MIN_K`); **`ice_fr2015` had none, and **48.1 % of the anchors' evaluator calls are served outside the paper's temperature grid** — 5 736 of 11 922 requests below 295 K, measured on the secant's request stream at `b4063a01` (work seat; the old inverter's stream gives the same count, and ⚠ *the same count is not the same requests — the two streams' inputs differ in 97.6 %*). ⚠ *An earlier printing of this row said that missing floor «is why C82 is reachable», which is false*: C82's clamp fires at both **grid edges** — `density_at(3.30, 2000.0)` at the ceiling and `density_at(345.0, 295.0)` at the floor — so a 295 K `t_min` would have prevented neither. C82 is a shape mismatch in `density_at`'s bracket; C84 is a missing edge in `covers_t`, and the evaluator path never consults `covers_t` at all**. *An earlier version of this row named a 4000 K figure that appears nowhere in `eos.py` or `fe_liquid.py`, called `fe_liquid.HCP.t_ref` a floor when it is a reference isotherm the code does read, and said no code reads a lower edge when two evaluators do — corrected by the audit seat before it was committed.* ⚠ **Schema landed `8e26093e`, floors declared in this commit.** ⚠ *So a set could be asked below the data that made it and answer without a grade*, which is the same asymmetry 187 Amendment 3 closed on the **upper** T edge and nobody closed on the lower. **190 C's domain declaration depended on this**, and the order held: the floors were declared first (198 B), so when 190 C widened the ρ bracket the lower temperature edge was already guarded — the unguarded edge was removed rather than moved. *190 C then made the departures countable, and on its positive control the T floor is asked below **280** times on the answering integration alone*. ⚠ *J5C's third check failed on its first run against the wrong expectation — two cells, where the tree has **four**, because `_ice_vii_x_gamma_sets()` is called on both the `ice_vii` and the `ice_x` phase. It was fixed by re-reading the object, not by relaxing the assertion.* **A test that fails against a wrong expectation is worth more than the case it was written for** — it corrects the writer's model, which the case it was aimed at cannot do |
| **C86** | the committed dependency-graph page is a generated file that no check regenerates or compares, so it drifts from `chain.yaml` in silence | **built 2026-09-14 (C86 + C86-2) — the page is regenerated and the gate now compares it** | `engine/chain-explorer.html` is produced by `engine/build_graph_page.py` from `chain.yaml` + `bindings.yaml` + `phase4/*.yaml`, and **no gate runs that generator** — `git grep build_graph_page` at `86dfbc11` returns prose mentions only. The committed page has not moved since **`0c494b05` (2026-09-09)** while `chain.yaml` changed in **six** commits since, 189 among them. A scratchpad regeneration at `86dfbc11` (audit seat; generator run outside the tree, no repo write) differs from the committed page by **205 edges against 210** and **1 230 lines** folded. ⚠ **Nothing asks whether the committed page matches the graph it says it renders** — `check_refs`'s live set is `{.py, .yaml, .md}` and skips `.html`; `check_contracts` reads `chain.yaml` and `bindings`, not the page; `scripts/check_build_freshness.py` looks at `docs/phase2`·`docs/phase3` html and `db/systems`, not `engine/`. *So the page is the one artifact in the tree that states it is the reference for the graph and is checked by nothing.* ⚠ **And regeneration alone does not fix a rename**: the old name `has_inner_core_solved` appears **2** times in the committed page and **2** times in the regenerated one — renaming removes it, regenerating does not. **C68 B therefore leaves the page alone** (its Amendment 2) and a separate regeneration commit carries the new names, because folding regeneration into the rename commit would carry six commits' worth of unrelated graph drift — five edges — into a rename. |
| **C87** | a guard that is keyed to a function's *name* goes blind the moment the body moves out from behind that name | **listed 2026-09-13 — candidate, tooling** | 190 C turned `interior.integrate` into a counting wrapper `(*args, **kw)` and moved the body to `_integrate_raw`. **Three separate guards read `interior.integrate` by name, and all three read the wrapper instead of the body** — with three different results. ① `engine/test_ice_giant.py`'s path fingerprint hashes `getattr(interior, name).__code__` for the **seven** names in `PATH_FUNCTIONS` (`solve`, `shoot`, `_shoot_pressure`, `_narrow_bracket`, `_surface_temperature_met`, `_stack`, `integrate`) plus **13** constants; the wrapper's bytecode is not the body's, so the fingerprint moved **`3bcb4d7334472eef` → `bfeb10cbb5800cca`** and the gate FAILed. ② The ammonia-reach row in `engine/test_interior.py` asks `inspect.getsource(interior.integrate)` for `def with_ices`, `with_rock(with_ices(mat))` and `MATERIALS["nh3"]`; the wrapper's source has none of the three, so `static_ok` went **False** and the gate FAILed — while the **dynamic** half of the same row passed unchanged (positive control 1, ice-giant firings 0). ③ The same `and` chain then asks `inspect.signature(interior.integrate).parameters["ammonia_mass_fraction"]`, which on a `(*args, **kw)` wrapper is a **`KeyError`**, not a `False` — it never ran only because the chain **short-circuited at ②**. ⚠ **So one mechanism change produced a FAIL, a second FAIL, and a latent exception, and the third was hidden by evaluation order rather than by being sound.** The two halves need different repairs: `functools.wraps(_integrate_raw)` restores ② and ③ because `getsource` and `signature` both follow `__wrapped__`, but **not** ①, which reads `__code__` directly and can only be answered by widening `PATH_FUNCTIONS` and re-pinning. *The general shape: every guard that names a module attribute is a guard on a binding, not on a body, and body extraction is invisible to it.* |
| **C88** | a snapshot that is re-frozen only when the path fingerprint moves goes stale exactly when a change is subtle | **built 2026-09-14 (C + D) — the trigger reads the inputs, the comparison reads all 21 keys** | `engine/ice_giant_anchor.json` was last written at **`f681afbd`** (189 commit 2, `frozen_at` **2026-09-11**, `path_fingerprint` **`3bcb4d7334472eef`**, python 3.9.6, `STEPS` 1500). **Thirteen commits** landed between that freeze and `86dfbc11`, **seven** of them touching `engine/eos.py` or `engine/ice_fr2015.py` (190, 190 B's two perf commits, 197, 198, 198 B, and 190 C itself) — and **the anchor was never re-frozen** at that point. ⚠ **Corrected 2026-09-14** — the snapshot *was* re-frozen on **2026-09-13 17:23** (`8e64ec5b`, `frozen_at 2026-09-13`, fingerprint `471a27fd0793ca5e`), so «re-freezes since `f681afbd`: none» no longer holds. ⚠ **And the gap reopened the same evening**: `engine/eos.py` changed in `b6040e98` (21:33) and `6a9b3622` (02:23) with the snapshot unmoved. **The defect is not that nobody re-freezes — it is that re-freezing is an event someone must remember**, which is what this item's repair removes. ⚠ **The rule was obeyed, and that is the finding**: the rule is «if you change a path function, `--refresh` in the same commit», the gate enforces it by comparing `path_fingerprint()` against the stored one, and none of those six pre-190 C commits changed a path function. **The fingerprint never moved, so nothing ever asked.** ⚠ **Meanwhile the file carried a false fact**: `values.bracket_invalid` reads `[]` for **both** bodies, but since 190 gave ice VII and ice X a French & Redmer set, `ice_fr2015.density_at` leaves its bracket **275 times in one `Uranus` solve** — the work seat re-solved the same anchor on an **`e0009cd6`** clone and printed `["ice_fr2015.density_at"]`, so the entry was **already true before 190 C**; 190 C's re-freeze is merely the first thing that caught up. ⚠ **And the same diff states the opposite fact too**: every other field — the four `BIT_KEYS`, the remaining **17** `values` keys, both **8-key** `standalone` blocks, `standalone_reproduces_solve`, `grade`, `regime`, `applicable`, `converged` — is **byte-identical** to the pre-190 snapshot. Five items rewrote the ice path and moved nothing in this file but the fingerprint, the date, two timings and that one list. ⚠ **The row is about the scope of the rule**: «path function» is a **subset** of «code that produces these values», so a field that other code writes sits outside the trigger. It is compounded on the reading side — the full-solve comparison checks **`BIT_KEYS` only, four of 21** (`engine/test_ice_giant.py`, the two `moved = [k for k in BIT_KEYS ...]` sites), and the other 17 plus both `standalone` blocks are **re-frozen without ever being compared**. *So this kind of staleness is never printed; it lives in the file silently until something else forces a refresh.* ⚠ **C87 and C88 are two faces of one root** (the audit): a name-keyed watch misses the body that left the name, and a snapshot refreshed only when that watch moves goes stale when it does **not**. ⚠ **The file's diff `f681afbd` → `86dfbc11` is empty** (the audit; the parallel seat re-ran it), so fix-up (a)'s re-freeze diff is read directly against the `f681afbd` freeze, and the `bracket_invalid` entry in it is **190's effect, not 190 C's**. |
| **C90** | the page that calls itself the ledger's mirror is a hand-copied list, and the first full comparison found it wrong in eleven places | **built 2026-09-14 — the generator reads the ledger** | `core_items_0912.py` prints a status chip for every C-number from an **`ITEMS` literal typed by hand** — it never opens `engine/interior-core.md`, and the only git call it makes is `rev-parse` on the sha it stamps in the masthead. ⚠ **So the sha in the header is what an operator typed, not evidence that the page read that ledger.** The first full comparison against the ledger's own cells ran on 2026-09-13 (audit seat, 293-commit walk) and found **eleven** disagreements in 85 rows, of **two different kinds**. ⚠ **Five are transcription flips** — C45 (`listed 2026-09-07` printed as built), C51 (`pre-registered … before the build` as built), C54 (`candidate, listed 2026-09-09` as built), C63 (`closed … as a named refusal` as blocked), C65 (`built 2026-09-11` as listed) — and *all five sit on cells the ledger has never changed*, so **re-running the generator would never have fixed them**; they were wrong when they were typed. **Six are losses in the fold**: the ledger's status vocabulary is **23 first words** and the page's is **seven**, and six rows lost half their meaning on the way — C46 · C50 · C57 said «closed, but something remains» and the `conditional` chip that means exactly that went unused, while C4 · C21 · C55 say «half closed, half open», ⚠ *which the seven words cannot express at all*. A further **three** rows (C86 · C87 · C88) were absent because the page was generated before the commit that added them. *The distinction matters for the repair*: staleness is fixed by regenerating, and neither of these kinds is. ⚠ **자동 분류의 한계**: the audit's classifier also raised **five false positives** — C18 · C48 · C52 · C56 · C62 — where prose words and negations (`no checker built`, `nothing built`, `re-open`, `open below`) read as status; ⚠ *those are a limit of the classifier, not defects of the table*, and the eleven above survived because all ten candidates were read by hand. |
| **C89** | the harness measures CPU time, context switches and page faults, and deletes them — it keeps only max RSS | **built 2026-09-13 — landed `38e54329`** | Both of `scripts/check.sh`'s step paths already run every step under **`/usr/bin/time -l`**. The pool path is `PYTHONDONTWRITEBYTECODE=1 /usr/bin/time -l bash -c '"$@" 2>&1' _ "$@" >"$_base.out" 2>"$_st"` and the serial path is `/usr/bin/time -l bash -c '"$@" 2>&3' _ "$@" 2>"$_tf"`. ⚠ **From that whole stat block exactly one number survives**: an `awk '/maximum resident set size/ {printf "%.0f", $1/1048576}'` feeds the `RSS … MB` field of the `[TIME]` line, and the stat file is then removed (`rm -f "$_tf"` at `:250` in the serial path, `rm -f "$_st" "$_base.out"` at `:229` in the pool path). **User and system CPU time, involuntary context switches and page faults are produced on every step of every gate and thrown away.** ⚠ **This cost a measurement today.** `check_contracts.py` ran **222 s** in the `86dfbc11` gate, **565 s** in the `e080447f` gate and **222 s** in the `8e64ec5b` gate, all three at RSS 52 MB, all three alone in a serial lane with no overlapping step. Four seats spent the afternoon narrowing the 565 s and killed five candidates, and the one number that separates the surviving classes — CPU ≈ wall means «worked slowly», CPU ≪ wall with large involuntary context switches means «contended», neither with a long wall means «waited on I/O» — **had been measured three times and deleted three times**. ⚠ ***The 565 s CPU figure is gone, and the code is what deleted it.*** *Distinction from C86–C88, which are the same family: those three describe a check that does not look. This one looks, and discards what it saw.* ⚠ **And the scope of what it would have told us is bounded**: `/usr/bin/time -l` reports the **wrapper process and its children only**, so `[COST]` can separate «worked slowly» from «waited on I/O» from «was descheduled» **for that step**, and says nothing about what other seats were running — *the same wall four seats hit today*. ⚠ **Built 2026-09-13 ((c)–(e))**: `[COST]` prints nine fields in both paths, and `exec` was added both to the two `/usr/bin/time -l bash -c` wrappers and at **49** compound `step` call sites (54 compound minus the 5 that already carried it), so the counters belong to the step rather than to a surviving shell. The field that is read is **`instr`** — `cycles` is printed and deliberately not interpreted, because `exec` fixed *who* is counted and not *what* the column is. ⚠ **Measured, and the first gate's answer is not zero**: of the 72 `[COST]` lines in the (e) gate **one** sits below 1e8 instructions retired — `engine/backflow.py` at **29 002 892 instr against 1.00 s of user time** with 821 involuntary context switches, which is precisely the «spent a second without doing a second's work» shape the line was added to show. The next gate (196 B, pool 2) printed **0 of 72** below that line. In neither did the dash for «this step has no instruction counter» appear. |
| **C91** | a solve calls `shoot` more than once, and which of the returned structures is the answer is decided by a match nobody prints | **listed 2026-09-13 — candidate** | The call count follows the path, not the body class: the node path runs **six**, `dante_fixture` runs **twenty-two**, a direct `solve` runs **one**. The six are not interchangeable — they alternate warm and cold in three pairs (`earth`'s `t_center` reads 3169.5267230925806 · 0.0 three times over). ⚠ **The answering structure is the one whose `t_center` equals that node's printed `core_temperature`, and nothing prints that match.** A first dump took **the last** call and so recorded `T = 0` for five of eight bodies; the reading placed on it — «the integrator produces no interior temperature profile for rocky bodies» — was false and **is withdrawn** (work seat's own defect and own withdrawal). The corrected dump `profiles-b6040e98-v2.csv` has **533** rows of which **123** carry `T = 0`, all inside the two bodies whose nodes print `core_temperature` 0.0 (`dante_fixture` 43 · `water` 80); an earlier **129** counted the file's own six header comment lines and is withdrawn too. `mars` also gains shell points 45 → 50 in the warm structure, a second mark that the first capture was the cold one. **What the other calls feed, and what they cost, is unmeasured**, and so is whether `core_temperature` 0.0 on those two bodies is design or gap. ⚠ **Census v2 names every caller, and the six are two callers rather than one loop** (work seat, 2026-09-14, a hook on `interior.shoot`): `earth` · `mars` · `pandora` run `interior_layers` **3** + `mass_radius_relation` → `interior_layers` **3**; `dante_fixture`'s twenty-two are the porosity search → `interior_layers` **20** + `mass_radius_relation` **2**. ⚠ **The `mass_radius_relation` share is the cold half** — those calls arrive with `t_pot` `None` and cost about **0.2 s** each against the warm calls' tens of seconds, so «warm and cold in three pairs» was two callers interleaving, not one loop alternating. The twenty narrow `phi0` (0.6 → 0.6 → 0.3 → 0.45). ⚠ **The cost sits in single solves, not in the repetition** — one call each for `GJ1214b` **67.2 s** · `Neptune` **62.2 s** · `Uranus` **41.1 s**, against `dante_fixture`'s twenty for **4.8 s total**: the body with the most calls is the cheapest of the four. ⚠ **And a first census could not have been extrapolated** — its hook replaced `interior.solve`, which `mass_radius.py`'s `from interior import … solve` had already bound by value, so it measured **3**, the `interior_layers` path alone. Filling the missing share by proportion would have written `dante_fixture` as **20** and dissolved its two `mass_radius_relation` calls into a ratio. *A partial instrument gives a number that looks complete.* |
| **C92** | a material that gains a phase silently re-points every `phases[0]` reader, and P33 B gave the two Fe–S binaries a second phase | **listed 2026-09-14 — candidate** | `engine/core_state.py` reads the fit it reports from `material.phases[0]` at **five** sites — `k0_flip_gpa`'s single-phase guard, the two `melt_ref` notes, the `melt_scale` test, the printed `k0`, and the `fit_state == "liquid"` test. Before P33 B each Fe–S binary had exactly one phase, so `phases[0]` and «the phase that covers the core pressure» were the same object. ⚠ **P33 B prepends the Balog low-pressure phase, so those five reads now land on the 1.5–19 GPa fit**: `phases[0].k0` moves from 100.167873788 GPa (13 wt %) and 72.614874943 GPa (19 wt %) to Balog's printed K₀T for **both**, so *the two binaries would print the same K₀*, and `k0_flip_gpa` returns `None` because its `len(material.phases) != 1` guard now fires. ⚠ **No shipped digit moves today** — measured: **0** composition presets select an `fe_s_*` core material, so no roster body reaches `core_state` with one, and the `c55_cells.py` table is bit-identical across the change. **It is a latent wrong-phase read, not a moved digit.** ⚠ **Its twin in `interior.solve` was repaired inside P33 B**, because there the re-pointing *removed a label that used to print* — an Fe–S core at centre pressure **48.83 GPa** printed **0** grade notes with `phases[0]` and **1** with the covering phase, both arms measured in one run. ⚠ **The five were left deliberately**: the obvious patch — select the phase covering the pressure — also re-points `silicate` (3 phases) and `h2o`, and `core_state.py`'s own comment records that a non-core material reaches that node in `test_core_state`; those are roster-reachable, so the change must be measured before it is made. *Same family as C87 (name-keyed guards blinded by extraction) and C88 (a snapshot refrozen only on fingerprint movement): **the reader's key stopped selecting what its sentence says.*** ⚠ **The repair, named so the row is actionable**: give `Material` an accessor returning **the phase that covers a given pressure**, and move `core_state`'s five reads onto it; `k0_flip_gpa` then replaces the covering phase instead of refusing on phase count. Acceptance is that the two binaries' `core_state` values return to their pre-P33 B digits **with the Balog phase present**, and — because the patch also touches `silicate` and `h2o` — that every roster-reachable body's values are shown bit-identical or their movement named; *that second half is why this is a row and not a clause.* ⚠ **`eos.py`'s own `phases[0]` is a different sentence**: there it means **the floor** (`rho0`, the under-versus-gap refusal) and stays correct when a phase is prepended, provided the prepended phase is the lowest. `core_state`'s reads mean **the fit that answers at the core**, a different phase the moment a material has two. ⚠ **Two readers, one index, two different sentences** — the repair must not be applied to both by pattern. |
| **C93** | a density fit answers below the pressure where its own phase exists, and nothing declares that floor | **listed 2026-09-14 — note, not a class row** | `fe_eps` is Seager+ 2007's Vinet fit to ε-Fe and its `Phase.p_min` is **0.0**, so it answers at **1 bar**, where hcp iron does not exist. ⚠ **Its thermal term vanishes there too** — 8 300.01 kg/m³ at 300 K against **8 300.00** at 10 030 K, so a 9 730 K difference moves the density by 0.01. *Measured while building P41's instrument control, where the table gave 7 270.57 at 1 bar / 1670 K and the band's top was our own fit, not a disagreement about iron.* ⚠ **Same shape as C84 on a different axis**: C84 was a thermal set with a temperature ceiling and no floor cell; this is the **pressure** axis, and the floor is absent even in prose. **Not a PALEOS finding** — the table asked the same question at the same place and made it visible. **What is missing is a statement of where the fit is valid**, not a correction to the fit. Note draft `75198b7ae1c4b8af`. ⚠ **The row, after the sources were opened**: **21 phase-based materials, 6 with first-phase `p_min` 0.** The enforcement path exists — `Material.phase_at` refuses below a first phase's floor with `under_reason` — ⚠ **and has nothing to enforce.** Of the six, ⚠ **five are correct or already documented**: `ice_ih` **is** the 1 bar solid; `antigorite`'s source measures from ambient **to 10 GPa** (Hilairet+ 2006); `mgsio3_en` is placed **below 10 GPa** by Seager+ 2007 — **a ceiling, not a floor**; `fe_prem`'s `join_note` already says the outer-core fit is used **from 1 bar** (Zeng+ 2016). ⚠ **`fe_eps`'s 0 is Seager's declared choice** — ε and α share K₀ and K₀′ within error, and the fit comes from data to 330 GPa. ⚠ **What is undeclared there is not a pressure floor but how many kelvin a cold fit means at zero pressure — the thermal-validity axis of C84.** ⚠ **Why this is a note**: the census found a pattern and the pattern was not a defect. **«No floor declared» and «no floor to declare» are different facts**, and only opening the four sources separated them — a row saying «six materials are missing a floor» would have sent someone to declare five floors that should not exist. |
| **C96** | a test nobody runs and a test that passes look the same in a report — `engine/test_paleos.py` is not a gate step | **closed 2026-09-15 — `5a7687dd`** | ㄱ's pre-registration (`a610ae6d`) registers no gate step, so the PALEOS test is built outside `scripts/check.sh` and runs only when a person calls it. ⚠ **The file says so itself** — «not in the gate ≠ passing in the gate» — but a docstring is not a schedule. Registering it needs its own pre-registration, and that registration has two things to settle beyond the step line: the cost is **0.008 s** for 14 lookups so the step is nearly free, and the step depends on **192 MB of tables that live outside the worktree** in the read-only paper cache, so the gate must decide whether a missing table is a skip with a name or a failure. *Name registered here; nothing built.* |
| **C94** | a line-number citation written with a space, and an anchor written with a backtick after the file name, are invisible to the check that exists to find them | **closed 2026-09-15 — `d301d433`** | `check_refs` counted citations only in the attached spelling, so a citation whose number is separated from its file name by a space passed the step that FAILs on the same citation written with the number against the name; and `ANCHOR`'s `FILE` has no backtick, so `` `file`@«…» `` was neither an anchor nor a line number — `interior-core.md`'s anchor count went **139 → 139** across a commit that claimed to add one. Both detectors are in, and **24 citations migrated in the same commit** (15 split line numbers · 8 malformed anchors · 1 kept verbatim at `engine/tools/README.md@«a backtick after the filename rather»`, outside SCAN, where this defect was already recorded once at `406 → 406`). **malformed 8 → 0 · anchors 560 → 581** (+21 = 13 newly parsed + 8 made visible) · `retired` 2 · `shared` 3. Editing `eos.py` pulled the C88 trigger, so the anchor re-freeze rode the same commit — four changed lines, **21 × 2 values unchanged**. ⚠ **And a shape worth its own line: this item was closed, published to the board and written into the night summary while having no ledger row at all — C95 the same.** *The generator catches an item whose Korean cells are empty; it cannot catch an item that is not in the list.* **Named C99.** |
| **C95** | the anchor's input trigger digests bytes, so a documentation edit and a code change are the same event to it | **listed 2026-09-15 — registered `929667c373eced02`, measurement only** | Of the two `eos.py` re-freezes this week, one (`02bb7a2a`) was a citation rewrite with no code change. Two cheap paths are named and replayed rather than built — a `__code__.co_code` chain and an AST digest with docstrings removed; ⚠ **both are blind to the citation rewrite, and the acceptance line requires the opposite direction too — a candidate that does not move across a commit that changed code is struck.** The item prints and decides nothing: the choice between byte digest, code-object digest and AST digest is an owner cell, because it is a judgement about what the anchor promises, not a measurement. |
| **C97** | a line number written after a comma, with no file name and no `doc` before it, is caught by none of the four cells | **closed 2026-09-16 — `fa9b679d` + `65b08151`** | The spelling is `` `:1148` `` following `` `:1146`, `` — the citation's own continuation. ⚠ **Its size depends on the net and both figures are recorded rather than one chosen: 81 occurrences in 19 files by one sweep, 47 in 17 by another.** Naming the item without settling the net is the honest form; the first thing the item does is fix the net and re-count. Not migrated by C94, deliberately. |
| **C98** | `engine/tools/*.md` is outside `check_refs`'s SCAN, so the checker never opens those files | **closed 2026-09-16 — `db9c5fd9`** | `SCAN` (`engine/check_refs.py@«SCAN = (("engine/chain.yaml",),»`) lists `engine/*.md` and `engine/tools/*.py` but no `engine/tools/*.md`, and `ROOT.glob`'s `*` does not cross `/`. ⚠ **Priced during C94 and deliberately not folded into it: 2 files (`README.md` · `adaptive-step-prereg.md`), newly caught anchors 2 · line-number citations 5 · code span 1 · malformed 0.** Those five line numbers are unmigrated citations, not the formatting defect C94 closed — a different fault in a file nobody scanned. |
| **C99** | the fit and the plain inversion straddle the density window — the fit 0.023 above in core mass fraction, the inversion 0.005 below | **open 2026-09-20 — observation only, no prescription** | ⚠ **The fit is 0.023 above the window and the inversion 0.005 below it, in core mass fraction; the window lies between them, and the nearer of the two is the path nobody was watching.** Everything below is that sentence with its sources. ⚠ **A fitted quantity cannot test itself.** The sulphur fit solves for the composition that puts Mars's core radius on the declared target, so a radius inside the window is the fit working, not a check passing. What is left to compare against is the normalised moment of inertia and the mean core density. ⚠ **The density misses.** At the declared target of 1845 km the declared fixing `box_ceiling` gives **6.7678 g cm⁻³** (S 15.5313 wt%, r 1841.5627 km, nmoi 0.3573337, six halvings) and the companion `box_floor` **6.7743** (S 20.5000 wt%, r 1840.9808 km, two halvings) — **+9.2 % to +9.3 % above Durán+ 2022's 6.0–6.2**, and above Stähler+ 2021's wider 5.7–6.3 as well, so C55's choice of which paper anchors the windows does not touch it. ⚠ **Source, because this pair has already been quoted wrong twice**: the two densities and the radii are read from the anchor the code loads — blob **`269649ff`**, `mars_sulphur_anchor.json` beside `interior.py`, frozen 2026-09-20 22:15 ⚠ *(the hash is the source; the path and the time are for a human, since a copy carries the same bytes under a different mtime — that is how this pair was misquoted)*; the sulphur figures and the halvings are the chain's own `[PASS]` lines from the run that ended 22:35. ⚠ **The artefact folder holds an older snapshot of that file** with a different target and no density column — reading it instead is how the first two quotations went wrong. ⚠ **Both fixings carry the same core mass fraction, 0.27604166666666663**, because the inversion's grid is quantised in steps of 1/192. The ratio of the two densities equals the cube of the ratio of the two radii to sixteen digits, so **the whole difference between them is the radius**: 4.97 wt% of sulphur separates the two fixings and moves the density by 0.095 %, about 0.019 % per wt%. **Sulphur is not the axis.** ⚠ **The axis is the mass fraction**, since the density is `cmf · M / (4/3 π r³)` and the fit has already consumed `r`. ⚠ **And the window lies between the two paths, not above both.** At this radius 6.0–6.2 needs cmf **0.244716–0.252873**; the fit lands on **53/192**, the plain inversion on **46/192**, and the only grid points inside the window are **47/192 and 48/192**. The fit is **+9.2 %** above the window and the inversion **−2.1 %** below it — **4.45 grid steps** separate the fit from the window's top. ⚠ *Quoting only the fit reads as «our answer is too dense» and sends the next reader to the materials; the fact here is that two paths straddle the window and neither is a materials distance away.* ⚠ **At fixed radius the density is linear in the fraction**, `rho = k · cmf` with **k = 24.5175 g cm⁻³ per unit cmf** taken from the anchor's own pair, which is the whole table: fit 0.27604 → **6.768**, window 6.0–6.2 → **0.24472–0.25288**, inversion 0.23958 → **5.874**. The inversion misses by **0.005** in cmf and the fit by **0.023** — *opposite sides, and the near miss is the one nobody was looking at*. ⚠ *A midpoint fraction of 0.25781 would print 6.321, just 0.12 above the window's top; noted because the owner asked, and **not adopted** — it is a number with no derivation behind it and it meets neither observation.* ⚠ *The candidate this points at next is the layered family rather than a different iron: a candidate, not a prescription.* ⚠ **This table does not reach that family.** Khan/Samuel's windows are **1650–1675 km and 6.5–6.65**, a different radius, and `k` is `M / (4/3 π r³)` — a different radius gives a different `k`. **Nothing here has been computed for it**, and carrying these numbers across would be the mistake this row already records twice. ⚠ *So the statement is about where the fit lands the mass fraction. The Fe–S equation of state is a candidate for why it lands there; it is not a candidate for the density directly, and neither are the light elements.* ⚠ *The companion row was fitted at two halvings, a sulphur resolution of about 3 wt%; its radius, density and nmoi are coarse and the 0.0064 g cm⁻³ between the two densities is not a physical difference.* ⚠ *For the record, not as an open cell: at this target `box_floor` needs S above the owner's 13–19 box, and the owner closed that by moving the declaration to `box_ceiling`.* |
| **C100** | the engine calls Mars's silicate base solid, so the layer the owner elected cannot form — and the reason is not a wrong number, it is that **composition never reaches the melting curve at all** | **closed 2026-09-22 — `2d8ca21c`, pushed 2026-09-23; split at the fit by owner decision, successor C103** | ⚠ **This plate's own numbers say it.** At Mars's core–mantle boundary the engine reaches **18.33 GPa · 1881 K**, reports `silicate_melt_fraction_max=0` and `basal_silicate_state=solid`, and so the apparent radius carries no layer and equals the iron-core radius (**1842 km**). The elected papers do not describe ordinary rock: Khan+ 2023 asks for a *"fully molten silicate layer overlying a smaller, denser"* core, and Samuel+ 2023 derives it from a magma ocean that *"solidified to form a basal layer **enriched in iron and heat-producing elements**"*. ⚠ **The blocker is one level deeper than «we cannot derive the enrichment».** `_silicate_melt_verdict` reads `rock_samples`, `potential_temperature` and `variant`, and `variant` comes from a `differentiated` boolean — **no composition enters**. `eos.py` states it about itself: composition changes the **liquidus** only, and the **solidus** uses the same expression for either composition. So the engine could not use an enrichment even if it were handed one. ⚠ **The correction itself is held, and was found by reading rather than assumed**: Samuel+ 2021 `:1377` prints *"the influence of iron on both the solidus and the liquidus is accounted for by subtracting the term: **6 (Fe_d − Fe_m)**"*, where `Fe_d` is the iron number **inside the basal layer** — the very quantity we could not derive. ⚠ **Quote it as «as quoted by Samuel+ 2021»**: the deriving paper (Elkins-Tanton 2008) is closed access, measured `is_oa: false`, so **the coefficient's own conditions are not in our hands** and are on the October list. ⚠ **Resolution, measured before it could surprise anyone**: the layer is **150 ± 15 km** but `rock_samples` are taken every twentieth integration step, ≈**34.3–39.3 km** for Mars, more than twice the tolerance. **Raising the step count is the wrong answer and that is a measurement, not an opinion** — the four integrator-bound gate steps cost **77.2e12 instr · 2 980 s**, doubling adds ≈**93 %** of the gate's wall clock, and the sample spacing would still be 18 km; it also drags an anchor re-freeze, since the step count sits inside `PATH_CONSTANTS`. **The answer is machinery that already runs**: `INTERPOLATE_LAYERS` is on, and engine/interior.py@«frac = (p - _lo_mat) / dp_step» splits a step at a material boundary by a fraction and moves the temperature to the same place — finer than one step, at no gate cost. ⚠ **And the melting curve can be called from there** — `silicate_solidus(p, variant)` and `silicate_melt_fraction(p, t, variant)` take plain scalars, `eos` is already imported, and `liquid_material(pp, tt)` is called **every step** as precedent. **What has to move is one line**: the composition label is worked out after the integration finishes, while its source `differentiated` is already an argument inside. ⚠ **This row declares the enrichment rather than fitting it, on purpose.** The owner rejected a user-typed composition on 2026-09-21 and that stands — the declaration is **scaffolding so the machinery can be judged before a fit is laid on it**, and **C103 removes it**, registered at the same time so the scaffold cannot become permanent. **Acceptance is therefore self-contained: declare an enrichment, and see whether a layer appears and at what thickness, with nothing fitted.** ⚠ **Not measured, and named as such**: moving the melting call from every twentieth step to every step is **twenty times the calls**; the per-call cost looks small beside the density-table interpolation each step already does, but **that is the shape of the arithmetic, not a measurement**, and the gate's cost lines are per step, so isolating it needs a run. ⚠ **Not observed either**: `molten` has never once fired — today's roster is `solid` 3, `off-curve` 1, `molten` **0**. This item switches on a branch nobody has seen run. |
| **C101** | PALEOS answered issue #4 and shipped v1.3.0 — ⚠ **this is not a label fix, it is a moved phase boundary in the pressure–temperature wedge rocky interiors actually use** | **built 2026-09-22** | ⚠ **The author confirmed our diagnosis verbatim** — *"Your diagnosis was right in every particular, and it matched what I found when I went digging, down to the row counts."* — and answered the question we had left open: the **high-resolution** iron table carries the same defect, **3 772 142 rows of 8 182 515**. MgSiO₃ and H₂O are clean at both resolutions. The generator is fixed at `13de516`, and ⚠ **the silent `.get` default became a raise** — the same disease this night kept counting, fixed upstream. ⚠ **The part that matters to us is the part we did not ask about.** Our v1.2.x tables are the April build; since then the γ→ε boundary was re-fitted to two Dorogokupets+ 2017 triple points (**7.3 GPa · 820 K** and **98.5 GPa · 3712 K**). Regenerating moves **0.128 % of grid points** (657 at 150 ppd, 10 503 at 600 ppd) from γ-fcc to ε-hcp, and **density there shifts by about 3.6 %**. The wedge is **≈7.5–98.5 GPa · 750–3700 K**; everything outside agrees to 1e-9. ⚠ **That wedge is where rocky interiors live, and this table is an *independent* check** — folding it into the layer plate would put two causes under one measurement. **Opening this row means**: take v1.3.0, verify the author's checksums (`paleos_iron_eos_table_pt.dat` `259a2267dcf58af3b2c4dd389105b597`, highres `80e2540b8239553d89d75e31714a4171`), **count how many of our comparison points fall inside the wedge**, and re-run the comparison. MgSiO₃ and H₂O checksums do not move. ⚠ **Ordered before C100 (owner, `37518948`)** — C100 fits a basal composition to an observation and **this comparison is the ruler that judges that fit**, so the ruler is set before anything is measured against it. **Successor: C100.** ⚠ **The docstring of `test_paleos.py` claimed this file was outside the gate, and the claim was read rather than checked — while **C96 already recorded the opposite**, `closed 2026-09-15 — `5a7687dd``, naming the day the step was registered. **Nothing new was learnt here: something written down was not read.** ⚠ **A second question opens with it: whether to read the phase column at all.** engine/paleos.py@«The iron table's phase column is never read» records why we do not — *"The iron table's phase column is **never read**. It carries `liquid` and `unknown` only — 236 651 rows of `unknown`, fully populated, names missing. **A label we cannot read must not decorate a value we print.**"* ⚠ **That is «could not», not «did not need to»**, and the fix removes the reason. Reading it **adds a check**: our own phase judgements — the iron fit dropping to `grade_kind="extrapolation"` above its printed 350 GPa / 6000 K range, for one — would gain an independent judgement to be held against. ⚠ **Reading is not adopting.** Using the column as a check and taking its phase as grounds for our values are two decisions; **this row opens only the first**. So the two columns of this table move differently: the **density values** stay what they were — a check we keep outside our own answers, so that an independent comparison is not contaminated by them — while the **phase column** goes from «unreadable, so unused» to «readable, use undecided». |
| **C102** | a frozen comparison walks the keys it froze, so a value that **appears** is invisible to it | **built 2026-09-22 — `f030fc97`** | ⚠ **Measured on this plate.** engine/test_ice_giant.py@«appeared = sorted(set(v) - set(keys))» takes `keys = _value_keys(rec)` — the keys of the **frozen record** — and both loops stay inside it: `moved` compares those keys, `missing` reports those that vanished. Nothing walks the other direction. The frozen files hold **22 keys** for Uranus and Neptune; this plate's `interior.solve` returns **24**, and the comparison printed `움직인 키 0` and passed. The anchor did go red, but for the **trigger digests** (`interior.py`'s code ruler and the sulphur anchor's byte ruler), not for the two new keys. ⚠ **A change that added keys without touching a watched file would have been silent.** ⚠ **This row does not say that appearing is a defect** — a node adding an output is ordinary, and several did this year. What it said was that **the appearance was not counted anywhere**, so nobody chose. The cheap end was one line — `set(v) - set(keys)`, counted and printed beside the existing two counts — and **printing is not judging**: whether a new key should stop a run is a separate decision, and this row does not take it. ⚠ **Built in `f030fc97`, and the gate has printed it** — the run on `8f61f619` carries `[기록 · C88] Uranus — 비교한 키 24 개 (그중 이름으로 박힌 것 4), 움직인 키 0 · 그중 넷 밖 0 · **답에만 있는 키 0**` and the same line for Neptune; the log is blob `1d14aecc`. The zero is the point: a line that only appears when something is wrong cannot be told from a line that stopped working. ⚠ **This row cited that line by number when it landed, and the citation checker refused it** — the rule it broke is the one this plate spent the morning paying for: a census note cited a line number in `interior.py` for `fit_sulphur_to_core_radius`, and by the time anyone followed it the function had moved seventy-three lines down. ⚠ **This sentence was itself written with those two numbers in it, and the checker counted them as a citation** — the warning against line numbers cannot be written in line numbers. **A row about a counter that goes stale was itself written in a form that goes stale.** |
| **C103** | the enrichment C100 declares has to come from somewhere, and fitting it is the only route the engine can walk today | **listed 2026-09-22 — predecessor C100** | ⚠ **This row exists so that C100's declaration cannot become the answer by neglect.** C100 hands the engine an iron number by hand; this one solves for it. ⚠ **The fit needs a target and a check, and they must be different quantities** — the sulphur fit is the recorded lesson, since it consumed the core radius and `core_radius_fraction` stopped being an independent test. **Two observations exist once C100 produces a thickness**: Khan+ 2023's **150 ± 15 km** (anchored at docs/phase3/_papers/2023Natur.622..718K.txt@«improves to 150 ± 15 km», where thickness, core density **6.65 ± 0.1 g cm⁻³** and core radius **1675 ± 30 km** sit in one sentence, so quoting one cannot drift from the others) and **`nmoi`**, the scored row that is red today at **−1.669 %** against a 1 % tolerance. **One knob, two observations: fit against one and the other stays an independent check.** ⚠ **Which one is the target is an owner cell, not a measurement** — aiming at the thickness closes today's red as a *check that passes*, aiming at `nmoi` closes it *by construction*, which is weaker evidence. A third option adds the core's mean density (**6.0–6.2 g cm⁻³**, not in `expected:` today, so the gate does not score it) so that two checks stand behind one fit; ⚠ **it may go red on the plate that adds it**. ⚠ **A defect this item must fix rather than inherit**: the sulphur fit takes its target from `core_plus_layer_radius_km` — the **apparent** boundary — and compares it against `core_radius_fraction`, the **iron core**. Today the layer is zero so the two coincide, measured on three bodies inside the printed resolution (Earth +0.06 km, Pandora +0.51, Mars +0.14). **The day the layer has a thickness those four comparison lines aim at one quantity and measure another.** ⚠ **Three claims of different strength, kept apart on purpose.** That the target and the ruler read **different keys** is *written in the code* — four comparison lines against one target expression. That the two values **agree today** is *measured* — three bodies, within 0.51 km. That they **must part once a thickness exists** *follows from a definition the refusal string itself prints*: apparent core radius = iron core + layer thickness. ⚠ **How far they part is a fourth question and nobody has measured it**, because `molten` has never fired. ⚠ *Recorded on 2026-09-21 in the layer census and repeated here because that record's line numbers have already rotted — `:3960` is now `:4033`, and the numerator was renamed.* ⚠ **How far the linear correction holds is unknown**, and the one paper that would say (Duncan+ 2018, the measured solidus of an iron-rich Martian composition to 25 GPa) is open access that this machine cannot fetch — the publisher answers HTTP 403. **It is a click, not a purchase**, and it is on the October list as such. |
| **C104** | the gate's lane chooser has two independent doors and both are closed, so every plate pays the full 54 minutes | **listed 2026-09-22 — measured on three attempts the same morning** | ⚠ **Door 1 — the safety net asks whether a full gate *passed* today, when for choosing a lane the question is whether the full layer *ran*.** `lane_decide.py` counts a day's full gates under four conditions — today, an END line, `lane=full`, and **`rc=0`** — and `:132` spells the last one out. ⚠ **A full run that reaches END has exercised every step; that one of them reported a **designed** red does not change what was covered.** ⚠ **And this is the unforeseen back side of the owner's 2026-09-21 decision**: while `recorded_disagreement` sat on Mars's `nmoi` row the red was invisible to `rc`, so the net worked; **counting that row in the verdict — which was the point — closes the door permanently until C100 lands.** *Measured, not predicted: three attempts on 2026-09-22 all fell to full.* ⚠ **Door 2 — `--targeted` maps changed paths to tests and gives up on the first path it cannot map.** This morning's gap was **`NOTICE`**, a file with no test, changed by C101 itself. **Non-code files therefore defeat the narrow lane even when every code path in the diff maps cleanly.** ⚠ **A third path was measured and found worthless**: `check.sh` hard-codes the artefact folder as the log directory, and its own comment predicts that a folder change freezes the net at full — but **pointing it at the real logs changes nothing, because the `rc=0` condition blocks independently.** *That is a measurement, and it is the reason the cheap-looking fix is not the fix.* ⚠ **The cost is not «54 minutes once».** Until `nmoi` closes, `--auto-lane` is permanently full; and any plate touching a document defeats `--targeted` as well. **Both doors have to open before a plate can be narrow, and they open in different places.** ⚠ **Neither is fixed here, and door 1's fix weakens a safety net** — separating «was the layer covered» from «did it pass» is the shape, but the net exists because «nothing else can be affected» has been wrong before. **This row names the two doors and measures the toll; it does not choose.** ⚠ *One overshoot noted while reading the mapping: `test_mars_sulphur.py` also names `ice_giant_anchor.json` in its docstring, so the mapping can select two tests where one would do. **Overshoot, not omission** — recorded so a later reader does not mistake it for a bug.* **Measured 2026-09-24 (parallel seat, replay of 15 plates 09-21–23):** opening both doors saves almost nothing on plates that change engine code — door 1 changes the automatic lane on 0 of 15 (every plate that day changed code), door 2 newly empties the targeted gap on 1 (`8f61f619`, `NOTICE`), and on `interior.py` plates the targeted set is 99.7 % of full by instr. **The 54 minutes belong to the physics tests, not to the lane chooser** — `test_mars_sulphur` · `test_interior_ocean` · `test_core_history` · `test_interior` carry 58.6 % of instr. Both doors are parked. **Decided instead: pool 2 → 4, longest steps first** — peak RSS of the top four together is 246 MB; predicted wall 54 → about 33 min, floored by `test_mars_sulphur` (≈ 1 140 s). Lands after this plate's gate, with one plate run at pool 2 and pool 4 on the same sha to compare. Lane doors: replayed on the 196c9189 log, gain ≈ 0 on code plates — dropped. Decided instead: pool 4 with the longest steps first (commit 4ba39795, spool re-check fix 11d27f47). Pool 4 measured 33.65 min vs 59.7 at pool 2 on the same chain, predicted 36.8 (the earlier estimate was 33). Same 76 steps, same PASS/FAIL sets outside the two anchor steps; total instr +0.001 % (137815.48 → 137816.90 G). |
| **C107** | moving Mars into the layered family does not make the layer form — and inside the owner's sulphur box the engine cannot reach that family's core at all | **closed 2026-09-23 — by measurement, nothing committed** | The owner asked whether our Mars lacks a molten basal layer because the physics says so or because we lack the tool. C100 answered «no layer» on a **1845 km** core; Samuel+ 2019 prints the layered (BML) family at **`R_c = 1650 ± 20 km`**, layer **`D_d = 165 ± 20 km`**. This row asks whether the test was run on the right body. **㉠ The core cannot be reached inside the box.** `fit_sulphur_to_core_radius` refuses with *«the axis does not bracket the target»*. The verdict is right and the stated reason is not: **the target lies outside the bracket, not outside the axis.** Across the whole axis the 1650 km crossing sits near **`S ≈ 29.97 wt%`** — ⚠ **a linear interpolation between measured points, not a measurement** — which is outside the owner's box (13–19) and **1.76×** the cosmochemical ceiling Samuel+ 2023 prints (`S 17 wt%`). **The composition does not hold; the tool is not the limit.** **㉡ A smaller core moves the base further from melting.** With sulphur **fixed at 30 wt%** (composition unphysical; only the depth at which a layer would sit is BML-like; structure solved directly, no fit) the core is **1646.82 km** and the basal silicate sits at **20.9 GPa · 1913 K · solid**, thickness **0.0 km**. Landed plate `S 15.53`: ≈1842 km · 18.3 GPa · 1881 K · **316.25 K** to the liquidus · **166.25 K** short even at the enrichment ceiling (`Fe_d = 100`, 490.92 K). Fixed `S 30`: 1646.82 km · 20.9 GPa · 1913 K · **360.61 K** · **210.61 K**. A smaller core puts the base deeper: pressure rises 18.3 → 20.9 GPa and temperature rises 32 K, but the liquidus rises more. **44.36 K further than the landed plate.** **«No layer» survives the family move and gets stronger — a stronger statement than C100's.** ⚠ **Retracted, at the claim:** a first report gave `159.56 K`, «6.69 K closer». **Those numbers came from the axis-end structure the failed fit returned (core `1923.96 km`, the core grown, not shrunk), and the direction was the opposite.** The failed fit's `nmoi` and core density were labelled as answers in the same report — they too belong to the 1923.96 km body. **㉢ This is still not the paper's geometry.** What was measured is a sulphur-30 plate with a 1646.82 km core. The paper sets a fully molten silicate layer on top of 1650 (apparent core `R_l = 1780 ± 20 km`); **we cannot build that structure, and building it is what the thermal-evolution item is for.** **Side result, an observation and not a measurement:** our Mars is declared in the **non-layered** family — core 1845 km (non-BML 1820 ± 10, BML 1650 ± 20; the BML apparent core 1780 ± 20 does not contain it either), core density **6.768** (BML 6470 ± 60 kg/m³: +3.6 %), CMB temperature 2000 K declared (BML 2760 ± 150). Changing family is the owner's call (Brief 174). **Deferred by the owner 2026-09-24:** the family question waits for plate 4 of the thermal-evolution item (the layered model of Samuel+ 2023 Fig. 1 g–l); until then Mars keeps its current declaration — core 1845 km, core density 6.768 g/cm³, CMB 2000 K. **Cost:** two fits 135.9 s · 136.9 s, an 11-point sweep 687 s, a 7-point measurement 472 s, one fixed plate 39.0 s. Preregistration `9ba31aa6`. **Added 2026-09-25 — owner: revisit after mixed-core declaration.** With a basal layer stacked in the structure (4050 kg/m³, core target 1845 − D_d km — assumes the apparent core + layer radius stays 1845 km; Samuel 2019 has R_l 1780 ± 20), the sulphur fit leaves the owner's box 13–19 wt% from below once the layer is thicker than the [25, 50] km cell (interpolated 36 km; converged at INFER_TOL 5e-7 against 5e-8 — prereg-structure-basal-layer addenda 4–5). The box and the layer declaration stay as they are. |
| **C108** | the sulphur fit's bracket straddles a turning point of the axis, so inside a narrow window it refuses a target that has two solutions | **listed 2026-09-23 — a defect of the ruler, not of the answer on record** | The axis, measured (core km against S wt%): ⚠ **conditions unrecorded and not reproducible — see C116** (re-run on this commit gives 13 → 1815.0656; the values below also depend on `INFER_TOL`). 0 → 1668.87 · 10 → 1773.96 · **13 → 1815.14 (bracket low)** · 15.5 → 1841.38 · 19 → 1883.75 · 20 → 1900.21 · 22 → 1920.08 · 23.5 → 1923.97 · 24.0 → 1936.21 · **24.5 → 1936.29** · **25.0 → 1923.96 (bracket high)** · 27 → 1898.38 · 28 → 1854.52 · 29 → 1769.85 · 30 → 1646.82. **Every point carries the same regime, `inferred_core_mass_fraction` — a smooth turn, not an equation-of-state branch change.** **The defect.** engine/interior.py@«SULPHUR_FIT_BRACKET = (0.13, 0.25)» is the bracket, and engine/interior.py@«if f_lo * f_hi > 0:» decides from the **two end signs only**. The peak (`S 24–24.5`) lies **inside** that bracket, so the monotone assumption the bisection rests on is already broken. **Where it shows — a false-refusal window.** A target between `at(0.25)` and the peak has **two** solutions inside the bracket, yet both ends sit on the same side of it, so the fit refuses. Measured window **`(1923.97, 1936.29) km`, width `12.32 km`** — ⚠ **a lower bound**: 24.0 and 24.5 differ by `0.08 km`, so the peak is not yet pinned. ⚠ **The refusal reads «the axis does not bracket the target», which a reader takes as «unreachable» — inside that window it is false.** **Our plate is not caught.** The 1845 km target sits **79 km** below the window, and `at(0.13) = 1815.14 < 1845 < 1923.96 = at(0.25)` changes sign exactly once: **`S 15.53` is the only solution inside the bracket, now on measured ends.** ⚠ **Right is not the same as sound** — it is right because the bracket's upper end happens to sit just past the peak; move the bracket and the same code gives a different answer. **Closing condition, one of two, chosen separately:** (1) confirm a single sign change inside the bracket (locate the peak first); or (2) narrow the refusal to «no solution found **inside this bracket**» so it stops claiming unreachability. **Not measured, and said so:** a second crossing of 1845 lies in `[28, 29]` — **fixed by the signs**; its value `≈28.11 wt%` is a linear interpolation. Outside the bracket and outside the cosmochemical ceiling, so it was not measured. ⚠ **«Not measured» is not «absent».** |
| **C109** | Earth's nmoi anchor is the polar C/MR², while the engine's spherical nmoi is a mean I/MR² | **listed 2026-09-24** | Earth's nmoi anchor 0.3307 is the polar C/MR² (Margot+ 2021 prints «C/M R2 = 0.3307», no uncertainty); the engine's spherical nmoi is a mean I/MR², about 0.001 lower for Earth — the anchor receives the polar number. Inside the anchor tol 0.01, so the gate cannot see it. Mars shows the same split at 0.8 % (polar 0.3662, mean 0.36340 — the board uses the mean), about half the size of C59's red (engine 0.3573 against the board's 0.3634, 1.7 %). Venus's 0.337 is also a precession C/MR², but with J2 4.5e-6 the split is negligible against its ±0.024. |
| **C110** | the Mars radiogenic declaration does not reach `c51_regimes` or `test_core_history` | **listed 2026-09-24** | The Mars declaration (Drilleau+ 2022, 14 ppb U · 54 ppb Th · 284 ppm K) does not reach two consumers: `tools/c51_regimes.py` and `test_core_history.py` build Mars's heat budget from `radiogenic.budget` with the default Earth set, so their Mars rows moved only with the constant swap and U 23 (× 1.020 = 21.75 / 21.32 on every row), not with Mars's own set. The node path (run.py) does use the declaration. Wiring the two to the declaration is open. |
| **C111** | `test_core_history`'s Nimmo line pins our numbers, not a reproduction of Nimmo+ 2004 Table 4 | **listed 2026-09-24** | test_core_history's Nimmo line pins our numbers rather than reproducing Nimmo+ 2004 Table 4 (PDF p. 10, printed 372): printed Tc 4155 K · Tm 1613 K · QC 9.0 TW · inner core age 1.10 Gyr; ours −151 · −27 K. The present mantle heat is Nimmo's printed product 23.4 TW, the decay history is our set. Whether to make it a comparison with a width, and why the core differs, is open. |
| **C113** | plate 2's mantle balance uses the whole silicate volume where the source defines the convective mantle | **listed 2026-09-25 · closed 2026-09-26 — sized on the source-form switch `5f430118`** | plate 2's mantle balance (2021 eq. 10) uses the whole silicate volume V_sil (lid and crust included) where the source defines Vm as «the volume of the convective mantle» (2021 published PDF p. 11). The choice was never registered (first written in 9f8e2c8c); plate 4 uses the convective volume as printed. Plate 2 and 2P verdicts are those of this mixed version — the size is not measured: the two volumes differ by about 1.9× in plate 2 (lid ≈ 530 km), but V enters both the inertia and the heating terms of eq. 10, so the ratio alone does not size the effect; it may exceed 2P's tightest margin (≈ 3 K). T2 keeps V_sil to prove bit reproduction; plates 2 and 2P are to be re-measured with the source's volume afterwards (prereg-thermal-v2 v2-31). **Closed 2026-09-26 (prereg-source-form-plates, frozen `d9d5af99`).** The layer stack carries a `source_volume` switch that puts the convective volume in eq. 10 as printed. Measured with that switch alone: **T_m moves −22 K** — larger than 2P's tightest margin (≈ 3 K), so the old 2/2P verdicts were verdicts of the mixed version, as this row warned. On the source form, plate 2S passes A0 at Λ 7–15. The frozen `samuel_run` keeps V_sil for bit reproduction; the source form is the switch, not a silent change. |
| **C114** | in layered plates the lid's heating is split without the basal layer while the mantle uses the layer-corrected heating | **listed 2026-09-25 · closed 2026-09-26 — sized on the source-form switch `5f430118`** | samuel_run splits the lid's heating from H_pm without the basal layer (heat_split(H_pm, V_cr, V_sil − V_cr)) even in layered plates, while the mantle balance and the quasi-steady comparison use the layer-corrected H′_m — two places in one plate use different heating. Unregistered; plates 4 and 4P verdicts carry it; size not measured. T2 preserves it for bit reproduction; re-measure in the source-form plates (prereg-thermal-v2 v2-32). **Closed 2026-09-26 (prereg-source-form-plates, frozen `d9d5af99`).** The `source_lid_heat` switch splits the lid's heating from the layer-corrected H′_m, so one plate uses one heating. Measured with that switch alone: **T_m moves +6.27 K**. With both switches, plate 4S passes A on the main plate at (4,10) (4,11) (5,11) (6,11) and on the uniform plate at (4,10) (4,11) (5,11). `samuel_run` keeps the old split for bit reproduction; `run` takes the lid heat from one place, `lid_heat()` (backlog #33, `ddaccc6e`). |
| **C115** | for Earth's fixed composition the structure solve's r_b jumps between T_pot 1683 and 1684 K, all points 1670–1692 K unconverged | **listed 2026-09-25 · closed 2026-09-26 — the periodic sawtooth is gone in both interventions; the leftover moves to C118** | for Earth's fixed composition, the structure solve's r_b (= cmb_temperature / T_pot) jumps between T_pot 1683 and 1684 K, 1.576106 → 1.574290 (relative −1.15e-3, against a smooth slope of +4.1e-5 per K on both sides), with the layer names and the ice fingerprint unchanged; every point from 1670 to 1692 K reports converged False (unconverged_solvers ['fe_liquid.volume_newton']). Cause unknown (guess: a discretisation point on the core side moves with T_pot). Found by the adaptive structure grid (prereg-structure-grid addendum 15); the grid now treats it as a break it will not interpolate across (addendum 16). The fix belongs to the solver/cleanup stage. **Added 2026-09-25 (parallel seat):** Earth's r_b also jumps in two steps from T_pot 1888 to 1890 K (−1.7e-4 · −9.4e-4, together −1.1e-3), with a small kink at 1884 K. Hypothesis under test: these jumps are C116's tolerance quantisation (their size is about twice `INFER_TOL` 5e-4) — Earth is being re-run at 1 K steps with 5e-4 and 5e-7. **Withdrawn 2026-09-25:** Earth uses a declared composition and never calls infer_composition, so INFER_TOL cannot cause its jumps. Now testing T_TOL 1e-6→1e-9 and STEPS 1500→3000 (grid addendum 19). **Added 2026-09-25 (parallel seat):** Wide scan 1650–1950 K (grid addendum 22): Earth's r_b is a sawtooth — 18 jumps about every 20 K, each about −1.04e-3 (1715 K: −7.8e-3). Changing STEPS 1500→3000 moves and resizes the jumps; T_TOL 1e-9 does not change them. Earth gets a 9-point uniform table as a stopgap until C115 is fixed. **Diagnosis 2026-09-25 (parallel seat; prereg-structure-grid addenda 29–34, blob `84066539`):** at Earth's STEPS 1500 each tooth sits at a one-step temperature discontinuity six steps below the surface (P ≈ 0.48 GPa, `mgsio3_en`). A diagnostic run (1650–1950 K at 1 K, scratch only) that replaces `Phase.density`'s thermal-pressure floor branch (p − P_th ≤ 0 → rho0) by the zero-pressure tangent's linear continuation removes all 18 teeth at ~19 K spacing and the 1714 K refusal (temperature-loop budget). The same run also changes the smooth slope, not only the teeth — the median 1 K step in r_b goes from +2.60e-5 to +4.50e-5 (1.7×), the share of a few surface steps' changed density; the tooth removal and the slope change are separate findings. The registered verdict is «report only» (teeth 20 → 2). The two teeth left (1713 · 1714 K) sit inside a 1700–1714 K hump (+7.6e-3 up · −7.8e-3 down) present in both the diagnostic and the original run — a separate structure, not tested; the hump is parked. The fix is not a code patch but, on the director's recommendation and pending the owner's decision, a surface lithosphere/crust layer declaration in the layer generalisation; until then Earth keeps its 9-point stopgap table and the floor branch is unchanged. **Owner decision 2026-09-25:** fix C115 first by declaring a surface lithosphere/crust layer in the layer generalisation; only if teeth remain, change the thermal-pressure floor branch. Until then the Earth 9-point provisional table stays and the floor code is unchanged. Acceptance test (to be fixed in the layer-generalisation prereg): re-measure the C115 wide window with the floor branch on (prereg-structure-grid addendum 35, blob `fa4fdd5b`). **Closed 2026-09-26 (owner-directed order: surface lithosphere first, floor branch only if that fails).** The periodic r_b sawtooth (18–25 teeth, ~14–19 K apart, ~−1.1e-3 each) disappears in both interventions — the floor branch switched off (prereg-structure-grid addenda 33–34: 18 teeth gone) and the expansion-side fix with the surface lithosphere (prereg-thermal-pressure-floor addendum 3, corrected by blob `ea76f70d`; against baseline 20 teeth and lid-only 25). The one tooth left (1712 K, −1.92e-5, 1/60 of the old size) sits inside the 1698–1714 K hump present in both runs — outside C115, moved to C118. Registered verdict: ‘report’ (between 0 and 20). |
| **C116** | C108's axis values carry no recorded conditions, and both the sulphur anchor and the C108 window depend on the composition inversion's tolerance | **listed 2026-09-25 · closed 2026-09-26 — `INFER_TOL` 5e-7, `ffab53a0` · `ece73d08`** | **What C108 printed cannot be reproduced.** C108's fifteen axis points (core km against S wt%, e.g. «13 → 1815.14 (bracket low)» · «24.5 → 1936.29» · «25.0 → 1923.96 (bracket high)») were measured by the work seat on 2026-09-23 03:2x (prereg-c107-layered-family-probe revision 5, «7 점 실측, 472 s»); the tree is not recorded — revision 5's «고친 판 `10dfcdf2`» is the blob of the pre-registration file itself, not a commit — and the measuring seat's script and arguments are not in this machine's session logs. Re-run on C108's own commit `c3f39e4c` with the declared inputs (T_pot 1600 K · `basal_iron_number` 75 · `box_ceiling`) and the engine's `INFER_TOL` 5e-4: S 13 → **1815.0656 km** (cmf 13/48), not 1815.14. **The cause of the scatter is the inversion's stopping rule.** `infer_composition` stops bisecting the core mass fraction once the planet radius is within `INFER_TOL` 5e-4 (relative, ≈ 1.7 km for Mars), so the fraction sits on bisection points (n/48, n/64, n/96 …) and the core radius moves in steps of ≈ 13 km (measured: the integration grid ×1 · ×2 · ×4 moves it ≤ 0.007 km; the stair stays). **Re-measured at 5e-4 / 5e-7 (D_d 0, same declarations):** S 0 → 1668.967 / 1668.291 · 10 → 1773.156 / 1779.153 · 13 → 1815.066 / 1815.630 · 15.5 → 1840.595 / **1846.572** · 19 → 1882.994 / 1888.826 · 20 → 1900.250 / 1899.965 · 22 → 1920.203 / 1919.207 · 23.5 → 1923.332 / 1928.478 · 24 → 1937.099 / 1929.876 · 24.5 → 1937.169 / **1930.016** · 25 → 1923.321 / 1928.590 · 27 → 1898.762 / 1895.540 · 28 → 1855.226 / 1849.553 · 29 → 1769.686 / 1770.876 · 30 → 1646.334 / 1649.576 km. **Two consequences.** (1) The frozen sulphur anchor S 15.53 wt% (fitted at 5e-4) sits on the quantisation — at S 15.5 the two tolerances differ by 5.98 km (1840.595 against 1846.572; the 5e-7 value alone, not checked at 5e-8, is above the 1845 km target); at a tight tolerance the solution lies near S ≈ 15.3 (not measured by a fit). (2) The axis peak moves from 1937.17 to 1930.02 km and C108's false-refusal window from (1923.97, 1936.29) to (1928.59, 1930.02) km (lower bound). **Not measured:** the fitted S at a tight tolerance; the convergence of the axis between 5e-7 and 5e-8 (only the basal-layer scan was checked there — prereg-structure-basal-layer addendum 4). **Closing condition:** a separate plate narrows the default `INFER_TOL` (pre-registered first: the value by a sign/anchor-stability rule set before results, cost in instr, every anchor and frozen hash it moves), and re-freezes the sulphur anchor there; the shipped number's move is reported to the owner at that landing. **Closed 2026-09-26 (prereg-infer-tol, frozen `5be20136`).** The ladder rule, fixed before results, picked **5e-7**: against 5e-8 every inversion body holds core radius within 0.0111 km, nmoi within 2.9e-7 and the Mars fit within 0.094 wt%, with regime, refusal and bracket signs the same for all 37 bodies. **Sulphur anchor (IT-sulphur):** box_ceiling S 15.5313 → **15.3438 wt%**, core 1841.56 → 1844.63 km, nmoi 0.357334 → 0.357080, mean core density 6.768 → 6.780 g/cm³; box_floor stays at S 20.5, core 1840.98 → 1845.71 km. **Ice-giant anchor (IT-ice):** value fields moved 0; only input hashes and seconds, frozen unloaded. **C108 axis at 5e-7 / 5e-8 (IT-C108, output blob `0ab8220a`):** the fifteen points differ by ≤ 0.007 km between the two tolerances; bracket ends 13 → 1815.630 / 1815.626 and 25 → 1928.590 / 1928.585 km straddle 1845 with one sign change at both; the peak sits at 24.5 → 1930.016 / 1930.020 km, so C108's false-refusal window is **(1928.59, 1930.02) km**, still a lower bound. **Roster (IT-roster):** of 34 measured rows, 29 solve at both tolerances and 5 are refused at both, with the same refusals; the largest core move is TRAPPIST-1 g, −14.06 km, and the largest nmoi move 0.0003. **Cost (IT-cost):** one Venus inversion 1.326e11 → 2.076e11 instructions (×1.57). |
| **C117** | the owner's external benchmark reports Earth, Venus and Pandora UNCONVERGED on the thermal path, from `fe_liquid.volume_newton` alone | **listed and closed 2026-09-26 — the flag is strict; the values are right** | **Measured** (prereg-fe-liquid-newton, frozen `e1bbe64c`; tool `tools/fe_newton_probe.py`; output blob `bcce64c0`). In `volume_at` Newton leaves through its **window exit** on most calls — Earth 198 723 of 203 894, Venus 7 392 828 of 7 960 628, Pandora 209 787 of 242 384 — all in the liquid-iron column at 129–835 GPa and 1989–3760 K; no other exit fails. Each time the 80-halving bisection takes over with its bracket valid (**0 false brackets**), and lands at \|P(v) − p\| ≤ 0.00085 Pa (Earth) · 0.0016 Pa (Venus) · 0.00067 Pa (Pandora), against the Newton criterion of 1 Pa. **Verdict rule, fixed before results:** tighten only the failed calls to 1e-3 Pa and re-solve; ‘strict flag’ if every body-file `tol` field moves by less than tol/100 and core_temperature by less than 0.22 K (1/100 of prereg-structure-coupling addendum 11's 22 K). **Result: 0 of 114 (Earth) · 52 (Venus) · 73 (Pandora) outputs move by a single bit** — ① strict flag for all three. The instrumented copy returns bit-identical outputs (P-0). ⚠ Venus has **1548 calls** (at 613–835 GPa, 2899–3468 K) where even a bisection run to machine precision stays at 0.0011–0.0016 Pa — the float spacing of v at that pressure — so 1e-3 Pa is not reachable there; the frozen fallback rule used that value, and no output moved. **What stays open:** the flag still reads UNCONVERGED on correct values. Changing the Newton start, window or flag rule is a separate plate; so are the benchmark's cost line (40–1000×, concentrated in this Newton) and the ice-giant C/MR² line. |
| **C118** | Earth's r_b has a 1698–1714 K hump, and the 1713 K point is refused by the temperature loop's budget | **listed 2026-09-26 — cause unknown; not parked, to look at after the layer generalization** | **The hump.** r_b rises **+7.55e-3** at 1698 → 1699 K with the surface lithosphere and the expansion-side fix (r_b 1.586047 → 1.598023; prereg-thermal-pressure-floor addendum 3 as corrected, blob `ea76f70d`), at 1699 → 1700 K without them (prereg-structure-grid addendum 34, blob `84066539`: «1700 → 1714 사이 r_b 가 +7.8e-3 오르고 −7.8e-3 내려오는 혹»). It comes back down by about the same size near 1713–1715 K: on the original run 1713 → 1715 K **−7.840e-3** (a 2 K cell, because 1714 K is refused; log `clamp-1650.log`), on the floor-off run 1713 **−2.64e-3** + 1714 **−5.12e-3** (sum −7.76e-3; `off-1650.log`) — the same size as addendum 22's «1715 K 만 −7.78e-3». ⚠ The lid + fix run refuses 1713 K, so it gives **no value** for the drop; its numbers are not used for it. **The refusal.** At 1713 K the temperature loop runs out of budget (deviation 0.33 % against 0.1 % allowed) in the lid + fix run. **Not measured:** the cause of either. The 1712 K tooth left by C115 (−1.92e-5) sits inside this hump. **Side task after landing:** re-register the adaptive Earth grid, since its old refusal sat on C115's sawtooth. |
| **C119** | a hot iron core below `fe_prem`'s spinodal refuses the body — GJ 1214 b's test fixture now refuses by name | **listed 2026-09-26 — owner decision: accept the refusal now; the fix goes with the core-composition stage** | With the expansion-side fix (prereg-thermal-pressure-floor, blob `e0462218`), the temperature bracket takes a spinodal refusal as an upper wall. For GJ 1214 b (8.41 M⊕ · cmf 0.3185 · H/He 2 % · 1 bar 300 K, `test_interior` fixture) the hottest centre temperature that binds the envelope is 7868 K, giving R 2.43 R⊕ and 160 K at 1 bar; above 7872 K `fe_prem`'s cold pressure falls below its spinodal (−37.167 against −37.145 GPa), so 300 K at 1 bar is not reached and the solve refuses by name (addenda 6–8). The old answer (R 2.733) used a silent `rho0` in that core. At those conditions `fe_prem`'s thermal pressure is 412 GPa at 7868 K and 546 GPa at 9000 K, and core iron there is liquid; `fe_liquid.volume_at` (Dorogokupets 2017 liquid column) gives 9.7–15.4 g/cm³ at 132–600 GPa (at 35 GPa it returns the same 4678.4 at both temperatures — not chased). **Owner decision 2026-09-26 («2. A»):** accept the refusal; the fixture now expects it. The fix — a hot core read as liquid iron — goes with the `fe_liquid` density-path decision (A) (2026-09-11, owner review pending), in the layer generalisation's core-composition stage (ⓒ). |

⚠ **C23 does not say "closed", and the wording is deliberate.** The existence gate is built and judges;
the **field strength is not available and this item cannot produce it** — Tang's 37 pages contain
*magnetic moment*, *field strength* and *Gauss* zero times. A title reading "closed" would be read as
"a sub-Neptune's field can now be emitted", which is false. Aurorae, magnetosphere size and every
other visual axis stay shut until something else opens them.

**Keeping this file alive.** C2 was stale within a day of being written. So each brief's
Landing section carries one checkbox — *update the matching row in `interior-core.md`* — and
a row is not closed by the work being done but by that line being written here.

**Prose that carries a number carries the duty to update it.** Notes, domain rows, tables —
wherever a number sits, when the code moves that number the same commit either fixes it or
dates it *interim, superseded <date>*. Three times a note fell behind the code (C2 within a
day; the domain row that stated Neptune's "1797 K, three kelvin under the floor" as fact; the
H/He note's Saturn +2.09 % after the gas-layer temperature carry moved it to +7.06 %), and
the rule above only covered core rows.

**Labels are re-checked at their place in the text, not only the constants.** When a
transcription is verified against a source, the equation number itself is confirmed to sit
where the text puts it. Constants that are right hide a wrong label, and the next reader who
follows the label opens the wrong equation — the same failure as a fabricated DOI that
resolves to a real, unrelated paper: the form is plausible, so it passes. (C8 wrote Noack &
Lasbleis's R_p scaling as their eq. (8); it is their eq. (5), and (8) is X_CMF. The constants
were right, eight labels were not.) **And when one file carries two papers, the same number
can exist twice, so a label is written with the paper's name** — `Noack & Lasbleis eq. 5`,
never a bare `eq. 8` — which is how `test_interior.py` came to hold Unterborn's real eq. 8
beside a mislabelled Noack & Lasbleis eq. 8 without either looking wrong. That is the fourth
kind of plausible-because-well-formed failure this list has met, after the fabricated
identifier, the stale number and the label slip: the same number from a different paper.

**When a source is baked, its claimed range is swept against physical criteria registered
in advance, and the effective ceiling is measured and recorded with the table.** A label can
be verified faithfully at its place in the source and the source's own claim can still
break in execution — the fifth kind of plausible-because-well-formed failure. SeaFreeze's
`water2` (water2 item, 2026-08-30) carries knots to 100 GPa and AQUA quotes that as its
range, and the spline returns negative densities inside it; the effective ceiling (2.3 GPa
at 360 K rising to 30 GPa at 1000 K) was found by a sweep whose criteria — ρ finite and
rising with P, 1000 < c_P < 15 000 J/kg/K, dT/dP|_S > 0, no runaway in successive density
increments, two cells of margin — were fixed *before* the sweep, so the ceiling could not
drift to wherever the results looked odd. **Pre-registration is the point**: without it,
"as far as it looks fine" is an impression, not a verdict. `fermi.py`, `hhe_table.py` and
`ammonia_table.py` already meet this in their own ways; it is stated here so the next baked
table does too.

**Relays without verification, in both directions.** *Downward*: a number without its label
does not enter a brief. *Upward*: **a number that changes a verdict is reproduced by the
directing session before it goes to the audit.** Verdict-changing, specified in advance so
it is not judged by impression: (a) a number that opens, closes or reopens a row; (b) **a
first claim that a published value is contained or reproduced**; (c) a number that moves an
anchor; (d) a number that changes a grade. The directing session's reproduction does **not**
replace the audit's: a verdict-changing number is computed by the working session,
reproduced by the directing session, and reproduced again by the audit. The five failures
that produced these two sentences are one disease in two directions — four unlabelled
numbers travelling down into briefs, and one headline (C11's "Titan is inside a declared
band", 2026-08-30) travelling up without reproduction; the rule above stops the first and
this one the second.

**The disease is independent of role.** On 2026-08-30 it fired once in each of the three
sessions: the directing session put unlabelled numbers into briefs (four times); the working
session wrote a gate time it had not measured; the audit session joined the triple point's
pressure (14.6 GPa) to an isotherm's temperature (905 K) into one pair and took it for a
melting point (Queyroux+ 2020 — the pressure belongs to 14.6(5) GPa · 850(20) K, the
temperature to an isotherm whose melting pressure the Letter does not print). What stops it
is not the role but the label and the prior reading — and the procedure held: the audit had
fenced its own suggestion with "read first · do not quote · direction only", so the mistaken
pair was read before it was used and never reached a verdict. An error occurred and the
procedure caught it; "it passed the audit" is not a reason to skip the reading.

**False provenance — the label is present and false.** Registered as sub-kind 7 by the
audit, and worse than a missing label, because **a label stops verification**: a reader who sees "the
value you gave me" checks nothing. (2026-08-31: a relay message attributed Neptune's J₂ as
3538.0×10⁻⁶ "from your message" — the message had carried only (2/3)J₂ and the source name;
the digits were filled from memory and labeled as received. NH22 Table 1 prints 3535.94.)
This is **the only sub-kind whose check lives in someone else's hands**: a fabricated
identifier is caught by holding the title against the original, but a false attribution is
caught only when **the attributed party compares it with what they actually sent**. The
prescription is therefore a pair — *sender*: quote only what sits inside quotation marks;
never fill in a number the other party did not say and label it "yours"; a filled value is
marked "filled by me". *Receiver*: a number someone attributes to you is compared against
what you actually sent before it is accepted. And the verification is **exhaustive, not
sampled**: in the case that named this, the same message's Uranus J₂ (3510.7) happened to
be right, so a spot-check would have passed both. Scope, stated precisely: the error lived
only in the relay message; the notes' printed values (3510.68 / 3535.94) were correct.

**A third party checks a solver by closure, not by A/B against a harness whose brackets it
does not own.** Registered 2026-09-01 by the audit, against its own instrument. Verifying the
region-3 Newton inversion, its first two bisection harnesses reported a worst disagreement of
**0.4** — and both were the harness's fault: the first bisected globally across a
non-monotonic stretch below T_c, the second used a lower bracket of 50 kg/m³ while the hot
low-pressure root sat at 34.3. At the worst point the audit evaluated **p(ρ_Newton) = 17.0 MPa
against p(ρ_bisection) = 24.3** and judged, on the spot, that **Newton was right and the
instrument was wrong**. It then changed the final check from A/B to **root reproduction** —
does the returned density close the equation it was inverting — and got worst **8.6e-13**.
The general form: an A/B against the previous implementation is the *implementer's* check,
because they know the old brackets; **an outside leg's check should be one that cannot inherit
the old method's assumptions**, and a closure test is that. A verification harness is code, and
code that disagrees with the thing it verifies is a suspect, not a verdict.

**An unreachable boundary condition should close as a named refusal, not as a failure to
converge.** Proposed by the audit 2026-09-01 and recorded here as the ice axis's settling path.
The four ends of Brief 23/25 are currently `conv=False`, which reads as *"the solver could not
do it"* — but the measurement says something stronger and more specific: **no central
temperature reaches a 76 K surface, because the `h_he` table has no state below ~1830 K at
130 GPa.** That is the same kind of statement every material ceiling in C6 makes, and this
list's standard is that a refusal names its mechanism and its citation. Once the controller can
*conclude* rather than cycle (the second defect above), these ends stop being an unfinished
measurement and become a **recorded refusal with coordinates** — which is a closeable state,
where "did not converge" is not.

**A sentinel carried in a variable something else re-arms is not a contract.** Registered
2026-09-01 from the temperature loop's non-termination. The loop meant to extend its pass
budget **once**: on running out it set `bracketed = "extended"` and checked for that sentinel
before extending again. But the deviation test re-armed `bracketed = True` on every pass that
failed to contract, overwriting the sentinel, so *"one more set, only once"* re-fired every
time the budget hit zero. A converged attempt was measured at **51 attempts against an
intended ceiling of 29** (1 + 14 + 14). The repair is five lines: a dedicated `extended` flag
that nothing else writes. **State that encodes a promise gets its own variable** — a value
doing double duty is a promise anyone downstream can silently revoke.

**And it is the cold flank again, in a new form: the climb hid the wall from the controller.**
The four members registered on 2026-08-31 were trial refusals *killing* a solve. This one is
the opposite failure with the same cause — the temperature loop lowers by ratio, meets a
too-cold refusal at 130–152 GPa (the H/He envelope's base), and the attempt's internal climb
(×1.6) carries it back up to the same ~360 K surface, so **the controller never learns that
its target is unreachable from below** and cycles forever instead of refusing by name. A wall
that a trial path climbs away from is a wall the answer never gets told about. Brief 22 taught
trial refusals to steer the bracket; this says the steering must also be able to **conclude**.
It was invisible before region 3 was baked, because every trial died in the steam wedge first —
which is why the earlier four-end measurement finished in 195–246 s.

**A process listing is an instant, not a state — and a serial chain is invisible between its
steps.** Registered 2026-08-31 by the directing seat, against itself. After the work session
was compacted, this seat ran `ps` for `python|check.sh`, saw nothing, and reported *"the run
never started"* as measured fact. The chain was alive — started 22:27 — and the work session,
trusting that report, launched an identical chain at 22:53; **two copies of the same solve ran
at once on a machine whose owner had spent the day fighting thermal throttling.** The `ps` was
not wrong about its instant: a chain that runs its steps sequentially shows **no matching
process in the gap between two steps**, and a single sample lands in that gap often enough to
be useless. The same seat had, an hour earlier, used `ps` correctly to find two 31-hour ghost
processes — which is exactly why the second reading felt authoritative.

The prescription is a pair, and it mirrors sub-kind 7's. *Reporting*: process state is
reported with its sampling — "no match in one `ps` at 22:5x", never "it never started" — and
liveness is established from something durable (the task's own output file growing, a
timestamped log, the launching session's own record), not from absence in one listing.
*Receiving*: **a session about to re-launch work checks for itself before starting**, however
the report reads; the cost of a duplicate heavy run is paid in someone's battery and fan, and
the check costs a second. The work session drew that conclusion unprompted and it is the right
one.

**A runtime estimate belongs to the code state it was measured on.** Same event, second
lesson. The "~15 minutes" this seat put in a brief was measured on the four ice-axis ends
before region 3 existed, when every path stopped early at the wall. With the wall filled the
paths integrate all the way, and the first solve passed **two hours of CPU** without printing.
The number was honest when taken and false when quoted, because the thing it measured had been
replaced in between — so a timing carried into a brief carries the commit it was taken on, or
it is not carried.

**A number whose source was not stated is quoted without one — you do not supply the
provenance.** The receiving half of the rule above, registered 2026-08-31 by the work session
against itself. The brief said only *"about 15 minutes"*; the checklist and the commit message
that quoted it wrote *"measured on the runs that died in 1 s at the wall"* — a provenance
inferred from the diagnostic story around it and then written as fact. The figure was in fact
measured on the directing seat's four full integrations (195 / 246 / 213 / 212 s, all
`conv=False`, on paths that stopped early at the wall). Nothing downstream moved, and the
sub-kind is still worth its line, because **an invented source is harder to catch than a
missing one**: a reader who sees a provenance stops looking for it — the same mechanism as
sub-kind 7, arriving from the other direction. The correction was made in place with a
correction commit rather than by rewriting an already-quoted hash.

**A new number is carried back to the old ones before it is used to clear them.** Registered
2026-08-31 by the parallel session, against itself, and it is its own kind because nothing was
misread: having established that the ice ladder's data ceiling is ~355 GPa, it wrote that
"every anchor sits far below 355 GPa" — while the ice giants' mantles reach 820 and 1016 GPa,
a table it had read that same morning. The anchors *are* safe, for a different reason
(`ICE_VII_X_T_MAX` = 1800 K, above which Mazevet carries the column), so the conclusion held
and **the condition was inverted**: not "safe below 355 GPa" but "safe above 1800 K", which
sends the next reader looking for danger in exactly the wrong place. The others in this list
are failures of reading; this one is a failure of *re-reading* — a new measurement obsoletes
the safety statements standing around it, and clearing them requires opening them again, not
recalling them. The check is cheap and its absence is invisible, which is why it is written
down.

**A correction request is itself a labelled claim, and it is opened before it is sent.**
Registered 2026-08-31 by the audit, against itself. Reviewing the directing seat's handoff,
it asked that C13's 26 % / 41 % be marked as standing on two of three legs, with the work
session's reproduction and two caveats outstanding — and wrote *"`19360f72` already records
the row as revisited"* while never opening `19360f72`, whose checklist closes all three and
whose §6 table reproduces the audit's own float-residual point to the digit. The correction
was withdrawn the same hour. Two known sub-kinds combined: a number left stale (2), resting
on an identifier cited but not read (the shadow of 1). What makes it worth its own line is
the direction — **the list was ahead of the ledger, not behind it**, so "the row closed
before verification did" was the exact inverse of what happened, and a correction accepted
on its face would have re-opened a settled row. Hence the pair: *sender* — the moment you
write "X already says so", X is a document you have opened, exhaustively, not by title;
*receiver* — **a correction is reproduced before it is applied**, the same duty as a number
attributed to you. The incoming seat reproduced it and it did not survive, which is the
only reason this is a recorded lesson rather than a re-opened row.

**A retrial's outcomes are registered before it runs, and the register now has five kinds:**
sits with A · sits with B · between · the source does not reach the deciding region (added
after F1) · **the source disagrees with both candidates** (added after F4, where Queyroux sat
above IAPWS and Reinhardt alike) — in which no reopening condition fires, the band's question
is rewritten from "which one" to "how wrong are both", and the grade keeps its word while its
reason changes. Two unregistered results in a row meant the list was young; every retrial
brief now carries all five.

**A discriminating test states, beside each prediction, the assumption that prediction
stands on, and its register includes the default ending "every prediction misses = the test
itself failed; the product is the name of the wrong assumption."** Born in C12 (2026-08-31):
the test's (나) prediction — "our water lands on the printed density" — carried the unspoken
assumption that the water-only profile's material is pure water, forgetting the H/He of a
three-layer model's inner envelope; when every prediction missed by 18–32 %, the result was
not a reading chosen but an assumption exposed. This is a rule about the tool, not about the
evidence: the outcome register classifies what the evidence did; this classifies what the
test could not do.

**A trial-path refusal steers the bracket; it does not kill the solve.** The refusal
machinery exists to keep the **answer** honest — every material stops where its evidence
stops (C6) — but the shoot and temperature loops route their *trials* through the same
refusals, so a solve could die in a state no converged answer would occupy. Repeated
sightings in two days (C11's over-broad refusal · the Queyroux–Neptune route death ·
C13 end B's stack-build death, sharpened by the 1 ULP that separated a 1 s refusal from a
112 s convergence) made it structure, and Brief 22 (2026-08-31) repaired the corridor's
three static spots: the centre seed dispatches fluid/solid like a step; the pressure
bracket's ceiling respects the dispatch (a hot centre is the fluid's, whose fit states no
pressure cap — a **cold** watery centre still stops at the ladder's 1 TPa by name); and
the fluid↔solid **availability seam** at exactly that cap — which the in-step boundary
finder can land a trial on — throws too_cold with the local temperature instead of a
temperatureless cap refusal the shoot would mis-read as geometry. Acceptance was
pre-registered and measured: end B solves with no stub under either `imf` expression, and
the Queyroux-window Neptune converges to the anchor's own solution. The distinction to
keep: **evidence caps are real for answers** (the cold refusal survives, tested), **and
representational for trials**. `engine/cold-flank-context-notes.md`.

**A table is regenerated on the code that ships, in the commit that ships it — and when the
regeneration differs, which side is right is settled by a separate trace.** The sub-kind's
name ("the table ran ahead of the code inside one commit") invites doubting the table first;
in the case that named it (C11, 2026-08-30) the table was right and the code had regressed —
an over-broad refusal written after the table removed a converged member. Regenerate, diff,
then trace; do not correct the table to the code, or the code to the table, on the name alone.

## Where the line is

Not by body class — by **what is missing**.

**In:** the missing thing is a material, a structure, a declaration, or a wire. The recipe
can reach it.

**Out:** the missing thing is physics the hydrostatic integration does not contain, or a
node that already exists elsewhere.

| out of scope | why |
|---|---|
| brown dwarf | deuterium burning above ~13 M_J puts an energy source inside the body. Not an input this recipe lacks — a term the equations do not have |
| star | the stellar C/MR² is the n = 3/2 polytrope value 0.205 (Chandrasekhar 1939), already on a separate `body_figure` branch |
| evolution and cooling tracks | age-dependent envelope thickness and luminosity belong to `internal_heat_nontidal` and to nodes not yet written |
| gate economics | the gate ran 14:12 → 14:22 → 17:44 and the cost was twice *recorded, not repaid*. Not solver physics — but it belongs on **a maintenance list of its own**, written down here only so it cannot fall between the two. Two small fixes ride with it: the conditional `_LAST_INVERSE` line, and a double-cut test for a thin layer |

**Sub-Neptunes are in.** What they lack is a gas mass fraction, which age and irradiation
set — an *input*, not physics. This recipe already takes six such inputs by declaration and
drops its grade for each: `ice_allowed`, `tidal_heating`, `initial_porosity`, `envelope_z`,
`potential_temperature`, `core_cmb_temperature`. A seventh is the same move, not a new
standard.

## The list

Closed entries were moved, byte for byte and in their original order, to [`interior-core-closed.md`](interior-core-closed.md) on 2026-09-23. Their rows stay in the table above.

### C4 — Ammonia and methane — **closed 2026-08-30, unbuilt; reopened 2026-08-30 for ammonia and closed again for that half, built**

The ice-giant envelope is water alone, standing in for a water–ammonia–methane mixture. That
is the field's own convention, but it is a stated substitution and **its price is not
quantified** — not bounded, not estimated. Bethkenhagen+ 2017's 2.1 % is the deviation from
*mixing three components you already have*, not the cost of replacing two of them with the
third; `eos.py` states the distinction correctly. The number only comes into existence when
the tables do, and the tables cannot be reached from here. Three routes, checked on
2026-08-27 and again on 2026-08-30:

| route | why it fails |
|---|---|
| Bethkenhagen+ 2017 (2017ApJ...848...67B, full text in the cache) | describes the grid exactly — 1000 GPa · 20 000 K, thirteen isotherms — and publishes no data-availability statement and no URL |
| Bethkenhagen+ 2013 (2013JChPh.138w4504B, doi 10.1063/1.4810883), the ammonia source | **held** (owner-obtained 08-30 11:29, PROVENANCE) and **already baked** as `ammonia_table.py` (`80fde5d7`, 08-30 17:13); 330 GPa · 500–10 000 K — **pure ammonia**, so not the mixture grid this table was looking for. *"AIP paywall" stood here until Brief 64 / P3.* |
| FPEOS, Militzer+ 2021 (2021PhRvE.103a3203M) | distributes tables and code, and carries CH₄ — but **no NH₃**, and its range 10⁴–10⁹ K begins above the ice-giant adiabat (5500–6300 K) |

**An author request is the only remaining route.** Bethkenhagen+ 2013 goes on the owner's
paper-request list; the 2017 tables would come from the same authors. **Closed 2026-09-01 by
the owner: the paper was not obtained, and the item ends as *recorded, not found*.** What was
searched and by what route is above; the grid stays unreachable without the authors.
**Why that closure still holds after Brief 64 / P3 (2026-09-03):** Bethkenhagen+ **2013** is held and
transcribed (`ammonia_table.py`) and is **pure ammonia**; what this row needed is the **2017 mixture
grid** (1000 GPa · 20 000 K, thirteen isotherms), and that is still not held. Holding 2013 does not
reopen the row — its closure was never about 2013's absence.


What can be said about the sign, in three tiers, only the first carrying a number:

- **composition** — direction **+**, it *widens* the residual. The solar-ratio mixture
  (0.31 : 0.08 : 0.61 CH₄ : NH₃ : H₂O by mass, Bethkenhagen+ 2017 §V) has a mean molecular
  weight of 17.28 against water's 18.02, so water overestimates the ice density by 4.27 % at
  equal number density (*derived*); electrons per unit mass agree in direction (H₂O 0.555,
  NH₃ 0.587, CH₄ 0.623 e/amu, *derived*). Correcting it lowers the density and enlarges a
  planet the model already makes too large, on a ~1.5 % radius scale (*derived*).
- **thermal** — mechanism named, **sign ungrounded**. Atoms per unit mass run H₂O 3/18 <
  NH₃ 4/17 < CH₄ 5/16, so the ideal-gas intuition is a higher heat capacity, a shallower
  adiabat, a colder and denser interior (Bethkenhagen+ 2017's icy Uranus is cold, T_core ~
  4000 K), pulling the radius back. Dissociation at high pressure shrinks that difference
  and with it the sign; no direction is defended.
- **net** — needs the tables.

Writing "1.5 % worse" would quote the first tier as the third.

C5 was attributed on 2026-08-30: the ice giants' residual belongs to a thermal boundary
layer at the transition between the ice/rock interior and the H/He envelope and to the
inner mantle's ice:rock ratio (Nettelmann+ 2016), with non-adiabatic interiors the review's
own open question (Helled+ 2020). **C4 is not a candidate for that residual in either
direction**, so closing it unbuilt costs the recipe nothing it was counting on.
`engine/ammonia-methane-context-notes.md` has the search.

**Reopened 2026-08-30 for the ammonia half** — the registered overturn condition fired: the
owner obtained Bethkenhagen, French & Redmer 2013 and **the table is printed inside it**
(Appendix B, Table I; no repository, no fit — the printed table is the distribution). The
closure above assumed it was out of reach; it was not. The methane half stays closed as
written — nothing new bears on it.

**Closed again for ammonia, built.** `engine/ammonia_table.py`, baked by
`tools/make_ammonia_table.py` from the cached PDF's text layer and checked against the
printed page: 93 points on a **ragged** grid (500 K to 1.5 g/cm³, 700 K to 2.0, 1000 K and
above to 3.0; 0.309–333.2 GPa), the five asterisked points carried as a 5 % flag against the
paper's 2 %, nothing interpolated across the six absent cells. The material `nh3`
(`eos.Ammonia`) refuses outside the table by name. **The convention is stated and tested**:
the caloric column includes the vibrational correction (2013 Appendix B) — the correction
Bethkenhagen+ 2017 §II.4 removed from this set — and the exposure is c_P / ∇_ad only, never
the density mixing. The ice-giant adiabat (5500–6300 K) lies between the 5000 and 7000 K
isotherms: **interpolation, not extrapolation.** Interpolation error, leave-one-out at
doubled spacing: 8.7 % in the mantle region (ρ ≥ 1 g/cm³, T ≥ 2000 K), 17.3 % in the low-density dissociation corner.

**What the table settles, and only that.** Water (Mazevet+ 2019) and ammonia (this table)
read at the same (P, T) at eight points — four on the engine's own solved Uranus profile
(50–250 GPa, 2830–3950 K) and four bracketing the central temperatures — mixed by additive
volume at the solar-ratio pair fraction w_NH₃ = 0.1159: ammonia is 21–24 % less dense than water at
equal (P, T) — the equal-number-density μ argument (5.5 %) was a floor — and **water
standing in for the water–ammonia pair overestimates its density by 2.9–3.5 %**, direction
+, above the propagated noise (0.6 %). That is the composition tier's number for the
**ammonia share**; the tier's direction stands. The thermal tier gets a first table-derived
indication that is **not uniform**: ammonia's ∇_ad is 19–45 % below water's at seven points
(the pair's adiabat 3–10 % shallower) and above it at the mantle top (50 GPa, 2830 K: 2.6 %
steeper), under the convention caveat — so it **keeps "sign ungrounded"**. The net tier still needs the tables,
**because methane — the largest share, 0.31 — is still missing.** Ammonia is not wired
into any body; whether it enters the mantle as a declared fraction is the owner's decision,
with the grounds (for, against, and the ceiling below the ice giants' centres) in
`engine/ammonia-table-context-notes.md`. Anchors bit-identical — no path function moved.

**The methane half, re-stated from the full text (2026-08-30, not built).** Sherman, Wilson,
Weeraratne & Militzer 2012, *Ab initio simulations of hot, dense methane during shock
experiments*, Phys. Rev. B 86, 224113 (2012PhRvB..86v4113S, arXiv 1207.2948) is in the
cache as the published PDF and the arXiv LaTeX source. **A table exists and is distributed**:
the source's appendix carries 79 DFT-MD (T, P, E) points with 1σ error bars, marked *"to be
published as online supplementary information"* — the published PDF refers to the
supplement and does not print it. The row's old reason, *not obtained because paywalled*, is
replaced by two that hold with the table in hand:

- **Methane does not persist as a species in the region.** Sherman: *"At a temperature of
  approximately 4000–5000 K, a plateau is reached … the system entering into a polymeric
  regime where the methane molecules spontaneously dissociate to form long hydrocarbon
  chains"*, a regime they show to be metallic; at 6000 K a plasma. Bethkenhagen+ 2017 §III on
  their own runs: *"Pure methane does not become superionic but instead decomposes into
  long-chained molecules in our simulations."* Additive volume assumes each component keeps
  its identity at (P, T); **no mixing error for a dissociating component has been measured
  or published**, so a methane table would not make a linear-mixing mantle grounded.
- **The grid does not cover the region.** Counted from the source (13 densities × 13
  temperatures, 79 cells filled): the low densities stop at 4000 K, only two density lines
  (1.201 and 1.498 g/cm³) run the full 300–75 000 K, and single points sit at 0.600, 1.353,
  2.129 and 2.376 g/cm³. Bethkenhagen+ 2017 §II.3, naming Sherman: *"none of them covers the
  entire pressure-temperature region required for Uranus and Neptune interior models."*

| ρ (g/cm³) | 0.600 | 0.800 | 1.000 | 1.201 | 1.353 | 1.498 | 1.600 | 1.775 | 2.010 | 2.129 | 2.257 | 2.376 | 2.502 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| points | 1 | 5 | 5 | 13 | 1 | 13 | 9 | 9 | 9 | 1 | 6 | 1 | 6 |
| T (K) | 300 | 300–4000 | 300–4000 | 300–75 000 | 2000 | 300–75 000 | 2000–75 000 | 2000–75 000 | 2000–75 000 | 10 000 | 5000–75 000 | 10 000 | 5000–75 000 |

**Measured: the solved mantles do pass the published dissociation thresholds.**
`tools/methane_thresholds.py` reads the frozen convergence point and samples the ice layer:

| | Uranus | Neptune |
|---|---|---|
| ice mantle span | 34.5–820 GPa, 2663–5948 K | 39.2–1016 GPa, 2553–6066 K |
| C–C bonds (> 1100 K and > 10 GPa, Hirai+ via Sherman) | the whole mantle, from its top | the whole mantle, from its top |
| diamond, **C–H system** (> 3000 K) | from 80 GPa (3037 K) to the base — 71 of 78 samples | from 114 GPa (3049 K) — 67 of 76 |
| diamond, **C–O–H system** (> 1600 K) — *the mantle's own chemistry* | **the whole mantle, from its top** (34.5 GPa, 2663 K) — 78 of 78 | **the whole mantle, from its top** (39.2 GPa, 2553 K) — 76 of 76 |
| polymeric 4000 K / 5000 K | 262 GPa / 525 GPa | 334 GPa / 626 GPa |

**The threshold this row first used was the wrong chemical system, and it understated the
crossing** (survey ④, 2026-08-31). 3000 K is C–H, from Hirai+ via Sherman; our mantles are
C–O–H — methane *and water* — and Kadobayashi+ 2021 measure that system directly:
*"…to ultimately form diamond proceeds at **milder temperatures (~1600 K) and pressures
(13–45 GPa) in the C–O–H system than in the C–H system due to the influence of water**"*,
with *"below ~1600 K, diamond formation did not occur, even under prolonged [heating]"*.
Re-run at 1600 K (`tools/methane_thresholds.py`, one constant changed, reproduced by the
directing seat), the count is **78/78 and 76/76 — crossed at the mantle's top**, the
coldest point of either mantle (Neptune's 2553 K) sitting 953 K above the threshold. The
C–H row is kept above it rather than deleted, because it is what the earlier text was
measured against.

So in this recipe's own profiles the entire ice mantle sits above the carbon–carbon bond
threshold, **all of it above the diamond threshold of its own chemistry** (nine tenths, by
the C–H threshold this row first used), and its deeper half inside or beyond the polymeric
regime. That is a measurement, recorded here as grounds
either way; whether carbon separation becomes an item (carbon as its own phase rather than
methane in a mixture) is the owner's decision. **The three-tier sign statement does not
move**: methane's absence is now more precisely stated, and the net still needs tables that
would have to carry a dissociating component — which none published does.

**Opened by the owner 2026-08-31, and surveyed (④).** Four questions were put to the
literature; the answers move the blocker rather than removing it.

*Separation happens, and it has a destination.* Kadobayashi+ 2021 on the C–O–H system:
diamond formation *"can occur throughout the icy mantles of Uranus and Neptune (even in
their upper regions)"*, and the diamond *"settles deep into the icy mantle and accumulates
at the boundary between the icy mantle and rocky core."* The overlap is one-sided, and this
must be carried with the claim: **in temperature our whole mantle is above threshold, but
the experiments reach 45 GPa (C–O–H) and 80 GPa (C–H) against our 34.5–1016 GPa** — they
cover the mantle's top few per cent, and below that the authors are extrapolating.

*An equation of state exists and it reaches us — the survey's first answer was wrong and
was retracted.* Correa+ 2008's multiphase carbon EOS is neither a static-DAC table (≤900 K)
nor a warm-dense-matter one (≥10⁴ K), the two categories the survey had generalised into a
gap. §III: the solid-phase treatment holds *"in the range of our interest (below a pressure
of ~2500 GPa)"*, against our mantle base of 1016 GPa; BC8 becomes *"stable above a pressure
of roughly 1100"* GPa with the cold curves crossing at **1075 GPa**, so Neptune's base sits
inside the diamond field by ~60 GPa; and Correa+ 2006 puts the diamond–BC8–liquid triple
point at **7445 K · 850 GPa**, above our hottest 6066 K, so separated carbon is solid here.
Table I prints the coefficients.

*The cost is a form mismatch, not an absence.* The cold curve is a Vinet fit, which
`eos.Phase` already takes (V₀ = 5.785 Å³/atom → **ρ₀ = 3.4477 g/cc**, recomputed). The
thermal term is not ours: they carry a volume-dependent Debye θ(V) with a Grüneisen
parameter varying with volume plus an anharmonic term, and **our Anderson–Goto form is the
special case where γ₀/V is constant**. So this is an implementation extension with a
measurable error, of the kind the ladder has taken before — not a missing table. The
authors also flag their own bias: V₀ is *"3% larger than that of experiment **once
zero-point motion and thermal expansion have been accounted for** … it may be necessary to
shift V₀ 'by hand'"*, a *"well-known error resulting from the use of GGA-DFT"*. **Only that
3 % is theirs**: dividing their V₀ by a 298 K measurement gives −2.00 % in density and is
not like-for-like — their V₀ is a static-lattice cold-curve parameter with neither
zero-point motion nor thermal expansion in it, and both corrections shrink the experimental
static volume, which is why their number is the larger one.

*And the experimental branch is a table too, not just a range check.* Dewaele+ 2008's
Table III prints a complete Mie–Grüneisen–Debye equation of state for diamond —
V₀ = 5.6693 Å³/atom, K₀ = 444.5 GPa (fixed), K₀′ = 4.18(15), θ₀ = 1860 K fixed *"based on
heat capacity measurements"*, γ₀ = 0.85 fixed *"based on ambient pressure thermal expansion
data"*, with q = 3.6(1.5) the single adjusted parameter; Occelli's 298 K V₀ = 5.6724(19)
sits beside it. It reaches only 80 GPa · 900 K, so it cannot carry our mantle — **but it is
the same function family as Correa's**, which is what makes either of them consumable: one
`Phase` extension takes both, and **the experimental set becomes a low-pressure check on
the first-principles one**. That is a better position than either paper alone.

**And there are two carbon stories, not one** (survey ⑤, 2026-08-31 — the owner asked
whether theory exists where measurement does not). Everything above is **diamond**: a solid
that nucleates, sinks and piles up. The other is **fluid**: Militzer 2024
([`2024PNAS..12103981M`](https://ui.adsabs.harvard.edu/abs/2024PNAS..12103981M), single
author, CC BY; Europe PMC full text cached as `.xml`/`.txt` — the PDF is script-blocked,
not paywalled; the figures record is not in the cache, but the **SI data deposit is** —
Zenodo 13937364 unpacked in `_papers/militzer2024_zenodo/`, 7 files, since 09-02 22:34; only the figures
record 13952386 is unheld — corrected by Brief 64, the earlier "figures and SI" was half false) finds a solar-type
7 H₂O : 4 CH₄ : 1 NH₃ mixture at **343 GPa · 4750 K** — inside our solved mantles, not an
extrapolation — where *"the homogeneous fluid **spontaneously phase separates** into a
water-rich fluid and a C-N-H fluid"*, self-checked as *"not sensitive to the hydrogen
concentration"*, with compositions printed (C₈N₂H₁₁…H₃₄ / C₈N₂H₁₃…H₃₈). **No solid**: the
word `precipitat` appears **0 times** in the distributed full text (counted twice, by the
surveyor and by the directing seat), and `diamond` 5 times — all in the literature review,
where *"the formation of diamond from CH₄ in ice giant interiors has been explored with
theoretical and experimental techniques (17–19)"*. **It cites the diamond work and models
something else.**

That splits both blockers by axis:

| | a theory for *how much* | a target model that has it |
|---|---|---|
| **fluid C-N-H separation** | **yes** — Militzer 2024, first-principles | **yes** — Militzer 2024 builds Concentric MacLaurin Spheroid ensembles that *"match the observed gravity field"*, printing J₂ = 3510.99 and J₄ = −33.61 / −35.8 (×10⁻⁶) as the fit targets |
| **diamond precipitation** | partial — Cheng+ 2023, still C/H with no water | **none found** (three ADS sweeps; Ross 1981 is the idea's origin, Bailey & Stevenson 2021 separates H₂–H₂O, not carbon) |

**So C13's trap is lifted on the fluid axis and stands on the diamond axis** — and choosing
between them is a physics choice, not a gap: Militzer knew the diamond literature and
modelled the other thing. One cost rides along with the fluid axis: their mixture
**contains ammonia** and our column does not, so adopting the theory adopts a composition.

*What blocks the diamond axis is the other two questions.* **How much** carbon separates has no
published rule that includes water (Cheng+ 2023 give coexisting compositions for C/H, with
no water, and the quantity still needs a declared bulk carbon fraction — `composition_intent`,
currently a gap). And **the target does not have this component**: the three-layer practice,
Nettelmann+ 2013 included, represents HCNO molecules by a water equation of state. That is
C13's registered trap — adding what the target lacks and then matching its number means no
longer computing the same thing. Both are owner questions, not literature ones.

*A timescale, not an uncertainty.* Frost+ 2024 measure diamond forming at 2500 K over
19–27 GPa and find it *"took at least 30 µs to form"*, and name why the field splits:
*"the disagreement between static and shock compression studies is the timescale of the
physical processes, which can differ by more than 10 orders of magnitude."* The static and
shock thresholds are one process seen at timescales ten orders apart — so the spread
between them is **a rate, and must not be carried as an error bar**. On planetary
timescales the static side is the relevant one.

### C6 — Material ceilings

Each material stops where its evidence stops, and each ceiling is a row that declines by
name. They are listed together because they are one kind of work.

| material | ceiling | what is above it |
|---|---|---|
| `h2o` | 1 TPa · 1800 K **(printed; the data ceiling is ~355 GPa — see below)** | ice X above the knot domain; superionic above the temperature |
| `silicate` | 13.5 TPa | Thomas–Fermi–Dirac (electron degeneracy) |
| `fe_prem` · `fe_eps` | 12 · 20.9 TPa | the same |
| `h_he` | 10⁴ GPa in the giant branch | the table's own edge |

Needs: nothing, unless a body the roster wants is refused by one of them. **Each is a
correctly stated limit, not a defect** — the work here is to keep them honest, not to remove
them. Listed so that a future refusal can be traced to its row rather than re-diagnosed.

**Except one, found 2026-08-31 — `h2o`'s 1 TPa is the spline's knot box, not the source's
data ceiling.** French & Redmer 2015 §III, read in the cached PDF: *"A total number of 92 MD
simulations of these ices were [performed] … The densities were varied between 1.6 and
4.25 g/cm³, and the temperatures were chosen from 295 up to 2000 K… Densities of 4.5 g/cm³
and higher lead to a distortion of the bcc oxygen lattice."* On our own 300 K isotherm
(point evaluations, not a sweep) ρ = 4.201 g/cc at 340 GPa and 4.267 at 360 GPa, so their
highest simulated density sits at **≈355 GPa**; at the printed 1 TPa ceiling our ladder
returns **5.755 g/cc** — 1.35× their highest simulation and well past the 4.5 g/cc where
they say the lattice distorts. **The ladder's upper two thirds in pressure is extrapolation**,
resting on the paper's own §I assurance that the potential "is well behaved in
extrapolation" — a statement about the function's smoothness, not about those values being
verified. This is the fifth failure kind (printed validity range ≠ executed range, the rule
`water2` produced) landing on **our** side rather than a third party's, and the rule's
prescription — record the effective ceiling with the table — is what this paragraph is.

**Where it bites, stated precisely, because the obvious reading is wrong.** It is *not* true
that the anchors stay under 355 GPa: the ice giants' mantles span 34.5–820 GPa (Uranus) and
39.2–1016 GPa (Neptune). They are unaffected for a different reason — their mantles run
2553–6066 K, above `ICE_VII_X_T_MAX` = 1800 K (`eos.py@«# # **그 처방을 따르지 않았다.**»`), so the ladder branch never
fires there and Mazevet carries the column. **The extrapolation therefore bites only on a
cold, dense water column: T < 1800 K above ~355 GPa** — the same cold flank this list has
been tracking all day, and a second reason (beyond "no table at all") that AQUA's high-
pressure 300–1000 K corner is the gain worth having. No answer moves today; what moves is
what this row is allowed to claim.

Depends on: a body that actually hits one.

**A trace component can veto a state, and what that costs was measured, not declared
(Brief 28, 2026-09-01).** The mixture's evidence gate is weight-blind by design —
`eos.py@«# #   * 이성분 — "deviati»`, `min(m.p_max for m, w in self.parts if w > 0.0)` — and its comment gives the
reason: *"if one component is outside its evidence range the mixture density there has no
grounding; using the highest ceiling would hide ungrounded extrapolation behind a grounded
component."* **The general statement stands.** What Brief 27 exposed is the edge: the fatal
refusal fired on an `h_he` component whose weight in that shell is **6.87 × 10⁻⁶**.

Rather than declare a cutoff — this list has refused arbitrary thresholds twice — the
contribution was **measured**, at the same pressure but above the floor so both mixtures can
be evaluated:

| w | Δρ/ρ | Δc_p/c_p | Δ∇_ad/∇_ad |
|---|---|---|---|
| **6.87e-6** (the actual weight) | −1.18e-5 | +1.46e-5 | −8.9e-6 |
| 1e-4 | −1.72e-4 | +2.12e-4 | −1.30e-4 |
| 1e-3 | −1.71e-3 | +2.12e-3 | −1.30e-3 |

**Linear to three or four digits** (slopes −1.716 / +2.118 / −1.299), so branch ③ did not
fire and **the crossing point is computed rather than chosen**: at this location the
contribution reaches the anchor's own reproducibility (3.7–3.9e-4) near **w ≈ 1.7 × 10⁻⁴**.
At the weight that actually vetoed, all three quantities sit **25–30× below** that jitter.

**The comparison's own weakness, stated by the measuring session and not by its proposer.**
A point-wise EOS error and an end-to-end radius jitter are **different quantities**; putting
them side by side is a **scale reference, not a propagation**. So "smaller than the anchor's
jitter" is not yet a bound on the answer — turning it into one means perturbing the density
by that amount and re-solving. **Not done.** The directing seat proposed this criterion; the
limitation belongs with it.

**And what the measurement does not cover, registered in advance**: the refusal's effect on
the *search trajectory* (Brief 27's `conv=False` is exactly that, and a point measurement
cannot call it negligible), the other weight-blind gates (`cold_phases`, `in_domain`), and
the `_EnvelopeWater` dispatch interaction. The slopes are also location-dependent, so any
policy would need a conservative envelope or a per-site check.

**Owner's decision, 2026-09-01: leave the gate as it is, and keep the measurement.** The
reason is that **the case which raised the question dissolved** — the state where the trace
component vetoed turned out to be forbidden anyway, with helium solid there and the source
saying its equation of state must not be used at those conditions. **So there is not yet a
single instance of a trace component blocking an otherwise legitimate answer**, and this list
does not build machinery without a consumer (the rule C5 followed when it declined to
implement a graded envelope). Nothing was changed. When a body is refused by a trace component
at a state that is otherwise sound, the item opens with the method already in hand.

**Fired again 2026-09-01, and this time the ceiling is a third one: `ice_x` has three, and the
code uses the largest** (surveys ⑩/⑩b; `engine/superionic-ceiling-context-notes.md`).

| ceiling | value | what it is |
|---|---|---|
| **data** | **≈355 GPa** | above it the ladder is extrapolation — the row above, unchanged |
| **stability** | **≈520 GPa** | where the ice region *closes* in the potential `ice_x` is fitted to — new |
| printed | 1 000 GPa | SeaFreeze's `VII_X_French` knot box, and what `ICE_X_P_MAX` says |

The stability ceiling is the new one and it is **not a competing source**: the ice side of the
boundary is French, Desjarlais & Redmer 2016's Fig. 4, whose ices potential is *"taken from
Ref. [30]"* = French & Redmer 2015 ([`2015PhRvB..91a4308F`](https://ui.adsabs.harvard.edu/abs/2015PhRvB..91a4308F)),
**the same potential SeaFreeze's `VII_X_French` carries and `eos.py`'s `ice_x` is fitted to**
(`eos.py@«#     ρ₀ = 4.10 Mg/m³ · K₀ = 247 ± 4 GPa · K₀′ = 3.97 · 적합 BME4 · K₀″ = −0.016 /GPa»`, `2027-2036`). So this is *the authors of our own ice potential computing
where their ice stops being the stable phase* — the bcc–ices boundary turns back down and
leaves the plotted temperature range near 520 GPa, above which their calculation shows no ice
region at any plotted temperature. They say it closes and do not say what replaces it: *"There
have been several predictions of crystalline structures of water ice at zero Kelvin **beyond
the stability region of ice X** [69–75] … most of them are of noncubic structure and the
derivation of accurate thermodynamic potentials for them is not an easy task."*

**This is the same disease C6 was opened for, one layer deeper.** The row above already found
that our ladder's printed ceiling is not its data ceiling. The third ceiling says the printed
ceiling is not its *stability* ceiling either, and the smallest of the three is the data one
while the code carries the largest. **No published number moves**: the anchors' mantles bottom
out at 2553 K, far above `ICE_VII_X_T_MAX` = 1800 K, so the ladder branch does not fire on a
converged column — which is exactly the condition the row above already registered. **What is
unmeasured is the trial path**, and that is what separates a labelling defect from a
convergence defect.

**And a second finding rides with it, which is a label rather than a ceiling.** The gate's
superionic floor (`test_interior.py@«# 거짓을 주장했다. 대체 검사 = test_ice_giant 의 교란-불변 회귀 (eos.py ICE_VII_X_T_MAX 주석).»`, `MILLOT_SUPERIONIC = (100.0e9, 2000.0)`) is **flat**,
and the boundary is not: it rises to a maximum near 200 GPa and descends through 1800 K
somewhere in **305–375 GPa** (two independent figure renderings; the maximum agrees to 0.7 % in
T and 5 % in P, the crossing disagrees by 29 GPa with error bars barely touching, and **was not
adjudicated** — a figure reading does not settle a figure disagreement). So `ICE_VII_X_T_MAX <
t_sup` **passes while asserting something false**, and the promise in `eos.py@«#   500 GPa 위      **이름 대고 거절** — 여섯 논문 어디에도 자료가 있는 전사 가능한»` — that
superionic ice will not quietly be called ice X — is reachable. Worse, the constants'
provenance is false in the way subspecies 7 describes: Millot+ 2019's *"exceeding 100 gigapascals
and high temperatures above 2,000 kelvin"* is that paper restating **the prediction of its own
refs 6–12** (*"Particularly intriguing is **the prediction** that H₂O becomes superionic⁶⁻¹²…"*,
verified verbatim in the cached PDF by the directing seat), not its result — and the paper's own
measurement window, 100–400 GPa × 2 000–3 000 K, is an experimental range, not a boundary.
`eos.py`'s `SUPERIONIC_MIN_T`/`_P` were meanwhile **defined and never read**; the live copy was
the test's, unlinked to them.

**Closed 2026-09-01 by Brief 34 — and the answer was cheaper than either candidate fix**
(`438efd70`, `6ae41eb4`, `21f37436`; `engine/superionic-gate-context-notes.md`). **The two
paragraphs above are the state before that brief and are kept as the finding's record; what
follows is the state now.**

**Both ceilings do have a consumer, and it is a trial corridor that does not reach the answer.**
Item A instrumented every `ice_x` evaluation across all seven anchors: the five moons make
**zero** (their deepest phase call is 8 GPa-scale), Neptune's corridor stops at 235 GPa, and
**Uranus makes 1,854 evaluations inside the region** — 355→535 GPa traversed continuously along
an adiabat, T rising 1643→1800 K with pressure (0.87 K/GPa; not pinned at the ceiling — ≥1799 K
is 0.8 % of them, median 1728). **A directing-seat reading that the temperature loop was riding
the ceiling was refuted by that distribution**, which is what the distribution was asked for.

**Then item A2 measured whether the answer depends on that region, and it does not — on both
axes.** Criterion fixed before running (same solution within the anchors' recorded
reproducibility, not bit-identity, since a perturbation moves the shoot's iterates). Five runs
came back **bit-identical, Δ exactly 0**: a ±5 % density perturbation confined to the region
**fired 1,754 times** and moved nothing, so the answer is insensitive to the *values*; and
refusal at first contact **fired once** and left the trajectory identical to base, so the trials
that walk the region are **discardable** — first-contact death and full-walk death are the same
signal to the controller. The null result was validated by hook-fire counts before being
believed, which is the reason it is trustworthy rather than an instrument that never fired.

**So both candidate repairs were discarded, each by measurement rather than by preference.** B2
("assert `ice_x` is never evaluated there") had its **premise** disproved — it is evaluated 1,854
times. B1 ("refuse by name at the boundary") had its **necessity** disproved — refusing changes
nothing, so it is machinery without a consumer, which is C5's rule. What landed instead is
**tolerance plus labels**: the flat-floor check and the falsely-attributed constants are removed,
and the gate now asserts **the measured invariance** — a +5 % perturbation in the region must
reproduce Uranus's anchor to the bit (`test_ice_giant._clamp_invariance`, +22 s, ≈2 % of the
gate). That is a claim about our code rather than about the world, and it **fails loudly on the
day a solver change connects the trial corridor to the answer.**

**The scope limit is part of the result, not a caveat on it**: this invariance is *measured for
the current roster's Uranus, and is not a general guarantee.* A body whose **converged** column
enters the region reopens it — which is why C6 remains a standing watch. `ICE_X_P_MAX` stays at
1 000 GPa, and A2 **weakened** the case for narrowing it: the only consumer is a corridor that
does not reach the answer.

**Held, unused — a candidate, not a task (2026-09-03, Briefs 51 and 53).** Chabrier & Debras 2021 (Paper II,
H/He *interacting* mixture, dropping the 2019 Ideal Volume Law) is in the cache
(`docs/phase3/_papers/chabrier_direos2021/`, owner-fetched, provenance written). Switching `hhe_table.py`
to it is a **physics decision**, not housekeeping, so nothing was switched. What is actually measured, both
editions parsed to (log T, log P) → grad_ad over the 7,889 baked-window points (logT 2.0–4.4, logP −4…+4 GPa):

- **Format**: identical header, columns, grid (53,361 points) and sentinel convention (−8.8603 → `None` in
  `make_hhe_table.py`); the reader needs only the filename. Sentinel cells move from seven (2019, logT
  2.70–2.85, logP 1.10–2.30) to three (2021, logP 2.50 at logT 2.45–2.55), all in the same cold-dense corner
  below the reach line — **not an advantage either way**.
- **grad_ad differs by more than 0.01 at 40.5 % of window points, median 6.2×10⁻⁵.** Those two figures stand.
- **The former headline "max 0.40" is a clamp-convention artifact and must not be quoted as a physical
  change.** Both editions clamp unconverged grad_ad cells to round numbers, differently: 2019 carries 0.1 at
  626 cells and 0.5 at 263; 2021 carries 0.1 at 618 and **0.4** at 542 — **rounded-match counts** (value equal
  to the clamp at the baked table's four decimals; exact match gives 624 and 617, the difference being computed
  values such as 0.100003 that the baked table cannot tell apart from the clamp — the rounded count is the one
  that matters for anything the engine reads, and this is which one it is). Every one of
  the 47 maximum-difference points is 2019 = 0.5000 against 2021 = 0.1000. `make_hhe_table.py@«"# 외피가 닿지 않고, 배포 표의 결함(밀도 자리의 sentinel 7칸, 0.1/0.5 로 눌린 grad_ad)이",»` had said
  so already — *"배포 표의 결함(밀도 자리의 sentinel 7칸, 0.1/0.5 로 눌린 grad_ad)"*, all below the reach line — the
  third time this week the generator held the answer before it was re-derived.
- **Genuine large differences, with the definition stated**: of the 730 window points with |Δ| > 0.1, 497
  (68.1 %) have either side sitting exactly on one of that edition's clamp values ({0.1, 0.5} for 2019, {0.1,
  0.4} for 2021); the remaining **233** are genuine, **max 0.3289 at logT 2.55, logP +1.00** (2019 0.4610 vs
  2021 0.1320), all at **logT 2.40–3.85**, the cold-dense corner. *(Superseded: the audit's first count, 288
  clamp-involved / 442 genuine / 201 baked, came from an edition-blind filter that tested {0.1, 0.5} against
  both editions and never tested 0.4, so every 2021 cell clamped at 0.4 fell into "genuine"; the audit
  re-ran the edition-specific definition and reproduces 497 / 233 / 121 exactly. The conclusions below never
  depended on the split.)*
- **Against the table the engine actually reads** (`hhe_table.py`'s `KEEP`: per-isotherm cell counts summing
  to **5,495**, the baked cell count — the mapping checked; baked grad_ad is the distributed value rounded to
  four decimals, max |Δ| 5×10⁻⁵): **0 of the 47 maximum-difference (0.5 vs 0.1) points are baked** — the old
  0.40 headline sits at coordinates our table does not contain, both halves of that statement. Of the 233
  genuine large differences, **121 are baked**; **the largest genuine
  difference inside the baked table is 0.2607, at logT 3.35, logP +0.95 (2019 0.4056 vs 2021 0.1449)** — that is
  the number this entry carries. **0 of the baked genuine large points fall in the paper's departure box**
  (all 147 box points are baked). The generator's claim that the distributed table's defects are *"전부 거기
  있다"* (all below the reach line) holds for the high clamp — **zero baked cells at exactly 0.5** — and only
  partly for the low one: **72 baked cells sit at exactly 0.1**.
- **The paper's stated departure region is inside our window and does not contain the large differences.**
  Chabrier & Debras give *"≲5 % of the total entropy in the 5,000–10,000 K, 10–100 GPa … T–P maximum departure
  range"* (읽음: c4) = logT 3.699–4.000, logP 1.0–2.0, **147 grid points, all baked**. Binned: |Δ| > 0.01 in
  **80.3 %** of box points vs 39.8 % outside (2.0×); |Δ| > 0.05 in 34.7 % vs 20.3 % (1.7×); |Δ| > 0.1 in **0.0 %**
  vs 9.4 %; |Δ| > 0.3 in 0.0 % vs 1.5 %. Zero box points among the top 100 differences; zero of the 233 genuine
  large ones in the box. ⚠ "≲5 % of total entropy" is a bound on entropy, not on grad_ad — a different quantity,
  and the clamp finding is exactly how a number attached to the wrong quantity survives in an entry.
- **Passed through from c4, unverified here, and qualified**: Paper II claims, **for Jupiter interior
  conditions**, density error < 1.0 % and entropy error < 0.5 % against MH13, versus several per cent on
  density and up to 30 % on entropy for Miguel+ 2016 — a Jupiter statement, not a global one.

**The corrected chain, in the order a reader needs it**: (1) the old headline 0.40 is a clamp-convention
difference at coordinates our table does not contain — 0 of 47 baked; (2) the real in-table maximum is
**0.2607 at logT 3.35, logP +0.95**, with 121 of the genuine large differences baked; (3) none of
them sit in the paper's maximum-departure box, which is itself 147/147 inside the baked table and enriched only
at 0.01–0.05; so (4) the switch stays unmade **because a 0.26 difference in the quantity the envelope's
temperature depends on is unattributed** — not because the differences are small. The Paper II accuracy
figures above are *"for Jupiter interior conditions"* (c4 re-read the sentence) and must not be read as global.
**Named hole, not silence**: nothing yet explains the genuine large differences in the cold-dense corner; a
future switch has to answer that first. Uranus/Neptune anchors would move; that is what "candidate" means
here.

**Standing watches attached here (owner's notation, Brief 64, 2026-09-03) — three constants the answers
lean on and no source settles.** Each is a labelled condition, not an open item; it fires the day a body or
a solver change makes it load-bearing in a new place.
- **γ = 1.5** — `GAMMA_CORE`, a solid (h.c.p.) value on a liquid density fit; Earth's inner core exists in
  this recipe only at that value (Brief 42's knife-edge, 0.94 %), and now it rides upstream of `Q_adiabat`
  (Brief 60). Not moved, because moving a constant to make an answer come out is prohibited. **One
  knife-edge, three axes (C14, 2026-09-04)**: Earth's inner-core verdict in this recipe is thin and flips
  within its own uncertainty on three independent axes — **γ** 1.500 declared, flips at 1.514 (0.94 %,
  Brief 42) · **centre margin** −17.6 K (Brief 42, "thin") · **T_c** 3 760 K declared, flips at 3 772.5 K
  (12.5 K; audit, 6 400-step bisection; 3 769.8 with the 2 % cutoff). At 3 760 K both `core_state` and the
  C14 profile find a 566–572 km inner core (ICB 351.3–351.4 GPa, half of PREM's 1 220 km); at the balance's
  own T_c, 3 978 K — 205 K past the threshold — **the core is all liquid** (a verdict, not a refusal: every
  sample has a melting temperature, minimum margin +290 K), because the pressure profile stays
  (`fe_prem` is temperature-independent) while the adiabat rises through the melting curve. *(A "second
  face — the pressure profile's temperature" stood here for one evening and is withdrawn: it was a numerical
  artefact of an unconverged Euler profile, `core-energy-balance-context-notes.md` §3b/§5.)*
- **`Rm > 40` quoted, never evaluated** — the rocky dynamo's alive-gate sits in the ladder as a class
  judgement; no magnetic-Reynolds expression exists in the recipe (Brief 43). Building one is the larger
  brief the owner has not opened (C15 is its φ half).
- **0.06 as a secondary citation** — `MULTIPOLAR_FACTORS`' OC06 value was taken through RM22; OC06 has been
  held since 09-03 13:40, so it is **checkable at source and not yet checked** (Brief 64 ②).

### C14–C19 — opened 2026-09-03 under the owner's notation (Brief 64); each is a `status: gap` edge in `chain.yaml`

None of these is work in progress; they are the holes named so that the queue has a number to point at.
Order among them is the owner's, brief by brief.

**Handoff inventory 2026-09-04 evening** (`interior-dynamo-handoff-context-notes.md`): the interior domain owes the dynamo one printed Need, `conductor_phase`, and supplies it; the five drawn interior → dynamo_rocky edges (`:677 :684 :686 :687 :725`) have no printed Need and no code consumer — outcome Ⓢ, refs corrected in `chain.yaml`.

| C | edge (`chain.yaml`) | what the hole is |
|---|---|---|
| **C14** | `internal_heat_nontidal → dynamo_rocky via geotherm` (`:639`) | whether the core is *still* convecting needs thermal evolution, not only decay history; Brief 62 step 1 measured that the present-epoch closure is a root-find in T_c with the cooling rate declared. **Built 2026-09-03** (owner *"c14 진행하자"*; `core_energy.py`, node `core_energy_balance`, `core-energy-balance-context-notes.md`): Nimmo's analytic core reproduces Table 4 component by component (all within 10 %, Q_L/Q_g 8 % low and left low) and the root lands at 4 152 K vs printed 4 155; on the engine's Earth the solved T_c is **3 978 K (band 3 750–4 284), +218 K over the declared lower bound**, Q_C 4.91 TW — inside Nimmo's 4.5–9 on this model's terms. **Finding (corrected 2026-09-04 after a convergence bug the directing seat caught — the first evening's "two codes disagree" was an Euler artefact)**: at the declared 3 760 K both codes find an inner core (566 km, ICB 351.3 GPa); **at the solved 3 978 K the core is all liquid** — closing the loop removes Earth's inner core, so Q_L = Q_g = 0 on the solved Earth and C15's entropy budget loses its two largest terms. Nothing moved; not fed back. The edge itself stays `gap` — the *consumer* (dynamo) is C15. ⚠ *2026-09-09 (C25 (c)): this root is where the mantle-side flow and the core-side supply are the same number — 4.913 against 4.912 TW — which is what the closure **is**. And "never nucleates" fits no camp in the printed inner-core-age literature, 0.37 – >2.5 Ga (C25 (d)); that is the depression factor's, not this row's.* |
| **C15** | `heat_transport_mode → dynamo_rocky via cmb_heat_flux` (`:638`) | the supplier `cmb_heat_flux` exists (Brief 60); the consumer wiring is φ, core entropy production. **φ built 2026-09-04** (`core_entropy.py`, node `core_entropy_production`, `core-entropy-context-notes.md`): Nimmo eq. 43's six terms on C14's profile; Table 4's entropy components reproduced within 10 % each (ΔE 328 vs 351); the engine's Earth at the solved 3 978 K gives **ΔE −69 MW/K, band −264…+238, 4/8 corners positive, H = 0 → −167** — C14's vanished inner core arriving at the budget. **A band, not a verdict** (the required excess is 0.1–1 000 MW/K; `ΔE > 0` is the paper's own threshold-avoidance), **not wired into `dynamo_rocky`** (edge kept `gap` on purpose), and the 3-Gyr statement is refused by name — **C20 is this node's first real consumer.** ⚠ *2026-09-09 (later): this budget now takes the **declared** core-side temperature — Earth 3 760 K, the owner's horn — rather than C14's root, and `H` is capped at **0.088** pW/kg (0.14 until Brief 166 E corrected the conversion); the measured result is `ΔE` **+26.5** MW/K, band **−76.3 … +188.3**, 4/8 corners positive, H = 0 → +20.4 — **still straddling zero** (C25 (f)). ⚠ *The cap moved the band's **top only** (+191.9 → +188.3): its floor is the H = 0 corner, which no potassium decision can touch.* ⚠ And the regime gate's `Ro_ℓ` ≈ 0.12 agrees with Christensen & Aubert 2006, but **the engine declares `locked` and never computes `Ro_ℓ`** — the number we agree with is one we do not calculate.* ⚠ *2026-09-09: the band's two axes are laid against the printed literature in C25 (d) — `k` 18–226 and every later potassium constraint below our ceiling — and C25 (c) measures what each horn of C25 does to this budget: the inner core is the whole difference. Three owner decisions are collected there; none is made.* |
| **C16** | `tidal_locking → dynamo_rocky via rossby` (`:635`) | *(the first line here — "not derivable from a rotation period" — was wrong: Ω is exactly what `rotation_period` supplies)*. **Built as a partial build 2026-09-04** (`regime-gate-context-notes.md`): RM22's branch structure — free rotator → dipolar by rule (eq. 20, no Ro_ℓ); locked → Ro_ℓ **refused by three names** (ν has no value in RM22; q_conv is undefined; the printed equation misses the paper's own Table 8 by 4–5×, a table that is itself a fit of k = 60); key absent → `cannot-say (no tidal_locking)`. **The key `locked` is `tidal_locking`'s output and that node has no recipe** (34 computed nodes, 10 registered), so today every body gets the last answer — the correct state. Measured with a positive control: the thrice-corrected `MULTIPOLAR_FACTORS` has **no consumer that elects it** on the roster (0 of 3 primary; Earth's beside-pair only, read by nothing downstream) — a C5 question for the owner, not judged. |
| **C17** | `ocean_fraction → dynamo_rocky` (`:636`), `→ cassini_state` (`:552`), `→ surface_albedo` (`:781`) | three consumers, no supplier of an ocean fraction. **Measured 2026-09-04** (`ocean-fraction-context-notes.md`): `f_ocean` means three different things to its three consumers (surface inventory · subsurface ocean · the dynamo doc's "water-rich" bulk class), and the dynamo edge's real payload is `ice_mass_fraction`, which reaches `dynamo_rocky` today by the ladder (regime 4, ℳ_base 0.002 — confirmed to fire). The structural half — water fraction → interior → `cmb_heat_flux` — **could not be tested: the interior does not converge at 0.1 / 0.3 water on an Earth-mass rocky body** (branch ③), and the unconverged trials put the CMB *hotter* (2 526 → ~4 400 K), not cooler as the doc says, so at Earth's declared 3 760 K there is no jump and `cmb_flux` refuses. **Superseded the same day by C24's fix**: the column now converges — ice 0.1 → T_cmb **3 105 K**, ice 0.3 → **3 050 K** (dry 2 526) — still hotter than dry, opposite to the doc, but a converged size; C17's structural half is measurable now, start separate. **Stays open, two reasons named**: (1) the interior does not converge on a water-rich rocky body — **C24**; (2) the doc's mechanism sentence (item 4) carries **no citation** (item 3 beside it cites Gaidos 2010) and its temperature direction is the opposite of what our unconverged column shows — so the mechanism is both ungrounded and untested. Nothing wired. The Ganymede anchor 2×10⁻³ is RM22's relayed *observed* value (its ref. 3), not its computed 0.003 — both now written. **Opened by the owner and closed the same day, 2026-09-04 — ③b** (`ocean-fraction-context-notes.md` §5): the −55 K is a real turnover (noise floor 0.7 K; converged points 2 526 → 3 105 → 3 065 → 3 050 K at 0 / 0.1 / 0.25 / 0.3), its maximum unbracketed below 0.1 because 0.05 / 0.15 / 0.20 do not converge (a C24-adjacent coverage finding, recorded, not repaired); with Earth's declared 3 760 K the boundary-layer Q_C *rises* 2.75 → 3.11 → 3.20 TW (eq. 39 viscosity beats the smaller jump), C14's T_c falls ~90 K, C15's band moves (−69 → −68 → −82 MW/K) and still straddles zero — **the mechanism is real and measured; C15 cannot use it.** Item 4 corrected (en + ko) as a correction of our own uncited sentence. Nothing wired. |
| **C18** | `body_class → dynamo_rocky via sub_neptune` (`:623`) | a sub-Neptune integrates (C1) and has no dynamo path. **Closed 2026-09-04 as a named refusal — corrected the same night after the parallel seat found the paper the first wording said did not exist.** The refusal, in its final form: **the on/off criterion for a sub-Neptune iron-core dynamo *is* published** — Tang, Fortney, Nimmo, Thorngren, Ohno & Murray-Clay 2025 (`2025ApJ...989...28T`, owner-obtained, cached) §4.2: `Rm = μ₀σUD` (eq. 46), critical 50, `U` from Christensen 2010's scaling (eq. 47), `F_conv = F_CMB − F_cond` (eq. 48); abstract: *"Dynamo action in sub-Neptune iron cores persists as long as the mantle surface remains molten, often exceeding 10 Gyr"*. **The moment / field-strength scaling is not published** — in 37 pages *magnetic moment*, *field strength*, *Gauss*, *Rossby*, *dipole* and *field* itself occur zero times (reproduced). `dynamo_rocky` needs ℳ, so **this edge closes**; what opens instead is the *existence* question, listed as **C23**. *(The first wording — "no held paper prints a scaling" — was true of the cache and false of the literature; it is withdrawn.)* Two things recorded for the next seat: (i) **the three refusals are not one statement and they form a round trip** — `dynamo_rocky` sends the class to `dynamo_giant` (*"거대행성·서브넵튠은 dynamo_giant 의 몫"*), `dynamo_giant` sends it back by mass (`GIANT_M_MIN` 0.3 M_J = 95 M⊕, and its ground is helium rain, nothing to do with an iron core), and only `core_state` states the actual question (*"그 핵을 받는 다이나모 갈래가 아직 없다"*) — with the cause written as *no consumer*, not *no published scaling*; (ii) **`sub_neptune` sits in `CORELESS_CLASSES` (`core_state.py@«NOT_THIS_NODES_QUESTION = ("giant", "gas_giant", "ice_giant", "sub_neptune",»`; the constant was named `CORELESS_CLASSES` when this was written and was renamed by C23 on 2026-09-06 — that rename is the repair this line records as outstanding) while its own refusal says the iron core is there under the envelope** — the constant's name and its reason disagree; recorded, not repaired. The edge stays `status: gap` — a real coupling with no supplier. |
| **C19** | `body_age → dynamo_giant via cooling_luminosity` (`:614`) | the giant dynamo wants a cooling luminosity L(M, age) that no node emits  **Measured 2026-09-04** (`giant-dynamo-age-context-notes.md`): the giant branch consumes the age directly (the −0.33 exponent is the cooling track) — `run.py` gives Polyphemus 344.7 µT from `body_age` alone, so for giants the edge was **already wired, mislabelled** (now `via: t_body`). **Narrowed to the brown-dwarf branch** (13–70 M_J), where it stays a gap and is a *roster* gap: Luhman 16 A/B (33.5 · 28.5 M_J, 0.5 Gyr) return out-of-domain. Two consumers wait on the same missing cooling track (`dynamo_giant`'s BD branch, `internal_heat_nontidal` for giants). Request: a Burrows / Baraffe-class L(M, age) track, grounded before read-in. **Built 2026-09-04 (daytime, owner-released, outside the interior stem)**: the brown-dwarf branch runs RC10 eq. 1 on the DB's *measured* bolometric luminosity (isolated brown dwarf ⇒ L_bol is the cooling luminosity; declared `isolated`), b_eq = B_dyn/(2√2) with no depth attenuation, emitted as a band over the declared radius; Luhman 16 A 1.25 kG (1.10–1.43), B 1.18 kG (1.04–1.35). The `cooling_luminosity` gap edge closes. **What did not happen**: no downstream wiring (`magnetosphere_geometry` has no recipe), `internal_heat_nontidal` for giants still waits. `giant-dynamo-age-context-notes.md` §5–§6. |

**C16, measured 2026-09-06 against Driscoll & Olson 2011** (`engine/regime-gate-context-notes.md` §6): the three-name refusal is now two. `q_conv` is resolved as the **super-adiabatic excess per unit CMB area** — the paper prints `Q_conv = Q_c − Q_ad` and, separately, its own convention `q₁ = Q₁/A₁`; the relation for `q_conv` itself is never printed and follows from that convention. ⚠ `ν` is **not** resolved and the paper carries a decoy: its 6.2e16 m²/s is the **mantle's**, from post-glacial rebound. ⚠ `Rossby` and `Ekman` occur **zero times** in DO11, so the Table 8 discrepancy stays RM22's own. `c_d = 0.2` is printed and conditioned on *fast rotating dipolar*, a condition the paper never makes numeric — and it sits on the B_c path, not this gate. ⚠ Nothing evaluates on any body regardless: `tidal_locking` has no recipe, so every body takes `NO_LOCK` before the refusal is reached.

### C20 — the thermal-history integrator (forward integration in time) — **listed 2026-09-03; released 2026-09-04 ("C20 ㄱㄱ"), pre-registration and design in `core-thermal-history-context-notes.md`**

**Built 2026-09-04 (daytime)** — `core_history.py`, node `core_thermal_history`, 11th recipe. ⑤ converged (0.001 %, sweep on demand), ① T_c 4 027 K inside C14's band with a colder, low-surface-flow history (the pre-registered (나) direction — recorded, 0.70 unmoved), ② never nucleates (consistent with C14, unlike Nimmo's nominal), ④ −36 K/Gyr inside 33–126, **③c: the four-corner ΔE_min band −259…+32 MW/K straddles zero — C20 built, C15 still cannot say.** Run record: `core-thermal-history-context-notes.md` §4. **§5 (same day)**: against the observation the surface heat flow is ~25 % low like for like (Davies 2013 via Nimmo & Primack); eq. 35 reproduces Nimmo's Table 4 exactly, so the miss is the mantle temperature; two diagnostics (report, not adopt) show **both halves of the mantle-side miss are Nimmo's conventions** — the crust in the mantle equation and a uniform-density (10 % heavier) mantle — while **the inner core never appears on any convention** (Ⓑ) — and the same afternoon a melting-curve diagnostic (Ⓧ) **demoted** C14's finding: the pure-iron curves agree, the ~540 K gap at ICB pressures is the light-element depression (ours ×0.80, declared, consistent with Sinmyo's measured ICB; Nimmo's ×0.89, Alfè ab initio), and on his factor our adiabat freezes an oversized 2 000 km core. The inner core hangs on one declared factor; not decided here. Hypothesis recorded, not tested: the parametrised equations and their conventions may be a package. The initial condition is a reading (25th declaration); ΔE_min is insensitive to the conventions.

Owner's approval, verbatim (session `4b8e06ba`, 09-03 17:55): *"적분기 c20, ㅇㅇ 그게 좋겠다. 작은 의견 몇개.
행성의 생성 시기는 모천체의 생성시기로, 그리고 방사성 동위원소 관련 열 생성도 같이 넝어야 할 것같아."* (quoted as
typed; the last clause reads "넣어야" — radiogenic heat production is to be included).

**Why it is open.** The entropy-production verdict is a statement *over time* — "enough to run a geodynamo
for the last ~3 Gyr" — and no present-epoch value answers it. When the owner adopted the ladder (*"ㄱㄱ 하자."*,
`1588ff47`, 09-03 11:19, as the directing seat relays it), the entropy route was not closed but *deferred until
an integrator exists*, and that deferral had no address anywhere in the documents. This row is the address.

**What it is.** The coupled mantle–core energy balance rolled forward over 4.5 Gyr at `h = min(4 Myr, 0.1·τ)`
— Nimmo's 4 Myr is the cap and τ the mantle time constant (Brief 157); ≈1 150 steps on Earth. Brief 45 ended at its (c) stop for exactly this reason: `Q_C` depends on `T_c` at every step and the
core's equation is driven by the same `Q_C`, so neither half can be integrated alone. A different kind from the
spatial integration (shooting, already built) and from C14's root-find (no integration).

**Two design conditions from the owner, in the same message:**
1. *"행성의 생성 시기는 모천체의 생성시기로"* — the integration's t = 0 is pinned to the **star's / system's
   age**, not a per-body declaration; one declaration fewer. ⚠ **This conflicts with the graph as it stands**:
   `chain.yaml@«body_age:»` `body_age` is `kind: measured`, `domain: given`, layer 0, with the note *"천체 자신의 나이.
   항성 나이와 다르고, 거대행성 냉각광도의 실입력이다"*, and `system_age` (`t_sys`, `chain.yaml@«system_age:»`) is a separate node
   (`:666`: *"항성풍의 나이는 항성의 나이 = 계의 나이"*). **Resolving the `body_age` / `system_age` relation is a
   prerequisite of starting C20** — recorded here as a fact, nothing in `chain.yaml` changed.
   *Correction, same evening: it is the note that is out of step with the roster, not the owner's condition
   that makes a new rule.* The owner asked (`4b8e06ba`) *"천체 나이와 행성 나이가 얼마나 차이가 나지? 적분
   스텝보다 작으면 구분하는 의미가 없을거같은데"*, and the answer was already in this file: C9's time-axis
   paragraph (2026-08-31, above) puts the star–planet difference at the **Ma** scale — Neumann & Kruse's
   t₀ ≈ 1.3–1.9 Ma (§3.3) and "no differentiation for t₀ ≥ 5.5 Ma" (§3.4), read there from the cached text
   — which is the size of one ~4 Myr integration step, so a Gyr thermal history cannot resolve it.
   ⚠ *2026-09-08, after Brief 157 made the step adaptive: **this ground no longer holds.** Earth's first
   step is 0.393 Ma and Mars's 0.0053 Ma, so a 1.3–1.9 Ma offset is several steps, not one. The
   decision may still be right for other reasons — **the ground needs restating, and the decision is
   left standing until it is.*** A printed
   number now stands under that: Lichtenberg+ 2019 (`2019NatAs...3..307L`, preprint, cached), `.tex:216`:
   *"Disk lifetimes are distributed around 5 Myr, which is controlled via the photoevaporation rate"* (their
   ref. `2013A&A...549A..44F`) — planet formation ends within about one step of the star's birth. And the
   roster already does this: `bodies/alpha_centauri_a_b.yaml` and `bodies/pandora.yaml` both carry
   `age_gyr: 5.3` (the system's age), `earth.yaml` 4.54; only the `chain.yaml@«outputs: [t_body]»` note says otherwise.
   ⚠ **The opposite trap, from the same C9 paragraph, rides with this**: *"Feeding `body_age` (Gyr) into
   this node would give it the number it is least sensitive to while the number it is most sensitive to
   stays undefined"* and *"Do not draw a `body_age → porosity` edge … it must carry `t_form` (Ma after CAI),
   not `t_body` (Gyr); a Gyr endpoint is at most an `influences`"*. Unifying the age does **not** make age
   the input for everything; the Ma-scale consumers keep needing `t_form`, which no body declares.
2. *"방사성 동위원소 관련 열 생성도 같이 넝어야 할 것같아"* — **wiring, not building**: `radiogenic.history_factor`
   is that input already, and the module says so (`radiogenic.py@«What this module does not do: thermal evolution. H(t) is four exponentials and is built; turning it»` *"H(t) is four exponentials and is
   built"*; `radiogenic-budget-context-notes.md@«**H(t) is built and NOT wired to the third consumer.** `→ dynamo_rocky via geotherm` (`:404`) asks whether the core is *still* convecting, which needs thermal evolution — Nimmo+ 2004.»` *"H(t) is built and NOT wired to the third consumer"*).
   Condition 2 names exactly that unwired consumer. **But it is half of radiogenic heating, and the row must
   say which half**, or the next seat reads "radiogenic heat included" as complete:

       long-lived  (K · Th · U)          → `radiogenic.history_factor`, built; wireable into C20
       short-lived (²⁶Al · ⁵³Mn · ⁶⁰Fe)  → the formation pulse; needs t_form (Ma after CAI), which we do not hold

   The short-lived half is **closed as a named refusal, not open** (`radiogenic-context-notes.md` §3: *"the
   term is real and can dominate for small early bodies; we decline it because the input does not exist
   here"*; to reopen it needs a declared formation epoch on the body, the two half-lives, and initial
   ²⁶Al/²⁷Al · ⁶⁰Fe/⁵⁶Fe ratios from a held source). For the 4.5 Gyr history C20 aims at, the formation
   pulse is outside the window anyway — no loss for C20 — but "radiogenic heating is in" means the long-lived
   half only.

**Cost.** A dozen-odd core constants (heat capacity, expansivity, latent heat, gravitational-energy
coefficient, light-element content …), an initial-condition declaration, and **the condition that the model is
calibrated on Earth** — its success criterion is "reproduce Earth's present state", so the output is
"consistent with an Earth-calibrated model", not "this body's actual value".

**Relation to C14.** C14 *declares* `dT_c/dt` and solves the present epoch only (honest band 33–126 K/Gyr,
4× between two published Earth models). **When C20 stands, that declaration becomes a computation**, and a
body kept warm by tides and one that cooled quietly finally get different answers — the thing the ladder
cannot do.

**Start condition.** Not now. Order: P3 → C14 → then reconsider. **First real consumer, 2026-09-04: C15** —
`core_entropy_production` emits `entropy_history_verdict = "cannot-say (needs C20)"` on every result, because
two of Nimmo's three dynamo criteria (mean and minimum ΔE over the last 3.1 Gyr) are history quantities and
the discriminating one is ΔE_min; a present-day φ cannot answer them. C20 stops being a listed-only item.

#### C20 (i) 2026-09-19 — Mars is given a lid thickness, and nothing moves

Decision 8 routes a `stagnant` body to Foley eq. (3) and reads δ **from the body file**. ⚠ **No body file had one** — a `git grep` for `lid_thickness`, `delta_km` and `lid_km` across `engine/bodies` returned nothing, while the declared regimes are Earth `mobile`, Pandora `mobile`, Mars `stagnant`. **So decision 8 as frozen would have sent Mars to its own named refusal and deleted its C20 outputs**, and its acceptance — *print Mars's today `T_p` before and after* — could not have been met. *Its trap 1 forbids moving the law and δ together, so the input landed first, alone.*

**`engine/bodies/mars.yaml` gains `lid_thickness_km: 330.0`, `grade: analog`, `source: 2011Icar..212..541M`** — Morschhauser, Grott & Breuer 2011's present-day stagnant lid. ⚠ **It is the quantity eq. (3) takes**: the paper defines `Dl` as the lid thickness, and the ~250 km elastic thickness printed in the same sentence is a **different quantity** that neither confirms nor refutes it. **The grade is `analog` because the number is a model output, not an observation**, and the declaration writes its own refutation site: *an observational lid-base thickness, an InSight-class result, not another model.*

⚠ **The declared value sits below the tool's sweep band.** `engine/tools/c51_regimes.py` sweeps **350–500 km**; the declaration is **330 km**, and the tool is untouched. **A sweep range and a declaration are different objects, and they now coexist on purpose** — *so the tool has never evaluated Mars at Mars's own lid thickness, and when decision 8 lands it will be the first time that happens.*

**The gate says nothing moved.** `gate-0fed555b.log`, `rc=0`: `[PASS]` **753** · `[FAIL]` **0** · `[SKIP]` **13** · `[판정` **5** · `[GRADE]` **4** · `[STOP]` **1** · `[STEP]`/`[COST]` **77** · anchors **602** · line-number citations **0** — every count identical to `b4b92728`. **`test_transfers.py` passes**, which is the gate confirming the value is *not* a transfer: `transfers:` records values that arrived **from another body**, its rule (iii) requires the anchor to be a phrase citation into another file — the form written `<file>` then `@` then the phrase in guillemets — and a paper reference cannot live there. ⚠ *Had it been written into that block, the step would have refused it by name rather than pass quietly.*

⚠ **`instr` and seconds were deliberately kept out of the "nothing moved" acceptance**, and the run shows why: wall clock read **1 926.97 s** against the previous run's **1 912.91 s**, **+0.7 %**, on an edit that no code reads. **An equality test on those would have failed for reasons unconnected to the change.**

#### C20 (j) 2026-09-20 — the declared regime now chooses the loss law, and two rulers were corrected on the way

**A rocky body's mantle loses heat through whichever lid it has**, and the two regimes are not two settings of one law. `engine/core_history.py` now reads the body's `tectonic_regime` and routes a lid regime to **Foley 2018 eq. (3)** and everything else to **Nimmo+ 2004 eqs 34–36**. Mars, declared `stagnant` with `lid_thickness_km: 330.0`, is the first body ever evaluated at its own declared lid thickness — `engine/tools/c51_regimes.py` sweeps **350–500 km**, and the declaration sits below that band.

**Same body, same inputs, only the law**: `t_m` **1378.076674658375** on Nimmo against **1774.674973674531** on Foley. ⚠ *Only the direction was registered, and only the direction is claimed.* **1739 K is not a target** — that number belongs to a mantle-only integrator started at 1750 K, and a near miss would be a coincidence of two configurations.

⚠ **A draft compared the declaration block to a string, which is always false.** A stagnant body would have cooled on the mobile law **silently**, with `loss_law` honestly reporting the law that actually ran. It surfaced only because the neighbouring key died with `TypeError: unsupported operand type(s) for *: 'dict' and 'float'`: **the cell that failed loudly caught the one that was failing quietly.**

**Refusals, all by name**: a lid regime with no thickness; a lid outside its own mantle (reusing `mantle_budget`'s wording, so the message matches the guard in `91f5440b`); a declared regime with no mapping; and a surface temperature that is absent or not finite. ⚠ **That last check reads the *unwrapped* value** — a block whose `value` is missing passed the earlier form and then died unnamed inside the law.

**Two rulers were corrected while landing this.**
⚠ **Foley eq. (3) does not respond to the surface temperature, and that is measured, not argued.** Holding everything else fixed and moving `t_s` 216 ↔ 293 K returns **the same number to sixteen digits** (`0.002130395885779607` at `T_p` 1400 K; `0.03887510417178484` at 1800 K) — the leading `(T_p − T_s)` cancels against the ΔT inside `θ^(−4/3) Ra_i^(1/3)`. *The reading that ΔT enters twice and therefore matters is wrong for this law.* ⚠ **The cancellation is exact, not coincidental**: `θ ∝ ΔT` and `Ra_i ∝ ΔT`, and `Nu = a·θ^(−1−β)·Ra^β` at `β = 1/3`, so `F ∝ ΔT^(−4/3 + 1/3 + 1) = ΔT⁰`. **Nimmo does move**: `q_m` **3.609e12 → 3.300e12 W** across the same two values. The argument is still passed, because the cancellation is a property of this fit rather than a promise of the law, and because leaving it out restores the asymmetry where `g` and `d_m` are the body's and `T_s` is a module default.
⚠ **The witness lines are a ruler and stay fixed.** `engine/test_core_history.py` builds its own `params`, so a change to `mars.yaml` does not move them — which is what makes them usable as the bit-identity check for the untouched branch. *A ruler that follows what it measures is not a ruler*, so they were deliberately not wired to the body file.

⚠ **Mars's `core_thermal_history` output does not move in this commit.** Mars is `stagnant`, so it runs Foley, and Foley does not see the surface temperature. What moves is the **counterfactual** `[증인·법칙]` line — Mars with its regime removed, on Nimmo — from **1378.076674658375** to **1358.4226002593311**, and `[전이·pending]` from **1** to **0**. *A declaration that replaces an inherited placeholder changed no published value here, and saying so is the point of the line.*

**What the red gate taught.** `d6dd5463` failed alone and `393c9489` turned it green; they are one landing read together. ⚠ **Adding a required input means walking every direct call site** — three files had to follow (`test_core_history.py`, `tools/mars_step_sweep.py`, `test_domain.py`), found one gate run at a time when one `git grep` would have found all three. ⚠ **And an anchor's input trigger reaches non-Python files**: this is the first time `chain.yaml`'s byte digest moved it.

**Departures from the frozen registration, recorded rather than absorbed.** *Undeclared regime takes the Nimmo law* (as registered) rather than refusing; routing it to a refusal would delete C20 for any body that never declared one. *Acceptance A reads as «existing value keys unchanged, plus one declared addition»* — `loss_law` and `loss_law_reason` are new returns. *Foley's 273 K module constant is now fixture-only.* *The 216 K registration's acceptance E was closed in the parent commit*, where the finite-number check landed. ⚠ *The two `seconds` in the re-frozen anchor were taken on a run whose clock loop read **−12.5 %**, outside the ±5 % band — they record today's noise and gate nothing.*

⚠ **One item found and not fixed**: `[PASS] 컨벤션 점검 통과` is not a verdict about conventions. `scripts/check.sh` keeps `fail` as a script-wide accumulator, so an unrelated earlier failure deletes that line even when the section's own checks passed — which is exactly what the red run showed. A local variable closes it.


#### C20 (k) 2026-09-20 — Mars's surface temperature stops being Earth's, and nothing published moves

**`engine/bodies/mars.yaml` declares `surface_temperature_k: 216.0`** (`analog`, `2016JGRE..121.2386P`), replacing the **293.0** it had carried for one commit as an explicit inheritance from Earth. That 293.0 was never a Mars number: it was `mantle_flux`'s module default lifted into a declaration so the substitution would be visible while a source was found. The `transfers:` entry that recorded the inheritance is removed — the value no longer comes from another body.

⚠ **Mars's `core_thermal_history` output does not move.** Mars is `stagnant`, so it runs Foley eq. (3), and that law is exactly insensitive to the surface temperature — `t_m` stays **1774.674973674531**. *So this commit did not change an answer; it changed where the answer's input comes from.* **Reading it as «216 K shifted Mars by so much» would be wrong in both direction and size.**

**What did move, in full:**

| quantity | before | after |
|---|---|---|
| the counterfactual `[증인·법칙]` line — Mars with its regime removed, on Nimmo | **1378.076674658375** | **1358.4226002593311** (−19.65 K) |
| `[전이·pending]` | **1** | **0** |
| anchors | **606** | **605** |
| the registered direction, Foley over Nimmo on one body | **+396.60 K** | **+416.25 K** |

⚠ **The anchor count falls rather than rises**, which is the opposite of what adding a source usually does: deleting the `transfers:` entry took its phrase anchor into `earth.yaml` with it, and a bibcode inside a body file is an off-repo citation that the anchor rule never counted. *The new source is cited and the anchor total drops by one; both are true.*

⚠ **The pending counter has still caught nothing.** It was added in the parent commit, counted exactly one entry — this one — and returns to zero here. **It has not yet survived long enough to catch a placeholder anybody would otherwise have missed**, which is the case it exists for.

### C21 — the short-lived radiogenic formation pulse (²⁶Al · ⁶⁰Fe) — **listed 2026-09-03, not started**

Owner: *"단수명도 파긴 해야겠네."* (`4b8e06ba`, 09-03 18:10) and *"등재하고 측정은 그때 가서."* (18:17) — listed
now, measured when it is started.

**Why it opens.** `radiogenic-context-notes.md` §3 closed this term as a named refusal and **narrowed the
ground of the refusal on purpose**: *"The refusal rests on our missing input, not on borrowing their
conclusions"* and *"Neither says ²⁶Al is negligible for a small body that formed early — Monteux says the
opposite for 10–100 km objects, a class the roster may want."* The owner's judgement is that sentence's.

**Two design proposals from the owner, verbatim:**
1. *"단수명 방사성 원소가 소멸할 때까지의 구간만 촘촘하게 적분하는 식으로 접근하면 안되려나?"* (18:10) →
   **a variable step.** Half-lives ²⁶Al 0.73 My · ⁶⁰Fe 1.5 My (Monteux+ 2016 lines 187–191, held, quoted
   verbatim in `radiogenic-context-notes.md` §3, citing Carlson & Lugmair 2000): integrate the first ~10 Ma
   finely (0.1 Ma steps ≈ 100 steps), then C20's steps. **C21 is the first ~10 Ma of C20's time axis.**
   ⚠ **Restated 2026-09-09 on the measurement, replacing three phrases this seat had written** (the
   owner's proposal above is verbatim and untouched): the cost is **≈86 additional steps, not ≈100**, on
   a base of **1 152** rather than ~1 100, because **14 of the window's steps already exist**; the claim
   *"there is no other way"* is **withdrawn** as unproven; and *"a uniform 4 Myr step cannot see the
   pulse at all"* becomes **body-dependent** — Earth resolves the ²⁶Al half-life with about **1.4
   samples** (one step is 0.520 Ma at t ≈ 1.4 Ma), while **Mars already resolves it**, 32 of its 56
   window steps sitting under 0.1 Ma. **The fine interval is still needed, and Earth is why.**
   ⚠ *2026-09-08: **the step is no longer uniform, so what was arithmetic here is now a measurement.***
   *Measured by re-running the two integrations at this tree and printing one column (C47 (i)) — the stage-0 JSON
   carries per-run scalars only, no rows: the first 10 Ma holds **14** steps on Earth (h 0.393 → 1.304 Ma)
   and **56** on Mars (h 0.0053 → 0.906 Ma, 32 of them under 0.1 Ma). So C21's fine sampling is still needed
   on Earth — at t ≈ 1.4 Ma one step is 0.520 Ma, about **1.4 samples per ²⁶Al half-life** — but three
   phrases above must be restated: «cannot see the pulse at all» (14 steps land in the window, not none),
   «there is no other way» (unproven), and «≈100 steps on top of C20's ~1 100». **Re-judging the design
   belongs to C21's start, not here.***
2. *"초기비의 경우에는 계 단위로 그냥 랜덤한 시드값을 넣는게 어떨까?"* (18:17) → **a system-level seeded value**,
   with two conditions attached together: **the system is the right unit physically** — ²⁶Al enrichment is a
   property of the star-forming environment, so the bodies of one system share it; drawing per body is wrong.
   **And it lives in a different layer** — a draw is an art / gameplay decision, not grounding, so it belongs
   in the **Phase 4 gate override**, not in the engine; the engine goes as far as *"accept a declared ²⁶Al₀
   with its band"*. An engine that rolls its own dice blurs measurement and draw the day a measurement
   arrives. The synthetic-eccentricity concept sits in that layer for the same reason, and its guardrails
   move over unchanged: never overwrite a measured value · reproducible from the seed · labelled synthetic.

**⚠ Two prerequisites before starting:**
- **(a) There is no *measured* distribution to draw from — and the relayed range was wrong.** The *"0–10×
  solar ²⁶Al₀"* that C9's paragraph carried as *"reported by the directing session … not re-read here"* was
  re-read on 09-03 once the owner supplied the paper: **Lichtenberg+ 2019** (`2019NatAs...3..307L`, cached as
  the **arXiv v1 preprint** — its own title block says *"preprint differing from journal version"* — with
  LaTeX source; identifier read from ADS, matched to page 1). `Al26_desiccation.tex:216`: *"we consider
  values in the range ²⁶Al₀ ∈ [0.1, 10] × ²⁶Al_⊙"*, with *"the solar system's 'canonical' ²⁶Al value … of
  ²⁶Al_⊙ = (²⁶Al/²⁷Al)₀ = 5.25 × 10⁻⁵"* (their ref. `2013M&PS...48.1383K`). **The floor is 0.1, not 0** — and
  for a threshold-type output that is material: a draw of 0 means no ²⁶Al and therefore never
  differentiates, 0.1× does not. ⚠ **Label the range for what it is**: *"the range a published model
  scanned"* ("we consider values in the range"), **not an observed distribution** — the order-of-magnitude
  variation it motivates is cited to nine papers (`2014ApJ...789...86A` … `2018PrPNP.102....1L`) that are
  **not held**. Also printed and usable by the dominance measurement: planetesimal radii scanned [1, 100] km
  with *"r_plts ≳ 30–50 km"* expected (`Al26_desiccation.tex:88`, `Al26_desiccation.tex:112`); ²⁶Al half-life **≈ 0.72 Myr** (`:86`) against Monteux's
  quoted **0.73 My** — two printed values, both carried with their source, the choice made in the measurement
  brief; initial water-to-rock ratio `f_H2O,init = 0.3` (`:172` ff.). Data availability: *"available from the
  corresponding author upon reasonable request"* (`:219`) — no deposit; not needed, the ranges and anchors are
  printed; **not put on any request list**.
- **(b) Measure dominance first** (owner: *"측정은 그때 가서"* — not now; first thing when started). Monteux's
  "major role" is for **10–100 km** bodies, and the paper's own planetesimal scan is [1, 100] km with
  ≳ 30–50 km expected (above); the roster's moons are **400–5724 km** on the committed board
  (`phase4/alpha_centauri.yaml`, the `moons:` body definitions at main's HEAD: Chaos 400 · Hades 750 · Dante
  900 · Cassandra 3400 · Pandora 5724 km — Dante is being resized in an uncommitted main working tree, so no
  judgement here hangs on its value). **That is an order of magnitude above the paper's premise, stated as
  the premise gap, not as the result** — whether the formation pulse is actually dominant for *our* bodies is
  still a measurement: the two held half-lives plus a solar initial ratio give each body's pulse
  energy, compared against the long-lived budget — the `ice_x` / ammonia-ceiling template. If it does not
  reach, the refusal stands; if it does, (a)'s paper request and a declaration grid become justified.

**A width warning, left as a question for the owner.** Two declarations multiply here — `t₀` and ²⁶Al₀ —
and C9's paragraph prints the shape of the answer: wet olivine succeeds only for t₀ ≈ 1.3–1.9 Ma (§3.3),
antigorite does not differentiate at all for t₀ ≥ 5.5 Ma (§3.4). The output is **a threshold verdict, not a
continuous spectrum**. Following C11 ("the grid is the answer, no pair is elected"), the honest product is
*"this body may or may not have differentiated, depending on t₀"* — **whether that product is worth having
is the owner's decision**, not settled here.

### (b) measured 2026-09-07 — the answer is `t₀`, and the refusal is renamed rather than lifted

⚠ **What this measurement can and cannot be about (owner, 2026-09-07).** *"우리 천체는 아바타 설정
기반이라 원래 지어낸 거고 확증할 방법이 없잖아. 반박 안 된 거지 이거는."* **Our moons are ours.** A
calculation about them is arithmetic on objects we defined, not a measurement of the world, and there is
no fact for it to be refuted by. Two statements are therefore mixed in what follows and are kept apart:

| statement | kind | testable? |
|---|---|---|
| the pulse meets the melting requirement at `t₀ ≈ 1.4 Myr` | about physics | **yes** — against real meteorite parent bodies |
| three of our moons sit below that | about our design choices | **no**, and not the kind of thing that could be |

⚠ **So "the pre-registration was refuted" was the wrong frame**, and it is struck. What was actually
wrong was an inference: the roster was summarised as *"all too large for the pulse to matter"*, and the
**400–750 km three are not that large.** A rough generalisation, not a world that surprised us.

⚠ **The recipe this section wrote for itself was not executable.** It said *"the two held half-lives
plus a solar initial ratio give each body's pulse energy"* — they do not. A half-life and an isotopic
ratio give a decay rate, not an energy: the decay energy per atom and the aluminium content of the rock
are both needed, and **Monteux prints neither.** Monteux gives only the two half-lives (attributed to
Carlson & Lugmair 2000), and its *"major role … for 10 to 100 km size objects"* is itself a citation to
**Yoshino et al. 2003**, not a Monteux result. **The premise this item has been quoting belongs to a
paper we do not hold.**

**The constants.** Abundances from Neumann+ 2019
([`2019ApJ...882...47N`](https://ui.adsabs.harvard.edu/abs/2019ApJ...882...47N), held), Table 2 —
stable-isotope mass fraction `8.86×10⁻³`, initial ratio `5.25×10⁻⁵`. ⚠ **Read from the publisher's HTML
table cells, not a page image** — the cache holds no PDF for this paper, and cell boundaries remove the
layout guessing that cost a factor of 4.4 on 2026-09-06.

⚠ **The energy is NOT that table's `6.416×10⁻¹³ J`, and an earlier version of this section used it.**
Ruedas 2017 ([`2017GGG....18.3530R`](https://ui.adsabs.harvard.edu/abs/2017GGG....18.3530R), held)
Table 2 prints both quantities for ²⁶Al in one row, and the difference is the whole point:

| | keV | J | what it is |
|---|---|---|---|
| `Q` | 4004.393 | 6.416×10⁻¹³ | total decay energy — **identical to Neumann's figure** |
| `E_H` | 3150.155 | **5.047×10⁻¹³** | heat-effective, after the neutrino is subtracted |
| `H` | | 0.3583 W/kg | specific heat production per kg of ²⁶Al |

Ruedas states why: *"a part `E_ν` of the energy is carried away by a neutrino or antineutrino, whose
interaction with matter is almost nil and **which therefore does not contribute to heat production**"*,
giving `E_H = (m_P − m_D)c² − E_ν`. **A neutrino does not warm a moon.** Every number below uses `E_H`,
and the earlier ones were **1.271× too high**.

⚠ **This was not a conflict between sources — it was one seat's inconsistency.** Bierson & Nimmo 2019
([`2019Icar..326...10B`](https://ui.adsabs.harvard.edu/abs/2019Icar..326...10B), held) print
`0.355 W/kg`, within 0.9 % of Ruedas's `H`, and this section first read that 28 % gap as two papers
disagreeing. They never did. **What made it visible was a falsification test**: our own long-lived
table agrees with Ruedas to 0.1–1.5 % on all four nuclides, so it is already heat-effective — and the
question became *why does only ²⁶Al differ?* **Because only there had `Q` been substituted by hand.**

⚠ **And an argument used the day before was weaker than it looked.** "Our long-lived table matches
theirs, so the conventions match" — our table is Nimmo & Primack, theirs is Robuchon & Nimmo. **Shared
lineage, not agreement.** Ruedas is the third lineage that actually settles it.

**Three axes, because the three ask different questions.** The pulse's energy per kilogram does not
depend on body size; size enters only by changing what it is compared against.

| what the pulse is compared with | J/kg | pulse ÷ it, at `t₀ = 0` |
|---|---|---|
| long-lived K·Th·U, integrated over 4.5 Gyr | 5.461×10⁵ | **9.59×** |
| sensible heat to the surface solidus | 1.693×10⁶ | **3.09×** |
| gravitational binding, Chaos (400 km) | 5.405×10⁴ | 96.9× |
| gravitational binding, Dante (521 km) | 1.193×10⁵ | 43.9× |
| gravitational binding, Hades (750 km) | 2.669×10⁵ | 19.6× |
| gravitational binding, Cassandra (3400 km) | 1.060×10⁷ | 0.494× |
| gravitational binding, Pandora (5724 km) | 2.693×10⁷ | 0.195× |

The first axis is the one this section specified. The second is built from engine materials: `C_PM`
1200 J/(kg·K) (`mantle_flux.py`, eq. 32) across 250 K → 1661 K, the peridotitic solidus at surface
pressure from `eos.silicate_solidus`. The third was added here to make the size dependence visible, and
it does: the pulse dominates the small three and is dominated by the large two.

⚠ **The second axis is two questions, not one incomplete one.** An earlier version of this section said
twice that latent heat was excluded *"because no held source gives one for silicate"*, making the
requirement a lower bound. **Both statements were wrong.** `eos.py` carries
`SILICATE_MELT_DH = 4.0e5 J/kg`, cited to Monteux+ 2016 Table 1 — *"Specific enthalpy change ΔH
4 × 10⁵ J/kg (Ghosh and McSween, 1998)"* — **in the same file whose solidus function this measurement
calls.** And latent heat is not a missing piece of one number: it is spent *after* the solidus is
reached, so the sensible-heat figure was the correct answer to a different question.

| | requirement [J/kg] | what it answers |
|---|---|---|
| `C_p ΔT` | 1.693×10⁶ | heat enough to **begin** melting |
| `C_p ΔT + ΔH` | 2.093×10⁶ | heat enough to melt **completely** |

**But none of that is the answer, because the pulse decays with `τ ≈ 1.03 Myr`.**

| `t₀` [Myr] | remaining pulse [J/kg] | ÷ long-lived | ÷ solidus requirement |
|---|---|---|---|
| 0 | 5.240×10⁶ | 9.59× | 3.09× |
| 1 | 1.993×10⁶ | 3.65× | 1.18× |
| 2 | 7.580×10⁵ | 1.39× | 0.448× |
| 3 | 2.883×10⁵ | 0.528× | 0.170× |
| 5 | 4.170×10⁴ | 0.076× | 0.025× |

**A closure, and ⚠ a correction to how it was first described.** The `t₀` at which the pulse exactly
meets the onset-of-melting requirement comes out at **1.17–1.19 Myr** (**0.95 Myr** for complete
melting), and C9's paragraph prints *"for the wet
olivine rheology successful models live in t₀ ≈ 1.3–1.9 Ma (§3.3)"*. The threshold lands inside that
band.

⚠ **It was first written here as an *independent* closure "from a different paper". It is not.** C9's
Neumann & Kruse 2019 is [`2019ApJ...882...47N`](https://ui.adsabs.harvard.edu/abs/2019ApJ...882...47N)
— **the same paper whose Table 2 supplied every constant above.** What agrees is a hand-built energy
budget against that paper's own thermal-evolution model, using that paper's own numbers.

**So what the closure is worth, stated as two sentences that must travel together** — because either
one alone is misleading:

- ✅ **It is evidence the implementation is right.** From that paper's constants, a hand energy budget
  reproduces that paper's own modelled threshold. A dropped factor, a mis-set unit, a mistaken exponent
  — the failures that cost us a square root, an atomic mass and five significant figures **on this same
  day** — would each have broken it. That is a real check and not a small one.
- ⚠ **It is not evidence the constants or the framing are right.** Both came from the paper it agrees
  with. An outside check needs a source this measurement did not draw from, and there is not one here.

⚠ **And this is the one result here that does not depend on our bodies being invented.** Whether
Pandora exists has no bearing on whether a given set of constants reproduces a given threshold. Every
other line in this section is either physics we borrowed or arithmetic about objects we chose; **the
implementation check is the part that would still stand if the roster were replaced tomorrow.** Without
that sentence the whole item reads as void, and it is not.

**Reading only the second turns a genuine implementation check into nothing**, which would be the
opposite error and just as wrong.

⚠ **The mis-description mattered more than the number.** "Independent" was the word that made this look
like the strongest result of the day, and it survived one round of reporting before the bibcodes were
compared. **A closure is only as independent as its least independent input**, and checking that means
reading the citation, not the claim.

**The printed half-lives do not matter.** 0.73 My (Monteux), ≈0.72 Myr (Kimura), 7.17×10⁵ a (Neumann),
0.717 My (Ruedas) move that threshold 1.1896 → 1.1733 → 1.1684 Myr — **1.8 % across the whole spread.**
Per this engine's convention, all are carried and none is elected.

⚠ **Composition does matter, and our moons have ice.** The pulse scales with the rock fraction, since
aluminium rides in the silicate:

| rock mass fraction | pulse [J/kg] | ÷ begin melting | ÷ melt completely |
|---|---|---|---|
| 1.0 | 5.240×10⁶ | 3.09× | 2.50× |
| 0.7 | 3.668×10⁶ | 2.17× | 1.75× |
| 0.5 | 2.620×10⁶ | 1.55× | 1.25× |
| 0.3 | 1.572×10⁶ | ⚠ **0.928×** | ⚠ **0.751×** |

**At 30 % rock the pulse does not melt the body under either reading.** That row is not a corner of the
table — our moons carry ice, so it is the part that describes them.

⚠ **And the 50 % row survives, which both seats predicted it would not.** Working and directing seat
each expected latent heat to sink it; it comes out at **1.25×**. `ΔH` is **24 % of the sensible heat**,
not a comparable term. **Both guesses ran the same way** — an unquantified term assumed large enough to
overturn the result. **A term nobody has evaluated is not evidence for either side**, and estimating
its size in advance is how a table gets read before it is computed.

⚠ **Two numbers in the source disagree with each other.** Neumann defines `f_i` as *"the number of
atoms of **the stable isotope** per 1 kg"* and then prints `f_i = 10³ x_i N_A / m_{a,i}` *"with the
relative mass fraction x_i of the stable isotope, the molar mass of **the radioactive** isotope"*.
Counting ²⁷Al atoms requires dividing by 26.98, not 26. The tables above use **26.98**; the printed
formula gives **6.912×10⁶ J/kg**, 3.77 % higher. **Neither reading is elected here** — the paper prints
no initial heat-production rate to close against. The discriminant is recorded so the next person who
meets an ordinary-chondrite ²⁶Al figure can settle it without going looking: **`H₀ = 2.041×10⁻⁷ W/kg`
for 26.98, `2.118×10⁻⁷ W/kg` for 26.**

⚠ **What the two readings still do not answer, named so the next person knows where to start.**
Yoshino's *"major role for 10–100 km objects"* is a claim about **differentiation** — iron sinking —
and neither reading is that. **Onset is too little** (a trace of melt separates nothing) and **complete
melting is too much** (nothing has to melt entirely). The real criterion is a **melt-fraction
threshold**, and our two numbers bracket it rather than being it. ⚠ **The material is already in the
engine**: `eos.silicate_melt_fraction(p, t, variant)`, which its own docstring calls the single source
of truth for `φ`. **Not built here** — this item's job was the dominance question — but the bracket and
the tool are recorded together so the next step is a step, not a restart.

**What stands after both corrections**: an ice-rich body — rock fraction below roughly 35 % — is not
melted by the formation pulse under either reading, and above that the answer turns on `t₀`.

### `t₀` declared 2026-09-07 — late, and from the formation order rather than from our own threshold

**Owner**: *"늦게 잡는 걸로."*

⚠ **The reasoning must not run through our own answer.** "Our threshold is 1.17 Myr, so `t₀` is later"
would be choosing an input to produce a wanted output — the move this file refuses in three separate
places. **`t₀` is argued from the formation order, which knows nothing about our threshold, and only
then compared against it.**

**The order, from a held paper's abstract.** Canup & Ward 2002
([`2002AJ....124.3404C`](https://ui.adsabs.harvard.edu/abs/2002AJ....124.3404C)): *"the satellites form
in a circumplanetary accretion disk produced during the **very end stages of gas accretion onto
Jupiter**"*, with *"protracted satellite accretion times of 10⁵ yr"*. **A gas giant's moons post-date
the giant.** That is a statement about sequence, and it is the whole of the non-circular part.

⚠ **The clock is weaker than the order, and both belong in the record.** Nothing we hold measures when
Polyphemus finished accreting. The only Myr-scale figure in that paper is `τ_G = 5×10⁶ yr`, and it is
an **input to the worked figures** — *"Figure 5a shows … for τ_G = 5×10⁶ yr"* — a model choice, not a
measurement of Jupiter. **It is cited here as the scale the literature works at, nothing more.**

**So the declaration is:**

> `t₀` for these five moons is **after Polyphemus finished accreting**. We have not measured when that
> was; the only figure in hand puts giant gas accretion at the **Myr scale**, against an onset
> threshold of **1.17 Myr**. **The formation pulse is therefore not available to them.**

⚠ **"Not available" rather than "certainly absent", because the two numbers share an order of
magnitude.** A giant that finished inside ~1 Myr would leave some pulse; nothing we hold says one did,
and nothing we hold rules it out. **The margin is not large and the record should not imply it is.**

### One path, and `t₀` is a declaration rather than a branch

**Owner, 2026-09-07**: *"우리 규칙대로, 모든 케이스에 대응 가능하게."*

⚠ **An earlier version of this section split into "branch A — moon of a gas giant" and "branch B — body
orbiting a star directly". That split is removed.** It was a hardcoded fork where this repository's rule
is a data-driven general path, and **the physics gives it no reason to exist**: both sides of the
melting comparison are energy per kilogram, so neither the body's size nor its type enters. **The only
thing that differs between a moon and a planet is `t₀`, and `t₀` is a fact about the body, not a code
path.**

    path      one. It does not ask what kind of body this is
    input     t₀, declared per body
    output    the melt ratios by rock fraction — the table already computed above

⚠ **Do not branch on `kind` to implement this.** C43, found the same day, is exactly that disease:
`body_class` applied a protoplanetary-disc criterion to a moon and filled the missing distance with a
silent default. **A second instance must not be built on purpose.**

**Where `t₀` comes from is a list of sources for a declaration, not a set of branches:**

| the body formed | `t₀` | grounds | who is here |
|---|---|---|---|
| in a circumplanetary disc, after its planet's gas accretion | late | Canup & Ward 2002 | our five moons |
| in the stellar disc, directly | as the disc gives it, possibly early | — | `bodies/earth.yaml` |

**Nothing is unimplemented.** ⚠ An earlier draft called the second row an "open branch with no roster
body"; **there is no branch to open.** The path is one, Earth already runs through it, and what a new
body brings is a `t₀` value — not a new route.

⚠ **And size does not enter the melting comparison at all.** This must be said plainly, because it has
been said loosely more than once today. **Both sides of that comparison are per kilogram**, so the body
mass divides out:

    pulse            5.240×10⁶ J/kg
    to begin melting 1.693×10⁶ J/kg      to melt completely 2.093×10⁶ J/kg

**A 10 km belt object and 5724 km Pandora read the same row.** What separates them is rock fraction,
nothing else. **Size enters only the gravitational-binding axis**, which asks a different question
(accretion heat), and *that* is where "large bodies are dominated by their own budget" belongs. Carry
the two apart or the record teaches that big bodies are safe from the pulse, which the table does not
say.

**What the roster holds today.** Five bodies — two planets, two brown dwarfs, one moon — and no belt
object; `phase4/alpha_centauri.yaml` discusses belts at length and declares **no `- body:` entry** for
one. ⚠ **An occurrence count stood here and is removed**: three seats counted it three ways under three
definitions, and **no claim here rests on the number.** Belts are discussed and not instantiated; that
is the whole fact.

⚠ **`bodies/earth.yaml` already takes the second row** (`kind: planet`, `parent: Sun`). It is an anchor
rather than a roster body, and at 100 % rock the table puts it well past melting, which is the
direction the Earth actually went — a weak check, and the only one this row has.

**Belts come last — owner, 2026-09-07**: *"벨트는 진짜 맨 마지막에 해도 괜찮을 것 같아."* ⚠ **Last in
order, not declined.** Two reasons, and both are about the pipeline rather than the belt: adding bodies
before the wiring holes close (C14 · C15 · C17) **adds one "cannot say" per body added**, and the two
gaps found the same day — C43 and C45 — **sit in the layer that handles body kinds**, so a new kind
multiplies them rather than adding to them. When the wiring is continuous, one belt object can be
declared and judged, which is the point of waiting. **A belt is the first body that would exercise
the second `t₀` row with something other than an anchor.**

⚠ **A limit of the calculation, not of any body class: there is no heat-loss term.** The
pulse is compared against an energy requirement as if every joule stayed in the body. A small object
loses heat faster than it accumulates it, so **for small bodies these numbers are an upper bound**, and
the smaller the body the looser the bound. **This is stated as a property of our calculation, not as an
explanation of anything published**: the 10–100 km range Monteux attributes to Yoshino is quoted
without a rationale, and searching Monteux's text produces no argument for the lower end. **We do not
know why that range starts at 10 km.**

**This is a Phase 4 fact, not an engine measurement**: it is a statement about how our system formed,
declared from the literature's ordering, and the engine reads it rather than deriving it.

**What this changes.** ⚠ **The refusal is not lifted; it is renamed.** It was *"we have no input"*. It is
now *"the input has narrowed to one: `t₀`"* — the formation time after CAIs, which no body declares and
which C21 was holding out for all along. No `t₀` is elected here, following C11: the grid is the
answer.

**Start condition.** Not now. Order still P3 → C14.

### C22 — ammonia fraction in the ice-giant mantle — **listed 2026-09-03; step 1 blocked pending a survey**

Owner's decision on P3's C5 question, verbatim (`4b8e06ba`, 09-03): *"1로 하되 조심히 접근하자."* — wire it
(option 1), carefully. The grounds are already written and are not re-surveyed here:
`ammonia-table-context-notes.md` §"Grounds for the next decision (not taken)" — **for**: the material is
grade *table* with its uncertainty carried; the mixing rule already exists in `Mixture`;
`SOLAR_ICE_MASS_FRACTIONS` is a published default ratio; the mantle's (P, T) is *inside* the table
(interpolation). **Against / wait**, which become the design constraints below: a water–ammonia mantle is not
the ternary the field models; the convention caveat touches the adiabat; the table's ceiling is below the
mantle base; wiring touches a path function.

**"Carefully" as code — two steps.**
- **Step 1 — wire it with default 0; the anchors do not move.** `ammonia_mass_fraction` becomes a declared
  argument of the ice-giant layer (the same shape as `mantle_rock_fraction`, C5: mixed in `integrate` at the
  deep-mantle water-material wrap, `_stack` untouched), default **0.0**, and at 0 the path must be
  **bit-identical** to today's — that is the step's acceptance test. The bytecode of `integrate`/`solve`
  changes, so the path fingerprint changes and `test_ice_giant.py --refresh` rides in the same commit; **the
  refreshed values must equal the old ones bit for bit** — if they do not, the 0 path is not the old path:
  stop and trace. An opt-in check shows the wiring works: at w_NH₃ = 0.1159 (0.08/(0.08+0.61), Bethkenhagen+
  2017 §V — the value §113 of the notes already used) the mantle density on §113's eight (P, T) points must
  move by the −2.9 to −3.5 % that table measured; that table is the prediction, this is the confirmation. A
  full solve at w > 0 is expected to **refuse by name at the table ceiling** (`Mixture.p_max` is the lowest
  component's, 333 GPa, against a mantle base of 820–1016 GPa) — the step-2 prerequisite made visible, not a
  defect.
- **Step 2 — raise the default to the solar ratio? Later, owner's decision.** Here the anchors move, and one
  thing has to be decided first (the deep-mantle fallback below).

**Three labels that ride on every value once w > 0** (the "against" items do not disappear):
1. **Methane asymmetry.** Solar ice composition has methane at **0.31** against ammonia's **0.08**; ammonia
   alone fixes the small term and leaves the large one as water — not the ternary the field models. Methane
   is *not built* by C4 (*"decomposes into long-chained molecules"*). Every emitted value says so.
2. **The table's ceiling is below the mantle base.** ≈ 290–333 GPa at mantle temperatures against a solved
   mantle base of 820–1016 GPa — **most of the mantle is outside the table.** Step 1's default 0 never hits
   it; step 2 cannot start without a stated deep-mantle rule (owner's decision, not made here).
3. **The convention caveat reaches the adiabat.** The internal energy in this edition **includes** the
   vibrational (nuclear-quantum) correction that the 2017 edition removed; §113 left ∇_ad as *"mechanism
   named, sign ungrounded"* for that reason. The density side (−2.9 to −3.5 %) is grounded; the thermal side
   is not. Do not blur them.

**Not done, by instruction**: `SOLAR_ICE_MASS_FRACTIONS` is not switched on as a default (step 2); no
deep-mantle fallback rule is chosen; methane is untouched; the water side's error is not quantified (§113 takes
water as the reference).

**⚠ Step 1 is blocked before it started — the owner put two questions ahead of the wiring** (`4b8e06ba`,
09-03): *"암모니아 고압에서 분해되는지 어케되는지 조사부터 해보자. 메탄 선례 따라가자. 그리고 맨틀보다 위, 저압
구역에 암모니아가 있을 수는 없나"*. The parallel seat is surveying; **the target layer itself may change**, so
wiring now could be wasted. Why each question bites:
- Methane was closed on Bethkenhagen+ 2017 §III, *"Pure methane does not become superionic but instead
  decomposes into long-chained molecules"*. **If a corresponding sentence exists for ammonia, C22's scope is
  cut** — that is exactly the precedent the owner named.
- The low-pressure question meets our own notes: `ammonia-table-context-notes.md` calls the worst interpolation
  corner *"the low-density dissociation corner"* (ρ 0.5 · 3000 K · 17.3 %), the 5 % flags sit in the same
  corner, and *"3000 K is where the paper reports its first-order transition … the table does not mark it and
  the interpolation crosses it"*. Coverage is actually better at low pressure — the table starts at
  **0.309 GPa** while the mantle base is far outside it — and the envelope's ice is one constant
  (`ENVELOPE_WATER`, `interior.py@«parts.append((ENVELOPE_WATER, z_ice))»`), so an envelope wiring would be a single change point.
- ⚠ **Do not read "low density = low pressure = envelope."** 3000 K is not an envelope temperature; which
  layer, if any, the survey answers.

**Unblocked the same evening — the survey came back and the precedent does not transfer.** Three sentences,
each reproduced by the work seat from the cache (`ammonia-wiring-context-notes.md` §1 has them in full):
Bethkenhagen+ 2017, the paragraph before the methane sentence — *"pure ammonia becomes superionic as well but
only below 4000 K"* (⚠ the PDF text layer splits *"superi onic"*; grep the `.md`); decomposition is
elementisation to **N₂ + H₂**, not methane's polymerisation. And in our bodies it is **fluid**: 2013 §III A,
*"Neither of the isentropes crosses the superionic phase … ammonia is very likely to only occur as a fluid under
conditions present in the interior of Uranus and Neptune"* — molecular or dissociated unsaid, with 2017's
Fig. 6 marking *"partial dissociation of ammonia into N₂ and H₂"* in the figure only. **The low-pressure
branch is closed**: the "dissociation corner" is 1.906 GPa at **3000 K** (a hot dilute fluid, not an envelope);
the table's floor is 500 K; 2017 puts the ice-rich layer *below* P₁₋₂ = 10–15 GPa. **Target layer: the mantle;
`ENVELOPE_WATER` untouched.** One constraint added to step 1: the interpolation crosses unmarked first-order
transitions on three isotherms (2013 §IV A: 3000 K at 1.8–2.0 g/cm³, 1000/2000 K at 1.3–1.5, 500 K at 1.0–1.3);
the pressures we attach (59.40 / 76.45 GPa at 3000 K, from Table I) are **ours** — the paper prints none.
Not held, identifiers not yet read from ADS: **Meyer+ 2015** (chain-like aggregates in mixtures — 2017:
*"Similar molecular aggregates can occur also in mixtures with water and ammonia"*) and **Hirai+ 2009** (methane
phase diagram) — on the not-held list, not needed for C22, which uses the pure-ammonia material.

**Start condition — met.** Step 1 pre-registered in `ammonia-wiring-context-notes.md` §1–§3 (committed before
code), then wired.

**Step 1 landed 2026-09-03** (`ammonia-wiring-context-notes.md` §4). `ammonia_mass_fraction` (default 0) is
threaded `solve → shoot → _shoot_pressure → integrate`, mixed at the deep-mantle water wrap
(`with_rock(with_ices(mat))`), `_stack` untouched. **① fired exactly**: `--refresh` changed only the path
fingerprint; every frozen value of both anchors is byte-identical. **③ fired exactly**: the wrap's mixture
reproduces §113's eight ratios to four decimals (0.9654–0.9705). **④ fired in an unregistered kind**: the
opt-in Uranus solve at w = 0.1159 refused **not at the 333 GPa ceiling but on the trial corridor's cold flank**
— 152 GPa · 545 K on the temperature loop's first cold guess, 0 s, four fires, four refusals — because
`Ammonia.density`'s `PhaseGap` carries no `too_cold`, so Brief 22's bracket steering does not engage and the
shoot reads the refusal as geometry. **Step 2 therefore has two prerequisites**: the deep-mantle rule (owner)
**and** a cold-flank label on the ammonia refusals (the cold-flank family's newest member; not fixed here —
measurement, not repair). The P3 gate row's static half now asserts the wrap exists with default 0.

**Step 2-② landed 2026-09-03** (owner: *"일단 2부터 보자."*; `ammonia-wiring-context-notes.md` §5–§6).
`Ammonia.density` decides `too_cold` from `p_bounds(T)` — above the ceiling → hotter, below the floor →
colder — resting on the table's floor and ceiling both rising with T, which is now a gate row in
`test_ammonia.py` (a fact of this table, not a guarantee). Anchors untouched (not a path function). **What ④
then showed, reproduced twice**: the cold trials now steer up and pass the state that killed step 1; the
corridor meets the registered ceiling deep (1 035 GPa · 3 935 K, "hotter"); and the hotter adiabat puts the
mantle top at **4.10 GPa · 4 749 K, 0.023 GPa below the table's low-density floor** ("colder") — the loop
concludes by name between two walls pulling opposite ways. **So the deep-mantle rule is not one rule**: step 2
needs a rule above the ceiling *and* one below the floor at a hot mantle top (or an entry condition on the
wrap), and neither is declared here. That is the shape of the owner's decision — **two decisions**, numbered:
① above the ceiling (deep mantle; fired at 1 035 GPa · 3 935 K) · ② below the floor (mantle top; fired at
4.10 GPa · 4 749 K — **by 0.024 GPa, 0.6 %**, a hair, not a gross violation; the floor climbs 0.309 GPa at
500 K → 4.45 GPa at 5 000 K). *"Far outside"* and *"0.6 % outside"* are different decisions.

**The extrapolation axis above the table is closed on the literature (same evening; notes §7).** Searched
and found wanting: no published ammonia fit joins a high-pressure asymptote (ADS: 3 hits, all unrelated — the
silicate/iron TFD construction has no ammonia candidate); the one paper in range, Li+ 2013
(`2013JChPh.139m4505L`, owner-obtained preprint + source), is a Hugoniot whose single table sits at
19 000–113 000 K over 221–1 274 GPa against a mantle at 2 550–6 070 K — it does not pass near our region;
and four reported transitions in 90–350 GPa (ionic crystal, ammonium amide, liquid → plasma; three papers not
held) plus *"no experiment above 350 GPa"* (Ravasio+ 2021) mean an extension would assert physics the 2013
table does not contain. The refusal above ≈ 333 GPa is therefore **"looked, and cannot be used — for these
reasons"**, not merely "refused by name". The extended 2017 data set (to 1 000 GPa, four more isotherms)
exists, is undistributed, and has the nuclear-quantum correction *removed* where our table *includes* it —
not appendable; an author request is the only route and is **recorded as possible, not opened** (the owner
closed that class on 09-03). **State tonight**: step 1 landed · step 2-② landed · step 2-① waits on the
owner (two decisions) · default 0.

### C23 — does a sub-Neptune's iron core run a dynamo at all? (existence, not strength) — **existence judged 2026-09-06; the field strength is not available and this item cannot produce it**

**Built 2026-09-06.** `sub_neptune_dynamo.dynamo_verdict` reads the two gates in Tang's order. Gate 1
is `eos.silicate_solidus`: while the mantle surface is molten the dynamo runs and `k_c` is never
consulted, which the test enforces by requiring both candidates to return the same answer on that
branch. Gate 2 is `k_c`, and with nobody having chosen the verdict stops at `choice required` rather
than the engine picking. Off the solidus curve the answer is `undetermined`, kept distinct from
`solid` so that a consumer cannot read an absent verdict as a verdict.

The three-way refusal loop is broken where it was actually closed: `core_state`'s sub-Neptune refusal
said no branch received that core, and one does now, so it names it — while still declining, because
the first gate is silicate melting rather than the iron melting curve. `CORELESS_CLASSES` became
`NOT_THIS_NODES_QUESTION`, since the old name said the class had no core while the reason beneath it
said the iron core sits under the envelope.

⚠ **What this does not give.** No field strength, no moment, no aurora. Tang prints none, and the
existence gate cannot be turned into one.

Opened by C18's closure. Tang+ 2025 (`2025ApJ...989...28T`, cached) publishes the **on/off criterion** and every
input of it is held or declarable:

    Rm  = μ₀ σ U D  > 50                      (eq. 46)      threshold — Tang 50; our ladder quotes 40 (Gaidos/RM22, OC06's onset) → **40–50 is the width**, both "studies have shown"-class citations
    U   from Christensen 2010's scaling       (eq. 47)      Christensen 2010 (SSRv 152, 565) not held — Tier 2
    F_conv = F_CMB − F_cond                    (eq. 48)      F_CMB ← our `cmb_heat_flux` (Brief 60); F_cond along the adiabat
    k_c   declared — Tang tests 40 (Konôpková+ 2016) and 100 (Pozzo+ 2012) W/m/K; RM22 quotes the same Pozzo 100 → the two papers confirm each other's reading
    R_c, D ← our `interior_layers`;  Ω — Tang assumes 1 day and writes that the exact value does not matter much;  H_T = c_P/(α g)

**Why not built tonight**: it is a new C item that changes the refusal structure of `dynamo_rocky` and
`core_state` (which today send a sub-Neptune round the C18 loop), so it is **listed like C20/C21 and left to
the owner**. **Cost when built, small**: Tang extends Nimmo+ 2004 rather than replacing it — Nimmo is used
three times (mantle / magma-ocean energy balance; the local-Rayleigh boundary-layer scaling for δ; Table 1's
source (7)) — and *"the envelope limits cooling"* is not a new equation but a **top boundary condition**: the
H/He blanket *"sets the mantle surface temperature above 1000 K"*, shrinking ΔT_CMB. Our `cmb_heat_flux`
structure carries over; what changes is that boundary condition and one δ branch for a molten mantle.
**⚠ The question above was asked of the wrong body.** Read against Tang's own text on 2026-09-05
(`pdftotext` of the cached PDF; every quotation below is verbatim), **Rm is not the gate**. The paper
says *"as long as a convective layer is present in the liquid iron, Rm can readily exceed the
critical value. Our numerical results show that **Rm typically ranges from 10³ − 10⁵, well surpassing
the critical threshold**"*. Against a threshold of 40 or 50 that is a margin of 20× to 2500×, so the
three worries this entry was built on — RM22's 2.26× σ contradiction, the 40-vs-50 threshold width,
Christensen's velocity scaling — **all die inside it**. They were real discrepancies about a quantity
that turns out not to decide anything.

What decides it is the **mantle**, and the paper says so in its own abstract: *"dynamo action in
sub-Neptune iron cores persists **as long as the mantle surface remains molten**, often exceeding
10 Gyr, and becomes sensitive to core thermal conductivity after solidification."* Figure 19 repeats
it: *"a dynamo exists in the iron core as long as the mantle surface remains in the liquid phase.
Once the mantle surface solidifies … the cooling rate of the iron core sharply declines … dynamo
operation starts to become sensitive to the conductivity choice."*

So the gates are ordered, and neither of them is Rm:

1. **Is the mantle surface still molten?** While it is, the dynamo is on and nothing else is consulted.
2. **Only after it solidifies**, `k_c`: 40 or 100 W/m/K.

**This moves where C23 starts.** Not `core_state`, which asks whether the metal core is liquid — the
silicate melting judgement (`eos.silicate_solidus`) is what answers gate 1. *"Does the iron core run a
dynamo"* turned out to be a question about the mantle. The pre-registration below is kept as written,
because what it got wrong is the useful part of the record.

**⚠ And `k_c` is the A-grade band this looked for and did not find.** Tang prints **both** ends and
attributes each: *"a value of 4 × 10⁶ erg s⁻¹ cm⁻¹ K⁻¹ (Konôpková et al. 2016, solid) and a high value
of 1 × 10⁷ erg s⁻¹ cm⁻¹ K⁻¹ (Pozzo et al. 2012, dashed)"* — that is **40 and 100 W m⁻¹ K⁻¹**. Both
printed, both attributed, and the pick flips a dynamo on or off on a low-mass thin-envelope
sub-Neptune, which in art terms is aurora or no aurora. ⚠ It is also the first `Choice` whose
consequence is **conditional**: before the mantle surface solidifies the choice changes nothing at
all, and C32's structure has no way yet to say "this decision is empty on that branch".

**Pre-registration as written on 2026-09-04, kept for the record.** ⚠ **σ for the Rm criterion is
self-contradictory inside RM22** (phase table, 2026-09-04): the printed 1.36e6 S/m and the printed λ_m 1.32 m²/s (⇒ 6.03e5) differ by 2.26×, and Rm = μ₀σUD carries that factor whole against the threshold of 50. Pre-registered for the start of C23: compute Rm with both values and report first whether the on/off verdict flips; Tang's ~1e6 fixes only the order. **Tang does not unlock Driscoll & Olson 2011** (`Driscoll`, `Olson` 0 hits) — RM22's `q_conv` definition and
`γ_d = 0.2` still sit behind Driscoll & Olson 2011 ([`2011Icar..213...12D`](https://ui.adsabs.harvard.edu/abs/2011Icar..213...12D)) — ⚠ **held since 2026-09-04 09:17**, so C16's next step is to read it rather than to request it; the standing request is stale (corrected 2026-09-06).

### C24 — a water-rich rocky body does not converge in `interior_layers` — **listed 2026-09-04; opened by the owner the same afternoon — diagnosed and fixed: `water-world-convergence-context-notes.md`**

*Record note 2026-09-04: the heading's "fixed" was written in 1eea9957 (15:02) before the fix landed in 6113c804 (15:27); the state was true 25 min later. Kept as written; noted for the audit's ledger.*

**Blocks**: C17 (its structural half cannot be measured until this converges).
**Symptom** (`ocean-fraction-context-notes.md` §3): 1 M⊕ · CMF 0.325 · T_pot 1 600 K · no atmosphere,
`ice_mass_fraction` 0.1 and 0.3 → the temperature loop misses the surface condition (`converged=False`,
48–52 s per solve). **The positive control holds**: the layer stack itself is built (radius 1.151 / 1.293 R⊕,
P_cmb 131.8 / 116.2 GPa, centre 353.8 / 333.1 GPa), so this is a failure of the *temperature* closure, not
of placement. Directing seat's hypothesis, **unchecked**: the silicate mantle top may start at the water
layer's *bottom* temperature rather than the declared potential temperature, which would explain a hotter CMB
at lower pressure — to be measured when C24 is opened, not assumed.
**Roster check**: none of the seven Phase 4 boards (40 Eri, α Cen, Barnard, Fomalhaut, Luhman 16, Proxima,
Tau Cet) declares a water-rich rocky body — Pandora is Earth-density with a surface ocean, which is not the
interior water fraction. The roster's only water-rich rocky candidates are **TRAPPIST-1 f/g/h** (Phase 3
triage only, no board yet). **Priority: low until a TRAPPIST-1 board exists, high the day it does.**
Start is the owner's decision.
**Diagnosed 2026-09-04 (compute-only, pre-registered)**: not the temperature update, not the pressure bracket — every centre temperature below ≈ 4 100 K is refused by the water column, and the answer (≈ 2 900 K) lies inside that refused window (**(b)**): near-surface water at ~0.09 GPa · 560–870 K, below the dense-liquid table's 0.1 GPa floor and under Mazevet's 1 000 K. **A held table covers exactly that window (IAPWS-IF97, `_Steam`/`h2o_if97`) and the water column's dispatch never consulted it** — Brief 25 closed the same wall for envelope water only; a coverage gap between three IAPWS-lineage tables (seams ≤ 0.04 %), not a data problem. Fix: one candidate line, placed last in `liquid_material` so anchors stay bit-identical by construction. Under an envelope the window stays closed: opening it makes Neptune's solution disappear at ice_x's ceiling (measured 2026-09-04; C26) — closed is not "right", it is "not yet evaluable". Beside it: 1 600 K is the rock's potential temperature, not a water world's (independent, not causal); the dispute band is a two-sided strip on a one-way flag (③, off the critical path).

### Owner list — main-repository findings of 2026-09-04 (outside this worktree; not tonight's work)

| # | finding | where | evidence | what it is not |
|---|---|---|---|---|
| O1 | Luhman 16 A/B age: DB 1.5 ± 1.5 Gyr ("unverified" — the midpoint of a 0.1–3 Gyr range put in the value slot) and board 0.5 Gyr (phase4/luhman_16.yaml@«- { name: age, value: 0.5, unit: Gyr, op: passthrough, note: "Phase 3 resolved: Oceanus ») (Gagné 2023 moving group). **Not a contradiction but a precision difference**: 0.5 lies inside the DB's range; Burrows supports the narrow one (directing seat's correction of its own first wording) | `db/systems/luhman_16_{a,b}.json` vs `phase4/luhman_16.yaml@«- { name: age, value: 0.5, unit: Gyr, op: passthrough, note: "Phase 3 resolved: Oceanus moving group (Gagné 2023), corroborated by 12C/13C = 74 (de Regt 2026); supersedes the Faherty 2014 field guess 1.5", note_ko: "Phase 3 해결값. 오케아누스 이동군(Gagné 2023), ¹²C/¹³C = 74 교차지지(de Regt 2026). Faherty 2014 필드 추정 1.5를 대체" }»,640` | Burrows+ 2001 eq. 4 with the DB's own g → 0.54 / 0.44 Gyr; eq. 1 closes the DB luminosity within 20–30 % at 0.5 Gyr, 3–4× off at 1.5 | not a worktree edit — `db/systems` is build output; fix in the source layer |
| O2 | Luhman 16 A and B carry the same radius 62 613 km in the `principia` block, source unrecorded | same files, `principia.mean_radius_km` | eqs 3–4 are sensitive to it through g | not a value judgement — a provenance check |
| O3 | Three cache names are arXiv abstract pages, not papers: `1004.1091`, `1209.5323`, `1401.8145` (50-byte .md, .html without `ltx_document`) | `docs/phase3/_papers/` | `check_paper_held.py` now says ABSTRACT-ONLY for them | not an engine citation — none of the engine axis cites them |
| O4 | Two methodology docs label those shells "cached": Crossfield 2014 (`spin-axis-inclination-methodology.md@«- **Crossfield et al. 2014**, Nature 505, 654 ([`2014Natur.505..654C`](https://ui.adsabs.harvard.edu/abs/2014Natur.505..654C), arXiv [1401.8145](https://arxiv.org/abs/1401.8145), **cached**).»`, claims v sin i for both components — not in the abstract) and Heller & Barnes 2013 (`ice-stability-methodology.md@«- **Heller & Barnes 2013** ([arXiv:1209.5323](https://arxiv.org/abs/1209.5323), cached).»`, claims the satellite energy budget — the abstract only names four terms). **The values are safe**: the board's spin-axis row (`phase4/luhman_16.yaml@«구간 안에 머문다. refs: ["docs/reference/spin-axis-inclination-methodology.md", "2021ApJ...906...64A"]»`) cites only Apai+ 2021, held in full. The defect is the label — *false provenance* — en and ko alike | those two docs + ko mirrors | `check_paper_held.py --scan` | not a number error; do not inflate |
| O5 | C19's brown-dwarf branch: two routes to L(M, age) — a grounded track (Burrows eq. 1 with declared κ_R, or Baraffe+ 2003) or the DB's measured luminosity (Faherty+ 2014) — written side by side, hanging on O1 | `giant-dynamo-age-context-notes.md` §4 | — | not decided |

⚠ *(2026-09-04, evening)* **What closed is the diagnosed mechanism** — the coverage gap of near-surface water — **not the
whole symptom in this title.** Water fractions 0.05 · 0.15 · 0.20 on the same body still do not converge, and with a different
signature (no `PhaseGap` refusal loop — 0 raised in 120 / 279 / 355 structures; the surface condition is missed by −0.77 / +0.86 / −1.45 % at 0.05 / 0.15 / 0.20, corrected 2026-09-04 evening from a single "0.75 %") — **C27**. Read C24 as narrow.

### C25 — the measured CMB temperature and the published CMB heat-flow range cannot both be met in this model — **listed 2026-09-04, not started**

Re-stated the same hour it was listed (the first form, "eqs 37–39 as the source of the low Q_C", was wrong: the
law reproduces Nimmo's printed 9.0 TW / 140 km at his own inputs to 1 %, and in the module T_c is the input, Q_C
the output — low T_c gives low Q_C, 2.75 → 7.69 TW over 3 760 → 4 155 K, not the reverse). The tension: at the
measured CMB temperature 3 760 K the model has an Earth-like inner core (566–572 km) but Q_C 2.75 TW, below
Nimmo's printed 4.5–9.0; at 4 155 K Q_C is inside the range but the inner core is gone. Scope: the closure that
picks T_c (C14's energy balance / C20's history), the mantle-base adiabat ratio (our 1.579 vs his 1.69 is 15 % of
Q_C at his inputs), and the depression factor's hypersensitivity (C20 §5). Excluded: the boundary-layer law's
constants, the melting-curve source, the mantle conventions. **Listed only; start is the owner's decision.**

### C25 (b) 2026-09-09 — the option table's shape, committed before the numbers are computed

⚠ **This subsection is the table's columns and nothing else. It is committed before any of the cells is
computed**, so that the shape cannot be chosen to suit a result. **It is not a verdict table**: it is the
last column of an owner choice, and C25's own entry already says *"start is the owner's decision"*.

**Why the table exists.** C15's entropy band straddles zero — `ΔE` −69 MW/K with a band −264…+238 and
1 of 4 corners positive once C20's computed cooling rate collapses the third axis. Reading the chain
(brief 164) put the cause one step upstream of `k`: **C14's closure solves `T_c` = 3 978 K, at which the
core is entirely liquid, so `e_l` and `e_g` — the budget's two largest positive terms — are exactly
zero** (`engine/core_entropy.py@«e_l = e_g = e_h = 0.0»`). Whether they are zero is decided by which horn
of C25 is taken, and that is a declaration, not a measurement.

**Rows — the two horns, each at three potassium caps.** ⚠ The `H` axis is a *cap*, not a measurement:
the literature runs in one direction (Nimmo's model needs 400 ppm K; later work puts the upper bound
lower), so the three rows bracket that rather than centring on it.

| row | `T_c` present | `H` cap | what it declares |
|---|---|---|---|
| 1 | **3 760 K** — the measured CMB temperature | 1.5 pW/kg (400 ppm K, Nimmo Table 4) | the measurement wins; `Q_C` may fall below the published range |
| 2 | 3 760 K | 0.9 (250 ppm) | ditto, with the mid cap |
| 3 | 3 760 K | 0.14 (40 ppm) | ditto, with the newest cap |
| 4 | **4 155 K** — the temperature at which `Q_C` enters Nimmo's printed 4.5–9.0 TW | 1.5 | the published flux range wins; the inner core is gone |
| 5 | 4 155 K | 0.9 | ditto |
| 6 | 4 155 K | 0.14 | ditto |
| ref | **3 978 K** — C14's own root, what the engine has today | 1.5 · 0.9 · 0.14 | the baseline the other rows are read against |

**Columns.**

| column | what it is |
|---|---|
| inner-core radius | `core_energy.inner_core`'s `r_i`, or **none** |
| `Q_C` | `core_terms`' `q_total` [TW] — the quantity C25's tension is about |
| **`ΔE` at `k` = 30 · 70** | the verdict corners as `cmb_flux.K_CORE_RANGE` declares them (50 ± 20, Nimmo Table 1) |
| record: `ΔE` at `k` = 20 · 40 · 100 | the literature's camps — Hsieh+ 2020 ([`2020NatCo..11.3332H`](https://ui.adsabs.harvard.edu/abs/2020NatCo..11.3332H)) ≈20, Konôpková+ 2016 ([`2016Natur.534...99K`](https://ui.adsabs.harvard.edu/abs/2016Natur.534...99K)) 40, Pozzo+ 2012 ([`2012Natur.485..355P`](https://ui.adsabs.harvard.edu/abs/2012Natur.485..355P)) 100 — ⚠ **record only**, since electing one is owner decision ② |

**Fixed before the run, so nothing in the table is chosen afterwards.**

- **`dT_c/dt` = −33 K/Gyr**, Nimmo Table 4's nominal (`core_energy.DTC_DT`). ⚠ `Q_s`, `Q_L` and `Q_g` are
  linear in it and `Q_R` is not, so the choice matters and is stated: C20's own trajectory computes
  **36 K/Gyr** at its own `T_c`, and one row of the table is repeated at that rate to show the size of
  the difference.
- **The entropy is the present-epoch `ΔE`**, computed at a declared `T_c` — **not** C20's window minimum
  `ΔE_min`. ⚠ They are comparable but not the same quantity, and the reason they are readable side by
  side is measured: in the four corners C20 reported, the window minimum **sits at the present**
  (`min … (t +0.00 Gyr)` in all four).
- **No cell in this table is a pass or a fail.** The threshold is owner decision ③ below.

**The three owner decisions this table serves, with candidates and no selection.**

| # | decision | candidates |
|---|---|---|
| ① | **which horn of C25** | measured `T_c` 3 760 K (inner core present, `Q_C` below the published range) · `T_c` 4 155 K (`Q_C` inside it, no inner core) · keep C14's root 3 978 K and accept that `e_l` = `e_g` = 0 |
| ② | **how `k_core` is carried** | Nimmo's 50 ± 20 band as now · elect Konôpková+ 2016's 40 · elect Pozzo+ 2012's 100 · unify with the sub-Neptune path, which already declares 40 and 100 (C49) |
| ③ | **whether `ΔE` > 0 is our threshold** | the paper's own `ΔE` > 0, which it calls a threshold-avoidance · the printed required excess **0.1–1 000 MW/K**, whose upper end no corner reaches |

### C25 (c) 2026-09-09 — the option table, computed; and the pre-registered `Q_C` column had to become three

⚠ **First, a correction to C25 (b)'s own column list, made visible rather than quietly fixed.** That
subsection defined one column — *"`Q_C` | `core_terms`' `q_total` [TW] — **the quantity C25's tension is
about**"*. **It is not.** Running it against C25's recorded sentence (*"2.75 → 7.69 TW over
3 760 → 4 155 K"*) reproduced neither the values nor the direction, and the reason is that this engine has
**three different CMB heat flows**, all legitimately called `Q_C` somewhere:

| | what it is | direction in `T_c` |
|---|---|---|
| **① mantle-side `Q_CMB`** | `cmb_flux.bottom_layer`, Nimmo eqs 37–39 — the flow the mantle's basal boundary layer can carry | **rises** with `T_c` (the jump across the CMB grows) |
| **② core-side adiabat `Q_ad`** | `cmb_flux.adiabatic_flow` — `4π r² k \|dT/dr\|_ad`, the flow conduction alone carries, **∝ k** | rises slowly |
| **③ core-side supply `q_total`** | `core_energy.core_terms` — `Q_s + Q_L + Q_g + Q_R` at a declared cooling rate; **what the entropy budget uses** | **falls** across the inner core's disappearance |

**C25's tension is about ①**, the published 4.5–9.0 TW range is ①'s, and the entropy corners are ③'s.
⚠ **This is what pinning the columns first bought:** the wrong column was **findable** because it had
been written down before the numbers existed, and it was found by the first cell that disagreed with a
sentence already in the document. Had the table been built and labelled in one pass, ① and ③ would have
been one column called `Q_C` and nothing would have contradicted anything.
⚠ **One column could not have carried both**, and the pre-registration said it did. **The rows and the
`k` axis stand as registered; the flow column is split, and the split is recorded here rather than
edited into (b).**

**① reproduces C25's sentence exactly**, which is how the mislabel was caught:

| `T_c` | ① mantle-side `Q_CMB` | ② core-side adiabat `Q_ad` (k 30 · 50 · 70) | ③ core-side supply |
|---|---|---|---|
| **3 760 K** (measured) | **2.750 TW** — below the published 4.5–9.0 | 4.07 · 6.79 · 9.50 | 6.465 |
| **3 978 K** (C14's root) | **4.913** | 4.31 · 7.18 · 10.05 | **4.912** |
| **4 155 K** | **7.693** — inside the range | 4.50 · 7.50 · 10.50 | 4.912 |

⚠ **At 3 978 K, ① = 4.913 and ③ = 4.912 — that equality *is* C14's closure**, which is why the root
lands there and not somewhere else. Reading the two flows side by side makes the closure visible as an
identity rather than as a number someone chose.

⚠ **And the same `k` decides whether the core convects at all.** At C14's closure the CMB carries
**4.91 TW** against an adiabat of **7.18 TW at k = 50** — *sub-adiabatic*, no thermal convection — while
at **k = 30** the adiabat is **4.31 TW** and the same closure is *super-adiabatic*. **So `k` is not only
the entropy band's dominant axis; it decides the prior question.** Owner decision ② therefore carries
more than the band's width.

#### The option table, filled

**Fixed as registered: `dT_c/dt` = −33 K/Gyr, present-epoch `ΔE` [MW/K], `k` 30 and 70 as the verdict
corners, `k` 20 · 40 · 100 as record.** No cell is a pass or a fail.

| `T_c` | `H` | inner core | ① `Q_CMB` | ③ supply | **`ΔE` k 30** | **`ΔE` k 70** | k 20 | k 40 | k 100 |
|---|---|---|---|---|---|---|---|---|---|
| **3 760 K** | 1.5 pW/kg | **572.2 km** | 2.750 | 6.465 | **+221.5** | **+28.1** | +269.9 | +173.2 | −117.0 |
| 3 760 | 0.9 | 572.2 km | 2.750 | 5.300 | **+179.8** | −13.7 | +228.1 | +131.4 | −158.7 |
| 3 760 | 0.14 | 572.2 km | 2.750 | 3.825 | **+126.9** | −66.6 | +175.2 | +78.5 | −211.6 |
| **4 155 K** | 1.5 | **none** | 7.693 | 4.912 | **+20.6** | −172.8 | +69.0 | −27.8 | −317.9 |
| 4 155 | 0.9 | none | 7.693 | 3.747 | −17.2 | −210.6 | +31.2 | −65.6 | −355.7 |
| 4 155 | 0.14 | none | 7.693 | 2.272 | −65.1 | −258.5 | −16.7 | −113.4 | −403.6 |
| *ref* 3 978 | 1.5 | none | 4.913 | 4.912 | +28.0 | −165.5 | +76.3 | −20.4 | −310.5 |
| *ref* 3 978 | 0.9 | none | 4.913 | 3.747 | −11.5 | −204.9 | +36.9 | −59.9 | −350.0 |
| *ref* 3 978 | 0.14 | none | 4.913 | 2.272 | −61.5 | −254.9 | −13.1 | −109.9 | −400.0 |

**What the table shows, stated as measurement and not as choice.**

- **The inner core is the whole difference.** At 3 760 K it is **572.2 km** and the two largest positive
  entropy terms exist; at 3 978 and 4 155 K it is gone and they are zero. **Every `ΔE` in the 3 760 rows
  is positive at `k` = 30 — including at the newest 40 ppm potassium cap** — and at 4 155 K only the
  richest potassium cap is positive there.
- **`k` = 100 makes every row negative.** The high-conductivity camp closes the budget on its own,
  regardless of the horn or the potassium.
- **`k` = 70, our own upper corner, is negative in eight of nine rows** — positive only in the wettest
  cell (3 760 K with 400 ppm K, +28.1).
- ⚠ **The cooling-rate choice is small on the horns without an inner core and 3.6× larger on the one
  with it, and the first draft of this line missed that.** Repeating every cell at C20's computed
  36 K/Gyr moves `ΔE` by **+6.5 MW/K at 4 155 K** and **+6.8 at 3 978 K** — but by **+23.8 at 3 760 K**,
  because `Q_L` and `Q_g` are linear in the rate too and they exist only there. *(The parenthetical in
  the draft, 3 760/1.5: +221.5 → +245.4, already showed the +23.9 and the sentence generalised the wrong
  number; corrected on the audit's sweep of all 45 cells.)*
- ⚠ **And it does decide one sign: exactly one cell of 45 flips, `3 760 · H 0.9 · k 70`, from −13.7 to
  +10.2 MW/K** — and that is a **verdict corner**, not a record column. **44 of 45 cells keep their
  sign; the cooling rate is the deciding variable in that one.**
- ⚠ **So owner decision ① and the cooling rate are not independent.** The flipping cell sits on the
  **inner-core horn**: choose 3 760 K and the cooling rate becomes a new decision axis for that cell;
  choose 4 155 or 3 978 K and it is harmless. This is the shape `engine/bands.py`'s `Choice` calls an
  `only_when` dependence, and it is recorded here rather than left for whoever reads the table next.

**The parallel seat's H-ladder prediction is reproduced, and that is all it is.** P4 predicted the
descent +32 → ≈ −7 → ≈ −57 across the three potassium caps at `k` = 30; the reference row at C20's own
rate gives **+34.7 → −4.7 → −54.7**. The ~2–3 MW/K offset is C20's present `T_c` (4 027 K) against
C14's root (3 978 K), not a disagreement. ⚠ **So the ladder is a reproduction, not a new finding.**

**Each horn's cost, in one line each, and nothing is chosen.**

- **3 760 K** — the measurement wins: an Earth-like inner core, every `k` = 30 cell positive, and
  ⚠ **`Q_CMB` = 2.750 TW, below Nimmo's printed 4.5–9.0**, so the published flux range is contradicted.
- **4 155 K** — the published range wins: `Q_CMB` = 7.693 TW inside it, and ⚠ **no inner core**, so
  `e_l` = `e_g` = 0 and the band is negative everywhere except one cell.
- **3 978 K** — C14's own closure, where ① and ③ balance; ⚠ it inherits the second horn's cost (no inner
  core) without gaining the first's flux agreement.

⚠ **Nothing in the engine changed, and no value moved.** The table is a measurement of what the existing
code says at three declared temperatures. **The choice is owner decision ①, and it is not made here.**

### C25 (d) 2026-09-09 — what the literature prints behind the band's two axes, and the three decisions in one place

**Read by the parallel seat (P4), transcribed here with labels and grades, and no value selected.** The
report is at `/Users/vana/Desktop/NearStars-artifacts/2026-09-09-c20-entropy-band/P4-core-entropy-band-inputs.md`;
**held 6 · abstract only 14** for this task.

#### `k_core` — the printed span is **18–226**, and it has been two camps since 2012

| camp | printed | grade |
|---|---|---|
| **high** | Pozzo+ 2012 ([`2012Natur.485..355P`](https://ui.adsabs.harvard.edu/abs/2012Natur.485..355P)) Table 1 — `k_CMB` **100** for core mixtures (pure Fe 144/140), `k_ICB` **150**; text *"DAC … 90–130 at the top of the outer core"* | **held** |
| high | Zhang+ 2022 ([`2022PNAS..11919001Z`](https://ui.adsabs.harvard.edu/abs/2022PNAS..11919001Z)) Results — hcp Fe-9Si *"**∼100 to 110** W m⁻¹ K⁻¹ at ∼140 GPa and 4 000 K … unexpectedly close to that of pure hcp Fe (**100 ± 10**) (Ohta+ 2016 ([`2016Natur.534...95O`](https://ui.adsabs.harvard.edu/abs/2016Natur.534...95O)))"*; Fe-(4.3–9.0)Si ∼78 at 120–140 GPa, 2 500 K | **held** (Europe PMC mirror) |
| high | de Koker+ 2012 ([`2012PNAS..109.4070D`](https://ui.adsabs.harvard.edu/abs/2012PNAS..109.4070D)) — ⚠ **no single `k_CMB` in the text**; conductive flux at the top of the core *"**14–20 TW**"*, and Fig. 3 read by eye (±5): liquid Fe ≈130–140, Fe₇Si ≈115–125, Fe₃Si ≈95–105 W/m·K — **figure-read, barred from any board row** | **held** (Europe PMC mirror) |
| high | Gomi+ 2013 ([`2013PEPI..224...88G`](https://ui.adsabs.harvard.edu/abs/2013PEPI..224...88G)) abstract — outermost core *"greater than **90**"* | abstract only |
| **low** | Hsieh+ 2020 ([`2020NatCo..11.3332H`](https://ui.adsabs.harvard.edu/abs/2020NatCo..11.3332H)) — Fe-15Si *"about **20**"* at ∼132 GPa, Fe-4Si ≈40 saturated, pure Fe ≈120–130 near CMB pressure | **held** |
| low | Konôpková+ 2016 ([`2016Natur.534...99K`](https://ui.adsabs.harvard.edu/abs/2016Natur.534...99K)) abstract — *"**18–44** watts per metre per kelvin"*, solid Fe, direct measurement | abstract only |
| re-cited | Ohta+ 2016 prints no number in its abstract; Hsieh+ 2020 re-cites it as **≈226** | abstract only |

⚠ **The sharpest form of the split is inside one alloy family**: for comparable silicon, Hsieh+ 2020
reads **≈20** and Zhang+ 2022 reads **∼100–110**. **Our 30–70 is a low-to-middle subset of 18–226, and
nothing in this literature narrows it** — which is why C49 exists and why owner decision ② is a choice
between camps rather than a measurement.

⚠ **The rows above are mostly solid iron, and the outer core is liquid.** The parallel seat's P8 read the
two camps' own **liquid-alloy** numbers at CMB conditions, and they are not the numbers in the abstracts:

| camp | liquid alloy at the CMB | pure Fe, same study |
|---|---|---|
| low — Konôpková+ 2016 | **25 ± 7** | 33 ± 7 |
| high — Ohta+ 2016, liquid Fe₆₇.₅Ni₁₀Si₂₂.₅ | **88 (+29 / −13)** | 226 (+71 / −31) |
| synthesis — Davies+ 2015 ([`2015NatGe...8..678D`](https://ui.adsabs.harvard.edu/abs/2015NatGe...8..678D)) | CMB **80–110** | — |

**So Konôpková's printed "18–44" is the solid-iron band**, and its liquid value is lower still. ⚠ **Our
50 ± 20 sits between 25 and 88 and is neither camp's number** — it is not a compromise anyone published,
which is a stronger statement of C49's problem than "a low-to-middle subset" was.

#### `H_core` — the literature moves one way only

Our ceiling **1.5 pW/kg** is Nimmo+ 2004 ([`2004GeoJI.156..363N`](https://ui.adsabs.harvard.edu/abs/2004GeoJI.156..363N))'s own model requirement (*"The core contains 400 ppm
potassium"*, Table 4), and the partition experiments since then print **ceilings**: Gessmann & Wood 2002 ([`2002E&PSL.200...63G`](https://ui.adsabs.harvard.edu/abs/2002E%26PSL.200...63G))
*"highest possible K content is about **250 ppm**"*, Bouhifd+ 2007 ([`2007PEPI..160...22B`](https://ui.adsabs.harvard.edu/abs/2007PEPI..160...22B)) *"∼25 or ∼250 ppm"*, Watanabe+ 2014 ([`2014PEPI..237...65W`](https://ui.adsabs.harvard.edu/abs/2014PEPI..237...65W))
*"less than **40 ppm** … less than 0.17 TW"*, Gaidos+ 2010 ([`2010ApJ...718..596G`](https://ui.adsabs.harvard.edu/abs/2010ApJ...718..596G)) §2 *"a few tens of ppm"* — all abstract only
except Gaidos, which is held. On the textbook conversion (natural K ≈ 3.5 × 10⁻⁹ W/kg) those are
**≈0.09 · 0.87 · 0.14 pW/kg**. ⚠ **That conversion is ours, and where a paper prints its own the paper
wins** (Brief 166 E): Watanabe+ 2014 prints *"less than 0.17 TW"*, which over its own core mass is
**0.088 pW/kg** — the textbook constant 3.5 × 10⁻⁹ is **56 % above** the 2.243 × 10⁻⁹ the paper's own
constants imply (⁴⁰K 1.917 × 10⁻⁵ W/kg, ⁴⁰K/K 1.17 × 10⁻⁴). Gessmann and Bouhifd print no power, so
their 0.87 and 0.09 stay **our arithmetic** and are labelled as such.
⚠ **So the axis is not symmetric: every later constraint is below our
ceiling**, and C25 (c) measured what that costs — the reference row's only positive corner falls
**+34.7 → −4.7 → −54.7** MW/K across 400 → 250 → 40 ppm **at C20's own rate (−36 K/Gyr)** — and
**+28.0 → −11.5 → −61.5** at the registered −33 K/Gyr, which is what C25 (c)'s table prints.

#### `Q_CMB` and the inner core — where our outputs sit against the printed ranges

| quantity | ours | printed |
|---|---|---|
| present `Q_CMB` | **5.07 TW** (C20), 4.91 at C14's closure | **5–17 TW** (Hsieh+ 2020 text, held); Nimmo 2007 ([`2007cody.book...31N`](https://ui.adsabs.harvard.edu/abs/2007cody.book...31N)) 6–14; Labrosse 2015 ([`2015PEPI..247...36L`](https://ui.adsabs.harvard.edu/abs/2015PEPI..247...36L)) isentropic 13.25 at present; Zhang+ 2022 mantle-side ∼10–12 |
| adiabatic requirement | `Q_ad` 4.31 (k 30) · 7.18 (k 50) · 10.05 (k 70) TW | **15–16 TW** at k 100 (Pozzo+ 2012 Table 2); ≈3 TW at k ≈20 (Hsieh+ 2020) |
| inner-core age | ⚠ **never nucleates in 4.54 Gyr** | 0.37–1.90 Gy (Nimmo 2007, four studies) · 0.3–1.0 Ga (Pozzo Table 2) · <0.7 Ga (Ohta) · **∼0.5 to >2.5 Ga** (Bono+ 2019 ([`2019NatGe..12..143B`](https://ui.adsabs.harvard.edu/abs/2019NatGe..12..143B)), *"span set by k"*) · >2 Ga at k ≈20 (Hsieh) |

⚠ **Our `Q_CMB` sits at the floor of the printed range, and the comparison collapses into the `k`
choice**: high `k` needs 13–16 TW for the adiabat alone — three times what we have — while low `k` needs
≈3 TW, which we clear. ⚠ **And "never nucleates" fits no camp at all**; that is C14's melting-curve
depression factor (0.80), which is outside P4's scope and is not touched here.

#### The papers say `k` is the deciding variable, and so does our own run

- **Nimmo+ 2004 §6.1 (held), printed:** *"Reducing the core thermal conductivity … increases the
  available entropy production, but has no effect on the rate of inner core growth. … Reducing the
  conductivity to **20 W m⁻¹ K⁻¹ results in positive entropy production throughout** (because `E_k` is
  reduced)."* ⚠ **C25 (c)'s `k` = 20 record column agrees except at the lowest potassium** (+269.9 …
  +76.3, but −13.1 and −16.7 in the two 40 ppm rows) — the paper's *"throughout"* is inside its own model,
  which carries 400 ppm K.
- **Nimmo Table 6** (k 20, `η₀` 2 × 10²² Pa s): `E_min` **+74** MW/K, inner-core age 1 400 Myr, **no
  potassium needed** — a printed anchor for the low-`k` case.
- **Nimmo Table 5**: every other parameter needs a multiple of its own error to close the budget and
  still gives negative `E_min`; only `ζ` reaches positive (**+54**), and its error is ±50 %.
- **Pozzo+ 2012 (held)**: high `k` *"approximately doubling the heat conducted down the adiabatic
  gradient … and halving the power to drive a dynamo"*; their Model 1 gives `E_J` **−111** MW/K.
- **Hsieh+ 2020 (held)**: *"the key role played by thermal conductivity on core evolution"*, with Fig. 3
  giving maximum inner-core age and minimum initial CMB temperature **as functions of `k` alone**.
- **Bono+ 2019 (abstract only)**: *"Plausible yet contrasting core thermal conductivity values lead to
  inner core growth initiation ages that span 2 billion years."*
- **Ours**: the `k` axis moves `ΔE_min` by **193** MW/K against `H`'s **98** — 2:1, measured on our own
  run.

#### The three owner decisions, in one place, with candidates and no selection

| # | decision | candidates | what each costs |
|---|---|---|---|
| ① | **which horn of C25** — ⚠ *where each number comes from is C25 (e); the two are not the same kind of number* | measured `T_c` 3 760 K · `Q_C`-in-range 4 155 K · keep C14's root 3 978 K | inner core and a positive band, at the price of contradicting the published flux · the published flux, at the price of `e_l` = `e_g` = 0 · the closure's own consistency, with the second horn's cost and none of the first's gain |
| ② | **how `k_core` is carried** | keep Nimmo's 50 ± 20 (30–70) · elect the low camp (Hsieh ≈20 / Konôpková 18–44) · elect the high camp (Pozzo · Zhang · de Koker, 95–140) · widen to the printed span 18–226 · unify with the sub-Neptune declaration (C49) | our current band is a subset nothing narrows · low `k` makes the budget positive nearly everywhere and needs no potassium (Nimmo Table 6) · high `k` closes the budget on its own (every row negative at k 100) · widening makes the answer a surer *cannot-say* · unification is a housekeeping decision with a physics consequence |
| ③ | **whether `ΔE` > 0 is our threshold** | the paper's own `ΔE` > 0, which it calls a threshold-avoidance · the printed required excess **0.1–1 000 MW/K** | the first is reachable in the 3 760 rows · ⚠ **no cell in C25 (c) reaches the upper end of the second**, so under that reading the answer is *fails* everywhere |

⚠ **Nothing here is chosen, and nothing in the engine moved.** This subsection is the literature laid
beside our numbers so that the three decisions can be made on printed values rather than on our own
outputs.

### C25 (e) 2026-09-09 — where each horn's number comes from, and they are not the same kind of number

**Read by the parallel seat (P5), transcribed with labels and grades.** Report:
`/Users/vana/Desktop/NearStars-artifacts/2026-09-09-c20-entropy-band/P5-c25-two-horns-sources.md`.
⚠ **Nothing is selected here**, and the two horns turn out to be different *kinds* of quantity — which
is itself the reason the choice cannot be made by comparing them.

#### Horn 1 — the declared 3 760 K is an **upper bound**, from a melting anchor

`engine/bodies/earth.yaml`'s `core_cmb_temperature: 3760.0` comes from Sinmyo, Hirose & Ohishi 2019
([`2019E&PSL.510...45S`](https://ui.adsabs.harvard.edu/abs/2019E%26PSL.510...45S), **abstract only**),
whose abstract prints it in these words:

> *"A small extrapolation of the present experimental results yields a melting point of **5500 ± 220 K
> at the ICB** … Accounting for the melting temperature depression due to core-alloying elements, **the
> upper bounds** for the temperature at the ICB and the core-mantle boundary (CMB) **are estimated to be
> 5120 ± 390 K and 3760 ± 290 K**, respectively. Such low present-day CMB temperature suggests that the
> lowermost mantle has avoided global melting."*

**What kind of number that is:** a pure-iron melting curve measured to 290 GPa in a resistance-heated
DAC, extrapolated to 330 GPa, reduced by an alloy depression, then carried down the core adiabat — a
**mineral-physics upper bound**, not a seismological or heat-flow measurement.

⚠ **And the depression that produced it is itself a minimum** (parallel seat P8, from the held paper):
the 3 760 K follows from **Si 2 wt% + O 3.6 wt%**, giving a melting-point depression of **380 ± 170 K** —
the *smallest* alloy load the paper considers, against a traditional CMB value of **∼4 000 K**. So "upper
bound" has two floors under it: a minimum depression applied to a pure-iron curve. **A heavier alloy load
would put the number lower, not higher**, which is the direction owner decision ① is already exposed to.

⚠ **And our own text labels it the other way round.** `engine/cmb_flux.py@«Q_CMB 는 하한이다»` calls the
declared core-side temperature a **lower** bound. **The engine's argument for that is about the engine's
own biases** — the D″ jump is set by a CMB flux this repository does not derive, and two named biases
point down — **and it stands**; what does not stand is applying "lower bound" to *Sinmyo's* number,
which the paper prints as an upper bound. The module keeps its own reasoning, with the paper's label
recorded beside it.

**Every printed alternative is higher, and the mantle solidus brackets exactly this gap:**

| core-side `T_CMB` | source | grade |
|---|---|---|
| **3 760 ± 290** — *upper bound* | Sinmyo+ 2019 | abstract only |
| 3 820 | Yukutake 2000 ([`2000PEPI..121..103Y`](https://ui.adsabs.harvard.edu/abs/2000PEPI..121..103Y)), thermal history | abstract only |
| **4 100 ± 300** assumed · **4 155** solved · 4 161 adiabat at CMB | Nimmo+ 2004 Table 1 · Table 4 · Fig. 1 | **held** |
| ≈4 050 implied | Anzellini+ 2013 ([`2013Sci...340..464A`](https://ui.adsabs.harvard.edu/abs/2013Sci...340..464A))'s ICB 6 230 ± 500 K carried down an adiabat — **the reader's arithmetic, not printed** | abstract only |
| *ceiling* pyrolite solidus **3 570 ± 200** | Nomura+ 2014 ([`2014Sci...343..522N`](https://ui.adsabs.harvard.edu/abs/2014Sci...343..522N)) | abstract only |
| *ceiling* chondritic solidus **4 150 ± 150** | Andrault+ 2011 ([`2011E&PSL.304..251A`](https://ui.adsabs.harvard.edu/abs/2011E%26PSL.304..251A)) | **held** |
| *ceiling* peridotite solidus **4 180 ± 150** | Fiquet+ 2010 ([`2010Sci...329.1516F`](https://ui.adsabs.harvard.edu/abs/2010Sci...329.1516F)) | abstract only |

⚠ **So the horn is also a choice about whether the lowermost mantle is molten:** 3 760 K stays below
every solidus above; 4 100–4 160 K crosses Nomura's and touches Andrault's and Fiquet's. **Sinmyo's own
closing sentence is that argument**, and it is the one place where the two horns argue with each other
through a third quantity rather than directly.

#### Horn 2 — the 4.5–9 TW range is Anderson 2002's, re-cited, and it is the oldest number in the set

Nimmo+ 2004 §5.1, verbatim (**held**):

> *"The total current heat flux from the core is 9 TW, which lies just within the **4.5–9 TW range
> recently proposed by Anderson (2002)** … This total heat flux exceeds that carried by the adiabat,
> 6.2 TW, so that the outer core is likely to be convecting."*

**So the range is a re-citation** of Anderson 2002
([`2002PEPI..131....1A`](https://ui.adsabs.harvard.edu/abs/2002PEPI..131....1A), **abstract only**,
whose abstract prints *"about 8 TW"* and *"P(conduction) = 6.8 TW"* — the 4.5–9 span is in the body we
do not hold). **Every later review keeps the floor near 5 and raises the ceiling:**

| range | who | grade | relation to 4.5–9 |
|---|---|---|---|
| **4.5–9** | Anderson 2002 via Nimmo+ 2004 | Nimmo held, Anderson abstract only | the horn |
| 6–14 | Nimmo 2007 | abstract only | same author, three years later |
| 5–15 | Lay+ 2008 ([`2008NatGe...1...25L`](https://ui.adsabs.harvard.edu/abs/2008NatGe...1...25L)) | abstract only | ceiling +6 |
| **5–17** | Hsieh+ 2020 | **held** | widest |
| **10–12** | Zhang+ 2022 | **held** | ⚠ **entirely above 9** |
| ≈3 (floor at k ≈ 20) · 13.25 · 15–16 (isentropic at high k) | Hsieh+ 2020 · Labrosse 2015 ([`2015PEPI..247...36L`](https://ui.adsabs.harvard.edu/abs/2015PEPI..247...36L)) · Pozzo+ 2012 | held · abstract only · held | these are *adiabatic floors*, not measurements |

⚠ **Our engine's 2.75 TW is below every floor in that table**, so *"outside the range"* does not change
whichever range is adopted — the ceiling choice is not what decides our verdict.

#### The coupling, which is why this is one decision and not two

In Nimmo's model the two horns are **one balance**: the bottom-boundary-layer flux of eqs 37–39 *is*
`Q_C`. A lower `T_c` shrinks the CMB jump that drives `F_b` — which is exactly why C25 (c) measures
**2.750 TW at 3 760 K and 7.693 TW at 4 155 K**. ⚠ **So the owner is not choosing between a temperature
and a flux; they are choosing which of Nimmo's two anchors to keep and which to override with Sinmyo.**

**The two beliefs, in the owner's own terms (P5 §(c), transcribed):**

- **Horn 1** — *"I believe the 2019 iron melting curve plus an alloy depression, carried down the
  adiabat, gives an upper limit on the core-side CMB temperature, and I take that limit as the value —
  which keeps the lowermost mantle unmelted and makes our boundary-layer heat flux small."*
- **Horn 2** — *"I believe the 2002 heat-flow synthesis Nimmo re-cites, whose 9 TW ceiling every later
  review has raised to 14–17, is the range a present-day Earth core flux must fall inside."*

### C25 (f) 2026-09-09 — the owner's decisions, wired; the band still straddles zero, and that is the answer

**Five decisions were put to the owner in C25 (b). Four are made, one is held, and a fifth thing was
decided that none of them asked about: what to do next.**

| # | decision | outcome |
|---|---|---|
| ① | which horn of C25 | **3 760 K** — Sinmyo+ 2019 ([`2019E&PSL.510...45S`](https://ui.adsabs.harvard.edu/abs/2019E%26PSL.510...45S))'s *upper bound* taken as the value, with the inner core it implies and the sub-range `Q_CMB` it implies |
| ② | how `k_core` is carried | **unchanged** — Nimmo's 50 ± 20, corners 30 / 70. C49's unification stays open |
| ④ | the on/off threshold | **`ΔE` > 0**, with the label below and two record columns |
| ⑤ | the potassium cap | **0.088 pW/kg** — Watanabe+ 2014's under-40 ppm, on **the paper's own conversion**. ⚠ *Written 0.14 when the decision was wired and corrected the same day (Brief 166 E): 0.14 came from our textbook constant, which is 56 % high. The decision — "the cap is Watanabe's" — is unchanged; only our arithmetic was.* |
| ③ | what the transport table is fed (C34) | ⚠ **held** — the third path changes that table's input, so choosing now would be choosing twice |
| — | **the third path** | ⚠ **adopted: build the missing term** — stagnant-lid capacity and long-term cooling, the two-regime law family C47 (e) named. **The band is not to be closed by picking numbers inside it** |

#### What the decisions did to the numbers, measured

⚠ **Three columns, because the decision was wired twice.** The middle column is the day's first
measurement, at the mis-converted `H` = 0.14 pW/kg; the right column is the same measurement at the
paper's own 0.088 (Brief 166 E). **Nothing in the verdict column changes between them** — which is the
useful thing the correction shows, and the reason the middle column is kept rather than overwritten.

| quantity | before | at `H` 0.14 (as first wired) | at `H` 0.088 (corrected) |
|---|---|---|---|
| Earth `ΔE` (centre) | — | **+30.1 MW/K** at the declared 3 760 K | **+26.5 MW/K** |
| eight-corner band (`k` × `H` × rate) | — | **−76.3 … +191.9**, **4 of 8** positive, inner core present | **−76.3 … +188.3**, **4 of 8**, inner core present |
| four corners at the fixed −33 K/Gyr | — | **+117.1 · +126.9 · −76.3 · −66.6** | **+117.1 · +123.2 · −76.3 · −70.2** |
| C20's own reference row (no inner core) | −259 … +32, 1/4 positive | ⚠ **−259 … −57, 0 of 4, verdict `fails`** (`T_c` 3 915.75 K) | ⚠ **−203.4 … −4.1, 0 of 4, `fails`** (`T_c` 3 911.29 K) |
| C14's root | 3 978 K | ⚠ **3 770.9 K** — the lower `H` moved the closure by 207 K | **3 770.33 K**, inner core **239.3 km** |

⚠ **Two of those rows say something the single-column version could not.** The band's **floor never
moves** — −76.3 in both columns — because the floor is the `H` = 0 corner, and no potassium decision can
reach it; only the ceiling moved, by −3.6 MW/K. And **C14's root barely moved** (−0.57 K) while its inner
core **grew** from 206.2 to 239.3 km, because a cooler core freezes more of itself: the correction moved
the closure *away* from the cliff at 3 772.37 K, from 1.47 K below it to **2.04 K** below it.

⚠ **So the band still straddles zero on the chosen horn, and it is the honest result.** The owner's four
decisions were each defensible and together they do not close the question: lowering `H` subtracts from
every corner, and on the horn that keeps the inner core the two largest positive terms survive to hold
the top corner up. **A decision that does not decide is worth recording as one.**

#### ⚠ Decision ⑤ mostly pre-empted decision ①, and the positive corners sit on a cliff

**The audit seat re-bisected C14's closure with the new cap** (60 iterations): at `H` = 1.5 pW/kg the
root was **3 977.9 K** (`Q_C` 4.912 TW, **no inner core**); at `H` = 0.14 it is **3 770.9 K** (2.834 TW,
**inner core 206.2 km**). ⚠ **That is 10.9 K from the declared 3 760 K, and both have an inner core** —
so the tension C25 was built on, *"the measurement has an inner core and the closure does not"*, is
**largely dissolved by the potassium cap alone**. **Decisions ① and ⑤ are not independent: ⑤ moved the
closure onto the same side as ①.**

**And this seat measured what that neighbourhood costs, because the two temperatures are 11 K apart and
their entropy is not:**

| `T_c` | inner core | `Q_C` | `ΔE` k30·H0 | k30·H0.14 | k70·H0 | k70·H0.14 |
|---|---|---|---|---|---|---|
| **3 760.0** — declared (owner ①) | **572.2 km** | 3.825 TW | +117.1 | **+126.9** | −76.3 | −66.6 |
| **3 770.9** — C14's root at the new cap | **206.2 km** | 2.841 TW | +1.6 | **+11.3** | −191.9 | −182.2 |
| 3 777.0 — 17 K above the declaration | **none** | 2.272 TW | −66.8 | −57.1 | −260.2 | −250.5 |

⚠ **The cliff has since been located exactly, and it is much closer than "within 17 K"** (this seat,
independent bisection, 60 iterations): the inner core is **206.2 km at 3 770.9**, 120.7 km at 3 772.0,
87.3 km at 3 772.3, and **gone at 3 772.4** — the boundary is **≈3 772.37 K**. ⚠ *And that boundary does
not depend on `H`*: neither `core_profile` nor the melting-curve crossing reads the potassium term, so
the correction in Brief 166 E moved the **closure** and not the cliff. At the corrected cap the root is
**3 770.33 K** with a **239.3 km** inner core, which is **2.04 K** below the cliff (it was 1.47 K at
0.14). **So C14's closure keeps its inner core by about two kelvin.**

⚠ **The inner core loses 366 km over 11 K and vanishes within 17 K**, and because `e_l` and `e_g` ride on
that radius the top corner falls **+126.9 → +11.3 → −57.1** across the same span. **So "Earth has an
inner core here" is robust and "572 km" is not**, and neither is the size of the positive margin. **The
sensitivity sits exactly where C14's melting-point depression factor 0.80 sits** — the same knob C25's
own scope named — which is why this is recorded as a measurement and nothing is decided from it.

⚠ **And the two rows now say opposite things, which is the clearest statement of the horn's weight.** P4
forecast *"lowering `H` makes the band read **fails**"* — that came true **for the reference row**, which
has no inner core. On the declared 3 760 K horn, `e_l` and `e_g` are alive and the same cap only moves
the positive corners down. **The same decision reads *fails* on one temperature and *cannot-say* on the
other.**

**What decision ⑤ cost, which was not in front of the owner when it was made.** Lowering the nominal H is a
one-line declaration, and it **broke two C20 reproduction anchors in the next gate** — `test_core_history` had
been reading `core_energy.H_CORE`, so C48's recorded Earth and Mars numbers were measured under a condition the
decision changed. The repair (Brief 166 D, at the end of this file) pins each anchor to its own H and adds the
declared-H rows beside them: **the gate grows by +114 s**, 235 → 360 s on that node. ⚠ *No result moved that
should not have moved, and Mars's criterion B still passes with more headroom (5.1 K) than before — but "a
declaration in C14 re-defines what C20's recorded anchors mean" was not on the decision sheet, and it is the
kind of coupling nobody has counted (C52 candidate).*

#### Decision ④'s label, and what the literature actually prints

**The threshold is `ΔE` > 0, and the label is that it is inherited, not derived:** *Nimmo+ 2004 ([`2004GeoJI.156..363N`](https://ui.adsabs.harvard.edu/abs/2004GeoJI.156..363N)) §4's
assumption, taken as ours; the paper itself calls it a threshold-avoidance.* The parallel seat's P6
survey (`/Users/vana/Desktop/NearStars-artifacts/2026-09-09-c20-entropy-band/P6-dynamo-criterion-literature.md`)
puts the label on firm ground:

- ⚠ **No paper prints "`ΔE` > 0" as a claim about nature.** The one paper that *uses* it says both
  *"a **necessary (though not sufficient) condition** … may be obtained by simply considering the energy
  or entropy production"* and *"any positive `E` is **assumed** sufficient to drive the geodynamo, **an
  assumption** which is discussed later"*.
- **The required excess is unknown by two orders of magnitude**, in the same paper's words — *"the excess
  entropy production rate required to power it is unclear"*, and *"the 2 TW Ohmic heating estimate of
  Roberts et al."* is the other end.
- **Other criteria in print, none of them ours:** `Φ` > 0 as *"permitted"* (Gaidos+ 2010 ([`2010ApJ...718..596G`](https://ui.adsabs.harvard.edu/abs/2010ApJ...718..596G))); a minimum
  Ohmic power of **0.2–0.5 TW** (Christensen & Tilgner 2004 ([`2004Natur.429..169C`](https://ui.adsabs.harvard.edu/abs/2004Natur.429..169C))), against estimates spanning **0.1–3.5 TW**;
  a critical magnetic Reynolds number **≈ 50** (Christensen & Aubert 2006 ([`2006GeoJI.166...97C`](https://ui.adsabs.harvard.edu/abs/2006GeoJI.166...97C))) or **> 40** as used on
  exoplanets (Gaidos+ 2010); and cooling-rate thresholds of **35 / 69 K/Gyr** (Gubbins+ 2004 ([`2004GeoJI.157.1407G`](https://ui.adsabs.harvard.edu/abs/2004GeoJI.157.1407G))).

**So the two record columns beside the verdict, neither of them the threshold:**

| record | value | where the 3 760 horn's top corner (+126.9) stands |
|---|---|---|
| Nimmo §5.1's estimate of the required excess | **≈ 100 MW/K** | ⚠ **clears it** |
| Roberts+ 2003 ([`2003eclm.book..100C`](https://ui.adsabs.harvard.edu/abs/2003eclm.book..100C))'s 2 TW Ohmic estimate, via §6.3 ⚠ *ADS files this chapter under Calderwood, Roberts & Jones — same work, different author order* | **≈ 400 MW/K** | ⚠ **does not** |

⚠ **The verdict is therefore "positive on part of the band, and short of the stricter published
requirement" — which is exactly why the third path exists.**

#### One line the same survey settles about the regime gate

P6 (b): the dipolar/multipolar transition is printed at **`Ro_ℓ` ≈ 0.12**, with Earth at **0.09** — and
**our gate's 0.12 agrees with the paper**. ⚠ **But the engine does not compute `Ro_ℓ`**: `dynamo_rocky`
branches on a **declared** `locked`, and the Rossby number is never evaluated. **The number we agree with
is one we do not calculate**, which belongs in C16's record and not in a claim about our dynamo regimes.

⚠ **Corrected 2026-09-09 (Brief 166 E), by reading both papers rather than either summary.** The line
above attributed the quoted sentence *"narrow interval around `Ro_l` ≃ 0.12"* to Christensen & Aubert
2006. **That sentence is Olson & Christensen 2006's**, and the two papers say the number differently:

| paper | its own words | what it is |
|---|---|---|
| Christensen & Aubert 2006 ([`2006GeoJI.166...97C`](https://ui.adsabs.harvard.edu/abs/2006GeoJI.166...97C)) | *"There is a rather clear transition from the dipolar regime (f dip > 0.5) to the non-dipolar one (f dip < 0.3) at Ro ≈ 0.12, irrespective of the values of the Ekman number, Prandtl number and magnetic Prandtl number. The only outlier is a non-dipolar case at Ro ≈ 0.09"* (Fig. 3) | **the primary source**: it *defines* the quantity, eq. (28), `Ro_ℓ = Ro · ℓ̄_u / π`, and calls it the **modified** Rossby number |
| Olson & Christensen 2006 ([`2006E&PSL.250..561O`](https://ui.adsabs.harvard.edu/abs/2006E%26PSL.250..561O)) | *"For the base-heated dynamos, the transition from dipole-dominant to multipolar dynamos occurs in a narrow interval around Rol ≃ 0.12"*, and the internally heated cases *"transition … is more gradual, shows more scatter, and it begins at smaller Rol-values"* | **re-uses it**, its eq. (15) reading *"as in CA [32]"* — and renames it the **local** Rossby number |

**So the attribution moves to C&A 2006 and the sentence stays with OC06.** ⚠ *Two things this settles
that the summaries did not.* First, **0.09 is not "Earth" in C&A 2006** — there it is the paper's single
non-dipolar **outlier**, a model case whose regime depended on its starting field; Earth's 0.09 is
OC06's Table 3 entry. Two different 0.09s, and our text had them as one. Second, C&A 2006's critical
magnetic Reynolds number is **"of order 50" in the abstract and 40–45 in the body** (their Fig. 2b), so
**our `Rm > 40` quotes the body value** — which is the tighter of the two and the right one to name.

⚠ **And one claim next door does not survive the same reading — recorded, not repaired.**
`engine/bands.py@«the multipolar grid {0.05, 0.10}, both printed by OC06»` is one of only two places
this engine claims a band has **both ends printed**. In OC06's text `0.05` appears as a **dipole-moment
ratio** — *"with M− ≃ 0.05M+ on the multipolar side"* — and the only other occurrences of either number
are inside **Table 3's per-planet columns**, which are `Ro_ℓ` and `Lo_dip` values for nine planets, not a
multipolar grid. **So "both printed" may be pairing two numbers that the paper prints about different
quantities**, which is the shape C50's fifth case names. ⚠ *This was found while verifying a different
citation and is not measured yet* — the check is one read of OC06's Table 3 against `MULTIPOLAR_FACTORS`,
and `bands.py`'s own docstring says a band that fails this test is a `point`, not an `interval`. **The
numbers are left exactly as they are** until someone runs that read.

### C26 — the superionic-ice representation above ice_x's 1 800 K ceiling — **listed 2026-09-04, not started**

⚠ *(2026-09-04, evening — owner's question, `superionic-ceiling-context-notes.md` §5)* **The 1800 K ceiling is the
intermediary's box, not the source's bound**: SeaFreeze v1.1.0's `VII_X_French` knot ceiling, read 08-27; French & Redmer 2015's
own grid runs to 2000 K and its stated validity is the *stability region*. Neptune's open-window column meets the ceiling at
**923.6 GPa · 1800 K, first contact** — above the ≈520 GPa where the same authors' ices field closes — so C26's object is a
fluid/superionic water representation at ~500–1000 GPa, not "ice above 1800 K". The ceiling did not move; nothing filled from AQUA.

**Why it opens**: close the near-surface water coverage gap under an envelope (the IF97 window of C24) and
Neptune's temperature bracket reaches ice_x's 1 800 K ceiling. Today an *earlier* gap sends the search elsewhere
and that wall is never met — the avoidance is a by-product, not a design (`water-world-convergence-context-notes.md`
§7; `test_ice_giant.py` header).
**What is needed**: a density and adiabatic-gradient representation of superionic ice, or a named refusal at that
boundary. The first step is the usual literature search — ⚠ which papers exist has **not** been checked; the
search itself is the first item.
**Consumers**: Neptune (an anchor) and ice giants generally. Under the relaxed C5 "not on the roster" would not be
a refusal anyway; here the consumer already sits in the anchors.
**What this is not**: not "Neptune is wrong" — it is "we cannot yet evaluate the region Neptune's solution has to
pass through". Listed only; the window stays closed under envelopes meanwhile.

### C27 — water fractions 0.05 · 0.15 · 0.20 do not converge on an Earth-mass rocky body — **listed 2026-09-04, not started**

**Symptom** *(corrected 2026-09-04 evening after the audit's reproduction; the work seat reproduced it on a scratch copy of the engine at
35d6eead — `interior.solve(1.0, cmf 0.325, imf, T_pot 1600)` with counters on `PhaseGap.__init__` and `Structure.__init__`)*:
`converged=False` with the surface condition missed **by a fraction-dependent amount**, the water fluid all the way up:

| ice_mass_fraction | T_surface | miss vs 1 600 K | p_surface | surface_reached | PhaseGap raised / structures built | T_cmb (unconverged, not read) |
|---|---|---|---|---|---|---|
| 0.05 | 1 587.7 K | −0.77 % | 0.000 GPa | True | 0 / 120 | 3 033 K |
| 0.15 | 1 613.7 K | **+0.86 %** (overshoots) | 0.000 GPa | True | 0 / 279 | 3 123 K |
| 0.20 | 1 576.7 K | −1.45 % | 0.000 GPa | True | 0 / 355 | 3 086 K |

The first wording ("missed by 0.75 % — the column tops out at 0.2 GPa · 1 588 K") described the 0.05 column only, and its
"0.2 GPa" is **unreproduced and removed**: every column reaches the surface (`p_surface` 0.000 GPa, `surface_reached` True), and
no log in the previous work seat's scratch (`c17_curve.log` printed T_cmb only) carries that number. ⚠ **Unlike C24, this is not
a `PhaseGap` refusal loop** — zero `PhaseGap` objects were constructed in any of the three solves (the counts above are the
instrument's, not an inference); C24 was refusal → 1.6× oscillation → a fixed 2-cycle, identical twelve times.
**Found**: during C17's measurement (`ocean-fraction-context-notes.md` §5), trying to bracket the maximum of the T_cmb curve.
0.0 · 0.1 · 0.25 · 0.3 converge; the fractions between and below do not.
**Mechanism**: **unknown.** Do not carry C24's diagnosis (a coverage gap) over to this item.
**Candidate, unconfirmed** — an observation recorded the same day: 1 600 K is Earth's *mantle* potential temperature, and put
on a body whose outside is water it lays a hot fluid layer at the surface; a water world's potential temperature should be
the water's. ⚠ No measurement says this is the cause.
The unconverged trial values (T_cmb 3 033 · 3 123 · 3 086 K) are recorded in §5's table and not read. **Listed only; start is
the owner's decision.**

### C28 — the dynamo's ice fraction comes from the composition preset, not a second declaration — **listed and built 2026-09-04 (owner-approved)**

**Ground**: the handoff inventory (`interior-dynamo-handoff-context-notes.md` §3, edge `:684`) found the one gap of kind *no
value*: `ladder(..., ice_mass_fraction=0.0)` took a separate input with a literal-0 default while `interior.COMPOSITIONS`
(`interior.py@«COMPOSITIONS: dict[str, tuple[float, float, float, str]] = {»`, slot 1) already carried the same body's ice fraction under `composition_intent` — two places knowing one
number, the second silently. **Built**: `dynamo_rocky.ice_fraction_from_state` — a declared `ice_mass_fraction` wins; else the
preset is *read* from `interior.COMPOSITIONS` (referenced, not copied; earth_like 0.00 · water 0.50); no preset → `cannot-say
(no composition preset)`, never 0. The source is printed in the result's notes ("ice_mass_fraction 0.50 (composition preset:
water …, grade class)"). No value authored. `chain.yaml@«- {from: tidal_locking, to: dynamo_rocky, kind: selects, via: locked,»` drops `status: gap` (the edge now flows); the old status and its text are kept in the note, dated. Anchors: every roster
body is earth_like (0.00), so no emitted value moves — the gate is the check. Tests: `test_dynamo_rocky.py` §5.
⚠ *Corrected 2026-09-04 (audit hold on b8d86b68)*: "every roster body is earth_like" was 2 of 5 — only `earth.yaml` and
`pandora.yaml` declare `composition_intent`; the other three (A b, Luhman 16 A/B) are outside the rocky ladder and must never reach the
preset lookup. b8d86b68 consulted the preset **before** the ladder's class gate, so their named refusal ("… 암석 사다리 밖이다")
regressed to "cannot-say (no composition preset)" — values None either way, but a named refusal lost its name. the follow-up commit "fix(dynamo_rocky): C28 - consult the composition preset only inside the rocky ladder" moves
the lookup behind the ladder's own gates (probe with the old default 0.0 first; consult the preset only for a body the ladder classifies);
all five bodies' results compared node by node as JSON against 5ad8f56c's `dynamo_rocky.py` on the same inputs — identical.

### C29 — the mantle potential temperature: an Earth-analog declaration now, self-derivation listed — **declared 2026-09-04 (owner); the loop is listed, not started**

**(a) Declaration and measurement.** `earth.yaml@«potential_temperature: 1600.0»` declares `potential_temperature: 1600.0` (petrological, the anchor); Pandora
declared none, so `interior_layers` solved isothermal and `core_state` refused ("온도가 없다"), and the one quantity the dynamo
asks of the interior (`conductor_phase`) never existed for Pandora. Owner declaration 2026-09-04: `bodies/pandora.yaml`
`potential_temperature: 1600.0` — **Earth analog, grade analog, not scaled** (dry rocky, composition_intent earth_like; source
comment beside the value). Measured with the read hook on `BodyState.__getitem__` (`run.py`, scratch copy):

| step | before the declaration | after (1600 K declared) |
|---|---|---|
| `interior_layers` | isothermal — `cmb_temperature` 0 | mantle-side T_cmb **2 347 K**, T_center 2 474 K, P_cmb 91.25 GPa (calibrated) |
| `core_state` | refuses: "온도가 없다" | **`lower_bound` · `conductor_phase` "undecided"** (judgment): the mantle-side lower bound 2 347 K sits under the melting curve 2 714 K, and a one-sided bound decides neither liquid nor solid — "declare `core_cmb_temperature` and this node answers" |
| `dynamo_rocky` | cannot-say (conductor_phase undecided); the key had no source | reads it (hook fired, source `core_state`) → still **cannot-say (conductor_phase undecided)** |
| C14 · cmb_heat_flux · C15 · C20 | refuse | refuse unchanged: "no core-side CMB temperature declared" |

So the declaration gives Pandora a geotherm and a `core_state` verdict *of the lower-bound kind*; the dynamo's key stays
undecided for a **second missing declaration** — the core-side CMB temperature that Earth declares separately
(`earth.yaml@«# C20 열진화의 초기온도 — Nimmo+ 2004»`, 3 760 ± 290 K, Sinmyo+ 2019). Whether to declare it for Pandora by analogy is a separate owner decision,
recorded here, not taken (P_cmb 91 vs Earth's 135 GPa makes the analogy weaker than the potential temperature's).

**Grounding level of the 1600 K itself** (parallel seat, `pandora-1600k-analogy-notes.md`, printed facts): (1) the only source is
Unterborn+ 2019 (arXiv:1905.06530, held), which calls 1600 K an **"Earth-like"** single-value simplification (`:94`) and **relaxes it
to 1400 / 1900 K** in its §3.2 (`:98`, 1900 K flagged as a surface-magma-ocean case); nothing there ties 1600 K to a mass or an age.
(2) No held paper prints a mass/age scaling of the potential temperature: Noack & Lasbleis 2020 eq. 22 holds T_um = 2000 K fixed
over 0.8–2 M⊕, Nimmo+ 2004 integrates Earth to T_m 1 613 K. The engine's `mantle_temperature_floor_min/max` (Brief 57) is
1 017–1 468 K for Pandora — a **floor family**, not an estimate, its own doc says. So the grade stays *analog* and the declaration's
comment says the source relaxes it to 1400–1900 K.

**(c) The dynamo declared on — owner decision 2026-09-04.** Rather than author a core-side CMB temperature for Pandora, the
owner declares what the board already states: `phase4/alpha_centauri.yaml@«- { name: magnetic_field, value: "75 µT (~1.8× Earth; the upper bound of the rocky-dynamo M+ lad»` "75 µT … a tidally driven iron-core dynamo",
and, in that same board file, "Radiogenic plus weak tidal heating … enough to drive volcanism, continental drift and a
dynamo" and "fast continental drift". `bodies/pandora.yaml` gains `dynamo_alive: true` and `stagnant_lid: false` (grade declared, sources beside
each). `dynamo_rocky.ladder` honours `dynamo_alive` **only while `conductor_phase` is undecided**; a computed liquid or solid
core is never overridden — the declaration is then ignored and the note says "declaration ignored: core_state decided …".
Grade stays judgment. Priority rule, read from the code: `BodyState.__getitem__` (`state.py@«def __getitem__(self, key: str) -> Any:»`) returns a declared
*input* before any recipe's value, so a declared key with the same name as a computed output would win — `conductor_phase`
is therefore **not** declared anywhere (it must stay computed), and the declaration takes its own name, `dynamo_alive`.

| step | before (c) | after (c) |
|---|---|---|
| `core_state` | `lower_bound` · `conductor_phase` undecided (2 347 vs 2 714 K) | unchanged — the declaration does not touch it |
| `dynamo_rocky` alive gate | `cannot-say (conductor_phase undecided)` | **alive** by owner declaration (note printed) |
| `dynamo_rocky` result | dipole null, B_eq null | regime 1 (dry, 0.64 M⊕), ℳ_base 1.0 ℳ⊕ (declared family), **B_eq 41.4 µT · B_pol 82.7 µT** (30 µT · ℳ · (0.8984 R⊕)⁻³), regime gate `undeclared (both emitted)` (no `tidal_locking`), multipolar 2.1–4.1 µT |
| board comparison | — | board 75 µT (`:2296`, "the upper bound of the rocky-dynamo ℳ⁺ ladder") vs engine 41.4 µT: **−44.8 %**, recorded in `expected.b_eq` (tol 100 %, comparison not enforcement); the board is not changed |

The difference is the board's choice of the ladder's upper bound against the engine's elected Earth-anchored ℳ_base = 1; the
engine cannot elect ℳ⁺ from anything it holds. Tests: `test_dynamo_rocky.py` §4b (declaration passes only an undecided core;
solid and liquid ignore it, liquid bit-identical).

**(b) Self-derivation — listed, not started.** The loop that would replace the declaration: obtain the present potential
temperature from C20's thermal history (`core_thermal_history` already emits `mantle_potential_temperature_present`,
1 525 K on Earth) and iterate it against `interior_layers` (whose `cmb_pressure` C20 consumes — a cycle). Why not now: it moves
one declaration onto two unmeasurable ones (`mantle_initial_potential_temperature`, `core_initial_temperature`) plus the
radiogenic budget, and it is exactly the structure + thermal-evolution coupling `rocky-planet-dynamo-methodology.md@«NearStars does not re-run RM22's full internal-structure + thermal-evolution»`
says this project does not re-run per body. `chain.yaml@«from: internal_heat_nontidal, to: dynamo_rocky»`'s note stands: no thermal model turns the heat budget into a
potential temperature, so consumers still declare it. And the loop is not yet better than the declaration where it can be checked:
on Earth C20's present T_m is **1 525 K**, −75 K (−4.7 %) against the declared 1 600 K and −88 K against Nimmo's own 1 613 K
(`core-thermal-history-context-notes.md@«Report lines, not gates: present T_m **1 525 K** against the declared 1 600 K (**−75 K**); present surface heat flow»`, a report line, not a gate). Listed by owner decision.

### C30 — tidal heat wired into the interior heat budget — **listed and built 2026-09-04 (owner: "조석 배선 다시 가보자"); `tidal-heating-context-notes.md`**

*Doc line numbers cited in this section are those of 839b2c7c (before b29b556e's contract blocks); add 18 (tidal en) / 15 (tidal ko) / 1 (heat, below :44) for the current files.*

Owner: Pandora's temperature is held by tidal heating, so the heat budget must carry it. Built: `engine/tidal_heating.py`
(recipes `tidal_heating` — the doc's §1 fixed-Q law, `io_power_ratio` on the printed ~1e14 W, the §6.1 outcome labels — and
`heat_transport_mode` — the §6.2 mode on the total surface flux); `internal_heat_nontidal` gains `l_int_total` · `t_int_total`
and a total-heat floor that is inverted only in a boundary-layer mode and refused by name under a heat pipe; chain.yaml,
contract blocks (en + ko), `bodies/pandora.yaml` tidal inputs (a, M_p, forced e, fitted k₂/Q — declarations with sources).
**Pandora**: Ė 1.866e16 W · F 45.33 W/m² (board 45, 0.7 %) · 186.6× Io · regime vigorous · mode heat pipe · l_int_total
1.868e16 W, t_int_total 168 K · total floor cannot-say (heat pipe). Io: 9.343e13 W inside the printed 0.6–1.6e14 band. Earth
unchanged; giants/BDs cannot-say (no orbit). Pre-registered Ⓟ. Not emitted in v1: `radius_ceiling`, `plains_temperature`
(§6.3–6.5 lid axis; the two edges carrying them are `status: gap`, dated); `tidal_transport.derive_potential_temperature` not
consulted (validation-failed). Dante's stale 900 km board rows are recorded in the note (§5), not repaired — that is C31.

### C31 — Dante's tidal and dependent board rows refreshed from the C30 recipe — **built 2026-09-05; main `7fd5a6ea`, `30317daf`, `b99b16a9`**

Constraints (owner, relayed): the board of record is the **main checkout's** `phase4/alpha_centauri.yaml`, which carries
uncommitted pre-crash changes — nothing is written there until instructed. Tool: `engine/tools/refresh_board_rows.py --board
<path> --body Dante` (draft in scratch) runs `tidal_heating` and rewrites `bulk.tidal_heating` / `tidal_surface_flux` with a
dated note ("refreshed … from tidal_heating @<sha>, R 521 km; was 900 km draft"); `geopotential_j2 reference_radius_km`
900 → 521 is a plain correction; the dependent rows (360 K / 673 K / 5.7 % / 2.1–2.4 m / albedo, glow) get only a dated
"stale: derived from the 900 km draft; awaiting moon_energy_budget recipe" note with the doc's 521 km values (223 K, 452 K)
beside them — no value authored, no note deleted. Dry-run on the worktree copy (diff only) first; main is a separate order.

**Built 2026-09-05.** Seven values moved (mass 8.0e21 → 1.552e21 kg, radius and reference_radius 900 → 521 km,
gravity 0.659 → 0.382 m/s², tidal_heating ~1200× → ~79× Io, tidal_surface_flux ~11,500 → ~2,324 W/m², and the
`internal_heat` echo), the identity row's frozen sentence had its one digit corrected (78 → 79, the old figure
being the rounded 1200 scaled rather than the law's own 79.28), and three rows no recipe can produce
(`surface_temperature`, `albedo`, `geopotential_j2`) kept their values and gained a dated stale note. J₂, C₂₂,
flattening and rotation_period do not move because the invariant is R³/M, not R or M — the resize preserves
density, and a tide-locked body takes ω from an untouched orbit; the 0.0037 % residual is the board rounding
1.551943e21 to 1.552e21. The `geopotential_j2` note carries the size of its own delay: 0.039 against 900 km is
0.0131 against 521 km, a factor 3 if read literally. The tool refuses by name when the satellites table and the
bulk rows disagree, and `--take-satellites-figure` is how the operator says which side is current — the guard
would otherwise have blocked the very repair it exists for, since the board disagreed with itself on purpose.

### C32 — band output and handoff choices — **listed 2026-09-04 (owner, 19:57); structure built 2026-09-05, `engine/bands.py`; instances landing one at a time**

Owner: *"자기장 세기는 밴드로 출력하면 좋겠다. 하나의 묶음에서 다른 묶음으로 값이 오갈 때는 사용자한테 선택지가 있음 좋겠어."*
(1) Strength-type derived values emit `*_min/*_max` beside the point, the width's source labelled. `dynamo_rocky` already carries
`dipole_moment_min/max` and `b_eq_multipolar_min/max`, so `b_eq_min/max` come from that width (regime grid · multipolar 0.05–0.10
· declared range); `dynamo_giant` and, later, `magnetosphere_geometry` follow. (2) At a bundle boundary (engine result → phase4
board, declared input vs computed value, canonical vs interesting-first) the engine emits a `choices` record — candidates, source,
grade — and the owner records the pick on the board with a reason; no silent default. The record's shape and its place in
`BodyState` / `run.py` are designed after C30 and C31. Trigger: Pandora's 41.4 µT (engine, C29 c) against the board's 75 µT.

**Built (structure).** `engine/bands.py`: three shapes, not two — interval, *floored point* (one end
printed, which is real information), point. A width with no printed source is refused; a bundle moves
in step so a corner grid cannot cross its members; a `Choice` needs at least two candidates and a
mapping of consequences, because a pick can improve one axis and cost another. The first instance
added a fourth state the design missed: **a band may have ends and no point inside them.** Eight
albedo rows are in exactly that state, and emitting one is refused — picking the point is a
`Collapse`, not a default.

**Instance 1 — Bond albedo (`engine/albedo_table.py`).** All eight surface types of
`surface-color-albedo-methodology` are ranges; the test parses them out of the document, so a doc edit
that moves a range fails the gate rather than drifting. The two consequence axes are printed and
**not ranked**: the ends of the volatile-ice row move `T_eq` by 1.351×, while the carbonaceous row is
three times wide and moves `T_eq` by 1.010×. No printed exchange rate says how many kelvin a factor of
three in brightness is worth, so the engine prints both and the ranking is the owner's.

**A correction to the brief, with the document quoted.** The relay called the albedo band and the
phase-integral band a bundle. They are not: the document joins the two routes with *or* — *"adopt a `q`
appropriate to the surface type (analog-grounded), **or** take the Bond albedo directly from a
solar-system analog"* — and `A = q·p` already has `A` on the left, so multiplying the analog table by
the phase integral is a category error, not a wide band. The real bundle is `q` with `p`, inside the
second route; it cannot be walked yet because no per-surface-type `p` table exists (§5 estimates `p`
spectrally per body). Named, not filled.

**Held for the owner — two findings on the α Cen Class II line.** The board's gas-giant evidence
adopts `A_B = 0.3` and its own sentence prints the Class II albedo as 0.5–0.8. (a) The adopted value
lies **below both ends** of the band it cites, so it is not a collapse to an end — the `Collapse`
record has no shape for it, and inventing one would hide the disagreement. (b) That 0.5–0.8 band is
printed on the board and in **no methodology document**; the eight-row table does not cover cloud
decks. Both are left as they stand.

**Instance 2 — the stagnant-lid ceiling (`tidal_heating.py`).** §6.2 prints the ceiling as 10–30
mW/m² and the code used 0.030: not a width dropped, an end chosen silently. The consumer is a label
table, so the width cannot pass through — it splits into branches, and this is the case where a
`Choice` is mandatory. The stated consequence is machine-checked: fed the four control fluxes the
engine itself produces, the high end reproduces the document's own label for three of them (Venus is
the exception, and it is the document's own stagnant-lid anchor), the low end for one. The second
axis is what the losers become — the table has nothing between the ceiling and the plate row, so a
body under the ceiling is not called unknown but *plate tectonics*, a positive claim made at 0.010
about Mercury and Mars, which the same table lists as stagnant lid. Default stays the high end.

**Instance 3 — the two greenhouse cases (`greenhouse_cases.py`), and a rule the structure was
missing.** The relay called them a published combination grid; they are two runs on two different
bodies by two different papers (Ramirez 2014 on early Mars, Wordsworth & Pierrehumbert 2013 on early
Earth), and Wordsworth's H₂ is a point, 0.1, not a range. So they are `Choice` candidates — one axis
with two options, the first place a candidate's value is a case name rather than a scalar — with no
default, because the document's instruction is to borrow a run that brackets the body.

The rule they forced: **walking a bundle in step is a second assumption, not the cautious option.**
Raising CO₂ lets a run reach the same temperature on less H₂, so pairing the low ends invents a
combination exactly as much as crossing the corners does. A band now declares `pairing="unknown"` and
`corners()` refuses it by name. Both cases are in that state, and the refusal is tested.

**Owner decision, 2026-09-05 — a band with no chosen point is emitted after all, and the label does
the work the refusal was doing.** The game cannot start without a number. So the point goes out
labelled, and the three origins never share a word: `printed` (the document prints the centre),
`chosen` (someone picked, and a `Collapse` says which end and why), `unchosen` (the engine filled the
middle). Ends and their source travel with the value. The grade vocabulary is untouched — filling a
middle is not a judgment, and "we filled it in" must not enter the same vocabulary as measurement.
A printed centre is never replaced by a computed one (660 µT stays 660, not the midpoint 675), and
the mean is arithmetic unless a band declares `mean="geometric"`, because choosing one for every band
would be an exchange rate the engine invented. `engine/tools/unchosen_defaults.py` counts the seats a
default is holding open — ten today — the same shape as C33's unmigrated-citation count.

That decision collided with the pairing rule in one place, and the collision is the interesting part.
A member of a bundle whose pairing nobody published has **no middle of its own**: filling one per
sibling rebuilds precisely the combination `corners()` refuses, so the guard on the corner grid would
have been reopened through the back door. Its emit sends the caller to the case's `Choice` instead,
and nothing stalls, because choosing the case supplies every member at once. The report separates the
two states rather than adding them up, since a count the owner reads must not blur them.

`Collapse` also gained `end="outside"`, for an adopted value that disagrees with the band its own
source prints. It exists so the α Cen `A_B = 0.3` cannot be quietly replaced by the midpoint 0.65 of
the 0.5–0.8 it sits beside — the disagreement stays visible while the owner decides.

**Verified, no work.** The multipolar grid `{0.05, 0.10}` already emits both ends from `dynamo_rocky`
(relay item 6, confirmed). The Hapke roughness presets are the enumerated form, not a band —
`hapke-shader-methodology` calls them *"discrete family presets"* and lists the set — and `Choice` is
that shape, so nothing is forced into an interval.

### P1–P3 — parked, each marked with the C it came from

- **P1 · Queyroux seam retrial (from C3).** The adopted below-kink mean (Queyroux+ 2020 · Prakapenka+ 2021,
  Brief 33) and the disputed 14.6–20.6 GPa refusal were built on a *simulated* liquid line (Reinhardt+ 2022,
  `ice_melt_table.py`, grade analog). The owner ordered *"점검부터 하자"* (relayed, Brief 64 follow-up): first
  comparison of the adopted values against the two **measurements** — Queyroux SM Table S1 (12 points with
  σ) and Kimura & Murakami 2023. Outcomes are pre-registered before the transcriptions arrive (the work seat's
  next brief); `ice_melt_table.py` is generated and is never hand-edited.
- **P2 · Kimura as arbiter of the disputed band (from C3).** Whether Kimura 2023 gives a point inside
  14.6–20.6 GPa at all — if not, C3's "arbiter" expectation was wrong and P2 closes on that record. Runs
  with P1.
- **P3 · Bethkenhagen ammonia (from C4) — redefined the same evening, and the first definition was wrong.**
  The owner approved a measurement (*"끝나고 그것도 재보자."*, `4b8e06ba`, 17:2x KST), and the directing seat
  first framed it as *"is the 2013 table's 330 GPa enough for C4?"* — **a wrong question**: the 2013 paper was
  never C4's missing piece. It has been held since 08-30 11:29 and **baked the same day** (`ammonia_table.py`,
  `80fde5d7`, 08-30 17:13); it is pure ammonia, and C4's open half needs the **2017 mixture grid**, still not
  held. So the 09-01 closure stands (see the C4 paragraph). What P3 actually is, three parts: ① the two
  stale "AIP paywall" phrasings corrected (done, this brief); ② the one-line reason the closure holds written
  into C4 (done); ③ **a C6-class measurement**: `ammonia_table.P_MAX_PA = 333.2 GPa` is the material's domain
  ceiling (`eos.py@«return ammonia_table.P_MAX_PA»`) and its isotherm range 500–10 000 K refuses outside (`eos.py@«if t < ammonia_table.T_MIN_K or t > ammonia_table.T_MAX_K:»`), and **no gate
  row says whether any roster column ever reaches either** — `test_interior.py` has no ammonia row
  (`test_ammonia.py` checks the transcription, not the reach). Measured by the `ice_x` template (a spy on the
  material, evaluation counts, positive control first). Measurement, not repair: a reach, if any, is reported
  and left.

  **③ measured 2026-09-03 17:59–18:18 (code `ee3a8308`), spy on `NH3.density` / `check_temperature` /
  `in_domain` and on `ammonia_table.density` / `pressure`; positive control first — one direct call fired
  `NH3.density` 1, `check_temperature` 1, `ammonia_table.density` 1 (62 table pressure lookups behind it), so
  the instrument counts.** Then, with every counter reset:

  | column | solve | nh3 evaluations | ceiling / isotherm refusals |
  |---|---|---|---|
  | Uranus | full `solve`, converged, 23 s | **0** | 0 / 0 |
  | Neptune | full `solve`, converged, 65 s | **0** | 0 / 0 |
  | Ganymede · Callisto · Titan · Europa · Enceladus | `infer_three_layer` band, 240 · 145 · 175 · 365 · 134 s | **0** each | 0 / 0 |

  **The ceiling 333.2 GPa and the 500–10 000 K isotherm range reach no roster column, and the reason is not
  the corridor — it is that nothing calls the material.** `interior.py` contains no `"nh3"` (static check), so
  the material is registered in `MATERIALS`, carries its domain check and temperature refusal, and has no
  consumer. That is a **C5 matter** (machinery without a consumer), and it sits beside C4's *"ammonia half —
  built"*: built as a material, not wired into any layer. **Wire it or retire it is the owner's decision; this
  row reports the measurement and does not judge.** Frozen as a gate row in `test_interior.py` (static check +
  positive control + zero fires on the two frozen ice-giant standalone integrations, ≈1 s) so the day someone
  wires ammonia into a layer, the row rings and the ceiling reach is re-measured under C6.
  **Gate on `bd81b237` (P3 ①②③ · C20 · C21, five commits): FAIL 0, 457 PASS, 19:18:41 → 19:40:01 = 1280 s** —
  +12 s on Brief 64's 1268 s, of which the new row is 0.81 s measured; the rest is run-to-run noise.
  **P3 is now an owner decision** (C5: wire it or retire it) — and the owner took it the same evening:
  see C22.

### C33 — citations resolved against the document instead of a line number — **built 2026-09-05 (owner: "인용 부패 싹다 고쳐"); `engine/check_refs.py`**

A line number is not a citation, it is a bet that the document will not grow, and the bet kept losing
silently. `internal-heat-luminosity-methodology.md@«**Returns** — `core_cmb_temperature_solved` [K] · `core_cmb_temperature_solved_min` [K] · `core_cmb_temperature_solved_max` [K] ·»` was a contract block's Needs line when 30 chain
edges were drawn against it, then another block's Needs line, then a Returns line — that last shift
happened inside `25980fdc`, the commit that went to *fix* citations. 24 of the 30 were wrong, 20 of them
from birth, and no reader could see it: five contract blocks in that one document carry near-identical
Needs lines. A line number the directing seat had read by hand at 22:00 (`:281-282`) was `:285` three
hours later.

So the engine cites phrases, and the citation carries its own test: `<doc>.md@«a phrase that occurs
exactly once in that document»`, with guillemets because a phrase contains quotes and apostrophes and has
to survive YAML, Python and Markdown unescaped. Inside a recipe module that declares `RECIPE = "<slug>"`,
the bare word `doc` in place of a file name means its own document, and *only* its own, because `radiogenic.py`
had used that form for
the tidal document's §6.2 table while `doc` meant the heat one. A citation can name the wrong document
entirely, which no line number can reveal.

`check_refs.py` enumerates every citation in `chain.yaml`, `bindings.yaml`, `bodies/*.yaml`, the engine and
scripts modules and the engine notes, and resolves each anchor: one match passes, zero is rotten, two or
more is ambiguous — a verdict the old scheme could not even express. Three more rules: an edge whose
citation lands inside `## Contract — \`X\`` must have X as one of its own endpoints (the only deterministic
test for the `:119` failure, and written so the four legitimate contract landings still pass); a landing on
a blank line, table separator or rule fails in wiring and code and warns in a preserved note; and a target
shared by two or more edges must literally name the payload each wants (8/8 on the reused targets,
useless on single-use ones). `test_check_refs.py` aims the checker at a synthetic document where all five
outcomes are known by construction, because a checker that only ever passes is the thing being replaced.

The same inheritance mechanism turned out to be inside the checker, which is the finding worth
carrying: rule 2 read each citation's edge endpoints with a regex over the citing line, so an edge
written as a block mapping — `from:`, `to:` and `ref:` on separate lines — silently inherited the
previous flow-style edge's endpoints, exactly as a new chain edge had been inheriting whatever
happened to sit on `heat:119`. The same disease in the data and in the instrument built to find it.
Endpoints now come from the parsed structure, queued per value so two edges sharing one ref are each
judged against their own. **Anything read line by line inherits from the line above; ask what.**

The audit found five enumeration holes, all "passes silently", all closed: an upper-case file name was
invisible (`DANTE_HEAT_TRANSPORT_EVIDENCE.md`), non-`.md` targets were not counted at all (unmigrated 204
→ 392 when that opened), `bodies/*.yaml` was outside the scan, a folded `note: >` block could hide a
citation from the line scan (YAML is now read from parsed values, which also makes the endpoints exact),
and a bare file name matched no pattern at all — that last one had already let two `## Related` citations
be quietly abandoned.

Measured basis for the design, from a month of edit history (parallel seat, `c32-l-loose-aim-notes.ko.md`):
citations break at ~1.4 %/month overall, **table rows are the worst target at 3.5 %** with 31 of 40
failures being ambiguity rather than rot, and list-like documents survive best when anchored on headings
(`data-sources.md` 78.4 %, `methodology-index.md` 87.0 %). Hence: anchor prose, not table rows; extend a
phrase until it is unique rather than truncating it, so the anchor still carries a claim.

chain.yaml is fully migrated: 209 anchors, every one resolving, no line number left in the wiring. Open: 174
citations on line numbers in code and notes, migrating in batches (`c32-h/i/k/l-*-notes.ko.md` carry the
blame traces). And the contract-heading anchors are loosely aimed by the shared-target rule's own report —
tightening them to a unique Need item where one exists (`` `mantle_radiogenic_power` [W] `` is unique;
`core_cmb_temperature_solved` occurs 5×, `t_body` 0×) is the next pass.

### C33 (b) 2026-09-09 — a second citation rule, counted and not judged: papers cited without a bibcode

**C33 made every anchor citation carry its own test.** This is the other half of the same habit: a
**paper** cited as *"author + year"* with no bibcode anywhere in its section — where a reader cannot
check the claim and, when the section also states a paper **grade**, cannot check the grade either.

⚠ **The first version counts and does not judge**, because the count is not a property of the tree but
of the rule. The audit seat's three implementations gave **160 · 193 · 185** for this one file (856–1008
across the tree), which is why `engine/tools/check_citations.py` carries **the rule's text and its known
false-positive classes beside the number** — a number copied without its rule is re-measured differently
by the next reader.

**Rule A, as implemented:** split the document on `### `; count citations **only in sections that contain
no bibcode at all**; accept a bibcode in backticks, ⚠ *including one wrapped in a markdown link, which
the first implementation missed and which inflated its count*; count `Author+ 2019`, `Author & Author
2002`, `Author et al. 2013`. **Rejected as false positives:** date prose (`Corrected 2026-09-08` — a year
followed by `-\d`), participle-plus-year heads (`Measured 2026`, a list in the tool), and the possessive
`Nimmo's` without a year — while *"Nimmo's 2004 Table 4"* **is** a citation and is counted.

**Rule A's first measurement, 2026-09-09: `engine/interior-core.md` has 27 sections with no bibcode and
124 citations in them.** The largest are C38 (15), C13 (13), C47 (10) and C9 (9).

⚠ **So the habit was the norm and the exception was the section that carried bibcodes** — C47 (i). One
confirmed count from before this brief: **C25 (d) held 28 author-plus-year mentions, 15 of them distinct,
and 0 bibcodes**; commit A of Brief 165 gave all fifteen a bibcode and an ADS URL. **The reason was not
that a regression had to be undone**, but that a section which states grades must carry the identifiers
that let those grades be checked.

⚠ **And the rule catches its own documentation.** This section quotes citation *examples* while carrying
no bibcode, so rule A counts **4** in it: the file went from **27 sections · 124 citations** to **28 ·
128** the moment this subsection was written. **No syntax for "this is an example, not a citation" was
invented** — it is recorded as a false-positive class in the tool instead, and it is one of the reasons
the first version only counts.

⚠ **Three defects in the first version of this tool, found by the audit seat and fixed in B2.** Its
`BASELINE` was **dead code** — never read, never written — so the count was printed with nothing to
compare against and **forty new citations tomorrow would have passed unnoticed**; it now holds
`(28, 128)` and prints *"⚠ 기준선과 다르다"* when the count moves (still no `FAIL`). Its gate line carried
`|| fail=1`, which **cannot fire** because `main()` always returns 0 — removed, with the reason written
beside the call so nobody reads it as judging. And `check.sh`'s comment said *"27 sections · 124"* while
the tool prints **28 · 128**; the four extra are this section's own examples, and the comment now says
so.

**Fixing the other 27 sections is out of this brief's scope**, and the promotion path is the one C45 (b)
class ③ uses: the count is printed on every run, and when it reaches zero the rule becomes a `FAIL`. **New
sections are expected to keep it from today.**

⚠ **Updated 2026-09-09 (Brief 166 E) — the rule caught its first increase, and the count is now 26 · 121.**
*"New sections are expected to keep it from today"* was tested within hours and **failed first**: 166 B/C
wrote C25 (f) with ten author-plus-year mentions and no bibcode, and the counter read **29 · 138**. 166 E
attached the bibcodes and repaired two more sections in the same pass — **C25 (f) 10 · C25 (b) 5 · C34
re-drawn 2** — landing at **26 · 121**, below the first measurement. ⚠ **This section's own four are left
in place** and are the reason the count will never reach zero by repair alone: three of them are the
`Author …` strings written above as the regex's worked examples. ⚠ *Naming them again in this paragraph
would raise the count by three, which is how this note found out — the first draft did exactly that and
the counter read 124.* **So the promotion path above needs one amendment**: the `FAIL` threshold is
this section's own count, not zero. **The remaining 25 sections are the backlog the rule was built to
surface** (C38 15 · C13 13 · C47 10 · C9 9 …) and are still not this brief's.

### C34 — what the heat-transport table is fed, and where its thresholds come from — **thresholds half answered 2026-09-06: none is published, and the 0.03 became a C32 band. What the table is fed is still the owner's**

Three facts, named and not repaired. The code's verdicts are unchanged by this entry.

**Venus splits** — ⚠ **and it is C46's, not this item's.** What follows is the measurement; *why* the
table cannot place Venus is a question about the table's axis, and it moved to C46 on 2026-09-07.
The §6.2 table prints Venus as its stagnant-lid anchor body at 10–20 mW/m² — ⚠ **corrected 2026-09-09:
that number is not a measurement of Venus.** It is Reese, Solomatov & Moresi 1998's
([`1998JGR...10313643R`](https://ui.adsabs.harvard.edu/abs/1998JGR...10313643R)) **melting ceiling**, read where their
stagnant-lid curve meets the peridotite solidus at the lid base (their Fig. 4b/c, wet-olivine `n = 3`),
and the paper prints Mars's as 15–30 in the same sentence. **The only printed measurement of Venus's
heat flow is 78 ± 69 mW/m²** (Smrekar+ 2023, [`2023NatGe..16...13S`](https://ui.adsabs.harvard.edu/abs/2023NatGe..16...13S),
from active rifting), beside a **model** global mean of ∼40 (O'Rourke & Smrekar 2018 §2.2) and local
21–287 at coronae; **there is no global measurement.** The word *measured* stood here through four
sections and is removed. Earlier text: *"at a measured 10–20 mW/m²"*,
and the engine computes 37.75 mW/m² for it and returns **plate tectonics**. The arithmetic is Earth's
21.32 TW scaled by mass to 17.37 TW over 4.6023e14 m². No core-mass fraction in 0.20–0.40 flips it; the
flip is at 0.4636.

**The plate-tectonics ceiling 0.135 W/m² is authored.** It is `0.09 * 1.5` in `tidal_heating.py`, and the
document prints the 0.09 capacity but not the ±50 % width: a full sweep for `50 %`, `factor of 1.5` and
`×1.5` returns two hits, both a different quantity (Io's heat concentration, 50 % of the flow from 1.2 %
of the surface). The comment "read ±50 % as its row" is the code's own reading of the table.

### Resolved 2026-09-07 — the document's own anchors picked, and we took the result

**Owner**: *"고증에 맞는 건 아래쪽 아냐?"* ⚠ **Not a choice of ours.** Yesterday's decision was to carry
a band; measuring the band showed it is **not verdict-neutral**, and the discriminator was already in
the document.

| what is fed | reproduces the document's own §6.2 anchor labels |
|---|---|
| **low end** — tidal + radiogenic, what the engine already feeds | **3 of 4** |
| high end — the measured surface heat flow | **1 of 4** (Earth alone) |

⚠ **This is the same shape as the neutrino case earlier today**: two readings disagreed, and a third
body of evidence said which one. There it was Ruedas's table; here it is **the document's own anchor
bodies**. In neither case did a seat pick.

**Why the margin matters, and it is the only number that shows why this decision has weight.** The
candidates span **2.203×**, while Mercury (0.01575) and Mars (0.01587) sit only **1.90× and 1.89×**
below the stagnant/plate boundary at 0.030. **The spread is wider than their margin**, so any upward
revision of the fed quantity past ~1.9× moves both out of stagnant lid — and the document labels both
stagnant lid. ⚠ **That statement does not assume uniform scaling**; an earlier draft multiplied every
body by Earth's 2.203× and that construction was ours, not a measurement of those bodies. **The margin
comparison stands without it.**

⚠ **Nothing in the output moves.** The engine already feeds the low end, so no value changes anywhere.
**What changes is the grounds**: it was the recipe's own contract sentence at `tidal:59`, added by
`b29b556e` — the code declaring what it feeds — and it is now the document reproducing three of its
four anchors.

⚠ **Two things this does not fix.**
1. **Venus disagrees at both ends.** The document prints it stagnant lid at 10–20 mW/m²; the engine
   computes 37.75 and returns plate tectonics. ⚠ **And the 10–20 is not a Venus measurement at all** —
   parallel seat P8, from the held papers: it is **Reese+ 1998's melting ceiling** for stagnant-lid
   convection, a finite-element model output. What the literature prints for Venus is a **model** global
   mean of **∼40 mW/m²** (O'Rourke & Smrekar 2018 ([`2018JGRE..123..369O`](https://ui.adsabs.harvard.edu/abs/2018JGRE..123..369O)) §2.2),
   **local** flexure estimates of **21–287** at coronae (their Table 2), and **78 ± 69** from active
   rifting (Smrekar+ 2023 ([`2023NatGe..16...13S`](https://ui.adsabs.harvard.edu/abs/2023NatGe..16...13S))) — **there is no global
   measurement of Venus's heat flow.** Earth's global measurement, for scale, is **86 ± 6** (Jaupart+ 2007
   ([`2007mady.book..253J`](https://ui.adsabs.harvard.edu/abs/2007mady.book..253J))). **So the engine's 37.75 disagrees with a
   ceiling, and it is within 6 % of the only model global mean anyone prints** — which reverses which side
   of this mismatch looks wrong. **Three of four, not four**, and the Venus mismatch is
   independent of this decision — see the paragraph below, which was written before it.
2. **The plate ceiling 0.135 is still authored** (`0.09 * 1.5`). This decision is about **which quantity
   is fed**, not about where the thresholds sit. Different question, still open.

**The document does not say what quantity to feed the table.** Earth alone has four candidates spanning
**2.20×**: the measured surface heat flow 0.0921, the total flux the engine actually feeds 0.0418,
`implied_surface_heat_flux` 0.0769, and §6.1's own 0.08. The single sentence that says "the total flux"
is the contract block at `tidal:59`, which `b29b556e` added — the recipe's own declaration, not the
methodology's statement, the same shape as C30's finding (e). The document meanwhile writes that there is
no published W/m² boundary between the modes and that any flux threshold is a conversion rather than a
citation, so of the three thresholds the 0.03 is the cheapest to turn into a C32 band (the document
already prints 10–30 mW/m²).

Two more from the same batch, for the facets they belong to: **ε Eri b's 540–810 µT band is authored** —
of the six endpoints across three brackets only one reproduces from the document's printed inputs (546.5,
+1.2 %), and GJ 896 A b's upper bound comes from an age the recipe itself refuses; and **Cassandra's
verdict is carried by one declaration, not by its mass and radius** — `composition_intent` `earth_like`
(ice 0.00) gives 197.38 µT against `water` (ice 0.50) giving 0.3948 µT, a factor 500, and the board's own
9.0e23 kg / 3400 km is 5 467 kg/m³ = 0.991 ρ⊕, rocky, which runs opposite to declaring the ice-rich
preset (real Ganymede is 1 936 kg/m³). Both are in `c32-d-e-epseri-cassandra-notes.ko.md`.

### C34 re-drawn 2026-09-09 — C47 closed without filling, so the question is what the table is *declared* to be fed

⚠ **The computable survivor did not survive.** C34 had narrowed to **0.0769 W/m²** —
`mantle_flux.implied_flux`, the only candidate that is both the right quantity and computable for our
bodies — with one defect recorded against it: it is a **mobile-lid** law and C47 (b) measured it handing
Mars **85.7 mW/m²** against Reese's own **15–30** ceiling. **The stagnant-lid law that would have
replaced it is now closed as *named, not filled*** (C47 (k): `q_E/q_M` = 1.5114 against the 3.68 / 4.78
the Urey ratios need). **So there is no computed surface-flux candidate that reproduces Mars**, and
waiting for one is no longer a plan.

**That changes the question rather than answering it.** C34 was *"which of four candidates is right"*;
with two disqualified, one uncomputable and one wrong-lid, it becomes **"what does this engine declare
it feeds the §6.2 thresholds, and with what label"** — the same shape as `MANTLE_SHARE = 0.70` or
`T_s = 293 K`, which are declarations rather than measurements. ⚠ **A declaration is the owner's, so the
options are laid out and none is chosen here.**

| option | what it declares | grade of the source | where it is verified, where it fails | what the table then returns | the cost |
|---|---|---|---|---|---|
| **(a) keep the current feed** — tidal + radiogenic, **0.0418** on Earth | *"the thresholds are read against the body's internal production, not its surface flow"* | measured radiogenic sets (`radiogenic.py`), **analog** | reproduces **2 of 4** §6.2 anchor labels (Mercury 15.75 ✓, Mars 15.87 ✓); **fails Earth 41.80** and Venus 37.75 | the labels the engine emits today | ⚠ C47's finding stands against it: **it is a different quantity from the one the thresholds are defined on**, and on the C46 ladder Earth reads *plutonic-squishy lid* |
| **(b) declare `implied_flux`** — **0.0769** on Earth | *"the thresholds are read against a modelled surface flow"* | Nimmo+ 2004 ([`2004GeoJI.156..363N`](https://ui.adsabs.harvard.edu/abs/2004GeoJI.156..363N)) eqs 34–36, **analog**, reads no measurement | right quantity; **fails Mars** at 2.9–5.7× Reese's ceiling (C47 (b)) | a surface flow for every body, Mars included | ⚠ a **mobile-lid** law on the archetypal stagnant lid, and C47 (k) closed the stagnant-lid alternative without filling it |
| **(c) declare the measured flow, and refuse where it does not exist** — **0.0921** on Earth | *"only a measured surface heat flow may be fed"* | Davies & Davies 2010 ([`2010SolE....1....5D`](https://ui.adsabs.harvard.edu/abs/2010SolE....1....5D)), **measured** | exists for **three solar-system bodies and none of ours** | `regime_candidates` and **no single regime** for every NearStars body | ⚠ the table would never place any body this project actually ships |
| **(d) refuse to feed it at all** until a law reproduces Mars | *"no regime is emitted while no law reproduces both bodies"* | — | — | what `solve_mode` already does when more than one regime stands | ⚠ C46's ladder and `dynamo_rocky`'s regime gate both lose an input that exists today |
| ~~0.08~~ | — | ⚠ **disqualified**, no source in any version of the document and the same number used under two labels | — | — | — |

**Two things that ride on the choice, so it is not only C34's.**

- **C46's ladder reads the same input.** Its rungs are scored on the fed quantity, and C46 (b)'s measured
  finding — *the flux is a sieve, and it sieves almost nothing* — was measured on the current feed. **A
  different declaration re-scores the ladder**, which is why this row and C46's move together.
- **`dynamo_rocky`'s regime gate** takes `heat_transport_mode` through a `status: gap` edge
  (`engine/chain.yaml@«mode 는 라벨이고 열류는 수다»`), so option (d) removes a value that a downstream
  consumer is already declared to want, even though it does not read it yet.

⚠ **Nothing in the engine changed with this entry, and no value moved.** The current feed is unchanged
and still emits what it emitted yesterday; what changed is that **the item is no longer waiting on C47**,
and what it waits on now is a declaration.

### C35 — `stellar_wind` computes, and has no document to be a recipe in — **listed 2026-09-06, deliberately not registered**

`engine/stellar_wind.py` produces all three of the node's declared outputs from real routes (`v_sw`
declared, `n_sw` derived, `p_ram` wired) and the Ramstad IMB on top of them. It is **not** registered
with `registry.recipe`, and that is a decision rather than an omission: `chain.yaml`'s `stellar_wind`
node has no `recipe:` document, so a `## Contract` block has nowhere to live and `check_contracts`
fails the moment it registers. No stellar-wind methodology document exists — `docs/reference/` has
`stellar-photosphere-color` and nothing else on the wind — and the magnetosphere document is the
**consumer** of the wind, not its owner, so hanging the contract there would misfile it.

**What a future stellar-wind document owes, so nobody researches this twice:**

- **`n = Ṁ / (4π r² v m_p)`** — spherical steady-state mass conservation, a textbook identity and
  therefore exempt from the paper-grounding rule. At solar values it returns 6.70 cm⁻³ at 1 AU,
  inside the observed 5–7.
- **`v_sw = 400 km/s` is an assumption, not a measurement**, and the repository has exactly one of
  them: *"stellar_wind_speed_kms = 400 (assumed, Wood) unless measured"*
  (`phase3/stellar_wind_synthesis/context-notes.md`). No host carries a measured wind speed.
- **The hosts that carry `Ṁ`** — five, and **all five are measured**, by one method and one group:
  astrospheric Lyman-α, Wood et al. Alpha Centauri A **2.0**, Barnard's Star **0.2**, ε Ind A **0.5**,
  Proxima Cen **0.2**, τ Cet **0.1**, in solar units. ⚠ Two corrections to the working list this was
  relayed as: **40 Eri A carries none**, and **Barnard's Star does**. ⚠ And α Cen A's own note says
  its 2.0 is the **combined A+B astrosphere value**, the pair sharing one astrosphere at a ≈ 24 AU —
  so it is not A's wind, and a future document must decide how to split or refuse to.
- **`P_SOLAR_1AU_NPA = 2.0` in `scripts/refs/magnetopause_geometry.py` carries no bibcode.** Two
  Proxima boards already depend on it.
- ⚠ **The 10 % gap.** That 2.0 nPa anchor against 1.79 nPa from the identity above, at the same place
  and the same wind. Left standing on purpose. A future document either reconciles them or writes
  down why it cannot — replacing one with the other silently would move two boards' values under a
  commit about something else.

### C36 — the tidal-locking timescale — **released by the owner 2026-09-06 as the next item**

`tidal_locking` is declared with `recipe: tidal-locking-timescale-methodology` and nothing registered
against it, so `locked` has never reached any of its **eight** consumers. Brief 121 stood a placeholder
in its place; C36 replaces that with the computation.

⚠ **Two things are already set up for it and should not be rebuilt.** The wiring is frozen and tested
(`test_provisional.py`), so when the recipe lands only the answer moves — whatever changes then changed
because of the physics. And the pre-registered outcomes are recorded in `regime-gate-context-notes.md`
§7 as a control table: `locked` False → dipolar by rule; True → the C16 two-name refusal.

⚠ **The gate will fail on the day it lands, by design.** `provisional.recipe_arrived()` reports any
placeholder whose node has acquired a recipe, and `test_provisional.py` proves that fires. Deleting the
placeholder is part of landing C36, not an afterthought — the gate will say so.

### C38 — the recipe draws from two tidal models, and nothing says they may be mixed — **closed by record 2026-09-06**

`tidal_locking` takes its despin timescale from **Goldreich & Soter 1966** and its equilibrium spin
from **Hut 1981**. Barnes 2017 (held) puts those in different camps: §2.1, *"The Constant Phase Lag
Model … commonly utilized in Solar System studies (e.g. Goldreich and Soter 1966; Greenberg 2009)"*,
and separately *"the 'constant-timelag,' or CTL, model (Mignard 1979; **Hut 1981**; Greenberg 2009)"*.

⚠ **Barnes calls them "qualitatively different"** and says they coincide *"if a linear dependence
between phase lags and tidal frequencies is assumed"*. Neither our document nor our code states that
assumption. **And it cannot be checked here**: Hut 1981 is in the cache **as a scan**, so what it
actually assumes is unreadable — the first time the "held but unreadable" grade has cost anything.

⚠ **The seam is quantitative, not formal.** Barnes: *"the **CTL model does not predict such short tidal
locking times** for Earth-like planets in the HZ of G dwarfs."* The two models disagree about the very
number this recipe returns.

**Do not read this as licence to blame the Venus mismatch on the seam.** Barnes prints a known failure
of this model family — *"As is well known, the current estimates for Q and τ of Earth, 12 and 640 s,
respectively, predict that the Moon has only been in orbit for 1–2 Gyr … far less than its actual age
of 4.5 Gyr"* — and the literature's escape is to move Q: *"many researchers … assume that the
historical averages of Earth's tidal Q and τ have been about 10 times different. Indeed, Kasting et
al. (1993) assumed Q = 100"*. That is the same shape as Venus needing `Q/k₂ ≲ 28` against a printed
class of 10²–10³.

⚠ **But that escape does not reach Venus, and the reason is printed.** The justification is oceanic:
*"tidal dissipation in the oceans is a complex function of continental positions and in the past
different arrangements could have allowed for weaker dissipation."* Venus has no ocean, and neither do
the dry rocky bodies and moons of this roster. **The same qualifier bounds the model warning itself** —
the models are *"poor approximations to the physics of the deformations of planetary surfaces,
**particularly those with oceans and continents**"*. ⚠ And the escape is shaky on its own terms: a
measurement puts the factor at **two**, not ten — *"the modern Earth is about twice as dissipative as
compared to the historical average (Green et al. 2017)"*.

So the Venus finding is **not** dissolved by the seam. If anything it hardens: the standard way out of
this family's known failure is unavailable on a waterless planet.

**How it closes, and it is not by being fixed.** The mixed quantity is `ω_eq`, and `ω_eq` is reached
only through `STATE_PSEUDO`, which needs `e ≥ 0.206`. No body reaches it, so that branch has never
executed and no verdict in the engine depends on which lag model it came from. The seam is inert, and
it is closed as a record rather than as a repair.

⚠ **The reason it is inert is a worse thing than the seam, and it moved the same day.** It was never
that our bodies are on circular orbits. `eccentricity` has **no supplier** — `orbit_elements` has no
recipe — and `tidal_locking` used to substitute `0.0`, classifying every body `1:1 synchronous` on a
number nobody set. That is C41, and it is the finding this item produced. As of the owner's decision
the substitution is a registered placeholder at `e = 0.10`, which lands in §4's unprinted gap, so
every body now reads `unclassified` — still short of `STATE_PSEUDO`, and the seam is still not reached.

⚠ **So the closure now rests on a choice of ours, not on data.** Before, the seam was unreachable
because a value was missing; now it is unreachable because the placeholder sits below the state
threshold. **Move that placeholder to 0.25 and C38 is live again** — the CPL/CTL disagreement would
start deciding rotation states. Whoever changes that number is changing this item's status, and this
paragraph is where they find that out.

**The replacement is available whenever eccentricity starts flowing.** Barnes 2017 prints a CPL-native
equilibrium period, so the recipe could stand on one model instead of two:

    P_eq^CPL = P for e < √(1/19);  2P/3 above          (Barnes eq. 6, verified on the page image, p. 8)
    P_eq^CTL = P / (1 + 6e²) at low e, ψ = 0           (eq. 16 — what Hut gives us today)

⚠ **√(1/19) = 0.2294, not 1/19 = 0.0526.** A plain-text extraction of that page drops the radical and
leaves a lone `p` on its own line, and the difference is a factor of 4.4 that decides an anchor: at
0.0526 the Moon (e = 0.0549) sits just above the threshold and CPL would predict **3:2** against its
observed 1:1; at 0.2294 the Moon is far below and CPL predicts 1:1, agreeing. **The body that lands
near the threshold is Mercury** — e = 0.206, nine-tenths of the way to it, still below — where CPL
predicts 1:1 and the observation is 3:2. ⚠ That is not CPL failing: an equilibrium period is where the
tide alone would drive a body, and Mercury's 3:2 is a **capture** outcome. This recipe does not compute
capture and says so; Goldreich & Peale 1966 puts the Moon's synchronous capture probability at 0.71.

**Switching would also end a dependency we cannot read**: Hut 1981 is held only as a scan, and the
linear-phase-lag assumption that lets the two models coincide would no longer be needed. ⚠ **Neither
closes what stays open**: Goldreich & Soter 1966 and Murray & Dermott 1999 are still not held, so
`τ_lock` remains carried as what the methodology document prints. C38 closing does not close that.

### C40 — a fitted value has no seat in the vocabulary — **listed 2026-09-06, not started**

C32 gave three words for where an emitted number came from: **printed** (a document prints it),
**chosen** (a person picked it from a band), **unchosen** (the engine filled a middle and said so). A
value **fitted backwards from a wanted output** is none of the three, and the boards are full of them.

The clearest is Dante's `k₂/Q`, because the board does not hide it: *"The tidal term needs k₂/Q ≈
0.0016 at the simulated e ≈ 0.005, which is fitted rather than predicted."* The number exists because
a chosen tidal-heating flux needed it, so asking what its uncertainty is means asking how tightly that
target was chosen — which nobody has written down.

**C39 made this visible rather than creating it.** Wiring the declaration into `tidal_locking` turned
`τ` from `0.0315–0.315 yr` into `0.0203 yr` for Dante, and from `0.288–2.88 yr` into `2.88 yr` for
Hades. Before, not knowing was a width; now it is nothing. `tidal_heating` reads two declarations of
this kind (`k2_over_q` and `eccentricity_forced`) and its own header already calls them declarations,
so every body carrying one has the same hole.

⚠ **Two different things are called "fitted", and merging them would be the first mistake.**

- **Fitted to our own output** — Dante's `k₂/Q`, Hades's `1e-3`. No independent existence; the residual
  is whatever the target was.
- **Fitted in the literature, then clamped by us** — `pause_alpha = 0.42`, Jupiter's fitted ceiling
  from Rutala 2025, held rather than extrapolated because the planet sits outside the calibration
  range. Here a published fit quality *does* exist, and the clamp is a recorded owner decision.

These need different treatment, and this item does not yet say what either one is.

⚠ **What this item is not asking for.** It is not asking anyone to give a fitted value a band. Choosing
a width for one means deciding what the fit's residual is, which nobody has done and which is the
owner's call, not the engine's — the same line drawn three times already today. What it asks for first
is the **word**: somewhere to record that a number was solved backwards, so a reader can tell it apart
from a measurement at a glance instead of following a citation to find out.

### C41 — `eccentricity` has no supplier, and the recipe answers anyway — **listed 2026-09-06, not started**

`tidal_locking` reads `eccentricity` to choose among §4's rotation states. **Nothing produces it.**
`bindings.yaml` says `eccentricity: {produced_by: [orbit_elements]}`, and `orbit_elements` is not among
the fifteen registered recipes. So the value is absent for every body, and `solve` fills it with `0.0`.

The consequence is not a refusal, which is what makes it worth an item: **every body comes out `1:1
synchronous`**, and the reason line says "despun" without ever saying that the eccentricity behind the
classification was assumed. Pandora, Dante and Hades are all classified on a zero nobody wrote.

⚠ **The boards are not silent about eccentricity — they use a different name.** `eccentricity_forced`
is declared for Pandora (0.005), Dante (0.0186) and Hades (0.0385), and `tidal_heating` reads it.
**Do not assume the two names are one quantity.** A forced eccentricity is what a resonance maintains;
the despin formula wants the orbit's actual eccentricity at that moment. For a body locked in
resonance they coincide, and for a body with a free eccentricity they do not. Treating similar names
as the same quantity is the failure this engine hit four times on 2026-09-06 alone — `rotation_period`
spelled three ways, "constant Q" meaning two models, RM22's `ν`, and a phrase count read as a claim
about a concept.

**Related but not the same as C37.** There a name mismatch made a node **refuse**; here it makes the
node **answer**. A refusal is visible in the output and gets fixed; an answer on a substituted zero
propagates to eight consumers of `locked` and looks exactly like a result.

**Owner decision, 2026-09-06: (b), the provisional pattern.** Three routes were on the table and they
differed in what each claims — (a) keep the `0.0` default, which is the silence this engine has spent
two days removing; (b) take it through `engine/provisional.py`, so the substitution is counted, barred
from emit and recorded at both ends; (c) read `eccentricity_forced`, which asserts the two names are
one quantity and needs someone who knows that they are. **(b) landed the same day**, and
`orbit_elements.eccentricity` is the pattern's first real instance.

⚠ **The value chosen classifies the entire roster, uniformly.** Not one body supplies its own
eccentricity, so unlike `ω₀` — which is at least multiplied by per-body data before it decides
anything — this one number is the answer for everybody:

| provisional `e` | Pandora | Dante | Hades |
|---|---|---|---|
| 0.0 (what ran before) | 1:1 | 1:1 | 1:1 |
| 0.03 | 1:1 | 1:1 | 1:1 |
| **0.10 (chosen)** | **unclassified** | **unclassified** | **unclassified** |
| 0.25 | pseudo-synchronous | pseudo-synchronous | pseudo-synchronous |

⚠ **What was chosen is the interval, not the number.** Any value in §4's unprinted gap `(0.055,
0.206)` gives that row exactly; `0.10` has no standing of its own and must not acquire one by sitting
in a file. **And the input is not neutral** — `0.10` asserts *this body's eccentricity is middling*
just as surely as `0.0` asserts *circular*. What the interval buys is not an input that claims
nothing; it is an input whose **output declines to classify**, which is the only one of the three
rotation states that carries the placeholder's own meaning of *not yet a value*. Those two are
different sentences, and reading the first for the second is how `0.10` would become a neutral value
in someone's mind.

⚠ **The interval stops below 0.206 on purpose.** Between our pseudo threshold and Barnes's CPL
threshold `√(1/19) = 0.2294` there is an 11 % gap where this engine would say pseudo-synchronous and
the CPL model would say 1:1. Parking a placeholder there would manufacture C38's disagreement out of a
number nobody measured. **That the gap exists at all is what keeps C38's seam alive** even while the
item is closed.

⚠ ### Declared 2026-09-07 — the forced eccentricity IS the orbital eccentricity

**Owner**: *"이심률은 실제값 줘야하지 않나? 공명에 의한 강제 이심률은 시뮬 돌려서 나온거니까 그대로 써야지."*

⚠ **The engine's doubt was about the field's name, and the name was the only evidence for it.** This
item and brief 127 both argued that a *forced* eccentricity — what a resonance maintains — might not
be the *orbital* eccentricity the despin formula wants. **The boards say where the numbers came from,
and nobody had looked**: Dante's row reads *"가정한 평균이 아니라 안정성 시계열에서 측정한 e_rms
0.0186"* — an assumed mean was replaced by one measured from the stability run — and Pandora's reads
*"at the simulated e ≈ 0.005"*. These are measurements of the orbit in a simulation, not a theoretical
forcing term. **A resonance maintaining an eccentricity does not make it something other than that
orbit's eccentricity; it is what keeps it there.**

`bodies/pandora.yaml` now declares `eccentricity: 0.005` beside the existing `eccentricity_forced`,
each with its own source anchor. Measured through the recipe, before and after:

| | before | after |
|---|---|---|
| `rotation_state` | `unclassified` | **`1:1 synchronous`** |
| `locked` | True | True |
| `τ` | 99.35 yr | 99.35 yr (`e` is not in the despin formula) |
| `eccentricity_pick` | `provisional` | — |
| `refuse_emit` | *cannot emit: eccentricity is provisional* | **clear** |

**Nothing moved except the classification and the guardrail.** The placeholder is released for this
body — guardrail ③ no longer blocks its emit — which is the outcome C42 was worried about arriving by
a route that cannot fire.

⚠ **The point is not that 0.005 lands below the threshold; it is that the whole oscillation does.**
The sim's `e` for Pandora runs 0.00016–0.0072 and Dante's runs 0.0002–0.031, against §4's 1:1 ceiling
of 0.055. **Dante's maximum is 0.15 of our pseudo-synchronous threshold**, so 1:1 holds across the
excursion rather than at a point that happens to sit low.

⚠ **A caveat that belongs next to the declaration, not in a footnote.** The eccentricities are measured
— **in a run whose masses are not the ones the board ships**:

| body | sim mass | board mass | ratio | sim R | board R |
|---|---|---|---|---|---|
| Pandora | 4.300×10²⁴ kg | 3.850×10²⁴ kg | 1.12× | 5724 km | 5724 km |
| Dante | 8.000×10²¹ kg | 1.552×10²¹ kg | **5.15×** | 900 km | 521 km |
| Hades | 5.000×10²¹ kg | 5.000×10²¹ kg | 1.00× | 750 km | 750 km |

Dante was five times heavier in the run that produced these numbers. **It does not overturn the
decision** — a measured eccentricity from a nearby configuration beats a placeholder chosen for
saying nothing — and the verdict is robust, since even Dante's excursion maximum sits at 0.15 of the
threshold. **But "measured" without "measured in which configuration" is the failure this repository
recorded today under a different name**, so it is written here rather than left to be rediscovered.

### What that decision looked like before it was made — the overnight measurement

Asked overnight, with the owner asleep and nothing declared: what would each roster body's rotation
state become if `eccentricity` were taken from the `eccentricity_forced` already on the boards?

| body | `eccentricity_forced` | today (provisional 0.10) | if declared | vs our 0.206 / CPL 0.2294 |
|---|---|---|---|---|
| Pandora | 0.005 | `unclassified` | **1:1 synchronous** | 0.024× / 0.022× |
| Dante | 0.0186 | `unclassified` | **1:1 synchronous** | 0.090× / 0.081× |
| Hades | 0.0385 | `unclassified` | **1:1 synchronous** | 0.187× / 0.168× |

**No body reaches `STATE_PSEUDO`, so C38 stays closed.** All three sit far below both thresholds; the
largest, Hades, reaches 0.187 of ours.

⚠ **But the reason C38 stays closed would change, and improve.** Today it is closed because *our
placeholder sits below the state threshold* — a choice of ours. On declared values it would be closed
because *the three bodies' forced eccentricities are all below it* — **data rather than a decision.**
That is the sentence this table exists for.

⚠ **Nothing was declared.** Every body moves `unclassified` → `1:1`, which is a verdict changing, and
the forced eccentricity may not even be the quantity the despin formula wants (C41 above). The table
is here so the decision is cheap, not so it looks made.

**Guardrail ⑤ is aimed at the wrong event, and that is worth more than the placeholder.**
`test_provisional.py` fires when `orbit_elements` gains a **registered recipe** — and `chain.yaml`
declares that node `kind: measured`, `domain: given`, in the layer it names
`engine/chain.yaml@«outputs: [a, e, i, lan, aop, n]»`. **It is not supposed to acquire a recipe.** Ten of the eleven `given`
nodes have none, by design; the one that does, `body_class`, carries `kind: computed` and its own
`recipe:` key, so `kind` is the discriminator and `domain` is not. **The day that trigger fires may
never come**, which makes the guardrail decorative here even though the pattern is right in general.

**The event that should release this placeholder is a body declaring the value.** The mechanism
already behaves correctly — `solve` uses the placeholder only when `eccentricity is None`, so any body
that declares one stops using it immediately — but nothing *notices* that the placeholder has gone
stale for the rest. That check is a scan of `engine/bodies/*.yaml`, and it is the honest form of
guardrail ⑤ for a measured node.

### What building `orbit_elements` will actually involve — measured, not scoped

The obvious question is whether the node owes eccentricity or more than that, and the files answer it
without anyone deciding. **The node already exists and is not a recipe's job.** `chain.yaml` gives it
`kind: measured`, `domain: given`, `engine/chain.yaml@«outputs: [a, e, i, lan, aop, n]»`, with
`outputs: [a, e, i, lan, aop, n]` and **seven `requires` edges** — to `body_figure`, `cassini_state`,
`tidal_locking`, `tidal_heating`, `dynamo_rocky`, `t_eq_stellar` and `moon_energy_budget` — plus an
`influences` and an `excludes`. **So "build `orbit_elements`" means make bodies declare these values,
not write a solver.** `bindings.yaml` additionally attributes four derived values to it —
`orbital_period`, `hill_radius`, `satellite_stability_limit`, `barycentric_split` — **none of which
appear in the node's own `outputs`**, so bindings and chain do not agree on what this node produces.

⚠ **One of the ten cannot be supplied and the file says so.** `barycentric_split`'s own note reads
*"binary-epoch-pipeline 이 근거인데 chain 에는 노드가 없다"* — the procedure has a methodology document
and **no node in the chain**. That is not a decision waiting to be made; it is a named hole, and it
should be visible before anyone starts rather than discovered at the eighth value.

⚠ **And the same quantity is called three things at three layers.** This is C37's class, except that
C37 had one wrong name while here every name is live and in use:

| layer | name |
|---|---|
| `chain.yaml` edge `via` | `a`, `e`, `n`, `i`, `period` |
| `bindings.yaml` | `semi_major_axis_au`, `eccentricity`, `inclination_deg`, `orbital_period` |
| body files | `semi_major_axis_km`, `eccentricity_forced` |

`tidal_locking` and `tidal_heating` read `semi_major_axis_km`; `body_class` reads
`semi_major_axis_au`. **Nothing bites today** — the two tidal recipes take the body file's key directly
and bypass the binding, and `body_class` falls back to a reference value when the `_au` name is absent,
so `check_via --gate` passes. **But `hill_radius` and `orbital_period` both name `semi_major_axis_au` in
their `derived_from`**, so the first real `orbit_elements` meets it head-on.

⚠ **Four of the six elements are read by no registered recipe — and the reason is not that nobody
wants them.** `inclination_deg`, `longitude_ascending_node`, `argument_periapsis` and `mean_anomaly`
are read in zero places because **their consumers are unbuilt too**: of the seven `requires` edges,
only `tidal_locking`, `tidal_heating` and `dynamo_rocky` have recipes, while `body_figure`,
`cassini_state`, `t_eq_stellar` and `moon_energy_budget` do not. Inclination's consumer is
`moon_energy_budget` (`via [a, i, e]`), which does not exist yet. **The question is therefore about
order, not about need** — supply ahead of the consumers, or with them.

⚠ **Two things here are the owner's, not the engine's**: that ordering question, and which spelling of
the semi-major axis is canonical — or whether the conversion gets one named home the way
`q_over_k2_from_declaration` did in C39.

### C42 — the release event never happens on a measured node — **listed 2026-09-06, not started**

Guardrail ⑤ exists for one reason: **a placeholder must not quietly become permanent.**
`recipe_arrived(registry.registered())` reports any placeholder whose node has acquired a real recipe,
and `test_provisional.py` reads the live registry so the gate goes red on the day that happens.

⚠ **For `orbit_elements` that day is not coming.** `chain.yaml` marks it
`engine/chain.yaml@«outputs: [a, e, i, lan, aop, n]»` with `kind: measured`, `domain: given` — the value is *supplied*,
not computed. Of the eleven `domain: given` nodes exactly one has a recipe, `body_class`, and it
carries `kind: computed` and its own `recipe:` key. **`kind` is the discriminator; `domain` is not.**

**The machinery is not broken — it is aimed at the wrong event, and the outcome is the same one it was
built to prevent.** The first real instance of the pattern is, today, on a trajectory to permanence,
guarded by a check that cannot fire.

⚠ **And this is not one placeholder's problem.** ⑤ consults the registered-recipe set and nothing else,
so **any** placeholder standing for **any** measured node inherits the same hole. It is a gap in the
general form, found by its first use.

**The shape of the repair**: the release condition depends on the node's `kind`.

| node `kind` | release event | how it is checked |
|---|---|---|
| `computed` | a recipe is registered for the node | `recipe_arrived()`, as today |
| `measured` | **a body file declares the value** | scan `engine/bodies/*.yaml` for the output's key |

The mechanism downstream is already correct — `solve` uses the placeholder only when `eccentricity is
None`, so a body that declares one stops using it at once. What is missing is that **nothing notices
the placeholder has gone stale for everyone else**, which is precisely what ⑤ is for.

⚠ **A second disagreement sits in the same node, and it is separate.** `bindings.yaml` names
`orbit_elements` as producer of `orbital_period`, `hill_radius`, `satellite_stability_limit` and
`barycentric_split`; the node's own `outputs` in `chain.yaml` are `[a, e, i, lan, aop, n]` and list
none of the four. **Two files disagree about what this node produces**, and `barycentric_split`'s own
binding note already records that its chain node does not exist at all. Whoever builds the supply side
meets both.

### C44 — a name that argued against its own value — **listed 2026-09-07, not started**

`eccentricity_forced` carries, for every roster moon, an eccentricity **measured from the stability
simulation**. Dante's board row says so in as many words: *"가정한 평균이 아니라 안정성 시계열에서
측정한 e_rms 0.0186"* — an assumed mean was replaced by a measured one. Pandora's says *"at the
simulated e ≈ 0.005"*.

⚠ **The name says something else, and it won.** Across brief 127 and this file, two seats reasoned that
a *forced* eccentricity is what a resonance maintains and therefore might not be the *orbital*
eccentricity the despin formula wants — a real distinction, argued carefully, and **built entirely on
the field's name.** Neither opened the board row that says where the number came from. The owner did,
in one sentence: *"공명에 의한 강제 이심률은 시뮬 돌려서 나온거니까 그대로 써야지."*

**This is C37's class — a name that does not match its value — with something C37 did not have: a
record of the name actually misleading someone.** C37's `rotation_period` spellings caused a node to
refuse; this one caused two seats to withhold a correct value for a day and to build a placeholder,
an item and a guardrail discussion on top of the withholding.

⚠ **What makes it worth an item rather than a rename**: the fix is not obvious. `eccentricity_forced`
is read by `tidal_heating`, where *forced* is doing real work — it distinguishes an eccentricity
sustained against damping from a free one, which is exactly what a tidal-heating calculation needs to
know. **The name is not wrong for its original consumer.** It became wrong when a second consumer read
it for a different purpose. Whether that resolves by renaming, by aliasing, or by leaving both keys
declared side by side as `bodies/pandora.yaml` now does, is not decided here.

**The general shape, which is the part worth keeping**: *a name is evidence about intent, not about
provenance.* When a value's origin decides how it may be used, the origin has to be read, and it lives
on the board and not in the key.

### C45 — the check compares labels, not lookups — **listed 2026-09-07, not started**

`check_contracts` is this engine's structural check: it holds each methodology document's `Needs` and
`Returns` against what the recipe actually uses. **It reads `set(candidate.inputs)`** — the keys of the
dict the recipe builds for its own evidence — and those keys are strings the author typed. **The string
handed to `state.get(...)` is never examined.**

⚠ **So a recipe can look up a key nobody supplies and stay green indefinitely**, provided it files the
resulting `None` under a name the contract recognises. That is not a hypothetical: it is exactly how
C37 survived. `dynamo_rocky` looked up `rotation_period`, labelled the `None` `"rotation_period"`, the
contract said `rotation_period`, and the check passed on every run while the value was never once
supplied.

**This is the widest of the blind checks found on 2026-09-06/07**, and the others were narrower by
comparison: a skip list that never reached its directory; guardrail ⑤ watching an event a measured node
cannot have; a citation checker that did not recognise one citation form. Those were single checks with
single blind spots. **This one is the structural check at the centre, and it applies to every recipe.**

**The detection is static, and the principle is proven.** Extract the literal in every
`state.get("…")` / `state["…"]` with `ast`, and require that set to agree with **both** the evidence
keys and the contract's `Needs` — three sets, one vocabulary, where today only two are compared.
Prototyped read-only against all 13 recipe modules: the extraction works on every one, and run against
`ce7aff2d^` it finds `rotation_period` among `dynamo_rocky`'s lookups — **it would have caught C37**.

⚠ **What the prototype's current output is not.** It reports mismatches on seven nodes, and **they are
not triaged findings.** At least five come from the prototype itself: `tidal-heating-methodology.md`
holds **two** contract blocks, and the sketch assumed one node and one `Needs` per file, so it paired
`tidal_heating`'s node with the wrong Needs list — the contract does declare `k2_over_q` and the rest.
**The sketch fell into a trap this repository had already written down**, under *"two tables in one
file make the first match unusable"*. Whoever builds this must key on the block, not the file.

⚠ **Some of the remainder may be real and are the same question restated**: `body_class` looks up
`state.get("body_class")` for a value its contract calls `declared_class`, and several recipes look up
`radius` where the contract says `radius_earth`. Whether those are aliases the loader resolves or C37
repeated is **exactly what this check exists to answer**, and it is not answered here.

**Not built now**: it is a new gate check and needs a full lane. The item comes first; the tool follows.

### C45 (b) 2026-09-09 — the instrument, pre-registered before it is built

⚠ **Written and committed before a line of the check exists**, so that what counts as a finding cannot
be chosen after seeing what the tool prints.

**The instrument, and why it is not the AST route C45 sketched.** `engine/state.py` is 113 lines and
every read funnels through **one** place — `BodyState.__getitem__`, with `get` wrapping it — which looks
in `inputs`, then in every applicable `Result.values`, then raises `Missing`. ⚠ **There is no alias
resolution anywhere in it.** So the actual lookup key can be captured at runtime: `run.solve` marks the
node it is about to run, and the two readers append `(node, key, hit | miss)` to a list on the state.
**The failure C45 names — a lookup nobody supplies, filed under a name the contract recognises — is a
`miss`, and a miss log reports it exactly**, including keys built at runtime that no `ast` pass can see.

**The AST pass stays, as the backstop.** A lookup on a branch the sample bodies never take leaves no
runtime record, so the literal keys are extracted too and the check compares **three** sets per contract
block: **runtime misses · AST literals · the document's `Needs`**. C45 asked for three sets and one
vocabulary; the change is that the first set is now what the code *did*, not what its author typed.

**Keyed on the block, not the file** — `tidal-heating-methodology.md` carries **two** `## Contract` blocks
and `parse_contract` already selects by node name; the sketch that ignored this produced five of its
seven "mismatches".

⚠ **`state.get_optional(...)` is added, and this is the one design decision in the brief.** Some misses
are legitimate: the engine already contains **five** preference lookups —
`engine/core_history.py@«state.get_optional("radius") or state.get_optional("radius_earth")»` is the pattern — plus
`dynamo_rocky.ice_fraction_from_state`, where a declared value wins and a preset is the fallback. **A
miss there is the design working.** Rather than an allowlist, those call sites move to a named entry
point, so the intent is visible to the next reader and to the checker at once. **Whether a lookup is
optional becomes a statement in the code, not a judgement in the tool.**

**Pre-registered outcomes — the check must prove it can fail before its result is written down.**

| # | test | required |
|---|---|---|
| ⓐ | the clean tree | **passes** — 13 recipe modules, every miss either declared optional or matching a `Needs` item |
| ⓑ | a scratch copy with one letter changed: `dynamo_rocky`'s `rotation_period` → `rotation_period_` | **fails**, naming that key |
| ⓒ | `ce7aff2d^`, where C37 was live | **fails**, naming `rotation_period` — the historical case this instrument exists for |

⚠ **ⓑ is this brief's form of *"if it always fires it is a constant"***
(`engine/test_interior.py@«늘 발화하면 상수다»`): a checker that cannot be made to fail has not been shown
to check anything.

**What is a finding and what is not, fixed now.** A finding is a key that is **missed at the end of a
full graph run** (not merely missed early and supplied later by a downstream node), is **not** declared
optional, and is **not** in the contract's `Needs` — or the reverse, a `Needs` item that no lookup ever
requests. ⚠ **Everything else is the tool's own noise**, and the two candidates C45 already named
(`body_class` vs `declared_class`; `radius` vs `radius_earth`) are expected to resolve as *precedence*
rather than as C37 repeated — `radius` is supplied by `mass_radius`'s Result, and `earth.yaml`'s own
`radius:` sits under `expected:`, which the engine reads only for comparison.

**Cost, and what this brief does with what it finds.** The check runs inside `check_contracts.py`, which
**already** calls `run.solve` on every body file, so the runtime log is one append per lookup and the AST
pass is a parse of 13 modules — the expectation is **no measurable gate time**, and the measured number
goes in the implementing commit. ⚠ **Findings are reported in a table in C45 and repaired in a later
brief**: a repair may move a value, and this brief is the instrument.

### C45 (c) 2026-09-09 — the instrument runs, ⓐ failed as registered, and the disease is live in four places

⚠ **The pre-registration's first outcome failed, and the cause is the pre-registration, not the tree.**
C45 (b) required *"the clean tree **passes** — every miss either declared optional or matching a `Needs`
item"* **and** required ⓒ, that C37 — whose `rotation_period` **was** a `Needs` item — **fail**. **Those
two cannot both hold.** The implementation followed ⓒ, so ⓐ broke on the first run: 9 nodes flagged.
**Recorded as a failure of the registration**, in the words it was registered in, with (b) left as
written.

⚠ **And the repair is not to narrow the rule — that is what pre-registration exists to prevent.** The
verdict is **split into three classes, all of them printed on every run**, so nothing is hidden by being
reclassified:

| class | signature | verdict |
|---|---|---|
| **①** | the lookup misses on **every** sample body **and** the resulting `None` is filed in `Result.inputs` **under the same name** — *value absent, name present*, which is exactly how C37 stayed green | **FAIL**, outside a named baseline of the four existing instances |
| **②** | a non-optional lookup that misses everywhere and is **not** in `Needs` — the misspelling shape | **FAIL** |
| **③** | a `Needs` item that no roster body supplies, where the call site copes (a default, or the evidence filed under another name) | **counted, printed, baseline recorded — not a FAIL yet** (C50) |

**What the first run found.**

| class | count | where |
|---|---|---|
| **①** | **3 nodes · 4 keys** | `body_class` — `gas_mass_fraction`, `semi_major_axis_au` · `dynamo_rocky` — `dynamo_regime` · `interior_layers` — `porosity_cap` |
| ② | **none** | — |
| ③ | **8 nodes · 8 keys** | `core_material` in `cmb_heat_flux`, `core_energy_balance`, `core_entropy_production`, `core_thermal_history` · `ice_mass_fraction` in `dynamo_rocky`, `internal_heat_nontidal`, `interior_layers` · `interior_layers` also `differentiated`, `envelope_z`, `gas_mass_fraction`, `initial_porosity`, `tidal_heating` · `tidal_locking` — `permanent_quadrupole` |
| record | 10 nodes | `Needs` items never looked up at all (they may arrive as another node's output) |
| record | 2 nodes | lookups in the source that no sample body exercises — `heat_transport_mode` (5 keys), `tidal_heating` (2) |

⚠ **So C37 was not one historical accident: its exact signature is live in four places today.** Those
four are entered in the `CLASS1_KNOWN` baseline and **listed as C50** — repairing them can move values,
which is a separate brief. **Anything outside that set fails the gate**, so the disease cannot spread
quietly while the four wait.

**How the classification was justified rather than assumed.** Four runs, each a full
`check_contracts.py`:

| # | run | result |
|---|---|---|
| ⓐ′ | the clean tree, log on | **`rc=0`, 136 s** — no `FAIL`, class ③ at its baseline (8 nodes · 8 keys), **1 182 lookups** compared against `Needs` and the AST literals |
| — | the same tree, log **off** (`NEARSTARS_LOOKUP_LOG=0`) | **141 s** — ⚠ *five seconds **slower** than with the log, i.e. the log's cost is below this machine's run-to-run variance.* No opt-in is needed; the gate keeps it on |
| **① fires** | one pair removed from `CLASS1_KNOWN` | **`rc=1`**, naming `dynamo_rocky: … dynamo_regime (C37 의 서명, 클래스 ①)` |
| **② fires** | one letter changed in a live lookup (`age_gyr` → `age_gyr_zz`, reverted) | **`rc=1`**, naming `dynamo_rocky: 아무도 공급하지 않는 조회이고 Needs 에도 없다 — age_gyr_zz` |

⚠ **So both FAIL classes are shown to fire and the clean tree is shown to pass** — the two halves of
`engine/test_interior.py@«늘 발화하면 상수다»`. **And the timing is the surprise**: `check.sh`'s comment
still says this check costs 77 s, while **three** runs today landed at **136, 141 and 136.22 s** (the
last by the audit seat). ⚠ *Three measurements in the same place is not a machine having a bad night —
**the comment is stale.** The log is not the cause: with it off the run took 5 s **longer**. The 77 s
dates from the 09-06 reordering, and the workload has grown since — the check now runs **14 recipes over
35 computed nodes** on every sample body. Not adjusted here; the candidate cause is recorded instead of
a guess about the machine.*

⚠ **And ⓒ was not run as registered.** It asked for `ce7aff2d^`, where C37 was live; reaching it means
grafting today's `state.py` and checker onto that tree, which is a build of its own. **What stands in its
place is stronger in one way and weaker in another**: stronger because class ① fires on **today's** tree,
in three nodes, so the signature is demonstrated on live code rather than on a reconstruction; weaker
because the historical case itself is still unverified by this instrument. **Recorded as not run, with
the substitute named.**

#### B2 2026-09-09 — the check was standing behind two early exits, and one claim in its commit was too wide

⚠ **The lookup check sat *after* `check_contracts`'s two early exits** — `res is None` (no sample body
produced a `Result` for the node) and `not res.applicable` (every sample out of domain). **The lookup log
does not depend on either**, so a typo in a key whose absence stops the node from running at all would
have been invisible: the node would be skipped before the three sets were ever compared. **Moved above
both**, with the reason written at the call site.

**After the move, the tree still passes** — `rc=0`, 1 182 lookups compared, class ③ unchanged at 8 nodes
· 8 keys · 13 pairs.

⚠ **And one sentence in `446a6366`'s message was wider than the evidence.** It said *"both FAIL classes
are shown to fire"*; what had been shown was **class ② on one node** (`dynamo_rocky`) and **class ① by
removing one pair from the baseline**. The corrected record, now with four runs behind it:

| class | fired on | checker | run |
|---|---|---|---|
| ② | `dynamo_rocky` — `age_gyr` → `age_gyr_zz` | **pre-move** | this seat, in-tree, `rc=1` |
| ② | `internal_heat_nontidal` — `radiogenic.py`'s `age_gyr` → `age_gyr_zz` | **pre-move** | **audit seat**, real-file harness, `rc=1`, 143.76 s — *and this seat independently, isolated copy, `rc=1`* |
| ① | `dynamo_rocky` — `dynamo_regime`, its pair removed from `CLASS1_KNOWN` | **pre-move** | this seat, `rc=1` |
| ② | `internal_heat_nontidal`, same typo | **post-move** | this seat, isolated copy, **`rc=1`, 143 s** |
| ② | `dynamo_rocky`, same typo | **post-move** | this seat, isolated copy, **`rc=1`, 141 s** |
| — | the clean tree · the clean copy | **post-move** | `rc=0`, 1 182 lookups, class ③ unchanged · `rc=0`, 143 s, **14 contracts** |

**Read as three statements, because they have three different supports:**

- **Pre-move, class ② is reproduced on two nodes by two seats** — `dynamo_rocky` here, `internal_heat_nontidal`
  by the audit seat and again here.
- **Post-move, the same two nodes fire — but all three of those runs are this seat's.** No second seat has
  re-run them on the moved checker.
- **The audit seat's post-move leg is a different fault**: the `core_initial_temperature_zz` pair below,
  which is the one that distinguishes the two checkers at all.

**And class ① fired on one node.** ⚠ *The sentence this replaces said "two nodes by two seats, before and
after the move", which stretched the two-seat part across the post-move rows — **an overclaim written
inside the paragraph that exists to correct an overclaim**, and caught by the audit seat rather than by
this one.* ⚠ *The move widened coverage without disturbing what already worked: the same two typos fire on
the moved checker, and the clean copy still passes at 14 contracts.*

⚠ **An operating fact that cost the audit seat a run, worth more than the run.** Its first probe returned
`rc=0` and looked like a hole in the checker. It was the **harness**: six engine modules do
`sys.path.insert(0, Path(__file__).resolve().parent)`, and in a scratch tree made of **symlinks** that
`resolve()` walks back to the repository's own directory — so `registry`'s first import pulled the
**original** `radiogenic`, not the edited one, and the planted typo was never in the run. **A symlinked
scratch tree silently executes the originals.** An isolated tree must hold **real `.py` files**; this
seat's probes were `rsync` copies with `find -type l` returning nothing, which is why they were valid.

⚠ **And this seat lost five hours to the same family, in its own waiter.** The shell that was to launch
the post-move probes waited on `until ! pgrep -f "check_contracts"; do sleep …` — **and its own command
line contains that string**, so the loop matched itself, never exited, and the probes it was guarding
never started. Nothing said so; the tree simply sat with four uncommitted files until the directing seat
asked. `engine/tools/README.md@«A gate is a process group»` already holds this family — *a process
listing is an instant, not a state* — and the new member is: **a waiter that greps for a name is itself
a process whose command line contains that name.**

⚠ **And today's two isolation failures are one shape.** The symlinked scratch tree let `.resolve()` walk
back to the original directory; the waiting shell matched its own command line. **In both, the device
built to isolate something contained the thing it was isolating from** — a tree of links pointing at the
source it was meant to stand apart from, and a process whose text is the pattern it was meant to watch
from outside. **Neither failed loudly; both simply reported the state of the thing they were supposed to
be separate from.**

#### The pair of runs that is the actual evidence for B2

⚠ **The move's justification is not a line of code; it is two runs of the same planted fault.** The audit
seat planted `core_initial_temperature` → `core_initial_temperature_zz` in `core_history.py` — a key
whose absence puts **every sample body out of domain**, which is precisely the case the two early exits
swallowed:

| checker | result |
|---|---|
| **`446a6366`**, block after the exits | **`rc=0`** — and `[PASS] 계약 대조 **13**건` |
| **`b9f01961`**, block before them | **`rc=1`** — `[FAIL] core_thermal_history … core_initial_temperature_zz` |

with the `[건너뜀]` lines identical in both. ⚠ **So this repair is a guard rather than a regression fix:
no sample body exercises the hole today.** And the sharpest part is the count — **13 against 14**. **The
hole was never silent**: the contract check had been reporting one contract fewer, and **nobody read the
number.** A skipped node is a subtraction from a total that is printed on every gate run.

### C45 (d) 2026-09-09 — the fifth shape gets a detector, pre-registered before it is built

⚠ **This section is committed before the code.** C45 (c) named a shape the instrument cannot see and
C50 (b) hit it twice: **a key whose lookups all missed, appearing later in `Result.inputs` with a real
number.** Class ① tests `inputs[key] is None`, so a *plausible value* written from a constant or from the
solver's own working is invisible to it — worse than C37, which at least leaves a `None` a reader might
notice.

**The rule, stated before the measurement:** for each node, take the keys whose lookups were asked and
**missed on every sample body**, then look at that body's `Result.inputs`. A key that is present there
with a value that is not `None` is **class ④**.

#### The one exception, named rather than listed

⚠ **An inverse solve legitimately reports what it inferred, under the name of the thing it inferred.**
`interior.py` does this at four places and `test_interior` reads it that way — `res.regime` names the
axis and `res.inputs[axis]` holds the value read back. 170 B mistook that convention for a defect,
removed one of the four, and `gate207` failed on it (C50 (b), correction 170 C).

So the exception is **on the regime, not on the key**: a `Result` whose `regime` begins with `inferred_`
is an inversion and may report its axes. ⚠ **It is not an allowlist** — no key name is exempted anywhere,
the exception is a property the result declares about itself, and those hits are still **printed**, on
their own line, so that nothing disappears. A future inversion gets the same treatment without an edit,
and a non-inversion writing the same key is still caught.

#### Registered expectations, before running it

1. **Unexplained class ④ = 0.** The only instance anyone has found — `porosity_cap` — was removed in
   170 B, and nothing else is known.
2. **The convention line fires on `interior_layers`, or on nothing.** The four writes all live in that
   recipe's inversion branches. ⚠ Whether any *roster* body takes one of those branches is **not known
   to this seat before the measurement**, so the count is deliberately not predicted — only the node is.
3. ⚠ **If (1) is wrong, that is the finding**, and the instance is reported before it is repaired: the
   count is the point of the item, not a number to get to zero.

The baseline goes into `check_contracts.py` beside the others, with the reason, and moves only with one.

#### C45 (d) built 2026-09-09 — both registered expectations failed, and the shape resists a clean test

**Registered expectation 1 — «unexplained class ④ = 0» — failed: it measures 12.**
**Registered expectation 2 — «the convention line fires on `interior_layers`, or on nothing» — also
failed**, in the second way: it fires on nothing, because no roster body takes an inversion branch. Both
registrations are left as written.

⚠ **The rule as registered could not be shipped, and finding that out was the work.** «Missed lookup,
non-`None` in the evidence» fires on **every declared default**: the recipe records the value it used, and
for a declared-optional key that value *is* the default. Refining it to «different from the call-site
default» still fired, because a recipe's own **parameter default** is a second legitimate layer
(`ladder(..., ice_mass_fraction: float = 0.0)`). Accepting both layers left **12**, all of one kind:
`interior_layers` records `0.0` for `gas_mass_fraction` and `ice_mass_fraction` on all six sample bodies,
where both declared defaults are `None` and the recipe normalises «absent» to zero internally.

**So a number in the evidence has at least three honest origins** — the call-site default, the callee's
signature default, and the recipe's own normalisation — and only a fourth is the defect. ⚠ **What
separates them is not a property of the value; it is whether the source is one the contract names.** That
is why the shape stayed invisible to C45 (b)'s `is None` test and why it cannot be closed by comparing
numbers.

**What was built, and what it is worth.** The detector ships with the two-layer rule, printed with the
node, the key, the body, the value and the accepted defaults, plus separate lines for inversion-convention
hits and for keys whose defaults are not literals. ⚠ **A unit assertion aims at that verdict** — a value
against a declared default of `None` is not explained, which is what `porosity_cap` recording `P_LAB_MAX`
was — **but it is not proven end to end**: no roster body takes an inversion branch, so re-planting the
original write changes nothing the pipeline can show (audit seat, measured: 0). The detector is proven at
the predicate and unproven at the body until a body exercises that branch.

⚠ **171 C closed the 12 by fixing the contract, not the count.** Of the two ways to close the
disagreement — write the normalisation into the contract, or keep the raw `None` in the evidence — the
second can move an output, so the first was taken. The two `Declared-optional` entries now *say* it:
*«absent is recorded as `0.0`, because the recipe normalises it internally»*, and the parser reads that
sentence. ⚠ **This is not an allowlist and the difference is testable**: a normalisation the contract does
not state is still class ④, and a new key doing the same thing is caught until someone writes the
sentence. The baseline is **0** and two rows in `test_check_refs` hold the parser to reading it.

**What is still not decided** is the deeper question this item exposed — a number in the evidence has
three honest origins and the contract can only name them one sentence at a time. Nothing forces a recipe
to declare its normalisations; this brief made it *possible* to, and made the omission visible.

#### C50 (b) addendum, 172 (a) — the asymmetry behind the zero is now a number

Class ③ asks whether **any** sample body supplies a key, so one body's declaration empties the cell for
all of them. That was written beside the baseline as a sentence; it is now measured. `check_contracts`
records **per-body supply** — for a `Needs` key that some in-domain body supplies and another does not —
and prints it as a record, never a verdict, because «one body declares it and another does not» can be
correct.

**First count: 13.** Two of them are open items wearing a number for the first time:

* `core_thermal_history.core_material` — **supplied by Earth, undeclared on Mars**. That is C50 (b) row
  5's owner-pending cell, and class ③ reads **0**.
* `core_state.core_cmb_temperature` — **supplied by Earth, undeclared on Mars and Pandora**. ⚠ That is
  **C54's root**: Mars's `conductor_phase` is `undecided` because this declaration exists for Earth only,
  and the lid axis therefore never decides anything on Mars.

⚠ **Only bodies the node actually answered are counted.** Stars and brown dwarfs walk the same lookups —
the domain gate sits behind the probe — and not declaring a rocky input is right for them; counting those
would bury the real asymmetry under out-of-domain noise.

### C45 (e) 2026-09-09 — a fixture body, pre-registered before it is added

⚠ **This section is committed before the body file.** Every contract-check sample today is a *published*
body, and none of them takes `interior_layers`' **inversion branch** — which is why C45 (d)'s
inversion-convention line reads 0 and why re-planting the original class-④ instance changes nothing the
pipeline can show (172 (a)'s addendum). The instrument's range stops short of a branch the engine has.

Brief 173 adds **one fixture body, Dante**, from `test_interior`'s porosity roster (1.552 × 10²¹ kg,
521 km), carrying a mandatory label: *engine fixture body — values copied from the `test_interior`
fixture; the mass–radius pair is an owner-open question (the Dante·Hades radius), not a board value; no
board or `phase4` wiring.* ⚠ **It is not a claim about Dante.** It is a body-shaped input that makes the
checker walk a branch, and the label says so in the file.

#### The four baselines that must move, predicted before the run

| baseline | today | predicted |
|---|---|---|
| inversion-convention line (C45 (d)) | **0** | ⚠ **≥ 1** — this is the point of the brief. Direct call gives `regime = inferred_initial_porosity` with φ₀ = 0.3890625 |
| class ④ unexplained | **0** | **0** — the inversion write is explained *by the regime*, and if it is not, the exception is wrong and that is the finding |
| class ③ | **(0, 0, 0)** | **(0, 0, 0)** — a new body can only *add* supply, never remove it, so this one cannot move by construction |
| per-body supply (172 (a)) | **13** | ⚠ **rises** — the fixture declares almost nothing, so every key Earth supplies and it does not becomes a row. **The number is not predicted**, only the direction; predicting it would be arithmetic on a run not yet made |

**And a fifth expectation, the one that would stop the brief:** the six existing bodies' outputs are
**bit-identical**. A sample body is an input to the checker, not to them; if any answer moves, the file
did something a body file must not.

⚠ **What this must not do.** No board row, no `phase4` wiring, no emit. And the fixture's numbers are
**not** to be cited anywhere as Dante's properties — the mass–radius pair is exactly the question the
owner has open, and copying it into a body file does not settle it.

#### C45 (e) built 2026-09-09 — the fixture lands, and the branch it was for is unreachable from the node

| baseline | predicted | measured |
|---|---|---|
| inversion-convention line | **≥ 1** | ⚠ **0 — the prediction failed** |
| class ④ unexplained | 0 | **0** ✓ |
| class ③ | (0, 0, 0) | **(0, 0, 0)** ✓ |
| per-body supply | rises, number not predicted | **13 → 20** ✓ |
| the six existing bodies | bit-identical | ⚠ **0 values moved**, across every node of every body ✓ |

⚠ **The main prediction failed for a structural reason, and that is the brief's finding.** The fixture
does reach `interior_layers` — lookups go **1215 → 1399** — but it lands on `integrated_fe_prem_silicate`,
the forward path, on both attempts. The first attempt was my own fault: I declared `composition_intent:
earth_like`, whose preset supplies a core mass fraction, leaving nothing to infer. Removing it — which is
also **restoring the copy**, since `test_interior`'s roster calls `infer_composition` with mass, radius,
ice-permission and tidal heating and nothing else — changed the branch not at all.

**The reason is one line in the adapter**: `composition=state.get("composition_intent", "earth_like")` in `interior.py` — ⚠ **that fallback **was** there when this was written and was removed on 2026-09-20 (C57 (c)); the call now reads `composition=state.get("composition_intent"),`.** *The phrase is quoted as plain code, not as an anchor: the line it named no longer exists.*
The node **always** hands `solve` a composition, falling back to `earth_like`, so the recipe always
integrates forward. ⚠ **`infer_composition` is not reachable from `interior_layers` under any body
declaration** — only a direct call reaches it, which is what `test_interior` does.

**So C45 (d)'s inversion exception guards a path the checker cannot make the node take.** It is not
wrong; it is *unexercised through the node*, and no body file can exercise it. That is a different
sentence from «no roster body happens to take that branch», which is what 172 (a) recorded, and it means
adding bodies will never close it. Whether the node should be able to infer a composition is a question
about the recipe, not about the checker, and it is not decided here.

⚠ **The fixture is kept**, for what it *did* do rather than what it was for: the checker's samples were
six published bodies, and a body that declares almost nothing is the only way the per-body-supply count
sees an empty declaration at all — seven of its twenty rows are the fixture's. It widened the reach by 184
lookups and holds the six published bodies bit-identical.

⚠ **The recommendation that produced this brief predicted three things and got two wrong** — that the
inversion line would fire, and that a body file could make it fire — and both predictions were made
before anyone read the call graph. The audit seat recorded that as its thirteenth correction of the day;
**the directing seat passed the same prediction through without checking it, and the work seat built on
it**. The failure is not that a prediction was wrong. It is that three seats agreed about a code path
none of them had read, and the reading took one `grep`.

⚠ **And the inversion convention's consumers are named now**, since 170 C's record made it sound like a
property of the chain: `test_interior` and `rocky_roster` call the inverse solvers directly. **The chain
does not.** The convention is real and its scope is those two callers — see C57.

### C54 (b) 2026-09-09 — Mars gets a declared core-side CMB temperature, pre-registered before the run

⚠ **Committed before the declaration.** 172 (a) measured C54's root: `core_state.core_cmb_temperature` is
supplied by Earth and undeclared on Mars and Pandora, so Mars's `conductor_phase` is `undecided` and the
lid axis in front of it never decides anything. **Owner decision, 2026-09-09: declare the literature band
1900–2100 K for Mars.**

**The band and its source.** Durán+ 2022 ([`2022PEPI..32506851D`](https://ui.adsabs.harvard.edu/abs/2022PEPI..32506851D), held) prints
a CMB temperature of **1900–2100 K** with a potential temperature of 1650–1750 K, *"implying an entirely
liquid core at present"*; Stähler+ 2021 ([`2021Sci...373..443S`](https://ui.adsabs.harvard.edu/abs/2021Sci...373..443S), held) reaches
the same phase from seismology — *"the observation of ScS … rules out a solid outer core"*. ⚠ **The
layered-model family is deliberately outside the band**: Khan+ 2023
([`2023Natur.622..718K`](https://ui.adsabs.harvard.edu/abs/2023Natur.622..718K), held) puts a fully molten silicate layer over a
smaller, denser core, which is *a different choice of mantle model*, not a different measurement of the
same one. Mixing the two would give a width that is a modelling disagreement wearing the shape of an
uncertainty.

⚠ **One judgement is mine and it is flagged, not hidden.** The engine's input is a **scalar** and this
band has two ends. `cmb_flux`'s own note says a declared core-side temperature acts as a **lower bound**
on `Q_CMB`, so the band's **low end, 1900 K**, is what keeps that direction honest. **Both ends are
measured and reported**; if they give the same verdicts the choice does not matter today, and if they do
not, the owner has a real decision instead of my quiet one.

#### What is predicted, before running it

1. `conductor_phase` **undecided → decided**. Which value is *not* predicted with confidence, and here is
   why: Mars's melting comparison today already reads `cmb_melt_temperature` **2714.25 K** against a
   fallback `core_cmb_temperature_used` of **2346.73 K** — a margin of **−367.51 K**, i.e. *below*
   melting. Declaring **1900 K** moves the input **further below** that curve. ⚠ **So the arithmetic
   points at `solid`, while every held observation says liquid.**
2. ⚠ **If it reads `solid`, that is the finding and nothing is tuned.** It would mean our melting-curve
   comparison disagrees with the Mars literature, and the disagreement gets an item, not a patch.
3. **The lid axis decides for the first time, or it does not get the chance.** If the phase reads
   `liquid`, Mars is `stagnant` → `DEAD_LID`; if it reads `solid`, the core branch fires first and the lid
   axis stays untested — which would leave C54 open on a *different* leg than the one being closed.
4. **Earth and Pandora bit-identical**, every node, every value.
5. **C20's endpoint is 3763 K for the same body.** That is ~1700 K above this band, and it is **not
   reconciled here** — listed as a candidate instead, because one of the two is wrong about Mars and
   choosing which is not a declaration.

#### C54 (b) built 2026-09-09 — the lid axis decides on Mars, and my own end-choice reasoning lost to the measurement

| | 1900 K (low end) | 2000 K (midpoint) | 2100 K (high end) |
|---|---|---|---|
| `conductor_phase` | ⚠ `liquid_outer_solid_inner` | **`liquid`** | `liquid` |
| CMB margin above melting | +116.76 K | +216.76 K | +316.76 K |
| `cmb_heat_flux` | ⚠ **refuses by name** — *«핵 쪽 1900 K 가 맨틀 단열선 밑 1910 K 이하 — 초단열 점프가 없다»* | computes | computes |
| `dynamo_rocky` | `dead (stagnant lid, declared)` · ℳ 0 · B_eq 0 | **same** | **same** |

**Prediction 3 holds: the lid axis decides on Mars for the first time**, and it decides the same way at
every point of the band. Prediction 4 holds: Earth, Pandora and the rest are **bit-identical, 0 values
moved**; Mars gains 63 values where its core nodes previously produced none.

⚠ **Predictions 1 and 2 were wrong, and the way they were wrong is the finding.** I reasoned that
declaring 1900 K would push Mars *further below* its melting curve toward `solid`, because the fallback
comparison read 2346.73 K against a melt temperature of 2714.25 K. Both numbers move when the
declaration arrives — the melt temperature is **1783.24 K** once the interior solves on the declared
temperature — so the margin is **positive** at every point of the band and the core reads liquid, which
is what the literature says. The arithmetic I did was on two numbers that do not survive the change I was
predicting.

⚠ **And the end-choice reasoning lost too.** The pre-registration argued for the **low end** because
`cmb_flux`'s own note says a declared `T_c` acts as a lower bound on `Q_CMB`. Measured, the low end is the
only point in the owner's band that (i) infers an **inner core no held paper reports** — Helffrich 2017
([`2017PEPS....4...24H`](https://ui.adsabs.harvard.edu/abs/2017PEPS....4...24H)) writes of Mars's
*"probable absence of an inner core"* — and (ii) makes `cmb_heat_flux` **undefined**, because 1900 K sits
below the mantle adiabat's 1910 K. **Keeping a bound's direction is not free: it adds a physical claim.**
So the declaration is the band's **midpoint, 2000 K** — the point that leans on neither end and contradicts
nothing held. ⚠ **The owner confirmed that midpoint as the decision** once both ends' physics was
measured and reported (2026-09-09 23:4x); it was written here first as this seat's reversible choice, and
the record keeps that order rather than back-dating it.

⚠ **What is not closed.** C20's endpoint for the same body is **3763 K**, about 1700 K above this band.
Both cannot be right about Mars, and choosing between them is not a declaration — **C58**.

### C55 — a liquid Fe–S core material, because neither `fe_prem` nor `fe_eps` can be Mars's core — **pre-registered 2026-09-09, before the build** (drafted by the parallel seat as P13)

⚠ **This section is committed before the change.** P12 measured that our two iron materials give a local
density of 7.6–8.2 (`fe_prem`) or 9.0–9.6 × 10³ kg m⁻³ (`fe_eps`) across Mars's core pressures (19–40 GPa),
while every printed Mars **mean** core density is 5.7–6.9 × 10³ kg m⁻³. The owner decided (2026-09-09,
relayed by the directing seat): **build a new Fe–S material.** This registers the EOS form, the printed
parameters it may use, the composition choices the owner still has to make, the reproduction anchors, the
judgement anchor, and three things the build must not do. **Nothing here is chosen by a seat.** Every
source carries a bibcode, an ADS link, and whether the full text is held in `docs/phase3/_papers`.

#### Where the new material would sit, counted before the design

| where | what it does today | moves? |
|---|---|---|
| `engine/eos.py@«FE_PREM = Material(»` (1793) · `«FE_EPS = Material(»` (1810) | the two iron `Material`s; `Phase(name, form, rho0, k0, k0p, p_max, ref, …, melt, melt_scale, melt_ref, join, fit_state, join_note)` | ⚠ **untouched** — a third `Material` is *added* beside them |
| `engine/eos.py@«MATERIALS: dict[str, Material»` (2666) | the registry `core_material` keys into | one new key |
| `engine/eos.py@«def iron_fes_eutectic_t_melt(»` (1520) | Mori+ 2017 Fe–Fe₃S eutectic, **bound only**, 21–350 GPa, `IRON_FES_GAP_REASON` below 21 GPa | ⚠ **untouched** — becomes the new material's melting *bound*, not refit |
| `engine/core_state.py@«material = MATERIALS.get(core_material)»` (255) | refuses a material with no melting curve (`melt_free_phases()`) | the new material must carry a `melt` so this line does not refuse it |
| `engine/interior.py@«COMPOSITIONS: dict[str, tuple[float, float, float, str]] = {»` (82) | presets → `fe_prem` / `fe_eps` | ⚠ **untouched**; Mars passes `core_material` per body, the preset table does not change |
| `engine/bodies/mars.yaml` | today inherits `fe_prem` | the one declaration that changes |

**Non-consumers, which is the useful half.** Earth (`earth.yaml`) keeps `fe_prem`; Pandora keeps whatever
it declares today. `dynamo_rocky` reads `conductor_phase`, not the material — **C54 (Mars
`conductor_phase`) is a separate item and this brief does not touch it** (see *must not*, 3).

#### (1) EOS form and the printed parameters

**Our slot.** `eos.Phase` takes `form ∈ {bm2, bme4?, vinet, polytrope}` with `rho0, k0, k0p` (+ `k0pp` for
BME4), thermal terms `alpha_k, alpha_k_dt, c_v_ref, t_ref, t_ref_kind`, and `fit_state`. `fe_prem` is
`bm2` with `fit_state="liquid"`; `fe_eps` is `vinet`, `"solid"`. So a liquid Fe–S phase fits the existing
slot **only as a (ρ₀, K₀, K₀′) triple at a reference state plus a melting curve** — the two printed sources
below give exactly that, at two different reference states.

| source | what is printed | fits the slot? | held |
|---|---|---|---|
| **Huang, Li, Khan, Sossi, Giardini, Murakami 2023**, *GRL* 50, e2022GL102271 — [`2023GeoRL..5002271H`](https://ui.adsabs.harvard.edu/abs/2023GeoRL..5002271H) | AIMD liquid Fe–X (X = Ni, S, C, O, H) at two Mars-core anchors. **Table 1 (pure liquid Fe):** at 19 GPa/2100 K ρ = 8083 ± 1 kg m⁻³, K_T = 156 ± 2 GPa, dK_T/dT = −0.026 ± 0.006 GPa K⁻¹, K_S = 218 ± 3, α = 6.99 × 10⁻⁵ K⁻¹, C_V = 494 J kg⁻¹ K⁻¹, γ = 2.74; at 35 GPa/2400 K ρ = 8640 ± 1, K_T = 215 ± 4, K_S = 288 ± 5, α = 5.31 × 10⁻⁵, γ = 2.66. The Fe–X mixing model: "second-order BM EoS, [K₀′] equals 4" about each anchor; ∂ρ/∂x_i and ∂K_T/∂x_i "constants for Ni, O, C and H, except for S because of its non-linear behavior (**Table S5** in Supporting Information S1)". Printed Fe–S points: Fig. 3 caption "Fe-S … 6.7 g cm⁻³ … at 19 GPa" (2100 K, composition in Fig. 2 only); text: "a binary core would require at least 30 mol% (∼20 wt%) S estimated from the data at 19 GPa, or 40 mol% (∼30 wt%) S estimated from those at 35 GPa" to reach the ∼2 g cm⁻³ deficit; target local densities "5.8–6.2 g cm⁻³ [19 GPa] and 6.3–6.8 g cm⁻³ [35 GPa]" (Bagheri+ 2019, Khan+ 2018). | **Yes for the pure-Fe end member** (BM2 about 19 GPa with K₀′ = 4 is our `bm2` form exactly, with `rho0`/`k0` re-referenced to 19 GPa, not 0 GPa — the slot's `p_min` would have to say so). **Fe–S itself: the S derivative is in Table S5, which is in the SI we do not hold** — the numbers are figure-read (Fig. 2) until the SI is fetched. | held (ETH copy of the cc-by-nc VoR; **SI not held**) |
| **Xu, Morard, Boulard, Rivoldini, Nishida, Antonangeli 2021**, *EPSL* 563, 116884 — [`2021E&PSL.56316884X`](https://ui.adsabs.harvard.edu/abs/2021E&PSL.56316884X) | Experimental liquid Fe–S density 4.7–8.4 GPa, 1280–2250 K, 8.4–51.2 at% S (**Table 1, 37 points**, error 220–270 kg m⁻³). Mixing rule, verbatim: "the relation K₀ = K_Fe^(1−X_S) ∗ K_S^(X_S), assuming an exponential dependence of the bulk modulus of liquid Fe-S alloys with S content, and with **K_Fe = 76 GPa and K_S = 1.6 GPa**" (isothermal, ambient pressure, 1900 K); "K′ = K′_Fe + X_S · 3, with **K′_Fe = 6.5** (Morard et al., 2018)"; densities rescaled with a Murnaghan form (their eq. 3); thermodynamic model = asymmetric Margules non-ideal Fe–FeS solution on top of a pure-Fe EOS (Komabayashi 2014 / Dorogokupets+ 2017 / Wagle & Steinle-Neumann 2019), "EOS parameters and Margules coefficients … given in **Table S1**". | **Partly.** (K₀, K′) at 1 bar/1900 K vs S is a Murnaghan-type pair, which our `bm2` (K₀′ fixed at 4) cannot carry — it needs `bme4`/`vinet` or a new `murnaghan` form. ρ₀(X_S) at 1 bar/1900 K is not printed in the main text (it is in Table S1, **SI not held**). The Margules excess volume has no slot in `eos.Phase` at all. | held (OSTI accepted MS; **SI not held**) |
| Morard+ 2018, *Am. Min.* 103, 1770 — [`2018AmMin.103.1770M`](https://ui.adsabs.harvard.edu/abs/2018AmMin.103.1770M) | the Fe–FeS liquid "tool box" Xu 2021's K′_Fe = 6.5 comes from | needed to cite K′ | abstract only (B21) |
| Nishida+ 2020, *Nat. Commun.* 11, 1954 — [`2020NatCo..11.1954N`](https://ui.adsabs.harvard.edu/abs/2020NatCo..11.1954N) | V_P of liquid Fe, Fe₈₀S₂₀, Fe₅₇S₄₃ to 20 GPa; adiabatic BM3 fit extrapolated to ~40 GPa; "V_P of liquid iron is least sensitive to its sulfur concentration in the Mars' whole core pressure range"; reduction "less than 0.3 % per atomic % S at maximum (between Fe₈₀S₂₀ and Fe₅₇S₄₃ at 20 GPa)". Fit parameters in Supplementary. | a **velocity check**, not a density source | held (**SI not held**) |
| Kuwayama+ 2020, *PRL* 124, 165701 — [`2020PhRvL.124p5701K`](https://ui.adsabs.harvard.edu/abs/2020PhRvL.124p5701K) | liquid-Fe thermal EOS to 116 GPa/4350 K (Huang 2023's benchmark: experimental 7.7 g cm⁻³ at 20 GPa/3000 K vs their 8.3 before correction) | pure-Fe end member alternative | abstract only (no OA) |
| Sanloup+ 2000, *GRL* 27, 811 — [`2000GeoRL..27..811S`](https://ui.adsabs.harvard.edu/abs/2000GeoRL..27..811S) | liquid Fe–S density 1.5–6.2 GPa, 1500–1780 K; "decreases the bulk incompressibility by −2.5 GPa per 1 weight% of S" | low-P cross-check | abstract only (B22) |
| Mori+ 2017 (already in `eos.py` as `MORI_FES_EUTECTIC`) | Fe–Fe₃S eutectic T(P), 21–350 GPa | the melting **bound** the new material cites | (as cited in eos.py) |

⚠ **The honest statement of the slot problem:** Huang 2023 gives a BM2 about a *high-pressure* reference
(19 GPa), Xu 2021 gives a Murnaghan-type pair about *1 bar*. Our `Phase` has one `rho0, k0, k0p` at "zero
pressure" and a `form`. **Which of the two the build adopts is an owner/work-seat design choice, listed
here as two candidates, not chosen:**
- **(A) Huang-anchored**: `form="bm2"`, reference re-based at 19 GPa (`p_min` ≈ 19 GPa, so the material is
  *refused* below the CMB pressure it was fit at), ρ₀ and K₀ from Table 1 shifted by the S derivative of
  Table S5 (SI needed) or figure-read from Fig. 2 (figure-read grade until then).
- **(B) Xu-anchored**: a new `form` (Murnaghan with K′ = 6.5 + 3 X_S) or `vinet` with the exponential
  K₀(X_S) rule, ρ₀(X_S) from Table S1 (SI needed) or from the 7 GPa-corrected Table 1 column by
  extrapolation (which would be *our* fit, not theirs — and the standing rule says the paper's printed
  arithmetic wins over ours).

`fit_state = "liquid"` in both; `melt = "iron_fes_eutectic"` (Mori 2017 bound) in both; `melt_scale` is
**not** used (the depression is the eutectic itself, not a 20 % factor).

#### (2) The composition choices — owner's, listed and not chosen

**Sulfur, wt%** (each is a printed value, source and grade as in P12):

| S wt% | source | note |
|---|---|---|
| ≥ ~5 | Williams & Nimmo 2004 [`2004Geo....32...97W`](https://ui.adsabs.harvard.edu/abs/2004Geo....32...97W), abstract only | floor from "entirely liquid" thermal history |
| ≤ 7 (+5.2 O, 0.9 H) | Yoshizaki & McDonough 2020 [`2020GeCoA.273..137Y`](https://ui.adsabs.harvard.edu/abs/2020GeCoA.273..137Y), held | volatility-trend model; mean core density 6910 |
| 10–15 (+<5 O, <1 C, H) | Stähler+ 2021 [`2021Sci...373..443S`](https://ui.adsabs.harvard.edu/abs/2021Sci...373..443S), held | "preliminary observation"; Fe–S alone needs >25 |
| 13.5 ± 3.5 | Steenstra & van Westrenen 2018 [`2018Icar..315...69S`](https://ui.adsabs.harvard.edu/abs/2018Icar..315...69S), abstract only | chondritic building blocks |
| 14 | Dreibus & Wänke (via Bertka & Fei 1998 [`1998E&PSL.157...79B`](https://ui.adsabs.harvard.edu/abs/1998E&PSL.157...79B)), abstract only | the classic model core |
| 15 ± 2 (+3 ± 1 O, 1 ± 1 C) | Samuel+ 2023 [`2023Natur.622..712S`](https://ui.adsabs.harvard.edu/abs/2023Natur.622..712S), held | basal-molten-layer model; also "17 S + 2.9 O" |
| 15.4–16.5 (+~3 O, ~1.3 C, ~0.5 H; total 20–22) | Irving+ 2023 [`2023PNAS..12017090I`](https://ui.adsabs.harvard.edu/abs/2023PNAS..12017090I), held | SKS-informed, homogeneous mantle |
| 16 ± 2 | Rivoldini+ 2011 [`2011Icar..213..451R`](https://ui.adsabs.harvard.edu/abs/2011Icar..213..451R), abstract only | geodesy |
| 18–19 | Brennan+ 2020 [`2020E&PSL.53015923B`](https://ui.adsabs.harvard.edu/abs/2020E&PSL.53015923B), held | core-formation model; EH upper limit 21 |
| ≥ ~20 (30 mol%) at 19 GPa / ≥ ~30 (40 mol%) at 35 GPa | Huang+ 2023 (held) | what an **Fe–S binary alone** needs to hit the seismic density |
| 21 | Brennan+ 2020 (held) | EH-chondrite upper limit |

#### The two owner decisions, taken 2026-09-10 after the table above

⚠ **Recorded here, above the candidates, so that what was open and what was decided stay separable.**

1. **Sulphur: the band 13–19 wt%, not a point.** It is the union of the InSight-era estimates in the
   table (Stähler 10–15, Steenstra 13.5 ± 3.5, Dreibus–Wänke 14, Samuel 15 ± 2, Irving 15.4–16.5,
   Rivoldini 16 ± 2, Brennan 18–19), and **the engine emits both ends** rather than a chosen middle —
   the same shape every other band in this file has. ⚠ **No point is elected**, so any single-number
   answer derived from it is a defect, not a rounding.
2. **Binary Fe–S first (candidate B, Xu 2021's printed rule); multi-component waits for the SI.** The
   owner is fetching the supplementary tables now; until they arrive, a multi-component material would
   have to be built on figure-reads or on our own extrapolation, and the standing rule is that a paper's
   printed arithmetic wins over ours.

⚠ **What the second decision does not settle** is the disagreement recorded just below: several held
sources say S alone cannot reach the seismic density (Stähler's *"surpass 25 wt%"*, Huang's 20–30 wt%
requirement). **Building the binary first is a decision about order, not about sufficiency** — and the
verdict cell is where that gets tested, on radius 1820–1870 km and density 6–6.2 g cm⁻³.

**Whether S is enough** — the second choice, with the printed reasons on both sides:
- *"S alone does not match"*: Stähler 2021 ("sulfur contents surpass 25 wt%, … above … EH chondrites");
  Khan 2023 [`2023Natur.622..718K`](https://ui.adsabs.harvard.edu/abs/2023Natur.622..718K) (held): "approximately 27 % lighter than pure liquid iron"; "9–15 wt% light elements, chiefly sulfur, carbon, oxygen and hydrogen"; Huang 2023: 40 mol% "serves as the lower bound for the amount of any LE".
- *Fe–S(–O) suffices within cosmochemical bounds*: Samuel 2023 "17 wt% of S and 2.9 wt% of O" (with the
  basal molten layer making the core smaller and denser); Brennan 2020 "less than one weight percent O".
- *Bounds on the others*: O ≤ 4 wt% (Samuel 2023, Steenstra 2018); C ≤ ~1 wt% at 16 wt% S (Samuel), ≤ 0.5 (Brennan); H ≤ 0.15 wt% (Samuel, "experimental constraints").

**Registered as owner-pending, two decisions:** (a) the S value (or a band) from the table; (b) whether
the material is a **binary Fe–S** (both EOS sources support it directly) or an **Fe–S–O(–C–H)** mixture
(only Huang 2023's mixing model supports it, and only with the SI). ⚠ A band (min/max) is the standing
output convention for values of this kind; a single elected S is not required by this brief.

#### (3) Reproduction anchors — printed (P, T, ρ) points the new EOS must pass

**Pure-Fe end member (must pass first, whichever candidate is built):**

| # | P | T | ρ printed | source | pass line |
|---|---|---|---|---|---|
| R1 | 19 GPa | 2100 K | 8083 kg m⁻³ | Huang 2023 Table 1 | ≤ 1 % |
| R2 | 35 GPa | 2400 K | 8640 kg m⁻³ | Huang 2023 Table 1 | ≤ 1 % |
| R3 | 20 GPa | 3000 K | 7.7 g cm⁻³ (experimental, Kuwayama 2020 as quoted by Huang 2023 §3.1) | Huang 2023 text | ≤ 3 % (a quoted figure, not a table row) |

**Fe–S (candidate B, Xu 2021 Table 1 — three points spanning composition, all near 7 GPa so the
pressure lever is short; these test the *mixing rule*, not the compression):**

| # | S at% (wt%) | P | T | ρ printed | pass line |
|---|---|---|---|---|---|
| R4 | 9.1 ± 0.5 (~5.4 wt%) | 6.8 GPa | 1850 K | 6746 kg m⁻³ | ≤ 4 % (their stated error 270 kg m⁻³) |
| R5 | 25.1 ± 0.3 (~16 wt%) | 7.5 GPa | 1600 K | 6211 kg m⁻³ | ≤ 4 % (error 250) |
| R6 | 38.3 ± 0.5 (~26 wt%) | 6.5 GPa | 1280 K | 5619 kg m⁻³ | ≤ 4 % (error 230) |

(wt% from at% by 32.06 S / 55.85 Fe; the paper prints at%.) Two more available for a five-point check:
18.1 at% / 5.6 GPa / 1500 K / 6308; 31.7 at% / 7.1 GPa / 1415 K / 5944.

**Fe–S (candidate A, Huang 2023):** the only printed Fe–S density in the main text is **6.7 g cm⁻³ at
19 GPa / 2100 K (Fig. 3a caption)** with its S content given only graphically; Fig. 2a supplies the
ρ(x_S) curve at both anchors. ⚠ **Figure-read values are registered as figure-read grade**; the SI
(Table S5) turns them into printed derivatives. Until the SI is held, candidate A has **one** printed
Fe–S anchor and cannot meet a three-point line — that is a registered *reason* to fetch the SI first or to
prefer B, not a seat's choice between them.

**Cross-check, not an anchor:** Nishida 2020's V_P of Fe₈₀S₂₀ ≈ V_P of liquid Fe between ~20 and ~40 GPa
(within 0.3 % per at% S). A built EOS whose K_S/ρ at 20–40 GPa puts Fe–S V_P more than a few % below
pure Fe contradicts a held measurement and must say so.

#### (4) The judgement anchor — the third cell, and it has two numbers

InSight's density is a **whole-core mean**, so the pass/fail is not a point evaluation. Registered cell:

> **Solve Mars with the interior solver using the new material and the owner's chosen S (or band). The
> whole-core mean density must land in 5.7–6.65 × 10³ kg m⁻³ AND the core radius in 1830 ± 40 km — both,
> in the same run.**

Sources of the two windows (printed): ⚠ **both axes are Durán+ 2022 since 2026-09-20** — 1820–1870 km and 6.0–6.2 g cm⁻³, the ranges its own abstract prints. Stähler+ 2021 "1830 ± 40 kilometers", "5.7 to 6.3 g cm⁻³" is what Durán calls *previously*, and was the density window in force until that decision (held);
Le Maistre+ 2023 [`2023Natur.619..733L`](https://ui.adsabs.harvard.edu/abs/2023Natur.619..733L) "1,835 ± 55 km", "5,955–6,290 kg m⁻³" (abstract only, B18); Durán+ 2022 [`2022PEPI..32506851D`](https://ui.adsabs.harvard.edu/abs/2022PEPI..32506851D) "1820–1870 km", "6–6.2 g cm⁻³" (held); Khan+ 2023 "1,675 ± 30 km", "6.65 ± 0.1 g cm⁻³" (held; **this is the molten-silicate-layer model — its radius window does *not* overlap Stähler's, so the cell above is the homogeneous-mantle window; if the owner elects the Khan/Samuel layered model the cell becomes 1650–1675 ± 30 km and 6.5–6.65**). The 5.7–6.65 band spans both families on purpose and the radius window does not — ⚠ **registered as the one place this cell can pass on density and fail on radius, which is the point of carrying both.**

Expected outcomes, registered before running:
1. With `fe_prem` (today) the same run gives a mean density **above** 6.9 and a radius **below** 1790 km at
   Mars's mass/MoI — the baseline that shows why the material exists. (Direction only; the number comes
   from the work seat's run and is recorded, not predicted here.)
2. With the new Fe–S at any S in the 10–21 wt% band, the mean density falls into the window; whether the
   radius does depends on the mantle density profile the solver carries, which this brief does not touch.
3. An outcome outside 1–2 is written down as its own kind afterwards and registered then.

#### The registered regression

1. **Earth is bit-identical**: every Earth number that reads `fe_prem` (core_state's ICB check −0.12 σ,
   the C13/C20 cells, the interior anchors) does not move. If one moves, the registry edit touched
   `fe_prem`, and that is the bug.
2. `core_state.run(core_material="<new>")` is **not refused** by the melt-free check (line 256), and its
   `conductor_phase` output for Mars is **not read into anything** by this brief (C54 owns it).
3. Below 21 GPa the new material's melting bound returns the named `IRON_FES_GAP_REASON` refusal, not a
   number — the Mars CMB (~19–24 GPa) straddles that line, and **the refusal at 19 GPa is the expected
   outcome, not a risk**.
4. R1–R2 pass at ≤ 1 %; R4–R6 (if B) pass at ≤ 4 %; the numbers are printed in the test with their sources.

#### What this brief must not do

1. ⚠ **It must not touch `fe_prem` or `fe_eps`** — not their constants, not their `melt_scale`, not their
   comments. Earth's reproduction is the regression.
2. ⚠ **It must not refit the melting bound.** Mori+ 2017's eutectic stays as `MORI_FES_EUTECTIC` with its
   21–350 GPa validity and the declared 10–21 GPa gap. Xu 2021's liquidus model (Margules on
   Komabayashi/Dorogokupets/Wagle) is a *different* curve and is **not** adopted here; if it is ever
   wanted it is its own item with its own registration.
3. ⚠ **It must not decide Mars's `conductor_phase`.** C54 lists that separately (P11); the new material's
   `fit_state="liquid"` describes the *fit*, not a verdict about Mars, exactly as `fe_prem`'s does for Earth.

**Size (estimate for the work seat):** one `Material` (+ one `Phase`, possibly one new `form`), one registry
line, one `mars.yaml` line, one test with R1–R6, one doc paragraph. The SI fetch (Huang Table S5, Xu Table
S1) is the only external dependency and is on the owner request list.

#### Amendment 00:2x, on insertion — three things checked, two changed

⚠ **The 166 lines above are the parallel seat's draft, moved verbatim except where this says otherwise.**

**1. Two edits, both mechanical.** The heading carried its own hand-off instruction — *"for the work seat
to move into `interior-core.md`"* — which contradicts itself once inside that file; it now reads as a
dated pre-registration and names P13 as the draft. And the draft's anchor into `interior.py` aimed at the
bare name `COMPOSITIONS`, which occurs **four times** there and `check_refs` fails as ambiguous; it now
points at the declaration line. **No claim, number or source was touched.** ⚠ *Naming the broken anchor in
its own anchor syntax makes this paragraph a citation too* — that is why the sentence describes it instead
of quoting it, the same trap C33 (b)'s example strings set for the citation counter.

**2. Every anchor was resolved before insertion**, not after: `eos.py@«FE_PREM = Material(»`,
`«FE_EPS = Material(»`, `«MATERIALS: dict[str, Material»`, `«def iron_fes_eutectic_t_melt(»`,
`core_state.py@«material = MATERIALS.get(core_material)»` — one match each.

**3. The two owner-pending cells stay open and are named here so a reader does not have to hunt them:**
the sulphur band, and whether the core is treated as binary Fe–S or multi-component. ⚠ **And the SI
dependency is registered as the draft states it**: candidate (A) cannot reach its three-point pass line
without Huang's Table S5, and candidate (B) needs Xu's Table S1 — **B24 and B25 on the owner's request
list**. Until those arrive, any Fe–S density we could write would be figure-read or our own extrapolation,
and the standing rule is that the paper's printed arithmetic wins over ours.

#### Amendment 2, 2026-09-10 — the verdict cell can be anchored now, and radius is what discriminates

⚠ **Waiting for the supplementary tables is only about the EOS parameters, not about the target.** Durán+
2022's abstract prints a Mars core radius of **1820–1870 km** and a mean core density of **6–6.2 g cm⁻³**,
and it is held — so the verdict cell has printed anchors today.

**Two families, and only one of them can be told apart by radius.**

| family | core radius | mean core density |
|---|---|---|
| layer-free | Stähler 2021 **1830 ± 40 km** · Durán 2022 **1845 ± 25 km** (= 1820–1870) | 5.7–6.3 · 6.0–6.2 |
| layered | Samuel 2023 1650 ± 20 km · Khan 2023 **1675 ± 30 km** | 6.5 · 6.0–6.3 |

⚠ **Density cannot separate them — the two ranges overlap.** Radius can: roughly **1790–1870 km** against
**1630–1705 km**, a gap of about 120 km with nothing in it. **So the verdict cell discriminates on radius,
and density is a pass condition rather than a discriminator**, and the cell must say so or it will read as
though two independent checks were made when there is one.

⚠ **The layer-free family has two independent sources, not three.** Samuel 2023 also prints 1830 ± 40 km,
but that is a *citation of Stähler*, not a third measurement.

**Which family the target uses is inherited, not chosen here.** Brief 174 declared Mars's core-side CMB
temperature from Durán 2022's band, and the reason recorded there — that the layered family is a
different choice of mantle model rather than a different measurement of the same one — applies unchanged
to the radius. **This section takes the layer-free target because 174 already took that family**, and
that inheritance is the whole of the justification; if the owner moves the family, both move together.

#### Amendment 3 — the density row was wrong, and so was the conclusion drawn from it

⚠ **I put a number in the table above that neither source prints.** The layered family's density is
**Samuel 2023 6.5** and **Khan 2023 6.65 ± 0.1 g cm⁻³**, not the *"6.0–6.3"* written there — that range is
what Khan's paper **argues against**, not what it reports. The correct row is `layered … 6.5 · 6.65 ± 0.1`.

⚠ **How it got in is the part worth recording.** The number came from a relayed message and I copied it
instead of opening the source, which was one `grep` away in the parallel seat's own P11 table — the same
file the rest of this section is built from. *Carrying a number from a relay is exactly what this file
keeps finding, and it found me.*

**And the conclusion built on it is withdrawn.** With the real numbers the two families are
**5.7–6.3** (layer-free) against **6.5–6.75** (layered): a gap of about 0.2 g cm⁻³, so **density separates
them too**. *(Khan 2023 prints its uncertainty twice — ± 0.1 in the abstract and body, ± 0.15 once in the
body. The 6.75 upper edge here takes ± 0.1; with ± 0.15 the gap narrows to 0.15 and does not close.)* The sentence above — *"density cannot separate them … density is a pass condition rather than
a discriminator"* — is wrong and is retracted here rather than edited away. **The verdict cell's meaning
is therefore stronger, not weaker**: radius and density are **two independent axes**, and the cell asks
whether they point at the *same* family.

**The density window is narrowed to 5.7–6.3**, the layer-free family, ⚠ inheriting Brief 174's choice
exactly as the radius window does — directing seat's decision, reversible. **The layered family's
6.5–6.75 sits outside both axes**, which is what it means for the two to agree.

#### Amendment 4 — where R7–R9 were registered, and the rule that follows from it

⚠ **R7–R9 are not in this section's original registration** — they were added by the parallel seat to
**P13's Amendment 1** after Huang's supplement arrived, *before* the implementation, and the ledger only
caught up afterwards. The order was right; the record was late. R7's pass line, *"≤ 2.5 % of the NSP–SP
midpoint 6.80 (the paper's own spread)"*, is that amendment's wording and its width comes from the two
values Huang prints (NSP 6.72, SP 6.88), not from anywhere else. **Achieved: 0.07 %.** The implementation
also requires the value to lie *between* those two printed numbers, which is **stricter than what was
registered** — recorded here rather than folded in silently.

⚠ **The rule this exposes.** P-files live in the shared folder, outside git, so a later reader cannot
check what they said when they were cited. **From now on, when this ledger cites a P-file it records that
file's sha256 and byte count at the moment of citing.** For this citation: `P13-c55-fe-s-material-prereg.md`,
sha256 `903413d84a02f8bb…`, 27258 B. ⚠ And the ordering rule: *a P-file amendment is moved into the ledger
before it is implemented*, not after — this one went the other way and the amendment above is the repair.

⚠ **And none of this is why C55 exists.** Every family puts Mars's core density between **5.7 and 6.5**
g cm⁻³, while our two irons give **7.6–8.2** and **9.0–9.6**. The families change the *radius target*;
they do not change the fact that neither of our materials can be Mars's core.

### C55 (b) 2026-09-10 — wiring Mars to the Fe–S material, pre-registered before the run

⚠ **Committed before the implementation.** 178 B transcribed Huang's printed mixing and 179 gave it a
`Phase` through the high-pressure-referenced BM2. This registers what happens when Mars is actually wired
to it, and what must not.

#### The composition conversion, and why it is allowed

The owner's sulphur band is **13–19 wt%**; Huang's derivatives take a **mole fraction**. The conversion is
`c_S = (w/M_S) / (w/M_S + (1−w)/M_Fe)` with **M_Fe = 55.845** and **M_S = 32.06** g/mol:

| band end | wt% S | **c_S** |
|---|---|---|
| low | 13 | **0.206527** |
| high | 19 | **0.290071** |

⚠ **This is our arithmetic and it is allowed** — it is textbook stoichiometry, the one exception the
derived-value rule names, and the label travels with the numbers so a reader can redo it. Nothing about
the *physics* is converted; only the unit the paper's table demands.

#### ⚠ What the reading found before any code was written

**A body-level `core_material` declaration does not move the radius.** The four core nodes read
`core_material` from the state, but `interior_layers` — which is where `core_radius_fraction` and the mean
density come from — takes its core material from the **composition preset**:
`interior.py@«COMPOSITIONS: dict[str, tuple[float, float, float, str]] = {»` supplies `fe_prem` for
`earth_like`, and the adapter hands `solve` a composition, never the body's `core_material`.

**So wiring Mars in the obvious way would change the four core nodes and leave C59's two rows exactly
where they are.** The implementation therefore needs the material to reach `_stack`, and `_stack` looks
its material up in `MATERIALS` by name — which means **registering** it, which the sulphur band forbids
doing at a single point.

**The shape that satisfies both:** register the band's **two ends** as two named materials, not a
midpoint. Both ends emitted is what every other band in this engine does.

#### The four cells to be measured, and the two axes that make them

| | 19 GPa anchor | 35 GPa anchor |
|---|---|---|
| **c_S 0.206527** (13 wt%) | radius · mean core density | radius · mean core density |
| **c_S 0.290071** (19 wt%) | radius · mean core density | radius · mean core density |

⚠ **The anchor axis is not a free choice and not a preference** — 179 measured the two anchors as **2.9 %
apart** when extrapolated onto each other, and Mars's core spans both (19–40 GPa). Each cell is scored
against the verdict windows **radius 1820–1870 km** and **density 5.7–6.3 g cm⁻³**, and ⚠ **whichever
cells pass or fail, no value is adjusted to make them pass.**

#### Predicted, before running

1. **Radius rises from 1667 km toward 1830.** Direction only: the same core mass fraction in a lighter
   material must occupy more volume. **How far is the measurement**, and it is the point of C55.
2. **C59's two recorded disagreements move.** If either comes inside its tolerance, the
   `[기록·해소?]` line must appear — that mechanism was built in 177 for exactly this moment and has
   never fired on a real change.
3. **Earth, Pandora and the rest stay bit-identical.** Mars is the only body wired.
4. ⚠ **Prediction 1 may be right about direction and still fail both windows**, because the core mass
   fraction is `earth_like`'s 0.325 and **is deliberately left undeclared** — C55 tests the *material*,
   and letting a second unknown move at the same time would make the result unattributable.

#### C55 (b) built 2026-09-10 — all four cells refuse, and the reason was already named

| c_S (wt% S) | 19 GPa anchor | 35 GPa anchor |
|---|---|---|
| 0.206527 (13) | ⚠ **refused** | ⚠ **refused** |
| 0.290071 (19) | ⚠ **refused** | ⚠ **refused** |

**All four, with one reason, and it is not this brief's:** `IRON_FES_GAP_REASON` — *the Fe–S melting
between 10 and 21 GPa is covered neither by Mori+ 2017 ([`2017E&PSL.464..135M`](https://ui.adsabs.harvard.edu/abs/2017E%26PSL.464..135M), below its reference point) nor by Buono & Walker
2011*. ⚠ **Mars's core-mantle boundary is 20.65 GPa in this engine**, so the top of its core sits **inside
that gap**, and a material whose melting bound is undefined there cannot be solved.

**So the registered predictions are not resolved, and they are not being called wrong either.**
Prediction 1 (radius rises from 1667 km toward 1830) is **untestable today** — the direction argument
still stands and no number tests it. Prediction 2 (C59's rows move, possibly firing 177's resolution
notice) **does not occur**. Prediction 3 holds, trivially: Mars is **not wired**, so every body is
bit-identical. ⚠ **Mars is deliberately left on `fe_prem`**: declaring the new material would replace the
answers it has with a refusal, and trading answers for a refusal is not what C55 is for.

**What was built and stands.** The band's two ends are registered as materials — `fe_s_13wt_19gpa` and
`fe_s_19wt_19gpa`, ⚠ **with the anchor in the name**, because the two anchors differ by 2.9 % (179) and
any evidence carrying the material name should carry which anchor produced it. The engine's Mars CMB of
20.65 GPa makes the 19 GPa anchor *the nearer one*, and that is recorded as a fact rather than used as a
choice.

⚠ **A second gate caught something the first did not.** `test_eos_joins` (Brief 41's discipline) refused
both new materials because their melting curve had no registered composition: a phase must be able to say
how its **density fit's composition** differs from its **melting curve's**, and `iron_fes_eutectic` was
not in `MELT_CURVE_JOIN` at all — so there was **nowhere to write the difference down**. It is registered
now, and both phases carry the `join_note` saying the density is an arbitrary-`c_S` liquid while the
melting bound is at the fixed eutectic composition.

⚠ **And a limit worth stating plainly, because it looks like a bug and is not:** this material *does*
return a density at 20.65 GPa — the density path never calls the melting curve — but it **cannot say
whether the core is liquid there**. The separation is correct (a density fit and a melting curve are
different measurements, which is the whole of Brief 41's discipline), and it is also a limit: the phase
verdict for Mars's core top stays unavailable while the melting gap stands, even though the structure
solve would have a number.

**What would unblock the cells** is a melting bound between 10 and 21 GPa, which is C55's own recorded
gap and not a modelling choice we may make; the two measured points inside it (Pommier+ 2018, [`2018Icar..306..150P`](https://ui.adsabs.harvard.edu/abs/2018Icar..306..150P)) print a
eutectic *composition* that does not match the curve's, which is exactly why the gap was declared rather
than interpolated.

### C55 (c) 2026-09-10 — the 10–21 GPa melting bound as a bracket, pre-registered before the build

⚠ **Committed before the code.** 178 C's four verdict cells all refused on the Fe–S melting gap between 10
and 21 GPa, and Mars's core-mantle boundary sits at **20.65 GPa**, inside it. The parallel seat's P16
surveyed the window (`P16-fe-s-melting-10-21gpa.md`, sha256 `ea4055ff27e7c986…`, **17952 B** at the moment
of citing). What it found is why this is a **bracket and not a curve**.

#### The window's printed values do not agree

| source | printed | grade |
|---|---|---|
| Andrault+ 2009 ([`2009PEPI..174..181A`](https://ui.adsabs.harvard.edu/abs/2009PEPI..174..181A)) | *"the eutectic temperature increases from **1023 K at 15 GPa** to **1123 K at 20.6 GPa**"* | abstract only |
| Li+ 2001 ([`2001E&PSL.193..509L`](https://ui.adsabs.harvard.edu/abs/2001E&PSL.193..509L)) | phase diagram *"between 7 and 25 GPa and temperatures between **1223 and 1473 K**"* | abstract only |
| Fei+ 2000 ([`2000AmMin..85.1830F`](https://ui.adsabs.harvard.edu/abs/2000AmMin..85.1830F)) | 21 GPa, 950–1400 °C — the **1348 K** our Mori curve is anchored on | abstract only |

⚠ **Two lineages, about 225 K apart at the same pressure**, and Buono & Walker 2015
([`2015M&PS...50..547B`](https://ui.adsabs.harvard.edu/abs/2015M&PS...50..547B)) reads the lower ones as hydrogen contamination.
**This brief takes no side.** ⚠ And a fact that disqualifies a single curve outright: **our own Mori
anchor is not Mori's measurement** — Mori+ 2017 §3.3 takes its 1348 K at 21 GPa *from Fei 2000*, and
Mori's own points start at 34 GPa.

#### What gets built

`iron_fes_eutectic_t_melt` keeps its single value **at and above 21 GPa**. Between **10 and 21 GPa** the
melting bound becomes a **bracket** — the printed low and the printed high — and the consumer compares a
temperature against **both ends**: below both → solid, above both → liquid, **between them → cannot-say**.
That is this engine's band rule applied where the literature disagrees, rather than a choice dressed as a
measurement.

⚠ **Three things this must not do.** (a) Extend Mori's Simon form below its reference point — the form's
anchor is borrowed and its own data start 13 GPa higher. (c) Fit a line through the printed points — that
is our arithmetic and the sources draw a **kink**, not a line: Fe₃S₂ stabilises near 14 GPa and Fe₃S near
21 GPa, and Chen 2008 draws inflections at both. And it must not **elect** a lineage; if a curve is ever
chosen it is registered as *piecewise*, because a single segment across this window erases that kink.

#### Amendment — Andrault's body is held, and the two ends now carry different grades

⚠ **P16 grew after the section above was written.** Cited then at sha256 `ea4055ff27e7c986…` / 17952 B; it
is now `adbe3d80444a5841…` / **23542 B** with an Amendment 1 that installs Andrault+ 2009's body text.
*That is the hash rule earning its place on its first use* — the earlier citation was true when made and
can be shown to be.

**The low end is no longer abstract-only.** Andrault's Table 1 prints, as results, three in-window
triples of (P, T_Sol, X_eut): **(15 GPa, 1023 K, 20 ± 2 wt%)**, **(18.5 GPa, 1073 K, 14.5 ± 0.5)**,
**(20.6 GPa, 1123 K, 16 ± 0.5)**. `T_Sol` is *"complete recrystallization"* and `T_Liq` is complete
melting, so **the eutectic floor is `T_Sol`** and the liquidus values (1373 / 1523 / 1423 K) are a
different quantity — the bracket's low end takes `T_Sol`.

⚠ **The two ends do not have the same grade, and the band says so rather than inventing a word for it.**
The low end is **body** (Andrault's own table); the high end stays **abstract only** (Fei 2000's 1348 K at
21 GPa, Li 2001's 1223–1473 K band). The engine's grade vocabulary attaches to values, so **each end
carries its own grade** and the band is labelled *mixed-grade* in prose — no new grade name is created.

⚠ **One caveat travels with the low end, and it sits exactly on the ends.** The two charges with 2 at% Si
added *"in order to provide more reducing conditions"* are the **15 and 20.6 GPa** points — that is, **both
ends of the bracket's low side**, while the only Si-free charge (18.5 GPa) falls *inside* the window. So
the width the floor spans is carried entirely by Si-bearing runs, and the sentence the abstract is famous
for — *1023 K at 15 GPa to 1123 K at 20.6 GPa* — is that same pair. The paper treats them as the same
Fe–S system; this file records which charges the ends came from, because "two of three" would have
concealed that the two are the ends.

#### Predicted, before running

1. **Mars's core top reads liquid at both ends.** Its declared `T_c` is **2000 K**, above even the high
   end 1473 K, so the bracket does not straddle it and the verdict is not `cannot-say`.
2. **The four verdict cells become evaluable** — the refusal that blocked them was this gap.
3. **Radius rises from 1667 km toward 1830 km**; direction only, as registered in C55 (b) and still
   untested.
4. ⚠ **Every body that is not Mars stays bit-identical**, including the ones using `fe_prem`: this touches
   a curve no other material names.
5. ⚠ **A cell may become evaluable and still fail its window.** The core mass fraction is still
   `earth_like`'s 0.325 and still undeclared — that is C55's test of the *material*, not of the body.

#### Correction 178 D — the four cells do not refuse for the reason I wrote down

⚠ **C55 (b) says the cells refuse on the 10–21 GPa melting gap. That is wrong, and it was wrong because
I read the engine's message instead of the mechanism.** The message *was* the melting gap — because 178 C
attached `IRON_FES_GAP_REASON` to the material as its `gap_reason`, and `Material.phase_at` prints that
string whenever a pressure falls below a phase's floor. The label was mine, the print was faithful, and
the sentence it produced described a different fact.

**What actually happens.** `Material.phase_at` refuses at **0.0981 GPa** — the solver asks this material
for a density at essentially surface pressure — and the Fe–S fit is referenced at **19 GPa**, with nothing
printed below it. Removing the floor does not help: with `p_min = 0` the same solve fails with
*"P = 9.808e+07 Pa 에서 밀도가 수렴하지 않는다"*, because a 19 GPa-referenced BM2 has no root down there.

⚠ **So extending the melting bound would not have unblocked a single cell**, and 178 D's premise —
registered in C55 (c) — is wrong on that point. The melting gap is real and the bracket is still worth
building; **it is simply not what is in the way.**

**What is in the way** is that the structure solve evaluates the core material across the whole pressure
range it walks, including near the surface, while this material is only defined from 19 GPa up. Closing
that needs either a low-pressure branch for liquid Fe–S — *another* fit, another paper — or a solver that
never asks a core material for a surface-pressure density. **Neither is decided here**, and naming which
one it is comes before choosing.

**Repaired now:** the material's `gap_reason` says the pressure floor rather than the melting gap, so the
next reader gets the mechanism instead of the story I told.

⚠ **The rule this cost:** *read the mechanism, not the message.* An engine's refusal string is written by whoever set the label, and a label can be wrong while the print is faithful — so a refusal is evidence about **which branch fired**, and the branch is what has to be looked at before the sentence is copied into a record. This seat copied the sentence. The melting-gap constant stays exactly where
it belongs — on the melting curve, which is a different question asked at a different place.

### C60 (a) 2026-09-10 — two trial sites, one principle, pre-registered before the build

⚠ **Committed before the code.** C60 is the row saying a domain refusal raised **during a trial** is being
read as a **verdict about the body**. Brief 181 closes it. This section registers the rules, the decision
lines and the predictions first, because the brief's own predecessor — C55 (c) — got its premise wrong by
describing a mechanism it had not looked at.

**Baseline `1c87ef6e`.** Both sites were measured with the audit seat's instrument
`~/Desktop/NearStars-artifacts/2026-09-08-c47-step4/audit/audit_boundary_step.py`, sha256
`66f770b2374673b4…`, **3463 B**, hashed by this seat rather than copied from the relay (it replaces the
`9897f5bd…` · 2821 B version, which had no `--shoot` mode). It spies on `Material.phase_at` and
`Material.density` and prints the call sequence.

#### Site ① — the boundary trial step

An RK4 step evaluates four points, and the last of them sits a full step beyond where the step starts.
Measured, Mars-scale (`p_center` 45.9 GPa, cmf 0.325):

| material | core calls | lowest call | the step it belongs to | past the boundary |
|---|---|---|---|---|
| `fe_prem` | 4208 | **15.1531 GPa** (index 4204) | 15.2070 / 15.1801 / 15.1801 / 15.1531 — width ≈ 0.0539 GPa | 0.0535 GPa below the 15.2066 transition, and it **succeeds** |
| `fe_s_13wt_19gpa` | 4051 | **18.9993 GPa** | 19.0447 / 19.0220 / 19.0220 / 18.9993 — width ≈ 0.0454 | **0.0007 GPa = 0.7 MPa** below the 19 GPa floor, **1.5 %** of the step |
| `fe_s_19wt_19gpa` | 4199 | **18.9893 GPa** | 19.0313 / 19.0103 / 19.0103 / 18.9893 — width ≈ 0.0420 | 0.0107 GPa, **25 %** of the step |

The middle two evaluations are the same point, so **the difference of two consecutive recorded calls can
be 0** and is not a usable scale. The scale registered is the **step's own**, the Euler estimate that
`engine/interior.py@«dp = dr / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])»` is the corrected form of.

**Rule.** A substep that leaves the current material's domain by **no more than that step's width** is
**boundary reached**, and the in-step bisection this file already runs for `p_floor` finds the fraction.
Past that width it is a refusal and it is named. ⚠ `fe_prem` survives today only because its lowest phase
floor is 0 — it walks the same overshoot, it just has nothing to hit.

#### Site ② — the shooting bracket's trial central pressure

`engine/interior.py@«x1 = math.log(max(lo, hi * 1e-3))»` opens the bracket's lower end at a thousandth of
the upper one, and `integrate`'s first act is
`engine/interior.py@«rho_c = mat_c.density(p_center, t, t_pot)»` — the **innermost** material, asked at
that trial pressure. With `hi` near 98.1 GPa the trial is **0.0981 GPa**. Measured (`--shoot`):
`fe_s_13wt_19gpa` refuses there at index 46004, the three preceding calls being `silicate` at 0.0013 GPa —
the previous trial finishing; `fe_prem` walks the same path down to **0.0001 GPa** and lives.

⚠ **Site ①'s rule cannot cover this**, and registering that before building matters because 181's first
framing had one rule for both: 0.0981 GPa is about **19 GPa** below the floor, not a step's width. Under
the `dp` rule it would be judged a real refusal and the shot would die.

**Rule.** The bracket's lower end gets **a third name of its own** — `shoot_lo` — taken from the
**innermost** material's lowest `Phase.p_min`. A central pressure is the body's maximum pressure, so a
trial below the core material's floor **cannot be a solution**; excluding it removes non-solutions from
the search rather than physics from the model. ⚠ **`p_floor` is not reused for this.** `p_floor` is the
integration-*stop* convention read off the **outermost** material (1 bar for `h_he`, 0 for a condensed
body); attaching it to a core material would cut the body off at its own floor. And if the **converged**
central pressure lands below that floor, that is a real refusal, named with `under_reason` (178 E) — a
body too small for this fit.

#### Site ③ — the bracket built in 178 D has no consumer

`engine/core_state.py@«t_melt_cmb = material.t_melt(p_cmb)»` asks for a single value, and
`engine/eos.py@«def iron_fes_phase_verdict»` is called from tests only. So the 10–21 GPa bracket exists and
nothing reads it. 181 wires it: what `core_state` receives at Mars's **20.65 GPa** core-mantle boundary
must be the **bracket verdict** — liquid / solid / cannot-say against both ends — and not the old
"this melting-curve name has no branch" refusal. The single value still answers at and above 21 GPa.

⚠ **`t_melt`'s return type does not change**, and that is a decision rather than a convenience. Widening it
to *value-or-band* would rewrite eight consumers to serve one, and 178 D registered that **the consumer
compares against both ends** — not that `t_melt` hands back a band. So the band gets **its own accessor**
(`t_melt_band`), `core_state` is the only caller, and the other seven consumers keep today's path and
today's numbers. The regression line that holds this: **the seven other `t_melt` consumers return
bit-identical values.**

#### The four decision lines

- **ⓐ `fe_prem`'s boundary-overshooting step is still taken.** The reading changes; the integration path
  does not. **And its shoot-path trial sequence is unchanged too** — the same trial central pressures, in
  the same order, in the same number. That second half is the half that site ② could break.
- **ⓑ `fe_s_13wt_19gpa` walks centre-to-CMB with its lowest core call above 19 GPa.**
- **ⓒ A planted material with `p_min = 30 GPa` still refuses by name**, and the sentence names the floor.
  Neither rule may turn a real domain limit into silence.
- ⚠ **`fe_s_19wt_19gpa`'s 25 % is inside the condition, not near its edge.** Its overshoot is 0.0107 GPa
  against a step 0.0420 GPa wide — the largest of the three measured, and still a quarter of one step. The
  rule is registered as *within one step's width*, so 25 % passes and **1.5 % passing is not what makes it
  work**; a rule that only covered the 0.7 MPa case would leave the 19 wt% material refusing.
- **ⓓ The existing 11 materials' grids stay byte-identical and the seven bodies bit-identical.**

#### Predicted, before running

1. **Mars's two `fe_s` materials solve.**
2. ⚠ **Every body that is not Mars is bit-identical** — `fe_prem`, Earth, Pandora, all of them. **This is
   the regression that matters most**, because site ② edits a line whose own comment says it was left
   alone so that anchors stay bit-identical. The mechanism that should make this structural rather than
   hopeful: `shoot_lo` is a `max` against the existing lower end, and every material but the two Fe–S ones
   has `p_min = 0`, so the expression returns exactly what it returns today.
3. **C55's four verdict cells carry numbers for the first time**, compared against 1820–1870 km and
   5.7–6.3 g cm⁻³. ⚠ Evaluable is not passing — the core mass fraction is still `earth_like`'s 0.325 and
   still undeclared.
4. **Wired through site ③, `core_state` reads `liquid` at 20.65 GPa** (2000 K is above even the 1473 K
   high end).
5. **C59's two recorded-disagreement rows move.** Direction only — and a row does not close because it
   moved; a person closes it.

⚠ **Material domains and solver physics do not change.** No fit gains a range, no equation is rewritten.
What changes is **which pressures the solver asks about**. If a body's answer moves for any reason other
than Mars gaining a core material, that is a failure of this brief and not a result of it.

**Re-run after 181:** the same instrument, the same two commands, both modes, printed next to this table.

### C60 (b) 2026-09-10 — the build, and the one registered prediction that did not hold

Built against C60 (a), which was committed first. **Decision lines ⓐ ⓒ ⓓ ⓔ hold; ⓑ holds only away from
the composition Mars declares.** Measured with the audit seat's instruments, hashed here rather than
copied: `audit_boundary_step.py` sha256 `66f770b2374673b4…` (3463 B) and `tmelt_dump.py`
`15a7f2c3a894dc63…` (790 B) against its baseline `tmelt_1c87ef6e.json` `c9663b216c2891b7…` (5453 B).

#### What was built, and why two rules were needed rather than one

| site | what changed | what it says |
|---|---|---|
| ① boundary trial step | `deriv` clamps a substep to the material's own floor **only when the floor is within the step's width** | *a step brushing the boundary has reached it* |
| ② shooting bracket, static | the lower end takes `Material.shoot_lo`, the innermost material's lowest `Phase.p_min` | *this material has no values below here* |
| ② shooting bracket, narrowing | the lower point retries upward on `PhaseGap`, up to `SHOOT_LO_TRIES` | *this **body** does not solve with this material below here* |
| ③ consumer | `Material.t_melt_band` + a `melt_bracket` branch in `core_state` | *where the bound is a bracket, the verdict is, too* |

⚠ **The static floor alone does not open a single cell**, and finding that out is why the second half
exists. `shoot_lo` says Fe–S has values at and above 19 GPa; it does not say a Mars-mass body with a
32.5 % core needs a **central** pressure near 43–49 GPa before its core bottom clears that floor. Those are
different facts and the code now carries them as different mechanisms.

⚠ **And a rounding no-op became a refusal the moment the bracket end became a material floor.**
`math.exp(math.log(19e9))` is 18.9999 GPa, which is below the floor by 1e-4 GPa, so the first trial died on
the fit's own reference pressure. `p_try` raises the round-trip back to the end it came from — a `max`
that never binds when the end is 100 Pa, which is every other body.

#### The five decision lines

| line | result |
|---|---|
| **ⓐ** `fe_prem` still takes its boundary-overshooting step, and its shoot-path trial sequence is unchanged | ✅ the audit's trace is **identical in both modes** — 121954 calls / 59300 core in `--shoot`, the same lowest 15.1531 GPa at index 4204, the same 0.0001 GPa in the bracket walk |
| **ⓑ** `fe_s` walks centre-to-CMB with its lowest core call above 19 GPa | ⚠ **holds at cmf ≤ 0.24 and fails at the declared 0.325** — see below |
| **ⓒ** a planted `p_min = 30 GPa` material still refuses by name | ✅ *"29.9902 GPa 는 이 적합의 기준 아래(30.0000 GPa)"* — 178 E's `under_reason`, naming the floor |
| **ⓓ** the material grids stay byte-identical and the bodies bit-identical | ✅ **13 materials × 200 pressures × 3 temperatures byte-identical**, and **all seven bodies' `run.py` output byte-identical** |
| **ⓔ** `t_melt` does not move at a single point | ✅ **182 points (13 materials × 14 pressures) identical, values and `None`s and exceptions alike** — 75 values, 85 `None`, 22 refusals |

⚠ **One file had to change, and the guard that caught it is the point.** `test_ice_giant` failed on its
**path fingerprint** — values unchanged, code text of `_shoot_pressure` and `integrate` changed — and told
this brief to re-freeze in the same commit. It did. **The refreshed anchor's diff is four lines**: the
fingerprint, the date, and two wall-clock seconds. Uranus and Neptune are the two bodies that walk deepest
through the shooting and temperature loops, and neither moved.

#### ⓑ, and the correction it forces

**At `earth_like`'s core mass fraction the Fe–S core bottom is below the fit's floor, and it stays a
refusal.** Mars declares `composition_intent: earth_like`, which supplies **cmf 0.325**; at that value the
core cannot reach its mass share before pressure falls through 19 GPa, and the shot refuses at 18.98 GPa —
now from the right place, with the right sentence. Lower the core mass fraction and it solves:

| cmf | `fe_s_13wt_19gpa` | `fe_s_19wt_19gpa` |
|---|---|---|
| **0.325** (declared) | refuses @ 18.9809 GPa | refuses @ 18.9887 GPa |
| 0.28 | refuses @ 18.9793 | refuses @ 18.9781 |
| **0.24** | R_core **1698.6 km** · ρ **7.499** · P_cmb 20.042 | R_core **1736.8 km** · ρ **7.015** · P_cmb 19.344 |
| 0.20 | R_core 1600.1 km · ρ 7.475 · P_cmb 20.624 | R_core 1635.8 km · ρ 6.997 · P_cmb 19.976 |

⚠ **So the material's floor now selects the core mass fraction**, which is a constraint this engine did not
have before and did not go looking for. It is not a defect: 19 GPa is where Huang's anchor is, and a core
whose bottom is shallower than that is outside what the paper printed. **The cell that decides which cmf
Mars gets is still the owner's** (C55), and this brief does not touch `mars.yaml`.

#### The four verdict cells, with numbers for the first time — and all four outside their windows

`tools/c55_cells.py` prints the table above. Against the homogeneous-mantle window (**1820–1870 km** and
**5.7–6.3 g cm⁻³**, Durán 2022 / Stähler 2021), at cmf 0.24 the radii are **1698.6 / 1736.8 km** and the
densities **7.499 / 7.015 g cm⁻³** — **both axes outside, on both materials**. ⚠ *C55 (c) registered that
a cell may become evaluable and still fail, and it did.*

**The direction the density misses is the direction its own source predicts.** Huang+ 2023 writes that a
binary Fe–S core needs **at least ~20 wt% S at 19 GPa** to reach the seismic deficit; the owner's band tops
out at **19 wt%**, and 19 wt% lands at 7.0 against a 6.3 ceiling. So this is the band being measured, not
the engine being wrong — **and it is the first time C55's question has been asked in numbers.**

#### Prediction 5 could not be evaluated

C59's two recorded-disagreement rows were predicted to move. **They did not, and could not**: `mars.yaml`
still declares no `core_material`, so Mars's answer is byte-identical to the baseline's — it is one of the
seven in ⓓ. That prediction was about a wiring this brief deliberately does not do.

#### Two corrections to C60 (a)'s own text

⚠ **"Eight consumers" was a number nobody had counted.** `Material.t_melt` is called from **ten sites,
eleven calls**, in three modules — `core_state` five, `core_energy` three sites (four calls, one line calls
it twice), `interior` two — plus two delegations inside `eos.py` itself. The audit counted it, this seat
reproduced the count, and the code comments now carry the measured number. The decision the wrong number
supported is unaffected: ten sites is more reason not to widen the return type, not less.

⚠ **Site ① is not only a wasted step.** C60 (a) described the boundary excursion as a step that is taken
and thrown away, which is true of `fe_prem`. For Fe–S at Mars's scale the excursion happens **where the
core actually ends**, within 0.1 GPa of the fit's reference pressure — so what the clamp buys is not the
discarding of a wasted evaluation but the last step of a real layer. The rule is the same; the description
it was registered under was narrower than what it covers.

### C60 (c) 2026-09-10 — 181's fix moved the defect instead of removing it, and one of its conclusions is retracted

⚠ **C60 (b)'s headline conclusion — "the material's floor selects the core mass fraction" — is withdrawn.**
It was not the material. It was the clamp this seat wrote. The audit seat found it, and this seat
reproduced every step of the finding before accepting it.

#### The measurement that settles it

`fe_prem` and `fe_s_13wt_19gpa` are asked for the same body at the same core mass fractions. If the Fe–S
refusals were physics, `fe_prem`'s core-mantle boundary would be below 19 GPa in the refusing range. **It is
not, anywhere:**

| cmf | `fe_prem` P_cmb | `fe_s` after 181 | `fe_s` after 181 B |
|---|---|---|---|
| 0.24 | 20.649 GPa | ✅ 20.042 | ✅ 20.042 |
| 0.27 | **20.188** | ❌ refused @ 18.9996 | ✅ **19.564** |
| 0.30 | **19.693** | ❌ refused @ 18.9607 | ✅ **19.053** |
| 0.325 | **19.256** | ❌ refused @ 18.9809 | ❌ refused (answer below the floor) |

**Every refusal 181 produced between 0.27 and 0.30 was an artefact**, and the refusal pressures clustering
at 18.96–19.00 were the clamp's own position, not any body's boundary.

#### Two defects, both this seat's

⚠ **① `shoot_lo` was set to the floor exactly.** A trial starting at 19.0000 GPa takes its first step
straight through the floor, so the bracket's lower point was guaranteed to fail by construction and the
narrowing loop had to climb out of a hole this seat had dug.

⚠ **② The registered rule was implemented against the wrong quantity.** C60 (a) registered *"a substep that
leaves the domain by no more than the step's width"*, and the code tested **the step's starting point**
(`p − floor ≤ dp_step`) instead of the overshoot. Where the third Runge-Kutta stage is steeper than the
first, those two disagree — a **2340 Pa** excursion escaped the clamp and refused. ⚠ **And the rule as
worded was close to unfalsifiable**: the substeps of a step of width `dp` are within `dp` of its start by
construction, so "overshoot ≤ dp" almost never fails. A rule that cannot fail is not a rule.

#### What replaced it, and why the replacement is about the profile

**Inside a step, the material's floor is now clamped unconditionally** — exactly what
`engine/interior.py@«rr_rho = (mat.density(_at_floor(max(pp, p_stop)), t_rho, t_pot) if pp > 0.0»` already did
for `p_stop`, whose comment has said since the gas tables landed that a half-step below the floor is read
at the floor. Intermediate stages are machinery; they do not appear in any profile.

**The rule that can fail is about what the profile records:**

1. If the layer's floor falls inside this step and the layer will *not* finish inside it, the step is cut
   at the floor and the structure is marked `floor_truncated` with **the material, the pressure, and the
   fraction of its mass share it managed to fill**.
2. A truncated structure is a **legitimate trial** — its mass is short, which is exactly what the bracket's
   lower end is for — and an **illegitimate answer**. `shoot` refuses it by name.
3. If the layer *does* finish, but the boundary the profile records sits below the floor, that answer is
   refused too. This is the case a truncation check alone misses, and it is not rare: it is what
   `earth_like`'s 0.325 does.

⚠ **The refusal now names the mass-share shortfall and says explicitly that the pressure it prints is where
the layer stopped, not where the boundary is** — the boundary is below what this fit answers for, so the
engine does not have it and does not guess it.

#### The cut lands where the physics puts it — and the two layers do not cut at the same place

⚠ **Which layer produced a number has to be written down, because the answer differs.** `shoot` and the
node's own consumer `solve` record core-mantle boundaries about **0.5 kPa** apart, and 19 GPa is close
enough to the cut that this decides one cmf value:

| cmf | `shoot` P_cmb | `solve` P_cmb (the consumer) |
|---|---|---|
| 0.24 | 20.04157 ✅ | 20.04106 ✅ |
| 0.27 | 19.56360 ✅ | 19.56310 ✅ |
| 0.30 | 19.05322 ✅ | 19.05273 ✅ |
| **0.302** | 19.01809 ✅ | **19.01760 ✅ — the last one that survives** |
| **0.303** | 19.00047 ✅ | ❌ refused (19.0000, below 19.0000) |
| 0.305 | ❌ 18.96514 | ❌ 18.9647 |

**The last core mass fraction this material carries is 0.302 at the layer that matters**, and the crossing
is where Mars's core-mantle boundary passes the fit's 19 GPa reference. ⚠ *The audit's independent
extrapolation of `fe_prem`'s slope predicted 19.57 GPa at cmf 0.27; the built engine gives **19.5636**.*
Two seats, two methods, 0.007 GPa apart.

⚠ **This is what closes C60.** The floor sets an **upper bound on the core mass fraction**, that bound
comes from physics — the boundary reaching the fit's reference pressure — and it is decided on the
**converged answer**, never on a trial. A trial that walks out of the domain is a bracket point; only an
answer refuses.

**The mass axis does not misfire.** A 0.5 M⊕ body converges at every core mass fraction from 0.20 to 0.40,
with P_cmb from **86.9 down to 72.5 GPa** — nowhere near the floor, and no rule fires.

**ⓐ, ⓓ and ⓔ are unchanged by this brief**: `fe_prem`'s trace is identical in both audit modes, the 13
material grids are byte-identical, and `t_melt` does not move at any of the 182 points.

#### The C55 cells, re-measured across a band rather than at one point

⚠ **0.24 was never "the maximum the clamp allowed" — it was simply the first value tried.** Measured
properly (`tools/c55_cells.py`, now calling `shoot` so it cannot print a number the engine would refuse):

| cmf | `fe_s_13wt_19gpa` (`shoot` layer) | `fe_s_19wt_19gpa` | consumer (`solve`) |
|---|---|---|---|
| 0.24 | R 1698.6 km · ρ 7.499 | R 1736.8 km · ρ 7.015 | both ✅ |
| 0.27 | R 1765.6 · ρ 7.512 | refused (P_cmb 18.988) | 13 wt% ✅ |
| 0.30 | **R 1828.0 — inside the window** · ρ 7.521 | refused | 13 wt% ✅ |
| **0.302** | **R 1832.0 — inside** · ρ 7.521 | refused | **13 wt% ✅ — the last one** |
| 0.303 | R 1834.0 · ρ 7.522 | refused | ❌ refused |
| 0.325 | refused (P_cmb 18.968) | refused (18.962) | both ❌ |

⚠ **The radius axis passes and the density axis fails**, which is the exact case C55 registered as the
reason for carrying two axes: *"the one place this cell can pass on density and fail on radius, which is
the point of carrying both"* — here it is the mirror image, and it would have been read as a success if
only one axis were carried. **The density is 7.5 against a ceiling of 6.3 and does not come close at any
core mass fraction**, because the density of the core is set by the material, not by how big the core is.

⚠ *And the tool itself had this defect until now*: it called `_shoot_pressure` directly, below the layer
that refuses out-of-domain answers, so it printed numbers the engine would not have released. **It now
prints both layers side by side with the layer named**, because a table that does not say which layer a
number came from invites the next reader to mix them — and at 0.303 the two layers disagree.

⚠ **The sulphur band cannot reach the density window on this anchor.** At **19 wt%, the band's own top
end**, the core density is **7.015 g cm⁻³** against a ceiling of 6.3 — and the density barely moves with
core mass fraction, because it is set by the material. **So more sulphur is not the lever**; the next one
is the multi-component core (stage 2), which is the owner's decision of 2026-09-10.

### C55 (d) 2026-09-10 — the window's third source, the shelf above 21 GPa, and the one published curve that spans it

⚠ **No constant moves in this section.** Everything here is recorded because it is now *held as a body*,
and because two of the three findings would each be a reason to change `MORI_FES_EUTECTIC` if this
engine were in the business of electing a lineage. It is not. Sources: the parallel seat's
`P16-fe-s-melting-10-21gpa.md` (sha256 `31e03997df756426…`, **41260 B**) and
`P12-mars-core-material-candidates.md` (sha256 `b932c70929c9386b…`, **21970 B**), hashed at the moment of
citing; the arithmetic below was re-done at this seat from the printed coefficients.

#### A third body inside the window, and one that is not a eutectic temperature at all

**Fei, Bertka & Finger 1997** ([`1997Sci...275.1621F`](https://ui.adsabs.harvard.edu/abs/1997Sci...275.1621F), held) prints, as a result, *"The eutectic T linearly
decreased with increasing P, from **988°C at 1 bar to 860°C at 14 GPa**"* and *"At T = 875°C and P = 14 GPa,
Fe₃S₂ coexisted with a eutectic liquid composition (**18.2 ± 0.3% S**)"*. So **1133 K at 14 GPa** is a third
in-window point, and it agrees with Andrault 2009's low lineage to about 100 K — Morard 2007 says so in its
own words (*"With a systematic difference of approximately 100 K, we have a reasonable agreement … with the
study of Fei et al. (1997)"*).

⚠ **Morard+ 2007's Table 2 must not be read as a eutectic curve**, and this is the kind of mistake this
file exists to prevent. Its P–T rows are *"in-situ conditions at which the liquid was measured"* with a
stated uncertainty of **170 K** — measurement conditions, not bracketed melting points. It enters this
record as **qualitative agreement only**: *"Our observations are compatible with a decrease of eutectic
temperature with increasing pressure."*

**The bracket's low end does not move.** Fei 1997's 1133 K at 14 GPa sits *above* Andrault's 1023 K at
15 GPa, so the printed minimum inside 10–21 GPa is unchanged.

#### The shelf immediately above 21 GPa, now held as bodies

| P | T_eutectic | source |
|---|---|---|
| 21.9 GPa | **1512 ± 19 K** (in situ, liquid present) | Chudinovskikh & Boehler 2007 ([`2007E&PSL.257...97C`](https://ui.adsabs.harvard.edu/abs/2007E&PSL.257...97C)) |
| 23.0 GPa | **1450 ± 30 K** (liquid + Fe + FeS) | same, run eu30 |
| 26.4–28.4 GPa | **1380–1410 ± 80 K** (first melt by XRD) | Kamada+ 2010 ([`2010E&PSL.294...94K`](https://ui.adsabs.harvard.edu/abs/2010E&PSL.294...94K)) |
| 29 → 65 GPa | **1450 ± 150 → 1980 ± 150 K**, slope 15 K/GPa | Morard+ 2008 ([`2008E&PSL.272..620M`](https://ui.adsabs.harvard.edu/abs/2008E&PSL.272..620M)) |
| 40 GPa | **1520 K** | Stewart+ 2007 ([`2007Sci...316.1323S`](https://ui.adsabs.harvard.edu/abs/2007Sci...316.1323S)) |

⚠ **These bracket the 21 GPa value our curve is anchored on from *above*** — Fei 2000's 1348 K as Mori 2017
reads it, or **1380 K as Morard 2007 reads the same paper** — and they sit **250–400 K above** Andrault's
1123 K at 20.6 GPa. **The 20.6 → 21.9 GPa step is printed as a kink by the sources themselves**: Stewart
2007 writes *"Eutectic temperature inflections around 14 and 20 GPa are due to the stabilization of Fe₃S₂
and Fe₃S above these pressures."* ⚠ Whether that step is the phase change or a between-laboratory offset
**cannot be settled without Fei 2000's body**, which did not arrive. **`MORI_FES_EUTECTIC` keeps 1348 K**;
that the same paper is read as 1380 K elsewhere is recorded next to it, not averaged into it.

#### Candidate (f): the only published curve that crosses the window continuously — and it disagrees with itself

**Rivoldini+ 2011** ([`2011Icar..213..451R`](https://ui.adsabs.harvard.edu/abs/2011Icar..213..451R), held) parameterises the eutectic as three linear segments,
eq. (4) `T_e(P) = T_e,0 + b₁(P − P_e,0)`, Table 4:

| interval | P_e,0 | T_e,0 | b₁ |
|---|---|---|---|
| 3 ≤ P < 14 GPa | 3 | 1268 K | −11 K/GPa |
| **14 ≤ P < 21 GPa** | 14 | **1144 K** | **+29 K/GPa** |
| 21 ≤ P < 60 GPa | 21 | 1255 K | +13 K/GPa |

Recomputed here from those coefficients: **T_e(20.65 GPa) = 1336.8 K**, which is **inside our bracket
(1023–1473 K)**. ⚠ *So the one published continuous curve does not open or close a single verdict cell* —
Mars's declared 2000 K is above it exactly as it is above both bracket ends.

⚠ **And the paper does not agree with itself in four places, recomputed here rather than taken on report:**

| # | as printed | what it gives | the reading that fits the paper's own figures |
|---|---|---|---|
| A | Table 3 `a₁ = −0.32 K/GPa`, `a₂ = 28.95 K/GPa²` | T_m,Fe(20.65) = **14161 K** | swap them → **2283.8 K**, matching its Fig. 1 range |
| B | eq. (5) `c₂ = −0.065 GPa⁻¹` | x_e(20 GPa) = **0.796** | read as decreasing → **0.161** (≈16 wt% S) |
| C | Table 4 middle segment | T_e(21⁻) = **1347 K** vs the third segment's start **1255 K** | joining them needs b₁ = **15.857**, not 29 |
| D | Table 4 first segment at its own upper end | T_e(14) = **1147 K** vs the middle segment's declared start **1144 K** | a **3 K** discontinuity where the text says the segments were *joined* |

⚠ **C is the interesting one**: with the printed b₁ = 29 the middle segment lands on **1347 K at 21 GPa**,
one kelvin from the 1348 K Mori 2017 attributes to Fei 2000 — so the fit's middle segment appears to be
aimed at the very value the low-lineage bodies contradict. **None of A–D is resolved here.** Candidate (f)
is listed with the note that it is usable only with a *declared* reading of each, and a declared reading is
an owner decision, not a transcription.

#### One printed sulphur value from outside the owner's band

**Terasaki+ 2019** ([`2019JGRE..124.2272T`](https://ui.adsabs.harvard.edu/abs/2019JGRE..124.2272T), body held) prints, adopting Rivoldini's core radius: *"For R_C =
1,794 ± 65 km … we find that the core contains either **32.4 +1.8/−2.4 wt% of S** or 30.3 +2.4/−2.8 wt% of
Si."* ⚠ That is **far above the owner's 13–19 wt% band**, and the paper says why in its own sentence — at
that composition *"the liquidus phase … is either (Fe,Ni)₃₋ₓS₂ … because the S or Si content in the core is
richer than the eutectic composition (S = 16 wt% …) at the Martian CMB."* Recorded as a printed value from
a different modelling family, **not as a candidate for the band**, and not averaged with anything.

### C59 (a) 2026-09-10 — Mars never used `earth_like`'s 0.325, and three records said it did

⚠ **A correction, found while reading for C57 and verified here before being written down.** `mars.yaml`
declares **`core_mass_fraction: 0.24`** eight lines above the note that says the engine ignores it, and
`interior.solve` prefers a declaration over a preset. The state the node receives carries 0.24 — checked
with a spy on `_solve_from_state` — and `solve(0.1074, core_mass_fraction=0.24)` reproduces the shipped
run's `core_radius_fraction` **0.4919 exactly**. At 0.325 the engine gives **0.5542 = 1842 km**, which is
*inside* the board's 1820–1870 km window and 12 km from its 1830.

**Three records were wrong and are repaired here**: `mars.yaml`'s own recorded-disagreement note, C60 (b)
and (c)'s description of "the composition Mars declares", and `tools/c55_cells.py`, whose "declared
composition" row printed the preset's 0.325 — **a composition Mars does not solve with**. The tool now
reads the declaration out of the body file, and falls back to the preset only when there is none.

⚠ **What is retracted is the cause, not the observation.** The engine's 1666.5 km still lands inside the
layered family's windows (Khan 2023 1645–1705 km, Samuel 2023 1630–1670), and we still never elected that
family, so **that reading stays "coincidence"**. What was wrong was attributing the number to a preset.

#### C59 is not about which preset was picked

**It is a statement about the density profile.** At Mars's mass and radius this engine needs a core mass
fraction near **0.325** to reproduce the observed **1830 km** core, while the declared value is **0.24** —
and the pair (0.24 ↔ 1830 km) is what `test_interior.py`'s `ANCHORS` table carries in one row, sourced
"Konopliv+ 2011 · InSight". ⚠ *So the anchor table states a pair this engine cannot produce*, and that is
the disagreement C59 actually names.

⚠ **And the two axes move in opposite directions**, which is the finding that matters for C57:

| cmf | core radius fraction (want 0.5398) | `nmoi` (want 0.36340) |
|---|---|---|
| **0.24** (declared) | 0.4919 — **8.87 %** off | 0.3545 — **2.71 %** off |
| **0.325** (`earth_like`) | 0.5542 — **2.65 %** off | 0.3450 — **5.32 %** off |

**No single core mass fraction satisfies both.** Enlarging the core fixes the radius and breaks the moment
of inertia, and the reverse. *An inversion that optimises one axis will make the other worse*, and that is
registered here before C57 is built rather than discovered afterwards.

#### Mars's declared composition does solve with Fe–S

Because 0.24 is below the 0.302 cut C60 (c) measured, **both band-end materials solve at the composition
Mars actually declares** — the opposite of what C60 (b) recorded, which was about 0.325:

| core material | R_core | fraction (want 0.5398) | `nmoi` (want 0.36340) |
|---|---|---|---|
| `fe_prem` (today) | 1666.5 km | 0.4919 — 8.87 % | 0.3545 — 2.71 % |
| `fe_s_13wt_19gpa` | 1698.6 km | 0.5001 — 7.36 % | 0.3566 — 2.14 % |
| **`fe_s_19wt_19gpa`** | **1736.7 km** | **0.5097 — 5.57 %** | **0.3593 — 1.40 %** |

⚠ **Both of C59's recorded rows move in the right direction and the moment-of-inertia gap roughly halves**
— and neither closes. ⚠ *C60 (b) registered prediction 5 as "could not be evaluated"; it could, and the
reason it was not is the same 0.325 error.* **Mars is still not wired**: which material Mars declares is
C55's owner cell, and this section changes no body input.

#### Two smaller corrections

⚠ **The 19 GPa crossing is at cmf 0.3030, not 0.306.** Measured on the consuming path: P_cmb is 19.08772
at 0.298, 19.05273 at 0.300, 19.01760 at 0.302 — a slope of **−17.53 GPa per unit cmf**, crossing 19 GPa
at **0.3030**. So 181 B's cut (converges to 0.302, refuses from 0.303) sits **on** the physical crossing
rather than short of it, and the "solvable but refused" band the earlier number implied does not exist.

⚠ **`mars.yaml`'s 0.24 is sourced, but one step short.** Its comment cites `test_interior.py`'s `ANCHORS`
row rather than Konopliv+ 2011 itself — *our own table is base material, not evidence* — so it is recorded
here as a citation to be walked one step further back, not as an unsourced number.

⚠ **The item count in 169 G's commit message (37) was the derivation's output, not the gate's**; the gate
counts 43–44 items for the same commit. And the `tools/*.py` rule was never blanket: measured, a changed
`tools/make_water_table.py` yields `gap` and the lane falls back to full, so no writer tool can be run by
a narrowed lane. **Nothing was rolled back because nothing needed to be.**

#### Where the silent default actually bites — measured, not assumed

Of the seven roster bodies, **the three that reach the rocky path all declare their own core mass
fraction** (Earth 0.325, Mars 0.24, Pandora 0.325). The four that declare neither a fraction nor an intent
are `alpha_centauri_a_b`, `dante_fixture` and the two Luhman 16 components — and only there does
`_solve_from_state`'s literal `"earth_like"` decide anything.

⚠ **And it decides more than a refusal.** `dante_fixture` **produces an answer**: `interior_layers` returns
a radius of 455.7 km with `inputs["core_mass_fraction"] = 0.325` and `composition = earth_like` in its own
evidence — *a number nobody declared, carried under a name*. ⚠ `alpha_centauri_a_b` is a **giant** of
120 M⊕ with no composition declared at all, and the same default sends it down the rocky path to refuse
that *"this mass needs a central pressure above `fe_prem`'s ceiling (12000 GPa)"* — **a refusal that names
iron where the fact is that nobody declared a composition for a gas giant.** That is C37's shape again.

⚠ **The two consumers of the same silence do not agree.** `interior_layers` fills it with `earth_like`;
`dynamo_rocky` never asks — its printed refusal for the fixture is `cannot-say (conductor_phase
undecided)`, which is about temperature. The fixture's own comment claimed `dynamo_rocky` *"refuses by
name because there is no composition preset (C28)"*; **it does not**, and that comment is repaired here.

#### A rule this seat's own mistake bought

⚠ **In a shared worktree, never `git reset --hard`, `git checkout -- .`, or `git stash`.** This seat ran a
`reset --hard` to measure the lane's behaviour and **destroyed another seat's uncommitted edits to
`SESSION-HANDOFF.md`** — unstaged changes are not in the object store and were not recoverable. The
measurement did not need the shared tree at all; a scratch clone was already sitting in `$TMPDIR`.
**Measurements that need a commit are made in a scratch clone.**

### C57 (a) 2026-09-10 — the inverse branch is unreachable, and the undeclared case is a nameless default — read and pre-registered before the build

⚠ **Committed before the code.** The owner's decision of 2026-09-10 is that **Mars's core mass fraction is
not to be declared — the solver must infer it**, which makes C57 (the inverse branch nothing calls) the
brief that has to run first. This section is the reading; the build is 182 B.

#### What is there today, measured

| fact | measured how |
|---|---|
| `infer_composition` is called from **two files only** — `test_interior.py` and `rocky_roster.py` | grep of every call site; the node path has none |
| the node path enters through `engine/interior.py@«def _solve_from_state(state):»`, which resolves composition as `state.get("composition_intent", "earth_like")` | read, then confirmed by a spy on the state a real body hands over |
| a **declared** `core_mass_fraction` beats the preset (`cmf = preset_cmf if core_mass_fraction is None else core_mass_fraction`) | Mars: declared 0.24 reproduces the shipped 0.4919 exactly (C59 (a)) |
| **three of seven** bodies declare a core mass fraction; four declare neither it nor an intent | body-file census |
| the silent default **produces answers**, not only refusals | `dante_fixture` returns a 455.7 km radius carrying `inputs["core_mass_fraction"] = 0.325` |
| it also sends a **giant** down the rocky path | `alpha_centauri_a_b`, 120 M⊕, no composition declared, refuses on `fe_prem`'s 12000 GPa ceiling |
| the two consumers of the same silence **disagree** | `interior_layers` fills it; `dynamo_rocky` never asks (its refusal is about temperature) |

#### The first judgement C50's vocabulary asks for

**Is `earth_like` a `Declared-optional` — a default with a written reason — or a nameless one?**
⚠ **Nameless.** `docs/reference/interior-structure-methodology.md@«**Declared-optional** — inputs this recipe declares a default for, in the code and in prose above; absent is a normal state, not a hole (C50 (b), Brief 170 B). `ice_mass_fraction` [—] (absent is recorded as `0.0`, because the recipe normalises it internally)»`
lists six optional inputs and **`composition` is not among them — it is on the `Needs` line**, i.e. the
contract calls it required. The default lives at the call site instead, and `check_contracts` reports
**class ④ = 0**, so nothing today counts it. ⚠ *A required input silently supplied by its caller is the
shape C45 was built to find, and it is not being found.* **Why the checker misses it is a decision line
below, not an assertion here** — the contract's name (`composition`) and the state key
(`composition_intent`) are two strings for one quantity, and whether that is the reason is 182 B's to
measure.

#### The decision lines, before anything is built

- **ⓐ The census does not move.** Three bodies declare a core mass fraction, four declare nothing, and the
  four are `alpha_centauri_a_b`, `dante_fixture`, `luhman_16_a`, `luhman_16_b`.
- **ⓑ `dante_fixture`'s `inputs["core_mass_fraction"]` stops being 0.325-from-nowhere.** It becomes either
  a value the body declares or a refusal that names the missing declaration — **not a third silent number**.
- **ⓒ The 0.24 is traced one step further back.** Its source today is *our own* `test_interior.py` ANCHORS
  row; the primary is Konopliv+ 2011, **which is not in the held cache** (`docs/phase3/_papers/` has no
  `…K` bibcode for it). Fetching it, or labelling the value as second-hand through Rivoldini 2011, is the
  first act of 182 B.
- **ⓓ The moment-of-inertia anchor declares its convention.** ⚠ **This entry stated the convention backwards
  and the correction is written here rather than below.** It said: *0.3644 is Konopliv 2011's **equatorial-radius**
  form; the mean-radius form differs by **≈0.0009**, which is larger than the printed uncertainties
  (0.0001–0.0006).* ⚠ **0.3644 is the mean-radius form.** Rivoldini+ 2011's table carries it under the footnote
  `MOI = I/ma ra²` with `ra = 3389.5 ± 0.2 (Seidelmann 2002)`, the volumetric mean radius; the equatorial
  convention is the separate polar row `C/(ma·re²)` at `re = 3396.2`, and 0.3644 is not that number.
  ⚠ **And the convention does not explain the gap it was invoked for.** `(3396.2/3389.5)² = 1.003957`, so
  `0.36340 × 1.003957 = 0.36484` — a convention step of **0.0014**, while the difference actually to be
  explained is `0.3644 − 0.36340 = 0.0010`. **The step is larger than the gap and in the wrong place**: the two
  figures are not one number in two conventions but **two determinations**, pre-InSight (Konopliv) against
  InSight (Stähler). ⚠ **Three numbers — 0.0009, 0.0014, 0.0010 — never agreed with each other, and that was the
  signal.** Nobody stopped on it; the entry's own arithmetic contradicted its own claim for as long as it stood.
  ⚠ *The gate's 0.01 tolerance is a gate width, not an uncertainty — that part stands.*
- **ⓔ No value moves.** 182 A is documentation; the seven bodies stay byte-identical.

#### Predicted, before running

1. ⚠ **An inversion that fits one axis will miss the other by more.** Already measured in C59 (a): at
   cmf 0.24 the radius is 8.87 % off and `nmoi` 2.71 %; at 0.325 they are 2.65 % and 5.32 %. The axes move
   against each other, so **there is no core mass fraction that satisfies both**, and an inverse solve on
   radius alone will hand back something near 0.325 and make the moment of inertia worse than today's.
2. **The inversion will not reach Mars anyway until a body stops declaring**, because a declaration beats
   the preset. So the first bodies it changes are the four that declare nothing — and three of those are
   not rocky.
3. **`dante_fixture` is the only body the inverse branch can actually run on today**, which is the reason
   that fixture exists (C45 (e)) and also the reason its evidence is the cleanest place to see the change.
4. ⚠ **Class ④ may move off zero**, if the reason the checker misses this is nameable and fixable. If it
   does not move, that is a finding about the checker, not a success.
5. **`alpha_centauri_a_b`'s refusal changes what it names** — from iron's pressure ceiling to the absent
   declaration — or it stays and that is recorded as a second consumer needing the same repair.

### C57 (b) 2026-09-10 — the inversion is on the node path, and the silent fill is gone

Built against C57 (a). **Decision lines ⓐ, ⓑ and ⓔ hold; ⓒ and ⓓ stay open by design.**

#### What changed

`engine/interior.py@«def _infer_from_state(state):»` replaces the call-site literal. When a body declares
**neither** `composition_intent` **nor** `core_mass_fraction`, the recipe no longer fills the hole: it
inverts if the inversion means anything for that body, and otherwise **refuses by name, saying what the
old default was**. A body that declares either one never reaches the new branch, which is why the declared
bodies are untouched.

⚠ **The first cut of this broke two refusals, and the ordering rule it bought is the finding.** Putting the
composition branch first made the two brown dwarfs refuse with *"no composition is declared"* instead of
`solve`'s *"deuterium burns — above 13 M_J the luminosity varies with time (Spiegel+ 2011)"*. **A refusal
that already names its own physics wins over a more general one**, so `FLUID_CLASSES` bodies keep the old
path and both Luhman 16 components are byte-identical again.

#### The two bodies that move, and what they now say

| body | before | after |
|---|---|---|
| `dante_fixture` | an answer carrying `core_mass_fraction = 0.325` **that nobody declared** | **the inversion runs**: regime `inferred_initial_porosity`, core mass fraction **0**, `initial_porosity` **0.3890625**, radius 0.08175 R⊕ (the declared one, by construction), `nmoi` 0.3518 → **0.3771** |
| `alpha_centauri_a_b` | *"the integration failed — this mass needs a central pressure above `fe_prem`'s ceiling (12000 GPa)"* | *"no composition is declared — neither `composition_intent` nor `core_mass_fraction`. This used to be filled silently with `earth_like` … the inversion cannot stand in either, because this recipe's inversion fits a radius with metal, rock and ice, which means nothing for a `giant`. **A declaration is needed.**"* |

⚠ **The fixture's low density turns out to be void space, not a small core.** The inversion chose the
**porosity** axis — its radius is *larger* than pure rock at that mass and ice is excluded by the file's own
`ice_mass_fraction: 0.0` — so `core_state` now says *"there is no core"* instead of reporting a core the
declaration never asked for. ⚠ *That is the same fixture whose comment claimed `dynamo_rocky` refuses for a
missing preset; both statements were artefacts of the silent fill.*

⚠ **And the giant's refusal now names the cause instead of iron.** 120 M⊕ was being asked to be a
32.5 %-iron body because nobody said otherwise, and the sentence it printed was about iron's pressure
ceiling. **That was C37's shape at the widest scale in this engine** — a faithful message about the wrong
mechanism.

#### The registered predictions

| # | registered | result |
|---|---|---|
| 1 | an inversion fitting one axis misses the other by more | ⚠ **not yet tested** — no body inverts on radius *and* has a published moment of inertia. Mars declares, so it does not invert. **Stays registered.** |
| 2 | the inversion reaches only bodies that declare nothing | ✅ four bodies; three of those are not rocky |
| 3 | `dante_fixture` is the only body the inverse branch can run on | ✅ exactly one body inverts |
| 4 | class ④ may move off zero | ✅ **it moved, and into the right bucket**: `0 unexplained · 1 inversion convention · 0 undecidable`, the convention row reading *"the missed `initial_porosity` is in Dante's evidence as 0.3890625 (call-site default [0.0]) — the inversion reported its own axis"*. ⚠ *The `inputs[axis] = value` convention fired on the node path for the first time.* |
| 5 | the giant's refusal changes what it names | ✅ |

#### Two contract facts the build had to settle

⚠ **`ice_allowed` became a contract input the moment the inversion reached the node path**, and
`check_contracts` said so: *"code uses it, the document's Needs does not have it."* It is written into
`Declared-optional` as **derived, not declared** — `ice_mass_fraction` read as a statement, where an
explicit `0.0` means *"this body has no ice"* and absence means *"unknown"*, and only the second opens the
ice axis. The Korean mirror carries the same sentence.

⚠ **And a printed count went quietly false.** `test_check_refs` compares the exemption set as a *set*, so
it passed once `ice_allowed` was registered — but the number printed beside it, *"9 unique · 12 slots"*,
was a literal and now said the wrong thing. **It is computed from the set now**, so the next entry cannot
make the sentence lie. *That is Brief 38 E's shape, found in the test that exists to find such things.*

**Everything else is unchanged**: ten test files pass, Earth and Pandora are byte-identical, Mars's values
are identical (only the note this seat corrected differs), and the contract check goes from 1399 lookups
to 1405 — the six the inversion path adds.

### C45 (f) 2026-09-10 — a contract's required input given a default by its caller, nineteen times, counted by nothing

⚠ **Measured while closing 182 B, not designed for.** `engine/check_contracts.py@«def ast_lookup_defaults(node: str) -> dict[str, object]:»`
collects defaults from **two layers**, and says so itself (171 B): the adapter's `state.get(k, d)`, and
**every function-parameter default in the same module**, gathered by name — *"this side is coarse, and
coarse is the safe direction: it errs toward forgiving, not toward missing."* Its discriminant is then
*whether the recorded value equals one of those defaults*. ⚠ **What no line asks is the prior question —
whether any contract line declares a default at all** — so a literal written only in the code answers for
one the contract never wrote, and class ④ stays at zero.

**Intersecting each recipe's `Needs` set with the non-`None` literal defaults its node can receive gives
nineteen pairs**, reproduced here with the audit seat's `audit_c45f.py` (sha256 `2471641d1ce75226…`,
**2666 B**, hashed here) and independently with this seat's own walk — both give **19**:

| key | default | nodes |
|---|---|---|
| `core_material` | `'fe_prem'` | **five** — `cmb_heat_flux`, `core_energy_balance`, `core_entropy_production`, `core_state`, `core_thermal_history` |
| `composition` | `'earth_like'` | **two** — `interior_layers`, `mass_radius_relation` |
| `body_class` | `'rocky'` / `'giant'` | `dynamo_rocky`, `dynamo_giant` |
| `is_satellite` | `False` | `body_class` |
| nine more (`tidal_heating` `False`, `envelope_z_rock_fraction` `1.0`, `serpentinisation` `0.0`, `differentiation_front` `1.0`, `crust_rock_fraction` `0.0`, `crust_porosity` `False`, `boundary_temperature_jump` `0.0`, `mantle_rock_fraction` `0.0`, `ammonia_mass_fraction` `0.0`) | as printed | `interior_layers` |

⚠ **The split between the two layers matters for the repair, not for the count.** Only **6** of the 19 come
from an adapter's `state.get(k, literal)`; all 19 are reachable through a module's signature defaults, so
**deleting the adapter literal — which is what 182 B did for one key — does not remove the default.**
`core_state` is the clean example: it has no `state.get("core_material", …)` at all and still receives
`'fe_prem'`, through `engine/core_state.py@«core_material = COMPOSITIONS.get(composition, (0, 0, 0, "fe_prem"))[3]»`.

⚠ **`core_material = 'fe_prem'` in five nodes is the same problem C55 spent a day on**, one layer down: a
body that declares no core material is silently given PREM iron by every thermal node, and no check counts
it. ⚠ **And `composition = 'earth_like'` survives in `mass_radius_relation`** — 182 B removed the silent
fill from one consumer and a second still has it.

**Some of the sixteen are surely legitimate** (`tidal_heating` absent meaning "no tidal heating" is a
reasonable reading). ⚠ **The finding is that nothing separates the legitimate ones from the smuggled ones.**
The repair is per-entry: move it into `Declared-optional` with the reason written, or refuse. **Listed, not
started**; the count 16 is the baseline a checker addition would have to move.

⚠ **The `earth_like` literal was still in the code when this was written** — `composition=state.get("composition_intent", "earth_like"),` — **and was removed on 2026-09-20 (C57 (c))**; the call now reads `composition=state.get("composition_intent"),`. *Both are quoted as plain code, since the first no longer exists to anchor to.*
182 B removed the *bodies* that reach it, not the mechanism: the path that still would is «a body that
declares a mass fraction but no intent», and **there is no such body today**. If one appears it takes the
preset's *material* — `fe_prem` — so the problem 182 B stripped off the fraction remains one layer down on
the **material**. *"The material is a declaration too"* is the sentence C55 arrived at from the other side.

⚠ **And one number from C57 (a) ⓓ is now cross-checked**: Rivoldini+ 2011 prints `I/MR²` **0.3645 ± 0.0005**
in the same convention as the board's 0.3644 — ⚠ **which is the mean-radius convention, not the equatorial one
this paragraph first named** (the correction, with the arithmetic that refutes it, is at C57 (a) ⓓ itself).
The two figures agreeing to 0.0001 in the same convention is the cross-check; **the convention still has to be
declared before an inversion is anchored on it**, and that is what this entry was reaching for.

### C57 (c) 2026-09-20 — the inversion's answer is delivered, and Mars stops declaring its core

**Registered in `c57-inversion-prereg-revision.md`, body blob `72577201`, amendments 1 and 2.** The owner's
decision of 2026-09-10 — *Mars's core mass fraction is not declared, the solver infers it* — was built in
C57 (b) and **did not reach Mars**, because `mars.yaml` declared both `core_mass_fraction: 0.24` and
`composition_intent: earth_like` and the branch tests for both.

⚠ **Deleting the two lines alone does not work, and that was measured before anything was written.** Eight
nodes fall from *value* to *out of domain*, `core_thermal_history` among them, refusing with «cannot-say
(no core — no core radius or no core mass fraction)». The inversion solves the fraction and writes it into
the payload's **`inputs`**; `core_history` reads `state.get("core_mass_fraction")`, which sees **values**.
**The answer existed and was not delivered.**

**So the node delivers it.** `interior_layers` now returns `core_mass_fraction`, `ice_mass_fraction` and
`composition` whichever branch ran. Three things had to move together, and each was found by a run rather
than by reading:

- **The delivery sits in the node wrapper**, not in the inference branch. Emitting only there made the key
  blink — pass 1 inferred and published it, pass 2 read it back as a declaration, and pass 2's result
  carried no such key, so the state lost it again.
- **The branch is chosen from declared inputs only.** Asking `state.get` asked a question this node's own
  output could answer: pass 2 relabelled the inferred fraction `earth_like` and raised the grade from
  analog to **calibrated**. On declared inputs the branch is the same every pass and the answer is a fixed
  point.
- ⚠ **A departure from the registration**: the inversion now receives the body's declared
  `potential_temperature`. It was not registered, and without it that branch solves isothermally,
  `cmb_temperature` returns 0 K and `cmb_flux` raises *"no superadiabatic jump, eq. 37 undefined"*. **Every
  figure below was measured with that change in place.**

**Two things about that branch, read by the audit seat in the `4018fad8` tree and re-counted here** *(each phrase matches once)*: *it solves **one** free fraction — `engine/interior.py@«# 위의 역산은 자유 분율 **하나** 를 푼다 — 질량과 반지름 둘로 미지수 하나»` — and it refuses by name when it cannot: `engine/interior.py@«조성이 선언되지 않았고 역산할 반지름도 없다»`.* ⚠ **So the radius is not optional on this path** *(work seat, measured)*: **a caller that reaches `infer_composition` without `radius_earth` does not get an inversion — it falls to the preset's 0.325.** *The declaration this item deletes is therefore replaced by a different requirement, not by nothing.*

**The unchosen axis is pinned at 0.0** rather than left None — the solve used that value, and None read
downstream as *not declared*, which is what made `dynamo_rocky` refuse for want of an ice fraction it could
have been told. ⚠ *That 0.0 is this inversion's model assumption for a rocky body, not a measurement.*

**What the gate and the roster say** (parent `6d91e82a`, its log blob `03b76d88`): `[PASS]` **762** ·
`[FAIL]` **0** · `[SKIP]` **13** · `[STEP]` **77** · anchors **605 → 605**, by two different routes. ⚠ **Two anchors were retired on purpose**: *two ledger sentences cited the `"earth_like"` fallback by phrase, and the phrase is gone with it. **The sentences stay**, quoted as plain code in the past tense — an anchor to a line that no longer exists is a rotten anchor, and the record of what the line used to be is not.* ⚠ **And two were added in this record** — the inversion's degree of freedom and its named refusal — *so the count leaves at 603 and returns to 605 by a different route than it left.* Every body's node tally is unchanged
across both commits and across two rebases — `2·12·1·20` (Alpha Centauri A b) · `4·10·1·20` (Dante
fixture) · `11·3·1·20` (Earth) · `2·12·1·20` · `2·12·1·20` (Luhman 16 A, B) · `11·3·1·20` (Mars) ·
`9·5·1·20` (Pandora). The three `[증인]` lines of `test_core_history` are byte-identical to the baseline.

**The ice-giant fingerprint was re-frozen, six lines, and the six are three commits' worth**: *`chain.yaml` and `interior.py` (byte and code digests) from C57 (c) itself; `core_history.py`'s byte digest from the 216 K commit that landed before it; and the two `seconds` (28.2 → 27.8, 37.4 → 37.1), which are machine, not model.* **No value key moved.** ⚠ *The two `seconds` are **one run's clock**, not a property of this tree: a re-freeze on the same digests produced 28.0 / 37.3 against the committed 27.8 / 37.1, and the committed pair was kept because it came **first**, not because it is more right. **When they drift again, that is the machine** — tonight one clock loop read −12.5 %.*

⚠ **Acceptance B's three predictions: two missed, and they are written as missed** *(audit seat's reading)*. *The registration predicted the fraction would **rise** toward ~0.325 and the core radius would enter the board's 1820–1870 km window. Measured: **0.24 → 0.23958333333333331**, a fall of 0.17 % of itself; core radius **0.2616 → 0.2614 R⊕ ≈ 1 665.6 km**, which is **~155 km below the window**, and `core_radius_fraction` **0.4916**. **The third — that `d_m` would fall — is not reported here because this item does not print it.*** ⚠ **A miss stays a miss**: *0.325 is the `earth_like` preset's fraction, and an inversion tied to Mars's radius cannot choose it. That is the evidence branch ⓑ of the sulphur-fit registration rests on — the box, not the declaration, is what the core radius waits on.*

⚠ **One printed pair moved, and this seat did not declare it** *(the directing seat saw the movement after the green gate; the audit seat confirmed that the frozen registration `24f5d27c` never registered those rows)*: the `[증인·법칙]` rows, which run through the **recipe** rather than through hand-built params, read **foley `t_m` 1774.674973674531 → 1768.2056095076882** and **nimmo 1358.4226002593311 → 1349.4669881086427**. *The cause is this item's whole point — the recipe now feeds them the inverted **0.23958333333333331** instead of the declared 0.24 — but **it was not in the pre-print**, and the three `[증인]` rows that were declared unchanged are the hand-built ones, which never read the body file.* **Two witness families, and only one of them was named.**

⚠ **C57 also moved the gate's total `instr`** *(audit seat)*: **106 226 900 440 337 → 127 123 476 525 090, +19.68 %**. *That is Mars beginning to run the inversion on every gate, not measurement noise — the number belongs beside the item that caused it.*

**Mars, before and after**: `core_mass_fraction` **0.24 declared → 0.23958333333333331 inferred**,
`composition` **`inferred`**, grade **`analog`**, `ice_mass_fraction` **0.0**, `cmb_temperature`
**1910.0244647221907 K**. ⚠ **The registered prediction failed**: the registration expected the fraction to
rise toward ~0.325 and the core radius to enter the board's window. It does neither — **0.325 is the
`earth_like` preset's fraction, and an inversion constrained by Mars's radius cannot choose it**. The
declared 0.24 and the inverted 0.2396 are the same answer to three decimals, so **C59's two recorded
disagreements stay outside their tolerances**: `core_radius_fraction` **8.9 %** against a 3 % tolerance,
`nmoi` **2.7 %** against 1 %.

**A second commit removes the silent default behind all of this.** `_solve_from_state` passed
`composition_intent` with a literal `"earth_like"` fallback, so a body that declared no composition was
solved as Earth and nothing said so — and the name reached `solve()` before the check that refuses an
unknown composition, so that refusal could not fire. The literal is gone; an undeclared body sends `None`,
and the branch above routes it to the inversion. **The roster is identical after that change too**, giants
included.

### C55 (g) 2026-09-20 — the quaternary phases answer below 19 GPa, named and counted

**Registered in `item19-quaternary-floor-prereg.md`, body blob `671ecc2d`, frozen.** The owner's decision of
2026-09-20 turns off `FE_S_BELOW_REF_REASON` **for the Fe–S–O–C phases only**: they may be carried below the
pressure their fit was measured at, so long as every such call is counted and its depth printed. ⚠ **No
tolerance was widened** — the rule was reversed for one family, and the binaries still refuse below 1.5 GPa.

**The floor is derived, not chosen.** `bm2_ref` reads `p = p_ref + 1.5·k0·(x^{7/3} − x^{5/3})` with
`x = ρ/ρ₀`, and that pressure **turns around** at `x = (5/7)^{3/2} = 0.6037`: below it two densities share a
pressure and the inversion has no answer. So `p_min` is now computed from the fit itself — measured on the
four S = 19 wt% corners, **6.4798 · 5.8730 · 9.9277 · 9.2766 GPa** — and `p_ref` does not move.

⚠ **That is a «cannot solve» floor, not a «solves wrongly» floor.** *Between it and 19 GPa the fit answers,
and how far wrong it is there is a different question: the same corners read **−16.7 % to −35.8 %** against
their own 19 GPa anchors at 10 GPa. **Mars sits 0.010601 GPa below the reference — 0.0558 % — and the
corners' own solutions sit 0.40 to 1.19 GPa below it**, where the density is off by 0.6 % to 2.3 %.*

**No new counter.** The existing `DENSITY_REACH["beyond_measured"]` counts these calls; beside it,
`DENSITY_BELOW_REF` carries **two depth cells** — the lowest pressure reached and `min(p / p_ref)`. *A count
says how often, the depths say how far; one without the other cannot tell a net that measures from a net
that is merely quiet.*

**What the fixtures separate, measured in one run**: a binary asked at 1.0 GPa **refuses by name**; a
quaternary at Mars's CMB **answers and counts once**, **0.010601 GPa below the reference — 0.0558 %**
*(`p/p_ref` 99.9442 %)*; a quaternary just above its turning point (6.4805 GPa) also answers,
**12.5195 GPa below — 65.89 %** *(`p/p_ref` 34.11 %)*. ⚠ **Both conventions are printed**, because the
registration's table used «how far below» and the first implementation printed its complement.
⚠ **And the registration's own guess for that third probe was wrong**: it said **≈9–13 GPa, ≈50 %**, and
the measurement is **6.4805 GPa, 65.89 %**. *The requirement — that the two depths differ visibly — is met;
the predicted numbers are not, and a miss is written as a miss.* ⚠ **The two depths must differ,
and they do by a factor of three** — *the roster's only sub-19 GPa user is Mars, so a counter that printed
«1» and nothing else would look exactly like a counter that measures nothing.*

⚠ **The materials say they are temporary.** *Each quaternary `Material`'s label now carries «19 GPa 아래는
이 적합을 이어 쓴 값 … 그 구간의 자료(P39)가 들어오면 이 상을 갈아 끼운다» — the condition lives on the
object, not only in a brief.*

### C55 (h) 2026-09-20 — the floor was checked against one pressure and the inversion ran at another

**Registered in `item19-quaternary-floor-prereg.md`, body blob `671ecc2d`, amendment 2 (file `25441802`).**
Item 19 gave the quaternary phases a floor at the fit's own turning point. ⚠ **The guard and the inversion
were not looking at the same number**: `Material.phase_at` tests the **total** pressure, while
`Phase.density` inverts at the **cold** pressure, `p − P_th`. A trial that passed the guard could therefore
run Newton **below** the floor and die there — measured, at `cmf 0.25` with `potential_temperature 1600`:
*«fe_core_19GPa_S0.2795O0.0295C0.0196: P=1.271e+09 Pa 에서 밀도가 수렴하지 않는다»*, a total of about
6.5 GPa arriving at the inverter as **1.271 GPa**.

**The floor now sits where the inversion reads.** Inside `Material.density`, for phases that declare
`graded_below_ref`, the cold pressure is computed once and tested: **not positive → a named refusal**
(the thermal pressure exceeds the total), **below the turning point → a named refusal** that prints the
cold pressure, the turning point, the total and the thermal pressure together. ⚠ *Phases without the
declaration do not take this branch, so nothing else in the registry changes.*

**What it unblocked.** *With the declared potential temperature on, the quaternary route had been refusing
almost everywhere — seven of eight probes across S 13–30 wt%. After this fix the same composition
(S 19 · O 1 · C 0.5 wt%, 1600 K) converges and returns a core radius of* **1 832.07 km** *(cmf 0.276042) —
a number produced in the region below 19 GPa that this engine continues by its own arithmetic, measured
against a board window (1820–1870 km) whose radii are **Durán+ 2022's abstract band**
(`2022PEPI..32506851D:79`) while its densities are Stähler+ 2021's 5.7–6.3 — ⚠ **two papers in one window**;
the earlier claim that it mixed the ends of Stähler's own two estimates is **withdrawn as wrong**, and which
series the gate should use is the owner's cell (④′), so*
**landing inside that window is not evidence**; *it is the same fit, carried further, compared with a
number nobody published.*

⚠ **Where the fingerprint's four lines can be seen, and where they cannot.** *They live in this commit's **diff of `engine/ice_giant_anchor.json`** — `eos.py`'s byte and code digests, and two `seconds`. **The gate log prints only the frozen figure**, one line, so a reader checking «did the fingerprint move» against the log will find nothing to compare. **The corpus to open is the diff.*** ⚠ *And the two `seconds` (27.3 → 27.7 · 36.3 → 36.7) are **the re-freeze's own clock**, not a quantity to compare across commits.*

⚠ **The earlier reading is withdrawn.** *«The sulphur axis cannot reproduce Mars's observed core radius»
was measured under this defect and is not a statement about the box. The sulphur fit is re-run after this
lands, and the owner's table carries the retraction beside the new figures.*

### C55 (e) 2026-09-10 — stage 2, the multi-component core, pre-registered before the build

⚠ **Committed before the code.** The owner's decisions of 2026-09-10: **O 1–4 wt%**, **C 0.5–1.4 wt%
included**, **H not declared** (the literature spread is six-fold and hydrogen dominates the density, so it
becomes its own decision). The sulphur band stays **13–19 wt%**. **Fe is the balance and Ni is excluded** —
Huang prints Ni derivatives (−0.182 / −0.018) if the owner later adds it.

Sources, hashed at the moment of citing: the parallel seat's `P21-c55-stage2-endpoints.md` (sha256
`23fe53c6e0ce2318…`, **3853 B**), `P22-huang-derivative-range.md` (`d1af9a75b0fbf520…`, **6404 B**) and
`P19-mars-core-light-elements.md` (`58564720345858d9…`, **7076 B**).

#### What gets built

The **eight end points** of the owner's box, S {13, 19} × O {1, 4} × C {0.5, 1.4} wt%, each converted to
atomic mole fractions with IUPAC conventional weights and mixed by **Khan+ 2023's printed recipe** — their
eqs (1)–(2), ideal mixing, `ρ_mix = ρ_Fe + Σ_i ∫₀^{x_i} (∂ρ/∂c_i) dc_i` — on **Huang+ 2023 Table S5's**
derivatives about **Huang Table 1's** two pure-Fe anchors. The S derivative is linear in `c_S` and so
integrates to a quadratic; O and C are constants. ⚠ *Ideal mixing is Khan's own stated assumption for this
range, not ours*, and it is the only printed recipe that uses Table S5 for a multi-component core.

#### The decision lines

- **ⓐ The existing 13 materials stay byte-identical.** The band-end Fe–S materials are not refitted; the
  multi-component ones are **added beside them** (as 179 did).
- **ⓑ Our arithmetic reproduces P21's eight rows.** Two seats, the same printed derivatives, independently.
- **ⓒ Only `S 19 · O 4` reaches Huang's own targets — registered before running.** ⚠ *Reproduced
  independently by the audit seat to the printed digits, with one sharper reading: inside the 5.7–6.3
  g cm⁻³ band at 19 GPa **every row is a 19 wt% S row** — 13 wt% stays above the band (6.339) even with
  oxygen at the top of its range. So what opens the window is not "oxygen and carbon lower it" but
  **the top of the sulphur band, with oxygen needed as well.*** Two of the eight end points land
  **inside** both of Huang's quoted Mars windows (5.8–6.2 g cm⁻³ at 19 GPa, 6.3–6.8 at 35 GPa) —
  **19/4/0.5 → 5.934 and 6.774**, **19/4/1.4 → 5.906 and 6.730** — and a third, **19/1/1.4**, sits **on the
  edge**: 6.2056 against a window top of 6.2, over by **0.0056**, which is below the precision of the
  printed derivatives it is computed from. ⚠ *It is registered as a boundary row, not as a miss.* Every
  13 wt% row misses by a wide margin. **So the top of the sulphur band is required, and oxygen is required
  as well unless the boundary row is read as inside.**
- **ⓓ ⚠ The new materials carry Huang's α and γ so that `has_thermal` is `True`.** Both existing Fe–S
  materials are the **only two of thirteen** with `has_thermal = False`, and their `c_p` and `grad_ad`
  return **0**; the engine already names them through `cold_phases()` (`fe_s_19GPa_c0.2065`,
  `fe_s_19GPa_c0.2901`). Huang prints α = 6.99 × 10⁻⁵ K⁻¹ and γ = 2.74 at the 19 GPa anchor, so the slot
  can be filled from the same table the density comes from.

  ⚠ **Every quantity carries its own source label, and mixing sources inside one material is allowed only
  that way** — the C56 trap is a material whose fit says one thing and whose thermal constants come from
  another without saying so:

  | quantity | source |
  |---|---|
  | ρ, K_T at the two anchors | Huang+ 2023 Table 1 (pure Fe) + Table S5 derivatives, mixed by Khan+ 2023's printed recipe |
  | α = 6.99 × 10⁻⁵ K⁻¹, γ = 2.74 | Huang+ 2023 Table 1, **19 GPa anchor** — the label must say which anchor |
  | `c_p` | P26 finds **one** printed value in this family, the l-FeS end member's **711 J kg⁻¹ K⁻¹**. If it cannot be justified for the mixture, the quantity **refuses by name** rather than borrowing pure iron's |

  ⚠ *A material that cannot fill a slot from print must leave it empty and be named by `cold_phases()`* —
  the refusal is the honest state, and it is the state the two existing Fe–S materials are in.

  ⚠ **Where a zero actually bites was measured, and it is not where it was first supposed.** Three things
  had to be separated:

  1. **`core_state` never asks the material for `grad_ad`.** Its adiabat (`engine/core_state.py@«return t_cmb * (rho / rho_cmb) ** gam»`, which read `** GAMMA_CORE` until 180 B wired it)
     raises the core adiabat with the **module constant** γ = 1.5 and a density ratio. ⚠ *So the material
     holds the slot and the consumer does not ask* — C58's shape exactly, and another instance of C45 (f).
  2. **At Mars the Fe–S materials do not reach that branch at all.** With P_cmb near 19–20 GPa they take
     the `melt_bracket` branch (C60 (c)), where no centre temperature is derived and `center_margin` is
     `None`. A flat adiabat changes nothing there.
  3. **It bites in the structure integrator**, which does use the material's own gradient. Measured at
     cmf 0.24: `fe_prem` puts the centre **51.0 K** above the core-mantle boundary (1960.9 vs 1910.0 K);
     `fe_s_19wt_19gpa` puts it **0.0 K** above — *an exactly isothermal core* — and that isothermal core is
     what `core_state`'s lower-bound branch is handed.

  ⚠ **The "the centre freezes" flip reported alongside this does not survive checking**: it pairs `fe_prem`'s
  melting temperature (2140.6 K at 45.9 GPa) with the Fe–S material's flat adiabat. Against **its own**
  eutectic — 1733.0 K at the same pressure — 2000 K is **+267 K clear** and the verdict stays `liquid`.
  *Two materials must not be crossed to make a verdict.* The prescription is unchanged and the reason is
  different.
- **ⓔ The criterion is not the gap between two optima — it is whether one core mass fraction satisfies
  both axes.** ⚠ *The gap was proposed as the measure and this seat's own sweep shows why it cannot be
  one*: across cmf 0.20 → 0.26 with `fe_s_19wt_19gpa` the radius error falls **monotonically** (11.74 % →
  2.68 %) while the `nmoi` error rises **monotonically** (0.11 % → 1.99 %). Neither optimum is an interior
  minimum — **each is pinned to an end of the admissible range**, and the upper end is set by the 19 GPa
  floor (cmf ≈ 0.26). So the "gap" partly measures where the sweep was cut.

  ⚠ **The direction it was proposed for is nevertheless real**, measured here on a 0.01 grid over
  0.14–0.34:

  | core material | radius-optimal cmf | `nmoi`-optimal cmf | gap |
  |---|---|---|---|
  | `fe_prem` | 0.30 | 0.17 | **0.130** |
  | `fe_s_13wt_19gpa` | 0.29 | 0.18 | **0.110** |
  | `fe_s_19wt_19gpa` | 0.26 | 0.20 | **0.060** |

  ⚠ *But `fe_s_19wt`'s radius optimum sits **on the floor's cut** (≈0.26), so part of that 0.060 is the
  19 GPa reference and not the material* — which is why the "did the floor hide the answer?" column above
  is required, and why the gap is reported rather than judged.

  ⚠ **Today that column's answer is *yes*, and the radius axis alone shows it**: `fe_s_13wt_19gpa` reaches
  **0.375 %** on the radius at cmf 0.29, two steps inside its own cut at 0.31, while `fe_s_19wt_19gpa`
  manages only **2.675 %** at 0.26, immediately under its cut at 0.27. ⚠ **And the direction is the opposite of the tempting
  one**: the material that does better on the radius is the **denser** one (13 wt% S → ρ 7.499, P_cmb
  20.04 GPa) while the lighter 19 wt% (ρ 7.015, P_cmb 19.34) is the one the floor cuts sooner, because a
  lighter core lowers the boundary pressure toward the 19 GPa reference. **So the floor punishes exactly
  the direction the density window wants**, and a multi-component material — lighter still — must be read
  in the same column: an optimum sitting on the cut is the floor's number rather than the material's.

  **The line that can fail:** *does some single cmf put the radius inside 3 % and `nmoi` inside 1 % at the
  same time?* **Today none does** — at 0.26 the radius is inside (2.68 %) and `nmoi` is not (1.99 %); at
  0.20 `nmoi` is inside (0.11 %) and the radius is not (11.74 %). The direction is still the registered
  one: repairing the density should shrink the window between "radius passes" and "`nmoi` passes" until
  they overlap, and `fe_s_19wt` narrowing it against `fe_prem` is the first evidence. **The number to
  report is the overlap, not the gap.**

  ⚠ **And a column is required in the result: "did the floor hide the answer?"** The 19 GPa reference cuts
  cmf above ≈0.26 for `fe_s_19wt`, so its radius-optimal value sits against that edge — and **a lighter
  material lowers P_cmb, which pushes more of the sweep under the floor.** If the optimum lands on the cut
  rather than inside the sweep, the number is the floor's and not the material's, and the low-pressure
  branch (C60's untaken road) becomes the next item.
- **ⓕ No body is wired.** Which material Mars declares is the owner's cell; the seven bodies stay
  byte-identical.

#### Predicted, before running

1. **Only the `S 19 · O 4` corner reaches the density target**, and it reaches it at the top of two bands at
   once. ⚠ **Two quantities must not be mixed here**: Huang's windows are *local* densities at 19 and
   35 GPa, while C55's 5.7–6.3 g cm⁻³ is a **mean core density**. Our engine's 7.5 for the binary is a mean
   over 19–45 GPa against a local 6.9 at the reference, so the mean sits above the local by roughly 0.5–0.6.
   Converted, the best corner should land **near the top of 5.7–6.3 or just above it** — direction only.
2. **Carbon is not a density lever.** Across its full declared band it moves ρ(19 GPa) by ≈**0.06** g cm⁻³
   against sulphur's ≈0.49 and oxygen's ≈0.36. It is in the box because the owner declared it, and its
   value will show in `K_T`, not in ρ.
3. **The radius axis will pass more easily than density**, as in C60 (c) — a larger core is easy to arrange
   and a lighter core is not.
4. **The gap between the two optimal core mass fractions narrows but does not close.** Closing it needs the
   mantle as well, and this brief touches only the core.
5. **`t_melt` stays a refusal for the new materials.** The eutectic curve this engine holds is Fe–Fe₃S; a
   printed melting curve for Fe–S–O–C does not exist in the held set, so a name without a branch must
   refuse (178 C′) rather than borrow the binary's.

### C55 (f) 2026-09-10 — stage 2 built: the floor hides exactly the compositions that would have passed

Built against C55 (e). **ⓐ, ⓑ, ⓓ and ⓕ hold; ⓒ holds on the paper's own windows and fails on ours; ⓔ fails.**

#### ⓑ — two seats, the same printed derivatives, the same numbers

All **eight** end points reproduce the parallel seat's table **to its printed digits**, with **zero**
mismatches: ρ within 6 × 10⁻⁴ g cm⁻³ and K_T within 0.06 GPa at both anchors. The engine's own conversion
(`core_mole_fractions`, IUPAC weights) and its own integration of Huang's Table S5 — S quadratic, O and C
linear — land where the other seat's independent arithmetic landed. ⚠ *The boundary row registered in
C55 (e) is exact*: 19/1/1.4 gives **6.2056** against a window top of 6.2.

#### ⓒ — the corners reach the paper's window and are then cut by our floor

⚠ **Six of the eight corners refuse at Mars's declared composition**, and the two that solve are the two
**densest** ones. The two that land inside Huang's own Mars windows — `S 19 · O 4` — are **exactly the two
the 19 GPa reference cuts**, because a lighter core lowers the core-mantle boundary pressure toward that
reference.

| corner (cmf 0.24) | result |
|---|---|
| `S 13 · O 1 · C 0.5` | ✅ R_core 1712.3 km · ρ̄ 7.320 · P_cmb 19.787 |
| `S 13 · O 1 · C 1.4` | ✅ R_core 1719.1 km · ρ̄ 7.233 · P_cmb 19.662 |
| the other six, including both `S 19 · O 4` | ❌ refused, every one at 18.998–18.999 GPa |

**Lowering the core mass fraction buys some of it back.** `S 19 · O 4 · C 0.5` survives to cmf **0.20**,
and there it gives **ρ̄ 6.661 g cm⁻³**, `nmoi` off by **0.37 %** and the radius off by **10.46 %**; at 0.22
it is cut.

⚠ **So the answer to "did the floor hide the answer?" is yes, and it hides the ones that would have
passed.** The low-pressure branch — C60's untaken road — is no longer one option among two: it is what
stands between this engine and the only compositions that can reach the density window.

⚠ **The two quantities behaved as registered, and the offset is now measured.** C55 (e) predicted that our
**mean** core density would sit above the paper's **local** density at the anchor by roughly 0.5–0.6
g cm⁻³. Measured: the `S 19 · O 4` corner is **5.934 local** and **6.661 mean** — an offset of **0.727**.
So the corner that is inside 5.8–6.2 locally is at 6.66 against our 5.7–6.3 mean window: **outside, and by
much less than before.** Against the binary's **7.5**, the multi-component core closes about **70 %** of
the distance to 6.3.

#### ⓓ — the thermal slot is filled, and filling it has a visible consequence

`has_thermal` is **true** for all eight, with `t_ref` at the anchor's **2100 K**. ⚠ *That pairing is the
whole point*: C56's trap is attaching α while leaving `t_ref` at zero, which heats from absolute zero. The
existing binary materials are **not touched** — they keep `has_thermal = False`, and the new constants live
only in the new builder.

⚠ **And the mixture's adiabatic gradient is large.** At **Mars's core-mantle boundary, 20.65 GPa**, the
eight corners give ∇_ad **0.3101–0.3615** where `fe_prem` **at the same pressure** gives **0.02588** — about
**twelve to fourteen times**. *(An earlier line here compared against 0.055, which is `fe_prem` at 136 GPa;
a gradient must be compared at one pressure.)* Higher up it reaches **0.386**. It is not a mistake — it is
Huang's own derivative doing its work: the light elements soften the alloy so much that K_T falls from
**156 GPa** (pure Fe) to **93.8** (13/1/0.5) and **49.1** (19/4/0.5), and ∇_ad ≈ γP/K_S rises accordingly.

⚠ **And the price of the zero derivative is not one number — it doubles across the box.** The derived γ
runs **1.1706 – 2.0378** against the paper's printed **2.74** for pure Fe: `S 13 · O 1 · C 1.4` keeps 74 %
of it, `S 19 · O 4 · C 0.5` keeps **43 %**. That spread is a direct consequence of holding α and C_V at the
anchor while ρ and K_T move with composition. **The assumption is ours, the label says so, and the label
now has to say how large it is.**

**The melting curve is absent by construction.** Fe–Fe₃S is the *binary* eutectic and no multi-component
curve is in the held set, so `melt` is empty, `melt_free_phases()` names the phase, and a consumer refuses
by that name rather than borrowing the binary's — 178 C′'s rule applied before it could be broken.

#### ⓔ — fails, and the reason is the floor again

**No core mass fraction puts the radius inside 3 % and `nmoi` inside 1 % at once.** ⚠ *An earlier sentence
here said the radius is never better than 8.6 %; that was one cell, not the sweep.* Measured across the box
on a 0.01 grid:

| | best radius | its `nmoi` | where |
|---|---|---|---|
| unconstrained | **3.82 %** | 2.46 % | `S 13 · O 1 · C 0.5`, cmf 0.26 |
| with `nmoi` ≤ 1 % | **6.76 %** | 0.93 % | `S 13 · O 4 · C 1.4`, cmf 0.23 |

So the radius **can** come within 3.82 %, and the moment of inertia is easy on its own (0.11 % at the right
cmf) — **the two are simply not satisfied by the same body**, and the cmf range where the radius would keep
improving is above the cut.

#### What moved that was pinned

⚠ **A registered baseline moved and the guard named it**: `test_fe_s`'s row *"the materials with a
reference pressure are the two Fe–S ends"* (179) is now **ten** — the two binaries plus the eight corners.
The rule it encodes is unchanged, only the count; it is re-pinned as "the liquid cores sitting on Huang's
anchor", and the negative half — *every other phase's `p_ref` is 0* — still holds.

**ⓕ holds: no body is wired.** Which composition Mars declares is the owner's cell, and this brief adds
materials beside the existing ones without touching a body file.

### C60 (d) 2026-09-10 — a finite difference's foothold is a trial step too

⚠ **The same shape as C60, found in a place nobody had walked.** `Material.k_t` differentiates the density
numerically, and its comment already says of the **upper** end that *"the stencil must not poke past the
ceiling and manufacture a refusal"* — the lower end was clamped only to 1 Pa. **Until a material with a
non-zero reference pressure existed, that asymmetry could not be reached.** With the ten Huang-anchored
liquid cores it is reached immediately: at **exactly the reference pressure**, `grad_ad` and `k_t` refused.
Measured: **19.0000 – 19.0019 GPa raise `PhaseGap`, 19.0020 GPa returns a number.**

**The rule C60 registered applies unchanged**: the foothold of a difference is a trial step, and a refusal
it manufactures is not a judgement about that pressure. The stencil is clamped to the material's own floor,
which makes it one-sided there — symmetric with what the ceiling already did.

⚠ **The repair recovers the fit's own bulk modulus**, though the check is weaker than it first looked:
at exactly 19 GPa the one-sided difference returns **K_T = 49.10 GPa** for `S 19 · O 4 · C 0.5`, against the
**49.09** that the same Huang derivatives give analytically. ⚠ *That 49.09 is **our** arithmetic, not a
number the paper prints* — so this says the stencil agrees with the closed form it differentiates, which is
the right thing to check but is not agreement with a publication.

⚠ **"The thirteen original grids stay byte-identical" is true of the density grid only.** The clamp does
not fire where the floor is zero — eleven materials — but the **two Fe–S binaries share the same 19 GPa
floor**, and their `k_t` at exactly 19.0 GPa changed from `PhaseGap` to a number: **100.1707 GPa** (13 wt%)
and **72.6177** (19 wt%). **That is the intended repair, not a side effect**, and `fe_prem`'s ρ(136 GPa) is
pinned unchanged in `test_fe_s`.

### C58 (a) 2026-09-10 — layer 1 is not "constants → declarations" but "constants → what the material returns at (P, T)" — pre-registered before the build

⚠ **Committed before the code.** Reviewed as a scratch draft first (`C58-prereg-draft.md`, sha256
`1c2e474e872ee3b3…`, 11292 B, passed by the audit seat) and moved here **with every number unchanged**;
the language is English because that is what this file is, and the `file:line` pointers of the draft are
**phrase anchors** here because line-number citations are not reproducible. Sources: P17 v4.1
(`4103e440…`, 19957 B), P25, P26, P27.

#### What changes about the design

C58's first plan (P17 v1–v3) lifted the constants baked into the thermal-history integrator into
**per-body declarations**. ⚠ **That was wrong one level up** — those values belong to the **material**, and
`eos.py` already holds the slot. **All twenty-one materials implement `c_p` and `grad_ad`.**

⚠ **Which tables actually print those quantities has to be said narrowly**: **Chabrier, Mazevet &
Soubiran 2019** is held and `hhe_table.py` bakes it with s, c_p and ∇_ad. **The AQUA table is not held**,
and **the Militzer-family papers are behind a paywall and not held** — the code cites those names as the
*source of a curve*, which is not the same as holding a table.

**Layer 1 = a consumer hands the material a (P, T) and gets `c_p`, `∇_ad`, `α` back.** What stays a
declaration is only what a material cannot give: initial temperatures, the surface temperature, the
viscosity law, a `Ra_c` override.

#### 1. Does the material already return it — all twenty-one, measured

| material | c_p [J/kg/K] | ∇_ad | at (P, T) | state |
|---|---|---|---|---|
| `fe_prem` | 448.1 | **0.0245** | 19 GPa · 2100 K | ✅ ⚠ **solid hcp parameters** — §3 |
| `fe_eps` | 453.2 | 0.0500 | 19 GPa · 2100 K | ✅ ⚠ **and that is correct**: `fit_state = solid`, t_ref 300 K |
| `silicate` · `silicate_chondritic` | 1372 | 0.1239 | 19 GPa · 2100 K | ✅ |
| `h_he` | 10519 | 0.2756 | 19 GPa · 2100 K | ✅ (the baked Chabrier+ 2019 table) |
| `h2o_hot` | 5615.4296 | 0.1119 | 19 GPa · 2100 K | ✅ |
| `h2o_liquid_dense` | 3571.1368 | 0.1679 | 19 GPa · 2100 K | ✅ |
| `nh3` | 5271.5831 | 0.1230 | 19 GPa · 2100 K | ✅ |
| `antigorite` · `h2o` · `h2o_liquid` | refuse | refuse | 19 GPa · 2100 K — **outside their domain** | ⚠ the draft's first pass wrote ✅ here: **a table without its conditions cannot be checked, and so it was wrong** |
| the eight box corners | 578.9–641.8 | 0.3096–0.3866 | anchor 19 GPa · 2100 K | ✅ (183 put α and γ in) |
| the same eight | 561.2–619.5 | 0.3101–0.3615 | Mars's CMB, 20.65 GPa | ✅ |
| **`fe_s_13wt_19gpa` · `fe_s_19wt_19gpa`** | **0.0** | **0.0** | **all 30 in-domain cells** | ❌ below |

⚠ **The two binaries do not "fail to return" — they are never asked, and they return 0.** Call `c_p` or
`grad_ad` and a number comes back: **0.0**, at every one of the 30 in-domain cells. It is not a refusal and
not an absence — **a zero is delivered to the consumer.** `has_thermal = False` carries that fact and
**no consumer asks it.** ⚠ *That is C45 (f)'s shape*: a value the contract calls required, filled by a
number the code chose, counted by nothing. **So the registered line is not "fill it" — it is "do not
deliver a zero silently."**

⚠ The only printed `c_p` in this family is P26's l-FeS end member, **711 J kg⁻¹ K⁻¹** (the same number as
Xu's 62.5 J K⁻¹ mol⁻¹ converted), and **its composition is different** — filling from it or refusing by
name is a decision line, not a detail.

#### 2. The consumers — every place a constant stands in

| site | constant | can the material give it? |
|---|---|---|
| `engine/core_energy.py@«C_P = 840.0»` | core heat capacity (Nimmo+ 2004 Table 1) | ✅ `Material.c_p` — ⚠ **1.88× apart**, §3 |
| `engine/core_energy.py@«ALPHA_C = 1.35e-5»` | core thermal expansion | ✅ from `Phase.alpha_k / k_t` |
| `engine/core_energy.py@«L_H = 750.0e3»` | latent heat of inner-core freezing | ❌ no printed per-material value → stays a declaration |
| `engine/core_state.py@«GAMMA_CORE = 1.5 는 h.c.p. **고체** 의»` | the core adiabat's γ | ✅ derivable from `Phase` constants — and the comment itself says it is the **solid** value |
| `engine/cmb_flux.py@«아무것도 그것을 인쇄하지 않았다** — 감사 추적표가 «저장만, 읽는 곳 0» 으로 잡았다»` | was **a second copy** of the literal; 180 B left the name for printing and moved the calculation into the one function | ✅ wired ⚠ **The line this row used to cite no longer exists** — 180 C removed the alias after the audit value-trace found that «the name for printing» printed nowhere (C66). The anchor now points at the comment recording the removal, so the history is here rather than in a dead pointer. |
| `engine/core_energy.py@«GAMMA = cs.GAMMA_CORE»` | a third reference | — |
| `engine/core_state.py@«GAMMA_LIQUID_RANGE = (1.51, 1.52)»` | the **liquid** γ band | ✅ — ⚠ a different value from the 1.5 above, and which one a consumer reads varies |
| `engine/core_state.py@«GAMMA_SPAN = (min(GAMMA_CORE, GAMMA_LIQUID_RANGE[0]), GAMMA_LIQUID_RANGE[1])»` | **mixes those two into one span** | ⚠ one solid value and one liquid band inside a single interval |
| `engine/cmb_flux.py@«K_CORE = 50.0»` | core thermal conductivity | ⚠ **outside C58 — moved to C49** (owner, 2026-09-10) |
| `engine/core_entropy.py@«K_RANGE = cf.K_CORE_RANGE»` · `engine/core_history.py@«K_CORNERS = cf.K_CORE_RANGE»` | two copies of that band | ⚠ **moved to C49**, which takes this consumer list |
| `engine/mantle_flux.py@«C_PM = 1200.0»` | **mantle** heat capacity (eq. 32) | ✅ `silicate.c_p` |
| `engine/mantle_budget.py@«C_P_J_KG_K = 1250.0»` | **a second number** for that quantity | ✅ same |
| `silicate.c_p(19 GPa, 2100 K)` = **1372** | **a third number** for it | — |
| `engine/mantle_flux.py@«RHO_M = 4800.0»` vs `engine/stagnant_lid.py@«RHO_MANTLE_KG_M3 = 4000.0»` | two mantle densities | ⚠ recorded in one line |
| the structure integrator (`_adiabatic_dtdp`) | **uses the material's own** | ✅ already the right place |

⚠ **There are four γ, not three, and none of the four knows about the other three**: the printed **2.74**
is stored and **read by nothing**; the value **derived** from the stored constants, **1.17–2.04** across the
eight corners, drives `grad_ad`; the module constant **1.5** is what `core_state` uses, and its own comment
says that is the h.c.p. **solid**; and the **liquid** band **1.51–1.52** sits beside it, with `GAMMA_SPAN`
folding the third and fourth into one interval. **The resolution criterion: for one core, the consumers
read one γ.** Which value is chosen is the owner's; what this brief closes is that four coexist.

⚠ **And the same shape is in the mantle** — three numbers for one heat capacity (1200, 1250, the material's
1372) and two for the density (4800, 4000). **Repairing only the core leaves the identical defect one layer
across.**

#### 3. `fe_prem`'s thermal parameters are a solid's

`Material.c_p` already implements c_p = c_v(1 + αγT) correctly, but `fe_prem` carries `alpha_k`
**1.21 MPa/K** (Isaak & Anderson 2003, **hcp solid**) and `c_v_ref` **446.6** (Dulong–Petit). At
19 GPa / 2100 K that gives **αγT = 0.00341**, where Huang's **liquid** printed values give **0.4022**
(P25, reproduced here).

⚠ So the answer to "840 versus 447.5" is narrower than "different quantities" — **neither is liquid iron's
c_p.** 840 is a constant Nimmo *assumed* in order to reproduce Gubbins 2003's adiabat (P25 quotes §3.3
verbatim); 447.5 is a **solid lattice** c_v. Huang prints liquid C_V 494/496, which converts to
c_p ≈ 693/664 (our arithmetic).

**Layer 1 replaces `fe_prem`'s thermal parameters with liquid printed values.** ⚠ **`fe_eps` is not
touched** — it is `fit_state = solid`, t_ref 300 K, Seager's Fe(ε), and P27 likewise assigns Dorogokupets's
hcp thermal set; making it liquid would put it wrong **in the other direction**.

⚠ **This moves answers.** Earth's and Mars's core temperatures and the verdicts hanging off them change, so
**naming every value that moves is this brief's output.** If they move quietly, the brief has failed.

#### 4. The decision lines

- **ⓐ Four sites, one function — and where the function cannot be trusted, a named fallback.** All four
  consumers (`core_state`, `core_energy`, `cmb_flux`, the structure integrator) read **one function**,
  `core_gamma(material, P, T)`. It returns the material's γ(P, T) when that material's
  `thermal_source_state` check is **green**, and when the check is **red** it returns the **declared
  constant 1.5** — labelled *"hcp-solid in origin, standing in while no liquid set is adopted"* — which is
  **printed and counted every run** and **emits both numbers as values** — `core_gamma_used`
  (⚠ renamed `core_gamma_cmb` by 180 C, once the same node started asking γ at two pressures) and
  `core_gamma_material`, with `core_gamma_fallback` as the counter. ⚠ *An earlier draft of this line said
  the pair travels in a `recorded_disagreement`; that is a **spec field** read from a body file
  (`engine/run.py@«recorded = spec.get("recorded_disagreement")»`, 177's board comparisons) and **not a
  `Result` field** — `payload.Result` has ten, and that is not one of them. A node cannot put its
  disagreement there.*
  ⚠ **The constant literal lives only inside that function**, and **which materials the function answers
  for is a property of the material, not a list of names** — `role='core'`, carried by the twelve core
  materials. *A name list is the hole that bit first*: written as `CORE_MATERIALS = (…)` it omitted the two
  binary Fe–S materials 178 C had registered, so the function refused them as "not a core material" — and
  `_adiabat` called it without a guard, so a body whose boundary sits **above the 10–21 GPa bracket window**
  went down the declared branch and **crashed the node with an uncaught exception**. Mars did not crash only
  because its 20.65 GPa falls inside the window. Both are repaired: the role decides, and `_adiabat` turns
  a misuse into a named refusal. ⚠ **Candidate, outside 180 B's scope**: `role` defaults to the empty
  string, so a new core material that **fails to declare it** is still a human's job to remember — the
  hole is moved to where the author is already typing, not closed. The check that closes it is *"a
  material the core node accepts must carry `role='core'"*, and it is not built here.

  ⚠ **And a material with no thermal set must not come back green.** `thermal_label` answered `ok` when
  `has_thermal` was false — *"nothing to ask about the source"* — while `core_gamma` computed its γ as
  **0.0**, so the binaries would have delivered **a green verdict carrying γ = 0**, i.e. a flat adiabat.
  *That is §1b's "do not deliver a zero silently", reappearing one layer up.* The verdict is now
  `no-thermal-set` and it routes to the fallback, so those materials get 1.5, get counted, and the fact that
  this family has exactly one printed `c_p` shows up in the verdict.

  ⚠ *Why a fallback rather than unification or refusal.* Wiring the material's own γ today would flip
  Mars's centre to solid: `fe_prem`'s γ is **0.3524** at Mars's core-mantle boundary and **0.2732** at
  Earth's, against a flip point of **0.8722** — a `center_margin` of about **−85 K**, contradicting
  Durán 2022 and Stähler 2021's *"entirely liquid"* and the owner's 174 decision. ⚠ **So the module
  constant is what holds Mars's core liquid today, and the material's own γ would freeze it** — and the
  reason that γ is 0.3524 is that the thermal parameters are the **solid** set, which is the very mismatch
  this brief names. *Four sites disagreeing is therefore not untidiness: one of them is holding up a
  shipped verdict.* And refusing outright would take `core_state` away from every body using `fe_prem`,
  Earth included, breaking the dynamo chain over a label — not a decision this brief may make.
  ⚠ **Unifying three of the four is worse than either**, because `core_energy` and `cmb_flux` import their
  γ from `core_state` and so agree with it by construction today; moving three onto a value we have just
  judged untrustworthy would replace one disagreement with a three-against-one.

  ⚠ **Three sites read the function, and the integrator asks the material directly — a decision now,
  not a delay** (revised 2026-09-11 after 180 C measured what the fourth site costs; owner review pending,
  the revert is one function). `core_state`, `core_energy` and `cmb_flux` take the named fallback when the
  label is red; the **structure integrator uses the material's own γ(P, T) and prints and counts the red
  label** — `integrator_red_gamma_used`.

  ⚠ **Two policies, because the two sites ask different questions.** The integrator asks for a **local**
  γ(P, T) at every step, and a constant there **flattens a quantity that varies** — the material's own γ
  runs **0.9178 → 1.1498** across one core (358 → 118 GPa at 3000 K), and 1.5 everywhere is not a better
  description of that, only a labelled one. The core nodes need **one number at one point** for a
  closed-form adiabat, and there a declared constant with a counter is the honest object. *They become one
  answer the day a liquid set is adopted.*

  ⚠ **Bit-identity with `fbfe6b2a` is impossible for the three bodies that moved, by construction.**
  ⓐ reverts the *wiring* — the integrator asks the material again — but ① changed **the material**:
  `fe_prem`'s phase now carries interval sets, so `Material.gruneisen` is a **different function** than it
  was. At Earth's core-mantle boundary it answers **1.1267** (Dorogokupets, graded) where it used to answer
  **0.2735** (the solid constant). *No wiring choice returns the old core temperatures; the only way back
  would be removing the sets, which is removing the brief.* So the verdict line for ⓐ′ is «the three
  bodies move, each movement named with the set that caused it», not bit-identity.

  ⚠ **What the gap between the integrator and the core nodes became.** It was **5.5×** — the constant 1.5
  against an **unlabelled** 0.2735 — and it is now **1.33×**, 1.5 against **1.1267**, *with both sources
  named* (the declared hcp-solid constant against Dorogokupets+ 2017's liquid equations). **The
  disagreement did not shrink because anything was reconciled**; its nature changed, from «a labelled
  constant against an unlabelled solid value» to «two papers». What remains closes only when a liquid set
  is adopted.

  ⚠ **And at one and the same point, one consumer refuses what the other uses.** `core_state` asks
  `core_gamma` at Earth's boundary, gets `graded-disagreement`, and takes the fallback **1.5**; the
  integrator asks the material at that same pressure and **uses Dorogokupets's 1.1267**. *That is the state
  the counters record: one side declines the number, the other spends it.* Recorded, not resolved.

  ⚠ **And the two counters mean opposite things, by design.** `integrator_red_gamma_used` says *"the label
  was red and that γ was used anyway"*; `core_gamma_fallback` says *"the label was red so it was not"*.
  **Both are 1 on every `fe_prem` body today**, and one counter would have hidden which happened.

  *The 180 B text, kept because its measurement still stands:* three sites, not four, **the structure
  integrator left on its own path for now**, because routing it through the fallback would
  move the core rise from **+51 K** to about **+237 K**, and that shifts the lower-bound input
  `core_state` receives for the **five bodies with no declared T_cmb** by roughly **+186 K** — enough to
  flip a phase verdict, with the owner away. *The reason is time, not design*: the day the label turns
  green all four move together.

  **Today's result: every `fe_prem` body gets 1.5 at all three wired sites — no verdict flips, no new
  disagreement, and the fallback is visible.** ⚠ *The unification is not a no-op in general, though*:
  `fe_eps`'s check is **green**, so it now receives **its own γ at the caller's (P, T)** — **0.6275** at
  Mars's boundary (20.649 GPa · 2000 K) and **0.7653** at Earth's (136 GPa · 3760 K), against the constant
  **1.5**: a factor of **2.4** and **2.0** below it. The only reason nothing moves is that **no roster body
  uses `fe_eps`**.

  ⚠ **An earlier report of this line printed the flip point as 0.8723 and explained a 4.7e-5 shift in it
  as this wiring's effect. Both were artefacts of a hand-run that fed `gamma_flip` pressures rounded to two
  decimals** — 45.90 / 20.65 GPa instead of 45.90016599537648 / 20.648606564786558 GPa. `gamma_flip` is a
  closed form over `density` and `t_melt` and never reaches `core_gamma`, so **this wiring cannot move it**
  (audit seat, 2026-09-10; reproduced here from run output). *Numbers that go into print are read off the
  run, not retyped from a rounded console line.*

  ⚠ **And an earlier draft of this line said 0.2994, "a fifth of the constant" — that was the γ at the
  material's 300 K reference isotherm, a temperature no consumer asks about.** The cause was in the code,
  not the prose: `core_gamma` read `Phase.alpha_k` directly instead of the file's own identity
  `gruneisen`, so it dropped the `alpha_k_dt·ΔT` term that dominates in a metal — at 19 GPa `fe_eps` runs
  **0.2976 → 0.6518** from 300 K to 2100 K. *A γ printed without its (P, T) is the same defect the
  stage-2 check line was given a mandatory condition column for.* The Fe–S family is
  `composition-substitute`, adopted with a named grade, and **no body declares one today** either.

- **ⓑ The centre-minus-boundary temperature is the same number at the three wired consumers**, the
  fallback's number while the check is red. ⚠ **And the fourth gap stays open, reported as a number, not
  as a failure**: the structure integrator gives **+50.98 K** where `core_state` gives **+236.75 K** at the
  same boundary anchor (1909.9501 K, Mars at cmf 0.24) — **4.64×**. *That is a registered open state, and
  it closes on the day the label turns green and the integrator joins as the fourth.*
- **ⓐ′ The adopted set is checked on three quantities, not one.** ⚠ *Checking only C_V would let the very
  quantity that drives the adiabat through unchecked* — and it already disagrees: **Dorogokupets+ 2017's
  liquid γ₀ is 2.033** where **Huang prints γ = 2.74**, **35 % apart**. So the check line is:

  | quantity | condition — **mandatory column** | Huang's printed target | what the candidate set must be evaluated to give |
  |---|---|---|---|
  | C_V | 19 GPa · 2100 K | **494 ± 16** J kg⁻¹ K⁻¹ | Dorogokupets+ 2017 **Table 1 liquid set**, eqs 6–17, at that (P, T) |
  | C_V | 35 GPa · 2400 K | **496 ± 24** | same |
  | α | 19 GPa · 2100 K | **6.99 × 10⁻⁵ K⁻¹** — ⚠ *no uncertainty printed → report the reproduction error only* | ⚠ **not** the set's 1 bar recommended **92 × 10⁻⁶** — eqs 6–17 **raised to 19 GPa** |
  | α | 35 GPa · 2400 K | **5.31 × 10⁻⁵** — same | same, raised to 35 GPa |
  | γ | 19 GPa · 2100 K | **2.74** — ⚠ *no uncertainty printed → report the error only* | the **Table 1 fit set** γ₀ **2.033** with β **1.168** and γ_∞ **0**, evaluated at that (P, T) |
  | γ | 35 GPa · 2400 K | **2.66** — same | same |

  ⚠ **The candidate set prints γ₀ twice and only one of them is ours.** Table 1's fit parameter is
  **2.033**, and the 1 bar *recommended* value is **1.735**; we take **the Table 1 fit set**, because it
  comes as one piece with the equations that use it — **the 1 bar value is a cross-reference column, never
  an input.** ⚠ *The same trap sits on α*: putting the set's 1 bar 92 × 10⁻⁶ beside Huang's 19 GPa
  6.99 × 10⁻⁵ would compare two different conditions, which is why the condition column is mandatory.
  Transcription source: P27 (`f4b9809a7976ae35…`, 14910 B, hashed here).

  ⚠ **Miss any one of the three and the set is not adopted** — the miss is named, and the result goes to
  the owner as *"the two sources disagree on γ."* **Adopting it anyway is forbidden**, because that would
  be electing a number under cover of a check that passed on a different quantity.
- **ⓒ A label check, and the owner chose how.** The source phase of a thermal parameter lives only in
  `Phase.ref`, which is prose, so "source phase ≠ `fit_state`" cannot be judged by code. ⚠ **The decision
  is (a): this brief adds `Phase.thermal_source_state`** (`'liquid' | 'solid' | 'table'`, **no default —
  an undeclared value fails the check**) and the check compares it with `fit_state`. **A check where a
  person reads the `ref` is not accepted**, for the same reason as "do not deliver a zero silently": *a
  source phase must not sit quietly in prose either.* Today `fe_prem` is exactly that case —
  `fit_state = liquid`, t_ref 1600 K, thermal parameters from Isaak & Anderson's **hcp solid**.
- **ⓓ ⚠ No value moves, and that is what gets verified.** Wiring three consumers onto a fallback they
  already held, with the integrator untouched and no roster body using `fe_eps`, changes nothing — so the
  claim is **bit-identity against the four baselines**, not a table of movements. *An earlier draft of this
  line said the opposite ("this brief changes answers"); with the integrator held back it would have had
  nothing to report and no way to fail.* **The seven-body table is the output of the day the label turns
  green and all four move together** — that is the only moment values actually move, and it must then
  cover `core_temperature`, `conductor_phase` and `center_margin` for all seven. **The four comparison baselines,
  each hashed at citing time by this seat:**

  | file | sha256[:16] | bytes |
  |---|---|---|
  | `audit/eos_thermal_05da70ad.json` | `1cf7dbed15230301` | 288194 |
  | `audit/c58_thermal_table_05da70ad.txt` | `0b7fe36525aa9c69` | 1974 |
  | `audit/c58_thermal_mismatch_167ac9ee.txt` | `c76441233760ed6b` | 3458 |
  | `audit/thermal_5e7f6993.json` | `e07977cfd77fd8ed` | 13823 |

  ⚠ **Measured after the build, by the audit seat (2026-09-10): all four hold.** The material grids are
  **byte-identical**, **no existing key moved**, and `core_state` gained **exactly three keys** —
  `core_gamma_used` (now `core_gamma_cmb`), `core_gamma_material`, `core_gamma_fallback` — whose printing, counting and
  both-distances lines were confirmed from run output rather than from this file. The post-build
  fingerprint is `audit/thermal_eec846df.json`, sha256 `74595510730d816c…`, **14287 B**.

  ⚠ **`thermal_<sha>.json` is compared with its `seconds` field excluded** — wall-clock timings differ
  between runs of identical physics, and comparing them would turn every re-run into a false difference.
  *(The thermal node's output has not moved since `3a4f6b37`, so that baseline is a resting state.)*
- **ⓔ Only what a material cannot give stays a declaration**: `L_H`, initial temperatures, T_s, the
  viscosity law, `Ra_c`. If that list shrinks, the reason is written down.

#### 5. The owner's decisions, and the one thing they dissolve

- **The source for liquid `fe_prem`'s c_p, α and γ is Dorogokupets+ 2017's Table 1 liquid thermal set**
  (their eqs 6–17, held in P27's text layer). **Huang 2023's Table 1 is the check line, not the source**:
  its two points — **C_V 494 ± 16** at 19 GPa/2100 K and **496 ± 24** at 35 GPa/2400 K — must be reproduced
  **inside the printed uncertainty** for the set to be adopted. ⚠ *If they are not reproduced, the set is
  **not** adopted and the miss is reported by name* — the check is not decoration.
- ⚠ **"Printed γ versus derived γ" is not a conflict, and the owner's decision dissolves it: γ is one
  function.** It is computed from the paper's γ₀ and its printed rate of change as a function of (P, T),
  so there is nothing to elect. **What remains is that four sites must read that one function** —
  `core_state`'s three (`GAMMA_CORE`, `GAMMA_LIQUID_RANGE`, `GAMMA_SPAN`) plus `core_energy`, `cmb_flux`
  and the structure integrator. *That is decision line ⓐ, and it is now a statement about wiring rather
  than about which number is true.*
- ~~Whether `K_CORE` closes here~~ → **closed: moved to C49** (owner, 2026-09-10), and its three consumer
  sites go with it.

### C58 (a) amended 2026-09-11 — the owner's decisions, and one design constraint they hit

⚠ **Committed before the code, again.** 180 B built the fallback; 180 C is the build that **moves
answers**, so these amendments are registered first and the seven-body table below is the output.

#### ① The liquid thermal set is a pressure split **inside one phase**, not a second phase

**Owner decision (2026-09-11), candidate (iv):** at or below **35 GPa** the set is Huang+ 2023 Table 1's
two measured points (19 and 35 GPa) with the valid interval **declared**; above it, Dorogokupets+ 2017's
liquid set (eqs 6–17) carrying the grade label *"disagrees with the low-pressure measurements by 40 %"*.
⚠ **The discontinuity at the boundary is reported as a number**, not smoothed.

⚠ **And it may not be built as two phases.** `engine/core_state.py@«if len(material.phases) != 1:»`
makes `k0_flip_gpa` answer `None` when a material has more than one phase — *"cannot compute, and says
so"*. Splitting `fe_prem` into a ≤35 GPa phase and a >35 GPa phase would therefore turn a **number into a
refusal** for every body: Earth's flip point **194.005586674557 GPa** would silently become `None`.
*(Audit seat's finding, reproduced here: `interior.solve(1.0, earth_like, cmf 0.325)` → p_c
**358.458095 GPa**, p_cmb **135.275636 GPa**, then `k0_flip_gpa(fe_prem, …, 3760.0)`.)* So the split lives
**in the thermal set inside the single phase**, and `thermal_label` returns a **per-interval** label —
`ok` inside 19–35 GPa, and the graded label above it.

⚠ **One more thing that number shows, and it changes what the baseline means.** At the **structure's own**
`T_cmb` (2526.2085 K on the same run) `k0_flip_gpa` **already returns `None`** — the sign does not change
inside the multiplier range. The 194.0056 figure exists **only at the declared horn 3760 K**. *So the ⓓ
baseline must say which temperature each cell was taken at, or a `None` will be read as this brief's
damage when it is today's answer.*

#### ② The low-pressure Fe–S slot stays empty, by decision

**Owner decision:** candidate (c) — **leave it empty** and wait for Balog+ 2003, which the owner will
fetch. **Code changed by this decision: none.** The refusal below 19 GPa keeps naming itself, and no
extrapolation is added to cover the gap.

#### ⓐ amended — four sites, and the constant becomes a fallback only for "the material cannot say"

The 180 B text reads *"three sites, not four — the structure integrator is left on its own path"*. With
① decided, **the integrator joins**: all four consumers take the material's γ(P, T). The declared
constant **1.5** survives **only** as the named fallback for a material that cannot give a value at the
asked (P, T) — not for a material whose set is merely graded. ⚠ *So the verdict set changes meaning:
`composition-substitute` and the graded high-pressure label now **deliver the material's own γ**, and only
`no-thermal-set` and a domain refusal reach the constant.* That is a widening of what moves, and it is
why ⓓ below is a table of values rather than a bit-identity claim.

#### ⓓ amended — the table of what moves, and a rule for a movement that is not a number

**The output of 180 C is the seven-body table**: `core_temperature`, `conductor_phase` and
`center_margin` for all seven bodies that reach `core_state`, before and after, with **every changed
value named**. Plus the thermal-history fingerprint, since the integrator joins.

⚠ **New rule, from ①'s constraint:** a value that changes from **a number to `None`**, or from `None` to
a number, **counts as a movement and gets named** — the same as a number that moves. *A refusal is an
answer, and a silently vanished number is the worst kind of movement because a diff of two tables reads
it as an empty cell.*

| pre-listed cell | expected | value today, and where it came from |
|---|---|---|
| Earth `k0_flip` at the **declared** 3760 K | **unchanged** | **194.005586674557 GPa** — this file's run, pressures above |
| Earth `k0_flip` at the **structure's** T_cmb 2526.2085 K | **unchanged** | **`None`** today — no sign change in the multiplier range |
| the seven bodies' `core_temperature` · `conductor_phase` · `center_margin` | ⚠ **expected to move** | filled at build time, each change named |
| the thermal-history fingerprint | ⚠ **expected to move** | `audit/thermal_eec846df.json` `74595510730d816c…` · 14287 B is the before |

**What would falsify each line:** a `k0_flip` differing from the two cells above; a body whose
`conductor_phase` changes without appearing in the named list; a fingerprint that does **not** move
(which would mean the integrator did not in fact join).

### C58 (b) 2026-09-11 — 180 C built: the liquid set arrives as a pressure split, and it reaches exactly the interval it was measured in

Built against **C58 (a) as amended 2026-09-11**. ⚠ **Decision lines: ① built with one change of effect
(below) · ② built as «nothing» by decision · ⓐ built with one measured exception · ⓓ is the table at the
end.**

#### ① The split lives inside one phase, and the reason is a number

`fe_prem`'s single phase now carries **two `ThermalSet`s for γ and c_p** — `[19, 35)` GPa from Huang+
2023 Table 1's measured liquid Fe, and `[35, ∞)` from Dorogokupets+ 2017's liquid equations
(`engine/fe_liquid.py`, new). **The density path does not read them** (decision (A)): the phase keeps its
PREM adiabat reference, so no density, radius or moment of inertia moves. That asymmetry is a **partial
repair** and `Phase.thermal_label` now returns **two cells** — γ side and density side — which
`core_state` emits as `core_gamma_verdict` and `core_gamma_density_path`, with
`core_gamma_partial_repair` counting the bodies where they disagree.

⚠ **It is not two phases, and the cost of getting that wrong is a number**:
`engine/core_state.py@«if len(material.phases) != 1:»` makes `k0_flip_gpa` answer `None` for a
multi-phase material, so a two-phase split would have turned Earth's flip point **194.005586674557 GPa**
into a silent refusal.

**The identity closes on the paper's own printed value** — α·K_T/(ρ c_V) at the 19 GPa anchor gives
**2.7309** against Table 1's printed γ **2.74** (−0.3 %). *That is the check that licensed attaching the
set: no new constant was invented, the file's own identity reproduces what Huang printed.*

#### ② The low-pressure Fe–S slot: nothing built, by decision

Owner decision (c): leave it empty and wait for Balog+ 2003. **Lines of code changed: zero.** The refusal
below 19 GPa keeps naming itself, and — measured — that is also where `fe_prem` falls back to its own
solid constants, so **no extrapolation covers the gap in either material**.

#### ⚠ The effect of the owner's (iv) is narrower than (iv) reads, and this is the difference

Owner decision ① chose candidate (iv): *the measured set below 35 GPa, Dorogokupets above it with a
grade label.* Built and measured, the graded set **turned three of Earth's registered literature checks
red**: T_c 4559 K against Sinmyo+ 2019's 5120 ± 390 K (**10.95 %**), inner-core boundary **240 GPa against
PREM's 328.85 (−27.0 %)**, and ⚠ **`k0_flip` 194.0056 GPa → `None`** — the cell C58 (a) had pre-listed as
*expected unchanged*, contradicted within the hour by the rule the same amendment added.

**Why:** evaluated at Huang's **own** 35 GPa point, Dorogokupets's γ is **1.3987** against Huang's printed
**2.66** (**−47.4 %**) while density agrees to 0.5 %. ⚠ *The set is 47 % off at the only pressure where a
comparison exists, and Earth's entire core lies above that pressure.*

**So the directing seat decided (2), owner review pending:** `graded-disagreement` **does not deliver a
value**. It is printed as the candidate in `core_gamma_material`, counted by
`core_gamma_fallback`, and `_gamma_note` prints **why** it did not deliver. The effect of ① is therefore
**«repair inside the measured interval, candidate outside it»** rather than (iv) as written.
⚠ **Reverting is one line** — the verdict tuple in `eos.core_gamma`; and then the three Earth cells above
are what ⓓ must carry.

**The discontinuity at the boundary is printed as two numbers** (`eos.gamma_set_boundary_jump`): what a
consumer sees, γ **2.7402 → 1.5000 (−45.3 %)**, and what the two papers say, **2.7402 → 1.3987
(−49.0 %)**. *The second is the size of the revert.* Nothing smooths the join, because smoothing invents a
value that appears in neither paper.

#### ⓐ Four sites — and one exception that only measuring found

The structure integrator joined: `interior._core_or_own_gamma` routes a `role='core'` material through
`eos.core_gamma`, passing **its own local ρ** (γ ∝ 1/ρ, so re-measuring the cold density there would give
two γ at one point).

⚠ **The exception: a material with no thermal set keeps the integrator's own rule.** The first cut sent
`no-thermal-set` materials to the fallback 1.5, and that **broke the integrator's first sentence — «do not
invent a slope».** The two binary Fe–S materials have no printed c_p, so they had been **isothermal**
inside the integrator (γ = 0); the fallback turned them adiabatic and **moved two of C55 stage-2's shoot
verdicts.** The tests caught it. `no-thermal-set` is exactly the name that distinguishes «a set exists but
mismatches this fit» (fallback) from «there is no set» (invent nothing), and it now decides which.

#### A performance defect made and fixed inside this brief

`fe_liquid.volume_at`'s first version inverted P(V) with **200 bisection steps**, and γ is asked once per
integration step — one `core_state` run went past **two minutes**. *The answer was right and unusable.*
Newton with a bisection safety net: **2000 evaluations in 0.04 s**, values identical to the last printed
digit (γ 1.3987 · ρ 8598.9 at 35 GPa/2400 K).

#### ⚠ The liquid set's γ does not respond to temperature

Measured while explaining the thermal-history movement: `core_gamma(fe_prem, 20.649 GPa, T)` returns
**2.8718195876825363 at 2000, 3763 and 3900 K** — the same number. Two reasons stack. Huang's Table 1
prints **no `(∂αK/∂T)_V`**, so `alpha_k_dt` is 0 where the solid set had a second-order term that
*dominates* in a metal (180 B measured `fe_eps` moving 0.2976 → 0.6275 between 300 K and 2000 K); and
`core_gamma` takes ρ at **`t_pot = 0`**, which for a phase referenced to an adiabat is the cold density,
so the density in the denominator does not move with T either.

⚠ **So the repaired γ is a constant per pressure, not a function of state** — better than the solid
set's value but flat where the physics is not. *That is the same shape as C67* (a single exponent where
the material now has structure), one layer down: the material's γ varies with **P** and not with **T**,
and both facts come from what the paper printed rather than from a modelling choice. Recorded here so
the next reader does not mistake the flatness for a claim.

#### ⚠ Refreshing a fingerprint erases the check that just fired — so the refresh is measured

`test_ice_giant` failed exactly one row after 180 D: **the path fingerprint**, with every value row
passing — *"Neptune — the whole solve in 60 s (56 s when frozen): radius, C/MR², central temperature and
central pressure identical to the bit"*, and the same for Uranus, plus the grid-phase, grid-refinement and
perturbation-invariance rows. **That is the direct evidence for C60's rule**: the bracket and the pass
count are trial machinery, and changing them did not move an answer.

⚠ **But re-freezing the fingerprint deletes the only signal that a path changed**, so the moment of
refreshing is the only chance to look (audit seat, 2026-09-11). Measured per item — the fingerprint is one
hash over **7 functions + 13 constants + the interpreter version**, so each was hashed separately in a
clone of `61374a86` and in this tree:

**21 items · 2 changed** — `fn:shoot` `2ec97ee94d80` → `0fe6809abf52` (the pass-budget extension and the named refusal) and `fn:solve` `92976fff9143` → `50219a4d45e2` (the two new counter values). *Both are functions this brief edited.*

⚠ *Nothing else on the watch list moved*: not `_shoot_pressure`,
`_narrow_bracket`, `_surface_temperature_met`, `_stack` or `integrate`, and not one of the thirteen
constants — `T_PASSES` included, because the extension refills the budget at run time rather than raising
the constant.

⚠ **But "21 items · 2 changed" is a statement about the watch list, not about the code** (audit seat,
2026-09-11, reproduced independently). `PATH_FUNCTIONS` holds **seven** names, and the two functions this
brief actually changed are **not among them** — `interior._adiabatic_dtdp` (edited: it now routes core
materials through `core_gamma` and passes `p` to `dpdt_v`) and `interior._core_or_own_gamma` (**new**).
And `_feed_code` hashes `co_code`, `co_names` and nested code objects — *it does not follow calls*, so
`integrate` calling `_adiabatic_dtdp` puts the **name** in the hash but not the body.

⚠ **That gap is narrower than it first looks, and the reason is worth stating** (the audit seat raised the
gap, then narrowed it itself). **The fingerprint's job is the path change that does *not* move a value**;
the net for changes that *do* move values is the test's **assertion 1** — *"the whole solve is identical to
the frozen values to the bit; a change in the equation of state, the Fermi integral, the integrator, the
stacking, the shooting or the temperature loop is caught here"*. 180 C/D's γ edits are the value-moving
kind, and they **were** caught — by `test_core_history`'s three Mars anchors and by the three moved bodies
in the ⓓ table. On the ice giants nothing moved because those bodies use no `role='core'` material, so the
γ change is a **no-op for them**: there was nothing to detect, which is different from failing to detect.

**The licence to re-freeze therefore comes from the value assertions** — two bodies bit-identical in
radius, C/MR², central temperature and central pressure, plus grid refinement and perturbation
invariance — **and the two nets overlap**, so "21 items · 2 changed" is a statement about the watch list
sitting beside a statement about the values. ⚠ *The residual risk C70 keeps is the thin one: an edit to
`_adiabatic_dtdp` that leaves the frozen convergence point's values untouched and changes only the path.
That is the only shape that slips both nets — and it is exactly the shape a fingerprint exists for.*

#### ⚠ And the gate caught what my test choice did not — 180 D

`gate235` (pool 2, on `61374a86`) failed one step: **`test_ice_giant.py`**, with
`TypeError: dpdt_v() takes from 2 to 3 positional arguments but 4 were given` inside Uranus's solve.
**The cause is this brief.** `interior._adiabatic_dtdp` now calls `ph.dpdt_v(t, t_pot, p)`, and the ice
giants' phases are **not `eos.Phase`** — the four table-backed phases take `(t, t_pot)` only.

⚠ **The four core tests could not have caught it**: every material they touch is a `Phase`. *A consumer
that calls without knowing which phase it holds is a place where adding an argument must be tried on
every phase kind*, and the test that does that lives only in the gate (`test_ice_giant`, `test_giant`) —
because **the roster has no ice-giant or sub-Neptune body**, so nothing in the fast path exercises those
phases.

**Repaired in 180 D** by giving the four table phases the same signature, with the argument **named
`_p_unused`** rather than commented: the day an interval set is attached to one of them, a name that says
"not read" is what stops it becoming a quiet fallback. **`61374a86` is not pushed** — the gate's verdict
belongs to the sha it ran on, and the repair is its own commit so that «the gate caught this» stays in
the history rather than being amended away.

#### Housekeeping folded in

- `cmb_flux.py`'s `GAMMA = CORE_GAMMA_FALLBACK` was a **dead alias** 180 B left as *"a name for
  printing"* that nothing printed (audit value-trace, 2026-09-11). Removed. Its twin in
  `core_energy.py` is **listed as C66**, not touched.
- Gate pool: `GATE_POOL` default **8**. Measured on one commit, three ways: **serial 34.5–44.7 min ·
  pool 2 20–22 min · pool 8 12 min 8 s** (gate234, 71 steps, PASS 682, peak RSS 57 MB). The floor is
  `test_giant`; quiet mode is `GATE_POOL=2` in the environment.

#### ⓓ The table — what moved, on which body, and by which mechanism

Measured by running the whole chain on all seven body files in this tree and in a scratch clone of
`fbfe6b2a` (the commit 180 C is built on), and diffing eleven keys. ⚠ **Three of seven bodies move, and
the two mechanisms are different** — one is the repair, the other is the unification.

| body | key | before (`fbfe6b2a`) | after | mechanism |
|---|---|---|---|---|
| **mars** | `core_gamma_used` → **`core_gamma_cmb`** | 1.5 | **2.8718195876825363** | ⚠ **the repair** — its CMB (20.649 GPa) is inside Huang's measured 19–35 GPa. ⚠ *The key is **renamed** by this same brief: `core_gamma_used` no longer exists, because a name meaning "the one that was used" became false the moment two sites could disagree* |
| mars | `core_gamma_center` | *(key did not exist)* | **1.5** | ⚠ **new key** — the centre 45.9002 GPa is in the graded interval, so the **fallback** is what the adiabat integrated |
| mars | `core_gamma_verdict_center` | *(key did not exist)* | **`graded-disagreement`** | new key — the verdict at the site that made the verdict |
| mars | `core_gamma_split` | *(key did not exist)* | **1** | new key — the two sites disagree, and the disagreement is counted rather than hidden |
| mars | `core_gamma_fallback` | 1 | **1** | ⚠ **the counter does not move, and an earlier draft of this row said it went to 0.** That draft was written from the CMB alone and was **refuted by this brief's own repair**: the fallback *is* used, at the centre, so «either site fell back» keeps the counter at 1. *A table that had shipped with the 0 would have said the opposite of the code* |
| mars | `core_gamma_material` | 0.3524492201745824 | 2.8718195876825363 | the material's own value is now the liquid set's |
| mars | `core_temperature` | 1960.9323053004 | **2225.6515648290306** | +264.7 K |
| mars | `entropy_production` | −8401236.288184777 | **−37726881.15867804** | ⚠ **4.49×** more negative — C15's φ reads this γ |
| mars | `cmb_temperature` | 1909.9501164449248 | 1909.950123378215 | +6.9e-6 K (K_S now asks the set) |
| mars | `q_cmb` | 365535766.62836087 | 365535733.32694596 | −9.1e-8 relative |
| **earth** | `core_temperature` | 2671.0924780458163 | **3169.5267230925806** | ⚠ **+498.4 K, and the cause is the graded set — not the unification.** *An earlier version of this row read +845.9 K and blamed the fallback; that was measured while the integrator went through `core_gamma` (the join, reverted on 2026-09-11). With the integrator asking the material again, the number it gets at Earth's boundary is **Dorogokupets's 1.1267**, not the old solid **0.2735** — **4.1×** — because ① changed the material itself* |
| earth | `core_gamma_material` | 0.2734673094085167 | 1.1266901786462618 | the material's own γ **is** the graded set now, above 35 GPa |
| earth | `cmb_temperature` | 2526.2085475146446 | 2526.2086058586447 | +5.8e-5 K |
| earth | `q_cmb` | 2749973604443.4155 | 2749973698461.779 | +3.4e-8 relative |
| **pandora** | `core_temperature` | 2474.3298155983525 | **2902.1981495526247** | +427.9 K, same cause as Earth (the graded set at its boundary, γ **1.2126**) |
| pandora | `center_margin` | −1772.3694996941963 | **−1344.501165739924** | +427.9 K — ⚠ a verdict margin moved by 428 K, and it moved **toward** the melting curve |
| **mars** (`core_thermal_history`) | `t_c` at present, adaptive H 1.5 | 3893.07 | **3905.34** | ⚠ **+12.27 K — found by the gate, not by this table.** `core_history` does **not** pass through the structure integrator; it calls `cmb_flux` and `core_energy`, and **those ask `core_gamma` at p_cmb**, which for Mars is inside the measured interval — so ① moved this trajectory directly |
| mars (`core_thermal_history`) | `t_c` at present, declared H 0.088 | 3763.10 | **3780.60** | +17.50 K, same cause; step count **1197 unchanged** |
| mars (`core_thermal_history`) | `t_m` at present (both branches) | 1382.90 · 1377.03 | 1383.78 · 1377.96 | +0.88 · +0.93 K |
| mars (`core_thermal_history`) | `t_m` at 3.7 Ga, declared H | 1668.00 | **1668.79** | ⚠ **+0.79 K, and it eats headroom**: criterion B's distance to Herzberg's 1673.15 K upper edge goes **5.15 → 4.36 K**. C20 already recorded that band as *"a 5 K error anywhere in the trajectory flips this"*, so this movement is **toward the edge** and is named for that reason, not for its size |
| pandora | `core_gamma_material` | 0.2944463614060906 | 1.2125984260169187 | the graded set |
| **sub-Neptune `GJ 1214 b`** (test body) | `converged` · `radius` | **True** · **2.7674024618153776** | **True** · **2.7791897274983373** | ⚠ **Two sentences, both true.** *The answer came back* — 180 C's first cut lost it to a wall refusal (14682 K · 2.65 R⊕ · 246 K), and reverting the join returned it; ⚠ **the recovery is the revert alone**, identical with and without the pass-budget extension (R 2.7791897274983373 · T_c 11396.293824433487 either way). *And the agreement got slightly worse*: against the published **2.733** the distance goes **+1.26 % → +1.69 %** (the radius itself moved **+0.43 %**). **Recovering an answer is not the same as improving it**, and the label on the γ that produced it is still `graded-disagreement` |
| **water-rich rocky, `imf 0.3`** | `converged` · `radius` | **True** · **1.258513071917607** | **True** · **1.25852361765906** | recovered (**+0.00084 %**), ⚠ **and the split runs attribute it**: with the revert alone it is `converged False` at R 1.2584557449170426; **the extension is what produced the answer** (audit seat, two isolated clones, 2026-09-11) |
| **water-rich rocky, `imf 0.1`** | `converged` · `radius` | **True** · **1.1312792111770278** | ⚠ **a named refusal** | *"the surface-temperature condition did not close inside the budget — last deviation **3.09 %** (tolerance 0.1 %), **28** passes, **1** extension"*. ⚠ **The cause is the graded set, not the unification and not the liquid set in general**: this body's core runs **p_cmb 132 · p_c 354 GPa**, entirely above 35 GPa, so **Huang's measured set never reaches it** and Dorogokupets answers — 1.1267 against the old 0.2735, **4.1×**, which steepens the core adiabat until the proportional update oscillates about a root it cannot reach. ⚠ **And the same set is refused by `core_state` (graded → fallback 1.5) while the integrator spends it.** The value that would have been shipped is the **last trial**, which moves when the budget moves (+0.0033 % when passes were added), so it is not shipped. Tracked as **C69** |
| **the pass-budget extension, measured alone** | five keys on the six bodies that converge either way | — | **bit-identical** | ⚠ **`radius`·`nmoi`·`core_temperature`·`core_pressure`·`cmb_pressure` all identical across GJ 1214 b · dante_fixture · earth · mars · pandora · water `imf 0.0`** — *and this control does not lean on the C56 identity*, because `core_temperature` matches too (3169.5267230925806 on both sides). **So the extension is trial machinery: it does not move an answer.** |
| **what the extension actually bought** | `imf 0.1`'s output | `applicable True` · `converged False` · R **1.130250786008135** | ⚠ **`applicable False` — a named refusal** | ⚠ **The better half is not the extra convergence but this**: without the extension the engine hands back a **non-converged radius as a value**, and a consumer that does not read `converged` uses 1.13025 as an answer. *That is the shape this ledger has fought all week — «do not deliver it quietly» — and the extension replaced it with a refusal that names itself.* |
| **water-rich rocky, `imf 0.0`** (control) | `converged` · `radius` · `core_temperature` | True · **1.0029682364205592** · 2671.0924780458163 | True · **1.0029682364205592** · **3169.5267230925806** | ⚠ **The radius is bit-identical and the core temperature is not** — +498.4 K, the same graded-set movement as Earth (this body *is* Earth's mass and core fraction). ⚠ *And the bit-identical radius is **not** evidence that the pass-budget extension leaves answers alone*: `fe_prem` is referenced to an adiabat at `t_ref` 1600 K, so at `t_pot` 1600 K the C56 identity makes `delta_t` exactly zero and this composition's radius is insensitive to the core temperature. **The control shows less than it looks like it shows.** What the extension does to a converged answer is measured by **separated runs** — extension-only against ⓐ′-only — which the audit seat is running |
| **alpha_centauri_a_b · dante_fixture · luhman_16_a · luhman_16_b** | — | — | — | **no key moved** |

⚠ **Earth's and Pandora's movement is the integrator taking the named fallback where it used to take an
unlabelled red value.** Before this brief the structure integrator asked the material directly and got
**0.2735** (Earth) and **0.2944** (Pandora) — the *solid* hcp constants on a liquid fit, the very mismatch
C58 exists to name — and it used them without a label or a count. Now `role='core'` materials go through
`core_gamma`, the verdict is red, and the **declared 1.5** arrives instead. *That is a 846 K and 649 K
movement produced by labelling, not by new physics*, and it is what 180 B deferred when it held the
integrator back.

⚠ **Earth's core temperature moved toward its own declaration** (2671 → 3517 K against the declared
3760 K), and this is **not** read as a verification: the lower-bound branch is not the declared branch,
and no literature number was consulted in producing it.

⚠ **Mars's φ moved 4.49×** and stays negative, so C15's band still straddles zero and the item's verdict
is unchanged — but the number a future consumer would read changed by a factor of four and a half, from
one γ label to another.

⚠ **`conductor_phase` moved on no body**, and neither did `center_margin` on Earth or Mars — the declared
branch asks γ at the **centre** pressure, and the centres that reach this node are all above 35 GPa where
the graded set does not deliver. **So the shipped liquid/solid verdicts are all unchanged**, which is why
this brief could land with the owner away.

⚠ *And the reason has to be stated per body, because one body breaks the short version.* Measured central
pressures: earth **358.4580952308751** · pandora **237.64826743155024** · mars **45.90016599537648** ·
**dante_fixture 0.31717986058738007 GPa** · alpha_centauri_a_b · luhman_16_a · luhman_16_b **None**. So
"every roster centre is above 35 GPa" is **false for `dante_fixture`**; that body is unchanged because
`core_state` is out of domain for it, not because of its pressure (audit seat, 2026-09-11). *The day a
low-pressure core reaches this node, the sentence as first written would not have protected it.*

#### ⚠ The defect the audit found in the printing, and what it says about the counter

`core_state` asks for γ **twice at different pressures** and only printed one of them:
`_gamma_values` asked at **p_cmb**, while `_adiabat` — through `_center_temperature` — asks at **p_c**.
Before the pressure split those were always the same verdict, so nothing showed. **Mars split them**: its
CMB 20.6486 GPa is inside the measured interval (γ **2.8718**, `composition-substitute`) while its centre
45.9002 GPa is in the graded interval (γ **1.5**, `graded-disagreement`, candidate 1.3587).

⚠ **So the fallback was used and the counter said 0, and the note's first line said the material's own
value was used.** That is the exact failure this whole item exists to prevent — *a fallback going quiet* —
reproduced inside the brief that was built to prevent it, on the one body the brief was for.

Repaired by **naming the split rather than hiding it**: `core_state` now emits `core_gamma_cmb` and
`core_gamma_center` with a verdict label each, `core_gamma_split` is **1** when the two verdicts differ,
and `core_gamma_fallback` is **1 if either site fell back**. The note prints both numbers, both verdicts,
and the sentence *"the adiabat that made the verdict used the centre's γ"*. ⚠ *The key `core_gamma_used`
from 180 B is renamed `core_gamma_cmb` — one commit old, and the name was wrong the moment two sites could
disagree.*

**Registered against C58 (a) ⓓ:** the pre-listed cells hold — Earth's `k0_flip` is
**194.005586674557** at the declared horn and **`None`** at the structure's own T_cmb, and **both are
unchanged before and after**; the thermal-history fingerprint moves, as registered, because the
integrator joined.

⚠ **And the same rounding trap appeared again in the same cell.** Feeding `k0_flip_gpa` the pressures
**as printed** (`358.458095` / `135.275636` GPa) gives **194.0055846744**, not 194.005586674557 — a
difference in the seventh digit, from re-typing a console line instead of passing the solve's own floats.
*That is yesterday's 0.8722/0.8723 in a different cell, one day later, in a number this brief
pre-registered.* Both trees were measured with the same rounded literals, so the «unchanged» verdict
stands; the full-precision figure is the one printed here.

### 185 (a) 2026-09-11 — the Fe–S bracket's upper edge is not a eutectic, and it is not even inside the window — pre-registration draft

⚠ **Written before the code.** Li, Fei, Mao, Hirose & Shieh 2001 (*EPSL* **193**, 509,
[`2001E&PSL.193..509L`](https://ui.adsabs.harvard.edu/abs/2001E&PSL.193..509L)) is now **held in full**
(owner, 2026-09-11), so row 10 of P16's source table leaves **abstract grade for primary**. Source:
`P16-fe-s-melting-10-21gpa.md` at its **final version**, sha256 `f2164f6a2328d4a6…`, **53887 B**, hashed
at citation time. ⚠ *The file moved four times while this brief was written — Amendment 5
(`a8b0b95e0f4fc4bf…`) is what it was first written against, 6 fixed the 7 GPa attribution, 7 restored the
disagreement against its right partner, and the last one closed the thread. The version cited is the
final one and the numbers below were re-read from it; the earlier hashes are listed so that a reader who
finds one of them knows where it sits in the sequence.*

#### Two defects in one constant, and they point the same way

`engine/eos.py@«IRON_FES_WINDOW_HIGH_POINTS = (»` held `((21.0 GPa, 1348.0), (25.0 GPa, 1473.0))` **before this brief** and fed
`IRON_FES_BRACKET_K = (1023.0, 1473.0)`, which `iron_fes_eutectic_bracket` returns for **every** pressure
in 10–21 GPa — Mars's 20.65 GPa included. *(The anchor above points at the constant as it stands after the
repair; the pair it used to hold is quoted here because the citation cannot point at a line that no longer
exists — the same rot this ledger hit twice yesterday.)*

1. ⚠ **1473 K is not a eutectic temperature at any pressure.** It is the **upper end of Li's
   experimental range**, and Table 1 shows what happened there: at 8.5, 10, 14 and 25 GPa the 1473 K runs
   have **liquid present** (S_liquid measured). A temperature at which the sample was partly molten is a
   **ceiling on** the eutectic, not the eutectic. *What the body actually brackets at 25 GPa is
   `1373 < T_eut ≤ 1423 K`* — no liquid at 1223 and 1373 K, liquid at 1423 K.
2. ⚠ **And it is worse than "the point is outside the window" — the upper edge is not an in-window value
   at all** (audit seat's measurement, 2026-09-11). The window is tested as `lo <= p < hi`, so it is
   **[10, 21)**, and **both** old high points lie outside it: 21 GPa is the exclusive upper bound and
   25 GPa is far beyond. The only printed points **inside** are the three lower-lineage eutectics —
   15 GPa/**1023**, 18.5/**1073**, 20.6/**1123**. So the constant's own comment, *"the lowest and highest
   printed values **inside the window**"*, was false at the top: the highest in-window value is **1123 K**
   and the edge read **1473 K**, **350 K above it**. The bracket was **450 K wide where the in-window data
   support 100 K**, and the whole excess came from outside the window.

*Neither defect needs the new paper to be seen — the second is arithmetic on the constant's own comment.
The paper is what makes the first one certain.*

⚠ **And the first defect is verified against the PDF, not the transcription** (this seat, 2026-09-11):
`docs/phase3/_papers/2001E_PSL.193..509L.pdf`, sha256 `7f55355a05ac17a7e2d742a9…`, 384349 B. Table 1's own
columns read P = 7 · 8.5 · 8.5 · 10 · 10 · 14 · 20 · 25 · 25 · 25 · 25 GPa against T = 1223 · 1473 ·
1473 · 1473 · 1473 · 1473 · 1273 · 1223 · 1373 · 1423 · 1473 K, with S_liquid printed for every row
except the two marked *"No liquid. Sulfur-bearing solid iron coexists with Fe₃S"* — which are exactly
25 GPa at **1223 and 1373 K**, while 1423 K has liquid at 23.1 at.%. *So «1373 < T_eut ≤ 1423 K at
25 GPa» is the table's, and P16's transcription is exact.*

#### What Li 2001 adds inside the window — three ceilings, one of them informative

| P | T | what it is | effect on the bracket |
|---|---|---|---|
| 10 GPa | 1473 K, liquid present | ceiling | loose — far above the lower lineage |
| 14 GPa | 1473 K, liquid present | ceiling | loose |
| **20 GPa** | **1273 K, liquid present** | ceiling | ⚠ **the informative one** — it puts T_eut at 20 GPa **at or below 1273 K**, between Andrault's 20.6 GPa/1123 K (lower lineage) and Fei 2000's 21 GPa/1348 K (upper, still quoted second-hand) |

⚠ **It narrows the 21 GPa disagreement from above without resolving it.** 1273 K is a ceiling, not a
determination, so the two lineages still disagree by ~225 K and this brief does **not** choose between
them — that is P16 §4's owner-pending line and it stays open.

#### ⚠ The 7 GPa "disagreement" does not exist — the two numbers were at different pressures

An earlier version of this draft recorded a **~40 K disagreement** at 7 GPa between Li's liquid-at-1223 K
and *"Fei 1997's eutectic ≈ 1261 K"*. **There is no disagreement.** Both seats went to the PDF
(`1997Sci...275.1621F.pdf`, sha256 `cb3ea81deb87a6e0…`) and Fei prints the eutectic as a **line**:
*"The eutectic T linearly decreased with increasing P, from **988 °C at 1 bar** to **860 °C at 14 GPa**"*
(p. 1621). So **1261 K (988 °C) is the 1 bar value**, not a 7 GPa value; reading the line at 7 GPa gives
924 °C = **1197 K**, which is **26 K below** Li's ≤ 1223 K ceiling. *The two papers agree, and the
ceiling did its job.*

⚠ **Recording a disagreement that does not exist would have been worse than missing one** — the next
person would have tried to resolve it. What actually went wrong is one thing: **the number travelled
without its condition.**

⚠ **But the ~40 K disagreement at 7 GPa is real — its partner is Buono & Walker 2015, not Fei** (audit
seat, 2026-09-11; verified in P16 row 7 by this seat). That paper's abstract, held at result grade, reads
*"The Fe-FeS system maintains a eutectic temperature of **990 ± 10 °C to at least 8 GPa** if starting
materials and pressure media are rigorously dehydrated. **Literature reports of pressure-induced freezing
point depression of the eutectic for the Fe-FeS system are not confirmed.**"* — i.e. **1263 ± 10 K at
7 GPa** against Li's ceiling **≤ 1223 K**. So the withdrawal above must be **an attribution fix, not a
withdrawal of the disagreement**: the number was compared to the wrong paper, and the right paper
disagrees by about the amount originally claimed.

⚠ **The lineage split is not our inference — it is a printed table.** Buono & Walker 2011
(`2011GeCoA..75.2072B`, **held in full**, sha256 `8cf466cc5d1a7c82…`) prints, under *"Eutectic data:
6 GPa"*, **five** sources at **one** pressure: this study **1263 ± 25**, Morard+ 2007 **1140 ± 170**,
Fei+ 1997 **1206**, Ryzhenko & Kennedy 1973 **1263 ± 15**, Usselman 1975 **1259 ± 12** — a spread of
**123 K** in a single table (verified in the PDF by this seat). *So "the literature disagrees in this
window" is a quotation, not a reading* — and with five rows the shape is sharper still: **three cluster
at 1259–1263, Fei sits alone at 1206, and Morard is 1140 ± 170.**

⚠ *P16's transcription of that table listed **four** rows, dropping Usselman 1975 — and this brief
carried that count until the number was checked against the PDF. The audit seat recorded the miss as its
own (it had relayed our own document as if it were the paper); P16 now carries an erratum. **The spread,
123 K, and Fei's 1206 K are unchanged**, and the method check below is now against the paper rather than
against our transcription of it.*

⚠ **And that table validates the method used above.** Reading Fei's own line at 6 GPa gives
988 − 128·(6/14) = 933.14 °C = **1206.29 K**, and B&W 2011 prints Fei's 6 GPa value as **1206 K** —
agreement to **0.29 K**. *The same arithmetic at 7 GPa gives 1197.15 K, so the number this brief uses is
produced by a method the literature checks at the neighbouring pressure.* That is what licenses calling
the 7 GPa figure «our arithmetic on the paper's own word "linearly"» rather than an invention.

⚠ **And B&W contradicts the falling half of the slope argument itself.** This draft uses *"Fei falls to
14 GPa, Li rises to 25 GPa, so the sign turns inside the window"* as a reason for a bracket; B&W prints
that the reported depression **is not confirmed**, with a condition — *"if rigorously dehydrated"* —
which is the same place as the hydrogen-contamination reading `eos.py` already cites B&W for. ⚠ *The two
B&W papers do different jobs here and both are cited: **2011** supplies the composition polynomial and
the 6 GPa comparison table (held in full), **2015** supplies the flat-to-8-GPa eutectic and the
dehydration condition (abstract only). Neither is the bracket's edge; they are why the edge is a bracket.* **The
verdict does not change** (7 GPa is outside the 10–21 GPa window, and Mars is `liquid` under every
candidate); what changes is that the reason for a bracket rather than a curve gets **one layer
thicker**. *That is the same failure as reading a paper's introduction value as its result,
and as comparing `fe_prem`'s γ at 136 GPa against a mixture at 20 GPa — three times in two days, always
the number arriving without the condition attached.*

⚠ **And Fei's line stops at 14 GPa.** The same paper says Fe₃S₂ changes the system from *"a simple binary
eutectic system to a binary system with an intermediate compound that melted incongruently"*, so it
**cannot be extrapolated to 20 GPa**. Fei is not a comparison in the window's upper half — which is
itself an argument for a bracket rather than a curve. Only the printed endpoints are kept
(`IRON_FES_FEI_LINE_C`).

#### The repair, and the decision it needs

**Every point in the two tuples gets a label** — `eutectic` · `liquid-present ceiling` ·
`experimental range` — so that a point can no longer enter the bracket without saying what it is. That
part is not a decision.

⚠ **The decision is which value the upper edge takes**, and the candidates are:

| # | candidate | the bracket at Mars's 20.65 GPa |
|---|---|---|
| (i) | drop the 25 GPa point; the edge is Fei 2000's **21 GPa / 1348 K** (still second-hand) | (1023, **1348**) |
| (ii) | adopt Li's **20 GPa / ≤ 1273 K** ceiling as the edge — the only in-window primary-grade upper constraint, ⚠ **and a reversal run** (Table 1's ᵃ: heated higher, then cooled), so the label travels with the number | (1023, **1273**) |
| (iii) | keep two edges and print both — «second-hand 1348 · primary ceiling 1273» | two bands, consumer compares against both |
| (iv) | ⚠ **the 25 GPa point stays but becomes the table's own tighter number, 1423 K** (audit seat, 2026-09-11): MO535 has liquid at **1423 K** and LO140 none at **1373 K**, so the same table brackets that pressure to **50 K** — 1473 K (LO95) was *the looser of two ceilings in one table*. It is out of window either way, so it does not set the edge; it is **recorded** where it belongs | unchanged — but the discarded 1473 K is replaced by a **narrower printed value**, so «do not throw a printed number away» is satisfied rather than bent |

⚠ **A fourth option exists and is worse, and saying why is part of the decision.** *"Use the in-window
maximum, 1123 K"* looks like the honest reading of the comment — but all three in-window points are
**lower-lineage** eutectics, so adopting their maximum as the ceiling **chooses the lower lineage**, which
is the one thing this bracket exists not to do. The ~225 K disagreement is owner-pending; a ceiling that
resolves it silently is worse than a ceiling that borrows the window's edge.

⚠ **Using 1348 K therefore spends one assumption, and it is named**: that the eutectic curve **rises with
pressure**, so a value at the window's edge bounds the window's interior. The sources' figures point that
way and the curve is **kinked**, not straight — so it is written down as an assumption rather than left
implicit.

**The band whose verdict moves, and whether anyone is in it.** `iron_fes_phase_verdict` says `liquid`
only above the upper edge, so lowering 1473 → 1348 turns **(1348, 1473) K** from `cannot-say` into
`liquid`; under the 1123 option the band would be **(1123, 1473) K**. ⚠ **No roster body is in either
band**: not one body declares an Fe–S core (both declare `fe_prem`), and Mars's core-side temperatures —
**1909.95 K** structure, **2000 K** declared — are above every candidate ceiling, so the verdict is
`liquid` before and after. *Contradicted by:* any body's Fe–S verdict changing, which would stop the
brief.

⚠ **Decided (directing seat, 2026-09-11; owner review pending, revert = one tuple): the upper edge is
the labelled out-of-window point, 25 GPa / 1423 K** — candidate (iv) promoted from "recorded" to "the
edge". It is the **narrower** of the two ceilings the same table prints, it is **primary grade**, and — the
reason that settles it — ⚠ **1423 K is the narrowest primary-grade ceiling that still contains the
1348 K of the upper lineage.** Sort the candidates: in-window maximum **1123** · Li's in-window ceiling
**1273** · the 21 GPa lineage **1348** (second-hand) · Li's 25 GPa **1423** (primary, with 1373 as its
own lower side) · the experimental range's top **1473** (not a eutectic at all). The bracket's second job
survives only while the upper edge sits **above 1348**, so 1123 and 1273 would **silently reject the
upper lineage** rather than decline to choose — and above 1348 there is exactly **one** primary-grade
printed value. *So the slack — the window's own eutectic runs about 1133–1273 K — exists to contain
1348, and that is the answer to "why not narrower".* ⚠ *The sign of the slope also flips inside this
window: Fei falls from 988 °C at 1 bar to 860 °C (1133 K) at 14 GPa, while Li rises from ≤ 1273 K at
20 GPa to (1373, 1423] at 25 GPa — the turn sits where Fe₃S₂ and Fe₃S become stable, which is why this
interval is a bracket and not a curve.* (i)'s 1348 K stays in the
code as the recorded alternative; (ii)'s 1273 K stays as the in-window primary ceiling, printed
alongside. The bracket becomes **(1023, 1423)** at Mars's 20.65 GPa, the verdict-flip band narrows to
**(1423, 1473] K**, and Mars is `liquid` on both sides of the change.

*(The paragraph below is the earlier draft's reasoning for (iii); it is kept because the decision above
rests on the same principle — do not throw a printed number away — and because the revert path is this
paragraph's option.)*

**This seat's earlier default: (iii)**, because it is the only one that does not throw
away a printed number, and because the item's whole shape is *"the sources disagree, so return a bracket
rather than a curve"* — collapsing two upper constraints into one repeats at the top edge the mistake the
bracket exists to avoid at the bottom. ⚠ **Labelled as the seat's default, owner review pending, revert =
one tuple.**

#### Registered before running

1. **Mars's printed band moves.** `cmb_melt_bracket_high` goes from **1473** to whichever candidate
   lands; `cmb_melt_bracket_low` stays **1023**. *Contradicted by:* the low edge moving, or the high edge
   not moving.
2. ⚠ **The verdict must not flip, and this is the check that says so.** Mars's core-side boundary
   temperature is **1909.95 K** (structure) / **2000 K** (declared), both **above every candidate
   ceiling**, so `iron_fes_phase_verdict` stays `liquid`. *Contradicted by:* any body's verdict changing;
   if one does, the brief stops and reports rather than shipping it.
3. **`test_fe_s.py@«20.65 GPa (화성 CMB) → 괄호»`'s pinned `(1023.0, 1473.0)` is a registered baseline
   and it moves** — the new value is named in the ledger, and the test is re-pinned in the same commit as
   the code, never before it.
4. **Row 10's grade goes `abstract` → `primary`** in P16's provenance, and the ledger says which sentence
   that grade now rests on (Table 1, not the abstract's range).
5. An outcome outside 1–4 is registered as its own kind before it is reported.

#### Two rules this brief adopts about its own new constants

1. ⚠ **A constant that was never committed was not "removed".** The disagreement above briefly had a
   constant, `IRON_FES_7GPA_DISAGREEMENT_K`, written during 185 and taken out in review. It **never
   shipped** — `61374a86` has neither a definition nor a reader for it — so **no baseline moved**, and the
   ledger says «born and withdrawn», not «deleted». *Saying «deleted» would send the next reader looking
   through the history for a constant that was never there — the same shape as citing a hash for a version
   that no longer exists, twice today.*
2. ⚠ **Every new record-only constant gets a reader in the same commit.** Today's value-trace counted
   **seven** constants nothing reads, and three are from this family — printed values kept "for the
   record". So `IRON_FES_OUT_OF_WINDOW_BRACKETS` and `IRON_FES_FEI_LINE_C` are **read by the
   out-of-window refusal**: `iron_fes_phase_verdict`'s *"cannot-say"* string now carries the 25 GPa
   printed bracket and the pressure range Fei's line actually covers. ⚠ **No verdict changes** — only
   what the refusal says. *A refusal that names what does exist nearby is a different thing from one that
   implies nothing does.*

#### What this brief must not do

1. ⚠ **No interpolation between points.** The sources draw this interval as a **kinked** line (Fe₃S₂
   stable near 14 GPa, Fe₃S near 21 GPa); a straight line through them would be our arithmetic on top of
   a shape the papers deny. *Contradicted by:* `iron_fes_eutectic_bracket(p)` returning a value that
   **varies with p** inside the window.
2. ⚠ **It must not choose between the two lineages.** The ~225 K disagreement is owner-pending and stays
   so; this brief only stops a **non-eutectic** number from acting as the ceiling. *Contradicted by:* the
   bracket becoming a **scalar** instead of a 2-tuple — that is what choosing looks like in code.

   ⚠ **And narrowing is not choosing, but it can stop showing** (audit seat, 2026-09-11). The 225 K is
   **1348 − 1123**: the gap between the out-of-window 21 GPa point and the highest in-window point. The
   bracket has been doing **two jobs** — enclosing the in-window printed values *and* carrying the
   lineage disagreement — and fixing the first can silently drop the second. So the decision table above
   carries that consequence explicitly: **(ii) at 1273 or the in-window 1123 leaves the 225 K with no
   home in the bracket, and then it needs a named one** (its own constant or label); **(i)/(iii)/(iv)
   keep the upper edge above the lower lineage, so the bracket still spans the disagreement.** *This
   seat's default (iii) keeps it — 1023 to 1348 contains both lineages, which is the property the bracket
   was built for.*
3. ⚠ **It must not use the paper's actual subject.** S in solid iron (0.09–0.26 at.% at 7–14 GPa rising
   to 0.8–1.4 at.% at 25 GPa) is a quantity the engine **has no slot for**; it goes on the coverage map,
   not into a constant. *Contradicted by:* any constant carrying an at.% value appearing in the code.
4. ⚠ **It must not touch `iron_fes_eutectic_t_melt`** (the single value above 21 GPa) — different
   pressure range, different sources, and the 25 GPa point's removal does not change what that function
   answers. *Contradicted by:* that function's output differing before and after on a grid above 21 GPa
   (bit-identity is the check).

### 196 B 2026-09-13 — the liquid Fe–S density fit answers above its anchors, and the answer now carries the grade

**Built, commit `b6040e98`.** `Phase` gained `p_graded_above` · `p_measured_max` · `graded_reason` and
a `density_reach(p)` that returns one of `ok` / `graded-extrapolation` / the beyond-measured case with
the sentence that explains it; `Material.density` calls it, and a module counter `DENSITY_REACH` tallies
the asks. For the two Fe–S binaries the three pressures are **35 GPa** (above both anchors, 19 and 35),
**254 GPa** (`MORI_FES_P_MEASURED_MAX`, the number in Mori+ 2017's own title) and **350 GPa**
(`MORI_FES_P_MAX`). ⚠ **The ceiling is not this density fit's number** — it is the pressure Mori's paper
itself extrapolates to when it states the ICB temperature, and the reach sentence says so rather than
implying the fit was measured that far.

**The backflow is the point.** `interior.solve` snapshots the counter before shooting, prints the two
deltas beside the answer, and **downgrades the regime label to `analog`** when the answering structure's
centre pressure sits above the anchors. ⚠ *The counts include discarded shooting attempts; what carries
the grade is the answer's own centre pressure, and the note says which is which.*

⚠ **Its gate needed three runs, and only the third is a verdict.** The first was **killed by the host at
68 of 72 steps** with free pages at 5 613 (≈ 88 MB) — a machine state, not a judgement on the tree. The
second was stopped by this seat when the directing seat ruled the retry should go at pool 2. The third,
at pool 2, reached `GATE END` with `rc=0`. *Recorded because a killed gate and a failed gate look the
same in a log and are not the same fact.*

### P33 B 2026-09-14 — Fe–S answers below 19 GPa at model grade, and the refusal floor moves to 1.5 GPa

**Built overnight 2026-09-13/14 against the pre-registration `7bb23dd8448120ab`.** Below its 19 GPa
anchor the liquid Fe–S slot used to refuse outright. It now answers from a second phase built on
**Balog+ 2003** (`2003JGRB..108.2124B`), whose measurement-only BM3 on liquid Fe–10 wt % S **revealed
K0T = 64.3 GPa, K00T = 4.7** with 5.5 g cm⁻³ at 1 atm over **1.5–17.5 GPa**. The composition axis is
**ours**: the ρ₀ of a 13 or 19 wt % mixture is obtained by integrating Huang's printed ∂ρ/∂c between
mole fractions, and that chain rule is recorded in the code as our arithmetic, not the paper's. The
phase therefore ships at **grade `model`**, with a second band inside it — at or below 17.5 GPa the
sentence says «inside what the measurements carry», above it «past the measured interval, the fit's own
reach» — and `FE_S_MODEL_ASKS` counts both.

**What the acceptance measured** (all four printed by the build, not asserted in prose):

| # | check | measured |
|---|---|---|
| ① | no roster body moves | the six control bodies' **30** printed cells are bit-identical, and the count of compositions that select an `fe_s_*` core is **0**, so **0** roster bodies reach the reopened window |
| ② | the refusal shrinks exactly where intended | over 42 C55 cells (2 materials × 21 core mass fractions) the floor refusals go **9 → 0**, the other refusals **15 → 0** and the answered cells **18 → 42**, the control printed in the same run |
| ③ | pinned anchors hold | both binaries' Huang cells (ρ(19 GPa) 6900.851694586217 · 6380.181979270691) and all **8** quaternary materials are bit-identical; `c55_cells.py`'s whole table diffs clean |
| ④ | printed digits outside the window unmoved | `fe_prem` ρ(136 GPa) 9916.93698295698, `fe_eps` 11566.81899540878, both binaries at 35 GPa unchanged; of 48 engine tests only the Fe–S trio changes, the rest differ by wall-clock seconds or by a gitignored paper cache the comparison tree lacked |

**Its gate**: one run, `GATE END rc=0`, 02:23:58 → 02:59:16 at **pool 2 — not comparable with a pool-8 run**; the pool was chosen by the free-pages rule, START **7 263** free pages and END **221 298**. All 72 `[COST]` lines printed and **0** sat below 1e8 instructions retired.

⚠ **Adding a phase re-pointed a reader, exactly where a comment had predicted it.** 196 B's note in
`interior.solve` said in writing that its `phases[0]` read leaned on «a material that carries the
declaration has one phase», and that a later multi-phase material **with the declaration on a rear
phase** would make the line read the wrong one. P33 B is that case: with Balog in front, the graded
label for an Fe–S core **vanished silently**. Measured with the control in the same run — a Mars-mass
body with an Fe–S core at centre pressure **48.83 GPa** printed **0** grade notes before the repair and
**1** after. The line now selects the phase whose domain contains the centre pressure, and falls back to
the last phase whose floor is below it, because `phase_at` may raise and a label site must not.

⚠ **The same read exists five more times in `core_state.py` and is *not* repaired here.** There
`phases[0]` means «the fit that answers at the core», and for the two binaries it now returns Balog's
K₀ (64.3 GPa for both, where the two used to print 100.167873788 and 72.614874943) while
`k0_flip_gpa`'s one-phase guard turns its number into «not computed». **No shipped digit moves** — no
composition selects these materials — so it is written up as a candidate row rather than fixed inside
this brief: the obvious patch would also re-point `silicate` and `h2o`, which **do** reach that node,
and that has to be measured before it is changed.

### C90 2026-09-14 — the mirror reads the ledger, and the tool moves into the repo

**Built against the pre-registration `2d20de0d19cd6196` (434 lines, amendments 1–6).** The core-items
page's statuses were a hand-typed literal; the sha in its masthead was **an argument, not evidence
that anything read that ledger**. The generator of record now lives at **`engine/tools/core_items.py`**
— in the repo, beside `refresh_board_rows.py` — and reads the item table out of the ledger at the sha.

**What it reads, declared in the script**: the ledger at the sha, and **nothing else** — the page
header is embedded in the file. ⚠ *The old generator opened `board-0908.html`, an untracked scratch
file beside it, and when that file was cleaned away the canonical tool could not start at all.*

**How the table is found**: by its header row `| # | what it is | state | next step, if open |`,
refusing unless that line occurs **exactly once**. ⚠ **The row-pattern net is the wrong one** — it
also matches the dynamo-hole table further down, whose rows are `C14`–`C19` **as graph edges**.
Measured at this commit: strict net over the whole file **97**, loose **104**, inside the table
**91**, distinct **91**.

**How a status becomes a chip**: one phrase table of **29 rules**, printed into the page, each with a
priority. ⚠ **First-word classification is forbidden** — the status cells' first words run to about
thirty tokens, several of them prose. Of the 91 rows, **30** match more than one rule and **11** have
rules pointing at *different* chips — `C4` · `C21` · `C38` · `C41` · `C46` · `C50` · `C55` · `C57` ·
`C58` · `C59` · `C74`, exactly the partial-closure and closed-but-remains rows the table exists for.
*A tie is not an error; an unprinted tie is.*

**Two refusals, fired rather than inspected**: an injected unmappable phrase exits 1 naming the row
and the phrase; an injected duplicate id exits 1 naming the id and both line numbers. ⚠ **And the
real one** — at `6a9b3622` the item table still held `C82` **twice**, so the generator refused on the
true tree before the merge below.

⚠ **Acceptance ① could not be «diff 0», and that is the finding.** Against the hand-corrected page the
generated chips agree everywhere except **four rows** — `C60`, `C79`, `C80` and **`C90` itself**, whose
row this commit flips to «built» while the page still prints 미착수; in the first three the ledger says
`built …` and the page printed 닫힘. **The page now follows the ledger.** ⚠ *The fourth is this commit's
own description, not a defect — the mirror and the ledger disagree until the page is published again,
and saying so is what the item asks for.* (The audit seat measured **4** on the committed state; an
earlier **3** was read before the row was flipped, and the tie count moved 31 → 30 in the same edit,
because «listed … candidate» matched two rules and «built …» matches one.) *Demanding zero would have
assumed the hand page was right, which is the assumption this item exists to remove.*

**The ledger defect it found, fixed in the same commit**: `C82` occupied **two rows** of the item
table with two different status cells. They are merged into one, keeping the fuller status and the
**union of both bodies** — the shorter row carried seven facts the longer did not (the 11.62 GPa
wedge and its endpoints 342.18 / 353.82, `Trace.note`'s `setdefault` behaviour, and `bracket_invalid`
twice as 189's first real customer). *Keeping «the longer row» would have deleted a measurement and a
named defect.* Row counts by sha, read through the header: `b6040e98` 91/90 · `6a9b3622` 92/91 · after
the merge **91/91**.

⚠ **Committed before the re-clearance.** The C90 build (`d43b9e4c`, **03:15:38**) landed while
`engine/interior-core.md` was still being re-read. The committed pair is **`a54fc5c1` (`6a9b3622`) →
`08bddf7b` (`d43b9e4c`)**; the blob the audit seat cleared at **03:14**, **`1eec7786`, is a worktree
blob that was never committed**, and its **4 / 30** reading was a disk read of a file that had already
moved. The re-clearance came **post hoc at 03:16**, and the gate had started before that line arrived.
*One root: a blob named from a stale read, and a build that did not wait for the name to be re-taken.*
⚠ **`1eec7786` never entering a commit is the evidence, not a gap in it** — a blob that exists,
carries a reading, and belongs to no tree is exactly what «the file moved under the reader» looks like
afterwards. *The rule both seats now work to: a blob is named only after re-hashing it on the spot,
and every hash set carries the time the hash was taken.*

**And the tool proves it can start**: `git ls-tree -r <sha>` lists `engine/tools/core_items.py` (⑦a),
and `git archive <sha> | tar -x` into an empty directory runs it there to a finished page on the
unpacked tree alone (⑦b/⑧). ⚠ *That is the acceptance none of the output comparisons could make —
every one of them asks whether the page is right, and none asks whether the program can begin.*

#### Two more rules, and a template for the third (2026-09-14)

**⑥ 표본은 모집단의 말로 쓰이지 않는다. 세어진 수가 오면 그 위에 적은 문장을 다시 읽는다.** ⚠ *사례*:
`fe_prem` 의 탈락 210 점에 대해 **손으로 찍은 두 점**이 둘 다 `graded-disagreement` 였고, 그래서
「두 판정이 함께 나온다」고 적혔다. 전수로 세니 **`phase-mismatch` 180 · `graded-disagreement` 30** —
지배적인 것은 상(相) 쪽이고 그게 네 배 넘는다. ⚠ **두 문장 다 거짓이 아니고, 쓸 수 있는 것은 둘째뿐이다** —
표본은 「무엇이 있는가」를 말하고 모집단은 「무엇이 얼마나」를 말하는데, 앞의 말투로 뒤를 적으면 읽는 쪽이
비율을 짐작한다.

**⑦ 줄번호는 이름 붙인 줄만 색인 인쇄해서 인용하고, 같은 인쇄에 아는 줄을 대조로 넣는다. 본 목록의
기억에서 인용하지 않는다.** ⚠ *사례 둘, 같은 밤 같은 항목에서*: 줄번호 둘을 고치는 문장이 그 안의 곁가지
하나를 한 칸 밀어 틀렸고(`:68` 은 `stalled` 초기화가 아니라 `for node in computable:`, `stalled` 는
`:67`), 같은 모양으로 「`coupled_core` 가 16 이니 `len(unit) > 1`」이라는 핀은 **선언**에 대한 사실이지
러너의 `unit`(`engine/run.py@«for unit in order(g):»` 가 낸 컴포넌트)과 같은 물건이 아니었다.
⚠ **고장은 한 칸이 아니라 방법이다** — ④ 의 자 다섯 칸이 「같은 것을 다른 자로 읽는 것」을 닫았다면,
⑦ 은 「같은 자리를 기억으로 가리키는 것」을 닫는다.

**③ 의 보내는 꼴** — 확인 뒤에 나간 해시에는 **바뀐 문단을 그 자리에 인용해 함께 보낸다.** ⚠ *해시 한
줄만 보내면, 그 해시가 가리키는 것이 저장되지 않았을 때 남는 것이 아무것도 없다.* **규칙 ③ 이 처음으로
값을 했다**: C86-2 에서 확인 10:20:36 → `build_graph_page.py` 한 줄 편집 10:21:50 → 커밋 10:22:17 로
재확인 없이 지나갔고, 워크트리 블롭 `8d7dbb40` 은 커밋에 안 들어가 `git cat-file -t` 가 «fatal: Not a
valid object name» 을 답한다. **그런데 보내는 쪽이 두 판의 문단을 다 인용해 두어 복구 비용이 0 이었다** —
하루에 네 번째 안 풀리는 블롭(`1eec7786` · `d508e092` · `63a4f89a` 다음)이면서 **처음으로 값이 안 든
것**이고, 차이는 인용된 문단 하나뿐이었다.

#### The process record this item is named after

> ⚠ **Committed before the re-clearance.** The C90 build (`d43b9e4c`, **03:15:38**) landed while
> `engine/interior-core.md` was still being re-read. The committed pair is **`a54fc5c1` (`6a9b3622`)
> → `08bddf7b` (`d43b9e4c`)**; the blob the audit seat cleared at **03:14**, **`1eec7786`, is a
> worktree blob that was never committed**, and its **4 / 30** reading was a disk read of a file that
> had already moved. The re-clearance came **post hoc at 03:16**, and the gate had started before
> that line arrived. *One root: a blob named from a stale read, and a build that did not wait for the
> name to be re-taken.*

⚠ **`1eec7786` never entering a commit is the evidence, not a gap in it.** *A blob that exists,
carries a reading, and belongs to no tree is exactly what «the file moved under the reader» looks
like afterwards.*

### C86 2026-09-14 — the graph page is regenerated, and the generator says what it reads

**Built against the pre-registration `0951d8ec0487fc05` (167 lines, amendments 1–2).** The committed
`engine/chain-explorer.html` was **five edges behind** the graph it claims to draw — 205 against
`chain.yaml`'s 210 — and still printed a node name the graph no longer has. Seven `chain.yaml` commits
had landed since the page was last written (`0c494b05`, 2026-09-09), and **no check compares the two**.

**Regenerated with `engine/build_graph_page.py` at `d43b9e4c`.** Measured after the run: the page
holds **51 nodes · 210 edges**, `chain.yaml` holds **51 · 210**, the node sets are equal, and the
`has_inner_core_solved` name occurs **0** times where it occurred twice — counted as *occurrences*,
because the page is one long line. `has_inner_core` and `inner_core_branch_taken` each occur once.

⚠ **The equality is a measurement, not an identity.** The generator keeps only
`[e for e in edges if e["from"] in nodes and e["to"] in nodes]`, so «page edges = graph edges» holds
only while **0** edges are dropped — which is what it is today. *An equal pair of numbers with a
silent filter behind it is C90's mirror in another costume, right by accident.* **210 is not the
acceptance**; the graph as read at the commit's own sha is.

**And the generator now declares what it reads** — `engine/chain.yaml`, `engine/bindings.yaml`,
`phase4/*.yaml` and the page it writes. ⚠ **The third lies outside `engine/`** — `phase4/*.yaml`, **7** files at this
sha — and that is the input the archive proof is about. *The declaration is a sentence about the
program; the program itself is unchanged, and the diff shows that.*

⚠ **And the failure mode is worse than the one on record.** The proof was run twice, and ⚠ **the sha
matters in the first line**: the **full** archive unpacked into an empty directory reproduces the
committed page **byte for byte** — measured on a throwaway commit carrying these same three files,
**not** on `d43b9e4c`, where regenerating gives a page of a different size from the committed one —
**105 902 bytes against 103 696** (in characters, 92 567 against 90 858; both files are 358 lines),
and that difference is what C86 opens. ⚠ *Two seats read those sizes as 105 902 and 92 567 and spent a
round reconciling them: one counted bytes, the other characters, and **both were right**. Sixth unit
collision of the night, after the hash tool, two lengths, the tree state, the frozen state and the
time a hash was taken — which is the whole argument for writing the ruler beside the number.*
*That difference is C86 itself*, and byte-identity is a property of the tree **after** this
regeneration lands, never before it;
the **`engine/`-only** archive ⚠ **does not die. It writes a page** — `rc=0`, with the
shipped-value counts silently at zero (**179** occurrences of `"n": 0` at this sha, where the full
tree gives `9` in those places). *A tool that dies names its missing input; this one answers with a
quieter graph, and that is the stronger reason for the declaration.* **Measured twice, independently,
on 2026-09-14 — by this seat and by the audit seat.** ⚠ **The earlier statement that the `engine/`-only
archive died on a missing `bindings.yaml` is withdrawn by the seat that made it**: that crash came
from a different attempt which unpacked only four files, and the two runs had been reported as one.

**PALEOS, recorded where it touches this work**: the due-diligence read is P40 (`e7e0f7f5171cf5be`) and the comparison is P41 (`a0b23bfcc58bbbc3`, bound to its results file `51eb6bc895a02b31`). *They are artifacts, not repo documents, and the hashes are how they are cited.*

⚠ **The row stays open, and the second half is now two items.** C86 named two halves — the page
drifts, **and nothing checks it**. This commit fixes the first. What is left: **(1)** a check
comparing the committed page against `chain.yaml`, and **(2)** a generator that **refuses when a
declared input is missing** instead of emitting zeros — the second was not visible until the archive
proof above ran it without `phase4/`. There is no check comparing the committed page against
`chain.yaml`, and the three that run today skip it by construction: `check_refs`'s live set is `{.py, .yaml, .md}`,
`check_contracts` reads `chain.yaml` and `bindings.yaml` rather than the page, and
`check_build_freshness.py` looks at `docs/phase2`·`docs/phase3` and `db/systems`. **Until that check
exists the page will drift again from the next `chain.yaml` commit onward.**

### C88 2026-09-14 — the anchor re-freezes on its inputs, and the comparison reads all 21 keys

**Built against the pre-registration `2bfaf71aca408494` (96 lines, frozen), owner's choice C + D.**
The snapshot's trigger was the path fingerprint alone, so a change to a table or a data file left it
untouched; the comparison was `BIT_KEYS` — **4** of the **21** value keys the file already held.

**The trigger now reads the inputs.** `refresh()` writes a `sha256` prefix for every file the solve
reads, and the check compares them: **20** files watched, **19** hashed (the anchor itself is watched
by existing rather than by value, because it cannot carry its own hash). ⚠ **The list is walked, not
typed** — the tool parses `import` statements from two seeds (`test_ice_giant`, `interior`), keeps
what resolves to a file inside `engine/`, and prints every module with its depth beside the counts.

⚠ **The hand-written list was one hop short, and the walk found the file it missed.** The first build
carried a typed chain of 17 modules; the audit seat walked the imports transitively and found
`water_hot` doing `from fermi import …`, and `fermi.py` carries **frozen tables of its own**
(`FD_M12`, `_LN_M12`). *A table the solve reads, whose change moves the anchor, watched by nothing —
the exact shape this item removes.* The measured closure is **18** modules: 2 seeds, **11** at depth
1, **5** at depth 2 with `fermi` among them. ⚠ **Depth is a number about the seeds** — this seat's two
seeds put `fermi` at depth 2; the parallel seat's single seed put the same file on the same path at
depth 3. *A depth without its root is a length without its unit, which is this night's own lesson
landing in the very column built to show a boundary.*

⚠ **`registry` is watched but not expanded, and the excluded set is measured too.** Eighteen node
modules hang below it — `bands` · `body_class` · `cmb_flux` · `core_energy` · `core_entropy` ·
`core_history` · `core_state` · `domain` · `dynamo` · `dynamo_rocky` · `mantle_flux` · `mass_radius` ·
`provisional` · `radiogenic` · `tectonic_regime` · `tidal_heating` · `tidal_locking` ·
`tidal_response` — and **the anchor calls `interior.solve` directly without walking the node graph**,
so watching them would over-fire until «an input changed» meant nothing. **18 watched + 18 excluded =
36 unfolded**, and the run prints all three. ⚠ *Counting `registry`'s **direct** imports and calling
that the fan-out gives 13 and misses five that arrive through them.*

**The comparison now reads what the file holds**: **21** keys per body, counted from the snapshot,
plus the six-key `standalone` block and `standalone_reproduces_solve`. Measured on the re-freeze —
Uranus **0** moved keys of 21, Neptune **0**, standalone **0** of 6, the flag `True` on both.

⚠ **Acceptance ⑥ asked what the widening bought, and today's honest answer is «nothing yet»** — 0 of
the 17 extra keys moved on this re-freeze. *Registered before the build precisely so that answer
could be printed rather than quietly dropped.* **The price is written down too** (⑤): the freeze
costs **25.7 s** for Uranus and **59.6 s** for Neptune, and the check re-solves both.

⚠ **The first run of the widened comparison fired eight false positives, and the cause is worth the
row.** `refresh()` stores floats through `repr` and everything else raw; the comparison wrapped every
key in `repr`, so each non-float key — `ice_column_state`, `silicate_melt_state`, `voids_expected`,
the two integrator verdicts and three more — compared unequal against itself. **The widened
comparison's first risk is not a missed change but a false alarm**, and the fix is that both sides go
through one function.

**Three injections, fired rather than inspected**: touching `porosity.py` (depth 1) and `fermi.py`
(depth 2, the file the hand list missed) each make the check demand a re-freeze; touching
`dynamo.py` — ⚠ **a file that really is among the excluded eighteen** — leaves it quiet. *Without the
third the first two are a tautology; with it, «node modules are not triggers» is shown by touching
one rather than by saying so.* And the refusal fired on real data before
any injection: the pre-C88 snapshot has no `inputs` block at all, so the check said so and named it.

### The five process rules, and why they sit under C90

⚠ **Written 2026-09-13/14, each attached to something that actually went wrong.** *No rule here was
written without an incident.* (The parallel seat's paragraph `356280ebeadc7168`, carried into the
ledger's language; the Korean original is that draft.)

1. **After a clearance line, the cleared file is not edited** — if it must be, the re-clearance goes
   to both seats **before** the commit; otherwise the change waits for the next one.
2. **The audit sends a HOLD with a list, or a clearance — never both in one message**, or the reader
   cannot tell which way to move.
3. **A hash set quotes the changed paragraph in place.** ⚠ **Measured reason**: two blobs named in
   one night — `1eec7786` and `d508e092` — **entered no commit and cannot be resolved at all**
   (`fatal: Not a valid object name`). *They carry a reading and have nothing left to diff against.*
4. **Every number carries its ruler**: tool · unit · base tree · frozen state · the time the hash was
   taken. ⚠ **Six round trips in one night were the same number read with two rulers** — hash tool,
   bytes against characters, worktree against `HEAD`, a moved «frozen» file, page size, and the
   definition of a net.
5. **The recipient list is decided before the body.** ⚠ **Three times a clearance existed and did not
   arrive** — a verdict existing and a verdict arriving are different events.

⚠ **They belong under C90 because C90 is that shape between people**: *what was cleared and what is
actually there drift apart, and nobody notices the drift.*

### C86-2 2026-09-14 — the gate compares the page it ships

**Built against `26aa1024ef795e71` (253 lines, amendments 1–3).** C86's first half regenerated the
page; this is the half that stops it drifting again. A gate step —
`engine/tools/check_graph_page.py`, one `step` line in `scripts/check.sh` — **deletes the committed
page inside the isolated clone, regenerates it from that commit's `chain.yaml`, `bindings.yaml` and
`phase4/*.yaml`, and compares the bytes.**

⚠ **The first build deleted the page before regenerating, and that was the defect.** With only a
`git diff` as judge, a generator that writes nothing leaves the committed file untouched and the diff
comes back empty — a run that did nothing would pass — so the check deleted first. ⚠ **But the
isolation it relied on happens only inside `check.sh`'s `--from <sha>` branch**; called without
arguments, the step ran in the live worktree, and the audit seat measured what that costs: with
`phase4/` absent the page stayed **deleted**, and on a tree carrying a stale page the check
**overwrote the tracked file** and then told the reader to regenerate and commit it.

**The repair is structural, not a restore-on-exit**: the generator runs in a **temporary mirror** —
its own file plus the declared inputs copied into `<tmp>/engine/` and `<tmp>/phase4/` — and the check
compares that output against the committed page, **reading the tracked file and never writing it**.
*`OUT` is a module constant, so running the generator elsewhere is what moves its output without
touching its logic.* ⚠ **«Wrote nothing» is then caught directly** — no temporary output means no
output — instead of being inferred from an empty diff.

⚠ **The list of inputs has one owner, and so does the resolution.** `build_graph_page.py` declares
**`INPUTS`** (patterns) and exposes **`input_paths()`**, which expands them; its refusal and the check
both call that function — the check by asking the module,
`python3 -c 'import build_graph_page as b; print("\n".join(str(p) for p in b.input_paths()))'` from
`engine/`, never a `grep` over the source, because a second reader ages in its own way. ⚠ **The
expansion is a function, not a module constant, on purpose**: a constant that globbed at import would
touch the filesystem, and this check's other precondition is that importing the generator does
nothing (its write sits behind `if __name__ == "__main__"`). ⚠ **And the risk it closes is not «the
shell globs»** — nothing here is expanded by a shell — *it is two call sites resolving the same
pattern from different roots: the check from the repository root, the generator from `HERE.parent`.*
**One owner for the list, one function for the resolution.** *Importing is safe here: the
module writes only under `if __name__ == "__main__"`.* **A copy list written a second time in the
checker would go stale the day the generator reads one more file — and then the check prints «same»
instead of «different», which is C90's hand-copied list one layer down.**

**The single owner is proven by injection, both directions** (audit seat's fifth test):
  · **a name added** to `INPUTS` (`engine/nonexistent.yaml`) → the check's copy list reads
    `('engine/chain.yaml', 'engine/bindings.yaml', 'phase4/*.yaml', 'engine/nonexistent.yaml')` **and**
    the generator's refusal names that same file. *Both moved; neither was edited.*
  · **`phase4/*.yaml` removed** from `INPUTS` → the boards are no longer copied, the generator no
    longer refuses, and it writes a page whose shipped-value fields are zero — ⚠ **caught anyway, by
    bytes**: `FAIL … 간선 210 → 210 · 첫 다른 줄 142 · 바이트 105 902 → 105 836`. *The counts are
    identical; only the byte comparison sees it — the same lesson as the stale page, in the opposite
    direction.*

⚠ **Three edge numbers, not one** (audit seat): the generator prints only the **kept** count, and one
number cannot separate «0 dropped» from «5 dropped and 5 that were never edges». The step prints the
graph's **raw** count, the **dropped** count and the **kept** count, and requires
**raw − dropped == the page's**. Measured at this commit: **210 − 0 = 210**.

⚠ **The counts are for naming the difference, never for the verdict.** Measured: the stale page at
`0c494b05` holds **51 nodes · 205 edges** and today's holds **51 · 210** — ⚠ **the node counts are
identical**, so a check comparing counts would have passed the very page this item exists to catch.
Bytes catch it; the counts then say *what* moved.

**Both injections fired, not inspected**:
  · **`phase4/` removed** → the generator exits **1** and names the missing input in full (the step
    also prints the mirror's path and the real one, so «no file in a temp directory» cannot be
    misread), and the step reports `생성기가 rc=1 로 끝났다`. *That input is the one silent read of the three — the other two
    raise `FileNotFoundError` on their own; this one used to return an empty `glob`, run the loop zero
    times and write a page whose shipped-value fields were all zero at `rc=0`.*
  · **`0c494b05`'s page put back in place** → **FAIL naming the edge count, 205 → 210**, first differing
    line 117, bytes 103 696 → 105 902 (characters 90 858 → 92 567).
  · ⚠ **All four injections end with `git status --porcelain` empty** — clean tree, stale page
    committed, `phase4/` removed, stale page committed again. *That paste is an acceptance clause, not
    a courtesy: the deletion defect was found by looking at the tree after a run, and the registration
    now demands that look four times.*

⚠ **The step is serial, deliberately.** `_pool_eligible` decides where a step runs by **matching its
name** (`test_*`, `run.py*`), and renaming this step to fit that pattern would be C87's own defect —
changing the subject to satisfy a name-keyed rule — in an item that has not been repaired. Regeneration
measures **0.57–0.72 s**, so the serial floor does not notice it. *The name-matching rule itself is
recorded for C87, not fixed here.*

**Nothing repinned.** ⚠ `git grep` finds **no literal step count in the code** — `check.sh` counts at
runtime, and the four places that say 71 or 72 are all records of named runs (`gate226`, `gate234`,
C61's accounting, and `587842b3`'s C80 incident, which carries both numbers in one line). *Editing them
would turn true records into false ones.* The gate now prints **73**, and that number lives only in the
print.

### C82-2 2026-09-14 — the ice set's ceiling is the fit's reach at the asked temperature

**Built against `45f91076b7c329d1` (544 lines, amendments 1–8), owner's order item ㄷ.** The two
FR2015 thermal sets met at a constant, **`FR2015_FIT_P_MAX` = 353.8 GPa**. The fit's actual reach is
the pressure of its ρ-grid edge (`FIT_RHO_MAX` = 4.25 g/cm³), and **that pressure depends on
temperature**: measured at this sha, **342.1843 GPa at 295 K** and **353.8167 GPa at 2000 K**. ⚠ **The
declared number is neither end of the band** — it over-states the reach below 2000 K by **+11.6157
GPa** and under-states it above by **−0.0167 GPa**. *A wedge that inverts at the top; the declaration
is wrong in both directions.*

**`ThermalSet` gained `p_edge`**, the *name* of the function that computes its boundary at a
temperature, and `covers(p, t)` uses it: the in-band set's ceiling and the graded set's floor are now
**one call to the same function**, so the seam cannot gap or overlap. ⚠ *It could not before either —
but only because both sides read the same constant, which is agreement by coincidence rather than by
construction.*

**Temperature is threaded, not defaulted.** `gamma_set_at(p, t)` and `c_v_at(p, t)` take it; the six
callers pass what they hold, and `c_v_at`'s only two callers sit inside `c_p` itself — no
caller outside the file moved. ⚠ **Callers passing `t=None`: 0.** The one caller that *omits* it is
`engine/test_fe_hcp.py@«「온도 모름」은 통과가 아니라 등급이다»`, the pinned «asked without a temperature» test whose answer C58 and 180 B named;
with `t=None` the bound is the declared constant and the docstring says so **in the same sentence as
the two errors**, so a reader meets the over- and under-statement where the number is used.

**What it costs, measured before the gate** (190 B's lesson): `p_edge` is evaluated **30 520** times
for Uranus and **6 938** for Neptune, **0** for all six roster bodies — ⚠ **all eight counts come from
one run**, the counter reset between bodies, so the anchors' large numbers are the roster zeros' own
control rather than a separate execution's. In the anchor that shows as
**27.2 → 28.1 s** and **63.3 → 65.6 s**.

**J8, a new pinned test**: over a 7-point temperature grid × 5 probes around the moving edge —
**35 cells** — exactly one set covers each pressure, and the note prints both edges beside the
declared constant.

⚠ **C88's trigger fired, by design, and the anchor's diff is three lines**: `eos.py`'s digest, and the
two `seconds`. **Every one of the 21 value keys per body, both `standalone` blocks, `grade` and
`regime` are byte-identical** — *the wedge was a declaration defect, not a value defect, and this is
the measurement that says so rather than the expectation.*

**Where the wedge is actually asked** (measured, not assumed): the six roster bodies never consult an
ice thermal set at all — **0** ice thermal calls, **0** `covers` queries. The only answers inside the
wedge belong to the two anchors, **348** of them (**Uranus 308 · Neptune 40**), against controls of
**20 958** and **4 756** ice thermal calls. *Two earlier tables were withdrawn before this one: the
first hooked `ice_fr2015.density_at`, which `eos` never calls because it binds
`thermal_at_hse` by value at import, and printed 0 everywhere; the second counted every material's
sets and gave Earth 47 442 wedge hits while that body's ice thermal calls were 0.* ⚠ **The control
printed in the same run is what separated «none» from «not measured».**

⚠ **정정 (C94, 2026-09-15).** 이 항목의 fix-up 커밋 `02bb7a2a` 와 ㄱ 의 `26e44e36` 이 낸 `rc=0` 은
**앵커 이행이 아니라 인용 소실**이었습니다. 쓴 꼴 `` `file`@«…» `` 은 이름과 `@` 사이에 백틱이 끼어
`ANCHOR` 정규식에 안 맞고, 그래서 **앵커로 세어진 적이 없습니다** — `interior-core.md` 의 앵커 수가
그 커밋을 가로질러 **139 → 139** 였습니다. 줄번호 FAIL 만 사라져 초록이 났습니다. **C94(`d301d433`)
가 `malformed anchor` 검출을 넣고 그 인용들을 정식 꼴(백틱이 인용 **전체**를 감싸는 꼴)로 이행하며 닫습니다.**
⚠ **이 절에서 잰 수는 하나도 안 움직입니다** — 쐐기·앵커 diff·348 칸·73 단계가 전부 그대로이고,
바뀌는 것은 **추론 하나**입니다: 「인용 검사가 통과했다」를 「이제 앵커다」로 읽었는데, 그것은 앵커도
줄번호도 아니었습니다.

### C65 — two nodes emit `radius`, and the winner is decided by nothing anyone declared — **pre-registration draft, 2026-09-11**

⚠ **Split out of C64 by the directing seat** because a key the whole engine reads is a different item
from a verdict key nothing consumes. Draft only; no code written.

#### The verdict line, in the form that can be contradicted

**Not** *"the two values differ"* — they sometimes do and that is a symptom. The line is:
⚠ **is one key emitted by two nodes allowed at all, and if it is, what decides the winner?** Today the
answer is *nothing declared*: `state.results` fills in `graph.order`'s topological order, so
`state.get("radius")` returns whichever node the sort happens to run first (`interior_layers`, #24) and
`state.resolved` returns the last (`mass_radius_relation`, #26). **Move one node in `chain.yaml` and five
consumers silently receive a different radius.** *Contradicted by:* a declared owner for the key, or a
check that fails when two nodes claim one name.

#### What the audit seat measured (2026-09-11, `audit_dupkeys.py`)

| fact | number |
|---|---|
| bodies where **both** producers are applicable | **4 of 7** |
| bodies where the two values **differ** | **2** — `mars` **−1.87 %**, `dante_fixture` **−12.51 %** |
| shipped consumers of `radius` | **5**, by node name: `core_thermal_history` · `dynamo_rocky` · `internal_heat_nontidal` · `tidal_heating` · `heat_transport_mode` (*an earlier version of this row wrote «`tidal_heating` ×2», which named a file twice instead of two nodes*) — **all receive `interior_layers`'s value** |
| what reads the *other* value | `run.py`'s convergence comparison and `state.py`'s summary count — **nothing that ships** |

⚠ **So today's shipped output is unaffected, and that is exactly what makes it dangerous**: the
convergence verdict is computed on a value **no consumer reads**, and the 12.51 % disagreement on
`dante_fixture` sits inside the loop that decides whether the chain converged.

#### ⚠ What the two producers actually are — measured before writing the repair

`mass_radius_relation` **does not solve for a radius of its own**: it calls the same solver
(`engine/mass_radius.py@«structure = solve(mass_earth, composition=composition)»`) — and that call
carries **mass and composition only**. No ice mass fraction, no gas mass fraction, no potential
temperature, no porosity. `interior_layers` calls the same function with **everything the body
declares**.

⚠ **So the two numbers are not two models disagreeing; they are one solver run twice on different
inputs.** That also explains the size of the gap where the audit seat measured it — `mars` **−1.87 %**,
`dante_fixture` **−12.51 %** — the more a body declares, the further the screening call sits from the
body's own solve.

**This changes what the repair is about.** Before asking *who owns the name*, the question is *what each
number is*: one is a **screening estimate from mass and composition**, the other is the **body's full
structure**. The rename should say that (`radius_mr_screen` or similar), because a name that says
"radius" twice is what let them be read as the same quantity.

⚠ **And two declared edges are already false.** `chain.yaml` carries `mass_radius_relation → body_figure`
and `→ tidal_heating`, both `via: radius`, yet all five shipping consumers receive `interior_layers`'s
value (audit seat's measurement). Renaming does not create that problem — **it exposes it**. Where those
edges should point is a declaration decision, not a code one, and it is listed for the owner rather than
taken here.

#### The repair, registered before it is written

1. **`radius` gets a declared owner: `interior_layers`.** The owner is written where a reader looks —
   in `chain.yaml` beside the node, not in prose.
2. **`mass_radius_relation`'s output is renamed** (candidate: `radius_mr_scaling`) **or demoted to
   comparison-only**. Its number stays available; what goes away is the collision on the name.
3. **The owner declaration is data, and the rule that reads it is not this item.** ⚠ *Scoped after the
   audit seat's objection and the directing seat's call (2026-09-11)*: making `state.resolved`'s **merge
   rule** owner-aware would reach **all six** duplicated keys — including C64's, which prohibition 3
   forbids this brief to touch. So the merge rule is **C68**, and it has **three states**: ① an owner is
   declared → only the owner's value enters `resolved`; ② the claimants are **class-exclusive** → it
   passes without an owner, but the contract check **measures «zero same-run co-occurrences» every run**
   rather than carrying an allow-list; ③ neither → **FAIL**. C65's job is to **declare `radius`'s owner and rename the other output**, which is the
   material C68's rule will read. *Contradicted by:* this brief changing what `resolved` does for any
   key, `radius` included.
4. **A check fails when one key is claimed by two contracts** — the cheap version, a document scan, is
   C64's; this item consumes it rather than building a second one.

**Registered expectations:** the seven bodies' shipped values are **bit-identical** (the five consumers
already read the owner's value); the count of emitted phases and the convergence verdict may move, and
**every such movement is named**; `dante_fixture`'s 12.51 % becomes a printed comparison rather than a
hidden branch. *Contradicted by:* any shipped value moving, or a convergence verdict changing without a
name.

#### What this must not do

1. ⚠ **It must not delete the second number.** Two ways of getting a radius disagreeing by 12.51 % on a
   fixture is a finding; the repair removes the ambiguity, not the measurement. *The property:*
   `mass_radius_relation`'s value still appears in the output under some name. *Contradicted by:* a run
   whose output contains no radius from that node at all.
2. ⚠ **It must not rename the key consumers read.** `radius` stays `radius` for the five consumers.
   *The property:* all five lookups resolve to the same name before and after. *Contradicted by:* a
   consumer reading a differently-named key, or a `Missing` raised where none was raised before.
3. ⚠ **It must not fix C64's key** — different item, different owner decision. *The property:*
   `entropy_history_verdict` is byte-identical across this brief's commit, and **the check already
   exists**: `engine/test_core_entropy.py@«2: 이 노드는 이력 판정을 **내지 않는다**»`.
   *Contradicted by:* that key's value differing before and after.

### C61 — a step that was never tallied reads as a step that passed — **listed 2026-09-10, hardened the same day**

⚠ **The third of a family.** 169 E was *a body the full lane never ran* (Mars's shipped-value comparison
went unrun for a month because three names were typed by hand). C60 was *a trial step read as a verdict*.
This one is the same shape at the harness level: **"did not run" and "passed" are not distinguishable to
the gate's own tally.**

**The case that named it, gate229 (2026-09-10).** Brief 184 put the test steps in a pool: each child writes
its output, its exit status and a `.done` marker into a spool directory, and the parent drains them. The
spool directory was deleted **while the gate was running**, so no child could write its status, the drain
read nothing, the barrier's `wait` returned because the children had in fact finished — and the gate printed
**`[STEP]` 71 times, `[TIME]` 19 times (the serial steps only), and `rc=0` after 4 min 52 s.** ⚠ **52 steps
never reached the verdict and the gate was green.** *(The deletion was the directing seat's — it saw a
0-byte directory in `$TMPDIR` while tidying. That is one line of the case; the item is the harness's, because
a harness whose green depends on nobody tidying is not a harness.)*

#### What was hardened (184 B, same day)

- **The spool's absence is a named failure.** Before each pooled launch the spool is probed for existence
  *and writability*; if it fails, `[FAIL] pool_dir` is printed, `fail=1` is set, **and that step is demoted
  to serial** so its verdict still arrives.
- **The barrier counts launches against completions, from two different sources.** Launches are counted in
  the **parent's memory**; completions are counted from the **exit-status files the children leave**. ⚠ *A
  count taken twice from the same log cannot catch the case where the log is what went missing.* A mismatch
  prints `[FAIL] pool_incomplete — N steps never reported completion`, names every launched step, and sets
  `fail=1`.
- **"Tallied count equals launched count" is part of the gate's own rc**, not a warning beside it.
- **Children exit quietly when the spool is gone** rather than emitting twenty shell errors, so the real
  failure sentence is not buried in them.
- **Proved by injection** in an isolated harness: a normal run with an injected non-zero exit
  (`fail=1`), a run whose spool is deleted mid-flight (`pool_incomplete`, naming both steps), and a run
  with a spool that never existed (`pool_dir`, step demoted to serial and still judged). The injection is
  planted and removed; nothing is left behind.

⚠ **The rule this bought, beyond the code**: gate scratch and spool directories are cleaned **only after
`GATE END`**, and **never for a live pid** — by any seat.

**184's own verdict line, measured on one commit three ways (2026-09-11).** The pool exists to buy
wall-clock, so the number is the verdict: **serial 34.5–44.7 min · pool 2 20–22 min · pool 8 **12 min
8 s**** (gate234 on `fbfe6b2a`, full lane, 71 steps launched and 71 tallied, PASS 682, peak RSS 57 MB).
⚠ **The floor is one step**: `test_giant` alone is 311 s at pool 8, so no pool size takes the full lane
below ~6 min without splitting that step. The default is now **8**, and quiet mode is `GATE_POOL=2` in
the environment — *the three values pass through the same code path, and the pool size is the only thing
that differs between them.*

### C62 (a) 2026-09-10 — `tidal_response`, a layered viscoelastic Love-number node (k₂, h₂, Q as a rheology band) — pre-registered before the build

⚠ **Committed before the code.** The text below is P28 (parallel seat, 2026-09-10 evening) moved into
the ledger **verbatim**: `P28-tidal-response-prereg.md`, sha256 `92b95059014d03db…`, **9211 B** in the
shared folder `~/Desktop/NearStars-artifacts/2026-09-09-c20-entropy-band/`, hashed here. Two things are
added and nothing is removed — the **owner-pending labels** in §"Owner decisions" at the end, and this
header. *The pre-registration is the parallel seat's; the labels are what a seat may write, and the
elections are not.*

⚠ **Nothing reads k₂ today**
(P28's own "non-consumers, the useful half"), so the node is an emitter and no shipped verdict can move
when it lands. That is why it may be registered while the owner is away — and also why nothing in it
may be *elected* while the owner is away.

⚠ **This section is committed before the change.** P24/P27 established that the minimal set closes *at the equation level* inside held papers —
the propagator system (Beuthe 2015 eqs 13–18, the Takeuchi & Saito 1972 eq. 82 form), the rheologies (Bagheri+ 2022 §2.3–2.7), and four parameter
tables — with one named limit: the liquid-layer (core/ocean) condition and the static-limit degeneracy (Saito 1974, paywalled, not held) exist in
the held set only as Beuthe's membrane limit (eq. 27, k°_n + 1 = h°_n). **Nothing chosen here.** Sources carry bibcode, ADS link, grade.

#### The blast radius, counted before the design

| where | what exists today | what the node adds |
|---|---|---|
| `engine/interior*.py` (layer stack: radii, ρ(r), P(r), T(r) per material) | the structure the propagator integrates over | read-only consumer: ρ_r, g_r, μ, K (or ν) per layer |
| `engine/eos.py` materials | ρ, K_T, K_S from the EoS; **no shear modulus μ anywhere** | ⚠ μ per layer must be **declared** (or taken from a printed source per material) — a gap, not a computation |
| `engine/dynamo_rocky.py`, `core_state.py`, `mantle_flux.py` | unrelated (no k₂ reader today) | no change |
| `engine/bodies/*.yaml` | no `tidal_response` block | new block: rheology choice, μ per layer, forcing frequency (orbital period), liquid-layer flag |
| Phase-4 boards / SPEC | no k₂ row | out of scope (owner facet choice, as C53 (d)) |

**Non-consumers, the useful half:** nothing reads k₂ today; the node is a pure emitter until a consumer (tidal heating, Q for orbital evolution)
is wired — that wiring is not this item.

#### Inputs (declared per body, or derived from the interior solve)

```yaml
tidal_response:
  rheology: maxwell | andrade | sundberg_cooper       # emit all three as a band by default
  forcing_period_s: ...                                # orbital (synchronous) or eccentricity tide period — declared
  layers:                                              # from the interior solve; μ and rheology parameters declared per layer
    - name: core   ; state: liquid ; mu_pa: 0     ; treatment: membrane_limit   # ⚠ labelled limit (Beuthe eq. 27), not Saito 1974
    - name: mantle ; state: solid  ; mu_pa: ...   ; eta_pa_s: ... ; andrade_alpha: ... ; andrade_zeta: ...
    - name: crust  ; ...
  grade: declared | analog
  source: [bibcodes]
```

Printed parameter sets the owner can point a declaration at (candidates, not chosen):

| set | values | source (grade) |
|---|---|---|
| Henning 2009 Table 2 "Baseline Material Parameters" | M = M_B = 5 × 10¹⁰ Pa; δJ = 4 × 10⁻¹² Pa⁻¹; η_set = 10²² Pa s; η_B,set = 2 × 10²⁰ Pa s; E* = E*_B = 300 kJ mol⁻¹; T_sol 1600 K, T_liq 2000 K, T_brkdwn 1800 K; η = η_solid e^(−40χ) (eq. 21) | Henning, O'Connell & Sasselov 2009 [`2009ApJ...707.1000H`](https://ui.adsabs.harvard.edu/abs/2009ApJ...707.1000H) (held) — assumed baseline |
| Beuthe 2015 Table 7 | μ_m 40 GPa, K_m 10²⁰ Pa (SatStress), μ_E 3.5 GPa, ν_E 0.33, η_top 10⁷ η_crit, η_bot 10/1/0.1 η_crit; η_crit Europa 1.71 × 10¹⁴ Pa s, Titan 7.67 × 10¹⁴ Pa s | Beuthe 2015 [`2015Icar..258..239B`](https://ui.adsabs.harvard.edu/abs/2015Icar..258..239B) (held) — assumed, icy shells |
| Renaud & Henning 2018 | Andrade / Sundberg–Cooper complex compliances and parameter ranges (α, ζ) for Io-like silicates | [`2018ApJ...857...98R`](https://ui.adsabs.harvard.edu/abs/2018ApJ...857...98R) (held) — assumed/scanned |
| Bagheri 2019 | Mars: five rheologies fitted to k₂, MoI, mean density; "Maxwell is only capable of fitting data for unrealistically low viscosities" | [`2019JGRE..124.2703B`](https://ui.adsabs.harvard.edu/abs/2019JGRE..124.2703B) (held) — result |
| Bagheri 2022 §2 | Maxwell (§2.3), Burgers / extended Burgers (§2.4), **Andrade (§2.5, eq. 18: J(t) = J_U + β t^α + t/η)**, Sundberg–Cooper (§2.6), power law (§2.7); homogeneous-body quality function §4.4 eqs 58–59 | [`2022AdGeo..63..231B`](https://ui.adsabs.harvard.edu/abs/2022AdGeo..63..231B) (held) — formalism |

#### The equations the build implements (all held; nothing from blogs or unsourced notes)

- Propagator: **Beuthe 2015 eqs (13)–(18)** — y₁′ … y₆′ for degree n, frequency ω, with (ρ_r, g_r, μ, ν, χ) per layer; three regular solutions at the
  centre; surface conditions on y₂, y₄ (no radial stress) and y₆ (potential gradient); Love numbers from the surface values (eq. 7 form: h = g y₁(R),
  l = g y₃(R), k = y₅(R) − 1). Viscoelasticity enters by the correspondence principle: μ → μ̃(ω) = 1/J̃(ω).
- Rheology: the complex compliance J̃(ω) of Bagheri 2022 §2.3 (Maxwell), §2.5 (Andrade), §2.6 (Sundberg–Cooper); Q from Im/Re of k̃₂ (Bagheri §4.3).
- ⚠ **Liquid layer = membrane/fluid limit only** (Beuthe eq. 27, k°_n + 1 = h°_n; μ → 0 for the fluid layer). The general liquid-layer interface
  condition and the ω → 0 degeneracy (Saito 1974) are **not in the held set** — every result carries the label «fluid core treated in the membrane
  limit (Beuthe 2015 eq. 27); Saito 1974 not held».

#### Outputs

k₂, h₂ (and l₂), phase lag → Q, **as a band over the three rheologies** {Maxwell, Andrade, Sundberg–Cooper} at the declared forcing period, plus the
per-rheology values. A body without declared μ or rheology parameters is **refused by name**; a body with a liquid layer emits with the membrane
label.

#### Reproduction anchors (printed; pass lines = the papers' own error bars)

| # | anchor | printed value | source (grade) | pass line |
|---|---|---|---|---|
| T1 | Beuthe 2015 Titan/Europa membrane cases | "h₂ = 1.27 (Model L) or h₂ = 1.35 (Models M and D)" (App. C, eq. C.3 context); relation k°₂ + 1 = h°₂ for a fluid top layer | Beuthe 2015 (held, result) | reproduce h₂ to the printed 2 decimals for the stated model |
| T2 | Henning 2009 baseline body | the Table 2 body under Maxwell/SAS/Burgers: reported heat rates and Q in Table 1/Fig. 4 (values figure-read) | Henning 2009 (held) | qualitative order-of-magnitude agreement per rheology (figure grade) |
| T3 | Mars k₂ | **0.169 ± 0.006**, Q **95 ± 10** (Khan 2018 Table; Bagheri 2019); 0.1697 ± 0.0027 (Konopliv 2016 via Bagheri 2022); 0.174 ± 0.008 (Konopliv 2020 via Drilleau 2022); Phobos-based Q = 92 ± 11 (Bagheri 2022 §5) | held (result) | inside the quoted ± for the elected solution family (P20 §1) |
| T4 | Moon k₂ | **0.02416 ± 0.00022** (GRAIL, Konopliv 2013/2014 via Bagheri 2022 §5.3); monthly Q = 38 (Williams & Boggs 2015 via Bagheri) | Bagheri 2022 (held, second-hand) | inside ± |
| T5 | Earth | solid-Earth semi-diurnal **Q = 280 ± 70** (Ray et al. via Bagheri 2022); k₂ itself not printed in the held set (IERS value not held) | Bagheri 2022 (held, second-hand) | Q inside ±; k₂ anchor **absent until a printed source is held** |
| T6 | Mercury / Venus | k₂ 0.451 ± 0.014 (Mazarico), 0.464 ± 0.023 (Verma & Margot 2016), 0.569 ± 0.025 (Genova+ 2019), h₂ 1.55 ± 0.65 (Bertone 2021), h₂ 1.02 ± 0.04 (prediction); Venus k₂ 0.295 ± 0.066 (Konopliv & Yoder 1996) | Bagheri 2022 §5 (held, second-hand) | inside ± where a model is declared |

#### Expected results, registered before running

1. With Henning's Table 2 baseline on a homogeneous silicate body, the three-rheology band on k₂ is narrow (elastic limit) and the band on Q spans
   orders of magnitude at low temperature — the *direction* Henning 2009 and Renaud & Henning 2018 report; no number registered.
2. Mars with the elected interior (P11/P12/P14 declarations) and a fluid core in the membrane limit: k₂ inside 0.163–0.182 only for some
   (μ, η, rheology) declarations — the band is the result; Bagheri 2019's statement that Maxwell needs "unrealistically low viscosities" is expected
   to reappear.
3. Any body without a declared μ is refused by name; any body with a fluid layer carries the membrane label in every output.
4. An outcome outside 1–3 is written down as its own kind afterwards and registered then.

#### What this brief must not do

1. ⚠ **No unsourced deceleration/despinning formulae** (no blog-derived constant-Q or CTL shortcuts; Bagheri 2022 §4.4–4.5 and Efroimsky 2012
   CeMDA are the printed sources for anything frequency-dependent).
2. ⚠ **The fluid core is the membrane limit and says so** — it must not be presented as Saito's general liquid-layer solution.
3. ⚠ **It must not invent μ per material.** μ is declared per layer with a printed source, or the body is refused.
4. ⚠ **It must not pick the rheology.** All three are emitted; the owner elects, if at all, as a facet.
5. ⚠ **It must not couple to tidal heating or orbital evolution** — emitter only.

**Size (estimate):** one propagator (six ODEs, three regular solutions, 3×3 surface solve), three complex-compliance functions, one body block,
tests T1/T3/T4/T5 with printed ± and the membrane label asserted by name.

#### Owner decisions this surfaces (none taken) — the labels this seat adds

| # | decision | candidates recorded | label |
|---|---|---|---|
| (a) | **the liquid-layer condition**: is the membrane limit the shipped treatment, or does the node refuse a fluid layer until Saito 1974 is held | (i) emit in Beuthe 2015 eq. 27's membrane limit with the label on every output (P28's registered behaviour); (ii) refuse a body with a fluid layer by name until the general condition is held; (iii) hold the item until Saito 1974 (`1974RSPTA.275...41S`, paywalled, **not held**) is acquired | ⚠ **owner pending** |
| (b) | **the shear modulus per layer**: declared per body with a printed source, or taken per material from a printed table | (i) declared per layer in `bodies/*.yaml`, no default, a body without it refused by name (P28's registered behaviour); (ii) a per-material printed μ in `eos.py` beside K_T, with the same verdict machinery C58 (a) built for γ; (iii) both — material printed value as the fallback, declaration wins, and the choice is printed | ⚠ **owner pending** |
| (c) | **the rheology**: does a body ever elect one, or is the three-rheology band the only output | (i) band only, forever (P28's registered behaviour); (ii) an optional declared election, band still printed; (iii) a class default per body class | ⚠ **owner pending** — and P28 §"must not do" 4 forbids a seat from choosing |
| (d) | whether k₂/Q from this node ever replaces the **declared** `k₂/Q` that C39 unified, and on which bodies | **(i) is the standing default for the first build — the node emits and does not replace a declaration, so C39's seam is kept** (directing seat, 2026-09-10); (ii) the node's band becomes a third source below a declaration; (iii) the node replaces the class band for bodies whose μ is declared | ⚠ **owner pending** — the default is what the build does meanwhile, not the election; reopening this seam moves shipped τ values |

⚠ **(d) is the one that can move a shipped number**, and it is the reason this item stays an emitter in
its first build: Dante declares `k₂/Q = 0.0155` (`Q/k₂ = 64.5`, **below** the class band's floor) and
Hades `1e-3` (the band's top), and C40 already records that both are **fitted to our own output** with no
width anywhere. A node that computes k₂ from structure would hand those two bodies a first independent
number — which is exactly why the swap is an owner decision and not a wiring detail.

⚠ **Not fabricated here, and not an owner decision either**: the engine has **no shear modulus anywhere
today** (P28's blast-radius row for `eos.py`). Until (b) is decided, μ is a gap the node names, not a
quantity it fills — the same shape as C58 (a)'s γ, where the material was asked and answered *"my thermal
set is for another state"*. **A μ invented per material would be C40's fitted value with no seat.**

### C62 (b) 2026-09-11 — the first build's implementation pre-registration (P35), folded before the code

⚠ **Committed before the code, and refreshed twice while the code was written.** The text below is P35
(parallel seat, 2026-09-11) moved into the ledger, sha256 `bbb916e27af20a6a…`, **39187 B**, living at
`~/Desktop/NearStars-artifacts/2026-09-09-c20-entropy-band/drafts/P35-tidal-response-build-prereg-draft.md`
— ⚠ *the 09-11 rule points foldable drafts at that day's folder, and this one is cited at its existing
path instead: a draft the work and audit seats have already cited by path and hash is not moved, because
moving it breaks both at once* (directing seat, 2026-09-11). **The first fold was `bb67e2ced144f8eb`,
29375 B**, at Amendment 12; this section now carries Amendment 20, and the refresh is recorded rather
than silent because *the gap between the two is where the implementation pushed back on its own
pre-registration.*

⚠ **Twenty amendments, and the useful fact is who found what.** The draft reached this form through
twenty corrections in about three hours — the audit seat against the PDFs (Wahr's line pointers and the
Table 4 trap, the Moon's Q lineage, Io's missing number, the Kelvin–Love form), the audit seat against
the engine (there is no ρ(r) on a radius grid to integrate; `Structure` has no `r_ice_base`; the preset
label needed a node prefix; `crust_thickness` is in the contract but not in the graph), and this seat
against the engine and the papers (the mantle map double-covered ocean bodies; `cmf`/`imf` live in
`Result.inputs` where `state.get` cannot see them; `cmf` has a preset precedent inside `solve` itself;
only five of the seven boundary radii are reachable and they arrive in two different units; **Saito 1974
is held, not paywalled**, and it closes the starting-value gap Beuthe left open; **eq. (27) answers a
different question than decision (a) asked it**; and Bagheri prints a closed form for `k₂` itself, so
neither closed form has to be re-derived).

⚠ **Most of them are one shape.** *«The pre-registration asked the engine, or a paper, for something
that is not there — or is there and was thought not to be.»* None would have survived first contact with
the code. The cost of finding them here was messages; after the build it is a commit, a gate and a
re-measurement.

⚠ **Three edits were made in the move, and they are all the same edit.** The draft cited three code
sites by line number, and this tree forbids that form, so each became a phrase anchor at the same site
(`COMPOSITIONS: dict[str, tuple[float, float, float, str]] = {`, the `if stack[layer][1].name == "h2o":`
branch that assigns `p_ice_base`, and `def check(g: dict) -> int:`). *Nothing else was changed.* The
headings are one level deeper than in the draft, to nest under this section. The three forms as the
draft wrote them on **2026-09-11**, so the move is reversible:

> note (2026-09-11): `interior.py:82` · `interior.py:734` · `chain.py:52`

⚠ **What is decided and what is not.** Decisions A–F, the three input routes ①②③, and the `cmf`
routes (가)/(나′) were **owner-level and came down through the directing seat** — they are recorded in
the draft at the point they apply, with the losing candidate kept beside the winner and the reason each
seat argued for it. Nothing below is elected by a seat.

#### P35 — implementation pre-registration draft for the first `tidal_response` build (C62, emitter only) — **draft 2026-09-11 11:xx, parallel seat; nothing built, no value transcribed**

⚠ **Committed before the change (draft form).** P28 (`92b95059…`, moved into the ledger as C62) registered the node; this draft is the *implementation* pre-registration under the owner's/directing seat's decisions of 09-11. Every number below is a pointer to where it is printed, not a copy.

##### Decisions this draft implements (given, not open)

| # | decision |
|---|---|
| scope | **emitter only** — the node emits k₂, h₂, l₂, Q; it does **not** replace any declared `k2_over_q` (Pandora's `k2_over_q: 0.0016`, board-fitted) and the C39 seam `k2q_class_table → tidal_heating via k2_over_q` (`engine/chain.yaml@«{from: k2q_class_table, to: tidal_heating, kind: requires, via: k2_over_q»`) stays as it is |
| (a) liquid layer | **(revised, Amendment 18)** A fluid layer **that reaches the surface** takes Beuthe 2015 eq. (27) `k°_n + 1 = h°_n` (layout line 525) with μ → 0 — that is eq. (27)'s applicability condition. A **subsurface ocean under a solid shell** is Beuthe §3's membrane approach with effective parameters (Λ, δρ°) and is **outside this build → named refusal** («ocean under shell: Beuthe §3 membrane parameters not built; solid-over-fluid start vectors are printed by Saito only at the CMB»); registered as **C62 (c) successor candidate**. Liquid **core**: Saito 1974 §2.3 eqs (17)–(20) start (Amendment 16) |
| (b) shear modulus | **declared per layer first**; if absent, a material-level μ from a printed source (P28 candidates table: Henning 2009 Table 2, Beuthe 2015 Table 7) with the label «material substitute»; if neither, refuse by name |
| (c) rheology | **all three emitted as a band** — Maxwell (Bagheri 2022 §2.3), Andrade (§2.5, eq. 18), Sundberg–Cooper (§2.6); no election |

##### The blast radius, counted before the design

| where | today | moves? |
|---|---|---|
| `engine/chain.yaml@«핵 쪽 경계 온도를 선언하면 둘 다 말한다»` | `status: missing`, `outputs: [k2_over_q, layer_q]`, note «k2q_class_table이 이 자리를 대신» | status → built; outputs become `[k2, h2, l2, q, k2_over_q_emitted, layer_q]` — ⚠ the emitted `k2_over_q_emitted` is a **new name**, so the existing edge :555 (`k2q_class_table → tidal_heating via k2_over_q`) is untouched by construction |
| `engine/tidal_heating.py@«if k2_over_q is None:»` (the `cannot-say` branch) | reads the **declared** `k2_over_q` only | **untouched** — non-consumer of the new node in this brief |
| `engine/interior.py` `solve` / `Result` (layer radii, ρ(r), P(r), T(r), `core_pressure`, `cmb_pressure`, shell/ocean thicknesses) | the structure the propagator integrates over | read-only input (see contract) |
| `engine/eos.py` materials | no μ anywhere | unchanged; μ comes from declaration or the substitute table |
| `engine/bodies/*.yaml` (7) | Pandora: `eccentricity_forced 0.005`, `k2_over_q 0.0016`, `tidal_heating: true`; Dante fixture: `tidal_heating: true`; no `tidal_response` block anywhere | **no body file changes in this brief** — the node runs only when a `tidal_response` block exists, so the seven bodies are bit-identical (registered) |
| boards / phase4 | no k₂ row for Dante or Hades in `phase4/*.yaml` (grep: only Fomalhaut's stellar k₂ path) | untouched |
| `test_tidal_heating.py`, `test_tidal_locking.py`, `test_tidal_transport.py` | existing | unchanged; a new `test_tidal_response.py` carries the anchors below |

**Non-consumers, the useful half.** `tidal_heating`, `tidal_locking`, `dynamo_*`, `core_*`, `interior_*` read nothing from the new outputs. **Registered: all seven roster bodies' full solves are bit-identical before/after** (`run.py bodies/*` in the gate), because no body declares the block.

##### Input contract (node `Needs`, to be added to the methodology `Needs` table **first**, C53 order rule)

```yaml
tidal_response:                       # per body; absent → node not run (no refusal, no output)
  forcing_period_s: <declared>        # orbital or eccentricity-tide period; source label mandatory
  degree: 2                           # n; only 2 in this build
  layers:                             # one entry per interior_layers layer, outer to inner, matching the solve's layer stack by name
    - name: <layer>  state: solid|liquid
      mu_pa: <declared> | material_substitute   # (b): declared wins; substitute names its printed table
      eta_pa_s: <declared>                       # Maxwell/Andrade/S–C need η; absent → refuse by name
      andrade_alpha: <declared> ; andrade_zeta: <declared>          # Andrade (Bagheri 2022 §2.5) — absent → Andrade member of the band refused by name, others still emitted
      sc_delta_j, sc_tau: <declared>                                # Sundberg–Cooper (§2.6) — same rule
  grade: declared | analog ; source: [bibcodes]
```
From `interior_layers` (read-only) — **layer-homogeneous model, not profiles** (audit, Amendment 6): `Structure` keeps **no ρ(r), P(r), T(r) on a radius grid** (its `ice_samples`/`rock_samples` are (P, T) pairs without radius; `integrate()` builds profiles but does not return them, `engine/interior.py@«겉질량이 목표에 못 미치므로 괄호는 이 점을 아래끝으로 쓴다»`, and the second of that pair), and a node sees only the `interior_layers` `values` (21 keys measured on the four applicable bodies at c2a6a324; `chain.yaml` declares 14 — the difference is C73's seven). What exists and is reachable (Amendment 13, work seat): the node **cannot see `Structure`** — it sees only the `interior_layers` `values` (21 keys; graph declares 14), and among them **five** reach the layer boundaries: `radius` · `core_radius` · `ocean_thickness` · `ice_shell_thickness` · `crust_thickness`. The others are derived in the node: r_ocean_top = R − ice_shell_thickness; r_ocean_base = r_ocean_top − ocean_thickness; r_crust_base = R − crust_thickness. `r_grad_base`/`r_grad_top` are **not** layer boundaries (Brief 26 gradient-region markers) and never belong in the map's domain. So **the domain of the layer-name map is these five values**, ⚠ with one unit trap: `radius` and `core_radius` are in **R⊕** and the three thicknesses in **km** (`interior.py` units dict) — the conversion lives in one place in the node and a test asks for it. (The earlier «seven `Structure` radii» wording is withdrawn — the tenth case of «the draft asked for something the node cannot reach».) ⚠ **Amendment 14 (audit):** of the five, **`crust_thickness` is emitted in `values` and in the contract Returns (`engine/interior.py@«이 답은 **거절이 아니라 외삽**이고, 등급이 그 사실을 진다»`, and the contract Returns line beside it) but is missing from `chain.yaml` `interior_layers.outputs`** (fourteen keys listed there, against 21 in `values`/Returns). Reading works (`state._find` looks at `values`), but declaring the edge `interior_layers → tidal_response via: crust_thickness` would fail `check_via`, which checks the supplier's `outputs`. **Registered as part of this build (route 가): add `crust_thickness` to `interior_layers.outputs` in `chain.yaml`, and declare the five edges** — so the new node is not the first consumer that eats an undeclared value. The wider fact — **40 contract-Returns keys absent from `chain.yaml` outputs** (interior_layers 7, core_state 9, tidal_locking 8, heat_transport_mode 6, internal_heat_nontidal 5, dynamo_giant 5; reverse direction 1, `tidal_locking.t_lock`) — is **not this build's job**: it is registered as **C73** («chain.yaml outputs forty cells behind the contract Returns, one in reverse»; directing seat 2026-09-11; candidate row goes into the C62 commit's ledger), measured by the audit's `c62_outputs_vs_returns.py`. the phase list (fluid flag from material `fit_state`/declared `state`), and the **declared mass fractions** (`core_mass_fraction`, `ice_mass_fraction`) with the total mass. ⚠ **Where the fractions come from (work seat, Amendment 9):** a node cannot read `core_mass_fraction` / `ice_mass_fraction` from `state` — `state._find` looks at declared inputs first, then only at each result's `values` (`state.py` «선언된 입력이 먼저, 그 다음 도출값»), and `interior_layers` puts the fractions in `Result.inputs`, not `values` (`interior.py` ~2323); the 21 `values` keys carry `core_radius_fraction` but no mass fraction (the same shape as C64's `converged`; and see Amendment 13 for the boundary radii, which have the same visibility issue but are reachable through five `values`). Three routes: ① **declaration only** — the node builds densities only when the body declares cmf/imf (and a `tidal_response` block), else refuses by name; inverse-solved bodies (dante_fixture declares neither cmf nor composition_intent, C65 (b)) do not run; «read-only» and «seven bodies bit-identical» hold. ② `interior_layers` also emits the fractions in `values` — one line, but it grows the contract `Returns` and moves the duplicate-producer count J8 measures in the same commit (J8's baseline would have to be re-taken first). ③ back-solve two densities from `nmoi` and `core_radius_fraction` — unique for two layers only, undetermined with ocean/crust, and a new model rather than «our arithmetic» → its own registration. **Decided (directing seat, 2026-09-11): ① for the first build** — declaration only; a body without the block is refused by name; expected roster count 0; J1–J3 stand on declared test-anchor blocks (Earth, Moon, Mars). ② is **listed as a follow-up candidate** — structurally the right direction, same family as C64/C71 («in `inputs` only, so consumers cannot read it»). ⚠ Audit (Amendment 10): ② does **not** move J8 — no node in `chain.yaml` lists `core_mass_fraction`/`ice_mass_fraction` under `outputs` (the names appear only in edge notes), so emitting them from `interior_layers` adds two single-producer keys and creates no duplicate; the «J8 baseline first» precondition is therefore **lifted** (directing seat, 2026-09-11); ② remains **outside the first build** (follow-up). ③ is a separate registration candidate. Under ①, the build must **count and record how many roster bodies actually run the node today** (expected 0), so that J1–J7 are read as standing on declared test bodies, not on the roster. Audit's count of the declarations today (acc49b09, `engine/bodies/*.yaml`): `core_mass_fraction` declared on **three** (earth 0.325 · mars 0.24 · pandora 0.325), `ice_mass_fraction` on **one** (dante_fixture 0.0) — so ①'s real shape is «cmf works on three bodies, imf on one», and the first body to get a block will hit the imf side first.

**imf when undeclared — use the engine's existing rule, do not make a second one (Amendment 10, audit).** `engine/chain.yaml@«돌릴 수 있는 **상태** 인가는 별개의 판정이다»` (C28, built): `dynamo_rocky` reads an undeclared `ice_mass_fraction` from `interior.COMPOSITIONS[composition_intent]` slot 1 (earth_like 0.00, water 0.50), with three rules — **a declaration wins · an unknown preset refuses by name («cannot-say (no composition preset)») · the source is printed in the result notes.** The tidal node applies **exactly that rule** for imf, so the engine keeps one answer to «what is this body's water fraction» (the C64 shape avoided). ⚠ **cmf has a precedent too (work seat, Amendment 11):** `interior.solve` itself uses `COMPOSITIONS` slot 0 when `core_mass_fraction` is None (`interior.py@«cmf = preset_cmf if core_mass_fraction is None else core_mass_fraction»` — the place C65 (a) named, and the cause of Mars's −1.87 % at preset 0.325). A tidal node that refuses cmf would therefore give the engine **two answers to one question** (solver: preset radius; node: «unknown») — the C64 shape ① was meant to avoid. Two routes: **(가)** the node takes the same path as C28/C65 for cmf — declaration wins → `COMPOSITIONS[composition_intent][0]` → unknown preset refused by name — and counts preset use with a label (`composition_preset_used`, the C65 shape); **(나)** the node refuses and the mismatch itself is registered as a C64-family item. The audit (same hour, correcting its own «no precedent» line) confirms the table-level precedent — `COMPOSITIONS` is a 4-tuple whose **slot 0 is cmf** (`engine/interior.py@«COMPOSITIONS: dict[str, tuple[float, float, float, str]] = {»`), and `mass_radius_relation`'s `assign(composition=…)` already uses it (the place C65 counts as `composition_preset_used`) — but argues for **refusal by choice, not by absence**: «cmf has a preset path, but this node does not use it and refuses, because a tidal propagator that fills the core size from a preset makes k₂ silently a function of that preset, and nothing in the output would say so.» So the two candidates are: **(가)** node follows the preset route for cmf with the `composition_preset_used` label (work seat: one engine answer to one question); **(나′)** node refuses cmf by name with the stated reason (audit: k₂ must not become a hidden function of a preset; the solver/node mismatch is then registered as a C64-family item rather than hidden). **Decided (directing seat, 2026-09-11): (가)** — one engine answer to one question (declaration > preset with label > unknown preset refused by name). The audit's concern is closed by emitting the label **in this node's own `values`**: `tidal_response` outputs `tidal_composition_preset_used` and `tidal_composition_preset_name` as values (node-prefixed — see Amendment 12), so whenever k₂ is a function of a preset the output says so. dante_fixture's refusal wording unchanged. Under (가) dante_fixture still ends in a named refusal, because it declares neither cmf nor `composition_intent` («cannot-say (no composition preset)»), and that refusal text keeps the inverse-solved wording above. **Refusal wording for inverse-solved bodies:** dante_fixture obtains its cmf by inversion (C65 (b), the −12.51 % case), and that value lives only in `interior_layers.Result.inputs` — the refusal must say «this body's composition was inverse-solved and is not visible in state», not «no declaration», so the next reader does not re-open «why only Dante». Layer densities are then **ρ_layer = (declared fraction × M) / (shell volume between the two radii)** — exact at the converged solution because the integrator places boundaries at the target mass fractions: core = cmf·M over [0, core_radius_m]; rock column (mantle + crust as one density; crust keeps its own μ) = (1 − cmf − imf)·M; ice column = imf·M over [r_ocean_base, radius_m] — ⚠ **one density for ocean + ice shell** in this build (label «ice column homogeneous»); a per-sub-layer split would need per-layer masses that `interior_layers` does not emit, and adding them is a **registered change of its own**, not this brief. g(r) inside each homogeneous layer is then **analytic** (no profile integral). Beuthe's propagator is itself layer-homogeneous (constant ρ, μ, ν per layer), so this is the formalism's native input, not an approximation added by us. **No μ, η or rheology parameter is ever derived from the EoS in this build.**

*Contract clarification (work seat questions, 2026-09-11 11:4x):*
- **Layer naming.** `Structure` carries no named layer list, so the node builds the map **declared layer name → (r_inner, r_outer)** itself from the boundary radii with one fixed table: `core` = [0, core_radius_m]; `mantle` = [core_radius_m, **min of the existing upper boundaries** {r_crust_base, r_ocean_base, radius_m}] — ⚠ not «r_crust_base or radius_m»: `r_crust_base` is the rocky primordial-crust slot (`interior.py@«r_crust_base = None    # 원시 지각 (C11)»`) and is None on ocean bodies, which would let mantle run to the surface and double-cover ocean/ice_shell; `crust` = [r_crust_base, radius_m] when present; `ocean` = [r_ocean_base, r_ocean_top]; `ice_shell` = [r_ocean_top, radius_m] when present. **Why «min» is right (structural, audit):** `interior._stack` orders layers outward as core → rock mantle (rock_deep) → ice column (ice_deep) → primordial crust → gas envelope, so whenever crust and ocean coexist `r_crust_base ≥ r_ocean_top ≥ r_ocean_base`; the minimum of the existing upper boundaries is therefore always the mantle's top. ⚠ **A second rule (audit):** `Structure` has **no `r_ice_base` slot** — the ice-column base is kept only as a pressure (`engine/interior.py@«if stack[layer][1].name == "h2o":»`, whose body assigns `p_ice_base`); `r_ocean_base` is filled only when the material is liquid during integration (:768–769) and `r_ocean_top` only at the end of a liquid interval (:1091). On a body whose ice column is **entirely frozen**, both are None and the mantle map would swallow the ice column silently (mixed density, and the coverage check below would not see it — it is an absorption, not a gap). **Registered rule: if the declared ice mass fraction is > 0 and no ice boundary radius exists, refuse by name** («ice column present, no radius boundary in Structure»). This matters because C62's target class — Beuthe's membrane worlds — are exactly ice-shell bodies; today's roster has no body with imf > 0, so nothing fires yet. After the map is built the node checks that **the layer intervals cover [0, radius_m] with no gap and no overlap** (registered one-line check, same character as the g(R) check; an overlap would be integrated twice by the propagator and would not be caught by name refusals). Whether `r_crust_base` and `r_ocean_base` ever coexist on one body is **not assumed**: the build counts it on the seven bodies; by the stacking order above the order cannot invert, so that count reads as «how often the min-rule actually saw two candidates», not as «did the rule break». A declared name with no boundary pair on this body, or a boundary pair with no declaration, is a **named refusal** («layer «X» declared but absent from the solve» / «solve has layer «Y» with no tidal declaration»). No silent default layer.
- **g(r).** (superseded by Amendment 6) With layer-homogeneous densities, g(r) = G m(r)/r² is analytic from the layer masses; the self-consistency check is **g(R) = G·mass_kg/R² to floating-point precision (registered tolerance: relative 1e-12)**. ⚠ Its scope, named (audit): this is an **arithmetic identity, not a physics check** — with ρ_layer built from declared fractions, Σm_i = M by construction, so the line catches only «layers cover [0, R] without gap/overlap and the fractions sum to 1»; it cannot say whether the layer split matches the structure the integrator actually solved. The check is named `g_surface_identity` so nobody reads it as structure validation. `interior.solve` is **not** opened in this brief; if a later item decides true ρ(r) is needed, storing profiles in `Structure` is a registered change of its own.

##### The equations, with verbatim pointers (all held)

| piece | where it is printed | what we take from it |
|---|---|---|
| propagator y₁′…y₆′ | Beuthe 2015 [`2015Icar..258..239B`](https://ui.adsabs.harvard.edu/abs/2015Icar..258..239B), eqs **(13)–(18)** (layout lines 401–427 of the cached PDF text) | the six ODEs per layer for degree n, with (ρ_r, g_r, μ, ν, χ) from the layer |
| Love numbers from surface values | Beuthe 2015 eq. **(7)**: `(h_n, l_n, k_n) = (g y₁(R), g y₃(R), y₅(R) − 1)` (layout line 336) | the output map |
| liquid-core start (centre → CMB) | Saito 1974 `_saito1974.pdf` (held) §2.3, eqs **(17)–(20)**, printed p. 130 = PDF p. 8 (page image; audit transcription below) | y₇ variable, (y₅, y₇) system in the liquid core, centre start values, three CMB boundary sets — the regular start vectors Beuthe defers to T&S 1972 |
| ↳ verbatim (audit, from the page image) | (17) y₇ = y₆ + (4πG/g) y₂ = ẏ₅ + ((n+1)/r − 4πGρ/g) y₅ · (18) ẏ₅ = (4πGρ/g − (n+1)/r) y₅ + y₇ ; ẏ₇ = (2(n−1)/r)(4πGρ/g) y₅ + ((n−1)/r − 4πGρ/g) y₇ · (19) y₅(r) = rⁿ, r·y₇(r) = 2(n−1) rⁿ · (20) set 1: y^s₁₁(b)=0, y^s₂₁(b)=−ρˡ(b)·y^l₅₁(b), y^s₅₁(b)=y^l₅₁(b), y^s₆₁(b)=y^l₇₁(b)+(4πGρˡ(b)/g(b))·y^l₅₁(b); set 2: y^s₁₂(b)=1, y^s₂₂(b)=ρˡ(b)·g(b)·y^s₁₂(b), y^s₆₂(b)=−4πGρˡ(b)·y^s₁₂(b); set 3: y^s₃₃(b)=1. Self-check: solving (18)'s first line for y₇ reproduces (17)'s second equality. **Counts the build must keep:** the liquid core yields **one** solution, opened into **three** at the CMB with y₁(b), y₃(b) as integration constants — that is the content of the check «did the start vectors come from (19)–(20)» | |
| static limit, whole body (label; Amendment 18 replaces Amendment 17's «quasi-static join») | The build solves the **whole body in the static limit** — Beuthe 2015 eq. (22), «typically applied to the whole body» — so Saito's static core and the solid layers share one formalism (no ω² term anywhere); viscoelasticity enters only through the complex μ̃(ω) (correspondence principle). Output label: **«static limit whole body»** (Beuthe layout 477–482 verbatim: «the static limit consists in setting ω = 0 (22) … typically applied to the whole body»). The Amendment 17 «quasi-static join» label is withdrawn. **Registered consequence (audit):** with ω = 0 everywhere, ω enters only through μ̃(ω) — so (i) the **elastic-limit k₂ is bit-identical under any change of `forcing_period_s`** (registered check — measured: η = 1e30 Pa·s, periods 1 h and 24 h both give k₂ = 0.377442, equal to the elastic limit; thresholds fixed at relative 1e-9 / 1e-6; a change would mean an ω² inertia term survived), and (ii) every period dependence seen in J1–J3 is the rheology's | Beuthe 2015 eq. (22), layout 477–482 (held) |
| fluid-layer limit (ocean/ice shell) | Beuthe 2015 eq. **(27)** `k°_n + 1 = h°_n` (layout line 525), Appendix C membrane cases (h₂ 1.27 Model L / 1.35 Models M, D — P28 T1) | decision (a) label and anchor T1 |
| correspondence principle, complex compliance | Bagheri+ 2022 [`2022AdGeo..63..231B`](https://ui.adsabs.harvard.edu/abs/2022AdGeo..63..231B) §2.3 (Maxwell), §2.5 eq. 18 `J(t) = J_U + β t^α + t/η` (Andrade), §2.6 (Sundberg–Cooper); Q from Im/Re of k̃₂ (§4.3); Renaud & Henning 2018 eq. (11) for the Andrade Im/Re form | μ → μ̃(ω) = 1/J̃(ω) per rheology |
| parameter tables the owner may point declarations at | Henning 2009 Table 2 «Baseline Material Parameters»; Beuthe 2015 Table 7; Renaud & Henning 2018 (α, ζ ranges); Bagheri 2019 Mars fits | P28 candidates table — **none chosen** |

##### Outputs (per body with a block)

`k2`, `h2`, `l2`, `q` — each as `{maxwell, andrade, sundberg_cooper}` plus `band: [min, max]`; `k2_over_q_emitted` (band); `layer_q` per layer; `tidal_composition_preset_used` (bool) and `tidal_composition_preset_name` — **values, not notes** (Amendment 11), **node-prefixed** because `mass_radius_relation` already emits `composition_preset_used` (`engine/chain.yaml@«outputs: [radius_mr_screen, density, composition_preset_used]»`; the methodology's Returns line) and the two answer different questions (screen-radius composition vs tidal layer-model composition) — an unprefixed name would recreate a duplicate-producer key and turn J8's 10 → 9 into 10 → 10 (Amendment 12, audit); labels: `liquid_layer_treatment: membrane_limit (Beuthe 2015 eq. 27)`, `mu_source per layer: declared | material_substitute(<table>)`, `rheology_members_emitted: [...]` with named refusals for members lacking parameters. **Nothing written into `k2_over_q`.**

##### Judgement lines (form fixed here; thresholds = owner)

| # | check | what is compared | source (grade) | pass line |
|---|---|---|---|---|
| J1 | Earth, elastic limit | our k₂ at ω → ∞ (elastic) for an Earth-like layered declaration — ⚠ **the build must state which Earth model's layers it declared** (Wahr's numbers are for PEM-C; a PREM-based declaration differs from PEM-C at the same order as the 2 % threshold candidate, so model choice is part of the comparison) vs **Wahr 1981 k₀ = 0.302, h₀ = 0.609** (body text, layout lines 991–992: M₂ tide, model PEM-C, rotational and elliptical effects included; held `1981GeoJ...64..677W`). ⚠ Trap: Table 4 (layout line 1154) prints the same-looking number pair for the 1066A variant, but those are the deformation scalars S₁·S₂·S₃ — read by position they are **not** (h, l, k) and vs the measured semi-diurnal set Bagheri 2022 quotes: **k₂ = 0.3531, h₂ = 0.6072, l₂ = 0.0843, Q ≈ 10** (Krásná+ 2013; Seitz+ 2012 — second-hand). ⚠ The two differ because the second includes the oceans/anelasticity; the elastic solid-Earth comparison is Wahr's. Henning 2009's «k₂ = 0.3» is an **assumed baseline**, not a measurement — contrast only | held (result) / held (second-hand) / held (assumption) | report only; owner threshold candidates: within 2 % of Wahr's 0.302 / within the spread between the two printed sets |
| J2 | Moon | k₂ **0.02416 ± 0.00022** (Bagheri 2022 §5.3 quoting GRAIL); monthly Q 38 from the **LLR** lineage (Bagheri 2022 layout lines 1645–1646, Williams & Boggs 2015 et al.), not GRAIL — with a declared lunar layering | held (second-hand) | inside ± for some declaration in the rheology band |
| J3 | Mars | k₂ 0.169 ± 0.006 — source **Konopliv** as printed in the held papers: Bagheri 2019 layout lines 645–646 (Konopliv+ 2016) and Bagheri 2022 layout line 1808 (Konopliv+ 2020); Q 95 ± 10 — **Khan 2018** only (cited from the held paper tables, not from P28) | held (result) | as P28: inside ± only for some (μ, η, rheology) — the band is the result |
| J4 | Io | **Renaud & Henning 2018 prints no Io k₂ number** (audit-checked) — the value lives in Bierson & Nimmo 2016 (not held), which R&H only cite; the rest of the held set was **not swept** | — | refusal by name: «Io anchor not found (R&H 2018 checked; full-set sweep pending)» |
| J5 | Beuthe membrane cases | h₂ 1.27 / 1.35 (P28 T1) — **outside this build's scope** (Amendment 18): these are subsurface-ocean-under-shell cases (§3 / eq. C.3), and eq. (27) applies only to a fluid layer reaching the surface; kept as the C62 (c) successor's anchor | held (result) | not run in this build |
| J6 | Dante · Hades · Pandora | Pandora's declared `k2_over_q 0.0016` (board-fitted) and any Dante/Hades declared values (none in body files or boards today) | declaration | **print side by side only** — no verdict, no replacement |
| J0 | homogeneous-sphere classical solution | the propagator on a uniform incompressible sphere vs the closed-form Love numbers, at **three μ values**; registered pass line **0.004 %** (work seat's measured reproduction) | **Beuthe 2015 layout line 1803: the Kelvin–Love formula h₂ = (5/2)/(1 + (19/2) μ̂), μ̂ = μ/(ρ g R) (layout 1789 · 2080), see eq. (E.9)** — printed for **h₂**, not k₂. ⚠ Which quantity J0 compares comes before the threshold: either (가) compare **h₂** against the printed formula, or (나) compare k₂ against k₂ = (3/5) h₂ (homogeneous incompressible limit) **labelled «our arithmetic»**. **Corrected (Amendment 20, work seat): k₂'s closed form is printed too** — Bagheri+ 2022 §4.4 «Quality function of a homogeneous celestial body», eqs **(56)–(57)**: k̄ₙ(χ) = [3/(2(n−1))]·1/(1 + Bₙ/J̄(χ)), Bₙ = (2n²+4n+3)/(n g ρ R); n = 2 elastic (J̄ = 1/μ) gives k₂ = 1.5/(1 + 19μ/(2ρgR)) — a specialisation, not our arithmetic. **J0 therefore compares both**: k₂ vs Bagheri (56)–(57) and h₂ vs Beuthe's Kelvin–Love, plus the cross-check that the two printed forms agree (k₂/h₂ = 3/5 in the homogeneous incompressible limit, registered ≤ 1e-12). Measured at μ = 1e10 · 5e10 · 1.45e11 Pa: k₂ 1.17611/0.63106/0.30041 vs printed 1.17610/0.63104/0.30040 (Δ 9.7e-6 · 2.6e-5 · 3.6e-5); h₂ 1.96018/1.05177/0.50068 vs 1.96017/1.05174/0.50067 | ≤ 0.004 % at all three μ |
| J7 | seven bodies bit-identical | full solves of the roster; plus: a registered node that emits no value on these bodies must **not move** the contract checker's class ③/④ baselines or the lookup count (same line as C64) | gate · `check_contracts` | required |
| J9 (**included — report item, not a judgement line**; directing seat 2026-09-11) | structure-approximation size | the layer-homogeneous model's nmoi — analytic, Σ (8π/15) ρ_i (r_o⁵ − r_i⁵) / (M R²) — **printed beside** the `nmoi` that `interior_layers` emits, for the four roster bodies that solve; ⚠ **not an equality line**: homogeneous layers approximate the true ρ(r), so a non-zero difference is expected — the registered output is «the difference in % per body», which is the size of the approximation the propagator stands on and is used when reading J1/J3 deviations | `interior_layers.nmoi` (held value) | report and register the numbers; no pass/fail |
| J8 | chain.yaml duplicate-producer keys | (Amendment 14: adding `crust_thickness` to `interior_layers.outputs` adds a single-producer key — no effect on the duplicate count) \| registered expectation: **10 → 9** (the two nodes emitting `k2_over_q` become one, the new node emits `k2_over_q_emitted`). ⚠ `chain.py check` does **not** count this today (audit, `engine/chain.py@«def check(g: dict) -> int:»` at acc49b09: edge integrity, node axes, cycles only) — so **adding the duplicate-producer count to `chain.py check` is part of this build** (option (가)); until it lands, the audit script `c65_returns_census.py` (sha256 2c5a198eaed52914) is the measuring tool. Audit's current list of 10: mass · radius · p_rot · present · nmoi · k2_over_q · has_inner_core_solved · b_pol · b_eq · dipole_moment | `chain.py check` (extended in this build) | exact count 9 |

##### Owner decisions this draft leaves open

| # | decision | candidates |
|---|---|---|
| A | thresholds for J1–J3 | inside printed ±; inside 2 %; report only |
| B | which printed μ table is the default `material_substitute` for silicate / ice / iron layers | Henning 2009 Table 2 (silicate baseline); Beuthe 2015 Table 7 (ice shell); none (declare or refuse) |
| C | forcing period for a body without a declared one | orbital period from `orbit_elements`; refuse |
| D | whether `layer_q` is emitted per layer or only the body Q | both / body only |
| E | whether Saito 1974's full fluid-layer propagation for **oceans** becomes the next C-item (the liquid **core** start already uses Saito eqs 17–20 in this build) | yes — reason is scope, not availability (paper held; ocean equations still to be transcribed from page images); defer |
| F | whether Wahr 1981 (elastic, no ocean) or the Bagheri-quoted measured set is J1's primary line | Wahr / measured / both printed |

##### What this build must not do

1. ⚠ **No declared k₂/Q is replaced or overwritten** — `k2_over_q` stays the declaration's; the emitted value has its own name.
2. ⚠ **No value is typed from a paper into code** — μ, η, α, ζ come from body declarations or a named printed table read at build with its hash.
3. ⚠ **No tuning toward Wahr/PREM or any anchor** — J1–J5 report.
4. ⚠ **No ocean/ice-shell fluid-layer treatment beyond the membrane limit** without its own registration (Saito ocean route = decision E); the liquid-core start via Saito eqs (17)–(20) is in scope, the solid-core start (T&S 1972, not held) is refused by name.
5. ⚠ **No coupling to tidal heating, locking or orbital evolution** — emitter only.
6. ⚠ **No body file edits** in this brief; the seven bodies stay bit-identical.

**Size (if registered):** one node file (~200 lines: propagator + three compliances + band), one methodology `Needs`/`Returns` block, one test file (J1–J7), chain.yaml status line; gate: targeted lane + `test_tidal_response`.

*Correction 1 (2026-09-11, audit against the PDFs): Wahr line pointers + Table 4 trap; Moon Q 38 is LLR-lineage not GRAIL; Mars k₂ source is Konopliv (2016 via Bagheri 2019 / 2020 via Bagheri 2022), Khan 2018 only for Q; Io line narrowed to «R&H 2018 checked, sweep pending».*

*Correction 2 (2026-09-11, directing seat + audit): J1 must name the declared Earth model (PEM-C vs PREM ≈ threshold-size); J3 cites Bagheri 2019 lines 645–646 / 2022 line 1808 directly; J4 «R&H prints no number, value is in Bierson & Nimmo 2016 (unheld)»; J5 is a membrane-formula check not a propagator check; J7 adds the contract-checker invariance line; new J8 = duplicate-producer keys 10 → 9.*

*Amendment 3 (2026-09-11): contract clarification for layer naming (name → boundary-radius pair map inside the node, refusals by name) and g(r) (node-side mass integral, labelled, with a g(R) self-consistency line; `interior.solve` stays untouched). File location: this draft sits in `2026-09-09-c20-entropy-band/drafts/`; the 09-11 rule puts foldable drafts in `2026-09-11-interior-state/drafts/` — moving it is the directing seat's call; cite the current path until then.*

*Amendment 4 (2026-09-11, audit): J8's tool — `chain.py check` gains the duplicate-producer key count as part of this build (option 가); audit census script is the interim tool; the current 10 keys are listed.*

*Amendment 5 (2026-09-11, work seat): mantle's upper bound = min of existing upper boundaries (crust base, ocean base, surface), not «crust base or surface» — on ocean bodies the old rule double-covered ocean/ice_shell; coverage check «[0, R] without gap or overlap» registered; crust+ocean coexistence to be counted, not assumed.*

*Amendment 6 (2026-09-11, audit): the input contract asked for ρ(r), P(r), T(r) and a mass profile that the engine does not keep — replaced by the layer-homogeneous model (declared mass fractions + the seven `Structure` boundary radii, which are also the domain of the name map; ρ_layer from fraction × M / shell volume; ice column one density, labelled; g(r) analytic; g(R) check at 1e-12 relative). `interior.solve` stays untouched.*

*Amendment 7 (2026-09-11, audit): structural reason for the min rule (`_stack` order core → rock → ice → crust → envelope); frozen ice column has no radius boundary in `Structure` (no `r_ice_base`; `r_ocean_*` only for liquid intervals) → registered refusal «imf > 0 and no ice boundary radius»; coexistence count re-read as «min saw two candidates».*

*Amendment 8 (2026-09-11, audit): g(R) check renamed `g_surface_identity` with its scope stated (arithmetic identity, not structure validation); proposed J9 = analytic nmoi of the homogeneous layers vs `interior_layers.nmoi`, printed as a % difference per body (report only) — inclusion is the directing seat's call.*

*Amendment 9 (2026-09-11, work seat): cmf/imf live in `Result.inputs`, invisible to `state.get`; routes ①/②/③ recorded, draft default ① (declaration only, node refuses otherwise; count of roster bodies that run = registered number, expected 0); ② would move J8's count in the same commit; ③ is a new model. J9 marked «included, report item» per the directing seat.*

*Amendment 9 decided (directing seat): ① first build; ② follow-up candidate (C64/C71 family, J8 baseline re-take first); ③ separate candidate.*

*Amendment 10 (2026-09-11, audit): declaration counts today (cmf 3 · imf 1); ② does not move J8 (no node outputs the fractions) — precondition lifted by the directing seat, ② stays a follow-up; undeclared imf follows C28's existing rule (declaration > preset from composition_intent > named refusal, source in notes) instead of a new refusal; dante refusal wording names the inverse-solved cause.*

*Amendment 11 (2026-09-11, work seat + audit): cmf precedent exists at table level (`COMPOSITIONS` slot 0, used by `mass_radius_relation`/`interior.solve`, counted by C65); candidates (가) follow the preset route with the `composition_preset_used` label vs (나′) refuse by choice so k₂ never becomes a hidden function of a preset (register the mismatch); decided (가) with `composition_preset_used` emitted in the node's values.*

*Amendment 12 (2026-09-11, audit): the preset-label values are node-prefixed (`tidal_composition_preset_used`, `tidal_composition_preset_name`) — `composition_preset_used` is already `mass_radius_relation`'s output (C65, `engine/chain.yaml@«outputs: [radius_mr_screen, density, composition_preset_used]»`), so the unprefixed name would create a new duplicate-producer key and break J8's 10 → 9. Decision (가) itself unchanged.*

*Amendment 13 (2026-09-11, work seat): the map's domain is the five reachable `interior_layers` values (radius · core_radius · ocean_thickness · ice_shell_thickness · crust_thickness), not the seven `Structure` slots (invisible to the node; `r_grad_*` are not boundaries anyway); derived radii listed; R⊕/km unit conversion centralised and tested. Folded into ledger C62 (b) at `883c0508`; this amendment goes to the same ledger sentence in the work seat's next commit.*

*Amendment 14 (2026-09-11, audit): `crust_thickness` is in `values`/Returns but not in `chain.yaml` outputs → this build adds it to outputs and declares the five edges (route 가); the 40-key Returns-vs-outputs gap is a separate candidate item, tool `c62_outputs_vs_returns.py`.*

*Amendment 15 (2026-09-11, audit): the `interior_layers` `values` count is **21** (measured; graph declares 14; contract Returns 21; difference 7 = C73's interior_layers share) — the earlier «14»/«16» wordings corrected; the «five boundary keys» statement is unaffected.*

*Amendment 16 (2026-09-11, work seat + directing seat): Saito 1974 is held (`_saito1974`) — the three «not held» wordings corrected; this build uses Saito §2.3 eqs (17)–(20) as the liquid-core start (closing the gap Beuthe defers to T&S 1972 / Sabadini & Vermeersen, both unheld); ocean stays membrane limit ((a) unchanged); decision E's reason becomes scope; solid core (μ > 0) start values → named refusal (T&S 1972 not held).*

*Amendment 17 (2026-09-11, audit): Saito (17)–(20) transcribed verbatim from the page image (printed p. 130 = PDF p. 8) with the (17)/(18) self-check; the one-solution-in-the-core → three-at-the-CMB count registered; the quasi-static join (static Saito core, ω-bearing Beuthe layers) named as a label.*

*Amendment 18 (2026-09-11, work seat + directing seat): (a) split — surface fluid layer → eq. (27); subsurface ocean under a shell → Beuthe §3 membrane (Λ, δρ°) outside this build, named refusal, C62 (c) successor; J5 out of scope for the same reason; the «quasi-static join» label withdrawn — the build is the whole-body static limit (Beuthe eq. 22) with complex μ̃(ω), label «static limit whole body»; new registered check J0 = homogeneous-sphere classical solution at three μ, 0.004 %.*

*Amendment 19 (2026-09-11, audit): static-limit wording tied to Beuthe layout 477–482; registered consequence — elastic k₂ bit-identical under forcing-period changes, all period dependence is rheology; J0's printed closed form is the Kelvin–Love h₂ (Beuthe layout 1803, eq. E.9) so J0 compares h₂, with k₂ = (3/5)h₂ only as a labelled our-arithmetic side line.*

*Amendment 20 (2026-09-11, work seat): k₂ closed form is printed (Bagheri 2022 §4.4 eqs 56–57), so J0 compares both k₂ and h₂ against printed forms plus their 3/5 cross-check (≤ 1e-12); measured values recorded; period-invariance check measured (k₂ 0.377442 at 1 h and 24 h). Tests rc = 0; check_contracts running.*

### C62 (b) — the build, 2026-09-11 — and the four places the papers decided the scope

⚠ **It stands, and the check that says so is internal.** Shrink the core until the stack is one uniform
density and the propagator must reproduce what the held papers print for a homogeneous body — Bagheri+
2022 eqs (56)(57) for `k̄ₙ`, and Beuthe's Kelvin–Love form for `h₂`. Measured at μ = 1e10 · 5e10 ·
1.45e11 Pa:

| μ [Pa] | our `k₂` | Bagheri (56)(57) | our `h₂` | Kelvin–Love |
|---|---|---|---|---|
| 1.0e10 | 1.17611 | 1.17610 | 1.96018 | 1.96017 |
| 5.0e10 | 0.63106 | 0.63104 | 1.05177 | 1.05174 |
| 1.45e11 | 0.30041 | 0.30040 | 0.50068 | 0.50067 |

Worst relative difference **3.6e-05**. ⚠ *Four things have to be right at once for that to come out* —
Saito's three start vectors at the core-mantle boundary, Beuthe's six ODEs, the surface conditions and
eq. (7). And the two printed forms are checked against **each other**: `k̄₂ / h₂ = 3/5` in the
homogeneous incompressible limit, held to 1e-12, so neither had to be re-derived on our side.

**J1, Earth, printed and not tuned.** A two-layer Earth (core 3480 km, cmf 0.325) against Wahr 1981's
`k₀ = 0.302`, `h₀ = 0.609`: at μ = 2.0e11 Pa `k₂ = 0.3106` (+2.9 %) and `h₂ = 0.5643` (−7.3 %); at
2.1e11, `k₂ = 0.3010` (−0.3 %) and `h₂ = 0.5466` (−10.2 %). ⚠ **The two cannot be matched at once by two
homogeneous layers, and that is the result** — PEM-C is not this stack. The test prints three rigidities
side by side rather than electing the one that lands on 0.302.

**J9, the size of the approximation.** The homogeneous stack's `nmoi` is **0.3457** against Earth's
measured **0.3307** — **+4.5 %**. That is how far the propagator's layer stack sits from the structure
the integrator solves, and it is the number to read J1's deviations against.

**The static limit is the whole body's, and the consequence is now a test.** Beuthe prints it as eq. (22)
and calls it *"typically applied to the whole body [e.g. Wahr et al., 2006]"*; viscoelasticity enters
through the complex μ̃(ω) alone. ⚠ *So there is no quasi-static join to assume between a static core and
a dynamic mantle — neither is dynamic*, and an earlier instruction to label one was withdrawn because the
code does not make that assumption. What the code does make is testable: with η = 1e30 Pa·s, `k₂` is
**0.377442 at a 1-hour forcing period and 0.377442 at 24 hours**, equal to the elastic limit. If the ω²
inertial terms were live, that would move.

**J8, measured in the checker rather than by hand.** `chain.py check` now counts keys that two nodes
declare as `outputs`, and it prints **9 (registered 9)** — the 10 the audit counted became 9 because
`tidal_response` emits `k2_over_q_emitted` and `k2q_class_table` keeps `k2_over_q` alone. ⚠ *Pinned as a
**set**, not a count* — the lesson C64 B bought this morning, where one key leaving and another arriving
would have cancelled out.

⚠ **Four places where a paper, not a preference, set the scope.**

| what | what the paper actually prints | what the build does |
|---|---|---|
| the three solutions regular at the centre | Beuthe defers them to Takeuchi & Saito 1972 eqs I(98)–I(103), and the static solid-layer propagator matrix to a book — **neither is held** | Saito 1974 §2.3 closes it: eq. (17)'s continuous `y₇`, eq. (18)'s two-variable liquid system, eq. (19)'s centre start, eq. (20)'s three start vectors at the boundary. ⚠ *Saito was downloaded by the owner on 2026-09-11 for exactly this gap, and three sentences of the pre-registration still called it paywalled* |
| a **solid** core | the start values are in the unheld paper | **refused by name**, not invented. A declaration-decided branch |
| an ocean under an ice shell | Beuthe's eq. (27) holds *"if the fluid layer reaches the surface"* — the superscript marks that **the surface layer behaves as a fluid**. The subsurface case is his section 3's membrane approach | **refused by name**, with both reasons: the cited equation answers a different question, and Saito prints start vectors for climbing back into a solid **only** at the core-mantle boundary. Registered as **C62 (c)** |
| J5 (`h₂` 1.27 / 1.35) | those are values of the membrane approximation | ⚠ **cannot stand in this build, and it is printed rather than dropped** — a registered judgement line that the scope decision removed. It becomes C62 (c)'s anchor |

⚠ **And a second one was caught before the commit, in C73's other direction.** The node's `outputs`
listed **seventeen** keys while the contract's `Returns` listed **eight**, and the code emitted all
seventeen — the four `*_band` keys, the two labels and the two self-checks were missing from the
contract (audit seat, 2026-09-11, on the pre-commit hashes). ⚠ *It passed only because no body runs the
node*: the first body to declare a block would have met a checker that had never seen nine of its
values. Left alone it would have made C73's reverse direction **1 → 10 on the day that item was
listed** — a new item's first act being to grow the thing it names. The nine went into both contract
mirrors before the commit. **A contract that is right only while nothing exercises it is not right.**

⚠ **A registered line did not hold, and the two registrations contradicted each other.** J7 said the
contract checker's class ③/④ baselines would not move. ④ did not; **③ moved 0 → 1** — `tidal_response`'s
`Needs` carries the declaration block, and no roster body supplies it. *That is decision ①'s registered
state seen from the other side*: «nobody declares it» and «the Need is supplied by some sample» cannot
both be true, so the pre-registration asserted two things that exclude each other and this seat noticed
only when the checker printed it. ⚠ **And the path it took is the part worth keeping.** The audit seat
proposed that line as a **question** — *does a registered node that emits no value on any body move the
class ③/④ baselines and the lookup count?* — and the draft wrote it down as **an invariant**. Three
seats then read that page and none of them saw the conversion. *A question becoming a prediction is a
step nobody reviews*, and that is the structural version of this; «which seat missed it» is not. The baseline moves to (1, 1, 1) with the reason written in
`check_contracts.py`, and the cell empties by itself on the day a body declares a block. ⚠ *The failure
is in the registration, not the code — which is the case a pre-registration exists to produce.*

⚠ **Today's roster has no body with an ice mass fraction above zero and none declares a `tidal_response`
block, so the number of roster bodies this node runs on is zero.** J1–J3 stand on declared test bodies,
not on the roster, and every seven-body solve is bit-identical by construction. *That is the registered
shape of decision ①, not a disappointment* — but it does mean the anchors are the only evidence this
node has, and they are listed above with their gaps rather than their agreements.

### C15 (a) 2026-09-10 — wiring core entropy into the rocky dynamo ladder — **pre-registration draft, before any build**

⚠ **Nothing built, nothing decided.** C15's row has read `open (status: gap)` since Brief 44: *"the
supplier exists (Brief 60); what is missing is the consumer wiring through φ and core entropy"*. This
draft says what the consumer wiring would have to be, what today's numbers actually are, and **which
three of its questions a seat may not answer.** *Written before the build so that the answer cannot be
chosen after seeing it.*

#### The item is three edges, not one

`engine/chain.yaml` carries **three** gap edges into `dynamo_rocky`, and they are three different kinds
of gap. The pre-registration names all three, because a build that closes one and leaves the other two
unmentioned will read afterwards as though C15 were finished.

| edge | kind | status today |
|---|---|---|
| `core_entropy_production → dynamo_rocky` (`influences`, sign non-monotonic) | ⚠ **value exists, no verdict can be drawn** — φ is emitted and its band crosses zero | the edge C15 owns |
| `heat_transport_mode → dynamo_rocky` **via `cmb_heat_flux`** (`selects`) | value exists, **consumer does not read it** — `cmb_heat_flux` has emitted `q_cmb` since Brief 60, `tidal_heating` has supplied the §6.2 mode label since C30 | untouched by this draft |
| `internal_heat_nontidal → dynamo_rocky` **via `geotherm`** (`requires`) | value exists, **consumer does not read it** — C20's `core_thermal_history` emits `core_cmb_temperature_present` and `q_cmb_present` | untouched by this draft |

**So the honest scope line is:** C15 (a) is about *whether a quantity that cannot decide may enter a
gate that must decide.* The other two edges are about a consumer that never asks, which is a wiring
brief and not this one.

#### What the ladder's gate is today, read from the code

`dynamo_rocky.ladder` decides "alive" from **three labels and no formula** — `conductor_phase` from
`core_state` (`liquid` / `solid` / `undecided`), with a **declared** `dynamo_alive` standing in *only*
while `conductor_phase` is undecided (C29 (c), owner). It reads neither φ, nor `q_cmb`, nor any
temperature. ⚠ **That is the whole of the alive gate**, so "wiring entropy" means, concretely, adding a
fourth thing to a three-label gate that currently has no numeric input at all.

#### What φ actually is today — measured for this file

`python3 engine/test_core_entropy.py` (2026-09-10, this file's run):

| path | T_c | ΔE | band (8 corners) | corners positive | H = 0 corner |
|---|---|---|---|---|---|
| the engine's own Earth, on C14's solved T_c | **3770 K** | **−78 MW/K** | **−181 … +172** | **4/8** | **−85** |
| the same profile at the owner's declared horn | 3760 K | **+27** | (E_L 69 · E_g 170 · E_H −56) | — | — |
| the same profile at 4000 K, inner core gone | 4000 K | **−162** | (E_L = E_g = E_H = 0) | — | — |

Terms on the first row: E_R 6 + E_s 78 + E_L 29 + E_H −24 + E_g 73 − E_k **242**. Integration width
against a 4× finer step: **1.2 MW/K** — two orders below the declared band, which is the useful part of
that number.

⚠ **The sign of ΔE is set by which horn is declared, not by the entropy budget.** 3760 K gives **+27**
and 3770 K gives **−78**: ten kelvin of declaration, 105 MW/K of answer, because the inner-core terms
(E_L, E_g, E_H — all three carry dR_i/dt) switch on and off with it. *A quantity this sensitive to a
declaration cannot be the thing that overrules a label.* And the threshold cannot help: the paper's own
required excess is *"probably ∼100 MW K⁻¹, but could lie anywhere within the range 0.1–1000"* (§5.2), so
**the band and the threshold overlap in both directions.**

#### ⚠ Two defects found while writing this draft — moved out of C15's scope

Both are recorded as a **separate candidate (C64)**, not as part of this item: `c64-entropy-verdict-key-draft.md`
in this directory. *The reason they are not folded in here is that C15's scope is one edge, and a
pre-registration that also carries a repair is a pre-registration that can be satisfied by the repair.*
⚠ **One of them touches this brief's own inputs**, though, so it is named in (d) below: `core_entropy`
emits a history verdict as a **literal refusal** naming a dependency that has since been built.

#### The decision lines — candidates recorded, none chosen

- **ⓐ How may a band that straddles zero enter a gate that must decide?** Candidates: **(i)** it may
  not — φ stays a printed side-channel with a count, the ladder unchanged (today's behaviour, and the
  node says so in its own notes: *"the threshold cannot decide, so it has no standing to overwrite the
  ladder"*); **(ii)** φ becomes a **fourth label** that can only move `liquid` → `undecided`, never
  `undecided` → `liquid` — i.e. it may withdraw a verdict but not grant one; **(iii)** φ gates only when
  **all eight corners share a sign**, and prints `cannot-say (band straddles zero)` otherwise;
  **(iv)** φ replaces the phase label where both exist. ⚠ **(iv) moves shipped verdicts** and is the one
  a seat may not take.
- **ⓑ Which temperature the budget is taken at** — C58's shape in a second place. Today it is the
  **declared** horn where one exists and C14's solved T_c otherwise, and the two differ by 105 MW/K on
  Earth. Candidates: keep the declaration-wins rule and print both; take C20's present-day endpoint
  (which is a third number again); refuse when the two disagree by more than the band's width.
- **ⓒ Whether `q_cmb` is wired in the same brief** — the second gap edge. Candidates: one brief for both
  (φ and Q_C-vs-Q_k are the paper's own pair, printed side by side); φ alone now and `q_cmb` later; neither
  until ⓐ is decided.

#### Registered before running — each line in a form a run can contradict

⚠ **Written this way on the audit seat's criterion (2026-09-11): a registered line that no test can
disagree with is not a line.** C58 (a)'s ⓓ was first written as *"this brief changes answers"*, which
nothing could refuse; inverted to bit-identity it became measurable. Each line below therefore names the
field or file a run would read to contradict it.

1. **Under ⓐ(i) — the side-channel candidate — every roster body whose `dynamo_rocky` is applicable
   returns a bit-identical result**, the whole `values` dict and not the alive label alone.
   *Contradicted by:* one differing key on one body. ⚠ **The comparison set is stated up front**: bodies
   where the node is out of domain are excluded, and **how many were excluded is printed**, so an empty
   comparison cannot pass as agreement.
1b. ⚠ **Under ⓐ(ii) and ⓐ(iii) the verdict is designed to move, so bit-identity is the wrong line and is
   not registered for them.** What is registered instead is the **direction**: **no body moves toward a
   dynamo.** Not one goes `undecided → liquid`, or dead → alive, because of ΔE; movement is
   withdrawal-only. Every body that moves is **named**, with its **corner count** (`x/8`) and its band
   printed beside it, and **how many moved is a printed integer**. *Contradicted by:* one body gaining a
   dynamo it did not have, or a withdrawal that appears with no name and no corner count. *(The audit
   seat found that lines 1 and «must not» 1 as first written forbade what (ii) and (iii) are for: this
   brief's own measurement puts Earth at **4/8 corners positive**, so under (ii) Earth is a withdrawal
   candidate on day one.)*
2. **Both numbers appear as values, not prose** — the entropy label and the phase label — plus a third
   value naming **which one the verdict came from**. *Contradicted by:* a run where the verdict differs
   from both, or where the naming field is absent while both are present. *(C58 (a)'s lesson: prose can
   be grepped but only a value can be counted.)*
3. **The straddle fallback is a printed integer.** How many bodies got `cannot-say (band straddles
   zero)` is a value in the result, as `core_gamma_fallback` is. *Contradicted by:* a run where a body
   takes that branch and the counter does not move.
4. **A body with no solved T_c still refuses by name**, and the refusal string does not contain a dynamo
   verdict. *Contradicted by:* the refusal turning into "no dynamo", or into a silent `False`.
5. **An outcome outside 1–4 is registered as its own kind before it is reported**, not folded into one
   of the four.

#### What this brief must not do — each stated as a property, not an intention

1. ⚠ **ΔE may never *grant* a dynamo — only withdraw one.** *The property:* in any run, no body's
   alive label becomes more alive (`undecided → liquid`, dead → alive) as a consequence of ΔE, whatever
   the band does; a **withdrawal** is permitted, and only under ⓐ(ii)/(iii). *Contradicted by:* a body
   that gains an alive label when only ΔE changes. ⚠ *An earlier draft of this line said the label must
   be derivable from `conductor_phase` alone — that forbade (ii) and (iii) outright, i.e. it forbade the
   thing they exist to do. The asymmetry is the point: a quantity whose threshold spans four orders of
   magnitude may take a verdict away, because that direction only ever loses information, and may not
   hand one out.*
2. ⚠ **The temperature the budget is taken at is printed, and it equals the declaration where one
   exists.** *The property:* a value field carries the temperature used and a second one carries where it
   came from. *Contradicted by:* a body with a declared core-side T_cmb whose printed budget temperature
   is not that number. *(The 105 MW/K between 3760 K and 3770 K is what picking silently would decide.)*
3. ⚠ **`entropy_history_verdict` is byte-identical across this brief's commit.** C64 owns that repair.
   *Contradicted by:* the key's value differing before and after — and **the check already exists**:
   `engine/test_core_entropy.py@«2: 이 노드는 이력 판정을 **내지 않는다**»` pins the exact string, so
   this line needs no new test and must not build one. *(That the pinning test is itself C64's problem
   does not change what it does here: while C64 is open, it is this line's check.)*
4. ⚠ **The row does not close, and the two other edges stay named.** *The property:* `chain.yaml` still
   carries `status: gap` on `heat_transport_mode → dynamo_rocky` and `internal_heat_nontidal →
   dynamo_rocky`, and C15's row text names both. *Contradicted by:* a row reading "closed" while either
   edge is untouched.

#### Owner decisions this surfaces (none taken)

| # | decision | candidates | label |
|---|---|---|---|
| (a) | how φ may enter the alive gate | (i) side-channel only · (ii) may withdraw a verdict, never grant one · (iii) gate only when all eight corners share a sign · (iv) φ replaces the phase label | ⚠ **owner pending** — (iv) moves shipped verdicts |
| (b) | which core temperature the budget is taken at | declaration wins and print both · C20's present-day endpoint · refuse when the two disagree beyond the band | ⚠ **owner pending** — 105 MW/K on Earth between two numbers ten kelvin apart |
| (c) | whether `q_cmb` is wired in the same brief | both together (the paper's own pair) · φ first · neither until (a) | ⚠ **owner pending** |
| (d) | what happens to `entropy_history_verdict`'s literal | C15 asks C20 · C15 stops emitting the key · leave and count it | ⚠ **owner pending** — a defect this draft found, not a design choice; recorded as **C64** and outside C15's scope |

**Size (estimate):** no new physics. One label path in `dynamo_rocky`'s alive gate, one printed count,
one note line, and the before/after table over the roster — plus whichever of (a)–(d) the owner elects.

### C64 — one key, two producers, and the two read paths answer differently — **listed 2026-09-11**

⚠ **The verdict line, written so that a run can contradict it.** `entropy_history_verdict` is emitted by
**two nodes**, and **the two ways the engine reads a value give different answers for it in the same
run** — `state.get(...)` returns the **first** applicable node's value, `state.resolved` the **last**.
*The measurable form is the condition, not the claim*: it holds **exactly when both nodes are
applicable in the same run**, and it is falsified by a roster body where one of them is out of domain.

| where | what it emits | how it gets there |
|---|---|---|
| `engine/core_entropy.py@«**`entropy_history_verdict` 를 여기서 내지 않는다**»` | a **literal** refusal | C15's node says *"I cannot answer until C20 exists"* |
| `engine/core_history.py@«"entropy_history_verdict": (ws["verdict"]»` | a **computed** verdict (`NOT_CONVERGED` when the sweep did not converge) | C20's node, built 2026-09-04 |
| `engine/state.py@«if r.applicable and key in r.values:»` | the **first** match wins | `_find` iterates `self.results.values()` and returns on the first hit |
| `engine/state.py@«out.update(r.values)»` | the **last** writer wins | `resolved` merges every applicable node's values in order — **and emit, the evidence dump and the board comparison read this one** |

#### The conditions, measured before the claim (2026-09-11)

1. ⚠ **The declaration branch is dead, so it is not part of the claim.** `state.py@«"""조회 한 번의 순수한 부분 — 기록하지 않는다. 선언된 입력이 먼저, 그 다음 도출값."""»`
   makes `_find` check declared inputs **before** any node's values — so a declared key would beat both
   nodes on that path while `resolved` still returned the last node. **No body declares this key**
   (`engine/bodies/*.yaml`, 0 files), and it is a verdict key, so none is expected to. *Measured, and it
   removes a branch from the claim rather than adding one.*
2. **`applicable` is therefore the only live condition.** `resolved` skips a node that is out of domain,
   and `_find` skips it too — so on a body where only one of the two nodes applies, **both paths agree**,
   and that agreement is not evidence against this item. **The one thing to count is: how many roster
   bodies have both nodes applicable in the same run.** If that number is zero today, the item is a
   latent defect rather than a live one, and the row must say which.
3. ⚠ **No consumer reads either key today**, which is why this survived. It becomes a wrong answer the
   moment one does, and *which* wrong answer depends on the door it comes in by.

#### ⚠ The contract layer says it too, and nothing counts that

Both contracts in **one document** list the same key in their `Returns`:
`docs/reference/internal-heat-luminosity-methodology.md@«`inner_core_branch_taken` [—] · `entropy_integration_width` [W/K]»`
(`core_entropy_production`) and
`docs/reference/internal-heat-luminosity-methodology.md@«`delta_e_present_hi` [W/K] · `entropy_history_verdict` [—]»`
(`core_thermal_history`). `check_contracts` compares **each node against its own** `Returns`, so both
pass — **there is no check that counts one key claimed by two nodes.** *That is a new shape in the C45
family, and it is cheaper than the output-side check: comparing contracts needs no body to run, so it
fires at registration time rather than on the first body that happens to exercise both nodes.*

⚠ **And the contract prose asserts the literal**:
`docs/reference/internal-heat-luminosity-methodology.md@«**This recipe does not return `entropy_history_verdict`**»`. So a
repair moves **three** places, not one — the code, the test that pins the string
(`engine/test_core_entropy.py@«2: 이 노드는 이력 판정을 **내지 않는다**»`), and the contract line. **Each
is a baseline movement and each needs its own name**; fixing the code alone would leave the contract
stating the opposite of the code.

#### The scope, widened by measurement — six keys, not one

⚠ **The audit seat ran the contract-side count this draft asked for** (document scan, no run, using
`check_contracts`'s own parser, 2026-09-11): **168** keys are listed across the contracts' `Returns`, and
**six** are claimed by **two nodes**.

| key | the two claimants | live? |
|---|---|---|
| `dipole_moment` · `b_eq` · `b_pol` | `dynamo_giant` / `dynamo_rocky` | ⚠ *claimed harmless by body-class exclusivity* — the two ladders refuse each other's classes, so the pair should never both apply. **Not asserted here: it is one row of the count below**, which settles it by measurement instead of by argument |
| `entropy_history_verdict` | `core_entropy_production` / `core_thermal_history` | **this item** |
| `has_inner_core_solved` | `core_energy_balance` / `core_entropy_production` | **split 2026-09-13 (C68 B) — no longer live**: the answer fact is `has_inner_core` (`core_energy_balance`) and the execution fact is `inner_core_branch_taken` (`core_entropy_production`), so no node emits this name. *Was: live candidate — both are rocky-core nodes, so both applying is the expected case.* |
| `radius` | `interior_layers` / `mass_radius_relation` | ⚠ **pre-listed, and split out as C65 if the count says it is live** — *the whole engine reads `radius`*, unlike a verdict key nothing consumes |

**So the one line to count is widened**: for **each of the six**, how many roster bodies have **both**
claimants applicable in the same run, and where that number is non-zero, **what the two values are**.
*That is one run of the roster, not six.*

⚠ **And the direction must be read from the execution order, not from `chain.yaml`'s declaration
order** — this seat measured both and they disagree. `run.solve` walks `graph.order(g)`, a topological
sort, and `state.results` fills in **that** order; `chain.yaml`'s mapping order is a different sequence.
For `radius` the two answers are opposite:

| pair | declaration order in `chain.yaml` | **execution order** (`graph.order`) | so `state.get` returns | and `resolved` returns |
|---|---|---|---|---|
| `radius` | `mass_radius_relation` 13 · `interior_layers` 14 | ⚠ **`interior_layers` #25 · `mass_radius_relation` #27** | `interior_layers` | `mass_radius_relation` |
| `entropy_history_verdict` | `core_thermal_history` 21 · `core_entropy_production` 22 | `core_thermal_history` #37 · `core_entropy_production` #43 | `core_history`'s computed verdict | `core_entropy`'s literal |
| `has_inner_core_solved` *(split 2026-09-13, C68 B — the row records the state before the split)* | — | `core_energy_balance` #35 · `core_entropy_production` #43 | `core_energy_balance` | `core_entropy_production` |

*The `entropy_history_verdict` direction happens to be the same either way; `radius`'s is reversed.*
⚠ **A relayed ordinal is not the order** — the numbers 12/13 and 20/21 that reached this seat were
declaration positions, one-based off by one from this file's own count, and using them would have printed
the `radius` disagreement backwards. **So an ordinal must name which order it is**, wherever it is
printed: `chain.yaml`'s declaration position and `graph.order`'s execution position are different
sequences and only the second decides who wins a key. ⚠ *The audit seat reproduced the cause in its own
tool: it read `g.get("order") or list(g["nodes"])`, and `graph.load()` returns no `order` key at all — so
the `or` was an **unnamed fallback** that silently handed back the declaration order, and the number was
printed as though it came from the real thing. That is C58's own shape inside the tool built to audit
C58.*

#### Why this is a family member, not a typo

C45 (f) is *a contract key given a literal call-site default, counted by nothing*. C61 is *a step never
tallied reading as a step that passed*. This is the third form, and the family's signature is one
sentence: **there was a check, and the check agreed.** The test asserts the refusal, the contract asserts
the refusal, and the refusal's own reason — *"needs C20"* — expired on 2026-09-04 when C20 was built.

#### Candidates, none chosen

| # | candidate | what it moves |
|---|---|---|
| (i) | C15's node **asks C20** for the verdict | a new dependency edge; C15's node stops being self-contained and gains a refusal for "C20 not run" |
| (ii) | C15's node **stops emitting the key** it cannot compute | one key leaves a values dict — a contract change, `check_contracts` re-run, and the pinned test renamed |
| (iii) | keep the literal, **name it and count it** | cheapest, and C58 (a)'s shape: the string stays, a counter says how many nodes refuse on a dependency that exists |

⚠ **Measured, and it is a class**: six keys, four pairs (above). The contract-side count came first
because it is a document scan; the run-side count — both claimants applicable on the same body — is the
one still open, and it is scheduled after the next gate END. ⚠ **`radius` leaves this item if it is
live**: it becomes **C65**, because a key the whole engine reads is a different item from a verdict key
nothing consumes, and C64 must not grow into it (directing seat, 2026-09-11).

**Size:** (iii) is a few lines plus a counter; (i) and (ii) are contract changes. No physics moves in any
of the three.

### C46 — the table is short of rows, and cut on a different axis — **listed 2026-09-07, not started**

C34 settled *which quantity* is fed to the §6.2 transport table. This is the other half: **what the
table cuts on, and whether its rows are the literature's rows.** Venus is where it surfaced — the
document prints it as the stagnant-lid anchor at 10–20 mW/m², and the engine computes 37.75 and returns
plate tectonics.

**The literature's set is five, from a held paper's full text.** Lourenço+ 2020
([`2020GGG....2108756L`](https://ui.adsabs.harvard.edu/abs/2020GGG....2108756L), 24 pp, text layer
intact) builds a regime diagram and states its criteria outright:

| regime | criterion, verbatim from §3.4 |
|---|---|
| mobile lid | time-averaged **mobility > 0.5** |
| stagnant lid | time-averaged **mobility < 5×10⁻³** |
| **heat pipe** | the stagnant-lid criterion **and eruption efficiency = 100 %** |
| plutonic-squishy lid | **quiescent plateness ≥ 0.4** |
| episodic lid | mobility between 5×10⁻³ and 0.5, **and** plateness < 0.4 |

⚠ **A pre-registration was wrong, and in a useful direction.** It was expected that our *heat pipe* row
would turn out to be Turcotte's Venus proposal rather than one of the literature's regimes. **It is one
of them** — but **not as a third rung above plate tectonics.** It is a *sub-case of stagnant lid*, the
one where every drop of melt erupts. **Our ladder orders the three by increasing flux; the literature
nests one inside another.** That is a structural mismatch, not a missing row.

**What cuts the regimes is surface kinematics**, and the definitions are printed:

    mobility     M = v_rms(surface) / v_rms(mantle)          Lourenço §3.1, after Tackley 2000
    plateness    from f₈₀, the surface-area fraction over
                 which 80 % of the deformation occurs        Lourenço §3.3, after Weinstein & Olson 1992

The control parameters of the diagram are **yield stress (20–300 MPa) and eruption efficiency** at a
reference viscosity of 10²⁰ or 10²¹ Pa·s. **No heat flux appears anywhere in the criteria.**

**Moresi & Solomatov 1998 cuts on the same kind of axis and names a number.**
[`1998GeoJI.133..669M`](https://ui.adsabs.harvard.edu/abs/1998GeoJI.133..669M), *"Mantle convection with
a brittle lithosphere: thoughts on the global tectonic styles of the Earth and Venus"* — ⚠ **read from a
rendered page image, because this PDF has no text layer at all** (294 bytes of extraction, all of it ADS
stamps; a `grep` of it returns 0 for everything and that 0 means nothing). Its summary: high yield
stress → stagnant lid, low → mobilized, **intermediate → episodic cycling**, and *"mobilization of the
Earth's lithosphere can occur if the friction coefficient in the lithosphere is less than
**0.03–0.13**"*. On Venus, *"the friction coefficient may be high as a result of the dry conditions, and
brittle mobilization of the lithosphere would then be **episodic and catastrophic**."*

⚠ **So the literature gives Venus two different answers, and neither is a row we have.** Moresi &
Solomatov say **episodic**; Lourenço and Smrekar+ 2023 point at **plutonic-squishy lid**. Both are
non-stagnant, both are absent from our table.

⚠ **And the sharpest part: we could not adopt their axis if we wanted to.** Mobility and plateness are
**outputs of a 4.5 Gyr convection simulation** — `v_rms` of a surface against `v_rms` of a mantle, and
the area fraction carrying 80 % of the strain rate. **For a body we will never observe, neither is
measurable.** Yield stress and friction coefficient are rheological properties we do not have either.
**That is why our own document says what it says**: *"there is no published W/m² boundary between the
modes, because the real criterion is melt fraction and any flux threshold is a conversion, not a
citation."* The flux ladder is a proxy for an axis we cannot reach, and this item is about admitting
that rather than adding two rows.

⚠ **Which also means the document contradicts itself, and the contradiction is now sourced.** The same
document that denies a published flux boundary uses a flux ceiling table to assign modes. C34's
decision is untouched by this — it was about which quantity is fed, and Mercury, Earth and Mars still
come out at the document's labels. **Venus moves here.**

**Still at abstract level, and labelled as such**: Smrekar+ 2023's 11 ± 7 km → 78 ± 69 mW/m² and its
squishy-lid conclusion (the held copy is the one-page conference abstract, which carries the numbers
without method or errors), and Turcotte 1989's heat-pipe proposal for Venus with its 150 km lithosphere
and 200 km³/yr requirement. ⚠ **Smrekar+ 2018 and Turcotte 1989 are not held** — the first is
paywalled, the second failed at the gateway. **No statement here rests on them beyond what an abstract
supports.**

### C46 (b) built 2026-09-07 — the flux is a sieve, and it sieves almost nothing

**Owner**: *"B로 해보자. 금성/지구 어떻게 나오나 예시가 좀 궁금하네."* So the recipe stops choosing a
regime and emits **the set the flux is compatible with**.

⚠ **No threshold was invented, because inventing one is the disease this item names.** The only honest
relation available is: collect the heat-flow values the literature **actually prints** per regime, and
exclude a regime **only** where our number falls outside a printed range. Lourenço+ 2020 §4.3 prints
them, for an Earth-sized model, averaged over the last 2 Gyr:

⚠ **A correction to the row below, and it changed the finding.** This section first recorded mobile lid
as *"conductive 35–45 TW, magmatic low"* — one component numeric, so no printed ceiling on the total.
**The same section prints the total**, and this seat missed the line while the directing seat found it:
*"the total surface heat flow (i.e., the sum of magmatic and conductive heat flows) for cases with a
mobile lid obtained in our simulations are ∼40–50 TW"*, with that paper's own Earth reference at
**44.4 TW** (Turcotte & Schubert 2014). **Mobile lid is bounded on both sides; the other three are not.**

| regime | printed | kind |
|---|---|---|
| mobile lid | **total 40–50 TW** | both bounds |
| stagnant lid | magmatic **up to 30–35 TW**; conductive "generally low" | one bound, one word |
| episodic lid | magmatic **up to 20 TW**; conductive "intermediate" | one bound, one word |
| plutonic-squishy lid | magmatic **up to ~10 TW**; conductive "intermediate", "very high compared to a stagnant lid" | one bound, one word |
| heat pipe | **nothing** — it is stagnant lid at 100 % eruption efficiency, defined by eruption, not flux | none |

⚠ **The TW → W/m² conversion is ours** (Lourenço §2: *"realistic parameter values and physics
descriptive of planet Earth"*), and **the printed values are per component.** Where one component is a
number and the other is a word, **the total has no printed ceiling** — so that regime cannot be
excluded from above at all. That single fact is why the sieve barely sieves.

**The output, run rather than written** (`solve_mode`, engine values):

| body fed | total | ladder cell | compatible | excluded |
|---|---|---|---|---|
| Earth, measured **46 TW** (Korenaga 2008) | 0.0902 W/m² | plate tectonics | **4** — mobile, stagnant, episodic, squishy | **none** |
| Venus, our own scaled estimate | 0.03775 W/m² = 17.4 TW | plate tectonics | 3 | **mobile lid** |
| Venus, Smrekar+ 2023 **measured 78 mW/m²** | 0.078 W/m² = 35.9 TW | plate tectonics | **4** | **none** |
| Venus, that value's upper error, 147 mW/m² | 0.147 W/m² = 67.7 TW | ⚠ *unclassified* | **4** | **none** |

⚠ **This paragraph said the opposite until the missed line was found, and the correction matters.** It
read: *the one exclusion is an artefact of our own number, and fed Smrekar's measurement it vanishes.*
With the floor at **40 TW** rather than 35, it does not vanish:

| body fed | total | mobile lid |
|---|---|---|
| Earth, measured | 46 TW | **compatible** — the only body that is |
| Venus, our estimate | 17.4 TW | excluded, below the floor |
| Venus, Smrekar measured | 35.9 TW | **excluded**, still below the floor |
| Venus, upper error | 67.7 TW | **excluded**, now above the ceiling |

**So the axis does separate Earth from Venus, on measured values, and in the direction the literature
says** — Venus lacks plate tectonics (Smrekar+ 2018). ⚠ **The earlier reading was wrong because one
sentence of a held paper had not been read**, not because the reasoning was loose: the conductive
component alone gives 35 TW and no ceiling, and that is what was recorded. **A component read in place
of a total was the whole of the error.**

**What still stands from the band**: the other three regimes cannot be excluded from above at all, so
Earth at 46 TW remains compatible with stagnant lid, episodic and squishy. **The candidate set never
falls below three across four decades of flux**, and a test pins that.

⚠ **And the ladder cell is no longer called a regime.** `mode` stays in the output because eight
consumers read it, but the note beside it now says what it is: **the §6.2 flux-ladder cell, not a
tectonic regime.** The two were the same word before, which is how a flux threshold came to look like a
classification.

**The sentence that was a footnote is now the finding.** Our own document already said it: *"there is no
published W/m² boundary between the modes, because the real criterion is melt fraction and any flux
threshold is a conversion, not a citation."* This section is that sentence with the measurement attached.

### C46 — the ladder, built 2026-09-07: always one cell, and the cell is an analogy

**Owner**: *"이것보다는 크다를 기준으로 종류를 확정지어버리는게 어때?"* — so the flux picks **one** cell,
by the highest rung it passes. No ceiling is needed, which also disposes of `unclassified`: the top
cell has no upper edge.

⚠ **Corrected 2026-09-07 — the version of this table built earlier today had the lowest rung upside
down.** What stands now is below; what was wrong and how it was found is C46 (c).

| cell | bounded by | W/m² | where the number comes from |
|---|---|---|---|
| stagnant lid | **a ceiling** | Venus **10–20** · Mars **15–30** · union 10–30 for any other body | Reese, Solomatov & Moresi 1998 ([`1998JGR...10313643R`](https://ui.adsabs.harvard.edu/abs/1998JGR...10313643R)), ⚠ **body not held — ADS abstract only.** *"the critical heat flux which can be removed without widespread melting"*, from finite-element simulations of stagnant-lid convection — **a model output, and two different numbers for two bodies.** ⚠ **No floor, and none is wanted**: a colder body is *more* stagnant, not less |
| plutonic-squishy lid (ceiling exceeded) | that same ceiling, from below | above its own ceiling, under 0.09 | ⚠ **our join of two papers, not a sentence in either.** Reese+ 1998 says a stagnant lid asked to pass more than its ceiling melts widely; Lourenço+ 2020 §3.4's plutonic-squishy lid is a lid that stays immobile and carries melt. Does not collide with Smrekar+ 2018's *no plate tectonics on Venus* — squishy is a sub-kind of immobile lid |
| plate tectonics | **a floor** | **0.09** | §6.2's Earth, and Earth's is a measurement (92.1 mW/m², 47±2 TW from 38,347 observations, [`2010SolE....1....5D`](https://ui.adsabs.harvard.edu/abs/2010SolE....1....5D)). ⚠ **Independently bracketed by body text we hold**: Lourenço's mobile-lid TOTAL of 40–50 TW is **0.0784–0.0980 W/m²** over Earth's area, and 0.09 sits inside |
| heat pipe | **a floor** | **2.5** | §6.2's Io — Kankanamge & Moore 2019's melt-carried flux for Io's parameters. ⚠ the one rung that is still nothing but an analogy to a single body |

⚠ **The floors are not boundaries. They are what bodies we know actually radiate**, so they carry
their own origin word `analogy-rung` — not `printed`, not `chosen`, not `provisional`, not a grade.
What the ladder says is *"Earth's worth of heat, Earth's worth of crust"* and nothing stronger, and
the output says that in words. ⚠ **The bottom of the ladder is not of that kind at all** — it is a
ceiling from a paper whose body we do not hold, so it carries a fifth word, `abstract-level`. Three
cells, three different provenances; earlier today all three shared one word.

⚠ **Therefore Earth coming out `plate tectonics` is not evidence. That rung is Earth.** Its margin is
**0.2 %** (0.0902 against 0.09), and the test that pins it says in its own comment that it is a
tautology recorded so nobody reads it as a verdict.

**What the ladder produces:**

| body fed | flux | cell (corrected ladder) |
|---|---|---|
| Earth, measured | 0.0902 W/m² | plate tectonics |
| Venus, 78−69 = 9 mW/m² | 0.009 | stagnant lid — under its own 20 mW/m² ceiling |
| Venus, 78 mW/m² *(the measurement)* | 0.078 | **plutonic-squishy lid — 3.9× its own ceiling** |
| Venus, 78+69 = 147 mW/m² | 0.147 | **plate tectonics** |
| Pandora | 45.36 | heat pipe |

⚠ **One error bar still crosses three cells** — but no longer one unnamed one. Smrekar's 78 ± 69 mW/m²
puts Venus under its ceiling, over its ceiling, and on the Earth rung depending on where in its own
uncertainty you read it. **The one-cell answer is that thin**, which is why the band travels beside it
in the same output rather than being replaced by it.

### Re-scored 2026-09-07 with a body that is not one of our rungs

⚠ **Every anchor this project had been scoring with defines the cell it is scored against.** The plate
rung *is* Earth, the stagnant rung *is* the Venus–Mars pair, the heat-pipe rung *is* Io. **So 3 of 4 or
2 of 2 measured arithmetic, not the ladder.** Two papers were fetched to break that:

**The Moon — the only body in no rung.** Langseth, Keihm & Peters 1976
([`1976LPSC....7.3143L`](https://ui.adsabs.harvard.edu/abs/1976LPSC....7.3143L)) ⚠ **read from page
images; the text layer is 609 bytes of ADS stamps.** Apollo 15 Hadley Rille **2.1 μW/cm²**, which the
paper calls *"representative of the regional value"*; Apollo 17 **1.6**, corrected to **1.4** as the
best regional estimate; and a global average of **1.8 μW/cm² = 18 mW/m²** from measured surface thorium
and inferred crustal thickness. ⚠ This paper exists to **replace** Langseth+ 1972/1973 — the
conductivities are 30–50 % lower — so the older values must not be cited. And it says of its own global
figure that *"the need is emphasized for extended areal coverage"*.

**Mars — an independent method on a rung body.** Parro+ 2017
([`2017NatSR...745629P`](https://ui.adsabs.harvard.edu/abs/2017NatSR...745629P), open access): preferred
model **14–25 mW/m², average 19**, and *"we propose an upper limit of 20 ± 1 mW m⁻² for the present-day
global average"*. The method — crustal and mantle radiogenic production scaled by crustal thickness and
topography, anchored on polar elastic thickness — has nothing to do with a stagnant-lid flux conversion.

⚠ **Re-run on the corrected ladder** (the table below is the second version; the first was scored
against the inverted rung and is void — see C46 (c)):

| body | flux | cell | | what the score is worth |
|---|---|---|---|---|
| **Moon** | 18 mW/m² | stagnant lid | ✓ | **independent, and still independent** — the Moon anchors no cell, is an undisputed one-plate body, and 18 mW/m² is an *in situ* measurement. ⚠ It stayed independent only because the stagnant cell was given **no floor**. Making the Moon's 18 that floor was the obvious way to build the cell, and it would have spent the only non-circular score this ladder has |
| Mars | 19 mW/m² | stagnant lid | ✓ | the 19 (Parro+ 2017) comes from a method unrelated to the ceiling — but the ceiling read here is **Mars's own 15–30**, so the score is half circular |
| Venus | 78 mW/m² | **plutonic-squishy lid** | ✗ / ✓ | ⚠ **the ladder now contradicts our own document and agrees with the paper the document cites.** §6.2's anchor column labels Venus a stagnant lid; 78 mW/m² is **3.9×** Venus's own 10–20 ceiling, and Reese+ 1998's criterion for exceeding it is *widespread melting* |
| Earth | 0.0902 W/m² | plate tectonics | ✓ | **circular**: that rung is Earth |
| Io | 2.5 W/m² | heat pipe | ✓ | **circular**: that rung is Io |

**Independent 1 of 1. Self-scored 3 of 4** — ⚠ **and the two are not added**, because summing them
counts a tautology as evidence. Mercury has no measured surface heat flow at all and is scored nowhere.

⚠ **What looked like a superseded rung was a misread form.** Yesterday this section recorded that
Smrekar+ 2023's Venus measurement (78 mW/m²) is four to eight times the 10–20 that
[`1998JGR...10313643R`](https://ui.adsabs.harvard.edu/abs/1998JGR...10313643R) gives for Venus, and
concluded that *"the measurement that sets half of our lowest rung was replaced twenty-five years
later, and the rung did not move."* **That was wrong about what the 1998 number is.** It is not a
value Venus was observed to emit — it is the *ceiling* Venus would have to stay under to shed its heat
by conduction, and 78 exceeding it is **the criterion firing, not a stale rung.** Nothing is
superseded; the two papers agree, and together they say Venus's lid is melting. The anomaly was the
verdict.

### C34, re-scored on the corrected ladder — the count moves, and which function you score decides which way

⚠ **The version of this section written earlier today is void.** It scored the fed quantity against a
ladder whose lowest rung was a ceiling turned into a floor, so its 1-of-2 and 2-of-2 mean nothing.
This is the re-run, and every cell below came out of `regime_ladder_cell` rather than out of arithmetic
done by hand.

C34's decision — **what the transport table is fed** — was made on `transport_mode`, the function that
reads §6.2's three-row table literally. That function is **unchanged**, and it still reproduces exactly
what C34 recorded:

| fed quantity, scored on `transport_mode` (unchanged) | §6.2 anchor labels reproduced | fails |
|---|---|---|
| low end — tidal + radiogenic, current | **3 of 4** | Venus |
| high end — measured surface heat flow | 1 of 4 → **2 of 3 scored** | Venus; Mercury has no measured flux to feed |

The C46 ladder cell is a **different function**, and on it the count reverses:

| fed quantity, scored on `regime_ladder_cell` | §6.2 anchor labels reproduced | independent | fails |
|---|---|---|---|
| low end — tidal + radiogenic, current | **2 of 4** (Mercury 15.75 ✓ · Mars 15.87 ✓) | — | **Earth 41.80**, and Venus 37.75 |
| high end — measured surface heat flow | **2 of 3 scored** (Earth 92.1 ✓ · Mars 19 ✓) | **Moon 18 ✓** | Venus 78; Mercury unscored |

⚠ **One body moved, and it is Earth.** At the low feed Earth's 41.80 mW/m² is above the 30 mW/m²
ceiling and below the 90 mW/m² plate rung. `transport_mode` calls that **plate tectonics** — correctly,
by its own docstring, because *"the table has nothing between the ceiling and the plate row, so a body
under the ceiling is not called unknown, it is called plate tectonics."* **That was a free pass, and
naming the gap took it away.** The C46 ladder now has a cell there, so the same 41.80 reads
`plutonic-squishy lid` and Earth becomes a fail. Venus fails under both feeds and on both functions, so
Venus is not what discriminates.

**⚠ All four of C34's candidates are now identified, and two of them are disqualified.** The
decision has been carrying them as four readings of one quantity; they are four different quantities.

| candidate | what it actually is | fit to be fed to a §6.2 threshold |
|---|---|---|
| **0.0418** W/m² | Earth's **radiogenic production**, `radiogenic.py` default set (21.3 TW) — C47 | ✗ **wrong quantity**: the thresholds are surface heat flow |
| **0.0769** | `mantle_flux.implied_flux` at `T_m ≈ 1600 K` — Nimmo+ 2004 eqs 34–36, a **model surface flow** reading no measurement | ✓ right quantity, ⚠ but a **mobile-lid** law: C47 (b) measures it handing Mars 2.9–5.7× Reese's own ceiling |
| **0.08** | ⚠ **no source, ever** (`98774764`, 2026-06-23; `git log -S` finds no cited version). 2.1× both held radiogenic estimates, 87 % of the measured total — **and the same document uses it under the other label**, §5 calling Io's 2 W/m² *"an order of magnitude above **Earth's** ~0.08"*, where only the total makes the comparison work | ✗ **disqualified** — no source, and two labels for one number |
| **0.0921** | Earth's **measured surface heat flow**, Davies & Davies 2010 (47 ± 2 TW) | ✓ right quantity, ⚠ but exists for **three bodies in the solar system and none of ours** |

⚠ **So the four-way choice was never four-way.** One candidate is a different quantity (C47), one has
no source, and of the two survivors the measured one cannot be computed for any body in this project.
**What is left is 0.0769 — the only candidate that is both the right quantity and computable
everywhere — and C47 (b) shows it fails on Mars.** That is why C34 does not close by choosing.

**⚠ Status changed 2026-09-07: this does not close by choosing, and it is not being put to the owner.**
Two of the four candidates are disqualified outright, the measured survivor cannot be computed for any
body in this project, and the computable survivor fails on Mars (C47 (b)). Asking for a choice now would
be asking which disqualified value to adopt. **Held until C47 closes**, at which point the candidate set
is re-drawn rather than re-ranked.

⚠ **Not resolved here, and not resolvable here.** Which function C34 should be scored on is the same
question as whether §6.2's missing row should exist — and the owner has already been given that gap as
C46. The low feed's 3-of-4 was true and is still true of the function it was measured on; it is not
true of the function that fills the gap C46 opened. **Reporting both and picking neither is the whole
of what this section does.**

### C46 (c) 2026-09-07 — the lowest rung was a ceiling stood on its head

**A brief told this seat to build the stagnant cell as a floor at 0.010 W/m². The instruction was
wrong, and our own document already said so.** This is where that is recorded, because the value it
produced was plausible and the gate passed it.

**What the source actually prints.** Reese, Solomatov & Moresi 1998
([`1998JGR...10313643R`](https://ui.adsabs.harvard.edu/abs/1998JGR...10313643R)) — ⚠ **body not held;
every AGU and ADS scan returns 403, so the abstract is all of it** — reads verbatim:

> *"For Venus, the critical heat flux which can be removed **without widespread melting** is only
> 10-20 mW/m². For Mars, it is 15-30 mW/m²."*

and gets there by *"thermal boundary layer analyses as well as finite element simulations of stagnant
lid convection with non-Newtonian viscosity."* Three facts follow, and the floor version had all three
backwards. It is a **ceiling**, not a floor. It is a **model output**, not a measurement. And it is
**two numbers for two bodies**, not one number for a pair.

**Where the merge happened, checked line by line rather than taken from the brief.** In
`docs/reference/tidal-heating-methodology.md`:

| line | what it says | verdict |
|---|---|---|
| §6.2 table row | *"ceiling **10–30 mW/m²** \| Venus 10–20, Mars 15–30"* | ✓ **correct** — the word `ceiling` is there and the two bodies are apart |
| §6.2 prose | *"put the stagnant-lid conductive ceiling at 10–30 mW/m² before widespread melting sets in"* | ✓ **correct** — `ceiling` again; the two bodies are merged, harmlessly |
| §6.2 bullet | *"**0.09 W/m² is Earth** and **10–30 mW/m² is the Venus and Mars pair.** Same reading."* | ✗ **the one that inverted it** — `ceiling` is gone, the bodies are merged, and the sentence above it calls the whole column *"three measured bodies"* |

**So the document was right twice and wrong once, and the wrong one is the one that got read.** The
bullet sits under a heading arguing that these numbers are bodies rather than thresholds — a true and
useful point about Earth and Io that is false about this pair, since 10–30 is neither a body nor
measured. Both the bullet and that heading are corrected in the same commit as the code.

**What the corrected ladder does that the floor version could not.** Venus's measured 78 mW/m²
(Smrekar+ 2023) had been the ladder's embarrassment: on the floor version it read `stagnant lid`,
agreeing with our anchor column for the wrong reason, and yesterday's note called the rung
*superseded*. With the ceiling restored and split per body, 78 is **3.9× Venus's own 10–20** and the
cell becomes `plutonic-squishy lid` — which is Reese's own criterion (*widespread melting*) joined to
Lourenço+ 2020 §3.4's regime for a lid that stays immobile and carries melt. ⚠ **That join is ours**,
in neither paper's words, and it is labelled as ours in the code. It does not collide with Smrekar+
2018's *no plate tectonics on Venus*: squishy is a sub-kind of immobile lid. **The anomaly was the
verdict.**

**Two things this seat decided rather than was told, and both are reversible.**

1. **The stagnant cell was given no floor.** The obvious build — brief 142's own sketch has it — makes
   the Moon's 18 mW/m² the bottom rung. That is a real value a real body emits, so it would have been
   a legitimate `analogy-rung`. ⚠ **It would also have consumed the only non-circular anchor this
   ladder has.** The Moon is the one body that scores a cell it does not define; the moment it becomes
   the rung, scoring the Moon against it is as empty as scoring Earth against Earth. A stagnant lid
   needs no floor anyway — a colder body is *more* stagnant, not less — so the cell is bounded above
   only, and `BELOW_LADDER` is gone: a cold body is a stagnant lid, and the Moon and Mars are measured
   there.
2. **A body with no published ceiling gets the Venus∪Mars union, 10–30, transferred to it.** ⚠ The
   transfer is ours. Reese solved two bodies, and a conduction ceiling is a function of each body's
   size, gravity and rheology. Every invented body in this project takes this path, so the label
   travels in the output.

**Three cells, three provenances, where yesterday all three shared one word.** `analogy-rung` was
applied to the whole ladder; it fits only the heat-pipe rung now. Earth's 0.09 is bracketed by body
text we hold (Lourenço's mobile-lid **total** 40–50 TW = 0.0784–0.0980 W/m²), and the stagnant ceiling
carries a fifth origin word, **`abstract-level`**, because its paper's body is unread.

**The knot this cell sits in, written in both places it binds:** *a correct surface heat flow needs
the regime, and placing the regime needs the surface heat flow.* C46 needs the flux to place the cell;
the flux needs a boundary-layer law, and which law applies is the regime. ⚠ **A stagnant-lid law does
not cut the knot** — C47 (c) tested that and removed it: Korenaga 2009's conventional stagnant-lid
scaling gives the same Earth→Mars flux ratio as the mobile-lid law we already had, 0.723 against 0.724,
because `D` cancels and both go as `g^{1/3}`. **A law that spans both regimes would cut it**, which is
what makes Foley & Bercovici 2014 the candidate worth a build. Until then this cell's bottom stands on
an abstract-level ceiling, and no single regime is emitted.

⚠ **What caught this was a person, not the gate.** The floor version computed correctly, emitted its
reasoning in words, and passed a full lane. A ceiling used as a floor is not a wrong number — it is a
right number carrying the wrong sign of an inequality, and no check in this repo tests the direction of
an inequality against its source. That is the same class as the two errors this seat was corrected on
earlier: **the gate catches wrong values; it does not catch a conclusion given a status it has not
earned.**

#### The C21 premise, re-measured — what was arithmetic is now a measurement

C21's design says *"a uniform 4 Myr step cannot see the pulse at all"* and proposes 0.1 Ma steps for
the first ~10 Ma. ⚠ **The step is no longer uniform** (Brief 157), so that sentence's arithmetic no
longer decides anything. One column of the existing runs, printed — no new model and nothing
pre-registered:

| body | steps inside the first 10 Ma | `h` at the first step | `h` at t ≈ 1.4 Ma (C21's ²⁶Al threshold) | `h` at the window's edge | steps with `h` < 0.1 Ma |
|---|---|---|---|---|---|
| **Earth** | **14** | 0.3929 Ma | 0.5201 Ma | 1.3041 Ma | **0 / 14** |
| **Mars** | **56** | 0.005279 Ma | 0.1431 Ma | **0.906071 Ma** | **32 / 56** |

- **C21's 0.1 Ma sampling is still needed, and Earth is why.** At t ≈ 1.4 Ma one Earth step is 0.520 Ma —
  about **1.4 samples per ²⁶Al half-life** (0.73 My, Monteux+ 2016). The adaptive step does not stand in
  for C21.
- ⚠ **But three phrases in C21's design are now wrong or unproven and must be restated at its start:**
  *«a uniform 4 Myr step cannot see the pulse at all»* — 14 steps land inside the window, not none;
  *«there is no other way»* — unproven; *«≈100 steps on top of C20's ~1 100»* — the base is 1 152 and 14 of
  the 100 already exist.
- ⚠ **The premise's truth is body-dependent, which is itself new.** Mars, whose start is far stiffer, already
  takes **56** steps in the window with **32** of them under 0.1 Ma — so on Mars the adaptive step nearly
  does what C21 proposed to add, while on Earth it does not.
- ⚠ **The Mars row is labelled by its initial mantle temperature, because two defensible runs differ in
  the fourth decimal.** This row uses `engine/bodies/mars.yaml`'s **printed 4021.0 K**; test ⑥ and step 0
  use **4800/r_b = 4021.0474 K**, and at the window's edge that run gives **0.905921 Ma** against this one's
  **0.906071 Ma** (window count 56 and the cap count 1123/1197 identical in both). ⚠ *And what the label
  does **not** move, measured: the present `T_p` and `T_c` are identical to four decimals (1382.8969 K,
  3893.0083 K) and the step count is 1197 either way — but **the 3.7 Ga column does move, by 0.0014 K**
  (1669.2199 against 1669.2213), so "the label only changes the step size" would be wrong. Both round to
  the 1669.22 the criterion-B table prints, against 4.29 K of headroom.* ⚠ **So the audit seat's
  0.905921 and this table's 0.906071 were never a transcription error — they are two runs 0.047 K apart in
  `T_m0`**, which is `docs/reference/derivation-discipline.md@«A number cannot enter without its label»` in
  its smallest possible form.
- **Method, so this is not mistaken for a new model or for a second measurement of step 0.** The two
  integrations were **re-run** at this tree (~57 s each; the stage-0 JSON carries per-run scalars only, no
  rows), and `h` between consecutive rows *is* the step the integrator took
  (`engine/core_history.py@«t_next = 0.0 if h == remaining else t_now + h / GYR_S»`). ⚠ **Only `t_gyr` was
  read out of the rows and no temperature was**, so criterion B's blinding held while this was measured —
  which is also why this table can sit in the commit that fixes the rule.

**C21 is still not started, and this does not re-judge its design** — it replaces a claim that was
arithmetic with a number, so that whoever opens C21 re-weighs the premise instead of inheriting it.

### C49 — one engine declares `k_core` twice, and one declaration's ground forbids the other's number — **listed 2026-09-09, not started**

**Found while reading the entropy band's inputs (brief 164), by looking at where `k` comes from.**

| | rocky path | sub-Neptune path |
|---|---|---|
| where | `engine/cmb_flux.py@«K_CORE = 50.0»` | `engine/sub_neptune_dynamo.py@«CORE_CONDUCTIVITY = Band(»` |
| shape | **one declared midpoint, 50, ± 20** → `K_CORE_RANGE` = (30, 70) | **midpoint `None`**, ends **40** and **100**, plus an unmade `Choice` with both candidates |
| source | Nimmo+ 2004 Table 1's own ±, one paper | **two** papers, as Tang+ 2025 runs them both — Konôpková+ 2016 ([`2016Natur.534...99K`](https://ui.adsabs.harvard.edu/abs/2016Natur.534...99K)) 40, Pozzo+ 2012 ([`2012Natur.485..355P`](https://ui.adsabs.harvard.edu/abs/2012Natur.485..355P)) 100. ⚠ **And the module's own bibcode for Konôpková was `2016ApJ...817..107K`, which resolves to nothing in ADS** (`numFound` 0) — corrected 2026-09-09; this seat had copied it into this row before checking |
| grade | declared | calibrated |
| consumed by | `core_entropy.K_RANGE`, `core_history.K_CORNERS`, and `cmb_flux`'s `q_ad` band | the sub-Neptune dynamo verdict, which **refuses to run until the `Choice` is made** |

⚠ **The sharp part is not that the two differ. It is that one of them says the other's number does not
exist.** `sub_neptune_dynamo.py`'s comment, one line above its band, reads *"70 W/m/K 는 두 논문 중 어느
쪽도 말하지 않은 수다"* — **and 70 is exactly the upper corner the rocky path feeds to the entropy
budget** (`K_CORE_RANGE`'s top, `K_CORNERS`'s second element). So a ground written down in one file to
exclude a value is, in another file, the value in use. ⚠ **And it is the corner that does the work**:
C25 (c) measured `k` = 70 as the corner that turns eight of nine `ΔE` rows negative.

**What this is and is not.** It is **not** a claim that 50 ± 20 is wrong — Nimmo's Table 1 prints it, and
`cmb_flux`'s own note places it inside Gaidos+ 2010's 28–100. It is that **two paths in one engine hold
the same physical quantity in two shapes with two grades, and the newer one's reasoning contradicts the
older one's arithmetic.** Deciding it is part of **owner decision ②** in C25 (b) — keep the ±, elect a
camp, or unify on the two-paper form — and no value is changed by listing it.

⚠ **One thing did move, and it is a citation rather than a value.** The sub-Neptune module attributed its
40 W/m/K to Konôpková+ 2016 under the bibcode **`2016ApJ...817..107K`**, and that bibcode **resolves to
nothing in ADS** — `numFound` 0, checked 2026-09-09 through `ADS_API_TOKEN`. The paper is *"Direct
measurement of thermal conductivity in solid iron"*, **Nature 534, 99**,
[`2016Natur.534...99K`](https://ui.adsabs.harvard.edu/abs/2016Natur.534...99K), 253 citations. The value
is unchanged — Tang+ 2025 is what runs 40 and 100 — and only the pointer is fixed. ⚠ **This seat had
already copied the dead bibcode into the row above before checking it**, which is
`docs/reference/derivation-discipline.md@«A number whose source was not stated is quoted without one; an invented source is harder to catch than a missing one.»`
happening to the seat that quotes that rule.

⚠ **Otherwise nothing moved.** Both `k` declarations stand exactly as they were; this entry is the record
that they cannot both be right about 70.

### C50 — contracts list `Needs` that no body on the roster supplies, and four of them are C37's exact signature — **listed 2026-09-09, not started**

**Found by the instrument C45 (b) registered and C45 (c) ran.** Every number below is a measurement of
the current tree, not an estimate.

**Class ① — the C37 signature, live in four places.** The recipe looks the key up, **no sample body
supplies it**, and the resulting `None` is filed in `Result.inputs` **under that same name**, so the
contract check saw a name and reported agreement:

| node | key |
|---|---|
| `body_class` | `gas_mass_fraction` · `semi_major_axis_au` |
| `dynamo_rocky` | `dynamo_regime` |
| `interior_layers` | `porosity_cap` |

**Class ③ — a `Needs` item no roster body supplies, where the call site copes** (a default, or the
evidence filed under another name). **8 nodes · 8 distinct keys · 13 (node, key) occurrences:**

| key | nodes that declare it in `Needs` |
|---|---|
| `core_material` | `cmb_heat_flux` · `core_energy_balance` · `core_entropy_production` · `core_thermal_history` |
| `ice_mass_fraction` | `dynamo_rocky` · `internal_heat_nontidal` · `interior_layers` |
| `differentiated` · `envelope_z` · `gas_mass_fraction` · `initial_porosity` · `tidal_heating` | `interior_layers` |
| `permanent_quadrupole` | `tidal_locking` |

⚠ **Each of these is one of two different faults, and which one is not decidable from the count.**
Either **the contract is wrong** — the value arrives from a composition preset or a call-site default,
so it was never a *need* — or **the body declarations are missing** and the recipe has been running on a
fallback nobody noticed. `core_material` looks like the first (the call sites pass `"fe_prem"` as a
default); `permanent_quadrupole` and `envelope_z` look like the second. **Deciding each is the repair,
and the repair can move values** — which is why this is listed rather than done.

**What holds the line meanwhile.** The four class-① instances are named in
`engine/check_contracts.py@«이 집합 밖의 사례는 FAIL 이다»` and **anything outside that set fails the gate**; the class-③
count is recorded as a baseline (`CLASS3_BASELINE` = 8 nodes · 8 keys · **13 pairs**) and printed on
every run. ⚠ **So the disease is
frozen at its measured size rather than fixed** — new instances of either class are caught immediately,
and the existing ones are visible in the gate's own output on every run.

⚠ **No owner decision is involved.** This is a repair of the engine's own declarations against its own
contracts; nothing here is an art or physics choice.

**When this closes:** when the four class-① pairs are repaired and
`engine/check_contracts.py@«이 집합 밖의 사례는 FAIL 이다»`'s set is **empty** — at which point class ① is
simply a gate rule with nothing grandfathered — and when class ③'s printed baseline reaches **(0, 0)**,
which promotes that class to a `FAIL` as well.

#### ⚠ A fifth shape, harder to catch than C37, and one instance is already in the list

**`porosity_cap` was in class ① only by luck.** `engine/interior.py@«inputs["porosity_cap"] = P_LAB_MAX»`
— the inversion branch — **wrote the evidence dict directly with a real number that came from no
lookup at all** (⚠ *removed in Brief 170 B; the line the anchor now lands on is the comment recording
that removal, and C50 (b)'s correction 170 C says why the neighbouring `initial_porosity` write was a
convention and stayed*). On a
body that takes that branch the evidence therefore reads `porosity_cap = 0.3` or whatever `P_LAB_MAX` is,
**not `None`** — and the checker's class-① test is `inputs[key] is None`. ⚠ **So "the lookup missed and
the evidence was filled with a constant" is structurally invisible to today's check, and it is worse
than C37**: C37 left a `None` that a reader might notice, while this leaves a plausible number.

**It shows up here only because some sample body does *not* take the inversion branch**, leaving the
`None` for the checker to find. **The detection is one line and it is not built here:** *does a key
whose lookups all missed later appear in `inputs` with a **non-`None`** value?*

**Two instances are known, both in the same two lines of `interior.py`:**

| key | where it lands in class ① / ③ | what the branch writes |
|---|---|---|
| `porosity_cap` | class ① (only because some body skips the branch) | `P_LAB_MAX` |
| `initial_porosity` | class ③ | `phi`, the inverted value |

⚠ **`initial_porosity` is the cleaner example of the shape**: its evidence is the number the inversion
*solved for*, so the contract check sees a plausible value that no body declared and no lookup returned.
**Named, with its detection and both instances, and left for the repair brief.**

⚠ **And the two instances land in *different* classes — `porosity_cap` in ①, `initial_porosity` in ③ —
which settles where the detection belongs: outside the class split.** It is a **fourth test**, run on
every node regardless of which class its keys fall into: *does a key whose lookups all missed later
appear in `inputs` with a non-`None` value?* **Building it inside either class would catch one instance
and miss the other**, and the shape is the same shape in both.

⚠ **A neighbouring gap, found the same week by a gate failure rather than by a checker — named as a C52
candidate at the end of this file** (*Brief 166 D, 2026-09-09*): C45 asks whether a node's lookups are
declared, and C50 asks whether a declared `Needs` is supplied. **Neither asks how many nodes' recorded
anchors depend on one shared module constant** — and one of them, `core_energy.H_CORE`, turned out to hold
up the reproduction anchors of a different node entirely.

### C51 — the missing term: a stagnant-lid energy budget, so that secular cooling is an output — **pre-registered 2026-09-09, before any of it is built**

⚠ **This section is committed before the build.** The owner chose the third path — *build the missing
term* rather than close the entropy band by picking numbers inside it (C25 (f)) — and this is what that
means in equations, with what will count as a pass fixed first.

#### What is actually missing, in the sources' own words

`heat_transport_mode` is fed **radiogenic production**, while §6.2's thresholds are defined on **surface
heat flow** (C47). The term between them is named where C47 quoted it — Korenaga 2008 §2: *"Loss of
internal energy is balanced primarily by (1) heat production from radiogenic elements and (2) a decrease
in the primordial heat content of Earth (i.e. **secular cooling**)"*, and *"the present-day internal heat
production is about 20 TW …, so **the rest of the surface heat flux must be from secular cooling**."*

⚠ **And the flux law is not what is missing.** Foley 2018 ([`2018AsBio..18..873F`](https://ui.adsabs.harvard.edu/abs/2018AsBio..18..873F), **held**)
writes the stagnant-lid capacity as

> (3) `F_man = c₁ k (T_p − T_s)/d · θ^(−4/3) Ra_i^(1/3)`, with *"We use **c₁ = 0.5** and a_rh = 2.5"*,

citing Reese+ 1998/1999, Solomatov & Moresi 2000 and Korenaga 2009 — **and that is the equation this
engine already transcribed** as Korenaga's eq. 30, whose `n = 1` exponents are exactly `−1−β = −4/3` and
`β = 1/3`. **What is missing is the budget around it:**

> (1) `V_man ρ c_p dT_p/dt = Q_man − A_man F_man − f_m ρ_m (c_p ΔT_m + L_m)`
> (2) `ρ c_p (T_p − T_l) dδ/dt = −F_man − k ∂T/∂z|_{z=R_p−δ}`
> (4) `T_l = T_p − a_rh R T_p² / E_v`

**`dT_p/dt` in (1) *is* secular cooling**, and this engine has no equation that ties the mantle's heat
capacity to its radiogenic supply and its surface loss.

⚠ **(1) carries a third term this engine cannot supply, and it is named here rather than dropped
quietly.** `f_m ρ_m (c_p ΔT_m + L_m)` is volumetric melt production times the heat it removes, and this
engine has no melt-production node. **Pre-registered handling:** stage 1 evaluates (1) **twice** — at
`f_m` = 0 and at the melt term needed to change the answer by 10 % — and reports both, so the size of
the gap is printed rather than assumed small. ⚠ *If the 10 % melt production implied is physically
absurd for the present epoch, that is itself the finding, and it is a stronger statement than setting
`f_m` = 0 with a footnote.* **Neither number is a verdict cell**; the cells are below.

#### The design decision, fixed here

⚠ **Stage 1 solves the present epoch only.** (1) and (2) are time evolutions; running them means either
another integrator beside C20 or a restriction. **The restriction is chosen: `dT_p/dt` is the unknown,
(1) is solved for it at the present state, and secular cooling comes out as a number rather than as a
history.** Coupling to C20's time axis is a separate brief. **Gate cost of stage 1 is therefore ~0** — it
is algebra on state that already exists.

#### The constants, all printed (Foley 2018 Table 1)

`c₁` = **0.5** · `a_rh` = **2.5** · `E_v` = **300 kJ/mol** (Karato & Wu 1993) · `μ_n` = **4 × 10¹⁰ Pa·s**
(→ `μ_r` ≈ 2 × 10²⁰ at `T_r` = 1623 K) · `ρ` = **4000 kg/m³** · `c_p` = **1250 J/kg/K** · `k` = **5 W/m/K**
· `κ` = **10⁻⁶ m²/s** · `α` = **3 × 10⁻⁵ /K** · `T_s` = **273 K** · `R_p` = 6378.1 km · `R_c` = 3488.1 km
· `d` = 2890 km, with `V_man = (4/3)π((R_p−δ)³ − R_c³)` and `A_man = 4π(R_p−δ)²`.

⚠ **The paper's own caveat travels with (3):** it uses `T_p − T_s` and `d` rather than `T_p − T_l` and
`d − δ`, and states that *"in the heat flux scaling law both the mantle thickness and temperature
difference **cancel out**, so the equation … is independent of the definition"*. **Transcribed as
printed; the caveat is the paper's, not ours.**

#### The first anchor — three transcriptions of one fit, and the source sits between them

**The primary source is Solomatov & Moresi 2000 ([`2000JGR...10521795S`](https://ui.adsabs.harvard.edu/abs/2000JGR...10521795S), held).**
Its eq. (9) is the law both later papers cite — *"All scaling relationships for the Nusselt number in the
stagnant lid convection regime have the form `Nu = a θ^(−α) Ra_i^β`, where a, α and β are constants
depending on n"* — and its **Table 5** prints the fits. For `n = 1`, verbatim:

| fit | `a_rh` | `a` | `β` | `χ²ᵥ` |
|---|---|---|---|---|
| two-parameter | 2.0 | 0.47 ± 0.05 | 0.342 ± 0.008 | 0.3 |
| two-parameter | 3.0 | 0.57 ± 0.06 | 0.329 ± 0.008 | 0.3 |
| **one-parameter** | **2.4** | **0.528 ± 0.002** | **0.333** (theoretical, held fixed) | 0.3 |

⚠ **So the two constants we had been comparing straddle the source, and both miss it by more than an
order of magnitude beyond its own precision:**

| | value | against 0.528 ± 0.002 | Earth `F_man` at `T_p` 1623 K |
|---|---|---|---|
| Foley 2018's printed `c₁` | **0.5** | **−5.30 %** — **14×** the fit's ±0.38 % | **14.233 mW/m²** |
| S&M 2000's own one-parameter fit | **0.528** | — | **15.030** |
| our Korenaga refit `a_of_n(1)` | **0.5539** | **+4.91 %** — **13×** it | **15.768** |

*(Same three at `T_p` 1600 K: 12.317 · 13.007 · 13.645 mW/m². The prefactor is linear in (3), so these
are exact scalings, computed on Foley's own Table 1 parameters: `θ` 18.49, `Ra_i` 2.118 × 10⁸,
`μ_i` 1.810 × 10²⁰ Pa·s at 1623 K.)*

⚠ **This reframes the anchor twice over, and the second reframing came from reading Korenaga rather than
our own note.** *"Two independent transcriptions agree to 10.8 %"* was the wrong way to say it — but so
is *"our 0.5539 is an optimistic comparison against a rounded 0.55"*. **Korenaga 2009 prints its own
refit and says why it differs**, verbatim: *"Solomatov & Moresi (2000) fit eq. (29) … and obtained
**a ≈ 0.31 + 0.22n** by assuming a_rh = 1.2(n + 1). As **my definition of T̄_i (eq. 20) results in
slightly different values of Nu, Ra_i and a_rh**, I repeated their regression analysis and obtained that
**a ≈ 0.30 + 0.25n**. The rms error of the fit is ∼1.2 per cent."* **So one quantity has five values:**

| `a` at `n = 1` | source | note |
|---|---|---|
| **0.528 ± 0.002** | S&M 2000 Table 5, one-parameter fit | the primary fit; `β` fixed at 1/3, `a_rh` 2.4 |
| **0.53** | S&M as Korenaga summarises it, `0.31 + 0.22n` | assumes `a_rh` = 1.2(n+1) |
| **0.55** | **Korenaga's own re-regression**, `0.30 + 0.25n` | rms of the fit **∼1.2 %** |
| **0.57** | Korenaga Fig. 6, per-`n` subgroup fit | a third number in the same paper |
| **0.5** | Foley 2018's printed `c₁` | cites Reese, S&M and Korenaga together |

⚠ **Which makes our own claim better, not worse.** C47 (f)'s *"0.5539 reproduces a = 0.55 to 0.7 %"*
names **Korenaga's** refit, and 0.7 % is **inside that fit's own ∼1.2 % rms**. What it must not be read
as is agreement with the primary fit: against 0.528 ± 0.002 we are **+4.91 %**, thirteen times its stated
precision, and Foley is **−5.30 %**, fourteen times.

⚠ **And the cause of the spread is printed, which is the useful part.** It is not sloppiness — it is
**the definition of the internal temperature `T̄_i`**, named by Korenaga in one sentence. That is also the
**only candidate explanation on the table for the 3.65× absolute-flux gap** below, and it is why the rule
*"never mix one paper's constants with another's"* is a physics rule here and not tidiness.

⚠ **Corrected 2026-09-09, later the same day (Brief 167 B's first verification, from the three papers'
own definitions).** The table above is **not five readings of one quantity** — the quantity itself is
defined differently in each, and that changes which comparisons mean anything. Verbatim:

| paper | what its `T_i` is | in its own words |
|---|---|---|
| S&M 2000 | the **maximum horizontally averaged temperature** in the layer | *"The interior temperature T_i is often defined as the average bottom temperature … Perhaps, a more meaningful (but not much different) definition of T_i is the maximum horizontally averaged temperature in the layer (Figure 2)."* |
| Korenaga 2009 | the **average below the boundary layer**, solved self-consistently (his eq. 20, `δ = Nu⁻¹`) | *"how to define T̄_i is not very unique. **It is not described by Solomatov & Moresi (2000).** … Here, I choose to rely solely on temperature and define T̄_i in a self-consistent manner"* |
| Foley 2018 | `T_p`, a **potential temperature** — a thermal-evolution state variable, not a field diagnostic | *"T_p is the potential temperature of the upper mantle"*; `θ` and `Ra_i` are built on `T_p − T_s` with viscosity at `T_p` |

**So the comparisons split into three kinds, and only one of them could ever indicate a defect in our code:**

- **Within one definition — our 0.5539 against Korenaga's 0.55: +0.71 %**, inside his fit's own ∼1.2 %
  rms. ✓ **This is the consistency check, and it passes.**
- ⚠ **Across a definition boundary — our 0.5539 against S&M's 0.528: +4.91 %** (13× that fit's ±0.38 %),
  and **Foley's 0.5 against S&M's 0.528: −5.30 %** (14×). **Both of those "13–14×" figures are
  comparisons that crossed a definition boundary, and neither is evidence of an implementation error.**
  They measure how much the definition of `T_i` is worth, not how well anyone transcribed.
- **Neither, in Foley's case.** Foley does not claim `c₁` is either paper's fitted `a`: it attributes
  eq. (3) to *"Reese et al. 1998, 1999; Solomatov & Moresi 2000; Korenaga 2009"* together and then says
  *"We use c₁ = 0.5"*. **It is an adopted round constant under a third temperature definition** — so its
  −5.30 % from S&M and −9.09 % from Korenaga are not a disagreement between fits at all.

⚠ **This is the second time today that a number's *label* mattered more than its value**, and it is the
same lesson as C25 (e)'s upper-bound-called-a-lower-bound. **The one comparison that would have caught a
real defect is the within-definition one, and it is the one that agrees.**

⚠ **And the absolute flux still meets nowhere: 3.65×.** Korenaga's normalization puts Earth at **51.99
mW/m²** (eq. 29; 50.00 by construction on eq. 30) where Foley's printed parameters give **14.23**. The
difference is the viscosity normalization — a fitted `b` against a printed `μ_n` = 4 × 10¹⁰ Pa·s — not
the prefactor. **So C47 (e)'s finding survives contact with a second paper**: *"the absolute scale has no
anchor"*, now measured across two papers instead of argued from one.

⚠ **Two parameter disagreements to carry, not average.** Foley's Table 1 prints `k` = **5 W/m/K** and
`α` = **3 × 10⁻⁵ /K**; our `stagnant_lid.py` holds Korenaga's `k` = **4** and an `α` of **2 × 10⁻³** in
the Rayleigh normalization. **The transcription keeps each paper's own set and never mixes them** — this
is the trap commit `c23e69b0` exists to prevent, and this seat fell into it once already on this very
comparison (a first pass mixed `α` and produced 1.06× instead of 3.65×).

#### The three verdict cells, written before the numbers

| # | cell | pass |
|---|---|---|
| ① | **Mars, stagnant lid** — the budget's `F_man` for Mars | inside **[14, 25] mW/m²** — Parro+ 2017 ([`2017NatSR...745629P`](https://ui.adsabs.harvard.edu/abs/2017NatSR...745629P), held), verbatim: *"Our preferred model finds heat flows varying between **14 and 25 mW m⁻²**, with an average value of **19 mW m⁻²**"* ⚠ *model against model, no in-situ measurement exists* |
| ② | **Earth, stagnant lid — a counterfactual, and read as one** | ⚠ **not** the 46 ± 3 TW anchor, which belongs to the mobile-lid branch. Pass = the budget puts a stagnant-lid Earth **far below** its observed loss and in the direction the literature gives (Korenaga 2009's ~50 mW/m² by construction; Reese+ 1998 ([`1998JGR...10313643R`](https://ui.adsabs.harvard.edu/abs/1998JGR...10313643R), **now held**), verbatim: *"in the absence of plate tectonics, the mantle temperature on Earth, which is already close to the solidus, would be about **700–1500 K higher** for the present-day value of the surface heat flux"*) |
| ③ | **Urey direction** | `Ur`(Earth) **<** `Ur`(Mars) — the direction four law families have failed on (C47 (k)) |

**If a cell fails, the sentence is fixed now.** ① outside [14, 25] → *the budget does not reproduce the
only rocky body with a published stagnant-lid flux, and the transcription is suspect before the physics
is*. ② in the mobile-lid range → *the budget is not describing a stagnant lid at all*. ③ wrong direction →
**a fifth law family failing in the same direction**, and C47's closing sentence covers it without
revision.

#### The transitional law, and what it prints (commit C's target)

**Foley & Bercovici 2014 ([`2014GeoJI.199..580F`](https://ui.adsabs.harvard.edu/abs/2014GeoJI.199..580F), held)** reaches its
transitional-regime law through the grain-damage shear-stress chain — its eq. (9) `τ'_xz = 2C₁ Ra'^(2/3)
A'_i^(−m/3)`, eq. (10) the steady-state grainsize balance `D τ'²_xz A'_i = H A'_i^p`, eq. (11) `A'_i =
(D τ'²_xz / H)^(1/(p−m))`, and eq. (12) the combination `τ'_xz = (2C₁)^(3(p−m)/(3p−m)) (D/H)^(−m/(3p−m))
Ra'^(2(p−m)/(3p−m))` — and closes with the top-boundary-layer scaling, its **eq. (54)**:

> `δ'_l = C₅ L'^βL μ'_l^βμ (D/(H h'_l))^βD (Ra' T'_i)^βRa`

**Its Table 1 prints the constants for three `(m, p)`, verbatim:**

| `m` | `p` | `C₅` | `β_Ra` | `β_D` | `β_μ` | `β_L` |
|---|---|---|---|---|---|---|
| 2 | 4 | 20 | −0.6603 | −0.3151 | 0.2484 | **0.1071** |
| 3 | 4 | 86 | −0.8515 | −0.4919 | 0.2598 | **−0.0218** |
| 3 | 5 | 11 | −0.6232 | −0.4342 | 0.1931 | **0.0582** |

⚠ **`β_L` changes sign across the three rows**, so *"how does plate length enter"* has no single answer in
the paper — which matters because the paper also declines to derive `L′`: *"we choose to exploit our
numerical results and calculate `L′` directly from the models. We therefore **treat the plate length,
`L′`, as an unknown** in (54)."* **`C₅` also spans 11 to 86 across the same three rows.**

#### What is not chosen here

⚠ **The two unknowns are carried as bands, not values.** `L′` is an unknown in the source's own words,
and `(m, p)` has three printed combinations whose constants disagree in **sign** as well as magnitude.
**Both go in as bands; the owner is asked only after the numbers exist (commit D).** And **C34's feed is not changed by this brief** — decision ③ stays
held, exactly as C25 (f) recorded.

#### Record columns, and the Reese ceiling's label

⚠ **The stagnant-lid "ceiling" our own ladder uses is a melting limit read off a figure, and the label
travels with it from now on.** Reese, Solomatov & Moresi 1998 (held) prints *"For Venus, the critical
heat flux which can be removed without widespread melting is only **10–20 mW/m²**. For Mars, it is
**15–30 mW/m²**"* — obtained by running stagnant-lid scalings to a surface-flux/interior-temperature
curve and reading where it **meets the peridotite solidus at the lid base**, their Fig. 4b/c, with a
**wet-olivine `n = 3`** rheology (`E*` 430 kJ/mol, `V*` 15). **Label: melting limit · figure
intersection · n = 3 wet rheology · model output, two bodies, two numbers.** It is not a heat-flow
measurement of either planet and must never be cited as one (C34, C46 (c)).

**Mars comparison columns, recorded and not targets** (parallel seat P8, from held papers):

| source | what it prints |
|---|---|
| Morschhauser+ 2011 ([`2011Icar..212..541M`](https://ui.adsabs.harvard.edu/abs/2011Icar..212..541M)) | reference model surface heat flow *"about 20 mW m⁻² today"*, mantle heat flow 75 → 10, mantle cooling ∼260 K, permissible models from initial 1650 K with 30 km primordial crust; ⚠ **Urey ratio not printed** |
| Breuer & Spohn 2003 ([`2003JGRE..108.5072B`](https://ui.adsabs.harvard.edu/abs/2003JGRE..108.5072B)) | present mantle **1800–2100 K**, lid **350–500 km**; ⚠ **no heat-flow number printed** |
| Parro+ 2017 | the verdict cell above; crustal component 1.3–13.5, average 7.0 mW m⁻² |

⚠ **Only Parro prints a range this budget can be scored against**, which is why cell ① names it alone
and the other two are columns. **Two of the three print no Urey ratio at all**, so cell ③ is a
**direction** test and not a value test — as registered.

#### What would make this pre-registration wrong

⚠ Three ways, written now so they cannot be discovered conveniently later.
1. **If (1) at the present epoch turns out to need a melt production nobody would defend**, stage 1's
   restriction is the wrong restriction and the honest move is to say so, not to tune `f_m`.
2. **If the leading-constant spread (0.5 · 0.528 · 0.5539) turns out to matter to a verdict cell**, then
   the cell was never a test of the budget — it was a test of which paper we copied, and it is withdrawn
   rather than reported.
3. **If cell ② cannot be stated without an Earth stagnant-lid number nobody printed**, the cell is
   recorded as unmeasurable rather than scored against the mobile-lid 46 ± 3 TW, which would be the exact
   error C47 (b) named.

---

#### C51 (b) 2026-09-09 — the budget is transcribed, and the printed law reads less than it appears to

**Built: `engine/mantle_budget.py` and `engine/test_mantle_budget.py`, wired into the gate at ~0 s** —
Foley 2018's eqs (1), (2), (3) and (4) with that paper's own Table 1 constants, and nothing else. eq. (3)
is **called, not retyped**: `stagnant_lid.nu_asymptotic(θ, Ra_i, n=1, a=c₁)` reproduces it bit for bit,
which is the claim *"the flux law is not what is missing"* turned into code.

**Two printed derived values reproduced, under C51's own printed-value rule:**

| the paper prints | we compute | note |
|---|---|---|
| *"μ_r ≈ 2 × 10²⁰"* at `T_r` = 1623 K | **1.810 × 10²⁰ Pa·s** | agrees at the printed significant figure (−9.5 %); **the value we carry is the printed 2 × 10²⁰** |
| *"P e ≈ 0.6"* from Λ ∼100 km, u ≈ 6 × 10⁻¹² m/s, κ = 10⁻⁶ | **0.600** | exact |

⚠ **And the paper's cancel-out remark is an identity, not an approximation.** ⚠ *The invariance is
**Foley's own printed statement**, not something this seat derived — what we added is the confirmation
and the exponent arithmetic behind it.* Foley notes that (3) uses `T_p − T_s` and `d` rather than
`T_p − T_l` and `d − δ` because
*"in the heat flux scaling law both the mantle thickness and temperature difference cancel out"*. Measured:
the two forms agree to a relative **10⁻¹²**, and so does **any** substitution — `T_s` at 100, 273, 500 and
737 K, and `d` at 1700, 2890 and 4000 km, all give `F_man` = **14.233339 mW/m²** to a relative
**2.4 × 10⁻¹⁶**. The exponents make it exact: `1 − 4/3 + 1/3 = 0` and `−1 + 3/3 = 0`.

⚠ **So this law's `F_man` reads exactly two things: `T_p` and `g`** (through `θ ∝ 1/T_p²`, `μ_i(T_p)`, and
`Ra_i^(1/3) ∝ g^(1/3)`). **Venus's 737 K surface does not change it. Mars's thinner mantle does not change
it.** ⚠ *That is a fact about the law we are adopting, and it bears directly on C34 and C46*: a ladder
built on this law cannot discriminate two bodies by surface temperature or mantle depth at all, only by
interior temperature and gravity. **Recorded, no verdict** — C51's cells are read in commit D.

**What the budget produces, and one number that is a finding rather than a pass.** At `T_p` = 1623 K,
`δ` = 100 km, and our own radiogenic mantle budget `Q_man` = **14.9 TW**, the stagnant-lid surface loss is
`A_man F_man` = **7.0 TW**, so eq. (1) solved for the unknown gives `dT_p/dt` = **+57.9 K/Gyr** with a
Urey ratio of **2.117**. ⚠ **The sign is positive: under this law a stagnant-lid Earth cannot cool, it
heats.** *That is Reese+ 1998's "700–1500 K higher" written as a budget*, and it is the **counterfactual**
cell ② registered — not a number to set against Earth's observed ~46 TW.

⚠ **The pre-registration's own assertion was wrong here, and it is recorded rather than adjusted.** This
seat first wrote the gate row as *"`dT_p/dt` < 0"*, presuming cooling. **It failed, and the honest repair
was to the row and not to the physics**: the gate now checks that eq. (1) **closes term by term**
(residual < 10⁻¹² of `Q_man`), and the sign is printed as a record pointed at cell ②. *A stage-1
transcription cannot own a verdict that stage D registered.*

**The melt gap is printed, not assumed.** Moving `dT_p/dt` by 10 % takes a melt heat loss of **0.79 TW**,
**11.2 %** of the surface loss. It is reported as a **power** and never converted to `f_m`, because `ΔT_m`
has no value in this engine and converting would invent a temperature.

**eq. (2) refuses by name.** The lid-base conductive gradient is eq. (5)'s output and eq. (5) is not built
(it needs `Q_crust`, `δ_c` and the crust/mantle production split), so `ddelta_dt_m_s` returns a named
refusal rather than a default. Given the steady-state gradient `−F_man/k` it returns `dδ/dt` = 0, which is
the check that the equation was transcribed the right way round.

#### C51 (c) 2026-09-09 — the transitional law transcribed, and the source denies the field our bodies declare

**Built: `engine/transitional_lid.py` and `engine/test_transitional_lid.py`, in the gate at ~0 s** —
Foley & Bercovici 2014 ([`2014GeoJI.199..580F`](https://ui.adsabs.harvard.edu/abs/2014GeoJI.199..580F), held): eqs (9)–(12)'s
grain-damage shear-stress chain, eq. (54)'s top boundary layer, eq. (58)'s bottom one, eq. (59)'s energy
balance closing `T'_i`, and eq. (60)'s Nusselt number. **Table 1's three `(m, p)` rows are stored to the
printed digit** and Fig. 13's four panel fits are recorded beside them.

⚠ **No body is evaluated and no verdict cell is read.** All seven inputs are non-dimensional quantities
of that paper's own models — `L′`, `μ'_l`, `μ'_i`, `D/(H h'_l)`, `D/(H h'_i)`, `Ra'`, `(m, p)` — and
**this engine declares none of them**, so `solve_on_body()` refuses by name and lists all seven.

**Three measurements the paper leaves as prose:**

| what | measured |
|---|---|
| **the paper's own rounding of its own exponents** — eq. (60) uses (1/10, 1/4, 1/3, 2/3) where Table 1's (2, 4) fit prints (0.1071, 0.2484, −0.3151, −0.6603) | over the 64 physical points inside Fig. 13's plotted ranges the `Nu` ratio spans **0.917–1.319**, i.e. up to **31.9 %** |
| **how far apart the three `(m, p)` rows put one answer** | at `Ra'` 10⁷, `μ'_l` 10⁵, `D/(H h'_l)` 10⁻²: `Nu` **23.69 · 50.46 · 27.05** — a **2.1× span**, which is why owner decision (b) carries a band and not a value |
| **`β_L` changes sign and `C₅` spans 7.8×** | (+0.1071 · −0.0218 · +0.0582) and 20 · 86 · 11 — *"how does plate length enter"* has no single answer in the source, which is consistent with the source treating `L′` as an unknown |

⚠ **And the paper's headline contradicts a field our bodies declare.** F&B 2014's own words: *"with
grain-damage, the transition between stagnant lid convection and fully mobile convection is gradual and
takes place over a large transitional regime, **with plate-tectonics lying within the transitional
regime**"*, and Venus *"can be explained by convection in the transitional regime, close to the
fully-stagnant lid regime, with a very slow «plate» speed"*. **Every body in `engine/bodies/` declared
`stagnant_lid: true` or `false`** and `dynamo_rocky`'s survival gate read it. ⚠ *That is what C53 (b)
replaced on 2026-09-09* (`engine/bodies/earth.yaml@«판구조 영역 — **선언**. 옛 `stagnant_lid: false` 를 대신하고»`);
the sentence is kept in its original tense below because it is the finding that opened the item. **This is a two-valued field the source says does not
describe either Earth or Venus** — and it is the same shape as C46's finding that the ladder always
lands on one cell.

⚠ **And the paper's abstract names our field as the thing it is arguing against**, verbatim:

> *"Contrary to many previous studies, the transitional regime between the stagnant lid and fully
> mobilized regimes is large, and the transition from stagnant lid to mobile convection is gradual and
> continuous. Thus planets could exhibit a full range of surface mobility, **as opposed to the bimodal
> distribution of fully mobile lid planets and stagnant lid planets that is typically assumed.**"*

**`stagnant_lid: true/false` is that bimodal distribution.** So this is not a case of our field being
coarser than the source — **it is the source's stated foil.** ⚠ *Named, not repaired: changing it moves
outputs, and it is the same shape as C46 (the ladder always lands on one cell). The transitional law
cannot replace the field either, because it needs seven inputs no body declares (C51 (d)).*

⚠ **A fourth printed value for Earth's mantle potential temperature.** F&B §8.1 eq. (68) prints
*"`T_m,0` = **1650 K** is the Earth's mantle potential temperature"*, beside Foley 2018's `T_r` = 1623 K,
Korenaga's 1350 °C = 1623.15 K, and our bodies' declared **1600 K** (Unterborn+ 2019). **Four papers,
four numbers, one quantity** — and unlike the prefactor spread this one is not a definition difference,
it is four choices of the same declaration. **Recorded where the next seat will read it.**

#### C51 (d) 2026-09-09 — the three cells read: one fails, one passes, one was under-specified

**Built: `engine/tools/c51_regimes.py`, in the gate at ~0 s.** Each regime is scored against **its own**
anchor and nothing else — the stagnant-lid budget against a stagnant-lid anchor, the mobile-lid law
against a measured surface flow, the transitional law against nothing because its inputs do not exist
here. ⚠ **The gate checks reproduction, not the verdicts** (six rows, ±0.06), the way `c47_step4.py`
does: a verdict left red in the gate becomes the background the next seat reads new regressions against.

| regime | law | Earth | Mars | its anchor |
|---|---|---|---|---|
| stagnant lid | Foley 2018 eqs (1)(3) | **counterfactual** | evaluated | Reese ceiling (Earth +700–1500 K; Mars 15–30) · Parro [14, 25] |
| mobile lid | Nimmo+ 2004 eqs 34–36, already in the engine | evaluated | evaluated | measured global flow (Earth 86 ± 6, Jaupart+ 2007) |
| transitional | F&B 2014 eqs (54)(58)(59)(60) | ⚠ **refused** | ⚠ **refused** | seven non-dimensional inputs, none declared |

**Cell ① — Mars's stagnant-lid `F_man` inside Parro's [14, 25] mW/m²: FAILS, on every combination.**
1.784 mW/m² at C20's `T_p` 1377.9563 K and 8.923 at the declared 1600 K ⚠ *(the pair read 1.770 at 1377.03 K until 2026-09-19, which was the pre-180 C generation)*, at both lid thicknesses (350 and
500 km — Breuer & Spohn 2003's printed band; `δ` changes the area, not the flux). **The registered
failure sentence stands as written:** *"the budget does not reproduce the only rocky body with a
published stagnant-lid flux, and the transcription is suspect before the physics is."* ⚠ Mars would need
`T_p` ≈ **1673.6 K** — 74 K above the declaration — to reach the band's lower edge.

**Cell ② — Earth's stagnant lid as a counterfactual: PASSES.** `F_man` 12.325 mW/m², loss **6.09 TW**,
`dT_p/dt` **+65.1 K/Gyr**, Urey **2.450**; the mobile-lid law at the same `T_p` gives **39.22 TW**, a
factor **6.4** more. The direction is Reese's *"700–1500 K higher"*, and the 46 ± 3 TW anchor was **not**
used, as registered.

**Cell ③ — the Urey direction: ⚠ UNDER-SPECIFIED, and the registration is what failed.**

| pairing | Urey (Earth) | Urey (Mars) | direction |
|---|---|---|---|
| **each body at its own C20 temperature** — ✅ **the owner's row** | 4.251 | **8.713** | ✓ **as registered** *(8.780 until 2026-09-19, at the older `T_p` 1377.03 K)* |
| both at the declared 1600 K | 2.450 | 1.742 | ✗ **reversed** |

⚠ **The pre-registration named a direction and never fixed which temperature row it is read on**, and
the two answers disagree. **Electing the row that passes would be a choice made after seeing the
output**, so it was not made by a seat: the defect was filed at `85b1d7d2` with both pairings printed.

⚠ **Closed 2026-09-09 by an owner decision taken outside the registration: the cell is read at each
body's own C20 temperature, so cell ③ passes.** The owner's reason: *a Urey ratio is a quantity built to
measure the difference between two bodies, so the two bodies cannot be put at one `T_p`.* **The three
cells therefore read ① ✗ · ② ✓ · ③ ✓** — and ③ carries its own label: *the registration could not decide
it, the disagreement was committed first, and the owner decided it afterwards.* **That order is the
whole difference between this and a post-hoc choice**, and git carries it: the both-pairings commit
precedes the decision.
*The physical content of the ambiguity is worth stating: Mars's declared 1600 K is a value C47 (i)'s
stage 0 **transferred from Earth**, so putting both bodies at the same `T_p` erases exactly the
difference a Urey ratio is built to measure.*

#### ⚠ A reported intermediate was built on another body's arguments — fixed 2026-09-09 (Brief 167 E)

**The audit seat could not reproduce Mars's `Ra_i` and was right not to.** `mantle_budget.dtp_dt_k_s`
returned its diagnostics as `theta_fk(t_p_k)` and `ra_internal(t_p_k)` — **without `flux_kw`** — so the
answer used Mars's `g` while the number printed beside it was built on **Earth's `g` and Foley's printed
`d` = 2890 km**: `3.26409501 × 10⁶` where the answer's arguments give `2.62935029 × 10⁵`, a factor
**12.4141** = (9.8/3.7262) × (2890/1722.838)³. ⚠ **Earth's row had the same disease** at 0.2 % — the
answer took the computed `g` = 9.8195 and the diagnostic took Foley's printed 9.8.

**Two repairs, and the second is the one worth naming.** The diagnostics now recompute with the same
arguments the answer used; and `c51_regimes` now passes **each body's own mantle thickness** instead of
leaving it at Foley's Earth value. ⚠ *The second was free precisely because of what C51 (b) measured:*
(3)'s flux is **exactly invariant to `d`**, so passing the right thickness cannot move an answer — and
every number in this section is **bit-identical** after both repairs (`F_man` 7.1041467231 and
1.7840798826 mW/m², Urey 4.25068708 and 8.71318123, all six regression rows unchanged ⚠ *(1.7704573721 and 8.78022345 until 2026-09-19)*).

⚠ **No answer was ever wrong, and that is the whole point.** `F_man` received the right `g` and does
not read `d`, so the physics was right while the printed path to it was not. **An intermediate value is
the path to the answer**, and a path built on another body's arguments cannot be checked by anyone —
which is exactly how the audit seat found it: by trying to walk the path.

#### ⚠ What this evaluation says that is larger than the three cells

**The ratio is right and the absolute scale is wrong by an order of magnitude, and both halves are
measurements rather than impressions.**

- At equal `T_p` this law's Mars/Earth flux ratio is fixed at **0.724 by gravity alone** — `F_man ∝
  g^(1/3)` and it reads nothing else (C51 (b)). **The measured ratio is 19/86 = 0.221.** So gravity
  alone cannot produce the contrast between the two bodies.
- At each body's **own** C20 temperature the ratio is **0.249**, within **13 %** of the measured 0.221.
  **Essentially all of the observed contrast is the temperature difference**, and the law reproduces it.
- ⚠ **And the absolute values miss in the same direction on both bodies** — Earth 86/7.10 = **12.1×**,
  Mars 19/1.77 = **10.7×**.

⚠ **So C47 (e)'s argument is now a measurement on two bodies with a budget:** *"the absolute scale has no
anchor."* And the anchor situation is worse than it looks — **Earth's stagnant-lid number is a
counterfactual and cannot anchor anything**, so the only printed anchor available to fix the scale is
**Mars's Parro band**, the very cell that fails by a factor of 8–11. **A one-parameter rescale would fit
it and would be fitting to the single anchor that exists**, which is what `AUTHORED-VALUES-POLICY.md`
forbids without a printed ground. **Not done here.**

#### Owner decisions this brief hands up, with numbers instead of options

| # | decision | what the numbers say |
|---|---|---|
| (a) | **`L′`, the plate length** | the source *"treat[s] the plate length, `L′`, as an unknown"* and reads it off its own models; changing the domain aspect ratio 4 × 1 → 16 × 1 moves it **≈1.5 → ≈4**. Carried as that band; ⚠ **no NearStars body can supply it**, so electing a value is electing a number nobody measured |
| (b) | **`(m, p)`, the grain-damage pair** | three printed rows put one input point at `Nu` **23.69 · 50.46 · 27.05** (**2.1×**), `C₅` spans **7.8×**, and `β_L` **changes sign**. Carried as a band |
| (c) | ⚠ **new — which temperature row cell ③ means** | **decided 2026-09-09: each body's own C20 temperature.** The direction flips between the two pairings, so this was the registration's defect rather than a physics choice — the one decision this brief created rather than inherited, and the only one already closed |

⚠ **One sensitivity to carry beside (a) and (b): `δ` moves the Urey ratio and nothing anchors `δ`.**
Mars's Urey goes **8.713 → 9.641** across Breuer & Spohn 2003's printed lid band 350 → 500 km, **+10.7 %**,
purely through `A_man = 4π(R_p − δ)²` — the flux itself does not read `δ` at all. **So a cell scored on
Urey inherits the lid-thickness band**, and no printed value picks a point inside it.

⚠ **Decision ③ (C34's feed) is still held**, exactly as C25 (f) recorded, and nothing in this brief
changed the transport table's input.

#### C51 (e) 2026-09-19 — three dials swept one at a time, and none reaches Khan+ 2022

*Why here: the three dials are inputs to the stagnant-lid budget itself, so they belong beside the item that built it. Source blob **`d7b608cb`**, registered in **`06dc3ed7`**.*

**Three dials, one at a time, and none of them reaches the checkpoint.** The budget's present-epoch answer
on Mars is **`T_p` 1739.1481 K** at `c1` 0.5 · δ 350 km · start 1750 K, which is **+104.15 K** from the
centre of Khan+ 2022's 1635 ± 31 K and **+73.15 K** from its near edge. Each dial was swept alone, on one
geometry (`r_p` 3 389 372.0 m · `r_c` 1 666 533.8 m · `d_m` 1 722 838.2 m · `g` 3.72625):

| dial | range | `T_p` today, low → high | span | slope |
|---|---|---|---|---|
| flux prefactor `c1` | 0.5 → 0.57 | 1739.1481 → **1714.7586 K** | **24.39 K** | **−3.48 K per 0.01 of `c1`** |
| lid δ | 300 → 500 km | 1735.4697 → **1750.9119 K** | **15.44 K** | **+0.77 K per 10 km** |
| hot start | 1650 → 1900 K | 1738.6795 → **1739.5787 K** | **0.90 K** | **+0.36 K per 100 K** |

⚠ **The lid runs the wrong way for closing the gap** — a thinner lid *lowers* today's `T_p`, and 300 km,
the thin end InSight supports, still sits **+100.47 K** above the centre. **The hot start reproduces
Stage 3's erasure exactly**: 250 K of spread arrives as 0.90 K, a factor of **278**, which the run
predicted before measuring. The nearest approach of any dial is `c1` at 0.57 — **1714.76 K, still
79.76 K above the centre and 48.76 K above the near edge** — and extrapolating `c1` alone the gap would
close at about **0.799**, far outside every printed value in either definition system. ⚠ *That number is
printed to show the distance, not to propose a value.* The five `c1` values are fits of differently
defined quantities, so the column is a spread across definition systems rather than an error bar.

⚠ **Two dials together were not tried, by registration**, and the three spans do not add to 104 K even if
they combined. **Reaching is not being right**: matching one checkpoint by moving one constant would be
evidence about arithmetic, not about Mars.

**Code this row points at**: `engine/mantle_budget.py@«def integrate_tp(»` — the function every row above
was run through — and `engine/mantle_budget.py@«def dtp_dt_k_s(»`, which holds the `c1` and δ terms.

---

#### C51 (f) 2026-09-19 — the mantle's share of the budget, swept 50–90 %

*Why here: the model that was measured is the lid budget, so the row sits with the item that owns it. Source blob **`79c44de4`**, registered in **`f506b3a4`**. **C20 gets one prose line of cross-reference instead of the row**, because the two models share this budget and split only on the law:*

> The mantle's share of the radiogenic budget was swept 50–90 % under C51 and moves today's `T_p` by **+2.132 K per percentage point, 85.28 K across the range** — the largest of the four dials measured, and still short of Khan+ 2022 by **+57.01 K** at its nearest row. The integrator here draws the same budget from the same line of code; the **14.4×** between the two models is in the loss law, not in the budget.

⚠ **That quoted line is the whole of C20's share of this section** — *it adds no anchor, so the expected anchor count is unchanged.*

**The mantle's share was swept 50 → 90 %, and it does not close the gap either.** `radiogenic.MANTLE_SHARE`
itself was never edited — the caller scales `q_man` — so `core_history` did not move with this sweep:

| share | today's `q_man` | `T_p` today | to Khan's centre | to the near edge | label |
|---|---|---|---|---|---|
| **50 %** | 1.2890e12 W | **1692.0129 K** | +57.01 K | **+26.01 K** | printed — Taylor+ 2006, via Morschhauser+ 2011 |
| 60 % | 1.5468e12 W | 1717.0028 K | +82.00 K | +51.00 K | inside the printed range |
| **70 %** | 1.8045e12 W | 1739.1481 K | +104.15 K | +73.15 K | **the declaration — Earth's appendix figure, no Mars source** |
| 80 % | 2.0623e12 W | 1759.0941 K | +124.09 K | +93.09 K | inside the printed range |
| 90 % | 2.3201e12 W | 1777.2927 K | +142.29 K | +111.29 K | range end, not a candidate |

**Slope +2.132 K per percentage point · span 85.28 K across 50–90 %.** The predictions were registered
first and held: ≈1.9 K per point measured **2.132** (+12 %), ≈77 K across the range measured **85.28 K**
(+11 %), and the direction held. ⚠ **The size prediction came from the other model** — `core_history`'s
1.347 K per percent of `q_man` — *so the two models' responses to the same fractional change in mantle
power agree in size, which nothing required.* **They share the budget exactly and split on the law**: the
same two models differ by **14.4×** in `Q_surf` at the same temperature.

**1635 K is not reachable inside 50–90 %**; the nearest row, 50 %, is **+57.01 K** from the centre, and
extrapolating the slope the gap would close at about **23 %**, less than half the lowest figure the
literature prints. ⚠ **One paper carries two figures** — Morschhauser+ 2011 reports Taylor's «about half»
and then adopts Λ = 5, i.e. 12 % of the heat-producing elements in the crust — **and the engine's 0.70
sits between them and cites neither**. ⚠ **The checkpoint is not independent of the dial**: Khan+ 2022's
areotherm assumes no crustal enrichment in heat-producing elements, which is precisely the quantity swept
here, so the comparison is worth printing and **is not a test**.

**Code this row points at**: `engine/radiogenic.py@«# — the appendix. Earth's number, DECLARED for every rocky body.»`
— the declaration's own provenance comment — and `engine/radiogenic.py@«def budget(silicate_mass_kg: float, set_name: str = DEFAULT_SET, t_gyr: float = 0.0,»`,
the one line both models draw the budget from.

---

#### C51 (g) 2026-09-19 — the 3.7 Ga checkpoint is read by interpolation now, and two recorded anchors moved

**The checkpoint was reading the nearest sampled row, not 3.7 Ga.** `core_history.integrate` prints rows on
its own adaptive step, so the reader's `min(rows, key=…)` returned whichever row happened to land closest and
never compared that row's own time against the time it was asked for. `core_history.t_at_gyr(rows, t_gyr,
key="t_m")` now brackets the requested time and interpolates linearly between the two neighbouring rows, and
refuses outside the span instead of extrapolating. `engine/tools/mars_step_sweep.py` reads it the same way, so
`t_37_actual` is now the time that was requested rather than the time that was sampled.

**Two recorded anchors moved by about one sampling step**: `1668.79 → 1668.68 K` and `1669.99 → 1669.88 K`,
both **−0.11 K**. ⚠ *Neither number was wrong as printed* — each was a real row's temperature — and both were
wrong as read, because this file and the tests called them the 3.7 Ga values. The old rule's comment is kept
at `engine/test_core_history.py@«2026-09-19: 3.7 Ga 칸의 규칙이 바뀌어 그 수가 다시 움직였다»` with a generation label, so the movement stays legible.

⚠ **The helper raises `ValueError`, and that is a departure from the convention the same night defended.**
`mantle_budget.LidOutsideMantle` exists precisely so a domain refusal is not swallowed by code catching
`ValueError` (pre-registration B, trap 4), and `t_at_gyr` then uses `ValueError` for out-of-order rows. The
distinction claimed is that unsorted rows are a **caller's bug**, not a physical domain refusal, so a physics
name would be the wrong label; the docstring carries that reasoning. **The tension is registered, not
resolved** — if a second caller-bug condition appears, the two decisions should be decided together rather
than one at a time.

⚠ **The pre-registration for this item missed a coupling, and the bundle gate found it.** Item 2 registered
the anchor movements and the tests that would move; it never listed `engine/ice_giant_anchor.json`, whose
input trigger watches `core_history.py` **by code digest**. The gate went red at `gate-17a6274d.log:1453`:

> `· 굳힌 뒤로 풀이가 읽는 파일이 움직였다 — 코드가 바뀐 파일 core_history.py 코드 0f4cbd0e7c9021ce → aab09c48a45af765 (바이트 a375ad175350e25a → f676f6d957cd2b64). **이 커밋에서 `--refresh`** 로 다시 굳혀 diff 에 남겨라`

**A pre-registration that lists the tests but not the frozen snapshots is incomplete.** The rule this adds:
*a change to a module named in an anchor's input trigger is a change to that anchor*, and belongs in the same
commit.

#### C51 (h) 2026-09-19 — the lid guard refuses by name, and nothing reads the refusal

**A lid must be inside its own mantle**: `0 ≤ δ < d_m`, half-open, because at `δ = d_m` the stagnant-lid
expression divides by a zero mantle thickness and died with `ZeroDivisionError` — a refusal with no name.
`engine/mantle_budget.py@«def _lid_domain_message(delta_m: float, body_d_m: float) -> str:»` states the domain and returns the refusal text
*«뚜껑 두께 δ … 가 이 천체의 맨틀 … 밖이다 (0 ≤ δ < d_m)»*; the two remaining entrances that still died
unnamed were closed by the parallel seat in `91f5440b` with the `LidOutsideMantle` type.
`engine/tools/c51_regimes.py` catches **that type only** — `except Exception` would swallow the next
unnamed death — and prints one `[STOP]` line, which is the `[STOP]` the gate counts.

⚠ **The refusal dict has no reader, and this is an open defect rather than a finished repair.** `stagnant()`
returns `{"refused": str(why)}` on the stop path while its consumers index the success shape:
`stag[("Earth", "C20", 100.0e3)]["urey"]` and two neighbouring reads would raise `KeyError` if that entry
were ever a refusal. **No roster row takes the branch tonight, so the gate is green and the hole is
invisible** — which is the condition under which this kind of defect normally survives. Registered as its own
item: either the call site filters refusals before indexing, or the refusal carries the keys its readers use.

**No number moved when the lid thickness became an argument.** `f_man_lid_variables` records `d_m_used_m` and
`d_m_from_caller`, and the ratio of the two answers is exactly **1.0** — `d` cancels in Foley 2018 eq. (3), so
the value was never at risk. The two variables exist so that the cancellation is **printed** rather than
assumed by whoever reads this next.

#### C88 (e) 2026-09-19 — the anchor was re-frozen, and the trigger printed which of its three rulers moved

**Six lines changed in `engine/ice_giant_anchor.json` and no value key moved**: `frozen_at` 2026-09-17 →
2026-09-19, `core_history.py` in **both** digest tables, `interior.py` in the byte table **only**, and two
`seconds`. ⚠ **That `interior.py` moved on one ruler and not the other is the two-ruler split doing its
job** — it means that file has changed only in prose since 2026-09-17. The question *«why did a file I did
not touch move?»* has its answer inside the diff.

⚠ **The gate printed the same reading independently.** `gate-17a6274d.log:1418`:

> `[FAIL] 입력 방아쇠 33 파일 · 바이트 자 32 개 · 코드 자 31 개 — 코드 자 1 개 움직임 (문서만 바뀐 파일 1 개는 판정 밖) — 폐포 18 모듈 + 이름으로 더한 모듈 13 + 데이터 1 + 앵커 자신`

**One line carries all three counts and the reason they differ** — 33 files are watched, 32 have a byte
digest and 31 a code digest, because the data file and the anchor itself have no code to digest. *«문서만
바뀐 파일 1 개는 판정 밖»* is `interior.py`. **So the red gate was caused by exactly one moved code digest,
`core_history.py`**, and the diff-reading and the gate's own printed sentence agree without having consulted
each other. The green run prints the same line ending in *«그대로»* (`gate-6c90ae31.log:1414`).

⚠ **The two `seconds` (27.2 → 26.9 and 35.9 → 35.8) are not measurements of anything.** They are the timings
of the re-freeze itself, taken on a machine that had just finished a 32-minute bundle gate. Acceptance line
⑤ reads them **as a ruler, not as a threshold**: they say which run produced the snapshot, and nothing about
whether the solve got faster.

#### C90 (b) 2026-09-19 — the ledger generator runs as a gate step, and its cost needs three rulers to state honestly

**`engine/tools/core_items.py` now runs inside `scripts/check.sh` against `git rev-parse --short HEAD`**, so
a ledger page that disagrees with the ledger cannot pass unseen. Pre-registration 10's trap 4 asked for the
cost to be reported if it was large. **It is not large, and one ruler alone would overstate how small.**

| ruler | value |
|---|---|
| `instr` | **1 044 209 094** |
| share of the gate's total (`93 281 762 738 828`) | **0.0011 %** |
| share of the median step (`15 272 987 247.5`) | **6.84 %** |
| rank | **17th-cheapest of 76 steps** |

⚠ **«0.0011 % of the total» is the lenient ruler and should not be quoted alone.** The five heaviest steps
are **67.6 %** of the total and the distribution spans five orders of magnitude (max
`23 115 860 165 213`, min `214 620 140`), so *any* new step looks negligible against the sum. Against a
median step the new one is **one-fifteenth**; by rank it is an ordinary cheap step, three to five times the
cheapest five (`0.214–0.300 G`) and an order of magnitude under the median. **All three rulers point the same
way, which is why all three are printed.** The rank is the ruler that does not move when one heavy step is
added or removed.

#### C90 (c) 2026-09-19 — the gate's peak memory, and what removing it cost

One expression owned it. Measured alone, the skill-path `git grep -lE` in `scripts/check.sh`'s section 5 peaked at **2 577.0 MiB** and its sibling, the old-path grep beside it, at **974.4 MiB** — enough to account for every logged run (2 572.6 · 2 578.0 · 2 580.9 · 2 583.9 MiB). **Both sat outside `step()`, so the cost appeared in no `[TIME]` and no `[COST]` line.**

**Both prefix and suffix are literal**, so `-F -e <literal>` per alternative selects the same files. ⚠ **Checked on a scratch clone with bait files `git add -f`-ed into the index** — on a clean tree both greps return empty, and *an empty-to-empty comparison proves nothing*. Sorted, old against new: **`:707` 2 = 2 · `:708` 2 = 2, no diff.**

| | before | after |
|---|---|---|
| `:708` alone | **2 577.0 MiB** | **61.2 MiB** |
| `:707` alone | **974.4 MiB** | **53.3 MiB** |
| whole gate | **2 580.9 MiB** | **88.6 MiB** |

**The gate's peak fell 29×**, `rc=0`, and the verdict counts did not move: `[PASS]` **753**. **The price of the edit is one step**: `[STEP]` and `[COST]` go **76 → 77**, and the new step costs **32 833 241 `instr`** — **0.000035 %** of the gate's total. ⚠ *That cost is now printed every run, which is the point of moving it inside `step()`.*

⚠ **The registered prediction named the right number for the wrong reason, and finding out why moved the ruler itself.** It said the new ceiling would be **132.6 MiB, the clone**. The gate printed **88.6 MiB**, below the clone's own standalone figure — so the first reading was *«a block that was seen does not cost what it cost alone»*. **That reading is wrong.**

**Re-measured, the clone is immovable**: 138 969 088 · 138 969 088 · 139 001 856 B — **132.5 · 132.5 · 132.6 MiB** across three runs, 0.02 % apart, cold or warm. It was never cheaper inside the gate.

⚠ **The outer ruler could not see it.** `scripts/check.sh` ends its isolation block with `exec bash "$dest/scripts/check.sh"`, and the clone, the checkout and the scratch cleanup all happen **before** that `exec`. **`exec` discards the accumulated child rusage of the process it replaces.** Shown directly:

| command | `maxrss` |
|---|---|
| `bash -c 'python3 <300 MB>; python3 <small>'` | **308 412 416 B** |
| `bash -c 'python3 <300 MB>; **exec** python3 <small>'` | **8 388 608 B** |

**The same 300 MB child disappears when an `exec` follows it.**

⚠ **So every gate `maxrss` quoted in this repository measures only what happens after the `exec`** — the 2 580.9 MiB before this change and the 88.6 MiB after it alike. **The gate's actual ceiling is `max(88.6, 132.6) = 132.6 MiB`, the clone**, which no run has ever printed. *The prediction's number was right and its reason was not; the failure clause — «if not, there is another block I have not seen» — pointed at the block that was there all along, on the far side of a window boundary nobody had checked.*

⚠ **So «outside `step()`» was never one category — there are three rulers, not two.** ⓐ the `[COST]` sums, which see steps only; ⓑ the outer `/usr/bin/time -l`, which sees **everything after the `exec`**, steps and non-steps alike; ⓒ a window **nothing measures**, the work the `:477` block does before handing over.

⚠ **And «before the `exec`» is not one thing either — sorting the blocks by line number is the wrong ruler.** What decides is the guard around each block, and there are four cases:

| case | blocks | what the outer ruler sees |
|---|---|---|
| exec-only | the `:477` block — stale-scratch cleanup, clone, checkout, gate-logic copy, symlink count | **nothing** |
| runs on **both** sides | unconditional top-level work — the interpreter pin `:25`, the requirements blob `:36`–`:37` | **the second execution only** |
| not reached in these runs | `:448`–`:450`, inside `while [ "$auto_req" = 1 ]` | nothing, because **`--auto-lane` was never passed** |
| after the `exec` | every `step()` and every non-step block past `:524` | **everything** |

⚠ **«Invisible», «runs twice» and «never ran» had been collapsed into one category.** *They are three different facts and only the first is a limitation of the ruler.*

⚠ **The second case leaves a visible trace that had been read as noise**: `[note] gate venv 선언 일치` prints **twice** in every log — `:9` and `:13` in `gate-b4b92728.log`, twice again in the quick log. **That is `:36`–`:37` executing once on each side of the `exec`**, not a duplicated line.

⚠ **One block that looked like the same structure is not.** `engine/backflow.py check` **ran twice in a full gate until `502a5c7b`** — once at `:881` outside `step()`, where its non-`[WARN]` output was printed, and once at `:882` inside `step()`, where the output was discarded and only the exit status was judged. *Both sat after the `exec`*, so this was two call sites invoking one program, not one block executing on both sides of a window boundary — **and that reading still holds; only the call sites are gone.** **The measured half cost `instr` 24 380 241 542 at 22 MB** (⚠ *this paragraph first printed `2 422 389`, a leading-digit truncation of the `24223895184` in `gate-b4b92728.log`, retyped by hand; the figure kept here is read from `gate-e88625c8.log`. The step is not constant across plates — the 43 logs that still ran it twice put it between `24 117 558 355` and `28 207 985 542` — so it is quoted with its log, not as a property of the program*)**; the unmeasured half was never measured at all.** ⚠ **`502a5c7b` closed that, and moved the counter at the same time**: one run now prints and is judged inside one `step()`, but the pipe makes `python3` a grandchild of the timed process, so **the step sum counts backflow about 24.3 G `instr` less than before** — `[COST]` fell from **24 358 653 070** to **31 340 967** while `user` held at **1.00 s → 0.99 s**, which is the signature of a counter moving rather than work disappearing. ***That 0.019 % of the step sum is not a saving.*** `[TIME]` and `user` still see the work.

**The conclusion is a rule, not a list: a line number does not say which window a block falls in — the condition wrapping it does.** ⚠ *Re-splitting the 17-block census has to be done by guard, and the only guard verified here is `:477`.*

**The same boundary applies to `instr`** on the outer `/usr/bin/time -l` line. It does **not** affect the `[COST]` sums used for the width measurement above, which are per-step and all post-`exec`; ⚠ *but the outer line and the `[COST]` sum are two different windows and should never be quoted as one.*

#### ⚠ The `instr` ruler's own reproducibility width, measured — and last night's verdict retracted

**Two full gates ran back to back on the same machine tonight**, `17a6274d` (rc=1) and `6c90ae31` (rc=0), the
trees differing by one JSON file that only the anchor step reads. Removing that step leaves **75 steps of
identical code on identical inputs**:

| run | total `instr` | anchor step | total minus anchor |
|---|---|---|---|
| `gate-17a6274d.log` | 93 285 818 601 091 | 2 381 471 962 889 | **90 904 346 638 202** |
| `gate-6c90ae31.log` | 93 281 762 738 828 | 2 381 524 719 039 | **90 900 238 019 789** |

**Difference −4 108 618 413 = −0.00452 %.** ⚠ *This is the first same-machine, same-night, consecutive pair
this ruler has been measured against*, and it was counted twice from the two log blobs independently by the
work and audit seats. The isolated clone is built outside any `step`, so its work never enters these sums and
did not need removing.

⚠ **It retracts a verdict from 2026-09-18.** That night a **−0.055 %** movement in an `instr` total was
called *ruler noise*, on the grounds that untouched steps had scattered **0.1–2 %** in both signs while the
touched step rose **+1.132 %**. **A width of 0.0045 % cannot support that reading**: the scatter and the
0.055 % total cannot both be noise, and by tonight's number neither is. What survives unchanged is the
touched step's own movement (**+51 052 076**, +1.132 %, attributable); what is withdrawn is the claim that the
remaining −51 G was the ruler. **It is now unexplained, which is a different and smaller statement.**

⚠ **The measurement still owed is the clean one**: two runs of the **same sha**, so that no file differs at
all. Tonight's pair differs by one JSON, and that is why the anchor step had to be subtracted rather than
compared.

**Two rulers that did not settle, recorded so they are not read as settled.** *Seconds*: the leading and
trailing clock loops read **0.886 s** and **0.922 s**, within the ±5 % rule (**+4.06 %**), so seconds are
usable **inside** this run — but the trailing loop sits above the established 0.86–0.88 s band, so this run
licenses no seconds comparison **between** runs. *Peak memory*: `maxrss` was **2 580.9 MiB** here against
**2 578.0 MiB** in the red run (**+0.11 %** — the new step did not move it), but across five full-lane gates
it reads 1 786.2 · 2 022.0 · 2 572.0 · 2 578.0 · 2 580.9 MiB with no monotone relation to the tree. `maxrss`
is the **maximum over children**, so it names whichever child peaked and not the gate's demand. ⚠ **The
~1.8 GiB child from the memory census is still unidentified**, and these five numbers are new material for
that count rather than an answer to it.

#### ⚠ The `instr` ruler at one unchanged sha — the width the night's pair could not give, 2026-09-19

Two full gates ran back to back on `54e4671d`, nothing edited between them. `git status --porcelain` printed **0** four times — before and after each run. Logs `4bcbf6bd…` and `6005514f…`, both `rc=0`, both `matches_tree=yes`.

**The verdict counts are identical in both**: `[PASS]` **753** · `[FAIL]` **0** · `[SKIP]` **13** · `[판정` **5** · `[GRADE]` **4** · `[STOP]` **1** · `[COST]` **76** · `[STEP]` **76** · anchors **602**. The frozen acceptance line — *both runs must print 76* — holds, so the pair is valid.

**Summed `instr`: 93 185 591 977 534 → 93 255 343 092 781, a difference of +69 751 115 247 = +0.07485 %.**

⚠ **Three of the four registered predictions failed.**

| # | registered before the runs | outcome |
|---|---|---|
| 1 | summed difference **< 0.01 %** | **failed** — 7.5× that |
| 2 | lands near **0.0045 %**, the mixed-sha figure | **failed** — 17× that |
| 3 | per-step differences scatter in **both signs** | **held** — 36 up, 40 down |
| 4 | no single step holds **more than half** of the difference | **failed** — one step holds **228 %** of it |

**`test_water_column_steam.py` moved +159 110 075 235 (+2.1684 %)**, which is **228 % of the whole difference**; the next three run the other way — `test_interior.py` −0.2387 %, `test_core_history.py` −0.3140 %, `run.py bodies/earth.yaml` −0.3016 %.

⚠ **A verdict is withdrawn, and it is the withdrawal of a withdrawal.** On 2026-09-18 a **−0.055 %** movement was called ruler noise. That call was retracted the same night on the strength of a **0.0045 %** width. **At one unchanged sha the width is 0.07485 %, so 0.055 % sits inside it** and the original reading stands again. ⚠ *The precise sentence is not «proved to be noise» but **«not distinguishable from run-to-run width, so it cannot be read as a saving»**.*

⚠ **And «the width» is not a single number.** The scatter is not spread evenly — it concentrates in a few steps, and which steps are loud changes between pairs. **0.0045 % was a draw in which the loud step was quiet.** *Two runs cannot set this ruler's tick size; the next measurement is more runs, and the scale has to come from the per-step distribution rather than from the sum.*

⚠ **A counting trap, found by falling into it.** `[COST]` names repeat — `run.py bodies/…` appears **7 times** — and with `GATE_POOL=2` **the two runs finish in different orders**. Pairing rows by position produced `test_fe_s.py` **−75 %** and `test_core_energy.py` **+304 %**, both artefacts. **Rows must be paired by name with duplicates summed.**

#### ⚠ Clearance before the edit, twice — a process record

**Twice tonight a hash was cleared by the audit seat and then the file was edited before the commit**, so the
committed blob was not the blob that was cleared. Both times the content turned out to be within the expected
range, and the audit seat's reading of that is the sentence worth keeping: *«두 번 다 「내용이 예상 범위였다」가
이유였고 그건 규칙이 아니라 운입니다».* **A clearance is a statement about one blob, not about an
intention.** The rule adopted: when a cleared file changes for any reason, send *«해시 바뀌었습니다, 재클리어
주십시오»* before committing — the cost is one message and it removes the luck.

---

#### ⚠ Earth has three present-day CMB temperatures, and the supplier and the consumer reach opposite verdicts

**Measured 2026-09-09, after Briefs 166 D/E. No verdict is drawn here** — this is the asymmetry the third
path has to close, written down where the build that closes it is registered.

| `T_c` at the present epoch | where it comes from | who reads it | what the entropy budget says there |
|---|---|---|---|
| **3 760 K** | the **owner's declaration** (C25 horn ①, `earth.yaml`) | **C15** (`core_entropy_production`, via `get_optional`) | `ΔE` **+26.5 MW/K**, band **−76.3 … +188.3**, 4/8 corners, inner core → **straddles zero, `cannot-say`** |
| **3 770.33 K** | **C14's own root** — the temperature at which its energy balance closes | C14, and C15 as a fallback when no declaration exists | inner core **239.3 km**, **2.04 K** below the cliff at ≈3 772.37 K |
| **3 911.29 K** | **C20's trajectory endpoint** — integrated from the 4 800 K start, fixed and adaptive agreeing | C20 itself; it emits this as `core_cmb_temperature_present` | 3.1 Gyr band **−203.4 … −4.1**, **0/4** corners → **`fails`** |

⚠ **The spread is 151 K and the two ends disagree on the answer.** The declared horn says *cannot-say*;
C20's own endpoint says *fails*. **Both are "Earth, now, under the same four owner decisions."**

**Why they differ is structural, not numerical.** `core_history` (C20) **never reads**
`core_cmb_temperature`: its inputs are the mantle-side `cmb_temperature` (the adiabat's boundary value,
eq. 29's form) plus the two initial temperatures, and it **emits** `core_cmb_temperature_present` as a
result. ⚠ *So owner decision ① reached the consumer and not the supplier.* C15 was rewired in Brief 166 A
to prefer the declaration; C20 has no place to put it, because a declared present-day temperature is not
an input to an initial-value problem — **it is a target the trajectory either hits or misses, and nothing
in this engine compares the two.**

⚠ **That comparison is the missing measurement, and it is one line: C20 misses the declaration by
+151.29 K.** Whether that is C20's initial conditions, its flux laws, or the declaration itself is
exactly what the missing term is supposed to arbitrate — which is why it is recorded here and not in a
verdict. **Recorded consequence for reading C25 (f):** its sentence *"the band still straddles zero"* is
**true at C15's temperature and false at C20's**, and the section should be read as a statement about the
declared horn only.

*(Stale numbers this uncovered: `engine/chain.yaml`'s C20 note still says the node emits **4 028 K** and
**5.07 TW** on Earth — the H 1.5 pW/kg values. Both moved twice on 2026-09-09 and the note did not. ⚠ The
temperature is now **3 911.29 K**; `q_cmb_present` is **re-measured at commit time rather than scaled by
hand**, and the note then carries its condition, which is the repair Brief 166 D applied to the test
anchors. **A third place holding H-conditioned numbers with no label — the C52 candidate's instance
count is now three.**)*

#### ⚠ A pre-registration that turns out wrong is the institution working, not a lapse

**Three registrations failed on 2026-09-09, and none of them was rewritten to match its output.**

| registration | what happened |
|---|---|
| C47 (g)'s fourth cell | its **premise** was falsified; (g) had registered how to record that, and it was recorded |
| C48's diagnosis | the **cause** was misdiagnosed (the out-of-domain call, not the step); the old text is kept in the item's second column and marked superseded on the cause alone |
| C51's `dT_p/dt` < 0 | the row presumed **cooling**; it failed, the wording stands, the outcome is printed as `[기록·실패]`, and a new row checks what a stage-1 transcription can actually own — that eq. (1) closes term by term |

⚠ **The value of a pre-registration is precisely that it can fail**, and the only thing that would
destroy it is editing the sentence afterwards. **So a failed registration is filed, never silently
repaired** — the failure is the measurement. *This paragraph exists because three of them landed in one
day and the pattern is worth naming rather than re-deriving each time.*

#### ⚠ One rule out of three mistakes: the paper's own arithmetic wins

**Three defects of the same kind were found on 2026-09-09, all in one day and all ours:**

| what happened | the paper's own number | ours |
|---|---|---|
| the potassium cap converted with a textbook constant | *"less than 0.17 TW"* → **0.088 pW/kg** | 0.14 pW/kg (3.5 × 10⁻⁹ W/kg per ppm, **56 % high**) — Brief 166 E |
| Sinmyo's CMB temperature relabelled | *"the **upper bounds** … are estimated to be … 3760 ± 290 K"* | our module called the same number a **lower** bound — C25 (e) |
| Earth's present mantle temperature carried three ways | Foley 2018: *"`T_r` = **1623 K** is Earth's present day mantle temperature"*; Korenaga 2009's `T_p` 1350 °C = 1623.15 K; ⚠ *and a fourth, F&B 2014 §8.1's* **1650 K** | our bodies declare **1600 K** (Unterborn+ 2019 §2), and C47's step-4 tables run **both** |
| ✓ **the one that went the right way round** — eq. (3)'s invariance to `T_s` and `d` | Foley prints it in prose: *"in the heat flux scaling law both the mantle thickness and temperature difference **cancel out**, so the equation … is independent of the definition"* | we went to the paper's sentence **first** and only then confirmed it with the exponents (`1 − 4/3 + 1/3 = 0`), so our arithmetic was the check the rule asks for and not a replacement |

⚠ **None of these was a physics error and all three were arithmetic or labelling** — the papers had
already done the work, and we redid it. **The rule, stated once so the next brief inherits it:**

> **Where a paper prints a derived value, that printed value is what we carry. Our own conversion of the
> paper's inputs is a *check* on it, never a replacement — and where the two disagree, the disagreement
> is recorded with both numbers rather than resolved by preferring ours.**

⚠ *This is the same rule `feedback_own_docs_are_base_material` states one level up* (our own documents are
not evidence; go back to the source). **The new part is that it applies to the paper's arithmetic too, not
only to its prose** — a printed 0.17 TW is a source, and a ppm figure we multiply ourselves is not.

### C53 — the tectonic regime is declared as a boolean the sources say does not exist — **pre-registered 2026-09-09, before the build**

⚠ **This section is committed before the change.** C51 (c) found that `stagnant_lid: true/false` is the
*"bimodal distribution … that is typically assumed"* which Foley & Bercovici 2014's abstract names as its
foil, and the parallel seat's P9 survey found **no source that uses a binary**. This registers what
replaces it, what must not move, and the three owner decisions that were taken before any of it was built.

#### The blast radius, counted before the design

| where | what it does | moves? |
|---|---|---|
| `engine/dynamo_rocky.py@«elif stagnant_lid:»` | the **survival gate**: `None` → `cannot-say`; truthy → **`dead (stagnant lid)`**, and `dipole_moment`, `b_eq`, `b_pol` all emit **0** | ⚠ **the only place a value reaches an output** |
| `engine/bodies/earth.yaml` · `mars.yaml` · `pandora.yaml` | the three declarations (`false` · `true` · `false`) | the data |
| `engine/chain.yaml` one edge ref · `test_dynamo_rocky.py` two call sites · the dynamo methodology's `Needs` | text and test inputs | text |

**And two non-consumers, which is the useful half.** ⚠ `heat_transport_mode` **does not read it** —
`engine/tidal_heating.py@«def _mode_from_state(state):»` reads `surface_flux`, `radiogenic_power` and
`radius` only, and the emitted `tectonics` field comes from that computed ladder. ⚠ And **nothing in
`phase2/`, `phase4/`, `db/` or the SPEC mentions it** (grep: 0 hits) — no board row, no curation
contract, no writer. **One live consumer, one branch, three declarations.**

⚠ **A declared boolean and a computed ladder on the same quantity, with no check between them.** Earth
declares `stagnant_lid: false` while the C46 ladder scores Earth **`plutonic-squishy lid`**. **The
consistency check is deliberately not built here** — see *what this must not do*.

#### The data shape

```yaml
tectonic_regime:
  value: stagnant       # stagnant | mobile | transitional | episodic | heat_pipe | contested
  grade: measured       # measured | analog | declared | contested
  source: "2004PEPI..142..225S"     # bibcode, or a list when contested
  note: "single plate in every scheme surveyed (P9)"
```

**The old boolean stays as a derived value, so no consumer changes in this brief:**

| `tectonic_regime.value` | derived `stagnant_lid` | what the survival gate then says |
|---|---|---|
| `stagnant` | **True** | `dead (stagnant lid)` — unchanged from today |
| `mobile` | **False** | dynamo permitted — unchanged from today |
| `contested` | **True** | `dead` — ⚠ **owner decision (a)**, below |
| `transitional` | **None** | `cannot-say (undeclared lid)` — refused by name |
| `episodic` · `heat_pipe` | ⚠ **no mapping declared** | ⚠ **refuse by name**: *"no derived-boolean mapping is declared for regime «X» — owner pending"* |

⚠ **`episodic` and `heat_pipe` are left unmapped on purpose.** No roster body takes either value today,
and guessing would be a seat deciding whether an episodically-mobilising planet gets a dynamo. **The
candidates are recorded and not chosen:** `episodic` → `False` (it mobilises, so a dynamo is permitted)
or `None` (it is stagnant for most of its history); `heat_pipe` → `True` (Lenardic 2018 files heat pipe
as a *hot stagnant lid* sub-mode) or `None`. **Registered as owner-pending.**

⚠ **And the derived boolean erases what the enum was built to carry.** With `contested` → `True`, the
boolean cannot tell `stagnant` from `contested`, which is exactly the distinction P9 measured. **That is
accepted deliberately** — the enum keeps the distinction for any consumer that needs it, and the boolean
keeps today's outputs bit-identical. *A consumer that needs to know Venus is contested must read
`tectonic_regime`, never the derived boolean.*

#### The three owner decisions, taken 2026-09-09 before the build

| # | decision | the owner's reason |
|---|---|---|
| **(a)** | **`contested` → derived `True` → `dead`, field 0** | *"0보다 크면 있다인데 아예 0인 거잖아? 실제 금성 자기장도 대기 상층부의 이온화로 생긴다고 나왔었고. 기전이 아예 다르니까 다이나모가 0이어도 괜찮을 것 같아"* — the dynamo really is zero on such a body, and the field a Venus-like planet does have comes from a **different mechanism** |
| **(b)** | Earth = **`mobile`**, with the note *"the grain-damage scheme (F&B 2014) reads it as transitional"* | our own transitional law cannot be evaluated (C51 (d): seven undeclared non-dimensional inputs), so `transitional` would be a label with no computation behind it |
| **(c)** | Pandora = **`mobile`**, labelled *"owner-declared 2026-09-09 (fiction body, no measurement)"* | a created body has nothing to measure; today's `false` carries no recorded reason |
| (d) | whether the regime reaches a board row | **deferred** — a Phase 4 facet choice |

⚠ **Decision (a)'s label is mandatory and it points at a branch that already exists.** The ionospheric
field the owner names is the **induced magnetosphere**, and `magnetosphere_geometry` already carries that
branch — `engine/induced-magnetosphere-source-check-notes.md` source-checked it on 2026-09-05. ⚠ *But the
authority for the **Venus** statement specifically, Luhmann 1991 (`1991SSRv...55..201L`), is **not
held*** (that note's own table records it), so the label travels as: **a dynamo of 0 does not mean no
magnetosphere; the induced branch is a different mechanism, out of this node's scope, and its Venus
source is uncached.** **Nothing about the induced branch is built or changed in this brief.**

#### The registered regression — the thing that proves no consumer moved

**Three assertions, written before the code:**
1. **The three roster bodies' derived booleans equal today's values bit for bit** — Earth `False`,
   Mars `True`, Pandora `False`. *If any of the three moves, the mapping is wrong, not the data.*
2. `contested` → `True` → the gate returns `dead (stagnant lid)` with `dipole_moment == 0.0`; and
   `transitional` → `None` → the gate returns the **`cannot-say`** string, **not** `dead`.
3. `episodic` and `heat_pipe` raise the named refusal rather than defaulting to anything.

⚠ **The order of operations is fixed here because `check_contracts` will catch it otherwise:** the new
key goes into the dynamo methodology's `Needs` table **first**, then the body files. Reversed, the check
fails class ② (*"a lookup nobody supplies and it is not in Needs"*) — **and that failure would be the
check working**, so it is registered as the expected outcome of doing it in the wrong order rather than
as a risk.

#### What this brief must not do

1. ⚠ **It must not decide Earth's or Venus's regime as a matter of physics.** (b) elects a *statement*
   under a named scheme; the schemes still disagree and P9 records both.
2. ⚠ **It must not touch the computed ladders** — `heat_transport_mode` or C46's five rungs. They read
   flux, not this field, and C51 (d) evaluated them separately.
3. ⚠ **It must not add a consistency check between the declared regime and the computed ladder.** That
   check is worth its own item, because **the first thing it would report is that Earth's declaration and
   Earth's ladder cell already disagree** — and reporting that inside a data-shape change would mix two
   findings in one commit.

**Size:** ~60 lines of code, three body files, three doc edits, gate ~0 s.

#### Amendment 18:14, written before B, from the audit seat's reading

⚠ **The 101 lines above are left exactly as they were approved.** These four items are *appended*, not
merged into them, so that what was registered and what was corrected stay separable in the diff.

**1. Assertion 2's two strings were abbreviations.** The constants are
`dead (stagnant lid, declared)` and `cannot-say (stagnant-lid judgement undeclared)`. ⚠ **So the
regression is hung on identity with `dynamo_rocky.DEAD_LID` and `dynamo_rocky.UNDECIDED_LID`, not on the
literal text** — a test that retypes the sentence would keep passing while the label drifted underneath
it. **Neither constant's string changes in Brief 168.** The three lines, measured **before** the change
(audit seat, at `ccda2d50`), which is what the bit-identity claim compares against:

| `stagnant_lid` today | the gate's label | `dipole_moment` · `b_eq` · `b_pol` |
|---|---|---|
| `True` | `dead (stagnant lid, declared)` = `DEAD_LID` | 0.0 · 0.0 · 0.0 |
| `False` | `undeclared (both emitted)` | 1.0 · 30.0 · 60.0 |
| `None` | `cannot-say (stagnant-lid judgement undeclared)` = `UNDECIDED_LID` | all three **None** |

⚠ **`contested` rides that existing `DEAD_LID` branch and adds one line to the label** — *«contested →
declared-dead; induced magnetosphere is a separate branch (`magnetosphere_geometry`)»* — and
`transitional` reuses the existing `UNDECIDED_LID` path verbatim. *A second cannot-say string would make
the enum look as though it had changed a consumer, which is the one thing this brief registers it must
not do.*

**2. The derived boolean is typed `bool`, and the regression asserts `is True` · `is False` · `is None`.**
`1` and `0` are refused. *An `int` passes every truthiness branch in the gate and is still the wrong type
at the one place a consumer would compare identity — the failure would surface somewhere else, later.*

**3. The transitional collision** (directing seat's decision, reversible). A body file carrying **both**
`tectonic_regime` and the old `stagnant_lid` raises a **named refusal** that says both are declared and
elects neither. A body carrying **only** the old key makes `check_contracts` fire **class ②** — `Needs`
asks for `tectonic_regime` by then — ⚠ **and that firing is the expected outcome, not a risk**, the same
registration the ordering paragraph above already makes. In 168 B the three body files **drop the old key
and keep only the new one**, and the derived boolean is computed inside the node and **never written back
to a body file**. *Two declarations of one quantity is the shape C49 is open for; this brief does not
create a fourth instance of it.*

**4. What the two bibcodes in this section are** — both already confirmed elsewhere, neither re-queried
for this brief. The example `source` is **Stein, Schmalzl & Hansen 2004**
([`2004PEPI..142..225S`](https://ui.adsabs.harvard.edu/abs/2004PEPI..142..225S)), the yield-stress scheme the parallel seat's P9
surveyed, **abstract only** — it illustrates the field's shape and is not a declaration for any body. The
Venus authority named in owner decision (a) is **Luhmann 1991**
([`1991SSRv...55..201L`](https://ui.adsabs.harvard.edu/abs/1991SSRv...55..201L)), and ⚠ **it is not held** — the label travels with
that fact, as the paragraph above states.

### C53 (b) 2026-09-09 — built in the registered order, and the three assertions read as registered

The pre-registration above was committed at `e0ae82e0`; this is what the build measured. **The order was
the registered one** — the methodology's `Needs` first, then the three body files — and the reason it
matters is in the numbers below.

#### The registered regression: the three bodies' derived booleans, bit for bit

Measured **before** the change by solving each body on `3c5ede48`, and again after:

| body | declared `tectonic_regime` | derived `stagnant_lid` | the node's verdict | `ℳ` · `B_eq` · `B_pol` |
|---|---|---|---|---|
| Earth | `mobile` · declared · [`2018AsBio..18..873F`](https://ui.adsabs.harvard.edu/abs/2018AsBio..18..873F) | **`False`** (was `False`) | `undeclared (both emitted)` · alive | 1.0 · 30.0 · 60.0 |
| Mars | `stagnant` · measured · [`1998JGR...10313643R`](https://ui.adsabs.harvard.edu/abs/1998JGR...10313643R) | **`True`** (was `True`) | `cannot-say (conductor_phase undecided)` | None · None · None |
| Pandora | `mobile` · declared · owner, 2026-09-04 | **`False`** (was `False`) | `undeclared (both emitted)` · alive | 1.0 · 41.37252479971432 · 82.74504959942864 |

**Every emitted value is bit-identical**, Pandora's 17 significant figures included, and the booleans are
`bool` — the test compares with `is`, so `1` and `0` would fail it. ✓ Assertion 1 as registered.

⚠ **Two things did change, and neither is a value.** The gate's label line said *«정체 암석권 선언»* and
now says *«정체 암석권 파생 … (tectonic_regime 선언에서)»*, because a derived value must not be labelled
declared. And the evidence key in `Result.inputs` moved from `stagnant_lid` to `tectonic_regime` —
required, not cosmetic: see below.

#### Assertions 2 and 3, hung on constants rather than on text

`contested` → `True` → the gate returns **`dynamo_rocky.DEAD_LID`** with `dipole_moment`, `b_eq` and
`b_pol` all `0.0`, and the label carries the extra line the owner's decision requires (the induced
magnetosphere is a separate branch). `transitional` → `None` → **`dynamo_rocky.UNDECIDED_LID`**, and
`dipole_moment` is `None` rather than `0.0` — *not* dead. ✓ Assertion 2. `episodic` and `heat_pipe`
return the named refusal with their own name inside it and are absent from the derivation table
altogether. ✓ Assertion 3. ⚠ **The comparisons are identity with the module constants, never the literal
sentences** — a test that retypes a label keeps passing while the label drifts underneath it.

#### The ordering rule fired, exactly as registered — on the evidence key

⚠ **`check_contracts` failed on the first run after the body files changed**, with both halves of the
same message: *«문서가 Needs 에 적었는데 코드가 안 쓴다 — tectonic_regime»* and *«코드가 쓰는데 문서
Needs 에 없다 — stagnant_lid»*. The lookups were already right; what was wrong was the **evidence
label**. The check compares `Result.inputs`' keys against the printed `Needs`, and the name in `Needs`
is the name of the **declaration**, so the recipe's evidence has to carry `tectonic_regime` and the
derived boolean has to live in the label line. That is C37's rule (a label and a lookup are one string)
arriving through a different door, and **the check found it rather than a body's output being wrong**.
After the rename: 14 contracts match, class ③ stays at its C50 baseline (8 nodes · 8 keys · 13 pairs),
and the lookup count went 1182 → **1206**.

#### Two corrections to the pre-registration itself

1. ⚠ **Decision (c)'s stated reason was wrong.** The pre-registration says Pandora's `false` *"carries no
   recorded reason"*. It did: two comment lines above it anchor the board's own prose (*mobile lid, not
   stagnant*, from the volcanism and continental-drift rows) and were already citation-checked. So the
   owner's declaration is a declaration **standing on those anchors**, not one filling a void, and the
   body file now says so. The decision does not change; its ground does.
2. ⚠ **Mars's `True` does not support today's verdict.** The survival gate tests `conductor_phase`
   **before** the lid, and Mars's is `undecided`, so Mars answers `cannot-say (conductor_phase
   undecided)` and never reaches `DEAD_LID`. Mars's output is the same whether its regime is `stagnant`
   or `contested`. That is why assertion 2 is tested on the gate function at fixed inputs and not on a
   body — and it is worth writing down, because *«Mars is stagnant, therefore no dynamo»* is a sentence
   this engine does not currently execute. **This is now C54.**
   ⚠ **And it hollows out one third of assertion 1 at the output layer.** All four mapped regime values
   give Mars the same emitted result, so «Mars's output is bit-identical» would have held even if the
   mapping were wrong — the Mars leg is carried entirely by the unit test on the derivation, not by the
   body. Earth's and Pandora's legs are load-bearing at the output layer; Mars's is not, and a later
   seat reading three green rows would not see that without this sentence.

#### What this did not do

The consistency check between the declared regime and C46's computed ladder is **still not built** — its
first report would be that Earth declares `mobile` while the ladder scores Earth `plutonic-squishy lid`,
and that belongs in its own item. `episodic` and `heat_pipe` are **still unmapped, owner-pending**; the
parallel seat's P10 survey of dynamo survival under those two modes arrived while this was being built
and is not read here. And `heat_transport_mode` was not touched: it reads the computed flux ladder.

### C52 — how many recorded anchors rest on one shared constant, and nobody counts — **named and counted 2026-09-09; no checker built**

C45 asks whether a node's lookups are declared. C50 asks whether a declared `Needs` is supplied. ⚠ **Neither
asks how many nodes' recorded anchors depend on one shared module constant** — and that question is the one
that fired twice this week, both times as a gate failure rather than as a check.

#### Instance 1 — `core_energy.H_CORE`, and the sweep that closes the count

Brief 166 D found it: C48's reproduction anchors were reading `core_energy.H_CORE` through
`params["h_core"]`, so a constant declared for **C14/C15** silently re-defined what **C20** had recorded.
Six places were repaired then (166 D and 167 A). ⚠ **This item's closing sweep says the number of places is
not six but ten**, and that the three it had not touched had each gone wrong in a *different* way:

| where | what it holds | what was wrong |
|---|---|---|
| `core_history.py`'s `H_CORNERS` comment | mirrors `ce.H_CORE_RANGE` | said `(0, 0.14e-12)` while the constant said `0.088e-12` — ⚠ **the label went stale, not the value** |
| `core-thermal-history-context-notes.md` §4 | the run record of 2026-09-04 | its labelling sentence named 0.14 pW/kg as *the declared value*, superseded by 166 E the same day |
| `tools/adaptive-step-prereg.md` | the Brief 157 pre-registration: 1525.46 K · 4027–4028 K · 1135 steps | ⚠ **no condition at all** — the numbers are right for what was registered and never said under which `H` |
| the other seven | `test_core_history.py` · `tools/mars_step_sweep.py` · `bodies/mars.yaml` · `chain.yaml` · `chain-explorer.html` (generated from it) · `pandora-1600k-analogy-notes.md` · `interior-dynamo-handoff-context-notes.md` | labelled in 166 D / 167 A, still correct |

⚠ **The disease changed shape between the two rounds, and that is the finding.** In 166 D the *numbers* had
no labels. Here the *labels* had gone stale — because the constant moved **twice in one day**
(1.5 → 0.14 → 0.088 pW/kg), and a label written after the first move was wrong after the second. A rule that
says "name the condition" does not survive a condition that moves; what survives is a label that names
**where the condition is declared**, which is why the repair points at `ce.H_CORE_RANGE` rather than
retyping the number. The pre-registration was labelled by *appending*, never by editing what it registered.

#### Instance 2 — `mantle_budget`'s four Earth defaults, and why two counts disagreed

The audit seat counted **5** by AST where an earlier grep had said **3**. Both were right about different
questions, and the AST run that settles it prints this:

| function | Earth default in the signature | Earth constant in the body | forwards `**flux_kw` |
|---|---|---|---|
| `ra_internal` | `d_m=D_MANTLE_M`, `g=G_M_S2` | — | no |
| `f_man_w_m2` | `d_m=D_MANTLE_M`, `g=G_M_S2` | — | no |
| `volumes` | `r_p_m=R_P_M`, `r_c_m=R_C_M` | — | no |
| `dtp_dt_k_s` | `r_p_m=R_P_M`, `r_c_m=R_C_M` | `D_MANTLE_M`, `G_M_S2` | **yes** |
| `f_man_lid_variables` | — | `D_MANTLE_M` | **yes** |
| `secular_cooling` | `r_p_m=R_P_M`, `r_c_m=R_C_M` | — | **yes** |

**5** is the number of functions whose *signature* carries one of the four; **3** is the number carrying the
*radius pair* specifically, which is what the grep matched; and **6** is the number that touch any of them at
all — the fifth and sixth routes being a body-level fallback (`flux_kw.get("d_m", D_MANTLE_M)`) and a
`**flux_kw` that lets a caller's value arrive without the constant's name appearing anywhere in the callee.
⚠ **So the earlier «three of them take it indirectly through `**flux_kw`» and the audit's «the defaults are on
the line after `def`» were both true and neither was the count** — one described the forwarding, the other the
signatures. This is the item's own lesson arriving on itself: *a count is not a fact until the question it
answers is written beside it.*

#### What is not built

No checker. What one would have to ask is now stated: **for each module constant, how many other nodes' recorded
anchors change if it changes** — which is neither C45's question (are the lookups declared) nor C50's (is a
`Needs` supplied), and would need the anchor tables as data rather than as prose. That is a build, and this item
is closed at *named, counted, and labelled* rather than at *fixed*. ⚠ Instance 2 is **not** repaired: the four
Earth defaults stay where they are, and nothing in `mantle_budget` moved for this item.

### C50 (b) 2026-09-09 — the twelve rows read before anything is repaired, and eight of them are one defect

⚠ **This section is committed before the repair.** C50 counted: class ① is live in 3 nodes / 4 keys and
class ③ in 8 nodes / 8 keys (13 pairs). The count said nothing about *which of two faults* each one is —
the contract is wrong, or a body declaration is missing — and that is what this brief reads first. Every
row below names where the recipe actually looks, what the methodology's `Needs` line says, and whether any
body declares it; the repair direction and the expected output movement are registered **before** the
repair, so that a movement of zero is a prediction rather than a description.

#### Class ① — the lookup misses everywhere and the `None` is filed under that name (C37's signature)

| # | node · key | what the recipe really does | verdict | repair | expected movement |
|---|---|---|---|---|---|
| 1 | `body_class` · `gas_mass_fraction` | used **only** inside `_ice_giant_vs_gas_giant`, and that branch already refuses by name: *«이 경계를 답하려면 `gas_mass_fraction` 을 선언해야 한다»* | ⚠ **the contract is wrong** — a *conditional* need is listed unconditionally, so every rocky body files a `None` it never consulted | mark the need conditional in `body-class-methodology.md`; the named refusal stays | **0** — no roster body takes that branch |
| 2 | `body_class` · `semi_major_axis_au` | same branch; `pebble_isolation_mass(a or PEBBLE_ISO_REF_AU)` falls back to a reference distance | ⚠ **the contract is wrong**, and a second question underneath: the value exists in the system data, so the supplier should be an edge, not a body declaration | conditional in the doc, and record that the supplier is the orbit, not a declaration | **0** |
| 3 | `dynamo_rocky` · `dynamo_regime` | undeclared is the **designed** state: the recipe emits the dipolar and multipolar branches both, and C11 records that regimes 2 and 3 have no elected number | ⚠ **the contract is wrong** — this is an optional override, and calling it a need makes a deliberate absence look like a hole | move it out of `Needs` into a declared-override line | **0** |
| 4 | `interior_layers` · `porosity_cap` | ⚠ **neither of C50's two faults.** `interior.py@«inputs["porosity_cap"] = P_LAB_MAX»` writes a **module constant** into the evidence under a `Needs` name while the lookup itself missed | ⚠ **the recipe's evidence is wrong** — a third category this reading found | record it as what it is (the constant the solver used), not as a lookup that succeeded | **0** in values; the evidence line changes. ✓ *repaired 170 B* |

#### Class ③ — a `Needs` no body supplies, and the call site coping

| # | key · nodes | the call site | verdict | repair | expected movement |
|---|---|---|---|---|---|
| 5 | `core_material` · `cmb_heat_flux`, `core_energy_balance`, `core_entropy_production`, `core_thermal_history` | `state.get("core_material", "fe_prem")` in all four | **a declaration is missing** — this is the cleanest of the twelve | declare it on Earth with its source (PREM). ⚠ **Mars and Pandora are owner-pending**: `fe_prem` is *Earth's* PREM, and asserting it for a lighter Martian core is a choice, not a transcription | **0** if the declared value equals the default — to be measured, not assumed |
| 6 | `ice_mass_fraction` · `dynamo_rocky`, `internal_heat_nontidal`, `interior_layers` | `dynamo_rocky` reads it with `get_optional` and prefers `composition_intent`'s preset (C28); `radiogenic` defaults 0.0 | ⚠ **the contract is wrong** — for `dynamo_rocky` the real need is `composition_intent`, and the declaration is the optional override | fix the `Needs` line to name what is actually required | **0** |
| 7 | `differentiated` · `interior_layers` | `state.get("differentiated", True)` | **the contract is wrong** — optional with a documented default | see the structural note below | **0** |
| 8 | `envelope_z` · `interior_layers` | `state.get("envelope_z", 0.0)`, and the code says why: *«Z 는 선언이다. 강착과 진화가 정하는 값이고 이 레시피에 그 둘이 없다»* | **the contract is wrong** — optional, and the file already says so in prose | as above | **0** |
| 9 | `gas_mass_fraction` · `interior_layers` | `state.get("gas_mass_fraction")`, `None` meaning "not a gas body" | **the contract is wrong** — optional | as above | **0** |
| 10 | `initial_porosity` · `interior_layers` | `state.get("initial_porosity", 0.0)`, whose comment says the default *«means this recipe does not decide, not that porosity is zero»* — **and** the inverse path writes `inputs["initial_porosity"] = phi` | ⚠ **one fault, not two** — optional-in-contract only. ⚠ *This row read the second half wrong; see the correction below* | the contract line; **the write stays** | **0** |
| 11 | `tidal_heating` · `interior_layers` | `bool(state.get("tidal_heating", False))` | **a declaration is missing, and it is not free** — ⚠ Pandora has tidal heating on the board (C30, 45 W/m²), so declaring `true` there **would move the structure solve** | ⚠ **owner-pending**: this is the one row whose repair is a physics decision, not a transcription | ⚠ **non-zero for Pandora** — the only row that is not expected to be silent. ⚠ *Declared 170 D and the prediction **failed**: nothing moved. See the record below* |
| 12 | `permanent_quadrupole` · `tidal_locking` | `bool(state.get("permanent_quadrupole", False))` | **the contract is wrong** — optional; electing a non-zero value for any body would move its locking timescale | doc; ⚠ any value is owner territory | **0** while it stays absent |

#### The structural reading: eight of twelve are one defect

⚠ **Rows 1, 2, 3, 6, 7, 8, 9 and 12 are the same fault wearing eight faces** — the contract has **one word,
`Needs`, for two different things**: an input without which the recipe cannot answer, and an input the
recipe *declares a default for and says so in prose*. `interior.py` already writes the distinction in
comments; the contract cannot express it, so the checker counts eight healthy defaults as holes. **The
repair for those eight is therefore one thing, not eight** — a second contract line the checker reads
(a declared-optional list) — and it changes no output at all.

That leaves **four genuine rows**: two evidence defects (4, 10, the same shape as C37's), one missing
declaration that should be free (5, with two of its three bodies owner-pending), and one missing
declaration that is not free (11, Pandora's tidal heating).

⚠ **What must not happen here.** No value is elected to make a count go down. Row 5's Mars and Pandora and
row 11's Pandora stay **owner-pending** even though declaring something would empty their cells — a class ③
cell emptied by a guess is worse than the cell, because the guess then reads as a declaration with a
source. And the class ③ baseline `(8, 8, 13)` moves **only with the reason written beside it**.

#### The closing condition, registered

`CLASS1_KNOWN` becomes empty and the class ③ baseline drops, with each drop attributable to one row above.
⚠ **It will not reach zero in this brief**, and that is registered now rather than reported later: rows 5
(Mars, Pandora) and 11 stay until the owner decides.

#### Correction 170 C — one of the two «evidence defects» was a convention

⚠ **Row 10 was wrong, and the gate said so.** Brief 170 B removed
`inputs["initial_porosity"] = phi` from the inverse-solve branch as an evidence defect, and gate207 failed
with `KeyError: 'initial_porosity'` from `test_interior`'s low-density-satellite roster.

**Writing the inferred value back under the axis's own name is this file's convention, not a defect.**
`interior.py` does the same at three other places — the generic `inputs[axis] = x`, and
`core_mass_fraction` and `ice_mass_fraction` in the composition inversion — and the test reads it the way
the convention intends: `res.regime` names the inferred axis and `res.inputs[axis]` is the value the
inversion read back. So the sentence *«the recipe writes its own solved value into the evidence»* is true
and is not a fault: an inverse solve **reports what it inferred**, under the name of the thing it inferred.

⚠ **`porosity_cap` is genuinely different and its repair stands.** It is not an inferred axis; it is a
module constant the solver chose, and a constant sitting in the evidence under a lookup's name is exactly
*«the value is absent and the name is present»*. Only that one is gone.

⚠ **How the reading went wrong is the part worth keeping.** Two adjacent lines were read as one fault
because they were adjacent, and the convention they belong to lives **three functions away**. A `grep` for
the literal `inputs["initial_porosity"]` found the write and could not find its meaning, and the consumer
that would have shown it reads the key through a **variable** (`res.inputs[axis]`), which no literal search
returns. The test that covers it was one step costing 1 484–1 733 s — 40.5–41.7 % of the step-time total, not of the wall clock — **until `4e4b08af`; since 2026-09-18 it is two steps**, the ocean block (845 s, 59.3 % of the file measured solo) having moved to `engine/test_interior_ocean.py`, leaving about 580 s here (measured over five gates on 2026-09-17/18; the seconds track machine state while the share does not, the 1 484 s run having a 3 602 s total; the line read «459 s» until then, with no denominator) and was deferred to the gate rather than run before the
commit — the gate caught it in the isolated lane, which is what that lane is for, and the scratch was kept
because `rc=1`.

#### ⚠ Where the ocean step's seconds go — counted, 2026-09-19

*Why here: that paragraph is the only place in the ledger that prices this test's step, and this row says where the price goes. Source blob **`5ea86a68`**, registered in **`80c41938`**.*

**One ocean step, counted rather than timed.** `density()` was called **38 062 675** times and
`pressure()` **459 612 424** times — **12.075 `pressure` calls per `density`**. ⚠ **The Newton loop's cap
is 60 and the measured maximum is 13**: **69.45 %** of calls take 4 iterations, **30.37 %** take 3, and
the loop is therefore not where iterations pile up. **34.69 %** of `density` calls repeat a
`(class, p, t, t_pot)` key already seen; the top key repeats **18 times** in 38 million calls, so the
repetition is broad and shallow. ⚠ *This counts repetition; it does not say a cache is worth it.*

**What an analytic derivative would buy, measured in isolation** (`Phase` on `fe_prem` at 50 GPa,
`pressure` 149.5 ns, `density` 3.03 µs): the 12.08 `pressure` calls inside one `density` cost **≈1.81 µs,
59.6 %** of it; removing two of the three calls per iteration leaves ≈4.03 calls and saves **≈1.20 µs —
39.7 % of a `density` call**. ⚠ **That is the ceiling on `density`, not on `solve()`** — the shooting
loop, the phase ladder and the ocean layer are untouched, and their share is unmeasured. ⚠ **It also
moves the last bits**, so any registration that builds it must state a tolerance instead of claiming
bit-identity.

**The bookkeeping is the small term.** A no-op `convergence.note` run reproduced the total exactly —
**39 206 250** notes across **10 sites**, of which `eos.density_newton` holds **38 045 467**, which is
**38 062 675 − 17 208**, the density calls minus the early returns. The notes cost **79 031 525 392
instructions, 0.311 %** of the run — **2 016 instructions per note** against roughly **666 577 per
`density()` call**. ⚠ **No share of `solve()`'s 28.6 s is attributed here**; the step from a `density`
call to a whole `solve()` needs the shooting loop's own profile, which this run does not have.

**Code this row points at**: `engine/eos.py@«이 자리가 적분 안쪽 고리라 반복 횟수가 그대로»` — the
docstring sentence that says why this loop's iteration count is the run time — and
`engine/eos.py@«dfd = (self.pressure(rho + h) - self.pressure(rho - h)) / (2.0 * h)»`, the two-sided
difference an analytic derivative would delete.

---

#### Record 170 D — the owner's two declarations, and a registered prediction that failed

The owner decided two of the three held rows on 2026-09-09: Pandora's `core_material` = `fe_prem`
(owner-declared, a fiction body with no literature to transcribe) and Pandora's `tidal_heating` = `true`
(owner-declared, the board's forced-eccentricity heating switched on in the structure solve). Mars's
`core_material` stays held pending a survey of light-element iron candidates.

⚠ **Row 11 registered that the second one would move the answer. It moved nothing.** Measured before and
after, on Pandora, every value of every node this brief could touch:

| node | values compared | moved |
|---|---|---|
| `interior_layers` | 19 | **0** |
| `core_state` | 14 | **0** |
| `dynamo_rocky` | 11 | **0** |
| `body_class` | 4 | **0** |

**The reason is in the source and it is not an accident.** `interior.py` says of this input:
*"`tidal_heating` 도 계산에 쓰이지 않는다"* — it is not used in the calculation. It is one of the three
indicators in `porosity.voids_expected`, all three of which fire **only toward «no porosity left»**, and
Pandora already trips the first two by a wide margin: its mass is **38 501×** the observed transition mass
and its central pressure **23 765×** the grain-crushing threshold. The verdict `voids_expected` was
already `False` and stays `False`.

⚠ **Two corrections to the paragraph above, both from the audit seat.** *(1)* The multipliers first
reported were **38 222 and 22 000** — hand-computed here from a mass rounded to 0.64 M⊕ and a *guessed*
central pressure, while the body declares **0.6447** and the solver has its own pressure. The numbers
above are the ones the recipe **prints**, and the first pair was an instance of the very thing this file
keeps recording: a number carried without the run that produced it. *(2)* **«Nothing moved» was about the
values, and the evidence did move** — `inputs["tidal_heating"]` goes `False` → `True`, and the porosity
note gains a third ground. The declaration is visible in the record and invisible in every answer, and
those are different sentences.

⚠ **The registration is left as written and the failure recorded beside it** (the C45 ⓐ format): what
failed is the prediction, not the code, and rewriting the row to match the outcome would erase the only
evidence that it was written first. **What the row got wrong was the direction of «it is not free»** — the
declaration is *not free to state*, because it asserts a physical fact about a body, and that is why it
was the owner's to make. It is entirely free in the *answer*, and those are two different freedoms that
the row ran together.

⚠ **And C50's counter reached zero, which 170 A registered as impossible in this brief.** That
registration was right about the mechanism — the remaining cells were waiting on owner decisions — and
wrong about the timing, because the decisions came the same day. ⚠ **Zero does not mean every question is
answered**: the check asks whether *any* sample body supplies a key, and Mars still declares no
`core_material` at all. Its cell is empty because Earth and Pandora fill it.

### C74 — the silicate slot answers from a fit, and a fit cannot be asked «what if this mantle has more iron» — **listed 2026-09-11 — open on P34's A–I only; licence Q1–Q7 answered 2026-09-11 by the REBOUND precedent + owner decision (a)**

This folds P34 (parallel seat, `~/Desktop/NearStars-artifacts/2026-09-09-c20-entropy-band/P34-silicate-slot-prereg-draft.md`,
sha256 `10034d9c085a6dde`, 19376 B — folded from the `6b8fe8a871a5bbc3` state, 11487 B, plus that
file's Amendments 1–3) together with what P30 §6 and §8 have established since. The work seat's
fold is `2026-09-11-interior-state/drafts/C74-silicate-slot-ledger-draft.md`, sha256 `b021b9ae72975150`,
15008 B. ⚠ **The pinning is one-directional by the audit seat's ruling**: this section pins P34 by hash,
and P34 names this draft by path only, so neither document can falsify the other by being edited. ⚠ *«One document at two times» is read from the two dated
amendment blocks and the byte arithmetic, not from a byte diff* — no copy of the 11487 B state survives
on disk (parallel seat, 2026-09-11), so nothing here rests on having compared them.

⚠ **A number, not yet an item.** C74 is listed so the material can be cited and argued against; it
becomes a registered item when the owner has answered A–I or marked them deferred. *That condition is
P34's own, and this section does not relax it.*

⚠ **No value is transcribed.** Every number that will be compared is named by where it lives.

⚠ **Installed 2026-09-12 (191), and nothing in the engine imports it.** `burnman==2.1.0` now lives in
**`engine/.venv-burnman`** (Python 3.9.6), pinned by the new **`engine/requirements-burnman.txt`**;
`engine/.venv` and `engine/requirements.txt` are untouched, because that file's `mpmath==1.4.1` is
`test_fermi.py`'s second oracle and `sympy 1.14.0` requires `mpmath<1.4`. **The downgrade was measured
before the split was taken**: on the only thing in this repository that reads mpmath, 26 states agree to
every printed digit between 1.4.1 and 1.3.0 (`191-fermi-oracle-mpmath.txt`,
`c628f7e35a2c2320`) — so the split stands on the pin's integrity and owner row F, not on that
uncertainty. P34's prohibition 6 is untouched: **no engine module imports BurnMan**, the gate still runs
on system python, and owner decision F — which interpreter the silicate node uses when a body is
solved — is open.

**191's four print-only checks, run 2026-09-12** (`191-burnman-checks.py` `b8a5465c61bf893f`, output
`191-burnman-checks.txt` `841469652ec5493a`; the pins `191-burnman-freeze.txt` `270841f1f4e02e86`):
`burnman.__version__` is **2.1.0**; `equilibrate` **converges on SLB_2022 phases** — `olivine` and
`wadsleyite`, root in **5 iterations**, at 12.954 GPa for T = 1600 K, which is the first answer the
repository gave to P30 §7's registered question; the installed `SLB_2011.py` · `SLB_2022.py` ·
`SLB_2024.py` carry **61 · 77 · 92** `^class` lines, equal to the reading copies in `P30-data/`; and
**all eleven author-not-recommended species** decision C excludes are present to be excluded. ⚠ *No
property value was read from any of them* — the checks print counts, versions, a hash and a convergence
verdict.

⚠ **The licence absence is the registered result, not a gap**: neither `burnman/` nor
`burnman-2.1.0.dist-info/` holds a `LICEN*` or `COPYING` file, so the GPL v2 text the NOTICE row rests
on is the **repository's** `license.txt`, held as `P30-data/burnman-license.txt`
(`8177f97513213526df2cf6184d8ff986c675afb514d4e68a404010521b880643`) and not a file the install ships.
*The first run of that check asked «is `burnman` in the path» and passed every package in a venv whose
own directory name contains `burnman` — eighty-odd licence files read as «present». The fixed check
prints where it looked, which is what makes an absence checkable.*

⚠ **The closure counts 29 by download and 28 by install, and both are right**: `osqp` (← `cvxpy` ←
`burnman`) requires `setuptools` with no upper bound, which the venv's bundled **58.0.4** — the version
macOS's `/usr/bin/python3` puts into a fresh venv — already satisfies, so the closure's fetched
`setuptools 82.0.1` was never installed, and `pip freeze` hides `setuptools` and `pip` in any case.
⚠ **So the pin file carries `setuptools==58.0.4` as its 29th line**: a list that yields a different
environment depending on which interpreter built the venv is not a pin, and 58.0.4 is the version 191's
four checks actually ran against — «pin what you checked», not a number nobody chose. Its wheel is held
beside the artifacts (`191-closure/setuptools-58.0.4-py3-none-any.whl`, 816539 B,
`69cc739bc2662098a68a9bc575cd974a57969e70c1d58ade89d104ab73d79770`, `py3-none-any`, resolved on
Python 3.9), so the file names only archives we hold. ⚠ **Two counts travel together and stay split**:
the **pin file is 29 lines**, the **closure record is 30 archives** — the 29 measured before the
install plus this `setuptools 58.0.4`, with `82.0.1` kept as «fetched, not installed». *The 82.0.1 is
the parallel seat's measurement of the download closure; this install never fetched that archive, so it
is not re-derivable from here.* 
⚠ **The venv broke three tree walkers, and 191 fixes them because 191 broke them.** `.gitignore` tells
**git** to ignore `engine/.venv-burnman`; it tells a scanner nothing. `engine/check_refs.py` skipped
the exact string `.venv`, so it walked the new venv and found `burnman/tools/eos.py` beside
`engine/eos.py` — **18 citations turned ambiguous in a tree where nothing citable had changed**
(`eos.py` 13 · `state.py` 2 · `chain.py` 1 and three more). The same name-exact skip sits in
`scripts/check_md_tables.py` and `scripts/check_md_dupes.py`, where it had not failed yet only because
nothing had looked: with the prefix skip in place `check_md_tables` scans **827** files against the
**833** of the broken run, and `check_md_dupes` now reports «`.venv*` 10개» — ten markdown files that
were being read as ours. All three now filter path components that **start with** `.venv`, and
`check_refs`'s second walk — which had filtered `.git` alone, so the two walks disagreed about what the
repository contains — uses the same skip. `scripts/check_dead_links.py` and `scripts/check_language.py`
enumerate through `git ls-files` and `scripts/build_sitemap.py` and `scripts/check_site_links.py` walk
`docs/` only — and `scripts/retrofit_paper_links.py`, which does not run in the gate, walks
`docs · plans · phase2 · phase3 · phase4 · gameplay · ko` and never `engine/` — so none of those five
can see a venv at all (checked, 2026-09-12, and confirmed rather than changed). ⚠ *The «18 ambiguous»
count is the work seat's measurement **with the venv present**; it cannot be reproduced on a tree
without one.* ⚠ *And `check_refs`'s second walk was already exposed by the old `engine/.venv` — that
site filtered `.git` alone, so this is a pre-existing hole the new venv only made reachable.*
**The rule: `.gitignore` speaks to git, not to scanners — every tree walker needs its own skip.**
⚠ **And the fix is measured to have changed nothing else**, against the `3716708f` gate log: each markdown
checker scans **827** files and `check_refs` resolves **559** anchors, before and after — *the widened
second walk also stopped seeing `ko`, `_papers`, `.archive` and `node_modules`, and no resolution moved*
(audit seat, 2026-09-12). *This line rides 195's commit rather than 191's: the clearance was attached to
a hash, so a fact arriving after it goes in the commit message, not into the approved file.*
191's Amendment 7 records the sweep; the registered draft is `f135ab70e9cf8658`, 298 lines. `mpmath` resolved to **1.3.0**, as Amendment 2 predicted.

⚠ **Three papers that P34 treated as pending are held**: `2022GeoJI.228.1119S.pdf`,
`2024GeoJI.237.1699S.pdf` and `2011GeoJI.184.1180S.pdf`. Everything about the tables below is read from
those PDFs directly, and the **provenance rows were corrected 2026-09-11** — `P30-data/PROVENANCE.txt`
(`ebcb4d8e7a0647d2`, 3493 B) now carries a row per paper with its path and sha256, measured here.
⚠ *An earlier version of this material flagged that file as still saying «OUP 403, owner request B»,
and that flag was false against the file*: the 09-10 statuses were already marked superseded, so the
draft had quoted the superseded notice as if it were live. *What the refresh fixed was narrower — one
prose line instead of three rows, no path per paper, a truncated sha (parallel seat's account of the
`849f6b2e1b7052ca` state, which no longer exists on disk to be re-read).* Recorded rather than deleted,
because a ledger that keeps a defect nobody had is worse than one that keeps none.

#### What the owner has already decided (P30 §5, 2026-09-10) — inputs, not open

| # | decision |
|---|---|
| (a) | BurnMan is a **runtime dependency of the engine, not an offline grid generator**, pinned `burnman==2.1.0` (GPL-2.0-or-later). ⚠ *That clause is what decision I's cached-grid candidate has to answer to, and the licence sentence that has to accompany the pin is still open — see F and Q7 below.* |
| (b) | the parameter base is **S&LB 2022** (`burnman.minerals.SLB_2022`) — not 2011, not 2024 |
| (c) | ① the body file declares **chemical ratios** (Mg/Si, iron content, C/O and the like; **exact keys pre-registered at build time**); ② the mineral assemblage is **computed by a sourced rule** — **S&LB 2022 phase boundaries + BurnMan equilibrium**, *whether `burnman.equilibrate` or similar exists in 2.1.0 and runs with the SLB_2022 `Solution`s is to be verified at build time* — and hard-coding an Earth-reference assemblage and perturbing it is **forbidden**; ③ a body whose mineral fractions are known directly may **declare them and override** ②. Composition travels as a **node contract**; no module-global state |

⚠ **(c) ② is the whole point of the item.** The engine already has a silicate answer — two fitted
`Phase` objects. What it does not have is an answer that *changes when the chemistry changes*. A fit
cannot be asked «what if this mantle has more iron»; an assemblage can.

#### The two checks that moved since P34 was written

**Check ① — the first-call convergence check, and it is a stop condition.** Rebuild BurnMan's own
`example_equilibrate.py` assemblage with the **SLB_2022** counterparts and run it at the example's own
(P, T) constraints. Converges → the programme proceeds. Fails or throws → **named refusal**, «SLB_2022
assemblage does not equilibrate in BurnMan 2.1.0 at the example conditions», and the programme stops at
owner row A's fallback. ⚠ *No tolerance is loosened past the function's defaults without recording it* —
a check that can be made to pass by widening it is not a check. **The reason this is first is P30 §7:
`equilibrate` is shipped with SLB_2011 examples and is untested with SLB_2022 in BurnMan's own
repository**, so the risk is not in our code at all.

**Check ⑦ — not a pair of numbers, and not even a «window».** P34 wrote «read the dataset's stated
P–T range». **Neither paper states one.** What they print is measured below, read from the held PDFs
rather than from our own transcription of them — *an earlier version of this material repeated P30's
summary and got four things wrong about the tables, which is the rule about our documents being base
material and not evidence, arriving on schedule.*

| what P30's summary said | what the PDF prints |
|---|---|
| 2022 Table A4 has *Species · P_min · P_max · T_min · T_max* | **Species · N · P_min(GPa) · P_max(GPa) · T_min(K) · T_max(K) · Ref.** |
| 2024 Table C4 has *N · P_min · P_max · T_min · T_max · Ref.* — a different shape | **the same seven columns.** The two tables have identical structure, and a sampled species row was checked to agree between them — *the row itself is not transcribed here* |
| «per species and per reaction» = the 2022 table and the 2024 table | **both granularities live in each paper**: A4 *stability* (per species) and A5 *reactions* (per reaction). The transcription target is **two tables**, not one |
| a species has a window | **a species has a set of rows**, each row one P×T box — a common silicate end-member carries a double-figure `N` spread over several rows in A4. *The values are not transcribed here: that is check ⑦'s own item* |

**Where the material lives, since no value may be printed until it is transcribed.** 2022
(`2022GeoJI.228.1119S.pdf`): **Table A4** *«Summary of phase equilibria data: stability»*, printed pages
1145–1146, columns *Species · N · P_min (GPa) · P_max (GPa) · T_min (K) · T_max (K) · Ref.*; **Table A5**
*«Summary of phase equilibrium data: reactions»*, printed page 1146. 2024 (`2024GeoJI.237.1699S.pdf`):
**Table C4**, printed pages 1731–1732, and **Table C5** *reactions*, printed page 1733. Until the
transcription exists with its own hash, **the only sentence this material may print about coverage is
«coverage not transcribed yet».**

⚠ **So the transcription item had a decision inside it, and it is now taken.** **J: a species' coverage
is the union over P×T boxes — a body's (P, T) is covered only if it lies inside at least one table row's
box, and separate unions of the P intervals and the T intervals are forbidden** (directing seat,
2026-09-11). ⚠ **The reason is the audit seat's counter-example**: 9 GPa · 1200 K can sit inside the
union of a species' P intervals **and** inside its T envelope while sitting inside **no row** — the two
axes are folded independently, so the pair is never checked against any single measurement. Under the
box rule that body gets the **«outside the data coverage»** refusal instead. *The refusal is the point —
an axis-wise union and an envelope are both shapes that hide the question.*

⚠ **And the stability table's own title is the sentence this material must print.** A4's is *"Summary
of phase equilibria data"* — *A5's prints the singular, "Summary of phase equilibrium data", and 2024's
C5 is back to the plural* — **the P–T coverage of the experiments the parameters were fitted against**, not a
declared range of validity. So the refusal is «outside the data coverage», never «outside the valid
range». *Those read differently to the next person, and only one of them is what the paper says.*

⚠ **And the reactions table carried a second decision of the same kind, also now taken.** Its rows are
**reactions**, not species — **A5 in the 2022 paper, C5 in the 2024 one; never C4, which is the
stability table**. *No reaction row is transcribed here either.* **K: a reaction row's box goes to every
species in the reaction**, products and reactants alike, and each such box carries a
**`reaction-row attribution`** label so a coverage claim can always be traced back to whether it came
from a stability row or a reaction row (directing seat, 2026-09-11).

**So the transcription item is not «copy two tables».** It is **two tables and two rules** — the P×T box
union within a species (J), attribution to all participants across the reactions table (K) — and both
are decisions the transcription must carry, not conventions it may assume.

⚠ **A caveat sits on decision C, and its source is held.** *An earlier version of this material had to
say «reported, source not held»: the two sentences C and Q7 rest on existed in two of our own documents
and nowhere else — not in `SLB_2022.py`, not in `P30-data/`, not in our repository.* The parallel seat
fetched both READMEs on 2026-09-11 and they sit beside the other `P30-data/` files:
`HeFESTo_parameters_010121-README.md` (sha256 `c645fbf93a5b1ba3`, 1471 B) and
`HeFESTo_Parameters_010123-README.md` (`6eb0d60dee14215f`, 1188 B). Read in the held file, verbatim:

> *"Parameter files of the following species have not yet been discussed in the published literature and
> are not recommended as they are still being optimized: crst, enm, fapv, fea, fee, feg, flpv, hem,
> hepv, hlpv, hmag, hppv, lppv, mag, mgl, sil, wuls"*

⚠ **Counted rather than assumed: `SLB_2022.py` ships eleven of those seventeen** — `crst`, `fapv`,
`flpv`, `hem`, `hepv`, `hlpv`, `hmag`, `hppv`, `lppv`, `mag`, `wuls` — eleven of its **77** top-level
classes, measured against the held file; the audit seat's count and this seat's agree. ⚠ *«77» is
`^class` lines*, which decompose as **62 `Mineral` + 15 `Solution`* — worth writing because the same
number counted as «species» would be 62. *The four low-spin end-members are a subset, not the story*:
the other seven are cristobalite, three Fe-perovskites and three iron oxides, and **spin has nothing to
do with them**. An earlier version of this material called this «a caveat on the spin decision», which
was the smaller half of it.

⚠ **The list is in the 010121 README only** — the 010123 (2024) one does not carry that paragraph at
all. *Decision (b) chose the 2022 base, so the caveat applies at full strength to exactly the set this
item will use*; had (b) gone the other way the sentence would not exist, which is worth knowing before
anyone revisits (b). ⚠ *And that is not «2024 is cleaner»*: `SLB_2024.py` ships **twelve** of the
seventeen out of its 92 top-level classes (**74 `Mineral` + 15 `Solution` + 2 `RelaxedSolution` + 1
`SLB3` helper**, so 91 are species and one is not) — dropping **both** `crst` and `flpv` and adding
`fea`, `fee`, `feg` (11 − 2 + 3 = 12; `flpv` does not appear anywhere in that file, grep 0) — with **no
README paragraph saying anything about them** — so the right label for the 2024 set is **«unknown»**,
not «recommended». ⚠ *The two files do not share one decomposition*: 2022 has no `RelaxedSolution` and
no SLB3-derived class at all, so reading the 2022 count through the 2024 breakdown is wrong.

#### Owner decisions this item needs

⚠ **A–I carry candidates and nothing is chosen. J and K carry a directing-seat default for owner
review**, and the rejected alternative is written beside each so the choice stays visible.

| # | decision | candidates |
|---|---|---|
| A | a rocky body **without** `mantle_chemistry` | refuse by name · fall back to today's `silicate` fit with the label «fit, no chemistry declared» · a `Declared-optional` default chemistry (Earth's) carrying the transfer label |
| B | the chemistry keys | `mg_si` + `fe_number` (+ optional `al_si`, `ca_si`, `na_si`) · `feo_wt` instead of `fe_number` · a full oxide wt % vector. ⚠ *P30 §8 narrows this*: the 2022 base is six oxides (SiO₂ MgO FeO CaO Al₂O₃ Na₂O), so `fe_number` addresses it; the 2024 set is the one that adds **Fe₂O₃ (ferric iron, with spin states), Cr₂O₃ and native-iron phases**, and a single `fe_number` cannot address its Fe³⁺/Fe²⁺ split — (b) chose 2022 |
| C *(re-framed 2026-09-11)* | **the eleven author-not-recommended species that `SLB_2022.py` ships** — `crst`, `fapv`, `flpv`, `hem`, `hepv`, `hlpv`, `hmag`, `hppv`, `lppv`, `mag`, `wuls` | **C1** include all of them, leaving the eleven open to `equilibrate` · **C2** exclude them by default under the label `author-not-recommended species excluded`, with a body's **declared mineral fractions** able to bring a named one in — this is P34's «declaration-only per body» and it is what owner clause (c) ③ already allows · **C3** exclude with no opt-in at all. **Directing-seat default: C2**, labelled a default pending owner ⑥-2. ⚠ *This was written as «spin transitions», and that framed four of the eleven*; the other seven are cristobalite, three Fe-perovskites and three iron oxides, and spin is irrelevant to them. Source held: `P30-data/HeFESTo_parameters_010121-README.md`, sha256 `c645fbf93a5b1ba3` |
| D | the composite averaging scheme | Voigt–Reuss–Hill · Reuss · Voigt |
| E | melting | stays a separate slot (today's Monteux/Deng/Fei chain) — S&LB 2022 has no melt phases; confirm rather than decide |
| F | the `NOTICE` sentence | a REBOUND-style row · a fuller GPL note · defer until P30 §6's questions are answered |
| G | the first target body | Earth as a contrast · Mars first |
| H | what happens to `silicate_chondritic` | keep it for crust and serpentinisation mixes · retire it once the chondritic chemistry is declared |
| I | the cost ceiling | one `equilibrate` per integration step · a per-body (P, T) grid cached **in memory for the run only**. ⚠ *I is now entangled with Q7 — see below* |
| **J** *(default set, owner review)* | how a species' coverage folds from its several stability rows (A4 in 2022, C4 in 2024) | **union over P×T boxes** — chosen: a body's (P, T) is covered only if it lies inside at least one row's box, and **separate unions of the P intervals and the T intervals are forbidden**. *Rejected: the min–max envelope, and equally the axis-wise union — 9 GPa · 1200 K can sit in a species' P-union and in its T envelope while sitting in no row, so both shapes report a fill where no measurement is.* Alternatives recorded, not chosen |
| **K** *(default set, owner review)* | how a reaction row's box is attributed (**A5** in 2022, **C5** in 2024 — never C4, which is stability) | **every species in the reaction** — chosen, with a `reaction-row attribution` label on each box so any coverage claim can be traced to a stability row or a reaction row. *Alternatives recorded: reactants only · no attribution at all* |

#### The licence row, and the question that is new

**The default the repo already has.** `NOTICE` carries a GPL-3.0 library used exactly this way —
*"REBOUND — GPL-3.0. Used as a library (not vendored) by the stability sandbox under
`phase3/stability-sim/`; simulations are run against an installed copy."* **That precedent is the
proposed default for BurnMan**: import-only, installed by the user, no BurnMan file in the repo or in a
release. *It is proposed because the repo already made this call once and nothing about BurnMan's shape
differs — not because the licence text settles it.*

⚠ **Q7 is new and it is not the same question.** P30 §6 asked six questions about GPL-2.0 and
import-only use. §8 added a seventh, and it comes from the **parameter repository's** README, not from
BurnMan's licence: *"We grant the right to download and use this data, but do not grant the right to
redistribute modified versions of the data in any form."* ⚠ **Held in both READMEs, verbatim** — the
same clause appears in 010121 and 010123, so it does not depend on which parameter set is chosen. Our
engine would redistribute nothing. But **a cached c_p/α grid derived from those parameters** — which is
exactly what owner decision **I**'s second candidate builds — is «modified data» or «output» depending
on a reading the README does not make.

⚠ *So I and Q7 cannot be answered separately.* Choosing the cached grid without answering Q7 would put
a derived artefact of a no-redistribution dataset inside the run, and the in-memory-only clause is the
reason the candidate was written that way in the first place. **Recorded as a pair, owner pending.**

#### What this item must not do

1. ⚠ **No hard-coded Earth assemblage**, not even as a default — (c) ② is explicit.
2. ⚠ **No module-global composition or cached mineralogy shared across bodies.** The material is built
   from the node contract, per call.
3. ⚠ **No value typed from S&LB 2022 or from BurnMan's files into our code.** BurnMan reads its own
   package. *The one exception under discussion is Table A4's coverage, and that is check ⑦'s own item
   with its own hash.*
4. ⚠ **No change to `ENVELOPE_Z_MATERIAL`, to the core materials, to melting, or to the C58 module
   constants.** The giant-planet Z proxy uses the silicate fit as a proxy, not as a mantle.
5. ⚠ **No tuning toward PREM.** Check ② reports a per-depth-bin contrast; it does not fit.
6. ⚠ **No install in the shared worktree before the licence row exists** (F), and now also before Q7 is
   answered if I chooses the cached grid.

#### An isodensity measurement cell (2026-09-14)

⚠ **정정됨 — superseded 2026-09-15, 아래 문단이 대신한다. 원문은 지우지 않고 남긴다.**

> ⚠ **Our three silicate phases carry no thermal set, and the isodensity curves show exactly that.**
> `mgsio3_en` · `mgsio3_prem` · `mgsio3_pv` all have `thermal=None`, and a curve of constant ρ through
> them is flat in temperature: at ρ = 6 g/cm³ our pressure is **192.774 GPa at 500 · 1000 · 1500 ·
> 2000 K alike — +0.000 %**. ⚠ **PALEOS's table over the same four temperatures is not flat** —
> 196.204 → 199.555 → 203.362 → **207.452 GPa**, **+5.733 %** from 500 K to 2000 K.
>
> ⚠ **The 0.000 % is not agreement; it is the absence of a temperature term.** *A reader who sees two
> curves and one of them straight will read «our silicate is temperature-insensitive», and the truth is
> that nothing in it was asked.* **That is the gap decision (c) above exists to close** — the
> assemblage path is what would give these three a thermal answer at all.

⚠ **The thermal term is there; what was missing is a declared potential temperature.** All three
phases carry `alpha_k` = **6.92e6 Pa/K** (Anderson & Goto 1989 in the form Seager+ 2007 §IV.2.2 uses),
`t_ref` = **1600 K** and ⚠ **`t_ref_kind = "adiabat"`**, so `delta_t` is `t · (1 − t_ref / t_pot)` and
returns **0 whenever `t_pot` is not declared** — and 0 again when `t_pot` equals `t_ref`. **The probe
passed `t_pot = 0`.** The flat column was the argument, not the physics.

Re-measured with `t_pot` printed beside every figure (script `e3f0169b`, CSV `e50b6571`, isodensity
pressure spread 500 → 2000 K at ρ = 6 g/cm³): **`t_pot` 1600 → +0.000 % · 2000 → +1.073 % · 2500 →
+1.926 %**. ⚠ **PALEOS's +5.733 % stands unchanged** — ours moves, and at the hottest declaration it
still moves less than a third as far. ⚠ **PALEOS has no `t_pot` axis at all**, so that column is one
**we** fill, and the CSV's ruler cell now says so on every row.

⚠ **The 1600 column reproduces the earlier CSV exactly** — 74.249 · 192.774 · 361.927 GPa at ρ 5 · 6 ·
7 — so the old table is not wrong, it is **a table that did not print its ruler**. *That is the
difference this correction is about, and it is why the superseded text is kept rather than deleted.*

The numbers come from the isodensity script `66eb7fd8` and CSV `git af04bd2c` (111 lines), with all
four controls passing — the band edges 342.1843 · 353.8167 GPa, 104 data rows split 40 ice + 32 iron
+ 32 silicate, and our own 52 rows split 25 pressures + 6 `swallowed_by_join` + 21 `not_reached`.
⚠ **`residual_not_a_join` = 0**, and that zero is the record that the filter ran — *without it,
«nothing was filtered» and «nothing was looked at» print the same.*

⚠ **Five defects in that script family were named by reading, before any run** — an argument taken by
index, a neighbour-row check that lived only in a comment, a control that printed without judging,
typed lane constants, and a three-cause `None` wearing two labels. **None of them reached this cell.**

#### Status

Open. ⚠ **A number, not a registered item** — the condition for becoming one is P34's: the owner answers
A–I or marks them deferred. *Two of the nine now carry printed caveats that did not exist when P34 was
written (C's «not recommended» list, I's entanglement with Q7), which is the reason to re-present them
rather than to carry the old table forward.*


## What closing all of these does not do

It does not make the solver answer every body. Brown dwarfs and stars stay out by the line
above, and each material ceiling stays where its evidence stops. What it does is make every
remaining refusal **one this recipe chose**, with a named mechanism and a citation, rather
than one it fell into.

That is the standard the rest of the engine is held to, and it is what "finished" means
here.

## Papers a document calls unreadable while the cache holds them

`python3 scripts/refs/check_paper_held.py --contradictions docs/reference/*.md engine/*.md` lists
every place where a bibcode the cache HOLDS sits within three lines of a sentence saying it cannot be
read. **This class is worse than a wrong number**: a wrong number eventually fails a reproduction,
while "we do not have it" makes sure nobody looks again. Two batches of papers arrived on 2026-09-05
and both left such sentences behind, so the check is a tool's job now rather than a habit's.

Four were repaired the same day — the two Summers papers and Mauk & Fox in the magnetosphere document
(all three resolvable only through their cache sidecars), and Bethkenhagen+ 2013 in the
ammonia-methane note, which the ledger in this file had already recorded as held and baked.
**The count is the argument for the tool**: two people looked for this class by hand — one by grep,
one by close reading — and each found four. The tool found nineteen on its first run. **Why the two
people found the same four is now known**, and it is not carelessness: four bibcodes contain an `&`,
and the cache stores them with the `&` written as `_` (`2001E_PSL.185...49A.pdf`). A person searching
the cache for the bibcode they are reading cannot match those files — not "might miss", *cannot*. The
Allègre & Manhès line was one of them, and it sat on a want-list telling the owner to go find a paper
already on disk. That is the class only a tool reaches, and it is the argument for having built it. **All 17 were read on
2026-09-05** (14 distinct places; three lines are reported twice). They are not "false positives":
the checker matches by proximity, and whether a sentence three lines away is about *this* paper is a
judgement it cannot make. That is the limit of the check, not a bug in it. ⚠ **Do not widen the window to fix them** — a
wider window means more to dismiss, more dismissing means the check gets ignored, and an ignored
check is no check. (Same reason the citation checker's total-count reconciliation was dropped.)

The verdict is recorded per place so that nobody adjudicates the same line twice. **Four were real
and are corrected; ten stand as written.** The test applied: does the sentence claim *we* cannot read
the paper, or does it describe the paper's publication status — and is the word even about this
bibcode?

| place | bibcode | verdict |
|---|---|---|
| `SESSION-HANDOFF` "Still not held" list | `2001E&PSL.185...49A` Allègre & Manhès | **corrected** — held; cached under the `&`→`_` name, which is why a hand grep missed it |
| same list | `2013GGG....14.4608D` Davies | **corrected** — held since 09-04 |
| `SESSION-HANDOFF` Tier 1 want-list | `2011Icar..213...12D` Driscoll & Olson | **corrected** — the paywall is the publisher's; the PDF landed 09-04 09:17 |
| `SESSION-HANDOFF` Tier 2 want-list | `2009Natur.457..167C` Christensen+ | **corrected** — "not held" was true when the tier list was written and stopped being true the same morning |
| `ice-stability` citations | `2009P&SS...57.2053F` Fray & Schmitt | stands — the same sentence says *paywalled … obtained through the owner's institutional access* |
| `interior-structure` citations | `2019Natur.569..251M` Millot+ | stands — "no preprint" is about arXiv, not about us |
| `interior-core` ammonia route table | `2017ApJ...848...67B` Bethkenhagen+ | stands — a different defect, recorded just below: the grid was never published, so "not obtainable" should read "not published" |
| `SESSION-HANDOFF` obtained list | `2008RvGeo..46.2007K` Korenaga | stands — marked **obtained**; the paywall two lines down is Jaupart+ 2007 |
| same | `2017GGG....18.3530R` Ruedas | stands — marked **obtained**; the paywall is Karato & Wu |
| `SESSION-HANDOFF` not-held list | `2020ApJ...903L..37N` Nimmo & Primack | stands — the line says *held and consumed* |
| `SESSION-HANDOFF` conductivity note | `2012E&PSL.349..109O` Ohta | stands — *the only … conductivity we hold*; "unobtained" is Fei+ 2000 in the next bullet |
| `silicate-melt-checklist` | `2011E&PSL.304..251A` Andrault+ | stands — "still unobtained" is Herzberg & Zhang 1996, the neighbouring paper |
| `silicate-melt-context-notes` | `2011E&PSL.304..251A` Andrault+ | stands — same sentence, same neighbour; it says Andrault is **held since 2026-09-05** |
| `surveys-2026-08-31` | `2021NatPh..17.1233P` Prakapenka+ | stands — *Obtained the same day*, with the cache path and the repository it came from |

**The count will not reach zero, and should not be read as if it could.** Most of the ten that stand
say "paywalled" or "unobtained" *and* resolve it in the same breath, which is the right thing for
those sentences to say — a paper's publication status is worth recording beside the fact that we got
it anyway. The four corrections were annotated in place with the date rather than rewritten, because
the sentences were true when written; what they lacked was a second visit.

One is a defect of a different kind. Bethkenhagen+ **2017** (`2017ApJ...848...67B`) is open access
and its full text is in the cache; what blocks C22 is not access but that **the grid values were
never published** — no data-availability statement, no URL. That line should say "not published"
rather than "not obtainable": buying or requesting it changes nothing, and only an author enquiry
would, which is the owner's call.

## Related

- [`interior-structure-methodology.md`](../docs/reference/interior-structure-methodology.md)
  — the domain table these entries index
- `engine/*-context-notes.md` — the reasoning behind each closed item
- `engine/coverage-review.md` — a 2026-08-27 snapshot, superseded by this file

**Brief 155, 2026-09-08 — what the repair turned out to be, and what it did not touch.** The reading above
held on the paper: `BRACKET_K` was the inversion's bisection bracket, not eqs 34–36's domain, and the
paper prints no lower usage limit. What it *does* print is an upper one — its own initial condition
`2004GeoJI.156..363N.txt@«conditions are that T c = T m = 4800 K»` with the §6 caveat
`2004GeoJI.156..363N.txt@«is due to the short mantle time constant at high temperatures»`. So the item is
renamed: **an undeclared domain had a bisection bracket standing in for it.** `mantle_flux.EQ35_DOMAIN`
now declares 4800 K above and open below (owner: only the printed edge travels; T₀ = 1573 K is an expansion
point, 1603 K a present-day value, neither a limit), `implied_flux` keeps it as the callee, and
`core_history.rates` stops by name when refused. eqs 37–39 got their **first** domain the same way
(`cmb_flux.EQ39_DOMAIN`, D5). Below an expansion point a call is allowed and **noted** as declared
extrapolation; the count rides on every `core_history` result. Two observations that note made visible:
Brief 57's radiogenic-floor band (1000–1500 K) has always run below eq. 35's expansion point, and **Mars's
deep mantle sits below eq. 39's** (T̃_m ≈ 1910 K puts T_a under 3400 K at any T_c below 4890 K). Earth's
anchors are unchanged (T_c(0) 4027 K, 1135 steps). **Not touched here:** the Mars step sweep (h against the
mantle time constant, `engine/tools/mars_step_sweep.py`) — it is the next brief, and it decides whether the
divergence is the step or the state.

**Briefs 156–157, 2026-09-08 — the second half, the step, and the item closes.** The pre-registered sweep
(`engine/tools/mars_step_sweep.py`, five fixed steps) gave: 4 · 2 · 1 Myr **diverge** (T_m −6244, −1111,
−1115 K), 0.5 and 0.25 Myr agree to 1.3 K (T_p 1383.02 / 1382.90, T_c 3894.34 / 3893.07, T_p at 3.7 Ga
1668.97 / 1669.12). Verdict by the registered sentence: *발산 (3 of 5 steps)*; the unregistered shape —
diverging steps mixed with surviving steps that converge on each other — is registered now as **E**. Three
records that the sweep forced straight: (i) *yesterday's "plausible Mars values"* (T_p 1351.8 … 1373.2 K)
were integrations from **initial temperatures 2000–4000 K**, not from the transferred 4800 K; at 4800 K the
4 Myr step diverged yesterday too, and the value is bit-identical at e8715934 (−6243.664 K), so Brief 155
changed nothing on this path. (ii) *"τ ≈ 0.717 Myr, Earth 36.3"* in the sweep's own comment had no
derivation anywhere in the repo — 0.717 Myr is the ²⁶Al half-life (this document, C21) — and the directing
seat relayed it into Briefs 156 and 157 as "h/τ Earth 0.1 · Mars 5.6". Withdrawn. The derived time constant
is τ = C_eff / (dQ_m/dT_m) (`engine/tools/adaptive-step-prereg.md`): **Earth's first fixed step was h/τ =
1.02, Mars's 75** — Earth survived at the stability edge. (iii) The rule is now the step itself:
`core_history.integrate` takes `h = min(4 Myr, 0.1·τ)` recomputed every step (F = 0.1: 1/28 of RK4's
real-axis limit, 1/10 of what Earth already passed). Mars integrates in 1197 steps (smallest h 0.0053 Myr,
largest h/τ 0.100) to **1382.90 / 3893.01 / 1669.22 K** (at H 1.5 pW/kg) — within 0.00 / 0.06 / 0.10 K of the 0.25 Myr sweep,
inside the pre-registered 5 K. Earth: 1152 steps (was 1135), T_p 1525.46 and T_c 4027.43 unchanged at two
decimals, T_p at 3.7 Ga +0.05 K; the step count is the one anchor that moved and `test_core_history` records
both the new count and the fixed-step reproduction. **What the closed item leaves for C47:** a converged
Mars history from the transferred 4800 K start — present T_p 1383 K against the declared 1600 K, 3.7 Ga T_p
1669 K — consistent with an Earth-calibrated model, not Mars's actual values.

**Brief 166 D, 2026-09-09 — one nominal constant moved another node's reproduction anchors, and the repair is
to name the condition.** Owner decision ⑤ lowered the declared core heating from **1.5 to 0.14 pW/kg**
(`engine/core_energy.py@«상한은 오너 결정 ⑤ (Watanabe 2014, 논문 자신의 환산)»`). That is a C14/C15 declaration; it was not
a C20 change, and nobody predicted it would touch C20. **gate200 failed on two C48 anchors**, both in
`test_core_history.py`: Earth's fixed-step `T_p` came out **1517.62 K against the anchor 1525.46**, and the
Mars pair came out **1377.23 · 3768.09 · 1668.05 against 1382.90 · 3893.01 · 1669.22**. Nothing was wrong with
the integrator — **the anchors had been reading the module constant** through `params["h_core"]`, so a
declaration in one node re-defined the condition another node's recorded numbers were measured under.

**The repair, and what it deliberately is not.** Each reproduction anchor now names its own H, the way
`test_core_energy.H4` already named Nimmo's Table 4 condition: `H_NIMMO = 1.5e-12` is passed as an argument
and the C48 numbers reproduce **exactly** (Earth 1135 steps, `T_p` 1525.46, `T_c` 4027.43; Mars 1197 steps,
1382.90 / 3893.01 / 1669.22). The declared H gets **gate rows of its own**, measured 2026-09-09 and pinned as
anchors in turn: Earth 1135 steps `T_p` **1517.62** `T_c` **3915.75** (adaptive minus fixed **+0.0004 K**), Mars
1197 steps **1377.23 / 3768.09 / 1668.05**. ⚠ **This does not decouple anything.** C14, C15 and C20 still share
one constant; what changed is that the sharing is now written where the numbers are, and a future move of the
nominal will fail the gate on the *declared* rows — which is the correct place to fail — instead of on the
reproduction ones.

⚠ **A second breakage was found by the repair, in a tool the gate never runs.** `tools/mars_step_sweep.py`
proves itself live before printing anything — it re-runs Earth and checks the anchor 1525.46 K
(`engine/test_interior.py@«늘 발화하면 상수다»`). It built its `params` from `ce.H_CORE` too, so after decision ⑤
that proof would have **failed on its own anchor** the next time anyone ran the sweep, and nothing in the gate
would have said so beforehand. It now names `H_NIMMO` and the proof reproduces 1525.46 K again. **This is the
argument against moving the declared-H rows out of the gate**: what a lane does not recompute, nobody re-measures.

⚠ **A third breakage in the same tool, found 2026-09-20 by the work seat and confirmed independently by the
audit seat.** `mars_step_sweep.py` carried Mars's core mass fraction as a literal in its own module-level
dict — a copy of a declaration `bodies/mars.yaml` stopped making when C57 (c) removed the key. Nothing
compares a copy with the tree it was copied from, so the sweep kept printing Mars rows from a number with no
origin, and the tool's own `cmf is None` stop could never fire because the copy always supplied one.
⚠ **Deleting the copy alone is worse, and that was measured rather than argued**: with no fraction and no
radius in the call, `interior.solve` does not invert. It looks the composition name up and falls back to the
`earth_like` preset while the rows still say Mars. The inversion is a different function, `infer_composition`,
which needs mass *and* radius — and the tool's dict already held the radius; the call simply never passed it.
**What was missing was not in the file, it was in the call.** The fraction now comes from three branches —
declaration, inversion, then a stop that names the body and both places looked at — and Earth still takes the
first branch from its own declared value, so one run exercises both. The inversion returns
**0.23958333333333331**, reproduced bit-identically by the audit seat from `infer_composition` directly.

⚠ **Two quantities had been conflated, and separating them is the repair.** `composition` is the engine's
material vocabulary and accepts five names; the inversion's own label is not one of them, and passing it — or
`None` — is refused before integration, with the refusal carrying no values, so the next line died on a
missing key rather than on the refusal. The tool now passes the vocabulary name, prints the *source* of the
number as a label beside the solved regime, and stops on the refusal by name. ⚠ **A first attempt at an
acceptance test here was inverted**: recovering the fraction from the two masses and comparing it with the
literal passes two wrong values and fails the true one. ⚠ **The stated mechanism was wrong once, and the
correction is the point**: the two masses sum exactly, so the subtraction's error cancels; the residual comes
from multiplying and dividing back, and no algebra removes it. That is recorded where the line lives, in the tool's own comment, with the three numbers that show
it — **not repeated here, so that one place stays canonical.** The check line prints the difference instead of
judging it.

⚠ **Two cost figures, and one of them was wrong for a reason worth keeping.** The inversion takes about two
minutes per call on an idle machine (121.41 s for the inversion and 127.99 s for the whole of
`build` on one run, 132 s for `build` on a second, each with the machine's process count recorded from inside
the measurement); a figure of about 20 seconds had been carried into this
work and is withdrawn — it was a binary-system measurement applied to a quaternary one, not an unsupported
number. ⚠ An earlier explanation that the slow timing came from contention is also withdrawn: the busy-machine
figure and the idle one differ by 1.1 s. **The tool is not a gate step**, so none of this appears in the
gate's timings, and a reader who wants the cost has to run it — two minutes, once, per call.

**The integrator's own reference row moves with it, and it is not the row C15 reads.** At the declared H the
Earth history ends at `T_c` **3915.75 K** (inside C14's 3750–4284 K band), inner-core branch **`never`**,
−d`T_c`/d`t` **58 K/Gyr**, and the four-corner ΔE_min band **−205.7 … −2.9 MW/K, 0 of 4 corners positive →
`fails`**. ⚠ **That is the C20 reference row, and it is a different row from C25 (f)'s declared 3 760 K horn,
which has an inner core and a band that straddles zero.** The two are not in conflict and neither supersedes
the other: one integrates from a 4800 K start to whatever `T_c` it reaches, the other is evaluated at the
owner's declared `T_c`.

**Criterion B, re-read at the declared H — recorded, verdict unchanged.** Mars's 3.7 Ga checkpoint reads
**1668.05 K**, still inside the owner's Herzberg+ 2007 `[1553.15, 1673.15]` K line, with **5.1 K** of upper-end
headroom (it was 4.0–4.7 K at H 1.5, so the margin grew). ⚠ **The row-selection rule is part of the number**:
`min(rows, key=|t_gyr + 3.7|)` — the nearest **sampled** row, no interpolation. Here that row is unique
(t = −3.700566 Gyr, |Δ| 0.000566 Gyr against the next row's 0.003434) and its value is **1668.0452 K**. The audit
seat's independent run reported 1668.043744 from a row at −3.700558 Gyr; the trajectories agree to the printed
digit, so the 0.0014 K is the two seats' *row grids*, not the physics. ⚠ **And neither number is worth its last
digits**: the local step is ~4 Myr, so "nearest row" is itself ±2 Myr, worth **≈0.19 K** here — three orders of
magnitude more than the disagreement. One rule, one number: **1668.05**.

**The cost, measured, and one claim withdrawn.** The gate grows by **+114 s** (`test_core_history` 235 → 360 s)
for the two added integrations. ⚠ *An earlier audit measurement put the declared-H Mars run at **843 s**, a
15.6× per-step blow-up, and the directing seat had provisionally moved the declared rows to an on-demand lane
because of it.* **It did not reproduce** — three sequential runs on this tree took **59.6 / 58.9 / 59.9 s**, the
audit seat's re-measurement took **57.9 / 57.7 / 58.7 s**, and the proposed cause (an inner core nucleating at
the colder declared `T_c` and making every step search for it) is **false**: the declared-H Mars branch is
`never`, present `r_i` **0.0 km**. Since the two runs agree to the printed digit they execute the same path, and
the same path cannot cost 15×. The 843 s was environment. The rows stay in the gate, because an on-demand lane
would have created exactly one more *"number the gate does not recompute"* — the kind of gap that produced this
brief.

**What this brief names and does not fix — C52 candidate.** `_core_side` was reading `ce.H_CORE` directly and
throwing the result away (`core_terms`' `h` feeds only `Q_R`, and `Q̃` is `Q_s + Q_L + Q_g`); it is now passed
`h = 0.0` with the reason written down, so the one path that reaches an answer is `params["h_core"]`. That is a
tidy-up, not the finding. **The finding is that nobody has counted which shared constants hold up which nodes'
anchors.** C45 checks that a node's lookups are declared; C50 checks that a declared `Needs` is supplied;
**neither of them can see that `core_energy.H_CORE` is load-bearing for `test_core_history`, `mars_step_sweep`
and `mars.yaml`'s stage-0 verdict at once.** The detection is countable — for each module constant, which
recorded anchors change when it changes — and it is **not built here**. ⚠ *And it was a gate, not a checker,
that found this one, which is the same lesson as C45: the hole was never silent, it was simply never counted.*

**Brief 166 E, 2026-09-09 — the declared `H` was our arithmetic, not the paper's, and the anchors 166 D had
just pinned moved again.** Decision ⑤ was *"the cap is Watanabe+ 2014's under-40 ppm"*, and that decision
stands. What was wrong is how we turned ppm into W/kg: we used a **textbook** specific power for natural
potassium, ≈3.5 × 10⁻⁹ W/kg, and got 0.14 pW/kg. **The paper prints its own answer** — *"less than 0.17 TW"*
— and its own constants (⁴⁰K 1.917 × 10⁻⁵ W/kg, ⁴⁰K/K 1.17 × 10⁻⁴) imply **2.243 × 10⁻⁹**, so our constant
was **56 % high**. Three routes from the paper's own numbers agree:

| route | arithmetic | pW/kg |
|---|---|---|
| its printed power ÷ its own core mass | 0.17 × 10¹² W ÷ 1.932 × 10²⁴ kg | **0.0880** |
| its own constants, from 39 ppm | 39 × 10⁻⁶ × 1.917 × 10⁻⁵ × 1.17 × 10⁻⁴ | **0.0875** |
| its printed power ÷ **our** core mass (0.325 M⊕) | 0.17 × 10¹² ÷ 1.9409 × 10²⁴ | **0.0876** |

`H_CORE` and the upper end of `H_CORE_RANGE` are now **0.088e-12 W/kg**. Recorded and not adopted:
Gessmann & Wood's 250 ppm on the same textbook constant is **0.86 pW/kg**, which is where our old ceiling
came from being read as generous.

**What moved, measured — and the shape of the answer did not.** The two H-conditioned anchor sets behaved
exactly as 166 D's repair intended: **the Nimmo-condition rows did not move at all** (Earth 1135 steps
1525.46 / 4027.43; Mars 1197 steps 1382.90 / 3893.01 / 1669.22), and only the declared rows did.

| declared-`H` row | at 0.14 (166 D) | at 0.088 (166 E) | Δ |
|---|---|---|---|
| Earth fixed 4 Myr `T_p` / `T_c` | 1517.62 / 3915.75 | **1517.34 / 3911.29** | −0.28 / −4.46 |
| Earth adaptive (1152 steps) `T_p` / `T_c` | 1517.62 / 3915.75 | **1517.34 / 3911.29** | same, adaptive − fixed +0.0004 K |
| Earth ΔE_min band, 3.1 Gyr, 4 corners | −205.7 … −2.9, 0/4, `fails` | **−203.4 … −4.1, 0/4, `fails`** | verdict unchanged |
| Mars adaptive (1197 steps) `T_p` / `T_c` / 3.7 Ga | 1377.23 / 3768.09 / 1668.05 | **1377.03 / 3763.10 / 1668.00** | −0.20 / −4.99 / −0.05 |
| C15's declared-horn `ΔE` and band | +30.1, −76.3 … +191.9, 4/8 | **+26.5, −76.3 … +188.3, 4/8** | ceiling −3.6; **floor unmoved** |

⚠ **Criterion B still passes and by slightly more**: Mars's 3.7 Ga checkpoint is **1668.00 K** inside
Herzberg+ 2007's `[1553.15, 1673.15]`, headroom **5.15 K** (5.1 at 0.14, 4.0–4.7 at Nimmo's `H`).
⚠ **Criterion A's 1400–1800 K sweep has still not been re-run at the declared `H`**, and `mars.yaml` says so.

⚠ **The band's floor cannot be moved by any potassium decision**, which this correction is the second
measurement of: −76.3 MW/K is the `H` = 0 corner. **Every version of decision ⑤ moves the ceiling only.**

**The citation rule caught its own first increase, and was returned below its baseline.** `check_citations`
read **29 · 138** against the baseline 28 · 128 — the drift was one new section, C25 (f), written by 166 B/C
with ten author-plus-year mentions and no bibcode. Bibcodes were attached there and in two more sections
(C25 (b) 5, C34 re-drawn 2), landing at **26 · 121**. The baseline is updated **with the reason beside it**
rather than absorbed; `check_citations.py`'s docstring now carries which three sections were repaired and
why C33 (b)'s four are deliberately left (three of them are the regex's own worked examples, so the rule's
`FAIL` threshold is that section's count and not zero). **The other 25 flagged sections are the backlog the
rule exists to surface** and were not touched.

⚠ **Eleven days later the same line had become decoration, and the count had moved twice more**
(2026-09-20, work seat; audit seat reproduced every figure independently). Sixty gate logs carry the
record line and **not one of them prints 26 · 121** — the oldest already reads 36 · 161, so the first
ten steps of the drift happened before the log series and cannot be placed from it. Ordering those
logs by their `GATE START` commit dates rather than by file time gives the same two boundaries, each
**+1 section and +1 citation**: 2026-09-11, then 2026-09-16, then today's 38 · 163. That shape is
ordinary ledger writing rather than a regression, which is exactly why a standing ⚠ on every plate
taught no one anything.
⚠ **The warning was removed and the difference put in its place** — the line now reads the counts,
the baseline, the commit and date the baseline was taken, and the signed deltas since. It is still
not a verdict and the literal is still one pair; today's figures are computed at print time and
stored nowhere, so no second place can go stale. ⚠ **The docstring rule that a baseline is not
updated without a written reason is untouched**: this changed what is printed, not whether the
number may move. ⚠ *A pointer at the end of the old line, saying where the rule text lives, went
with the old wording. It is recorded rather than restored, because the printed string is itself the
registered acceptance for this change; whether to bring it back is for the next registration.*
⚠ **One figure in the pre-registration was wrong and is corrected here**: the baseline entered at
`e5f2f83d`, not at the commit that wrote the counter — and 26 · 121 is the **second** baseline, taken
after bibcodes pulled 28 · 128 down, not the first count of anything.

**Two source corrections, from the originals rather than from either summary.** The dipolar/multipolar
transition sentence this file quoted as Christensen & Aubert 2006's is **Olson & Christensen 2006's**; C&A
2006 is the primary source because it *defines* the quantity (its eq. 28, `Ro_ℓ = Ro · ℓ̄_u / π`, which it
calls the **modified** Rossby number, renamed **local** by OC06's eq. 15 *"as in CA [32]"*). ⚠ And the
**0.09 our text carried as "Earth"** is, in C&A 2006, that paper's single non-dipolar **outlier**, a model
case whose regime depended on its starting field — Earth's 0.09 is OC06's Table 3. Also recorded, not
repaired: `engine/bands.py@«the multipolar grid {0.05, 0.10}, both printed by OC06»` may be pairing two
numbers that paper prints about different quantities. Full reading in C25 (f)'s regime-gate subsection.

⚠ **The contract check earned its keep inside this brief.** Adding the sensitivity note to
`engine/bodies/earth.yaml` **deleted the `core_cmb_temperature: 3760.0` line it was written above** — an
edit that left the file valid YAML and passed `yaml.safe_load`. `check_contracts` failed four nodes at
once (`cmb_heat_flux`, `core_energy_balance`, `core_entropy_production`, `core_state`), each with *"every
lookup missed and that `None` is filed in the evidence under the same name"* — **C37's signature, class ①,
reported against the key that had just vanished.** Restored in the same pass. **This is the failure mode
C45 (b) was built for**, and the first time it caught a live deletion rather than a historical one.

**What this brief did not do.** It did not re-run criterion A, it did not touch the 25 older sections the
citation rule flags, and it did not resolve the `bands.py` pair. ⚠ *And it is the second time in one day
that a constant declared for C14/C15 moved C20's recorded anchors* — which is the C52 candidate named at
the end of 166 D, now with two instances instead of one. **The count still does not exist.**
