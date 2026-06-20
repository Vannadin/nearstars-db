# 디스크 산란광 색을 Mie 산란 + 항성 조명 스펙트럼 + CIE 변환으로 합성하는 스크립트
"""Synthesize debris-disk scattered-light colors via Mie scattering.

For each belt the *visible* color is SCATTERED STARLIGHT, not thermal
emission. We compute it physically:

    scattered_SED(lambda) ∝ B_star(lambda, Teff) * Qsca(lambda; size dist, n,k)

then convert that SED to an sRGB hex via the CIE 1931 observer.

Mie efficiencies via the Bohren & Huffman bhmie algorithm (numpy, no deps
beyond numpy). Grain size distribution n(a) ∝ a^-q over [a_min, a_max].
Optical constants (n, k) are representative optical-band values per
composition class (documented as a first-order assumption; the dominant
color driver is the size parameter x = 2*pi*a/lambda, i.e. a_min vs the
optical wavelengths, which this captures correctly).

Validation: reproduces the two MEASURED colors — AU Mic (tiny blowout
grains -> blue, Krist 2005) and Fomalhaut main ring (large grains ->
neutral grey, Kalas 2005).

Usage: python3 scripts/phase3/disk_color_mie.py
"""
from __future__ import annotations
import numpy as np

# ── Bohren & Huffman Mie (bhmie) ─────────────────────────────────────────────

def mie_qsca(x: float, m: complex) -> float:
    """Scattering efficiency Q_sca for size parameter x and refractive index m."""
    if x <= 0:
        return 0.0
    nmax = int(round(x + 4.0 * x ** (1.0 / 3.0) + 2.0))
    nmx = int(max(nmax, abs(m * x)) + 16)
    # downward recurrence for logarithmic derivative D
    d = np.zeros(nmx + 1, dtype=complex)
    for n in range(nmx, 0, -1):
        d[n - 1] = (n / (m * x)) - 1.0 / (d[n] + n / (m * x))
    psi0 = np.cos(x); psi1 = np.sin(x)
    chi0 = -np.sin(x); chi1 = np.cos(x)
    xi0 = psi0 - 1j * chi0; xi1 = psi1 - 1j * chi1
    qsca = 0.0
    an_1 = bn_1 = 0.0
    for n in range(1, nmax + 1):
        psi = (2 * n - 1) * psi1 / x - psi0
        chi = (2 * n - 1) * chi1 / x - chi0
        xi = psi - 1j * chi
        da = d[n] / m + n / x
        db = d[n] * m + n / x
        an = (da * psi - psi1) / (da * xi - xi1)
        bn = (db * psi - psi1) / (db * xi - xi1)
        qsca += (2 * n + 1) * (abs(an) ** 2 + abs(bn) ** 2)
        psi0, psi1 = psi1, psi
        chi0, chi1 = chi1, chi
        xi1 = psi1 - 1j * chi1
    return (2.0 / x ** 2) * qsca


# ── CIE 1931 color (analytic gaussian fit to the color-matching functions) ────

def _g(x, a, mu, s1, s2):
    s = np.where(x < mu, s1, s2)
    return a * np.exp(-0.5 * ((x - mu) / s) ** 2)

def cie_xyz(wl_nm, spec):
    # Wyman et al. 2013 multi-lobe gaussian fit to CIE 1931 2-deg CMFs
    xbar = (_g(wl_nm, 1.056, 599.8, 37.9, 31.0) + _g(wl_nm, 0.362, 442.0, 16.0, 26.7)
            + _g(wl_nm, -0.065, 501.1, 20.4, 26.2))
    ybar = (_g(wl_nm, 0.821, 568.8, 46.9, 40.5) + _g(wl_nm, 0.286, 530.9, 16.3, 31.1))
    zbar = (_g(wl_nm, 1.217, 437.0, 11.8, 36.0) + _g(wl_nm, 0.681, 459.0, 26.0, 13.8))
    X = np.trapz(spec * xbar, wl_nm); Y = np.trapz(spec * ybar, wl_nm); Z = np.trapz(spec * zbar, wl_nm)
    return X, Y, Z

