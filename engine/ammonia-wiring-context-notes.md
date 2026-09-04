<!-- C22 — 얼음거대행성 맨틀에 암모니아 분율을 선언 인자로 배선한다. step 1 = 기본값 0, 비트 동일. 사전등록 → 실행 기록 -->
# Ammonia wiring — context notes (C22, step 1)

2026-09-03. **§1–§3 are the pre-registration, committed before any code ran.** §4 is filled in after the
run. Owner's decision, verbatim (`4b8e06ba`): *"1로 하되 조심히 접근하자."* The grounds are in
`ammonia-table-context-notes.md` §"Grounds for the next decision" and `interior-core.md` C22; not re-derived
here.

## 1. What the survey settled before code (parallel seat, three sentences reproduced by the work seat from the cache)

- **Methane's precedent does not transfer.** Bethkenhagen+ 2017 (`1709.04133.md`), the paragraph *before* the
  methane sentence that closed C4's methane half: *"pure ammonia becomes superionic as well but only below
  4000 K (Bethkenhagen et al. 2013)"*. ⚠ Extraction note: the PDF's text layer splits the word (*"superi
  onic"*), in this seat's `pdftotext` run with and without `-layout`; grep the ar5iv `.md` or search
  `superi`. The decomposition products also differ — methane polymerises into long chains, ammonia
  elementises into **N₂ + H₂** (2013 §III: *"the formation of H₂ and N₂ molecules, which is a clear sign that
  the ammonia molecules are at least partially dissociated"*).
- **In our bodies it is not even superionic — it is fluid.** 2013 §III A, Redmer+ 2011 isentropes laid on their
  phase diagram: *"Neither of the isentropes crosses the superionic phase albeit the isentrope of Neptune is
  located very close to the superionic region at 3000 K. According to our phase diagram, ammonia is very
  likely to only occur as a fluid under conditions present in the interior of Uranus and Neptune."* ⚠ "Fluid"
  splits into molecular and dissociated fluid and **the sentence does not say which**; 2017's Fig. 6 caption
  marks *"partial dissociation of ammonia into N₂ and H₂"* on the Uranus model **in the figure only, with no
  printed coordinates**. Both go on the emit label when w > 0.
- **The low-pressure / envelope branch is closed, two reasons.** (i) The *"low-density dissociation corner"*
  (ρ 0.5 g/cm³ · 3000 K) sits at a printed **1.906 GPa** but **3000 K** — a hot, dilute supercritical fluid,
  not an envelope state. (ii) The table's lowest isotherm is 500 K, so real envelope conditions are not in it
  at all; and 2017's structure models put the ice-rich layer **below** *"P₁₋₂ = 10–15 GPa between the outer
  H/He-rich and the inner ice-rich envelope"*. **Target layer: the mantle. `ENVELOPE_WATER` is not touched.**
- **A first-order transition the interpolation crosses, at three isotherms** (2013 §IV A): *"continuity
  between 1.8 g/cm³ and 2.0 g/cm³ in the 3000 K isotherm which coincides with the phase transition between the
  superionic and the dissociated phase. This is a strong indication for a first-order phase transition"*;
  *"the same behavior … for the 1000 K and 2000 K isotherms, but it is less pronounced … between 1.3 g/cm³ and
  1.5 g/cm³"*; *"the same effect should occur … at 500 K between 1.0 g/cm³ and 1.3 g/cm³, but it is probably
  too small to be seen"*. The table does not mark any of them. **Pressures are ours, not the paper's**: Table I
  rows at 3000 K give 1.8 g/cm³ → 59.40 GPa and 2.0 g/cm³ → 76.45 GPa; the paper attaches no pressure to the
  transition.
- **Correction to `ammonia-table-context-notes.md`** (line ~106): the 17.3 % worst interpolation point (ρ 0.5 ·
  3000 K) is **not** in *"the same corner the 5 % flags sit in"* — `ammonia_table.py`'s five flags are at
  4000 K (0.5 · 0.75 · 1.0 g/cm³) and 5000 K (0.5 · 0.75); none at 3000 K. *Adjacent (the hotter neighbour)*,
  and the asterisk means **convergence error** (Appendix: *"uncertainty of up to 5%"*), not dissociation.

## 2. Design — the shape of `mantle_rock_fraction` (C5), nothing new

- New declaration **`ammonia_mass_fraction`** (default **0.0**) on `integrate`, `solve_with_temperature`,
  `solve` (and the `inputs` record), threaded exactly where `mantle_rock_fraction` is.
- In `integrate`, at the deep-mantle water wrap (`in_column and p > water_table.P_MAX_PA`, where `with_rock`
  is applied today): `with_ices(water_mat)` = `mix(water_mat, 1 − w; NH3, w)` when w > 0, else **the same
  object**; then `with_rock` as today. Order: ices first, rock second — the rock fraction is of the ice
  mantle, the ammonia fraction is of its ices.
- Validation as for rock: `0 ≤ w < 1`; needs `imf > 0`; needs a potential temperature (the table is (ρ, T)
  and `Mixture.grad_ad` is c_P-weighted). `_stack` untouched.
- Three labels on the emitted note whenever w > 0 (C22 in `interior-core.md`): methane asymmetry (0.31 vs
  0.08, methane not built); table ceiling below the mantle base (≈ 290–333 GPa vs 820–1016 GPa); convention
  caveat on the adiabat (density grounded, thermal not); plus the survey's two: fluid but molecular-vs-
  dissociated unsaid; partial dissociation into N₂ + H₂ marked only in a figure.
- **`integrate` and `solve` are path-fingerprint functions**, so the fingerprint changes and
  `test_ice_giant.py --refresh` rides in the same commit — **and the refreshed values must equal the old
  ones bit for bit.** The two sentences are not a contradiction; together they are this step's test.

## 3. Pre-registered outcomes

- ① **Default 0 is the old path**: after `--refresh`, every frozen value (`radius`, `nmoi`, `core_pressure`,
  `core_temperature`, …) is byte-identical to the previous `ice_giant_anchor.json`; only `path_fingerprint`
  and `frozen_at` change. *Expected: at w = 0 the wrap returns the same material object.*
- ② **Any value moves** → stop, trace, do not absorb into the refresh. *Not expected.*
- ③ **Opt-in point check confirms §113's prediction**: at w = 0.1159 the mixture built by the wrap gives
  ρ_mix/ρ_H₂O on §113's eight (P, T) points inside **0.9654–0.9705** (−2.9 to −3.5 %), the table's own
  numbers. *Expected — it is the same two materials and the same rule.*
- ④ **Opt-in full solve of Uranus at w = 0.1159**: expected to **refuse by name** — the ammonia table refuses
  above its ceiling (`ammonia_table.density` → `PhaseGap`, ceiling 237–333 GPa by isotherm) and the mantle
  reaches 820 GPa. The refusal is the step-2 prerequisite (a deep-mantle rule) made visible. If it
  **converges**, the evidence gate was not consulted on this layer → trace. If the trial corridor **cycles**
  instead of concluding → record with the cold-flank family (Brief 22's steering rule).
- ⑤ Gate FAIL 0, and what the step adds to its time.

## 4. Run record — 2026-09-03, step 1 wired

**Branch fired: ① exactly, ③ exactly, and ④ in a kind that was not registered — recorded as such.**

- **①** `test_ice_giant.py --refresh` after the wiring: **only `path_fingerprint` changed**
  (`708ff4627f24c448` → `8021c2c929cb7f0b`); every body field of both anchors (`radius`, `nmoi`,
  `core_pressure`, `core_temperature`, the standalone record, `converged`) is **byte-identical** to the
  pre-wiring file (diffed field by field against a copy taken before the refresh; `frozen_at` same date).
  Uranus 25 s · Neptune 58 s. `--fast` passes. The default-0 path is the old path.
- **③** The wrap's own mixture (`mix(h2o_hot 0.8841, nh3 0.1159)`) on §113's eight (P, T) points gives
  ρ_mix/ρ_H₂O = **0.9654 · 0.9684 · 0.9685 · 0.9687 · 0.9674 · 0.9689 · 0.9700 · 0.9705** — the §113 table to
  four decimals at all eight. The wiring produces the predicted −2.9 to −3.5 %.
- **④ — unregistered kind: refused by name on the trial corridor's cold flank, before any ceiling.** The
  opt-in Uranus solve at w = 0.1159 died in **0 s**: *"152.00 GPa at 545 K is outside Bethkenhagen, French &
  Redmer 2013 … Table I (0.360–22.4 GPa at this temperature)"*. Spy: `NH3.density` fired **4** times,
  **4** refusals, max pressure touched 164 GPa. The state is the temperature loop's first trial (centre
  guess 2 × 76 K), a cold adiabat that puts 545 K at 152 GPa — **a state no converged column occupies** (the
  converged mantle is ~3 500 K there). The registered prediction (refusal at the 333 GPa ceiling on the
  converged column) never got a chance. **Mechanism, read from the code, not fixed**: `Ammonia.density`
  re-raises the table's `ValueError` as `PhaseGap(name, p, msg, t)` **without `too_cold`**, so Brief 22's
  steering (trial refusals steer the temperature bracket instead of killing the solve) does not engage — the
  shoot reads a cold-flank refusal as geometry and dies. This is the cold-flank family's newest member
  (`interior-core.md` rules: *"a trial-path refusal steers the bracket; it does not kill the solve"*), and it
  means **step 2 has two prerequisites, not one**: the deep-mantle rule (registered) **and** a cold-flank
  label on the ammonia table's refusals (new). Neither is done here — measurement, not repair, and both
  touch what the owner has not decided.
- **⑤ Gate on `2b869096`: FAIL 1** — 20:11:57, 456 PASS: `check_contracts` caught the new input missing from
  the contract (*"interior_layers: 코드가 쓰는데 문서 Needs 에 없다 — ammonia_mass_fraction"*). The check did
  its job: a declaration is not wired until the methodology doc's Needs line and domain table carry it. Added
  (en + ko, one row beside the rock declaration), `check_contracts` 8/8, re-gated below. **Worth its own
  sentence: this was the day's first FAIL, and the contract check — not a person — caught the code–document
  divergence**; that is the reason the check exists, and it becomes a pre-registration checklist line (§5).
  **Gate on `20776346`: FAIL 0, 457 PASS, 20:13:26 → 20:39:51 = 1585 s.** ⚠ That is +292 s on gate66's
  1293 s **on the same code** (gate66 → gate67 differs by the two methodology docs only), so the extra is not
  the wiring; the step's own cost is gate66's +13 s over gate65's 1280 s, itself within run-to-run noise. The
  1585 s is unexplained by this seat (no competing gate or solve was running; a single `ps` at 20:39 showed
  only this gate) and is recorded rather than attributed. *Trend, for the next time it jumps*: today's gates
  ran 1224 → 1268 → 1280 → 1293 → 1585 s; the first four carry a cause (one new 0.81 s row plus noise), only
  the fifth jumps. **Attributed the same evening by the owner, not by a session** (`4b8e06ba`): *"그거 아마
  내가 절전모드 잠깐 켜서 그런걸거야."* — the owner reports switching low-power mode on briefly in that window.
  Recorded as *reported cause, not verified as the cause* (the owner's own "아마"); the thermal-throttling
  hypothesis that stood here is withdrawn, and the re-run check is not needed — the cause is not in the code.
  This is the fourth time today that a fact living only outside the repository (owner / transcript) filled a
  gap the code could not; gate times with no cause in the code will keep being that kind of number.

**Labels landed in code**: at w > 0 the recipe's note carries the five (methane asymmetry · ceiling below the
mantle base · convention caveat on ∇_ad · fluid but molecular-vs-dissociated unsaid · partial N₂+H₂
dissociation figure-only) and drops the grade to analog; validation refuses w ∉ [0, 1), w > 0 without ice,
w > 0 without a potential temperature. The P3 ③ gate row's static half now asserts the wrap exists with
default 0 (instead of "no nh3 in the source"); its dynamic half (positive control 1, zero fires on the frozen
standalone integrations) is unchanged and is what says the default path is inert.

## 5. Step 2-② — the cold-flank label on the ammonia table's refusals (pre-registration, before code)

Owner: *"일단 2부터 보자."* (`4b8e06ba`, 2026-09-03) — the refusal label (②) before the deep-mantle rule (①).

**Diagnosis, reproduced from the table by the work seat.** `ammonia_table.density` raises one `ValueError`
for both `p < p_lo(T)` and `p > p_hi(T)`; `Ammonia.check_temperature` already labels `too_cold` correctly
for T outside 500–10 000 K, but `Ammonia.density` re-raises the table's error as `PhaseGap` with the default
`too_cold=False`. The table's bounds are **both monotone increasing in T** (measured, 11 isotherms: floor
0.309 → 7.70 GPa, ceiling 22.1 → 333.2 GPa from 500 to 10 000 K), so the direction is decidable:

    p > p_hi(T)  → hotter brings the state inside → too_cold = True
    p < p_lo(T)  → colder brings it inside          → too_cold = False

