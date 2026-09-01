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
