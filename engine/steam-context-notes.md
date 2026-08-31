# IAPWS steam for the wedge — context notes

Brief 25, 2026-08-31. Pre-registration in `steam-checklist.md` (criteria fixed before the
sweep). Target: the wall Brief 23 named — fluid water at p ≲ 0.1 GPa × 500–1000 K.

## §1 The source and the transcription

**IAPWS R7-97(2012)**, cached as `docs/phase3/_papers/IAPWS-IF97-Rev.pdf` (49 pp; the
iapws.org relguide URL now serves HTML, so the canonical PDF came from the Internet
Archive's capture of the same path — title checked). The text layer drops every power of
ten in the coefficient tables, so **all tables were transcribed from the typeset page
images**, the exact failure mode that would otherwise fabricate magnitudes silently.

Transcribed into `engine/steam_if97.py` (plain Python, closed-form Gibbs — no fitting, no
baked table, no runtime dependency): region 1 (eq. 7, Table 2's 34 coefficients), region 2
(eqs. 15–17, Tables 10–11: 9 + 43 coefficients), the B23 boundary (eq. 5, Table 1), the
saturation line (eq. 30, Table 34), and the property relations (Tables 3–4, 12–14).
∇_ad is derived from the same Gibbs derivatives (the module docstring carries the two-line
derivation: ∇_ad = −π(γ_π − τγ_πτ)/(τ²γ_ττ)).

**Verification, the standard's own**: R7-97 prints computer-program verification values to
9 significant digits (Tables 5, 15, 35 and the B23 point). `steam_if97.verify()`
recomputes all of them; **worst relative error 2.9 × 10⁻⁹** — print-precision exact. The
gate now runs this check every time.

**What is deliberately not transcribed, with coordinates**: region 3 (623.15–863.15 K
between the B23 line and 100 MPa — a Helmholtz-in-density form needing iteration;
B23 runs 20.0 MPa at 650 K → 30.5 at 700 → 46.0 at 750 → 66.7 at 800 → 100 at 863.15)
and region 5 (above 1073.15 K). Both refuse by name through the dispatch.

## §2 Sweep and seams (criteria pre-registered in the checklist)

**Physicality sweep** over 500–1070 K × 0.1–100 MPa (log grid, regions 1·2 only):
**0 violations** — ρ finite, positive, monotone in P on every isotherm; c_P ∈
[1981, 14040] J/kg/K (the top sits near the critical region, inside the registered
15 000 bound); 0 < ∇_ad < 1 throughout.

**Seams, measured not asserted**:
- steam(r1) ↔ water1 at 100 MPa (300–500 K): ρ worst **0.005 %**, c_P worst 0.21 % — the
  same physical water through two independent representations.
- steam ↔ water2 at 0.1 GPa (500–1000 K where both stand): ρ ≤ 0.02 %, c_P ≤ 0.12 %.
- steam ↔ **Mazevet at 1000 K, low P: +88 % (100 MPa) → +994 % (20 MPa)** — not a defect
  of either source but the measurement of Mazevet's own validity statement (ρ ≳ 1 g/cc):
  the hot-water fit must never serve low-density steam. The envelope dispatch therefore
  asks IF97 **before** the T ≥ 1000 K Mazevet branch.

## §3 Wiring, and the acceptance

`_Steam` (a Material-shaped adapter over `steam_if97`) slots into `_EnvelopeWater`'s
liquid dispatch ahead of water1/Mazevet/water2; solid and in-column paths untouched. The
path fingerprint did not move and the anchors are bit-identical (`--fast` PASS, no
refresh needed — the edits sit outside the fingerprinted corridor).

**Mixing-gap label, carried as required**: filling the wedge's water EOS does **not**
validate the additive-volume mixing there — the band is outside Soubiran & Militzer's
2–70 GPa × 1000–6000 K; any crossing rides on unvalidated extrapolation, and the solve's
envelope-water note says so (grade stays analog with that named reason).

*(acceptance — the four end-B solves — recorded below when they land)*
