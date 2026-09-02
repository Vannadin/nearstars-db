# 고체 맨틀 점성 법칙과 맥스웰 완화시간 — 정유체 도형 가정을 판정하는 relaxation verdict (Brief 39)
"""Solid-mantle viscosity laws and the Maxwell relaxation verdict.

    verdict = relaxation_verdict(t_top_k=1600.0, t_cmb_k=2526.0, p_top_pa=0.0,
                                 p_cmb_pa=135.3e9, age_gyr=4.54)

What this answers, and only this: **could this body's degree-2 figure have relaxed to
hydrostatic within its age?** The figure solver (`scripts/refs/body_figure.py`, not touched)
assumes hydrostatic J2 = 10/3·C22 for synchronous bodies as a blanket declaration
(body-figure-methodology.md §3, fossil-bulge caveat). This module supplies the value that
declaration was missing, upstream of the `fossil_bulge` wire in chain.yaml. It does **not**
predict a fossil figure — that needs a history (earlier spin or orbit), which this engine
declares out of scope. The refusing branch refuses by name.

Design, argued in engine/figure-relaxation-context-notes.md §2 and repeated where it bites:

* **Maxwell is a floor.** τ_M = η/μ. Rovira-Navarro+ 2021, the paper that supplies μ, says the
  Maxwell model "does not properly capture the complex behavior of olivine observed in
  laboratory experiments" and omits anelastic transient creep. This is an order-of-magnitude
  gate and every output says so.
* **Every solid-viscosity constant below is RELAYED.** Karato & Wu 1993 (1993Sci...260..771K)
  is the source Monteux's 256 / 25.17, Rovira-Navarro's 300 kJ/mol and the Kankanamge thesis
  creep law all cite; none reproduces it and it was not obtainable (owner, 2026-09-03; Science,
  no open-access route). μ = 65 GPa is Rovira-Navarro's table value from Segatz+ 1988, also not
  held. **They are usable here for one reason, measured not assumed: the criterion is
  insensitive to them over the full admissible range.** Two decades of solidus-viscosity anchor
  (1e15–1e17 Pa·s) and the whole Mars-mantle activation-energy range (300–540 kJ/mol, Nimmo &
  Stevenson 2000 via Rovira-Navarro) move the 4.5 Gyr threshold temperature by ~300 K
  (689–986 K), while τ_M spans more than twenty decades across mantle temperatures. Age matters
  less still (0.1 → 10 Gyr moves it ~70 K). The spread is carried as an output, not hidden in a
  point value: a body whose temperature falls *inside* the spread gets `cannot-say`, because a
  check whose own error exceeds its criterion cannot decide.
* **Adopted as a declared family with a grid**, never one elected quadruple (C11): the verdict
  compares against every (E_a, η_s) threshold, not a chosen one.
"""
from __future__ import annotations

import math

import eos

R_GAS = 8.314                      # J/(mol·K)
GYR_S = 1e9 * 365.25 * 86400.0     # seconds per Gyr

# ── Rovira-Navarro+ 2021 (2021PSJ.....2..119R) eq. 5, parameter table ──────────────
# η = η_s · exp[(E_a / (R T_s)) · (T_s/T − 1)], T_s = solidus temperature.
# "Mantle solidus viscosity" 1·10¹⁶ Pa·s and "Activation energy" 300 kJ/mol, footnote 4 =
# Karato & Wu (1993) — RELAYED, see module docstring. E_a's admissible range 300–540 kJ/mol is
# the paper's own sentence (lines 413–421 of the extraction): "the activation pressure at
# Mars' mantle varies between 300 KJ mol⁻¹ close to the surface to 540 KJ mol⁻¹ in the
# mid-mantle (Nimmo & Stevenson 2000)" — Mars, second-hand, and the paper's own word is
# "activation pressure" for a quantity printed in kJ/mol.
RN_ETA_S_PA_S = 1.0e16
RN_E_A_J_MOL = 300.0e3
RN_E_A_RANGE_J_MOL = (300.0e3, 540.0e3)
RN_ETA_S_RANGE_PA_S = (1.0e15, 1.0e16, 1.0e17)     # two decades around the declared anchor
# "Mantle shear modulus" 65 GPa, footnote 5 = Segatz et al. (1988), NOT HELD — relayed.
MU_PA = 65.0e9
MU_SOURCE = "Rovira-Navarro+ 2021 table, 'Mantle shear modulus' 65 GPa, from Segatz+ 1988 (not held; relayed)"