The dead case (152 GPa · 545 K, ceiling 22.1–64.6 GPa there) is the ceiling side, so it went out as
`False`, and `interior.py@«뚫는데, 그건 이 천체가 안 풀린다는 뜻이 아니라 **시험값이 낮았다** 는 뜻이다.»` (`t_now * 1.6 if gap.too_cold else t_now / 1.6`) pushed the trial **colder** —
steering exactly reversed. ⚠ A blanket `too_cold=True` would reverse the floor side instead.

**Design.** Decide the direction in `eos.Ammonia.density` (the consumer), using the public
`ammonia_table.p_bounds(t)`; `ammonia_table.py` is generated and is not touched. Freeze the monotonicity the
direction logic rests on as a gate row (it is a fact of this table, not a guarantee; a regenerated table could
break it silently). No other material's `too_cold` is touched; the default stays 0; no deep-mantle rule.

**Registered outcomes.**
- ① both directions exist and each carries the right flag (unit check on the two sides of the table at one
  isotherm) → the ceiling-side refusal steers the temperature **up**.
- ② the floor-side refusal never fires on the roster's paths → the direction logic stays, recorded as
  "unfired" (C5 forbids machinery without a consumer, not one branch of a two-way decision).
- ③ a temperature interval where either bound is not monotone → the premise is wrong: **stop and report**.
- ④ the opt-in Uranus solve at w = 0.1159 gets past 152 GPa → **the next wall's location is the product**;
  no expectation written (the last one was wrong).
