# 원소별 재진입 플라스마 발광색을 온도(1000K 간격)의 함수로 산출해 db/refs/element_temperature_colors.yaml 생성
"""Per-element plasma emission color vs temperature (1000K steps).

The single-element analog of plasma_temperature_colors.yaml (which is per bulk
composition). Same LTE model as saha_boltzmann, run for one neutral element:

    j(λ) = thermal continuum (density·Planck)  +  neutral atomic line emission

with the neutral fraction depleted by Saha ionization as T rises. Low T → thermal
incandescence; mid T → the element's characteristic atomic lines emerge; high T →
neutral ionizes, lines fade, the thermal continuum (blue-white) takes over.

SCOPE / APPROXIMATIONS (documented):
  - Atomic only — no molecular bands (a lone element; molecular reentry colors
    live in the per-composition table). LTE.
  - Neutral-line emission only; first-ion line emission is NOT included (we lack
    X II line data for most elements), so very-high-T colors trend to the thermal
    continuum rather than showing ion lines. Saha still depletes the neutral.
  - Ion partition function approximated U_ion ≈ U_neutral in the Saha balance.
  - Only elements with NIST A-values are temperature-resolvable (~73); complex
    spectra without A (Zr, Nb, lanthanides, actinides) are omitted here — see
    the single-temperature lte_plasma regime for those.

Reads the NIST line/level cache (build_lte_plasma_colors' cache dir). Reuses the
saha_boltzmann engine constants + cie_color so this table is consistent with the
per-composition one.

Usage:
    python3 scripts/refs/build_element_temperature_colors.py
    python3 scripts/refs/build_element_temperature_colors.py --sanity
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cie_color                       # noqa: E402
import build_atomic_lines as BA        # noqa: E402
from saha_boltzmann import (           # noqa: E402
    K_EV, K_CM, K_ERG, SAHA, P_REF, N_REF, GAIN, LINE_WIDTH_NM, partition_fn,
)

ROOT = Path(__file__).resolve().parents[2]
ELEMENT_DB = ROOT / "db" / "refs" / "element_plasma_colors.yaml"
OUT = ROOT / "db" / "refs" / "element_temperature_colors.yaml"
CACHE = Path("/tmp/nist_clean")

TEMPS = list(range(1000, 15001, 1000))
BB_TEMPS = list(range(1000, 20001, 1000))

# First ionization energies [eV] (NIST recommended). Elements absent here are
# skipped (no Saha → would over-emit neutral lines at high T).
IONIZATION_EV = {
    "H": 13.598, "He": 24.587, "Li": 5.392, "Be": 9.323, "B": 8.298, "C": 11.260,
    "N": 14.534, "O": 13.618, "F": 17.423, "Ne": 21.565, "Na": 5.139, "Mg": 7.646,
    "Al": 5.986, "Si": 8.152, "P": 10.487, "S": 10.360, "Cl": 12.968, "Ar": 15.760,
    "K": 4.341, "Ca": 6.113, "Sc": 6.561, "Ti": 6.828, "V": 6.746, "Cr": 6.767,
    "Mn": 7.434, "Fe": 7.902, "Co": 7.881, "Ni": 7.640, "Cu": 7.726, "Zn": 9.394,
    "Ga": 5.999, "Ge": 7.900, "As": 9.789, "Se": 9.752, "Br": 11.814, "Kr": 14.000,
    "Rb": 4.177, "Sr": 5.695, "Y": 6.217, "Zr": 6.634, "Nb": 6.759, "Mo": 7.092,
    "Tc": 7.280, "Ru": 7.361, "Rh": 7.459, "Pd": 8.337, "Ag": 7.576, "Cd": 8.994,
    "In": 5.786, "Sn": 7.344, "Sb": 8.609, "Te": 9.010, "I": 10.451, "Xe": 12.130,
    "Cs": 3.894, "Ba": 5.212, "La": 5.577, "Ce": 5.539, "Pr": 5.473, "Nd": 5.525,
    "Pm": 5.582, "Sm": 5.644, "Eu": 5.670, "Gd": 6.150, "Tb": 5.864, "Dy": 5.939,
    "Ho": 6.022, "Er": 6.108, "Tm": 6.184, "Yb": 6.254, "Lu": 5.426, "Hf": 6.825,
    "Ta": 7.550, "W": 7.864, "Re": 7.834, "Os": 8.438, "Ir": 8.967, "Pt": 8.959,
    "Au": 9.226, "Hg": 10.438, "Tl": 6.108, "Pb": 7.417, "Bi": 7.286, "Po": 8.417,
    "Rn": 10.749, "Fr": 4.073, "Ra": 5.278, "Ac": 5.380, "Th": 6.307, "Pa": 5.890,
    "U": 6.194, "Np": 6.266, "Pu": 6.026, "Am": 5.974, "Cm": 5.991,
}

BOOL_SYM = {False: "No", True: "Yes"}


def neutral_fraction(S: float, n_heavy: float) -> float:
    """Single-element Saha: n_ion²/(n_heavy−n_ion) = S, n_e = n_ion."""
    n_ion = (-S + math.sqrt(S * S + 4.0 * S * n_heavy)) / 2.0
    return max(0.0, (n_heavy - n_ion) / n_heavy)


def element_color(lines: list[dict], levels: list[dict], chi_ev: float, T: float):
    """(hex, ionization_fraction) for a pure neutral element at temperature T."""
    n_heavy = P_REF / (K_ERG * T)
    U = partition_fn(levels, T)
    S = 2.0 * SAHA * T ** 1.5 * math.exp(-chi_ev / (K_EV * T))   # U_ion ≈ U_neutral
    f_neu = neutral_fraction(S, n_heavy)
    kt_cm = K_CM * T

    contribs = []
    for ln in lines:
        n_up = f_neu * ln["g_upper"] * math.exp(-ln["E_upper_cm"] / kt_cm) / U
        s = n_up * ln["A_ki"] * (1e7 / ln["nm"])
        if s > 0:
            contribs.append((ln["nm"], s))

    planck = [cie_color.planck_rel(lam, T) for lam in cie_color.LAMBDAS]
    pk = max(planck) or 1.0
    therm_w = n_heavy / N_REF
    inten = []
    for i, lam in enumerate(cie_color.LAMBDAS):
        emis = 0.0
        for lam0, s in contribs:
            d = (lam - lam0) / LINE_WIDTH_NM
            if -6 < d < 6:
                emis += s / (LINE_WIDTH_NM * 2.5066) * math.exp(-0.5 * d * d)
        inten.append(therm_w * planck[i] / pk + GAIN * emis)
    return cie_color.spectrum_to_hex(inten), round(1.0 - f_neu, 4)


def _bb_note(T: int) -> str:
    if T <= 1500: return "deep red — ember"
    if T <= 3000: return "orange — lava"
    if T <= 5000: return "warm white"
    if T <= 7000: return "near white"
    if T <= 11000: return "blue-white"
    return "blue"


class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


def build(sanity: bool = False) -> dict:
    edb = yaml.safe_load(ELEMENT_DB.read_text(encoding="utf-8"))
    out: dict = {"_blackbody": {}, "elements": {}}
    for T in BB_TEMPS:
        rgb, _ = cie_color.blackbody_srgb(T)
        out["_blackbody"][T] = {"temp_k": T, "hex": cie_color.rgb_to_hex(rgb),
                                "note": _bb_note(T)}

    elements = sorted(((v["atomic_number"], BOOL_SYM.get(s, s), v["name"])
                       for s, v in edb.items() if isinstance(v, dict)),
                      key=lambda t: t[0])
    skipped = []
    for z, sym, name in elements:
        chi = IONIZATION_EV.get(sym)
        lp = CACHE / f"lines_{sym.lower()}.txt"
        vp = CACHE / f"levels_{sym.lower()}.txt"
        lines = BA.parse_lines(lp.read_text(encoding="utf-8")) if lp.exists() else []
        levels = BA.parse_levels(vp.read_text(encoding="utf-8")) if vp.exists() else []
        if not lines or chi is None:
            skipped.append(sym)
            continue
        rows = {}
        for T in TEMPS:
            hexv, ionf = element_color(lines, levels, chi, T)
            rgb = cie_color.hex_to_rgb(hexv)
            rows[T] = {"temp_k": T, "hex": hexv,
                       "rgb": [round(c * 255) for c in rgb],
                       "ionization_fraction": ionf}
        out["elements"][sym] = {"z": z, "name": name, "colors": rows}
    if sanity:
        print(f"resolved {len(out['elements'])} elements; skipped {len(skipped)} "
              f"(no A-lines or no ionization energy): {skipped}")
    return out


HEADER = """\
# Per-element plasma emission color vs temperature (1000K steps) — the
# single-element analog of plasma_temperature_colors.yaml. Built by
# scripts/refs/build_element_temperature_colors.py from the saha_boltzmann engine.
#
# Model: thermal continuum (Planck->CIE, exact in _blackbody) + neutral atomic
# line emission (NIST A-values, Boltzmann), neutral fraction Saha-depleted with T.
# ATOMIC ONLY (no molecular bands), neutral lines only (no ion-line emission for
# most elements), LTE. Only elements with NIST A-values are resolvable.
# Colors are hue at full brightness (max-channel normalized).
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--sanity", action="store_true")
    args = ap.parse_args()
    data = build(sanity=args.sanity)
    if args.sanity:
        for sym in ("Na", "Cu", "Fe", "Ca", "Li", "Ba", "Hg", "Cs"):
            e = data["elements"].get(sym)
            if not e:
                print(f"  {sym}: (not resolved)"); continue
            cells = "  ".join(e["colors"][T]["hex"] for T in (2000, 4000, 6000, 8000, 12000))
            print(f"  {sym:3} (2/4/6/8/12k): {cells}")
        return 0
    OUT.write_text(HEADER + yaml.dump(data, Dumper=NoAliasDumper, sort_keys=False,
                                      allow_unicode=True, default_flow_style=False),
                   encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}  ({len(data['elements'])} elements x "
          f"{len(TEMPS)} temps)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
