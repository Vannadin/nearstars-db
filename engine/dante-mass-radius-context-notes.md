# Dante mass → radius through our own compaction solver — context notes

Owner request (2026-09-02, via directing seat), **measurement only, zero adoption**.
The board's Dante mass–radius pair is marked INVENTED on both sides
(phase4/alpha_centauri.yaml:1469,1472) and was built by *assuming* a constant density
of 2,620 kg/m³ across the whole design family. The engine's reason to exist is deriving
radius from mass, so the open question (memory: "압밀 모형이 INVENTED 질량-반지름 쌍을
의심") is whether our tool supports that invented pair — and whether the solver's
density stays at 2,620 across the mass family or drifts with mass.

## 1. Pre-registration (committed BEFORE the first run)

**Inputs, read from sources (no hand-typing; the Brief-35-③ rule).** The mass family
and its invented radii come from the stability sim's combo files and the board:

| mass (kg) | invented R | source file |
|---|---|---|
| 1.5519×10²¹ | 521 km | phase3/stability-sim/hypotheticals/_dante521_combo.json |
| 2.0×10²¹ | 567 km | …/_dante2e+21_combo.json |
| 4.0×10²¹ | 714 km | …/_dante4e+21_combo.json |
| 8.0×10²¹ | 900 km | phase4/alpha_centauri.yaml moons block (rejected draft, still resident) |

The run script reads these files; the board stays read-only.

**Declaration ① — composition.** `composition="silicate"` (interior.py COMPOSITIONS):
iron core mass fraction **0 — no core declared**. The invented pair carries no core
information, so declaring zero is itself an output of this measurement; the C10
(lighter-rock/serpentinisation) and C7 (partial differentiation) axes stay at their
defaults (0 / fully differentiated). Mantle material = the engine silicate stack
(eos.py: mgsio3_en BME3 ρ₀ 3220 kg/m³ → mgsio3_prem BM2 3980 → mgsio3_pv BME4 4100,
refs at their definitions). `ice_mass_fraction 0` (board identity: silicate volcanic,
the moon ROSTER already declares ice excluded for Dante). `tidal_heating=True`
(declaration; porosity-regime indicator only). `initial_porosity 0` (declared).
Sensitivity row: `earth_like` (cmf 0.325) at the adopted mass only, both thermal cases,
to show the iron-core lever.

**Declaration ② — thermal state, two cases per mass.**
(a) `potential_temperature=None` — the solver's isothermal legacy path;
label **declared (cold/nominal)**.
(b) `potential_temperature=2122 K` — Brief 35's transport-axis output for the matched
Dante pair; label **derived-from-Ė, UNVALIDATED** (the axis failed its Io validation;
the label rides along).

**Tolerance for branch ① (declared before running):** our radius within **±2 %** of
the invented radius. Basis: the solver's forward-radius anchor (Earth) reproduces to
0.30 % in the gate; the family radii are printed to 3 significant figures; ±2 % is a
generous ceiling over both. Density-drift verdict: the four solver densities
ρ̄ = M/(4/3·πR³) within ±2 % of each other → "stays"; a monotonic rise beyond that →
"drifts with mass, the heavy end of the invented family is the most wrong" (and the
heavy end, 8×10²¹, is what still sits in the board's moons block).

**Pre-registered outcomes, five (as issued):**
① ours within tolerance → the invented pair is supported by the tool.
② ours larger → the assumed 2,620 is too high for that mass (less compaction).
③ ours smaller → self-compression (or the mineral's own zero-pressure density)
   exceeds the assumption.
④ refusal → legitimate ending; name what is missing (mass outside the rocky path's
   validated window, or an insufficient composition declaration).
⑤ outside the register → name it; record the kind afterwards.

Hard lines: measurement only; the board read-only; no tidal-gate or stability-sim
reruns; every result carries the unvalidated/measurement label with both declarations'
sources. Anchors expected bit-identical (no engine code changes planned; gate skippable
if none happen).

## 2. Results (2026-09-02, measurement only — nothing adopted)

**Branch ③ fired, uniformly.** Bare declared silicate (no core), both thermal cases:

| mass (kg) | invented R | ours, cold | ours, 2122 K | Δ vs invented | ρ̄ ours (cold) |
|---|---|---|---|---|---|
| 1.5519×10²¹ | 521 km | 486.2 km | 486.4 km | **−6.7 % / −6.6 %** | 3,224 |
| 2.0×10²¹ | 567 km | 529.1 km | 529.3 km | −6.7 / −6.7 | 3,224 |
| 4.0×10²¹ | 714 km | 666.4 km | 666.9 km | −6.7 / −6.6 | 3,227 |
| 8.0×10²¹ | 900 km | 839.3 km | 840.2 km | −6.7 / −6.6 | 3,230 |

- **Density drift: neither registered sub-branch.** The solver's density is flat at
  3,224→3,230 across the 5.15× mass family (self-compression contributes +0.2 %), and
  none of the four sits near 2,620. Named as its own kind: **the invented family's
  constant-density scaling law is supported by the tool at these masses; the constant
  is what is wrong** (the engine's silicate floor is enstatite ρ₀ = 3,220, not 2,620).
  Every member is offset by the same −6.7 %; no end of the family is "most wrong", the
  resident 8×10²¹ draft included. Equivalently R_ours = R_inv·(2620/3224)^{1/3} to the
  printed digit.
- **The thermal declaration does not move this answer.** 2122 K (derived-from-Ė,
  UNVALIDATED) inflates the radius by ≤ 0.9 km (≤ 0.11 %) over the cold declaration —
  at these masses the solver's thermal pressure is negligible, so the tool does *not*
  need the thermal state to state this body's radius at the ±2 % tolerance. Both cases
  labelled as pre-registered.
- **An iron core moves it the wrong way.** Sensitivity earth_like (cmf 0.325) at the
  adopted mass: 455.7 km (−12.5 %). Declaring any core makes the mismatch worse, so
  "no core declared" is the family-favourable reading and it still misses.

**Reconciliation axes, measured and labelled (NOT adopted):**
- `serpentinisation = 1.0` (C10 axis, antigorite ρ₀ ≈ 2,600, Hilairet+ 2006 room-T
  fit): **519.4 km, −0.3 % — inside the ±2 % tolerance.** The only measured axis that
  reproduces the invented pair. But it is incoherent with the board's own identity: a
  fully hydrated, water-saturated alteration rock as the bulk of an Io-type volcanic,
  strongly tidally heated moon. Measured as a fact about the family's implicit density,
  not as a composition proposal.
- `initial_porosity = 0.187` (the void fraction 1 − 2620/3224): 506.7 km (−2.8 %,
  partial compaction under pressure) **and the engine's own regime judgment rejects
  it** — `voids_expected = False` with tidal heating declared.

**Verdict line for the owner (measurement, unvalidated where labelled):** our
compaction solver does not support the INVENTED pair as bare silicate at any mass in
the family — it wants **~486 km at the adopted 1.552×10²¹ kg** (ρ̄ ≈ 3,224). The
family is internally consistent (constant density is a fine approximation here) but
sits on a density no dry silicate in our stack provides; the measured routes to
2,620-class density (full serpentinisation, or ~19 % surviving porosity) each
contradict either the board identity or the engine's own porosity regime.

Anchors: no engine code touched; measurement calls only. Gate not re-run (docs-only
commits since the passing 1221 s run; nothing in scope changes a converged answer).
