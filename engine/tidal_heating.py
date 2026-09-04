# 조석 가열 — fixed-Q 식으로 Ė·표면 플럭스를 내고(§1), 표면 열수송 모드·결과 분류 라벨을 붙인다(§6.1·§6.2); C30
"""Tidal heating from the fixed-Q law (`tidal-heating-methodology.md`), plus the two label sets §6 attaches to it.

    Ė = (21/2) · (k₂/Q) · G M_p² R⁵ n e² / a⁶,   n = √(G M_p / a³)   (doc @«Ė  =  (21/2) · (k₂/Q) · (G M_p² R⁵ n e²) / a⁶»; m ≪ M_p)
    F = Ė / (4πR²)                                                 (doc @«`F = Ė / (4πR²)`, the number that decides volcanism/melting»)

Two recipes live here because both are the same document's outputs:
- `tidal_heating` — `power` [W], `surface_flux` [W/m²], `io_power_ratio` [—], `heat_transport_regime` (the §6.1 outcome
  table, doc @«### 6.1 The flux → regime table», strings verbatim; the 10⁻³–10⁻² decade has no row → "unclassified (between table rows)").
- `heat_transport_mode` — `mode` (the §6.2 table, doc @«### 6.2 How the heat actually leaves: the three-mode ladder»: plate tectonics · stagnant lid · heat pipe), judged on the
  **total** surface flux (tidal + radiogenic, the latter as l_int / 4πR² from `internal_heat_nontidal`).
  `resurfacing_rate` is declared in chain.yaml and NOT emitted — the document prints no formula for it.

Both tables are "guides, not sharp lines" (doc @«(these are guides, not sharp lines):») and "there is no published W/m² boundary between the modes"
(doc @«published W/m² boundary** between the modes»); the labels carry that. Not emitted in this version: `radius_ceiling` and `plains_temperature` (the §6.3–6.5
Dante axis — a separate item), and `tidal_transport.derive_potential_temperature` is not consulted (its own docstring
labels it validation-failed, and Pandora is not a §6 lid-bearing case, doc @«**Scope — lid-bearing bodies only.**»).

Inputs `eccentricity_forced` and `k2_over_q` are DECLARATIONS (the board fits k₂/Q, phase4/alpha_centauri.yaml@«The tidal term needs k₂/Q ≈ 0.0016 at the simulated e ≈ 0.005, which is fitted rather than predicted, but it»); the
result says so. Missing orbit or k₂/Q → cannot-say by name, never a default.
"""
from __future__ import annotations

import math

from payload import Result, out_of_domain

# Anchors for the sentences the values below stand on. They are cited here rather than inside the
# shipped strings, because a citation that reaches a reader should be short: the string says §6.2,
# this comment says which sentence, and check_refs resolves the comment.
#   the law            doc @«Ė  =  (21/2) · (k₂/Q) · (G M_p² R⁵ n e²) / a⁶»
#   the flux           doc @«`F = Ė / (4πR²)`, the number that decides volcanism/melting»
#   mean motion        doc @«with the mean motion `n = √(G(M_p + m)/a³) ≈ √(G M_p / a³)`»
#   §6.1 label table   doc @«### 6.1 The flux → regime table»
#   §6.2 mode table    doc @«### 6.2 How the heat actually leaves: the three-mode ladder»
#   §6.3 lid scope     doc @«**Scope — lid-bearing bodies only.**»
#   §6.5 size ceiling  doc @«### 6.5 The super-Io ceiling: what size a lava moon can be»
#   Io calibration     doc @«output at ~10¹⁴ W, i.e. a surface flux ~2 W/m²»
#   k₂/Q spread        doc @«`k₂/Q` is the **dominant uncertainty**»
#   R³ flux scaling    doc @«**surface flux scales as `R³` at fixed density**»
RECIPE = "tidal-heating-methodology"
VERSION = "1"
REFS = ("docs/reference/tidal-heating-methodology.md@«Ė  =  (21/2) · (k₂/Q) · (G M_p² R⁵ n e²) / a⁶»", ":99-100", ":264-269", ":295-299")

