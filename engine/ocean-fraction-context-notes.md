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
