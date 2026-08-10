# 항성 Teff/스펙트럼형에서 광구 가시색(sRGB)을 실측 Pickles SED + 공용 CIE 엔진으로 계산
# regenerable: computes stellar photospheric sRGB tint, backs stellar-photospheric-color-methodology.md
"""Stellar photospheric color — Teff/spectral-type -> visible sRGB tint.

Backs `docs/reference/stellar-photospheric-color-methodology.md`. Two paths,
both through the project's shared colorimetry engine (`cie_color.py`, the same
CIE 1931 -> sRGB used by the reflected-color and plasma docs):

  * FGK / white dwarfs   -> Planck blackbody at Teff (good approximation; the
    displayed tints are near-white with a faint warm/cool cast).
  * M dwarfs             -> a REAL observed SED from the Pickles 1998 stellar
    spectral flux library (1998PASP..110..863P), which carries the true TiO/VO/
    H2O molecular-band structure. The blackbody is only a fair approximation for
    M dwarfs; the molecular bands shift the brightness-normalized chromaticity
    modestly (a pale warm orange, NOT a brick-red — the large molecular effect
    is on color index / luminosity, not the displayed hue).

Pipeline validation: the Pickles G2V SED through this engine returns ~#fff4f2,
matching the standard rendered solar color (~#fff5f2).

Pickles spectra are fetched on demand from VizieR (J/PASP/110/863) and cached
under `scripts/refs/.cache/pickles/` (gitignored), mirroring how the plasma
builders cache their NIST source data. Run with no network only if the cache is
already populated.
"""
from __future__ import annotations

import bisect
import gzip
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cie_color import LAMBDAS, spectrum_to_hex, blackbody_srgb, rgb_to_hex  # noqa: E402

_CACHE = Path(__file__).resolve().parent / ".cache" / "pickles"
_VIZIER = "https://cdsarc.cds.unistra.fr/ftp/cats/J/PASP/110/863"

# Pickles dwarf templates actually used, with their library effective temperatures.
_PICKLES_TEFF = {
    "g2v": 5772, "m0v": 3850, "m1v": 3680, "m2v": 3500,
    "m3v": 3350, "m4v": 3170, "m5v": 3050, "m6v": 2800,
}

# NearStars M-dwarf roster: curated Teff (K) -> tint via Pickles interpolation.
NEARSTARS_M_DWARFS = [
    ("AU Mic",    "M1",   3665),
    ("GJ 896 A",  "M3.5", 3300),
    ("Barnard",   "M4",   3195),
    ("40 Eri C",  "M4.5", 3167),
    ("YZ Cet",    "M4.5", 3100),
    ("GJ 9066",   "M4.5", 3100),
    ("Proxima",   "M5.5", 2904),
    ("Teegarden", "M7",   2900),
]


def _pickles_path(name: str) -> Path:
    _CACHE.mkdir(parents=True, exist_ok=True)
    dat = _CACHE / f"{name}.dat"
    if not dat.exists():
        url = f"{_VIZIER}/{name}.dat.gz"
        raw = gzip.decompress(urllib.request.urlopen(url, timeout=30).read())
        dat.write_bytes(raw)
    return dat


def load_pickles_sed(name: str) -> list[float]:
    """Pickles .dat (lambda[A], f_lambda) resampled onto the CMF grid LAMBDAS."""
    wl, fl = [], []
    for line in _pickles_path(name).read_text().splitlines():
        p = line.split()
        if len(p) < 2:
            continue
        try:
            a, f = float(p[0]), float(p[1])
        except ValueError:
            continue
        wl.append(a / 10.0)          # Angstrom -> nm
        fl.append(max(0.0, f))
    out = []
    for L in LAMBDAS:
        if L <= wl[0] or L >= wl[-1]:
            out.append(0.0)
            continue
        i = bisect.bisect_left(wl, L)
        x0, x1, y0, y1 = wl[i - 1], wl[i], fl[i - 1], fl[i]
        out.append(y0 + (y1 - y0) * (L - x0) / (x1 - x0) if x1 > x0 else y0)
    return out


def pickles_hex(name: str) -> str:
    return spectrum_to_hex(load_pickles_sed(name))


