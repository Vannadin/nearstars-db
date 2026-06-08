# Planck 흑체복사 + CIE 1931 등색함수(Wyman 2013) → sRGB hue 변환 공용 모듈
"""Shared colorimetry: Planck blackbody + CIE 1931 color-matching functions
(Wyman, Sloan & Shirley 2013 analytic fit) + XYZ→sRGB hue normalization.

Both the temperature-color builder and the Saha/Boltzmann LTE engine convert a
spectral radiance I(λ) into a display color through this one path, so the two
share an identical colorimetry. Colors are returned as HUE at full brightness
(max-channel normalized), not absolute luminance.

The CMF fit is multi-lobe piecewise-Gaussian; sigma values are inverse widths
(1/nm). Lambda grid is 360-830 nm in 1 nm steps.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

# Sibling reuse for hex helpers.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from wavelength_to_rgb import rgb_to_hex, hex_to_rgb  # noqa: E402,F401  (re-export)

# ─────────────────────────────────────────────────────────────────────
# CIE 1931 2-deg color-matching functions — Wyman, Sloan & Shirley 2013,
# "Simple Analytic Approximations to the CIE XYZ Color Matching Functions"
# (JCGT 2(2)).
# ─────────────────────────────────────────────────────────────────────

def _g(x: float, mu: float, s1: float, s2: float) -> float:
    t = (x - mu) * (s1 if x < mu else s2)
    return math.exp(-0.5 * t * t)


def _xbar(w: float) -> float:
    return (1.056 * _g(w, 599.8, 0.0264, 0.0323)
            + 0.362 * _g(w, 442.0, 0.0624, 0.0374)
            - 0.065 * _g(w, 501.1, 0.0490, 0.0382))


def _ybar(w: float) -> float:
    return (0.821 * _g(w, 568.8, 0.0213, 0.0247)
            + 0.286 * _g(w, 530.9, 0.0613, 0.0322))


def _zbar(w: float) -> float:
    return (1.217 * _g(w, 437.0, 0.0845, 0.0278)
            + 0.681 * _g(w, 459.0, 0.0385, 0.0725))


LAMBDAS = list(range(360, 831))   # 1 nm steps, 360-830 nm
_C2_NM_K = 1.4388e7               # hc/k in nm*K


def planck_rel(wl_nm: float, T: float) -> float:
    """Relative spectral radiance (shape only) — Planck's law."""
    x = _C2_NM_K / (wl_nm * T)
    if x > 700:                   # guard overflow at low T / short wl
        return 0.0
    return (wl_nm ** -5) / (math.exp(x) - 1.0)


def xyz_to_srgb_hue(X: float, Y: float, Z: float) -> tuple[float, float, float]:
    """XYZ → sRGB (0-1), clamped + max-normalized to show HUE at full
    brightness (not absolute luminance), then sRGB-gamma encoded."""
    r = 3.2406 * X - 1.5372 * Y - 0.4986 * Z
    g = -0.9689 * X + 1.8758 * Y + 0.0415 * Z
    b = 0.0557 * X - 0.2040 * Y + 1.0570 * Z
    r, g, b = (max(0.0, c) for c in (r, g, b))   # clamp out-of-gamut
    peak = max(r, g, b)
    if peak <= 0.0:
        return (0.0, 0.0, 0.0)
    r, g, b = r / peak, g / peak, b / peak        # normalize hue (scale-free)

    def gamma(c: float) -> float:
        return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055

    return gamma(r), gamma(g), gamma(b)


def spectrum_to_xyz(intensity) -> tuple[float, float, float]:
    """Integrate a spectral radiance against the CIE CMF → (X, Y, Z).

    `intensity` is a sequence aligned to LAMBDAS (one value per nm, 360-830),
    or a callable intensity(wl_nm). Absolute scale is irrelevant — only the
    spectral shape sets the resulting hue.
    """
    call = callable(intensity)
    X = Y = Z = 0.0
    for i, wl in enumerate(LAMBDAS):
        I = intensity(wl) if call else intensity[i]
        X += I * _xbar(wl)
        Y += I * _ybar(wl)
        Z += I * _zbar(wl)
    return X, Y, Z


def spectrum_to_srgb_hue(intensity) -> tuple[float, float, float]:
    """Spectral radiance → sRGB hue (0-1)."""
    return xyz_to_srgb_hue(*spectrum_to_xyz(intensity))


def spectrum_to_hex(intensity) -> str:
    return rgb_to_hex(spectrum_to_srgb_hue(intensity))


def blackbody_srgb(T: float) -> tuple[tuple[float, float, float], tuple[float, float]]:
    """Return ((r,g,b) 0-1, (x,y) chromaticity) for a blackbody at T."""
    X = Y = Z = 0.0
    for wl in LAMBDAS:
        b = planck_rel(wl, T)
        X += b * _xbar(wl)
        Y += b * _ybar(wl)
        Z += b * _zbar(wl)
    s = X + Y + Z
    xy = (X / s, Y / s) if s > 0 else (0.0, 0.0)
    return xyz_to_srgb_hue(X, Y, Z), xy