- ⑤ anchors: at w = 0 ammonia is never called → byte-identical, `--refresh` **not** needed. If it becomes
  needed, stop and trace. (`Ammonia.density` is not a path-fingerprint function; `interior.py` is untouched.)
- ⑥ gate FAIL 0, cost stated.

**Checklist line, added after gate66's one FAIL (`check_contracts` caught the code–document divergence 21
minutes after the commit):** a new declaration, output or node goes into the methodology doc's Needs line and
domain table (en + ko) **in the same commit** as the code — a pre-registration item, not a follow-up. This
step adds no declaration or output (a flag on an existing refusal), so the line is carried, not exercised.

## 6. Run record — step 2-②, 2026-09-03

**Branches fired: ① · ⑤ exactly; ② as registered ("unfired" is wrong — the floor side *did* fire, once,
and it is the product); ③ did not fire; ④ answered.**

- **①** `eos.Ammonia.density` now decides the flag from `ammonia_table.p_bounds(t)`: `too_cold = p > p_hi(T)`.
  Unit row in `test_ammonia.py`: at 3000 K, 2 × ceiling → `too_cold=True`, ½ × floor → `False`. Both directions
  exist and carry the right flag. **③ did not fire**: the monotonicity of both bounds over all 11 isotherms is
  now a gate row (floor 0.309 → 7.70, ceiling 22.1 → 333.2 GPa).
