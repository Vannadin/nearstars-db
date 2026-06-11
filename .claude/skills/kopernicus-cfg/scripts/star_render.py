#!/usr/bin/env python3
# Teff/L/분광형 -> Kopernicus 항성 ScaledVersion(Light/Material/Coronas) 값을 생성하는 순수 모듈
"""Star-rendering field synthesis for the Kopernicus emitter.

Pure functions (no DB, no file I/O, no body-name logic, no numpy) that turn
curated stellar parameters into Kopernicus `ScaledVersion` field text:

    Teff (K)        -> blackbody sRGB -> Light colors + Material emit/rim
    L   (Lsun)      -> luminosity (= 1360 * L/Lsun) + intensity curves
    spectral type   -> rim/sunspot sharpness tuning

Conventions are anchored on RSS-Reborn/Sol-Configs' Sun cfg (a FACT/convention,
not copied text — Sol-Configs stays link-only per project policy):
  * `luminosity` is flux in W/m^2 at `sunAU`; Sol = 1360. So a star's value is
    `1360 * L_star/L_sun`.  (NB: the kopernicus-cfg skill's old star-body.md
    example used `luminosity = L_in_Lsun` directly — that is WRONG vs Sol and
    is corrected by this module.)
  * `sunAU` is kept at Sol-Configs' reference constant 13599840256 (NOT the real
    AU) — even Sol-Configs leaves it at the stock value at real scale.
  * `insolation = 0.15`, `radiationFactor = 1` (Sol defaults).

The blackbody->sRGB path mirrors the validated method in
`scripts/phase3/disk_color_mie.py` (Planck * Wyman-2013 CMF gaussians * XYZ->sRGB),
ported to dependency-free Python.

Intensity curves are PARAMETRIC (generated here, scaled by sqrt(L)); curve
fidelity is an acknowledged future refinement — `luminosity` is the dominant
brightness knob, the curves are distance falloffs.
"""
from __future__ import annotations

import math

# ── physical / convention constants ──────────────────────────────────
SOLAR_TEFF = 5772.0
SOL_LUMINOSITY_WM2 = 1360.0          # Sol-Configs Sun `luminosity` (W/m^2 @ sunAU)
SUN_AU_REF = 13599840256             # Sol-Configs `sunAU` reference constant (m)
INSOLATION = 0.15                    # Sol default
RADIATION_FACTOR = 1                 # Sol default
LIGHT_REACH_SOL_M = 1.49597871e13    # Sol IntensityCurve outer cutoff (~100 AU) at L=1

_WL = [380.0 + 10.0 * i for i in range(41)]   # 380..780 nm, matches disk_color_mie


# ── blackbody -> sRGB (pure python port of disk_color_mie method) ─────

def _planck(wl_nm: float, teff: float) -> float:
    wl = wl_nm * 1e-9
    h, c, kB = 6.626e-34, 3.0e8, 1.381e-23
    return (1.0 / wl ** 5) / (math.exp(h * c / (wl * kB * teff)) - 1.0)


def _g(x: float, a: float, mu: float, s1: float, s2: float) -> float:
    s = s1 if x < mu else s2
    return a * math.exp(-0.5 * ((x - mu) / s) ** 2)


def _cie_xyz(spec: list[float]) -> tuple[float, float, float]:
    # Wyman et al. 2013 multi-lobe gaussian fit to the CIE 1931 2-deg CMFs
    X = Y = Z = 0.0
    for wl, s in zip(_WL, spec):
        xbar = (_g(wl, 1.056, 599.8, 37.9, 31.0) + _g(wl, 0.362, 442.0, 16.0, 26.7)
                + _g(wl, -0.065, 501.1, 20.4, 26.2))
        ybar = _g(wl, 0.821, 568.8, 46.9, 40.5) + _g(wl, 0.286, 530.9, 16.3, 31.1)
        zbar = _g(wl, 1.217, 437.0, 11.8, 36.0) + _g(wl, 0.681, 459.0, 26.0, 13.8)
        X += s * xbar; Y += s * ybar; Z += s * zbar
    return X, Y, Z


def _xyz_to_lin_rgb(xyz: tuple[float, float, float]) -> tuple[float, float, float]:
    X, Y, Z = xyz
    r = 3.2406 * X - 1.5372 * Y - 0.4986 * Z
    g = -0.9689 * X + 1.8758 * Y + 0.0415 * Z
    b = 0.0557 * X - 0.2040 * Y + 1.0570 * Z
    return r, g, b


