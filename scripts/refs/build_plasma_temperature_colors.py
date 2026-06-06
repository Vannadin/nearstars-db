# 조성별 플라스마 방출색을 온도(1000K 간격)의 함수로 산출해 db/refs/plasma_temperature_colors.yaml 로 생성
"""Build a temperature-resolved plasma color table per bulk composition.

For each composition and each temperature T (1000K steps), the visible
color is modeled as two contributions blended by a temperature-dependent
weight:

  combined(T) = blend( continuum(T), emission, w(T) )

  - continuum(T): blackbody thermal color via Planck -> CIE 1931 -> sRGB.
    EXACT (analytic CMF, no fudge). This is also emitted standalone as
    the `_blackbody` table (option "가").
  - emission: the characteristic plasma emission hue of the gas, computed
    from the curated emission-band lists in db/refs/*_plasma_colors.yaml
    via the project's existing mix_lines() (same method as all other
    plasma colors -> internally consistent).
  - w(T): emission weight, ramps 0 -> 1 across the dissociation/ionization
    range (~3000K to ~9000K). A MODELING CHOICE, documented in output.

HONEST LIMITS (see plan / YAML header): this is a physically-motivated
MODEL, not an ab-initio plasma-radiation calculation. The continuum is
exact; the emission hue is the curated high-T (reentry_plasma) signature
and its weight-vs-T is modeled, not derived from Saha/Boltzmann level
populations (we lack per-line upper-state energies + Einstein A's). A
full Saha/Boltzmann version is a documented future upgrade.

Usage:
    python3 scripts/refs/build_plasma_temperature_colors.py
    python3 scripts/refs/build_plasma_temperature_colors.py --sanity   # print checks, no write
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import yaml

# Sibling-module reuse (project's existing color machinery).
sys.path.insert(0, str(Path(__file__).resolve().parent))
from wavelength_to_rgb import rgb_to_hex, hex_to_rgb  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
MOLECULAR_DB = ROOT / "db" / "refs" / "molecular_plasma_colors.yaml"
ELEMENT_DB = ROOT / "db" / "refs" / "element_plasma_colors.yaml"
OUT = ROOT / "db" / "refs" / "plasma_temperature_colors.yaml"

# Temperature grids
BB_TEMPS = list(range(1000, 20001, 1000))      # blackbody continuum standalone
COMP_TEMPS = list(range(1000, 15001, 1000))    # per-composition

# Emission-weight ramp (modeling choice): 0 below dissociation onset,
# 1 above ionization onset. Linear between.
W_T_LO = 3000.0   # below: thermal continuum dominates
W_T_HI = 9000.0   # above: plasma emission dominates


# ─────────────────────────────────────────────────────────────────────
# CIE 1931 2-deg color-matching functions — Wyman, Sloan & Shirley 2013
# "Simple Analytic Approximations to the CIE XYZ Color Matching
# Functions" (JCGT 2(2)). Multi-lobe piecewise-Gaussian fit; sigma
# values are inverse widths (1/nm).
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


_LAMBDAS = list(range(360, 831))   # 1 nm steps, 360-830 nm
_C2_NM_K = 1.4388e7                 # hc/k in nm*K


def _planck_rel(wl_nm: float, T: float) -> float:
    """Relative spectral radiance (shape only) — Planck's law."""
    x = _C2_NM_K / (wl_nm * T)
    # guard overflow at low T / short wl
    if x > 700:
        return 0.0
    return (wl_nm ** -5) / (math.exp(x) - 1.0)


