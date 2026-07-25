# 온실 상승폭(T_surf - T_eq)을 문헌 iso-Ts 격자로 추정하는 계산기 (greenhouse-warming-methodology.md)
"""Greenhouse temperature increment from a literature-anchored iso-Ts grid.

Method + citations: docs/reference/greenhouse-warming-methodology.md

This implements **Layer 3** of that doc: the fast shortcut for the common
N2-CO2(-CH4) case. It is not the general recipe. For exotic mixtures, thick
atmospheres or non-solar host spectra, the doc routes you to Layer 1 (the
Robinson & Catling 2012 analytic model) or Layer 2 (per-gas and per-pair
opacity data). Check `layer_check()` before trusting a number from here.

The grid is pinned by three published CO2-only points on the Ts = 273 K contour
(1 bar background, cloud-free 1-D radiative-convective models):

  S/S0 = 0.80 -> pCO2 = 0.01 bar   Feulner 2012 (2012RvGeo..50.2006F) sec. 5.1, late Archean
  S/S0 = 0.75 -> pCO2 = 0.06 bar   Feulner 2012, early Archean
  S/S0 = Seff_maxgh(Teff) -> 8 bar Kopparapu 2013 (arXiv 1301.6674) maximum-greenhouse limit

and two on the Ts = 288 K contour (Feulner 2012 sec. 5.1):

  S/S0 = 0.80 -> pCO2 = 0.1 bar
  S/S0 = 0.75 -> pCO2 = 0.3 bar

The third anchor moves with the host star: Kopparapu's parametric fit (their
Table 3) puts the maximum-greenhouse limit at Seff = 0.344 for the Sun but
0.227 for an M dwarf at 3050 K. The two Archean anchors are solar-spectrum
calculations and do NOT move, which is why Layer 3 is only valid for host stars
near solar Teff -- see `layer_check()`.

Usage:
  python3 scripts/refs/greenhouse_dt.py                 # validation table + NearStars bodies
  python3 scripts/refs/greenhouse_dt.py --s 0.594 --pco2 0.03 --ch4 0.003
  python3 scripts/refs/greenhouse_dt.py --seff-table     # maximum-greenhouse limit vs Teff
"""
from __future__ import annotations

import argparse
import math

# Earth's equilibrium temperature for zero albedo at 1 AU, S0 = 1361 W/m2.
TEQ_REF_K = 278.6

# Kopparapu 2013 (arXiv 1301.6674) Table 3: Seff = Seff_sun + a*T + b*T^2 + c*T^3 + d*T^4
# with T = Teff - 5780 K, valid 2600 <= Teff <= 7200 K.
KOPPARAPU_LIMITS = {
    "recent_venus":      (1.7753, 1.4316e-4, 2.9875e-9, -7.5702e-12, -1.1635e-15),
    "runaway_greenhouse": (1.0512, 1.3242e-4, 1.5418e-8, -7.9895e-12, -1.8328e-15),
    "moist_greenhouse":  (1.0140, 8.1774e-5, 1.7063e-9, -4.3241e-12, -6.6462e-16),
    "maximum_greenhouse": (0.3438, 5.8942e-5, 1.6558e-9, -3.0045e-12, -5.2983e-16),
    "early_mars":        (0.3179, 5.4513e-5, 1.5313e-9, -2.7786e-12, -4.8997e-16),
}
TEFF_SUN_K = 5780.0
# The maximum-greenhouse column: Kopparapu fixes Ts at 273 K and varies CO2 from
# 1 to 37.8 bar; the limit itself falls at pCO2 ~ 8 bar.
MAXGH_PCO2_BAR = 8.0

# Archean iso-Ts anchors (solar spectrum): (S/S0, log10 pCO2[bar]).
ISO_273_ARCHEAN = [(0.75, math.log10(0.06)), (0.80, math.log10(0.01))]
ISO_288_ARCHEAN = [(0.75, math.log10(0.30)), (0.80, math.log10(0.10))]

# Methane credit: Feulner 2012 sec. 5.3 / Kiehl & Dickinson 1987 -- a CH4 mixing
# ratio ~1e-4 lowers the CO2 needed for a given Ts by about a factor of 3.
CH4_CREDIT = 3.0
# Organic-haze anti-greenhouse: Arney 2016 (arXiv 1610.04515), optically thick.
HAZE_COOLING_MAX_K = 20.0
# Haze forms once CH4/CO2 exceeds roughly this ratio (Haqq-Misra 2008, Arney 2016).
HAZE_CH4_CO2_RATIO = 0.1


