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
