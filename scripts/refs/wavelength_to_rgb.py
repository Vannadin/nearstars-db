# 가시광선 파장 → sRGB 변환 (Bruton 1996 piecewise + CIE 1931 비교용)
# regenerable: library module, imported by cie_color.py, build_molecular_db.py, the element-DB migrate/populate scripts, and phase3/build_html.py
"""Wavelength → sRGB conversion for the plasma color DB.

Uses the Bruton 1996 piecewise approximation. While CIE 1931 + sRGB
gamma is the colorimetrically correct path, the Bruton fit is the
documented standard for "what does a spectral line look like" on a
display, and is the canonical version used by visible-spectrum
visualizers across the web. It's an empirical fit to how observers
perceive narrow-band emission on calibrated displays.

Functions:
    wavelength_to_rgb(nm)              → (r, g, b) in [0, 1]
    mix_lines([(nm, intensity), ...])  → (r, g, b) in [0, 1]
    rgb_to_hex((r, g, b))              → "#rrggbb"

Mixing uses additive XYZ-equivalent: each line contributes proportional
to (intensity × visibility_factor) so multi-line mixes preserve hue
relations even when one line is outside visible.

Validation (in __main__): Na 589 → yellow, Hα 656 → red, OI 558 → green,
N2+ 391 → violet, H Balmer mix → hot pink.

Sources:
    Bruton, Dan. "Color science." Texas A&M University, 1996.
    http://www.physics.sfasu.edu/astro/color/spectra.html
"""
from __future__ import annotations


def _piecewise_rgb(wl: float) -> tuple[float, float, float]:
    """Bruton 1996 piecewise wavelength → linear RGB (0–1).

    Returns (0, 0, 0) outside the 380–780 nm visible band.
    """
    if wl < 380 or wl > 780:
        return 0.0, 0.0, 0.0

    if wl < 440:
        r = -(wl - 440) / (440 - 380)
        g = 0.0
        b = 1.0
    elif wl < 490:
        r = 0.0
        g = (wl - 440) / (490 - 440)
        b = 1.0
    elif wl < 510:
        r = 0.0
        g = 1.0
        b = -(wl - 510) / (510 - 490)
    elif wl < 580:
        r = (wl - 510) / (580 - 510)
        g = 1.0
        b = 0.0
    elif wl < 645:
        r = 1.0
        g = -(wl - 645) / (645 - 580)
        b = 0.0
    else:  # 645..780
        r = 1.0
        g = 0.0
        b = 0.0
    return r, g, b


def _display_brightness(wl: float) -> float:
    """Brightness ramp for SINGLE-line display.

    Goal: show saturated hue across most of visible band, gentle taper
    at IR/UV edges. Bruton's original formulation (full 420–700 nm,
    30% at edges) — eye adapts when viewing a single line in isolation,
    so absolute photopic dimness doesn't apply.
    """
    if wl < 380 or wl > 780:
        return 0.0
    if wl < 420:
        return 0.3 + 0.7 * (wl - 380) / (420 - 380)
    if wl <= 700:
        return 1.0
    return 0.3 + 0.7 * (780 - wl) / (780 - 700)


def _photopic_v(wl: float) -> float:
    """CIE 1931 photopic luminosity function V(λ) for MIX weighting.

    Peak at 555 nm (=1.0), drops sharply outside. Critical for
    multi-line mixes — at the IR edge (766 nm K I) perceived brightness
    is ~10⁴× lower than at 555 nm, so naive NIST-intensity weighting
    gives wrong colors (K I 766/770 IR appears to dominate over 404 nm
    violet by intensity but is essentially invisible perceptually).

    Gaussian fit: V(λ) ≈ 1.019 · exp(-285.4 · (λ/1000 − 0.559)²).
    Within ~10% of CIE V(λ) tables over 400–700 nm.
    """
    import math
    if wl < 380 or wl > 780:
        return 0.0
    return max(1e-6, 1.019 * math.exp(-285.4 * ((wl / 1000.0) - 0.559) ** 2))


def _gamma(c: float, gamma: float = 0.8) -> float:
    """Bruton uses γ=0.8 (compresses highs slightly, brightens mid).

    Per Bruton's original code; not strict sRGB gamma. Matches how the
    historical visible-spectrum images on physics.sfasu.edu look.
    """
    return c ** gamma if c > 0 else 0.0


