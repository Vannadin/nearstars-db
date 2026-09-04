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
