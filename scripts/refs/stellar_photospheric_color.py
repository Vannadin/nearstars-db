# 항성 Teff/스펙트럼형에서 광구 가시색(sRGB)을 실측 Pickles SED + 공용 CIE 엔진으로 계산
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
