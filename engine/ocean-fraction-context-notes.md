<!-- C17 — ocean_fraction → dynamo_rocky 간선. payload 가 무엇인지, 이미 구조로 실려 있는지 측정한다. 사전등록 → 실행 기록 -->
# Ocean fraction and the rocky dynamo (C17) — context notes

2026-09-04. **§1–§2 are the pre-registration, committed before any measurement ran.** Directing seat's hypothesis,
relayed: the mechanism the methodology names for water-rich bodies *"passes straight through `cmb_heat_flux`"*,
so the edge may already be carried by structure. Recorded as a hypothesis; **no expectation is written**.

## 1. What the edge says, and what its supplier is

`chain.yaml:670`: `ocean_fraction → dynamo_rocky, kind: influences, sign: negative, status: gap, ref:
rocky-planet-dynamo-methodology.md:109`. The supplier `ocean_fraction` is a **layer-0 owner declaration** with
one output, `f_ocean`, itself `status: gap` — no body declares it, nothing computes it. The methodology's
sentence behind the edge (step 4 of the regime list): *"Water-rich rocky (ocean worlds): for the same mass and
core size, the CMB heat flux Q_c is lower (cooler, lower-pressure CMB) → weaker moment. Ganymede analog
(ℳ ≈ 2×10⁻³)."*

**Read before measuring — `f_ocean` means three different things to its three consumers**, and the dynamo
edge's meaning is the odd one out:
- `→ surface_albedo` (tidally-locked-temperature doc §"water-bearing tidally-locked planets"): the **surface
  water inventory** — a climate-state axis picked on the Phase 4 board.
- `→ cassini_state` (cassini doc item 4): a **subsurface ocean** that decouples the shell (Titan's non-rigid
  amplification, ×2–3 on ε) — a documented option, not a default.
- `→ dynamo_rocky` (the sentence above): **"water-rich rocky" as a bulk class** — the same mass and core
  with more water in the mantle column, i.e. the interior's **water mass fraction**, which the engine already
  carries as `ice_mass_fraction` and which the ladder already consumes (`dynamo_rocky.ladder(…,
  ice_mass_fraction)` selects regime 4, *water-rich*).

So the hypothesis sharpens: **the dynamo edge's payload is not `f_ocean` at all; it is `ice_mass_fraction`**,
which reaches `dynamo_rocky` by two routes that both exist — (i) the ladder's regime 4 (explicit), and (ii)
the interior: `ice_mass_fraction → interior_layers` (cmb_pressure, cmb_temperature, core_radius) →
`cmb_heat_flux` (Q_CMB) — the mechanism sentence itself. If (ii) moves Q_CMB when the water fraction moves,
the edge's stated mechanism is already delivered by structure, and what is wrong is the edge's *supplier*
label, not the coupling.

## 2. Measurement and registered outcomes

**Instrument.** `interior.solve` on one body at two water fractions with everything else fixed (1 M⊕, CMF 0.325,
T_pot 1600 K; `ice_mass_fraction` 0 → 0.1 and 0.3 as the water-rich end), reading `cmb_pressure`,
`cmb_temperature`, `core_radius`; then `cmb_flux.solve` on each with the same declared core-side T_c (Earth's
3760 K — a declaration held fixed so only the mantle side moves), reading `q_cmb` and `q_adiabat`; and the
ladder's regime on each. Positive control: the solve must actually change *something* (radius) when the water
fraction changes, else the instrument is dead.

- **①** `ice_mass_fraction` moves `cmb_pressure` / `cmb_temperature` / `core_radius` and hence `Q_CMB` in the
  direction the doc names (lower) → the mechanism is already carried by structure; the edge is re-labelled
  (supplier `ice_mass_fraction`, not `f_ocean`) and **C17 closes as *already wired, mislabelled***.
- **②** They move, but `Q_CMB` goes the *other* way or does not move → the doc's mechanism sentence is
  contradicted by our own interior; reported, not tuned; C17 stays open with that fact.
- **③** The solve refuses or fails to converge at the water-rich end → named, reported; the mechanism is
  untestable on this body class today.
- **④** Both routes exist but the ladder's regime 4 and the structural route disagree on direction → both
  emitted, the disagreement named.
- **⑤** `f_ocean` for the other two consumers is untouched — surface ocean coverage and a subsurface ocean are
  not the interior water fraction; those edges keep their own gap.
- **⑥** No code path changes; anchors untouched; docs-only closure or a one-line edge relabel in `chain.yaml`.
  Gate FAIL 0, time, `pmset`.

## 3. Run record — 2026-09-04

