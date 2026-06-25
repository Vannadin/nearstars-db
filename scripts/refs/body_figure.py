# 천체 figure 계산기 — 자전 J2(Radau-Darwin) + 조석고정 C22 + seeded Kaula 고차 지오이드
"""Body figure: rotational J2, synchronous tidal C22, and a seeded Kaula-spectrum
high-degree geoid. Grounding: docs/reference/body-figure-methodology.md.

Degree 2 is deterministic (rotation/tide). Degree 3+ is a per-body seeded synthetic
field obeying Kaula's rule s_n = K/n² (Kaula 1966), flagged synthesis-grade — to be
replaced by a heightmap-derived field at the terrain pass.
"""
import hashlib
import math
import random

G = 6.674e-11
M_EARTH = 5.972e24
R_EARTH = 6.371e6

# Kaula constant K (per-coefficient RMS = K/n²) by body class. Earth = 1e-5 anchor;
# airless/mascon-rich bodies are rougher (larger K); see methodology §5.
KAULA_K = {
    "earth_like": 1.0e-5,   # active tectonics, thick crust
    "airless_rocky": 2.5e-5,  # Moon/Mercury-like: uneroded, mascon-rich, rougher
    "icy": 1.5e-5,          # icy moons: intermediate
}


def rotational_figure(R_mean_m, M_kg, P_rot_s, nmoi):
    """Free rotator → (q, J2, flattening f) via the Radau-Darwin inversion.
    q uses the MEAN radius (Helled+2011 convention); the emit `reference_radius`
    is the equatorial radius, set separately."""
    omega = 2 * math.pi / P_rot_s
    q = omega**2 * R_mean_m**3 / (G * M_kg)
    s = 2.5 * (1 - 1.5 * nmoi)
    J2 = (q / 3) * (5 / (s**2 + 1) - 1)
    f = 1.5 * J2 + 0.5 * q
    return q, J2, f


def synchronous_figure(R_eq_m, M_kg, P_orb_s, c_sync=1.0):
    """Tidally-locked body → (q_s, J2, C22). J2 ≈ c_sync·q_s (cal. 0.9–1.1 on the
    Galilean moons); C22 = 0.3·J2 (hydrostatic J2 = 10/3·C22)."""
    n = 2 * math.pi / P_orb_s
    q_s = n**2 * R_eq_m**3 / (G * M_kg)
    J2 = c_sync * q_s
    C22 = 0.3 * J2
    return q_s, J2, C22


def kaula_field(body_name, K, n_min=3, n_max=8):
    """Seeded synthetic normalized coefficients C̄nm, S̄nm for degree n_min..n_max.
    Deterministic per body (name hash) → reproducible. s_n = K/n²."""
    seed = int(hashlib.sha256(body_name.encode()).hexdigest()[:16], 16)
    rng = random.Random(seed)
    coeffs = {}
    for n in range(n_min, n_max + 1):
        s_n = K / n**2
        for m in range(0, n + 1):
            Cbar = rng.gauss(0, s_n)
            Sbar = 0.0 if m == 0 else rng.gauss(0, s_n)
            coeffs[(n, m)] = (Cbar, Sbar)
    return coeffs


def ellipsoid_ratios(J2=None, f=None):
    """Kopernicus VertexHeightOblateAdvanced `CustomEllipsoid` a:b:c ratios, normalized
    to the polar axis (c=1; a,b >= 1). Feeds the VISUAL mesh (the Principia J2/C22 is the separate
    GRAVITY emit). Pass J2 (already φ-scaled) for a synchronous TRIAXIAL body (hydrostatic
    4:1 → a/R=1+7J2/3, b/R=1−2J2/3, c/R=1−5J2/3); pass f for a free OBLATE rotator (a=b)."""
    if f is not None:
        a = b = 1.0; c = 1.0 - f
    else:
        a, b, c = 1 + 7 * J2 / 3, 1 - 2 * J2 / 3, 1 - 5 * J2 / 3
    return a / c, b / c, 1.0


def _check():
    """Reproduce calibration anchors."""
    # Earth: q≈3.45e-3, NMoI 0.331 → J2≈1.08e-3
    q, J2, f = rotational_figure(R_EARTH, M_EARTH, 86164.0, 0.331)
    print(f"Earth   q={q:.3e} J2={J2:.4e} f=1/{1/f:.1f}  (meas J2=1.083e-3)")
    # Jupiter: mean radius 69911 km, q≈0.083, NMoI 0.265 → J2≈0.0147
    q, J2, f = rotational_figure(69.911e6, 1.898e27, 35730.0, 0.265)
    print(f"Jupiter q={q:.3e} J2={J2:.4e}            (meas J2=1.470e-2)")
    # Callisto synchronous: P 16.69 d, R 2410.3 km, M 1.076e23 → J2≈32.7e-6
    q, J2, C22 = synchronous_figure(2.4103e6, 1.076e23, 16.689 * 86400)
    print(f"Callisto q_s={q:.3e} J2={J2:.3e} C22={C22:.3e} (meas J2=32.7e-6 C22=10.2e-6)")


if __name__ == "__main__":
    _check()
