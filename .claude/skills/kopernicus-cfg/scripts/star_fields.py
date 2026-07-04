#!/usr/bin/env python3
# Teff/L/분광형 -> Kopernicus 항성 ScaledVersion(Light/Material/Coronas) 필드를 생성하는 순수 모듈. 항성 기본색은 근거화된 stellar_photospheric_color 엔진에서만 도출
"""Star-rendering field synthesis for the Kopernicus emitter.

Pure functions (no DB, no file I/O, no body-name logic) that turn curated
stellar parameters into Kopernicus `ScaledVersion` field text.

**Single source of truth for star color.** The star's base photospheric hex is
NOT computed here — it is taken from the grounded engine
`scripts/refs/stellar_photospheric_color.py` (backed by
`docs/reference/stellar-photospheric-color-methodology.md`), which owns the ONLY
blackbody->color / SED->color path in the codebase. This module calls it via
`base_tint_hex(teff, spectype)` and applies the doc's §6 three-regime rule:

    FGK / white dwarf / hot (A/B/O)  -> blackbody_hex(Teff)   (§6.1)
    M dwarf                          -> mdwarf_tint(Teff)     (§6.2, Pickles SED)
    L/T/Y brown dwarf                -> blackbody_hex(Teff)   (§6.3 special case:
                                        deep dim red at ~1000-1300 K; the M-dwarf
                                        Pickles ladder does not extend here)

Everything else this module emits (rim / sunspot / corona / the several Light
colors) is a **rendering derivation** of that one grounded base hex — a scalar
brightness/tint transform, never a second independent color computation. The
rim/sunspot *sharpness* and the luminosity/curve math stay parametric.

Convention constants are anchored on RSS-Reborn/Sol-Configs' Sun cfg (a
FACT/convention, not copied text — Sol-Configs stays link-only per project
policy):
  * `luminosity` is flux in W/m^2 at `sunAU`; Sol = 1360. So a star's value is
    `1360 * L_star/L_sun`.
  * `sunAU` is kept at Sol-Configs' reference constant 13599840256 (NOT the real
    AU) — even Sol-Configs leaves it at the stock value at real scale.
  * `insolation = 0.15`, `radiationFactor = 1` (Sol defaults).

Intensity curves are PARAMETRIC (generated here, scaled by sqrt(L)); curve
fidelity is an acknowledged future refinement — `luminosity` is the dominant
brightness knob, the curves are distance falloffs.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

# The grounded color engine — the ONLY blackbody/SED -> color path in the repo.
# scripts/refs lives at <repo>/scripts/refs; this module is 5 levels down under
# .claude/skills/kopernicus-cfg/scripts/, so repo root is parents[4].
_ENGINE_DIR = Path(__file__).resolve().parents[4] / "scripts" / "refs"
sys.path.insert(0, str(_ENGINE_DIR))
from stellar_photospheric_color import (  # noqa: E402
    blackbody_hex,
    mdwarf_tint,
    hex_to_rgb_int,
)

# ── physical / convention constants ──────────────────────────────────
SOLAR_TEFF = 5772.0
SOL_LUMINOSITY_WM2 = 1360.0          # Sol-Configs Sun `luminosity` (W/m^2 @ sunAU)
SUN_AU_REF = 13599840256             # Sol-Configs `sunAU` reference constant (m)
INSOLATION = 0.15                    # Sol default
RADIATION_FACTOR = 1                 # Sol default
LIGHT_REACH_SOL_M = 1.49597871e13    # Sol IntensityCurve outer cutoff (~100 AU) at L=1


# ── base photospheric color: grounded engine only ────────────────────

def _spectral_class(spectype: str | None) -> str:
    """Leading spectral class letter.

    Returns 'D' for a white dwarf (any D-prefixed type: DA/DB/DQ/DZ/…), else the
    first OBAFGKM(LTY) letter, else '?'. The 'd' luminosity prefix (dM4.5 = dwarf
    M) is skipped so it does not shadow the real class. White dwarfs are their own
    regime token so §6.1 blackbody treatment is explicit, not incidental."""
    if not spectype:
        return "?"
    s = spectype.strip()
    # White dwarf: uppercase 'D' as the FIRST letter (not the 'd' dwarf prefix).
    if s[:1] == "D":
        return "D"
    for ch in s:
        u = ch.upper()
        if u in "OBAFGKMLTY":
            return u
        if ch.isdigit():
            break
    return "?"


def base_tint_hex(teff: float, spectype: str | None) -> str:
    """Grounded base photospheric hex per methodology §6 three regimes.

    This is the SINGLE color decision; every other color below is derived from
    it. Regime is picked by spectral class first, then Teff as the fallback
    when the class letter is unknown.
    """
    cls = _spectral_class(spectype)
    if cls == "M":
        # §6.2 — molecular-band-corrected pale warm orange (Pickles real SED).
        return mdwarf_tint(teff)
    if cls in ("L", "T", "Y"):
        # §6.3 — L/T/Y brown dwarfs: below the Pickles M-ladder floor. Blackbody
        # at ~1000-1300 K is a deep dim red, which is the intended tint.
        return blackbody_hex(teff)
    if cls in ("O", "B", "A", "F", "G", "K", "D"):
        # §6.1 — smooth-continuum photosphere (FGK/hot) OR a white dwarf ('D'):
        # a pure-H/He atmosphere with no metals/molecules, so blackbody at Teff
        # is an excellent approximation and there is no metallicity term.
        return blackbody_hex(teff)
    # Unknown class: fall back on Teff. M-dwarf temperature band -> M regime.
    if teff < 4000.0:
        return mdwarf_tint(teff) if teff >= 2700.0 else blackbody_hex(teff)
    return blackbody_hex(teff)


def _hex_to_unit_rgb(h: str) -> tuple[float, float, float]:
    r, g, b = hex_to_rgb_int(h)
    return (r / 255.0, g / 255.0, b / 255.0)


# ── field formatting ─────────────────────────────────────────────────

def _c4(rgb: tuple[float, float, float], scale: float = 1.0, alpha: float = 1.0) -> str:
    r, g, b = (min(max(v * scale, 0.0), 1.0) for v in rgb)
    return f"{r:.4g},{g:.4g},{b:.4g},{alpha:g}"


# rim/sunspot *sharpness* by class (NOT color): hotter -> tighter rim, finer
# spots. Colors are derived from the grounded base hex; only these shape
# parameters are parametric. (rimPower, rimBlend, sunspotPower)
_CLASS_RIM = {
    "O": (0.25, 0.9, 40), "B": (0.3, 1.0, 30), "A": (0.4, 1.5, 20),
    "F": (0.55, 2.5, 12), "G": (0.7, 3.5, 8),  "K": (0.8, 4.0, 4),
    "M": (0.9, 4.0, 1),   "L": (0.95, 4.0, 1), "T": (0.95, 4.0, 1),
    "Y": (0.95, 4.0, 1),  "D": (0.4, 1.5, 2),  "?": (0.7, 3.5, 8),
}


def light_block(teff: float, l_lsun: float, spectype: str | None) -> dict[str, str]:
    """ScaledVersion.Light scalar + color fields (curves are separate).

    All colors here are the grounded base hex (`base_tint_hex`) or a scalar
    dimming of it (ambient); none is an independent color computation."""
    rgb = _hex_to_unit_rgb(base_tint_hex(teff, spectype))
    base = _c4(rgb)
    return {
        "sunlightColor": base,
        "sunlightShadowStrength": "0.75",
        "scaledSunlightColor": base,
        "IVASunColor": base,
        "ambientLightColor": _c4(rgb, scale=0.06),   # base hex, dimmed to ambient
        "sunLensFlareColor": base,
        "givesOffLight": "True",
        "sunAU": str(SUN_AU_REF),
        "luminosity": f"{SOL_LUMINOSITY_WM2 * l_lsun:.6g}",  # = 1360 * L/Lsun
        "insolation": str(INSOLATION),
        "radiationFactor": str(RADIATION_FACTOR),
    }


def material_block(teff: float, spectype: str | None, sunspot_tex: str) -> dict[str, str]:
    """ScaledVersion.Material fields.

    emitColor/rimColor are scalar dimmings of the grounded base hex (rendering
    derivations, not a second color path); rim/sunspot *sharpness* is the only
    parametric-by-class knob (`_CLASS_RIM`)."""
    rgb = _hex_to_unit_rgb(base_tint_hex(teff, spectype))
    rim_power, rim_blend, sunspot_power = _CLASS_RIM[_spectral_class(spectype)]
    return {
        "emitColor0": _c4(rgb, scale=0.85),   # base hex, slightly dimmed
        "emitColor1": _c4(rgb, scale=0.7),    # base hex, dimmed further
        "rimColor": _c4(rgb),                 # base hex
        "rimPower": f"{rim_power:g}",
        "rimBlend": f"{rim_blend:g}",
        "noiseMap": sunspot_tex,
        "sunspotTex": sunspot_tex,
        "sunspotPower": str(sunspot_power),
        "sunspotColor": "1,1,1,1",
    }


def _curve(keys: list[tuple[float, float]], indent: str) -> str:
    return "\n".join(f"{indent}    key = {k:g} {v:g} 0 0" for k, v in keys)


def intensity_curves_text(l_lsun: float, indent: str = "            ") -> str:
    """The four FloatCurves, generated parametrically (scaled by sqrt(L)).

    Distance falloffs only — per-star brightness is carried by `luminosity`.
    Anchored on Sol's ~100 AU light reach at L=1; reach ∝ sqrt(L)."""
    reach = LIGHT_REACH_SOL_M * math.sqrt(max(l_lsun, 1e-6))
    scaled_reach = 2.5e7 * math.sqrt(max(l_lsun, 1e-6))
    brightness = [(0.0, 0.2), (5.0, 4.0 * math.sqrt(max(l_lsun, 1e-6))), (40.0, 1.8)]
    intensity = [(0.0, 0.9), (reach * 0.1, 0.9), (reach, 0.0)]
    scaled = [(0.0, 1.0), (scaled_reach, 1.0), (scaled_reach * 10.0, 0.0)]
    iva = [(0.0, 0.8), (1.0, 0.8)]
    blocks = []
    for name, keys in (("brightnessCurve", brightness), ("IntensityCurve", intensity),
                       ("ScaledIntensityCurve", scaled), ("IVAIntensityCurve", iva)):
        blocks.append(f"{indent}{name}\n{indent}{{\n{_curve(keys, indent)}\n{indent}}}")
    return "\n".join(blocks)


# ── self-test: color sanity across regimes (all via the grounded engine) ──
if __name__ == "__main__":
    print("Teff   type        base hex   regime path")
    cases = [
        (5772, "G2 V"), (5143, "K0.5 V"), (17200, "DA"), (8600, "A3 V"),
        (3665, "M1 Ve"), (3195, "M4.0 Ve"), (2904, "M5.5 Ve"),
        (1310, "L7.5"), (1280, "T0.5"), (910, "T6"), (482, "Y"),
    ]
    for teff, sp in cases:
        print(f"{teff:5d}  {sp:10}  {base_tint_hex(teff, sp):9}  class={_spectral_class(sp)}")