def teq(s_rel: float, albedo: float) -> float:
    """Equilibrium temperature [K] for insolation s_rel (in Earth units) and Bond albedo."""
    return TEQ_REF_K * s_rel ** 0.25 * (1.0 - albedo) ** 0.25


def _interp_log_pco2(anchors, s_rel: float) -> float:
    """Piecewise-linear log10 pCO2 vs S/S0; the end segments extrapolate."""
    pts = sorted(anchors)
    if len(pts) == 1:
        raise ValueError("need at least two anchors")
    if s_rel <= pts[0][0]:
        (s0, y0), (s1, y1) = pts[0], pts[1]
    elif s_rel >= pts[-1][0]:
        (s0, y0), (s1, y1) = pts[-2], pts[-1]
    else:
        for (s0, y0), (s1, y1) in zip(pts, pts[1:]):
            if s0 <= s_rel <= s1:
                break
    return y0 + (y1 - y0) * (s_rel - s0) / (s1 - s0)


def kopparapu_seff(teff_k: float, limit: str = "maximum_greenhouse") -> float:
    """Effective stellar flux (Earth units) at one of Kopparapu 2013's five HZ limits."""
    s0, a, b, c, d = KOPPARAPU_LIMITS[limit]
    t = teff_k - TEFF_SUN_K
    return s0 + a * t + b * t ** 2 + c * t ** 3 + d * t ** 4


def iso_pco2(s_rel: float, ts_k: float = 273.0, teff_k: float = TEFF_SUN_K) -> float:
    """CO2 partial pressure [bar] needed for surface Ts at insolation s_rel (CO2 only).

    The 273 K contour terminates at the host star's maximum-greenhouse limit; the
    288 K contour has no published end point, so below the Archean anchors it is
    extrapolated with the 273 K contour's slope (which keeps the two-contour
    spacing, and therefore the CO2 sensitivity, at its S = 0.75 value).
    """
    if ts_k == 273.0:
        anchors = [(kopparapu_seff(teff_k), math.log10(MAXGH_PCO2_BAR))] + ISO_273_ARCHEAN
        return 10.0 ** _interp_log_pco2(anchors, s_rel)
    lo = ISO_288_ARCHEAN[0][0]
    if s_rel >= lo:
        return 10.0 ** _interp_log_pco2(ISO_288_ARCHEAN, s_rel)
    shift = math.log10(iso_pco2(s_rel, 273.0, teff_k) / iso_pco2(lo, 273.0, teff_k))
    return 10.0 ** (ISO_288_ARCHEAN[0][1] + shift)


def layer_check(teff_k: float, s_rel: float, pco2_bar: float, p_total_bar: float,
                exotic: bool = False) -> list:
    """Return the reasons, if any, that Layer 3 does not apply to this body."""
    out = []
    if abs(teff_k - TEFF_SUN_K) > 800:
        out.append("host Teff %.0f K is far from solar: the Archean anchors are "
                   "solar-spectrum runs, so re-anchor (Layer 1/2) or use Ramirez 2018"
                   % teff_k)
    if not 0.30 <= s_rel <= 1.05:
        out.append("S/S0 %.3f is outside the anchored range 0.30-1.05" % s_rel)
    elif s_rel < 0.75:
        out.append("S/S0 %.3f is in the extrapolated band (0.35-0.75): +-10 K" % s_rel)
    if p_total_bar > 2.0:
        out.append("total pressure %.1f bar is a thick atmosphere: use Layer 1"
                   % p_total_bar)
    if pco2_bar > 8.0:
        out.append("pCO2 %.1f bar exceeds the maximum-greenhouse column" % pco2_bar)
    if exotic:
        out.append("mixture is outside N2-CO2-CH4: use Layer 2 opacity data")
    return out


def slope_per_decade(s_rel: float, teff_k: float = TEFF_SUN_K) -> float:
    """dTs / dlog10(pCO2) [K per decade], read off the 273 K and 288 K contour spacing.

    Below S/S0 = 0.75 both contours are extrapolated with the same slope, so the
    spacing -- and therefore this sensitivity -- freezes at its S = 0.75 value.
    """
    spacing = math.log10(iso_pco2(s_rel, 288.0, teff_k) / iso_pco2(s_rel, 273.0, teff_k))
    return 15.0 / spacing