# ── ultracool dwarfs (L / T / Y) and the continuous Teff ladder ─────────────
# Below ~2600 K the visible band is shaped by condensate clouds and by the
# pressure-broadened Na I / K I resonance wings, not by a continuum, so neither
# the blackbody nor the Pickles M templates apply. Grids:
#   L, T  : BT-Settl (Allard, Homeier & Freytag 2012, 2012RSPTA.370.2765A)
#   Y     : Morley et al. 2014 water-cloud models (2014ApJ...787...78M)
# Both come from the SVO Theoretical Spectra Server and cache like Pickles does.
_UC_CACHE = Path(__file__).resolve().parent / ".cache"
_SVO = "http://svo2.cab.inta-csic.es/theory/newov2/ssap.php"

# (grid, Teff) -> SVO file id.  logg 5.0, solar metallicity; Morley f_sed 5.
_BTSETTL_FID = {
    600: 13643, 700: 13648, 800: 13652, 900: 13657, 1000: 13661, 1100: 13666,
    1200: 13671, 1300: 13676, 1400: 13681, 1500: 13686, 1600: 13691, 1700: 13696,
    1800: 13701, 1900: 13706, 2000: 13718, 2100: 13730, 2200: 13742, 2300: 13754,
    2400: 13766, 2500: 13778, 2600: 185, 2800: 495, 3000: 806,
}
_MORLEY_FID = {400: 63, 450: 70}


def _svo_path(grid: str, teff: int, fid: int) -> Path:
    d = _UC_CACHE / grid
    d.mkdir(parents=True, exist_ok=True)
    dat = d / f"{grid}_{teff}.txt"
    if not dat.exists():
        url = f"{_SVO}?model={grid}&fid={fid}&format=ascii"
        dat.write_bytes(urllib.request.urlopen(url, timeout=180).read())
    return dat


def _resample_ascii(path: Path) -> list[float]:
    """SVO ascii (lambda[A], f_lambda) resampled onto the CMF grid."""
    wl, fl = [], []
    for line in path.read_text().splitlines():
        if line.startswith("#"):
            continue
        p = line.split()
        if len(p) < 2:
            continue
        try:
            a, f = float(p[0]), float(p[1])
        except ValueError:
            continue
        if 3000.0 <= a <= 9000.0:
            wl.append(a / 10.0)
            fl.append(max(0.0, f))
    out = []
    for L in LAMBDAS:
        if L <= wl[0] or L >= wl[-1]:
            out.append(0.0)
            continue
        i = bisect.bisect_left(wl, L)
        x0, x1, y0, y1 = wl[i - 1], wl[i], fl[i - 1], fl[i]
        out.append(y0 + (y1 - y0) * (L - x0) / (x1 - x0) if x1 > x0 else y0)
    return out


def ultracool_hex(teff: int) -> str:
    """L/T dwarf photosphere colour from BT-Settl (grid points only)."""
    return spectrum_to_hex(_resample_ascii(_svo_path("bt-settl", teff, _BTSETTL_FID[teff])))


def ydwarf_hex(teff: int) -> str:
    """Y dwarf photosphere colour from Morley+ 2014 (grid points only).

    BT-Settl is not usable here: its 400-500 K models return a larger visible-band
    integral than its own 800 K model, so the grid changes regime below ~600 K.
    """
    return spectrum_to_hex(_resample_ascii(_svo_path("morley14", teff, _MORLEY_FID[teff])))


# ── the continuous ladder ───────────────────────────────────────────────────
# One knot per model, each reduced to its CHROMATICITY (normalised to a common
# luminance): how bright to draw a swatch is a UI decision, what colour it is
# is not. colour_for_teff() interpolates between knots in linear light, so a
# body is drawn at its own temperature rather than snapped to a grid step.
def _srgb_to_linear(c: float) -> float:
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _linear_to_srgb(c: float) -> float:
    c = max(0.0, min(1.0, c))
    return 255.0 * (12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055)


def _chromaticity(hexstr: str) -> list[float]:
    v = [_srgb_to_linear(int(hexstr.lstrip("#")[i:i + 2], 16)) for i in (0, 2, 4)]
    y = 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]
    return [c / y for c in v] if y > 0 else v