def _lin_rgb_for_teff(teff: float) -> tuple[float, float, float]:
    return _xyz_to_lin_rgb(_cie_xyz([_planck(wl, teff) for wl in _WL]))


def blackbody_rgb(teff: float) -> tuple[float, float, float]:
    """Normalized linear-ish sRGB (0..1, brightest channel = 1) for a star of
    temperature `teff`, white-balanced so the Sun (5772 K) reads ~white. M/K
    stars come out warm/orange, A stars blue-white."""
    lin = _lin_rgb_for_teff(teff)
    sun = _lin_rgb_for_teff(SOLAR_TEFF)
    # white-balance to the Sun, then clip negatives and normalize to max channel
    wb = [max(c / s, 0.0) for c, s in zip(lin, sun)]
    mx = max(wb) or 1.0
    wb = [c / mx for c in wb]
    # sRGB gamma
    out = []
    for c in wb:
        c = min(max(c, 0.0), 1.0)
        out.append(12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055)
    return tuple(min(max(c, 0.0), 1.0) for c in out)  # type: ignore[return-value]


# ── field formatting ─────────────────────────────────────────────────

def _c4(rgb: tuple[float, float, float], scale: float = 1.0, alpha: float = 1.0) -> str:
    r, g, b = (min(max(v * scale, 0.0), 1.0) for v in rgb)
    return f"{r:.4g},{g:.4g},{b:.4g},{alpha:g}"


def _spectral_class(spectype: str | None) -> str:
    """First letter of an OBAFGKM(LT) spectral type; '?' if unknown."""
    if not spectype:
        return "?"
    for ch in spectype.strip():
        u = ch.upper()
        if u in "OBAFGKMLTY":
            return u
        if ch.isdigit():
            break
    return "?"


# rim/sunspot sharpness by class: hotter -> tighter rim, finer spots.
# (rimPower, rimBlend, sunspotPower)
_CLASS_RIM = {
    "O": (0.25, 0.9, 40), "B": (0.3, 1.0, 30), "A": (0.4, 1.5, 20),
    "F": (0.55, 2.5, 12), "G": (0.7, 3.5, 8),  "K": (0.8, 4.0, 4),
    "M": (0.9, 4.0, 1),   "L": (0.95, 4.0, 1), "T": (0.95, 4.0, 1),
    "Y": (0.95, 4.0, 1),  "?": (0.7, 3.5, 8),
}


def light_block(teff: float, l_lsun: float) -> dict[str, str]:
    """ScaledVersion.Light scalar + color fields (curves are separate)."""
    rgb = blackbody_rgb(teff)
    base = _c4(rgb)
    return {
        "sunlightColor": base,
        "sunlightShadowStrength": "0.75",
        "scaledSunlightColor": base,
        "IVASunColor": base,
        "ambientLightColor": _c4(rgb, scale=0.06),
        "sunLensFlareColor": base,
        "givesOffLight": "True",
        "sunAU": str(SUN_AU_REF),
        "luminosity": f"{SOL_LUMINOSITY_WM2 * l_lsun:.6g}",  # = 1360 * L/Lsun
        "insolation": str(INSOLATION),
        "radiationFactor": str(RADIATION_FACTOR),
    }


def material_block(teff: float, spectype: str | None, sunspot_tex: str,
                   corona_unused: None = None) -> dict[str, str]:
    rgb = blackbody_rgb(teff)
    rim_power, rim_blend, sunspot_power = _CLASS_RIM[_spectral_class(spectype)]
    return {
        "emitColor0": _c4(rgb, scale=0.85),
        "emitColor1": _c4(rgb, scale=0.7),
        "rimColor": _c4(rgb),
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


# ── self-test: color sanity across spectral types ────────────────────
if __name__ == "__main__":
    print("Teff   class  blackbody sRGB        luminosity(L=1)")
    for teff, sp in [(3000, "M4 V"), (4000, "K5 V"), (5772, "G2 V"),
                     (6500, "F5 V"), (9600, "A0 V"), (25000, "B1 V")]:
        rgb = blackbody_rgb(teff)
        print(f"{teff:5d}  {_spectral_class(sp):>3}    {_c4(rgb):22} "
              f"{light_block(teff, 1.0)['luminosity']}")