def surface_t(s_rel: float, pco2_bar: float, ch4_bar: float = 0.0,
              hazy: bool | None = None, p_total_bar: float = 1.0,
              teff_k: float = TEFF_SUN_K) -> dict:
    """Estimate the surface temperature and the greenhouse increment.

    Returns a dict with teq/ts/delta_t plus the individual contributions.
    """
    slope = slope_per_decade(s_rel, teff_k)
    pco2_eff = pco2_bar
    ch4_gain = 0.0
    if ch4_bar > 0:
        pco2_eff *= CH4_CREDIT
        ch4_gain = slope * math.log10(CH4_CREDIT)

    if hazy is None:
        hazy = pco2_bar > 0 and (ch4_bar / pco2_bar) > HAZE_CH4_CO2_RATIO
    haze = HAZE_COOLING_MAX_K if hazy else 0.0

    # Goldblatt 2009: doubling the N2 column adds ~4.4 K via pressure broadening.
    n2_gain = 4.4 * math.log2(p_total_bar) if p_total_bar > 0 else 0.0

    iso = iso_pco2(s_rel, 273.0, teff_k)
    ts = 273.0 + slope * math.log10(pco2_eff / iso) - haze + n2_gain
    return {
        "iso273_pco2_bar": iso,
        "slope_k_per_decade": slope,
        "ch4_gain_k": ch4_gain,
        "n2_gain_k": n2_gain,
        "haze_k": -haze,
        "ts_k": ts,
    }


def greenhouse_increment(s_rel: float, pco2_bar: float, albedo: float,
                         ch4_bar: float = 0.0, hazy: bool | None = None,
                         p_total_bar: float = 1.0,
                         teff_k: float = TEFF_SUN_K) -> float:
    """The increment alone [K], for composing with a T_eq computed elsewhere.

    Ts = T_eq + this. Use it when T_eq is not the plain stellar value -- a
    satellite's four-term budget, for instance (see
    docs/reference/moon-energy-budget-methodology.md). Caveat: the contours were
    calibrated on bodies whose internal heat is negligible, so once the extra
    flux is a large fraction of the absorbed stellar flux this composition is an
    extrapolation; Barnes 2013 (arXiv 1203.5104) is the proper treatment.
    """
    r = surface_t(s_rel, pco2_bar, ch4_bar, hazy=hazy, p_total_bar=p_total_bar,
                  teff_k=teff_k)
    return r["ts_k"] - teq(s_rel, albedo)