**Branch fired: ③ — the solve does not converge at the water-rich end, so the mechanism is untestable on this
body today. Route (i) is confirmed to exist. Nothing wired.**

    ice_mass_fraction  R (R⊕)   core_radius   P_cmb (GPa)   T_cmb (K)   P_c (GPa)   converged   cmb_flux at declared T_c 3760 K        ladder regime
    0.0                1.0030   0.5470        135.28        2526        358.5       True        Q_CMB 2.750 TW (δ_b 394 km)             1 (dry)
    0.1                1.1509   0.5478        131.78        4397        353.8       **False**   refused — T_c 3760 ≤ T̃_m 4397, no jump    4 (water-rich, ℳ_base 0.002)
    0.3                1.2934   0.5515        116.20        4372        333.1       **False**   refused — T_c 3760 ≤ T̃_m 4372, no jump    4 (water-rich, ℳ_base 0.002)

- **Positive control held**: the water fraction moves the solve (radius +15 % / +29 %, P_cmb −3 % / −14 %).
- **③, precisely**: at 0.1 and 0.3 the interior's temperature loop **does not converge** (`converged=False` —
  the surface temperature condition is missed; 48–52 s each), and *an end that misses its boundary condition
  is not an end* (this list's rule from C13's ice axis). The numbers in those two rows are therefore
  **unconverged trial states, not results**, and no direction is read from them as a finding.
- **What the unconverged trials show anyway, labelled as such**: the pressure half of the doc's mechanism
  (*"lower-pressure CMB"*) goes the stated way (135 → 132 → 116 GPa); the temperature half (*"cooler"*) goes
  **the opposite way on our column** — T̃_m at the CMB rises from 2 526 to ~4 400 K, because a water/ice
  layer above the rock lengthens the adiabatic column from the same 1 600 K potential temperature. With the
  core-side T_c held at Earth's declared 3 760 K that leaves **no superadiabatic jump**, and `cmb_flux`
  refuses by name — the instrument cannot even reach Q_CMB. Whether a water-rich body's CMB is cooler or
  hotter is therefore **not something this measurement decided**; it is what a converged water-rich solve
  with its *own* declared core-side temperature would have to say.
- **Route (i) exists and fires**: `dynamo_rocky.ladder(…, ice_mass_fraction)` selects regime 4 at both
  water fractions, ℳ_base 0.002 (the Ganymede analog) — the *class* half of the mechanism is already wired
  through the ladder, independent of the interior.