G = 6.67430e-11            # m³ kg⁻¹ s⁻², CODATA 2018
M_EARTH_KG = 5.9722e24     # IAU 2015 B3 nominal
R_EARTH_M = 6.371e6
# Io's tidal output as the document prints it: "~10¹⁴ W" (doc @«output at ~10¹⁴ W, i.e. a surface flux ~2 W/m²»). The Dante rows of §6.5 (doc @«### 6.5 The super-Io ceiling: what size a lava moon can be»)
# imply 1.016e14 W when inverted (2.44 W/m² at R 1822 km) — 1.6 % from this constant; that is a convention difference.
IO_POWER_W = 1.0e14
# Two Io flux anchors with different sources: ~2 W/m² = Veeder+ 2012 (2012Icar..219..701V, ABSENT from the cache);
# 2.5 W/m² = Kankanamge & Moore 2019 (2019JGRE..124..114K, HELD; doc @«| **Heat pipe** | melt migrates through the lid and erupts | ≥ ~2.5 W/m², no firm upper bound»,
# doc @«**Do not transcribe Kankanamge §6's "totaling ∼1 TW".**»). Neither is used in a verdict here.
IO_FLUX_VEEDER_W_M2 = 2.0
IO_FLUX_KM2019_W_M2 = 2.5

# §6.1 outcome table, doc @«### 6.1 The flux → regime table» — strings verbatim
REGIME_VIGOROUS = "vigorous silicate volcanism, possible magma ocean"
REGIME_ACTIVE = "active resurfacing, episodic volcanism"
REGIME_OCEAN = "enough to maintain a subsurface ocean under an ice shell"
REGIME_DEAD = "geologically dead; no ocean, no plumes from tides alone"
REGIME_UNCLASSIFIED = "unclassified (between table rows)"
# §6.2 transport-mode table, doc @«### 6.2 How the heat actually leaves: the three-mode ladder»
MODE_PLATE = "plate tectonics"
MODE_STAGNANT = "stagnant lid"
MODE_HEAT_PIPE = "heat pipe"
MODE_UNCLASSIFIED = "unclassified (between table rows)"
# The two sentences these labels rest on: doc @«(these are guides, not sharp lines):»
# and doc @«published W/m² boundary** between the modes». They are cited here, in a comment, and
# NOT inside the shipped string: a value's reader gets the pointer, not the document's prose.
GUIDES = "§6: guides, not sharp lines, and no published W/m² boundary between the modes"


def tidal_power(k2_over_q: float, perturber_kg: float, radius_m: float, a_m: float, e: float) -> tuple[float, float, float]:
    """(Ė [W], F [W/m²], n [rad/s]) — doc @«Ė  =  (21/2) · (k₂/Q) · (G M_p² R⁵ n e²) / a⁶», doc @«`F = Ė / (4πR²)`, the number that decides volcanism/melting»."""
    n = math.sqrt(G * perturber_kg / a_m ** 3)
    power = 10.5 * k2_over_q * G * perturber_kg ** 2 * radius_m ** 5 * n * e ** 2 / a_m ** 6
    return power, power / (4.0 * math.pi * radius_m ** 2), n


def outcome_regime(flux_w_m2: float) -> str:
    """§6.1 table, doc @«### 6.1 The flux → regime table». The decade 10⁻³–10⁻² has no row."""
    if flux_w_m2 >= 1.0:
        return REGIME_VIGOROUS
    if flux_w_m2 >= 0.1:
        return REGIME_ACTIVE
    if flux_w_m2 >= 0.01:
        return REGIME_OCEAN
    if flux_w_m2 <= 1e-3:
        return REGIME_DEAD
    return REGIME_UNCLASSIFIED


