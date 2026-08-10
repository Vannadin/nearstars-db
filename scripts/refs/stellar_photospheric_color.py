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


# ── ultracool dwarfs (L / T / Y): BT-Settl model atmospheres ─────────────────
# Pickles stops at M; below that the optical spectrum is shaped by dust clouds
# and by the pressure-broadened Na I / K I resonance wings, not by a blackbody.
# BT-Settl (Allard, Homeier & Freytag 2012, 2012RSPTA.370.2765A) is the standard
# grid for this regime; spectra come from the SVO Theoretical Spectra server and
# are cached next to the Pickles ones.
_BTSETTL_CACHE = Path(__file__).resolve().parent / ".cache" / "btsettl"
_SVO = "http://svo2.cab.inta-csic.es/theory/newov2/ssap.php?model=bt-settl"

# solar-metallicity, logg 5.0 (field ultracool dwarfs) -> SVO file id
_BTSETTL_FID = {
    800: 13652, 1000: 13661, 1100: 13666, 1300: 13676,
    1400: 13681, 1700: 13696, 1900: 13706, 2100: 13730,
}


def _btsettl_path(teff: int) -> Path:
    _BTSETTL_CACHE.mkdir(parents=True, exist_ok=True)
    dat = _BTSETTL_CACHE / f"btsettl_{teff}.txt"
    if not dat.exists():
        fid = _BTSETTL_FID[teff]
        url = f"{_SVO}&fid={fid}&format=ascii"
        dat.write_bytes(urllib.request.urlopen(url, timeout=120).read())
    return dat


def load_btsettl_sed(teff: int) -> list[float]:
    """BT-Settl ascii (lambda[A], f_lambda) resampled onto the CMF grid."""
    wl, fl = [], []
    for line in _btsettl_path(teff).read_text().splitlines():
        if line.startswith("#"):
            continue
        p = line.split()
        if len(p) < 2:
            continue
        try:
            a, f = float(p[0]), float(p[1])
        except ValueError:
            continue
        if 3000.0 <= a <= 9000.0:      # visible neighbourhood only
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


# ── Y dwarfs: Morley et al. 2014 water-cloud models ──────────────────────────
# BT-Settl's 400-500 K entries are not usable here: their visible-band integral
# is non-monotonic against the 800 K model, which means the grid changes regime
# below ~600 K. Morley, Marley, Fortney et al. 2014 (2014ApJ...787...78M) is the
# grid built for this temperature range (water clouds, Teff 200-450 K).
_MORLEY_CACHE = Path(__file__).resolve().parent / ".cache" / "morley14"
_SVO_MORLEY = "http://svo2.cab.inta-csic.es/theory/newov2/ssap.php?model=morley14"
_MORLEY_FID = {400: 63, 450: 70}          # logg 5.0, fsed 5, solar metallicity


def _morley_path(teff: int) -> Path:
    _MORLEY_CACHE.mkdir(parents=True, exist_ok=True)
    dat = _MORLEY_CACHE / f"morley14_{teff}.txt"
    if not dat.exists():
        url = f"{_SVO_MORLEY}&fid={_MORLEY_FID[teff]}&format=ascii"
        dat.write_bytes(urllib.request.urlopen(url, timeout=120).read())
    return dat


def _resample(path: Path) -> list[float]:
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


def ydwarf_hex(teff: int) -> str:
    """Visible colour of a Y dwarf photosphere (Morley+ 2014 water-cloud grid)."""
    return spectrum_to_hex(_resample(_morley_path(teff)))


def ultracool_hex(teff: int) -> str:
    """Visible colour of an L/T/Y dwarf photosphere at this Teff."""
    return spectrum_to_hex(load_btsettl_sed(teff))


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