_M_XYZ2RGB = np.array([[3.2406, -1.5372, -0.4986],
                       [-0.9689, 1.8758, 0.0415],
                       [0.0557, -0.2040, 1.0570]])

def _lin_rgb(spec):
    X, Y, Z = cie_xyz(WL, spec)
    return _M_XYZ2RGB @ np.array([X, Y, Z])

SOLAR_TEFF = 5772.0

# sat: chroma factor about the grey point. 0.82 = faithful (mild desaturation,
# dust not neon); ~2.6 = the "vivid" / prettier cfg pack (saturation boosted so
# the disk colors are clearly visible), same HUE, just pushed off grey.
SAT_FAITHFUL = 0.82
SAT_VIVID = 2.6

def _to_hex(rgb, sat):
    rgb = np.clip(rgb, 1e-6, None)
    rgb = rgb / rgb.max()
    rgb = rgb.mean() + sat * (rgb - rgb.mean())   # scale chroma about grey
    rgb = np.clip(rgb, 0, None)
    rgb = rgb / max(rgb.max(), 1e-9)
    srgb = np.where(rgb <= 0.0031308, 12.92 * rgb, 1.055 * rgb ** (1 / 2.4) - 0.055)
    return "#" + "".join(f"{int(round(c * 255)):02x}" for c in np.clip(srgb, 0, 1))

def color_reflectance(qsca_lambda, sat=SAT_FAITHFUL):
    """Intrinsic dust reflectance color (star-independent), white-balanced to a
    flat illuminant: flat reflectance -> neutral grey. Matches the measured
    disk-vs-star colors (AU Mic blue, Fomalhaut grey)."""
    return _to_hex(_lin_rgb(qsca_lambda) / _lin_rgb(np.ones_like(WL)), sat)

def color_absolute(qsca_lambda, teff, sat=SAT_FAITHFUL):
    """ABSOLUTE scattered-starlight color = star_blackbody(Teff) * Qsca(lambda),
    white-balanced to the SUN (a neutral grain under a Sun-like star -> white;
    under a K/M star -> warm; under an A star -> blue-white). This is the repo
    convention (star color baked in), upgraded from crude 'star color + albedo'
    to proper grain-size Mie scattering with wavelength-dependent n,k."""
    spec = planck(WL, teff) * qsca_lambda
    return _to_hex(_lin_rgb(spec) / _lin_rgb(planck(WL, SOLAR_TEFF)), sat)


def planck(wl_nm, teff):
    wl = wl_nm * 1e-9
    h, c, kB = 6.626e-34, 3.0e8, 1.381e-23
    return (1.0 / wl ** 5) / (np.exp(h * c / (wl * kB * teff)) - 1.0)


# ── per-belt synthesis ───────────────────────────────────────────────────────

WL = np.linspace(380, 780, 41)  # optical band, nm

# Wavelength-dependent optical constants n(lambda), k(lambda), sampled at
# [400,500,600,700,800] nm from the literature and interpolated to WL. k carries
# the blue-absorption that reddens absorbing materials; transparent grains (ice,
# forsterite) get their color from grain size alone. Representative optical-band
# values from:
#   astrosil  — Draine 2003 astronomical silicate (2003ApJ...598.1017D)
#   carbon    — amorphous C, Rouleau & Martin 1991 (1991ApJ...377..526R)
#   ice       — water ice, Warren & Brandt 2008 (2008JGRD..11314220W)
#   olivine   — Mg-rich crystalline forsterite, Jäger et al. 2003 (2003A&A...408..193J)
#   tholin    — Titan organic tholin, Khare et al. 1984 (1984Icar...60..127K)
# ice_sil / sil_org are two-component grains mixed with Maxwell-Garnett
# effective-medium theory (see _BLENDS below), NOT a linear n,k average.
_WLS = np.array([400.0, 500.0, 600.0, 700.0, 800.0])
_NK = {
    "astrosil": ([1.70, 1.69, 1.69, 1.69, 1.69], [0.031, 0.017, 0.010, 0.006, 0.004]),
    "carbon":   ([1.98, 1.96, 1.95, 1.94, 1.93], [0.64, 0.58, 0.54, 0.51, 0.49]),
    "ice":      ([1.32, 1.31, 1.31, 1.31, 1.31], [1e-9, 2e-9, 1e-8, 3e-8, 6e-8]),
    "olivine":  ([1.65, 1.64, 1.64, 1.63, 1.63], [3e-4, 1.5e-4, 1e-4, 8e-5, 7e-5]),
    "tholin":   ([1.66, 1.65, 1.64, 1.63, 1.63], [0.27, 0.065, 0.022, 0.010, 0.006]),
}