# ── Monteux+ 2016 (2016E&PSL.448..140M) eq. 8, after Abe 1997 ─────────────────────
# η = η_s,0 · exp(B · T_liq/T); line 342: "We used η_s,0 = 256 Pa s, and B = 25.17 based on
# the olivine rheology (Karato and Wu, 1993; Abe, 1997)." RELAYED. ⚠ Not robust: the exponent
# reaches ~45 at deep-mantle ratios, so a 1 % error in T_liq/T is a 45 % error in η. Used here
# as the SECOND law (pre-registered branch ③: do the two laws disagree on a verdict), not as
# the primary.
MONTEUX_ETA0_PA_S = 256.0
MONTEUX_B = 25.17

# Verdict labels. Strings, not numbers dressed as measurements.
RELAXES = "relaxes-within-age"
CANNOT_RELAX = "cannot-relax-within-age"
INSIDE_SPREAD = "cannot-say (inside criterion spread)"
NO_TEMPERATURE = "cannot-say (no temperature)"
NO_SILICATE = "not-applicable (no silicate mantle)"
NO_SOLIDUS = "cannot-say (solidus undefined at this pressure)"

CONDITION = ("Maxwell floor, order-of-magnitude gate; all viscosity constants relayed through "
             "unobtained Karato & Wu 1993; solver has no conductive lid, so 'relaxes' means the "
             "convecting mantle relaxes; age is the most permissive window, so 'relaxes' is "
             "necessary not sufficient and 'cannot' is a hard refusal")


def viscosity_rovira(t_k: float, t_s_k: float,
                     eta_s: float = RN_ETA_S_PA_S, e_a: float = RN_E_A_J_MOL) -> float:
    """Rovira-Navarro+ 2021 eq. 5 [Pa·s]. Relayed constants — see module docstring."""
    return eta_s * math.exp((e_a / (R_GAS * t_s_k)) * (t_s_k / t_k - 1.0))


def viscosity_monteux(t_k: float, t_liq_k: float) -> float:
    """Monteux+ 2016 eq. 8 [Pa·s]. Relayed constants; exponent ~45 deep — not robust."""
    return MONTEUX_ETA0_PA_S * math.exp(MONTEUX_B * t_liq_k / t_k)


def maxwell_time_s(eta_pa_s: float, mu_pa: float = MU_PA) -> float:
    """τ_M = η/μ [s]. A floor: transient creep would relax faster, never slower."""
    return eta_pa_s / mu_pa


def threshold_temperature_k(age_s: float, t_s_k: float,
                            eta_s: float = RN_ETA_S_PA_S, e_a: float = RN_E_A_J_MOL,
                            mu_pa: float = MU_PA) -> float:
    """Temperature at which τ_M(Rovira-Navarro) equals the comparison time. Closed form:
    η_s·exp[(E_a/RT_s)(T_s/T − 1)] = μ·age  ⇒  T_s/T = 1 + ln(μ·age/η_s)·R·T_s/E_a."""
    ratio = 1.0 + math.log(mu_pa * age_s / eta_s) * R_GAS * t_s_k / e_a
    return t_s_k / ratio


def threshold_spread_k(age_s: float, t_s_k: float) -> dict[tuple[float, float], float]:
    """The declared family: threshold over {E_a} × {η_s}. The verdict reads the whole grid."""
    return {(e_a, eta_s): threshold_temperature_k(age_s, t_s_k, eta_s, e_a)
            for e_a in RN_E_A_RANGE_J_MOL for eta_s in RN_ETA_S_RANGE_PA_S}


def _verdict_at(t_k: float, thresholds: dict) -> str:
    lo, hi = min(thresholds.values()), max(thresholds.values())
    if t_k > hi:
        return RELAXES
    if t_k < lo:
        return CANNOT_RELAX
    return INSIDE_SPREAD