def transport_mode(total_flux_w_m2: float) -> str:
    """§6.2 table, doc @«### 6.2 How the heat actually leaves: the three-mode ladder», read on the total surface flux. Plate tectonics sits at ~0.09 W/m² (Earth 92.1 mW/m²);
    the stagnant-lid ceiling is 10–30 mW/m²; heat pipe from ≥ ~2.5 W/m². Between 0.14 (the plate row read at +50 %, the
    branch below) and 2.5 W/m² the table has no row."""
    if total_flux_w_m2 >= IO_FLUX_KM2019_W_M2:
        return MODE_HEAT_PIPE
    if total_flux_w_m2 <= 0.03:
        return MODE_STAGNANT
    if total_flux_w_m2 <= 0.09 * 1.5:          # the plate-tectonics anchor is one body, 92.1 mW/m²; read ±50 % as its row
        return MODE_PLATE
    return MODE_UNCLASSIFIED


def solve(mass_earth: float, radius_earth: float | None, semi_major_axis_km: float | None,
          perturber_mass_earth: float | None, eccentricity_forced: float | None, k2_over_q: float | None) -> Result:
    # km, not m: this is the key a body declares (`semi_major_axis_km`, e.g. bodies/pandora.yaml), and the contract is
    # only a signature if the name it prints is the name that works. The law wants metres, so convert at the call.
    semi_major_axis_m = semi_major_axis_km * 1e3 if semi_major_axis_km is not None else None
    inputs = {"mass_earth": mass_earth, "radius_earth": radius_earth, "semi_major_axis_km": semi_major_axis_km,
              "perturber_mass_earth": perturber_mass_earth, "eccentricity_forced": eccentricity_forced,
              "k2_over_q": k2_over_q}
    missing = [k for k, v in (("semi_major_axis", semi_major_axis_m), ("perturber_mass", perturber_mass_earth),
                              ("eccentricity_forced", eccentricity_forced)) if v is None]
    if missing:
        return out_of_domain(RECIPE, VERSION, f"cannot-say (no orbit): {', '.join(missing)} 미선언 — Ė ∝ M_p² e²/a⁶ (§1의 fixed-Q 식)",
                             inputs, REFS)
    if k2_over_q is None:
        return out_of_domain(RECIPE, VERSION, "cannot-say (no k2_over_q): 조석 소산 k₂/Q 미선언 — 클래스 밴드는 2–3 자리수 폭이라 "
                             "(§4의 k₂/Q 표) 값을 고르지 않는다", inputs, REFS)
    if radius_earth is None:
        return out_of_domain(RECIPE, VERSION, "cannot-say (no radius): Ė ∝ R⁵, F ∝ R³ (§1 · §6.5)", inputs, REFS)
    power, flux, n = tidal_power(k2_over_q, perturber_mass_earth * M_EARTH_KG, radius_earth * R_EARTH_M,
                                 semi_major_axis_m, eccentricity_forced)
    regime = outcome_regime(flux)
    notes = (
        f"fixed-Q law §1 with n = √(G M_p/a³) (m ≪ M_p): k₂/Q {k2_over_q} · e {eccentricity_forced} · "
        f"a {semi_major_axis_m / 1e3:,.0f} km · M_p {perturber_mass_earth:.4g} M⊕ · R {radius_earth:.4f} R⊕ → P_orb "
        f"{2 * math.pi / n / 3600:.3f} h. G CODATA 2018, M⊕ IAU 2015 nominal.",
        "e and k₂/Q are DECLARATIONS (grade declared): the board fits k₂/Q to its chosen flux (phase4/alpha_centauri.yaml@«The tidal term needs k₂/Q ≈ 0.0016 at the simulated e ≈ 0.005, which is fitted rather than predicted, but it» "
        "'fitted rather than predicted'); the class band for k₂/Q spans 2–3 decades (doc §5) and is not elected here.",
        f"io_power_ratio = Ė / {IO_POWER_W:.1e} W, the document's printed '~10¹⁴ W' (§2). The §6.5 Dante "
        "rows invert to 1.016e14 W (2.44 W/m² at R 1822 km), 1.6 % from this constant — a convention difference.",
        f"heat_transport_regime is the §6.1 outcome table read on the TIDAL flux alone; {GUIDES}.",
        "not emitted: radius_ceiling · plains_temperature (§6.3–6.5, the Dante lid axis — a separate item); "
        "tidal_transport.derive_potential_temperature is not consulted (validation failed by its own docstring; Pandora is not a "
        "§6 lid-bearing case, §6.3).",
    )
    return Result(recipe=RECIPE, version=VERSION, regime="fixed_q_synchronous",
                  reason=f"Ė {power:.3e} W · F {flux:.4g} W/m² ({power / IO_POWER_W:.3g}× Io's ~10¹⁴ W) → {regime}",
                  grade="analog",   # the law is the standard first-order form; e and k₂/Q are declarations
                  inputs=inputs,
                  values={"power": power, "surface_flux": flux, "io_power_ratio": power / IO_POWER_W,
                          "heat_transport_regime": regime, "orbital_period": 2 * math.pi / n / 3600},
                  units={"power": "W", "surface_flux": "W/m2", "io_power_ratio": "dimensionless",
                         "heat_transport_regime": "", "orbital_period": "h"},
                  refs=REFS, notes=notes)