def wavelength_to_rgb(wl: float, intensity: float = 1.0) -> tuple[float, float, float]:
    """Single wavelength → sRGB (0–1).

    For displaying what a monochromatic line LOOKS like when viewed
    in isolation. Uses display brightness ramp (saturated hue across
    bulk of visible band).
    """
    r, g, b = _piecewise_rgb(wl)
    factor = _display_brightness(wl) * intensity
    r = _gamma(r * factor)
    g = _gamma(g * factor)
    b = _gamma(b * factor)
    return r, g, b


def mix_lines(lines: list[tuple[float, float]]) -> tuple[float, float, float]:
    """Multi-line perceptual mix.

    Each line contributes (raw RGB × intensity × V(λ)) where V(λ) is
    the photopic luminosity function. Result is gamma-corrected at
    the end. Hue is preserved by normalizing the peak channel.

    Args:
        lines: list of (wavelength_nm, intensity) tuples.
               Intensities are relative (e.g., NIST relative_intensity
               scaled to peak = 1, or arbitrary positive floats).

    For NIST relative_intensity values: pass the published numbers
    directly. V(λ) handles the perceptual scaling.
    """
    r_sum = g_sum = b_sum = 0.0
    for wl, i in lines:
        r, g, b = _piecewise_rgb(wl)
        f = _photopic_v(wl) * i
        r_sum += r * f
        g_sum += g * f
        b_sum += b * f
    peak = max(r_sum, g_sum, b_sum, 1e-9)
    return _gamma(r_sum / peak), _gamma(g_sum / peak), _gamma(b_sum / peak)


def rgb_to_hex(rgb: tuple[float, float, float]) -> str:
    r, g, b = rgb
    return "#{:02x}{:02x}{:02x}".format(
        max(0, min(255, round(r * 255))),
        max(0, min(255, round(g * 255))),
        max(0, min(255, round(b * 255))),
    )


def hex_to_rgb(hexstr: str) -> tuple[float, float, float]:
    h = hexstr.lstrip("#")
    return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255)


# ─────────────────────────────────────────────────────────────────────
# Self-test
# ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    cases = [
        ("Na D-line 589nm",            589.0,   "saturated yellow"),
        ("Hα 656.3nm",                 656.3,   "red"),
        ("OI green 557.7nm",           557.7,   "green"),
        ("OI red 630.0nm",             630.0,   "orange-red"),
        ("N2+ 391.4nm",                391.4,   "violet (visibility ramped)"),
        ("Cu band 510nm",              510.0,   "green"),
        ("K I 766.5nm IR",             766.5,   "dim red"),
        ("K I 404nm violet",           404.0,   "violet, dim"),
        ("Hg 546.1nm",                 546.1,   "green"),
        ("Li 670.8nm",                 670.8,   "crimson red"),
        ("Sr 605nm",                   605.0,   "orange"),
        ("Ba 553nm",                   553.0,   "yellow-green"),
    ]
    print("=== Single-line tests ===")
    for label, wl, expected in cases:
        rgb = wavelength_to_rgb(wl)
        print(f"  {label:30s}  {rgb_to_hex(rgb)}  (expected: {expected})")

    mixes = [
        ("H Balmer (NIST: Hα 500, Hβ 100, Hγ 50)",
            [(656.3, 500.0), (486.1, 100.0), (434.0, 50.0)],
            "hot pink"),
        ("Na D doublet",
            [(589.0, 1.0), (589.6, 0.5)],
            "saturated yellow"),
        ("K I 766+770 IR + 404 violet (1:1:0.3)",
            [(766.5, 1.0), (769.9, 1.0), (404.0, 0.3)],
            "lilac (red + violet)"),
        ("Earth aurora 557+630 (1:0.4)",
            [(557.7, 1.0), (630.0, 0.4)],
            "yellow-green"),
        ("CuCl 510+515+520",
            [(510.0, 1.0), (515.0, 0.8), (520.0, 0.6)],
            "green"),
        ("Sr crimson 605+640 (1:0.7)",
            [(605.0, 1.0), (640.0, 0.7)],
            "crimson red"),
    ]
    print("\n=== Multi-line mixes ===")
    for label, lines, expected in mixes:
        rgb = mix_lines(lines)
        print(f"  {label:40s}  {rgb_to_hex(rgb)}  (expected: {expected})")