def relaxation_verdict(t_top_k: float | None, t_cmb_k: float | None,
                       p_top_pa: float, p_cmb_pa: float | None, age_gyr: float | None,
                       silicate_state: str = "solid", variant: str = "peridotitic") -> dict:
    """Labelled verdict for one body. Returns a dict with `figure_relaxation` (label),
    `maxwell_time_mantle_top` [yr] (Rovira-Navarro at the top temperature, or None),
    `relaxation_threshold_max` [K] (worst-case threshold across the family), `second_law`
    (Monteux's verdict at the same point, for branch ③), and `notes` (tuple of str).

    The verdict is taken at the **coldest temperature the solver owns** — the top of the
    adiabat. If that relaxes, everything hotter below it does. The CMB verdict is computed as a
    consistency reading, never as the headline."""
    notes: list[str] = []
    out = {"figure_relaxation": None, "maxwell_time_mantle_top": None,
           "relaxation_threshold_max": None, "second_law": None, "notes": ()}

    if silicate_state in ("none", None):
        out["figure_relaxation"] = NO_SILICATE
        notes.append("figure relaxation: no silicate mantle in the solved column — the "
                     "viscosity laws here are olivine rheology and do not apply.")
        out["notes"] = tuple(notes)
        return out
    if not t_top_k or t_top_k <= 0.0 or age_gyr is None or age_gyr <= 0.0:
        out["figure_relaxation"] = NO_TEMPERATURE
        notes.append("figure relaxation: cannot say — the solver carries no temperature "
                     "(potential_temperature undeclared) or no age; refusing rather than "
                     "defaulting to hydrostatic.")
        out["notes"] = tuple(notes)
        return out

    t_s = eos.silicate_solidus(p_top_pa, variant)
    t_l = eos.silicate_liquidus(p_top_pa, variant)
    if t_s is None or t_l is None:
        out["figure_relaxation"] = NO_SOLIDUS
        notes.append(f"figure relaxation: cannot say — silicate solidus undefined at "
                     f"{p_top_pa / 1e9:.0f} GPa.")
        out["notes"] = tuple(notes)
        return out

    age_s = age_gyr * GYR_S
    spread = threshold_spread_k(age_s, t_s)
    lo, hi = min(spread.values()), max(spread.values())
    verdict = _verdict_at(t_top_k, spread)
    tau_top = maxwell_time_s(viscosity_rovira(t_top_k, t_s))
    # Second law (Monteux) at the same point: relaxes iff τ_M < age. Branch ③ instrument.
    tau_monteux = maxwell_time_s(viscosity_monteux(t_top_k, t_l))
    second = RELAXES if tau_monteux < age_s else CANNOT_RELAX

    out["figure_relaxation"] = verdict
    out["maxwell_time_mantle_top"] = tau_top / (365.25 * 86400.0)
    out["relaxation_threshold_max"] = hi
    out["second_law"] = second
    notes.append(
        f"figure relaxation ({verdict}): top-of-mantle {t_top_k:.0f} K against the "
        f"τ_M = age threshold family {lo:.0f}–{hi:.0f} K (E_a 300–540 kJ/mol × η_s 1e15–1e17 Pa·s, "
        f"μ 65 GPa, age {age_gyr:.2f} Gyr, T_sol {t_s:.0f} K at {p_top_pa / 1e9:.0f} GPa); "
        f"τ_M(Rovira-Navarro) = {tau_top:.2e} s = {tau_top / (365.25 * 86400.0):.2e} yr. "
        f"Monteux/Abe at the same point: {second} (τ_M {tau_monteux:.2e} s"
        + (", laws agree" if second == verdict or verdict == INSIDE_SPREAD
           else " — LAWS DISAGREE, branch ③") + "). " + CONDITION + ".")
    if t_cmb_k and t_cmb_k > 0.0 and p_cmb_pa is not None:
        t_s_cmb = eos.silicate_solidus(p_cmb_pa, variant)
        if t_s_cmb is not None:
            v_cmb = _verdict_at(t_cmb_k, threshold_spread_k(age_s, t_s_cmb))
            notes.append(f"figure relaxation at the CMB ({t_cmb_k:.0f} K, {p_cmb_pa / 1e9:.0f} GPa): "
                         f"{v_cmb} — consistency reading, not the headline.")
    out["notes"] = tuple(notes)
    return out