def ladder_knots() -> list[tuple[int, list[float]]]:
    """(Teff, linear-RGB chromaticity) knots across the whole roster range."""
    knots = [(t, ydwarf_hex(t)) for t in sorted(_MORLEY_FID)]
    knots += [(t, ultracool_hex(t)) for t in sorted(_BTSETTL_FID)]
    knots += [(t, mdwarf_tint(t)) for t in (3200, 3500, 3850)]
    knots += [(t, blackbody_hex(t)) for t in
              (4200, 4800, 5500, 6500, 8000, 10000, 15000, 25000, 40000)]
    return [(t, _chromaticity(h)) for t, h in sorted(knots)]


def _to_gamut(v: list[float], luminance: float) -> list[float]:
    """Bring an out-of-gamut chromaticity into sRGB by desaturating, not clipping.

    Cool dwarf chromaticities sit well outside sRGB — at 1100 K the blue channel
    wants 4.3x maximum and green goes negative. Clipping each channel separately
    is what produced the vivid magenta in the first pass: it invents saturation the
    colour never had and can move the hue. Mixing toward a grey of the same
    luminance keeps the hue and gives up only what the display cannot show.
    """
    lo, hi = 0.0, 1.0
    for _ in range(40):
        t = (lo + hi) / 2
        c = [(1 - t) * x + t * luminance for x in v]
        if all(-1e-9 <= x <= 1 + 1e-9 for x in c):
            hi = t
        else:
            lo = t
    return [(1 - hi) * x + hi * luminance for x in v]


def colour_for_teff(teff: float, luminance: float = 0.46) -> str:
    """Photospheric colour at ANY Teff — knots interpolated in linear light."""
    knots = ladder_knots()
    if teff <= knots[0][0]:
        v = knots[0][1]
    elif teff >= knots[-1][0]:
        v = knots[-1][1]
    else:
        i = bisect.bisect_left([k[0] for k in knots], teff)
        t0, v0 = knots[i - 1]
        t1, v1 = knots[i]
        f = (teff - t0) / (t1 - t0)
        v = [a + (b - a) * f for a, b in zip(v0, v1)]
    y = 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]
    v = _to_gamut([c * luminance / y for c in v], luminance)
    return "#%02x%02x%02x" % tuple(
        int(round(max(0, min(255, _linear_to_srgb(c))))) for c in v)


def blackbody_hex(teff: float) -> str:
    rgb, _ = blackbody_srgb(teff)
    return rgb_to_hex(rgb)


def _m_anchors() -> list[tuple[int, tuple[int, int, int]]]:
    out = []
    for name, T in _PICKLES_TEFF.items():
        if not name.startswith("m"):
            continue
        h = pickles_hex(name)
        out.append((T, hex_to_rgb_int(h)))
    return sorted(out)


def hex_to_rgb_int(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def mdwarf_tint(teff: float) -> str:
    """Real-SED tint at an arbitrary M-dwarf Teff, interpolated between the
    bracketing Pickles templates (the M-sequence chromaticity is nearly flat)."""
    a = _m_anchors()
    if teff <= a[0][0]:
        rgb = a[0][1]
    elif teff >= a[-1][0]:
        rgb = a[-1][1]
    else:
        for i in range(len(a) - 1):
            if a[i][0] <= teff <= a[i + 1][0]:
                (t0, c0), (t1, c1) = a[i], a[i + 1]
                f = (teff - t0) / (t1 - t0)
                rgb = tuple(round(c0[j] + f * (c1[j] - c0[j])) for j in range(3))
                break
    return "#%02x%02x%02x" % rgb


def main() -> None:
    print("Sun validation (Pickles G2V):", pickles_hex("g2v"), "(expect ~#fff4f2)")
    print()
    print(f"{'star':12s}{'type':6s}{'Teff':6s}{'blackbody':11s}real (Pickles ladder)")
    for name, typ, teff in NEARSTARS_M_DWARFS:
        print(f"{name:12s}{typ:6s}{teff:<6d}{blackbody_hex(teff):11s}{mdwarf_tint(teff)}")


if __name__ == "__main__":
    main()
