# The liquid-water gap, closed with water2 — context notes

The band: liquid water above the ocean table's 2.3 GPa (or above its 500 K) and below the
hot-water fit's 1000 K floor. The melting curve called it liquid; the repository had no
equation of state there and threw `too_cold`, so the shooting loop pushed the central
temperature up and integrated the rest on Mazevet's fit. C3 recorded it as an open defect;
F2 paid for it (Callisto and Titan at f = 0.75, 70 CPU-minutes without finishing). The
answer was on the shelf `eos.py` itself named: SeaFreeze `water2`, Brown 2018.

## Provenance, with every number labelled

- **Brown, J. M. 2018**, *Local basis function representations of thermodynamic surfaces:
  H₂O at high pressure and temperature as an example*, Fluid Phase Equilibria 463, 18
  ([`2018FlPEq.463...18B`](https://ui.adsabs.harvard.edu/abs/2018FlPEq.463...18B), doi
  [10.1016/j.fluid.2018.02.001](https://doi.org/10.1016/j.fluid.2018.02.001)). Paywalled,
  no preprint; **its fit-and-residual discussion has not been read here.** Title checked
  against the bibcode on ADS.
- The representation is distributed as SeaFreeze v1.1.0's `water2` (Journaux+ 2020,
  [`2020JGRE..12506176J`](https://ui.adsabs.harvard.edu/abs/2020JGRE..12506176J)); the
  spline file `splines/water_Brown/water_Brown.mat` (MATLAB v7.3, read with h5py) has knots
  **0–100 000 MPa × 240–10 000 K** (176 × 156).
- The readable third-party statement of the range: **AQUA**, Haldemann, Alibert, Mordasini
  & Benz 2020, A&A 643, A105
  ([`2020A&A...643A.105H`](https://ui.adsabs.harvard.edu/abs/2020A&A...643A.105H), arXiv
  [2009.10098](https://arxiv.org/abs/2009.10098), open access; fetched into
  `docs/phase3/_papers/2009.10098.pdf` and read), **§2.3.5 "Region 5 (liquid and
  supercritical Fluid)"**: *"Since pressures above 1 GPa are outside of the validity region
  of the IAPWS-R6-95, we use the EoS by Brown (2018) for region 5. Through the usage of local
  basis functions to fit a Gibbs energy potential, Brown (2018) provide an EoS which is
  appropriate for liquid and supercritical H₂O from 1 GPa to 100 GPa and up to 10⁴ K."*
  Verified at that place in the text.

## What was found about the library — the ceiling is the spline's, not the knots'

Evaluating SeaFreeze's `water2` on a log-P × T grid, the spline returns **negative
densities and c_P of order 10⁶ J/kg/K well inside its 100 GPa knot box**. Measured
2026-08-30 on the venv's SeaFreeze v1.1.0, per isotherm, the last pressure before the first
unphysical cell (criteria: ρ finite and rising with P, 1000 < c_P < 15 000 J/kg/K, dT/dP|_S
positive, no runaway in successive density increments; then two cells of margin):

| T (K) | 240 | 280 | 320 | 360 | 400 | 500 | 600 | 700 | 800 | 900 | 1000 | 1100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| valid to (GPa) | 0.7 | 1.1 | 1.8 | 2.3 | 3.0 | 5.5 | 10.0 | 13.2 | 15.8 | 22.9 | 30.2 | 36.3 |

Set beside this recipe's melting curve (IAPWS to 20.6 GPa, Reinhardt above): T_m(2.3 GPa)
= 362 K, T_m(5) = 511 K, T_m(10) = 614 K, T_m(15) = 663 K, T_m(20) = 705 K. **The valid
ceiling hugs the liquid side of the melting curve**: the spline was evidently fitted to the
liquid and extrapolates into nonsense on the solid side of the curve. AQUA's own use is
consistent with this — its region 5 ↔ 7 transition to Mazevet is bounded at
log₁₀ P₅to₇ = log₁₀(42 GPa) + log₁₀(6) (T/1000 K − 2)/18 for 1800–4500 K (their eq. (26)),
i.e. AQUA leaves Brown before ~40 GPa — but AQUA quotes the knot range as the validity
range, and the spline in this library does not honour it below ~1000 K. This is a finding
about the library, recorded here so the next reader does not bake the knot box.

**What this leaves uncovered**, by name: (a) between the melting curve and the valid
ceiling at **12–20.6 GPa** — T_m is 640–705 K there and the ceiling reaches those pressures
only at ~700–870 K — a band ≲ 100–170 K wide that is still refused as `too_cold` (hotter
resolves it: water2's ceiling rises, and Mazevet takes over at 1000 K); (b) hot low-pressure
water **below 0.1 GPa** at > 500 K (steam-like; not baked); (c) above 1000 K nothing
changed — Mazevet+ 2019 carries it as before, and the h2o_hot code path was not touched.

## What was baked

`engine/water2_table.py`, by `tools/make_water2_table.py` (dev venv only; no runtime
dependency; `check.sh` on system Python): ρ, dT/dP|_S = αT/(ρc_P), and **c_P** (so a
rock-bearing mixture can weight ∇_ad in this band, which the ocean table could not) on a
log₁₀ P grid 0.1 GPa upward at step 0.02 dex, × 360–1100 K at 10 K, **ragged** — each
isotherm kept only to its valid ceiling (`KEEP`). Bilinear in (log P, T).

- Why 360 K and not 240 K: the table is asked for only above 2.3 GPa (where T_m = 362 K) or
  above 500 K; the colder part belongs to `water1`, and the spline is unphysical there
  anyway (above 0.6–2 GPa at 240–330 K).
- Why 1100 K: 100 K past the Mazevet floor, so the seam is measured from inside.
- Interpolation error, generator-measured against the spline at off-grid points: **band
  2.3–10 GPa × 500–1000 K: ρ 1.8×10⁻⁵, dT/dP 2.0×10⁻⁴, c_P 2.7×10⁻⁵; whole window: ρ
  2.5×10⁻⁴, dT/dP 8.9×10⁻⁴** (relative, worst; the window's worst is the 0.1 GPa · ~990 K
  corner).

`eos.DenseLiquidWater` (`h2o_liquid_dense`) in the `LiquidWater` shape plus `c_p` and
`grad_ad`; refusals name Brown 2018 / water2 and the ceiling at the given temperature, with
`too_cold=True` above the ceiling (hotter helps) and a pressure-wall refusal below 0.1 GPa.
`interior.integrate.liquid_material` now dispatches: water1's box → water1 (unchanged);
T ≥ 1000 K → Mazevet (unchanged, one line not touched); else water2 if in domain; else the
named refusal. `_ice_verdict` names which fluid representation the column used.

## The two seams, measured

**water1 ↔ water2** (both SeaFreeze), inside their overlap:

| region | ρ | dT/dP\|_S | c_P | where |
|---|---|---|---|---|
| baked overlap 0.1–2.3 GPa × 360–500 K (splines, generator) | **0.13 %** | **9.0 %** | 3.9 % | ρ worst at ~2.1 GPa · 460 K |
| same, from the two baked tables (`test_water2.py`) | 0.12 % | 8.3 % | — | 2.09 GPa · 460 K / 360 K |
| ocean region 252–360 K (splines) | up to 712 % | — | — | water2 unphysical above 0.6–2.0 GPa there; within 1 % of water1 only up to 0.63 GPa at 240 K, 2.0 GPa at 330 K, 2.24 GPa from 340 K |

So the two representations agree in density to ~0.1 % where both are physical, and differ
by up to 9 % in the adiabatic slope — α/(ρ c_P) is where the local-basis fits of the two
papers part. The ocean stays on water1 (its job), so nothing this recipe computes today
crosses that slope disagreement; a warm ocean top at 360–500 K would.

**water2 ↔ Mazevet+ 2019 at 1000 K** (the fit's floor for ρ ≳ 1 g/cc, §3.1), Mazevet
relative to water2: −2.47 % at 2.3 GPa, −2.61 % at 3.45, −2.83 % at 5.2, −3.06 % at 7.8,
−3.21 % at 11.6, −3.26 % at 17.5, **−3.32 % at 26.2 GPa** (the ceiling at 1000 K is 30 GPa).
A body whose column crosses 1000 K in a liquid state therefore sees a **~3 % density step
downward** at the switch — the same kind of seam as IAPWS ↔ Reinhardt's +26 % in melting
temperature, smaller, and now stated. It is not smoothed: the two are different physics
(a Gibbs local-basis fit; an analytic free-energy fit to TFMD), and interpolating them
would be AQUA's Method 2, whose price AQUA states.

## AQUA — on the shelf, not in the engine

AQUA stitches seven regions from 0.1 Pa to 400 TPa and writes its seam methodology out:
*Method 1* switches at the Gibbs-energy crossing (a phase transition), *Method 2*
interpolates the first and second derivatives independently across a transition band —
*"with the draw back that the thermodynamic consistency will not be guaranteed, i.e., the
thermodynamic variables will show deviations from Eq. (3) – (18)"* — and *Method 3* connects
two EoS that agree in an overlap. Its Table 2 assigns 5 ↔ 3 (Brown ↔ French & Redmer) to
Method 1 and 5 ↔ 7 (Brown ↔ Mazevet) to Method 2. That is a candidate for the day this
recipe's own ladder runs out of range, with an auditable seam method; today's need was one
band, and its answer was the region AQUA itself delegates to Brown. Recorded, not baked.

## Anchors — what moved, and why

- **Uranus and Neptune: bit-identical** (`test_ice_giant.py`, full solves: radius, C/MR²,
  central temperature and pressure to the last bit). Their converged columns are on
  Mazevet's fit above 1000 K, which this item did not touch; their *trial* paths do enter
  the band (the temperature bracket walked Neptune through 0.098 GPa · 817 K), and there the
  refusal keeps the pre-existing direction — `too_cold`, so the bracket raises the centre
  exactly as before. The first attempt threw the sub-0.1 GPa case as a pressure wall and
  Neptune was refused in one second; that was the wrong direction and was corrected before
  landing. `ice_giant_anchor.json` was re-frozen for the **fingerprint only** (the dispatch
  lives inside `integrate`, a path function); values identical.
- **Rock and giant anchors (Earth, Mars, Mercury, Moon; Jupiter, Saturn): untouched** — no
  water column.
- **Europa's three-layer inversion in the gate: unchanged** — band C/MR² 0.2979–0.3655,
  narrowed to core 0.071 · ice 0.078, ocean 105 km / shell 26 km, the same print as before
  this item. One observation outside the gate: on the wider default core grid, the cmf 0.45
  member now solves where its ice-rich trial path used to be thrown out of the band, so
  that exploratory band's low end reads 0.2774 and the narrowed point 0.070 · 0.078 — a
  member reached, not an anchor moved.
- **Ganymede** (two-layer, isothermal-path check) — no temperature, no band: unchanged.

## F2's open thread — closed

Callisto and Titan at serpentinisation f = 0.75, 270 K (`infer_three_layer`), the runs F2
could not finish in 70 CPU-minutes: **54 s and 58 s**, band tops 0.3265 and 0.3276 — the
values F2 had traced for the finished points, now reached directly. C11's road is clear.