- **Ganymede anchor, observed not judged** (directing seat's rider): the methodology's validation table
  gives Ganymede *ℳ/ℳ⊕ (RM22 / obs)* = 2×10⁻³; RM22 Table 8 prints **0.003 (model)** and **0.002 (observed,
  its ref. (3))** for Ganymede — so the ladder's anchor is the *observed* value as relayed by RM22's
  citation (3), a secondary citation of an observation, not RM22's own computed 0.003. Both numbers are
  now written; which the ladder should carry is not decided here.

**Closure state**: C17 **stays open, with its reason named** — the edge's stated mechanism cannot be tested
on this class until a water-rich rocky body *converges* in `interior_layers` (C1 closed sub-Neptunes with a
gas envelope; a 0.1–0.3 water mantle on an Earth-mass rocky body without one has not been made to converge —
its own item, not C17's), and until such a body carries its own declared core-side temperature (Earth's
3 760 K is not a water world's). **Second reason (directing seat, 2026-09-04)**: the methodology's item 4 — the mechanism sentence this edge
rests on — carries **no citation**; item 3 beside it cites Gaidos 2010, item 4 nothing. And its temperature
direction (*"cooler"*) is the opposite of what our unconverged column shows. So C17 is open on two counts:
the mechanism is **untested** (C24 blocks) and **ungrounded** (no source). Both are now marked in the
methodology (en + ko), beside the Ganymede row, which likewise carries no citation of its own.
What C17 *did* settle: the edge's supplier is mislabelled — its payload is
`ice_mass_fraction`, not `f_ocean` — and half of it (the class → regime 4) already arrives. **Nothing wired
into `dynamo_rocky`; the moment step was not attempted** (it needs `locked`, C16).

## 4. After C24 closed (2026-09-04, later the same day) — the numbers above are superseded

The unconverged rows of §3 (ice 0.1 → T̃_m 4 397 K, ice 0.3 → 4 372 K) were the stuck-hot state of a loop blocked by
the water column's coverage gap (`water-world-convergence-context-notes.md`). With the gap bridged the column
converges: **ice 0.1 → R 1.1313 R⊕ · P_cmb 132.2 GPa · T_cmb 3 105 K; ice 0.3 → R 1.2585 · 117.7 GPa · 3 050 K**
(dry: 1.0030 · 135.3 · 2 526 K). The direction stands — a water-rich body's CMB is *hotter* than the dry one's,
not cooler as the methodology's item 4 says — but the size is now a converged one, and the "~4 400 K" in §3 and
in the methodology is superseded. **C17's structural half is measurable from here; opening it is a separate
start, not done in this file.**

**Observation, not a task (directing seat):** the same derived number had been copied into five places — this
file, the C17 row in `interior-core.md`, the rocky-dynamo methodology (en and ko) and the `chain.yaml` edge note.
One went stale, so five went stale, and when C17 actually starts the same five places will need the same edit
again. Item ① (the phase side tables) was built today so that a *value* has one home; the prose already had
five homes for this one. The same problem with another face; recorded for the day it is addressed.

*(2026-09-04, later: C17 was opened and measured — §5. The five copies each carry a dated addendum; the numbers above stand.)*

## 5. C17 opened (2026-09-04, owner) — pre-registration, written before any run

Reason it can be measured now: reason (1) of the closure — the water-rich column did not converge — was removed
by C24 the same day. Reason (2) — the methodology's item 4 has no citation and states the temperature direction
opposite to our column — is what this section measures. The converged points in hand before this section:
dry 2 526 K · ice 0.1 → 3 105 K · ice 0.3 → 3 050 K (T_cmb, mantle side, Earth mass, cmf 0.325, T_pot 1 600 K).

Order: ② first (is the −55 K a turnover or noise), then ③ (does the dynamo verdict move), then ① (what to do
with the document). ① is last because it is a *reading* of ② and ③, not a measurement of its own.

### ② The curve is not monotone — noise or turnover?  (measured first)
`0.0 → 2 526 · 0.1 → 3 105 (+579) · 0.3 → 3 050 (−55)`.
- **Noise floor, measured not assumed**: |T_cmb(0.301) − T_cmb(0.300)|, one perturbation of 0.001 in the water
  fraction. The solver's own bounds are T_TOL 1e-6 (temperature loop) and T_SURFACE_TOL 1e-3 on the surface
  temperature (≈ 1.6 K at 1 600 K); the perturbation is the empirical version, which also sees any layer-boundary
  step quantisation (the C13 staircase).
- **Curve points**: ice 0.05 · 0.15 · 0.20 · 0.25, added to the three in hand (7 points, ~50 s each).
- **②a** the interior maximum exceeds 3 × the measured noise floor → a real turnover; report where the maximum sits
  and the two competing lengths (the water column above the rock lengthens the adiabat; the lower P_cmb shortens
  the rock column) as the reading, not as a proven mechanism.
- **②b** the −55 K is within 3 × the noise floor → the curve is "rise, then saturate"; no turnover is claimed.
- **②c** the added points do not converge → the measurement stops there and says so (C24's window is not
  reopened for this; the refusal is the result).

### ③ Does the water fraction move the dynamo verdict?  (the C17 question)
Run the present-epoch chain the way `test_core_history.py` builds it — `interior.solve` → `cmb_flux.solve` →
`core_energy.solve` (C14, solves T_c) → `core_entropy.solve` (C15, ΔE band) — at ice 0.0 / 0.1 / 0.3, everything
else Earth's: cmf 0.325, T_pot 1 600 K, **the core-side CMB temperature 3 760 K stays Earth's declared value**
(labelled: an Earth declaration on a water world, not a water world's own; the dry/wet difference is then the
mantle-side temperature and the CMB pressure only).
Dry reference already on record: Q_CMB 2.750 TW at the declared T_c (δ_b 394 km); C14 T_c 3 978 K;
C15 ΔE −69 MW/K, band −264…+238, 4/8 corners positive → `cannot-say`.
- **③a** the C15 band changes its sign structure (all corners one sign) at 0.1 or 0.3 → the mechanism is real and
  its size is measured; the verdict string changes.
- **③b** Q_C, T_c and ΔE move but the band still straddles zero → the mechanism is real and measured, and *C15
  cannot use it*. **This is the expected outcome and it is not a failure of C17**: the band already straddles
  zero on the dry body. C17 closes as a named refusal — "measured; the consumer cannot resolve it".
- **③c** nothing moves (|ΔQ_C| < 0.01 TW and |ΔΔE| < 1 MW/K) → the mechanism does not reach the dynamo on this
  chain; the document's item stands on nothing.
- Thresholds are fixed here; whichever fires is reported with the three numbers per water fraction.

### ① The document: item 4 says "cooler, lower-pressure CMB → lower Q_c"
The item cites nothing, so the outcome is a correction of *our* sentence, not a rebuttal of anyone.
- **①a** the doc is wrong on the temperature half → rewrite item 4 (en + ko) from the measured curve: the pressure
  half as written, the temperature half reversed, and Q_C's direction as ③ measured it.
- **①b** we misread it → quote the sentence and state what it does say. (Ruled out or in by the text alone.)
- **①c** a different condition — the sentence could be about the core-side temperature of a body that formed
  with less accretional heat, or about a different mass. It fires only if a condition can be named from the
  text; the text names none, so ①c needs the owner's word, not ours.
- The five copies of the 3 105 / 3 050 pair (this file §4, the C17 row, the methodology en/ko, the chain note)
  get one dated addendum each; no number is edited in place.

### Scope (held)
No code change is expected; the three `f_ocean` meanings are already measured (§2) and are not re-measured;
C24's window and the anchors are untouched; `dynamo_rocky` is not wired.

### Run record — 2026-09-04 (after the pre-registration commit `d7570d96`)

**② — ②a on the converged points, ②c on three of the four added points.**

    ice     converged   R (R⊕)   r_c      P_cmb (GPa)   T_cmb (K)    time
    0.000   yes         1.0030   0.5470   135.28        2 526.21     2 s
    0.050   NO          1.0861   0.5472   134.21        3 033.28     15 s   (trial state, not read)
    0.100   yes         1.1313   0.5477   132.19        3 105.17     49 s
    0.150   NO          1.1683   0.5483   129.49        3 123.38     70 s   (trial state, not read)
    0.200   NO          1.1993   0.5491   126.23        3 085.77     94 s   (trial state, not read)
    0.250   yes         1.2293   0.5500   122.37        3 065.14     58 s
    0.300   yes         1.2585   0.5511   117.67        3 049.64     51 s
    0.301   yes         1.2591   0.5512   117.57        3 048.95     52 s   (noise-floor perturbation)

- **Noise floor 0.69 K** (0.300 → 0.301; ~0.3 K of it is the curve's own slope, so the floor is at most 0.7 K). 3 × floor = 2 K.
  The falls 3 105 → 3 065 (−40 K) and → 3 050 (−15 K) both exceed it: **the turnover is real** on the converged points.
- **Where the maximum sits is not bracketed**: 0.05, 0.15 and 0.20 return `converged=False` — the surface condition is
  missed (the trial column tops out at 0.2 GPa · 1 588 K against the 1 600 K target, a 0.75 % miss above
  `T_SURFACE_TOL` 1e-3, with the water fluid all the way up). So C24's fix made 0.1 and 0.3 converge but not the
  fractions between and below them. **A C24-adjacent coverage finding, recorded here and not repaired** (C24 is not
  reopened by this section; the anchors are untouched). The reading of the mechanism — the water column lengthens the
  adiabat, the lower CMB pressure shortens the rock column — is a reading, not shown.

**③ — ③b, as named in advance.** Everything Earth's except the water fraction; core-side 3 760 K is Earth's declaration.

    ice    T̃_m (K)   Q_C at declared T_c (TW)   C14 T_c solved (K)   Q_C solved (TW)   C15 ΔE (MW/K)   band            corners +   verdict
    0.0    2 526     2.750 (1.54–4.77)          3 978 (3 769–4 284)  4.91              −69             −264…+238       4/8         cannot-say
    0.1    3 105     3.110 (2.54–3.71)          3 890 (3 736–4 133)  4.91              −68             −268…+247       4/8         cannot-say
    0.3    3 050     3.199 (2.74–3.64)          3 887 (3 636–4 138)  4.93              −82             −294…+251       4/8         cannot-say

- **The boundary-layer flux rises with water, not falls**: the jump T_c − T̃_m shrinks (1 234 → 655 → 710 K) but the
  layer's mean temperature rises and eq. 39's viscosity falls faster than the jump shrinks — Q_C 2.75 → 3.11 → 3.20 TW.
  The document's "lower Q_c" is the opposite of this column.
- **C14's solved T_c falls ~90 K** and its Q_C stays ≈4.9 TW — as it must: C14's Q_C is the core-supply side under a
  *declared* cooling rate, so a hotter mantle side lowers the T_c that balances it rather than the flux.
- **C15 moves and still straddles zero**: ΔE −69 → −68 → −82 MW/K; 4 of 8 corners positive at every fraction; no inner
  core at any. **The mechanism is real and its size is measured; C15 cannot resolve it.** That is C15's limit (the dry
  band already straddles zero), not C17's failure.

**① — ①a.** Item 4 cites nothing, and both testable halves of its sentence go the other way on this engine: the
mantle-side CMB temperature rises, and Q_C rises. The correction is written into the item (en + ko) as a dated addendum,
with the pressure half left standing. ①c was not fired: the text names no condition, so none can be claimed for it.

**Closure.** C17 closes as **③b — measured; the consumer cannot use it.** Nothing wired into `dynamo_rocky`; the ladder's
regime-4 class path is unchanged; the Ganymede anchor is untouched. Five copies got one dated addendum each.