# Two-component grains via Maxwell-Garnett: spherical inclusions of volume
# fraction f embedded in a host matrix, mixing the dielectric function
# eps = (n + ik)^2 (NOT a linear n,k average, which is unphysical). The
# inclusion volume fraction is derived from a 50/50 MASS split and bulk
# densities (ice 1.0, silicate 3.3, organic/tholin 1.3 g/cc), with the
# majority-volume component as the host:
#   ice_sil  — eps Eri cold ring: silicate cores (f=0.23 by vol) in an ice mantle
#   sil_org  — tau Cet broad belt: silicate inclusions (f=0.28) in an organic host
# (50/50 mass -> f_sil = (0.5/rho_sil) / (0.5/rho_sil + 0.5/rho_host).)
# MG is valid for f well below the percolation threshold (~0.3), satisfied here.
_BLENDS = {
    "ice_sil": ("ice",    "astrosil", 0.23),
    "sil_org": ("tholin", "astrosil", 0.28),
}

def _maxwell_garnett(eps_h, eps_i, f):
    """Effective dielectric of inclusions (eps_i, volume fraction f) in host eps_h."""
    num = eps_i + 2 * eps_h + 2 * f * (eps_i - eps_h)
    den = eps_i + 2 * eps_h - f * (eps_i - eps_h)
    return eps_h * num / den

def _m_single(comp):
    n_s, k_s = _NK[comp]
    n = np.interp(WL, _WLS, n_s)
    k = np.interp(WL, _WLS, k_s)
    return n + 1j * k

def _m_lambda(comp):
    if comp in _BLENDS:
        host, incl, f = _BLENDS[comp]
        eps = _maxwell_garnett(_m_single(host) ** 2, _m_single(incl) ** 2, f)
        return np.sqrt(eps)  # principal root -> n>0, k>0 for these materials
    return _m_single(comp)

def belt_color(a_min, a_max, q, comp, teff):
    """Size-distribution-integrated Qsca(lambda) with wavelength-dependent n,k.
    Returns the per-wavelength scattering efficiency (the reflectance spectrum)."""
    m = _m_lambda(comp)
    sizes = np.logspace(np.log10(a_min), np.log10(a_max), 40)  # micron
    weights = sizes ** (-q)
    qsca_lambda = np.zeros_like(WL)
    for a, w in zip(sizes, weights):
        x = 2 * np.pi * a * 1000.0 / WL  # a[µm]->nm; x=2πa/λ
        qs = np.array([mie_qsca(x[j], m[j]) for j in range(len(WL))])
        qsca_lambda += w * (a ** 2) * qs
    qsca_lambda /= np.trapz(weights * sizes ** 2, sizes)
    return qsca_lambda


def a_blow(L, M, rho=2.5):
    # radiation-pressure blowout radius [µm]; ~0.5*(L/Lsun)/(M/Msun)*(2.5/rho)
    # rho=2.5 g/cc is a representative grain-density assumption (not a measurement).
    return 0.5 * (L / M) * (2.5 / rho)


