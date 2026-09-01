# Wire tidal heating into interior structure — context notes (Brief 35)

## 1. Extraction from Kankanamge & Moore 2019 (read in full, 2026-09-01)

Source: `docs/phase3/_papers/2019JGRE..124..114K.pdf`
([`2019JGRE..124..114K`](https://ui.adsabs.harvard.edu/abs/2019JGRE..124..114K),
doi 10.1029/2018JE005800). All equation labels below checked at their place in the text.

The solved object is a **nonlinear 2-equation system in (T_i, δ)** — internal temperature
and lid (lithosphere) thickness — their eqs. (36) and (38), §4. Auxiliaries:

- Kankanamge & Moore eq. 1 — η(T) = η₀·exp(−A(T−T₀)), Frank-Kamenetskii linearised viscosity.
- eq. 3 — ΔT_rh = A⁻¹, rheological temperature scale (Davaille & Jaupart 1994).
- eq. 5 — Ra_rh = ρ g α ΔT_rh (D−δ)³ / (κ η(T_i)), sub-lid Rayleigh number.
- eq. 9 — δ_rh = (a_rh/a_c)(D−δ)·Ra_rh^(−1/3), rheological sublayer thickness.
- eq. 10 — T_sol(d) = T_sol0 + (dT_sol/dz)·d, two-parameter linear solidus.
- eq. 13/fitted in eq. 21 — v_m = a_u·(κ/(D−δ))·Ra_rh^(1/2), upwelling velocity, a_u = 0.63
  (their own fit, Figure 3).
- eq. 21 — v = C_p·v_m·ΔT_m / L, melt volume flux = lid burial velocity, where
  ΔT_m = T_i − T_sol0 − (dT_sol/dz)(δ+δ_rh) (drop across the melt zone; Figure 2 geometry:
  the average temperature FOLLOWS THE SOLIDUS through the melt zone, so T_i is the solidus
  at the melt zone's bottom, eq. 16–17. Note eq. 4 (T_l = T_i − a_rh·ΔT_rh) is the
  *non-melting* Figure-1 relation and is superseded by eq. 17 when a melt zone exists).
- eq. 20 — F_m = ρ v [L + C_p((T_i + T_sol0 + (dT_sol/dz)(δ+δ_rh) − 2·T_s)/2)],
  volcanic heat flux (latent + sensible at melt-zone midpoint temperature, eqs. 18–19).
- eq. 36 — k·a_rh·ΔT_rh/δ_rh − kH/(ρC_p v) − [HD − F_m − kH/(ρC_p v)]·exp(ρC_p v δ/k) = 0
  (lid-base flux condition; lid conducts *and* is buried at velocity v, eq. 24–29).
- eq. 38 — H·δ/(ρC_p v) + (1/(ρC_p v))[HD − F_m − kH/(ρC_p v)][exp(ρC_p v δ/k) − 1]
  + T_s − T_sol0 − (dT_sol/dz)(δ+δ_rh) + a_rh·ΔT_rh = 0 (lid-base temperature condition,
  eq. 17 eliminated through eq. 37).
- Table 1 — a_rh = 2.4 (Solomatov 1995; Solomatov & Moresi 2000), a_c = 1.7 (Solomatov &
  Moresi 2000).
- Energy closure: F_s = F_c + F_m = H·D (eqs. 22–23, 28); κ = k/(ρC_p).

**Io parameters (Table 5, transcribed)**: g = 1.8 m/s², D = 1000 km, T_s = 100 K,
T_sol0 = 1395 K (Hirschmann 2000), dT_sol/dz = 0.362 K/km (Hirschmann 2000, slope at
2 GPa), ρ = 3000 kg/m³, C_p = 1000 J/(kg·K), L = 5×10⁵ J/kg, H = 3×10⁻⁶ W/m³,
k = 4 W/(m·K), η₀ = 10¹⁷ Pa·s, A = 15 (see gap ② below), T₀ = 1400 K.

**Printed Io result (§6)**: T_i = 1471 K, δ = 12.6 km, F_m = 2.5 W/m², F_c = 9 mW/m².
⚠ Known trap (directing seat, carried): never transcribe §6's "totaling ∼1 TW".
Also noted here: the printed §6 fluxes are not internally consistent with eq. 28
(F_m + F_c = 2.509 W/m² but H·D = 3.0 W/m²); the equations force F_m + F_c = HD
exactly, so at least one printed flux is loose. Recorded before running.

## 2. Two gaps found in Table 5, before running

① **α (thermal expansivity) is absent from Table 5** yet required by eq. 5. §6 says
"Material parameter values are typical mantle rock values from Schubert et al. (2001)".
**Filled in: α = 3×10⁻⁵ K⁻¹** (Schubert, Turcotte & Olson 2001, canonical mantle value).
This is a filled-in number and is labelled as such wherever it appears.

② **A = 15 carries no printed unit.** In eq. 1, A is dimensional (K⁻¹); in the §5
simulations A = 15 is dimensionless. A = 15 K⁻¹ literal gives ΔT_rh = 0.067 K
(unphysical); the simulation scale D²H/k = 7.5×10⁵ K gives ΔT_rh = 5×10⁴ K
(unphysical). **Pre-registered resolution procedure**: solve the system over a grid of
dimensional A; if the printed (1471 K, 12.6 km) is reproduced inside the §3 tolerance at
some A, check whether that A corresponds to a natural reading (e.g. A = E/(R·T₀²) with
Karato & Wu 1993 creep energies: E = 240 kJ/mol wet olivine → A = 0.0147 K⁻¹,
ΔT_rh ≈ 68 K; E = 300 kJ/mol dry → A = 0.0184 K⁻¹). Decision rule, registered BEFORE
running: exactly one natural reading reproduces → adopt it, labelled
*unit-resolved-by-reproduction*; none → outcome branch 4 (the paper does not print
enough); the diagnosis names A, not the transport declaration — the declaration is not
touched (branch-3 discipline).

## 3. Pre-registered Io tolerance (BEFORE first run — this commit precedes the solver)

From the paper's own stated precision, two tiers, both registered now:

- **Target (print precision)**: T_i = 1471 ± 0.5 K, δ = 12.6 ± 0.05 km — what exact
  arithmetic reproduction of their own solve would give if their printed inputs are
  exactly the inputs they used.
- **Acceptance (the paper's own stated model precision, §5 + abstract)**: internal
  temperature relative error "less than 1.4%" (their §5 statement of the
  parameterization's T_i misfit) → **|ΔT_i| ≤ 21 K**; lid thickness inside the
  abstract's "<15% relative error" bound (their Tables 2–4 lid column reaches 12.6%)
  → **|Δδ| ≤ 1.9 km**.
- Landing inside acceptance but outside target is reported as such (expected causes:
  the α fill-in, input print-rounding — H is printed to one significant figure — and
  the §6 flux inconsistency noted in §1).
- Solver convergence tolerance must sit ≪ both tiers (residuals driven to machine-level;
  verified in the test).

Outcome branches are the brief's five, unchanged.

## 4. Verdict (2026-09-01, after the runs) — branches ③+④ fired

**Io does not reproduce under any natural reading of the unprinted constants; the
product is the name of the wrong assumption, and it is not on our side of the wiring.**

What was established, in order:

1. **Transcription verified verbatim.** Every equation (1)–(38) was checked against the
   PDF text layer (FlateDecode extraction), not only the rendered pages. The solver
   drives the printed system's residuals to ~1e-14 and preserves the built-in closure
   F_m + F_c = H·D to machine precision.
2. **A numerically necessary reformulation, algebraically identical.** The printed
   eq. (36)/(38) contain c₁·exp(+ρC_p v δ/k); away from the root this is a huge
   exponential times a near-cancelling bracket, and sign-scanning it produces hundreds
   of spurious "roots" with astronomical residuals. Eliminating c₁ analytically leaves
   only exp(−Pe) terms; at the root the two forms agree to the bit.
3. **Natural readings miss, decisively.** With Table 5 verbatim, α = 3×10⁻⁵ (Schubert
   fill-in, the paper's own pointer) and A over the full physical range (ΔT_rh 10–500 K,
   including the Karato & Wu wet/dry readings 0.0147/0.0184 K⁻¹), and H at both the
   printed 3×10⁻⁶ and the flux-implied 2.509×10⁻⁶ W/m³: the unique root sits at
   **T_i ≈ 1447–1594 K, δ ≈ 97–534 km** — the lithosphere misses the printed 12.6 km by
   **8–42×** at every candidate; T_i misses the ±21 K acceptance at the natural A's.
   (Robust half worth recording: F_c = 7.4–8.0 mW/m² across the entire grid, matching
   the printed "9 mW/m²" in kind — the burial-limited conduction physics is stable;
   the (T_i, δ) placement is what fails.)
4. **Exact-root recovery pins the diagnosis.** Solving (A, α) so that the printed
   (1471 K, 12.6 km) is an exact root of the printed system (H = 2.509×10⁻⁶ from the
   printed fluxes' own closure) converges to **α = 8.71×10⁻⁷ K⁻¹ (≈ 1/34 of mantle
   rock) and ΔT_rh = 354 K (rock rheological scales are ~40–100 K)** — residuals 1e-14,
   and the all-roots solver lands on (1471.00 K, 12.599 km) at exactly those constants.
   No physically admissible fill-in exists: the printed §6 result is not a root of the
   printed §4 system under the paper's own cited material values.
5. **Independent of Io, the paper's own nondim Tables 2–4 fail deterministic
   inversion.** Using only printed Model columns and printed equations: the latent heat
   L recovered per row (one constant in the model) drifts 0.3 → 10.8 across rows, and
   the v recovered from the flux equation (36) disagrees with the v recovered from the
   temperature equation (37) by up to 4×, systematically in dT_sol/dz. Neither
   exponent-sign convention fixes it. So the non-reproducibility is a property of the
   paper's printed system, not of our Io setup.

**Branch ③ product — the wrong assumption, named**: that Kankanamge & Moore 2019's
printed §4 equations + Table 5 constitute the closed system that produced their §6 Io
numbers. They do not: α is absent, A's unit is unprinted, H is printed at one
significant figure against its own flux printout, and the actual solved system appears
to differ from print in some undocumented way (their §7 notes "we did refit a_u" —
the class of quiet refits that would explain the table inversion failure).
**Branch ④ unblock**: the paper's stated data link (http://cas.hamptonu.edu/data-products,
"Simulation results and data extraction scripts are available at") or the authors —
per standing rule, ask the owner before any fetch outside the ADS/_papers channel.
Not tuned: the transport-mode declaration was never touched (branch-③ discipline).

**What shipped anyway (wired, labelled, unvalidated)**: `engine/tidal_transport.py` —
Ė/(4πR²) → labelled (internal temperature, lithosphere thickness) under a **declared**
transport mode, with the derived-vs-declared provenance on every number, the
Rovira-Navarro+ 2021 stability label (stable under Andrade; conditionally-stable with
the runaway-cooling caveat under Maxwell+convection), and a permanent
`validation: failed-io-reproduction` tag so a reader cannot mistake these numbers for
validated ones. `derive_potential_temperature()` exists but its output carries the same
tag — the declaration-to-derivation upgrade is wired and **blocked from adoption by its
own label**. Io enters the gate as a check table (`test_tidal_transport.py`, registered
in check.sh): it pins the transcription closure, the measured miss (as invariants — if
Io ever lands inside tolerance the test fires loudly, because the story changed), the
exact-root recovery, and the label discipline.

## 5. Roster measurement (measured, NOT adopted — hard line kept)

Io-class material fill-ins (Table 5), per-body g and T_s, D/R = 0.549 declared:

- **Dante (A b I)** — *interim, superseded 2026-09-01 (see §6): the inputs below were
  a mismatched pair.* R 521 km was fed the **rejected 900-km draft's flux** 11,500 W/m²
  (and a ρ=3000 g), so the measured "no root" was an input artifact, not physics.
- **Hades (A b II)** — R 750 km, M 5.0e21, board flux 207 W/m² (band bottom), T_s
  278 K: unique root **T_i = 1844 K, lithosphere = 224 km** (on D = 412 km — more than
  half the declared mantle depth, where the 1-D slab is least trustworthy; §6 of the
  paper itself says spherical correction would reduce both). Unvalidated, unadopted;
  the Dante/Hades radius question stays parked with the owner.

Anchors: no engine module imports `tidal_transport`; anchors expected bit-identical
(gate run confirms).


## 6. Corrections after the owner's question (2026-09-01, same day)

**① The Dante measurement used a mismatched pair, and the verdict flips.** §5's input
(R 521 km + F 11,500 W/m²) paired the adopted radius with the rejected 900-km draft's
flux — methodology §6.5 is the canonical table (directing seat confirmed
(900/521)³ = 5.15 and 2,231 × 5.15 = 11,500 exactly; F ∝ R³ at fixed density). Re-run
with the matched pair (521 km · 1.552×10²¹ kg · ρ 2,620 · 2,231 W/m² · plains 223 K ·
g 0.3816): **the printed system has a unique root — T_i = 2122 K, lithosphere 147 km**
(F_m = 2231, F_c = 29 mW/m²). So Dante is *not* an absence; the "no root at Dante"
line in §5 is superseded. Still measured-not-adopted, still unvalidated-labelled.
(T_s sensitivity: the board-era 360 K moves it to 2125 K / 136 km — small.)

**② Hades inputs cross-checked and kept.** Canonical = phase4/alpha_centauri.yaml,
which is self-consistent for Hades (no radius redesign): moons block M 5.0×10²¹ kg ·
R 750 km (density M/V = 2,830 kg/m³, inside the rocky band, matching the board's
"Moon-sized rocky body"); bulk.tidal_heating 207 W/m² whose "~15× Io" multiple implies
an Io output of 9.76×10¹³ W (inside the ~10¹⁴ W Veeder order) — flux and radius are a
pair. surface_temperature 278 K. §5's Hades numbers stand: (1844 K, 224 km).

**③ Hand-typed inputs removed.** The same defect fired twice in one day (this
session's Dante pair; the audit's g·T_s omission), so `roster_inputs()` now reads the
values from the canonical files with their sources attached and refuses mismatched
pairs by name before running: Dante's F∝R³ check against the drafted row and
M = ρ(4/3)πR³; Hades's rocky-band density and the ×Io-multiple ↔ flux·area
consistency. Canonical choices recorded in the module: **Dante = methodology §6.5
table** (the phase4 board is internally split while the radius question is parked:
decisions row says 521 km, moons block still carries the 900 km draft, and
bulk.tidal_heating still carries 11,500 W/m²); **Hades = the phase4 board**. The board
stays read-only. The gate now pins the corrected measurements as invariants
(test_tidal_transport.py §5–6).

**④ Both roster roots sit where the model is least trustworthy.** Hades:
lithosphere/mantle-depth = 224/412 = **54 %**; Dante: 147/286 = **51 %**. The
parameterization's convection scalings (eq. 5's Ra with (D−δ)³, eq. 13's velocity) are
stagnant-lid laws for a thin lid over a deep convecting layer; at δ/D > ½ the "layer"
is thinner than its lid, the melt zone occupies most of what remains, and the paper's
own §5 validation never went there — their nondimensional lid thickness tops out at
δ/D = 0.26 (Tables 2–4), and §6 says even Io's spherical correction (ignored in the
1-D slab) would lower both outputs. The unvalidated label already applies; this notes
*which regime* the numbers sit in, so a reader does not mistake them for interpolation
inside the validated range.
