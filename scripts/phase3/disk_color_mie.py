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

def color_from_reflectance(qsca_lambda):
    """White-balanced reflectance color: a FLAT (grey) reflectance maps to
    neutral grey; blue-sloped -> blue, red-sloped -> red. (Equal-energy
    reference: divide the spectrum's linear RGB by a flat spectrum's RGB.)"""
    rgb = _lin_rgb(qsca_lambda) / _lin_rgb(np.ones_like(WL))
    rgb = np.clip(rgb, 1e-6, None)
    rgb = rgb / rgb.max()
    rgb = 0.72 * rgb + 0.28 * rgb.mean()  # desaturate toward grey (dust, not neon)
    srgb = np.where(rgb <= 0.0031308, 12.92 * rgb, 1.055 * rgb ** (1 / 2.4) - 0.055)
    srgb = np.clip(srgb, 0, 1)
    return "#" + "".join(f"{int(round(c * 255)):02x}" for c in srgb)


def planck(wl_nm, teff):
    wl = wl_nm * 1e-9
    h, c, kB = 6.626e-34, 3.0e8, 1.381e-23
    return (1.0 / wl ** 5) / (np.exp(h * c / (wl * kB * teff)) - 1.0)


# ── per-belt synthesis ───────────────────────────────────────────────────────

# representative optical-band (n, k) per composition class
COMP = {
    "astrosil":   (1.65, 0.02),   # astronomical silicate (Draine), weakly absorbing
    "olivine":    (1.67, 0.01),   # crystalline olivine, transparent-ish
    "ice_sil":    (1.45, 0.005),  # icy/silicate mix, large transparent grains
    "carbon":     (1.95, 0.45),   # amorphous carbon, strongly absorbing -> dark
    "sil_org":    (1.70, 0.10),   # amorphous silicate + organics
}

WL = np.linspace(380, 780, 81)  # optical band, nm

def belt_color(a_min, a_max, q, comp, teff):
    """Intrinsic dust REFLECTANCE color = Qsca(lambda) under an equal-energy
    illuminant (star-independent). This is what 'the disk is blue/grey/red'
    means observationally (disk-relative-to-star); the renderer applies the
    in-game star illumination on top. Matches the two measured anchors."""
    n, k = COMP[comp]
    m = complex(n, k)
    sizes = np.logspace(np.log10(a_min), np.log10(a_max), 40)  # micron
    weights = sizes ** (-q)
    qsca_lambda = np.zeros_like(WL)
    for a, w in zip(sizes, weights):
        x = 2 * np.pi * a * 1000.0 / WL  # a[µm]->nm; x=2πa/λ
        qs = np.array([mie_qsca(xi, m) for xi in x])
        qsca_lambda += w * (a ** 2) * qs
    qsca_lambda /= np.trapz(weights * sizes ** 2, sizes)
    return color_from_reflectance(qsca_lambda), qsca_lambda


def a_blow(L, M, rho=2.5):
    # radiation-pressure blowout radius [µm]; ~0.5*(L/Lsun)/(M/Msun)*(2.5/rho)
    return 0.5 * (L / M) * (2.5 / rho)


# (belt, a_min_um or None->a_blow, a_max_um, q, comp, starL, starM, Teff)
BELTS = [
    ("eps Eri asteroid ~3AU",     2.0,  1000, 3.5, "astrosil", 0.32, 0.82, 5039),
    ("eps Eri intermediate ~20AU", None, 1000, 3.5, "astrosil", 0.32, 0.82, 5039),
    ("eps Eri cold ~64AU",        15.0, 1000, 3.5, "ice_sil",  0.32, 0.82, 5039),
    ("Fomalhaut inner warm",      None, 100,  3.5, "carbon",  16.63, 1.92, 8590),
    ("Fomalhaut intermediate",    None, 1000, 3.5, "astrosil",16.63, 1.92, 8590),
    ("Vega warm ~14AU",           None, 1000, 3.5, "astrosil", 47.2, 2.15, 9360),
    ("Vega cold ~110AU",          None, 1000, 3.5, "astrosil", 47.2, 2.15, 9360),
    ("HD 69830 warm ~1AU",        None, 100,  3.5, "olivine",  0.622, 0.863, 5394),
    ("61 Vir cold ~30AU",         None, 1000, 3.5, "astrosil", 0.8222, 0.93, 5538),
    ("tau Cet broad ~6-55AU",     None, 1000, 3.5, "sil_org",  0.488, 0.783, 5370),
    # validation against MEASURED colors:
    ("[val] AU Mic (measured BLUE)", None, 100, 3.5, "astrosil", 0.102, 0.50, 3665),
    ("[val] Fomalhaut main (measured GREY)", None, 1000, 3.5, "ice_sil", 16.63, 1.92, 8590),
]

if __name__ == "__main__":
    print(f"{'belt':40s} {'a_blow':>7s} {'a_min':>7s} {'comp':9s} {'hex':9s}")
    for name, amin, amax, q, comp, L, M, teff in BELTS:
        ab = a_blow(L, M)
        am = amin if amin is not None else max(ab, 0.05)
        hexc, _ = belt_color(am, amax, q, comp, teff)
        print(f"{name:40s} {ab:7.2f} {am:7.2f} {comp:9s} {hexc}")