# Phase 2 provenance for the grain-size + composition inputs below (the
# scattered-light status per belt; only AU Mic + Fomalhaut-main are MEASURED
# colors, the rest are synthesized). Researched 2026-05-30, value-checked.
#   eps Eri: Backman 2009 (2009ApJ...690.1522B) silicate inner + icy/sil cold
#            15/135 um grains; Su 2017 (2017AJ....153..226S); NO scattered light
#            (HST/STIS non-detection, arXiv:2408.06973, omega<0.487).
#   Fomalhaut: cold main ring MEASURED neutral/grey (Kalas 2005 2005Natur.435.1067K,
#            Acke 2012 cometary fluffy aggregates). Inner warm + intermediate dust =
#            PR-drag fragments of the same outer belt, ~50-80% water ice by volume
#            (Sommer 2025 2503.18127) -> icy ice_sil, NOT carbon/silicate; same
#            composition as the cold ring, hence the same synthesized color.
#   Vega: featureless silicate, large blowout grains (Su 2013 2013ApJ...763..118S);
#            thermal/mm only.
#   AU Mic: MEASURED BLUE (Krist 2005 2005AJ....129.1008K, B/I~1.6; Fitzgerald 2007
#            2007ApJ...670..536F; porous aggregates Graham 2007 2007ApJ...654..595G).
#   HD 69830: crystalline olivine (Beichman 2005 2005ApJ...626.1061B; Lisse 2007
#            2007ApJ...658..584L); thermal/mm only.
#   61 Vir: no spectral features (Wyatt 2012 2012MNRAS.424.1206W); thermal/mm only.
#   tau Cet: amorphous silicate + organics (Lawler 2014 2014MNRAS.444.2665L);
#            thermal/mm only.
# q = 3.5 is the standard collisional-cascade size-distribution exponent
# (Dohnanyi 1969, 1969JGR....74.2531D).
# (belt, a_min_um or None->a_blow, a_max_um, q, comp, starL, starM, Teff)
BELTS = [
    ("eps Eri asteroid ~3AU",     2.0,  1000, 3.5, "astrosil", 0.32, 0.82, 5039),
    ("eps Eri intermediate ~20AU", None, 1000, 3.5, "astrosil", 0.32, 0.82, 5039),
    ("eps Eri cold ~64AU",        15.0, 1000, 3.5, "ice_sil",  0.32, 0.82, 5039),
    ("Fomalhaut inner warm",      None, 100,  3.5, "ice_sil", 16.63, 1.92, 8590),
    ("Fomalhaut intermediate",    None, 1000, 3.5, "ice_sil", 16.63, 1.92, 8590),
    ("Vega warm ~14AU",           None, 1000, 3.5, "astrosil", 47.2, 2.15, 9360),
    ("Vega cold ~110AU",          None, 1000, 3.5, "astrosil", 47.2, 2.15, 9360),
    ("HD 69830 warm ~1AU",        None, 100,  3.5, "olivine",  0.622, 0.863, 5394),
    ("61 Vir cold ~30AU",         None, 1000, 3.5, "astrosil", 0.8222, 0.93, 5538),
    ("tau Cet broad ~6-55AU",     None, 1000, 3.5, "sil_org",  0.488, 0.783, 5370),
    # validation against MEASURED colors:
    ("[val] AU Mic (measured BLUE)", None, 100, 3.5, "astrosil", 0.102, 0.50, 3665),
    ("[val] Fomalhaut main (measured GREY)", None, 1000, 3.5, "ice_sil", 16.63, 1.92, 8590),
]

def band_ratio(qsca, lo=445.0, hi=806.0):
    return float(np.interp(lo, WL, qsca) / np.interp(hi, WL, qsca))  # B/I reflectance ratio

if __name__ == "__main__":
    print(f"{'belt':40s} {'a_min':>6s} {'comp':9s} {'faithful':9s} {'vivid':9s} {'B/I':>5s}")
    for name, amin, amax, q, comp, L, M, teff in BELTS:
        ab = a_blow(L, M)
        am = amin if amin is not None else max(ab, 0.05)
        qsca = belt_color(am, amax, q, comp, teff)
        faith = color_reflectance(qsca, SAT_FAITHFUL)
        vivid = color_reflectance(qsca, SAT_VIVID)
        print(f"{name:40s} {am:6.2f} {comp:9s} {faith:9s} {vivid:9s} {band_ratio(qsca):5.2f}")
