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

This file is 2 700 lines. The table is here so that "what is open right now" does not require reading
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
| **C14** | `internal_heat_nontidal → dynamo_rocky via geotherm` | **open** (`status: gap`) | needs thermal evolution, not decay history alone; C20's integrator is the supplier to wire |
| **C15** | `heat_transport_mode → dynamo_rocky via cmb_heat_flux` | **open** (`status: gap`) | the supplier exists (Brief 60); what is missing is the consumer wiring through φ and core entropy |
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
| **C47** | the transport table is fed radiogenic production, and its thresholds are defined on surface heat flow | **closed 2026-09-08 — named, not filled (C47 (k))**; earlier status kept: *measured 2026-09-07, not fixed* | Verdict: **a different quantity**, not an inaccurate one. The low feed reproduces radiogenic production on two bodies (Earth 1.07–1.33× of Korenaga 2008's 16–20 TW; Mars 1.11× of Parro+ 2017's 14.3 mW/m²) and misses surface heat flow by **body-dependent** factors (Earth 0.45×, Mars 0.84×). ⚠ **That factor is the Urey ratio** — 0.35 for Earth, 0.68–0.75 for Mars — so `1/Ur` would be 2.2–2.9 against 1.3–1.5 and **no correction constant can serve both.** The missing term is secular cooling, which our own §6 already names (*"radiogenic, accretional, primordial"*) and no node emits. ⚠ Consequence for C34: Mars passing and Earth failing at the low feed measured **how close each body's Urey ratio is to 1**, not whether the feed is right. ⚠ **Attempted 2026-09-07 (C47 (b)) and it does not close by code.** The quantity already exists — C20's `q_mantle_present` **is** `Q_M`, from Nimmo eqs 34–36, and it reads no measured flux — but one law cannot serve both bodies: at a common `T_m` Earth lands on 0.35 while Mars reads **0.209 against 0.68–0.75**, and `Ur` **falls** ×1.69 toward smaller bodies where the literature has it **rise** ×2.0. ⚠ **The ordering is wrong, so no `T_m` fixes it** — `implied_flux` is a mobile-lid law (our own docstring says it was tuned on four present-day Earth constraints) and Mars is the archetypal stagnant lid; it hands Mars 85.7 mW/m² against Reese's own 15–30 ceiling, **2.9–5.7× what C46's own bottom rung allows.** ⚠ Also blocked outright: only `earth.yaml` declares C20's two initial temperatures, so **C20 cannot run on Mars**. **The block is C46's circularity** (the flow needs the regime, the regime needs the flow) plus a paper we do not hold — Reese+ 1998's stagnant-lid scaling, abstract only |
| **C48** | the thermal-history integrator was validated on Earth alone, and calls its flux law far outside that law's expansion point | **closed 2026-09-08 in two halves — domain (Brief 155) and step (Briefs 156–157): the fixed 4 Myr step was h/τ ≈ 75 on Mars's first step and 1.02 on Earth's; the step is now h = min(4 Myr, 0.1·τ) and Mars integrates (1382.90 / 3893.01 / 1669.22 K, within 0.1 K of the 0.25 Myr sweep) while Earth's anchors hold to two decimals (1152 steps, was 1135) — ⚠ **every one of those numbers is at the
core heating H = 1.5 pW/kg, which was the nominal when they were measured; owner decision ⑤ (2026-09-09) declared
0.14 and moved them, so Brief 166 D pins each anchor to its condition instead of to the module constant.** Earlier text of this cell:** renamed and half-repaired 2026-09-08 (Brief 155): the inversion bracket had stood in for a domain nobody declared — eqs 34–36's domain is now declared from the paper (upper edge 4800 K, §3; «<8 per cent» caveat, §6; open below), eqs 37–39's for the first time (D5), and the callee keeps both. The Mars step sweep (h/τ) stays open as its own item** | C20 diverges on Mars at every pre-registered `T_pot` (`T_m` → −6244 … −8208 K). ⚠ **The divergence is not the finding** — the flux law is called at **719,546 mW/m² on Mars and 25,144 on Earth**, against measured 19 and 92.1, because Nimmo's eq. 35 is a linearisation about `T₀ = 1573 K` and C20 feeds it **+1467 K (Earth) and +2448 K (Mars)**, giving mantle viscosities of `η₀`÷2.35 M and ÷42.8 G. **Earth's own outputs come from the same out-of-range call and survive only on heat capacity.** ⚠ No published range was violated — **none is printed**; our `BRACKET_K` is a Brief 57 bisection aid. **Two values from one paper fail to compose on a second body**, which is the failure mode of this engine's Earth-number-on-every-body pattern. Blast radius counted: **one consuming edge** (`core_entropy_production`), no board row, no `db/`. Next: a usable flux law, or a grounded starting epoch — ⚠ **never a starting value chosen because it integrates**. ⚠ **The diagnosis above predates Briefs 155 and 157 and is superseded on the cause of the divergence** (kept, not deleted, as this cell's second column keeps its earlier text): the out-of-domain call is real and is still counted on every result, but Mars diverged because of the step — the fixed 4 Myr was h/τ ≈ 75 on the first step — and at h = min(4 Myr, 0.1·τ) Mars integrates |
| **C49** | one engine, two `k_core` declarations — and one file's stated ground forbids the number the other consumes | **listed 2026-09-09, not started** | Rocky: `cmb_flux.py@«K_CORE = 50.0»`, a single declared midpoint ± 20, consumed as the corners (30, 70) by `core_entropy.K_RANGE` and `core_history.K_CORNERS` and as the `q_ad` band. Sub-Neptune: `sub_neptune_dynamo.py@«CORE_CONDUCTIVITY = Band(»`, midpoint **None**, ends **40 and 100** from two papers Tang+ 2025 runs both ways, grade *calibrated*, with an unmade `Choice`. ⚠ **And the comment above it says «70 W/m/K 는 두 논문 중 어느 쪽도 말하지 않은 수다» — that very 70 is the upper corner the rocky path feeds to the entropy band.** So one file's stated ground disqualifies a number the other file uses. Two shapes as well as two values: one paper's ± against two papers' ends. Unification is part of owner decision ② (C25 (b)); listed only |
| **C50** | contracts list `Needs` that no roster body supplies — and four are C37's exact signature | **closed 2026-09-09 at (0, 0, 0) — one row still owner-pending behind the zero** | Measured by C45's new lookup check: **class ① (C37's signature — the lookup misses everywhere and the `None` is filed under that name) is live in 3 nodes / 4 keys** (`body_class` `gas_mass_fraction`·`semi_major_axis_au`, `dynamo_rocky` `dynamo_regime`, `interior_layers` `porosity_cap`), and **class ③ (a `Needs` no body supplies, the call site coping) in 8 nodes / 8 keys** (`core_material` ×4, `ice_mass_fraction` ×3, `differentiated`, `envelope_z`, `gas_mass_fraction`, `initial_porosity`, `tidal_heating`, `permanent_quadrupole`). Each is one of two faults — the contract is wrong, or the body declarations are missing — and which is not decidable from the count. Held at measured size meanwhile: the four are named in `engine/check_contracts.py@«이 집합 밖의 사례는 FAIL 이다»` and anything outside fails the gate; class ③ has a printed baseline. Repair can move values, so it is a later brief. No owner decision |
| **C51** | the engine has no mantle energy budget, so secular cooling is an input nobody supplies rather than an output | **pre-registered 2026-09-09, before the build** | The owner's third path (C25 (f)): build the missing term instead of picking numbers inside the entropy band. ⚠ **The flux law is not what is missing** — Foley 2018's eq. (3) is the Korenaga eq. 30 this engine already transcribed at `n = 1`. What is missing is the budget around it, eqs (1)(2)(4), whose `dT_p/dt` **is** secular cooling. Stage 1 is the present epoch only, with `dT_p/dt` as the unknown, so the gate cost is ~0. Three verdict cells and their failure sentences are fixed in the section below, before any of it exists; `L′` and `(m, p)` go in as bands because the source treats the first as an unknown and prints three disagreeing sets of the second. ⚠ **First anchor measured: one prefactor has five values across two papers (0.528 · 0.53 · 0.55 · 0.57 · 0.5) and Korenaga names the cause — his own definition of `T̄_i`** — which is also the only candidate explanation for the 3.65× absolute-flux gap. Owner decisions on `L′` and `(m, p)` come after commit D's numbers; C34's feed stays held |
| **C52** | how many recorded anchors rest on one shared module constant, and nobody counts | **named and counted 2026-09-09; no checker built** | C45 asks whether a node's lookups are declared, C50 whether a declared `Needs` is supplied; ⚠ **neither asks how many *other* nodes' recorded anchors move when one shared constant moves**, which is what fired twice this week as a gate failure. Instance 1 is `core_energy.H_CORE`, whose value re-defined C20's reproduction anchors from a C14/C15 declaration: six places were repaired in 166 D / 167 A and this item's closing sweep found the real count is **ten**, with three distinct defects left — a comment mirroring `H_CORE_RANGE` that had gone stale at `0.14e-12`, a context note naming 0.14 pW/kg as the declared value after 166 E replaced it with 0.088, and a pre-registration carrying 1525.46 K · 4027–4028 K · 1135 steps with **no condition named at all**. ⚠ **The disease changed shape**: in 166 D the numbers lacked labels, here the labels had gone stale, because the constant moved twice in one day. Instance 2 is `mantle_budget`'s four Earth defaults, where an AST count of 5 and a grep count of 3 were both right about different questions and the number of functions touching them at all is **6**. Closed at named, counted and labelled — **not fixed**: no checker exists, and instance 2 is untouched |
| **C53** | the tectonic regime is declared as a boolean, and no source surveyed uses one | **built 2026-09-09; two owner mappings still pending** | `stagnant_lid: true/false` is the *“bimodal distribution … that is typically assumed”* which **Foley & Bercovici 2014**'s abstract ([`2014GeoJI.199..580F`](https://ui.adsabs.harvard.edu/abs/2014GeoJI.199..580F)) names as its foil, and the parallel seat's P9 survey found **no scheme that is binary** (Mars and Mercury stagnant in all of them, Earth mobile *or* transitional depending on the scheme, Venus genuinely contested across five printed classifications). Registered replacement: a `tectonic_regime` enum {stagnant · mobile · transitional · episodic · heat_pipe · contested} carrying a grade and a source, with the old boolean kept as a **derived** value so that **no consumer moves**. ⚠ **The blast radius was counted before the design and it is one branch**: `dynamo_rocky`'s survival gate is the only place a value reaches an output (truthy → `DEAD_LID`, `dipole_moment` 0), `heat_transport_mode` does **not** read it — it reads the computed flux ladder — and `phase2/`, `phase4/`, `db/` and the SPEC have **zero hits**. Three owner decisions were taken before the build (`contested` → derived `True`; Earth = `mobile` with the grain-damage note; Pandora = `mobile`, owner-declared), and `episodic` · `heat_pipe` are **left unmapped by name** with their candidates recorded — owner-pending. The regression that proves nothing moved is the three roster bodies' derived booleans, bit for bit: Earth `False` · Mars `True` · Pandora `False`. ⚠ The declared-regime-versus-computed-ladder consistency check is **deliberately not built here** — its first report would be that Earth's declaration and Earth's ladder cell already disagree, which is its own item. ⚠ **Built and measured (C53 (b)): every emitted value bit-identical for all three bodies** (Earth `False` · Mars `True` · Pandora `False`, Pandora's 41.37252479971432 µT included), and the ordering rule fired as registered — `check_contracts` failed on the **evidence key** until `Result.inputs` carried `tectonic_regime` instead of the derived boolean. Two corrections to the pre-registration are recorded there: Pandora's old declaration *did* carry a reason, and Mars's `True` is not load-bearing because the core gate fires first |
| **C54** | `conductor_phase` stands in front of the lid axis, and Mars's is `undecided` | **candidate, listed 2026-09-09** | Opened by a measurement in C53 (b), not by a design opinion: the survival gate tests `conductor_phase` **before** the tectonic regime, and Mars's is `undecided`, so Mars answers `cannot-say (conductor_phase undecided)` and its declared `stagnant` never reaches `DEAD_LID`. ⚠ **Mars's dynamo output is identical whether its regime is `stagnant` or `contested`** — so *«Mars is a single-plate planet, therefore no dynamo»* is a sentence this engine does **not** execute, and the lid axis cannot be exercised on any roster body until the axis in front of it decides. What decides `conductor_phase` is `core_state`, which needs a **core-side** CMB temperature, and that is declared for Earth only (owner decision ①, C25) — which is why Mars is *undecided* rather than wrong. Candidate only: no owner decision is asked for here, and nothing beyond the one measurement C53 (b) recorded has been done. ⚠ **The root is now measured (172 (a)): `core_state.core_cmb_temperature` is supplied by Earth and undeclared on Mars and Pandora.** The core-side CMB temperature is what decides `conductor_phase`, it exists for Earth only (owner decision ①, C25), and that single asymmetry is why the axis in front of the lid never decides on Mars. Candidates for a declared Martian `T_c` are the parallel seat's |
| **C55** | the engine has two irons and Mars's core is between them | **stage 1 built 2026-09-10; the verdict cells are blocked on a melting gap** | Opened by C50 (b) row 5's owner-pending cell: Mars cannot declare a `core_material` because neither of our two irons covers it. The printed Martian core density is **5.7–6.65 g/cm³** (S 13–19 wt%), while `fe_prem` sits at 7.6–8.2 and `fe_eps` at 9.0–9.6 — ⚠ **the body is outside both, so declaring either would be asserting a density we know is wrong**, which is why the cell stayed empty rather than taking the default. The owner's decision is to **build a third material, Fe–S**. Source order for the equation of state, held first: Huang 2023 (AIMD) → Xu 2021 (liquid Fe–S mixing) → Morard 2018 → Nishida 2020 → Sanloup 2000; the melting bound stays Mori 2017 with its **declared 10–21 GPa gap**. No number is elected here and nothing is built **at listing time**. **The pre-registration is the section below** (drafted as P13, moved in 2026-09-10 with its anchors resolved). ⚠ **Since then, stage 1 is built**: Huang's printed mixing reproduces its own independent anchor to 0.07 % (178 B), a high-pressure-referenced BM2 gives it a `Phase` without moving any existing material (179), and the sulphur band's **two ends are registered** with the pressure anchor in their names (178 C). ⚠ **The four verdict cells all refuse**, on the 10–21 GPa Fe–S melting gap that predates this item, and **Mars is deliberately not wired** — declaring the material would replace the answers it has with a refusal. Unblocking needs a melting bound in that interval, which is a literature question, not a modelling choice. ⚠ Two owner cells stay open — the sulphur band, and binary Fe–S versus multi-component — and **both candidate EOS anchorings need supplementary tables we do not hold** (B24 Huang Table S5, B25 Xu Table S1). ⚠ **The verdict target does not wait for them**: Durán 2022's printed core radius 1820–1870 km and density 6–6.2 g cm⁻³ anchor the cell today, and **radius and density are two independent axes that each separate the two mantle families** — layer-free 1790–1870 km and 5.7–6.3 g cm⁻³ against layered 1630–1705 km and 6.5–6.75, with gaps of about 120 km and 0.2 g cm⁻³. ⚠ *An earlier version of this row said density could not discriminate; that was built on a density for Khan 2023 which the paper argues against rather than reports, and the retraction is in the section's third amendment* |
| **C56** | `fe_prem` looks temperature-blind, and it is the reference that makes it so | **checked 2026-09-09 — not a defect; recorded so the next reader does not re-open it** | Observed: `fe_prem.density(p, T, 0.0)` returns the same number at 300 K and at 2100 K while `fe_eps` moves. ⚠ **Measured and explained rather than filed as a bug.** The two phases carry different reference kinds — `fe_eps` is `isotherm` at 300 K (laboratory ε-iron), `fe_prem` is **`adiabat` at 1600 K**, because PREM is a fit to *the hot real Earth* and its geotherm is already inside the effective ρ₀. So `Phase.delta_t` returns `t · (1 − t_ref/t_pot)`: it is **keyed on the declared potential temperature, not on T**, and it is exactly 0 whenever `t_pot` equals 1600 K — an identity, not a tolerance, and the stated reason Earth does not move. Measured at 136 GPa: `t_pot` 1600 gives ΔT 0.0 K at both 2100 K and 4000 K (ρ 9916.9370 either way), `t_pot` 2000 gives 420.0 / 800.0 K (ρ 9908.4176 / 9898.9401), `t_pot` 3040 gives 994.7 / 1894.7 K (ρ 9893.4281 / 9862.1307). ⚠ The call that raised the question passed `t_pot = 0.0`, which the same function reads as «no declared potential temperature» and returns 0 by design — heating a PREM fit from a 300 K baseline would heat Earth twice, which `eos.py` names as the trap it is avoiding. No brief; no change |
| **C57** | the inversion branch is not on the node's path at all | **listed 2026-09-09; not decided** | ⚠ **Corrected from the first reading.** 173 reported this as an adapter default — `state.get("composition_intent", "earth_like")` always handing `solve` a composition — but the audit's call-graph read is sharper: `_from_state → _solve_from_state → solve` contains **no call** to `infer_composition`, `infer_three_layer` or `_porous_rock_verdict` at all, and the only callers are `rocky_roster.py` and `test_interior.py`. **Removing the default would not route the node to the inversion; there is no route.** So the four `inferred_*` regimes are dead code on the chain's path, C45 (d)'s inversion-convention exception guards something the checker can never make the node produce, and no body file will ever change that (173 measured it: 0). The question — should a recipe be able to infer a composition — is left open, and this row exists so the next reader does not re-derive the answer from the adapter line |
| **C58** | two of our own numbers for Mars's core-mantle boundary are 1700 K apart | **candidate, listed 2026-09-09** | C54 (b) declared Mars's core-side CMB temperature from the literature band **1900–2100 K** (Durán+ 2022, held). C20's thermal-history integrator ends the same body at **3763 K**. ⚠ **Both are ours and both are labelled**, and they disagree by roughly **1700 K** on one quantity of one body. The declaration is an observation-constrained band; the endpoint is the output of an integration whose Mars run has never been checked against Mars literature — but «the integrator is wrong» is a conclusion, not an observation, and it is not drawn here. Candidate only |
| **C59** | Mars's core radius and moment of inertia miss the board by 8.9 % and 2.7 %, and no gate had ever checked | **listed 2026-09-10 as a recorded disagreement** | Found by the **targeted** lane, which is the part worth keeping: `check.sh` ran three answer bodies named by hand and `bodies/mars.yaml` was in neither that list nor `gate_targeted`'s copy of it, so Mars's shipped-value comparison went unrun from 2026-09-08 until the body rule ran it (169 E made the list a glob). ⚠ **A narrowing found a hole in the full lane.** The engine gives `core_radius_fraction` **0.4919** against the board's **0.5398** — a core radius of about **1667 km** against **1830 km** — and `nmoi` **0.3545** against **0.3644**, which is the same cause seen through a second quantity. ⚠ **The 1667 km is not a Mars number**: it is what `composition_intent: earth_like`'s core mass fraction of 0.325 produces, and the board's 1830 km is the layer-free family's anchor (Stähler 2021) — the family the owner chose in 174. That the engine's value falls inside the *layered* family's window (Khan 2023, 1675 ± 30 km) is **read as coincidence**: we never elected that family. Neither the board value nor the tolerance was touched; the two rows print every run and are not counted (Brief 177). What closes this is **C55** (an Fe–S material, since our iron is too dense for Mars) and a declared Martian core mass fraction — not this row. ⚠ **178 C did not move it**: the Fe–S materials exist but all four verdict cells refuse on the 10–21 GPa melting gap, so Mars stays on `fe_prem` and both rows print unchanged. 177's resolution notice has still never fired on a real change |
| **C60** | the solve asks a core material for a surface-pressure density | **pre-registered 2026-09-10 — C60 (a); the build is Brief 181** | Found while 178 D was being built, and it is what actually blocks C55's verdict cells — ⚠ **and the first two descriptions of it, one per seat, were both right about different runs.** The audit measured a refusal at **18.9993 GPa**, a *boundary trial step* 0.7 MPa (0.0037 %) below the 19 GPa floor, in the body solve. This seat measured **0.0981 GPa** and traced it: it is a *trial central pressure* from `_shoot_pressure`'s bracket, reached through `integrate`'s `rho_c = mat_c.density(p_center, …)` on the radius-matching path — 23271 calls in that run, the next lowest at 59.0 GPa. **Neither pressure appears in any final profile.** So the shape is one thing seen twice: **a domain refusal raised during a trial is being read as a verdict about the body**, and the core material is only asked from the centre out to the CMB when the answer is actually computed. ⚠ **Removing the floor does not help** — with `p_min = 0` the same solve fails to converge at 9.808e7 Pa, since a 19 GPa-referenced BM2 has no root there. ⚠ **Mars's core-mantle boundary is 20.65 GPa, inside the fit**, so this is not physics telling us the material is wrong; it is the range the solver asks over. Two roads were listed — a low-pressure branch for liquid Fe–S (another fit, another paper), or a solver that asks a core material only at `P ≥ P_cmb` — and **C60 (a) takes a third**: a trial is not a verdict, so the boundary step is read against its own width and the shooting bracket's lower end is raised to the core material's floor. **No fit gains a range and no equation changes.** ⚠ **178 D's registered premise blamed the melting gap and was wrong** — the label on the material said melting, and the message was read as the mechanism |

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

### C1 — Sub-Neptunes, and the defect hiding behind them — **closed 2026-08-30**

The sweep (5 M⊕ · CMF 0.20 · 500 K at 1 bar) now solves at 2, 5, 10, 20 and 30 % gas and
declines at 50, 80 and 100 % citing the hottest bound solution and the wall above it —
neither sentence mentions a ceiling. `sub_neptune` is off `FLUID_CLASSES`; `gas_mass_fraction`
is the seventh declaration. GJ 1214 b (8.41 M⊕, 2.733 R⊕) is reproduced by 1.5–2.4 % H/He for
1-bar temperatures of 350–250 K, inside Valencia+ 2013's < 7 % and beside their ~3 % for a
solar-metallicity envelope.

Both measurements were wrong: the 17.7 M⊕ row was the polytrope era's, the "0 M⊕ since the
table" of 2026-08-28 was the same defect as the sweep's refusal (the envelope base cut off as a
surface), and the cap re-measured with the defect fixed was 11.46 M⊕ (interim, superseded
2026-08-30 F2: 16.69 M⊕ once the bulk-modulus finite difference stopped poking past the
silicate ceiling on the shooting's ceiling trial). Under it were three defects, none a ceiling: the
integrator took the envelope base leaving the H/He table's reach line for the 1-bar surface,
so the envelope had no mass; the temperature loop's proportional update diverges when the
1-bar temperature scales faster than the central one (thin envelopes on heavy cores); and a
ladder seed already over the target fell onto the inflated branch of the U-shaped surface-mass
curve. Each fix is gated so that no anchor path enters it, and the bit lines say so.
`engine/sub-neptune-context-notes.md` has the measurements.

Left open, named: a sub-Neptune now integrates but has **no dynamo path** — `core_state`
declines by class, `dynamo_giant` excludes it by mass, `dynamo_rocky` does not take the class.
Recorded as a gap edge in `chain.yaml` (`body_class → dynamo_rocky, via: sub_neptune`); not a
solver item, so it is not on this list. *(It became C18 under the owner's notation and closed on
2026-09-04 as a named refusal — see C18.)*

### C2 — The ocean layer, and multi-axis inversion — **closed 2026-08-29**

Liquid water came from SeaFreeze's `water1`, the phase switch is pinned inside the
integration step the same way layer boundaries are, and `infer_three_layer` returns a band
over the core axis, narrowing only when a measured C/MR² is supplied. Grid phase 2e-3 → 8e-7,
asserted at the gate. Condensed anchors bit-identical; `chain.yaml` cycle 7 declares the
phase → density → temperature loop.

Two of the five icy anchors came inside — Ganymede 2.1 % → 0.4 %, Europa narrowed to a 7 %
core under a 104 km ocean. **The other three moved the question rather than answering it,
which is C10.**

Reasoning: `engine/ocean-layer-context-notes.md`.

### C3 — The melting-curve gap, and dispatch by class — **closed 2026-08-30**

The ice material is now chosen by the local (P, T) against two published lines, never by
`body_class`: IAPWS's melting curve to 20.6 GPa, then Reinhardt+ 2022's liquid–solid line
(to 52.4 GPa) and its ice VII′–VII″ line (to 70 GPa), baked from the paper's public data by
`tools/make_ice_melt_table.py`. Below the VII′–VII″ line the column is the condensed ladder;
above it, VII″ and the liquid alike go to Mazevet's fit, whose floor is now the paper's own
1000 K rather than the ladder's 1800 K ceiling. Every result names the phase at both ends of
the column and the line it was measured against. Neptune's envelope base at convergence is
39 GPa · 2 555 K, 999 K above the liquid line — fluid for a stated reason. The seam at
20.6 GPa is +26 % in melting temperature, measured and stated; the grade is analog because
the lines are simulation.

Two things came out from under it. The "1797 K, three kelvin under the floor" was a trial
path, not the converged point; and Neptune's old convergence was luck — the 1-bar
temperature was jagged in the central temperature by ±0.4 K because the closing
extrapolation read its adiabatic gradient at a grid-bound step start. The gradient is now read
at the exit point and the temperature loop keeps its best pass; Uranus moved +3.8 × 10⁻⁵ in
radius, Neptune −2.8 × 10⁻⁴ (6 308 → 6 296 K at the centre), both reported in
`engine/melting-curve-context-notes.md`. Above 70 GPa no line reaches and none is invented:
the verdict says "fluid or superionic" with Millot+ 2018's one point.

**The seam is itself under review.** Kimura 2023
([`2023JChPh.158m4504K`](https://ui.adsabs.harvard.edu/abs/2023JChPh.158m4504K), *Revisiting
the melting curve of H₂O by Brillouin spectroscopy to 54 GPa* — a measurement across the whole
Reinhardt range, on the owner's paper-request list; bibcode checked by title, this session and
the audit session) becomes the arbiter of the disputed band when it arrives: its product is
not only a possible grade upgrade but a **re-verdict of the band (16.5–20.6 GPa / 715–902 K)
and a possible narrowing of the seam's width.**

**Revisited 2026-08-30 (F1), with the criterion fixed before the comparison.** Kimura &
Murakami measure melting only from 25.9 to 53.6 GPa (their lower rows are liquid runs at a
temperature *estimated from Queyroux's curve*). Against Reinhardt's line, six of their seven
melting points sit inside their own stated ±130–150 K, and the one outside (25.9 GPa) is the
measurement *hotter* than the simulation by 171 K — away from IAPWS, not toward it. At the
seam their Simon–Glatzel fit (eq. (2), anchored on Queyroux's 14.6 GPa · 850 K triple point)
gives 1028 K (968–1155 at 1σ): +14 % above Reinhardt and +44 % above IAPWS's 715 K.
**Kimura sits with Reinhardt; the step is not an artefact of the simulation.** C3 stays
closed, the seam number stands, the dispatch is unchanged, and the grade stays analog
because the check's own error is 8–11 % and it does not reach the seam. The band is not
narrowed: the measurement gives no support to IAPWS's end. Table I enters the gate as a check
table. What would still move this is a measured point between 15 and 26 GPa — Queyroux+ 2020,
now in the cache. `engine/seam-retrial-context-notes.md` has the tables.

**Revisited 2026-08-30 (water2): the open defect this row named is filled, not overturned.**
The band with no equation of state — liquid water above the ocean table's 2.3 GPa (or above
its 500 K) and below the hot-water fit's 1000 K floor, the one F2's Callisto and Titan at
f = 0.75 walked into — is now carried by SeaFreeze `water2` (Brown 2018,
2018FlPEq.463...18B; range as AQUA §2.3.5 states it, *"liquid and supercritical H₂O from
1 GPa to 100 GPa and up to 10⁴ K"*), baked ragged to the spline's **real** ceiling, which is
not its knot box: SeaFreeze's `water2` returns negative densities inside 100 GPa — valid to
2.3 GPa at 360 K, 10 GPa at 600 K, 13 GPa at 700 K, 30 GPa at 1000 K, hugging the liquid
side of this row's melting curve. Two seams measured: water1 ↔ water2 in their overlap ρ
0.13 % / dT/dP|_S 9 %; water2 ↔ Mazevet at 1000 K, Mazevet 2.5–3.3 % less dense over
2.3–26 GPa. Still uncovered by name: 12–20.6 GPa between the melting curve and the ceiling
(≲ 170 K wide), and hot water below 0.1 GPa. `engine/water2-context-notes.md`. C3 stays
closed; the dispatch by (P, T) is unchanged, one more material answers it.

**Parked at the gate 2026-08-30 (F4, Queyroux at the seam).** The band 16.5–20.6 GPa has
one measurement, Queyroux+ 2020 (2020PhRvL.125s5501Q, the arbiter's seat, independent of
Kimura 2023), and this repository holds its six-page Letter but not the Supplemental Material
that carries the individual melting points (Table S1). The values printed in the band —
15.6(2) GPa at 905 K and **18.4(9) GPa at 944 K** — are the ice VII″ → VII′ **isostructural
solid transition** on two isotherms (§*Isostructural transition*; Fig. 1 keeps "melting line"
and "isostructural solid transition" as separate symbols), not melting points; the triple
point is 14.6(5) GPa · 850(20) K. F1's criterion, reused, has nothing to put a residual inside
of, and a fit cannot reopen a row, so the fourth branch fires and nothing moves. What the
Letter does give is a **bound**: liquid at 15.4 GPa · 944 K (Fig. 2a) and solid at 18.4(9) GPa
· 944 K put T_m(18.4 GPa) above 944 K — above IAPWS's 690 K by 254 K and Reinhardt's 801 K by
143 K, the direction and size of Kimura's out-of-band point. Recorded as orientation, not a
verdict. Table S1 (free from APS, requested from the owner) is what would run the item.
`engine/queyroux-seam-context-notes.md`.

**Revisited 2026-08-31 (F4 resumed): Table S1 arrived, and the measurement sits with
neither curve — it is hotter than both.** Twelve measured melting points (Queyroux+ 2020
Supplemental Material Table S1, read from the PDF), three inside the band: 16.6 ± 0.5 GPa ·
930 ± 10 K, 16.6 ± 0.2 · 944 ± 10, 17.3 ± 1.1 · 978 ± 10. Against them IAPWS eq. (5) is
255–297 K cold (25–30 σ) and Reinhardt's line 213–228 K cold (21–23 σ); at every point from
8.4 to 17.3 GPa both curves are on the cold side, IAPWS already 69–79 K (14–16 σ) cold at
8.4–8.8 GPa. So of the three registered outcomes none fires as written: not "with Reinhardt",
not "with IAPWS" — **C3 does not reopen** — and not "between" but *above both*. The band is
redrawn to what the data support: **both curves too cold by 210–300 K at 16.6–17.3 GPa**,
Reinhardt the less wrong by 40–70 K; the +26 % step is in the measured direction and not
large enough; the dispatch is unchanged because the recipe has no third curve, and adopting
Queyroux's points as a melting-curve source is an owner decision with this table as its
grounds. Above 27 GPa (σ_T = 100 K) Reinhardt is inside at 27 GPa and hotter than Queyroux by
160 and 239 K at 36.7 and 44.7 GPa — while F1 found it inside Kimura & Murakami's ±130–150 K
at six of seven points; the two experiments differ by the 100–150 K Queyroux themselves
report against the laser-heated family, and this recipe does not adjudicate between them.
Grade: the measurement clears the 5 % bar (σ_T/T_m 0.7–1.3 % to 17.3 GPa) and the curves do
not clear the measurement, so analog stands with a new reason — the one measurement in the
band sits 210–300 K above both lines. Table S1 is a check table in `test_interior.py`.
Two ways a check can fail to raise a grade, now both on record: F1's — the check's own error
(8–11 %) is larger than the scale, so it cannot see; F4's — the check is precise enough
(0.7–1.3 %) and **the thing checked is wrong**. The grade word is the same; the reasons are
opposites, and the second is the one that names what would have to change.

**Revisited 2026-09-01 (Brief 33) — the owner adopted, and the adopted thing is not
"Queyroux".** F4's park closed the way it registered: the reopening condition (a
melting-curve source decision by the owner, with the S1 table as grounds) fired. Below the
kink (14.6 GPa) the dispatch now carries **the unweighted mean of the two post-2020
measurements** — Queyroux+ 2020's lower Simon–Glatzel and Prakapenka+ 2021's ice-VII
segment — a stretch where the continuous-vs-discontinuous lineage debate (Rescigno+ 2025
defends continuous; Datchi stands on both sides) does not exist and the two agree
(|Q−P| ≤ 54 K vs 71–348 K to the old curve). Our own IAPWS piece is excluded from the mean
(a three-way mean let our curve vote on its own trial, 111–120 K below both measurements).
Label conditions carried in `eos.py` at the constants: the two papers share Datchi's anchor
(2.17 GPa · 354.8 K printed in both), so the 1.0 K agreement at 8.2 GPa is never independent
confirmation — the independent number is 8.7 K at 20.0 GPa; the mean's uncertainty is the
curves' separation alongside each σ, never σ/√2; below 8.4 GPa the span is anchored
interpolation, not measurement support. **14.6–20.6 GPa is now a named disputed refusal**
(the sources agree numerically but assign different phases — VII′ vs VII — and the dispatch
consumes the phase; verdicts are still given outside the candidates' envelope, and no roster
body reaches the band: ice-giant column tops 34.5/39.2 GPa, moon calls all below 8.4 GPa).
Above 20.6 GPa nothing changed. **The grade's reason moves accordingly**: below the kink the
curve is no longer simulation but the mean of two mutually consistent measurements (grade
question now hangs on the mean's declared uncertainty, not on "the lines are simulation");
in the band the honest state is refusal, not a graded curve. Handover step at our VI–VII
triple point: +4.1 K, recorded not smoothed. Anchors bit-identical (measured); the old seam
sentence ("+26 % at 20.6 GPa, both curves cold against S1") stays above as the record of
what the dispatch was when C3 closed.

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

### C5 — Where the giants' leftovers belong — **closed 2026-08-30**

Two residuals; both now have an owner, and one has two declarations it can be read against.

**Jupiter, and the diluted core — reached, no consumer.** The mixture rule carries one
homogeneous Z through the envelope. Post-Juno structure is not "graded inward": Debras &
Chabrier 2019 §4.1 (2019ApJ...872..100D, text in the cache) is titled *Inward decreasing
abundance of heavy elements in some part of the outer envelope* — locally ∇Z > 0 — and the
structure needs four regions: an outer convective envelope, a composition-and-entropy
gradient, an inner convective envelope and an extended dilute core. Not implemented: Alpha
Centauri A b's radius is a declaration, so nothing in the roster would read a graded-Z
envelope today. The earlier compact-core attempt and its silicate ceiling stay in the domain
row.

**Corrected 2026-08-31 (survey ⑥) — this row claimed "two transcribable forms exist" and one
of them is not one.** *Helled & Stevenson 2017's* Z(m) is a Gaussian the paper prints and
then disowns twice: the sentence introducing it says *"In such a case (**which is merely
chosen to aid the explanation**)"*, and §I says the validity of their suggestion
*"**doesn't automatically lead to a prediction for the final Z-profile** which depends on the
specific conditions under which the giant planet has formed."* What the paper gives is a
**formation-history relation** plus an illustrative profile computed from a specific Jupiter
formation model — not a form to transcribe. The accurate label is *"a formation-history
relation, and an example Gaussian chosen to aid an argument."* **`Howard, Guillot & Bazot
2023` is a real closed form** and stands: an erf profile whose width parameter δm_dil the
paper *"set[s] to 0.075"*, with no derivation or sensitivity test in the text.

*The consequence for C13*: its registered fourth branch — Helled & Stevenson's ice-envelope
applicability — **closes here, and not for the registered reason.** Not "Jupiter-only, cannot
be transferred" but **there is no function to transfer**; the mechanism's own conditions are
composition-independent, and the profile only ever arrives through a formation model our
bodies do not have.

*And the row was missing the paper that matters most for the ice giants.* **Vazan & Helled
2020** ([`2020A&A...633A..50V`](https://ui.adsabs.harvard.edu/abs/2020A%26A...633A..50V),
arXiv 1908.10682, cached) is about **Uranus**, fits **the moment of inertia directly**
(*"we fit MoI instead of the gravitational moments"*, target **0.222–0.230 MR²**), tests
whether a gradient survives on Gyr timescales with the Ledoux criterion, and tabulates four
adopted models. Its conclusion lands on this list's own open question: *"an interior with a
**mixture of ice and rock, rather than separated ice and rock shells**, is consistent with
measurements, suggesting that **Uranus might not be 'differentiated'**."* It has no closed
Z(r) either — it sweeps *"composition gradients of various slopes"* and selects on R, L and
MoI.

**The ice giants — the residual has an owner, and the question was wrong.** Helled,
Nettelmann & Guillot 2020 (2020SSRv..216...38H, text in the cache): "even a very small (in
mass) H-He atmosphere can imply high interior temperatures, if an adiabatic temperature
profile is assumed" — the +8 % / +14.7 % central-temperature excess is the signature of an
adiabatic H/He envelope, not a missing material, and whether layer transitions are sharp or
gradual is open (their Fig. 4). Nettelmann, Wang & Fortney 2016 (2016Icar..275..107N, text
in the cache) put the mechanism at the **boundary**: a stably stratified thermal boundary
layer at the H/He–ice/rock transition near 0.1 Mbar (their Table 1), whose class II and III
models "yield by a factor of up to about 2 to 3 warmer core temperatures than the class I
models. As a result, the presence of rocks is required in the inner mantle in order to
match the gravity data" (§7); their U15-II has ΔT = 2500 K and U15-III 4700 K (Fig. 9),
≈ 5000 K (≈ 9000 K) higher central temperatures (§6), and their favoured models carry 1× solar
I:R with "the mixing behavior of rocks with … ices … not well-understood". Their negative
result is narrower than it was quoted: the I:R ratio "does not provide a solution to the
**low luminosity**" (§3) — a cooling-time statement, not a gravity-fit one. C4 is not a
candidate for this residual either way.

**Two declarations, integrated without tuning.** `boundary_temperature_jump` (the TBL step at
this recipe's mantle/envelope boundary, 30–40 GPa for the anchors) and
`mantle_rock_fraction` (silicate mixed into the water phases above 2.3 GPa). Published values
for the first (2500 K, 4700 K); no published mass fraction for the second, so a declared grid:

| declaration | Uranus ΔR (T_c) | Neptune ΔR (T_c) |
|---|---|---|
| none (anchor) | +5.48 % (6 160 K) | +8.94 % (6 296 K) |
| ΔT 2500 K | +7.99 % (11 493 K) | +11.50 % (11 886 K) |
| ΔT 4700 K | +10.04 % (15 661 K) | +13.58 % (16 241 K) |
| rock 0.10 | +3.64 % (6 275 K) | +7.02 % (6 401 K) |
| rock 0.20 | +1.83 % (6 369 K) | +5.13 % (6 486 K) |
| ΔT 2500 K + rock 0.10 | +5.61 % (11 630 K) | +9.00 % (11 994 K) |
| ΔT 2500 K + rock 0.20 | +3.26 % (11 718 K) | +6.56 % (12 053 K) |

Read, not fitted: the boundary layer **widens** the radius residual (+2.5 %p per 2500 K) and
raises the centre by ≈ 5 300 K per 2500 K — the same ≈ 5 000 K Nettelmann report for class II;
rock **narrows** it by ≈ 1.8 %p per 0.10. Neither published value closes either planet on its
own; the two together are the chain the paper describes (warmer → less dense → rock), and the
rock fraction that would close it is not a number this recipe has a source for, so it is not
declared. Anchors keep both at 0 and are bit-identical. `engine/giant-residual-context-notes.md`
has the runs and the provenance of every number.

*Revisited 2026-08-31 (C13)* — (a)'s *"reached, no consumer"* was true when written and is
**superseded on the consumer half**: the ice giants' measured C/MR² deficit (−15.8 % /
−11.4 % after the radius is stripped, the gate's 2026-08-31 comparison) is a consumer. The
blocker moved, it did not vanish — not "nothing would read a graded-Z envelope" but "the
recipe cannot yet hold the arrangement it would grade toward": see C13, where the rock-free
extreme refuses at stack build. (b) is untouched.

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

### C7 — Partial differentiation — **closed 2026-08-30: the intermediate state is not a mixture**

`differentiated: false` integrates rock and metal mixed in one layer and declines when ice
or gas is present. The refusal stays; its reason is raised. It used to say the mixture rule
handles rock and metal only — true of the code, and an invitation to go looking for the
missing rule. Searched 2026-08-30 (additive-volume / ideal / linear mixing for rock + ice,
interior models of undifferentiated icy bodies): **no mixing rule for an ice-bearing layer
exists, and no published bound on the error of using one.** Two reasons, and they are the
content of this closure.

**It is a reaction, not a mixture.** Water and silicate combine into hydrated minerals with
their own density, volume change and heat; that is why hydrated-rock density in the
literature comes from Gibbs-energy minimisation over a mineral database rather than from
mixing two end-member densities. C10 hit the same wall from the other side — no closed-form
hydrated-rock EOS and no ice–rock mixing rule are two faces of one fact.

**It is a process, not a state.** What makes a body neither fully mixed nor fully layered is
how far the water got. Malamud & Prialnik 2015 (2015Icar..246...21M) start from a
homogeneous ice–rock body and follow the multiphase flow of water through porous rock, the
differentiation that results and the aqueous alteration of the rock, with the density profile
from hydrostatic equilibrium maintained through changing composition, pressure and
temperature; Malamud & Prialnik 2013 (2013Icar..225..763M) treat serpentinisation
explicitly, exothermy included; Prialnik & Merk 2008 (2008Icar..197..211P) is the porous
icy-body evolution code both stand on. **Provenance, plainly: all three are Elsevier, no
preprint, and only the abstracts were read.** This closure can say a treatment exists and
what kind it is; it cannot say whether it is transcribable. Malamud & Prialnik 2015 goes on
the owner's paper-request list serving **C7 and C9 at once** — its heat sources include
compaction's gravitational potential energy and serpentinisation, two of the five
exclusions C9 is about.

**This does not touch C10.** C7 forbids mixing water *into* silicate — a reaction. C10 mixes
antigorite with enstatite/PREM: two solids coexisting as grains, each with its own measured
equation of state, which is what a partially serpentinised rock physically is. Volume
additivity between them is standard and is the same shape as the rock–metal rule this
recipe already carries, so C10's interpolation is one declared axis — how serpentinised —
and not the forbidden mixture.

**Revisited 2026-08-30 (F3), from the full text now in the cache.** The stated limit is
removed in the transcribable direction: the paper's EOS (§3.3, eqs. (1)–(7)) is an
**equilibrium closed form in (P, T, X_d) with every coefficient printed** — porosity of ice
ψ_w = 0.45 exp(−β_w(T/T_m)√P) and of rock ψ_d = 0.4 exp(−β_d P) Γ(T_max), volumes added by
the two-layer model — and its only history variable is T_max, one number per shell. It fits
laboratory compaction to 764 MPa, ice I only, no rock melt; at Callisto's and Titan's core
pressures it is out of range and gives ~1 % void, so **it does not reach the deciding region
of C10's three moons; it reaches their crusts.** Both reasons above are confirmed from the
text: serpentinisation is a reaction *"only so long as there is available liquid water"*, and
the front is an output of a 4.6 Gyr multiphase-flow run with no input parameter for how far
melting reached. **One sentence above was too broad and is corrected here in words:** a
mixing rule for an ice-bearing layer *does* exist for the never-wet state — cold ice and rock
grains, each compacted on its own curve, volumes additive (Yasui & Arakawa 2009's two-layer
model, adopted as eq. (1) and reported to reproduce the mixture's compaction curve) — which is
C10's shape; what still has no rule is the reacted, partially differentiated body, and the
refusal stays on that. "No consumer" is therefore a **choice** about the missing front, not an
absence of a treatment. The full text names the declared-front shortcut (*"assuming that
differentiation somehow occurred, without actually computing how"*) and does not take it;
grounds for a middle rung — a declared front plus a cold mixed crust, Callisto and Titan as
consumers — are written as a proposal, not an item, in
`engine/malamud-readthrough-context-notes.md`. C7 stays closed.

### C8 — The temperature branch's validated window — **closed 2026-08-30**

The adiabat had one published check, Unterborn+ 2019 eq. 7 — 4.4 % at 1 R⊕, −17 % at
1.46 R⊕ — and one anchor is a coincidence with an error bar. The second is Noack & Lasbleis
2020 (2020A&A...638A.129N, PDF in the cache): their eq. (22) carries the mantle adiabat to the
CMB with every term printed, valid 0.8–2 M⊕ for Earth-like composition, and all constants
were re-read from the PDF. Their eqs. (20)–(21) are initial post-magma-ocean temperatures and
were not used. Engine against both, Earth-like CMF 0.325 at 1600 K
(`test_interior.py --adiabat`, and the section *Temperature, checked against a published
core-mantle boundary* carries the full table):

| M (M⊕) | R (R⊕) | engine | vs eq. (22) | vs eq. 7 | anchors vs each other |
|---|---|---|---|---|---|
| 0.8 | 0.942 | 2430 K | −2.2 % | −2.9 % | +0.7 % |
| 1.0 | 1.003 | 2526 K | −1.4 % | −4.4 % | +3.1 % |
| 1.5 | 1.123 | 2724 K | −0.7 % | −7.2 % | +7.1 % |
| 2.0 | 1.216 | 2884 K | −0.8 % | −9.5 % | +9.6 % |

The Earth point reproduces the 2562 K an independent reading reported (2563 K) — the
transcription check. So the grade above 1.05 R⊕ rests on a measured spread: the engine is
within 2.2 % of one published estimate and within 9.5 % of the other, and **the two published
estimates disagree with each other by up to 9.7 %**, with the engine between them. The
agreement in absolute temperature is partly two differences cancelling (the paper's 2000 K at
250 km against the engine's 1736 K there; the engine's rise to the CMB 12–14 % steeper than
the paper's damped exponent), and the test pins both. **2 M⊕ (1.22 R⊕) is the paper's own
ceiling**; above it the recipe is back to one anchor, to Unterborn's 1.5 R⊕. Anchors
bit-identical: this added a comparison, not a change to the adiabat.
`engine/adiabat-window-context-notes.md` has the transcription and the runs.

### C9 — Porosity on a heated body — **closed 2026-08-30: a relation exists, and it depends on rheology**

**This row's own prediction was wrong, and is corrected here rather than quietly.** It said
*"this one may close as 'the bound is the answer', which is a legitimate ending."* The
2026-08-30 survey found otherwise, and a row that carries a guess carries the duty to correct
it — left standing, it tells the next reader to skip the search.

The compaction relation (Bierson+ 2019) returns an upper bound on void space, never an
estimate, because melt, differentiation, convection, impacts and tidal heating all remove
porosity and its §2.2 excludes all five. **Three of the five are carried, with
coefficients, by Neumann & Kruse 2019** (2019ApJ...882...47N, open access, full text fetched
through the ADS gateway into the cache and read): Enceladus heated by radionuclides and tidal
dissipation, differentiating through a melting front, its core compacted by creep — their
§2.5, "compaction is a change of the density and volume of a porous material that is being
heated and applied pressure to … facilitated by creep processes on a geologic timescale" —
with the olivine creep laws of Mei & Kohlstedt 2000 and the antigorite law of Amiguet+ 2012,
coefficients for dry olivine (A1–A4), wet olivine (B1–B4) and antigorite (C1–C2) in their
Table 3. Results: core radius 185–205 km, **porous core layer 4–70 km**, ocean ≈10–27 km, ice
shell ≈30–40 km. Convection and impacts: ✗ — still carried by nobody, and said so.

**How it closes.** Not "the bound is the answer" and not "the bound is replaced":

- Bierson's bound stays the **general case**, validated over 123–2326 km diameter; Neumann is
  one body at one size (252 km) and cannot replace a general bound.
- Neumann & Kruse enter as the **branch** for a tidally heated, differentiating body, grade
  analog — **reached and specified, not wired.** The relation is a creep law integrated over
  a thermal history (porosity as a function of time, stress, grain size, water and
  temperature), and this recipe integrates hydrostatics, not time. Wiring it means a thermal
  evolution the recipe does not have; the specification (which creep laws, which table) is
  written so that whoever brings the history finds the branch ready. Consumers, when it is
  wired: the icy anchors that are heated and differentiating — Enceladus first (the paper's
  own body; on the icy roster, solved today with no porosity declared), Europa, and the roster's
  tidally heated moons that declare `tidal_heating`.
- **The path on the day it is wired:** parse Table 3 from the cached publisher HTML
  (`docs/phase3/_papers/2019ApJ...882...47N.html`, whose `<table>` keeps the columns the text
  extraction flattened) or from the publisher PDF (`PUB_PDF` on ADS), bake the creep
  coefficients the way the other tables are baked, and integrate the creep law over a declared
  thermal history — the history being the thing the recipe does not yet have.
- Malamud & Prialnik 2015 (2015Icar..246...21M, on the request list from C7) serves this item
  too: its abstract carries compaction's gravitational potential energy and serpentinisation
  heat as heat sources — two more of the five.

**The discriminator it hands C10, kept on its own layer.** "No porosity is retained for an
antigorite rheology, implying that the core of Enceladus is not dominated by this mineral."
Vance+ 2018 gave two routes to Enceladus's ~2700 kg/m³ — hydrous rock, or anhydrous rock plus
pores — and density alone cannot tell them apart; retained porosity can, because antigorite
is weak and creep closes its pores. **That is a rheology statement, not a density
statement**: Hilairet's antigorite ρ₀ still stands and still lands on Vance's target. What
Neumann adds is that a body *made* of it would not keep its pores. The two live on different
layers; a later session must not read this as a density refutation.

*Revisited 2026-08-31* — **a time axis was considered and rejected** (owner's decision; the
planned C13 was not opened). Not because the recipe lacks an axis, but because **the axis is
a different one**. The Neumann & Kruse relation does not take an age in Gyr. What it takes is
**t₀ — the accretion time after CAI formation, in Ma** (their §2.3), and the outcome turns
on that value at the megayear level: for the wet olivine rheology successful models live in
t₀ ≈ 1.3–1.9 Ma (§3.3), and for the antigorite rheology **no differentiation occurs at all
for t₀ ≥ 5.5 Ma (at ϕ₀ = 0.6)** (§3.4) — because the short-lived isotopes (²⁶Al, ⁵³Mn, ⁶⁰Fe) release their
heat "within the first few millions of years after CAIs" (§2.3; all read from the cached
text this session). The structure is decided within ~5 Ma; the remaining 4.5 Gyr is
bookkeeping. **Feeding `body_age` (Gyr) into this node would give it the number it is least
sensitive to while the number it is most sensitive to stays undefined.** The six consumers
in sight (Uranus, Neptune, Callisto, Titan, Europa, Enceladus) are all solar-system anchors
whose ages are CAI-anchored directly, so inheriting an age from a star does not even arise
for them. For invented bodies neither t₀ nor the initial ²⁶Al abundance derives from the
star's age (Lichtenberg+ 2019 — reported by the directing session as 0–10× solar ²⁶Al₀
across systems, not re-read here — *corrected 2026-09-03 from the cached preprint, C21 (a): the paper's
scanned range is **[0.1, 10] × ²⁶Al_⊙**, floor 0.1 not 0, and it is a model scan, not an observed
distribution*): both are **declarations**, not derived values, and
whether to introduce them is a Phase 4 owner decision. Since ²⁶Al matters only for bodies
small enough to be shaped by it, the node never applies to the ice giants. **Do not draw a
`body_age → porosity` edge in the chain**: the edge is real but the payload would be wrong —
it must carry `t_form` (Ma after CAI), not `t_body` (Gyr); a Gyr endpoint is at most an
`influences`. Two papers considered for the request list are dropped with the time axis —
**Kruijer+ 2017** (Jupiter's Hf-W age) and **Castillo-Rogez+ 2009** (Iapetus): both served
only the Gyr-age inheritance question, which no longer exists.

**Revisited 2026-08-30 (F3), from the full text.** The abstract-derived sentence holds and
gets its weights: serpentinisation heat is the second source after radioactivity (an order of
magnitude below it over the run, twice it in the first 200–235 Myr); compaction's
gravitational energy is *"marginal"*, two orders below serpentinisation. Tidal heating,
impacts and convection are still carried by nobody — satellites are excluded from the
paper's sample for the first two. What the text adds is a **third relation of its own kind**:
rock porosity as a closed form in (P, T_max), eq. (5) with a step Γ centred at 675 K that the
authors call *"hypothetical"*, valid to ~0.8 GPa, ice I, no rock melt. It does not replace
Bierson (general) or Neumann (rheology over a history); but its history is one declared
number per shell, T_max ≥ T, and the present T gives the maximum porosity — a bound. For
this relation "reached, no consumer" is a choice about a declaration, not about a thermal
evolution. Transcription note when it is ever wired: the printed eq. (7) exponent
15(T_max/675) − 1 contradicts the text's stated behaviour; 15(T_max/675 − 1) is the form the
text describes. `engine/malamud-readthrough-context-notes.md`. C9 stays closed.

### C10 — Lighter rock — **closed 2026-08-30: the axis exists, and it does not reach**

Callisto, Titan and Enceladus sit **above** every three-layer band: every member of a band
lowers C/MR² as the core grows, so a published value above the zero-core end cannot be reached
by any layering, and the reason was read as the material — rock lighter than the
enstatite-plus-PREM silicate, hydrated or porous. Set aside on 2026-08-26 for want of a
grounded lighter rock; the evidence arrived and was used.

**The material.** Hilairet, Daniel & Reynard 2006 (2006GeoRL..33.2302H, open access, PDF in
the cache): antigorite compressed to 10 GPa with no amorphisation, transition or hysteresis;
their adopted second-order Birch–Murnaghan **V₀ = 2926.23(50) Å³, K₀ = 67.27(123) GPa,
K₀′ = 4**, confirmed by an F–f plot (§3 [13]). The paper prints no ρ₀; it prints the structural
formula (Mg₂.₆₂Fe₀.₁₆Al₀.₁₅)(Si₁.₉₆Al₀.₀₄)O₅(OH)₃.₅₇ (§2 [6]) and "the V₀ value corresponding to
m = 1 … is 172 Å³" (§4 [15]), and from those **ρ₀ = 273.50 u / 172 Å³ = 2640.5 kg/m³** — derived
here from the PDF, matching two earlier independent readings (2638–2640), and checked twice:
2926.23 / 172 = 17.01 is the m = 17 polysome the paper indexes with (Capitani & Mellini 2004),
and the paper's one printed density, 2765 kg/m³ at 5.7 GPa and 470 °C, comes back as 2841 at
room temperature on this curve — +2.7 %, the size and sign of 450 K of expansion.
**Room temperature only**: the paper measures no thermal term and borrows Holland & Powell
1998 where it needs one; that paper is on the request list, and the grade is set by this
deficiency, not by the fit. `test_interior.py` re-derives ρ₀ and re-runs both checks.

**The axis.** `serpentinisation`, a declared fraction of antigorite in the rock layer, mixed
by additive volume with the silicate — **two solids coexisting as grains**, the rock–metal
rule's own shape and not the reaction C7 declined (water *into* silicate). Where the water
went is history, so it is a declaration and drops the grade. Temperature passes through the
antigorite component the way it passes through any phase without thermal constants.

**Bracketing, and the result.** Antigorite sits under the Vance+ 2018 targets (2641 kg/m³ at
Enceladus's 0.023 GPa, 2742 at Callisto's 2.73, 2761 at Titan's 3.28, against ~2700 and
~3100) and the existing silicate sits over them, so the three-layer band was re-run at
fractions 0, 0.25, 0.5, 0.75, 1 — declared, not fitted:

| moon | published | band top f = 0 → 1 | fraction in [0, 1] that closes it |
|---|---|---|---|
| Callisto | 0.3549 | 0.3119 → 0.3321 | **none** — 0.023 short at pure antigorite |
| Titan | 0.3414 | 0.3126 → 0.3334 | **none** — 0.008 short |
| Enceladus | 0.3350 | 0.3008 → 0.3216 | **none** — 0.013 short |

Lightening the rock to pure antigorite closes 40–75 % of each gap and no more. That is the
strong result the brief allowed for: **the answer on these three is not serpentinisation but
void space** — C9's branch, porosity retained on a heated body — or the partial
differentiation C7 declined to model. Two items now answer one question from two sides, and
C9's discriminator keeps its own layer: a body whose core is antigorite-dominated would not
keep its pores (rheology), while Hilairet's density stands (density) — on Enceladus the two
statements together say the pores are in rock that is *not* mostly antigorite, which is
consistent with this table.

**Dante / Hades.** One of the two readings of that open radius question is that the rock is
lighter than this silicate; C10 gives it a tool and does not run it. The judgment is the
owner's.

**Revisited 2026-08-30 (F2), with the overturn condition registered first.** Holland & Powell
1998 is in the cache and antigorite **is** in its Table 5 (atg, a° = 4.70×10⁻⁵ K⁻¹ in
α(T) = a°(1 − 10/√T), κ₂₉₈ = 525 kbar, the C_p polynomial), and Hilairet's §4 borrows from
exactly that paper — the chain holds. The term is carried flattened at 298 K
(αK_T = 1.33 MPa/K with Hilairet's K₀; c_V 966 J/kg/K), from a pure-Mg end-member onto a
natural Fe/Al sample. Re-run on the same grid, the bands are unchanged to four decimals at
every finished point (Enceladus −0.0001 at f ≥ 0.75; Callisto and Titan at f = 0.75 ran past
the sweep's budget, a C3 band defect traced in the notes, not a change in the answer): the
moons' rock sits within ~100 K of the reference and the thermal pressure is ≲ 0.1 GPa
against 2–3 GPa. **No moon reaches its
published C/MR² at any fraction in [0, 1]; C10 stays closed.** The grade stays analog, and
its reason is now the borrowing and flattening, not the term's absence — the sentence that
said otherwise is rewritten here and in the docs. Two ceiling-poking finite differences were
fixed on the way (`eos.Material.k_t`, `interior._adiabatic_dtdp`); no anchor touched.
`engine/antigorite-thermal-context-notes.md` has the transcription and the runs.

### C11 — The middle rung: a declared differentiation front and a never-melted crust — **opened 2026-08-30 on F3's grounds; closed 2026-08-30; the declared pair settled 2026-09-01 — the grid is the answer, and no pair is elected**

**What it is, and what it is not.** C7 refuses a body that is neither fully mixed nor fully
layered, because ice mixed through rock *where liquid water reached it* is a reaction and a
transport history. **C7 stays closed, and C11 is not its repair.** C11 is the other case F3
found in Malamud & Prialnik 2015's full text: the depth the melting reached is taken as a
**declaration**, and the body is static — metal core, rock, water/ice mantle, and above the
front a crust that never melted, cold ice and rock grains never in contact with liquid water.
Hydration is a story about places liquid water reached, so C7's argument does not apply
there; and for that state a mixing rule exists — Yasui & Arakawa 2009's two-layer model,
adopted as Malamud & Prialnik's eq. (1) and reported to do *"a very good job of reproducing
the compaction curve of the mixture"* (§3.1.3) — the shape C10 already uses for antigorite
plus enstatite. The first row added after the list closed.

**Two declarations, not one.** `differentiation_front` (cumulative mass fraction from the
centre that melted; 1.0 is today's body) and `crust_rock_fraction` — the second because the
source's outer mantle is *not* primordial: it is ice-enriched by water that rose and refroze
(§5.1), so the front alone does not fix the crust's composition; the primordial fraction is
an upper bound. Optional `crust_porosity`: the same paper's eqs. (4)–(6) with Γ = 1 (never
melted), laboratory compaction curves, an **upper bound** on void. Directions registered
before the sweep: crust rock **raises** C/MR², porosity **lowers** it. `_stack` gains the
crust as a fourth layer (ice ladder + silicate as grains, additive volume, no
serpentinisation — water never reached it); a crust step above the melting curve is refused
as a self-contradictory declaration. Grade analog whenever a crust is declared; the
Malamud porosity functions landed first (8786d857) so no intermediate commit is broken.

**The sweep, on a declared grid, not tuned.** Potential temperature 200 K — at the roster's
270 K the crust is refused, because ice Ih/III/V melt at 251–273 K between 0.02 and 0.6 GPa
and a never-melted crust cannot sit there; the reference (front 1.0) is re-run at the same
200 K. `infer_three_layer` over core fractions 0/0.15/0.30/0.45; `test_interior.py
--middle-rung` regenerates it. Band = C/MR² over the core-fraction members that reproduce
the radius:

| moon (published) | front | X_d 0.3 | X_d 0.6 |
|---|---|---|---|
| Callisto (0.3549) | 1.0 | 0.2881–0.3127 (no crust) | — |
| | 0.9 | 0.3010–0.3077 | 0.3155–0.3203 |
| | 0.8 | 0.3107–0.3158 | 0.3393 |
| | 0.7 | 0.3220–0.3348 | **0.3561–0.3643** |
| | 0.6 | 0.3275–0.3390 | 0.3714–0.3768 |
| Titan (0.3414) | 1.0 | 0.2883–0.3138 (no crust) | — |
| | 0.9 | 0.3011–0.3081 | 0.3158–0.3207 |
| | 0.8 | 0.3103–0.3300 | **0.3384–0.3498** |
| | 0.7 | 0.3218–0.3350 | 0.3547–0.3633 |
| | 0.6 | 0.3270–0.3390 | 0.3695–0.3757 |

**Where they land.** C10's grid lay entirely below both published values; C11's grid
**brackets them**. Titan's 0.3414 falls **inside** the band of one declared pair — front
0.8, X_d 0.6 (0.3384 at core 0.15 to 0.3498 at core 0) — closed along the core axis the way
Europa's is, with the declarations untouched. Callisto's 0.3549 falls **between** two
declared pairs: above the front 0.8 · X_d 0.6 band (0.3393) and just below the front 0.7 ·
X_d 0.6 band (0.3561–0.3643), 0.0012 under its low end; no grid point's band contains it,
and the grid is not refined to make one — that would be the fitting C5 and C10 declined.
Porosity on the front 0.7 · X_d 0.6 pair moves the band down as registered: Callisto
0.3561–0.3643 → 0.3390–0.3494, Titan 0.3547–0.3633 → 0.3386–0.3496 (about −0.015, the
laboratory upper bound on crust void). One member did not converge (Callisto, front 0.9 ·
X_d 0.3, core 0.30).

**Owner's decision 2026-09-01: the grid stands as the answer and no pair is elected.** The
question this row left open — *which declared pair should Callisto and Titan actually use* —
is resolved by declining it. **Titan's published value falls inside one pair's band and
Callisto's falls between two**, and refining the grid to capture Callisto's remaining 0.0012
is the fitting C5 and C10 refused and Brief 26 refused again. So the published statement is
the band, not a point: **the recipe says what each declaration implies, and does not claim to
know which one these moons are.** Anything downstream that needs a single number — a cfg
value, a board row — declares its own choice and carries that label, rather than borrowing
authority from a measurement that was never made. The table is the regeneration on the code that
ships (2026-08-30, after the crust-refusal fix was narrowed — see the notes' post-mortem),
identical at all twenty points to the first pass; run times 2–7 min per point; the 270 K
refusal through the inversion route did not finish in 17–24 CPU-minutes and was stopped — the temperature bracket is
exhausted on every solve of the regula falsi — where the direct `solve` refuses in about 12 s.
Recorded as a cost, not fixed here.

**What moves and what does not.** Anchors bit-identical: Uranus and Neptune (the stack's
bounds for a body with a gas envelope reproduce the old expressions to the bit — checked
after a negative-crust bug in the first pass had frozen both as refusals, which is exactly
the failure the anchor exists to catch), Europa's inversion, the rock and giant anchors;
`--refresh` for the fingerprint (`_stack`, `integrate`, `shoot` changed). The Callisto and
Titan question C10 left — *void space or partial differentiation* — now has its second half
measured: a declared front with a rock-bearing crust reaches the published values, a
serpentinisation fraction does not. Which pair, if any, a body should declare is the owner's
call; this row supplies the grid. `engine/middle-rung-context-notes.md`.

### C12 — A ternary anchor from a diffusion table? — **opened 2026-08-31 on the owner's grounds; closed 2026-08-31, recorded**

**A check, not a material — and not a reopening of C4.** Opened when the owner doubted the
report that Bethkenhagen+ 2017's typeset version (`2017ApJ...848...67B.pdf`, in the cache)
carried no usable data — a report made from the text layer twice — and read it as images:
the EOS grid is indeed absent (Figures 1–3 only, no table, no supplement; **C4's methane half
stays on its author-request route**), but **Table 1** prints R · ρ · T · p at thirty state
points along three Uranus profiles beside the real 2:1:4 mixture's self-diffusion
coefficients. If ρ were the mixture's, water-alone could be measured against the real ternary
— the number C4 said needed the tables.

**Settled from the text first**: §4 introduces the table as *"the diffusion coefficients of
each species in the real ternary mixture, as well as radius, density, temperature, and
pressure along the three profiles"* — profile quantities; §2.7 matches the profile's
*pressure* within 2 % and says nothing of tabulating the box's density; the mixture's own
density appears as Figure 4. The text's reading is (나), the profile's density. **The
registered discriminating check then failed on its own premise**: this recipe's water
(Mazevet+ 2019 at all thirty rows) is 18–32 % denser than *every* printed ρ, including the
water-only profile's (29 % at 6.9 GPa · 1775 K → 18 % at 510 GPa · 5750 K), so the column is
not pure water's density anywhere — and both readings can explain that size (an H/He-bearing
inner envelope under (나); a mixture 15–25 % lighter than water under (가), which C4's own
ammonia result makes plausible). **Closed on the conservative branch**: no ternary anchor can
be read from the column with the evidence held; C4's composition tier keeps its water +
ammonia number. What would settle it: Redmer+ 2011's own ρ(R) for the water-only model, or the
authors. **The failed test was the audit session's proposal, fixed into the brief by the
directing session — the responsibility is joint**, recorded the way this project keeps every
error named. *Observation, derived, not a verdict*: the residual shrinks with depth
(+29 % → +16–19 %), which is qualitatively what reading (나) with a small H/He admixture in
the inner envelope would do; Redmer+ 2011's ρ(R) would most likely settle it that way.
**Redmer+ 2011** (Icarus 211, 798, the water-only Uranus model) goes on the owner's
paper-request list; if it prints 1.00 g cm⁻³ at 0.839 R_U, (나) is settled and C12 reopens as
*revisited*. *(Superseded by the revisit below, written later the same day: the paper was obtained,
printed no ρ(R), and came **off** the list because a shell-boundary sentence replaced the need — the
later paragraph is the current state, kept here as the record of what was asked; Brief 64 labelled it.)* No code, no anchor, no gate change. `engine/ternary-anchor-context-notes.md`.

*Revisited 2026-08-31* — the owner obtained **Redmer+ 2011**
([2011Icar..211..798R](https://ui.adsabs.harvard.edu/abs/2011Icar..211..798R), cached as
`docs/phase3/_papers/2011Icar..211..798R.pdf`), and the expected settle path does not exist
in it: **no ρ(R) table** (Figures 1–3 only, no supplement; the structure models are taken
from Fortney & Nettelmann 2010). **(나) is settled anyway, by a shorter path** — one
sentence of shell geometry instead of a number. Bethkenhagen+ 2017's Figure 3 caption names
the model (*"water-only (Redmer et al. 2011)"*), their §2(i) states what the name means
(*"ices are represented solely by a water EOS"* — the ice component's representation, not
the planet's composition; the model is three-layer with an H/He-rich outer envelope), and
Redmer+ 2011 prints the shell boundaries: *"the ionic water shell extending from 0.6 to
0.8 R_p"*. Table 1's shallowest row sits at **0.839 R_U — above the water shell, inside the
H/He-bearing outer envelope**, where ρ = 1.00 g cm⁻³ is the profile's density and could not
be pure water's; our water being +29 % against it is thereby explained. The verdict does not
move (closed, conservative branch; no ternary anchor; C4's tier keeps water + ammonia — that
Table 1 gives no mixture density is now confirmed, not assumed). What moves is the closure's
quality, from *"could not confirm — the anchor cannot be read under either reading"* to
*"confirmed — reading (나)"*, and the failed test's wrong assumption gets its final name: **a
misreading of the profile's name** — "water-only" states the ice component's composition,
not the body's. Redmer+ 2011 comes **off the request list**: not because it yielded the
number, but because the shell-boundary sentence replaced the need for it. All three quotes
verified against the cached PDFs in this session.

### C13 — Does the fuzzy core account for the moment-of-inertia deficit? — **opened 2026-08-31; closed 2026-09-01 as a named refusal: the deficit is real, three axes were measured, and each stops at a boundary this recipe can name**

**Not C5's repair.** C5(a) recorded a graded-Z envelope as *reached, no consumer* — true
when written. What opened this row is a **measurement**: the ice giants' C/MR² sits
−24.3 % / −25.3 % under Nettelmann+ 2013 (P_Voy, R_mean), and **−15.8 % / −11.4 % remains
after the radius is stripped**. A fuzzy core is the candidate whose sign matches — and sign
is not size (C5(b) taught that: the boundary layer had the plausible direction and widened
the residual).

**The target is a derived value, said plainly**: λ is J₂, J₄ and an assumed rotation period
passed through an interior model — matching 0.230 is agreeing with what the gravity field
permits, not matching nature. And N13's own models are three-layer with **rocks confined to
the core**, so the number this row would chase was produced by a model that does not contain
the thing this row would add; λ being gravity-constrained softens that, but any future
"matched by adding what they did not have" needs its own justification, written here in
advance.

**The non-core terms, bounded first** (each ruled out as the owner of the remainder): the
rotation term — our λ is a non-rotating sphere's — is order 1 % by the axial-vs-mean
identity (2/3)J₂ = 0.00234 / 0.00236, with m_rot = ω²R_eq³/GM = 2.95 % / 2.61 % as the
restructuring scale; the rotation-period spread is a **target-side** spread of −3.3 % /
+6.0 % (attribution measured against P_Voy: IAU baseline, normalization-matched, both
papers' default). Together ≲ 7 % against 11.4–15.8 %: a remainder survives.

**The bracket, and why it could not be held.** As briefed: end A = the anchor's compact
central silicate; end B = the same rock mass (5.43 % / 6.07 % of the planet) spread
uniformly through the envelope (`envelope_z` = 0.283 / 0.321, no silicate layer). **End B
refuses at stack build, at any temperature**: with no silicate at the centre the water
column reaches P_c (1220 / 1533 GPa) and the cold-phase pre-check demands the solid
ladder's coverage, whose French & Redmer 2015 evidence span ends at **1000 GPa** — even
though the answer's deep column is fluid (Mazevet) and never touches the ladder there.
Branch 2's registered assumption ("nothing in the recipe caps the outer extreme") is
**false, with the cap named**. Third member of one family in two days (C11's over-broad
refusal, the Queyroux–Neptune route death): **the trial corridor's cold flank demands
evidence the answer never uses.** The analytic ceiling, computed since the engine could not
(all rock at the surface, structure held fixed — assumptions written): Δλ/λ ≤ f_rock/λ =
+31.2 % / +33.7 %, above the required +18.7 % / +12.9 % — so the fuzzy core **cannot be
excluded**, and is not confirmed: the solvable span was never measured.

**Open, with the settling path named**: the cold-flank representability work (route the
over-depth ladder refusal so the temperature loop stays on the fluid side, or teach the
pre-check that a column can be fluid-only where the answer is), after which end B is two
solves. It is the same prerequisite the Queyroux adoption would need — the two owner
decisions share it. **The registered fourth branch — Helled & Stevenson 2017's
ice-envelope applicability — is closed as of survey ⑥ (see C5's correction): there is no
closed form to apply, because that paper disowns its own Gaussian as illustrative and
delivers a formation-history relation instead.**
Both refusals reproduce in ≤ 1 s. No code, no anchor, no gate change.
`engine/fuzzy-core-context-notes.md`.

*Revisited 2026-08-31, same day — the audit overturned "could not be held": end B was
**1 ULP away**, and the bracket is now measured.* The audit's independent construction
(`imf = 1 − (rock+hhe)/m`) leaves a floating-point residual of +5.6e-17 for Neptune — a
ghost silicate stub that occupies the centre, keeps the water column off the 1000 GPa
ladder cap, and lets the cold flank survive: **1 s refusal vs 112 s convergence on one
ULP.** The directing session pre-registered the reading (λ stable across ε → the ε→0
limit; λ moving with ε → artifact) and ran ε = 1e-7 / 1e-9; this session's runner
reproduced every digit (triple complete), added the float-residual point, and retired the
caveats: **λ is stable across nine orders of ε** (Neptune 0.219683 at 1e-9 vs 0.219617 at
5.6e-17, a 3e-4 relative move; Uranus 0.209756 / 0.209749 at 1e-9 / 1e-7 — its
float-residual point does not exist, because 1 − (0.79+2.0)/14.536 leaves a residual of
exactly 0.0 and dies: **the same expression revives Neptune and leaves Uranus dead**,
which is the cold-flank family's strongest exhibit); the ladder wall does **not** press
Neptune's P_c 984 GPa (a probe at 1010 GPa integrates; mass closure 1.000000); grid
1500 → 6000 moves the radius 3.7–3.9e-4, the anchors' own order. **The measured bracket:**

| | I/(M·R_pub²), end A | end B | target (N13, P_Voy) | gap covered |
|---|---|---|---|---|
| Uranus | 0.1937 | 0.2032 (λ 0.2098, R −1.57 %) | 0.2300 | **26 %** |
| Neptune | 0.2135 | 0.2248 (λ 0.2197, R +1.15 %) | 0.2410 | **41 %** |

**The answer this axis gives: rearranging the declared rock mass — any grading between
compact core and uniform envelope Z — buys at most 26 % / 41 % of the gap. This axis
cannot close the deficit.**

> ⚠ **Condition attached 2026-09-01 (Brief 31): these two percentages were measured on the
> clamped table, and they do not survive its repair.** With the 66 repairable clamped nodes
> assembled instead of read, **both ends of this bracket stop converging** (λ −6.9 % / −5.5 %,
> boundary condition missed) — so the bracket **is not measurable at all** on that path. The
> same holds for Brief 26's gradient span: 39.7 % / 60.0 % collapses to ≈3.6 % / ≈1.5 %, the
> wide half refusing. **These are measurements of a table choice, not of the planet.** A number
> that exists on one grounded route and will not converge on the other was never robust to
> that choice. Which route is nearer the truth this experiment does not say — the truth is in
> the original authors' unpublished calculation. Default path unchanged: the repair is an
> opt-in instrument (`engine/hhe_repair.py`), nothing imports it, the baked table still carries
> its 72 clamped cells, the anchors were not refreshed, and both readings are kept side by
> side wherever the numbers appear. **Owner's decision 2026-09-01: the default stays the
> published table** — not because that route is judged nearer the truth, but because there is
> no ground to elect either as truth, and this list's practice when it cannot choose is to
> record the divergence rather than pick (the move C11 made when it published a grid of
> declared pairs and declined to select one).

What this is *not*: a ceiling on the fuzzy core as the
literature means it, which spreads **ice** as well as rock; the recipe's end B moves only
the declared rock. The remaining owners on the table are that difference (graded ice) and
the ice mantle's own density profile — the ice axis stays open, unmeasured. The stub is an
apparatus, not a repair: that the corridor's boundary sits one floating-point digit from
the answer's path strengthens the structural diagnosis (`f3f3a3fd`), and the general fix
remains the shared prerequisite of both pending owner decisions. Bonus, measured on the
way: end B also **shrinks the radius residual** (Uranus +5.48 % → −1.57 %, Neptune
+8.94 % → +1.15 %) and cools the centre (T_c 4953 / 4901 K) — recorded, not attributed.

*Revisited 2026-08-31, later the same day (Brief 22)* — **the stub is retired: end B
solves with no stub at all.** The cold-flank corridor repair (the rules paragraph;
`engine/cold-flank-context-notes.md`) removed the three static spots, and the
pre-registered acceptance passed: both planets solve under **both** `imf` expressions —
Uranus (residual exactly 0.0, the configuration that died) λ 0.209729 · renorm 0.2032;
Neptune (±5.6e-17) λ 0.219577 / 0.219617 · renorm 0.2248 both ways. 1 ULP no longer gates
solvability, only nudging λ by 1.8e-4 relative, inside the ε-ladder envelope. **The
measured bracket stands stub-free: 26 % / 41 % were not stub-dependent** (branch 4 did
not fire). The ice axis (③) is now measurable without any phantom device — which was the
reason ① was ordered before it.

*Revisited 2026-08-31, Brief 23 — **the ice axis, attempted: representable except one
named wall, and no bracket end converges through it.*** The mixing question was answered
from sources first (Soubiran & Militzer 2015: additive volume for H₂O–H₂ measured good to
a few %, ≤10 % locally, over 2–70 GPa × 1000–6000 K; and N13's own envelopes are LM-REOS
*linear-mixed* water — matching like with like), so branch 4 did not fire. The
representation was built (`envelope_z_rock_fraction`, a dispatching `_EnvelopeWater`
part, and **water1's c_P baked** — the source's own Gibbs quantity, closing the hole that
confined C5(b)'s rock mixing to ≥ 2.3 GPa). All four end-B states (ice / ice+rock × two
planets) close mass exactly and **none converges**: a refusal spy shows 1102 of 1202
trial deaths on one wall — **liquid envelope water at p ≲ 0.1 GPa × 500–1000 K**, the
tri-corner of water1's 500 K top, water2's 0.1 GPa floor and Mazevet's 1000 K floor,
which every path cold enough to reach the 76 / 72 K boundary must cross carrying 85 %
dissolved water. Branch 3, refined: blocker named, with a published filler (IAPWS-95 /
IF97 steam covers it) whose baking is an owner decision. **No gap-covered percentage is
reported** — a bracket end that misses the boundary condition by ~1200 K is not a
measured end. Recorded, not judged: all four states sit *above* the targets (renorm
0.2531–0.3061 vs 0.2300 / 0.2410), and the wedge-crossing is partly the uniform-Z
bracket's own artifact — a graded profile tapers the water toward 1 bar and is not
blocked to the same degree. `engine/ice-axis-context-notes.md`.

**The ice axis, attempted twice and measured as a wall both times — 2026-09-01 (Briefs 23, 25).**
Brief 23 put the declared ice into the envelope as a uniform Z; every bracket end refused, and
**1102 of 1202 refusals sat at one water wall** (p ≲ 0.1 GPa × 500–1000 K — the junction of
water1's 500 K ceiling, water2's 0.1 GPa floor and Mazevet's 1000 K floor). Brief 25 baked
IAPWS-IF97 regions 1–3 to fill exactly that window.

**The steam bake did what it was for: the water wall is retired.** In the same solve the spy
now counts **100 refusals, 100 % of them `h_he`, water 0.** But no end converges, so **no
gap-covered percentage exists** and the registered product is the next wall's coordinates.

**Where it moved, and why the target is unreachable.** The surface pins at **355–363 K
regardless of central temperature, against a declared 76 K.** Every trial adiabat cold enough
to head for 76 K dies on the **H/He table's low-temperature floor**, measured here directly
rather than inferred from the refusals:

| pressure | lowest temperature the `h_he` table will evaluate |
|---|---|
| 130 GPa | **1830 K** |
| 150 GPa | 1900 K |
| 164 GPa | 1945 K |
| 1050 GPa | 3130 K |

The refusal samples sit at 131–1121 K in the first band (130–164 GPa) and 1929–3096 K in the
second (~1046–1062 GPa) — **below the floor in both.** So a cold envelope at those depths has
no representation at all, and the 76 K surface is not reachable from below by any central
temperature.

*Corrected 2026-09-01 (survey ⑦) — this was first written as "a material ceiling of the kind
C6 lists". It is not one.* The floor is **our own declared line**, not the source's evidence
limit: `hhe_table.py` carries `REACH_A = 2.7198`, `REACH_B = 0.2567` and the rule
`log T ≥ REACH_A + REACH_B · log P`, whose comment says *"below that a **convecting** envelope
does not reach, and the distributed table's defects (7 sentinel cells in the density slot,
grad_ad clamped to 0.1/0.5) are all down there. We refuse rather than repair — stating the
domain beats touching published numbers."* Evaluated at the five pressures probed above, the
line gives 1830.0 / 1898.5 / 1942.5 / 3128.5 / 3132.3 K — **reproducing every measured floor
point**, residuals 0 to +2.7 K in the direction a 5 K probe step would give. The underlying
table (Chabrier, Mazevet & Soubiran 2019, cached) advertises **10² to 10⁸ K** and our own
baked subset starts at 100 K. **Nothing is missing. We declined to enter.**

*The four ends, recorded and not judged* (λ, then the radius residual, then
`I/(M·R_pub²)`): Uranus B_ice 0.294150 / −10.51 % / 0.2356; Uranus B_both 0.313228 /
−12.81 % / 0.2381; Neptune B_ice 0.299345 / −7.81 % / 0.2544; Neptune B_both 0.305116 /
−5.30 % / 0.2736. All four sit **above** the targets (0.2300 / 0.2410), the same direction as
the earlier attempt with values moved by the surface coming down from ~1275 K to ~360 K.
**None of this is a measurement** — an end that misses its boundary condition is not an end,
and these numbers must not be quoted as the ice axis's coverage.

**The label steam does not buy still rides**: trial paths now *cross* the old wedge on IF97,
and that crossing happens over an unverified additive mixture, outside Soubiran & Militzer's
validated band on both axes (`7769be6e`).

Two defects were found on the way and are registered in the rules above — the re-armed
sentinel that let the temperature loop run 51 attempts against a ceiling of 29, and the
climb that hid the wall from the controller. Both were invisible while every trial died in
the steam wedge first.

**The composition gradient, measured — and the widths that work are the ones that are not
allowed (2026-09-01, Brief 26).** Z(x) as Howard+ 2023's erf, discretised by shell mass. The
implementation's own check came first and passed twice: **width → 0 reproduces the layer stack
bit-identically**, both against the anchor and against a rock-free toy, so the gradient is
continuous with what it replaces rather than a second recipe. It also **clears the wall that
stopped the ice axis** — the uniform-Z end carried heavy material to the surface and dragged
the adiabat under `h_he`'s floor, while a gradient's upper envelope converges to clean H/He
and stays inside the window. That was predicted in Brief 23's landing note and tested here.

**Then the cap excluded the result — and the cap is weaker than "stability".** What route A
actually transcribes is **a description of Vazan & Helled 2020's successful models, not a
stability calculation.** Their sentence, read at its place in the cached text: models matching
radius, luminosity and moment of inertia *"have some **common properties**: in these models the
outer 20% of the planetary radius develop a large-scale convection on top of a stratified inner
region. This convective layer is metal rich for all models except for the two-layer model
(U-1) … heavy-element enrichment of 0.6-0.7."* So the criterion is **"does this look like the
profiles that worked for them"**, not **"is this convectively stable"** — Ledoux is what
*they* used to test survival; the 0.8 R figure is an outcome they observed. The row says so
because the two readings license very different next moves.

Under that criterion, the gradient's span sits below 0.8 R **only at δm_dil = 0.01 and 0.025 —
the two widths that sit on the layer limit and move nothing.** w ≥ 0.05 crosses
0.8 R and w ≥ 0.075 reaches the surface. **Taking route A as transcribed, the reachable
coverage is ~0 %, and the span below is a set of unreachable points.** Route B (deriving our
own ∇X) refuses by name: no radiative gradient exists in this recipe, and the check does not
invent one.

| δm_dil | Uranus renorm | ΔR | Neptune renorm | ΔR |
|---|---|---|---|---|
| 0.01 · 0.025 *(within the cap)* | 0.1937 · 0.1937 | +5.44 % · +5.32 % | 0.2135 · 0.2136 | +8.90 % · +8.78 % |
| 0.05 | 0.1938 | +4.97 % | 0.2137 | +8.37 % |
| 0.075 *(Howard's value)* | 0.1941 | +4.27 % | 0.2140 | +7.58 % |
| 0.125 | 0.1951 | +2.19 % | 0.2153 | +5.50 % |
| 0.20 | 0.1991 | +0.33 % | 0.2200 | **+3.98 %** |
| 0.30 | 0.2081 | **+0.12 %** | 0.2300 | +4.14 % |
| target (N13, P_Voy) | 0.2300 | | 0.2410 | |

All fourteen converged; **no width was adopted** and the observables are reported beside the
grid, never fitted to. The span, if the cap were not there: **39.7 % (Uranus) / 60.0 %
(Neptune)** of the deficit, monotonic in width with no plateau inside the registered grid.
(Neptune's 0.2300 at w = 0.30 equals *Uranus's* target — a coincidence of digits, not a
result.) Shell count is not a knob: 32 → 64 leaves renorm at 0.1941.

**The exclusion's own scope, stated because it bounds the verdict.** The declared family here
is a two-end erf with `z_shallow = 0`; Vazan's stable models put a **metal-rich homogeneous
convective top (Z ≈ 0.6–0.7) above the gradient** — a shape this family cannot express. So the
finding is *"widths that move the answer are outside the cap **for this family**"*, not
*"gradients are unstable."*

**A second product, unasked for: the radius residual collapses.** Uranus **+5.44 % → +0.12 %**,
monotonic. Neptune **+8.90 % → 3.98 % at w = 0.20, then back to 4.14 %** — **non-monotonic,
with its optimum inside the grid**, while renorm rises monotonically for both. So the radius
axis behaves differently from the moment-of-inertia axis, and the two planets behave
differently from each other. Recorded, not judged.

**And the wall the two gradient families died on is one assumption answering two questions
(survey ⑦, 2026-09-01).** The reach line's justification is *"below that a **convecting**
envelope does not reach"*, and it was derived by integrating **adiabats**. Both halves are
statements about a convective, adiabatic envelope.

**A composition gradient is, by definition, stably stratified** — that is what makes it a
gradient rather than a mixed layer — and Vazan & Helled say what follows: *"The heat in a
stable (steep) composition gradient region is transported by **conduction**"*, the layer
*"acts as a thermal boundary to suppress convection and slow down the internal cooling."* A
sub-adiabatic profile is **colder than an adiabat at the same pressure**, so a gradient model
descends below the reach line **on purpose**. That both families died on the same line is not
coincidence: **we asked a question outside the premise of a domain we had drawn from that
premise.**

*This does not make the refusal wrong.* The distributed values below the line really are
damaged — 7 sentinel cells, 887 clamped — and the source calls part of that region
*"unphysical"*, naming solid hydrogen and helium and the breakdown of the Wigner–Kirkwood
expansion, *"identified in Fig. 1 and 16"*. **What changes is the reason attached to the
refusal**: "a convecting envelope does not reach here" stops applying the moment the layer
being carried is stratified. One line is answering two questions, and only one of them is
still its own.

**Settled 2026-09-01 (survey ⑦ addendum): both bands are inside the forbidden region, and
what puts them there is helium, not hydrogen.** The figures arrived (the owner fetched the
paper; the earlier cached copy was an ar5iv conversion whose only two `<img>` tags were the
converter's own logo, which is why the text was readable and the figures were not).

**Fig. 1 and Fig. 16 are not two cuts of one diagram — they are the two pure components.**
Caption 1: *"Temperature-density domain of the present EOS for **hydrogen**."* Caption 16:
*"…for **helium**."* Both end with the same sentence, verified twice in the cached text:
**"The EOS must not be used beyond these limits."** Our table is the Y = 0.275 additive
mixture of those two.

| band | hydrogen's melting line | helium's | verdict |
|---|---|---|---|
| 130–164 GPa · 131–1121 K | ≈870 K at 130, ≈740 K at 164 — the band **straddles**, 81–88 % of its log-T width solid | ≈1180 K at 130, ≈1400 K at 164 — **the whole band sits below** | **solid** |
| ~1055 GPa · 2309–2340 K | Γ_m = 175 line ≈1520 K — band is 1.5× hotter, so **fluid by hydrogen** | ≈4100 K — band is **1.85× colder**, 0.27 dex, several times the error | **solid** |

**Read Fig. 1 alone and the second band answers "fluid".** It is helium that binds it, and
helium is 27.5 % of the mixture. Method, because the numbers are figure reads: vector PDF
rendered at 2400 dpi, measured against tick marks inside the same crop, **± 1 % in pressure
and ± 3.5–5 % in temperature**, with the calibration checked against a printed number — the
surveyor's H₂ melting maximum at ≈80 GPa · ≈1000 K against the text's *"determined
experimentally up to T ≃ 1000 K, P ≃ 100 GPa"*. One corner is left undecided rather than
claimed: band 1's top at 130 GPa (1121 vs 1180 K, inside the error), and band 2's crossing of
the f_WK = 0.7 validity limit (5 % ± 4 %).

**So §5's finding stands and does not open the region.** The reach line's stated reason —
*"a convecting envelope does not reach"* — genuinely stops applying to a stratified layer.
**But a second limit sits in the same place and does not care whether the layer convects:**
the source forbids its own EOS there. **The gradient path is wrong at those cells, and that
reason survives dropping the convective assumption.** Two limits happened to lie close
together and we had been citing the one that does not apply.

*What would settle the remaining corners, and it is arithmetic rather than a search*: the
melting and validity curves are printed as **eqs. (1), (2), (3), (7)**. Evaluating them turns
every ± 4 % above into an exact number. Not yet done.

**Tightened by the printed equations, and one of them has a wrong unit note.** The melting
and validity curves are printed, so the figure reads could be replaced by arithmetic —
reproduced independently by the directing seat.

**Helium, eq. (7): `T_m = 61.0 P^0.639`, followed by *"where the pressure P is in kbar
(= 0.1 GPa)"*. Read that way it gives 5959 K at 130 GPa against a figure read of ≈1180 K —
5× off.** The upstream source settles it, and it was already in our cache from the water
survey: Chabrier cites **Datchi+ 2000**, whose Simon law is `P = 1.6067 × 10⁻³ T^1.565`.
Inverting: **1/1.6067e-3 = 622.394, and 622.394^0.639 = 61.011**, while **1/1.565 = 0.6390** —
the printed coefficient *and* exponent are that inversion to the decimal. Round trip, checked
here: 300 K → 12.096 GPa → 300.01 K; 1000 K → 79.604 GPa → 1000.06 K. And 12.1 GPa at 300 K
is helium's known room-temperature solidification pressure, so it holds physically as well as
algebraically. **The coefficient is right and the unit note is wrong — P is in GPa.** A kbar
reading would require the printed coefficient to be 14.0. The paper is quoted as printed, the
discrepancy is named, and anyone transcribing eq. (7) uses GPa and cites Datchi alongside.
(Second odd printed unit in this paper; no common cause claimed.)

**Hydrogen, eq. (1)** confirms the figure reads to better than 1 % (988.4 K at the 76.3 GPa
maximum; **869.8 K at 130 GPa, 741.6 K at 164** against ≈870 and ≈740 read). **Helium's
equation replaces them**: 1368.2 K at 130 GPa and 1587.1 K at 164, where the figure had been
read as 1180 and 1400 — **12–14 % low against a stated ± 5–7 %.** The surveyor named their own
error bar as optimistic and identified the cause they had already flagged: Fig. 16's axis
labels had to be read from a different crop than the region of interest.

**Effect on the verdict — it strengthens.** Band 1's top corner, previously "5 % below the
line, inside the error", is **18 % below at 130 GPa and 29 % below at 164**. The whole band,
corner included, is solid with room. Band 2's helium margin goes from 1.85× to **2.25×**.

**One limit cannot be closed, and the reason is worth more than the answer.** Eqs. (2) and (3)
— the OCP melting line and the f_WK = 0.7 validity limit — are functions of **density**, not
pressure. Our bands are given in (P, T). Converting needs ρ(P, T), **which is the very table
whose usability at those cells is the open question.** The check requires the object it is
checking. That is the cleanest statement of why this question and the baked-cell count are
two different questions, and it is left undecided rather than forced.

**And counting the baked table turned the second reason false as stated (Brief 29,
2026-09-01).** The reach line's comment gives two grounds; the first was shown not to apply
to a stratified layer, and the second — *"the distributed table's defects are **all** down
there"* — was checked against **our own baked product** rather than the distributed original.

*The two bands were never baked at all.* `KEEP` trims columns per isotherm, and for band A the
kept range stops far short of it; for band B the four isotherms of the fatal point's bicubic
stencil end at 224–794 GPa while evaluation needs 1259 GPa. **The fatal cell is neither
damaged nor sound — it is unbaked**, so the refusal there is the reach line itself, not data.
Sentinels in the baked table: **zero** — all seven sit in trimmed columns. That is registered
branch ④, and it makes *"the table is damaged there"* the wrong sentence: **we did not bake
those cells.**

*But 72 clamped cells survive the bake, and 70 of them sit **above** the line* — inside the
region we use. Reproduced by the directing seat over the baked arrays: 5495 cells kept, 72
with `grad_ad` pinned, **70 above the reach line, 2 below**, every one of them at the **0.1**
clamp end and none at 0.5. The block runs **≈18–112 GPa × 1585–3981 K** — the molecular-to-
atomic transition band, near where Gupta+ 2025 place the fluid structural transition. So the
second reason holds for the sentinels and for the cold pinned mass, and **fails for one block
that lives in the used domain**.

**Tested, and the answer is the uncomfortable middle (Brief 30, 2026-09-01).**

**Contact is universal.** A stencil hook reproducing the baked bicubic's clamped 4×4 was run
over 22 converged points: **every published number in this row reads clamped stencils.**
Anchors **12.1 % (Uranus) / 18.5 % (Neptune)** of envelope `grad_ad` lookups, contact zone
22–37 GPa · 2359–2624 K — the middle of the block. **The rock-axis end B behind C13's
26 % / 41 % : 20.7 % / 26.2 %.** Ice ends 13.2–20.2 %, the whole gradient grid 13.6–20.1 % — **the grid figures reproduced by
the directing seat on the preserved runner, all fourteen points, range identical**.
Branch ① is out. (The first attempt returned zero lookups from a declaration slip in the
runner's own setup; it was discarded and re-run rather than reported.)

**Propagation says the answers hold — with one quantity at the edge.** All 72 cells were
replaced by in-isotherm linear interpolation behind a non-committed hook and **both anchors
were re-solved** — the propagation test that Brief 28's point measurement could not stand in
for.

| | Δλ | ΔR | ΔT_c |
|---|---|---|---|
| Uranus | +9.3e-6 | +9.0e-6 | **+3.41e-4** |
| Neptune | −4.3e-5 | +2.9e-5 | +1.43e-4 |

Against the anchors' own reproducibility (3.7–3.9e-4): λ and R sit 10–40× below it, and
**T_c sits at 0.87–0.92× — inside, but against the wall.** Branch ③ did not fire and
**`--refresh` was not run anywhere**, which is the right instinct: re-freezing on a
substituted table would make the substitution the reference.

**What this does and does not establish, kept together.** It establishes that our published
numbers do not move under *this* substitution. It does **not** establish distance from the
unpublished true values — **the replacement is our own interpolation, not truth**, so this is
a sensitivity to one substitution and not an error bar. And **we are reading clamped values**,
which the answers surviving does not undo: a colder-starting or higher-Z body sits deeper in
the block, and the same test could come out differently. The two runners
(`clamp_contact`, `clamp_propagate`, ~3 min together) are preserved for exactly that re-check.

**Still open, and it belongs to the figures rather than the code**: whether the original clamp
is conservative or violent at those conditions — the block sits in the molecular-to-atomic
transition band, near where Gupta+ 2025 place the fluid structural transition.

*The follow-up as first opened*: the notes' own table has a 60 K-start adiabat passing 100 GPa
at ≈2371 K, which puts a cold-start ice-giant profile **inside the stencil reach of those
pinned rows**. **Whether our anchor integrations read stencils containing a clamped node is
not known and is checkable.** If they do, the adiabatic gradient at those steps is a clamp end
rather than a published value. Verdict-changing if true; opened as its own item rather than
folded in here.

*What was named and not guessed*: **Chabrier's Fig. 1 and Fig. 16**, read as
(log T, log P) coordinates. If the cells we hit lie inside the solid-H/He region, the wall is
physics and the gradient path is wrong there; if they lie merely below our adiabatic cut, the
numbers exist and the question becomes whether the sentinel and clamped cells actually touch
them. The surveyor **did not guess** — the figures are not in the cached text, and the
hydrogen melting curve was not recalled from memory to decide it. Second candidate, unmeasured
because this survey was scoped to literature: whether the damaged cells overlap the two bands
at all (the notes put sentinels at 500–710 K · 8–225 GPa and the clamp at T ≤ 3550 K — the
latter covers both bands).

*And the target passes by a different trade, not a wider table.* Vazan & Helled use **SCvH
(Saumon+ 1995)** — a semi-analytic free-energy model that returns a number everywhere by
construction — while ours is a simulation-assembled table with declared holes. Chabrier 2019
contains SCvH as its own low-temperature component and then spends several sections on where
SCvH disagrees with QMD. **Not a better table: a different bargain.**

**What this leaves the owner.** A gradient that reaches the numbers exists; a gradient that
reaches them *and* resembles the profiles Vazan found workable does not. Two ways forward,
both declarations of their own: **(a)** find or derive an actual stability cap — this recipe
has never had one, and route A turned out to be a family resemblance rather than a criterion —
or **(b)** widen the declared family to `z_shallow > 0`, which **is Vazan's own successful
shape**, and measure again. (b) is the cheaper honesty: it tests our recipe against the
literature's geometry instead of re-drawing a line around our own answer. Fitting the width
to the observables would have produced 39.7 % / 60.0 % and no way to know this — which is
what the method was chosen to prevent.

**Closed 2026-09-01 as a named refusal — the ending the audit proposed and the owner chose.**
`conv=False` reads as *"the solver could not"*; the measurements say something stronger and
addressable, so this row ends the way C6's ceilings do: **with a mechanism and a citation, not
a shrug.**

*The deficit is real and stands*: −15.8 % / −11.4 % after the radius is stripped, against
N13's gravity-constrained λ.

*Three axes were measured, and each stops somewhere this recipe can point at.*

| axis | where it stops |
|---|---|
| **declared rock, redistributed** | Reaches 26 % / 41 % of the gap on the published table — **and that bracket does not exist on the repaired one** (Brief 31). The axis's own ceiling is real; its size is a table choice. |
| **declared ice, uniform envelope Z** | Not measurable. Every bracket end refuses — first at the water wedge (1102 of 1202), then, once IF97 filled it, at `h_he`'s declared reach line. |
| **composition gradient Z(x)** | Built, general, continuous with the layer stack to the bit. Clears the wall the uniform end died on. **The widths that move λ lie outside the geometry Vazan's successful models share**, and the family that does share it (`z_shallow > 0`) cannot reach a 76 K surface at all. |

*And the wall the last two share is now identified to the cell.* It is **our own declared
reach line**, not a source limit — `log T ≥ 2.7198 + 0.2567 log P`, reproducing every measured
floor point. Its stated reason (*"a convecting envelope does not reach"*) **stops applying to
a stratified gradient**, which transports by conduction and is sub-adiabatic by construction.
**But a second limit sits in the same place and does not care whether the layer convects**:
Chabrier's Fig. 1 and Fig. 16 put both bands inside the forbidden region, **helium binding
where hydrogen would have allowed it**, under captions that read *"The EOS must not be used
beyond these limits."* Confirmed by arithmetic on the printed equations, once eq. (7)'s unit
note was shown wrong against Datchi+ 2000.

**So the refusal is chosen, named and cited** — which is this list's definition of finished.
What is *not* claimed: that a fuzzy core cannot account for the deficit. What is claimed is
that **this recipe cannot decide it**, and exactly why.

*Left on the table for whoever reopens it*: the ice mantle's own density profile — the one
named candidate never measured; the unpublished `grad_ad` behind the 66 repairable clamps,
which only the original authors hold; and whether the clamp is conservative or violent in the
molecular-to-atomic band.

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
   항성 나이와 다르고, 거대행성 냉각광도의 실입력이다"*, and `system_age` (`t_sys`, `:85`) is a separate node
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
  with *"r_plts ≳ 30–50 km"* expected (`:88`, `:112`); ²⁶Al half-life **≈ 0.72 Myr** (`:86`) against Monteux's
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
| **② core-side adiabat `Q_ad`** | `cmb_flux.adiabatic_flow` — `4π r² k |dT/dr|_ad`, the flow conduction alone carries, **∝ k** | rises slowly |
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
`:2139` "Radiogenic plus weak tidal heating … enough to drive volcanism, continental drift and a dynamo", `:2259` "fast
continental drift". `bodies/pandora.yaml` gains `dynamo_alive: true` and `stagnant_lid: false` (grade declared, sources beside
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

### C37 — `rotation_period` under three spellings, and a `None` nobody noticed — **listed 2026-09-06**

`dynamo_rocky` asks `state.get("rotation_period")`; bodies declare `rotation_period_h`;
`chain.yaml` names the node's output `rotation_period`. Measured on Luhman 16 A: the declared key is
`rotation_period_h` = 6.94, and `state.get("rotation_period")` returns **None**. So every body has been
handing the rocky ladder a rotation period of `None`.

**It is a one-line bug, not a schema decision.** The sibling `dynamo.py` already reads
`state.get("rotation_period_h")` and works — the answer exists in a module that runs. What is left over
is the graph label, a third spelling of the same field.

⚠ **Nothing has been wrong in any verdict, and that is the uncomfortable part.** `rotation_period_h`
has no consumer inside `dynamo_rocky` — it appears in the signature, in the recorded inputs, and in the
call, and no branch reads it. So the engine has been writing `"rotation_period": None` into its own
evidence record for every body and **emitting no signal at all**, because nothing depended on it. The
first person to be misled would be someone auditing that record later.

**Not fixed here, deliberately.** It landed in the middle of Brief 121, and folding a schema repair
into the placeholder commit would have meant the wiring and a value changed together — exactly what the
A/B for C36 exists to avoid.

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

### C39 — one tidal quality, two ways of getting it — **closed 2026-09-06**

`tidal_heating` takes `k2_over_q` as a **per-body declaration** and the boards carry values;
`tidal_locking` uses the **class band** `Q/k₂` 10²–10³ that its document prints. Same physical
quantity, two sources, so **two nodes can look at one body and see different numbers**.

The values make the point. Hades declares `k₂/Q = 1e-3`, i.e. `Q/k₂ = 1000` — the top of the class
band. **Dante declares 0.0155, i.e. `Q/k₂ = 64.5` — below the band's floor.** ⚠ And it misses on the
same side as Venus: both want a body that dissipates *more* than the class allows. For a tidally
molten moon that is physically reasonable, which is the uncomfortable part — **the class band does not
describe our own roster**, and Venus is then not an isolated failure of that band but the second
instance.

**The shape it took**: whatever was declared wins, and the class band is the fallback — the same
pattern `ω₀` acquired in C36/brief 124. The inversion lives at one named function so the direction
cannot be lost between the two nodes, and the output carries `q_over_k2_source`, which says in words
which of the two the verdict stood on.

**Why it was worth doing, which is not tidiness.** The class band's *ceiling* is the uncertain end,
and it was deciding a verdict on its own. Holding everything else fixed and moving only that ceiling:

| `Q/k₂` ceiling | consistency-window floor | this code's 5 h default |
|---|---|---|
| 500 | 2.30 h | passes |
| **1000** (the document's) | **4.60 h** | **passes, by 8.8 %** |
| 1500 | 6.89 h | ⚠ excluded |
| 2000 | 9.18 h | ⚠ excluded |

**The 5 h default is excluded if the ceiling is under 10 % higher than the printed one** — and the
document prints `~10³`, with the tilde, so no tighter statement is available. A number nobody has
measured for our bodies decides the answer, and it decides it within its own printing error. Every
body that declares its own `k₂/Q` is one body that no longer rests on it.

**What moved on the boards: nothing.** Measured before and after on the two roster bodies that
declare a tidal quality, at the board's own mass and radius:

| body | declared `k₂/Q` | `Q/k₂` | τ before (class band) | τ after (declaration) | verdict |
|---|---|---|---|---|---|
| Dante | 0.0155 | 64.5 | 0.0315–0.315 yr | 0.0203 yr | 1:1 → 1:1 |
| Hades | 1e-3 | 1000 | 0.288–2.88 yr | 2.88 yr | 1:1 → 1:1 |

Against a 5.3 Gyr age, both are decided by the `a⁶` gate with nine orders of magnitude to spare, so
the declaration moves `τ` and moves no verdict. **That is the finding, not a null result** — the
before-and-after was run precisely because a flip would have moved a board value the owner has already
approved, and it is recorded so the next person does not have to re-run it to find out.

⚠ **What the same table shows and the verdict column hides.** Read the two `τ` columns again:

    Dante   0.0315 – 0.315 yr   →   0.0203 yr
    Hades   0.288  – 2.88  yr   →   2.88   yr

**Wiring the declaration turned `τ` from a band into a point, and that point's uncertainty is now
carried nowhere.** Physically it follows — a declaration is one number, so the result is one number —
but Dante's 0.0155 is not a measurement: the board says in its own words that it is *"fitted rather
than predicted"*. While the class band ran, not knowing showed up as a width. It no longer does. **That
is not a cost of this change so much as a thing this change made visible**, and it is C40.

⚠ **Wiring `k₂` from the interior solver is only half a route.** `k₂` follows from structure, but `Q`
is rheology, and Barnes writes that the *"tidal dissipation rate is poorly constrained"*. And the
solver computes neither rigidity nor `k₂` today. A separate item, not this one.

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
`chain.yaml`@«0층. 계산되지 않는 것». **It is not supposed to acquire a recipe.** Ten of the eleven `given`
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
`kind: measured`, `domain: given`, `chain.yaml`@«0층. 계산되지 않는 것», with
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
`chain.yaml`@«0층. 계산되지 않는 것» with `kind: measured`, `domain: given` — the value is *supplied*,
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

### C43 — a disc criterion on a moon, fed by a silent default — **listed 2026-09-07, not started**

Brief 127 asked for something that sounded mechanical: `bindings.yaml` names `semi_major_axis_au` and
the bodies declare `semi_major_axis_km`, so unify them at one named conversion, the way C39 unified
the tidal quality. **The conversion does not exist**, and finding out why turned up something larger.

**The two names are not one quantity in two units.** `bodies/pandora.yaml` declares `kind: moon` with
`parent: Alpha Centauri A b`, so its `semi_major_axis_km` is the orbit **around its planet** — the same
file's `perturber_mass_earth: 120.0` (Polyphemus) confirms which body it orbits.
`body_class`'s `semi_major_axis_au` is the distance **from the star**: its only consumer is
`pebble_isolation_mass`, `body_class.py@«Lambrechts & Johansen 2014 의 페블 고립질량»`, which asks where
in the **protoplanetary disc** a core grew. One key, two frames — and a moon's planetocentric axis
cannot produce a heliocentric distance, because that number belongs to the parent and is not in this
file.

⚠ **What the attempted conversion would have done**, measured before anything was edited:

| `semi_major_axis_au` | pebble isolation mass | boundary verdict for Pandora at 0.6447 M⊕ |
|---|---|---|
| absent → 5 AU default | 20.000 M⊕ | `BELOW` [analog] |
| 252 393 km → 0.001687 AU | 0.00215 M⊕ | ⚠ `INSIDE` [judgment] — stops narrowing |
| moon, boundary skipped (the fix) | — | `INSIDE` [judgment], and it says why |

⚠ **Correction to this row, made after the fix was written.** An earlier draft of this section, and the
message that reported it, called the converted case `ABOVE`. **It is `INSIDE`.** The mass does clear
the isolation mass, but the next gate asks whether it also exceeds twice the maximum core mass
(50 M⊕), and 0.6447 does not — so the boundary returns "no published criterion separates this range"
rather than the opposite verdict. **The error was computing `m_iso` by hand and inferring the branch
from it instead of calling the function**, which is the same defect this file records elsewhere under
a different name. The direction of the finding is unchanged and its size is smaller: the boundary stops
narrowing and its grade drops from `analog` to `judgment`.

**The emitted class does not move** in any of the three — all give `rocky`, `decided_by=radius valley`,
`grade=calibrated`, because that boundary settles Pandora first. **That is luck, not safety**: a
slightly larger moon surfaces it, and even here the wrong reading would sit underneath a correct
answer.

⚠ **The bigger finding is not the naming.** Strip the conversion away and the code still applies a
disc-formation criterion to a moon — and, lacking the distance, fills it in:
`body_class.py@«a = semi_major_axis_au or PEBBLE_ISO_REF_AU»`. **A moon did not grow by accreting
pebbles in the protoplanetary disc**, so the question is not merely being asked with a wrong number;
it is the wrong question for this body, answered from a quiet 5 AU that nobody wrote.

**Three routes, all the owner's**:
1. A moon inherits its parent's `semi_major_axis_au` — the chain already has `scope: parent` edges for
   exactly this shape.
2. `body_class` does not evaluate the pebble-isolation boundary for a moon at all, which may be the
   physically right answer rather than a workaround.
3. Split the names, so the frame is in the name: planetocentric axis versus stellar distance. The most
   honest, and a rename, which is why it was not started at night.

### Resolved 2026-09-07 — route 2, and the naming question dissolves with it

**Owner decision: a satellite does not take the pebble-isolation branch.** Inheriting the parent's
distance was rejected because it still applies a *stellar*-disc criterion to a body that did not form
in the stellar disc.

**What the literature gives, and neither path uses a distance from the star.** Earth's Moon comes from
a giant impact — Canup & Asphaug 2001,
[`2001Natur.412..708C`](https://ui.adsabs.harvard.edu/abs/2001Natur.412..708C) — and the Galilean and
Saturnian systems accrete in a **circumplanetary** disc fed during the giant's own gas accretion —
Canup & Ward 2002, [`2002AJ....124.3404C`](https://ui.adsabs.harvard.edu/abs/2002AJ....124.3404C),
now held. **The disc that matters is the planet's, not the star's.**

`_ice_giant_vs_gas_giant` now returns `INSIDE` with that reason for a satellite, and the recipe passes
`is_satellite=(state.kind == "moon")`. A declared `gas_mass_fraction` still answers the boundary, since
that is a statement about composition and carries no frame.

⚠ **And the `semi_major_axis_au` / `_km` question closes with it.** If a moon never consumes a stellar
distance, there is nothing to fill that key with, and the "which spelling is canonical" question has
no subject. It was never an independent decision.

### The satellite mass budget — recorded, nothing changed

Canup & Ward 2006, [`2006Natur.441..834C`](https://ui.adsabs.harvard.edu/abs/2006Natur.441..834C):
a gas planet's satellite system holds *"a similar fraction of their respective planet's mass
(~10⁻⁴)"*. ⚠ **Read from the ADS abstract, not the paper** — it is not held.

Against Polyphemus at 120 M⊕, from the board's own masses:

| body | board mass | M⊕ | fraction of planet | vs 10⁻⁴ |
|---|---|---|---|---|
| Pandora | 3.850×10²⁴ kg | 0.6447 | 5.37×10⁻³ | **53.7×** |
| Cassandra | 9.000×10²³ kg | 0.1507 | 1.26×10⁻³ | **12.6×** |
| Hades | 5.000×10²¹ kg | 0.0008 | 6.98×10⁻⁶ | 0.1× |
| Dante | 1.552×10²¹ kg | 0.0003 | 2.17×10⁻⁶ | 0.02× |
| Chaos | 5.400×10²⁰ kg | 0.0001 | 7.53×10⁻⁷ | 0.008× |
| **system** | 4.757×10²⁴ kg | 0.7965 | 6.64×10⁻³ | **66.4×** |

**All five are exempt and no value changes**, and the reasons are not the same for all five:

- **Pandora** — the source material fixes it. *"아바타는 설정이 그러니 그대로 두고 기록만"* (owner).
- **Cassandra** — **owner decision, 2026-09-07**: *"카산드라도 면제 및 기록."* A 13× reduction would
  falsify already-approved prose about its surface gravity and density.
- **Hades, Dante, Chaos** — already inside the convention. **There was never anything to exempt.**

⚠ **Two things this table must not be read as saying.**

1. **10⁻⁴ is a budget for the whole system, not a cap per moon.** Singling Pandora out as the body
   that breaks it is **our construction** and appears nowhere in the paper; what the paper constrains
   is the 66.4× on the bottom row.
2. **The scaling is stated for gaseous planets**, and the same abstract says the fraction is *"two to
   three orders of magnitude smaller than that of the largest satellites of the solid planets (such as
   the Earth's Moon)"*. It applies here because Polyphemus is a gas giant — which the engine derives
   independently — and would not apply around a rocky primary.

⚠ **The abstract also names our case directly**: the mechanism *"could limit the largest moons of
extrasolar Jupiter-mass planets to Moon-to-Mars size."* Pandora at 0.6447 M⊕ is well past Mars. **The
exemption is a decision made against a stated expectation, not in the absence of one**, and that is
why it is recorded rather than quietly allowed.

**Going forward**: newly invented moons follow the scaling. The existing five are not revisited.

**Nothing was changed.** The measurement above is the whole of the work.

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

### C37 — one lookup, four names, and a contract check that could not see it — **closed 2026-09-07**

⚠ **First, a correction: there were two spellings, not three.** This file previously counted
`rotation_period_days` among them. It is not a declaration — `bodies/luhman_16_a.yaml` reads
`rotation_period_h: 6.94    # DB rotation_period_days 0.2892`, a comment preserving the source value
next to the converted one, and **no code reads it**. The 24× hazard that name implied never existed.

**The real defect was one lookup.** `dynamo_rocky` read `state.get("rotation_period")`; every supplier
writes `rotation_period_h` — three body files, the sibling `dynamo.py`, and `tidal_locking`'s own
output. So the recipe received `None` **on every body, always**, and wrote that `None` into its
evidence record.

⚠ **Why nothing noticed, which is the part worth keeping.** `check_contracts` compares the document's
`Needs` against `set(result.inputs)` — **the labels a recipe attaches to its evidence, not the keys it
looked up.** `dynamo_rocky` labelled the value `"rotation_period"`, the contract said
`rotation_period`, they matched, and the lookup string was never examined. **A recipe can read a key
nobody supplies and stay green indefinitely, as long as it files the resulting `None` under a name the
contract knows.** That is the mechanism, and it is not specific to this node.

**So the repair is four sites, not one** — otherwise the same trap stays open for whoever reads the
contract next:

| site | was | now |
|---|---|---|
| `dynamo_rocky` lookup | `state.get("rotation_period")` | `state.get("rotation_period_h")` |
| its evidence label | `"rotation_period"` | `"rotation_period_h"` |
| contract Needs (en + ko) | `rotation_period` [h] | `rotation_period_h` [h] |
| `chain.yaml` outputs label | `rotation_period` | `rotation_period_h` |

With label and lookup now one string, `check_contracts` actually covers this node.

**What changed in the answers: nothing.** Measured on Pandora, the only roster body that both reaches
the rocky ladder and has a rotation period to give (32 h, from `tidal_locking`): every emitted value is
identical — `b_eq` 41.3725 µT, `ladder_regime` 1, `dynamo_alive` alive, the same `rossby_verdict`.
Only `inputs` moves, from `None` to 31.999 h.

⚠ **That is not a reason to call the repair empty.** The engine wrote `"rotation_period": None` into its
own evidence for every body it ever judged, and the first person to reconstruct a verdict from that
record would have been reading a lie. **A test now fails if the lookup regresses**, since nothing else
would notice: verified by reverting the key and watching it go red.

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

**The reason is one line in the adapter**: `interior.py@«composition=state.get("composition_intent", "earth_like")»`.
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

Sources of the two windows (printed): Stähler+ 2021 "1830 ± 40 kilometers", "5.7 to 6.3 g cm⁻³" (held);
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

### C47 — the table is fed radiogenic production, and its thresholds are defined on surface heat flow — **measured 2026-09-07, not fixed**

**The question this answers is not "which end", it is "why half".** The low feed gives Earth
41.80 mW/m² where the measurement is 92.1. A factor of two does not look like an inaccuracy, and if a
term is missing then it is not something to choose between — it is something to fill.

**What the code is actually fed, read from `chain.yaml` rather than assumed.** `heat_transport_mode`
has exactly **two** incoming `requires` edges: `tidal_heating` → `surface_flux` and
`internal_heat_nontidal` → `radiogenic_power`. The second edge's own note says the judgement is made
on *"the whole radiogenic output (l_int = radiogenic_power) plus the tidal flux"*. **There is no
secular-cooling edge, and no node in the chain emits such a value.**

**What the thresholds are defined on, from both papers.** Reese+ 1998: *"the critical **heat flux**
which can be removed without widespread melting"*. Lourenço+ 2020 §4.3: *"the **total surface heat
flow** (i.e., the sum of magmatic and conductive heat flows)"*. Both are surface heat flow. So the fed
quantity and the threshold quantity are not the same physical quantity.

**Two bodies, measured.** Earth alone cannot settle this, because Earth is the only body with a
measured surface flux sitting beside our number.

| body | our low feed | that body's **radiogenic production** | ours ÷ radiogenic | that body's **surface heat flow** | ours ÷ surface |
|---|---|---|---|---|---|
| Earth | 41.80 mW/m² = **21.32 TW** | Korenaga 2008 §41: BSE **16 ± 3 TW**; §2's sketch says *"about 20 TW"* | **1.33×** (1.12–1.64 across 13–19 TW); **1.07×** against the sketch | Davies & Davies 2010: **47 ± 2 TW** = 92.1 mW/m² | **0.45×** |
| Mars | 15.87 mW/m² | Parro+ 2017: **14.3 mW/m²**, Wänke & Dreibus composition | **1.11×** | Parro+ 2017's own model: **19 mW/m²** (range 14–25) | **0.84×** |

⚠ **Verdict: (b) — a different quantity, not an inaccurate one.** It agrees with radiogenic production
on both bodies to within 11–33 % and misses surface heat flow by factors that differ *between* the
bodies. An inaccurate surface flux would miss by a similar factor on both.

**⚠ Which is why no multiplier is allowed here, and the reason is quantitative.** The gap between the
two quantities is the **Urey ratio**, and it is a property of the body:

| body | Urey ratio, and whose | `1/Ur` |
|---|---|---|
| Earth | **0.35**, Korenaga 2008's bulk-Earth value (= 16/46 TW, which this seat reproduced by arithmetic); our own 21.32/47 gives 0.454; his **convective** Urey ratio is 0.23 ± 0.15 and is a different quantity again | **2.2–2.9** |
| Mars | **0.68–0.75**, Parro+ 2017 (0.715 at 20 mW/m²); convective-history models give 0.52–0.62 and 0.594 ± 0.024 | **1.3–1.5** |

**A single constant cannot serve both**, and the two bodies we can check are the two that disagree most.
Multiplying Earth by ~2 to seat it at 90 mW/m² is the exact defect class this ledger spent 2026-09-07
removing.

**What the missing term is, in the source's words.** Korenaga 2008 §2: *"Loss of internal energy is
balanced primarily by (1) heat production from radiogenic elements and (2) a decrease in the primordial
heat content of Earth (i.e., secular cooling)… Other energy sources such as tidal dissipation are
negligible compared to these two processes"*, and *"the present-day internal heat production is about
20 TW …, so the rest of the surface heat flux must be from secular cooling."* Parro+ 2017 says the same
of Mars in the other direction — Ur near 0.7 means *"a relatively small difference between the total
radioactive heat production and heat loss through the surface, and therefore a **moderate** contribution
from secular cooling."*

⚠ **Our own document already names the term.** §6 of `tidal-heating-methodology.md`: *"Note that tidal
heating is one heat source among several (radiogenic, **accretional, primordial**)."* Four sources are
named in our text and the chain feeds two of them. This is not an undiscovered gap; it is an unfilled
one.

⚠ **And that same sentence carries a second defect.** It continues: *"For an Earth-mass body radiogenic
heating alone is ~0.08 W/m²; tidal heating matters when it exceeds that."* The figure is **uncited**,
and it is **2.1× both held estimates** of Earth's radiogenic production (Korenaga's 16–20 TW =
0.031–0.039 W/m²; our own engine 0.0418) while being **87 % of Earth's measured total** (0.0921). It
sits with the totals, not with the components. ⚠ **It is also one of C34's four candidates** — listed
there as *"0.08 §6.1"* — so one of the four values that decision was choosing between is a figure whose
own label is in doubt. Not repaired here; its source has to be found first.

**⚠ What this does to C34's score, and it is not a small correction.** At the low feed Mars passed and
Earth failed. That difference is **not** evidence about the fed quantity — it is a measure of how close
each body's Urey ratio is to 1. Mars's 0.68–0.75 means a radiogenic number fed into a surface threshold
still lands in the right cell; Earth's 0.35–0.45 means it does not. **The 3-of-4 was scoring the Urey
ratio.** Mercury and Venus have no measured surface heat flow, so they cannot even be checked this way.

**⚠ Not fixed, and wider than C34.** The same shortfall applies to **every body this engine feeds**; it
is visible only on Earth and Mars because only they have an independent number beside ours. Filling it
needs a grounded secular-cooling recipe — a cooling rate times a heat capacity times a mass, of the
shape Korenaga's own eq. (8) uses (`C dTi/dt = H(t) − Q(t)`, with `C = 7×10²⁷ J K⁻¹` for the whole
Earth) — not a factor. ⚠ *The `eq. (8)` pointer itself is confirmed, not stale: C47 (b) item 1 shows
C20's mantle equation **is** that equation (`C dT/dt = H − Q` with `C = M_m C_pm`). What was stale here
is the number beside it.* C20 (`core_thermal_history`) already emits `q_cmb_present` **3.745 TW** for
Earth (⚠ **5.07 TW until 2026-09-09** — that was the `H` = 1.5 pW/kg value, and owner decision ⑤ moved
it twice in one day; Briefs 166 D/E),
but that is the core's contribution across the CMB, not the planet's secular cooling, so it does not
close this on its own. **The low/high choice in C34 stays the owner's, and this section exists so that
it is made knowing the low candidate is a different quantity rather than a smaller one.**

### C47 (b) 2026-09-07 — the integrator was opened first, and the two-body condition fails on the ordering

**The instruction was to look before building, and looking changed the answer twice.**

**Answer to the three-way question: (ii) for the cooling rate, and *already an output* for the thing
C47 actually needs.**

1. **C20's mantle equation *is* Korenaga eq. (8).** `engine/core_history.py` line 8 prints it:
   `mantle (eq. 32)   H_m M_m − Q_M + Q_C = M_m C_pm · dT_h/dt`. That is `C dT/dt = H − Q` with
   `C = M_m C_pm`. The integrator has been solving this equation since 2026-09-04.
2. **`dT_h/dt` is computed and not emitted** — the output list carries `dtc_dt_present_k_per_gyr`,
   which is the **core**'s rate. So the mantle rate is case (ii), inside and unpromoted.
3. ⚠ **But promoting it is not needed, because the surface flow is already an output.**
   `q_mantle_present` **is** `Q_M = 4π R_p² F_t`, from `mantle_flux.implied_flux` (Nimmo+ 2004 eqs
   34–36). The quantity C47 was going to build already exists and is already emitted. **Guardrail ①
   (fix `C` from the paper) is therefore moot for this route** — no `C` is used.
4. **Guardrail ③ holds.** `implied_flux(t_m_k, g, r_m)` takes a mantle potential temperature, gravity
   and radius. **No measured surface heat flux enters anywhere**, which is what the guardrail asked.

⚠ **And our own module diagnosed C47 sixteen days ago.** `engine/mantle_flux.py`'s header, written at
Brief 46: *"The implied flow and the radiogenic budget are not required to match; **secular cooling is
the expected difference** (the paper: Earth 'loses heat roughly twice as fast as it is being generated
by radioactive decay')."* That is C47's whole finding, in our own code, citing Nimmo for it — the
**third** independent place this was already written down, after §6's *"accretional, primordial"* and
Korenaga's own §2. The consumer never read any of them.

**The pass condition, measured.** One recipe, `Ur = radiogenic / implied_flux`, no per-body adjustment,
default concentration set:

| common `T_m` | Earth `Ur` | Mars `Ur` |
|---|---|---|
| 1603 K (Nimmo's own printed present-day Earth value) | 0.537 | 0.317 |
| 1700 K | **0.353** — Korenaga's 0.35 almost exactly | **0.209** |
| **published** | **0.35** (Korenaga, 16/46) | **0.68–0.75** (Parro+ 2017) |

**Earth can be landed. Mars misses by 3.4×.** ⚠ **And the failure is in the ordering, which no choice
of `T_m` repairs.** Earth → Mars under this law:

| quantity | Earth | Mars | factor |
|---|---|---|---|
| `δ_t` top boundary layer | 41.1 km | 56.8 km | **×1.38 thicker** (`δ ∝ g^−1/3`) |
| `F_t` | 118.3 mW/m² | 85.7 mW/m² | ×0.72 |
| `Q_M` | 60.4 TW | 12.4 TW | ÷4.88 |
| `H` radiogenic | 21.3 TW | 2.58 TW | ÷8.27 |
| **`Ur = H/Q_M`** | | | **falls ×1.69** |

The literature has `Ur` **rise** ×2.0 from Earth to Mars. **A recipe that reverses the direction is not
off by a constant, and the two bodies we can check are the only two we can check.** To pass, Mars would
need `T_m = 1419 K` against Earth's 1702 K — **283 K colder, chosen because it makes `Ur` come out.**
That is per-body tuning wearing a physical name.

⚠ **Why it inverts, in our own docstring's words.** `mantle_flux.py`: the parameterisation was tuned on
four simultaneous **present-day Earth** constraints — *"the present-day mantle temperature, viscosity
and heat flux"* — plus densities adopted to match PREM. Eight Earth constants ride along (`ρ_m`,
`α_m`, `κ_t`, `k_t`, `η₀`, `T₀`, `ζ`, `Ra_c`), and `T_s = 293 K` is *"the one constant here that is
obviously not the roster's."* **It is a mobile-lid boundary-layer law, and Mars is the archetypal
stagnant lid.**

⚠ **A source already on our own ladder falsifies it outright.** `implied_flux` gives Mars
**85.7 mW/m²** at `T_m = 1700 K`. Reese+ 1998's ceiling for Mars is **15–30 mW/m²** — the very number
that is the bottom of the C46 ladder. So **our own ladder says this law hands Mars 2.9–5.7× more heat
than its lid can conduct without widespread melting.** Meanwhile Parro's measured-model 19 mW/m² =
2.74 TW sits **inside** Reese's 2.17–4.33 TW. The stagnant-lid law and the measurement agree with each
other; the mobile-lid law agrees with neither.

⚠ **A hard blocker on the (i)/(ii) route independent of all of the above.** Only
`engine/bodies/earth.yaml` declares `core_initial_temperature` and
`mantle_initial_potential_temperature`. **C20 cannot run on Mars at all**, so the two-body condition
cannot be scored through the integrator even if the physics were right.

**⚠ And the loop closes on C46.** The right surface flow needs the **regime** — mobile-lid bodies take
Nimmo eqs 34–36, stagnant-lid bodies need a stagnant-lid law — while C46 needs the surface flow to
place the cell. C46 already recorded that flux cannot supply the regime, and that Lourenço's
discriminants are mobility and plateness, both outputs of a 4.5 Gyr simulation. **So C47 is not
blocked on writing code. It is blocked on the same circularity C46 named, and closing one closes the
other.**

**What would actually unblock it, stated as a request rather than a build.** The stagnant-lid
scaling is Reese, Solomatov & Moresi 1998's own subject — *"thermal boundary layer analyses as well as
finite element simulations of stagnant lid convection with non-Newtonian viscosity"* — and ⚠ **we hold
only its abstract; every AGU and ADS scan returns 403.** The abstract prints the two ceilings and not
the scaling law. **Nothing is built here because the half of the physics that Mars needs is in a paper
we do not have.**

**Nothing was changed in the engine by this section.** No node, no edge, no value. Item B of the
brief — no regime name is emitted while this stands — is already the state of the code: `solve_mode`
emits `regime_candidates` and refuses a single regime whenever more than one stands.

### C47 (c) 2026-09-07 — the stagnant-lid law was read, and the mobile/stagnant distinction is not what was breaking C47

**A paper was found on an open route and read from source. It changes the diagnosis, and it does not
close the item.** Korenaga 2009 ([`2009GeoJI.179..154K`](https://ui.adsabs.harvard.edu/abs/2009GeoJI.179..154K)),
*"Scaling of stagnant-lid convection with Arrhenius rheology and the effects of mantle melting"* — same
author as the Urey-ratio review this project already cites for C47's Earth numbers, adjacent year.

**⚠ First correction: the law is not eq. 30.** The brief identified eq. 30 as the scaling law. The
paper's §4 says the opposite in its own voice — *"The boundary-layer stability criterion (**eq. 43**)
is used to calculate `Nu`"* — and describes eq. 30 as *"**the conventional scaling** of `Ra_i^{1/3}`"*
that its results *"deviate considerably from"*. **Eq. 30 is the law this paper argues against.** Its
contribution is that mantle melting *"may reduce the conventional prediction of surface heat flux by up
to a factor of ∼5–10"* (Summary, read in full).

**⚠ Second, and this is the finding: the conventional stagnant-lid law fails the direction test, and
fails it *identically* to the mobile-lid law we already had.** Eq. 30 is
`Nu ≈ a θ^(−1−β) Ra_i^β` with `a ≈ 0.30 + 0.25n` and `β = n/(n+2)`, `Ra_i` from eq. 21 (Arrhenius),
`q = Nu k ΔT / D` from eq. 19. Evaluated with the paper's own constants and **one shared `b`**, at a
common `ΔT` and `T_i`:

| law | Mars/Earth surface flux | `Ur` Earth → Mars | needed |
|---|---|---|---|
| Nimmo eqs 34–36, **mobile lid** (what we had) | **0.724** | falls ×0.59 | — |
| Korenaga eq. 30, **stagnant lid**, `n = 1` | **0.723** | falls ×0.59 | rises ×2.0 |
| Korenaga eq. 30, **stagnant lid**, `n = 3` | 0.557 | falls ×0.77 | rises ×2.0 |

⚠ **0.724 and 0.723 are the same number, and it is not a coincidence.** Both laws put the flux at
`q ∝ g^{1/3} ΔT^{4/3}` for `n = 1`: the boundary layer thickens as `g^{−1/3}`, and **`D` cancels
analytically** out of `q = Nu k ΔT/D` for every `n`, because `Ra_i ∝ g ΔT D^{(n+2)/n}` raised to
`β = n/(n+2)` returns exactly one factor of `D`. **So swapping a mobile-lid law for a conventional
stagnant-lid law changes the Earth→Mars ordering not at all.** The mobile/stagnant distinction was the
wrong suspect — C47 (b) named it as the cause and that was too quick.

**What does carry the direction is the melting correction**, and the paper says so in its own §4.2:
mantle melting *"starts to affect heat-flow scaling at **lower temperatures for Mars than Earth**
because the **low gravity of Mars results in the formation of thicker depleted mantle** for a given
potential temperature."* Suppressing Mars's flux harder than Earth's is exactly the direction `Ur`
needs. ⚠ But that is eqs 41–56 solved iteratively with `z*_D = Nu^{−1}`, not a formula to transcribe —
**it is a build, and nothing was built here.**

**⚠ Third, and it is a harder stop than the direction: this law cannot give an absolute Urey ratio
either, by the author's own statement.** From p. 163, verified on the page image rather than the text
layer:

> *"the pre-exponential factor `b` in eq. (1) is determined so that the surface heat flux is
> **50 mW m⁻²** at the present-day Earth condition … **different planets may take different
> pre-exponential factors** … The purpose of this **(arbitrary) normalization** for mantle rheology is
> to provide a simple reference point and highlight differences caused by mantle melting and the size
> of a planet."*

And the Earth it normalizes to is **counterfactual**: *"Earth does not presently exhibit stagnant-lid
convection … it is convenient to use this familiar planet first to derive a **hypothetical** heat-flow
scaling law, **against which results for other planets may be compared**."* The 50 mW/m² is not
Earth's measured 92.1. **So the absolute scale is free per planet, declared arbitrary, and anchored to
an Earth that does not exist.** Choosing `b` per body to land the two Urey ratios is the per-body
tuning guardrail ④ forbids — with a citation attached, which makes it worse rather than better.

**⚠ The pass condition is therefore not obtainable from this paper.** Not because its physics is wrong,
but because it is built as a **relative** comparison instrument and says so.

**The reserve law was given a qualification check only — not a fit.** Foley & Bercovici 2014
([`2014GeoJI.199..580F`](https://ui.adsabs.harvard.edu/abs/2014GeoJI.199..580F), ⚠ **arXiv eprint; its
page and equation numbers are not the journal's**) was opened for one question: does it carry a
constant fixed by calibrating to Earth? **It does not** — its exponents come from least-squares fits to
its own numerical experiments. And its abstract claims the shape C47 actually needs: scalings
*"across the stagnant lid and plate-tectonic regimes"*, i.e. **a law that does not require the regime
as an input.** ⚠ It has freedom of its own kind (grain-damage material parameters, and it *"treat[s]
the plate length as an unknown"*), and evaluating it is a build. **It was not fitted, and no number was
taken from it**, because brief 145's own warning applies: trying two laws and keeping the one that
lands is per-body tuning wearing two citations.

**The knot, written in both places it binds:** *a correct surface heat flow needs the regime, and placing the regime needs the surface heat flow.* ⚠ **And the stagnant-lid
law does not cut it** — that was the hope this section tested and removed. A law that spans both
regimes would, which is why Foley & Bercovici is the one worth a build if the owner spends one.

**Nothing was changed in the engine.** No node, no edge, no value, no constant transcribed.

### C47 (d) 2026-09-08 — the declared-regime path already exists, runs the other way, and the law contradicts the declaration it would serve

**Guardrail ① asked for a sweep of the grade names before a fifth one was coined. The sweep found the
word already in use, and then found the module that uses it.**

**The vocabulary, swept.** Four axes, and they do not collide:

| axis | words | where |
|---|---|---|
| `Result.grade` | `measured` · `calibrated` · `analog` · `judgment` · `authored` | `payload.GRADES` |
| `Band.value_origin` | `printed` · `chosen` | `bands.py` |
| `Band.pick` | `printed` · `chosen` · `unchosen`, plus `provisional` as a fourth pick word | `bands.py`, `provisional.py` |
| ladder rung origin | `analogy-rung` · `abstract-level` · `held body text` | `tidal_heating.py` |

⚠ **A fifth word is not needed, because `declared` already exists.** `engine/tidal_transport.py` has
carried `mode=dict(value=mode, provenance="declared")` since **Brief 35, 2026-09-01**, on a `provenance`
axis of its own. Coining a grade for declared regimes would duplicate a word this engine has been using
for a week.

⚠ **And the sweep turned up an inconsistency this seat made yesterday**: `REGIME_LADDER`'s third rung
origin is the bare literal `"held body text"` while its two siblings are named constants
(`ANALOGY_RUNG`, `ABSTRACT_LEVEL`). Three origins, two of them named. Not repaired in this section —
recorded so it is repaired deliberately rather than noticed again.

**⚠ The bigger find: D is already built, and it runs the other way.** `engine/tidal_transport.py`,
Brief 35, opens with *"Ė → (internal temperature, lithosphere thickness) under a **DECLARED** transport
mode"* and argues D's exact case — *"수송 모드는 **선언**이고 도출이 아니다"*, citing Kankanamge & Moore
2019 §6 doing the same thing (*"the internal heating rate is chosen to satisfy the observed thermal
emission"*). Its `TRANSPORT_MODES` are `heat-pipe`, `stagnant-lid`, `plate-tectonics`.

But three things separate it from what D needs:

1. ⚠ **The flux is an INPUT, not an output.** It takes `surface_flux_wm2`, sets `H = F_s / D`, and
   returns internal temperature, lithosphere thickness, and the melt/conductive **split** of the flux it
   was given. **Flux in, state out.** D asks for regime in, flux out — the opposite direction.
2. ⚠ **Only `heat-pipe` is solved at all.** `stagnant-lid` and `plate-tectonics` return
   `internal_temperature=None` with the module's own note that other modes are *"§6.2의 용량 사다리로
   판정만 한다"* — judged by the ladder, not converted. **The two regimes C47 needs are the two it does
   not solve.**
3. ⚠ **Its verification status is `failed-io-reproduction`, and its numbers are marked 채택 금지.** The
   transcription is verbatim and solves to ~10⁻¹⁴ residual, but Kankanamge & Moore 2019 cannot reproduce
   its own printed Io result (1471 K, 12.6 km) from its own printed constants; back-solving the constants
   that make it a root gives `α = 8.71×10⁻⁷ K⁻¹` — **1/34 of rock's** — and `ΔT_rh = 354 K` against a
   rheological scale of 40–100 K.

**The `b` question, answered — and the answer is what stops D.** Guardrail: an absolute flux from the
declared path needs `b` fixed, or the regime refuses flux. **It can be fixed**: take Korenaga 2009's own
`b`, re-fitted on the paper's own printed Earth condition using the paper's own printed constant list
(including its `α`, self-consistently — see paper defect #24), as **one global declaration** for every
body. That is not per-body tuning; it is the same shape as `mantle_flux`'s `T_s = 293 K` or
`radiogenic`'s `MANTLE_SHARE = 0.70`, both of which are Earth's numbers declared for every rocky body.
⚠ Its width is **unquantified by the paper** — *"different planets may take different pre-exponential
factors … grain size and mantle composition"*, with no range printed — and `q ∝ b^{−β/n}`, so a decade
of grain size is **2.15×** in flux at `n = 1`.

**⚠ But at that normalization the law contradicts the declaration it is being asked to serve.**

| body declared **stagnant-lid** | eq. 30 flux | against Reese's stagnant ceiling 10–30 mW/m² |
|---|---|---|
| Earth-size | **50 mW/m²** (by construction) | **1.7× the top, 5.0× the bottom** |
| Mars-size | **36 mW/m²** | **1.2× the top, 3.6× the bottom** |

**Declare "stagnant lid", compute the flux, and C46 answers that the body cannot be a stagnant lid.**
The declaration and the law disagree, so D's flux path would emit a value that its own consumer
rejects. That is not a number worth emitting.

**⚠ And the repair is in Korenaga, not in Foley & Bercovici — which is the reason to stop and report.**
The paper's advertised contribution is that mantle melting *"may reduce the conventional prediction of
surface heat flux by up to a factor of ∼5–10"*. Apply that:

⚠ **Corrected 2026-09-08, same seat, a few hours later — the table below originally read the ÷5–10 as
a two-sided interval and it is an upper bound.** The paper's words, in both places it says this
(Summary and §5), are *"could reduce the conventional prediction of surface heat flux **by up to** a
factor of ∼5–10"*, and it is prose summarising Figs 12–13, not a printed range of computed values. **A
reduction of *at most* 5–10× means the reduced flux lies somewhere in `[q/10, q]`** — it does not mean
the flux is `q/10` or `q/5`. Reading "up to X" as an interval and then taking its ends is the same
error class as C46's ceiling-used-as-floor, made by this seat hours after repairing that one.

| body | eq. 30 | what the paper's *"up to ∼5–10"* actually licenses | ceiling 10–30 |
|---|---|---|---|
| Earth-size | 50 | somewhere in **5.0 – 50 mW/m²** | **may** reach it; not delivered |
| Mars-size | 36 | somewhere in **3.6 – 36 mW/m²** | **may** reach it; not delivered |

**So the melting correction permits the ceiling to be satisfied and does not deliver it.** The
conclusion below survives — Korenaga is the remaining candidate and C47 (c) tested the wrong equation —
but it survives as *the only unexhausted route inside this paper*, not as a route already shown to
land. ⚠ **Korenaga 2009 is not exhausted: C47 (c) tested only the law the paper argues *against*.**
Eq. 43 with
the melting correction (eqs 41–56, solved iteratively with `z*_D = Nu^{−1}`) is the paper's actual law,
and it is the single build that serves **both** open paths — D's flux output, and the direction test
that C47 (c) ran on the wrong equation.

**Nothing was built, and nothing in the engine changed.** Per brief 146's own instruction: a reason
appeared to change the order, so this stops here. **The proposed order is: Korenaga eq. 43 + melting
first** (it serves D and re-runs A's test on the right equation), with Foley & Bercovici held as the
genuinely independent third family for the pre-registered "three families, same direction" verdict.

⚠ **Closed 2026-09-08 by a fourth family, not a third.** Korenaga eq. 43 with melting was built (C47 (e)
→ (k)) and it fails in the same direction as the other three: `q_E/q_M` reaches **1.5114** against the
**3.68 / 4.78** the Urey ratios need. **So the verdict this note was waiting for is in, and Foley &
Bercovici was never needed to reach it** — four families, one direction. *(C47 (g)'s cell calls this
"the note in C47 (c)"; it is this paragraph, in C47 (d).)*

### C47 (e) 2026-09-08 — the law was read before building, and the build is C20-sized

**Brief 147 put one step in front of the build: read, size it, then decide. This is the size.**

**The chain, counted.** Korenaga 2009's actual law is not one equation:

| what | equations | note |
|---|---|---|
| Arrhenius correction to `θ` | 39, 40, **41** | `θ_eff = (c₁c₂)^{1/2}`, a geometric mean of two correction factors, *"c₁ tends to be too low for higher n whereas c₂ too high"* |
| local Rayleigh number | **42** | `Ra_l(δ) = Ra_i · max[ δ_eff^{(n+2)/n} T*_eff / η*_eff ]` — a **maximum over sublayers**, with `η*_eff` a **logarithmic average** |
| stability criterion | **43**, 44 | `Ra_l(δ) = Ra_crit(n)`, `Ra_crit(n) ≈ exp(3.84 + 2.25/n)`; `Nu = δ^{−1}` |
| dry solidus | **45** | `P₀ = (T_p − 1150)/100`, Takahashi & Kushiro 1983 |
| depth-dependent viscosity | 46, **47** | a step: `1` below `z*_D`, `Δη` above |
| density stratification | **48**, 52 | and eq. 52 is a **second branch** for when `Nu > 1/z*_D` |
| compositional buoyancy | **50**, 51 | `dρ/dF ≈ −1.2 kg m⁻³ per per cent` (Korenaga 2006), and a mean degree of melting |
| equivalent temperature contrast | 53, **54** | `T*_ρ`, how the density contrast enters as a temperature |
| the outer solve | **56** | `Nu = F_Nu(n, E, T_s, ΔT, Ra_i, Δη, Δρ, z*_D)`, iterated by setting `z*_D = Nu^{−1}` when `Nu > 1/z*_D` |

**Fourteen equations, and three nested numerical levels** — a maximization over `δ_eff` inside a
root-find for `δ` inside a fixed-point iteration on `z*_D`. ⚠ **That is C20-sized**, not a
transcription: `core_history.py` is the closest thing this engine already has to it.

**⚠ Two declared inputs we would have to supply, and one of them comes from a figure.**

- `Δη`, the dehydration viscosity contrast: §4 **sets it to 10²**, while §3 reports experiments
  suggesting *"a factor of ∼10³ increase in viscosity due to dehydration"* for diffusion creep. Printed
  ends, different values, no election — **a C32 band, not a constant.**
- `Δρ`: §4 says *"compositional buoyancy is calculated based on **Fig. 11**"*. ⚠ **An input read off a
  graph.** Everything else here is a formula; this one is not.
- Also declared and ours to carry: melt productivity `(dF/dP)_S = 15 %/GPa` (Korenaga 2006) and
  `P_f = 0`, *"for simplicity"*.

**⚠ What we already hold — and the honest answer is nothing that fits.** Brief 147 asked this first
because two builds today turned out to exist already. This one does not.

| candidate | what it is | verdict |
|---|---|---|
| `eos.py`'s `silicate_solidus(p, variant)` | melting **temperature as a function of pressure**, Andrault+ 2011 A-chondritic/peridotitic | ✗ **the inverse quantity from a different source.** Eq. 45 gives the **pressure at which a mantle of potential temperature `T_p` begins to melt**. Substituting ours moves the paper's own depleted-layer depth |
| `mantle_flux.py`'s `viscosity()` | `η₀ exp(−ζ(T − T₀))`, **linear-exponential**, Nimmo eq. 35 | ✗ **this is the rheology the paper argues against.** Korenaga 2009's subject *is* Arrhenius versus linear-exponential, and its eq. 21 carries `exp[E/(nRT_i)]` |

⚠ One thing does come free from the comparison: Nimmo's `ζ = 10⁻² K⁻¹` gives `θ = ζΔT = 13.5` at
`ΔT = 1350 K`, and Korenaga's Table 2 lists `θ` from **7.93 to 15.11** across `Δη = 3–30000`. **The two
papers' `θ` mean the same thing and sit in the same range** — a free consistency check between two
independently transcribed modules.

**⚠ Reproduction anchors — and this is where it is stronger than the last transcription this engine
tried.** `tidal_transport.py` carries `failed-io-reproduction` because Kankanamge & Moore 2019 cannot
reproduce its own printed result. Korenaga 2009 offers three checks, and two already pass:

| anchor | status |
|---|---|
| §4.1's printed *"`Ra_i` varies from ∼10⁹ to ∼10¹³"* over `T_i` 1200–1800 °C | ✅ **passes** — this seat's transcription gives **1.26 × 10⁹ → 2.27 × 10¹²**. ⚠ Note `Ra_i` at the Earth condition is pinned by `q = 50 mW/m²` alone, so this tests the `θ`/`Ra_i`/`Nu` chain and says nothing about `α` |
| eq. 44's `Ra_crit(n)` against the text's *"∼450 (n = 1), ∼134 (n = 2), ∼104 (n = 3)"* | ✅ **passes at n = 1 and 3** — `exp(3.84 + 2.25/n)` gives 440 and 98.5. ⚠ `n = 2` gives 143 against ∼134, **7 % off** |
| **Table 2**, which prints per-row `θ`, `Ra`, `Nu`, `δ` for `Δη = 3 … 30000` | **the real anchor, unused so far** — row-by-row numbers for exactly the stability analysis eq. 43 performs |
| §4's dimensional planetary results | ⚠ **Figs 12–14 only.** No printed dimensional flux to check against, so the absolute scale has no anchor — consistent with C47 (c)'s finding that the absolute scale is declared arbitrary |

**Size verdict: a multi-session build with a good row-level anchor and no absolute-scale anchor.** The
stability analysis can be verified against Table 2 row by row; the dimensionalized planetary flux
cannot be verified against anything the paper prints.

**⚠ And the guardrail check found an error in this seat's own C47 (d), corrected there.** The
*"÷5–10"* is **prose, appearing twice** (Summary and §5) and reading *"could reduce … **by up to** a
factor of ∼5–10"* — a summary of Figs 12–13, not a printed range of computed values, and an **upper
bound on the reduction**. C47 (d) put ÷5 and ÷10 at the ends of an interval and observed that both
landed under the ceiling. **An "up to" is one-sided**: the reduced flux lies in `[q/10, q]`, so the
melting correction **permits** the ceiling and does not deliver it. Reading a bound as an interval and
taking its ends is the same error class as C46's ceiling-used-as-floor, repeated by the same seat a few
hours after repairing it. **The conclusion that Korenaga is the remaining unexhausted route stands; the
claim that it already lands does not.**

### C47 (f) 2026-09-08 — step 1 passes: the transcription reproduces the only row-level anchor this engine has

**Built: `engine/stagnant_lid.py` + `engine/test_stagnant_lid.py`, wired into the gate.** Brief 148's
step 1 was to match eq. 43's stability analysis against Table 2's printed rows and **stop if it does
not match**. It matches.

**⚠ First, the directing seat corrected this seat's stopping line, and the correction is right.** C47
(e) recommended abandoning the build because the absolute flux has no anchor. But the pass condition is
a **ratio**:

    Ur_Mars / Ur_Earth  =  (H_Mars/H_Earth) × (q_Earth/q_Mars)

`H` is known absolutely for both bodies, and if `b` is **one global declaration** then `q ∝ b^{−β/n}`
appears on both sides of `q_Earth/q_Mars` and cancels. **So the direction test does not need the
absolute scale, and the missing anchor does not block it.** My stopping line was drawn around the wrong
quantity. ⚠ It survives in one narrowed place — the *absolute* flux still has no anchor and must not be
emitted — which is now the recorded reason for a refusal rather than a reason to stop.

**⚠ Second, two things this seat had told the directing seat turned out wrong on reading.**

1. **The equation to test is eq. 29, not eq. 30.** The paper introduces eq. 30 with *"In the limit of
   `Nu ≫ 1`, it approaches the following asymptotic formula"*, and Table 2's `Nu` is **3.1–7.2**. Read
   from the page image of p. 158, eq. 29 is
   `Nu[1 − 2Nu⁻¹(1 − a_rh θ⁻¹)]^{1−β(n+2)/(2n)} = a θ^{−1−β} Ra_i^β` — and `a ≈ 0.30 + 0.25n` was
   **fitted to eq. 29, not eq. 30**. ⚠ So **C47 (c)'s direction test ran the asymptotic form outside
   its own stated limit.** At Table 2's scale the two forms differ by **27 %**; they converge to 0.1 %
   only when `Ra_i` is raised 10⁸×. That does not overturn C47 (c)'s finding — `D` still cancels and
   both laws still go as `g^{1/3}` — but the test has to be re-run on eq. 29 in step 4.
2. **Table 1 cannot be an anchor.** C47 (e) listed it as one. Its linear-exponential block prints `Nu`
   but its `θ` and `Ra_i` sit in the **Arrhenius** columns, so no `(θ, Ra_i, Nu)` triple exists there.
   **Table 2's Δη = 1 block is the only row-level anchor in this paper**, ten rows of it.

**Step 1's result.**

| check | result |
|---|---|
| eq. 29 against Table 2's ten `Δη = 1` rows | **rms 2.27 %**, bias **−0.44 %p**, worst row **4.63 %** |
| the paper's own stated fit quality | *"The rms error of the fit is ∼1.2 per cent"* — ⚠ **on Table 1**, the set the fit was made to. 2.27 % on a held-out set is the expected degradation |
| eq. 44's `Ra_crit(n)` against the text's ∼450 / ∼134 / ∼104 | 441 · **143** · 98 — n = 1 and 3 pass, ⚠ **n = 2 off by 7 %**, now pinned by a test that fires if it ever changes |
| eq. 30 as the `Nu ≫ 1` limit of eq. 29 | ratio **1.270** at Table 2's scale → **1.001** at 10⁸× `Ra_i` |
| free cross-check: Nimmo's `ζ = 10⁻²` at `ΔT = 1350` gives `θ = 13.50` | inside Table 2's `θ` range 7.93–16.05. **Two independently transcribed modules agree on a quantity that means the same thing in both papers** |

**⚠ And the residual was tested for tunability, then left alone.** Refitting `a_rh` from the text's
2.5 gives 2.256 and buys **0.08 percentage points** of rms. A residual that refitting cannot move is
not a knob, so the text's single value stands and `Δη`-free `a_rh` is not read off Fig. 3. **A test
pins that**: if refitting ever buys more than 0.5 %p, it fires, because that would mean the residual
*is* adjustable and the single value would need re-arguing.

**What is not built, and stays not built until later steps:** any flux, dimensional or not. This module
emits nothing into the chain. The melting correction (eqs 41–56), the `b` sensitivity measurement, and
the Earth-vs-Mars direction test are steps 2–4.

### C47 (f2) 2026-09-08 — step 3's dehydration half passes 30 rows with zero tuned parameters

**Built into `engine/stagnant_lid.py`: eq. 42's local Rayleigh number, eq. 43's stability criterion,
eqs 45/50/51/53/54's melting parameters.** ⚠ **n = 1 only** — eq. 46's stress term `(τ*)^{1−n}` is
exactly 1 there and the derivation below drops it. The paper's own §4.1 and Table 2 are both n = 1.

**⚠ The geometry was derived, not guessed, and the derivation reproduces the paper's own fitted
coefficient.** Sublayers are measured **upward from the boundary layer's base**, and `η*` is relative
to `η(T_i)` because `Ra_i` already carries `exp[E/(nRT_i)]`, so `⟨1−T*⟩ = u/2` and
`η*_eff = exp(θu/2)`. The maximum in eq. 42 then falls at an interior point `u* = 4(n+1)/(nθ)`, and
eliminating `δ` gives `Nu ∝ θ^{−(2n+2)/(n+2)} Ra_i^β` — where **`(2n+2)/(n+2) = 1+β` exactly**, which
is eq. 30's form. The coefficient that falls out is

    a = [4(n+1)/n]^{1+β} exp(−2(n+1)β/n) / Ra_crit^β  =  **0.5539**  at n = 1

against the paper's regression result **`a = 0.55`** — **0.7 %.** ⚠ **That is not a transcription
check; it is an independent reproduction of the paper's own claim** that *"the boundary-layer stability
approach reproduces exactly the asymptotic heat-flow scaling"*. Confirmed numerically too: eq. 43's
numerics sit at **1.0071×** eq. 30 on every row, and 1.0071 is exactly 0.5539/0.55.

⚠ **And the same derivation fails at n ≥ 2** (0.274 and 0.187 against 0.80 and 1.05), which is the
dropped stress term showing itself. Diagnosed rather than patched, and the scope is recorded as n = 1.

⚠ **Labelled 2026-09-09 (Brief 167 A) — "the paper's regression result" is one of five numbers for this
one quantity, and Korenaga states the reason for the spread himself.** Read verbatim from the held paper:
*"Solomatov & Moresi (2000) ([`2000JGR...10521795S`](https://ui.adsabs.harvard.edu/abs/2000JGR...10521795S)) fit eq. (29) to their
numerical results and obtained **a ≈ 0.31 + 0.22n** by assuming a_rh = 1.2(n + 1). As **my definition of
T̄_i (eq. 20) results in slightly different values of Nu, Ra_i and a_rh**, I repeated their regression
analysis and obtained that **a ≈ 0.30 + 0.25n**. The rms error of the fit is ∼1.2 per cent."*

| value at `n = 1` | where it comes from |
|---|---|
| **0.528 ± 0.002** | S&M 2000 Table 5's one-parameter fit (`a_rh` 2.4, `β` fixed at the theoretical 0.333, χ²ᵥ 0.3) |
| **0.53** | the same paper as Korenaga summarises it, `a ≈ 0.31 + 0.22n` under `a_rh = 1.2(n+1)` |
| **0.55** | **Korenaga's own re-regression**, `a ≈ 0.30 + 0.25n` — *this is the 0.55 above, and the comparison stands* |
| **0.57** | Korenaga's Fig. 6 caption, a separate per-`n` subgroup fit in the same paper |
| **0.5** | Foley 2018's printed `c₁`, citing Reese, S&M and Korenaga together |

**So the 0.7 % is a correct statement about the number it names**, and it is a better one than it looked:
Korenaga's own fit carries an **rms of ∼1.2 per cent**, so our closed form lands **inside the paper's own
fit error**. ⚠ **What the 0.7 % must not be read as is agreement with the primary fit** — against S&M's
0.528 ± 0.002 our 0.5539 is **+4.91 %**, thirteen times that fit's stated precision. **And the cause is
printed, not mysterious: a different definition of the internal temperature `T̄_i`.** ⚠ *Which also means
that "+4.91 %, thirteen times" is a **comparison across a definition boundary and not evidence of an
implementation error** — the within-definition check is the 0.7 % against Korenaga's own refit, and it
passes inside his fit's rms. The three definitions are laid out verbatim in C51's first-anchor section.* That same
difference is the one candidate explanation for the 3.65× absolute-flux gap between the two papers
(C51's first anchor), which is why this is labelled here rather than repaired.

**Table 2, all three blocks, `nu_full` = eq. 43 + eq. 29's pre-asymptotic bracket:**

| `Δη` | rms | bias | worst | rows used in the paper's fit? |
|---|---|---|---|---|
| 1 | **2.16 %** | −0.01 %p | 4.22 % | no — the fit was to Table 1 |
| 3 | **2.84 %** | +1.68 %p | 6.10 % | ⚠ **no. independent anchor** |
| 10 | **3.35 %** | +1.95 %p | 8.24 % | ⚠ **no. independent anchor** |
| **all 30** | **2.83 %** | +1.21 %p | | |

**Zero free parameters**: `Ra_crit` from eq. 44, `a_rh` = 2.5 from §2.2's text, `z*_D` = 0.75 from
Table 2's footnote, `Δη` from the table's own column. **So the twenty `Δη = 3` and `Δη = 10` rows are
an independent anchor for the dehydration-stiffening mechanism**, and a test comment says so, so that
nobody later reads all thirty as fitted.

⚠ **One construction here is ours and is labelled in the code.** The stability analysis returns the
**asymptotic** `Nu`; Table 2's `Nu` of 3–7 is not asymptotic. So eq. 43's result is fed as the
right-hand side of eq. 29 and `Nu` re-solved. At `Δη = 1` that is exactly eq. 29; extending it to
`Δη ≠ 1` is our step, not the paper's.

**Two claims this seat made to the directing seat were wrong, and reading fixed both — in the
favourable direction this time.**

1. ⚠ **`Δρ` needs no figure read.** C47 (e) called it *"an input read off a graph"*. Eqs 51 and 53
   with §5's printed `(dF/dP)_S = 15 %/GPa` and `P_f = 0`, eq. 50's `dρ/dF`, §4's `ρ₀ = 3300` and
   eq. 45's solidus compute it outright. **Fig. 11 is a plot of the result.**
2. ⚠ **The paper contradicts its own `α`, and the contradiction is load-bearing.** §4's constant list
   prints `α = 2 × 10⁻³ K⁻¹`; §3.2's worked example says *"The factor αΔT is ∼0.05, so Δρ of 0.99
   corresponds to ΔT*_ρ of ∼0.2"*. At the paper's own `ΔT = 1350 K`, §4's value gives `αΔT = 2.70` and
   `ΔT*_ρ = 0.0037` — **missing both numbers** — while `3.7 × 10⁻⁵` gives `0.0499` and `0.2002`,
   **hitting both inside 0.2 %.** And ⚠ **this seat's earlier "harmless inside the paper" verdict on
   defect #24 was wrong**: `b` absorbs `α` inside `Ra_i`, but `α` **also** sets `ΔT*_ρ` in eq. 54,
   where nothing absorbs it. Using the printed value switches compositional buoyancy **off** rather
   than weakening it.


### C47 (g) 2026-09-08 — pre-registration for step 4, written before the test was run

⚠ **This section was written and committed BEFORE the direction test was computed.** That is the
point of it. The `α` choice below feeds the one mechanism that could produce the Earth-vs-Mars
asymmetry step 4 measures, and the two candidate values differ by **54×**, so the choice has to be
justified on grounds that cannot know the answer.

**The choice: `α = 3.7 × 10⁻⁵ K⁻¹`, from Korenaga 2009 §3.2, not the `2 × 10⁻³ K⁻¹` printed in §4.**

**The grounds, which are independent of step 4's outcome.** §3.2 states its own worked example:

> *"The factor **αΔT is ∼0.05**, so Δρ of 0.99 corresponds to `ΔT*_ρ` of ∼0.2."*

With the paper's own `ΔT = 1350 K`:

| `α` | `αΔT` | `ΔT*_ρ` at `Δρ = 0.99` | reproduces §3.2? |
|---|---|---|---|
| **2 × 10⁻³** — printed in §4's constant list | 2.700 | 0.0037 | ✗ off by 54× |
| **3.7 × 10⁻⁵** | **0.0499** | **0.2002** | ✅ both numbers, to 0.2 % |

**The paper contradicts itself, and only one of the two readings reproduces the paper's own worked
example.** That is the whole argument, and it is settled by arithmetic on two printed sentences —
nothing in it looks at Earth, Mars, or a Urey ratio.

⚠ **Why this is a place where a reader should be suspicious, stated by us rather than left to be
found.** `α` sets `ΔT*_ρ` (eq. 54), `ΔT*_ρ` enters `ΔT*_eff` in eq. 42, and compositional buoyancy is
**the candidate mechanism for the very asymmetry step 4 is about to measure**. Choosing the value that
makes that mechanism 54× stronger, immediately before measuring whether the mechanism is strong
enough, is a sequence that looks like knob-turning from the outside however sound the argument is.

**So step 4 is run BOTH ways and both lines are reported, side by side, whichever passes.** The
dependence is published, not resolved: a reader must be able to see at a glance that the conclusion
rests on which half of the paper's self-contradiction is taken.

**What is already fixed and cannot move**, so that step 4 has nothing left to tune:

| quantity | value | source |
|---|---|---|
| `Ra_crit(n)` | `exp(3.84 + 2.25/n)` | eq. 44 |
| `a_rh` (n = 1, linear-exponential) | 2.5 | §2.2 text, and refitting buys 0.08 %p — C47 (f) |
| `(dF/dP)_S` | 15 %/GPa | §5, printed (Korenaga 2006) |
| `P_f` | 0 | §5, *"for simplicity"* |
| `dρ/dF` | −1.2 kg m⁻³ per per cent | eq. 50 |
| `ρ₀` for melting parameters | 3300 kg m⁻³ | §4 |
| `b` | re-fitted on the paper's own printed Earth condition, one global declaration | C47 (d), and C47 (f) measured the ratio's sensitivity at 3.7 % per decade against the absolute flux's 115 %, bounded above at 1.384 |
| `Δη` | **a band, 10² (§4) and ∼10³ (§3)** — not elected | §3, §4 |

**The target step 4 must hit, fixed in C47 (f) before this section:** `q_Earth/q_Mars` must reach
**3.68** (against our own 0.454 denominator) or **4.78** (against Korenaga's 0.35), from the
no-melting value of **1.372**. So the melting correction must suppress Mars's flux **2.7–3.5× more
than Earth's**.

**⚠ Pre-registered verdict rule — all four cells, written before the run.** The fourth was missing
from the first draft of this section and was filled on the directing seat's catch, still before the
computation. A rule invented after seeing which cell you landed in is not a rule.

| outcome | verdict |
|---|---|
| **neither `α` reaches the target** | the **fourth** law family to fail in the same direction. C47 closes as *named, not filled* — the recorded answer becomes "no single untuned law in this literature reproduces both Urey ratios", and the three-families-same-direction note in C47 (c) closes with it |
| **both reach it** | the choice did not matter; the result stands on its own and `α` is recorded as a non-issue for this test |
| **only §3.2's `α = 3.7 × 10⁻⁵` reaches it** | reported as **conditional on the paper's self-contradiction**, and **not** presented as a pass. The arithmetic favours §3.2, but a result that exists only under one half of a contradiction is a result with a footnote, not a closed item |
| **only §4's printed `α = 2 × 10⁻³` reaches it** | ⚠ **also not a pass, and for a sharper reason than "wrong for the right reason".** At `αΔT = 2.7` the equivalent temperature contrast is `ΔT*_ρ ≈ 0.004` — compositional buoyancy is *switched off*, not merely weakened. So this cell would mean **the asymmetry is carried by dehydration stiffening alone, and adding compositional buoyancy destroys it** — i.e. the paper's two melting mechanisms push in opposite directions on the very quantity being tested. That is a finding about the mechanisms and it gets its own item; it is not evidence that the law reproduces the Urey ratios, because the `α` producing it fails the paper's own worked example |

**⚠ The point of the eight fixed values above is that step 4 has nothing left to tune.** That sentence
matters more than the table: every quantity the direction test touches was pinned by a printed source
before the test ran, so a failure cannot be argued away and a pass cannot be manufactured.

**⚠ Registered decomposition — the test is run three ways per `α`, six runs in all.** The insight
behind the fourth cell is that **dehydration stiffening and compositional buoyancy push in opposite
directions on the asymmetry.** If that is true it is true whichever cell lands, so it must be measured
in the main test rather than invoked only where it becomes extreme:

| run | mechanisms on | what it answers |
|---|---|---|
| **(a)** | dehydration stiffening only (`Δη`, `z*_D`) | how much of the asymmetry the stiff dehydrated lid carries alone |
| **(b)** | compositional buoyancy only (`ΔT*_ρ`) | how much the density contrast carries alone, and **with what sign** |
| **(c)** | both — **this is the test** | whether the target 3.68 / 4.78 is reached |

⚠ **Registered before the computation, and the reason matters:** with a single number the result is
uninterpretable either way — reaching the target would not say what carried it, and missing it would
not say what was short. A decomposition added *after* seeing where (c) landed would be a
decomposition built to explain the answer. Registered now, it also puts the opposite-directions claim
at risk: if (a) and (b) turn out to push the **same** way, the fourth cell's reasoning is wrong and
that gets recorded as this seat's error.

**Sign convention fixed now, so it cannot be reinterpreted later:** the asymmetry is `q_Earth/q_Mars`,
and a mechanism *helps* if turning it on **raises** that ratio above the no-melting 1.372. A mechanism
that lowers it pushes against the test.

### C47 (h) 2026-09-08 — step 4's verdict is held, and step 0's threshold is written before the measurement

**Step 4 ran, its numbers are final, and its verdict is held.** The numbers are in C47 (g)'s
pre-registration and are not revised here. ⚠ *Corrected 2026-09-08 (Brief 160): **that run's outputs are
not in this repo.** (g) holds the pre-registration — the four cells, the eight fixed values, the target
3.68 / 4.78 and the no-melting 1.372 — and no `q_Earth/q_Mars` from a run appears in any document,
module, test or scratch directory. The run lived in the 09-07/08 seats' transcripts and its numbers went
with them. Step 4 is therefore a **build**, not a re-run — counted in C47 (j).* ⚠ *And that marker is
itself superseded within the day: the run **was recovered** from the 09-07 transcript at `f3f068ea`, so
"in no scratch directory", "went with them" and "a build, not a re-run" are each no longer true as
written — see C47 (j) and (k).* What is recorded here is why the verdict cannot be read off
them yet.

**⚠ The pre-registration had a hole, and the directing seat found it, not this seat.** The eight
quantities pinned before step 4 do not include `T_p`. The direction test was run at a **common
potential temperature** for Earth and Mars — a decision made while implementing, on the mistaken
ground that C47 (c) had already settled it. **C47 (c) settled something else**: it forbade *choosing*
Mars's `T_m` so that `Ur` comes out. **Reading `T_p` off a thermal history is not choosing.** Those two
were collapsed into one, and the collapse is this seat's.

⚠ **The omission is shared and is recorded as shared.** This seat pinned eight values and published
the table; the directing seat approved it. Neither noticed the ninth. It is not the work seat's alone.

**Why it matters, in one sentence:** Mars's higher Urey ratio is explained in the literature by Mars
having *cooled more* — so running the test at a common `T_p` may have removed the very physics being
tested, in which case the failure is the setup's and not Korenaga's.

**And route (ii) is not hypothetical.** `core_history` already emits
`mantle_potential_temperature_present`, and on Earth it returns **1525 K** against the 1623 K this
seat fed step 4 from Korenaga's own §4 condition — a 98 K difference between two non-arbitrary
sources. ⚠ **Corrected later the same night by C48: that 1525 K comes out of a call made far outside
the flux law's expansion point.** The blast radius of C48 is small — one consuming edge, no board row,
no `db/` entry — **but a small blast radius does not exempt this citation**, which is inside it. The
argument above stands only as far as C48 leaves it standing. It cannot run on Mars because `earth.yaml` is the only body declaring the two initial
temperatures.

**⚠ Route (i) is closed, and not for want of looking.** Monders, Médard & Grove 2007
([`2007M&PS...42..131M`](https://ui.adsabs.harvard.edu/abs/2007M%26PS...42..131M)) states
*"the persistence of high mantle potential temperatures on Mars, **similar to those on the modern
Earth**, until at least the very latest Noachian (**3.7 Ga**)"*. **Mars has no present volcanism, so
no erupted melt records a present `T_p`** — every "present Martian potential temperature" in the
literature is a thermal-model output, not a measurement. ⚠ And the paper's `1320 °C` is the multiple
saturation temperature of **one Gusev basalt at 1.0 GPa**, not a mantle potential temperature; it is
not transcribed. Baratoux+ 2011 ([`2011Natur.472..338B`](https://ui.adsabs.harvard.edu/abs/2011Natur.472..338B))
is the canonical `T_p`-versus-time curve and was **not held** (Nature) — ⚠ *held since 2026-09-08
(owner-supplied PDF). Reading it closed the hole and narrowed the claim: the paper prints the epoch
**difference** (80 ± 20 °C) but no absolute `T_p` anywhere in its text — the levels everyone re-cites are
contour labels on its Fig. 3/4. See C47 (i).*
⚠ **2026-09-08 — re-cited present-day values found, the original still unheld.** Yoshizaki & McDonough
2020 (~1500 K) and Dong+ 2022 (1600 K "today") both print present-day Martian `T_p` **as model inputs**,
100 K apart, both tracing to Baratoux+ 2011 — held since 2026-09-08, and its absolute levels are
figure-read, not printed (C47 (i)). **So "closed" above is wrong as written** — what
survives is that no Mars `T_p` is *measured*. Corrected in full in C47 (i).

**What Mars needs, which is more than the brief supposed.** ⚠ *Stale since Brief 149 (`2d1bb397`), which
created it: `engine/bodies/mars.yaml` exists, with the two declarations below written into it.* There is no `mars.yaml` at all; the five
body files are Earth, Alpha Centauri A b, Pandora and the two Luhman 16 components. So this is a new
control body, on `earth.yaml`'s own stated footing — *"a specimen for checking the engine against
published values, not a board body"* — and **it does not go on the board.** Of its inputs, mass,
radius, age and core mass fraction are published and `stagnant_lid: true` is a fact, but **three
declarations have no Martian source**: `potential_temperature` and the two initial temperatures.

**Two of the three cost nothing, and one is the whole question.**

- **The initial temperatures transfer unchanged from Nimmo+ 2004's printed starting condition** —
  Fig. 2's caption, *"starting temperature of both mantle and core was 4800 K"*, which is where
  Earth's own 4800 K / 3040 K come from. That is this engine's established pattern for an Earth number
  declared on every rocky body (`MANTLE_SHARE = 0.70`, `T_s = 293 K`), and its value here is precisely
  that **it leaves nothing for this seat to pick.** The 3.7 Ga checkpoint then validates or refutes the
  transfer.
- ⚠ **`potential_temperature` is different, and transferring Earth's 1600 K would re-introduce the
  defect this section exists to fix — with a citation attached.** It also steers the trajectory:
  `core_history` sets `r_b = cmb_temperature / potential_temperature` and divides the mantle cooling
  rate by `√r_b`.

**So step 0's question, stated the way the directing seat put it, which is sharper than this seat's
first framing:** not *"is route (ii) circular"* but **"may Earth's `potential_temperature` be
transferred to Mars at all?"**

**⚠ Threshold and sweep width, fixed here before the measurement.** Naming "weak" and "strong" after
seeing the numbers would be inventing a rule to fit the cell it landed in — the error this seat
blocked in C47 (g)'s fourth cell and would otherwise repeat one section later.

| item | value | ground |
|---|---|---|
| **sweep** | declared Mars `potential_temperature` over **1400–1800 K** | Earth's declared value is 1600 K (Unterborn+ 2019) and Monders has Mars *"similar to modern Earth"* until 3.7 Ga, so ±200 K brackets it without being chosen for an outcome |
| **criterion A** | `abs(d output T_p / d declared T_pot) < 0.5` | at a slope of 1 the declaration **is** the output; at 0 the trajectory has forgotten it. Half is the point where the body's own mass, radius and age stop dominating |
| **criterion B** | the 3.7 Ga checkpoint verdict must be **the same at both sweep ends** | if sweeping our declaration flips the checkpoint, the checkpoint is testing the declaration and not the trajectory |
| **rule** | **both** must hold to proceed. Either failing stops step 0 and the transfer is refused | — |

⚠ **Criterion A measures the declaration's effect on the *output `T_p`*, not on `q_E/q_M`, and that
is deliberate.** The end-to-end sensitivity looks like the more relevant one and it is the one that
must not gate this decision: **fixing a threshold on the final answer means letting the answer decide
whether the input was legitimate.** A is on the intermediate quantity because the question is whether
Earth's number propagates into Mars's state — which is answerable without knowing what that state then
implies. **Not an omission; the placement is the point**, and it is written here because the obvious
"improvement" is to move it.

**The end-to-end sensitivity is measured afterwards and kept as a record.** Once the verdict is fixed
it can no longer influence it, and what the result depends on, and by how much, still gets written
down. Order buys both.

⚠ **And the checkpoint's own limit, recorded beside it so a pass is not over-read:** Monders gives a
**qualitative** statement, not a number. The checkpoint can only catch a badly wrong trajectory. **A
pass is not a precision validation of the Martian thermal history**, and nothing downstream may cite
it as one.

### C47 (i) 2026-09-08 — step 0's numbers, the criterion-B rule fixed before the unblinding, and four corrections

**Step 0 asked one question — `engine/interior-core.md@«be transferred to Mars at all?»` — and this section carries its numbers.** Criterion A's are below and
final, and criterion B's are below. ⚠ **The rule that decides criterion B was committed at `2fb2bba4`
with the 3.7 Ga column still unread** — including the verdict-line paper, which was the owner's to pick.
The table was computed afterwards and added in the commit that follows it, so **git testifies to the
order** rather than this sentence doing it.

⚠ **Every number in this section is at the core heating H = 1.5 pW/kg** (`core_energy.H_CORE` as it stood on
2026-09-08). Owner decision ⑤ lowered the declared H to 0.14 on 2026-09-09, and at the declared H the same
trajectory ends at **T_p 1377.23 K** with **T_p@3.7 Ga 1668.05 K** — criterion B still passes, with the upper-end
headroom **5.1 K** instead of 4.0–4.7 K. Criterion A's 1400–1800 K sweep has **not** been re-run at the declared H.
The numbers below are left exactly as measured; the label is what Brief 166 D adds.

#### The criterion-B rule, fixed before the numbers were read

C47 (h) pre-registered criterion B as one sentence — *the 3.7 Ga checkpoint verdict must be the same
at both sweep ends*. That sentence plus a paper band did not compose into one window, and the work
seat refused to unblind until the directing seat closed the four gaps. ⚠ **The refusal is the reason
this subsection exists: the rule below was fixed while the answer was still unread, and the commit
carrying it is dated before the commit carrying the table.**

| # | question the sentence did not answer | decided 2026-09-08 | why this and not the other reading |
|---|---|---|---|
| ① | is the window the paper's **absolute** band, or the paper's width **centred on** Earth's declared 1600 K? | **absolute band.** Pass = `T_p@3.7 Ga ∈ [band]`. The declared 1600 K does **not** enter the arithmetic; it stays as the guard that the window is never built from the engine's own 1525 K output | centring would invent a `±` no paper prints (Herzberg 2007's band is not symmetric about 1600 K), which is `docs/reference/derivation-discipline.md@«A band is the opposite of a knob only when its width comes from the physics»`. ⚠ The two readings differ by 13.15 K at each edge, so this is not cosmetic |
| ② | one of the four candidate papers prints a **point** (Herzberg+ 2010, 1350 °C = 1623 K, no `±` in the abstract) — what is its in/out? | **excluded from the agreement test**, kept as a record column reporting the distance in K | a zero-width window admits nothing, so its cell is undefined under either reading of ①. The agreement test runs on the three candidates that print a band |
| ③ | "the same verdict at both ends" — is **both ends out** "the same"? | **failure.** Both ends out means no declared value passes the checkpoint, which is a refutation, not stability. Step 0 fails and the transfer is refused | the checkpoint asks whether the declaration puts Mars near modern Earth at 3.7 Ga; "stable and wrong at every point" answers that with no |
| ④ | which variant, and do the interior sweep points count? | **verdict on `T_m0-fixed`** (the variant that uses `engine/bodies/mars.yaml@«mantle_initial_potential_temperature: 4021.0»`, the file's printed value), **at the two ends only**. `r_b-point` and the three interior points are record columns | (h) says *both sweep ends*, and the variants are an implementation choice that (h) never registered, so the file's own printed state is the one under test |

**The verdict line is the owner's, and it is chosen: Herzberg+ 2007, `[1553.15, 1673.15]` K
(2026-09-08 17:35, from the four candidates below).** ⚠ The rank order that would have picked it
— rank 1 Monders+ 2007, rank 2 Herzberg+ 2007 — **was a seat's, is in no commit, and collided with
the parallel seat's own finding** that *the choice of paper is the choice of width, so it is an
owner-facing choice*. So the rank order is chronicle only; the four candidates went to the owner and
the owner picked the first:

| candidate | window, K | grade | note |
|---|---|---|---|
| **Herzberg+ 2007** [`2007GGG.....8.2006H`](https://ui.adsabs.harvard.edu/abs/2007GGG.....8.2006H) — ✅ **owner's choice, the verdict line** | **[1553.15, 1673.15]** | ⚠ **held** since 2026-09-08 (owner-supplied PDF, cache) — upgraded from *abstract only*, and the label re-read in the body: *"Our preferred `T_P` range for ambient mantle is 1280–1400 °C (Figure 5)"*, computed by the **McKenzie & Bickle 1988** potential-temperature method for *"MORB magmas with 10–13 % MgO"*, and again where the paper states its result — *"Our work shows that ambient mantle temperatures at normal oceanic ridges are 1280–1400°C"*, `ΔT_P` = 120 °C — the sentence pinning the location rather than a paragraph number | a potential temperature of the ambient mantle, so it does not repeat the Monders defect below. The body also warns its Iceland values *"should not be used as a high `T_P` anchor for ambient mantle"* — we do not |
| Katsura+ 2010 [`2010PEPI..183..212K`](https://ui.adsabs.harvard.edu/abs/2010PEPI..183..212K) — record column | [1575, 1645] from the abstract; **[1560, 1640] from the body** | ⚠ **held** since 2026-09-08 | mineral-physics route (410-km discontinuity + adiabat), no solidus anywhere in it. ⚠ **The abstract and the body disagree**: abstract *"the mantle potential temperature is found to be 1610 ± 35 K"*, body §4 *"1600 ± 40 K"* — and the divergence is systematic, not only in `T_p` (transition-zone base 2010 ± 40 vs 1990 ± 50 K, 2700 km 2730 ± 50 vs 2630 ± 60 K). **Neither is elected**, both are recorded, and **Mars's 1668 K is outside both**, so the record column's verdict does not move |
| Putirka 2016 [`2016AmMin.101..819P`](https://ui.adsabs.harvard.edu/abs/2016AmMin.101..819P) — record column | [1603.15, 1723.15] | abstract only | 1330–1450 °C, modern ambient MORB, olivine–liquid Fe–Mg re-calibration |
| union of the four | [1553.15, 1723.15] | — | widest reading, **unchanged** by Herzberg+ 2010's band, which lies inside it |
| ⚠ **Monders+ 2007 cannot supply one** | — | held | its 1280–1475 °C is Earth's **basaltic magmatism** range (Kinzler & Grove 1992, McKenzie & Bickle 1988), not a potential temperature. Using it would put a magmatism range in a `T_p` slot — the same class of error C47 was opened for |
| record only | Herzberg+ 2010 [`2010E&PSL.292...79H`](https://ui.adsabs.harvard.edu/abs/2010E%26PSL.292...79H) 1623 K (the point of rule ②) — ⚠ **held** since 2026-09-08, and the body §3 does print a **band**: *"a mantle potential temperature (i.e., `T_P`) of **1350 ± 50 °C** is required to produce primary basaltic magmas having 10–13 % MgO"* = **[1573.15, 1673.15] K**, which Mars's 1668 K is **inside**. ⚠ **Rule ②'s "point candidate, excluded" was a decision taken on the abstract**, which prints no ±; recorded here as an after-the-fact column, and **the agreement test is not recomputed** — re-running a test on evidence that arrived after its verdict is the thing pre-registration exists to prevent. Also record-only: Sarafian+ 2017's **+60 °C** | — | so the apparent agreement of the two routes is not independent of whether that correction is applied |

#### Criterion A — passes, and by three orders of magnitude

**Sweep: Mars's declared `potential_temperature` over 1400–1800 K, five points, both variants.
Threshold `|d T_p,out / d T_pot,declared| < 0.5`, pre-registered in C47 (h).**

| declared `T_pot` | `r_b` | `T_m0` (`r_b`-point) | steps | output `T_p` | output `T_c` | `h_min` Myr | max `h/τ` |
|---|---|---|---|---|---|---|---|
| 1400 | 1.1882 | 4039.58 | 1197 | **1382.74** | 3897.09 | 0.0049 | 0.100 |
| 1500 | 1.1909 | 4030.44 | 1197 | **1382.82** | 3895.08 | 0.0051 | 0.100 |
| 1600 | 1.1937 | 4021.05 | 1197 | **1382.90** | 3893.01 | 0.0053 | 0.100 |
| 1700 | 1.1868 | 4044.41 | 1198 | **1382.73** | 3897.84 | 0.0048 | 0.100 |
| 1800 | 1.1799 | 4067.99 | 1199 | **1382.56** | 3902.68 | 0.0044 | 0.100 |

| variant | end-to-end slope | adjacent slopes | max \|slope\| | verdict |
|---|---|---|---|---|
| `r_b`-point | −0.0004 | +0.0008 +0.0008 −0.0017 −0.0017 | **0.0017** | ✅ ≪ 0.5 |
| `T_m0`-fixed | −0.0004 | +0.0008 +0.0008 −0.0017 −0.0017 | **0.0017** | ✅ ≪ 0.5 |

**Three things the table says beyond the threshold.**

- **The two variants agree to the printed digit at every point.** So ④'s choice of verdict variant
  moves nothing in the output; it is a provenance choice, not an accuracy one.
- ⚠ **The slope changes sign at 1600 K**, because `r_b` is itself non-monotonic in the declaration
  (1.1882 · 1.1909 · **1.1937** · 1.1868 · 1.1799 — a 1.2 % spread with its maximum at 1600 K). The
  400 K sweep moves the answer by **0.34 K**: the trajectory has all but forgotten the declaration.
- **Liveness, both parts, before any slope was read.** Earth's anchor reproduced inside the same run
  (`T_p` 1525.46 K against the anchor 1525.46, 1152 steps, `r_b` 1.5789) and the five outputs are five
  distinct values in both variants, so the sweep is not a constant — `engine/test_interior.py@«늘 발화하면 상수다»`
  applied to a scratch script whose numbers get reported.

#### Criterion B — passes, and ⚠ by 4 K

**Unblinded at 17:44:58 under the rule at `2fb2bba4`, from the values the 16:40 run wrote blind
(`C47 STAGE0 END rc=0 16:40:01`).** Verdict line **Herzberg+ 2007 `[1553.15, 1673.15]` K** (owner, 17:35 —
before the unblinding), verdict variant `T_m0`-fixed, verdict points the two ends.

⚠ **The seal held for nine of the ten columns, not ten.** The `1600 K` point's `T_p@3.7 Ga` was **already
public**: `engine/test_core_history.py` prints it as test ⑥'s third value (`T_p@3.7Ga`, the nearest adaptive
row) and `engine/interior-core.md@«within 0.1 K of the 0.25 Myr sweep»`'s C48 cell has carried **1669.22 K**
since `20ed09d7`. **What was public was the value, not the verdict** — 1600 K is an interior point and the
verdict is read at the two ends, so no cell could be anticipated from it. *(The same label, run two ways, is
0.10 K apart: 1669.22 adaptive against the 0.25 Myr sweep's 1669.12, which is test ⑥'s ±5 K comparand.)*

⚠ **And the pre-registered hold branch never fired, which is different from being skipped.** The rule said
*if the candidates disagree the verdict is held and the owner picks the paper* — and they do disagree. But
the owner picked at **17:35**, before the disagreement was visible at 17:44:58, so the branch was
**pre-empted by an earlier choice** rather than passed over. Its purpose — that a seat must not elect the
width — was served by the route the choice actually took.

| declared `T_pot` | variant | `T_p@3.7 Ga` | row's actual t, Gyr | `q_M`, TW | `q_C`, TW | **Herzberg 07** | Katsura 10 | Putirka 16 | union | − 1623 K |
|---|---|---|---|---|---|---|---|---|---|---|
| **1400** | **`T_m0`-fixed** | **1668.86** | −3.7007 | 3.057 | 0.405 | **in** | out | in | in | +45.86 |
| 1400 | `r_b`-point | 1668.65 | −3.6995 | 3.057 | 0.405 | in | out | in | in | +45.65 |
| 1500 | `T_m0`-fixed | 1669.04 | −3.7006 | 3.058 | 0.405 | in | out | in | in | +46.04 |
| 1500 | `r_b`-point | 1668.57 | −3.6981 | 3.058 | 0.405 | in | out | in | in | +45.57 |
| 1600 | `T_m0`-fixed | 1669.22 | −3.7006 | 3.059 | 0.405 | in | out | in | in | +46.22 |
| 1600 | `r_b`-point | 1669.22 | −3.7006 | 3.059 | 0.405 | in | out | in | in | +46.22 |
| 1700 | `T_m0`-fixed | 1668.81 | −3.7007 | 3.056 | 0.405 | in | out | in | in | +45.81 |
| 1700 | `r_b`-point | 1668.74 | −3.7003 | 3.056 | 0.405 | in | out | in | in | +45.74 |
| **1800** | **`T_m0`-fixed** | **1668.41** | −3.7008 | 3.054 | 0.406 | **in** | out | in | in | +45.41 |
| 1800 | `r_b`-point | 1668.27 | −3.7000 | 3.054 | 0.406 | in | out | in | in | +45.27 |

**Verdict: 1400 K → 1668.86 K in · 1800 K → 1668.41 K in — the same verdict at both ends, and the
verdict is *in*. Criterion B passes.** With criterion A, **step 0 passes: Earth's declared
`potential_temperature` may be transferred to Mars**, and `engine/bodies/mars.yaml`'s `validated:
pending` becomes a validation.

**Four things that must be read with it.**

- ⚠ **The margin is 4 K on a 120 K band.** The band's top edge is 1673.15 K and the trajectory lands at
  1668.4–1669.2 K, so the headroom is **4.0–4.7 K**. **A 5 K error anywhere in the trajectory flips this
  cell**, so the pass may not be cited as a comfortable one — and C48 has already shown this integrator
  calling its flux law far outside the law's expansion point.
- ⚠ **The four banded candidates do not agree, and the verdict rests on which one the owner picked.**
  *(Four, not three: Herzberg+ 2010's body band arrived after the verdict and is recorded above — the
  count moves, the verdict is not recomputed.)* Herzberg+ 2007, Putirka 2016, Herzberg+ 2010's
  `[1573.15, 1673.15]` and the union all say *in*; **Katsura+ 2010 `[1575, 1645]` puts both ends OUT** —
  because 1668 K is above its top edge. So under the mineral-physics reading of modern Earth this checkpoint
  fails. **The dependence is published, not resolved**, exactly as C47 (g) published step 4's dependence
  on `α`: the owner chose the paper before the column was opened, which is why this is recorded rather
  than re-litigated.
- **The declaration barely moves the checkpoint**: 0.81 K of spread in `T_p@3.7 Ga` across the whole
  400 K sweep, and the two variants agree to ~0.5 K. That is criterion A's 0.0017 slope seen at the
  checkpoint instead of at the present.
- **Earth, in the same run, is at 1824.70 K at 3.7 Ga** (present 1525.46 K, 1152 steps). So Mars at
  3.7 Ga sits ~156 K **below Earth-at-3.7-Ga** while inside **modern** Earth's band. ⚠ That is what
  Monders' sentence says — *similar to those on the **modern** Earth* — and it is what the rule
  implemented; a checkpoint against Earth's own 3.7 Ga state would be a different test and would fail.

**Sampling:** the checkpoint reads the nearest adaptive row. ⚠ *Corrected on the audit seat's
reproduction: the row lands within **0.79 Myr** of −3.7 Ga on the **verdict variant** (`T_m0`-fixed, all five
points), which is what the verdict rests on — but the widest **record** row, `1500 | r_b`-point, is
**1.91 Myr** away (−3.6981 Gyr). "Within 0.8 Myr at every point" was wrong as written; the table's own t
column carried the counter-example.* The sampling gap does not move a cell here — the sweep's whole spread
in `T_p@3.7 Ga` is 0.81 K — but the claim had a scope it did not state.

⚠ **And the ceiling, restated because the pass is thin:** Monders+ 2007's statement is **qualitative**.
It can catch a badly wrong trajectory and nothing finer. **A pass is not a precision validation of the
Martian thermal history**, and at 4 K of headroom it is not even a comfortable qualitative one.

⚠ **And the checkpoint's ceiling, restated so a pass is not over-read** (C47 (h) put it first):
Monders+ 2007's statement is **qualitative** — high `T_p`, *"similar to those on the modern Earth"*,
until 3.7 Ga. It can catch a badly wrong trajectory and nothing finer. **A pass is not a precision
validation of the Martian thermal history.**

#### Four corrections carried by this section

**1. Where 1623 K comes from — the C47 (h) attribution was wrong, and the chain is one link longer.**
⚠ *Settled 2026-09-08 with both papers held:* **1623 K is Herzberg+ 2010's `1350 ± 50 °C`** — itself a
consensus value, carrying seven citations in that sentence (McKenzie & Bickle 1988, Langmuir+ 1992, Kinzler
1997, Herzberg+ 2007, Courtier+ 2007, Lee+ 2009, Gregg+) — **and the range under it is Herzberg+ 2007's
1280–1400 °C**. So Korenaga 2010 §5's attribution to *2007* skips a step: the digits are 2010's, the
supporting range is 2007's. The paragraph below is the trace as it stood before the papers were held. (h) called it *"Korenaga's own
§4 condition"*. Traced: Korenaga 2010 §5 prints *"The reference temperature is set to 1623 K (1350 °C),
which corresponds to the present-day potential temperature of the ambient mantle"* and attributes it to
**Herzberg et al. 2007** — but Herzberg+ 2007's own abstract prints **1280–1400 °C**, and the **1350 °C
at the present** is printed by Herzberg+ **2010**. Korenaga **2009** §4's `ΔT` = 1350 K with `T_s` = 273 K
is a **third** path to the same digits and is a different quantity (a contrast, not a potential
temperature). ⚠ **So three readings in two papers land on 1623 K, and which one step 4 used is not
decidable from the number** — which is exactly `docs/reference/derivation-discipline.md@«A number cannot enter without its label»`.

**2. `h_min_myr` mixes the landing step into the minimum — measured, not argued.**
`engine/core_history.py@«# land exactly on the present»` truncates the final step so the history ends on
t = 0, and that truncated value competes for the minimum. `max_h_over_tau` does not have the defect (the
ratio is taken before the truncation). **On Earth the reported minimum IS the landing step:**

| what | value | where |
|---|---|---|
| `h_min_myr` as `integrate` reports it | **0.249252 Myr** | step **#1152 of 1152**, 1-based — the last one |
| the four steps before it | 4.0000 Myr each | the cap, binding — and **1125 of the 1152** steps run at the cap |
| the actual stiffest step | **0.3929 Myr** | step 0, the first |

⚠ **And that closes an open label.** `engine/tools/adaptive-step-prereg.md@«first steps shrink from 4 Myr to ≈ 0.39 Myr»`
predicted 0.39 Myr and the audit measured a minimum of 0.249 Myr — **two different quantities, not a wrong
prediction.** The prediction is right to three digits (0.3929 Myr); the 0.249 is the landing step. The
pre-registration stays verbatim; the comparison lives here. So Mars's `h_min` 0.0044–0.0053 Myr in the
criterion-A table is read with the same caveat, and nothing downstream uses `h_min` as a physical quantity.

**3. "Mars's 75" is a truncation of 75.8.** The fixed 4 Myr step was `h/τ` = **75.8** on Mars's first
step (τ = 0.0528 Myr at the start), not 75. The three places that print it carry `≈`, so the label is
sound and only the digit is corrected here.

**4. Route (i) is not closed the way (h) says.** (h) states *"Route (i) is closed, and not for want of
looking"* on the ground that no present Martian `T_p` is published. **Re-cited present-day values do
exist** — Yoshizaki & McDonough 2020 ([`2020GeCoA.273..137Y`](https://ui.adsabs.harvard.edu/abs/2020GeCoA.273..137Y), §5.1, held) assumes **~1500 K** as a
present-day areotherm input; Dong+ 2022 ([`2022Icar..38515113D`](https://ui.adsabs.harvard.edu/abs/2022Icar..38515113D), held) uses **1600 K** for *"the average
Martian mantle today"* and the Baratoux curve by epoch (Amazonian ~1600–1650 K, Hesperian ~1650–1700 K).
Both are **model inputs, 100 K apart, and both trace to Baratoux+ 2011**, which Parro+ 2017 warns are
*"volcanic (non-average) regions"*. ⚠ **Baratoux+ 2011 is held since 2026-09-08** (owner-supplied PDF) and
it changes the grade of everything downstream of it:

| what Baratoux+ 2011 gives | value | grade |
|---|---|---|
| epoch-to-epoch **difference** — printed in the text and Methods | *"a total spread of ~80 K"*, and *"a temperature decrease of **80 ± 20 °C**"* | **printed** |
| absolute `T_p` by epoch — **only as contour labels on Fig. 3/4**, never in the text | Amazonian **1611–1678 K**, Hesperian **1649–1673 K**, read off the figures by eye (±10 °C) | ⚠ **figure-read — not a printed value, and it may not enter a board row** |

So the paper's own numeric claim is a **difference**, not a level, and the levels every re-citation quotes
are figure readings. Against those figures **Yoshizaki & McDonough's ~1500 K is more than 100 K below any
contour**, while **Dong+ 2022's 1600 K is an Amazonian volcanic-province value**. ⚠ Baratoux's own
corrigendum (*Nature* **475**, 254) touches only the heat-flow numbers, and this repo cites none of them —
checked. ⚠ **The original claim's core survives — no
Mars `T_p` is measured, because Mars has no present volcanism to record one — but "does not exist in
the literature" is wrong as written**, and the sentence is marked rather than replaced.

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

#### Recorded only — the convergence branch ⑤ had stopped testing what it registered

**Found while correcting the stale step strings, and it is not a step string.** Pre-registered branch ⑤ is a
**step**-halving convergence test (`engine/core-thermal-history-context-notes.md@«Run the full history at **h, h/2, h/4**»`,
recorded 2026-09-04 as width 0.001 % at **1135 / 2270 / 4540** steps). ⚠ *Two widths appear in these
documents and they are the same test on two days: **0.001 % is the 2026-09-04 record** (the figure the
code and the test carry) and **0.0006 % is the 2026-09-08 re-run** after the restoration, on the same
three step counts. Both are far inside the pre-registered 10 % pass line, so the branch's verdict never
moved.* After Brief 157 `core_history.sweep`
went on passing only `step_myr`, which is now the **cap** in `h = min(cap, 0.1·τ)` — so halving it changed
only the steps where the cap binds, and the recorded counts could not be reproduced. ⚠ **A pre-registered
branch had quietly become a different test, and nothing failed**: the gate does not run `--sweep`, and the
docstring still described the old one.

**Brief 161 restored the registered meaning** — `sweep` runs `adaptive=False` — rather than re-writing ⑤ to
match the code, because *"a branch registered before the adaptive step exists is not re-written afterwards"*.
An adaptive-**cap** sweep is a real question and is **deliberately not built**; it would need its own
registration.

#### The audit seat's independent run, at the same tree

**`test_core_history.py` re-run by a third seat, `rc=0`, digit-for-digit against the C48 row:** Earth
adaptive **1152** steps, max `h/τ` **0.100**, reported minimum `h` **0.249** Myr (the landing step, above);
Earth fixed-step **1135** steps, `T_p` **1525.46** K; Mars adaptive **1382.90 / 3893.01 / 1669.22** K,
**1197** steps, `h_min` **0.0053** Myr. **Runtime 223.66 s** against the ~235 s stated in the commit
message — **−4.8 %**, inside load variation, and reported because
`docs/reference/derivation-discipline.md@«say what your work adds to the gate's time»` asks for it.

#### Waiting on the owner, recorded so neither is decided by a seat

| decision | the two candidates | what turns on it |
|---|---|---|
| ~~criterion B's verdict line~~ | **answered 2026-09-08 17:35: Herzberg+ 2007 [1553.15, 1673.15] K**, the other three record-only | the 3.7 Ga in/out, hence whether the transfer is allowed |
| ~~Mars's declared `potential_temperature`~~ | **answered 2026-09-08 17:52: Earth's 1600 K, transferred (Unterborn+ 2019), in Brief 153's transfer-record form.** The two re-citations (Yoshizaki & McDonough 2020 ~1500 K; Dong+ 2022 1600 K, which agrees) are record columns | ⚠ **nothing in the Mars result** — criterion A's 0.0017 slope means the whole 400 K sweep moves the answer 0.34 K. It was a provenance choice, not an accuracy one |

### C47 (j) 2026-09-08 — step 4 is a build, not a re-run, and this is the head written before anything is computed

**Written at 18:44 KST, before any step-4 quantity was computed.** Brief 160 asked for step 4 to be
re-run with the ninth fixed value (`T_p`) supplied. ⚠ **There is nothing to re-run.** The search was
`step 4` / `단계 4` and `q_Earth/q_Mars` across `engine/` and `docs/reference/`, plus every earlier
seat's scratch directory for a runner or a log:

| what exists | where |
|---|---|
| the pre-registration — four verdict cells, eight fixed values, the target **3.68 / 4.78** from the no-melting **1.372**, the sign convention, the (a)(b)(c) decomposition | C47 (g), committed before the run |
| **step 1** — eq. 29/30/42/43/44 transcribed and checked row by row against Table 2's three `Δη` blocks | `engine/stagnant_lid.py`, `engine/test_stagnant_lid.py` (in the gate) |
| **step 3's dehydration half** — eqs 45/50/51/53/54, 30 rows, no tuned parameter | C47 (f2), same module |
| **step 4's outputs** | ⚠ **not in this repo** — and ⚠ *recovered 2026-09-08 ~21:00 from the 09-07 work seat's transcript (`a0402cc0`) by the directing seat, verbatim with per-block timestamps and tool ids, into `/Users/vana/Desktop/NearStars-artifacts/2026-09-08-c47-step4/c47_step4_recovered.md` (md5
`ce35dc0ad7d084a475b7242af75605d5`) — a durable path, since a scratch directory belongs to one session.* The runner was **two inline `python3 -c` blocks** (16:39:22, which raised `OverflowError`, and 16:39:56, which ran), so nothing of it was ever committed |

⚠ **So C47 (h)'s opening — *"Step 4 ran, its numbers are final"* — points at an artifact this repo does
not hold.** It ran inside the 09-07 seat's transcript, and that transcript — not the repo — is where the
numbers were. That sentence is marked in (h) rather than deleted, and this section exists so the next run
has a head that predates it.

⚠ **What the recovery changes, and what it does not.** The 09-07 outputs now exist as a recovered
artifact, so Brief 162 is *promote the inline runner and reproduce those numbers bit-for-bit*, not
*build from nothing*. ⚠ **And reproducing them proves only that the same code gives the same numbers — it is not a physical
anchor.** The independent legs are the four anchors below, and the load-bearing one is `b` reproducing
50 mW/m² at the paper's Earth condition. **But this seat has now read them**, so they are a
**reproduction anchor, not a blind target** — the head's ordering claim above covers this seat's own computation, which has not
happened, and it may not be read as a claim that the re-run was blind to the recovered values. The
verdict cells in (g) are what they always were: written before any of it.

**What the build must add, counted before it is started** (`engine/stagnant_lid.py`'s own docstring
already says *"차원화는 단계 3–4"* — the module deliberately stops short of a flux):

| # | missing piece | what pins it |
|---|---|---|
| 1 | the fixed-point iteration **`z*_D = Nu⁻¹`** (eq. 56) — `nu_full` today takes `z_d` as an argument and does not iterate it | Korenaga 2009 eq. 56, *"iterated by setting `z*_D = Nu⁻¹` when `Nu > 1/z*_D`"* (C47 (e)) |
| 2 | per-body **`θ`** and **`Ra_i`** from `E`, `T_s`, `ΔT`, `g`, `D`, `κ`, `ρ`, `C_p` | the paper's §4 constant list; ⚠ and the `α` in it is the one the paper contradicts itself on (C47 (g)) |
| 3 | the **`b` normalization** — one global declaration, re-fitted on the paper's own printed Earth condition | C47 (d): *"take Korenaga 2009's own `b`, re-fitted on the paper's own printed Earth condition … as one global declaration for every body"*. ⚠ Width unquantified by the paper, and `q ∝ b^{−β/n}` — a decade of grain size is 2.15× in flux |
| 4 | **`Nu → q`** dimensionalization | `q = Nu · k ΔT / D`, with the absolute scale carried by 3 |

**⚠ The pre-registration is not touched.** (g)'s four cells, eight fixed values, target, sign
convention and decomposition stand **verbatim** — no re-registration, no widening, and **whichever cell
the result lands in, that cell's sentence is the verdict.** If it lands outside all four, the table is
recorded and the verdict is left to the owner rather than invented here.

**The ninth fixed value, which is why (h) held the verdict — both bodies, with their labels:**

| body | `T_p` | provenance |
|---|---|---|
| Earth | **1600 K** | declared, Unterborn+ 2019 §2 (`engine/eos.py@«EARTH_POTENTIAL_T = 1600.0»`) |
| Mars | **1600 K** | Earth's value **transferred**, `engine/bodies/mars.yaml` at `4ad07b07`; step 0 passed (criterion A max \|slope\| 0.0017, criterion B in at both ends) and the owner chose the transfer over the ~1500 K re-citation at **17:52** |

⚠ **The two being equal is the thing (h) warned about, and it is now a measured choice rather than an
implementation accident.** Criterion A measured that Mars's trajectory forgets this declaration —
0.0017 K of output per K of declaration — so a common `T_p` is no longer removing the physics the test
measures **by assumption**; it is doing so, if at all, at a rate step 0 bounded.

**How the build gets verified before it is run.** Four anchors, three of them named in C47 (e) before
any of this:

| anchor | what it checks |
|---|---|
| `Ra_i` over `T_i` = 1200–1800 °C against §4.1's printed *"∼10⁹ to ∼10¹³"* | the `θ`/`Ra_i` chain |
| `Ra_crit(n)` against the text's *"∼450 (n = 1), ∼134 (n = 2), ∼104 (n = 3)"* | eq. 44, already passing at n = 1 and 3 |
| Table 2's three `Δη` blocks, row by row | the stability solve, already in the gate |
| **`b` reproducing 50 mW/m² at the Earth condition** — by construction, so a miss means the dimensionalization is wrong | the new piece, and the only anchor the absolute scale has. ⚠ *Sharpened in (k) commit 3: the paper defines this on **eq. 30 without melting**, so the anchor reads `q_E` = 50.000 ± 10⁻³ **evaluated that way** — not on the eq. 29 path the runs use, which sits 3.98 % higher by construction* |

**⚠ And there is no absolute-scale anchor beyond that one, by the paper's own doing:** §4's planetary
results are **Figs 12–14 only**, with no printed dimensional flux. That was C47 (e)'s size verdict and
it has not changed.

**Carried in the same commit, because they touch the same file: the audit seat's three findings on
C47 (i).** Three bibcodes that carried no clickable link now have one (Putirka 2016, Yoshizaki &
McDonough 2020, Dong+ 2022); the banded-candidate count moves from three to **four**, since Herzberg+
2010's body band is now recorded — ⚠ *the count moves, the agreement test is still not recomputed*; and
Herzberg+ 2007's citation is pinned by its own sentence rather than by the words *"concluding
paragraph"*. ⚠ **One count is worth keeping beside them: the audit seat counted twelve distinct edits in
`8d83b03d` where this seat's report grouped them as seven.** Same work, but the smaller number is the
one that would leave a reader thinking less had changed — a report's grouping is not a count.

**This section is the head. The build is Brief 162**, and the recovery settles how it starts: the
inline runner is promoted to engine code, re-verified against the four anchors above rather than
trusted, and re-run at the two `T_p` labels. ⚠ **Three things in the recovered runner are questions for
that brief, named here before it starts** — it fits `b` with eq. 30 (`nu_asymptotic`) while every run
uses eq. 29 with the stability solve (`nu_full`), which is why its Earth flux comes out at 52 rather
than the 50 mW/m² it was fitted to — ⚠ *withdrawn in (k) commit 3: that fit is the paper's own printed
definition, and the 52 is the eq. 29 − eq. 30 difference*; it hardcodes `α = 2 × 10⁻³` inside `Ra_i` while sweeping `α` only
in the buoyancy term, so the paper's self-contradiction is resolved *two ways at once inside one run*;
and it sets `z*_D` from the melting-onset depth instead of iterating eq. 56's `z*_D = Nu⁻¹`, which is
missing piece 1 above. **None of these is a reason to discard it** — it is the fastest route to a
reproducible step 4 — but each must be decided in the open rather than inherited.

### C47 (k) 2026-09-08 — step 4's runner is promoted with its defects, and the 09-07 numbers reproduce

**Brief 162 commit 1. What is promoted is the 09-07 work seat's second inline block, arithmetic
unchanged**, from the recovery in C47 (j)
(`/Users/vana/Desktop/NearStars-artifacts/2026-09-08-c47-step4/c47_step4_recovered.md`, md5
`ce35dc0ad7d084a475b7242af75605d5`). It now lives in `engine/stagnant_lid.py` as four functions and
six constants plus `engine/tools/c47_step4.py`, and the tool checks every printed number of that run.

⚠ **What this reproduction is, and what it is not.** *It confirms that the same code produces the same
numbers — that promotion did not damage anything.* **It is not a physical anchor.** The independent
legs are the four anchors C47 (j) named, and the load-bearing one is **`b` reproducing 50 mW/m² at the
paper's own Earth condition** — ⚠ *which the promoted code passes exactly, once the anchor is read the
way §4 defines it (eq. 30, no melting): 50.0000 mW/m². The 52.02 in the runs is the eq. 29 − eq. 30
difference, not a missed fit — commit 3 below.* Commits 2–5 repair one defect each; the physics is
tested there, not here.

⚠ **And the blinding scope, stated as in (j):** this seat read the recovered numbers before writing the
runner, so they are a **reproduction anchor, not a blind target.** (g)'s four verdict cells predate all
of it, and the verdict is not written in this section.

#### The 09-07 numbers, reproduced

`b` = **4.1921 × 10¹⁰** (one global declaration, re-fit on the paper's Earth condition). Target
`q_Earth/q_Mars` = **3.68** (against our 0.454) or **4.78** (against Korenaga's 0.35), from the
no-melting baseline **1.372** — all three fixed in C47 (f)/(g) before any of this.

| `T_p` | body | depleted layer | as % of mantle | `z*_D` |
|---|---|---|---|---|
| 1350 °C | Earth | 61.8 km | 2.13 % | 0.9787 |
| 1350 °C | Mars | 163.8 km | 9.10 % | 0.9090 |
| 1500 °C | Earth | 108.2 km | 3.73 % | 0.9627 |
| 1500 °C | Mars | 286.7 km | 15.93 % | 0.8407 |

| `T_p` | `α` | run | `q_E` | `q_M` | **`q_E/q_M`** | `Ur_E` | `Ur_M` | `Ur_M/Ur_E` |
|---|---|---|---|---|---|---|---|---|
| 1350 °C | §3.2 `3.7e-5` | (a) dehydration only | 52.02 | 29.17 | **1.7832** | 0.803 | 0.612 | 0.762 |
| 1350 °C | §3.2 | (b) buoyancy only | 52.02 | 35.90 | **1.4492** | 0.803 | 0.498 | 0.619 |
| 1350 °C | §3.2 | **(c) both** | 52.02 | 29.17 | **1.7832** | 0.803 | 0.612 | 0.762 |
| 1350 °C | §4 `2.0e-3` | (a) | 52.02 | 29.17 | **1.7832** | 0.803 | 0.612 | 0.762 |
| 1350 °C | §4 | (b) | 52.04 | 39.06 | **1.3323** | 0.803 | 0.457 | 0.569 |
| 1350 °C | §4 | **(c)** | 52.02 | 29.17 | **1.7832** | 0.803 | 0.612 | 0.762 |
| 1500 °C | §3.2 | (a) | 51.04 | 23.42 | **2.1791** | 0.819 | 0.763 | 0.931 |
| 1500 °C | §3.2 | (b) | 105.33 | 77.74 | **1.3549** | 0.397 | 0.230 | 0.579 |
| 1500 °C | §3.2 | **(c) both** | 51.04 | 22.79 | **2.2396** | 0.819 | 0.784 | 0.957 |
| 1500 °C | §4 | (a) | 51.04 | 23.42 | **2.1791** | 0.819 | 0.763 | 0.931 |
| 1500 °C | §4 | (b) | 120.93 | 89.01 | **1.3586** | 0.346 | 0.201 | 0.581 |
| 1500 °C | §4 | **(c)** | 51.04 | 23.41 | **2.1800** | 0.819 | 0.763 | 0.932 |

**Seventeen anchors — twelve run cells, four depleted layers and `b` — all reproduce at the printed
precision** (`✅ 09-07 앵커 17/17 일치`, `rc=0`), and `engine/tools/c47_step4.py` exits `rc=1` if any of them moves. ⚠ **No verdict is read
off this table**, because four defects sit between it and the physics.

#### ⚠ The (g) fourth cell's premise is falsified, and (g) registered how to record that

C47 (g) reasoned that dehydration stiffening and compositional buoyancy *"push in opposite directions
on the asymmetry"*, and registered the consequence in advance: *"if (a) and (b) turn out to push the
**same** way, the fourth cell's reasoning is wrong and that gets recorded as this seat's error."*

**They push the same way.** Against the no-melting **1.372**, dehydration alone gives **1.7832** and
buoyancy alone **1.4492** — both **above** it, so by (g)'s own sign convention both mechanisms *help*.
**So the reasoning behind the fourth cell was wrong, and it is recorded here as the 09-07 seat's error,
in the form that seat registered for it.**

⚠ **What is true instead is stranger, and it is visible in the same rows.** At 1350 °C, **(c) equals
(a) to four decimals** (1.7832): with dehydration on, buoyancy adds *nothing at all*. At 1500 °C it
adds a little (2.2396 against 2.1791) under §3.2's `α` and almost nothing (2.1800) under §4's. And
(b)'s own absolute fluxes are the loudest thing in the table — 105.33 and 120.93 mW/m² on Earth, twice
the other rows — because with `Δη = 1` the dehydrated lid is not stiff and the flux is not suppressed.
**So the mechanisms do not oppose; the stiff lid dominates, and once it is on the density contrast is
nearly invisible.** That is a finding about the mechanisms, and it is not a verdict on the target.

#### Commit 2 — defect ④ repaired: one surface temperature, and the prediction held

**Registered before the run: Earth's flux moves by ≪ 1 %.** With `T_s` unified to a single 273.15 K —
so `ΔT` = `T_p` exactly and the `b` fit sits on the same condition the runs do — the twelve runs move
like this.

⚠ **Why 273.15 and not the paper's printed 273, stated because the paper is the source of the
ambiguity.** §4 prints the Earth condition as `T_s` = **273 K**, `ΔT` = **1350 K**, `T_i` = **1350 °C** —
mutually inconsistent by 0.15 K (1623.15 − 273 = 1350.15). Two resolutions exist: `T_s` = 273.15 makes
`ΔT` = `T_p` exactly and so reproduces **the paper's `ΔT` = 1350 K** exactly, while `T_s` = 273.0
reproduces the paper's printed `T_s` and leaves `ΔT` at 1350.15. **We take the first**, because `ΔT` is
the quantity the equations evaluate. Either way the fit and the runs now share one condition, which is
what defect ④ was about.

| what | before (09-07) | after | move |
|---|---|---|---|
| `b` | 4.1921 × 10¹⁰ | **4.2038 × 10¹⁰** | +0.28 % |
| `q_E` at 1350 °C | 52.02 | **51.98** | −0.04 mW/m² = **−0.08 %** |
| `q_E` at 1500 °C | 51.04 | **51.03** | −0.01 mW/m² = **−0.02 %** |
| `q_E/q_M` (c), 1350 °C | 1.7832 | **1.7823** | −0.0009 |
| `q_E/q_M` (c), 1500 °C | 2.2396 | **2.2398** | +0.0002 |
| depleted layers, all four | 61.8 / 163.8 / 108.2 / 286.7 km | **unchanged** | `z*_D` does not read `T_s` |

**The prediction held**, and the largest move anywhere in the table is `q_E` in the buoyancy-only rows
(105.33 → 105.23 and 120.93 → 120.81 mW/m², −0.1 %). ⚠ **No verdict is read here either** — this
subsection reports one change's size and nothing else.

⚠ **And the runner proved it can fail as well as pass**: `--anchors` returned `rc=0` at `aea75984` and
`rc=1` here, which is `docs/reference/derivation-discipline.md@«A check must prove it can pass and can fail before its result is written down»`
applied to the tool that guards the rest of this brief.

#### Commit 3 — defect ① is withdrawn: the eq. 30 fit is what the paper prints

**Read before repairing, and the repair turned out to be the mistake.** §4, printed:

> *"the pre-exponential factor `b` in eq. (1) is determined so that the surface heat flux is
> **50 mW m⁻²** at the present-day Earth condition (`D` = 2900 × 10³ m, `g` = 9.8 m s⁻², `T_s` = 273 K,
> and `ΔT` = 1350 K) **without the effects of mantle melting (i.e. Δη = 1 and Δρ = 1)**"*

and Fig. 12's caption — *"Reference viscosity is chosen so that **conventional scaling** predicts
surface heat flux of 50 mW m⁻² at `T_i` = 1350 °C"* — with the body naming *"the conventional scaling of
`Ra_i` (**eq. 30**)"*. **So fitting `b` on eq. 30 with melting off is the paper's own definition, and the
09-07 runner did what the paper says.**

| what | value |
|---|---|
| `q_E` at the paper's Earth condition **evaluated on eq. 30** (the definition) | **50.0000 mW/m²** — by construction |
| `q_E` on **eq. 29 + the stability solve**, melting off, same `b` | **51.9919 mW/m²** — **+3.98 %** |
| `b` if it were re-fitted on the eq. 29 path instead | 4.7452 × 10¹⁰ (**×1.1288** of 4.2038 × 10¹⁰) |
| what eq. 30 would then read — the departure from the paper's normalization | **48.0211 mW/m²** |
| effect on the verdict quantity (`q_E/q_M`, 1350 °C, (c), §3.2) | 1.7823 → **1.7311**, −2.9 %, **away from the 3.68 / 4.78 target** |

**So the choice is about faithfulness, not about the verdict**: `b` is one global declaration entering
both bodies, so the ratio barely moves — C47 (f) had already measured that at 3.7 % per decade of `b`
against 115 % for the absolute flux. **The paper's definition is kept, the alternative is recorded, and
nothing is re-fitted.**

⚠ **Whose error this was, recorded where the others are.** The pass line *"`b` reproduces 50 mW/m²"* was
set as an anchor in C47 (j) without checking which equation the paper normalizes on; **that was the
directing seat's — and the audit seat approved the same pass line, so two of the three legs were wrong
together**, which is the failure mode three separate legs exist to prevent. It is written here rather
than left in a message. The anchor is not deleted but sharpened: **`q_E` = 50.000 ± 10⁻³ evaluated on
eq. 30**, which the code passes.

⚠ **And the reclassification costs us an anchor, which has to be said plainly.** If `b` is *defined* by
"eq. 30, no melting, Earth = 50 mW/m²", then reproducing 50.000 at that condition is **a definition, not
a verification** — C47 (e)'s fourth anchor was never an anchor. **So the absolute scale has no
independent check at all**, exactly as (e) said when it noted that §4's planetary results are Figs 12–14
with no printed dimensional flux. The independent legs are **three**: `Ra_i`'s printed range over
`T_i` = 1200–1800 °C, `Ra_crit`'s ∼450 / 134 / 104, and Table 2's three `Δη` blocks row by row.

**That weakness does not reach the verdict, and the reason is structural.** The verdict cells read
`q_Earth/q_Mars` and `Ur_M/Ur_E` — **ratios** — and `b` is one global constant entering both bodies
identically, so it cancels to first order: C47 (f) measured the ratio's sensitivity at **3.7 % per decade
of `b`** against **115 %** for the absolute flux. **An unanchored absolute scale is a real limit on any
flux we would emit, and not a limit on the direction test.**

⚠ **And this is the ninth time today that reading the thing before building it changed the build** —
after existing code four times, a declared limit, a paper's own sentence, our own rule, and the recovery
that turned "build from nothing" into "promote and reproduce". **None of the nine was caught by the
gate.**

#### Commit 4 — defect ② repaired, and the repair proves the defect could not have mattered

**`α` now enters `Ra_i` as an argument, and `b` is fitted with the same `α`** — self-consistently, which
is the only way a normalization and the constant it normalizes can be read together. **The result is
that nothing moves, and that is the finding:**

| `α` | `b`, fitted with that `α` | `Ra_i` at the Earth condition | `q_E` (c), 1350 °C | `q_E/q_M` |
|---|---|---|---|---|
| §4's `2.0 × 10⁻³` | 4.203785 × 10¹⁰ | 1.360020 × 10¹⁰ | 51.9758 | 1.782288 |
| §3.2's `3.7 × 10⁻⁵` | **7.777002 × 10⁸** | **1.360020 × 10¹⁰** | **51.9758** | **1.782288** |
| ratio | **1.850000 × 10⁻²** | identical to every digit | identical | identical |

⚠ **`Ra_i ∝ α/b`, and `b` is fitted at the Earth condition, so `α` is absorbed by `b` exactly.** ⚠ *And
the claim holds only under that condition: **`α` is invisible through `Ra_i` while `b` is obtained by
fitting a fixed Earth condition.** Take `b` any other way — a literature value, a per-body grain size —
and the `Ra_i` path opens again silently. The sentence must never be written without that clause.* The `b`
ratio equals the `α` ratio to six digits (1.85 × 10⁻²), `Ra_i` is unchanged to every printed digit, and
all twelve runs are bit-identical to commit 3's. **So the paper's `α` self-contradiction cannot act
through `Ra_i` at all — it can only act through `ΔT*_ρ`**, which is where C47 (g) put it. `α` and `b` are
not separately identifiable, and the paper itself calls its normalization *"(arbitrary)"*.

⚠ **This means the split the audit seat proposed as commit 4's pass line — §3.2 and §4 giving different
`q_E` in the (a) rows — cannot happen, and its absence is not evidence that the argument was left
unwired.** The wiring is visible in the `b` column instead: two `α` values now produce two `b` values in
the ratio 1.85 × 10⁻², where before commit 4 there was one `b` for both.

**The counterfactual, recorded because it is the only way `α` in `Ra_i` bites.** ⚠ *Label first, because
"the paper's `b`" would be false: `b` is **not** printed anywhere in Korenaga 2009 — it is **our** global
declaration, fitted to the paper's Earth condition (C47 (d)). What is held fixed below is therefore
`b` = 4.203785 × 10¹⁰, the value fitted with §4's `α`. And the two rows were measured in scratch: **the
shipped code has no `b`-freeze mode**, by design, since freezing it is the mixing commit 4 exists to
prevent.* With that `b` held and `α` in `Ra_i` moved to §3.2's, `Ra_i` falls 54×:

| case, `α` in `Ra_i` only | `q_E` 1350 °C | `q_M` | `q_E/q_M` | `Ra_i` (Earth) |
|---|---|---|---|---|
| 2.0 × 10⁻³ (paper's `b` and `α` together) | 51.9758 | 29.1624 | 1.7823 | 1.360 × 10¹⁰ |
| 3.7 × 10⁻⁵ with the paper's `b` kept | **15.0253** | 12.5636 | **1.1959** | 2.516 × 10⁸ |

⚠ **And that case falls *below* the no-melting 1.372**, so even the mixed reading moves away from the
target. It is recorded, not adopted: mixing a `b` fitted at one `α` with runs at another is the thing
commit 4 exists to stop.

**One thing this settles in the good direction.** The `α` ambiguity's blast radius is now bounded: with
`b` fitted per `α` and eq. 56 solved, the two `α` values give **identical `q_E`, `q_M` and ratios in the
(a) and (c) rows to four decimals**, and differ **only in the buoyancy-alone (b) rows**. **So C47 (g) was
right, after the fact, to put `α` on the buoyancy axis** — the axis it registered as the one `α` could
move is the only axis `α` moves.

#### Commit 5 — defect ③ repaired: eq. 56's fixed point, and it takes the 1500 °C asymmetry away

**The recursion, as the paper states it.** §3.1: *"when the dehydrated layer becomes dynamically
unstable, that is, `Nu > 1/z*_D`, we can modify the depth-dependent viscosity"*, solved
*"recursively … until `Nu` converges. The convergence is usually achieved within a few iterations"*; §4:
*"eq. (56) is solved iteratively by setting `z*_D = Nu⁻¹` when `Nu > 1/z*_D`, to have a self-consistent
pair of the surface heat flux and the assumed viscosity and density structure."*

⚠ **The paper uses `z*_D` in two senses, and its own numbers say which sense the trigger takes.** This
was first written up as *our* reading justified by the alternative being implausible. Korenaga 2009 is
**held**, so it was read, and the grade improves: **the prose defines a coordinate, the numbers require a
thickness.**

**The chain, four printed steps and one confirmation.**

1. ⚠ **`δ` is a thickness, and `z*` increases upward — printed under eq. 20.** *"`T_i − T_s` =
   `1/(1−δ) ∫₀^{1−δ} T dz*`"*, and then: *"where **δ = Nu⁻¹** = (T_i − T_s)/ΔT_H. **The
   non-dimensionalized thickness of the top thermal boundary layer is the reciprocal of the Nusselt
   number**, and the internal temperature is defined as the average of temperature below the boundary
   layer."* The integral runs **0 → 1−δ** with prefactor `1/(1−δ)`, so the interior is `z* ∈ [0, 1−δ]`
   and **the boundary layer is the top slab `z* ∈ [1−δ, 1]`**.
2. **Eq. 47 puts the dehydrated layer at `z* > z*_D`** — `Z(z*)` is 1 below and `Δη` above — so there
   `z*_D` is a **coordinate** and the layer's **thickness is `1 − z*_D`** (Table 2's 0.75 → a lid 0.25
   thick).
3. **Eq. 49 substitutes a length into that slot**: *"self-consistent and solve the following equation
   recursively: `Nu = F_Nu(n, θ, Ra_i, Δη, Nu⁻¹)`, until `Nu` converges."* Eq. 48's fifth argument is
   `z*_D`; eq. 49's is `Nu⁻¹` = `δ`.
4. **So the trigger's `z*_D` is a thickness, by arithmetic on 1–3.** *"Is the dehydrated layer thicker
   than the boundary layer?"* is `1 − z*_D > δ`, i.e. `Nu > 1/(1 − z*_D)` — and the paper writes that
   condition as **`Nu > 1/z*_D`**. ⚠ **The symbol carries both senses in the paper's own text**, which
   is why the overload is the paper's and not our reading.
5. **Table 2 confirms which sense discriminates.** On our 30 transcribed rows (`Δη` = 1, 3, 10; `Nu`
   **3.09–7.22**): the coordinate threshold `1/0.75` = **1.333** has **0 rows below, 30 above** — the
   trigger would be permanently true and §3.1's two regimes, *"reduces surface heat flux even when the
   dehydrated lid is thinner"* versus *"eventually destabilized"*, could not both exist. The thickness
   threshold `1/(1 − 0.75)` = **4.0** has **15 below, 15 above**, and `δ = 1/Nu` (**0.1385–0.3236**)
   straddles the lid thickness 0.25 **15/15**. Fig. 8(a)'s caption puts its horizontal line
   `Nu = 1/z*_D` in the middle of the figure, not off its bottom edge.

**And the code already carries step 1's geometry:** `engine/stagnant_lid.py@«above = max(0.0, min(top, 1.0) - max(1.0 - delta, z_d))»`
measures the stiff share of a sublayer as the part above `z_d`, with the boundary layer occupying the
top `δ` — the same convention, written before any of this was read.

**So the overload is the paper's**, and it belongs beside its `α` self-contradiction (defect #24) rather
than in our list of reading choices. The implementation uses the thickness sense for the trigger and the
update, and the boundary-coordinate sense for `nu_full`'s geometry, which is what Table 2 fixes;
`nu_eq56` converts (`1 − thickness`).

**The third possibility, checked and closed:** the `Nu` in the trigger could have been a different
normalization from the one `nu_full` returns, which would dissolve the "always fires" objection. It is
not — the paper defines `Nu` as `δ⁻¹`, and `nu_stability` solves eq. 43 for `δ` and returns `δ⁻¹`.

**Under the thickness sense the trigger fires in 10 of the 24 body-cells** — two at 1350 °C (Mars's
buoyancy-only rows) and eight at 1500 °C (all three Mars runs plus Earth's buoyancy-only, both `α`).
⚠ *Corrected on the audit's count: "four of twelve" had mixed this up with the number of **cells that hit
the 50-iteration cap**, which was also four.*

| where it fires | initial `d/D` | `1/(d/D)` | `Nu` before | fires? |
|---|---|---|---|---|
| Earth, 1350 °C, (a)/(c) | 0.0213 | 46.89 | 27.91 | no |
| Mars, 1350 °C, (a)/(c) | 0.0910 | 10.99 | 9.72 | no |
| Mars, 1350 °C, (b) | 0.0910 | 10.99 | — | **yes** |
| Earth, 1500 °C, (a)/(c) | 0.0373 | 26.80 | 24.66 | no |
| **Mars, 1500 °C, all three** | 0.1593 | 6.28 | 6.83–7.02 | **yes** |
| Earth, 1500 °C, (b) | 0.0373 | 26.80 | — | **yes** |

**What it does to the twelve runs:**

| `T_p` | run | `q_E/q_M` before | after | move |
|---|---|---|---|---|
| 1350 °C | (a), (c), both `α` | 1.7823 | **1.7823** | unchanged — does not fire |
| 1350 °C | (b) §3.2 | 1.4492 | **1.4276** | −0.0216 |
| 1350 °C | (b) §4 | 1.3323 | **1.3319** | −0.0004 |
| **1500 °C** | **(a), both `α`** | 2.1791 | **1.5838** | **−0.5953** |
| **1500 °C** | **(c) §3.2** | 2.2396 | **1.5838** | **−0.6558** |
| **1500 °C** | **(c) §4** | 2.1800 | **1.5838** | −0.5962 |
| 1500 °C | (b) §3.2 / §4 | 1.3549 / 1.3586 | 1.3467 / 1.3584 | −0.0082 / −0.0002 |

⚠ **And at the verdict temperature eq. 56 never fires — so commit 5 moved the exploratory column and
left the verdict cells untouched.** At the declared 1600 K (1326.85 °C) the dehydrated layer is thinner
than the boundary layer on both bodies: Earth `1/(d/D)` = **53.03** against `Nu` = **24.67**, Mars
**12.43** against **10.13**, and the recursion exits at zero iterations in all 24 declared-`T_p` cells.
**Commit 6's 1.5114 is the same number before and after this repair**, which is worth knowing before
anyone reads the verdict as resting on eq. 56.

⚠ **The self-consistent lid is thinner, so Mars leaks more**: at 1500 °C Mars's dehydrated layer falls
from 15.93 % of the mantle to **10.35 %** and its flux rises **22.79 → 32.22 mW/m²**, while Earth's is
untouched at (a)/(c). **The 1500 °C column, which had been the best case for the test, loses most of its
asymmetry.** The largest `q_E/q_M` anywhere in the table is now **1.7823**, at 1350 °C — **48 % of the
3.68 target and 37 % of the 4.78 one.**

⚠ **And the paper's "a few iterations" is not our experience, which is worth recording as a limit of the
transcription rather than of the paper.** The `(b)` rows converge in **4–14** iterations, as advertised.
The `Δη = 100` rows at 1500 °C take **117–129**, and the rate is linear with a ratio that **drifts
upward**: `Nu·z*_D − 1` falls by **0.66–0.73× over the first four steps, 0.8194× at the fifth — one step, not a
stretch — and 0.8466× from the sixth to the end** (measured on Mars 1500 °C (a): residuals
1.187 × 10⁻¹ → 7.892 × 10⁻² → 5.404 × 10⁻² …). ⚠ *"≈ 0.82 through the middle" was a single point written
as an interval; corrected on the audit's trace.* At the tail rate 10⁻¹⁰ needs **~125** steps, which is what the observed 117–129
are. ⚠ *Corrected on the audit's measurement: "≈ 0.7× and ~60 steps" read the early rate as if it were
the asymptotic one.* **The cap was 50 and four cells hit it**; it was raised to **400** after the rate was measured, and `nu_eq56` reports `converged: False`
rather than returning a number if it is ever hit. **The runner now takes ~61 s.**

⚠ **And the reason the paper's "few iterations" does not describe our runs is that the recursion is
running outside the region the paper exercised** — the same shape of finding as C48, where two of one
paper's numbers failed to compose on a second body. The paper's claim of *"trivial differences (< 0.1 per
cent)"* is made for `Δη` ≤ 10 with Table 2's `Nu` of **3.09–7.22** (our 30 transcribed rows). **We run
`Δη` = 100 at `Nu` = 9.67–27.9** — **10× outside in `Δη`, 1.3–3.9× outside in `Nu`** — and there the recursion is not trivial: Mars at 1500 °C moves its
dehydrated layer from **15.93 % to 10.35 %** of the mantle and its flux by **+41 %**. **That is an
extrapolation, and it is a limit on the 1500 °C exploration rather than on the verdict** — at the
declared 1600 K the trigger never fires (above), so the verdict cells contain no extrapolated
recursion.

#### Commit 6 — the verdict: neither `α` reaches the target, which is C47 (g)'s first cell

**Run at the declared potential temperatures, read from the body files rather than typed in: Earth
1600 K (Unterborn+ 2019, `engine/eos.py@«EARTH_POTENTIAL_T = 1600.0»`) and Mars 1600 K (transferred,
step 0 passed, owner 2026-09-08 17:52).** ⚠ *Both declarations are the same number today, so this set
coincides with a common-`T_p` case — **because Mars carries Earth's value, which is a provenance fact,
not a physical coincidence.** The moment Mars gets a Martian `T_p`, this set separates from the common
one.* In °C, which is what eq. 45 takes: **1326.85 °C** for both.

| body | depleted layer | as % of mantle | `z*_D` |
|---|---|---|---|
| Earth | 54.7 km | 1.89 % | 0.9811 |
| Mars | 144.8 km | 8.05 % | 0.9195 |

| `α` | run | `q_E` | `q_M` | **`q_E/q_M`** | of 3.68 | of 4.78 | `Ur_E` | `Ur_M` | `Ur_M/Ur_E` |
|---|---|---|---|---|---|---|---|---|---|
| §3.2 `3.7e-5` | (a) dehydration only | 45.15 | 29.87 | **1.5114** | 41.1 % | 31.6 % | 0.926 | 0.598 | 0.646 |
| §3.2 | (b) buoyancy only | 45.15 | 32.67 | **1.3818** | 37.5 % | 28.9 % | 0.926 | 0.547 | 0.591 |
| §3.2 | **(c) both — the test** | 45.15 | 29.87 | **1.5114** | **41.1 %** | **31.6 %** | 0.926 | 0.598 | 0.646 |
| §4 `2.0e-3` | (a) | 45.15 | 29.87 | **1.5114** | 41.1 % | 31.6 % | 0.926 | 0.598 | 0.646 |
| §4 | (b) | 45.15 | 34.09 | **1.3243** | 36.0 % | 27.7 % | 0.926 | 0.524 | 0.566 |
| §4 | **(c) both** | 45.15 | 29.87 | **1.5114** | **41.1 %** | **31.6 %** | 0.926 | 0.598 | 0.646 |

**The verdict, read off C47 (g)'s pre-registered table and not composed here.** The target was
`q_E/q_M` ≥ **3.68** (against our own `Ur_Earth` 0.454) or **4.78** (against Korenaga's 0.35), from the
no-melting **1.372**. The best cell is **1.5114**, both `α`, so:

> **neither `α` reaches the target** → the **fourth** law family to fail in the same direction. C47
> closes as *named, not filled* — the recorded answer becomes "no single untuned law in this literature
> reproduces both Urey ratios", and the three-families-same-direction note in C47 (c) closes with it

*(quoted in C47 (g)'s own formatting; the words are unchanged from that cell.)*

**Said in Urey terms, which is where the failure is legible.** The law hands Earth `Ur` = **0.926**
against a literature 0.35–0.454, and Mars **0.598** against 0.68–0.75 — so it makes **Earth** look like
the body that retains its heat and **Mars** the one that has cooled, `Ur_M/Ur_E` = **0.646** where the
literature wants roughly 1.5–2.1. ⚠ **The melting correction moved the ratio the right way** (1.372 →
1.5114, +10 %) **and by nowhere near enough**, and eq. 56's self-consistency took back most of what the
1500 °C case had appeared to offer.

**What this closes and what it does not.** It closes step 4, and with it C47 as *named, not filled*.
⚠ **C34 and C46 are not touched here** — the candidate set C34 waits on is re-drawn by this result, and
that is the next brief's work, not this section's. **Nothing in `db/`, no board row and no emitted value
depends on any number above**; the step-4 path has never had a consumer.

⚠ **And the honest limit on all of it, restated because a closing section is where it would be
dropped:** the absolute scale has **no independent anchor** (commit 3), so these fluxes are not a
prediction of anyone's heat flow — the verdict rests on the **ratio**, which is what the pre-registration
put the threshold on.

#### Commit 7 — the gate now checks step 4, and the two references are kept apart

**Two reference tables, and the distinction is the point.** `ANCHORS` holds the 09-07 run's printed
numbers and is **frozen** — it passes only at `aea75984`, because commits 2–6 repaired defects and the
numbers were *supposed* to move. `EXPECTED` holds **this commit's** numbers and is updated whenever a
change is justified. **`--anchors` demands the first; the default mode demands the second, and the gate
runs the default.**

⚠ **Why both are needed, stated as the failure each one prevents.** Keeping only the frozen anchors
means every commit after the first reports a red herring, so the check gets ignored. Updating the
anchors each commit means they stop being anchors — there is then nothing that says the promotion was
faithful. And having no current table at all is the hole this commit closes: **a regression in
`stagnant_lid.py` would have passed the gate silently**, since nothing in the gate evaluated step 4.

| mode | reference | cells | verdict at this commit |
|---|---|---|---|
| default (in the gate) | `EXPECTED` + `DEPLETED_EXPECTED`, current | **26** | **`rc=0`** |
| `--anchors` | `ANCHORS` + `DEPLETED_ANCHORS`, 09-07, frozen | **17** | **`rc=1`** — 13 cells moved, as commits 2–6 intended |

⚠ **Two holes in the first version of this check, found by the audit seat.** The depleted-layer
comparison sat **inside the `if not quiet:` block**, so the gate — which runs `--quiet` — never evaluated
it: printing and checking were one statement, and silencing one silenced the other. And the
**declared-`T_p` depleted layers were in no table at all** (Earth 54.7 km / 1.89 %, Mars 144.8 km /
8.05 %), so the verdict set's geometry was unguarded. Both are now checked in both modes, which is why
the default count is **26** and not the 24 first reported here.

**Cost, stated because the discipline asks for it: ~62 s added to the gate**, which is eq. 56's fixed
point iterating 117–129 times in the four `Δη = 100` rows at 1500 °C. `scripts/check.sh@«C47 4단계 방향 시험 (브리프 162)»`
carries the same number beside the call.

#### Where the checks were wrong, recorded because two of three legs failed together

**Four pass lines set by other seats were withdrawn on evidence during this brief**, and they are worth
listing beside this seat's own errors:

| pass line | withdrawn because |
|---|---|
| *"`b` must reproduce 50 mW/m²"* on the eq. 29 path — **directing seat, approved by the audit seat** | §4 defines the normalization on eq. 30 without melting; the 52 is the two equations' difference (commit 3) |
| *"the (a) rows must split between the two `α`"* — audit seat | `Ra_i ∝ α/b` and `b` is fitted, so `α` is absorbed exactly; the split cannot occur (commit 4) |
| *"Table 2's `Nu` is 2.76–6.03"* — audit seat | that is Table **3**; Table 2's 30 rows are 3.09–7.22 |
| *"our runs are at `Nu` 24–45"* — audit seat | a flux converted as if it were a `Nu`; the `Δη` = 100 cells are 9.67–27.9 |

⚠ **The first line is the one to keep: the directing seat set it and the audit seat approved it, so two of
the three legs were wrong at once** — and what caught it was neither leg but **reading the paper before
repairing the code**. Three legs are not three checks when two of them share a reading.

#### The four defects, named before any of them is repaired

| # | defect | why it matters | repaired in |
|---|---|---|---|
| ~~①~~ | `b` is fitted with **eq. 30** (`nu_asymptotic`) while every run uses **eq. 29 + the stability solve** (`nu_full`) | ⚠ **withdrawn — not a defect.** §4 defines the normalization exactly this way, and the 52 is the two equations' difference. Commit 3 records it instead of repairing it | ⚠ **no repair** |
| ② | `Ra_i` hardcodes **`α = 2 × 10⁻³`** (§4's printed value) while `α` is swept only in the buoyancy term | one run then takes **both halves of the paper's self-contradiction at once**, which is not what (g) registered — (g) asked for the two `α` read side by side, not mixed inside one run | commit **4** — repaired, and ⚠ *it moved nothing: `α` is absorbed by `b`* |
| ③ | `z*_D` is set from the **melting-onset depth**, not iterated as **eq. 56**'s `z*_D = Nu⁻¹` | the paper's outer solve is a fixed point; ours is a single geometric guess | commit **5** — repaired, and ⚠ *it removed most of the 1500 °C asymmetry: (c) 2.2396 → 1.5838* |
| ④ | `T_s` is **mixed inside one run**: `T_i = T_p + 273.15` but `ΔT = T_i − 273.0`, so `ΔT` = 1350.15 K at `T_p` = 1350 °C — while the `b` fit line uses the literals **1350.0 / 1623.0** | the fit condition and the run condition differ by **0.15 K** | commit **2**, and it goes first |

⚠ **④ was repaired first, and the reasoning that put it there survives its neighbour's withdrawal.** A
fit's fixed point is exact only at the condition it was fitted on, so a `T_s` mixed between the fit line
and the runs would have contaminated any statement about the normalization. It was unified first (one
273.15 K), and the normalization then turned out to need **no repair at all**. **Each commit reports how
far its own change moved the twelve runs, and no commit reports two changes at once.**

**⚠ What is promoted is the second block (16:39:56), and the difference from the first is `θ`'s
definition — this matters enough to state where a reader will trip over it.** The first block (16:39:22)
used `θ = E ΔT / (R T_i)` and died with `OverflowError` inside `_ra_local_max`'s
`d_eta ** frac * exp(θu/2)`; the second uses **`θ = E ΔT / (R T_i²)`**, the Frank-Kamenetskii form, and
runs. **Run the `T_i` form and `b` comes out at `6.0416 × 10⁻³` — a factor `6.94 × 10¹²`, 12.8 orders
of magnitude, from `4.1921 × 10¹⁰` — and none of the twelve rows reproduces.** Both figures were
re-derived at this tree before this section was written, and both match what the recovered blocks
printed. ⚠ **The overflow has a one-line cause:** at `ΔT` = 1350 K and `T_i` = 1623 K the `T_i` form
gives `θ` = **30 014** against the Frank-Kamenetskii **18.49**, and `_ra_local_max` evaluates
`exp(θu/2)` — `exp(15 007)` is not a float. ⚠ **The promoted code is the `T_i²` form**, and
`engine/stagnant_lid.py@«실행된 것은 이 정의다»` says so where a reader will look.

⚠ **`b` is re-fitted rather than pinned to the printed digits.** The 09-07 run printed `4.1921e+10` to
four significant figures and used the bisection's full precision; declaring the printed value as the
constant would not reproduce the run. So `fit_b_eq30()` solves the same bisection and
`B_GRAIN_RECORDED` carries the printed value **for comparison only**.

### C48 — the integrator was validated on Earth, and Earth survived by not blowing up rather than by being right — **closed 2026-09-08: domain (Brief 155) + step (Briefs 156–157)**

**This one number is the whole item:**

> ⚠ **`2.3 × 10¹⁰ Pa·s`** — the mantle viscosity `core_history` asks Nimmo's law for, at the
> temperature it starts Mars from. **That is not a mantle.** Solid rock near its solidus is
> `10¹⁸–10²¹`; this is eight orders below the bottom of that, in the neighbourhood of a warm lava
> rather than of a convecting mantle. Earth's own start asks for `4.3 × 10¹⁴` — still four orders
> under solid rock.

**C20 ran on a second body for the first time today and diverged.** Mars's mantle integrates to
`T_m = −6244 K` at the declared potential temperature of 1600 K, and to −6977 … −8208 K across the
whole pre-registered 1400–1800 K sweep. Every point. ⚠ **The divergence is not the interesting part** —
a body that survives the same call is not thereby getting a right answer.

**What the flux law returns at the temperatures the integrator actually feeds it:**

| body | `T_m` | `F_t` | `Q_M` | measured, for scale |
|---|---|---|---|---|
| Mars | **4021 K** (its initial condition) | **719,546 mW/m²** | **103,882 TW** | Parro+ 2017: **19 mW/m²** |
| Mars | 1600 K | 55.6 | 8.03 TW | Reese ceiling 15–30 mW/m² |
| **Earth** | **3040 K** (its initial condition) | **25,144 mW/m²** | **12,825 TW** | Davies & Davies 2010: **92.1 mW/m², 47 TW** |
| Earth | 1600 K | 76.9 | 39.2 TW | — |

**Earth is called at 273× its own measured flux and Mars at ~38,000× Parro's.** ⚠ **Earth's numbers
come out of the same out-of-range call; Earth simply has the mantle heat capacity to survive it.**
That is the finding, and it is about C20 rather than about Mars.

**Why, precisely — and the answer is not the one this seat first reached for.** `mantle_flux.py`
declares `BRACKET_K = (1000, 2500)` and its `consistency` path refuses outside it by name. `core_history`
calls `implied_flux` directly with no such check. But ⚠ **that bracket is ours, not Nimmo's**: its own
comment calls it *"the bisection bracket"*, and `invert_for_flow`'s docstring dates it to Brief 57,
where a bisection on the **inverse** problem was returning an endpoint as a value. **Nimmo+ 2004 prints
no validity range for eq. 35 at all.**

**The real constraint is in the equation's form.** Eq. 35 is a linear-exponential expansion about a
reference temperature, and Nimmo's Table 2 fixes it: *"We adopt this value for `T₁` and **1573 K for
`T₀`**"*, with `η₀ = 10²¹ Pa·s` there. Evaluated away from that point:

| `T_m` | distance from `T₀` | viscosity | as a fraction of `η₀` |
|---|---|---|---|
| 1600 K — Nimmo's own present-day Earth | +27 K | 7.6 × 10²⁰ Pa·s | ÷ 1 |
| 2500 K — our bracket ceiling | +927 K | 9.4 × 10¹⁶ | ÷ 10,615 |
| **3040 K — C20's Earth initial** | **+1467 K** | 4.3 × 10¹⁴ | **÷ 2,350,174** |
| **4021 K — C20's Mars initial** | **+2448 K** | 2.3 × 10¹⁰ | **÷ 42,808,392,211** |

So no published range was violated — **none is printed** — and **a linearisation was evaluated 1467
and 2448 K from its expansion point.**

⚠ **The obvious repair does not exist, and it is the first thing the next reader will reach for.**
`BRACKET_K` looks like the guard that failed, so widening it — or adding it to `core_history`'s call —
looks like the fix. **It is not.** That constant is ours and it is about a different problem (a
bisection on the inverse map, Brief 57). Enforcing it would turn a wrong number into a refusal, which
is better, but it would not give the integrator a flux at 3000 K. **There is no value of `BRACKET_K`
that makes eq. 35 usable 1500 K from its expansion point.**

**⚠ And the sharpest way to say it: two numbers from the same paper do not compose on a second body.**
The 4800 K initial condition is what Nimmo prints **for Earth**, and the flux law's blow-up point moves
with gravity and radius, so it sits **somewhere different on every body**. A starting temperature that
Earth barely survives is outside the usable region on Mars. **Not our arithmetic error — a
composition failure between two of one paper's own values**, found only by running a second body.

⚠ **That generalises past C20, and it is the reason to record it somewhere wider.** This engine
declares Earth's numbers on every rocky body by design — `MANTLE_SHARE = 0.70`, `T_s = 293 K`,
Korenaga's `b`, and now Nimmo's 4800 K. **The pattern is sound and this is its failure mode: a transfer
that is safe on the body it came from can be outside the usable region on another, and only running the
second body shows it.** Transfers need a per-body check, not just a label.

**Blast radius, counted rather than estimated.** `core_thermal_history` has **one** consuming edge —
`core_entropy_production` (`chain.yaml`, `kind: influences`) — plus `core_entropy.py` and its test.
**No board row and no `db/` entry stands on any C20 output.** Nine markdown records mention
`entropy_history_verdict`. ⚠ **And one C20 output was used in argument today**: C47 (h) cited Earth's
`mantle_potential_temperature_present = 1525 K` as evidence that route (ii) already produces a value.
**It does — from an out-of-range call.**

**⚠ Not repaired tonight, and the two directions are named rather than taken.**

1. **A flux law the integrator can use at early high temperatures.** Not this one, outside ~1573 ± a
   few hundred K.
2. **Starting the integration inside the usable region, on grounds.** ⚠ **This is not "lower the
   initial temperature until it runs."** Choosing a starting value because it integrates is the defect
   this whole item exists to name. A grounded starting *epoch* is a different thing from a working
   starting *value*.

**⚠ And C47's verdict does not move.** Inside the usable region — Mars at 1600 K — the flux is
**55.6 mW/m²**, about **2× Reese's own ceiling** for Mars. The original defect stands exactly where
C47 (b) put it. **The divergence is a separate cause, and repairing it would not make the direction
test pass.**

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
1.770 mW/m² at C20's `T_p` 1377.03 K and 8.923 at the declared 1600 K, at both lid thicknesses (350 and
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
| **each body at its own C20 temperature** — ✅ **the owner's row** | 4.251 | 8.780 | ✓ **as registered** |
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
1.7704573721 mW/m², Urey 4.25068708 and 8.78022345, all six regression rows unchanged).

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
Mars's Urey goes **8.780 → 9.716** across Breuer & Spohn 2003's printed lid band 350 → 500 km, **+10.7 %**,
purely through `A_man = 4π(R_p − δ)²` — the flux itself does not read `δ` at all. **So a cell scored on
Urey inherits the lid-thickness band**, and no printed value picks a point inside it.

⚠ **Decision ③ (C34's feed) is still held**, exactly as C25 (f) recorded, and nothing in this brief
changed the transport table's input.

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
returns. The test that covers it costs 459 s and was deferred to the gate rather than run before the
commit — the gate caught it in the isolated lane, which is what that lane is for, and the scratch was kept
because `rc=1`.

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