def solve_mode(surface_flux: float | None, radiogenic_power: float | None, radius_earth: float | None) -> Result:
    inputs = {"surface_flux": surface_flux, "radiogenic_power": radiogenic_power, "radius_earth": radius_earth}
    refs = ("docs/reference/tidal-heating-methodology.md@«A body's surface has exactly three ways to pass internal heat, and they differ by **four orders of magnitude in capacity**.»",)
    if radius_earth is None:
        return out_of_domain(RECIPE, VERSION, "cannot-say (no radius): 총 표면 플럭스를 낼 반지름이 없다", inputs, refs)
    if surface_flux is None and radiogenic_power is None:
        return out_of_domain(RECIPE, VERSION, "cannot-say (no heat source): tidal_heating 도 internal_heat_nontidal 도 값을 내지 않았다",
                             inputs, refs)
    area = 4.0 * math.pi * (radius_earth * R_EARTH_M) ** 2
    radiogenic_flux = (radiogenic_power or 0.0) / area
    total = (surface_flux or 0.0) + radiogenic_flux
    mode = transport_mode(total)
    parts = []
    if surface_flux is not None:
        parts.append(f"tidal {surface_flux:.4g}")
    if radiogenic_power is not None:
        parts.append(f"radiogenic {radiogenic_flux:.4g}")
    else:
        parts.append("radiogenic absent")
    notes = (
        f"§6.2 table read on the TOTAL surface flux {total:.4g} W/m² = {' + '.join(parts)} W/m²; "
        f"chain :631 supplies W/m² and :632 supplies W — the W is divided by 4πR² here. {GUIDES}.",
        "resurfacing_rate (chain.yaml outputs) is not emitted: the document prints no formula for it.",
        "selectors not wired in this version: global_fluid_layer (chain :633, no recipe) and t_eq_stellar (:634) — "
        "§6.3 names Pandora a global-fluid-layer case, so its selector is the next item.",
    )
    return Result(recipe=RECIPE, version=VERSION, regime=f"mode_{mode.split()[0]}",
                  reason=f"total surface flux {total:.4g} W/m² → {mode}",
                  grade="analog", inputs=inputs,
                  values={"mode": mode, "total_surface_flux": total},
                  units={"mode": "", "total_surface_flux": "W/m2"}, refs=refs, notes=notes)


from registry import recipe  # noqa: E402


@recipe("tidal_heating")
def _from_state(state):
    return solve(mass_earth=state["mass_earth"],
                 radius_earth=state.get("radius_earth", state.get("radius")),
                 semi_major_axis_km=state.get("semi_major_axis_km"),
                 perturber_mass_earth=state.get("perturber_mass_earth"),
                 eccentricity_forced=state.get("eccentricity_forced"),
                 k2_over_q=state.get("k2_over_q"))


@recipe("heat_transport_mode")
def _mode_from_state(state):
    return solve_mode(surface_flux=state.get("surface_flux"),
                      radiogenic_power=state.get("radiogenic_power"),
                      radius_earth=state.get("radius_earth", state.get("radius")))