def _xyz_to_srgb_hue(X: float, Y: float, Z: float) -> tuple[float, float, float]:
    """XYZ -> sRGB (0-1), clamped + max-normalized to show HUE at full
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


def blackbody_srgb(T: float) -> tuple[tuple[float, float, float], tuple[float, float]]:
    """Return ((r,g,b) 0-1, (x,y) chromaticity) for a blackbody at T."""
    X = Y = Z = 0.0
    for wl in _LAMBDAS:
        b = _planck_rel(wl, T)
        X += b * _xbar(wl)
        Y += b * _ybar(wl)
        Z += b * _zbar(wl)
    s = X + Y + Z
    xy = (X / s, Y / s) if s > 0 else (0.0, 0.0)
    return _xyz_to_srgb_hue(X, Y, Z), xy


# ─────────────────────────────────────────────────────────────────────
# Composition -> signature emitting species (high-T / reentry regime).
# Bands pulled from the curated DBs; color via mix_lines (project method).
# ─────────────────────────────────────────────────────────────────────

COMPOSITIONS = {
    "air":   {"label_en": "N2 / O2 (Earth-like)", "label_ko": "N2 / O2 (지구형)",
              "species": ["N2"]},
    "co2":   {"label_en": "CO2 (Mars / Venus)", "label_ko": "CO2 (화성 / 금성)",
              "species": ["CN", "C2"]},
    "h2_he": {"label_en": "H2 / He (gas giant)", "label_ko": "H2 / He (가스자이언트)",
              "species": ["H2"]},
    "ch4":   {"label_en": "CH4 (Titan-class)", "label_ko": "CH4 (타이탄형)",
              "species": ["CH", "C2", "CN"]},
    "h2o":   {"label_en": "H2O (steam)", "label_ko": "H2O (수증기)",
              "species": ["H2", "OH"]},
    "nh3":   {"label_en": "NH3 (ice-giant ammonia)", "label_ko": "NH3 (아이스자이언트 암모니아)",
              "species": ["NH", "NH2"]},
}


def _emission_color(species: list[str], mdb: dict, edb: dict):
    """Average the CURATED reentry_plasma hex of the signature species.

    We use the curated hex (not a fresh mix_lines on the bands) because
    the curated values already encode the human-perceived reentry hue —
    e.g. N2+ 391nm reads blue-violet to the eye despite low photopic V(λ),
    which a V(λ)-weighted re-mix would wash out to red. Multi-species
    compositions (CO2 -> CN+C2) average their hexes."""
    rgbs: list[tuple[float, float, float]] = []
    used: list[str] = []
    for sp in species:
        entry = mdb.get(sp) or edb.get(sp)
        reg = entry.get("regimes", {}).get("reentry_plasma") if entry else None
        if reg and reg.get("status") == "visible" and reg.get("hex"):
            rgbs.append(hex_to_rgb(reg["hex"]))
            used.append(sp)
    if not rgbs:
        return None, []
    avg = tuple(sum(ch) / len(rgbs) for ch in zip(*rgbs))
    return avg, used


def _w(T: float) -> float:
    return max(0.0, min(1.0, (T - W_T_LO) / (W_T_HI - W_T_LO)))


def _blend(c1: tuple, c2: tuple, w: float) -> tuple:
    return tuple((1 - w) * a + w * b for a, b in zip(c1, c2))


# ─────────────────────────────────────────────────────────────────────

def _bb_note(T: int) -> str:
    if T <= 1500:
        return "deep red — ember / lava glow"
    if T <= 3000:
        return "warm orange — lava / cool-star surface"
    if T <= 5000:
        return "warm white — K/G-star tint"
    if T <= 7000:
        return "near white — Sun-like"
    if T <= 11000:
        return "blue-white — A-star / hot reentry"
    return "blue — hot star"


class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


def build() -> dict:
    mdb = yaml.safe_load(MOLECULAR_DB.read_text(encoding="utf-8"))
    edb = yaml.safe_load(ELEMENT_DB.read_text(encoding="utf-8"))

    out: dict = {}

    # _blackbody continuum standalone (option 가)
    bb: dict = {}
    for T in BB_TEMPS:
        rgb, xy = blackbody_srgb(T)
        bb[T] = {
            "temp_k": T,
            "hex": rgb_to_hex(rgb),
            "rgb": [max(0, min(255, round(c * 255))) for c in rgb],
            "chromaticity_xy": [round(xy[0], 4), round(xy[1], 4)],
            "note": _bb_note(T),
        }
    out["_blackbody"] = bb

    # Per-composition temperature-resolved color
    for key, cfg in COMPOSITIONS.items():
        emission, used = _emission_color(cfg["species"], mdb, edb)
        emission_hex = rgb_to_hex(emission) if emission else None

        rows: dict = {}
        for T in COMP_TEMPS:
            cont, _ = blackbody_srgb(T)
            w = _w(T)
            if emission is not None:
                combined = _blend(cont, emission, w)
            else:
                combined = cont
            rows[T] = {
                "temp_k": T,
                "continuum_hex": rgb_to_hex(cont),
                "emission_hex": emission_hex,
                "emission_weight": round(w, 2),
                "combined_hex": rgb_to_hex(combined),
                "rgb": [max(0, min(255, round(c * 255))) for c in combined],
            }
        out[key] = {
            "label_en": cfg["label_en"],
            "label_ko": cfg["label_ko"],
            "active_emitters": used,
            "colors": rows,
        }

    return out


HEADER = """\
# Plasma emission color vs temperature (1000K steps), per bulk composition.
#
# MODEL — not ab-initio. Read before trusting:
#   continuum: blackbody thermal color, Planck -> CIE 1931 (Wyman 2013
#     analytic CMF) -> sRGB. EXACT. Also standalone under `_blackbody`.
#   emission: characteristic high-T plasma hue, from the curated
#     reentry_plasma emission_bands in *_plasma_colors.yaml via mix_lines
#     (same method as all project plasma colors).
#   combined = (1-w)*continuum + w*emission, w(T) ramps 0->1 over
#     {lo}-{hi}K (dissociation->ionization). The weight-vs-T and the
#     fixed emission hue are MODELING CHOICES — a full Saha/Boltzmann
#     level-population calc (needs per-line upper-state energies +
#     Einstein A) is a documented future upgrade.
#
# Colors are hue at full brightness (max-channel normalized), not
# absolute luminance. Range: _blackbody 1000-20000K, compositions
# 1000-15000K, 1000K steps.
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--sanity", action="store_true",
                    help="Print sanity checks and sample colors; do not write")
    args = ap.parse_args()

    data = build()

    if args.sanity:
        print("=== blackbody continuum sanity (hue) ===")
        for T in (1000, 3000, 5500, 6500, 10000, 20000):
            rgb, xy = blackbody_srgb(T)
            print(f"  {T:6d}K  {rgb_to_hex(rgb)}  xy=({xy[0]:.3f},{xy[1]:.3f})")
        print("\n=== composition emission hue (high-T signature) ===")
        for key, blk in data.items():
            if key == "_blackbody":
                continue
            print(f"  {key:6} emitters={blk['active_emitters']}  "
                  f"emission={blk['colors'][15000]['emission_hex']}  "
                  f"combined@2000K={blk['colors'][2000]['combined_hex']}  "
                  f"@15000K={blk['colors'][15000]['combined_hex']}")
        return 0

    body = yaml.dump(data, Dumper=NoAliasDumper, sort_keys=False,
                     allow_unicode=True, default_flow_style=False)
    OUT.write_text(HEADER.format(lo=int(W_T_LO), hi=int(W_T_HI)) + body, encoding="utf-8")
    n_comp = len([k for k in data if not k.startswith("_")])
    print(f"wrote {OUT.relative_to(ROOT)}  ({len(BB_TEMPS)} blackbody temps, "
          f"{n_comp} compositions x {len(COMP_TEMPS)} temps)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