def _row(label, s_rel, pco2, ch4, albedo, published=None, hazy=None, p_total=1.0,
         teff=TEFF_SUN_K):
    r = surface_t(s_rel, pco2, ch4, hazy=hazy, p_total_bar=p_total, teff_k=teff)
    t_eq = teq(s_rel, albedo)
    note = ""
    if published is not None:
        note = "  published %5.1f  diff %+5.1f" % (published, r["ts_k"] - published)
    print("%-34s S=%.3f pCO2=%-8.4g CH4=%-7.4g A=%.2f | Teq %5.1f  Ts %5.1f  dT %+5.1f%s"
          % (label, s_rel, pco2, ch4, albedo, t_eq, r["ts_k"], r["ts_k"] - t_eq, note))
    return r


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--s", type=float, help="insolation in Earth units (S/S0)")
    ap.add_argument("--pco2", type=float, help="CO2 partial pressure [bar]")
    ap.add_argument("--ch4", type=float, default=0.0, help="CH4 partial pressure [bar]")
    ap.add_argument("--albedo", type=float, default=0.30, help="Bond albedo")
    ap.add_argument("--ptotal", type=float, default=1.0, help="total surface pressure [bar]")
    ap.add_argument("--teff", type=float, default=TEFF_SUN_K, help="host star Teff [K]")
    ap.add_argument("--seff-table", action="store_true",
                    help="print the maximum-greenhouse limit vs host Teff")
    args = ap.parse_args()

    if args.seff_table:
        print("== Kopparapu 2013 maximum-greenhouse limit vs host star ==")
        print("Teff [K]   Seff   outer edge for L=1 Lsun [AU]")
        for teff in (2600, 3050, 3400, 4400, 5250, 5780, 5847, 6500, 7200):
            seff = kopparapu_seff(teff)
            print("  %5d   %.3f   %.2f" % (teff, seff, seff ** -0.5))
        print("(3050 K = Proxima, 5847 K = alpha Cen A; valid 2600-7200 K)")
        return

    if args.s and args.pco2:
        r = _row("query", args.s, args.pco2, args.ch4, args.albedo, p_total=args.ptotal,
                 teff=args.teff)
        for w in layer_check(args.teff, args.s, args.pco2, args.ptotal):
            print("  [layer] " + w)
        return

    print("== Validation against published runs ==")
    _row("Earth today (observed)", 1.0, 2.8e-4, 1.7e-6, 0.30, published=288.0)
    _row("Feulner 2012 late Archean 273K", 0.80, 0.01, 0.0, 0.35, published=273.0)
    _row("Feulner 2012 late Archean 288K", 0.80, 0.10, 0.0, 0.35, published=288.0)
    _row("Feulner 2012 early Archean 273K", 0.75, 0.06, 0.0, 0.35, published=273.0)
    _row("Feulner 2012 early Archean 288K", 0.75, 0.30, 0.0, 0.35, published=288.0)
    _row("Kiehl+Dickinson 1987 +CH4", 0.75, 0.10, 1e-4, 0.35, published=288.0, hazy=False)
    _row("Charnay 2013 GCM comp. C", 0.75, 0.10, 2e-3, 0.35, published=290.0, hazy=False)
    _row("Kopparapu 2013 max greenhouse", kopparapu_seff(TEFF_SUN_K), 8.0, 0.0, 0.35,
         published=273.0)

    print()
    print("== Early Mars: does the recipe reproduce the CO2-only impossibility? ==")
    iso = iso_pco2(0.32, 273.0)
    print("S=0.32 -> iso-273 needs pCO2 = %.1f bar, above the %.0f bar maximum-greenhouse"
          % (iso, 8.0))
    print("column, so CO2+H2O alone cannot reach 273 K (Kasting 1991; Ramirez 2014).")

    print()
    print("== NearStars: Polyphemus moons, alpha Cen A (L=1.521 Lsun) at 1.6 AU ==")
    s_poly = 1.521 / 1.6 ** 2
    print("S/S0 = %.4f" % s_poly)
    _row("Cassandra as written (3% CO2)", s_poly, 0.03, 3e-3, 0.35, hazy=True)
    _row("Cassandra, haze-free variant", s_poly, 0.03, 3e-3, 0.35, hazy=False)
    _row("Cassandra for Ts=273 (CO2 only)", s_poly, iso_pco2(s_poly), 0.0, 0.35)
    _row("Cassandra for Ts=273 (with CH4)", s_poly, iso_pco2(s_poly) / CH4_CREDIT, 3e-3,
         0.35, hazy=False)
    _row("Pandora as written (18% CO2)", s_poly, 0.198, 5e-3, 0.30, hazy=False, p_total=1.1)
    _row("Pandora for Ts=290 (with CH4)", s_poly, 1.15, 5e-3, 0.30, hazy=False, p_total=1.1)
    print("  [layer] " + "; ".join(layer_check(5847.0, s_poly, 0.198, 1.1)))

    print()
    print("== Host-star generalization: the same body around different stars ==")
    print("A 1 bar / 3%% CO2 / 3 mbar CH4 world at S/S0 = %.3f" % s_poly)
    for label, teff in (("alpha Cen A (5847 K)", 5847.0), ("K dwarf (4400 K)", 4400.0),
                        ("Proxima-like (3050 K)", 3050.0)):
        r = surface_t(s_poly, 0.03, 3e-3, hazy=False, teff_k=teff)
        print("  %-22s Seff_maxgh %.3f  iso-273 needs %6.2f bar  Ts %5.1f K"
              % (label, kopparapu_seff(teff), r["iso273_pco2_bar"], r["ts_k"]))
    print("  The trend is real (a cooler star's maximum-greenhouse limit sits at lower")
    print("  flux, so the same body needs less CO2), but the Archean anchors are")
    print("  solar-spectrum runs: for the M dwarf this is Layer-1/2 territory, not a")
    print("  number to quote. layer_check() says so.")


if __name__ == "__main__":
    main()