- **⑤** `--fast` passes untouched; `Ammonia.density` is not a path-fingerprint function and `interior.py` is
  unchanged. No `--refresh`.
- **④ — the next wall, and it is the *floor*, not the ceiling.** Opt-in Uranus solve at w = 0.1159, traced
  twice with identical output (4.3 s / 4.4 s; `density` 9 959 calls, `c_p` 1 990, `grad_ad` 1 990; seven
  refusals):

  | # | P (GPa) | T (K) | table floor–ceiling at T (GPa) | side | `too_cold` → steer |
  |---|---|---|---|---|---|
  | 1–3 | 164 · 162 · 158 | 131 · 210 · 338 | below 500 K (isotherm range) | temperature | True → hotter |
  | 4–5 | 152 · 143 | 545 · 883 | 0.36–22.4 · 0.67–65.6 | **ceiling** | True → hotter |
  | 6 | **1 035** | 3 935 | 3.07–268.3 | **ceiling** (the registered deep-mantle wall) | True → hotter |
  | 7 | **4.10** | **4 749** | **4.123**–276.8 | **floor**, by 0.023 GPa | False → colder — bracket flips, the loop concludes |

  Reading, in order: the fixed flag now steers the cold trials **up** (refusals 1–5, the state that killed
  step 1's run is passed in 0 s), the corridor reaches the deep mantle and meets the registered ceiling at
  1 035 GPa (refusal 6, steer hotter again), and the hotter adiabat then puts the **mantle top** — the first
  ice state above the ocean table's 2.3 GPa, where `with_ices` engages — at 4.10 GPa · 4 749 K, **below the
  table's low-density floor** at that temperature (4.123 GPa; the floor rises with T, 0.309 GPa at 500 K to
  4.45 GPa at 5 000 K). That refusal says "colder", the previous said "hotter": **the corridor is pinched
  between two walls that pull opposite ways**, and the temperature loop concludes by name instead of cycling
  (Brief 22's rule held). *"Refused by name at the ceiling"* was the expectation written for step 1; the
  truth is **two walls**: the deep ceiling (a deep-mantle rule, owner) **and the shallow floor** (the
  low-density edge of the table at a hot mantle top — a *shallow* rule, or a hotter-than-the-floor entry
  condition on `with_ices`, neither declared here). **No single temperature satisfies both at w = 0.1159 on
  Uranus's column.** That is the shape the owner's deep-mantle decision has to take: it is not one rule.
- **Instrument error, caught by running twice** (the rule from Brief 34's null result): a first inline trace
  reported *"131 K … ValueError, 1 fire"* — its own `except` block called `p_bounds(131 K)`, which raises
  outside the isotherm range, replacing the `PhaseGap` it was logging. Guarded in the kept script
  (`scratchpad/c22_trace.py`); the two guarded runs above agree to the digit. Reported so the false first
  reading is not quoted.
  **How close the floor refusal is, in numbers** (directing seat's recomputation, reproduced here): at 4 749 K
  the table spans 4.124–276.8 GPa; the mantle top sits at 4.101 GPa — **0.024 GPa, 0.6 % below the floor**.
  Not a gross violation; a hair. The floor's climb with temperature, from the table:

      500 K 0.309 GPa · 1000 K 0.749 · 2000 K 1.320 · 3000 K 1.906 · 4000 K 3.150 · 5000 K 4.450

  So the owner's decision is **two decisions**, and *"far outside"* and *"0.6 % outside"* are different ones:
  ① above the ceiling (deep mantle; fired at 1 035 GPa · 3 935 K) · ② below the floor (mantle top; fired at
  4.10 GPa · 4 749 K, by 0.6 %). Neither is declared; refusing by name is the correct state until then.
- **⑥ Gate on `7393528f`: FAIL 0, 459 PASS (+2, the two new `test_ammonia` rows), 20:44:47 → 21:24:28 =
  2 381 s.** The two rows cost ≈ 0 s (a handful of table lookups). **Attributed, by asking the machine**
  (directing seat, reproduced by the work seat at 21:3x): `pmset -g` → `powermode 1` — **low-power mode was
  still on**; `pmset -g therm` → *"No thermal warning level has been recorded"*, *"No performance warning
  level has been recorded"* — **thermal throttling is excluded by evidence, not withdrawn as a guess**; the
  machine was on battery (25 %, discharging). So 1 585 s and 2 381 s are **both low-power mode** — the
  owner's *"아마 절전모드"* was right, and the mode stayed on, which is why the second run was slower.
  **Trend, in two branches that must not be mixed**: on mains power 1 224 → 1 268 → 1 280 → 1 293 s, each
  step with a cause (one new row + noise); in low-power mode 1 585 → 2 381 s, **not comparable to code
  cost**. This project's gate is ~21 minutes, not 40. Before launching a gate: `pmset -g batt` — on battery,
  ask the owner first (a dying machine mid-gate leaves the orphan-process situation of this morning).

## 7. The extrapolation axis above the table — closed on the literature, 2026-09-03

Owner-obtained: **Li, Wang, Chen & Song 2013** (`2013JChPh.139m4505L`, cached as the arXiv preprint PDF +
LaTeX source, ISO-8859/CRLF — read via `iconv -f latin1`). Result, reproduced by the work seat from the source:
**the deep-mantle refusal above ≈ 333 GPa has no published route around it, and does not need one.**

1. **No published ammonia fit joins a high-pressure asymptote.** The parallel seat's ADS query
   `abs:"ammonia" abs:("Thomas-Fermi" OR "degenerate electron")` → numFound 3, all unrelated. The construction
   `eos.py` uses for silicate (Seager's BME4 → TFD) and iron (Vinet → TFD) has **no ammonia candidate** — zero.
2. **The one paper whose range fits (Li+ 2013) is a Hugoniot, and cannot be used as numbers.** Its source has
   **one table** (Table I, *"Points along the principal ammonia Hugoniot"*); the other eight captions are
   figures; nothing after `\end{document}`. *"Wide-range equation of state"* appears in the abstract only —
   no coefficients, no grid. Table I, transcribed:

   | ρ (g/cm³) | P (GPa) | T (K) |
   |---|---|---|
   | 1.9 | 77.09 | 4 791 |
   | 2.0 | 95.94 | 6 036 — our mantle's top temperature (6 070 K) is here |
   | 2.2 | 221.44 | 19 180 |
   | 2.4 | 567.67 | 54 229 |
   | 2.6 | 1 273.65 | 112 663 |

   Where we need it — 333 to 1 035 GPa — this path is at **19 000–113 000 K against a mantle at
   2 550–6 070 K**. Not "a different path shape": at high pressure the Hugoniot **does not pass near our
   region at all**; at 6 036 K it is at 95.9 GPa, already inside our table, and from where the table ends it
   is an order of magnitude hotter. Its *"at about 4800 K, the system transforms into a metallic, complex
   mixture state consisting of NH₃, N₂, H₂, N and H"* is **a transition along the Hugoniot, not along an
   isentrope** — the distinction is kept.
3. **Extending the 2013 table upward would assert two things.** Four transitions are already reported in
   90–350 GPa that 2013's four-phase picture does not contain — ionic crystal (Pickard & Needs' prediction at
   ~90 GPa; Ninet+ 2014 `2014PhRvB..89q4103N` experiment ~180 GPa), self-ionisation to ammonium amide
   (Palasyuk+ 2014 `2014NatCo...5.3460P`, ~120 GPa), molecular liquid → plasma (Ravasio+ 2021
   `2021PhRvL.126b5003R`, from ~90 GPa, reaching ~350 GPa) — identifiers from the parallel seat's ADS lookup,
   **none of the three held** (0 cache hits). And Ravasio+ write *"the experimentally accessed region of the
   ammonia phase diagram today is still very limited"*: **above 350 GPa there is no experiment.**

**The data we want already exist and are not distributed.** Bethkenhagen+ 2017 §2.4 (reproduced from the
cached `.md`): *"We extended the ammonia EOS data set from Bethkenhagen et al. (2013), which ranged up to
10 000 K and 330 GPa, to higher pressures and temperatures … the density grid was extended by seven additional
densities per isotherm in order to cover the pressure range up to 1000 GPa. Additionally, four more isotherms
(12 000 K, 14 000 K, 16 000 K, and 20 000 K) were computed."* ⚠ **It cannot be appended to our table**: the same
paragraph says *"the correction due to nuclear quantum effects was removed from the published data set"*,
and our baked 2013 Table I **includes** that correction — a separate data set; joining them puts a
discontinuity at the seam. The only route is an author request, which is the class the owner closed on
09-03 (*"둘 다 지금은 안 한다"*): **recorded as a possible route, not opened.** Aside, worth carrying: 2017
interpolates its own tables with Akima splines and warns of *"oscillatory behavior when calculating small
differences, especially when the underlying data grid is coarse and/or the data possess residual statistical
fluctuations"* — the authors describing, for their data, the problem our interpolation-error work measured.

**C22 as of tonight**: step 1 landed (dial at 0, anchors unmoved); step 2-② landed (cold-flank label);
**step 2-① waits on the owner — two decisions, ceiling and floor**; default stays 0.
